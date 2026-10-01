#!/usr/bin/env python3
"""Bind the maintained English translation's manual semantic review to inputs."""
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
WORK=Path(__file__).resolve().parent
source=ROOT/'corpus/public/reader/iclr2024-generalizable/content.json'
english=ROOT/'corpus/public/translations/iclr2024-generalizable.en.json'
a=json.loads(source.read_text());b=json.loads(english.read_text())
assert {r['id'] for r in a['results']}==set(b['results'])
checks=[
 {'topic':'fixed-input and baseline','finding':'g(S)=v(x_S) uses the raw output and does not impose g(empty)=0; the centered game is a distinct object.'},
 {'topic':'mask composition and label parameters','finding':'Repeated actual coordinate masks compose by intersection; label-game parameters remain separate when masked samples coincide.'},
 {'topic':'AND/OR reconstruction and empty coalition','finding':'Conditioned coefficients are recomputed; the OR complement-game transform applies only at nonempty coefficient indices, with the original empty OR baseline handled separately.'},
 {'topic':'nonzero baseline numerical example','finding':'The four game values 7,8,9,13 give raw AND coefficients 7,1,2,3 and nonempty OR coefficients 4,5,-3. The empty baseline remains 7; the conditioned singleton reconstructs as 7+1+0=8.'},
 {'topic':'noise variance','finding':'Variance uses the same fixed T random variable and all original independent noises. The finite sign coefficients have squared magnitude one; the empty-case variance remains sigma squared.'},
 {'topic':'row-norm counterexample and parent optimization','finding':'The (-3,2) example refutes only the pointwise signed-max expansion. Neither language claims that it proves distinct minima for the unresolved parent optimization equation.'},
 {'topic':'query counts and source-only claims','finding':'The 2^n count concerns masks/query labels, not injectively distinct samples. Approximation/citation/empirical statements retain their original scope and are not promoted to proved theorems.'}]
raw=json.loads((WORK/'evidence/bilingual-checks.json').read_text())
ids=set(b['results']);diffs=[d for d in raw['inline_math_differences'] if d['id'] in ids]
report={'status':'reviewed','scope':'manual_translation_semantics_of_these_30_results_not_independent_mathematical_acceptance','review_method':'English prose was authored and checked against the preserved active Chinese result text and the shared finite proof. Core baseline, quantifier, mask and counterexample boundaries were checked explicitly. Inline TeX formatting differences below remain visible; exact string inequality does not imply mathematical inequality.','results':len(ids),'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'english_sha256':hashlib.sha256(english.read_bytes()).hexdigest(),'translator_source_sha256':hashlib.sha256((WORK/'translate_generalizable.py').read_bytes()).hexdigest(),'checks':checks,'inline_tex_differences_reviewed':diffs,'formula_identity_checked_separately':'reader/bilingual.py preserves independent formula fields, step IDs and formal mappings; most inline differences add math delimiters or combine repeated numerical values.'}
(WORK/'evidence/generalizable-translation-semantic-review.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'status':'reviewed','results':len(ids),'inline_tex_difference_items':len(diffs)}))
