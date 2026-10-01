import json
from pathlib import Path

BASE=Path('research/full-proof-integration-20260930/iclr2024-sparse')
PAPER='iclr2024-sparse'
symbols=[]

def symbol(key, canonical, name, definition, domain, scope, original, pages, equations=None,
           relation='same_definition', empty='', baseline='', conflict='', assumptions=None, lean=None):
    symbols.append({'id':key,'canonical_tex':canonical,'name_zh':name,'definition_tex':definition,
        'description_md':conflict or name,'type_or_domain':domain,'scope':scope,'assumptions':assumptions or [],
        'empty_set_convention':empty,'baseline_convention':baseline,'aliases':[original],
        'paper_mappings':[{'paper_id':PAPER,'source_id':'src-iclr2024-sparse-main','version':'ICLR 2024 formal',
            'original_tex':original,'original_definition_tex':definition,'pdf_pages':pages,'equation_labels':equations or [],
            'canonical_concept_id':key,'relation_type':relation,'conflict_note':conflict}],
        'lean_names':lean or [],'version':'1.0'})

symbol('model-output','v','固定的标量模型',r'v:X\to\mathbb R','X→ℝ','论文全局','v',[3,5],lean=['SparseFull.maskedGame'])
symbol('fixed-input','x','固定待解释输入',r'x=(x_1,\ldots,x_n)','X；Taylor部分X=ℝⁿ','固定样本','x',[3,5])
symbol('input-baseline-vector','r','输入掩码基线向量',r'r=(r_1,\ldots,r_n)','ℝⁿ或对应输入域','掩码 / Taylor','b',[3,5,15,16],relation='renaming',baseline='x_∅=r；这不是输出标量基线',conflict='原b表示输入基线向量；规范b专指v(x_∅)。')
symbol('input-coordinate','x_i','输入坐标',r'x_i=\text{第i个输入变量}','ℝ或输入变量域','固定样本','x_i',[3,5,16])
symbol('variable-universe','N','有限变量总体',r'N=\{1,\ldots,n\}','有限集合','全局','N',[3,14],lean=['Finset (Fin n)'])
symbol('variable-count','n','输入变量数','n=|N|','ℕ，相关对数/矩阵段n>M≥1','全局','n',[3,7,17])
symbol('coalition','S','保留变量集合',r'S\subseteq N','Finset N','掩码与交互','S,T,L,K',[3,14,21],empty='允许空集；特定命题的非空限制单独保留')
symbol('masked-input','x_S','保留S的掩码输入',r'(x_S)_i=\begin{cases}x_i&i\in S\\r_i&i\notin S\end{cases}','X','固定x,r,N','x_S',[3,16],empty='x_∅=r',baseline='输入基线向量r',lean=['mask : Finset (Fin n) → X'])
symbol('masked-game','g','掩码集合函数','g(S)=v(x_S)','Finset N→ℝ','固定样本','v(x_S)',[3,4,15],relation='derived_quantity',empty='g(∅)=b，未假设为0',lean=['SparseFull.maskedGame','Harsanyi.Game'])
symbol('output-baseline','b','模型输出基线标量',r'b=v(x_\varnothing)','ℝ','固定样本','v(x_∅)',[3,4,15],relation='renaming',baseline='与输入r及原文输入b不同')
symbol('centered-game','g_0','去输出基线集合函数','g_0(S)=g(S)-b','Finset N→ℝ','全局','u(S)',[3,14],relation='centered_variant',empty='g0(∅)=0',baseline='减去输出标量b',lean=['Harsanyi.centered'])
symbol('interaction-raw','I_g','含空集基线的原始交互',r'I_g(S)=\sum_{T\subseteq S}(-1)^{|S|-|T|}g(T)','Finset N→ℝ','公共库','无独立原符号（经中心化映射）',[3],relation='derived_quantity',empty='I_g(∅)=b',lean=['Harsanyi.interaction'])
symbol('interaction-centered','I','中心化AND交互',r'I(S)=I_{g_0}(S)=\sum_{T\subseteq S}(-1)^{|S|-|T|}g_0(T)','Finset N→ℝ','全局；D.2记Iand','I(S), Iand(S)',[3,29],equations=['1','61'],empty='I(∅)=0；非空时I=I_g',lean=['Harsanyi.interaction (Harsanyi.centered g)'])
symbol('interaction-order','|S|','交互阶数',r'\operatorname{order}(S)=|S|','ℕ','全局','order(S), |S|',[5,16])
symbol('cutoff-order','M','非零交互/导数最高阶',r'I(S)=0\text{ for }|S|>M','ℕ；Lemma3有1≤M<n','3.2 / B.2–B.4','M',[5,17])
symbol('mask-order','m','保留变量的数量','m=|S|','0≤m≤n','平均输出 / 下界','m,m′',[6,7,16])
symbol('interaction-order-index','k','交互阶指标','k=|T|','1≤k≤M','A^(k)及组合矩阵','k',[7,16,17])
symbol('mean-output',r'\bar g_0^{(m)}','m阶平均掩码输出',r'\bar g_0^{(m)}=\binom nm^{-1}\sum_{S\subseteq N,|S|=m}g_0(S)','ℝ，0≤m≤n','3.2 / B.3',r'\bar u^{(m)}',[6,16,17],relation='renaming',empty='m=0时为0',lean=['SparseFull.meanOutput'])
symbol('robustness-exponent','p','平均输出稳健性指数',r'\bar g_0^{(m′)}\ge(m′/m)^p\bar g_0^{(m)}','正实数；0/0边界原文未定义','Assumption3 / Theorem2','p',[7,19],conflict='与Beta函数临时参数p是不同概念。')
symbol('order-total','A^{(k)}','k阶交互带符号总和',r'A^{(k)}=\sum_{S\subseteq N,|S|=k}I(S)','ℝ','3.2 / B.3–B.4','A^(k)',[7,16,20],lean=['SparseFull.orderTotal'])
symbol('cancellation-ratio',r'\eta^{(k)}','交互正负抵消后的比例',r'\eta^{(k)}=A^{(k)}/\sum_{|S|=k}|I(S)|','ℝ；分母0时数学比例未定义','3.2 / B.4','η^(k)',[7,8,20],empty='无k阶交互时分母可能为0',conflict='Theorem3所在Case1排除完全抵消；Case2不能统一用零除法。')
symbol('salient-count','R^{(k)}','显著k阶交互数',r'R^{(k)}=|\{S\subseteq N:|S|=k,|I(S)|\ge\tau\}|','ℕ','3.2 / B.4','R^(k)',[8,20],lean=['SparseFull.salientCount'])
symbol('salience-threshold',r'\tau','显著性强度阈值',r'\tau>0','正实数','3.2 / AppendixF','τ',[5,8,33],conflict='经验图使用严格>，定理计数使用≥；边界必须保留。')
symbol('normalized-interaction',r'\widetilde I','归一化交互',r'\widetilde I(S)=I(S)/\max_{S′}|I(S′)|','ℝ；最大值非零时','Figures3/10–13',r'\widetilde I(S)',[4,30],empty='若全零则分母0，原图规范未给该边界')
symbol('mean-strength',r'I_{\rm str}^{(m)}','每阶平均绝对强度',r'I_{\rm str}^{(m)}=\mathbb E_{|S|=m}|I(S)|','非负实数','Figures4/7–9','Istr^(m)',[6,30])
symbol('leading-coefficient',r'\lambda^{(k)}','各阶最高块归一化系数',r'|\lambda^{(k)}|\le1','ℝ','Theorem2','λ^(k)',[7,19,20])
symbol('leading-aggregate',r'\Lambda','m0处最高块的组合权重和',r'\Lambda=\sum_{k=1}^M\frac{\binom{m_0}k}{\binom nk}\lambda^{(k)}\ne0','ℝ','Theorem2','λ',[7,19,20],relation='renaming',conflict='原无上标λ与λ^(k)不同。')
symbol('growth-offset',r'\delta','最高n进制块的共同指数偏移',r'n^{p+\delta}\text{ 作为共同最高块尺度}','ℝ','Theorem2','δ,δ^(k)',[7,19,20],conflict='δ^(k)为临时每阶偏移，与共同δ另有最大值关系。')
symbol('nary-degree','q^{(k)}','第k阶n进制最高次数',r'A^{(k)}/\bar g_0^{(1)}=\sum_{i=0}^{q^{(k)}}a_i^{(k)}n^i','ℕ','Theorem2 proof','q^(k)',[19])
symbol('nary-digit','a_i^{(k)}','各阶n进制低位系数',r'|a_i^{(k)}|\in\{0,\ldots,n-1\}\ (i\ge1),\quad |a_0^{(k)}|<n','整数（i≥1）或实数（i=0）','Theorem2','a_i^(k)',[7,19])
symbol('nary-aggregate','a_i','m0处低位组合权重和',r'a_i=\sum_{k=1}^M\frac{\binom{m_0}k}{\binom nk}a_i^{(k)}','ℝ','Theorem2','a_i',[7,19,20])
symbol('witness-order','m_0','最高块组合非零的保留变量数',r'm_0\in\{n,n-1,\ldots,n-M\}','ℕ','Theorem2','m0',[7,18,20])
symbol('taylor-multiindex',r'\kappa','Taylor多重指标',r'\kappa=(\kappa_1,\ldots,\kappa_n),\quad |\kappa|=\sum_i\kappa_i','ℕⁿ','Taylor / Lemma1','κ',[5,15,16])
symbol('taylor-support-class','Q_S','恰以S为支撑的多重指标',r'Q_S=\{\kappa: i\in S\Rightarrow\kappa_i>0,\ i\notin S\Rightarrow\kappa_i=0\}','ℕⁿ子集','B.2','Q_S',[15,16],empty='Q_∅={0}，但作者候选I~(∅)单独定义0')
symbol('taylor-restricted-class','P_S','支撑包含于S的多重指标',r'P_S=\{\kappa:i\notin S\Rightarrow\kappa_i=0\}=\bigsqcup_{T\subseteq S}Q_T','ℕⁿ子集','B.2','P_S',[16],empty='P_∅={0}')
symbol('mixed-derivative',r'D^\kappa v(r)','在输入基线的混合导数',r'D^\kappa v(r)=\left.\frac{\partial^{|\kappa|}v}{\partial x_1^{\kappa_1}\cdots\partial x_n^{\kappa_n}}\right|_{x=r}','ℝ；需相应阶可微','B.2','∂^(κ1+…+κn)v / ∂x1^κ1…∂xn^κn |x=b',[5,15,16],relation='renaming')
symbol('marginal-difference',r'\Delta_T g_0(S)','T在环境S中的边际差分',r'\Delta_T g_0(S)=\sum_{L\subseteq T}(-1)^{|T|-|L|}g_0(L\cup S)','ℝ；T∩S=∅','B.5–B.7','∆u_T(S)',[21,23,25],relation='renaming',empty='T=∅时为g0(S)；S=∅时为I(T)')
symbol('shapley-value',r'\phi_i','变量i的Shapley值',r'\phi_i=\sum_{S\subseteq N\setminus\{i\}}\frac{|S|!(n-|S|-1)!}{n!}[g_0(S\cup\{i\})-g_0(S)]','ℝ；i∈N','Theorem4','ϕ(i)',[14,21,22])
symbol('shapley-interaction',r'\operatorname{SI}(T)','Shapley交互指标',r'\operatorname{SI}(T)=\sum_{S\subseteq N\setminus T}\frac{|S|!(n-|S|-|T|)!}{(n-|T|+1)!}\Delta_Tg_0(S)','ℝ','Theorem5','I^Shapley(T)',[14,23,24],empty='按本篇显示定义T=∅可计算，非通常只写非空指标的省略约定')
symbol('shapley-taylor',r'\operatorname{ST}_q(T)','q阶Shapley–Taylor指标',r'\operatorname{ST}_q(T)=\begin{cases}\Delta_Tg_0(\varnothing)&|T|<q\\\frac qn\sum_{S\subseteq N\setminus T}\binom{n-1}{|S|}^{-1}\Delta_Tg_0(S)&|T|=q\\0&|T|>q\end{cases}','ℝ；1≤q≤n','Theorem6','I^Shapley-Taylor(k)(T)',[14,25,26,27],relation='renaming',conflict='规范q用于最高阶；原k在本节与A^(k)的阶指标不同。')
symbol('beta-function',r'B_\mathrm{Beta}(a,c)','Beta函数临时工具',r'B(a,c)=\int_0^1t^{a-1}(1-t)^{c-1}\,dt','a,c>0','B.5–B.7证明工具','B(p,q)',[22,23,24,26,27],relation='conflict',conflict='正式p22写(1−x)^(1−q)，与后续阶乘式不一致；正确工具定义只用于已授权证明修复，原式保真。')
symbol('or-interaction',r'I_{\lor}','中心化OR交互',r'I_{\lor}(S)=-\sum_{T\subseteq S}(-1)^{|S|-|T|}g_0(N\setminus T)\ (S\ne\varnothing)','Finset N→ℝ','D.2','Ior(S)',[29],equations=['61'],empty='Ior(∅)=0，空集不套非空公式')
symbol('and-component',r'g_\land','AND输出分量',r'g_0(S)=g_\land(S)+g_\lor(S)','Finset N→ℝ','D.2','uand(S)',[29],relation='renaming',empty='gand(∅)=0')
symbol('or-component',r'g_\lor','OR输出分量',r'g_0(S)=g_\land(S)+g_\lor(S)','Finset N→ℝ','D.2','uor(S)',[29],relation='renaming',empty='gor(∅)=0')
symbol('decomposition-parameter',r'\gamma_S','AND–OR分解参数',r'g_\land(S)=0.5g_0(S)+\gamma_S','ℝ','D.2 optimizer','γS',[29],empty='γ∅=0由两分量空集0导出',conflict='原文未去噪句两次写uand；去噪gor同写+γ与分解和不符，作为证明/算法式问题记录。')
symbol('output-noise',r'\varepsilon_S','掩码输出噪声',r'g′(S)=g(S)+\varepsilon_S','ℝ或随机变量','3.3 / D.2','ϵS',[8,29],baseline='ε∅随中心化扣除，不应默认零')
symbol('noise-bound',r'\zeta','可学习噪声绝对界',r'|\varepsilon_S|\le\zeta=0.04|v(x)-v(x_\varnothing)|','非负实数','D.2','ζ',[29])
symbol('output-filter-threshold',r'\xi','样本分类置信筛选阈值',r'g_0(N)\ge\xi\text{ 才保留样本}','ℝ','D.1','ξ',[29],conflict='ξ与输入坐标xi不同。')
symbol('sample-count','t','每阶抽样掩码个数',r'\widehat {\bar g_0}^{(m)}=t^{-1}\sum_{j=1}^tg_0(S_j)','正整数','AppendixI','t',[34])

original_definitions={
 'model-output':r'v:\mathbb R^n\to\mathbb R', 'fixed-input':r'x=[x_1,\ldots,x_n]^\top',
 'input-baseline-vector':r'b=[b_1,\ldots,b_n]^\top', 'masked-input':r'(x_S)_i=x_i\ (i\in S),\quad (x_S)_i=b_i\ (i\notin S)',
 'masked-game':None,'output-baseline':r'v(x_\varnothing)', 'centered-game':r'u(S)=v(x_S)-v(x_\varnothing)',
 'interaction-raw':None,'interaction-centered':r'I(S)=\sum_{T\subseteq S}(-1)^{|S|-|T|}u(T)',
 'mean-output':r'\bar u^{(m)}=\mathbb E_{|S|=m}[u(S)]',
 'robustness-exponent':r'\bar u^{(m′)}\ge(m′/m)^p\bar u^{(m)},\quad p>0',
 'order-total':r'A^{(k)}=\sum_{S\subseteq N,|S|=k}I(S)',
 'leading-aggregate':r'\lambda=\sum_{k=1}^M\frac{\binom{m_0}k}{\binom nk}\lambda^{(k)}\ne0',
 'nary-degree':r'A^{(k)}/\bar u^{(1)}=a_{q^{(k)}}^{(k)}n^{q^{(k)}}+\cdots+a_0^{(k)}',
 'mixed-derivative':r'\left.\frac{\partial^{\kappa_1+\cdots+\kappa_n}v}{\partial x_1^{\kappa_1}\cdots\partial x_n^{\kappa_n}}\right|_{x=b}',
 'marginal-difference':r'\Delta u_T(S)=\sum_{L\subseteq T}(-1)^{|T|-|L|}u(L\cup S)',
 'shapley-value':r'\phi(i)=\mathbb E_m\mathbb E_{S\subseteq N\setminus\{i\},|S|=m}[u(S\cup\{i\})-u(S)]',
 'shapley-interaction':r'I^{\mathrm{Shapley}}(T)=\sum_{S\subseteq N\setminus T}\frac{|S|!(n-|S|-|T|)!}{(n-|T|+1)!}\Delta u_T(S)',
 'shapley-taylor':r'I^{\mathrm{Shapley\text{-}Taylor}(k)}(T)=\begin{cases}\Delta u_T(\varnothing)&|T|<k\\\frac kn\sum_{S\subseteq N\setminus T}\binom{n-1}{|S|}^{-1}\Delta u_T(S)&|T|=k\\0&|T|>k\end{cases}',
 'beta-function':r'B(p,q)=\int_0^1x^{p-1}(1-x)^{1-q}\,dx',
 'or-interaction':r'I_{or}(S)=-\sum_{T\subseteq S}(-1)^{|S|-|T|}u(N\setminus T),\quad S\ne\varnothing',
 'and-component':r'u(S)=u_{and}(S)+u_{or}(S)', 'or-component':r'u(S)=u_{and}(S)+u_{or}(S)',
 'decomposition-parameter':r'u_{and}(S)=0.5u(S)+\gamma_S,\quad u_{and}(S)=0.5u(S)-\gamma_S',
 'output-noise':r'v′(x_S)=v(x_S)+\varepsilon_S',
 'sample-count':r'\bar u^{(m)}\approx t^{-1}\sum_{i=1}^tu(S_i),\quad |S_i|=m',
 'output-filter-threshold':r'v(x)-v(x_\varnothing)<\xi\ \Rightarrow\ \text{discard }x'
}
canonical_ids={'model-output':'sym-model','fixed-input':'sym-input','input-baseline-vector':'sym-input-baseline',
 'masked-input':'sym-mask','variable-universe':'sym-universe','coalition':'sym-coalition','masked-game':'sym-game',
 'output-baseline':'sym-output-baseline','centered-game':'sym-centered-game','interaction-centered':'sym-centered-interaction','interaction-raw':'sym-and-interaction',
 'or-interaction':'sym-or-interaction','interaction-order':'sym-order','shapley-value':'sym-shapley'}
for s in symbols:
    if s['id'] in original_definitions:
        s['paper_mappings'][0]['original_definition_tex']=original_definitions[s['id']]
    s['paper_mappings'][0]['original_definition_status']='source_definition' if s['paper_mappings'][0]['original_definition_tex'] else 'project_derived_concept_no_separate_source_definition'
    s['canonical_id']=canonical_ids.get(s['id'],s['id'])
    s['lean_names']=[n.replace('SparseFull.meanOutput','Harsanyi.Sparsity.meanOutput').replace('SparseFull.orderTotal','Harsanyi.Sparsity.orderTotal') for n in s['lean_names'] if n not in ['SparseFull.maskedGame','SparseFull.salientCount']]
    actual_names={'model-output':[],'variable-universe':[],'masked-input':['Harsanyi.maskCoordinates'],
      'masked-game':['FullSparse.maskedGame'],'interaction-centered':['Harsanyi.interaction','Harsanyi.centered'],
      'mean-output':['Harsanyi.Sparsity.meanOutput'],'order-total':['Harsanyi.Sparsity.orderTotal']}
    if s['id'] in actual_names:s['lean_names']=actual_names[s['id']]
    s['lean_status']='actual_declaration_reference; source_semantic_mapping_reviewed_separately'
derivative_symbols=Path('research/full-proof-integration-20260930/cvpr2023/derivative-cutoff-results.json')
if derivative_symbols.exists():
    extras=json.loads(derivative_symbols.read_text())['symbols']
    symbols.extend(s for s in extras if s['id'] not in {x['id'] for x in symbols})
(BASE/'symbols.json').write_text(json.dumps({'schema_version':'symbol-table-1.0','paper_id':PAPER,'symbols':symbols},ensure_ascii=False,indent=2)+'\n')

issues=[]
def issue(key,title,pages,original,analysis,affected,kind='source_proof_error',impact='',evidence=None):
    issues.append({'id':'sparse-issue-'+key,'paper_id':PAPER,'title':title,'kind':kind,
      'source_refs':[{'source_id':'src-iclr2024-sparse-main','pdf_page':p,'image_path':str(BASE/'evidence/pages'/f'page-{p:02d}.png'),'text_path':str(BASE/'evidence/source-text'/f'p{p:02d}.txt')} for p in pages],
      'original_formula_tex':original,'analysis_md':analysis,'affected_result_ids':affected,
      'impact_scope':impact,'evidence_checked':evidence or 'formal PDF page text; image check recorded separately',
      'user_confirmation':'not_required_for_proof_repair_under_latest_instruction','fix_authorization':'proof_only_granted',
      'statement_change_authorization':'not_granted','statement_status':'not_declared_false' if kind=='source_proof_error' else 'requires_assessment',
      'resolution_status':'recorded_repair_in_progress' if kind=='source_proof_error' else 'separate_original_statement_review'})

issue('determinant-sign','Lemma3行列式消元漏余子式符号',[18],r'D\prod_{k=1}^M\binom nk=1,\quad D=(\prod_{k=1}^M\binom nk)^{-1}',
      '取n=3,M=2，Eq31的矩阵为[[1,2],[1,1]]，行列式−1。Eq32沿首列展开漏(−1)^(M+1)，重复后应有(−1)^(M(M−1)/2)。这只改变非零行列式的符号，不推翻满列秩命题。',
      ['iclr2024-sparse-lemma3'],impact='Eq33–36的精确值；Lemma3最终零空间结论保持，已授权修中间证明。',evidence='p18 PNG visually checked, exact 2×2 determinant countercheck')
issue('beta-exponent','Beta定义指数方向与后续值不一致',[22],r'B(p,q)=\int_0^1x^{p-1}(1-x)^{1-q}\,dx',
      '正式图像确写1−q。取p=1,q=2，右侧为发散积分；随后给B(1,2)=1/2。修证明可用有限组合计数，不改Shapley/SII/STI命题。',
      ['iclr2024-sparse-theorem4','iclr2024-sparse-theorem5','iclr2024-sparse-theorem6'],impact='证明工具定义及后续积分路线；非三个最终指标恒等式的反例。',evidence='p22 PNG visually checked; same error occurs in formal CVPR supplement p7')
issue('beta-empty-L','Shapley等证明的L=∅零参数边界未处理',[22,23,24,26,27],r'B(n-|L|-k,|L|+k),\qquad |L|\int_0^1(1-x)^{|L|-1}\,dx=1',
      '允许L=∅且k=0时调用B(n,0)，违反刚声明的正参数域。|L|=0时标①的被积函数在(0,1)为0，不能统一写成1；原离散权重项本身有限，需独立处理边界。',
      ['iclr2024-sparse-theorem4','iclr2024-sparse-theorem5','iclr2024-sparse-theorem6'],impact='权重化简路线的空集分支；最终公式可以不改，使用共享修复证明。',evidence='p22 visually checked plus p23/24/26/27 full formal text')
issue('taylor-validity','Lemma1的一般无限Taylor恒等式缺少有效性前提',[5,15,16],r'v(x_S)=\sum_{\kappa\in\mathbb N^n}\frac{D^\kappa v(b)}{\kappa!}(x_S-b)^\kappa',
      '原文仅说适用于continuously differentiable functions，Lemma1本身未假设解析性或Taylor级数等于函数。n=1,b=0,x=1，取v(t)=exp(−1/t²)（t≠0），v(0)=0。此函数C∞，所有在0的导数为0，但I({1})=e^(−1)≠0，而Eq8右边为0。反例针对一般Lemma1，不满足全空间高阶导数为零，故不直接否定1β⇒1α。',
      ['iclr2024-sparse-lemma1'],kind='source_statement_counterexample',impact='一般Lemma1与无限展开Eq2/11不能无条件修复；不能补解析性后冒充原命题。')
issue('zero-power','Lemma1掩码幂式漏κ_i>0条件',[16],r'\forall i\notin S,\ [(x_S)_i-b_i]^{\kappa_i}=0',
      'κ_i=0时该式为0^0=1（Taylor单项式约定），不是0。后续PS过滤实际只需“若κ_i>0则项为零”，可修证明中间解释；不改PS或最终目标。',
      ['iclr2024-sparse-lemma1'],impact='p16关于零项的单句；与一般Taylor有效性缺口是两个独立问题。')
issue('theorem2-zero-output','Theorem2原路线未处理ū(1)=0',[19],r'A^{(k)}/\bar u^{(1)}',
      '取所有掩码u(S)=0，三条假设均满足，但Eq41除以0。此反例只否定原证明步骤：最终等式乘ū(1)=0仍可成立，不能据此宣布Theorem2是假。修路线应处理全零分支，不能增添ū(1)>0假设。',
      ['iclr2024-sparse-theorem2'],impact='n进制构造步骤；正确的零平均分支已在项目重写中完整补齐；不从均值零推逐点输出零。',evidence='p19 PNG visually checked')
issue('theorem2-empty-G','Theorem2原构造G可为空',[19,20],r'G=\{k:1\le k\le M,q^{(k)}\ge\lfloor p\rfloor\},\quad\delta=\max_{k\in G}\delta^{(k)}',
      'n=3,M=1,p=2，u(S)=|S|满足三假设，ū(1)=1,A(1)=3，n进制最高次数q(1)=1≤floor(p)−1，故G为空。原最大值与k*不存在；Lemma3不能制造原构造全零λ以外的λ。最终存在式或有另一构造，此为路线缺口而非最终结论反例。',
      ['iclr2024-sparse-theorem2'],impact='δ,k*构造及Eq50调用；不能仅补G非空。')
issue('theorem2-m0-range','Theorem2调用Lemma2的m范围不足',[20],r'm_0\in\{n,n-1,\ldots,n-M\},\qquad (40)\text{ only for }M\le m\le n',
      '当M<n<2M时n−M<M，Lemma3取得的非零行可能不在Eq40已陈述范围。平均公式本身可对所有m扩展（k>m的组合数为0），属于证明补全而非新增数学假设。',
      ['iclr2024-sparse-theorem2'],impact='Eq51的前提引用。')
issue('theorem2-p-under-one','p∈(0,1)时低位下标书写未定义',[7,19],r'a_{\lfloor p\rfloor-1}^{(k)}n^{\lfloor p\rfloor-1}+\cdots+a_0^{(k)}',
      'p>0允许p<1；floor(p)−1=−1，而正文只定义非负进制位、常数位。作者实验包含约0.9值，不能擅补p≥1。规范求和读作有限族J={i∈ℕ:i<floor(p)}时该族为空；若继续保留额外显示的a0项，全部低位取0的同一见证也成立。项目给任意有限低位族的统一构造，覆盖这两种常规读法，无须添加p≥1。原省略号书写问题仍保留，不声称原式逐字定义了负指标。',
      ['iclr2024-sparse-theorem2','iclr2024-sparse-theorem3'],kind='statement_notation_scope_issue',impact='原定理的索引族须明确，保留原式。')
issue('eta-zero','完全抵消与空阶下η除法边界',[7,8,20,21],r'\eta^{(k)}=A^{(k)}/\sum_{|S|=k}|I(S)|,\quad A^{(k)}/\eta^{(k)}=\sum_{|S|=k}|I(S)|',
      '无交互时定义为0/0；非零正负交互恰好抵消时η=0，Eq57除法亦未定义。Theorem3所在Case1明确|η|≫1/n，已提供非零上下文，可以在该原范围忠实证明；不能扩大为完全抵消情况。',
      ['iclr2024-sparse-theorem3'],impact='完全抵消情况不在可用除法范围；Case1计数推导无须增假设。')
issue('noise-variance','fully random不足以推出2^|S|方差放大',[8],r'\operatorname{Var}(I_\varepsilon(S))=2^{|S|}\operatorname{Var}(\varepsilon)',
      '原文未说明噪声项相互独立且同方差。令所有εT同一个非退化随机Z，中心化后εT−ε∅=0，所有噪声交互为0；该方差放大式不成立。若fully random意为iid需明确语义，不能自行给独立同方差假设。空集交互恒0也不是1倍原噪声方差。',
      ['iclr2024-sparse-noise-variance'],kind='source_statement_assumption_gap',impact='噪声线性分解成立；概率结论另列，不公开增条件版本。')
issue('parity-empty','奇偶例的u(∅)与中心化冲突',[9],r'u(S)=\begin{cases}+1&|S|\text{ odd}\\-1&|S|\text{ even}\end{cases}',
      '空集偶数，所以该显示定义给u(∅)=−1，而本篇全局定义给u(∅)=0。原示例在当前定义域中不存在。不能把u改成g或改空集值后宣称原例证明完成；原符号语义冲突单列。',
      ['iclr2024-sparse-parity-mask'],kind='source_statement_definition_conflict',impact='正文Scenario2示例；不涉及Assumption2作为条件的其他证明。')
issue('transfer','单样本稀疏与重构不能推出样本间迁移',[9],r'\text{sparsity} + \text{universal matching}\Rightarrow\text{sample-wise transferability}',
      '令总体N有n≥2变量，n个样本分别诱导g0^(j)(S)=1若j∈S，反之0。每个样本仅一个非零单变量交互，全部掩码都精确重构；不同样本的显著支撑互不相交。这些集合函数可由同一模型在不同掩码样本上实现（例如各样本仅一个坐标非零、v(z)=sum_i z_i），所有样本输出为1，可按分类阈值v(z)>1/2全部指定为同一正类，满足原“same category”条件。无需“爆炸”模式数。原反证没有全模型模式预算前提。',
      ['iclr2024-sparse-transfer-inference'],kind='source_statement_counterexample',impact='Section4迁移推断不是两已知性质的逻辑推论，单独列出。')
issue('decomposition-notation','D.2两个分量名称及去噪γ符号不一致',[29],r'u_{and}=0.5u+\gamma,\quad u_{and}=0.5u-\gamma;\qquad u_{and}=0.5(u-\varepsilon)+\gamma,\quad u_{or}=0.5(u-\varepsilon)+\gamma',
      '正式原式第二分量同名uand，去噪两项加γ使和为u−ε+2γ而非去噪输出。属于算法/证明中间式的标记与符号错；在原最终分解u=uand+uor保持不变下可标注并修中间式。',
      ['iclr2024-sparse-and-or-optimization'],impact='D.2分解参数式；Eq61/62的数学目标本身未因此被推翻。')
issue('asymptotic-sparsity','Case2非指数小抵消比例不足以推出同阶稀疏',[7,8],r'\text{Case2: }|\eta^{(k)}|\text{ not exponentially small}\ \Longrightarrow\ R^{(k)}\text{ still much less than }\binom nk',
      '完整无限族反例已写于math/rewrites.zh.md的asymptotic-claim。取n≥3且n≡2/3 mod4，q=choose(n,2)奇数；二阶±1系数的正/负项数为(q−1)/2与(q+1)/2，总和−1。模型v=Σzi+Σc_A∏i∈A zi，输入全1、基线0，给A1=n,A2=−1，所有高于二阶交互和混合偏导为零。μm=m−choose(m,2)/q；μm+1−μm=1−m/q>0，μm/m=1−(m−1)/(2q)非增，故原三条件以M=2,p=1完整满足。固定τ=1/100得到R2=q、η2=−1/q，其仅多项式小却二阶全显著。T3右端100q仍有效。反例只否定第8页Case2额外同阶推断，不把邻近mostcases经验描述当全称命题，也不否定总O(n²)相对2^n仍稀疏。',
      ['iclr2024-sparse-asymptotic-claim'],kind='source_statement_counterexample',impact='Only p8 Case2 non-exponentially-small η ⇒ per-order R≪choose(n,k) inference; exact T2/T3 and neighboring empirical most-cases claim unchanged.',evidence='formal p8 source and PNG independently checked by CVPR agent/root; complete original-assumption counterexample independently recalculated')
issues[-1]['statement_status']='specific_case2_per_order_inference_refuted; adjacent_mostcases_not_refuted; exact_T2_T3_unchanged'
issues[-1]['assessment_status']='specific_original_clause_refuted_by_complete_infinite_family'
issues[-1]['resolution_status']='original_clause_preserved_and_counterexample_separately_proved'
issues[-1]['proof_path']=str(BASE/'math/rewrites.zh.md')
issues[-1]['scope_notes_md']='此外，有限n的O(n^(p+δ)/|τη|)表达若未控制δ、阈值及抵消比例随n的变化，不自动成为统一渐近界；这一范围说明保留。Case1相邻mostcases经验描述不被当成全称命题反驳。'

issue('example-H-arithmetic','Appendix H三阶表漏x3单变量项',[34],r'u(\{3,4,5\})=0,\qquad\bar u^{(3)}=1.8',
      '正式图像确给0，但代入v=x1x2x3+x1x2+x2x3+x2+x3、x=(1,1,1,1,1)、基线0，{3,4,5}保留x3=1，所以输出为1。三阶10项和应19、平均1.9。原二阶平均1≤三阶平均的结论仍成立；仅修算例表项和派生均值。',
      ['iclr2024-sparse-monotonicity-example'],impact='一个中间表项与均值1.8；不否定原单调示例结论。',evidence='p34 PNG visually checked; independently detected by root and confirmed locally')


issue('reconstruction-index','Theorem1换序后的第三行误用S⊇L',[15],r'\sum_{\substack{T\subseteq S:S\supseteq L\\|T|=t}}(-1)^{t-|L|}u(L)',
      '上一行要求T⊇L；第三行写成S⊇L不能筛选该L对应的T，导致计数不再是choose(|S|−|L|,t−|L|)。这是证明中间索引排印错；恢复上一行的T⊇L或用完整子集双射可证明相同原重构命题。',
      ['iclr2024-sparse-reconstruction'],impact='B.1证明第三个等式中的求和限制；最终定理保持不变。',evidence='p15 PNG visually checked')
issue('marginal-free-L','Lemma4按l分组后仍保留未绑定L',[21],r'\sum_{l=|K\setminus S|}^{|T|}(-1)^{|T|-|L|}\binom{|T|-|K\setminus S|}{l-|K\setminus S|}',
      '按基数l分组后L已经不是求和变量，指数应随l变化才能调用二项式抵消。保留原自由L式供核查，项目共享有限差分证明不使用该错误中间式；原引理目标和全部T/S边界不变。',
      ['iclr2024-sparse-lemma4'],impact='B.5分组求和的一行；不影响修复后的原边际命题。',evidence='p21 PNG visually checked')
issue('STI-free-S','Theorem6临界阶换序后组合数误留自由S',[26],r'\sum_{L\subseteq N\setminus T}I(T\cup L)\sum_{q=0}^{n-t}\frac{\binom{n-t-|L|}{q-|L|}}{\binom{n-1}{|S|}}',
      '外层原环境S在换序后已按q=|S|分组，分母仍出现自由S；下一段转积分要求分母为choose(n−1,q)。这是局部索引排印错误，修复的共享有限阶乘卷积证明直接得到原临界阶权重，保留三分支命题。',
      ['iclr2024-sparse-theorem6'],impact='B.7临界阶权重换序行；原STI最终展开保持不变。',evidence='p26 PNG visually checked')


issue('T2-parameter-domain','T2参数域未在陈述中明确',[5,7,17,18,19],r'\lambda=\sum_{k=1}^M\frac{\binom{m_0}k}{\binom nk}\lambda^{(k)}\ne0,\qquad\log_n(\cdot)',
      'T2正文/附录没有明确重复Lemma3的M<n；不能把该限制偷偷加到T2。新构造覆盖M=n。实数log_n和n进制在n>1，全部choose(n,k)分母非零在M≤n；这是原表达的定义域说明。原页面未找到明确M∈N+约定：若允许M=0，取n=3且所有中心化输出0，三假设均成立，λ的空和为0，与λ≠0矛盾；因此这一读法的原陈述有反例，单列，不补M>0后冒充无条件原命题。正阶定义域中的完整存在构造另可验证。',
      ['iclr2024-sparse-theorem2','iclr2024-sparse-theorem3'],kind='statement_parameter_domain_gap',impact='缺失的参数作用域与零阶读法；正常正阶范围原系数目标不改。',evidence='formal p5/7/17/18/19 text and formula boundaries reviewed')


issue('lemma3-copied-row','Lemma3 Eq33的降阶矩阵一行复制了n−2',[18],r'\left[\binom{n-3}0,\binom{n-2}1,\ldots,\binom{n-2}{M-2}\right]',
      '正式Eq33第二行除第一列外仍印n−2，与Eq32相邻行差分后第二行应来自n−3不一致。原数组在完整TeX中保留；正确消元或已完成的有限差分归纳可证明原零空间结论，不需沿错误矩阵再计算。该索引复制错与余子式符号漏项分别标记。',
      ['iclr2024-sparse-lemma3'],impact='Eq33降阶矩阵的第二行；不改变Lemma3正确最终结论。',evidence='p18 PNG visually checked')

for i in issues:
    if i['kind']=='source_proof_error' and i['id'] not in ['sparse-issue-zero-power']:
        i['resolution_status']='proof_repaired_same_original_statement_in_project_layer'
(BASE/'issues.json').write_text(json.dumps({'schema_version':'source-issues-1.0','paper_id':PAPER,'authorization':'latest user grants proof-only repair; original statements/assumptions cannot be changed','issues':issues},ensure_ascii=False,indent=2)+'\n')
lines=['# ICLR 2024 Sparse：原式问题与影响范围','','最新用户允许“直接修正原文错误证明，标注错误地方；不能修正命题，命题错单独列出”。本报告严格区分证明错误与原陈述反例；仅证明修复授权为 `proof_only_granted`，原命题修改未授权。','']
for i in issues:
    lines += ['## '+i['title'],'',f"ID：`{i['id']}`；类别：`{i['kind']}`；正式 PDF 页："+', '.join(str(r['pdf_page']) for r in i['source_refs'])+'。','',r'\['+i['original_formula_tex']+r'\]','',i['analysis_md'],'', '**影响范围：** '+i['impact_scope'],'']
(BASE/'issues.md').write_text('\n'.join(lines)+'\n')
print(f'{len(symbols)} symbols; {len(issues)} source issues')
