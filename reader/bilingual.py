"""Language overlays preserve proof identities and formal evidence verbatim."""
from __future__ import annotations
import copy,json,re
from pathlib import Path
PROTECTED={'id','paper_id','statement_tex','formula_tex','lean_refs','shared_step_ref','result_step_ref','lean','source_refs','shared_proof_ids','symbol_ids','original_tex','canonical_tex','relationship','source','canonical','original','rewrite_status','alignment_status','user_review_status','proof_target','statement_assessment','verification_role','rewrite_role','reading_status','compiled','status','evidence_role','fix_authorization','requested_compilation_status'}
TEXT_KEYS={'title','overview','assumptions','definitions','proof_scope','completion_scope','scope_label','proof_steps','notation_map','paper_adaptation_md','adaptation_md','statement_md','original_statement_md','original_proof_md','original_statement_coverage_md','original_proof_coverage_md','original_proof_notes_md','scope','label','name_zh','name_en','description_md','type_or_domain','empty_set_convention','baseline_convention','body_md','text_md','justification','note','meaning','explanation_md','original_statement_note','original_proof_note','example_md','caveats','statement_zh_md','original_statement_heading','original_proof_heading','source_material_summary_md','evidence_md','counterexample_md','impact_md','summary_md','problem_md','analysis_md','explanation'}
TEXT_KEYS.update({'encoding_note','description'})

def machine_refs(refs):
 return [{k:v for k,v in r.items() if k not in {'explanation_md'}} if isinstance(r,dict) else r for r in refs]

def merge_overlay(base,overlay,path=''):
 """ID keyed sequences; omitted formulas/Lean references are inherited."""
 if isinstance(base,dict) and isinstance(overlay,dict):
  result=copy.deepcopy(base)
  for key,value in overlay.items():
   if key=='lean' and value=={}:continue  # An empty overlay inherits the entire formal object.
   if key=='lean_refs':
    if machine_refs(base.get(key,[]))!=machine_refs(value):raise ValueError('Translation changed Lean mapping: '+path)
    result[key]=copy.deepcopy(value);continue
   if key not in PROTECTED and key not in TEXT_KEYS:raise ValueError('Translation contains non-text field: '+path+'/'+key)
   if key in PROTECTED:
    if key in base and value!=base[key]:raise ValueError('Translation changed protected value: '+path+'/'+key)
    continue
   if key=='translations':continue
   result[key]=merge_overlay(base.get(key),value,path+'/'+key)
  return result
 if isinstance(base,list) and isinstance(overlay,list):
  if all(isinstance(x,dict) and x.get('id') for x in base) and base:
   rows={x['id']:x for x in overlay if isinstance(x,dict) and x.get('id')}
   if set(rows)-{x['id'] for x in base}:raise ValueError('Translation introduced step or definition ID: '+path)
   return [merge_overlay(x,rows.get(x['id'],{}),path+'/'+str(x['id'])) for x in base]
  # Lists such as assumptions retain their count and any formula-bearing records.
  if len(base)!=len(overlay):raise ValueError('Translation changed list length: '+path)
  return [merge_overlay(x,y,path+'/'+str(i)) for i,(x,y) in enumerate(zip(base,overlay))]
 return copy.deepcopy(overlay)

def attach_translations(output,manifest,read,project_path,strict=False):
 results={r['id']:r for r in output['results']};shared={r['id']:r for r in output['shared_proofs']};issues={r['id']:r for r in output.get('issues',[])}
 for rel in manifest.get('translation_paths',[]):
  path=project_path(rel,False)
  if not path.exists():
   if strict:raise ValueError('Missing translation sidecar: '+rel)
   continue
  data=read(path)
  for section,nodes in [('results',results),('shared_proofs',shared),('issues',issues)]:
   for ident,overlay in data.get(section,{}).items():
    if ident not in nodes:raise ValueError('Translation references missing active ID: '+ident)
    node=nodes[ident]
    if section=='results' and data.get('paper_id')!=node.get('paper_id'):raise ValueError('Translation paper differs')
    node.setdefault('translations',{})['en']=overlay
 from symbols_english import translate_symbol
 for sym in output['symbols']:
  sym.setdefault('translations',{})['en']=translate_symbol(sym)
 symbolmap={s['id']:s for s in output['symbols']}
 for node in list(results.values())+list(shared.values()):
  en=node.get('translations',{}).get('en')
  if not en:continue
  scope_labels={'Taylor展开的不同读法与反例':'Taylor interpretations and a counterexample','Case2逐阶稀疏推断的反例':'Counterexample to the Case 2 per-order sparsity inference','方差主张与独立性前提':'Variance claims and independence premises','奇偶交互的空集约定':'Empty-coalition convention for parity interactions','原推论的反例论证':'Counterexample argument for the original inference'}
  if node.get('scope_label') in scope_labels and not en.get('scope_label'):en['scope_label']=scope_labels[node['scope_label']]
  if node.get('proof_scope') and not en.get('proof_scope') and en.get('completion_scope'):en['proof_scope']=en['completion_scope']
  if en.get('definitions') and all(isinstance(x,str) for x in en['definitions']) and any(isinstance(x,dict) for x in node.get('definitions',[])):
   en.pop('definitions')
  generated=[]
  for definition in node.get('definitions',[]):
   if isinstance(definition,dict) and definition.get('definition_origin')=='symbol_registry':
    sym=symbolmap.get(definition.get('symbol_id'),{});eng=sym.get('translations',{}).get('en',{})
    generated.append({'id':definition['id'],'text_md':eng.get('name_en',definition['id'])+': '+eng.get('description_md','')})
  if generated:
   existing=en.get('definitions',[]);byid={x['id']:x for x in existing if isinstance(x,dict) and x.get('id')}
   byid.update({x['id']:x for x in generated});en['definitions']=[byid.get(x.get('id'),{}) if isinstance(x,dict) else x for x in node['definitions']]
  # T2 replaces the author's short reference with the three actual assumptions.
  if len(en.get('assumptions',[]))!=len(node.get('assumptions',[])) and any(isinstance(x,dict) and x.get('source_result_id') for x in node.get('assumptions',[])):
   old=en.get('assumptions',[]);translated=[];tail=iter(old[1:])
   for assumption in node['assumptions']:
    if isinstance(assumption,dict) and assumption.get('source_result_id'):
     src=results[assumption['source_result_id']];title=src.get('translations',{}).get('en',{}).get('title',src['id']);translated.append({'text_md':src.get('original_label','')+': '+title})
    else:translated.append(next(tail,''))
   en['assumptions']=translated
 # Aggregation can replace exact duplicated paper proofs with an adaptation.
 # Translate that generated sentence and resolve shared steps through the same ID.
 for node in list(results.values())+list(shared.values()):
  en=node.get('translations',{}).get('en')
  if not en:continue
  raw=en.get('proof_steps',[]);rawmap={x['id']:x for x in raw}
  current=[]
  for step in node.get('proof_steps',[]):
   if step['id']=='paper-notation-adaptation':
    current.append({'id':step['id'],'title':'Check the paper definitions and apply the shared proof','body_md':'The paper objects, quantifiers and baseline match the shared proposition. The conditions above preserve its application scope. The complete shared proof follows below.','justification':'The checked notation correspondence is recorded in this result.'})
   elif step['id'] in rawmap:
    # Exact duplicate aggregation replaces the original body by an ID reference.
    # Its authoritative owner supplies body, formulas and Lean mappings in both
    # languages; the local translation must not restore a second copy.
    current.append({k:v for k,v in rawmap[step['id']].items() if k in {'id','title'}} if step.get('shared_step_ref') or step.get('result_step_ref') else rawmap[step['id']])
   elif step.get('shared_step_ref') or step.get('result_step_ref'):
    ref=step.get('shared_step_ref') or step.get('result_step_ref');owner=shared.get(ref.get('proof_id')) or results.get(ref.get('result_id'))
    owner_steps={x['id']:x for x in (owner or {}).get('translations',{}).get('en',{}).get('proof_steps',[])}
    source=owner_steps.get(ref['step_id'])
    if source:current.append({**source,'id':step['id']})
  if current:en['proof_steps']=current
 return validate_translations(output,strict=strict)

def prose_strings(value):
 if isinstance(value,str):yield value
 elif isinstance(value,list):
  for row in value:yield from prose_strings(row)
 elif isinstance(value,dict):
  for key,row in value.items():
   if key in {'text_md','body_md','title','justification','meaning','note','explanation_md'}:yield from prose_strings(row)

def inline_math(text):
 return re.findall(r"(?<!\\)\$([^$]+)\$|\\\((.*?)\\\)|\\\[(.*?)\\\]",str(text),re.S)

def validate_translations(output,strict=True):
 checks=[];missing=[];math_differences=[]
 for kind,nodes in [('result',output['results']),('shared_proof',output['shared_proofs'])]:
  for node in nodes:
   en=node.get('translations',{}).get('en')
   if not en:missing.append(node['id']);continue
   translated=merge_overlay(node,en,node['id'])
   for key in ['title','overview','assumptions','definitions','proof_scope','completion_scope','scope_label','paper_adaptation_md','adaptation_md','notation_map','caveats','example_md','statement_md','statement_zh_md']:
    raw=node.get(key)
    if not raw:continue
    for text in prose_strings(translated.get(key,raw)):
     # IDs and formulas are inherited. Chinese source notation is excluded by
     # prose_strings, while explanatory paragraphs must actually be English.
     if re.search(r'[\u3400-\u9fff]',text):missing.append(node['id']+':'+key)
    if key in ['title','overview'] and key not in en:missing.append(node['id']+':'+key)
   es={x['id']:x for x in en.get('proof_steps',[])}
   for step in node.get('proof_steps',[]):
    translated_step=next(x for x in translated.get('proof_steps',[]) if x['id']==step['id'])
    ref=step.get('shared_step_ref') or step.get('result_step_ref')
    for field in ['title','body_md','justification']:
     if not step.get(field):continue
     english=translated_step.get(field,'')
     if (not ref and not es.get(step['id'],{}).get(field)) or re.search(r'[\u3400-\u9fff]',str(english)):
      missing.append(node['id']+':step:'+step['id']+':'+field)
    if inline_math(step.get('body_md',''))!=inline_math(translated_step.get('body_md','')):
     math_differences.append({'id':node['id'],'step_id':step['id'],'classification':'inline_tex_text_difference_requires_semantic_review','zh':inline_math(step.get('body_md','')),'en':inline_math(translated_step.get('body_md',''))})
   for raw,eng in zip(node.get('proof_steps',[]),translated.get('proof_steps',[])):
    for key in ['id','formula_tex','shared_step_ref','result_step_ref']:
     if raw.get(key)!=eng.get(key):raise ValueError('Translation changed proof mapping: '+node['id']+':'+key)
    if machine_refs(raw.get('lean_refs',[]))!=machine_refs(eng.get('lean_refs',[])):raise ValueError('Translation changed formal Lean mapping: '+node['id'])
   checks.append({'kind':kind,'id':node['id'],'protected_fields_unchanged':True,'proof_steps':len(node.get('proof_steps',[]))})
 missing=list(dict.fromkeys(missing))
 if strict and missing:raise ValueError('Incomplete English content: '+', '.join(missing[:20]))
 return {'status':'passed' if not missing else 'in_progress','checks':checks,'missing':missing,'inline_math_differences':math_differences,'scope':'language_coverage_and_formal_identity_only_not_mathematical_review','inherited_fields':['Original source text and original notation','formula_tex','Lean machine names, paths, line numbers, reports and signatures'],'review_required':'Inline TeX text differences are reported for semantic review; they are not automatically judged mathematically unequal.'}
