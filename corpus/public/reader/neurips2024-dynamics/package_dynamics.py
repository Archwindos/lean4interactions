"""Assemble checked F07 prose and real Lean evidence; never manufactures verification."""
from pathlib import Path
import json, sys, re
sys.path.insert(0, str(Path(__file__).parent))
from build_content import D, OBJ_Z, OBJ_E
from source_transcripts import T
from checked_dynamics_transcripts import T as CHECKED_T
T.update(CHECKED_T)
T['dyn-regression']=T['dyn-regression'].replace('作者求导（原 Eq.(46) 漏了公共 $2^{-n}$ 因子，不影响驻点）：','作者求导并令其为零：').replace('转置错式与对角元乘积错式保留。','')
R=Path.cwd(); P=R/'corpus/public/reader/neurips2024-dynamics'; pid=P.name
inv=json.loads((P/'inventory.json').read_text()); sid=inv['sources'][0]['source_id'];vid=inv['sources'][0]['version_id']
D['dyn-split-labels']=('Appendix C: duplicated component label',r'a_T=g(T)/2+\gamma_T,\quad a_T=g(T)/2-\gamma_T',None,None,r'原 Appendix C 同时将两个相反符号分量都记作 $v_{and}$，若逐字作为同一个函数的两条定义，二者相减强制 $2\gamma_T=0$，与任意可学习 $\gamma_T$ 不符。取常数网络 $v=1$、$\gamma_T=1$，两条定义分别要求同一 $v_{and}(x_T)=3/2$ 和 $-1/2$。这是原标签冲突；主文已分别规定 AND/OR 分量的定义不受该笔误影响。',r'Appendix C labels both opposite-sign components $v_{and}$. Taken literally as two definitions of the same function, subtraction forces $2\gamma_T=0$, contradicting an arbitrary learnable parameter. For the constant network $v=1$ and $\gamma_T=1$, the same $v_{and}(x_T)$ must equal both $3/2$ and $-1/2$. This is a printed label conflict; the distinct main-text AND/OR definitions are unaffected.','counterexample')
D['dyn-noise-split']=('Appendix C: noise-removal split equality',r'a_T+o_T=g(T)-\delta_T,\quad a_T=(g(T)-\delta_T)/2+\gamma_T,\quad o_T=(g(T)-\delta_T)/2+\gamma_T',None,None,r'原两分量都加 $\gamma_T$，其和实际是 $g(T)-\delta_T+2\gamma_T$；这条代数恒等主张错误。以原允许的常数网络 $g=1$、$\delta_T=0$、$\gamma_T=1$ 为例，原界 $|\delta_T|\le0.02|g(N)-b|=0$ 确实满足，而两分量各为 $3/2$，和为3不等于去噪输出1。实际 Lean 反例绑定整个掩码游戏、原去噪界与原两分量定义；不声称这个参数是 L1 最优解，原分解定义本就需对允许变量成立。',r'The two printed branches both add $\gamma_T$, so their sum is $g(T)-\delta_T+2\gamma_T$. This algebraic split claim is false. Use the allowed constant network $g=1$, $\delta_T=0$ and $\gamma_T=1$. The actual bound $|\delta_T|\le0.02|g(N)-b|=0$ holds, but both components equal $3/2$, summing to three rather than the denoised output one. The Lean counterexample binds the full masked game, source noise bound and both printed component definitions. It does not assert that this parameter is an L1 minimizer; a split definition must already hold on its permitted variables.','counterexample')
D['dyn-complement']=tuple(list(D['dyn-complement'][:6])+['partial_proof'])
for di in ['dyn-taylor']:
 row=list(D[di]);row[4]=row[4].replace(r'm_A(x_S)=\mathbf1_{A\subseteq S}m_A(x)', r'm_A(z^S)=\mathbf1_{A\subseteq S}m_A(z)');row[5]=row[5].replace(r'm_A(x_S)=\mathbf1_{A\subseteq S}m_A(x)', r'm_A(z^S)=\mathbf1_{A\subseteq S}m_A(z)');D[di]=tuple(row)
report=json.loads((P/'verification/report.json').read_text()); assert report['status']=='passed'
cat={d['name']:d for d in report['declarations']}
def clean(s):return s.replace(r'\n\n','\n\n')
OBJ_Z=r'固定有限总体 $N$、输入 $x$、输入基线向量 $r$ 与实值模型 $v$。掩码 $x_S$ 在 $S$ 内保留 $x_i$，其余取 $r_i$；原始游戏 $g(S)=v(x_S)$，输出基线 $b=g(\varnothing)$，中心化游戏 $g_0(S)=g(S)-b$。原输入 $b_i$ 对应 $r_i$，不将输出标量 $b$ 默认零。'
OBJ_E=r'Fix the finite universe $N$, input $x$, input baseline vector $r$ and real-valued model $v$. The mask $x_S$ retains $x_i$ in $S$ and uses $r_i$ elsewhere. Set $g(S)=v(x_S)$, output baseline $b=g(\varnothing)$ and centered game $g_0(S)=g(S)-b$. Source input $b_i$ maps to $r_i$, and scalar output baseline $b$ is not assumed zero.'
local_defs={
 'dyn-universal':(r'固定同一分解 $a(S)=g(S)/2+\gamma_S,o(S)=g(S)/2-\gamma_S$；$A(T)=I_a(T)$，非空 $O(T)=-I_h(T)$，$h(L)=o(N\setminus L)$。原F.1空分量规定是 $a(\varnothing)=b,o(\varnothing)=0$。',r'Fix the same split $a(S)=g(S)/2+\gamma_S,o(S)=g(S)/2-\gamma_S$. Put $A(T)=I_a(T)$ and, for nonempty T, $O(T)=-I_h(T)$ with $h(L)=o(N\setminus L)$. The F.1 empty convention is $a(\varnothing)=b,o(\varnothing)=0$.'),
 'dyn-taylor':(r'增量坐标 $z_i=x_i-r_i$；多重指标 $\pi_i\in\mathbb N$，支持 $\{i:\pi_i>0\}$，$Q_T$ 要求支持恰为 $T$。$D^\pi v(r)$ 是在输入基线向量处的经典混合导数，不是输出基线处导数。',r'Increment coordinates are $z_i=x_i-r_i$. A multi-index has natural entries and support $\{i:\pi_i>0\}$; $Q_T$ requires support exactly T. $D^\pi v(r)$ denotes the classical mixed derivative at the input baseline vector, not at the output-baseline scalar.'),
 'dyn-trigger-representation':(r'参考输入为 $\hat x$，$w_T=I_g(T\mid\hat x)$；支持贡献 $K_T$ 是原Taylor和。$J_T=K_T/w_T$ 是比值表达式，$w_\varnothing=b,J_\varnothing=1$ 是原特设空项。',r'The reference input is $\hat x$ with $w_T=I_g(T\mid\hat x)$. The support contribution $K_T$ is the source Taylor sum; $J_T=K_T/w_T$ is its ratio. The empty coordinate is separately specified as $w_\varnothing=b,J_\varnothing=1$.'),
 'dyn-noisy-output':(r'每个遮罩输出的噪声为 $\Delta v_L$，交互噪声 $\Delta I_T=\sum_{L\subseteq T}(-1)^{|T|-|L|}\Delta v_L$。给定原 $w_T$ 后，$\epsilon_T=\Delta I_T/w_T$ 只在该分母有定义的普通实数范围使用。',r'Noise on each mask output is $\Delta v_L$; dividend noise is $\Delta I_T=\sum_{L\subseteq T}(-1)^{|T|-|L|}\Delta v_L$. For the given $w_T$, $\epsilon_T=\Delta I_T/w_T$ is used on its ordinary-real defined denominator domain.'),
 'dyn-complement':(r'反向游戏 $h(L)=o(N\setminus L)$ 使用固定OR分量o与固定总体N。反向遮罩 $\tilde x_L$ 在L内取r、其余取x；不另变动分量函数或输入总体。',r'The reversed game $h(L)=o(N\setminus L)$ uses the fixed OR component o and fixed universe N. The reversed mask $\tilde x_L$ uses r in L and x elsewhere, without changing the component function or universe.'),
 'dyn-salience':(r'$\tau$ 取样本平均相对输出幅度的3%；$\Omega_{and},\Omega_{or}$ 分别筛选两个分量。$Z$ 是 $1\le k\le n$ 阶数的平均强度，$Z_{theo}$ 对理论权重另定义；两个分母不预设为正。',r'Threshold $\tau$ is three percent of mean relative output magnitude. $\Omega_{and},\Omega_{or}$ select the components separately. Z averages strength over orders $1\le k\le n$; $Z_{theo}$ is separately defined for theoretical weights. Neither denominator is assumed positive by default.'),
 'dyn-extraction':(r'$\gamma_T$ 是每个遮罩的拆分优化变量；$\delta_T$ 是有界输出修正，$\zeta=0.02|g(N)-b|$。L1目标是两分量全部交互绝对值和。',r'Each mask has a split variable $\gamma_T$ and bounded output correction $\delta_T$, with $\zeta=0.02|g(N)-b|$. The L1 objective sums magnitudes of all dividends in both components.'),
 'dyn-mask-monotonic':(r'$\bar u^{(k)}$ 是基数为k的全部掩码中 $g(S)-b$ 的均匀平均；这里k是保留变量数。',r'$\bar u^{(k)}$ is the uniform average of $g(S)-b$ over all masks of cardinality k; k counts retained variables.'),
 'dyn-mask-polynomial':(r'使用同一掩码平均 $\bar u^{(k)}$；$p>0$ 是退化界的常数指数，不是类别概率，原 $k^\prime/k$ 需要非零分母。',r'Use the same mask average $\bar u^{(k)}$. Here $p>0$ is the constant exponent of the degradation bound, not a class probability, and the source ratio requires a nonzero k.'),
 'dyn-cutoff':(r'$M\in\mathbb N$ 是最高允许非零交互阶数；条件对每个 $|S|\ge M+1$ 的集合要求交互严格为零。',r'$M\in\mathbb N$ is the maximum allowed nonzero dividend order; the condition requires exact zero for every coalition with $|S|\ge M+1$.'),
 'dyn-uniqueness':(r'线性变换系数a(S,U)独立于游戏g、定义于U⊆S；其变换值d(S)=Σ_{U⊆S}a(S,U)g(U)。候选系数族 $d:2^N\to\mathbb R$ 在每个遮罩U上满足 $g(U)=\sum_{T\subseteq U}d(T)$。待比较的真实系数是 $I_g$；不是仅全输入拟合的一组权重。',r'The linear transform coefficients a(S,U) are independent of g and defined on U⊆S, with transformed values d(S)=Σ_{U⊆S}a(S,U)g(U). The candidate family $d:2^N\to\mathbb R$ satisfies $g(U)=\sum_{T\subseteq U}d(T)$ at every mask U. It is compared with the actual dividend family $I_g$, not merely weights fitted at the full input.')}
for ci in ['dyn-split-labels','dyn-noise-split']:local_defs[ci]=local_defs['dyn-extraction']
reg_z=r'令 $\mathcal A=2^N$，$m=|\mathcal A|=2^n$。$y,w,w^*\in\mathbb R^{\mathcal A}$；$y_S=g^*(S)$。矩阵 $J\in\mathbb R^{\mathcal A\times\mathcal A}$ 的行S是遮罩、列T是概念，$J_{ST}=\mathbf1_{T\subseteq S}$。触发噪声 $\epsilon=(\epsilon_T)_{T\in\mathcal A}$ 定义在概率空间上，方差向量 $c_T=2^{|T|}\sigma^2$。$B=J^\top J$，$D=m\operatorname{diag}(c)$，$A=B+D$，$\hat M=A^{-1}B$；$\hat m_T$ 是 $\hat M$ 的第T行，欧氏范数为该行平方和的平方根。原损失是 $\widetilde L(w)=m^{-1}\sum_{S\in\mathcal A}E[(y_S-(Jw)_S-w^\top\epsilon)^2]$。'
reg_e=r'Let $\mathcal A=2^N$ and $m=|\mathcal A|=2^n$. Vectors $y,w,w^*\in\mathbb R^{\mathcal A}$ include every coalition, with $y_S=g^*(S)$. Matrix $J\in\mathbb R^{\mathcal A\times\mathcal A}$ has mask rows S, concept columns T, and entries $J_{ST}=\mathbf1_{T\subseteq S}$. Trigger noise $\epsilon=(\epsilon_T)_{T\in\mathcal A}$ lives on a probability space and has variance vector $c_T=2^{|T|}\sigma^2$. Put $B=J^\top J$, $D=m\operatorname{diag}(c)$, $A=B+D$ and $\hat M=A^{-1}B$. Row $\hat m_T$ has Euclidean norm equal to the square root of its squared-entry sum. The source loss is $\widetilde L(w)=m^{-1}\sum_{S\in\mathcal A}E[(y_S-(Jw)_S-w^\top\epsilon)^2]$.'
for ri in ['dyn-regression','dyn-equal-order','dyn-order-monotonic','dyn-zero-noise','dyn-regression-definition','dyn-first-phase']:local_defs[ri]=(reg_z,reg_e)
local_defs['dyn-binary-trigger']=local_defs['dyn-trigger-representation']
u=list(D['dyn-universal'])
u[4]+=r'\n\n主文Eq.(2)明确仅为非空S定义分量交互；Eq.(3)却遍历T⊆N，包括未说明的空AND系数。它首先是空项的定义域/约定缺口。若按普通Möbius公式扩展空AND为a(empty)=b，常数网络v=1、a=1,o=0给空AND1、非空系数0，原Eq.(3)扩展解释给2而原输出1；若另约定空AND为0则不会重复，但该约定不能从Eq.(2)读出。Eq.(4)仅求非空AND，不依赖这种扩展。显著截断Eq.(5)的残差是两个未保留激活和，绝对值至多对应绝对尾和；没有统一小尾和前提时不升级近似号。'
u[5]+=r'\n\nMain Eq.(2) explicitly defines component dividends only for nonempty S, whereas Eq.(3) sums over all T⊆N, including an unspecified empty AND coefficient. This is first a domain/convention gap. Under the ordinary Möbius extension, the empty AND coefficient is a(empty)=b. The constant network v=1 with a=1,o=0 has empty coefficient one and zero nonempty coefficients, so this extension of Eq.(3) gives two rather than one. Setting the empty AND coefficient to zero avoids duplication but is not specified in Eq.(2). Eq.(4) uses only nonempty AND terms and avoids this extension. The residual of salient truncation in Eq.(5) is the two omitted activated sums and is bounded by their absolute tails; no uniform small-tail premise is supplied.'
u[6]='partial_proof';D['dyn-universal']=tuple(u)
v=list(D['dyn-salience'])
v[4]+=r'\n\n原理论指标完整定义为 $I_{theo}^{(k)}=E_x[\sum_{S:|S|=k,|\hat w_S|\ge\tau_{theo}}|\hat w_S|]/Z_{theo}$，$Z_{theo}=E_{1\le k\prime\le n}E_x[\sum_{S:|S|=k\prime,|\hat w_S|\ge\tau_{theo}}|\hat w_S|]$，$v_{theo}(x)=\sum_{S\subseteq N}\hat w_S$，$\tau_{theo}=0.03|v_{theo}(x)-\hat w_\varnothing|$。其Z仍不含空阶，但输出基线保留；拟合不同epoch的sigma由最佳经验匹配选择，不由训练公式唯一推出。'
v[5]+=r'\n\nThe complete theoretical metric is $I_{theo}^{(k)}=E_x[\sum_{S:|S|=k,|\hat w_S|\ge\tau_{theo}}|\hat w_S|]/Z_{theo}$, where $Z_{theo}=E_{1\le k\prime\le n}E_x[\sum_{S:|S|=k\prime,|\hat w_S|\ge\tau_{theo}}|\hat w_S|]$, $v_{theo}(x)=\sum_{S\subseteq N}\hat w_S$, and $\tau_{theo}=0.03|v_{theo}(x)-\hat w_\varnothing|$. Its normalization excludes order zero but preserves the output baseline. Noise values at different epochs are selected by best empirical matching, rather than uniquely derived from a training formula.'
D['dyn-salience']=tuple(v)
# English retains all intermediate equations; inline variable spelling may differ.
replacements={
 'dyn-universal':[(r'Their full sum is $o(N)-o(\varnothing)$',r'Their full sum is $h(\varnothing)-h(N)=o(N)-o(\varnothing)$'),(r'is $o(N)-o(S)$',r'is $h(\varnothing)-h(N\setminus S)=o(N)-o(S)$')],
 'dyn-trigger-representation':[(r'Nonzero normalization yields the binary trigger.',r'Nonzero normalization yields $J_T(\hat x_S)=\mathbf1_{T\subseteq S}$.')],
 'dyn-binary-trigger':[(r'Nonzero normalization yields the binary trigger.',r'Nonzero normalization yields $J_T(\hat x_S)=\mathbf1_{T\subseteq S}$.')],
 'dyn-noisy-output':[(r'The main statement specifies only Gaussian marginals.',r'The main statement specifies only Gaussian marginals $\Delta v_L\sim\mathcal N(0,\sigma^2)$. '),(r'for both masks.',r'for both masks, $\Delta v_\varnothing=\Delta v_{\{1\}}=Z$.'),(r'every sign has square one',r'every sign has square $1$')],
 'dyn-regression':[(r'The nonnegative diagonal penalty is positive semidefinite',r'The diagonal penalty $2^n\operatorname{diag}(c)$ is positive semidefinite'),(r'$A$ is positive definite',r'$A=J^\top J+2^n\operatorname{diag}(c)$ is positive definite'),(r'F.4 prints the erroneous transpose',r'F.4 prints the erroneous transpose $J^\top w^*$')],
 'dyn-complement':[(r'$b_i$',r'$r_i$'),(r'The source reversed mask retains $x_i$',r'The source reversed mask has $(\tilde x_T)_i=x_i$')],
 'dyn-dummy':[(r'makes $h_i$ constant on every $U\subseteq S$.',r'makes $h_i$ equal the constant $g(\{i\})$ on every $U\subseteq S$.')],
 'dyn-anonymity':[(r'Each sign is preserved',r'Each sign $(-1)^{|S|-|U|}$ is preserved')],
 'dyn-distribution':[(r'Its subset sum is $c\mathbf1_{A\subseteq S}=g_A(S)$',r'Its subset sum is $\sum_{T\subseteq S}d(T)=c\mathbf1_{A\subseteq S}=g_A(S)$')]
}
for di,rrs in replacements.items():
 row=list(D[di]);en=row[5]
 for x,y in rrs:en=en.replace(x,y)
 row[5]=en;D[di]=tuple(row)

cc=list(D['dyn-complement']);cc[4]=cc[4].replace('$b_i$','$r_i$');D['dyn-complement']=tuple(cc)

u=list(D['dyn-uniqueness'])
u[1]=r'\left[\forall g,W,\quad g(W)=\sum_{S\subseteq W}\sum_{U\subseteq S}a(S,U)g(U)\right]\Longrightarrow\left[\forall U\subseteq S,\quad a(S,U)=(-1)^{|S|-|U|}\right]'
u[4]+=r'\n\n这还需隔离作者所说的变换系数：设实系数a(S,U)独立于游戏g、只作用于U⊆S，且对所有游戏的所有遮罩都能由这些变换值重构。前一步给每个游戏的变换值等于I_g(S)。固定U，取基游戏 $g_U(L)=\mathbf1_{L=U}$；有限和只有L=U存活，左变换值为a(S,U)，而Möbius和为 $(-1)^{|S|-|U|}$。所以整个线性算子的每个系数唯一。对单个固定游戏，这个基游戏论证不能使用；AND/OR联合拆分参数gamma也不因此唯一。'
u[5]+=r'\n\nTo isolate the transform coefficients claimed by the author, take real coefficients a(S,U), independent of the game g and supported on U⊆S, whose transformed values reconstruct every mask for every game. The first step identifies each transformed value with I_g(S). Fix U and choose the basis game $g_U(L)=\mathbf1_{L=U}$. Only L=U survives in either finite sum: the proposed transform gives a(S,U), and the Möbius transform gives $(-1)^{|S|-|U|}$. Thus every coefficient of the linear operator is unique. This basis argument is unavailable for a single fixed game and does not establish uniqueness of a joint AND/OR split parameter gamma.'
D['dyn-uniqueness']=tuple(u)

def ref(n,en=False):
 d=cat[n]
 return dict(declaration=n,source_path=d['source_path'],line=d['line'],scope='exact_declared_type')
maps={
 'dyn-universal':[['Harsanyi.reconstruction'],['Harsanyi.or_reconstruction','Harsanyi.Layerwise.and_or_matching'],[]],
 'dyn-taylor':[[],['Harsanyi.TaylorMoments.monomial_mask','Harsanyi.PolynomialSupport.mask_terms','Harsanyi.PolynomialSupport.support_reconstruct','Harsanyi.PolynomialSupport.interaction_eq_supportCoefficient']],
 'dyn-trigger-representation':[[],['Harsanyi.TaylorMoments.normalized_trigger']],
 'dyn-binary-trigger':[[],['Harsanyi.TaylorMoments.normalized_trigger']],
 'dyn-noisy-output':[['Harsanyi.interaction_add'],['PaperDynamics.correlated_noise_counterexample'],['Harsanyi.and_gaussian_variance']],
 'dyn-regression':[['Harsanyi.GaussianRegression.independent_residual','PaperDynamics.noisyLoss_expansion'],['Harsanyi.NoisyRegression.zeta_injective','Harsanyi.NoisyRegression.normal_posDef','Harsanyi.NoisyRegression.quadratic_unique_min'],['PaperDynamics.meanNoisyLoss_unique_min']],
 'dyn-equal-order':[['Harsanyi.NoisyRegression.transfer_permutation'],['Harsanyi.NoisyRegression.exists_coalition_permutation','PaperDynamics.equal_order_norm']],
 'dyn-order-monotonic':[['PaperDynamics.zero_noise_row_ratio'],['PaperDynamics.equal_order_norm']],
 'dyn-zero-noise':[['PaperDynamics.zero_noise_recovery']],
 'dyn-efficiency':[['PaperDynamics.efficiency']], 'dyn-linearity':[['Harsanyi.interaction_add']],
 'dyn-dummy':[['PaperDynamics.dummy']], 'dyn-symmetry':[['PaperDynamics.symmetry']],
 'dyn-anonymity':[['Harsanyi.interaction_relabel']], 'dyn-recursion':[['Harsanyi.interaction_recursive']],
 'dyn-distribution':[['Harsanyi.interaction_unanimity']], 'dyn-uniqueness':[['Harsanyi.reconstruction_unique'],['PaperDynamics.transform_coefficients_unique']],
 'dyn-complement':[['Harsanyi.maskCoordinates_complement','Harsanyi.or_dual'],[]],
 'dyn-noise-split':[['PaperDynamics.noise_split_counterexample']]
}
shared_map={
 'dyn-universal':['proof-finite-mobius-reconstruction-v2','shared-harsanyi-or-reconstruction'],
 'dyn-taylor':['dyn-shared-polynomial-support'], 'dyn-trigger-representation':['dyn-shared-polynomial-support'],
 'dyn-binary-trigger':['dyn-shared-polynomial-support'], 'dyn-noisy-output':['dyn-shared-independent-residual'],
 'dyn-regression':['dyn-shared-independent-residual','dyn-shared-positive-regression'],
 'dyn-equal-order':['dyn-shared-positive-regression'], 'dyn-order-monotonic':['dyn-shared-positive-regression'],
 'dyn-zero-noise':['dyn-shared-positive-regression'],
 'dyn-efficiency':['proof-finite-mobius-reconstruction-v2'], 'dyn-linearity':['shared-harsanyi-linearity'],
 'dyn-dummy':['shared-harsanyi-dummy-nonempty'],'dyn-symmetry':['shared-harsanyi-symmetry'],
 'dyn-anonymity':['shared-harsanyi-anonymity'],'dyn-recursion':['shared-harsanyi-recursive'],
 'dyn-distribution':['shared-harsanyi-interaction-distribution'],'dyn-uniqueness':['proof-finite-mobius-uniqueness-v2'],
 'dyn-complement':['shared-harsanyi-or-reconstruction']
}
titles={
 'dyn-uniqueness':[('重构确定每个游戏的交互值','Reconstruction determines each game’s dividend values'),('基游戏隔离线性变换系数','Basis games isolate linear transform coefficients')],
 'dyn-universal':[('AND 重构与空项','Reconstruct the AND component'),('OR 激活和与合并','Sum activated OR coefficients and combine'),('未说明的空项与显著近似','Unspecified empty terms and salient approximation')],
 'dyn-taylor':[('完整 ReLU 反例','A complete ReLU counterexample'),('有限多项式的有效子结果','The valid finite-polynomial subresult')],
 'dyn-trigger-representation':[('核查归一化定义域','Check the normalization domain'),('有定义范围的二值化','Prove binary masking on the defined domain')],
 'dyn-binary-trigger':[('核查归一化定义域','Check the normalization domain'),('有定义范围的二值化','Prove binary masking on the defined domain')],
 'dyn-noisy-output':[('交互噪声的线性展开','Expand the dividend noise'),('边缘 Gaussian 的相关反例','Correlated Gaussian marginal counterexample'),('独立模型与缩放','Independent variance and trigger scaling')],
 'dyn-regression':[('精确计算期望损失','Compute the expected loss exactly'),('反演、正定与唯一全局最优','Inversion, positivity and unique global minimality'),('适配原标签与权重','Adapt the source labels and coefficients')],
 'dyn-equal-order':[('共轭不变的完整矩阵','Conjugation invariance of the full matrix'),('同阶集合排列与行范数','Permute equal-order coalitions and row norms')],
 'dyn-order-monotonic':[('零噪声否定严格子句','Zero noise refutes the strict clause'),('有效子句与未决一般单调性','Valid clauses and unresolved general monotonicity')],
 'dyn-complement':[('逐坐标核对反向遮罩','Check the reversed mask coordinatewise'),('补集适配的条件边界','Check the boundary of the complement adaptation')],
 'dyn-split-labels':[('比较原两个同名定义','Compare the two identically labeled definitions')],
 'dyn-noise-split':[('计算原分量和及允许反例','Compute the printed component sum and an allowed counterexample')]
}
assumptions={
 'dyn-universal':[(r'使用原 F.1 明确规定的空分量 $v_{and}(x_\varnothing)=v(x_\varnothing)$、$v_{or}(x_\varnothing)=0$；等价于 $\gamma_\varnothing=b/2$，不是任意无约束分解。',r'Use the empty-component convention explicitly imposed in F.1: $v_{and}(x_\varnothing)=v(x_\varnothing)$ and $v_{or}(x_\varnothing)=0$, equivalently $\gamma_\varnothing=b/2$. This is not an arbitrary unconstrained split.')],
 'dyn-taylor':[(r'原文只规定 DNN 与固定输入基线，没有解析性、Taylor 收敛区间或有限多项式前提。',r'The source specifies a DNN and fixed input baseline without analyticity, a Taylor convergence domain or a finite-polynomial premise.')],
 'dyn-noisy-output':[(r'正文各输出噪声只有 $\mathcal N(0,\sigma^2)$ 边缘条件；附录 F.3 另称 iid。二者单独审查。',r'The main statement gives only $\mathcal N(0,\sigma^2)$ output-noise marginals; F.3 separately adds iid noise. These scopes are reviewed separately.')],
 'dyn-regression':[(r'原 Assumption 1：触发噪声彼此独立、零均值，$c_T=\operatorname{Var}\epsilon_T=2^{|T|}\sigma^2$；通常有限二阶矩语义在 Lean 中为 MemLp 2。',r'Source Assumption 1: independent centered trigger noise with $c_T=\operatorname{Var}\epsilon_T=2^{|T|}\sigma^2$. Its ordinary finite-second-moment meaning is encoded as MemLp 2 in Lean.'),(r'所有 $2^n$ 个遮罩均匀平均；Lemma 2 的有定义二值设计 $J_{ST}=\mathbf1_{T\subseteq S}$，标签 $y=Jw^*$，包含空项。',r'Average uniformly over all $2^n$ masks. Use Lemma 2 on its defined binary-design domain, $J_{ST}=\mathbf1_{T\subseteq S}$ and $y=Jw^*$, including the empty coordinate.')],
 'dyn-equal-order':[(r'原 Theorem 3 的二值设计与按阶数方差；$T,T\prime\subseteq N$ 且 $|T|=|T\prime|$，$\sigma^2\ge0$ 包括零。',r'Theorem 3 binary design and order-dependent variances; $T,T\prime\subseteq N$ with equal cardinality and $\sigma^2\ge0$, including zero.')],
 'dyn-order-monotonic':[(r'原 Proposition 1 不排除 $\sigma=0$；Theorem 3 的 $\hat M$ 不含 $w^*$。',r'Proposition 1 does not exclude $\sigma=0$; its transfer matrix from Theorem 3 contains no $w^*$.')],
 'dyn-zero-noise':[(r'原 Theorem 3 回归设置且 $\sigma=0$；没有 $b=0$ 假设。',r'The Theorem 3 regression setting with $\sigma=0$, without an assumption $b=0$.')]
}
assumptions.update({
 'dyn-efficiency':[(r'固定有限总体 N，所有S⊆N，交互取原始输出游戏。',r'Fix the finite universe N; use all coalitions S⊆N and dividends of the raw output game.')],
 'dyn-linearity':[(r'原模型满足全部遮罩上的逐点关系 v(x_S)=v1(x_S)+v2(x_S)，参数和输入基线固定。',r'The source models satisfy v(x_S)=v1(x_S)+v2(x_S) on every mask, with fixed parameters and input baseline.')],
 'dyn-dummy':[(r'i不在S，S非空；原dummy前提对全部U⊆N\{i}成立，包括空U。',r'The variable i is outside the nonempty coalition S; the source dummy premise holds on every U⊆N\{i}, including empty U.')],
 'dyn-symmetry':[(r'S⊆N\{i,j}；对全部相同作用域U，两插入变量的原输出相等。',r'S⊆N\{i,j}; for every context U in this domain, inserting either variable gives equal source outputs.')],
 'dyn-anonymity':[(r'原π是有限总体N的排列，新模型在πS上的值等于原模型在S上的值。',r'The source π permutes N, and the new model at πS equals the original model at S.')],
 'dyn-recursion':[(r'原i∈N且S⊆N\{i}；始终出现i的背景游戏按原有限和明确定义。',r'The source has i∈N and S⊆N\{i}; its always-present-i context game is defined by the displayed finite sum.')],
 'dyn-distribution':[(r'固定T⊆N与实数c；原v_T只在T全部出现时取c，其余取0。',r'Fix T⊆N and real c; source v_T equals c exactly when T is fully present, and zero otherwise.')],
 'dyn-uniqueness':[(r'系数a(S,U)独立于g，三角支持U⊆S；对所有有限游戏g的所有遮罩均满足重构。',r'The coefficients a(S,U) are independent of g and triangular on U⊆S; reconstruction holds for every mask of every finite game.')]
})
for i in ['dyn-trigger-representation','dyn-binary-trigger']:
 assumptions[i]=[(r'保存原 Taylor 定义与原所有子集量词；作者未排除 $w_T=0$。有效子结果明确仅在该比值有定义及支持展开有效的范围使用，不算无条件原式已证。',r'Retain the source Taylor definition and all-coalition quantifier; zero $w_T$ is not excluded by the author. The valid subresult uses only the defined-ratio domain and a valid support expansion, and is not a proof of the unrestricted expression.')]
issues=[]
def issue(i,title,en,pages,kind,expr,z,e,ez,ee,iz,ie):
 issues.append(dict(id=i,paper_id=pid,title=title,kind=kind,source_refs=[dict(source_id=sid,version_id=vid,pdf_pages=pages)],original_expression=expr,description_md=z,evidence_md=ez,impact_md=iz,user_confirmation='not_individually_confirmed',fix_authorization='proof_only_granted',proposition_modification_authorized=False,status='agent_checked',translations=dict(en=dict(title=en,description_md=e,evidence_md=ee,impact_md=ie))))
issue('dyn-issue-taylor','任意 DNN 的全局 Taylor 等式不成立','The global Taylor equality fails for arbitrary DNNs',[18,19],'statement_error',r'v(x_S)=\sum_\pi D^\pi v(x_\varnothing)(x_S-b)^\pi/\pi!',
 '原 Lemma 3 没有解析或收敛前提。','Lemma 3 has no analyticity or convergence premise.',
 r'$v(t)=\max(t-1/2,0)$、基线0、输入1，是一层 ReLU 网络；在0邻域恒零，全部 Taylor 系数0，而单变量交互为1/2。',r'The one-layer ReLU network $v(t)=\max(t-1/2,0)$ is zero near baseline 0, so every Taylor coefficient vanishes, while the dividend at input 1 is 1/2.',
 '原无条件命题被反驳；有限多项式支持分组是另列的有效子结果。','The unrestricted claim is refuted; finite-polynomial support grouping is a separate valid subresult.')
issue('dyn-issue-zero-trigger','零交互使归一化触发无定义','A zero dividend leaves the normalized trigger undefined',[7,19,20,22],'undefined_boundary',r'J_T=K_T/w_T,\quad w_T=I(T\mid\hat x)',
 '原 Eq.(7) 与 Lemma 2 对所有子集使用除法而未排非空零交互。','Eq.(7) and Lemma 2 divide by every coefficient without excluding zero nonempty dividends.',
 r'恒定模型 $v=1$ 满足原 DNN 设置，所有非空 $I(T)=K_T=0$；对 $T\subseteq S$ 的触发是通常实数中无定义的0/0，不能约去得到1。',r'The allowed constant model $v=1$ has $I(T)=K_T=0$ for every nonempty $T$. Its triggered ratio is the undefined ordinary-real expression 0/0, which cannot be canceled to one.',
 '保留原定义域问题，非零域的归一化证明不冒充原无条件命题。','Retain the domain issue; the normalization proof on the nonzero domain does not replace the unrestricted claim.')
issue('dyn-issue-marginal-independence','Lemma 1 的边缘律不足以给方差和','Lemma 1 marginals do not justify summing variances',[7,20,21],'statement_error',r'\operatorname{Var}\Delta I_T=2^{|T|}\sigma^2',
 '正文只有 Gaussian 边缘，附录才新增 iid。','Only Gaussian marginals occur in the main statement; iid is introduced in the appendix.',
 r'一变量两个输出噪声共用 $Z\sim\mathcal N(0,\sigma^2)$，$\sigma>0$；全部边缘满足原条件而 $\Delta I_{\{1\}}=Z-Z=0$。PaperDynamics 的反例实际绑定 Gaussian map-law 与原交互。',r'For one variable, both output noises equal the same $Z\sim\mathcal N(0,\sigma^2)$ with $\sigma>0$. Every marginal satisfies the source law, but the dividend noise is zero. The PaperDynamics counterexample binds the Gaussian map-law and actual dividend.',
 '均值与线性恒等式有效；iid 方差另作为带明确原附录前提的子结果。','The mean and linear identity remain valid; the iid variance is a separate subresult with the explicit appendix premise.')
issue('dyn-issue-trigger-variance','触发缩放与 Assumption 1 是不同模型','Trigger scaling and Assumption 1 describe different models',[7,8,21],'scope_mismatch',r'\operatorname{Var}\epsilon_T=2^{|T|}\sigma^2/w_T^2',
 'Lemma 1 的除以权重会引入逐概念比例；输出噪声也使多个交互相关。','Dividing by weights introduces a concept-dependent scale, and shared output noise correlates dividends.',
 r'若 $w_{T_1}=1,w_{T_2}=2$，同一阶数的方差比例为1和1/4；不能使用同一个比例常数。',r'If equal-order weights are 1 and 2, the scaling factors are 1 and 1/4; one common proportionality constant does not apply.',
 'Theorem 3 可在另外明确规定的 Assumption 1 下证明；不宣称该假设由 Lemma 1 推出。','Theorem 3 is proved under separately imposed Assumption 1, which is not claimed to follow from Lemma 1.')
issue('dyn-issue-gram-determinant','Gram 行列式不是对角项乘积','A Gram determinant is not the product of its diagonal entries',[22],'proof_error',r'\det(J^\top J)=\prod_k\lambda_k=\prod_k(J^\top J)_{kk}',
 '原 F.4 把特征值乘积误等同对角项乘积，并把零噪声对角罚项误称正定。','F.4 identifies the eigenvalue product with the diagonal product and calls the penalty positive definite even at zero noise.',
 r'一变量 zeta Gram 为 $\begin{pmatrix}2&1\\1&1\end{pmatrix}$，行列式1而对角积2；$\sigma=0$ 罚项为零。',r'The one-variable zeta Gram is $\begin{pmatrix}2&1\\1&1\end{pmatrix}$, with determinant 1 and diagonal product 2. At zero noise the penalty is zero.',
 '用 Möbius 单射证明 Gram 正定，再加半正定罚项；原最优命题无需新条件。','Möbius injectivity proves Gram positive definiteness, then a positive-semidefinite penalty is added; the source optimum needs no new condition.')
issue('dyn-issue-expectation','大样本协方差不能替代精确期望','A sample-covariance limit does not establish the exact expectation',[21,22],'proof_error',r'E[E^\top E]=2^n\operatorname{diag}(c)',
 '原证明把样本数足够大的近似收敛作为固定样本数的等式理由。','The proof uses large-sample approximate convergence to justify an equality at a fixed sample size.',
 r'逐行有 $E[\epsilon_T\epsilon_U]=0$（$T\ne U$）和 $E[\epsilon_T^2]=c_T$，求和恰为 $2^n\operatorname{diag}(c)$，无需行间独立或渐近。',r'Each row has $E[\epsilon_T\epsilon_U]=0$ for $T\ne U$ and $E[\epsilon_T^2]=c_T$. Summing gives exactly $2^n\operatorname{diag}(c)$, without independence across rows or asymptotics.',
 '逐行精确期望补正同一证明，Lean 直接积分平方残差。','The same proof is repaired by exact rowwise expectations; Lean integrates the squared residual directly.')
issue('dyn-issue-label-transpose','标签向量转置错误','The label-vector transpose is incorrect',[22],'proof_error',r'y=J^\top w^*',
 '原矩阵行是遮罩、列是概念，所以标签应用 J 而非其转置。','Rows index masks and columns index concepts, so labels use J rather than its transpose.',
 r'$y_S=\sum_{T\subseteq S}w_T^*$ 正是 $(Jw^*)_S$；一变量取 $w^*=(1,2)$，$Jw^*=(1,3)$ 而 $J^\top w^*=(3,2)$。',r'The source rowwise labels are exactly $(Jw^*)_S$. For one variable and $w^*=(1,2)$, $Jw^*=(1,3)$ while $J^\top w^*=(3,2)$.',
 '正文 Theorem 3 的末式正确，用正确标签补正证明。','The final main-text formula is correct; its proof uses the correct label vector.')
issue('dyn-issue-or-grouping','OR 证明的激活分组边界','Activation-grouping boundary in the OR proof',[17,18],'proof_error',r'\sum_{|T^{\prime\prime}|=0}^{|S|}\binom{|S|}{|T^{\prime\prime}|}(-1)^{|T^{\prime\prime}|}=0',
 'L 与 S 不交时，T 必须仍与 S 相交，不能把空激活项放入内和。另当 L 包含 S 但 L≠N 时，原声称内和零也无效。','When L is disjoint from S, T must still intersect S; the empty activation cannot be included. If L contains S but differs from N, the printed inner-zero assertion also fails.',
 r'$N=\{1,2\},S=\{1\},L=\varnothing$：合法超集T为{1},{1,2}，激活块只取{1}，不是包括空块的二项式和。$L=S=\{1\}\ne N$ 时原内和仅一项1。',r'For $N=\{1,2\},S=\{1\},L=\varnothing$, the admissible supersets are {1} and {1,2}; the activation block is {1}, not the full binomial family including the empty block. If $L=S=\{1\}\ne N$, the printed inner sum has only the term one.',
 '全 OR 和减去不激活和给完整同命题证明。','Subtracting the inactive OR sum from the full OR sum proves the same theorem.')
issue('dyn-issue-eq3-empty','Eq.(3) 使用未定义空 AND 项','Eq.(3) uses an unspecified empty AND coefficient',[3,4,16],'undefined_boundary',r'f(x_S)=v(x_\varnothing)+\sum_{T\subseteq N}I_{and}(T)\mathbf1_{T\subseteq S}+\cdots',
 '主文 Eq.(2) 只定义非空分量交互，Eq.(3) 却包含空 AND 系数。F.1 规定的是空分量输出，不是主文空交互定义。','Main Eq.(2) defines only nonempty component dividends, while Eq.(3) includes the empty AND coefficient. F.1 specifies empty component outputs, rather than the missing main-text empty-dividend definition.',
 r'若按通常 Möbius 公式补扩展 $I_a(\varnothing)=a(\varnothing)=b$，取常数网络 $v=1,a=1,o=0$，扩展后的 Eq.(3) 给2而原输出1；该例严格依赖此显式扩展。若约定空 AND 为0，重复消失，但主文 Eq.(2) 未给该约定。Eq.(4) 非空和正确。',r'Under the explicitly stated ordinary Möbius extension $I_a(\varnothing)=a(\varnothing)=b$, the constant network $v=1,a=1,o=0$ makes extended Eq.(3) equal two while the output is one. This witness depends on that extension. An empty-AND convention of zero avoids duplication but is absent from Eq.(2). Eq.(4) uses the correct nonempty sum.',
 '记录定义域/约定缺口及条件性反例，不能无说明把辅助扩展当作原定义再宣称原式已否定。','Record the domain/convention gap and conditional witness; an auxiliary extension is not silently treated as the source definition to refute the source expression.')
issue('dyn-issue-and-scope','普通交互与分量交互同名作用域','Ordinary and component dividends share a source name',[3,14],'notation_scope_ambiguity',r'I_{and}(S\mid x)',
 'Appendix A 七性质以完整模型 v 的普通交互使用该符号，主文 Eq.(2) 以 v_and 分量且只对非空S定义。','Appendix A uses ordinary dividends of the full model v, while main Eq.(2) applies the name to the v_and component and only nonempty S.',
 r'两实例分别是 $I_g$ 与 $I_a$；任意拆分参数不能使 $I_a$ 单独重构完整 $g$，也不能从 $g=g_1+g_2$ 自动推出任意分量间同样关系。',r'The instances are $I_g$ and $I_a$. An arbitrary split does not make $I_a$ alone reconstruct g, nor does $g=g_1+g_2$ imply the same relation among arbitrary components.',
 '七性质按普通全模型实例保留原前提并证明；符号表明确记录两个局部映射。','Prove the seven properties with their ordinary full-model instance and source premises; record the two local mappings separately.')
issue('dyn-issue-complement-half','Appendix E 半模型与裸 v 记号不一致','Appendix E mixes half-model and bare-v notation',[15,16],'notation_scope_ambiguity',r'v_{and}=v_{or}=0.5v;\quad I_{or}=-\sum_T(-1)^{|S|-|T|}v(x_{N\setminus T})',
 '原先明确两个分量等于0.5v，随后 Eq.(14)–(16) 用裸v写变换，未交代是否重新命名分量模型。','The source first sets both components to 0.5v, then uses bare v in Eq.(14)–(16) without specifying a local renaming.',
 r'若裸v仍是同一总模型，取一变量 $v(x)=x$、基线0、输入1，原分量 OR 为1/2，Eq.(14) 裸v右端为1。若裸v指固定分量o，则负补集恒等式准确，实际Lean验证此忠实局部解释。',r'If bare v remains the total model, the one-variable model $v(x)=x$ at baseline zero and input one has component OR value 1/2, whereas bare-v Eq.(14) gives one. If v denotes the fixed component o locally, the negative-complement identity is exact; Lean verifies that explicit local interpretation.',
 '保留原全部式与半模型前提；精确分量补集适配是有效子结果，不无说明宣称原每行缩放一致。','Retain every source equation and half-model premise. Exact component duality is a valid subresult, without claiming that every printed scaling is consistent.')
issue('dyn-issue-split-sign','Appendix C 的分量标签和噪声拆分符号','Component labels and the noise-split sign in Appendix C',[15],'definition_equation_error',r'v_{and}=\tfrac12(v-\delta)+\gamma,\quad v_{or}=\tfrac12(v-\delta)+\gamma',
 '原第一段把第二个分量也标为 AND，噪声段两个分量都加 gamma。','The first paragraph labels both components AND, and the noise paragraph adds gamma in both branches.',
 r'取 $v(x_T)=1,\delta_T=0,\gamma_T=1$，两个原噪声分量均为3/2，总和3而目标输出1。',r'For $v(x_T)=1,\delta_T=0,\gamma_T=1$, both printed noise components are 3/2 and their sum is three rather than one.',
 '保存原录文与精确反例；不把修改过的优化定义冒充原式。','Preserve the transcription and precise counterexample; an altered optimization definition is not substituted for the printed one.')
issue('dyn-issue-proposition1','Proposition 1 严格子句失败，一般单调性未决','Proposition 1 strictness fails; general monotonicity remains unresolved',[9,23],'statement_error_and_unresolved_clause',r'|T|<|T^\prime|\Longrightarrow\|\hat m_T\|_2/\|\hat m_{T^\prime}\|_2>1',
 '原命题未排零噪声，且原文仅给 Figure 3 数值验证，没有一般解析证明。','The source does not exclude zero noise and gives only Figure 3 numerical verification, without a general analytic proof.',
 r'$\sigma=0$ 时 $\hat M=I$，全部行范数1；例如一变量 $T=\varnothing,T\prime=\{1\}$ 的比为1而非大于1。Lean 给所有有限总体完整矩阵证明。',r'At $\sigma=0$, $\hat M=I$ and all row norms are one. For example, in a one-variable universe, the empty/singleton ratio is one rather than strictly greater. Lean proves the complete matrix boundary for every finite universe.',
 '仅严格原子句被反驳；同阶不变与真权重独立有效，正噪声一般阶数比及噪声单调子句保留未决，有限数值不替代。','Only the unconditional strict clause is refuted. Equal-order invariance and independence from true weights remain valid; general positive-noise order ratios and noise monotonicity remain unresolved, without replacing them by finite numerical checks.')
issue('dyn-issue-sparsity-transfer','补集恒等式不足以传递稀疏定理前提','Complement duality does not transfer the sparsity premises',[4,14,15,16],'unverified_external_adaptation',r'I_{or}(S\mid x)=-I_{and}(S\mid\tilde x)',
 '外引稀疏界有三个游戏条件，分量分解或反向输入尚未核实这些条件。','The cited sparsity bound has three game-level conditions, not established for split components or reversed inputs.',
 '精确的有限反演及补集变换只控制重构，不自动给最高阶零、平均单调与多项式界。','Exact inversion and complement transforms control reconstruction, but do not automatically imply a cutoff, monotone averages or a polynomial bound.',
 '外引适配保持范围审查，不冒称原渐近界机器已证。','The external adaptation remains a scope review, without claiming a machine proof of the original asymptotic bound.')

issue('dyn-issue-derivative-scale','Eq.(46) 导数漏公共归一化','Eq.(46) omits the common normalization in the derivative',[21],'proof_error',r'\partial\widetilde L/\partial w=-2E[(J+E)^\top]y+2E[(J+E)^\top(J+E)]w',
 'Eq.(45)损失有2^{-n}，Eq.(46)导数未带该公共因子。','Loss Eq.(45) has the common factor 2^{-n}, which is absent from its derivative in Eq.(46).',
 r'真实梯度是原Eq.(46)右端乘 $2^{-n}$。该因子严格正，所以设梯度为0时得到同一正规方程；不改变唯一最优结论。',r'The actual gradient is the printed right side of Eq.(46) multiplied by $2^{-n}$. This factor is strictly positive, so setting the gradient to zero yields the same normal equations and optimum.',
 '保留原导数式，重写直接精确期望和完成平方，不依赖该漏因子。','Retain the printed derivative; exact expectations and completing the square prove the same conclusion without that omission.')
issue('dyn-issue-permutation-involution','原排列构造未说明每步为换位','The permutation construction does not specify involutive factors',[23],'missing_proof_construction',r'P_i^2=I\quad\text{for permutation matrices }P_i',
 'Eq.(63)之后用P_i平方为单位，但此前只称每个P_i是permutation matrix，未说明是换位矩阵。','After Eq.(63), the proof uses P_i squared equal to the identity, although each P_i was described only as a permutation matrix rather than a transposition matrix.',
 r'三循环排列的平方不为单位。可以把所需有限变量排列分解为换位，各因子才满足该性质；也可直接对整体P用 $P^{-1}$ 共轭。实际Lean与重写使用正确的逆和置换。',r'A three-cycle does not square to the identity. Decomposing a finite variable permutation into transpositions makes the claim valid for its factors; alternatively conjugate by the inverse $P^{-1}$ of the whole permutation. Lean and the rewritten proof use the correct inverse and permutation.',
 '这是缺少构造说明的证明缺口，Theorem4同阶范数结论未被否定。','This is a missing construction detail in the proof, not a refutation of the equal-order norm conclusion of Theorem 4.')

links={
 'dyn-universal':['dyn-issue-or-grouping','dyn-issue-eq3-empty'], 'dyn-taylor':['dyn-issue-taylor'],
 'dyn-trigger-representation':['dyn-issue-taylor','dyn-issue-zero-trigger'], 'dyn-binary-trigger':['dyn-issue-zero-trigger'],
 'dyn-noisy-output':['dyn-issue-marginal-independence','dyn-issue-trigger-variance'],
 'dyn-regression':['dyn-issue-derivative-scale','dyn-issue-expectation','dyn-issue-gram-determinant','dyn-issue-label-transpose','dyn-issue-trigger-variance','dyn-issue-zero-trigger','dyn-issue-taylor'],
 'dyn-equal-order':['dyn-issue-permutation-involution'], 'dyn-order-monotonic':['dyn-issue-proposition1'], 'dyn-extraction':['dyn-issue-split-sign'],
 'dyn-complement':['dyn-issue-complement-half','dyn-issue-sparsity-transfer'], 'dyn-split-labels':['dyn-issue-split-sign'],'dyn-noise-split':['dyn-issue-split-sign'],'dyn-sparsity':['dyn-issue-sparsity-transfer']}
original_math={
 'dyn-cutoff':r'\forall S\in\{S\subseteq N:|S|\ge M+1\},\ I_{and}(S\mid x)=0',
 'dyn-mask-monotonic':r'\bar u^{(k)}\overset{def}=E_{|S|=k}[v(x_S)-v(x_\varnothing)],\quad\forall k^\prime\le k,\bar u^{(k^\prime)}\le\bar u^{(k)}',
 'dyn-mask-polynomial':r'\forall k^\prime\le k,\quad\bar u^{(k^\prime)}\ge(k^\prime/k)^p\bar u^{(k)},\quad p>0',
 'dyn-uniqueness':r'(-1)^{|S|-|T|}',
 'dyn-split-labels':r'v_{and}(x_T)=0.5v(x_T)+\gamma_T,\quad v_{and}(x_T)=0.5\cdot v(x_T)-\gamma_T',
 'dyn-noise-split':r'v_{and}(x_T)=0.5(v(x_T)-\delta_T)+\gamma_T,\quad v_{or}(x_T)=0.5(v(x_T)-\delta_T)+\gamma_T,\quad\delta_T\in[-\zeta,\zeta],\quad\zeta=0.02|v(x)-v(x_\varnothing)|',
 'dyn-complement':r'I_{or}(S\mid x)=-I_{and}(S\mid\tilde x),\quad v_{and}(\cdot)=v_{or}(\cdot)=0.5v(\cdot)',
 'dyn-efficiency':r'v(x)=\sum_{S\subseteq N}I_{and}(S\mid x)',
 'dyn-linearity':r'\left[\forall S\subseteq N,\ v(x_S)=v_1(x_S)+v_2(x_S)\right]\Longrightarrow\left[\forall S\subseteq N,\ I^v_{and}(S\mid x)=I^{v_1}_{and}(S\mid x)+I^{v_2}_{and}(S\mid x)\right]',
 'dyn-dummy':r'\left[\forall S\subseteq N\setminus\{i\},\ v(x_{S\cup\{i\}})=v(x_S)+v(x_{\{i\}})\right]\Longrightarrow\left[\forall\varnothing\ne S\subseteq N\setminus\{i\},\ I_{and}(S\cup\{i\}\mid x)=0\right]',
 'dyn-symmetry':r'\left[\forall S\subseteq N\setminus\{i,j\},\ v(x_{S\cup\{i\}})=v(x_{S\cup\{j\}})\right]\Longrightarrow\left[\forall S\subseteq N\setminus\{i,j\},\ I_{and}(S\cup\{i\}\mid x)=I_{and}(S\cup\{j\}\mid x)\right]',
 'dyn-anonymity':r'\forall S\subseteq N,\ I^v_{and}(S\mid x)=I^{\pi v}_{and}(\pi S\mid x),\quad\pi S=\{\pi(i):i\in S\},\quad(\pi v)(x_{\pi S})=v(x_S)',
 'dyn-recursion':r'\forall S\subseteq N\setminus\{i\},\ I_{and}(S\cup\{i\}\mid x)=I_{and}(S\mid x,i\text{ always present})-I_{and}(S\mid x),\quad I_{and}(S\mid x,i\text{ always present})=\sum_{L\subseteq S}(-1)^{|S|-|L|}v(x_{L\cup\{i\}})',
 'dyn-distribution':r'v_T(x_S)=\begin{cases}c&T\subseteq S,\\0&\text{otherwise},\end{cases}\quad I_{and}(T\mid x)=c,\quad\forall S\ne T,\ I_{and}(S\mid x)=0',
 'dyn-interaction-definition':r'I_{and}(S\mid x)=\sum_{T\subseteq S}(-1)^{|S|-|T|}v_{and}(x_T),\quad I_{or}(S\mid x)=-\sum_{T\subseteq S}(-1)^{|S|-|T|}v_{or}(x_{N\setminus T}),\quad v_{and}(x_T)=0.5v(x_T)+\gamma_T,\ v_{or}(x_T)=0.5v(x_T)-\gamma_T',
 'dyn-regression':r'\hat w=\arg\min_w\widetilde L(w)=(J^\top J+2^n\operatorname{diag}(c))^{-1}J^\top y=(J^\top J+2^n\operatorname{diag}(c))^{-1}J^\top Jw^*=\hat Mw^*,\quad J=[\mathbf J(x_{S_1}),\ldots,\mathbf J(x_{S_{2^n}})]^\top,\quad y=[y(x_{S_1}),\ldots,y(x_{S_{2^n}})]^\top,\quad c=\operatorname{vec}\{\operatorname{Var}\epsilon_T=2^{|T|}\sigma^2:T\subseteq N\}',
 'dyn-noisy-output':r'\forall S\subseteq N,\ \widetilde v(x_S)=v(x_S)+\Delta v_S,\quad\Delta v_S\sim\mathcal N(0,\sigma^2);\quad\forall\varnothing\ne T\subseteq N,\ \widetilde I(T\mid x)=I(T\mid x)+\Delta I_T,\quad E\Delta I_T=0,\quad\operatorname{Var}\Delta I_T=2^{|T|}\sigma^2;\quad\widetilde J_T(x)=J_T(x)+\epsilon_T,\quad\epsilon_T=\Delta I_T/w_T,\quad E\epsilon_T=0,\quad\operatorname{Var}\epsilon_T\propto2^{|T|}\sigma^2',
 'dyn-equal-order':r'\hat w_T=\hat m_T^\top w^*,\quad\hat M=[\hat m_{T_1},\ldots,\hat m_{T_{2^n}}]^\top;\quad\forall T,T^\prime\subseteq N,\ |T|=|T^\prime|\Longrightarrow\|\hat m_T\|_2=\|\hat m_{T^\prime}\|_2',
 'dyn-order-monotonic':r'\forall T,T^\prime\subseteq N,\ |T|<|T^\prime|\Longrightarrow\|\hat m_T\|_2/\|\hat m_{T^\prime}\|_2>1;\quad\text{the ratio decreases monotonically as }\sigma^2\text{ decreases during training};\quad\|\hat m_T\|_2\text{ depends only on }n,\sigma^2,|T|\text{ and is agnostic to }\{w_T^*:T\subseteq N\}',
 'dyn-universal':r'\forall S\subseteq N,\ f(\hat x_S)=v(\hat x_S),\quad f(\hat x_S)=v(\hat x_\varnothing)+\sum_{T\subseteq N}I_{and}(T\mid\hat x)\mathbf1(\hat x_S\text{ triggers AND }T)+\sum_{T\subseteq N}I_{or}(T\mid\hat x)\mathbf1(\hat x_S\text{ triggers OR }T)\tag{3}\\=v(x=\hat x_\varnothing)+\sum_{\varnothing\ne T\subseteq S}I_{and}(T\mid x=\hat x)+\sum_{T\subseteq N:T\cap S\ne\varnothing}I_{or}(T\mid x=\hat x)\tag{4}\\\approx v(x=\hat x_\varnothing)+\sum_{T\in\Omega_{and}:\varnothing\ne T\subseteq S}I_{and}(T\mid x=\hat x)+\sum_{T\in\Omega_{or}:T\cap S\ne\varnothing}I_{or}(T\mid x=\hat x)\tag{5}',
 'dyn-taylor':r'I(T\mid x)=\sum_{\pi\in Q_T}\frac1{\prod_{i=1}^n\pi_i!}\left.\frac{\partial^{\pi_1+\cdots+\pi_n}v}{\partial x_1^{\pi_1}\cdots\partial x_n^{\pi_n}}\right|_{x=x_\varnothing}\prod_{i\in T}(x_i-b_i)^{\pi_i},\quad Q_T=\{[\pi_1,\ldots,\pi_n]^\top:\forall i\in T,\pi_i\in\mathbb N^+;\forall i\notin T,\pi_i=0\}',
 'dyn-extraction':r'v(x_T)=v_{and}(x_T)+v_{or}(x_T),\quad v_{and}(x_T)=0.5v(x_T)+\gamma_T,\quad v_{and}(x_T)=0.5v(x_T)-\gamma_T;\quad\min_{\{\gamma_T\}}\sum_{S\subseteq N}(|I_{and}(S\mid x)|+|I_{or}(S\mid x)|)\tag{11}\\v_{and}(x_T)=0.5(v(x_T)-\delta_T)+\gamma_T,\quad v_{or}(x_T)=0.5(v(x_T)-\delta_T)+\gamma_T,\quad\delta_T\in[-\zeta,\zeta],\quad\zeta=0.02|v(x)-v(x_\varnothing)|',
 'dyn-salience':r'v(x)=\log\frac{p(y^{truth}\mid x)}{1-p(y^{truth}\mid x)},\quad\tau=0.03E_x|v(x)-v(x_\varnothing)|,\quad I_{real}^{(k)}=\frac{E_x[\sum_{type\in\{and,or\}}\sum_{S:|S|=k,|I_{type}(S\mid x)|\ge\tau}|I_{type}(S\mid x)|]}Z,\quad Z=E_{1\le k^\prime\le n}E_x[\sum_{type\in\{and,or\}}\sum_{S:|S|=k^\prime,|I_{type}(S\mid x)|\ge\tau}|I_{type}(S\mid x)|]'
}
# Each tuple supplies an actual symbol meaning in both languages, including domain and boundaries.
S=[
 ('model-output','sym-model',r'v',r'g(S)=v(x_S)','实值网络输出','Real-valued network output','固定参数网络的分类实数分数。','A real classification score from a network with fixed parameters.','输入空间到实数的函数','A function from the input space to the reals'),
 ('masked-input','sym-mask',r'x_S',r'(x_S)_i=x_i\ (i\in S),\ r_i\ (i\notin S)','掩码输入','Masked input','保留集内输入，其余为同一输入基线。','Retain coordinates in the coalition and use the same input baseline elsewhere.','有限坐标实向量','Real vectors indexed by a finite universe'),
 ('set-game','sym-game',r'g',r'g(S)=v(x_S)','原始掩码游戏','Raw masked game','同一个输入和基线的全部掩码输出。','All masked outputs for the same input and baseline.','幂集到实数的函数','A function from the powerset to the reals'),
 ('output-baseline','sym-output-baseline',r'b',r'b=g(\varnothing)','输出基线','Output baseline','全遮罩输出的标量，原文记作v(x_empty)。','The scalar output on the fully masked input, written v(x_empty) in the source.','实数标量','A real scalar'),
 ('input-baseline','sym-input-baseline',r'r_i',r'r_i=b_i\text{ (source)}','输入基线向量','Input baseline vector','原b_i是坐标遮罩值，与标量输出基线不同。','Source b_i is a coordinate masking value and differs from the scalar output baseline.','有限坐标实向量','Real vectors indexed by a finite universe'),
 ('dyn-centered-game','sym-centered-game',r'g_0',r'g_0(S)=g(S)-b','中心化游戏','Centered game','仅用于明确移除同一输出基线，非替换原始交互定义。','Explicitly removes the common output baseline; it does not replace the raw source dividend definition.','幂集到实数的函数','A function from the powerset to the reals'),
 ('dyn-dividend','sym-and-interaction',r'I_g',r'I_g(S)=\sum_{T\subseteq S}(-1)^{|S|-|T|}g(T)','原始游戏交互','Raw-game dividend','总模型游戏的Möbius交互，区别于分量交互。','The Möbius dividend of the total model game, distinct from component dividends.','幂集到实数的函数','A function from the powerset to the reals'),
 ('dyn-and-component','sym-and-output',r'a',r'a(S)=g(S)/2+\gamma_S','AND 分量输出','AND component output','原vand，仅对固定分解定义。','Source vand for a fixed decomposition.','幂集到实数的函数','A function from the powerset to the reals'),
 ('dyn-or-component','sym-or-output',r'o',r'o(S)=g(S)/2-\gamma_S','OR 分量输出','OR component output','原vor，与AND分量合成原游戏。','Source vor, which sums with the AND component to the raw game.','幂集到实数的函数','A function from the powerset to the reals'),
 ('dyn-gamma','sym-decomposition-parameter',r'\gamma_S',r'a+o=g','分解参数','Decomposition parameter','每个遮罩的L1提取优化变量。','An L1 extraction variable for each mask.','幂集索引的实向量','Real vectors indexed by the powerset'),
 ('dyn-and-dividend','sym-and-component-interaction',r'A(S)',r'A(S)=I_a(S)\ (S\ne\varnothing)','AND 分量交互','AND component dividend','原Iand在分量定义中作用于a，不等于总模型I_g。','Source Iand applies to a in the component definition, rather than automatically to the total game.','幂集到实数的函数','A function from the powerset to the reals'),
 ('dyn-or-dividend','sym-or-component-interaction',r'O(S)',r'O(S)=-I_{L\mapsto o(N\setminus L)}(S)\ (S\ne\varnothing)','OR 分量交互','OR component dividend','原Ior是补集游戏的负交互，非空时由与遮罩相交激活。','Source Ior is the negative dividend of the complementary game; a nonempty coalition activates by intersecting the mask.','非空幂集到实数的函数','A function from nonempty coalitions to the reals'),
 ('dyn-trigger','dyn-trigger',r'J_T',r'J_T(x_S)=\mathbf1_{T\subseteq S}','归一化概念触发','Normalized concept trigger','Taylor支持贡献除以固定参考交互；零分母域单列。','A support contribution divided by its fixed reference dividend; the zero denominator is recorded separately.','输入到实数的函数；二值遮罩子域','Real functions of input, with a binary masked subdomain'),
 ('dyn-weight','dyn-weight',r'w_T',r'w_T=I(T\mid\hat x)','回归概念权重','Regression concept weight','参考样本的原始交互，回归中是优化变量。','The reference-sample dividend, treated as an optimization variable in regression.','幂集索引的实向量','Real vectors indexed by the powerset'),
 ('dyn-true-weight','dyn-true-weight',r'w_T^*',r'y=Jw^*','收敛交互目标','Converged dividend target','最终收敛DNN的交互，不定义为理想任务表征。','The finally converged DNN dividends, not necessarily an ideal task representation.','幂集索引的实向量','Real vectors indexed by the powerset'),
 ('dyn-noise','dyn-noise',r'\epsilon_T',r'E\epsilon_T=0,\quad c_T=\operatorname{Var}\epsilon_T','触发噪声','Trigger noise','Lemma1的缩放噪声与Assumption1的独立替代噪声区分。','Distinguish scaled noise in Lemma 1 from independently imposed surrogate noise in Assumption 1.','概率空间上的实随机变量族','Families of real random variables on a probability space'),
 ('dyn-noise-variance','dyn-noise-variance',r'c_T',r'c_T=2^{|T|}\sigma^2\text{ in Assumption 1}','独立触发方差','Independent trigger variance','原Assumption1重设的方差，不由除w自动推出。','The variance reset by Assumption 1, not automatically obtained by dividing by w.','非负实数向量','Vectors of nonnegative reals'),
 ('dyn-design','dyn-design',r'J_{ST}',r'J_{ST}=\mathbf1_{T\subseteq S}','完整幂集设计','Complete powerset design','行是遮罩S，列是概念T；含空行与空列。','Rows are masks S and columns are concepts T, including the empty row and column.','2^n乘2^n实矩阵','Real matrices of size 2^n by 2^n'),
 ('dyn-transfer','dyn-transfer',r'\hat M',r'\hat M=(J^\top J+2^n\operatorname{diag}c)^{-1}J^\top J','噪声回归转移矩阵','Noisy-regression transfer matrix','把真交互目标变成同噪声水平的最优交互。','Maps true target dividends to optimal dividends at the fixed noise level.','2^n乘2^n实矩阵','Real matrices of size 2^n by 2^n'),
 ('dyn-order','sym-order',r'k',r'k=|S|','概念阶数','Concept order','概念内参与变量数，区别于训练epoch与Taylor总次数。','The number of variables in a concept, distinct from epochs and total Taylor degree.','0到n的自然数','Natural numbers between zero and n'),
 ('dyn-taylor-index','dyn-taylor-index',r'\pi\in Q_T',r'\pi_i>0\ (i\in T),\quad\pi_i=0\ (i\notin T)','Taylor 支持多重指标','Taylor support multi-index','Q_T规定严格正次数支持恰为T。','Q_T specifies that the positive-degree support is exactly T.','有限坐标自然数向量','Natural-number vectors indexed by the finite universe'),
 ('dyn-threshold','dyn-threshold',r'\tau',r'\tau=0.03E_x|v(x)-v(x_\varnothing)|','显著交互阈值','Salient-dividend threshold','经验阈值与理论回归阈值分别使用原作用域。','Empirical and theoretical-regression thresholds retain their separate source scopes.','非负实数','A nonnegative real'),
 ('dyn-salient','dyn-salient',r'\Omega',r'\Omega=\{S:|I(S)|\ge\tau\}','显著支持族','Salient support family','由指定分量和指定阈值筛选的集合族。','A coalition family selected for the stated component and threshold.','幂集的子族','Subfamilies of the powerset'),
 ('dyn-strength','dyn-strength',r'I_{real}^{(k)}',r'I_{real}^{(k)}=\text{salient order strength}/Z','归一化阶数强度','Normalized order strength','同阶显著交互的绝对值和按原Z归一化。','The sum of magnitudes of same-order salient dividends normalized by source Z.','Z非零域的非负实数','Nonnegative reals on the domain Z nonzero'),
 ('dyn-cutoff-order','dyn-cutoff-order',r'M',r'|S|>M\Longrightarrow I(S)=0','最高非零交互阶数','Maximum nonzero interaction order','外引稀疏条件1的严格最高阶，不是经验几乎为零。','The exact cutoff in cited sparsity Condition 1, rather than empirical near-zero values.','自然数','A natural number'),
]
symbols=[]
for i,ci,tex,definition,zname,ename,zdesc,edesc,zdom,edom in S:
 pages={'model-output':[3,4,5,7],'masked-input':[3,15],'set-game':[3,4],'output-baseline':[4,7,16],'input-baseline':[3,7,15,18],'dyn-centered-game':[14],'dyn-dividend':[14],'dyn-and-component':[3,4,15,16],'dyn-or-component':[3,4,15,17],'dyn-gamma':[4,15],'dyn-and-dividend':[3,4,14,16],'dyn-or-dividend':[3,4,15,16,17],'dyn-trigger':[6,7,8,19,20,22],'dyn-weight':[6,7,8,19,20],'dyn-true-weight':[7,8,9,24],'dyn-noise':[7,8,20,21],'dyn-noise-variance':[8,21,22],'dyn-design':[8,21,22,23],'dyn-transfer':[8,9,22,23,24],'dyn-order':[5,9,14],'dyn-taylor-index':[7,18,19],'dyn-threshold':[4,5,24,27,28],'dyn-salient':[4,5,14,27],'dyn-strength':[5,9,24,27,28],'dyn-cutoff-order':[14]}[i]
 ze='空集保留原输出基线；原特殊分量和触发约定按相关条目明示。';ee='The empty set retains the raw output baseline; special component and trigger conventions are stated in their entries.'
 if i=='dyn-centered-game':ze='中心化游戏在空集严格为零。';ee='The centered game is exactly zero on the empty set.'
 if i=='dyn-and-dividend':ze='主文Eq.(2)只定义非空分量AND；机器辅助完整Möbius扩展的空项为a(empty)，不冒充原文约定。';ee='Main Eq.(2) defines only nonempty component AND dividends. The auxiliary full Möbius extension has empty value a(empty), which is not claimed to be the source convention.'
 if i=='dyn-or-dividend':ze='仅非空系数使用负补集公式；原F.1设OR空输出为零。';ee='The negative-complement formula is used for nonempty coefficients; F.1 sets the empty OR output to zero.'
 if i in ['dyn-trigger','dyn-weight','dyn-true-weight']:ze='原w_empty=v(x_empty)，J_empty=1。';ee='The source sets w_empty=v(x_empty) and J_empty=1.'
 zb='规范输出基线b=g(empty)不默认零；原输入b_i统一映为r_i。';eb='The canonical output baseline b=g(empty) is not assumed zero; source input b_i maps to r_i.'
 zm='按此符号的局部定义映射；不把总输出、分量、触发和回归向量混同。';em='Map by this local definition; total outputs, components, triggers and regression vectors are distinguished.'
 mapping=dict(paper_id=pid,version_id=vid,source_id=sid,original_tex={'input-baseline':r'b_i','set-game':r'v(x_S)','output-baseline':r'v(x_\varnothing)','dyn-dividend':r'I_{and}(S\mid x)\text{ (Appendix A)}','dyn-and-component':r'v_{and}(x_S)','dyn-or-component':r'v_{or}(x_S)','dyn-and-dividend':r'I_{and}(S\mid x)','dyn-or-dividend':r'I_{or}(S\mid x)'}.get(i,tex),original_definition=definition,pdf_pages=pages,canonical_concept=ci,relationship='renaming_or_explicit_local_instance',note=zm,conflict_note=zb,translations=dict(en=dict(note=em,conflict_note=eb)))
 symbols.append(dict(id=i,canonical_id=ci,canonical_tex=tex,definition_tex=definition,name_zh=zname,description_md=zdesc,type_or_domain=zdom,scope='本篇固定输入、基线、分解或回归设置；依相关条目的局部量词。',assumptions=[],empty_set_convention=ze,baseline_convention=zb,aliases=[mapping['original_tex']],paper_mappings=[mapping],lean_names=[],version='1.0',translations=dict(en=dict(name_zh=ename,name=ename,description_md=edesc,type_or_domain=edom,scope='This paper at a fixed input, baseline, split or regression setting, according to each entry’s local quantifiers.',assumptions=[],empty_set_convention=ee,baseline_convention=eb))))
base=['model-output','masked-input','set-game','output-baseline','input-baseline','dyn-dividend']
local={
 'dyn-split-labels':['dyn-gamma','dyn-and-component','dyn-or-component'],'dyn-noise-split':['dyn-gamma','dyn-and-component','dyn-or-component'],
 'dyn-universal':['dyn-and-component','dyn-or-component','dyn-gamma','dyn-and-dividend','dyn-or-dividend'],
 'dyn-complement':['dyn-or-component','dyn-or-dividend'], 'dyn-interaction-definition':['dyn-and-component','dyn-or-component','dyn-and-dividend','dyn-or-dividend'],
 'dyn-taylor':['dyn-taylor-index'],'dyn-trigger-representation':['dyn-trigger','dyn-weight','dyn-taylor-index'],'dyn-binary-trigger':['dyn-trigger','dyn-weight'],
 'dyn-noisy-output':['dyn-noise','dyn-noise-variance','dyn-weight'], 'dyn-regression':['dyn-noise','dyn-noise-variance','dyn-design','dyn-transfer','dyn-weight','dyn-true-weight'],
 'dyn-equal-order':['dyn-design','dyn-transfer','dyn-order'],'dyn-order-monotonic':['dyn-design','dyn-transfer','dyn-order','dyn-true-weight'],
 'dyn-zero-noise':['dyn-design','dyn-transfer','dyn-weight','dyn-true-weight'], 'dyn-salience':['dyn-threshold','dyn-salient','dyn-strength','dyn-order'],
 'dyn-extraction':['dyn-gamma','dyn-and-component','dyn-or-component'],'dyn-sparsity':['dyn-salient','dyn-threshold','dyn-cutoff-order'],
 'dyn-cutoff':['dyn-cutoff-order'],'dyn-mask-monotonic':['dyn-centered-game','dyn-order'],'dyn-mask-polynomial':['dyn-centered-game','dyn-order'],
 'dyn-regression-definition':['dyn-design','dyn-noise','dyn-noise-variance','dyn-weight','dyn-true-weight'], 'dyn-first-phase':['dyn-transfer','dyn-order']}
for ai in ['dyn-efficiency','dyn-linearity','dyn-dummy','dyn-symmetry','dyn-anonymity','dyn-recursion','dyn-distribution']:links[ai]=['dyn-issue-and-scope']
results=[]
for ent in inv['entries']:
 i=ent['id'];en,tex,key,src,z,e,role=D[i];z=clean(z);e=clean(e)
 if i=='dyn-complement':key='dyn-complement';src=None
 if i=='dyn-taylor':tex=tex.replace('b_i','r_i')
 zp=z.split('\n\n');ep=e.split('\n\n');assert len(zp)==len(ep),(i,len(zp),len(ep))
 st=[];et=[]
 for j,(zz,ee) in enumerate(zip(zp,ep)):
  tz,te=titles.get(i,[(ent['title'],en)]*len(zp))[j]
  rr=maps.get(i,[[]]*len(zp));names=rr[j] if j<len(rr) else []
  names=[n for n in names if n in cat]
  st.append(dict(id=f'{i}-step-{j+1}',title=tz,body_md=zz,formula_tex='',lean_refs=[ref(n) for n in names]))
  et.append(dict(id=f'{i}-step-{j+1}',title=te,body_md=ee))
 names=list(dict.fromkeys(r['declaration'] for s in st for r in s['lean_refs']))
 loc=ent['statement_location'];pfs=ent['proof_location'];ps=sorted(set(loc['pdf_pages']+pfs['pdf_pages']))
 az,ae=zip(*assumptions[i]) if i in assumptions else ([],[])
 # Formula, local quantities and normalization are displayed before derivation in both languages.
 defs=[dict(id=i+'-game-objects',body_md=OBJ_Z)]
 edefs=[dict(id=i+'-game-objects',body_md=OBJ_E)]
 if i in local_defs:
  dz,de=local_defs[i];defs.append(dict(id=i+'-local-objects',body_md=dz));edefs.append(dict(id=i+'-local-objects',body_md=de))
 if i in ['dyn-efficiency','dyn-linearity','dyn-dummy','dyn-symmetry','dyn-anonymity','dyn-recursion','dyn-distribution']:
  defs.append(dict(id=i+'-raw-scope',body_md=r'本条 Appendix A 的原 $I_{and}$ 解释为完整模型 $v$ 的普通 Harsanyi 交互 $I_g$，包含空项 $I_g(\varnothing)=b$。主文Eq.(2)同名系数只定义非空AND分量交互 $I_a$；两者是不同概念实例。'))
  edefs.append(dict(id=i+'-raw-scope',body_md=r'Appendix A uses source $I_{and}$ as the ordinary Harsanyi dividend $I_g$ of the full model v, including $I_g(\varnothing)=b$. The same name in main Eq.(2) denotes only nonempty component dividends $I_a$. These are distinct concept instances.'))
  src=None
 note=[dict(original='v(x_S)',canonical='g(S)=v(x_S)',note='固定相同输入与基线的原始输出游戏，空项为b。'),dict(original='b_i',canonical='r_i',note='原输入基线坐标；与标量输出基线b严格区分。')]
 enote=[dict(original='v(x_S)',canonical='g(S)=v(x_S)',note='The raw masked game at the same input and baseline; its empty term is b.'),dict(original='b_i',canonical='r_i',note='Source input-baseline coordinates, distinct from scalar output baseline b.')]
 for sym in symbols:
  if sym['id'] in local.get(i,[]):
   note.append(dict(original=sym['paper_mappings'][0]['original_tex'],canonical=sym['canonical_tex'],note=sym['description_md']));enote.append(dict(original=sym['paper_mappings'][0]['original_tex'],canonical=sym['canonical_tex'],note=sym['translations']['en']['description_md']))
 otex=original_math.get(i,tex)
 original=(src+'\n\n' if src else '')+'原 '+ent['original_label']+' 完整数学陈述（原符号）：\n\\['+otex+'\\]'
 if i=='dyn-salience':original+=r'\n理论指标（原第10页）：$I_{theo}^{(k)}=E_x[\sum_{S:|S|=k,|\hat w_S|\ge\tau_{theo}}|\hat w_S|]/Z_{theo}$，$Z_{theo}=E_{1\le k\prime\le n}E_x[\sum_{S:|S|=k\prime,|\hat w_S|\ge\tau_{theo}}|\hat w_S|]$，$v_{theo}(x)=\sum_{S\subseteq N}\hat w_S$，$\tau_{theo}=0.03|v_{theo}(x)-\hat w_\varnothing|$。'
 if i=='dyn-regression-definition':original+=' 原Assumption1另外规定不同触发噪声相互独立，统一重设上述方差，零均值沿用噪声定义。'
 if i=='dyn-order-monotonic':original+=r'\n全部原子句另包括：范数只由n、sigma平方和阶数决定，而与最终真交互w*无关。原文称通过Figure3实验验证，并未给一般解析证明。'
 if i=='dyn-uniqueness':original+=r' Appendix D 引用[13]/[23]称这个系数是唯一保证每个遮罩输出由内部交互和精确重构的系数；原文没有另写候选系数族d的公式。候选族的精确形式化放在重写区。'
 if i=='dyn-interaction-definition':original+=r'\n原定义明确S⊆N且S≠empty，主文分量公式不赋值空交互。'
 if i=='dyn-universal':original+=r'\nEq.(3)原AND和写T⊆N并另加v(x_empty)；Eq.(4)改写为非空T⊆S；Eq.(5)将两个和限制为显著族并使用近似号。F.1另规定AND空输出为原基线、OR空输出为0。三个编号差别保留，不将近似或空项错误省略。'
 sourceproof=T[key] if key else ('本条没有独立本地作者证明；原定义、外引说明或实验材料已在原陈述和来源页记录。')
 assessment='partially_refuted' if i in ['dyn-order-monotonic','dyn-noisy-output'] else 'refuted' if i in ['dyn-taylor','dyn-split-labels','dyn-noise-split'] else 'scope_under_review' if role in ['partial_proof','scope_analysis'] else 'no_statement_error_recorded'
 scopez=z if role in ['partial_proof','counterexample','scope_analysis'] else ('完整有限命题的重写与实际声明已适配。' if role=='complete_proof' else '原定义或经验范围的完整解释；不计为普遍数学定理。')
 scopee=e if role in ['partial_proof','counterexample','scope_analysis'] else ('The complete finite claim is rewritten and adapted to actual declarations.' if role=='complete_proof' else 'The source definition or empirical scope is fully explained; it is not counted as a universal mathematical theorem.')
 lr='none' if not names else 'counterexample' if i=='dyn-noise-split' else 'partial_component' if role in ['partial_proof','scope_analysis','counterexample'] or i=='dyn-universal' else 'theorem_proof'
 lean=dict(status='partial_scope_verified' if names and lr=='partial_component' else 'verified' if names else 'not_applicable',declarations=names,compiled=bool(names),scope=scopee,evidence_role=lr,encoding_note='The finite universe is a type α and every mask/concept is Finset α. All empty coordinates are retained. Integral hypotheses have their actual measure-theoretic meanings; no source proposition is assumed as a Lean premise.',statement_md='\n\n'.join(cat[n]['signature'] for n in names) if names else 'No additional Lean declaration is claimed for this source-material entry.',source_semantics_automatically_verified=False)
 if names:
  lean.update(report_path=str((P/'verification/report.json').relative_to(R)),build_id=report['build_id'],source_fingerprint=report['source_fingerprint'],axiom_audit='passed',axioms=sorted({a for n in names for a in cat[n]['axioms']}),step_map=[dict(step_id=s['id'],**r) for s in st for r in s['lean_refs']])
 
 if i in ['dyn-regression','dyn-equal-order','dyn-zero-noise']:
  scopez+=' 回归证明以已给定的Boolean zeta设计为模型内对象，不解决任意DNN上游Taylor收敛或零系数触发的定义问题。期望之和只依赖各行共同边缘，无需跨行独立；同一随机函数表示共同边缘而非强制论文各行完全相关。原均匀平均由meanNoisyLoss显式定义，正card倒数保持唯一最优。'
  scopee+=' The regression proof takes the Boolean zeta design as a given object inside the model. It does not resolve upstream Taylor convergence or zero-coefficient trigger definitions for arbitrary DNNs. The sum of expectations depends only on the common row marginals, without requiring cross-row independence; one random family represents those marginals, rather than imposing perfect row correlation on the source. The original uniform average is explicitly meanNoisyLoss, whose positive cardinality normalization preserves the unique minimizer.'
  lean['scope']=scopee
 rr={'complete_proof':'proof','partial_proof':'partial_component','counterexample':'partial_proof_with_refuted_clause','scope_analysis':'statement_scope_explanation','definition':'source_material','empirical':'source_material'}[role]
 if i=='dyn-taylor':rr='counterexample'
 lean['translations']={'en':dict(scope=scopee,encoding_note=lean['encoding_note'],statement_md=lean['statement_md'])}
 results.append(dict(id=i,paper_id=pid,title=ent['title'],kind=ent['kind'],original_label=ent['original_label'],inventory_ids=[i],source_refs=[dict(source_id=sid,version_id=vid,pdf_pages=ps,section=loc['section'])],statement_tex=tex,assumptions=list(az),definitions=defs,original_statement_md=clean(original),original_proof_md=sourceproof,original_statement_source_type='formal_mathematical_transcription_with_project_chinese_translation',original_proof_source_type='formal_complete_mathematical_transcription_with_project_chinese_translation' if key else 'no_local_author_proof',source_transcription_status='complete_statement_and_author_proof' if key else 'complete_statement_no_local_author_proof',overview=zp[0],proof_steps=st,shared_proof_ids=shared_map.get(i,[]),symbol_ids=base+local.get(i,[]),notation_map=note,rewrite_status='complete',rewrite_role=rr,statement_assessment=assessment,proof_scope=scopez,completion_scope=scopez,alignment_status='agent_checked_statement_and_proof_boundaries',user_review_status='pending',lean=lean,related_issue_ids=links.get(i,[]),translations=dict(en=dict(title=en,overview=ep[0],assumptions=list(ae),definitions=edefs,proof_steps=et,notation_map=enote,proof_scope=scopee,completion_scope=scopee,original_statement_md=en+':\n\\['+otex+'\\]'))))
def shared(i,ztitle,etitle,tex,z,e,decls):
 zp=clean(z).split('\n\n');ep=clean(e).split('\n\n');assert len(zp)==len(ep)
 steps=[];es=[]
 labels={
 'dyn-shared-polynomial-support':[('检查正次单项式的遮罩','Mask positive-degree monomials'),('分组支持并归一化非零贡献','Group supports and normalize nonzero contributions')],
 'dyn-shared-independent-residual':[('分解独立产品的一阶与二阶积分','Factor first and second product moments'),('计算中心化加权残差','Compute centered weighted residuals'),('由 Gaussian 映射律得到矩','Derive moments from Gaussian map-laws')],
 'dyn-shared-positive-regression':[('逐行精确展开期望','Expand row expectations exactly'),('证明 Gram 正定并完成平方','Prove Gram positivity and complete the square'),('代入标签并保留源定义域','Substitute labels and preserve source domains')]}
 for k,(zz,ee) in enumerate(zip(zp,ep)):
  ns=decls[k] if k<len(decls) else []
  lz,le=labels[i][k]
  steps.append(dict(id=i+f'-step-{k+1}',title=lz,body_md=zz,formula_tex='',lean_refs=[ref(n) for n in ns]))
  es.append(dict(id=i+f'-step-{k+1}',title=le,body_md=ee))
 if i=='dyn-shared-polynomial-support':
  az=[r'有限坐标总体；有限单项式索引集P，每项k的支持A_k与自然次数d_{k,i}满足i∈A_k时严格正；每项实系数c_k，不要求支持互异。'];ae=[r'A finite coordinate universe and finite monomial index set P. Each support A_k has strictly positive natural degrees on its coordinates and a real coefficient c_k. Distinct terms may share a support.']
  dz=r'$P$ 为有限项索引集，$A_k,d_{k,i},c_k$ 为各项支持、次数、系数；$K_A=\sum_{k\in P:A_k=A}c_km_{A_k}(z)$。$z_i=x_i-r_i$ 为增量，$z_i^S=z_i$（i∈S）、0（其余）；$m_A(z)=\prod_{i\in A}z_i^{d_i}$。';de=r'Let P index finitely many terms, with support A_k, degrees d_{k,i} and coefficients c_k. Put $K_A=\sum_{k\in P:A_k=A}c_km_{A_k}(z)$. The increment is $z_i=x_i-r_i$, with $z_i^S=z_i$ in S and zero elsewhere. Define $m_A(z)=\prod_{i\in A}z_i^{d_i}$.'
  sz=r'实际Lean证明单项式遮罩律、任意有限项索引多项式的遮罩和、按支持分组重构及真实Möbius交互等于支持贡献；同支持不同次数可同时存在。另验证非零参考贡献的二值归一化。无限Taylor收敛与任意DNN不是本共享命题。'
  se=r'Lean proves monomial masking, masked sums for arbitrary finite term indices, reconstruction grouped by support, and equality of actual Möbius dividends to support contributions. Equal supports with different degrees are allowed. Nonzero reference normalization is also verified. Infinite Taylor convergence and arbitrary DNNs are outside this shared claim.'
 elif i=='dyn-shared-independent-residual':
  az=[r'概率测度、可测独立的有限随机量族；每个因子具有有限二阶矩。残差子结论另取中心化噪声和指定方差。'];ae=[r'A probability measure and a finite measurable independent family with finite second moments. The residual subresult additionally uses centered noises with specified variances.']
  dz=r'$X_i:\Omega\to\mathbb R$、$\epsilon_i:\Omega\to\mathbb R$；$E$是真实概率积分，$\operatorname{Var}X=E(X-EX)^2$。$r,w_i$ 为固定实数，$q_i$为噪声方差；Gaussian子结论通过map-law规定分布。';de=r'$X_i,\epsilon_i:\Omega\to\mathbb R$; E denotes an actual probability integral and variance is $E(X-EX)^2$. Residual r and weights w_i are fixed reals, while q_i are noise variances; the Gaussian subresult specifies laws through map-laws.'
  sz='实际积分产品矩、乘积L2、中心化残差期望与Gaussian矩前提的推导全部编译；本篇具体适配与其他论文的缩放分别提供。';se='Actual product integrals, product L2, centered residual expectations and Gaussian moment discharge all compile; source-specific scaling is supplied separately.'
 else:
  az=[r'有限完整幂集设计J；非负对角惩罚d，y为任意有限实标签向量。'];ae=[r'The complete finite powerset design J, a nonnegative diagonal penalty d, and any finite real label vector y.']
  dz,de=reg_z,reg_e
  sz='zeta单射、Gram正定、非负罚项后可逆、完成平方的唯一全局最小均已真实编译；原均匀期望loss由paper adapter绑定。';se='Zeta injectivity, Gram positivity, invertibility after a nonnegative penalty and the completed-square unique global minimum all compile; the paper adapter binds the original uniform expected loss.'
 ns=list(dict.fromkeys(n for block in decls for n in block));lr='theorem_proof'
 le=dict(status='partial_scope_verified' if lr=='partial_component' else 'verified',evidence_role=lr,compiled=True,declarations=ns,scope=se,report_path=str((P/'verification/report.json').relative_to(R)),build_id=report['build_id'],source_fingerprint=report['source_fingerprint'],axiom_audit='passed',axioms=sorted({a for n in ns for a in cat[n]['axioms']}),statement_md='\n\n'.join(cat[n]['signature'] for n in ns),step_map=[dict(step_id=s['id'],**rr) for s in steps for rr in s['lean_refs']],source_semantics_automatically_verified=False)
 return dict(id=i,title=ztitle,statement_tex=tex,assumptions=az,definitions=[dict(id=i+'-objects',body_md=dz)],overview=zp[0],proof_scope=sz,proof_steps=steps,rewrite_status='complete',rewrite_role='proof',statement_assessment='no_statement_error_recorded',lean=le,translations=dict(en=dict(title=etitle,overview=ep[0],assumptions=ae,definitions=[dict(id=i+'-objects',body_md=de)],proof_scope=se,proof_steps=es)))
shared_proofs=[
 shared('dyn-shared-polynomial-support','共享证明：有限多项式支持与二值掩码','Shared proof: finite-polynomial support and binary masks',r'm_A(z^S)=\mathbf1_{A\subseteq S}m_A(z),\quad z_i=x_i-r_i,\ z_i^S=z_i\mathbf1_{i\in S}',
 r'定义单项式 $m_A(z)=\prod_{i\in A}z_i^{d_i}$，其中每个 $d_i>0$；掩码增量坐标为 $z_i\mathbf1_{i\in S}$。若 $A\subseteq S$，每个因子不变；若不是，取 $i\in A\setminus S$，正次零因子使全积零。这给精确支持律。\n\n对有限个单项式逐项应用支持律，将同支持的贡献累加为 $K_A$。全部掩码输出为 $\sum_{A\subseteq S}K_A$，有限 Möbius 唯一性给 $K_A=I_g(A)$，包括空支持常数。若 $u=K_A(x)\ne0$，则 $K_A(x_S)/u=\mathbf1_{A\subseteq S}$。不声称无限 Taylor 在任意网络收敛。',
 r'Define $m_A(z)=\prod_{i\in A}z_i^{d_i}$ with every $d_i>0$ and masked increment coordinates $z_i\mathbf1_{i\in S}$. If $A\subseteq S$, every factor is retained. Otherwise choose $i\in A\setminus S$; its positive-degree zero factor annihilates the product. This proves the exact support identity.\n\nApply this identity to every term in a finite polynomial and group equal supports into $K_A$. All mask outputs equal $\sum_{A\subseteq S}K_A$, so finite Möbius uniqueness identifies $K_A=I_g(A)$, including the constant empty support. If $u=K_A(x)\ne0$, normalization gives $K_A(x_S)/u=\mathbf1_{A\subseteq S}$. No convergence of an infinite Taylor series for an arbitrary network is claimed.',
 [['Harsanyi.TaylorMoments.monomial_mask'],['Harsanyi.PolynomialSupport.mask_terms','Harsanyi.PolynomialSupport.support_reconstruct','Harsanyi.PolynomialSupport.interaction_eq_supportCoefficient','Harsanyi.TaylorMoments.normalized_trigger']]),
 shared('dyn-shared-independent-residual','共享证明：独立随机量的乘积矩与平方残差','Shared proof: independent-product moments and squared residuals',r'E(r+\sum_iw_i\epsilon_i)^2=r^2+\sum_iw_i^2q_i',
 r'在概率测度下，独立可测随机量 $X_i$ 各有有限二阶矩，独立乘积可积且有有限二阶矩。对 $X_i$ 及 $X_i^2$ 分别使用乘积积分分解，得 $E\prod_iX_i=\prod_iEX_i$，$E(\prod_iX_i)^2=\prod_iEX_i^2$。用 $EX_i^2=(EX_i)^2+\operatorname{Var}X_i$，相减得乘积方差 $\prod_i[(EX_i)^2+\operatorname{Var}X_i]-\prod_i(EX_i)^2$。\n\n若 $\epsilon_i$ 独立、中心化、方差为$q_i$，有限加权和 $Z=\sum_iw_i\epsilon_i$ 均值零、方差 $\sum_iw_i^2q_i$，故 $E(r+Z)^2=r^2+\sum_iw_i^2q_i$。这是真实积分，不是形式矩占位。\n\nGaussian法则进一步提供所有矩前提：从映射分布 $\mu\circ\epsilon_i^{-1}=\mathcal N(0,q_i)$ 推出 L2、均值0和方差$q_i$；平移因子 $1+\epsilon_i$ 独立、均值1、方差$q$，于是积均值1、方差$(1+q)^s-1$。本篇用于Lemma1的独立子模型和Theorem3逐行噪声残差；BNN/Difficulty将另显式适配坐标缩放与参考系数。',
 r'Under a probability measure, measurable independent $X_i$ with finite second moments have an integrable product with finite second moment. Factor the integrals for $X_i$ and $X_i^2$: $E\prod_iX_i=\prod_iEX_i$ and $E(\prod_iX_i)^2=\prod_iEX_i^2$. Substitute $EX_i^2=(EX_i)^2+\operatorname{Var}X_i$ and subtract the mean square to obtain the product-variance formula $\prod_i[(EX_i)^2+\operatorname{Var}X_i]-\prod_i(EX_i)^2$.\n\nFor independent centered $\epsilon_i$ with variances $q_i$, the finite weighted sum $Z=\sum_iw_i\epsilon_i$ has mean zero and variance $\sum_iw_i^2q_i$. Therefore $E(r+Z)^2=r^2+\sum_iw_i^2q_i$. These are actual integrals, rather than formal moment placeholders.\n\nGaussian map-laws discharge the moment premises: $\mu\circ\epsilon_i^{-1}=\mathcal N(0,q_i)$ implies L2, mean zero and variance $q_i$. Independent shifted factors $1+\epsilon_i$ have mean one and variance $q$, hence their product has mean one and variance $(1+q)^s-1$. This paper applies the proof to the independent submodel of Lemma 1 and to rowwise residuals in Theorem 3. BNN and Difficulty explicitly adapt coordinate scaling and reference coefficients separately.',
 [['Harsanyi.TaylorMoments.product_memLp','Harsanyi.TaylorMoments.product_mean','Harsanyi.TaylorMoments.product_variance'],['Harsanyi.GaussianRegression.independent_residual'],['Harsanyi.GaussianRegression.gaussian_memLp','Harsanyi.GaussianRegression.gaussian_mean','Harsanyi.TaylorMoments.gaussian_affine_product','Harsanyi.GaussianRegression.gaussian_residual']]),
 shared('dyn-shared-positive-regression','共享证明：Möbius 可逆设计与全局回归最优','Shared proof: invertible Möbius design and global regression optimum',r'A=J^\top J+\operatorname{diag}d,\quad d\ge0,\quad u=A^{-1}J^\top y',
 D['dyn-regression'][4],D['dyn-regression'][5],
 maps['dyn-regression'])]
# Explicit stable issue categories; source kind and mathematical assessments stay unchanged.
issue_categories = {
 'dyn-issue-taylor': ('statement_counterexample', 'counterexample_verified'),
 'dyn-issue-marginal-independence': ('statement_partial_counterexample', 'compound_clause_counterexample_verified'),
 'dyn-issue-proposition1': ('statement_partial_counterexample', 'compound_clause_counterexample_verified'),
 'dyn-issue-zero-trigger': ('definition_or_algorithm_boundary', 'scope_under_review'),
 'dyn-issue-eq3-empty': ('statement_alignment_or_scope', 'scope_under_review'),
 'dyn-issue-and-scope': ('statement_alignment_or_scope', 'scope_under_review'),
 'dyn-issue-complement-half': ('statement_alignment_or_scope', 'scope_under_review'),
 'dyn-issue-sparsity-transfer': ('statement_alignment_or_scope', 'scope_under_review'),
 'dyn-issue-trigger-variance': ('statement_alignment_or_scope', 'scope_under_review'),
 'dyn-issue-split-sign': ('definition_or_algorithm_boundary', 'counterexample_verified'),
}
for item in issues:
 category, assessment = issue_categories.get(item['id'], ('proof_step_error', 'no_statement_error_recorded'))
 item['issue_type'] = category
 item['original_statement_status'] = assessment
 item['related_result_ids'] = [r['id'] for r in results if item['id'] in r.get('related_issue_ids', [])]
 assert item['related_result_ids'], item['id']
content=dict(schema_version=1,paper_id=pid,inventory_path=str((P/'inventory.json').relative_to(R)),results=results,shared_proofs=shared_proofs,issues=issues,symbols=symbols,counts=dict(results=len(results)),source_transcription_policy='Official published source only. Complete per-result mathematical TeX transcriptions retain source errors; connecting source prose is project Chinese translation. Whole-page pdftotext files are source evidence only. No missing proof is filled by pretending project rewriting was author text.',authorization=dict(proof_only_repairs=True,proposition_modification=False))
def rendering_numbering(x):
 if isinstance(x,str):return re.sub(r'\\tag\{([^}]+)\}',r'\\quad\\text{(\1)}',x)
 if isinstance(x,list):return [rendering_numbering(y) for y in x]
 if isinstance(x,dict):return {k:rendering_numbering(v) for k,v in x.items()}
 return x
content=rendering_numbering(content);symbols=content['symbols'];issues=content['issues']
for f,x in [('content.json',content),('symbols.json',dict(paper_id=pid,symbols=symbols)),('issues.json',dict(paper_id=pid,issues=issues))]:
 (P/f).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
md=['# F07 正式论文逐页清单','',f'正式PDF：36页，SHA256 `{inv["sources"][0]["sha256"]}`。','', '初始抽取将 Appendix C/D 误标为 Shapley；逐页核对后核销，C 为稀疏提取、D 为唯一性。A 七性质、B 三条件各自拆为可检索入口。','', '| ID | 原标签 | 原陈述页 | 原证明页 |','|---|---|---|---|']
for x in inv['entries']:md.append('|'+x['id']+'|'+x['original_label']+'|'+','.join(map(str,x['statement_location']['pdf_pages']))+'|'+(','.join(map(str,x['proof_location']['pdf_pages'])) or '无本地独立证明')+'|')
md+=['','所有物理页在 inventory.json.page_audit 中保留，包括无证明、引用、图表页。Proposition 1 正噪声一般单调子句未决；零噪声只否定其无条件严格子句。']
(P/'inventory.md').write_text('\n'.join(md)+'\n')
print(pid,len(results),'results',len(shared_proofs),'new shared proofs',len(issues),'issues',len(symbols),'symbols')
