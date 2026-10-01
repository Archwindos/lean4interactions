"""Apply the root-requested, limited metadata correction to the bound package."""
from pathlib import Path
import copy,hashlib,json
from status_correction import apply_status_correction,CORRECTIONS
D=Path(__file__).parent
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
tracked=['content.json','inventory.json','verification/report.json','lean/PaperDecoder.lean',
 'issues.json','symbols.json','source-occurrence-map.json']
before_hashes={f:sha(D/f) for f in tracked}
data=json.load(open(D/'content.json'));old=copy.deepcopy(data)
inv=json.load(open(D/'inventory.json'));oldinv=copy.deepcopy(inv)
changes=[]
for row in data['results']:
 prior=copy.deepcopy(row)
 apply_status_correction(row)
 if row!=prior:
  def without_metadata(x):
   x=copy.deepcopy(x)
   for key in ['statement_assessment','rewrite_status','rewrite_role','scope_label']:x.pop(key,None)
   x['translations']['en'].pop('scope_label',None)
   return x
  assert without_metadata(row)==without_metadata(prior),row['id']
  changes.append(dict(id=row['id'],
   before={k:prior.get(k) for k in ['statement_assessment','rewrite_status','rewrite_role','scope_label']},
   after={k:row.get(k) for k in ['statement_assessment','rewrite_status','rewrite_role','scope_label']},
   scope_label_en=row['translations']['en']['scope_label']))
assert {r['id'] for r in changes}==set(CORRECTIONS)
for entry in inv['entries']:
 if entry['id'] in CORRECTIONS:
  row=next(r for r in data['results'] if r['id']==entry['id'])
  for key in ['statement_assessment','rewrite_status','rewrite_role']:entry[key]=row[key]
assert data['shared_proofs']==old['shared_proofs']
assert data['coverage']==old['coverage']
assert inv['counts']==oldinv['counts'] and inv['proof_targets']==oldinv['proof_targets']
for filename,value in [('content.json',data),('inventory.json',inv)]:
 (D/filename).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
after_hashes={f:sha(D/f) for f in tracked}
assert all(before_hashes[f]==after_hashes[f] for f in tracked if f not in ['content.json','inventory.json'])
review=[]
for row in data['results']:
 linked=[q for q in data['issues'] if q['id'] in row['related_issue_ids']]
 review.append(dict(id=row['id'],statement_assessment=row['statement_assessment'],
  related_issue_types=[q['issue_type'] for q in linked],
  decision='domain_boundary_status_corrected' if row['id'] in CORRECTIONS else 'retained_after_individual_scope_review'))
out=dict(status='passed',scope='Only original-statement assessment and domain-boundary presentation metadata',
 before_hashes=before_hashes,after_hashes=after_hashes,changes=changes,
 mathematical_prose_originals_and_lean_unchanged=True,shared_proofs_unchanged=True,
 denominator_and_counts_unchanged=True,all_34_assessments_reviewed=review,
 rationale=dict(backpropagation='The full same-loss Eq5 matrix identity is proved using finite sums. Related errors concern undefined sine quotients and local proof steps; there is no counterexample to its matrix conclusion.',
 geometric_sum='The sole issue is an undefined ordinary sine quotient at denominator zeros. Finite sums and the valid quotient domain are proved; undefined notation is not a numerical clause counterexample.',
 retained_partial_counterexamples='The K-growth, non-DC padding and exact one-step zero-loss clauses each have actual original-model counterexamples and remain partially_refuted.'))
(D/'verification/status-assessment-correction.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(dict(changes=changes,after_hashes=after_hashes),ensure_ascii=False))
