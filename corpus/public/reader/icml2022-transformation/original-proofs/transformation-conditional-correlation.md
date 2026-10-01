• $I(X;\Sigma_l;Y)$

Proof. According to the definition of $I(X;\Sigma_l;Y)$, we have

$$I(X;\Sigma_l;Y)=I(X;\Sigma_l)-I(X;\Sigma_l\mid Y).\tag{18}$$

We have discussed the first term $I(X;\Sigma_l)$ above, so we focus on the second term $I(X;\Sigma_l\mid Y)$, which measures the complexity of transformations that are unrelated to the inference. Similarly, the entanglement of the inference-irrelevant transformations is represented by

$$TC(\Sigma_l\mid Y)=\mathbb E_y\left(KL\left(p(\sigma_l\mid y)\Big\|\prod_d p(\sigma_l^d\mid y)\right)\right).\tag{19}$$

Then, we have

$$\begin{aligned}
&I(X;\Sigma_l\mid Y)+TC(\Sigma_l\mid Y)\\
&=H(\Sigma_l\mid Y)-H(\Sigma_l\mid X,Y)+TC(\Sigma_l\mid Y)\\
&=\mathbb E_y\left[H(\Sigma_l\mid y)+KL\left(p(\sigma_l\mid y)\Big\|\prod_d p(\sigma_l^d\mid y)\right)\right]-H(\Sigma_l\mid X,Y)\\
&=\mathbb E_{\sigma_l,y}\left[\log\frac1{p(\sigma_l\mid y)}+\log\frac{p(\sigma_l\mid y)}{\prod_d p(\sigma_l^d\mid y)}\right]-H(\Sigma_l\mid X,Y)\\
&=-\mathbb E_{\sigma_l,y}\left[\log\prod_d p(\sigma_l^d\mid y)\right]-H(\Sigma_l\mid X,Y)\\
&=C_{l\mid Y}-H(\Sigma_l\mid X,Y).
\end{aligned}\tag{20}$$

If there is no additional information besides the input in the DNN, then $H(\Sigma_l\mid X,Y)=0$. Thus, we have

$$\begin{aligned}
I(X;\Sigma_l)+TC(\Sigma_l)&=C_l-H(\Sigma_l\mid X)=C_l\\
I(X;\Sigma_l\mid Y)+TC(\Sigma_l\mid Y)&=C_{l\mid Y}-H(\Sigma_l\mid X,Y)=C_{l\mid Y}.
\end{aligned}\tag{21}$$

Therefore,

$$\begin{aligned}
I(X;\Sigma_l;Y)&=I(X;\Sigma_l)-I(X;\Sigma_l\mid Y)\\
&=(C_l-TC(\Sigma_l))-(C_{l\mid Y}-TC(\Sigma_l\mid Y))\\
&=(C_l-C_{l\mid Y})-\underbrace{(TC(\Sigma_l)-TC(\Sigma_l\mid Y))}_{\text{multi-variate mutual information used to infer }Y}.
\end{aligned}\tag{22}$$

where the difference between $TC(\Sigma_l)$ and $TC(\Sigma_l\mid Y)$ represents the entanglement of the transformations that are used to infer $Y$. For DNNs with similar activation rates, we can also roughly consider that these DNNs share similar values of $C_l$ and $C_{l\mid Y}$. Thus, we can conclude that the higher complexity makes the DNN use more disentangled transformation for inference.
