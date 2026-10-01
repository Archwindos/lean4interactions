# CVPR 2023 原陈述与证明问题

用户已授权直接标注并修正证明，禁止修改命题；此授权不等于用户逐个审阅数学事实。原命题错误单列，完整原文另见transcripts。

## Dummy 原陈述包括空集，结论错误 (`cvpr-issue-dummy-empty`)

类别：statement_counterexample；来源：src-cvpr2023-supplement PDF 第 2,4 页。

\[\forall S\subseteq N\setminus\{i\},\;v(x_{S\cup\{i\}})=v(x_S)+v(x_{\{i\}})\ \Longrightarrow\ \forall S\subseteq N\setminus\{i\},\;w_{S\cup\{i\}}=0\]

取 $N=\{i\}$，$v(x_\varnothing)=0$、$v(x_{\{i\}})=1$。原前提只有 $S=\varnothing$ 一个实例，$1=0+1$ 成立。按原定义 $w_{\{i\}}=1-0=1\ne0$。第4页末把 $\sum_{S^{\prime}\subseteq S}(-1)^{|S|-|S^{\prime}|}$ 统一写为0，在 $S=\varnothing$ 时实际为1。PDF图像 supp-04.png 可逐式复核。

只否定原 Dummy 陈述的全部量词版本。其他性质与Theorem1–5不依赖该错误。不能添加S非空条件或删去单变量结论后称原命题证明完成。

原陈述状态：`counterexample_verified`；证明修正授权：`proof_only_granted`；命题修改授权：`not_granted`。

## Linearity 原证明把求和内输出索引印为固定 S (`cvpr-issue-linearity-index`)

类别：proof_display_index_error；来源：src-cvpr2023-supplement PDF 第 4 页。

\[w^v_S=\sum_{S^{\prime}\subseteq S}(-1)^{|S|-|S^{\prime}|}v(x_S)\]

内层应随求和变量变化，但原式固定为 $x_S$。取 $S=\{i\}$、$v(x_\varnothing)=0$、$v(x_{\{i\}})=1$，原显示右侧为 $-1+1=0$，按原定义左侧为1。原稿随后t,u输出亦相同索引。原陈述的线性性没有改变；修正证明直接逐项使用 $g_v(U)=g_t(U)+g_u(U)$。

错误限于原证明显示式，线性性原命题可按现有公共interaction_add忠实证明。

原陈述状态：`no_counterexample_found`；证明修正授权：`proof_only_granted`；命题修改授权：`not_granted`。

## Theorem2–4 的 Beta 定义排印与零参数边界 (`cvpr-issue-beta-proof`)

类别：proof_definition_and_boundary_error；来源：src-cvpr2023-supplement PDF 第 7,8,9,10,11 页。

\[B(p,q)=\int_0^1x^{p-1}(1-x)^{1-q}\,dx;\quad B(|N|-|L|-k,|L|+k);\quad \int_0^1|L|(1-x)^{|L|-1}\,dx=1\]

第7页(ii)明示 $p,q>0$ 却将指数写为 $1-q$。取 $(p,q)=(1,2)$，其积分发散，后续有限阶乘公式不匹配。同页 $L=\varnothing,k=0$ 是求和允许项，却调用 $B(|N|,0)$，超出正参数定义；①在 $|L|=0$ 时被积函数在开区间上为零，统一写成1不成立。Theorem3第9页和Theorem4第10–11页复用这一路线，故归并为同一issue。另极端剩余集合为空时②的重编号上界成为负数，须明确空和，而原文未单独处理。

原Shapley、SII、STI结论未发现反例。保持同一命题的全部允许集合，使用有限阶乘卷积给完整证明，含L空集与剩余集合为空，避免修补原积分域而改变目标。

原陈述状态：`no_counterexample_found`；证明修正授权：`proof_only_granted`；命题修改授权：`not_granted`。

## 纯AND分布证明的三个case没有覆盖不可比集合 (`cvpr-issue-distribution-incomparable`)

类别：proof_case_coverage_gap；来源：src-cvpr2023-supplement PDF 第 5,6 页。

\[S\subsetneq T;\quad S=T;\quad S\supsetneq T\]

原目标量化全部 $S\subseteq N$，但原证明只写上述三类。例 $N=\{1,2\}$、$T=\{1\}$、$S=\{2\}$ 落在三类之外。目标 $w_S=0$ 在此仍真，因为没有 $U\subseteq S$ 包含T。修正证明以 $T\not\subseteq S$、$S=T$、$T\subsetneq S$ 分组（不改原陈述），也可直接复用已编译的interaction_unanimity。

原目标正确，原证明缺case。Add-Mul推导复用这个目标，保留同一原命题并完成修证明。

原陈述状态：`no_counterexample_found`；证明修正授权：`proof_only_granted`；命题修改授权：`not_granted`。

## 选择集合大小与非零系数个数不总相等 (`cvpr-issue-l0-support`)

类别：algorithm_or_definition_boundary；来源：src-cvpr2023-main PDF 第 4 页。

\[\|\boldsymbol w_\Omega\|_0=|\Omega|\]

第4页定义 $w^{\prime}_S=w_S$ 若 $S\in\Omega$，否则为0。若 $S\in\Omega$ 而 $w_S=0$，它贡献集合大小却不贡献L0范数；例如全零模型、$\Omega=\{\varnothing\}$ 给0与1。两类可行表示的最优值可能通过删除零项联系，但原逐项相等并无无条件证明。

这是算法段的原等式边界，不是编号定理；不静默把Omega定义改为support。目录保留原式和反例。

原陈述状态：`counterexample_verified`；证明修正授权：`proof_only_granted`；命题修改授权：`not_granted`。

## L0约束与固定罚参数目标的等价箭头未被证明 (`cvpr-issue-lagrange-equivalence`)

类别：algorithm_or_definition_boundary；来源：src-cvpr2023-main PDF 第 4 页。

\[\min\mathrm{unfaith}\ \mathrm{s.t.}\|w_\Omega\|_0\le M\ \Longleftrightarrow\ \min\mathrm{unfaith}+\lambda\|w_\Omega\|_0\]

原Eq.(6)没有规定罚参数如何选取或证明离散非凸目标的强对偶。一般离散优化中，可行点 (support,error)=(0,3),(1,2),(2,0)，约束M=1选择中点，但任何lambda要选中点都需lambda≤1且lambda≥2，矛盾。本反例针对一般等价箭头，没有声称这一三点实例已由本文某个DNN产生。

只能按原文登记为启发式目标转换/松弛；不当作本篇已证明的数学等价。

原陈述状态：`no_counterexample_found`；证明修正授权：`proof_only_granted`；命题修改授权：`not_granted`。

## 已解释比例在全部效应为零时未定义 (`cvpr-issue-ratio-zero-denominator`)

类别：algorithm_or_definition_boundary；来源：src-cvpr2023-main PDF 第 5 页。

\[R_\Omega=\frac{\sum_{S\in\Omega}|w_S|}{\sum_{S\in\Omega}|w_S|+|\Delta|}\]

取 $v(x_S)=0$ 对所有S，得到全部 $w_S=0$、$\Delta=0$，分母为0。原文未给此边界约定。符号表把分母非零记录为表达式的定义域条件，不据此修改原论文命题或杜撰R值。

仅影响指标的零模型边界与符号域；重构/唯一性仍适用。

原陈述状态：`counterexample_verified`；证明修正授权：`proof_only_granted`；命题修改授权：`not_granted`。


## 基线变化也会改变截断的平方残差损失

原“just affects $\|w_\Omega\|_1$”不能解释为截断损失unfaith不随基线变。取单变量模型 $v(z)=z$、原输入x=1、输入基线r、只保留 $\Omega=\{\varnothing\}$。完整交互为 $w_\varnothing=r,w_{\{1\}}=1-r$；截断残差平方和为 $[r-r]^2+[1-r]^2=(1-r)^2$，随r变化。完整交互的unfaith始终0，但截断损失部分也可能改变。保留原句、单列该解释错误，不把原复合断言替换成较弱命题后算整体通过。

完整w各自重构的恒等式成立；不据此证明截断损失只变化L1。原复合句保留且分开状态。
