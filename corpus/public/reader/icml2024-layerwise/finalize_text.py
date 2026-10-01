import json
from pathlib import Path
P=Path(__file__).parent;d=json.loads((P/'content.json').read_text());s=json.loads((P/'symbols.json').read_text())
canonical={'model-output':'sym-model','masked-input':'sym-mask','set-game':'sym-game','output-baseline':'sym-output-baseline','input-baseline':'sym-input-baseline','layer-and-component':'sym-and-output','layer-or-component':'sym-or-output','layer-gamma':'sym-decomposition-parameter','layer-and-interaction':'sym-and-component-interaction','layer-or-interaction':'sym-or-component-interaction','layer-conditional-game':'sym-conditional-interaction','layer-shapley':'sym-shapley','layer-order':'sym-order'}
for a in s['symbols']:a['canonical_id']=canonical.get(a['id'],a['id'])
base=['model-output','masked-input','set-game','output-baseline','input-baseline'];comp=['layer-and-component','layer-or-component','layer-gamma','layer-and-interaction','layer-or-interaction'];metrics=['layer-order','layer-threshold','layer-salient-family','layer-shared','layer-all-strength','layer-overlap','layer-forget-new','layer-normalization','layer-ratios','layer-iou','layer-noise','layer-moments','layer-stability']
sets={'and-definition':base,'and-reconstruction':base,'decomposition':base+comp[:3],'or-definition':base+comp,'universal-matching':base+comp+['layer-conditional-game'],'salient-matching':base+comp+['layer-salient-family'],'probe-definition':['model-output','set-game','output-baseline','input-baseline','layer-probe','layer-feature','layer-probe-intercept','layer-residual','layer-residual-bound'],'metric-definition':base+comp+metrics,'strength-decomposition':['set-game','output-baseline']+comp+metrics[:8],'binomial-symmetry':['layer-order'],'shapley-and-or':base+comp+['layer-shapley'],'complement-duality':base+comp,'or-sparsity-inheritance':base+comp,'noise-ratio':['masked-input','layer-noise','layer-noise-ratio','layer-order'],'singleton-merge':['set-game','layer-and-interaction','layer-or-interaction'],'experiments':['layer-order','layer-salient-family'],'external-properties':['set-game','layer-and-interaction']}
for r in d['results']:
 k=r['id'].removeprefix('layer-');r['symbol_ids']=sets[k]
 for language in [r,r['translations']['en']]:
  for definition in language.get('definitions',[]):
   if definition['id']=='layer-objects':
    extra=r' 局部 $a=g_{and}$、$o=g_{or}$、$A=I_{g_{and}}$、$O=O_{g_{or}}$ 是对应公共概念的简称。' if language is r else r' Local $a=g_{and}$, $o=g_{or}$, $A=I_{g_{and}}$, and $O=O_{g_{or}}$ abbreviate the corresponding public concepts.'
    definition['body_md']+=extra
 for zs,es in zip(r['proof_steps'],r['translations']['en']['proof_steps']):
  if zs['lean_refs']:
   es['lean_refs']=[{**ref,'explanation_md':('This declaration checks the stated scalar algebra only; it does not establish the thresholded aggregate claim.' if 'scalar_strength' in ref['declaration'] else 'This declaration checks the final equality or explicitly stated intermediate scope of this step; the full human paragraph is not separately asserted as formalized.')} for ref in zs['lean_refs']]
# Compact object definitions on results that only use inversion, sharing, or a complementary transform.
for r in d['results']:
 if r['id'] in ['layer-universal-matching','layer-salient-matching','layer-shapley-and-or','layer-complement-duality','layer-or-sparsity-inheritance','layer-strength-decomposition']:
  for language in [r,r['translations']['en']]:
   for definition in language['definitions']:
    if definition['id']=='layer-objects':
     definition['body_md']=(r'固定有限 $N$、输入 $x$、输入基线 $r$；$g(U)=v(x_U)$，$b=g(\varnothing)$。$a=g_{and}=g/2+\gamma$、$o=g_{or}=g/2-\gamma$，$A=I_{g_{and}}$ 为 Möbius 交互，$O=O_{g_{or}}$ 为非空负补集交互。总输出与分量交互的作用域不同。' if language is r else r'Fix finite $N$, input $x$, and input baseline $r$; $g(U)=v(x_U)$ and $b=g(\varnothing)$. Write $a=g_{and}=g/2+\gamma$, $o=g_{or}=g/2-\gamma$, $A=I_{g_{and}}$ for the Möbius dividend, and $O=O_{g_{or}}$ for the nonempty negative complementary dividend. Total-output and component dividends have distinct scopes.')
d['symbols']=s['symbols'];(P/'symbols.json').write_text(json.dumps(s,ensure_ascii=False,indent=2)+'\n');(P/'content.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
