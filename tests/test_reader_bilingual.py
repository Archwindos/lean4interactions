"""Translation coverage and proof identity checks, independent of mathematics."""
import sys
from pathlib import Path
import pytest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'reader'))
from bilingual import merge_overlay,validate_translations
from lean_english import attach_lean_english

def test_chinese_text_in_english_lean_reference_does_not_pass_coverage():
 target={'id':'proof','lean':{'step_map':[{'step_id':'s','declaration':'Actual.theorem','explanation_md':'待译对应说明'}]},'translations':{'en':{'proof_steps':[{'id':'s','lean_refs':[{'declaration':'Actual.theorem','explanation_md':'待译对应说明'}]}]}}}
 report=attach_lean_english({'results':[target],'shared_proofs':[]})
 assert report['missing']==['proof:lean_step:s:explanation_md']

def test_english_lean_reference_translates_explanation_with_machine_identity():
 target={'id':'proof','lean':{'step_map':[{'step_id':'s','declaration':'Actual.theorem','signature':'P → P','status':'passed','explanation_md':'待译对应说明'}]},'translations':{'en':{'proof_steps':[{'id':'s','lean_refs':[{'declaration':'Actual.theorem','explanation_md':'The current declaration covers this step.'}]}]}}}
 report=attach_lean_english({'results':[target],'shared_proofs':[]})
 row=target['lean']['step_map'][0]
 assert report['missing']==[]
 assert row['translations']['en']['explanation_md']=='The current declaration covers this step.'
 assert (row['declaration'],row['signature'],row['status'])==('Actual.theorem','P → P','passed')

def node():
 return {'id':'proof','title':'中文标题','overview':'概述','assumptions':['有限集合'],
  'definitions':[{'id':'g','body_md':'集合函数','formula_tex':'g(S)=v(x_S)'}],
  'proof_scope':'完整有限等式','rewrite_status':'complete','lean':{'status':'verified'},
  'proof_steps':[{'id':'step','title':'配对消去','body_md':'有限求和。','formula_tex':'x=x','justification':'相反符号',
   'lean_refs':[{'declaration':'Harsanyi.test','source_path':'lean/Test.lean','line':1,'explanation_md':'真实声明'}]}],
  'translations':{'en':{'title':'Title','overview':'Overview','assumptions':['Finite set'],
   'definitions':[{'id':'g','body_md':'Set function'}],'proof_scope':'Complete finite identity',
   'proof_steps':[{'id':'step','title':'Pair cancellation','body_md':'A finite sum.','justification':'Opposite signs'}]}}}

def test_preserves_formula_mapping_and_all_status():
 n=node();en=merge_overlay(n,n['translations']['en'])
 assert en['proof_steps'][0]['formula_tex']=='x=x'
 assert en['proof_steps'][0]['lean_refs']==n['proof_steps'][0]['lean_refs']
 assert en['rewrite_status']=='complete' and en['lean']==n['lean']
 assert validate_translations({'results':[n],'shared_proofs':[]})['status']=='passed'

@pytest.mark.parametrize('field,value',[('rewrite_status','in_progress'),('formula_tex','x=0'),('lean',{'status':'verified'}),('hidden_count',2)])
def test_cannot_change_status_formula_or_nontext(field,value):
 n=node();target=n if field in {'rewrite_status','lean','hidden_count'} else n['proof_steps'][0]
 changed={'lean':{'status':'stale'}} if field=='lean' else {field:value}
 with pytest.raises(ValueError):merge_overlay(target,changed)

def test_explanatory_lean_text_can_translate_without_changing_machine_ref():
 n=node()['proof_steps'][0];ref=n['lean_refs'][0]
 en=merge_overlay(n,{'lean_refs':[{**ref,'explanation_md':'Actual declaration'}]})
 assert en['lean_refs'][0]['explanation_md']=='Actual declaration'
 with pytest.raises(ValueError):merge_overlay(n,{'lean_refs':[{**ref,'declaration':'False.theorem'}]})

@pytest.mark.parametrize('missing',['assumptions','definitions','proof_scope','body_md','title','justification'])
def test_missing_or_chinese_proof_text_is_not_complete(missing):
 n=node();en=n['translations']['en']
 if missing in {'assumptions','definitions','proof_scope'}:del en[missing]
 else:en['proof_steps'][0][missing]='未翻译'
 with pytest.raises(ValueError,match='Incomplete English'):validate_translations({'results':[n],'shared_proofs':[]})

def test_empty_english_assumption_and_definition_are_rejected():
 n=node();n['translations']['en']['assumptions']=[''];n['translations']['en']['definitions'][0]['body_md']=''
 with pytest.raises(ValueError,match='Incomplete English'):validate_translations({'results':[n],'shared_proofs':[]})

def test_symbol_domain_and_mapping_explanations_need_real_translation():
 symbol={'id':'symbol','canonical_tex':'x','name_zh':'输入','type_or_domain':'输入域','scope':'固定样本',
  'paper_mappings':[{'paper_id':'paper','original_tex':'x','relation_type':'same_definition','conflict_note':'局部作用域'}],
  'translations':{'en':{'name_zh':'Input','type_or_domain':'Input domain','scope':'Fixed sample','paper_mappings':[{'conflict_note':''}]}}}
 with pytest.raises(ValueError,match='Incomplete English'):validate_translations({'results':[],'shared_proofs':[],'symbols':[symbol]})
 symbol['translations']['en']['paper_mappings'][0]['conflict_note']='The symbol has a local scope.'
 assert validate_translations({'results':[],'shared_proofs':[],'symbols':[symbol]})['status']=='passed'
 assert merge_overlay(symbol,symbol['translations']['en'])['paper_mappings'][0]['original_tex']=='x'

def test_scope_variant_conventions_cannot_disappear_in_english():
 symbol={'id':'symbol','scope_variants':[{'scope':'局部集合函数','baseline_convention':'保留非零基线'}],
  'translations':{'en':{'scope_variants':[{'scope':'Local set function','baseline_convention':''}]}}}
 with pytest.raises(ValueError,match='Incomplete English'):validate_translations({'results':[],'shared_proofs':[],'symbols':[symbol]})
 symbol['translations']['en']['scope_variants'][0]['baseline_convention']='Preserve a nonzero baseline.'
 assert validate_translations({'results':[],'shared_proofs':[],'symbols':[symbol]})['status']=='passed'

def test_new_author_scope_translation_overrides_an_unknown_dictionary_entry():
 from symbols_english import translate_symbol
 symbol={'id':'new-symbol','name_zh':'新局部概念',
  'scope_variants':[{'type_or_domain':'作者新增的精确域','scope':'作者新增的局部范围',
   'translations':{'en':{'type_or_domain':'The source-specific domain.', 'scope':'The local scope supplied by the author.'}}}],
  'translations':{'en':{'name_zh':'New local concept'}}}
 symbol['translations']['en']=translate_symbol(symbol)
 assert validate_translations({'results':[],'shared_proofs':[],'symbols':[symbol]})['status']=='passed'
 assert symbol['translations']['en']['scope_variants'][0]['scope']=='The local scope supplied by the author.'
