Then, the Monte Carlo approximation to $\frac{\partial L(\theta_f)}{\partial\theta_f}$ is given as follows.

$$\begin{aligned}
\frac{\partial L(\theta_f)}{\partial\theta_f}&\approx\frac1n\sum_{i=1}^n\frac\partial{\partial\theta_f}f(\widetilde\sigma_{l,i};\theta_f)-\frac1n\sum_{i=1}^n\frac\partial{\partial\theta_f}f(\sigma_{l,i};\theta_f)\\
&=\frac\partial{\partial\theta_f}\left[\frac1n\sum_{i=1}^n\mathcal E_{\theta_f}(\sigma_{l,i})-\frac1n\sum_{i=1}^n\mathcal E_{\theta_f}(\widetilde\sigma_{l,i})\right].
\end{aligned}\tag{38}$$

where $\widetilde\sigma_{l,i}$ is the sample synthesized via Langevin dynamics.
