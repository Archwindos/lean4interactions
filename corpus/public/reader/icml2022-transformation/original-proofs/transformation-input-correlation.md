• $I(X;\Sigma_l)$

Proof.

$$\begin{aligned}
I(X;\Sigma_l)+TC(\Sigma_l)&=H(\Sigma_l)-H(\Sigma_l\mid X)+KL\left(p(\sigma_l)\Big\|\prod_d p(\sigma_l^d)\right)\\
&=C_l-H(\Sigma_l\mid X).
\end{aligned}\tag{17}$$

If the DNN does not introduce additional information through the layerwise propagation, then the $X$ determines $\Sigma_l$, i.e. $H(\Sigma_l\mid X)=0$. Thus, for DNNs with similar values of $C_l$, there is a negative correlation between $I(X;\Sigma_l)$ and $TC(\Sigma_l)$.
