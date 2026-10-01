"""Reject actual admission failures that would erase new mathematical targets."""
import sys
from pathlib import Path
import pytest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'reader'))
from inventory_contract import validate_inventory,issue_errors,control_character_errors

def inventory():
 return {'paper_id':'new-formal-paper','entries':[{'id':'proof','kind':'external_theorem','proof_target':True,'merge_target_id':'result'}],'proof_targets':['result']}

def result(ident,role='proof'):
 return {'id':ident,'title':ident,'rewrite_status':'in_progress','rewrite_role':role,'statement_assessment':'no_statement_error_recorded','lean':{'evidence_role':'none','declarations':[]}}

def test_missing_explicit_target_does_not_become_false():
 value=inventory();del value['entries'][0]['proof_target']
 with pytest.raises(ValueError,match='missing_or_nonboolean_proof_target'):validate_inventory(value)

@pytest.mark.parametrize('value',[0,1,'false',None])
def test_only_boolean_target_flags_are_valid(value):
 data=inventory();data['entries'][0]['proof_target']=value
 with pytest.raises(ValueError,match='missing_or_nonboolean_proof_target'):validate_inventory(data)

def test_external_theorem_cannot_leave_denominator_with_generic_reason():
 data=inventory();data['entries'][0].update(proof_target=False,non_proof_reason='An external citation.');data['proof_targets']=[]
 with pytest.raises(ValueError,match='non_target_kind_requires_mathematical_review'):validate_inventory(data)

@pytest.mark.parametrize('kind,reason',[('unknown','Not a proof.'),('definition','')])
def test_non_targets_require_known_classification_and_actual_reason(kind,reason):
 data=inventory();data['entries'][0].update(kind=kind,proof_target=False,non_proof_reason=reason);data['proof_targets']=[]
 with pytest.raises(ValueError):validate_inventory(data)

def test_misspelled_merge_field_cannot_silently_drop_mapping():
 data=inventory();data['entries'][0]['merged_target_id']=data['entries'][0].pop('merge_target_id')
 with pytest.raises(ValueError,match='unknown_merge_field=merged_target_id'):validate_inventory(data)

def test_root_target_list_and_entry_flags_must_agree():
 data=inventory();data['proof_targets']=[]
 with pytest.raises(ValueError,match='root_proof_targets_disagree'):validate_inventory(data)

def test_merge_target_must_exist_in_actual_content():
 with pytest.raises(ValueError,match='merge_target_not_an_actual_result'):validate_inventory(inventory(),{'results':[{'id':'wrong'}]})

def test_definition_reason_and_target_mapping_admit_without_default_flags():
 data=inventory();data['entries'].append({'id':'definition','kind':'definition','proof_target':False,'non_proof_reason':'This paragraph only defines the DFT and asserts no derived equality.'})
 validate_inventory(data,{'results':[result('result'),result('definition','source_material')]})

def test_two_results_cannot_resolve_the_same_inventory_entry():
 rows=[result('result'),result('another')]
 for row in rows:row['inventory_ids']=['proof']
 with pytest.raises(ValueError,match='ambiguous_actual_content_mapping'):validate_inventory(inventory(),{'results':rows})

def test_cross_id_inventory_reference_requires_an_explicit_merge():
 data=inventory();del data['entries'][0]['merge_target_id'];data['proof_targets']=['proof']
 row=result('result');row['inventory_ids']=['proof']
 with pytest.raises(ValueError,match='implicit_cross_id_mapping_requires_explicit_merge'):validate_inventory(data,{'results':[row]})

def test_accepted_legacy_root_target_list_remains_compatible():
 data=inventory();del data['entries'][0]['proof_target']
 data['entries'][0]['merged_target_id']=data['entries'][0].pop('merge_target_id')
 validate_inventory(data,legacy=True)

@pytest.mark.parametrize('field,value',[('statement_assessment','valid'),('statement_assessment','false_original_clause'),('rewrite_role','complete_proof')])
def test_unknown_semantic_role_is_not_defaulted_to_no_issue(field,value):
 row=result('result');row[field]=value
 with pytest.raises(ValueError,match='unknown_'+field):validate_inventory(inventory(),{'results':[row]})

def test_mixed_lean_role_is_not_reclassified_as_a_counterexample():
 row=result('result');row['lean']['evidence_role']='counterexample_and_partial_results'
 with pytest.raises(ValueError,match='unknown_lean_evidence_role'):validate_inventory(inventory(),{'results':[row]})

def test_shared_proof_requires_its_own_status_and_actual_evidence_binding():
 shared={'id':'shared','title':'A related proof','proof_steps':[{'id':'s','body_md':'A body.'}]}
 with pytest.raises(ValueError,match='missing_shared_field=rewrite_status'):validate_inventory(inventory(),{'results':[result('result')],'shared_proofs':[shared]})

@pytest.mark.parametrize('field,text',[
 ('original_proof_md','**Project source note (not author text):** The selected formal file provides no separate local author proof for this entry.'),
 ('original_statement_md','**Project source synopsis (not an author quotation):** The experiments compare transformation complexity and feature entanglement.'),
])
def test_explicit_project_attribution_cannot_fill_an_author_original_field(field,text):
 row=result('result');row[field]=text
 with pytest.raises(ValueError,match='project_comment_in_author_original_field='+field):
  validate_inventory(inventory(),{'results':[row]})

def issue_fixture():
 issue={'id':'error','title':'A source proof error','kind':'author_specific_proof_class','issue_type':'proof_step_error','source_refs':[{'source_id':'formal','version_id':'published-version','pdf_pages':[2]}],'related_result_ids':['proof']}
 metadata={'sources':[{'id':'formal','version_id':'published-version','total_pages':2}]}
 content={'results':[{'id':'proof','related_issue_ids':['error']}]}
 return issue,metadata,content

def test_explicit_issue_type_preserves_the_author_classification():
 issue,metadata,content=issue_fixture()
 assert issue_errors([issue],metadata,content)==[]
 assert issue['kind']=='author_specific_proof_class'

@pytest.mark.parametrize('field,value,message',[
 ('kind',None,'issue_kind_must_be_nonempty_metadata'),
 ('issue_type','statement_error','unknown_issue_type'),
 ('source_refs',[],'missing_precise_issue_source_refs'),
 ('related_result_ids',[],'missing_actual_issue_result_links'),
 ('related_result_ids',['absent'],'unknown_issue_result'),
])
def test_issue_requires_real_kind_type_sources_and_result_links(field,value,message):
 issue,metadata,content=issue_fixture();issue[field]=value
 assert any(message in e for e in issue_errors([issue],metadata,content))

@pytest.mark.parametrize('field,value,message',[
 ('source_id','unpublished-other','unknown_issue_formal_source'),
 ('version_id','preprint','issue_source_version_mismatch'),
 ('pdf_pages',[3],'issue_pdf_page_out_of_range'),
 ('pdf_pages',[True],'invalid_issue_pdf_pages'),
])
def test_issue_source_location_must_match_the_actual_formal_file(field,value,message):
 issue,metadata,content=issue_fixture();issue['source_refs'][0][field]=value
 assert any(message in e for e in issue_errors([issue],metadata,content))

def test_a_clause_counterexample_cannot_be_tagged_as_a_whole_statement_refutation():
 issue,metadata,content=issue_fixture();issue.update(issue_type='statement_counterexample',original_statement_status='compound_clause_counterexample_verified')
 assert any('issue_statement_assessment_scope_mismatch' in e for e in issue_errors([issue],metadata,content))

def test_issue_and_result_keep_a_reciprocal_affected_relation():
 issue,metadata,content=issue_fixture();content['results'][0]['related_issue_ids']=[]
 assert any('issue_result_missing_reciprocal_link' in e for e in issue_errors([issue],metadata,content))

@pytest.mark.parametrize('field,value,code',[
 ('original_tex','\beta','U+0008'),
 ('canonical_tex','\frac{a}{b}','U+000C'),
 ('statement_tex','\tau','U+0009'),
 ('definition_tex','\rho','U+000D'),
 ('body_md','Bias '+chr(8)+'eta is corrupt.','U+0008'),
 ('body_md','Value $\rho$.','U+000D'),
])
def test_corrupt_python_tex_escapes_are_rejected_before_rendering(field,value,code):
 row=result('result');row['notation_map']=[{field:value}]
 with pytest.raises(ValueError,match='invalid_control_characters='+code.replace('+',r'\+')):
  validate_inventory(inventory(),{'results':[row]})

def test_correct_tex_and_prose_line_breaks_are_preserved():
 value={'symbols':[{'canonical_tex':r'\beta+\frac{x}{\tau}+\rho',
  'description_md':'First paragraph.\n\nIndented\ttext.\r\nNext line.'}],
  'statement_tex':['x=x\ny=y',r'\beta=0']}
 assert control_character_errors(value)==[]
