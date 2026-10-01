# Theorem 3：原模型AND交互与经典Shapley

固定 $N=\{1,\ldots,n\}$、模型 $v:\mathbb R^n\to\mathbb R$、样本 $x$ 和同一个输入基线 $r$。记 $g(A)=v(x_A)$，$b=g(\varnothing)$。二次掩码定义条件游戏 $g_T(A)=v((x_T)_A)=g(T\cap A)$。AND为 $I_g(S)=\sum_{L\subseteq S}(-1)^{|S|-|L|}g(L)$，另记 $w_A=I_g(A)$。非空OR为 $O_g^N(S)=-I_{g^c}(S)$，其中 $g^c(L)=g(N\setminus L)$；空OR单独规定 $O_g^N(\varnothing)=g(\varnothing)$。所有子集和包括空集，原始输出不要求零基线。涉及分量时分别以 $v_{and},v_{or}$ 定义对应游戏和条件游戏。

\[\phi_g(i)=\sum_{S\subseteq N:i\in S}\frac{I_{and}(S\mid x)}{|S|}\]

经典边际阶乘定义先变为等分交互；把外部环境子集与含i的交互集合一一对应，得到作者外引公式。

## 核对是原模型的AND交互

原Theorem3的 $I_{and}(S\mid x)$ 来自模型 $v$ 自身的AND定义，不是任意学习分解中 $v_{and}$ 的系数。取 $g(A)=v(x_A)$、$i\in N$，即满足经典阶乘Shapley与共有证明的前提。

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

## 把环境子集换成含i的交互集合

环境 $U\subseteq N\setminus\{i\}$ 与含 $i$ 的交互集合一一对应：$S=U\cup\{i\}$，逆映射 $U=S\setminus\{i\}$，且 $|S|=|U|+1$。逐项换索引，便得到原分母 $|S|$。空集不含 $i$，不参与分配。

\[\phi_g(i)=\sum_{U\subseteq N\setminus\{i\}}\frac{I_g(U\cup\{i\})}{|U|+1}=\sum_{S\subseteq N:i\in S}\frac{I_g(S)}{|S|}.\]

