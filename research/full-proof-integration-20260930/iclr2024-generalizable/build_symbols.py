#!/usr/bin/env python3
"""Source-grounded symbols; a new notation never changes an original assertion."""
import json
from pathlib import Path
P=Path(__file__).resolve().parent
PAPER='iclr2024-generalizable';SOURCE='src-iclr2024-generalizable-main'
symbols=[]
def add(id,tex,name,definition,domain,scope,original,origdef,pages,relation='renaming',note='',empty='',baseline='',equations=()):
 symbols.append(dict(id=id,canonical_id=id,canonical_tex=tex,name_zh=name,definition_tex=definition,
  description_md=note or name,type_or_domain=domain,scope=scope,assumptions=[],empty_set_convention=empty,baseline_convention=baseline,
  aliases=[original],paper_mappings=[dict(paper_id=PAPER,source_id=SOURCE,version_id='ver-iclr2024-generalizable-formal',
  original_tex=original,original_definition_tex=origdef,pdf_pages=pages,equation_labels=list(equations),canonical_concept_id=id,
  relation_type=relation,conflict_note=note if relation in ('conflict','pending_alignment') else '')],
  lean_names=[],lean_status='not_claimed_available',version='1.0'))
add('sym-model',r'v','模型标量输出',r'v:X\to\mathbb R','X→ℝ','固定模型',r'v',r'v:\mathbb R^n\to\mathbb R',[2,7,20], 'same_definition',note='正文以标量坐标举例；附录L每个变量可为向量嵌入，两个模型的输入域不同。')
add('sym-input',r'x','固定输入',r'x\in X','X','某模型与某样本',r'\boldsymbol x',r'\boldsymbol x=[x_1,\ldots,x_n]^\top',[2,20])
add('sym-input-coordinate',r'x_i','输入变量/嵌入',r'x_i\in X_i','X_i','某样本第i变量',r'x_i',r'x_i\in\mathbb R;\quad x_i\in\mathbb R^{768}\ \text{or}\ \mathbb R^{1024}\text{ in L}',[2,20],note='正文实数坐标与附录token嵌入的域分开；同token不要求两模型向量相等。')
add('sym-input-baseline',r'r','输入基线向量',r'r=(r_i)_{i\in N}\in X','X','固定模型的掩码规则',r'b_i',r'x_i=b_i\text{ denotes the masked state}',[3,20],'renaming',note='原文bi是输入基线；规范b是输出基线标量，不能混用。',baseline='同一固定r用于所有掩码；未选择的背景保持原输入。')
add('sym-universe',r'N','选定输入变量总体',r'N=\{1,\ldots,n\}','有限集合','当前选定变量',r'N',r'N=\{1,2,\ldots,n\};\quad N=\{1,\ldots,t\}\ (t<n)\text{ in E}',[2,15,23],'same_definition',note='附录E的t是选定变量数，总样本变量数n可更大；全部掩码只针对选定N。')
add('sym-variable-count',r'n','当前掩码总体大小',r'n=|N|','自然数','某次交互提取',r'n,t',r'n\text{ input variables};\quad t<n\text{ selected in E}',[2,15,20,23])
add('sym-coalition',r'S,T,L','变量子集',r'S,T,L\subseteq N','2^N','各求和式的绑定范围',r'S,T,L',r'S,T,L\subseteq N',[2,3,12,13,14],'same_definition',empty='包含空集；OR非空求和与OR空集约定分别写。')
add('sym-mask',r'x_S','保留S的掩码输入',r'(x_S)_i=\begin{cases}x_i&i\in S,\\r_i&i\notin S\end{cases}','X','固定x,r,N',r'\boldsymbol x_S',r'x_S:\text{ variables in }N\setminus S\text{ masked by baseline}',[2,3,20],'same_definition',empty=r'x_\varnothing=r（所选变量全掩码；固定背景不变）。',baseline='同一输入基线；重复掩码按集合交合成。')
add('sym-game',r'g','固定掩码集合函数',r'g(S)=v(x_S)','2^N→ℝ','固定v,x,r,N',r'v(x_S)',r'v(x_S)\in\mathbb R',[2,3,20],'derived_quantity',baseline='不默认g(∅)=0。')
add('sym-output-baseline',r'b','输出基线标量',r'b=v(x_\varnothing)=g(\varnothing)','ℝ','固定模型与样本',r'v(x_\varnothing)',r'I_{\mathrm{and}}(\varnothing\mid x)=v(x_\varnothing)',[2,3],'derived_quantity',empty='空集AND/OR系数为各自分量的输出基线。',baseline='b不是原文输入基线bi。')
add('sym-centered-game',r'g_0','规范去输出基线函数',r'g_0(S)=g(S)-b','2^N→ℝ','跨论文对照；本篇公式未先中心化',r'v(x_S)-v(x_\varnothing)',r'v(x)-v(x_\varnothing)\text{ appears in thresholds}',[6,7],'centered_variant',empty=r'g_0(\varnothing)=0',note='规范对照量；不把本篇原始Iand偷换成中心化定义。')
add('sym-and-output',r'g_{\mathrm{and}}','AND分量的集合函数',r'g_{\mathrm{and}}(S)=v_{\mathrm{and}}(x_S)','2^N→ℝ','固定分解',r'v_{\mathrm{and}}(x_S)',r'v(x_S)=v_{\mathrm{and}}(x_S)+v_{\mathrm{or}}(x_S)',[3,4,6,12],'derived_quantity',baseline='各分量空集值不默认0。')
add('sym-or-output',r'g_{\mathrm{or}}','OR分量的集合函数',r'g_{\mathrm{or}}(S)=v_{\mathrm{or}}(x_S)','2^N→ℝ','固定分解',r'v_{\mathrm{or}}(x_S)',r'v(x_S)=v_{\mathrm{and}}(x_S)+v_{\mathrm{or}}(x_S)',[3,4,6,13],'derived_quantity')
add('sym-and-interaction',r'I_{\mathrm{and}}(S\mid x)','AND/Harsanyi交互',r'I_g(S)=\sum_{L\subseteq S}(-1)^{|S|-|L|}g(L)','ℝ','固定原样本；分量用途分别标注',r'I_{\mathrm{and}}(S\mid x)',r'I_{\mathrm{and}}(S\mid x)=\sum_{L\subseteq S}(-1)^{|S|-|L|}v(x_L)',[2,12],'same_definition',empty=r'I_g(\varnothing)=g(\varnothing)',equations=['1','8'])
symbols[-1]['paper_mappings'][0]['pdf_pages']=[2]
symbols[-1]['scope']='Section2.1整体模型；固定原样本x'
add('sym-and-component-interaction',r'I_{g_{\mathrm{and}}}(S)','AND分量的Harsanyi交互',r'I_{g_{\mathrm{and}}}(S)=\sum_{L\subseteq S}(-1)^{|S|-|L|}v_{\mathrm{and}}(x_L)','ℝ','AppendixC(1)固定分量',r'I_{\mathrm{and}}(S\mid x)',r'I_{\mathrm{and}}(S\mid x)=\sum_{L\subseteq S}(-1)^{|S|-|L|}v_{\mathrm{and}}(x_L)',[12,13],'same_definition',empty=r'I_{g_{\mathrm{and}}}(\varnothing)=v_{\mathrm{and}}(x_\varnothing)',equations=['8'])
symbols[-1]['parent_concept_id']='sym-mobius-transform'
add('sym-or-interaction',r'I_{\mathrm{or}}(S\mid x)','OR交互',r'I_{\mathrm{or}}(S\mid x)=-\sum_{L\subseteq S}(-1)^{|S|-|L|}g(N\setminus L)\quad(S\ne\varnothing)','ℝ','有限总体N与固定输入',r'I_{\mathrm{or}}(S\mid x)',r'I_{\mathrm{or}}(S\mid x)=-\sum_{L\subseteq S}(-1)^{|S|-|L|}v(x_{N\setminus L})',[3,13],'same_definition',empty=r'I_{\mathrm{or}}(\varnothing\mid x)=g(\varnothing)\text{ separately defined}',equations=['2','9'])
symbols[-1]['paper_mappings'][0]['pdf_pages']=[3]
symbols[-1]['scope']='Section2.1整体模型的OR变换'
add('sym-or-component-interaction',r'O_{g_{\mathrm{or}}}(S)','OR分量交互',r'O_{g_{\mathrm{or}}}(S)=-\sum_{L\subseteq S}(-1)^{|S|-|L|}g_{\mathrm{or}}(N\setminus L)\quad(S\ne\varnothing)','ℝ','AppendixC(2)固定OR分量',r'I_{\mathrm{or}}(S\mid x)',r'I_{\mathrm{or}}(S\mid x)=-\sum_{L\subseteq S}(-1)^{|S|-|L|}v_{\mathrm{or}}(x_{N\setminus L})',[13,14],'same_definition',empty=r'O_{g_{\mathrm{or}}}(\varnothing)=v_{\mathrm{or}}(x_\varnothing)',equations=['9'])
add('sym-conditional-interaction',r'I(S\mid x_T)','再次掩码后输入上的交互',r'g_T(L)=v((x_T)_L)','ℝ','Theorem2/Eq3,7–9',r'I_{\mathrm{and/or}}(S\mid x_T)',r'\text{Theorem2 conditions on }x_T;\ \text{Appendix definitions use fixed }x',[3,12,13,14],'pending_alignment',note='须显式验证固定基线掩码合成后对原字面式证明；不能直接字符串改为固定x。')
symbols[-1]['empty_set_convention']=r'I_{g_{\mathrm{and},T}}(\varnothing)=v_{\mathrm{and}}((x_T)_\varnothing)；OR空集值亦按分量定义单列。'
add('sym-order',r'|S|','交互阶数',r'\operatorname{order}(S)=|S|','自然数','交互S',r'\operatorname{order}(S)',r'\operatorname{order}(S)=|S|',[5,7],'same_definition')
add('sym-threshold',r'\tau','显著性阈值',r'\Omega=\{S\subseteq N:|I(S\mid x)|>\tau\}','ℝ','某模型/交互类型',r'\tau,\tau^{(i)}',r'\Omega^{\mathrm{and/or},(i)}=\{S\subseteq N:|I^{(i)}_{\mathrm{and/or}}(S\mid x)|>\tau^{(i)}\}',[3,4,21],'same_definition')
add('sym-significant-set',r'\Omega','显著交互集合',r'\Omega=\{S\subseteq N:|I(S\mid x)|>\tau\}','有限子集族','固定阈值/模型/类型',r'\Omega,\Omega^{\mathrm{and},(i)},\Omega^{\mathrm{or},(i)}',r'\Omega=\{S\subseteq N:|I(S\mid x)|>\tau\}',[3,4,21],'same_definition')
add('sym-model-count',r'm','模型数',r'i\in\{1,\ldots,m\}','正整数','多模型优化与Definition1',r'm',r'v^{(1)},\ldots,v^{(m)}',[4,6],'same_definition',note='与附录M匹配精度指标m同字母、不同概念。')
add('sym-shared-interactions',r'\Omega_{\mathrm{shared}}','各模型共同显著交互',r'\Omega^{\mathrm{and/or}}_{\mathrm{shared}}=\bigcap_{i=1}^m\Omega^{\mathrm{and/or},(i)}','有限子集族','同一语义变量总体的m个模型',r'\Omega^{\mathrm{and/or}}_{\mathrm{shared}}',r'\Omega^{\mathrm{and/or}}_{\mathrm{shared}}=\bigcap_{i=1}^m\Omega^{\mathrm{and/or},(i)}',[4],'same_definition')
add('sym-transferability',r's^{(i)}_{\mathrm{and/or}}','迁移率',r's^{(i)}_{\mathrm{and/or}}=\frac{|\Omega^{\mathrm{and/or}}_{\mathrm{shared}}|}{|\Omega^{\mathrm{and/or},(i)}|}','ℝ；原分母须非零','Definition1某模型/类型',r's^{(i)}_{\mathrm{and/or}}',r's^{(i)}_{\mathrm{and/or}}=|\Omega^{\mathrm{and/or}}_{\mathrm{shared}}|/|\Omega^{\mathrm{and/or},(i)}|',[4,8],'same_definition',note='原文未指定空显著集合的比率约定。')
add('sym-decomposition-parameter',r'\gamma_T^{(i)}','分解参数',r'v_{\mathrm{and/or}}^{(i)}(x_T)=\tfrac12v^{(i)}(x_T)\pm\gamma_T^{(i)}','ℝ','模型i与掩码T',r'\gamma_T^{(i)}',r'v_{\mathrm{and}}^{(i)}(x_T)=0.5v^{(i)}(x_T)+\gamma_T^{(i)},\quad v_{\mathrm{or}}^{(i)}(x_T)=0.5v^{(i)}(x_T)-\gamma_T^{(i)}',[4,6,20],'same_definition')
add('sym-common-gamma',r'\bar\gamma_T','共享分解参数',r'\gamma_T^{(i)}=\bar\gamma_T+\hat\gamma_T^{(i)}','ℝ','跨模型优化',r'\bar\gamma_T',r'\gamma_T^{(i)}=\bar\gamma_T+\hat\gamma_T^{(i)}',[6],'same_definition')
add('sym-individual-gamma',r'\hat\gamma_T^{(i)}','模型特定分解参数',r'\gamma_T^{(i)}=\bar\gamma_T+\hat\gamma_T^{(i)}','ℝ','模型i',r'\hat\gamma_T^{(i)}',r'|\hat\gamma_T^{(i)}|<\tau_\gamma^{(i)}',[6],'same_definition',note='严格<约束与原剪裁产生等于阈值的边界分别保留。')
add('sym-gamma-threshold',r'\tau_\gamma^{(i)}','分解差异阈值',r'\tau_\gamma^{(i)}=0.5\mathbb E_x|v^{(i)}(x)-v^{(i)}(x_\varnothing)|','非负实数','模型i与数据分布',r'\tau_\gamma^{(i)}',r'\tau_\gamma^{(i)}=0.5\mathbb E_x[|v^{(i)}(x)-v^{(i)}(x_\varnothing)|]',[6],'same_definition')
add('sym-interaction-matrix',r'\mathbf I_{\mathrm{and/or}}','交互矩阵',r'\mathbf I_{\mathrm{and/or}}\in\mathbb R^{2^n\times m}','2^n×m实矩阵','按子集行、模型列',r'I_{\mathrm{and/or}}',r'I_{\mathrm{and/or}}=[I_{\mathrm{and/or}}^{(1)},\ldots,I_{\mathrm{and/or}}^{(m)}]',[5,6,16],'same_definition',empty='原矩阵列出全部2^n项，包括空集。')
add('sym-rowmax',r'\operatorname{rowmax}','每行最大绝对强度',r'\operatorname{rowmax}(A)_k=\|A[k,:]\|_\infty=\max_i|A_{ki}|','实矩阵→非负向量','Eq5,6定义',r'\operatorname{rowmax}',r'\operatorname{rowmax}(I_{\mathrm{and}})=[\|I_{\mathrm{and}}[1,:]\|_\infty,\ldots,\|I_{\mathrm{and}}[2^n,:]\|_\infty]^\top',[6,16],'conflict',note='p16 Eq10的|max(a,b)|不等于p6定义max(|a|,|b|)，原等价式有反例。')
add('sym-entrywise-l1',r'\|A\|_1','向量/矩阵元素绝对值和',r'\|A\|_1=\sum_{k,i}|A_{ki}|','非负实数','Eq4–6',r'\|\cdot\|_1',r'\text{sum of absolute values of all vector/matrix elements}',[5,6],'same_definition',note='这里不是矩阵诱导1范数。')
add('sym-redundancy-weight',r'\alpha','冗余惩罚权重',r'\alpha\in[0,1]','实数','Eq6和AppendixI',r'\alpha',r'\alpha\in[0,1]',[6,18],'same_definition')
add('sym-gaussian-noise',r'\epsilon_L^{(i)}','IID随机输出噪声',r'\epsilon_L^{(i)}\sim\mathcal N(0,\sigma^2)','概率空间→ℝ','固定模型/样本；随机性来自输出噪声',r'\epsilon_T^{(i)}',r'\epsilon_T^{(i)}\sim\mathcal N(0,\sigma^2)\text{ IID over }T',[7,15],'same_definition',note='与同页可学习确定误差epsilon分开；方差对噪声分布而非输入样本。')
add('sym-noise-variance',r'\sigma^2','单个输出噪声方差',r'\operatorname{Var}(\epsilon_L^{(i)})=\sigma^2','非负实数','AppendixD IID模型',r'\sigma^2',r'\epsilon_T^{(i)}\sim\mathcal N(0,\sigma^2)',[7,15],'same_definition')
add('sym-learned-error',r'\eta_T^{(i)}','可学习确定输出误差',r'v^{(i)}(x_T)=v_{\mathrm{and}}^{(i)}(x_T)+v_{\mathrm{or}}^{(i)}(x_T)+\eta_T^{(i)}','ℝ','鲁棒优化参数',r'\epsilon_T^{(i)}',r'v^{(i)}(x_T)=v_{\mathrm{and}}^{(i)}(x_T)+v_{\mathrm{or}}^{(i)}(x_T)+\epsilon_T^{(i)}',[7],'renaming',note='原文复用epsilon字母；此参数不声明服从IID高斯。')
add('sym-error-threshold',r'\tau_\epsilon^{(i)}','学习误差阈值',r'\tau_\epsilon^{(i)}=0.02|v^{(i)}(x)-v^{(i)}(x_\varnothing)|','非负实数','模型i/样本x',r'\tau_\epsilon^{(i)}',r'\tau_\epsilon^{(i)}=0.02|v^{(i)}(x)-v^{(i)}(x_\varnothing)|',[7],'same_definition')
add('sym-shapley',r'\phi(i)','Shapley值',r'\phi(i)=\sum_{S\subseteq N:i\in S}\frac{I_{\mathrm{and}}(S\mid x)}{|S|}','ℝ','Theorem3/固定整体模型g',r'\phi(i)',r'\phi(i)=\sum_{S\subseteq N:S\ni i}|S|^{-1}I_{\mathrm{and}}(S\mid x)',[15],'same_definition',note='本篇外引无原证明；整体模型AND系数与任意分解AND分量需区分。')
add('sym-matching-precision',r'\operatorname{precision}_k','前k交互匹配精度指标',r'\operatorname{precision}_k=\frac{\sum_{S\in K}|I(S)|}{\sum_{S\in K}|I(S)|+|g(N)-g(\varnothing)-\sum_{S\in K}I(S)|}','实数；分母非零时','AppendixM',r'm',r'm=\frac{\sum_{S\in\{\mathrm{top}\ k\}}|I(S)|}{\sum_{S\in\{\mathrm{top}\ k\}}|I(S)|+|v(N)-v(\varnothing)-\sum_{S\in\{\mathrm{top}\ k\}}I(S)|}',[21],'renaming',note='原m与模型数m冲突；v(N)按上下文为集合输出g(N)，原文未给零分母约定。')
P.joinpath('symbols.json').write_text(json.dumps({'schema_version':'3.0','paper_id':PAPER,'symbols':symbols},ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'symbols':len(symbols),'scope':'source_symbol_mapping_only'}))
