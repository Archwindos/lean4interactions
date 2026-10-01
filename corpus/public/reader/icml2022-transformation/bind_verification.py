from pathlib import Path
import json
D=Path(__file__).parent;rep=json.load(open(D/'verification/report.json'));assert rep['status']=='passed';api={r['name']:r for r in rep['declarations']}
c=json.load(open(D/'content.json'));report_path='corpus/public/reader/icml2022-transformation/verification/report.json'
for r in c['results']+c['shared_proofs']:
 names=r['lean']['declarations'];role=r['lean']['evidence_role'];scope=r['scope'];en=r['translations']['en']['scope']
 if names:
  assert all(n in api for n in names),(r['id'],set(names)-set(api));q=[api[n] for n in names];last=next((z for z in reversed(q) if z['kind']=='theorem'),q[-1])
  r['lean']=dict(status='verified' if role in ['theorem_proof','counterexample'] else 'partial_scope_verified',evidence_role=role,declarations=names,compiled=True,scope=scope,report_path=report_path,build_id=rep['build_id'],source_fingerprint=rep['source_fingerprint'],source_path=last['source_path'],line=last['line'],statement=last['signature'],axiom_audit='passed',axioms=sorted(set(a for z in q for a in z['axioms'])),source_semantics_automatically_verified=False,translations={'en':dict(scope=en)})
 else:r['lean'].update(compiled=False,scope=scope,translations={'en':dict(scope=en)})
 for st,es in zip(r['proof_steps'],r['translations']['en']['proof_steps']):
  maps=[];emaps=[]
  for n in st['lean_refs']:
   n=n if isinstance(n,str) else n['declaration'];z=api[n]
   a=dict(declaration=n,source_path=z['source_path'],line=z['line'],scope='exact_declaration_type_in_report',explanation_md=st['body_md']);maps.append(a);emaps.append({**a,'explanation_md':es['body_md']})
  st['lean_refs']=maps;es['lean_refs']=emaps
 r['lean']['step_map']=[dict(step_id=st['id'],**ref) for st in r['proof_steps'] for ref in st['lean_refs']]
(D/'content.json').write_text(json.dumps(c,ensure_ascii=False,indent=2)+'\n')
i=json.load(open(D/'inventory.json'));i['review_status']='agent_full_page_reviewed_pending_root_audit'
rs={r['id']:r for r in c['results']}
for e in i['entries']:e['statement_assessment']=rs[e['id']]['statement_assessment']
(D/'inventory.json').write_text(json.dumps(i,ensure_ascii=False,indent=2)+'\n')
coverage=dict(paper_id=c['paper_id'],reading_entries=len(c['results']),proof_targets=len(i['proof_targets']),physical_pages=len(i['page_audit']),audited_declarations=len(api),shared_proofs=[r['id'] for r in c['shared_proofs']],full_original_statement_adapters=[r['id'] for r in c['results'] if r['lean']['evidence_role']=='theorem_proof'],counterexample_targets=[r['id'] for r in c['results'] if r['lean']['evidence_role']=='counterexample'],partial_targets=[r['id'] for r in c['results'] if r['lean']['evidence_role']=='partial_component'],unformalized_external_targets=[r['id'] for r in c['results'] if r['proof_target'] and r['lean']['evidence_role']=='none' and r['id']!='transformation-activation-heuristics'],unformalized_scope_targets=[r['id'] for r in c['results'] if r['proof_target'] and r['lean']['evidence_role']=='none' and r['id']=='transformation-activation-heuristics'],source_semantics_automatically_verified=False)
(D/'verification/coverage.json').write_text(json.dumps(coverage,ensure_ascii=False,indent=2)+'\n');print(coverage)
