# Appendix E. Proof of Theorem 4 and Corollary 5

Source: official PDF pages 15–16. Main labels: Theorem 3.4 and Corollary 3.5. Put J(T)=I_and(T)+I_or(T) only as a shorthand for the exact repeated source bracket.

According to Theorem 2, φ_i=varphi(i)=∑_{T⊆N,i∈T}J(T)/|T|. According to Eq. (6), φ(S)=∑_{T⊇S}|S|J(T)/|T|. The complete calculation is
\[
\begin{aligned}
\sum_{i\in S}\varphi(i)
&=\sum_{i\in S}\sum_{T\subseteq N,T\ni i}\frac1{|T|}J(T)\\
&=\sum_{i\in S}\left[\sum_{T\subseteq N,T\supseteq S}\frac1{|T|}J(T)+\sum_{T\subseteq N,T\not\supseteq S,T\ni i}\frac1{|T|}J(T)\right]\\
&=\sum_{i\in S}\left[\frac1{|S|}\sum_{T\subseteq N,T\supseteq S}\frac{|S|}{|T|}J(T)+\sum_{T\subseteq N,T\not\supseteq S,T\ni i}\frac1{|T|}J(T)\right]\\
&=\sum_{i\in S}\left[\frac1{|S|}\phi(S)+\sum_{T\subseteq N,T\not\supseteq S,T\ni i}\frac1{|T|}J(T)\right]\\
&=\sum_{i\in S}\frac1{|S|}\phi(S)+\sum_{i\in S}\sum_{T\subseteq N,T\not\supseteq S,T\ni i}\frac1{|T|}J(T)\\
&=|S|\frac1{|S|}\phi(S)+\sum_{\substack{T\subseteq N\\T\cap S\ne\varnothing,\ T\cap S\ne S}}\frac{|T\cap S|}{|T|}J(T)\\
&=\phi(S)+\sum_{\substack{T\subseteq N\\T\cap S\ne\varnothing,\ T\cap S\ne S}}\frac{|T\cap S|}{|T|}J(T).
\end{aligned}
\]
The source explains that each J(T)/|T| is counted |T∩S| times. It does not discuss S=empty.

For Corollary 5 the original printed premise is
\[
\forall T\in\{T:S\not\subseteq T,\ T\subseteq N,\ i\in S\},\quad I_{and}(T)=I_{or}(T)=0.
\]
The free i is retained as printed. The source then obtains
\[
\sum_{i\in S}\varphi(i)=\phi(S)+\sum_{\substack{T\subseteq N\\T\cap S\ne\varnothing,\ T\cap S\ne S}}\frac{|T\cap S|}{|T|}J(T)=\phi(S),
\]
and, for the individual variable,
\[
\varphi(i)=\frac1{|S|}\phi(S)+\sum_{T\subseteq N,T\not\supseteq S,T\ni i}\frac1{|T|}J(T)=\frac1{|S|}\phi(S).
\]
This concludes both source results.

