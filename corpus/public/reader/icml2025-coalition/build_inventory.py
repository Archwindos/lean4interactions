import json,hashlib
from pathlib import Path
D=Path('corpus/public/reader/icml2025-coalition'); S='src-icml2025-coalition'; V='ver-icml2025-coalition-formal'; H=hashlib.sha256((D/'source.pdf').read_bytes()).hexdigest()
entries=[]
def add(key,title,kind,sp,pp=(),label='',section='',target=None,note=''):
 loc=lambda ps:[{'source_id':S,'version_id':V,'pdf_pages':list(ps),'section':section} ] if ps else []
 e=dict(id='coalition-inv-'+key,original_label=label or key,title=title,kind=kind,statement_locations=loc(sp),proof_locations=loc(pp),all_occurrences=loc(sorted(set(sp)|set(pp))),merge_target_id=target or 'coalition-'+key,merge_rationale=note or 'Distinct mathematical statement or explicitly classified non-proof item.',external_citation='Li & Zhang (2023)' if key=='matching' else None,review_status='agent_reviewed',user_review_status='pending');entries.append(e)
add('illustration','Figure 1 的分配与冲突算例','illustrative_calculation',[1,4],label='Figure 1; §3.2 example')
add('logit','分类任务输出定义','definition',[3,8],label='Eq. (1); Go output definition')
add('shapley-definition','阶乘边际 Shapley 定义与外引唯一性','definition_and_external_result',[3],label='Eq. (2)')
add('and-or-definition','AND/OR 分量、交互与分解参数','definition',[3],label='Eqs. (3),(4)')
add('sparse-optimization','AND/OR 稀疏优化的外引方法','external_algorithm',[3],label='LASSO-like loss')
add('conflict-definition','不同分区的归因冲突定义','definition',[4],label='Definition 3.1')
add('shapley','Shapley 的 AND/OR 均分表达','numbered_theorem',[4],[12,13,14],'Theorem 3.2; Appendix Theorem 2','§3.2; C')
add('banzhaf-definition','Banzhaf 均匀边际定义','definition',[4],label='Eq. (5)')
add('banzhaf','Banzhaf 的 AND/OR 分配表达','numbered_theorem',[4],[14,15],'Theorem 3.3; Appendix Theorem 3','§3.2; D')
add('coalition-definition','联盟归因定义与空集定义域','definition',[4],label='Eq. (6)')
add('conflict','联盟内总 Shapley 与冲突项分解','numbered_theorem',[5],[15,16],'Theorem 3.4; Appendix Theorem 4','§3.4; E')
add('no-conflict','无部分交互时归因无冲突','numbered_corollary',[5],[16],'Corollary 3.5; Appendix Corollary 5','§3.4; E')
add('individual','单变量 Shapley 的联盟与部分覆盖分解','numbered_theorem',[5],[16],'Theorem 3.6; Appendix Theorem 6','§3.4; F')
add('singleton','单元素联盟与 Shapley 一致','numbered_corollary',[5],[17],'Corollary 3.7; Appendix Corollary 7','§3.4; F')
for k,t,p,l in [('anonymity','联盟归因匿名性',[17],'Anonymity axiom'),('symmetry-alpha','联盟归因对称性 α',[18,19],'Symmetry axiom-α'),('symmetry-beta','联盟归因对称性 β',[19,20],'Symmetry axiom-β'),('additivity','联盟归因可加性',[20],'Additivity axiom'),('dummy','联盟归因虚设变量性质',[21],'Dummy axiom')]:add(k,t,'axiom_claim',[6],p,l,'§3.5; G')
add('efficiency','含冲突项的输出效率分解','numbered_corollary',[6],[21],'Corollary 3.8; Appendix Corollary 8','§3.5; G.6')
for k,t,p,l in [('R','绝对值比例的定义域与范围',[6],'Eq. (7)'),('Rprime','单变量绝对交互比例的定义域与范围',[6,7],'Eq. (8)'),('Q','联盟绝对交互比例的定义域与范围',[7],'Eq. (9)')]:add(k,t,'unnumbered_domain_and_range_claim',p,(),l,'§4.1')
add('toy-support','二进制单项式函数的真实交互','unnumbered_algebraic_claim',[7],(), 'Toy function in §4.1','§4.1')
add('matching','AND/OR 全掩码重构','externally_proved_identity',[3,12],(),'Universal-matching; Eq. (10)','§3.1; B')
add('marginal-pairing','插入变量的 AND/OR 配对边际','unnumbered_proof_ingredient',[14],[14,15,21],'D first equations; G.5 first equations','D; G.5',target='coalition-banzhaf',note='Two formula occurrences retained; AND sign misprint is separately recorded. This ingredient is not a second copy of Theorem 3.3.')
add('shapley-coefficient','Shapley 上集/不交集权重为逆阶数','unnumbered_derivation',[13,14],[13,14],'α_L; OR coefficient','C')
add('banzhaf-coefficient','有符号二项式上集权重','unnumbered_derivation',[15],[15],'D signed power sum','D')
add('empirical','三类任务与误差、忠实度的经验观察','empirical_claim',[6,7,8,9,21,22,23,24],label='Tables 2–5; Figures 2–7; I; J')
add('external-comparison','其他归因指标性质的外引与表格','external_comparison',[2,3,5,12],label='Related work; Table 1; A')
sections={1:'Abstract; Introduction; Figure 1',2:'Introduction; Related work; §3.1',3:'§3.1–3.2; Eqs. (1)–(4)',4:'§3.2–3.4; Definition 3.1; Eqs. (5)–(6)',5:'§3.4; Table 1; Theorems/Corollaries 3.4–3.7',6:'§3.5–4.1; Axioms; Corollary 3.8; Eqs. (7)–(8)',7:'§4.1–4.2; Eq. (9); toy functions',8:'§4.2; Figure 2; Go score',9:'§4.2; Conclusion; Impact; References',10:'References',11:'References',12:'A; B; C start; Eq. (10)',13:'C AND coefficient',14:'C OR coefficient; D start',15:'D; E start',16:'E; F',17:'F; G.1',18:'G.2',19:'G.2 end; G.3 start',20:'G.3; G.4',21:'G.5; G.6; H; I start',22:'I; J; Figure 3',23:'Figures 4–5',24:'Figures 6–7'}
page=[]
for p in range(1,25):
 ids=[e['id'] for e in entries if any(p in l['pdf_pages'] for l in e['all_occurrences'])]
 page.append(dict(source_id=S,version_id=V,pdf_page=p,section=sections[p],classification='references_only' if p in (10,11) else ('empirical_figures' if p>=22 else 'mathematical_and_expository'),mathematical_entry_ids=ids,review_status='agent_reviewed',method='full page text read; formula issue pages additionally rendered for visual confirmation',evidence_path=str(D/'source-evidence'/f'p{p:02}.txt'),user_review_status='pending'))
proofkinds={'numbered_theorem','numbered_corollary','axiom_claim','unnumbered_domain_and_range_claim','unnumbered_algebraic_claim','externally_proved_identity','unnumbered_derivation'}
targets=[{'id':e['merge_target_id'],'inventory_ids':[e['id']],'classification':e['kind']} for e in entries if e['kind'] in proofkinds]
x=dict(schema_version='1.0',paper_id='icml2025-coalition',title='Towards Attributions of Input Variables in a Coalition',sources=[dict(source_id=S,path=str(D/'source.pdf'),sha256=H,page_count=24,version_id=V,version='ICML 2025 official PMLR final PDF, includes appendices',page_numbering='1-based physical PDF pages')],review_scope=dict(all_main_and_supplement_pages=True,pdf_pages_checked=24,formal_source_boundary='PMLR final 24-page PDF; no additional linked supplementary PDF'),page_audit=page,entries=entries,proof_targets=targets,counts=dict(numbered_results=7,axiom_claims_excluding_repeated_efficiency=5,unnumbered_domain_or_algebra_targets=4,unnumbered_coefficient_derivations=2,external_identity_targets=1,all_proof_targets=len(targets),original_dedicated_proof_blocks=10,inventory_entries=len(entries),pages_checked=24),review_status='agent_reviewed',user_review_status='pending',completeness_note='The old ten proof blocks are source occurrences, not a denominator. Definitions, empirical claims and proof ingredients remain separately classified. Semantic correctness and Lean scope are audited independently.')
(D/'inventory.json').write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
md=['# ICML 2025 Coalition：正式来源逐页数学清单','',f'正式 PDF：24 页；SHA256 `{H}`。正文编号 3.x 与附录省略前缀的编号合并，原文十个证明块不作为目标数量上限。','', '## 逐页审查','']
for a in page:md.append(f"- PDF {a['pdf_page']}：{a['section']}；条目：{', '.join(a['mathematical_entry_ids']) or '无证明/仅参考文献'}。")
md+=['','## 独立条目','']
for e in entries:md.append(f"- `{e['id']}` ({e['kind']})：{e['title']}；原标签 {e['original_label']}；目标 `{e['merge_target_id']}`。")
md+=['','## 分母','',json.dumps(x['counts'],ensure_ascii=False),'','当前仅代理审查；原陈述正确性、文字重写和 Lean 证据分别记录。']
(D/'inventory.md').write_text('\n'.join(md)+'\n')
meta=dict(id='icml2025-coalition',short_title='联盟输入变量归因',title=x['title'],authors=['Xinhao Zheng','Huiqi Deng','Quanshi Zhang'],venue='ICML 2025',year=2025,intro='以 AND/OR 交互分配重述 Shapley、Banzhaf，并定义联盟归因与冲突分解。',scope='正式正文与所附全部附录24页；编号结果、未编号推导、定义与经验结果分别登记。',version_id=V,version_label='ICML 2025 official PMLR 267:78115–78138 final PDF',visibility='public',publication_status='published',canonical_publication_key='https://proceedings.mlr.press/v267/zheng25d.html',publication_url='https://proceedings.mlr.press/v267/zheng25d.html',results=[],sources=[dict(id=S,label='正式全文（含附录）',kind='main_with_appendix',local_path=str(D/'source.pdf'),url='https://raw.githubusercontent.com/mlresearch/v267/main/assets/zheng25d/zheng25d.pdf',sha256=H,total_pages=24,version_id=V,publication_status='published',visibility='public')],translations={'en':{'short_title':'Coalition attribution','intro':'AND/OR allocation formulas for Shapley and Banzhaf values, coalition attribution, and attribution conflicts.','scope':'All 24 pages of the official paper and included appendices; numbered results, unnumbered derivations, definitions, and empirical observations are separately recorded.'}})
(D/'paper-metadata.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2)+'\n')
print(x['counts'])
