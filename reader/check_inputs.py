#!/usr/bin/env python3
"""Early source/inventory validation, independent of content delivery."""
import hashlib,json
from pathlib import Path
from pypdf import PdfReader
from pypdf.errors import PyPdfError
from input_manifest import MANIFEST,ROOT,load_manifest,project_path
from evidence_paths import EVIDENCE,input_hashes
from inventory_contract import accepted_paper_ids,inventory_errors

def checked_pdf_pages(path,expected):
 actual=len(PdfReader(path).pages)
 if actual!=expected:raise ValueError('actual PDF page count '+str(actual)+' differs from metadata '+str(expected))
 return actual

def check_inputs():
 manifest=load_manifest();checks=[];errors=[];inputs={MANIFEST.relative_to(ROOT).as_posix():hashlib.sha256(MANIFEST.read_bytes()).hexdigest()};all_sourceids=set();legacy_ids=accepted_paper_ids()
 for item in manifest['papers']:
  ident=item['paper_id'];meta=json.loads(project_path(item['metadata_path']).read_text());inventory=json.loads(project_path(item['inventory_path']).read_text())
  errors.extend(inventory_errors(inventory,legacy=ident in legacy_ids))
  for key in ['metadata_path','inventory_path']:
   inputs[item[key]]=hashlib.sha256(project_path(item[key]).read_bytes()).hexdigest()
  if meta.get('id')!=ident or inventory.get('paper_id')!=ident:errors.append(ident+': mismatched identity')
  sourceids=set()
  for source in meta.get('sources',[]):
   missing={'id','local_path','sha256','total_pages','publication_status','visibility','url'}-source.keys()
   if missing:errors.append(ident+': missing metadata source fields '+str(sorted(missing)));continue
   sourceids.add(source['id']);path=project_path(source['local_path']);hashok=hashlib.sha256(path.read_bytes()).hexdigest()==source['sha256']
   inputs[source['local_path']]=hashlib.sha256(path.read_bytes()).hexdigest()
   if source['id'] in all_sourceids:errors.append(ident+': duplicate global source ID '+source['id'])
   all_sourceids.add(source['id'])
   if not hashok:errors.append(ident+': source hash changed')
   actual_pages=None
   try:actual_pages=checked_pdf_pages(path,source['total_pages'])
   except (PyPdfError,ValueError,OSError) as exc:errors.append(ident+': PDF page check failed '+source['id']+': '+str(exc))
   inventory_source=[s for s in inventory.get('sources',[]) if s.get('source_id')==source['id']]
   if len(inventory_source)!=1:errors.append(ident+': missing/duplicate inventory source '+source['id'])
   else:
    listed=inventory_source[0]
    if listed.get('path')!=source['local_path'] or listed.get('sha256')!=source['sha256'] or listed.get('page_count',listed.get('pdf_page_count',listed.get('pages')))!=source['total_pages']:errors.append(ident+': metadata/inventory source mismatch '+source['id'])
   pages=[row['pdf_page'] for row in inventory['page_audit'] if row['source_id']==source['id']]
   if len(pages)!=len(set(pages)) or set(pages)!=set(range(1,source['total_pages']+1)):errors.append(ident+': incomplete/duplicated page audit')
   checks.append({'paper_id':ident,'source_id':source['id'],'sha256':source['sha256'],'hash_current':hashok,'page_count':len(pages),'actual_pdf_pages':actual_pages})
  if any(row['source_id'] not in sourceids for row in inventory['page_audit']):errors.append(ident+': unknown audit source ID')
  entry_ids=[e['id'] for e in inventory['entries']]
  if len(set(entry_ids))!=len(entry_ids):errors.append(ident+': duplicate inventory IDs')
  for row in inventory['page_audit']:
   if row.get('review_status')!='agent_reviewed' or not any(row.get(k) for k in ['classification','finding','note','section']):errors.append(ident+': source page lacks reviewed classification '+str(row.get('pdf_page')))
   if any(eid not in entry_ids for eid in row.get('entry_ids',row.get('mathematical_entry_ids',[]))):errors.append(ident+': unknown inventory ID on source page '+str(row.get('pdf_page')))
 inputs.update(input_hashes(Path(__file__).resolve(),ROOT/'reader/input_manifest.py',ROOT/'reader/inventory_contract.py',ROOT/'reader/architecture/admission-contract.json',ROOT/'reader/evidence_paths.py',ROOT/'reader/evidence/six-paper-preservation-baseline.json'))
 return {'status':'passed' if not errors else 'failed','checks':checks,'errors':errors,'inputs':inputs,'scope':'configured_identity_actual_pdf_pages_source_hash_page_coverage_not_mathematical_review'}
if __name__=='__main__':
 report=check_inputs();(EVIDENCE/'input-preflight.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps(report,ensure_ascii=False));raise SystemExit(bool(report['errors']))
