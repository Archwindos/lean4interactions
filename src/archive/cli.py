"""Offline-first command line entry point."""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

from .extract import extract_paper
from .ingest import ingest_inbox, ingest_local, ingest_url
from .store import ArchiveStore
from .util import ArchiveError, resolve_root, safe_path
from .validate import validate_archive


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(prog="archive", description="Local proof archive; files are the source of truth.")
    result.add_argument("--root", help="Archive root (default ARCHIVE_ROOT or project root)")
    commands = result.add_subparsers(dest="command", required=True)
    ingest = commands.add_parser("ingest", help="Import a local file/batch or explicitly requested public URL")
    ingest.add_argument("source", nargs="?", help="Local project path")
    ingest.add_argument("--url", help="Public HTTP(S) source; no private files are uploaded")
    ingest.add_argument("--paper-id")
    ingest.add_argument("--version")
    ingest.add_argument("--title")
    commands.add_parser("inbox", help="Import all immediate inbox batch folders")
    extract = commands.add_parser("extract", help="Detect local candidates; completeness remains pending")
    extract.add_argument("paper_id")
    extract.add_argument("--version")
    metadata = commands.add_parser("update-metadata", help="Revise descriptive metadata with a local history record")
    metadata.add_argument("paper_id")
    metadata.add_argument("--version")
    metadata.add_argument("--title")
    metadata.add_argument("--author", action="append", dest="authors")
    metadata.add_argument("--publication-status")
    metadata.add_argument("--visibility", choices=("private", "public"))
    metadata.add_argument("--doi")
    metadata.add_argument("--arxiv-id")
    commands.add_parser("validate", help="Validate source hashes, paths and relationships")
    build = commands.add_parser("build", help="Rebuild SQLite search index")
    build.add_argument("--public", action="store_true")
    coverage = commands.add_parser("coverage", help="Report reviewed denominator and independent statuses")
    coverage.add_argument("--public", action="store_true")
    for name in ("search", "search-lemmas"):
        search = commands.add_parser(name)
        search.add_argument("query", nargs="?")
        search.add_argument("--query", dest="query_option")
        search.add_argument("--limit", type=int, default=50)
        search.add_argument("--format", choices=("json", "text"), default="json")
        search.add_argument("--public", action="store_true")
        if name == "search":
            search.add_argument("--kind")
    show = commands.add_parser("show-lemma")
    show.add_argument("id")
    show.add_argument("--format", choices=("json", "text"), default="json")
    show.add_argument("--public", action="store_true")
    impact = commands.add_parser("impact")
    impact.add_argument("id")
    impact.add_argument("--public", action="store_true")
    issues = commands.add_parser("issues", help="List recorded proof problems awaiting separate confirmation")
    issues.add_argument("--public", action="store_true")
    verify = commands.add_parser("verify", help="Run actual Lean build/audit script or inspect existing report")
    verify.add_argument("--report-only", action="store_true")
    serve = commands.add_parser("serve", help="Serve the local archive")
    serve.add_argument("--host", default="127.0.0.1")
    serve.add_argument("--port", type=int, default=8000)
    serve.add_argument("--public", action="store_true")
    export = commands.add_parser("export", help="Export a portable local website")
    export.add_argument("--output", default="build/site")
    export.add_argument("--public", action="store_true")
    return result


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    root = resolve_root(args.root)
    store = ArchiveStore(root, public=getattr(args, "public", False))
    try:
        if args.command == "ingest":
            if bool(args.url) == bool(args.source):
                raise ArchiveError("Supply exactly one local source or --url")
            if args.url:
                output = ingest_url(root, args.url, paper_id=args.paper_id, version=args.version, title=args.title)
            else:
                output = ingest_local(root, args.source, metadata={"title": args.title} if args.title else None, paper_id=args.paper_id, version=args.version)
        elif args.command == "inbox":
            output = ingest_inbox(root)
        elif args.command == "extract":
            output = extract_paper(root, args.paper_id, args.version)
        elif args.command == "update-metadata":
            from .ingest import update_metadata
            fields = {name: getattr(args, name) for name in ("title", "authors", "publication_status", "visibility", "doi", "arxiv_id") if getattr(args, name) is not None}
            output = update_metadata(root, args.paper_id, args.version, fields)
        elif args.command == "validate":
            output = validate_archive(root)
        elif args.command == "build":
            output = store.build_index()
        elif args.command == "coverage":
            output = store.coverage()
        elif args.command in {"search", "search-lemmas"}:
            query = args.query_option or args.query
            if not query:
                raise ArchiveError("Supply query text or --query")
            output = store.search(query, args.kind, args.limit) if args.command == "search" else store.search_lemmas(query, args.limit)
        elif args.command == "show-lemma":
            output = store.show_lemma(args.id)
            if output is None:
                raise ArchiveError(f"No matching library declaration: {args.id}")
        elif args.command == "impact":
            output = store.impact(args.id)
        elif args.command == "issues":
            output = store.list_issues()
        elif args.command == "verify":
            if args.report_only:
                output = store.latest_verification()
            else:
                script = safe_path(root, "scripts/verify-lean.sh")
                if not script.exists():
                    output = {"status": "unavailable", "reason": "Actual scripts/verify-lean.sh is not available."}
                else:
                    completed = subprocess.run(["bash", str(script)], cwd=root, check=False)
                    output = store.latest_verification()
                    output["verification_command_exit_code"] = completed.returncode
        elif args.command == "serve":
            import uvicorn
            from .web import create_app
            uvicorn.run(create_app(root=root, public=args.public), host=args.host, port=args.port)
            return 0
        elif args.command == "export":
            from .export import export_site
            output = export_site(root=root, output=safe_path(root, args.output), public=args.public)
        else:
            raise ArchiveError("Unknown command")
        if getattr(args, "format", "json") == "text":
            if isinstance(output, list):
                for item in output:
                    print(f"{item.get('kind', 'declaration')} {item.get('id', item.get('name', ''))}: {item.get('title', '')}")
            else:
                print(output)
        else:
            print(json.dumps(output, ensure_ascii=False, indent=2))
        if args.command == "validate" and output["status"] != "passed":
            return 1
        if args.command == "verify" and (output.get("effective_status", output.get("status")) != "passed" or output.get("verification_command_exit_code", 0) != 0):
            return 1
        return 0
    except (ArchiveError, OSError, ValueError) as exc:
        print(json.dumps({"status": "error", "error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
