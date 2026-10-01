This section introduces more details about the learning of a minimum-complexity DNN in Section 4.3 of the paper. In Section 4.3, the complexity loss is defined as

$$\mathcal L_{\mathrm{complexity}}=\sum_{l=1}^L H(\Sigma_l)=\sum_{l=1}^L\{-\mathbb E_{\sigma_l}[\log p(\sigma_l)]\}.\tag{30}$$

The exact value of $p(\sigma_l)$ is difficult to calculate. Thus, inspired by (Gao et al., 2018), we design an energy-based model (EBM) $p_{\theta_f}(\sigma_l)$ to approximate it, as follows.

$$\begin{aligned}
p_{\theta_f}(\sigma_l)&=\frac1{Z(\theta_f)}\exp[f(\sigma_l;\theta_f)]\cdot q(\sigma_l)\\
Z(\theta_f)&=\mathbb E_q[\exp[f(\sigma_l;\theta_f)]]=\int_{\sigma_l}q(\sigma_l)\exp[f(\sigma_l;\theta_f)]d\sigma_l.
\end{aligned}\tag{31}$$

where $q(\sigma_l)$ denotes the prior distribution, which is formulated as follows.

$$q(\sigma_l)=\prod_d q(\sigma_l^d),\qquad q(\sigma_l^d)=\begin{cases}\widehat p,&\sigma_l^d=1,\\1-\widehat p,&\sigma_l^d=0.\end{cases}\tag{32}$$

If we write the EBM as $p_{\theta_f}(\sigma_l)=\frac1{Z(\theta_f)}\exp[-\mathcal E(\sigma_l)]$, then the energy function is as follows.

$$\mathcal E_{\theta_f}(\sigma_l)=-\log q(\sigma_l)-f(\sigma_l;\theta_f).\tag{33}$$
