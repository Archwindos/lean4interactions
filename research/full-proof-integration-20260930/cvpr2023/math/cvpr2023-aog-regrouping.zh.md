# AOG：共享AND子模式的等价重组

固定有限总体 $N$、输入 $x$ 与输入基线向量 $r$。掩码 $x_S$ 在 $S$ 内保留原坐标、在其余坐标使用同一个 $r$。模型是 $v:X\to\mathbb R$，集合函数是 $g(S)=v(x_S)$，输出基线是 $b=g(\varnothing)$。本文原始交互为
\[
w_A=I_g(A)=\sum_{U\subseteq A}(-1)^{|A|-|U|}g(U).
\]
所有子集求和包括空集。特别地 $w_\varnothing=b$。若改用 $g_0=g-b$，只有空集交互改为零；本篇的原始输出没有零基线假设。

\[A=\bigcup_{c\in\mathcal C}V_c\ \Rightarrow\ C_A(x_T)=\prod_{c\in\mathcal C}C_{V_c}(x_T),\qquad\sum_{A\in\Omega}w_A\prod_{c\in\mathcal C_A}C_{V_c}(x_T)=\sum_{A\in\Omega}w_AC_A(x_T)\]

父模式的变量集合是所有孩子变量集合的并集。有限个孩子的触发乘积等于父触发，故共享子节点的重组保留根输出。

## 两个子AND的合并等式

对有限变量集合 $A,B$ 及保留集合 $T$，$A\cup B\subseteq T$ 当且仅当 $A\subseteq T$ 且 $B\subseteq T$。因此 $C_{A\cup B}(x_T)=C_A(x_T)C_B(x_T)$，即使 $A,B$ 重叠也成立，因为触发值为0或1。

## 反复合并保留全部模式状态和输出

令有限孩子族为 $\mathcal C$，孩子 $c$ 所包含的原变量集合为 $V_c$，父模式为 $A=\bigcup_{c\in\mathcal C}V_c$。对孩子族作插入归纳：空孩子族的并集为空、触发与空积都为1；加入一个孩子后，由二集合并集等式，把父触发拆成该孩子触发乘以其余孩子触发，再应用归纳假设。因此 $C_A(x_T)=\prod_{c\in\mathcal C}C_{V_c}(x_T)$。孩子变量允许重叠，且同一孩子可被多个父模式共享。对每个原模式采用这样的分组，乘积等于原触发；保持原系数 $w_A$ 并逐项累加，根输出相同。

\[C_{\bigcup_{c\in\mathcal C}V_c}(x_T)=\prod_{c\in\mathcal C}C_{V_c}(x_T).\]

## 空集与掩码例子

例如共享节点 $\beta=\{5,6\}$ 把模式 $\{4,5,6\}$ 写成孩子 $\{4\}$ 与 $\beta$。保留 $T=\{4,5\}$ 时两种表示都不触发；保留 $T=\{4,5,6\}$ 时都触发。空模式的触发与空孩子积都为1。这里只证明等价重组；原MDL贪心算法的最优性属于独立问题。

