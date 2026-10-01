"""Integrity tests use synthetic private records; no user manuscript is read."""
import copy
import json
from pathlib import Path
import tempfile
import unittest

from paper_agent import PaperPackage, PackageError, PROJECT_ROOT, digest, fingerprint, structural_errors


class PackageIntegrityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.package = PaperPackage()

    def test_actual_package_structure_and_semantics(self):
        result = self.package.validate()
        self.assertEqual(result["errors"], [])
        self.assertEqual(result["warnings"], [])
        self.assertEqual(result["counts"]["papers"], 3)
        self.assertEqual(result["status"], "passed")

    def test_three_papers_reuse_one_proof_through_distinct_adapters(self):
        ids = ["cvpr2023-reconstruction", "iclr2024-sparse-reconstruction", "iclr2024-generalizable-and"]
        data = [self.package.get_result(identity)["result"] for identity in ids]
        self.assertEqual({r["proof_ids"][0] for r in data}, {"proof-finite-mobius-reconstruction-v2"})
        self.assertEqual(len({r["adapter_ids"][0] for r in data}), 3)
        maps = [self.package.get(r["adapter_ids"][0])["definition_map"] for r in data]
        self.assertTrue(any("centered" in mapping for mapping in maps))
        self.assertTrue(any("vAnd" in mapping for mapping in maps))

    def test_component_pass_does_not_verify_pending_parent(self):
        component = self.package.verification_status("iclr2024-generalizable-and")
        parent = self.package.verification_status("iclr2024-generalizable-andor")
        self.assertEqual(component["compilation"], "passed")
        self.assertEqual(component["axiom_audit"], "passed")
        self.assertEqual(component["completion_scope"], "selected_subresult")
        self.assertEqual(parent["compilation"], "unavailable")
        self.assertEqual(parent["source_alignment"], "pending_alignment")
        self.assertEqual(parent["readable_rewrite"], "not_started")
        self.assertEqual(parent["user_review"], "pending")

    def test_notation_note_is_separate_from_mathematical_issue(self):
        result = self.package.get_result("iclr2024-generalizable-andor")
        self.assertEqual(len(result["issues"]), 1)
        self.assertEqual(len(result["alignment_notes"]), 1)
        self.assertEqual(result["issues"][0]["user_confirmation"], "pending")
        self.assertEqual(result["issues"][0]["fix_authorization"], "pending")
        self.assertFalse(result["alignment_notes"][0]["is_mathematical_error"])

    def test_query_excludes_duplicate_appearances_and_experimental_or(self):
        result = self.package.query()
        ids = [r["id"] for r in result["results"]]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertEqual(result["count"], 5)
        self.assertGreater(len(self.package.data["occurrences"]), result["count"])
        self.assertNotIn("library-or-reconstruction", ids)
        resources = json.dumps(self.package.resources(), ensure_ascii=False)
        self.assertNotIn("IndependentOR", resources)
        self.assertNotIn("experimental/", resources)
        self.assertEqual(self.package.query(text="Möbius")["count"], 3)

    def test_json_resource_returns_selected_proof_only(self):
        output = self.package.get_resource("res-proof-finite-mobius-reconstruction-v2")
        self.assertEqual(output["record"]["id"], "proof-finite-mobius-reconstruction-v2")
        self.assertNotIn("results", output["record"])
        self.assertNotIn("text", output)

    def test_private_derivatives_and_edges_do_not_leak(self):
        manifest = copy.deepcopy(self.package.data)
        secret = "private-fixture-secret"
        manifest["papers"].append({"id":secret,"version_ids":[],"publication_status":"unpublished","visibility":"private"})
        private_result = copy.deepcopy(manifest["results"][0])
        private_result.update(id=secret+"-result",paper_id=secret,title="synthetic private mathematical text",
                              adapter_ids=[],verification_report_ids=[],occurrence_ids=[],visibility="private")
        manifest["results"].append(private_result)
        # A mislabeled public derivative still inherits privacy from its source-paper reference.
        derivative = copy.deepcopy(private_result)
        derivative.update(id=secret+"-derivative",visibility="public")
        manifest["results"].append(derivative)
        manifest["resources"].append({"id":secret+"-resource","visibility":"public","path":"never-read-private-file",
                                       "kind":"synthetic","content_format":"structured_math_and_explanation",
                                       "mime_type":"text/plain","derived_from_ids":[private_result["id"]]})
        manifest["edges"].append({"id":"edge-synthetic-private","from_id":"proof-finite-mobius-reconstruction-v2",
                                   "to_id":private_result["id"],"type":"depends_on","review_status":"candidate",
                                   "evidence":"synthetic record only","visibility":"public"})
        package = PaperPackage(manifest=manifest, math_content=self.package.math)
        exported = json.dumps([package.query(),package.resources(),
                               package.dependencies("proof-finite-mobius-reconstruction-v2",5)], ensure_ascii=False)
        self.assertNotIn(secret, exported)
        self.assertNotIn("synthetic private mathematical text", exported)
        self.assertEqual(package.query()["count"],5)
        self.assertIn("proof-finite-mobius-reconstruction-v2",package.visible_ids())
        for identity in [private_result["id"],derivative["id"],secret+"-resource"]:
            with self.assertRaises(PackageError): package.get(identity)

    def test_closed_tool_parameters_and_depth_bounds(self):
        with self.assertRaises(PackageError):
            self.package.invoke("query",{"text":"","shell":"cat anything"})
        with self.assertRaises(PackageError):
            self.package.invoke("get-resource",{"identity":"../../anything"})
        with self.assertRaises(PackageError):
            self.package.invoke("dependencies",{"identity":"cvpr2023-reconstruction","depth":6})
        with self.assertRaises(PackageError):
            self.package.invoke("run-shell",{})

    def test_unsupported_schema_keyword_fails_explicitly(self):
        errors = structural_errors({}, {"type":"object","oneOf":[{"required":["id"]}]})
        self.assertTrue(any("unsupported schema keyword oneOf" in error for error in errors))

    def test_foreign_key_version_and_duplicate_edges_fail(self):
        manifest = copy.deepcopy(self.package.data)
        manifest["sources"][0]["version_id"]="nonexistent-version"
        manifest["edges"].append(copy.deepcopy(manifest["edges"][0]))
        package = PaperPackage(manifest=manifest,math_content=self.package.math)
        errors=package.validate()["errors"]
        self.assertTrue(any("dangling foreign key" in error for error in errors))
        self.assertTrue(any("source/version/paper mismatch" in error for error in errors))
        self.assertTrue(any("duplicate relation" in error for error in errors))

    def test_project_path_and_symlinks_rejected(self):
        with self.assertRaises(PackageError): self.package.file("../outside")
        with self.assertRaises(PackageError): self.package.file("/absolute/path")
        with tempfile.TemporaryDirectory(prefix="paper-agent-",dir=PROJECT_ROOT/".tmp") as name:
            directory=Path(name);target=directory/"target.txt";target.write_text("synthetic test")
            link=directory/"link.txt";link.symlink_to(target)
            with self.assertRaises(PackageError): self.package.file(link.relative_to(PROJECT_ROOT).as_posix())

    def test_report_freshness_missing_axioms_and_disallowed_axioms(self):
        with tempfile.TemporaryDirectory(prefix="paper-agent-report-",dir=PROJECT_ROOT/".tmp") as name:
            directory=Path(name);source=directory/"Fixture.lean";source.write_text("synthetic checker fixture")
            source_name=source.relative_to(PROJECT_ROOT).as_posix()
            files=[{"path":source_name,"sha256":digest(source)}]
            report={"status":"passed","source_files":files,"source_fingerprint":fingerprint(files),
                    "commands":[{"argv":["lean","Fixture.lean"],"exit_code":0},
                                {"argv":["lean","AuditFixture.lean"],"exit_code":0}],
                    "declarations":[{"name":"Fixture.synthetic","status":"passed","source_path":source_name,"axioms":[]}]}
            path=directory/"report.json";path.write_text(json.dumps(report))
            node={"id":"verification-synthetic","visibility":"private","path":path.relative_to(PROJECT_ROOT).as_posix(),
                  "scope":"general_library","expected_declarations":["Fixture.synthetic"]}
            package=PaperPackage(manifest={"verification_reports":[node]},math_content={})
            self.assertEqual(package.report_evidence(node["id"])["compilation"],"passed")
            source.write_text("changed synthetic checker fixture")
            self.assertEqual(package.report_evidence(node["id"])["freshness"],"stale")
            source.write_text("synthetic checker fixture")
            del report["declarations"][0]["axioms"];path.write_text(json.dumps(report))
            self.assertEqual(package.report_evidence(node["id"])["axiom_audit"],"unavailable")
            report["declarations"][0]["axioms"]=["sorryAx"];path.write_text(json.dumps(report))
            self.assertEqual(package.report_evidence(node["id"])["axiom_audit"],"failed")
            report["declarations"][0]["axioms"]=[]
            report["declarations"][0]["source_path"]="unregistered-source.lean";path.write_text(json.dumps(report))
            self.assertEqual(package.report_evidence(node["id"])["compilation"],"unavailable")
            report["declarations"][0]["source_path"]=source_name
            report["commands"][0]["exit_code"]=1;path.write_text(json.dumps(report))
            self.assertEqual(package.report_evidence(node["id"])["compilation"],"failed")
            report["commands"][0]["exit_code"]=0
            report["declarations"]=[];path.write_text(json.dumps(report))
            self.assertEqual(package.report_evidence(node["id"])["compilation"],"unavailable")


if __name__ == "__main__":
    unittest.main(verbosity=2)
