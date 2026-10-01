"""Precise source type, compound-claim scope and shared-dummy distinctions."""
from pathlib import Path
import json
BASE=Path('research/full-proof-integration-20260930/cvpr2023')
PAPER='cvpr2023-sparse-concepts'
d=json.loads((BASE/'content.json').read_text())
by={r['id']:r for r in d['results']}
eff=r'''**Supplement D.1(1)，PDF第4页效率性质的独立原重证：** $v(x)=\sum_{S\subseteq N}w_S$。
\[
\begin{aligned}\sum_{S\subseteq N}w_S
&=\sum_{S\subseteq N}\sum_{U\subseteq S}(-1)^{|S|-|U|}v(x_U)\\
&=\sum_{U\subseteq N}\sum_{U\subseteq S\subseteq N}(-1)^{|S|-|U|}v(x_U)\\
&=\sum_{U\subseteq N}\sum_{s=|U|}^{n}\sum_{\substack{U\subseteq S\subseteq N\\|S|=s}}(-1)^{s-|U|}v(x_U)\\
&=\sum_{U\subseteq N}v(x_U)\sum_{m=0}^{n-|U|}\binom{n-|U|}m(-1)^m
=v(x).
\end{aligned}
\]
作者说明唯一没有消去的情形是U=N。该段与C重构证明重复，但作为本篇独立出现的完整证明保留。'''
by['cvpr2023-reconstruction']['original_proof_md']+='\n\n'+eff
aog=r'''**正文PDF第5页3.3，完整有关等价重组的推导段（中文翻译与公式转录）。** 原SCM表示And-Sum：
\[
v(x)\approx\sum_{S\in\Omega}w_SC_S(x)=\sum_{S\in\Omega}w_S.
\]
作者说这一And-Sum可等价转为AOG。三层AOG底层为n个输入变量，第二层每个AND节点编码孩子变量的AND关系；例如 $x_4x_5x_6$ 是 $S=\{x_4,x_5,x_6\}$ 的因果模式，其 $w_S=2.0$。根是noisy OR节点，累加所有孩子AND节点的效应：$\mathrm{output}=\sum_{S\in\Omega}w_SC_S$。
为进一步简化，作者提取不同模式共享的coalition作为新节点：$x_5,x_6$ 在多个模式里共同出现，于是设
\[
\beta=\{x_5,x_6\},\qquad
\{x_4,x_5,x_6\}\longmapsto\{x_4,\beta\}.
\]
于是每个中间层coalition/pattern S的触发状态由其全部孩子的触发状态相乘：
\[
C_S=\prod_{S'\in\operatorname{Child}(S)}C_{S'}.
\]
Child(S)是组成S的全部输入变量或coalition；S触发当且仅当所有孩子触发。上述内容是作者的未编号等价推导；没有独立的树归纳定理。MDL目标及其贪心选择属于下一算法段，单独登记，不伪称此段已证明全局最优。'''
by['cvpr2023-aog-regrouping']['original_proof_md']=aog
by['cvpr2023-aog-regrouping']['original_proof_source_type']='complete_unnumbered_author_derivation_mathematical_transcription_with_chinese_translation'
addmul=r'''**正文PDF第7页4.1的原普通系数示例：** 给二值变量 $x_i\in\{0,1\}$，
\[
y=x_1x_3+x_3x_4x_5+x_4x_6,\qquad x=[1,1,1,1,1,1].
\]
原标注真值为 $\Omega_{\rm truth}=\{\{x_1,x_3\},\{x_3,x_4,x_5\},\{x_4,x_6\}\}$。作者解释二值乘法可作为AND关系，每个模式的全部变量共同出现时给输出贡献1。

**补充PDF第13页G.3，普通Add-Mul示例及两个输入：**
\[
v(x)=x_1+x_2x_3+x_3x_4x_5+x_4x_6,\quad x_i\in\{0,1\}.
\]
只有每个项包含的全部变量存在时，该项贡献。原两输入的真值列举为
\[
\begin{aligned}
x=[1,1,1,1,1,1]:\quad&\Omega_{\rm truth}=\{\{x_1\},\{x_2,x_3\},\{x_3,x_4,x_5\},\{x_4,x_6\}\},\\
x=[1,1,0,1,1,1]:\quad&\Omega_{\rm truth}=\{\{x_1\},\{x_4,x_6\}\}.
\end{aligned}
\]
**补充PDF第14页G.3，带系数扩展Add-Mul示例及全部原系数：**
\[
v(x)=3x_1-2x_2x_3-x_3x_4x_5+5x_4x_6.
\]
作者将每个项视为真值模式，因果效应就是该项系数。原列举为
\[
\begin{aligned}
x=[1,1,1,1,1,1]:\quad&w_{\{x_1\}}=3,\;w_{\{x_2,x_3\}}=-2,\;w_{\{x_3,x_4,x_5\}}=-1,\;w_{\{x_4,x_6\}}=5,\\
&w_S=0\quad\text{对其他 }S\subseteq\{x_1,\ldots,x_6\},\\
x=(1,1,0,1,1,1):\quad&w_{\{x_1\}}=3,\;w_{\{x_4,x_6\}}=5,\;w_S=0\quad\text{对其他 }S.
\end{aligned}
\]
这些是原文未编号示例、变量共同出现的解释以及模式/系数列举，不是作者给出一般线性组合定理的完整证明。项目另给一般有限证明，明确区别于13页sigmoid阈值标签。'''
by['cvpr2023-addmul-coefficients']['original_proof_md']=addmul
by['cvpr2023-addmul-coefficients']['original_proof_source_type']='complete_author_worked_examples_and_unnumbered_derivation_mathematical_transcription'

sti=by['cvpr2023-shapley-taylor']
sti['original_statement_md']=sti['original_statement_md'].replace('对正阶数k，k阶','对第k阶，k阶')
sti['original_statement_md']+=r' 原文没有明写 $k>0$；本轮证明和Lean对齐的是正阶数的有效定义域，不能把此条件伪记为作者原文的不等式。$k=0$不属于当前有效域核验。'
sti['completion_scope']='all three original branches on the explicitly documented positive-order definition domain; k=0 is not source-domain verified'

baseline=by['cvpr2023-baseline-faithfulness']
baseline['completion_scope']='verified full-interaction reconstruction subclaim; the source sentence also contains a separate truncated-loss claim with a counterexample'
baseline['lean']['scope']='full interaction vector unfaithfulness=0 after recomputing all coefficients for each fixed baseline; does not prove truncated loss only changes the L1 term'
baseline['related_issue_ids']=['cvpr-issue-baseline-truncated-loss']
baseline['source_claim_status']='compound_source_sentence_has_false_truncated_clause; verified algebraic subclaim preserved without rewriting the source assertion'
baseline['proof_steps'].append({'id':'base-truncated-counterexample','title':'原句关于截断损失的边界错误','body_md':r'原“just affects $\|w_\Omega\|_1$”不能解释为截断损失unfaith不随基线变。取单变量模型 $v(z)=z$、原输入x=1、输入基线r、只保留 $\Omega=\{\varnothing\}$。完整交互为 $w_\varnothing=r,w_{\{1\}}=1-r$；截断残差平方和为 $[r-r]^2+[1-r]^2=(1-r)^2$，随r变化。完整交互的unfaith始终0，但截断损失部分也可能改变。保留原句、单列该解释错误，不把原复合断言替换成较弱命题后算整体通过。','formula_tex':r'\operatorname{unfaith}(w_\Omega)=(1-r)^2','justification':'直接算两个掩码；不涉及训练或概率假设。','lean_refs':[]})

dummy_steps=[{'id':'dummy-nonempty-exact-domain','title':'有效公共命题的作用域','body_md':r'此公共性质要求S非空，与CVPR原空集量词不同，不能修复或替代CVPR错误命题。若i不在S，且每个U子集S都满足g(U∪{i})−g(U)=c，则含i的交互为S上常数c的交互。','formula_tex':r'S\ne\varnothing,\ \forall U\subseteq S,\ g(U\cup\{i\})=g(U)+c\ \Rightarrow\ I_g(S\cup\{i\})=0','justification':'原Sparse版本若本来排除空S，可以忠实适配；CVPR原版本不能。','lean_refs':[]}, {'id':'dummy-nonempty-pair','title':'完整子集配对消去','body_md':r'按含i/不含i对子集配对，指数差一，得 $I_g(S\cup\{i\})=\sum_{U\subseteq S}(-1)^{|S|-|U|}[g(U\cup\{i\})-g(U)]=c\sum_{U\subseteq S}(-1)^{|S|-|U|}$。因S非空，取一个元素j，再按U是否含j配对，两项符号相反，和0。若S空，和为c，因此非空条件确实必要。','formula_tex':'','justification':'不要求原始输出基线为0；原加法常数c可由g(i)−g空给出。','lean_refs':[]}]
d['shared_proofs'].append({'id':'shared-harsanyi-dummy-nonempty','title':'共享有效性质：非空环境的加法Dummy交互为零','statement_tex':dummy_steps[0]['formula_tex'],'assumptions':['i∉S；S非空；对子集U恒定加法效应c。'],'definitions':[],'proof_steps':dummy_steps,'rewrite_status':'complete','alignment_status':'agent_checked_full_statement','user_review_status':'pending','not_a_repair_of':'cvpr2023-dummy','lean':{'status':'not_yet_verified','declarations':['Harsanyi.interaction_additive_dummy_nonempty'],'report_path':str(BASE/'verification/report.json')}})

ix={'id':'cvpr-issue-baseline-truncated-loss','paper_id':PAPER,'title':'基线变化也会改变截断的平方残差损失','category':'source_compound_claim_truncated_clause_counterexample','source_refs':[{'source_id':'src-cvpr2023-main','version_id':'ver-cvpr2023-formal','pdf_pages':[5],'section':'3.2 first paragraph'}],'original_formula_tex':r'\text{change of baseline values always ensures unfaith}(w)=0\text{ and just affects }\|w_\Omega\|_1','evidence_md':baseline['proof_steps'][-1]['body_md'],'impact_md':'完整w各自重构的恒等式成立；不据此证明截断损失只变化L1。原复合句保留且分开状态。','related_result_ids':['cvpr2023-baseline-faithfulness'],'original_statement_status':'compound_clause_counterexample_verified','user_confirmation':'not_individually_reviewed','fix_authorization':'proof_only_granted','statement_fix_authorization':'not_granted','status':'false_clause_recorded_without_statement_replacement'}
d['issues'].append(ix)
issues=json.loads((BASE/'issues.json').read_text());issues['issues'].append(ix)
(BASE/'issues.json').write_text(json.dumps(issues,ensure_ascii=False,indent=2)+'\n')
with (BASE/'issues.md').open('a') as f:f.write('\n\n## '+ix['title']+'\n\n'+ix['evidence_md']+'\n\n'+ix['impact_md']+'\n')
for r in d['results']:
    (BASE/'transcripts'/f'{r["id"]}.md').write_text('# '+r['title']+'：来源数学转录\n\n'+r['original_statement_md']+'\n\n'+r['original_proof_md']+'\n')
    prose='# '+r['title']+'\n\n'+r['definitions'][0]['body_md']+'\n\n'+r'\['+r['statement_tex']+r'\]'+'\n\n'
    for s in r['proof_steps']:
        prose+='## '+s['title']+'\n\n'+s['body_md']+'\n\n'
        if s['formula_tex']:prose+=r'\['+s['formula_tex']+r'\]'+'\n\n'
    (BASE/'math'/f'{r["id"]}.zh.md').write_text(prose)
(BASE/'content.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
print('source types, duplicate efficiency proof, baseline scope, and valid shared Dummy refined')
