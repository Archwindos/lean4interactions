#!/usr/bin/env python3
from pathlib import Path
import os,json,re,hashlib,subprocess,datetime
R=Path.cwd();D=R/'corpus/public/reader/icml2025-coalition';V=D/'verification';L=R/'lean/HarsanyiLib';M=L/'Harsanyi/Extensions/CoalitionAttribution.lean';A=D/'lean/PaperCoalition.lean'
(D/'lean/CoalitionAttribution.lean').write_bytes(M.read_bytes())
names=[];loc={}
for p,ns in [(M,'Harsanyi.Coalition'),(A,'PaperCoalition')]:
 for line,text in enumerate(p.read_text().splitlines(),1):
  match=re.match(r'^\s*(?:noncomputable )?(?:def|theorem) (\w+)',text)
  if match:
   n=ns+'.'+match[1];names.append(n);loc[n]=(str(p.relative_to(R)),line)
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
    liftM <| IO.println ("COALITION_API:" ++ (Json.mkObj [
      ("name", toJson name.toString), ("signature", toJson signature.pretty),
      ("kind", toJson kind), ("axioms", toJson (axioms.map Name.toString)),
      ("dependencies", toJson (deps.map Name.toString))]).compress)
'''.replace('NAMES',', '.join('`'+n for n in names))
aud=V/'AuditCoalition.lean';aud.write_text('import Lean.Util.CollectAxioms\nimport Harsanyi.Extensions.CoalitionAttribution\n'+ '\n'.join(s for s in A.read_text().splitlines() if not s.startswith('import '))+'\n'+collector)
track=sorted(set([M,A,D/'lean/CoalitionAttribution.lean',aud,Path(__file__).resolve(),D/'source.pdf',L/'lean-toolchain',L/'lakefile.toml',L/'lake-manifest.json',R/'locks/lean-dependencies.json']+list((L/'Harsanyi/Core').glob('*.lean'))+[L/'Harsanyi/Extensions/Attribution.lean',L/'Harsanyi/Extensions/OrInteraction.lean']))
def snap():
 files=[dict(path=str(p.relative_to(R)),sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in track];return files,hashlib.sha256(json.dumps(files,sort_keys=True,separators=(',',':')).encode()).hexdigest()
initial=snap();commands=[];env=os.environ.copy();env['PATH']=str(R/'.tools/lean-4.24.0-linux/bin')+os.pathsep+env['PATH']
def run(argv,label):
 p=subprocess.run(argv,cwd=R,env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT);log=V/(label+'.log');log.write_text(p.stdout);commands.append(dict(cwd=str(R),argv=argv,exit_code=p.returncode,log_path=str(log.relative_to(R))));print(label,p.returncode,flush=True);return p
version=run(['lean','--version'],'toolchain');build=run(['lake','-d',str(L),'build','Harsanyi.Extensions.CoalitionAttribution'],'build');adapter=run(['lake','-d',str(L),'env','lean',str(A)],'adapter');audit=run(['lake','-d',str(L),'env','lean',str(aud)],'axioms')
rows=[json.loads(s.removeprefix('COALITION_API:')) for s in audit.stdout.splitlines() if s.startswith('COALITION_API:')];white={'propext','Classical.choice','Quot.sound'}
for row in rows:
 row['source_path'],row['line']=loc[row['name']];row['declaration']=row['name'];row['statement']=row['signature'];row['axiom_audit_passed']=set(row['axioms'])<=white;row['source_sha256']=hashlib.sha256((R/row['source_path']).read_bytes()).hexdigest();row['dependencies']=sorted(set(row['dependencies']))
for row in rows:
 row['status']='passed' if all(c['exit_code']==0 for c in commands) and row['axiom_audit_passed'] and initial==snap() else 'failed'
passed=all(c['exit_code']==0 for c in commands) and len(rows)==len(names) and all(r['axiom_audit_passed'] for r in rows) and initial==snap()
report=dict(schema_version=1,build_id='coalition-formal-20261001',status='passed' if passed else 'failed',generated_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),toolchain=version.stdout.strip(),mathlib_revision='f897ebcf72cd16f89ab4577d0c826cd14afaafc7',source_files=initial[0],source_fingerprint=initial[1],sources_unchanged_during_verification=initial==snap(),commands=commands,axiom_whitelist=sorted(white),declarations=rows,checked_declarations=len(rows),expected_declarations=len(names),proof_scope_note='Compiled exact finite algebra, actual coordinate-mask paper adapters, and quotient-domain inequalities. This is not an automated proof of source semantics or completeness. False axioms and source undefined cases are not marked verified.',source_semantics_automatically_verified=False)
(V/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');(V/'catalog.json').write_text(json.dumps(dict(declarations=rows),ensure_ascii=False,indent=2)+'\n')
print('passed',passed,'declarations',len(rows))
raise SystemExit(0 if passed else 1)
