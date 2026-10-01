• $I(X;\{\Sigma_1,\ldots,\Sigma_1\})\le I(X;\{\Sigma_1,\ldots,\Sigma_{l+1}\})$.

Proof. If the DNN does not introduce additional information besides the input during the forward propagation, then $\Sigma_1,\ldots,\Sigma_l,\Sigma_{l+1}$ are all determined by $X$, thereby $H(\Sigma_1,\ldots,\Sigma_l\mid X)=H(\Sigma_1,\ldots,\Sigma_{l+1}\mid X)=0$. Therefore,

$$\begin{aligned}
&I(X;\{\Sigma_1,\ldots,\Sigma_l\})-I(X;\{\Sigma_1,\ldots,\Sigma_{l+1}\})\\
&=(H(\Sigma_1,\ldots,\Sigma_l)-H(\Sigma_1,\ldots,\Sigma_l\mid X))-(H(\Sigma_1,\ldots,\Sigma_{l+1})-H(\Sigma_1,\ldots,\Sigma_{l+1}\mid X))\\
&=H(\Sigma_1,\ldots,\Sigma_l)-H(\Sigma_1,\ldots,\Sigma_{l+1})\\
&\le0.
\end{aligned}\tag{9}$$
