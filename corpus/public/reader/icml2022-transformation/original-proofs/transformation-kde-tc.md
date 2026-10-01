The entanglement of transformations is formulated as

$$TC(\Sigma_l)=KL\left(p(\sigma_l)\Big\|\prod_d p(\sigma_l^d)\right)=\mathbb E_{\sigma_l}\left[\log\frac{p(\sigma_l)}{\prod_d p(\sigma_l^d)}\right].\tag{28}$$

where $p(\sigma_l^d)$ denotes the marginal distribution of the $d$-th element in $\sigma_l$. To enable fair comparisons between $I(\widehat T,X)$ computed by the KDE method in Eq. (23) and $TC(\Sigma_l)$, we also apply the KDE method to approximate $TC(\Sigma_l)$. To this end, we synthesize a new distribution $p(\widehat\sigma_l)$ to represent the distribution of $\prod_d p(\sigma_l^d)$. In $\widehat\sigma_l$, $\widehat\sigma_l^d$ in each dimension follows the Bernoulli distribution with the same activation rate $a_l^d$ with the original $\sigma_l^d$. Gating states $\widehat\sigma_l^d$ in different dimensions are independent with each other. In this way, $\prod_d p(\sigma_l^d)$ can be approximated by $p(\widehat\sigma_l)$.

Inspired by (Kolchinsky & Tracey, 2017; Kolchinsky et al., 2019), $TC(\Sigma_l)$ is quantified as the following upper bound.

$$\begin{aligned}
TC(\Sigma_l)&=\mathbb E_{\sigma_l}\left[\log\frac{p(\sigma_l)}{p(\widehat\sigma_l)}\right]\\
&\le\frac1P\sum_i\log\frac{\sum_j\exp\left(-\frac12\frac{\|\sigma_{l,i}-\sigma_{l,j}\|_2^2}{\sigma_0^2}\right)}{\sum_j\exp\left(-\frac12\frac{\|\sigma_{l,i}-\widehat\sigma_{l,j}\|_2^2}{\sigma_0^2}\right)}.
\end{aligned}\tag{29}$$

where $P$ denotes the number of samples. $\widehat\sigma_{l,i}$ denotes the synthesized gating states, which have the same activation rates with the gating states of the sample $i$.
