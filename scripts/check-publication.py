#!/usr/bin/env python3
"""Audit public files without printing source text or credential values.

Run after sourcing scripts/env.sh. The default audits exact index blobs, so
forced additions and content differing from the working tree are checked too.
--worktree audits tracked and non-ignored candidate files before staging.
This is a guard against known local private data, not a proof that arbitrary
unlabelled new manuscripts are public. Keep new local papers in inbox/.
"""
from __future__ import annotations

import argparse
import collections
import hashlib
import html
import json
import os
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys

import yaml

ROOT = Path(__file__).resolve().parents[1]
CACHE_PARTS = {".git", ".conda-env", ".tools", ".cache", ".tmp", ".lake", "node_modules", "__pycache__", ".pytest_cache", ".venv", "venv"}
PRIVATE_COMPONENT = re.compile(r"maintext|manual-draft|未发表|未发布|未公开|待发表", re.I)
PRIVATE_DIR_NAMES = {"private", "unpublished", "private-papers", "unpublished-papers"}
GENERIC_ROOTS = {"src", "scripts", "tests", "templates", "docs"}
TEXT_EXTENSIONS = {".txt", ".tex", ".md", ".html", ".json", ".yaml", ".yml", ".py", ".js", ".lean", ".log", ".csv"}
OFFICIAL_PDFS = {
    "research/paper-survey-20260930/earlier/venue-papers/sparse-cvpr2023-main/sparse-cvpr2023-main.pdf",
    "research/paper-survey-20260930/earlier/venue-papers/sparse-cvpr2023-supp/sparse-cvpr2023-supp.pdf",
    "research/paper-survey-20260930/recent/pdf/iclr2024-sparse.pdf",
    "research/paper-survey-20260930/recent/pdf/iclr2024-generalizable.pdf",
}


def git(*args: str) -> bytes:
    result = subprocess.run(["git", "-C", str(ROOT), *args], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    if result.returncode:
        raise RuntimeError("Git command failed: " + " ".join(args[:2]))
    return result.stdout


def contained(path: Path) -> bool:
    return path.resolve().is_relative_to(ROOT)


def local_read(path: Path) -> bytes:
    if not contained(path) or path.is_symlink():
        raise RuntimeError("Refusing to read a file outside the project or through a symlink")
    return path.read_bytes()


def load_local(path: Path):
    return yaml.safe_load(local_read(path)) or {}


def declared_private(data) -> bool:
    if isinstance(data, dict):
        if str(data.get("visibility", "")).lower() in {"private", "restricted"}:
            return True
        if str(data.get("publication_status", "")).lower() in {"unpublished", "private"}:
            return True
        return any(declared_private(value) for value in data.values())
    if isinstance(data, list):
        return any(declared_private(value) for value in data)
    return False


def discover_private() -> tuple[set[str], set[str]]:
    roots: set[str] = {"corpus/private"}
    identifiers: set[str] = set()
    for pattern in ("corpus/papers/*/*/manifest.yaml", "corpus/claims/*/metadata.yaml", "corpus/issues/*.yaml", "corpus/private/papers/*/*/manifest.yaml", "corpus/private/claims/*/metadata.yaml", "corpus/private/issues/*.yaml", "corpus/private/reviews/**/*.yaml", "corpus/public/papers/*/*/manifest.yaml", "corpus/public/claims/*/metadata.yaml"):
        for path in ROOT.glob(pattern):
            data = load_local(path)
            if declared_private(data):
                location = path.parent.parent if path.name == "manifest.yaml" else path.parent if path.name == "metadata.yaml" else path
                roots.add(location.relative_to(ROOT).as_posix())
                for key in ("paper_id", "claim_id", "issue_id"):
                    value = data.get(key)
                    if isinstance(value, str):
                        identifiers.add(value)
    for base, directories, files in os.walk(ROOT, followlinks=False):
        directories[:] = [name for name in directories if name not in CACHE_PARTS and name != "browser-tools"]
        for name in directories + files:
            if PRIVATE_COMPONENT.search(name) or name.lower() in PRIVATE_DIR_NAMES:
                roots.add((Path(base) / name).relative_to(ROOT).as_posix())
    inbox = ROOT / "inbox"
    if inbox.is_dir():
        roots.update(path.relative_to(ROOT).as_posix() for path in inbox.iterdir() if path.name != "README.md")
    local = ROOT / "corpus/relations-local-private.yaml"
    if local.exists():
        roots.add(local.relative_to(ROOT).as_posix())
    return roots, identifiers


def under(path: str, roots: set[str]) -> bool:
    return any(path == base or path.startswith(base + "/") for base in roots)


def words(data: str) -> list[str]:
    data = html.unescape(re.sub(r"<[^>]+>", " ", data))
    return re.findall(r"[\w]+", data.lower())


def shingles(data: str) -> set[tuple[str, ...]]:
    tokens = words(data)
    result = set()
    width = sum(len(token) for token in tokens[:18])
    for index in range(len(tokens) - 17):
        if width >= 100:
            result.add(tuple(tokens[index:index + 18]))
        if index + 18 < len(tokens):
            width += len(tokens[index + 18]) - len(tokens[index])
    return result


def overlaps_private(data: str, private_text: set[tuple[str, ...]]) -> bool:
    tokens = words(data)
    matches = set()
    for index in range(len(tokens) - 17):
        window = tuple(tokens[index:index + 18])
        if window in private_text:
            matches.add(window)
            if len(matches) >= 3:
                return True
    return False


def private_fingerprints(roots: set[str]):
    hashes: dict[str, set[int]] = collections.defaultdict(set)
    source_shingles: set[tuple[str, ...]] = set()
    paths = set()
    for location in roots:
        path = ROOT / location
        candidates = path.rglob("*") if path.is_dir() else [path]
        for candidate in candidates:
            if not candidate.is_file() or candidate.is_symlink() or not contained(candidate):
                continue
            if candidate.stat().st_size > 40 * 1024 * 1024:
                continue
            paths.add(candidate)
    for path in paths:
        data = local_read(path)
        if data and path.suffix != ".log":
            hashes[hashlib.sha256(data).hexdigest()].add(len(data))
        if path.suffix in {".txt", ".tex", ".md"}:
            try:
                source_shingles.update(shingles(data.decode("utf-8")))
            except UnicodeDecodeError:
                pass
    # Shared mathematical prose can originate in published papers too. Remove
    # those matches before checking private text overlaps.
    public_text = set()
    public_manifests = list(ROOT.glob("corpus/public/papers/*/*/manifest.yaml")) + list(ROOT.glob("corpus/papers/*/*/manifest.yaml"))
    for manifest in public_manifests:
        if declared_private(load_local(manifest)):
            continue
        for path in manifest.parent.rglob("*"):
            if not path.is_file() or path.is_symlink() or not contained(path):
                continue
            data = local_read(path)
            hashes.pop(hashlib.sha256(data).hexdigest(), None)
            if path.suffix in {".txt", ".tex", ".md"}:
                public_text.update(shingles(data.decode("utf-8", errors="replace")))
    for pattern in ("research/full-proof-integration-20260930/*/source-evidence/*.txt", "research/reader-v2-20260930/math/source-review/*.txt", "corpus/public/reader/*/source-evidence/*.txt"):
        for path in ROOT.glob(pattern):
            if not under(path.relative_to(ROOT).as_posix(), roots) and contained(path):
                public_text.update(shingles(local_read(path).decode("utf-8", errors="replace")))
    return hashes, source_shingles - public_text, len(paths)


def path_rules(path: str, private_roots: set[str]) -> list[str]:
    parts = PurePosixPath(path).parts
    rules = []
    if not parts or PurePosixPath(path).is_absolute() or ".." in parts:
        rules.append("unsafe-path")
    if any(part in CACHE_PARTS or part.endswith(".egg-info") for part in parts):
        rules.append("dependency-or-cache")
    if len(parts)>1 and parts[0]=="corpus" and parts[1] in {"papers","claims","theorems","issues","reviews"} or path.startswith("corpus/relations"):
        rules.append("inactive-legacy-corpus")
    if any(part.startswith((".ingest-", ".migration-", ".promote-")) for part in parts):
        rules.append("unfinished-migration-or-import-staging")
    if "build" in parts or "browser-tools" in parts:
        rules.append("generated-build-or-browser-download")
    if under(path, private_roots):
        rules.append("local-private-material")
    if any(PRIVATE_COMPONENT.search(part) or part.lower() in PRIVATE_DIR_NAMES for part in parts):
        rules.append("unpublished-path")
    if path.startswith(("reports/acceptance/", "reports/web/", "reports/performance/20260930-coverage-read/")) or path.endswith("/evidence/production-baseline.json"):
        rules.append("historical-private-snapshot")
    if path in {"docs/history/readme-before-full-integration-20260930.md", "docs/history/status-before-full-integration-20260930.md"}:
        rules.append("historical-private-review")
    if path == "scripts/upload-github.local.sh":
        rules.append("local-only-upload-helper")
    filename = parts[-1] if parts else ""
    if (filename in {".env", ".netrc", ".npmrc", ".pypirc"} or filename.startswith(".env.") and filename != ".env.example"
            or any(part in {".aws", ".ssh"} for part in parts) or filename.endswith((".pem", ".key")) or "credentials" in filename.lower()):
        rules.append("credential-file")
    if filename.endswith((".olean", ".ilean", ".trace", ".o", ".a", ".so", ".dll", ".dylib", ".pyc", ".pyo")):
        rules.append("compiled-artifact")
    if path.startswith("research/paper-survey-20260930/") and path not in OFFICIAL_PDFS:
        if filename.endswith((".pdf", ".bin", ".tar", ".zip", ".gz", ".zst", ".html", ".atom", ".xml")) or filename in {"pages.json", "layout.txt", "text.txt"} or "/recent/text/" in path:
            rules.append("uncollected-survey-download")
    return rules


def candidates(worktree: bool):
    if worktree:
        names = git("ls-files", "--cached", "--others", "--exclude-standard", "-z").decode().split("\0")
        for name in sorted(set(names) - {""}):
            path = ROOT / name
            if path.is_symlink():
                yield name, "120000", os.readlink(path).encode()
            elif path.is_file():
                yield name, "100644", local_read(path)
    else:
        records = git("ls-files", "--stage", "-z").decode().split("\0")
        for record in records:
            if not record:
                continue
            details, name = record.split("\t", 1)
            mode, oid, stage = details.split()
            if stage != "0":
                yield name, "unmerged", b""
            elif mode == "160000":
                yield name, mode, b""
            else:
                yield name, mode, git("cat-file", "blob", oid)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--worktree", action="store_true", help="check candidate working-tree files before staging")
    parser.add_argument("--report", type=Path, help="write a paths-and-findings-only JSON report inside this project")
    args = parser.parse_args()
    if not (ROOT / ".git").is_dir():
        raise RuntimeError("Initialize this project repository before auditing; parent repositories are not consulted")
    if Path(git("rev-parse", "--show-toplevel").decode().strip()) != ROOT:
        raise RuntimeError("Git repository must be rooted at this project")
    manifest_path = ROOT / "corpus/public/reader/input-manifest.json"
    if manifest_path.exists():
        active = load_local(manifest_path)
        paper_ids=[item.get('paper_id') for item in active.get('papers',[])]
        if not paper_ids or any(not isinstance(x,str) or not x for x in paper_ids) or len(paper_ids)!=len(set(paper_ids)):
            raise RuntimeError('Active reader requires a nonempty explicit manifest with unique paper IDs')
        if active.get('visibility')!='public' or active.get('publication_status')!='published':
            raise RuntimeError('Active reader manifest is not public/formal')
        for item in active["papers"]:
            meta_rel=item['metadata_path']
            if not meta_rel.startswith('corpus/public/reader/'+item['paper_id']+'/') or '..' in Path(meta_rel).parts:
                raise RuntimeError('Active metadata is outside its paper directory')
            meta_path = ROOT / meta_rel
            if not meta_path.is_file():raise RuntimeError('Active formal metadata is missing')
            metadata = load_local(meta_path)
            if metadata.get("visibility") != "public" or metadata.get("publication_status") != "published":
                raise RuntimeError("Active reader metadata is not public/formal")
            for source in metadata.get("sources", []):
                source_path = source.get("local_path", "")
                if not source_path.startswith("corpus/public/reader/" + item["paper_id"] + "/") or ".." in Path(source_path).parts:
                    raise RuntimeError("Active formal source is outside its paper directory")
                if source.get("visibility") != "public" or source.get("publication_status") != "published":
                    raise RuntimeError("Active reader source is not public/formal")
                if not (ROOT / source_path).is_file():
                    raise RuntimeError("Active formal source is missing")
                if not source.get("sha256"):
                    raise RuntimeError("Active formal source has no pinned hash")
                if hashlib.sha256(local_read(ROOT / source_path)).hexdigest() != source["sha256"]:
                    raise RuntimeError("Active formal source hash changed")
                OFFICIAL_PDFS.add(source_path)
    private_roots, identifiers = discover_private()
    hashes, private_text, private_count = private_fingerprints(private_roots)
    forbidden = []
    warnings = []
    count = 0
    size = 0
    largest = []
    for name, mode, data in candidates(args.worktree):
        count += 1
        size += len(data)
        largest.append((len(data), name))
        rules = path_rules(name, private_roots)
        if mode in {"160000", "unmerged"}:
            rules.append("submodule-or-unmerged-index")
        if mode == "120000":
            target = (ROOT / name).parent / data.decode(errors="replace")
            if not contained(target):
                rules.append("symlink-outside-project")
            elif under(target.resolve().relative_to(ROOT).as_posix(), private_roots):
                rules.append("symlink-to-private-material")
        if len(data) > 95 * 1024 * 1024:
            rules.append("oversized-git-blob")
        digest = hashlib.sha256(data).hexdigest()
        if data and digest in hashes:
            rules.append("exact-private-copy")
        filename = PurePosixPath(name)
        if filename.suffix in TEXT_EXTENSIONS and len(data) <= 40 * 1024 * 1024:
            try:
                content = data.decode("utf-8")
            except UnicodeDecodeError:
                content = ""
            if content:
                generic = filename.parts[0] in GENERIC_ROOTS or name in {"AGENTS.md", "PLAN.md", "README.md", ".gitignore"}
                if filename.suffix in {".json", ".yaml", ".yml"} and not generic:
                    try:
                        structured = json.loads(content) if filename.suffix == ".json" else yaml.safe_load(content)
                        if declared_private(structured):
                            rules.append("declared-private-record")
                    except (yaml.YAMLError, json.JSONDecodeError):
                        rules.append("unreadable-structured-data")
                if identifiers and any(identifier in content for identifier in identifiers) and not rules:
                    warnings.append({"path": name, "rule": "private-identifier-reference-review"})
                if private_text:
                    if overlaps_private(content, private_text):
                        rules.append("private-text-overlap")
                secret_patterns = [
                    rb"gh[pousr]_[A-Za-z0-9]{25,}", rb"github_pat_[A-Za-z0-9_]{40,}",
                    rb"\bAKIA[A-Z0-9]{16}\b", rb"\bsk-[A-Za-z0-9_-]{32,}\b",
                    b"-----BEGIN " + b"PRIVATE KEY-----", b"-----BEGIN " + b"RSA PRIVATE KEY-----",
                ]
                if any(re.search(pattern, data) for pattern in secret_patterns):
                    rules.append("credential-value-pattern")
        if rules:
            forbidden.append({"path": name, "rules": sorted(set(rules))})
    report = {
        "mode": "worktree" if args.worktree else "index",
        "checked_files": count, "checked_bytes": size,
        "private_seed_files": private_count,
        "forbidden": forbidden, "review_warnings": warnings,
        "largest_files": [{"path": name, "bytes": length} for length, name in sorted(largest, reverse=True)[:15]],
        "limitations": ["Known private metadata, paths, exact copies, prose overlap, and common credential formats are checked.",
                        "New unlabelled private manuscripts, transformed images, and arbitrary secret formats still require review."],
    }
    if args.report:
        path = args.report if args.report.is_absolute() else ROOT / args.report
        if not contained(path):
            raise RuntimeError("Report must stay inside this project")
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(f"Checked {count} {report['mode']} files ({size / (1024 * 1024):.2f} MiB); {len(forbidden)} forbidden paths; {len(warnings)} references for review.")
    for finding in forbidden:
        print(f"BLOCK {finding['path']}: {', '.join(finding['rules'])}")
    for finding in warnings:
        print(f"REVIEW {finding['path']}: {finding['rule']}")
    return 1 if forbidden else 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, RuntimeError, yaml.YAMLError) as error:
        print("Publication audit failed: " + str(error), file=sys.stderr)
        sys.exit(2)
