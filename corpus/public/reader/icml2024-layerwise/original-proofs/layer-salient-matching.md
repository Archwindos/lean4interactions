Appendix G, physical PDF page 16. Complete author mathematical proof transcription of Lemma 3.4, including its external-reference argument and the duplicate-baseline equality.

The statement (18) says that every masked output can be universally matched by a small set of salient interactions:
\[
\begin{aligned}
v(x_T)&=v_{and}(x_T)+v_{or}(x_T)
=\sum_{S\subseteq T}I_{and}(S\mid x_T)+\sum_{S\cap T\ne\varnothing}I_{or}(S\mid x_T)\\
&\approx v(x_\varnothing)
+\sum_{S\in\Omega_{salient}^{and}:\varnothing\ne S\subseteq T}I_{and}(S\mid x_T)
+\sum_{S\in\Omega_{salient}^{or}:S\cap T\ne\varnothing}I_{or}(S\mid x_T).
\end{aligned}
\]
The entire author argument first cites Ren et al. (2023a) for the claim that, under common conditions (footnote 1), a well-trained DNN output $v_{and}(x_T)$ on all $2^n$ masks is approximated by a small number of AND interactions with salient effects, with $|\Omega_{salient}^{and}|\ll2^n$.

It then invokes Appendix C's assertion that OR interactions are particular AND interactions, and concludes that a well-trained DNN output $v_{or}(x_T)$ is similarly approximated by a small number of OR interactions, with $|\Omega_{salient}^{or}|\ll2^n$.

The final calculation (19), retained exactly in its baseline placement, is
\[
\begin{aligned}
v(x_T)&=v_{and}(x_T)+v_{or}(x_T)\\
&=v(x_\varnothing)+\sum_{S\subseteq T}I_{and}(S\mid x_T)+\sum_{S\cap T\ne\varnothing}I_{or}(S\mid x_T)\\
&\approx v(x_\varnothing)
+\sum_{S\in\Omega_{salient}^{and}:\varnothing\ne S\subseteq T}I_{and}(S\mid x_T)
+\sum_{S\in\Omega_{salient}^{or}:S\cap T\ne\varnothing}I_{or}(S\mid x_T).
\end{aligned}
\]
The author concludes that Lemma 3.4 is proved. The argument contains no quantitative definition of “small” or of the approximation error, and no demonstration that both learned decomposition components satisfy the cited DNN conditions. These gaps and the first equality's duplicate empty AND dividend are recorded separately.
