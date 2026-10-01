#!/usr/bin/env python3
"""Reject unfinished proof targets; scope explanations remain distinct outcomes."""
import json
from pathlib import Path
WORK=Path(__file__).resolve().parent
FINAL={'complete','complete_with_scope_issue','complete_with_definition_only_counterexample','complete_with_original_domain_issue','statement_refuted'}
def completion_report(data):
    proofs={p['id']:p for p in data.get('shared_proofs',[])}
    incomplete=[];scope=[];targets=[]
    issues={i['id'] for i in data.get('issues',[])}
    for r in data['results']:
        if not r.get('proof_target'):continue
        targets.append(r['id'])
        reasons=[]
        issue_analysis=(r.get('rewrite_status')=='blocked_by_source_issue' and
                        r.get('rewrite_role') in {'counterexample','statement_scope_explanation','partial_proof_with_refuted_clause','partial_component'} and
                        bool(r.get('proof_steps')) and
                        any(i in issues for i in r.get('related_issue_ids',[])) and
                        r.get('statement_assessment') in {'refuted','partially_refuted','counterexample_recorded','scope_under_review'})
        if r.get('rewrite_status') not in FINAL and not issue_analysis:reasons.append('rewrite_status='+str(r.get('rewrite_status')))
        if not r.get('proof_steps') and not r.get('shared_proof_ids'):reasons.append('no_proof_body_or_shared_proof')
        for ident in r.get('shared_proof_ids',[]):
            proof=proofs.get(ident)
            if not proof or proof.get('rewrite_status')!='complete' or not proof.get('proof_steps'):reasons.append('incomplete_shared_proof='+ident)
        if reasons:incomplete.append({'id':r['id'],'paper_id':r['paper_id'],'reasons':reasons})
        elif r.get('rewrite_status')!='complete' or r.get('rewrite_role')!='proof':scope.append({'id':r['id'],'rewrite_status':r['rewrite_status'],'rewrite_role':r.get('rewrite_role'),'statement_assessment':r.get('statement_assessment')})
    return {'status':'failed' if incomplete else 'passed','scope':'proof_target_content_delivery_only_not_mathematical_acceptance','proof_targets':len(targets),'incomplete':incomplete,'distinct_scoped_or_counterexample_outcomes':scope}
if __name__=='__main__':
    d=json.loads((WORK/'data/full-content.json').read_text());r=completion_report(d)
    (WORK/'evidence/content-completion-checks.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'status':r['status'],'proof_targets':r['proof_targets'],'incomplete':r['incomplete']},ensure_ascii=False));raise SystemExit(bool(r['incomplete']))
