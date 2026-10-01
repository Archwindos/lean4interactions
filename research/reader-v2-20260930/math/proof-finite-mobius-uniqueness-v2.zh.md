# 公共证明：同时重构所有掩码输出的系数唯一

本页范围：公共有限集合定理。

## 命题

\[\forall g,d,\quad\bigl[\forall S,\ R_d(S)=g(S)\bigr]\Longrightarrow\bigl[\forall S,\ d(S)=I_g(S)\bigr]\]

## 必要定义与适用条件

S 是有限变量集合。g 与 d 是定义在有限变量子集上的任意实值函数；不要求连续、可微、独立性或零输出基线。

\[g,d:\mathcal P_{\mathrm{fin}}(U)\to\mathbb R\]

U 表示变量总体，\(\mathcal P_{\mathrm{fin}}(U)\) 表示其所有有限子集。每次参与求和的 S、T 都有限；变量总体本身可以无限。论文应用则固定有限总体 N，只讨论 \(2^N\)。

\[S\in\mathcal P_{\mathrm{fin}}(U)\]

同一组系数 d 必须重构定义域内每一个有限子集的输出，包括空集。只在一个指定集合上重构不够。

\[\forall S\in\mathcal P_{\mathrm{fin}}(U),\quad\sum_{T\subseteq S}d(T)=g(S)\]

交互是有限交替和。\(T\subseteq S\) 保证 |T|≤|S|，因此指数 \(|S|-|T|\) 是非负整数。

\[I_g(S):=\sum_{T\subseteq S}(-1)^{|S|-|T|}g(T)\]

\(R_d\) 是在给定保留变量集 S 上累加所有被激活的系数。

\[R_d(S):=\sum_{T\subseteq S}d(T)\]

插入差分比较保留 i 与掩码 i 两种状态。下面的插入引理只在 \(i\notin S\) 时使用。

\[(\Delta_i g)(T):=g(T\cup\{i\})-g(T)\]

## 证明思路

把“对系数求子集和”再做一次交替差分，会恢复原系数。这是逆向 Möbius 反演 \(I_{R_d}=d\)。先证明这个辅助结论，再把“所有掩码上 \(R_d=g\)”的假设代入，就得到 \(d=I_g\)。下面完整证明所需的逆向反演，给出唯一性成立的理由。

## 辅助引理：逆向反演的归纳起点

<a id="step-1"></a>

先暂时不使用 \(R_d=g\)，单独证明任意系数函数 d 都满足 \(I_{R_d}(S)=d(S)\)。同样对有限 S 插入归纳，并把 d 保留为任意函数，因为插入步骤会引入新函数 e。

若 \(S=\varnothing\)，则 \(R_d(\varnothing )=d(\varnothing )\)。再由空集交互等于被变换函数的空集值，得 \(I_{R_d}(\varnothing )=R_d(\varnothing )=d(\varnothing )\)。这是逆向反演的起点，也说明空集系数并非可以随意选择的额外自由参数。

\[I_{R_d}(\varnothing)=R_d(\varnothing)=d(\varnothing)\]

依据：重构定义、空集交互公式与加强归纳。

## 辅助引理：重构函数的差分也是一个重构

<a id="step-2"></a>

设 \(i\notin S\)，并定义新的系数函数 \(e(U)=d(U\cup \{i\})\)。对任意 \(T\subseteq S\)，都有 \(i\notin T\)，可将 \(R_d(T\cup \{i\})\) 按不含/含 i 的子集拆成 \(R_d(T)\) 加 \(\sum _{U\subseteq T}d(U\cup \{i\})\)。减去 \(R_d(T)\) 后，留下的恰好是 \(R_e(T)\)。

注意该等式只在 \(T\subseteq S\) 的范围使用。若 T 已含 i，子集拆分就不再是两类互不重叠；这个局部等式不需要、也不能强行推广到不受 \(T\subseteq S\) 限制的每个 T。

\[\begin{aligned}(\Delta_i R_d)(T)&=R_d(T\cup\{i\})-R_d(T)\\&=\left(\sum_{U\subseteq T}d(U)+\sum_{U\subseteq T}d(U\cup\{i\})\right)-\sum_{U\subseteq T}d(U)\\&=\sum_{U\subseteq T}e(U)=R_e(T),\qquad T\subseteq S.\end{aligned}\]

依据：\(i\notin T\)；子集拆分；相同有限和消去；e 与 \(R_e\) 的定义。

## 辅助引理：从局部一致性完成插入步骤

<a id="step-3"></a>

先用重构证明中的插入交互引理，得到 \(I_{R_d}(S\cup \{i\})=I_{\Delta_i R_d}(S)\)。交互 \(I_h(S)\) 只读取 h 在 S 的子集上的值；第二步已经逐个证明 \(\Delta_i R_d(T)=R_e(T)\)，故两种函数在这次交替和中的每一项相同。因此 \(I_{\Delta_i R_d}(S)=I_{R_e}(S)\)。最后用“对任意系数函数”的归纳假设，将 \(I_{R_e}(S)\) 化为 \(e(S)=d(S\cup \{i\})\)。这样证明了逆向反演在插入集合上的结论。

\[I_{R_d}(S\cup\{i\})=I_{\Delta_i R_d}(S)=I_{R_e}(S)=e(S)=d(S\cup\{i\})\]

依据：插入交互引理；交互对参与求和的局部函数值保持一致；加强归纳假设。

## 主证明：将全部掩码的重构假设代入

<a id="step-4"></a>

现在恢复假设 ∀T，\(R_d(T)=g(T)\)。固定任意 S。由刚证完的逆向反演，\(d(S)=I_{R_d}(S)\)。在定义 \(I_{R_d}(S)\) 的有限和中，每个 U 都满足 \(U\subseteq S\)，重构假设给出 \(R_d(U)=g(U)\)。逐项替换后，该和就是 \(I_g(S)\)。因此 \(d(S)=I_g(S)\)。这一步使用的是同一组 d 在所有掩码上的假设，而不是每个 S 临时选一组系数。

\[d(S)=I_{R_d}(S)=\sum_{U\subseteq S}(-1)^{|S|-|U|}R_d(U)=\sum_{U\subseteq S}(-1)^{|S|-|U|}g(U)=I_g(S)\]

依据：逆向反演与逐个子集上的重构假设。

## 主证明：逐点相等与适用范围

<a id="step-5"></a>

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

公共系数唯一性及其实际依赖的逆向反演；论文有限总体量词见独立适配。

声明：`Harsanyi.reconstruction_unique`, `Harsanyi.interaction_reconstruct`

报告：`research/reader-v2-20260930/math/verification/report.json`。

## 文字到 Lean 对照

数学上的有限子集族用 Finset 表示；库要求可判定相等关系。论文适配取 Fin n，使 ∀ S : Finset (Fin n) 恰好遍历固定总体的全部掩码。T⊆S 保证指数中的自然数减法没有截断。库源码中的 h1/h2 是插入基数和符号计算；generalizing v/d 保持对任意函数的加强归纳；funext 实现逐点相等。编译检查形式陈述，定义与论文语义的对应仍须人工核对。

- step-1：`Harsanyi.interaction_reconstruct`，`lean/HarsanyiLib/Harsanyi/Core/Mobius.lean:51`。interaction_reconstruct 对 S 归纳并 generalizing d；这一步为其 empty 分支。

- step-1：`Harsanyi.interaction_empty`，`lean/HarsanyiLib/Harsanyi/Core/Basic.lean:30`。reused_exact_declaration

- step-2：`Harsanyi.interaction_reconstruct`，`lean/HarsanyiLib/Harsanyi/Core/Mobius.lean:51`。库证明中的局部 h 使用 sum_powerset_insert；e 在代码中是 fun T => d (insert i T)。

- step-3：`Harsanyi.interaction_insert`，`lean/HarsanyiLib/Harsanyi/Core/Mobius.lean:8`。reused_exact_declaration

- step-3：`Harsanyi.interaction_congr`，`lean/HarsanyiLib/Harsanyi/Core/Basic.lean:39`。这里只要求在 S 的所有子集上相同，不要求两函数处处相同。

- step-3：`Harsanyi.interaction_reconstruct`，`lean/HarsanyiLib/Harsanyi/Core/Mobius.lean:51`。库证明的 rw [h, ih] 完成该辅助引理。

- step-4：`Harsanyi.reconstruction_unique`，`lean/HarsanyiLib/Harsanyi/Core/Mobius.lean:66`。reconstruction_unique 中先改写 interaction_reconstruct，再用 interaction_congr 将 h T 代入。

- step-5：`Harsanyi.reconstruction_unique`，`lean/HarsanyiLib/Harsanyi/Core/Mobius.lean:66`。funext S 在声明开头说明函数相等的含义。

- step-5：`ReaderV2.cvpr_unique_coefficients`，`research/reader-v2-20260930/math/lean/ReaderAdapters.lean:23`。真实适配的 faithful 量词是 ∀ S : Finset (Fin n)，不会要求总体外集合。

## 边界说明

- 本结果约束的是固定模型/样本/基线下，使用相同 AND 激活规则的系数；不是在声称所有解释框架、因果模型或 AND-OR 分解都唯一。

- 原论文按 |S| 归纳；现有库以逆向反演证明唯一性。本文完整展开的是库实际采用的方法。

- 每个子集都要重构，包含空集。只拟合完整输入或仅近似拟合时，不能调用这个精确唯一性结论。

