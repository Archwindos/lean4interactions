#!/usr/bin/env python3
"""Strictly validate every active proof overlay, separate from mathematics."""
import json
from pathlib import Path
from bilingual import validate_translations
from evidence_paths import EVIDENCE,input_hashes
WORK=Path(__file__).resolve().parent
if __name__=='__main__':
 data=json.loads((WORK/'data/full-content.json').read_text())
 report=validate_translations(data,strict=False)
 report['input_hashes']=input_hashes(WORK/'data/full-content.json',WORK/'bilingual.py',WORK/'evidence_paths.py',Path(__file__).resolve())
 (EVIDENCE/'bilingual-checks.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps({'status':report['status'],'entries':len(report['checks']),'missing':report['missing'],'inline_tex_differences':len(report['inline_math_differences'])}))
 raise SystemExit(bool(report['missing']))
