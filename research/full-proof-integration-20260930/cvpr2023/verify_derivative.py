#!/usr/bin/env python3
"""Audit the actual mixed-partial/MVT/mask bridge with its necessary imported inputs."""
from pathlib import Path
import datetime, hashlib, json, os, re, subprocess, sys

ROOT=Path(os.environ['ARCHIVE_PROJECT_ROOT']).resolve()
BASE=ROOT/'research/full-proof-integration-20260930/cvpr2023'
LIB=ROOT/'lean/HarsanyiLib'
OUT=BASE/'verification'
MODULE=LIB/'Harsanyi/Extensions/DerivativeCutoff.lean'
SOURCE=BASE/'lean/SparseDerivativeAdapter.lean'
NAMES=[];LINES={}
for p,ns in [(MODULE,'Harsanyi'),(SOURCE,'FullSparseDerivative')]:
    for i,line in enumerate(p.read_text().splitlines(),1):
        m=re.match(r'^(?:@\[[^\]]*\]\s*)?(?:noncomputable )?(?:def|theorem) (\w+)',line)
        if m:
            name=ns+'.'+m.group(1)
            NAMES.append(name);LINES[name]=(str(p.relative_to(ROOT)),i)
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
    liftM <| IO.println ("DERIVATIVE_API:" ++ (Json.mkObj [
      ("name", toJson name.toString), ("signature", toJson signature.pretty),
      ("kind", toJson kind), ("axioms", toJson (axioms.map Name.toString)),
      ("dependencies", toJson (deps.map Name.toString))]).compress)
'''.replace('NAMES',', '.join('`'+n for n in NAMES))
AUDIT=OUT/'AuditDerivative.lean'
body='\n'.join(line for line in SOURCE.read_text().splitlines() if not line.startswith('import '))
AUDIT.write_text('import Lean.Util.CollectAxioms\nimport Harsanyi.Extensions.DerivativeCutoff\n'+body+'\n'+collector)
track=[MODULE,SOURCE,AUDIT,BASE/'lean/DerivativeCutoff.lean',Path(__file__).resolve(),LIB/'lakefile.toml',LIB/'lake-manifest.json',LIB/'lean-toolchain',ROOT/'locks/lean-dependencies.json',ROOT/'research/paper-survey-20260930/recent/pdf/iclr2024-sparse.pdf']
track+=sorted((LIB/'Harsanyi/Core').glob('*.lean'))
track+=[LIB/'Harsanyi/Extensions/Attribution.lean',LIB/'Harsanyi/Extensions/OrInteraction.lean']
def snapshot():
    rows=[{'path':str(p.relative_to(ROOT)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in sorted(set(track))]
    return rows,hashlib.sha256(json.dumps(rows,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
initial=snapshot();commands=[]
def run(argv,label):
    r=subprocess.run(argv,cwd=ROOT,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
    log=OUT/(label+'.log');log.write_text(r.stdout)
    commands.append({'cwd':str(ROOT),'argv':argv,'exit_code':r.returncode,'log_path':str(log.relative_to(ROOT))})
    print(label,'passed' if r.returncode==0 else 'failed',flush=True)
    return r
version=run(['lean','--version'],'derivative-toolchain')
run(['lake','-d',str(LIB),'build','Harsanyi.Extensions.DerivativeCutoff'],'derivative-public-build')
run(['lake','-d',str(LIB),'env','lean','-o',str(OUT/'SparseDerivativeAdapter.olean'),str(SOURCE)],'derivative-adapter-compile')
audit=run(['lake','-d',str(LIB),'env','lean',str(AUDIT)],'derivative-axiom-audit')
rows=[json.loads(line.removeprefix('DERIVATIVE_API:')) for line in audit.stdout.splitlines() if line.startswith('DERIVATIVE_API:')]
whitelist={'propext','Classical.choice','Quot.sound'}
for r in rows:
    r['dependencies']=sorted(set(r['dependencies']))
    r['status']='passed' if set(r['axioms'])<=whitelist else 'failed'
    r['source_path'],r['line']=LINES[r['name']]
final=snapshot();matches=MODULE.read_bytes()==(BASE/'lean/DerivativeCutoff.lean').read_bytes()
good=all(c['exit_code']==0 for c in commands) and len(rows)==len(NAMES) and set(r['name'] for r in rows)==set(NAMES) and all(r['status']=='passed' for r in rows) and initial==final and matches
report={'schema_version':1,'build_id':'derivative-cutoff-mvt-20260930','status':'passed' if good else 'failed','generated_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'toolchain':version.stdout.strip(),'lean_version':'4.24.0','mathlib_revision':'f897ebcf72cd16f89ab4577d0c826cd14afaafc7','source_files':final[0],'source_fingerprint':final[1],'sources_unchanged_during_verification':initial==final,'staging_matches_public':matches,'commands':commands,'declarations':rows,'axiom_whitelist':sorted(whitelist),'scope':'actual ordered coordinate mixed derivatives, derivative existence for prefixes, global zero mixed derivatives imply rectangular finite differences zero via one-variable mean value theorem, actual arbitrary baseline coordinate masks, source centered interaction cutoff','source_semantics_automatically_verified':False,'excluded_scope':['C1 alone without classical higher mixed-partial existence','zero values of total Lean deriv at points where classical derivatives do not exist','general infinite Taylor representation/Lemma1 outside supplied representation assumptions','approximations to ReLU DNNs or numerical smoothing','a human acceptance of the source ordering convention']}
(OUT/'derivative-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
(BASE/'derivative-registry.json').write_text(json.dumps({'schema_version':1,'registry_id':'derivative-cutoff-20260930','status':report['status'],'imports':['Harsanyi.Extensions.DerivativeCutoff'],'report_path':str((OUT/'derivative-report.json').relative_to(ROOT)),'source_fingerprint':final[1],'declarations':rows},ensure_ascii=False,indent=2)+'\n')
print('derivative declarations',len(rows),'/',len(NAMES),'status',report['status'],flush=True)
sys.exit(0 if good else 1)
