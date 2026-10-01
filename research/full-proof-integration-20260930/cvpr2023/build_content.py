"""Full source-specific content, not an automatic extraction or selected-result pilot."""
from pathlib import Path
import json

BASE=Path('research/full-proof-integration-20260930/cvpr2023')
PAPER='cvpr2023-sparse-concepts'
OLD=json.loads(Path('research/reader-v2-20260930/data/math-content.json').read_text())
INV=json.loads((BASE/'inventory.json').read_text())
ISSUES=json.loads((BASE/'issues.json').read_text())['issues']
for folder in ['transcripts','math','verification']: (BASE/folder).mkdir(exist_ok=True)
results=[]
shared=[]

def ref(kind,pages,section):
    return {'source_id':'src-cvpr2023-main' if kind=='main' else 'src-cvpr2023-supplement','version_id':'ver-cvpr2023-formal','pdf_pages':pages,'section':section}
def step(id,title,body,formula='',justification=''):
    return {'id':id,'title':title,'body_md':body,'formula_tex':formula,'justification':justification,'lean_refs':[]}

CONVENTION=r'''固定有限总体 $N$、输入 $x$ 与输入基线向量 $r$。掩码 $x_S$ 在 $S$ 内保留原坐标、在其余坐标使用同一个 $r$。模型是 $v:X\to\mathbb R$，集合函数是 $g(S)=v(x_S)$，输出基线是 $b=g(\varnothing)$。本文原始交互为
\[
w_A=I_g(A)=\sum_{U\subseteq A}(-1)^{|A|-|U|}g(U).
\]
所有子集求和包括空集。特别地 $w_\varnothing=b$。若改用 $g_0=g-b$，只有空集交互改为零；本篇的原始输出没有零基线假设。'''

def add(id,title,label,inv,statement,original_statement,original_proof,steps,shared_ids=None,issues=None,lean_names=None,kind='theorem',status='complete',source_refs=None,assumptions=None,overview=''):
    obj={'id':id,'paper_id':PAPER,'title':title,'kind':kind,'original_label':label,'inventory_ids':inv,
      'source_refs':source_refs or [],'statement_tex':statement,'assumptions':assumptions or [r'$N$有限；固定同一输入、模型和输入基线。'],
      'definitions':[{'id':'cvpr-objects','body_md':CONVENTION}],
      'original_statement_md':original_statement,'original_proof_md':original_proof,
      'original_statement_source_type':'formal_statement_mathematical_transcription_with_chinese_translation',
      'original_proof_source_type':'complete_author_mathematical_proof_transcription_with_chinese_prose_translation' if original_proof else 'no_separate_proof_in_this_paper',
      'original_statement_note':'数学公式与量词据正式PDF核对；中文是翻译，不是英文逐字原文。',
      'original_proof_note':'保留作者全部数学推导与必要论证文字，原错误不静默修。版面原文另由正式PDF及逐页source-evidence全文提供。未编号推导与作者没有给出的完整证明分别标识。',
      'overview':overview or '先核对论文对象与量词，再用有限集合恒等式给完整证明。',
      'proof_steps':steps,'shared_proof_ids':shared_ids or [],'symbol_ids':['sym-model','sym-input','sym-input-baseline','sym-mask','sym-universe','sym-coalition','sym-game','sym-output-baseline','sym-and-interaction'],
      'notation_map':[{'original_tex':r'v(\boldsymbol x_S)','canonical_tex':r'v(x_S)=g(S)','relationship':'same_definition'},{'original_tex':r'w_S','canonical_tex':r'I_g(S)','relationship':'renaming'}],
      'rewrite_status':status,'completion_scope':'entire original result; source proof and repaired proof separately preserved' if status=='complete' else 'original statement and proof preserved; original statement refuted without alteration',
      'alignment_status':'agent_checked_full_statement','user_review_status':'pending',
      'source_transcription_status':'complete_mathematical_transcription' if original_proof else 'statement_complete_no_separate_author_proof',
      'lean':{'status':'not_yet_verified','declarations':lean_names or [],'scope':'entire faithful statement' if status=='complete' else 'counterexample only; no proof of false statement','report_path':str(BASE/'verification'/'report.json')},
      'related_issue_ids':issues or []}
    results.append(obj)
    transcript='# '+title+'：来源数学转录\n\n'+original_statement+'\n\n'+original_proof+'\n'
    (BASE/'transcripts'/f'{id}.md').write_text(transcript)
    rewrite='# '+title+'\n\n'+CONVENTION+'\n\n'+r'\['+statement+r'\]'+'\n\n'
    for s in steps:
        rewrite+='## '+s['title']+'\n\n'+s['body_md']+'\n\n'
        if s['formula_tex']:rewrite+=r'\['+s['formula_tex']+r'\]'+'\n\n'
        if s['justification']:rewrite+=s['justification']+'\n\n'
    (BASE/'math'/f'{id}.zh.md').write_text(rewrite)
    obj['transcript_path']=str(BASE/'transcripts'/f'{id}.md');obj['rewrite_path']=str(BASE/'math'/f'{id}.zh.md')
    return obj

def add_shared(id,title,statement,steps,names):
    x={'id':id,'title':title,'statement_tex':statement,'assumptions':[r'有限集合函数 $g:\mathcal P(N)\to\mathbb R$；不假定 $g(\varnothing)=0$。'],'definitions':[{'id':'finite-game','body_md':CONVENTION}],'proof_steps':steps,'rewrite_status':'complete','alignment_status':'agent_checked_full_statement','user_review_status':'pending','lean':{'status':'not_yet_verified','declarations':names,'report_path':str(BASE/'verification'/'report.json')}}
    shared.append(x)
    return id

AUTHOR_RECON=r'''正式来源：正文 PDF 第3页 Theorem 1/Eq.(3)；补充 PDF 第2页 C/Eq.(2)。固定输入 $x$，取 $\Omega=2^N$，每个因果效应为 $w_A=\sum_{U\subseteq A}(-1)^{|A|-|U|}v(x_U)$。作者主张 $\forall S\subseteq N,\ Y(x_S)=v(x_S)$；补充材料另主张 Harsanyi dividend 是满足该忠实性要求的唯一度量。'''
AUTHOR_RECON_PROOF=r'''以下转录补充第3页完整证明数学内容（作者把两部分称为 necessity 与 sufficiency）。由正文SCM，$Y(x_S)=\sum_{A\in\Omega}w_A C_A(x_S)=\sum_{A\subseteq S}w_A$，故忠实性等价于 $v(x_S)=\sum_{A\subseteq S}w_A$。

**Necessity 原计算：** 对每个 $S\subseteq N$，
\[
\begin{aligned}
\sum_{A\subseteq S}w_A
&=\sum_{A\subseteq S}\sum_{L\subseteq A}(-1)^{|A|-|L|}v(x_L)\\
&=\sum_{L\subseteq S}\sum_{A\subseteq S:A\supseteq L}(-1)^{|A|-|L|}v(x_L)\\
&=\sum_{L\subseteq S}\sum_{a=|L|}^{|S|}\sum_{\substack{L\subseteq A\subseteq S\\|A|=a}}(-1)^{a-|L|}v(x_L)\\
&=\sum_{L\subseteq S}v(x_L)\sum_{m=0}^{|S|-|L|}\binom{|S|-|L|}{m}(-1)^m
=v(x_S).
\end{aligned}
\]
**Sufficiency 原证明：** 假设另一组系数 $\widetilde w_A$ 对全部掩码满足 $v(x_S)=\sum_{A\subseteq S}\widetilde w_A$。按 $|S|$ 归纳。作者列出三个基例：
\[
\widetilde w_\varnothing=v(x_\varnothing)=w_\varnothing;\quad
\widetilde w_{\{i\}}=v(x_{\{i\}})-v(x_\varnothing)=w_{\{i\}};\quad
\widetilde w_{\{i,j\}}=v(x_{\{i,j\}})-v(x_{\{i\}})-v(x_{\{j\}})+v(x_\varnothing)=w_{\{i,j\}}.
\]
原文字写“假设对任意 $|S|=s\ge2$ 成立，考虑 $|S|=s+1$”，计算中使用全部真子集的归纳结论：
\[
\begin{aligned}
v(x_S)&=\widetilde w_S+\sum_{A\subsetneq S}\widetilde w_A\\
&=\widetilde w_S+\sum_{A\subsetneq S}\sum_{L\subseteq A}(-1)^{|A|-|L|}v(x_L)\\
&=\widetilde w_S+\sum_{L\subsetneq S}\sum_{L\subseteq A\subsetneq S}(-1)^{|A|-|L|}v(x_L)\\
&=\widetilde w_S+\sum_{L\subsetneq S}\sum_{a=|L|}^{|S|-1}\sum_{\substack{L\subseteq A\subsetneq S\\|A|=a}}(-1)^{a-|L|}v(x_L)\\
&=\widetilde w_S+\sum_{L\subsetneq S}v(x_L)\underbrace{\sum_{m=0}^{|S|-|L|-1}\binom{|S|-|L|}{m}(-1)^m}_{0-(-1)^{|S|-|L|}}\\
&=\widetilde w_S-\sum_{L\subsetneq S}(-1)^{|S|-|L|}v(x_L).
\end{aligned}
\]
移项得到 $\widetilde w_S=v(x_S)+\sum_{L\subsetneq S}(-1)^{|S|-|L|}v(x_L)=\sum_{L\subseteq S}(-1)^{|S|-|L|}v(x_L)=w_S$，从而唯一性成立。原文字归纳句与计算实际采用的强归纳作用范围在重写中明示；不修改原命题。'''
for p in OLD['shared_proofs']:
    if p['id'] in ['proof-finite-mobius-reconstruction-v2','proof-finite-mobius-uniqueness-v2']:shared.append(p)
RECON_STEPS=[step('cvpr-recon-context','把原SCM译为同一组集合系数',r'固定原输入、模型、基线以后，$C_A(x_S)=1$ 当且仅当 $A\subseteq S$。因此原定理是对同一组 $w_A$、全部 $S\subseteq N$ 的恒等式。输入变量是否统计独立不出现在有限代数的前提中。'),step('cvpr-recon-main','有限双重求和与区间消去',r'对固定 $S$ 展开 $w_A$。每对 $L\subseteq A\subseteq S$ 只出现一次，交换有限求和不会改变项。固定L后，用 $B=A\setminus L\subseteq S\setminus L$ 给一一对应；指数 $|A|-|L|=|B|$。若 $L\ne S$，任选 $i\in S\setminus L$，把B按是否含i配对，符号相反，内和为0；若L=S，只有空集B，内和为1。故仅剩g(S)。',r'\sum_{A\subseteq S}w_A=\sum_{L\subseteq S}g(L)\sum_{B\subseteq S\setminus L}(-1)^{|B|}=g(S).'),step('cvpr-recon-empty','空集与两个变量核对',r'$S=\varnothing$ 时只有 $w_\varnothing=b$。取 $g(\varnothing)=7,g(\{1\})=8,g(\{2\})=9,g(\{1,2\})=13$，系数为7,1,2,3；完整输入和为13，空输入为7，单变量输入分别为8和9。')]
add('cvpr2023-reconstruction','Theorem 1：重构全部掩码输出','Theorem 1; Axiom (1) Efficiency',['cvpr-inv-thm1','cvpr-inv-efficiency'],r'\forall S\subseteq N,\quad\sum_{A\subseteq S}I_g(A)=g(S)=v(x_S)',AUTHOR_RECON,AUTHOR_RECON_PROOF,RECON_STEPS,['proof-finite-mobius-reconstruction-v2'],lean_names=['Harsanyi.reconstruction','FullCvpr.reconstruction'],source_refs=[ref('main',[3],'3.1'),ref('supp',[2,3,4],'C; D.1(1)')])
UNIQUE_STEPS=[step('cvpr-unique-quantifiers','保留全部掩码与同一组系数',r'假设 $d_A$ 是一组固定系数，且对每个 $S\subseteq N$（包括空集）都有 $g(S)=\sum_{A\subseteq S}d_A$。只给完整输入等式不能推出唯一性。'),step('cvpr-unique-induction','按集合基数作强归纳',r'基例S空集给 $d_\varnothing=g(\varnothing)=w_\varnothing$。强归纳假设是对所有 $A\subseteq N$ 且 $|A|<|S|$ 有 $d_A=w_A$；所有真子集正好满足这个范围。分别在S上应用假设重构与已证重构，减去相同的真子集项，得到 $d_S=w_S$。任意S均成立，因此系数逐项唯一。',r'd_S=g(S)-\sum_{A\subsetneq S}d_A=g(S)-\sum_{A\subsetneq S}w_A=w_S.'),step('cvpr-unique-empty','空集与必要的量词边界',r'仍以7,8,9,13为例，空集等式固定d空为7，两单变量等式固定1和2，再用完整输入固定3。若只知道 $g(N)=13$，比如把13全放在空集或全放在N均符合一个等式，所以不能省略其他掩码。')]
add('cvpr2023-uniqueness','Appendix C：全部掩码重构系数唯一','Appendix C sufficiency',['cvpr-inv-thm1-uniqueness'],r'[\forall S\subseteq N,\;\sum_{A\subseteq S}d_A=g(S)]\Longrightarrow\forall A\subseteq N,\;d_A=I_g(A)',AUTHOR_RECON,AUTHOR_RECON_PROOF,UNIQUE_STEPS,['proof-finite-mobius-uniqueness-v2'],lean_names=['Harsanyi.reconstruction_unique','FullCvpr.uniqueness'],source_refs=[ref('supp',[2,3],'C')])

LINEAR_ORIG=r'''补充第2页B(2)及第4页D.1(2)：若对全部 $S\subseteq N$ 有 $v(x_S)=t(x_S)+u(x_S)$，则 $w^v_S=w^t_S+w^u_S$。'''
LINEAR_PROOF=r'''第4页原完整显示推导（输出下标固定为S，保留错误）：
\[
\begin{aligned}w^v_S&=\sum_{U\subseteq S}(-1)^{|S|-|U|}v(x_S)\\
&=\sum_{U\subseteq S}(-1)^{|S|-|U|}[t(x_S)+u(x_S)]\\
&=\sum_{U\subseteq S}(-1)^{|S|-|U|}t(x_S)+\sum_{U\subseteq S}(-1)^{|S|-|U|}u(x_S)\\
&=w^t_S+w^u_S.\end{aligned}
\]
原式并非Harsanyi定义；问题和具体反例见 cvpr-issue-linearity-index。'''
LINEAR_STEPS=[step('linearity-pointwise','在真实求和自变量上代入原前提',r'设 $g_v(U)=g_t(U)+g_u(U)$ 对全部U成立。固定A，每个 $U\subseteq A$ 都可代入该前提；原证明的 $x_A$ 固定索引在此明确修为 $x_U$，原命题不变。'),step('linearity-distribute','有限求和逐项分配',r'对每个子集U，用实数乘法分配律拆成两项，再用有限求和的加法分配律拆成两和。两和分别是原定义的交互。',r'I_{g_v}(A)=\sum_{U\subseteq A}(-1)^{|A|-|U|}[g_t(U)+g_u(U)]=I_{g_t}(A)+I_{g_u}(A).'),step('linearity-empty','空集与例子',r'A空集时结论就是三个输出基线满足 $b_v=b_t+b_u$，不需要任何一个为零。例如两个常数模型2与5相加得7；空集交互7，非空交互都为0。')]
sid=add_shared('shared-harsanyi-linearity','共享证明：交互的线性性',r'I_{g+h}(A)=I_g(A)+I_h(A)',LINEAR_STEPS,['Harsanyi.interaction_add'])
add('cvpr2023-linearity','Linearity：逐点相加的交互相加','Axiom (2)',['cvpr-inv-linearity'],r'[\forall U\subseteq N,\;g_v(U)=g_t(U)+g_u(U)]\Rightarrow\forall A\subseteq N,\;I_{g_v}(A)=I_{g_t}(A)+I_{g_u}(A)',LINEAR_ORIG,LINEAR_PROOF,LINEAR_STEPS,[sid],['cvpr-issue-linearity-index'],['Harsanyi.interaction_add','FullCvpr.linearity'],kind='axiom_property',source_refs=[ref('supp',[2,4],'B(2); D.1(2)')])

DUMMY_ORIG=r'''补充第2、4页(3)：若 $i\in N$ 且 $\forall S\subseteq N\setminus\{i\},\ v(x_{S\cup\{i\}})=v(x_S)+v(x_{\{i\}})$，则 $\forall S\subseteq N\setminus\{i\},\ w_{S\cup\{i\}}=0$。'''
DUMMY_PROOF=r'''第4页原完整推导：
\[
\begin{aligned}w_{S\cup\{i\}}&=\sum_{U\subseteq S\cup\{i\}}(-1)^{|S|+1-|U|}v(x_U)\\
&=\sum_{U\subseteq S}(-1)^{|S|+1-|U|}v(x_U)+\sum_{U\subseteq S}(-1)^{|S|-|U|}v(x_{U\cup\{i\}})\\
&=\sum_{U\subseteq S}(-1)^{|S|+1-|U|}v(x_U)+\sum_{U\subseteq S}(-1)^{|S|-|U|}[v(x_S)+v(x_{\{i\}})]\\
&=\left[\sum_{U\subseteq S}(-1)^{|S|-|U|}\right]v(x_{\{i\}})=0.\end{aligned}
\]
原第三行同样出现固定下标S；最后“=0”在S空集时错误。原命题错误，项目不发布补条件版作为替代。'''
add('cvpr2023-dummy','Dummy：原命题空集反例（不修改）','Axiom (3)',['cvpr-inv-dummy'],r'[\forall S\subseteq N\setminus\{i\},\;g(S\cup\{i\})=g(S)+g(\{i\})]\Rightarrow\forall S\subseteq N\setminus\{i\},\;I_g(S\cup\{i\})=0',DUMMY_ORIG,DUMMY_PROOF,[step('dummy-counterexample','原量词下的完整反例',r'取 $N=\{i\},g(\varnothing)=0,g(\{i\})=1$。只有 $S=\varnothing$，前提为 $1=0+1$，结论为 $I_g(\{i\})=0$。实际交互按定义为 $1-0=1$，因此原命题不成立。这里不增加“非空S”条件，也不把库的无效变量版本interaction_dummy当作原论文Dummy。')],issues=['cvpr-issue-dummy-empty'],lean_names=['FullCvpr.dummy_statement_counterexample'],kind='axiom_property',status='blocked_by_source_issue',source_refs=[ref('supp',[2,4],'B(3); D.1(3)')])

SYMM_ORIG=r'''补充第2、4页(4)：若 $i,j\in N$ 且对全部 $U\subseteq N\setminus\{i,j\}$ 有 $v(x_{U\cup\{i\}})=v(x_{U\cup\{j\}})$，则同一范围全部S满足 $w_{S\cup\{i\}}=w_{S\cup\{j\}}$。'''
SYMM_PROOF=r'''补充第4页末至第5页首完整计算：
\[
\begin{aligned}w_{S\cup\{i\}}&=\sum_{U\subseteq S\cup\{i\}}(-1)^{|S|+1-|U|}v(x_U)\\
&=\sum_{U\subseteq S}(-1)^{|S|+1-|U|}v(x_U)+\sum_{U\subseteq S}(-1)^{|S|-|U|}v(x_{U\cup\{i\}})\\
&=\sum_{U\subseteq S}(-1)^{|S|+1-|U|}v(x_U)+\sum_{U\subseteq S}(-1)^{|S|-|U|}v(x_{U\cup\{j\}})\\
&=\sum_{U\subseteq S\cup\{j\}}(-1)^{|S|+1-|U|}v(x_U)=w_{S\cup\{j\}}.\end{aligned}
\]'''
SYMM_STEPS=[step('symm-split','把含i的子集按是否含i分组',r'i不在S。$S\cup\{i\}$ 的子集唯一写为U或 $U\cup\{i\}$，其中U子集S。后一类基数比U加一，其符号指数因此少一。原合作前提适用于每个U，因为U不含i,j。',r'w_{S\cup\{i\}}=\sum_{U\subseteq S}(-1)^{|S|-|U|}\big[g(U\cup\{i\})-g(U)\big].'),step('symm-substitute','逐项替换相同的合作输出',r'每个括号的第一项可以换成 $g(U\cup\{j\})$；第二项不变。重新按含j/不含j的子集配对，得到 $w_{S\cup\{j\}}$。i=j时结论也成立，证明没有要求二者不同。'),step('symm-empty','空集边界与例子',r'S空集时只需原前提给出的 $g(\{i\})=g(\{j\})$，共同减去g空即可。例 $g(\varnothing)=7,g(i)=g(j)=8,g(ij)=12$，两单变量交互都为1，二阶交互为3。')]
sid=add_shared('shared-harsanyi-symmetry','共享证明：交互对称性',r'I_g(S\cup\{i\})=I_g(S\cup\{j\})',SYMM_STEPS,['Harsanyi.interaction_symmetry'])
add('cvpr2023-symmetry','Symmetry：相同合作输出具有相同交互','Axiom (4)',['cvpr-inv-symmetry'],r'\forall S\subseteq N\setminus\{i,j\},\;I_g(S\cup\{i\})=I_g(S\cup\{j\})',SYMM_ORIG,SYMM_PROOF,SYMM_STEPS,[sid],lean_names=['Harsanyi.interaction_symmetry','FullCvpr.symmetry'],kind='axiom_property',source_refs=[ref('supp',[2,4,5],'B(4); D.1(4)')],assumptions=[r'$i,j\in N$；对全部 $U\subseteq N\setminus\{i,j\}$，$g(U\cup\{i\})=g(U\cup\{j\})$。'])

ANON_ORIG=r'''补充第2、5页(5)：对N的任意置换 $\pi$，记 $\pi S=\{\pi(i):i\in S\}$；新模型满足 $(\pi v)(x_{\pi S})=v(x_S)$。则 $w^v_S=w^{\pi v}_{\pi S}$。'''
ANON_PROOF=r'''第5页完整计算：
\[
w^{\pi v}_{\pi S}=\sum_{U\subseteq S}(-1)^{|S|-|U|}(\pi v)(x_{\pi U})
=\sum_{U\subseteq S}(-1)^{|S|-|U|}v(x_U)=w^v_S.
\]'''
ANON_STEPS=[step('anon-bijection','明确新集合函数和子集对应',r'定义 $g^\pi(V)=g(\pi^{-1}V)$。因pi为双射，映射 $U\mapsto\pi U$ 是S的子集与piS的子集之间的一一对应，并保持基数。'),step('anon-reindex','按此双射重编号求和',r'新交互的每个项对应原U，指数 $|\pi S|-|\pi U|=|S|-|U|$，输出 $g^\pi(\pi U)=g(U)$。所有项逐一相等，故总和相等。',r'I_{g^\pi}(\pi S)=\sum_{U\subseteq S}(-1)^{|S|-|U|}g(U)=I_g(S).'),step('anon-empty','空集与例子',r'pi空集还是空集，输出基线不变；交换两个变量时上述7,8,9,13例的单变量1与2交换位置，空集7和二阶3保留。')]
sid=add_shared('shared-harsanyi-anonymity','共享证明：置换不变性',r'I_{g^\pi}(\pi S)=I_g(S)',ANON_STEPS,['Harsanyi.interaction_relabel'])
add('cvpr2023-anonymity','Anonymity：重命名变量保持交互','Axiom (5)',['cvpr-inv-anonymity'],r'I_{g^\pi}(\pi S)=I_g(S)',ANON_ORIG,ANON_PROOF,ANON_STEPS,[sid],lean_names=['Harsanyi.interaction_relabel','FullCvpr.anonymity'],kind='axiom_property',source_refs=[ref('supp',[2,5],'B(5); D.1(5)')],assumptions=[r'$\pi:N\to N$是双射；$g^\pi(V)=g(\pi^{-1}V)$。'])

REC_ORIG=r'''补充第2、5页(6)：$i\in N$、$S\subseteq N\setminus\{i\}$。令 $w_{S\mid i\ present}=\sum_{U\subseteq S}(-1)^{|S|-|U|}v(x_{U\cup\{i\}})$，则 $w_{S\cup\{i\}}=w_{S\mid i\ present}-w_S$。'''
REC_PROOF=r'''第5页完整计算：
\[
\begin{aligned}w_{S\cup\{i\}}&=\sum_{U\subseteq S\cup\{i\}}(-1)^{|S|+1-|U|}v(x_U)\\
&=\sum_{U\subseteq S}(-1)^{|S|+1-|U|}v(x_U)+\sum_{U\subseteq S}(-1)^{|S|-|U|}v(x_{U\cup\{i\}})\\
&=\sum_{U\subseteq S}(-1)^{|S|-|U|}v(x_{U\cup\{i\}})-\sum_{U\subseteq S}(-1)^{|S|-|U|}v(x_U)\\
&=w_{S\mid i\ present}-w_S.\end{aligned}
\]'''
REC_STEPS=[step('rec-context','定义始终保留i的上下文函数',r'令 $g_i(U)=g(U\cup\{i\})$；这改变了掩码环境，却不改变原模型。$w_{S\mid i\ present}=I_{g_i}(S)$，它的空集值是g(i)，不是g空。'),step('rec-pair','配对子集并检查符号',r'S不含i。含i子集 $U\cup\{i\}$ 的指数为 $|S|+1-(|U|+1)=|S|-|U|$；不含i的U多一个负号。两族合并成 $g_i(U)-g(U)$，再按线性性拆开。',r'I_g(S\cup\{i\})=I_{g_i-g}(S)=I_{g_i}(S)-I_g(S).'),step('rec-empty','空集与具体数值',r'S空集给 $w_i=g(i)-g空$，无需强制单变量交互为0。7,8,9,13例中S={2},i=1时，上下文交互13−8=5，原交互9−7=2，相减得二阶3。')]
sid=add_shared('shared-harsanyi-recursive','共享证明：插入变量的上下文差分',r'I_g(S\cup\{i\})=I_{g_i}(S)-I_g(S)',REC_STEPS,['Harsanyi.interaction_context_difference'])
add('cvpr2023-recursive','Recursive：始终保留变量的上下文差分','Axiom (6)',['cvpr-inv-recursive'],r'I_g(S\cup\{i\})=I_{g_i}(S)-I_g(S)',REC_ORIG,REC_PROOF,REC_STEPS,[sid],lean_names=['Harsanyi.interaction_context_difference','FullCvpr.recursive'],kind='axiom_property',source_refs=[ref('supp',[2,5],'B(6); D.1(6)')],assumptions=[r'$i\in N$，$S\subseteq N\setminus\{i\}$。'])

DIST_ORIG=r'''补充第2、5页(7)：对T子集N及实常数c，$v_T(x_S)=c$ 若 $T\subseteq S$，否则为0。则 $w_T=c$，且全部 $S\ne T$ 有 $w_S=0$。'''
DIST_PROOF=r'''第5–6页原完整三case证明：
\[
S\subsetneq T:\quad w_S=\sum_{U\subseteq S}(-1)^{|S|-|U|}\underbrace{v(x_U)}_{U\subseteq S\subsetneq T\Rightarrow v(x_U)=0}=0.
\]
\[
S=T:\quad w_S=w_T=\sum_{U\subseteq T}(-1)^{|T|-|U|}v(x_U)
=v(T)+\sum_{U\subsetneq T}(-1)^{|T|-|U|}\underbrace{v(x_U)}_{=0}=c.
\]
\[
S\supsetneq T:\quad w_S=c\sum_{\substack{U\subseteq S\\U\supseteq T}}(-1)^{|S|-|U|}
=c\sum_{m=0}^{|S|-|T|}\binom{|S|-|T|}{m}(-1)^m=0.
\]
原文没有写S,T不可比的case。第二式原 $v(T)$ 是模型/集合函数混记，转录保留；项目统一为g(T)。'''
DIST_STEPS=[step('dist-outside','T不包含于S的所有情形',r'若 $T\not\subseteq S$，任意 $U\subseteq S$ 都不可能包含T，所以所有输出u_T(U)=0。这个case同时覆盖原文的S真子集T与不可比集合，保持原结论不变。'),step('dist-equal','S等于T',r'只有U=T这一项为c，符号为1；其余真子集项全零。若T空集，同样只有空集项c。'),step('dist-superset','T真子集S的消去',r'剩下U包含T。令 $B=U\setminus T\subseteq S\setminus T$，这是双射；指数为 $|S\setminus T|-|B|$。取该非空差集中的一个变量，把含它/不含它的B配对，符号相反，全部消去。',r'I_{u_T}(S)=\begin{cases}c&S=T,\\0&S\ne T.\end{cases}'),step('dist-example','空集与不可比例子',r'若T空集，u_T为常数c，只空集交互c。若N={1,2},T={1},c=3，则g空0,g1=3,g2=0,g12=3；交互分别0,3,0,0，原文漏写的S={2}也有严格理由为0。')]
sid=add_shared('shared-harsanyi-interaction-distribution','共享证明：纯AND函数的唯一交互',r'I_{u_T}(S)=\mathbf1_{S=T}c',DIST_STEPS,['Harsanyi.interaction_unanimity'])
add('cvpr2023-interaction-distribution','Interaction distribution：纯AND只在指定集合有交互','Axiom (7)',['cvpr-inv-distribution'],r'I_{u_T}(S)=\begin{cases}c&S=T,\\0&S\ne T,\end{cases}\qquad u_T(S)=c\,\mathbf1_{T\subseteq S}',DIST_ORIG,DIST_PROOF,DIST_STEPS,[sid],['cvpr-issue-distribution-incomparable'],['Harsanyi.interaction_unanimity','FullCvpr.interaction_distribution'],kind='axiom_property',source_refs=[ref('supp',[2,5,6],'B(7); D.1(7)')],assumptions=[r'$T\subseteq N$；$c\in\mathbb R$；允许T空集。'])

MARG_ORIG=r'''补充第2、6页Theorem 5：$T\subseteq N\setminus S$，定义 $\Delta v_T(x_S)=\sum_{L\subseteq T}(-1)^{|T|-|L|}v(x_{L\cup S})$，则 $\Delta v_T(x_S)=\sum_{U\subseteq S}w_{T\cup U}$。第6页另给 $T=\{i\}$ 的特例 $\Delta v_{\{i\}}(x_S)=\sum_{L\subseteq S}w_{L\cup\{i\}}$，并引用[40]。'''
MARG_PROOF=r'''第6页作者全部计算如下（用L′等哑变量；末两行作者按大小l计数时，符号指数仍印作|L|，这里保留说明）：
\[
\begin{aligned}\Delta v_T(x_S)&=\sum_{L\subseteq T}(-1)^{|T|-|L|}v(x_{L\cup S})\\
&=\sum_{L\subseteq T}(-1)^{|T|-|L|}\sum_{K\subseteq L\cup S}w_K\\
&=\sum_{L\subseteq T}(-1)^{|T|-|L|}\sum_{L'\subseteq L}\sum_{S'\subseteq S}w_{L'\cup S'}\\
&=\sum_{S'\subseteq S}\left[\sum_{L\subseteq T}(-1)^{|T|-|L|}\sum_{L'\subseteq L}w_{L'\cup S'}\right]\\
&=\sum_{S'\subseteq S}\left[\sum_{L'\subseteq T}\sum_{L'\subseteq L\subseteq T}(-1)^{|T|-|L|}w_{L'\cup S'}\right]\\
&=\sum_{S'\subseteq S}\left[w_{T\cup S'}+\sum_{L'\subsetneq T}\sum_{l=|L'|}^{|T|}\binom{|T|-|L'|}{l-|L'|}(-1)^{|T|-|L|}w_{L'\cup S'}\right]\\
&=\sum_{S'\subseteq S}\left[w_{T\cup S'}+\sum_{L'\subsetneq T}w_{L'\cup S'}\underbrace{\sum_{l=|L'|}^{|T|}\binom{|T|-|L'|}{l-|L'|}(-1)^{|T|-|L|}}_{=0}\right]\\
&=\sum_{S'\subseteq S}w_{T\cup S'}.
\end{aligned}
\]
第三行用L与S不相交；第二行用Theorem1。'''
MARG_STEPS=[step('marg-expand','在每个掩码输出上使用已证重构',r'固定环境S与差分变量T，要求T∩S空。对每个L子集T重构g(L∪S)。每个K子集L∪S唯一写为A∪U，其中A=K∩L子集L、U=K∩S子集S；无重复计数，因两总体不相交。'),step('marg-cancel','固定环境子集，交换有限求和并配对',r'按U再按A分组。固定A子集T，外层L可唯一写为A∪B，B子集T\A；符号为 $(-1)^{|T|-|A|-|B|}$。若A≠T，取差集一个变量，把B配对消去；若A=T只有B空集，系数1。每个U只留下w(T∪U)。',r'\Delta_Tg(S)=\sum_{U\subseteq S}\sum_{A\subseteq T}w_{A\cup U}\sum_{A\subseteq L\subseteq T}(-1)^{|T|-|L|}=\sum_{U\subseteq S}w_{T\cup U}.'),step('marg-empty','空集与具体差分',r'T空集时左为g(S)，右为重构和；S空集时左就是w(T)，右唯一项w(T)。在7,8,9,13例中T={1},S={2}，差分13−9=4，右侧w1+w12=1+3=4；S空时8−7=1。')]
sid=add_shared('shared-harsanyi-marginal-decomposition','共享证明：环境边际差分的交互分解',r'\Delta_Tg(S)=\sum_{U\subseteq S}I_g(T\cup U)',MARG_STEPS,['Harsanyi.higherMarginal_eq_sum_interaction'])
add('cvpr2023-marginal-decomposition','Theorem 5：环境中的高阶边际分解','Theorem 5',['cvpr-inv-thm5'],r'T\cap S=\varnothing\ \Longrightarrow\ \Delta_Tg(S)=\sum_{U\subseteq S}I_g(T\cup U)',MARG_ORIG,MARG_PROOF,MARG_STEPS,[sid],lean_names=['Harsanyi.higherMarginal_eq_sum_interaction','FullCvpr.marginal_decomposition'],source_refs=[ref('supp',[2,6],'B; D.2 Theorem5')],assumptions=[r'$T,S\subseteq N$ 且 $T\cap S=\varnothing$；允许任一为空集。'])

FACTORIAL_STEPS=[step('factorial-lemma','完整辅助引理：有限阶乘卷积',r'对任意有限R、非负整数a,b，记m=|R|，$F_R(a,b)=\sum_{A\subseteq R}(a+|A|)!(b+m-|A|)!$。证明下式时，对R插入归纳，归纳假设必须同时对全部a,b成立。R空时左a!b!，右同值。插入一个新变量i后，按A是否含i分组得到 $F_{R\cup\{i\}}(a,b)=F_R(a,b+1)+F_R(a+1,b)$。两项由归纳假设有相同分母(a+b+2)!和相同大阶乘(a+b+m+2)!。小阶乘部分为 $a!(b+1)!+(a+1)!b!=a!b!(a+b+2)$。约去(a+b+2)即得插入后的公式；所有阶乘都正，除法合法。此论证覆盖a=0、b=0、m=0，不使用Beta。',r'F_R(a,b)=\frac{a!b!(a+b+m+1)!}{(a+b+1)!}.'),step('factorial-coefficient','完整辅助引理：包含固定子集的权重和',r'取正整数k、有限M、L子集M，m=|M|、l=|L|、R=M\L。每个包含L的S唯一写为L∪A，A子集R，且|S|=l+|A|、|R|=m−l。将上引理用于a=l、b=k−1，得到下式；$k(k-1)!=k!$，大阶乘(m+k)!可约去。这包括L空、L=M。',r'\sum_{L\subseteq S\subseteq M}\frac{k\,|S|!(m+k-|S|-1)!}{(m+k)!}=\frac{l!k!}{(l+k)!}=\binom{l+k}{k}^{-1}.'),step('factorial-transform','交换有限求和，得到一般加权差分恒等式',r'若T与M不相交，用边际分解 $\Delta_Tg(S)=\sum_{U\subseteq S}w_{T\cup U}$。有限双和对每对U子集S子集M重新排序。固定U的权重和是上一个辅助引理，故全部U得到其精确系数。',r'\sum_{S\subseteq M}\frac{k\,|S|!(m+k-|S|-1)!}{(m+k)!}\Delta_Tg(S)=\sum_{U\subseteq M}\binom{|U|+k}{k}^{-1}w_{T\cup U}.')]
add_shared('shared-harsanyi-factorial-convolution','共享辅助证明：包含全部空集边界的有限阶乘恒等式',r'\sum_{S\subseteq M}\frac{k\,|S|!(m+k-|S|-1)!}{(m+k)!}\Delta_Tg(S)=\sum_{U\subseteq M}\binom{|U|+k}{k}^{-1}I_g(T\cup U)',FACTORIAL_STEPS,['Harsanyi.factorial_powerset_sum','Harsanyi.factorialWeight_superset_sum','Harsanyi.weighted_higherMarginal_eq'])

SHAPLEY_ORIG=r'''正文第4页Theorem2（标明由[15]证明），补充第2、6页Theorem2：输入变量i的Shapley值为 $\phi(i)=\sum_{S\subseteq N\setminus\{i\}}\frac1{|S|+1}w_{S\cup\{i\}}$。作者解释为一个m变量模式的效应均分给这m个变量。'''
SHAPLEY_PROOF=r'''补充第6页末至第8页Theorem3之前，作者完整数学推导：设n=|N|，l=|L|。
\[
\begin{aligned}\phi(i)&=\sum_{S\subseteq N\setminus\{i\}}\frac{|S|!(n-|S|-1)!}{n!}\Delta v_{\{i\}}(x_S)\\
&=\frac1n\sum_{m=0}^{n-1}\binom{n-1}{m}^{-1}\sum_{\substack{S\subseteq N\setminus\{i\}\\|S|=m}}\Delta v_{\{i\}}(x_S)\\
&=\frac1n\sum_{m=0}^{n-1}\binom{n-1}{m}^{-1}\sum_{\substack{S\subseteq N\setminus\{i\}\\|S|=m}}\sum_{L\subseteq S}w_{L\cup\{i\}}\\
&=\frac1n\sum_{L\subseteq N\setminus\{i\}}\sum_{m=0}^{n-1}\binom{n-1}{m}^{-1}\sum_{\substack{L\subseteq S\subseteq N\setminus\{i\}\\|S|=m}}w_{L\cup\{i\}}\\
&=\frac1n\sum_{L\subseteq N\setminus\{i\}}\sum_{m=l}^{n-1}\binom{n-1}{m}^{-1}\sum_{\substack{L\subseteq S\subseteq N\setminus\{i\}\\|S|=m}}w_{L\cup\{i\}}\\
&=\frac1n\sum_L\sum_{m=l}^{n-1}\binom{n-1}{m}^{-1}\binom{n-l-1}{m-l}w_{L\cup\{i\}}\\
&=\frac1n\sum_L w_{L\cup\{i\}}\underbrace{\sum_{r=0}^{n-l-1}\binom{n-1}{l+r}^{-1}\binom{n-l-1}{r}}_{\alpha_L}.
\end{aligned}
\]
第7页文字把待简化项称为“term $w_L$”，紧接公式/后文使用 $\alpha_L$。作者列出三项材料：(i) $m\binom nm=n\binom{n-1}{m-1}$；(ii) 对p,q>0写 $B(p,q)=\int_0^1x^{p-1}(1-x)^{1-q}dx$（原指数错误保留）；(iii) 正整数p,q有 $B(p,q)=[q\binom{p+q-1}{p-1}]^{-1}$，及正整数n>m有 $\binom nm=[mB(n-m+1,m)]^{-1}$。
\[
\begin{aligned}\alpha_L&=\sum_{r=0}^{n-l-1}\binom{n-l-1}{r}(l+r)B(n-l-r,l+r)\\
&=\underbrace{\sum_{r=0}^{n-l-1}l\binom{n-l-1}{r}B(n-l-r,l+r)}_{\text{①}}
+\underbrace{\sum_{r=0}^{n-l-1}r\binom{n-l-1}{r}B(n-l-r,l+r)}_{\text{②}}.
\end{aligned}
\]
\[
\begin{aligned}\text{①}&=\int_0^1l\sum_{r=0}^{n-l-1}\binom{n-l-1}{r}x^{n-l-r-1}(1-x)^{l+r-1}dx\\
&=\int_0^1l\underbrace{\sum_{r=0}^{n-l-1}\binom{n-l-1}{r}x^{n-l-r-1}(1-x)^r}_{=1}(1-x)^{l-1}dx
=\int_0^1l(1-x)^{l-1}dx=1.
\end{aligned}
\]
\[
\begin{aligned}\text{②}&=\sum_{r=1}^{n-l-1}(n-l-1)\binom{n-l-2}{r-1}B(n-l-r,l+r)\\
&=(n-l-1)\sum_{r'=0}^{n-l-2}\binom{n-l-2}{r'}B(n-l-r'-1,l+r'+1)\\
&=(n-l-1)\int_0^1\sum_{r'=0}^{n-l-2}\binom{n-l-2}{r'}x^{n-l-r'-2}(1-x)^{l+r'}dx\\
&=(n-l-1)\int_0^1\underbrace{\sum_{r'=0}^{n-l-2}\binom{n-l-2}{r'}x^{n-l-r'-2}(1-x)^{r'}}_{=1}(1-x)^l dx\\
&=(n-l-1)\int_0^1(1-x)^l dx=\frac{n-l-1}{l+1}.
\end{aligned}
\]
因此作者写 $\alpha_L=1+(n-l-1)/(l+1)=n/(l+1)$，再得 $\phi(i)=\frac1n\sum_L\alpha_L w_{L\cup\{i\}}=\sum_L\frac1{l+1}w_{L\cup\{i\}}$。错误Beta定义、l=0零参数和①边界见统一issue；最后结论在项目中用不同但完整的有限证明保留。'''
SHAPLEY_STEPS=[step('shapley-definition','从经典阶乘权重定义开始',r'对i在N，n≥1。Shapley的定义是对所有S子集N\{i}以 $|S|!(n-|S|-1)!/n!$ 加权 $g(S\cup\{i\})-g(S)$。它等于 $\Delta_{\{i\}}g(S)$。项目没有把等分式当作定义来绕过等价性。',r'\phi_g(i)=\sum_{S\subseteq N\setminus\{i\}}\frac{|S|!(n-|S|-1)!}{n!}\Delta_{\{i\}}g(S).')]+FACTORIAL_STEPS+[step('shapley-specialize','逐项检查共有引理的参数',r'在共有加权差分定理取T={i}、M=N\{i}、k=1，所以m=n−1，权重恰是经典阶乘权重。右侧系数 $\binom{|U|+1}{1}^{-1}=1/(|U|+1)$，得原结论。所用不相交、正阶数、有限集合前提均满足。',r'\phi_g(i)=\sum_{U\subseteq N\setminus\{i\}}\frac{I_g(U\cup\{i\})}{|U|+1}.'),step('shapley-empty-example','空集输出基线与二变量例子',r'求和允许U空集，但交互是{i}，不是空集交互。b不被分配给变量。在7,8,9,13例中，phi1=1+3/2=2.5，phi2=2+3/2=3.5，总和6=g(N)−b。若N仅{i}，唯一环境为空，phi=g(i)−b，公式仍成立。')]
sid=add_shared('shared-harsanyi-shapley-dividend','共享证明：经典Shapley等于交互均分',r'\phi_g(i)=\sum_{U\subseteq N\setminus\{i\}}\frac{I_g(U\cup\{i\})}{|U|+1}',SHAPLEY_STEPS,['Harsanyi.factorialShapley_eq_dividends'])
add('cvpr2023-shapley','Theorem 2：经典Shapley的交互均分','Theorem 2',['cvpr-inv-thm2'],r'\phi_g(i)=\sum_{U\subseteq N\setminus\{i\}}\frac{I_g(U\cup\{i\})}{|U|+1}',SHAPLEY_ORIG,SHAPLEY_PROOF,SHAPLEY_STEPS,[sid,'shared-harsanyi-factorial-convolution'],['cvpr-issue-beta-proof'],['Harsanyi.factorialShapley_eq_dividends','FullCvpr.shapley'],source_refs=[ref('main',[4],'3.1'),ref('supp',[2,6,7,8],'B; D.2 Theorem2')],assumptions=[r'$i\in N$；Shapley使用经典阶乘权重边际定义。'])

SII_ORIG=r'''补充第2、8页Theorem3：$T\subseteq N$，$I^{\rm Shapley}(T)=\sum_{S\subseteq N\setminus T}\frac{|S|!(|N|-|S|-|T|)!}{(|N|-|T|+1)!}\Delta v_T(x_S)$，则 $I^{\rm Shapley}(T)=\sum_{S\subseteq N\setminus T}\frac1{|S|+1}w_{S\cup T}$；把T作为单个组成变量解释其均匀分配。'''
SII_PROOF=r'''补充第8页Theorem3至第9页Theorem4之前的全部推导。令n=|N|、t=|T|、l=|L|、M=n−t。
\[
\begin{aligned}I^{\rm Shapley}(T)&=\sum_{S\subseteq N\setminus T}\frac{|S|!(n-|S|-t)!}{(n-t+1)!}\Delta v_T(x_S)\\
&=\frac1{M+1}\sum_{m=0}^{M}\binom M m^{-1}\sum_{\substack{S\subseteq N\setminus T\\|S|=m}}\Delta v_T(x_S)\\
&=\frac1{M+1}\sum_{m=0}^{M}\binom M m^{-1}\sum_{\substack{S\subseteq N\setminus T\\|S|=m}}\sum_{L\subseteq S}w_{L\cup T}\\
&=\frac1{M+1}\sum_{L\subseteq N\setminus T}\sum_{m=l}^{M}\binom M m^{-1}\sum_{\substack{L\subseteq S\subseteq N\setminus T\\|S|=m}}w_{L\cup T}\\
&=\frac1{M+1}\sum_L\sum_{m=l}^{M}\binom M m^{-1}\binom{M-l}{m-l}w_{L\cup T}\\
&=\frac1{M+1}\sum_Lw_{L\cup T}\underbrace{\sum_{r=0}^{M-l}\binom M{l+r}^{-1}\binom{M-l}{r}}_{\alpha_L}.
\end{aligned}
\]
作者复用Theorem2的组合数/Beta材料：
\[
\begin{aligned}\alpha_L&=\sum_{r=0}^{M-l}\binom{M-l}r(l+r)B(M-l-r+1,l+r)\\
&=\underbrace{\sum_{r=0}^{M-l}l\binom{M-l}rB(M-l-r+1,l+r)}_{\text{①}}
+\underbrace{\sum_{r=0}^{M-l}r\binom{M-l}rB(M-l-r+1,l+r)}_{\text{②}}.
\end{aligned}
\]
\[
\begin{aligned}\text{①}&=\int_0^1l\sum_{r=0}^{M-l}\binom{M-l}r x^{M-l-r}(1-x)^{l+r-1}dx\\
&=\int_0^1l\underbrace{\sum_{r=0}^{M-l}\binom{M-l}r x^{M-l-r}(1-x)^r}_{=1}(1-x)^{l-1}dx
=\int_0^1l(1-x)^{l-1}dx=1,\\
\text{②}&=\sum_{r=1}^{M-l}(M-l)\binom{M-l-1}{r-1}B(M-l-r+1,l+r)\\
&=(M-l)\sum_{r'=0}^{M-l-1}\binom{M-l-1}{r'}B(M-l-r',l+r'+1)\\
&=(M-l)\int_0^1\sum_{r'=0}^{M-l-1}\binom{M-l-1}{r'}x^{M-l-r'-1}(1-x)^{l+r'}dx\\
&=(M-l)\int_0^1\underbrace{\sum_{r'=0}^{M-l-1}\binom{M-l-1}{r'}x^{M-l-r'-1}(1-x)^{r'}}_{=1}(1-x)^l dx\\
&=(M-l)\int_0^1(1-x)^l dx=\frac{M-l}{l+1}.
\end{aligned}
\]
于是原证明得 $\alpha_L=1+(M-l)/(l+1)=(M+1)/(l+1)$，$I^{\rm Shapley}(T)=\frac1{M+1}\sum_L\alpha_Lw_{L\cup T}=\sum_Lw_{L\cup T}/(l+1)$。l=0时原①不成立；完整修正证明不改T的量词。'''
SII_STEPS=[step('sii-definition','保留原阶乘定义与总体外部集合',r'设t=|T|、m=n−t，外部变量M=N\T恰有m个。原权重为 $|S|!(m-|S|)!/(m+1)!$，不是把T中t个变量分别当玩家。原量词T子集N包括T空与T=N。')]+FACTORIAL_STEPS+[step('sii-specialize','取共有加权差分定理的k=1',r'T与M不相交，取共有定理k=1。左侧权重与原定义逐项相同，右侧系数为1/(|U|+1)，得原结论。T=N时M空，唯一环境空集，输出交互wN；T空时这是空目标的加权输出平均，空交互b参与，不把它改为0。'),step('sii-example','二变量边界核对',r'7,8,9,13例中T={1,2}，SII为w12=3；T={1}恢复phi1=2.5；T空时原加权和为 $(7/3)+(8/6)+(9/6)+(13/3)=9.5$，交互形式为 $7+1/2+2/2+3/3=9.5$。')]
sid=add_shared('shared-harsanyi-shapley-interaction-dividend','共享证明：SII的精确交互权重',r'I_g^{\rm Shapley}(T)=\sum_{U\subseteq N\setminus T}\frac{I_g(T\cup U)}{|U|+1}',SII_STEPS,['Harsanyi.factorialShapleyInteraction_eq_dividends'])
add('cvpr2023-shapley-interaction','Theorem 3：Shapley interaction 的交互权重','Theorem 3',['cvpr-inv-thm3'],r'I_g^{\rm Shapley}(T)=\sum_{U\subseteq N\setminus T}\frac{I_g(T\cup U)}{|U|+1}',SII_ORIG,SII_PROOF,SII_STEPS,[sid,'shared-harsanyi-factorial-convolution'],['cvpr-issue-beta-proof'],['Harsanyi.factorialShapleyInteraction_eq_dividends','FullCvpr.shapley_interaction'],source_refs=[ref('supp',[2,8,9],'B; D.2 Theorem3')],assumptions=[r'$T\subseteq N$；SII采用原阶乘权重定义。'])

STI_ORIG=r'''补充第2、9页Theorem4：对正阶数k，k阶Shapley–Taylor指数满足：$|T|<k$ 时等于wT；$|T|=k$ 时等于 $\sum_{S\subseteq N\setminus T}\binom{|S|+k}{k}^{-1}w_{S\cup T}$；$|T|>k$ 时为0。正阶数的域来自k-th order及其引用的定义，项目显式记录，不假定n≥k（当k>n只用第一分支）。'''
STI_PROOF=r'''补充第9页末至第11页E之前的完整作者证明。原定义为
\[
I^{\rm Shapley\text{-}Taylor(k)}(T)=\begin{cases}
\Delta v_T(x_\varnothing),&|T|<k,\\
\frac{k}{n}\sum_{S\subseteq N\setminus T}\binom{n-1}{|S|}^{-1}\Delta v_T(x_S),&|T|=k,\\0,&|T|>k.
\end{cases}
\]
低阶分支直接按Harsanyi定义给 $\Delta v_T(x_\varnothing)=\sum_{L\subseteq T}(-1)^{|T|-|L|}v(x_L)=w_T$。最高阶分支，n=|N|、l=|L|，作者计算
\[
\begin{aligned}I^{\rm ST(k)}(T)&=\frac{k}{n}\sum_{S\subseteq N\setminus T}\binom{n-1}{|S|}^{-1}\Delta v_T(x_S)\\
&=\frac{k}{n}\sum_{m=0}^{n-k}\sum_{\substack{S\subseteq N\setminus T\\|S|=m}}\binom{n-1}{|S|}^{-1}\Delta v_T(x_S)\\
&=\frac{k}{n}\sum_{m=0}^{n-k}\sum_{\substack{S\subseteq N\setminus T\\|S|=m}}\binom{n-1}{|S|}^{-1}\sum_{L\subseteq S}w_{L\cup T}\\
&=\frac{k}{n}\sum_L\sum_{m=l}^{n-k}\binom{n-1}{|S|}^{-1}\sum_{\substack{L\subseteq S\subseteq N\setminus T\\|S|=m}}w_{L\cup T}\\
&=\frac{k}{n}\sum_L\sum_{m=l}^{n-k}\binom{n-1}{|S|}^{-1}\binom{n-l-k}{m-l}w_{L\cup T}\\
&=\frac{k}{n}\sum_Lw_{L\cup T}\underbrace{\sum_{r=0}^{n-l-k}\binom{n-1}{l+r}^{-1}\binom{n-l-k}r}_{\alpha_L}.
\end{aligned}
\]
中间两行原稿在按m分组之后仍印|S|（S在内族满足|S|=m）；最后按r重新编号。
\[
\begin{aligned}\alpha_L&=\sum_{r=0}^{n-l-k}\binom{n-l-k}r(l+r)B(n-l-r,l+r)\\
&=\underbrace{\sum_{r=0}^{n-l-k}l\binom{n-l-k}r B(n-l-r,l+r)}_{\text{①}}
+\underbrace{\sum_{r=0}^{n-l-k}r\binom{n-l-k}r B(n-l-r,l+r)}_{\text{②}}.
\end{aligned}
\]
\[
\begin{aligned}\text{①}&=\int_0^1l\sum_{r=0}^{n-l-k}\binom{n-l-k}r x^{n-l-r-1}(1-x)^{l+r-1}dx\\
&=\int_0^1l\underbrace{\sum_{r=0}^{n-l-k}\binom{n-l-k}r x^{n-l-r-k}(1-x)^r}_{=1}x^{k-1}(1-x)^{l-1}dx\\
&=lB(k,l)=\binom{l+k-1}{k-1}^{-1},\\
\text{②}&=(n-l-k)\sum_{r=1}^{n-l-k}\binom{n-l-k-1}{r-1}B(n-l-r,l+r)\\
&=(n-l-k)\sum_{r'=0}^{n-l-k-1}\binom{n-l-k-1}{r'}B(n-l-r'-1,l+r'+1)\\
&=(n-l-k)\int_0^1\sum_{r'=0}^{n-l-k-1}\binom{n-l-k-1}{r'}x^{n-l-r'-2}(1-x)^{l+r'}dx\\
&=(n-l-k)\int_0^1\underbrace{\sum_{r'=0}^{n-l-k-1}\binom{n-l-k-1}{r'}x^{n-l-r'-k-1}(1-x)^{r'}}_{=1}x^{k-1}(1-x)^l dx\\
&=(n-l-k)B(k,l+1)=\frac{n-l-k}{(l+1)\binom{l+k}{k-1}}.
\end{aligned}
\]
\[
\begin{aligned}\alpha_L&=\binom{l+k-1}{k-1}^{-1}+\frac{n-l-k}{(l+1)\binom{l+k}{k-1}}\\
&=\frac{l!(k-1)!}{(l+k-1)!}+\frac{n-l-k}{l+1}\frac{(l+1)!(k-1)!}{(l+k)!}\\
&=\frac{l!(k-1)!}{(l+k-1)!}+\frac{n-l-k}{l+k}\frac{l!(k-1)!}{(l+k-1)!}\\
&=\left[1+\frac{n-l-k}{l+k}\right]\frac{l!(k-1)!}{(l+k-1)!}
=\frac n{l+k}\frac{l!(k-1)!}{(l+k-1)!}
=\frac nk\frac{l!k!}{(l+k)!}=\frac nk\binom{l+k}k^{-1}.
\end{aligned}
\]
于是作者最终写 $I^{\rm ST(k)}(T)=\frac kn\sum_L\alpha_Lw_{L\cup T}=\sum_L\binom{l+k}k^{-1}w_{L\cup T}$。高阶为0由定义。原积分域与l=0问题保留在issue中。'''
STI_STEPS=[step('sti-low','低阶和高阶分支',r'若|T|<k，环境空集的差分按定义就是wT；T空集时值为b。若|T|>k，原定义直接给0。两分支没有除n，也不需要n≥k。'),step('sti-top-weight','最高阶把原权重化为共有阶乘权重',r'若|T|=k，因k是正阶数且T子集N，有n≥k≥1，故除n合法。设M=N\T，m=n−k；每个S子集M满足s≤m≤n−1。由二项系数阶乘公式，$\frac{k}{n}\binom{n-1}s^{-1}=\frac{k\,s!(n-1-s)!}{n!}=\frac{k\,s!(m+k-1-s)!}{(m+k)!}$。没有把k或S的空集边界排除。')]+FACTORIAL_STEPS+[step('sti-top-finish','最高阶应用共有恒等式',r'T与M不相交，正k满足共有定理前提，故精确得到 $\binom{|U|+k}k^{-1}$ 权重。结合前两分支构成原三分支结论。'),step('sti-example','空集与两种阶数例子',r'7,8,9,13例中k=1：空目标值b=7，单变量目标phi1=2.5、phi2=3.5，二变量目标高于k为0。k=2：空目标7，单变量交互1和2，最高阶二变量交互3；全部四项之和13。若总体空而k≥1，只剩低阶空交互b。')]
sid=add_shared('shared-harsanyi-shapley-taylor-dividend','共享证明：STI全部三分支的交互形式',r'I_g^{\rm ST(k)}(T)=\begin{cases}I_g(T)&|T|<k,\\\sum_{U\subseteq N\setminus T}\binom{|U|+k}k^{-1}I_g(T\cup U)&|T|=k,\\0&|T|>k.\end{cases}',STI_STEPS,['Harsanyi.shapleyTaylor_eq_dividends'])
add('cvpr2023-shapley-taylor','Theorem 4：Shapley–Taylor 的全部阶数分支','Theorem 4',['cvpr-inv-thm4'],r'I_g^{\rm ST(k)}(T)=\begin{cases}I_g(T)&|T|<k,\\\sum_{U\subseteq N\setminus T}\binom{|U|+k}k^{-1}I_g(T\cup U)&|T|=k,\\0&|T|>k,\end{cases}',STI_ORIG,STI_PROOF,STI_STEPS,[sid,'shared-harsanyi-factorial-convolution'],['cvpr-issue-beta-proof'],['Harsanyi.shapleyTaylor_eq_dividends','FullCvpr.shapley_taylor'],source_refs=[ref('supp',[2,9,10,11],'B; D.2 Theorem4')],assumptions=[r'$T\subseteq N$；k为正整数阶数；采用原三分支定义。'])

SCM_ORIG=r'''正文第3页Eq.(1),(2)及第4页首：二值Xi是变量是否保留，$P(C_A=1\mid X)=\prod_{i\in A}X_i$，$Y(X)=\sum_{A\in\Omega}w_AC_A(X)$。在xS上，$Y(x_S)=\sum_{A\in\Omega}w_AC_A(x_S)=\sum_{A\subseteq S,A\in\Omega}w_A$。'''
SCM_STEPS=[step('scm-trigger','逐项核二值触发',r'对固定S，每个Xi为i在S的指示。若A子集S，全部因子1，积1；若不是，至少一个因子0，积0。A空集采用空积1，故输出基线模式始终触发。'),step('scm-sum','筛选所有激活模式',r'把逐项触发等式代入有限SCM和，每个不包含于S的模式项为0，其他项保留；不要求Omega包含全部模式。Omega=2^N时和就是重构。')]
add('cvpr2023-scm-subset-sum','SCM：二值AND触发化为子集和','Main Eq.(1),(2)',['cvpr-inv-scm'],r'Y(x_S)=\sum_{A\in\Omega,\,A\subseteq S}w_A',SCM_ORIG,SCM_ORIG,SCM_STEPS,lean_names=['FullCvpr.andTrigger_union','FullCvpr.causalOutput_full'],kind='unnumbered_derivation',source_refs=[ref('main',[3,4],'3.1')])
BASE_STEPS=[step('base-rereconstruct','每个输入基线各自重算交互',r'对任何基线r，用它定义全部xS和相应g_r，再由同一有限重构定理得到每个S上的零残差。换r后须重算g和w，论文不是声称w不变。'),step('base-unfaith','全部平方残差逐项为零',r'完整权重不删模式时，每个残差 $g_r(S)-\sum_{A\subseteq S}I_{g_r}(A)=0$，平方0，有限和0。任何两个基线各自适用；截断Omega后则不能据此声称unfaith仍零。')]
add('cvpr2023-baseline-faithfulness','改变输入基线后完整交互仍各自精确','Main 3.2 unnumbered',['cvpr-inv-baseline-invariance'],r'\forall r,\quad\sum_{S\subseteq N}\left[v(x_S^{(r)})-\sum_{A\subseteq S}I_{g_r}(A)\right]^2=0',r'正文第5页首：the change of baseline values always ensures unfaith(w)=0 and just affects ||w_Omega||_1。这里w是完整交互向量，wOmega是保留项向量。','',BASE_STEPS,['proof-finite-mobius-reconstruction-v2'],lean_names=['FullCvpr.complete_unfaithfulness_zero'],kind='unnumbered_derivation',source_refs=[ref('main',[5],'3.2')])
AOG_STEPS=[step('aog-union','两个子AND的合并等式',r'对子集合A,B及保留集合T，$A\cup B\subseteq T$ 当且仅当A和B都包含于T。因此二值AND指示满足 $C_{A\cup B}(x_T)=C_A(x_T)C_B(x_T)$。即使A,B重叠，该等式仍成立，因为指示值为0或1。'),step('aog-tree','反复合并保留全部模式状态和输出',r'按有限树的节点数归纳。叶对应单变量；每个父节点取所有子节点变量集合的并集。应用前一等式（多子节点可反复二元合并），其触发等于直接检查全部原叶变量。故每个原模式触发不变；保留相同w与最终加和，输出相同。共享beta={5,6}把{4,5,6}写成{4,beta}就是该恒等式实例，不要求模式稀疏或系数为正。'),step('aog-empty','空集与掩码例子',r'空模式空AND为1；若输入只保留4,5而遮住6，beta与原模式都不触发；若保留4,5,6，两种表达都触发。原MDL贪心是否最优是独立算法问题，此恒等式不作最优性断言。')]
add('cvpr2023-aog-regrouping','AOG：共享AND子模式的等价重组','Main 3.3 unnumbered',['cvpr-inv-aog'],r'C_{A\cup B}(x_T)=C_A(x_T)C_B(x_T)',r'正文第5页3.3：And-Sum可等价改写AOG；beta={x5,x6}，{x4,x5,x6}改为{x4,beta}；一般C_S=product_{S′ in Child(S)}C_S′。',r'作者完整论证为上述例子与一般子触发乘积规则；本篇没有独立树归纳证明。',AOG_STEPS,lean_names=['FullCvpr.andTrigger_union'],kind='unnumbered_derivation',source_refs=[ref('main',[5],'3.3')])
ADDMUL_STEPS=[step('addmul-binary','固定二值样本后的每一项',r'输入坐标xi为0或1，输入基线为0。一个多项式项 $c_A\prod_{i\in A}x_i$ 在掩码S上等于 $c_A(\prod_{i\in A}x_i)\mathbf1_{A\subseteq S}$；样本里任一xi为0使该项系数为0。空项则为常数。若多个原项有相同A，先相加其系数。'),step('addmul-transform','逐项纯AND交互再线性合并',r'每一项是纯AND函数，交互只在A非零。对有限多个项用线性性反复相加，固定集合B只收到A=B的项。不可比集合由修正后的完整纯AND证明覆盖。',r'I_g(B)=\sum_{A=B}c_A\prod_{i\in A}x_i.'),step('addmul-examples','原文两样本与边界',r'补充第14页函数3x1−2x2x3−x3x4x5+5x4x6。在全1输入，非零交互为3,−2,−1,5；若x3=0，只剩{x1}的3与{x4,x6}的5。完整输入输出分别5与8；空掩码输出0，空交互0。该精确论证不把sigmoid阈值人工标签说成精确Harsanyi系数。')]
add('cvpr2023-addmul-coefficients','二值加乘模型：交互就是激活项的系数','Main 4.1; Supplement G.3',['cvpr-inv-addmul'],r'g(S)=\sum_{A\in\mathcal P}d_A\mathbf1_{A\subseteq S}\ \Rightarrow\ I_g(B)=\begin{cases}d_B&B\in\mathcal P,\\0&B\notin\mathcal P,\end{cases}',r'正文第7页、补充第13–14页：二值乘法项只有当其全部变量存在时贡献，故每项是ground-truth模式；扩展数据集中的因果效应就是系数。',r'作者说明：xi属于{0,1}；只有一个乘法项的全部变量均为1时该项贡献；据此逐项列出13–14页两个输入样本的模式与系数。该段是解释性推导，没有完整代数证明；项目重写给出一般有限线性组合证明。',ADDMUL_STEPS,['shared-harsanyi-linearity','shared-harsanyi-interaction-distribution'],['cvpr-issue-distribution-incomparable'],['FullCvpr.addmul_interactions'],kind='unnumbered_derivation',source_refs=[ref('main',[7],'4.1'),ref('supp',[13,14],'G.3')],assumptions=[r'坐标二值，输入基线0；有限加乘多项式按相同变量集合合并；这里的零输入基线不等于一般模型输出零基线。'])

data={'schema_version':'full-paper-1.0','paper_id':PAPER,'inventory_path':str(BASE/'inventory.json'),'results':results,'shared_proofs':shared,'issues':ISSUES,'symbols':[],
  'counts':{'proof_targets':16,'results_present':len(results),'rewrite_complete':sum(x['rewrite_status']=='complete' for x in results),'statement_errors':1},
  'source_transcription_policy':'PDF authority; complete mathematical transcriptions with Chinese prose translation; display errors preserved; no project summary labelled full author proof.',
  'authorization':{'proof_fix_authorization':'proof_only_granted','statement_fix_authorization':'not_granted','user_review_status':'pending'}}
(BASE/'content.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
print(len(results),'results;',len(shared),'shared proofs; complete rewrites',data['counts']['rewrite_complete'])
