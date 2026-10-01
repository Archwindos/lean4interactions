"""Source integrity and reference validation without mathematical claims."""
from __future__ import annotations

from .store import ArchiveStore
from .util import ArchiveError, identifier, load_data, sha256


def validate_archive(root=None) -> dict:
    store = ArchiveStore(root)
    errors, warnings = [], []
    theorem_ids, proof_ids, claim_ids = set(), set(), set()
    versions = set()
    open_issues = 0
    try:
        for paper in store._paper_versions():
            pid, ver = paper.get("paper_id"), paper.get("version")
            identifier(pid, "paper_id")
            identifier(ver, "version")
            versions.add((pid, ver))
            if paper.get("schema_version") != 1:
                errors.append(f"{pid}/{ver}: unsupported schema_version")
            if paper.get("visibility") not in {"public", "private"}:
                errors.append(f"{pid}/{ver}: invalid visibility")
            base = store.path(f"corpus/papers/{pid}/{ver}")
            for entry in paper.get("files", []):
                relative = entry.get("path", "")
                if not relative.startswith("sources/"):
                    errors.append(f"{pid}/{ver}: source is outside sources/: {relative}")
                    continue
                path = store.path(base / relative, must_exist=True)
                if sha256(path) != entry.get("sha256"):
                    errors.append(f"{pid}/{ver}: checksum mismatch: {relative}")
            inventory = store._data(f"corpus/papers/{pid}/{ver}/inventory.yaml", {})
            if not inventory.get("denominator_reviewed"):
                warnings.append(f"{pid}/{ver}: proof inventory completeness is not reviewed")
        for theorem in store._raw_theorems():
            tid = identifier(theorem.get("theorem_id"), "theorem_id")
            if tid in theorem_ids:
                errors.append(f"Duplicate theorem_id: {tid}")
            theorem_ids.add(tid)
            base = store.path(f"corpus/theorems/{tid}")
            if not (base / "statement.tex").exists():
                errors.append(f"{tid}: statement.tex missing")
            for path in base.glob("proofs/*/metadata.yaml"):
                proof = load_data(store.path(path), {})
                proof_id = identifier(proof.get("proof_id"), "proof_id")
                if proof_id in proof_ids:
                    errors.append(f"Duplicate proof_id: {proof_id}")
                proof_ids.add(proof_id)
                if proof.get("theorem_id", tid) != tid:
                    errors.append(f"{proof_id}: theorem_id disagrees with path")
                if not store.path(path.parent / "proof.zh.md").exists():
                    errors.append(f"{proof_id}: proof.zh.md missing")
        claims = store._raw_claims()
        for claim in claims:
            cid = identifier(claim.get("claim_id"), "claim_id")
            if cid in claim_ids:
                errors.append(f"Duplicate claim_id: {cid}")
            claim_ids.add(cid)
            pair = (claim.get("paper_id"), claim.get("paper_version"))
            if pair not in versions:
                errors.append(f"{cid}: missing paper version {pair}")
            for tid in claim.get("theorem_ids", []):
                if tid not in theorem_ids:
                    errors.append(f"{cid}: missing theorem {tid}")
            for proof_id in claim.get("proof_ids", []):
                if proof_id not in proof_ids:
                    errors.append(f"{cid}: missing proof {proof_id}")
            location = claim.get("source_location", {})
            source = location.get("file") or location.get("path")
            if not source:
                errors.append(f"{cid}: source_location.file missing")
            elif pair in versions:
                store.path(f"corpus/papers/{pair[0]}/{pair[1]}/{source}", must_exist=True)
            if claim.get("review_status") == "candidate":
                warnings.append(f"{cid}: extraction candidate needs review")
        all_ids = theorem_ids | proof_ids | claim_ids | {pid for pid, _ in versions}
        for paper in store._paper_versions():
            inventory = store._data(f"corpus/papers/{paper['paper_id']}/{paper['version']}/inventory.yaml", {})
            for item in inventory.get("items", []):
                if item.get("claim_id") not in claim_ids:
                    errors.append(f"Inventory references missing claim {item.get('claim_id')}")
        for relation in store.relations():
            for key in ("from_id", "to_id"):
                if relation.get(key) not in all_ids:
                    errors.append(f"Relation references missing {key}: {relation.get(key)}")
            if relation.get("review_status") not in {"reviewed", "approved"}:
                warnings.append(f"Shared relation remains {relation.get('review_status', 'unreviewed')}")
        all_issues = store.list_issues()
        open_issues = len(all_issues)
        for issue in all_issues:
            if issue.get("user_confirmation", "pending") == "pending":
                warnings.append(f"{issue['issue_id']}: awaiting user confirmation; no fix authorized")
        verification = store.latest_verification()
        if verification.get("effective_status") != "passed":
            warnings.append(f"Lean verification is {verification.get('effective_status')}")
    except (ArchiveError, OSError, TypeError, KeyError, ValueError) as exc:
        errors.append(str(exc))
    return {"status": "passed" if not errors else "failed", "errors": errors, "warnings": warnings, "counts": {"paper_versions": len(versions), "theorems": len(theorem_ids), "proofs": len(proof_ids), "claims": len(claim_ids)}, "open_issues": open_issues}
