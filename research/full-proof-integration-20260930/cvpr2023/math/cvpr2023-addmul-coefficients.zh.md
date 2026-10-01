# 二值加乘模型：交互就是激活项的系数

固定有限总体 $N$、输入 $x$ 与输入基线向量 $r$。掩码 $x_S$ 在 $S$ 内保留原坐标、在其余坐标使用同一个 $r$。模型是 $v:X\to\mathbb R$，集合函数是 $g(S)=v(x_S)$，输出基线是 $b=g(\varnothing)$。本文原始交互为
\[
w_A=I_g(A)=\sum_{U\subseteq A}(-1)^{|A|-|U|}g(U).
\]
所有子集求和包括空集。特别地 $w_\varnothing=b$。若改用 $g_0=g-b$，只有空集交互改为零；本篇的原始输出没有零基线假设。

\[v(z)=\sum_{A\in\mathcal P}c_A\prod_{i\in A}z_i,\quad r=0\ \Rightarrow\ I_{S\mapsto v(x_S)}(B)=\begin{cases}c_B\prod_{i\in B}x_i&B\in\mathcal P,\\0&B\notin\mathcal P.\end{cases}\]

先从实际零基线坐标掩码证明每个乘积项是纯AND响应，再按交互线性性合并；系数由原样本中的乘积决定。

## 固定二值样本后的每一项

原坐标 $x_i\in\{0,1\}$，输入基线为零。对一个项 $c_A\prod_{i\in A}x_i$，若 $A\subseteq S$，掩码保留全部因子；否则有某个因子被置零。因此该项在实际掩码 $x_S$ 上等于 $c_A\bigl(\prod_{i\in A}x_i\bigr)\mathbf1_{A\subseteq S}$。样本中任一因子为零使该项系数为零；空项的空积为1。相同变量集合的原项先合并系数。

## 逐项纯AND交互再线性合并

记不同变量集合构成有限族 $\mathcal P$，且 $v(z)=\sum_{A\in\mathcal P}c_A\prod_{i\in A}z_i$。上一坐标掩码等式把实际 $g(S)=v(x_S)$ 转成纯AND函数之和。每个纯AND响应的交互只在自身集合 $A$ 非零；有限和的线性性说明固定 $B$ 只收到 $A=B$ 的项。因此 $I_g(B)=c_B\prod_{i\in B}x_i$（若 $B\in\mathcal P$），否则为零。

\[I_g(B)=\begin{cases}c_B\prod_{i\in B}x_i&B\in\mathcal P,\\0&B\notin\mathcal P.\end{cases}\]

## 原文两样本与边界

补充第14页的模型为 $v(x)=3x_1-2x_2x_3-x_3x_4x_5+5x_4x_6$。在 $x=(1,1,1,1,1,1)$，非零交互逐一为 $w_{\{1\}}=3$、$w_{\{2,3\}}=-2$、$w_{\{3,4,5\}}=-1$、$w_{\{4,6\}}=5$。在 $x=(1,1,0,1,1,1)$，只剩 $w_{\{1\}}=3$ 和 $w_{\{4,6\}}=5$。完整输出分别为5和8；两例空掩码输出及空交互均为零。这是原加乘响应的精确系数说明。

