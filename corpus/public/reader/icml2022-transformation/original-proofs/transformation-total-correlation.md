• $H(\Sigma_l)$

Proof.

$$\begin{aligned}
H(\Sigma_l)+TC(\Sigma_l)&=H(\Sigma_l)+KL\left(p(\sigma_l)\Big\|\prod_d p(\sigma_l^d)\right)\\
&=\mathbb E_{\sigma_l}\left[\log\frac1{p(\sigma_l)}\right]+\mathbb E_{\sigma_l}\left[\log\frac{p(\sigma_l)}{\prod_d p(\sigma_l^d)}\right]\\
&=-\mathbb E_{\sigma_l}\left[\log\prod_d p(\sigma_l^d)\right]\quad\text{\\\\ }p(\sigma_l^d)\text{ does not depend on the input}\\
&=C_l.
\end{aligned}\tag{16}$$

Let us consider DNNs with similar activation rates $a_l^d$. Because $p(\sigma_l^d)$ follows the Bernoulli distribution with the activation rate $a_l^d$, for DNNs with similar activation rates $a_l^d$, they share similar values of $C_l$. In this case, there is a negative correlation between $H(\Sigma_l)$ and $TC(\Sigma_l)$.
