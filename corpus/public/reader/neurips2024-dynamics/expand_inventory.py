import json
from pathlib import Path
D=Path('corpus/public/reader/neurips2024-dynamics');inv=json.loads((D/'inventory.json').read_text());meta=json.loads((D/'paper-metadata.json').read_text());sid=inv['sources'][0]['source_id']
new=[('dyn-efficiency','A(1) Efficiency axiom','效率公理','external_theorem'),('dyn-linearity','A(2) Linearity axiom','线性公理','external_theorem'),('dyn-dummy','A(3) Dummy axiom','Dummy 公理','external_theorem'),('dyn-symmetry','A(4) Symmetry axiom','对称公理','external_theorem'),('dyn-anonymity','A(5) Anonymity axiom','匿名公理','external_theorem'),('dyn-recursion','A(6) Recursive axiom','递归公理','external_theorem'),('dyn-distribution','A(7) Interaction distribution axiom','纯交互分布公理','external_theorem'),('dyn-cutoff','B Condition 1','最高交互阶数条件','assumption'),('dyn-mask-monotonic','B Condition 2','掩码平均输出单调条件','assumption'),('dyn-mask-polynomial','B Condition 3','掩码平均输出多项式界条件','assumption'),('dyn-uniqueness','Appendix D','交互系数唯一性','external_theorem')]
inv['entries']=[e for e in inv['entries'] if e['id'] not in ['dyn-properties','dyn-shapley']]
for i,label,title,kind in new:
 ps=[15] if i=='dyn-uniqueness' else [14,15] if i=='dyn-mask-polynomial' else [14];loc={'source_id':sid,'pdf_pages':ps,'section':'D' if i=='dyn-uniqueness' else 'A' if 'axiom' in label else 'B'}
 inv['entries'].append(dict(id=i,original_label=label,title=title,kind=kind,statement_location=loc,proof_location=dict(loc,pdf_pages=[]),appearances=[loc],proof_target=kind=='external_theorem',merge_target_id=i if kind=='external_theorem' else None,non_proof_reason='' if kind=='external_theorem' else '原文明确列出的外引稀疏性假设，不是须独立证明的结论。',external_reference=True,determination_basis='每个独立原性质/条件分别登记，不因同在附录合并陈述。'))
for a in inv['page_audit']:
 a['entry_ids']=[i for i in a['entry_ids'] if i not in ['dyn-properties','dyn-shapley']]+[e['id'] for e in inv['entries'] if e['id'] in [x[0] for x in new] and a['pdf_page'] in e['statement_location']['pdf_pages']]
inv['proof_targets']=[e['id'] for e in inv['entries'] if e.get('proof_target')]
meta['results']=[e['id'] for e in inv['entries']]
for f,d in [('inventory.json',inv),('paper-metadata.json',meta)]: (D/f).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
print(len(inv['entries']))
