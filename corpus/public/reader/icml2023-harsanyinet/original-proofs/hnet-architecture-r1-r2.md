Theorem 4, Appendix B, physical PDF pages 13–14. Complete author mathematical proof transcription, including the questionable quantifiers and the gate-factor equality as printed.

The receptive field is defined by
\[
R_u^{(l)}=\bigcup_{(l',u')\in S_u^{(l)}}R_{u'}^{(l')},\qquad R_u^{(1)}=S_u^{(1)}.
\]
**(1) Requirement 1.** For arbitrary inputs $\widetilde x=\widetilde z^{(0)}$ and $x=z^{(0)}$, suppose $\widetilde x_i=x_i$ for $i\in R_u^{(l)}$; the goal is $z_u^{(l)}(\widetilde x)=z_u^{(l)}(x)$.

For first-layer neurons, the author considers $R_{u'}^{(1)}=S_{u'}^{(1)}\subseteq R_u^{(l)}$ and writes
\[
g_{u'}^{(1)}(\widetilde x)=(A_{u'}^{(1)})^\top\Sigma_{u'}^{(1)}\widetilde z^{(0)}=(A_{u'}^{(1)})^\top\zeta,
\]
where $\zeta_i=\widetilde z_i^{(0)}$ for $i\in R_{u'}^{(1)}$ and zero otherwise. Similarly,
\[
g_{u'}^{(1)}(x)=(A_{u'}^{(1)})^\top\Sigma_{u'}^{(1)}z^{(0)}=(A_{u'}^{(1)})^\top\eta,
\]
where $\eta_i=z_i^{(0)}=\widetilde z_i^{(0)}$ on this receptive field and zero otherwise. Thus $g_{u'}^{(1)}(\widetilde x)=g_{u'}^{(1)}(x)$ and $z_{u'}^{(1)}(\widetilde x)=z_{u'}^{(1)}(x)$.

For the second layer the author writes
\[
R_{u'}^{(2)}=\bigcup_{(1,u'')\in S_{u'}^{(2)}}R_{u''}^{(1)}\subseteq R_u^{(l)}.
\]
Its children have first-layer receptive fields contained in $R_u^{(l)}$, and their outputs agree on the two samples, so $z_{u'}^{(2)}(\widetilde x)=z_{u'}^{(2)}(x)$. Repeating this argument recursively yields $z_u^{(l)}(\widetilde x)=z_u^{(l)}(x)$, proving R1.

**(2) Requirement 2.** For $x$ and its masked sample $x_S$, the goal is
\[
z_u^{(l)}(x_S)=z_u^{(l)}(x)\prod_{i\in R_u^{(l)}}\mathbf1(i\in S).
\]
The author separates (a) $S\supseteq R_u^{(l)}$ from (b) $S\subsetneq R_u^{(l)}$ or $S$ incomparable with $R_u^{(l)}$ (written $S\cup R_u^{(l)}\ne S$ and $S\cup R_u^{(l)}\ne R_u^{(l)}$).

In case (a), all receptive-field coordinates remain unchanged. The established R1 gives
\[
z_u^{(l)}(x_S)=z_u^{(l)}(x)=z_u^{(l)}(x)\prod_{i\in R_u^{(l)}}\mathbf1(i\in S).
\]
In case (b), choose $j\in R_u^{(l)}\setminus S$. Since $z^{(0)}=x-b$ and masking sets $(x_S)_j=b$, one has
\[
(z_S^{(0)})_j=0,\qquad\prod_{i\in R_u^{(l)}}\mathbf1(i\in S)=0.
\]
There exists a first-layer neuron with $j\in R_{u'}^{(1)}=S_{u'}^{(1)}\subseteq R_u^{(l)}$. The original then prints a universal $\forall u'$ and the equality
\[
h_{u'}^{(1)}(x_S)
=g_{u'}^{(1)}(x_S)\prod_{(0,u'')\in S_{u'}^{(1)}}\mathbf1(z_{u''}^{(0)}(x_S)\ne0)
=g_{u'}^{(1)}(x_S)\mathbf1((z_S^{(0)})_j\ne0)=0,
\]
and hence $z_{u'}^{(1)}(x_S)=0$. The proof continues on page 14: since $j$ lies in the recursive union of child receptive fields, such a first-layer neuron affects the target recursively, so $h_u^{(l)}(x_S)=0$ and $z_u^{(l)}(x_S)=0$. Therefore
\[
z_u^{(l)}(x_S)=z_u^{(l)}(x)\prod_{i\in R_u^{(l)}}\mathbf1(i\in S)=0.
\]
The author concludes R2. The repair explains why the entire product vanishes rather than equating it to one factor, and propagates zero along the relevant ancestor path without the unwarranted universal quantifier.
