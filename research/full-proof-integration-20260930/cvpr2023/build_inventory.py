"""Source-bound full inventory. Run only from the project root after env.sh."""
from pathlib import Path
import hashlib
import json

ROOT = Path("research/full-proof-integration-20260930/cvpr2023")
SOURCE_ROOT = Path("research/paper-survey-20260930/earlier/venue-papers")
PAPER = "cvpr2023-sparse-concepts"
ROOT.mkdir(parents=True, exist_ok=True)

def source(kind, count):
    path = SOURCE_ROOT / f"sparse-cvpr2023-{kind}" / f"sparse-cvpr2023-{kind}.pdf"
    return {"source_id": source_id(kind), "path": str(path), "sha256": hashlib.sha256(path.read_bytes()).hexdigest(), "page_count": count, "version_id": "ver-cvpr2023-formal", "version": "CVPR 2023 official CVF open-access " + ("main paper" if kind == "main" else "supplementary material"), "page_numbering": "1-based PDF pages; independent for each source"}

def source_id(kind):
    return "src-cvpr2023-main" if kind == "main" else "src-cvpr2023-supplement"

def loc(kind, pages, section, detail=""):
    return {"source_id": source_id(kind), "version_id": "ver-cvpr2023-formal", "pdf_pages": pages, "section": section, "detail": detail}

entries = []
def entry(id, label, title, kind, statements, proofs=None, target=None, rationale="", issue_ids=None, external=None):
    entries.append({"id": id, "original_label": label, "title": title, "kind": kind, "statement_locations": statements, "proof_locations": proofs or [], "all_occurrences": statements + (proofs or []), "merge_target_id": target, "merge_rationale": rationale, "related_issue_ids": issue_ids or [], "external_citation": external, "review_status": "agent_reviewed", "user_review_status": "pending"})

entry("cvpr-inv-thm1", "Theorem 1; Appendix C Theorem 1", "全部掩码的重构与唯一性", "numbered_theorem", [loc("main", [3], "3.1", "Eq. (3), reconstruction only"), loc("supp", [2], "C", "Eq. (2), with uniqueness sentence")], [loc("supp", [3], "C", "entire Proof: necessity and sufficiency")], "cvpr2023-reconstruction", "两个独立子目标：重构 cvpr2023-reconstruction 与唯一性 cvpr2023-uniqueness。")
entry("cvpr-inv-thm1-uniqueness", "Appendix C sufficiency", "同一组系数在全部掩码上满足重构时唯一", "theorem_subresult", [loc("supp", [2], "C", "More crucially, ... unique metric")], [loc("supp", [3], "C", "Proof for sufficiency, base and induction step")], "cvpr2023-uniqueness")
entry("cvpr-inv-efficiency", "Axiom (1) Efficiency", "总输出等于全部交互之和", "axiom_property", [loc("main", [4], "3.1", "seven axioms list"), loc("supp", [2], "B", "(1)")], [loc("supp", [4], "D.1", "(1) full proof")], "cvpr2023-reconstruction", "固定 S=N 的重构实例；原文有独立重证，不再计一个独立数学目标。")
entry("cvpr-inv-linearity", "Axiom (2) Linearity", "模型输出逐点相加使交互逐项相加", "axiom_property", [loc("supp", [2], "B", "(2)")], [loc("supp", [4], "D.1", "(2) complete four-line proof")], "cvpr2023-linearity", issue_ids=["cvpr-issue-linearity-index"])
entry("cvpr-inv-dummy", "Axiom (3) Dummy", "Dummy 与其他变量的因果效应为零", "axiom_property", [loc("supp", [2], "B", "(3) includes empty S"), loc("supp", [4], "D.1", "(3) repeated statement")], [loc("supp", [4], "D.1", "(3) complete proof")], "cvpr2023-dummy", issue_ids=["cvpr-issue-dummy-empty"])
entry("cvpr-inv-symmetry", "Axiom (4) Symmetry", "相同合作方式导致相同交互", "axiom_property", [loc("supp", [2], "B", "(4)"), loc("supp", [4], "D.1", "(4)")], [loc("supp", [4,5], "D.1", "last two equations p4; remaining three p5")], "cvpr2023-symmetry")
entry("cvpr-inv-anonymity", "Axiom (5) Anonymity", "置换变量不改变交互", "axiom_property", [loc("supp", [2], "B", "(5)"), loc("supp", [5], "D.1", "(5)")], [loc("supp", [5], "D.1", "(5) complete three-line proof")], "cvpr2023-anonymity")
entry("cvpr-inv-recursive", "Axiom (6) Recursive", "插入变量的交互等于上下文差分", "axiom_property", [loc("supp", [2], "B", "(6)"), loc("supp", [5], "D.1", "(6)")], [loc("supp", [5], "D.1", "(6) complete four-line proof")], "cvpr2023-recursive")
entry("cvpr-inv-distribution", "Axiom (7) Interaction distribution", "纯 AND 函数只在指定集合有非零交互", "axiom_property", [loc("supp", [2], "B", "(7)"), loc("supp", [5], "D.1", "(7)")], [loc("supp", [5,6], "D.1", "three cases: proper subset, equality, proper superset")], "cvpr2023-interaction-distribution", issue_ids=["cvpr-issue-distribution-incomparable"])
entry("cvpr-inv-thm5", "Theorem 5", "环境中的边际差分由交互分解", "numbered_theorem", [loc("supp", [2], "B", "first listed theorem"), loc("supp", [6], "D.2", "Theorem 5")], [loc("supp", [6], "D.2", "entire 8-line proof and singleton specialization")], "cvpr2023-marginal-decomposition")
entry("cvpr-inv-thm2", "Theorem 2", "Shapley 值等分全部参与交互", "numbered_theorem", [loc("main", [4], "3.1", "Theorem 2, explicitly inherited from Harsanyi [15]"), loc("supp", [2], "B", "Theorem 2"), loc("supp", [6], "D.2", "Theorem 2")], [loc("supp", [6,7,8], "D.2", "begins at bottom p6; Beta calculation p7–8; ends immediately before Theorem 3 p8")], "cvpr2023-shapley", issue_ids=["cvpr-issue-beta-proof"], external={"main_reference": "[15] Harsanyi (1963)", "supplement_reference": "[43] Shapley (1953)", "proof_in_this_paper": True})
entry("cvpr-inv-thm3", "Theorem 3", "Shapley interaction 指数的交互等分形式", "numbered_theorem", [loc("supp", [2], "B", "Theorem 3"), loc("supp", [8], "D.2", "Theorem 3 with factorial-weight definition")], [loc("supp", [8,9], "D.2", "all equations before Theorem 4 p9")], "cvpr2023-shapley-interaction", issue_ids=["cvpr-issue-beta-proof"])
entry("cvpr-inv-thm4", "Theorem 4", "Shapley–Taylor 各阶的交互权重", "numbered_theorem", [loc("supp", [2], "B", "Theorem 4"), loc("supp", [9], "D.2", "Theorem 4 and defining three cases")], [loc("supp", [9,10,11], "D.2", "definition p9, low/top-order proof p10, coefficient simplification and final equation p11; high-order case follows definition")], "cvpr2023-shapley-taylor", issue_ids=["cvpr-issue-beta-proof"])
entry("cvpr-inv-scm", "Main Eq. (1), (2); unnumbered derivation", "二值 AND 触发把 SCM 输出化为子集求和", "unnumbered_derivation", [loc("main", [3,4], "3.1", "SCM, masked sample, and first paragraph p4")], [loc("main", [4], "3.1", "Y(x_S)=sum w_T C_T(x_S)=sum_{T⊆S,T∈Omega} w_T")], "cvpr2023-scm-subset-sum")
entry("cvpr-inv-baseline-invariance", "Main 3.2 unnumbered statement", "改变输入基线后完整交互始终零不忠实度", "unnumbered_derivation", [loc("main", [5], "3.2", "change of baseline values always ensures unfaith(w)=0")], [loc("main", [3,5], "3.1–3.2", "deduced from Theorem 1, no separate displayed proof")], "cvpr2023-baseline-faithfulness")
entry("cvpr-inv-aog", "Main 3.3 unnumbered derivation", "将重复子 AND 合并仍保持触发状态", "unnumbered_derivation", [loc("main", [5], "3.3", "equivalent transformation and C_S=product of child C")], [loc("main", [5], "3.3", "x4x5x6 -> x4 beta with beta={x5,x6}, and general child-product rule")], "cvpr2023-aog-regrouping")
entry("cvpr-inv-addmul", "Main 4.1; Supplement G.3 examples", "二值加乘模型的交互等于各项系数", "unnumbered_derivation", [loc("main", [7], "4.1", "y=x1x3+x3x4x5+x4x6"), loc("supp", [13,14], "G.3", "Addition-Multiplication and extended coefficient dataset")], [loc("main", [7], "4.1", "binary multiplication is AND"), loc("supp", [13,14], "G.3", "each term contributes iff all its variables are present; explicit coefficient examples")], "cvpr2023-addmul-coefficients", "复用线性性和纯 AND，但本条本身无独立编号或作者完整证明。", issue_ids=["cvpr-issue-distribution-incomparable"])
entry("cvpr-inv-harsanyi-definition", "Supplement Eq. (1); main Theorem 1 definition", "Harsanyi dividend 原定义", "definition", [loc("main", [3], "3.1"), loc("supp", [2], "B", "negative exponent convention printed; parity equivalent")])
entry("cvpr-inv-mask-definition", "Main Eq. (4); Supplement E", "固定输入与输入基线定义掩码", "definition", [loc("main", [3,4], "3.1"), loc("supp", [11], "E")])
entry("cvpr-inv-remark1", "Remark 1", "少量模式近似 DNN 的经验稀疏现象", "empirical_observation", [loc("main", [4], "3.2"), loc("main", [2,3,8], "2; Figure 2; 4.2")], target=None, rationale="原文使用≈和≪、无误差或规模定量假设，无数学证明；不能伪造稀疏性定理。")
entry("cvpr-inv-combinatorial-beta", "D.2 (i)–(iii), unnumbered ingredients", "二项系数恒等式与 Beta 性质", "external_unproved_ingredient", [loc("supp", [7], "D.2", "(i) m choose(n,m)=n choose(n-1,m-1); (ii) Beta definition; (iii) formulas")], rationale="作为Theorem2–4的证明材料整体纳入逐式转录；本篇未独立证明这些性质，不额外计目标。", issue_ids=["cvpr-issue-beta-proof"])
entry("cvpr-inv-optimization", "Main Eq. (5), (6)", "模式选择与L0→L1松弛", "algorithm_and_heuristic", [loc("main", [4,5], "3.2")], rationale="优化目标和启发式松弛，无数学最优化等价证明。", issue_ids=["cvpr-issue-l0-support", "cvpr-issue-lagrange-equivalence"])
entry("cvpr-inv-explained-ratio", "Main Eq. (7)", "已解释效应比例", "definition", [loc("main", [5], "3.2")], issue_ids=["cvpr-issue-ratio-zero-denominator"])
entry("cvpr-inv-mdl", "Main Eq. (8); Supplement Eq. (3)", "MDL目标与贪心规则", "algorithm_and_definition", [loc("main", [5,6], "3.3"), loc("supp", [12], "F")], rationale="没有全局最优性或复杂度证明；O(|Omega|²)为未证明算法复杂度声明。")
entry("cvpr-inv-evaluation", "Main 4.1–4.3; Supplement G.4–G.8 Eq. (4), (5)", "实验指标、相似性及结果", "definition_and_empirical_analysis", [loc("main", [6,7,8], "4"), loc("supp", [14,15,16], "G.4–G.8")])
entry("cvpr-inv-synthesized-labels", "Supplement G.3", "sigmoid与And-Or实验人工真值规则", "experimental_labeling_convention", [loc("supp", [13,14], "G.3")], rationale="阈值激活的人工标签，不声称等于全部Harsanyi系数；与Add-Mul精确系数分开。")
entry("cvpr-inv-runtime", "Main 3.3; Supplement H", "运行时间与维数降低", "unproved_complexity_and_empirical_runtime", [loc("main", [6], "3.3", "O(|Omega|²)"), loc("supp", [16,17], "H")])
entry("cvpr-inv-bow", "Supplement I; Table 6,7", "AOG与BoW的区别及共同词组", "discussion_and_empirical_example", [loc("supp", [17,18], "I")], rationale="同位置词组会形成相同系数的说明依赖相同掩码和基线；该段并非独立数学证明。")
entry("cvpr-inv-related-work", "Main 2; Supplement A", "相关文献的外引结论", "external_claim_without_proof", [loc("main", [2], "2"), loc("supp", [1], "A")], rationale="诸如DNN中阶交互瓶颈等只有文献引用，不是本篇证明，保留外引标识。")

MAIN = {
1: ("Abstract; 1 Introduction", "expository_and_empirical", []),
2: ("1 Introduction; 2 XAI theory; 3 Method", "related_work_and_overview", ["cvpr-inv-related-work", "cvpr-inv-remark1"]),
3: ("3.1 Causal graph", "definitions_and_numbered_theorem_statement", ["cvpr-inv-thm1", "cvpr-inv-scm", "cvpr-inv-mask-definition", "cvpr-inv-harsanyi-definition"]),
4: ("3.1–3.2", "theorem_property_statements_and_optimization", ["cvpr-inv-thm2", "cvpr-inv-efficiency", "cvpr-inv-remark1", "cvpr-inv-optimization", "cvpr-inv-scm"]),
5: ("3.2–3.3", "unnumbered_derivations_and_algorithms", ["cvpr-inv-baseline-invariance", "cvpr-inv-aog", "cvpr-inv-optimization", "cvpr-inv-explained-ratio", "cvpr-inv-mdl"]),
6: ("3.3; 4 Experiments", "definitions_unproved_complexity_and_experiments", ["cvpr-inv-mdl", "cvpr-inv-runtime", "cvpr-inv-evaluation"]),
7: ("4.1–4.2", "synthetic_derivation_and_empirical_evaluation", ["cvpr-inv-addmul", "cvpr-inv-evaluation"]),
8: ("4.2–4.3; 5 Conclusion", "empirical_results_and_conclusion", ["cvpr-inv-evaluation", "cvpr-inv-remark1"]),
9: ("References", "references_only", []), 10: ("References", "references_only", [])}
SUPP = {
1: ("A Related works; B Harsanyi dividend", "related_work_and_definition", ["cvpr-inv-related-work", "cvpr-inv-harsanyi-definition"]),
2: ("B; C", "definitions_all_axiom_and_theorem_statements", ["cvpr-inv-harsanyi-definition", "cvpr-inv-thm1", "cvpr-inv-thm1-uniqueness", "cvpr-inv-efficiency", "cvpr-inv-linearity", "cvpr-inv-dummy", "cvpr-inv-symmetry", "cvpr-inv-anonymity", "cvpr-inv-recursive", "cvpr-inv-distribution", "cvpr-inv-thm5", "cvpr-inv-thm2", "cvpr-inv-thm3", "cvpr-inv-thm4"]),
3: ("C; D.1 introduction", "complete_reconstruction_and_uniqueness_proofs", ["cvpr-inv-thm1", "cvpr-inv-thm1-uniqueness"]),
4: ("D.1 (1)–(4)", "property_proofs", ["cvpr-inv-efficiency", "cvpr-inv-linearity", "cvpr-inv-dummy", "cvpr-inv-symmetry"]),
5: ("D.1 (4)–(7)", "property_proofs", ["cvpr-inv-symmetry", "cvpr-inv-anonymity", "cvpr-inv-recursive", "cvpr-inv-distribution"]),
6: ("D.1 (7); D.2 Theorem5,2", "property_and_theorem_proofs", ["cvpr-inv-distribution", "cvpr-inv-thm5", "cvpr-inv-thm2"]),
7: ("D.2 Theorem2", "theorem_proof_and_beta_ingredients", ["cvpr-inv-thm2", "cvpr-inv-combinatorial-beta"]),
8: ("D.2 Theorem2,3", "theorem_proofs", ["cvpr-inv-thm2", "cvpr-inv-thm3"]),
9: ("D.2 Theorem3,4", "theorem_proofs", ["cvpr-inv-thm3", "cvpr-inv-thm4"]),
10: ("D.2 Theorem4", "theorem_proof", ["cvpr-inv-thm4"]),
11: ("D.2 Theorem4; E", "proof_continuation_and_baseline_discussion", ["cvpr-inv-thm4", "cvpr-inv-mask-definition"]),
12: ("F; G.1–G.2", "algorithm_definitions_and_experimental_setup", ["cvpr-inv-mdl", "cvpr-inv-evaluation"]),
13: ("G.2–G.3", "synthetic_derivations_and_experimental_labeling", ["cvpr-inv-addmul", "cvpr-inv-synthesized-labels"]),
14: ("G.3–G.5", "synthetic_derivation_and_evaluation", ["cvpr-inv-addmul", "cvpr-inv-synthesized-labels", "cvpr-inv-evaluation"]),
15: ("G.5–G.6", "evaluation_metric_definitions_and_empirical_results", ["cvpr-inv-evaluation"]),
16: ("G.6–G.8; H", "empirical_analysis_and_runtime", ["cvpr-inv-evaluation", "cvpr-inv-runtime"]),
17: ("H; I", "runtime_and_bow_discussion", ["cvpr-inv-runtime", "cvpr-inv-bow"]),
18: ("I Table7; References", "empirical_example_and_references", ["cvpr-inv-bow"]),
19: ("References", "references_only", []),20: ("References", "references_only", [])}
for p in range(21,28): SUPP[p] = (f"AOG examples Figures {6 if p==21 else 9 if p==22 else 11 if p==23 else 12 if p==24 else 13 if p==25 else 15 if p==26 else 17}", "visual_empirical_examples_no_proof", [])
audit=[]
for kind, pages in [("main", MAIN),("supp", SUPP)]:
    for number, (section, classification, ids) in pages.items():
        audit.append({"source_id": source_id(kind), "version_id": "ver-cvpr2023-formal", "pdf_page": number, "section": section, "classification": classification, "mathematical_entry_ids": ids, "review_status": "agent_reviewed", "method": "page text read; proof issue pages additionally rendered and visually checked", "evidence_path": str(ROOT / "source-evidence" / f"{kind}-p{number:02d}.txt"), "user_review_status": "pending"})

target_ids=[]
for e in entries:
    if e["merge_target_id"] and e["merge_target_id"] not in target_ids: target_ids.append(e["merge_target_id"])
inventory={"schema_version":"1.0", "paper_id":PAPER,"title":"Defining and Quantifying the Emergence of Sparse Concepts in DNNs", "sources":[source("main",10),source("supp",27)], "review_scope":{"all_main_and_supplement_pages":True,"pdf_pages_checked":37,"formal_source_boundary":"CVPR 2023 CVF main and official supplementary files only"}, "page_audit":audit,"entries":entries,"proof_targets":[{"id":t,"inventory_ids":[e["id"] for e in entries if e["merge_target_id"]==t]} for t in target_ids],"counts":{"numbered_theorem_labels":5,"axiom_property_labels":7,"theorem1_subresults":2,"deduplicated_numbered_or_property_proof_targets":12,"unnumbered_derivation_targets":4,"all_proof_targets":len(target_ids),"inventory_entries":len(entries),"pages_checked":37},"review_status":"agent_reviewed","user_review_status":"pending","completeness_note":"All 37 pages inspected; counts distinguish proof targets, repeated source occurrences, definitions, external ingredients, empirical claims and algorithms. Source-math correctness is separate."}
(ROOT/"inventory.json").write_text(json.dumps(inventory,ensure_ascii=False,indent=2)+"\n")
lines=["# CVPR 2023 全篇正式证明清单", "", "来源：正文 10 页及正式补充材料 27 页，独立从 PDF 第 1 页计数。全部 37 页已检查；这不等于数学无误、重写完成或 Lean 全部通过。", "", "5 个独立定理编号、7 项性质。定理 1 分为重构与唯一性；效率性质是重构的总体实例。归并后 12 个编号/性质目标，另 4 个未编号推导目标，共 16 个。", "", "|ID|原编号|类别|归并目标|陈述页|证明页|", "|---|---|---|---|---|---|"]
def pagestring(locs):return "; ".join(x["source_id"].removeprefix("cvpr2023-")+":"+",".join(map(str,x["pdf_pages"])) for x in locs) or "本篇未给数学证明"
for e in entries:lines.append(f'|{e["id"]}|{e["original_label"]}|{e["kind"]}|{e["merge_target_id"] or "—"}|{pagestring(e["statement_locations"])}|{pagestring(e["proof_locations"])}|')
lines += ["", "## 逐页审查", "", "|来源|PDF页|章节|判定|条目|", "|---|---:|---|---|---|"]
for p in audit:lines.append(f'|{p["source_id"]}|{p["pdf_page"]}|{p["section"]}|{p["classification"]}|{", ".join(p["mathematical_entry_ids"]) or "没有数学证明"}|')
lines += ["", "疑点见 [issues.md](issues.md)。原文出处、转录和内容状态在 content.json 分开保存；原文含疑点的证明依然保留在目录，不从分母删除。"]
(ROOT/"inventory.md").write_text("\n".join(lines)+"\n")
print(json.dumps(inventory["counts"],ensure_ascii=False))
