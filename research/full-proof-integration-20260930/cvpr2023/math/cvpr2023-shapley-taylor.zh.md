# Theorem 4：Shapley–Taylor 的全部阶数分支

固定有限总体 $N$、输入 $x$ 与输入基线向量 $r$。掩码 $x_S$ 在 $S$ 内保留原坐标、在其余坐标使用同一个 $r$。模型是 $v:X\to\mathbb R$，集合函数是 $g(S)=v(x_S)$，输出基线是 $b=g(\varnothing)$。本文原始交互为
\[
w_A=I_g(A)=\sum_{U\subseteq A}(-1)^{|A|-|U|}g(U).
\]
所有子集求和包括空集。特别地 $w_\varnothing=b$。若改用 $g_0=g-b$，只有空集交互改为零；本篇的原始输出没有零基线假设。

\[I_g^{\rm ST(k)}(T)=\begin{cases}I_g(T)&|T|<k,\\\sum_{U\subseteq N\setminus T}\binom{|U|+k}k^{-1}I_g(T\cup U)&|T|=k,\\0&|T|>k,\end{cases}\]

低于截断阶数的目标保留原交互，高于阶数的目标为零；最高阶目标的有限权重和给出二项系数倒数。

## 低阶和高阶分支

在正整数阶数 $k$ 的定义域内，若 $|T|<k$，环境空集上的差分按定义就是 $w_T$；$T=\varnothing$ 时值为 $b$。若 $|T|>k$，定义直接给零。这两个分支不除以 $n$，也不需要 $n\ge k$。

## 最高阶把原权重化为共有阶乘权重

若 $|T|=k$，由于 $k>0$、$T\subseteq N$，有 $n\ge k\ge1$，除以 $n$ 合法。设 $E=N\setminus T$、$m=n-k$。对 $S\subseteq E$，记 $s=|S|\le m\le n-1$。二项系数的阶乘式给 $\frac{k}{n}\binom{n-1}{s}^{-1}=\frac{k\,s!(n-1-s)!}{n!}=\frac{k\,s!(m+k-1-s)!}{(m+k)!}$，恰好是加权差分引理的权重。$S=\varnothing$ 也在范围内。

## 完整辅助引理：有限阶乘卷积

对任意有限集合 $R$、非负整数 $a,b$，记 $m=|R|$，$F_R(a,b)=\sum_{A\subseteq R}(a+|A|)!(b+m-|A|)!$。对 $R$ 作插入归纳，并加强归纳命题为对所有 $a,b$ 成立。$R=\varnothing$ 时两边都是 $a!b!$。插入新变量 $i\notin R$ 后，按 $A$ 是否含 $i$ 分组得到 $F_{R\cup\{i\}}(a,b)=F_R(a,b+1)+F_R(a+1,b)$。归纳假设给出的两项有共同分母 $(a+b+2)!$ 和共同大阶乘 $(a+b+m+2)!$，小阶乘相加为 $a!(b+1)!+(a+1)!b!=a!b!(a+b+2)$。约去正数 $a+b+2$ 得插入后的公式。全部阶乘为正，除法合法；论证包括 $a=0$、$b=0$、$m=0$。

\[F_R(a,b)=\frac{a!b!(a+b+m+1)!}{(a+b+1)!}.\]

## 完整辅助引理：包含固定子集的权重和

取正整数 $k$、有限环境集合 $E$ 及 $L\subseteq E$。记 $m=|E|$、$l=|L|$、$R=E\setminus L$。每个包含 $L$ 的 $S\subseteq E$ 唯一写成 $L\cup A$，其中 $A\subseteq R$，且 $|S|=l+|A|$、$|R|=m-l$。将上一引理用于 $a=l$、$b=k-1$；利用 $k(k-1)!=k!$ 并约去大阶乘 $(m+k)!$，得到下式，包括 $L=\varnothing$ 和 $L=E$。

\[\sum_{L\subseteq S\subseteq E}\frac{k\,|S|!(m+k-|S|-1)!}{(m+k)!}=\frac{l!k!}{(l+k)!}=\binom{l+k}{k}^{-1}.\]

## 交换有限求和，得到一般加权差分恒等式

若 $T\cap E=\varnothing$，边际分解给 $\Delta_Tg(S)=\sum_{U\subseteq S}w_{T\cup U}$。每对 $U\subseteq S\subseteq E$ 恰好出现一次，交换有限双和。固定 $U$ 后，所有包含它的环境的权重之和由上一引理给出，所以每个 $w_{T\cup U}$ 得到下式中的精确系数。

\[\sum_{S\subseteq E}\frac{k\,|S|!(m+k-|S|-1)!}{(m+k)!}\Delta_Tg(S)=\sum_{U\subseteq E}\binom{|U|+k}{k}^{-1}w_{T\cup U}.\]

## 最高阶应用共有恒等式

差分变量 $T$ 与环境 $E$ 不相交，且 $k>0$，所以一般加权差分引理给出 $\binom{|U|+k}{k}^{-1}$ 的系数。与低于阶数、高于阶数的两个定义分支合并，得到完整三分支结论。

## 空集与两种阶数例子

令 $N=\{1,2\}$，$g(\varnothing)=7$、$g(\{1\})=8$、$g(\{2\})=9$、$g(\{1,2\})=13$。于是 $w_\varnothing=7$、$w_{\{1\}}=1$、$w_{\{2\}}=2$、$w_{\{1,2\}}=3$。 当 $k=1$，空目标值为7，两单变量目标分别为 $5/2$、$7/2$，二变量目标高于 $k$，值为零。当 $k=2$，四个目标的值为7、1、2、3，总和13。若 $N=\varnothing$ 而 $k\ge1$，仅有低阶空目标，值为 $b$。正阶数是当前定义域解释；原文仅写第 $k$ 阶，未显式写出不等式。

