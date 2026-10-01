# Appendix D. Proof of Theorem 3 (main Theorem 3.3)

Source: official PDF pages 14–15. The original names v_and,v_or and original alternating exponents are retained. The displayed exponent +1 differs by two from the common paired form −1, so it is not itself a sign error.

According to the AND/OR definitions,
\[
\begin{aligned}
I_{and}(S)&=\sum_{L\subseteq S}(-1)^{|S|-|L|}v_{and}(L)
=\sum_{L\subseteq S\setminus\{i\}}(-1)^{|S|-|L|+1}[v_{and}(L\cup\{i\})-v_{and}(L)],\\
I_{or}(S)&=-\sum_{L\subseteq S}(-1)^{|S|-|L|}v_{or}(N\setminus L)
=\sum_{L\subseteq S\setminus\{i\}}(-1)^{|S|-|L|+1}[v_{or}(N\setminus L)-v_{or}(N\setminus L\setminus\{i\})],
\end{aligned}
\]
where v(L)=v_and(L)+v_or(L). Define, solely to keep the long source braces readable,
\[
D(L)=[v_{and}(L\cup\{i\})-v_{and}(L)]+[v_{or}(N\setminus L)-v_{or}(N\setminus L\setminus\{i\})].
\]
The source page-15 chain, with each repeated brace D(L) written in this explicitly defined shorthand, is
\[
\begin{aligned}
\sum_{S\subseteq N,S\ni i}\frac{I_{and}(S)+I_{or}(S)}{2^{|S|-1}}
&=\sum_{S\subseteq N,S\ni i}\sum_{L\subseteq S\setminus\{i\}}\frac{(-1)^{|S|-|L|+1}}{2^{|S|-1}}D(L)\\
&=\sum_{S\subseteq N\setminus\{i\}}\sum_{L\subseteq S}\frac{(-1)^{|S|-|L|}}{2^{|S|}}D(L)\\
&=\sum_{L\subseteq N\setminus\{i\}}(-1)^{|L|}\sum_{\substack{S\subseteq N\setminus\{i\}\\S\supseteq L}}\frac{(-1)^{|S|}}{2^{|S|}}D(L)\\
&=\sum_{L\subseteq N\setminus\{i\}}(-1)^{|L|}\frac{(-1)^{|L|}}{2^{|N|-1}}D(L)\\
&=\sum_{L\subseteq N\setminus\{i\}}\frac1{2^{|N|-1}}D(L)\\
&=\sum_{S\subseteq N\setminus\{i\}}\frac{v_{and}(S\cup\{i\})-v_{and}(S)}{2^{|N|-1}}
+\sum_{S\subseteq N\setminus\{i\}}\frac{v_{or}(N\setminus S)-v_{or}(N\setminus S\setminus\{i\})}{2^{|N|-1}}\\
&=\sum_{S\subseteq N\setminus\{i\}}\frac{v_{and}(S\cup\{i\})-v_{and}(S)}{2^{|N|-1}}
+\sum_{S\subseteq N\setminus\{i\}}\frac{v_{or}(S\cup\{i\})-v_{or}(S)}{2^{|N|-1}}\\
&=\sum_{S\subseteq N\setminus\{i\}}\frac{[v_{and}(S\cup\{i\})+v_{or}(S\cup\{i\})]-[v_{and}(S)+v_{or}(S)]}{2^{|N|-1}}\\
&=\sum_{S\subseteq N\setminus\{i\}}\frac{v(S\cup\{i\})-v(S)}{2^{|N|-1}}=B(i).
\end{aligned}
\]
The source comment in the fourth line asserts
\[
\sum_{\substack{S\subseteq N\setminus\{i\}\\S\supseteq L}}\frac{(-1)^{|S|}}{2^{|S|}}=\frac{(-1)^{|L|}}{2^{|N|-1}}.
\]
The last line gives the claimed reformulation.

