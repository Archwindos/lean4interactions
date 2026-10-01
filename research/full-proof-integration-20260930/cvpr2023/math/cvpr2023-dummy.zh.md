# Dummy：原命题空集反例（不修改）

固定有限总体 $N$、输入 $x$ 与输入基线向量 $r$。掩码 $x_S$ 在 $S$ 内保留原坐标、在其余坐标使用同一个 $r$。模型是 $v:X\to\mathbb R$，集合函数是 $g(S)=v(x_S)$，输出基线是 $b=g(\varnothing)$。本文原始交互为
\[
w_A=I_g(A)=\sum_{U\subseteq A}(-1)^{|A|-|U|}g(U).
\]
所有子集求和包括空集。特别地 $w_\varnothing=b$。若改用 $g_0=g-b$，只有空集交互改为零；本篇的原始输出没有零基线假设。

\[[\forall S\subseteq N\setminus\{i\},\;g(S\cup\{i\})=g(S)+g(\{i\})]\Rightarrow\forall S\subseteq N\setminus\{i\},\;I_g(S\cup\{i\})=0\]

原量词包括空环境，单变量模型满足加法前提却有非零单变量交互，直接反驳原命题。

## 原量词下的完整反例

取 $N=\{i\},g(\varnothing)=0,g(\{i\})=1$。只有 $S=\varnothing$，前提为 $1=0+1$，结论为 $I_g(\{i\})=0$。实际交互按定义为 $1-0=1$，因此原命题不成立。这里不增加“非空S”条件，也不把库的无效变量版本interaction_dummy当作原论文Dummy。

