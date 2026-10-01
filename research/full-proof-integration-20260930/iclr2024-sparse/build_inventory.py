"""Source-checked full-paper inventory. Run from the project root."""
import json
import hashlib
from pathlib import Path
from collections import Counter

BASE = Path('research/full-proof-integration-20260930/iclr2024-sparse')
PDF = Path('research/paper-survey-20260930/recent/pdf/iclr2024-sparse.pdf')
PAGES = json.loads(Path('research/paper-survey-20260930/recent/text/iclr2024-sparse.pages.json').read_text())
SOURCE = 'src-iclr2024-sparse-main'
entries = []

def entry(key, label, title, kind, statement_pages, proof_pages=None, section='', equations=None,
          aliases=None, occurrences=None, merge=None, external=None, issues=None, note='', target=False):
    eid = 'iclr2024-sparse-' + key
    occ = occurrences or [{'source_id': SOURCE, 'pdf_pages': statement_pages, 'role': 'statement', 'section': section}]
    if proof_pages:
        occ += [{'source_id': SOURCE, 'pdf_pages': proof_pages, 'role': 'proof', 'section': section}]
    refs = []
    for p in sorted(set(statement_pages + (proof_pages or []))):
        refs.append({'source_id': SOURCE, 'pdf_page': p,
                     'text_path': str(BASE / 'evidence/source-text' / f'p{p:02d}.txt'),
                     'image_path': str(BASE / 'evidence/pages' / f'page-{p:02d}.png') if (BASE / 'evidence/pages' / f'page-{p:02d}.png').exists() else None})
    entries.append(dict(id=eid, original_label=label, aliases=aliases or [], title=title, kind=kind,
        statement_location={'source_id':SOURCE,'pdf_pages':statement_pages,'section':section,'equation_labels':equations or []},
        proof_range={'source_id':SOURCE,'pdf_pages':proof_pages or [],'start_pdf_page':min(proof_pages) if proof_pages else None,
                     'end_pdf_page':max(proof_pages) if proof_pages else None,'section':section,'scope':'complete_source_proof' if proof_pages else 'no_local_proof'},
        occurrences=occ, merge_id=merge or eid, external=external or [], evidence=refs,
        classification_reason=note, proof_target=target, related_issue_ids=issues or [],
        review_status='agent_reviewed', user_review_status='pending'))

entry('definitions', 'Eq. (1)', '掩码、去基线输出与 Harsanyi 交互定义', 'definition', [3], equations=['1'], note='u=g0；空集交互为0，输入基线原符号b与规范输出基线b不同。')
entry('desiderata', 'Section 3.1 (1)–(3)', '稀疏性、普遍匹配、逐样本迁移三个评价标准', 'desiderata_and_empirical_observation', [3,4], note='本段列标准并外引经验发现，不把三个标准计作三个已证明定理。')
entry('reconstruction', 'Theorem 1', '所有掩码输出的去基线重构', 'numbered_theorem', [4,15], [15], '3.1 / B.1', ['7'], external=['Ren et al. (2023a)'], target=True,
      merge='iclr2024-sparse-reconstruction', note='正文与附录重述同一全量掩码命题；A.1(1)是全输入特例。')
entries[-1]['related_issue_ids'].append('sparse-issue-reconstruction-index')
entry('salient-approximation', 'Section 3.1 unnumbered', '仅保留显著交互的近似式', 'unnumbered_inference', [2,4], section='1 / 3.1', target=True, note='依重构给近似，但未给总遗漏误差的定量界；原文≈不能换成未经授权的界。')
entry('taylor-expansion', 'Eq. (2)', '在输入基线的无限多元 Taylor 展开', 'analytic_representation', [5], equations=['2'], issues=['sparse-issue-taylor-validity'], note='不是一般光滑函数恒等式；与Lemma1共享收敛/解析前提疑点。')
entry('assumption-1alpha', 'Assumption 1-α', '高于 M 阶交互为零', 'assumption', [5,16], section='3.2 / B.2', note='这是稀疏证明前提，不能记为无条件结论。')
entry('assumption-1beta', 'Assumption 1-β', '全空间高于 M 阶导数为零', 'assumption', [5], section='3.2', note='量词覆盖所有展开点b与多重指标；原文还提ReLU有限差分但未给相应推论证明。')
entry('lemma1', 'Lemma 1', '按变量支撑分组的 Taylor 交互表达式', 'numbered_lemma', [15], [15,16], 'B.2', ['8','9','10','11','12','13'], external=['Ren et al. (2023c) similar proof','Grabisch & Roubens (1999) uniqueness','Ren et al. (2023a) uniqueness'],
      issues=['sparse-issue-taylor-validity','sparse-issue-zero-power'], target=True, note='作者先定义候选再以全掩码重构唯一性识别；来源全部数学公式需保真。')
entry('derivative-cutoff', 'Assumption 1-β ⇒ Assumption 1-α', '由导数阶数推出交互阶数截断', 'unnumbered_proved_implication', [5,16], [16], 'B.2', ['14','15'], target=True, note='此推论使用Lemma1；全空间高阶导数为零可支持有限Taylor展开，但不能因此宣称一般Lemma1已无问题。')
entry('assumption2', 'Assumption 2 (Monotonicity)', '按掩码阶数的平均输出单调性', 'assumption', [6], section='3.2', note='平均单调不等于每对嵌套掩码的逐点单调。')
entry('assumption3', 'Assumption 3', '平均输出的多项式下界', 'assumption', [7], section='3.2', note='p>0；m=0时比例0/0未界定，正文使用m≥1。记录边界，不自动补量词。')
entry('order-statistics', 'A^(k), η^(k), R^(k)', '阶交互总和、抵消比例与显著交互计数', 'definition', [7,8], section='3.2', equations=['3','6'], issues=['sparse-issue-eta-zero'], note='η分母为绝对交互总强度；总强度或η为零时除法推导需单独处理。')
entry('lemma2', 'Lemma 2', '平均掩码输出的组合系数表达式', 'numbered_lemma', [16], [17], 'B.3', ['16','17','18','19','20','21','22','23','24','25','26','27'], target=True,
      note='M≤m≤n；使用1-α和I(∅)=0。组合计数过程属于同一引理，不独立抬高目标数。')
entry('lemma3', 'Lemma 3', '连续阶数的组合系数矩阵满列秩', 'numbered_lemma', [17], [17,18], 'B.3', ['28','29','30','31','32','33','34','35','36'], target=True,
      issues=['sparse-issue-determinant-sign','sparse-issue-lemma3-copied-row'], note='结论满秩与作者行列式值不同层次；Eq35/36漏交错符号不自动判引理结论为假。')
entry('theorem2', 'Theorem 2', '阶交互总效应的 n 进制表达与 δ 界', 'numbered_theorem', [7,18,19], [19,20], '3.2 / B.3', ['3','4','5','37','38','39','40','41','42','43','44','45','46','47','48','49','50','51','52','53'], target=True,
      issues=['sparse-issue-theorem2-zero-output','sparse-issue-theorem2-empty-G','sparse-issue-theorem2-m0-range','sparse-issue-theorem2-p-under-one','sparse-issue-T2-parameter-domain'], note='正文与附录仅重述；大O解读另记而不扩大定理量词。')
entry('asymptotic-claim', 'Section 3.2 unnumbered', 'O(n^(p+δ)) 及相比组合数稀疏的解释', 'unnumbered_asymptotic_inference', [7,8], section='3.2', target=True,
      issues=['sparse-issue-asymptotic-sparsity'], note='δ、η、M、p对n的依赖未给统一控制；记录原解释，不能以有限n界冒充渐近稀疏定理。')
entry('theorem3', 'Theorem 3', '显著 k 阶交互数的上界', 'numbered_theorem', [8,20], [20,21], '3.2 / B.4', ['6','54','55','56','57','58','59','60'], target=True,
      aliases=['B.4 printed Theorem 6'], issues=['sparse-issue-eta-zero'], note='B.4标题明确Theorem3，p20重述误编号Theorem6；归并一次，和B.7真正Theorem6分开。')
for k,title in [('efficiency','效率'),('linearity','线性'),('dummy','虚设变量'),('symmetry','对称'),('anonymity','匿名性'),('recursive','递归差分'),('distribution','纯交互分布')]:
    i=['efficiency','linearity','dummy','symmetry','anonymity','recursive','distribution'].index(k)+1
    entry('axiom-'+k, f'A.1 ({i})', title+'性质', 'listed_property_no_local_proof', [14], section='A.1',
          external=['Harsanyi (1963)'] if i==1 else (['Sundararajan et al. (2020) interaction functions'] if i==7 else []),
          merge='iclr2024-sparse-reconstruction' if i==1 else None, target=True,
          note='此正式版只列性质，没有逐条原作者证明；由CVPR共享证明做独立项目说明。' + ('T=∅时u_T不再去基线，需保留作用域差异。' if i==7 else ''))
entry('lemma4', 'Lemma 4', '边际收益的交互展开', 'numbered_lemma', [21], [21], 'B.5', target=True, note='T与环境S不相交；T=∅仍按差分定义可写，但u空集项须保留中心化。')
entries[-1]['related_issue_ids'].append('sparse-issue-marginal-free-L')
entry('theorem4', 'Theorem 4', 'Shapley 值按交互等分', 'numbered_theorem', [4,14,21], [22,23], 'A.2 / B.5', external=['Harsanyi (1963)','Shapley (1953)'], target=True,
      issues=['sparse-issue-beta-exponent','sparse-issue-beta-empty-L'], note='p4脚注是相同公式；作者完整求和与Beta路线在p22–23。结论与路线问题分别呈现。')
entry('theorem5', 'Theorem 5', 'Shapley 交互指标的交互展开', 'numbered_theorem', [14,23], [23,24,25], 'A.2 / B.6', external=['Ren et al. (2023a)','Grabisch & Roubens (1999)'], target=True,
      issues=['sparse-issue-beta-exponent','sparse-issue-beta-empty-L'], note='使用Lemma4和Theorem4中的同一权重恒等式。')
entry('theorem6', 'Theorem 6', 'Shapley–Taylor 指标的分段交互展开', 'numbered_theorem', [14,25], [25,26,27], 'A.2 / B.7', external=['Ren et al. (2023a)','Sundararajan et al. (2020)'], target=True,
      issues=['sparse-issue-beta-exponent','sparse-issue-beta-empty-L'], note='|T|<k、=k、>k三分支完整登记；最大阶k应在1至n间。')
entries[-1]['related_issue_ids'].append('sparse-issue-STI-free-S')
entry('noise-linearity', 'Scenario 1, unnumbered', '掩码输出噪声的交互线性分解', 'unnumbered_algebraic_derivation', [8], section='3.3', target=True, note='Iε对ε中心化；此线性恒等式独立成立。')
entry('noise-variance', 'Scenario 1, unnumbered', '噪声交互方差放大 2^|S| 倍', 'unnumbered_probability_claim', [8,9], section='3.3', target=True,
      issues=['sparse-issue-noise-variance'], note='fully random未明确独立同方差；I(∅)=0，空集不可套该方差式。')
entry('parity-mask', 'Scenario 2', '按保留变量数奇偶的交互符号', 'unnumbered_example_derivation', [9], section='3.3', target=True,
      issues=['sparse-issue-parity-empty'], note='原文偶数时u(S)=−1包含空集，与u(∅)=0有定义冲突。')
entry('or-density', 'Scenario 3', '高阶 OR 产生多项 AND 交互的讨论', 'qualitative_mathematical_claim', [9], section='3.3', target=False, note='本段没有定量公式或证明；与D.2的正式OR定义关联。')
entry('periodic-density', 'Scenario 4', '正弦输出交互不稀疏的示意', 'qualitative_mathematical_claim', [9], section='3.3', target=False, note='未给xi范围/阈值，不能把所有正弦样本不稀疏当成已证全称命题。')
entry('parity-task', 'Scenario 5 / E.3', '奇偶分类任务的大 p 经验观察', 'empirical_observation', [9,32], section='3.3 / E.3', note='100%训练准确率及p区间是实验结果。')
entry('transfer-inference', 'Section 4 unnumbered', '由稀疏与普遍匹配推逐样本迁移的反证论述', 'unnumbered_contradiction_argument', [9], section='4', target=True,
      issues=['sparse-issue-transfer'], note='未提供全模型模式总数上界；单样本稀疏不蕴含样本间支撑重叠。')
entry('or-reverse', 'D.2 unnumbered', 'OR 交互与反向掩码 AND 交互的关系', 'unnumbered_algebraic_inference', [29], section='D.2', equations=['61'], target=True, external=['Li & Zhang (2023a)'], note='原文为反向掩码的概念说明；精确符号含负号，规范映射须显式。')
entry('and-or-matching', 'Eq. (62)', 'AND–OR 分解的全掩码匹配', 'external_result_no_local_proof', [29], section='D.2', equations=['62'], target=True, external=['Li & Zhang (2023a)'], note='本篇没有展开证明；与Generalizable正式结果对齐后方可复用。')
entry('and-or-optimization', 'Eq. (63)', '稀疏 AND–OR 与去噪的优化定义', 'algorithm_description', [29], section='D.2', equations=['63'],
      issues=['sparse-issue-decomposition-notation'], note='原文两个u_and与去噪后的两次+γ保真记录；目标式不保证求得全局稀疏解。')
entry('threshold-discussion', 'Appendix F', '阈值以下交互多为精确零的解释', 'heuristic_empirical_claim', [33], section='F', note='作者承认不能排除小而非零交互，无概率模型或数值定理；不属于严格证明。')
entry('monotonicity-example', 'Appendix H', '五个二进制变量的平均单调例', 'worked_example', [34], section='H', target=True, issues=['sparse-issue-example-H-arithmetic'], note='作者列完整二阶/三阶各10个值；原三阶末项0与均值1.8有算术错，正确为1和1.9。只验证该例，不代表Assumption2全称证明。')
entry('sampling-complexity', 'Appendix I', '每阶抽 t 个掩码的均值估计及 O(nt) 代价', 'unnumbered_algorithmic_derivation', [34], section='I', target=True, note='是模型调用次数估计，无估计置信区间；抽样估计不等于严格认证假设。')
entry('experiments', 'Figures 2–14 / Tables 1–2', '经验稀疏性、均值单调与 p 数值', 'empirical_observation', [3,4,5,6,7,8,27,28,29,30,31,32,33], section='3 / C / D / E', note='实验图表和参数完整归类；不冒充证明。')
entry('related-work', 'Section 2', '外引既有数学与经验结果', 'external_background_no_local_proof', [2,3], section='2', note='综述背景，不把每个被引用论文的证明并入本篇目标。')

topics = {
1:('Abstract / 1','动机与三条件摘要；无独立证明'),2:('1 / 2','示意、近似式与外引背景'),3:('2 / 3.1','Eq1定义、中心化、图2经验结果'),
4:('3.1','三个标准、Thm1、Thm4脚注及近似解释'),5:('3.1 / 3.2','实验图3、Taylor Eq2、Assumptions1α/1β'),
6:('3.2','Assumption2、经验高阶与均值单调'),7:('3.2','Assumption3、Thm2及η定义'),8:('3.2 / 3.3','Thm3、两抵消情况、噪声线性与方差'),
9:('3.3 / 4 / 5','奇偶、OR、周期示例及迁移反证论述'),10:('References','复现声明与参考文献；无证明'),11:('References','参考文献；无证明'),
12:('References','参考文献；无证明'),13:('References','参考文献；无证明'),14:('A.1 / A.2','七条性质、Thm4–6陈述；无性质逐条原证明'),
15:('B.1 / B.2','Thm1完整证明、Lemma1陈述/证明开始'),16:('B.2 / B.3','Lemma1证明结束、1β⇒1α完整证明、Lemma2陈述'),
17:('B.3','Lemma2完整证明、Lemma3陈述/证明开始'),18:('B.3','Lemma3证明结束、Thm2陈述开始'),19:('B.3','Thm2陈述续、n进制展开与两分支'),
20:('B.3 / B.4','Thm2证明结束、Thm3误标Thm6与证明开始'),21:('B.4 / B.5','Thm3证明结束、Lemma4完整证明、Thm4重述'),
22:('B.5','Thm4有限求和/计数/Beta表达'),23:('B.5 / B.6','Thm4证明结束、Thm5陈述/定义'),24:('B.6','Thm5求和/Beta计算'),
25:('B.6 / B.7','Thm5结束、Thm6定义与低阶分支'),26:('B.7','Thm6临界阶求和与Beta第一项'),27:('B.7 / C.1','Thm6结束、实验设置'),
28:('C / D.1','语义部件与LLM实验设置；无严格证明'),29:('D.1 / D.2','OR定义、反向AND、Eq62匹配、Eq63优化与去噪'),
30:('E.1 / E.2','图7–9经验高阶近零；无证明'),31:('E.2','图10–11经验计数/上界；无证明'),32:('E.2 / E.3 / E.4','图12、奇偶实验与部件大小实验；无证明'),
33:('E.4 / E.5 / F','图13–14与阈值启发解释；无严格证明'),34:('G / H / I','影响展望、完整五变量例、抽样复杂度推导')}

page_audit=[]
for page in range(1,35):
    related=[e['id'] for e in entries if any(page in o['pdf_pages'] for o in e['occurrences'])]
    page_audit.append({'source_id':SOURCE,'pdf_page':page,'section':topics[page][0],
                       'finding':topics[page][1],'entry_ids':related,'text_checked':True,
                       'image_checked':page in [15,18,19,21,22,26,34], 'review_status':'agent_reviewed'})
targets={e['merge_id'] for e in entries if e['proof_target']}
report={
 'schema_version':'full-paper-inventory-1.0','paper_id':'iclr2024-sparse',
 'title':'Where We Have Arrived in Proving the Emergence of Sparse Interaction Primitives in DNNs',
 'sources':[{'source_id':SOURCE,'path':str(PDF),'sha256':hashlib.sha256(PDF.read_bytes()).hexdigest(),'pdf_page_count':34,'version':'ICLR 2024 published conference paper','supplement_status':'appendices A–I included in this formal PDF'}],
 'review_scope':'all 34 PDF pages, main text and appendices A–I, formal version only',
 'review_status':'agent_reviewed','user_review_status':'pending','page_audit':page_audit,'entries':entries,
 'counts':{'source_pages':34,'page_audits':len(page_audit),'entries':len(entries),'unique_numbered_theorems':6,'unique_numbered_lemmas':4,
           'numbered_statement_occurrences':'Theorem1/2/3/4/5/6 repetitions and B.4 typo are merged by mathematics, not label',
           'listed_properties':7,'unique_proof_targets':len(targets),'by_kind':dict(Counter(e['kind'] for e in entries))},
 'counting_policy':'Numbered results, listed mathematical properties, actual unnumbered deductions, external matching result and worked example are individually reviewable targets; assumptions, definitions, experiments, qualitative scenarios and heuristics remain visible but are not strict-proof targets. Efficiency merges with reconstruction. A target is not a completion claim.',
 'evidence_policy':'Complete extracted source text of every page is preserved separately; source images for all appendix-proof pages are preserved. Formula-critical images are independently inspected before issue confirmation.'}
(BASE/'inventory.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
lines=['# ICLR 2024 Sparse：正式全篇数学清单','',f"正式 PDF 34 页，已逐页审查。6 个编号定理、4 个编号引理；7 条仅列述性质。清单共 {len(entries)} 项，按声明与推导归并后 {len(targets)} 个可审查目标；定义、假设、实验、定性说明另分类。该数字是覆盖分母，不是已证明或形式化完成数。",'',
       '正文重述与附录证明是同一目标；B.4 的 `Theorem 6` 是正文 Theorem 3 的编号别名，B.7 的真正 Theorem 6 单列。A.1 效率性质归并到 Theorem 1。用户审核均待定。','',
       '| ID | 原编号 | 类型 | 陈述 PDF 页 | 原证明 PDF 页 | 归并 |','| --- | --- | --- | --- | --- | --- |']
for e in entries:
    lines.append(f"| {e['id']} | {e['original_label']} | {e['kind']} | {','.join(map(str,e['statement_location']['pdf_pages']))} | {','.join(map(str,e['proof_range']['pdf_pages'])) or '本篇无展开证明'} | {e['merge_id']} |")
lines += ['','## 逐页审查','', '| PDF 页 | 章节 | 检查结论 |','| --- | --- | --- |']
for p in page_audit:lines.append(f"| {p['pdf_page']} | {p['section']} | {p['finding']} |")
lines += ['','## 证据与边界','','原作者各页完整文本在 `evidence/source-text/pXX.txt`，正式图像在 `evidence/pages/page-XX.png`。完整正文/证明的数学转录将在 `math/author-transcript.tex.md` 与 content.json 对齐；本清单只登记范围，不把摘要命名为原证明全文。','',
          '数学疑点保留在对应条目；原式、核图、反例与影响单独记录。即使某行符号错误，也分别评估中间步骤和最终结论。最新用户授权 proof_only_granted：直接修复错误证明并标原错处，原命题及假设不改；错误原命题与反例单独列出。']
(BASE/'inventory.md').write_text('\n'.join(lines)+'\n')
print(json.dumps(report['counts'],ensure_ascii=False,indent=2))
