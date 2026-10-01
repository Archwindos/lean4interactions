"""Source-specific page inventory; every physical PDF page is retained."""
import json, hashlib
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
ROOT = BASE.parents[2]
def write(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2)+'\n')
def row(id, label, title, kind, pages, section, proof=(), external=False):
    return dict(id=id, original_label=label, title=title, kind=kind,
        statement_location=dict(pdf_pages=list(pages),section=section),
        proof_location=dict(pdf_pages=list(proof),section=section),
        appearances=[dict(pdf_pages=list(pages),section=section),dict(pdf_pages=list(proof),section=section)] if proof else [dict(pdf_pages=list(pages),section=section)],
        merged_target_id=id if kind in ['theorem','lemma','derivation','external_theorem','false_derivation','external_axiom','scope_claim'] else None,
        external_reference=external, determination_basis='正式PDF逐页阅读全文；定义、经验观察与数学论证分别分类。')

DATA={
'icml2023-harsanyinet':dict(
 sections=['Abstract; 1','1; 2; 2.1','2.2; 3; 3.1; 3.2','3.2','3.3','3.4; 4.1','4.1; 4.2','4.2','4.2; 5; References','References','References','A; B Theorem 2/3','B Theorem 3/4','B Theorem 4; C','C; D; E','E Setting 2; F.1','F.1–F.4','F.4–F.7','F.7–F.8','F.5 Figure 8','F.5 Figures 9–10','F.5 Figure 11'],
 classes=['background','background_and_definitions','definitions_and_derived_reconstruction','numbered_mathematical_statements','architecture_and_complexity','sparsity_scope_and_cnn','experiments_and_cnn_definition','experiments','conclusion_and_references','references','references','axioms_and_proofs','proofs','proofs','proofs_and_architecture','proof_and_experiments','experiments','experiments','conditional_game_derivation','figures','figures','figures'],
 entries=[
 row('hnet-shapley-definition','Definition 1; Eq.(1)','经典阶乘权重 Shapley 定义','definition',[2],'2.1'),
 row('hnet-centered-definition','Definition 2','中心化游戏及递归交互','definition',[3],'3.1'),
 row('hnet-reconstruction','Definition 2 aftermath','中心化交互精确重构输出差','derivation',[3],'3.1'),
 row('hnet-r1-r2','Requirements R1/R2','感受野依赖与缺变量灭活','definition',[4],'3.2'),
 row('hnet-shapley-dividend','Theorem 1; Eq.(3)','Shapley 等于交互均分','external_theorem',[4],'3.2',external='Harsanyi (1963)'),
 row('hnet-unit-interaction','Lemma 1','单一单元只贡献感受野交互','lemma',[4],'3.2; C',proof=[14,15]),
 row('hnet-readout-linearity','Theorem 2','线性读出交互是单元交互加权和','theorem',[4],'3.2; B',proof=[12]),
 row('hnet-forward-shapley','Theorem 3; Eq.(4)','一次前向传播的 Shapley 表达式','theorem',[4],'3.2; B',proof=[12,13]),
 row('hnet-runtime','Cost of computing; O(nM)','归因累加运算计数','derivation',[5],'3.3'),
 row('hnet-architecture','Eq.(5)–(8)','无偏置线性、AND gate、ReLU、感受野并集','definition',[5,15],'3.3; D'),
 row('hnet-architecture-r1-r2','Theorem 4','递归架构满足 R1/R2','theorem',[5],'3.3; B',proof=[13,14]),
 row('hnet-smooth-gate','Unnumbered tanh approximation','训练使用的光滑 AND 实现','definition',[5],'3.3'),
 row('hnet-sparsity-count','At most M; Eq.(9)','非零交互数量至多单元数；经验截断','derivation',[6],'3.4'),
 row('hnet-cnn-receptive','Setting 2','共享子节点的 CNN 通道具有同一感受野','derivation',[6,7],'4.1; E',proof=[16]),
 row('hnet-cnn-regroup','Setting 2 proof second half','向量化通道与标量通道交互等价','derivation',[7],'4.1; E',proof=[16]),
 row('hnet-axiom-linearity','A(1)','Shapley 线性公理','external_axiom',[12],'A',external='Young (1985); Weber (1988)'),
 row('hnet-axiom-dummy','A(2)','Shapley Dummy 公理','external_axiom',[12],'A',external='Young (1985); Weber (1988)'),
 row('hnet-axiom-symmetry','A(3)','Shapley 对称公理','external_axiom',[12],'A',external='Young (1985); Weber (1988)'),
 row('hnet-axiom-efficiency','A(4)','Shapley 效率公理','external_axiom',[12],'A',external='Young (1985); Weber (1988)'),
 row('hnet-conditional-attribution','F.8 unnumbered formula','外部变量固定时选定变量的条件 Shapley','derivation',[19],'F.8'),
 row('hnet-experiments','Tables 1–6; Figures 2–11','准确率、鲁棒性与交互经验稀疏性','empirical_observation',[6,7,8,9,16,17,18,19,20,21,22],'4; F'),
 row('hnet-external-sparsity','Ren et al. (2023b)','传统 DNN 稀疏性外引','external_claim',[6],'3.4',external='Ren et al. (2023b)')]),
'icml2024-layerwise':dict(
 sections=['Abstract; 1','1','2; 3.1','3.1; 3.2.1','3.2.1; 3.2.2','3.2.2 Eq.(6)–(7)','3.2.2 Eq.(8); 3.3','3.3 Eq.(9)–(10)','3.3; 4; References','References','References','A; B','B; C; D','D; E','F','G','H Table of metrics','I.1','I.1; I.2','J; K','L; M.1','M.1–M.4'],
 classes=['background','background_and_empirical_scope','definitions_and_reconstruction','numbered_statements','probe_definitions_and_experiments','metric_definitions','metric_derivation_and_experiments','definitions_and_combinatorial_derivation','conclusion_and_references','references','references','background_and_external_claims','attribution_and_complement_derivation','background','proof','proof_and_external_sparsity_argument','image_table_definition_duplicate','experiments','experiments','experiments','noise_empirical_argument_and_methods','methods_and_singleton_derivation'],
 entries=[
 row('layer-and-definition','Definition 3.1; Eq.(1)','原始 AND 交互定义','definition',[3,17],'3.1; H'),
 row('layer-and-reconstruction','Eq.(1) aftermath','AND 交互重构全部输出','derivation',[3],'3.1',proof=[15]),
 row('layer-decomposition','vand/vor and gamma','AND/OR 分量与可学习分解','definition',[3,4],'3.1'),
 row('layer-or-definition','Definition 3.2; Eq.(2)','非空 OR 交互与特设空集','definition',[4,17],'3.1; H'),
 row('layer-universal-matching','Theorem 3.3; Eq.(3),(14)–(17)','全部掩码输出的 AND/OR 精确匹配','theorem',[4],'3.1; F',proof=[15]),
 row('layer-salient-matching','Lemma 3.4; Eq.(4),(18)–(19)','少量显著交互普遍近似匹配','lemma',[4],'3.1; G',proof=[16]),
 row('layer-probe-definition','Eq.(5),(20)','线性 probe、logit 与受限确定性残差','definition',[5,20],'3.2.2; J'),
 row('layer-metric-definition','Eq.(6),(7),(9),(10),(21); H','显著集合、重叠/遗忘/新增、IoU及稳定度','definition',[5,6,7,8,17,21,22],'3.2.2; 3.3; H; L; M.4'),
 row('layer-strength-decomposition','Eq.(8)','阈值化强度的重叠/遗忘/新增分解','derivation',[7],'3.2.2'),
 row('layer-binomial-symmetry','Unnumbered binomial comparison','m阶与n−m阶候选交互数量相同','derivation',[8],'3.3'),
 row('layer-shapley-and-or','Appendix B Perspective 2','AND/OR交互均分给出Shapley','derivation',[13],'B'),
 row('layer-complement-duality','Eq.(11)–(13)','反转掩码状态的 OR/AND 对偶','derivation',[13],'C'),
 row('layer-or-sparsity-inheritance','Appendix C last paragraph','引用 AND 稀疏性推出 OR 稀疏性','scope_claim',[13],'C',external='Ren et al. (2024)'),
 row('layer-noise-ratio','Appendix L; Figure 12','噪声比例及高阶信号强度的经验说明','empirical_observation',[8,21],'3.3; L'),
 row('layer-singleton-merge','M.4 last paragraph','一阶 OR 与 AND 的贡献可以合并','derivation',[22],'M.4'),
 row('layer-experiments','Figures 1–12','稀疏性、分层变化、泛化与稳定性的经验结果','empirical_observation',[1,2,4,5,6,7,8,9,12,18,19,20,21,22],'1; 3; B; I–M'),
 row('layer-external-properties','Section 2 list','稀疏性、泛化、七条性质等外引论证','external_claim',[3],'2',external='Li & Zhang (2023); Ren et al. (2023a,2024); others')])}

for pid,d in DATA.items():
    out=BASE/pid
    candidates=json.loads((ROOT/'research/paper-survey-20260930/recent/formal-candidates.json').read_text())
    m=next(x for x in candidates if x['local_pdf'].endswith(pid+'.pdf'))
    source=dict(source_id='src-'+pid+'-formal',version_id='ver-'+pid+'-formal',path=str((out/'sources/formal.pdf').relative_to(ROOT)),sha256=hashlib.sha256((out/'sources/formal.pdf').read_bytes()).hexdigest(),page_count=22,pages=22,url=m['pdf_url'],role='formal_main_with_included_appendix')
    audits=[]
    for page,(sec,cl) in enumerate(zip(d['sections'],d['classes']),1):
        ids=[e['id'] for e in d['entries'] if page in e['statement_location']['pdf_pages']+e['proof_location']['pdf_pages']]
        audits.append(dict(source_id=source['source_id'],pdf_page=page,section=sec,classification=cl,entry_ids=ids,review_status='agent_reviewed',evidence_path=str((out/f'source-evidence/page-{page:02}.txt').relative_to(ROOT)),note='全文正文、脚注、公式、图表及附录检查；第17页表格另作图片核查。' if pid=='icml2024-layerwise' and page==17 else '阅读全文；经验结果未计作定理证明。'))
    targets=[e['id'] for e in d['entries'] if e['merged_target_id']]
    for e in d['entries']:
        for loc in [e['statement_location'],e['proof_location']]+e['appearances']:
            loc['source_id']=source['source_id']
    inv=dict(schema_version=1,paper_id=pid,title=m['title'],sources=[source],review_scope='All 22 physical pages of the formal proceedings PDF, including main text, appendices, footnotes and unnumbered mathematical derivations.',page_audit=audits,entries=d['entries'],proof_targets=targets,counts=dict(source_pages=22,audited_pages=22,inventory_entries=len(d['entries']),merged_targets=len(targets),numbered_results=5 if pid.startswith('icml2023') else 2),review_status='agent_reviewed',user_review_status='pending',completeness_note='First full page inventory. Semantic correctness and Lean verification are independent; external claims and empirical observations remain distinguished.')
    write(out/'inventory.json',inv)
    (out/'inventory.md').write_text('# '+m['title']+'：正式全文逐页清单\n\n来源SHA256：`'+source['sha256']+'`；审查22/22物理PDF页。\n\n|PDF页|章节|分类|数学条目|\n|---|---|---|---|\n'+''.join(f"|{a['pdf_page']}|{a['section']}|{a['classification']}|{', '.join(a['entry_ids']) or '无新数学目标'}|\n" for a in audits)+'\n## 去重条目\n\n'+''.join(f"- `{e['id']}`：{e['original_label']}，{e['kind']}，陈述页{e['statement_location']['pdf_pages']}，证明页{e['proof_location']['pdf_pages']}。\n" for e in d['entries']))
    reader_source=dict(source,id=source['source_id'],local_path=source['path'],label='正式会议PDF（含附录）',kind='main_with_appendix',total_pages=22,visibility='public',publication_status='published')
    meta=dict(id=pid,title=m['title'],short_title='HarsanyiNet' if pid.startswith('icml2023') else 'Layerwise Knowledge',authors=m['authors'],venue='ICML',year=m['year'],intro='正式会议论文完整数学范围；正文、附录和未编号推导均可检索。',scope='正式PDF全部22页；数学正确性、文字重写和形式化分别记录。',version_id=source['version_id'],version_label=m['version'],visibility='public',publication_status='published',publication_url=m['source_url'],canonical_publication_key=m['source_url'],sources=[reader_source],results=targets,translations=dict(en=dict(intro='Complete mathematical scope of the formal conference paper, including main text, appendices and unnumbered derivations.',scope='All 22 pages of the formal PDF; mathematical validity, rewritten proofs and Lean verification are recorded separately.')))
    write(out/'paper-metadata.json',meta)
    print(pid,len(d['entries']),len(targets),'pages',len(audits))
