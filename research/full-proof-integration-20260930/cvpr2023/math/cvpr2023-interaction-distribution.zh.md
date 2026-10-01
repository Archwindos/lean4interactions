# Interaction distribution：纯AND只在指定集合有交互

固定有限总体 $N$、输入 $x$ 与输入基线向量 $r$。掩码 $x_S$ 在 $S$ 内保留原坐标、在其余坐标使用同一个 $r$。模型是 $v:X\to\mathbb R$，集合函数是 $g(S)=v(x_S)$，输出基线是 $b=g(\varnothing)$。本文原始交互为
\[
w_A=I_g(A)=\sum_{U\subseteq A}(-1)^{|A|-|U|}g(U).
\]
所有子集求和包括空集。特别地 $w_\varnothing=b$。若改用 $g_0=g-b$，只有空集交互改为零；本篇的原始输出没有零基线假设。

\[I_{u_T}(S)=\begin{cases}c&S=T,\\0&S\ne T,\end{cases}\qquad u_T(S)=c\,\mathbf1_{T\subseteq S}\]

未包含目标模式时输出全零；恰好目标模式时留下一个系数；严格包含时剩余变量使符号配对消去。

## T不包含于S的所有情形

若 $T\not\subseteq S$，任意 $U\subseteq S$ 都不可能包含 $T$，故 $u_T(U)=0$，每个交互项为零。此情形同时覆盖 $S$ 是 $T$ 的真子集和二者不可比的情况，补齐原证明漏掉的不可比集合。

## S等于T

若 $S=T$，只有 $U=T$ 这一项输出为 $c$，符号为1，其余真子集输出全为零。$T=\varnothing$ 时也只有空集项 $c$。

## T真子集S的消去

若 $T\subsetneq S$，只有包含 $T$ 的 $U$ 可能贡献。令 $B=U\setminus T\subseteq S\setminus T$，这是双射，指数为 $|S\setminus T|-|B|$。差集非空，选其中一个变量，再把含它与不含它的 $B$ 配对，符号相反，全部消去。

\[I_{u_T}(S)=\begin{cases}c&S=T,\\0&S\ne T.\end{cases}\]

## 空集与不可比例子

若 $T=\varnothing$，$u_T$ 是常数 $c$，只有空集交互为 $c$。若 $N=\{1,2\}$、$T=\{1\}$、$c=3$，则 $g(\varnothing)=0$、$g(\{1\})=3$、$g(\{2\})=0$、$g(N)=3$，对应交互为0、3、0、0。原文遗漏的不可比集合 $S=\{2\}$ 已由第一情形处理。

