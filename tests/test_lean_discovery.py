"""The base audit discovers its import closure, with independent modules excluded."""
import importlib.util
from pathlib import Path
PROJECT=Path(__file__).resolve().parents[1]

def verifier(tmp_path):
    spec=importlib.util.spec_from_file_location('verify_import_closure',PROJECT/'scripts/verify-lean.py')
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    module.ROOT=tmp_path;module.PACKAGES=[('pkg',['Entry'],'Fixture')]
    base=tmp_path/'pkg';base.mkdir()
    (base/'Entry.lean').write_text('import A\n/- outer /- nested -/ import Unused -/\nnamespace Fixture\ndef entry := 0\n')
    (base/'A.lean').write_text('import Mathlib\nnamespace Fixture\ntheorem a : True := True.intro\n')
    (base/'Unused.lean').write_text('namespace Fixture\ndef independent := 0\n')
    (base/'lakefile.toml').write_text('name="fixture"\n')
    (tmp_path/'scripts').mkdir();(tmp_path/'scripts/verify-lean.sh').write_text('fixture script\n')
    # snapshot binds the actual script itself; use a project-local fixture copy.
    module.__file__=str(tmp_path/'scripts/verify-lean.py');Path(module.__file__).write_text('fixture audit script\n')
    return module,base

def test_discovery_uses_reachable_local_modules(tmp_path):
    module,base=verifier(tmp_path)
    assert [p.name for p in module.local_import_closure('pkg',['Entry'])]==['A.lean','Entry.lean']
    assert {d['name'] for d in module.discover()}=={'Fixture.entry','Fixture.a'}

def test_snapshot_binds_audited_scope_without_unrelated_extensions(tmp_path):
    module,base=verifier(tmp_path);files,before=module.snapshot()
    (base/'Unused.lean').write_text('namespace Fixture\ndef independent := 1\n')
    assert module.snapshot()==(files,before)
    (base/'A.lean').write_text((base/'A.lean').read_text()+'-- relevant change\n')
    assert module.snapshot()[1]!=before
