# Appendix C(1)：固定原样本的 AND 分量精确重构

本页范围：Selected Appendix C(1) AND component subresult, not full Theorem 2。

## 正式来源

- ICLR 2024 Generalizable 正式正文及随文附录，PDF 页 2,12,13：Eq.(1)：AND 定义与空集值; Appendix C Eq.(7) 及 Proof(1) 固定 x AND 子结论; Appendix C(1) Eq.(8) AND 推导与 OR proof 起点。来源文件：`research/paper-survey-20260930/recent/pdf/iclr2024-generalizable.pdf`。

## 命题

\[I_{\mathrm{and}}(S\mid x):=\sum_{L\subseteq S}(-1)^{|S|-|L|}v_{\mathrm{and}}(x_L),\qquad\forall T\subseteq N,\quad v_{\mathrm{and}}(x_T)=\sum_{S\subseteq T}I_{\mathrm{and}}(S\mid x)\]

## 必要定义与适用条件

固定一个模型 v、一个原始输入 x 和一组输入基线 r。为每个 \(S\subseteq N\) 使用同一规则构造 \(x_S\)，输出 \(v(x_S)\) 是有限实数。

\[N=\{1,\ldots,n\},\quad v(x_S)\in\mathbb R\]

讨论同一有限总体 N 的全部子集，包含空集；不要求不同掩码输入必须互不相同，也不要求输入变量统计独立。

\[S\subseteq N\]

固定一个实值分量函数 \(v_{\mathrm{and}}\)，并使用与原样本相同的掩码规则。只证明这个分量的恒等式，不要求任何特定的分解优化方法。

\[v_{\mathrm{and}}(x_T)\in\mathbb R\]

为避免把总体模型和分量混淆，令 \(g_{\mathrm{and}}\) 是该固定 AND 分量在所有掩码输入上的输出。

\[g_{\mathrm{and}}(S):=v_{\mathrm{and}}(x_S)\]

附录 C(1) 明确使用固定原样本 x 的系数；它没有先对分量输出去基线。

\[I_{\mathrm{and}}(S\mid x)=I_{g_{\mathrm{and}}}(S),\qquad I_{\mathrm{and}}(\varnothing\mid x)=v_{\mathrm{and}}(x_\varnothing)\]

## 证明思路

本页选的是 Appendix C(1) 自己明确写出的固定 x 的 AND 子结论。它是 Theorem 2 证明中的一个分量，但本页完成状态只覆盖这个子结论。原文引用既有 Harsanyi 重构，并在第 13 页完整重证；下方公共证明展示其严谨理由及实际 Lean 路线。

## 固定 AND 分量与原样本 x

<a id="step-1"></a>

取 \(g_{\mathrm{and}}(S)=v_{\mathrm{and}}(x_S)\)。样本 x、输入基线以及分量函数 \(v_{\mathrm{and}}\) 在全部 S 中固定。附录 C(1) 的交互因此是对 \(g_{\mathrm{and}}\) 的 Harsanyi 变换，空集项等于 \(v_{\mathrm{and}}(x_\varnothing )\)。不要求 \(v_{\mathrm{and}}(x_\varnothing )\)=0。

\[I_{\mathrm{and}}(S\mid x)=I_{g_{\mathrm{and}}}(S)\]

依据：附录 C(1) 的定义逐项一致。

## 对分量函数应用完整重构证明

<a id="step-2"></a>

公共重构定理对任意实值集合函数成立，因此将 g 换为 \(g_{\mathrm{and}}\)，待重构集合换为 T，就得到 \(\sum _{S\subseteq T}I_{g_{\mathrm{and}}}(S)=g_{\mathrm{and}}(T)\)。用第一步定义改回论文记号，恰好是第 12 页的固定 x 子结论。空集 \(T=\varnothing\) 时，只留下 \(I_and(\varnothing |x)=v_{\mathrm{and}}(x_\varnothing )\)，边界仍成立。

\[\sum_{S\subseteq T}I_{\mathrm{and}}(S\mid x)=\sum_{S\subseteq T}I_{g_{\mathrm{and}}}(S)=g_{\mathrm{and}}(T)=v_{\mathrm{and}}(x_T)\]

依据：公共重构定理、固定分量定义与空集交互。

## 复用的完整公共证明

以下公共证明作为整体被复用，论文特有定义已在上文逐项对齐。

### 辅助引理：为什么子集能分成两组

固定有限集合 S 及不属于 S 的变量 i。\(S\cup \{i\}\) 的任何子集 A，要么不含 i，这时 A 本身就是 S 的子集；要么含 i，这时唯一地写成 \(A=T\cup \{i\}\)，其中 \(T=A\setminus \{i\}\subseteq S\)。两类互不重叠，且各自覆盖所有可能情况，所以对任意实值函数 F 可以把有限和改写为下面的两组和。没有遗漏空集：它出现在第一组 \(T=\varnothing\)；第二组 \(T=\varnothing\) 对应 {i}。

\[\sum_{A\subseteq S\cup\{i\}}F(A)=\sum_{T\subseteq S}F(T)+\sum_{T\subseteq S}F(T\cup\{i\})\]

依据：子集与不含/含 i 两类的显式一一对应。

### 辅助引理：展开符号，得到插入差分

把上一步用于交互 \(I_g(S\cup \{i\})\) 的定义。每个 \(T\subseteq S\) 都满足 \(i\notin T\)，因此 \(|S\cup \{i\}|=|S|+1\)、\(|T\cup \{i\}|=|T|+1\)。令 \(k=|S|-|T|\ge 0\)：第一组的系数是 \((-1)^{k+1}=-(-1)^k\)；第二组的系数是 \((-1)^k\)。把同一 T 的两项合并，得到 \((-1)^k\)[\(g(T\cup \{i\})−g(T)\)]。最后一行正是 \(I_{\Delta_i g}(S)\) 的定义。

\[\begin{aligned}I_g(S\cup\{i\})&=\sum_{T\subseteq S}(-1)^{|S|+1-|T|}g(T)+\sum_{T\subseteq S}(-1)^{|S|-|T|}g(T\cup\{i\})\\&=\sum_{T\subseteq S}(-1)^{|S|-|T|}\bigl(g(T\cup\{i\})-g(T)\bigr)\\&=I_{\Delta_i g}(S).\end{aligned}\]

依据：\(i\notin S\) 及 \(T\subseteq S\) 给出两个插入基数；整数幂的递推关系给出负号；有限和逐项相加。

### 主证明：加强归纳命题，并处理空集

对有限集合 S 作插入归纳，但归纳命题必须说“对任意集合函数 g 都有 \(R_{I_g}(S)=g(S)\)”。不能只固定最初的 g 后归纳，因为插入一步还要对新函数 \(\Delta_i g\) 使用归纳假设。

当 \(S=\varnothing\) 时，空集只有一个子集，即自身。定义中的指数是 0，(−1)^0=1，所以 \(I_g(\varnothing )=g(\varnothing )\)，而重构和也只有这一项。这是归纳起点；无需且不能在这里默默令 \(g(\varnothing )\)=0。

\[R_{I_g}(\varnothing)=I_g(\varnothing)=(-1)^0g(\varnothing)=g(\varnothing)\]

依据：有限集合插入归纳；空集的子集族只有空集本身；空集交互公式。

### 主证明：对两组和分别使用归纳假设

现在设 \(i\notin S\)，并假设任意函数 h 在 S 上都满足 \(R_{I_h}(S)\)=h(S)。第一步的拆分把 \(S\cup \{i\}\) 上的重构和写成两组。对第二组中的每个 \(T\subseteq S\)，仍有 \(i\notin T\)，所以第二步的插入交互引理可以逐项使用。得到的第二组是 \(\Delta_i g\) 在 S 上的交互总和。对第一组用归纳假设 h=g，对第二组用归纳假设 h=\(\Delta_i g\)，便分别得到 \(g(S)\) 与 \(\Delta_i g(S)\)。这里明确使用了两次同一个归纳假设，而不是假设差分的结论未经证明成立。

\[\begin{aligned}R_{I_g}(S\cup\{i\})&=\sum_{T\subseteq S}I_g(T)+\sum_{T\subseteq S}I_g(T\cup\{i\})\\&=R_{I_g}(S)+R_{I_{\Delta_i g}}(S)\\&=g(S)+(\Delta_i g)(S).\end{aligned}\]

依据：子集拆分；插入交互引理逐项使用；加强归纳假设适用于任意集合函数。

### 主证明：消去中间输出，完成归纳

按插入差分的定义，\(\Delta_i g(S)=g(S\cup \{i\})-g(S)\)。将其代入上一步，\(g(S)\) 与 −\(g(S)\) 在实数加法中消去，得到所需的 \(g(S\cup \{i\})\)。空集起点与每次插入的步骤已经覆盖所有有限 S，因此对任意有限 S 的重构恒等式成立。论文中只需把这里的 \(g(S)\) 换成固定模型和掩码规则给出的 \(v(x_S)\)。

\[g(S)+(\Delta_i g)(S)=g(S)+g(S\cup\{i\})-g(S)=g(S\cup\{i\})\]

依据：插入差分定义与实数加减法；有限集合归纳结论。

## 小例子与空集

取两个变量 \(N=\{1,2\}\)，固定四个AND 分量输出：\(v_{\mathrm{and}}(x_\varnothing)=2\)、\(v_{\mathrm{and}}(x_{\{1\}})=5\)、\(v_{\mathrm{and}}(x_{\{2\}})=7\)、\(v_{\mathrm{and}}(x_{\{1,2\}})=13\)。于是
\[I_g(\varnothing)=2,\quad I_g(\{1\})=5-2=3,\quad I_g(\{2\})=7-2=5,\]
\[I_g(\{1,2\})=13-5-7+2=3.\]
在完整输入上，\(2+3+5+3=13\)；仅保留变量 1 时，\(2+3=5\)；全掩码时求和只有空集项 2。后三个检查说明同一组系数要同时重构全部掩码输出。

## Lean 检查范围

只验证正式附录 C(1) 的固定 x AND 分量子结论。完整 Theorem 2、OR 推导及 AND-OR 分解未被该报告覆盖。

声明：`ReaderV2.generalizable_and_subresult`

报告：`research/reader-v2-20260930/math/verification/report.json`。

## 文字到 Lean 对照

数学上的有限子集族用 Finset 表示；库要求可判定相等关系。论文适配取 Fin n，使 ∀ S : Finset (Fin n) 恰好遍历固定总体的全部掩码。T⊆S 保证指数中的自然数减法没有截断。库源码中的 h1/h2 是插入基数和符号计算；generalizing v/d 保持对任意函数的加强归纳；funext 实现逐点相等。编译检查形式陈述，定义与论文语义的对应仍须人工核对。

- step-1：`ReaderV2.generalizable_and_subresult`，`research/reader-v2-20260930/math/lean/ReaderAdapters.lean:59`。实际参数名 vAnd 明确是分量；适配没有为 OR 分量或全部模型作任何验证声明。

- step-2：`Harsanyi.reconstruction`，`lean/HarsanyiLib/Harsanyi/Core/Mobius.lean:34`。reused_exact_declaration

- step-2：`ReaderV2.generalizable_and_subresult`，`research/reader-v2-20260930/math/lean/ReaderAdapters.lean:59`。真实编译的声明精确是此选定固定 x AND 子结论。

## 边界说明

- 这是一条已完成的选定子结论，不是完整 Theorem 2 的完成标记。

- 正文 Theorem 2 使用 \(I(S|x_T)\)，而附录 C(1) 定义与子结论使用固定 x；全文记号语义仍单列对齐说明，不在此页静默改写。

- OR 原证明第 14 页的中间求和疑点单列待用户确认；它不影响本页第 12–13 页 AND 子结论的对齐，也不能被本页编译通过所关闭。

## 原证明路线与本重写的关系

正式 PDF 第 12–13 页将 AND 定义代入子集和，按 L 集中 \(v_{\mathrm{and}}(x_L)\) 的系数。若 \(L=T\)，系数为 1；若 \(L\subsetneq T\)，系数为 \((1-1)^{|T|-|L|}=0\)，故只剩 \(v_{\mathrm{and}}(x_T)\)。第 13 页 Eq.(8) 给出结果。
\[\sum_{S\subseteq T}I_{\mathrm{and}}(S\mid x)=\sum_{L\subseteq T}v_{\mathrm{and}}(x_L)\sum_{L\subseteq S\subseteq T}(-1)^{|S|-|L|}=v_{\mathrm{and}}(x_T).\]
这是本页对齐的原证明范围。附录同页起接下来的 OR 推导及全文 Theorem 2 不在已完成范围内。

