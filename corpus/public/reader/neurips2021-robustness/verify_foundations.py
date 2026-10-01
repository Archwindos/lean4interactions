#!/usr/bin/env python3
"""Actual Lean compilation, exact declaration types, dependencies and transitive axioms."""
from pathlib import Path
import os,json,re,hashlib,subprocess,datetime,sys
R=Path.cwd();pid=sys.argv[1] if len(sys.argv)>1 else 'neurips2021-robustness'
module,ns={'neurips2021-robustness':('RobustnessFinite','Harsanyi.Robustness'),'icml2022-transformation':('TransformationEntropy','Harsanyi.Entropy'),'icml2023-decoder':('DecoderFrequency','Harsanyi.Frequency')}[pid]
D=R/'corpus/public/reader'/pid;V=D/'verification';L=R/'lean/HarsanyiLib';M=L/'Harsanyi/Extensions'/f'{module}.lean';V.mkdir(exist_ok=True)
transitive=set()
def walk(p):
 if p in transitive:return
 transitive.add(p)
 for line in p.read_text().splitlines():
  if line.startswith('import Harsanyi.'):
   walk(L/(line.removeprefix('import ').strip().replace('.','/')+'.lean'))
walk(M)
names=[];locations={}
for ln,line in enumerate(M.read_text().splitlines(),1):
 m=re.match(r'\s*(?:noncomputable )?(?:def|theorem|abbrev) (\w+)',line)
 if m:
  n=ns+'.'+m[1];names.append(n);locations[n]=(str(M.relative_to(R)),ln)
content=json.load(open(D/'content.json'))
requested=set()
def visit(x):
 if isinstance(x,dict):
  for k,v in x.items():
   if k in ['lean_refs','declarations','lean_names']:
    for n in v:
     n=n if isinstance(n,str) else n.get('declaration')
     if n:requested.add(n)
   else:visit(v)
 elif isinstance(x,list):
  for v in x:visit(v)
visit(content)
for n in sorted(requested-set(names)):
 for p in transitive:
  for ln,line in enumerate(p.read_text().splitlines(),1):
   if re.match(r'\s*(?:noncomputable )?(?:def|theorem|abbrev) '+re.escape(n.split('.')[-1])+r'\b',line):
    names.append(n);locations[n]=(str(p.relative_to(R)),ln);break
  if n in locations:break
if requested-set(names):raise RuntimeError('Unlocated declaration refs: '+str(requested-set(names)))
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
    liftM <| IO.println ("FOUNDATIONS_API:" ++ (Json.mkObj [
      ("name", toJson name.toString), ("signature", toJson signature.pretty),
      ("kind", toJson kind), ("axioms", toJson (axioms.map Name.toString)),
      ("dependencies", toJson (deps.map Name.toString))]).compress)
'''.replace('NAMES',', '.join('`'+n for n in names))
aud=V/f'Audit{module}.lean';aud.write_text('import Lean.Util.CollectAxioms\nimport Harsanyi.Extensions.'+module+'\n'+collector)
track=sorted(transitive|{aud,Path(__file__).resolve(),L/'lean-toolchain',L/'lakefile.toml',L/'lake-manifest.json',R/'locks/lean-dependencies.json'}|set((D/'sources').glob('*.pdf')))
def snap():
 files=[dict(path=str(p.relative_to(R)),sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in track]
 return files,hashlib.sha256(json.dumps(files,sort_keys=True,separators=(',',':')).encode()).hexdigest()
initial=snap();commands=[]
def run(argv,label):
 out=subprocess.run(argv,cwd=R,env=os.environ.copy(),text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
 log=V/(label+'.log');log.write_text(out.stdout);commands.append(dict(cwd=str(R),argv=argv,exit_code=out.returncode,log_path=str(log.relative_to(R))));print(pid,label,out.returncode,flush=True);return out
version=run(['lean','--version'],'toolchain');run(['lake','-d',str(L),'build','Harsanyi.Extensions.'+module],'build');run(['lake','-d',str(L),'env','lean',str(M)],'adapter');audit=run(['lake','-d',str(L),'env','lean',str(aud)],'axioms')
rows=[json.loads(s.removeprefix('FOUNDATIONS_API:')) for s in audit.stdout.splitlines() if s.startswith('FOUNDATIONS_API:')]
white={'propext','Classical.choice','Quot.sound'};stable=initial==snap();clean=all(c['exit_code']==0 for c in commands)
for row in rows:
 row['source_path'],row['line']=locations[row['name']];row['declaration']=row['name'];row['statement']=row['signature'];row['axiom_audit_passed']=set(row['axioms'])<=white;row['source_sha256']=hashlib.sha256((R/row['source_path']).read_bytes()).hexdigest();row['dependencies']=sorted(set(row['dependencies']));row['status']='passed' if clean and stable and row['axiom_audit_passed'] else 'failed';row['evidence_role']='definition' if row['kind']!='theorem' else 'counterexample' if 'counterexample' in row['name'] else 'proved_finite_statement'
passed=clean and stable and len(rows)==len(names) and all(r['axiom_audit_passed'] for r in rows)
report=dict(schema_version=1,build_id=pid+'-formal-20261001',status='passed' if passed else 'failed',generated_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),toolchain=version.stdout.strip(),mathlib_revision='f897ebcf72cd16f89ab4577d0c826cd14afaafc7',source_files=initial[0],source_fingerprint=initial[1],sources_unchanged_during_verification=stable,commands=commands,axiom_whitelist=sorted(white),declarations=rows,checked_declarations=len(rows),expected_declarations=len(names),source_semantics_automatically_verified=False,proof_scope_note='Types and transitive axioms are collected from real Lean constants. The finite statements, paper adapters, counterexamples and source-domain analyses have different evidence roles. No original false statement is claimed proved; declaration count does not equal paper-target count.')
(V/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');(V/'catalog.json').write_text(json.dumps(dict(declarations=rows),ensure_ascii=False,indent=2)+'\n');print(pid,'passed',passed,'declarations',len(rows));raise SystemExit(0 if passed else 1)
