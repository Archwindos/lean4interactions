# ICLR 2024 Generalizable：全篇数学清单

已审查正式 PDF 全部23页。共30个归并条目、18个证明/推导覆盖目标、87处出现。包括父定理与子结论，不把这个数字称为独立原证明数量。正文3个Theorem、1个Proposition；Definition 1以及方法、实验另列。

原件未修改。原证明错误依最新授权可作忠实证明修正；原命题/假设未获修改授权。

## 逐页核对

| PDF页 | 章节 | 条目数 | 分类 |
|---|---|---:|---|
| 1 | Abstract; Introduction | 1 | external_claim |
| 2 | Introduction; 2.1 AND preliminaries | 3 | definition, unnumbered_claim |
| 3 | 2.1 OR, sparsity, Theorem 1; 2.2 Theorem 2 | 9 | definition, external_claim, external_theorem_component, theorem, unnumbered_derivation |
| 4 | Proposition 1; Challenge 1; Definition 1; 2.3 decomposition | 5 | definition, proposition, unnumbered_derivation, worked_algebraic_example |
| 5 | Eq.(4); 2.3.1 limitations; 2.3.2 begins | 3 | definition, optimization_definition, unnumbered_theorem |
| 6 | Eq.(5),(6); rowmax; shared decomposition | 4 | algorithm_rule, optimization_definition, unnumbered_derivation |
| 7 | Modeling noises; Section 3 tasks | 4 | algorithm_rule, empirical_observation, unnumbered_theorem |
| 8 | Section 3 experiments; Figures 2–4 | 2 | definition, empirical_observation |
| 9 | Section 3 Figure 5; Conclusion; Acknowledgements | 1 | empirical_observation |
| 10 | References | 0 | references |
| 11 | References | 0 | references |
| 12 | Appendix A literature; B conditions; C Theorem 2 / AND proof starts | 6 | definition, external_claim, external_theorem_component, theorem, theorem_component |
| 13 | Appendix C AND proof; OR proof case(1) | 3 | definition, theorem_component |
| 14 | Appendix C OR case(2)–(4); Eq.(9); AND-OR synthesis | 2 | theorem, theorem_component |
| 15 | Theorem 3; Appendix D variance; E theory and experiments | 10 | empirical_observation, experimental_scope, external_claim, external_theorem, external_theorem_component, proposition, theorem, unnumbered_theorem |
| 16 | Appendix E Figure6; F Eq.(10); G complexity starts | 3 | claimed_identity, optimization_definition, unnumbered_derivation |
| 17 | Appendix G timings; H baseline experiment | 4 | algebraic_corollary, empirical_observation, optimization_definition, unnumbered_derivation |
| 18 | Appendix I alpha ablation; J visualization | 3 | algebraic_corollary, empirical_observation, optimization_definition |
| 19 | Appendix J Figure9; K discussion; L Step1 starts | 2 | algorithm_example, empirical_observation |
| 20 | Appendix K Figure10; L Steps1–6 | 7 | algorithm_example, definition, empirical_observation, unnumbered_derivation |
| 21 | Appendix L Steps7–8; M metric; N.1 diversity experiments | 6 | algorithm_example, definition, empirical_observation, optimization_definition |
| 22 | Appendix N.2 matching; O.1 model performance; O.2 starts | 5 | algorithm_rule, empirical_observation, experimental_scope, theorem, unnumbered_derivation |
| 23 | Appendix O.2 input selection details | 3 | definition, experimental_scope, unnumbered_derivation |

## 归并条目

| ID | 原号 | 类型/覆盖 | 陈述页 | 原证明范围 | 判定 |
|---|---|---|---|---|---|
| f11-model-mask | Section 2.1; footnotes 3–5 | definition | 2, 3 | 本篇无单独展开 | 同一模型/输入/基线下的掩码定义；输入bi与输出基线分离。 |
| f11-and-definition | Eq.(1) | definition | 2 | 本篇无单独展开 | 定义并非待证明定理；附录定义作用于AND分量。 |
| f11-and-mask-zero | Section 2.1, AND interactions | unnumbered_claim / 待证覆盖 | 2 | 本篇无单独展开 | 给出一般消失结论但本篇没有展开证明；依赖同一基线的重复掩码语义。 |
| f11-or-definition | Eq.(2) | definition | 3 | 本篇无单独展开 | Eq.(2)的非空式与明确空集约定分别保存，不把空集定义误报为矛盾。 |
| f11-or-duality | Section 2.1; footnote 5 | unnumbered_derivation / 待证覆盖 | 3 | 3–3 footnote 5 | 对非空S，OR值等于反转掩码集合函数AND变换的负值；稀疏推广仍需外引条件。 |
| f11-external-sparsity | Section 2.1; Appendix B | external_claim / 待证覆盖 | 3, 12 | 本篇无证；外引Ren et al. (2024) | 本篇仅定性转述三个条件，没有本地完整证明；对应ICLR Sparse论文需独立对齐。 |
| f11-significant-definition | Definition of interaction primitives | definition | 3 | 本篇无单独展开 | 阈值定义；不把显著性阈值本身当作稀疏性证明。 |
| iclr2024-generalizable-theorem1 | Theorem 1 | external_theorem_component / 待证覆盖 | 3 | 本篇无证；外引Ren et al. (2024) | 原定理把精确重构与近似稀疏同写；此项是可独立证明的精确恒等式。 |
| f11-theorem1-approx | Theorem 1, approximate clause | external_theorem_component / 待证覆盖 | 3 | 本篇无证；外引Ren et al. (2024) | ≈与≪没有本篇量化精度定义；不得补阈值误差结论后冒充原定理。 |
| iclr2024-generalizable-andor | Theorem 2; Eq.(3),(7) | theorem / 待证覆盖 | 3, 12 | 12–14 Appendix C Proof(1)–(3) | 保留原x_T条件式。三个分量/合成证明分别登记；母式证明不能替代字面式掩码合成对齐。 |
| iclr2024-generalizable-and | Appendix C(1); Eq.(8) | theorem_component / 待证覆盖 | 12 | 12–13 Appendix C(1) | 正文父定理与子结论不合并完成状态；Eq.(8)首行x_T记号保留并说明。 |
| iclr2024-generalizable-or | Appendix C(2); Eq.(9) | theorem_component / 待证覆盖 | 13 | 13–14 Appendix C(2) | case(3)内和逐项为0与case(4)范围有原证明错误；已获proof-only修正权限，命题保持。 |
| f11-proposition1 | Proposition 1 | proposition / 待证覆盖 | 4 | 本篇无单独展开 | 本篇无单独证明，依赖Theorem 2和外引稀疏；近似精度未量化，不能编造假设或证明。 |
| f11-boolean-decomposition | Section 2.2 Challenge 1 | worked_algebraic_example / 待证覆盖 | 4 | 4–4 Challenge 1 | 完整代数恒等式与支持项计数；不是全局优化唯一性/最优性定理。 |
| f11-transferability | Definition 1 | definition | 4 | 本篇无单独展开 | 集合交/比例定义；空分母未指定，符号表保留该定义域限制。 |
| f11-reparameterization | Section 2.3; Section 2.3.2 | unnumbered_derivation / 待证覆盖 | 4, 6 | 4–4 Section 2.3 | 对各掩码逐点的实数恒等式；无须优化完成或原OR证明。 |
| f11-objectives | Eq.(4),(5),(6) | optimization_definition | 5, 6 | 本篇无单独展开 | 损失定义及设计解释，原文未证明训练最终全局泛化保证。 |
| f11-rowmax-penalty | Section 2.3.2, following Eq.(5) | unnumbered_derivation / 待证覆盖 | 6 | 6–6 following Eq.(5) | 可证明的是行最大范数的局部不变性；不扩大成学习得到泛化的全局定理。 |
| f11-shared-gamma | Section 2.3.2, Sharing decomposition | algorithm_rule | 6 | 本篇无单独展开 | 优化参数化和操作；严格<目标与剪裁等于阈值的边界表述需显式记录。 |
| f11-and-variance | Section 2.3.2; Appendix D | unnumbered_theorem / 待证覆盖 | 7, 15 | 15–15 Appendix D | 固定交互为常数；对所有子集IID高斯输出噪声推导真正随机变量方差，不仅符号平方计数。 |
| f11-or-variance | Section 2.3.2, Similarly | unnumbered_theorem / 待证覆盖 | 7 | 本篇无单独展开 | 本篇没有独立OR细证；同样通过补集重索引的随机噪声证明，空集值单列。 |
| f11-noise-error | Section 2.3.2, Modeling noises | algorithm_rule | 7 | 本篇无单独展开 | IID随机噪声与优化误差同用epsilon但不同概念；打印|epsilon|=tau sign(epsilon)负号问题独立登记。 |
| f11-shapley | Theorem 3 | external_theorem / 待证覆盖 | 15 | 本篇无证；外引Harsanyi (1963) | 只外引Harsanyi1963，本篇无原证明；复用公共精确定义与完整数学证明。 |
| f11-equation10 | Appendix F; Eq.(10) | claimed_identity / 待证覆盖 | 16 | 16–16 Appendix F Eq.(10) | p6行范数的逐点展开与p16有符号max有反例；原父min等式还含自由索引，严格意义及最优值等价尚未判定。 |
| f11-mask-complexity | Appendix G | unnumbered_derivation / 待证覆盖 | 16 | 16–17 Appendix G | 严格可核的是2^n子集/按全部掩码查询的计数；不将其等同整个训练优化运行时的完整界。 |
| f11-alpha-zero | Appendix I, alpha=0 | algebraic_corollary / 待证覆盖 | 17 | 本篇无单独展开 | 原文消融中的确定恒等式，保留为小推导，经验曲线不计数学证明。 |
| f11-procedure-example | Appendix L, Steps 1–8 | algorithm_example | 19, 20, 21 | 本篇无单独展开 | 列输入域、基线、64掩码、log odds、gamma、交互、优化、阈值；它不是另一条一般正确性证明。 |
| f11-matching-metric | Appendix M | definition | 21 | 本篇无单独展开 | m与模型个数m冲突；v(N)是集合输出简写；分母为0边界未指定。 |
| f11-empirical | Section 3; Appendix E,H,I,J,K,M,N,O.1 | empirical_observation | 7, 8, 9, 15, 17, 18, 19, 20, 21, 22 | 本篇无单独展开 | N.1是随机初始化所得局部解/交互差异实验，没有全球最优解多样性的数学证明。 |
| f11-background-selection | Appendix O.2; Appendix E | experimental_scope | 15, 22, 23 | 本篇无单独展开 | 全部掩码是相对所选N；未选背景不属于掩码总体。经验无交互判断不是形式化零交互条件。 |
