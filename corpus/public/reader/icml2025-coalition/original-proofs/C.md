# Appendix C. Proof of Theorem 2 (main Theorem 3.2)

Source: official PDF pages 12–14. This is a complete mathematical transcription of the author calculation. In this transcription U denotes the background called S in the PDF, and the source's A and B marginal components are written A_U and B_U. The source interaction names Iand and Ior are preserved. These changes only prevent a bound-variable collision; the erroneous nonempty-intersection domains on page 14 are retained below.

According to the definition of Shapley values,
\[
\varphi(i)=\sum_{U\subseteq N\setminus\{i\}}\frac{|U|!(n-|U|-1)!}{n!}[v(U\cup\{i\})-v(U)]
=\mathbb E_{U\subseteq N\setminus\{i\}}[v(U\cup\{i\})-v(U)].
\]
According to Eq. (10), for every U⊆N,
\[
v(U)=v(\varnothing)+\sum_{L\subseteq U,L\ne\varnothing}I_{and}(L)+\sum_{L\cap U\ne\varnothing}I_{or}(L).
\]
Thus
\[
\begin{aligned}
v(U\cup\{i\})-v(U)
&=\left[v(\varnothing)+\sum_{L\subseteq U\cup\{i\},L\ne\varnothing}I_{and}(L)+\sum_{L\cap(U\cup\{i\})\ne\varnothing}I_{or}(L)\right]\\
&\quad-\left[v(\varnothing)+\sum_{L\subseteq U,L\ne\varnothing}I_{and}(L)+\sum_{L\cap U\ne\varnothing}I_{or}(L)\right]\\
&=\left[\sum_{L\subseteq U\cup\{i\},L\ne\varnothing}I_{and}(L)-\sum_{L\subseteq U,L\ne\varnothing}I_{and}(L)\right]
+\left[\sum_{L\cap(U\cup\{i\})\ne\varnothing}I_{or}(L)-\sum_{L\cap U\ne\varnothing}I_{or}(L)\right]\\
&=\underbrace{\sum_{L\subseteq U}I_{and}(L\cup\{i\})}_{A_U}
+\underbrace{\sum_{L\cap U=\varnothing}I_{or}(L\cup\{i\})}_{B_U}.
\end{aligned}
\]
This breaks the Shapley value into E[A_U+B_U]. For the AND part the complete page-13 chain is
\[
\begin{aligned}
\mathbb E_U[A_U]
&=\mathbb E_U\sum_{L\subseteq U}I_{and}(L\cup\{i\})\\
&=\frac1n\sum_{m=0}^{n-1}\frac1{\binom{n-1}m}\sum_{\substack{U\subseteq N\setminus\{i\}\\|U|=m}}\sum_{L\subseteq U}I_{and}(L\cup\{i\})\\
&=\frac1n\sum_{L\subseteq N\setminus\{i\}}\sum_{m=0}^{n-1}\frac1{\binom{n-1}m}\sum_{\substack{U\supseteq L,\ U\subseteq N\setminus\{i\}\\|U|=m}}I_{and}(L\cup\{i\})\\
&=\frac1n\sum_{L\subseteq N\setminus\{i\}}\sum_{m=|L|}^{n-1}\frac1{\binom{n-1}m}\sum_{\substack{U\supseteq L,\ U\subseteq N\setminus\{i\}\\|U|=m}}I_{and}(L\cup\{i\})\\
&=\frac1n\sum_{L\subseteq N\setminus\{i\}}\sum_{m=|L|}^{n-1}\frac{\binom{n-1-|L|}{m-|L|}}{\binom{n-1}m}I_{and}(L\cup\{i\})\\
&=\sum_{L\subseteq N\setminus\{i\}}\underbrace{\left[\frac1n\sum_{k=0}^{n-1-|L|}\frac{\binom{n-1-|L|}k}{\binom{n-1}{|L|+k}}\right]}_{\alpha_L}I_{and}(L\cup\{i\})\\
&=\sum_{L\subseteq N\setminus\{i\}}\frac1{|L|+1}I_{and}(L\cup\{i\})
=\sum_{T\subseteq N,i\in T}\frac1{|T|}I_{and}(T).
\end{aligned}
\]
The source comments give |U|≥|L| in the third-to-fourth line, k=m−|L| in the sixth line, and T=L∪{i} in the last line.

The OR chain on page 14 prints the following domains. **The first three nonempty-intersection conditions are source errors and are not corrected in this original-proof field.**
\[
\begin{aligned}
\mathbb E_U[B_U]
&=\mathbb E_U\sum_{L\cap U\ne\varnothing}I_{or}(L\cup\{i\})\\
&=\frac1n\sum_{m=0}^{n-1}\frac1{\binom{n-1}m}\sum_{\substack{U\subseteq N\setminus\{i\}\\|U|=m}}\sum_{L\cap U\ne\varnothing}I_{or}(L\cup\{i\})\\
&=\frac1n\sum_{L\subseteq N\setminus\{i\}}\sum_{m=0}^{n-1}\frac1{\binom{n-1}m}\sum_{\substack{U\cap L\ne\varnothing,\ U\subseteq N\setminus\{i\}\\|U|=m}}I_{or}(L\cup\{i\})\\
&=\frac1n\sum_{L\subseteq N\setminus\{i\}}\sum_{m=0}^{n-1}\frac1{\binom{n-1}m}\sum_{\substack{U\subseteq N\setminus\{i\}\setminus L\\|U|=m}}I_{or}(L\cup\{i\})\\
&=\frac1n\sum_{L\subseteq N\setminus\{i\}}\sum_{m=0}^{n-1-|L|}\frac1{\binom{n-1}m}\sum_{\substack{U\subseteq N\setminus\{i\}\setminus L\\|U|=m}}I_{or}(L\cup\{i\})\\
&=\frac1n\sum_{L\subseteq N\setminus\{i\}}\sum_{m=0}^{n-1-|L|}\frac{\binom{n-1-|L|}m}{\binom{n-1}m}I_{or}(L\cup\{i\})\\
&=\frac1n\sum_{L\subseteq N\setminus\{i\}}\sum_{k=0}^{n-1-|L|}\frac{\binom{n-1-|L|}{n-1-|L|-k}}{\binom{n-1}{n-1-|L|-k}}I_{or}(L\cup\{i\})\\
&=\frac1n\sum_{L\subseteq N\setminus\{i\}}\sum_{k=0}^{n-1-|L|}\frac{\binom{n-1-|L|}k}{\binom{n-1}{|L|+k}}I_{or}(L\cup\{i\})\\
&=\frac1n\sum_{L\subseteq N\setminus\{i\}}\frac n{|L|+1}I_{or}(L\cup\{i\})\\
&=\sum_{L\subseteq N\setminus\{i\}}\frac1{|L|+1}I_{or}(L\cup\{i\})
=\sum_{T\subseteq N,i\in T}\frac1{|T|}I_{or}(T).
\end{aligned}
\]
The source comments use |U|≤n−1−|L| and k=n−1−|L|−m. Adding both parts concludes
\[
\varphi(i)=\mathbb E_U[A_U]+\mathbb E_U[B_U]
=\sum_{T\subseteq N,i\in T}\frac1{|T|}[I_{and}(T)+I_{or}(T)].
\]

