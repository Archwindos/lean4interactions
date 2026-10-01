"""Require an explicit reviewed proof denominator for newly admitted papers."""
import json
import re
from pathlib import Path

WORK=Path(__file__).resolve().parent
CONTRACT_PATH=WORK/'architecture/admission-contract.json'
CONTRACT=json.loads(CONTRACT_PATH.read_text())
NON_PROOF_KINDS=set(CONTRACT['non_proof_kinds'])
MERGE_FIELDS=set(CONTRACT['merge_fields'])

def control_character_errors(value,path='content',field=None):
 """Reject escaped-character corruption without interpreting mathematical text."""
 errors=[]
 if isinstance(value,str):
  tex=str(field).endswith('_tex');allowed={'\n'} if tex else {'\n','\t'}
  bad=sorted({ord(char) for index,char in enumerate(value)
              if ((ord(char)<32 and char not in allowed) or ord(char)==127)
              and not (not tex and char=='\r' and value[index+1:index+2]=='\n')})
  if bad:errors.append(path+':invalid_control_characters='+','.join('U+%04X'%code for code in bad))
 elif isinstance(value,dict):
  for key,child in value.items():errors.extend(control_character_errors(child,path+'.'+str(key),key))
 elif isinstance(value,list):
  for index,child in enumerate(value):errors.extend(control_character_errors(child,path+'.'+str(index),field))
 return errors

def accepted_paper_ids(read=None):
 path=WORK/'evidence/six-paper-preservation-baseline.json'
 read=read or (lambda p:json.loads(p.read_text()))
 return set(read(path)['paper_ids']) if path.is_file() else set()

def merge_target(entry):
 return entry.get('merge_target_id') or entry.get('merge_id') or entry['id']

def inventory_errors(inventory,content=None,legacy=False):
 """Structural failures only; reasonable classifications still need source review."""
 errors=[];ident=inventory.get('paper_id','unknown');entries=inventory.get('entries',[])
 if legacy:return errors
 errors.extend(control_character_errors(inventory,'inventory'))
 def error(entry,reason):errors.append(ident+':'+str(entry.get('id','unknown'))+':'+reason)
 for entry in entries:
  for key in entry:
   if (key.startswith('merge') or key.startswith('merged')) and key not in MERGE_FIELDS:error(entry,'unknown_merge_field='+key)
  for key in ['merge_target_id','merge_id']:
   value=entry.get(key)
   if value is not None and (not isinstance(value,str) or not value.strip()):error(entry,'invalid_merge_target='+key)
  if entry.get('merge_target_id') and entry.get('merge_id') and entry['merge_target_id']!=entry['merge_id']:error(entry,'conflicting_merge_targets')
  if type(entry.get('proof_target')) is not bool:error(entry,'missing_or_nonboolean_proof_target');continue
  if not entry['proof_target']:
   if entry.get('kind') not in NON_PROOF_KINDS:error(entry,'non_target_kind_requires_mathematical_review='+str(entry.get('kind')))
   if not isinstance(entry.get('non_proof_reason'),str) or not entry['non_proof_reason'].strip():error(entry,'missing_non_proof_reason')
 if not legacy and 'proof_targets' in inventory:
  declared=[]
  for row in inventory['proof_targets']:
   target=row.get('id') if isinstance(row,dict) else row
   if not isinstance(target,str) or not target.strip():errors.append(ident+':invalid_root_proof_target');continue
   declared.append(target)
   if isinstance(row,dict):
    for entry_id in row.get('inventory_ids',[]):
     matches=[e for e in entries if e.get('id')==entry_id]
     if len(matches)!=1 or matches[0].get('proof_target') is not True or merge_target(matches[0])!=target:errors.append(ident+':root_proof_target_inventory_mapping_mismatch='+str(entry_id))
  expected={merge_target(e) for e in entries if e.get('proof_target') is True}
  if len(declared)!=len(set(declared)) or set(declared)!=expected:errors.append(ident+':root_proof_targets_disagree_with_entry_booleans')
 if content is not None and not legacy:
  results=content.get('results',[])
  resolved={}
  for entry in entries:
   target=merge_target(entry)
   matches=[r for r in results if r.get('id')==target or entry.get('id') in r.get('inventory_ids',[])]
   if not matches:error(entry,'missing_actual_content_mapping='+str(target))
   elif len(matches)!=1:error(entry,'ambiguous_actual_content_mapping='+','.join(str(r.get('id')) for r in matches))
   else:
    actual=matches[0].get('id')
    if actual!=entry.get('id') and not (entry.get('merge_target_id') or entry.get('merge_id')):error(entry,'implicit_cross_id_mapping_requires_explicit_merge='+str(actual))
    if actual==target:resolved[entry['id']]=actual
   if (entry.get('merge_target_id') or entry.get('merge_id')) and not any(r.get('id')==target for r in results):error(entry,'merge_target_not_an_actual_result='+str(target))
  target_results={resolved[e['id']] for e in entries if e.get('proof_target') is True and e['id'] in resolved}
  for result in results:
   if 'proof_target' in result and (type(result['proof_target']) is not bool or result['proof_target']!=(result['id'] in target_results)):errors.append(ident+':'+result['id']+':content_proof_target_disagrees_with_inventory')
 return errors

def validate_inventory(inventory,content=None,legacy=False):
 errors=inventory_errors(inventory,content,legacy)
 if content is not None and not legacy:errors.extend(content_errors(content))
 if errors:raise ValueError('Inventory admission rejected: '+'; '.join(errors[:20]))

def machine_role_status_reviews(content):
 """Expose mixed status wording for author review without changing a role."""
 return [{'id':row.get('id'),'evidence_role':row['lean']['evidence_role'],
          'status':row['lean']['status'],'scope':row['lean'].get('scope'),
          'required_review':'Mathematics author must reconcile machine scope/status; statement assessment is a separate dimension.'}
         for row in content.get('results',[])+content.get('shared_proofs',[])
         if isinstance(row.get('lean'),dict)
         and row['lean'].get('status')=='partial_scope_verified'
         and row['lean'].get('evidence_role') in {'counterexample','theorem_proof'}]

def content_errors(content):
 errors=control_character_errors(content)
 for kind,rows in [('result',content.get('results',[])),('shared',content.get('shared_proofs',[]))]:
  for row in rows:
   ident=str(row.get('id','unknown'))
   for field in ['original_statement_md','original_proof_md']:
    text=row.get(field,'')
    if isinstance(text,str) and re.search(r'\bProject source (?:note|synopsis)\s*\(\s*(?:not\s+author\s+text|not\s+an\s+author\s+quotation)\s*\)',text,re.I):
     errors.append(ident+':project_comment_in_author_original_field='+field)
   for field in CONTRACT[kind+'_required_fields']:
    if field not in row:errors.append(ident+':missing_'+kind+'_field='+field)
   fields=['rewrite_status']+(['rewrite_role','statement_assessment'] if kind=='result' else [])
   for field in fields:
    if row.get(field) not in CONTRACT[field]:errors.append(ident+':unknown_'+field+'='+str(row.get(field)))
   lean=row.get('lean')
   if not isinstance(lean,dict):errors.append(ident+':lean_must_be_object');continue
   if lean.get('evidence_role') not in CONTRACT['lean_evidence_role']:errors.append(ident+':unknown_lean_evidence_role='+str(lean.get('evidence_role')))
   declarations=lean.get('declarations')
   if not isinstance(declarations,list):errors.append(ident+':lean_declarations_must_be_array')
   elif declarations and not lean.get('report_path'):errors.append(ident+':claimed_declarations_missing_actual_report')
   if not declarations and lean.get('evidence_role') not in {None,'none'}:errors.append(ident+':nonempty_lean_role_without_declarations')
   if kind=='shared':
    for field in ['assumptions','definitions','proof_steps']:
     if not isinstance(row.get(field),list):errors.append(ident+':shared_field_must_be_array='+field)
    if not isinstance(row.get('translations'),dict) or not isinstance(row.get('translations',{}).get('en'),dict):errors.append(ident+':shared_english_overlay_missing')
 return errors

def source_errors(metadata):
 errors=control_character_errors(metadata,'metadata')
 for source in metadata.get('sources',[]):
  for field in CONTRACT['source_required_fields']:
   if field not in source:errors.append(str(metadata.get('id'))+':missing_source_field='+field)
  if not isinstance(source.get('id'),str) or not source.get('id'):errors.append(str(metadata.get('id'))+':source_id_must_be_nonempty_id_field')
 return errors

def issue_errors(issues,metadata=None,content=None):
 """Explicit types and real locations/relations; no automatic mathematical judgment."""
 errors=control_character_errors(issues,'issues');sources={s.get('id'):s for s in (metadata or {}).get('sources',[])}
 results={r.get('id'):r for r in (content or {}).get('results',[])}
 for issue in issues:
  ident=str(issue.get('id','unknown'))
  for field in CONTRACT['issue_required_fields']:
   if field not in issue:errors.append(ident+':missing_issue_field='+field)
  if not isinstance(issue.get('kind'),str) or not issue.get('kind','').strip():errors.append(ident+':issue_kind_must_be_nonempty_metadata')
  typ=issue.get('issue_type')
  if typ not in CONTRACT['issue_type']:errors.append(ident+':unknown_issue_type='+str(typ))
  wanted={'statement_counterexample':'counterexample_verified','statement_partial_counterexample':'compound_clause_counterexample_verified'}.get(typ)
  if wanted and issue.get('original_statement_status')!=wanted:errors.append(ident+':issue_statement_assessment_scope_mismatch')
  refs=issue.get('source_refs')
  if not isinstance(refs,list) or not refs:errors.append(ident+':missing_precise_issue_source_refs')
  else:
   for ref in refs:
    if not isinstance(ref,dict):errors.append(ident+':issue_source_ref_must_be_object');continue
    pages=ref.get('pdf_pages')
    if not isinstance(pages,list) or not pages or any(type(p) is not int or p<=0 for p in pages):errors.append(ident+':invalid_issue_pdf_pages');continue
    if not ref.get('source_id') or not ref.get('version_id'):errors.append(ident+':missing_issue_source_identity');continue
    if metadata is not None:
     source=sources.get(ref['source_id'])
     if not source:errors.append(ident+':unknown_issue_formal_source='+str(ref['source_id']));continue
     if ref['version_id']!=source.get('version_id'):errors.append(ident+':issue_source_version_mismatch')
     if any(p>source['total_pages'] for p in pages):errors.append(ident+':issue_pdf_page_out_of_range')
  linked=[]
  for field in ['affected_result_ids','related_result_ids']:
   value=issue.get(field,[])
   if not isinstance(value,list) or any(not isinstance(v,str) or not v for v in value):errors.append(ident+':invalid_issue_result_links='+field)
   else:linked.extend(value)
  if not linked:errors.append(ident+':missing_actual_issue_result_links')
  if content is not None:
   for target in set(linked):
    if target not in results:errors.append(ident+':unknown_issue_result='+target)
    elif ident not in results[target].get('related_issue_ids',[]):errors.append(ident+':issue_result_missing_reciprocal_link='+target)
 return errors
