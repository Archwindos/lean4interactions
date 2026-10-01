To enable the computation of $\frac{\partial\sigma_{l,i}}{\partial\theta_{DNN}}$ and $\frac{\partial q(\sigma_{l,i}^d)}{\partial\sigma_{l,i}^d}$, we can approximate the ReLU operation using the following Swish function (Ramachandran et al., 2017).

$$\begin{aligned}
\sigma_l&\approx\operatorname{sigmoid}(\beta x)\\
\operatorname{ReLU}(x)&=x\odot\sigma_l\approx x\odot\operatorname{sigmoid}(\beta x).
\end{aligned}\tag{41}$$

where $\odot$ denotes the element-wise multiplication.

According to Eq. (32), the prior distribution $q(\sigma_l)$ is approximated as follows.

$$q(\sigma_l^d)\approx1-\widehat p+\sigma_l^d(2\widehat p-1),\qquad\frac{\partial q(\sigma_l^d)}{\partial\sigma_l^d}\approx2\widehat p-1.\tag{42}$$
