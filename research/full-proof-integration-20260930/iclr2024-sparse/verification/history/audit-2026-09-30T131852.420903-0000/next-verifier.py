#!/usr/bin/env python3
"""Compile source-matched paper adapters and collect genuine Lean signatures and axioms."""
from pathlib import Path
import datetime, hashlib, json, os, re, shutil, subprocess, sys
ROOT=Path(os.environ['ARCHIVE_PROJECT_ROOT']).resolve()
BASE=ROOT/'research/full-proof-integration-20260930/iclr2024-sparse'
LIB=ROOT/'lean/HarsanyiLib';OUT=BASE/'verification';OUT.mkdir(exist_ok=True)
if (OUT/'report.json').exists():
    previous=json.loads((OUT/'report.json').read_text())
    stamp=previous['generated_at'].replace(':','').replace('+','-')
    archive=OUT/'history'/('audit-'+stamp)
    archive.mkdir(parents=True,exist_ok=True)
    for old in OUT.iterdir():
        if old.is_file() and old.suffix in {'.json','.lean','.log'}:
            shutil.copy2(old,archive/old.name)
    if (BASE/'registry.json').exists():shutil.copy2(BASE/'registry.json',archive/'registry.json')
    # Save available exact old sources as well. Changed adapters remain recoverable in
    # the old AuditMath source; never relabel current source bytes as the old version.
    for row in previous.get('source_files',[]):
        path=ROOT/row['path']
        if path.exists() and hashlib.sha256(path.read_bytes()).hexdigest()==row['sha256']:
            dest=archive/'sources'/row['path'];dest.parent.mkdir(parents=True,exist_ok=True)
            shutil.copy2(path,dest)
    shutil.copy2(Path(__file__).resolve(),archive/'next-verifier.py')
MODULES=[LIB/'Harsanyi/Extensions/Sparsity.lean',LIB/'Harsanyi/Extensions/Noise.lean']
ADAPTERS=[BASE/'lean/FullSparse.lean',BASE/'lean/FullGeneralizableAnalysis.lean']
DEPENDENCIES=sorted((LIB/'Harsanyi/Core').glob('*.lean'))+[LIB/'Harsanyi/Extensions/Attribution.lean',LIB/'Harsanyi/Extensions/OrInteraction.lean']
NAMES=[];SOURCE_LINES={}
for path in MODULES+ADAPTERS:
    namespace={'Sparsity.lean':'Harsanyi.Sparsity','Noise.lean':'Harsanyi','FullSparse.lean':'FullSparse','FullGeneralizableAnalysis.lean':'FullGeneralizableAnalysis'}[path.name]
    for lineno,line in enumerate(path.read_text().splitlines(),1):
        m=re.match(r'^(?:@\[[^\]]*\]\s*)?(?:noncomputable )?(?:def|theorem|structure) (\w+)',line)
        if m:
            name=namespace+'.'+m.group(1)
            if name in NAMES:raise RuntimeError('duplicate '+name)
            NAMES.append(name);SOURCE_LINES[name]=(str(path.relative_to(ROOT)),lineno)
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
    let kind := match info with | .thmInfo _ => "theorem" | .inductInfo _ => "structure" | _ => "definition"
    liftM <| IO.println ("SPARSE_API:" ++ (Json.mkObj [
      ("name", toJson name.toString), ("signature", toJson signature.pretty),
      ("kind", toJson kind), ("axioms", toJson (axioms.map Name.toString)),
      ("dependencies", toJson (deps.map Name.toString))]).compress)
'''.replace('NAMES',', '.join('`'+n for n in NAMES))
AUDIT=OUT/'AuditMath.lean'
body='\n\n'.join('\n'.join(l for l in p.read_text().splitlines() if not l.startswith('import ')) for p in ADAPTERS)
AUDIT.write_text('import Lean.Util.CollectAxioms\nimport Harsanyi.Extensions.Sparsity\nimport Harsanyi.Extensions.Noise\nimport Harsanyi.Extensions.Attribution\nimport Harsanyi.Extensions.OrInteraction\n\n'+body+'\n'+collector+'\n')
track=MODULES+ADAPTERS+DEPENDENCIES+[AUDIT,Path(__file__).resolve(),LIB/'lakefile.toml',LIB/'lake-manifest.json',LIB/'lean-toolchain',ROOT/'locks/lean-dependencies.json',BASE/'lean/Sparsity.lean',BASE/'lean/Noise.lean',ROOT/'research/paper-survey-20260930/recent/pdf/iclr2024-sparse.pdf',ROOT/'research/paper-survey-20260930/recent/pdf/iclr2024-generalizable.pdf']
def snapshot():
    rows=[{'path':str(p.relative_to(ROOT)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in sorted(set(track))]
    return rows,hashlib.sha256(json.dumps(rows,sort_keys=True,separators=(',',':')).encode()).hexdigest()
initial=snapshot();commands=[]
def run(argv,label):
    r=subprocess.run(argv,cwd=ROOT,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
    log=OUT/(label+'.log');log.write_text(r.stdout)
    commands.append({'cwd':str(ROOT),'argv':argv,'exit_code':r.returncode,'log_path':str(log.relative_to(ROOT))})
    print(label,'passed' if r.returncode==0 else 'failed',flush=True)
    return r
version=run(['lean','--version'],'toolchain')
run(['lake','-d',str(LIB),'build','Harsanyi.Extensions.Sparsity','Harsanyi.Extensions.Noise'],'public-build')
for p in ADAPTERS:run(['lake','-d',str(LIB),'env','lean','-o',str(OUT/(p.stem+'.olean')),str(p)],p.stem+'-compile')
r=run(['lake','-d',str(LIB),'env','lean',str(AUDIT)],'axiom-audit')
rows=[json.loads(l.removeprefix('SPARSE_API:')) for l in r.stdout.splitlines() if l.startswith('SPARSE_API:')]
white={'propext','Classical.choice','Quot.sound'}
for d in rows:
    d['dependencies']=sorted(set(d['dependencies']));d['axioms']=sorted(d['axioms'])
    d['status']='passed' if set(d['axioms'])<=white else 'failed'
    d['source_path'],d['line']=SOURCE_LINES[d['name']]
    d['verification_role']='counterexample' if d['name'].endswith('signed_max_counterexample') else ('definition' if d['kind']!='theorem' else 'theorem_proof')
    d['verification_scope']='actual_model_mask_paper_adapter' if d['name'].startswith('FullSparse.') or d['name'].startswith('FullGeneralizableAnalysis.masked_model_') else 'finite_general_library_or_original_matrix_definition'
final=snapshot();staging=all(p.read_bytes()==(BASE/'lean'/p.name).read_bytes() for p in MODULES)
good=all(c['exit_code']==0 for c in commands) and len(rows)==len(NAMES) and set(d['name'] for d in rows)==set(NAMES) and all(d['status']=='passed' for d in rows) and initial==final and staging
report={'schema_version':1,'build_id':'sparse-analysis-full-20260930','status':'passed' if good else 'failed','generated_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'toolchain':version.stdout.strip(),'lean_version':'4.24.0','mathlib_revision':'f897ebcf72cd16f89ab4577d0c826cd14afaafc7','source_files':final[0],'source_fingerprint':final[1],'sources_unchanged_during_verification':initial==final,'staging_matches_public':staging,'commands':commands,'declarations':rows,'axiom_whitelist':sorted(white),'source_semantics_automatically_verified':False,
 'scope':'Full Sparse model/mask reconstruction, seven properties (efficiency merged into reconstruction), means, binomial kernel, full coefficient witness and T3 coefficient substitution in positive-order expression domain, actual centered OR reverse, general baseline-preserving matching plus literal Eq62 component/matching wrappers with both original zero-empty conditions, noise algebra, source worked example and query count. Generalizable decomposition bijection, finite row max plateau, actual matrix alpha0 and AND/OR true IID Gaussian variance including the raw OR empty branch.',
 'excluded_scope':['General smooth infinite Taylor statement without equality/convergence premise; conditional given-Taylor interpretation separately retained','Sparse T2 M=0 reading and undefined log/binomial parameter domains; positive-order 1≤M≤n,n>1 proof does not close that source scope issue','Unquantified approximation, Big-O and training/generalization explanations','Sparse variance without explicit IID and centered empty interaction convention','Eq10 optimization-minimum equation and free indices (only row expansion is refuted)','Derivative-cutoff analytic bridge delegated separately; original general Lemma1 is not thereby proved','Sampling runtime or confidence guarantees; only requested evaluation count n*t is proved','Whole-network mean monotonicity: Appendix H only the original two-versus-three mask example comparison']}
(OUT/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
registry={'schema_version':1,'registry_id':'sparsity-noise-20260930','build_id':report['build_id'],'status':report['status'],'report_path':str((OUT/'report.json').relative_to(ROOT)),'source_fingerprint':final[1],'imports':['Harsanyi.Extensions.Sparsity','Harsanyi.Extensions.Noise'],'declarations':[d for d in rows if d['name'].startswith('Harsanyi.')]}
(BASE/'registry.json').write_text(json.dumps(registry,ensure_ascii=False,indent=2)+'\n')
print('declarations',len(rows),'/',len(NAMES),'status',report['status'],flush=True)
sys.exit(0 if good else 1)
