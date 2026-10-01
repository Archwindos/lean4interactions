import json,re
from pathlib import Path
BASE=Path('research/full-proof-integration-20260930/iclr2024-sparse')
inv=json.loads((BASE/'inventory.json').read_text())
sym=json.loads((BASE/'symbols.json').read_text())['symbols']
issues=json.loads((BASE/'issues.json').read_text())['issues']
pages={p['page']:p['text'] for p in json.loads(Path('research/paper-survey-20260930/recent/text/iclr2024-sparse.pages.json').read_text())}
raw=(BASE/'math/rewrites.zh.md').read_text()
parts=re.split(r'<!-- result:([^>]+) -->',raw)
rewrites={parts[i]:parts[i+1].strip() for i in range(1,len(parts),2)}

def marked_file(path, prefix):
    chunks=re.split(r'<!-- '+prefix+r':([^>]+) -->',(BASE/path).read_text())
    return {chunks[i]:chunks[i+1].strip() for i in range(1,len(chunks),2)}
author_statements=marked_file('math/author-statements.tex.md','statement')
author_proofs=marked_file('math/author-proofs.tex.md','proof')

proof_bounds={
 'reconstruction':(15,15,'Proof. According to the definition','B.2'),
 'lemma1':(15,16,'Proof. Let us denote','Then, we prove'),
 'derivative-cutoff':(16,16,'Proof. According to Lemma 1','B.3'),
 'lemma2':(17,17,'Proof. According to the definition','Lemma 3.'),
 'lemma3':(17,18,'Proof. We first represent','Next, we will prove'),
 'theorem2':(19,20,'Proof. First, according','B.4'),
 'theorem3':(20,21,'Proof. According to the definition','B.5'),
 'lemma4':(21,21,'Proof. By the definition','Then, let us prove'),
 'theorem4':(22,23,'Proof. By the definition','B.6'),
 'theorem5':(23,25,'Proof. The Shapley interaction','B.7'),
 'theorem6':(25,27,'Proof. By the definition','C       E XPERIMENTAL')}
def original_proof(key,e):
    if key in proof_bounds:
        a,b,start,end=proof_bounds[key]
        block='\n\n'.join(pages[p] for p in range(a,b+1))
        si=block.find(start)
        if si<0:raise ValueError(f'missing start {key} {start}')
        ei=block.find(end,si)
        if ei<0:raise ValueError(f'missing end {key} {end}')
        selected=block[si:ei].strip()
        (BASE/'evidence/source-text'/f'{key}-complete-proof.txt').write_text(selected+'\n')
        return author_proofs[key]
    if e['proof_target'] and not e['proof_range']['pdf_pages']:
        return '本篇未提供独立展开的原作者证明；原陈述/论述完整页保留在来源入口。项目说明与共享证明另列，不冒充本篇原证明。'
    return '此项为定义、假设、算法或经验材料，本篇没有相应数学证明。'

statements={
 'reconstruction':r'\forall S\subseteq N,\quad v(x_S)=\sum_{T\subseteq S}I(T)+v(x_\varnothing).',
 'salient-approximation':r'v(x)\approx\sum_{S\in\Omega_{\mathrm{salient}},S\ne\varnothing}I(S)+v(x_\varnothing).',
 'lemma1':r'I(S)=\sum_{\kappa\in Q_S}\frac{D^\kappa v(r)}{\kappa!}\prod_{i\in S}(x_i-r_i)^{\kappa_i},\quad S\ne\varnothing.',
 'derivative-cutoff':r'\bigl[\forall r\in\mathbb R^n,\ \forall|\kappa|\ge M+1,\ D^\kappa v(r)=0\bigr]\Rightarrow\bigl[\forall S\subseteq N,\ |S|\ge M+1\Rightarrow I(S)=0\bigr].',
 'lemma2':r'\forall M\le m\le n,\quad\bar g_0^{(m)}=\sum_{k=1}^M\frac{\binom mk}{\binom nk}A^{(k)}.',
 'lemma3':r'\forall n,M\in\mathbb N^+,\ M<n:\quad\left[\forall m\in\{n,\ldots,n-M\},\ \sum_{k=1}^M\frac{\binom mk}{\binom nk}w_k=0\right]\Rightarrow\forall1\le k\le M,\ w_k=0.',
 'theorem2':r'\exists m_0\in\{n,\ldots,n-M\},\quad A^{(k)}=(\lambda^{(k)}n^{p+\delta}+a_{\lfloor p\rfloor-1}^{(k)}n^{\lfloor p\rfloor-1}+\cdots+a_1^{(k)}n+a_0^{(k)})\bar g_0^{(1)}\quad(1\le k\le M),',
 'theorem3':r'R^{(k)}\le\frac{\bar g_0^{(1)}}{\tau|\eta^{(k)}|}\left|\lambda^{(k)}n^{p+\delta}+a_{\lfloor p\rfloor-1}^{(k)}n^{\lfloor p\rfloor-1}+\cdots+a_0^{(k)}\right|.',
 'lemma4':r'\Delta_Tg_0(S)=\sum_{L\subseteq T}(-1)^{|T|-|L|}g_0(L\cup S)=\sum_{U\subseteq S}I(T\cup U),\quad T\cap S=\varnothing.',
 'theorem4':r'\phi(i)=\sum_{S\subseteq N\setminus\{i\}}\frac{I(S\cup\{i\})}{|S|+1}.',
 'theorem5':r'\operatorname{SI}(T)=\sum_{S\subseteq N\setminus T}\frac{I(S\cup T)}{|S|+1}.',
 'theorem6':r'\operatorname{ST}_k(T)=\begin{cases}I(T)&|T|<k\\\sum_{S\subseteq N\setminus T}\binom{|S|+k}k^{-1}I(S\cup T)&|T|=k\\0&|T|>k.\end{cases}',
 'axiom-efficiency':r'g_0(N)=\sum_{S\subseteq N}I(S).',
 'axiom-linearity':r'u=u_1+u_2\Rightarrow I_u(S)=I_{u_1}(S)+I_{u_2}(S).',
 'axiom-dummy':r'[\forall T\subseteq N\setminus\{i\},\ g_0(T\cup\{i\})=g_0(T)+g_0(\{i\})]\Rightarrow[\forall\varnothing\ne S\subseteq N\setminus\{i\},\ I(S\cup\{i\})=0].',
 'axiom-symmetry':r'[\forall T\subseteq N\setminus\{i,j\},\ g_0(T\cup\{i\})=g_0(T\cup\{j\})]\Rightarrow I(S\cup\{i\})=I(S\cup\{j\}).',
 'axiom-anonymity':r'I_{g_0}(S)=I_{\pi g_0}(\pi S),\quad (\pi g_0)(\pi T)=g_0(T).',
 'axiom-recursive':r'I(S\cup\{i\})=\sum_{L\subseteq S}(-1)^{|S|-|L|}g_0(L\cup\{i\})-I(S),\quad i\notin S.',
 'axiom-distribution':r'u_T(S)=c\mathbf1_{T\subseteq S}\quad\Rightarrow\quad I_{u_T}(S)=c\mathbf1_{S=T}.',
 'noise-linearity':r'I′(S)=I(S)+\sum_{T\subseteq S}(-1)^{|S|-|T|}(\varepsilon_T-\varepsilon_\varnothing).',
 'noise-variance':r'\operatorname{Var}(I_\varepsilon(S))\text{ is }2^{|S|}\text{ times the noise variance}.',
 'parity-mask':r'u(S)=1\text{ if }|S|\text{ odd},\quad u(S)=-1\text{ otherwise}.',
 'transfer-inference':r'\text{sparsity}+\text{universal matching}\Rightarrow\text{sample-wise transferability}.',
 'or-reverse':r'I_\lor(S)=-\sum_{T\subseteq S}(-1)^{|S|-|T|}g_0(N\setminus T),\quad I_\lor(\varnothing)=0.',
 'and-or-matching':r'g_0(S)=g_\land(S)+g_\lor(S),\quad g_\land(S)=\sum_{T\subseteq S}I_\land(T),\quad g_\lor(S)=\sum_{T\cap S\ne\varnothing}I_\lor(T).',
 'monotonicity-example':r'v(z)=z_1z_2z_3+z_1z_2+z_2z_3+z_2+z_3,\quad\mathbb E_{|S|=2}u(S)\le\mathbb E_{|S|=3}u(S).',
 'sampling-complexity':r'\widehat{\bar g_0}^{(m)}=\frac1t\sum_{j=1}^tg_0(S_j),\quad |S_j|=m,\quad O(nt)\text{ model queries}.',
 'assumption-1alpha':r'\forall S\subseteq N,\ |S|\ge M+1\Rightarrow I(S)=0.',
 'assumption-1beta':r'\forall r\in\mathbb R^n,\ \forall\kappa\in\mathbb N^n,\ |\kappa|\ge M+1\Rightarrow D^\kappa v(r)=0.',
 'assumption2':r'\forall 0\le m′\le m\le n,\ \bar g_0^{(m′)}\le\bar g_0^{(m)}.',
 'assumption3':r'\forall m′\le m,\quad\bar g_0^{(m′)}\ge(m′/m)^p\bar g_0^{(m)},\quad p>0.'}

shared={
 'reconstruction':['proof-finite-mobius-reconstruction-v2'],
 'lemma1':['proof-finite-mobius-uniqueness-v2'],
 'derivative-cutoff':['proof-finite-mobius-uniqueness-v2'],
 'axiom-linearity':['shared-harsanyi-linearity'], 'axiom-dummy':['shared-harsanyi-dummy-nonempty'],
 'axiom-symmetry':['shared-harsanyi-symmetry'], 'axiom-anonymity':['shared-harsanyi-anonymity'],
 'axiom-recursive':['shared-harsanyi-recursive'], 'axiom-distribution':['shared-harsanyi-interaction-distribution'],
 'lemma4':['shared-harsanyi-marginal-decomposition'], 'theorem4':['shared-harsanyi-shapley-dividend'],
 'theorem5':['shared-harsanyi-shapley-interaction-dividend'], 'theorem6':['shared-harsanyi-shapley-taylor-dividend'],
 'and-or-matching':['shared-harsanyi-or-reconstruction']}
assumptions={
 'lemma1':['原Lemma未单独声明Taylor级数收敛/等于函数；B.2作为1β推1α的预备引理，作用域缺口单列。'],
 'derivative-cutoff':['原Assumption1β全空间高阶导数为零与论文可微函数背景。'],
 'lemma2':['有限总体n=|N|','原中心化I(∅)=0','Assumption1α','M≤m≤n'],
 'lemma3':['n,M正整数，M<n','全部M+1行等式'],
 'theorem2':['Assumptions1α、2、3','p>0；原对数/组合分母定义域n>1、M≤n','原M=0作用域缺口另列；正阶构造包含M=n，未沿用Lemma3的M<n','低位全0见证覆盖有限空索引族'],
 'theorem3':['原Case1非完全抵消范围；η≠0','τ>0','Theorem2的同一A(k)系数表示'],
 'lemma4':[r'T⊆N\S，即T与S不相交'],
 'axiom-dummy':['g0(∅)=0','S明确非空，忠实于本篇A.1(3)'],
 'axiom-distribution':['按uT显示定义取Möbius变换；T=∅时uT不再符合g0(∅)=0，但变换恒等式自身仍有意义'],
 'theorem4':['有限总体，i∈N；经典Shapley定义'],
 'theorem5':['经典SII阶乘权重定义与有限总体'],
 'theorem6':['原STI定义对应1≤k≤n；三分支保留']}
REPORT=BASE/'verification/report.json'
report=json.loads(REPORT.read_text()) if REPORT.exists() else {}
audited={d['name']:d for d in report.get('declarations',[])}
finite_report_path=Path('research/full-proof-integration-20260930/cvpr2023/verification/report.json')
finite_report=json.loads(finite_report_path.read_text()) if finite_report_path.exists() else {}
finite_audited={d['name']:d for d in finite_report.get('declarations',[])}
lean_map={
 'reconstruction':['FullSparse.theorem1'], 'lemma2':['FullSparse.lemma2','Harsanyi.Sparsity.mean_centered_cutoff'],
 'lemma3':['Harsanyi.Sparsity.binomial_matrix_kernel'],
 'theorem2':['FullSparse.theorem2','Harsanyi.Sparsity.sparse_original_coefficient_witness','Harsanyi.Sparsity.sparse_coefficient_existence','Harsanyi.Sparsity.coefficient_normalization'],
 'theorem3':['FullSparse.theorem3','Harsanyi.Sparsity.sparse_original_T2_T3','Harsanyi.Sparsity.salient_bound_original_coefficients','Harsanyi.Sparsity.salient_count_bound'],
 'axiom-linearity':['FullSparse.linearity'],'axiom-dummy':['FullSparse.dummy'],
 'axiom-symmetry':['FullSparse.symmetry'],'axiom-anonymity':['FullSparse.anonymity'],
 'axiom-recursive':['FullSparse.recursive'],'axiom-distribution':['FullSparse.distribution'],
 'lemma4':['FullSparse.lemma4'],'theorem4':['FullSparse.theorem4'],'theorem5':['FullSparse.theorem5'],'theorem6':['FullSparse.theorem6'],
 'noise-linearity':['FullSparse.noise_linearity'],'or-reverse':['FullSparse.or_reverse'],'and-or-matching':['FullSparse.and_or_matching_eq62','FullSparse.and_matching_zero_baseline','FullSparse.or_matching_zero_baseline','FullSparse.and_or_matching'],
 'monotonicity-example':['FullSparse.example_mean_two','FullSparse.example_mean_three','FullSparse.example_mean_monotone_comparison'],
 'sampling-complexity':['FullSparse.sampling_evaluation_count']}
scope_map={
 'theorem2':'all original coefficient constraints and both sign implications in positive-order defined domain n>1, 1≤M≤n, including M=n; source M=0 reading issue remains; finite low-family J arbitrary, all-zero witness covers p<1',
 'theorem3':'source non-cancellation τ>0, η≠0 scope; exact T2 witness constructed from original three assumptions and substituted into the count formula; same parameter-domain note as T2',
 'monotonicity-example':'only original actual five-coordinate polynomial example: μ2=1, μ3=19/10 and μ2≤μ3; not a general monotonicity theorem',
 'sampling-complexity':'exact requested model evaluation count n*t on positive mask-size layers; no runtime or concentration statement',
 'axiom-distribution':'displayed uT unanimity game including T=empty constant-game transform; no false claim that nonzero constant game is centered',
 'and-or-matching':'literal Eq62 with a(empty)=b(empty)=0: both component sums and their combined actual centered model output; baseline-preserving generic identity is a separate helper',
 'theorem4':'classic factorial-weighted Shapley equivalent to original per-cardinality average definition, actual centered model game',
 'theorem5':'classic factorial SII including all finite targets and empty targets',
 'theorem6':'all three original branches for positive k, actual centered masked model game'}

def lean_refs(names):
    refs=[]
    for n in names:
        d=audited.get(n) or finite_audited.get(n)
        if d and d.get('status')=='passed':
            refs.append({'declaration':n,'source_path':d['source_path'],'line':d['line'],'scope':'actual_proved_statement_or_internal_proof_dependency',
              'report_path':str(REPORT if n in audited else finite_report_path),'explanation_md':'文字阶段对应该真实声明或其内部证明；不把阶段数量称为新Lean定理数。'})
    return refs

def lean_record(key):
    names=lean_map.get(key,[])
    ds=[audited[n] for n in names if n in audited]
    if names and len(ds)==len(names) and report.get('status')=='passed':
        d=ds[0]
        return {'status':'verified','verification_role':'theorem_proof','evidence_role':'theorem_proof','declarations':names,'compiled':True,'axiom_audit':'passed',
          'report_path':str(REPORT),'build_id':report['build_id'],'source_fingerprint':report['source_fingerprint'],
          'source_path':d['source_path'],'line':d['line'],'statement':d['signature'],'scope':scope_map.get(key,'entire source mathematical target with actual model/mask/baseline alignment'),
          'completion_scope':scope_map.get(key,'entire source mathematical target'),'axioms':sorted(set(a for d in ds for a in d['axioms'])),
          'source_semantics_automatically_verified':False,'label':'所列精确范围已编译并审计；原来源问题另列'}
    return {'status':'not_formalized','verification_role':'none','evidence_role':'none','completion_scope':'no complete Lean claim; see exact source/explanation scope'}


core=['model-output','fixed-input','input-baseline-vector','variable-universe','coalition','masked-input','masked-game','output-baseline','centered-game','interaction-centered']
order=['interaction-order','cutoff-order','mask-order','interaction-order-index','mean-output','order-total']
coeff=['robustness-exponent','leading-coefficient','leading-aggregate','growth-offset','nary-digit','nary-aggregate','witness-order']
symbols_by_key={
 'definitions':core,'desiderata':core+['salience-threshold'],
 'reconstruction':core,'salient-approximation':core+['salience-threshold'],
 'taylor-expansion':['model-output','fixed-input','input-baseline-vector','input-coordinate','variable-count','taylor-multiindex','mixed-derivative'],
 'assumption-1alpha':core+['interaction-order','cutoff-order'],
 'assumption-1beta':['model-output','input-baseline-vector','variable-count','cutoff-order','taylor-multiindex','mixed-derivative'],
 'lemma1':core+['input-coordinate','variable-count','taylor-multiindex','taylor-support-class','taylor-restricted-class','mixed-derivative'],
 'derivative-cutoff':core+['input-coordinate','variable-count','interaction-order','cutoff-order','taylor-multiindex','taylor-support-class','mixed-derivative'],
 'assumption2':core+['mask-order','mean-output'],
 'assumption3':core+['mask-order','mean-output','robustness-exponent'],
 'order-statistics':core+['interaction-order-index','order-total','cancellation-ratio','salient-count','salience-threshold'],
 'lemma2':core+['variable-count']+order,
 'lemma3':['variable-count','cutoff-order','mask-order','interaction-order-index'],
 'theorem2':core+['variable-count']+order+coeff+['normalized-interaction','nary-degree'],
 'asymptotic-claim':core+order+coeff+['cancellation-ratio','salience-threshold','salient-count'],
 'theorem3':core+['variable-count']+order+coeff+['cancellation-ratio','salience-threshold','salient-count'],
 'axiom-linearity':core,'axiom-dummy':core,'axiom-symmetry':core,
 'axiom-anonymity':core,'axiom-recursive':core+['marginal-difference'],'axiom-distribution':core,
 'lemma4':core+['marginal-difference'],
 'theorem4':core+['variable-count','marginal-difference','shapley-value','beta-function'],
 'theorem5':core+['variable-count','marginal-difference','shapley-interaction','beta-function'],
 'theorem6':core+['variable-count','marginal-difference','shapley-taylor','beta-function'],
 'noise-linearity':core+['output-noise'],
 'noise-variance':core+['interaction-order','output-noise'],
 'parity-mask':core+['mask-order','interaction-order'],
 'or-density':core+['or-interaction'],'periodic-density':core,'parity-task':core+['robustness-exponent'],
 'transfer-inference':core+['salience-threshold'],
 'or-reverse':core+['or-interaction'],
 'and-or-matching':core+['or-interaction','and-component','or-component'],
 'and-or-optimization':core+['or-interaction','and-component','or-component','decomposition-parameter','output-noise','noise-bound'],
 'threshold-discussion':core+['salience-threshold'],
 'monotonicity-example':core+['variable-count','mask-order','mean-output'],
 'sampling-complexity':core+['variable-count','mask-order','mean-output','sample-count'],
 'experiments':core+['interaction-order','mean-output','robustness-exponent','salience-threshold'],
 'related-work':core
}
property_adapters={
 'axiom-linearity':'两个中心化集合函数的和仍中心化；公共线性恒等式对任意有限S成立，代入原u、u1、u2即可，包括空集。',
 'axiom-dummy':'原A.1(3)已有S非空与i∉S。取公共常数c=u({i})，把原全体T的加法条件限制到U⊆S；完整非空dummy证明逐项满足前提。不能引用CVPR的空集量词版本。',
 'axiom-symmetry':r'原对所有T⊆N\{i,j}的相等条件蕴含对子集U⊆S的相等；i,j均不在S，公共对称证明应用于原u。',
 'axiom-anonymity':'把论文的排列π作为有限变量的等价映射。重标记掩码、u与交互，公共重标记证明对任意集合函数成立；中心化空集也保留。',
 'axiom-recursive':'原i∉S，公共context差分恒等式给I(S∪{i})=I_{u(·∪{i})}(S)−I_u(S)；展开前一交互即原递归式。',
 'axiom-distribution':'原显示uT(S)=c当T⊆S，否则0，直接是公共unanimity函数；其Möbius变换仅在S=T取c。T=∅时显示函数是常数c，空集交互c；不能把此时uT又当成全局中心化u。',
 'lemma4':r'取公共higherMarginal中的g=u=g0；原T⊆N\S给Disjoint T S，公共恒等式不要求非空，因此T或S空也保持原正确等式。',
 'theorem4':'取公共factorialShapley中的g=u、有限N及i∈N。原按阶均匀平均权重1/[n choose(n−1,|S|)]与|S|!(n−|S|−1)!/n!完全相等；公共有限卷积证明含L=∅边界，得到原每个交互1/(|S|+1)的分摊。',
 'theorem5':'原SII定义的|S|!(n−|T|−|S|)!/(n−|T|+1)!就是公共factorialShapleyInteraction。代入u和T⊆N，完整有限卷积覆盖空T、空环境和空L，得到原1/(|S|+1)展开。',
 'theorem6':'公共shapleyTaylor采用原k/n·choose(n−1,|S|)的倒数权重、同一有限N与u。原阶k为正，T⊆N；共享证明完整给|T|<k、=k、>k三支，临界阶通过正阶factorial卷积得到choose(|S|+k,k)的倒数，所有空环境分支都包括。'
}


stage_spec={
 'reconstruction':[(r'所有求和都包含空集','空集与有限换序',['Harsanyi.reconstruction']),(r'最后一步只留下','保留唯一项与基线',['FullSparse.theorem1'])],
 'lemma2':[(r'先对每个','重构与阶数分组',['Harsanyi.Sparsity.layer_sum_reconstruct']),(r'对一个固定','含给定交互的掩码双射',['Harsanyi.Sparsity.card_supermasks','Harsanyi.Sparsity.subset_layer_sum']),(r'因为','组合数比值',['Harsanyi.Sparsity.choose_ratio']),(r'除以','中心化与高阶截断',['Harsanyi.Sparsity.mean_centered_cutoff','FullSparse.lemma2']),(r'例如','边界与三变量核对',[])],
 'lemma3':[(r'沿 Eq. (32)','作者行列式的符号修复',[]),(r'实际 Lean 使用','全量有限差分归纳',['Harsanyi.Sparsity.choose_coefficients_zero','Harsanyi.Sparsity.binomial_matrix_kernel'])],
 'theorem2':[(r'写 \(\mu_m','原平均条件的上下界',['Harsanyi.Sparsity.sparse_coefficient_existence']),(r'当 \(\mu_1>0','正均值的归一化与对数界',['Harsanyi.Sparsity.coefficient_normalization']),(r'当 \(\mu_1=0','零均值推出全部阶总效应零',['Harsanyi.Sparsity.mean_centered_cutoff_all','Harsanyi.Sparsity.binomial_coefficients_zero_of_le']),(r'现在取 \(m_0','零均值系数见证',['Harsanyi.Sparsity.coefficient_normalization']),(r'低位可规范写为','低位索引与完整原约束',['Harsanyi.Sparsity.sparse_original_coefficient_witness','FullSparse.theorem2'])],
 'theorem3':[(r'第一步是','阈值计数与抵消关系',['Harsanyi.Sparsity.threshold_count','Harsanyi.Sparsity.salient_count_bound']),(r'再代入 Theorem 2','代入同一系数表示及Case1边界',['Harsanyi.Sparsity.salient_bound_original_coefficients','Harsanyi.Sparsity.sparse_original_T2_T3','FullSparse.theorem3'])],
 'monotonicity-example':[(r'全阶也可用','仅此算例的层均值核对',['FullSparse.example_mean_two','FullSparse.example_mean_three','FullSparse.example_mean_monotone_comparison'])],
 'sampling-complexity':[(r'单次 DNN 推理','查询次数与实际运行成本的范围',[])]
}
stage_spec['asymptotic-claim']=[
 (r'构造有限符号族','无限参数族与完整符号划分',[]),
 (r'固定同一输入','实际模型及其全部交互系数',[]),
 (r'验证原截断与平均条件','逐项验证原三假设',[]),
 (r'固定显著阈值','原阈值、抵消比例与同阶稠密性',[]),
 (r'核对反例的影响范围','精确T3仍成立与反驳子句的范围',[])]

def steps_for(key,body,eid):
    if not body:return []
    cuts=[(0,'定义、目标与原条件',lean_map.get(key,[]))]
    for anchor,title,names in stage_spec.get(key,[]):
        pos=body.find(anchor)
        if pos>0:cuts.append((pos,title,names))
    cuts.sort();cuts.append((len(body),'',[]))
    steps=[]
    for j,(pos,title,names) in enumerate(cuts[:-1]):
        chunk=body[pos:cuts[j+1][0]].strip()
        if not chunk:continue
        steps.append({'id':eid+'-step-'+str(j+1),'title':title,'body_md':chunk,'formula_tex':statements.get(key,'') if j==0 else '',
          'justification':'原条件、明确有限索引依据与完整共享证明；修复只改变证明步骤。','lean_refs':lean_refs(names)})
    return steps

results=[]
for e in inv['entries']:
    if e['id']!=e['merge_id']:
        continue
    key=e['id'].removeprefix('iclr2024-sparse-')
    refs=e['evidence']
    body=rewrites.get(key)
    is_target=e['proof_target']
    blocked=key in ['lemma1','noise-variance','parity-mask','transfer-inference','asymptotic-claim']
    shared_ids=shared.get(key,[])
    if key in property_adapters:
        body='完整公共中文证明可由共享ID进入；下文是本篇逐项条件适配。\n\n'+property_adapters[key]
        if key in ['theorem4','theorem5','theorem6']:
            body+=' 原Beta/零参数/自由索引错误逐式保留于原文与issue；项目修复使用同一原指标的有限组合证明，原陈述保持。'
    if not body and shared_ids:
        body='完整共享证明见关联入口；本篇应用条件另列。'
    status=('blocked_by_false_statement' if key=='transfer-inference' else 'blocked_by_source_issue') if blocked else ('complete' if body else 'not_started')
    if not is_target:status='not_applicable'
    original_statement=author_statements[key]
    semantic_symbols=list(dict.fromkeys(symbols_by_key[key]))
    steps=steps_for(key,body,e['id'])
    results.append({'id':e['id'],'paper_id':'iclr2024-sparse','title':e['title'],'kind':e['kind'],'original_label':e['original_label'],
      'aliases':e['aliases'],'inventory_ids':[x['id'] for x in inv['entries'] if x['merge_id']==e['id']],
      'source_refs':refs,'statement_tex':statements.get(key,''),'verification_role':'scope_explanation' if key in ['salient-approximation','asymptotic-claim'] else ('counterexample_or_scope_analysis' if blocked else 'theorem_proof'),'statement_status':('general_smooth_reading_refuted; given_Taylor_representation_reading_not_refuted; 1beta_application_separate' if key=='lemma1' else ('positive_order_domain_proof_complete; M0_reading_counterexample_separate' if key=='theorem2' else 'see_original_source_scope_and_issues')),'assumptions':assumptions.get(key,[]),
      'definitions':semantic_symbols,
      'original_statement_md':original_statement,'original_proof_md':original_proof(key,e),
      'original_statement_source_type':'source_mathematical_statement_tex_with_textual_paraphrase_and_explicit_scope_notes',
      'original_proof_source_type':'complete_source_mathematical_proof_tex_with_textual_paraphrase_and_explicit_transcription_notes' if key in proof_bounds else 'no_local_original_proof',
      'original_statement_note':'原数学陈述精确切分、TeX转录，保留原符号及原错式；英文连接文字为忠实意译，来源边界说明另标。非逐字全文引用。statement_tex是项目规范式。',
      'original_proof_note':'11个原局部证明逐式完整数学转录，英文连接文字忠实意译；每个推导等式和原错误均保留。正式页图与raw文本用于核查；项目修复另列。',
      'overview':(body.split('\n\n')[1] if body and '\n\n' in body else e['classification_reason']),
      'proof_steps':steps,'shared_proof_ids':shared_ids,'shared_alignment_status':'explicit_premise_alignment_to_complete_shared_proof' if shared_ids else 'not_applicable',
      'symbol_ids':semantic_symbols,
      'notation_map':[{'source':'u(S)','canonical':'g0(S)','meaning':'去模型输出基线；不是v(x_∅)=0'},{'source':'b','canonical':'r','meaning':'输入基线向量'}],
      'rewrite_status':status,'completion_scope':(scope_map.get(key,'scope explanation only; original unquantified claim not proved as a new theorem' if key in ['salient-approximation','asymptotic-claim'] else 'entire source target') if status=='complete' else ('original source preserved; exact mathematical issue listed' if blocked else 'continuing precise mathematical target')),
      'alignment_status':'agent_checked_full_source_range','user_review_status':'pending','lean':lean_record(key),
      'related_issue_ids':e['related_issue_ids'],'proof_target':is_target})

asymptotic=next(r for r in results if r['id']=='iclr2024-sparse-asymptotic-claim')
asymptotic['title']='渐近稀疏解释与Case2同阶稀疏推断的无限反例'
asymptotic['overview']='原三项假设允许一个光滑二次模型无限族，其二阶抵消比例仅按多项式衰减，却有全部二阶交互显著。因此第8页Case2从非指数小抵消比例推出同阶稀疏的额外推断不成立。精确Theorem2、3仍成立，相邻mostcases经验描述和相对全部2^n组合的稀疏性不被此反例否定；另保留参数随n变化的大O作用域说明。'
asymptotic['verification_role']='counterexample'
asymptotic['statement_status']='specific_case2_per_order_inference_refuted; adjacent_mostcases_not_refuted; exact_T2_T3_unchanged'
asymptotic['completion_scope']='complete infinite-family counterexample under all original three assumptions to p8 Case2 per-order sparsity inference; finite-n BigO scope also explained; original T2/T3 and empirical mostcases not refuted'
asymptotic['lean']['verification_role']='counterexample'
asymptotic['lean']['evidence_role']='counterexample'
asymptotic['lean']['completion_scope']='No new Lean counterexample claim; complete original-assumption infinite-family proof is in the project Chinese layer'
asymptotic['clause_assessments']=[
 {'id':'case2_nonexponential_eta_implies_per_order_sparsity','status':'refuted','scope':'actual original-assumption infinite family n≡2/3 mod4, M=2,p=1,τ=.01,η2=−1/choose(n,2),R2=choose(n,2)'},
 {'id':'case1_mostcases','status':'empirical_not_refuted','scope':'not read as a universal quantified theorem'},
 {'id':'exact_T2_T3','status':'unchanged_and_verified','scope':'the exact coefficient existence and count inequality; source parameter-domain notes remain'},
 {'id':'finite_n_bigO_interpretation','status':'scope_explanation','scope':'n-dependent δ,η,τ do not by themselves supply a uniform asymptotic comparison'}]
shared_proofs=[]
derivative_path=Path('research/full-proof-integration-20260930/cvpr2023/derivative-cutoff-results.json')
if derivative_path.exists():
    derivative=json.loads(derivative_path.read_text())
    patch=derivative['results'][0]
    target=next(r for r in results if r['id']==patch['id'])
    # The owner keeps the complete author transcription and exact source boundaries.
    for field in ['overview','proof_steps','shared_proof_ids','assumptions','rewrite_status',
                  'completion_scope','alignment_status','lean','source_proof_correction_note_md']:
        if field in patch:target[field]=patch[field]
    target['lean']['evidence_role']='theorem_proof'
    target['lean']['verification_role']='theorem_proof'
    target['lean']['declarations']=list(dict.fromkeys(
      ['FullSparseDerivative.assumption1beta_implies1alpha']+target['lean']['declarations']))
    target['proof_steps'][0]['body_md']='\n\n'.join(
      [d['body_md'] for d in patch['definitions']]+[target['proof_steps'][0]['body_md']])
    target['statement_status']='original_classical_high_derivative_exists_and_zero_implication_proved; independent_general_Taylor_lemma_scope_unchanged'
    target['symbol_ids']=[s for s in symbols_by_key['derivative-cutoff'] if s!='taylor-support-class']+[s['id'] for s in derivative['symbols']]
    target['definitions']=target['symbol_ids']
    shared_proofs=derivative['shared_proofs']
    for proof in shared_proofs:
        if proof.get('lean'):
            proof['lean']['evidence_role']='theorem_proof'
            proof['lean']['verification_role']='theorem_proof'
    known={s['id'] for s in sym}
    sym.extend(s for s in derivative['symbols'] if s['id'] not in known)

content={'schema_version':'full-paper-content-1.0','paper_id':'iclr2024-sparse','results':results,'shared_proofs':shared_proofs,
 'issues':issues,'symbols':sym,'inventory_path':str(BASE/'inventory.json'),'rewrite_path':str(BASE/'math/rewrites.zh.md'),
 'source_transcription_status':'42 precise mathematical statement blocks and all 11 complete local mathematical proofs transcribed in TeX; narrative is faithful paraphrase, source page images retained; source-math range reviewed by agent',
 'authorization':'proof_only_granted; no original proposition or assumption change',
 'counts':{'directory_results':len(results),'proof_targets':sum(r['proof_target'] for r in results),
           'by_rewrite_status':{s:sum(r['rewrite_status']==s for r in results) for s in sorted(set(r['rewrite_status'] for r in results))}}}
(BASE/'content.json').write_text(json.dumps(content,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(content['counts'],ensure_ascii=False))
