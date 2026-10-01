#!/usr/bin/env python3
"""Local read-only paper package. No MCP server, shell runner, network, or writes."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import sys
from typing import Any


BASE = Path(__file__).resolve().parent
PROJECT_ROOT = BASE.parents[2]
MANIFEST = BASE / "agent-package.json"
SCHEMA = BASE / "package.schema.json"
COLLECTIONS = (
    "papers", "versions", "sources", "occurrences", "propositions", "shared_proofs",
    "results", "adapters", "verification_reports", "issues", "alignment_notes", "resources", "prompts",
)
AXIOMS = {"propext", "Quot.sound", "Classical.choice"}
REFERENCE_FIELDS = {
    "paper_id", "version_id", "source_id", "result_id", "proposition_id", "proof_id",
    "version_ids", "source_ids", "occurrence_ids", "proposition_ids", "proof_ids",
    "adapter_ids", "verification_report_ids", "issue_ids", "source_occurrence_ids",
    "result_ids", "subject_ids", "dependency_ids", "derived_from_ids",
    "alignment_note_ids",
}


class PackageError(ValueError):
    pass


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fingerprint(records: list[dict[str, str]]) -> str:
    ordered = sorted(records, key=lambda item: item["path"])
    raw = json.dumps(ordered, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def unsupported_schema_keywords(schema: dict, at: str = "schema") -> list[str]:
    supported = {"$schema", "$id", "$defs", "$ref", "title", "description", "type", "required",
                 "properties", "additionalProperties", "items", "enum", "const", "pattern",
                 "minLength", "maxLength", "minItems", "maxItems", "uniqueItems", "minimum",
                 "maximum", "default"}
    errors = [f"{at}: unsupported schema keyword {key}" for key in schema if key not in supported]
    if isinstance(schema.get("additionalProperties"), dict):
        errors.append(f"{at}: additionalProperties schemas are unsupported; use a boolean")
    for collection in ["properties", "$defs"]:
        for name, item in schema.get(collection, {}).items():
            errors.extend(unsupported_schema_keywords(item, f"{at}.{collection}.{name}"))
    if isinstance(schema.get("items"), dict):
        errors.extend(unsupported_schema_keywords(schema["items"], f"{at}.items"))
    return errors


def structural_errors(value: Any, schema: dict, root: dict | None = None, at: str = "$") -> list[str]:
    """Validate the used Draft 2020-12 subset without third-party dependencies."""
    if root is None:
        unsupported = unsupported_schema_keywords(schema)
        if unsupported:
            return unsupported
    root = root or schema
    if "$ref" in schema:
        ref = schema["$ref"]
        if not ref.startswith("#/$defs/"):
            return [f"{at}: unsupported schema reference"]
        return structural_errors(value, root["$defs"][ref.split("/")[-1]], root, at)
    errors = []
    types = {"object": dict, "array": list, "string": str, "boolean": bool,
             "integer": int, "number": (int, float), "null": type(None)}
    typ = schema.get("type")
    candidates = typ if isinstance(typ, list) else [typ] if typ else []
    if candidates and not any(isinstance(value, types[t]) and not
        (t in {"integer", "number"} and isinstance(value, bool)) for t in candidates):
        return [f"{at}: expected {typ}"]
    if "const" in schema and value != schema["const"]:
        errors.append(f"{at}: unexpected constant")
    if "enum" in schema and value not in schema["enum"]:
        errors.append(f"{at}: not in allowed values")
    if isinstance(value, dict):
        for key in schema.get("required", []):
            if key not in value:
                errors.append(f"{at}: missing {key}")
        props = schema.get("properties", {})
        for key, item in value.items():
            if key in props:
                errors.extend(structural_errors(item, props[key], root, f"{at}.{key}"))
            elif schema.get("additionalProperties") is False:
                errors.append(f"{at}: unexpected {key}")
    if isinstance(value, list):
        if len(value) < schema.get("minItems", 0):
            errors.append(f"{at}: too few items")
        if len(value) > schema.get("maxItems", len(value)):
            errors.append(f"{at}: too many items")
        if schema.get("uniqueItems") and len({json.dumps(x, sort_keys=True) for x in value}) != len(value):
            errors.append(f"{at}: duplicate array value")
        for i, item in enumerate(value):
            if "items" in schema:
                errors.extend(structural_errors(item, schema["items"], root, f"{at}[{i}]"))
    if isinstance(value, str):
        if len(value) < schema.get("minLength", 0):
            errors.append(f"{at}: string too short")
        if len(value) > schema.get("maxLength", len(value)):
            errors.append(f"{at}: string too long")
        if "pattern" in schema and re.search(schema["pattern"], value) is None:
            errors.append(f"{at}: pattern mismatch")
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        if value < schema.get("minimum", value) or value > schema.get("maximum", value):
            errors.append(f"{at}: outside allowed range")
    return errors


class PaperPackage:
    def __init__(self, root: Path = PROJECT_ROOT, manifest: dict | None = None,
                 math_content: dict | None = None):
        self.root = root.resolve()
        self.data = manifest if manifest is not None else read_json(MANIFEST)
        self.nodes = {}
        self.kinds = {}
        for collection in COLLECTIONS:
            for record in self.data.get(collection, []):
                if record.get("id") in self.nodes:
                    raise PackageError(f"duplicate stable ID: {record['id']}")
                self.nodes[record["id"]] = record
                self.kinds[record["id"]] = collection
        self.math = math_content
        if self.math is None:
            path = self.file(self.data["data_files"]["math_path"])
            self.math = read_json(path) if path.is_file() else {"results": [], "shared_proofs": []}
        self.math_results = {r["id"]: r for r in self.math.get("results", [])}
        self.math_proofs = {r["id"]: r for r in self.math.get("shared_proofs", [])}

    def file(self, name: str) -> Path:
        rel = PurePosixPath(name)
        if not name or rel.is_absolute() or ".." in rel.parts or "\\" in name:
            raise PackageError(f"unsafe project-relative path: {name}")
        path = self.root
        for part in rel.parts:
            path = path / part
            if path.is_symlink():
                raise PackageError(f"symbolic link excluded: {name}")
        if not path.resolve().is_relative_to(self.root):
            raise PackageError(f"path leaves project: {name}")
        return path

    @staticmethod
    def refs(node: dict) -> set[str]:
        values = set()
        for key in REFERENCE_FIELDS:
            value = node.get(key)
            if isinstance(value, str):
                values.add(value)
            elif isinstance(value, list):
                values.update(x for x in value if isinstance(x, str))
        return values

    def visible_ids(self, include_private: bool = False) -> set[str]:
        if include_private:
            return set(self.nodes)
        visible = {key for key, node in self.nodes.items() if node.get("visibility") == "public"}
        # Source-derived entities inherit privacy. Independent public library proofs have no
        # source provenance, so a private paper's use of them cannot privatize the library.
        changed = True
        while changed:
            changed = False
            for key in list(visible):
                node = self.nodes[key]
                if self.refs(node) - visible:
                    visible.remove(key)
                    changed = True
        return visible

    def get(self, identity: str, include_private: bool = False) -> dict:
        if identity not in self.visible_ids(include_private):
            raise PackageError("unknown or unavailable ID")
        return self.nodes[identity]

    def report_evidence(self, identity: str) -> dict:
        node = self.nodes[identity]
        out = {"id": identity, "path": node["path"], "scope": node["scope"],
               "compilation": "unavailable", "axiom_audit": "unavailable", "freshness": "unknown"}
        try:
            report = read_json(self.file(node["path"]))
        except (OSError, ValueError) as error:
            out["reason"] = str(error)
            return out
        if not isinstance(report, dict):
            out["reason"] = "report must be a JSON object"
            return out
        files = report.get("source_files")
        if not isinstance(files, list) or not files or not report.get("source_fingerprint"):
            out["reason"] = "report lacks source file hashes or fingerprint"
            return out
        if any(not isinstance(source, dict) or not isinstance(source.get("path"), str) or
               not isinstance(source.get("sha256"), str) or
               re.fullmatch(r"[0-9a-f]{64}", source["sha256"]) is None for source in files):
            out["reason"] = "malformed report source file evidence"
            return out
        if len({source.get("path") for source in files}) != len(files):
            out["reason"] = "duplicate report source paths"
            return out
        mismatches = []
        for source in files:
            try:
                path = self.file(source["path"])
                if not path.is_file() or digest(path) != source.get("sha256"):
                    mismatches.append(source["path"])
            except (PackageError, KeyError):
                mismatches.append(source.get("path", "invalid path"))
        if mismatches or fingerprint(files) != report["source_fingerprint"]:
            out.update(freshness="stale", compilation="stale", axiom_audit="stale",
                       changed_files=mismatches)
            return out
        out["freshness"] = "current"
        commands = report.get("commands", [])
        declaration_list = report.get("declarations", [])
        if not isinstance(commands, list) or not all(isinstance(c, dict) for c in commands) or not isinstance(
            declaration_list, list) or not all(isinstance(d, dict) for d in declaration_list):
            out["reason"] = "malformed command or declaration evidence"
            return out
        declarations = {d.get("name"): d for d in declaration_list}
        if len(declarations) != len(declaration_list):
            out["reason"] = "duplicate declaration evidence"
            return out
        selected = [declarations.get(name) for name in node["expected_declarations"]]
        if (not commands or not selected or any(d is None for d in selected) or
            any("exit_code" not in cmd for cmd in commands)):
            out["reason"] = "commands or requested declaration evidence missing"
            return out
        source_paths = {source["path"] for source in files}
        if any(d.get("source_path") not in source_paths for d in selected):
            out["reason"] = "requested declaration source is outside the pinned report inputs"
            return out
        if not any("build" in cmd.get("argv", []) or
                   ("lean" in cmd.get("argv", []) and "--version" not in cmd.get("argv", []))
                   for cmd in commands):
            out["reason"] = "successful toolchain query is not compilation evidence"
            return out
        out["compilation"] = "passed" if report.get("status") == "passed" and all(
            cmd["exit_code"] == 0 for cmd in commands) and all(
            d.get("status") == "passed" for d in selected) else "failed"
        audit_present = any(any("audit" in str(arg).lower() for arg in cmd.get("argv", []))
                            for cmd in commands)
        if not audit_present:
            out["reason"] = "audit command evidence missing"
        elif any(not isinstance(d.get("axioms"), list) for d in selected):
            out["reason"] = "explicit axiom lists missing"
        else:
            unexpected = sorted({a for d in selected for a in d["axioms"]} - AXIOMS)
            out["axiom_audit"] = "failed" if unexpected else "passed"
            out["unexpected_axioms"] = unexpected
        out["declarations"] = [{"name": d["name"], "status": d.get("status"),
                                "axioms": d.get("axioms")} for d in selected if d]
        out["source_semantics_automatically_verified"] = False
        return out

    def verification_status(self, identity: str | None = None, include_private: bool = False) -> dict:
        if identity is None:
            return {"scope": "selected result records only", "results": [
                self.verification_status(r["id"], include_private) for r in self.data["results"]
                if r["id"] in self.visible_ids(include_private)]}
        record = self.get(identity, include_private)
        ids = record.get("verification_report_ids", [])
        if self.kinds[identity] == "verification_reports":
            ids = [identity]
        reports = [self.report_evidence(r) for r in ids if r in self.visible_ids(include_private)]
        def combine(field: str) -> str:
            statuses = [r[field] for r in reports]
            for priority in ["stale", "failed", "unavailable"]:
                if priority in statuses:
                    return priority
            return "passed" if statuses else "unavailable"
        return {"id": identity, "record_kind": self.kinds[identity],
                "scope": record.get("scope", record.get("completion_scope", "declared record only")),
                "completion_scope": record.get("completion_scope", "not_applicable"),
                "source_alignment": record.get("alignment_status", "not_applicable"),
                "readable_rewrite": record.get("rewrite_status", "not_applicable"),
                "user_review": record.get("user_review_status", "not_recorded"),
                "compilation": combine("compilation"), "axiom_audit": combine("axiom_audit"),
                "reports": reports, "issue_ids": record.get("issue_ids", []),
                "alignment_note_ids": record.get("alignment_note_ids", [])}

    def query(self, text: str = "", paper_id: str | None = None, kind: str | None = None,
              include_private: bool = False) -> dict:
        if paper_id is not None:
            self.get(paper_id, include_private)
            if self.kinds[paper_id] != "papers":
                raise PackageError("paper_id must identify a paper")
        selected = []
        for node in self.data["results"]:
            if node["id"] not in self.visible_ids(include_private):
                continue
            if paper_id and node["paper_id"] != paper_id:
                continue
            if kind and node["kind"] != kind:
                continue
            haystack = json.dumps([node] + [self.nodes[x] for x in
                                  node["proposition_ids"] + node["adapter_ids"]], ensure_ascii=False).casefold()
            if text.casefold() not in haystack:
                continue
            selected.append({"id": node["id"], "paper_id": node["paper_id"], "title": node["title"],
                             "kind": node["kind"], "proposition_ids": node["proposition_ids"],
                             "proof_ids": node["proof_ids"], "verification": self.verification_status(node["id"], include_private)})
        return {"count": len(selected), "denominator": "selected result records; repeated source appearances excluded",
                "results": selected}

    def get_result(self, identity: str, include_private: bool = False) -> dict:
        node = self.get(identity, include_private)
        if self.kinds[identity] != "results":
            raise PackageError("ID must identify a result")
        visible = self.visible_ids(include_private)
        mathematics = self.math_results.get(identity)
        if mathematics and mathematics.get("visibility", "public") == "private" and not include_private:
            mathematics = None
        return {"result": node, "mathematical_content": mathematics,
                "occurrences": [self.nodes[x] for x in node["occurrence_ids"] if x in visible],
                "propositions": [self.nodes[x] for x in node["proposition_ids"] if x in visible],
                "shared_proofs": [{"metadata": self.nodes[x], "content": self.math_proofs.get(x)}
                                  for x in node["proof_ids"] if x in visible],
                "adapters": [self.nodes[x] for x in node["adapter_ids"] if x in visible],
                "issues": [self.nodes[x] for x in node["issue_ids"] if x in visible],
                "alignment_notes": [self.nodes[x] for x in node.get("alignment_note_ids", []) if x in visible],
                "verification": self.verification_status(identity, include_private)}

    def dependencies(self, identity: str, depth: int = 2, include_private: bool = False) -> dict:
        self.get(identity, include_private)
        if depth < 1 or depth > 5:
            raise PackageError("depth must be between 1 and 5")
        visible = self.visible_ids(include_private)
        seen = {identity}
        frontier = {identity}
        edges = []
        for _ in range(depth):
            nxt = set()
            for edge in self.data["edges"]:
                if (edge["visibility"] == "private" and not include_private) or not {
                    edge["from_id"], edge["to_id"]}.issubset(visible):
                    continue
                if edge["from_id"] in frontier:
                    if edge not in edges:
                        edges.append(edge)
                    if edge["to_id"] not in seen:
                        nxt.add(edge["to_id"])
            seen |= nxt
            frontier = nxt
        return {"root_id": identity, "depth": depth, "nodes": [self.nodes[x] for x in sorted(seen)],
                "edges": edges, "direction": "explicit outgoing relations"}

    def resources(self, include_private: bool = False) -> dict:
        visible = self.visible_ids(include_private)
        return {"resources": [node for node in self.data["resources"] if node["id"] in visible]}

    def get_resource(self, identity: str, include_private: bool = False) -> dict:
        node = self.get(identity, include_private)
        if self.kinds[identity] != "resources":
            raise PackageError("ID must identify a registered resource")
        path = self.file(node["path"])
        if not path.is_file():
            raise PackageError("registered resource is unavailable")
        actual = digest(path)
        if node.get("sha256") and actual != node["sha256"]:
            raise PackageError("resource changed since package pinning")
        out = {"resource": node, "actual_sha256": actual, "size_bytes": path.stat().st_size}
        if node.get("record_collection"):
            data = read_json(path)
            selected = next((item for item in data.get(node["record_collection"], [])
                             if item.get("id") == node["record_id"]), None)
            if selected is None:
                raise PackageError("registered JSON record is unavailable")
            out["record"] = selected
        elif node["mime_type"] != "application/pdf":
            out["text"] = path.read_text(encoding="utf-8")
        else:
            out["retrieval"] = "read pinned local_path with a PDF reader; CLI does not encode binary data"
        return out

    def validate(self) -> dict:
        errors = structural_errors(self.data, read_json(SCHEMA))
        warnings = []
        papers = read_json(self.file(self.data["data_files"]["papers_path"]))
        ui_papers = {p["id"]: p for p in papers.get("papers", [])}
        excerpts = read_json(self.file(self.data["data_files"]["source_excerpts_path"]))
        excerpt_ids = {e["id"] for e in excerpts.get("excerpts", [])}
        if papers.get("schema_version") != "2.0" or self.math.get("schema_version") != "2.0":
            errors.append("UI and mathematics data must use schema_version 2.0")
        for collection in ["results", "shared_proofs"]:
            ids = [r["id"] for r in self.math.get(collection, [])]
            if len(set(ids)) != len(ids):
                errors.append(f"math-content: duplicate {collection} ID")
        for excerpt in excerpts.get("excerpts", []):
            for key in ["page_text_paths", "proof_page_text_paths"]:
                for ref in excerpt[key]:
                    try:
                        if digest(self.file(ref["path"])) != ref["sha256"]:
                            errors.append(f"{excerpt['id']}: changed page text extract")
                    except (PackageError, OSError):
                        errors.append(f"{excerpt['id']}: missing page text extract")
            try:
                if digest(self.file(excerpt["transcription_path"])) != excerpt["transcription_sha256"]:
                    errors.append(f"{excerpt['id']}: changed mathematical transcription")
            except (PackageError, OSError):
                errors.append(f"{excerpt['id']}: missing mathematical transcription")
        for identity, node in self.nodes.items():
            for ref in self.refs(node):
                if ref not in self.nodes:
                    errors.append(f"{identity}: dangling foreign key {ref}")
            if node.get("visibility") == "public" and identity not in self.visible_ids():
                errors.append(f"{identity}: public record depends on private/unavailable provenance")
            for key in ["path", "source_path", "content_path"]:
                if key in node:
                    try:
                        path = self.file(node[key])
                        if not path.is_file():
                            errors.append(f"{identity}: missing {key}")
                        if key == "path" and node.get("sha256") and path.is_file() and digest(path) != node["sha256"]:
                            errors.append(f"{identity}: changed resource")
                    except PackageError as error:
                        errors.append(f"{identity}: {error}")
        for paper in self.data["papers"]:
            if paper["id"] not in ui_papers:
                errors.append(f"{paper['id']}: paper missing from UI data")
            else:
                expected = {r["id"] for r in self.data["results"] if r["paper_id"] == paper["id"]}
                actual = {r["id"] for r in ui_papers[paper["id"]]["results"]}
                if expected != actual:
                    errors.append(f"{paper['id']}: UI/package selected result IDs differ")
        for source in self.data["sources"]:
            version = self.nodes.get(source["version_id"], {})
            if source["paper_id"] != version.get("paper_id") or source["id"] not in version.get("source_ids", []):
                errors.append(f"{source['id']}: source/version/paper mismatch")
            if source["visibility"] == "public" and source["publication_status"] != "published":
                errors.append(f"{source['id']}: public demo requires a published source")
            try:
                path = self.file(source["local_path"])
                if not path.is_file() or digest(path) != source["sha256"]:
                    errors.append(f"{source['id']}: formal PDF missing or changed")
            except PackageError as error:
                errors.append(f"{source['id']}: {error}")
        for occurrence in self.data["occurrences"]:
            source = self.nodes.get(occurrence["source_id"], {})
            if occurrence["version_id"] != source.get("version_id") or occurrence["paper_id"] != source.get("paper_id"):
                errors.append(f"{occurrence['id']}: occurrence/source/version mismatch")
            if occurrence["excerpt_id"] not in excerpt_ids:
                errors.append(f"{occurrence['id']}: missing source excerpt")
            if any(p < 1 or p > source.get("total_pages", 0) for p in occurrence["pdf_pages"]):
                errors.append(f"{occurrence['id']}: invalid one-based PDF page")
        for proof in self.data["shared_proofs"]:
            if proof["id"] not in self.math_proofs:
                errors.append(f"{proof['id']}: readable shared proof missing")
            else:
                text = self.math_proofs[proof["id"]]
                if text.get("rewrite_status") != "complete" or not text.get("proof_steps"):
                    errors.append(f"{proof['id']}: shared proof is incomplete")
        for collection in ["issues", "alignment_notes"]:
            for record in self.data[collection]:
                try:
                    source_records = read_json(self.file(record["path"]))[collection]
                    source_record = next((r for r in source_records if r["id"] == record["id"]), None)
                    if source_record is None or record["classification"] != source_record["classification"]:
                        errors.append(f"{record['id']}: review record missing or misclassified")
                    if collection == "alignment_notes" and record["is_mathematical_error"] is not False:
                        errors.append(f"{record['id']}: notation note cannot be silently recast as an error")
                except (OSError, PackageError, KeyError, ValueError):
                    errors.append(f"{record['id']}: review record unavailable")
        for result in self.data["results"]:
            if result["id"] not in self.math_results:
                errors.append(f"{result['id']}: mathematics record missing")
            math_record = self.math_results.get(result["id"], {})
            if math_record.get("paper_id") != result["paper_id"]:
                errors.append(f"{result['id']}: mathematical paper identity mismatch")
            if result["rewrite_status"] != math_record.get("rewrite_status"):
                errors.append(f"{result['id']}: mathematical rewrite status differs")
            if result["alignment_status"] != math_record.get("alignment_status"):
                errors.append(f"{result['id']}: mathematical alignment status differs")
            if set(result["proof_ids"]) != set(math_record.get("shared_proof_ids", [])):
                errors.append(f"{result['id']}: shared proof IDs differ")
            if result["rewrite_status"] == "complete" and not math_record.get("proof_steps"):
                errors.append(f"{result['id']}: completed readable proof has no steps")
            if result["kind"] == "theorem_component":
                parents = [edge["to_id"] for edge in self.data["edges"] if edge["from_id"] == result["id"] and edge["type"] == "component_of"]
                if not parents or result["completion_scope"] != "selected_subresult":
                    errors.append(f"{result['id']}: component parent or completion scope missing")
            if result["alignment_status"] == "pending_alignment" and result["verification_report_ids"]:
                errors.append(f"{result['id']}: pending source theorem cannot claim adapter verification")
            for adapter_id in result["adapter_ids"]:
                adapter = self.nodes.get(adapter_id, {})
                if adapter.get("result_id") != result["id"] or adapter.get("paper_id") != result["paper_id"]:
                    errors.append(f"{result['id']}: adapter scope mismatch")
                if set(adapter.get("lean_declarations", [])) != set(math_record.get("lean", {}).get("declarations", [])):
                    errors.append(f"{result['id']}: adapter declarations differ from mathematics record")
            for source_ref in self.math_results.get(result["id"], {}).get("source_refs", []):
                path = source_ref.get("local_path", source_ref.get("path", source_ref.get("local_pdf")))
                sha = source_ref.get("sha256")
                if path and not any(s["paper_id"] == result["paper_id"] and s["local_path"] == path and
                                    (not sha or s["sha256"] == sha) for s in self.data["sources"]):
                    errors.append(f"{result['id']}: mathematical source reference is not pinned to its formal paper")
                source = self.nodes.get(source_ref.get("source_id", source_ref.get("id")), {})
                if source_ref.get("version_id") != source.get("version_id"):
                    errors.append(f"{result['id']}: mathematical source version differs")
                if any(page < 1 or page > source.get("total_pages", 0) for page in source_ref.get("pages", [])):
                    errors.append(f"{result['id']}: mathematical source page out of range")
        edges = set()
        edge_ids = set()
        for edge in self.data["edges"]:
            key = (edge["from_id"], edge["to_id"], edge["type"])
            if key in edges or edge["id"] in edge_ids:
                errors.append(f"{edge['id']}: duplicate relation")
            edges.add(key); edge_ids.add(edge["id"])
            if edge["from_id"] not in self.nodes or edge["to_id"] not in self.nodes:
                errors.append(f"{edge['id']}: relation endpoint missing")
            if edge["visibility"] == "public" and not {edge["from_id"], edge["to_id"]}.issubset(self.visible_ids()):
                errors.append(f"{edge['id']}: public relation leaks private endpoint")
        evidence = [self.report_evidence(r["id"]) for r in self.data["verification_reports"]]
        for tool in self.data["tools"]:
            errors.extend(unsupported_schema_keywords(tool["input_schema"], f"tool.{tool['name']}"))
            if tool["input_schema"].get("additionalProperties") is not False:
                errors.append(f"{tool['name']}: tool parameters must be closed")
        for record in evidence:
            if record["freshness"] == "stale":
                warnings.append(f"{record['id']}: stale build evidence")
            if record["compilation"] != "passed" or record["axiom_audit"] != "passed":
                warnings.append(f"{record['id']}: build or axiom evidence not passed/current")
        return {"status": "passed" if not errors else "failed", "errors": errors, "warnings": warnings,
                "counts": {key: len(self.data[key]) for key in COLLECTIONS},
                "verification_reports": evidence, "scope": "package integrity, selected records only"}

    def invoke(self, tool_name: str, arguments: dict) -> dict:
        spec = next((t for t in self.data["tools"] if t["name"] == tool_name), None)
        if spec is None:
            raise PackageError("unknown tool name")
        errors = structural_errors(arguments, spec["input_schema"])
        if errors:
            raise PackageError("; ".join(errors))
        funcs = {"query": self.query, "get-result": self.get_result, "dependencies": self.dependencies,
                 "verification-status": self.verification_status, "list-resources": self.resources,
                 "get-resource": self.get_resource}
        return funcs[tool_name](**arguments)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    query = sub.add_parser("query")
    query.add_argument("--text", default="")
    query.add_argument("--paper", dest="paper_id")
    query.add_argument("--kind", choices=["theorem", "theorem_component"])
    for name in ["get-result", "dependencies", "get-resource"]:
        cmd = sub.add_parser(name); cmd.add_argument("identity")
        if name == "dependencies":
            cmd.add_argument("--depth", type=int, choices=range(1, 6), default=2)
    status = sub.add_parser("verification-status"); status.add_argument("identity", nargs="?")
    sub.add_parser("list-resources")
    sub.add_parser("validate")
    invoke = sub.add_parser("invoke"); invoke.add_argument("tool_name"); invoke.add_argument("arguments_json")
    args = vars(parser.parse_args(argv)); command = args.pop("command")
    try:
        package = PaperPackage()
        if command == "validate":
            output = package.validate()
        elif command == "invoke":
            output = package.invoke(args["tool_name"], json.loads(args["arguments_json"]))
        else:
            output = package.invoke(command, args)
        print(json.dumps(output, ensure_ascii=False, indent=2))
        return 0 if output.get("status") != "failed" else 1
    except (PackageError, OSError, json.JSONDecodeError, KeyError) as error:
        print(json.dumps({"error": str(error)}, ensure_ascii=False), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
