"""PDF 16--24: author-order TeX transcription. Chinese connecting prose is translation.
Project calculations, corrections and boundary arguments belong in rewritten steps.
"""
T={}
T['dyn-universal']=r'''F.1 分三部分。
(1) AND universal matching。作者要证 $\forall\varnothing\ne S\subseteq N,v_{and}(x_S)=\sum_{\varnothing\ne T\subseteq S}I_{and}(T\mid x)+v(x_\varnothing)$，并规定 $v_{and}(x_\varnothing)=v(x_\varnothing)$。按 Eq.(2)，$I_{and}(T\mid x)=\sum_{L\subseteq T}(-1)^{|T|-|L|}v_{and}(x_L)$。交换 $L\subseteq T\subseteq S$ 的求和顺序，固定L后先计算所有 $T\supseteq L$ 的线性组合，再对 $L\subseteq S$ 求和。作者分两类：(1) $L=S=T$ 的组合为 $(-1)^{|S|-|S|}v_{and}(x_L)=v_{and}(x_L)$；(2) $L\ne S$，令 $m=|T|-|L|$，$0\le m\le|S|-|L|$，对应T的个数为 $\binom{|S|-|L|}{m}$，所以
$$\sum_{T:L\subseteq T\subseteq S}(-1)^{|T|-|L|}v_{and}(x_L)=v_{and}(x_L)\sum_{m=0}^{|S|-|L|}\binom{|S|-|L|}{m}(-1)^m=0.$$
原完整链（Eq.17）：
$$\begin{aligned}
\sum_{\varnothing\ne T\subseteq S}I_{and}(T\mid x)
&=\sum_{\varnothing\ne T\subseteq S}\sum_{L\subseteq T}(-1)^{|T|-|L|}v_{and}(x_L)\\
&=\sum_{L\subseteq S}\sum_{T:L\subseteq T\subseteq S}(-1)^{|T|-|L|}v_{and}(x_L)-v_{and}(x_\varnothing)\\
&=v_{and}(x_S)+\sum_{L\subseteq S,L\ne S}v_{and}(x_L)\sum_{m=0}^{|S|-|L|}\binom{|S|-|L|}{m}(-1)^m-v_{and}(x_\varnothing)\\
&=v_{and}(x_S)-v_{and}(x_\varnothing)\\
&=v_{and}(x_S)-v(x_\varnothing).\tag{17}
\end{aligned}$$
故对每个非空S，$v_{and}(x_S)=\sum_{\varnothing\ne T\subseteq S}I_{and}(T\mid x)+v(x_\varnothing)$。
(2) OR universal matching。作者要证 $\forall S\subseteq N,v_{or}(x_S)=\sum_{T:T\cap S\ne\varnothing}I_{or}(S\mid x)$，并规定 $v_{or}(x_\varnothing)=0$。原此处和内仍写S。定义是 $I_{or}(T\mid x)=-\sum_{L\subseteq T}(-1)^{|T|-|L|}v_{or}(x_{N\setminus L})$。交换求和后固定L，计算 $\sum_{T:T\cap S\ne\varnothing,T\supseteq L}(-1)^{|T|-|L|}v_{or}(x_{N\setminus L})$，然后对L求和。作者分四类：
1. $L=N\setminus S$。此时 $T\ne L$；令 $|T^\prime|=|T|-|L|$，$1\le|T^\prime|\le|S|$。作者得到
$$\sum_{T:T\cap S\ne\varnothing,T\supseteq L}(-1)^{|T|-|L|}v_{or}(x_{N\setminus L})=v_{or}(x_S)\sum_{|T^\prime|=1}^{|S|}\binom{|S|}{|T^\prime|}(-1)^{|T^\prime|}=-v_{or}(x_S).$$
2. $L=N$，于是 $T=N$，组合为 $(-1)^{|N|-|N|}v_{or}(x_\varnothing)=v_{or}(x_\varnothing)$。
3. $L\cap S\ne\varnothing,L\ne N$。令 $T^\prime=\{i:i\in T,i\notin L,i\in N\setminus S\}$、$T^{\prime\prime}=\{i:i\in T,i\notin L,i\in S\}$，则 $|T|-|L|=|T^\prime|+|T^{\prime\prime}|$，$0\le|T^{\prime\prime}|\le|S|-|S\cap L|$。原组合写为
$$v_{or}(x_{N\setminus L})\sum_{T^\prime\subseteq N\setminus S\setminus L}\sum_{|T^{\prime\prime}|=0}^{|S|-|S\cap L|}\binom{|S|-|S\cap L|}{|T^{\prime\prime}|}(-1)^{|T^\prime|+|T^{\prime\prime}|}=0.$$
4. $L\cap S=\varnothing,L\ne N\setminus S$。令 $T^\prime=\{i:i\in T,i\notin L,i\in N\setminus S\}$、$T^{\prime\prime}=\{i:i\in T,i\in S\}$，原文取 $0\le|T^{\prime\prime}|\le|S|$，写
$$v_{or}(x_{N\setminus L})\sum_{T^\prime\subseteq N\setminus S\setminus L}\sum_{|T^{\prime\prime}|=0}^{|S|}\binom{|S|}{|T^{\prime\prime}|}(-1)^{|T^\prime|+|T^{\prime\prime}|}=0.$$
原完整链（Eq.18）：
$$\begin{aligned}
\sum_{T:T\cap S\ne\varnothing}I_{or}(T\mid x)
&=\sum_{T:T\cap S\ne\varnothing}\left[-\sum_{L\subseteq T}(-1)^{|T|-|L|}v_{or}(x_{N\setminus L})\right]\\
&=-\sum_{L\subseteq N}\sum_{T:T\cap S\ne\varnothing,T\supseteq L}(-1)^{|T|-|L|}v_{or}(x_{N\setminus L})\\
&=-\left[\sum_{|T^\prime|=1}^{|S|}\binom{|S|}{|T^\prime|}(-1)^{|T^\prime|}\right]v_{or}(x_S)-v_{or}(x_\varnothing)\\
&\quad-\sum_{L\cap S\ne\varnothing,L\ne N}\left[\sum_{T^\prime\subseteq N\setminus S\setminus L}\left(\sum_{|T^{\prime\prime}|=0}^{|S|-|S\cap L|}\binom{|S|-|S\cap L|}{|T^{\prime\prime}|}(-1)^{|T^\prime|+|T^{\prime\prime}|}\right)\right]v_{or}(x_{N\setminus L})\\
&\quad-\sum_{L\cap S=\varnothing,L\ne N\setminus S}\left[\sum_{T^\prime\subseteq N\setminus S\setminus L}\left(\sum_{|T^{\prime\prime}|=0}^{|S|}\binom{|S|}{|T^{\prime\prime}|}(-1)^{|T^\prime|+|T^{\prime\prime}|}\right)\right]v_{or}(x_{N\setminus L})\\
&=-(-1)v_{or}(x_S)-v_{or}(x_\varnothing)-\sum_{L\cap S\ne\varnothing,L\ne N}\left[\sum_{T^\prime\subseteq N\setminus S\setminus L}0\right]v_{or}(x_{N\setminus L})\\
&\quad-\sum_{L\cap S=\varnothing,L\ne N\setminus S}\left[\sum_{T^\prime\subseteq N\setminus S\setminus L}0\right]v_{or}(x_{N\setminus L})\\
&=v_{or}(x_S)-v_{or}(x_\varnothing)\\
&=v_{or}(x_S).\tag{18}
\end{aligned}$$
(3) 作者将AND与OR结论相加，$v(x_S)=v_{and}(x_S)+v_{or}(x_S)=v(x_\varnothing)+\sum_{\varnothing\ne T\subseteq S}I_{and}(T\mid x)+\sum_{T:T\cap S\ne\varnothing}I_{or}(T\mid x)$，得到AND-OR universal matching theorem。'''
T['dyn-taylor']=r'''Lemma 3（原Eq.19）：
$$I(T\mid x)=\sum_{\pi\in Q_T}\frac1{\prod_{i=1}^n\pi_i!}\left.\frac{\partial^{\pi_1+\cdots+\pi_n}v}{\partial x_1^{\pi_1}\cdots\partial x_n^{\pi_n}}\right|_{x=x_\varnothing}\prod_{i\in T}(x_i-b_i)^{\pi_i}.\tag{19}$$
其中 $Q_T=\{[\pi_1,\ldots,\pi_n]^\top:\forall i\in T,\pi_i\in\mathbb N^+;\forall i\notin T,\pi_i=0\}$。作者说明类似证明首先在[26]给出。
作者把Eq.19右端记为函数K，原文此句仍写“for S≠empty”：
$$K(T\mid x)\overset{def}=\sum_{\pi\in Q_T}\frac1{\prod_{i=1}^n\pi_i!}\left.\frac{\partial^{\pi_1+\cdots+\pi_n}v}{\partial x_1^{\pi_1}\cdots\partial x_n^{\pi_n}}\right|_{x=x_\varnothing}\prod_{i\in T}(x_i-b_i)^{\pi_i}.\tag{20}$$
作者引用[13,23]，AND交互是满足下式的唯一指标：
$$\forall S\subseteq N,\quad v(x_S)=\sum_{\varnothing\ne T\subseteq S}I(T\mid x)+v(x_\varnothing).\tag{21}$$
因此只需证明K也满足该性质。在 $x_\varnothing=b=[b_1,\ldots,b_n]^\top$ 展开任意遮罩输出：
$$\forall S\subseteq N,\quad v(x_S)=\sum_{\pi_1=0}^{\infty}\cdots\sum_{\pi_n=0}^{\infty}\frac1{\prod_{i=1}^n\pi_i!}\left.\frac{\partial^{\pi_1+\cdots+\pi_n}v}{\partial x_1^{\pi_1}\cdots\partial x_n^{\pi_n}}\right|_{x=x_\varnothing}\prod_{i=1}^n((x_S)_i-b_i)^{\pi_i}.\tag{22}$$
原b_i是遮罩输入xi的基线。遮罩规则给 $i\in S$ 时 $(x_S)_i=x_i$，$i\notin S$ 时 $(x_S)_i=b_i$；被遮罩正次因子为0，零次因子规定为1。故只保留 $P_S=\{[\pi_1,\ldots,\pi_n]^\top:\forall i\in S,\pi_i\in\mathbb N;\forall i\notin S,\pi_i=0\}$ 中的项：
$$\forall S\subseteq N,\quad v(x_S)=\sum_{\pi\in P_S}\frac1{\prod_{i=1}^n\pi_i!}\left.\frac{\partial^{\pi_1+\cdots+\pi_n}v}{\partial x_1^{\pi_1}\cdots\partial x_n^{\pi_n}}\right|_{x=x_\varnothing}\prod_{i\in S}(x_i-b_i)^{\pi_i}.\tag{23}$$
$P_S$ 分为不交集合 $\bigcup_{T\subseteq S}Q_T$，因此原Eq.24只有如下两行：
$$\begin{aligned}\forall S\subseteq N,\quad v(x_S)&=\sum_{T\subseteq S}\sum_{\pi\in Q_T}\frac1{\prod_{i=1}^n\pi_i!}\left.\frac{\partial^{\pi_1+\cdots+\pi_n}v}{\partial x_1^{\pi_1}\cdots\partial x_n^{\pi_n}}\right|_{x=x_\varnothing}\prod_{i\in T}(x_i-b_i)^{\pi_i}\\&=\sum_{\varnothing\ne T\subseteq S}K(T\mid x)+v(x_\varnothing).\tag{24}\end{aligned}$$
原注说明第二步按Eq.20；当 $T=\varnothing$ 时Q_T仅含全零指标，对应 $v(x_\varnothing)$。所以K满足Eq.21，作者得到 $I(T\mid x)=K(T\mid x)=\sum_{\pi\in Q_T}\frac1{\prod_{i=1}^n\pi_i!}\left.\frac{\partial^{\pi_1+\cdots+\pi_n}v}{\partial x_1^{\pi_1}\cdots\partial x_n^{\pi_n}}\right|_{x=x_\varnothing}\prod_{i\in T}(x_i-b_i)^{\pi_i}$。'''
T['dyn-trigger-representation']=r'''给定具体样本 $\hat x$，作者考虑Eq.6和7的函数：
$$f(x)=\sum_{T\subseteq N}w_TJ_T(x),\tag{25}$$
其中 $w_T=I(T\mid x=\hat x)$，$J_T(x)=\sum_{\pi\in Q_T}\frac1{\prod_{i=1}^n\pi_i!}\left.\frac{\partial^{\pi_1+\cdots+\pi_n}v}{\partial x_1^{\pi_1}\cdots\partial x_n^{\pi_n}}\right|_{x=x_\varnothing}\prod_{i\in T}(x_i-b_i)^{\pi_i}/w_T$。作者要证每个S都有 $f(\hat x_S)=v(\hat x_S)$。完整原链及原注编号：
$$\begin{aligned}
f(\hat x_S)&=\sum_{T\subseteq N}w_TJ_T(\hat x_S)\tag{26}\\
&=\sum_{T\subseteq N}\sum_{\pi\in Q_T}\frac1{\prod_{i=1}^n\pi_i!}\left.\frac{\partial^{\pi_1+\cdots+\pi_n}v}{\partial x_1^{\pi_1}\cdots\partial x_n^{\pi_n}}\right|_{x=x_\varnothing}\prod_{i\in T}((\hat x_S)_i-b_i)^{\pi_i}\tag{27}\\
&=\sum_{T\subseteq S}\sum_{\pi\in Q_T}\frac1{\prod_{i=1}^n\pi_i!}\left.\frac{\partial^{\pi_1+\cdots+\pi_n}v}{\partial x_1^{\pi_1}\cdots\partial x_n^{\pi_n}}\right|_{x=x_\varnothing}\prod_{i\in T}((\hat x_S)_i-b_i)^{\pi_i}\tag{28}\\
&=\sum_{T\subseteq S}\sum_{\pi\in Q_T}\frac1{\prod_{i=1}^n\pi_i!}\left.\frac{\partial^{\pi_1+\cdots+\pi_n}v}{\partial x_1^{\pi_1}\cdots\partial x_n^{\pi_n}}\right|_{x=x_\varnothing}\prod_{i\in T}(\hat x_i-b_i)^{\pi_i}\tag{30}\\
&=\sum_{\varnothing\ne T\subseteq S}I(T\mid x=\hat x)+v(x_\varnothing)\tag{32}\\
&=v(\hat x_S).\tag{33}
\end{aligned}$$
原Eq.27旁注是w_T约去。原编号29是文字注：若 $T\nsubseteq S$，存在 $j\in T\setminus S$ 使 $(\hat x_S)_j-b_j=0$，全项为0。原编号31也是文字注：当 $T\subseteq S$ 时每个 $i\in T$ 满足 $(\hat x_S)_i=\hat x_i$。Eq.32原注使用刚证明的Lemma3逆向，Eq.33使用universal matching逆向。
原Remark：f给universal matching Eq.3的连续实现；w_T是未遮罩样本的交互，J_T连续扩展AND指标，故称触发函数、其值称触发强度。'''
T['dyn-noisy-output']=r'''作者按Eq.2从全部遮罩分数提取 $\widetilde I(T\mid x)=\sum_{S\subseteq T}(-1)^{|T|-|S|}\widetilde v(x_S)$。因原假设 $\forall S\subseteq N,\widetilde v(x_S)=v(x_S)+\Delta v_S,\Delta v_S\sim\mathcal N(0,\sigma^2)$，展开为：
$$\begin{aligned}
\widetilde I(T\mid x)&=\sum_{S\subseteq T}(-1)^{|T|-|S|}\widetilde v(x_S)\tag{34}\\
&=\sum_{S\subseteq T}(-1)^{|T|-|S|}(v(x_S)+\Delta v_S)\tag{35}\\
&=\sum_{S\subseteq T}(-1)^{|T|-|S|}v(x_S)+\sum_{S\subseteq T}(-1)^{|T|-|S|}\Delta v_S\tag{36}\\
&=I(T\mid x)+\Delta I_T.\tag{37}
\end{aligned}$$
原I为无噪声非随机项，$\Delta I_T=\sum_{S\subseteq T}(-1)^{|T|-|S|}\Delta v_S$ 为噪声。作者此处称每个Gaussian噪声独立同分布，于是 $E\Delta I_T=\sum_{S\subseteq T}(-1)^{|T|-|S|}E\Delta v_S=0$，并计算
$$\begin{aligned}\operatorname{Var}\Delta I_T&=\operatorname{Var}\left(\sum_{S\subseteq T}(-1)^{|T|-|S|}\Delta v_S\right)\tag{38}\\&=\operatorname{Var}\Delta v_{S_1}+\operatorname{Var}\Delta v_{S_2}+\cdots+\operatorname{Var}\Delta v_{S_{2^{|T|}}}\tag{39}\\&=2^{|T|}\sigma^2.\tag{40}\end{aligned}$$
作者的理由为T有 $2^{|T|}$ 个子集。又按Eq.19交互解析式，作者称 $\widetilde I(T\mid x)$ 与 $\widetilde J_T(x)$ 的比为w_T；写 $\widetilde J_T=J_T+\epsilon_T$ 后噪声为 $\epsilon_T=\Delta I_T/w_T$，得到 $E\epsilon_T=0,\operatorname{Var}\epsilon_T\propto2^{|T|}\sigma^2$。'''
T['dyn-binary-trigger']=r'''作者按Eq.7给具体样本 $\hat x$ 的触发：
$$J_T(x)=\sum_{\pi\in Q_T}\frac1{\prod_{i=1}^n\pi_i!}\left.\frac{\partial^{\pi_1+\cdots+\pi_n}v}{\partial x_1^{\pi_1}\cdots\partial x_n^{\pi_n}}\right|_{x=x_\varnothing}\prod_{i\in T}(x_i-b_i)^{\pi_i}/w_T.\tag{52}$$
其中 $w_T=I(T\mid x=\hat x)$，$Q_T=\{[\pi_1,\ldots,\pi_n]^\top:\forall i\in T,\pi_i\in\mathbb N^+;\forall i\notin T,\pi_i=0\}$。作者要证遮罩样本满足 $J_T(\hat x_S)=\mathbf1(T\subseteq S)$，分两类。
Case 1：$T\nsubseteq S$，存在 $j\in T\setminus S$。遮罩使 $(\hat x_S)_j-b_j=0$，而 $j\in T$ 使 $\pi_j>0$，所以
$$\forall\pi\in Q_T,\quad\prod_{i\in T}((\hat x_S)_i-b_i)^{\pi_i}=0.\tag{53}$$
每项为0，所以 $J_T(\hat x_S)=0$。
Case 2：$T\subseteq S$，每个 $i\in T$ 也在S内，遮罩规则给 $(\hat x_S)_i=\hat x_i$。按F.2的Eq.19，
$$w_T=I(T\mid x=\hat x)=\sum_{\pi\in Q_T}\frac1{\prod_{i=1}^n\pi_i!}\left.\frac{\partial^{\pi_1+\cdots+\pi_n}v}{\partial x_1^{\pi_1}\cdots\partial x_n^{\pi_n}}\right|_{x=x_\varnothing}\prod_{i\in T}(\hat x_i-b_i)^{\pi_i}.\tag{54}$$
因此原完整链是
$$\begin{aligned}
J_T(\hat x_S)&=\sum_{\pi\in Q_T}\frac1{\prod_{i=1}^n\pi_i!}\left.\frac{\partial^{\pi_1+\cdots+\pi_n}v}{\partial x_1^{\pi_1}\cdots\partial x_n^{\pi_n}}\right|_{x=x_\varnothing}\prod_{i\in T}((\hat x_S)_i-b_i)^{\pi_i}/w_T\tag{55}\\
&=\frac{\displaystyle\sum_{\pi\in Q_T}\frac1{\prod_{i=1}^n\pi_i!}\left.\frac{\partial^{\pi_1+\cdots+\pi_n}v}{\partial x_1^{\pi_1}\cdots\partial x_n^{\pi_n}}\right|_{x=x_\varnothing}\prod_{i\in T}((\hat x_S)_i-b_i)^{\pi_i}}{\displaystyle\sum_{\pi\in Q_T}\frac1{\prod_{i=1}^n\pi_i!}\left.\frac{\partial^{\pi_1+\cdots+\pi_n}v}{\partial x_1^{\pi_1}\cdots\partial x_n^{\pi_n}}\right|_{x=x_\varnothing}\prod_{i\in T}(\hat x_i-b_i)^{\pi_i}}\tag{56}\\
&=\frac{\displaystyle\sum_{\pi\in Q_T}\frac1{\prod_{i=1}^n\pi_i!}\left.\frac{\partial^{\pi_1+\cdots+\pi_n}v}{\partial x_1^{\pi_1}\cdots\partial x_n^{\pi_n}}\right|_{x=x_\varnothing}\prod_{i\in T}(\hat x_i-b_i)^{\pi_i}}{\displaystyle\sum_{\pi\in Q_T}\frac1{\prod_{i=1}^n\pi_i!}\left.\frac{\partial^{\pi_1+\cdots+\pi_n}v}{\partial x_1^{\pi_1}\cdots\partial x_n^{\pi_n}}\right|_{x=x_\varnothing}\prod_{i\in T}(\hat x_i-b_i)^{\pi_i}}\tag{57}\\
&=1.\tag{59}
\end{aligned}$$
Eq.56原注按Eq.54；编号58是文字注：已证每个 $i\in T$ 有 $(\hat x_S)_i=\hat x_i$。合并两情况得到二值触发。作者据此称无论如何改变DNN或输入，$J=[\mathbf J(x_{S_1}),\ldots,\mathbf J(x_{S_{2^n}})]^\top\in\{0,1\}^{2^n\times2^n}$总是固定二值矩阵。'''
T['dyn-complement']=r'''Appendix E：OR可以在互换出现/遮罩状态后视为一类AND。给 $x\in\mathbb R^n$，$b\in\mathbb R^n$ 为输入遮罩基线，原坐标定义为
$$ (x_T)_i=\begin{cases}x_i&i\in T,\\b_i&i\in N\setminus T.\end{cases}\tag{12}$$
按该定义，AND是 $I_{and}(S\mid x)=\sum_{T\subseteq S}(-1)^{|S|-|T|}v_{and}(x_T)$，OR是 $I_{or}(S\mid x)=-\sum_{T\subseteq S}(-1)^{|S|-|T|}v_{or}(x_{N\setminus T})$。作者为简化分析假设 $v_{and}(\cdot)=v_{or}(\cdot)=0.5v(\cdot)$。互换出现与遮罩状态的样本定义为
$$ (\widetilde x_T)_i=\begin{cases}x_i&i\in N\setminus T,\\b_i&i\in T.\end{cases}\tag{13}$$
然后原链直接用裸v：
$$\begin{aligned}I_{or}(S\mid x)&=-\sum_{T\subseteq S}(-1)^{|S|-|T|}v(x_{N\setminus T})\tag{14}\\&=-\sum_{T\subseteq S}(-1)^{|S|-|T|}v(\widetilde x_T)\tag{15}\\&=-I_{and}(S\mid\widetilde x).\tag{16}\end{aligned}$$
作者最后称[27]的AND稀疏证明可扩展到OR，因此后续只分析AND即可。'''
