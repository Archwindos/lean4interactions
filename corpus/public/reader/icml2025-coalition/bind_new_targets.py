import json
from pathlib import Path
P=Path(__file__).parent;d=json.loads((P/'content.json').read_text());rep=json.loads((P/'verification/report.json').read_text());api={r['name']:r for r in rep['declarations']}
for r in d['results']:
 k=r['id'].removeprefix('coalition-');names={'shapley-coefficient':'Harsanyi.Coalition.shapley_kernel','banzhaf-coefficient':'Harsanyi.Coalition.signed_half_superset','toy-support':'Harsanyi.Coalition.toy_and_support'}
 if k not in names:continue
 n=names[k];a=api[n];scope={'shapley-coefficient':'Equivalent factorial predecessor kernel compiled; explicit cardinality grouping into the displayed binomial indexed expression is a human adaptation, not a separate numeric-index theorem.','banzhaf-coefficient':'Entire signed superset coefficient identity, including empty L and R=L.','toy-support':'Finite sum of pure AND games compiled with arbitrary supports and weights. The binary coordinate product-to-indicator adapter is justified in the human proof and is not a separate actual-mask formal declaration.'}[k]
 ref={'declaration':n,'source_path':a['source_path'],'line':a['line'],'scope':'exact_signed_kernel' if k=='banzhaf-coefficient' else 'finite_kernel_with_human_paper_adaptation','explanation_md':{'shapley-coefficient':'真实前驱有限和核验；按基数归并至二项式指标写法仍为文字适配。','banzhaf-coefficient':'真实有符号上集权重完整恒等式，空集与相等边界均包含。','toy-support':'真实有限纯AND和的支撑公式；二进制坐标乘积到指示游戏的适配尚未另形式化。'}[k]}
 r['proof_steps'][0]['lean_refs']=[ref];r['translations']['en']['proof_steps'][0]['lean_refs']=[{**ref,'explanation_md':scope}]
 r['lean'].update(declarations=[n],scope=scope,step_map=[{'step_id':r['proof_steps'][0]['id'],**ref}])
 if k in ('toy-support','shapley-coefficient'):r['lean']['status']='partial_scope_verified'
(P/'content.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
c=json.loads((P/'verification/coverage.json').read_text());targets=set(t['id'] for t in json.loads((P/'inventory.json').read_text())['proof_targets']);rows=[r for r in d['results'] if r['id'] in targets]
c['lean_declarations_audited']=len(api);c['lean_full_original_claims']=[r['id'] for r in rows if r['lean']['status']=='verified'];c['lean_scope_limited_claims']=[r['id'] for r in rows if r['lean']['status']=='partial_scope_verified'];c['lean_unformalized_targets']=[r['id'] for r in rows if r['lean']['status']=='not_formalized'];(P/'verification/coverage.json').write_text(json.dumps(c,ensure_ascii=False,indent=2)+'\n')
print('coverage:',len(c['lean_full_original_claims']),len(c['lean_scope_limited_claims']),len(c['lean_unformalized_targets']))
