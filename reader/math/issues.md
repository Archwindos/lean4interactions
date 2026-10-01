# 原文数学问题与修正记录

原式和来源保留；证明错误与命题错误分别登记。此文件由当前全篇输入生成。

## Dummy 原陈述包括空集，结论错误

记录 ID：cvpr-issue-dummy-empty

取 $N=\{i\}$，$v(x_\varnothing)=0$、$v(x_{\{i\}})=1$。原前提只有 $S=\varnothing$ 一个实例，$1=0+1$ 成立。按原定义 $w_{\{i\}}=1-0=1\ne0$。第4页末把 $\sum_{S^{\prime}\subseteq S}(-1)^{|S|-|S^{\prime}|}$ 统一写为0，在 $S=\varnothing$ 时实际为1。PDF图像 supp-04.png 可逐式复核。

\[\forall S\subseteq N\setminus\{i\},\;v(x_{S\cup\{i\}})=v(x_S)+v(x_{\{i\}})\ \Longrightarrow\ \forall S\subseteq N\setminus\{i\},\;w_{S\cup\{i\}}=0\]

取 $N=\{i\}$，$v(x_\varnothing)=0$、$v(x_{\{i\}})=1$。原前提只有 $S=\varnothing$ 一个实例，$1=0+1$ 成立。按原定义 $w_{\{i\}}=1-0=1\ne0$。第4页末把 $\sum_{S^{\prime}\subseteq S}(-1)^{|S|-|S^{\prime}|}$ 统一写为0，在 $S=\varnothing$ 时实际为1。PDF图像 supp-04.png 可逐式复核。

只否定原 Dummy 陈述的全部量词版本。其他性质与Theorem1–5不依赖该错误。不能添加S非空条件或删去单变量结论后称原命题证明完成。

来源：src-cvpr2023-supplement PDF 2, src-cvpr2023-supplement PDF 4

## Linearity 原证明把求和内输出索引印为固定 S

记录 ID：cvpr-issue-linearity-index

内层应随求和变量变化，但原式固定为 $x_S$。取 $S=\{i\}$、$v(x_\varnothing)=0$、$v(x_{\{i\}})=1$，原显示右侧为 $-1+1=0$，按原定义左侧为1。原稿随后t,u输出亦相同索引。原陈述的线性性没有改变；修正证明直接逐项使用 $g_v(U)=g_t(U)+g_u(U)$。

\[w^v_S=\sum_{S^{\prime}\subseteq S}(-1)^{|S|-|S^{\prime}|}v(x_S)\]

内层应随求和变量变化，但原式固定为 $x_S$。取 $S=\{i\}$、$v(x_\varnothing)=0$、$v(x_{\{i\}})=1$，原显示右侧为 $-1+1=0$，按原定义左侧为1。原稿随后t,u输出亦相同索引。原陈述的线性性没有改变；修正证明直接逐项使用 $g_v(U)=g_t(U)+g_u(U)$。

错误限于原证明显示式，线性性原命题可按现有公共interaction_add忠实证明。

来源：src-cvpr2023-supplement PDF 4

## Theorem2–4 的 Beta 定义排印与零参数边界

记录 ID：cvpr-issue-beta-proof

第7页(ii)明示 $p,q>0$ 却将指数写为 $1-q$。取 $(p,q)=(1,2)$，其积分发散，后续有限阶乘公式不匹配。同页 $L=\varnothing,k=0$ 是求和允许项，却调用 $B(|N|,0)$，超出正参数定义；①在 $|L|=0$ 时被积函数在开区间上为零，统一写成1不成立。Theorem3第9页和Theorem4第10–11页复用这一路线，故归并为同一issue。另极端剩余集合为空时②的重编号上界成为负数，须明确空和，而原文未单独处理。

\[B(p,q)=\int_0^1x^{p-1}(1-x)^{1-q}\,dx;\quad B(|N|-|L|-k,|L|+k);\quad \int_0^1|L|(1-x)^{|L|-1}\,dx=1\]

第7页(ii)明示 $p,q>0$ 却将指数写为 $1-q$。取 $(p,q)=(1,2)$，其积分发散，后续有限阶乘公式不匹配。同页 $L=\varnothing,k=0$ 是求和允许项，却调用 $B(|N|,0)$，超出正参数定义；①在 $|L|=0$ 时被积函数在开区间上为零，统一写成1不成立。Theorem3第9页和Theorem4第10–11页复用这一路线，故归并为同一issue。另极端剩余集合为空时②的重编号上界成为负数，须明确空和，而原文未单独处理。

原Shapley、SII、STI结论未发现反例。保持同一命题的全部允许集合，使用有限阶乘卷积给完整证明，含L空集与剩余集合为空，避免修补原积分域而改变目标。

来源：src-cvpr2023-supplement PDF 7, src-cvpr2023-supplement PDF 8, src-cvpr2023-supplement PDF 9, src-cvpr2023-supplement PDF 10, src-cvpr2023-supplement PDF 11

## 纯AND分布证明的三个case没有覆盖不可比集合

记录 ID：cvpr-issue-distribution-incomparable

原目标量化全部 $S\subseteq N$，但原证明只写上述三类。例 $N=\{1,2\}$、$T=\{1\}$、$S=\{2\}$ 落在三类之外。目标 $w_S=0$ 在此仍真，因为没有 $U\subseteq S$ 包含T。修正证明以 $T\not\subseteq S$、$S=T$、$T\subsetneq S$ 分组（不改原陈述），也可直接复用已编译的interaction_unanimity。

\[S\subsetneq T;\quad S=T;\quad S\supsetneq T\]

原目标量化全部 $S\subseteq N$，但原证明只写上述三类。例 $N=\{1,2\}$、$T=\{1\}$、$S=\{2\}$ 落在三类之外。目标 $w_S=0$ 在此仍真，因为没有 $U\subseteq S$ 包含T。修正证明以 $T\not\subseteq S$、$S=T$、$T\subsetneq S$ 分组（不改原陈述），也可直接复用已编译的interaction_unanimity。

原目标正确，原证明缺case。Add-Mul推导复用这个目标，保留同一原命题并完成修证明。

来源：src-cvpr2023-supplement PDF 5, src-cvpr2023-supplement PDF 6

## 选择集合大小与非零系数个数不总相等

记录 ID：cvpr-issue-l0-support

第4页定义 $w^{\prime}_S=w_S$ 若 $S\in\Omega$，否则为0。若 $S\in\Omega$ 而 $w_S=0$，它贡献集合大小却不贡献L0范数；例如全零模型、$\Omega=\{\varnothing\}$ 给0与1。两类可行表示的最优值可能通过删除零项联系，但原逐项相等并无无条件证明。

\[\|\boldsymbol w_\Omega\|_0=|\Omega|\]

第4页定义 $w^{\prime}_S=w_S$ 若 $S\in\Omega$，否则为0。若 $S\in\Omega$ 而 $w_S=0$，它贡献集合大小却不贡献L0范数；例如全零模型、$\Omega=\{\varnothing\}$ 给0与1。两类可行表示的最优值可能通过删除零项联系，但原逐项相等并无无条件证明。

这是算法段的原等式边界，不是编号定理；不静默把Omega定义改为support。目录保留原式和反例。

来源：src-cvpr2023-main PDF 4

## L0约束与固定罚参数目标的等价箭头未被证明

记录 ID：cvpr-issue-lagrange-equivalence

原Eq.(6)没有规定罚参数如何选取或证明离散非凸目标的强对偶。一般离散优化中，可行点 (support,error)=(0,3),(1,2),(2,0)，约束M=1选择中点，但任何lambda要选中点都需lambda≤1且lambda≥2，矛盾。本反例针对一般等价箭头，没有声称这一三点实例已由本文某个DNN产生。

\[\min\mathrm{unfaith}\ \mathrm{s.t.}\|w_\Omega\|_0\le M\ \Longleftrightarrow\ \min\mathrm{unfaith}+\lambda\|w_\Omega\|_0\]

原Eq.(6)没有规定罚参数如何选取或证明离散非凸目标的强对偶。一般离散优化中，可行点 (support,error)=(0,3),(1,2),(2,0)，约束M=1选择中点，但任何lambda要选中点都需lambda≤1且lambda≥2，矛盾。本反例针对一般等价箭头，没有声称这一三点实例已由本文某个DNN产生。

只能按原文登记为启发式目标转换/松弛；不当作本篇已证明的数学等价。

来源：src-cvpr2023-main PDF 4

## 已解释比例在全部效应为零时未定义

记录 ID：cvpr-issue-ratio-zero-denominator

取 $v(x_S)=0$ 对所有S，得到全部 $w_S=0$、$\Delta=0$，分母为0。原文未给此边界约定。符号表把分母非零记录为表达式的定义域条件，不据此修改原论文命题或杜撰R值。

\[R_\Omega=\frac{\sum_{S\in\Omega}|w_S|}{\sum_{S\in\Omega}|w_S|+|\Delta|}\]

取 $v(x_S)=0$ 对所有S，得到全部 $w_S=0$、$\Delta=0$，分母为0。原文未给此边界约定。符号表把分母非零记录为表达式的定义域条件，不据此修改原论文命题或杜撰R值。

仅影响指标的零模型边界与符号域；重构/唯一性仍适用。

来源：src-cvpr2023-main PDF 5

## 基线变化也会改变截断的平方残差损失

记录 ID：cvpr-issue-baseline-truncated-loss

原“just affects $\|w_\Omega\|_1$”不能解释为截断损失unfaith不随基线变。取单变量模型 $v(z)=z$、原输入x=1、输入基线r、只保留 $\Omega=\{\varnothing\}$。完整交互为 $w_\varnothing=r,w_{\{1\}}=1-r$；截断残差平方和为 $[r-r]^2+[1-r]^2=(1-r)^2$，随r变化。完整交互的unfaith始终0，但截断损失部分也可能改变。保留原句、单列该解释错误，不把原复合断言替换成较弱命题后算整体通过。

\[\text{change of baseline values always ensures unfaith}(w)=0\text{ and just affects }\|w_\Omega\|_1\]

原“just affects $\|w_\Omega\|_1$”不能解释为截断损失unfaith不随基线变。取单变量模型 $v(z)=z$、原输入x=1、输入基线r、只保留 $\Omega=\{\varnothing\}$。完整交互为 $w_\varnothing=r,w_{\{1\}}=1-r$；截断残差平方和为 $[r-r]^2+[1-r]^2=(1-r)^2$，随r变化。完整交互的unfaith始终0，但截断损失部分也可能改变。保留原句、单列该解释错误，不把原复合断言替换成较弱命题后算整体通过。

完整w各自重构的恒等式成立；不据此证明截断损失只变化L1。原复合句保留且分开状态。

来源：src-cvpr2023-main PDF 5

## Lemma3行列式消元漏余子式符号

记录 ID：sparse-issue-determinant-sign

取n=3,M=2，Eq31的矩阵为[[1,2],[1,1]]，行列式−1。Eq32沿首列展开漏(−1)^(M+1)，重复后应有(−1)^(M(M−1)/2)。这只改变非零行列式的符号，不推翻满列秩命题。

\[D\prod_{k=1}^M\binom nk=1,\quad D=(\prod_{k=1}^M\binom nk)^{-1}\]

来源：src-iclr2024-sparse-main PDF 18

## Beta定义指数方向与后续值不一致

记录 ID：sparse-issue-beta-exponent

正式图像确写1−q。取p=1,q=2，右侧为发散积分；随后给B(1,2)=1/2。修证明可用有限组合计数，不改Shapley/SII/STI命题。

\[B(p,q)=\int_0^1x^{p-1}(1-x)^{1-q}\,dx\]

来源：src-iclr2024-sparse-main PDF 22

## Shapley等证明的L=∅零参数边界未处理

记录 ID：sparse-issue-beta-empty-L

允许L=∅且k=0时调用B(n,0)，违反刚声明的正参数域。|L|=0时标①的被积函数在(0,1)为0，不能统一写成1；原离散权重项本身有限，需独立处理边界。

\[B(n-|L|-k,|L|+k),\qquad |L|\int_0^1(1-x)^{|L|-1}\,dx=1\]

来源：src-iclr2024-sparse-main PDF 22, src-iclr2024-sparse-main PDF 23, src-iclr2024-sparse-main PDF 24, src-iclr2024-sparse-main PDF 26, src-iclr2024-sparse-main PDF 27

## Lemma1的一般无限Taylor恒等式缺少有效性前提

记录 ID：sparse-issue-taylor-validity

原文仅说适用于continuously differentiable functions，Lemma1本身未假设解析性或Taylor级数等于函数。n=1,b=0,x=1，取v(t)=exp(−1/t²)（t≠0），v(0)=0。此函数C∞，所有在0的导数为0，但I({1})=e^(−1)≠0，而Eq8右边为0。反例针对一般Lemma1，不满足全空间高阶导数为零，故不直接否定1β⇒1α。

\[v(x_S)=\sum_{\kappa\in\mathbb N^n}\frac{D^\kappa v(b)}{\kappa!}(x_S-b)^\kappa\]

来源：src-iclr2024-sparse-main PDF 5, src-iclr2024-sparse-main PDF 15, src-iclr2024-sparse-main PDF 16

## Lemma1掩码幂式漏κ_i>0条件

记录 ID：sparse-issue-zero-power

κ_i=0时该式为0^0=1（Taylor单项式约定），不是0。后续PS过滤实际只需“若κ_i>0则项为零”，可修证明中间解释；不改PS或最终目标。

\[\forall i\notin S,\ [(x_S)_i-b_i]^{\kappa_i}=0\]

来源：src-iclr2024-sparse-main PDF 16

## Theorem2原路线未处理ū(1)=0

记录 ID：sparse-issue-theorem2-zero-output

取所有掩码u(S)=0，三条假设均满足，但Eq41除以0。此反例只否定原证明步骤：最终等式乘ū(1)=0仍可成立，不能据此宣布Theorem2是假。修路线应处理全零分支，不能增添ū(1)>0假设。

\[A^{(k)}/\bar u^{(1)}\]

来源：src-iclr2024-sparse-main PDF 19

## Theorem2原构造G可为空

记录 ID：sparse-issue-theorem2-empty-G

n=3,M=1,p=2，u(S)=|S|满足三假设，ū(1)=1,A(1)=3，n进制最高次数q(1)=1≤floor(p)−1，故G为空。原最大值与k*不存在；Lemma3不能制造原构造全零λ以外的λ。最终存在式或有另一构造，此为路线缺口而非最终结论反例。

\[G=\{k:1\le k\le M,q^{(k)}\ge\lfloor p\rfloor\},\quad\delta=\max_{k\in G}\delta^{(k)}\]

来源：src-iclr2024-sparse-main PDF 19, src-iclr2024-sparse-main PDF 20

## Theorem2调用Lemma2的m范围不足

记录 ID：sparse-issue-theorem2-m0-range

当M<n<2M时n−M<M，Lemma3取得的非零行可能不在Eq40已陈述范围。平均公式本身可对所有m扩展（k>m的组合数为0），属于证明补全而非新增数学假设。

\[m_0\in\{n,n-1,\ldots,n-M\},\qquad (40)\text{ only for }M\le m\le n\]

来源：src-iclr2024-sparse-main PDF 20

## p∈(0,1)时低位下标书写未定义

记录 ID：sparse-issue-theorem2-p-under-one

p>0允许p<1；floor(p)−1=−1，而正文只定义非负进制位、常数位。作者实验包含约0.9值，不能擅补p≥1。规范求和读作有限族J={i∈ℕ:i<floor(p)}时该族为空；若继续保留额外显示的a0项，全部低位取0的同一见证也成立。项目给任意有限低位族的统一构造，覆盖这两种常规读法，无须添加p≥1。原省略号书写问题仍保留，不声称原式逐字定义了负指标。

\[a_{\lfloor p\rfloor-1}^{(k)}n^{\lfloor p\rfloor-1}+\cdots+a_0^{(k)}\]

来源：src-iclr2024-sparse-main PDF 7, src-iclr2024-sparse-main PDF 19

## 完全抵消与空阶下η除法边界

记录 ID：sparse-issue-eta-zero

无交互时定义为0/0；非零正负交互恰好抵消时η=0，Eq57除法亦未定义。Theorem3所在Case1明确|η|≫1/n，已提供非零上下文，可以在该原范围忠实证明；不能扩大为完全抵消情况。

\[\eta^{(k)}=A^{(k)}/\sum_{|S|=k}|I(S)|,\quad A^{(k)}/\eta^{(k)}=\sum_{|S|=k}|I(S)|\]

来源：src-iclr2024-sparse-main PDF 7, src-iclr2024-sparse-main PDF 8, src-iclr2024-sparse-main PDF 20, src-iclr2024-sparse-main PDF 21

## fully random不足以推出2^|S|方差放大

记录 ID：sparse-issue-noise-variance

原文未说明噪声项相互独立且同方差。令所有εT同一个非退化随机Z，中心化后εT−ε∅=0，所有噪声交互为0；该方差放大式不成立。若fully random意为iid需明确语义，不能自行给独立同方差假设。空集交互恒0也不是1倍原噪声方差。

\[\operatorname{Var}(I_\varepsilon(S))=2^{|S|}\operatorname{Var}(\varepsilon)\]

来源：src-iclr2024-sparse-main PDF 8

## 奇偶例的u(∅)与中心化冲突

记录 ID：sparse-issue-parity-empty

空集偶数，所以该显示定义给u(∅)=−1，而本篇全局定义给u(∅)=0。原示例在当前定义域中不存在。不能把u改成g或改空集值后宣称原例证明完成；原符号语义冲突单列。

\[u(S)=\begin{cases}+1&|S|\text{ odd}\\-1&|S|\text{ even}\end{cases}\]

来源：src-iclr2024-sparse-main PDF 9

## 单样本稀疏与重构不能推出样本间迁移

记录 ID：sparse-issue-transfer

令总体N有n≥2变量，n个样本分别诱导g0^(j)(S)=1若j∈S，反之0。每个样本仅一个非零单变量交互，全部掩码都精确重构；不同样本的显著支撑互不相交。这些集合函数可由同一模型在不同掩码样本上实现（例如各样本仅一个坐标非零、v(z)=sum_i z_i），所有样本输出为1，可按分类阈值v(z)>1/2全部指定为同一正类，满足原“same category”条件。无需“爆炸”模式数。原反证没有全模型模式预算前提。

\[\text{sparsity} + \text{universal matching}\Rightarrow\text{sample-wise transferability}\]

来源：src-iclr2024-sparse-main PDF 9

## D.2两个分量名称及去噪γ符号不一致

记录 ID：sparse-issue-decomposition-notation

正式原式第二分量同名uand，去噪两项加γ使和为u−ε+2γ而非去噪输出。属于算法/证明中间式的标记与符号错；在原最终分解u=uand+uor保持不变下可标注并修中间式。

\[u_{and}=0.5u+\gamma,\quad u_{and}=0.5u-\gamma;\qquad u_{and}=0.5(u-\varepsilon)+\gamma,\quad u_{or}=0.5(u-\varepsilon)+\gamma\]

来源：src-iclr2024-sparse-main PDF 29

## Case2非指数小抵消比例不足以推出同阶稀疏

记录 ID：sparse-issue-asymptotic-sparsity

完整无限族反例已写于math/rewrites.zh.md的asymptotic-claim。取n≥3且n≡2/3 mod4，q=choose(n,2)奇数；二阶±1系数的正/负项数为(q−1)/2与(q+1)/2，总和−1。模型v=Σzi+Σc_A∏i∈A zi，输入全1、基线0，给A1=n,A2=−1，所有高于二阶交互和混合偏导为零。μm=m−choose(m,2)/q；μm+1−μm=1−m/q>0，μm/m=1−(m−1)/(2q)非增，故原三条件以M=2,p=1完整满足。固定τ=1/100得到R2=q、η2=−1/q，其仅多项式小却二阶全显著。T3右端100q仍有效。反例只否定第8页Case2额外同阶推断，不把邻近mostcases经验描述当全称命题，也不否定总O(n²)相对2^n仍稀疏。

\[\text{Case2: }|\eta^{(k)}|\text{ not exponentially small}\ \Longrightarrow\ R^{(k)}\text{ still much less than }\binom nk\]

来源：src-iclr2024-sparse-main PDF 7, src-iclr2024-sparse-main PDF 8

## Appendix H三阶表漏x3单变量项

记录 ID：sparse-issue-example-H-arithmetic

正式图像确给0，但代入v=x1x2x3+x1x2+x2x3+x2+x3、x=(1,1,1,1,1)、基线0，{3,4,5}保留x3=1，所以输出为1。三阶10项和应19、平均1.9。原二阶平均1≤三阶平均的结论仍成立；仅修算例表项和派生均值。

\[u(\{3,4,5\})=0,\qquad\bar u^{(3)}=1.8\]

来源：src-iclr2024-sparse-main PDF 34

## Theorem1换序后的第三行误用S⊇L

记录 ID：sparse-issue-reconstruction-index

上一行要求T⊇L；第三行写成S⊇L不能筛选该L对应的T，导致计数不再是choose(|S|−|L|,t−|L|)。这是证明中间索引排印错；恢复上一行的T⊇L或用完整子集双射可证明相同原重构命题。

\[\sum_{\substack{T\subseteq S:S\supseteq L\\|T|=t}}(-1)^{t-|L|}u(L)\]

来源：src-iclr2024-sparse-main PDF 15

## Lemma4按l分组后仍保留未绑定L

记录 ID：sparse-issue-marginal-free-L

按基数l分组后L已经不是求和变量，指数应随l变化才能调用二项式抵消。保留原自由L式供核查，项目共享有限差分证明不使用该错误中间式；原引理目标和全部T/S边界不变。

\[\sum_{l=|K\setminus S|}^{|T|}(-1)^{|T|-|L|}\binom{|T|-|K\setminus S|}{l-|K\setminus S|}\]

来源：src-iclr2024-sparse-main PDF 21

## Theorem6临界阶换序后组合数误留自由S

记录 ID：sparse-issue-STI-free-S

外层原环境S在换序后已按q=|S|分组，分母仍出现自由S；下一段转积分要求分母为choose(n−1,q)。这是局部索引排印错误，修复的共享有限阶乘卷积证明直接得到原临界阶权重，保留三分支命题。

\[\sum_{L\subseteq N\setminus T}I(T\cup L)\sum_{q=0}^{n-t}\frac{\binom{n-t-|L|}{q-|L|}}{\binom{n-1}{|S|}}\]

来源：src-iclr2024-sparse-main PDF 26

## T2参数域未在陈述中明确

记录 ID：sparse-issue-T2-parameter-domain

T2正文/附录没有明确重复Lemma3的M<n；不能把该限制偷偷加到T2。新构造覆盖M=n。实数log_n和n进制在n>1，全部choose(n,k)分母非零在M≤n；这是原表达的定义域说明。原页面未找到明确M∈N+约定：若允许M=0，取n=3且所有中心化输出0，三假设均成立，λ的空和为0，与λ≠0矛盾；因此这一读法的原陈述有反例，单列，不补M>0后冒充无条件原命题。正阶定义域中的完整存在构造另可验证。

\[\lambda=\sum_{k=1}^M\frac{\binom{m_0}k}{\binom nk}\lambda^{(k)}\ne0,\qquad\log_n(\cdot)\]

来源：src-iclr2024-sparse-main PDF 5, src-iclr2024-sparse-main PDF 7, src-iclr2024-sparse-main PDF 17, src-iclr2024-sparse-main PDF 18, src-iclr2024-sparse-main PDF 19

## Lemma3 Eq33的降阶矩阵一行复制了n−2

记录 ID：sparse-issue-lemma3-copied-row

正式Eq33第二行除第一列外仍印n−2，与Eq32相邻行差分后第二行应来自n−3不一致。原数组在完整TeX中保留；正确消元或已完成的有限差分归纳可证明原零空间结论，不需沿错误矩阵再计算。该索引复制错与余子式符号漏项分别标记。

\[\left[\binom{n-3}0,\binom{n-2}1,\ldots,\binom{n-2}{M-2}\right]\]

来源：src-iclr2024-sparse-main PDF 18

## OR原证明的分类中间零和、条件输出代入及空掩码重合

记录 ID：issue-f11-or-intermediate-20260930

第13页该首代入式不保留二次掩码。取N={1,2}、T={1}、$g(A)=\mathbf1_{N\subseteq A}$、S=N。字面条件游戏hT全零，所以OR系数左0；原右−1。正确逐项输出是 $v_{or}((x_T)_{N\setminus L})=v_{or}(x_{T\setminus L})$。第14页case(3)以 $\sum_{j=0}^{|T|-|T\cap L|}\binom{|T|-|T\cap L|}j(-1)^j=0$ 作内层消去，但T子集L时上界0，和1；例如N={1,2},T=L={1}。完整外层仍能消去，但原标注内零不成立。case(4)激活要求在T新增至少一个变量，原下界印0，应分别核实际索引族；T空时case(1) L=N\T与case(2)L=N重合，不能重复计同一项。

\[\sum_{S:S\cap T\ne\varnothing}I_{or}(S\mid x_T)=\sum_{S:S\cap T\ne\varnothing}\left[-\sum_{L\subseteq S}(-1)^{|S|-|L|}v_{or}(x_{N\setminus L})\right]\]

第13页该首代入式不保留二次掩码。取N={1,2}、T={1}、$g(A)=\mathbf1_{N\subseteq A}$、S=N。字面条件游戏hT全零，所以OR系数左0；原右−1。正确逐项输出是 $v_{or}((x_T)_{N\setminus L})=v_{or}(x_{T\setminus L})$。第14页case(3)以 $\sum_{j=0}^{|T|-|T\cap L|}\binom{|T|-|T\cap L|}j(-1)^j=0$ 作内层消去，但T子集L时上界0，和1；例如N={1,2},T=L={1}。完整外层仍能消去，但原标注内零不成立。case(4)激活要求在T新增至少一个变量，原下界印0，应分别核实际索引族；T空时case(1) L=N\T与case(2)L=N重合，不能重复计同一项。

错误属于原证明的中间分类和条件式代入；原OR及AND-OR父命题不变。修正证明使用相交子集族差及完整Möbius重构，包含T空，逐项保留literal conditioned sample。

来源：src-iclr2024-generalizable-main PDF 13, src-iclr2024-generalizable-main PDF 14

## Appendix D首句方差中心跨S与期望下标不一致

记录 ID：f11-issue-variance-expectation-indices

首句内层中心写I′(S)，外层仅εT下标；严格方差须对全部噪声联合样本求期望且中心为同T随机变量的期望。随后原Proof实际使用Var(I′(T))和固定I(T)，其IID方差结论正确。原首句保留，修记号与证明解释，不改最终Var结论。

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

## Lemma 1 的空场命题反例

记录 ID：hnet-issue-empty-field

原Lemma只要求R1/R2。取 $R_j=\varnothing,z_j\equiv1$，R1成立且R2为空积1。但原Definition2使所有中心化交互零，尤其 $J_j(\varnothing)=0\ne1$。PDF15推导非空集合交替和为零时未分辨空场。

原Lemma全范围错误，不能加非空前提；实际无偏置架构零基线子结论另证。Theorem3只分给包含玩家的场，常数单元贡献零，并未被此反例推翻。

\[J_j(R_j)=z_j(x)\]

原Lemma只要求R1/R2。取 $R_j=\varnothing,z_j\equiv1$，R1成立且R2为空积1。但原Definition2使所有中心化交互零，尤其 $J_j(\varnothing)=0\ne1$。PDF15推导非空集合交替和为零时未分辨空场。

原Lemma全范围错误，不能加非空前提；实际无偏置架构零基线子结论另证。Theorem3只分给包含玩家的场，常数单元贡献零，并未被此反例推翻。

来源：src-icml2023-harsanyinet-formal PDF 3, src-icml2023-harsanyinet-formal PDF 14, src-icml2023-harsanyinet-formal PDF 15

## Theorem 3 原全j分式空场约定未明

记录 ID：hnet-issue-t3-empty-division

全j求和可能包含空场；实数域先算分式再乘零需要除零约定。严谨条件和只在场含i时算分式，含i保证基数正。

这是表达式定义域歧义；完整经典归因条件和恒等式已证，不宣称Theorem3被空场Lemma反例推翻。

\[\sum_j\frac{w_jz_j(x)}{|R_j|}\mathbf1_{i\in R_j}\]

全j求和可能包含空场；实数域先算分式再乘零需要除零约定。严谨条件和只在场含i时算分式，含i保证基数正。

这是表达式定义域歧义；完整经典归因条件和恒等式已证，不宣称Theorem3被空场Lemma反例推翻。

来源：src-icml2023-harsanyinet-formal PDF 12, src-icml2023-harsanyinet-formal PDF 13

## Theorem 4 证明的全第一层量词及乘积替换错误

记录 ID：hnet-issue-t4-quantifier

缺一个输入变量只保证依赖它的孩子沿路径为零，不保证所有第一层节点为零。整个AND积也不能无条件等于指定单因子；修正只使用存在一个零因子使乘积零。

命题不变，按感受野并集和拓扑次序证明R1/R2；完整原链保留在original-proofs。

\[\forall u^{\prime},\ z_{u^{\prime}}^{(1)}(x_T)=0\]

缺一个输入变量只保证依赖它的孩子沿路径为零，不保证所有第一层节点为零。整个AND积也不能无条件等于指定单因子；修正只使用存在一个零因子使乘积零。

命题不变，按感受野并集和拓扑次序证明R1/R2；完整原链保留在original-proofs。

来源：src-icml2023-harsanyinet-formal PDF 13, src-icml2023-harsanyinet-formal PDF 14

## CNN 原交互展开漏感受野过滤

记录 ID：hnet-issue-cnn-filter

目标S固定时只有 $R_j=S$ 的单元贡献。场分别为单例1/2、贡献各1时，目标单例1的交互1而无过滤末和2。原等式全文保留，修正加入已由unit变换导出的过滤。

不否定正确有限通道重组；修正同一模型的目标交互展开。

\[I(S=R_u)=\sum_jw_jz_j(x)\]

目标S固定时只有 $R_j=S$ 的单元贡献。场分别为单例1/2、贡献各1时，目标单例1的交互1而无过滤末和2。原等式全文保留，修正加入已由unit变换导出的过滤。

不否定正确有限通道重组；修正同一模型的目标交互展开。

来源：src-icml2023-harsanyinet-formal PDF 16

## 共同gate不推出全部通道输出同时非零

记录 ID：hnet-issue-cnn-activation

原句用共同孩子推出同时激活。共同gate确相同，但两个权重给线性值1与-1，ReLU后为(1,0)。因此只能说gate同时开闭，不能把非零输出同步当作group证明前提。

感受野等式及加权有限和仍成立；分组gate掩码律独立证明。

\[h_{(1,h,w)},\ldots,h_{(C,h,w)}\text{ activate simultaneously}\]

原句用共同孩子推出同时激活。共同gate确相同，但两个权重给线性值1与-1，ReLU后为(1,0)。因此只能说gate同时开闭，不能把非零输出同步当作group证明前提。

感受野等式及加权有限和仍成立；分组gate掩码律独立证明。

来源：src-icml2023-harsanyinet-formal PDF 16

## scalar AND 与 group gate 数值等价子句错误

记录 ID：hnet-issue-cnn-gate-equivalence

孩子向量(1,0)给左gate0、右gate1；父线性值1时ReLU输出分别0、1。改变gate没有保持同一函数。

仅此数值等价子句被否定；新groupgate架构仍能满足R1/R2及其自身输出的Shapley式，正文完整直接归纳。

\[\prod_c\mathbf1_{z_c\ne0}=\mathbf1_{\sum_c|z_c|\ne0}\]

孩子向量(1,0)给左gate0、右gate1；父线性值1时ReLU输出分别0、1。改变gate没有保持同一函数。

仅此数值等价子句被否定；新groupgate架构仍能满足R1/R2及其自身输出的Shapley式，正文完整直接归纳。

来源：src-icml2023-harsanyinet-formal PDF 7, src-icml2023-harsanyinet-formal PDF 16

## Eq.(9) 任意传统网络省略输出基线

记录 ID：hnet-issue-eq9-baseline

本篇I为中心化交互，重构和是 $v(x)-v(x_\varnothing)$。常数模型1全部I为零但原输出1，反例否定任意传统网络的第一等号。

无偏置Harsanyi实际架构基线零时成立；M数量界不证明传统DNN尾和小。

\[v(x)=\sum_{S\subseteq N}I(S)\]

本篇I为中心化交互，重构和是 $v(x)-v(x_\varnothing)$。常数模型1全部I为零但原输出1，反例否定任意传统网络的第一等号。

无偏置Harsanyi实际架构基线零时成立；M数量界不证明传统DNN尾和小。

来源：src-icml2023-harsanyinet-formal PDF 3, src-icml2023-harsanyinet-formal PDF 6

## 光滑gate空选子指数与第一层非负域未说明

记录 ID：hnet-issue-smooth-domain

空选子使trace为零，几何均值指数无实数定义约定。第一层x-r未经ReLU，可为负，不能自动套所有前层非负的说明。

完整记录训练定义及边界；hardgate形式化不冒充该训练公式全参数域验证。

\[1/\operatorname{tr}\Sigma_j\]

空选子使trace为零，几何均值指数无实数定义约定。第一层x-r未经ReLU，可为负，不能自动套所有前层非负的说明。

完整记录训练定义及边界；hardgate形式化不冒充该训练公式全参数域验证。

来源：src-icml2023-harsanyinet-formal PDF 5, src-icml2023-harsanyinet-formal PDF 6

## Eq.(15) 缺失二项式系数

记录 ID：layer-issue-binomial-15

作者按阶数汇总子集时漏掉组合数量。

$|T|-|L|=2$ 时原和为 $1-1+1=1$，并非 $0$；正确和为 $1-2+1=0$。

同一重构命题用完整二项式消去补正，原错式保留。

来源：src-icml2024-layerwise-formal PDF 15

## Eq.(16) OR 分组的零因子不成立

记录 ID：layer-issue-or-calculation-16

原分组的符号缺少固定 L 与 T 交集的指数；零因子仍须按两个剩余块完整核对。

取 $N=\{1,2\},T=\{1\},L=\{1\}$，原式 $S_1=\varnothing,\{2\}$ 的符号与原 $|S|-|L|$ 相反。其分组总和虽可由剩余块消去，但这不使逐项错符号相等。

用全 OR 和减去不激活 OR 和完整补证，不改变定理。

来源：src-icml2024-layerwise-formal PDF 15

## 固定与条件 OR 游戏不可混换

记录 ID：layer-issue-conditional-scope

AND 在 S⊆T 时可限制相等；OR 补集变换在再次掩码后通常改变。

$N=\{1,2\}$，$o(U)=\mathbf1_{\{1,2\}\subseteq U}$，$T=\{1\}$：固定 $O(\{1\})=1$，限制游戏 $o_T\equiv0$ 的 $O_T(\{1\})=0$。

两种重构均证明；限制分解与独立重新学习的分解须分别实例化。

来源：src-icml2024-layerwise-formal PDF 4, src-icml2024-layerwise-formal PDF 15

## Eq.(2) 字面空集值与定理特设值不同

记录 ID：layer-issue-empty-or

Definition 3.2 对所有 S 的公式在空集不等于随后特设基线。

$o(\varnothing)=0,o(N)=1$ 给原公式空值 $-1$，而定理空值 $0$。

非空负变换与原定理空集约定分开保存。

来源：src-icml2024-layerwise-formal PDF 4

## Eq.(19) 重复加入输出基线

记录 ID：layer-issue-baseline-19

AND 求和已经含空集基线，原式又加了一次。

$g\equiv1,a\equiv1,o\equiv0$ 满足原空分量条件，原右端为 $1+1=2\ne1$。

保留显式 b 时删去 AND 求和中的空项；这修复中间式，不解决显著近似的外引缺口。

来源：src-icml2024-layerwise-formal PDF 16

## Lemma 3.4 与 OR 稀疏外引条件未验证

记录 ID：layer-issue-sparse-transfer

补集代数等式不能自动保证学习分量满足所引稀疏定理条件。

原文缺少对 AND 分量、OR 分量补集游戏的条件检验，也没有给“小”和近似误差的定量定义。

完整原文仍保留，项目给出尾和条件界并将原断言范围标为未完成，未偷添条件。

来源：src-icml2024-layerwise-formal PDF 3, src-icml2024-layerwise-formal PDF 4, src-icml2024-layerwise-formal PDF 13, src-icml2024-layerwise-formal PDF 16

## Eq.(12) 不是所需反向掩码

记录 ID：layer-issue-coordinate-13

原两坐标定义实际互补，Eq.(13) 的第二等号错误。

$N=T=\{1\},x_1=1,r_1=0,v(z)=z_1$ 给 $0\ne1$。

原坐标错式独立登记；游戏层面的补集负变换证明有效，不把新定义换进原式。

来源：src-icml2024-layerwise-formal PDF 13

## Eq.(8) 在原显著支持下第一等式失败

记录 ID：layer-issue-strength-8

重叠项只在共同显著支持求和，忘记项却从每个本层显著系数减去实际共享值。

归一化纯 AND 系数本层 $(1/2,1/2)$、末层 $(1/101,100/101)$；原阈值给支持 $\{\{1\},\{2\}\}$ 与 $\{\{2\}\}$。$\operatorname{all}_{l,1}=1$，$\operatorname{overlap}_{l,1}+\operatorname{forget}_{l,1}=1/2+99/202=100/101$。两分解 L1=1 全局最优。

第一子句有完整反例；本例第二子句成立。不能用正确标量引理冒充原总式证明。

来源：src-icml2024-layerwise-formal PDF 5, src-icml2024-layerwise-formal PDF 6, src-icml2024-layerwise-formal PDF 7

## 比值、平均与归一化的零边界未规定

记录 ID：layer-issue-zero-metrics

空并集、零总强度、零方差、空显著集合或零归一化因子会产生未定义实数表达。

原文未分别给这些情况的赋值规则；残差严格界在 κ=0 时也无可行解。

只在原表达有定义时解释数值，不新增隐含零值约定。

来源：src-icml2024-layerwise-formal PDF 5, src-icml2024-layerwise-formal PDF 7, src-icml2024-layerwise-formal PDF 8, src-icml2024-layerwise-formal PDF 21

## 原空联盟归因未定义

记录 ID：issue-coalition-empty-coalition

Eq.(6) 的全子集量词包含空集，但 T=空集项含0/0；3.4、3.8及部分公理沿用该未定义对象。

S=\varnothing,T=\varnothing gives |S|/|T|=0/0; Eq.(3),(4) only define nonempty interactions.

The nonempty-coalition proof is recorded separately. No zero convention or new hypothesis is silently appended to the original statement.

来源：src-icml2025-coalition PDF 4, src-icml2025-coalition PDF 5, src-icml2025-coalition PDF 6

## OR边际的原求和域错印

记录 ID：issue-coalition-or-condition

附录C的OR边际第一行和随后求和域误写非空交集；必须是不交。下一行改为 S⊆N\{i}\L 说明作者实际计算的是不交。

The OR effect is activated by adding i exactly when i belongs to T and T∩S=empty. A term already intersecting S cancels from the marginal.

Theorem 3.2 is unchanged; only the erroneous proof condition is repaired.

来源：src-icml2025-coalition PDF 14

## 忠实度比例的零分母

记录 ID：issue-coalition-zero-denominators

三个比例未规定零分母。零游戏配零分解使分子分母皆零；不能直接声称所有输入上均定义且落在区间。

g(S)=0, γ_S=0 for every S gives A(T)=O(T)=0 and all three ratios 0/0.

Bounds hold on the original quotient domain where the denominator is positive. This scope restriction is disclosed, not added to the original claim.

来源：src-icml2025-coalition PDF 6, src-icml2025-coalition PDF 7

## 总游戏对称不保证最优分解对称

记录 ID：issue-coalition-symmetry-decomposition

总输出对称不能推出各分量对称；α、β公理在原给定分解规则下均有全局最优反例。

取 $N=\{1,2,3\}$，$g(U)=|U|$。令 $P=\{1,3\}$，$a(U)=\mathbf1[P\subseteq U]+\mathbf1[2\in U]$，$o(U)=\mathbf1[U\cap P\ne\varnothing]$；这确实满足 $a+o=g$（在 $P$ 中有0、1、2个变量时，AND+OR分别为0、1、2）。因此 $\gamma_U=a(U)-g(U)/2$ 是原分量形式的实际实现。其唯一非零非空系数为 $A(P)=1,O(P)=1,A(\{2\})=1$。于是 $\phi(P)=2$ 而 $\phi(\{2,3\})=0$。任意精确分解由 Eq.(10) 满足 $g(N)-g(\varnothing)=\sum_{T\ne\varnothing}(A(T)+O(T))$，三角不等式给出 $|g(N)-g(\varnothing)|\le\sum_{T\ne\varnothing}(|A(T)|+|O(T)|)$。本例右侧为3、左侧也为3，故是全局最优的稀疏分解。总游戏完全对称，而最优分解非唯一，并不保证分量对称。

Let $N=\{1,2,3\}$ and $g(U)=|U|$. Put $P=\{1,3\}$, $a(U)=\mathbf1[P\subseteq U]+\mathbf1[2\in U]$, and $o(U)=\mathbf1[U\cap P\ne\varnothing]$. Then $a+o=g$: AND plus OR contributes 0, 1, or 2 according to the number of present members of $P$. The actual decomposition parameter is $\gamma_U=a(U)-g(U)/2$. The only nonzero nonempty coefficients are $A(P)=1,O(P)=1,A(\{2\})=1$, so $\phi(P)=2$ and $\phi(\{2,3\})=0$. Equation (10) implies $g(N)-g(\varnothing)=\sum_{T\ne\varnothing}(A(T)+O(T))$ for every exact decomposition. Hence the triangle inequality gives $|g(N)-g(\varnothing)|\le\sum_{T\ne\varnothing}(|A(T)|+|O(T)|)$. Both sides equal 3 here, proving global optimality. A symmetric total game can therefore have nonsymmetric globally sparsest decompositions.

For α use i=1,j=2,L={3}; for β use S={1},T={2},L={3}. Its premise holds because g depends only on cardinality. The claimed conclusion fails.

来源：src-icml2025-coalition PDF 6, src-icml2025-coalition PDF 18, src-icml2025-coalition PDF 19, src-icml2025-coalition PDF 20

## 最优分解不能保证联盟归因可加

记录 ID：issue-coalition-additivity-decomposition

附录G.4从总输出可加性直接推出分量交互可加性，未得到分解参数兼容；原可加公理有最优分解反例。

取 $N=\{1,2\}$，$g_1(U)=\mathbf1[1\in U]$、$g_2(U)=\mathbf1[2\in U]$，总游戏 $g=g_1+g_2$。对子游戏取 $a_k=g_k,o_k=0$，二者最小 L1 都为1，联盟 $N$ 的归因为0。对总游戏取 $a(U)=\mathbf1[N\subseteq U]$、$o(U)=\mathbf1[U\ne\varnothing]$，对应 $\gamma_U=a(U)-|U|/2$，唯一非零交互为 $A(N)=O(N)=1$，L1=2，达到 $|g(N)-g(\varnothing)|=2$ 下界。故三次分解均全局最优，但 $\phi_g(N)=2\ne0=\phi_{g_1}(N)+\phi_{g_2}(N)$。

Let $N=\{1,2\}$, $g_1(U)=\mathbf1[1\in U]$, $g_2(U)=\mathbf1[2\in U]$, and $g=g_1+g_2$. Choose $a_k=g_k,o_k=0$ for the component games. Each has globally minimal L1 value 1 and zero attribution to $N$. For the total game choose $a(U)=\mathbf1[N\subseteq U]$, $o(U)=\mathbf1[U\ne\varnothing]$, and thus $\gamma_U=a(U)-|U|/2$. Its only nonzero interactions are $A(N)=O(N)=1$. Its L1 value 2 reaches the lower bound $|g(N)-g(\varnothing)|=2$. All three decompositions are globally optimal, yet $\phi_g(N)=2\ne0=\phi_{g_1}(N)+\phi_{g_2}(N)$.

A linearity theorem for a fixed compatible coefficient decomposition is valid but is not a proof of the original axiom.

来源：src-icml2025-coalition PDF 6, src-icml2025-coalition PDF 20

## Dummy条件与分解选择的范围

记录 ID：issue-coalition-dummy-decomposition

总输出dummy不能推出分量dummy；给出满足显示定义、但不是L1最优的反例，最优规则的dummy版本单独保留未判定。

令 $N=\{1,2\}$、总游戏 $g=0$，取 $\gamma_U=\mathbf1[U=N]$，所以 $a=\gamma,o=-\gamma$。所有变量都是总游戏的dummy。计算 $A(N)=1$、$O(N)=1$，所以 $\phi(N)=2\ne0$。此例满足正文显示的分解定义，但 L1=4 并非全局最稀疏（零分解的 L1=0）。因此它反驳“仅依据分解定义即可满足dummy”的表述，不能声称已反驳额外规定全局最优且给定选择规则的dummy版本。论文没有把该选择规则完整规定为公理前提。

Let $N=\{1,2\}$ and $g=0$, and choose $\gamma_U=\mathbf1[U=N]$, so $a=\gamma$ and $o=-\gamma$. Every variable is dummy for the total game. Nevertheless $A(N)=O(N)=1$, giving $\phi(N)=2$. This satisfies the displayed decomposition definitions, but its L1 value 4 is not globally minimal: the zero decomposition has value 0. It refutes the dummy claim from the displayed definitions alone; it is not a counterexample to a separately stipulated global-optimum selection rule. The paper does not fully specify such a rule as an axiom premise.

No component-dummy premise is added to complete the original axiom.

来源：src-icml2025-coalition PDF 6, src-icml2025-coalition PDF 21

## 匿名性中的分量运输与重新选解

记录 ID：issue-coalition-anonymity-selection

若σ作用于既定AND/OR分解，匿名性是正确的换元恒等式；若仅作用于总游戏并重新求最优分解，最优非唯一不能保证此推断。

取 $N=\{1,2,3\}$，$g(U)=|U|$。令 $P=\{1,3\}$，$a(U)=\mathbf1[P\subseteq U]+\mathbf1[2\in U]$，$o(U)=\mathbf1[U\cap P\ne\varnothing]$；这确实满足 $a+o=g$（在 $P$ 中有0、1、2个变量时，AND+OR分别为0、1、2）。因此 $\gamma_U=a(U)-g(U)/2$ 是原分量形式的实际实现。其唯一非零非空系数为 $A(P)=1,O(P)=1,A(\{2\})=1$。于是 $\phi(P)=2$ 而 $\phi(\{2,3\})=0$。任意精确分解由 Eq.(10) 满足 $g(N)-g(\varnothing)=\sum_{T\ne\varnothing}(A(T)+O(T))$，三角不等式给出 $|g(N)-g(\varnothing)|\le\sum_{T\ne\varnothing}(|A(T)|+|O(T)|)$。本例右侧为3、左侧也为3，故是全局最优的稀疏分解。总游戏完全对称，而最优分解非唯一，并不保证分量对称。

Let $N=\{1,2,3\}$ and $g(U)=|U|$. Put $P=\{1,3\}$, $a(U)=\mathbf1[P\subseteq U]+\mathbf1[2\in U]$, and $o(U)=\mathbf1[U\cap P\ne\varnothing]$. Then $a+o=g$: AND plus OR contributes 0, 1, or 2 according to the number of present members of $P$. The actual decomposition parameter is $\gamma_U=a(U)-g(U)/2$. The only nonzero nonempty coefficients are $A(P)=1,O(P)=1,A(\{2\})=1$, so $\phi(P)=2$ and $\phi(\{2,3\})=0$. Equation (10) implies $g(N)-g(\varnothing)=\sum_{T\ne\varnothing}(A(T)+O(T))$ for every exact decomposition. Hence the triangle inequality gives $|g(N)-g(\varnothing)|\le\sum_{T\ne\varnothing}(|A(T)|+|O(T)|)$. Both sides equal 3 here, proving global optimality. A symmetric total game can therefore have nonsymmetric globally sparsest decompositions.

The transported-decomposition proof is preserved with its exact meaning; it does not prove invariance under an unspecified independently selected optimum.

来源：src-icml2025-coalition PDF 6, src-icml2025-coalition PDF 17

## 对称性β原配对的重复计数

记录 ID：issue-coalition-beta-pairing

G.3把两边分别求和改成全部等基数对求和，未给双射；每一项通常被重复计数。最初WLOG不交也没有给重叠化简。

If there are c subsets on each side of a fixed cardinality, the all-pairs sum equals c times the difference of the two original sums, not that difference. For c=2 take f=(1,0),h=(0,0): original difference 1, paired difference 2.

These proof defects are retained; the original symmetry-β statement already fails by the independent optimal-decomposition counterexample.

来源：src-icml2025-coalition PDF 19, src-icml2025-coalition PDF 20

## Table7若沿用相邻概率输出尺度，则数值不相容；本节未说明尺度变化

记录 ID：cvpr-issue-bow-table7-probability-scale

正式p17脚注在Table6相邻例子写In this example，采用概率输出；p18Table7有单变量6.568和二变量−13.481。若Table7继续使用这一概率尺度，原Möbius差分分别受[−1,1]及[−2,2]限制，故两表值与该定义不能同时成立。但是该脚注没有无歧义声明延续到Table7，原本节也未说明尺度是否变化；这里不无条件判表数据已证伪。正式PNG已实际查看，排除了文本提取误差。

\[v(x_S)=p(y=\text{positive sentiment}\mid x_S)\quad\text{(p17: In this example)},\qquad w_{\{\mathrm{smart}\}}=6.568,\quad w_{\{\mathrm{not},\mathrm{smart}\}}=-13.481\quad\text{(Table7)}\]

来源：src-cvpr2023-supplement PDF 17, src-cvpr2023-supplement PDF 18
