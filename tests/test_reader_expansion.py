"""Exercise the real admission edges exposed by adding new paper owners."""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'reader'))
from aggregate import resolve_lean_evidence_role


def test_complete_clause_counterexample_is_independent_of_partial_parent_assessment():
    lean={'status':'partial_scope_verified','evidence_role':'counterexample',
          'declarations':['Paper.checkedClause']}
    assert resolve_lean_evidence_role(lean,'partially_refuted')=='counterexample'


def test_partial_machine_component_remains_partial_even_with_a_human_counterexample():
    lean={'status':'partial_scope_verified','evidence_role':'partial_component',
          'declarations':['Paper.finiteDomainFact']}
    assert resolve_lean_evidence_role(lean,'refuted')=='partial_component'


def test_accepted_legacy_partial_scope_keeps_its_prior_role():
    lean={'status':'partial_scope_verified','evidence_role':'counterexample',
          'declarations':['Paper.checkedClause']}
    assert resolve_lean_evidence_role(lean,'partially_refuted',legacy=True)=='partial_component'


def test_new_admitted_results_preserve_reviewed_machine_roles_and_scope():
    current={row['id']:row for row in load('reader/data/full-content.json')['results']}
    baseline=set(load('reader/evidence/six-paper-preservation-baseline.json')['paper_ids'])
    checked=0
    for paper in load('corpus/public/reader/input-manifest.json')['papers']:
        if paper['paper_id'] in baseline:continue
        for source in load(paper['content_path'])['results']:
            assert current[source['id']]['lean']['evidence_role']==source['lean']['evidence_role']
            assert current[source['id']]['lean'].get('scope')==source['lean'].get('scope')
            checked+=1
    assert checked>0


def test_decoder_quotient_domain_and_proof_repairs_do_not_refute_finite_sum_conclusions():
    """The actual quotient/bars/shape issues concern domains and proof steps."""
    content = load('reader/data/full-content.json')
    results = {row['id']: row for row in content['results']}
    for ident, machine_role in (
        ('decoder-backpropagation', 'theorem_proof'),
        ('decoder-geometric-sum', 'partial_component'),
    ):
        result = results[ident]
        related = [row for row in content['issues'] if ident in row.get('related_result_ids', [])]
        assert related and {row['issue_type'] for row in related} <= {
            'definition_or_algorithm_boundary', 'proof_step_error'}
        assert result['statement_assessment'] == 'scope_under_review'
        assert result['rewrite_status'] == 'complete_with_original_domain_issue'
        assert result['rewrite_role'] != 'partial_proof_with_refuted_clause'
        assert result['verification_role'] == machine_role
        # Retain the undefined quotient boundary in both reader languages.
        assert result['scope_label'] and result['translations']['en']['scope_label']
    assert results['decoder-backpropagation']['proof_scope'] == 'full_original_statement_with_finite_sum_domain_repair'


def load(relative):
    return json.loads((ROOT / relative).read_text())


def test_old_shared_proofs_keep_their_accepted_report_when_new_reports_cover_them():
    baseline = load('reader/evidence/six-paper-preservation-baseline.json')
    old = json.loads(subprocess.check_output(
        ['git', 'show', baseline['baseline_commit'] + ':reader/data/full-content.json'],
        cwd=ROOT, text=True))
    current = {row['id']: row for row in load('reader/data/full-content.json')['shared_proofs']}
    for proof in old['shared_proofs']:
        # New paper reports genuinely include some of these common declarations.
        # Their arrival must not move the evidence of the accepted shared text.
        assert current[proof['id']]['lean'] == proof['lean']


def test_new_symbol_scope_variants_retain_the_authors_actual_english():
    content = load('reader/data/full-content.json')
    symbols = content['symbols']
    checked = 0
    for paper in load('corpus/public/reader/input-manifest.json')['papers']:
        if paper['paper_id'] not in {'neurips2021-robustness', 'neurips2024-dynamics'}:
            continue
        for source in load(paper['symbols_path'])['symbols']:
            provided = source.get('translations', {}).get('en', {})
            relevant = {key: provided[key] for key in ('type_or_domain', 'scope') if key in provided}
            if not relevant:
                continue
            canonical = next(row for row in symbols if source['id'] in row['record_ids'])
            pair = next((original, english) for original, english in zip(
                canonical['scope_variants'], canonical['translations']['en']['scope_variants'])
                if all(original.get(key, '') == source.get(key, '')
                       for key in ('definition_tex', 'type_or_domain', 'scope'))
                and original.get('translations', {}).get('en') == relevant)
            assert all(pair[1][key] == value for key, value in relevant.items())
            checked += 1
    assert checked > 0


def test_new_shared_proofs_resolve_symbols_under_their_source_owner():
    content = load('reader/data/full-content.json')
    proofs = {row['id']: row for row in content['shared_proofs']}
    symbols = {row['id']: row for row in content['symbols']}
    expected = ['sym-universe', 'sym-variable-count', 'sym-coalition', 'robustness-context-order']
    for ident in ('robustness-flagged-context-counting', 'robustness-context-relabeling'):
        proof = proofs[ident]
        assert proof['paper_id'] == 'neurips2021-robustness'
        assert proof['symbol_ids'] == expected
        for symbol_id in expected:
            assert any(mapping['paper_id'] == proof['paper_id']
                       for mapping in symbols[symbol_id]['paper_mappings'])
