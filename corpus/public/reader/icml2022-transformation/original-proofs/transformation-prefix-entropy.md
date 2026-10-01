• $H(\Sigma_1,\ldots,\Sigma_l)\le H(\Sigma_1,\ldots,\Sigma_{l+1})$.

Proof.

$$\begin{aligned}
&H(\Sigma_1,\ldots,\Sigma_l)-H(\Sigma_1,\ldots,\Sigma_{l+1})\\
&=-H(\Sigma_{l+1}\mid\Sigma_1,\ldots,\Sigma_l)\\
&=\mathbb E_{\sigma_1,\ldots,\sigma_{l+1}}[\log p(\sigma_{l+1}\mid\sigma_1,\ldots,\sigma_l)]\\
&\le0.
\end{aligned}\tag{8}$$
