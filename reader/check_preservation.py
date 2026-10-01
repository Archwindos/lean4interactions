#!/usr/bin/env python3
"""Compare the current release against accepted public inputs; never read private material."""
import hashlib
import json
import subprocess
from pathlib import Path
from evidence_paths import EVIDENCE,input_hashes

ROOT=Path(__file__).resolve().parents[1]
BASELINE=ROOT/'reader/evidence/six-paper-preservation-baseline.json'

def semantic(value):
 if isinstance(value,dict):return {k:semantic(v) for k,v in value.items() if k!='translations'}
 if isinstance(value,list):return [semantic(x) for x in value]
 return value

def check_preservation():
 baseline=json.loads(BASELINE.read_text())
 historical=json.loads(subprocess.check_output(['git','show',baseline['baseline_commit']+':reader/data/full-content.json'],cwd=ROOT,text=True))
 current=json.loads((ROOT/'reader/data/full-content.json').read_text())
 errors=[];inputs=[];results=[];shared=[]
 for rel,expected in baseline['input_sha256'].items():
  path=ROOT/rel;actual=hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else None
  inputs.append({'path':rel,'sha256':actual,'unchanged':actual==expected})
  if actual!=expected:errors.append('accepted_input_changed:'+rel)
 now={r['id']:r for r in current['results']}
 for old in historical['results']:
  new=now.get(old['id']);unchanged=bool(new) and semantic(old)==semantic(new)
  changed=[k for k in old if k!='translations' and semantic(old[k])!=semantic((new or {}).get(k))]
  results.append({'id':old['id'],'semantic_fields_unchanged':unchanged,'changed_fields':changed})
  if not unchanged:errors.append('accepted_result_changed:'+old['id'])
 now_shared={r['id']:r for r in current['shared_proofs']}
 for old in historical['shared_proofs']:
  new=now_shared.get(old['id']);unchanged=bool(new) and semantic(old)==semantic(new)
  shared.append({'id':old['id'],'semantic_fields_unchanged':unchanged})
  if not unchanged:errors.append('accepted_shared_proof_changed:'+old['id'])
 unmapped=[ident for ident in baseline['unmapped_lean_targets'] if ident in now and not now[ident].get('lean',{}).get('declarations')]
 if unmapped!=baseline['unmapped_lean_targets']:errors.append('accepted_unmapped_target_status_changed')
 report={'status':'failed' if errors else 'passed','scope':'accepted_six_paper_sources_rewrites_and_machine_states_preserved_english_display_updates_allowed',
  'baseline_commit':baseline['baseline_commit'],'baseline_sha256':hashlib.sha256(BASELINE.read_bytes()).hexdigest(),
  'current_full_content_sha256':hashlib.sha256((ROOT/'reader/data/full-content.json').read_bytes()).hexdigest(),
  'input_hashes':input_hashes(Path(__file__).resolve(),ROOT/'reader/evidence_paths.py',BASELINE,ROOT/'reader/data/full-content.json'),
  'inputs':inputs,'results':results,'shared_proofs':shared,'unmapped_lean_targets':unmapped,'errors':errors}
 (EVIDENCE/'six-paper-preservation-checks.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
 return report

if __name__=='__main__':
 report=check_preservation();print(json.dumps({'status':report['status'],'old_results':len(report['results']),'old_unmapped_targets':len(report['unmapped_lean_targets']),'errors':report['errors']},ensure_ascii=False));raise SystemExit(bool(report['errors']))
