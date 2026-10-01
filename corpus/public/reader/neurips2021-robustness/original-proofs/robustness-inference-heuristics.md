Cheng et al. [11] has also proven that low-order interactions (local collaborations) mainly reflect simple and common concepts (features), and high-order interactions (global collaborations) usually represent complex and global features.

Note that in Proposition 1, we set $\widehat v(S)=H(Y\mid X_S)$, which is slightly different from setting $v(S)=\log p(y=y^{\mathrm{truth}}\mid S,x)$ in Section 4.1. Nevertheless, the trend of $v(S)$ can roughly reflect the negative trend of $\widehat v(S)$, which is discussed in the supplementary material.

According to Proposition 1, $\widehat v(S)=H(Y\mid X_S)$ denotes the entropy of the classification probability given variables in $S$ of the image $x$. Thus, $\widehat v(S)$ measures the uncertainty of the prediction. If the model prediction is correct and confident, i.e. the value of $v(S)=\log p(y=y^{\mathrm{truth}}\mid x,S)$ is large, then the uncertainty $\widehat v(S)$ is very low. In comparison, if the model prediction is correct but with a small value of $v(S)$, then the uncertainty is large, yielding a large value of $\widehat v(S)$. Therefore, the trend of $v(S)$ can roughly reflect the negative trend of $\widehat v(S)$ when the model prediction is correct.

This indicates that $\phi^{(n-1)}(i\mid x)$ contains the interaction components with the highest order ($m=n-2$), which are not included in Shapley values with orders lower than $n-1$. Section 4.1 of the paper has pointed that high-order interactions are the most sensitive to adversarial perturbations, thereby enabling the detection of adversarial examples.

Thus, the dropout operation can remove sensitive interaction components of the DNN, thereby reducing the attacking utility of perturbations and correcting the network output.
