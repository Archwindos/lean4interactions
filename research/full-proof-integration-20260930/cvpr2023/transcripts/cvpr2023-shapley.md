# Theorem 2：经典Shapley的交互均分：来源数学转录

正文第4页Theorem2（标明由[15]证明），补充第2、6页Theorem2：输入变量i的Shapley值为 $\phi(i)=\sum_{S\subseteq N\setminus\{i\}}\frac1{|S|+1}w_{S\cup\{i\}}$。作者解释为一个m变量模式的效应均分给这m个变量。

补充第6页末至第8页Theorem3之前，作者完整数学推导：设n=|N|，l=|L|。
\[
\begin{aligned}\phi(i)&=\sum_{S\subseteq N\setminus\{i\}}\frac{|S|!(n-|S|-1)!}{n!}\Delta v_{\{i\}}(x_S)\\
&=\frac1n\sum_{m=0}^{n-1}\binom{n-1}{m}^{-1}\sum_{\substack{S\subseteq N\setminus\{i\}\\|S|=m}}\Delta v_{\{i\}}(x_S)\\
&=\frac1n\sum_{m=0}^{n-1}\binom{n-1}{m}^{-1}\sum_{\substack{S\subseteq N\setminus\{i\}\\|S|=m}}\sum_{L\subseteq S}w_{L\cup\{i\}}\\
&=\frac1n\sum_{L\subseteq N\setminus\{i\}}\sum_{m=0}^{n-1}\binom{n-1}{m}^{-1}\sum_{\substack{L\subseteq S\subseteq N\setminus\{i\}\\|S|=m}}w_{L\cup\{i\}}\\
&=\frac1n\sum_{L\subseteq N\setminus\{i\}}\sum_{m=l}^{n-1}\binom{n-1}{m}^{-1}\sum_{\substack{L\subseteq S\subseteq N\setminus\{i\}\\|S|=m}}w_{L\cup\{i\}}\\
&=\frac1n\sum_L\sum_{m=l}^{n-1}\binom{n-1}{m}^{-1}\binom{n-l-1}{m-l}w_{L\cup\{i\}}\\
&=\frac1n\sum_L w_{L\cup\{i\}}\underbrace{\sum_{r=0}^{n-l-1}\binom{n-1}{l+r}^{-1}\binom{n-l-1}{r}}_{\alpha_L}.
\end{aligned}
\]
第7页文字把待简化项称为“term $w_L$”，紧接公式/后文使用 $\alpha_L$。作者列出三项材料：(i) $m\binom nm=n\binom{n-1}{m-1}$；(ii) 对p,q>0写 $B(p,q)=\int_0^1x^{p-1}(1-x)^{1-q}dx$（原指数错误保留）；(iii) 正整数p,q有 $B(p,q)=[q\binom{p+q-1}{p-1}]^{-1}$，及正整数n>m有 $\binom nm=[mB(n-m+1,m)]^{-1}$。
\[
\begin{aligned}\alpha_L&=\sum_{r=0}^{n-l-1}\binom{n-l-1}{r}(l+r)B(n-l-r,l+r)\\
&=\underbrace{\sum_{r=0}^{n-l-1}l\binom{n-l-1}{r}B(n-l-r,l+r)}_{\text{①}}
+\underbrace{\sum_{r=0}^{n-l-1}r\binom{n-l-1}{r}B(n-l-r,l+r)}_{\text{②}}.
\end{aligned}
\]
\[
\begin{aligned}\text{①}&=\int_0^1l\sum_{r=0}^{n-l-1}\binom{n-l-1}{r}x^{n-l-r-1}(1-x)^{l+r-1}dx\\
&=\int_0^1l\underbrace{\sum_{r=0}^{n-l-1}\binom{n-l-1}{r}x^{n-l-r-1}(1-x)^r}_{=1}(1-x)^{l-1}dx
=\int_0^1l(1-x)^{l-1}dx=1.
\end{aligned}
\]
\[
\begin{aligned}\text{②}&=\sum_{r=1}^{n-l-1}(n-l-1)\binom{n-l-2}{r-1}B(n-l-r,l+r)\\
&=(n-l-1)\sum_{r'=0}^{n-l-2}\binom{n-l-2}{r'}B(n-l-r'-1,l+r'+1)\\
&=(n-l-1)\int_0^1\sum_{r'=0}^{n-l-2}\binom{n-l-2}{r'}x^{n-l-r'-2}(1-x)^{l+r'}dx\\
&=(n-l-1)\int_0^1\underbrace{\sum_{r'=0}^{n-l-2}\binom{n-l-2}{r'}x^{n-l-r'-2}(1-x)^{r'}}_{=1}(1-x)^l dx\\
&=(n-l-1)\int_0^1(1-x)^l dx=\frac{n-l-1}{l+1}.
\end{aligned}
\]
因此作者写 $\alpha_L=1+(n-l-1)/(l+1)=n/(l+1)$，再得 $\phi(i)=\frac1n\sum_L\alpha_L w_{L\cup\{i\}}=\sum_L\frac1{l+1}w_{L\cup\{i\}}$。错误Beta定义、l=0零参数和①边界见统一issue；最后结论在项目中用不同但完整的有限证明保留。
