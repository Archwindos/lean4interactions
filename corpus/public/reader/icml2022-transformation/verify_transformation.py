#!/usr/bin/env python3
"""Compile the real paper adapter; collect exact constant types and axioms."""
from pathlib import Path
import os,json,re,hashlib,subprocess,datetime
R=Path.cwd();D=R/'corpus/public/reader/icml2022-transformation';V=D/'verification';V.mkdir(exist_ok=True)
L=R/'lean/HarsanyiLib';M=D/'lean/PaperTransformation.lean';transitive=set()
def walk(p):
 if p in transitive:return
 transitive.add(p)
 for line in p.read_text().splitlines():
  if line.startswith('import Harsanyi.'):
   walk(L/(line.removeprefix('import ').strip().replace('.','/')+'.lean'))
walk(M);names=[];locations={}
for p in sorted(transitive):
 ns='PaperTransformation' if p==M else 'Harsanyi.GatedAffine' if p.stem in ['TransformationAffine','TransformationOperators'] else 'Harsanyi.Entropy'
 for ln,line in enumerate(p.read_text().splitlines(),1):
  m=re.match(r'\s*(?:noncomputable )?(?:def|theorem|abbrev|structure) (\w+)',line)
  if m:
   n=ns+'.'+m[1];names.append(n);locations[n]=(str(p.relative_to(R)),ln)
assert len(names)==len(set(names))
c=json.load(open(D/'content.json'));requested=set()
def visit(x):
 if isinstance(x,dict):
  for k,v in x.items():
   if k in ['lean_refs','declarations']:
    for n in v:
     n=n if isinstance(n,str) else n.get('declaration')
     if n:requested.add(n)
   else:visit(v)
 elif isinstance(x,list):
  for v in x:visit(v)
visit(c);assert requested<=set(names),requested-set(names)
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
    liftM <| IO.println ("TRANSFORMATION_API:" ++ (Json.mkObj [
      ("name", toJson name.toString), ("signature", toJson signature.pretty),
      ("kind", toJson kind), ("axioms", toJson (axioms.map Name.toString)),
      ("dependencies", toJson (deps.map Name.toString))]).compress)
'''.replace('NAMES',', '.join('`'+n for n in names))
aud=V/'AuditPaperTransformation.lean';aud.write_text('import Lean.Util.CollectAxioms\n'+M.read_text()+'\n'+collector)
track=sorted(transitive|{aud,Path(__file__).resolve(),L/'lean-toolchain',L/'lakefile.toml',L/'lake-manifest.json',R/'locks/lean-dependencies.json'}|set((D/'sources').glob('*.pdf')))
def snap():
 files=[dict(path=str(p.relative_to(R)),sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in track]
 return files,hashlib.sha256(json.dumps(files,sort_keys=True,separators=(',',':')).encode()).hexdigest()
initial=snap();commands=[]
def run(argv,label):
 out=subprocess.run(argv,cwd=R,env=os.environ.copy(),text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
 log=V/(label+'.log');log.write_text(out.stdout);commands.append(dict(cwd=str(R),argv=argv,exit_code=out.returncode,log_path=str(log.relative_to(R))));print(label,out.returncode,flush=True);return out
version=run(['lean','--version'],'toolchain')
mods=[line.removeprefix('import ').strip() for line in M.read_text().splitlines() if line.startswith('import Harsanyi.')]
run(['lake','-d',str(L),'build',*mods],'build')
run(['lake','-d',str(L),'env','lean',str(M)],'adapter')
audit=run(['lake','-d',str(L),'env','lean',str(aud)],'axioms')
rows=[json.loads(s.removeprefix('TRANSFORMATION_API:')) for s in audit.stdout.splitlines() if s.startswith('TRANSFORMATION_API:')]
white={'propext','Classical.choice','Quot.sound'};stable=initial==snap();clean=all(c['exit_code']==0 for c in commands)
for row in rows:
 row['source_path'],row['line']=locations[row['name']];row['declaration']=row['name'];row['statement']=row['signature'];row['axiom_audit_passed']=set(row['axioms'])<=white;row['source_sha256']=hashlib.sha256((R/row['source_path']).read_bytes()).hexdigest();row['dependencies']=sorted(set(row['dependencies']));row['status']='passed' if clean and stable and row['axiom_audit_passed'] else 'failed'
passed=clean and stable and len(rows)==len(names) and all(r['axiom_audit_passed'] for r in rows)
report=dict(schema_version=1,build_id='icml2022-transformation-formal-20261001',status='passed' if passed else 'failed',generated_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),toolchain=version.stdout.strip(),mathlib_revision='f897ebcf72cd16f89ab4577d0c826cd14afaafc7',source_files=initial[0],source_fingerprint=initial[1],sources_unchanged_during_verification=stable,commands=commands,axiom_whitelist=sorted(white),declarations=rows,checked_declarations=len(rows),expected_declarations=len(names),source_semantics_automatically_verified=False,proof_scope_note='Exact types and transitive axioms are collected from actual compiled Lean constants. Whole paper targets, auxiliary components and counterexamples have explicit different roles in content; counts do not establish semantic source equivalence.')
(V/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');(V/'catalog.json').write_text(json.dumps(dict(declarations=rows),ensure_ascii=False,indent=2)+'\n')
print('passed',passed,'declarations',len(rows));raise SystemExit(0 if passed else 1)
