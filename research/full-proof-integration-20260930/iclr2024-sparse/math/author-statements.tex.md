# 正式原陈述与原定义：精确数学边界

仅用正式版，保留作者 \(u\)、输入基线 \(b\) 及原标签。这里是原数学陈述的 TeX 转录；项目规范符号、解释和修复证明不混入原陈述。原始 PDF 与原文文本仍保留。

<!-- statement:definitions -->
Given \(v\), \(x=[x_1,\ldots,x_n]^\top\), and \(N=\{1,\ldots,n\}\), the Harsanyi interaction is
\[
I(S)\stackrel{\rm def}{=}\sum_{T\subseteq S}(-1)^{|S|-|T|}u(T),\qquad
u(T)\stackrel{\rm def}{=}v(x_T)-v(x_\varnothing).\tag{1}
\]
The variables in \(N\setminus T\) are masked using \(b=[b_1,\ldots,b_n]^\top\), and those in \(T\) remain unchanged. In particular, \(u(\varnothing)=I(\varnothing)=0\). For classification, the paper uses \(v(x)=\log[p(y=y^{\rm truth}\mid x)/(1-p(y=y^{\rm truth}\mid x))]\).

<!-- statement:desiderata -->
The paper lists: (1) sparsity — few salient interactions on a specific sample; (2) universal matching — output on any masked sample is well matched by specific interactions; (3) sample-wise transferability — salient interactions are shared across different samples in the same category. The empirical observations are attributed to Li & Zhang (2023b).

<!-- statement:reconstruction -->
Theorem 1. Let the input sample \(x\) be arbitrarily masked to obtain \(x_S\). The output can be disentangled into all interaction effects within \(S\):
\[
\forall S\subseteq N,\qquad v(x_S)=\sum_{T\subseteq S}I(T)+v(x_\varnothing).\tag{7}
\]

<!-- statement:salient-approximation -->
The inference score can be summarized by a small number of salient interactions:
\[
v(x)\approx\sum_{S\in\Omega_{\rm salient},S\ne\varnothing}I(S)+v(x_\varnothing).
\]
This is the original qualitative approximation formula; the paper gives no explicit uniform remainder tolerance in this displayed statement.

<!-- statement:taylor-expansion -->
The Taylor expansion of \(v(x)\) at \(b=[b_1,\ldots,b_n]^\top\) is displayed as
\[
v(x)=\sum_{\kappa_1=0}^{\infty}\cdots\sum_{\kappa_n=0}^{\infty}
\left.\frac{\partial^{\kappa_1+\cdots+\kappa_n}v}{\partial x_1^{\kappa_1}\cdots\partial x_n^{\kappa_n}}\right|_{x=b}
\frac{(x_1-b_1)^{\kappa_1}\cdots(x_n-b_n)^{\kappa_n}}{\kappa_1!\cdots\kappa_n!}.\tag{2}
\]

<!-- statement:assumption-1alpha -->
Assumption 1-α. Interactions higher than the \(M\)-th order have zero effect:
\[
\forall S\in\{S\subseteq N:|S|\ge M+1\},\qquad I(S)=0,
\quad\operatorname{order}(S)\stackrel{\rm def}{=}|S|.
\]

<!-- statement:assumption-1beta -->
Assumption 1-β. The network has at most \(M\)-order nonzero derivatives:
\[
\forall b\in\mathbb R^n,\ \forall\kappa_1,\ldots,\kappa_n\in\mathbb N,
\quad\kappa_1+\cdots+\kappa_n\ge M+1\ \Rightarrow\
\left.\frac{\partial^{\kappa_1+\cdots+\kappa_n}v}{\partial x_1^{\kappa_1}\cdots\partial x_n^{\kappa_n}}\right|_{x=b}=0.
\]
The surrounding text restricts this assumption to continuously differentiable functions, and notes that later proofs need only 1-α.

<!-- statement:lemma1 -->
Lemma 1. The effect \(I(S)\), \(S\ne\varnothing\), can be rewritten as
\[
I(S)=\sum_{\kappa\in Q_S}
\left.\frac{\partial^{\kappa_1+\cdots+\kappa_n}v}{\partial x_1^{\kappa_1}\cdots\partial x_n^{\kappa_n}}\right|_{x=b}
\frac{\prod_{i\in S}(x_i-b_i)^{\kappa_i}}{\kappa_1!\cdots\kappa_n!},\tag{8}
\]
where \(Q_S=\{[\kappa_1,\ldots,\kappa_n]^\top:\kappa_i\in\mathbb N^+\ (i\in S),\ \kappa_i=0\ (i\notin S)\}\). A similar proof is attributed to Ren et al. (2023c). This is presented as a preparatory lemma before the derivation from 1-β to 1-α; its independent statement does not add a Taylor convergence condition.

<!-- statement:derivative-cutoff -->
Combining Lemma 1 and Assumption 1-β gives Assumption 1-α:
\[
\forall S\in\{S\subseteq N:|S|\ge M+1\},\qquad I(S)=0.
\]

<!-- statement:assumption2 -->
Assumption 2 (Monotonicity). The average output increases monotonically with the number of unmasked variables:
\[
\forall m′\le m,\qquad\bar u^{(m′)}\le\bar u^{(m)},
\quad\bar u^{(m)}\stackrel{\rm def}{=}\mathbb E_{|S|=m}[u(S)],
\quad u(S)=v(x_S)-v(x_\varnothing).
\]

<!-- statement:assumption3 -->
Assumption 3. For \(m′\le m\),
\[
\bar u^{(m′)}\ge\left(\frac{m′}{m}\right)^p\bar u^{(m)},\qquad p>0.
\]
The statement does not separately define \(0/0\) for \(m=0\); the proof uses \(m′=1\) and positive \(m\).

<!-- statement:order-statistics -->
\[
A^{(k)}\stackrel{\rm def}{=}\sum_{S\subseteq N,|S|=k}I(S),\qquad
\eta^{(k)}\stackrel{\rm def}{=}\frac{\sum_{|S|=k}I(S)}{\sum_{|S|=k}|I(S)|},\qquad
R^{(k)}\stackrel{\rm def}{=}|\{S\subseteq N:|S|=k,|I(S)|\ge\tau\}|.
\]
Case 1 sets \(|\eta^{(k)}|\gg1/n\); the salient threshold obeys \(0<\tau\ll\mathbb E_{T\subseteq S}|u(T)|\).

<!-- statement:lemma2 -->
Lemma 2. For every \(M\le m\le n\),
\[
\bar u^{(m)}=\sum_{k=1}^M\frac{\binom mk}{\binom nk}A^{(k)},\qquad
A^{(k)}=\sum_{T\subseteq N,|T|=k}I(T).\tag{16}
\]

<!-- statement:lemma3 -->
Lemma 3. Given \(n,M\in\mathbb N^+\), \(M<n\), if
\[
\forall m\in\{n,n-1,\ldots,n-M\},\qquad\sum_{k=1}^M\frac{\binom mk}{\binom nk}w_k=0,
\]
then \(w_k=0\) for \(k=1,\ldots,M\).

<!-- statement:theorem2 -->
Theorem 2. There exists \(m_0\in\{n,n-1,\ldots,n-M\}\) such that for all \(1\le k\le M\),
\[
A^{(k)}=\left(\lambda^{(k)}n^{p+\delta}+a_{\lfloor p\rfloor-1}^{(k)}n^{\lfloor p\rfloor-1}+\cdots+a_1^{(k)}n+a_0^{(k)}\right)\bar u^{(1)}.\tag{37}
\]
Here \(|\lambda^{(k)}|\le1\), \(|a_0^{(k)}|<n\), \(|a_i^{(k)}|\in\{0,1,\ldots,n-1\}\) for \(i=1,\ldots,\lfloor p\rfloor-1\), and
\[
\delta\le\log_n\left[\frac1\lambda\left(1-\frac{a_{\lfloor p\rfloor-1}}{n^{p-\lfloor p\rfloor+1}}-\cdots-\frac{a_0}{n^p}\right)\right]\quad\text{if }\lambda>0,\tag{38}
\]
\[
\delta\le\log_n\left[\frac1{-\lambda}\left(\frac{a_{\lfloor p\rfloor-1}}{n^{p-\lfloor p\rfloor+1}}+\cdots+\frac{a_0}{n^p}\right)\right]\quad\text{if }\lambda<0.\tag{39}
\]
\[
\lambda\stackrel{\rm def}{=}\sum_{k=1}^M\frac{\binom{m_0}k}{\binom nk}\lambda^{(k)}\ne0,
\qquad a_i\stackrel{\rm def}{=}\sum_{k=1}^M\frac{\binom{m_0}k}{\binom nk}a_i^{(k)},\quad i=0,\ldots,\lfloor p\rfloor-1.
\]
The main-text copies of these expressions are numbered (3)–(5).

<!-- statement:asymptotic-claim -->
The text interprets Theorem 2 as \(A^{(k)}=O(n^{p+\delta})\), and Theorem 3 as \(R^{(k)}=O(n^{p+\delta}/|\tau\eta^{(k)}|)\), usually much less than \(\binom nk\). Case 2 says this is still much less if \(|\eta^{(k)}|\) is not exponentially small. These are original asymptotic interpretations, not additional explicitly quantified theorems.

<!-- statement:theorem3 -->
Theorem 3 (main text; B.4 prints “Theorem 6”). The upper bound is
\[
R^{(k)}\le\frac{\bar u^{(1)}}{\tau|\eta^{(k)}|}\left|\lambda^{(k)}n^{p+\delta}+a_{\lfloor p\rfloor-1}^{(k)}n^{\lfloor p\rfloor-1}+\cdots+a_0^{(k)}\right|.\tag{54}
\]
The main-text formula is Eq. (6); the statement occurs under Case 1's non-cancellation discussion.

<!-- statement:axiom-linearity -->
A.1(2) Linearity. If \(u(S)=u_1(S)+u_2(S)\) for every \(S\subseteq N\), then
\[
\forall S\subseteq N,\qquad I_u(S)=I_{u_1}(S)+I_{u_2}(S).
\]

<!-- statement:axiom-dummy -->
A.1(3) Dummy. If \(i\in N\) obeys
\[
\forall T\subseteq N\setminus\{i\},\qquad u(T\cup\{i\})=u(T)+u(\{i\}),
\]
then \(\forall\varnothing\ne S\subseteq N\setminus\{i\},\ I(S\cup\{i\})=0\).

<!-- statement:axiom-symmetry -->
A.1(4) Symmetry. If \(i,j\in N\) cooperate in the same way,
\[
\forall T\subseteq N\setminus\{i,j\},\qquad u(T\cup\{i\})=u(T\cup\{j\}),
\]
then \(\forall S\subseteq N\setminus\{i,j\},\ I(S\cup\{i\})=I(S\cup\{j\})\).

<!-- statement:axiom-anonymity -->
A.1(5) Anonymity. For every permutation \(\pi\) on \(N\),
\[
\forall S\subseteq N,\quad I_u(S)=I_{\pi u}(\pi S),\qquad
\pi S=\{\pi(i):i\in S\},\quad(\pi u)(\pi S)=u(S).
\]

<!-- statement:axiom-recursive -->
A.1(6) Recursive. For \(i\in N\), \(S\subseteq N\setminus\{i\}\),
\[
I(S\cup\{i\})=I(S\mid i\text{ is always present})-I(S),\qquad
I(S\mid i\text{ is always present})=\sum_{L\subseteq S}(-1)^{|S|-|L|}u(L\cup\{i\}).
\]

<!-- statement:axiom-distribution -->
A.1(7) Interaction distribution. An interaction function is
\[
u_T(S)=\begin{cases}c&T\subseteq S,\\0&\text{otherwise}.\end{cases}
\]
Its interactions satisfy \(I(T)=c\), and \(I(S)=0\) for all \(S\ne T\).

<!-- statement:lemma4 -->
Lemma 4 (Connection to the marginal benefit). For \(T\subseteq N\setminus S\),
\[
\Delta u_T(S)=\sum_{L\subseteq T}(-1)^{|T|-|L|}u(L\cup S)
=\sum_{S′\subseteq S}I(T\cup S′).
\]

<!-- statement:theorem4 -->
Theorem 4. The Shapley value is a uniform allocation of every interaction to its participating variables:
\[
\phi(i)=\sum_{S\subseteq N\setminus\{i\}}\frac1{|S|+1}I(S\cup\{i\}).
\]
The paper cites Shapley (1953) and Harsanyi (1963), and also proves it in B.5.

<!-- statement:theorem5 -->
Theorem 5. Given \(T\subseteq N\),
\[
I^{\rm Shapley}(T)=\sum_{S\subseteq N\setminus T}\frac1{|S|+1}I(S\cup T).
\]
The explanation treats the variables in \(T\) as a single coalition. The paper cites Grabisch & Roubens (1999) and Ren et al. (2023a), and proves it in B.6.

<!-- statement:theorem6 -->
Theorem 6. The \(k\)-th order Shapley–Taylor interaction index has the form
\[
I^{\rm Shapley\text{-}Taylor}(T)=\begin{cases}
I(T)&|T|<k,\\
\displaystyle\sum_{S\subseteq N\setminus T}\binom{|S|+k}k^{-1}I(S\cup T)&|T|=k,\\
0&|T|>k.
\end{cases}
\]
The paper cites Sundararajan et al. (2020) and Ren et al. (2023a), and proves it in B.7.

<!-- statement:noise-linearity -->
Scenario 1. Write \(v′(x_S)=v(x_S)+\varepsilon_S\). The interaction is
\[
I′(S)=I(S)+I_\varepsilon(S),\qquad
I_\varepsilon(S)=\sum_{T\subseteq S}(-1)^{|S|-|T|}(\varepsilon_T-\varepsilon_\varnothing).
\]

<!-- statement:noise-variance -->
Scenario 1 continues: because \(I_\varepsilon(S)\) is a sum of \(2^{|S|}\) noise terms, its variance with respect to the noise is \(2^{|S|}\) times larger. The noise is described as “fully random”; the formal statement here does not explicitly supply independence or common variance.

<!-- statement:parity-mask -->
Scenario 2. If \(|S|\) is odd, \(u(S)=+1\); otherwise \(u(S)=-1\). The paper states that \(I(S)\) is positive for odd \(|S|\) and negative for even \(|S|\), and is not sparse.

<!-- statement:or-density -->
Scenario 3. A high-order OR such as “blue patch 1” \(\lor\cdots\lor\) “blue patch \(m\)” is explained by many lower-order Harsanyi interactions. The paper proposes removing such a high-order concept before explaining the remaining output. No numerical bound or local proof is supplied here.

<!-- statement:periodic-density -->
Scenario 4. The example \(v(x_S)=\sin(\sum_{i\in S}x_i)\) is described as having non-sparse interactions and violating 1-α, 1-β and monotonicity. No quantified range of \(x_i\), salience threshold or independent proof is given.

<!-- statement:parity-task -->
Scenario 5 and E.3 discuss classifying the parity of binary sequences. A trained three-layer MLP on length-10 sequences is reported to reach 100% training accuracy with estimated \(p\) around 9.9–19.7. These are empirical results, not a new exact theorem.

<!-- statement:transfer-inference -->
Section 4 states that sparsity plus universal matching gives sample-wise transferability by contradiction: if interactions differ across samples, the number of interaction patterns encoded by the DNN would be explosively large. The earlier definition specifies samples in the same category.

<!-- statement:or-reverse -->
D.2 defines, for \(S\ne\varnothing\),
\[
I_{or}(S)=-\sum_{T\subseteq S}(-1)^{|S|-|T|}u(N\setminus T),\quad
u(N\setminus T)=v(x_{N\setminus T})-v(x_\varnothing),\quad I_{or}(\varnothing)=u(\varnothing)=0.\tag{61}
\]
An OR interaction is described as a specific AND interaction after exchanging masked and unmasked states.

<!-- statement:and-or-matching -->
D.2 quotes the learned decomposition and matching formulas
\[
u(S)=u_{and}(S)+u_{or}(S),\quad
u_{and}(S)=\sum_{T\subseteq S}I_{and}(T),\quad
u_{or}(S)=\sum_{T\cap S\ne\varnothing}I_{or}(T),\tag{62}
\]
with \(I_{and}(\varnothing)=u_{and}(\varnothing)=0\) and \(I_{or}(\varnothing)=u_{or}(\varnothing)=0\). This is attributed to Li & Zhang (2023a).

<!-- statement:and-or-optimization -->
D.2 prints the parameterization
\[
u_{and}(S)=0.5u(S)+\gamma_S,\qquad u_{and}(S)=0.5u(S)-\gamma_S,
\]
and the loss
\[
\min_{\{\gamma_S\}}\sum_{S\subseteq N}|I_{and}(S)|+|I_{or}(S)|.\tag{63}
\]
The noise-removal parameterization is printed as
\[
u_{and}(S)=0.5(u(S)-\varepsilon_S)+\gamma_S,\qquad
u_{or}(S)=0.5(u(S)-\varepsilon_S)+\gamma_S,
\]
with \(\varepsilon_S\in[-\zeta,\zeta]\), \(\zeta=0.04|v(x)-v(x_\varnothing)|\). These duplicated names and repeated plus signs are original printed formulas, retained as source issues.

<!-- statement:threshold-discussion -->
Appendix F argues that most interactions with \(|I(S)|<\tau\) actually have \(I(S)=0\), because the signed sum of \(2^{|S|}\) outputs cancels if the exact AND relation is absent. The text also explicitly does not exclude a few extremely small nonzero interactions; it is a heuristic discussion, not a probability theorem.

<!-- statement:monotonicity-example -->
Appendix H gives \(v(x)=x_1x_2x_3+x_1x_2+x_2x_3+x_2+x_3\), five binary variables, and the following original full tables:
\[
\begin{array}{c|rrrrrrrrrr}
S&12&13&14&15&23&24&25&34&35&45\\\hline
u(S)&2&1&0&0&3&1&1&1&1&0
\end{array}
\]
\[
\begin{array}{c|rrrrrrrrrr}
S&123&124&125&134&135&145&234&235&245&345\\\hline
u(S)&5&2&2&1&1&0&3&3&1&0
\end{array}
\]
The author then prints \(\mathbb E_{|S|=2}u(S)=1\le1.8=\mathbb E_{|S|=3}u(S)\). The last original table value and the 1.8 are retained here; project arithmetic correction is separately marked.

<!-- statement:sampling-complexity -->
Appendix I samples \(\{S_1,\ldots,S_t\}\) at each order \(m\), with \(|S_i|=m\), and uses
\[
\bar u^{(m)}\approx\frac1t\sum_{i=1}^tu(S_i).
\]
It states that estimating monotonicity and \(p\) this way costs \(O(nt)\), compared with \(O(2^n)\) full enumeration. No confidence bound is stated.

<!-- statement:experiments -->
Figures 2–14 and Tables 1–2 report empirical interaction strengths, monotonicity percentages, \(p\), valid-interaction counts and computed bounds. The definitions used include \(\widetilde I(S)=I(S)/\max_{S′}|I(S′)|\), \(I_{str}^{(m)}=\mathbb E_{|S|=m}|I(S)|\), and thresholds \(0.05\max_{S′}|I(S′)|\) (LLMs) or \(0.1\max_{S′}|I(S′)|\) (the tabular MLP). All numerical experimental pages remain directly accessible, but are not original proofs.

<!-- statement:related-work -->
Section 2 surveys external results on defining, extracting and using game-theoretic interactions. These cited papers' own proofs are not locally reproduced in this formal document and are not counted as new local proofs.
