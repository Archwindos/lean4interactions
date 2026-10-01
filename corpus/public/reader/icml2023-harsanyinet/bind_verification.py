from pathlib import Path
import json
D=Path('corpus/public/reader/icml2023-harsanyinet');p=D/'content.json';x=json.loads(p.read_text());report=json.loads((D/'verification/report.json').read_text());api={r['name']:r for r in report['declarations']};assert report['status']=='passed'
prim={'hnet-centered-definition':'Harsanyi.interaction_recursive','hnet-reconstruction':'Harsanyi.reconstruction','hnet-shapley-definition':'Harsanyi.factorialShapley','hnet-shapley-dividend':'Harsanyi.factorialShapley_eq_dividendAllocation','hnet-readout-linearity':'PaperHarsanyiNet.centered_readout','hnet-forward-shapley':'PaperHarsanyiNet.finite_requirements_attribution','hnet-architecture':'Harsanyi.Network.value','hnet-architecture-r1-r2':'Harsanyi.Network.value_mask','hnet-unit-interaction':'Harsanyi.Network.empty_unit_counterexample','hnet-sparsity-count':'PaperHarsanyiNet.finite_support_card','hnet-cnn-receptive':'Harsanyi.Network.receptive_shared_children','hnet-cnn-regroup':'Harsanyi.Network.groupedBlock_mask','hnet-conditional-attribution':'PaperHarsanyiNet.finite_conditional_attribution','hnet-axiom-efficiency':'PaperHarsanyiNet.shapley_efficiency','hnet-axiom-linearity':'PaperHarsanyiNet.shapley_add','hnet-axiom-dummy':'PaperHarsanyiNet.shapley_dummy','hnet-axiom-symmetry':'PaperHarsanyiNet.shapley_symmetry'}
partial={'hnet-forward-shapley','hnet-unit-interaction','hnet-sparsity-count','hnet-cnn-regroup'}
for r in x['results']:
 k=r['id'];stepmap=[]
 for st in r['proof_steps']:
  for ref in st['lean_refs']:
   if ref['declaration'] in api:
    rr=api[ref['declaration']];ref.update(source_path=rr['source_path'],line=rr['line']);stepmap.append({'step_id':st['id'],**ref})
 if k not in prim:
  r['lean'].update(status='not_formalized' if k.startswith('hnet-axiom') else 'not_applicable',compiled=False,declarations=[])
  continue
 row=api[prim[k]];names=list(dict.fromkeys([prim[k]]+r['lean']['declarations']));names=[n for n in names if n in api]
 r['lean'].update(status='partial_scope_verified' if k in partial else 'verified',compiled=True,axiom_audit='passed',declarations=names,report_path=str(D/'verification/report.json'),build_id=report['build_id'],source_fingerprint=report['source_fingerprint'],statement=row['signature'],source_path=row['source_path'],line=row['line'],step_map=stepmap,axioms=row['axioms'],source_semantics_automatically_verified=False)
 if k=='hnet-unit-interaction':r['lean'].update(evidence_role='counterexample',source_evidence_role='counterexample_and_valid_architecture_subclaim')
 if k=='hnet-cnn-regroup':r['lean'].update(evidence_role='partial_component',source_evidence_role='grouped_block_step_and_regrouping_and_counterexample')
 if k=='hnet-axiom-efficiency':r['lean']['scope']='Entire classical factorial Shapley efficiency, with the output baseline retained; V is explicitly centered.'
 if k=='hnet-forward-shapley':r['lean']['scope']='Entire classical Shapley conditional-sum algorithm. The printed all-unit reciprocal lacks an empty-field convention; no validation of its literal undefined expression is claimed.'
 r['translations']['en'].pop('lean',None)
for r in x['results']:
 for zs,es in zip(r['proof_steps'],r['translations']['en']['proof_steps']):
  es['lean_refs']=[{**ref,'explanation_md':'This declaration verifies the stated mathematical scope; correspondence to the source prose is checked separately.'} for ref in zs['lean_refs']]
p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
inv=json.loads((D/'inventory.json').read_text())
coverage=dict(paper_id=x['paper_id'],source_pages_reviewed=22,inventory_entries=len(inv['entries']),reading_entries=len(x['results']),english_reading_entries=len(x['results']),source_local_proof_transcripts=['hnet-readout-linearity','hnet-forward-shapley','hnet-architecture-r1-r2','hnet-unit-interaction','hnet-cnn-receptive','hnet-cnn-regroup'],lean_declarations_audited=len(api),lean_full_scope_entries=[r['id'] for r in x['results'] if r['lean']['status']=='verified'],lean_limited_scope_entries=[r['id'] for r in x['results'] if r['lean']['status']=='partial_scope_verified'],lean_unformalized_targets=[r['id'] for r in x['results'] if r['lean']['status']=='not_formalized'],false_original_statement='hnet-unit-interaction',false_original_subclaims=['hnet-cnn-regroup','hnet-sparsity-count'],source_semantics_automatically_verified=False,user_review_status='pending',scope_note='Definitions, externally cited axioms, empirical descriptions, author proof blocks, and original counterexamples are counted separately. No original proposition or assumptions were modified.')
(D/'verification/coverage.json').write_text(json.dumps(coverage,ensure_ascii=False,indent=2)+'\n');print('Hnet verified binding',len(prim))
