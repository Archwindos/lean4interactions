from pathlib import Path
import json

BASE=Path('research/full-proof-integration-20260930/cvpr2023')
PAPER='cvpr2023-sparse-concepts'
symbols=[]
def add(id,tex,name,definition,domain,scope,original,pages,description='',empty='不适用',baseline='固定输入基线r；不假定输出基线为0',names=None,relation='renaming',source='main',formula=None,assumptions=None):
    x={'id':id,'canonical_id':id,'canonical_tex':tex,'name_zh':name,'definition_tex':definition,
      'description_md':description or name,'type_or_domain':domain,'scope':scope,
      'assumptions':assumptions or [],'empty_set_convention':empty,'baseline_convention':baseline,
      'aliases':[original],'paper_mappings':[{'paper_id':PAPER,'version_id':'ver-cvpr2023-formal',
        'original_tex':original,'original_definition_tex':definition,'source_id':'src-cvpr2023-main' if source=='main' else 'src-cvpr2023-supplement',
        'pdf_pages':pages,'equation_label':formula,'relation_type':relation,'canonical_id':id}],
      'lean_names':names or [],'version':'full-paper-20260930','alignment_status':'agent_checked_definition','user_review_status':'pending'}
    symbols.append(x)

add('sym-model',r'v:X\to\mathbb R','模型输出函数',r'v(x_S)\in\mathbb R','X→ℝ','all paper',r'v(\boldsymbol x)',[3],description='实数输出分数；分类实例用对数几率。模型的输入是完整输入对象，集合参数属于其掩码适配。',names=['FullCvpr.maskedGame'],relation='same_definition')
add('sym-input',r'x','固定原输入',r'x\in X','输入向量；原文n个变量','one input-specific explanation',r'\boldsymbol x',[3],relation='same_definition')
add('sym-universe',r'N','有限变量总体',r'N=\{1,\ldots,n\}','finite set','fixed input sample',r'\mathcal N',[3],empty='n=0的代数边界允许；Shapley选i∈N时强制n≥1',relation='same_definition')
add('sym-cvpr-input-dimension',r'n','输入变量数',r'n=|N|','ℕ','fixed input sample',r'n',[3],empty='n=0时有唯一空掩码',relation='same_definition')
add('sym-coalition',r'S,T,A,U,L\subseteq N','变量子集',r'S\in\mathcal P(N)','finite subset','各公式内哑变量/目标集合须区分',r'\mathcal S,\mathcal T,\mathcal L',[3],empty='本篇子集和包括空集',relation='same_definition')
add('sym-input-baseline',r'r','输入基线向量',r'r=(r_1,\ldots,r_n)','与输入坐标同型的向量','mask rule and learned baseline',r'\boldsymbol r',[3,4,5],description='坐标缺失的替代输入值。不同r需各自重算g和交互；不是输出标量b。',formula='main (4)',relation='same_definition')
add('sym-mask',r'x_S','掩码输入',r'(x_S)_i=\begin{cases}x_i&i\in S,\\r_i&i\notin S\end{cases}','X','fixed x and r',r'\boldsymbol x_\mathcal S',[3,4],empty='x空=r；xN=x',formula='main (4)',relation='same_definition')
add('sym-game',r'g(S)','固定掩码集合函数',r'g(S)=v(x_S)','𝒫(N)→ℝ','all finite algebra proofs',r'v(\boldsymbol x_\mathcal S)',[3],description='项目规范集合函数，与原AOG结构g不同。',empty='g空=b',names=['Harsanyi.Game','FullCvpr.maskedGame'],relation='derived_quantity')
add('sym-output-baseline',r'b','输出基线标量',r'b=v(x_\varnothing)=g(\varnothing)','ℝ','fixed model,input,baseline',r'v(\boldsymbol x_\emptyset)',[3],empty='空集交互等于b',names=['Harsanyi.interaction_empty'],relation='derived_quantity')
add('sym-centered-game',r'g_0(S)','中心化集合函数',r'g_0(S)=g(S)-b','𝒫(N)→ℝ','cross-paper convention only; not CVPR original convention',r'\text{本篇没有单独中心化定义}',[3],description='规范派生量；不要将本篇w自动改成中心化交互。',empty='g0空=0是定义后果',names=['Harsanyi.centered'],relation='centered_variant')
add('sym-and-interaction',r'I_g(A)','原始AND交互',r'I_g(A)=\sum_{U\subseteq A}(-1)^{|A|-|U|}g(U)','𝒫(N)→ℝ','CVPR original uncentered coefficients',r'w_\mathcal S',[3],empty='I_g空=g空=b',names=['Harsanyi.interaction'],formula='main Theorem1; supp(1)',relation='renaming')
add('sym-order',r'|S|','交互阶数',r'\operatorname{order}(S)=|S|','ℕ','coalition-specific cardinality',r'|\mathcal S|',[3],empty='空集阶数0',relation='same_definition')
add('sym-cvpr-source-state',r'X_i','二值变量保留状态',r'X_i(x_T)=\mathbf1_{i\in T}','{0,1}','SCM input state',r'X_i',[3],empty='空掩码时所有Xi=0',formula='main(1)',relation='same_definition')
add('sym-cvpr-trigger',r'C_A(x_T)','AND模式触发状态',r'C_A(x_T)=\prod_{i\in A}X_i=\mathbf1_{A\subseteq T}','{0,1}','SCM and AOG',r'C_\mathcal S',[3,5],empty='空模式空积1',names=['FullCvpr.andTrigger','FullCvpr.andTrigger_product'],relation='same_definition')
add('sym-cvpr-causal-output',r'Y_\Omega(x_T)','因果图输出',r'Y_\Omega(x_T)=\sum_{A\in\Omega}w_A C_A(x_T)','ℝ','selected or full graph',r'Y(\boldsymbol x_\mathcal S)',[3,4],empty='若空模式保留则空输入Y=b；删去空模式则可有基线误差',names=['FullCvpr.causalOutput'],formula='main(2)',relation='renaming')
add('sym-cvpr-pattern-set',r'\Omega','保留模式集合',r'\Omega\subseteq\mathcal P(N)','finite set of finite subsets','full graph Theorem1 versus sparse selected graph 3.2',r'\Omega',[3,4,5],description='Theorem1中Omega=𝒫(N)；3.2中Omega是保留集合，不保证每个保留系数非零。两作用域明确区分。',empty='可含空模式；Omega本身也可为空',relation='same_definition')
add('sym-cvpr-alternative-coefficients',r'd_A','另一组重构系数',r'\forall T\subseteq N,\;g(T)=\sum_{A\subseteq T}d_A','𝒫(N)→ℝ','Appendix C uniqueness',r'\tilde w_\mathcal S',[3],source='supp',empty='d空=g空',names=['Harsanyi.reconstruction_unique'],relation='renaming')
add('sym-cvpr-context-interaction',r'I_{g_i}(S)','变量i始终存在的上下文交互',r'g_i(U)=g(U\cup\{i\});\ I_{g_i}(S)=\sum_{U\subseteq S}(-1)^{|S|-|U|}g_i(U)','ℝ','recursive axiom',r'w_{\mathcal S|i\ present}',[2,5],source='supp',empty='I_gi空=g(i)，不是原基线b',names=['Harsanyi.interaction_context_difference'])
add('sym-cvpr-permutation',r'\pi','变量置换',r'\pi:N\simeq N;\;g^\pi(V)=g(\pi^{-1}V)','bijection and relabeled game','anonymity axiom',r'\pi,\pi v',[2,5],source='supp',empty='π空=空',names=['Harsanyi.interaction_relabel'])
add('sym-cvpr-pure-and-coefficient',r'c','纯AND常数效应',r'u_A(S)=c\,\mathbf1_{A\subseteq S}','ℝ','interaction distribution axiom',r'c',[2,5,6],source='supp',empty='A空时uA为常数c；唯一空交互c',names=['Harsanyi.unanimity'])
add('sym-cvpr-marginal',r'\Delta_Tg(S)','环境中的高阶边际差分',r'\Delta_Tg(S)=\sum_{L\subseteq T}(-1)^{|T|-|L|}g(L\cup S)','ℝ','Theorem5 and attribution definitions',r'\Delta v_\mathcal T(\boldsymbol x_\mathcal S)',[2,6],source='supp',description='要求差分集合T与环境S不相交。与正文近似残差Δ不同。',empty='T空时等于g(S)；S空时等于I_g(T)',names=['Harsanyi.higherMarginal'],assumptions=[r'T\cap S=\varnothing'])
add('sym-shapley',r'\phi_g(i)','经典Shapley值',r'\phi_g(i)=\sum_{S\subseteq N\setminus\{i\}}\frac{|S|!(n-|S|-1)!}{n!}[g(S\cup\{i\})-g(S)]','ℝ, i∈N','Theorem2',r'\phi(i)',[4],description='先用经典阶乘权重定义，再证明等分交互式；非定义同义反复。',empty='环境S可空；w空不分给i',names=['Harsanyi.factorialShapley','Harsanyi.factorialShapley_eq_dividends'],assumptions=['i∈N，故n≥1'])
add('sym-cvpr-sii',r'I_g^{\rm Shapley}(T)','Shapley interaction 指数',r'\sum_{S\subseteq N\setminus T}\frac{|S|!(n-|T|-|S|)!}{(n-|T|+1)!}\Delta_Tg(S)','ℝ','Theorem3',r'I^{Shapley}(\mathcal T)',[2,8,9],source='supp',empty='原T⊆N量词允许T空；采用公式的空目标延伸，基线b参与',names=['Harsanyi.factorialShapleyInteraction'])
add('sym-cvpr-sti',r'I_g^{\rm ST(k)}(T)','Shapley–Taylor 指数',r'\begin{cases}\Delta_Tg(\varnothing)&|T|<k,\\\frac{k}{n}\sum_{S\subseteq N\setminus T}\binom{n-1}{|S|}^{-1}\Delta_Tg(S)&|T|=k,\\0&|T|>k\end{cases}','ℝ; positive order k','Theorem4',r'I^{Shapley\text{-}Taylor(k)}(\mathcal T)',[2,9,10,11],source='supp',empty='T空、k>0属低阶分支，值b；N空仍成立',names=['Harsanyi.shapleyTaylor'],assumptions=['T⊆N；正阶k≥1是有效定义域核验，原文只称k-th未明写不等式；k=0不在本轮对齐范围'])
add('sym-cvpr-sti-order',r'k','Shapley–Taylor最高保留阶数',r'k\in\mathbb N_{>0}','positive integer','Theorem4','k',[9,10,11],source='supp',description='独立于输入维数n和单个交互阶数|S|。作者原文只写k-th，项目正阶域是显式语义对齐，不能伪称作者给出k>0。',names=['Harsanyi.shapleyTaylor_eq_dividends'],assumptions=['正阶域；k=0未经原定义有效性核验'])
add('sym-cvpr-beta',r'B(p,q)','Beta辅助函数',r'B(p,q)=\int_0^1t^{p-1}(1-t)^{q-1}dt','p,q>0','author Theorem2–4 proof ingredient',r'B(p,q)',[7],source='supp',description='原第7页定义印作(1−t)^{1−q}，与后用公式冲突，原式保留在issue/transcript；新证明不用Beta。',relation='conflict',assumptions=['正确定义域p,q>0；原路线调用q=0非法'])
add('sym-cvpr-coefficient-weight',r'\alpha_L','原证明重排后的组合系数',r'\alpha_L=\sum_r\binom{m}{|L|+r}^{-1}\binom{m-|L|}{r}','ℝ','theorem-specific coefficient; m differs in Theorem2/3/4',r'\alpha_\mathcal L',[7,8,9,10,11],source='supp',description='按所属定理保存参数；不是AOG共用子节点α。',empty='L空必须保留，不可套用原非法Beta零参数')
add('sym-cvpr-support-budget',r'M_{\rm max}','最大保留模式数',r'|\Omega|\le M_{\rm max}','ℕ','main Eq.(5)',r'M',[4],description='与AOG节点集合𝓜不同。原L0=|Omega|有零系数边界问题。')
add('sym-cvpr-lasso-penalty',r'\lambda','稀疏惩罚系数',r'L=\operatorname{unfaith}(w_\Omega)+\lambda\|w_\Omega\|_1','real hyperparameter','main Eq.(6)',r'\lambda',[4,5],description='原约束→罚目标等价箭头并无一般证明，作为算法解释记录。')
add('sym-cvpr-unfaithfulness',r'\operatorname{unfaith}(w_\Omega)','全部掩码平方残差和',r'\sum_{T\subseteq N}[g(T)-Y_\Omega(x_T)]^2','ℝ≥0','main Eq.(5)',r'\mathrm{unfaith}(\boldsymbol w_\Omega)',[4],empty='含空掩码；完整权重必0，截断权重不必0',names=['FullCvpr.complete_unfaithfulness_zero'])
add('sym-cvpr-residual',r'\Delta_{\rm residual}','完整输入上未解释效应',r'\Delta_{\rm residual}=g(N)-\sum_{S\in\Omega}w_S','ℝ','main Eq.(7)',r'\Delta',[5],description='标量残差；不是Theorem5带集合下标的高阶差分Δ_Tg(S)。')
add('sym-cvpr-explained-ratio',r'R_\Omega','已解释效应比例',r'R_\Omega=\frac{\sum_{S\in\Omega}|w_S|}{\sum_{S\in\Omega}|w_S|+|\Delta_{\rm residual}|}','[0,1] when denominator positive','main Eq.(7)',r'R_\Omega',[5],empty='Omega空且gN=0时原定义0/0未给约定',assumptions=['表达式分母>0；原文未明示零分母规则'])
add('sym-cvpr-aog',r'G','And-Or图结构',r'G=\text{learned And-Or graph}','finite graph','main 3.3 and MDL',r'g',[5,6],description='原字母g是图，不是规范集合函数g(S)；必须按作用域区分。',relation='conflict')
add('sym-cvpr-node-set',r'\mathcal M','AOG节点词典集合',r'\mathcal M=N\cup\Omega_{\rm coalition}','finite node set','main3.3 and supp F',r'\mathcal M',[5,6],description='叶变量与新共享AND节点的集合；不是最大模式数M。',relation='same_definition')
add('sym-cvpr-shared-node',r'\alpha,\beta','共享AND子模式节点',r'\beta=\{x_5,x_6\}','finite coalition label','main Fig1 and 3.3',r'\alpha,\beta',[5],description='独立于定理证明中的组合系数α_L。',relation='same_definition')
add('sym-cvpr-children',r'\operatorname{Child}(A)','组成一个模式的子节点',r'C_A=\prod_{B\in\operatorname{Child}(A)}C_B','finite set of graph child nodes','main3.3',r'\operatorname{Child}(\mathcal S)',[5],empty='空子节点族积1',relation='same_definition')
add('sym-cvpr-description-length',r'L(G,\mathcal M)','MDL总描述长度',r'L(G,\mathcal M)=L(\mathcal M)+L_\mathcal M(G)','real objective','main Eq.(8), supp F',r'L(g,\mathcal M)',[5,6],description='后两项为节点词典与图的编码描述长度；不是集合L的基数。')
add('sym-cvpr-mdl-efficiency',r'\delta_{\rm MDL}(\alpha)','共享节点的描述长度变更率',r'\delta_{\rm MDL}(\alpha)=\frac{L(G,\mathcal M\cup\{\alpha\})-L(G,\mathcal M)}{|\alpha|}','ℝ; nonempty α','supp F Eq.(3)',r'\delta(\alpha)',[12],source='supp',empty='需α非空方可除其大小',description='ΔL是长度变化，不是模型输出残差Δ。')
add('sym-cvpr-baseline-radius',r'\tau_{\rm baseline}','基线学习的允许范围',r'\|r_i-r_i^{initial}\|_2\le\tau_{\rm baseline}','nonnegative real','main3.2,4.2; supp E',r'\tau',[5,8],description='实验设0.01 Var[x_i]；与And-Or人工显著激活阈值0.5区分。')
add('sym-cvpr-label-threshold',r'\tau_{\rm label}','人工真值模式激活阈值',r'\tau_{\rm label}=0.5','real threshold','supp G.3 And-Or labeling',r'\tau',[14],source='supp',description='人工标签规则，不等价全部Harsanyi交互真值。')

mapping={
'cvpr2023-reconstruction':['sym-cvpr-trigger','sym-cvpr-causal-output','sym-cvpr-pattern-set'],
'cvpr2023-uniqueness':['sym-cvpr-alternative-coefficients'],
'cvpr2023-linearity':[], 'cvpr2023-dummy':[], 'cvpr2023-symmetry':[],
'cvpr2023-anonymity':['sym-cvpr-permutation'], 'cvpr2023-recursive':['sym-cvpr-context-interaction'],
'cvpr2023-interaction-distribution':['sym-cvpr-pure-and-coefficient'],
'cvpr2023-marginal-decomposition':['sym-cvpr-marginal'],
'cvpr2023-shapley':['sym-shapley','sym-cvpr-marginal','sym-cvpr-coefficient-weight','sym-cvpr-beta'],
'cvpr2023-shapley-interaction':['sym-cvpr-sii','sym-cvpr-marginal','sym-cvpr-coefficient-weight','sym-cvpr-beta'],
'cvpr2023-shapley-taylor':['sym-cvpr-sti','sym-cvpr-sti-order','sym-cvpr-marginal','sym-cvpr-coefficient-weight','sym-cvpr-beta'],
'cvpr2023-scm-subset-sum':['sym-cvpr-source-state','sym-cvpr-trigger','sym-cvpr-causal-output','sym-cvpr-pattern-set'],
'cvpr2023-baseline-faithfulness':['sym-cvpr-unfaithfulness','sym-cvpr-pattern-set'],
'cvpr2023-aog-regrouping':['sym-cvpr-aog','sym-cvpr-shared-node','sym-cvpr-children','sym-cvpr-trigger'],
'cvpr2023-addmul-coefficients':['sym-cvpr-pure-and-coefficient']}
core=['sym-model','sym-input','sym-input-baseline','sym-mask','sym-universe','sym-cvpr-input-dimension','sym-coalition','sym-game','sym-output-baseline','sym-and-interaction','sym-order']
(BASE/'symbols.json').write_text(json.dumps({'paper_id':PAPER,'symbols':symbols},ensure_ascii=False,indent=2)+'\n')
d=json.loads((BASE/'content.json').read_text());d['symbols']=symbols
for r in d['results']:r['symbol_ids']=core+mapping[r['id']]
(BASE/'content.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
print(len(symbols),'symbol records bound to results')
