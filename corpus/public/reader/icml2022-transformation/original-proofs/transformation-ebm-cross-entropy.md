Thus, the loss for the learning of the DNN can be rewritten as follows.

$$\begin{aligned}
\mathcal L_{\mathrm{complexity}}&=-\sum_{l=1}^L\mathbb E_{\sigma_l}[\log p_{\widehat\theta_f}(\sigma_l)]\\
&=\frac1n\sum_{l=1}^L\sum_{i=1}^n[\mathcal E_{\widehat\theta_f}(\sigma_{l,i})+\log Z(\widehat\theta_f)]\\
&=-\frac1n\sum_{l=1}^L\sum_{i=1}^n[f(\sigma_{l,i};\widehat\theta_f)+\log q(\sigma_{l,i})-\log Z(\widehat\theta_f)].
\end{aligned}\tag{39}$$
