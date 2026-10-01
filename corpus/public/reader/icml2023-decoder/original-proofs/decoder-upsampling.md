In this section, we prove Theorem 4.4 in the main paper, as follows.

Proof.

$$G^{(c)}_{uv}=\sum_{m=0}^{M_0-1}\sum_{n=0}^{N_0-1}F^{(c)}_{mn}e^{-i(um/M_0+vn/N_0)2\pi}\qquad\text{//Equation (19)}.\tag{40}$$

$$\begin{aligned}
H^{(c)}_{u+(s-1)M_0,v+(t-1)N_0}
&=\sum_{m=0}^{M-1}\sum_{n=0}^{N-1}\widetilde F^{(c)}_{mn}e^{-i((u+(s-1)M_0)m/M+(v+(t-1)N_0)n/N)2\pi}\quad\text{//Equation (19)}\\
&=\sum_{m=0}^{M_0-1}\sum_{n=0}^{N_0-1}F^{(c)}_{mn}e^{-i((u+(s-1)M_0)(m\cdot ratio)/M+(v+(t-1)N_0)(n\cdot ratio)/N)2\pi}\\
&=\sum_{m=0}^{M_0-1}\sum_{n=0}^{N_0-1}F^{(c)}_{mn}e^{-i((u+(s-1)M_0)m/(M/ratio)+(v+(t-1)N_0)n/(N/ratio))2\pi}\\
&=\sum_{m=0}^{M_0-1}\sum_{n=0}^{N_0-1}F^{(c)}_{mn}e^{-i((u+(s-1)M_0)m/M_0+(v+(t-1)N_0)n/N_0)2\pi}\quad\text{//}M=M_0\cdot ratio;\ N=N_0\cdot ratio\\
&=\sum_{m=0}^{M_0-1}\sum_{n=0}^{N_0-1}F^{(c)}_{mn}e^{-i(um/M_0+vn/N_0)2\pi}\cdot e^{-i((s-1)m+(t-1)n)2\pi}\\
&=\sum_{m=0}^{M_0-1}\sum_{n=0}^{N_0-1}F^{(c)}_{mn}e^{-i(um/M_0+vn/N_0)2\pi}\quad\text{//}s,t\in\mathbb Z\\
&=G^{(c)}_{uv}\quad\text{//Equation (40)}.
\end{aligned}\tag{41}$$

Therefore we prove that:

$$\forall c,u,v,\quad H^{(c)}_{u+(s-1)M_0,v+(t-1)N_0}=G^{(c)}_{uv},\qquad\text{s.t. }s=1,\ldots,M/M_0;\quad t=1,\ldots,N/N_0.\tag{42}$$
