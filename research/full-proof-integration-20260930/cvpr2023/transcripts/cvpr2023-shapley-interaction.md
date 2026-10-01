# Theorem 3：Shapley interaction 的交互权重：来源数学转录

补充第2、8页Theorem3：$T\subseteq N$，$I^{\rm Shapley}(T)=\sum_{S\subseteq N\setminus T}\frac{|S|!(|N|-|S|-|T|)!}{(|N|-|T|+1)!}\Delta v_T(x_S)$，则 $I^{\rm Shapley}(T)=\sum_{S\subseteq N\setminus T}\frac1{|S|+1}w_{S\cup T}$；把T作为单个组成变量解释其均匀分配。

补充第8页Theorem3至第9页Theorem4之前的全部推导。令n=|N|、t=|T|、l=|L|、M=n−t。
\[
\begin{aligned}I^{\rm Shapley}(T)&=\sum_{S\subseteq N\setminus T}\frac{|S|!(n-|S|-t)!}{(n-t+1)!}\Delta v_T(x_S)\\
&=\frac1{M+1}\sum_{m=0}^{M}\binom M m^{-1}\sum_{\substack{S\subseteq N\setminus T\\|S|=m}}\Delta v_T(x_S)\\
&=\frac1{M+1}\sum_{m=0}^{M}\binom M m^{-1}\sum_{\substack{S\subseteq N\setminus T\\|S|=m}}\sum_{L\subseteq S}w_{L\cup T}\\
&=\frac1{M+1}\sum_{L\subseteq N\setminus T}\sum_{m=l}^{M}\binom M m^{-1}\sum_{\substack{L\subseteq S\subseteq N\setminus T\\|S|=m}}w_{L\cup T}\\
&=\frac1{M+1}\sum_L\sum_{m=l}^{M}\binom M m^{-1}\binom{M-l}{m-l}w_{L\cup T}\\
&=\frac1{M+1}\sum_Lw_{L\cup T}\underbrace{\sum_{r=0}^{M-l}\binom M{l+r}^{-1}\binom{M-l}{r}}_{\alpha_L}.
\end{aligned}
\]
作者复用Theorem2的组合数/Beta材料：
\[
\begin{aligned}\alpha_L&=\sum_{r=0}^{M-l}\binom{M-l}r(l+r)B(M-l-r+1,l+r)\\
&=\underbrace{\sum_{r=0}^{M-l}l\binom{M-l}rB(M-l-r+1,l+r)}_{\text{①}}
+\underbrace{\sum_{r=0}^{M-l}r\binom{M-l}rB(M-l-r+1,l+r)}_{\text{②}}.
\end{aligned}
\]
\[
\begin{aligned}\text{①}&=\int_0^1l\sum_{r=0}^{M-l}\binom{M-l}r x^{M-l-r}(1-x)^{l+r-1}dx\\
&=\int_0^1l\underbrace{\sum_{r=0}^{M-l}\binom{M-l}r x^{M-l-r}(1-x)^r}_{=1}(1-x)^{l-1}dx
=\int_0^1l(1-x)^{l-1}dx=1,\\
\text{②}&=\sum_{r=1}^{M-l}(M-l)\binom{M-l-1}{r-1}B(M-l-r+1,l+r)\\
&=(M-l)\sum_{r'=0}^{M-l-1}\binom{M-l-1}{r'}B(M-l-r',l+r'+1)\\
&=(M-l)\int_0^1\sum_{r'=0}^{M-l-1}\binom{M-l-1}{r'}x^{M-l-r'-1}(1-x)^{l+r'}dx\\
&=(M-l)\int_0^1\underbrace{\sum_{r'=0}^{M-l-1}\binom{M-l-1}{r'}x^{M-l-r'-1}(1-x)^{r'}}_{=1}(1-x)^l dx\\
&=(M-l)\int_0^1(1-x)^l dx=\frac{M-l}{l+1}.
\end{aligned}
\]
于是原证明得 $\alpha_L=1+(M-l)/(l+1)=(M+1)/(l+1)$，$I^{\rm Shapley}(T)=\frac1{M+1}\sum_L\alpha_Lw_{L\cup T}=\sum_Lw_{L\cup T}/(l+1)$。l=0时原①不成立；完整修正证明不改T的量词。
