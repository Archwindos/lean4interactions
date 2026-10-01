"""Paper-specific source transcription, semantic maps and adapters for F01."""
from pathlib import Path

def finish(p):
 rows={r['id']:r for r in p.rows}
 def original(key,statement,proof=None):
  r=rows['robustness-'+key];r['original_statement_md']=statement
  if proof is not None:
   r['original_proof_md']=proof;r['original_proof_source_type']='complete_manual_formal_proof_transcription'
   (p.D/'original-proofs'/(r['id']+'.md')).write_text(proof+'\n')
 # All author chains below retain author notation, typos and parentheses.
 original('interaction-linearity',r'''(1) Linearity property: If we merge outputs of two DNNs, $u(S)=w(S)+v(S)$, then, $\forall i,j\in N$, the interaction $I_{ij,u}^{(m)}$ w.r.t. the new output $u$ can be decomposed into $I_{ij,u}^{(m)}=I_{ij,w}^{(m)}+I_{ij,v}^{(m)}$.''',r'''Proof:
$$\begin{aligned}I_{ij,u}^{(m)}&=E_{S\subseteq N\setminus\{i,j\},|S|=m}[\Delta u(S,i,j)]\\&=E_{S\subseteq N\setminus\{i,j\},|S|=m}[\Delta v(i,j,S)+\Delta w(S,i,j)]\\&=I_{ij,v}^{(m)}+I_{ij,w}^{(m)}.\end{aligned}$$''')
 original('interaction-nullity',r'''(2) Nullity property: The dummy variable $i\in N$ satisfies $\forall S\subseteq N\setminus\{i\}$, $v(S\cup\{i\})=v(S)+v(\{i\})$. It means that the variable $i$ has no interactions with other variables, i.e. $\forall j\in N$, $I_{ij}^{(m)}=0$.''',r'''Proof:
$$\begin{aligned}I_{ij}^{(m)}&=E_{S\subseteq N\setminus\{i,j\},|S|=m}[v(S\cup\{i,j\})-v(S\cup\{i\})-v(S\cup\{j\})+v(S)]\\&=E_{S\subseteq N\setminus\{i,j\},|S|=m}\left[v(S\cup\{j\}\cup\{i\})-v(S\cup\{j\})-\left(v(S\cup\{i\})-v(S)\right)\right]\\&=E_{S\subseteq N\setminus\{i,j\},|S|=m}[v(\{i\})-v(\{i\})]=0.\end{aligned}$$''')
 original('interaction-commutativity',r'''(3) Commutativity property: $\forall i,j\in N$, $I_{ij}^{(m)}=I_{ji}^{(m)}$.''',r'''Proof:
$$\begin{aligned}I_{ij}^{(m)}&=E_{S\subseteq N\setminus\{i,j\},|S|=m}[v(S\cup\{i,j\})-v(S\cup\{i\})-v(S\cup\{j\})+v(S)]\\&=E_{S\subseteq N\setminus\{i,j\},|S|=m}[v(S\cup\{i,j\})-v(S\cup\{j\})-v(S\cup\{i\})+v(S)]\\&=I_{ji}^{(m)}.\end{aligned}$$''')
 original('interaction-symmetry',r'''(4) Symmetry property: If input variables $i,j\in N$ have same cooperations with other variables $\forall S\subseteq N\setminus\{i,j\}$, $v(S\cup\{i\})=v(S\cup\{j\})$, then they have same interactions, $\forall k\in N\setminus\{i,j\}$, $I_{ik}^{(m)}=I_{jk}^{(m)}$.''',r'''Proof:
$$\begin{aligned}I_{ik}^{(m)}&=E_{S\subseteq N\setminus\{i,j\},|S|=m}[\Delta v(i,k,S)]\\&=\frac{m!(n-2-m)!}{(n-2)!}\sum_{S\subseteq N\setminus\{i,k\},|S|=m}\Delta v(i,k,S)\\&=\frac{m!(n-2-m)!}{(n-2)!}\left(\sum_{S\subseteq N\setminus\{i,j,k\},|S|=m-1}\Delta v(i,k,S\cup\{j\})+\sum_{S\subseteq N\setminus\{i,j,k\},|S|=m}\Delta v(i,k,S)\right)\\&=\frac{m!(n-2-m)!}{(n-2)!}\left(\sum_{S\subseteq N\setminus\{i,j,k\},|S|=m-1}\Delta v(j,k,S\cup\{i\})+\sum_{S\subseteq N\setminus\{i,j,k\},|S|=m}\Delta v(j,k,S)\right)\\&=E_{S\subseteq N\setminus\{i,j\},|S|=m}[\Delta v(j,k,S)]\\&=I_{jk}^{(m)}.\end{aligned}$$''')
 original('shapley-linearity',r'''(1) Linearity property: If we merge the outputs of two DNNs $u(S)=w(S)+v(S)$, then the Shapley values of input variables also can be added, i.e. $\forall i\in N$, $\phi_u^{(m)}(i)=\phi_w^{(m)}(i)+\phi_v^{(m)}(i)$.''',r'''Proof:
$$\begin{aligned}\phi_u^{(m)}(i)&=E_{S\subseteq N\setminus\{i\},|S|=m}[u(S\cup\{i\})-u(S)]\\&=E_{S\subseteq N\setminus\{i\},|S|=m}[w(S\cup\{i\})+v(S\cup\{i\})-w(S)-v(S)]\\&=E_S[w(S\cup\{i\})-w(S)]+E_S[v(S\cup\{i\})-v(S)]\\&=\phi_w^{(m)}(i)+\phi_v^{(m)}(i).\end{aligned}$$
Both $E_S$ in the third line retain $S\subseteq N\setminus\{i\},|S|=m$.''')
 original('shapley-nullity',r'''(2) Nullity property: An input variable $i\in N$ is considered as a dummy player if $\forall S\subseteq N\setminus\{i\}$, $v(S\cup\{i\})=v(S)+v(\{i\})$. Thus, the variable $i$ has no interactions with other variables, i.e. $\phi^{(m)}(i)=v(\{i\})$.''',r'''Proof:
$$\phi^{(m)}(i)=E_{S\subseteq N\setminus\{i\},|S|=m}[v(S\cup\{i\})-v(S)]=E_{S\subseteq N\setminus\{i\},|S|=m}[v(\{i\})]=v(\{i\}).$$''')
 original('shapley-symmetry',r'''(3) Symmetry property: Given two input variables $i,j\in N$, if these two variables have same cooperations with all other variables $\forall S\subseteq N\setminus\{i,j\}$, $v(S\cup\{i\})=v(S\cup\{j\})$, then $\phi^{(m)}(i)=\phi^{(m)}(j)$.''',r'''Proof:
$$\begin{aligned}\phi^{(m)}(i)&=E_{S\subseteq N\setminus\{i\},|S|=m}[v(S\cup\{i\})-v(S)]\\&=\frac{m!(n-1-m)!}{(n-1)!}\sum_{S\subseteq N\setminus\{i\},|S|=m}[v(S\cup\{i\})-v(S)]\\&=\frac{m!(n-1-m)!}{(n-1)!}\left(\sum_{S\subseteq N\setminus\{i,j\},|S|=m-1}[v(S\cup\{i,j\})-v(S,j)]+\sum_{S\subseteq N\setminus\{i,j\},|S|=m}[v(S\cup\{i\})-v(S)]\right)\\&=\frac{m!(n-1-m)!}{(n-1)!}\left(\sum_{S\subseteq N\setminus\{i,j\},|S|=m-1}[v(S\cup\{i,j\})-v(S,i)]+\sum_{S\subseteq N\setminus\{i,j\},|S|=m}[v(S\cup\{j\})-v(S)]\right)\\&=E_{S\subseteq N\setminus\{j\},|S|=m}[v(S\cup\{j\})-v(S)]=\phi^{(m)}(j).\end{aligned}$$''')
 original('shapley-efficiency',r'''(4) Efficiency property: The overall reward can be assigned to all players, $\frac1n\sum_{i\in N}\sum_{m=0}^{n-1}\phi^{(m)}(i)=v(N)-v(\varnothing)$.''',r'''Proof:
$$v(N)-v(\varnothing)=\sum_{i\in N}\phi(i)=\frac1n\sum_{i\in N}\sum_{m=0}^{n-1}\phi^{(m)}(i).$$''')
 original('marginal-attribution',r'''(1) Marginal attribution property: The marginal attribution of the $(m+1)$-th order Shapley values beyond the $m$-th order is equal to the average interaction of the $m$-th order between $i$ and all other variables. $\forall i,j\in N$, $i\ne j$, $\phi^{(m+1)}(i)-\phi^{(m)}(i)=E_{j\in N\setminus\{i\}}[I_{ij}^{(m)}]$.''',r'''Proof:
$$\begin{aligned}\phi^{(m+1)}(i)-\phi^{(m)}(i)&=E_{S'\subseteq N\setminus\{i\},|S'|=m+1}[v(S'\cup\{i\})-v(S')]-E_{S\subseteq N\setminus\{i\},|S|=m}[v(S\cup\{i\})-v(S)]\\&=E_{S\subseteq N\setminus\{i\},|S|=m}\left[E_{j\in N\setminus(S\cup\{i\})}[v(S\cup\{j\}\cup\{i\})-v(S\cup\{j\})]\right]-E_S[v(S\cup\{i\})-v(S)]\\&=E_SE_{j\in N\setminus(S\cup\{i\})}[v(S\cup\{j\}\cup\{i\})-v(S\cup\{j\})-v(S\cup\{i\})+v(S)]\\&=E_SE_{j\in N\setminus(S\cup\{i\})}[\Delta v(i,j,S)]\\&=E_{j\in N\setminus\{i\}}E_{S\subseteq N\setminus\{i,j\},|S|=m}[\Delta v(i,j,S)]\\&=E_{j\in N\setminus\{i\}}[I_{ij}^{(m)}].\end{aligned}$$
In the middle lines $E_S$ retains $S\subseteq N\setminus\{i\},|S|=m$.''')
 original('accumulation',r'''(2) Accumulation property: The $m$-th ($m>0$) order Shapley value of the variable $i\in N$ can be decomposed into interactions of lower orders, $\phi^{(m)}(i)=E_{j\in N\setminus\{i\}}[\sum_{k=0}^{m-1}I_{ij}^{(k)}]+\phi^{(0)}(i)$.''',r'''Proof:
$$\begin{aligned}\phi^{(m)}(i)&=\phi^{(m)}(i)-\phi^{(m-1)}(i)+\phi^{(m-1)}(i)-\phi^{(m-2)}(i)+\cdots-\phi^{(0)}(i)+\phi^{(0)}(i)\\&=E_j[I_{ij}^{(m-1)}]+E_j[I_{ij}^{(m-2)}]+\cdots+E_j[I_{ij}^{(0)}]+\phi^{(0)}(i)\\&=E_{j\in N\setminus\{i\}}\left[\sum_{k=0}^{m-1}I_{ij}^{(k)}\right]+\phi^{(0)}(i).\end{aligned}$$
Every $E_j$ is over $j\in N\setminus\{i\}$.''')
 original('interaction-efficiency',r'''(5) Efficiency property: The output of the DNN can be decomposed into interactions of different orders,
$$v(N)=v(\varnothing)+\sum_{i\in N}\phi^{(0)}(i)+\sum_{i\in N}\sum_{j\in N\setminus\{i\}}\left[\sum_{m=0}^{n-2}\frac{n-1-m}{n(n-1)}I_{ij}^{(m)}\right],\qquad\phi^{(0)}(i)\overset{\rm def}=v(i)-v(\varnothing).$$''',r'''Proof:
$$\begin{aligned}v(N)&=v(\varnothing)+\frac1n\sum_{i\in N}\sum_{m=0}^{n-1}\phi^{(m)}(i)\\&=v(\varnothing)+\frac1n\sum_i\phi^{(0)}(i)+\frac1n\sum_i\sum_{m=1}^{n-1}\left[E_{j\in N\setminus\{i\}}\left[\sum_{k=0}^{m-1}I_{ij}^{(k)}\right]+\phi^{(0)}(i)\right]\\&=v(\varnothing)+\sum_i\phi^{(0)}(i)+\frac1{n(n-1)}\sum_i\sum_{j\in N\setminus\{i\}}\sum_{m=1}^{n-1}\left[\sum_{k=0}^{m-1}I_{ij}^{(k)}\right]\\&=v(\varnothing)+\sum_i\phi^{(0)}(i)+\sum_i\sum_{j\in N\setminus\{i\}}\left[\sum_{m=0}^{n-2}\frac{n-1-m}{n(n-1)}I_{ij}^{(m)}\right].\end{aligned}$$
All unqualified $\sum_i$ are over $i\in N$.''')
 # B.4 original statement includes its probability/entropy scope, not fixed-sample output.
 original('entropy-interaction',r'''When a DNN outputs a probability distribution, we prove that the interaction between input variables can be represented in the form of mutual information. Without loss of generality, let us take the image classification task for example. Let $x\in\mathcal X\subseteq\mathbb R^n$ denote an input image of the DNN. $x_i$ denotes the $i$-th pixel, and $X_i=\{x_i\}$. $\forall S\subseteq N$, we define $X_S=\{x_S\mid x\in\mathcal X\}$; each $x_S$ represents the image, where pixels in $S$ remain unchanged, and other pixels $j\in N\setminus S$ are masked following settings of [1]. Let $y\in Y=\{y^1,\ldots,y^C\}$ denote the network prediction. Given $x_S$ as the input, $p(y\mid x_S)$ denotes the output probability of the DNN. Let us set
$$v(S)=H(Y\mid X_S)=\sum_{x_S}p(x_S)H(Y\mid X_S=x_S),$$
which measures the entropy of $y$ given the input $x_S$. Then we prove that
$$I_{ij}^{(m)}=E_{S\subseteq N\setminus\{i,j\},|S|=m}[MI(X_i;X_j;Y\mid X_S)].\tag{6}$$''',r'''Proof:
$$\begin{aligned}I_{ij}^{(m)}&=E_S[v(S\cup\{i,j\})-v(S\cup\{i\})-v(S\cup\{j\})+v(S)]\\&=E_S[-H(Y\mid X_S,X_i,X_j)+H(Y\mid X_S,X_i)+H(Y\mid X_S,X_j)-H(H\mid X_S)]\\&=E_S[H(Y\mid X_S,X_j)-H(Y\mid X_S,X_j,X_i)+H(Y\mid X_S,X_i)-H(Y\mid X_S)]\\&=E_S[MI(X_i;Y\mid X_S,X_j)-MI(X_i;Y\mid X_S)]\\&=E_S[MI(X_i;X_j;Y\mid X_S)].\end{aligned}$$
Every expectation has $S\subseteq N\setminus\{i,j\},|S|=m$. The source's $H(H\mid X_S)$ and signs are preserved.

The conditional mutual information $MI(X_i;X_j;Y\mid X_S)$ measures the remaining mutual information between $X_i,X_j$ and $Y$ when $X_S$ is given. Note that unlike the bivariate mutual information, $MI(X_i;X_j;Y\mid X_S)$ can be negative.''')
 original('exclusive-shared-benefits',r'''When $X_S$ (each $x_S\in X_S$ containing $m$ pixels) is given, we can roughly understand the conditional mutual information $MI(X_{\{i,j\}};Y\mid X_S)$ as the additional benefits from $X_i$ and $X_j$ to classification. We prove that it can be decomposed into the exclusive benefits of $X_i$, $MI(X_i;Y\mid X_j,X_S)$, the exclusive benefits of $X_j$, $MI(X_j;Y\mid X_i,X_S)$, and the benefit shared by $X_i$ and $X_j$, $MI(X_i;X_j;Y\mid X_S)$. Thus, the latter can be considered as the benefits from the interaction between $X_i$ and $X_j$.
$$MI(X_{\{i,j\}};Y\mid X_S)=MI(X_i;Y\mid X_j,X_S)+MI(X_j;Y\mid X_i,X_S)+MI(X_i;X_j;Y\mid X_S).\tag{7}$$''',r'''Proof:
$$\begin{aligned}\mathrm{right}&=MI(X_i;Y\mid X_j,X_S)+MI(X_j;Y\mid X_i,X_S)+MI(X_i;X_j;Y\mid X_S)\\&=MI(X_i;Y\mid X_j,X_S)+MI(X_j;Y\mid X_i,X_S)+MI(X_i;Y\mid X_S)-MI(X_i;Y\mid X_j,X_S)\\&=MI(X_i;Y\mid X_j,X_S)+MI(X_i;Y\mid X_S)\\&=\sum_{x_i,x_j,x_S,y}p(x_i,x_j,x_S,y)\log\frac{p(x_j,y\mid x_i,x_S)}{p(x_j\mid x_i,x_S)p(y\mid x_i,x_S)}+\sum_{x_i,x_S,y}p(x_i,x_S,y)\log\frac{p(x_i,y\mid x_S)}{p(x_i\mid x_S)p(y\mid x_S)}\\&=\sum_{x_i,x_j,x_S,y}p(x_i,x_j,x_S,y)\log\frac{p(x_j,y\mid x_i,x_S)}{p(x_j\mid x_i,x_S)p(y\mid x_i,x_S)}+\sum_{x_i,x_j,x_S,y}p(x_i,x_j,x_S,y)\log\frac{p(x_i,y\mid x_S)}{p(x_i\mid x_S)p(y\mid x_S)}\\&=\sum_{x_i,x_j,x_S,y}p(x_i,x_j,x_S,y)\log\frac{p(x_j,y\mid x_i,x_S)p(x_i,y\mid x_S)}{p(x_j\mid x_i,x_S)p(y\mid x_i,x_S)p(x_i\mid x_S)p(y\mid x_S)}\\&=\sum_{x_i,x_j,x_S,y}p(x_i,x_j,x_S,y)\log\frac{p(x_j,y\mid x_i,x_S)p(x_i,y\mid x_S)p(x_i,x_S)p(x_S)}{p(x_j\mid x_i,x_S)p(y\mid x_i,x_S)p(x_i\mid x_S)p(y\mid x_S)p(x_i,x_S)p(x_S)}\\&=\sum_{x_i,x_j,x_S,y}p(x_i,x_j,x_S,y)\log\frac{p(x_i,x_j,x_S,y)p(x_i,x_S,y)}{p(x_j\mid x_i,x_S)p(x_i,x_S,y)p(x_i\mid x_S)p(y\mid x_S)p(x_S)}\\&=\sum_{x_i,x_j,x_S,y}p(x_i,x_j,x_S,y)\log\frac{p(x_i,x_j,x_S,y)}{p(x_j\mid x_i,x_S)p(x_i\mid x_S)p(y\mid x_S)p(x_S)}\\&=\sum_{x_i,x_j,x_S,y}p(x_i,x_j,x_S,y)\log\frac{p(x_i,x_j,y\mid x_S)}{p(x_i,x_j\mid x_S)p(y\mid x_S)}\\&=MI(X_{\{i,j\}};Y\mid X_S)=\mathrm{left}.\end{aligned}$$
The source's third line prints $X_i$ in its first exclusive term even though the following logarithm uses $X_j$; that mismatch is retained.''')
 original('delta-average',r'''In section 4.1 of the paper, we propose the metric $I^{(m)}=E_{x\in\Omega}E_{i,j}[I_{ij}^{(m)}(x)]$, and $\Delta I^{(m)}\overset{\rm def}=I_{\rm nor}^{(m)}-I_{\rm adv}^{(m)}$, which measures the difference in interactions between normal samples and adversarial examples. We prove
$$\Delta I^{(m)}=E_{x\in\Omega}E_{i,j}[\Delta I_{ij}^{(m)}(x)],\quad\Delta I_{ij}^{(m)}(x)=I_{ij}^{(m)}(x)-I_{ij}^{(m)}(x_{\rm adv}).\tag{8}$$''',r'''Proof:
$$\begin{aligned}\Delta I^{(m)}&=I_{\rm nor}^{(m)}-I_{\rm adv}^{(m)}\\&=E_{x\in\Omega_{\rm nor}}E_{i,j}[I_{ij}^{(m)}(x)]-E_{x\in\Omega_{\rm adv}}E_{i,j}[I_{ij}^{(m)}(x)]\\&=E_{x\in\Omega_{\rm nor}}E_{i,j}[I_{ij}^{(m)}(x)]-E_{x\in\Omega_{\rm nor}}E_{i,j}[I_{ij}^{(m)}(x+\Delta x)]\\&=E_{x\in\Omega_{\rm nor}}E_{i,j}[I_{ij}^{(m)}(x)-I_{ij}^{(m)}(x+\Delta x)]\\&=E_{x\in\Omega_{\rm nor}}E_{i,j}[I_{ij}^{(m)}(x)-I_{ij}^{(m)}(x_{\rm adv})]\\&=E_{x\in\Omega_{\rm nor}}E_{i,j}[\Delta I_{ij}^{(m)}(x)].\end{aligned}$$''')
 original('dropout-expansion',r'''Given the input sample $x\in\mathbb R^n$ and the dropout rate $\alpha$, let $\mathcal K=\{K\mid K\subset N,|K|=\lfloor(1-\alpha)n\rfloor\}$ denote all possible sets of remained variables after the dropout operation. Let $v^\alpha(N\mid x)=E_{K\in\mathcal K}[v(K\mid x)]$ denote the average network output among all inputs after the dropout operation with rate $\alpha$. According to the efficiency property,
$$v(N\mid x)=v(\varnothing\mid x)+\sum_{i\in N}\phi^{(0)}(i\mid x)+\sum_{i\ne j\in N}\sum_{m=0}^{n-2}\frac{n-1-m}{n(n-1)}I_{ij,N}^{(m)}(x).\tag{12}$$
Here $I_{ij,N}^{(m)}(x)$ denotes the $m$-order interaction with all variables $N$. Similarly,
$$v(K\mid x)=v(\varnothing\mid x)+\sum_{i\in K}\phi^{(0)}(i\mid K,x)+\sum_{i\ne j\in K}\sum_{m=0}^{k-2}\frac{k-1-m}{k(k-1)}I_{ij,K}^{(m)}(x),\quad k=|K|=\lfloor(1-\alpha)n\rfloor.\tag{13}$$
The following source derivation claims Equations (14)–(15), retained below even where it changes $k$ to $(1-\alpha)n$.''',r'''Thus,
$$\begin{aligned}v^\alpha(N\mid x)&=E_{K\in\mathcal K}[v(K\mid x)]\\&=E_K\left[v(\varnothing\mid x)+\sum_{i\in K}\phi^{(0)}(i\mid K,x)+\sum_{i\ne j\in K}\sum_{m=0}^{k-2}\frac{k-1-m}{k(k-1)}I_{ij,K}^{(m)}(x)\right]\\&=v(\varnothing\mid x)+E_K\left[\sum_{i\in K}(v(i\mid x)-v(\varnothing\mid x))\right]+E_K\left[\sum_{i\ne j\in K}\sum_{m=0}^{k-2}\frac{k-1-m}{k(k-1)}I_{ij,K}^{(m)}(x)\right]\\&=v(\varnothing\mid x)+E_{K\subset N,k=(1-\alpha)n}\left[\sum_{i\in K}\phi^{(0)}(i\mid x)\right]+E_{K\subset N,k=(1-\alpha)n}\left[\sum_{i\ne j\in K}\sum_{m=0}^{k-2}\frac{k-1-m}{k(k-1)}I_{ij,K}^{(m)}(x)\right]\\&=v(\varnothing\mid x)+(1-\alpha)\sum_{i\in N}\phi^{(0)}(i\mid x)+E_{K\subset N,k=(1-\alpha)n}\left[\sum_{i\ne j\in K}\sum_{m=0}^{k-2}\frac{k-1-m}{k(k-1)}I_{ij,K}^{(m)}(x)\right]\\&=v(\varnothing\mid x)+(1-\alpha)\sum_{i\in N}\phi^{(0)}(i\mid x)+E_{K\subset N,k=(1-\alpha)n}\left[\sum_{i\ne j\in K}\sum_{m=0}^{k-2}\frac{k-1-m}{k(k-1)}E_{S\subseteq K\setminus\{i,j\},|S|=m}[\Delta v(i,j,S\mid x)]\right]\\&=v(\varnothing\mid x)+(1-\alpha)\sum_{i\in N}\phi^{(0)}(i\mid x)+\frac{k(k-1)}{n(n-1)}\sum_{i\ne j\in N}\sum_{m=0}^{k-2}\frac{k-1-m}{k(k-1)}E_{K\subset N,k=(1-\alpha)n}E_{S\subseteq K\setminus\{i,j\},|S|=m}[\Delta v(i,j,S\mid x)]\\&=v(\varnothing\mid x)+(1-\alpha)\sum_{i\in N}\phi^{(0)}(i\mid x)+\sum_{i\ne j\in N}\sum_{m=0}^{k-2}\frac{k-1-m}{n(n-1)}E_{K\subset N,k=(1-\alpha)n}E_{S\subseteq K\setminus\{i,j\},|S|=m}[\Delta v(i,j,S\mid x)]\\&=v(\varnothing\mid x)+(1-\alpha)\sum_{i\in N}\phi^{(0)}(i\mid x)+\sum_{i\ne j\in N}\sum_{m=0}^{k-2}\frac{k-1-m}{n(n-1)}E_{S\subset N\setminus\{i,j\},|S|=m}[\Delta v(i,j,S\mid x)]\\&=v(\varnothing\mid x)+(1-\alpha)\sum_{i\in N}\phi^{(0)}(i\mid x)+\sum_{i\ne j\in N}\sum_{m=0}^{k-2}\frac{k-1-m}{n(n-1)}I_{ij,N}^{(m)}(x).\tag{14}\end{aligned}$$
Thus, the change in the network output caused by dropout can be represented as follows:
$$\begin{aligned}v(N\mid x)-v^\alpha(N\mid x)&=\alpha\sum_{i\in N}\phi^{(0)}(i,x)+\sum_{i\ne j\in N}\left[\sum_{m=0}^{n-2}\frac{n-1-m}{n(n-1)}I_{ij,N}^{(m)}(x)-\sum_{m=0}^{k-2}\frac{k-1-m}{n(n-1)}I_{ij,N}^{(m)}(x)\right]\\&=\alpha\sum_{i\in N}\phi^{(0)}(i,x)+\sum_{i\ne j\in N}\sum_{m=0}^{k-2}\frac{n-k}{n(n-1)}I_{ij,N}^{(m)}(x)+\sum_{i\ne j\in N}\sum_{m=k-1}^{n-2}\frac{n-1-m}{n(n-1)}I_{ij,N}^{(m)}(x)\\&=\alpha\sum_{i\in N}\phi^{(0)}(i,x)+\frac\alpha{n-1}\sum_{i\ne j\in N}\sum_{m=0}^{k-2}I_{ij,N}^{(m)}(x)+\sum_{i\ne j\in N}\sum_{m=k-1}^{n-2}\frac{n-1-m}{n(n-1)}I_{ij,N}^{(m)}(x).\tag{15}\end{aligned}$$
The final sum is labelled “high-order interactions” in the source. According to Eq. (15), the dropout operation removes all high-order interactions ($m>(1-\alpha)n-2$), while slightly affects low-order interactions. Thus, the dropout operation can remove sensitive interaction components of the DNN, thereby reducing the attacking utility of perturbations and correcting the network output.''')
 # Classic A statements are externally attributed; the paper supplies no proofs.
 classic=[
 ('linearity','经典Shapley线性与缩放','Classical Shapley linearity and scaling',r'\phi_{v+w}(i)=\phi_v(i)+\phi_w(i),\quad\phi_{c\cdot u}(i)=c\phi_u(i)',r'If two independent games can be merged into one game $u(S)=v(S)+w(S)$, then $\forall i\in N$, $\phi_u(i)=\phi_v(i)+\phi_w(i)$; $\forall c\in\mathbb R$, $\phi_{c\cdot u}(i)=c\cdot\phi_u(i)$.',['shapley_linearity','shapley_homogeneity'],('对m阶边际逐项线性及缩放，然后使用真实factorial Shapley到等阶平均适配；不要求两个确定性游戏有概率独立性。','Use linearity and scaling of each order-wise marginal, then the exact factorial-Shapley/order-average adapter. No probabilistic independence of deterministic games is required.')),
 ('dummy','经典Shapley dummy','Classical Shapley dummy property',r'\phi(i)=v(\{i\})-v(\varnothing)',r'The dummy player $i$ satisfies $\forall S\subseteq N\setminus\{i\}$, $v(S\cup\{i\})=v(S)+v(\{i\})$, which indicates that the player $i$ has no interactions with other players, $\phi(i)=v(\{i\})-v(\varnothing)$.',['source_shapley_dummy'],('原dummy条件在空上下文强制b=0；原结论仍显式写g({i})−b。以每阶常数边际及等阶平均证明。','The source dummy condition forces b=0 at the empty context. The source conclusion still retains g({i})−b. Prove the constant marginal at every order and use the order average.')),
 ('symmetry','经典Shapley合作对称性','Classical Shapley cooperation symmetry',r'\phi(i)=\phi(j)',r'If $\forall S\subseteq N\setminus\{i,j\}$, $v(S\cup\{i\})=v(S\cup\{j\})$, then $\phi(i)=\phi(j)$.',['shapley_symmetry'],('弱合作相等推出有限上下文交换双射下的边际相等；每阶归因相同后取等阶平均。','Weak cooperation equality gives equal marginals under the context-swap bijection. Average the equal order-wise attributions.')),
 ('efficiency','经典Shapley效率','Classical Shapley efficiency',r'\sum_{i\in N}\phi(i)=v(N)-v(\varnothing)',r'The overall reward can be assigned to all players, $\sum_{i\in N}\phi(i)=v(N)-v(\varnothing)$.',['shapley_efficiency'],('现有factorial Shapley到dividend allocation等价适配与真实重构效率给出总和g(N)−b；不删除非零基线。','Use the existing exact equivalence with dividend allocation and its reconstruction efficiency, obtaining g(N)−b with a possibly nonzero baseline.'))]
 for key,z,e,tex,src,ln,st in classic:
  rr=p.result('robustness-classical-'+key,z,e,'supplement A externally attributed property',tex,[('supplement',[1],'A Shapley properties; Weber[22]')],[(st[0],st[1],'',['Harsanyi.Robustness.'+n for n in ln])],kind='external_statement_with_project_proof',assumptions=[('有限玩家集合N及i∈N；按原factorial权重定义经典φ。本条的原前提逐字保留在原陈述。','A finite player set N and i∈N; classical φ uses the source factorial weights. This entry retains its original premise verbatim in the source statement.')],original=src,lean=['Harsanyi.Robustness.'+n for n in ln]);rows[rr['id']]=rr
 rr=p.result('robustness-classical-uniqueness','Weber唯一性外引','Weber uniqueness citation','supplement A; Weber[22]',r'\text{Shapley is the unique allocation satisfying the four source axioms.}',[('supplement',[1,16],'A;reference[22]')],[('原文明确归给Weber[22]，本篇没有本地唯一性证明。四条性质在本项目另证，不由此自动得到唯一性；唯一性也不由有限平均等式自动推出。','The source attributes uniqueness to Weber [22] and gives no local proof. The four axioms are proved separately in this project; neither those individual checks nor the finite average identity automatically establish uniqueness.','')],kind='external_theorem_scope',role='scope_analysis',assessment='externally_attributed_not_locally_proved',original='Weber [22] has proven that the Shapley value is a unique method to fairly allocate overall reward to each player that satisfies following properties.');rows[rr['id']]=rr
 rr=p.result('robustness-shapley-interaction-orders','经典pair index差值及多阶平均','Classical pair-index difference and its order average','supplement B.1 Eqs.(2),(3)',r'I(i,j)=\widetilde\phi(i)_{j\text{ present}}-\widetilde\phi(i)_{j\text{ absent}}=\frac1{n-1}\sum_{m=0}^{n-2}I_{ij}^{(m)}',[('supplement',[2],'B.1 Shapley interaction index;[6],[25]')],[('两种φ均在同一缩减玩家集N\{j}计算，present游戏是R↦g(Rj)，absent游戏是R↦g(R)。不能把present玩家数仍设n而改变归一化。','Both values use the reduced player set N\{j}. The present game is R↦g(Rj), and the absent game is R↦g(R). Keeping n players in the present game would change the normalization.',''),('用factorial Shapley的等阶平均拆开这两个归因；同阶相减四项恰是Δg(i,j,S)。上下文为N\{i,j}，归一化每阶1/(n−1)。','Apply the exact order decomposition to both factorial Shapley values. Subtract the same-order marginals to obtain the four-term Δg(i,j,S), with contexts excluding i,j and order normalization 1/(n−1).','',['Harsanyi.Robustness.shapley_interaction_orders'])],assumptions=[('不同i,j∈N，n≥2，经典Shapley采用原Eq1 factorial定义。','Distinct i,j∈N, n≥2, and classical Shapley uses the source Equation (1) factorial definition.')],original=r'''Shapley interaction index [6] measures whether absence/presence of $j$ changes the importance of $i$:
$$I(i,j)=\widetilde\phi(i)_{j\text{ always present}}-\widetilde\phi(i)_{j\text{ always absent}}.\tag{2}$$
Both quantities are conditional Shapley values as described in the source. Note that $I(i,j)=I(j,i)$. Zhang et al. [25] decomposed the index into interactions of different orders,
$$I_{ij}^{(m)}=E_{S\subseteq N\setminus\{i,j\},|S|=m}[\Delta v(i,j,S)],\quad\Delta v(i,j,S)\overset{\rm def}=v(S\cup\{i,j\})-v(S\cup\{i\})-v(S\cup\{j\})+v(S).\tag{3}$$
The equal-order-average equation is the project's explicit adaptation of these source definitions, not an extra numbered formula printed in B.1.''',lean=['Harsanyi.Robustness.shapley_interaction_orders']);rows[rr['id']]=rr
 id=p.issue('robustness-self-pair-quantifier','Nullity显示量词与双玩家定义域','The displayed nullity quantifier and the two-player domain','domain_ambiguity',r'\forall j\in N,\ I_{ij}^{(m)}=0','supplement PDF3 B.1 Nullity statement','原文字说other variables，但显示∀j∈N包含j=i。pair的原上下文大小范围n−2及两玩家解释要求i≠j；若硬扩成自配对，Δ(i,i,S)=g(S)−g(Si)，dummy增量非零时不为0。原量词照录，适配的i≠j是双玩家domain，不是补入以救自配对扩张。','The prose says other variables, while the display includes j=i. The source two-player interpretation and n−2 context range use distinct players. A literal self-pair extension gives Δ(i,i,S)=g(S)−g(Si), which is nonzero for a nonzero dummy increment. The displayed quantifier is retained; the adapter’s distinct-player premise records the pair domain rather than proving the self-pair extension.','仅量词/定义域歧义，双玩家nullity仍有效。','This is a quantifier/domain ambiguity; two-player nullity remains valid.',['robustness-interaction-nullity'])
 rows['robustness-interaction-nullity']['related_issue_ids'].append(id)
 id=p.issue('robustness-benefit-cancellation-typo','Eq7取消后的exclusive变量误植','Wrong exclusive variable after cancellation in Equation (7)','proof_error',r'\mathrm{right}=MI(X_i;Y\mid X_j,X_S)+MI(X_i;Y\mid X_S)','supplement PDF7 Eq7 proof third line','取消Xi exclusive后应留下MI(Xj;Y|Xi,XS)，原第三行却仍写Xi。下一行log分子p(xj,y|xi,xS)已经使用正确Xj。重写以四熵恒等式消去该误植，原链照录。','After cancelling the Xi exclusive term, the remaining exclusive term is MI(Xj;Y|Xi,XS). The third line still prints Xi, while its next logarithm uses Xj correctly. The rewrite uses the four-entropy identity and retains the original chain.','只修作者证明变量，不改Eq7原命题及co-information约定。','Only the proof variable is repaired; Equation (7) and its co-information convention remain intact.',['robustness-exclusive-shared-benefits'])
 rows['robustness-exclusive-shared-benefits']['related_issue_ids'].append(id)
 # Actual paper adapters, rather than a generic algebraic lemma labelled as a full proof.
 adapters={
 'interaction-linearity':['interaction_linearity','interaction_homogeneity'],
 'interaction-nullity':['interaction_dummy','source_dummy_baseline'],
 'interaction-commutativity':['interaction_commutativity'],
 'interaction-symmetry':['interaction_symmetry'],
 'shapley-linearity':['attribution_linearity'],
 'shapley-nullity':['attribution_dummy','source_dummy_baseline'],
 'shapley-symmetry':['attribution_symmetry'],
 'shapley-orders':['shapley_orders'],
 'shapley-efficiency':['attribution_efficiency'],
 'marginal-attribution':['attribution_recurrence'],
 'accumulation':['attribution_accumulation'],
 'interaction-efficiency':['interaction_efficiency'],
 'attacking-decomposition':['source_attack_decomposition'],
 'entropy-interaction':['entropy_interaction'],
 'exclusive-shared-benefits':['entropy_shared_benefit'],
 'delta-average':['average_sub'],
 'detector-attribution':['attribution_top'],
 'dropout-expansion':['fixed_size_floor_counterexample','fixed_size_cardinal_mean','cardinal_game_interaction'],
 'disentanglement':['disentanglement_bounds','disentanglement_zero_domain']}
 for key,names in adapters.items():
  r=rows['robustness-'+key];r['lean']['declarations']=['Harsanyi.Robustness.'+n for n in names]
  for st in r['proof_steps']:
   # Replace provisional entropy algebra references with the actual entropy-game adapter.
   st['lean_refs']=[n for n in st['lean_refs'] if not n.startswith('Harsanyi.Entropy.')]
  r['proof_steps'][-1]['lean_refs']=list(r['lean']['declarations'])
 # Source definitions and project definitions are explicitly separated.
 objects={
 'game':(r'固定标量模型v、输入x及输入mask基线r；$x_S$在S内保留x，其余取r。定义$g_x(S)=v(x_S)$，$b=v(x_\varnothing)$，$g_{x,0}=g_x-b$，不假设b=0。',r'Fix a scalar model v, an input x and an input-mask baseline r. The masked input x_S keeps x on S and uses r elsewhere. Define $g_x(S)=v(x_S)$, $b=v(x_\varnothing)$ and $g_{x,0}=g_x-b$, without assuming b=0.'),
 'contexts':(r'设$N$是有限玩家集，$n=|N|$；$\mathcal C(R,m)=\{S\subseteq R:|S|=m\}$。均匀平均是$|\mathcal C|^{-1}\sum_{S\in\mathcal C}$，只在m≤|R|时对应原概率平均。',r'Let N be a finite player set with n=|N|. Write $\mathcal C(R,m)=\{S\subseteq R:|S|=m\}$. The uniform average is $|\mathcal C|^{-1}\sum_{S\in\mathcal C}$; it represents the source probabilistic average only when m≤|R|.'),
 'pair':(r'定义$\Delta g(i,j,S)=g(Sij)-g(Si)-g(Sj)+g(S)$与$I_{ij}^{(m)}=E_{S\in\mathcal C(N\setminus\{i,j\},m)}\Delta g$。Sij是S∪{i,j}；i≠j，m是上下文大小，并非dividend的集合阶数。',r'Define $\Delta g(i,j,S)=g(Sij)-g(Si)-g(Sj)+g(S)$ and $I_{ij}^{(m)}=E_{S\in\mathcal C(N\setminus\{i,j\},m)}\Delta g$. Sij means S∪{i,j}; i≠j, and m is context size rather than dividend-coalition order.'),
 'phi':(r'定义$\phi^{(m)}(i)=E_{S\in\mathcal C(N\setminus\{i\},m)}[g(Si)-g(S)]$，0≤m≤n−1。经典$\phi(i)$采用原Eq1的factorial权重，不把任一单阶归因自动称为经典Shapley。',r'Define $\phi^{(m)}(i)=E_{S\in\mathcal C(N\setminus\{i\},m)}[g(Si)-g(S)]$, with 0≤m≤n−1. Classical φ(i) uses the source Equation (1) factorial weights; a single-order attribution is not automatically the classical Shapley value.'),
 'entropy':(r'本条改用分布平均熵游戏$H_Y(S)=H(Y\mid X_S)=E[-\sum_y p(y\mid X_S)\log p(y\mid X_S)]$。此条件期望对输入分布积分，不要求输入空间有限；原离散数据情形等于$\sum_{x_S}p(x_S)[-\sum_y p(y\mid x_S)\log p(y\mid x_S)]$。它不是某个固定x的单次模型输出g_x。零质量项按0log0=0，条件熵须有限。条件MI定义为$H_Y(S)-H_Y(Si)$，co-information定义为该量减去$H_Y(Sj)-H_Y(Sij)$，采用原Eq7约定。',r'This entry uses the population entropy game $H_Y(S)=H(Y\mid X_S)=E[-\sum_y p(y\mid X_S)\log p(y\mid X_S)]$. This conditional expectation integrates over the input law and does not require a finite input space; the source discrete-data case is $\sum_{x_S}p(x_S)[-\sum_y p(y\mid x_S)\log p(y\mid x_S)]$. It is distinct from a single fixed-input output g_x. Zero-mass terms use 0log0=0, and the conditional entropies must be finite. Conditional MI is $H_Y(S)-H_Y(Si)$, and co-information subtracts $H_Y(Sj)-H_Y(Sij)$, as in the source Equation (7).'),
 'joint':('标准Shannon条件信息要求这些条件分布来自同一联合律。原文本把不同mask的DNN概率写作p(y|x_S)，并未另证其联合兼容性。Lean的原等式适配证明任意有限实值条件熵表上的四项恒等式，不构造任意DNN mask输出的共同联合律；本文使用此条件信息语义时保留该原隐含对象要求。','Standard Shannon conditional information uses conditional laws from one common joint distribution. The source writes probabilities from different DNN masks as p(y|x_S), but does not separately prove their joint compatibility. The Lean adapter proves the four-term identity for any finite real conditional-entropy table; it does not construct a common joint law for arbitrary masked network outputs. The source’s implicit conditional-information object requirement remains visible.'),
 'attack':(r'使用同一scalar输出与mask规则的normal游戏g及attacked游戏a；$\Delta I=I_g-I_a$，原攻击效用亦为g(N)−a(N)，方向一致。各自空mask输出a(∅)、g(∅)都保留。',r'Use a normal game g and an attacked game a with the same scalar output and mask rule. Define $\Delta I=I_g-I_a$, and the source attack utility is g(N)−a(N), with the same direction. Retain both empty-mask outputs a(∅),g(∅).'),
 'dropout':(r'原dropout均匀取固定大小K⊂N，$k=\lfloor(1-\alpha)n\rfloor$，$v^\alpha=E_{|K|=k}g_x(K)$。反例用n=4,α=2/5,k=2及真实游戏g_x(S)=|S|，而非Bernoulli保留模型。',r'The source dropout samples a fixed-size subset K⊂N uniformly, with $k=\lfloor(1-\alpha)n\rfloor$ and $v^\alpha=E_{|K|=k}g_x(K)$. The counterexample uses n=4, α=2/5, k=2 and the actual game g_x(S)=|S|, not Bernoulli retention.'),
 'ratio':('对每个样本/pair令A=均匀平均Δg，B=均匀平均|Δg|。原局部ratio=|A|/B，D(m)再平均样本及不同pair。B=0时原定义没有约定。','For each sample and pair, let A be the uniform average of Δg and B the uniform average of |Δg|. The source local ratio is |A|/B, and D(m) then averages over samples and distinct pairs. The source gives no convention when B=0.')}
 all_pair=['game','contexts','pair'];all_phi=['game','contexts','phi']
 for id,r in rows.items():
  key=id.removeprefix('robustness-')
  if key in ['entropy-interaction','exclusive-shared-benefits']:ks=['contexts','pair','entropy','joint'];prem=('原B4的分布平均conditional-entropy游戏、不同i,j∈N及0≤m≤n−2；采用Eq7的co-information约定。X可来自Rⁿ，形式化不添加X有限的假设。','The population conditional-entropy game in source B.4, distinct i,j∈N and 0≤m≤n−2, using Equation (7)’s co-information convention. X may range in ℝⁿ; no finite-input-type premise is added.')
  elif key=='dropout-expansion':ks=all_pair+['phi','dropout'];prem=('原固定大小均匀dropout和floor；反例全部参数及游戏见定义，保留原错误陈述。','The source fixed-size uniform dropout and floor; all counterexample parameters and the game are defined below, with the faulty statement retained.')
  elif key=='disentanglement':ks=all_pair+['ratio'];prem=('原双玩家及合法m上下文；原ratio定义域问题保留，正分母仅属于辅助比值界的范围。','The source distinct-player domain and admissible m-contexts; retain the original ratio-domain issue. Positive denominator is the scope of the auxiliary ratio bound only.')
  elif key=='delta-average':ks=all_pair+['attack'];prem=('同一有限normal样本总体逐一攻击，adv总体为它的同权配对pushforward；同一pair及context平均。','Attack each member of the same finite normal population; the adversarial population is its paired pushforward with the same weights. Use identical pair and context averages.')
  elif key=='attacking-decomposition':ks=all_pair+['phi','attack'];prem=('n≥2，原同一标量输出在normal/adv输入的两个游戏，各自完整输出及基线保留；没有概率分布或零输出基线假设。','n≥2 and the two games from the same scalar output at normal/adversarial inputs, retaining both full outputs and baselines; no probability-law or zero-output-baseline premise.')
  elif key=='detector-attribution':ks=all_phi;prem=('i∈N，类别c由原x固定选定，两输出均用同c；mask第i输入坐标为0，不重新选类别。','i∈N, and c is fixed from the original x and used in both outputs. Mask input coordinate i to zero without reselecting the category.')
  elif key.startswith('classical-') or key.startswith('shapley-'):ks=all_phi;prem=('有限非空N及目标玩家i∈N；φ(m)定义域0≤m≤n−1。每条dummy/合作对称/线性前提按原陈述另行适配，未把这些性质作为待证结论加入假设。','A finite nonempty N with target i∈N, and the order-wise domain 0≤m≤n−1. Each entry separately adapts its source dummy/cooperation-symmetry/linearity premise; the target property is not placed among the assumptions.')
  else:ks=all_pair+(['phi'] if key in ['multiorder-definitions','marginal-attribution','accumulation','interaction-efficiency'] else []);prem=('有限N、n≥2；pair为不同i,j∈N，pair阶0≤m≤n−2。递推的m+1≤n−1，累积的0≤m≤n−1；各性质的额外原前提逐条保留于原陈述。','A finite N with n≥2, distinct pair players i,j∈N and pair orders 0≤m≤n−2. Recurrence uses m+1≤n−1 and accumulation uses 0≤m≤n−1; each property’s additional source premise is retained in its source statement.')
  r['assumptions']=[{'id':id+'-assumption-1','body_md':prem[0]}];r['translations']['en']['assumptions']=[{'id':id+'-assumption-1','body_md':prem[1]}]
  r['definitions']=[{'id':id+'-definition-'+k,'body_md':objects[k][0]} for k in ks]
  r['translations']['en']['definitions']=[{'id':id+'-definition-'+k,'body_md':objects[k][1]} for k in ks]
  for a,b in zip(r['proof_steps'],r['translations']['en']['proof_steps']):
   a['justification']=a['body_md'];b['justification']=b['body_md']
  r['rewrite_status']='complete'
  r['original_statement_source_type']='complete_manual_source_statement_transcription' if r['original_statement_md'][:2]!='$$' else 'source_formula_transcription_with_original_premises_in_assumptions'
  scope=('对应原命题的有限集合/条件熵恒等式适配；实际声明量词和条件见类型审计。' if r['rewrite_role']=='proof' else '原陈述保留；这里只提供反例或准确定义域/外引/经验范围分析。')
  scope_en=('The finite-set or conditional-entropy identity adapts the original target; the type audit records its exact quantifiers and conditions.' if r['rewrite_role']=='proof' else 'The source statement is retained; the evidence provides the displayed counterexample or precise domain, external, or empirical scope analysis.')
  if key in ['entropy-interaction','exclusive-shared-benefits']:
   scope='完整四项条件熵恒等式，沿原Eq7的信息定义适配；不构造任意masked网络输出的共同joint law。'
   scope_en='The complete four-conditional-entropy identity under the source Equation (7) information convention. It does not construct a common joint law for arbitrary masked network outputs.'
  r['scope']=scope;r['translations']['en']['scope']=scope_en
  if r['lean']['declarations']:
   r['lean']['scope']=scope_en;r['lean']['evidence_role']='theorem' if r['rewrite_role']=='proof' else 'counterexample' if r['rewrite_role']=='counterexample' else 'partial'
  if key in ['interaction-symmetry','shapley-symmetry']:r['shared_proof_ids']=['robustness-context-relabeling']
  elif key in ['marginal-attribution','accumulation','interaction-efficiency','dropout-expansion']:r['shared_proof_ids']=['robustness-flagged-context-counting']
  elif key in ['entropy-interaction','exclusive-shared-benefits']:r['shared_proof_ids']=['robustness-four-entropy-identity']
 # Explicit extra premises for the individual property, instead of a generic placeholder.
 specific={
 'interaction-linearity':('原合并游戏u=w+v逐个S成立。','The source merged game satisfies u=w+v at every S.'),
 'interaction-nullity':('原dummy条件∀R⊆N\{i},g(Ri)=g(R)+g({i})；i≠j是pair domain。','The source dummy premise is ∀R⊆N\{i},g(Ri)=g(R)+g({i}); i≠j is the pair domain.'),
 'interaction-symmetry':('i,j,k∈N且k不同于i,j；∀R⊆N\{i,j},g(Ri)=g(Rj)。','i,j,k∈N, with k distinct from i,j; ∀R⊆N\{i,j},g(Ri)=g(Rj).'),
 'shapley-linearity':('原游戏u=w+v逐个S成立，m∈[0,n−1]。','The source game satisfies u=w+v at every S, with m∈[0,n−1].'),
 'shapley-nullity':('∀R⊆N\{i},g(Ri)=g(R)+g({i})，m∈[0,n−1]。','∀R⊆N\{i},g(Ri)=g(R)+g({i}), with m∈[0,n−1].'),
 'shapley-symmetry':('i,j∈N，∀R⊆N\{i,j},g(Ri)=g(Rj)，m∈[0,n−1]。','i,j∈N, ∀R⊆N\{i,j},g(Ri)=g(Rj), and m∈[0,n−1].'),
 'classical-linearity':('原u=v+w；缩放c是任意实数。','The source merged game is u=v+w; the scaling c is any real scalar.'),
 'classical-dummy':('∀R⊆N\{i},g(Ri)=g(R)+g({i})，原特殊dummy条件不变。','∀R⊆N\{i},g(Ri)=g(R)+g({i}), retaining the source’s specific dummy premise.'),
 'classical-symmetry':('i,j∈N，∀R⊆N\{i,j},g(Ri)=g(Rj)。','i,j∈N and ∀R⊆N\{i,j},g(Ri)=g(Rj).')}
 for key,(z,e) in specific.items():
  r=rows['robustness-'+key];aid=r['id']+'-source-premise'
  r['assumptions'].append({'id':aid,'body_md':z});r['translations']['en']['assumptions'].append({'id':aid,'body_md':e})
 original('attacking-decomposition',r'''According to the efficiency property, we can decompose the overall utility of adversarial perturbations on the network output into elementary effects on interactions:
$$\Delta v(N\mid x)\overset{\rm def}=v(N\mid x)-v(N\mid x_{\rm adv})=\Delta v(\varnothing\mid x)+\sum_{i\in N}\Delta\phi^{(0)}(i\mid x)+\sum_{i\ne j\in N}\sum_{m=0}^{n-2}\Delta J_{ij}^{(m)}(x).\tag{3}$$
Here $x\in\mathbb R^n$ is the normal sample and $x_{\rm adv}=x+\Delta x$ the adversarial example. The first term $\Delta v(\varnothing)=v(\varnothing\mid x)-v(\varnothing\mid x_{\rm adv})=0$. The second term is
$$\Delta\phi^{(0)}(i\mid x)\overset{\rm def}=(v(\{i\}\mid x)-v(\varnothing\mid x))-(v(\{i\}\mid x_{\rm adv})-v(\varnothing\mid x_{\rm adv}))=v(\{i\}\mid x)-v(\{i\}\mid x_{\rm adv}).$$
Because in most applications the importance of a single variable is usually small, we can ignore this term. In the third term,
$$\Delta J_{ij}^{(m)}(x)\overset{\rm def}=\frac{n-1-m}{n(n-1)}\Delta I_{ij}^{(m)}(x),\quad\Delta I_{ij}^{(m)}(x)\overset{\rm def}=I_{ij}^{(m)}(x)-I_{ij}^{(m)}(x_{\rm adv}).$$
The second sum is labelled “usually can be ignored”; this is retained as an empirical qualification, not an exact cancellation.''')
 # Scope annotations tied to the exact audited type.
 exactscope={
 'delta-average':('实际Lean证明同一有限均匀样本索引的average_sub；adv通过原配对x↦xadv表示。任意不同权重或独立抽样总体不在该声明内。','Lean proves average_sub for the same finite uniform sample index, with adversarial values represented by the paired map x↦xadv. Different weights or independently sampled populations are outside that declaration.'),
 'dropout-expansion':('真实Fin4固定size游戏均值与floor反例，另有任意cardinalGame的零pair交互声明；不证明原Eq14/15，也未形式化一般修订dropout计数公式。','The actual Fin4 fixed-size mean and floor counterexample, plus zero pair interactions for cardinalGame. It does not prove source Equations (14)–(15), and no general corrected dropout expansion is claimed formalized.'),
 'disentanglement':('真实有限平均三角界只覆盖正分母局部ratio；另证全零分母，原全域D定义未被当作有效定理。','The finite-average triangle bound covers a local ratio with positive denominator, and a separate declaration proves its all-zero denominator. The total source definition of D is not treated as a valid theorem.'),
 'shapley-interaction-orders':('同一缩减玩家集上的两个factorial Shapley值之差，实际类型明确i,j∈N且i≠j；准确接原Eq2差值及Eq3平均。','The difference of two factorial Shapley values on the same reduced player set. The actual type requires i,j∈N and i≠j, adapting the source Equation (2) difference and Equation (3) context average.')}
 for key,(z,e) in exactscope.items():
  r=rows['robustness-'+key];r['scope']=z;r['translations']['en']['scope']=e;r['lean']['scope']=e
 # Fully translated symbol records; original author TeX is intentionally unchanged.
 symbolspec=[
 ('model-output','sym-model','v','固定标量模型','Fixed scalar model','v:X\\to\\mathbb R','模型输出的一个固定scalar维度。','A fixed scalar dimension of the model output.','X→ℝ','X→ℝ','固定模型','Fixed model','v',[4,5],'game',[]),
 ('fixed-input','sym-input','x','正常固定输入','Fixed normal input','x\\in\\mathcal X','正常样本；对抗样本为xadv=x+Δx。','The normal sample; the adversarial sample is xadv=x+Δx.','输入域X','Input domain X','固定样本','Fixed sample','x',[4,5],'game',[]),
 ('input-baseline-vector','sym-input-baseline','r','输入mask基线','Input-mask baseline','x_\\varnothing=r','所有mask使用同一输入基线。','All masks use the same input baseline.','输入域X中的向量','A vector in input domain X','掩码输入','Masked inputs','mask settings',[4],'game',[]),
 ('variable-universe','sym-universe','N','玩家总体','Player universe','N=\\{1,\\ldots,n\\}','有限输入变量集合。','The finite set of input variables.','有限集','Finite set','各固定输入游戏','Each fixed-input game','N',[4,5],'contexts',[]),
 ('variable-count','variable-count','n','玩家数','Number of players','n=|N|','上下文归一化的总体大小。','The universe size used in context normalization.','自然数；pair条目n≥2','Natural number; pair entries use n≥2','有限总体','Finite universe','n',[4,5],'contexts',[]),
 ('coalition','sym-coalition','S','上下文集合','Context set','S\\subseteq N','保留输入变量的mask集合，合法pair上下文排除i,j。','The mask set of retained variables; admissible pair contexts exclude i,j.','N的有限子集','Finite subset of N','当前上下文','Current context','S',[4,5],'contexts',[]),
 ('masked-input','sym-mask','x_S','掩码输入','Masked input','(x_S)_i=\\begin{cases}x_i&i\\in S\\\\r_i&i\\notin S\\end{cases}','原输入在S内保留，其余取r。','Keep the original input on S and use r elsewhere.','输入域X','Input domain X','固定x及r','Fixed x and r','x_S',[4,7],'game',[]),
 ('masked-game','sym-game','g_x','固定样本集合函数','Fixed-input set function','g_x(S)=v(x_S)','把原fixed-x的v(S|x)映为g_x；不与分布熵游戏混同。','Map the source fixed-x v(S|x) to g_x; keep it distinct from the population entropy game.','2^N→ℝ','2^N→ℝ','固定样本','Fixed sample','v(S|x)',[4,5],'game',[]),
 ('output-baseline','sym-output-baseline','b','输出基线','Output baseline','b=g_x(\\varnothing)=v(r)','全mask的真实scalar输出。','The actual scalar output under the empty mask.','实数','Real number','固定模型和输入基线','Fixed model and input baseline','v(∅)',[5],'game',[]),
 ('centered-game','sym-centered-game','g_{x,0}','中心化游戏','Centered game','g_{x,0}=g_x-b','项目辅助中心化，不把原v的空值默认0。','Project centering, without declaring the source v empty value zero.','2^N→ℝ','2^N→ℝ','同一固定样本','Same fixed sample','v(S)−v(∅)',[5],'game',[]),
 ('robustness-context-order','robustness-context-order','m','pair上下文阶','Pair context order','m=|S|','m计上下文变量，不是dividend阶数。','m counts context variables, not dividend order.','0,…,n−2；φ为0,…,n−1','0,…,n−2 for pairs; 0,…,n−1 for φ','固定size上下文','Fixed-size contexts','m',[4,8],'contexts',[]),
 ('robustness-pair-difference','robustness-pair-difference','\\Delta g','四项pair差','Four-term pair difference','\\Delta g(i,j,S)=g(Sij)-g(Si)-g(Sj)+g(S)','有限上下文二阶差分。','A second finite difference in a context.','实数；不同i,j且S排除两者','Real number; distinct i,j and S excludes them','当前pair上下文','Current pair context','Δv',[4],'pair',['Harsanyi.Robustness.pairDelta']),
 ('robustness-order-interaction','robustness-order-interaction','I_{ij}^{(m)}','多阶pair交互','Order-wise pair interaction','I_{ij}^{(m)}=E_{|S|=m}\\Delta g(i,j,S)','同一size上下文的均匀四项差平均。','The uniform average of the four-term difference at one context size.','实数；0≤m≤n−2','Real number; 0≤m≤n−2','固定样本与pair','Fixed sample and pair','I_{ij}^{(m)}',[4,5],'pair',['Harsanyi.Robustness.multiOrderInteraction']),
 ('robustness-order-attribution','robustness-order-attribution','\\phi^{(m)}','多阶归因','Order-wise attribution','\\phi^{(m)}(i)=E_{|S|=m}[g(Si)-g(S)]','当前m上下文中玩家i的平均边际。','The average marginal of player i in m-contexts.','实数；0≤m≤n−1','Real number; 0≤m≤n−1','固定样本与玩家','Fixed sample and player','φ^{(m)}',[8],'phi',['Harsanyi.Robustness.multiOrderAttribution']),
 ('shapley-value','sym-shapley','\\phi','经典Shapley值','Classical Shapley value','\\phi(i)=\\sum_{S\\subseteq N\\setminus\\{i\\}}\\frac{|S|!(n-|S|-1)!}{n!}(g(Si)-g(S))','原factorial边际分配。','The source factorial-weighted marginal allocation.','实数；i∈N','Real number; i∈N','固定游戏','Fixed game','φ(i)',[8],'phi',['Harsanyi.factorialShapley']),
 ('shapley-interaction','shapley-interaction','I(i,j)','经典Shapley pair index','Classical Shapley pair index','I(i,j)=\\widetilde\\phi_{j\\text{ present}}(i)-\\widetilde\\phi_{j\\text{ absent}}(i)','两个缩减游戏Shapley值之差。','The difference of Shapley values on two reduced games.','实数；i≠j','Real number; i≠j','同一缩减玩家总体','Same reduced player universe','I(i,j)',[4],'pair',['Harsanyi.Robustness.conditionalShapleyDifference']),
 ('robustness-entropy-game','robustness-entropy-game','H_Y','分布平均熵游戏','Population entropy game','H_Y(S)=H(Y\\mid X_S)','原B4的v(S)是条件熵平均，不是fixed-x g_x。','The source B.4 v(S) is a population conditional entropy, distinct from fixed-x g_x.','有限实值条件熵表','A finite real-valued conditional-entropy table','B4/Proposition1','B.4/Proposition 1','v(S)=H(Y|X_S)',[7],'entropy',[]),
 ('robustness-label','robustness-label','Y','预测标签随机变量','Predicted-label random variable','Y\\in\\{y^1,\\ldots,y^C\\}','原分类概率输出的标签空间。','The label space of the source classification probabilities.','有限标签集','Finite label set','共同概率律','Common probability law','Y',[7],'entropy',[]),
 ('robustness-context-random-variable','robustness-context-random-variable','X_S','上下文输入随机变量','Context-input random variable','X_S=\\{x_S:x\\in\\mathcal X\\}','熵游戏中分布变化的masked输入。','The distribution-varying masked input in the entropy game.','原X⊆ℝⁿ的mask像','The masked image of source X⊆ℝⁿ','B4共同分布','B.4 common distribution','X_S',[7],'entropy',[]),
 ('robustness-conditional-mi','robustness-conditional-mi','MI(X_i;Y\\mid X_S)','条件mutual information','Conditional mutual information','MI=H_Y(S)-H_Y(Si)','原两元条件MI的熵差。','The entropy difference for source bivariate conditional MI.','熵有限时实数','Real when the entropies are finite','B4共同条件信息','B.4 common conditional information','MI(X_i;Y|X_S)',[7],'entropy',['Harsanyi.Robustness.conditionalMI']),
 ('robustness-co-information','robustness-co-information','MI(X_i;X_j;Y\\mid X_S)','条件co-information','Conditional co-information','MI(X_i;Y\\mid X_S)-MI(X_i;Y\\mid X_S,X_j)','采用Eq7符号，可负；不是反号的enhancement。','Use the Equation (7) sign, which may be negative; it is not the opposite enhancement sign.','有限实条件熵差','A finite real conditional-entropy difference','B4/Proposition1','B.4/Proposition 1','MI(X_i;X_j;Y|X_S)',[7],'entropy',['Harsanyi.Robustness.conditionalCoI']),
 ('robustness-interaction-attack-change','robustness-interaction-attack-change','\\Delta I_{ij}^{(m)}','交互攻击差','Interaction attack difference','\\Delta I=I(x)-I(x_{adv})','原normal−adv方向。','The source normal-minus-adversarial direction.','实数','Real number','配对样本','Paired sample','ΔI',[5,6],'attack',[]),
 ('robustness-disentanglement','robustness-disentanglement','D^{(m)}','disentanglement比值平均','Average disentanglement ratio','D^{(m)}=E_xE_{i\\ne j}|E_S\\Delta g|/E_S|\\Delta g|','局部ratio再跨样本/pair平均，原0分母未定义。','Average the local ratio over samples and pairs; zero denominator is undefined in the source.','每个分母正时实数','Real only when every denominator is positive','样本总体','Sample population','D^{(m)}',[8],'ratio',[]),
 ('robustness-retention-size','robustness-retention-size','k','固定保留变量数','Fixed number of retained variables','k=\\lfloor(1-\\alpha)n\\rfloor','原固定size取整，不是期望保留数。','The rounded fixed size in the source, not an expected retention count.','0,…,n','0,…,n','dropout','Dropout','k',[9,10],'dropout',[]),
 ('robustness-dropout-rate','robustness-dropout-rate','\\alpha','丢弃率','Dropout rate','0\\le\\alpha\\le1','原固定保留size由α确定。','α determines the source fixed retention size.','[0,1]实数','Real in [0,1]','dropout','Dropout','α',[9,10],'dropout',[])]
 groups={}
 for sid,cid,tex,z,e,definition,zd,ed,zt,et,zscope,escope,alias,pg,group,names in symbolspec:
  key='supplement' if sid in ['shapley-value','shapley-interaction','robustness-retention-size','robustness-dropout-rate'] else 'formal'
  if sid=='shapley-value':pg=[1]
  if sid=='shapley-interaction':pg=[2]
  empty=('g(∅)=b；不设为0。' if group in ['game','contexts','pair','phi','attack','dropout','ratio'] else '空上下文熵H_Y(∅)=H(Y)，不设为0。')
  empty_en=('g(∅)=b, without assuming zero.' if group in ['game','contexts','pair','phi','attack','dropout','ratio'] else 'The empty-context entropy is H_Y(∅)=H(Y), without assuming zero.')
  baseline=('r是输入基线，b=v(r)是输出基线；二者不同类型。' if group!='entropy' else 'H_Y是分布平均游戏；不使用fixed-x输出基线替代H(Y)。')
  baseline_en=('r is the input baseline and b=v(r) the output baseline; they have different types.' if group!='entropy' else 'H_Y is a population game; do not replace H(Y) by a fixed-x output baseline.')
  note=('保留原作者符号，规范概念与scope见当前定义。' if alias==tex else '原作者符号按此scope映为规范概念；原原文公式不改符号。')
  note_en=('Retain the author notation; the canonical concept and scope are given in this definition.' if alias==tex else 'Map the author notation to the canonical concept in this scope; original-source formulas retain their notation.')
  conflict=('m是上下文size，不能合并到dividend阶数。' if sid=='robustness-context-order' else '熵游戏与fixed-x masked游戏不能同名合并。' if group=='entropy' else '本映射没有符号冲突。')
  conflict_en=('m is context size and is distinct from dividend order.' if sid=='robustness-context-order' else 'Keep the population entropy game separate from the fixed-x masked game.' if group=='entropy' else 'This mapping has no notation conflict.')
  premise=(['原对象须位于上列domain。'] if group!='entropy' else ['条件熵有限；标准Shannon语义使用共同联合概率律。'])
  premise_en=(['The object must lie in the domain stated above.'] if group!='entropy' else ['Conditional entropies are finite; standard Shannon semantics use a common joint probability law.'])
  mapping=dict(paper_id=p.pid,source_id='src-'+p.pid+'-'+key,version='NeurIPS 2021 formal',original_tex=alias,original_definition_tex=definition,pdf_pages=pg,equation_labels=[],canonical_concept_id=sid,relation_type='same_definition' if alias==tex else 'scope_preserving_mapping',note=note,conflict_note=conflict,original_definition_status='source_definition_with_project_concept_mapping',translations={'en':dict(note=note_en,conflict_note=conflict_en)})
  p.symbols.append(dict(id=sid,canonical_id=cid,canonical_tex=tex,name_zh=z,name=z,definition_tex=definition,description_md=zd,type_or_domain=zt,scope=zscope,assumptions=premise,empty_set_convention=empty,baseline_convention=baseline,aliases=[alias],paper_mappings=[mapping],lean_names=names,version='1.0',translations={'en':dict(name=e,name_zh=e,description_md=ed,type_or_domain=et,scope=escope,assumptions=premise_en,empty_set_convention=empty_en,baseline_convention=baseline_en,paper_mappings=[dict(note=note_en,conflict_note=conflict_en)])}))
  groups.setdefault(group,[]).append(sid)
 for id,r in rows.items():
  key=id.removeprefix('robustness-')
  g=['game','contexts']
  if key in ['entropy-interaction','exclusive-shared-benefits']:g=['entropy','contexts','pair']
  elif key.startswith('classical-') or key.startswith('shapley-') or key=='detector-attribution':g+=['phi']
  else:g+=['pair']
  if key in ['multiorder-definitions','marginal-attribution','accumulation','interaction-efficiency','attacking-decomposition','dropout-expansion']:g+=['phi']
  if key in ['attacking-decomposition','delta-average']:g+=['attack']
  if key=='dropout-expansion':g+=['dropout']
  if key=='disentanglement':g+=['ratio']
  r['symbol_ids']=list(dict.fromkeys(s for group in g for s in groups[group]))
  r['notation_map']=[];r['translations']['en']['notation_map']=[]
  for sid in r['symbol_ids']:
   sym=next(s for s in p.symbols if s['id']==sid);mp=sym['paper_mappings'][0]
   zmap=dict(symbol_id=sid,original_tex=mp['original_tex'],canonical_tex=sym['canonical_tex'],note=mp['note'],explanation_md=sym['description_md'])
   emap=dict(original_tex=mp['original_tex'],canonical_tex=sym['canonical_tex'],note=mp['translations']['en']['note'],explanation_md=sym['translations']['en']['description_md'])
   r['notation_map'].append(zmap);r['translations']['en']['notation_map'].append(emap)
 # Reusable mathematical bodies contain the complete reasoning, while each target retains its adapter.
 shared=[
 ('robustness-flagged-context-counting','带标记上下文双计数','Double counting flagged contexts',r'(m+1)\binom r{m+1}=(r-m)\binom rm=r\binom{r-1}m',
 ['有限R，r=|R|，0≤m<r，f:2^R→ℝ。'],['A finite R with r=|R|, 0≤m<r, and f:2^R→ℝ.'],
 [('令flags为(S,j)，S⊂R且|S|=m，j∈R\S。映到(T=S∪{j},j)是双射，逆映到(T\{j},j)。每个T大小m+1有m+1个flag；每个S有r−m个flag。','A flag is (S,j), where S⊂R, |S|=m and j∈R\S. The map to (T=S∪{j},j) is a bijection, inverted by (T\{j},j). Each size-(m+1) T has m+1 flags and each S has r−m flags.','sum_insert_flags'),
 ('先按j分组时S属于(R\{j})的m-subsets，所有组大小choose(r−1,m)。把f(T)及f(S)分别计数，得到raw差=(m+1)Σ_T f(T)−(r−m)Σ_S f(S)。','Grouping first by j gives the m-subsets of R\{j}, all with cardinality choose(r−1,m). Count f(T) and f(S) separately to obtain raw difference (m+1)Σ_T f(T)−(r−m)Σ_S f(S).','sum_erase_contexts'),
 ('把f恒取1得到三种总flag计数相等；正的非空card确保除法合法，除以该共同数得到相邻context平均差=平均j的平均边际差。没有把该归一化或递推作为假设。','Set f=1 to equate the three flag counts. Their nonempty cardinalities are positive, so divide by the common count to obtain the difference of adjacent context averages as the average of j-conditioned differences. Neither normalization nor recurrence is assumed.','flag_count_identity')]),
 ('robustness-context-relabeling','弱合作对称到上下文双射','From weak cooperation symmetry to a context bijection',r'g(Si)=g(Sj)\ \forall S\subseteq N\setminus\{i,j\}\Rightarrow\phi_i^{(m)}=\phi_j^{(m)},\ I_{ik}^{(m)}=I_{jk}^{(m)}',
 ['有限N，i,j∈N；pair结论还要求k∈N\{i,j}；仅采用原弱合作相等。'],['A finite N with i,j∈N; the pair conclusion also has k∈N\{i,j}. Use only the source weak cooperation equality.'],
 [('交换τ=(i j)。若S同时含两者或都不含，τS=S；若仅含i，把S写为Ri，R排除i,j，原假设给g(Ri)=g(Rj)；仅含j同理。因此∀S⊆N,g(τS)=g(S)。','Let τ=(i j). If S contains both players or neither, τS=S. If it contains only i, write S=Ri with R excluding i,j and use g(Ri)=g(Rj); the j-only case is symmetric. Thus g(τS)=g(S) for every S⊆N.','swap_game_of_cooperation'),
 ('τ保N、保card，并把排除i的m上下文双射到排除j的m上下文；pair时k固定，映排除i,k到排除j,k。四个mask集合同时映，逐项值相等，再以同card的有限平均重排求和。','τ preserves N and cardinality and bijects m-contexts excluding i with those excluding j. In the pair case k is fixed, and exclusions i,k map to j,k. Map all four mask sets simultaneously, match every value, and reindex the equal-cardinality finite average.','interaction_symmetry')]),
 ('robustness-four-entropy-identity','四个条件熵的co-information恒等式','Co-information identity of four conditional entropies',r'h_{ij}-h_i-h_j+h_0=(h_0-h_i)-(h_j-h_{ij})',
 ['四个条件熵有限，采用原Eq7的co-information约定；不要求X为有限类型。'],['The four conditional entropies are finite and use the source Equation (7) co-information sign; X need not be a finite type.'],
 [('设h0=H(Y|XS)，hi=H(Y|XS,Xi)，hj=H(Y|XS,Xj)，hij=H(Y|XS,Xi,Xj)。CMI_i=h0−hi、CMI_i_given_j=hj−hij，因此coI=CMI_i−CMI_i_given_j=hij−hi−hj+h0。','Write h0=H(Y|XS), hi=H(Y|XS,Xi), hj=H(Y|XS,Xj), and hij=H(Y|XS,Xi,Xj). Then CMI_i=h0−hi and CMI_i_given_j=hj−hij, so coI=CMI_i−CMI_i_given_j=hij−hi−hj+h0.','entropy_interaction'),
 ('exclusive_i=hj−hij，exclusive_j=hi−hij，两者加coI=h0−hij，即joint benefit。该恒等式及前一个逐上下文等式只用真实定义和实数代数，不需要相反熵游戏或待证等式假设。','The exclusive terms are hj−hij and hi−hij. Adding both and coI gives h0−hij, the joint benefit. This identity and the previous context identity use the actual definitions and real algebra, without an opposite-sign entropy game or the target equality as a premise.','entropy_shared_benefit')])]
 for sid,z,e,tex,za,ea,steps in shared:
  ps=[];pe=[]
  for k,(zb,eb,ln) in enumerate(steps,1):
   ps.append(dict(id=sid+'-step-'+str(k),title=zb.split('。')[0],body_md=zb,justification=zb,formula_tex='',lean_refs=['Harsanyi.Robustness.'+ln]))
   pe.append(dict(id=sid+'-step-'+str(k),title=eb.split('. ')[0],body_md=eb,justification=eb))
  p.shared.append(dict(id=sid,title=z,statement_tex=tex,assumptions=za,definitions=[],overview=ps[0]['body_md'],proof_steps=ps,symbol_ids=[s for s in groups['contexts']],rewrite_status='complete',translations={'en':dict(title=e,assumptions=ea,definitions=[],overview=pe[0]['body_md'],proof_steps=pe)}))
 # Original statements without local author proofs have explicit provenance; the source evidence remains separate.
 for key in ['detector-attribution']:
  rows['robustness-'+key]['original_proof_source_type']='complete_manual_formal_proof_transcription'
 original('detector-attribution',r'''Yang et al. [23] proposed an attribution-based method to detect adversarial examples, using the attribution score
$$\phi(x)_i:=f(x)_c-f(x^{(i)})_c,\quad c=\arg\max_{j\in C}f(x)_j.\tag{11}$$
$x^{(i)}$ masks the $i$-th variable by 0. $f(x)_c$ can be written as $v(N\mid x)$ and $f(x^{(i)})_c$ as $v(N\setminus\{i\}\mid x)$. We prove $v(N\mid x)-v(N\setminus\{i\}\mid x)=\phi^{(n-1)}(i\mid x)$.''',r'''Proof:
$$\begin{aligned}v(N\mid x)-v(N\setminus\{i\}\mid x)&=v((N\setminus\{i\})\cup\{i\}\mid x)-v(N\setminus\{i\}\mid x)\\&=v(S\cup\{i\}\mid x)-v(S\mid x),\quad S\overset{\rm def}=N\setminus\{i\},\ |S|=n-1\\&=E_{S\subseteq N\setminus\{i\},|S|=n-1}[v(S\cup\{i\}\mid x)-v(S\mid x)]\\&=\phi^{(n-1)}(i\mid x).\end{aligned}$$
According to the accumulation property,
$$\phi^{(n-1)}(i\mid x)=E_{j\in N\setminus\{i\}}\left[\sum_{m=0}^{n-2}I_{ij}^{(m)}\right]+\phi^{(0)}(i\mid x).$$
This indicates it contains the highest-order interaction components ($m=n-2$), absent from lower-order Shapley values. The source's subsequent sensitivity/detection interpretation is classified separately as empirical in the project.''')

 for issue in p.issues:issue['translations']['en'].pop('source_location',None)
 # Short editorial action titles, written independently of prose and TeX.
 action_titles={
 'multiorder-definitions':[('定义四项上下文差','Define the four-term context difference'),('保留真实输出基线','Retain the actual output baseline')],
 'interaction-linearity':[('展开合并游戏','Expand the merged game'),('分配有限平均','Distribute the finite average')],
 'interaction-nullity':[('两次使用dummy前提','Apply the dummy premise twice'),('平均零差并核对基线','Average zero differences and check the baseline')],
 'interaction-commutativity':[('交换两个玩家','Swap the two players'),('平均逐项相等的差','Average termwise equal differences')],
 'interaction-symmetry':[('构造上下文交换双射','Construct the context-swap bijection'),('核对两类上下文','Check both context cases'),('重排相同大小的平均','Reindex equal-size averages')],
 'shapley-linearity':[('拆开边际贡献','Split the marginal contribution')],
 'shapley-nullity':[('平均常数边际','Average constant marginals'),('核对特殊dummy基线','Check the source dummy baseline')],
 'shapley-symmetry':[('逐类交换上下文','Swap each context class'),('核对基数及端点','Check cardinalities and endpoints')],
 'shapley-orders':[('按上下文大小分组','Group by context size'),('识别等阶归因平均','Identify the order-wise average')],
 'shapley-efficiency':[('使用经典Shapley效率','Apply classical Shapley efficiency'),('代入多阶平均','Substitute the order decomposition')],
 'marginal-attribution':[('双计数扩张上下文','Count extended contexts twice'),('重排带标记上下文','Reindex flagged contexts'),('识别多阶交互平均','Identify the interaction average')],
 'accumulation':[('展开望远镜和','Expand the telescoping sum'),('代入每阶递推','Substitute each order recurrence')],
 'interaction-efficiency':[('代入归因累积式','Substitute attribution accumulation'),('计算每阶出现次数','Count occurrences of each order'),('保留基线并核对权重','Retain the baseline and check the weights')],
 'attacking-decomposition':[('相减两次效率分解','Subtract the two efficiency decompositions'),('核对相同输入基线','Check the shared input baseline')],
 'entropy-interaction':[('定义分布平均熵游戏','Define the population entropy game'),('核对co-information符号','Check the co-information sign'),('对合法上下文取平均','Average admissible contexts')],
 'exclusive-shared-benefits':[('消去中间条件熵','Cancel intermediate conditional entropies'),('处理零质量条件事件','Handle zero-mass conditioning events')],
 'delta-average':[('固定正常与攻击配对','Fix the normal/adversarial pairing'),('用有限平均差法则','Apply subtraction of finite averages')],
 'disentanglement':[('核对比值定义域','Check the ratio domain'),('解释同号与抵消','Explain common signs and cancellation')],
 'detector-attribution':[('固定类别及mask规则','Fix the category and mask rule'),('识别唯一最高阶上下文','Identify the unique top-order context')],
 'dropout-expansion':[('构造固定大小反例','Construct the fixed-size counterexample'),('比较原式与真实均值','Compare the source formula and actual mean'),('分开截断机制与错误系数','Separate truncation and the faulty coefficient')],
 'inference-heuristics':[('核对敏感性推断范围','Check the sensitivity inference'),('区分近似趋势及外引','Distinguish approximate trends and citations')],
 'classical-linearity':[('平均逐阶线性与缩放','Average order-wise linearity and scaling')],
 'classical-dummy':[('使用原dummy及基线条件','Use the source dummy and baseline premise')],
 'classical-symmetry':[('平均合作对称边际','Average cooperation-symmetric marginals')],
 'classical-efficiency':[('使用真实重构效率','Use exact reconstruction efficiency')],
 'classical-uniqueness':[('保留唯一性外引','Retain the external uniqueness claim')],
 'shapley-interaction-orders':[('定义两个缩减游戏','Define the two reduced games'),('相减等阶Shapley平均','Subtract the order-wise Shapley averages')]}
 for id,r in rows.items():
  key=id.removeprefix('robustness-');titles=action_titles[key];assert len(titles)==len(r['proof_steps']),key
  for st,en,(zt,et) in zip(r['proof_steps'],r['translations']['en']['proof_steps'],titles):
   st['title']=zt;en['title']=et;st['justification']='';en['justification']=''
  for d,en in zip(r['definitions'],r['translations']['en']['definitions']):
   if d['id'].endswith('-game'):
    d['body_md']+=r' 本条简写$g=g_x$。';en['body_md']+=r' In this entry, $g=g_x$.'
 # Target-local domains, with property-specific premises already appended above.
 pairprem=(r'有限$N$，$n=|N|\ge2$，不同$i,j\in N$，$0\le m\le n-2$。',r'A finite $N$, $n=|N|\ge2$, distinct $i,j\in N$, and $0\le m\le n-2$.')
 phiprem=(r'有限非空$N$，$n=|N|$，$i\in N$，$0\le m\le n-1$。',r'A finite nonempty $N$, $n=|N|$, $i\in N$, and $0\le m\le n-1$.')
 specialprem={
 'multiorder-definitions':(r'有限$N$；pair定义使用不同$i,j\in N$、$0\le m\le n-2$；归因定义使用$i\in N$、$0\le m\le n-1$。',r'A finite $N$; the pair definition has distinct $i,j\in N$ and $0\le m\le n-2$, while attribution has $i\in N$ and $0\le m\le n-1$.'),
 'interaction-symmetry':(r'有限$N$，$i,j,k\in N$，$i\ne j$，$k\notin\{i,j\}$，$0\le m\le n-2$。',r'A finite $N$, $i,j,k\in N$, $i\ne j$, $k\notin\{i,j\}$, and $0\le m\le n-2$.'),
 'shapley-symmetry':(r'有限非空$N$，$i,j\in N$，$0\le m\le n-1$。',r'A finite nonempty $N$, $i,j\in N$, and $0\le m\le n-1$.'),
 'shapley-orders':(r'有限非空$N$，$i\in N$，经典$\phi$按Eq1 factorial权重定义，所有阶$m=0,\ldots,n-1$。',r'A finite nonempty $N$, $i\in N$, classical $\phi$ defined by Equation (1)’s factorial weights, and all orders $m=0,\ldots,n-1$.'),
 'shapley-efficiency':(r'有限非空$N$，经典Shapley按Eq1定义；对所有$i\in N$及$m=0,\ldots,n-1$求和。',r'A finite nonempty $N$, classical Shapley as in Equation (1), and sums over all $i\in N$ and $m=0,\ldots,n-1$.'),
 'marginal-attribution':(r'有限$N$，$n\ge2$，$i\in N$，$0\le m\le n-2$；内平均的$j$取$N\setminus\{i\}$。',r'A finite $N$, $n\ge2$, $i\in N$, $0\le m\le n-2$, and the inner player $j\in N\setminus\{i\}$.'),
 'accumulation':(r'有限$N$，$n\ge2$，$i\in N$，$1\le m\le n-1$；项目声明还覆盖空累积的$m=0$。',r'A finite $N$, $n\ge2$, $i\in N$, and $1\le m\le n-1$; the project declaration also covers the empty accumulation at $m=0$.'),
 'interaction-efficiency':(r'有限$N$，$n\ge2$，任意实值游戏$g$；对全部不同$i,j\in N$及$m=0,\ldots,n-2$求和。',r'A finite $N$ with $n\ge2$ and any real-valued game $g$; sum over all distinct $i,j\in N$ and $m=0,\ldots,n-2$.'),
 'classical-uniqueness':(r'原外引的有限玩家博弈及线性、dummy、对称、效率四公理；本篇不提供本地唯一性证明。',r'The source external finite-player game and its linearity, dummy, symmetry and efficiency axioms; this paper supplies no local uniqueness proof.'),
 'shapley-interaction-orders':(r'有限$N$，$n\ge2$，不同$i,j\in N$；present/absent两游戏都在缩减总体$N\setminus\{j\}$上用Eq1定义Shapley。',r'A finite $N$ with $n\ge2$ and distinct $i,j\in N$; both present/absent games use Equation (1) Shapley on the reduced universe $N\setminus\{j\}$.'),
 'inference-heuristics':(r'原文具体实验中的mask、输出分数与攻击设置；Proposition1只给条件熵代数式，未给任意模型的扰动敏感性不等式。',r'The masks, output scores and attack settings of the source experiments; Proposition 1 provides conditional-entropy algebra, without a perturbation-sensitivity inequality for arbitrary models.')}
 for key,r in [(id.removeprefix('robustness-'),r) for id,r in rows.items()]:
  v=specialprem.get(key)
  if not v and key in ['interaction-linearity','interaction-nullity','interaction-commutativity']:v=pairprem
  if not v and key.startswith('shapley-'):v=phiprem
  if not v and key.startswith('classical-'):v=(r'有限非空$N$，$i\in N$，经典$\phi$按Eq1 factorial权重定义。',r'A finite nonempty $N$, $i\in N$, and classical $\phi$ defined by Equation (1)’s factorial weights.')
  if v:r['assumptions'][0]['body_md']=v[0];r['translations']['en']['assumptions'][0]['body_md']=v[1]
 # The entropy table uses H_Y throughout the actual rewritten proof.
 er=rows['robustness-entropy-interaction']
 er['proof_steps'][0]['body_md']=r'本条使用分布平均熵游戏$H_Y(S)=H(Y\mid X_S)$，它与固定样本游戏$g_x$分开。设$h_0=H_Y(S)$、$h_i=H_Y(S\cup\{i\})$、$h_j=H_Y(S\cup\{j\})$、$h_{ij}=H_Y(S\cup\{i,j\})$。保留作者正熵游戏，不取负号。'
 er['translations']['en']['proof_steps'][0]['body_md']=r'This entry uses the population entropy game $H_Y(S)=H(Y\mid X_S)$, separate from the fixed-input game $g_x$. Put $h_0=H_Y(S)$, $h_i=H_Y(S\cup\{i\})$, $h_j=H_Y(S\cup\{j\})$ and $h_{ij}=H_Y(S\cup\{i,j\})$. Retain the source positive entropy game.'
 er['proof_steps'][1]['body_md']=r'四项差为$h_{ij}-h_i-h_j+h_0=(h_0-h_i)-(h_j-h_{ij})$，即$MI(X_i;Y\mid X_S)-MI(X_i;Y\mid X_S,X_j)$。这正是原Eq7的co-information约定；作者证明的整体负号被修正。'
 er['translations']['en']['proof_steps'][1]['body_md']=r'The four-term difference is $h_{ij}-h_i-h_j+h_0=(h_0-h_i)-(h_j-h_{ij})$, namely $MI(X_i;Y\mid X_S)-MI(X_i;Y\mid X_S,X_j)$. This is the co-information convention in source Equation (7); the proof’s overall negative sign is repaired.'
 er['proof_steps'][1]['formula_tex']=r'\Delta H_Y(i,j,S)=MI(X_i;Y\mid X_S)-MI(X_i;Y\mid X_S,X_j)'
 er['overview']=er['proof_steps'][0]['body_md'];er['translations']['en']['overview']=er['translations']['en']['proof_steps'][0]['body_md']
 nr=rows['robustness-interaction-nullity'];nr['proof_scope']='原定义的不同双玩家范围；原显示量词扩到j=i的读法未被证明。';nr['translations']['en']['proof_scope']='The original distinct-player pair domain; the displayed extension to j=i is not proved.';nr['scope']=nr['proof_scope'];nr['translations']['en']['scope']=nr['translations']['en']['proof_scope'];nr['lean']['scope']=nr['translations']['en']['scope'];nr['statement_assessment']='scope_under_review'
 nr['proof_steps'][1]['body_md']+=r' 此结论只在$i\ne j$的原双玩家domain成立；不声称原显示量词按自配对读法也正确。'
 nr['translations']['en']['proof_steps'][1]['body_md']+=r' This conclusion uses the original pair domain $i\ne j$; it does not prove the displayed quantifier under a self-pair reading.'
 mr=rows['robustness-marginal-attribution']
 for st,en in zip(mr['proof_steps'],mr['translations']['en']['proof_steps']):
  st['body_md']=st['body_md'].replace('r=n−1','q=n−1').replace('$r\\binom{r-1}m$','$q\\binom{q-1}m$');en['body_md']=en['body_md'].replace('r=n−1','q=n−1').replace('r=n-1','q=n-1').replace('r binom(r−1,m)','q binom(q−1,m)').replace('r binom(r-1,m)','q binom(q-1,m)')
  st['formula_tex']=st['formula_tex'].replace('r','q')
 # Original D notation and every stated interpretation, separate from project domain analysis.
 original('disentanglement',r'''The motivation of disentanglement is to measure the discrimination power of interactions of a specific order. According to efficiency,
$$v(N\mid x)=v(\varnothing\mid x)+\sum_{i\in N}\phi^{(0)}(i\mid x)+\sum_{i,j\in N,i\ne j}\sum_{m=0}^{n-2}\frac{n-1-m}{n(n-1)}E_{S\subseteq N\setminus\{i,j\},|S|=m}[\Delta v(i,j,S)].\tag{9}$$
If interaction components of a certain order are all positive (or negative) and do not conflict, they jointly promote or suppress the output and show strong discrimination power. Otherwise positive and negative components’ effects will be eliminated, and the discrimination power is poor. The metric is
$$D^{(m)}=E_{x\in\Omega}E_{i,j\in N,i\ne j}\frac{|E_{S\subseteq N\setminus\{i,j\},|S|=m}\Delta v(i,j,S\mid x)|}{E_{S\subseteq N\setminus\{i,j\},|S|=m}|\Delta v(i,j,S\mid x)|}.\tag{10}$$
The numerator measures the strength of the average utility of all components; the denominator measures the strength of each component. If $D^{(m)}$ approximates to 1, almost all interaction components have similar effects (either positive or negative) on the model output. If it approximates to 0, most interaction components conflict with each other and are eliminated. Therefore, it measures the discrimination power of interactions. The main paper prints the same definition as Equation (4).''')
 # Distinguish editorial notes in source panes from author text.
 for r in rows.values():
  for field in ['original_statement_md','original_proof_md']:
   s=r[field]
   for sentence in ['Both $E_S$','In the middle lines','Every $E_j$','All unqualified','Every expectation','The source\'s third line','The source\'s subsequent','The equal-order-average equation is the project','The following source derivation']:
    s=s.replace(sentence,'**Project transcription note (not author text):** '+sentence)
   if r['original_proof_source_type']=='no_local_author_proof':s='**Project source note (not author text):** The selected formal source gives no separate local author proof for this entry.' if field=='original_proof_md' else s
   r[field]=s
  if r['original_proof_source_type']!='no_local_author_proof':(p.D/'original-proofs'/(r['id']+'.md')).write_text(r['original_proof_md']+'\n')
 # Render common prose notation as TeX; source transcriptions retain author symbols.
 import re
 for r in rows.values():
  for st,en in zip(r['proof_steps'],r['translations']['en']['proof_steps']):
   for node in [st,en]:
    text=node['body_md']
    for a,b in [('ΔIij',r'$\Delta I_{ij}^{(m)}$'),('Iij^(m)',r'$I_{ij}^{(m)}$'),('Iij',r'$I_{ij}^{(m)}$'),('φ0',r'$\phi^{(0)}(i)$'),('φ(m)',r'$\phi^{(m)}$'),('φ^(m)',r'$\phi^{(m)}$')]:text=text.replace(a,b)
    node['body_md']=text
 for sh in p.shared:
  for st,en in zip(sh['proof_steps'],sh['translations']['en']['proof_steps']):st['justification']='';en['justification']=''
  if sh['id']=='robustness-flagged-context-counting':
   sh['statement_tex']=sh['statement_tex'].replace('r','q');sh['assumptions']=[sh['assumptions'][0].replace('r=|R|','q=|R|').replace('m<r','m<q')];sh['translations']['en']['assumptions']=[sh['translations']['en']['assumptions'][0].replace('r=|R|','q=|R|').replace('m<r','m<q')]
   for st,en in zip(sh['proof_steps'],sh['translations']['en']['proof_steps']):
    st['body_md']=st['body_md'].replace('r−m','q−m').replace('r−1','q−1');en['body_md']=en['body_md'].replace('r−m','q−m').replace('r−1','q−1')
   sh['overview']=sh['proof_steps'][0]['body_md'];sh['translations']['en']['overview']=sh['translations']['en']['proof_steps'][0]['body_md']
  sh['definitions']=[dict(id=sh['id']+'-objects',body_md=objects['entropy' if sh['id']=='robustness-four-entropy-identity' else 'contexts'][0])]
  sh['translations']['en']['definitions']=[dict(id=sh['id']+'-objects',body_md=objects['entropy' if sh['id']=='robustness-four-entropy-identity' else 'contexts'][1])]
  if sh['id']=='robustness-four-entropy-identity':sh['symbol_ids']=groups['entropy']
 original('multiorder-definitions',r'''Input variables are players $N=\{1,\ldots,n\}$ and $v(S)$ denotes the DNN output with variables in $S$ retained and the others masked following [1]. The multi-order interaction is
$$I_{ij}^{(m)}=E_{S\subseteq N\setminus\{i,j\},|S|=m}[\Delta v(i,j,S)],\qquad\Delta v(i,j,S)\overset{\rm def}=v(S\cup\{i,j\})-v(S\cup\{i\})-v(S\cup\{j\})+v(S).$$
This is main Equation (2) and supplementary Equation (3). $I_{ij}^{(m)}$ measures average interactions under contexts consisting of $m$ variables; small $m$ represents simple contexts and large $m$ represents complex contexts. In supplementary B.2,
$$\phi(i)=\frac1n\sum_{m=0}^{n-1}\phi^{(m)}(i),\tag{4}$$
$$\phi^{(m)}(i)=E_{S\subseteq N\setminus\{i\},|S|=m}[v(S\cup i)-v(S)].\tag{5}$$
$\phi^{(m)}(i)$ measures the importance of variable $i$ with contexts containing $m\in\{0,\ldots,n-1\}$ variables. In particular, $\phi^{(0)}(i)=v(i)-v(\varnothing)$ is its importance without any context.

**Project source note (not author text):** The equations above retain the source $v$ and $E$ notation. Rewritten fixed-input formulas use $g_x(S)=v(x_S)$ and the alias $g=g_x$; the equivalent binomial inverse sums belong to that rewrite.''')
 original('inference-heuristics',r'''The following author claims are retained with their source locations and their original qualifications.

Main PDF5 cites Cheng et al. [11]: low-order interactions (local collaborations) mainly reflect simple and common concepts (features), and high-order interactions (global collaborations) usually represent complex and global features. This is an externally attributed claim.

Main PDF7, immediately after Proposition 1: compared to low-order interactions, high-order interactions are conditioned on more contextual variables. Thus, they are more likely to be changed by adversarial perturbations. This explains why adversarial perturbations mainly affect high-order interactions. The same page states that $\widehat v(S)=H(Y\mid X_S)$ is slightly different from $v(S)=\log p(y=y^{\rm truth}\mid x,S)$, and that the trend of $v(S)$ can roughly reflect the negative trend of $\widehat v(S)$.

Supplementary E, PDF8: $\widehat v(S)=H(Y\mid X_S)$ measures the uncertainty of prediction. If the model prediction is correct and confident, i.e. $v(S)=\log p(y=y^{\rm truth}\mid x,S)$ is large, then the uncertainty is very low. If the prediction is correct but $v(S)$ is small, the uncertainty is large. Therefore, its trend can roughly reflect the negative trend of $\widehat v(S)$ when the prediction is correct.

Supplementary G, PDF9: $\phi^{(n-1)}(i\mid x)$ contains the highest-order ($m=n-2$) interaction components, absent from Shapley values of lower orders. Section 4.1 has pointed out that high-order interactions are the most sensitive to adversarial perturbations, thereby enabling detection of adversarial examples.

Supplementary H, PDF10 after Equation (15): dropout removes all high-order interactions ($m>(1-\alpha)n-2$), while slightly affecting low-order interactions. It can therefore remove sensitive interaction components, reduce attacking utility and correct the output. The source floor error in Equations (14)–(15) is recorded separately.

Main PDF8–10 and supplementary I, PDF10–14 give the source-specific experiments on detection, rank/cutout, frequency comparisons, attacks, certified-robust models and recoverability. Their empirical outcomes are retained as experimental evidence, without a theorem asserting success for every model/input.

**Project source note (not author text):** The source claims above are scope-reviewed statements, not substituted universal perturbation bounds. No separate local proof is printed for these heuristic or experimental conclusions.''')
 rows['robustness-inference-heuristics']['statement_tex']=r'\text{High-order interactions are more likely to be changed by adversarial perturbations (source heuristic).}'
 # Preserve every repeated source occurrence without making a new copy of its proof target.
 for key,pg,section in [('interaction-efficiency',[8],'F Eq.(9)'),('accumulation',[9],'G highest-order accumulation'),('inference-heuristics',[9],'G sensitivity/detection interpretation')]:
  rows['robustness-'+key]['source_refs'].append(p.ref('supplement',pg,section))
 rows['robustness-inference-heuristics']['source_refs'].append(p.ref('formal',[5],'externally attributed Cheng[11] concept interpretation'))
 rows['robustness-accumulation']['original_statement_md']+=r'\n\nThe source repeats this at $m=n-1$ in supplementary G, PDF9: $$\phi^{(n-1)}(i\mid x)=E_{j\in N\setminus\{i\}}\left[\sum_{m=0}^{n-2}I_{ij}^{(m)}\right]+\phi^{(0)}(i\mid x).$$'
 rows['robustness-interaction-efficiency']['original_statement_md']+=r'\n\nSupplementary F, PDF8 repeats the same source identity as Equation (9), with the context average $E_S\Delta v$ in place of $I_{ij}^{(m)}$.'
 # Source proof remarks retain the author claim before its clearly marked scope note.
 dr=rows['robustness-detector-attribution'];dr['original_proof_md']=dr['original_proof_md'].replace('**Project transcription note (not author text):** The source\'s subsequent sensitivity/detection interpretation is classified separately as empirical in the project.','Section 4.1 of the paper has pointed that high-order interactions are the most sensitive to adversarial perturbations, thereby enabling the detection of adversarial examples.\n\n**Project transcription note (not author text):** The sensitivity/detection inference is scope-reviewed separately; the finite top-order attribution identity does not prove detection accuracy.')
 (p.D/'original-proofs'/(dr['id']+'.md')).write_text(dr['original_proof_md']+'\n')
 shared_titles={
 'robustness-flagged-context-counting':[('构造带标记双射','Construct the flagged bijection'),('分别计数两种边际','Count both marginal sums'),('核对共同归一化','Check the common normalization')],
 'robustness-context-relabeling':[('推出交换不变性','Derive swap invariance'),('重排有限平均','Reindex the finite averages')],
 'robustness-four-entropy-identity':[('展开co-information','Expand co-information'),('消去中间条件熵','Cancel the intermediate entropies')]}
 for sh in p.shared:
  for st,en,(z,e) in zip(sh['proof_steps'],sh['translations']['en']['proof_steps'],shared_titles[sh['id']]):st['title']=z;en['title']=e

 rows['robustness-disentanglement']['lean']['declarations'] += ['Harsanyi.Robustness.disentanglement_same_sign_nonneg','Harsanyi.Robustness.disentanglement_same_sign_nonpos']
 rows['robustness-disentanglement']['proof_steps'][1]['lean_refs'] += ['Harsanyi.Robustness.disentanglement_same_sign_nonneg','Harsanyi.Robustness.disentanglement_same_sign_nonpos']
 rows['robustness-shapley-interaction-orders']['lean']['declarations'].append('Harsanyi.Robustness.shapley_interaction_commutativity')
 rows['robustness-shapley-interaction-orders']['proof_steps'][1]['lean_refs'].append('Harsanyi.Robustness.shapley_interaction_commutativity')
 rows['robustness-shapley-interaction-orders']['proof_steps'][1]['body_md']+=' 再对每阶使用pair交换律，得到经典index的交换律。'
 rows['robustness-shapley-interaction-orders']['translations']['en']['proof_steps'][1]['body_md']+=' Apply pair commutativity at every order to obtain commutativity of the classical index.'
 rows['robustness-dropout-expansion']['lean']['declarations'].append('Harsanyi.Robustness.linear_masked_sum_cardinal')
 rows['robustness-dropout-expansion']['proof_steps'][0]['lean_refs'].append('Harsanyi.Robustness.linear_masked_sum_cardinal')
 rows['robustness-dropout-expansion']['proof_steps'][0]['body_md']+=' 该游戏由全1输入、全0输入mask基线的线性求和模型实现。'
 rows['robustness-dropout-expansion']['translations']['en']['proof_steps'][0]['body_md']+=' A linear sum model with an all-one input and all-zero input-mask baseline realizes this game.'
 for r in rows.values():
  for field in ['original_statement_md','original_proof_md']:r[field]=r[field].replace(r'\n\n','\n\n')
 rows['robustness-marginal-attribution']['translations']['en']['proof_steps'][1]['body_md']=rows['robustness-marginal-attribution']['translations']['en']['proof_steps'][1]['body_md'].replace(r'$r\binom{r-1}m$',r'$q\binom{q-1}m$')
 rows['robustness-interaction-efficiency']['translations']['en']['proof_steps'][0]['body_md']+=r' Explicitly, $g(N)-b=n^{-1}\sum_i\sum_{m=0}^{n-1}\phi^{(m)}(i)$.'
 rows['robustness-disentanglement']['translations']['en']['proof_steps'][0]['body_md']+=r' This uses $|\sum a_S|\le\sum|a_S|$.'
 rows['robustness-dropout-expansion']['translations']['en']['proof_steps'][0]['body_md']=rows['robustness-dropout-expansion']['translations']['en']['proof_steps'][0]['body_md'].replace('every zeroth attribution is one',r'every $\phi^{(0)}(i)$ is one')
 for key,zh,en in [
  ('multiorder-definitions','本条登记原pair差分、多阶平均与归因定义；定义本身不作为待证定理，步骤链接只指向定义和基线不变性辅助声明。','This entry records the source pair difference, order averages and attribution definitions. Definitions are not theorem targets; step links identify the definitions and the auxiliary baseline-invariance declaration.'),
  ('inference-heuristics','本条完整定位作者的外引、经验与启发性推断；有限计数和信息恒等式不提供其普遍敏感性、检测或鲁棒性保证，本条没有相应Lean定理。','This entry locates the author’s externally attributed, empirical and heuristic inferences. The finite identities do not provide universal sensitivity, detection or robustness guarantees, and no corresponding Lean theorem is claimed.'),
  ('classical-uniqueness','保留Supplement A对Weber唯一性定理的外引陈述；本文没有给出局部作者证明，本包未形式化Shapley四公理的唯一性。四性质分别有项目适配证明。','The externally cited Weber uniqueness statement in Supplement A is retained. The paper supplies no local author proof, and this package does not formalize uniqueness from the four Shapley axioms. The four properties have separate project adapters.')]:
  rr=rows['robustness-'+key];rr['lean']['scope']=zh;rr['lean'].setdefault('translations',{}).setdefault('en',{})['scope']=en

 for key in ['entropy-interaction','exclusive-shared-benefits']:
  rr=rows['robustness-'+key]
  for defs in [rr['definitions'],rr['translations']['en']['definitions']]:
   for de in defs:
    if de['id'].endswith('-pair'):
     de['body_md']=(r'本条的通用四项差取$g=H_Y$，并非$g_x$。定义$\Delta H_Y(i,j,S)=H_Y(Sij)-H_Y(Si)-H_Y(Sj)+H_Y(S)$与$I_{ij,H_Y}^{(m)}=E_{S\in\mathcal C(N\setminus\{i,j\},m)}\Delta H_Y$。Sij表示$S\cup\{i,j\}$；$i\ne j$，m是上下文大小。' if defs is rr['definitions'] else r'The generic four-term difference here is instantiated at $g=H_Y$, distinct from $g_x$. Define $\Delta H_Y(i,j,S)=H_Y(Sij)-H_Y(Si)-H_Y(Sj)+H_Y(S)$ and $I_{ij,H_Y}^{(m)}=E_{S\in\mathcal C(N\setminus\{i,j\},m)}\Delta H_Y$. Here Sij denotes $S\cup\{i,j\}$; $i\ne j$ and m counts context variables.')
  for j,mp in enumerate(rr['notation_map']):
   if mp['symbol_id'] in ['robustness-pair-difference','robustness-order-interaction']:
    mp['canonical_tex']=r'\Delta H_Y' if mp['symbol_id']=='robustness-pair-difference' else r'I_{ij,H_Y}^{(m)}'
    mp['explanation_md']='B4的原差分在本条实例化于分布平均熵游戏H_Y，不是fixed-x g_x。'
    en=rr['translations']['en']['notation_map'][j];en['canonical_tex']=mp['canonical_tex'];en['explanation_md']='The B.4 source difference is instantiated at the population entropy game H_Y here, rather than fixed-input g_x.'
 for sy in p.symbols:
  if sy['id']=='robustness-entropy-game':
   sy['type_or_domain']='有限玩家幂集上的实值条件熵表；输入分布空间可连续。';sy['translations']['en']['type_or_domain']='A real conditional-entropy table on a finite player powerset; the input distribution space may be continuous.'
 drop=rows['robustness-dropout-expansion']
 drop['proof_steps'][0]['lean_refs']=['Harsanyi.Robustness.linear_masked_sum_cardinal','Harsanyi.Robustness.cardinal_game_interaction']
 drop['proof_steps'][1]['lean_refs']=['Harsanyi.Robustness.fixed_size_cardinal_mean','Harsanyi.Robustness.fixed_size_floor_counterexample']
 drop['proof_steps'][2]['lean_refs']=[]
 for rr in rows.values():
  for st,en in zip(rr['proof_steps'],rr['translations']['en']['proof_steps']):
   st['body_md']=st['body_md'].replace(r'$\phi^{(0)}(i)$(i)',r'$\phi^{(0)}(i)$')
   en['body_md']=en['body_md'].replace(r'$\phi^{(0)}(i)$(i)',r'$\phi^{(0)}(i)$')
 issue_refs={
  'robustness-entropy-proof-sign':[('formal',[7],'Proposition 1'),('supplement',[6],'B.4 Equation (6) proof')],
  'robustness-symmetry-context-typo':[('supplement',[3],'B.1 interaction symmetry proof')],
  'robustness-dropout-floor':[('formal',[9,10],'dropout/cutout discussion'),('supplement',[9,10],'H fixed-size definition and Equations (14)–(15)')],
  'robustness-disentanglement-zero':[('formal',[8],'Equation (4)'),('supplement',[8],'F Equation (10)')],
  'robustness-self-pair-quantifier':[('supplement',[3],'B.1 Nullity displayed quantifier')],
  'robustness-benefit-cancellation-typo':[('supplement',[7],'B.4 Equation (7) cancellation chain')]}
 for iss in p.issues:
  iss['source_refs']=[p.ref(*t) for t in issue_refs[iss['id']]]
  iss['issue_type']='proof_step_error' if iss['kind']=='proof_error' else 'statement_partial_counterexample' if iss['id']=='robustness-dropout-floor' else 'statement_alignment_or_scope'
  iss['original_statement_status']='compound_clause_counterexample_verified' if iss['id']=='robustness-dropout-floor' else 'source_scope_under_review' if iss['kind'] in ['domain_issue','domain_ambiguity'] else 'original_statement_preserved'
 # Author source text and explicitly labelled project annotations are separate.
 for rr in rows.values():
  for field in ['original_statement_md','original_proof_md']:
   pattern=r'\*\*Project (?:source|transcription) note \(not author text\):\*\*[^\n]*(?:\n|$)'
   notes=re.findall(pattern,rr[field])
   if notes:
    rr.setdefault('source_transcription_notes',[]).extend(dict(note=n.strip(),attribution='project_source_note_not_author_text',original_field=field) for n in notes)
    rr[field]=re.sub(pattern,'',rr[field]).strip()
  if rr['original_proof_source_type']=='no_local_author_proof':rr['original_proof_md']=''
  (p.D/'original-proofs'/(rr['id']+'.md')).write_text(rr['original_proof_md']+'\n' if rr['original_proof_md'] else '')
 source_only=__import__('json').loads((p.D/'source-transcripts-inference-extra.json').read_text())
 hr=rows['robustness-inference-heuristics']
 hr['source_transcription_notes']=[n for n in hr['source_transcription_notes'] if 'No separate local proof is printed' not in n['note'] and 'gives no separate local author proof for this entry' not in n['note']]
 hr['source_transcription_notes'].append(dict(note=hr['original_statement_md'],attribution='superseded_project_source_synopsis_not_author_text'))
 hr['original_statement_md']='\n\n'.join(t['original_statement_md'] for t in source_only['transcripts'])
 # The heuristic author arguments are kept, without presenting the cited claim as a local theorem proof.
 hr['original_proof_md']='\n\n'.join(t['original_proof_md'] for t in source_only['transcripts'])
 hr['original_proof_source_type']='complete_manual_formal_proof_transcription'
 hr['original_proof_refs']=[p.ref('formal',[5,7],'Source concept/sensitivity arguments'),p.ref('supplement',[8,9,10],'E/G/H source heuristic arguments')]
 hr['source_transcription_notes'].extend(dict(note=n,attribution='project_source_note_not_author_text') for t in source_only['transcripts'] for n in t['transcription_notes'])
 (p.D/'original-proofs'/(hr['id']+'.md')).write_text(hr['original_proof_md']+'\n')
