import json
from pathlib import Path

BASE=Path('research/full-proof-integration-20260930/iclr2024-sparse')
issue={
 'id':'cvpr-issue-bow-table7-probability-scale', 'paper_id':'cvpr2023-sparse-concepts',
 'kind':'conditional_source_example_scale_gap',
 'issue_type':'conditional_source_example_scale_gap',
 'assessment_status':'conditional_incompatibility_proved; table7_output_scale_not_specified',
 'title':'Table7若沿用相邻概率输出尺度，则数值不相容；本节未说明尺度变化',
 'source_inventory_ids':['cvpr-inv-bow'], 'affected_result_ids':['cvpr-inv-bow'],
 'source_refs':[{
   'source_id':'src-cvpr2023-supplement', 'version_id':'ver-cvpr2023-formal',
   'pdf_pages':[17,18], 'section':'Appendix I; footnote after Table6; Table7',
   'image_paths':[str(BASE/'review-evidence/cvpr-supp-17.png'),str(BASE/'review-evidence/cvpr-supp-18.png')]}],
 'original_formula_tex':r'v(x_S)=p(y=\text{positive sentiment}\mid x_S)\quad\text{(p17: In this example)},\qquad w_{\{\mathrm{smart}\}}=6.568,\quad w_{\{\mathrm{not},\mathrm{smart}\}}=-13.481\quad\text{(Table7)}',
 'analysis_formula_tex':r'\left[\forall L,\ 0\le g(L)\le1\right]\ \Longrightarrow\ w_{\{i\}}=g(\{i\})-g(\varnothing)\in[-1,1],\quad w_{\{i,j\}}=g(\{i,j\})-g(\{i\})-g(\{j\})+g(\varnothing)\in[-2,2].',
 'analysis_md':'正式p17脚注在Table6相邻例子写In this example，采用概率输出；p18Table7有单变量6.568和二变量−13.481。若Table7继续使用这一概率尺度，原Möbius差分分别受[−1,1]及[−2,2]限制，故两表值与该定义不能同时成立。但是该脚注没有无歧义声明延续到Table7，原本节也未说明尺度是否变化；这里不无条件判表数据已证伪。正式PNG已实际查看，排除了文本提取误差。',
 'impact_scope':'Only the conditional compatibility between the neighboring probability-output convention and Table7 reported values; not a counterexample to arbitrary-real reconstruction, uniqueness, attribution, or unconditional Table7 data.',
 'statement_status':'conditional_incompatibility_if_same_probability_scale; unconditional_table7_values_not_refuted',
 'resolution_status':'source_scope_ambiguity_recorded_without_changing_data_or_output_definition',
 'fix_authorization':'proof_only_granted', 'statement_fix_authorization':'not_granted',
 'user_confirmation':'not_required_to_record_source_issue', 'user_review_status':'pending',
 'evidence_role':'scope_explanation', 'verification_role':'scope_explanation',
 'review_path':str(BASE/'review-of-cvpr-and-generalizable-finite.md')}
(BASE/'review-source-issues.json').write_text(json.dumps({'schema_version':1,'issues':[issue],
 'scope':'independent cross-review source issue only; other agents own their source content'},ensure_ascii=False,indent=2)+'\n')
print(issue['id'])
