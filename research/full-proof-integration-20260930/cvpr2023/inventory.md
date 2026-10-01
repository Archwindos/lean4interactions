# CVPR 2023 全篇正式证明清单

来源：正文 10 页及正式补充材料 27 页，独立从 PDF 第 1 页计数。全部 37 页已检查；这不等于数学无误、重写完成或 Lean 全部通过。

5 个独立定理编号、7 项性质。定理 1 分为重构与唯一性；效率性质是重构的总体实例。归并后 12 个编号/性质目标，另 4 个未编号推导目标，共 16 个。

|ID|原编号|类别|归并目标|陈述页|证明页|
|---|---|---|---|---|---|
|cvpr-inv-thm1|Theorem 1; Appendix C Theorem 1|numbered_theorem|cvpr2023-reconstruction|src-cvpr2023-main:3; src-cvpr2023-supplement:2|src-cvpr2023-supplement:3|
|cvpr-inv-thm1-uniqueness|Appendix C sufficiency|theorem_subresult|cvpr2023-uniqueness|src-cvpr2023-supplement:2|src-cvpr2023-supplement:3|
|cvpr-inv-efficiency|Axiom (1) Efficiency|axiom_property|cvpr2023-reconstruction|src-cvpr2023-main:4; src-cvpr2023-supplement:2|src-cvpr2023-supplement:4|
|cvpr-inv-linearity|Axiom (2) Linearity|axiom_property|cvpr2023-linearity|src-cvpr2023-supplement:2|src-cvpr2023-supplement:4|
|cvpr-inv-dummy|Axiom (3) Dummy|axiom_property|cvpr2023-dummy|src-cvpr2023-supplement:2; src-cvpr2023-supplement:4|src-cvpr2023-supplement:4|
|cvpr-inv-symmetry|Axiom (4) Symmetry|axiom_property|cvpr2023-symmetry|src-cvpr2023-supplement:2; src-cvpr2023-supplement:4|src-cvpr2023-supplement:4,5|
|cvpr-inv-anonymity|Axiom (5) Anonymity|axiom_property|cvpr2023-anonymity|src-cvpr2023-supplement:2; src-cvpr2023-supplement:5|src-cvpr2023-supplement:5|
|cvpr-inv-recursive|Axiom (6) Recursive|axiom_property|cvpr2023-recursive|src-cvpr2023-supplement:2; src-cvpr2023-supplement:5|src-cvpr2023-supplement:5|
|cvpr-inv-distribution|Axiom (7) Interaction distribution|axiom_property|cvpr2023-interaction-distribution|src-cvpr2023-supplement:2; src-cvpr2023-supplement:5|src-cvpr2023-supplement:5,6|
|cvpr-inv-thm5|Theorem 5|numbered_theorem|cvpr2023-marginal-decomposition|src-cvpr2023-supplement:2; src-cvpr2023-supplement:6|src-cvpr2023-supplement:6|
|cvpr-inv-thm2|Theorem 2|numbered_theorem|cvpr2023-shapley|src-cvpr2023-main:4; src-cvpr2023-supplement:2; src-cvpr2023-supplement:6|src-cvpr2023-supplement:6,7,8|
|cvpr-inv-thm3|Theorem 3|numbered_theorem|cvpr2023-shapley-interaction|src-cvpr2023-supplement:2; src-cvpr2023-supplement:8|src-cvpr2023-supplement:8,9|
|cvpr-inv-thm4|Theorem 4|numbered_theorem|cvpr2023-shapley-taylor|src-cvpr2023-supplement:2; src-cvpr2023-supplement:9|src-cvpr2023-supplement:9,10,11|
|cvpr-inv-scm|Main Eq. (1), (2); unnumbered derivation|unnumbered_derivation|cvpr2023-scm-subset-sum|src-cvpr2023-main:3,4|src-cvpr2023-main:4|
|cvpr-inv-baseline-invariance|Main 3.2 unnumbered statement|unnumbered_derivation|cvpr2023-baseline-faithfulness|src-cvpr2023-main:5|src-cvpr2023-main:3,5|
|cvpr-inv-aog|Main 3.3 unnumbered derivation|unnumbered_derivation|cvpr2023-aog-regrouping|src-cvpr2023-main:5|src-cvpr2023-main:5|
|cvpr-inv-addmul|Main 4.1; Supplement G.3 examples|unnumbered_derivation|cvpr2023-addmul-coefficients|src-cvpr2023-main:7; src-cvpr2023-supplement:13,14|src-cvpr2023-main:7; src-cvpr2023-supplement:13,14|
|cvpr-inv-harsanyi-definition|Supplement Eq. (1); main Theorem 1 definition|definition|—|src-cvpr2023-main:3; src-cvpr2023-supplement:2|本篇未给数学证明|
|cvpr-inv-mask-definition|Main Eq. (4); Supplement E|definition|—|src-cvpr2023-main:3,4; src-cvpr2023-supplement:11|本篇未给数学证明|
|cvpr-inv-remark1|Remark 1|empirical_observation|—|src-cvpr2023-main:4; src-cvpr2023-main:2,3,8|本篇未给数学证明|
|cvpr-inv-combinatorial-beta|D.2 (i)–(iii), unnumbered ingredients|external_unproved_ingredient|—|src-cvpr2023-supplement:7|本篇未给数学证明|
|cvpr-inv-optimization|Main Eq. (5), (6)|algorithm_and_heuristic|—|src-cvpr2023-main:4,5|本篇未给数学证明|
|cvpr-inv-explained-ratio|Main Eq. (7)|definition|—|src-cvpr2023-main:5|本篇未给数学证明|
|cvpr-inv-mdl|Main Eq. (8); Supplement Eq. (3)|algorithm_and_definition|—|src-cvpr2023-main:5,6; src-cvpr2023-supplement:12|本篇未给数学证明|
|cvpr-inv-evaluation|Main 4.1–4.3; Supplement G.4–G.8 Eq. (4), (5)|definition_and_empirical_analysis|—|src-cvpr2023-main:6,7,8; src-cvpr2023-supplement:14,15,16|本篇未给数学证明|
|cvpr-inv-synthesized-labels|Supplement G.3|experimental_labeling_convention|—|src-cvpr2023-supplement:13,14|本篇未给数学证明|
|cvpr-inv-runtime|Main 3.3; Supplement H|unproved_complexity_and_empirical_runtime|—|src-cvpr2023-main:6; src-cvpr2023-supplement:16,17|本篇未给数学证明|
|cvpr-inv-bow|Supplement I; Table 6,7|discussion_and_empirical_example|—|src-cvpr2023-supplement:17,18|本篇未给数学证明|
|cvpr-inv-related-work|Main 2; Supplement A|external_claim_without_proof|—|src-cvpr2023-main:2; src-cvpr2023-supplement:1|本篇未给数学证明|

## 逐页审查

|来源|PDF页|章节|判定|条目|
|---|---:|---|---|---|
|src-cvpr2023-main|1|Abstract; 1 Introduction|expository_and_empirical|没有数学证明|
|src-cvpr2023-main|2|1 Introduction; 2 XAI theory; 3 Method|related_work_and_overview|cvpr-inv-related-work, cvpr-inv-remark1|
|src-cvpr2023-main|3|3.1 Causal graph|definitions_and_numbered_theorem_statement|cvpr-inv-thm1, cvpr-inv-scm, cvpr-inv-mask-definition, cvpr-inv-harsanyi-definition|
|src-cvpr2023-main|4|3.1–3.2|theorem_property_statements_and_optimization|cvpr-inv-thm2, cvpr-inv-efficiency, cvpr-inv-remark1, cvpr-inv-optimization, cvpr-inv-scm|
|src-cvpr2023-main|5|3.2–3.3|unnumbered_derivations_and_algorithms|cvpr-inv-baseline-invariance, cvpr-inv-aog, cvpr-inv-optimization, cvpr-inv-explained-ratio, cvpr-inv-mdl|
|src-cvpr2023-main|6|3.3; 4 Experiments|definitions_unproved_complexity_and_experiments|cvpr-inv-mdl, cvpr-inv-runtime, cvpr-inv-evaluation|
|src-cvpr2023-main|7|4.1–4.2|synthetic_derivation_and_empirical_evaluation|cvpr-inv-addmul, cvpr-inv-evaluation|
|src-cvpr2023-main|8|4.2–4.3; 5 Conclusion|empirical_results_and_conclusion|cvpr-inv-evaluation, cvpr-inv-remark1|
|src-cvpr2023-main|9|References|references_only|没有数学证明|
|src-cvpr2023-main|10|References|references_only|没有数学证明|
|src-cvpr2023-supplement|1|A Related works; B Harsanyi dividend|related_work_and_definition|cvpr-inv-related-work, cvpr-inv-harsanyi-definition|
|src-cvpr2023-supplement|2|B; C|definitions_all_axiom_and_theorem_statements|cvpr-inv-harsanyi-definition, cvpr-inv-thm1, cvpr-inv-thm1-uniqueness, cvpr-inv-efficiency, cvpr-inv-linearity, cvpr-inv-dummy, cvpr-inv-symmetry, cvpr-inv-anonymity, cvpr-inv-recursive, cvpr-inv-distribution, cvpr-inv-thm5, cvpr-inv-thm2, cvpr-inv-thm3, cvpr-inv-thm4|
|src-cvpr2023-supplement|3|C; D.1 introduction|complete_reconstruction_and_uniqueness_proofs|cvpr-inv-thm1, cvpr-inv-thm1-uniqueness|
|src-cvpr2023-supplement|4|D.1 (1)–(4)|property_proofs|cvpr-inv-efficiency, cvpr-inv-linearity, cvpr-inv-dummy, cvpr-inv-symmetry|
|src-cvpr2023-supplement|5|D.1 (4)–(7)|property_proofs|cvpr-inv-symmetry, cvpr-inv-anonymity, cvpr-inv-recursive, cvpr-inv-distribution|
|src-cvpr2023-supplement|6|D.1 (7); D.2 Theorem5,2|property_and_theorem_proofs|cvpr-inv-distribution, cvpr-inv-thm5, cvpr-inv-thm2|
|src-cvpr2023-supplement|7|D.2 Theorem2|theorem_proof_and_beta_ingredients|cvpr-inv-thm2, cvpr-inv-combinatorial-beta|
|src-cvpr2023-supplement|8|D.2 Theorem2,3|theorem_proofs|cvpr-inv-thm2, cvpr-inv-thm3|
|src-cvpr2023-supplement|9|D.2 Theorem3,4|theorem_proofs|cvpr-inv-thm3, cvpr-inv-thm4|
|src-cvpr2023-supplement|10|D.2 Theorem4|theorem_proof|cvpr-inv-thm4|
|src-cvpr2023-supplement|11|D.2 Theorem4; E|proof_continuation_and_baseline_discussion|cvpr-inv-thm4, cvpr-inv-mask-definition|
|src-cvpr2023-supplement|12|F; G.1–G.2|algorithm_definitions_and_experimental_setup|cvpr-inv-mdl, cvpr-inv-evaluation|
|src-cvpr2023-supplement|13|G.2–G.3|synthetic_derivations_and_experimental_labeling|cvpr-inv-addmul, cvpr-inv-synthesized-labels|
|src-cvpr2023-supplement|14|G.3–G.5|synthetic_derivation_and_evaluation|cvpr-inv-addmul, cvpr-inv-synthesized-labels, cvpr-inv-evaluation|
|src-cvpr2023-supplement|15|G.5–G.6|evaluation_metric_definitions_and_empirical_results|cvpr-inv-evaluation|
|src-cvpr2023-supplement|16|G.6–G.8; H|empirical_analysis_and_runtime|cvpr-inv-evaluation, cvpr-inv-runtime|
|src-cvpr2023-supplement|17|H; I|runtime_and_bow_discussion|cvpr-inv-runtime, cvpr-inv-bow|
|src-cvpr2023-supplement|18|I Table7; References|empirical_example_and_references|cvpr-inv-bow|
|src-cvpr2023-supplement|19|References|references_only|没有数学证明|
|src-cvpr2023-supplement|20|References|references_only|没有数学证明|
|src-cvpr2023-supplement|21|AOG examples Figures 6|visual_empirical_examples_no_proof|没有数学证明|
|src-cvpr2023-supplement|22|AOG examples Figures 9|visual_empirical_examples_no_proof|没有数学证明|
|src-cvpr2023-supplement|23|AOG examples Figures 11|visual_empirical_examples_no_proof|没有数学证明|
|src-cvpr2023-supplement|24|AOG examples Figures 12|visual_empirical_examples_no_proof|没有数学证明|
|src-cvpr2023-supplement|25|AOG examples Figures 13|visual_empirical_examples_no_proof|没有数学证明|
|src-cvpr2023-supplement|26|AOG examples Figures 15|visual_empirical_examples_no_proof|没有数学证明|
|src-cvpr2023-supplement|27|AOG examples Figures 17|visual_empirical_examples_no_proof|没有数学证明|

疑点见 [issues.md](issues.md)。原文出处、转录和内容状态在 content.json 分开保存；原文含疑点的证明依然保留在目录，不从分母删除。
