import json,re,copy
from pathlib import Path
D=Path('corpus/public/reader/icml2025-coalition');p=D/'content.json';x=json.loads(p.read_text());by={r['id']:r for r in x['results']}
explicit={
'2^{-(n-1)}':r'2^{-(n-1)}','2^{n-|T|}':r'2^{n-|T|}','1/|T|':r'1/|T|','n-|T|':r'n-|T|','T\\{i}':r'T\setminus\{i\}','U⊆N\\{i}':r'U\subseteq N\setminus\{i\}','T含i':'T contains i',
'i∈N':r'i\in N','i∈T':r'i\in T','i∈S':r'i\in S','|S|>0':r'|S|>0','|S|=1':r'|S|=1','|S|':r'|S|','|T|':r'|T|','|S∩T|':r'|S\cap T|','S⊆T':r'S\subseteq T','S={i}':r'S=\{i\}','T∩S':r'T\cap S','T⊇S':r'T\supseteq S','N\\S':r'N\setminus S','n≥1':r'n\ge1','φ(S)/|S|':r'\phi(S)/|S|','φ({i})':r'\phi(\{i\})','φ(S)':r'\phi(S)','φ(i)':r'\varphi(i)','U_{i,\\bar S}':r'U_{i,\bar S}','U_{i,bar S}':r'U_{i,\bar S}','g(N)-b':r'g(N)-b','g(N)=总和':r'g(N)=\sum_{i\in N}\varphi(i)','d>0':r'd>0','d=0':r'd=0','a=0':r'a=0','0≤a≤d':r'0\le a\le d','0≤a/d≤1':r'0\le a/d\le1','0/0':r'0/0'}
# Remove the prose-only source-language key, then translate exact math expressions only.
explicit.pop('T含i')
pat=re.compile('|'.join(re.escape(k) for k in sorted(explicit,key=len,reverse=True)))
def fmt(s):
 a=re.split(r'(\$[^$]*\$|\\\[[\s\S]*?\\\]|\\\([\s\S]*?\\\))',s)
 for i in range(0,len(a),2):a[i]=pat.sub(lambda m:'$'+explicit[m.group()]+'$',a[i])
 return ''.join(a)
for r in x['results']:
 for steps in [r['proof_steps'],r['translations']['en']['proof_steps']]:
  for st in steps:st['body_md']=fmt(st['body_md'])
sh=by['coalition-shapley'];sh['proof_steps'][1]['body_md']=r'令 $n=|N|$，对每个 $U\subseteq N\setminus\{i\}$ 显式定义 $w(U)=|U|!(n-|U|-1)!/n!$。此阶乘权重是均匀随机排列中 $U$ 恰为 $i$ 前驱集合的概率：前驱和后继各自可任意排列，分别有 $|U|!$ 与 $(n-|U|-1)!$ 种，总排列数为 $n!$。固定非空 $T\subseteq N$ 含 $i$，AND项出现当且仅当 $i$ 在 $T$ 中最后出现，OR项出现当且仅当 $i$ 在 $T$ 中最先出现。交换 $T$ 成员标签给出 $|T|$ 个等大的排列类，故两种概率均为 $1/|T|$。Lean采用等价的有限阶乘卷积路线核验这两个权重；没有把本段排列语言的每句分别声明为Lean定理。'
sh['translations']['en']['proof_steps'][1]['body_md']=r'Let $n=|N|$ and explicitly define $w(U)=|U|!(n-|U|-1)!/n!$ for $U\subseteq N\setminus\{i\}$. This is the probability that U is exactly the predecessor set of i in a uniformly random permutation: the predecessor and successor orders have $|U|!$ and $(n-|U|-1)!$ choices among $n!$ permutations. For fixed nonempty $T\subseteq N$ containing i, its AND term occurs exactly when i is last in T, and its OR term exactly when i is first. Relabeling the members partitions all permutations into $|T|$ equally sized classes, so each probability is $1/|T|$. Lean verifies these weights by an equivalent finite factorial-convolution route; the individual permutation-language sentences are not separately formalized.'
sh['proof_steps'][1]['formula_tex']=r'\sum_{\substack{U\subseteq N\setminus\{i\}\\T\setminus\{i\}\subseteq U}}w(U)=\sum_{\substack{U\subseteq N\setminus\{i\}\\U\cap(T\setminus\{i\})=\varnothing}}w(U)=1/|T|'
sh['translations']['en']['proof_steps'][1]['formula_tex']=sh['proof_steps'][1]['formula_tex']
report=json.loads((D/'verification/report.json').read_text());api={r['name']:r for r in report['declarations']}
def ref(name,zh,en,scope):
 if name in api:row=api[name];path=row['source_path'];line=row['line']
 else:
  path='lean/HarsanyiLib/Harsanyi/Extensions/Attribution.lean';lines=Path(path).read_text().splitlines();line=next(i for i,s in enumerate(lines,1) if 'theorem '+name.split('.')[-1]+' ' in s)
 return dict(declaration=name,source_path=path,line=line,scope=scope,explanation_md=zh),dict(declaration=name,source_path=path,line=line,scope=scope,explanation_md=en)
refs={
'shapley':[
 [('Harsanyi.Coalition.universal_matching','此声明核验所用的重构恒等式；边际相减及激活集合分拆在文字中展开，未另声明此人类步骤完整形式化。','This declaration verifies the reconstruction identity used here. Subtraction and activation-set splitting are expanded in prose and are not a separate formalized marginal-step theorem.','reconstruction_input_to_human_step')],
 [('Harsanyi.factorialWeight_superset_sum','实际Lean路线以有限阶乘卷积证明所需AND权重，OR权重另经补集换元；本段排列计数是独立可读论证。','The Lean route proves the AND kernel by finite factorial convolution and obtains the OR kernel by complement reindexing. The permutation count here is the independent readable argument.','alternative_factorial_kernel_route')],
 [('PaperCoalition.theorem32','该实际模型掩码适配核验最终原Shapley等式，包含原γ分解；不据此声称上面每句分别编译。','This actual coordinate-mask adapter verifies the final original Shapley equality with the source γ decomposition. It does not separately compile every sentence above.','actual_paper_conclusion')]],
'banzhaf':[[('Harsanyi.Coalition.uniformWeight_superset','该有限子集权重声明对应包含计数；OR背景的不交计数在实际路线中使用补集双射。','This finite-subset kernel covers containment counts; the formal OR route obtains disjoint-background counts by a complement bijection.','uniform_subset_kernel')],[('PaperCoalition.theorem33','原均匀边际Banzhaf和真实模型分解的最终适配。','Final adapter for the original uniform-marginal Banzhaf value and actual model splitting.','actual_paper_conclusion')]],
'conflict':[[('Harsanyi.Coalition.sum_membership','逐T的成员计数恒等式真正对应|S∩T|重数。','The per-effect membership-count identity gives the exact intersection multiplicity.','finite_membership_count')],[('PaperCoalition.theorem34_nonempty','原非空商定义域的实际模型结论；原空联盟范围不由此补定义。','Actual model conclusion on the original nonempty quotient domain; the source empty-coalition object is not redefined.','nonempty_source_scope_adapter')]],
'individual':[[('Harsanyi.Coalition.individual_split','对一般交互系数的完整有限和拆分；非空由i∈S推出。','Complete finite-sum splitting for general effect coefficients; membership i∈S implies nonemptiness.','finite_effect_split')],[('PaperCoalition.theorem36','实际模型及原γ分解的Theorem3.6；没有额外非空假设。','Theorem 3.6 for the actual model and source γ split, with no added nonempty premise.','actual_paper_conclusion')]],
'R':[[('Harsanyi.Coalition.r_bounds','原实际联盟与冲突定义生成分子分母，绝对值非负逐项推出域内界；正分母是原商定义域，零分母问题保留。','The actual coalition/conflict definitions generate the numerator and denominator. Absolute-value nonnegativity proves the quotient-domain bound; the source zero-denominator defect remains.','actual_metric_positive_denominator_domain')]],
'Rprime':[[('Harsanyi.Coalition.coveredStrength_le_memberStrength','直接证明原具体有限和的包含关系与非负性，未把分子小于分母作假设。','Direct comparison of the specific source finite sums by containment and nonnegativity; numerator≤denominator is proved rather than assumed.','actual_finite_sum_comparison'),('Harsanyi.Coalition.rprime_bounds','正分母域内完整R′界，原零分母定义问题单列。','Complete R′ bound on the positive-denominator domain; the undefined source zero denominator is separate.','actual_metric_positive_denominator_domain')]],
'Q':[[('Harsanyi.Coalition.coalitionStrength_le_intersectStrength','直接识别覆盖项同权重，部分覆盖余项非负。','Directly match the full-coverage weights and prove the remaining partial-coverage terms nonnegative.','actual_finite_sum_comparison'),('Harsanyi.Coalition.q_bounds','原具体Q有限和的正分母域内界。','Bound for the actual Q finite sums on the positive-denominator domain.','actual_metric_positive_denominator_domain')]]}
for key,steprefs in refs.items():
 r=by['coalition-'+key]
 for zs,es,items in zip(r['proof_steps'],r['translations']['en']['proof_steps'],steprefs):
  pairs=[ref(*t) for t in items];zs['lean_refs']=[t[0] for t in pairs];es['lean_refs']=[t[1] for t in pairs]
 r['lean']['step_map']=[{'step_id':st['id'],**rr} for st in r['proof_steps'] for rr in st.get('lean_refs',[])]
p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
print('Step action and evidence mapping refined')
