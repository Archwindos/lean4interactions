#!/usr/bin/env python3
"""Build only this research demo's manifest/schema from the approved three-paper inputs."""
import json
from pathlib import Path

from paper_agent import BASE, PROJECT_ROOT, digest


DEMO = "research/reader-v2-20260930"
MATH = f"{DEMO}/data/math-content.json"
REPORT = f"{DEMO}/math/verification/report.json"
ADAPTER = f"{DEMO}/math/lean/ReaderAdapters.lean"
ISSUES = f"{DEMO}/math/issues.json"
PAPER_IDS = {"cvpr2023-sparse-concepts", "iclr2024-sparse", "iclr2024-generalizable"}
PUBLIC = {"visibility": "public"}


def dump(path, obj):
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def tool(name, description, props, required=()):
    return {"name": name, "description": description, "implementation": "paper_agent.py:PaperPackage.invoke",
            "transport": "local_json_cli", "read_only": True,
            "input_schema": {"type": "object", "required": list(required), "properties": props,
                             "additionalProperties": False}}


def build_manifest():
    papers = json.loads((PROJECT_ROOT / DEMO / "data/papers.json").read_text())["papers"]
    if {p["id"] for p in papers} != PAPER_IDS:
        raise ValueError("Demo input must contain exactly the three authorized published papers")
    data = {"schema_version": "2.0", "package_id": "interaction-reader-v2", "package_version": "0.2.0-demo",
            "scope": "three published papers; selected results only; no full-paper completeness denominator",
            "implementation": {"transport": "local_json_cli", "mcp_server_implemented": False,
                               "production_migration_implemented": False},
            "data_files": {"papers_path": f"{DEMO}/data/papers.json", "math_path": MATH,
                           "source_excerpts_path": f"{DEMO}/data/source-excerpts/metadata.json"},
            **{k: [] for k in ["papers", "versions", "sources", "occurrences", "propositions", "shared_proofs",
                              "results", "adapters", "verification_reports", "issues", "alignment_notes", "resources", "prompts", "edges"]}}
    for paper in papers:
        data["papers"].append({"id": paper["id"], "version_ids": [paper["version_id"]],
                               "publication_status": "published", **PUBLIC})
        data["versions"].append({"id": paper["version_id"], "paper_id": paper["id"],
                                 "label": paper["version_label"], "publication_status": "published",
                                 "source_ids": [s["id"] for s in paper["sources"]], **PUBLIC})
        for source in paper["sources"]:
            source = dict(source, paper_id=paper["id"], provenance_type="official_venue_pdf")
            data["sources"].append(source)
            data["resources"].append({"id": f"res-{source['id']}", "kind": "formal_pdf",
                                      "content_format":"formal_pdf_original",
                                      "path": source["local_path"], "sha256": source["sha256"],
                                      "mime_type": "application/pdf", "source_ids": [source["id"]],
                                      "version_ids": [source["version_id"]], **PUBLIC})
    reconstruction = "prop-set-function-reconstruction"
    uniqueness = "prop-set-function-uniqueness"
    proof_rec = "proof-finite-mobius-reconstruction-v2"
    proof_unique = "proof-finite-mobius-uniqueness-v2"
    data["propositions"] = [
        {"id": reconstruction, "title": "有限集合函数的 Möbius 重构",
         "statement_tex": r"I_g(S)=\sum_{T\subseteq S}(-1)^{|S|-|T|}g(T),\qquad\sum_{T\subseteq S}I_g(T)=g(S)",
         "assumptions": ["finite input subsets", "real-valued set function g; no g(empty)=0 assumption"],
         "proof_ids": [proof_rec], "origin": "project_general_theorem", **PUBLIC},
        {"id": uniqueness, "title": "全部子集上重构系数的唯一性",
         "statement_tex": r"[\forall S\subseteq N,\ \sum_{T\subseteq S}d(T)=g(S)]\Longrightarrow[\forall S\subseteq N,\ d(S)=I_g(S)]",
         "assumptions": ["fixed finite universe N", "reconstruction equality for every subset of N"],
         "proof_ids": [proof_unique], "origin": "project_general_theorem", **PUBLIC}]
    data["shared_proofs"] = [
        {"id": proof_rec, "proposition_ids": [reconstruction], "content_path": MATH,
         "dependency_ids": [], "verification_report_ids": ["verification-library-reconstruction-v2"],
         "lean_declarations": ["Harsanyi.reconstruction","Harsanyi.interaction_insert"], "origin": "project_new_readable_proof", **PUBLIC},
        {"id": proof_unique, "proposition_ids": [uniqueness], "content_path": MATH,
         "dependency_ids": [reconstruction], "verification_report_ids": ["verification-library-uniqueness-v2"],
         "lean_declarations": ["Harsanyi.reconstruction_unique","Harsanyi.interaction_reconstruct"], "origin": "project_new_readable_proof", **PUBLIC}]
    occurrences = [
        ("occ-cvpr2023-theorem1-main", "cvpr2023-sparse-concepts", "src-cvpr2023-main", [3], "Theorem 1", "main_statement", "excerpt-cvpr2023-theorem1"),
        ("occ-cvpr2023-theorem1-supplement", "cvpr2023-sparse-concepts", "src-cvpr2023-supplement", [2,3], "Appendix C, Theorem 1", "restatement_with_proof", "excerpt-cvpr2023-theorem1"),
        ("occ-iclr2024-sparse-theorem1-main", "iclr2024-sparse", "src-iclr2024-sparse-main", [3,4], "Eq(1), Theorem 1", "main_statement", "excerpt-iclr2024-sparse-theorem1"),
        ("occ-iclr2024-sparse-theorem1-appendix", "iclr2024-sparse", "src-iclr2024-sparse-main", [15], "Appendix B.1, Eq(7)", "restatement_with_proof", "excerpt-iclr2024-sparse-theorem1"),
        ("occ-iclr2024-generalizable-theorem2-main", "iclr2024-generalizable", "src-iclr2024-generalizable-main", [2,3], "Eqs(1)--(3), Theorem 2", "main_statement", "excerpt-iclr2024-generalizable-theorem2"),
        ("occ-iclr2024-generalizable-theorem2-appendix", "iclr2024-generalizable", "src-iclr2024-generalizable-main", [12,13,14], "Appendix C, Eqs(7)--(9)", "restatement_with_proof", "excerpt-iclr2024-generalizable-theorem2"),
        ("occ-iclr2024-generalizable-and-component", "iclr2024-generalizable", "src-iclr2024-generalizable-main", [12,13], "Appendix C(1), fixed-x AND clause", "proof_component", "excerpt-iclr2024-generalizable-and-component")]
    sources = {s["id"]: s for s in data["sources"]}
    for identity, paper, source, pages, label, role, excerpt in occurrences:
        data["occurrences"].append({"id": identity, "paper_id": paper, "source_id": source,
                                    "version_id": sources[source]["version_id"], "pdf_pages": pages,
                                    "original_label": label, "role": role, "excerpt_id": excerpt,
                                    "source_review_status": "agent_checked_against_pinned_pdf",
                                    "user_review_status": "pending", **PUBLIC})
    specs = [
        ("cvpr2023-reconstruction", "cvpr2023-sparse-concepts", "全部因果模式的精确重构", "theorem", reconstruction, proof_rec,
         "ReaderV2.cvpr_reconstruction", ["occ-cvpr2023-theorem1-main","occ-cvpr2023-theorem1-supplement"],
         "CVPR 2023 Theorem 1 reconstruction clause; all subsets of Fin n", "g(S)=v(mask(S)); uncentered I(empty)=v(mask(empty))"),
        ("cvpr2023-uniqueness", "cvpr2023-sparse-concepts", "忠实系数唯一性", "theorem", uniqueness, proof_unique,
         "ReaderV2.cvpr_unique_coefficients", ["occ-cvpr2023-theorem1-main","occ-cvpr2023-theorem1-supplement"],
         "CVPR 2023 Theorem 1 uniqueness clause; all subsets of one finite universe", "g(S)=v(mask(S)); faithful d on every subset"),
        ("iclr2024-sparse-reconstruction", "iclr2024-sparse", "中心化交互的精确重构", "theorem", reconstruction, proof_rec,
         "ReaderV2.sparse_centered_reconstruction", ["occ-iclr2024-sparse-theorem1-main","occ-iclr2024-sparse-theorem1-appendix"],
         "ICLR 2024 Sparse Theorem 1 only; excludes sparsity Theorems 2--3", "instantiate g with centered maskedGame; I(empty)=0; add v(mask(empty)) once"),
        ("iclr2024-generalizable-and", "iclr2024-generalizable", "Appendix C(1) AND 精确重构子结论", "theorem_component", reconstruction, proof_rec,
         "ReaderV2.generalizable_and_subresult", ["occ-iclr2024-generalizable-and-component"],
         "ICLR 2024 Generalizable Appendix C(1) fixed-x AND sub-conclusion only", "g(S)=vAnd(mask(S)); uncentered Iand(empty)=vAnd(mask(empty))")]
    for rid,pid,title,kind,proposition,proof,declaration,occs,scope,definition_map in specs:
        aid = f"adapter-{rid}-v2"; vid = f"verification-{rid}-v2"
        declarations = [declaration] + (["ReaderV2.sparse_empty"] if rid == "iclr2024-sparse-reconstruction" else [])
        data["results"].append({"id":rid,"paper_id":pid,"title":title,"kind":kind,
                                "proposition_ids":[proposition],"proof_ids":[proof],"adapter_ids":[aid],
                                "occurrence_ids":occs,"issue_ids":[],"alignment_note_ids":[],"verification_report_ids":[vid],
                                "scope":scope,"completion_scope":"selected_subresult" if kind == "theorem_component" else "selected_result",
                                "alignment_status":"agent_checked_selected_statement","rewrite_status":"complete",
                                "user_review_status":"pending", **PUBLIC})
        data["adapters"].append({"id":aid,"paper_id":pid,"result_id":rid,"proposition_ids":[proposition],
                                 "proof_ids":[proof],"source_occurrence_ids":occs,"source_path":ADAPTER,
                                 "lean_declarations":declarations,"definition_map":definition_map,
                                 "alignment_status":"agent_checked_selected_statement","user_review_status":"pending",
                                 "verification_report_ids":[vid],"scope":scope,
                                 "concrete_mask_implementation_verified":False, **PUBLIC})
        data["verification_reports"].append({"id":vid,"path":REPORT,"build_id":"reader-v2-public-20260930",
                                             "scope":"paper_adapter","scope_description":scope,
                                             "subject_ids":[rid,aid],"expected_declarations":declarations,**PUBLIC})
    full = "iclr2024-generalizable-andor"
    issue_ids = ["issue-f11-or-intermediate-20260930"]
    note_id = "issue-f11-mask-notation-20260930"
    data["results"].append({"id":full,"paper_id":"iclr2024-generalizable","title":"Theorem 2 AND/OR 联合匹配（待对齐）",
                            "kind":"theorem","proposition_ids":[],"proof_ids":[],"adapter_ids":[],
                            "occurrence_ids":["occ-iclr2024-generalizable-theorem2-main","occ-iclr2024-generalizable-theorem2-appendix"],
                            "issue_ids":issue_ids,"alignment_note_ids":[note_id],"verification_report_ids":[],"scope":"full original Theorem 2; original notation/proof preserved",
                            "completion_scope":"full_original_theorem",
                            "alignment_status":"pending_alignment","rewrite_status":"not_started",
                            "user_review_status":"pending",**PUBLIC})
    for identity, declaration, subject in [("verification-library-reconstruction-v2","Harsanyi.reconstruction",proof_rec),
                                           ("verification-library-uniqueness-v2","Harsanyi.reconstruction_unique",proof_unique)]:
        data["verification_reports"].append({"id":identity,"path":REPORT,"build_id":"reader-v2-public-20260930",
                                             "scope":"general_library","scope_description":"public library declaration only; no paper semantics claim",
                                             "subject_ids":[subject],"expected_declarations":[declaration]+[
                                                 "Harsanyi.interaction_insert" if subject == proof_rec else "Harsanyi.interaction_reconstruct"],**PUBLIC})
    for identity, summary in zip(issue_ids,["Appendix C(2) cases (3)--(4): intermediate binomial cancellation needs review"]):
        data["issues"].append({"id":identity,"path":ISSUES,"paper_id":"iclr2024-generalizable",
                               "result_ids":[full],"source_occurrence_ids":["occ-iclr2024-generalizable-theorem2-appendix"],
                               "classification":"source_proof_step_issue",
                               "summary":summary,"status":"awaiting_user_confirmation",
                               "user_confirmation":"pending","fix_authorization":"pending",**PUBLIC})
    data["alignment_notes"].append({"id":note_id,"path":ISSUES,"paper_id":"iclr2024-generalizable",
                                    "result_ids":[full],"source_occurrence_ids":["occ-iclr2024-generalizable-theorem2-main",
                                                                               "occ-iclr2024-generalizable-theorem2-appendix"],
                                    "classification":"notation_alignment_note","is_mathematical_error":False,
                                    "summary":"full Theorem 2 x_T and fixed-x convention require semantic alignment",
                                    "status":"pending_alignment","user_review_status":"pending",
                                    "fix_authorization":"not_requested",**PUBLIC})
    def edge(a,b,typ,review="agent_reviewed",evidence="explicit data association"):
        data["edges"].append({"id":f"edge-{len(data['edges'])+1:03d}","from_id":a,"to_id":b,"type":typ,
                              "review_status":review,"evidence":evidence,**PUBLIC})
    for occurrence in data["occurrences"]:
        edge(occurrence["id"],occurrence["source_id"],"located_in","agent_source_checked")
    for result in data["results"]:
        for key,typ in [("occurrence_ids","appears_in"),("proposition_ids","instantiates"),
                        ("proof_ids","uses_shared_proof"),("adapter_ids","implemented_by"),
                        ("verification_report_ids","has_build_evidence"),("issue_ids","raises_issue"),
                        ("alignment_note_ids","needs_alignment")]:
            for target in result[key]:
                edge(result["id"],target,typ,result["alignment_status"],result["scope"])
    for proof in data["shared_proofs"]:
        for proposition in proof["proposition_ids"]: edge(proposition,proof["id"],"proved_by")
        for dep in proof["dependency_ids"]: edge(proof["id"],dep,"depends_on")
        for report in proof["verification_report_ids"]: edge(proof["id"],report,"has_build_evidence")
    edge("occ-cvpr2023-theorem1-supplement","occ-cvpr2023-theorem1-main","repeats_statement","agent_source_checked")
    edge("occ-iclr2024-sparse-theorem1-appendix","occ-iclr2024-sparse-theorem1-main","repeats_statement","agent_source_checked")
    edge("occ-iclr2024-generalizable-theorem2-appendix","occ-iclr2024-generalizable-theorem2-main","repeats_statement","agent_source_checked")
    edge("iclr2024-sparse-reconstruction","cvpr2023-reconstruction","cites_prior_result","agent_source_checked","F03 PDF p4 and bibliography p11; centered definition retained through adapter")
    edge("iclr2024-generalizable-and",full,"component_of","agent_reviewed","Appendix C(1) only; component verification does not verify its parent")
    edge(full,"iclr2024-generalizable-and","has_component","agent_source_checked","selected AND component, original full theorem remains pending")
    def resource(identity,kind,path,mime="text/plain",**extra):
        formats={"readable_proof":"project_readable_proof","structured_result":"structured_math_and_explanation",
                 "checked_excerpt":"agent_math_transcription","verification_report":"build_report",
                 "lean_source":"lean_source","local_tool_source":"tool_source","data_schema":"schema",
                 "issue_evidence":"issue_evidence","workflow":"workflow"}
        data["resources"].append({"id":identity,"kind":kind,"path":path,"mime_type":mime,
                                  "content_format":formats[kind],**extra,**PUBLIC})
    for proof in data["shared_proofs"]:
        resource(f"res-{proof['id']}","readable_proof",MATH,"application/json",
                 record_collection="shared_proofs",record_id=proof["id"])
    for result in data["results"]:
        resource(f"res-{result['id']}","structured_result",MATH,"application/json",
                 record_collection="results",record_id=result["id"],derived_from_ids=[result["id"]])
    for name,source in [("cvpr2023-theorem1","src-cvpr2023-main"),
                        ("iclr2024-sparse-reconstruction","src-iclr2024-sparse-main"),
                        ("iclr2024-generalizable-andor","src-iclr2024-generalizable-main")]:
        resource(f"res-excerpt-{name}","checked_excerpt",f"{DEMO}/data/source-excerpts/{name}.tex",
                 source_ids=[source])
    resource("res-public-build-report","verification_report",REPORT,"application/json")
    resource("res-reader-adapters","lean_source",ADAPTER)
    resource("res-read-only-cli","local_tool_source",f"{DEMO}/architecture/paper_agent.py")
    resource("res-package-schema","data_schema",f"{DEMO}/architecture/package.schema.json","application/json")
    resource("res-f11-issues","issue_evidence",ISSUES,"application/json",source_ids=["src-iclr2024-generalizable-main"])
    for identity,path,title in [("prompt-read-result","docs/paper-agent-data-model.md","Read a result and its exact evidence scope"),
                                ("prompt-add-paper","docs/agent-extension-workflow.md","Add a published paper through source/alignment/proof/review steps")]:
        data["prompts"].append({"id":identity,"path":path,"title":title,"kind":"human_ai_workflow",**PUBLIC})
        resource(f"res-{identity}","workflow",path,"text/markdown")
    identity_schema = {"type":"string","pattern":"^[a-z][a-z0-9-]*$","maxLength":120}
    data["tools"] = [
        tool("query","Search selected result records; appearances never count as separate completed results",
             {"text":{"type":"string","maxLength":500},"paper_id":{"type":["string","null"]},
              "kind":{"type":["string","null"],"enum":["theorem","theorem_component",None]}}),
        tool("get-result","Get one result, shared proof, exact source occurrences, adapter, issues and scoped status",
             {"identity":identity_schema},["identity"]),
        tool("dependencies","Follow explicit outgoing relations, preserving edge type and review status",
             {"identity":identity_schema,"depth":{"type":"integer","minimum":1,"maximum":5}},["identity"]),
        tool("verification-status","Check current hashes, exact declarations, audit and independent source alignment",
             {"identity":{"type":["string","null"]}}),
        tool("list-resources","List registered public resources only",{}),
        tool("get-resource","Read a registered public resource ID; no arbitrary path, code execution or network",
             {"identity":identity_schema},["identity"])]
    for resource_node in data["resources"]:
        path = PROJECT_ROOT / resource_node["path"]
        if path.is_file(): resource_node["sha256"] = digest(path)
    return data


def build_schema():
    text = {"type":"string"}; texts = {"type":"array","items":text,"uniqueItems":True}
    identity = {"type":"string","pattern":"^[a-z][a-z0-9-]*$","maxLength":120}
    ids = {"type":"array","items":identity,"uniqueItems":True}
    common = {"id":identity,"visibility":{"type":"string","enum":["public","private"]}}
    user = {"type":"string","enum":["not_recorded","pending","accepted","rejected"]}
    align = {"type":"string","enum":["agent_checked_selected_statement","pending_alignment","not_applicable","candidate"]}
    path = {"type":"string","minLength":1}; sha = {"type":"string","pattern":"^[0-9a-f]{64}$"}
    defs = {}
    def node(name,props,required=None):
        defs[name]={"type":"object","required":["id","visibility"]+list(props if required is None else required),
                    "properties":{**common,**props},"additionalProperties":False}
    node("paper",{"version_ids":ids,"publication_status":text})
    node("version",{"paper_id":identity,"label":text,"publication_status":text,"source_ids":ids})
    node("source",{"paper_id":identity,"label":text,"kind":{"type":"string","enum":["main","supplement"]},
                    "local_path":path,"url":text,"sha256":sha,"total_pages":{"type":"integer","minimum":1},
                    "version_id":identity,"publication_status":text,"page_refs":{"type":"array","items":{"type":"integer","minimum":1}},
                    "provenance_type":{"type":"string","enum":["official_venue_pdf"]}})
    node("occurrence",{"paper_id":identity,"version_id":identity,"source_id":identity,
                        "pdf_pages":{"type":"array","minItems":1,"items":{"type":"integer","minimum":1}},
                        "original_label":text,"role":{"type":"string","enum":["main_statement","restatement_with_proof","proof_component"]},
                        "excerpt_id":identity,"source_review_status":text,"user_review_status":user})
    node("proposition",{"title":text,"statement_tex":text,"assumptions":texts,"proof_ids":ids,"origin":text})
    node("proof",{"proposition_ids":ids,"content_path":path,"dependency_ids":ids,"verification_report_ids":ids,
                   "lean_declarations":texts,"origin":text})
    node("result",{"paper_id":identity,"title":text,"kind":{"type":"string","enum":["theorem","theorem_component"]},
                    **{k:ids for k in ["proposition_ids","proof_ids","adapter_ids","occurrence_ids","issue_ids","alignment_note_ids","verification_report_ids"]},
                    "scope":text,"completion_scope":{"type":"string","enum":["selected_result","selected_subresult","full_original_theorem"]},
                    "alignment_status":align,"rewrite_status":{"type":"string","enum":["complete","not_started","in_progress"]},
                    "user_review_status":user})
    node("adapter",{"paper_id":identity,"result_id":identity,"proposition_ids":ids,"proof_ids":ids,"source_occurrence_ids":ids,
                     "source_path":path,"lean_declarations":texts,"definition_map":text,"alignment_status":align,
                     "user_review_status":user,"verification_report_ids":ids,"scope":text,
                     "concrete_mask_implementation_verified":{"type":"boolean"}})
    node("report",{"path":path,"build_id":text,"scope":{"type":"string","enum":["general_library","paper_adapter"]},
                    "scope_description":text,"subject_ids":ids,"expected_declarations":{"type":"array","minItems":1,"items":text}})
    node("issue",{"path":path,"paper_id":identity,"result_ids":ids,"source_occurrence_ids":ids,"summary":text,
                   "classification":{"type":"string","const":"source_proof_step_issue"},
                   "status":{"type":"string","enum":["awaiting_user_confirmation","awaiting_fix_authorization","resolved","rejected"]},
                   "user_confirmation":{"type":"string","enum":["pending","confirmed","rejected"]},
                   "fix_authorization":{"type":"string","enum":["pending","authorized","not_authorized"]}})
    node("alignment_note",{"path":path,"paper_id":identity,"result_ids":ids,"source_occurrence_ids":ids,"summary":text,
                            "classification":{"type":"string","const":"notation_alignment_note"},
                            "is_mathematical_error":{"type":"boolean","const":False},
                            "status":{"type":"string","const":"pending_alignment"},"user_review_status":user,
                            "fix_authorization":{"type":"string","const":"not_requested"}})
    node("resource",{"kind":text,"path":path,"mime_type":text,
                      "content_format":{"type":"string","enum":["formal_pdf_original","pdf_text_extract","agent_math_transcription",
                         "structured_math_and_explanation","project_readable_proof","build_report","lean_source","tool_source",
                         "schema","issue_evidence","workflow"]},"sha256":sha,"source_ids":ids,"version_ids":ids,
                      "record_collection":{"type":"string","enum":["shared_proofs","results"]},"record_id":identity,"derived_from_ids":ids},
         ["kind","path","mime_type","content_format"])
    node("prompt",{"path":path,"title":text,"kind":{"type":"string","const":"human_ai_workflow"}})
    edge_props={"from_id":identity,"to_id":identity,"type":{"type":"string","enum":["located_in","appears_in","instantiates",
                "uses_shared_proof","implemented_by","has_build_evidence","raises_issue","proved_by","depends_on",
                "repeats_statement","cites_prior_result","component_of","has_component","needs_alignment"]},"review_status":text,"evidence":text}
    node("edge",edge_props)
    node("tool",{"name":text,"description":text,"implementation":text,"transport":{"type":"string","const":"local_json_cli"},
                  "read_only":{"type":"boolean","const":True},"input_schema":{"type":"object","additionalProperties":True}},
         ["name","description","implementation","transport","read_only","input_schema"])
    # Tool IDs/visibility are not needed; the fixed manifest names are the callable registry.
    defs["tool"]["required"]=[x for x in defs["tool"]["required"] if x not in ["id","visibility"]]
    props={"schema_version":{"type":"string","const":"2.0"},"package_id":identity,"package_version":text,"scope":text,
           "implementation":{"type":"object","required":["transport","mcp_server_implemented","production_migration_implemented"],
             "properties":{"transport":{"type":"string","const":"local_json_cli"},"mcp_server_implemented":{"type":"boolean","const":False},
                           "production_migration_implemented":{"type":"boolean","const":False}},"additionalProperties":False},
           "data_files":{"type":"object","required":["papers_path","math_path","source_excerpts_path"],
                         "properties":{k:path for k in ["papers_path","math_path","source_excerpts_path"]},"additionalProperties":False}}
    names={"papers":"paper","versions":"version","sources":"source","occurrences":"occurrence","propositions":"proposition",
           "shared_proofs":"proof","results":"result","adapters":"adapter","verification_reports":"report","issues":"issue",
           "alignment_notes":"alignment_note","resources":"resource","prompts":"prompt","edges":"edge","tools":"tool"}
    props.update({k:{"type":"array","items":{"$ref":f"#/$defs/{v}"}} for k,v in names.items()})
    return {"$schema":"https://json-schema.org/draft/2020-12/schema","$id":"urn:interaction-reader-v2:package:2.0",
            "title":"Selected-paper agent package v2; use structural and semantic validation together",
            "type":"object","required":list(props),"properties":props,"additionalProperties":False,"$defs":defs}


if __name__ == "__main__":
    dump(BASE / "package.schema.json", build_schema())
    package=build_manifest()
    dump(BASE / "agent-package.json", package)
    print(f"Built schema and package: {len(package['papers'])} papers, {len(package['results'])} selected result records")
