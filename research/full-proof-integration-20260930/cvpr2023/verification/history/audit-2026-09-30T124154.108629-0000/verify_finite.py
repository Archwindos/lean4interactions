#!/usr/bin/env python3
"""Compile the finite attribution modules and real paper adapters, then collect axioms."""
from pathlib import Path
import datetime
import hashlib
import json
import os
import re
import subprocess
import sys

ROOT = Path(os.environ['ARCHIVE_PROJECT_ROOT']).resolve()
BASE = ROOT / 'research/full-proof-integration-20260930/cvpr2023'
LIB = ROOT / 'lean/HarsanyiLib'
OUT = BASE / 'verification'
OUT.mkdir(exist_ok=True)
MODULES = [LIB / 'Harsanyi/Extensions/Attribution.lean', LIB / 'Harsanyi/Extensions/OrInteraction.lean']
ADAPTERS = [BASE / 'lean/FullCvpr.lean', BASE / 'lean/FullGeneralizable.lean']
CORE = sorted((LIB / 'Harsanyi/Core').glob('*.lean'))
SOURCE_LINES = {}
NAMES = []
for path in MODULES + ADAPTERS + CORE:
    namespace = 'FullCvpr' if path.name == 'FullCvpr.lean' else 'FullGeneralizable' if path.name == 'FullGeneralizable.lean' else 'Harsanyi'
    for lineno, line in enumerate(path.read_text().splitlines(), 1):
        match = re.match(r'^(?:noncomputable )?(?:def|theorem) (\w+)', line)
        if match:
            name = namespace + '.' + match.group(1)
            if name in SOURCE_LINES:
                raise RuntimeError('duplicate declaration: ' + name)
            SOURCE_LINES[name] = (str(path.relative_to(ROOT)), lineno)
            NAMES.append(name)

collector = r'''
open Lean Elab Command Meta
set_option pp.universes true
set_option pp.fullNames true
set_option pp.piBinderTypes true
run_cmd liftTermElabM do
  for name in #[NAMES] do
    let info ← getConstInfo name
    let signature ← ppExpr info.type
    let axioms ← Lean.collectAxioms name
    let deps := info.type.getUsedConstants ++ (info.value?.map Expr.getUsedConstants).getD #[]
    let kind := match info with | .thmInfo _ => "theorem" | _ => "definition"
    liftM <| IO.println ("FINITE_API:" ++ (Json.mkObj [
      ("name", toJson name.toString), ("signature", toJson signature.pretty),
      ("kind", toJson kind), ("axioms", toJson (axioms.map Name.toString)),
      ("dependencies", toJson (deps.map Name.toString))]).compress)
'''.replace('NAMES', ', '.join('`' + n for n in NAMES))
AUDIT = OUT / 'AuditFinite.lean'
body = '\n\n'.join('\n'.join(line for line in source.read_text().splitlines() if not line.startswith('import ')) for source in ADAPTERS)
AUDIT.write_text('import Lean.Util.CollectAxioms\nimport Harsanyi.Extensions.Attribution\nimport Harsanyi.Extensions.OrInteraction\n\n' + body + '\n' + collector + '\n')
track = MODULES + ADAPTERS + CORE + [AUDIT, Path(__file__).resolve(), LIB / 'lakefile.toml', LIB / 'lake-manifest.json', LIB / 'lean-toolchain', ROOT / 'locks/lean-dependencies.json']
track += [BASE / 'lean/SharedFinite.lean', BASE / 'lean/OrInteraction.lean']
track += [ROOT / 'research/paper-survey-20260930/earlier/venue-papers/sparse-cvpr2023-main/sparse-cvpr2023-main.pdf', ROOT / 'research/paper-survey-20260930/earlier/venue-papers/sparse-cvpr2023-supp/sparse-cvpr2023-supp.pdf', ROOT / 'research/paper-survey-20260930/recent/pdf/iclr2024-generalizable.pdf']

def snapshot():
    rows = [{'path': str(p.relative_to(ROOT)), 'sha256': hashlib.sha256(p.read_bytes()).hexdigest()} for p in sorted(set(track))]
    fingerprint = hashlib.sha256(json.dumps(rows, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()).hexdigest()
    return rows, fingerprint

initial = snapshot()
commands = []
def run(argv, label):
    result = subprocess.run(argv, cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    log = OUT / (label + '.log')
    log.write_text(result.stdout)
    commands.append({'cwd': str(ROOT), 'argv': argv, 'exit_code': result.returncode, 'log_path': str(log.relative_to(ROOT))})
    print(label, 'passed' if result.returncode == 0 else 'failed', flush=True)
    return result

version = run(['lean', '--version'], 'finite-toolchain')
run(['lake', '-d', str(LIB), 'build', 'Harsanyi.Extensions.Attribution', 'Harsanyi.Extensions.OrInteraction'], 'finite-public-module-build')
for source in ADAPTERS:
    run(['lake', '-d', str(LIB), 'env', 'lean', '-o', str(OUT / (source.stem + '.olean')), str(source)], source.stem + '-compile')
audit = run(['lake', '-d', str(LIB), 'env', 'lean', str(AUDIT)], 'finite-axiom-audit')
rows = [json.loads(line.removeprefix('FINITE_API:')) for line in audit.stdout.splitlines() if line.startswith('FINITE_API:')]
whitelist = {'propext', 'Classical.choice', 'Quot.sound'}
for row in rows:
    row['dependencies'] = sorted(set(row['dependencies']))
    row['status'] = 'passed' if set(row['axioms']) <= whitelist else 'failed'
    row['source_path'], row['line'] = SOURCE_LINES[row['name']]
    row['verification_scope'] = 'paper_adapter' if row['name'].startswith(('FullCvpr.', 'FullGeneralizable.')) else 'public_library_declaration'
final = snapshot()
staging_matches_public = (MODULES[0].read_bytes() == (BASE / 'lean/SharedFinite.lean').read_bytes() and MODULES[1].read_bytes() == (BASE / 'lean/OrInteraction.lean').read_bytes())
good = all(c['exit_code'] == 0 for c in commands) and len(rows) == len(NAMES) and set(r['name'] for r in rows) == set(NAMES) and all(r['status'] == 'passed' for r in rows) and initial == final and staging_matches_public
report = {'schema_version': 1, 'build_id': 'full-finite-proof-20260930', 'status': 'passed' if good else 'failed', 'generated_at': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'toolchain': version.stdout.strip(), 'lean_version': '4.24.0', 'mathlib_revision': 'f897ebcf72cd16f89ab4577d0c826cd14afaafc7', 'source_files': final[0], 'source_fingerprint': final[1], 'sources_unchanged_during_verification': initial == final, 'staging_matches_public': staging_matches_public, 'commands': commands, 'declarations': rows, 'axiom_whitelist': sorted(whitelist), 'scope': 'finite game properties, exact higher marginals, classical factorial Shapley/SII, positive-order STI, actual coordinate mask AND/OR reconstruction, CVPR finite family AOG and zero-baseline coordinate AddMul adapters, Generalizable finite targets', 'source_semantics_automatically_verified': False, 'excluded_scope': ['CVPR false empty-inclusive dummy proposition (only counterexample is verified)', 'CVPR truncated baseline-loss compound clause (full-vector subclaim alone is proved)', 'STI order zero and unverified conventions outside positive-order definition', 'training, sparsity assumptions, approximation, derivative cutoffs, and optimization/runtime claims', 'independent human semantic acceptance; Lean compilation alone does not establish transcription fidelity']}
(OUT / 'report.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
registry = {'schema_version': 1, 'registry_id': 'finite-attribution-20260930', 'build_id': report['build_id'], 'status': report['status'], 'report_path': str((OUT / 'report.json').relative_to(ROOT)), 'source_fingerprint': final[1], 'imports': ['Harsanyi.Extensions.Attribution', 'Harsanyi.Extensions.OrInteraction'], 'declarations': [r for r in rows if r['name'].startswith('Harsanyi.') and '/Extensions/' in r['source_path']]}
(BASE / 'registry.json').write_text(json.dumps(registry, ensure_ascii=False, indent=2) + '\n')
print('declarations', len(rows), '/', len(NAMES), 'status', report['status'], flush=True)
sys.exit(0 if good else 1)
