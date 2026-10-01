#!/usr/bin/env python3
"""Export actual local query tools/resources with explicit snapshot fingerprints."""
import hashlib
import json
from pathlib import Path
from paper_agent import PaperPackage

ROOT=Path(__file__).resolve().parents[2];WORK=Path(__file__).resolve().parents[1];HERE=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def build():
    package=PaperPackage();data=package.data
    resources=[]
    paths=[WORK/'data/full-content.json',WORK/'data/papers.json',WORK/'data/math-content.json',WORK/'math/issues.json',ROOT/'catalog/library.json',ROOT/'corpus/public/reader/input-manifest.json']
    for path in paths:
        resources.append({'id':str(path.relative_to(ROOT)),'path':str(path.relative_to(ROOT)),'sha256':sha(path),'visibility':'public'})
    tools=[]
    actions=['papers','paper-search','results','result','inventory','search','symbols','symbol','shared','issues','verification-status','library','validate']
    requires={'paper-search','search','result','symbol','verification-status'}
    for action in actions:
        tools.append({'name':action,'transport':'local_python_cli','entrypoint':'reader/architecture/paper_agent.py',
          'input_schema':{'type':'object','properties':{'id':{'type':'string'},'paper_id':{'type':'string'}},'required':['id'] if action in requires else [],'additionalProperties':False},
          'read_only':True,'network':False,'executes_shell':False})
    nodes=[];edges=[]
    for kind,key in [('paper','papers'),('result','results'),('shared_proof','shared_proofs'),('symbol','symbols'),('issue','issues')]:
        for item in data[key]:nodes.append({'id':item['id'],'kind':kind})
    for r in data['results']:
        edges.append({'from':r['paper_id'],'to':r['id'],'relation':'contains'})
        edges.extend({'from':r['id'],'to':s,'relation':'uses_shared_proof'} for s in r.get('shared_proof_ids',[]))
        edges.extend({'from':r['id'],'to':s,'relation':'uses_symbol'} for s in r.get('symbol_ids',[]))
        edges.extend({'from':r['id'],'to':s,'relation':'has_source_issue'} for s in r.get('related_issue_ids',[]))
    out={'schema_version':'3.0','scope':'full_inventories_with_per_result_content_and_evidence_status','implementation':'local_read_only_python_not_deployed_mcp',
        'resources':resources,'tools':tools,'nodes':nodes,'edges':edges,'validation':package.validate()}
    (HERE/'agent-package.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
    schema={'$schema':'https://json-schema.org/draft/2020-12/schema','title':'Full formal-paper local package','type':'object',
      'required':['schema_version','resources','tools','nodes','edges','validation'],'properties':{'schema_version':{'const':'3.0'},'resources':{'type':'array'},'tools':{'type':'array'},'nodes':{'type':'array'},'edges':{'type':'array'},'validation':{'type':'object'}}}
    (HERE/'package.schema.json').write_text(json.dumps(schema,ensure_ascii=False,indent=2)+'\n')
    content_schema={'$schema':'https://json-schema.org/draft/2020-12/schema','title':'Full formal-paper content','type':'object',
      'required':['schema_version','papers','inventories','coverage','results','shared_proofs','symbols','issues'],'properties':{'schema_version':{'const':'3.0'}}}
    for key in ('papers','inventories','coverage','shared_proofs','symbols','issues'):content_schema['properties'][key]={'type':'array','items':{'type':'object'}}
    content_schema['properties']['results']={'type':'array','items':{'type':'object','required':['id','paper_id','proof_target','source_refs','rewrite_status','rewrite_role','proof_scope','statement_assessment','lean'],
      'properties':{'rewrite_status':{'enum':['complete','in_progress','not_started','blocked_by_source_issue','not_applicable','statement_refuted','not_a_proof_target','complete_empirical_explanation','complete_external_reference_explanation','complete_with_scope_issue','complete_with_definition_only_counterexample','complete_with_original_domain_issue']},'proof_target':{'type':'boolean'},
      'lean':{'type':'object','required':['evidence_role'],'properties':{'evidence_role':{'enum':['none','theorem_proof','counterexample','partial_component']}}}}}}
    (HERE/'full-content.schema.json').write_text(json.dumps(content_schema,ensure_ascii=False,indent=2)+'\n')
    return {'status':'built','resources':len(resources),'tools':len(tools),'nodes':len(nodes),'edges':len(edges),'validation':out['validation']}
if __name__=='__main__':print(json.dumps(build(),ensure_ascii=False))
