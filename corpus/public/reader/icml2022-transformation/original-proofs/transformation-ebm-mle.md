The EBM can be learned via the maximum likelihood estimation (MLE) with the following loss.

$$\widehat\theta_f=\mathop{\arg\max}_{\theta_f}L(\theta_f)=\mathop{\arg\max}_{\theta_f}\frac1n\sum_{i=1}^n\log p_{\theta_f}(\sigma_{l,i}).\tag{34}$$

where $n$ denotes the number of samples. $\sigma_{l,i}$ is a vector, which represents gating states in the $l$-th gating layer for the $i$-th sample.

The loss and gradient of $\theta_f$ can be calculated as follows.

$$L(\theta_f)=-\frac1n\sum_{i=1}^n\log p_{\theta_f}(\sigma_{l,i})=-\frac1n\sum_{i=1}^n[f(\sigma_{l,i};\theta_f)+\log q(\sigma_{l,i})]+\log Z(\theta_f).\tag{35}$$

$$\frac{\partial L(\theta_f)}{\partial\theta_f}=\mathbb E_{\theta_f}\left[\frac\partial{\partial\theta_f}f(\sigma_l;\theta_f)\right]-\frac1n\sum_{i=1}^n\frac\partial{\partial\theta_f}f(\sigma_{l,i};\theta_f).\tag{36}$$

where $\frac\partial{\partial\theta_f}\log Z(\theta_f)=\mathbb E_{\theta_f}[\frac\partial{\partial\theta_f}f(\sigma_l;\theta_f)]$.
