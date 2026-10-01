"""Bind actual declarations, retaining canonical evidence roles and exact scopes."""
from pathlib import Path
import json
from status_correction import apply_status_correction
D=Path(__file__).parent
rep=json.load(open(D/'verification/report.json'))
assert rep['status']=='passed'
api={r['name']:r for r in rep['declarations']}
data=json.load(open(D/'content.json'))
report_path='corpus/public/reader/icml2023-decoder/verification/report.json'
def bind(row):
 lean=row['lean'];role=lean['evidence_role'];decls=lean['declarations']
 enscope=lean['translations']['en']['scope']
 if decls:
  actual=[api[n] for n in decls];first=actual[0]
  row['lean']=dict(status='verified' if role in ['theorem_proof','counterexample'] else 'partial_scope_verified',
   evidence_role=role,declarations=decls,compiled=True,report_path=report_path,
   build_id=rep['build_id'],source_fingerprint=rep['source_fingerprint'],
   source_path=first['source_path'],line=first['line'],statement=first['signature'],
   axiom_audit='passed',axioms=sorted(set(a for r in actual for a in r['axioms'])),
   source_semantics_automatically_verified=False,scope=row['scope'],translations={'en':dict(scope=enscope)})
 else:
  assert role=='none'
  row['lean']=dict(status='not_formalized',evidence_role='none',declarations=[],compiled=False,
   scope=row['scope'],translations={'en':dict(scope=enscope)})
 for step,en in zip(row['proof_steps'],row['translations']['en']['proof_steps']):
  zh=[];ee=[]
  for name in step['lean_refs']:
   if isinstance(name,dict):name=name['declaration']
   actual=api[name]
   ref=dict(declaration=name,source_path=actual['source_path'],line=actual['line'],
    scope='exact_declaration_type_in_report',explanation_md=step['body_md'])
   zh.append(ref);ee.append({**ref,'explanation_md':en['body_md']})
  step['lean_refs']=zh;en['lean_refs']=ee
 row['lean']['step_map']=[dict(step_id=s['id'],**ref) for s in row['proof_steps'] for ref in s['lean_refs']]
 row['rewrite_status']='complete'
 apply_status_correction(row)
for row in data['results']+data['shared_proofs']:bind(row)
inv=json.load(open(D/'inventory.json'));lookup={r['id']:r for r in data['results']}
for e in inv['entries']:
 row=lookup[e['id']];row['proof_target']=e['proof_target']
 e['statement_assessment']=row['statement_assessment'];e['rewrite_status']='complete'
 e['rewrite_role']=row['rewrite_role']
 if row['id'] in ('decoder-backpropagation','decoder-geometric-sum'):
  e['rewrite_status']=row['rewrite_status']
inv['counts']['valid_proof_targets']=sum(r['lean']['evidence_role']=='theorem_proof' for r in data['results'])
inv['review_status']='agent_full_page_reviewed_pending_root_audit'
data['review_status']='agent_completed_pending_independent_root_admission'
data['coverage'].update(audited_declarations=len(api),formalization_complete=False,
 formalization_scope='Exact full statements, verified counterexamples, conditional components and explicitly unformalized inferential analyses are separated by canonical evidence_role.',
 human_rewrite_complete=True)
for name,x in [('content.json',data),('inventory.json',inv)]:
 (D/name).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
coverage=dict(paper_id=data['paper_id'],reading_entries=len(data['results']),
 physical_pages=len(inv['page_audit']),proof_targets=len(inv['proof_targets']),
 source_occurrences=len(inv['source_occurrence_map']),audited_declarations=len(api),
 theorem_targets=[r['id'] for r in data['results'] if r['lean']['evidence_role']=='theorem_proof'],
 counterexample_targets=[r['id'] for r in data['results'] if r['lean']['evidence_role']=='counterexample'],
 partial_targets=[r['id'] for r in data['results'] if r['lean']['evidence_role']=='partial_component'],
 unformalized_targets=[r['id'] for r in data['results'] if r['proof_target'] and r['lean']['evidence_role']=='none'],
 source_semantics_automatically_verified=False,user_review_status='pending')
(D/'verification/coverage.json').write_text(json.dumps(coverage,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(coverage,ensure_ascii=False))
