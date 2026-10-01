from pathlib import Path
import json,hashlib
R=Path.cwd();base=R/'corpus/public/reader'
# id,label,title,kind,statement pages,proof pages,section
DATA={
'neurips2024-dynamics':[
('dyn-interaction-definition','Eq.(2)','AND/OR 交互与分解','definition',[3,4],[],'3.1'),
('dyn-sparsity','Theorem 1','外引稀疏性','external_theorem',[4,14,15],[],'3.1; B'),
('dyn-universal','Theorem 2; Eq.(3)','任意掩码 AND/OR 重构','theorem',[4],[16,17,18],'3.1; F.1'),
('dyn-properties','Seven properties; Appendix A','AND 七条性质','external_properties',[4,5,14],[],'3.1; A'),
('dyn-salience','Threshold and normalized strength','显著性与阶数归一化','definition',[5,24,27,28],[],'3.2; G.3; J.3'),
('dyn-taylor','Lemma 3; Eq.(19)','Taylor 支持交互展开','lemma',[18],[18,19],'F.2'),
('dyn-trigger-representation','Eq.(6); Eq.(7)','Taylor 触发函数表示','derivation',[6,7],[19,20],'3.3.1; F.2'),
('dyn-noisy-output','Lemma 1; Eq.(37)–(40)','输出噪声与交互方差','lemma',[7],[20,21],'3.3.1; F.3'),
('dyn-regression-definition','Eq.(8); Eq.(9); Assumption 1','掩码回归模型及独立噪声假设','definition',[7,8],[21],'3.3.1; F.4'),
('dyn-regression','Theorem 3; Eq.(10)','噪声回归的唯一最优权重','theorem',[8],[21,22],'3.3.1; F.4'),
('dyn-binary-trigger','Lemma 2; Eq.(52)–(59)','掩码触发值恒为二值','lemma',[8],[22],'3.3.2; F.5'),
('dyn-equal-order','Theorem 4; Eq.(60)–(64)','同阶行向量等范数','theorem',[9],[23],'3.3.2; F.6'),
('dyn-order-monotonic','Proposition 1','阶数范数比随噪声单调','proposition',[9],[],'3.3.2'),
('dyn-zero-noise','Theorem 5','零噪声恢复全部权重','theorem',[9],[24],'3.3.2; F.7'),
('dyn-first-phase','Section 3.3.3','第一阶段独立初始化的机制','argument',[10,25],[],'3.3.3; H; I'),
('dyn-complement','Eq.(12)–(16)','OR 作为补集 AND 变换','derivation',[15,16],[15,16],'E'),
('dyn-shapley','Appendix C','外引归因指标关系','external_properties',[15],[],'C'),
('dyn-extraction','Eq.(4); Appendix G.3','稀疏分解优化与提取算法','algorithm',[4,24,25],[],'3.1; G.3'),
('dyn-experiments','Figures 1–9; J','两阶段动态与经验检验','empirical',[1,2,3,4,5,6,9,10,24,25,26,27,28,29],[],'Main; G; J')],
'icml2023-bayesian':[
('bnn-posterior','Eq.(1); Eq.(2)','均场变分 BNN 与替代模型','definition',[3,4,5,23,24,25],[],'2.1; H'),
('bnn-interaction','Eq.(3); Eq.(4)','Harsanyi 交互与忠实重构','derivation',[3,4],[15],'2.1; G.1'),
('bnn-sparsity','Concept emergence; Appendix B','稀疏概念外引条件','external_properties',[3,4,12],[],'2.1; B'),
('bnn-taylor','Lemma 2.1; Eq.(20)','Taylor 支持展开','lemma',[5],[15,16],'2.2; G.1'),
('bnn-reference','Reference and small perturbation','基线距离与扰动符号','definition',[5,6,7,16,17],[],'2.2; G.2; G.3'),
('bnn-lowest','Theorem 2.2; Eq.(27)–(32)','最低阶项扰动均值与方差','theorem',[6],[16,17],'2.2; G.2'),
('bnn-product','Proposition G.1','独立乘积矩公式','proposition',[16],[16],'G.2'),
('bnn-general-moments','Theorem 2.3; Eq.(33)–(39)','任意阶项的扰动矩','theorem',[6],[17,18],'2.2; G.3'),
('bnn-growth','Theorem 2.4; Eq.(40)–(46)','嵌套支持方差比增长','theorem',[6,7],[18,19,20],'2.2; G.4'),
('bnn-trigger','Eq.(12)–(14)','归一化概念触发函数','definition',[7],[],'2.3'),
('bnn-regression','Theorem 2.5; Eq.(47)–(59)','独立特征回归权重比例','theorem',[7],[20,21,22],'2.3; G.5'),
('bnn-scaling','Theorem 2.6; Eq.(60)','概念尺度的均值方差界','theorem',[8],[22],'2.3; G.6'),
('bnn-objective','Eq.(15)','简化学习目标','definition',[7,8],[],'2.3'),
('bnn-metrics','Eq.(5)–(7); Eq.(10)–(11)','概念强度及扰动指标','definition',[4,6,7],[],'2.1; 2.2'),
('bnn-generalization','Appendix F','概念泛化指标与方差解释','definition',[13,14],[],'F'),
('bnn-experiments','Figures 1–6; D; E; H','BNN 复杂度与替代模型实证','empirical',[1,2,4,5,6,7,8,9,13,14,23,24,25],[],'Main; D; E; H')],
'neurips2023-difficulty':[
('diff-interaction','Eq.(1)','Harsanyi 交互定义','definition',[3,4],[],'2.1'),
('diff-universal','Theorem 1; Eq.(2)','外引任意掩码忠实重构','external_theorem',[4],[],'2.1'),
('diff-sparsity','Salient concepts; Appendix F','概念稀疏性外引与实证','external_properties',[4,16],[],'2.1; F'),
('diff-reference','Eq.(3)','输入基线距离与小扰动','definition',[4,5],[],'2.2'),
('diff-taylor','Theorem 2; Eq.(4)','Taylor 支持展开','theorem',[4,5],[17,18],'2.2; G.1'),
('diff-moments','Theorem 3; Eq.(5)–(7)','Gaussian 扰动下概念矩','theorem',[5],[18,19],'2.2; G.2'),
('diff-product','Proposition 1','独立乘积矩公式','proposition',[18],[18],'G.2'),
('diff-trigger-definition','Eq.(8); Eq.(9)','概念触发函数定义','definition',[6],[],'2.3'),
('diff-binary','Theorem 4; Eq.(19)–(24)','掩码输入的二值激活','theorem',[6],[20],'2.3; G.3'),
('diff-multiorder','Eq.(25); Appendix G.4','多阶交互的概念关系','derivation',[20],[20,21],'G.4'),
('diff-regression','Eq.(26)–(28); Appendix G.5','方差与回归学习难度','derivation',[21],[21],'G.5'),
('diff-training-metrics','β; sim; A; Eq.(10)','学习速率与结构相似度指标','definition',[6,7,8,9,22],[],'2.3; 3; H'),
('diff-experiments','Figures 1–7; D; E; F','复杂度学习实证','empirical',[1,2,4,5,6,7,8,9,10,15,16,22],[],'Main; D; E; F; H')]
}
sections={
'neurips2024-dynamics':['Abstract; 1','1; 2','2; 3.1','3.1','3.2','3.2; 3.3.1','3.3.1','3.3.1; 3.3.2','3.3.2','3.3.3; 4','References','References','References','A; B','B; C; D; E','E; F.1','F.1','F.1; F.2','F.2','F.2; F.3','F.3; F.4','F.4; F.5','F.6','F.7; G.1; G.2; G.3','G.3; G.4; H; I','J.1','J.1; J.2; J.3','J.3','J.3','Checklist 1–2','Checklist 2–3','Checklist 3–5','Checklist 5–7','Checklist 8–10','Checklist 11–13','Checklist 13–15'],
'icml2023-bayesian':['Abstract; 1','1; 2','2.1','2.1','2.1; 2.2','2.2','2.2; 2.3','2.3; 3','3; References','References','References','A; B; C','D; E; F','F','G.1','G.1; G.2','G.2; G.3','G.3; G.4','G.4','G.4; G.5','G.5','G.5; G.6','H','H','H'],
'neurips2023-difficulty':['Abstract; 1','1','1; 2.1','2.1; 2.2','2.2','2.3','2.3','2.3','3','3; 4','References','References','References','References','A; B; C; D; E','E; F','G.1','G.1; G.2','G.2','G.3; G.4','G.4; G.5','H']}
allp=json.loads((R/'research/paper-survey-20260930/combined-papers.json').read_text())
for pid,rows in DATA.items():
 d=base/pid;pages=json.loads((d/'sources/pages.json').read_text());p=next(p for p in allp if (p.get('local_pdf') or '').endswith({'neurips2024-dynamics':'neurips2024-dynamics.pdf','icml2023-bayesian':'icml2023-bayesian.pdf','neurips2023-difficulty':'neurips2023-difficulty-main.pdf'}[pid]))
 sid='src-'+pid+'-formal';vid='ver-'+pid+'-formal';source=dict(id=sid,source_id=sid,version_id=vid,label='正式会议PDF（含附录）',kind='main_with_appendix',role='formal_main_with_included_appendix',path=str((d/'sources/formal.pdf').relative_to(R)),local_path=str((d/'sources/formal.pdf').relative_to(R)),sha256=hashlib.sha256((d/'sources/formal.pdf').read_bytes()).hexdigest(),total_pages=len(pages),page_count=len(pages),pages=len(pages),url=p['pdf_url'],visibility='public',publication_status='published')
 entries=[]
 for i,label,title,kind,sp,pp,sec in rows:
  loc=lambda ps:dict(source_id=sid,pdf_pages=ps,section=sec)
  entries.append(dict(id=i,original_label=label,title=title,kind=kind,statement_location=loc(sp),proof_location=loc(pp),appearances=[loc(sp)]+([loc(pp)] if pp else []),proof_target=kind in ['theorem','lemma','proposition','derivation','external_theorem','external_properties','argument'],merge_target_id=i if kind in ['theorem','lemma','proposition','derivation','external_theorem','external_properties','argument'] else None,non_proof_reason='' if kind in ['theorem','lemma','proposition','derivation','external_theorem','external_properties','argument'] else '原定义、明确假设、优化问题定义或经验材料；没有独立普遍数学断言作为证明目标。',external_reference=kind.startswith('external'),determination_basis='逐页核对正式正文、脚注及附录；原文重述不另计目标，定义/算法/经验与证明分别分类。'))
 audit=[];(d/'source-evidence').mkdir(exist_ok=True)
 for page in pages:
  k=page['pdf_page'];ep=d/'source-evidence'/f'page-{k:02d}.txt';ep.write_text(page['text']);ids=[i for i,l,t,kind,sp,pp,se in rows if k in sp+pp];sec=sections[pid][k-1]
  cls='proof' if any(k in r[5] for r in rows) else 'references' if sec=='References' else 'publication_checklist' if sec.startswith('Checklist') else 'definitions_and_empirical' if ids else 'background_and_scope'
  audit.append(dict(source_id=sid,pdf_page=k,section=sec,classification=cls,entry_ids=ids,review_status='agent_reviewed',evidence_path=str(ep.relative_to(R)),note='原文页全文检查；无独立证明的页保留分类，图表经验观察不计形式定理。'))
 inv=dict(schema_version=1,paper_id=pid,title=p['title'],sources=[source],review_scope=f'All {len(pages)} physical pages of the official published PDF, including appendices, footnotes, equations and unnumbered derivations.',page_audit=audit,entries=entries,proof_targets=[e['id'] for e in entries if e['proof_target']],review_status='agent_reviewed')
 (d/'inventory.json').write_text(json.dumps(inv,ensure_ascii=False,indent=2)+'\n');(d/'inventory.md').write_text('# '+p['title']+'：逐页数学覆盖\n\n'+f'正式文件 {len(pages)} 页，SHA256 `{source["sha256"]}`。源文件、原文出现与合并目标分开记录。\n\n'+'\n'.join(f'- PDF {a["pdf_page"]}: {a["section"]}；{a["classification"]}；'+', '.join(a['entry_ids']) for a in audit)+'\n\n'+'\n'.join(f'- `{e["id"]}` / {e["original_label"]}: 陈述 {e["statement_location"]["pdf_pages"]}；证明 {e["proof_location"]["pdf_pages"]}；{e["kind"]}' for e in entries)+'\n')
 meta=dict(id=pid,title=p['title'],short_title={'neurips2024-dynamics':'Dynamics','icml2023-bayesian':'Bayesian Concepts','neurips2023-difficulty':'Concept Difficulty'}[pid],authors=p['authors'],venue=p.get('venue',p['publication']['venue']),year=p['year'],intro='完整正式论文数学范围；原陈述、原证明、项目重写与机器证据分别显示。',scope=f'正式 PDF 全部 {len(pages)} 页及已含附录。',version_id=vid,version_label=p['version'],visibility='public',publication_status='published',publication_url=p['source_url'],canonical_publication_key=p['source_url'],sources=[source],results=[r[0] for r in rows],translations={'en':{'intro':'Complete mathematical scope of the official publication, separating source statements/proofs, rewritten reasoning and machine evidence.','scope':f'All {len(pages)} pages of the official PDF and included appendices.'}})
 (d/'paper-metadata.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2)+'\n')
 print(pid,len(entries),len(audit))
