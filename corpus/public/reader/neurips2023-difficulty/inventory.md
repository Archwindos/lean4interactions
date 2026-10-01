# F10 正式论文逐页与目标清单

22页正式PDF，SHA256 `068687d3930191bbb82d95ff2e509fb4f189a5c8c773ca1c616459527420664e`。
38入口、28显式数学目标。

| ID | 原局部标签 | 陈述页 | 证明页 | 目标 |
|---|---|---|---|---|
|diff-interaction|Main Eq.(1)|[3]|[]|False|
|diff-universal|Theorem1; Main Eq.(3), exact equality|[4]|[4]|True|
|diff-salient-reconstruction|Main Eq.(2); Theorem1 Eq.(3), approximate clauses|[3, 4]|[]|True|
|diff-sparsity|3.1; citations [45],[47],[27]|[3, 4]|[]|True|
|diff-concept-order|Complexity (order) paragraph|[4]|[]|False|
|diff-reference|Reference-value paragraph; footnote4|[4, 5]|[]|False|
|diff-taylor|Theorem2; Main Eq.(4); G.1 local Eq.(2)–(8)|[4, 17]|[17, 18]|True|
|diff-moments|Theorem3 main lowest-J clause; Main Eq.(5); related G.2 local Eq.(9)–(13)|[5]|[18, 19]|True|
|diff-lowest-interaction|G.2 repeated Theorem3: J prose but unnumbered lowest-I display; local Eq.(9)–(13) argument|[18]|[18, 19]|True|
|diff-general-moments|Theorem3 general-degree clause; Main Eq.(6); G.2 local Eq.(14)–(18)|[5, 19]|[19]|True|
|diff-product|G.2 Proposition1|[18]|[]|True|
|diff-order-variance-argument|After Theorem3, unnumbered chaotic-coefficient inference|[5]|[5]|True|
|diff-order-variance-metrics|E^(s), V^(s), E^(s)/sqrt(V^(s)); Figure2|[5, 6]|[]|False|
|diff-trigger-definition|Main Eq.(7)|[5, 6]|[]|False|
|diff-binary|Theorem4; Main Eq.(8); G.3 local Eq.(19)–(24)|[6, 20]|[6, 20]|True|
|diff-linear-representation|Main Eq.(9), exact equality and approximate salient sum|[6]|[6]|True|
|diff-learning-consistency-argument|3.2.2 unnumbered learning-difficulty inference|[6, 7]|[6, 7]|True|
|diff-training-metrics|beta(S); kappa(S); Figures3–4|[7, 8]|[]|False|
|diff-kappa-conversion|3.2.2 unnumbered equality between two kappa expressions|[7]|[7]|True|
|diff-efficiency|Appendix D property(1)|[15]|[]|True|
|diff-linearity|Appendix D property(2)|[15]|[]|True|
|diff-dummy|Appendix D property(3), nonempty S|[15]|[]|True|
|diff-symmetry|Appendix D property(4)|[16]|[]|True|
|diff-anonymity|Appendix D property(5)|[16]|[]|True|
|diff-recursion|Appendix D property(6), unnumbered|[16]|[]|True|
|diff-distribution|Appendix D property(7), unnumbered|[16]|[]|True|
|diff-multiorder-definition|Appendix F; local Eq.(1)|[16]|[]|False|
|diff-multiorder|G.4; local Eq.(25)|[20, 21]|[20, 21]|True|
|diff-regression|G.5 Steps1–3; local Eq.(26)–(28)|[21]|[21]|True|
|diff-experiments|Appendix H Experimental Settings; related experimental occurrences in C and E|[22]|[]|False|
|diff-training-similarity|3.2.3 unnumbered Jaccard and sign-split formulas; Figure5|[8]|[]|False|
|diff-adversarial-metric|alpha(S), A^(s); Figure6|[9]|[]|False|
|diff-fast-learning-inference|3.2.3 unnumbered consistency-to-speed inference|[8]|[8]|True|
|diff-adversarial-inference|4.1 multiorder-to-concept explanation|[8, 9]|[8, 9]|True|
|diff-noise-learning-inference|4.2 first bullet, Arpit/Cheng|[9]|[9]|True|
|diff-shallow-learning-inference|4.2 second bullet, Mangalam/Prabhu|[9, 10]|[9, 10]|True|
|diff-frequency-learning-inference|4.2 third bullet, Xu|[10]|[10]|True|
|diff-adversarial-learning-inference|4.2 fourth bullet, Liu|[10]|[10]|True|

Main Eq2/3与Appendix G1 Eq2/3有各自章节作用域；D递归/distribution未编号，不造Eq2/3别名。G2最低/一般证明按原转折切分，并独立记录正文J与附录I最低显示差异；原Prop1方差平方与下一式一次方差均保留。D七性质各有入口，dummy明确非空。3.2.3 Jaccard公式与4.1 α/A没有作者编号。

完整作者层由main/appendix/discussion三份独立source transcript及F/H实际原文补齐；逐页txt只作source evidence。真实Gaussian/有限掩码/单ReLU反例与条件证明分别登记，不将无量化学习解释冒充机器定理。
