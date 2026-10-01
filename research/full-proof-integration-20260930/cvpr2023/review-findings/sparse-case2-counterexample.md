# Sparse 第8页 Case 2 推断的独立反例

复核对象是正式 PDF 第8页 Case 2 的句子：“However, \(R^{(k)}\) is still much less than \(\binom nk\) if \(|\eta^{(k)}|\) is not exponentially small.” 原页没有附加“大 \(k\)”的条件。本反例只针对这一推断，不否定 Theorem 2 的系数存在式或 Theorem 3 的精确阈值计数不等式，也不把相邻的 “in most cases” 描述改作全称命题。

沿用问题 ID sparse-issue-asymptotic-sparsity，不新增同义问题或改变原命题。根代理已独立核过原第8页及以下平均公式。证明修复授权为 proof_only_granted，命题修改授权为 not_granted。

取任意 \(j\in\mathbb N\)，令 \(n=4j+3\)、\(N=\{1,\ldots,n\}\)、\(q=\binom n2=n(n-1)/2=(4j+3)(2j+1)\)。因此 \(n\ge3\)、\(q\) 为奇数，\(q\) 个二元集合可以划分为正系数族 \(P\) 和负系数族 \(Q\)，满足 \(|P|=(q-1)/2\)、\(|Q|=(q+1)/2\)。对每个二元集合 \(A\)，定义 \(c_A=1\)（\(A\in P\)）与 \(c_A=-1\)（\(A\in Q\)）；于是 \(\sum_{|A|=2}c_A=-1\)。

固定输入 \(x=(1,\ldots,1)\)、输入基线 \(r=0\)，取同一个模型

\[
v(z)=\sum_{i=1}^n z_i+\sum_{\substack{A\subseteq N\\|A|=2}}c_A\prod_{i\in A}z_i.
\]

这是光滑的二次多项式，\(v(r)=0\)。令 \(g_0(S)=v(x_S)\)。纯AND单项式的有限 Möbius 变换与线性性给出 \(I(\{i\})=1\)、\(I(A)=c_A\)（\(|A|=2\)），其余交互均为0。因此 \(A^{(1)}=n\)、\(A^{(2)}=-1\)。

原 Assumption 1-α 在 \(M=2<n\) 时成立。所有总阶至少3的混合偏导在全空间恒零，故原更强的 Assumption 1-β 也成立。按原均匀 \(m\) 元掩码平均定义，对 \(0\le m\le n\)，

\[
\mu_m=\bar u^{(m)}=m-\frac{\binom m2}{q}.
\]

对 \(0\le m<n\)，\(\mu_{m+1}-\mu_m=1-m/q\ge1-2/n>0\)，所以原 Assumption 2 成立。对 \(m\ge1\)，\(\mu_m/m=1-(m-1)/(2q)\) 随 \(m\) 非增。因此任意 \(1\le m'\le m\le n\) 都有 \(\mu_{m'}\ge(m'/m)\mu_m\)；\(m'=0\) 时两边为0。原 Assumption 3 因而以固定 \(p=1\) 成立。

取固定足够小阈值 \(\tau=1/100\)。所有二阶交互的绝对值都是1，所以

\[
R^{(2)}=q=\binom n2,\qquad B_2=\sum_{|A|=2}|I(A)|=q,\qquad \eta^{(2)}=\frac{-1}{q}.
\]

\(|\eta^{(2)}|=2/[n(n-1)]\) 只按多项式衰减，并非指数小；它相对 \(1/n\) 趋于0，确实落在作者的近乎抵消 Case 2。每个二元 \(A\) 的四个 \(u(L)\) 值是 \(0,1,1,2+c_A\)，故 \(\mathbb E_{L\subseteq A}|u(L)|\) 为 \(3/4\) 或 \(5/4\)；上述阈值也符合原“足够小”的定性要求。但是显著二阶交互占全部潜在二阶交互的比例恒为1，不能称为 “much less”。

Theorem 3 的精确界仍然成立：右边在代入相同总效应后为 \(|A^{(2)}|/(\tau|\eta^{(2)}|)=100q\)，而 \(R^{(2)}=q\le100q\)。反例揭示的是从这个上界跳到稀疏比较的额外推断，不是精确界本身。

若要求具体DNN实现，同一掩码顶点游戏还由单隐层ReLU模型
\[
v_{\rm ReLU}(z)=\sum_i\operatorname{ReLU}(z_i)
 +\sum_{i<j}c_{\{i,j\}}\operatorname{ReLU}(z_i+z_j-1)
\]
精确实现，因为在0/1顶点第二项恰是 \(z_i z_j\)。它满足本论后续所需的1-α、2、3；不能据此声称ReLU函数满足全空间经典1-β。前述光滑二次模型可由平方激活的有限网络表示，使用 \(z_i z_j=((z_i+z_j)^2-(z_i-z_j)^2)/4\)，并确实满足更强的1-β。两种全空间函数各自范围区分，不把顶点一致误当全空间可微性质一致。

正式来源：research/paper-survey-20260930/recent/pdf/iclr2024-sparse.pdf，第8页；页图 research/full-proof-integration-20260930/iclr2024-sparse/evidence/pages/page-08.png。本文件为项目独立核算，不是原作者证明或新增 Lean 通过声明。
