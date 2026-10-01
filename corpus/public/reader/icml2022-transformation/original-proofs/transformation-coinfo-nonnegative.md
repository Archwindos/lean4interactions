This section proves the three properties mentioned in Section 3 of the paper, and also gives detailed proofs for other important conclusions in the paper.

Proof. Recall that the mutual information is defined as

$$\begin{aligned}
I(X;\Sigma;Y)&=I(X;Y)-I(X;Y\mid\Sigma)\\
&=(H(Y)-H(Y\mid X))-(H(Y\mid\Sigma)-H(Y\mid X,\Sigma))\\
&=(H(Y)-H(Y\mid\Sigma))-(H(Y\mid X)-H(Y\mid X,\Sigma)).
\end{aligned}\tag{6}$$

If the DNN does not introduce additional information besides $X$, which means that $\Sigma$ is determined by $X$, then we have $H(Y\mid X)-H(Y\mid X,\Sigma)=I(\Sigma;Y\mid X)=0$. Therefore,

$$I(X;\Sigma;Y)=H(Y)-H(Y\mid\Sigma)\ge0.\tag{7}$$
