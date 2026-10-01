"""Rebuildable SQLite FTS5 index with Chinese substring fallback."""
from __future__ import annotations

import os
import re
import sqlite3
import tempfile

from .util import digest_data


def _signature(store) -> str:
    files = []
    for folder in ("corpus", "catalog"):
        base = store.path(folder)
        if base.exists():
            for path in sorted(base.rglob("*")):
                path = store.path(path)
                if path.is_file() and path.suffix.lower() in {".yaml", ".yml", ".json", ".tex", ".md", ".txt"}:
                    stat = path.stat()
                    files.append([path.relative_to(store.root).as_posix(), stat.st_mtime_ns, stat.st_size])
    return digest_data({"files": files, "public": store.public})


def _documents(store):
    for paper in store.list_papers():
        content = " ".join(str(paper.get(key, "")) for key in ("title", "authors", "doi", "arxiv_id", "paper_id", "version"))
        yield "paper", paper["paper_id"], paper.get("title", paper["paper_id"]), content, f"/papers/{paper['paper_id']}"
        for entry in paper["inventory"].get("extracted_files", []):
            text_path = store.path(f"{paper['base_path']}/{entry['text_path']}")
            if text_path.exists():
                content = text_path.read_text(encoding="utf-8")
                yield "source", f"{paper['paper_id']}:{paper['version']}:{entry['source_path']}", f"{paper['title']} — {entry['source_path']}", content, f"/papers/{paper['paper_id']}?version={paper['version']}"
    for claim in store.list_claims():
        content = "\n".join(str(claim.get(key, "")) for key in ("original_label", "original", "adaptation", "paper_id", "claim_id", "source_location", "issues"))
        yield "claim", claim["claim_id"], claim.get("original_label", claim["claim_id"]), content, f"/claims/{claim['claim_id']}"
    for theorem in store.list_theorems():
        content = "\n".join(str(theorem.get(key, "")) for key in ("title", "summary", "statement", "assumptions", "tags", "aliases", "theorem_id"))
        yield "theorem", theorem["theorem_id"], theorem.get("title", theorem["theorem_id"]), content, f"/theorems/{theorem['theorem_id']}"
        for proof in theorem.get("proofs", []):
            content = "\n".join(str(proof.get(key, "")) for key in ("title", "summary", "text", "proof_id", "dependencies", "steps"))
            yield "proof", proof["proof_id"], proof.get("title", proof["proof_id"]), content, f"/proofs/{proof['proof_id']}"
    for declaration in store.load_catalog().get("declarations", []):
        yield "declaration", declaration["name"], declaration.get("title") or declaration["name"], str(declaration), f"/library#{declaration['name']}"
    for issue in store.list_issues():
        yield "issue", issue["issue_id"], issue.get("problem", issue["issue_id"]), str(issue), f"/issues/{issue['issue_id']}"


def _index_path(store):
    return store.path("build/archive-public.sqlite" if store.public else "build/archive.sqlite")


def build_index(store) -> dict:
    destination = _index_path(store)
    destination.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix=".index-", suffix=".sqlite", dir=destination.parent)
    os.close(fd)
    count = 0
    try:
        with sqlite3.connect(temporary) as conn:
            conn.execute("CREATE TABLE documents (rowid INTEGER PRIMARY KEY, kind TEXT, id TEXT, title TEXT, content TEXT, url TEXT)")
            conn.execute("CREATE VIRTUAL TABLE documents_fts USING fts5(title, content, content='documents', content_rowid='rowid', tokenize='unicode61')")
            conn.execute("CREATE TABLE metadata (key TEXT PRIMARY KEY, value TEXT)")
            for doc in _documents(store):
                conn.execute("INSERT INTO documents(kind,id,title,content,url) VALUES (?,?,?,?,?)", doc)
                count += 1
            conn.execute("INSERT INTO documents_fts(documents_fts) VALUES ('rebuild')")
            conn.execute("INSERT INTO metadata VALUES ('signature',?)", (_signature(store),))
        os.replace(temporary, destination)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)
    return {"document_count": count, "index_path": destination.relative_to(store.root).as_posix(), "public": store.public}


def search(store, query: str, kind: str | None = None, limit: int = 50) -> list[dict]:
    if not query or not query.strip():
        return []
    limit = max(1, min(int(limit), 500))
    path = _index_path(store)
    current = False
    if path.exists():
        try:
            with sqlite3.connect(path) as conn:
                signature = conn.execute("SELECT value FROM metadata WHERE key='signature'").fetchone()
                current = bool(signature and signature[0] == _signature(store))
        except sqlite3.DatabaseError:
            pass
    if not current:
        build_index(store)
    tokens = query.strip().split()
    expression = " AND ".join('"' + token.replace('"', '""') + '"' for token in tokens)
    result = []
    with sqlite3.connect(path) as conn:
        conn.row_factory = sqlite3.Row
        constraints = " AND d.kind=?" if kind else ""
        arguments = [expression] + ([kind] if kind else []) + [limit]
        try:
            rows = conn.execute("SELECT d.*, bm25(documents_fts) AS score FROM documents_fts JOIN documents d ON d.rowid=documents_fts.rowid WHERE documents_fts MATCH ?" + constraints + " ORDER BY score LIMIT ?", arguments).fetchall()
        except sqlite3.OperationalError:
            rows = []
        result.extend(dict(row) for row in rows)
        # FTS unicode tokenizer treats uninterrupted Chinese text as a token.
        # LIKE supports Chinese substrings, original numbering and math aliases.
        escape = lambda token: token.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")
        clauses = " AND ".join("lower(d.title || ' ' || d.content || ' ' || d.id) LIKE ? ESCAPE '\\'" for _ in tokens)
        arguments = ["%" + escape(token.casefold()) + "%" for token in tokens] + ([kind] if kind else []) + [limit]
        rows = conn.execute("SELECT d.*, 0 AS score FROM documents d WHERE " + clauses + constraints + " ORDER BY kind,title LIMIT ?", arguments).fetchall()
        existing = {(item["kind"], item["id"]) for item in result}
        result.extend(dict(row) for row in rows if (row["kind"], row["id"]) not in existing)
    for item in result:
        content = item.pop("content")
        positions = [content.casefold().find(token.casefold()) for token in tokens]
        start = max(0, min((pos for pos in positions if pos >= 0), default=0) - 60)
        item["snippet"] = content[start:start + 260].replace("\n", " ")
        item.pop("rowid", None)
    return result[:limit]
