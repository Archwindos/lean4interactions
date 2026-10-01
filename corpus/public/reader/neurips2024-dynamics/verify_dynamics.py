#!/usr/bin/env python3
"""Compile one public module and its exact paper adapter; collect real Lean types/axioms."""
from pathlib import Path
import os,json,re,hashlib,subprocess,datetime,sys
R=Path.cwd();pid=sys.argv[1] if len(sys.argv)>1 else 'neurips2024-dynamics';D=R/'corpus/public/reader'/pid;V=D/'verification';L=R/'lean/HarsanyiLib'
adapter={'neurips2024-dynamics':'PaperDynamics','icml2023-bayesian':'PaperBayesian','neurips2023-difficulty':'PaperDifficulty'}[pid]
mods=[('TaylorMoments','Harsanyi.TaylorMoments'),('NoisyRegression','Harsanyi.NoisyRegression'),('GaussianRegression','Harsanyi.GaussianRegression'),('PolynomialSupport','Harsanyi.PolynomialSupport')]
A=D/'lean'/f'{adapter}.lean';V.mkdir(exist_ok=True)
module='GaussianRegression';M=L/'Harsanyi/Extensions/GaussianRegression.lean'
names=[];loc={}
for p,namespace in [(L/'Harsanyi/Extensions'/f'{m}.lean',ns) for m,ns in mods]+[(A,adapter)]:
 for ln,line in enumerate(p.read_text().splitlines(),1):
  m=re.match(r'^(?:noncomputable )?(?:def|theorem|inductive) (\w+)',line)
  if m:n=namespace+'.'+m[1];names.append(n);loc[n]=(str(p.relative_to(R)),ln)
extras={'Harsanyi.reconstruction':'Core/Mobius.lean','Harsanyi.reconstruction_unique':'Core/Mobius.lean','Harsanyi.interaction_insert':'Core/Mobius.lean','Harsanyi.interaction_add':'Core/Properties.lean','Harsanyi.interaction_recursive':'Core/Properties.lean','Harsanyi.interaction_relabel':'Core/Properties.lean','Harsanyi.interaction_unanimity':'Core/Properties.lean','Harsanyi.or_dual':'Extensions/OrInteraction.lean','Harsanyi.maskCoordinates_complement':'Extensions/OrInteraction.lean','Harsanyi.or_reconstruction':'Extensions/OrInteraction.lean','Harsanyi.Layerwise.and_or_matching':'Extensions/LayerwiseKnowledge.lean','Harsanyi.and_gaussian_variance':'Extensions/Noise.lean','Harsanyi.signed_gaussian_variance':'Extensions/Noise.lean'}
for n,file in extras.items():
 p=L/'Harsanyi'/file
 for ln,line in enumerate(p.read_text().splitlines(),1):
  if re.match(r'^(?:noncomputable )?(?:def|theorem) '+re.escape(n.split('.')[-1])+r'\b',line):
   names.append(n);loc[n]=(str(p.relative_to(R)),ln);break
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
    let kind := match info with | .thmInfo _ => "theorem" | .inductInfo _ => "inductive" | _ => "definition"
    liftM <| IO.println ("DYNAMICS_API:" ++ (Json.mkObj [
      ("name", toJson name.toString), ("signature", toJson signature.pretty),
      ("kind", toJson kind), ("axioms", toJson (axioms.map Name.toString)),
      ("dependencies", toJson (deps.map Name.toString))]).compress)
'''.replace('NAMES',', '.join('`'+n for n in names))
aud=V/f'Audit{module}.lean';aud.write_text('import Lean.Util.CollectAxioms\n'+'\n'.join(s for s in A.read_text().splitlines() if s.startswith('import '))+'\n'+'\n'.join(s for s in A.read_text().splitlines() if not s.startswith('import '))+'\n'+collector)
# All local transitive imports are hashed, not only the top-level module.
transitive=set()
def walk(p):
 if p in transitive:return
 transitive.add(p)
 for line in p.read_text().splitlines():
  if line.startswith('import Harsanyi.'):
   q=L/(line.removeprefix('import ').strip().replace('.','/')+'.lean');walk(q)
walk(M)
walk(A)
track=sorted(transitive|{M,A,aud,Path(__file__).resolve(),D/'sources/formal.pdf',L/'lean-toolchain',L/'lakefile.toml',L/'lake-manifest.json',R/'locks/lean-dependencies.json'})
def snap():
 fs=[dict(path=str(p.relative_to(R)),sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in track]
 return fs,hashlib.sha256(json.dumps(fs,sort_keys=True,separators=(',',':')).encode()).hexdigest()
initial=snap();commands=[];env=os.environ.copy();env['PATH']=str(R/'.tools/lean/bin')+os.pathsep+env['PATH']
def run(argv,label):
 p=subprocess.run(argv,cwd=R,env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT);log=V/(label+'.log');log.write_text(p.stdout);commands.append(dict(cwd=str(R),argv=argv,exit_code=p.returncode,log_path=str(log.relative_to(R))));print(pid,label,p.returncode,flush=True);return p
version=run(['lean','--version'],'toolchain');build=run(['lake','-d',str(L),'build','Harsanyi.Extensions.'+module,'Harsanyi.Extensions.LayerwiseKnowledge','Harsanyi.Extensions.Noise','Harsanyi.Extensions.PolynomialSupport'],'build');ad=run(['lake','-d',str(L),'env','lean',str(A)],'adapter');audit=run(['lake','-d',str(L),'env','lean',str(aud)],'axioms')
rows=[json.loads(s.removeprefix('DYNAMICS_API:')) for s in audit.stdout.splitlines() if s.startswith('DYNAMICS_API:')];white={'propext','Classical.choice','Quot.sound'};stable=initial==snap();clean=all(c['exit_code']==0 for c in commands)
for row in rows:
 row['source_path'],row['line']=loc[row['name']];row['declaration']=row['name'];row['statement']=row['signature'];row['axiom_audit_passed']=set(row['axioms'])<=white;row['source_sha256']=hashlib.sha256((R/row['source_path']).read_bytes()).hexdigest();row['dependencies']=sorted(set(row['dependencies']));row['status']='passed' if clean and stable and row['axiom_audit_passed'] else 'failed'
 row['evidence_role']='definition' if row['kind']!='theorem' else 'counterexample' if 'counterexample' in row['name'] else 'proved_finite_statement'
passed=clean and stable and len(rows)==len(names) and all(r['axiom_audit_passed'] for r in rows)
report=dict(schema_version=1,build_id=pid+'-formal-20261001',status='passed' if passed else 'failed',generated_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),toolchain=version.stdout.strip(),mathlib_revision='f897ebcf72cd16f89ab4577d0c826cd14afaafc7',source_files=initial[0],source_fingerprint=initial[1],sources_unchanged_during_verification=stable,commands=commands,axiom_whitelist=sorted(white),declarations=rows,checked_declarations=len(rows),expected_declarations=len(names),source_semantics_automatically_verified=False,proof_scope_note='Each row records a real Lean type and transitive axiom audit. Definitions, adapters, proofs, and counterexamples are distinguished; the declaration count is not the paper-proof count. Original false statements and unquantified external sparsity are not claimed proved. Human source alignment is separately reviewed.')
(V/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');(V/'catalog.json').write_text(json.dumps(dict(declarations=rows),ensure_ascii=False,indent=2)+'\n')
print(pid,'passed',passed,'declarations',len(rows));raise SystemExit(0 if passed else 1)
