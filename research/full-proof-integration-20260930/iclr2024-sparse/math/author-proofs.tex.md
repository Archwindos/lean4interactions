# 正式原作者证明的数学转录

来源仅为 ICLR 2024 正式 PDF，SHA256 `9f380ff7d659d8b414e2cdb70edf9dcc8d0e4108240a1f506c2337664e7c8f45`。以下逐式转录全部 11 个局部证明范围，保留原记号 \(u,b\)、原编号和原错式。英文理由按正式证明原意完整保留；PDF 图像与原始文本是辅助对照证据，项目修复证明另在 `rewrites.zh.md`。这里的 \(b\) 是作者输入基线向量。

<!-- proof:reconstruction -->
## B.1 — Proof of Theorem 1（PDF 15）

According to the definition of the Harsanyi interaction, we have \(\forall S\subseteq N\),
\[
\begin{aligned}
\sum_{T\subseteq S}I(T)
&=\sum_{T\subseteq S}\sum_{L\subseteq T}(-1)^{|T|-|L|}u(L)\\
&=\sum_{L\subseteq S}\sum_{T\subseteq S:T\supseteq L}(-1)^{|T|-|L|}u(L)\\
&=\sum_{L\subseteq S}\sum_{t=|L|}^{|S|}\sum_{\substack{T\subseteq S:S\supseteq L\\|T|=t}}(-1)^{t-|L|}u(L)\\
&=\sum_{L\subseteq S}u(L)\sum_{m=0}^{|S|-|L|}\binom{|S|-|L|}{m}(-1)^m\\
&=u(S)=v(x_S)-v(x_\varnothing).
\end{aligned}
\]
Therefore, we have \(v(x_S)=\sum_{T\subseteq S}I(T)+v(x_\varnothing)\).

转录注：原第三行内层限制实际印为 \(T\subseteq S:S\supseteq L\)，保留原式；与上一行 \(T\supseteq L\) 的正确分组条件不同。这一求和索引排印问题不改变 Theorem 1 陈述；项目证明按正确索引明确给双射。

<!-- proof:lemma1 -->
## B.2 — Proof of Lemma 1（PDF 15–16）

Let us denote the function on the right of Eq. (8) by \(\widetilde I(S)\), i.e., for \(S\ne\varnothing\),
\[
\widetilde I(S)\stackrel{\rm def}{=}\sum_{\kappa\in Q_S}
\left.\frac{\partial^{\kappa_1+\cdots+\kappa_n}v}{\partial x_1^{\kappa_1}\cdots\partial x_n^{\kappa_n}}\right|_{x=b}
\frac{\prod_{i\in S}(x_i-b_i)^{\kappa_i}}{\kappa_1!\cdots\kappa_n!}.\tag{9}
\]
According to Eq. (1), we define \(\widetilde I(\varnothing)=0\). The Harsanyi interaction defined in Eq. (1) is the unique metric satisfying the universal matching property (Grabisch & Roubens, 1999; Ren et al., 2023a):
\[
\forall S\subseteq N,\qquad v(x_S)=\sum_{T\subseteq S}I(T)+v(x_\varnothing).\tag{10}
\]
Thus, as long as we prove that \(\widetilde I(S)\) also satisfies the above universal matching property, we obtain \(\widetilde I(S)=I(S)\). Given \(x\in\mathbb R^n\), consider the Taylor expansion of the network output on an arbitrarily masked sample at \(x_\varnothing=b=[b_1,\ldots,b_n]^\top\):
\[
\forall S\subseteq N,\quad v(x_S)=\sum_{\kappa_1=0}^{\infty}\cdots\sum_{\kappa_n=0}^{\infty}
\left.\frac{\partial^{\kappa_1+\cdots+\kappa_n}v}{\partial x_1^{\kappa_1}\cdots\partial x_n^{\kappa_n}}\right|_{x=b}
\frac{((x_S)_1-b_1)^{\kappa_1}\cdots((x_S)_n-b_n)^{\kappa_n}}{\kappa_1!\cdots\kappa_n!}.\tag{11}
\]
Here \(b_i\) is the baseline masking value. All variables in \(S\) remain unchanged, others equal the baseline: \((x_S)_i=x_i\) for \(i\in S\), \((x_S)_i=b_i\) for \(i\notin S\). The original proof then states
\[
\forall i\notin S,\qquad[(x_S)_i-b_i]^{\kappa_i}=0.
\]
Only terms with degrees in \(P_S=\{[\kappa_1,\ldots,\kappa_n]^\top:\kappa_i\in\mathbb N\ (i\in S),\ \kappa_i=0\ (i\notin S)\}\) may be nonzero, and Eq. (11) is rewritten as
\[
\forall S\subseteq N,\quad v(x_S)=\sum_{\kappa\in P_S}
\left.\frac{\partial^{\kappa_1+\cdots+\kappa_n}v}{\partial x_1^{\kappa_1}\cdots\partial x_n^{\kappa_n}}\right|_{x=b}
\frac{\prod_{i\in S}(x_i-b_i)^{\kappa_i}}{\kappa_1!\cdots\kappa_n!}.\tag{12}
\]
The set \(P_S\) can be divided into disjoint sets \(P_S=\bigcup_{T\subseteq S}Q_T\), where \(Q_T=\{\kappa:\kappa_i\in\mathbb N^+\ (i\in T),\ \kappa_i=0\ (i\notin T)\}\). Consequently,
\[
\begin{aligned}
\forall S\subseteq N,\quad v(x_S)
&=\sum_{T\subseteq S}\sum_{\kappa\in Q_T}
\left.\frac{\partial^{\kappa_1+\cdots+\kappa_n}v}{\partial x_1^{\kappa_1}\cdots\partial x_n^{\kappa_n}}\right|_{x=b}
\frac{\prod_{i\in T}(x_i-b_i)^{\kappa_i}}{\kappa_1!\cdots\kappa_n!}\\
&=\sum_{T\subseteq S}\widetilde I(T)+v(x_\varnothing).\quad\text{(13)}
\end{aligned}
\]
When \(T=\varnothing\), \(Q_T\) has only \(\kappa=[0,\ldots,0]^\top\), corresponding to \(v(x_\varnothing)\); also \(\widetilde I(\varnothing)=0\). This yields the last line. Thus \(\widetilde I\) satisfies Eq. (10), and the lemma holds.

原式问题：掩码幂句在 \(\kappa_i=0\) 时不成立；一般无限 Taylor 等式的收敛/函数相等前提也未在该独立 Lemma 中注明。两项来源问题分别记录，不能静默更改作者式。

<!-- proof:derivative-cutoff -->
## B.2 — Derivation of Assumption 1-α from 1-β（PDF 16）

According to Lemma 1,
\[
I(S)=\sum_{\kappa\in Q_S}
\left.\frac{\partial^{\kappa_1+\cdots+\kappa_n}v}{\partial x_1^{\kappa_1}\cdots\partial x_n^{\kappa_n}}\right|_{x=b}
\frac{\prod_{i\in S}(x_i-b_i)^{\kappa_i}}{\kappa_1!\cdots\kappa_n!}.\tag{14}
\]
The set \(Q_S\) is \(\{[\kappa_1,\ldots,\kappa_n]^\top:\kappa_i\in\mathbb N^+\ (i\in S),\ \kappa_i=0\ (i\notin S)\}\). When \(|S|\ge M+1\), every \(\kappa\in Q_S\) has \(\kappa_1+\cdots+\kappa_n\ge M+1\). Combining with Assumption 1-β gives
\[
\left.\frac{\partial^{\kappa_1+\cdots+\kappa_n}v}{\partial x_1^{\kappa_1}\cdots\partial x_n^{\kappa_n}}\right|_{x=b}=0,
\qquad\forall\kappa\in Q_S.\tag{15}
\]
This leads to \(I(S)=0\), \(\forall S\subseteq N\) with \(|S|\ge M+1\).

<!-- proof:lemma2 -->
## B.3 — Proof of Lemma 2（PDF 17）

According to the definition of \(\bar u^{(m)}\),
\[
\begin{aligned}
\bar u^{(m)}
&=\mathbb E_{S\subseteq N,|S|=m}[u(S)]\quad\text{(17)}\\
&=\mathbb E_{S\subseteq N,|S|=m}[v(x_S)-v(x_\varnothing)]\quad\text{(18)}\\
&=\mathbb E_{S\subseteq N,|S|=m}\left[\sum_{T\subseteq S}I(T)\right] &&\text{by Theorem 1}\quad\text{(19)}\\
&=\mathbb E_{S\subseteq N,|S|=m}\left[\sum_{k=1}^m\sum_{T\subseteq S,|T|=k}I(T)\right]\quad\text{(20)}\\
&=\sum_{k=1}^m\mathbb E_{S\subseteq N,|S|=m}\left[\sum_{T\subseteq S,|T|=k}I(T)\right]\quad\text{(21)}\\
&=\sum_{k=1}^m\frac1{\binom nm}\sum_{S\subseteq N,|S|=m}\sum_{T\subseteq S,|T|=k}I(T)\quad\text{(22)}\\
&=\sum_{k=1}^m\frac1{\binom nm}\binom{n-k}{m-k}\sum_{T\subseteq N,|T|=k}I(T)\quad\text{(23)}\\
&=\sum_{k=1}^m\frac{\binom mk}{\binom nk}\sum_{T\subseteq N,|T|=k}I(T)\quad\text{(24)}\\
&=\sum_{k=1}^m\frac{\binom mk}{\binom nk}A^{(k)}.\quad\text{(25)}
\end{aligned}
\]
From Eq. (22) to (23), each \(T\subseteq N\), \(|T|=k\), is counted \(\binom{n-k}{m-k}\) times. From (23) to (24), the proof uses
\[
\binom nm\binom mk
=\frac{n!}{m!(n-m)!}\frac{m!}{k!(m-k)!}
=\frac{n!}{k!(n-k)!}\frac{(n-k)!}{(m-k)!(n-m)!}
=\binom nk\binom{n-k}{m-k}.\tag{26}
\]
Assumption 1-α gives \(I(S)=0\) for \(|S|\ge M+1\), hence \(A^{(k)}=0\) for \(k\ge M+1\). Therefore,
\[
\forall M\le m\le n,\qquad\bar u^{(m)}
=\sum_{k=1}^m\frac{\binom mk}{\binom nk}A^{(k)}
=\sum_{k=1}^M\frac{\binom mk}{\binom nk}A^{(k)}.\tag{27}
\]

<!-- proof:lemma3 -->
## B.3 — Proof of Lemma 3（PDF 17–18）

The problem is represented by \(Cw=0\), where
\[
C=\begin{bmatrix}
\binom n1/\binom n1&\binom n2/\binom n2&\cdots&\binom nM/\binom nM\\
\binom{n-1}1/\binom n1&\binom{n-1}2/\binom n2&\cdots&\binom{n-1}M/\binom nM\\
\vdots&\vdots&\ddots&\vdots\\
\binom{n-M}1/\binom n1&\binom{n-M}2/\binom n2&\cdots&\binom{n-M}M/\binom nM
\end{bmatrix}\in\mathbb R^{(M+1)\times M},\quad
w=[w_1,w_2,\ldots,w_M]^\top\in\mathbb R^M.\tag{28}
\]
It suffices to prove \(\operatorname{rank}(C)=M\). Subtract the \((i+1)\)-th row from the \(i\)-th row for \(i=1,\ldots,M\), using \(\binom nm-\binom{n-1}m=\binom{n-1}{m-1}\). The rank is unchanged and the resulting matrix is
\[
C'=\begin{bmatrix}
\binom{n-1}0/\binom n1&\binom{n-1}1/\binom n2&\cdots&\binom{n-1}{M-1}/\binom nM\\
\binom{n-2}0/\binom n1&\binom{n-2}1/\binom n2&\cdots&\binom{n-2}{M-1}/\binom nM\\
\vdots&\vdots&\ddots&\vdots\\
\binom{n-M}0/\binom n1&\binom{n-M}1/\binom n2&\cdots&\binom{n-M}{M-1}/\binom nM\\
\binom{n-M}1/\binom n1&\binom{n-M}2/\binom n2&\cdots&\binom{n-M}M/\binom nM
\end{bmatrix}.\tag{29}
\]
The proof shows that the first \(M\) rows are independent by a nonzero determinant:
\[
D\stackrel{\rm def}{=}\det\begin{bmatrix}
\binom{n-1}0/\binom n1&\binom{n-1}1/\binom n2&\cdots&\binom{n-1}{M-1}/\binom nM\\
\binom{n-2}0/\binom n1&\binom{n-2}1/\binom n2&\cdots&\binom{n-2}{M-1}/\binom nM\\
\vdots&\vdots&\ddots&\vdots\\
\binom{n-M}0/\binom n1&\binom{n-M}1/\binom n2&\cdots&\binom{n-M}{M-1}/\binom nM
\end{bmatrix}\ne0.\tag{30}
\]
The original recursive determinant calculation is
\[
\begin{aligned}
D\prod_{k=1}^M\binom nk
&=\det\begin{bmatrix}
\binom{n-1}0&\binom{n-1}1&\cdots&\binom{n-1}{M-1}\\
\binom{n-2}0&\binom{n-2}1&\cdots&\binom{n-2}{M-1}\\
\vdots&\vdots&\ddots&\vdots\\
\binom{n-M}0&\binom{n-M}1&\cdots&\binom{n-M}{M-1}
\end{bmatrix}\quad\text{(31)}\\
&=\det\begin{bmatrix}
0&\binom{n-2}0&\cdots&\binom{n-2}{M-2}\\
0&\binom{n-3}0&\cdots&\binom{n-3}{M-2}\\
\vdots&\vdots&\ddots&\vdots\\
\binom{n-M}0&\binom{n-M}1&\cdots&\binom{n-M}{M-1}
\end{bmatrix}&&\text{subtracting row }i+1\text{ from row }i\quad\text{(32)}\\
&=\det\begin{bmatrix}
\binom{n-2}0&\binom{n-2}1&\cdots&\binom{n-2}{M-2}\\
\binom{n-3}0&\binom{n-2}1&\cdots&\binom{n-2}{M-2}\\
\vdots&\vdots&\ddots&\vdots\\
\binom{n-M}0&\binom{n-M}1&\cdots&\binom{n-M}{M-2}
\end{bmatrix}\quad\text{(33)}\\
&=\cdots\quad\text{(34)}\\
&=1.\quad\text{(35)}
\end{aligned}
\]
Now, the original proof states
\[
D=\frac1{\prod_{k=1}^M\binom nk}\ne0.\tag{36}
\]
This leads to: if \(\sum_{k=1}^M\frac{\binom mk}{\binom nk}w_k=0\) for all \(m\in\{n,n-1,\ldots,n-M\}\), then \(w_k=0\) for \(1\le k\le M\).

原式保留注：Eq. (33) 漏余子式符号，Eq. (35)–(36) 的行列式值因此少了交错符号；Eq. (33) 第二行后几项也照正式页保留 \(n-2\)。项目正确零空间证明不改原命题，详见修复层。

<!-- proof:theorem2 -->
## B.3 — Proof of Theorem 2（PDF 19–20）

By Assumption 3 with \(m'=1\), \(\bar u^{(m)}\le m^p\bar u^{(1)}\). Assumption 2 gives \(\bar u^{(m)}\ge\bar u^{(0)}=v(x_\varnothing)-v(x_\varnothing)=0\). With Lemma 2,
\[
\forall M\le m\le n,\quad0\le\bar u^{(m)}=\sum_{k=1}^M\frac{\binom mk}{\binom nk}A^{(k)}\le m^p\bar u^{(1)}.\tag{40}
\]
For each \(1\le k\le M\), consider the \(n\)-ary representation after division by \(\bar u^{(1)}\):
\[
\frac{A^{(k)}}{\bar u^{(1)}}=a_{q^{(k)}}^{(k)}n^{q^{(k)}}+a_{q^{(k)}-1}^{(k)}n^{q^{(k)}-1}+\cdots+a_1^{(k)}n+a_0^{(k)},\tag{41}
\]
\[
A^{(k)}=\left(a_{q^{(k)}}^{(k)}n^{q^{(k)}}+a_{q^{(k)}-1}^{(k)}n^{q^{(k)}-1}+\cdots+a_1^{(k)}n+a_0^{(k)}\right)\bar u^{(1)}.\tag{42}
\]
Here \(q^{(k)}\in\mathbb N\), \(|a_i^{(k)}|\in\{0,1,\ldots,n-1\}\) for \(1\le i\le q^{(k)}\), and \(|a_0^{(k)}|<n\); the decimal part is absorbed into \(a_0^{(k)}\).

Case 1: \(q^{(k)}\le\lfloor p\rfloor-1\). Then
\[
A^{(k)}=\left(\lambda^{(k)}n^{p+\delta}+a_{\lfloor p\rfloor-1}^{(k)}n^{\lfloor p\rfloor-1}+\cdots+a_{q^{(k)}+1}^{(k)}n^{q^{(k)}+1}+a_{q^{(k)}}^{(k)}n^{q^{(k)}}+\cdots+a_1^{(k)}n+a_0^{(k)}\right)\bar u^{(1)},\tag{43}
\]
with \(\lambda^{(k)}=a_{\lfloor p\rfloor-1}^{(k)}=\cdots=a_{q^{(k)}+1}^{(k)}=0\) and arbitrary \(\delta\) (its choice and range discussed in Case 2).

Case 2: \(q^{(k)}\ge\lfloor p\rfloor\). Merge all degree terms at least \(\lfloor p\rfloor\):
\[
\begin{aligned}
A^{(k)}
&=\left(\underbrace{a_{q^{(k)}}^{(k)}n^{q^{(k)}}+\cdots+a_{\lfloor p\rfloor}^{(k)}n^{\lfloor p\rfloor}}_{=:s^{(k)}n^{p+\delta^{(k)}}}+a_{\lfloor p\rfloor-1}^{(k)}n^{\lfloor p\rfloor-1}+\cdots+a_1^{(k)}n+a_0^{(k)}\right)\bar u^{(1)}\quad\text{(44)}\\
&=\left(s^{(k)}n^{p+\delta^{(k)}}+a_{\lfloor p\rfloor-1}^{(k)}n^{\lfloor p\rfloor-1}+\cdots+a_1^{(k)}n+a_0^{(k)}\right)\bar u^{(1)}.\quad\text{(45)}
\end{aligned}
\]
The sign \(s^{(k)}\in\{-1,1\}\). Let \(G=\{k:1\le k\le M,q^{(k)}\ge\lfloor p\rfloor\}\), \(\delta=\max_{k\in G}\delta^{(k)}\), and \(k^*=\arg\max_{k\in G}\delta^{(k)}\). For \(k\in G\),
\[
s^{(k)}n^{p+\delta^{(k)}}=\underbrace{s^{(k)}n^{\delta^{(k)}-\delta}}_{=:\lambda^{(k)}}n^{p+\delta}=\lambda^{(k)}n^{p+\delta},\tag{46}
\]
\[
|\lambda^{(k)}|=|s^{(k)}n^{\delta^{(k)}-\delta}|=|n^{\delta^{(k)}-\delta}|\le1.\tag{47}
\]
In particular, \(|\lambda^{(k^*)}|=1\). Thus for any \(k\in G\),
\[
A^{(k)}=\left(\lambda^{(k)}n^{p+\delta}+a_{\lfloor p\rfloor-1}^{(k)}n^{\lfloor p\rfloor-1}+\cdots+a_1^{(k)}n+a_0^{(k)}\right)\bar u^{(1)},\tag{48}
\]
with the stated digit bounds. Plugging this into Eq. (40) gives
\[
\bar u^{(m)}=\left[
\left(\sum_{k=1}^M\frac{\binom mk}{\binom nk}\lambda^{(k)}\right)n^{p+\delta}
+\left(\sum_{k=1}^M\frac{\binom mk}{\binom nk}a_{\lfloor p\rfloor-1}^{(k)}\right)n^{\lfloor p\rfloor-1}
+\cdots+\left(\sum_{k=1}^M\frac{\binom mk}{\binom nk}a_0^{(k)}\right)\right]\bar u^{(1)}.\tag{49}
\]
Lemma 3 implies
\[
\exists m_0\in\{n,n-1,\ldots,n-M\},\quad\sum_{k=1}^M\frac{\binom{m_0}k}{\binom nk}\lambda^{(k)}\ne0.\tag{50}
\]
Indeed, if this sum were zero for every row, Lemma 3 would give every \(\lambda^{(k)}=0\), contradicting \(|\lambda^{(k^*)}|=1\). Let \(\lambda=\sum_k\frac{\binom{m_0}k}{\binom nk}\lambda^{(k)}\ne0\), \(a_i=\sum_k\frac{\binom{m_0}k}{\binom nk}a_i^{(k)}\). Then
\[
0\le\bar u^{(m_0)}=\left(\lambda n^{p+\delta}+a_{\lfloor p\rfloor-1}n^{\lfloor p\rfloor-1}+\cdots+a_1n+a_0\right)\bar u^{(1)}\le m_0^p\bar u^{(1)}\le n^p\bar u^{(1)}.\tag{51}
\]
When \(\lambda>0\), the right inequality gives
\[
\delta\le\log_n\left[\frac1\lambda\left(1-\frac{a_{\lfloor p\rfloor-1}}{n^{p-\lfloor p\rfloor+1}}-\cdots-\frac{a_0}{n^p}\right)\right].\tag{52}
\]
When \(\lambda<0\), the left inequality gives
\[
\delta\le\log_n\left[\frac1{-\lambda}\left(\frac{a_{\lfloor p\rfloor-1}}{n^{p-\lfloor p\rfloor+1}}+\cdots+\frac{a_0}{n^p}\right)\right].\tag{53}
\]

原式问题保留：\(\bar u^{(1)}=0\) 的除法、\(G=\varnothing\) 的最大值以及 \(m_0<M\) 时 Eq. (40) 的引用范围是原路线缺口；不会由它们直接判断系数存在式为假。

<!-- proof:theorem3 -->
## B.4 — Proof of Theorem 3（PDF 20–21；本节重述印成 Theorem 6）

According to the definition of \(A^{(k)}\),
\[
\begin{aligned}
A^{(k)}&=\sum_{|S|=k}I(S)\quad\text{(55)}\\
&=\eta^{(k)}\sum_{|S|=k}|I(S)| &&\text{by the definition of }\eta^{(k)}.\quad\text{(56)}
\end{aligned}
\]
Then,
\[
\begin{aligned}
\frac{A^{(k)}}{\eta^{(k)}}&=\sum_{|S|=k}|I(S)|\quad\text{(57)}\\
&\ge\sum_{|S|=k,|I(S)|\ge\tau}|I(S)|\quad\text{(58)}\\
&\ge\tau R^{(k)} &&R^{(k)}=|\{S\subseteq N:|S|=k,|I(S)|\ge\tau\}|.\quad\text{(59)}
\end{aligned}
\]
The original text notes that \(A^{(k)}\) has the same sign as \(\eta^{(k)}\), so \(A^{(k)}/\eta^{(k)}>0\), and adds absolute values to obtain \(|A^{(k)}|/|\eta^{(k)}|\ge\tau R^{(k)}\). Since \(\tau>0\),
\[
R^{(k)}\le\frac{|A^{(k)}|}{\tau|\eta^{(k)}|}
=\frac{\bar u^{(1)}}{\tau|\eta^{(k)}|}\left|\lambda^{(k)}n^{p+\delta}+a_{\lfloor p\rfloor-1}^{(k)}n^{\lfloor p\rfloor-1}+\cdots+a_0^{(k)}\right|.\tag{60}
\]

<!-- proof:lemma4 -->
## B.5 — Proof of Lemma 4（PDF 21）

By the definition of the marginal benefit and universal matching,
\[
\begin{aligned}
\Delta u_T(S)
&=\sum_{L\subseteq T}(-1)^{|T|-|L|}u(L\cup S)\\
&=\sum_{L\subseteq T}(-1)^{|T|-|L|}\sum_{K\subseteq L\cup S}I(K)\\
&=\sum_{L\subseteq T}(-1)^{|T|-|L|}\sum_{L′\subseteq L}\sum_{S′\subseteq S}I(L′\cup S′)&&L\cap S=\varnothing\\
&=\sum_{S′\subseteq S}\left[\sum_{L\subseteq T}(-1)^{|T|-|L|}\sum_{L′\subseteq L}I(L′\cup S′)\right]\\
&=\sum_{S′\subseteq S}\left[\sum_{L′\subseteq T}\sum_{\substack{L\subseteq T\\L\supseteq L′}}(-1)^{|T|-|L|}I(L′\cup S′)\right]\\
&=\sum_{S′\subseteq S}\left[I(S′\cup T)+\sum_{L′\subsetneq T}\sum_{l=|L′|}^{|T|}\binom{|T|-|L′|}{l-|L′|}(-1)^{|T|-|L|}I(L′\cup S′)\right]\\
&=\sum_{S′\subseteq S}\left[I(S′\cup T)+\sum_{L′\subsetneq T}I(L′\cup S′)\underbrace{\sum_{l=|L′|}^{|T|}\binom{|T|-|L′|}{l-|L′|}(-1)^{|T|-|L|}}_{=0}\right]\\
&=\sum_{S′\subseteq S}I(S′\cup T).
\end{aligned}
\]
转录注：按 \(l\) 分层之后原指数仍印 \(|L|\)，在对应行 \(L\) 不再是约束变量；原式保留，项目有限分组证明显式将指数与分层基数对应。

<!-- proof:theorem4 -->
## B.5 — Proof of Theorem 4（PDF 22–23）

By the definition of the Shapley value,
\[
\begin{aligned}
\phi(i)&=\mathbb E_m\mathbb E_{\substack{S\subseteq N\setminus\{i\}\\|S|=m}}[u(S\cup\{i\})-u(S)]\\
&=\frac1{|N|}\sum_{m=0}^{|N|-1}\binom{|N|-1}m^{-1}\sum_{\substack{S\subseteq N\setminus\{i\}\\|S|=m}}[u(S\cup\{i\})-u(S)]\\
&=\frac1{|N|}\sum_{m=0}^{|N|-1}\binom{|N|-1}m^{-1}\sum_{\substack{S\subseteq N\setminus\{i\}\\|S|=m}}\Delta u_{\{i\}}(S)\\
&=\frac1{|N|}\sum_{m=0}^{|N|-1}\binom{|N|-1}m^{-1}\sum_{\substack{S\subseteq N\setminus\{i\}\\|S|=m}}\sum_{L\subseteq S}I(L\cup\{i\})&&\text{by Lemma 4}\\
&=\frac1{|N|}\sum_{L\subseteq N\setminus\{i\}}\sum_{m=0}^{|N|-1}\binom{|N|-1}m^{-1}\sum_{\substack{S\subseteq N\setminus\{i\}\\|S|=m,S\supseteq L}}I(L\cup\{i\})\\
&=\frac1{|N|}\sum_{L\subseteq N\setminus\{i\}}\sum_{m=|L|}^{|N|-1}\binom{|N|-1}m^{-1}\sum_{\substack{S\subseteq N\setminus\{i\}\\|S|=m,S\supseteq L}}I(L\cup\{i\})\\
&=\frac1{|N|}\sum_{L\subseteq N\setminus\{i\}}\sum_{m=|L|}^{|N|-1}\binom{|N|-1}m^{-1}\binom{|N|-|L|-1}{m-|L|}I(L\cup\{i\})\\
&=\frac1{|N|}\sum_{L\subseteq N\setminus\{i\}}I(L\cup\{i\})\underbrace{\sum_{k=0}^{|N|-|L|-1}\binom{|N|-1}{|L|+k}^{-1}\binom{|N|-|L|-1}k}_{=:w_L}.
\end{aligned}
\]
The proof lists: (i) \(m\binom nm=n\binom{n-1}{m-1}\); (ii) for \(p,q>0\),
\[
B(p,q)=\int_0^1x^{p-1}(1-x)^{1-q}\,dx;
\]
(iii) for positive integers, \(B(p,q)=\left[q\binom{p+q-1}{p-1}\right]^{-1}\), and for \(n>m>0\), \(\binom nm=[mB(n-m+1,m)]^{-1}\). The original Beta definition above is retained with its printed exponent error.
\[
\begin{aligned}
w_L&=\sum_{k=0}^{|N|-|L|-1}\binom{|N|-1}{|L|+k}^{-1}\binom{|N|-|L|-1}k\\
&=\sum_{k=0}^{|N|-|L|-1}\binom{|N|-|L|-1}k(|L|+k)B(|N|-|L|-k,|L|+k)\\
&=\underbrace{\sum_{k=0}^{|N|-|L|-1}|L|\binom{|N|-|L|-1}kB(|N|-|L|-k,|L|+k)}_{\text{①}}
+\underbrace{\sum_{k=0}^{|N|-|L|-1}k\binom{|N|-|L|-1}kB(|N|-|L|-k,|L|+k)}_{\text{②}}.
\end{aligned}
\]
For ①,
\[
\begin{aligned}
\text{①}&=\int_0^1\sum_{k=0}^{|N|-|L|-1}|L|\binom{|N|-|L|-1}k x^{|N|-|L|-k-1}(1-x)^{|L|+k-1}\,dx\\
&=\int_0^1|L|\underbrace{\left[\sum_{k=0}^{|N|-|L|-1}\binom{|N|-|L|-1}k x^{|N|-|L|-k-1}(1-x)^k\right]}_{=1}(1-x)^{|L|-1}\,dx\\
&=\int_0^1|L|(1-x)^{|L|-1}\,dx=1.
\end{aligned}
\]
For ②, using \(k\binom ak=a\binom{a-1}{k-1}\) and then \(k'=k-1\),
\[
\begin{aligned}
\text{②}&=\sum_{k=1}^{|N|-|L|-1}(|N|-|L|-1)\binom{|N|-|L|-2}{k-1}B(|N|-|L|-k,|L|+k)\\
&=(|N|-|L|-1)\sum_{k'=0}^{|N|-|L|-2}\binom{|N|-|L|-2}{k'}B(|N|-|L|-k'-1,|L|+k'+1)\\
&=(|N|-|L|-1)\int_0^1\sum_{k'=0}^{|N|-|L|-2}\binom{|N|-|L|-2}{k'}x^{|N|-|L|-k'-2}(1-x)^{|L|+k'}\,dx\\
&=(|N|-|L|-1)\int_0^1\underbrace{\left[\sum_{k'=0}^{|N|-|L|-2}\binom{|N|-|L|-2}{k'}x^{|N|-|L|-k'-2}(1-x)^{k'}\right]}_{=1}(1-x)^{|L|}\,dx\\
&=(|N|-|L|-1)\int_0^1(1-x)^{|L|}\,dx=\frac{|N|-|L|-1}{|L|+1}.
\end{aligned}
\]
Hence \(w_L=\text{①}+\text{②}=1+(|N|-|L|-1)/(|L|+1)=|N|/(|L|+1)\), and
\[
\phi(i)=\frac1{|N|}\sum_{L\subseteq N\setminus\{i\}}w_L I(L\cup\{i\})
=\sum_{S\subseteq N\setminus\{i\}}\frac{I(S\cup\{i\})}{|S|+1}.
\]

<!-- proof:theorem5 -->
## B.6 — Proof of Theorem 5（PDF 23–25）

The Shapley interaction index is defined by
\[
I^{\rm Shapley}(T)=\sum_{S\subseteq N\setminus T}\frac{|S|!(|N|-|S|-|T|)!}{(|N|-|T|+1)!}\Delta u_T(S).
\]
Then,
\[
\begin{aligned}
I^{\rm Shapley}(T)
&=\frac1{|N|-|T|+1}\sum_{m=0}^{|N|-|T|}\binom{|N|-|T|}m^{-1}\sum_{\substack{S\subseteq N\setminus T\\|S|=m}}\Delta u_T(S)\\
&=\frac1{|N|-|T|+1}\sum_{m=0}^{|N|-|T|}\binom{|N|-|T|}m^{-1}\sum_{\substack{S\subseteq N\setminus T\\|S|=m}}\sum_{L\subseteq S}I(L\cup T)&&\text{by Lemma 4}\\
&=\frac1{|N|-|T|+1}\sum_{L\subseteq N\setminus T}\sum_{m=|L|}^{|N|-|T|}\binom{|N|-|T|}m^{-1}\sum_{\substack{S\subseteq N\setminus T\\|S|=m,S\supseteq L}}I(L\cup T)\\
&=\frac1{|N|-|T|+1}\sum_{L\subseteq N\setminus T}\sum_{m=|L|}^{|N|-|T|}\binom{|N|-|T|}m^{-1}\binom{|N|-|L|-|T|}{m-|L|}I(L\cup T)\\
&=\frac1{|N|-|T|+1}\sum_{L\subseteq N\setminus T}I(L\cup T)\underbrace{\sum_{k=0}^{|N|-|L|-|T|}\binom{|N|-|T|}{|L|+k}^{-1}\binom{|N|-|L|-|T|}k}_{=:w_L}.
\end{aligned}
\]
As in Theorem 4, the proof uses combinatorial numbers and the Beta function:
\[
\begin{aligned}
w_L&=\sum_{k=0}^{|N|-|L|-|T|}\binom{|N|-|T|}{|L|+k}^{-1}\binom{|N|-|L|-|T|}k\\
&=\sum_{k=0}^{|N|-|L|-|T|}\binom{|N|-|L|-|T|}k(|L|+k)B(|N|-|L|-|T|-k+1,|L|+k)\\
&=\underbrace{\sum_{k=0}^{|N|-|L|-|T|}|L|\binom{|N|-|L|-|T|}kB(|N|-|L|-|T|-k+1,|L|+k)}_{\text{①}}\\
&\quad+\underbrace{\sum_{k=0}^{|N|-|L|-|T|}k\binom{|N|-|L|-|T|}kB(|N|-|L|-|T|-k+1,|L|+k)}_{\text{②}}.
\end{aligned}
\]
For ①,
\[
\begin{aligned}
\text{①}&=\int_0^1\sum_{k=0}^{|N|-|L|-|T|}|L|\binom{|N|-|L|-|T|}k x^{|N|-|L|-|T|-k}(1-x)^{|L|+k-1}\,dx\\
&=\int_0^1|L|\underbrace{\left[\sum_{k=0}^{|N|-|L|-|T|}\binom{|N|-|L|-|T|}k x^{|N|-|L|-|T|-k}(1-x)^k\right]}_{=1}(1-x)^{|L|-1}\,dx\\
&=\int_0^1|L|(1-x)^{|L|-1}\,dx=1.
\end{aligned}
\]
For ②,
\[
\begin{aligned}
\text{②}&=\sum_{k=1}^{|N|-|L|-|T|}(|N|-|L|-|T|)\binom{|N|-|L|-|T|-1}{k-1}B(|N|-|L|-|T|-k+1,|L|+k)\\
&=(|N|-|L|-|T|)\sum_{k'=0}^{|N|-|L|-|T|-1}\binom{|N|-|L|-|T|-1}{k'}B(|N|-|L|-|T|-k',|L|+k'+1)\\
&=(|N|-|L|-|T|)\int_0^1\sum_{k'=0}^{|N|-|L|-|T|-1}\binom{|N|-|L|-|T|-1}{k'}x^{|N|-|L|-|T|-k'-1}(1-x)^{|L|+k'}\,dx\\
&=(|N|-|L|-|T|)\int_0^1\underbrace{\left[\sum_{k'=0}^{|N|-|L|-|T|-1}\binom{|N|-|L|-|T|-1}{k'}x^{|N|-|L|-|T|-k'-1}(1-x)^{k'}\right]}_{=1}(1-x)^{|L|}\,dx\\
&=(|N|-|L|-|T|)\int_0^1(1-x)^{|L|}\,dx=\frac{|N|-|L|-|T|}{|L|+1}.
\end{aligned}
\]
Hence \(w_L=1+(|N|-|L|-|T|)/(|L|+1)=(|N|-|T|+1)/(|L|+1)\), and
\[
I^{\rm Shapley}(T)=\frac1{|N|-|T|+1}\sum_{L\subseteq N\setminus T}w_L I(L\cup T)
=\sum_{L\subseteq N\setminus T}\frac{I(L\cup T)}{|L|+1}.
\]

<!-- proof:theorem6 -->
## B.7 — Proof of Theorem 6（PDF 25–27）

By the definition of the Shapley–Taylor interaction index,
\[
I^{\rm Shapley\text{-}Taylor(k)}(T)=
\begin{cases}
\Delta u_T(\varnothing),&|T|<k,\\
\displaystyle\frac{k}{|N|}\sum_{S\subseteq N\setminus T}\binom{|N|-1}{|S|}^{-1}\Delta u_T(S),&|T|=k,\\
0,&|T|>k.
\end{cases}
\]
When \(|T|<k\), Eq. (1) gives
\[
I^{\rm Shapley\text{-}Taylor(k)}(T)=\Delta u_T(\varnothing)=\sum_{L\subseteq T}(-1)^{|T|-|L|}u(L)=I(T).
\]
When \(|T|=k\),
\[
\begin{aligned}
I^{\rm Shapley\text{-}Taylor(k)}(T)
&=\frac{k}{|N|}\sum_{S\subseteq N\setminus T}\binom{|N|-1}{|S|}^{-1}\Delta u_T(S)\\
&=\frac{k}{|N|}\sum_{m=0}^{|N|-k}\sum_{\substack{S\subseteq N\setminus T\\|S|=m}}\binom{|N|-1}{|S|}^{-1}\Delta u_T(S)\\
&=\frac{k}{|N|}\sum_{m=0}^{|N|-k}\sum_{\substack{S\subseteq N\setminus T\\|S|=m}}\binom{|N|-1}{|S|}^{-1}\sum_{L\subseteq S}I(L\cup T)&&\text{by Lemma 4}\\
&=\frac{k}{|N|}\sum_{L\subseteq N\setminus T}\sum_{m=|L|}^{|N|-k}\binom{|N|-1}{|S|}^{-1}\sum_{\substack{S\subseteq N\setminus T\\|S|=m,S\supseteq L}}I(L\cup T)\\
&=\frac{k}{|N|}\sum_{L\subseteq N\setminus T}\sum_{m=|L|}^{|N|-k}\binom{|N|-1}{|S|}^{-1}\binom{|N|-|L|-k}{m-|L|}I(L\cup T)\\
&=\frac{k}{|N|}\sum_{L\subseteq N\setminus T}I(L\cup T)\underbrace{\sum_{m=0}^{|N|-|L|-k}\binom{|N|-1}{|L|+m}^{-1}\binom{|N|-|L|-k}m}_{=:w_L}.
\end{aligned}
\]
The proof again uses the earlier combinatorial and Beta properties:
\[
\begin{aligned}
w_L&=\sum_{m=0}^{|N|-|L|-k}\binom{|N|-1}{|L|+m}^{-1}\binom{|N|-|L|-k}m\\
&=\sum_{m=0}^{|N|-|L|-k}\binom{|N|-|L|-k}m(|L|+m)B(|N|-|L|-m,|L|+m)\\
&=\underbrace{\sum_{m=0}^{|N|-|L|-k}|L|\binom{|N|-|L|-k}mB(|N|-|L|-m,|L|+m)}_{\text{①}}\\
&\quad+\underbrace{\sum_{m=0}^{|N|-|L|-k}m\binom{|N|-|L|-k}mB(|N|-|L|-m,|L|+m)}_{\text{②}}.
\end{aligned}
\]
For ①,
\[
\begin{aligned}
\text{①}&=\int_0^1\sum_{m=0}^{|N|-|L|-k}|L|\binom{|N|-|L|-k}m x^{|N|-|L|-m-1}(1-x)^{|L|+m-1}\,dx\\
&=\int_0^1|L|\underbrace{\left[\sum_{m=0}^{|N|-|L|-k}\binom{|N|-|L|-k}m x^{|N|-|L|-m-k}(1-x)^m\right]}_{=1}x^{k-1}(1-x)^{|L|-1}\,dx\\
&=\int_0^1|L|x^{k-1}(1-x)^{|L|-1}\,dx=|L|B(k,|L|)=\binom{|L|+k-1}{k-1}^{-1}.
\end{aligned}
\]
For ②, with \(m'=m-1\),
\[
\begin{aligned}
\text{②}&=\sum_{m=1}^{|N|-|L|-k}(|N|-|L|-k)\binom{|N|-|L|-k-1}{m-1}B(|N|-|L|-m,|L|+m)\\
&=\sum_{m'=0}^{|N|-|L|-k-1}(|N|-|L|-k)\binom{|N|-|L|-k-1}{m'}B(|N|-|L|-m'-1,|L|+m'+1)\\
&=\int_0^1(|N|-|L|-k)\sum_{m'=0}^{|N|-|L|-k-1}\binom{|N|-|L|-k-1}{m'}x^{|N|-|L|-m'-2}(1-x)^{|L|+m'}\,dx\\
&=\int_0^1(|N|-|L|-k)\underbrace{\left[\sum_{m'=0}^{|N|-|L|-k-1}\binom{|N|-|L|-k-1}{m'}x^{|N|-|L|-m'-k-1}(1-x)^{m'}\right]}_{=1}x^{k-1}(1-x)^{|L|}\,dx\\
&=\int_0^1(|N|-|L|-k)x^{k-1}(1-x)^{|L|}\,dx=(|N|-|L|-k)B(k,|L|+1)\\
&=\frac{|N|-|L|-k}{(|L|+1)\binom{|L|+k}{k-1}}.
\end{aligned}
\]
Hence,
\[
\begin{aligned}
w_L&=\text{①}+\text{②}=\binom{|L|+k-1}{k-1}^{-1}+\frac{|N|-|L|-k}{(|L|+1)\binom{|L|+k}{k-1}}\\
&=\frac{|L|!(k-1)!}{(|L|+k-1)!}+\frac{|N|-|L|-k}{|L|+1}\frac{(|L|+1)!(k-1)!}{(|L|+k)!}\\
&=\frac{|L|!(k-1)!}{(|L|+k-1)!}+\frac{|N|-|L|-k}{|L|+k}\frac{|L|!(k-1)!}{(|L|+k-1)!}\\
&=\left[1+\frac{|N|-|L|-k}{|L|+k}\right]\frac{|L|!(k-1)!}{(|L|+k-1)!}\\
&=\frac{|N|}{|L|+k}\frac{|L|!(k-1)!}{(|L|+k-1)!}\\
&=\frac{|N|}{k}\frac{|L|!k!}{(|L|+k)!}=\frac{|N|}{k}\binom{|L|+k}{k}^{-1}.
\end{aligned}
\]
Therefore, when \(|T|=k\),
\[
\begin{aligned}
I^{\rm Shapley\text{-}Taylor}(T)
&=\frac{k}{|N|}\sum_{L\subseteq N\setminus T}w_L I(L\cup T)\\
&=\frac{k}{|N|}\sum_{L\subseteq N\setminus T}\frac{|N|}{k}\binom{|L|+k}{k}^{-1}I(L\cup T)\\
&=\sum_{L\subseteq N\setminus T}\binom{|L|+k}{k}^{-1}I(L\cup T).
\end{aligned}
\]
When \(|T|>k\), the displayed definition already gives zero. The zero-parameter \(L=\varnothing\) Beta boundary, the printed Beta exponent, and the free \(|S|\) denominators in the reordered original sums are retained and marked as source-proof issues; none is silently repaired in this original layer.
