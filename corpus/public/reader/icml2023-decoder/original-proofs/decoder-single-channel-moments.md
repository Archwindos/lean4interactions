**Then, we prove Theorem 4.2 as follows.**



According to Equation (27), $\forall d,c,l:\mathbb E[T^{(l,uv)}_{dc}]=\mu_lR_{uv},Var[T^{(l,uv)}_{dc}]=K^2\sigma_l^2$.

$$\begin{aligned}
SOM(T^{(l,uv)}_{dc})&=\mathbb E[|T^{(l,uv)}_{dc}|^2]\\
&=|\mathbb E[T^{(l,uv)}_{dc}]|^2+Var[T^{(l,uv)}_{dc}]\\
&=|\mu_lR_{uv}|^2+K^2\sigma_l^2.
\end{aligned}\tag{28}$$

Then, we have

$$\begin{aligned}
\log(SOM(\mathbb T^{(uv)(L:1)}))&=\log(\mathbb E[|\mathbb T^{(uv)(L:1)}|^2])\\
&=\log(\mathbb E[|T^{(L,uv)}\mathbb T^{(uv)(L-1:1)}|^2])\\
&=\log(\mathbb E[|T^{(L,uv)}|^2]\mathbb E[|\mathbb T^{(uv)(L-1:1)}|^2])\quad\text{//According to Assumption 4.1, and }C_l=1\\
&=\log((|\mu_LR_{uv}|^2+K^2\sigma_L^2)SOM(\mathbb T^{(uv)(L-1:1)}))\quad\text{//Equation (28)}\\
&=\log\left(\prod_{l=1}^{L}|\mu_lR_{uv}|^2+K^2\sigma_l^2\right)\\
&=\sum_{l=1}^{L}\log(|\mu_lR_{uv}|^2+K^2\sigma_l^2).
\end{aligned}$$


