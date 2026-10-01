"""F10 paper package: complete source layers, bilingual mathematics, actual type bindings."""
from pathlib import Path
import json,re,sys,copy
sys.path.insert(0,str(Path(__file__).parent));from difficulty_rewrites import R as DATA, FORMULAS
ROOT=Path.cwd();P=ROOT/'corpus/public/reader/neurips2023-difficulty';pid=P.name
inv=json.loads((P/'inventory.json').read_text());sid=inv['sources'][0]['source_id'];vid=inv['sources'][0]['version_id']
main=json.loads((P/'source-transcripts-main-extra.json').read_text());extra=json.loads((P/'source-transcripts-extra.json').read_text());discussion=json.loads((P/'source-transcripts-discussion-extra.json').read_text())
report=json.loads((P/'verification/report.json').read_text());assert report['status']=='passed';CAT={x['name']:x for x in report['declarations']};rp=str((P/'verification/report.json').relative_to(ROOT))
def sr(pages,section=''):return dict(source_id=sid,version_id=vid,pdf_pages=sorted(set(pages)),section=section)
def ref(n):
 d=CAT[n];return dict(declaration=n,source_path=d['source_path'],line=d['line'],scope='exact_declared_type')
MAP={
'diff-universal':[['Harsanyi.reconstruction'],['Harsanyi.reconstruction']],
'diff-salient-reconstruction':[['Harsanyi.reconstruction'],[]],
'diff-taylor':[[],['Harsanyi.PolynomialSupport.mask_terms','Harsanyi.PolynomialSupport.support_reconstruct','Harsanyi.PolynomialSupport.interaction_eq_supportCoefficient']],
'diff-moments':[['PaperDifficulty.sourceTrigger','PaperDifficulty.lowest_trigger_mean_counterexample'],['PaperDifficulty.lowest_trigger_variance_counterexample']],
'diff-lowest-interaction':[['PaperDifficulty.maskedLowest','PaperDifficulty.maskedLowest_eq','PaperDifficulty.lowest_actual_dividend','Harsanyi.ConceptGaussian.lowest_polynomial_identity'],['PaperDifficulty.appendix_lowest_actual_moments','PaperDifficulty.empty_interaction_moments']],
'diff-general-moments':[['Harsanyi.ConceptGaussian.signed_scaled_law','Harsanyi.ConceptGaussian.folded_power_memLp','Harsanyi.ConceptGaussian.folded_product_moments'],['PaperDifficulty.lowest_trigger_mean_counterexample','PaperDifficulty.lowest_trigger_variance_counterexample']],
'diff-product':[['Harsanyi.TaylorMoments.product_memLp','Harsanyi.TaylorMoments.product_mean','Harsanyi.TaylorMoments.product_variance'],['PaperDifficulty.product_variance_counterexample']],
'diff-binary':[['Harsanyi.ConceptMasks.maskedGame','Harsanyi.ConceptMasks.masked_dividend'],['Harsanyi.ConceptMasks.binary_trigger'],[]],
'diff-linear-representation':[['Harsanyi.reconstruction'],['Harsanyi.ConceptMasks.linear_representation']],
'diff-regression':[['Harsanyi.ConceptGaussian.pairwise_feature_expected_loss','Harsanyi.ConceptGaussian.gaussian_feature_moments','PaperDifficulty.half_loss_strict_iff'],['Harsanyi.ConceptGaussian.featureMatrix_posDef','Harsanyi.ConceptGaussian.featureOpt_normal','Harsanyi.ConceptGaussian.pairwise_feature_expected_unique_min','PaperDifficulty.feature_opt_cramer'],['PaperDifficulty.feature_model','PaperDifficulty.featureOpt_values','PaperDifficulty.regression_step_three_counterexample']],
'diff-multiorder':[['PaperDifficulty.pairDelta_eq_dividend_sum','PaperDifficulty.multiorder_context_identity'],['Harsanyi.DifficultyCounting.superset_context_count','Harsanyi.DifficultyCounting.superset_context_count_all','Harsanyi.DifficultyCounting.context_double_sum','Harsanyi.DifficultyCounting.context_grouped_sum','Harsanyi.DifficultyCounting.context_grouped_average','PaperDifficulty.multiorder_grouped_identity'],['PaperDifficulty.maskedPolynomial_eq_unanimity','PaperDifficulty.multiorder_index_counterexample','PaperDifficulty.multiorder_coefficient_counterexample']],
'diff-kappa-conversion':[['Harsanyi.DifficultyKappa.singletonGame','Harsanyi.DifficultyKappa.singleton_dividend','Harsanyi.DifficultyKappa.actual_references'],['Harsanyi.DifficultyKappa.perturbation_law','Harsanyi.DifficultyKappa.perturbation_moments','Harsanyi.DifficultyKappa.actual_variation_bounds'],['Harsanyi.DifficultyKappa.chosenScale_pos','Harsanyi.DifficultyKappa.chosenScale_small','Harsanyi.DifficultyKappa.literal_coefficient_kappa_eq','Harsanyi.DifficultyKappa.literal_gaussian_relu_kappa_counterexample']],
'diff-efficiency':[['Harsanyi.reconstruction']], 'diff-linearity':[['Harsanyi.interaction_add']], 'diff-dummy':[['PaperDifficulty.source_dummy','Harsanyi.interaction_additive_dummy_nonempty']], 'diff-symmetry':[['Harsanyi.interaction_symmetry']], 'diff-anonymity':[['Harsanyi.interaction_relabel']], 'diff-recursion':[['Harsanyi.interaction_context_difference']], 'diff-distribution':[['Harsanyi.interaction_unanimity']],
}
SHARED={'diff-universal':['proof-finite-mobius-reconstruction-v2'],'diff-efficiency':['proof-finite-mobius-reconstruction-v2'],'diff-taylor':['dyn-shared-polynomial-support'],'diff-moments':['bnn-shared-gaussian-concepts'],'diff-general-moments':['bnn-shared-gaussian-concepts'],'diff-product':['dyn-shared-independent-residual','bnn-shared-gaussian-concepts'],'diff-binary':['bnn-shared-mask-support'],'diff-linear-representation':['proof-finite-mobius-reconstruction-v2','bnn-shared-mask-support'],'diff-regression':['bnn-shared-feature-regression'],'diff-multiorder':['shared-harsanyi-marginal-decomposition'],'diff-kappa-conversion':['diff-shared-relu-noise-integrals']}
SHARED['diff-lowest-interaction']=['bnn-shared-gaussian-concepts','dyn-shared-polynomial-support']
SHARED['diff-regression'] += ['diff-shared-regression-cramer']
SHARED['diff-multiorder'] += ['diff-shared-finite-context-counting']
for k in ['linearity','symmetry','anonymity','recursive','interaction-distribution','dummy-nonempty']:
 SHARED[{'recursive':'diff-recursion','interaction-distribution':'diff-distribution','dummy-nonempty':'diff-dummy'}.get(k,'diff-'+k)]=['shared-harsanyi-'+k]
# Original-source strings preserve author formulas; notes/rewrites never enter these fields.
ORIGINAL={
'diff-interaction':r'''Specifically, given a pre-trained DNN $v$ and an input sample $\mathbf x=[x_1,\ldots,x_n]$ with $n$ variables indexed by $N=\{1,\ldots,n\}$, $v(\mathbf x)\in\mathbb R$ denotes a scalar output of the DNN. Each interaction in [45,27,47] is defined as Harsanyi dividend (or Harsanyi interaction) [18] in game theory, which represents a collaboration (AND relationship) between input variables in a specific set $S$ ($S\subseteq N$). The interaction effect $I(S\mid\mathbf x)$ on the input sample $\mathbf x$ is computed as follows.
$$I(S\mid\mathbf x)=\sum_{T\subseteq S}(-1)^{|S|-|T|}\cdot v(\mathbf x_T).\qquad\text{(1)}$$
where $\mathbf x_T$ denotes the masked input sample, when we mask input variables in $N\setminus T$ and keep variables in $T$ unchanged. Please see more properties of the Harsanyi dividend in the supplementary material.

Footnote 3. Here, $v(\mathbf x)\in\mathbb R$ can be implemented as either a scalar output of the DNN or a dimension of an output vector (e.g., the confidence score of classifying the sample $\mathbf x$ to the ground-truth category $v(\mathbf x)=\log\frac{p(y=y_{truth}\mid\mathbf x)}{1-p(y=y_{truth}\mid\mathbf x)}$).''',
'diff-sparsity':r'''Ren et al. [45], Li and Zhang [27] have empirically observed and Ren et al. [47] have mathematically proven the counter-intuitive emergence of concepts in DNNs, i.e., it is proven that under a set of common conditions, a DNN encodes just a small number of interactive concepts for inference.'''+main['diff-sparsity-background']['original_statement_md'],
'diff-salient-reconstruction':r'''Theoretically, there are $2^n$ potential subsets $S$ of input variables ($S\in2^N=\{S\mid S\subseteq N\}$). The proven concept-emergence phenomenon refers to that only a small number of subsets $S\in\Omega_{salient}\subseteq2^N$ make salient interaction effects $I(S\mid\mathbf x)$ on the network output, and can be considered as interactive concepts. Interaction effects of all other subsets are close to zero ($I(S\mid\mathbf x)\approx0$), which can be considered as ignorable noisy patterns. Therefore, the network output $v(\mathbf x)$ can be well approximated by interaction effects of a small number of interactive concepts, i.e.,
$$v(\mathbf x)=\sum_{S\subseteq N}I(S\mid\mathbf x)\approx\sum_{S\in\Omega_{salient}}I(S\mid\mathbf x).\qquad\text{(2)}$$'''+main['diff-universal']['original_statement_md'],
'diff-concept-order':main['diff-sparsity-background']['original_statement_md'].split('Complexity (order) of interactive concepts.')[1],
'diff-multiorder-definition':r'''F. Complexity of interactive concepts.
Many previous studies [11,67,59,45,43] used multi-order interactions to analyze DNNs. Specifically, Given a pre-trained DNN $v$ and a masked sample $\mathbf x_S$, the multi-order interaction $I^{(m)}(i,j)$ used in [59,11,67] is given as follows:
$$I^{(m)}(i,j)=\mathbb E_{S\subseteq N\setminus\{i,j\},|S|=m}[\Delta v(i,j,S)].\qquad\text{(1)}$$
where $\Delta v(i,j,S)=v(\mathbf x_{S\cup\{i,j\}})-v(\mathbf x_{S\cup\{i\}})-v(\mathbf x_{S\cup\{j\}})+v(\mathbf x_S)$. They consider that $I^{(m)}(i,j)$ reflects the collaboration with $m$ contextual variables ($m$ pixels). In this way, the order $m$ measures the number of variables in $S$. Therefore, a low-order interaction denotes a relatively simple collaboration between input variables with a small context $S$. In contrast, a high-order interaction represents a complex collaboration between input variables with a large context $S$.
In this paper, we consider that the number of variables in an interactive concept $S$ can measure the complexity of an interactive concept encoded by a DNN, namely the order of the interactive concept, $\operatorname{complexity}(S)=\operatorname{order}(S)=|S|$. Thus, low-order concepts usually represent simple AND relationships among a few input variables. In comparison, high-order concepts often refer to as relatively complex AND relationships among a large number of input variables.''',
'diff-experiments':r'''H. Experimental Settings.
Training details. We trained AlexNet [23], VGG-11 [55], ResNet-18/20 [19] on the CIFAR-10 dataset [22] and the Tiny ImageNet dataset [25], respectively. We also trained a five-layer MLP on the UCI census dataset (namely census dataset) and the UCI TV news dataset (namely TV news dataset) [6], respectively. Each layer of the MLP contained 100 neurons. We trained each neural networks for 200 epochs with the SGD optimizer.
Sampling details. Since, the computational cost of $I(S\mid\mathbf x)$ was intolerable in real implementation, we applied the sampling-based approximation method in [67] to calculate $I(S\mid\mathbf x)$. Due to the high dimension of image data (e.g. $224\times224$ for ImageNet), we uniformly split the input image into $8\times8$ patches. Furthermore, we random sampled 12 patches and considered these patches as input variables for each image. The remaining 52 patches are set to the baseline value.
Implementations details. Here, we introduce how to measure $\beta(S)$ and $\kappa(S)$ in Section 2.3. On the Tiny ImageNet dataset, we randomly sampled 100 training images. These training images were randomly sampled from different 10 classes. On the CIFAR-10 dataset, we randomly sampled 10 training images from each class. For tabular datasets, we randomly sampled 50 training samples from each class. For image datasets, we set $\tau=2$ when the input data is normalized by its standard deviation. For tabular datasets, we set $\tau=1$ when the input data is normalized by its standard deviation. In this way, we set the baseline $b_i=\max(x_i-\tau,\mu)$, if $x_i>\mu_i$, and we set the baseline $b_i=\min(x_i+\tau,\mu)$, if $x_i<\mu_i$. For Gaussian perturbation $\epsilon$, we set $\sigma=0.02$. Besides, for each training sample, we randomly sampled five Gaussian perturbation with five different seeds, respectively.
Adversarial attack. Here, we introduce how to measure $A^{(s)}$ in Section 3.1. For tabular datasets, we randomly sampled 50 training samples from each class from the training set. On the Tiny-ImageNet dataset, we randomly sampled 100 training images. These training images were randomly sampled from different 10 classes. On the CIFAR-10 dataset, we randomly sampled 10 training images from each class. We used the $\ell_\infty$ untargeted PGD attack by following [33], in which the constraint $\epsilon=16/255$, and the attack was conducted with 5 steps with the step size $\epsilon=3/255$.''',
}
# Keep compound source proof boundaries, then split only at actual author clause boundaries.
AUTHOR={}
for i in DATA:
 if i in discussion:AUTHOR[i]=discussion[i]
 elif i in main or i in extra:
  a=main.get(i,extra.get(i));b=extra.get(i)
  AUTHOR[i]=dict(a)
  if b:
   AUTHOR[i]['original_statement_md']=a['original_statement_md']+('\n\n'+b['original_statement_md'] if i in main else '')
   AUTHOR[i]['original_proof_md']=b['original_proof_md']
 if i in ORIGINAL:AUTHOR[i]=dict(original_statement_md=ORIGINAL[i],original_proof_md='')
AUTHOR['diff-training-metrics']=main['diff-training-metrics']
AUTHOR['diff-kappa-conversion']=dict(main['diff-training-metrics'])
AUTHOR['diff-kappa-conversion']['original_statement_md']='In addition, we use another metric'+main['diff-training-metrics']['original_statement_md'].split('In addition, we use another metric')[1].split('To this end, we use DNNs')[0]
AUTHOR['diff-kappa-conversion']['original_proof_md']=''
AUTHOR['diff-general-moments']=dict(extra['diff-moments'])
AUTHOR['diff-general-moments']['original_statement_md']=main['diff-moments']['original_statement_md'].split('Let us first consider')[0]+'Furthermore,'+main['diff-moments']['original_statement_md'].split('Furthermore,')[1]
marker='According to Theorem 2, given an arbitrary input sample'
AUTHOR['diff-moments']['original_statement_md']=main['diff-moments']['original_statement_md'].split('Furthermore,')[0]
AUTHOR['diff-general-moments']['original_proof_md']=marker+extra['diff-moments']['original_proof_md'].split(marker)[1]
AUTHOR['diff-moments']['original_proof_md']=extra['diff-moments']['original_proof_md'].split(marker)[0]
AUTHOR['diff-lowest-interaction']=dict(original_statement_md=extra['diff-moments']['original_statement_md'].split('Furthermore,')[0],original_proof_md=AUTHOR['diff-moments']['original_proof_md'])
AUTHOR['diff-binary']['original_proof_md']=main['diff-binary']['original_proof_md']+'\n\n'+extra['diff-binary']['original_proof_md']
AUTHOR['diff-interaction']['original_statement_md']=AUTHOR['diff-interaction']['original_statement_md'].replace('The interaction effect $I(S\\mid\\mathbf x)$ on the input sample',r'For example, as Figure 1(a) shows, the co-appearance of image patches forms a mouth interaction $S=\{x_1,x_2,x_3\}$. Only when these three patches are all present, the mouth interaction will be triggered, and make a certain interaction effect $I(S)$ on the network output. The absence (masking) of any patches of $x_1,x_2$, and $x_3$ will deactivate the mouth interaction and remove the interaction effect, i.e., $I(S)=0$. The interaction effect $I(S\mid\mathbf x)$ on the input sample')
AUTHOR['diff-order-variance-metrics']=main['diff-order-variance-metrics']
# Symbols: source definitions retain printed notation; canonical descriptions explain the local map.
ROWS=[
('game','sym-game',r'v(\mathbf x_T)',r'g(T)=v(\mathbf x_T)','固定掩码奖励','Fixed masked reward','同一样本与参考下的实值集合游戏','A real set game at one fixed sample/reference',[3,4,15]),
('baseline','sym-output-baseline',r'v(\mathbf x_\varnothing)',r'v(\mathbf x_\varnothing)','输出基线','Output baseline','标量，等于空掩码输出，不默认零','The scalar empty-mask output, with no zero convention',[3,4,15]),
('reference','sym-input-baseline',r'b_i',r'b_i=x_i-\tau\text{ if }x_i>\mu_i;\ b_i=x_i+\tau\text{ otherwise}','输入参考','Input reference','输入向量坐标，原b_i规范映射r_i','An input-vector coordinate; source b_i maps to canonical r_i',[4,5,17,20]),
('mask','sym-mask',r'\mathbf x_T',r'(\mathbf x_T)_i=x_i\text{ for }i\in T;\ b_i\text{ otherwise}','掩码输入','Masked input','输入向量，保留T坐标并替换其他坐标','An input vector retaining T coordinates and replacing the rest',[3,4,20]),
('dividend','sym-and-interaction',r'I(S\mid\mathbf x)',r'I(S\mid\mathbf x)=\sum_{T\subseteq S}(-1)^{|S|-|T|}v(\mathbf x_T)','普通 AND 交互','Ordinary AND dividend','支持索引实数，包括空交互','A support-indexed real including the empty dividend',[3,4,15,16]),
('order','sym-order',r'\operatorname{order}(S)',r'\operatorname{complexity}(S)=\operatorname{order}(S)=|S|','概念支持阶数','Concept support order','非负整数，支持基数而非上下文m','A natural support cardinality, distinct from context m',[4,5,16]),
('context','concept-multiorder-context-cardinality',r'm',r'I^{(m)}(i,j)=E_{S\subseteq N\setminus\{i,j\},|S|=m}\Delta v(i,j,S)','上下文基数','Context cardinality','0到n−2的整数，平均上下文大小','An integer from0 to n−2 giving the averaged context size',[16,20,21]),
('tau','concept-reference-distance',r'\tau',r'x_i-b_i\in\{-\tau,\tau\}','参考距离','Reference distance','严格正实数的有定义理论域；裁剪另有范围','A positive real on the defined theoretical domain; clipping is separate',[4,5,17,18,19]),
('noise','concept-coordinate-noise',r'\boldsymbol\epsilon',r'\boldsymbol\epsilon\sim\mathcal N(0,\sigma^2I)','输入 Gaussian 扰动','Input Gaussian perturbation','独立坐标Gaussian随机向量','A Gaussian random vector with independent coordinates',[5,18,19]),
('noise-variance','concept-coordinate-variance',r'\sigma^2',r'\epsilon_i\sim\mathcal N(0,\sigma^2)','输入噪声方差','Input-noise variance','非负实数，严格反例取正方差','A nonnegative real, positive in the strict counterexamples',[5,18,19]),
('degree','concept-taylor-multiindex',r'\boldsymbol\pi\in Q_S',r'Q_S=\{[\pi_1,\ldots,\pi_n]:\pi_i\in\mathbb N^+\ (i\in S),\ \pi_i=0\ (i\notin S)\}','Taylor 次数向量','Taylor multiindex','自然次数向量，正次数支持为S','A natural-degree vector with positive-degree support S',[4,17,19]),
('taylor-coefficient','concept-moving-taylor-coefficient',r'U_{S,\boldsymbol\pi}',r'U_{S,\boldsymbol\pi}=\frac{\tau^m}{\prod_{i=1}^n\pi_i!}\frac{\partial^m v(\mathbf x\prime_\varnothing)}{\partial x_1^{\pi_1}\cdots\partial x_n^{\pi_n}}\cdot\prod_{i\in S}[\operatorname{sign}(x_i\prime-b_i)]^{\pi_i}','含移动符号的系数','Coefficient with moving signs','实值次数项系数，随当前x′的符号可变','A real term coefficient that can vary with the current x′ signs',[4,17,18]),
('term','concept-absolute-expansion-trigger',r'J(S,\boldsymbol\pi\mid\mathbf x\prime)',r'J(S,\boldsymbol\pi\mid\mathbf x\prime)=\prod_{i\in S}(\operatorname{sign}(x_i\prime-b_i)(x_i\prime-b_i)/\tau)^{\pi_i}','绝对增量触发','Absolute-increment trigger','非负单项式随机函数，不能换有符号I','A nonnegative monomial random function, distinct from signed I',[4,5,17,18,19]),
('weight','concept-reference-dividend',r'U_S',r'U_S=I(S\mid\mathbf x)','固定参考交互系数','Fixed reference dividend coefficient','参考样本索引实数，跨噪声固定但跨数据可变','A reference-sample real, fixed across noise but variable across data',[5,6,7]),
('trigger','concept-normalized-trigger',r'C_S(\mathbf x\prime)',r'C_S(\mathbf x\prime)=\sum_{\boldsymbol\pi\in Q_S}U_{S,\boldsymbol\pi}J(S,\boldsymbol\pi\mid\mathbf x\prime)/U_S','连续归一化触发','Continuous normalized trigger','非零U_S域的实随机函数；只对参考掩码二值','A real random function on U_S≠0; binary only on reference masks',[6,7,20]),
('stability','concept-standard-deviation-stability',r'E^{(s)}/\sqrt{V^{(s)}}',r'E^{(s)}/\sqrt{V^{(s)}}','标准差相对稳定度','Relative stability using standard deviation','正V域的非负实数，区别F08的E/Var','A nonnegative real on V>0, distinct from F08’s E/Var',[5,6]),
('mean-aggregate','concept-order-absolute-mean-aggregate',r'E^{(s)}',r'E^{(s)}=E_xE_{|S|=s}|E_\epsilon I(S\mid\mathbf x+\boldsymbol\epsilon)|','同阶绝对均值平均','Order-averaged absolute mean','非负实数，先噪声均值后绝对值后数据平均','A nonnegative real: noise mean, absolute value, then data average',[5,6]),
('variance-aggregate','concept-order-variance-metric',r'V^{(s)}',r'V^{(s)}=E_xE_{|S|=s}\operatorname{Var}_\epsilon I(S\mid\mathbf x+\boldsymbol\epsilon)','同阶方差平均','Order-averaged variance','非负实数，噪声随机源','A nonnegative real with noise as the random source',[5,6]),
('feature-mean','concept-regression-feature-mean',r'\mu_i',r'\mu=E_{\mathbf f}[\mathbf f]','回归特征均值','Regression feature mean','G5特征均值向量，非数据均值','A G.5 feature-mean vector, distinct from data means',[21]),
('feature-variance','concept-regression-feature-variance',r'\sigma_i^2',r'\Sigma=\operatorname{diag}(\sigma_1^2,\ldots,\sigma_k^2)','回归方差记号','Regression variance notation','原σ²/Σ²有读法冲突；真实方差规范d_i','Source σ²/Σ² is ambiguous; true variance is canonical d_i',[21]),
('covariance','difficulty-source-covariance-square',r'\Sigma^2',r'\mathbf f\sim\mathcal N(\mu,\Sigma^2)','原平方协方差记号','Source squared-covariance notation','k维矩阵，保留Σ和Σ²区别','A k-dimensional matrix preserving the distinction between Σ and Σ²',[21]),
('gram','concept-feature-second-moment-matrix',r'K',r'K=E_{\mathbf f}[\mathbf f\mathbf f^\top]=\mu\mu^\top+\Sigma^2','特征二阶矩矩阵','Feature second-moment matrix','k×k实对称矩阵','A real symmetric k×k matrix',[21]),
('regression-weight','concept-linear-feature-weight',r'\mathbf w',r'y^*\approx\mathbf w^\top\mathbf f','可优化线性权重','Optimized linear weight','k维实向量，固定f的平方回归权重','A real k-vector in squared regression with fixed f',[21]),
('beta','difficulty-class-consistency-beta',r'\beta(S)',r'\beta(S)=E_c[|E_{x\in X_c}I(S\mid\mathbf x)|/\operatorname{Std}_{x\in X_c}I(S\mid\mathbf x)]','类别相对一致性','Class relative consistency','非零类内标准差域的非负实数','A nonnegative real on nonzero within-class standard deviations',[7]),
('kappa','difficulty-relative-absolute-instability',r'\kappa(S)',r'\kappa(S)=E_xE_\epsilon|I(S\mid\mathbf x+\boldsymbol\epsilon)-I(S\mid\mathbf x)|/E_x|I(S\mid\mathbf x)|','相对绝对扰动敏感度','Relative absolute perturbation sensitivity','正平均幅值域的非负实数，打印C转换另审','A nonnegative real on positive mean magnitude; the printed C conversion is separately audited',[7]),
('salient','concept-salient-support-family',r'\Omega_{salient}',r'\Omega_{salient}\subseteq2^N','显著支持族','Salient support family','有限powerset子族，无统一尾和界','A finite powerset subfamily without a uniform tail-sum bound',[3,4,6]),
('jaccard','difficulty-learning-vector-jaccard',r'\operatorname{sim}(I_t^{(s)},I_{final}^{(s)})',r'\operatorname{sim}=\|\min(\widetilde I_t^{(s)},\widetilde I_{final}^{(s)})\|_1/\|\max(\widetilde I_t^{(s)},\widetilde I_{final}^{(s)})\|_1','训练向量 Jaccard','Training-vector Jaccard','分母非零域上的[0,1]相似度','A similarity in[0,1] where the denominator is nonzero',[8]),
('attack','difficulty-adversarial-perturbation',r'\delta',r'\delta\text{ generated by }\ell_\infty\text{ attack [33]}','对抗攻击扰动','Adversarial attack perturbation','依赖输入和攻击的向量，非Gaussianε','An input/attack-dependent vector, distinct from Gaussian ε',[9]),
('alpha','difficulty-adversarial-sensitivity-alpha',r'\alpha(S),A^{(s)}',r'\alpha(S)=E_x|I(S\mid\mathbf x+\delta)-I(S\mid\mathbf x)|/E_x|I(S\mid\mathbf x)|,\quad A^{(s)}=E_{|S|=s}\alpha(S)','对抗敏感度及阶数平均','Adversarial sensitivity and order average','正平均幅值域的非负实数','A nonnegative real on a positive mean-magnitude domain',[9]),
('permutation','sym-variable-permutation',r'\pi',r'v^\pi(\pi S)=v(S)','变量重命名双射','Variable relabeling bijection','变量集合双射，区别Taylor粗体π次数','A variable-set bijection, distinct from the bold Taylor multiindex',[16]),
('unanimity','sym-unanimity-game',r'v_T',r'v_T(S)=c\text{ if }T\subseteq S;\ 0\text{ otherwise}','纯 AND 奖励','Pure AND reward','支持T与实幅值c确定的集合游戏','A set game determined by support T and real amplitude c',[16]),
]
ROWS += [
('product-factors','concept-independent-product-factors',r'X_1,\ldots,X_k',r'X_1,\ldots,X_k\text{ independent}', '独立乘积因子','Independent product factors','有限独立实随机变量，正确方差式需有限二阶矩','Finite independent real random variables; the correct variance formula needs finite second moments',[18]),
('total-degree','concept-taylor-total-degree',r'm=\sum_i\pi_i',r'm=\sum_{i=1}^n\pi_i','Taylor 局部总次数','Local Taylor total degree','G1局部m是次数之和；规范|π|1，区别F上下文m','G.1 local m sums degrees; canonical ||π||₁ differs from Section F context m',[17]),
('moving-sign','concept-moving-coordinate-sign',r'\operatorname{sign}(x_i\prime-b_i)',r'\operatorname{sign}(x_i\prime-b_i)','当前增量符号','Current-increment sign','{-1,0,1}值，随当前输入可变；参考非零时±1','Values in{-1,0,1}, varying with the current input; nonzero reference signs are±1',[4,17,18,19]),
('frequency','difficulty-sample-space-spectrum',r'\text{low/high frequencies}',r'\text{low/high frequencies in the loss landscape in [63]}','样本空间频谱解释','Sample-space spectrum interpretation','外引损失景观频率，未给定量域，不是中间特征二维DFT','Cited loss-landscape frequencies with no quantitative domain, distinct from intermediate-feature two-dimensional DFT',[10])]
SYMBOLS=[]
for k,canonical,orig,odef,zt,et,zd,ed,pages in ROWS:
 ident='diff-'+k;zb='规范 g(T)=v(x_T)、b=g(∅)、g0=g−b；输入原b_i映射r_i。此局部对象的域和来源按本行保留。';eb='Canonical g(T)=v(x_T), b=g(empty), g0=g−b; source input b_i maps to r_i. Preserve this object’s local domain and source scope.'
 ze='空支持仍有I_g(∅)=b；次数/上下文/比值各自按所列定义域。';ee='Empty support has I_g(empty)=b; degrees, contexts and ratios retain their own stated domains.'
 mapping=dict(paper_id=pid,source_id=sid,version_id=vid,original_tex=orig,original_definition=odef,pdf_pages=pages,canonical_concept=canonical,relationship='explicit_local_instance',note=zd,conflict_note=zb,translations=dict(en=dict(note=ed,conflict_note=eb)))
 SYMBOLS.append(dict(id=ident,canonical_id=canonical,canonical_tex='g' if k=='game' else 'b' if k=='baseline' else 'r_i' if k=='reference' else 'd_i' if k=='feature-variance' else orig,definition_tex=odef,name_zh=zt,description_md=zd,type_or_domain=zd,scope=zd,assumptions=[],empty_set_convention=ze,baseline_convention=zb,aliases=[orig],paper_mappings=[mapping],lean_names=[],version='1.0',translations=dict(en=dict(name_zh=et,name=et,description_md=ed,type_or_domain=ed,scope=ed,assumptions=[],empty_set_convention=ee,baseline_convention=eb))))
LOCAL={
'diff-taylor':['degree','taylor-coefficient','term','reference','tau','dividend'], 'diff-moments':['term','noise','noise-variance','tau','degree'], 'diff-general-moments':['term','noise','noise-variance','tau','degree'], 'diff-product':['product-factors','noise','noise-variance'], 'diff-order-variance-argument':['term','taylor-coefficient','order'], 'diff-regression':['feature-mean','feature-variance','covariance','gram','regression-weight','trigger'], 'diff-multiorder':['context','dividend','unanimity','order'], 'diff-multiorder-definition':['context','dividend','order'], 'diff-kappa-conversion':['kappa','weight','trigger','reference','baseline','noise'], 'diff-binary':['mask','trigger','weight','dividend'], 'diff-linear-representation':['trigger','weight','dividend','salient'], 'diff-trigger-definition':['trigger','weight','dividend'], 'diff-reference':['reference','tau','noise'], 'diff-order-variance-metrics':['mean-aggregate','variance-aggregate','stability','order'], 'diff-training-metrics':['beta','kappa','dividend'], 'diff-training-similarity':['jaccard','dividend','order'], 'diff-adversarial-metric':['alpha','attack','dividend'], 'diff-anonymity':['permutation','game','dividend'], 'diff-distribution':['unanimity','game','dividend'], 'diff-salient-reconstruction':['salient','game','baseline','dividend'], 'diff-concept-order':['order','degree','context'], 'diff-frequency-learning-inference':['order','attack','stability'], 'diff-adversarial-inference':['context','order','alpha','dividend']}
ISSUES=[]
def issue(i,kind,typ,status,related,pages,zt,et,tex,zp,ep,ze,ee,zi,ei):
 ISSUES.append(dict(id=i,paper_id=pid,title=zt,kind=kind,issue_type=typ,original_statement_status=status,related_result_ids=related,affected_result_ids=related,source_refs=[sr(pages)],original_statement_tex=tex,problem_md=zp,evidence_md=ze,impact_md=zi,review_status='agent_checked_pending_independent_review',translations=dict(en=dict(title=et,problem_md=ep,evidence_md=ee,impact_md=ei))))
issue('diff-issue-taylor','unrestricted_taylor_statement','statement_counterexample','counterexample_verified',['diff-taylor'],[4,17,18],
 '任意 DNN 的全局 Taylor 展开失败','Global Taylor expansion fails for arbitrary DNNs',r'I(S\mid x\prime)=\sum_\pi U_{S,\pi}J_\pi',
 '作者未要求解析性、全局收敛或所有掩码上的合法展开。','The author supplies no analyticity, global convergence or legitimate expansion at every mask.',
 r'一维ReLU v(t)=max(t−1/2,0)，r0,x1，全部Taylor系数零而单例交互1/2。人读网络反例完整；Lean只验证真实有限多项式支持子结果。',r'The one-dimensional ReLU v(t)=max(t−1/2,0), r0,x1 has zero Taylor coefficients but singleton dividend1/2. The human network counterexample is complete; Lean verifies only the finite-polynomial support component.',
 '不把有限多项式机器类型扩成任意DNN原量词。','The finite-polynomial machine type is not expanded to the original arbitrary-DNN quantifier.')
issue('diff-issue-lowest-absolute','folded_lowest_moments','statement_counterexample','counterexample_verified',['diff-moments'],[5,18,19],
 '最低阶 J 自身的均值和方差错式','Incorrect mean and variance of the lowest J itself',r'EJ=1,\quad VarJ=(1+q)^{|S|}-1',
 '原对象J含绝对增量；小Gaussian不会几乎处处保持符号。','The original J contains absolute increments; a small Gaussian does not preserve signs almost surely.',
 '单支持、τ1、ε~N(0,q),q>0时J=|1+ε|。实际Lean证明EJ>1及VarJ<q，完整原对象、真实法则和两个矩都已绑定。','For one support, τ1 and ε~N(0,q), q>0, J=|1+ε|. Lean proves EJ>1 and VarJ<q, binding the full source object, actual law and both moments.',
 '与F08及本篇G2显示的有符号最低I矩区分；这里只否定正文J精确子句，不由此否定附录I变体。','Distinguish this from F08 and this paper’s appendix signed-I display. This refutes the main J clauses without thereby refuting the appendix I variant.')
issue('diff-issue-main-appendix-lowest','lowest_object_and_coefficient_scope','statement_alignment_or_scope','scope_under_review',['diff-moments','diff-lowest-interaction','diff-taylor'],[4,5,18,19],
 '最低阶主文 J 与附录 I 的原陈述差异','Lowest-degree main J and appendix I statements differ',r'EJ=1\quad\text{versus}\quad EI=U_{S,\widehat\pi}',
 '正文Eq5写J自身矩；G2重述prose仍说J，显示式却为I并带U。Theorem2定义的U还含随x′变动的符号。','Main Eq. (5) states J moments; G.2 repeats J in its prose but displays I with U. Theorem2’s U also includes signs varying with x′.',
 '原两个版本均完整保留。真实最低单项式的固定参考U矩已用actual maskedLowest及Gaussian法则形式化；空支持的固定输出基线另证均值b、方差0。','Both source versions are retained completely. The actual lowest monomial’s fixed-reference U moments are formalized through maskedLowest and Gaussian laws; the empty-support fixed output baseline separately has mean b and variance0.',
 '不把主文folded反例扩大为附录signed I错误，也不将最低单项式类型扩大为任意DNN完整I。','Do not extend the main folded counterexample to the signed-I appendix clause or extend the lowest-monomial type to every complete DNN dividend.')
issue('diff-issue-general-absolute','odd_folded_power_transition','statement_partial_counterexample','compound_clause_counterexample_verified',['diff-general-moments'],[5,19],
 '一般次数的绝对幂不能全改有符号幂','General absolute powers cannot all become signed powers',r'EJ=E\prod(1+\epsilon_i/\tau)^{\pi_i}',
 '奇次幂在越过参考时与绝对幂不同，≪τ只为近似。','Odd powers differ from absolute powers on reference-crossing tails; ≪τ is approximate.',
 'π1=1复用实际最低J均值/方差反例。正确folded乘积矩有实际Gaussian L2和独立法则证明；偶数幂子域绝对值可消去。','Degree1 uses the actual lowest-J mean and variance counterexample. Correct folded-product moments have actual Gaussian L2 and independence proofs; absolute values cancel on the even-degree subdomain.',
 '不将错误奇次子句扩大为所有整数次数错误。','The odd-degree error is not extended to every integer degree.')
issue('diff-issue-product-variance-square','squared_variance_in_source','analysis_subclause_counterexample','compound_clause_counterexample_verified',['diff-product','diff-moments'],[18],
 'Proposition1 方差项被再次平方','Proposition1 squares the variance again',r'\prod_i((EX_i)^2+(VarX_i)^2)-\prod_i(EX_i)^2',
 '原声明方差平方，下一Eq12却使用正确方差一次。','The original statement squares variance, while the next Eq. (12) uses variance once.',
 '真实k1 GaussianX~N(0,2)：VarX=2，打印右式4；机器绑定实际积分及方差。原乘积均值仍有效。','For actual k1 Gaussian X~N(0,2), VarX=2 but printed RHS4. Lean binds the actual integral and variance. The product-mean clause remains valid.',
 '公共正确product_variance不替换原Proposition。','The correct public product_variance does not replace the original Proposition.')
issue('diff-issue-zero-reference','undefined_reference_quotient','definition_or_algorithm_boundary','scope_under_review',['diff-trigger-definition','diff-binary','diff-linear-representation','diff-kappa-conversion'],[5,6,7,20],
 '零参考交互的触发商无定义','Trigger quotients are undefined at zero reference dividends',r'C_S=I(S\mid x\prime)/U_S',
 '作者未排U_S=0，二值短证明直接约分。','The author does not exclude U_S=0 before cancellation in the binary proof.',
 '常数网络全部非空参考交互0；原商0/0，若当前交互变非零则不能固定零U表达。κ实际反例两个U非零，避开此域。','A constant network has zero nonempty reference dividends, producing0/0. A nonzero current dividend cannot be represented by a fixed zero U. Both U values in the actual kappa counterexample are nonzero.',
 '有效非零域的掩码/线性适配已证明，但不隐去源零域。','Mask and linear adapters are proved on the nonzero domain; the original zero boundary remains visible.')
issue('diff-issue-binary-inclusion','wrong_inclusion_in_proof','proof_step_error','scope_under_review',['diff-binary'],[20],
 'G3 不触发分支的包含方向错','Wrong inclusion direction in the G.3 inactive branch',r'S\subsetneq T\quad\text{then }j\in S\setminus T',
 r'严格包含S⊊T不允许找到S\T元素。',r'Strict inclusion S⊊T cannot supply an element of S\T.',
 '正确分支是S不包含于T；真实maskedGame支持律不依赖此错步。','The correct branch is S not contained in T; the actual maskedGame support theorem avoids this erroneous step.',
 '只修证明步骤，保留Theorem4原陈述及零U范围。','Repair the proof step while retaining Theorem4 and its zero-U scope.')
issue('diff-issue-reference-notation','input_reference_symbol_switch','statement_alignment_or_scope','scope_under_review',['diff-binary','diff-taylor'],[17,20],
 '输入 r_i 与 b_i 局部切换','Local switching between input r_i and b_i',r'r_i,\ b_i',
 'Eq21/24局部输入参考符号切换，需说明同一基线。','Eqs. (21)/(24) switch input-reference symbols locally and require an explicit same-baseline interpretation.',
 '原作者式原样保留；重写一致用r_i并与输出基线b区分。','The original expressions are retained; the rewrite consistently uses r_i and distinguishes output baseline b.',
 '不由记号笔误单独否定非零域的二值结论。','The notation slip alone does not refute binary behavior on its nonzero domain.')
issue('diff-issue-multiorder-final-index','wrong_final_support_index','analysis_subclause_counterexample','compound_clause_counterexample_verified',['diff-multiorder'],[21],
 '原 Eq25 内和错用 |L|=m','Eq. (25) uses the wrong inner support index |L|=m',r'\sum_{l=0}^m\cdots\sum_{|L|=m}I(Lij)',
 '按l分组内层应|L|=l，打印最终等式不是正确关系。','The grouped inner index must be |L|=l; the printed final equality is false.',
 '真实N3, v=z1z2, x1,r0,m1：实际上下文平均1，打印右式0；实际Lean maskedPolynomial反例。','Actual N3, v=z1z2,x1,r0,m1 gives context mean1 and printed RHS0, as verified by the maskedPolynomial counterexample.',
 '不得把修过下标的公式标成原等式已证。','A repaired-index formula is not reported as a proof of the original equality.')
issue('diff-issue-multiorder-coefficient','wrong_superset_count','analysis_subclause_counterexample','compound_clause_counterexample_verified',['diff-multiorder'],[21],
 '原 Eq25 包含上下文的计数错误','Eq. (25) miscounts contexts containing a support',r'\binom{n-2}{m-l}',
 '固定l个变量后应从剩余n−2−l变量选m−l。','After fixing l variables, choose m−l from the remaining n−2−l variables.',
 '实际N4,v=z1z2z3,m2平均1，修内层但保留原系数时右式2。第二机器反例独立验证。','For actual N4,v=z1z2z3,m2 the mean is1, but repairing only the inner index leaves RHS2. The second machine counterexample verifies this independently.',
 '公共一般上下文计数与l分组恒等式及论文n−2适配已机器完成，原最后错误式仍由两个反例分别否定。','The public general context-counting and l-grouping identities and the paper n−2 adapter are machine-verified, while the two counterexamples separately refute the original final formula.')
issue('diff-issue-regression-mean','omitted_feature_mean_factor','analysis_subclause_counterexample','compound_clause_counterexample_verified',['diff-regression','diff-learning-consistency-argument'],[21],
 'G5 Step3 省掉特征均值','G.5 Step3 drops the feature mean',r'|w_i^*|\propto1/\sigma_i^2',
 'Step2含μ_i，不能在跨特征比较无条件删除。','Step2 includes μ_i, which cannot be deleted unconditionally across features.',
 '真实独立Gaussian μ=(1,2),双方差1,y1，唯一最优(1/6,1/3)，比1/2而逆方差比1。Σ=Σ²=I使记号读法一致。','Actual independent Gaussians μ=(1,2), both variances1 and y1 have unique optimum(1/6,1/3), ratio1/2 versus inverse-variance ratio1. Σ=Σ²=I removes the notation ambiguity.',
 '保留有效期望损失、正规方程与唯一最优；Step2须按真实方差读法及非零分母限定，主反例专门反驳Step3。','Retain valid expected loss, normal equations and the unique optimum; Step2 is restricted to the true-variance interpretation and nonzero denominator, and the main counterexample specifically refutes Step3.')
issue('diff-issue-covariance-square','variance_covariance_square_ambiguity','statement_alignment_or_scope','scope_under_review',['diff-regression'],[21],
 'Σ 与 Σ² 的方差记号冲突','Variance notation conflicts between Σ and Σ²',r'f\sim N(\mu,\Sigma^2),\quad\Sigma=diag(\sigma_i^2)',
 '字面读法真实方差σ_i^4，后文比例使用σ_i²；故Step2也只能在将σ_i²解释真实方差d_i时与有效公式一致。','The literal reading gives true variance σ_i^4, whereas later ratios use σ_i². Thus Step2 agrees with the valid formula only when σ_i² is interpreted as the true variance d_i.',
 '原式保留；规范真实方差d_i。主反例取两方差1，在两个读法都否定丢μ。','Retain the original expressions and use canonical true variance d_i. The main counterexample sets both variances1, refuting omission of μ under both readings.',
 '不无说明将原Σ²替换成diag真实方差。','Do not silently replace original Σ² by a true-variance diagonal.')
issue('diff-issue-kappa-cancellation','sample_dependent_reference_cancellation','statement_counterexample','counterexample_verified',['diff-kappa-conversion','diff-training-metrics'],[7],
 '跨数据不能约去变化的 |U_x|','Variable |U_x| cannot cancel across data averages',r'\kappa_I=\kappa_C',
 '逐样本I=U_xC_x只给加权比值，U_x随参考x变化。','Samplewise I=U_xC_x gives a weighted ratio, since U_x varies with reference x.',
 '标准化数据±1,均值0,τ1,r0,单ReLU max(t+1/2,0),b1/2；完整Gaussian明确σ，实际单例I及literal C积分给κ_I>κ_C。全部前提实际编译。','Normalized data±1,mean0,τ1,r0,single ReLU max(t+1/2,0),b1/2 and the explicit full Gaussian sigma give κ_I>κ_C for the actual singleton I and literal C integrals. All premises compile.',
 '原等号被原模型反例否定，指标I定义本身仍保留。','The source equality is refuted in its model, while the I definition of the metric is retained.')
issue('diff-issue-superposition','missing_covariance_control','statement_alignment_or_scope','scope_under_review',['diff-order-variance-argument'],[5],
 'chaotic 系数未控制整体协方差','Chaotic coefficients do not control total covariance',r'VarI\text{ grows with support order}',
 '单项J方差增长与加权I增长有额外协方差、幅值与移动系数条件。','Component-J variance growth needs additional covariance, amplitude and moving-coefficient conditions to control weighted I.',
 '完整有限和方差有所有交叉协方差；源未给删除它们的定量前提。','The finite-sum variance includes every cross-covariance; no quantitative premise removes them here.',
 '保留roughly近似解释，不伪造精确普遍结论。','Retain the rough interpretation without inventing an exact universal result.')
issue('diff-issue-external-learning','unquantified_learning_bridge','statement_alignment_or_scope','scope_under_review',['diff-learning-consistency-argument','diff-fast-learning-inference','diff-adversarial-inference','diff-noise-learning-inference','diff-shallow-learning-inference','diff-frequency-learning-inference','diff-adversarial-learning-inference','diff-sparsity','diff-salient-reconstruction'],[3,4,6,7,8,9,10],
 '条件外引与学习机制解释的缺失桥梁','Missing bridges in cited conditions and learning interpretations',r'\text{stability/order implies learning speed}',
 '完整外引前提、学习率模型与不同频率对象的适配未在本篇给出。','Complete cited premises, a learning-rate model and adaptations between distinct frequency objects are absent here.',
 '每条人读证明明确其实际源前提和所缺桥梁；Xu段为样本空间/损失景观频率，不能套F06中间特征DFT。','Each rewrite identifies its actual source premise and missing bridge. The Xu paragraph concerns sample-space/loss-landscape frequencies, not F06’s intermediate-feature DFT.',
 '不将经验/未量化解释加强成通用Lean定理，也不宣称完整外引定理被否定。','Do not strengthen empirical or unquantified interpretations into generic Lean theorems or claim refutation of a cited theorem with full premises.')
issue('diff-issue-zero-metrics','undefined_ratio_domains','definition_or_algorithm_boundary','scope_under_review',['diff-reference','diff-order-variance-metrics','diff-training-metrics','diff-training-similarity','diff-adversarial-metric','diff-regression','diff-multiorder-definition'],[5,7,8,9,16,21],
 '标准差、幅值和上下文平均的零域','Zero domains of standard deviations, magnitudes and context averages',r'\operatorname{Std},\ E|I|,\ \binom{n-2}m',
 '源未统一指定零标准差、零平均幅值、零Jaccard并集及无上下文平均的赋值。','The source has no common value for zero standard deviation, mean magnitude, Jaccard union or an empty context average.',
 '常数交互给标准差0；全零概念给幅值0和Jaccard0/0；m>n−2无合法上下文。τ0亦使原J除法无定义。','Constant dividends have standard deviation0; all-zero concepts have magnitude0 and Jaccard0/0; m>n−2 gives no legal contexts. Tau0 also makes the original J quotient undefined.',
 '所有有效条件范围明确保留，不用Lean的总运算约定替作者补定义。','Preserve every valid conditional domain without substituting Lean’s total-operation conventions for author definitions.')
RELATED={e['id']:[] for e in inv['entries']}
for x in ISSUES:
 for i in x['related_result_ids']:RELATED[i].append(x['id'])
SCOPES={
'diff-taylor':('有限索引多项式按支持分组真实形式化；任意DNN原命题由人读ReLU反例否定，机器角色仅有效有限子结果。','Finite-index polynomial support grouping is formalized. The arbitrary-DNN statement is refuted by a human ReLU counterexample; machine evidence covers only the valid finite component.'),
'diff-moments':('真实原绝对J的单坐标Gaussian均值与方差反例已完整形式化；保留小噪声近似语境，不换成F08最低I。','Both actual one-coordinate Gaussian mean and variance counterexamples for source absolute J are formalized. Retain the small-noise approximation context without replacing J by F08’s lowest I.'),
'diff-general-moments':('真实独立folded产品矩与奇次π=1反例已编译；偶次合法子域的人读解释不扩大为原任意次数有符号式。','Actual independent folded-product moments and the odd degree1 counterexample compile. The human even-degree explanation is not expanded into the source signed formula for arbitrary degrees.'),
'diff-product':('有效独立L2乘积矩与原Var平方子句的真实Gaussian反例分别绑定；不将公共正确方差公式冒充原Proposition。','Valid independent L2 product moments and the actual Gaussian counterexample to the squared-variance clause are separately bound; the correct public formula does not replace the Proposition.'),
'diff-binary':('实际掩码游戏支持律与非零U归一化已证明；源零系数域与G3错包含步骤明确保留。','Actual mask support and nonzero-U normalization are proved, with the source zero-coefficient boundary and erroneous G.3 inclusion explicitly retained.'),
'diff-linear-representation':DATA['diff-linear-representation']['scope'],
'diff-lowest-interaction':DATA['diff-lowest-interaction']['scope'],
'diff-regression':('真实Gaussian/两两独立L2固定特征的期望损失与唯一全局最优已形式化；原Step3丢均值被真实Σ=I反例否定。','Actual expected loss and unique global optimum for Gaussian or pairwise independent fixed L2 features are formalized. Source Step3’s omitted mean is refuted by an actual Σ=I example.'),
'diff-multiorder':('真实逐上下文差分、一般包含上下文计数、l分组及n−2平均适配均形式化；原最后下标与choose系数分别有真实maskedPolynomial反例，正确辅助关系不替代原错误等式。','Actual per-context differences, general superset counts, l-grouping and n−2 averaging are formalized. Separate actual maskedPolynomial counterexamples refute the final index and choose coefficient; the correct auxiliary relation does not replace the false source equality.'),
'diff-kappa-conversion':('标准化±1数据、r0、单ReLU、b1/2与显式完整Gaussianσ的实际单例交互及literal C积分反例全部形式化，严格κ_I>κ_C。','The actual singleton dividend and literal C-integral counterexample are fully formalized for normalized±1 data, r0, one ReLU, b1/2 and the explicit full Gaussian sigma, yielding strict κ_I>κ_C.'),
}
LOCAL['diff-lowest-interaction']=['dividend','baseline','reference','weight','taylor-coefficient','term','noise','noise-variance','tau','moving-sign']
RESULTS=[]
for e in inv['entries']:
 i=e['id'];d=DATA[i];steps=[];esteps=[];names=[]
 for j,(zt,et,zb,eb) in enumerate(d['steps'],1):
  ns=MAP.get(i,[])[j-1] if j-1<len(MAP.get(i,[])) else []
  names+=ns;st=f'{i}-step-{j}'
  formula=FORMULAS.get(i,[])[j-1] if j-1<len(FORMULAS.get(i,[])) else ''
  steps.append(dict(id=st,title=zt,body_md=zb,formula_tex=formula,lean_refs=[ref(n) for n in ns]));esteps.append(dict(id=st,title=et,body_md=eb))
 names=list(dict.fromkeys(names));a=AUTHOR[i];role=d['role'];assessment=d['assessment']
 if i=='diff-taylor':role='counterexample'
 if not e['proof_target']:scope=('完整原定义、测量模型或实验范围说明，不计独立数学定理。','Complete source definition, measurement model or experimental-scope explanation; not an independent mathematical theorem.')
 elif i in SCOPES:scope=SCOPES[i]
 elif role=='statement_scope_explanation':scope=('该未量化原推理的前提、论证及缺失条件逐项完成范围审查；没有机器证明其普遍结论。','The premise, argument and missing conditions of this unquantified source inference are reviewed; no universal conclusion is claimed machine-proved.')
 else:scope=('原局部前提下的有限普通Harsanyi性质完整适配，包括原空集/基线范围。','Complete adaptation of the finite ordinary-Harsanyi property under its source local premises, including its empty-coalition/baseline scope.')
 lr='none' if not names else 'counterexample' if i in ['diff-moments','diff-kappa-conversion'] else 'partial_component' if role in ['partial_component','partial_proof_with_refuted_clause','counterexample','statement_scope_explanation'] else 'theorem_proof'
 status='not_a_proof_target' if not e['proof_target'] else 'complete_with_scope_issue' if assessment=='scope_under_review' else 'complete'
 lean=dict(status='verified' if lr in ['theorem_proof','counterexample'] else 'partial_scope_verified' if names else 'not_applicable',evidence_role=lr,declarations=names,compiled=bool(names),scope=scope[1],encoding_note='Types use actual probability integrals, Gaussian Measure.map laws and finite masked games. Helpers, repaired components and original-clause counterexamples are scoped separately.',statement_md='\n\n'.join(CAT[n]['signature'] for n in names) if names else 'No Lean declaration is claimed for this unquantified source inference or definition.',source_semantics_automatically_verified=False)
 if names:lean.update(report_path=rp,build_id=report['build_id'],source_fingerprint=report['source_fingerprint'],axiom_audit='passed',axioms=sorted({ax for n in names for ax in CAT[n]['axioms']}),step_map=[dict(step_id=st['id'],**r) for st in steps for r in st['lean_refs']])
 lean['translations']=dict(en=dict(scope=scope[1],encoding_note=lean['encoding_note'],statement_md=lean['statement_md']))
 syms=['diff-'+k for k in LOCAL.get(i,['game','baseline','dividend','order'])]
 if i=='diff-taylor':syms+=['diff-total-degree','diff-moving-sign']
 if i=='diff-frequency-learning-inference':syms+=['diff-frequency']
 notation=[dict(original=s['paper_mappings'][0]['original_tex'],canonical=s['canonical_tex'],note=s['description_md']) for s in SYMBOLS if s['id'] in syms]
 enotation=[dict(original=s['paper_mappings'][0]['original_tex'],canonical=s['canonical_tex'],note=s['translations']['en']['description_md']) for s in SYMBOLS if s['id'] in syms]
 pages=e['statement_location']['pdf_pages']+e['proof_location']['pdf_pages'];refs=[sr(pages,e['statement_location']['section'])]
 if i=='diff-taylor':refs=[sr([4],'3.2, Theorem2 and Eq.(4)'),sr([17,18],'G.1, local Eqs.(2)–(8)')]
 if i=='diff-moments':refs=[sr([5],'3.2, main Theorem3 lowest-J Eq.(5)'),sr([18,19],'G.2, related lowest-degree argument local Eqs.(9)–(13)')]
 if i=='diff-general-moments':refs=[sr([5],'3.2, main Theorem3 general-J Eq.(6)'),sr([19],'G.2, local Eqs.(14)–(18)')]
 if i=='diff-binary':refs=[sr([6],'3.2.1, Theorem4 Eq.(8) and short proof'),sr([20],'G.3, local Eqs.(19)–(24)')]
 for occurrence in e['appearances']:
  if occurrence['pdf_pages'] and any(p not in pages for p in occurrence['pdf_pages']):refs.append(sr(occurrence['pdf_pages'],occurrence['section']))
 if i in ['diff-sparsity','diff-universal']:refs.append(sr([10],'5, reiterated cited faithfulness'))
 r=dict(id=i,paper_id=pid,title=d['title'],kind=e['kind'],original_label=e['original_label'],inventory_ids=[i],source_refs=refs,statement_tex=d['statement_tex'],assumptions=[d['assumptions'][0]],definitions=[dict(name='本条局部定义',body_md=d['definitions'][0])],original_statement_md=a['original_statement_md'],original_proof_md=a['original_proof_md'],original_statement_source_type='formal_author_transcription',original_proof_source_type='formal_author_transcription' if a['original_proof_md'] else 'no_local_author_proof',source_transcription_status='complete_statement_and_author_proof' if a['original_proof_md'] else 'complete_statement_no_local_author_proof',overview=d['steps'][0][2],proof_steps=steps,shared_proof_ids=SHARED.get(i,[]),symbol_ids=syms,notation_map=notation,rewrite_status=status,rewrite_role=role,statement_assessment=assessment,proof_scope=scope[0],completion_scope=scope[0],alignment_status='agent_checked_statement_and_proof_boundaries',user_review_status='pending',lean=lean,related_issue_ids=RELATED[i],translations=dict(en=dict(title=d['title_en'],overview=d['steps'][0][3],assumptions=[d['assumptions'][1]],definitions=[dict(name='Local definitions for this entry',body_md=d['definitions'][1])],proof_steps=esteps,notation_map=enotation,proof_scope=scope[1],completion_scope=scope[1])))
 if i in ['diff-moments','diff-general-moments']:r['source_transcription_note']='Author G.2 is split at its actual lowest/general argument boundary; Proposition1 is a statement embedded in the lowest proof, separately indexed without an invented local proof.'
 if i=='diff-lowest-interaction':r['source_transcription_note']='G.2 repeats Theorem3 with J in prose but I in the display. Its lowest proof is the same source occurrence linked to diff-moments and is not counted twice as an author proof.'
 if i=='diff-binary':r['source_transcription_note']='The original proof retains both the short main-text PDF6 explanation after Eq.(8) and the full Appendix G.3 PDF20 derivation.'
 if i in ['diff-taylor','diff-moments','diff-general-moments','diff-product','diff-multiorder','diff-kappa-conversion','diff-regression']:
  r['statement_md']='下式保留作者待审主张，包含已反例否定的子句。后续步骤独立列出有效子结果、修正恒等式与原模型反例；这些辅助式不替代原命题。'
  r['translations']['en']['statement_md']='The following retains the source claim, including the refuted clauses. The steps separately present valid components, repaired identities and original-model counterexamples; these auxiliary formulas do not replace the source statement.'
 if i in ['diff-binary','diff-linear-representation','diff-lowest-interaction','diff-salient-reconstruction']:
  boundary={'diff-binary':('下式是原触发商有定义、固定参考交互非零域的有效适配；作者未排零U的原陈述与问题仍完整保留。','The display is a valid adaptation on the defined trigger-quotient domain with nonzero fixed reference dividend. The source statement and its unexcluded zero-U boundary remain intact.'),'diff-linear-representation':('下式是完整有限支持与非零固定参考系数域的有效重构辅助式；不由此证明源显著截断或任意Taylor展开。','The display is a valid full-finite-support reconstruction with nonzero fixed reference coefficients; it does not prove salient truncation or an unrestricted Taylor expansion.'),'diff-lowest-interaction':('下式原样保留G2的I显示变体；真正形式化的是固定参考最低单项式的精确矩与空支持基线分支。原prose/J、移动U及任意DNN高次截断歧义仍保留。','The display retains G.2’s source I variant. Actual formalization proves fixed-reference lowest-monomial moments and the empty-support baseline branch; the source J prose, moving U and arbitrary-DNN higher-term truncation scope remain.'),'diff-salient-reconstruction':('下式是从精确重构推出的有效余项辅助恒等式；作者的显著和近似主张仍按原文保留，未由本恒等式证明统一误差界。','The display is a valid residual identity following from exact reconstruction. The source salient-sum approximation remains intact; this identity does not prove a uniform error bound.')}[i]
  r['statement_md']=boundary[0];r['translations']['en']['statement_md']=boundary[1]
 RESULTS.append(r)
# One new reusable integral proof; the Taylor/moment/regression/mask proofs remain shared with F07/F08.
ks=DATA['diff-kappa-conversion'];kst=RESULTS[[r['id'] for r in RESULTS].index('diff-kappa-conversion')]
shared=dict(id='diff-shared-relu-noise-integrals',title='共享证明：单 ReLU 的完整 Gaussian 绝对变化界',statement_tex=r'A_{low}\le q/2,\quad A_{high}\ge m-q/6,\quad m=\sigma E|Z|,\ q=\sigma^2,\ Z\sim N(0,1)',assumptions=['Gaussian标准法则、σ≥0；严格反例另采用所列显式正σ。'],definitions=[dict(name='真实噪声积分',body_md=ks['definitions'][0])],overview=ks['steps'][1][2],proof_steps=copy.deepcopy(kst['proof_steps']),symbol_ids=kst['symbol_ids'],notation_map=kst['notation_map'],rewrite_status='complete',rewrite_role='proof',proof_scope='所有Gaussian矩、可积性、ReLU尾界及实际I/C连接均由真实声明消去；用于本篇跨样本κ反例。',lean=copy.deepcopy(kst['lean']),paper_mappings=[dict(paper_id=pid,result_id='diff-kappa-conversion',note='使用真实singleton掩码交互和两点标准化数据，不替换为离散噪声。',translations=dict(en=dict(note='Use an actual singleton masked dividend and normalized two-point data, without substituting discrete noise.')))],translations=dict(en=dict(title='Shared proof: full-Gaussian absolute-change bounds for one ReLU',assumptions=['The standard Gaussian law and σ≥0; the strict counterexample additionally uses the explicit positive sigma.'],definitions=[dict(name='Actual noise integrals',body_md=ks['definitions'][1])],overview=ks['steps'][1][3],proof_steps=copy.deepcopy(kst['translations']['en']['proof_steps']),notation_map=kst['translations']['en']['notation_map'],proof_scope='Actual declarations discharge Gaussian moments, integrability, ReLU-tail bounds and the I/C connection; applied to the across-data kappa counterexample.')))
bstep=ks['steps'][1]
shared['statement_tex']=r'A_{low}\le q/2,\quad A_{high}\ge m-q/6,\quad m=\sigma E|Z|,\ q=\sigma^2,\ Z\sim N(0,1),\ \sigma\ge0'
shared['definitions']=[dict(name='两个真实噪声绝对变化积分',body_md=r'ε=σZ，v(t)=max(t+1/2,0)，A_low=E|I(-1+ε)-I(-1)|，A_high=E|I(1+ε)-I(1)|；I(t)=v(t)-v(0)，输出基线v(0)=1/2。')]
shared['translations']['en']['definitions']=[dict(name='Two actual noise absolute-change integrals',body_md=r'ε=σZ, v(t)=max(t+1/2,0), A_low=E|I(-1+ε)-I(-1)| and A_high=E|I(1+ε)-I(1)|, where I(t)=v(t)-v(0), with output baseline v(0)=1/2.')]
shared['proof_steps']=copy.deepcopy([kst['proof_steps'][0],kst['proof_steps'][1]])
shared['translations']['en']['proof_steps']=copy.deepcopy([kst['translations']['en']['proof_steps'][0],kst['translations']['en']['proof_steps'][1]])
for j in range(2):
 shared['proof_steps'][j]['id']=shared['translations']['en']['proof_steps'][j]['id']=f'diff-shared-relu-noise-integrals-step-{j+1}'
sn=list(dict.fromkeys(n for j in [0,1] for n in MAP['diff-kappa-conversion'][j]))
shared['lean'].update(evidence_role='theorem_proof',status='verified',declarations=sn,statement_md='\n\n'.join(CAT[n]['signature'] for n in sn),step_map=[dict(step_id=t['id'],**r) for t in shared['proof_steps'] for r in t['lean_refs']],scope='Actual Gaussian/ReLU singleton model and generic nonnegative-scale absolute-change bounds; the strict kappa counterexample is a separate downstream application.',axioms=sorted({ax for n in sn for ax in CAT[n]['axioms']}))
shared['lean']['translations']['en'].update(scope=shared['lean']['scope'],statement_md=shared['lean']['statement_md'])
def public_shared(ident,result,zt,et,tex,assumptions,definitions,steps,scope):
 rr=next(r for r in RESULTS if r['id']==result);ps=[];es=[];ns=[]
 for j,(title,etitle,body,ebody,formula,names) in enumerate(steps,1):
  st=f'{ident}-step-{j}';ns+=names
  ps.append(dict(id=st,title=title,body_md=body,formula_tex=formula,lean_refs=[ref(n) for n in names]));es.append(dict(id=st,title=etitle,body_md=ebody))
 ns=list(dict.fromkeys(ns));sig='\n\n'.join(CAT[n]['signature'] for n in ns)
 le=dict(status='verified',evidence_role='theorem_proof',declarations=ns,compiled=True,scope=scope[1],encoding_note='Public extension theorem types are independently reusable; the paper adapter and original-clause counterexamples are separate.',statement_md=sig,report_path=rp,build_id=report['build_id'],source_fingerprint=report['source_fingerprint'],axiom_audit='passed',axioms=sorted({ax for n in ns for ax in CAT[n]['axioms']}),step_map=[dict(step_id=p['id'],**r) for p in ps for r in p['lean_refs']],source_semantics_automatically_verified=False,translations=dict(en=dict(scope=scope[1],encoding_note='Public extension theorem types are independently reusable; the paper adapter and original-clause counterexamples are separate.',statement_md=sig)))
 return dict(id=ident,title=zt,statement_tex=tex,assumptions=[assumptions[0]],definitions=[dict(name='共享局部对象',body_md=definitions[0])],overview=steps[0][2],proof_steps=ps,symbol_ids=rr['symbol_ids'],notation_map=rr['notation_map'],rewrite_status='complete',rewrite_role='proof',proof_scope=scope[0],lean=le,paper_mappings=[dict(paper_id=pid,result_id=result,note=scope[0],translations=dict(en=dict(note=scope[1])))],translations=dict(en=dict(title=et,assumptions=[assumptions[1]],definitions=[dict(name='Shared local objects',body_md=definitions[1])],overview=steps[0][3],proof_steps=es,notation_map=rr['translations']['en']['notation_map'],proof_scope=scope[1])))
counting=public_shared('diff-shared-finite-context-counting','diff-multiorder','共享证明：包含上下文的计数与平均分组','Shared proof: superset-context counts and grouped averages',r'\frac{\sum_{S\subseteq R,|S|=m}\sum_{L\subseteq S}a_L}{\binom{|R|}m}=\sum_{l=0}^m\frac{\binom{|R|-l}{m-l}}{\binom{|R|}m}\sum_{L\subseteq R,|L|=l}a_L',
 ('R有限，a_L实数，0≤m≤|R|，使uniform上下文集合非空。','R is finite, a_L is real and0≤m≤|R|, so the uniform context family is nonempty.'),
 (r'$\mathcal C_m=\{S\subseteq R:|S|=m\}$；每个支持 $L$ 的权重为 $a_L$。超范围 $|L|>m$ 的出现次数为零。',r'$\mathcal C_m=\{S\subseteq R:|S|=m\}$ and support L has weight a_L. Supports with |L|>m have multiplicity zero.'),[
 ('构造删除固定支持的双射','Construct the fixed-support removal bijection',r'对 $L\subseteq R$、$|L|\le m$，$S\mapsto S\setminus L$ 与 $W\mapsto L\cup W$ 互逆，前者目标为 $R\setminus L$ 的 $m-|L|$ 元子集。各自基数由不交并的加法公式计算。若 $|L|>m$，不存在包含L的合法S；单列此分支，避免自然数减法截断误计数。',r'For $L\subseteq R$ with $|L|\le m$, the maps $S\mapsto S\setminus L$ and $W\mapsto L\cup W$ are inverse, targeting subsets of $R\setminus L$ of cardinality $m-|L|$. Cardinalities follow from disjoint-union addition. If $|L|>m$ no context can contain L; this separate branch avoids miscounting from truncated natural subtraction.',r'\#\{S\in\mathcal C_m:L\subseteq S\}=\begin{cases}\binom{|R|-|L|}{m-|L|}&|L|\le m\\0&|L|>m\end{cases}',['Harsanyi.DifficultyCounting.superset_context_count','Harsanyi.DifficultyCounting.superset_context_count_all']),
 ('交换有限和并按支持大小分组','Exchange finite sums and group by support size',r'交换上下文S与支持L的有限和，每项a_L乘以上一步出现次数。再用有限基数纤维把支持按l=|L|分组；同组choose系数相同可提出。最后除以正的上下文数choose(|R|,m)，得到所列平均。Lean恒等式以总除法对全m定义；将它读成实际均匀平均仅在此m≤|R|域内。',r'Exchange the finite sums over contexts S and supports L, multiplying each a_L by its multiplicity. Partition supports into cardinality fibers l=|L| and factor out the common choose coefficient. Divide by the positive context count choose(|R|,m) to obtain the displayed average. Lean’s total-division identity exists for all m; it represents an actual uniform mean only on m≤|R|.',r'\sum_{S\in\mathcal C_m}\sum_{L\subseteq S}a_L=\sum_{l=0}^m\binom{|R|-l}{m-l}\sum_{L\subseteq R,|L|=l}a_L',['Harsanyi.DifficultyCounting.context_double_sum','Harsanyi.DifficultyCounting.context_grouped_sum','Harsanyi.DifficultyCounting.context_grouped_average'])],
 ('公共双计数/分组独立于论文；本篇a_L=I_g(Lij)与|R|=n−2的适配另由PaperDifficulty完成。','Public double counting and grouping are paper-independent; PaperDifficulty separately adapts a_L=I_g(Lij) and |R|=n−2.'))
regshared=public_shared('diff-shared-regression-cramer','diff-regression','共享证明：正方差特征最优的 Cramer 连接','Shared proof: Cramer connection for positive-variance feature optimization',r'\det K>0,\quad w_i^*=\frac{\det(K[i\leftarrow y\mu])}{\det K},\quad K=\mu\mu^\top+\operatorname{diag}d',
 ('有限固定特征索引、真实d_i>0、μ_i和y实数；本纯矩阵引理不额外要求联合独立。','A finite fixed-feature index, true d_i>0 and real μ_i,y. This matrix lemma adds no joint-independence assumption.'),
 (r'$K=\mu\mu^\top+\operatorname{diag}d$，$H=1+\sum\mu_i^2/d_i$，$w_i^*=y\mu_i/(d_iH)$；$K[i\leftarrow y\mu]$ 表示以 $y\mu$ 替换第i列。',r'K=μμᵀ+diag d, H=1+Σμ_i²/d_i and w_i*=yμ_i/(d_iH). K[i←yμ] replaces column i by yμ.'),[
 ('以正定性隔离唯一正规解','Use positive definiteness to isolate the normal solution',r'共享特征矩阵正定性给detK>0；闭式w*满足Kw*=yμ。Cramer向量满足K·cramer(K,yμ)=detK·yμ。K的单射性于是给detK·w*=cramer(K,yμ)，逐坐标除以非零detK得到显示式。',r'The shared positive definite feature matrix has detK>0 and the closed w* satisfies Kw*=yμ. Cramer’s vector satisfies K·cramer(K,yμ)=detK·yμ. Injectivity of K gives detK·w*=cramer(K,yμ); coordinatewise division by nonzero detK yields the display.',r'Kw^*=y\mu,\quad\det K>0,\quad w_i^*=\det(K[i\leftarrow y\mu])/\det K',['Harsanyi.ConceptGaussian.featureMatrix_posDef','Harsanyi.ConceptGaussian.featureOpt_normal','Harsanyi.DifficultyRegression.feature_opt_cramer']),
 ('连接正比例损失的相同最优','Connect the same optimum for positively scaled losses',r'原半损失是L/2；乘正数1/2保留任意两个权重的严格损失比较。因此公共期望损失的唯一最优也正是原Eq26的唯一最优，而不是将原归一化改写后略去说明。',r'The source half loss is L/2. Multiplication by positive1/2 preserves every strict loss comparison, so the unique public expected-loss optimum is also exactly the unique optimum of source Eq. (26); the normalization is not silently replaced.',r'\tfrac12a<\tfrac12b\quad\Longleftrightarrow\quad a<b',['Harsanyi.DifficultyRegression.half_loss_strict_iff'])],
 ('本共享证明只连接有效矩阵正规解与原Cramer表达/半损失；丢均值反例和σ²/σ⁴源范围在论文适配另列。','This shared proof only connects the valid normal solution to the source Cramer expression and half loss; omitted-mean counterexamples and source σ²/σ⁴ scope remain in the paper adapter.'))
CONTENT=dict(schema_version=1,paper_id=pid,inventory_path=str((P/'inventory.json').relative_to(ROOT)),results=RESULTS,shared_proofs=[shared,counting,regshared],issues=ISSUES,symbols=SYMBOLS,counts=dict(results=len(RESULTS),proof_targets=len(inv['proof_targets'])),source_transcription_policy='Official NeurIPS2023 published PDF only. Full author statements and proofs preserve printed formulas, errors, local equation scopes and approximate wording. Project notes and rewrites are separate. All22 physical pages are inventoried.',authorization=dict(proof_only_repairs=True,proposition_modification=False))
def numbers(x):
 if isinstance(x,str):return re.sub(r'\\tag\{([^}]+)\}',r'\\quad\\text{(\1)}',x)
 if isinstance(x,list):return [numbers(v) for v in x]
 if isinstance(x,dict):return {k:numbers(v) for k,v in x.items()}
 return x
CONTENT=numbers(CONTENT)
for f,x in [('content.json',CONTENT),('symbols.json',dict(paper_id=pid,symbols=CONTENT['symbols'])),('issues.json',dict(paper_id=pid,issues=CONTENT['issues']))]:
 temporary=P/(f+'.tmp')
 temporary.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
 temporary.replace(P/f)
metadata=json.loads((P/'paper-metadata.json').read_text())
metadata['results']=[r['id'] for r in RESULTS]
(P/'paper-metadata.json').write_text(json.dumps(metadata,ensure_ascii=False,indent=2)+'\n')

md=['# F10 正式论文逐页与目标清单','',f'22页正式PDF，SHA256 `{inv["sources"][0]["sha256"]}`。',f'{len(RESULTS)}入口、{len(inv["proof_targets"])}显式数学目标。','', '| ID | 原局部标签 | 陈述页 | 证明页 | 目标 |','|---|---|---|---|---|']
for e in inv['entries']:md.append('|'+e['id']+'|'+e['original_label']+'|'+str(e['statement_location']['pdf_pages'])+'|'+str(e['proof_location']['pdf_pages'])+'|'+str(e['proof_target'])+'|')
md+=['','Main Eq2/3与Appendix G1 Eq2/3有各自章节作用域；D递归/distribution未编号，不造Eq2/3别名。G2最低/一般证明按原转折切分，并独立记录正文J与附录I最低显示差异；原Prop1方差平方与下一式一次方差均保留。D七性质各有入口，dummy明确非空。3.2.3 Jaccard公式与4.1 α/A没有作者编号。','', '完整作者层由main/appendix/discussion三份独立source transcript及F/H实际原文补齐；逐页txt只作source evidence。真实Gaussian/有限掩码/单ReLU反例与条件证明分别登记，不将无量化学习解释冒充机器定理。']
(P/'inventory.md').write_text('\n'.join(md)+'\n')
print(pid,len(RESULTS),'results',len(inv['proof_targets']),'targets',len(ISSUES),'issues',len(SYMBOLS),'symbols')
