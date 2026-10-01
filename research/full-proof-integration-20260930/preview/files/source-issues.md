# 原文数学问题与修正记录

原式和来源保留；证明错误与命题错误分别登记。此文件由当前全篇输入生成。

## Dummy 原陈述包括空集，结论错误

记录 ID：cvpr-issue-dummy-empty



\[\forall S\subseteq N\setminus\{i\},\;v(x_{S\cup\{i\}})=v(x_S)+v(x_{\{i\}})\ \Longrightarrow\ \forall S\subseteq N\setminus\{i\},\;w_{S\cup\{i\}}=0\]

取 $N=\{i\}$，$v(x_\varnothing)=0$、$v(x_{\{i\}})=1$。原前提只有 $S=\varnothing$ 一个实例，$1=0+1$ 成立。按原定义 $w_{\{i\}}=1-0=1\ne0$。第4页末把 $\sum_{S^{\prime}\subseteq S}(-1)^{|S|-|S^{\prime}|}$ 统一写为0，在 $S=\varnothing$ 时实际为1。PDF图像 supp-04.png 可逐式复核。

只否定原 Dummy 陈述的全部量词版本。其他性质与Theorem1–5不依赖该错误。不能添加S非空条件或删去单变量结论后称原命题证明完成。

来源：src-cvpr2023-supplement PDF 2, src-cvpr2023-supplement PDF 4

## Linearity 原证明把求和内输出索引印为固定 S

记录 ID：cvpr-issue-linearity-index



\[w^v_S=\sum_{S^{\prime}\subseteq S}(-1)^{|S|-|S^{\prime}|}v(x_S)\]

内层应随求和变量变化，但原式固定为 $x_S$。取 $S=\{i\}$、$v(x_\varnothing)=0$、$v(x_{\{i\}})=1$，原显示右侧为 $-1+1=0$，按原定义左侧为1。原稿随后t,u输出亦相同索引。原陈述的线性性没有改变；修正证明直接逐项使用 $g_v(U)=g_t(U)+g_u(U)$。

错误限于原证明显示式，线性性原命题可按现有公共interaction_add忠实证明。

来源：src-cvpr2023-supplement PDF 4

## Theorem2–4 的 Beta 定义排印与零参数边界

记录 ID：cvpr-issue-beta-proof



\[B(p,q)=\int_0^1x^{p-1}(1-x)^{1-q}\,dx;\quad B(|N|-|L|-k,|L|+k);\quad \int_0^1|L|(1-x)^{|L|-1}\,dx=1\]

第7页(ii)明示 $p,q>0$ 却将指数写为 $1-q$。取 $(p,q)=(1,2)$，其积分发散，后续有限阶乘公式不匹配。同页 $L=\varnothing,k=0$ 是求和允许项，却调用 $B(|N|,0)$，超出正参数定义；①在 $|L|=0$ 时被积函数在开区间上为零，统一写成1不成立。Theorem3第9页和Theorem4第10–11页复用这一路线，故归并为同一issue。另极端剩余集合为空时②的重编号上界成为负数，须明确空和，而原文未单独处理。

原Shapley、SII、STI结论未发现反例。保持同一命题的全部允许集合，使用有限阶乘卷积给完整证明，含L空集与剩余集合为空，避免修补原积分域而改变目标。

来源：src-cvpr2023-supplement PDF 7, src-cvpr2023-supplement PDF 8, src-cvpr2023-supplement PDF 9, src-cvpr2023-supplement PDF 10, src-cvpr2023-supplement PDF 11

## 纯AND分布证明的三个case没有覆盖不可比集合

记录 ID：cvpr-issue-distribution-incomparable



\[S\subsetneq T;\quad S=T;\quad S\supsetneq T\]

原目标量化全部 $S\subseteq N$，但原证明只写上述三类。例 $N=\{1,2\}$、$T=\{1\}$、$S=\{2\}$ 落在三类之外。目标 $w_S=0$ 在此仍真，因为没有 $U\subseteq S$ 包含T。修正证明以 $T\not\subseteq S$、$S=T$、$T\subsetneq S$ 分组（不改原陈述），也可直接复用已编译的interaction_unanimity。

原目标正确，原证明缺case。Add-Mul推导复用这个目标，保留同一原命题并完成修证明。

来源：src-cvpr2023-supplement PDF 5, src-cvpr2023-supplement PDF 6

## 选择集合大小与非零系数个数不总相等

记录 ID：cvpr-issue-l0-support



\[\|\boldsymbol w_\Omega\|_0=|\Omega|\]

第4页定义 $w^{\prime}_S=w_S$ 若 $S\in\Omega$，否则为0。若 $S\in\Omega$ 而 $w_S=0$，它贡献集合大小却不贡献L0范数；例如全零模型、$\Omega=\{\varnothing\}$ 给0与1。两类可行表示的最优值可能通过删除零项联系，但原逐项相等并无无条件证明。

这是算法段的原等式边界，不是编号定理；不静默把Omega定义改为support。目录保留原式和反例。

来源：src-cvpr2023-main PDF 4

## L0约束与固定罚参数目标的等价箭头未被证明

记录 ID：cvpr-issue-lagrange-equivalence



\[\min\mathrm{unfaith}\ \mathrm{s.t.}\|w_\Omega\|_0\le M\ \Longleftrightarrow\ \min\mathrm{unfaith}+\lambda\|w_\Omega\|_0\]

原Eq.(6)没有规定罚参数如何选取或证明离散非凸目标的强对偶。一般离散优化中，可行点 (support,error)=(0,3),(1,2),(2,0)，约束M=1选择中点，但任何lambda要选中点都需lambda≤1且lambda≥2，矛盾。本反例针对一般等价箭头，没有声称这一三点实例已由本文某个DNN产生。

只能按原文登记为启发式目标转换/松弛；不当作本篇已证明的数学等价。

来源：src-cvpr2023-main PDF 4

## 已解释比例在全部效应为零时未定义

记录 ID：cvpr-issue-ratio-zero-denominator



\[R_\Omega=\frac{\sum_{S\in\Omega}|w_S|}{\sum_{S\in\Omega}|w_S|+|\Delta|}\]

取 $v(x_S)=0$ 对所有S，得到全部 $w_S=0$、$\Delta=0$，分母为0。原文未给此边界约定。符号表把分母非零记录为表达式的定义域条件，不据此修改原论文命题或杜撰R值。

仅影响指标的零模型边界与符号域；重构/唯一性仍适用。

来源：src-cvpr2023-main PDF 5

## 基线变化也会改变截断的平方残差损失

记录 ID：cvpr-issue-baseline-truncated-loss



\[\text{change of baseline values always ensures unfaith}(w)=0\text{ and just affects }\|w_\Omega\|_1\]

原“just affects $\|w_\Omega\|_1$”不能解释为截断损失unfaith不随基线变。取单变量模型 $v(z)=z$、原输入x=1、输入基线r、只保留 $\Omega=\{\varnothing\}$。完整交互为 $w_\varnothing=r,w_{\{1\}}=1-r$；截断残差平方和为 $[r-r]^2+[1-r]^2=(1-r)^2$，随r变化。完整交互的unfaith始终0，但截断损失部分也可能改变。保留原句、单列该解释错误，不把原复合断言替换成较弱命题后算整体通过。

完整w各自重构的恒等式成立；不据此证明截断损失只变化L1。原复合句保留且分开状态。

来源：src-cvpr2023-main PDF 5

## Lemma3行列式消元漏余子式符号

记录 ID：sparse-issue-determinant-sign



\[D\prod_{k=1}^M\binom nk=1,\quad D=(\prod_{k=1}^M\binom nk)^{-1}\]

来源：src-iclr2024-sparse-main PDF 18

## Beta定义指数方向与后续值不一致

记录 ID：sparse-issue-beta-exponent



\[B(p,q)=\int_0^1x^{p-1}(1-x)^{1-q}\,dx\]

来源：src-iclr2024-sparse-main PDF 22

## Shapley等证明的L=∅零参数边界未处理

记录 ID：sparse-issue-beta-empty-L



\[B(n-|L|-k,|L|+k),\qquad |L|\int_0^1(1-x)^{|L|-1}\,dx=1\]

来源：src-iclr2024-sparse-main PDF 22, src-iclr2024-sparse-main PDF 23, src-iclr2024-sparse-main PDF 24, src-iclr2024-sparse-main PDF 26, src-iclr2024-sparse-main PDF 27

## Lemma1的一般无限Taylor恒等式缺少有效性前提

记录 ID：sparse-issue-taylor-validity



\[v(x_S)=\sum_{\kappa\in\mathbb N^n}\frac{D^\kappa v(b)}{\kappa!}(x_S-b)^\kappa\]

来源：src-iclr2024-sparse-main PDF 5, src-iclr2024-sparse-main PDF 15, src-iclr2024-sparse-main PDF 16

## Lemma1掩码幂式漏κ_i>0条件

记录 ID：sparse-issue-zero-power



\[\forall i\notin S,\ [(x_S)_i-b_i]^{\kappa_i}=0\]

来源：src-iclr2024-sparse-main PDF 16

## Theorem2原路线未处理ū(1)=0

记录 ID：sparse-issue-theorem2-zero-output



\[A^{(k)}/\bar u^{(1)}\]

来源：src-iclr2024-sparse-main PDF 19

## Theorem2原构造G可为空

记录 ID：sparse-issue-theorem2-empty-G



\[G=\{k:1\le k\le M,q^{(k)}\ge\lfloor p\rfloor\},\quad\delta=\max_{k\in G}\delta^{(k)}\]

来源：src-iclr2024-sparse-main PDF 19, src-iclr2024-sparse-main PDF 20

## Theorem2调用Lemma2的m范围不足

记录 ID：sparse-issue-theorem2-m0-range



\[m_0\in\{n,n-1,\ldots,n-M\},\qquad (40)\text{ only for }M\le m\le n\]

来源：src-iclr2024-sparse-main PDF 20

## p∈(0,1)时低位下标书写未定义

记录 ID：sparse-issue-theorem2-p-under-one



\[a_{\lfloor p\rfloor-1}^{(k)}n^{\lfloor p\rfloor-1}+\cdots+a_0^{(k)}\]

来源：src-iclr2024-sparse-main PDF 7, src-iclr2024-sparse-main PDF 19

## 完全抵消与空阶下η除法边界

记录 ID：sparse-issue-eta-zero



\[\eta^{(k)}=A^{(k)}/\sum_{|S|=k}|I(S)|,\quad A^{(k)}/\eta^{(k)}=\sum_{|S|=k}|I(S)|\]

来源：src-iclr2024-sparse-main PDF 7, src-iclr2024-sparse-main PDF 8, src-iclr2024-sparse-main PDF 20, src-iclr2024-sparse-main PDF 21

## fully random不足以推出2^|S|方差放大

记录 ID：sparse-issue-noise-variance



\[\operatorname{Var}(I_\varepsilon(S))=2^{|S|}\operatorname{Var}(\varepsilon)\]

来源：src-iclr2024-sparse-main PDF 8

## 奇偶例的u(∅)与中心化冲突

记录 ID：sparse-issue-parity-empty



\[u(S)=\begin{cases}+1&|S|\text{ odd}\\-1&|S|\text{ even}\end{cases}\]

来源：src-iclr2024-sparse-main PDF 9

## 单样本稀疏与重构不能推出样本间迁移

记录 ID：sparse-issue-transfer



\[\text{sparsity} + \text{universal matching}\Rightarrow\text{sample-wise transferability}\]

来源：src-iclr2024-sparse-main PDF 9

## D.2两个分量名称及去噪γ符号不一致

记录 ID：sparse-issue-decomposition-notation



\[u_{and}=0.5u+\gamma,\quad u_{and}=0.5u-\gamma;\qquad u_{and}=0.5(u-\varepsilon)+\gamma,\quad u_{or}=0.5(u-\varepsilon)+\gamma\]

来源：src-iclr2024-sparse-main PDF 29

## Case2非指数小抵消比例不足以推出同阶稀疏

记录 ID：sparse-issue-asymptotic-sparsity



\[\text{Case2: }|\eta^{(k)}|\text{ not exponentially small}\ \Longrightarrow\ R^{(k)}\text{ still much less than }\binom nk\]

来源：src-iclr2024-sparse-main PDF 7, src-iclr2024-sparse-main PDF 8

## Appendix H三阶表漏x3单变量项

记录 ID：sparse-issue-example-H-arithmetic



\[u(\{3,4,5\})=0,\qquad\bar u^{(3)}=1.8\]

来源：src-iclr2024-sparse-main PDF 34

## Theorem1换序后的第三行误用S⊇L

记录 ID：sparse-issue-reconstruction-index



\[\sum_{\substack{T\subseteq S:S\supseteq L\\|T|=t}}(-1)^{t-|L|}u(L)\]

来源：src-iclr2024-sparse-main PDF 15

## Lemma4按l分组后仍保留未绑定L

记录 ID：sparse-issue-marginal-free-L



\[\sum_{l=|K\setminus S|}^{|T|}(-1)^{|T|-|L|}\binom{|T|-|K\setminus S|}{l-|K\setminus S|}\]

来源：src-iclr2024-sparse-main PDF 21

## Theorem6临界阶换序后组合数误留自由S

记录 ID：sparse-issue-STI-free-S



\[\sum_{L\subseteq N\setminus T}I(T\cup L)\sum_{q=0}^{n-t}\frac{\binom{n-t-|L|}{q-|L|}}{\binom{n-1}{|S|}}\]

来源：src-iclr2024-sparse-main PDF 26

## T2参数域未在陈述中明确

记录 ID：sparse-issue-T2-parameter-domain



\[\lambda=\sum_{k=1}^M\frac{\binom{m_0}k}{\binom nk}\lambda^{(k)}\ne0,\qquad\log_n(\cdot)\]

来源：src-iclr2024-sparse-main PDF 5, src-iclr2024-sparse-main PDF 7, src-iclr2024-sparse-main PDF 17, src-iclr2024-sparse-main PDF 18, src-iclr2024-sparse-main PDF 19

## Lemma3 Eq33的降阶矩阵一行复制了n−2

记录 ID：sparse-issue-lemma3-copied-row



\[\left[\binom{n-3}0,\binom{n-2}1,\ldots,\binom{n-2}{M-2}\right]\]

来源：src-iclr2024-sparse-main PDF 18

## OR原证明的分类中间零和、条件输出代入及空掩码重合

记录 ID：issue-f11-or-intermediate-20260930



\[\sum_{S:S\cap T\ne\varnothing}I_{or}(S\mid x_T)=\sum_{S:S\cap T\ne\varnothing}\left[-\sum_{L\subseteq S}(-1)^{|S|-|L|}v_{or}(x_{N\setminus L})\right]\]

第13页该首代入式不保留二次掩码。取N={1,2}、T={1}、$g(A)=\mathbf1_{N\subseteq A}$、S=N。字面条件游戏hT全零，所以OR系数左0；原右−1。正确逐项输出是 $v_{or}((x_T)_{N\setminus L})=v_{or}(x_{T\setminus L})$。第14页case(3)以 $\sum_{j=0}^{|T|-|T\cap L|}\binom{|T|-|T\cap L|}j(-1)^j=0$ 作内层消去，但T子集L时上界0，和1；例如N={1,2},T=L={1}。完整外层仍能消去，但原标注内零不成立。case(4)激活要求在T新增至少一个变量，原下界印0，应分别核实际索引族；T空时case(1) L=N\T与case(2)L=N重合，不能重复计同一项。

错误属于原证明的中间分类和条件式代入；原OR及AND-OR父命题不变。修正证明使用相交子集族差及完整Möbius重构，包含T空，逐项保留literal conditioned sample。

来源：src-iclr2024-generalizable-main PDF 13, src-iclr2024-generalizable-main PDF 14

## Appendix D首句方差中心跨S与期望下标不一致

记录 ID：f11-issue-variance-expectation-indices



\[\mathbb E_{\varepsilon_T\sim N(0,\sigma^2)}[I′_{\rm and}(T)-\mathbb E_{\forall S,\varepsilon_S\sim N(0,\sigma^2)}I′_{\rm and}(S)]^2=2^{|T|}\sigma^2\]

来源：src-iclr2024-generalizable-main PDF 15

## Eq.(10)：行范数的逐点展开有反例

记录 ID：f11-issue-rowmax-signed-max

第6页定义每行的最大绝对值范数；第16页Eq.(10)逐点展开用了有符号最大值的绝对值。两者不是同一函数。这个问题仅针对展开中的子断言，不证明两个带min目标的最优值不同。

\[\operatorname{rowmax}(a,b)=\max(|a|,|b|),\qquad\text{Eq.(10) uses }|\max(a,b)|\]

\[a=-3,\ b=2:\qquad\max(|a|,|b|)=3\ne2=|\max(a,b)|\]

原式中的这一逐点恒等式已由项目反例声明实际编译。完整Eq.(10)含未绑定的索引，父优化等式的严格含义与最优值等价另列未判定。

可以判定行范数逐点展开错误；不能将此反例提升为对整个原min等式的反驳。原Eq.(6)定义与作者Eq.(10)均保留。

来源：src-iclr2024-generalizable-main PDF 6, src-iclr2024-generalizable-main PDF 16

## Eq.(10)：求和索引与父优化等式的作用域未明确

记录 ID：f11-issue-equation10-free-indices

作者外层求和绑定T_k，内层使用T⊆S以及|S|-|T|，但S没有在这份展开中绑定；部分输出和参数仍按T_k而非内层T索引。项目保留完整原式，未替作者选择一种修正后的解释。

\[\begin{aligned}
\mathrm{Loss}&=\min_{\{\gamma_{T_k}^{(1)},\gamma_{T_k}^{(2)}\}}(\|\operatorname{rowmax}(I_{\mathrm{and}})\|_1+\|\operatorname{rowmax}(I_{\mathrm{or}})\|_1)+\alpha(\|I_{\mathrm{and}}\|_1+\|I_{\mathrm{or}}\|_1)\\
&=\min_{\{\gamma_{T_k}^{(1)},\gamma_{T_k}^{(2)}\}}\sum_{T_k\subseteq N}\left|\max\left(\sum_{T\subseteq S}(-1)^{|S|-|T|}[0.5v^{(1)}(x_{T_k})+\gamma_{T_k}^{(1)}],\sum_{T\subseteq S}(-1)^{|S|-|T|}[0.5v^{(2)}(x_{T_k})+\gamma_{T_k}^{(2)}]\right)\right|\\
&\quad+\sum_{T_k\subseteq N}\left|\max\left(-\sum_{T\subseteq S}(-1)^{|S|-|T|}[0.5v^{(1)}(x_{N\setminus T_k})-\gamma_{T_k}^{(1)}],-\sum_{T\subseteq S}(-1)^{|S|-|T|}[0.5v^{(2)}(x_{N\setminus T_k})-\gamma_{T_k}^{(2)}]\right)\right|\\
&\quad+\alpha\sum_{T_k\subseteq N}\sum_{i=1}^2\left|\sum_{T\subseteq S}(-1)^{|S|-|T|}[0.5v^{(i)}(x_{T_k})+\gamma_{T_k}^{(i)}]\right|\\
&\quad+\alpha\sum_{T_k\subseteq N}\sum_{i=1}^2\left|-\sum_{T\subseteq S}(-1)^{|S|-|T|}[0.5v^{(i)}(x_{N\setminus T_k})-\gamma_{T_k}^{(i)}]\right|.
\end{aligned}\]

请逐行对照正式PDF第16页：原Eq.(10)的min、求和范围、输出索引与自由S均在原文栏完整保留。已有(-3,2)反例只检验其中有符号max展开。

父min等式尚未判定。不得通过猜测索引、更改原陈述或根据逐点反例直接声称两种优化最优值不同。

来源：src-iclr2024-generalizable-main PDF 16

## Table7若沿用相邻概率输出尺度，则数值不相容；本节未说明尺度变化

记录 ID：cvpr-issue-bow-table7-probability-scale



\[v(x_S)=p(y=\text{positive sentiment}\mid x_S)\quad\text{(p17: In this example)},\qquad w_{\{\mathrm{smart}\}}=6.568,\quad w_{\{\mathrm{not},\mathrm{smart}\}}=-13.481\quad\text{(Table7)}\]

来源：src-cvpr2023-supplement PDF 17, src-cvpr2023-supplement PDF 18
