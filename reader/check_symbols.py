#!/usr/bin/env python3
"""Account for every source symbol and mapping in the canonical registry."""
import hashlib,json
from pathlib import Path
from input_manifest import load_manifest,project_path
WORK=Path(__file__).resolve().parent

def main():
    manifest=load_manifest();data=json.loads((WORK/'data/full-content.json').read_text())
    registry=data['symbols'];errors=[];records=[];inputs=[]
    for item in manifest['papers']:
        path=project_path(item['symbols_path']);inputs.append({'path':item['symbols_path'],'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
        source=json.loads(path.read_text());rows=source.get('symbols',[]) if isinstance(source,dict) else source
        for symbol in rows:
            owners=[s for s in registry if symbol['id'] in s.get('record_ids',[]) and any(m.get('paper_id')==item['paper_id'] for m in s.get('paper_mappings',[]))]
            if len(owners)!=1:errors.append({'paper_id':item['paper_id'],'symbol_id':symbol['id'],'reason':'canonical_owner_count','count':len(owners)});continue
            owner=owners[0]
            for mapping in symbol.get('paper_mappings',[]):
                fingerprint={k:v for k,v in mapping.items() if k not in {'canonical_concept_id','source_concept_id'}}
                if not any({k:v for k,v in m.items() if k not in {'canonical_concept_id','source_concept_id'}}==fingerprint for m in owner.get('paper_mappings',[])):
                    errors.append({'paper_id':item['paper_id'],'symbol_id':symbol['id'],'reason':'source_notation_or_scope_mapping_missing'})
            records.append({'paper_id':item['paper_id'],'symbol_id':symbol['id'],'canonical_id':owner['id'],'source_mapping_count':len(symbol.get('paper_mappings',[]))})
    ids={s['id'] for s in registry}
    for result in data['results']:
        for ident in result.get('symbol_ids',[]):
            if ident not in ids:errors.append({'result_id':result['id'],'symbol_id':ident,'reason':'dangling_symbol_reference'})
    report={'status':'failed' if errors else 'passed','scope':'complete_symbol_record_and_source_mapping_accounting_not_mathematical_equivalence','source_symbol_records':len(records),'canonical_concepts':len(registry),'inputs':inputs,'full_content_sha256':hashlib.sha256((WORK/'data/full-content.json').read_bytes()).hexdigest(),'records':records,'errors':errors}
    (WORK/'evidence/symbol-coverage-checks.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'status':report['status'],'source_symbol_records':len(records),'canonical_concepts':len(registry),'errors':errors},ensure_ascii=False));return bool(errors)
if __name__=='__main__':raise SystemExit(main())
