from pathlib import Path
import json
D=Path(__file__).parent;rep=json.load(open(D/'verification/report.json'));assert rep['status']=='passed';api={r['name']:r for r in rep['declarations']};data=json.load(open(D/'content.json'));report_path=str(D/'verification/report.json')
# Invocation path is relative to the project and kept reproducible.
report_path='corpus/public/reader/neurips2021-robustness/verification/report.json'
for r in data['results']:
 old=r['rewrite_role'];r['rewrite_role']={'scope_analysis':'statement_scope_explanation'}.get(old,old)
 if r['kind']=='definition':r['rewrite_role']='source_material'
 assessment=r['statement_assessment'];r['statement_assessment']={'valid':'no_statement_error_recorded','domain_issue':'partially_refuted','false_original_floor_clause':'refuted','empirical_or_unquantified':'scope_under_review','externally_attributed_not_locally_proved':'scope_under_review'}.get(assessment,assessment)
 names=r['lean']['declarations'];scope=r['lean']['scope'] if names else r['translations']['en']['scope']
 role='theorem_proof' if r['rewrite_role']=='proof' and names else 'counterexample' if r['rewrite_role']=='counterexample' and names else 'partial_component' if names else 'none'
 if names:
  assert all(n in api for n in names),(r['id'],names)
  rows=[api[n] for n in names];first=rows[0]
  r['lean']=dict(status='verified' if role in ['theorem_proof','counterexample'] else 'partial_scope_verified',evidence_role=role,declarations=names,compiled=True,scope=r['scope'],report_path=report_path,build_id=rep['build_id'],source_fingerprint=rep['source_fingerprint'],source_path=first['source_path'],line=first['line'],statement=first['signature'],axiom_audit='passed',axioms=sorted(set(a for q in rows for a in q['axioms'])),source_semantics_automatically_verified=False,translations={'en':dict(scope=scope)})
 else:r['lean']=dict(status='not_formalized' if r['kind']=='external_theorem_scope' else 'not_applicable',evidence_role='none',declarations=[],compiled=False,scope=r['scope'],translations={'en':dict(scope=scope)})
 for st,en in zip(r['proof_steps'],r['translations']['en']['proof_steps']):
  mapped=[];emap=[]
  for n in st['lean_refs']:
   n=n if isinstance(n,str) else n['declaration'];assert n in api,n
   q=api[n];ref=dict(declaration=n,source_path=q['source_path'],line=q['line'],scope='exact_declaration_type_in_report',explanation_md=st['body_md'])
   mapped.append(ref);emap.append({**ref,'explanation_md':en['body_md']})
  st['lean_refs']=mapped;en['lean_refs']=emap
 r['lean']['step_map']=[dict(step_id=st['id'],**ref) for st in r['proof_steps'] for ref in st['lean_refs']]
for sh in data['shared_proofs']:
 names=list(dict.fromkeys(n for st in sh['proof_steps'] for n in st['lean_refs']));assert all(n in api for n in names)
 sh['proof_scope']='exact_shared_finite_statement';sh['lean']=dict(status='verified',evidence_role='theorem_proof',declarations=names,compiled=True,report_path=report_path,build_id=rep['build_id'],source_fingerprint=rep['source_fingerprint'],scope='共享命题按下列实际类型实现；论文局部前提另行适配。',translations={'en':dict(scope='The shared proposition is implemented by the exact types listed below; paper-specific premises are adapted separately.')})
 for st,en in zip(sh['proof_steps'],sh['translations']['en']['proof_steps']):
  mapped=[];emap=[]
  for n in st['lean_refs']:
   q=api[n];ref=dict(declaration=n,source_path=q['source_path'],line=q['line'],scope='exact_shared_finite_statement',explanation_md=st['body_md']);mapped.append(ref);emap.append({**ref,'explanation_md':en['body_md']})
  st['lean_refs']=mapped;en['lean_refs']=emap
 sh['lean']['step_map']=[dict(step_id=st['id'],**ref) for st in sh['proof_steps'] for ref in st['lean_refs']]
 sh['translations']['en']['scope']='The complete finite shared proposition, with the conditions stated above.'
(D/'content.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
inv=json.load(open(D/'inventory.json'));lookup={r['id']:r for r in data['results']}
for e in inv['entries']:
 lookup[e['id']]['proof_target']=e['proof_target']
 e['statement_assessment']=lookup[e['id']]['statement_assessment']
 if not e['proof_target']:e['non_proof_reason']='Source Equations (2)–(5) define the pair/context averages and order-wise attribution; this entry records those definitions, while their properties have separate target entries.'
(D/'content.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
inv['review_status']='agent_full_page_reviewed_pending_root_audit';(D/'inventory.json').write_text(json.dumps(inv,ensure_ascii=False,indent=2)+'\n')
coverage=dict(paper_id=data['paper_id'],reading_entries=len(data['results']),physical_pages=len(inv['page_audit']),proof_targets=len(inv['proof_targets']),audited_declarations=len(api),full_original_statement_adapters=[r['id'] for r in data['results'] if r['lean']['evidence_role']=='theorem_proof'],counterexample_targets=[r['id'] for r in data['results'] if r['lean']['evidence_role']=='counterexample'],partial_targets=[r['id'] for r in data['results'] if r['lean']['evidence_role']=='partial_component'],external_unformalized=['robustness-classical-uniqueness'],source_semantics_automatically_verified=False,user_review_status='pending')
(D/'verification/coverage.json').write_text(json.dumps(coverage,ensure_ascii=False,indent=2)+'\n');print(coverage)
