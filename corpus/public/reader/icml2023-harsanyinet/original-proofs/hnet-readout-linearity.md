Theorem 2, Appendix B, physical PDF page 12. Mathematical transcription of the complete author proof; the source writes $w_u^{(l)}$ for the readout coefficient.

The author first expands the dot products:
\[
v(x)=\sum_{l=1}^L(w_v^{(l)})^\top z^{(l)}(x)
=\sum_{l=1}^L\sum_{u=1}^{m^{(l)}}w_u^{(l)}z_u^{(l)}(x).
\]
The stated linearity property is: if, for every $S\subseteq N$, $v(x_S)=u(x_S)+w(x_S)$ and $(cv)(x_S)=c\,v(x_S)$ for $c\in\mathbb R$, then
\[
I^v(S)=I^u(S)+I^w(S),\qquad I^{(cv)}(S)=cI^v(S).
\]
Since $J_u^{(l)}(S)$ denotes the Harsanyi interaction computed on $z_u^{(l)}(x)$, the author concludes
\[
I(S)=\sum_{l=1}^L\sum_{u=1}^{m^{(l)}}w_u^{(l)}J_u^{(l)}(S).
\]
There are no further proof calculations in this block.
