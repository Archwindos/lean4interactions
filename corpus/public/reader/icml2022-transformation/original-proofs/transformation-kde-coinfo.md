Similarly, the complexity $I(X;\Sigma_l;Y)$ can be estimated by its upper bound:

$$\begin{aligned}
I(X;\Sigma_l;Y)&=I(\Sigma_l;Y)-I(\Sigma_l;Y\mid X)\\
&=H(\Sigma_l)-H(\Sigma_l\mid Y)-I(\Sigma_l;Y\mid X)\\
&\le-\frac1n\sum_{j=1}^n\log\frac1n\sum_{k=1}^n\exp\left(-\frac12\frac{\|\sigma_{l,j}-\sigma_{l,k}\|_2^2}{\sigma_0^2}\right)\\
&\quad-\sum_{m=1}^M p_m\left[-\frac1{n_m}\sum_{j,\,Y_j=m}\log\frac1{n_m}\sum_{k,\,Y_k=m}\exp\left(-\frac12\frac{\|\sigma_{l,j}-\sigma_{l,k}\|_2^2}{\sigma_0^2}\right)\right]\\
&\quad-I(\Sigma_l;Y\mid X).
\end{aligned}\tag{27}$$

For the task of multi-category classification, $M$ denotes the number of categories. $n_m$ is the number of training samples belonging to the $m$-th category, and $p_m=n_m/M$. If the DNN does not introduce additional complexity besides the input, we have $I(\Sigma_l;Y\mid X)=0$.
