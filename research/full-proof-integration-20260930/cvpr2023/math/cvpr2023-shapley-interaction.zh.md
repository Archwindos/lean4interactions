# Theorem 3：Shapley interaction 的交互权重

固定有限总体 $N$、输入 $x$ 与输入基线向量 $r$。掩码 $x_S$ 在 $S$ 内保留原坐标、在其余坐标使用同一个 $r$。模型是 $v:X\to\mathbb R$，集合函数是 $g(S)=v(x_S)$，输出基线是 $b=g(\varnothing)$。本文原始交互为
\[
w_A=I_g(A)=\sum_{U\subseteq A}(-1)^{|A|-|U|}g(U).
\]
所有子集求和包括空集。特别地 $w_\varnothing=b$。若改用 $g_0=g-b$，只有空集交互改为零；本篇的原始输出没有零基线假设。

\[I_g^{\rm Shapley}(T)=\sum_{U\subseteq N\setminus T}\frac{I_g(T\cup U)}{|U|+1}\]

把目标集合视为一个整体差分，并对外部变量按原阶乘权重平均；同一有限权重和给出交互系数。

## 保留原阶乘定义与总体外部集合

记 $t=|T|$、$E=N\setminus T$、$m=n-t=|E|$。SII对整体目标 $T$ 的差分使用权重 $|S|!(m-|S|)!/(m+1)!$，不是分别对 $T$ 中的变量分配。原集合范围包括 $T=\varnothing$ 和 $T=N$。

## 完整辅助引理：有限阶乘卷积

对任意有限集合 $R$、非负整数 $a,b$，记 $m=|R|$，$F_R(a,b)=\sum_{A\subseteq R}(a+|A|)!(b+m-|A|)!$。对 $R$ 作插入归纳，并加强归纳命题为对所有 $a,b$ 成立。$R=\varnothing$ 时两边都是 $a!b!$。插入新变量 $i\notin R$ 后，按 $A$ 是否含 $i$ 分组得到 $F_{R\cup\{i\}}(a,b)=F_R(a,b+1)+F_R(a+1,b)$。归纳假设给出的两项有共同分母 $(a+b+2)!$ 和共同大阶乘 $(a+b+m+2)!$，小阶乘相加为 $a!(b+1)!+(a+1)!b!=a!b!(a+b+2)$。约去正数 $a+b+2$ 得插入后的公式。全部阶乘为正，除法合法；论证包括 $a=0$、$b=0$、$m=0$。

\[F_R(a,b)=\frac{a!b!(a+b+m+1)!}{(a+b+1)!}.\]

## 完整辅助引理：包含固定子集的权重和

取正整数 $k$、有限环境集合 $E$ 及 $L\subseteq E$。记 $m=|E|$、$l=|L|$、$R=E\setminus L$。每个包含 $L$ 的 $S\subseteq E$ 唯一写成 $L\cup A$，其中 $A\subseteq R$，且 $|S|=l+|A|$、$|R|=m-l$。将上一引理用于 $a=l$、$b=k-1$；利用 $k(k-1)!=k!$ 并约去大阶乘 $(m+k)!$，得到下式，包括 $L=\varnothing$ 和 $L=E$。

\[\sum_{L\subseteq S\subseteq E}\frac{k\,|S|!(m+k-|S|-1)!}{(m+k)!}=\frac{l!k!}{(l+k)!}=\binom{l+k}{k}^{-1}.\]

## 交换有限求和，得到一般加权差分恒等式

若 $T\cap E=\varnothing$，边际分解给 $\Delta_Tg(S)=\sum_{U\subseteq S}w_{T\cup U}$。每对 $U\subseteq S\subseteq E$ 恰好出现一次，交换有限双和。固定 $U$ 后，所有包含它的环境的权重之和由上一引理给出，所以每个 $w_{T\cup U}$ 得到下式中的精确系数。

\[\sum_{S\subseteq E}\frac{k\,|S|!(m+k-|S|-1)!}{(m+k)!}\Delta_Tg(S)=\sum_{U\subseteq E}\binom{|U|+k}{k}^{-1}w_{T\cup U}.\]

## 取共有加权差分定理的k=1

$T\cap E=\varnothing$。在加权差分恒等式取 $k=1$，左侧权重逐项等于原定义，右侧系数为 $1/(|U|+1)$，得原结论。$T=N$ 时环境为空，唯一项是 $w_N$；$T=\varnothing$ 时左侧是按该权重平均的原输出，右侧包括空交互 $b$。

## 二变量边界核对

令 $N=\{1,2\}$，$g(\varnothing)=7$、$g(\{1\})=8$、$g(\{2\})=9$、$g(\{1,2\})=13$。于是 $w_\varnothing=7$、$w_{\{1\}}=1$、$w_{\{2\}}=2$、$w_{\{1,2\}}=3$。 当 $T=N$，SII为 $w_N=3$；当 $T=\{1\}$，它等于 $\phi_g(1)=5/2$。当 $T=\varnothing$，阶乘定义给 $(7/3)+(8/6)+(9/6)+(13/3)=19/2$；交互形式给 $7+1/2+2/2+3/3=19/2$，两侧相等。

