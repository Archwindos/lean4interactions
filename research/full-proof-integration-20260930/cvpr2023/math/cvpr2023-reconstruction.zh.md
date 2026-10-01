# Theorem 1：重构全部掩码输出

固定有限总体 $N$、输入 $x$ 与输入基线向量 $r$。掩码 $x_S$ 在 $S$ 内保留原坐标、在其余坐标使用同一个 $r$。模型是 $v:X\to\mathbb R$，集合函数是 $g(S)=v(x_S)$，输出基线是 $b=g(\varnothing)$。本文原始交互为
\[
w_A=I_g(A)=\sum_{U\subseteq A}(-1)^{|A|-|U|}g(U).
\]
所有子集求和包括空集。特别地 $w_\varnothing=b$。若改用 $g_0=g-b$，只有空集交互改为零；本篇的原始输出没有零基线假设。

\[\forall S\subseteq N,\quad\sum_{A\subseteq S}I_g(A)=g(S)=v(x_S)\]

展开交互并交换有限双和。除当前保留集合本身以外，每个输出的系数都由正负子集配对消去。

## 把原SCM译为同一组集合系数

固定原输入、模型、基线以后，$C_A(x_S)=1$ 当且仅当 $A\subseteq S$。因此原定理是对同一组 $w_A$、全部 $S\subseteq N$ 的恒等式。输入变量是否统计独立不出现在有限代数的前提中。

## 有限双重求和与区间消去

对固定 $S$ 展开 $w_A$。每对 $L\subseteq A\subseteq S$ 只出现一次，交换有限求和不改变项。固定 $L$ 后，用 $B=A\setminus L\subseteq S\setminus L$ 给出一一对应，且 $|A|-|L|=|B|$。若 $L\ne S$，任选 $i\in S\setminus L$，把 $B$ 按是否含 $i$ 配对，符号相反，内和为零；若 $L=S$，只有 $B=\varnothing$，内和为一。因此只留下 $g(S)$。

\[\sum_{A\subseteq S}w_A=\sum_{L\subseteq S}g(L)\sum_{B\subseteq S\setminus L}(-1)^{|B|}=g(S).\]

## 空集与两个变量核对

$S=\varnothing$ 时只有 $w_\varnothing=b$。取 $g(\varnothing)=7,g(\{1\})=8,g(\{2\})=9,g(\{1,2\})=13$，系数为7,1,2,3；完整输入和为13，空输入为7，单变量输入分别为8和9。

