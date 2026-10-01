# SCM：二值AND触发化为子集和

固定有限总体 $N$、输入 $x$ 与输入基线向量 $r$。掩码 $x_S$ 在 $S$ 内保留原坐标、在其余坐标使用同一个 $r$。模型是 $v:X\to\mathbb R$，集合函数是 $g(S)=v(x_S)$，输出基线是 $b=g(\varnothing)$。本文原始交互为
\[
w_A=I_g(A)=\sum_{U\subseteq A}(-1)^{|A|-|U|}g(U).
\]
所有子集求和包括空集。特别地 $w_\varnothing=b$。若改用 $g_0=g-b$，只有空集交互改为零；本篇的原始输出没有零基线假设。

\[Y(x_S)=\sum_{A\in\Omega,\,A\subseteq S}w_A\]

AND触发就是“模式包含于保留集合”的指示。把它代入线性根的有限和，得到被激活模式的系数和。

## 逐项核二值触发

固定保留集合 $S$，令 $X_i=\mathbf1_{i\in S}$。若 $A\subseteq S$，乘积中每个因子为1；否则至少一个因子为0。因此 $C_A(x_S)=\prod_{i\in A}X_i=\mathbf1_{A\subseteq S}$。空积为1，所以空模式始终触发。

## 筛选所有激活模式

将触发等式代入任意有限保留模式族 $\Omega$ 的SCM线性根，不包含于 $S$ 的项为零，其余项保留。因此输出是 $\sum_{A\in\Omega,\,A\subseteq S}w_A$。不要求 $\Omega$ 含全部模式；当 $\Omega=\mathcal P(N)$ 时，该和由重构等于 $g(S)$。

