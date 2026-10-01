Let $\theta_{\mathrm{DNN}}$ denote parameters in the DNN. The gradient of $\theta_{\mathrm{DNN}}$ can be calculated as follows.

$$\frac{\partial Loss}{\partial\theta_{\mathrm{DNN}}}=-\frac1n\sum_{l=1}^L\sum_{i=1}^n\left\{\frac{\partial f(\sigma_l;\widehat\theta_f)}{\partial\sigma_{l,i}}+\sum_d^D\frac1{q(\sigma_{l,i}^d)}\frac{\partial q(\sigma_{l,i}^d)}{\partial\sigma_{l,i}^d}\right\}\frac{\partial\sigma_{l,i}}{\partial\theta_{\mathrm{DNN}}}.\tag{40}$$

We consider $Z(\theta_f)$ as a constant in the computation of $\frac{\partial Loss}{\partial\widehat\theta_{\mathrm{DNN}}}$.
