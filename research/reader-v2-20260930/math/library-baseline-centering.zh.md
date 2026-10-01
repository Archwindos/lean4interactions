# 公共结果：空集交互与去基线转换

本页范围：Explicit raw/centered convention conversion。

## 命题

\[g_0(S):=g(S)-g(\varnothing),\quad I_g(\varnothing)=g(\varnothing),\quad I_{g_0}(\varnothing)=0,\quad S\ne\varnothing\Longrightarrow I_{g_0}(S)=I_g(S)\]

## 必要定义与适用条件

S 是有限变量集合。g 与 d 是定义在有限变量子集上的任意实值函数；不要求连续、可微、独立性或零输出基线。

\[g,d:\mathcal P_{\mathrm{fin}}(U)\to\mathbb R\]

U 表示变量总体，\(\mathcal P_{\mathrm{fin}}(U)\) 表示其所有有限子集。每次参与求和的 S、T 都有限；变量总体本身可以无限。论文应用则固定有限总体 N，只讨论 \(2^N\)。

\[S\in\mathcal P_{\mathrm{fin}}(U)\]

交互是有限交替和。\(T\subseteq S\) 保证 |T|≤|S|，因此指数 \(|S|-|T|\) 是非负整数。

\[I_g(S):=\sum_{T\subseteq S}(-1)^{|S|-|T|}g(T)\]

\(R_d\) 是在给定保留变量集 S 上累加所有被激活的系数。

\[R_d(S):=\sum_{T\subseteq S}d(T)\]

插入差分比较保留 i 与掩码 i 两种状态。下面的插入引理只在 \(i\notin S\) 时使用。

\[(\Delta_i g)(T):=g(T\cup\{i\})-g(T)\]

模型输出基线取为标量 b=\(g(\varnothing )=v(x_\varnothing )\)。把它作为常数函数从 g 的每一个值中减去。

\[g_0(S):=g(S)-b,\qquad b:=g(\varnothing)=v(x_\varnothing)\]

## 证明思路

空集交互承载常数基线。把每个模型输出都减去同一个 \(v(x_\varnothing )\)，只会去掉这个空集项，任何非空交互都保留。这是公共库的记号转换结果，服务于不同论文约定的比较，不冒充某篇论文新定理。

## 直接计算两个空集值

<a id="step-1"></a>

空集只有一个子集，指数为 0，所以 \(I_g(\varnothing )=g(\varnothing )=v(x_\varnothing )\)。另一方面，\(g_0(\varnothing )=g(\varnothing )−g(\varnothing )\)=0，因此 \(I_{g_0}(\varnothing )\)=0。两个交互变换作用于不同的集合函数；不能从后一个零值推出原始模型输出为零。

\[I_g(\varnothing)=v(x_\varnothing),\qquad g_0(\varnothing)=I_{g_0}(\varnothing)=0\]

依据：空集的子集族、(−1)^0=1 与同一数相减。

## 常数函数的非空交互为什么消失

<a id="step-2"></a>

设 c(T)=b 为常数函数。若 \(S=\varnothing\)，它的交互等于 b。若 S 非空，选 \(i\in S\) 并令 \(S'=S\setminus \{i\}\)，则 \(i\notin S'\)。插入交互引理给出 \(I_c(S)=I_{\Delta_i c}(S')\)。由于 c(\(T\cup \{i\}\))−c(T)=b−b=0，Δᵢc 是零函数，定义中的每一项都为零。因此非空常数交互为零。这个论证也覆盖单变量 S，此时 \(S'=\varnothing\)。

\[I_c(S)=\begin{cases}b&S=\varnothing,\\0&S\ne\varnothing.\end{cases}\]

依据：插入交互引理与常数差分为零。

## 逐项线性性把去基线化成两种情况

<a id="step-3"></a>

去基线函数是 \(g_0=g-c\)。交互定义是有限线性和，因此 \(I_{g_0}(S)=I_g(S)−I_c(S)\)。把第二步的常数交互公式代入：空集时减去 b，结果是 0；非空时减去 0，结果与 \(I_g(S)\) 完全相同。这里必须保留非空条件；在空集上，原交互与去基线交互的值一般不同。

\[I_{g_0}(S)=I_g(S)-\mathbf1_{S=\varnothing}g(\varnothing)\]

依据：交互变换对差值的线性性、常数交互公式。

## 重构式的两种写法都加回同一个基线

<a id="step-4"></a>

把公共重构定理用于 \(g_0\)，得到 \(\sum _{T\subseteq S}I_{g_0}(T)=g_0(S)=g(S)−g(\varnothing )\)，两侧加回 \(g(\varnothing )\) 就得到第一种写法。由于空集交互为零而非空交互不变，也可把它写成第二种只求非空子集和的式子。

若 \(S=\varnothing\)，第一式的交互总和为 0，第二式的非空子集族为空、和也为 0，两式都还原为 \(g(\varnothing )=v(x_\varnothing )\)。这说明删去空集项必须明确补回基线。

\[\begin{aligned}v(x_S)&=v(x_\varnothing)+\sum_{T\subseteq S}I_{g_0}(T)\\&=v(x_\varnothing)+\sum_{\varnothing\ne T\subseteq S}I_g(T).\end{aligned}\]

依据：公共重构；分离空集求和项；去基线的非空交互不变性。

## 小例子与空集

沿用 \(v(x_\varnothing)=2\)、\(v(x_{\{1\}})=5\)、\(v(x_{\{2\}})=7\)、\(v(x_{\{1,2\}})=13\)。去基线后的函数值分别为 \(0,3,5,11\)，对应交互分别为 \(0,3,5,3\)。非空交互与未去基线时一致。
\[v(x_{\{1,2\}})=2+(0+3+5+3)=13.\]
这里为零的是 \(g_0(\varnothing)\) 和 \(I_{g_0}(\varnothing)\)，模型原始输出 \(v(x_\varnothing)\) 始终是 2。

## Lean 检查范围

公共空集/去基线结果的真实模型输出记号适配；不是新论文定理。

声明：`ReaderV2.masked_empty`, `ReaderV2.sparse_empty`, `ReaderV2.baseline_nonempty_agreement`, `ReaderV2.baseline_explicit_reconstruction`

报告：`research/reader-v2-20260930/math/verification/report.json`。

## 文字到 Lean 对照

数学上的有限子集族用 Finset 表示；库要求可判定相等关系。论文适配取 Fin n，使 ∀ S : Finset (Fin n) 恰好遍历固定总体的全部掩码。T⊆S 保证指数中的自然数减法没有截断。库源码中的 h1/h2 是插入基数和符号计算；generalizing v/d 保持对任意函数的加强归纳；funext 实现逐点相等。编译检查形式陈述，定义与论文语义的对应仍须人工核对。

- step-1：`Harsanyi.interaction_empty`，`lean/HarsanyiLib/Harsanyi/Core/Basic.lean:30`。reused_exact_declaration

- step-1：`Harsanyi.centered_empty`，`lean/HarsanyiLib/Harsanyi/Core/Basic.lean:36`。reused_exact_declaration

- step-1：`ReaderV2.masked_empty`，`research/reader-v2-20260930/math/lean/ReaderAdapters.lean:13`。paper_adapter

- step-1：`ReaderV2.sparse_empty`，`research/reader-v2-20260930/math/lean/ReaderAdapters.lean:38`。paper_adapter

- step-2：`Harsanyi.interaction_const`，`lean/HarsanyiLib/Harsanyi/Core/Properties.lean:23`。现有常数交互证明同样使用插入差分为零的机制。

- step-3：`Harsanyi.interaction_centered`，`lean/HarsanyiLib/Harsanyi/Core/Properties.lean:32`。reused_exact_declaration

- step-3：`Harsanyi.interaction_centered_nonempty`，`lean/HarsanyiLib/Harsanyi/Core/Properties.lean:37`。reused_exact_declaration

- step-3：`ReaderV2.baseline_nonempty_agreement`，`research/reader-v2-20260930/math/lean/ReaderAdapters.lean:43`。该 adapter 明确要求 S.Nonempty。

- step-4：`ReaderV2.sparse_centered_reconstruction`，`research/reader-v2-20260930/math/lean/ReaderAdapters.lean:29`。paper_adapter

- step-4：`ReaderV2.baseline_explicit_reconstruction`，`research/reader-v2-20260930/math/lean/ReaderAdapters.lean:49`。非空和在真实代码中为 S.powerset.erase ∅，包含 S=∅ 的情形。

## 边界说明

- 项目旧库的函数参数可能名为 v，但其类型是集合函数，本文统一解释为 g；论文模型 v 的类型是输入样本到实数。

- 输入全部置为零基线，也不保证模型输出 \(v(x_\varnothing )\) 为零；二者是不同层次。

- 本页只讨论输出减去常数的转换，不证明如何选择最优输入基线。

