#!/usr/bin/env python3
"""Check actual local retrieval, evidence roles, schemas and negative fixtures."""
import copy
import hashlib
import json
from pathlib import Path
from paper_agent import PaperPackage

ROOT=Path(__file__).resolve().parents[2];WORK=Path(__file__).resolve().parents[1]
def schema_errors(schema,value,path='$'):
    """Validate the used JSON Schema subset; fail on unsupported keywords."""
    allowed={'$schema','title','description','type','const','enum','required','properties','items','additionalProperties'}
    unknown=set(schema)-allowed
    if unknown:return [path+': unsupported schema keywords '+str(sorted(unknown))]
    errors=[];kind=schema.get('type')
    matches={'object':isinstance(value,dict),'array':isinstance(value,list),'string':isinstance(value,str),'boolean':isinstance(value,bool),'integer':isinstance(value,int) and not isinstance(value,bool),'number':isinstance(value,(int,float)) and not isinstance(value,bool),'null':value is None}
    if kind and not matches.get(kind,False):return [path+': expected '+kind]
    if 'const' in schema and value!=schema['const']:errors.append(path+': const mismatch')
    if 'enum' in schema and value not in schema['enum']:errors.append(path+': enum mismatch')
    if isinstance(value,dict):
        errors.extend(path+': missing '+key for key in schema.get('required',[]) if key not in value)
        props=schema.get('properties',{})
        if schema.get('additionalProperties') is False:errors.extend(path+': unexpected '+key for key in set(value)-set(props))
        for key,subschema in props.items():
            if key in value:errors+=schema_errors(subschema,value[key],path+'.'+key)
    if isinstance(value,list) and 'items' in schema:
        for i,item in enumerate(value):errors+=schema_errors(schema['items'],item,path+'['+str(i)+']')
    return errors
def main():
    p=PaperPackage();checks=[]
    def check(name,value,detail=None):checks.append({'name':name,'passed':bool(value),'detail':detail})
    paths=[WORK/'data/full-content.json',WORK/'architecture/agent-package.json',ROOT/'catalog/library.json',Path(__file__).resolve()]
    def fingerprints():return {str(x.relative_to(ROOT)):hashlib.sha256(x.read_bytes()).hexdigest() for x in paths}
    before=fingerprints();check('directory-source-and-reference-validation',p.validate()['status']=='passed',p.validate())
    check('cross-paper-Shapley-search',len({r['paper_id'] for r in p.search('Shapley')})==3)
    check('ambiguous-Sparse-Theorem6-search',set(r['id'] for r in p.search('Theorem 6','iclr2024-sparse'))=={'iclr2024-sparse-theorem3','iclr2024-sparse-theorem6'})
    check('whole-paper-title-search',[r['id'] for r in p.paper_search('Generalizable')]==['iclr2024-generalizable'])
    check('search-results-unique',len(p.search(''))==len({r['id'] for r in p.search('')}))
    dummy=p.verification_status('cvpr2023-dummy');check('dummy-is-counterexample',dummy['statement_assessment']=='refuted' and dummy['evidence_role']=='counterexample' and dummy['compilation']=='passed',dummy)
    valid=p.verification_status('iclr2024-sparse-axiom-dummy');check('nonempty-Sparse-dummy-is-theorem',valid['evidence_role']=='theorem_proof' and valid['compilation']=='passed',valid)
    partial=p.verification_status('cvpr2023-baseline-faithfulness');check('mixed-compound-is-partial',partial['statement_assessment']=='partially_refuted' and partial['evidence_role']=='partial_component',partial)
    parent=p.result('f11-equation10');check('Eq10-parent-not-refuted',parent['statement_assessment']=='scope_under_review' and any(c['status']=='not_assessed' for c in parent['clause_assessments']))
    check('Eq10-counterexample-only-subclause',p.verification_status('f11-equation10')['evidence_role']=='counterexample')
    for ident in ('f11-theorem1-approx','f11-proposition1','iclr2024-sparse-salient-approximation'):
        check('unquantified-claim-not-full-proof:'+ident,p.result(ident)['rewrite_role']=='statement_scope_explanation')
    case2=p.result('iclr2024-sparse-asymptotic-claim');check('Case2-refutation-not-T2-refutation',case2['rewrite_role']=='counterexample' and any(c.get('id')=='exact_T2_T3' and c.get('status')=='unchanged_and_verified' for c in case2['clause_assessments']))
    for ident in ('sym-and-interaction','sym-centered-interaction','sym-centered-or-interaction','sym-or-interaction','sym-and-component-interaction','sym-or-component-interaction','sym-conditional-interaction'):
        check('scoped-symbol:'+ident,len(p.symbol(ident)['records'])==1)
    catalog=p.library();check('library-current',catalog['library_version']=='0.2.0' and catalog['current_evidence']['freshness']=='current')
    expected={'Harsanyi.Sparsity.CoefficientWitness':'type','Harsanyi.Sparsity.CoefficientWitness.mk':'constructor','Harsanyi.Sparsity.CoefficientWitness.representation':'projection','Harsanyi.Sparsity.CoefficientWitness.leadingBound':'projection','Harsanyi.Sparsity.CoefficientWitness.positiveBound':'projection'}
    for name,kind in expected.items():
        rows=[r for r in p.library(name) if r['name']==name];check('actual-structure-type:'+name,len(rows)==1 and rows[0]['kind']==kind and bool(rows[0]['signature']))
    for filename,document in [('full-content.schema.json',p.data),('package.schema.json',json.loads((WORK/'architecture/agent-package.json').read_text()))]:
        errors=schema_errors(json.loads((WORK/'architecture'/filename).read_text()),document);check('declared-schema-subset:'+filename,not errors,errors)
    check('unsupported-schema-keywords-rejected',bool(schema_errors({'type':'object','oneOf':[]},{})))
    original=p.data
    for label,mutate in [('missing-actual-body',lambda r:r.update(rewrite_status='complete',proof_steps=[])),('missing-shared-reference',lambda r:r.update(shared_proof_ids=['unknown-proof'])),('missing-symbol-reference',lambda r:r.update(symbol_ids=['unknown-symbol'])),('missing-issue-reference',lambda r:r.update(related_issue_ids=['unknown-issue']))]:
        p.data=copy.deepcopy(original);mutate(p.data['results'][0]);check('negative:'+label,p.validate()['status']=='failed')
    p.data=original;after=fingerprints();check('bound-files-unchanged-during-API-check',before==after)
    report={'status':'passed' if all(c['passed'] for c in checks) else 'failed','scope':'retrieval_schema_evidence_role_and_reference_checks_only','checks':checks,'snapshot_hashes':{'before':before,'after':after}}
    (WORK/'evidence/api-checks.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'status':report['status'],'checks':len(checks),'failures':[c for c in checks if not c['passed']]},ensure_ascii=False));return int(report['status']!='passed')
if __name__=='__main__':raise SystemExit(main())
