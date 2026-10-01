import json,copy,re
from pathlib import Path
D=Path('corpus/public/reader/icml2025-coalition');p=D/'content.json';x=json.loads(p.read_text());by={r['id']:r for r in x['results']}
statements={
'anonymity':r'[\forall U\subseteq N,\ (\sigma g)(\sigma U)=g(U)]\ \Longrightarrow\ \forall S\subseteq N,\ \phi_g(S)=\phi_{\sigma g}(\sigma S)',
'symmetry-alpha':r'[\forall U\subseteq N\setminus\{i,j\},\ g(U\cup\{i\})=g(U\cup\{j\})]\ \Longrightarrow\ \forall L\subseteq N\setminus\{i,j\},\ \phi(L\cup\{i\})=\phi(L\cup\{j\})',
'symmetry-beta':r'[|S|=|T|\ \land\ \forall S\prime\subseteq S,\ \forall T\prime\subseteq T,\ |S\prime|=|T\prime|\Rightarrow\forall L\subseteq N\setminus(S\prime\cup T\prime),\ g(L\cup S\prime)=g(L\cup T\prime)]\ \Longrightarrow\ \forall L\subseteq N\setminus(S\cup T),\ \phi(L\cup S)=\phi(L\cup T)',
'additivity':r'[\forall U\subseteq N,\ g(U)=g_1(U)+g_2(U)]\ \Longrightarrow\ \forall S\subseteq N,\ \phi_g(S)=\phi_{g_1}(S)+\phi_{g_2}(S)',
'dummy':r'[\exists i\in S,\ \forall U\subseteq N\setminus\{i\},\ g(U\cup\{i\})=g(U)]\ \Longrightarrow\ \phi(S)=0'}
for k,f in statements.items():by['coalition-'+k]['statement_tex']=f
by['coalition-dummy']['rewrite_status']='complete_with_definition_only_counterexample';by['coalition-dummy']['semantic_status']='false_under_displayed_definitions; optimizer_selected_version_unresolved'
for k in ['anonymity','symmetry-alpha','symmetry-beta','additivity','dummy']:
 r=by['coalition-'+k];old=r['proof_steps'][0];enold=r['translations']['en']['proof_steps'][0]
 if k in ['anonymity','symmetry-alpha','symmetry-beta']:
  chunks=['取$N=\\{1,2,3\\}$和$g(U)=|U|$，令$P=\\{1,3\\}$。设$a(U)=\\mathbf1[P\\subseteq U]+\\mathbf1[2\\in U]$，$o(U)=\\mathbf1[U\\cap P\\ne\\varnothing]$。按U在P中的0/1/2个成员逐类检查，$a+o=g$；$\\gamma_U=a(U)-g(U)/2$给出实际原分解参数。', '纯AND/OR交互分布给$A(P)=O(P)=1$及$A(\\{2\\})=1$，其余非空交互为0，故L1=3。任意分解由全掩码匹配有$g(N)-b=\\sum_{T\\ne\\varnothing}(A(T)+O(T))$；三角不等式使L1至少为$|g(N)-b|=3$。本分解达到下界，是全局最优而非非最优自由分解。', '$\\phi(\\{1,3\\})=2$，$\\phi(\\{2,3\\})=0$。总g仅依赖基数，满足α的$i=1,j=2,L=\\{3\\}$及β的$S=\\{1\\},T=\\{2\\},L=\\{3\\}$全部前提，结论失败。对匿名性，若只置换总游戏而独立选择最优分解，同一选解也可失败；若同时运输既定分量，则原换元式成立，两种作用域分开。']
  echunks=[r'Let $N=\{1,2,3\}$, $g(U)=|U|$, and $P=\{1,3\}$. Define $a(U)=\mathbf1[P\subseteq U]+\mathbf1[2\in U]$ and $o(U)=\mathbf1[U\cap P\ne\varnothing]$. Checking 0, 1, and 2 present members of P gives $a+o=g$. The actual source parameter is $\gamma_U=a(U)-g(U)/2$.',r'Pure AND/OR coefficient distribution gives $A(P)=O(P)=1$ and $A(\{2\})=1$, with all other nonempty coefficients zero. Thus L1=3. Exact matching implies $g(N)-b=\sum_{T\ne\varnothing}(A(T)+O(T))$ for every decomposition, and the triangle inequality makes L1 at least $|g(N)-b|=3$. This decomposition reaches the bound and is globally optimal.',r'The attributions are $\phi(\{1,3\})=2$ and $\phi(\{2,3\})=0$. The cardinality game satisfies every premise of α with $i=1,j=2,L=\{3\}$, and of β with $S=\{1\},T=\{2\},L=\{3\}$, but their conclusions fail. For anonymity, independently selecting an optimum after permuting only the total game need not preserve attribution; transporting the fixed components does give the original valid change-of-variables identity. These scopes are distinct.']
 elif k=='additivity':
  chunks=['令$N=\\{1,2\\}$，$g_1(U)=\\mathbf1[1\\in U]$、$g_2(U)=\\mathbf1[2\\in U]$，$g=g_1+g_2$。对子游戏取$a_k=g_k,o_k=0$，对总游戏取$a(U)=\\mathbf1[N\\subseteq U]$、$o(U)=\\mathbf1[U\\ne\\varnothing]$；$a+o=g$且$\\gamma_U=a(U)-g(U)/2$。','子游戏L1均为1，总游戏唯一非零交互为$A(N)=O(N)=1$，L1=2。任何精确分解的L1都至少是$|g(N)-b|$，本例总游戏下界2和子游戏下界1都达到，所以三次分解全部全局最优。','两个子游戏只有单变量交互，$\\phi_{g_1}(N)=\\phi_{g_2}(N)=0$，总游戏则$\\phi_g(N)=2$。原总游戏可加条件成立，归因可加结论失败；不能补分量兼容条件来完成原公理。']
  echunks=[r'Let $N=\{1,2\}$, $g_1(U)=\mathbf1[1\in U]$, $g_2(U)=\mathbf1[2\in U]$, and $g=g_1+g_2$. Use $a_k=g_k,o_k=0$ for the subgames, and $a(U)=\mathbf1[N\subseteq U]$, $o(U)=\mathbf1[U\ne\varnothing]$ for the total game. Then $a+o=g$ and $\gamma_U=a(U)-g(U)/2$ realizes the source parameterization.',r'The subgames each have L1 value 1. The total game has only $A(N)=O(N)=1$, hence L1 value 2. Exact matching and the triangle inequality bound every L1 by $|g(N)-b|$ from below. Each of these three decompositions reaches its respective bound, so every one is globally optimal.',r'The subgames have only singleton effects, giving $\phi_{g_1}(N)=\phi_{g_2}(N)=0$, whereas $\phi_g(N)=2$. The source total-game additivity premise holds and its attribution conclusion fails. Adding compatibility of components would change the original axiom.']
 else:
  chunks=['令$N=\\{1,2\\}$、$g(U)=0$且$\\gamma_U=\\mathbf1[U=N]$，于是$a=\\gamma,o=-\\gamma$。所有变量都满足总游戏dummy条件，且原显示分量定义与$g=a+o$严格成立。','计算$A(N)=1$、$O(N)=1$，所以$\\phi(N)=2\\ne0$。此例L1=4而零分解L1=0，故此反例准确只反驳原显示定义推出dummy的陈述，不声称反驳另加全局最优选解规则的版本。该未充分规定版本保留未判定。']
  echunks=[r'Let $N=\{1,2\}$, $g(U)=0$, and $\gamma_U=\mathbf1[U=N]$, so $a=\gamma,o=-\gamma$. Every variable is dummy for the total game, while the displayed component definitions and $g=a+o$ hold exactly.',r'Compute $A(N)=O(N)=1$, hence $\phi(N)=2\ne0$. This decomposition has L1=4 whereas the zero decomposition has L1=0. It refutes dummy from the displayed definitions, not a separate rule selecting a global optimum. That incompletely specified stronger version remains unresolved.']
 titles=['构造符合原定义的分解','核对交互与全局最优性','计算归因并检查原结论'] if k!='dummy' else ['构造原显示定义的dummy游戏','计算反例并限定优化范围']
 etitles=['Construct a decomposition satisfying the source definitions','Check coefficients and global optimality','Compute attributions and test the original conclusion'] if k!='dummy' else ['Construct a dummy total game under the displayed definitions','Compute the counterexample and delimit optimizer scope']
 r['proof_steps']=[];r['translations']['en']['proof_steps']=[]
 for i,(zh,en,zt,et) in enumerate(zip(chunks,echunks,titles,etitles),1):
  stid='coalition-'+k+'-step-'+str(i);z=dict(id=stid,title=zt,body_md=zh,formula_tex='',justification='',lean_refs=[]);e=dict(z,title=et,body_md=en);r['proof_steps'].append(z);r['translations']['en']['proof_steps'].append(e)
# Specific action titles for every remaining proof step.
titles={'shapley':[('展开掩码边际','Expand masked marginals'),('按排列首尾位置计数','Count first and last positions'),('交换有限求和并保留边界','Exchange finite sums and check the domain')],'banzhaf':[('按均匀背景子集计数','Count uniform background subsets'),('累积AND/OR贡献','Accumulate AND/OR contributions')],'conflict':[('按交集基数计重数','Count intersection multiplicities'),('拆分全部与部分覆盖','Split full and partial coverage')],'no-conflict':[('逐项消去零交互','Eliminate zero interaction terms')],'individual':[('拆分含i的交互族','Split effects containing i'),('识别联盟均分项','Identify the equal coalition share')],'singleton':[('消去空的部分覆盖类','Eliminate the empty partial-coverage family')],'efficiency':[('应用带基线的效率','Apply efficiency with the baseline'),('代入联盟冲突分解','Insert the coalition-conflict decomposition')],'matching':[('分别反演AND与OR分量','Invert the AND and OR components')],'R':[('比较绝对值分子与分母','Compare the absolute numerator and denominator')],'Rprime':[('用覆盖族包含关系比较有限和','Compare finite sums by containment of coverage families')],'Q':[('匹配完整覆盖权重并保留非负余项','Match full-coverage weights and retain nonnegative residuals')],'toy-support':[('识别二进制单项式的AND支撑','Identify AND supports of binary monomials')],'shapley-coefficient':[('按排列位置证明逆阶数权重','Prove reciprocal-order weights by permutation positions')],'banzhaf-coefficient':[('用补集双射和二项式展开','Use a complement bijection and the binomial expansion')]}
for k,ls in titles.items():
 r=by['coalition-'+k]
 for st,enst,(zh,en) in zip(r['proof_steps'],r['translations']['en']['proof_steps'],ls):st['title']=zh;enst['title']=en
# Real paper adapters replace helper-only declaration links.
refs={'shapley':['shapley_and_or'],'banzhaf':['banzhaf_and_or'],'conflict':['paper_conflict'],'no-conflict':['paper_no_conflict','paper_individual_no_conflict'],'individual':['paper_individual'],'singleton':['paper_singleton'],'efficiency':['paper_efficiency'],'matching':['universal_matching'],'R':['r_bounds'],'Rprime':['rprime_bounds'],'Q':['q_bounds']}
for k,names in refs.items():
 r=by['coalition-'+k];r['lean']['declarations']=['Harsanyi.Coalition.'+n for n in names]
 if k in ['R','Rprime','Q']:
  r['lean']['scope']='Exact finite-sum numerator/denominator adapter on the original positive-denominator quotient domain; the source zero-denominator case is not repaired.'
  r['rewrite_status']='complete_with_original_domain_issue'
 for st in r['proof_steps']:st['lean_refs']=[dict(declaration='Harsanyi.Coalition.'+names[0],source_path='lean/HarsanyiLib/Harsanyi/Extensions/CoalitionAttribution.lean',scope='paper_adapter_with_scope_disclosed',explanation_md='实际原定义的有限和适配；原空集或分母范围另列。')]
 for st,enst in zip(r['proof_steps'],r['translations']['en']['proof_steps']):enst['lean_refs']=copy.deepcopy(st['lean_refs'])
# Contextual AND result does not identify learned AND/OR splitting coefficients.
r=by['coalition-toy-support'];r['proof_scope']='二进制原函数的Harsanyi AND系数；不把任意学习AND/OR分解的A/O系数称唯一真实支撑';r['completion_scope']=r['proof_scope'];r['translations']['en']['proof_scope']='Harsanyi AND coefficients of the binary target function; not uniqueness of A/O coefficients in an arbitrary learned AND/OR decomposition';r['translations']['en']['completion_scope']=r['translations']['en']['proof_scope']
r['proof_steps'][0]['body_md']+=' 这条纯单项式结论是总函数的Harsanyi AND支撑，不意味着原γ学习分解后的A、O分别只能在T_k非零；非唯一的AND/OR分解需另核。';r['translations']['en']['proof_steps'][0]['body_md']+=' This is the Harsanyi AND support of the total monomial game. It does not imply that A and O after learning γ can only be nonzero at the T_k; those decomposition coefficients can be nonunique.'
# Exact types of source content are individualized.
for r in x['results']:
 if r['kind'] not in {'numbered_theorem','numbered_corollary','axiom_claim','unnumbered_derivation'} and not r.get('original_proof_path'):r['original_statement_source_type']='classified_source_definition_or_claim_with_project_explanation';r['source_transcription_status']='source_mathematical_item_classified'
 if r['rewrite_status']=='not_a_proof_target':r['lean']['status']='not_applicable'
p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
# Canonical symbol mappings, with empty-set and baseline conventions kept separate.
symbols=[]
def sym(id,tex,zh,en,definition,domain,orig,pages,relation='renaming'):
 symbols.append(dict(id=id,canonical_tex=tex,name_zh=zh,definition_tex=definition,description_md=zh,type_or_domain=domain,scope='icml2025-coalition; fixed finite universe/input/baseline/decomposition',assumptions=['有限总体；所有掩码用同一分解。'],empty_set_convention='原AND/OR公式只对非空交互；分量空输出单独保留。',baseline_convention='g(空集)=b，a(空集)+o(空集)=b，不默认零。',aliases=[orig],paper_mappings=[dict(paper_id='icml2025-coalition',version_id='ver-icml2025-coalition-formal',original_tex=orig,original_definition=definition,pdf_pages=pages,source_id='src-icml2025-coalition',canonical_concept=id,relationship=relation)],lean_names=[],version='1.0',translations={'en':dict(name=en,description_md=en,assumptions=['Finite universe; one fixed decomposition for every mask.'],empty_set_convention='The source AND/OR coefficient formulas apply to nonempty sets; component empty outputs are separate.',baseline_convention='g(empty)=b and a(empty)+o(empty)=b; no zero baseline is assumed.')}))
sym('sym-coalition-and-component','a(S)','AND输出分量','AND output component',r'a(S)=g(S)/2+\gamma_S','2^N→ℝ','v_{and}(S)',[3])
sym('sym-coalition-or-component','o(S)','OR输出分量','OR output component',r'o(S)=g(S)/2-\gamma_S','2^N→ℝ','v_{or}(S)',[3])
sym('sym-coalition-decomposition-parameter',r'\gamma_S','AND/OR分解参数','AND/OR decomposition parameter',r'\gamma_S=a(S)-g(S)/2','2^N→ℝ',r'\gamma_L',[3])
sym('sym-coalition-and-effect','A(T)','分量AND交互','Component AND effect',r'A(T)=I_a(T)','nonempty T⊆N','I_{and}(T)',[3,12])
sym('sym-coalition-or-effect','O(T)','分量OR交互','Component OR effect',r'O(T)=-I_{o(N\setminus\cdot)}(T)','nonempty T⊆N','I_{or}(T)',[3,12])
sym('sym-coalition-total-effect','J(T)','AND/OR交互之和','Sum of AND/OR effects',r'J(T)=A(T)+O(T)','nonempty T⊆N','I_{and}(T)+I_{or}(T)',[4,5,6])
sym('sym-coalition-attribution',r'\phi(S)','联盟归因','Coalition attribution',r'\phi(S)=\sum_{T\supseteq S}|S|J(T)/|T|','nonempty S⊆N; original empty scope undefined',r'\phi(S)',[4])
sym('sym-coalition-shapley',r'\varphi(i)','经典Shapley值','Classical Shapley value',r'\varphi(i)=\sum_{U\subseteq N\setminus\{i\}}\frac{|U|!(n-|U|-1)!}{n!}[g(U\cup\{i\})-g(U)]','i∈N',r'\varphi(i)',[3])
sym('sym-coalition-banzhaf','B(i)','Banzhaf值','Banzhaf value',r'B(i)=2^{1-n}\sum_{U\subseteq N\setminus\{i\}}[g(U\cup\{i\})-g(U)]','i∈N','B(i)',[4])
sym('sym-coalition-uniform-share','U_{i,S}','单变量联盟均分项','Individual equal coalition share',r'U_{i,S}=\phi(S)/|S|','i∈S','U_{i,S}',[5])
sym('sym-coalition-individual-conflict',r'U_{i,\bar S}','单变量部分覆盖冲突','Individual partial-coverage conflict',r'U_{i,\bar S}=\sum_{T\ni i,T\not\supseteq S}J(T)/|T|','i∈S',r'U_{i,\bar S}',[5])
sym('sym-coalition-total-conflict',r'\varphi_{conflict}(S)','联盟总冲突归因','Total coalition conflict',r'\varphi_{conflict}(S)=\sum_{\varnothing\ne T\cap S\ne S}|T\cap S|J(T)/|T|','nonempty S⊆N',r'\varphi_{conflict}(S)',[5])
for key,tex,page in [('R','R(i)',[6]),('Rprime',r'R\prime(i)',[6]),('Q','Q(S)',[7])]:sym('sym-coalition-metric-'+key,tex,'联盟忠实度比例 '+key,'Coalition-faithfulness ratio '+key,by['coalition-'+key]['statement_tex'],'original positive-denominator quotient domain',tex,page)
# Common mappings use the established concept IDs and do not conflate the paper shorthand with the model.
for id,tex,zh,en,de,orig in [('sym-model','v','模型','Model',r'v:X\to\mathbb R','v'),('sym-game','g(S)','掩码集合函数','Masked game',r'g(S)=v(x_S)','v(S)'),('sym-output-baseline','b','输出基线标量','Output baseline scalar',r'b=v(x_\varnothing)',r'v(\varnothing)'),('sym-universe','N','有限变量总体','Finite variable universe',r'N=\{1,\ldots,n\}','N'),('sym-mask','x_S','固定基线掩码输入','Fixed-baseline masked input',r'(x_S)_i=x_i\ (i\in S),\quad r_i\ (i\notin S)','x_S')]:sym(id,tex,zh,en,de,'see canonical definition',orig,[3],relation='same_definition' if id!='sym-game' else 'renaming')
(D/'symbols.json').write_text(json.dumps(dict(paper_id='icml2025-coalition',symbols=symbols),ensure_ascii=False,indent=2)+'\n');x['symbols']=symbols
# Include all relevant paper-specific symbols in each entry, avoiding missing references.
for r in x['results']:r['symbol_ids']=list(dict.fromkeys(r['symbol_ids']+[s['id'] for s in symbols]))
p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
m=D/'paper-metadata.json';meta=json.loads(m.read_text());meta['results']=[dict(id=r['id'],title=r['title'],kind=r['kind']) for r in x['results']];m.write_text(json.dumps(meta,ensure_ascii=False,indent=2)+'\n')
print('Updated',len(x['results']),'results;',len(symbols),'symbol concepts')
