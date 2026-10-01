Proof:
$$\begin{aligned}v(N\mid x)-v(N\setminus\{i\}\mid x)&=v((N\setminus\{i\})\cup\{i\}\mid x)-v(N\setminus\{i\}\mid x)\\&=v(S\cup\{i\}\mid x)-v(S\mid x),\quad S\overset{\rm def}=N\setminus\{i\},\ |S|=n-1\\&=E_{S\subseteq N\setminus\{i\},|S|=n-1}[v(S\cup\{i\}\mid x)-v(S\mid x)]\\&=\phi^{(n-1)}(i\mid x).\end{aligned}$$
According to the accumulation property,
$$\phi^{(n-1)}(i\mid x)=E_{j\in N\setminus\{i\}}\left[\sum_{m=0}^{n-2}I_{ij}^{(m)}\right]+\phi^{(0)}(i\mid x).$$
This indicates it contains the highest-order interaction components ($m=n-2$), absent from lower-order Shapley values. Section 4.1 of the paper has pointed that high-order interactions are the most sensitive to adversarial perturbations, thereby enabling the detection of adversarial examples.
