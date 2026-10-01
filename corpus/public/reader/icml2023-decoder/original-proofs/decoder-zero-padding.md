In this section, we prove Theorem 4.3 in the main paper, as follows.

Proof.

$$\begin{aligned}
\mathbb E_{F^{(c)}}[G^{(c)}_{uv}]&=\mathbb E\left[\sum_{m=0}^{M-1}\sum_{n=0}^{N-1}F^{(c)}_{mn}e^{-i(um/M+vn/N)2\pi}\right]\quad\text{//Equation (19)}\\
&=\sum_{m=0}^{M-1}\sum_{n=0}^{N-1}\mathbb E[F^{(c)}_{mn}]e^{-i(um/M+vn/N)2\pi}\\
&=a\sum_{m=0}^{M-1}\sum_{n=0}^{N-1}e^{-i(um/M+vn/N)2\pi}\quad\text{//}F^{(c)}_{mn}\sim\mathcal N(a,\sigma^2)\\
&=aMN\delta_{uv};\quad 0\le u<M,\ 0\le v<N\quad\text{//Equation (15)}.
\end{aligned}\tag{33}$$

$$\begin{aligned}
\mathbb E_{F^{(c)}}[H^{(c)}_{uv}]&=\mathbb E_{F^{(c)}}\left[\sum_{m=0}^{M'-1}\sum_{n=0}^{N'-1}\widetilde F^{(c)}_{mn}e^{-i(um/M'+vn/N')2\pi}\right]\quad\text{//Equation (19)}\\
&=\mathbb E_{F^{(c)}}\left[\sum_{m=0}^{M-1}\sum_{n=0}^{N-1}F^{(c)}_{mn}e^{-i(um/M'+vn/N')2\pi}\right]\\
&=a\sum_{m=0}^{M-1}\sum_{n=0}^{N-1}e^{-i(um/M'+vn/N')2\pi}\quad\text{//}F^{(c)}_{mn}\sim\mathcal N(a,\sigma^2)\\
&=a\frac{\sin(Mu\pi/M')}{\sin(u\pi/M')}\frac{\sin(Nv\pi/N')}{\sin(v\pi/N')}e^{-i((M-1)u/M'+(N-1)v/N')\pi};\quad 0\le u<M',\ 0\le v<N'\quad\text{//Equation (13)}.
\end{aligned}\tag{34}$$

$$\begin{aligned}
Var_{F^{(c)}}[G^{(c)}_{uv}]&=Var\left[\sum_{m=0}^{M-1}\sum_{n=0}^{N-1}F^{(c)}_{mn}e^{-i(um/M+vn/N)2\pi}\right]\\
&=\sum_{m=0}^{M-1}\sum_{n=0}^{N-1}Var[F^{(c)}_{mn}e^{-i(um/M+vn/N)2\pi}]\quad\text{//}\forall m,n;F^{(c)}_{mn}\text{ is i.i.d}\\
&=\sum_{m=0}^{M-1}\sum_{n=0}^{N-1}Var[F^{(c)}_{mn}]\\
&=\sum_{m=0}^{M-1}\sum_{n=0}^{N-1}\sigma^2\quad\text{//}F^{(c)}_{mn}\sim\mathcal N(a,\sigma^2)\\
&=MN\sigma^2.
\end{aligned}\tag{35}$$

$$\begin{aligned}
Var_{F^{(c)}}[H^{(c)}_{uv}]&=Var\left[\sum_{m=0}^{M'-1}\sum_{n=0}^{N'-1}\widetilde F^{(c)}_{mn}e^{-i(um/M'+vn/N')2\pi}\right]\\
&=Var\left[\sum_{m=0}^{M-1}\sum_{n=0}^{N-1}F^{(c)}_{mn}e^{-i(um/M'+vn/N')2\pi}\right]\\
&=\sum_{m=0}^{M-1}\sum_{n=0}^{N-1}Var[F^{(c)}_{mn}e^{-i(um/M'+vn/N')2\pi}]\quad\text{//}\forall m,n;F^{(c)}_{mn}\text{ is i.i.d}\\
&=\sum_{m=0}^{M-1}\sum_{n=0}^{N-1}Var[F^{(c)}_{mn}]\\
&=\sum_{m=0}^{M-1}\sum_{n=0}^{N-1}\sigma^2\quad\text{//}F^{(c)}_{mn}\sim\mathcal N(a,\sigma^2)\\
&=MN\sigma^2;\quad0\le u<M',\ 0\le v<N'.
\end{aligned}\tag{36}$$

When $0\le u<M,0\le v<N$:

$$\begin{aligned}
SOM(H^{(c)}_{uv})-SOM(G^{(c)}_{uv})&=|\mathbb E[H^{(c)}_{uv}]|^2+Var(H^{(c)}_{uv})-\left(|\mathbb E[G^{(c)}_{uv}]|^2+Var(G^{(c)}_{uv})\right)\\
&=(a\tau_{uv})^2+MN\sigma^2-(aMN)^2\delta_{uv}-MN\sigma^2\\
&=(a\tau_{uv})^2-(aMN)^2\delta_{uv}.
\end{aligned}\tag{37}$$

// According to Equation (33), Equation (34), Equation (35) and Equation (36).

Therefore, We prove that $\forall0\le u<M,0\le v<N,u+v\ne0$

$$SOM(H^{(c)}_{uv})-SOM(G^{(c)}_{uv})=(a\tau_{uv})^2.\tag{38}$$

When $u=v=0$:

$$SOM(H^{(c)}_{uv})=SOM(G^{(c)}_{uv}).\tag{39}$$
