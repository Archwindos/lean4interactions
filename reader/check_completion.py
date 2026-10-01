#!/usr/bin/env python3
"""Reject unfinished proof targets; scope explanations remain distinct outcomes."""
import json
from pathlib import Path
from evidence_paths import EVIDENCE,input_hashes
from inventory_contract import accepted_paper_ids,inventory_errors,content_errors
WORK=Path(__file__).resolve().parent
FINAL={'complete','complete_with_scope_issue','complete_with_definition_only_counterexample','complete_with_original_domain_issue','statement_refuted'}
def completion_report(data):
    proofs={p['id']:p for p in data.get('shared_proofs',[])}
    legacy_ids=accepted_paper_ids()
    contract_errors=[error for inventory in data.get('inventories',[]) for error in inventory_errors(inventory,{'results':[r for r in data['results'] if r.get('paper_id')==inventory.get('paper_id')]},legacy=inventory.get('paper_id') in legacy_ids)]
    if data.get('inventories'):
        contract_errors.extend(content_errors({'results':[r for r in data['results'] if r.get('paper_id') not in legacy_ids]}))
    incomplete=[];scope=[];targets=[];step_basis_reviews=[]
    baseline_path=WORK/'evidence/six-paper-preservation-baseline.json'
    accepted_ids=set(json.loads(baseline_path.read_text())['results']) if baseline_path.is_file() else set()
    issues={i['id'] for i in data.get('issues',[])}
    for r in data['results']:
        if not r.get('proof_target'):continue
        targets.append(r['id'])
        reasons=[]
        complete_source=any('complete' in str(r.get(key,'')) for key in ['source_transcription_status','original_proof_source_type'])
        if complete_source and '```text' in r.get('original_proof_md',''):reasons.append('raw_extracted_page_mislabeled_as_complete_mathematical_transcription')
        issue_analysis=(r.get('rewrite_status')=='blocked_by_source_issue' and
                        r.get('rewrite_role') in {'counterexample','statement_scope_explanation','partial_proof_with_refuted_clause','partial_component'} and
                        bool(r.get('proof_steps')) and
                        any(i in issues for i in r.get('related_issue_ids',[])) and
                        r.get('statement_assessment') in {'refuted','partially_refuted','counterexample_recorded','scope_under_review'})
        if r.get('rewrite_status') not in FINAL and not issue_analysis:reasons.append('rewrite_status='+str(r.get('rewrite_status')))
        if not r.get('proof_steps') and not r.get('shared_proof_ids'):reasons.append('no_proof_body_or_shared_proof')
        if r['id'] not in accepted_ids:
            if not r.get('statement_tex'):reasons.append('missing_mathematical_statement')
            if not r.get('symbol_ids'):reasons.append('missing_related_symbols')
            if not r.get('notation_map'):reasons.append('missing_paper_notation_adaptation')
            if not r.get('source_refs'):reasons.append('missing_formal_source_location')
            for step in r.get('proof_steps',[]):
                if step.get('shared_step_ref') or step.get('result_step_ref'):continue
                if not str(step.get('body_md','')).strip() and not str(step.get('justification','')).strip():reasons.append('missing_readable_step_argument='+str(step.get('id')))
                elif not step.get('justification'):
                    step_basis_reviews.append({'result_id':r['id'],'step_id':step.get('id'),'review_required':'The step basis may be explained in body_md; a mathematical reviewer must inspect the actual argument and source, without copying it into a second field.'})
        for ident in r.get('shared_proof_ids',[]):
            proof=proofs.get(ident)
            if not proof or proof.get('rewrite_status')!='complete' or not proof.get('proof_steps'):reasons.append('incomplete_shared_proof='+ident)
        if reasons:incomplete.append({'id':r['id'],'paper_id':r['paper_id'],'reasons':reasons})
        elif r.get('rewrite_status')!='complete' or r.get('rewrite_role')!='proof':scope.append({'id':r['id'],'rewrite_status':r['rewrite_status'],'rewrite_role':r.get('rewrite_role'),'statement_assessment':r.get('statement_assessment')})
    return {'status':'failed' if incomplete or contract_errors else 'passed','scope':'proof_target_content_delivery_only_not_mathematical_acceptance','proof_targets':len(targets),'inventory_contract_errors':contract_errors,'incomplete':incomplete,'distinct_scoped_or_counterexample_outcomes':scope,'required_manual_step_basis_reviews':step_basis_reviews}
if __name__=='__main__':
    d=json.loads((WORK/'data/full-content.json').read_text());r=completion_report(d)
    r['input_hashes']=input_hashes(WORK/'data/full-content.json',WORK/'evidence/six-paper-preservation-baseline.json',WORK/'inventory_contract.py',WORK/'architecture/admission-contract.json',WORK/'evidence_paths.py',Path(__file__).resolve())
    (EVIDENCE/'content-completion-checks.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'status':r['status'],'proof_targets':r['proof_targets'],'inventory_contract_errors':r['inventory_contract_errors'],'incomplete':r['incomplete']},ensure_ascii=False));raise SystemExit(r['status']!='passed')
