"""Immutable import of local batches and explicitly requested public URLs."""
from __future__ import annotations

import hashlib
import mimetypes
import os
import shutil
import tempfile
from pathlib import Path
from urllib.parse import unquote, urlparse
from urllib.request import Request, urlopen

from .util import ArchiveError, SCHEMA_VERSION, digest_data, identifier, load_data, resolve_root, safe_path, sha256, utcnow, write_data

TEXT_FORMATS = {".pdf", ".tex", ".md", ".markdown", ".txt"}
MAX_DOWNLOAD_BYTES = 100 * 1024 * 1024


def ingest_local(root: str | Path | None, source: str | Path, *, metadata: dict | None = None, paper_id: str | None = None, version: str | None = None, source_url: str | None = None) -> dict:
    root = resolve_root(root)
    source = safe_path(root, source, must_exist=True)
    info = dict(metadata or {})
    if source.is_dir():
        forbidden = {"corpus", "src", "scripts", "lean", "examples", "catalog", "build", "reports", ".tools", ".conda-env", ".cache", ".tmp", ".git"}
        relative_parts = source.relative_to(root).parts
        if source == root or (relative_parts and relative_parts[0] in forbidden):
            raise ArchiveError("Import a dedicated source batch, not the project or generated/tool directories")
        manifest_path = safe_path(root, source / "metadata.yaml")
        if manifest_path.exists():
            parsed = load_data(manifest_path, {})
            if not isinstance(parsed, dict):
                raise ArchiveError("metadata.yaml must contain a mapping")
            info = {**parsed, **info}
        paths = []
        for base, dirs, files in os.walk(source, followlinks=False):
            for name in dirs:
                if name in forbidden:
                    raise ArchiveError(f"Batch contains project/generated directory: {name}")
            for name in dirs + files:
                safe_path(root, Path(base) / name, must_exist=True)
            dirs[:] = [name for name in dirs if not name.startswith(".")]
            paths.extend(Path(base) / name for name in sorted(files) if name != "metadata.yaml" and not name.startswith("."))
        paths.sort(key=lambda path: path.relative_to(source).as_posix())
        label = source.name
    elif source.is_file():
        paths = [source]
        label = source.stem
    else:
        raise ArchiveError("Source must be a file or directory")
    if not paths or not any(path.suffix.lower() in TEXT_FORMATS for path in paths):
        raise ArchiveError("Batch requires at least one PDF, TeX, Markdown or text source")
    entries = []
    for path in paths:
        relative = path.relative_to(source).as_posix() if source.is_dir() else path.name
        entries.append({"path": f"sources/{relative}", "sha256": sha256(path), "size": path.stat().st_size, "media_type": mimetypes.guess_type(path.name)[0] or "application/octet-stream", "role": "main" if path.suffix.lower() in TEXT_FORMATS else "attachment"})
    content_digest = digest_data([{key: entry[key] for key in ("path", "sha256")} for entry in entries])
    # Folder name is a stable manual identity; files use filename + content.
    resolved_id = identifier(paper_id or info.get("paper_id") or "manual-" + hashlib.sha256(label.encode()).hexdigest()[:16], "paper_id")
    requested_version = version or info.get("version")
    versions_dir = safe_path(root, f"corpus/papers/{resolved_id}")
    for existing in sorted(versions_dir.glob("*/manifest.yaml")) if versions_dir.exists() else []:
        current = load_data(safe_path(root, existing), {})
        if current.get("content_fingerprint") == content_digest and (not requested_version or current.get("requested_version", current.get("version")) == requested_version):
            changed = [key for key in ("title", "authors", "publication_status", "visibility", "doi", "arxiv_id", "license") if key in info and info[key] != current.get(key)]
            if changed:
                raise ArchiveError("Content is already archived but metadata differs (" + ", ".join(changed) + "); use update-metadata to record an explicit descriptive revision")
            return {**current, "idempotent": True}
    resolved_version = identifier(str(requested_version or "v1"), "version")
    destination = safe_path(root, versions_dir / resolved_version)
    if destination.exists():
        resolved_version = identifier(f"{resolved_version}-{content_digest[:12]}", "version")
        destination = safe_path(root, versions_dir / resolved_version)
        if destination.exists():
            raise ArchiveError("Version conflict: content directory already exists")
    source_type = "public_url" if source_url else info.get("source_type", "manual")
    if source_type not in {"manual", "public_url"}:
        raise ArchiveError("source_type must be manual or public_url")
    visibility = info.get("visibility", "public" if source_url else "private")
    if visibility not in {"private", "public"}:
        raise ArchiveError("visibility must be private or public")
    authors = info.get("authors", [])
    if not isinstance(authors, list):
        raise ArchiveError("authors must be a list")
    manifest = {"schema_version": SCHEMA_VERSION, "paper_id": resolved_id, "version": resolved_version, "requested_version": requested_version, "title": info.get("title") or label, "title_status": "provided" if info.get("title") else "temporary", "authors": authors, "publication_status": info.get("publication_status", "unknown" if source_url else "unpublished"), "source_type": source_type, "visibility": visibility, "source_url": source_url or info.get("source_url"), "doi": info.get("doi"), "arxiv_id": info.get("arxiv_id"), "license": info.get("license", "unknown"), "retrieved_at": utcnow(), "content_fingerprint": content_digest, "supersedes": None, "files": entries, "missing_materials": info.get("missing_materials", []), "review_status": "pending"}
    existing_versions = list(versions_dir.glob("*/manifest.yaml")) if versions_dir.exists() else []
    if existing_versions:
        previous = max((load_data(safe_path(root, path), {}) for path in existing_versions), key=lambda item: item.get("retrieved_at", ""))
        manifest["supersedes"] = previous.get("version")
    versions_dir.mkdir(parents=True, exist_ok=True)
    staging = Path(tempfile.mkdtemp(prefix=".ingest-", dir=versions_dir))
    try:
        for origin, entry in zip(paths, entries):
            target = staging / entry["path"]
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(origin, target)
            if sha256(target) != entry["sha256"]:
                raise ArchiveError("Source changed during import; retry with a stable batch")
        write_data(staging / "manifest.yaml", manifest)
        write_data(staging / "inventory.yaml", {"schema_version": SCHEMA_VERSION, "paper_id": resolved_id, "paper_version": resolved_version, "completeness_status": "not_reviewed", "extraction_status": "not_started", "denominator_reviewed": False, "items": [], "issues": ["Automatic extraction and section-by-section review are pending."]})
        os.rename(staging, destination)
    finally:
        if staging.exists():
            shutil.rmtree(staging)
    return {**manifest, "idempotent": False}


def ingest_inbox(root: str | Path | None = None) -> list[dict]:
    root = resolve_root(root)
    inbox = safe_path(root, "inbox")
    if not inbox.exists():
        return []
    results = []
    for path in sorted(inbox.iterdir()):
        safe_path(root, path, must_exist=True)
        if path.is_dir() and path.name != "example" and not path.name.startswith("."):
            results.append(ingest_local(root, path))
    return results


def ingest_url(root: str | Path | None, url: str, *, paper_id: str | None = None, version: str | None = None, title: str | None = None) -> dict:
    root = resolve_root(root)
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"} or not parsed.hostname or parsed.username or parsed.password:
        raise ArchiveError("Public import requires an unauthenticated HTTP(S) URL")
    root_tmp = safe_path(root, ".tmp")
    root_tmp.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="download-", dir=root_tmp) as temporary:
        filename = Path(unquote(parsed.path)).name or "source.pdf"
        if Path(filename).suffix.lower() not in TEXT_FORMATS:
            filename += ".pdf"
        target = Path(temporary) / filename
        request = Request(url, headers={"User-Agent": "HarsanyiArchive/0.1 (explicit public source import)"})
        with urlopen(request, timeout=45) as response, target.open("wb") as output:
            if urlparse(response.geturl()).scheme not in {"http", "https"}:
                raise ArchiveError("Redirected to a non-public protocol")
            size = 0
            while chunk := response.read(1024 * 1024):
                size += len(chunk)
                if size > MAX_DOWNLOAD_BYTES:
                    raise ArchiveError("Source exceeds the 100 MiB import limit")
                output.write(chunk)
        info = {"title": title or filename, "source_type": "public_url", "visibility": "public", "publication_status": "unknown"}
        public_id = paper_id or "url-" + hashlib.sha256(url.encode()).hexdigest()[:16]
        return ingest_local(root, target, metadata=info, paper_id=public_id, version=version, source_url=url)


def update_metadata(root, paper_id: str, version: str | None, fields: dict) -> dict:
    from .store import ArchiveStore
    root = resolve_root(root)
    paper = ArchiveStore(root).get_paper(paper_id, version)
    if not paper:
        raise ArchiveError(f"Unknown paper: {paper_id}")
    allowed = {"title", "authors", "publication_status", "visibility", "doi", "arxiv_id", "license"}
    if not fields or not set(fields) <= allowed:
        raise ArchiveError("Supply descriptive metadata fields; stable identity and sources cannot be changed")
    if "authors" in fields and not isinstance(fields["authors"], list):
        raise ArchiveError("authors must be a list")
    if "visibility" in fields and fields["visibility"] not in {"private", "public"}:
        raise ArchiveError("visibility must be private or public")
    manifest = dict(paper["manifest"])
    previous = {key: manifest.get(key) for key in fields}
    manifest.update(fields)
    if "title" in fields:
        manifest["title_status"] = "provided"
    stamp = utcnow()
    history = {"schema_version": 1, "changed_at": stamp, "previous": previous, "new": fields, "note": "Descriptive metadata revision; original source files remain immutable."}
    base = safe_path(root, paper["base_path"])
    write_data(base / "metadata-history" / (stamp.replace(":", "-") + ".json"), history)
    write_data(base / "manifest.yaml", manifest)
    return manifest
