#!/usr/bin/env python3
"""Compile only the selected reader adapters and audit actual transitive axioms."""
from pathlib import Path
import datetime, hashlib, json, os, re, subprocess, sys
ROOT=Path(os.environ['ARCHIVE_PROJECT_ROOT']).resolve()
BASE=ROOT/'research/reader-v2-20260930/math'
OUT=BASE/'verification'
OUT.mkdir(exist_ok=True)
SOURCE=BASE/'lean/ReaderAdapters.lean'
PUBLIC_NAMES=['ReaderV2.'+m.group(1) for m in re.finditer(r'^(?:noncomputable )?(?:def|theorem) (\w+)',SOURCE.read_text(),re.M)]
LIBRARY_NAMES=['Harsanyi.interaction_empty','Harsanyi.centered_empty','Harsanyi.interaction_insert','Harsanyi.reconstruction','Harsanyi.interaction_reconstruct','Harsanyi.reconstruction_unique','Harsanyi.interaction_congr','Harsanyi.interaction_const','Harsanyi.interaction_centered','Harsanyi.interaction_centered_nonempty']
NAMES=PUBLIC_NAMES+LIBRARY_NAMES
collector=r'''
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
    liftM <| IO.println ("READER_V2_API:" ++ (Json.mkObj [
      ("name", toJson name.toString), ("signature", toJson signature.pretty),
      ("kind", toJson kind), ("axioms", toJson (axioms.map Name.toString)),
      ("dependencies", toJson (deps.map Name.toString))]).compress)
'''.replace('NAMES',', '.join('`'+n for n in NAMES))
AUDIT=OUT/'AuditPublic.lean'
AUDIT.write_text('import Lean.Util.CollectAxioms\n'+SOURCE.read_text()+collector+'\n'+'\n'.join('#print axioms '+n for n in NAMES)+'\n')
LIB=ROOT/'lean/HarsanyiLib'
track=[SOURCE,AUDIT,Path(__file__).resolve(),LIB/'lakefile.toml',LIB/'lake-manifest.json',LIB/'lean-toolchain',ROOT/'locks/lean-dependencies.json']
track.extend(LIB/'Harsanyi/Core'/f for f in ['Basic.lean','Mobius.lean','Properties.lean'])
def snapshot():
 rows=[{'path':str(p.relative_to(ROOT)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in sorted(track)]
 raw=json.dumps(rows,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
 return rows,hashlib.sha256(raw).hexdigest()
initial=snapshot()
commands=[]
def run(argv,label):
 r=subprocess.run(argv,cwd=ROOT,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
 log=OUT/(label+'.log');log.write_text(r.stdout)
 commands.append({'cwd':str(ROOT),'argv':argv,'exit_code':r.returncode,'log_path':str(log.relative_to(ROOT))})
 print(label,'passed' if r.returncode==0 else 'failed',flush=True)
 return r
version=run(['lean','--version'],'toolchain')
build=run(['lake','-d',str(LIB),'build','Harsanyi.Core.Properties'],'library-import-build')
compile=run(['lake','-d',str(LIB),'env','lean','-o',str(OUT/'ReaderAdapters.olean'),str(SOURCE)],'public-adapter-compile')
audit=run(['lake','-d',str(LIB),'env','lean',str(AUDIT)],'public-axiom-audit')
rows=[json.loads(line.removeprefix('READER_V2_API:')) for line in audit.stdout.splitlines() if line.startswith('READER_V2_API:')]
whitelist={'propext','Classical.choice','Quot.sound'}
source_lines={}
for path in [SOURCE]+list((LIB/'Harsanyi/Core').glob('*.lean')):
 namespace='ReaderV2' if path==SOURCE else 'Harsanyi'
 for lineno,line in enumerate(path.read_text().splitlines(),1):
  m=re.search(r'(?:def|theorem) (\w+)',line)
  if m:source_lines[namespace+'.'+m.group(1)]=(str(path.relative_to(ROOT)),lineno)
for row in rows:
 row['dependencies']=sorted(set(row['dependencies']))
 row['status']='passed' if set(row['axioms']) <= whitelist else 'failed'
 row['source_path'],row['line']=source_lines[row['name']]
 row['verification_scope']='selected_reader_adapter' if row['name'].startswith('ReaderV2.') else 'imported_public_library_declaration'
final=snapshot()
good=all(c['exit_code']==0 for c in commands) and len(rows)==len(NAMES) and set(r['name'] for r in rows)==set(NAMES) and all(r['status']=='passed' for r in rows) and initial==final
report={'schema_version':1,'build_id':'reader-v2-public-20260930','status':'passed' if good else 'failed','generated_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'toolchain':version.stdout.strip(),'lean_version':'4.24.0','mathlib_revision':'f897ebcf72cd16f89ab4577d0c826cd14afaafc7','source_files':final[0],'source_fingerprint':final[1],'commands':commands,'declarations':rows,'axiom_whitelist':sorted(whitelist),'scope':'selected CVPR2023 reconstruction/uniqueness, ICLR2024 Sparse centered reconstruction, ICLR2024 Generalizable Appendix C(1) AND subresult, and baseline adapters','source_semantics_automatically_verified':False,'excluded_scope':['full-paper claims','F11 full Theorem 2 AND-OR notation and original proof','experimental OR file','training/sparsity/approximation claims','implementation of a concrete DNN or concrete mask operation']}
(OUT/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print('declarations',len(rows),'status',report['status'],flush=True)
sys.exit(0 if good else 1)
