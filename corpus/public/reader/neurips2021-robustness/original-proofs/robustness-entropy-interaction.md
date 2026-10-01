Proof:
$$\begin{aligned}I_{ij}^{(m)}&=E_S[v(S\cup\{i,j\})-v(S\cup\{i\})-v(S\cup\{j\})+v(S)]\\&=E_S[-H(Y\mid X_S,X_i,X_j)+H(Y\mid X_S,X_i)+H(Y\mid X_S,X_j)-H(H\mid X_S)]\\&=E_S[H(Y\mid X_S,X_j)-H(Y\mid X_S,X_j,X_i)+H(Y\mid X_S,X_i)-H(Y\mid X_S)]\\&=E_S[MI(X_i;Y\mid X_S,X_j)-MI(X_i;Y\mid X_S)]\\&=E_S[MI(X_i;X_j;Y\mid X_S)].\end{aligned}$$

The conditional mutual information $MI(X_i;X_j;Y\mid X_S)$ measures the remaining mutual information between $X_i,X_j$ and $Y$ when $X_S$ is given. Note that unlike the bivariate mutual information, $MI(X_i;X_j;Y\mid X_S)$ can be negative.
