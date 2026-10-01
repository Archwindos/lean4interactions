from pathlib import Path
import json,sys,hashlib,subprocess,re
R=Path.cwd();sys.path.insert(0,str(R/'reader'))
from inventory_contract import inventory_errors,content_errors,source_errors
from bilingual import validate_translations
from check_completion import completion_report
D=R/'corpus/public/reader/icml2023-decoder';c=json.load(open(D/'content.json'));i=json.load(open(D/'inventory.json'));m=json.load(open(D/'paper-metadata.json'));v=json.load(open(D/'verification/report.json'))
errors=inventory_errors(i,c)+content_errors(c)+source_errors(m);assert not errors,errors
assert v['status']=='passed'
for f in v['source_files']:assert hashlib.sha256((R/f['path']).read_bytes()).hexdigest()==f['sha256'],f['path']
source_checks=[]
for s in m['sources']:
 path=R/s['local_path'];p=subprocess.run(['pdfinfo',str(path)],text=True,stdout=subprocess.PIPE,check=True)
 pages=int(re.search(r'^Pages:\s+(\d+)',p.stdout,re.M)[1]);h=hashlib.sha256(path.read_bytes()).hexdigest();assert pages==s['total_pages'] and h==s['sha256']
 inv=next(t for t in i['sources'] if t['source_id']==s['id']);assert inv['page_count']==pages and inv['sha256']==h
 audited={a['pdf_page'] for a in i['page_audit'] if a['source_id']==s['id']};assert audited==set(range(1,pages+1))
 source_checks.append(dict(source_id=s['id'],physical_pages=pages,sha256=h,page_audit_complete=True))
api={r['name']:r for r in v['declarations']}
for r in c['results']:
 assert all(n in api for n in r['lean']['declarations']),r['id']
 for st in r['proof_steps']:assert '$' not in st['title'] and '\\' not in st['title'],st['id']
c['papers']=[m];c['inventories']=[i];b=validate_translations(c,strict=True);assert not b['inline_math_differences'],b['inline_math_differences'];q=completion_report(c);assert q['status']=='passed',q
report=dict(status='passed',scope='Source files/pages, explicit target denominator, actual Lean source freshness, bilingual coverage and content delivery. This does not replace independent mathematical/source review.',sources=source_checks,reading_entries=len(c['results']),proof_targets=len(i['proof_targets']),complete_author_proof_transcriptions=sum(r['original_proof_source_type']=='complete_manual_formal_proof_transcription' for r in c['results']),audited_declarations=len(api),allowed_axioms=v['axiom_whitelist'],bilingual=b,completion=q)
(D/'verification/content-preflight.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');(D/'verification/bilingual-checks.json').write_text(json.dumps(b,ensure_ascii=False,indent=2)+'\n');print({k:v for k,v in report.items() if k not in ['bilingual','completion','sources']})
