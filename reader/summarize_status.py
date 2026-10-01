#!/usr/bin/env python3
"""Count delivered text and current formal evidence without conflating scopes."""
import hashlib
import json
from collections import Counter
from pathlib import Path
from evidence_paths import EVIDENCE

WORK = Path(__file__).resolve().parent


def summarize():
    snapshot = WORK / 'preview/data.public.json'
    data = json.loads(snapshot.read_text())
    papers = []
    targets = []
    for paper in data['papers']:
        results = [r for r in data['math']['results'] if r.get('paper_id') == paper['id']]
        proof_targets = [r for r in results if r.get('proof_target')]
        evidence = Counter()
        records = []
        for result in proof_targets:
            lean = result.get('lean', {})
            role = lean.get('evidence_role', 'none') if lean.get('compiled') else 'none'
            if role not in {'theorem_proof', 'partial_component', 'counterexample', 'none'}:
                raise ValueError('Unknown evidence role: ' + str(role))
            evidence[role] += 1
            records.append({'id': result['id'], 'rewrite_role': result.get('rewrite_role'),
                            'rewrite_status': result.get('rewrite_status'),
                            'reading_status': result.get('reading_status'),
                            'statement_assessment': result.get('statement_assessment'),
                            'current_lean_evidence_role': role,
                            'current_mapped_declarations': lean.get('declarations', []) if lean.get('compiled') else []})
        full_text = sum(r.get('reading_status') == 'complete' and r.get('rewrite_role') == 'proof' for r in proof_targets)
        papers.append({'paper_id': paper['id'], 'result_pages': len(results),
                       'proof_targets': len(proof_targets), 'complete_proof_text': full_text,
                       'other_delivered_scope_or_counterexample_targets': len(proof_targets) - full_text,
                       'current_lean_evidence_roles': {k: evidence[k] for k in ('theorem_proof', 'partial_component', 'counterexample', 'none')},
                       'target_records': records})
        targets.extend(records)
    totals = Counter(r['current_lean_evidence_role'] for r in targets)
    report = {'status': 'counted', 'scope': 'data_and_current_evidence_accounting_not_mathematical_acceptance',
              'snapshot_sha256': hashlib.sha256(snapshot.read_bytes()).hexdigest(),
              'count_semantics': {'complete_proof_text': 'Complete rewritten proof text in its recorded scope; not a blanket assertion that every source statement is true.',
                                  'theorem_proof': 'Current Lean theorem evidence in the explicitly recorded Lean scope; the actual type and source assumptions remain authoritative.',
                                  'partial_component': 'Only a stated component, conditional domain, or component/counterexample combination is formalized.',
                                  'counterexample': 'A current formal counterexample as the primary role; never counted as a proof of the source statement. Partial-component targets can also contain formal counterexamples, so this exclusive role count is not the total number of formal counterexamples.',
                                  'none': 'No current mapped formal evidence for this target; delivered text and human counterexamples may still exist.'},
              'role_count_note': 'These mutually exclusive counts describe the primary evidence role of each target. Mixed partial proofs retain their counterexample declarations in target_records; a zero primary counterexample count does not mean no formal counterexample exists.',
              'paper_count': len(papers), 'inventory_entries': sum(len(i['entries']) for i in data['inventories']),
              'result_pages': len(data['math']['results']), 'proof_targets': len(targets),
              'shared_proofs': len(data['math']['shared_proofs']), 'canonical_concepts': len(data['symbols']),
              'complete_proof_text': sum(p['complete_proof_text'] for p in papers),
              'other_delivered_scope_or_counterexample_targets': sum(p['other_delivered_scope_or_counterexample_targets'] for p in papers),
              'current_lean_evidence_roles': {k: totals[k] for k in ('theorem_proof', 'partial_component', 'counterexample', 'none')},
              'papers': papers}
    output = EVIDENCE / 'status-summary.json'
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({k: report[k] for k in ('status', 'paper_count', 'inventory_entries', 'result_pages', 'proof_targets', 'shared_proofs', 'canonical_concepts', 'complete_proof_text', 'other_delivered_scope_or_counterexample_targets', 'current_lean_evidence_roles')}))
    return report


if __name__ == '__main__':
    summarize()
