"""Filesystem boundaries and deterministic metadata serialization."""
from __future__ import annotations

import hashlib
import json
import os
import re
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

SCHEMA_VERSION = 1
ID_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$")


class ArchiveError(ValueError):
    """An archive operation rejected invalid or unsafe input."""


def resolve_root(root: str | Path | None = None) -> Path:
    return Path(root or os.environ.get("ARCHIVE_ROOT") or Path(__file__).resolve().parents[2]).absolute().resolve()


def identifier(value: Any, field: str = "id") -> str:
    if not isinstance(value, str) or not ID_PATTERN.fullmatch(value) or value in {".", ".."}:
        raise ArchiveError(f"Invalid {field}: {value!r}")
    return value


def safe_path(root: Path, value: str | Path, *, must_exist: bool = False) -> Path:
    """Resolve a path under root, refusing symlinks and traversal at any level."""
    raw = Path(value)
    if ".." in raw.parts:
        raise ArchiveError(f"Parent traversal is forbidden: {value}")
    path = raw if raw.is_absolute() else root / raw
    try:
        relative = path.absolute().relative_to(root)
    except ValueError as exc:
        raise ArchiveError(f"Path is outside archive root: {value}") from exc
    current = root
    for part in relative.parts:
        current /= part
        if current.is_symlink():
            raise ArchiveError(f"Symlinks are forbidden: {current.relative_to(root)}")
    if not path.resolve().is_relative_to(root):
        raise ArchiveError(f"Resolved path is outside archive root: {value}")
    if must_exist and not path.exists():
        raise ArchiveError(f"Path does not exist: {value}")
    return path


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def digest_data(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode()).hexdigest()


def utcnow() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def load_data(path: Path, default: Any = None) -> Any:
    if not path.exists():
        return default
    with path.open(encoding="utf-8") as handle:
        return json.load(handle) if path.suffix == ".json" else yaml.load(handle, Loader=getattr(yaml, "CSafeLoader", yaml.SafeLoader))


def write_data(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(value, ensure_ascii=False, indent=2) + "\n" if path.suffix == ".json" else yaml.safe_dump(value, allow_unicode=True, sort_keys=False)
    write_text(path, text)


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temp = tempfile.mkstemp(prefix=".write-", dir=path.parent)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            handle.write(text)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp, path)
    finally:
        if os.path.exists(temp):
            os.unlink(temp)
