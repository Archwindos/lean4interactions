Proof. According to Equation (27), all elements in $T^{(l,uv)}$ follow the same Gaussian distribution. Therefore, we have

$$\begin{aligned}
\mathbb E[T^{(l,uv)}]&=\mathbb E[T^{(l,uv)}_{dc}]\mathbf 1_{(C_l\times C_{l-1})}\\
&=\mu_lR_{uv}\mathbf 1_{(C_l\times C_{l-1})}.
\end{aligned}\tag{29}$$

and we have

$$\begin{aligned}
SOM(T^{(l,uv)})&=SOM(T^{(l,uv)}_{dc})\mathbf 1_{(C_l\times C_{l-1})}\\
&=(|\mu_lR_{uv}|^2+K^2\sigma_l^2)\mathbf 1_{(C_l\times C_{l-1})}.
\end{aligned}\tag{30}$$

Let us first consider the expectation of $\mathbb T^{(uv)(L:1)}$ as follows.

$$\begin{aligned}
\mathbb E[\mathbb T^{(uv)(L:1)}]&=\mathbb E[T^{(L,uv)}\mathbb T^{(uv)(L-1:1)}]\\
&=\left(C_{L-1}\mathbb E[T^{(L,uv)}_{dc}]\mathbb E[\mathbb T^{(uv)(L-1:1)}_{dc}]\right)\mathbf 1_{(C_L\times C_0)}\quad\text{//Assumption 4.1, Equation (29)}\\
&=\left(C_{L-1}\mu_lR_{uv}\mathbb E[\mathbb T^{(uv)(L-1:1)}_{dc}]\right)\mathbf 1_{(C_L\times C_0)}\quad\text{//Equation (27)}\\
&=\left(\frac1{C_L}\prod_{l=1}^{L}C_l\mu_lR_{uv}\right)\mathbf 1_{(C_L\times C_0)}\quad\text{//Assumption 4.1}.
\end{aligned}\tag{31}$$

Then, we have

$$\begin{aligned}
SOM(\mathbb T^{(uv)(L:1)})&=\mathbb E[|\mathbb T^{(uv)(L:1)}|^2]\\
&=\mathbb E[|T^{(L,uv)}\mathbb T^{(uv)(L-1:1)}|^2]\\
&=\left(C_{L-1}SOM(T^{(L,uv)}_{dc})SOM(\mathbb T^{(uv)(L-1:1)}_{dc})+C_{L-1}(C_{L-1}-1)|\mathbb E[T^{(L,uv)}_{dc}]\mathbb E[\mathbb T^{(uv)(L-1:1)}_{dc}]|^2\right)\mathbf 1_{(C_L\times C_0)}\\
&=\left(C_{L-1}(|\mu_LR_{uv}|^2+K^2\sigma_L^2)SOM(\mathbb T^{(uv)(L-1:1)}_{dc})+\frac{C_{L-1}-1}{C_{L-1}}|\mathbb E[\mathbb T^{(uv)(L:1)}_{dc}]|^2\right)\mathbf 1_{(C_L\times C_0)}\\
&=\left(\frac1{C_L}\prod_{l=1}^{L}C_l(|\mu_lR_{u,v}|^2+(K\sigma_l)^2)+\sum_{l=2}^{L}\frac{C_{l-1}-1}{C_{l-1}}\left|\frac1{C_l}\prod_{k=1}^{l}C_k\mu_kR_{u,v}\right|^2\prod_{j=l+1}^{L}C_{j-1}(|\mu_jR_{u,v}|^2+(K\sigma_j)^2)\right)\mathbf 1_{C_L\times C_0}.
\end{aligned}\tag{32}$$

// According to Assumption 4.1 and Equation (30),

// we further Assume $\forall d\ne d';c\ne c',\mathbb E[\mathbb T^{(uv)(l:1)}_{dc}\mathbb T^{(uv)(l:1)}_{d'c'}]=\mathbb E[\mathbb T^{(uv)(l:1)}_{dc}]\mathbb E[\mathbb T^{(uv)(l:1)}_{d'c'}]$.

// According to Equation (28), Equation (31).

Therefore, we prove that for the more general case that $\forall l,C_l>1$, the second-order moment $SOM(\mathbb T^{(uv)(L:1)})$ also approximately exponentially increases along with the depth of the network.
