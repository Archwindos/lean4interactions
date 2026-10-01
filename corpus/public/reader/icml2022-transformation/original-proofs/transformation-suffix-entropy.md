• $H(\Sigma_l,\ldots,\Sigma_L)\ge H(\Sigma_{l+1},\ldots,\Sigma_L)$.

Proof.

$$\begin{aligned}
&H(\Sigma_l,\ldots,\Sigma_L)-H(\Sigma_{l+1},\ldots,\Sigma_L)\\
&=H(\Sigma_l\mid\Sigma_{l+1},\ldots,\Sigma_L)\\
&=-\mathbb E_{\sigma_l,\ldots,\sigma_L}[\log p(\sigma_l\mid\sigma_{l+1},\ldots,\sigma_L)]\\
&\ge0.
\end{aligned}\tag{12}$$
