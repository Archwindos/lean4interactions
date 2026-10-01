If the DNN does not introduce additional complexity besides the input $X$, we have $H(\Sigma_l\mid X)=0$, $I(X;\Sigma_l)=H(\Sigma_l)-H(\Sigma_l\mid X)=H(\Sigma_l)$. If the DNN introduces additional complexity (e.g. using the sampling operation in VAE, or the dropout operation), then $I(X;\Sigma_l)$ can be quantified as follows.

$$I(X;\Sigma_l)\le-\frac1n\sum_{j=1}^n\log\frac1n\sum_{k=1}^n\exp\left(-\frac12\frac{\|\widehat\sigma_{l,j}-\widehat\sigma_{l,k}\|_2^2}{\sigma_0^2}\right).\tag{26}$$

where $\widehat\sigma_{l,j}$ and $\widehat\sigma_{l,k}$ represent the vectorized gating states when sampling operations are removed (in this way, we can use the method of measuring $H(\Sigma_l)$ to quantify $I(X;\Sigma_l)$).
