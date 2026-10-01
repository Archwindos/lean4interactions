#!/usr/bin/env python3
"""Merge all inventoried formal-paper entries without inventing completed content."""
from __future__ import annotations
import copy
import hashlib
import json
import re
from pathlib import Path
from input_manifest import load_manifest, project_path
from bilingual import attach_translations

ROOT = Path(__file__).resolve().parents[1]
WORK = Path(__file__).resolve().parent
INPUTS = {}

def read(path):
    INPUTS[path.relative_to(ROOT).as_posix()] = hashlib.sha256(path.read_bytes()).hexdigest()
    return json.loads(path.read_text())

def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n')

def locations(entry):
    out=[]
    for role,keys in [('statement',('statement_locations','statement_location')),('proof',('proof_locations','proof_location','proof_ranges','proof_range'))]:
        for key in keys:
            rows=entry.get(key,[])
            if isinstance(rows,dict): rows=[rows]
            for row in rows:
                page_numbers=row.get('pdf_pages',[]) or ([row['pdf_page']] if row.get('pdf_page') else [])
                if not page_numbers and row.get('start_pdf_page'):
                    page_numbers=list(range(row['start_pdf_page'],row.get('end_pdf_page',row['start_pdf_page'])+1))
                for page in page_numbers:
                    out.append({'source_id':row['source_id'],'pdf_page':page,'role':role,'label':row.get('section',entry.get('original_label',''))})
    return out

def refs_normalized(refs):
    grouped={}
    for ref in refs:
        if not isinstance(ref,dict): continue
        sid=ref.get('source_id',ref.get('id'))
        if not sid: continue
        dst=grouped.setdefault(sid,{'id':sid,'source_id':sid,'locations':[]})
        if ref.get('locations'): dst['locations']+=copy.deepcopy(ref['locations'])
        else:
            numbers=ref.get('pdf_pages',[]) or ([ref['pdf_page']] if ref.get('pdf_page') else [])
            for page in numbers: dst['locations'].append({'pdf_page':page,'role':ref.get('role','statement'),'label':ref.get('label',ref.get('section','正式PDF'))})
    for dst in grouped.values():
        unique={json.dumps(x,sort_keys=True,ensure_ascii=False):x for x in dst['locations']}
        dst['locations']=list(unique.values())
    return list(grouped.values())

def normalize_issue(issue):
    issue=copy.deepcopy(issue)
    raw={k:copy.deepcopy(issue[k]) for k in ('category','kind','classification','statement_status','original_statement_status','assessment_status','status') if k in issue}
    issue['source_schema_status']=raw
    category=issue.get('issue_type') or issue.get('category') or issue.get('kind') or issue.get('classification')
    if category in {'false_original_statement','statement_counterexample'}:typ='statement_counterexample'
    elif category in {'undefined_original_scope','underspecified_decomposition_rule','false_under_displayed_definitions','statement_alignment_or_scope','expression_domain','scope_mismatch','external_scope_issue'}:typ='statement_alignment_or_scope'
    elif category=='analysis_subclause_counterexample':typ='analysis_subclause_counterexample'
    elif category in {'statement_counterexample','source_statement_counterexample'}:typ='statement_counterexample'
    elif category=='source_compound_claim_truncated_clause_counterexample':typ='statement_partial_counterexample'
    elif category in {'source_statement_assumption_gap','source_statement_definition_conflict','statement_notation_scope_issue','statement_parameter_domain_gap','conditional_source_example_scale_gap','notation_alignment_note','interpretation_scope_issue'}:typ='statement_alignment_or_scope'
    elif category=='algorithm_or_definition_boundary':typ='definition_or_algorithm_boundary'
    elif category in {'proof_case_and_mask_alignment_errors','proof_case_coverage_gap','proof_definition_and_boundary_error','proof_display_index_error','proof_error','proof_error_repaired','proof_step_error','source_proof_error','source_proof_notation_error','source_proof_step_issue'}:typ='proof_step_error'
    else:raise ValueError('Unknown issue category: '+str(category))
    issue['issue_type']=typ
    issue['assessment_status']='refuted' if category=='false_original_statement' else 'clause_refuted_parent_not_assessed' if typ=='analysis_subclause_counterexample' else 'refuted' if (issue.get('original_statement_status')=='counterexample_verified' or (typ=='statement_counterexample' and issue.get('status')=='statement_error_unrepaired')) else 'partially_refuted' if issue.get('original_statement_status')=='compound_clause_counterexample_verified' else 'recorded_for_review' if typ in {'statement_counterexample','statement_alignment_or_scope'} else 'proof_error_recorded'
    issue['affected_result_ids']=list(dict.fromkeys(issue.get('affected_result_ids',[])+issue.get('related_result_ids',[])))
    issue.setdefault('title',issue.get('original_label') or issue['id'])
    issue.setdefault('text_md',issue.get('description_md') or issue.get('summary_md') or issue.get('problem_md') or issue.get('analysis_md') or issue.get('evidence_md',''))
    if issue.get('translations',{}).get('en'):
        en=issue['translations']['en'];en.setdefault('title',issue.get('original_label') or issue['id']);en.setdefault('text_md',en.get('description_md') or en.get('summary_md') or en.get('problem_md') or en.get('analysis_md') or en.get('evidence_md',''))
    issue['source_refs']=refs_normalized(issue.get('source_refs',[]))
    return issue

def fallback(entry,paper_id):
    ident=entry.get('merge_target_id') or entry.get('merge_id') or entry['id']
    return {'id':ident,'paper_id':paper_id,'title':entry['title'],'kind':entry.get('kind','source_entry'),
            'original_label':entry.get('original_label',''),'inventory_ids':[entry['id']],
            'source_refs':refs_normalized(locations(entry)),'statement_tex':'','assumptions':[], 'definitions':[],
            'original_statement_md':'本条已列入全篇清单。原命题请查看对应正式PDF页；精确数学转录尚未交付。',
            'original_proof_md':'尚未交付完整数学转录；正式PDF对应页保留原证明。',
            'original_statement_source_type':'formal_pdf_reference_only', 'original_proof_source_type':'formal_pdf_reference_only',
            'source_transcription_status':'not_started','overview':entry.get('classification_basis',entry.get('classification_reason','')),
            'proof_steps':[],'shared_proof_ids':[],'symbol_ids':[],'notation_map':[],
            'rewrite_status':'not_started' if entry.get('proof_target') else 'not_applicable','alignment_status':'inventory_only','user_review_status':'pending',
            'lean':{'status':'not_formalized','declarations':[]},'related_issue_ids':entry.get('related_issue_ids',[]),
            'content_delivery_status':'awaiting_mathematical_content'}

def build():
    manifest=load_manifest(read)
    old_math=read(project_path(manifest['shared_proof_seed_path'])) if manifest.get('shared_proof_seed_path') else {'shared_proofs':[],'notation':{}}
    papers=[copy.deepcopy(read(project_path(item['metadata_path']))) for item in manifest['papers']]
    results={}; proofs={p['id']:copy.deepcopy(p) for p in old_math['shared_proofs']}
    issues={}; inventories=[]; symbols=[]; coverage=[]
    for item in manifest['papers']:
        folder=project_path(item['content_path']).parent; inventory=read(project_path(item['inventory_path'])); inventories.append(inventory)
        paper_id=inventory['paper_id']
        if paper_id!=item['paper_id']:raise ValueError('Configured inventory paper ID differs')
        content=read(project_path(item['content_path']))
        local=[]
        for r in content.get('results',[]):
            r=copy.deepcopy(r);r['source_semantic_status']={k:r[k] for k in ['statement_assessment','rewrite_role','verification_role'] if r.get(k)}
            r['paper_id']=paper_id; r['source_refs']=refs_normalized(r.get('source_refs',[]))
            allowed={'complete','in_progress','not_started','blocked_by_false_statement','blocked_by_source_issue','not_applicable','not_a_proof_target','complete_empirical_explanation','complete_external_reference_explanation','complete_with_scope_issue','complete_with_definition_only_counterexample','complete_with_original_domain_issue'}
            if r.get('rewrite_status') not in allowed:raise ValueError('Unknown rewrite status for '+r['id']+': '+str(r.get('rewrite_status')))
            if r.get('rewrite_status')=='blocked_by_false_statement':r['raw_rewrite_status']=r['rewrite_status'];r['rewrite_status']='blocked_by_source_issue'
            r.setdefault('shared_proof_ids',[r['shared_proof_id']] if r.get('shared_proof_id') else [])
            r['shared_proof_id']=next(iter(r['shared_proof_ids']),None)
            if r['id'] in results: raise ValueError('Duplicate result ID: '+r['id'])
            results[r['id']]=r; local.append(r)
        for proof in content.get('shared_proofs',[]): proofs[proof['id']]=copy.deepcopy(proof)
        issue_rows=content.get('issues',[])
        if item.get('issues_path') and project_path(item['issues_path'],False).is_file():
            value=read(project_path(item['issues_path'])); issue_rows+=value.get('issues',[]) if isinstance(value,dict) else value
        for issue in issue_rows: issues[issue['id']]=normalize_issue(issue)
        symbol_rows=content.get('symbols',[])
        if item.get('symbols_path') and project_path(item['symbols_path'],False).is_file():
            value=read(project_path(item['symbols_path'])); symbol_rows=value.get('symbols',[]) if isinstance(value,dict) else value
        symbols+=copy.deepcopy(symbol_rows)
        for entry in inventory['entries']:
            merge_id=entry.get('merge_target_id') or entry.get('merge_id') or entry['id']
            matched=[r for r in local if entry['id'] in r.get('inventory_ids',[]) or r['id']==merge_id]
            if not matched:
                r=fallback(entry,paper_id)
                if r['id'] in results:
                    results[r['id']].setdefault('inventory_ids',[]).append(entry['id']);matched=[results[r['id']]]
                else: results[r['id']]=r;local.append(r);matched=[r]
            if 'proof_target' in entry: target=entry['proof_target']
            else:
                ptargets=inventory.get('proof_targets',[])
                target=any((x.get('inventory_id')==entry['id'] or entry['id'] in x.get('inventory_ids',[]) or x.get('id')==entry.get('merge_target_id')) if isinstance(x,dict) else x==entry['id'] for x in ptargets)
            for r in matched:
                r['proof_target']=bool(r.get('proof_target',False) or target)
                r['source_refs']=refs_normalized(r['source_refs']+locations(entry))
                if target and r['rewrite_status']=='not_applicable':r['rewrite_status']='not_started'
            coverage.append({'paper_id':paper_id,'inventory_id':entry['id'],'result_ids':[r['id'] for r in matched],'proof_target':bool(target)})
        paper=next(p for p in papers if p['id']==paper_id)
        paper.setdefault('translations',{}).setdefault('en',{})['scope']='The directory covers every inventoried mathematical item in the formal main text, appendices and supplements. Source transcription, rewritten proof and Lean scope are recorded separately.'
        paper['scope']='目录覆盖正式正文、附录及补充材料的全部已登记数学条目；每条分别记录原文、重写与Lean范围。'
        paper['results']=[{'id':r['id'],'title':r['title'],'kind':r['kind'],'original_label':r.get('original_label','')} for r in local]
        paper['inventory_entry_count']=len(inventory['entries'])
    for path in manifest.get('additional_issues_paths',[]):
        path=project_path(path,False)
        if path.is_file():
            value=read(path)
            for issue in value.get('issues',[]) if isinstance(value,dict) else value:issues[issue['id']]=normalize_issue(issue)
    for issue in issues.values():
        canonical_paper=next((p['id'] for p in papers if any(s['id']==ref['source_id'] for s in p['sources'] for ref in issue.get('source_refs',[]))),None)
        if canonical_paper and issue.get('paper_id')!=canonical_paper:issue['source_paper_id']=issue.get('paper_id');issue['paper_id']=canonical_paper
        for ident in issue.get('affected_result_ids',[]):
            matched=[r for r in results.values() if r['id']==ident or ident in r.get('inventory_ids',[])]
            for r in matched:
                r['related_issue_ids']=list(dict.fromkeys(r.get('related_issue_ids',[])+[issue['id']]))
    deduplications=[]
    # Historical shared text remains immutable in the seed. The current snapshot
    # may bind its unchanged exact declarations to a new actual covering report.
    covering_reports=[]
    current_catalog=read(ROOT/'catalog/library.json')
    report_paths={r.get('lean',{}).get('report_path') for r in results.values() if r.get('lean',{}).get('report_path')}
    if current_catalog.get('verification_report'):report_paths.add(current_catalog['verification_report'])
    for path in sorted(report_paths):
        report=read(project_path(path))
        fresh=all((ROOT/x['path']).is_file() and hashlib.sha256((ROOT/x['path']).read_bytes()).hexdigest()==x['sha256'] for x in report.get('source_files',[]))
        if report.get('status')=='passed' and fresh and report.get('commands') and all(c.get('exit_code')==0 for c in report['commands']):covering_reports.append((path,report))
    for proof in proofs.values():
        lean=proof.get('lean',{});names={n if isinstance(n,str) else n.get('name') for n in lean.get('declarations',[])}
        if proof['id']=='proof-finite-mobius-uniqueness-v2':
            # A historical paper adapter is not a dependency of the generic
            # uniqueness proof. Step 5 already names reconstruction_unique,
            # whose funext implements this exact pointwise-to-function step.
            obsolete='ReaderV2.cvpr_unique_coefficients'
            lean['step_map']=[m for m in lean.get('step_map',[]) if m.get('declaration')!=obsolete]
            for step in proof.get('proof_steps',[]):
                step['lean_refs']=[r for r in step.get('lean_refs',[]) if (r if isinstance(r,str) else r.get('declaration'))!=obsolete]
        if names:
            for path,report in covering_reports:
                rows={d['name']:d for d in report['declarations']}
                if names<=rows.keys() and all(set(rows[n].get('axioms',[]))<={'propext','Classical.choice','Quot.sound'} for n in names):
                    lean['evidence_rebinding']={'historical_report_path':lean['report_path'],'current_report_path':path,'reason':'the current actual report covers these exact unchanged declarations'}
                    lean['report_path']=path
                    lean['source_fingerprint']=report['source_fingerprint']
                    break
    for r in results.values():
        related=[issues[i] for i in r.get('related_issue_ids',[]) if i in issues]
        r['statement_assessment']='refuted' if any(i['issue_type']=='statement_counterexample' and i['assessment_status']=='refuted' for i in related) else 'partially_refuted' if any(i['issue_type']=='statement_partial_counterexample' for i in related) else 'counterexample_recorded' if any(i['issue_type']=='statement_counterexample' for i in related) else 'scope_under_review' if any(i['issue_type']=='statement_alignment_or_scope' for i in related) else 'no_statement_error_recorded'
        if r.get('rewrite_status') in {'complete_with_scope_issue','complete_with_original_domain_issue'}:
            r['rewrite_role']='statement_scope_explanation';r['scope_label']='条件性证明与原文范围说明';r.setdefault('translations',{}).setdefault('en',{})['scope_label']='Conditional proof and source-scope explanation'
        elif r.get('rewrite_status')=='complete_with_definition_only_counterexample':
            r['rewrite_role']='partial_proof_with_refuted_clause';r['statement_assessment']='partially_refuted';r['scope_label']='显示定义版本的反例；最优选择版本未反驳';r.setdefault('translations',{}).setdefault('en',{})['scope_label']='Counterexample to the displayed-definition version; the optimal-selection version is not refuted'
        if any(c.get('id')=='parent_optimization_equation' and c.get('status')=='not_assessed' for c in r.get('clause_assessments',[])):r['statement_assessment']='scope_under_review'
        source_assessment=r.get('source_semantic_status',{}).get('statement_assessment')
        if source_assessment:
            assessment_map={x:x for x in ['refuted','partially_refuted','counterexample_recorded','scope_under_review','no_statement_error_recorded']};assessment_map.update({'scope_ambiguous':'scope_under_review','refuted_subclaim':'partially_refuted'})
            if source_assessment not in assessment_map:raise ValueError('Unknown declared assessment: '+source_assessment)
            r['statement_assessment']=assessment_map[source_assessment]
        if r.get('statement_assessment')=='scope_under_review' and not r.get('rewrite_role'):
            r['rewrite_role']='statement_scope_explanation'
        elif r.get('rewrite_role')=='corrected_proof_and_counterexample':r['rewrite_role']='partial_proof_with_refuted_clause'
        if r.get('rewrite_role')=='definition_context':r['rewrite_role']='source_material'
        elif r.get('rewrite_role')=='scope_analysis':r['rewrite_role']='statement_scope_explanation'
        if r.get('rewrite_role') and r['rewrite_role'] not in {'proof','counterexample','statement_scope_explanation','partial_proof_with_refuted_clause','partial_component','source_material'}:raise ValueError('Unknown rewrite role: '+r['rewrite_role'])
        declared_verification=r.get('source_semantic_status',{}).get('verification_role')
        verification_map={'partial_scope_verified':'partial_component','counterexample_or_scope_analysis':'partial_component','scope_explanation':'partial_component','counterexample':'counterexample','theorem_proof':'theorem_proof','partial_component':'partial_component','none':'none'}
        if declared_verification and declared_verification not in verification_map:raise ValueError('Unknown declared verification role: '+declared_verification)
        raw_lean_role=r.get('lean',{}).get('evidence_role') or r.get('lean',{}).get('verification_role')
        lean_role_map={'counterexample_with_explicit_partial_scope':'partial_component','grouped_block_step_and_regrouping_and_counterexample':'partial_component','counterexample_and_valid_architecture_subclaim':'partial_component','theorem_proof':'theorem_proof','partial_component':'partial_component','counterexample':'counterexample','none':'none'}
        if raw_lean_role and raw_lean_role not in lean_role_map:raise ValueError('Unknown Lean evidence role: '+raw_lean_role)
        raw_lean_status=r.get('lean',{}).get('status');r.setdefault('source_semantic_status',{})['lean_status']=raw_lean_status
        if raw_lean_status=='partial_scope_verified':r.setdefault('lean',{})['evidence_role']='partial_component';raw_lean_role='partial_component'
        if raw_lean_role:r.setdefault('source_semantic_status',{})['lean_evidence_role']=raw_lean_role;r['lean']['evidence_role']=lean_role_map[raw_lean_role]
        elif declared_verification:r.setdefault('lean',{})['evidence_role']=verification_map[declared_verification]
        names=r.get('lean',{}).get('declarations',[])
        declared_role=r.get('lean',{}).get('evidence_role') or r.get('lean',{}).get('verification_role')
        is_mixed=r['statement_assessment']=='partially_refuted'
        r['verification_role']='none' if not names else 'partial_component' if is_mixed else declared_role or ('counterexample' if r['statement_assessment']=='refuted' else 'partial_component' if r.get('lean',{}).get('status')=='partially_formalized' else 'theorem_proof')
        r.setdefault('lean',{})['evidence_role']=r['verification_role']
        if r['verification_role']=='partial_component' and r.get('rewrite_role') in {None,'proof'}:r['rewrite_role']='partial_component'
        if is_mixed:r['lean']['evidence_components']={'proved_clauses':[n for n in names if 'counterexample' not in (n if isinstance(n,str) else n.get('name','')).lower()], 'counterexample_clauses':[n for n in names if 'counterexample' in (n if isinstance(n,str) else n.get('name','')).lower()]}
        explanation_ids={'f11-external-sparsity','f11-theorem1-approx','f11-proposition1','iclr2024-sparse-salient-approximation','iclr2024-sparse-asymptotic-claim'}
        case2_refuted=any(c.get('id')=='case2_nonexponential_eta_implies_per_order_sparsity' and c.get('status')=='refuted' for c in r.get('clause_assessments',[]))
        if case2_refuted:
            r['rewrite_role']='counterexample';r['scope_label']='Case2逐阶稀疏推断的反例';r['statement_assessment']='partially_refuted'
            for issue in related:
                if issue['id']=='sparse-issue-asymptotic-sparsity':issue['issue_type']='statement_partial_counterexample';issue['assessment_status']='partially_refuted';issue['clause_assessments']=r['clause_assessments']
        elif r['id'] in explanation_ids:r['rewrite_role']='statement_scope_explanation'
        elif r['id']=='iclr2024-sparse-transfer-inference':r['rewrite_role']='counterexample';r['scope_label']='原推论的反例论证'
        elif r['id'] in {'iclr2024-sparse-lemma1','iclr2024-sparse-noise-variance','iclr2024-sparse-parity-mask'}:
            r['rewrite_role']='statement_scope_explanation';r['scope_label']={'iclr2024-sparse-lemma1':'Taylor展开的不同读法与反例','iclr2024-sparse-noise-variance':'方差主张与独立性前提','iclr2024-sparse-parity-mask':'奇偶交互的空集约定'}[r['id']]
        elif r['id']=='f11-mask-complexity':r['rewrite_role']='partial_component';r['lean']['evidence_role']='partial_component';r['verification_role']='partial_component'
        elif r['statement_assessment']=='partially_refuted':r['rewrite_role']='partial_proof_with_refuted_clause'
        elif r['statement_assessment']=='refuted':r['rewrite_role']='counterexample'
        elif r['verification_role']=='counterexample':r['rewrite_role']='counterexample'
        else:r.setdefault('rewrite_role','proof' if r.get('proof_target') else 'source_material')
        r['proof_scope']=r.get('proof_scope',r.get('completion_scope','not_delivered'))
        if not r.get('proof_target'):
            r['source_completion_scope']=r['proof_scope'];r['proof_scope']='source_material_no_proof_obligation';r['rewrite_role']='source_material'
        own=r.get('proof_steps',[])
        for sid in r.get('shared_proof_ids',[]):
            shared=proofs.get(sid,{})
            if own and own==shared.get('proof_steps'):
                r['proof_steps']=[{'id':'paper-notation-adaptation','title':'核对论文定义并应用公共证明',
                    'body_md':'本论文对象、量词、基线与下方公共命题一致。上方条件保留论文适用范围；公共证明全文在此连续呈现。',
                    'formula_tex':'','justification':'已核对的论文符号映射见本条 notation_map。','lean_refs':[]}]
                deduplications.append({'result_id':r['id'],'shared_proof_id':sid,'removed_exact_duplicate_steps':len(own)})
                break
    # Store exact duplicate public steps once. Same step ID and identical body /
    # formula are required; no fuzzy semantic merge is attempted. Prefer a small
    # independent shared lemma as the authoritative owner.
    step_owners={}
    ordered_proofs=sorted(proofs.values(),key=lambda p:(len(p.get('proof_steps',[])),p['id']))
    def step_key(step):return (step.get('id'),step.get('body_md',''),json.dumps(step.get('formula_tex',''),ensure_ascii=False,sort_keys=True))
    for proof in ordered_proofs:
        for index,step in enumerate(proof.get('proof_steps',[])):
            key=step_key(step)
            if not key[1] and not step.get('formula_tex'):continue
            owner=step_owners.get(key)
            if owner and owner['proof_id']!=proof['id']:
                proof['proof_steps'][index]={'id':step['id'],'title':step.get('title',''),'shared_step_ref':owner}
                deduplications.append({'proof_id':proof['id'],'step_id':step['id'],'authority':owner})
            else:step_owners[key]={'proof_id':proof['id'],'step_id':step['id']}
    result_owners={}
    # Components precede their composite parent, so a parent references already
    # reviewed exact component steps rather than duplicating them.
    ordered_results=sorted(results.values(),key=lambda r:(r['id']=='iclr2024-generalizable-andor',len(r.get('proof_steps',[])),r['id']))
    for r in ordered_results:
        for index,step in enumerate(r.get('proof_steps',[])):
            if step.get('id')=='paper-notation-adaptation':continue
            key=step_key(step);owner=step_owners.get(key)
            if owner:
                r['proof_steps'][index]={'id':step['id'],'title':step.get('title',''),'shared_step_ref':owner}
                deduplications.append({'result_id':r['id'],'step_id':step['id'],'authority':owner})
            elif key in result_owners:
                owner=result_owners[key]
                r['proof_steps'][index]={'id':step['id'],'title':step.get('title',''),'result_step_ref':owner}
                deduplications.append({'result_id':r['id'],'step_id':step['id'],'authority':owner})
            elif key[1] or step.get('formula_tex'):result_owners[key]={'result_id':r['id'],'step_id':step['id']}
    canonical_symbols={}
    explicit_concepts={'interaction-centered':'sym-centered-interaction','interaction-raw':'sym-and-interaction','or-interaction':'sym-centered-or-interaction',
       'variable-count':'sym-variable-count','sym-cvpr-input-dimension':'sym-variable-count','input-coordinate':'sym-input-coordinate',
       'marginal-difference':'sym-cvpr-marginal','shapley-interaction':'sym-cvpr-sii','shapley-taylor':'sym-cvpr-sti','beta-function':'sym-cvpr-beta'}
    catalog=read(ROOT/'catalog/library.json')
    available={d['name'] for d in catalog.get('declarations',[]) if not any(a=='sorryAx' for a in d.get('axioms',[]))}
    for _, report in covering_reports:
        available.update(d['name'] for d in report.get('declarations',[]) if set(d.get('axioms',[])) <= {'propext','Classical.choice','Quot.sound'})
    for sym in symbols:
        key=explicit_concepts.get(sym['id'],sym.get('canonical_id') or sym['id'])
        sym=copy.deepcopy(sym)
        lean_names=[];representations=[];planned=[]
        for name in sym.get('lean_names',[]):
            names=re.findall(r'\bHarsanyi\.[A-Za-z_][A-Za-z_0-9.]*',name)
            if not names or name not in names:representations.append(name)
            for found in names:
                if found in available:lean_names.append(found)
                else:planned.append(found)
        sym['lean_names']=list(dict.fromkeys(lean_names));sym['planned_lean_names']=list(dict.fromkeys(planned));sym['lean_representation_notes']=representations
        for mapping in sym.get('paper_mappings',[]):
            mapping['source_concept_id']=mapping.get('canonical_concept_id',sym['id'])
            mapping['canonical_concept_id']=key
        if key not in canonical_symbols:
            canonical_symbols[key]=copy.deepcopy(sym)
            canonical_symbols[key]['id']=key
            canonical_symbols[key]['canonical_id']=key
            canonical_symbols[key]['record_ids']=[sym['id']]
            canonical_symbols[key]['scope_variants']=[{'definition_tex':sym.get('definition_tex',''),'type_or_domain':sym.get('type_or_domain',''),'scope':sym.get('scope','')}]
        else:
            dest=canonical_symbols[key];dest['paper_mappings']+=sym.get('paper_mappings',[])
            dest['record_ids'].append(sym['id']);dest['aliases']=list(dict.fromkeys(dest.get('aliases',[])+sym.get('aliases',[])))
            dest.setdefault('lean_names',[]).extend(x for x in sym.get('lean_names',[]) if x not in dest.get('lean_names',[]))
            dest['scope_variants'].append({'definition_tex':sym.get('definition_tex',''),'type_or_domain':sym.get('type_or_domain',''),'scope':sym.get('scope','')})
    symbol_alias={alias:s['id'] for s in canonical_symbols.values() for alias in s['record_ids']}
    qualified_symbol_alias={(m['paper_id'],alias):s['id'] for s in canonical_symbols.values() for alias in s['record_ids'] for m in s.get('paper_mappings',[])}
    def symbol_for(result,ident):return qualified_symbol_alias.get((result['paper_id'],ident),symbol_alias.get(ident,ident))
    for r in results.values():
        r['symbol_ids']=list(dict.fromkeys(symbol_for(r,x) for x in r.get('symbol_ids',[])))
        if r['id'] in {'iclr2024-generalizable-and','iclr2024-generalizable-andor'}:r['symbol_ids']=list(dict.fromkeys(r['symbol_ids']+['sym-and-output','sym-and-component-interaction']))
        if r['id'] in {'iclr2024-generalizable-or','iclr2024-generalizable-andor'}:r['symbol_ids']=list(dict.fromkeys(r['symbol_ids']+['sym-or-output','sym-or-component-interaction','sym-conditional-interaction']))
    neutral={
       'sym-model':('v','模型标量输出',r'v:X\to\mathbb R','输入域X到实数','固定一个模型；输入域按论文与模型单列','模型值，不是集合函数本身。'),
       'sym-input':('x','固定输入',r'x\in X','X','固定模型的一次输入','在同一次交互计算中保持x固定。'),
       'sym-input-baseline':('r','输入基线向量',r'r\in X','X','固定掩码规则','输入基线的坐标/嵌入域按模型单列；不等于输出基线标量b。'),
       'sym-universe':('N','有限变量总体',r'N=\{1,\ldots,n\}','有限集合','当前所选输入变量','未选背景是否固定须按论文核对。'),
       'sym-variable-count':('n','总体变量数',r'n=|N|','自然数','当前有限总体N','总样本维数与选定变量数不一定相同。'),
       'sym-coalition':('S,T,A,L','变量子集',r'S,T,A,L\subseteq N','2^N','当前公式的绑定范围','每个求和变量在本式内绑定。'),
       'sym-mask':('x_S','保留S的掩码输入',r'(x_S)_i=\begin{cases}x_i&i\in S,\\r_i&i\notin S\end{cases}','X','固定x,r,N','相同输入基线作用于全部子集；背景规则按论文记录。'),
       'sym-game':('g(S)','掩码集合函数',r'g(S)=v(x_S)','2^N→ℝ','固定v,x,r,N','集合函数g与模型v分开记号。'),
       'sym-output-baseline':('b','输出基线标量',r'b=g(\varnothing)=v(x_\varnothing)','实数','固定模型与样本','输入基线向量记r；b是模型在全掩码输入上的输出。'),
       'sym-centered-game':('g_0(S)','去输出基线函数',r'g_0(S)=g(S)-b','2^N→ℝ','由当前g显式构造','是否先中心化由每篇原定义决定；不默认原输出b=0。'),
       'sym-and-interaction':('I_g(S)','原始Harsanyi交互',r'I_g(S)=\sum_{L\subseteq S}(-1)^{|S|-|L|}g(L)','实数','固定实值集合函数g','包含空集项；不同作用函数使用单独子概念。'),
       'sym-centered-interaction':('I_{g_0}(S)','中心化Harsanyi交互',r'I_{g_0}(S)=\sum_{L\subseteq S}(-1)^{|S|-|L|}g_0(L)','实数','中心化集合函数g₀','非空S时与I_g一致；空集值为0。'),
       'sym-and-output':(r'g_{\rm and}','AND分量集合函数',r'g=g_{\rm and}+g_{\rm or}','2^N→ℝ','固定总体、模型与掩码标签','分量按变量集合标签取值。若来自实际输入函数则是其掩码值；任意标签参数不保证能延拓为输入函数。'),
       'sym-or-output':(r'g_{\rm or}','OR分量集合函数',r'g=g_{\rm and}+g_{\rm or}','2^N→ℝ','固定总体、模型与掩码标签','与AND分量组成同一掩码游戏；各分量的空集值由论文约定决定。'),
       'sym-and-component-interaction':(r'I_{g_{\rm and}}(S)','AND分量的交互',r'I_{g_{\rm and}}(S)=\sum_{L\subseteq S}(-1)^{|S|-|L|}g_{\rm and}(L)','实数','指定AND分量游戏','这是AND分量的Möbius变换，不自动等于原模型的I_g。'),
       'sym-or-component-interaction':(r'O_{g_{\rm or}}(S)','OR分量的交互',r'S\ne\varnothing:\quad O_{g_{\rm or}}(S)=-\sum_{L\subseteq S}(-1)^{|S|-|L|}g_{\rm or}(N\setminus L)','实数','指定总体N与OR分量游戏','非空式包含负号；空集由分量的基线约定单列。'),
       'sym-conditional-interaction':(r'I_{f^T},O_{f^T}','条件掩码游戏的交互',r'f^T(L)=f(T\cap L)','由2^N→ℝ的f和T得到新游戏','固定当前分量f与保留标签T','对f^T重新求AND或OR系数。物理输入函数情形由同基线掩码合成得到；标签游戏不要求输入掩码映射单射。'),
    }
    for key,(tex,name,definition,domain,scope,description) in neutral.items():
        if key in canonical_symbols:canonical_symbols[key].update(canonical_tex=tex,name_zh=name,definition_tex=definition,type_or_domain=domain,scope=scope,description_md=description)
    for key,empty in [('sym-and-interaction',r'I_g(\varnothing)=b'),('sym-centered-interaction',r'I_{g_0}(\varnothing)=0'),('sym-centered-game',r'g_0(\varnothing)=0')]:
        if key in canonical_symbols:canonical_symbols[key]['empty_set_convention']=empty
    for key,empty in [('sym-and-component-interaction',r'I_{g_{\rm and}}(\varnothing)=g_{\rm and}(\varnothing)'),('sym-or-component-interaction',r'O_{g_{\rm or}}(\varnothing)=g_{\rm or}(\varnothing)'),('sym-conditional-interaction',r'f^T(\varnothing)=f(\varnothing)')]:
        if key in canonical_symbols:canonical_symbols[key]['empty_set_convention']=empty
    for r in results.values():
        defs=[];definition_ids=[]
        for item in r.get('definitions',[]):
            if isinstance(item,str) and symbol_for(r,item) in canonical_symbols:
                sid=symbol_for(r,item);sym=canonical_symbols[sid];definition_ids.append(sid)
                defs.append({'id':sid,'symbol_id':sid,'definition_origin':'symbol_registry','text_md':sym['name_zh']+'：'+sym.get('description_md',''),'formula_tex':sym.get('definition_tex','')})
            else:defs.append(item)
        r['definitions']=defs;r['definition_symbol_ids']=definition_ids
    t2=results.get('iclr2024-sparse-theorem2')
    if t2 and t2.get('assumptions') and t2['assumptions'][0]=='Assumptions1α、2、3':
        # Display the already transcribed original assumptions at their point
        # of use; these references do not add or alter a mathematical premise.
        ids=['iclr2024-sparse-assumption-1alpha','iclr2024-sparse-assumption2','iclr2024-sparse-assumption3']
        t2['assumptions']=[{'id':ident,'text_md':results[ident]['original_label']+'：'+results[ident]['title'],
                            'formula_tex':results[ident]['statement_tex'],'source_result_id':ident} for ident in ids]+t2['assumptions'][1:]
    canonical_symbols['sym-mobius-transform']={'id':'sym-mobius-transform','canonical_id':'sym-mobius-transform','canonical_tex':'I_f',
        'name_zh':'有限集合Möbius变换','definition_tex':r'I_f(S)=\sum_{L\subseteq S}(-1)^{|S|-|L|}f(L)',
        'description_md':'这是共同的变换操作。其作用函数f决定空集值：原始g、中心化g₀、AND分量与再次掩码的分量是不同实例。',
        'type_or_domain':'实值有限集合函数→实值有限集合函数','scope':'公共父概念','assumptions':['有限S'],
        'empty_set_convention':r'I_f(\varnothing)=f(\varnothing)','baseline_convention':'不默认f(∅)=0',
        'aliases':[],'paper_mappings':[],'lean_names':['Harsanyi.interaction'],'version':'1.0','record_ids':[]}
    for key,acting in [('sym-and-interaction','g'),('sym-centered-interaction','g_0'),('sym-and-component-interaction','g_and')]:
        if key in canonical_symbols:canonical_symbols[key]['parent_concept_id']='sym-mobius-transform';canonical_symbols[key]['acting_function']=acting
    output={'schema_version':'3.0','language':'zh-CN','papers':papers,'results':list(results.values()),
            'shared_proofs':list(proofs.values()),'issues':list(issues.values()),'symbols':list(canonical_symbols.values()),'inventories':inventories,
            'coverage':coverage,'notation':old_math['notation'],'merge_status':'content_is_incremental_completion_is_per_result'}
    language_report=attach_translations(output,manifest,read,project_path,strict=False)
    write(WORK/'evidence/bilingual-checks.json',language_report)
    write(WORK/'data/full-content.json',output)
    write(WORK/'data/papers.json',{'schema_version':'3.0','papers':papers})
    write(WORK/'data/math-content.json',{k:output[k] for k in ('schema_version','language','results','shared_proofs','notation')})
    write(WORK/'math/issues.json',{'issues':output['issues']})
    issue_lines=['# 原文数学问题与修正记录','', '原式和来源保留；证明错误与命题错误分别登记。此文件由当前全篇输入生成。','']
    for issue in output['issues']:
        issue_lines+=['## '+issue.get('title',issue['id']),'', '记录 ID：'+issue['id'], '',issue.get('text_md',issue.get('summary_md',issue.get('problem_md',''))),'']
        for key in ('original_formula_tex','original_assertion_tex','counterexample_tex'):
            if issue.get(key):issue_lines+=['\\['+issue[key]+'\\]','']
        for key in ('evidence_md','counterexample_md','impact_md'):
            if issue.get(key):issue_lines+=[issue[key],'']
        issue_lines+=['来源：'+', '.join(x['source_id']+' PDF '+str(l['pdf_page']) for x in issue.get('source_refs',[]) for l in x.get('locations',[]) if l.get('pdf_page')),'']
    (WORK/'math/issues.md').write_text('\n'.join(issue_lines),encoding='utf-8')
    write(WORK/'evidence/aggregate-report.json',{'status':'passed','scope':'directory_coverage_and_exact_duplicate_normalization','inventory_entries':len(coverage),'covered_entries':len(coverage),
        'paper_counts':{p['id']:sum(r['paper_id']==p['id'] for r in results.values()) for p in papers},
        'result_count':len(results),'shared_proof_count':len(proofs),'issue_count':len(issues),'symbol_records':len(symbols),
        'missing_directory_entries':[],'exact_shared_proof_deduplications':deduplications,
        'inputs':[{'path':p,'sha256':h} for p,h in sorted(INPUTS.items())]})
    return {'status':'merged','inventory_entries':len(coverage),'result_pages':len(results),'papers':len(papers)}

if __name__=='__main__': print(json.dumps(build(),ensure_ascii=False))
