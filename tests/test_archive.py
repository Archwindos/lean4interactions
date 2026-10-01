from pathlib import Path

import pytest

from archive.extract import extract_paper
from archive.ingest import ingest_inbox, ingest_local, update_metadata
from archive.store import ArchiveStore
from archive.util import ArchiveError, digest_data, load_data, sha256, write_data, write_text
from archive.validate import validate_archive


@pytest.fixture
def draft(tmp_path):
    folder = tmp_path / "inbox" / "draft"
    folder.mkdir(parents=True)
    (folder / "main.md").write_text("# 定理 1 唯一性 Uniqueness\n假设有限变量集合。\nProof. 中文证明过程。\n", encoding="utf-8")
    (folder / "image.bin").write_bytes(b"attachment")
    return tmp_path, folder


def test_private_manual_idempotent_and_versions(draft):
    root, folder = draft
    first = ingest_local(root, folder)
    assert first["visibility"] == "private"
    assert first["publication_status"] == "unpublished"
    assert first["source_url"] is None
    assert ingest_local(root, folder)["idempotent"] is True
    old = root / f"corpus/papers/{first['paper_id']}/{first['version']}/sources/main.md"
    (folder / "main.md").write_text("# Theorem 2\nA changed statement.", encoding="utf-8")
    changed = ingest_local(root, folder)
    assert changed["version"] != first["version"]
    assert old.read_text(encoding="utf-8").startswith("# 定理 1")
    assert changed["supersedes"] == first["version"]


def test_reject_path_symlink_and_project_import(draft):
    root, folder = draft
    with pytest.raises(ArchiveError):
        ingest_local(root, root)
    with pytest.raises(ArchiveError):
        ingest_local(root, "../outside.md")
    (folder / "linked.md").symlink_to(folder / "main.md")
    with pytest.raises(ArchiveError, match="Symlinks"):
        ingest_local(root, folder)


def test_metadata_revision_requires_explicit_history(draft):
    root, folder = draft
    first = ingest_local(root, folder)
    write_data(folder / "metadata.yaml", {"title": "正式题名"})
    with pytest.raises(ArchiveError, match="update-metadata"):
        ingest_local(root, folder)
    revised = update_metadata(root, first["paper_id"], None, {"title": "正式题名"})
    assert revised["title"] == "正式题名"
    assert revised["files"] == first["files"]
    assert list((root / f"corpus/papers/{first['paper_id']}/v1/metadata-history").glob("*.json"))
    assert ingest_local(root, folder)["idempotent"]


def test_extract_search_chinese_number_fulltext_and_rebuild(draft):
    root, folder = draft
    paper = ingest_local(root, folder)
    result = extract_paper(root, paper["paper_id"])
    assert result["candidate_count"] == 2
    assert result["completeness_status"] == "not_reviewed"
    store = ArchiveStore(root)
    assert any(item["kind"] == "claim" for item in store.search("定理 1"))
    assert any(item["kind"] == "source" for item in store.search("中文证明"))
    assert store.search("Uniqueness")
    assert not store.public_view().search("Uniqueness")
    assert store.coverage()["papers"][0]["coverage_ratio"] is None
    assert store.coverage()["papers"][0]["completed"] is False
    assert extract_paper(root, paper["paper_id"])["candidate_count"] == 2
    assert len(store.list_claims()) == 2
    (root / "build/archive.sqlite").unlink()
    assert store.search("Uniqueness")
    assert validate_archive(root)["status"] == "passed"


def _reviewed_extraction_fixture(root):
    """Synthetic review evidence, kept entirely in pytest's isolated archive."""
    folder = root / "inbox/reviewed"
    source = folder / "main.tex"
    write_text(source, r"""\begin{theorem}[Synthetic primary]
An identity statement with a proof.
\end{theorem}
\begin{theorem}[Synthetic duplicate]
The same statement appears again.
\end{theorem}
\begin{claim}[Synthetic false positive]
A detector match that manual review rejects.
\end{claim}
Manual-only fixture argument.
Previously undetected fixture argument.
""")
    paper = ingest_local(root, folder, paper_id="reviewed-fixture")
    extract_paper(root, paper["paper_id"], paper["version"])
    inventory_path = root / f"corpus/papers/{paper['paper_id']}/{paper['version']}/inventory.yaml"
    inventory = load_data(inventory_path)
    by_label = {item["original_label"]: item for item in inventory["items"]}
    primary = by_label["Synthetic primary"]
    duplicate = by_label["Synthetic duplicate"]
    false_positive = by_label["Synthetic false positive"]
    for item, disposition in ((primary, "retained"), (duplicate, "duplicate_occurrence"), (false_positive, "false_positive")):
        item.update(review_status="reviewed", disposition=disposition, review_evidence="Synthetic section-by-section audit")
        if item is duplicate:
            item["canonical_claim_id"] = primary["claim_id"]
        metadata_path = root / f"corpus/claims/{item['claim_id']}/metadata.yaml"
        metadata = load_data(metadata_path)
        metadata.update({key: item[key] for key in ("review_status", "disposition", "review_evidence", "canonical_claim_id") if key in item})
        write_data(metadata_path, metadata)
    claim_dir = root / f"corpus/claims/{primary['claim_id']}"
    write_text(claim_dir / "original.tex", "Synthetic statement transcript with manually checked boundaries.\n")
    write_text(claim_dir / "original-proof.tex", "Synthetic proof transcript; retain exactly on repeat extraction.\n")
    write_text(claim_dir / "adaptation.zh.md", "这是隔离测试的人工适配说明。\n")
    write_data(claim_dir / "alignment.yaml", {"schema_version": 1, "status": "aligned", "symbol_mapping": [{"original": "synthetic", "normalized": "synthetic"}], "evidence": ["Synthetic checked alignment"]})
    write_data(claim_dir / "review.yaml", {"schema_version": 1, "status": "reviewed", "proof_checked": True, "evidence": "Synthetic checked original proof"})
    adapter = claim_dir / "lean/Adapter.lean"
    write_text(adapter, "theorem Fixture.adapter (n : Nat) : n = n := rfl\n")
    log = claim_dir / "lean/build.log"
    write_text(log, "Synthetic test evidence; no Lean build was run for this fixture.\n")
    records = [{"path": adapter.relative_to(root).as_posix(), "sha256": sha256(adapter)}]
    report_path = claim_dir / "lean/report.json"
    write_data(report_path, {"schema_version": 1, "status": "passed", "visibility": "private",
                             "source_files": records, "source_fingerprint": digest_data(records),
                             "commands": [{"argv": ["synthetic-fixture-only"], "exit_code": 0, "log_path": log.relative_to(root).as_posix()}],
                             "declarations": [{"name": "Fixture.adapter", "status": "passed", "axioms": []}]})
    metadata_path = claim_dir / "metadata.yaml"
    metadata = load_data(metadata_path)
    metadata.update(alignment_status="aligned", rewriting_status="reviewed", lean_declarations=["Fixture.adapter"],
                    verification_report=report_path.relative_to(root).as_posix(), original_proof="Synthetic checked original proof")
    write_data(metadata_path, metadata)
    manual_item = {"claim_id": "manual-only-fixture", "original_label": "Manual-only fixture argument",
                   "kind": "proposition", "disposition": "retained", "review_status": "reviewed",
                   "source_location": {"file": "sources/main.tex", "section": "Synthetic body"},
                   "review_evidence": "This occurrence was added by human review, not the detector"}
    inventory["items"].append(manual_item)
    manual_dir = root / "corpus/claims/manual-only-fixture"
    write_data(manual_dir / "metadata.yaml", {"schema_version": 1, "paper_id": paper["paper_id"], "paper_version": paper["version"],
                                               "visibility": "private", "theorem_ids": [], "proof_ids": [], "alignment_status": "pending", **manual_item})
    write_text(manual_dir / "original.tex", "Manual-only fixture argument.\n")
    inventory.update(denominator_reviewed=True, completeness_status="reviewed",
                     completeness_review={"reviewer": "fixture reviewer", "sections": ["body", "appendix"], "evidence": "Synthetic complete inventory audit"})
    write_data(inventory_path, inventory)
    snapshots = {path.relative_to(root).as_posix(): path.read_bytes() for path in (root / "corpus/claims").rglob("*") if path.is_file()}
    return {"paper": paper, "source": source, "inventory_path": inventory_path,
            "inventory": inventory, "primary_id": primary["claim_id"], "claim_files": snapshots}


@pytest.mark.parametrize("detector_omits_rejected_match", [False, True])
def test_reextract_preserves_reviewed_inventory_and_claim_evidence(tmp_path, monkeypatch, detector_omits_rejected_match):
    import archive.extract as extraction
    fixture = _reviewed_extraction_fixture(tmp_path)
    detector = extraction._candidates
    if detector_omits_rejected_match:
        monkeypatch.setattr(extraction, "_candidates", lambda text, suffix: [candidate for candidate in detector(text, suffix) if candidate["label"] != "Synthetic false positive"])
    result = extract_paper(tmp_path, fixture["paper"]["paper_id"], fixture["paper"]["version"])
    current = load_data(fixture["inventory_path"])
    assert result["candidate_count"] == 4
    assert {item["claim_id"]: item for item in current["items"]} == {item["claim_id"]: item for item in fixture["inventory"]["items"]}
    assert current["denominator_reviewed"] is True and current["completeness_status"] == "reviewed"
    assert current["completeness_review"] == fixture["inventory"]["completeness_review"]
    for relative, content in fixture["claim_files"].items():
        assert (tmp_path / relative).read_bytes() == content, relative
    claim = ArchiveStore(tmp_path).get_claim(fixture["primary_id"])
    assert claim["alignment_status"] == "aligned" and claim["verification_status"] == "passed"
    assert claim["verification_scope"] == "independent_claim"
    assert ArchiveStore(tmp_path).coverage()["papers"][0]["proof_targets"] == 2


def test_parser_upgrade_new_candidate_invalidates_inventory_review(tmp_path, monkeypatch):
    import archive.extract as extraction
    fixture = _reviewed_extraction_fixture(tmp_path)
    detector = extraction._candidates

    def upgraded_detector(text, suffix):
        offset = text.index("Previously undetected fixture argument.")
        return detector(text, suffix) + [{"label": "Parser upgrade new candidate", "kind": "claim",
                                         "statement": "Previously undetected fixture argument.", "offset": offset,
                                         "line": text.count("\n", 0, offset) + 1}]

    monkeypatch.setattr(extraction, "_candidates", upgraded_detector)
    result = extract_paper(tmp_path, fixture["paper"]["paper_id"], fixture["paper"]["version"])
    current = load_data(fixture["inventory_path"])
    assert result["candidate_count"] == 5
    assert current["denominator_reviewed"] is False
    assert current["completeness_status"] == result["completeness_status"] == "not_reviewed"
    previous_ids = {item["claim_id"] for item in fixture["inventory"]["items"]}
    assert all(item in current["items"] for item in fixture["inventory"]["items"])
    added = [item for item in current["items"] if item["claim_id"] not in previous_ids]
    assert len(added) == 1 and added[0]["review_status"] == "candidate"
    assert added[0]["disposition"] == "pending"
    for relative, content in fixture["claim_files"].items():
        assert (tmp_path / relative).read_bytes() == content, relative
    store = ArchiveStore(tmp_path)
    assert store.get_claim(fixture["primary_id"])["verification_status"] == "passed"
    assert store.coverage()["papers"][0]["coverage_ratio"] is None
    assert store.coverage()["papers"][0]["completed"] is False
    # Repeating the upgraded parser does not certify its unreviewed addition.
    extract_paper(tmp_path, fixture["paper"]["paper_id"], fixture["paper"]["version"])
    assert load_data(fixture["inventory_path"])["denominator_reviewed"] is False


def test_new_source_version_does_not_inherit_inventory_review(tmp_path):
    fixture = _reviewed_extraction_fixture(tmp_path)
    previous_inventory = fixture["inventory_path"].read_bytes()
    fixture["source"].write_text(fixture["source"].read_text() + "A changed fixture source version.\n")
    paper = ingest_local(tmp_path, fixture["source"].parent, paper_id=fixture["paper"]["paper_id"])
    assert paper["version"] != fixture["paper"]["version"]
    current = ArchiveStore(tmp_path).get_paper(paper["paper_id"], paper["version"])
    assert current["inventory"]["denominator_reviewed"] is False
    assert current["inventory"]["completeness_status"] == "not_reviewed"
    extract_paper(tmp_path, paper["paper_id"], paper["version"])
    assert ArchiveStore(tmp_path).get_paper(paper["paper_id"], paper["version"])["inventory"]["denominator_reviewed"] is False
    assert fixture["inventory_path"].read_bytes() == previous_inventory
    assert ArchiveStore(tmp_path).get_claim(fixture["primary_id"])["verification_status"] == "passed"


def _theorem(root, theorem_id, visibility="public", dependencies=None, declaration=None):
    base = root / f"corpus/theorems/{theorem_id}"
    write_data(base / "metadata.yaml", {"schema_version": 1, "theorem_id": theorem_id, "title": theorem_id, "summary": "共享引理", "assumptions": [], "visibility": visibility, "proofs": ["proof-" + theorem_id], "lean_declarations": [declaration] if declaration else [], "tags": []})
    write_text(base / "statement.tex", "x=x")
    write_data(base / f"proofs/proof-{theorem_id}/metadata.yaml", {"schema_version": 1, "theorem_id": theorem_id, "proof_id": "proof-" + theorem_id, "visibility": visibility, "dependencies": dependencies or [], "lean_declarations": [declaration] if declaration else []})
    write_text(base / f"proofs/proof-{theorem_id}/proof.zh.md", "通过自反性。")


def _report(root, declarations, commands=None):
    source = root / "lean/HarsanyiLib/Harsanyi.lean"
    write_text(source, "theorem identity : 1 = 1 := rfl\n")
    records = [{"path": source.relative_to(root).as_posix(), "sha256": sha256(source)}]
    fingerprint = digest_data(records)
    write_data(root / "reports/lean/test/report.json", {"schema_version": 1, "build_id": "test", "status": "passed", "source_fingerprint": fingerprint, "source_files": records, "commands": commands if commands is not None else [{"argv": ["lake", "build"], "exit_code": 0}], "declarations": declarations})
    write_data(root / "catalog/library.json", {"schema_version": 1, "source_fingerprint": fingerprint, "verification_report": "reports/lean/test/report.json", "declarations": [{"name": "Harsanyi.identity", "visibility": "public", "verification_status": "passed"}]})
    return source


def test_verification_requires_evidence_and_detects_source_change(tmp_path):
    source = _report(tmp_path, [{"name": "Harsanyi.identity", "status": "passed", "axioms": []}])
    store = ArchiveStore(tmp_path)
    assert store.load_catalog()["declarations"][0]["verification_status"] == "passed"
    source.write_text(source.read_text() + "-- changed\n")
    assert store.load_catalog()["declarations"][0]["verification_status"] == "stale"


@pytest.mark.parametrize("declarations,commands", [([{ "name": "Harsanyi.identity", "status": "passed" }], None), ([{ "name": "Harsanyi.identity", "status": "passed", "axioms": ["sorryAx"] }], None), ([{ "name": "Harsanyi.identity", "status": "passed", "axioms": [] }], []), ([{ "name": "Harsanyi.identity", "status": "passed", "axioms": [] }], [{"exit_code": 1}])])
def test_never_trust_missing_axioms_or_failed_commands(tmp_path, declarations, commands):
    _report(tmp_path, declarations, commands)
    assert ArchiveStore(tmp_path).load_catalog()["declarations"][0]["verification_status"] != "passed"


def test_downstream_declaration_uses_actual_report(tmp_path):
    _theorem(tmp_path, "downstream", declaration="PaperProofs.actual")
    _report(tmp_path, [{"name": "Harsanyi.identity", "status": "passed", "axioms": []}, {"name": "PaperProofs.actual", "status": "passed", "axioms": ["propext"]}])
    assert ArchiveStore(tmp_path).get_theorem("downstream")["verification_status"] == "passed"


def test_public_filters_private_dependencies_issues_and_backlinks(draft):
    root, folder = draft
    paper = ingest_local(root, folder)
    extract_paper(root, paper["paper_id"])
    claim = ArchiveStore(root).list_claims()[0]
    _theorem(root, "private", visibility="private")
    _theorem(root, "public", dependencies=["proof-private"])
    _theorem(root, "independent")
    base = root / "corpus/theorems/independent/metadata.yaml"
    from archive.util import load_data
    data = load_data(base)
    data["source_claim_ids"] = [claim["claim_id"]]  # backlink does not privatize existing result
    write_data(base, data)
    write_data(root / "corpus/issues/issue-private.yaml", {"issue_id": "issue-private", "visibility": "public", "paper_id": paper["paper_id"], "problem": "a local finding", "affected_ids": []})
    store = ArchiveStore(root).public_view()
    assert not store.is_public("proof", "proof-public")
    assert store.get_theorem("public")["proofs"] == []
    assert store.get_theorem("independent") is not None
    assert store.list_issues() == []
    assert store.list_papers() == []


def test_impact_tracks_shared_proof_users(draft):
    root, folder = draft
    paper = ingest_local(root, folder)
    extract_paper(root, paper["paper_id"])
    store = ArchiveStore(root)
    claim = store.list_claims()[0]
    _theorem(root, "shared")
    metadata = root / f"corpus/claims/{claim['claim_id']}/metadata.yaml"
    from archive.util import load_data
    data = load_data(metadata)
    data.update(theorem_ids=["shared"], proof_ids=["proof-shared"])
    write_data(metadata, data)
    affected = store.impact("shared")["affected_ids"]
    assert claim["claim_id"] in affected
    assert paper["paper_id"] in affected


def test_validate_detects_corrupted_original_source(draft):
    root, folder = draft
    paper = ingest_local(root, folder)
    original = root / f"corpus/papers/{paper['paper_id']}/v1/sources/main.md"
    original.write_text("corrupted")
    assert validate_archive(root)["status"] == "failed"


def _coverage_paper(root, records, *, denominator_reviewed=True):
    write_data(root / "corpus/papers/coverage-test/v1/manifest.yaml", {
        "schema_version": 1, "paper_id": "coverage-test", "version": "v1",
        "title": "Synthetic coverage test", "visibility": "private", "files": [],
    })
    write_data(root / "corpus/papers/coverage-test/v1/inventory.yaml", {
        "schema_version": 1, "items": records,
        "denominator_reviewed": denominator_reviewed, "completeness_status": "reviewed",
    })
    for record in records:
        write_data(root / f"corpus/claims/{record['claim_id']}/metadata.yaml", {
            "schema_version": 1, "paper_id": "coverage-test", "paper_version": "v1",
            "visibility": "private", "theorem_ids": [], "proof_ids": [], **record,
        })


def test_coverage_keeps_records_but_counts_canonical_targets_once(tmp_path):
    records = [
        {"claim_id": "main", "kind": "theorem", "review_status": "reviewed",
         "alignment_status": "aligned", "lean_declarations": ["Harsanyi.identity"]},
        {"claim_id": "noise", "kind": "false_positive"},
        {"claim_id": "appendix", "kind": "theorem", "disposition": "duplicate_occurrence", "canonical_claim_id": "main"},
        {"claim_id": "replaced", "kind": "theorem", "canonical_claim_id": "main"},
        {"claim_id": "definition", "kind": "definition"},
        {"claim_id": "assumption", "kind": "assumption"},
        {"claim_id": "observation", "kind": "empirical_observation"},
    ]
    _coverage_paper(tmp_path, records)
    # An in-progress review may classify claim metadata before its inventory
    # row. This must not double count the superseded occurrence.
    replaced = {"schema_version": 1, "paper_id": "coverage-test", "paper_version": "v1",
                "visibility": "private", **records[3], "disposition": "superseded"}
    write_data(tmp_path / "corpus/claims/replaced/metadata.yaml", replaced)
    _report(tmp_path, [{"name": "Harsanyi.identity", "status": "passed", "axioms": []}])
    store = ArchiveStore(tmp_path)
    coverage = store.coverage()
    paper = coverage["papers"][0]
    assert paper["total_candidates"] == coverage["claim_count"] == 7
    assert paper["proof_targets"] == paper["original_claims_proved"] == 1
    assert paper["completed"] is True and paper["coverage_ratio"] == 1
    assert store.get_claim("appendix")["canonical_claim_id"] == "main"


def test_reviewed_denominator_does_not_certify_alignment_or_exclude_issues(tmp_path):
    records = [
        {"claim_id": "main", "kind": "theorem", "review_status": "reviewed",
         "alignment_status": "pending", "lean_declarations": ["Harsanyi.identity"]},
        {"claim_id": "unresolved", "kind": "theorem", "review_status": "issue",
         "disposition": "awaiting_user_confirmation", "alignment_status": "pending"},
    ]
    _coverage_paper(tmp_path, records)
    _report(tmp_path, [{"name": "Harsanyi.identity", "status": "passed", "axioms": []}])
    store = ArchiveStore(tmp_path)
    paper = store.coverage()["papers"][0]
    assert paper["denominator_reviewed"] is True
    assert paper["proof_targets"] == 2 and paper["lean_verified"] == 1
    assert paper["aligned"] == paper["original_claims_proved"] == 0
    assert paper["coverage_ratio"] == 0 and paper["completed"] is False
    from archive.util import load_data
    metadata = tmp_path / "corpus/claims/main/metadata.yaml"
    data = load_data(metadata)
    data["alignment_status"] = "aligned"
    write_data(metadata, data)
    assert store.coverage()["papers"][0]["coverage_ratio"] == 0.5
    _coverage_paper(tmp_path, records, denominator_reviewed=False)
    assert store.coverage()["papers"][0]["coverage_ratio"] is None
    assert store.coverage()["papers"][0]["completed"] is False


def _independent_claim_report(root):
    claim_id = "independent-claim"
    base = root / f"corpus/claims/{claim_id}/lean"
    source = base / "Adapter.lean"
    write_text(source, "theorem Private.adapter : 1 = 1 := rfl\n")
    records = [{"path": source.relative_to(root).as_posix(), "sha256": sha256(source)}]
    report = {"schema_version": 1, "status": "passed", "source_files": records,
              "source_fingerprint": digest_data(records), "commands": [{"exit_code": 0}],
              "declarations": [{"name": "Private.adapter", "status": "passed", "axioms": []}]}
    write_data(base / "report.json", report)
    _coverage_paper(root, [{"claim_id": claim_id, "kind": "theorem", "review_status": "reviewed",
                          "alignment_status": "aligned", "lean_declarations": ["Private.adapter"],
                          "verification_report": f"corpus/claims/{claim_id}/lean/report.json"}])
    return source, base / "report.json", report


def test_independent_claim_uses_own_report_and_expires_without_affecting_library(tmp_path):
    _report(tmp_path, [{"name": "Harsanyi.identity", "status": "passed", "axioms": []}])
    source, _, _ = _independent_claim_report(tmp_path)
    store = ArchiveStore(tmp_path)
    claim = store.get_claim("independent-claim")
    assert claim["verification_status"] == "passed"
    assert claim["verification_scope"] == "independent_claim"
    assert store.coverage()["papers"][0]["original_claims_proved"] == 1
    source.write_text(source.read_text() + "-- changed\n")
    assert store.get_claim("independent-claim")["verification_status"] == "stale"
    assert store.load_catalog()["declarations"][0]["verification_status"] == "passed"


@pytest.mark.parametrize("invalid", ["missing_report", "missing_axioms", "sorry", "failed_command", "missing_sources", "wrong_claim", "global_report"])
def test_independent_claim_rejects_invalid_evidence_and_foreign_report(tmp_path, invalid):
    # Even a global report containing this name cannot certify an invalid
    # explicitly selected claim report.
    _report(tmp_path, [{"name": "Harsanyi.identity", "status": "passed", "axioms": []},
                       {"name": "Private.adapter", "status": "passed", "axioms": []}])
    _, path, report = _independent_claim_report(tmp_path)
    if invalid == "missing_report":
        path.unlink()
    elif invalid == "missing_axioms":
        del report["declarations"][0]["axioms"]
        write_data(path, report)
    elif invalid == "sorry":
        report["declarations"][0]["axioms"] = ["sorryAx"]
        write_data(path, report)
    elif invalid == "failed_command":
        report["commands"][0]["exit_code"] = 1
        write_data(path, report)
    elif invalid == "missing_sources":
        del report["source_files"]
        write_data(path, report)
    else:
        from archive.util import load_data
        metadata = tmp_path / "corpus/claims/independent-claim/metadata.yaml"
        data = load_data(metadata)
        if invalid == "wrong_claim":
            foreign = "corpus/claims/foreign-claim/lean/report.json"
            write_data(tmp_path / foreign, report)
            data["verification_report"] = foreign
        else:
            data["verification_report"] = "reports/lean/test/report.json"
        write_data(metadata, data)
    assert ArchiveStore(tmp_path).get_claim("independent-claim")["verification_status"] != "passed"
