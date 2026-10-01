Appendix E, physical PDF page 16, second part of the complete Setting 2 proof. The printed sums without receptive-field filters, and the assertion about simultaneous activation, are preserved.

Considering $C$ channels as $C$ units, the source gives $m^{(l)}=HWC$ and writes
\[
I(S=R_{(1,h,w)}^{(l)})=\cdots=I(S=R_{(C,h,w)}^{(l)}),
\]
abbreviated $I(S=R_u^{(l)})$. It then invokes Theorem 2 and Lemma 1 and prints
\[
I(S=R_u^{(l)})
=\sum_{l=1}^L\sum_{u=1}^{m^{(l)}}w_{v,u}^{(l)}J_u^{(l)}(S=R_u^{(l)})
=\sum_{l=1}^L\sum_{u=1}^{HWC}w_{v,u}^{(l)}z_u^{(l)}(x).
\]
Here both weights and unit activations are scalar. The source says equal children make all $h_{(c,h,w)}^{(l)}(x)$ activated or deactivated simultaneously due to the AND operation. It specifies
\[
g_u^{(l)}(x)=(A_u^{(l)})^\top\Sigma_u^{(l)}z^{(l-1)},\qquad
A_u^{(l)}\in\mathbb R^{CK^2},
\]
and stacks the $C$ kernels as $B_u^{(l)}\in\mathbb R^{(CK^2)\times C}$, with $\Sigma_u^{(l)}\in\mathbb R^{(CK^2)\times(CK^2)}$ and local feature $z^{(l-1)}\in\mathbb R^{CK^2}$.

Considering all channels together as one vector unit gives $m^{(l)}=HW$ and prints
\[
I(S=R_{(:,h,w)}^{(l)})
=\sum_{l=1}^L\sum_{u=1}^{m^{(l)}}w_{v,u}^{(l)}J_u^{(l)}(S=R_u^{(l)})
=\sum_{l=1}^L\sum_{u=1}^{HW}(w_{v,u}^{(l)})^\top z_u^{(l)}(x).
\]
Both the weight and output now belong to $\mathbb R^C$. Since the vector unit shares the scalar units' children, the source says it has the same activation state. Its linear map is
\[
g_u^{(l)}(x)=(B_u^{(l)})^\top\Sigma_u^{(l)}z^{(l-1)}\in\mathbb R^C.
\]
The author concludes that channel units at one location share their field and contribute to the same interaction. No summand in the displayed scalar/vector sums is explicitly restricted to units whose receptive field equals the fixed target $S$. The corrected proof supplies this filter and distinguishes a common gate from nonzero post-ReLU outputs.
