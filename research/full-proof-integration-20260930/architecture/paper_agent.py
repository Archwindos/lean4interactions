#!/usr/bin/env python3
"""Local, read-only access to the complete formal-paper package and reusable library.
No shell, source edit, model call, network call or subprocess is exposed.
"""
from __future__ import annotations
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]
WORK=Path(__file__).resolve().parents[1]

class PaperPackage:
    def __init__(self,root=ROOT):
        self.root=Path(root)
        self.path=self.root/'research/full-proof-integration-20260930/data/full-content.json'
        self.data=json.loads(self.path.read_text())
    def _one(self,collection,ident):
        matches=[r for r in self.data[collection] if r.get('id',r.get('paper_id'))==ident or r.get('canonical_id')==ident]
        if not matches:raise KeyError(f'Unknown {collection} ID: {ident}')
        return matches[0] if len(matches)==1 else matches
    def papers(self):return self.data['papers']
    def results(self,paper_id=None):return [r for r in self.data['results'] if not paper_id or r.get('paper_id')==paper_id]
    def result(self,id):return self._one('results',id)
    def inventory(self,paper_id=None):return [i for i in self.data['inventories'] if not paper_id or i['paper_id']==paper_id]
    def symbols(self,paper_id=None):return [s for s in self.data['symbols'] if not paper_id or any(m.get('paper_id')==paper_id for m in s.get('paper_mappings',[]))]
    def symbol(self,id):
        rows=[s for s in self.data['symbols'] if s['id']==id or s.get('canonical_id')==id]
        if not rows:raise KeyError('Unknown symbol: '+id)
        return {'concept_id':id,'records':rows,'conflicts':[m for s in rows for m in s.get('paper_mappings',[]) if m.get('relation_type') in ('conflict','pending_alignment')]}
    def shared(self,id=None):return self._one('shared_proofs',id) if id else self.data['shared_proofs']
    def paper_search(self,query):
        query=''.join((query or '').lower().split())
        return [p for p in self.papers() if query in ''.join(' '.join([p['id'],p['title'],p.get('short_title',''),p.get('venue',''),str(p.get('year',''))]).lower().split())]
    def search(self,query,paper_id=None):
        query=''.join((query or '').lower().split());out=[]
        for r in self.results(paper_id):
            entries=[e for i in self.inventory(r['paper_id']) for e in i['entries'] if e['id'] in r.get('inventory_ids',[])]
            labels=[r.get('original_label','')]+r.get('aliases',[])+[e.get('original_label','') for e in entries]+[a for e in entries for a in e.get('aliases',[])]
            if query in ''.join(' '.join([r['id'],r['title']]+labels).lower().split()):out.append({'id':r['id'],'title':r['title'],'paper_id':r['paper_id'],'original_labels':labels,'source_refs':r['source_refs'],
                'source_occurrences':[o for e in entries for o in e.get('occurrences',e.get('all_occurrences',[]))]})
        return out
    def issues(self,paper_id=None):return [i for i in self.data['issues'] if not paper_id or i.get('paper_id')==paper_id]
    def library(self,name=None):
        path=self.root/'catalog/library.json'
        catalog=json.loads(path.read_text()) if path.exists() else {'status':'unavailable'}
        evidence=self._report_evidence(catalog.get('verification_report'),[d['name'] for d in catalog.get('declarations',[])]) if isinstance(catalog,dict) else {'compilation':'unavailable','freshness':'unavailable'}
        if isinstance(catalog,dict):catalog['current_evidence']=evidence
        if not name:return catalog
        if isinstance(catalog,list):rows=catalog
        else:rows=catalog.get('declarations',catalog.get('entries',[]))
        return [{**r,'current_evidence':evidence} for r in rows if name in r.get('name',r.get('declaration',''))]
    def _report_evidence(self,report,names,scope='requested exact declarations'):
        if not report or not names or not (self.root/report).is_file():return {'compilation':'unavailable','axiom_audit':'unavailable','freshness':'unavailable'}
        spec=importlib.util.spec_from_file_location('full_reader_verification',Path(__file__).parent/'v2_verification_helper.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
        node={'id':'current-evidence','path':report,'scope':scope,'expected_declarations':names,'visibility':'public'}
        return mod.PaperPackage(root=self.root,manifest={'verification_reports':[node]},math_content={'results':[],'shared_proofs':[]}).report_evidence(node['id'])
    def verification_status(self,result_id):
        r=self.result(result_id);lean=r.get('lean',{})
        status={'result_id':result_id,'rewrite_status':r.get('rewrite_status'),'source_transcription_status':r.get('source_transcription_status','unreported'),
                'rewrite_role':r.get('rewrite_role'),'proof_scope':r.get('proof_scope'),
                'alignment_status':r.get('alignment_status'),'user_review_status':r.get('user_review_status','pending'),
                'formalization_scope':lean.get('scope',lean.get('completion_scope','unspecified')),'compilation':'unavailable','axiom_audit':'unavailable',
                'statement_assessment':r.get('statement_assessment'),
                'verification_role':r.get('verification_role','none'), 'evidence_role':lean.get('evidence_role','none')}
        report=lean.get('report_path');names=lean.get('declarations',[])
        if not report or not (self.root/report).is_file() or not names:return status
        evidence=self._report_evidence(report,names,status['formalization_scope'])
        status.update(evidence);status['result_id']=result_id
        if status['verification_role']=='counterexample':status['meaning']='A compiled counterexample does not prove the refuted original statement.'
        return status
    def validate(self):
        errors=[];warnings=[];ids={r['id'] for r in self.data['results']};source_ids={s['id'] for p in self.data['papers'] for s in p['sources']}
        for c in self.data['coverage']:
            if not c['result_ids'] or any(i not in ids for i in c['result_ids']):errors.append('Missing directory target '+c['inventory_id'])
        for inventory in self.data['inventories']:
            for source in inventory['sources']:
                path=self.root/source['path'];expected=source['sha256']
                if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest()!=expected:errors.append('Formal source changed '+source['source_id'])
                page_count=source.get('page_count',source.get('pdf_page_count',source.get('pages')))
                reviewed={p['pdf_page'] for p in inventory['page_audit'] if p['source_id']==source['source_id']}
                if reviewed!=set(range(1,page_count+1)):errors.append('Incomplete page audit '+source['source_id'])
        proof_index={r['id']:r for r in self.data['results']+self.data['shared_proofs']}
        def resolve_body(step,seen):
            ref=step.get('shared_step_ref') or step.get('result_step_ref')
            if not ref:return bool(step.get('body_md') or step.get('formula_tex'))
            key=(ref.get('proof_id',ref.get('result_id')),ref.get('step_id'))
            if key in seen:return False
            target=next((x for x in proof_index.get(key[0],{}).get('proof_steps',[]) if x.get('id')==key[1]),None)
            if target is None:return False
            return resolve_body(target,seen|{key})
        for r in proof_index.values():
            for sid in r.get('symbol_ids',[]):
                if not any(s['id']==sid for s in self.data['symbols']):errors.append('Missing symbol '+r['id']+':'+sid)
            for iid in r.get('related_issue_ids',[]):
                if not any(i['id']==iid for i in self.data['issues']):errors.append('Missing source issue '+r['id']+':'+iid)
            for ref in r.get('source_refs',[]):
                if ref['source_id'] not in source_ids:errors.append('Unknown source '+r['id'])
            for step in r.get('proof_steps',[]):
                if not resolve_body(step,set()):errors.append('Missing, cyclic or empty proof step '+r['id']+':'+str(step.get('id')))
            if r.get('rewrite_status')=='complete' and not r.get('proof_steps'):errors.append('Empty completed rewrite '+r['id'])
            for sid in r.get('shared_proof_ids',[]):
                if sid not in proof_index:errors.append('Missing shared proof '+r['id']+':'+sid)
        return {'status':'passed' if not errors else 'failed','scope':'directory_source_and_schema_checks_only','errors':errors,'warnings':warnings,
                'source_pages':sum(len(i['page_audit']) for i in self.data['inventories']),'inventory_entries':len(self.data['coverage']),'results':len(ids)}

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('action',choices=['papers','paper-search','results','result','inventory','symbols','symbol','shared','issues','verification-status','library','search','validate'])
    p.add_argument('id',nargs='?');p.add_argument('--paper-id')
    a=p.parse_args();package=PaperPackage()
    methods={'papers':lambda:package.papers(),'paper-search':lambda:package.paper_search(a.id),'results':lambda:package.results(a.paper_id),'result':lambda:package.result(a.id),
        'inventory':lambda:package.inventory(a.paper_id),'symbols':lambda:package.symbols(a.paper_id),'symbol':lambda:package.symbol(a.id),
        'shared':lambda:package.shared(a.id),'issues':lambda:package.issues(a.paper_id),'verification-status':lambda:package.verification_status(a.id),
        'library':lambda:package.library(a.id),'search':lambda:package.search(a.id,a.paper_id),'validate':lambda:package.validate()}
    try:result=methods[a.action]()
    except (KeyError,ValueError) as e:p.error(str(e))
    print(json.dumps(result,ensure_ascii=False,indent=2))
    return 1 if isinstance(result,dict) and result.get('status')=='failed' else 0

if __name__=='__main__':raise SystemExit(main())
