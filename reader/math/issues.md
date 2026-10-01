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

## Proposition1原证明的两处熵符号错误

记录 ID：robustness-entropy-proof-sign

原命题定义+H。正确四项差为$H(Y\mid S,i,j)-H(Y\mid S,i)-H(Y\mid S,j)+H(Y\mid S)$，等于$MI(X_i;Y\mid S)-MI(X_i;Y\mid S,X_j)$。原证明用了四项的相反数，再用了与Eq7相反的三元MI定义，最终两错抵消。H(H|XS)另为Y误植。

原命题定义+H。正确四项差为$H(Y\mid S,i,j)-H(Y\mid S,i)-H(Y\mid S,j)+H(Y\mid S)$，等于$MI(X_i;Y\mid S)-MI(X_i;Y\mid S,X_j)$。原证明用了四项的相反数，再用了与Eq7相反的三元MI定义，最终两错抵消。H(H|XS)另为Y误植。

只修证明；保留原+H与Eq6。原Eq7采用co-information符号，不能改成enhancement约定。

来源：src-neurips2021-robustness-formal PDF 7, src-neurips2021-robustness-supplement PDF 6

## B.1对称性证明上下文集合误植

记录 ID：robustness-symmetry-context-typo

对象$I_{ik}^{(m)}$的上下文应排除i,k，首/末平均却印成排除i,j。中间求和实际用N\{i,k}及N\{i,j,k}，可修为交换i,j的上下文双射证明。

对象$I_{ik}^{(m)}$的上下文应排除i,k，首/末平均却印成排除i,j。中间求和实际用N\{i,k}及N\{i,j,k}，可修为交换i,j的上下文双射证明。

对称性原陈述与原条件保持。

来源：src-neurips2021-robustness-supplement PDF 3

## Eq14/15把固定大小取整丢弃率换成连续比例

记录 ID：robustness-dropout-floor

原K均匀取固定大小k，不是Bernoulli dropout。取n=4、α=2/5、k=2、$g(S)=|S|$，所有pair交互0，真实均值2，原Eq14为$(1-α)4=12/5$。正确抽取包含率k/n仅可作为另一个修订推导，不能把它冒充原Eq14证明。

原K均匀取固定大小k，不是Bernoulli dropout。取n=4、α=2/5、k=2、$g(S)=|S|$，所有pair交互0，真实均值2，原Eq14为$(1-α)4=12/5$。正确抽取包含率k/n仅可作为另一个修订推导，不能把它冒充原Eq14证明。

固定大小平均的floor子句错误；高阶截断及经验cutout结论另分范围。

来源：src-neurips2021-robustness-formal PDF 9, src-neurips2021-robustness-formal PDF 10, src-neurips2021-robustness-supplement PDF 9, src-neurips2021-robustness-supplement PDF 10

## D(m)在全零交互上下文未定义

记录 ID：robustness-disentanglement-zero

若全部上下文Δg=0，分母与分子均0，原文未给0/0约定。比值界和同号等号只在分母正的定义域证明；不增加前提后声称全部原定义有效。

若全部上下文Δg=0，分母与分子均0，原文未给0/0约定。比值界和同号等号只在分母正的定义域证明；不增加前提后声称全部原定义有效。

单列定义域问题，不等于interaction性质错误。

来源：src-neurips2021-robustness-formal PDF 8, src-neurips2021-robustness-supplement PDF 8

## Nullity显示量词与双玩家定义域

记录 ID：robustness-self-pair-quantifier

原文字说other variables，但显示∀j∈N包含j=i。pair的原上下文大小范围n−2及两玩家解释要求i≠j；若硬扩成自配对，Δ(i,i,S)=g(S)−g(Si)，dummy增量非零时不为0。原量词照录，适配的i≠j是双玩家domain，不是补入以救自配对扩张。

原文字说other variables，但显示∀j∈N包含j=i。pair的原上下文大小范围n−2及两玩家解释要求i≠j；若硬扩成自配对，Δ(i,i,S)=g(S)−g(Si)，dummy增量非零时不为0。原量词照录，适配的i≠j是双玩家domain，不是补入以救自配对扩张。

仅量词/定义域歧义，双玩家nullity仍有效。

来源：src-neurips2021-robustness-supplement PDF 3

## Eq7取消后的exclusive变量误植

记录 ID：robustness-benefit-cancellation-typo

取消Xi exclusive后应留下MI(Xj;Y|Xi,XS)，原第三行却仍写Xi。下一行log分子p(xj,y|xi,xS)已经使用正确Xj。重写以四熵恒等式消去该误植，原链照录。

取消Xi exclusive后应留下MI(Xj;Y|Xi,XS)，原第三行却仍写Xi。下一行log分子p(xj,y|xi,xS)已经使用正确Xj。重写以四熵恒等式消去该误植，原链照录。

只修作者证明变量，不改Eq7原命题及co-information约定。

来源：src-neurips2021-robustness-supplement PDF 7

## 任意 DNN 的全局 Taylor 等式不成立

记录 ID：dyn-issue-taylor

原 Lemma 3 没有解析或收敛前提。

$v(t)=\max(t-1/2,0)$、基线0、输入1，是一层 ReLU 网络；在0邻域恒零，全部 Taylor 系数0，而单变量交互为1/2。

原无条件命题被反驳；有限多项式支持分组是另列的有效子结果。

来源：src-neurips2024-dynamics-formal PDF 18, src-neurips2024-dynamics-formal PDF 19

## 零交互使归一化触发无定义

记录 ID：dyn-issue-zero-trigger

原 Eq.(7) 与 Lemma 2 对所有子集使用除法而未排非空零交互。

恒定模型 $v=1$ 满足原 DNN 设置，所有非空 $I(T)=K_T=0$；对 $T\subseteq S$ 的触发是通常实数中无定义的0/0，不能约去得到1。

保留原定义域问题，非零域的归一化证明不冒充原无条件命题。

来源：src-neurips2024-dynamics-formal PDF 7, src-neurips2024-dynamics-formal PDF 19, src-neurips2024-dynamics-formal PDF 20, src-neurips2024-dynamics-formal PDF 22

## Lemma 1 的边缘律不足以给方差和

记录 ID：dyn-issue-marginal-independence

正文只有 Gaussian 边缘，附录才新增 iid。

一变量两个输出噪声共用 $Z\sim\mathcal N(0,\sigma^2)$，$\sigma>0$；全部边缘满足原条件而 $\Delta I_{\{1\}}=Z-Z=0$。PaperDynamics 的反例实际绑定 Gaussian map-law 与原交互。

均值与线性恒等式有效；iid 方差另作为带明确原附录前提的子结果。

来源：src-neurips2024-dynamics-formal PDF 7, src-neurips2024-dynamics-formal PDF 20, src-neurips2024-dynamics-formal PDF 21

## 触发缩放与 Assumption 1 是不同模型

记录 ID：dyn-issue-trigger-variance

Lemma 1 的除以权重会引入逐概念比例；输出噪声也使多个交互相关。

若 $w_{T_1}=1,w_{T_2}=2$，同一阶数的方差比例为1和1/4；不能使用同一个比例常数。

Theorem 3 可在另外明确规定的 Assumption 1 下证明；不宣称该假设由 Lemma 1 推出。

来源：src-neurips2024-dynamics-formal PDF 7, src-neurips2024-dynamics-formal PDF 8, src-neurips2024-dynamics-formal PDF 21

## Gram 行列式不是对角项乘积

记录 ID：dyn-issue-gram-determinant

原 F.4 把特征值乘积误等同对角项乘积，并把零噪声对角罚项误称正定。

一变量 zeta Gram 为 $\begin{pmatrix}2&1\\1&1\end{pmatrix}$，行列式1而对角积2；$\sigma=0$ 罚项为零。

用 Möbius 单射证明 Gram 正定，再加半正定罚项；原最优命题无需新条件。

来源：src-neurips2024-dynamics-formal PDF 22

## 大样本协方差不能替代精确期望

记录 ID：dyn-issue-expectation

原证明把样本数足够大的近似收敛作为固定样本数的等式理由。

逐行有 $E[\epsilon_T\epsilon_U]=0$（$T\ne U$）和 $E[\epsilon_T^2]=c_T$，求和恰为 $2^n\operatorname{diag}(c)$，无需行间独立或渐近。

逐行精确期望补正同一证明，Lean 直接积分平方残差。

来源：src-neurips2024-dynamics-formal PDF 21, src-neurips2024-dynamics-formal PDF 22

## 标签向量转置错误

记录 ID：dyn-issue-label-transpose

原矩阵行是遮罩、列是概念，所以标签应用 J 而非其转置。

$y_S=\sum_{T\subseteq S}w_T^*$ 正是 $(Jw^*)_S$；一变量取 $w^*=(1,2)$，$Jw^*=(1,3)$ 而 $J^\top w^*=(3,2)$。

正文 Theorem 3 的末式正确，用正确标签补正证明。

来源：src-neurips2024-dynamics-formal PDF 22

## OR 证明的激活分组边界

记录 ID：dyn-issue-or-grouping

L 与 S 不交时，T 必须仍与 S 相交，不能把空激活项放入内和。另当 L 包含 S 但 L≠N 时，原声称内和零也无效。

$N=\{1,2\},S=\{1\},L=\varnothing$：合法超集T为{1},{1,2}，激活块只取{1}，不是包括空块的二项式和。$L=S=\{1\}\ne N$ 时原内和仅一项1。

全 OR 和减去不激活和给完整同命题证明。

来源：src-neurips2024-dynamics-formal PDF 17, src-neurips2024-dynamics-formal PDF 18

## Eq.(3) 使用未定义空 AND 项

记录 ID：dyn-issue-eq3-empty

主文 Eq.(2) 只定义非空分量交互，Eq.(3) 却包含空 AND 系数。F.1 规定的是空分量输出，不是主文空交互定义。

若按通常 Möbius 公式补扩展 $I_a(\varnothing)=a(\varnothing)=b$，取常数网络 $v=1,a=1,o=0$，扩展后的 Eq.(3) 给2而原输出1；该例严格依赖此显式扩展。若约定空 AND 为0，重复消失，但主文 Eq.(2) 未给该约定。Eq.(4) 非空和正确。

记录定义域/约定缺口及条件性反例，不能无说明把辅助扩展当作原定义再宣称原式已否定。

来源：src-neurips2024-dynamics-formal PDF 3, src-neurips2024-dynamics-formal PDF 4, src-neurips2024-dynamics-formal PDF 16

## 普通交互与分量交互同名作用域

记录 ID：dyn-issue-and-scope

Appendix A 七性质以完整模型 v 的普通交互使用该符号，主文 Eq.(2) 以 v_and 分量且只对非空S定义。

两实例分别是 $I_g$ 与 $I_a$；任意拆分参数不能使 $I_a$ 单独重构完整 $g$，也不能从 $g=g_1+g_2$ 自动推出任意分量间同样关系。

七性质按普通全模型实例保留原前提并证明；符号表明确记录两个局部映射。

来源：src-neurips2024-dynamics-formal PDF 3, src-neurips2024-dynamics-formal PDF 14

## Appendix E 半模型与裸 v 记号不一致

记录 ID：dyn-issue-complement-half

原先明确两个分量等于0.5v，随后 Eq.(14)–(16) 用裸v写变换，未交代是否重新命名分量模型。

若裸v仍是同一总模型，取一变量 $v(x)=x$、基线0、输入1，原分量 OR 为1/2，Eq.(14) 裸v右端为1。若裸v指固定分量o，则负补集恒等式准确，实际Lean验证此忠实局部解释。

保留原全部式与半模型前提；精确分量补集适配是有效子结果，不无说明宣称原每行缩放一致。

来源：src-neurips2024-dynamics-formal PDF 15, src-neurips2024-dynamics-formal PDF 16

## Appendix C 的分量标签和噪声拆分符号

记录 ID：dyn-issue-split-sign

原第一段把第二个分量也标为 AND，噪声段两个分量都加 gamma。

取 $v(x_T)=1,\delta_T=0,\gamma_T=1$，两个原噪声分量均为3/2，总和3而目标输出1。

保存原录文与精确反例；不把修改过的优化定义冒充原式。

来源：src-neurips2024-dynamics-formal PDF 15

## Proposition 1 严格子句失败，一般单调性未决

记录 ID：dyn-issue-proposition1

原命题未排零噪声，且原文仅给 Figure 3 数值验证，没有一般解析证明。

$\sigma=0$ 时 $\hat M=I$，全部行范数1；例如一变量 $T=\varnothing,T\prime=\{1\}$ 的比为1而非大于1。Lean 给所有有限总体完整矩阵证明。

仅严格原子句被反驳；同阶不变与真权重独立有效，正噪声一般阶数比及噪声单调子句保留未决，有限数值不替代。

来源：src-neurips2024-dynamics-formal PDF 9, src-neurips2024-dynamics-formal PDF 23

## 补集恒等式不足以传递稀疏定理前提

记录 ID：dyn-issue-sparsity-transfer

外引稀疏界有三个游戏条件，分量分解或反向输入尚未核实这些条件。

精确的有限反演及补集变换只控制重构，不自动给最高阶零、平均单调与多项式界。

外引适配保持范围审查，不冒称原渐近界机器已证。

来源：src-neurips2024-dynamics-formal PDF 4, src-neurips2024-dynamics-formal PDF 14, src-neurips2024-dynamics-formal PDF 15, src-neurips2024-dynamics-formal PDF 16

## Eq.(46) 导数漏公共归一化

记录 ID：dyn-issue-derivative-scale

Eq.(45)损失有2^{-n}，Eq.(46)导数未带该公共因子。

真实梯度是原Eq.(46)右端乘 $2^{-n}$。该因子严格正，所以设梯度为0时得到同一正规方程；不改变唯一最优结论。

保留原导数式，重写直接精确期望和完成平方，不依赖该漏因子。

来源：src-neurips2024-dynamics-formal PDF 21

## 原排列构造未说明每步为换位

记录 ID：dyn-issue-permutation-involution

Eq.(63)之后用P_i平方为单位，但此前只称每个P_i是permutation matrix，未说明是换位矩阵。

三循环排列的平方不为单位。可以把所需有限变量排列分解为换位，各因子才满足该性质；也可直接对整体P用 $P^{-1}$ 共轭。实际Lean与重写使用正确的逆和置换。

这是缺少构造说明的证明缺口，Theorem4同阶范数结论未被否定。

来源：src-neurips2024-dynamics-formal PDF 23

## B.2第三≥子句方向错误

记录 ID：transformation-prefix-direction

常数门与Y的MI为0，扩展门$(1,Y)$与Y的MI为$\log2$。两者由X确定，因此相应co-information也是0与$\log2>0$；原附录第三≥子句不成立。原Eq11≤0和正文increase方向仍正确。

常数门与Y的MI为0，扩展门$(1,Y)$与Y的MI为$\log2$。两者由X确定，因此相应co-information也是0与$\log2>0$；原附录第三≥子句不成立。原Eq11≤0和正文increase方向仍正确。

仅该附录子句被反驳；正文Property2与Eq11方向正确。

来源：src-icml2022-transformation-formal PDF 14

## IB条件独立推理的Y作用域复用

记录 ID：transformation-ib-label-prediction

取$X=Y\sim\mathrm{Bernoulli}(1/2)$。真实权重0、偏置1的ReLU特征对两个输入都等于1。因此唯一Z条件行的实际联合律仍为$p(0,0)=p(1,1)=1/2$；完整计算$I(X;Y\mid Z)=\log2>0$。Lean显式构造单元素Z联合条件律并连接实际ReLU常值计算。

取$X=Y\sim\mathrm{Bernoulli}(1/2)$。真实权重0、偏置1的ReLU特征对两个输入都等于1。因此唯一Z条件行的实际联合律仍为$p(0,0)=p(1,1)=1/2$；完整计算$I(X;Y\mid Z)=\log2>0$。Lean显式构造单元素Z联合条件律并连接实际ReLU常值计算。

预测确定于Z的读取成立；真实标签读取被实际ReLU反例反驳。保持两种作用域及原Y符号可追溯。

来源：src-icml2022-transformation-formal PDF 2, src-icml2022-transformation-formal PDF 3, src-icml2022-transformation-formal PDF 4

## Eq24字面公式为负

记录 ID：transformation-kde-label-negative

令层权重0、偏置1，两个输入的特征均$t_i=\operatorname{ReLU}(1)=1$；类别各半。添加独立Gaussian噪声后$\widehat T=1+\epsilon$仍独立于Y，故真实MI为0。任意概率特征律下常数标签条件核的MI0计算已验证。

所有核都是1。全局项为$-\log1=0$；每类括号为$-(1/2)\log(1/2)$，再乘类权重1/2并求和。原RHS为$-(1/2)\log2<0$，既不是真实MI等式也不是其上界。反例不要求特征区分类别，源也无此要求。

令层权重0、偏置1，两个输入的特征均$t_i=\operatorname{ReLU}(1)=1$；类别各半。添加独立Gaussian噪声后$\widehat T=1+\epsilon$仍独立于Y，故真实MI为0。任意概率特征律下常数标签条件核的MI0计算已验证。

所有核都是1。全局项为$-\log1=0$；每类括号为$-(1/2)\log(1/2)$，再乘类权重1/2并求和。原RHS为$-(1/2)\log2<0$，既不是真实MI等式也不是其上界。反例不要求特征区分类别，源也无此要求。

原公式保留，反驳该字面上界/等式；实验趋势保持原经验作用域。

来源：src-icml2022-transformation-formal PDF 17

## Eq25离散门熵界反例

记录 ID：transformation-kde-discrete-bound

门为等概率0/1，真实熵$\log2$、方差1/4。因此原$\sigma_0^2=\kappa\operatorname{Var}(\Sigma)$确实为$\kappa/4$，不使用自由带宽或零方差。

每个样本核平均为$[1+\exp(-2/\kappa)]/2$。所以估计值$\log2-\log(1+\exp(-2/\kappa))$严格小于$\log2$，因为跨状态核严格正。

门为等概率0/1，真实熵$\log2$、方差1/4。因此原$\sigma_0^2=\kappa\operatorname{Var}(\Sigma)$确实为$\kappa/4$，不使用自由带宽或零方差。

每个样本核平均为$[1+\exp(-2/\kappa)]/2$。所以估计值$\log2-\log(1+\exp(-2/\kappa))$严格小于$\log2$，因为跨状态核严格正。

原公式保留，反驳该字面上界/等式；实验趋势保持原经验作用域。

来源：src-icml2022-transformation-formal PDF 17

## Eq26随机dropout门MI界反例

记录 ID：transformation-kde-randomness-bound

四个等概率$(X,B)$状态推前到$(X,\Sigma)$得到质量$1/2,0,1/4,1/4$。dropout后ReLU确实产生该门，移除dropout得到X；这符合Eq26含额外随机性的前提。

$\operatorname{Var}(\Sigma)=3/16$，故原带宽$16(3/16)=3$。真实$I(X;\Sigma)=(3/4)\log(4/3)\ge3/16$；移除采样后的二值核估计在h=3时不超过1/6，且$1/6<3/16$。

四个等概率$(X,B)$状态推前到$(X,\Sigma)$得到质量$1/2,0,1/4,1/4$。dropout后ReLU确实产生该门，移除dropout得到X；这符合Eq26含额外随机性的前提。

$\operatorname{Var}(\Sigma)=3/16$，故原带宽$16(3/16)=3$。真实$I(X;\Sigma)=(3/4)\log(4/3)\ge3/16$；移除采样后的二值核估计在h=3时不超过1/6，且$1/6<3/16$。

原公式保留，反驳该字面上界/等式；实验趋势保持原经验作用域。

来源：src-icml2022-transformation-formal PDF 17

## Eq27正规类别权重下仍非上界

记录 ID：transformation-kde-coinfo-bound

门为等概率0/1，真实熵$\log2$、方差1/4。因此原$\sigma_0^2=\kappa\operatorname{Var}(\Sigma)$确实为$\kappa/4$，不使用自由带宽或零方差。

各类只有一个门状态，自核为1，类条件KDE为$-\log1=0$。确定性给$I(\Sigma;Y\mid X)=0$，真实co-information为$I(\Sigma;Y)=\log2$。

原RHS于是退化全局二值KDE，严格小于真实$\log2$。该反例不借助一般$p_m=n_m/M$的归一化错误；该错误另列。

门为等概率0/1，真实熵$\log2$、方差1/4。因此原$\sigma_0^2=\kappa\operatorname{Var}(\Sigma)$确实为$\kappa/4$，不使用自由带宽或零方差。

各类只有一个门状态，自核为1，类条件KDE为$-\log1=0$。确定性给$I(\Sigma;Y\mid X)=0$，真实co-information为$I(\Sigma;Y)=\log2$。

原RHS于是退化全局二值KDE，严格小于真实$\log2$。该反例不借助一般$p_m=n_m/M$的归一化错误；该错误另列。

原公式保留，反驳该字面上界/等式；实验趋势保持原经验作用域。

来源：src-icml2022-transformation-formal PDF 18

## Eq29精确合成边缘乘积仍非上界

记录 ID：transformation-kde-tc-bound

真实联合律$p_{00}=p_{11}=1/2$的TC为$\log2$。合成分布在四个二值状态上均匀，确实独立且逐坐标激活率与真实门一致。向量平方方差为1/2，故h为κ/2。

令$t=\exp[-1/(2h)]>0$。对于真实00或11状态，分子为$2(1+t^2)$，分母为$1+2t+t^2=(1+t)^2$。四项相同，所以Eq29 RHS为$\log[2(1+t^2)/(1+t)^2]$。

由于$2t>0$，比值严格小于2；log单调，故原核比上界严格小于真实TC=$\log2$。这是精确有限样本和精确边缘乘积，不是合成分布Monte Carlo误差。

真实联合律$p_{00}=p_{11}=1/2$的TC为$\log2$。合成分布在四个二值状态上均匀，确实独立且逐坐标激活率与真实门一致。向量平方方差为1/2，故h为κ/2。

令$t=\exp[-1/(2h)]>0$。对于真实00或11状态，分子为$2(1+t^2)$，分母为$1+2t+t^2=(1+t)^2$。四项相同，所以Eq29 RHS为$\log[2(1+t^2)/(1+t)^2]$。

由于$2t>0$，比值严格小于2；log单调，故原核比上界严格小于真实TC=$\log2$。这是精确有限样本和精确边缘乘积，不是合成分布Monte Carlo误差。

原公式保留，反驳该字面上界/等式；实验趋势保持原经验作用域。

来源：src-icml2022-transformation-formal PDF 18

## Eq27后的类别权重未归一化

记录 ID：transformation-class-weights

$\sum_mn_m=n$，所以$\sum_mp_m=n/M$，一般不是1；Eq24此前$p_l=P_l/P$正规。

$\sum_mn_m=n$，所以$\sum_mp_m=n/M$，一般不是1；Eq24此前$p_l=P_l/P$正规。

另列权重定义错误；Eq27反例即使n=M也成立。

来源：src-icml2022-transformation-formal PDF 18

## 连续近似Langevin更新的正值域边界

记录 ID：transformation-ebm-domain

添加Gaussian噪声给原更新算法，但有限步是否采到目标EBM没有在此证明。线性先验在s∈[0,1]且0<p̂<1时正，未约束Gaussian步可离开该域；例如p̂=3/4,s=−1时q=−1/4。这是具体域边界，不是否定作者已给的sigmoid松弛。

添加Gaussian噪声给原更新算法，但有限步是否采到目标EBM没有在此证明。线性先验在s∈[0,1]且0<p̂<1时正，未约束Gaussian步可离开该域；例如p̂=3/4,s=−1时q=−1/4。这是具体域边界，不是否定作者已给的sigmoid松弛。

作者已给sigmoid/Swish连续近似；需区分其正值域与未约束Gaussian采样状态。

来源：src-icml2022-transformation-formal PDF 19, src-icml2022-transformation-formal PDF 20

## 平均激活率不决定C

记录 ID：transformation-activation-average

$(1/2,1/2)$与$(0,1)$平均率都是1/2，但$C$分别2log2与0。因此PDF5由平均率收敛推出roughly constant不能仅由均值成立。此反例不否定PDF15逐坐标相似$a_l^d$或PDF6逐维实验。

$(1/2,1/2)$与$(0,1)$平均率都是1/2，但$C$分别2log2与0。因此PDF5由平均率收敛推出roughly constant不能仅由均值成立。此反例不否定PDF15逐坐标相似$a_l^d$或PDF6逐维实验。

只限定PDF5从跨维平均率到rough constant的推断，不否定逐坐标条件或精确Eq2/16。

来源：src-icml2022-transformation-formal PDF 5

## Eq34与35复用L但符号相反

记录 ID：transformation-mle-sign

原Eq34用L作正log最大化，Eq35/36用同名L作负log最小化/梯度。重写以负log损失为准，原式原样保留。

原Eq34用L作正log最大化，Eq35/36用同名L作负log最小化/梯度。重写以负log损失为准，原式原样保留。

优化目的可等价表达，但同名L的定义需区分。

来源：src-icml2022-transformation-formal PDF 19

## B.2第二子句重复Σ1

记录 ID：transformation-prefix-index

原第二bullet末索引印Σ1，而其证明Eq9完整使用Σl。重写按本条前缀作用域Σ1:l修下标；不修改原转录。

原第二bullet末索引印Σ1，而其证明Eq9完整使用Σl。重写按本条前缀作用域Σ1:l修下标；不修改原转录。

下标勘误；不改变正确前缀输入MI命题的作用域。

来源：src-icml2022-transformation-formal PDF 14

## 正文Swish等号需按原prose解释为近似

记录 ID：transformation-swish-equality

正文明确说can be approximated，但显示式写=；有限β且x=1时sigmoid(β)<1，所以不是精确ReLU值1。附录Eq41正确保留≈；重写导数属于连续近似本身。

正文明确说can be approximated，但显示式写=；有限β且x=1时sigmoid(β)<1，所以不是精确ReLU值1。附录Eq41正确保留≈；重写导数属于连续近似本身。

保留正文原等号和附录≈；不把平滑门当成硬门精确恒等式。

来源：src-icml2022-transformation-formal PDF 8, src-icml2022-transformation-formal PDF 20

## Appendix A门矩阵维度与池化下标笔误

记录 ID：transformation-gate-matrix-index

ReLU/dropout对象明确是D×D对角矩阵，却写属于{0,1}^D，向量是其对角值。池化选择条件写(h_l)_{d′}最大，却要定义行d′列d；应按窗口内输入索引d选择最大者。若最大值并列，需选择一个最大者，不能让多个1把值相加。

ReLU/dropout对象明确是D×D对角矩阵，却写属于{0,1}^D，向量是其对角值。池化选择条件写(h_l)_{d′}最大，却要定义行d′列d；应按窗口内输入索引d选择最大者。若最大值并列，需选择一个最大者，不能让多个1把值相加。

原文原样保留，固定门算子的维度与一个最大者选择在重写定义澄清；真实ReLU Eq1证明不受影响。

来源：src-icml2022-transformation-formal PDF 13

## 任意 DNN 的全局 Taylor 等式错误

记录 ID：bnn-issue-taylor

原Lemma2.1未给解析、收敛与合法分组条件。

允许的ReLU网络 $v(t)=\max(t-1/2,0)$，参考0输入1：所有基线Taylor系数零而交互1/2。人读反例完整；Lean只验证有效有限多项式子结果。

不修改原量词；有限多项式支持证明与原错误命题明确分开。

来源：src-icml2023-bayesian-formal PDF 5, src-icml2023-bayesian-formal PDF 15, src-icml2023-bayesian-formal PDF 16

## 奇次绝对触发的精确矩不等于有符号矩

记录 ID：bnn-issue-folded-moments

原Theorem2.3的J定义为绝对幂，而印出的均值/方差公式使用有符号Gaussian幂；正文虽明确忽略低概率越界，精确未截断等式仍不成立。

一坐标$x=1,r=0,\tau=1,\pi=1,\epsilon\sim N(0,q)$，任意$q>0$：原J均值严格大于1，有符号均值1。PaperBayesian.general_moment_counterexample实际绑定原触发定义与Gaussian积分。平方相同还给真实方差小于q。

该反例针对J，不否定真实最低交互的符号相消；Theorem2.4下界用独立乘积与绝对矩下界重新证明。

来源：src-icml2023-bayesian-formal PDF 5, src-icml2023-bayesian-formal PDF 6, src-icml2023-bayesian-formal PDF 17, src-icml2023-bayesian-formal PDF 18

## 移动符号系数与固定参考幅值的记号作用域

记录 ID：bnn-issue-moving-coefficient

Lemma的U定义含当前x′符号，但最低项矩式与附录证明又把U及δ按参考x取固定系数；二者不能无说明混同。

真实最低多项式I=a∏(x_i′−r_i)可以跨符号区精确因式分解为U_ref∏(1+s_iε_i/τ)。这里U_ref=I(x)是固定基点值；U(x′)与J_abs(x′)配对才恢复同一I。

提供忠实参考系数解释和完整实际交互证明；不将固定U×absJ反例误报成Theorem2.2真实I反例。

来源：src-icml2023-bayesian-formal PDF 5, src-icml2023-bayesian-formal PDF 6, src-icml2023-bayesian-formal PDF 15, src-icml2023-bayesian-formal PDF 16, src-icml2023-bayesian-formal PDF 17

## 零参考交互使触发比值无定义

记录 ID：bnn-issue-zero-trigger

作者没有排除精确为零的参考交互，定义及二值约去都会使用该分母。

允许的常数网络v=1所有非空I=0，原归一化分子也0，得到通常实数中无定义的0/0。实际有限掩码支持律仍成立，但不能除以0。

保留源定义域缺口；非零域的真实掩码声明只记有效适配，不覆盖原所有零系数。

来源：src-icml2023-bayesian-formal PDF 7

## 增长比的空支持与零噪声边界

记录 ID：bnn-issue-growth-domain

严格包含本身不排空旧支持，原Gaussian参数也未在该条排零噪声；这些比值需要非零方差。

S为空时J_S=1；σ=0时全部坐标扰动0、所有J恒1，所以相应方差为0。有效域S非空、σ>0时，Gaussian无原子与整数幂证明方差正，完整增长主干已实际形式化。

不将边界无定义升级为有效正噪声比较被否定，不把Lean总除法0当作作者约定。

来源：src-icml2023-bayesian-formal PDF 6, src-icml2023-bayesian-formal PDF 18, src-icml2023-bayesian-formal PDF 19, src-icml2023-bayesian-formal PDF 20

## 特征方差与交互尺度比值的零域

记录 ID：bnn-issue-regression-domain

原回归比例未排零特征方差，缩放界也未排零U导致的零交互方差。

C1=C2=1,y*=1时独立常数特征损失(y*−U1−U2)^2有整条最优直线，而EC/VarC=1/0无定义。缩放若U=0，则I=0且VarI=0。

真实期望损失的唯一全局最优已在正方差域证明；该条件不被隐藏为无条件原命题的机器证明。

来源：src-icml2023-bayesian-formal PDF 7, src-icml2023-bayesian-formal PDF 8, src-icml2023-bayesian-formal PDF 20, src-icml2023-bayesian-formal PDF 21, src-icml2023-bayesian-formal PDF 22

## 显著和缺激活条件且小残差未量化

记录 ID：bnn-issue-salient-activation

Eq5不同于Eq4，实际未写S⊆T，且“小”没有误差界；原式保留。

真实单变量线性掩码得分c>0，空输出0而显著单例交互和c，残差−c。PaperBayesian.salient_empty_mask绑定真实掩码得分和交互和，但只证明该精确代数事实，不冒充未量化近似命题的机器反例。

正确残差需同时计遗漏激活项与纳入的未激活项；没有统一小尾界时不证明小残差。

来源：src-icml2023-bayesian-formal PDF 3, src-icml2023-bayesian-formal PDF 4

## 外引稀疏与对抗关系未给完整本地适配

记录 ID：bnn-issue-sparsity-adaptation

外引技术前提不在本篇完整陈述；Appendix D代数分量关系不能自动转移所有对抗脆弱性结论。

有限重构可产生密集游戏；多阶上下文平均混合多种概念阶数。已证明的差分分解仅是准确有限代数适配。

保留外引与经验角色；不将条件库引理算成整篇无前提原结论。

来源：src-icml2023-bayesian-formal PDF 3, src-icml2023-bayesian-formal PDF 12, src-icml2023-bayesian-formal PDF 13

## 两端界下降不单独推出中间量阶数单调

记录 ID：bnn-issue-order-inference

源文保持approximately consider措辞；精确缩放界与后续近似推论是不同证明义务。

Amin=.1,Amax=.2，KI为10、9，|U|分别.1、.2时，两端界下降但KC从1升至1.8。该逻辑例未声称完整BNN模型反例。

整体阶数倾向还依赖近似模型、单项式到任意叠加的适配及经验数据。

来源：src-icml2023-bayesian-formal PDF 8

## 掩码零坐标的零次幂不能判为零

记录 ID：bnn-issue-zero-degree

原G1在未限制π_i>0时把所有掩码零坐标幂写成0。

π_i=0时通常多项式约定0^0=1；正确筛选只删除支持包含某个未保留正次数变量的项。

有限支持证明按严格正次数消去；不改原式，也不把该步骤修复当作任意DNN全局Taylor成立。

来源：src-icml2023-bayesian-formal PDF 15

## 单项方差到整个交互缺少协方差控制

记录 ID：bnn-issue-superposition

作者由单个绝对触发的支持增长及系数通常chaotic，粗略推出整个交互随阶数增长；没有系数概率律、交叉协方差或统一幅值前提。

有限L2和的真实方差包含 $\sum_{\pi,\rho}c_\pi c_\rho\operatorname{Cov}(J_\pi,J_\rho)$；同输入上的重叠次数触发不自动独立，移动符号系数也不能当固定数移出积分。

保留原近似措辞及其完整论述；有效单项增长证明不升级为任意Taylor和的统一跨阶结论。

来源：src-icml2023-bayesian-formal PDF 6

## 任意 DNN 的全局 Taylor 展开失败

记录 ID：diff-issue-taylor

作者未要求解析性、全局收敛或所有掩码上的合法展开。

一维ReLU v(t)=max(t−1/2,0)，r0,x1，全部Taylor系数零而单例交互1/2。人读网络反例完整；Lean只验证真实有限多项式支持子结果。

不把有限多项式机器类型扩成任意DNN原量词。

来源：src-neurips2023-difficulty-formal PDF 4, src-neurips2023-difficulty-formal PDF 17, src-neurips2023-difficulty-formal PDF 18

## 最低阶 J 自身的均值和方差错式

记录 ID：diff-issue-lowest-absolute

原对象J含绝对增量；小Gaussian不会几乎处处保持符号。

单支持、τ1、ε~N(0,q),q>0时J=|1+ε|。实际Lean证明EJ>1及VarJ<q，完整原对象、真实法则和两个矩都已绑定。

与F08及本篇G2显示的有符号最低I矩区分；这里只否定正文J精确子句，不由此否定附录I变体。

来源：src-neurips2023-difficulty-formal PDF 5, src-neurips2023-difficulty-formal PDF 18, src-neurips2023-difficulty-formal PDF 19

## 最低阶主文 J 与附录 I 的原陈述差异

记录 ID：diff-issue-main-appendix-lowest

正文Eq5写J自身矩；G2重述prose仍说J，显示式却为I并带U。Theorem2定义的U还含随x′变动的符号。

原两个版本均完整保留。真实最低单项式的固定参考U矩已用actual maskedLowest及Gaussian法则形式化；空支持的固定输出基线另证均值b、方差0。

不把主文folded反例扩大为附录signed I错误，也不将最低单项式类型扩大为任意DNN完整I。

来源：src-neurips2023-difficulty-formal PDF 4, src-neurips2023-difficulty-formal PDF 5, src-neurips2023-difficulty-formal PDF 18, src-neurips2023-difficulty-formal PDF 19

## 一般次数的绝对幂不能全改有符号幂

记录 ID：diff-issue-general-absolute

奇次幂在越过参考时与绝对幂不同，≪τ只为近似。

π1=1复用实际最低J均值/方差反例。正确folded乘积矩有实际Gaussian L2和独立法则证明；偶数幂子域绝对值可消去。

不将错误奇次子句扩大为所有整数次数错误。

来源：src-neurips2023-difficulty-formal PDF 5, src-neurips2023-difficulty-formal PDF 19

## Proposition1 方差项被再次平方

记录 ID：diff-issue-product-variance-square

原声明方差平方，下一Eq12却使用正确方差一次。

真实k1 GaussianX~N(0,2)：VarX=2，打印右式4；机器绑定实际积分及方差。原乘积均值仍有效。

公共正确product_variance不替换原Proposition。

来源：src-neurips2023-difficulty-formal PDF 18

## 零参考交互的触发商无定义

记录 ID：diff-issue-zero-reference

作者未排U_S=0，二值短证明直接约分。

常数网络全部非空参考交互0；原商0/0，若当前交互变非零则不能固定零U表达。κ实际反例两个U非零，避开此域。

有效非零域的掩码/线性适配已证明，但不隐去源零域。

来源：src-neurips2023-difficulty-formal PDF 5, src-neurips2023-difficulty-formal PDF 6, src-neurips2023-difficulty-formal PDF 7, src-neurips2023-difficulty-formal PDF 20

## G3 不触发分支的包含方向错

记录 ID：diff-issue-binary-inclusion

严格包含S⊊T不允许找到S\T元素。

正确分支是S不包含于T；真实maskedGame支持律不依赖此错步。

只修证明步骤，保留Theorem4原陈述及零U范围。

来源：src-neurips2023-difficulty-formal PDF 20

## 输入 r_i 与 b_i 局部切换

记录 ID：diff-issue-reference-notation

Eq21/24局部输入参考符号切换，需说明同一基线。

原作者式原样保留；重写一致用r_i并与输出基线b区分。

不由记号笔误单独否定非零域的二值结论。

来源：src-neurips2023-difficulty-formal PDF 17, src-neurips2023-difficulty-formal PDF 20

## 原 Eq25 内和错用 |L|=m

记录 ID：diff-issue-multiorder-final-index

按l分组内层应|L|=l，打印最终等式不是正确关系。

真实N3, v=z1z2, x1,r0,m1：实际上下文平均1，打印右式0；实际Lean maskedPolynomial反例。

不得把修过下标的公式标成原等式已证。

来源：src-neurips2023-difficulty-formal PDF 21

## 原 Eq25 包含上下文的计数错误

记录 ID：diff-issue-multiorder-coefficient

固定l个变量后应从剩余n−2−l变量选m−l。

实际N4,v=z1z2z3,m2平均1，修内层但保留原系数时右式2。第二机器反例独立验证。

公共一般上下文计数与l分组恒等式及论文n−2适配已机器完成，原最后错误式仍由两个反例分别否定。

来源：src-neurips2023-difficulty-formal PDF 21

## G5 Step3 省掉特征均值

记录 ID：diff-issue-regression-mean

Step2含μ_i，不能在跨特征比较无条件删除。

真实独立Gaussian μ=(1,2),双方差1,y1，唯一最优(1/6,1/3)，比1/2而逆方差比1。Σ=Σ²=I使记号读法一致。

保留有效期望损失、正规方程与唯一最优；Step2须按真实方差读法及非零分母限定，主反例专门反驳Step3。

来源：src-neurips2023-difficulty-formal PDF 21

## Σ 与 Σ² 的方差记号冲突

记录 ID：diff-issue-covariance-square

字面读法真实方差σ_i^4，后文比例使用σ_i²；故Step2也只能在将σ_i²解释真实方差d_i时与有效公式一致。

原式保留；规范真实方差d_i。主反例取两方差1，在两个读法都否定丢μ。

不无说明将原Σ²替换成diag真实方差。

来源：src-neurips2023-difficulty-formal PDF 21

## 跨数据不能约去变化的 |U_x|

记录 ID：diff-issue-kappa-cancellation

逐样本I=U_xC_x只给加权比值，U_x随参考x变化。

标准化数据±1,均值0,τ1,r0,单ReLU max(t+1/2,0),b1/2；完整Gaussian明确σ，实际单例I及literal C积分给κ_I>κ_C。全部前提实际编译。

原等号被原模型反例否定，指标I定义本身仍保留。

来源：src-neurips2023-difficulty-formal PDF 7

## chaotic 系数未控制整体协方差

记录 ID：diff-issue-superposition

单项J方差增长与加权I增长有额外协方差、幅值与移动系数条件。

完整有限和方差有所有交叉协方差；源未给删除它们的定量前提。

保留roughly近似解释，不伪造精确普遍结论。

来源：src-neurips2023-difficulty-formal PDF 5

## 条件外引与学习机制解释的缺失桥梁

记录 ID：diff-issue-external-learning

完整外引前提、学习率模型与不同频率对象的适配未在本篇给出。

每条人读证明明确其实际源前提和所缺桥梁；Xu段为样本空间/损失景观频率，不能套F06中间特征DFT。

不将经验/未量化解释加强成通用Lean定理，也不宣称完整外引定理被否定。

来源：src-neurips2023-difficulty-formal PDF 3, src-neurips2023-difficulty-formal PDF 4, src-neurips2023-difficulty-formal PDF 6, src-neurips2023-difficulty-formal PDF 7, src-neurips2023-difficulty-formal PDF 8, src-neurips2023-difficulty-formal PDF 9, src-neurips2023-difficulty-formal PDF 10

## 标准差、幅值和上下文平均的零域

记录 ID：diff-issue-zero-metrics

源未统一指定零标准差、零平均幅值、零Jaccard并集及无上下文平均的赋值。

常数交互给标准差0；全零概念给幅值0和Jaccard0/0；m>n−2无合法上下文。τ0亦使原J除法无定义。

所有有效条件范围明确保留，不用Lean的总运算约定替作者补定义。

来源：src-neurips2023-difficulty-formal PDF 5, src-neurips2023-difficulty-formal PDF 7, src-neurips2023-difficulty-formal PDF 8, src-neurips2023-difficulty-formal PDF 9, src-neurips2023-difficulty-formal PDF 16, src-neurips2023-difficulty-formal PDF 21

## 原几何/R/χ/τ商的零分母

记录 ID：decoder-issue-quotient-domain

θ=0或频率同坐标时，普通商0/0；χ完整和包含这些频率，不能排除必要项。有限和保留合法值n或K。

θ=0或频率同坐标时，普通商0/0；χ完整和包含这些频率，不能排除必要项。有限和保留合法值n或K。

全称商域问题；不否定有限DFT传播。

来源：src-icml2023-decoder-formal PDF 4, src-icml2023-decoder-formal PDF 5, src-icml2023-decoder-formal PDF 6, src-icml2023-decoder-formal PDF 11, src-icml2023-decoder-formal PDF 17, src-icml2023-decoder-formal PDF 20, src-icml2023-decoder-formal PDF 23

## Eq17正弦项数漏一项

记录 ID：decoder-issue-valid-count

M=N=3,K=2,u=v=0,u′=v′=1给正确有限和0、原式−1/9，两个分母都非0。原相位使用项数减1，恰为M−K与N−K，本身正确；错误仅正弦分子项数。

M=N=3,K=2,u=v=0,u′=v′=1给正确有限和0、原式−1/9，两个分母都非0。原相位使用项数减1，恰为M−K与N−K，本身正确；错误仅正弦分子项数。

仅无padding Eq17子式错误；circle Thm3.2不受牵连。

来源：src-icml2023-decoder-formal PDF 13

## A.2额外MN与层索引

记录 ID：decoder-issue-cascade-typos

正文β=MN乘全括号正确；A2末展开一行内多MN并把若干T层上标写l，逐层仿射归纳给正确同一命题。

正文β=MN乘全括号正确；A2末展开一行内多MN并把若干T层上标写l，逐层仿射归纳给正确同一命题。

修局部证明，不改正文Cor3.3。

来源：src-icml2023-decoder-formal PDF 14

## A.3 Eq24局部共轭遗漏

记录 ID：decoder-issue-backprop-bars

Eq24第一行g微分未带bar，第二行带bar；正文Eq5图上共轭完整，作者CR梯度约定从实梯度解释，不能把标准Wirtinger因子单独当原终式反例。

Eq24第一行g微分未带bar，第二行带bar；正文Eq5图上共轭完整，作者CR梯度约定从实梯度解释，不能把标准Wirtinger因子单独当原终式反例。

局部证明共轭修复；完整真实loss矩阵链现已实际验证。

来源：src-icml2023-decoder-formal PDF 17

## A.3漏输出通道求和及转置维度标注

记录 ID：decoder-issue-backprop-channel-shape

PDF17前层标量梯度左侧没有d，右侧却固定d且没有Σ_d，必须对全部输出通道求和。Eq22前文字把对(T的共轭转置)的导数标成D×C，实际g共轭列(C)与loss行(D)外积为C×D；T本身为D×C。重写从真实空间伴随和显式通道求和推导，不改变正确Eq23/正文Eq5矩阵终式。

PDF17前层标量梯度左侧没有d，右侧却固定d且没有Σ_d，必须对全部输出通道求和。Eq22前文字把对(T的共轭转置)的导数标成D×C，实际g共轭列(C)与loss行(D)外积为C×D；T本身为D×C。重写从真实空间伴随和显式通道求和推导，不改变正确Eq23/正文Eq5矩阵终式。

仅局部证明漏和/维度注修复，原完整矩阵更新命题不被此问题否定。

来源：src-icml2023-decoder-formal PDF 17

## 实Gaussian误写零复伪协方差

记录 ID：decoder-issue-real-gaussian-cast

实Gaussian复嵌入实际C(W)=σ²，非零方差时不是0；实际独立实线性组合得到原Eq27的C(T)=σ²R2u2v。

实Gaussian复嵌入实际C(W)=σ²，非零方差时不是0；实际独立实线性组合得到原Eq27的C(T)=σ²R2u2v。

原Eq27最终矩结论正确，错误在中间圆对称替换。

来源：src-icml2023-decoder-formal PDF 19, src-icml2023-decoder-formal PDF 20

## 显示一阶矩不足SOM乘积分解

记录 ID：decoder-issue-weak-independence

U与BU两Gaussian边缘满足显示一阶式但平方模乘积矩3≠1；多通道同列交叉矩也不在d≠d′且c≠c′的显示域。

U与BU两Gaussian边缘满足显示一阶式但平方模乘积矩3≠1；多通道同列交叉矩也不在d≠d′且c≠c′的显示域。

区分弱显示式与prose真正独立模型，后者可证明。

来源：src-icml2023-decoder-formal PDF 5, src-icml2023-decoder-formal PDF 18, src-icml2023-decoder-formal PDF 19, src-icml2023-decoder-formal PDF 21, src-icml2023-decoder-formal PDF 22

## K增大时SOM可下降

记录 ID：decoder-issue-kernel-growth

M=N=8,f=(4,0),μ1,σ²1/16，K1矩17/16而K2矩1/4；R随真实K改变。

M=N=8,f=(4,0),μ1,σ²1/16，K1矩17/16而K2矩1/4；R随真实K改变。

只反驳四参数列表的K全称子句。

来源：src-icml2023-decoder-formal PDF 5

## 实际独立GaussianSOM随深度下降

记录 ID：decoder-issue-depth-growth

真实独立N(0,1/4)、K1层响应给SOM=(1/4)^L，f=(1,1)也成立，正弦分母非0。

真实独立N(0,1/4)、K1层响应给SOM=(1/4)^L，f=(1,1)也成立，正弦分母非0。

否定无条件增加，保留正确product/log公式。

来源：src-icml2023-decoder-formal PDF 5, src-icml2023-decoder-formal PDF 21, src-icml2023-decoder-formal PDF 22

## 大核可加剧原频率不均衡

记录 ID：decoder-issue-large-k-imbalance

M=N8,μ=σ²=1，K2与4的DC/(4,0)矩比5→17。

M=N8,μ=σ²=1，K2与4的DC/(4,0)矩比5→17。

解释子句缺条件，不否定核矩公式。

来源：src-icml2023-decoder-formal PDF 6, src-icml2023-decoder-formal PDF 27

## Eq8遗漏两条边带

记录 ID：decoder-issue-padding-definition

打印零分支把m越界与n越界合取，只覆盖右下角；原文字edge-padding还需要两边带0。保留原打印条件，用原文字otherwise0定义算子。

打印零分支把m越界与n越界合取，只覆盖右下角；原文字edge-padding还需要两边带0。保留原打印条件，用原文字otherwise0定义算子。

定义排版域修复，与像素相关反例分开。

来源：src-icml2023-decoder-formal PDF 6

## 边缘Gaussian不足padding矩等式

记录 ID：decoder-issue-padding-iid

四像素同一U~N(0,q)，2×2补3×3，f11旧谱0新谱U(1+z)²，SOM差q而a0右边0。实际全源条件满足，原proof额外iid未加进命题。

四像素同一U~N(0,q)，2×2补3×3，f11旧谱0新谱U(1+z)²，SOM差q而a0右边0。实际全源条件满足，原proof额外iid未加进命题。

原非DC子句反例，DC相等仍正确。

来源：src-icml2023-decoder-formal PDF 6, src-icml2023-decoder-formal PDF 22, src-icml2023-decoder-formal PDF 23

## 移位设置不总减第一个幅值

记录 ID：decoder-issue-phase-magnitude

α3,φ0满足原α>0,φ<π/2但|1−A|2>1。

α3,φ0满足原α>0,φ<π/2但|1−A|2>1。

只影响设置的幅值解释；真实一步反例另取合法α1/4。

来源：src-icml2023-decoder-formal PDF 6, src-icml2023-decoder-formal PDF 7

## 满足43–46的真实网络仍一步非零loss

记录 ID：decoder-issue-one-step

两层identity2×2核、4×4δ输入、f01/f10、α1/4满足λ1=λ2=1、φ0、两层响应1和bypass和2。真实两层实梯度(0,−2α,2α,0)，任意η>0后Im H10=−2c(1+c)≠0。

两层identity2×2核、4×4δ输入、f01/f10、α1/4满足λ1=λ2=1、φ0、两层响应1和bypass和2。真实两层实梯度(0,−2α,2α,0)，任意η>0后Im H10=−2c(1+c)≠0。

精确一步零loss子句被反驳；不牵连DFT传播与矩定理。

来源：src-icml2023-decoder-formal PDF 7, src-icml2023-decoder-formal PDF 24, src-icml2023-decoder-formal PDF 25, src-icml2023-decoder-formal PDF 26

## Eq56归一化与Eq57自指

记录 ID：decoder-issue-gradient-norm

q=(MN)−1正相位DFT时Parseval给Σr²=MNΣ|q|²；Eq57中间印η√||ΔW||²应是梯度范数链。

q=(MN)−1正相位DFT时Parseval给Σr²=MNΣ|q|²；Eq57中间印η√||ΔW||²应是梯度范数链。

局部尺度/排版修复不挽救原精确一步命题。

来源：src-icml2023-decoder-formal PDF 26

## 未编号频率/训练推断的条件范围

记录 ID：decoder-issue-inference-scope

B1–4、main8、C6/C7从矩、输入幅值、层积或低Pearson相关推出训练/概率结论，原没有补齐响应下界、联合随机模型或概率量化。原完整作者链各条保留。

B1–4、main8、C6/C7从矩、输入幅值、层积或低Pearson相关推出训练/概率结论，原没有补齐响应下界、联合随机模型或概率量化。原完整作者链各条保留。

精确恒等式、条件比较、未量化解释分开，不把所有issue叫整定理错误。

来源：src-icml2023-decoder-formal PDF 6, src-icml2023-decoder-formal PDF 8, src-icml2023-decoder-formal PDF 25, src-icml2023-decoder-formal PDF 26, src-icml2023-decoder-formal PDF 27, src-icml2023-decoder-formal PDF 32, src-icml2023-decoder-formal PDF 33

## Table7若沿用相邻概率输出尺度，则数值不相容；本节未说明尺度变化

记录 ID：cvpr-issue-bow-table7-probability-scale

正式p17脚注在Table6相邻例子写In this example，采用概率输出；p18Table7有单变量6.568和二变量−13.481。若Table7继续使用这一概率尺度，原Möbius差分分别受[−1,1]及[−2,2]限制，故两表值与该定义不能同时成立。但是该脚注没有无歧义声明延续到Table7，原本节也未说明尺度是否变化；这里不无条件判表数据已证伪。正式PNG已实际查看，排除了文本提取误差。

\[v(x_S)=p(y=\text{positive sentiment}\mid x_S)\quad\text{(p17: In this example)},\qquad w_{\{\mathrm{smart}\}}=6.568,\quad w_{\{\mathrm{not},\mathrm{smart}\}}=-13.481\quad\text{(Table7)}\]

来源：src-cvpr2023-supplement PDF 17, src-cvpr2023-supplement PDF 18
