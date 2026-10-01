#!/usr/bin/env python3
"""Read-only structural/language feedback for a public draft; never admits it."""
import argparse,hashlib,json,re
from pathlib import Path
from bilingual import validate_translations
from inventory_contract import inventory_errors,content_errors,source_errors,issue_errors,machine_role_status_reviews,control_character_errors,CONTRACT_PATH
from symbols_english import translate_symbol
from evidence_paths import EVIDENCE

ROOT=Path(__file__).resolve().parents[1]

def check(ident):
 if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*',ident):raise ValueError('Invalid public paper ID')
 folder=ROOT/'corpus/public/reader'/ident
 paths=[folder/(key+'.json') for key in ['paper-metadata','inventory','content','symbols','issues']]
 raw=[path.read_bytes() for path in paths]
 metadata,inventory,content,symbols,issues=[json.loads(value) for value in raw]
 errors=inventory_errors(inventory,content)+content_errors(content)+source_errors(metadata)
 errors.extend(control_character_errors(symbols,'symbols'))
 symbols=symbols.get('symbols',[]) if isinstance(symbols,dict) else symbols
 issues=issues.get('issues',[]) if isinstance(issues,dict) else issues
 errors.extend(issue_errors(list(content.get('issues',[]))+issues,metadata,content))
 for sym in symbols:sym.setdefault('translations',{})['en']=translate_symbol(sym)
 try:
  language=validate_translations({**content,'papers':[metadata],'symbols':symbols,'issues':issues},strict=False)
  missing=language['missing'];differences=language['inline_math_differences']
 except ValueError as exc:missing=[str(exc)];differences=[]
 implementation=[Path(__file__).resolve(),CONTRACT_PATH]+[ROOT/'reader'/name for name in ['inventory_contract.py','bilingual.py','symbols_english.py','symbol_context_english.py','evidence_paths.py']]
 hashes={str(path.relative_to(ROOT)):hashlib.sha256(value).hexdigest() for path,value in zip(paths,raw)}
 hashes.update({str(path.relative_to(ROOT)):hashlib.sha256(path.read_bytes()).hexdigest() for path in implementation})
 changed=[str(path.relative_to(ROOT)) for path,value in zip(paths,raw) if path.read_bytes()!=value]
 errors.extend('input_changed_during_check='+path for path in changed)
 report={'scope':'Development-package structure and language only; no source/math/Lean acceptance or manifest mutation','paper_id':ident,'status':'rejected_draft' if errors or missing else 'structural_checks_passed_pending_mathematical_review','result_count':len(content.get('results',[])),'target_entries':sum(e.get('proof_target') is True for e in inventory.get('entries',[])),'target_result_ids':sorted({e.get('merge_target_id') or e.get('merge_id') or e['id'] for e in inventory.get('entries',[]) if e.get('proof_target') is True}),'non_target_entries':[{'id':e['id'],'kind':e.get('kind'),'reason':e.get('non_proof_reason'),'requires_source_and_content_review':True} for e in inventory.get('entries',[]) if e.get('proof_target') is False],'errors':errors,'bilingual_errors':missing,'inline_math_differences':differences,'input_hashes':hashes}
 report['machine_role_status_reviews']=machine_role_status_reviews(content)
 EVIDENCE.mkdir(exist_ok=True)
 (EVIDENCE/('draft-admission-'+ident+'.json')).write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
 return report

if __name__=='__main__':
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('paper_id');args=parser.parse_args()
 report=check(args.paper_id)
 print(json.dumps({key:report[key] for key in ['paper_id','status','result_count','target_entries','errors','bilingual_errors']},ensure_ascii=False))
 raise SystemExit(bool(report['errors'] or report['bilingual_errors']))
