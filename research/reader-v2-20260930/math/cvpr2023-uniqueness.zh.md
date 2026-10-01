# Appendix C：全部掩码都精确重构时，AND 系数唯一

本页范围：Appendix C uniqueness assertion for fixed AND activation。

## 正式来源

- CVPR 2023 正式补充材料，PDF 页 2,3：Appendix C Theorem 1 与唯一性重述; Appendix C necessity/sufficiency 完整证明。来源文件：`research/paper-survey-20260930/earlier/venue-papers/sparse-cvpr2023-supp/sparse-cvpr2023-supp.pdf`。

## 命题

\[\bigl[\forall S\subseteq N,\ v(x_S)=\sum_{A\subseteq S}\widetilde w_A\bigr]\Longrightarrow\bigl[\forall A\subseteq N,\ \widetilde w_A=\sum_{T\subseteq A}(-1)^{|A|-|T|}v(x_T)=w_A\bigr]\]

## 必要定义与适用条件

固定一个模型 v、一个原始输入 x 和一组输入基线 r。为每个 \(S\subseteq N\) 使用同一规则构造 \(x_S\)，输出 \(v(x_S)\) 是有限实数。

\[N=\{1,\ldots,n\},\quad v(x_S)\in\mathbb R\]

讨论同一有限总体 N 的全部子集，包含空集；不要求不同掩码输入必须互不相同，也不要求输入变量统计独立。

\[S\subseteq N\]

同一组候选系数 \(\widetilde w_A\) 使用相同的 AND 激活规则，并在全部掩码上精确重构。允许所有系数为任意实数。

\[\forall S\subseteq N,\quad\sum_{A\subseteq S}\widetilde w_A=v(x_S)\]

论文模型仍以样本为自变量；g 只是固定 x 和 r 后的集合函数。输入基线向量 r 与输出基线 \(v(x_\varnothing )\) 要分开。

\[g(S):=v(x_S),\qquad (x_S)_i=\begin{cases}x_i&i\in S,\\r_i&i\notin S.\end{cases}\]

候选系数 d 与原文 w̃ 是同一个 \(2^N\)→ℝ 函数，不会为不同 S 改变。

\[d(A):=\widetilde w_A,\qquad g(S):=v(x_S)\]

## 证明思路

在原文已有的全部掩码、相同 AND 激活与固定基线定义下，本条将“满足 faithfulness 的 metric 唯一”精确陈述为系数函数唯一。下方完整公共证明展开逆向反演，解释重构输出如何反过来唯一确定每个系数。

## 将全部掩码假设写成公共定理的前提

<a id="step-1"></a>

固定 x 与 r，设 \(g(S)=v(x_S)\)、\(d(A)=\widetilde w_A\)。论文的 faithfulness 前提就是对每个 \(S\subseteq N\) 都有 \(R_d(S)=g(S)\)。这里的 g、d 都只定义在 \(2^N\) 上，所以全称量词既包含全掩码，又不涉及 N 之外的变量。

\[\forall S\subseteq N,\quad R_d(S)=g(S)\]

依据：候选系数、集合函数、固定有限总体的定义。

## 使用展开过的公共唯一性证明

<a id="step-2"></a>

下方公共证明先给出 \(I_{R_d}=d\)，再逐项代入 \(R_d=g\)，推出 \(d=I_g\)。因此每个 \(A\subseteq N\) 都有 \(\widetilde w_A=I_g(A)=w_A\)。\(S=\varnothing\) 的假设在这个推导中强制 \(\widetilde w_\varnothing=v(x_\varnothing )\)；它不会被零基线约定替代。

\[\widetilde w_A=d(A)=I_g(A)=w_A,\qquad A\subseteq N\]

依据：逆向反演与函数逐点相等。

## 复用的完整公共证明

以下公共证明作为整体被复用，论文特有定义已在上文逐项对齐。

### 辅助引理：逆向反演的归纳起点

先暂时不使用 \(R_d=g\)，单独证明任意系数函数 d 都满足 \(I_{R_d}(S)=d(S)\)。同样对有限 S 插入归纳，并把 d 保留为任意函数，因为插入步骤会引入新函数 e。

若 \(S=\varnothing\)，则 \(R_d(\varnothing )=d(\varnothing )\)。再由空集交互等于被变换函数的空集值，得 \(I_{R_d}(\varnothing )=R_d(\varnothing )=d(\varnothing )\)。这是逆向反演的起点，也说明空集系数并非可以随意选择的额外自由参数。

\[I_{R_d}(\varnothing)=R_d(\varnothing)=d(\varnothing)\]

依据：重构定义、空集交互公式与加强归纳。

### 辅助引理：重构函数的差分也是一个重构

设 \(i\notin S\)，并定义新的系数函数 \(e(U)=d(U\cup \{i\})\)。对任意 \(T\subseteq S\)，都有 \(i\notin T\)，可将 \(R_d(T\cup \{i\})\) 按不含/含 i 的子集拆成 \(R_d(T)\) 加 \(\sum _{U\subseteq T}d(U\cup \{i\})\)。减去 \(R_d(T)\) 后，留下的恰好是 \(R_e(T)\)。

注意该等式只在 \(T\subseteq S\) 的范围使用。若 T 已含 i，子集拆分就不再是两类互不重叠；这个局部等式不需要、也不能强行推广到不受 \(T\subseteq S\) 限制的每个 T。

\[\begin{aligned}(\Delta_i R_d)(T)&=R_d(T\cup\{i\})-R_d(T)\\&=\left(\sum_{U\subseteq T}d(U)+\sum_{U\subseteq T}d(U\cup\{i\})\right)-\sum_{U\subseteq T}d(U)\\&=\sum_{U\subseteq T}e(U)=R_e(T),\qquad T\subseteq S.\end{aligned}\]

依据：\(i\notin T\)；子集拆分；相同有限和消去；e 与 \(R_e\) 的定义。

### 辅助引理：从局部一致性完成插入步骤

先用重构证明中的插入交互引理，得到 \(I_{R_d}(S\cup \{i\})=I_{\Delta_i R_d}(S)\)。交互 \(I_h(S)\) 只读取 h 在 S 的子集上的值；第二步已经逐个证明 \(\Delta_i R_d(T)=R_e(T)\)，故两种函数在这次交替和中的每一项相同。因此 \(I_{\Delta_i R_d}(S)=I_{R_e}(S)\)。最后用“对任意系数函数”的归纳假设，将 \(I_{R_e}(S)\) 化为 \(e(S)=d(S\cup \{i\})\)。这样证明了逆向反演在插入集合上的结论。

\[I_{R_d}(S\cup\{i\})=I_{\Delta_i R_d}(S)=I_{R_e}(S)=e(S)=d(S\cup\{i\})\]

依据：插入交互引理；交互对参与求和的局部函数值保持一致；加强归纳假设。

### 主证明：将全部掩码的重构假设代入

现在恢复假设 ∀T，\(R_d(T)=g(T)\)。固定任意 S。由刚证完的逆向反演，\(d(S)=I_{R_d}(S)\)。在定义 \(I_{R_d}(S)\) 的有限和中，每个 U 都满足 \(U\subseteq S\)，重构假设给出 \(R_d(U)=g(U)\)。逐项替换后，该和就是 \(I_g(S)\)。因此 \(d(S)=I_g(S)\)。这一步使用的是同一组 d 在所有掩码上的假设，而不是每个 S 临时选一组系数。

\[d(S)=I_{R_d}(S)=\sum_{U\subseteq S}(-1)^{|S|-|U|}R_d(U)=\sum_{U\subseteq S}(-1)^{|S|-|U|}g(U)=I_g(S)\]

依据：逆向反演与逐个子集上的重构假设。

### 主证明：逐点相等与适用范围

S 是任意有限子集，所以 d 与 \(I_g\) 在定义域的每个输入上取相同值，这正是两个函数相等的含义。本公共命题的量词遍历 U 的所有有限子集；应用于论文时把总体固定为有限 N，函数定义域随之取为 \(2^N\)。

特别取 \(S=\varnothing\)，重构假设强制 \(d(\varnothing )=g(\varnothing )\)。取 \(S=\{i\}\)，又强制 \(d(\{i\})=g(\{i\})−g(\varnothing )\)。继续增加集合，新的最高阶系数会被已经确定的低阶子集系数唯一决定；这解释了原论文按阶数归纳的直观路线。

\[\forall S,\ d(S)=I_g(S)\quad\Longrightarrow\quad d=I_g\]

依据：函数外延性；论文适配使用固定有限总体。

## 小例子与空集

取 \(N=\{1,2\}\)，并指定 \(g(\varnothing)=2\)、\(g(\{1\})=5\)、\(g(\{2\})=7\)、\(g(\{1,2\})=13\)。任何满足全部掩码重构的 d 都必须依次满足
\[d(\varnothing)=2,\quad d(\{1\})=5-2=3,\quad d(\{2\})=7-2=5,\]
\[d(\{1,2\})=13-2-3-5=3.\]
如果只要求完整输入输出等于 13，另一组 \(d(\varnothing),d(\{1\}),d(\{2\}),d(\{1,2\})=(0,0,0,13)\) 也能满足这一条等式，却在全掩码时输出 0、在单变量掩码时也输出 0。因此“所有 \(S\subseteq N\)”的量词不可删除。

## Lean 检查范围

仅验证 Appendix C 在同一 AND 规则下、所有掩码精确重构的系数唯一性。

声明：`ReaderV2.cvpr_unique_coefficients`

报告：`research/reader-v2-20260930/math/verification/report.json`。

## 文字到 Lean 对照

数学上的有限子集族用 Finset 表示；库要求可判定相等关系。论文适配取 Fin n，使 ∀ S : Finset (Fin n) 恰好遍历固定总体的全部掩码。T⊆S 保证指数中的自然数减法没有截断。库源码中的 h1/h2 是插入基数和符号计算；generalizing v/d 保持对任意函数的加强归纳；funext 实现逐点相等。编译检查形式陈述，定义与论文语义的对应仍须人工核对。

- step-1：`ReaderV2.cvpr_unique_coefficients`，`research/reader-v2-20260930/math/lean/ReaderAdapters.lean:23`。该真实声明的 faithful 参数精确记录所有有限总体掩码，而非只要求完整输入。

- step-2：`Harsanyi.reconstruction_unique`，`lean/HarsanyiLib/Harsanyi/Core/Mobius.lean:66`。reused_exact_declaration

- step-2：`ReaderV2.cvpr_unique_coefficients`，`research/reader-v2-20260930/math/lean/ReaderAdapters.lean:23`。适配复用整条已证明的系数唯一性。

## 边界说明

- 不把唯一性扩大为任意因果解释或任意 AND-OR 分解唯一。

- 只在 N 上匹配一条输出、只在部分掩码上匹配或只作近似匹配，都不足以使用这条命题。

## 原证明路线与本重写的关系

原文第 3 页从空集、单变量和二变量展开系数，然后按集合大小归纳。对一个待确定的 S，从输出恒等式中分离最高阶项：
\[v(x_S)=\widetilde w_S+\sum_{A\subsetneq S}\widetilde w_A.\]
已确定的真子集系数代入后，把有限交替和按 \(v(x_L)\) 收集，得到 w̃_S 的 Harsanyi 公式。本重写保留相同结论与假设，但完整展开现有 Lean 采用的“先证明逆向反演，再应用重构假设”路线；原文按阶数的推导没有逐行改成 Lean。

