#!/usr/bin/env python3
"""Build all packages, ask Lean for actual types/axioms, and bind evidence to sources.

Only the Python standard library is needed. This script never installs dependencies.
`#print axioms` and Lean.collectAxioms both run in the built environment.
"""
import datetime
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tomllib

ROOT = Path(__file__).resolve().parents[1]
PACKAGES = [
    ("lean/HarsanyiLib", ["Harsanyi"], "Harsanyi"),
    ("lean/PaperProofs", ["Papers"], "PaperProofs"),
    ("examples/library-consumer", ["Consumer", "Main"], "LibraryConsumer"),
]
WHITELIST = {"propext", "Classical.choice", "Quot.sound"}
MATHLIB_REV = "f897ebcf72cd16f89ab4577d0c826cd14afaafc7"
LIBRARY_VERSION = tomllib.loads((ROOT / "lean/HarsanyiLib/lakefile.toml").read_text())["version"]

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def local_import_closure(package,entrypoints):
    """Resolve only this package's modules actually reachable from audit imports."""
    base=ROOT/package;pending=list(entrypoints);seen=set();paths=[]
    while pending:
        module=pending.pop()
        if module in seen:continue
        seen.add(module)
        path=base/Path(*module.split('.')).with_suffix('.lean')
        if not path.is_file():continue  # Lean/Mathlib/dependency modules are audited transitively by Lean.
        if path.is_symlink() or not path.resolve().is_relative_to(base.resolve()):raise ValueError('Local import escaped package: '+module)
        paths.append(path)
        text=path.read_text();depth=0;clean=[];index=0
        # Lean block comments can nest. Ignore their import-looking examples.
        while index<len(text):
            token=text[index:index+2]
            if token=='/-':depth+=1;index+=2;continue
            if depth and token=='-/':depth-=1;index+=2;continue
            if text[index]=='\n':clean.append('\n')
            elif not depth:clean.append(text[index])
            index+=1
        for line in ''.join(clean).splitlines():
            match=re.match(r'^\s*import\s+(.+)$',line.split('--',1)[0])
            if match:pending.extend(match.group(1).split())
    missing=[module for module in entrypoints if not (base/Path(*module.split('.')).with_suffix('.lean')).is_file()]
    if missing:raise ValueError('Missing audit entrypoints: '+', '.join(missing))
    return sorted(paths)

def discover():
    records = []
    for package, imports, namespace in PACKAGES:
        for path in local_import_closure(package, imports):
            text = path.read_text()
            current_namespace = None
            current_structure = None
            module = ".".join(path.relative_to(ROOT / package).with_suffix("").parts)
            for line, value in enumerate(text.splitlines(), 1):
                ns = re.match(r"^namespace\s+(\S+)", value)
                if ns:
                    current_namespace = ns.group(1)
                if value and not value[0].isspace() and not value.startswith("--"):
                    current_structure = None
                structure = re.match(r"^(?:@\[[^]]+\]\s*)?(?:private\s+)?structure\s+(\w+)", value)
                if structure:
                    current_structure = (current_namespace + "." if current_namespace else "") + structure.group(1)
                    for name in (current_structure, current_structure + ".mk"):
                        records.append({"name": name, "package": package, "module": module,
                                        "source_path": str(path.relative_to(ROOT)), "line": line})
                field = re.match(r"^  (\w+)\s*:", value) if current_structure else None
                if field:
                    records.append({"name": current_structure + "." + field.group(1), "package": package,
                                    "module": module, "source_path": str(path.relative_to(ROOT)), "line": line})
                match = re.match(r"^(?:@\[[^]]+\]\s*)?(?:noncomputable\s+)?(?:def|abbrev|theorem|lemma)\s+(\w+)", value)
                if match:
                    name = (current_namespace + "." if current_namespace else "") + match.group(1)
                    records.append({"name": name, "package": package, "module": module,
                                    "source_path": str(path.relative_to(ROOT)), "line": line})
    return records

def snapshot():
    paths = []
    for package, imports, _ in PACKAGES:
        paths.extend(local_import_closure(package,imports))
        for name in ['lakefile.toml','lean-toolchain','lake-manifest.json']:
            path=ROOT/package/name
            if path.is_file():paths.append(path)
    paths.extend(ROOT.glob("locks/lean*.json"))
    paths.extend([Path(__file__).resolve(), ROOT / "scripts/verify-lean.sh"])
    files = [{"path": str(p.relative_to(ROOT)), "sha256": sha(p)} for p in set(paths)]
    files.sort(key=lambda item: item["path"])
    encoded = json.dumps(files, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
    return files, hashlib.sha256(encoded).hexdigest()

def lean_export(imports, names):
    prefix = "\n".join("import " + module for module in imports)
    quoted_names = ", ".join("`" + name for name in names)
    body = r'''
import Lean.Util.CollectAxioms
open Lean Elab Command Meta
set_option pp.universes true
set_option pp.fullNames true
set_option pp.piBinderTypes true
set_option pp.funBinderTypes true
run_cmd liftTermElabM do
  for name in #[NAMES] do
    let info ← getConstInfo name
    let signature ← ppExpr info.type
    let axioms ← Lean.collectAxioms name
    let deps := info.type.getUsedConstants ++ (info.value?.map Expr.getUsedConstants).getD #[]
    let isProjection := ((← getEnv).getProjectionFnInfo? name).isSome
    let kind := if isProjection then "projection" else match info with
      | .thmInfo _ => "theorem"
      | .inductInfo _ => "type"
      | .ctorInfo _ => "constructor"
      | _ => "definition"
    let row := Json.mkObj [
      ("name", toJson name.toString),
      ("signature", toJson signature.pretty),
      ("kind", toJson kind),
      ("axioms", toJson (axioms.map Name.toString)),
      ("dependencies", toJson (deps.map Name.toString)),
      ("universe_parameters", toJson (info.levelParams.map Name.toString))]
    liftM <| IO.println ("ARCHIVE_API:" ++ row.compress)
'''.replace("NAMES", quoted_names)
    return prefix + "\n" + body + "\n" + "\n".join("#print axioms " + name for name in names) + "\n"

def main():
    os.environ.update({"ELAN_HOME": str(ROOT / ".tools/elan"),
                       "MATHLIB_CACHE_DIR": str(ROOT / ".cache/mathlib"),
                       "TMPDIR": str(ROOT / ".tmp"),
                       "XDG_CACHE_HOME": str(ROOT / ".cache/xdg"),
                       "MATHLIB_NO_CACHE_ON_UPDATE": "1"})
    os.environ["PATH"] = str(ROOT / ".tools/lean/bin") + os.pathsep + os.environ["PATH"]
    generated = datetime.datetime.now(datetime.timezone.utc)
    build_id = generated.strftime("%Y%m%dT%H%M%S") + "-" + str(os.getpid())
    report_dir = ROOT / "reports/lean" / build_id
    report_dir.mkdir(parents=True)
    (ROOT / ".tmp").mkdir(exist_ok=True)
    declarations = discover()
    initial_source_files, initial_fingerprint = snapshot()
    commands = []
    exported = []
    failed = len(declarations) == 0
    def run(args, cwd, label):
        nonlocal failed
        log = report_dir / (label + ".log")
        try:
            result = subprocess.run(args, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                    text=True, check=False)
            output, code = result.stdout, result.returncode
        except OSError as exc:
            output, code = str(exc), 127
        log.write_text(output)
        commands.append({"cwd": str(cwd.relative_to(ROOT)), "argv": args, "exit_code": code,
                         "log_path": str(log.relative_to(ROOT))})
        if code:
            failed = True
            print(f"FAILED {label}; see {log.relative_to(ROOT)}", flush=True)
        else:
            print(f"passed {label}", flush=True)
        return output, code
    version, _ = run(["lean", "--version"], ROOT, "toolchain")
    for index, (package, imports, _) in enumerate(PACKAGES):
        cwd = ROOT / package
        _, code = run(["lake", "build"], cwd, f"build-{index}")
        if code:
            continue
        records = [d for d in declarations if d["package"] == package]
        audit = ROOT / ".tmp" / ("audit-" + build_id + "-" + str(index) + ".lean")
        audit.write_text(lean_export(imports, [d["name"] for d in records]))
        output, code = run(["lake", "env", "lean", str(audit)], cwd, f"audit-{index}")
        if code:
            continue
        raw = [json.loads(line.removeprefix("ARCHIVE_API:")) for line in output.splitlines()
               if line.startswith("ARCHIVE_API:")]
        by_name = {d["name"]: d for d in raw}
        if set(by_name) != {d["name"] for d in records}:
            failed = True
        for record in records:
            data = by_name.get(record["name"], {})
            axioms = data.get("axioms")
            good = isinstance(axioms, list) and all(isinstance(a, str) for a in axioms) and set(axioms) <= WHITELIST
            failed |= not good
            exported.append({**record, **data, "dependencies": sorted(set(data.get("dependencies", []))),
                             "status": "passed" if good else "failed"})
    if not failed:
        run(["lake", "exe", "demo"], ROOT / "examples/library-consumer", "consumer-demo")
    source_files, fingerprint = snapshot()
    if source_files != initial_source_files or fingerprint != initial_fingerprint:
        failed = True
        print("Source files changed during verification; report is failed.", flush=True)
    report = {"schema_version": 1, "build_id": build_id, "status": "failed" if failed else "passed",
              "generated_at": generated.isoformat(), "source_fingerprint": fingerprint,
              "source_files": source_files, "toolchain": version.strip(), "lean_version": "4.24.0",
              "mathlib_revision": MATHLIB_REV, "commands": commands, "declarations": exported,
              "axiom_whitelist": sorted(WHITELIST),
              "verification_scope":"actual_local_import_closure_of_audit_entrypoints",
              "entrypoints": [{"package":package,"imports":imports,"local_source_files":[str(p.relative_to(ROOT)) for p in local_import_closure(package,imports)]} for package,imports,_ in PACKAGES]}
    relative_report = str((report_dir / "report.json").relative_to(ROOT))
    (report_dir / "report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    (ROOT / "reports/lean/latest.json").write_text(json.dumps({"report_path": relative_report}, indent=2) + "\n")
    if not failed:
        descriptions_path = ROOT / "catalog/descriptions.json"
        descriptions = json.loads(descriptions_path.read_text()) if descriptions_path.exists() else {}
        public = []
        for item in exported:
            if item["package"] != "lean/HarsanyiLib":
                continue
            description = descriptions.get(item["name"], {})
            public.append({**item, "title": description.get("title", item["name"]),
                           "summary": description.get("summary", ""),
                           "summary_en": description.get("summary_en", item["name"].replace("_", " ")),
                           "statement_tex": description.get("statement_tex"),
                           "assumptions": description.get("assumptions", []),
                           "theorem_id": description.get("theorem_id"),
                           "proof_id": description.get("proof_id"),
                           "tags": description.get("tags", []), "visibility": "public",
                           "source_hash": sha(ROOT / item["source_path"]),
                           "import": item["module"],
                           "mathlib_correspondence": description.get("mathlib_correspondence", []),
                           "symbol_ids": description.get("symbol_ids", []),
                           "shared_proof_ids": description.get("shared_proof_ids", []),
                           "related_lemmas": [d for d in item["dependencies"] if d.startswith("Harsanyi.")],
                           "example_paths": description.get("example_paths", []),
                           "api_stability": "experimental-" + ".".join(LIBRARY_VERSION.split('.')[:2]), "deprecated": False,
                           "report_id": build_id,
                           "verification_status": "verified", "verification_report": relative_report,
                           "library_version": LIBRARY_VERSION})
        catalog = {"schema_version": 1, "library": "HarsanyiLib", "library_version": LIBRARY_VERSION,
                   "lean_version": "4.24.0", "mathlib_revision": MATHLIB_REV,
                   "source_fingerprint": fingerprint, "source_files": source_files,
                   "verification_report": relative_report, "declarations": public,
                   "verification_scope":report["verification_scope"],"entrypoints":report["entrypoints"]}
        (ROOT / "catalog/library.json").write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + "\n")
    print(relative_report, flush=True)
    return int(failed)

if __name__ == "__main__":
    sys.exit(main())
