• $I(T_{l-1};\{\Sigma_l,\ldots,\Sigma_L\};Y)\ge I(T_l;\{\Sigma_{l+1},\ldots,\Sigma_L\};Y)$.

Proof. According to Eq. (7), if there is no additional information besides the input throughout the DNN, then

$$I(T_{l-1};\{\Sigma_l,\ldots,\Sigma_L\};Y)=H(Y)-H(Y\mid\{\Sigma_l,\ldots,\Sigma_L\}).\tag{14}$$

We can obtain the following inequality:

$$\begin{aligned}
&I(T_{l-1};\{\Sigma_l,\ldots,\Sigma_L\};Y)-I(T_l;\{\Sigma_{l+1},\ldots,\Sigma_L\};Y)\\
&=(H(Y)-H(Y\mid\{\Sigma_l,\ldots,\Sigma_L\}))-(H(Y)-H(Y\mid\{\Sigma_{l+1},\ldots,\Sigma_L\}))\\
&=H(Y\mid\{\Sigma_{l+1},\ldots,\Sigma_L\})-H(Y\mid\{\Sigma_l,\ldots,\Sigma_L\})\\
&=I(\Sigma_l;Y\mid\{\Sigma_{l+1},\ldots,\Sigma_L\})\\
&\ge0.
\end{aligned}\tag{15}$$
