• $I(X;\{\Sigma_1,\ldots,\Sigma_l\};Y)\ge I(X;\{\Sigma_1,\ldots,\Sigma_{l+1}\};Y)$.

Proof. According to Eq. (7), if there is no additional information besides the input throughout the DNN, then

$$I(X;\{\Sigma_1,\ldots,\Sigma_l\};Y)=H(Y)-H(Y\mid\{\Sigma_1,\ldots,\Sigma_l\}).\tag{10}$$

We can obtain the following inequality:

$$\begin{aligned}
&I(X;\{\Sigma_1,\ldots,\Sigma_l\};Y)-I(X;\{\Sigma_1,\ldots,\Sigma_{l+1}\};Y)\\
&=(H(Y)-H(Y\mid\{\Sigma_1,\ldots,\Sigma_l\}))-(H(Y)-H(Y\mid\{\Sigma_1,\ldots,\Sigma_{l+1}\}))\\
&=H(Y\mid\{\Sigma_1,\ldots,\Sigma_{l+1}\})-H(Y\mid\{\Sigma_1,\ldots,\Sigma_l\})\\
&=-I(\Sigma_{l+1};Y\mid\{\Sigma_1,\ldots,\Sigma_l\})\\
&\le0.
\end{aligned}\tag{11}$$
