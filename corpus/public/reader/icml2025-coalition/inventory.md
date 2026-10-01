# ICML 2025 Coalition：正式来源逐页数学清单

正式 PDF：24 页；SHA256 `34f0f5be313ee5b2c260adcf59d4ecfadde0be0db0bebb82905879302590a63a`。正文编号 3.x 与附录省略前缀的编号合并，原文十个证明块不作为目标数量上限。

## 逐页审查

- PDF 1：Abstract; Introduction; Figure 1；条目：coalition-inv-illustration。
- PDF 2：Introduction; Related work; §3.1；条目：coalition-inv-external-comparison。
- PDF 3：§3.1–3.2; Eqs. (1)–(4)；条目：coalition-inv-logit, coalition-inv-shapley-definition, coalition-inv-and-or-definition, coalition-inv-sparse-optimization, coalition-inv-matching, coalition-inv-external-comparison。
- PDF 4：§3.2–3.4; Definition 3.1; Eqs. (5)–(6)；条目：coalition-inv-illustration, coalition-inv-conflict-definition, coalition-inv-shapley, coalition-inv-banzhaf-definition, coalition-inv-banzhaf, coalition-inv-coalition-definition。
- PDF 5：§3.4; Table 1; Theorems/Corollaries 3.4–3.7；条目：coalition-inv-conflict, coalition-inv-no-conflict, coalition-inv-individual, coalition-inv-singleton, coalition-inv-external-comparison。
- PDF 6：§3.5–4.1; Axioms; Corollary 3.8; Eqs. (7)–(8)；条目：coalition-inv-anonymity, coalition-inv-symmetry-alpha, coalition-inv-symmetry-beta, coalition-inv-additivity, coalition-inv-dummy, coalition-inv-efficiency, coalition-inv-R, coalition-inv-Rprime, coalition-inv-empirical。
- PDF 7：§4.1–4.2; Eq. (9); toy functions；条目：coalition-inv-Rprime, coalition-inv-Q, coalition-inv-toy-support, coalition-inv-empirical。
- PDF 8：§4.2; Figure 2; Go score；条目：coalition-inv-logit, coalition-inv-empirical。
- PDF 9：§4.2; Conclusion; Impact; References；条目：coalition-inv-empirical。
- PDF 10：References；条目：无证明/仅参考文献。
- PDF 11：References；条目：无证明/仅参考文献。
- PDF 12：A; B; C start; Eq. (10)；条目：coalition-inv-shapley, coalition-inv-matching, coalition-inv-external-comparison。
- PDF 13：C AND coefficient；条目：coalition-inv-shapley, coalition-inv-shapley-coefficient。
- PDF 14：C OR coefficient; D start；条目：coalition-inv-shapley, coalition-inv-banzhaf, coalition-inv-marginal-pairing, coalition-inv-shapley-coefficient。
- PDF 15：D; E start；条目：coalition-inv-banzhaf, coalition-inv-conflict, coalition-inv-marginal-pairing, coalition-inv-banzhaf-coefficient。
- PDF 16：E; F；条目：coalition-inv-conflict, coalition-inv-no-conflict, coalition-inv-individual。
- PDF 17：F; G.1；条目：coalition-inv-singleton, coalition-inv-anonymity。
- PDF 18：G.2；条目：coalition-inv-symmetry-alpha。
- PDF 19：G.2 end; G.3 start；条目：coalition-inv-symmetry-alpha, coalition-inv-symmetry-beta。
- PDF 20：G.3; G.4；条目：coalition-inv-symmetry-beta, coalition-inv-additivity。
- PDF 21：G.5; G.6; H; I start；条目：coalition-inv-dummy, coalition-inv-efficiency, coalition-inv-marginal-pairing, coalition-inv-empirical。
- PDF 22：I; J; Figure 3；条目：coalition-inv-empirical。
- PDF 23：Figures 4–5；条目：coalition-inv-empirical。
- PDF 24：Figures 6–7；条目：coalition-inv-empirical。

## 独立条目

- `coalition-inv-illustration` (illustrative_calculation)：Figure 1 的分配与冲突算例；原标签 Figure 1; §3.2 example；目标 `coalition-illustration`。
- `coalition-inv-logit` (definition)：分类任务输出定义；原标签 Eq. (1); Go output definition；目标 `coalition-logit`。
- `coalition-inv-shapley-definition` (definition_and_external_result)：阶乘边际 Shapley 定义与外引唯一性；原标签 Eq. (2)；目标 `coalition-shapley-definition`。
- `coalition-inv-and-or-definition` (definition)：AND/OR 分量、交互与分解参数；原标签 Eqs. (3),(4)；目标 `coalition-and-or-definition`。
- `coalition-inv-sparse-optimization` (external_algorithm)：AND/OR 稀疏优化的外引方法；原标签 LASSO-like loss；目标 `coalition-sparse-optimization`。
- `coalition-inv-conflict-definition` (definition)：不同分区的归因冲突定义；原标签 Definition 3.1；目标 `coalition-conflict-definition`。
- `coalition-inv-shapley` (numbered_theorem)：Shapley 的 AND/OR 均分表达；原标签 Theorem 3.2; Appendix Theorem 2；目标 `coalition-shapley`。
- `coalition-inv-banzhaf-definition` (definition)：Banzhaf 均匀边际定义；原标签 Eq. (5)；目标 `coalition-banzhaf-definition`。
- `coalition-inv-banzhaf` (numbered_theorem)：Banzhaf 的 AND/OR 分配表达；原标签 Theorem 3.3; Appendix Theorem 3；目标 `coalition-banzhaf`。
- `coalition-inv-coalition-definition` (definition)：联盟归因定义与空集定义域；原标签 Eq. (6)；目标 `coalition-coalition-definition`。
- `coalition-inv-conflict` (numbered_theorem)：联盟内总 Shapley 与冲突项分解；原标签 Theorem 3.4; Appendix Theorem 4；目标 `coalition-conflict`。
- `coalition-inv-no-conflict` (numbered_corollary)：无部分交互时归因无冲突；原标签 Corollary 3.5; Appendix Corollary 5；目标 `coalition-no-conflict`。
- `coalition-inv-individual` (numbered_theorem)：单变量 Shapley 的联盟与部分覆盖分解；原标签 Theorem 3.6; Appendix Theorem 6；目标 `coalition-individual`。
- `coalition-inv-singleton` (numbered_corollary)：单元素联盟与 Shapley 一致；原标签 Corollary 3.7; Appendix Corollary 7；目标 `coalition-singleton`。
- `coalition-inv-anonymity` (axiom_claim)：联盟归因匿名性；原标签 Anonymity axiom；目标 `coalition-anonymity`。
- `coalition-inv-symmetry-alpha` (axiom_claim)：联盟归因对称性 α；原标签 Symmetry axiom-α；目标 `coalition-symmetry-alpha`。
- `coalition-inv-symmetry-beta` (axiom_claim)：联盟归因对称性 β；原标签 Symmetry axiom-β；目标 `coalition-symmetry-beta`。
- `coalition-inv-additivity` (axiom_claim)：联盟归因可加性；原标签 Additivity axiom；目标 `coalition-additivity`。
- `coalition-inv-dummy` (axiom_claim)：联盟归因虚设变量性质；原标签 Dummy axiom；目标 `coalition-dummy`。
- `coalition-inv-efficiency` (numbered_corollary)：含冲突项的输出效率分解；原标签 Corollary 3.8; Appendix Corollary 8；目标 `coalition-efficiency`。
- `coalition-inv-R` (unnumbered_domain_and_range_claim)：绝对值比例的定义域与范围；原标签 Eq. (7)；目标 `coalition-R`。
- `coalition-inv-Rprime` (unnumbered_domain_and_range_claim)：单变量绝对交互比例的定义域与范围；原标签 Eq. (8)；目标 `coalition-Rprime`。
- `coalition-inv-Q` (unnumbered_domain_and_range_claim)：联盟绝对交互比例的定义域与范围；原标签 Eq. (9)；目标 `coalition-Q`。
- `coalition-inv-toy-support` (unnumbered_algebraic_claim)：二进制单项式函数的真实交互；原标签 Toy function in §4.1；目标 `coalition-toy-support`。
- `coalition-inv-matching` (externally_proved_identity)：AND/OR 全掩码重构；原标签 Universal-matching; Eq. (10)；目标 `coalition-matching`。
- `coalition-inv-marginal-pairing` (unnumbered_proof_ingredient)：插入变量的 AND/OR 配对边际；原标签 D first equations; G.5 first equations；目标 `coalition-banzhaf`。
- `coalition-inv-shapley-coefficient` (unnumbered_derivation)：Shapley 上集/不交集权重为逆阶数；原标签 α_L; OR coefficient；目标 `coalition-shapley-coefficient`。
- `coalition-inv-banzhaf-coefficient` (unnumbered_derivation)：有符号二项式上集权重；原标签 D signed power sum；目标 `coalition-banzhaf-coefficient`。
- `coalition-inv-empirical` (empirical_claim)：三类任务与误差、忠实度的经验观察；原标签 Tables 2–5; Figures 2–7; I; J；目标 `coalition-empirical`。
- `coalition-inv-external-comparison` (external_comparison)：其他归因指标性质的外引与表格；原标签 Related work; Table 1; A；目标 `coalition-external-comparison`。

## 分母

{"numbered_results": 7, "axiom_claims_excluding_repeated_efficiency": 5, "unnumbered_domain_or_algebra_targets": 4, "unnumbered_coefficient_derivations": 2, "external_identity_targets": 1, "all_proof_targets": 19, "original_dedicated_proof_blocks": 10, "inventory_entries": 30, "pages_checked": 24}

当前仅代理审查；原陈述正确性、文字重写和 Lean 证据分别记录。
