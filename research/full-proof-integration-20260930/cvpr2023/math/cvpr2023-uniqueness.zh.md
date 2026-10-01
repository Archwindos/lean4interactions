# Appendix C：全部掩码重构系数唯一

固定有限总体 $N$、输入 $x$ 与输入基线向量 $r$。掩码 $x_S$ 在 $S$ 内保留原坐标、在其余坐标使用同一个 $r$。模型是 $v:X\to\mathbb R$，集合函数是 $g(S)=v(x_S)$，输出基线是 $b=g(\varnothing)$。本文原始交互为
\[
w_A=I_g(A)=\sum_{U\subseteq A}(-1)^{|A|-|U|}g(U).
\]
所有子集求和包括空集。特别地 $w_\varnothing=b$。若改用 $g_0=g-b$，只有空集交互改为零；本篇的原始输出没有零基线假设。

\[[\forall S\subseteq N,\;\sum_{A\subseteq S}d_A=g(S)]\Longrightarrow\forall A\subseteq N,\;d_A=I_g(A)\]

空掩码固定常数项；每个较大集合的等式，在减去已固定的真子集系数后，唯一确定当前系数。

## 保留全部掩码与同一组系数

假设 $d_A$ 是一组固定系数，且对每个 $S\subseteq N$（包括空集）都有 $g(S)=\sum_{A\subseteq S}d_A$。只给完整输入等式不能推出唯一性。

## 按集合基数作强归纳

基例 $S=\varnothing$ 给出 $d_\varnothing=g(\varnothing)=w_\varnothing$。强归纳假设是：对所有 $A\subseteq N$ 且 $|A|<|S|$，都有 $d_A=w_A$。每个真子集都满足这个范围。在 $S$ 上分别应用假设的重构与已证重构，减去相同的真子集项，得到 $d_S=w_S$。任意 $S$ 均成立，因此系数逐项唯一。

\[d_S=g(S)-\sum_{A\subsetneq S}d_A=g(S)-\sum_{A\subsetneq S}w_A=w_S.\]

## 空集与必要的量词边界

令 $N=\{1,2\}$，$g(\varnothing)=7$、$g(\{1\})=8$、$g(\{2\})=9$、$g(\{1,2\})=13$。于是 $w_\varnothing=7$、$w_{\{1\}}=1$、$w_{\{2\}}=2$、$w_{\{1,2\}}=3$。 空集等式固定 $d_\varnothing=7$，两个单变量等式固定 $d_{\{1\}}=1$、$d_{\{2\}}=2$，再用完整输入等式固定 $d_{\{1,2\}}=3$。若只知道 $g(N)=13$，把全部系数13放在空集或放在 $N$ 都满足这一个等式，因此不能省略其他掩码。

