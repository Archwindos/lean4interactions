import json
from pathlib import Path
P=Path(__file__).parent;d=json.loads((P/'content.json').read_text());rep=json.loads((P/'verification/report.json').read_text());assert rep['status']=='passed';api={r['name']:r for r in rep['declarations']}
lookup={
'layer-and-reconstruction':(['Harsanyi.reconstruction'],'verified','Exact finite-game Mobius reconstruction; the raw output baseline is retained.'),
'layer-decomposition':(['Harsanyi.Layerwise.component_sum','Harsanyi.Layerwise.component_empty'],'verified','Pointwise component identity and the original empty-component convention; no optimizer uniqueness is claimed.'),
'layer-universal-matching':(['PaperLayerwise.actual_matching','PaperLayerwise.actual_remasked_matching','PaperLayerwise.repeated_mask','Harsanyi.Layerwise.restricted_and'],'verified','The original matching identity for actual coordinate masks, with the source empty-component condition. The remasked adapter restricts a fixed split; a freely relearned split is instantiated separately in the base matching theorem with its own stated empty convention.'),
'layer-salient-matching':(['Harsanyi.Layerwise.duplicated_baseline_counterexample'],'partial_scope_verified','Only the original Eq.(19) duplicate-baseline error is formally refuted. The original small-family approximation and external sparsity premises are not proved.'),
'layer-strength-decomposition':(['Harsanyi.Layerwise.normalized_thresholded_counterexample','Harsanyi.Layerwise.strengthGame_dividends','Harsanyi.Layerwise.strength_full_outputs','Harsanyi.Layerwise.strength_supports','Harsanyi.Layerwise.scalar_strength_decomposition'],'partial_scope_verified','A real finite-game thresholded support/metric counterexample to the first Eq.(8) clause is compiled, together with dividend and full-output checks. The source gamma/pure-AND interpretation, one-sample normalization, and global L1 optimality are established in the human proof; they are not an additional compiled optimizer theorem. The scalar identity is independent.'),
'layer-binomial-symmetry':(['Harsanyi.Layerwise.complementary_order_count'],'verified','Entire complementary-order counting identity; empirical generalization is outside this declaration.'),
'layer-shapley-and-or':(['PaperLayerwise.actual_shapley','Harsanyi.Layerwise.shapley_and_or'],'verified','Entire classical factorial-marginal Shapley sharing identity for the actual masked probe/model and its fixed gamma split.'),
'layer-singleton-merge':(['Harsanyi.Layerwise.singleton_merge','Harsanyi.Layerwise.singleton_activation'],'verified','Entire singleton contribution merge on every retained set; higher-order mergers and optimizer invariance are not claimed.')}
for r in d['results']:
 k=r['id']
 if k not in lookup:
  r['lean']={'status':'not_formalized' if k in ['layer-complement-duality','layer-or-sparsity-inheritance'] else 'not_applicable','declarations':[],'compiled':False,'scope':'The complete human explanation/proof or source-scope analysis is supplied; no additional exact Lean declaration is claimed for this entry.'};continue
 names,status,scope=lookup[k]
 if any(n not in api for n in names):
  r['lean']={'status':'compiled_pending_report','declarations':names,'compiled':False,'scope':scope+' A named shared declaration is awaiting inclusion in the current exact report.'};continue
 rows=[api[n] for n in names];row=rows[0]
 r['lean']={'status':status,'declarations':names,'compiled':True,'scope':scope,'report_path':'corpus/public/reader/icml2024-layerwise/verification/report.json','build_id':rep['build_id'],'source_fingerprint':rep['source_fingerprint'],'axiom_audit':'passed','axioms':sorted(set(a for t in rows for a in t['axioms'])),'source_path':row['source_path'],'line':row['line'],'statement':row['signature'],'source_semantics_automatically_verified':False}
 if k in ['layer-strength-decomposition','layer-salient-matching']:r['lean']['evidence_role']='counterexample_with_explicit_partial_scope'
 for zs,es in zip(r['proof_steps'],r['translations']['en']['proof_steps']):
  refs=zs['lean_refs']
  if k=='layer-strength-decomposition' and zs is r['proof_steps'][-1]:
   refs=[{'declaration':names[0],'scope':'actual_thresholded_finite_game_counterexample_without_formal_optimizer_theorem','explanation_md':'实际有限游戏的原阈值支持和三项强度均核验；全局优化与模型坐标适配仍在文字证明，不冒充该声明覆盖。'}]
  if k=='layer-strength-decomposition' and zs is r['proof_steps'][1]:
   refs=[{'declaration':n,'scope':'finite_game_dividends_and_full_outputs','explanation_md':'核验有限重构游戏的交互支撑及全输出；优化下界和零OR分解在文字中推导。'} for n in names[1:3]]
  if k=='layer-universal-matching' and zs is r['proof_steps'][2]:
   refs=[{'declaration':n,'scope':'actual_fixed_or_remasked_paper_adapter','explanation_md':'固定及再次掩码版本实际核验；重新自由学习分解用通用固定式另实例化，不假设优化器等于旧参数限制。'} for n in names[:3]]
  for ref in refs:
   if ref['declaration'] in api:ref['source_path']=api[ref['declaration']]['source_path'];ref['line']=api[ref['declaration']]['line']
  zs['lean_refs']=refs
  old={ref['declaration']:ref.get('explanation_md','') for ref in es.get('lean_refs',[])}
  es['lean_refs']=[{**ref,'explanation_md':old.get(ref['declaration']) or scope} for ref in refs]
 r['lean']['step_map']=[{'step_id':st['id'],**ref} for st in r['proof_steps'] for ref in st['lean_refs']]
(P/'content.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
targets=set(json.load(open(P/'paper-metadata.json'))['results']);selected=[r for r in d['results'] if r['id'] in targets]
summary={'paper_id':d['paper_id'],'source_pages_reviewed':22,'independent_mathematical_targets':9,'reading_entries':17,'original_full_proof_blocks':3,'english_reading_entries':17,'audited_declarations':len(api),'lean_full_original_claims':[r['id'] for r in selected if r['lean']['status']=='verified'],'lean_partial_or_counterexample_scope':[r['id'] for r in selected if r['lean']['status']=='partial_scope_verified'],'lean_unformalized_or_pending_targets':[r['id'] for r in selected if r['lean']['status'] in ['not_formalized','compiled_pending_report']],'false_original_subclaims':['layer-strength-decomposition:Eq8_first_clause','layer-complement-duality:Eq13_printed_coordinate_equality'],'external_scope_unresolved':['layer-salient-matching','layer-or-sparsity-inheritance'],'source_semantics_automatically_verified':False,'user_review_status':'pending'}
(P/'verification/coverage.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n');print(summary)
