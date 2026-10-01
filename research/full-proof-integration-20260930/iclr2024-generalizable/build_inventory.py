#!/usr/bin/env python3
"""Inventory of the selected published PDF; original bytes are never modified."""
import collections
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
LEAF = Path(__file__).resolve().parent
PAPER = 'iclr2024-generalizable'
SOURCE = 'src-iclr2024-generalizable-main'
PDF = ROOT / 'research/paper-survey-20260930/recent/pdf/iclr2024-generalizable.pdf'
TEXT = ROOT / 'research/paper-survey-20260930/recent/text/iclr2024-generalizable.pages.json'
pages = json.loads(TEXT.read_text())

def entry(id, label, title, kind, statement, proof, occurrences, basis, target=False, merge=None, external=None):
    return dict(id=id, paper_id=PAPER, original_label=label, aliases=[], title=title,
                kind=kind, proof_target=target,
                statement_locations=[dict(source_id=SOURCE, pdf_page=p, label=label) for p in statement],
                proof_ranges=[dict(source_id=SOURCE, start_pdf_page=a, end_pdf_page=b, section=s) for a,b,s in proof],
                occurrences=[dict(source_id=SOURCE,pdf_page=p,role=r,label=l) for p,r,l in occurrences],
                merge_target_id=merge or id, external_basis=external,
                classification_basis=basis, review_status='agent_reviewed',user_review_status='pending')

E = []
def add(*args,**kwargs): E.append(entry(*args,**kwargs))
add('f11-model-mask','Section 2.1; footnotes 3–5','模型、掩码与输入基线','definition',[2,3],[],[(2,'definition','v: R^n→R；固定x与N'),(3,'definition','footnote 5 input baseline bi'),(20,'example','L Steps 1–4'),(23,'scope','O.2 固定背景')], '同一模型/输入/基线下的掩码定义；输入bi与输出基线分离。')
add('f11-and-definition','Eq.(1)','AND/Harsanyi 交互及空集约定','definition',[2],[],[(2,'definition','Eq.(1)'),(12,'repeat','Appendix C(1)'),(20,'repeat','L Step 6')], '定义并非待证明定理；附录定义作用于AND分量。')
add('f11-and-mask-zero','Section 2.1, AND interactions','某变量被掩码后含该变量的AND交互为零','unnumbered_claim',[2],[],[(2,'statement','raining cats and dogs example')], '给出一般消失结论但本篇没有展开证明；依赖同一基线的重复掩码语义。',True)
add('f11-or-definition','Eq.(2)','OR交互及单列空集值','definition',[3],[],[(3,'definition','Eq.(2)'),(13,'repeat','Appendix C(2)'),(20,'repeat','L Step 6')], 'Eq.(2)的非空式与明确空集约定分别保存，不把空集定义误报为矛盾。')
add('f11-or-duality','Section 2.1; footnote 5','反转掩码状态后的负AND变换','unnumbered_derivation',[3],[(3,3,'footnote 5')],[(3,'argument','OR as a specific AND interaction, state reversal')], '对非空S，OR值等于反转掩码集合函数AND变换的负值；稀疏推广仍需外引条件。',True)
add('f11-external-sparsity','Section 2.1; Appendix B','AND稀疏性及其三项条件（外引）','external_claim',[3,12],[],[(1,'summary','Introduction'),(3,'statement','Sparsity of interactions'),(12,'conditions','Appendix B'),(15,'repeat','Appendix E')], '本篇仅定性转述三个条件，没有本地完整证明；对应ICLR Sparse论文需独立对齐。',True,external='Ren et al. (2024)')
add('f11-significant-definition','Definition of interaction primitives','显著交互集合','definition',[3],[],[(3,'definition','Omega threshold'),(4,'repeat','Definition 1'),(21,'repeat','L Step 8')], '阈值定义；不把显著性阈值本身当作稀疏性证明。')
add('iclr2024-generalizable-theorem1','Theorem 1','全部掩码的精确AND重构（Theorem 1精确部分）','external_theorem_component',[3],[],[(3,'statement','Theorem 1 exact equality'),(12,'reference','Appendix B'),(15,'repeat','Appendix E')], '原定理把精确重构与近似稀疏同写；此项是可独立证明的精确恒等式。',True,external='Ren et al. (2024)')
add('f11-theorem1-approx','Theorem 1, approximate clause','少量显著交互近似全部输出（外引）','external_theorem_component',[3],[],[(3,'statement','Theorem 1 ≈ clause'),(12,'conditions','Appendix B'),(15,'repeat','Appendix E')], '≈与≪没有本篇量化精度定义；不得补阈值误差结论后冒充原定理。',True,external='Ren et al. (2024)')
add('iclr2024-generalizable-andor','Theorem 2; Eq.(3),(7)','AND-OR联合匹配完整定理','theorem',[3,12],[(12,14,'Appendix C Proof(1)–(3)')],[(3,'statement','Eq.(3)'),(12,'statement_repeat','Eq.(7)'),(14,'proof','C(3) synthesis'),(15,'repeat','Appendix E'),(22,'empirical','N.2')], '保留原x_T条件式。三个分量/合成证明分别登记；母式证明不能替代字面式掩码合成对齐。',True)
add('iclr2024-generalizable-and','Appendix C(1); Eq.(8)','固定x的AND子结论','theorem_component',[12],[(12,13,'Appendix C(1)')],[(12,'statement','C(1) fixed x'),(13,'proof','AND binomial cancellation and Eq.(8)')], '正文父定理与子结论不合并完成状态；Eq.(8)首行x_T记号保留并说明。',True)
add('iclr2024-generalizable-or','Appendix C(2); Eq.(9)','OR子结论与原分类推导','theorem_component',[13],[(13,14,'Appendix C(2)')],[(13,'statement','OR universal matching'),(13,'proof','case(1)'),(14,'proof','case(2)–(4), Eq.(9)')], 'case(3)内和逐项为0与case(4)范围有原证明错误；已获proof-only修正权限，命题保持。',True)
add('f11-proposition1','Proposition 1','少量AND-OR交互近似输出','proposition',[4],[],[(4,'statement','Proposition 1'),(15,'repeat','Appendix E theory and empirical matching')], '本篇无单独证明，依赖Theorem 2和外引稀疏；近似精度未量化，不能编造假设或证明。',True)
add('f11-boolean-decomposition','Section 2.2 Challenge 1','五变量布尔函数的两种精确分解','worked_algebraic_example',[4],[(4,4,'Challenge 1')],[(4,'example','3AND+1OR versus 6AND')], '完整代数恒等式与支持项计数；不是全局优化唯一性/最优性定理。',True)
add('f11-transferability','Definition 1','交互可迁移率与共同交互','definition',[4],[],[(4,'definition','Definition 1'),(5,'application','two initialization overlap'),(8,'application','cross-model ratios'),(21,'application','N.1 Table 2')], '集合交/比例定义；空分母未指定，符号表保留该定义域限制。')
add('f11-reparameterization','Section 2.3; Section 2.3.2','AND-OR分解与gamma的一一重参数','unnumbered_derivation',[4,6],[(4,4,'Section 2.3')],[(4,'argument','equivalence of decomposition and gamma'),(6,'repeat','multi-model decomposition'),(20,'example','L Step 5')], '对各掩码逐点的实数恒等式；无须优化完成或原OR证明。',True)
add('f11-objectives','Eq.(4),(5),(6)','稀疏、跨模型及冗余损失的定义','optimization_definition',[5,6],[],[(5,'definition','Eq.(4)'),(6,'definition','Eq.(5),(6), rowmax ℓ∞'),(16,'repeat','Appendix F'),(17,'empirical','H'),(18,'empirical','I ablation'),(21,'algorithm','L Step 7')], '损失定义及设计解释，原文未证明训练最终全局泛化保证。')
add('f11-rowmax-penalty','Section 2.3.2, following Eq.(5)','不超过已有行最大强度时不增加该行惩罚','unnumbered_derivation',[6],[(6,6,'following Eq.(5)')],[(6,'argument','other m−1 models without a penalty')], '可证明的是行最大范数的局部不变性；不扩大成学习得到泛化的全局定理。',True)
add('f11-shared-gamma','Section 2.3.2, Sharing decomposition','共享/个体分解与剪裁规则','algorithm_rule',[6],[],[(6,'method','gamma=bar gamma+hat gamma; strict bound and clipping')], '优化参数化和操作；严格<目标与剪裁等于阈值的边界表述需显式记录。')
add('f11-and-variance','Section 2.3.2; Appendix D','独立高斯噪声的AND交互方差','unnumbered_theorem',[7,15],[(15,15,'Appendix D')],[(5,'motivation','noise sensitivity'),(7,'statement','2^|T| sigma²'),(15,'proof','Appendix D complete AND variance argument')], '固定交互为常数；对所有子集IID高斯输出噪声推导真正随机变量方差，不仅符号平方计数。',True)
add('f11-or-variance','Section 2.3.2, Similarly','独立高斯噪声的OR交互方差','unnumbered_theorem',[7],[],[(7,'statement','Similarly OR variance'),(15,'heading','D title mentions AND and OR but body only AND')], '本篇没有独立OR细证；同样通过补集重索引的随机噪声证明，空集值单列。',True)
add('f11-noise-error','Section 2.3.2, Modeling noises','可学习误差及剪裁','algorithm_rule',[7],[],[(7,'method','v=vand+vor+epsilon, clipping and error'),(22,'empirical','N.2 removal error')], 'IID随机噪声与优化误差同用epsilon但不同概念；打印|epsilon|=tau sign(epsilon)负号问题独立登记。')
add('f11-shapley','Theorem 3','AND交互均匀分配与Shapley值','external_theorem',[15],[],[(15,'statement','Theorem 3')], '只外引Harsanyi1963，本篇无原证明；复用公共精确定义与完整数学证明。',True,external='Harsanyi (1963)')
add('f11-equation10','Appendix F; Eq.(10)','两模型损失的原式展开','claimed_identity',[16],[(16,16,'Appendix F Eq.(10)')],[(16,'derivation','Eq.(10)')], 'p6行范数的逐点展开与p16有符号max有反例；原父min等式还含自由索引，严格意义及最优值等价尚未判定。',True)
add('f11-mask-complexity','Appendix G','全部掩码数与模型查询计数','unnumbered_derivation',[16],[(16,17,'Appendix G')],[(3,'repeat','2^n masked samples'),(16,'argument','G theoretical complexity'),(17,'empirical','G timing'),(20,'example','2^6=64 masks'),(22,'repeat','O.2'),(23,'repeat','O.2')], '严格可核的是2^n子集/按全部掩码查询的计数；不将其等同整个训练优化运行时的完整界。',True)
add('f11-alpha-zero','Appendix I, alpha=0','alpha=0时Eq.(6)退化为Eq.(5)','algebraic_corollary',[17],[],[(17,'statement','alpha=0 experiment setting'),(18,'figure','alpha ablation continuation')], '原文消融中的确定恒等式，保留为小推导，经验曲线不计数学证明。',True)
add('f11-procedure-example','Appendix L, Steps 1–8','六token完整交互提取例','algorithm_example',[19,20,21],[],[(19,'example','L Step1 start'),(20,'example','L Steps1–6'),(21,'example','L Steps7–8')], '列输入域、基线、64掩码、log odds、gamma、交互、优化、阈值；它不是另一条一般正确性证明。')
add('f11-matching-metric','Appendix M','前k交互的匹配精度指标','definition',[21],[],[(21,'definition','M metric m')], 'm与模型个数m冲突；v(N)是集合输出简写；分母为0边界未指定。')
add('f11-empirical','Section 3; Appendix E,H,I,J,K,M,N,O.1','稀疏性、迁移率、可视化与匹配实验','empirical_observation',[7,8,9,15,17,18,19,20,21,22],[],[(7,'empirical','Section3'),(8,'empirical','Figures2–4'),(9,'empirical','Figure5 and conclusion'),(15,'empirical','E'),(17,'empirical','G timing,H baselines'),(18,'empirical','I,J'),(19,'empirical','J,K'),(20,'empirical','K Figure10'),(21,'empirical','M,N.1'),(22,'empirical','N.2,O.1')], 'N.1是随机初始化所得局部解/交互差异实验，没有全球最优解多样性的数学证明。')
add('f11-background-selection','Appendix O.2; Appendix E','所选输入变量与固定背景的作用域','experimental_scope',[15,22,23],[],[(15,'scope','selected t<n'),(22,'scope','O.2 begins'),(23,'scope','SST2/SQuAD/MNIST selection')], '全部掩码是相对所选N；未选背景不属于掩码总体。经验无交互判断不是形式化零交互条件。')

sections = {
1:'Abstract; Introduction',2:'Introduction; 2.1 AND preliminaries',3:'2.1 OR, sparsity, Theorem 1; 2.2 Theorem 2',4:'Proposition 1; Challenge 1; Definition 1; 2.3 decomposition',
5:'Eq.(4); 2.3.1 limitations; 2.3.2 begins',6:'Eq.(5),(6); rowmax; shared decomposition',7:'Modeling noises; Section 3 tasks',8:'Section 3 experiments; Figures 2–4',9:'Section 3 Figure 5; Conclusion; Acknowledgements',10:'References',11:'References',12:'Appendix A literature; B conditions; C Theorem 2 / AND proof starts',13:'Appendix C AND proof; OR proof case(1)',14:'Appendix C OR case(2)–(4); Eq.(9); AND-OR synthesis',15:'Theorem 3; Appendix D variance; E theory and experiments',16:'Appendix E Figure6; F Eq.(10); G complexity starts',17:'Appendix G timings; H baseline experiment',18:'Appendix I alpha ablation; J visualization',19:'Appendix J Figure9; K discussion; L Step1 starts',20:'Appendix K Figure10; L Steps1–6',21:'Appendix L Steps7–8; M metric; N.1 diversity experiments',22:'Appendix N.2 matching; O.1 model performance; O.2 starts',23:'Appendix O.2 input selection details'}
page_audit=[]
for p in range(1,24):
    ids=[e['id'] for e in E if any(o['pdf_page']==p for o in e['occurrences'])]
    classes=sorted({e['kind'] for e in E if e['id'] in ids})
    if not ids: classes=['references']
    page_audit.append(dict(source_id=SOURCE,pdf_page=p,section=sections[p],entry_ids=ids,classifications=classes,
                           reviewed_text=True,review_status='agent_reviewed',
                           conclusion='数学条目与重复出现已登记；本页经验/定义不自动计为证明。' if ids else '参考文献页，无新命题或证明。'))

counts=dict(pages_reviewed=23,entries=len(E),proof_targets=sum(e['proof_target'] for e in E),
            local_explicit_proof_targets=[e['id'] for e in E if e['proof_target'] and e['proof_ranges']],
            named_theorems=['Theorem 1','Theorem 2','Theorem 3'],named_propositions=['Proposition 1'],
            occurrence_count=sum(len(e['occurrences']) for e in E),kinds=dict(collections.Counter(e['kind'] for e in E)))
inventory=dict(schema_version='3.0',paper_id=PAPER,sources=[dict(source_id=SOURCE,version_id='ver-iclr2024-generalizable-formal',
    path=str(PDF.relative_to(ROOT)),sha256=hashlib.sha256(PDF.read_bytes()).hexdigest(),pages=23,publication_status='published_formal',visibility='public')],
    review_scope='All 23 pages of the published ICLR 2024 PDF, main text and appendices A–O.',
    review_status='agent_reviewed',user_review_status='pending',page_audit=page_audit,entries=E,counts=counts,
    counting_note='18 proof targets include a parent joint theorem and its separately addressable AND/OR components. They are coverage obligations, not 18 distinct locally authored proofs. Definitions, algorithm rules and empirical results are outside this denominator.',
    source_transcription_policy='Complete original PDF pages are retained. Result-level mathematical transcription and complete project translation/rewrite are separately typed; text extraction is not advertised as verified TeX.')
LEAF.mkdir(parents=True,exist_ok=True)
(LEAF/'inventory.json').write_text(json.dumps(inventory,ensure_ascii=False,indent=2)+'\n')
lines=['# ICLR 2024 Generalizable：全篇数学清单','',f'已审查正式 PDF 全部23页。共{len(E)}个归并条目、{counts["proof_targets"]}个证明/推导覆盖目标、{counts["occurrence_count"]}处出现。包括父定理与子结论，不把这个数字称为独立原证明数量。正文3个Theorem、1个Proposition；Definition 1以及方法、实验另列。','', '原件未修改。原证明错误依最新授权可作忠实证明修正；原命题/假设未获修改授权。', '', '## 逐页核对', '', '| PDF页 | 章节 | 条目数 | 分类 |','|---|---|---:|---|']
for p in page_audit: lines.append(f'| {p["pdf_page"]} | {p["section"]} | {len(p["entry_ids"])} | {", ".join(p["classifications"])} |')
lines+=['','## 归并条目','', '| ID | 原号 | 类型/覆盖 | 陈述页 | 原证明范围 | 判定 |', '|---|---|---|---|---|---|']
for e in E:
    ps=', '.join(str(x['pdf_page']) for x in e['statement_locations'])
    pr='; '.join(f'{x["start_pdf_page"]}–{x["end_pdf_page"]} {x["section"]}' for x in e['proof_ranges']) or ('本篇无证；外引'+e['external_basis'] if e['external_basis'] else '本篇无单独展开')
    lines.append(f'| {e["id"]} | {e["original_label"]} | {e["kind"]}{" / 待证覆盖" if e["proof_target"] else ""} | {ps} | {pr} | {e["classification_basis"]} |')
(LEAF/'inventory.md').write_text('\n'.join(lines)+'\n')
# This complete extraction is an accessible source companion, not a mathematical rewrite.
(LEAF/'source-review'/'all-pages.txt').write_text('\n\n'.join(f'PDF PAGE {p["page"]}\n{p["text"]}' for p in pages))
print(json.dumps(counts,ensure_ascii=False))
