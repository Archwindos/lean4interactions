# Theorem 2：经典Shapley的交互均分

固定有限总体 $N$、输入 $x$ 与输入基线向量 $r$。掩码 $x_S$ 在 $S$ 内保留原坐标、在其余坐标使用同一个 $r$。模型是 $v:X\to\mathbb R$，集合函数是 $g(S)=v(x_S)$，输出基线是 $b=g(\varnothing)$。本文原始交互为
\[
w_A=I_g(A)=\sum_{U\subseteq A}(-1)^{|A|-|U|}g(U).
\]
所有子集求和包括空集。特别地 $w_\varnothing=b$。若改用 $g_0=g-b$，只有空集交互改为零；本篇的原始输出没有零基线假设。

\[\phi_g(i)=\sum_{U\subseteq N\setminus\{i\}}\frac{I_g(U\cup\{i\})}{|U|+1}\]

将经典边际定义中的每个差分展开为交互和。有限阶乘卷积算出每项的总权重，得到对模式内变量的均分。

## 从经典阶乘权重定义开始

取 $i\in N$，记 $n=|N|\ge1$。经典Shapley值对每个环境 $S\subseteq N\setminus\{i\}$ 的边际 $g(S\cup\{i\})-g(S)=\Delta_{\{i\}}g(S)$，按阶乘权重 $|S|!(n-|S|-1)!/n!$ 加权求和。

\[\phi_g(i)=\sum_{S\subseteq N\setminus\{i\}}\frac{|S|!(n-|S|-1)!}{n!}\Delta_{\{i\}}g(S).\]

## 完整辅助引理：有限阶乘卷积

对任意有限集合 $R$、非负整数 $a,b$，记 $m=|R|$，$F_R(a,b)=\sum_{A\subseteq R}(a+|A|)!(b+m-|A|)!$。对 $R$ 作插入归纳，并加强归纳命题为对所有 $a,b$ 成立。$R=\varnothing$ 时两边都是 $a!b!$。插入新变量 $i\notin R$ 后，按 $A$ 是否含 $i$ 分组得到 $F_{R\cup\{i\}}(a,b)=F_R(a,b+1)+F_R(a+1,b)$。归纳假设给出的两项有共同分母 $(a+b+2)!$ 和共同大阶乘 $(a+b+m+2)!$，小阶乘相加为 $a!(b+1)!+(a+1)!b!=a!b!(a+b+2)$。约去正数 $a+b+2$ 得插入后的公式。全部阶乘为正，除法合法；论证包括 $a=0$、$b=0$、$m=0$。

\[F_R(a,b)=\frac{a!b!(a+b+m+1)!}{(a+b+1)!}.\]

## 完整辅助引理：包含固定子集的权重和

取正整数 $k$、有限环境集合 $E$ 及 $L\subseteq E$。记 $m=|E|$、$l=|L|$、$R=E\setminus L$。每个包含 $L$ 的 $S\subseteq E$ 唯一写成 $L\cup A$，其中 $A\subseteq R$，且 $|S|=l+|A|$、$|R|=m-l$。将上一引理用于 $a=l$、$b=k-1$；利用 $k(k-1)!=k!$ 并约去大阶乘 $(m+k)!$，得到下式，包括 $L=\varnothing$ 和 $L=E$。

\[\sum_{L\subseteq S\subseteq E}\frac{k\,|S|!(m+k-|S|-1)!}{(m+k)!}=\frac{l!k!}{(l+k)!}=\binom{l+k}{k}^{-1}.\]

## 交换有限求和，得到一般加权差分恒等式

若 $T\cap E=\varnothing$，边际分解给 $\Delta_Tg(S)=\sum_{U\subseteq S}w_{T\cup U}$。每对 $U\subseteq S\subseteq E$ 恰好出现一次，交换有限双和。固定 $U$ 后，所有包含它的环境的权重之和由上一引理给出，所以每个 $w_{T\cup U}$ 得到下式中的精确系数。

\[\sum_{S\subseteq E}\frac{k\,|S|!(m+k-|S|-1)!}{(m+k)!}\Delta_Tg(S)=\sum_{U\subseteq E}\binom{|U|+k}{k}^{-1}w_{T\cup U}.\]

## 逐项检查共有引理的参数

在加权差分恒等式中取 $T=\{i\}$、$E=N\setminus\{i\}$、$k=1$，于是 $m=n-1$，左侧权重恰好是经典Shapley阶乘权重。右侧系数为 $\binom{|U|+1}{1}^{-1}=1/(|U|+1)$，得到原结论。差分集合与环境不相交，且 $k>0$，满足引理的全部前提。

\[\phi_g(i)=\sum_{U\subseteq N\setminus\{i\}}\frac{I_g(U\cup\{i\})}{|U|+1}.\]

## 空集输出基线与二变量例子

令 $N=\{1,2\}$，$g(\varnothing)=7$、$g(\{1\})=8$、$g(\{2\})=9$、$g(\{1,2\})=13$。于是 $w_\varnothing=7$、$w_{\{1\}}=1$、$w_{\{2\}}=2$、$w_{\{1,2\}}=3$。 因此 $\phi_g(1)=1+3/2=5/2$、$\phi_g(2)=2+3/2=7/2$，总和为 $6=g(N)-b$。环境 $U$ 可以为空，但分配的是非空交互 $\{i\}$；输出基线 $b$ 不分配给变量。若 $N=\{i\}$，唯一环境为空，公式给 $\phi_g(i)=g(\{i\})-b$。

