"""Manually checked TeX transcriptions; source errors remain verbatim in equations.
Connecting prose is project Chinese translation. PDF text files are separate evidence.
"""
T={}
T['taylor']=r'''作者首先把右端记为候选交互 $\widetilde I(S\mid x')=\sum_{\pi\in Q_S}U_{S,\pi}J(S,\pi\mid x')$。需要对任意 $x'$ 证明 $\widetilde I=I$。作者引用 Harsanyi 交互是满足忠实重构要求的唯一指标：
$$\forall T\subseteq N,\quad v(x'_T)=\sum_{S\subseteq T}I(S\mid x').$$
因此只要候选也满足该重构，就可由唯一性得到结论。作者在全遮罩基线 $x'_\varnothing=r$ 展开：
$$v(x'_T)=\sum_{\pi_1=0}^{\infty}\cdots\sum_{\pi_n=0}^{\infty}\frac1{\prod_{i=1}^n\pi_i!}\frac{\partial^m v(x'_\varnothing)}{\partial x_1^{\pi_1}\cdots\partial x_n^{\pi_n}}\prod_{i=1}^n[(x'_T)_i-r_i]^{\pi_i},\quad m=\sum_i\pi_i.$$
遮罩规则给 $i\in T$ 时 $(x'_T)_i=x'_i$、$i\notin T$ 时 $(x'_T)_i=r_i$；正次数的被遮罩因子为零。零次幂按 $1$ 处理，所以只保留 $P_T=\{\pi:\pi_i\in\mathbb N\ (i\in T),\pi_i=0\ (i\notin T)\}$：
$$v(x'_T)=\sum_{\pi\in P_T}\frac1{\prod_i\pi_i!}\frac{\partial^m v(x'_\varnothing)}{\partial x_1^{\pi_1}\cdots\partial x_n^{\pi_n}}\prod_{i\in T}(x'_i-r_i)^{\pi_i}.$$
$P_T$ 分为互不相交的 $Q_S$，$S\subseteq T$，其中 $Q_S=\{\pi:\pi_i\in\mathbb N^+\ (i\in S),\pi_i=0\ (i\notin S)\}$。取 $\delta_i=\operatorname{sign}(x'_i-r_i)\in\{-1,1\}$，利用 $\prod_{i\in S}\delta_i^{2\pi_i}=1$，作者写成
$$\begin{aligned}v(x'_T)&=\sum_{S\subseteq T}\sum_{\pi\in Q_S}\frac1{\prod_i\pi_i!}\frac{\partial^m v(x'_\varnothing)}{\partial x_1^{\pi_1}\cdots\partial x_n^{\pi_n}}\prod_{i\in S}(x'_i-r_i)^{\pi_i}\\&=\sum_{S\subseteq T}\sum_{\pi\in Q_S}\underbrace{\frac{\tau^m}{\prod_i\pi_i!}\frac{\partial^m v(x'_\varnothing)}{\partial x_1^{\pi_1}\cdots\partial x_n^{\pi_n}}\prod_{i\in S}\delta_i^{\pi_i}}_{U_{S,\pi}}\underbrace{\prod_{i\in S}\left(\delta_i\frac{x'_i-r_i}{\tau}\right)^{\pi_i}}_{J(S,\pi\mid x')}\\&=\sum_{S\subseteq T}\widetilde I(S\mid x').\end{aligned}$$
因此候选在 $\Omega=2^N$ 时满足忠实性；作者据此结束证明。原文中的无限 Taylor 等式、$\delta_i$ 定义及零坐标问题完整保留，项目的语义审查另列。'''
T['dyn-taylor']=r'''作者记 Eq.(19) 右端为 $K(T\mid x)=\sum_{\pi\in Q_T}\frac1{\prod_i\pi_i!}\left.\frac{\partial^{\pi_1+\cdots+\pi_n}v}{\partial x_1^{\pi_1}\cdots\partial x_n^{\pi_n}}\right|_{x=x_\varnothing}\prod_{i\in T}(x_i-b_i)^{\pi_i}$（Eq.(20)）。引用交互满足重构 $\forall S\subseteq N,v(x_S)=\sum_{\varnothing\ne T\subseteq S}I(T\mid x)+v(x_\varnothing)$（Eq.(21)）且唯一。只须验证 $K$ 也满足。作者在 $x_\varnothing=b$ 展开：
$$v(x_S)=\sum_{\pi_1=0}^\infty\cdots\sum_{\pi_n=0}^\infty\frac1{\prod_i\pi_i!}\left.\frac{\partial^{\pi_1+\cdots+\pi_n}v}{\partial x_1^{\pi_1}\cdots\partial x_n^{\pi_n}}\right|_{x=x_\varnothing}\prod_i((x_S)_i-b_i)^{\pi_i}.\tag{22}$$
对 $i\notin S$ 正次项为零，零次项为 $1$，故
$$v(x_S)=\sum_{\pi\in P_S}\frac1{\prod_i\pi_i!}\left.\frac{\partial^{\pi_1+\cdots+\pi_n}v}{\partial x_1^{\pi_1}\cdots\partial x_n^{\pi_n}}\right|_{x=x_\varnothing}\prod_{i\in S}(x_i-b_i)^{\pi_i},\quad P_S=\{\pi:\pi_i\in\mathbb N\ (i\in S),\pi_i=0\ (i\notin S)\}.\tag{23}$$
$P_S=\bigcup_{T\subseteq S}Q_T$ 是不交并，作者据此写
$$\begin{aligned}v(x_S)&=\sum_{T\subseteq S}\sum_{\pi\in Q_T}\frac1{\prod_i\pi_i!}\left.\frac{\partial^{\sum_i\pi_i}v}{\partial x_1^{\pi_1}\cdots\partial x_n^{\pi_n}}\right|_{x=x_\varnothing}\prod_{i\in T}(x_i-b_i)^{\pi_i}\\&=\sum_{\varnothing\ne T\subseteq S}\sum_{\pi\in Q_T}\frac1{\prod_i\pi_i!}\left.\frac{\partial^{\sum_i\pi_i}v}{\partial x_1^{\pi_1}\cdots\partial x_n^{\pi_n}}\right|_{x=x_\varnothing}\prod_{i\in T}(x_i-b_i)^{\pi_i}+v(x_\varnothing)\\&=\sum_{\varnothing\ne T\subseteq S}K(T\mid x)+v(x_\varnothing).\tag{24}\end{aligned}$$
作者由唯一性得到 $I(T\mid x)=K(T\mid x)$，Lemma 3 完成。'''
T['dyn-trigger-representation']=r'''作者定义（Eq.(25)）
$$f(x)=\sum_{T\subseteq N}w_TJ_T(x),\quad J_T(x)=\sum_{\pi\in Q_T}\frac1{\prod_i\pi_i!}\left.\frac{\partial^{\sum_i\pi_i}v}{\partial x_1^{\pi_1}\cdots\partial x_n^{\pi_n}}\right|_{x=x_\varnothing}\frac{\prod_{i\in T}(x_i-b_i)^{\pi_i}}{w_T},\quad w_T=I(T\mid x=\hat x),\quad w_\varnothing=v(\hat x_\varnothing),J_\varnothing=1.$$
作者对任意遮罩写完整链：
$$\begin{aligned}f(\hat x_S)&=\sum_{T\subseteq N}w_TJ_T(\hat x_S)\tag{26}\\&=\sum_{T\subseteq N}\sum_{\pi\in Q_T}\frac1{\prod_i\pi_i!}\left.\frac{\partial^{\sum_i\pi_i}v}{\partial x_1^{\pi_1}\cdots\partial x_n^{\pi_n}}\right|_{x=x_\varnothing}\prod_{i\in T}((\hat x_S)_i-b_i)^{\pi_i}\tag{27}\\&=\sum_{T\subseteq S}\sum_{\pi\in Q_T}\frac1{\prod_i\pi_i!}\left.\frac{\partial^{\sum_i\pi_i}v}{\partial x_1^{\pi_1}\cdots\partial x_n^{\pi_n}}\right|_{x=x_\varnothing}\prod_{i\in T}((\hat x_S)_i-b_i)^{\pi_i}\tag{28}\\&=\sum_{\varnothing\ne T\subseteq S}\sum_{\pi\in Q_T}\frac1{\prod_i\pi_i!}\left.\frac{\partial^{\sum_i\pi_i}v}{\partial x_1^{\pi_1}\cdots\partial x_n^{\pi_n}}\right|_{x=x_\varnothing}\prod_{i\in T}(\hat x_i-b_i)^{\pi_i}+v(x_\varnothing)\tag{29}\\&=\sum_{\varnothing\ne T\subseteq S}I(T\mid x=\hat x)+v(x_\varnothing)\tag{30}\\&=v(\hat x_S).\tag{31}\end{aligned}$$
Eq.(27) 注释为 “$w_T$ cancels out”；Eq.(28) 用被遮罩坐标的正次幂为零，Eq.(30) 用 Lemma 3 逆向，最后用 universal matching。作者据此说明 Eq.(6)/(7) 中权重即交互。'''
T['dyn-noisy-output']=r'''作者定义噪声输出 $\widetilde v(x_S)=v(x_S)+\Delta v_S$（Eq.(32)）并展开：
$$\begin{aligned}\widetilde I(T\mid x)&=\sum_{S\subseteq T}(-1)^{|T|-|S|}\widetilde v(x_S)\tag{33}\\&=\sum_{S\subseteq T}(-1)^{|T|-|S|}(v(x_S)+\Delta v_S)\tag{34}\\&=\sum_{S\subseteq T}(-1)^{|T|-|S|}v(x_S)+\sum_{S\subseteq T}(-1)^{|T|-|S|}\Delta v_S\tag{35}\\&=I(T\mid x)+\sum_{S\subseteq T}(-1)^{|T|-|S|}\Delta v_S\tag{36}\\&=I(T\mid x)+\Delta I_T.\tag{37}\end{aligned}$$
无噪声部分不是随机变量。作者此时称每个 $\Delta v_S\sim\mathcal N(0,\sigma^2)$ 是独立同分布，故
$$E[\Delta I_T]=\sum_{S\subseteq T}(-1)^{|T|-|S|}E[\Delta v_S]=0,$$
$$\operatorname{Var}[\Delta I_T]=\operatorname{Var}\left(\sum_{S\subseteq T}(-1)^{|T|-|S|}\Delta v_S\right)\tag{38}=\sum_{j=1}^{2^{|T|}}\operatorname{Var}[\Delta v_{S_j}]\tag{39}=2^{|T|}\sigma^2,\tag{40}$$
因为 $T$ 有 $2^{|T|}$ 个子集。最后按 Eq.(19) 把 $\widetilde I$ 与 $\widetilde J_T$ 的比例设为 $w_T$，取 $\epsilon_T=\Delta I_T/w_T$，得到 $E[\epsilon_T]=0$ 与 $\operatorname{Var}[\epsilon_T]\propto 2^{|T|}\sigma^2$。原正文未声明的独立条件、零分母与实际比例系数均保留待另核。'''
T['dyn-regression']=r'''作者把 $2^n$ 行触发向量排成 $J$，噪声排成 $E=[\epsilon^{(1)},\ldots,\epsilon^{(2^n)}]^\top$，标签排成 $y$。原式链：
$$\begin{aligned}\hat w&=\arg\min_w\widetilde L(w)\tag{41}\\\widetilde L(w)&=E_\epsilon E_{S\subseteq N}(y_S-w^\top(J(x_S)+\epsilon))^2\tag{42}\\&=E_E\left[2^{-n}\|y-(J+E)w\|_2^2\right]\tag{43}\\&=2^{-n}E_E[(y-(J+E)w)^\top(y-(J+E)w)]\tag{44}\\&=2^{-n}\{y^\top y-2y^\top E_E[J+E]w+w^\top E_E[(J+E)^\top(J+E)]w\}.\tag{45}\end{aligned}$$
作者求导（原 Eq.(46) 漏了公共 $2^{-n}$ 因子，不影响驻点）：
$$\partial\widetilde L/\partial w=-2E_E[(J+E)^\top]y+2E_E[(J+E)^\top(J+E)]w=0.\tag{46}$$
因此
$$\begin{aligned}E_E[(J+E)^\top(J+E)]w&=E_E[(J+E)^\top]y\tag{47}\\(J^\top J+E_E[E^\top J]+J^\top E_E[E]+E_E[E^\top E])w&=J^\top y\tag{48}\\(J^\top J+E_E[E^\top E])w&=J^\top y.\tag{49}\end{aligned}$$
作者说当 $m=2^n$ 很大时样本协方差 $m^{-1}E^\top E$ 收敛到真实 $\operatorname{Cov}(E)$，据此写 $E_E[E^\top E]=E_E[2^n\operatorname{Cov}(E)]=2^n\operatorname{diag}(c)$；不同交互噪声独立使协方差对角，$c_T=2^{|T|}\sigma^2$。得到
$$(J^\top J+2^n\operatorname{diag}(c))w=J^\top y.\tag{50}$$
作者分四步论证可逆：(1) $u^\top J^\top Ju=\|Ju\|_2^2\ge0$；(2) 因 $J^\top J$ 对角元均正，原文写 $\prod_i\lambda_i=\prod_i(J^\top J)_{ii}>0$，所以全部特征值正；(3) $2^n\operatorname{diag}(c)$ 每项正，正定矩阵之和正定；(4) 正定矩阵无零特征值所以可逆。于是
$$\hat w=(J^\top J+2^n\operatorname{diag}(c))^{-1}J^\top y.\tag{51}$$
最后 $y(x_S)=v(x_\varnothing)+\sum_{\varnothing\ne T\subseteq S}w_T^*$，由 Lemma 2 与 $w_\varnothing^*=v(x_\varnothing)$ 得 $y(x_S)=J(x_S)^\top w^*$。作者随后原文写 $y=J^\top w^*$，并结尾写 $\hat w=(J^\top J+2^n\operatorname{diag}(c))^{-1}J^\top Jw^*=\hat Mw^*$。转置错式与对角元乘积错式保留。'''
T['dyn-binary-trigger']=r'''作者重述
$$J_T(x)=\sum_{\pi\in Q_T}\frac1{\prod_i\pi_i!}\left.\frac{\partial^{\sum_i\pi_i}v}{\partial x_1^{\pi_1}\cdots\partial x_n^{\pi_n}}\right|_{x=x_\varnothing}\frac{\prod_{i\in T}(x_i-b_i)^{\pi_i}}{w_T}.\tag{52}$$
$w_T=I(T\mid x=\hat x)$，$Q_T$ 的支持恰为 $T$。分两种情况。Case 1 $T\nsubseteq S$：取 $j\in T\setminus S$，$(\hat x_S)_j=b_j$ 且 $\pi_j>0$，故
$$\forall\pi\in Q_T,\quad\prod_{i\in T}((\hat x_S)_i-b_i)^{\pi_i}=0.\tag{53}$$
每项为零，作者得 $J_T(\hat x_S)=0$。Case 2 $T\subseteq S$：对 $i\in T$，$(\hat x_S)_i=\hat x_i$。Lemma 3 给
$$w_T=\sum_{\pi\in Q_T}\frac1{\prod_i\pi_i!}\left.\frac{\partial^{\sum_i\pi_i}v}{\partial x_1^{\pi_1}\cdots\partial x_n^{\pi_n}}\right|_{x=x_\varnothing}\prod_{i\in T}(\hat x_i-b_i)^{\pi_i}.\tag{54}$$
把 Eq.(52) 的遮罩输入展开（Eq.(55)），代入 $w_T$（Eq.(56)），然后替换保留坐标（Eq.(57)/(58)）：
$$J_T(\hat x_S)=\frac{\sum_{\pi\in Q_T}\frac1{\prod_i\pi_i!}\left.\frac{\partial^{\sum_i\pi_i}v}{\partial x_1^{\pi_1}\cdots\partial x_n^{\pi_n}}\right|_{x=x_\varnothing}\prod_{i\in T}(\hat x_i-b_i)^{\pi_i}}{\sum_{\pi\in Q_T}\frac1{\prod_i\pi_i!}\left.\frac{\partial^{\sum_i\pi_i}v}{\partial x_1^{\pi_1}\cdots\partial x_n^{\pi_n}}\right|_{x=x_\varnothing}\prod_{i\in T}(\hat x_i-b_i)^{\pi_i}}=1.\tag{59}$$
合并两情况，作者得 $J_T(\hat x_S)=\mathbf1_{T\subseteq S}$，并称对任意 DNN 和输入 $J$ 都固定二值。原式的零分母不删去。'''
T['dyn-equal-order']=r'''作者要证明同阶 $T,T'$ 的行向量互为排列。定义由变量排列诱导的对称变换 $\mathcal T(A)=P_k\cdots P_1AP_1\cdots P_k$，每个 $P_i$ 为排列矩阵。令 $B=J^\top J,D=2^n\operatorname{diag}(c)$，则
$$(J^\top J+2^n\operatorname{diag}(c))\hat M=J^\top J\tag{60},\qquad (B+D)\hat M=B.\tag{61}$$
Step 1：变量集 $N=\{1,\ldots,n\}$ 的排列作用于幂集的全部行列，例 $N=\{1,2,3\}$、交换 $1,3$，$[\varnothing,\{1\},\{2\},\{3\},\{1,2\},\{1,3\},\{2,3\},N]$ 变成 $[\varnothing,\{3\},\{2\},\{1\},\{3,2\},\{3,1\},\{2,1\},N]$。包含关系保持，故 $\mathcal T(B)=B$；$D_{TT}=2^{|T|+n}\sigma^2$ 只依赖阶数，所以 $\mathcal T(B+D)=B+D$。
Step 2：作者写 $\mathcal T(B+D)\hat M=\mathcal T(B)$（Eq.(62)），即
$$P_k\cdots P_1(B+D)P_1\cdots P_k\hat M=P_k\cdots P_1BP_1\cdots P_k.\tag{63}$$
若 $\hat M$ 解此方程，则 $\mathcal T(\hat M)=P_k\cdots P_1\hat MP_1\cdots P_k$ 也解，因为 $P_i^2=I$。$B+D$ 可逆使解唯一，所以 $\mathcal T(\hat M)=\hat M$（Eq.(64)）。同阶集合可构造变量排列使 $T$ 映到 $T'$，故两行互为排列，Euclidean 范数相等。'''
T['dyn-zero-noise']=r'''作者由 Eq.(10) 直接写：当 $\sigma=0$，$\hat w=(J^\top J)^{-1}J^\top Jw^*=w^*$，所以 $\forall\varnothing\ne T\subseteq N,\hat w_T=w_T^*$。'''
T['product']=r'''原命题：若 $X_1,\ldots,X_k$ 相互独立，则
$$E[X_1\cdots X_k]=\prod_{i=1}^kE[X_i],\qquad\operatorname{Var}[X_1\cdots X_k]=\prod_{i=1}^k(E[X_i]^2+\operatorname{Var}[X_i])-\prod_{i=1}^kE[X_i]^2.$$
此处作者没有另立完整证明块，直接在后续计算中调用上述两个等式。'''
T['lowest']=r'''只保留最低次数 $\hat\pi_i=1$（$i\in S$），原 $J(S,\hat\pi\mid x')=\prod_{i\in S}\operatorname{sign}(x'_i-r_i)(x'_i-r_i)/\tau$。添加 $\epsilon\sim\mathcal N(0,\sigma^2I)$ 后，作者写
$$J(S,\hat\pi\mid x+\epsilon)=\prod_{i\in S}\left[\operatorname{sign}(x_i+\epsilon_i-r_i)\frac{x_i-r_i}{\tau}+\operatorname{sign}(x_i+\epsilon_i-r_i)\frac{\epsilon_i}{\tau}\right].$$
因为 $x_i-r_i\in\{-\tau,\tau\}$，作者忽略极小概率的大扰动（Difficulty 则写 $|\epsilon_i|\le\tau$），据此令 $\operatorname{sign}(x_i+\epsilon_i-r_i)=\operatorname{sign}(x_i-r_i)$，所以
$$J(S,\hat\pi\mid x+\epsilon)=\prod_{i\in S}\left(1+\operatorname{sign}(x_i-r_i)\frac{\epsilon_i}{\tau}\right).$$
每个括号服从 $\mathcal N(1,(\sigma/\tau)^2)$；调用独立乘积命题：
$$E[J]=\prod_{i\in S}1=1,\quad\operatorname{Var}[J]=\prod_{i\in S}(1^2+(\sigma/\tau)^2)-\prod_{i\in S}1^2=(1+(\sigma/\tau)^2)^{|S|}-1.$$
再由 $I=U_{S,\hat\pi}J$，作者写 $E[I]=U_{S,\hat\pi}$，$\operatorname{Var}[I]=U_{S,\hat\pi}^2((1+(\sigma/\tau)^2)^{|S|}-1)$。原近似替换与精确结论仍有区别。'''
T['general']=r'''由支持项定义
$$J(S,\pi\mid x')=\prod_{i\in S}\left(\operatorname{sign}(x'_i-r_i)\frac{x'_i-r_i}{\tau}\right)^{\pi_i}.$$
添加 Gaussian 扰动并展开每一因子：
$$J(S,\pi\mid x+\epsilon)=\prod_{i\in S}\left(\operatorname{sign}(x_i+\epsilon_i-r_i)\frac{x_i-r_i}{\tau}+\operatorname{sign}(x_i+\epsilon_i-r_i)\frac{\epsilon_i}{\tau}\right)^{\pi_i}.$$
作者以 $x_i-r_i\in\{-\tau,\tau\}$ 与小扰动忽略符号翻转，得到
$$J(S,\pi\mid x+\epsilon)=\prod_{i\in S}(1+\operatorname{sign}(x_i-r_i)\epsilon_i/\tau)^{\pi_i}.$$
取期望与方差后，由 $\epsilon_i$ 相互独立，作者写
$$\begin{aligned}E[J]&=\prod_{i\in S}E[(1+\operatorname{sign}(x_i-r_i)\epsilon_i/\tau)^{\pi_i}],\\\operatorname{Var}[J]&=\prod_{i\in S}E[(1+\operatorname{sign}(x_i-r_i)\epsilon_i/\tau)^{2\pi_i}]-\prod_{i\in S}E[(1+\operatorname{sign}(x_i-r_i)\epsilon_i/\tau)^{\pi_i}]^2.\end{aligned}$$
因为符号为 $\pm1$ 且 centered Gaussian 对称，$E[(1+\operatorname{sign}(x_i-r_i)\epsilon_i/\tau)^k]=E[(1+\epsilon_i/\tau)^k]$。于是
$$E[J]=\prod_{i\in S}E[(1+\epsilon_i/\tau)^{\pi_i}]=E\left[\prod_{i\in S}(1+\epsilon_i/\tau)^{\pi_i}\right],$$
$$\operatorname{Var}[J]=\prod_{i\in S}E[(1+\epsilon_i/\tau)^{2\pi_i}]-\prod_{i\in S}E[(1+\epsilon_i/\tau)^{\pi_i}]^2=\operatorname{Var}\left[\prod_{i\in S}(1+\epsilon_i/\tau)^{\pi_i}\right].$$'''
T['bnn-growth']=r'''令 $S\subsetneq S'$，共有坐标次数相同 $\pi'_i=\pi_i$。原命题给
$$\frac{\operatorname{Var}[J(S',\pi'\mid x+\epsilon)]}{\operatorname{Var}[J(S,\pi\mid x+\epsilon)]}>\prod_{i\in S'\setminus S}E[(1+\epsilon_i/\tau)^{\pi'_i}]^2\ge1,$$
$$\frac{E[J(S',\pi'\mid x+\epsilon)]/\operatorname{Var}[J(S',\pi'\mid x+\epsilon)]}{E[J(S,\pi\mid x+\epsilon)]/\operatorname{Var}[J(S,\pi\mid x+\epsilon)]}<\frac1{\prod_{i\in S'\setminus S}E[(1+\epsilon_i/\tau)^{\pi'_i}]}\le1.$$
由 Theorem 2.3 取 $A=\prod_{i\in S}(1+\epsilon_i/\tau)^{\pi_i}$、$B=\prod_{i\in S'\setminus S}(1+\epsilon_i/\tau)^{\pi'_i}$，相互独立。原 Eq.(40)：
$$\begin{aligned}\operatorname{Var}[AB]&=(E[A]^2+\operatorname{Var}[A])(E[B]^2+\operatorname{Var}[B])-E[A]^2E[B]^2\\&=\operatorname{Var}[A]\operatorname{Var}[B]+\operatorname{Var}[A]E[B]^2+\operatorname{Var}[B]E[A]^2\\&>\operatorname{Var}[A](\operatorname{Var}[B]+E[B]^2)\\&>\operatorname{Var}[A]E[B]^2.\end{aligned}$$
所以（Eq.(41)）$\operatorname{Var}[AB]/\operatorname{Var}[A]>E[B]^2+\operatorname{Var}[B]>E[B]^2=\prod_{i\in S'\setminus S}E[(1+\epsilon_i/\tau)^{\pi'_i}]^2$。其次作者在 Eq.(42) 把 $E[J(S',\pi')]=E[AB]$，Eq.(43) 写 $E[J(S,\pi)]=E[A]$，故 Eq.(44) 的均值比为 $E[B]$。得到 Eq.(45)：
$$\frac{E[J(S',\pi')]/\operatorname{Var}[J(S',\pi')]}{E[J(S,\pi)]/\operatorname{Var}[J(S,\pi)]}=\frac{E[B]}{\operatorname{Var}[AB]/\operatorname{Var}[A]}<\frac{E[B]}{E[B]^2}=\frac1{E[B]}=\frac1{\prod_{i\in S'\setminus S}E[(1+\epsilon_i/\tau)^{\pi'_i}]}.$$
最后引用 Gaussian 矩递推（Eq.(46)）：$E[\widetilde X^{k+1}]=\widetilde\mu E[\widetilde X^k]+k\widetilde\sigma^2E[\widetilde X^{k-1}]$。$X\sim\mathcal N(1,(\sigma/\tau)^2)$ 时变成 $E[X^{k+1}]=E[X^k]+k(\sigma/\tau)^2E[X^{k-1}]$。作者用归纳得到 $E[X^k]\ge E[X]=1$，结束证明。'''
T['bnn-regression']=r'''令 $p=|\Omega|$，$C=[C_{S_1},\ldots,C_{S_p}]^\top$、$U=[U_{S_1},\ldots,U_{S_p}]^\top$，各 $C$ 独立，$E[C]=\alpha$、$\operatorname{Cov}(C)=\operatorname{diag}(\beta_1^2,\ldots,\beta_p^2)$。Step 1，作者给 $U_{S_i}^*=\det(M_1,\ldots,M_{i-1},\rho,M_{i+1},\ldots,M_p)/\det M$（Eq.(48)），其中 $M=\alpha\alpha^\top+\operatorname{diag}(\beta^2)$、$\rho=y^*\alpha$。目标 $\min_U E[(y^*-U^\top C)^2]$（Eq.(49)），梯度链
$$\nabla_UL=E[2C(U^\top C-y^*)]=2E[CC^\top U-y^*C]=2E[CC^\top]U-2y^*E[C]=2(\alpha\alpha^\top+\operatorname{diag}(\beta^2))U-2y^*\alpha=0\tag{50}$$
给 $MU=y^*\alpha$（Eq.(51)），由 Cramer 法得到 Eq.(48)。Step 2，要证明
$$\frac{|U_{S_i}^*|}{|U_{S_j}^*|}=\frac{|\alpha_i/\beta_i^2|}{|\alpha_j/\beta_j^2|}.\tag{52}$$
原 Eq.(53) $M_j=\alpha_j\alpha+V_j$，$V_j$ 仅第 $j$ 坐标为 $\beta_j^2$。原 Eq.(54)/(55) 分别写两替换列的 determinant，除以 $|\det M|$。交换列只改变符号不改绝对值，故把 $M_j,\rho$ 放前两列，其余记 $M_{others}$，作者的 Eq.(56) 链：
$$\begin{aligned}|U_{S_i}^*|&=|1/\det M|\,|\det(M_j,\rho,M_{others})|\\&=|1/\det M|\,|\det(\alpha_j\alpha+V_j,y^*\alpha,M_{others})|\\&=|1/\det M|\,|\det(\alpha_j\alpha,y^*\alpha,M_{others})+\det(V_j,y^*\alpha,M_{others})|\\&=|1/\det M|\,|\det(V_j,y^*\alpha,M_{others})|\\&=|\alpha_i/\det M|\,|\det\begin{pmatrix}\beta_j^2&y^*\alpha_j&\alpha_j\alpha_{others}\\0&y^*&\alpha_{others}\\0&y^*\alpha_{others}&\alpha_{others}\alpha_{others}^\top+\operatorname{diag}(\beta_{others}^2)\end{pmatrix}|\\&=|\alpha_i\beta_j^2/\det M|\,|\det M'|,\end{aligned}$$
其中先把第 $j,i$ 行移到前两行，再从 $i$ 行抽出 $\alpha_i$；第一 determinant 的相关两列线性相关为零。原 Eq.(57) 为
$$M'=\begin{pmatrix}y^*&\alpha_{others}\\y^*\alpha_{others}&\alpha_{others}\alpha_{others}^\top+\operatorname{diag}(\beta_{others}^2)\end{pmatrix}.$$
对称地 $|U_{S_j}^*|=|\alpha_j\beta_i^2/\det M|\,|\det M'|$（Eq.(58)）。作者除两式得到 Eq.(52)，Step 3 随即给 $|U_S^*|\propto|E[C_S]/\operatorname{Var}[C_S]|$（Eq.(59)）。零行、零 determinant 或零方差并未在原文另外定义。'''
T['bnn-scaling']=r'''原 Theorem 2.6：$A_{min}=\min_S|U_S|$、$A_{max}=\max_S|U_S|$，则
$$A_{min}\frac{|E[I(S\mid x+\epsilon)]|}{\operatorname{Var}[I(S\mid x+\epsilon)]}\le\frac{|E[C_S(x+\epsilon)]|}{\operatorname{Var}[C_S(x+\epsilon)]}\le A_{max}\frac{|E[I(S\mid x+\epsilon)]|}{\operatorname{Var}[I(S\mid x+\epsilon)]}.\tag{60}$$
由原 Eq.(12)，$I(S\mid x')=U_SC_S(x')$，所以 $|E[I]|=|U_S||E[C_S]|$、$\operatorname{Var}[I]=U_S^2\operatorname{Var}[C_S]$。作者得 $|E[C_S]|/\operatorname{Var}[C_S]=|U_S|\,|E[I]|/\operatorname{Var}[I]$。把 $|U_S|$ 夹在 $A_{min},A_{max}$ 之间即得到两个不等式。'''
T['diff-binary']=r'''重述 Eq.(19)：$\forall T\subseteq N,C(S\mid x_T)=\prod_{i\in S}A_i(x_T)=\mathbf1_{S\subseteq T}$。作者给 Eq.(20)
$$C_S(x')=\sum_{\pi\in Q_S}U_{S,\pi}J(S,\pi\mid x')/U_S,\quad J(S,\pi\mid x')=\prod_{i\in S}\left(\operatorname{sign}(x'_i-b_i)\frac{x'_i-b_i}{\tau}\right)^{\pi_i}.$$
Case 1 原文写 “$S\subsetneq T$”，接着却写 “there exists some $j\in S\setminus T$”；因 $j\notin T$ 有 $(x_T)_j-b_j=0$，所以 $\forall\pi\in Q_S,J(S,\pi\mid x_T)=0$（Eq.(21)），由此 $C_S(x_T)=0$。Case 2 $S\subseteq T$：每个 $i\in S$ 保留，$(x_T)_i-b_i\in\{\tau,-\tau\}$，所以 $\operatorname{sign}((x_T)_i-b_i)((x_T)_i-b_i)/\tau=1$，$J(S,\pi\mid x_T)=1$（Eq.(22)）。得到 $C_S(x_T)=\sum_{\pi\in Q_S}U_{S,\pi}/U_S$（Eq.(23)）。由于原样本所有这些因子也为 $1$，$U_S=I(S\mid x)=\sum_{\pi\in Q_S}U_{S,\pi}$（Eq.(24)）；除法得到 $C_S(x_T)=1$。合并两种情况即完成。原 Case 1 的错误包含关系和分母边界保留。'''
T['diff-multiorder']=r'''作者定义 $I^{(m)}(i,j)=E_{S\subseteq N\setminus\{i,j\},|S|=m}[\Delta v(i,j,S)]$（Eq.(25)），$\Delta v(i,j,S)=v(x_{S\cup\{i,j\}})-v(x_{S\cup\{i\}})-v(x_{S\cup\{j\}})+v(x_S)$。更一般 $\Delta v_T(S)=\sum_{L\subseteq T}(-1)^{|T|-|L|}v(x_{L\cup S})$；引用 $\Delta v_T(S)=\sum_{S'\subseteq S}I(T\cup S')$。作者完整链（原错误保留）：
$$\begin{aligned}I^{(m)}(i,j)&=E_{S\subseteq N\setminus\{i,j\},|S|=m}\left[\sum_{L\subseteq S}I(L\cup\{i,j\})\right]\\&=\frac1{\binom{n-2}{m}}\sum_{\substack{S\subseteq N\setminus\{i,j\}\\|S|=m}}\sum_{L\subseteq S}I(L\cup\{i,j\})\\&=\sum_{\substack{L\subseteq N\setminus\{i,j\}\\|L|\le m}}I(L\cup\{i,j\})\sum_{\substack{L\subseteq S\subseteq N\setminus\{i,j\}\\|S|=m}}\frac1{\binom{n-2}{m}}\\&=\sum_{\substack{L\subseteq N\setminus\{i,j\}\\|L|\le m}}I(L\cup\{i,j\})\frac{\binom{n-2}{m-l}}{\binom{n-2}{m}}\\&=\sum_{l=0}^m\sum_{\substack{L\subseteq N\setminus\{i,j\}\\|L|=m}}\frac{\binom{n-2}{m-l}}{\binom{n-2}{m}}I(L\cup\{i,j\}).\end{aligned}$$
作者在末句重复最后等式。原分子 $n-2$ 与最后内层 $|L|=m$ 是需要独立审查的原式，不能在转录中直接换成正确系数。'''
T['diff-regression']=r'''作者把每个概念触发值记作 $f_i$、权重记作 $w_i$，近似输出 $y=w^\top f=\sum_{i=1}^dw_if_i$。$w_i\approx0$ 表示没有学该概念。作者设训练样本 $f\sim P(f)=\mathcal N(\mu,\Sigma^2)$，$\mu=[\mu_i]^\top$，原文又写 $\Sigma=\operatorname{diag}(\sigma_1^2,\ldots,\sigma_d^2)$，$y^*$ 为标签。目标
$$L=E_{P(f)}[\tfrac12(w^\top f-y^*)^2].\tag{26}$$
Step 1 给 $w_i=\det(K_1,\ldots,K_{i-1},\zeta,K_{i+1},\ldots,K_d)/\det K$（Eq.(27)），$K=\mu\mu^\top+\Sigma^2$、$\zeta=y^*\mu$。Step 2 声称 $|w_i|/|w_j|=|\mu_i/\sigma_i^2|/|\mu_j/\sigma_j^2|$（Eq.(28)）。Step 3 据此称 $|w_i|\propto|1/\sigma_i^2|$，于是高方差高阶概念更难学。此节没有给 Step 1 与 Step 2 的中间证明；$\Sigma$ 与 $\Sigma^2$ 的原符号和 Step 3 省略均值条件均保留。'''
T['dyn-universal']=r'''F.1 分三部分。第一部分 AND：$v_{and}(x_\varnothing)=v(x_\varnothing)$，$I_{and}(T\mid x)=\sum_{L\subseteq T}(-1)^{|T|-|L|}v_{and}(x_L)$。作者交换 $L\subseteq T\subseteq S$ 的有限求和，按 $L$ 分为 $L=S,L=\varnothing,\varnothing\ne L\subsetneq S$：
$$\begin{aligned}\sum_{\varnothing\ne T\subseteq S}I_{and}(T\mid x)&=\sum_{L\subseteq S}\sum_{\varnothing\ne T\subseteq S,T\supseteq L}(-1)^{|T|-|L|}v_{and}(x_L)\\&=v_{and}(x_S)+\left[\sum_{k=1}^{|S|}\binom{|S|}{k}(-1)^k\right]v_{and}(x_\varnothing)+\sum_{\varnothing\ne L\subsetneq S}\left[\sum_{k=0}^{|S|-|L|}\binom{|S|-|L|}{k}(-1)^k\right]v_{and}(x_L)\\&=v_{and}(x_S)-v_{and}(x_\varnothing).\tag{17}\end{aligned}$$
故 $v_{and}(x_S)=v(x_\varnothing)+\sum_{\varnothing\ne T\subseteq S}I_{and}(T\mid x)$。第二部分 OR：$v_{or}(x_\varnothing)=0$。由定义 $I_{or}(T\mid x)=-\sum_{L\subseteq T}(-1)^{|T|-|L|}v_{or}(x_{N\setminus L})$，作者写
$$\sum_{T:T\cap S\ne\varnothing}I_{or}(T\mid x)=-\sum_{L\subseteq N}\left[\sum_{T\supseteq L,T\cap S\ne\varnothing}(-1)^{|T|-|L|}\right]v_{or}(x_{N\setminus L}).$$
$L=N$ 系数为 $-1$；$L=N\setminus S$ 的内和为 $\sum_{k=1}^{|S|}\binom{|S|}{k}(-1)^k=-1$。其他 $L$ 的作者完整分组为：若 $L\cap S\ne\varnothing,L\ne N$，内和是
$$\sum_{T'\subseteq N\setminus(S\cup L)}\sum_{k=0}^{|S|-|S\cap L|}\binom{|S|-|S\cap L|}{k}(-1)^{|T'|+k};$$
若 $L\cap S=\varnothing,L\ne N\setminus S$，作者原式写内和
$$\sum_{T'\subseteq N\setminus(S\cup L)}\sum_{k=0}^{|S|}\binom{|S|}{k}(-1)^{|T'|+k}.$$
据此作者把其余两组记为零，得到
$$\sum_{T:T\cap S\ne\varnothing}I_{or}(T\mid x)=-(-1)v_{or}(x_S)-v_{or}(x_\varnothing)=v_{or}(x_S).\tag{18}$$
第三部分，把 AND 和 OR 两式相加，$v=v_{and}+v_{or}$，得到 Theorem 2。对 $S=\varnothing$，直接用规定的分量基线。原 OR 第二分组从 $k=0$ 开始的式子仍保留；项目给独立消去证明。'''
