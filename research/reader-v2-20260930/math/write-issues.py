#!/usr/bin/env python3
from pathlib import Path
import hashlib,json,os
ROOT=Path(os.environ['ARCHIVE_PROJECT_ROOT'])
BASE=ROOT/'research/reader-v2-20260930/math'
PDF='research/paper-survey-20260930/recent/pdf/iclr2024-generalizable.pdf'
IMAGE='research/reader-v2-20260930/math/source-review/iclr2024-generalizable-page-14.png'
issue={
 'id':'issue-f11-or-intermediate-20260930','issue_id':'issue-f11-or-intermediate-20260930','classification':'source_proof_step_issue','status':'awaiting_user_confirmation','paper_id':'iclr2024-generalizable','affected_result_ids':['iclr2024-generalizable-andor'],
 'title':'OR 原证明的中间求和断言：内层和并非在全部 case(3) 条件下为零',
 'text_md':'正式 PDF 第 14 页 case(3) 的内层二项和被标为 0，但当 T⊆L⊊N 时内层可为 ±1。整层外和仍可能抵消，本记录不据此判断完整定理为假。用户确认与修正授权都待定。',
 'evidence_path':'research/reader-v2-20260930/math/issues.md',
 'source_refs':[{'source_id':'src-iclr2024-generalizable-main','local_path':PDF,'sha256':hashlib.sha256((ROOT/PDF).read_bytes()).hexdigest(),'pdf_page':14,'section':'Appendix C Proof(2) OR case(3)/(4)；Eq.(9)','image_path':IMAGE,'image_location':'case(3) 段落末的内层求和 underbrace=0；case(4) 的内层和下限 0','visually_checked':True}],
 'original_conditions_tex':r'L\cap T\ne\varnothing,\qquad L\ne N',
 'original_assertion_tex':r'\underbrace{\sum_{m=0}^{|T|-|T\cap L|}\binom{|T|-|T\cap L|}{m}(-1)^{|S^{\prime}|+m}}_{=0}',
 'counterexample':{'N':[1,2],'T':[1],'L':[1],'S_prime_cases':[{'S_prime':[],'inner_sum':1},{'S_prime':[2],'inner_sum':-1}],'outer_sum':0,'explanation_md':'这里 |T|−|T∩L|=0，内层只有 m=0；S′=∅ 时为 1，S′={2} 时为 −1。两者相加为 0。因此失败的是 underbrace 对每个固定 S′ 的判断；这组例子不是最终 OR 重构结论的反例。'},
 'case4_note':{'original_conditions_tex':r'L\cap T=\varnothing,\qquad L\ne N\setminus T','original_range_tex':r'0\le |S^{\prime\prime}|\le |T|','problem_md':'原文同时要求 S∩T≠∅，且 case(4) 有 L∩T=∅；因此 S′′=S∩T 在被计数的集合中应非空。原式从 0 开始包含了不满足 S∩T≠∅ 的项。','minimal_instance':{'N':[1,2],'T':[1],'L':[],'S_prime':[],'valid_inner_term_m':[1],'displayed_inner_term_m':[0,1],'valid_inner_sum':-1,'displayed_inner_sum':0},'impact_md':'这是同一 OR 四分类推导中的范围问题；外层仍可抵消，记录不判断全文结论为假，也不提供修正版推导。'},
 'impact_md':'影响范围为正式原证明第 14 页 OR 分类计算的中间等号及其解释。附录 C(1) 第 12–13 页的固定 x AND 子结论不受影响；本轮已验证的 AND adapter 不能关闭该原文问题。',
 'assessment':'specific_intermediate_assertion_has_counterexample_not_a_counterexample_to_the_theorem',
 'user_confirmation':'pending','fix_authorization':'pending','replacement_proof_published':False,
 'verification_boundary':'This report records a source-proof issue. The independent public Lean report does not verify this original OR derivation.'}
note={
 'id':'issue-f11-mask-notation-20260930','classification':'notation_alignment_note','is_mathematical_error':False,'status':'pending_alignment','paper_id':'iclr2024-generalizable','related_result_ids':['iclr2024-generalizable-andor','iclr2024-generalizable-and'],
 'title':'全文 Theorem 2 的 x_T 记号与附录固定 x 定义需要单独语义对齐',
 'text_md':'正文 Eq.(3) 与附录重述 Eq.(7) 用 I(S|x_T)，而附录 C(1) 的明确子结论及紧后的定义用固定 x。AND 子结论已按其原式对齐；全文记号未静默替换，也不据此判定定理为假。',
 'evidence_path':'research/reader-v2-20260930/math/issues.md',
 'source_locations':[{'pdf_page':3,'label':'Theorem 2 Eq.(3)'},{'pdf_page':12,'label':'Theorem 2 Eq.(7) 与 Proof(1) 固定 x 的陈述/定义'},{'pdf_page':13,'label':'Eq.(8) AND 推导与 OR 定义'}],
 'original_full_formula_tex':r'v(x_T)=\sum_{S\subseteq T}I_{\mathrm{and}}(S\mid x_T)+\sum_{S\in\{S:S\cap T\ne\varnothing\}\cup\{\varnothing\}}I_{\mathrm{or}}(S\mid x_T)',
 'original_and_subformula_tex':r'\forall T\subseteq N,\quad v_{\mathrm{and}}(x_T)=\sum_{S\subseteq T}I_{\mathrm{and}}(S\mid x)',
 'definition_convention_md':'原文单列 I_or(∅|x)=v_or(x_∅)，非空 OR 项采用 Eq.(2) 的负补集交替和。此处把空集处理归为明确的定义约定，不另登记成数学错误。',
 'impact_md':'本轮只形式化固定 x 的 AND 子结论。完整 Eq.(3)/(7) 的系数如何依赖再次掩码，仍需核对；尚无据此判定完整等式不成立的证据。',
 'agent_review_status':'agent_checked_difference_in_printed_notation','user_review_status':'pending','fix_authorization':'not_requested','formula_rewritten':False}
(BASE/'issues.json').write_text(json.dumps({'schema_version':'1.0','issues':[issue],'alignment_notes':[note],'issue_count':1,'alignment_note_count':1},ensure_ascii=False,indent=2)+'\n')
md=r'''# F11 正式原证明的局部问题与记号对齐说明

本报告仅登记具体原文事实、局部反例与影响范围。用户确认 `pending`，修正授权 `pending`。未改写原文、未补入假设、未发布完整 Theorem 2 的替代证明。普通抽取或记号待核对不会计作数学错误。

## 一项原证明中间步骤问题

问题 ID：`issue-f11-or-intermediate-20260930`。正式文件：`research/paper-survey-20260930/recent/pdf/iclr2024-generalizable.pdf`，PDF 第 14 页，Appendix C 的 OR proof case(3)/(4)。已直接看过 [整页图像](source-review/iclr2024-generalizable-page-14.png)，确认 case(3) 的 underbrace 只覆盖内层和，排除文本抽取的定位错误。

原文 case(3) 的条件是 \(L\cap T\ne\varnothing\)、\(L\ne N\)。其式中把下面内层和标为零：

\[
\underbrace{\sum_{m=0}^{|T|-|T\cap L|}\binom{|T|-|T\cap L|}{m}(-1)^{|S'|+m}}_{=0}.
\]

取 \(N=\{1,2\}\)、\(T=L=\{1\}\)，满足原文条件。此时 \(|T|-|T\cap L|=0\)，内层只有 \(m=0\)。当 \(S'=\varnothing\) 时内层和为 1；当 \(S'=\{2\}\) 时为 −1。因而对这两个允许的固定 \(S'\)，原文内层 `=0` 都不成立。

外层遍历 \(S'\subseteq\{2\}\)，两项 1 与 −1 总和仍为 0。这说明此反例只否定内层的逐项断言，不否定最终 OR 重构定理。影响范围是第 14 页分类计算中间等号及其说明。

同页 case(4) 另有被计数集合的范围问题：它同时要求 \(L\cap T=\varnothing\) 和 \(S\cap T\ne\varnothing\)，并定义 \(S''=S\cap T\)，但内层按 \(0\le|S''|\le|T|\) 求和。\(S''=\varnothing\) 不满足这次计数条件。取 \(N=\{1,2\}\)、\(T=\{1\}\)、\(L=\varnothing\)、\(S'=\varnothing\)：实际有效的内层仅 \(m=1\)，和为 −1；原显示范围含 \(m=0,1\)，和为 0。外层其他项仍可能抵消，因此也不把这个范围问题当作最终定理的反例。

附录 C(1) PDF 第 12–13 页的固定原样本 AND 子结论不依赖这些 OR 分类计算。本轮 AND 适配的 Lean 成功不会确认、修改或关闭本问题。需用户先确认这条原证明问题，修正方案另行授权；本报告不提供修正方案。

## 一项记号语义对齐说明

说明 ID：`issue-f11-mask-notation-20260930`，分类是 `notation_alignment_note`，不是数学错误。

正文 PDF 第 3 页 Eq.(3) 与第 12 页 Eq.(7) 的全文陈述使用 \(I_{\mathrm{and}}(S\mid x_T)\) 和 \(I_{\mathrm{or}}(S\mid x_T)\)。但第 12 页 Proof(1) 的明确子结论和下一段定义使用固定原样本 \(x\)：

\[
\forall T\subseteq N,\quad v_{\mathrm{and}}(x_T)=\sum_{S\subseteq T}I_{\mathrm{and}}(S\mid x).
\]

本轮已完成结果按这条原式对齐，正文 full Theorem 2 的 \(x_T\) 原式保留。完整公式的系数如何依赖再次掩码仍需核对，尚无据此判定原定理不成立的证据。原文给出的 OR 空集值 \(I_{\mathrm{or}}(\varnothing\mid x)=v_{\mathrm{or}}(x_\varnothing)\) 单列为定义约定，不额外登记数学错误。

原件未改动；完整 AND-OR 陈述的对齐、重写与形式化均未完成，用户审核状态 `pending`。相关图片：[第 3 页](source-review/iclr2024-generalizable-page-3.png)、[第 12 页](source-review/iclr2024-generalizable-page-12.png)。
'''
(BASE/'issues.md').write_text(md+'\n')
print('one source-proof-step issue and one separate notation note written')
