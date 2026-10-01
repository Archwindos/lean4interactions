from pathlib import Path
import json,copy
D=Path('corpus/public/reader/icml2025-coalition');p=D/'content.json';x=json.loads(p.read_text());report=json.loads((D/'verification/report.json').read_text());api={r['name']:r for r in report['declarations']};assert report['status']=='passed'
prim={'shapley':'PaperCoalition.theorem32','banzhaf':'PaperCoalition.theorem33','conflict':'PaperCoalition.theorem34_nonempty','individual':'PaperCoalition.theorem36','singleton':'PaperCoalition.corollary37','efficiency':'PaperCoalition.corollary38_nonempty','no-conflict':'Harsanyi.Coalition.paper_no_conflict','matching':'Harsanyi.Coalition.universal_matching','R':'Harsanyi.Coalition.r_bounds','Rprime':'Harsanyi.Coalition.rprime_bounds','Q':'Harsanyi.Coalition.q_bounds','shapley-coefficient':'Harsanyi.Coalition.shapley_kernel','banzhaf-coefficient':'Harsanyi.Coalition.signed_half_superset','toy-support':'Harsanyi.Coalition.toy_and_support'}
partial={'conflict','no-conflict','efficiency','R','Rprime','Q','shapley-coefficient','toy-support'}
for r in x['results']:
 k=r['id'].removeprefix('coalition-')
 if k not in prim:continue
 decl=prim[k];row=api[decl];names=list(dict.fromkeys([decl]+r['lean']['declarations']));stepmap=[]
 for st in r['proof_steps']:
  for ref in st['lean_refs']:
   if ref['declaration'] in api:
    rr=api[ref['declaration']];ref['source_path']=rr['source_path'];ref['line']=rr['line']
   stepmap.append({'step_id':st['id'],**ref})
 # Translation changes prose only; formal fields are inherited from the updated map.
 for zs,es in zip(r['proof_steps'],r['translations']['en']['proof_steps']):
  es['lean_refs']=copy.deepcopy(zs['lean_refs'])
  for ref in es['lean_refs']:
   if ref.get('explanation_md')=='实际原定义的有限和适配；原空集或分母范围另列。':
    ref['explanation_md']='Finite-sum adapter of the actual original definitions; empty-set and denominator scope issues are recorded separately.'
 r['lean'].update(status='partial_scope_verified' if k in partial else 'verified',compiled=True,axiom_audit='passed',declarations=names,report_path=str(D/'verification/report.json'),build_id=report['build_id'],source_fingerprint=report['source_fingerprint'],statement=row['signature'],source_path=row['source_path'],line=row['line'],step_map=stepmap,axioms=row['axioms'],label='实际所列范围通过编译与公理审计；原命题语义人工核查',source_semantics_automatically_verified=False)
 if k=='no-conflict':r['lean']['scope']='The original prose partial-coverage zero-effects condition, with an explicit finite quantifier; not a repair of the printed free-i premise or empty-coalition domain.'
 if k in ['conflict','efficiency']:r['lean']['scope']='Exact actual coordinate-mask model adapter for the source nonempty quotient domain. The original all-subsets empty-coalition assertion is not marked proved.'
 if k in ['shapley','banzhaf','individual','singleton']:r['lean']['scope']='Entire source claim for the actual finite coordinate-mask model and original gamma splitting; all membership and baseline conditions retained.'
p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
# Honest coverage report, independent from compile counts.
inv=json.loads((D/'inventory.json').read_text());targetids={t['id'] for t in inv['proof_targets']};targets=[r for r in x['results'] if r['id'] in targetids]
summary={'paper_id':'icml2025-coalition','source_pages_reviewed':24,'inventory_entries':30,'independent_mathematical_targets':19,'reading_entries':29,'complete_author_proof_calculation_blocks':10,'source_numbered_results':7,'english_reading_entries':29,'lean_declarations_audited':len(api),'lean_full_original_claims':[r['id'] for r in targets if r['lean']['status']=='verified'],'lean_scope_limited_claims':[r['id'] for r in targets if r['lean']['status']=='partial_scope_verified'],'lean_unformalized_targets':[r['id'] for r in targets if r['lean']['status']=='not_formalized'],'false_original_claims':['coalition-symmetry-alpha','coalition-symmetry-beta','coalition-additivity'],'displayed_definition_only_counterexample':['coalition-dummy'],'source_selection_scope_issue':['coalition-anonymity'],'original_empty_or_zero_denominator_issues':['issue-coalition-empty-coalition','issue-coalition-zero-denominators'],'source_semantics_automatically_verified':False,'user_review_status':'pending','scope_note':'No source proposition was modified, no new optimizer compatibility or zero convention was added, and source/reading/formalization counts are independent.'}
(D/'verification/coverage.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
print(summary)
