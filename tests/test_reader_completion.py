"""Source extraction and missing adaptation must not acquire a completed label."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'reader'))
from check_completion import completion_report

def target():
 return {'id':'new-synthetic-result','paper_id':'new-paper','proof_target':True,'rewrite_status':'complete','rewrite_role':'proof',
  'source_transcription_status':'complete_mathematical_transcription','original_proof_md':'The author expands the finite sum.',
  'statement_tex':'a=b','symbol_ids':['symbol-a'],'notation_map':[{'original_tex':'a','canonical_tex':'a','note':'Same finite sum.'}],
  'source_refs':[{'source_id':'formal','locations':[{'pdf_page':1}]}],
  'proof_steps':[{'id':'step-1','body_md':'Pair terms with opposite signs; each pair contributes zero.','formula_tex':'a=b'}]}

def test_whole_page_extraction_is_not_a_complete_author_transcript():
 r=target();r['original_proof_md']='```text\nExtracted whole page with several properties.\n```'
 report=completion_report({'results':[r]})
 assert report['status']=='failed'
 assert 'raw_extracted_page_mislabeled_as_complete_mathematical_transcription' in report['incomplete'][0]['reasons']

def test_source_specific_symbols_and_adaptation_are_required():
 r=target();r['symbol_ids']=[];r['notation_map']=[]
 report=completion_report({'results':[r]})
 assert {'missing_related_symbols','missing_paper_notation_adaptation'} <= set(report['incomplete'][0]['reasons'])

def test_step_argument_can_state_its_basis_without_duplicate_justification():
 report=completion_report({'results':[target()]})
 assert report['status']=='passed'
 assert report['required_manual_step_basis_reviews'][0]['step_id']=='step-1'
