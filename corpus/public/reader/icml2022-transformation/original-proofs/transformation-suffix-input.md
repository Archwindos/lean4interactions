• $I(T_{l-1};\{\Sigma_l,\ldots,\Sigma_L\})\ge I(T_l;\{\Sigma_{l+1},\ldots,\Sigma_L\})$.

Proof. If the DNN does not introduce additional information besides the input during the forward propagation, then $\Sigma_l,\Sigma_{l+1},\ldots,\Sigma_L$ are all determined by $T_{l-1}$, thereby $H(\Sigma_l,\ldots,\Sigma_L\mid T_{l-1})=0$. Therefore,

$$\begin{aligned}
&I(T_{l-1};\{\Sigma_l,\ldots,\Sigma_L\})-I(T_l;\{\Sigma_{l+1},\ldots,\Sigma_L\})\\
&=(H(\Sigma_l,\ldots,\Sigma_L)-H(\Sigma_l,\ldots,\Sigma_L\mid T_{l-1}))-(H(\Sigma_{l+1},\ldots,\Sigma_L)-H(\Sigma_{l+1},\ldots,\Sigma_L\mid T_l))\\
&=H(\Sigma_l,\ldots,\Sigma_L)-H(\Sigma_{l+1},\ldots,\Sigma_L)\\
&\ge0.
\end{aligned}\tag{13}$$
