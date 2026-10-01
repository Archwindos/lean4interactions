#!/usr/bin/env python3
"""Actual Lean compilation, exact declaration types, dependencies and transitive axioms."""
from pathlib import Path
import os,json,re,hashlib,subprocess,datetime,sys
R=Path.cwd();pid='icml2023-decoder'
D=R/'corpus/public/reader'/pid;V=D/'verification';L=R/'lean/HarsanyiLib';V.mkdir(exist_ok=True)
modules=sorted((L/'Harsanyi/Extensions').glob('Decoder*.lean'))
M=D/'lean/PaperDecoder.lean'
transitive=set()
def walk(p):
 if p in transitive:return
 transitive.add(p)
 for line in p.read_text().splitlines():
  if line.startswith('import Harsanyi.'):
   walk(L/(line.removeprefix('import ').strip().replace('.','/')+'.lean'))
for p in modules+[M]:walk(p)
locations={};names=[]
def catalog(p):
 ns=''
 for ln,line in enumerate(p.read_text().splitlines(),1):
  if line.startswith('namespace '):ns=line.split()[1]
  m=re.match(r'\s*(?:noncomputable )?(?:def|theorem|lemma|abbrev) (\w+)',line)
  if m:
   name=ns+'.'+m[1];locations[name]=(str(p.relative_to(R)),ln)
   if p in modules or p==M:names.append(name)
for p in sorted(transitive):catalog(p)
content=json.load(open(D/'content.json'));requested=set()
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
if requested-set(locations):raise RuntimeError('Unlocated declaration refs: '+str(requested-set(locations)))
names=sorted(set(names)|requested)
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
aud=V/'AuditDecoder.lean';aud.write_text('import Lean.Util.CollectAxioms\n'+M.read_text()+'\n'+collector)
track=sorted(transitive|{aud,Path(__file__).resolve(),L/'lean-toolchain',L/'lakefile.toml',L/'lake-manifest.json',R/'locks/lean-dependencies.json'}|set((D/'sources').glob('*.pdf')))
def snap():
 files=[dict(path=str(p.relative_to(R)),sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in track]
 return files,hashlib.sha256(json.dumps(files,sort_keys=True,separators=(',',':')).encode()).hexdigest()
initial=snap();commands=[]
def run(argv,label):
 out=subprocess.run(argv,cwd=R,env=os.environ.copy(),text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
 log=V/(label+'.log');log.write_text(out.stdout);commands.append(dict(cwd=str(R),argv=argv,exit_code=out.returncode,log_path=str(log.relative_to(R))));print(pid,label,out.returncode,flush=True);return out
version=run(['lean','--version'],'toolchain');run(['lake','-d',str(L),'build']+['Harsanyi.Extensions.'+p.stem for p in modules],'build');run(['lake','-d',str(L),'env','lean',str(M)],'adapter');audit=run(['lake','-d',str(L),'env','lean',str(aud)],'axioms')
rows=[json.loads(s.removeprefix('FOUNDATIONS_API:')) for s in audit.stdout.splitlines() if s.startswith('FOUNDATIONS_API:')]
white={'propext','Classical.choice','Quot.sound'};stable=initial==snap();clean=all(c['exit_code']==0 for c in commands)
for row in rows:
 row['source_path'],row['line']=locations[row['name']];row['declaration']=row['name'];row['statement']=row['signature'];row['axiom_audit_passed']=set(row['axioms'])<=white;row['source_sha256']=hashlib.sha256((R/row['source_path']).read_bytes()).hexdigest();row['dependencies']=sorted(set(row['dependencies']));row['status']='passed' if clean and stable and row['axiom_audit_passed'] else 'failed';row['evidence_role']='definition' if row['kind']!='theorem' else 'exact_compiled_theorem_type'
passed=clean and stable and len(rows)==len(names) and all(r['axiom_audit_passed'] for r in rows)
report=dict(schema_version=1,build_id=pid+'-formal-20261001',status='passed' if passed else 'failed',generated_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),toolchain=version.stdout.strip(),mathlib_revision='f897ebcf72cd16f89ab4577d0c826cd14afaafc7',source_files=initial[0],source_fingerprint=initial[1],sources_unchanged_during_verification=stable,commands=commands,axiom_whitelist=sorted(white),declarations=rows,checked_declarations=len(rows),expected_declarations=len(names),source_semantics_automatically_verified=False,proof_scope_note='Types and transitive axioms are collected from real Lean constants. The finite statements, paper adapters, counterexamples and source-domain analyses have different evidence roles. No original false statement is claimed proved; declaration count does not equal paper-target count.')
(V/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');(V/'catalog.json').write_text(json.dumps(dict(declarations=rows),ensure_ascii=False,indent=2)+'\n');print(pid,'passed',passed,'declarations',len(rows));raise SystemExit(0 if passed else 1)
