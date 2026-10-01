# ICLR 2024 Sparse：原式问题与影响范围

最新用户允许“直接修正原文错误证明，标注错误地方；不能修正命题，命题错单独列出”。本报告严格区分证明错误与原陈述反例；仅证明修复授权为 `proof_only_granted`，原命题修改未授权。

## Lemma3行列式消元漏余子式符号

ID：`sparse-issue-determinant-sign`；类别：`source_proof_error`；正式 PDF 页：18。

\[D\prod_{k=1}^M\binom nk=1,\quad D=(\prod_{k=1}^M\binom nk)^{-1}\]

取n=3,M=2，Eq31的矩阵为[[1,2],[1,1]]，行列式−1。Eq32沿首列展开漏(−1)^(M+1)，重复后应有(−1)^(M(M−1)/2)。这只改变非零行列式的符号，不推翻满列秩命题。

**影响范围：** Eq33–36的精确值；Lemma3最终零空间结论保持，已授权修中间证明。

## Beta定义指数方向与后续值不一致

ID：`sparse-issue-beta-exponent`；类别：`source_proof_error`；正式 PDF 页：22。

\[B(p,q)=\int_0^1x^{p-1}(1-x)^{1-q}\,dx\]

正式图像确写1−q。取p=1,q=2，右侧为发散积分；随后给B(1,2)=1/2。修证明可用有限组合计数，不改Shapley/SII/STI命题。

**影响范围：** 证明工具定义及后续积分路线；非三个最终指标恒等式的反例。

## Shapley等证明的L=∅零参数边界未处理

ID：`sparse-issue-beta-empty-L`；类别：`source_proof_error`；正式 PDF 页：22, 23, 24, 26, 27。

\[B(n-|L|-k,|L|+k),\qquad |L|\int_0^1(1-x)^{|L|-1}\,dx=1\]

允许L=∅且k=0时调用B(n,0)，违反刚声明的正参数域。|L|=0时标①的被积函数在(0,1)为0，不能统一写成1；原离散权重项本身有限，需独立处理边界。

**影响范围：** 权重化简路线的空集分支；最终公式可以不改，使用共享修复证明。

## Lemma1的一般无限Taylor恒等式缺少有效性前提

ID：`sparse-issue-taylor-validity`；类别：`source_statement_counterexample`；正式 PDF 页：5, 15, 16。

\[v(x_S)=\sum_{\kappa\in\mathbb N^n}\frac{D^\kappa v(b)}{\kappa!}(x_S-b)^\kappa\]

原文仅说适用于continuously differentiable functions，Lemma1本身未假设解析性或Taylor级数等于函数。n=1,b=0,x=1，取v(t)=exp(−1/t²)（t≠0），v(0)=0。此函数C∞，所有在0的导数为0，但I({1})=e^(−1)≠0，而Eq8右边为0。反例针对一般Lemma1，不满足全空间高阶导数为零，故不直接否定1β⇒1α。

**影响范围：** 一般Lemma1与无限展开Eq2/11不能无条件修复；不能补解析性后冒充原命题。

## Lemma1掩码幂式漏κ_i>0条件

ID：`sparse-issue-zero-power`；类别：`source_proof_error`；正式 PDF 页：16。

\[\forall i\notin S,\ [(x_S)_i-b_i]^{\kappa_i}=0\]

κ_i=0时该式为0^0=1（Taylor单项式约定），不是0。后续PS过滤实际只需“若κ_i>0则项为零”，可修证明中间解释；不改PS或最终目标。

**影响范围：** p16关于零项的单句；与一般Taylor有效性缺口是两个独立问题。

## Theorem2原路线未处理ū(1)=0

ID：`sparse-issue-theorem2-zero-output`；类别：`source_proof_error`；正式 PDF 页：19。

\[A^{(k)}/\bar u^{(1)}\]

取所有掩码u(S)=0，三条假设均满足，但Eq41除以0。此反例只否定原证明步骤：最终等式乘ū(1)=0仍可成立，不能据此宣布Theorem2是假。修路线应处理全零分支，不能增添ū(1)>0假设。

**影响范围：** n进制构造步骤；正确的零平均分支已在项目重写中完整补齐；不从均值零推逐点输出零。

## Theorem2原构造G可为空

ID：`sparse-issue-theorem2-empty-G`；类别：`source_proof_error`；正式 PDF 页：19, 20。

\[G=\{k:1\le k\le M,q^{(k)}\ge\lfloor p\rfloor\},\quad\delta=\max_{k\in G}\delta^{(k)}\]

n=3,M=1,p=2，u(S)=|S|满足三假设，ū(1)=1,A(1)=3，n进制最高次数q(1)=1≤floor(p)−1，故G为空。原最大值与k*不存在；Lemma3不能制造原构造全零λ以外的λ。最终存在式或有另一构造，此为路线缺口而非最终结论反例。

**影响范围：** δ,k*构造及Eq50调用；不能仅补G非空。

## Theorem2调用Lemma2的m范围不足

ID：`sparse-issue-theorem2-m0-range`；类别：`source_proof_error`；正式 PDF 页：20。

\[m_0\in\{n,n-1,\ldots,n-M\},\qquad (40)\text{ only for }M\le m\le n\]

当M<n<2M时n−M<M，Lemma3取得的非零行可能不在Eq40已陈述范围。平均公式本身可对所有m扩展（k>m的组合数为0），属于证明补全而非新增数学假设。

**影响范围：** Eq51的前提引用。

## p∈(0,1)时低位下标书写未定义

ID：`sparse-issue-theorem2-p-under-one`；类别：`statement_notation_scope_issue`；正式 PDF 页：7, 19。

\[a_{\lfloor p\rfloor-1}^{(k)}n^{\lfloor p\rfloor-1}+\cdots+a_0^{(k)}\]

p>0允许p<1；floor(p)−1=−1，而正文只定义非负进制位、常数位。作者实验包含约0.9值，不能擅补p≥1。规范求和读作有限族J={i∈ℕ:i<floor(p)}时该族为空；若继续保留额外显示的a0项，全部低位取0的同一见证也成立。项目给任意有限低位族的统一构造，覆盖这两种常规读法，无须添加p≥1。原省略号书写问题仍保留，不声称原式逐字定义了负指标。

**影响范围：** 原定理的索引族须明确，保留原式。

## 完全抵消与空阶下η除法边界

ID：`sparse-issue-eta-zero`；类别：`source_proof_error`；正式 PDF 页：7, 8, 20, 21。

\[\eta^{(k)}=A^{(k)}/\sum_{|S|=k}|I(S)|,\quad A^{(k)}/\eta^{(k)}=\sum_{|S|=k}|I(S)|\]

无交互时定义为0/0；非零正负交互恰好抵消时η=0，Eq57除法亦未定义。Theorem3所在Case1明确|η|≫1/n，已提供非零上下文，可以在该原范围忠实证明；不能扩大为完全抵消情况。

**影响范围：** 完全抵消情况不在可用除法范围；Case1计数推导无须增假设。

## fully random不足以推出2^|S|方差放大

ID：`sparse-issue-noise-variance`；类别：`source_statement_assumption_gap`；正式 PDF 页：8。

\[\operatorname{Var}(I_\varepsilon(S))=2^{|S|}\operatorname{Var}(\varepsilon)\]

原文未说明噪声项相互独立且同方差。令所有εT同一个非退化随机Z，中心化后εT−ε∅=0，所有噪声交互为0；该方差放大式不成立。若fully random意为iid需明确语义，不能自行给独立同方差假设。空集交互恒0也不是1倍原噪声方差。

**影响范围：** 噪声线性分解成立；概率结论另列，不公开增条件版本。

## 奇偶例的u(∅)与中心化冲突

ID：`sparse-issue-parity-empty`；类别：`source_statement_definition_conflict`；正式 PDF 页：9。

\[u(S)=\begin{cases}+1&|S|\text{ odd}\\-1&|S|\text{ even}\end{cases}\]

空集偶数，所以该显示定义给u(∅)=−1，而本篇全局定义给u(∅)=0。原示例在当前定义域中不存在。不能把u改成g或改空集值后宣称原例证明完成；原符号语义冲突单列。

**影响范围：** 正文Scenario2示例；不涉及Assumption2作为条件的其他证明。

## 单样本稀疏与重构不能推出样本间迁移

ID：`sparse-issue-transfer`；类别：`source_statement_counterexample`；正式 PDF 页：9。

\[\text{sparsity} + \text{universal matching}\Rightarrow\text{sample-wise transferability}\]

令总体N有n≥2变量，n个样本分别诱导g0^(j)(S)=1若j∈S，反之0。每个样本仅一个非零单变量交互，全部掩码都精确重构；不同样本的显著支撑互不相交。这些集合函数可由同一模型在不同掩码样本上实现（例如各样本仅一个坐标非零、v(z)=sum_i z_i），所有样本输出为1，可按分类阈值v(z)>1/2全部指定为同一正类，满足原“same category”条件。无需“爆炸”模式数。原反证没有全模型模式预算前提。

**影响范围：** Section4迁移推断不是两已知性质的逻辑推论，单独列出。

## D.2两个分量名称及去噪γ符号不一致

ID：`sparse-issue-decomposition-notation`；类别：`source_proof_error`；正式 PDF 页：29。

\[u_{and}=0.5u+\gamma,\quad u_{and}=0.5u-\gamma;\qquad u_{and}=0.5(u-\varepsilon)+\gamma,\quad u_{or}=0.5(u-\varepsilon)+\gamma\]

正式原式第二分量同名uand，去噪两项加γ使和为u−ε+2γ而非去噪输出。属于算法/证明中间式的标记与符号错；在原最终分解u=uand+uor保持不变下可标注并修中间式。

**影响范围：** D.2分解参数式；Eq61/62的数学目标本身未因此被推翻。

## Case2非指数小抵消比例不足以推出同阶稀疏

ID：`sparse-issue-asymptotic-sparsity`；类别：`source_statement_counterexample`；正式 PDF 页：7, 8。

\[\text{Case2: }|\eta^{(k)}|\text{ not exponentially small}\ \Longrightarrow\ R^{(k)}\text{ still much less than }\binom nk\]

完整无限族反例已写于math/rewrites.zh.md的asymptotic-claim。取n≥3且n≡2/3 mod4，q=choose(n,2)奇数；二阶±1系数的正/负项数为(q−1)/2与(q+1)/2，总和−1。模型v=Σzi+Σc_A∏i∈A zi，输入全1、基线0，给A1=n,A2=−1，所有高于二阶交互和混合偏导为零。μm=m−choose(m,2)/q；μm+1−μm=1−m/q>0，μm/m=1−(m−1)/(2q)非增，故原三条件以M=2,p=1完整满足。固定τ=1/100得到R2=q、η2=−1/q，其仅多项式小却二阶全显著。T3右端100q仍有效。反例只否定第8页Case2额外同阶推断，不把邻近mostcases经验描述当全称命题，也不否定总O(n²)相对2^n仍稀疏。

**影响范围：** Only p8 Case2 non-exponentially-small η ⇒ per-order R≪choose(n,k) inference; exact T2/T3 and neighboring empirical most-cases claim unchanged.

## Appendix H三阶表漏x3单变量项

ID：`sparse-issue-example-H-arithmetic`；类别：`source_proof_error`；正式 PDF 页：34。

\[u(\{3,4,5\})=0,\qquad\bar u^{(3)}=1.8\]

正式图像确给0，但代入v=x1x2x3+x1x2+x2x3+x2+x3、x=(1,1,1,1,1)、基线0，{3,4,5}保留x3=1，所以输出为1。三阶10项和应19、平均1.9。原二阶平均1≤三阶平均的结论仍成立；仅修算例表项和派生均值。

**影响范围：** 一个中间表项与均值1.8；不否定原单调示例结论。

## Theorem1换序后的第三行误用S⊇L

ID：`sparse-issue-reconstruction-index`；类别：`source_proof_error`；正式 PDF 页：15。

\[\sum_{\substack{T\subseteq S:S\supseteq L\\|T|=t}}(-1)^{t-|L|}u(L)\]

上一行要求T⊇L；第三行写成S⊇L不能筛选该L对应的T，导致计数不再是choose(|S|−|L|,t−|L|)。这是证明中间索引排印错；恢复上一行的T⊇L或用完整子集双射可证明相同原重构命题。

**影响范围：** B.1证明第三个等式中的求和限制；最终定理保持不变。

## Lemma4按l分组后仍保留未绑定L

ID：`sparse-issue-marginal-free-L`；类别：`source_proof_error`；正式 PDF 页：21。

\[\sum_{l=|K\setminus S|}^{|T|}(-1)^{|T|-|L|}\binom{|T|-|K\setminus S|}{l-|K\setminus S|}\]

按基数l分组后L已经不是求和变量，指数应随l变化才能调用二项式抵消。保留原自由L式供核查，项目共享有限差分证明不使用该错误中间式；原引理目标和全部T/S边界不变。

**影响范围：** B.5分组求和的一行；不影响修复后的原边际命题。

## Theorem6临界阶换序后组合数误留自由S

ID：`sparse-issue-STI-free-S`；类别：`source_proof_error`；正式 PDF 页：26。

\[\sum_{L\subseteq N\setminus T}I(T\cup L)\sum_{q=0}^{n-t}\frac{\binom{n-t-|L|}{q-|L|}}{\binom{n-1}{|S|}}\]

外层原环境S在换序后已按q=|S|分组，分母仍出现自由S；下一段转积分要求分母为choose(n−1,q)。这是局部索引排印错误，修复的共享有限阶乘卷积证明直接得到原临界阶权重，保留三分支命题。

**影响范围：** B.7临界阶权重换序行；原STI最终展开保持不变。

## T2参数域未在陈述中明确

ID：`sparse-issue-T2-parameter-domain`；类别：`statement_parameter_domain_gap`；正式 PDF 页：5, 7, 17, 18, 19。

\[\lambda=\sum_{k=1}^M\frac{\binom{m_0}k}{\binom nk}\lambda^{(k)}\ne0,\qquad\log_n(\cdot)\]

T2正文/附录没有明确重复Lemma3的M<n；不能把该限制偷偷加到T2。新构造覆盖M=n。实数log_n和n进制在n>1，全部choose(n,k)分母非零在M≤n；这是原表达的定义域说明。原页面未找到明确M∈N+约定：若允许M=0，取n=3且所有中心化输出0，三假设均成立，λ的空和为0，与λ≠0矛盾；因此这一读法的原陈述有反例，单列，不补M>0后冒充无条件原命题。正阶定义域中的完整存在构造另可验证。

**影响范围：** 缺失的参数作用域与零阶读法；正常正阶范围原系数目标不改。

## Lemma3 Eq33的降阶矩阵一行复制了n−2

ID：`sparse-issue-lemma3-copied-row`；类别：`source_proof_error`；正式 PDF 页：18。

\[\left[\binom{n-3}0,\binom{n-2}1,\ldots,\binom{n-2}{M-2}\right]\]

正式Eq33第二行除第一列外仍印n−2，与Eq32相邻行差分后第二行应来自n−3不一致。原数组在完整TeX中保留；正确消元或已完成的有限差分归纳可证明原零空间结论，不需沿错误矩阵再计算。该索引复制错与余子式符号漏项分别标记。

**影响范围：** Eq33降阶矩阵的第二行；不改变Lemma3正确最终结论。

