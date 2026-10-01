"""Canonical metadata for proven identities with an original quotient boundary.

This deliberately does not change statements, premises, prose, source text,
Lean evidence roles, declarations or compiled reports.
"""
CORRECTIONS={
 'decoder-backpropagation':dict(
  statement_assessment='scope_under_review',
  rewrite_status='complete_with_original_domain_issue',
  scope_label='有限和解释下完整证明；原正弦商存在未定义频率',
  scope_label_en='Complete proof using finite sums; the original sine quotient is undefined at some frequencies'),
 'decoder-geometric-sum':dict(
  statement_assessment='scope_under_review',
  rewrite_status='complete_with_original_domain_issue',
  rewrite_role='partial_component',
  scope_label='有限和全域成立；原正弦商分母零点未定义',
  scope_label_en='Finite sums hold everywhere; the original sine quotient is undefined at its denominator zeros')
}

def apply_status_correction(row):
 correction=CORRECTIONS.get(row['id'])
 if not correction:return
 for key,value in correction.items():
  if key!='scope_label_en':row[key]=value
 row.setdefault('translations',{}).setdefault('en',{})['scope_label']=correction['scope_label_en']
