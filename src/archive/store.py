"""Stable read API. Files are authoritative; SQLite is expendable."""
from __future__ import annotations

import copy
from pathlib import Path

from .util import ArchiveError, digest_data, identifier, load_data, resolve_root, safe_path, sha256


class ArchiveStore:
    def __init__(self, root: str | Path | None = None, *, public: bool = False):
        self.root = resolve_root(root)
        self.public = public

    def public_view(self) -> "ArchiveStore":
        return ArchiveStore(self.root, public=True)

    def path(self, value: str | Path, *, must_exist: bool = False) -> Path:
        return safe_path(self.root, value, must_exist=must_exist)

    def _data(self, relative: str, default=None):
        return load_data(self.path(relative), copy.deepcopy(default))

    def _text(self, relative: str) -> str:
        path = self.path(relative)
        return path.read_text(encoding="utf-8") if path.exists() else ""

    def _paper_versions(self) -> list[dict]:
        directory = self.path("corpus/papers")
        result = []
        if directory.exists():
            for path in sorted(directory.glob("*/*/manifest.yaml")):
                manifest = self._data(path, {})
                if isinstance(manifest, dict) and (not self.public or manifest.get("visibility") == "public"):
                    result.append(manifest)
        return result

    def list_papers(self) -> list[dict]:
        grouped = {}
        for manifest in self._paper_versions():
            grouped.setdefault(manifest["paper_id"], []).append(manifest)
        result = []
        for paper_id, versions in grouped.items():
            latest = max(versions, key=lambda item: (item.get("retrieved_at", ""), item.get("version", "")))
            paper = self.get_paper(paper_id, latest["version"])
            paper["versions"] = [{"version": item["version"], "retrieved_at": item.get("retrieved_at"), "visibility": item.get("visibility")} for item in versions]
            result.append(paper)
        return sorted(result, key=lambda item: (item.get("title", ""), item["paper_id"]))

    def get_paper(self, paper_id: str, version: str | None = None) -> dict | None:
        identifier(paper_id, "paper_id")
        if version is None:
            versions = [item for item in self._paper_versions() if item.get("paper_id") == paper_id]
            if not versions:
                return None
            manifest = max(versions, key=lambda item: (item.get("retrieved_at", ""), item.get("version", "")))
            version = manifest["version"]
        identifier(version, "version")
        base = f"corpus/papers/{paper_id}/{version}"
        manifest = self._data(f"{base}/manifest.yaml")
        if not manifest or (self.public and manifest.get("visibility") != "public"):
            return None
        inventory = self._data(f"{base}/inventory.yaml", {"items": [], "completeness_status": "not_reviewed", "denominator_reviewed": False})
        claims = [claim for claim in self.list_claims() if claim.get("paper_id") == paper_id and claim.get("paper_version") == version]
        if self.public:
            inventory = {**inventory, "items": [item for item in inventory.get("items", []) if self.is_public("claim", item.get("claim_id", ""))]}
        return {**manifest, "manifest": manifest, "inventory": inventory, "claims": claims, "base_path": base}

    def _raw_claims(self) -> list[dict]:
        base = self.path("corpus/claims")
        if not base.exists():
            return []
        return [self._data(path, {}) for path in sorted(base.glob("*/metadata.yaml"))]

    def list_claims(self) -> list[dict]:
        results = []
        for raw in self._raw_claims():
            if self.public and not self.is_public("claim", raw.get("claim_id", "")):
                continue
            claim = copy.deepcopy(raw)
            base = f"corpus/claims/{claim['claim_id']}"
            claim.update({"original": self._text(f"{base}/original.tex"), "adaptation": self._text(f"{base}/adaptation.zh.md"), "alignment": self._data(f"{base}/alignment.yaml", {}), "review": self._data(f"{base}/review.yaml", {})})
            if self.public:
                claim["theorem_ids"] = [tid for tid in claim.get("theorem_ids", []) if self.is_public("theorem", tid)]
                claim["proof_ids"] = [pid for pid in claim.get("proof_ids", []) if self.is_public("proof", pid)]
            self._set_claim_verification(claim)
            results.append(claim)
        return results

    def _set_claim_verification(self, claim: dict, *, library_report: dict | None = None) -> None:
        # A public theorem never certifies a paper's alignment. A claim
        # adapter may carry its own report without entering the public API.
        verification = library_report
        if claim.get("verification_report") is not None:
            try:
                report_path = self._claim_report_path(claim["claim_id"], claim["verification_report"])
                verification = self.latest_verification(report_path=report_path)
            except (ArchiveError, TypeError):
                verification = {"effective_status": "unverified", "reason": "Claim report must be a relative JSON file inside this claim's lean directory."}
            claim["verification_scope"] = "independent_claim"
            claim["verification_evidence"] = {key: verification.get(key) for key in ("effective_status", "report_path", "reason")}
        else:
            claim["verification_scope"] = "library_report"
        claim["verification_status"] = self._entity_verification(claim.get("lean_declarations", []), report=verification)

    def _claim_report_path(self, claim_id: str, value: str) -> str:
        if not isinstance(value, str) or "\\" in value:
            raise ArchiveError("Invalid claim report path")
        path = Path(value)
        if path.is_absolute() or path.parts[:4] != ("corpus", "claims", claim_id, "lean") or path.suffix != ".json":
            raise ArchiveError("Claim report is outside its lean directory")
        return self.path(path).relative_to(self.root).as_posix()

    def get_claim(self, claim_id: str) -> dict | None:
        identifier(claim_id, "claim_id")
        return next((item for item in self.list_claims() if item.get("claim_id") == claim_id), None)

    def _raw_theorems(self) -> list[dict]:
        base = self.path("corpus/theorems")
        if not base.exists():
            return []
        return [self._data(path, {}) for path in sorted(base.glob("*/metadata.yaml"))]

    def list_theorems(self) -> list[dict]:
        return [theorem for raw in self._raw_theorems() if (theorem := self.get_theorem(raw["theorem_id"])) is not None]

    def get_theorem(self, theorem_id: str) -> dict | None:
        identifier(theorem_id, "theorem_id")
        base = f"corpus/theorems/{theorem_id}"
        raw = self._data(f"{base}/metadata.yaml")
        if not raw or (self.public and not self.is_public("theorem", theorem_id)):
            return None
        result = copy.deepcopy(raw)
        if self.public:
            result["source_claim_ids"] = [cid for cid in result.get("source_claim_ids", []) if self.is_public("claim", cid)]
        proof_base = self.path(f"{base}/proofs")
        proofs = [self.get_proof(path.parent.name) for path in sorted(proof_base.glob("*/metadata.yaml"))] if proof_base.exists() else []
        result.update({"statement": self._text(f"{base}/statement.tex"), "proofs": [item for item in proofs if item], "claims": [item for item in self.list_claims() if theorem_id in item.get("theorem_ids", [])], "relations": self.relations(theorem_id), "verification_status": self._entity_verification(raw.get("lean_declarations", []))})
        return result

    def _raw_proof(self, proof_id: str) -> dict | None:
        identifier(proof_id, "proof_id")
        base = self.path("corpus/theorems")
        paths = list(base.glob(f"*/proofs/{proof_id}/metadata.yaml")) if base.exists() else []
        if len(paths) > 1:
            raise ArchiveError(f"Duplicate proof_id: {proof_id}")
        if not paths:
            return None
        raw = self._data(paths[0], {})
        return {**raw, "theorem_id": raw.get("theorem_id", paths[0].parents[2].name), "base_path": paths[0].parent.relative_to(self.root).as_posix()}

    def get_proof(self, proof_id: str) -> dict | None:
        raw = self._raw_proof(proof_id)
        if not raw or (self.public and not self.is_public("proof", proof_id)):
            return None
        result = copy.deepcopy(raw)
        result.update({"text": self._text(f"{raw['base_path']}/proof.zh.md"), "proof": self._text(f"{raw['base_path']}/proof.zh.md"), "claims": [item for item in self.list_claims() if proof_id in item.get("proof_ids", [])], "relations": self.relations(proof_id), "verification_status": self._entity_verification(raw.get("lean_declarations", []))})
        return result

    def is_public(self, kind: str, entity_id: str, _seen: set[str] | None = None) -> bool:
        """Fail closed; private parents/dependencies propagate to derived records."""
        if not entity_id:
            return False
        seen = set(_seen or ())
        key = f"{kind}:{entity_id}"
        if key in seen:
            return False
        seen.add(key)
        try:
            identifier(entity_id)
            if kind == "issue":
                return any(item.get("issue_id") == entity_id for item in ArchiveStore(self.root, public=True).list_issues())
            if kind == "paper":
                versions = ArchiveStore(self.root)._paper_versions()
                return any(item.get("paper_id") == entity_id and item.get("visibility") == "public" for item in versions)
            if kind == "claim":
                raw = self._data(f"corpus/claims/{entity_id}/metadata.yaml", {})
                manifest = self._data(f"corpus/papers/{raw.get('paper_id')}/{raw.get('paper_version')}/manifest.yaml", {})
                return raw.get("visibility") == "public" and manifest.get("visibility") == "public"
            if kind == "theorem":
                raw = self._data(f"corpus/theorems/{entity_id}/metadata.yaml", {})
            elif kind == "proof":
                raw = self._raw_proof(entity_id) or {}
                if not self.is_public("theorem", raw.get("theorem_id", ""), seen):
                    return False
            else:
                return False
            if raw.get("visibility") != "public":
                return False
            for source in raw.get("derived_from", []) + (raw.get("source_claim_ids", []) if kind == "proof" else []):
                if not self.is_public("claim", source, seen):
                    return False
            for dependency in raw.get("dependencies", []):
                dep = dependency.get("id") if isinstance(dependency, dict) else dependency
                if isinstance(dep, str) and self._raw_proof(dep):
                    if not self.is_public("proof", dep, seen):
                        return False
                if isinstance(dep, str) and self._data(f"corpus/claims/{dep}/metadata.yaml"):
                    if not self.is_public("claim", dep, seen):
                        return False
                # Lean declaration names are not private archive entities.
                if isinstance(dep, str) and (self._data(f"corpus/theorems/{dep}/metadata.yaml") is not None):
                    if not self.is_public("theorem", dep, seen):
                        return False
            return True
        except (ArchiveError, TypeError):
            return False

    def relations(self, entity_id: str | None = None) -> list[dict]:
        data = self._data("corpus/relations.yaml", {"relations": []})
        items = list(data.get("relations", []))
        # Local-only relations stay outside the published corpus. Public reads
        # must never open the optional private file, even to filter it later.
        if not self.public:
            local = self._data("corpus/relations-local-private.yaml", {"relations": []})
            items.extend(local.get("relations", []))
        result = []
        for item in items:
            if entity_id and entity_id not in {item.get("from_id"), item.get("to_id")}:
                continue
            if self.public:
                if item.get("visibility") != "public":
                    continue
                if not all(self._any_public(item.get(key, "")) for key in ("from_id", "to_id")):
                    continue
            result.append(item)
        return result

    def _any_public(self, entity_id: str) -> bool:
        return any(self.is_public(kind, entity_id) for kind in ("paper", "claim", "theorem", "proof"))

    def latest_verification(self, report_path: str | None = None) -> dict:
        catalog = {} if report_path is not None else (self._data("catalog/library.json", {}) or {})
        report_path = report_path if report_path is not None else catalog.get("verification_report")
        if not report_path:
            reports = self.path("reports/lean")
            candidates = sorted(reports.glob("*/report.json")) if reports.exists() else []
            report_path = candidates[-1].relative_to(self.root).as_posix() if candidates else None
        if not report_path:
            return {"status": "unavailable", "effective_status": "unavailable", "reason": "No actual Lean verification report exists."}
        try:
            if not self.path(report_path).is_file():
                return {"status": "unavailable", "effective_status": "unavailable", "report_path": report_path, "reason": "No actual verification report exists at the recorded path."}
            report = self._data(report_path, {}) or {}
            result = {**report, "report_path": report_path, "effective_status": report.get("status", "unavailable")}
            commands = report.get("commands")
            if report.get("status") == "passed" and (not commands or not all(command.get("exit_code") == 0 for command in commands)):
                result.update(effective_status="unverified", reason="Passing report has no successful build command evidence.")
            records = report.get("source_files")
            if not records:
                result.update(effective_status="unverified", reason="Source fingerprint cannot be checked; report has no source_files.")
                return result
            current = []
            for entry in records:
                path = self.path(entry["path"], must_exist=True)
                current.append({"path": entry["path"], "sha256": sha256(path)})
            fingerprint = digest_data(sorted(current, key=lambda item: item["path"]))
            if fingerprint != report.get("source_fingerprint") or any(a["sha256"] != b["sha256"] for a, b in zip(sorted(records, key=lambda item: item["path"]), sorted(current, key=lambda item: item["path"]))):
                result.update(effective_status="stale", reason="Lean sources, toolchain or dependency locks changed.")
            if catalog.get("source_fingerprint") and catalog["source_fingerprint"] != report.get("source_fingerprint"):
                result.update(effective_status="stale", reason="Catalog and report fingerprints disagree.")
            return result
        except (ArchiveError, OSError, KeyError, TypeError, ValueError) as exc:
            return {"status": "unavailable", "effective_status": "stale", "report_path": report_path, "reason": str(exc)}

    def load_catalog(self) -> dict:
        catalog = copy.deepcopy(self._data("catalog/library.json", {"schema_version": 1, "declarations": []}) or {})
        verification = self.latest_verification()
        declarations = verification.get("declarations", [])
        declarations = list(declarations.values()) if isinstance(declarations, dict) else declarations
        report_by_name = {item.get("name"): item for item in declarations}
        entries = []
        for raw in catalog.get("declarations", []):
            entry = dict(raw)
            if self.public and (entry.get("visibility") != "public" or (entry.get("theorem_id") and not self.is_public("theorem", entry["theorem_id"])) or (entry.get("proof_id") and not self.is_public("proof", entry["proof_id"]))):
                continue
            effective = verification.get("effective_status", "unavailable")
            actual = report_by_name.get(entry.get("name"), {})
            axioms = actual.get("axioms")
            if effective == "passed" and "axioms" in actual and actual.get("status") == "passed" and isinstance(axioms, list) and not (set(axioms) - {"propext", "Classical.choice", "Quot.sound"}):
                entry["verification_status"] = "passed"
            else:
                entry["verification_status"] = effective if effective != "passed" else "unverified"
            entry["report_path"] = verification.get("report_path")
            entry["declaration"] = entry.get("name")
            entries.append(entry)
        catalog["declarations"] = entries
        catalog["verification"] = verification if not self.public else {"effective_status": verification.get("effective_status"), "reason": verification.get("reason")}
        return catalog

    def _entity_verification(self, declarations: list, *, report: dict | None = None) -> str:
        if not declarations:
            return "not_formalized"
        names = [item.get("name") if isinstance(item, dict) else item for item in declarations]
        report = self.latest_verification() if report is None else report
        effective = report.get("effective_status", "unavailable")
        if effective != "passed":
            return "stale" if effective == "stale" else "unverified"
        actual = report.get("declarations", [])
        actual = list(actual.values()) if isinstance(actual, dict) else actual
        by_name = {item.get("name"): item for item in actual}
        for name in names:
            entry = by_name.get(name, {})
            axioms = entry.get("axioms")
            if entry.get("status") != "passed" or not isinstance(axioms, list) or set(axioms) - {"propext", "Classical.choice", "Quot.sound"}:
                return "unverified"
        return "passed"

    def build_index(self) -> dict:
        from .search import build_index
        return build_index(self)

    def search(self, query: str, kind: str | None = None, limit: int = 50) -> list[dict]:
        from .search import search
        return search(self, query, kind=kind, limit=limit)

    def search_lemmas(self, query: str, limit: int = 50) -> list[dict]:
        entries = self.load_catalog().get("declarations", [])
        query = query.casefold()
        return [item for item in entries if all(token in str(item).casefold() for token in query.split())][:limit]

    def show_lemma(self, entity_id: str) -> dict | None:
        return next((item for item in self.load_catalog().get("declarations", []) if entity_id in {item.get("name"), item.get("theorem_id"), item.get("proof_id")}), None)

    def impact(self, entity_id: str) -> dict:
        edges = {}
        for theorem in self._raw_theorems():
            tid = theorem["theorem_id"]
            for path in self.path(f"corpus/theorems/{tid}/proofs").glob("*/metadata.yaml"):
                proof = self._data(path, {})
                for dep in proof.get("dependencies", []):
                    source = dep.get("id") if isinstance(dep, dict) else dep
                    edges.setdefault(source, set()).update({proof.get("proof_id"), tid})
        for claim in self._raw_claims():
            for source in claim.get("theorem_ids", []) + claim.get("proof_ids", []):
                edges.setdefault(source, set()).update({claim["claim_id"], claim["paper_id"]})
        for relation in self.relations():
            if relation.get("relation_type") in {"depends_on", "uses", "special_case", "corollary"}:
                edges.setdefault(relation.get("to_id"), set()).add(relation.get("from_id"))
        affected, frontier = set(), [entity_id]
        while frontier:
            for target in edges.get(frontier.pop(), set()):
                if target and target != entity_id and target not in affected:
                    affected.add(target)
                    frontier.append(target)
        if self.public:
            affected = {item for item in affected if self._any_public(item)}
        return {"entity_id": entity_id, "affected_ids": sorted(affected), "count": len(affected), "requires_revalidation": bool(affected)}

    def coverage(self) -> dict:
        papers = []
        non_proof_kinds = {"definition", "assumption", "empirical_observation"}
        excluded_dispositions = {"false_positive", "duplicate_occurrence", "superseded"}
        # Coverage needs metadata and actual verification, not full proof or
        # claim bodies/backlinks. Share evidence only within this call; future
        # calls must re-read metadata and rehash current Lean source files.
        library_report = self.latest_verification()
        all_claims = []
        claims_by_paper = {}
        for claim in self._raw_claims():
            if self.public and not self.is_public("claim", claim.get("claim_id", "")):
                continue
            self._set_claim_verification(claim, library_report=library_report)
            all_claims.append(claim)
            claims_by_paper.setdefault((claim.get("paper_id"), claim.get("paper_version")), {})[claim["claim_id"]] = claim
        latest_papers = {}
        for manifest in self._paper_versions():
            paper_id = manifest["paper_id"]
            current = latest_papers.get(paper_id)
            if current is None or (manifest.get("retrieved_at", ""), manifest.get("version", "")) > (current.get("retrieved_at", ""), current.get("version", "")):
                latest_papers[paper_id] = manifest
        for paper in sorted(latest_papers.values(), key=lambda item: (item.get("title", ""), item["paper_id"])):
            paper_id = identifier(paper["paper_id"], "paper_id")
            version = identifier(paper["version"], "version")
            inventory = self._data(f"corpus/papers/{paper_id}/{version}/inventory.yaml", {"items": [], "completeness_status": "not_reviewed", "denominator_reviewed": False})
            items = inventory.get("items", [])
            if self.public:
                items = [item for item in items if self.is_public("claim", item.get("claim_id", ""))]
            claims = claims_by_paper.get((paper_id, version), {})
            # Retain every occurrence for provenance, while counting each
            # reviewed mathematical target once. Issues and unfinished proofs
            # remain targets; only explicit classification can exclude a row.
            target = [item for item in items if not any(
                record.get("kind") in non_proof_kinds | excluded_dispositions
                or record.get("disposition") in excluded_dispositions
                for record in (item, claims.get(item.get("claim_id"), {}))
            )]
            reviewed = sum(claims.get(item.get("claim_id"), item).get("review_status") in {"reviewed", "approved"} for item in target)
            aligned = sum(claims.get(item.get("claim_id"), {}).get("alignment_status") in {"aligned", "approved"} for item in target)
            verified = sum(claims.get(item.get("claim_id"), {}).get("verification_status") == "passed" for item in target)
            proven_original = sum(claims.get(item.get("claim_id"), {}).get("verification_status") == "passed" and claims.get(item.get("claim_id"), {}).get("alignment_status") in {"aligned", "approved"} for item in target)
            denominator_reviewed = inventory.get("denominator_reviewed") is True
            papers.append({"paper_id": paper["paper_id"], "version": paper["version"], "total_candidates": len(items), "proof_targets": len(target), "denominator_reviewed": denominator_reviewed, "completeness_status": inventory.get("completeness_status", "not_reviewed"), "reviewed": reviewed, "aligned": aligned, "lean_verified": verified, "original_claims_proved": proven_original, "completed": bool(denominator_reviewed and target and reviewed == aligned == verified == len(target)), "coverage_ratio": proven_original / len(target) if target and denominator_reviewed else None})
        theorem_count = proof_count = 0
        for raw in self._raw_theorems():
            theorem_id = identifier(raw["theorem_id"], "theorem_id")
            base = f"corpus/theorems/{theorem_id}"
            if not self._data(f"{base}/metadata.yaml") or (self.public and not self.is_public("theorem", theorem_id)):
                continue
            theorem_count += 1
            proof_base = self.path(f"{base}/proofs")
            for path in sorted(proof_base.glob("*/metadata.yaml")) if proof_base.exists() else []:
                proof_id = path.parent.name
                if self._raw_proof(proof_id) and (not self.public or self.is_public("proof", proof_id)):
                    proof_count += 1
        catalog = self.load_catalog()
        return {"papers": papers, "paper_count": len(papers), "claim_count": len(all_claims), "theorem_count": theorem_count, "proof_count": proof_count, "verified_declarations": sum(item.get("verification_status") == "passed" for item in catalog.get("declarations", [])), "reviewed_shared_relations": sum(item.get("review_status") in {"reviewed", "approved"} for item in self.relations()), "verification_status": catalog.get("verification", {}).get("effective_status", "unavailable"), "open_issues": len(self.list_issues())}


    def list_issues(self) -> list[dict]:
        base = self.path("corpus/issues")
        if not base.exists():
            return []
        results = []
        for path in sorted(base.glob("*.yaml")):
            issue = self._data(path, {})
            if self.public:
                if issue.get("visibility") != "public":
                    continue
                references = []
                for field in ("claim_ids", "theorem_ids", "proof_ids", "paper_ids", "affected_ids", "derived_from"):
                    references.extend(issue.get(field, []))
                for field in ("paper_id", "claim_id", "theorem_id", "proof_id"):
                    if issue.get(field):
                        references.append(issue[field])
                if references and not all(self._any_public(value) for value in references):
                    continue
            results.append(issue)
        return results

    def get_issue(self, issue_id: str) -> dict | None:
        identifier(issue_id, "issue_id")
        return next((issue for issue in self.list_issues() if issue.get("issue_id") == issue_id), None)
