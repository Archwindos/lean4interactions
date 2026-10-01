"""Local, read-only Chinese archive views backed by the file-based store.

The app never fetches remote assets or sends paper text to another service.
Public exports must use the store's privacy-filtered view.
"""
from __future__ import annotations

import html
import re
from pathlib import Path
from typing import Any
from urllib.parse import quote

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from archive.store import ArchiveStore
from archive.util import ArchiveError, load_data


STATUS_LABELS = {
    "verified": "已验证", "passed": "通过", "complete": "已完成",
    "reviewed": "已核对", "aligned": "已对齐", "checked": "已检查",
    "pending": "待处理", "draft": "草稿", "not_started": "未开始",
    "partial": "部分完成", "in_progress": "进行中", "extracted": "已提取",
    "missing": "缺失", "missing_proof": "原证明缺失", "blocked": "有阻碍",
    "failed": "失败", "issue": "存在问题", "stale": "已过期",
    "unverified": "未验证", "not_verified": "未验证", "unknown": "尚无记录",
    "unpublished": "未发表", "published": "已发表", "private": "私有",
    "public": "公开", "candidate": "候选，未核对", "not_reviewed": "未审校",
    "awaiting_user_confirmation": "等待用户确认", "counterexample_found": "已发现反例，待确认",
    "confirmed": "用户已确认", "authorized": "用户已授权", "rejected": "用户未认可",
    "unavailable": "尚不可用", "not_checked": "未检查",
    "not_formalized": "尚未形式化",
    "false_positive": "自动提取误报", "duplicate_occurrence": "重复出现位置",
    "superseded": "已由新记录替代", "definition": "定义", "assumption": "假设",
    "empirical_observation": "经验观察",
}


def _label(value: Any) -> str:
    if value is None or value == "":
        return "尚无记录"
    if isinstance(value, dict):
        value = value.get("status", "unknown")
    return STATUS_LABELS.get(str(value), str(value))


def _items(value: Any) -> list:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    if isinstance(value, dict):
        return list(value.values())
    return [value]


def _text(value: Any) -> str:
    if isinstance(value, list):
        return "；".join(_text(x) for x in value)
    if isinstance(value, dict):
        return "；".join(f"{k}：{_text(v)}" for k, v in value.items())
    return "" if value is None else str(value)


def _identifier(item: dict, kind: str) -> str:
    return str(item.get(f"{kind}_id") or item.get("id") or "")


def _metadata(item: dict | None) -> dict:
    if not item:
        return {}
    return {**item.get("metadata", {}), **item}


def _private(item: dict) -> bool:
    item = _metadata(item)
    manifest = item.get("manifest", {})
    return bool(item.get("private", False)) or item.get("visibility", manifest.get("visibility")) == "private"


_STEP_ANCHOR = re.compile(r'<a id="(step-[1-9][0-9]*)"></a>')


def _explicit_step_ids(text: Any) -> set[str]:
    """Recognize only complete, standalone step markers outside code fences."""
    result: set[str] = set()
    in_code = False
    for line in str(text or "").splitlines():
        if line.startswith("```"):
            in_code = not in_code
        elif not in_code and (match := _STEP_ANCHOR.fullmatch(line.strip())):
            result.add(match.group(1))
    return result


def _safe_markdown(text: Any) -> str:
    """Render escaped text and one strictly defined internal step marker.

    A marker becomes generated markup; other raw HTML always remains escaped.
    Automatic IDs use a separate namespace when explicit steps exist.
    """
    blocks: list[str] = []
    paragraph: list[str] = []
    code: list[str] | None = None
    step = 0
    explicit = _explicit_step_ids(text)
    seen: set[str] = set()
    automatic_prefix = "auto-step" if explicit else "step"

    def flush() -> None:
        nonlocal step
        if paragraph:
            step += 1
            value = html.escape("\n".join(paragraph))
            blocks.append(f'<p id="{automatic_prefix}-{step}" class="proof-paragraph">{value}</p>')
            paragraph.clear()

    for line in str(text or "").splitlines():
        if line.startswith("```"):
            flush()
            if code is None:
                code = []
            else:
                blocks.append("<pre><code>" + html.escape("\n".join(code)) + "</code></pre>")
                code = None
        elif code is not None:
            code.append(line)
        elif (match := _STEP_ANCHOR.fullmatch(line.strip())):
            flush()
            anchor = match.group(1)
            if anchor not in seen:
                blocks.append(f'<span id="{anchor}" class="proof-step-anchor" aria-hidden="true"></span>')
                seen.add(anchor)
        elif re.match(r"^#{1,4} ", line):
            flush()
            level = min(len(line) - len(line.lstrip("#")) + 1, 5)
            step += 1
            blocks.append(f'<h{level} id="{automatic_prefix}-{step}">{html.escape(line.lstrip("# "))}</h{level}>')
        elif not line.strip():
            flush()
        else:
            paragraph.append(line)
    flush()
    if code is not None:
        blocks.append("<pre><code>" + html.escape("\n".join(code)) + "</code></pre>")
    return "\n".join(blocks)


def _proof_body(proof: dict) -> Any:
    return proof.get("proof_text", proof.get("proof", proof.get("body", proof.get("content", ""))))


def _proof_steps(proof: dict, entries: list[dict], *, public: bool) -> list[dict]:
    """Link only actual rendered anchors and declarations in this store view."""
    body = _safe_markdown(_proof_body(proof))
    anchors = set(re.findall(r'\bid="(step-[1-9][0-9]*)"', body))
    by_name = {_catalog_name(entry): entry for entry in entries}
    steps = []
    for index, raw in enumerate(proof.get("steps", []), 1):
        if not isinstance(raw, dict):
            continue
        step_id = str(raw.get("id", ""))
        declarations = []
        for value in raw.get("lean_declarations", []):
            name = str(value.get("name", "")) if isinstance(value, dict) else str(value)
            entry = by_name.get(name)
            if public and entry is None:
                continue
            url = "/library/" + quote(name, safe="") if entry else None
            declarations.append({
                "name": name, "url": url,
                "source_url": url + "#source" if url and entry.get("source_path") and not public else None,
            })
        steps.append({
            "id": step_id, "title": raw.get("title") or f"步骤 {index}",
            "url": "#" + step_id if step_id in anchors else None,
            "declarations": declarations,
        })
    return steps


def _catalog_entries(catalog: dict) -> list[dict]:
    value = catalog.get("declarations", catalog.get("entries", catalog.get("api", [])))
    return [_metadata(item) for item in _items(value) if isinstance(item, dict)]


def _catalog_name(item: dict) -> str:
    return str(item.get("declaration") or item.get("declaration_name") or item.get("name") or item.get("lean_name") or "")


def create_app(root: str | Path | None = None, store: ArchiveStore | None = None, public: bool = True, collection: str = "public") -> FastAPI:
    store = store or ArchiveStore(root=root, collection=collection if public else "private")
    if public and hasattr(store, "public_view"):
        store = store.public_view()
    project_root = Path(root or store.root).resolve()
    templates = Jinja2Templates(directory=str(project_root / "web" / "templates"))
    templates.env.filters.update(status_label=_label, text=_text, safe_markdown=_safe_markdown)
    templates.env.globals.update(entity_id=_identifier, catalog_name=_catalog_name, quote=lambda x: quote(str(x), safe=""))
    app = FastAPI(title="Harsanyi 证明档案库", docs_url=None, redoc_url=None)
    app.state.store = store
    app.state.root = project_root
    app.state.public = public
    app.mount("/static", StaticFiles(directory=str(project_root / "web" / "static")), name="static")

    @app.exception_handler(ArchiveError)
    async def archive_error(request: Request, exc: ArchiveError) -> JSONResponse:
        return JSONResponse({"detail": "条目或路径不可用"}, status_code=404)

    def visible(kind: str, item: dict) -> bool:
        if not public:
            return True
        # A missing privacy API fails closed; private-derived metadata is not
        # made public merely because it lacks an explicit private flag.
        checker = getattr(store, "is_public", None)
        if checker:
            try:
                return bool(checker(kind, _identifier(item, kind)))
            except TypeError:
                return bool(checker(item))
        return False

    def catalog() -> dict:
        result = store.load_catalog() or {}
        # The privacy-filtered store also handles declarations with no archive
        # theorem and removes private proof/source metadata transitively.
        return result

    def dependencies(values: list, entries: list[dict]) -> list[dict]:
        names = {_catalog_name(entry): entry for entry in entries}
        links = []
        for raw in values:
            dep_id = str(raw.get("id", "")) if isinstance(raw, dict) else str(raw)
            title = raw.get("title") if isinstance(raw, dict) else None
            url = None
            if dep_id in names:
                url = "/library/" + quote(dep_id, safe="")
                title = title or names[dep_id].get("title")
            else:
                for route, getter in (("theorems", store.get_theorem), ("proofs", store.get_proof), ("claims", store.get_claim)):
                    try:
                        related = getter(dep_id)
                    except ArchiveError:
                        related = None
                    if related:
                        url = "/" + route + "/" + quote(dep_id, safe="")
                        title = title or related.get("title")
                        break
            if url or not public:
                links.append({"id": dep_id, "title": title or dep_id, "url": url})
        return links

    def claim_evidence_files(item: dict) -> list[dict]:
        report_path = item.get("verification_evidence", {}).get("report_path")
        if not report_path:
            return []
        files = [{"path": report_path, "title": "独立验证报告"}]
        try:
            report = load_data(store._evidence_path(report_path), {})
            candidates = [(record.get("path"), "Lean 源码", {".lean"}) for record in report.get("source_files", [])]
            candidates += [(record.get("log_path"), "验证日志", {".log", ".txt"}) for record in report.get("commands", [])]
            prefix = tuple(Path(report_path).parts[:-1])
            for relative, title, suffixes in candidates:
                if not isinstance(relative, str):
                    continue
                path = Path(relative)
                if path.is_absolute() or path.parts[:len(prefix)] != prefix or path.suffix not in suffixes:
                    continue
                candidate = store._evidence_path(path)
                normalized = candidate.relative_to(project_root).as_posix()
                if candidate.is_file() and normalized not in {file["path"] for file in files}:
                    files.append({"path": normalized, "title": title})
        except (ArchiveError, OSError, KeyError, TypeError, ValueError):
            pass
        return files

    def render(request: Request, template: str, **context: Any) -> HTMLResponse:
        return templates.TemplateResponse(request=request, name=template, context={
            "request": request, "public_mode": public, "page_title": "证明档案库",
            "is_private": _private, "metadata": _metadata,
            "math_renderer": (project_root / "web/static/vendor/katex/katex.min.js").is_file(),
            **context,
        })

    def require(kind: str, item: dict | None) -> dict:
        if item is None or not visible(kind, item):
            raise HTTPException(404, "没有找到该条目")
        return _metadata(item)

    @app.get("/health")
    def health() -> dict:
        return {"status": "ok", "public_mode": public}

    @app.get("/", response_class=HTMLResponse)
    def home(request: Request) -> HTMLResponse:
        papers = [item for item in store.list_papers() if visible("paper", item)]
        return render(request, "index.html", papers=papers, coverage=store.coverage() if not public else {}, page_title="Harsanyi 证明档案库")

    @app.get("/papers", response_class=HTMLResponse)
    def papers(request: Request) -> HTMLResponse:
        return render(request, "papers.html", papers=[item for item in store.list_papers() if visible("paper", item)], page_title="论文")

    @app.get("/papers/{paper_id}", response_class=HTMLResponse)
    def paper(request: Request, paper_id: str, version: str | None = None) -> HTMLResponse:
        item = require("paper", store.get_paper(paper_id, version=version))
        for source in item.get("manifest", {}).get("files", []):
            if source.get("path") and item.get("base_path"):
                path = Path(str(item["base_path"]))
                if path.is_absolute():
                    try:
                        path = path.relative_to(project_root)
                    except ValueError:
                        continue
                source["download_path"] = (path / source["path"]).as_posix()
        inventory = item.get("inventory", {})
        claims = [_metadata(x) for x in _items(item.get("claims", inventory.get("claims", inventory.get("items", [])))) if isinstance(x, dict)]
        rows = {row.get("claim_id"): row for row in inventory.get("items", [])}
        for claim_item in claims:
            row = rows.get(claim_item.get("claim_id"), {})
            for key in ("kind", "disposition", "canonical_claim_id"):
                if key in row:
                    claim_item[key] = row[key]
        if public:
            claims = [claim for claim in claims if visible("claim", claim)]
        return render(request, "paper.html", paper=item, claims=claims, page_title=item.get("title", item.get("manifest", {}).get("title", paper_id)))

    @app.get("/theorems", response_class=HTMLResponse)
    def theorems(request: Request) -> HTMLResponse:
        return render(request, "theorems.html", theorems=[_metadata(x) for x in store.list_theorems() if visible("theorem", x)], page_title="公共数学结果")

    @app.get("/theorems/{theorem_id}", response_class=HTMLResponse)
    def theorem(request: Request, theorem_id: str) -> HTMLResponse:
        item = require("theorem", store.get_theorem(theorem_id))
        proofs = [_metadata(x) for x in _items(item.get("proofs", [])) if isinstance(x, dict) and visible("proof", x)]
        claims = [_metadata(x) for x in _items(item.get("claims", [])) if isinstance(x, dict) and visible("claim", x)]
        entries = [x for x in _catalog_entries(catalog()) if x.get("theorem_id") == theorem_id]
        return render(request, "theorem.html", theorem=item, proofs=proofs, claims=claims, entries=entries, page_title=item.get("title", theorem_id))

    @app.get("/proofs/{proof_id}", response_class=HTMLResponse)
    def proof(request: Request, proof_id: str) -> HTMLResponse:
        item = require("proof", store.get_proof(proof_id))
        theorem_id = item.get("theorem_id")
        result = store.get_theorem(theorem_id) if theorem_id else None
        theorem_item = _metadata(result) if result else {}
        claims = [_metadata(x) for x in _items(theorem_item.get("claims", [])) if isinstance(x, dict) and visible("claim", x)]
        all_entries = _catalog_entries(catalog())
        entries = [x for x in all_entries if x.get("proof_id") == proof_id or (not x.get("proof_id") and x.get("theorem_id") == theorem_id)]
        return render(request, "proof.html", proof=item, theorem=theorem_item, claims=claims, entries=entries,
                      steps=_proof_steps(item, all_entries, public=public),
                      dependency_links=dependencies(item.get("dependencies", []), all_entries),
                      lean_dependency_links=dependencies(item.get("lean_dependencies", []), all_entries),
                      page_title=item.get("title", proof_id))

    @app.get("/claims/{claim_id}", response_class=HTMLResponse)
    def claim(request: Request, claim_id: str) -> HTMLResponse:
        getter = getattr(store, "get_claim", None)
        item = getter(claim_id) if getter else None
        if item is None:
            for source in store.list_papers():
                full = store.get_paper(_identifier(source, "paper"), version=source.get("version")) or {}
                item = next((x for x in _items(full.get("claims", [])) if _identifier(_metadata(x), "claim") == claim_id), None)
                if item is not None:
                    break
        item = require("claim", item)
        return render(request, "claim.html", claim=item, verification_files=claim_evidence_files(item) if not public else [],
                      page_title=item.get("title", claim_id))

    @app.get("/issues", response_class=HTMLResponse)
    def issues_page(request: Request) -> HTMLResponse:
        getter = getattr(store, "list_issues", None)
        issues = [_metadata(x) for x in getter()] if getter else []
        return render(request, "issues.html", issues=issues, page_title="数学问题记录")

    @app.get("/issues/{issue_id}", response_class=HTMLResponse)
    def issue_page(request: Request, issue_id: str) -> HTMLResponse:
        getter = getattr(store, "get_issue", None)
        item = require("issue", getter(issue_id) if getter else None)
        return render(request, "issue.html", issue=item, page_title=item.get("title", issue_id))

    @app.get("/search", response_class=HTMLResponse)
    def search(request: Request, q: str = "", kind: str | None = None) -> HTMLResponse:
        q = q.strip()
        if len(q) > 500:
            raise HTTPException(400, "搜索词请限制为 500 字符")
        results = store.search(q, kind=kind or None, limit=100) if q else []
        if public:
            # Search uses a separately built index from the public store.
            # Source and declaration IDs are not archive entity IDs.
            results = list(results)
        for result in results:
            if result.get("kind") == "declaration":
                result["url"] = "/library/" + quote(str(result.get("id", "")), safe="")
        return render(request, "search.html", query=q, kind=kind or "", results=results, page_title="检索")

    @app.get("/library", response_class=HTMLResponse)
    def library(request: Request) -> HTMLResponse:
        index = catalog()
        return render(request, "library.html", catalog=index, entries=_catalog_entries(index), page_title="Lean 公共库 API")

    @app.get("/library/{declaration:path}", response_class=HTMLResponse)
    def declaration_page(request: Request, declaration: str) -> HTMLResponse:
        index = catalog()
        entry = next((x for x in _catalog_entries(index) if _catalog_name(x) == declaration or x.get("id") == declaration), None)
        if entry is None:
            raise HTTPException(404, "目录中没有该声明")
        source_text = None
        source_start = None
        path = entry.get("source_path", entry.get("source_file"))
        if isinstance(entry.get("source"), dict):
            path = path or entry["source"].get("path")
        if path and not public:
            try:
                source = resolve_file(str(path))
                if source.suffix == ".lean":
                    lines = source.read_text(encoding="utf-8").splitlines()
                    start = entry.get("line_start", entry.get("line", entry.get("source_line", 1)))
                    start = max(int(start), 1)
                    following = [int(other.get("line", other.get("line_start", 0))) for other in _catalog_entries(index)
                                 if other.get("source_path") == path and int(other.get("line", other.get("line_start", 0))) > start]
                    end = entry.get("line_end", min(following) - 1 if following else len(lines))
                    source_text = "\n".join(lines[start - 1:int(end)])
                    source_start = start
            except (HTTPException, OSError, ValueError, TypeError):
                pass
        reading_steps = []
        if entry.get("proof_id"):
            linked_proof = store.get_proof(entry["proof_id"])
            if linked_proof:
                for step in _proof_steps(linked_proof, _catalog_entries(index), public=public):
                    if step["url"] and any(link["name"] == _catalog_name(entry) for link in step["declarations"]):
                        reading_steps.append({"title": step["title"], "url": "/proofs/" + quote(entry["proof_id"], safe="") + step["url"]})
        return render(request, "declaration.html", entry=entry, catalog=index, source_text=source_text,
                      source_start=source_start, reading_steps=reading_steps, page_title=_catalog_name(entry))

    def resolve_file(relative: str) -> Path:
        path = Path(relative)
        if path.is_absolute() or ".." in path.parts or "\\" in relative or not path.parts:
            raise HTTPException(404, "文件路径不可用")
        if path.parts[0] not in {"lean", "reports", "catalog", "corpus", "examples"}:
            raise HTTPException(404, "文件路径不可用")
        candidate = store.path(path, must_exist=True)
        if not candidate.is_file():
            raise HTTPException(404, "文件不存在")
        # Corpus metadata are presented through typed routes, not raw downloads.
        if path.parts[0] == "corpus":
            parts=path.parts
            if len(parts)>6 and parts[1]==store.collection and parts[2]=="papers" and parts[5]=="sources":
                paper=store.get_paper(parts[3],version=parts[4])
                if not paper:raise HTTPException(404,"文件路径不可用")
            else:
                if len(parts)<6 or parts[1]!=store.collection or parts[2]!="claims" or parts[4]!="lean":
                    raise HTTPException(404,"文件路径不可用")
                item=store.get_claim(parts[3])
                if item is None or not visible("claim",item) or relative not in {file["path"] for file in claim_evidence_files(item)}:
                    raise HTTPException(404,"文件路径不可用")
        if candidate.suffix.lower() not in {".lean", ".json", ".log", ".txt", ".md", ".pdf", ".tex", ".yaml"}:
            raise HTTPException(404, "不支持该文件类型")
        return candidate

    @app.get("/files/{relative:path}", response_model=None)
    def file(relative: str) -> FileResponse | JSONResponse:
        if public:
            if relative == "catalog/library.json":
                return JSONResponse(catalog())
            # Raw source/log files can contain private neighbouring declarations
            # or paths. A public export needs explicit, sanitized artifacts.
            raise HTTPException(404, "公开视图不提供未经脱敏的文件")
        return FileResponse(resolve_file(relative))

    return app
