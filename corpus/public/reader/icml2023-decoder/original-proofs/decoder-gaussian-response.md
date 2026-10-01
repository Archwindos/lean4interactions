Then, we prove Theorem 4.2, as follows.



Proof. **We first prove that $T^{(l,uv)}_{dc}$ follows a Gaussian distribution of complex numbers.**

According to Assumption 4.1, each convolutional weight follows a Gaussian distribution, i.e., $W^{\mathrm{ker}=d}_{cts}\sim\mathcal N(\mu_l,\sigma_l^2)$. For the convenience of proving, let us extend $W^{\mathrm{ker}=d}_{cts}$ into an complex number. In this way, $W^{\mathrm{ker}=d}_{cts}$ follows a Gaussian distribution of complex numbers, i.e., $W^{\mathrm{ker}=d}_{cts}\sim Complex\mathcal N(\mu_l,\sigma_l^2,0)$.

Previous studies (Tse & Viswanath, 2005) proved that given $N$ complex numbers, if each complex number follows a Gaussian distribution, then the linear summation of these $N$ complex numbers also follows a Gaussian distribution of complex numbers. Since $T^{(l,uv)}_{dc}$ is a linear combination of $\forall t,s,W^{(l)[\mathrm{ker}=d]}_{cts}$, $T^{(l,uv)}_{dc}$ also follows a Gaussian distribution of complex numbers as follows.

$$\forall d,c,\qquad T^{(l,uv)}_{dc}\sim Complex\mathcal N(\hat\mu,\hat\sigma^2,r).$$

where

$$\begin{aligned}
\mu&=\mathbb E[T^{(l,uv)}_{dc}]\quad\text{//By definition of }\mu\\
&=\mathbb E\left[\sum_{t=0}^{K-1}\sum_{s=0}^{K-1}W^{(l)[\mathrm{ker}=d]}_{cts}e^{i(ut/M+vs/N)2\pi}\right]\quad\text{//Equation (19)}\\
&=\sum_{t=0}^{K-1}\sum_{s=0}^{K-1}\mathbb E[W^{(l)[\mathrm{ker}=d]}_{cts}]e^{i(ut/M+vs/N)2\pi}\\
&=\mu_l\sum_{t=0}^{K-1}\sum_{s=0}^{K-1}e^{i(ut/M+vs/N)2\pi}\quad\text{//}\mathbb E[W^{(l)[\mathrm{ker}=d]}_{cts}]=\mu_l\\
&=\mu_lR_{uv}.
\end{aligned}$$

// $\forall t\ne t'$ or $s\ne s'$: $\mathbb E[W^{(l)[\mathrm{ker}=d]}_{cts}W^{(l)[\mathrm{ker}=d]}_{ct's'}]=\mathbb E[W^{(l)[\mathrm{ker}=d]}_{cts}]\mathbb E[W^{(l)[\mathrm{ker}=d]}_{ct's'}]$.

// Let $R_{uv}=\sum_{t=0}^{K-1}\sum_{s=0}^{K-1}e^{i(ut/M+vs/N)2\pi}$.

$$\begin{aligned}
\sigma^2&=\mathbb E\left[(T^{(l,uv)}_{dc}-\mathbb E[T^{(l,uv)}_{dc}])\overline{(T^{(l,uv)}_{dc}-\mathbb E[T^{(l,uv)}_{dc}])}\right]\quad\text{//By definition of }\sigma^2\\
&=Var[T^{(l,uv)}_{dc}]\\
&=Var\left[\sum_{t=0}^{K-1}\sum_{s=0}^{K-1}W^{(l)[\mathrm{ker}=d]}_{cts}e^{i(ut/M+vs/N)2\pi}\right]\quad\text{//Equation (19)}\\
&=\sum_{t=0}^{K-1}\sum_{s=0}^{K-1}Var[W^{(l)[\mathrm{ker}=d]}_{cts}e^{i(ut/M+vs/N)2\pi}]\\
&=\sum_{t=0}^{K-1}\sum_{s=0}^{K-1}Var[W^{(l)[\mathrm{ker}=d]}_{cts}]\quad\text{//}Var[aX]=|a|^2Var[X]\\
&=\sum_{t=0}^{K-1}\sum_{s=0}^{K-1}\sigma_l^2\quad\text{//}Var[W^{(l)[\mathrm{ker}=d]}_{cts}]=\sigma_l^2\\
&=K^2\sigma_l^2.
\end{aligned}$$

// $\forall t\ne t'$ or $s\ne s'$: $\mathbb E[W^{(l)[\mathrm{ker}=d]}_{cts}W^{(l)[\mathrm{ker}=d]}_{ct's'}]=\mathbb E[W^{(l)[\mathrm{ker}=d]}_{cts}]\mathbb E[W^{(l)[\mathrm{ker}=d]}_{ct's'}]$.

$$\begin{aligned}
r&=\mathbb E\left[(T^{(l,uv)}_{dc}-\mathbb E[T^{(l,uv)}_{dc}])(T^{(l,uv)}_{dc}-\mathbb E[T^{(l,uv)}_{dc}])\right]\quad\text{//By definition of }r\\
&=C[T^{(l,uv)}_{dc}]\quad\text{//Define }C[\mathbf X]=\mathbb E[(\mathbf X-\mathbb E[\mathbf X])(\mathbf X-\mathbb E[\mathbf X])]\\
&=C\left[\sum_{t=0}^{K-1}\sum_{s=0}^{K-1}W^{(l)[\mathrm{ker}=d]}_{cts}e^{i(ut/M+vs/N)2\pi}\right]\quad\text{//Equation (19)}\\
&=\sum_{t=0}^{K-1}\sum_{s=0}^{K-1}C[W^{(l)[\mathrm{ker}=d]}_{cts}e^{i(ut/M+vs/N)2\pi}]\\
&=\sum_{t=0}^{K-1}\sum_{s=0}^{K-1}C[W^{(l)[\mathrm{ker}=d]}_{cts}]e^{i(2ut/M+2vs/N)2\pi}\quad\text{//}C[aX]=a^2C[X]\\
&=\sigma_l^2\sum_{t=0}^{K-1}\sum_{s=0}^{K-1}e^{i(2ut/M+2vs/N)2\pi}\quad\text{//}Var[W^{(l)[\mathrm{ker}=d]}_{cts}]=\sigma_l^2\\
&=\sigma_l^2R_{2u,2v}\quad\text{// }R_{uv}=\sum_{t=0}^{K-1}\sum_{s=0}^{K-1}e^{i(ut/M+vs/N)2\pi}.
\end{aligned}$$

// $\forall t\ne t'$ or $s\ne s'$: $\mathbb E[W^{(l)[\mathrm{ker}=d]}_{cts}W^{(l)[\mathrm{ker}=d]}_{ct's'}]=\mathbb E[W^{(l)[\mathrm{ker}=d]}_{cts}]\mathbb E[W^{(l)[\mathrm{ker}=d]}_{ct's'}]$.

Finally, let us consider the value of $R_{uv}$.

$$\begin{aligned}
R_{uv}&=\sum_{t=0}^{K-1}\sum_{s=0}^{K-1}e^{i(ut/M+vs/N)2\pi}\\
&=\sum_{t=0}^{K-1}e^{i(2u\pi/M)t}\sum_{s=0}^{K-1}e^{i(2v\pi/N)s}\\
&=\frac{\sin(Ku\pi/M)}{\sin(u\pi/M)}\cdot\frac{\sin(Kv\pi/N)}{\sin(v\pi/N)}\cdot e^{i((K-1)u/M+(K-1)v/N)\pi}\quad\text{//According to Equation (13)}.
\end{aligned}$$

Therefore, we prove that **$T^{(l,uv)}_{dc}$ follows a Gaussian distribution of complex numbers.**

$$\begin{gathered}
\forall d,c,\qquad T^{(l,uv)}_{dc}\sim Complex\mathcal N(\hat\mu=\mu_lR_{uv},\hat\sigma^2=K^2\sigma_l^2,r=\sigma_l^2R_{2u,2v})\\
\text{s.t. }R_{uv}=\frac{\sin(uK\pi/M)}{\sin(u\pi/M)}\frac{\sin(vK\pi/N)}{\sin(v\pi/N)}e^{i((K-1)u/M+(K-1)v/N)\pi}.
\end{gathered}\tag{27}$$


