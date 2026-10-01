The first term $\mathbb E_{\theta_f}[\frac\partial{\partial\theta_f}f(\sigma_l;\theta_f)]$ in the above equation is analytically intractable and has to be approximated by MCMC, such as the Langevin dynamics.

$$\begin{aligned}
\sigma_l^{\mathrm{new}}&=\sigma_l-\frac{\Delta\tau}2\frac\partial{\partial\sigma_l}\mathcal E_{\theta_f}(\sigma_l)+\sqrt{\Delta\tau}\epsilon\\
&=\sigma_l+\frac{\Delta\tau}2\left[\frac{\partial f(\sigma_l;\theta_f)}{\partial\sigma_l}+\sum_{d=1}^D\frac1{q(\sigma_l^d)}\frac{\partial q(\sigma_l^d)}{\partial\sigma_l^d}\right]+\sqrt{\Delta\tau}\epsilon.
\end{aligned}\tag{37}$$

where $\epsilon\sim N(0,I)$ is a Gaussian white noise. $\Delta\tau$ denotes the size of the Langevin step.
