# Theorem 1：同一组因果效应重构全部掩码输出

本页范围：Theorem 1 exact finite-mask reconstruction。

## 正式来源

- CVPR 2023 正式正文，PDF 页 3,4：Theorem 1；Eq.(2) 与掩码 Eq.(4) 起点; 掩码 Eq.(4) 后的子集和解释。来源文件：`research/paper-survey-20260930/earlier/venue-papers/sparse-cvpr2023-main/sparse-cvpr2023-main.pdf`。

- CVPR 2023 正式补充材料，PDF 页 2,3：Appendix C Theorem 1 与唯一性重述; Appendix C necessity/sufficiency 完整证明。来源文件：`research/paper-survey-20260930/earlier/venue-papers/sparse-cvpr2023-supp/sparse-cvpr2023-supp.pdf`。

## 命题

\[w_A:=\sum_{T\subseteq A}(-1)^{|A|-|T|}v(x_T),\qquad\forall S\subseteq N,\quad Y(x_S)=\sum_{A\subseteq S}w_A=v(x_S)\]

## 必要定义与适用条件

固定一个模型 v、一个原始输入 x 和一组输入基线 r。为每个 \(S\subseteq N\) 使用同一规则构造 \(x_S\)，输出 \(v(x_S)\) 是有限实数。

\[N=\{1,\ldots,n\},\quad v(x_S)\in\mathbb R\]

讨论同一有限总体 N 的全部子集，包含空集；不要求不同掩码输入必须互不相同，也不要求输入变量统计独立。

\[S\subseteq N\]

本条精确结论使用全部模式 Ω=\(2^N\)，每个模式 A 的激活规则是所有 A 中变量都保留时贡献 \(w_A\)。

\[\Omega=2^N,\quad C_A(x_S)=\mathbf1_{A\subseteq S}\]

论文模型仍以样本为自变量；g 只是固定 x 和 r 后的集合函数。输入基线向量 r 与输出基线 \(v(x_\varnothing )\) 要分开。

\[g(S):=v(x_S),\qquad (x_S)_i=\begin{cases}x_i&i\in S,\\r_i&i\notin S.\end{cases}\]

本篇直接对原始模型输出作交互变换，包含空集模式。

\[w_A=I_g(A),\quad w_\varnothing=v(x_\varnothing)\]

在掩码输入 \(x_S\) 上，把所有已触发模式的效应相加。

\[Y(x_S):=\sum_{A\subseteq N}w_A\mathbf1_{A\subseteq S}=\sum_{A\subseteq S}w_A\]

## 证明思路

先把论文的掩码输出和 AND 模式激活准确变成集合函数及子集和，再使用下方完整公共重构证明。原文没有假设 \(v(x_\varnothing )\)=0；空集模式给出的常数项正好承载这个输出基线。

## 将激活规则化成子集求和

<a id="step-1"></a>

固定一个待解释的掩码 S。模式 A 被触发当且仅当 \(A\subseteq S\)，所以求和中 \(A\nsubseteq S\) 的指示函数为 0、\(A\subseteq S\) 的为 1，\(Y(x_S)\) 就是 \(\sum _{A\subseteq S}w_A\)。\(A=\varnothing\) 是 S 的子集，空乘积约定给出其激活值为 1，因此空集效应始终贡献；不能把它删掉。

\[Y(x_S)=\sum_{A\subseteq N}w_A\mathbf1_{A\subseteq S}=\sum_{A\subseteq S}w_A\]

依据：原文 SCM 输出与 AND 激活的确定性求和语义。

## 对齐集合函数与有限总体

<a id="step-2"></a>

定义 \(g(S)=v(x_S)\)。由于 x、基线与模型都固定，这确实是定义在 \(2^N\) 上的同一个实值函数。将 \(g(T)=v(x_T)\) 代入交互定义，论文的 \(w_A\) 就逐项等于 \(I_g(A)\)。

\[g(S)=v(x_S),\qquad w_A=I_g(A)\]

依据：定义逐项一致；Fin n 表示固定有限总体。

## 应用完整公共重构证明

<a id="step-3"></a>

下方公共证明说明，对任意实值集合函数 g 以及任意有限 S，\(\sum _{A\subseteq S}I_g(A)=g(S)\)。将第二步的定义代入，并结合第一步得到 \(Y(x_S)=v(x_S)\)。该结论对所有 S 同时成立，而不是为每个掩码重新选一组权重。特别 \(S=\varnothing\) 时两边等于 \(v(x_\varnothing )\)，并非一般等于 0。

\[Y(x_S)=\sum_{A\subseteq S}w_A=\sum_{A\subseteq S}I_g(A)=g(S)=v(x_S)\]

依据：公共重构定理；定义代入。

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

取两个变量 \(N=\{1,2\}\)，固定四个模型输出：\(v(x_\varnothing)=2\)、\(v(x_{\{1\}})=5\)、\(v(x_{\{2\}})=7\)、\(v(x_{\{1,2\}})=13\)。于是
\[I_g(\varnothing)=2,\quad I_g(\{1\})=5-2=3,\quad I_g(\{2\})=7-2=5,\]
\[I_g(\{1,2\})=13-5-7+2=3.\]
在完整输入上，\(2+3+5+3=13\)；仅保留变量 1 时，\(2+3=5\)；全掩码时求和只有空集项 2。后三个检查说明同一组系数要同时重构全部掩码输出。

## Lean 检查范围

仅验证 Theorem 1 的有限掩码子集和恒等式；原文因果解释与具体 DNN 运行不由 Lean 检查。

声明：`ReaderV2.cvpr_reconstruction`

报告：`research/reader-v2-20260930/math/verification/report.json`。

## 文字到 Lean 对照

数学上的有限子集族用 Finset 表示；库要求可判定相等关系。论文适配取 Fin n，使 ∀ S : Finset (Fin n) 恰好遍历固定总体的全部掩码。T⊆S 保证指数中的自然数减法没有截断。库源码中的 h1/h2 是插入基数和符号计算；generalizing v/d 保持对任意函数的加强归纳；funext 实现逐点相等。编译检查形式陈述，定义与论文语义的对应仍须人工核对。

- step-2：`ReaderV2.cvpr_reconstruction`，`research/reader-v2-20260930/math/lean/ReaderAdapters.lean:18`。适配以真实模型输出函数 v 和真实类型的 mask 参数陈述有限子集和；具体 DNN/掩码实现不在验证范围。

- step-3：`Harsanyi.reconstruction`，`lean/HarsanyiLib/Harsanyi/Core/Mobius.lean:34`。reused_exact_declaration

- step-3：`ReaderV2.cvpr_reconstruction`，`research/reader-v2-20260930/math/lean/ReaderAdapters.lean:18`。真实代码只复用整条 reconstruction；辅助推导在下方公共证明与库源码中展开。

## 边界说明

- 正文本次代理已核对数学适配与正式 main/supp；Lean 编译检查给出的形式陈述，不自动保证译文或论文解释正确。

- 精确重构以 Ω=\(2^N\) 为前提；论文后续稀疏模式的近似效果未在此条证明。

- 第一步的指示函数模型语义已人工核对，但本轮 adapter 从等价子集和开始，没有新增一个因果图概率分布的 Lean 模型。

## 原证明路线与本重写的关系

原文先交换有限双重求和，把每个输出 \(v(x_L)\) 的系数集中起来：
\[\sum_{T\subseteq S}w_T=\sum_{L\subseteq S}v(x_L)\sum_{L\subseteq T\subseteq S}(-1)^{|T|-|L|}.\]
固定 \(L\subseteq S\)，将 T 唯一写成 L∪Q，\(Q\subseteq S\)\L，内层便成为 \(\sum_{Q\subseteq S\setminus L}(-1)^{|Q|}\)。若 \(L=S\)，只有 \(Q=\varnothing\)，系数为 1。若 \(L\subsetneq S\)，选一个 j∈S\L；把 Q 按不含/含 j 配对，两项符号相反且绝对值相同，内层总和为 0。于是只有 \(L=S\) 的 \(v(x_S)\) 留下。这是原文二项恒等式 \(\sum_{m=0}^{k}\binom{k}{m}(-1)^m=(1-1)^k\) 的具体理由；k=0 时系数是 1，不能写成 0。

上面是原文计算路线的完整中文解释；公共 Lean 当前采用下面展开的插入归纳路线，没有为这份双重求和解释另增一个 Lean 声明。

