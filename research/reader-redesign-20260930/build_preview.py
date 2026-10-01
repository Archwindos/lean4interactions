#!/usr/bin/env python3
"""Build a public-only reading prototype; never mutate the archive corpus."""
from __future__ import annotations

import hashlib
import json
import re
import shutil
from datetime import datetime, timezone
from pathlib import Path

import yaml
from pypdf import PdfReader

from archive.store import ArchiveStore

ROOT = Path(__file__).resolve().parents[2]
WORK = ROOT / "research/reader-redesign-20260930"
SITE = WORK / "preview"
EVIDENCE = WORK / "evidence"
PAPER_BASE = "corpus/papers/sparse-concepts-2111-06206/v6"
COMPLAINT = "claim-114147f1447e7138f450971e"
FORMAL_MAIN = "research/paper-survey-20260930/earlier/venue-papers/sparse-cvpr2023-main/sparse-cvpr2023-main.pdf"
FORMAL_SUPP = "research/paper-survey-20260930/earlier/venue-papers/sparse-cvpr2023-supp/sparse-cvpr2023-supp.pdf"
SOURCE_FILES: dict[str, dict] = {}


def read(path: str) -> str:
    value = (ROOT / path).read_text(encoding="utf-8")
    SOURCE_FILES[path] = {"path": path, "sha256": hashlib.sha256((ROOT / path).read_bytes()).hexdigest()}
    return value


def load(path: str) -> dict:
    value = yaml.safe_load(read(path))
    if not isinstance(value, dict):
        raise ValueError(f"Expected mapping: {path}")
    return value


def lines(path: str, first: int, last: int) -> dict:
    raw = "".join(read(path).splitlines(keepends=True)[first - 1:last])
    return {"path": path, "first": first, "last": last, "raw": raw,
            "label": f"{Path(path).name}:{first}–{last}"}


def copy_file(source: str, target: str) -> None:
    if (ROOT / source).is_symlink():
        raise ValueError("Source symlinks are not accepted")
    (SITE / target).parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(ROOT / source, SITE / target)
    SOURCE_FILES[source] = {"path": source, "sha256": hashlib.sha256((ROOT / source).read_bytes()).hexdigest()}


def write_json(path: Path, value: dict) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    SITE.mkdir(parents=True, exist_ok=True)
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    store = ArchiveStore(root=ROOT, public=True)
    manifest = load(f"{PAPER_BASE}/manifest.yaml")
    assert manifest["visibility"] == "public"
    inventory = load(f"{PAPER_BASE}/inventory.yaml")
    source_review = load(f"{PAPER_BASE}/source-review.yaml")
    selected_ids = ["claim-e15edb3df777058b68a8489c", "claim-574bfc8510d17c3209fd1d10",
                    "claim-9cd974272d015aded7b577c6", "claim-a31904cefdbc9e0a9374c802", COMPLAINT]
    claims = {}
    for cid in selected_ids:
        base = f"corpus/claims/{cid}"
        meta = load(f"{base}/metadata.yaml")
        assert meta["visibility"] == "public" and store.is_public("claim", cid)
        claims[cid] = {"metadata": meta, "original": read(f"{base}/original.tex"),
                       "alignment": load(f"{base}/alignment.yaml"), "review": load(f"{base}/review.yaml")}
        if (ROOT / base / "adaptation.zh.md").exists():
            claims[cid]["adaptation"] = read(f"{base}/adaptation.zh.md")

    main_tex = f"{PAPER_BASE}/sources/tex/AOG.tex"
    app_tex = f"{PAPER_BASE}/sources/tex/appendix.tex"
    original = {
        "reconstruction_statement": lines(main_tex, 205, 215),
        "appendix_statement": lines(app_tex, 116, 129),
        "theorem1_proof": lines(app_tex, 131, 186),
        "shapley_statement": lines(main_tex, 261, 265),
        # This is an unreviewed source context, not an asserted complete proof.
        "shapley_proof_context": lines(app_tex, 355, 430),
        "complaint_context": lines(main_tex, 320, 342),
    }
    assert "\\begin{theorem}" in original["reconstruction_statement"]["raw"]
    assert "\\begin{theorem}" not in original["complaint_context"]["raw"]
    assert "Theorem \\ref{th:harsanyi-faithful} by removing" in original["complaint_context"]["raw"]
    assert "\\begin{theorem}" in original["shapley_statement"]["raw"]

    catalog = store.load_catalog()
    validation = store.latest_verification()
    catalog_by_name = {x["name"]: x for x in catalog["declarations"]}
    proofs = {}
    for tid, pid, name in [
        ("harsanyi-reconstruction", "proof-reconstruction-v1", "Harsanyi.reconstruction"),
        ("harsanyi-reconstruction-unique", "proof-reconstruction-unique-v1", "Harsanyi.reconstruction_unique"),
    ]:
        base = f"corpus/theorems/{tid}"
        theorem = load(f"{base}/metadata.yaml")
        proof = load(f"{base}/proofs/{pid}/metadata.yaml")
        assert theorem["visibility"] == proof["visibility"] == "public"
        assert store.is_public("proof", pid)
        declaration = catalog_by_name[name]
        first = declaration["line"]
        last = 48 if name == "Harsanyi.reconstruction" else 72
        proofs[pid] = {
            "theorem": theorem, "metadata": proof, "statement": read(f"{base}/statement.tex"),
            "body": read(f"{base}/proofs/{pid}/proof.zh.md"),
            "declaration": {key: declaration.get(key) for key in
                            ("name", "signature", "module", "source_path", "line", "axioms", "verification_status")},
            "source": lines(declaration["source_path"], first, last),
        }
        copy_file(f"{base}/proofs/{pid}/proof.zh.md", f"files/{pid}.md")

    issue = load("corpus/issues/issue-sparse-concepts-v6-dummy-scope.yaml")
    assert issue["visibility"] == "public"
    public_relations = [x for x in store.relations() if x.get("from_id") in selected_ids]
    dependency_proofs = []
    for tid in ["harsanyi-interaction-insert", "harsanyi-interaction-empty", "harsanyi-reconstruct-empty"]:
        base = f"corpus/theorems/{tid}"
        theorem = load(f"{base}/metadata.yaml")
        assert theorem["visibility"] == "public"
        pid = theorem["proofs"][0]
        assert store.is_public("proof", pid)
        dependency_proofs.append({"title": theorem["title"], "body": read(f"{base}/proofs/{pid}/proof.zh.md")})
    raw_report = json.loads(read(validation["report_path"]))
    relevant_names = {"Harsanyi.reconstruction", "Harsanyi.reconstruction_unique"}
    verification_excerpt = {
        "notice": "Public declaration excerpt; existing evidence rechecked against current source, no new Lean build was run for this prototype.",
        "report_path": validation["report_path"], "status": validation["status"],
        "effective_status": validation["effective_status"], "generated_at": raw_report["generated_at"],
        "source_fingerprint": validation["source_fingerprint"], "toolchain": validation["toolchain"],
        "mathlib_revision": validation["mathlib_revision"],
        "declarations": [x for x in raw_report["declarations"] if x["name"] in relevant_names],
        "commands": [x for x in raw_report["commands"] if x["cwd"] == "lean/HarsanyiLib"],
    }
    write_json(SITE / "files/core-verification-excerpt.json", verification_excerpt)

    copy_file(FORMAL_MAIN, "files/cvpr2023-main.pdf")
    copy_file(FORMAL_SUPP, "files/cvpr2023-supplement.pdf")
    # arXiv files are auxiliary TeX, never presented as CVPR author source.
    copy_file(main_tex, "files/arxiv-v6-main.tex")
    copy_file(app_tex, "files/arxiv-v6-appendix.tex")
    for obsolete in ["public-v6.pdf", "paper-main.tex", "paper-appendix.tex"]:
        path = SITE / "files" / obsolete
        if path.exists():
            path.unlink()  # Only obsolete prototype copies, never originals.
    copy_file("lean/HarsanyiLib/Harsanyi/Core/Mobius.lean", "files/Mobius.lean")
    main_pdf = PdfReader(ROOT / FORMAL_MAIN)
    supp_pdf = PdfReader(ROOT / FORMAL_SUPP)
    assert len(main_pdf.pages) == 10 and len(supp_pdf.pages) == 27
    formal_main_statement = main_pdf.pages[2].extract_text()
    formal_supp_statement = supp_pdf.pages[1].extract_text()
    formal_supp_proof = supp_pdf.pages[2].extract_text()
    assert "Theorem 1" in formal_main_statement and "unique metric" in formal_supp_statement
    assert "Proof for necessity" in formal_supp_proof and "Proof for sufficiency" in formal_supp_proof
    assert "(Basis step)" in formal_supp_proof and "(Induction step)" in formal_supp_proof
    source_index = json.loads(read("research/paper-survey-20260930/earlier/venue-source-index.json"))
    formal_records = [x for x in source_index if x.get("key") in {"sparse-cvpr2023", "sparse-cvpr2023-main", "sparse-cvpr2023-supp"}]
    formal_sources = []
    for record in formal_records:
        local = ROOT / record["local_file"]
        assert hashlib.sha256(local.read_bytes()).hexdigest() == record["sha256"]
        formal_sources.append({key: record.get(key) for key in ("key", "url", "resolved_url", "retrieved_at", "local_file", "sha256", "total_pages", "status")})
    reference_page = main_pdf.pages[3].extract_text()
    reference_start = reference_page.find("The following para")
    reference_end_match = re.search(r"First,\s*boosting", reference_page[reference_start:])
    assert reference_start >= 0 and reference_end_match
    formal_reference_text = reference_page[reference_start:reference_start + reference_end_match.start()].strip()
    formal_audit = {
        "edition": "CVPR2023 official CVF open-access main paper and supplement",
        "main_pages": len(main_pdf.pages), "supplement_pages": len(supp_pdf.pages), "sources": formal_sources,
        "full_formal_inventory_reviewed": False, "corpus_edition_migrated": False,
        "scope": ["Main PDF page 3 Theorem 1 and fixed-masking/SCM definitions on pages 3–4",
                  "Supplement PDF page 2 Theorem 1 statement, page 3 complete reconstruction and uniqueness proof",
                  "Main PDF page 4 Theorem 2 statement and prose reference to Theorem 1; proof location only, supplement page 6 onwards"],
        "aligned_mathematical_components": [
            {"result": "harsanyi-reconstruction", "evidence": "Fixed input/DNN/baseline; real-valued g(S)=v(x_S); full power set including empty; SCM triggered iff T subset S; all-mask exact reconstruction.", "source_pages": ["main:3", "main:4", "supplement:2", "supplement:3"]},
            {"result": "harsanyi-reconstruction-unique", "evidence": "Alternative coefficients reconstruct every coalition exactly; supplement's empty-set base case retains w_empty=v(x_empty); no zero-baseline assumption added.", "source_pages": ["supplement:2", "supplement:3"]},
        ],
        "auxiliary_tex": {"edition": "arXiv:2111.06206v6", "is_official_cvpr_tex": False,
                          "scoped_visual_and_text_comparison": "Theorem 1 main statement and both supplement proof components match in mathematical hypotheses/formulas/conclusion. Citation and equation numbers differ, full documents are not asserted identical.",
                          "differences": ["Main Harsanyi citation is [15] in CVPR and [29] in arXiv", "Main Shapley citation is [31] in CVPR and [56] in arXiv", "Supplement reconstruction equation is (2) in official PDF and (10) in arXiv", "Official main has 10 pages; arXiv main content and pagination differ"]},
        "visual_evidence": ["evidence/official-main-page-03.png", "evidence/official-supp-page-02.png", "evidence/official-supp-page-03.png"],
        "new_proofs_or_lean_builds": False,
    }
    write_json(EVIDENCE / "formal-edition-audit.json", formal_audit)
    write_json(SITE / "files/formal-edition-evidence.json", formal_audit)
    (SITE / "files/official-pages").mkdir(parents=True, exist_ok=True)
    for name in ["official-main-page-03.png", "official-main-page-04.png", "official-supp-page-02.png", "official-supp-page-03.png"]:
        shutil.copyfile(EVIDENCE / name, SITE / "files/official-pages" / name)
    vendor = ROOT / "web/static/vendor/katex"
    (SITE / "vendor/katex/contrib").mkdir(parents=True, exist_ok=True)
    for name in ["katex.min.js", "katex.min.css", "LICENSE", "contrib/auto-render.min.js"]:
        shutil.copyfile(vendor / name, SITE / "vendor/katex" / name)
    shutil.copytree(vendor / "fonts", SITE / "vendor/katex/fonts", dirs_exist_ok=True)

    data = {
        "snapshot_at": datetime.now(timezone.utc).isoformat(), "prototype_only": True,
        "paper": {"paper_id": "sparse-concepts-cvpr2023", "version": "CVPR2023",
                  "title": manifest["title"], "authors": manifest["authors"], "visibility": "public",
                  "edition": "CVPR 2023 正式会议版 · CVF公开版本", "main_pages": 10, "supplement_pages": 27},
        "inventory": {"source_record_count": None, "reviewed_source_record_count": None,
                      "reviewed_unique_mathematical_results": 2, "denominator_reviewed": False,
                      "completeness_status": "formal_full_inventory_not_reviewed", "items": []},
        "formal_edition_audit": formal_audit, "formal_reference_text": formal_reference_text,
        "original": original, "proofs": proofs, "dependency_proofs": dependency_proofs,
        "verification": verification_excerpt,
    }
    write_json(SITE / "data.public.json", data)
    (SITE / "data.public.js").write_text("window.READER_DATA = " + json.dumps(data, ensure_ascii=False) + ";\n", encoding="utf-8")
    write_json(EVIDENCE / "input-provenance.json", {
        "generated_at": data["snapshot_at"], "visibility": "public",
        "sources": sorted(SOURCE_FILES.values(), key=lambda x: x["path"]),
        "original_claims_and_proofs_mutated": False,
    })
    write_json(EVIDENCE / "legacy-arxiv-records.json", {
        "edition": "arXiv:2111.06206v6 historical audit, not formal CVPR inventory",
        "inventory": inventory, "claims": claims, "source_review": source_review,
        "relations": public_relations, "issue": issue,
    })
    claim = claims[COMPLAINT]
    write_json(EVIDENCE / "display-audit.json", {
        "generated_at": data["snapshot_at"], "complaint_url_path": f"/claims/{COMPLAINT}",
        "classification": "prose_reference_false_positive_in_display_audit_only",
        "canonical_corpus_disposition": next(x["disposition"] for x in inventory["items"] if x["claim_id"] == COMPLAINT),
        "corpus_not_changed": True, "claim": claim,
        "source_context": original["complaint_context"],
        "pdf_evidence": "evidence/public-pdf-page-04.png",
        "reading": "PDF page 4, right column: a prose sentence referring to Theorem 1; no new theorem declaration.",
        "source_format": "original.tex is PDF-extracted plain text, not original TeX",
        "empty_modules": {"theorem_ids": claim["metadata"]["theorem_ids"],
                          "proof_ids": claim["metadata"]["proof_ids"],
                          "alignment_evidence": claim["alignment"]["evidence"],
                          "adaptation_file_exists": (ROOT / f"corpus/claims/{COMPLAINT}/adaptation.zh.md").exists()},
        "status_contract_bug": {"producer": "rewriting_status", "consumer": "rewrite_status",
                                "path": "web/templates/macros.html", "normalization_found": False},
        "alert_routing_bug": {"path": "web/templates/macros.html", "macro": "issues",
                              "prose_extraction_issue_labeled_as": "数学问题待确认"},
        "tex_renderer_limitation": "archive-math.js passes a mixed prose+TeX block to katex.render; document environments are unsupported and PDF plain text has no TeX delimiters.",
        "notation_warning": "Do not repair exponents, subscripts or formula boundaries from PDF text without checking source/PDF.",
    })
    watched = {}
    for directory in ["src/archive", "web", "corpus", "lean/HarsanyiLib/Harsanyi", "lean/PaperProofs/PaperProofs"]:
        for path in sorted((ROOT / directory).rglob("*")):
            if path.is_file() and "__pycache__" not in path.parts:
                watched[path.relative_to(ROOT).as_posix()] = hashlib.sha256(path.read_bytes()).hexdigest()
    write_json(EVIDENCE / "production-baseline.json", {"generated_at": data["snapshot_at"], "files": watched})
    print(json.dumps({"preview": str(SITE), "legacy_arxiv_source_records": len(inventory["items"]), "formal_inventory_count": None,
                      "proofs": list(proofs), "effective_lean_status": validation["effective_status"],
                      "inputs": len(SOURCE_FILES)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
