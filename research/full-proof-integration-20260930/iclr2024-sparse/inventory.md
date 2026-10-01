# ICLR 2024 Sparse：正式全篇数学清单

正式 PDF 34 页，已逐页审查。6 个编号定理、4 个编号引理；7 条仅列述性质。清单共 43 项，按声明与推导归并后 27 个可审查目标；定义、假设、实验、定性说明另分类。该数字是覆盖分母，不是已证明或形式化完成数。

正文重述与附录证明是同一目标；B.4 的 `Theorem 6` 是正文 Theorem 3 的编号别名，B.7 的真正 Theorem 6 单列。A.1 效率性质归并到 Theorem 1。用户审核均待定。

| ID | 原编号 | 类型 | 陈述 PDF 页 | 原证明 PDF 页 | 归并 |
| --- | --- | --- | --- | --- | --- |
| iclr2024-sparse-definitions | Eq. (1) | definition | 3 | 本篇无展开证明 | iclr2024-sparse-definitions |
| iclr2024-sparse-desiderata | Section 3.1 (1)–(3) | desiderata_and_empirical_observation | 3,4 | 本篇无展开证明 | iclr2024-sparse-desiderata |
| iclr2024-sparse-reconstruction | Theorem 1 | numbered_theorem | 4,15 | 15 | iclr2024-sparse-reconstruction |
| iclr2024-sparse-salient-approximation | Section 3.1 unnumbered | unnumbered_inference | 2,4 | 本篇无展开证明 | iclr2024-sparse-salient-approximation |
| iclr2024-sparse-taylor-expansion | Eq. (2) | analytic_representation | 5 | 本篇无展开证明 | iclr2024-sparse-taylor-expansion |
| iclr2024-sparse-assumption-1alpha | Assumption 1-α | assumption | 5,16 | 本篇无展开证明 | iclr2024-sparse-assumption-1alpha |
| iclr2024-sparse-assumption-1beta | Assumption 1-β | assumption | 5 | 本篇无展开证明 | iclr2024-sparse-assumption-1beta |
| iclr2024-sparse-lemma1 | Lemma 1 | numbered_lemma | 15 | 15,16 | iclr2024-sparse-lemma1 |
| iclr2024-sparse-derivative-cutoff | Assumption 1-β ⇒ Assumption 1-α | unnumbered_proved_implication | 5,16 | 16 | iclr2024-sparse-derivative-cutoff |
| iclr2024-sparse-assumption2 | Assumption 2 (Monotonicity) | assumption | 6 | 本篇无展开证明 | iclr2024-sparse-assumption2 |
| iclr2024-sparse-assumption3 | Assumption 3 | assumption | 7 | 本篇无展开证明 | iclr2024-sparse-assumption3 |
| iclr2024-sparse-order-statistics | A^(k), η^(k), R^(k) | definition | 7,8 | 本篇无展开证明 | iclr2024-sparse-order-statistics |
| iclr2024-sparse-lemma2 | Lemma 2 | numbered_lemma | 16 | 17 | iclr2024-sparse-lemma2 |
| iclr2024-sparse-lemma3 | Lemma 3 | numbered_lemma | 17 | 17,18 | iclr2024-sparse-lemma3 |
| iclr2024-sparse-theorem2 | Theorem 2 | numbered_theorem | 7,18,19 | 19,20 | iclr2024-sparse-theorem2 |
| iclr2024-sparse-asymptotic-claim | Section 3.2 unnumbered | unnumbered_asymptotic_inference | 7,8 | 本篇无展开证明 | iclr2024-sparse-asymptotic-claim |
| iclr2024-sparse-theorem3 | Theorem 3 | numbered_theorem | 8,20 | 20,21 | iclr2024-sparse-theorem3 |
| iclr2024-sparse-axiom-efficiency | A.1 (1) | listed_property_no_local_proof | 14 | 本篇无展开证明 | iclr2024-sparse-reconstruction |
| iclr2024-sparse-axiom-linearity | A.1 (2) | listed_property_no_local_proof | 14 | 本篇无展开证明 | iclr2024-sparse-axiom-linearity |
| iclr2024-sparse-axiom-dummy | A.1 (3) | listed_property_no_local_proof | 14 | 本篇无展开证明 | iclr2024-sparse-axiom-dummy |
| iclr2024-sparse-axiom-symmetry | A.1 (4) | listed_property_no_local_proof | 14 | 本篇无展开证明 | iclr2024-sparse-axiom-symmetry |
| iclr2024-sparse-axiom-anonymity | A.1 (5) | listed_property_no_local_proof | 14 | 本篇无展开证明 | iclr2024-sparse-axiom-anonymity |
| iclr2024-sparse-axiom-recursive | A.1 (6) | listed_property_no_local_proof | 14 | 本篇无展开证明 | iclr2024-sparse-axiom-recursive |
| iclr2024-sparse-axiom-distribution | A.1 (7) | listed_property_no_local_proof | 14 | 本篇无展开证明 | iclr2024-sparse-axiom-distribution |
| iclr2024-sparse-lemma4 | Lemma 4 | numbered_lemma | 21 | 21 | iclr2024-sparse-lemma4 |
| iclr2024-sparse-theorem4 | Theorem 4 | numbered_theorem | 4,14,21 | 22,23 | iclr2024-sparse-theorem4 |
| iclr2024-sparse-theorem5 | Theorem 5 | numbered_theorem | 14,23 | 23,24,25 | iclr2024-sparse-theorem5 |
| iclr2024-sparse-theorem6 | Theorem 6 | numbered_theorem | 14,25 | 25,26,27 | iclr2024-sparse-theorem6 |
| iclr2024-sparse-noise-linearity | Scenario 1, unnumbered | unnumbered_algebraic_derivation | 8 | 本篇无展开证明 | iclr2024-sparse-noise-linearity |
| iclr2024-sparse-noise-variance | Scenario 1, unnumbered | unnumbered_probability_claim | 8,9 | 本篇无展开证明 | iclr2024-sparse-noise-variance |
| iclr2024-sparse-parity-mask | Scenario 2 | unnumbered_example_derivation | 9 | 本篇无展开证明 | iclr2024-sparse-parity-mask |
| iclr2024-sparse-or-density | Scenario 3 | qualitative_mathematical_claim | 9 | 本篇无展开证明 | iclr2024-sparse-or-density |
| iclr2024-sparse-periodic-density | Scenario 4 | qualitative_mathematical_claim | 9 | 本篇无展开证明 | iclr2024-sparse-periodic-density |
| iclr2024-sparse-parity-task | Scenario 5 / E.3 | empirical_observation | 9,32 | 本篇无展开证明 | iclr2024-sparse-parity-task |
| iclr2024-sparse-transfer-inference | Section 4 unnumbered | unnumbered_contradiction_argument | 9 | 本篇无展开证明 | iclr2024-sparse-transfer-inference |
| iclr2024-sparse-or-reverse | D.2 unnumbered | unnumbered_algebraic_inference | 29 | 本篇无展开证明 | iclr2024-sparse-or-reverse |
| iclr2024-sparse-and-or-matching | Eq. (62) | external_result_no_local_proof | 29 | 本篇无展开证明 | iclr2024-sparse-and-or-matching |
| iclr2024-sparse-and-or-optimization | Eq. (63) | algorithm_description | 29 | 本篇无展开证明 | iclr2024-sparse-and-or-optimization |
| iclr2024-sparse-threshold-discussion | Appendix F | heuristic_empirical_claim | 33 | 本篇无展开证明 | iclr2024-sparse-threshold-discussion |
| iclr2024-sparse-monotonicity-example | Appendix H | worked_example | 34 | 本篇无展开证明 | iclr2024-sparse-monotonicity-example |
| iclr2024-sparse-sampling-complexity | Appendix I | unnumbered_algorithmic_derivation | 34 | 本篇无展开证明 | iclr2024-sparse-sampling-complexity |
| iclr2024-sparse-experiments | Figures 2–14 / Tables 1–2 | empirical_observation | 3,4,5,6,7,8,27,28,29,30,31,32,33 | 本篇无展开证明 | iclr2024-sparse-experiments |
| iclr2024-sparse-related-work | Section 2 | external_background_no_local_proof | 2,3 | 本篇无展开证明 | iclr2024-sparse-related-work |

## 逐页审查

| PDF 页 | 章节 | 检查结论 |
| --- | --- | --- |
| 1 | Abstract / 1 | 动机与三条件摘要；无独立证明 |
| 2 | 1 / 2 | 示意、近似式与外引背景 |
| 3 | 2 / 3.1 | Eq1定义、中心化、图2经验结果 |
| 4 | 3.1 | 三个标准、Thm1、Thm4脚注及近似解释 |
| 5 | 3.1 / 3.2 | 实验图3、Taylor Eq2、Assumptions1α/1β |
| 6 | 3.2 | Assumption2、经验高阶与均值单调 |
| 7 | 3.2 | Assumption3、Thm2及η定义 |
| 8 | 3.2 / 3.3 | Thm3、两抵消情况、噪声线性与方差 |
| 9 | 3.3 / 4 / 5 | 奇偶、OR、周期示例及迁移反证论述 |
| 10 | References | 复现声明与参考文献；无证明 |
| 11 | References | 参考文献；无证明 |
| 12 | References | 参考文献；无证明 |
| 13 | References | 参考文献；无证明 |
| 14 | A.1 / A.2 | 七条性质、Thm4–6陈述；无性质逐条原证明 |
| 15 | B.1 / B.2 | Thm1完整证明、Lemma1陈述/证明开始 |
| 16 | B.2 / B.3 | Lemma1证明结束、1β⇒1α完整证明、Lemma2陈述 |
| 17 | B.3 | Lemma2完整证明、Lemma3陈述/证明开始 |
| 18 | B.3 | Lemma3证明结束、Thm2陈述开始 |
| 19 | B.3 | Thm2陈述续、n进制展开与两分支 |
| 20 | B.3 / B.4 | Thm2证明结束、Thm3误标Thm6与证明开始 |
| 21 | B.4 / B.5 | Thm3证明结束、Lemma4完整证明、Thm4重述 |
| 22 | B.5 | Thm4有限求和/计数/Beta表达 |
| 23 | B.5 / B.6 | Thm4证明结束、Thm5陈述/定义 |
| 24 | B.6 | Thm5求和/Beta计算 |
| 25 | B.6 / B.7 | Thm5结束、Thm6定义与低阶分支 |
| 26 | B.7 | Thm6临界阶求和与Beta第一项 |
| 27 | B.7 / C.1 | Thm6结束、实验设置 |
| 28 | C / D.1 | 语义部件与LLM实验设置；无严格证明 |
| 29 | D.1 / D.2 | OR定义、反向AND、Eq62匹配、Eq63优化与去噪 |
| 30 | E.1 / E.2 | 图7–9经验高阶近零；无证明 |
| 31 | E.2 | 图10–11经验计数/上界；无证明 |
| 32 | E.2 / E.3 / E.4 | 图12、奇偶实验与部件大小实验；无证明 |
| 33 | E.4 / E.5 / F | 图13–14与阈值启发解释；无严格证明 |
| 34 | G / H / I | 影响展望、完整五变量例、抽样复杂度推导 |

## 证据与边界

原作者各页完整文本在 `evidence/source-text/pXX.txt`，正式图像在 `evidence/pages/page-XX.png`。完整正文/证明的数学转录将在 `math/author-transcript.tex.md` 与 content.json 对齐；本清单只登记范围，不把摘要命名为原证明全文。

数学疑点保留在对应条目；原式、核图、反例与影响单独记录。即使某行符号错误，也分别评估中间步骤和最终结论。最新用户授权 proof_only_granted：直接修复错误证明并标原错处，原命题及假设不改；错误原命题与反例单独列出。
