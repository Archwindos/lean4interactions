"""Read cost and integrity regressions using only synthetic archive records."""
from __future__ import annotations

import os
from collections import Counter

import pytest
import yaml

import archive.store as store_module
from archive.store import ArchiveStore
from archive.util import ArchiveError, digest_data, load_data, sha256, write_data, write_text


def _report(root, relative, source_relative, declaration):
    source = root / source_relative
    write_text(source, f"theorem {declaration} : 1 = 1 := rfl\n")
    records = [{"path": source_relative, "sha256": sha256(source)}]
    report = {"status": "passed", "commands": [{"exit_code": 0}],
              "source_files": records, "source_fingerprint": digest_data(records),
              "declarations": [{"name": declaration, "status": "passed", "axioms": []}]}
    write_data(root / relative, report)
    return source, report


@pytest.fixture
def read_root(tmp_path):
    library_source, report = _report(tmp_path, "reports/lean/test/report.json",
                                     "lean/Library.lean", "Test.identity")
    write_data(tmp_path / "catalog/library.json", {
        "source_fingerprint": report["source_fingerprint"],
        "verification_report": "reports/lean/test/report.json",
        "declarations": [{"name": "Test.identity", "visibility": "public"}],
    })
    adapter_source, _ = _report(tmp_path, "corpus/private/claims/private-claim/lean/report.json",
                                "corpus/private/claims/private-claim/lean/Adapter.lean", "Private.adapter")
    for visibility in ("public", "private"):
        paper_id = visibility + "-paper"
        claim_id = visibility + "-claim"
        write_data(tmp_path / f"corpus/{visibility}/papers/{paper_id}/v1/manifest.yaml", {
            "paper_id": paper_id, "version": "v1", "title": paper_id, "visibility": visibility,
        })
        write_data(tmp_path / f"corpus/{visibility}/papers/{paper_id}/v1/inventory.yaml", {
            "items": [{"claim_id": claim_id, "kind": "theorem"}],
            "denominator_reviewed": True, "completeness_status": "reviewed",
        })
        claim = {"claim_id": claim_id, "paper_id": paper_id, "paper_version": "v1",
                 "visibility": visibility, "review_status": "reviewed", "alignment_status": "aligned",
                 "theorem_ids": ["shared"], "proof_ids": ["public-proof"],
                 "lean_declarations": ["Test.identity" if visibility == "public" else "Private.adapter"]}
        if visibility == "private":
            claim["verification_report"] = "corpus/private/claims/private-claim/lean/report.json"
        write_data(tmp_path / f"corpus/{visibility}/claims/{claim_id}/metadata.yaml", claim)
        write_text(tmp_path / f"corpus/{visibility}/claims/{claim_id}/original.tex", "Synthetic body omitted from coverage")
    for theorem_id, derived_from in (("shared", []), ("derived", ["private-claim"])):
        pool = "private" if derived_from else "public"
        write_data(tmp_path / f"corpus/{pool}/theorems/{theorem_id}/metadata.yaml", {
            "theorem_id": theorem_id, "visibility": "public", "derived_from": derived_from,
        })
    for proof_id, source_claims in (("public-proof", []), ("derived-proof", ["private-claim"])):
        pool = "private" if source_claims else "public"
        parent = "derived" if source_claims else "shared"
        write_data(tmp_path / f"corpus/{pool}/theorems/{parent}/proofs/{proof_id}/metadata.yaml", {
            "proof_id": proof_id, "theorem_id": parent, "visibility": pool,
            "source_claim_ids": source_claims,
        })
    write_data(tmp_path / "corpus/private/issues/private-issue.yaml", {
        "issue_id": "private-issue", "visibility": "public", "paper_id": "private-paper",
    })
    return tmp_path, library_source, adapter_source


def test_coverage_does_not_expand_entities_or_reparse_claims(read_root, monkeypatch):
    root, _, _ = read_root
    store = ArchiveStore(root, collection="private")
    def unexpected(*args, **kwargs):
        pytest.fail("Coverage expanded full entities or read a body")
    for method in ("list_papers", "list_claims", "list_theorems", "get_theorem", "get_proof", "_text"):
        monkeypatch.setattr(store, method, unexpected)
    reads = Counter()
    original_load = store_module.load_data
    def counted_load(path, default=None):
        reads[path.relative_to(root).as_posix()] += 1
        return original_load(path, default)
    monkeypatch.setattr(store_module, "load_data", counted_load)
    coverage = store.coverage()
    assert coverage["paper_count"] == coverage["claim_count"] == coverage["theorem_count"] == coverage["proof_count"] == 1
    assert coverage["verified_declarations"] == coverage["open_issues"] == 1
    assert all(paper["completed"] and paper["coverage_ratio"] == 1 for paper in coverage["papers"])
    assert reads["corpus/public/claims/public-claim/metadata.yaml"] == 0
    assert reads["corpus/private/claims/private-claim/metadata.yaml"] == 1
    assert not any(path.endswith(("alignment.yaml", "review.yaml")) for path in reads)


def test_coverage_counts_follow_public_parent_and_dependency_filters(read_root):
    root, _, _ = read_root
    coverage = ArchiveStore(root, public=True).coverage()
    assert coverage["paper_count"] == coverage["claim_count"] == coverage["theorem_count"] == coverage["proof_count"] == 1
    assert coverage["open_issues"] == 0
    assert coverage["papers"][0]["paper_id"] == "public-paper"


@pytest.mark.parametrize("scope", ["library", "independent"])
def test_coverage_rehashes_same_size_sources_with_restored_mtime(read_root, scope):
    root, library_source, adapter_source = read_root
    store = ArchiveStore(root, collection="private")
    assert all(paper["completed"] for paper in store.coverage()["papers"])
    source = library_source if scope == "library" else adapter_source
    before = source.stat()
    old = source.read_bytes()
    changed = old.replace(b"1 = 1", b"2 = 2")
    assert changed != old and len(changed) == len(old)
    source.write_bytes(changed)
    os.utime(source, ns=(before.st_atime_ns, before.st_mtime_ns))
    after = source.stat()
    assert (after.st_size, after.st_mtime_ns) == (before.st_size, before.st_mtime_ns)
    coverage = store.coverage()
    by_id = {paper["paper_id"]: paper for paper in coverage["papers"]+ArchiveStore(root, collection="public").coverage()["papers"]}
    stale_id = "public-paper" if scope == "library" else "private-paper"
    unchanged_id = "private-paper" if scope == "library" else "public-paper"
    assert by_id[stale_id]["lean_verified"] == 0
    assert by_id[stale_id]["completed"] is False
    assert by_id[unchanged_id]["completed"] is True
    assert coverage["verification_status"] == ("stale" if scope == "library" else "passed")


def test_coverage_rereads_metadata_and_rejects_new_source_symlink(read_root):
    root, library_source, _ = read_root
    store = ArchiveStore(root, public=True)
    assert store.coverage()["claim_count"] == 1
    metadata = root / "corpus/public/claims/public-claim/metadata.yaml"
    before = metadata.stat()
    text = metadata.read_text()
    changed = text.replace("visibility: public", "visibility: hidden")
    assert changed != text and len(changed) == len(text)
    metadata.write_text(changed)
    os.utime(metadata, ns=(before.st_atime_ns, before.st_mtime_ns))
    assert store.coverage()["claim_count"] == 0
    alternate = root / "lean/Alternate.lean"
    alternate.write_bytes(library_source.read_bytes())
    library_source.unlink()
    library_source.symlink_to(alternate)
    assert store.coverage()["verification_status"] == "stale"
    with pytest.raises(ArchiveError, match="Symlinks"):
        store.path(library_source)


@pytest.mark.parametrize("fallback", [False, True])
def test_yaml_loaders_are_safe_and_equivalent(tmp_path, monkeypatch, fallback):
    if fallback:
        monkeypatch.delattr(yaml, "CSafeLoader", raising=False)
    path = tmp_path / "metadata.yaml"
    path.write_text("title: '中文'\nitems: [1, true, null]\n")
    assert load_data(path) == {"title": "中文", "items": [1, True, None]}
    path.write_text("!!python/object/apply:builtins.str [unsafe]\n")
    with pytest.raises(yaml.constructor.ConstructorError):
        load_data(path)
