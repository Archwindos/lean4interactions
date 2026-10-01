# Theorem 5：环境中的高阶边际分解

固定有限总体 $N$、输入 $x$ 与输入基线向量 $r$。掩码 $x_S$ 在 $S$ 内保留原坐标、在其余坐标使用同一个 $r$。模型是 $v:X\to\mathbb R$，集合函数是 $g(S)=v(x_S)$，输出基线是 $b=g(\varnothing)$。本文原始交互为
\[
w_A=I_g(A)=\sum_{U\subseteq A}(-1)^{|A|-|U|}g(U).
\]
所有子集求和包括空集。特别地 $w_\varnothing=b$。若改用 $g_0=g-b$，只有空集交互改为零；本篇的原始输出没有零基线假设。

\[T\cap S=\varnothing\ \Longrightarrow\ \Delta_Tg(S)=\sum_{U\subseteq S}I_g(T\cup U)\]

重构每个差分输出，再交换有限求和。差分变量没有全部出现的交互被消去，只留下包含全部差分变量的项。

## 在每个掩码输出上使用已证重构

固定差分变量集合 $T$ 与环境集合 $S$，要求 $T\cap S=\varnothing$。对每个 $L\subseteq T$ 重构 $g(L\cup S)$。每个 $K\subseteq L\cup S$ 唯一写成 $A\cup U$，其中 $A=K\cap L\subseteq L$、$U=K\cap S\subseteq S$。因为两总体不相交，这个表示不重复计数。

## 固定环境子集，交换有限求和并配对

按 $U$ 再按 $A$ 分组。固定 $A\subseteq T$，外层 $L$ 唯一写成 $A\cup B$，其中 $B\subseteq T\setminus A$，符号为 $(-1)^{|T|-|A|-|B|}$。若 $A\ne T$，从差集选一个变量把 $B$ 配对消去；若 $A=T$，只有空集 $B$，系数为1。因此每个 $U$ 只留下 $w_{T\cup U}$。

\[\Delta_Tg(S)=\sum_{U\subseteq S}\sum_{A\subseteq T}w_{A\cup U}\sum_{A\subseteq L\subseteq T}(-1)^{|T|-|L|}=\sum_{U\subseteq S}w_{T\cup U}.\]

## 空集与具体差分

令 $N=\{1,2\}$，$g(\varnothing)=7$、$g(\{1\})=8$、$g(\{2\})=9$、$g(\{1,2\})=13$。于是 $w_\varnothing=7$、$w_{\{1\}}=1$、$w_{\{2\}}=2$、$w_{\{1,2\}}=3$。 当 $T=\{1\}$、$S=\{2\}$，差分为 $13-9=4$，右侧 $w_{\{1\}}+w_{\{1,2\}}=1+3=4$。$T=\varnothing$ 时左侧为 $g(S)$，右侧为重构和；$S=\varnothing$ 时两侧都是 $w_T$。

