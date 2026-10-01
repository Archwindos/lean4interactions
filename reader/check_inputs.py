#!/usr/bin/env python3
"""Early source/inventory validation, independent of content delivery."""
import hashlib,json
from pathlib import Path
from input_manifest import MANIFEST,ROOT,project_path

def check_inputs():
 manifest=json.loads(MANIFEST.read_text());checks=[];errors=[]
 for item in manifest['papers']:
  ident=item['paper_id'];meta=json.loads(project_path(item['metadata_path']).read_text());inventory=json.loads(project_path(item['inventory_path']).read_text())
  if meta.get('id')!=ident or inventory.get('paper_id')!=ident:errors.append(ident+': mismatched identity')
  sourceids=set()
  for source in meta.get('sources',[]):
   missing={'id','local_path','sha256','total_pages','publication_status','visibility','url'}-source.keys()
   if missing:errors.append(ident+': missing metadata source fields '+str(sorted(missing)));continue
   sourceids.add(source['id']);path=project_path(source['local_path']);hashok=hashlib.sha256(path.read_bytes()).hexdigest()==source['sha256']
   if not hashok:errors.append(ident+': source hash changed')
   pages=[row['pdf_page'] for row in inventory['page_audit'] if row['source_id']==source['id']]
   if len(pages)!=len(set(pages)) or set(pages)!=set(range(1,source['total_pages']+1)):errors.append(ident+': incomplete/duplicated page audit')
   checks.append({'paper_id':ident,'source_id':source['id'],'sha256':source['sha256'],'hash_current':hashok,'page_count':len(pages)})
  if any(row['source_id'] not in sourceids for row in inventory['page_audit']):errors.append(ident+': unknown audit source ID')
 return {'status':'passed' if not errors else 'failed','checks':checks,'errors':errors,'scope':'configured_identity_source_hash_page_coverage_not_mathematical_review'}
if __name__=='__main__':
 report=check_inputs();(ROOT/'reader/evidence/input-preflight.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps(report,ensure_ascii=False));raise SystemExit(bool(report['errors']))
