# Appendix F. Proof of Theorem 6 and Corollary 7

Source: official PDF pages 16–17. Main labels: Theorem 3.6 and Corollary 3.7. J(T)=I_and(T)+I_or(T) is a shorthand for the repeated source bracket.

According to Theorem 3.2, varphi(i)=∑_{T⊆N,i∈T}J(T)/|T|. According to Eq. (6), φ(S)=∑_{T⊇S}|S|J(T)/|T|. For every i∈S,
\[
\begin{aligned}
\varphi(i)
&=\sum_{T\subseteq N,T\ni i}\frac1{|T|}J(T)\\
&=\sum_{T\subseteq N,T\supseteq S}\frac1{|T|}J(T)+\sum_{T\subseteq N,T\not\supseteq S,T\ni i}\frac1{|T|}J(T)\\
&=\frac1{|S|}\sum_{T\subseteq N,T\supseteq S}\frac{|S|}{|T|}J(T)+\sum_{T\subseteq N,T\not\supseteq S,T\ni i}\frac1{|T|}J(T)\\
&=\frac1{|S|}\phi(S)+\sum_{T\subseteq N,T\not\supseteq S,T\ni i}\frac1{|T|}J(T).
\end{aligned}
\]
For the corollary set S={i}:
\[
\begin{aligned}
\varphi(i)
&=\frac1{|S|}\phi(S)+\sum_{T\subseteq N,T\not\supseteq S,T\ni i}\frac1{|T|}J(T)\\
&=\frac11\phi(S)+\sum_{T\subseteq N,T\not\supseteq\{i\},T\ni i}\frac1{|T|}J(T)\\
&=\phi(S)=\phi(S=\{i\}).
\end{aligned}
\]

