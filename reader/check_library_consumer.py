#!/usr/bin/env python3
"""Compile a real downstream direct-import proof and export its actual Lean type.

Run after sourcing scripts/env.sh. This neither modifies the base API catalog nor
changes any paper's mathematical status. All generated files stay in this project.
"""
import datetime
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'reader/architecture'))
from paper_agent import PaperPackage
from evidence_paths import EVIDENCE, input_hashes

MODULE = 'Harsanyi.Extensions.RobustnessFinite'
DECLARATION = 'DirectImportConsumer.affine_masked_pair_interaction'
LIBRARY_NAMES = [
    'Harsanyi.Robustness.pairDelta_baseline',
    'Harsanyi.Robustness.pairDelta_smul',
    'Harsanyi.Robustness.average_smul',
]
CONSUMER = ROOT / 'examples/library-consumer/ExtensionConsumer.lean'


def main():
    spec = importlib.util.spec_from_file_location('consumer_lean_audit', ROOT / 'scripts/verify-lean.py')
    audit_helper = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(audit_helper)
    package = PaperPackage()
    available = {row['name']: row for row in package.library()['extension_declarations']}
    checks = []
    for name in LIBRARY_NAMES:
        row = available.get(name, {})
        evidence = row.get('current_evidence', {})
        checks.append({'name': 'current-public-import:' + name,
                       'passed': row.get('import') == MODULE and bool(row.get('signature'))
                       and evidence.get('compilation') == 'passed'
                       and evidence.get('freshness') == 'current'})

    generated = ROOT / '.tmp/direct-import-consumer'
    generated.mkdir(parents=True, exist_ok=True)
    audit_file = generated / 'Audit.lean'
    export = audit_helper.lean_export([], [DECLARATION])
    # The exact consumer proof is compiled again with Lean's own type/axiom
    # exporter. Move its additional import to the beginning of the generated file.
    audit_file.write_text('import Lean.Util.CollectAxioms\n' + CONSUMER.read_text()
                          + export.replace('import Lean.Util.CollectAxioms\n', '', 1))
    source_paths = audit_helper.local_import_closure('lean/HarsanyiLib', [MODULE])
    for base in ['lean/HarsanyiLib', 'examples/library-consumer']:
        source_paths.extend(ROOT / base / name for name in
                            ['lakefile.toml', 'lean-toolchain', 'lake-manifest.json'])
    source_paths.extend([CONSUMER, Path(__file__).resolve(), ROOT / 'scripts/verify-lean.py',
                         ROOT / 'scripts/env.sh', ROOT / 'reader/evidence_paths.py'])
    source_paths.extend(ROOT.glob('locks/lean*.json'))
    source_paths = sorted(set(source_paths))
    source_files = [{'path': str(path.relative_to(ROOT)), 'sha256': audit_helper.sha(path)}
                    for path in source_paths]
    before = input_hashes(*source_paths)
    api_paths = [ROOT / 'reader/data/full-content.json', ROOT / 'reader/architecture/paper_agent.py']
    api_paths.extend(ROOT / available[name]['report_path'] for name in LIBRARY_NAMES if name in available)
    api_inputs = input_hashes(*sorted(set(api_paths)))
    commands = []
    output_hashes = {}

    def run(argv, cwd, label):
        log = EVIDENCE / ('direct-import-consumer-' + label + '.log')
        try:
            result = subprocess.run(argv, cwd=ROOT / cwd, text=True, stdout=subprocess.PIPE,
                                    stderr=subprocess.STDOUT, check=False)
            output, code = result.stdout, result.returncode
        except OSError as error:
            output, code = str(error), 127
        log.write_text(output)
        commands.append({'cwd': cwd, 'argv': argv, 'exit_code': code,
                         'log_path': str(log.relative_to(ROOT))})
        output_hashes.update(input_hashes(log))
        checks.append({'name': label, 'passed': code == 0})
        return output, code

    version, _ = run(['lean', '--version'], '.', 'toolchain')
    _, build_code = run(['lake', 'build', MODULE], 'lean/HarsanyiLib', 'public-module-build')
    exported = []
    if build_code == 0:
        run(['lake', 'env', 'lean', 'ExtensionConsumer.lean'],
            'examples/library-consumer', 'compile')
        output, _ = run(['lake', 'env', 'lean', str(audit_file)],
                        'examples/library-consumer', 'actual-type-and-axioms')
        exported = [json.loads(line.removeprefix('ARCHIVE_API:'))
                    for line in output.splitlines() if line.startswith('ARCHIVE_API:')]
    good_export = len(exported) == 1 and exported[0].get('name') == DECLARATION
    checks.append({'name': 'exact-declaration-exported-by-Lean', 'passed': good_export})
    if good_export:
        actual = exported[0]
        axioms = actual.get('axioms')
        good = (actual.get('kind') == 'theorem' and bool(actual.get('signature'))
                and isinstance(axioms, list) and set(axioms) <= audit_helper.WHITELIST)
        checks.append({'name': 'actual-proof-and-transitive-axioms', 'passed': good})
        actual.update({'source_path': str(CONSUMER.relative_to(ROOT)),
                       'line': next(i for i, line in enumerate(CONSUMER.read_text().splitlines(), 1)
                                    if line.startswith('theorem affine_masked_pair_interaction')),
                       'status': 'passed' if good else 'failed'})
    after = input_hashes(*source_paths)
    checks.append({'name': 'all-consumed-inputs-unchanged',
                   'passed': before == after and api_inputs == input_hashes(*sorted(set(api_paths)))})
    fingerprint = hashlib.sha256(json.dumps(source_files, ensure_ascii=False, sort_keys=True,
                                            separators=(',', ':')).encode()).hexdigest()
    report = {
        'schema_version': 1, 'build_id': 'direct-import-consumer-20261001',
        'generated_at': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'status': 'passed' if all(check['passed'] for check in checks) else 'failed',
        'verification_scope': 'independent_downstream_proof_using_one_current_public_extension',
        'meaning': 'Verifies this finite-game consumer proof, not completion of any original paper theorem.',
        'import': MODULE, 'library_declarations': LIBRARY_NAMES,
        'definition_adapter': 'g(S)=v(mask(S)); the empty-set output may be nonzero.',
        'assumptions': ['A finite player set N and decidable equality on the player type.',
                        'A masking function on finite player sets and a real-valued model output.',
                        'The library finite-context average has value zero for an empty context family.'],
        'not_covered': ['An original context quotient whose denominator is zero.',
                        'A source claim about asymptotic sparsity or a neural-network training procedure.'],
        'toolchain': version.strip(), 'lean_version': '4.24.0',
        'mathlib_revision': audit_helper.MATHLIB_REV,
        'axiom_whitelist': sorted(audit_helper.WHITELIST),
        'source_files': source_files, 'source_fingerprint': fingerprint,
        'snapshot_hashes': {'before': before, 'after': after}, 'api_input_hashes': api_inputs,
        'generated_audit_hashes': input_hashes(audit_file), 'output_hashes': output_hashes,
        'commands': commands, 'declarations': exported, 'checks': checks,
    }
    target = EVIDENCE / 'direct-import-consumer-checks.json'
    target.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'status': report['status'], 'checks': len(checks),
                      'report_path': str(target.relative_to(ROOT)),
                      'failures': [check for check in checks if not check['passed']]}))
    return int(report['status'] != 'passed')


if __name__ == '__main__':
    raise SystemExit(main())
