#!/usr/bin/env python3
"""Build independent, public-only paper and result pages from reviewed v2 data.

Only this script's output directory is served. No archive-store traversal, corpus
export, experimental proof, browser environment, or unpublished paper is copied.
"""
from __future__ import annotations

import copy
import hashlib
import html
import importlib.util
import json
import re
import shutil
import subprocess
import tempfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
WORK = Path(__file__).resolve().parent
SITE = WORK / "preview"
EVIDENCE = WORK / "evidence"
PAPER_IDS = {"cvpr2023-sparse-concepts", "iclr2024-sparse", "iclr2024-generalizable"}
INPUTS: dict[str, dict] = {}
PUBLIC_FILES: dict[str, dict] = {}
LEAN_WHITELIST = {"propext", "Classical.choice", "Quot.sound"}
VERIFICATION_CHECKS: list[dict] = []


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def record(path: Path) -> None:
    INPUTS[path.relative_to(ROOT).as_posix()] = {"path": path.relative_to(ROOT).as_posix(), "sha256": digest(path)}


def project_file(path: str | Path) -> Path:
    result = (ROOT / path).resolve()
    if not result.is_relative_to(ROOT) or not result.is_file():
        raise ValueError(f"Expected an existing project file: {path}")
    if Path(path).is_absolute() or (ROOT / path).is_symlink():
        raise ValueError(f"Only ordinary project-relative files are supported: {path}")
    return result


def read_json(path: Path) -> dict:
    record(path)
    return json.loads(path.read_text(encoding="utf-8"))


def publish(source: Path, target: str, *, expected: str | None = None) -> str:
    if source.is_symlink() or not source.is_relative_to(ROOT):
        raise ValueError("Source must be an ordinary file inside this project")
    value = digest(source)
    if expected and value != expected:
        raise ValueError(f"Pinned source hash changed: {source.relative_to(ROOT)}")
    destination = SITE / target
    if not destination.resolve().is_relative_to(SITE):
        raise ValueError("Output escaped the preview directory")
    previous = PUBLIC_FILES.get(target)
    if previous and previous["sha256"] != value:
        raise ValueError(f"Different public sources would overwrite {target}")
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, destination)
    record(source)
    PUBLIC_FILES[target] = {"path": target, "source": source.relative_to(ROOT).as_posix(), "sha256": value}
    return "/" + target


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def verify_lean(lean: dict) -> dict:
    """Reuse the package's source/declaration/axiom checks, never a UI flag."""
    report_path = lean.get("report_path")
    names = [item if isinstance(item, str) else item.get("name", item.get("declaration")) for item in lean.get("declarations", [])]
    result = {"status": "unavailable", "declarations": names, "reasons": []}
    if not isinstance(report_path, str) or not report_path:
        result["reasons"].append("verification report is missing")
        return result
    try:
        report_file = project_file(report_path)
        report = read_json(report_file)
    except (ValueError, OSError, json.JSONDecodeError) as error:
        result["reasons"].append(str(error))
        return result
    helper_path = WORK / "architecture/paper_agent.py"
    record(helper_path)
    spec = importlib.util.spec_from_file_location("reader_v2_package_verifier", helper_path)
    helper = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(helper)
    node = {"id": "reader-verification", "path": report_path, "scope": lean.get("scope", "selected declaration"),
            "expected_declarations": names, "visibility": "public"}
    package = helper.PaperPackage(root=ROOT, manifest={"verification_reports": [node]}, math_content={"results": [], "shared_proofs": []})
    package_evidence = package.report_evidence(node["id"])
    result["package_evidence"] = package_evidence
    if package_evidence["freshness"] == "stale":
        result["status"] = "stale"
    elif package_evidence["compilation"] == "passed" and package_evidence["axiom_audit"] == "passed" and package_evidence["freshness"] == "current":
        result["status"] = "verified"
    else:
        result["reasons"].append(package_evidence.get("reason", "compilation or axiom audit did not pass"))
    commands = report.get("commands", [])
    if not any("lean" in command.get("argv", []) and any("Audit" in str(arg) for arg in command.get("argv", [])) and command.get("exit_code") == 0 for command in commands):
        result["reasons"].append("no successful declaration/axiom audit command")
    source_rows = report.get("source_files", [])
    for row in source_rows:
        try:
            record(project_file(row["path"]))
        except (ValueError, KeyError, OSError):
            pass  # The shared helper records missing or modified sources as stale.
    declared = {item["name"]: item for item in report.get("declarations", [])}
    for name in names:
        if name in declared and declared[name].get("source_path") not in {row.get("path") for row in source_rows}:
            result["reasons"].append(f"declaration source was not fingerprinted: {name}")
    if result["reasons"] and result["status"] == "verified":
        result["status"] = "unavailable"
    result["source_fingerprint"] = report.get("source_fingerprint")
    result["report_sha256"] = digest(report_file)
    return result


def public_lean(lean: dict) -> None:
    explicitly_unformalized = lean.get("status") == "not_formalized" and not lean.get("declarations") and not lean.get("report_path")
    verification = verify_lean(lean)
    VERIFICATION_CHECKS.append(verification)
    lean["status"] = "not_formalized" if explicitly_unformalized else verification["status"]
    lean["compiled"] = verification["status"] == "verified"
    lean["label"] = "尚未形式化" if explicitly_unformalized else {"verified": "Lean 对照已编译", "stale": "Lean 证据待更新", "unavailable": "Lean 证据未取得"}[verification["status"]]
    lean["verification"] = verification
    for key, label in (("source_path", "source"), ("report_path", "report")):
        path = lean.get(key)
        if not isinstance(path, str) or not path:
            continue
        # These paths are supplied by the mathematical reviewer. Experimental
        # OR work is deliberately outside the downloadable/readable snapshot.
        allowed = path.startswith("lean/HarsanyiLib/Harsanyi/") or path.startswith("research/reader-v2-20260930/math/")
        if not allowed or "/experimental/" in path:
            raise ValueError(f"Non-public Lean artifact requested: {path}")
        source = project_file(path)
        lean["public_" + key] = publish(source, "files/lean/" + digest(source)[:12] + "-" + source.name)
    # Kept in provenance outside the served data; reader code names are useful,
    # machine paths and build directories are not part of the reading flow.
    lean.pop("source_path", None)
    lean.pop("report_path", None)


def proof_body_present(proof: dict) -> bool:
    steps = proof.get("proof_steps", [])
    return bool(steps) and all(isinstance(step, dict) and bool(str(step.get("body_md", "")).strip() or step.get("formula_tex")) for step in steps)


def status_complete(result: dict, shared_by_id: dict[str, dict]) -> bool:
    # Reading completeness is separate from original-statement alignment. Only
    # an explicit positive rewrite status and actual proof text can establish it.
    if result.get("rewrite_status") != "complete" or not (result.get("statement_tex") or result.get("statement_md")):
        return False
    shared_id = result.get("shared_proof_id")
    if shared_id:
        shared = shared_by_id.get(shared_id, {})
        return shared.get("rewrite_status") == "complete" and proof_body_present(shared) and proof_body_present(result)
    return proof_body_present(result)


def check_status_contract() -> list[dict]:
    proof = {"id": "reviewed-proof", "rewrite_status": "complete", "proof_steps": [{"body_md": "A complete public derivation."}]}
    shared = {proof["id"]: proof}
    cases = [
        ("not_started with a candidate proof id is pending", {"rewrite_status": "not_started", "shared_proof_id": proof["id"], "statement_tex": "x=x", "proof_steps": [{"body_md": "candidate adaptation"}]}, False),
        ("unknown rewrite status with proof id is pending", {"rewrite_status": "unknown", "shared_proof_id": proof["id"], "statement_tex": "x=x", "proof_steps": [{"body_md": "candidate adaptation"}]}, False),
        ("complete metadata without actual body is pending", {"rewrite_status": "complete", "statement_tex": "x=x", "shared_proof_id": proof["id"]}, False),
        ("complete component with real shared body is complete", {"rewrite_status": "complete", "shared_proof_id": proof["id"], "statement_tex": "x=x", "proof_steps": [{"body_md": "explicit component adaptation"}]}, True),
    ]
    records = []
    for name, candidate, expected in cases:
        actual = status_complete(candidate, shared)
        if actual != expected:
            raise AssertionError(name)
        records.append({"name": name, "passed": True, "reading_status": "complete" if actual else "pending"})
    return records


def check_lean_contract(math_data: dict) -> list[dict]:
    reviewed = next((result["lean"] for result in math_data.get("results", []) if result.get("lean", {}).get("report_path") and result["lean"].get("declarations")), None)
    if not reviewed:
        raise ValueError("No public Lean verification evidence was supplied")
    report = json.loads(project_file(reviewed["report_path"]).read_text(encoding="utf-8"))
    checks = []
    current = verify_lean(reviewed)
    if current["status"] != "verified":
        # A later source edit must downgrade the evidence, not prevent a reading
        # snapshot from being built. Negative fixtures need a current baseline.
        return [{"name": "non-current evidence is not advertised as compiled", "passed": current["status"] in {"stale", "unavailable"}, "effective_status": current["status"]}]
    checks.append({"name": "current compiled declaration and approved axioms are verified", "passed": True})
    with tempfile.TemporaryDirectory(prefix="lean-status-fixtures-", dir=EVIDENCE) as fixture_dir:
        fixture = Path(fixture_dir) / "report.json"
        variants = []
        stale = copy.deepcopy(report)
        stale["source_files"][0]["sha256"] = "0" * 64
        variants.append(("stale source cannot inherit compiled metadata", stale, reviewed["declarations"], "stale"))
        failed = copy.deepcopy(report)
        failed["commands"][0]["exit_code"] = 1
        variants.append(("failed command cannot inherit compiled metadata", failed, reviewed["declarations"], "unavailable"))
        bad_axiom = copy.deepcopy(report)
        selected = {item if isinstance(item, str) else item.get("name") for item in reviewed["declarations"]}
        for declaration in bad_axiom["declarations"]:
            if declaration["name"] in selected:
                declaration["axioms"].append("sorryAx")
        variants.append(("unapproved axiom cannot inherit compiled metadata", bad_axiom, reviewed["declarations"], "unavailable"))
        variants.append(("missing exact declaration cannot inherit compiled metadata", report, ["ReaderV2.missing_declaration"], "unavailable"))
        for name, altered, names, expected in variants:
            fixture.write_text(json.dumps(altered, ensure_ascii=False), encoding="utf-8")
            candidate = {**reviewed, "status": "verified", "compiled": True, "report_path": fixture.relative_to(ROOT).as_posix(), "declarations": names}
            actual = verify_lean(candidate)["status"]
            if actual != expected:
                raise AssertionError(name)
            checks.append({"name": name, "passed": True, "effective_status": actual})
        INPUTS.pop(fixture.relative_to(ROOT).as_posix(), None)
    return checks


def build() -> dict:
    SITE.mkdir(parents=True, exist_ok=True)
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    paper_data = read_json(WORK / "data/papers.json")
    math_data = read_json(WORK / "data/math-content.json")
    papers = copy.deepcopy(paper_data["papers"])
    math_content = {key: copy.deepcopy(math_data[key]) for key in ("schema_version", "language", "notation", "shared_proofs", "results") if key in math_data}
    contract_checks = check_status_contract() + check_lean_contract(math_data)
    shared_value = math_content.get("shared_proofs", [])
    shared_by_id = {proof["id"]: proof for proof in shared_value} if isinstance(shared_value, list) else shared_value
    if len(papers) != 3 or {p["id"] for p in papers} != PAPER_IDS:
        raise ValueError("This snapshot must contain the three agreed formal papers")
    page_requests: dict[str, set[int]] = {}
    for result in math_content.get("results", []):
        for ref in result.get("source_refs", []):
            if isinstance(ref, str):
                continue
            source_id = ref.get("source_id", ref.get("id"))
            for location in ref.get("locations", []):
                page = location.get("pdf_page") if isinstance(location, dict) else None
                if isinstance(page, int):
                    page_requests.setdefault(source_id, set()).add(page)
    source_page_records = []
    page_cache_path = EVIDENCE / "source-pages-manifest.json"
    page_cache = json.loads(page_cache_path.read_text(encoding="utf-8")).get("pages", []) if page_cache_path.exists() else []
    for paper in papers:
        if paper.get("visibility") != "public" or paper.get("publication_status") != "published":
            raise ValueError(f"Non-public or non-formal paper: {paper['id']}")
        for source in paper["sources"]:
            if source.get("visibility") != "public" or source.get("publication_status") != "published":
                raise ValueError(f"Non-public or non-formal source: {source['id']}")
            source_file = project_file(source["local_path"])
            source["public_path"] = publish(source_file, "files/papers/" + source["id"] + ".pdf", expected=source["sha256"])
            source["page_images"] = {}
            for page_number in sorted(page_requests.get(source["id"], set())):
                if not 1 <= page_number <= source["total_pages"]:
                    raise ValueError(f"PDF page outside formal source: {source['id']}:{page_number}")
                cache_image = EVIDENCE / "source-pages" / f"{source['id']}-p{page_number:02}.png"
                valid = cache_image.exists() and any(item["source_id"] == source["id"] and item["pdf_page"] == page_number and item["pdf_sha256"] == source["sha256"] and item["image_sha256"] == digest(cache_image) for item in page_cache)
                if not valid:
                    cache_image.parent.mkdir(parents=True, exist_ok=True)
                    subprocess.run(["pdftoppm", "-f", str(page_number), "-l", str(page_number), "-r", "110", "-png", "-singlefile", str(source_file), str(cache_image.with_suffix(""))], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
                source["page_images"][str(page_number)] = publish(cache_image, "files/source-pages/" + cache_image.name)
                source_page_records.append({"source_id": source["id"], "pdf_page": page_number, "pdf_sha256": source["sha256"], "render_dpi": 110, "image_sha256": digest(cache_image)})
            source.pop("local_path", None)
        for key in ("candidate_id", "selection_status", "review_status", "user_approval_status", "version_label"):
            paper.pop(key, None)
    all_results = math_content.get("results", [])
    math_content["results"] = [r for r in all_results if r.get("publication_status") != "experimental_not_published" and r.get("status") != "experimental_not_published" and r.get("id") != "library-or-reconstruction"]
    source_ids = {s["id"] for p in papers for s in p["sources"]}
    transcript_by_paper: dict[str, list[dict]] = {}
    excerpt_metadata = WORK / "data/source-excerpts/metadata.json"
    if excerpt_metadata.exists():
        excerpts = read_json(excerpt_metadata)
        seen_transcripts = set()
        for excerpt in excerpts.get("excerpts", []):
            path = excerpt.get("transcription_path")
            if not path or path in seen_transcripts or excerpt.get("paper_id") not in PAPER_IDS:
                continue
            if excerpt.get("visibility") != "public" or excerpt.get("source_id") not in source_ids:
                raise ValueError("A formula transcript is outside the formal source whitelist")
            seen_transcripts.add(path)
            source = project_file(path)
            public_path = publish(source, "files/transcripts/" + source.name, expected=excerpt.get("transcription_sha256"))
            transcript_by_paper.setdefault(excerpt["paper_id"], []).append({"public_path": public_path, "raw_text": source.read_text(encoding="utf-8"), "label": "选定公式的 PDF 核对转录", "source_format": "agent_transcription_not_author_tex"})
    for result in math_content["results"]:
        if result.get("paper_id") not in PAPER_IDS | {None}:
            raise ValueError(f"Unexpected paper id: {result['id']}")
        for ref in result.get("source_refs", []):
            source_id = ref if isinstance(ref, str) else ref.get("source_id", ref.get("id"))
            if source_id not in source_ids:
                raise ValueError(f"Unknown formal source: {result['id']}: {source_id}")
        if result.get("rewrite_status") not in {"complete", "not_started", "in_progress"}:
            raise ValueError(f"Explicit rewrite_status is required: {result['id']}")
        result["reading_status"] = "complete" if status_complete(result, shared_by_id) else "pending"
        if result["rewrite_status"] == "complete" and result["reading_status"] != "complete":
            raise ValueError(f"Complete rewrite is missing actual proof text: {result['id']}")
        if result.get("lean"):
            public_lean(result["lean"])
    shared_proofs = math_content.get("shared_proofs", [])
    for proof in shared_proofs if isinstance(shared_proofs, list) else shared_proofs.values():
        if proof.get("lean"):
            public_lean(proof["lean"])
    for paper in papers:
        complete = [r for r in math_content["results"] if r.get("paper_id") == paper["id"] and r["reading_status"] == "complete"]
        if not complete:
            raise ValueError(f"No actual rewritten result for {paper['id']}")

    documentation = []
    for source_name, label, target in [
        ("docs/paper-agent-data-model.md", "数据关系与 Paper2Agent 参考", "files/paper-agent-data-model.md"),
        ("docs/agent-extension-workflow.md", "新增论文的处理流程", "files/agent-extension-workflow.md"),
        ("research/reader-v2-20260930/architecture/paper_agent.py", "只读命令行工具", "files/paper_agent.py"),
        ("research/reader-v2-20260930/architecture/agent-package.json", "可核验的数据包", "files/agent-package.json"),
    ]:
        source = ROOT / source_name
        if source.exists():
            documentation.append({"label": label, "public_path": publish(source, target)})
    issue_data = []
    issues_path = WORK / "math/issues.json"
    if issues_path.exists():
        issues = read_json(issues_path)
        issue_data = issues.get("issues", []) + issues.get("alignment_notes", []) if isinstance(issues, dict) else issues
        publish(issues_path, "files/source-issues.json")
        if (WORK / "math/issues.md").exists():
            publish(WORK / "math/issues.md", "files/source-issues.md")
        for issue in issue_data:
            issue["public_path"] = "/reviews/" + issue["id"] + "/"
        issue_map = {i["id"]: i for i in issue_data}
        for result in math_content["results"]:
            refs = result.get("issue_refs", result.get("issues", result.get("related_issue_ids", [])))
            if result["reading_status"] != "complete":
                refs = list(refs) + list(result.get("alignment_note_ids", []))
            mapped = []
            for ref in refs:
                issue_id = ref if isinstance(ref, str) else ref.get("id", ref.get("issue_id"))
                issue = copy.deepcopy(issue_map.get(issue_id, ref if isinstance(ref, dict) else {}))
                if issue:
                    issue["public_path"] = issue.get("public_path", "/files/source-issues.md")
                    mapped.append(issue)
            if mapped:
                result["issues"] = mapped

    data = {"schema_version": "2.0", "papers": papers, "math": math_content, "documentation": documentation,
            "formula_transcripts": transcript_by_paper,
            "issues": [{"label": i.get("title", i.get("id")), "public_path": i["public_path"]} for i in issue_data],
            "review_records": issue_data,
            "cli_example": "python research/reader-v2-20260930/architecture/paper_agent.py --help"}
    serialized = json.dumps(data, ensure_ascii=False, indent=2)
    if any(marker in serialized for marker in ("manual-maintext", "inbox/", "unpublished", "/experimental/")):
        raise ValueError("Private or experimental identifier reached the served reading data")
    write_json(SITE / "data.public.json", data)
    (SITE / "data.public.js").write_text("window.READER_V2_DATA = " + serialized.replace("</", "<\\/") + ";\n", encoding="utf-8")
    for filename in ("reader.js", "reader.css"):
        publish(WORK / "ui" / filename, filename)
    template = (WORK / "ui/index.html").read_text(encoding="utf-8")
    record(WORK / "ui/index.html")
    pages = []

    def page(relative: str, title: str, kind: str, **route: str) -> None:
        destination = SITE / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        attrs = " ".join(f'data-{key.replace("_", "-")}="{html.escape(value, quote=True)}"' for key, value in {"page_kind": kind, **route}.items())
        content = template.replace("<body>", "<body " + attrs + ">").replace("<title>论文与证明</title>", "<title>" + html.escape(title) + " · 论文与证明</title>")
        destination.write_text(content, encoding="utf-8")
        pages.append({"path": relative, "kind": kind, "title": title, **route})

    page("index.html", "论文", "home")
    page("about/index.html", "给 AI 与维护者", "about")
    for paper in papers:
        page(f"papers/{paper['id']}/index.html", paper["title"], "paper", paper_id=paper["id"])
    for result in math_content["results"]:
        paper_id = result.get("paper_id")
        path = f"papers/{paper_id}/results/{result['id']}/index.html" if paper_id else f"library/{result['id']}/index.html"
        page(path, result["title"], "result", result_id=result["id"], **({"paper_id": paper_id} if paper_id else {}))
    for issue in issue_data:
        page(f"reviews/{issue['id']}/index.html", issue["title"], "review", review_id=issue["id"])
    # Only the small, already-local KaTeX distribution is copied. Browser runtimes
    # and installed Python packages remain in the old tooling directory.
    vendor = ROOT / "web/static/vendor/katex"
    if not (vendor / "katex.min.js").exists():
        raise ValueError("Local KaTeX distribution is unavailable")
    for source in vendor.rglob("*"):
        if source.is_file() and source.suffix in {".js", ".css", ".woff2", ".woff", ".ttf", ".txt"}:
            publish(source, "vendor/katex/" + source.relative_to(vendor).as_posix())
    allowed = {p["path"] for p in pages} | set(PUBLIC_FILES) | {"data.public.js", "data.public.json"}
    stale = [p for p in SITE.rglob("*") if p.is_file() and p.relative_to(SITE).as_posix() not in allowed]
    for path in stale:
        path.unlink()  # Generated preview copies only; never any original source.
    generated = datetime.now(timezone.utc).isoformat()
    complete_count = sum(r["reading_status"] == "complete" and bool(r.get("paper_id")) for r in math_content["results"])
    record_value = {"generated_at": generated, "visibility": "public", "paper_count": len(papers), "result_page_count": len(math_content["results"]),
                    "rewritten_paper_result_count": complete_count, "pages": pages, "inputs": sorted(INPUTS.values(), key=lambda x: x["path"]),
                    "public_file_allowlist": sorted(PUBLIC_FILES.values(), key=lambda x: x["path"]), "private_or_experimental_exported": False}
    write_json(EVIDENCE / "build-manifest.json", record_value)
    write_json(page_cache_path, {"pages": source_page_records})
    write_json(EVIDENCE / "status-contract-checks.json", {"status": "passed", "checks": contract_checks, "lean_verification": VERIFICATION_CHECKS})
    baseline_path = EVIDENCE / "production-baseline.json"
    if not baseline_path.exists():
        watched = {}
        for directory in ("src/archive", "web", "corpus", "lean/HarsanyiLib/Harsanyi", "lean/PaperProofs/PaperProofs"):
            for path in sorted((ROOT / directory).rglob("*")):
                if path.is_file() and "__pycache__" not in path.parts:
                    watched[path.relative_to(ROOT).as_posix()] = digest(path)
        write_json(baseline_path, {"generated_at": generated, "files": watched})
    return {"status": "built", "papers": len(papers), "result_pages": len(math_content["results"]), "rewritten_paper_results": complete_count,
            "preview": str(SITE), "shared_proofs": len(shared_proofs)}


if __name__ == "__main__":
    print(json.dumps(build(), ensure_ascii=False))
