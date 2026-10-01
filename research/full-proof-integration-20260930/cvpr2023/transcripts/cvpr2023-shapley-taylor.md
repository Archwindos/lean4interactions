# Theorem 4：Shapley–Taylor 的全部阶数分支：来源数学转录

补充第2、9页Theorem4：对第k阶，k阶Shapley–Taylor指数满足：$|T|<k$ 时等于wT；$|T|=k$ 时等于 $\sum_{S\subseteq N\setminus T}\binom{|S|+k}{k}^{-1}w_{S\cup T}$；$|T|>k$ 时为0。正阶数的域来自k-th order及其引用的定义，项目显式记录，不假定n≥k（当k>n只用第一分支）。 原文没有明写 $k>0$；本轮证明和Lean对齐的是正阶数的有效定义域，不能把此条件伪记为作者原文的不等式。$k=0$不属于当前有效域核验。

补充第9页末至第11页E之前的完整作者证明。原定义为
\[
I^{\rm Shapley\text{-}Taylor(k)}(T)=\begin{cases}
\Delta v_T(x_\varnothing),&|T|<k,\\
\frac{k}{n}\sum_{S\subseteq N\setminus T}\binom{n-1}{|S|}^{-1}\Delta v_T(x_S),&|T|=k,\\0,&|T|>k.
\end{cases}
\]
低阶分支直接按Harsanyi定义给 $\Delta v_T(x_\varnothing)=\sum_{L\subseteq T}(-1)^{|T|-|L|}v(x_L)=w_T$。最高阶分支，n=|N|、l=|L|，作者计算
\[
\begin{aligned}I^{\rm ST(k)}(T)&=\frac{k}{n}\sum_{S\subseteq N\setminus T}\binom{n-1}{|S|}^{-1}\Delta v_T(x_S)\\
&=\frac{k}{n}\sum_{m=0}^{n-k}\sum_{\substack{S\subseteq N\setminus T\\|S|=m}}\binom{n-1}{|S|}^{-1}\Delta v_T(x_S)\\
&=\frac{k}{n}\sum_{m=0}^{n-k}\sum_{\substack{S\subseteq N\setminus T\\|S|=m}}\binom{n-1}{|S|}^{-1}\sum_{L\subseteq S}w_{L\cup T}\\
&=\frac{k}{n}\sum_L\sum_{m=l}^{n-k}\binom{n-1}{|S|}^{-1}\sum_{\substack{L\subseteq S\subseteq N\setminus T\\|S|=m}}w_{L\cup T}\\
&=\frac{k}{n}\sum_L\sum_{m=l}^{n-k}\binom{n-1}{|S|}^{-1}\binom{n-l-k}{m-l}w_{L\cup T}\\
&=\frac{k}{n}\sum_Lw_{L\cup T}\underbrace{\sum_{r=0}^{n-l-k}\binom{n-1}{l+r}^{-1}\binom{n-l-k}r}_{\alpha_L}.
\end{aligned}
\]
中间两行原稿在按m分组之后仍印|S|（S在内族满足|S|=m）；最后按r重新编号。
\[
\begin{aligned}\alpha_L&=\sum_{r=0}^{n-l-k}\binom{n-l-k}r(l+r)B(n-l-r,l+r)\\
&=\underbrace{\sum_{r=0}^{n-l-k}l\binom{n-l-k}r B(n-l-r,l+r)}_{\text{①}}
+\underbrace{\sum_{r=0}^{n-l-k}r\binom{n-l-k}r B(n-l-r,l+r)}_{\text{②}}.
\end{aligned}
\]
\[
\begin{aligned}\text{①}&=\int_0^1l\sum_{r=0}^{n-l-k}\binom{n-l-k}r x^{n-l-r-1}(1-x)^{l+r-1}dx\\
&=\int_0^1l\underbrace{\sum_{r=0}^{n-l-k}\binom{n-l-k}r x^{n-l-r-k}(1-x)^r}_{=1}x^{k-1}(1-x)^{l-1}dx\\
&=lB(k,l)=\binom{l+k-1}{k-1}^{-1},\\
\text{②}&=(n-l-k)\sum_{r=1}^{n-l-k}\binom{n-l-k-1}{r-1}B(n-l-r,l+r)\\
&=(n-l-k)\sum_{r'=0}^{n-l-k-1}\binom{n-l-k-1}{r'}B(n-l-r'-1,l+r'+1)\\
&=(n-l-k)\int_0^1\sum_{r'=0}^{n-l-k-1}\binom{n-l-k-1}{r'}x^{n-l-r'-2}(1-x)^{l+r'}dx\\
&=(n-l-k)\int_0^1\underbrace{\sum_{r'=0}^{n-l-k-1}\binom{n-l-k-1}{r'}x^{n-l-r'-k-1}(1-x)^{r'}}_{=1}x^{k-1}(1-x)^l dx\\
&=(n-l-k)B(k,l+1)=\frac{n-l-k}{(l+1)\binom{l+k}{k-1}}.
\end{aligned}
\]
\[
\begin{aligned}\alpha_L&=\binom{l+k-1}{k-1}^{-1}+\frac{n-l-k}{(l+1)\binom{l+k}{k-1}}\\
&=\frac{l!(k-1)!}{(l+k-1)!}+\frac{n-l-k}{l+1}\frac{(l+1)!(k-1)!}{(l+k)!}\\
&=\frac{l!(k-1)!}{(l+k-1)!}+\frac{n-l-k}{l+k}\frac{l!(k-1)!}{(l+k-1)!}\\
&=\left[1+\frac{n-l-k}{l+k}\right]\frac{l!(k-1)!}{(l+k-1)!}
=\frac n{l+k}\frac{l!(k-1)!}{(l+k-1)!}
=\frac nk\frac{l!k!}{(l+k)!}=\frac nk\binom{l+k}k^{-1}.
\end{aligned}
\]
于是作者最终写 $I^{\rm ST(k)}(T)=\frac kn\sum_L\alpha_Lw_{L\cup T}=\sum_L\binom{l+k}k^{-1}w_{L\cup T}$。高阶为0由定义。原积分域与l=0问题保留在issue中。
