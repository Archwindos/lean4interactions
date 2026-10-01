#!/usr/bin/env python3
"""Single mathematical text input for the reader and agent package.
Only selected source-aligned results are published. Experimental OR stays excluded.
"""
from pathlib import Path
import hashlib,json,os,re
ROOT=Path(os.environ['ARCHIVE_PROJECT_ROOT'])
BASE=ROOT/'research/reader-v2-20260930'
MATH=BASE/'math'
DATA=BASE/'data'
REPORT_PATH='research/reader-v2-20260930/math/verification/report.json'
REPORT=json.loads((ROOT/REPORT_PATH).read_text())
DECL={d['name']:d for d in REPORT['declarations']}
ADAPTER_PATH='research/reader-v2-20260930/math/lean/ReaderAdapters.lean'
ADAPTER_CODE=(ROOT/ADAPTER_PATH).read_text()

def ref(name,scope='reused_exact_declaration',explanation=''):
 d=DECL[name]
 return {'declaration':name,'source_path':d['source_path'],'line':d['line'],'scope':scope,'explanation_md':explanation}
def assumption(id,text,formula=None):
 return {'id':id,'text_md':text,'formula_tex':formula}
def definition(id,text,formula):
 return {'id':id,'text_md':text,'formula_tex':formula}
def step(id,title,body,formula,justification,refs=None):
 return {'id':id,'title':title,'body_md':body,'formula_tex':formula,'justification':justification,'lean_refs':refs or []}
def lean(names,scope,alignment='agent_checked_selected_statement'):
 return {'status':'verified','label':'选定陈述已编译并通过公理审计','compiled':True,'axiom_audit':'passed','scope':scope,'alignment_status':alignment,'source_semantics_automatically_verified':False,'declarations':names,'statement':DECL[names[0]]['signature'],'source_path':ADAPTER_PATH,'report_path':REPORT_PATH,'adapter_code':ADAPTER_CODE,'source_fingerprint':REPORT['source_fingerprint'],'step_map':[],'excluded_scope':REPORT['excluded_scope']}
def attach_step_map(item):
 maps=[]
 for s in item['proof_steps']:
  for r in s['lean_refs']:
   p=ROOT/r['source_path'];lines=p.read_text().splitlines();lo=r['line']-1
   end=next((i for i in range(lo+1,len(lines)) if re.match(r'(?:@\[simp\] )?(?:noncomputable )?(?:def|theorem) |end ',lines[i])),len(lines))
   maps.append({'step_id':s['id'],'declaration':r['declaration'],'explanation':r['explanation_md'] or r['scope'],'scope':r['scope'],'source_path':r['source_path'],'line':r['line'],'lean_excerpt':'\n'.join(lines[lo:end]).strip()})
 item['lean']['step_map']=maps
 return item
SOURCES={
 'src-cvpr2023-main':('CVPR 2023 正式正文','ver-cvpr2023-formal','research/paper-survey-20260930/earlier/venue-papers/sparse-cvpr2023-main/sparse-cvpr2023-main.pdf','https://openaccess.thecvf.com/content/CVPR2023/papers/Ren_Defining_and_Quantifying_the_Emergence_of_Sparse_Concepts_in_DNNs_CVPR_2023_paper.pdf'),
 'src-cvpr2023-supplement':('CVPR 2023 正式补充材料','ver-cvpr2023-formal','research/paper-survey-20260930/earlier/venue-papers/sparse-cvpr2023-supp/sparse-cvpr2023-supp.pdf','https://openaccess.thecvf.com/content/CVPR2023/supplemental/Ren_Defining_and_Quantifying_CVPR_2023_supplemental.pdf'),
 'src-iclr2024-sparse-main':('ICLR 2024 Sparse 正式正文及随文附录','ver-iclr2024-sparse-formal','research/paper-survey-20260930/recent/pdf/iclr2024-sparse.pdf','https://proceedings.iclr.cc/paper_files/paper/2024/file/db0ee27cb50dd9087b133f6e7d28a90e-Paper-Conference.pdf'),
 'src-iclr2024-generalizable-main':('ICLR 2024 Generalizable 正式正文及随文附录','ver-iclr2024-generalizable-formal','research/paper-survey-20260930/recent/pdf/iclr2024-generalizable.pdf','https://proceedings.iclr.cc/paper_files/paper/2024/file/67a9b444cbcd647572c88194619f72d5-Paper-Conference.pdf')}
def source(id,pages,locations):
 title,version,path,url=SOURCES[id]
 location_rows=[]
 for page in pages:
  if id=='src-cvpr2023-main': label,role=('Theorem 1；Eq.(2) 与掩码 Eq.(4) 起点','statement') if page==3 else ('掩码 Eq.(4) 后的子集和解释','statement')
  elif id=='src-cvpr2023-supplement': label,role=('Appendix C Theorem 1 与唯一性重述','statement') if page==2 else ('Appendix C necessity/sufficiency 完整证明','proof')
  elif id=='src-iclr2024-sparse-main': label,role={3:('Eq.(1)：去基线定义与空集约定','statement'),4:('Theorem 1：中心化重构原陈述','statement'),15:('Appendix B.1 Eq.(7) 与完整重证','proof')}[page]
  else: label,role={2:('Eq.(1)：AND 定义与空集值','statement'),3:('Eq.(2) OR 约定；Theorem 2 Eq.(3)','statement'),12:('Appendix C Eq.(7) 及 Proof(1) 固定 x AND 子结论','statement'),13:('Appendix C(1) Eq.(8) AND 推导与 OR proof 起点','proof'),14:('Appendix C(2) OR 分类计算与 Eq.(9)','proof')}[page]
  location_rows.append({'label':label,'pdf_page':page,'role':role})
 return {'id':id,'source_id':id,'title':title,'version':version,'version_id':version,'local_path':path,'local_pdf':path,'url':url,'sha256':hashlib.sha256((ROOT/path).read_bytes()).hexdigest(),'pages':pages,'page_numbering':'PDF page, one-based','locations':location_rows,'source_checked':True}

notation={
 'paper_output':{'symbol_tex':r'v(x_S)','text_md':'论文模型在掩码输入上的实值输出；模型的自变量是输入样本，不是集合。'},
 'masked_input':{'symbol_tex':r'(x_S)_i=\begin{cases}x_i&i\in S,\\r_i&i\notin S,\end{cases}','text_md':'固定样本 x 与同一组基线 r 后，S 表示保留原值的变量；x_∅ 是全部变量置为基线后的输入。'},
 'library_function':{'symbol_tex':r'g(S)=v(x_S)','text_md':'把固定模型、样本与掩码规则组合成实值集合函数；公共库变量即使名为 v，也代表这里的 g。'},
 'baseline':{'symbol_tex':r'b=g(\varnothing)=v(x_\varnothing)','text_md':'输出基线是模型在完全掩码输入上的输出，未假设它为零。这里 b 是标量；论文的输入基线向量另记 r。'},
 'centered_function':{'symbol_tex':r'g_0(S)=g(S)-g(\varnothing)=v(x_S)-v(x_\varnothing)','text_md':'显式去除输出基线；g₀(∅)=0 来自定义，不能推成 v(x_∅)=0。'},
 'empty_set':{'symbol_tex':r'I_g(\varnothing)=g(\varnothing),\qquad I_{g_0}(\varnothing)=0','text_md':'所有子集求和均包含空集，除非明确写成非空子集。'}
}
generic_assumptions=[
 assumption('finite-coalitions','S 是有限变量集合。g 与 d 是定义在有限变量子集上的任意实值函数；不要求连续、可微、独立性或零输出基线。',r'g,d:\mathcal P_{\mathrm{fin}}(U)\to\mathbb R'),
 assumption('finite-domain','U 表示变量总体，𝒫_fin(U) 表示其所有有限子集。每次参与求和的 S、T 都有限；变量总体本身可以无限。论文应用则固定有限总体 N，只讨论 2^N。',r'S\in\mathcal P_{\mathrm{fin}}(U)')]
generic_definitions=[
 definition('interaction','交互是有限交替和。T⊆S 保证 |T|≤|S|，因此指数 |S|−|T| 是非负整数。',r'I_g(S):=\sum_{T\subseteq S}(-1)^{|S|-|T|}g(T)'),
 definition('reconstruct','R_d 是在给定保留变量集 S 上累加所有被激活的系数。',r'R_d(S):=\sum_{T\subseteq S}d(T)'),
 definition('finite-difference','插入差分比较保留 i 与掩码 i 两种状态。下面的插入引理只在 i∉S 时使用。',r'(\Delta_i g)(T):=g(T\cup\{i\})-g(T)')]
example_raw=r'''取两个变量 \(N=\{1,2\}\)，固定四个模型输出：\(v(x_\varnothing)=2\)、\(v(x_{\{1\}})=5\)、\(v(x_{\{2\}})=7\)、\(v(x_{\{1,2\}})=13\)。于是
\[I_g(\varnothing)=2,\quad I_g(\{1\})=5-2=3,\quad I_g(\{2\})=7-2=5,\]
\[I_g(\{1,2\})=13-5-7+2=3.\]
在完整输入上，\(2+3+5+3=13\)；仅保留变量 1 时，\(2+3=5\)；全掩码时求和只有空集项 2。后三个检查说明同一组系数要同时重构全部掩码输出。'''
example_centered=r'''沿用 \(v(x_\varnothing)=2\)、\(v(x_{\{1\}})=5\)、\(v(x_{\{2\}})=7\)、\(v(x_{\{1,2\}})=13\)。去基线后的函数值分别为 \(0,3,5,11\)，对应交互分别为 \(0,3,5,3\)。非空交互与未去基线时一致。
\[v(x_{\{1,2\}})=2+(0+3+5+3)=13.\]
这里为零的是 \(g_0(\varnothing)\) 和 \(I_{g_0}(\varnothing)\)，模型原始输出 \(v(x_\varnothing)\) 始终是 2。'''

reconstruction={
 'id':'proof-finite-mobius-reconstruction-v2','title':'公共证明：所有交互精确重构每一个掩码输出','kind':'library_result','statement_tex':r'\forall g\ \forall S,\quad R_{I_g}(S)=\sum_{T\subseteq S}I_g(T)=g(S)',
 'assumptions':generic_assumptions,'definitions':generic_definitions,
 'overview':'每次插入一个新变量 i，都把子集分成“不含 i”和“含 i”两组。含 i 那组的交互等于插入差分 Δᵢg 的交互；这让两个子集总和分别重构 g(S) 和 g(S∪{i})−g(S)，相加后中间项消去。先把这个辅助引理证清，再对有限集合归纳。下面用有限集合归纳给出完整证明；原论文采用有限双重和的消去路线，另在论文结果的原证明摘要中解释。',
 'proof_steps':[
 step('step-1','辅助引理：为什么子集能分成两组',r'''固定有限集合 S 及不属于 S 的变量 i。S∪{i} 的任何子集 A，要么不含 i，这时 A 本身就是 S 的子集；要么含 i，这时唯一地写成 A=T∪{i}，其中 T=A\{i}⊆S。两类互不重叠，且各自覆盖所有可能情况，所以对任意实值函数 F 可以把有限和改写为下面的两组和。没有遗漏空集：它出现在第一组 T=∅；第二组 T=∅ 对应 {i}。''',r'\sum_{A\subseteq S\cup\{i\}}F(A)=\sum_{T\subseteq S}F(T)+\sum_{T\subseteq S}F(T\cup\{i\})','子集与不含/含 i 两类的显式一一对应。',[ref('Harsanyi.interaction_insert','detail_inside_existing_proof','插入引理证明内实际使用子集拆分；这一步没有另增一个项目定理。')]),
 step('step-2','辅助引理：展开符号，得到插入差分',r'''把上一步用于交互 I_g(S∪{i}) 的定义。每个 T⊆S 都满足 i∉T，因此 |S∪{i}|=|S|+1、|T∪{i}|=|T|+1。令 k=|S|−|T|≥0：第一组的系数是 (−1)^{k+1}=−(−1)^k；第二组的系数是 (−1)^k。把同一 T 的两项合并，得到 (−1)^k[g(T∪{i})−g(T)]。最后一行正是 I_{Δᵢg}(S) 的定义。''',r'\begin{aligned}I_g(S\cup\{i\})&=\sum_{T\subseteq S}(-1)^{|S|+1-|T|}g(T)+\sum_{T\subseteq S}(-1)^{|S|-|T|}g(T\cup\{i\})\\&=\sum_{T\subseteq S}(-1)^{|S|-|T|}\bigl(g(T\cup\{i\})-g(T)\bigr)\\&=I_{\Delta_i g}(S).\end{aligned}','i∉S 及 T⊆S 给出两个插入基数；整数幂的递推关系给出负号；有限和逐项相加。',[ref('Harsanyi.interaction_insert','detail_inside_existing_proof','这个三行等式是已存在 interaction_insert 的完整数学内容；h1/h2 位于该声明证明内。')]),
 step('step-3','主证明：加强归纳命题，并处理空集',r'''对有限集合 S 作插入归纳，但归纳命题必须说“对任意集合函数 g 都有 R_{I_g}(S)=g(S)”。不能只固定最初的 g 后归纳，因为插入一步还要对新函数 Δᵢg 使用归纳假设。

当 S=∅ 时，空集只有一个子集，即自身。定义中的指数是 0，(−1)^0=1，所以 I_g(∅)=g(∅)，而重构和也只有这一项。这是归纳起点；无需且不能在这里默默令 g(∅)=0。''',r'R_{I_g}(\varnothing)=I_g(\varnothing)=(-1)^0g(\varnothing)=g(\varnothing)','有限集合插入归纳；空集的子集族只有空集本身；空集交互公式。',[ref('Harsanyi.reconstruction','detail_inside_existing_proof','归纳语句 generalizing v 以及 empty 分支都在 reconstruction 的现有证明内。'),ref('Harsanyi.interaction_empty')]),
 step('step-4','主证明：对两组和分别使用归纳假设',r'''现在设 i∉S，并假设任意函数 h 在 S 上都满足 R_{I_h}(S)=h(S)。第一步的拆分把 S∪{i} 上的重构和写成两组。对第二组中的每个 T⊆S，仍有 i∉T，所以第二步的插入交互引理可以逐项使用。得到的第二组是 Δᵢg 在 S 上的交互总和。对第一组用归纳假设 h=g，对第二组用归纳假设 h=Δᵢg，便分别得到 g(S) 与 Δᵢg(S)。这里明确使用了两次同一个归纳假设，而不是假设差分的结论未经证明成立。''',r'\begin{aligned}R_{I_g}(S\cup\{i\})&=\sum_{T\subseteq S}I_g(T)+\sum_{T\subseteq S}I_g(T\cup\{i\})\\&=R_{I_g}(S)+R_{I_{\Delta_i g}}(S)\\&=g(S)+(\Delta_i g)(S).\end{aligned}','子集拆分；插入交互引理逐项使用；加强归纳假设适用于任意集合函数。',[ref('Harsanyi.reconstruction','detail_inside_existing_proof','现有代码的 sum_congr、ih v 和 ih (marginal v i) 分别实现逐项替换和两次归纳应用。')]),
 step('step-5','主证明：消去中间输出，完成归纳',r'''按插入差分的定义，Δᵢg(S)=g(S∪{i})−g(S)。将其代入上一步，g(S) 与 −g(S) 在实数加法中消去，得到所需的 g(S∪{i})。空集起点与每次插入的步骤已经覆盖所有有限 S，因此对任意有限 S 的重构恒等式成立。论文中只需把这里的 g(S) 换成固定模型和掩码规则给出的 v(x_S)。''',r'g(S)+(\Delta_i g)(S)=g(S)+g(S\cup\{i\})-g(S)=g(S\cup\{i\})','插入差分定义与实数加减法；有限集合归纳结论。',[ref('Harsanyi.reconstruction','detail_inside_existing_proof','reconstruction 最后 simp [marginal] 完成此消去；不是五个新定理各自独立编译。')])],
 'example_md':example_raw,
 'lean':lean(['Harsanyi.reconstruction','Harsanyi.interaction_insert'],'公共有限集合重构定理及其真实库内归纳证明；论文适配另见各结果。','not_a_paper_claim'),
 'caveats':['正文五节解释已有库内证明；它们没有五个新增 Lean 声明。被验证的是库定理以及单独编译的论文适配。','所有子集和包含空集；删掉空集项后应在和外加回 g(∅)。','原文采用双重求和/二项消去，Lean 采用插入归纳；两条证明方法要分别说明，不能把原文每一行标为已逐行翻译。']}
attach_step_map(reconstruction)

uniqueness={
 'id':'proof-finite-mobius-uniqueness-v2','title':'公共证明：同时重构所有掩码输出的系数唯一','kind':'library_result','statement_tex':r'\forall g,d,\quad\bigl[\forall S,\ R_d(S)=g(S)\bigr]\Longrightarrow\bigl[\forall S,\ d(S)=I_g(S)\bigr]',
 'assumptions':generic_assumptions+[assumption('all-masks','同一组系数 d 必须重构定义域内每一个有限子集的输出，包括空集。只在一个指定集合上重构不够。',r'\forall S\in\mathcal P_{\mathrm{fin}}(U),\quad\sum_{T\subseteq S}d(T)=g(S)')],
 'definitions':generic_definitions,
 'overview':'把“对系数求子集和”再做一次交替差分，会恢复原系数。这是逆向 Möbius 反演 I_{R_d}=d。先证明这个辅助结论，再把“所有掩码上 R_d=g”的假设代入，就得到 d=I_g。下面完整证明所需的逆向反演，给出唯一性成立的理由。',
 'proof_steps':[
 step('step-1','辅助引理：逆向反演的归纳起点',r'''先暂时不使用 R_d=g，单独证明任意系数函数 d 都满足 I_{R_d}(S)=d(S)。同样对有限 S 插入归纳，并把 d 保留为任意函数，因为插入步骤会引入新函数 e。

若 S=∅，则 R_d(∅)=d(∅)。再由空集交互等于被变换函数的空集值，得 I_{R_d}(∅)=R_d(∅)=d(∅)。这是逆向反演的起点，也说明空集系数并非可以随意选择的额外自由参数。''',r'I_{R_d}(\varnothing)=R_d(\varnothing)=d(\varnothing)','重构定义、空集交互公式与加强归纳。',[ref('Harsanyi.interaction_reconstruct','detail_inside_existing_proof','interaction_reconstruct 对 S 归纳并 generalizing d；这一步为其 empty 分支。'),ref('Harsanyi.interaction_empty')]),
 step('step-2','辅助引理：重构函数的差分也是一个重构',r'''设 i∉S，并定义新的系数函数 e(U)=d(U∪{i})。对任意 T⊆S，都有 i∉T，可将 R_d(T∪{i}) 按不含/含 i 的子集拆成 R_d(T) 加 ∑_{U⊆T}d(U∪{i})。减去 R_d(T) 后，留下的恰好是 R_e(T)。

注意该等式只在 T⊆S 的范围使用。若 T 已含 i，子集拆分就不再是两类互不重叠；这个局部等式不需要、也不能强行推广到不受 T⊆S 限制的每个 T。''',r'\begin{aligned}(\Delta_i R_d)(T)&=R_d(T\cup\{i\})-R_d(T)\\&=\left(\sum_{U\subseteq T}d(U)+\sum_{U\subseteq T}d(U\cup\{i\})\right)-\sum_{U\subseteq T}d(U)\\&=\sum_{U\subseteq T}e(U)=R_e(T),\qquad T\subseteq S.\end{aligned}','i∉T；子集拆分；相同有限和消去；e 与 R_e 的定义。',[ref('Harsanyi.interaction_reconstruct','detail_inside_existing_proof','库证明中的局部 h 使用 sum_powerset_insert；e 在代码中是 fun T => d (insert i T)。')]),
 step('step-3','辅助引理：从局部一致性完成插入步骤',r'''先用重构证明中的插入交互引理，得到 I_{R_d}(S∪{i})=I_{ΔᵢR_d}(S)。交互 I_h(S) 只读取 h 在 S 的子集上的值；第二步已经逐个证明 ΔᵢR_d(T)=R_e(T)，故两种函数在这次交替和中的每一项相同。因此 I_{ΔᵢR_d}(S)=I_{R_e}(S)。最后用“对任意系数函数”的归纳假设，将 I_{R_e}(S) 化为 e(S)=d(S∪{i})。这样证明了逆向反演在插入集合上的结论。''',r'I_{R_d}(S\cup\{i\})=I_{\Delta_i R_d}(S)=I_{R_e}(S)=e(S)=d(S\cup\{i\})','插入交互引理；交互对参与求和的局部函数值保持一致；加强归纳假设。',[ref('Harsanyi.interaction_insert'),ref('Harsanyi.interaction_congr','reused_exact_declaration','这里只要求在 S 的所有子集上相同，不要求两函数处处相同。'),ref('Harsanyi.interaction_reconstruct','detail_inside_existing_proof','库证明的 rw [h, ih] 完成该辅助引理。')]),
 step('step-4','主证明：将全部掩码的重构假设代入',r'''现在恢复假设 ∀T，R_d(T)=g(T)。固定任意 S。由刚证完的逆向反演，d(S)=I_{R_d}(S)。在定义 I_{R_d}(S) 的有限和中，每个 U 都满足 U⊆S，重构假设给出 R_d(U)=g(U)。逐项替换后，该和就是 I_g(S)。因此 d(S)=I_g(S)。这一步使用的是同一组 d 在所有掩码上的假设，而不是每个 S 临时选一组系数。''',r'd(S)=I_{R_d}(S)=\sum_{U\subseteq S}(-1)^{|S|-|U|}R_d(U)=\sum_{U\subseteq S}(-1)^{|S|-|U|}g(U)=I_g(S)','逆向反演与逐个子集上的重构假设。',[ref('Harsanyi.reconstruction_unique','detail_inside_existing_proof','reconstruction_unique 中先改写 interaction_reconstruct，再用 interaction_congr 将 h T 代入。')]),
 step('step-5','主证明：逐点相等与适用范围',r'''S 是任意有限子集，所以 d 与 I_g 在定义域的每个输入上取相同值，这正是两个函数相等的含义。本公共命题的量词遍历 U 的所有有限子集；应用于论文时把总体固定为有限 N，函数定义域随之取为 2^N。

特别取 S=∅，重构假设强制 d(∅)=g(∅)。取 S={i}，又强制 d({i})=g({i})−g(∅)。继续增加集合，新的最高阶系数会被已经确定的低阶子集系数唯一决定；这解释了原论文按阶数归纳的直观路线。''',r'\forall S,\ d(S)=I_g(S)\quad\Longrightarrow\quad d=I_g','函数外延性；论文适配使用固定有限总体。',[ref('Harsanyi.reconstruction_unique','detail_inside_existing_proof','funext S 在声明开头说明函数相等的含义。'),ref('ReaderV2.cvpr_unique_coefficients','paper_adapter','真实适配的 faithful 量词是 ∀ S : Finset (Fin n)，不会要求总体外集合。')])],
 'example_md':r'''取 \(N=\{1,2\}\)，并指定 \(g(\varnothing)=2\)、\(g(\{1\})=5\)、\(g(\{2\})=7\)、\(g(\{1,2\})=13\)。任何满足全部掩码重构的 d 都必须依次满足
\[d(\varnothing)=2,\quad d(\{1\})=5-2=3,\quad d(\{2\})=7-2=5,\]
\[d(\{1,2\})=13-2-3-5=3.\]
如果只要求完整输入输出等于 13，另一组 \(d(\varnothing),d(\{1\}),d(\{2\}),d(\{1,2\})=(0,0,0,13)\) 也能满足这一条等式，却在全掩码时输出 0、在单变量掩码时也输出 0。因此“所有 S⊆N”的量词不可删除。''',
 'lean':lean(['Harsanyi.reconstruction_unique','Harsanyi.interaction_reconstruct'],'公共系数唯一性及其实际依赖的逆向反演；论文有限总体量词见独立适配。','not_a_paper_claim'),
 'caveats':['本结果约束的是固定模型/样本/基线下，使用相同 AND 激活规则的系数；不是在声称所有解释框架、因果模型或 AND-OR 分解都唯一。','原论文按 |S| 归纳；现有库以逆向反演证明唯一性。本文完整展开的是库实际采用的方法。','每个子集都要重构，包含空集。只拟合完整输入或仅近似拟合时，不能调用这个精确唯一性结论。']}
attach_step_map(uniqueness)

paper_assumptions=[assumption('fixed-data','固定一个模型 v、一个原始输入 x 和一组输入基线 r。为每个 S⊆N 使用同一规则构造 x_S，输出 v(x_S) 是有限实数。',r'N=\{1,\ldots,n\},\quad v(x_S)\in\mathbb R'),assumption('all-subsets','讨论同一有限总体 N 的全部子集，包含空集；不要求不同掩码输入必须互不相同，也不要求输入变量统计独立。',r'S\subseteq N')]
mask_definition=definition('paper-mask','论文模型仍以样本为自变量；g 只是固定 x 和 r 后的集合函数。输入基线向量 r 与输出基线 v(x_∅) 要分开。',r'g(S):=v(x_S),\qquad (x_S)_i=\begin{cases}x_i&i\in S,\\r_i&i\notin S.\end{cases}')
source_route_raw=r'''原文先交换有限双重求和，把每个输出 v(x_L) 的系数集中起来：
\[\sum_{T\subseteq S}w_T=\sum_{L\subseteq S}v(x_L)\sum_{L\subseteq T\subseteq S}(-1)^{|T|-|L|}.\]
固定 L⊆S，将 T 唯一写成 L∪Q，Q⊆S\L，内层便成为 \(\sum_{Q\subseteq S\setminus L}(-1)^{|Q|}\)。若 L=S，只有 Q=∅，系数为 1。若 L⊊S，选一个 j∈S\L；把 Q 按不含/含 j 配对，两项符号相反且绝对值相同，内层总和为 0。于是只有 L=S 的 v(x_S) 留下。这是原文二项恒等式 \(\sum_{m=0}^{k}\binom{k}{m}(-1)^m=(1-1)^k\) 的具体理由；k=0 时系数是 1，不能写成 0。

上面是原文计算路线的完整中文解释；公共 Lean 当前采用下面展开的插入归纳路线，没有为这份双重求和解释另增一个 Lean 声明。'''

cvpr_recon={
 'id':'cvpr2023-reconstruction','paper_id':'cvpr2023-sparse-concepts','title':'Theorem 1：同一组因果效应重构全部掩码输出','kind':'paper_result','result_scope':'Theorem 1 exact finite-mask reconstruction','rewrite_status':'complete_selected_result','shared_proof_id':reconstruction['id'],'shared_proof_ids':[reconstruction['id']],
 'source_refs':[source('src-cvpr2023-main',[3,4],['Theorem 1；Eq.(2) 模型输出；Eq.(4) 掩码规则']),source('src-cvpr2023-supplement',[2,3],['Appendix C：Theorem 1 重述与 necessity proof'])],
 'statement_tex':r'w_A:=\sum_{T\subseteq A}(-1)^{|A|-|T|}v(x_T),\qquad\forall S\subseteq N,\quad Y(x_S)=\sum_{A\subseteq S}w_A=v(x_S)',
 'assumptions':paper_assumptions+[assumption('full-pattern-family','本条精确结论使用全部模式 Ω=2^N，每个模式 A 的激活规则是所有 A 中变量都保留时贡献 w_A。',r'\Omega=2^N,\quad C_A(x_S)=\mathbf1_{A\subseteq S}')],
 'definitions':[mask_definition,definition('causal-effect','本篇直接对原始模型输出作交互变换，包含空集模式。',r'w_A=I_g(A),\quad w_\varnothing=v(x_\varnothing)'),definition('graph-output','在掩码输入 x_S 上，把所有已触发模式的效应相加。',r'Y(x_S):=\sum_{A\subseteq N}w_A\mathbf1_{A\subseteq S}=\sum_{A\subseteq S}w_A')],
 'overview':'先把论文的掩码输出和 AND 模式激活准确变成集合函数及子集和，再使用下方完整公共重构证明。原文没有假设 v(x_∅)=0；空集模式给出的常数项正好承载这个输出基线。',
 'original_statement_md':r'正式正文 PDF 第 3 页 Theorem 1 给出 \(\forall S\subseteq N,\ Y(x_S)=v(x_S)\)，效应定义为 \(w_A=\sum_{T\subseteq A}(-1)^{|A|-|T|}v(x_T)\)。补充 PDF 第 2 页 Appendix C 重述，并在第 3 页给出证明。此处为公式摘录与中文定位，完整原文以正式 PDF 为准。',
 'original_proof_md':source_route_raw,
 'proof_steps':[
 step('step-1','将激活规则化成子集求和',r'''固定一个待解释的掩码 S。模式 A 被触发当且仅当 A⊆S，所以求和中 A⊈S 的指示函数为 0、A⊆S 的为 1，Y(x_S) 就是 ∑_{A⊆S}w_A。A=∅ 是 S 的子集，空乘积约定给出其激活值为 1，因此空集效应始终贡献；不能把它删掉。''',r'Y(x_S)=\sum_{A\subseteq N}w_A\mathbf1_{A\subseteq S}=\sum_{A\subseteq S}w_A','原文 SCM 输出与 AND 激活的确定性求和语义。',[]),
 step('step-2','对齐集合函数与有限总体',r'''定义 g(S)=v(x_S)。由于 x、基线与模型都固定，这确实是定义在 2^N 上的同一个实值函数。将 g(T)=v(x_T) 代入交互定义，论文的 w_A 就逐项等于 I_g(A)。''',r'g(S)=v(x_S),\qquad w_A=I_g(A)','定义逐项一致；Fin n 表示固定有限总体。',[ref('ReaderV2.cvpr_reconstruction','paper_adapter','适配以真实模型输出函数 v 和真实类型的 mask 参数陈述有限子集和；具体 DNN/掩码实现不在验证范围。')]),
 step('step-3','应用完整公共重构证明',r'''下方公共证明说明，对任意实值集合函数 g 以及任意有限 S，∑_{A⊆S}I_g(A)=g(S)。将第二步的定义代入，并结合第一步得到 Y(x_S)=v(x_S)。该结论对所有 S 同时成立，而不是为每个掩码重新选一组权重。特别 S=∅ 时两边等于 v(x_∅)，并非一般等于 0。''',r'Y(x_S)=\sum_{A\subseteq S}w_A=\sum_{A\subseteq S}I_g(A)=g(S)=v(x_S)','公共重构定理；定义代入。',[ref('Harsanyi.reconstruction'),ref('ReaderV2.cvpr_reconstruction','paper_adapter','真实代码只复用整条 reconstruction；辅助推导在下方公共证明与库源码中展开。')])],
 'example_md':example_raw,'lean':lean(['ReaderV2.cvpr_reconstruction'],'仅验证 Theorem 1 的有限掩码子集和恒等式；原文因果解释与具体 DNN 运行不由 Lean 检查。'),
 'caveats':['正文数学适配的人工作业已核对正式 main/supp；Lean 编译检查给出的形式陈述，不自动保证译文或论文解释正确。','精确重构以 Ω=2^N 为前提；论文后续稀疏模式的近似效果未在此条证明。','第一步的指示函数模型语义已人工核对，但本轮 adapter 从等价子集和开始，没有新增一个因果图概率分布的 Lean 模型。']}
attach_step_map(cvpr_recon)

cvpr_unique={
 'id':'cvpr2023-uniqueness','paper_id':'cvpr2023-sparse-concepts','title':'Appendix C：全部掩码都精确重构时，AND 系数唯一','kind':'paper_result','result_scope':'Appendix C uniqueness assertion for fixed AND activation','rewrite_status':'complete_selected_result','shared_proof_id':uniqueness['id'],'shared_proof_ids':[uniqueness['id']],
 'source_refs':[source('src-cvpr2023-supplement',[2,3],['Appendix C Theorem 1 后的 unique metric 断言；sufficiency proof'])],
 'statement_tex':r'\bigl[\forall S\subseteq N,\ v(x_S)=\sum_{A\subseteq S}\widetilde w_A\bigr]\Longrightarrow\bigl[\forall A\subseteq N,\ \widetilde w_A=\sum_{T\subseteq A}(-1)^{|A|-|T|}v(x_T)=w_A\bigr]',
 'assumptions':paper_assumptions+[assumption('same-coefficients','同一组候选系数 w̃_A 使用相同的 AND 激活规则，并在全部掩码上精确重构。允许所有系数为任意实数。',r'\forall S\subseteq N,\quad\sum_{A\subseteq S}\widetilde w_A=v(x_S)')],
 'definitions':[mask_definition,definition('candidate-coefficients','候选系数 d 与原文 w̃ 是同一个 2^N→ℝ 函数，不会为不同 S 改变。',r'd(A):=\widetilde w_A,\qquad g(S):=v(x_S)')],
 'overview':'在原文已有的全部掩码、相同 AND 激活与固定基线定义下，本条将“满足 faithfulness 的 metric 唯一”精确陈述为系数函数唯一。下方完整公共证明展开逆向反演，解释重构输出如何反过来唯一确定每个系数。',
 'original_statement_md':r'正式补充 PDF 第 2 页 Appendix C 在 Theorem 1 后断言 Harsanyi dividend 是满足 faithfulness 的唯一 metric；第 3 页说明：若 \(\widetilde w\) 也满足所有 S 的重构，则 \(\forall S\subseteq N,\ \widetilde w_S=w_S\)。这不是论文单独编号的新定理。',
 'original_proof_md':r'''原文第 3 页从空集、单变量和二变量展开系数，然后按集合大小归纳。对一个待确定的 S，从输出恒等式中分离最高阶项：
\[v(x_S)=\widetilde w_S+\sum_{A\subsetneq S}\widetilde w_A.\]
已确定的真子集系数代入后，把有限交替和按 v(x_L) 收集，得到 w̃_S 的 Harsanyi 公式。本重写保留相同结论与假设，但完整展开现有 Lean 采用的“先证明逆向反演，再应用重构假设”路线；原文按阶数的推导没有逐行改成 Lean。''',
 'proof_steps':[
 step('step-1','将全部掩码假设写成公共定理的前提',r'''固定 x 与 r，设 g(S)=v(x_S)、d(A)=w̃_A。论文的 faithfulness 前提就是对每个 S⊆N 都有 R_d(S)=g(S)。这里的 g、d 都只定义在 2^N 上，所以全称量词既包含全掩码，又不涉及 N 之外的变量。''',r'\forall S\subseteq N,\quad R_d(S)=g(S)','候选系数、集合函数、固定有限总体的定义。',[ref('ReaderV2.cvpr_unique_coefficients','paper_adapter','该真实声明的 faithful 参数精确记录所有有限总体掩码，而非只要求完整输入。')]),
 step('step-2','使用展开过的公共唯一性证明',r'''下方公共证明先给出 I_{R_d}=d，再逐项代入 R_d=g，推出 d=I_g。因此每个 A⊆N 都有 w̃_A=I_g(A)=w_A。S=∅ 的假设在这个推导中强制 w̃_∅=v(x_∅)；它不会被零基线约定替代。''',r'\widetilde w_A=d(A)=I_g(A)=w_A,\qquad A\subseteq N','逆向反演与函数逐点相等。',[ref('Harsanyi.reconstruction_unique'),ref('ReaderV2.cvpr_unique_coefficients','paper_adapter','适配复用整条已证明的系数唯一性。')])],
 'example_md':uniqueness['example_md'],'lean':lean(['ReaderV2.cvpr_unique_coefficients'],'仅验证 Appendix C 在同一 AND 规则下、所有掩码精确重构的系数唯一性。'),
 'caveats':['不把唯一性扩大为任意因果解释或任意 AND-OR 分解唯一。','只在 N 上匹配一条输出、只在部分掩码上匹配或只作近似匹配，都不足以使用这条命题。']}
attach_step_map(cvpr_unique)

sparse={
 'id':'iclr2024-sparse-reconstruction','paper_id':'iclr2024-sparse','title':'Theorem 1：去基线交互之和，再加回模型输出基线','kind':'paper_result','result_scope':'Theorem 1 exact centered reconstruction only','rewrite_status':'complete_selected_result','shared_proof_id':reconstruction['id'],'shared_proof_ids':[reconstruction['id']],
 'source_refs':[source('src-iclr2024-sparse-main',[3,4,15],['PDF p3 Eq.(1) 与 u(∅)=I(∅)=0；p4 Theorem 1；p15 Appendix B.1 Eq.(7) 及本篇重证'])],
 'statement_tex':r'u(T):=v(x_T)-v(x_\varnothing),\quad I(T):=\sum_{L\subseteq T}(-1)^{|T|-|L|}u(L),\qquad\forall S\subseteq N,\quad v(x_S)=\sum_{T\subseteq S}I(T)+v(x_\varnothing)',
 'assumptions':paper_assumptions,'definitions':[mask_definition,definition('source-centered-game','本篇定义 u 就是 g₀；其空集值为零来自显式相减。',r'u(T)=g_0(T)=v(x_T)-v(x_\varnothing)'),definition('source-interaction','本篇 I 对去基线函数作变换，因此空集交互是零。',r'I(T)=I_{g_0}(T),\qquad I(\varnothing)=u(\varnothing)=0')],
 'overview':'本篇正文明确把交互定义在 u(T)=v(x_T)−v(x_∅) 上，并把 Theorem 1 标为已有结果，仍在 Appendix B.1 给出完整重证。要把它与 CVPR2023 的式子比较，必须先区分空集项：本篇交互总和重构的是去基线输出，最后再加回 v(x_∅)。不需要把模型原始输出基线假设为零。',
 'original_statement_md':r'正式 PDF 第 3 页 Eq.(1) 定义 \(u(T)=v(x_T)-v(x_\varnothing)\) 和 I(T)，并明确 \(u(\varnothing)=I(\varnothing)=0\)。第 4 页 Theorem 1 给出 \(\forall S\subseteq N,\ v(x_S)=\sum_{T\subseteq S}I(T)+v(x_\varnothing)\)，标明已在 Ren et al. (2023a) 与 Appendix B.1 证明。第 15 页 Eq.(7) 重述。',
 'original_proof_md':r'''Appendix B.1 的完整推导首先交换有限双重和，再按每个 u(L) 集中其系数：
\[\sum_{T\subseteq S}I(T)=\sum_{L\subseteq S}u(L)\sum_{L\subseteq T\subseteq S}(-1)^{|T|-|L|}.\]
若 L=S，内层等于 1；若 L⊊S，内层等于 \((1-1)^{|S|-|L|}=0\)。所以交互总和为 \(u(S)=v(x_S)-v(x_\varnothing)\)，加回基线即得 Theorem 1。这条恒等式是继承并重证的基础结果，不能计作本篇新提出的稀疏性证明。下面公共正文展开相同命题的库内归纳证明。''',
 'proof_steps':[
 step('step-1','先把原输出与去基线函数分开',r'''固定原始模型输出 g(S)=v(x_S)。本篇另定义 u(S)=g₀(S)=g(S)−g(∅)。取 S=∅，两项完全相同，所以 u(∅)=0；再由空集交互公式得到 I(∅)=0。这里没有推出 v(x_∅)=0。''',r'u(\varnothing)=v(x_\varnothing)-v(x_\varnothing)=0,\qquad I(\varnothing)=0','原文 u 的定义与空集交互公式。',[ref('ReaderV2.sparse_empty','paper_adapter','真实声明只说 centered maskedGame 的空集交互为零。')]),
 step('step-2','把公共重构定理用在 u，而不是原输出 g',r'''下方公共证明适用于任意实值集合函数，故也适用于 u=g₀。它给出的结论是 ∑_{T⊆S}I_u(T)=u(S)。因为原文 I(T) 定义为 I_u(T)，右边等于 v(x_S)−v(x_∅)。所有子集仍然包括空集，只是它的贡献在本篇定义下恰好为零。''',r'\sum_{T\subseteq S}I(T)=\sum_{T\subseteq S}I_{g_0}(T)=g_0(S)=v(x_S)-v(x_\varnothing)','公共重构定理与论文去基线定义。',[ref('Harsanyi.reconstruction'),ref('ReaderV2.sparse_centered_reconstruction','paper_adapter','代码将 reconstruction 用于 centered (maskedGame v mask)，不添加原输出基线为零的参数。')]),
 step('step-3','加回输出基线，并核对空集边界',r'''在上式两侧加 v(x_∅)，得到原文 Theorem 1。若 S=∅，交互和为 I(∅)=0，右边就是 v(x_∅)，边界也成立。对任何非空 T，公共去基线结果说明 I_{g₀}(T)=I_g(T)；两篇写法的非空系数一致，区别由空集项移到和外的基线承载。''',r'v(x_S)=\sum_{T\subseteq S}I(T)+v(x_\varnothing)','实数加法移项；非空交互的去基线不变性。',[ref('ReaderV2.sparse_centered_reconstruction','paper_adapter'),ref('ReaderV2.baseline_nonempty_agreement','paper_adapter','非空前提 hS 必须显式存在。')])],
 'example_md':example_centered,'lean':lean(['ReaderV2.sparse_centered_reconstruction','ReaderV2.sparse_empty'],'仅验证原文 Theorem 1 的精确中心化重构；不验证本篇高阶导数条件、稀疏性定理或近似误差结论。'),
 'caveats':['原文把这一条标为继承自 Ren et al. (2023a)，本篇仍给出重证；本页共享基础证明，不冒充新的稀疏交互定理。','原文后续关于稀疏性、Taylor 展开和训练条件的命题都未在本条形式化。','零值是 u(∅)=0，不是 v(x_∅)=0。']}
attach_step_map(sparse)

f11_and={
 'id':'iclr2024-generalizable-and','paper_id':'iclr2024-generalizable','title':'Appendix C(1)：固定原样本的 AND 分量精确重构','kind':'paper_result','result_scope':'Selected Appendix C(1) AND component subresult, not full Theorem 2','rewrite_status':'complete_selected_subresult','shared_proof_id':reconstruction['id'],'shared_proof_ids':[reconstruction['id']],
 'source_refs':[source('src-iclr2024-generalizable-main',[2,12,13],['p2 Eq.(1) AND 定义与空集约定；p12 Appendix C Proof(1) 的固定 x 子结论；p13 Eq.(8) 完整 AND 推导'])],
 'statement_tex':r'I_{\mathrm{and}}(S\mid x):=\sum_{L\subseteq S}(-1)^{|S|-|L|}v_{\mathrm{and}}(x_L),\qquad\forall T\subseteq N,\quad v_{\mathrm{and}}(x_T)=\sum_{S\subseteq T}I_{\mathrm{and}}(S\mid x)',
 'assumptions':paper_assumptions+[assumption('and-component','固定一个实值分量函数 v_and，并使用与原样本相同的掩码规则。只证明这个分量的恒等式，不要求任何特定的分解优化方法。',r'v_{\mathrm{and}}(x_T)\in\mathbb R')],
 'definitions':[definition('and-output','为避免把总体模型和分量混淆，令 g_and 是该固定 AND 分量在所有掩码输入上的输出。',r'g_{\mathrm{and}}(S):=v_{\mathrm{and}}(x_S)'),definition('and-coefficients','附录 C(1) 明确使用固定原样本 x 的系数；它没有先对分量输出去基线。',r'I_{\mathrm{and}}(S\mid x)=I_{g_{\mathrm{and}}}(S),\qquad I_{\mathrm{and}}(\varnothing\mid x)=v_{\mathrm{and}}(x_\varnothing)')],
 'overview':'本页选的是 Appendix C(1) 自己明确写出的固定 x 的 AND 子结论。它是 Theorem 2 证明中的一个分量，但本页完成状态只覆盖这个子结论。原文引用既有 Harsanyi 重构，并在第 13 页完整重证；下方公共证明展示其严谨理由及实际 Lean 路线。',
 'original_statement_md':r'正式 PDF 第 12 页 Appendix C Proof(1) 明确写出 \(\forall T\subseteq N,\ v_{\mathrm{and}}(x_T)=\sum_{S\subseteq T}I_{\mathrm{and}}(S\mid x)\)，下一段定义 \(I_{\mathrm{and}}(S\mid x)=\sum_{L\subseteq S}(-1)^{|S|-|L|}v_{\mathrm{and}}(x_L)\)。这里确实是固定 x，区别于正文 Theorem 2 的 x_T 记号；本页不替换后者原式。',
 'original_proof_md':r'''正式 PDF 第 12–13 页将 AND 定义代入子集和，按 L 集中 v_and(x_L) 的系数。若 L=T，系数为 1；若 L⊊T，系数为 \((1-1)^{|T|-|L|}=0\)，故只剩 v_and(x_T)。第 13 页 Eq.(8) 给出结果。
\[\sum_{S\subseteq T}I_{\mathrm{and}}(S\mid x)=\sum_{L\subseteq T}v_{\mathrm{and}}(x_L)\sum_{L\subseteq S\subseteq T}(-1)^{|S|-|L|}=v_{\mathrm{and}}(x_T).\]
这是本页对齐的原证明范围。附录同页起接下来的 OR 推导及全文 Theorem 2 不在已完成范围内。''',
 'proof_steps':[
 step('step-1','固定 AND 分量与原样本 x',r'''取 g_and(S)=v_and(x_S)。样本 x、输入基线以及分量函数 v_and 在全部 S 中固定。附录 C(1) 的交互因此是对 g_and 的 Harsanyi 变换，空集项等于 v_and(x_∅)。不要求 v_and(x_∅)=0。''',r'I_{\mathrm{and}}(S\mid x)=I_{g_{\mathrm{and}}}(S)','附录 C(1) 的定义逐项一致。',[ref('ReaderV2.generalizable_and_subresult','paper_adapter','实际参数名 vAnd 明确是分量；适配没有为 OR 分量或全部模型作任何验证声明。')]),
 step('step-2','对分量函数应用完整重构证明',r'''公共重构定理对任意实值集合函数成立，因此将 g 换为 g_and，待重构集合换为 T，就得到 ∑_{S⊆T}I_{g_and}(S)=g_and(T)。用第一步定义改回论文记号，恰好是第 12 页的固定 x 子结论。空集 T=∅ 时，只留下 I_and(∅|x)=v_and(x_∅)，边界仍成立。''',r'\sum_{S\subseteq T}I_{\mathrm{and}}(S\mid x)=\sum_{S\subseteq T}I_{g_{\mathrm{and}}}(S)=g_{\mathrm{and}}(T)=v_{\mathrm{and}}(x_T)','公共重构定理、固定分量定义与空集交互。',[ref('Harsanyi.reconstruction'),ref('ReaderV2.generalizable_and_subresult','paper_adapter','真实编译的声明精确是此选定固定 x AND 子结论。')])],
 'example_md':example_raw.replace('模型输出','AND 分量输出').replace('v(x_',r'v_{\mathrm{and}}(x_'),
 'lean':lean(['ReaderV2.generalizable_and_subresult'],'只验证正式附录 C(1) 的固定 x AND 分量子结论。完整 Theorem 2、OR 推导及 AND-OR 分解未被该报告覆盖。'),
 'caveats':['这是一条已完成的选定子结论，不是完整 Theorem 2 的完成标记。','正文 Theorem 2 使用 I(S|x_T)，而附录 C(1) 定义与子结论使用固定 x；全文记号语义仍单列对齐说明，不在此页静默改写。','OR 原证明第 14 页的中间求和疑点单列待用户确认；它不影响本页第 12–13 页 AND 子结论的对齐，也不能被本页编译通过所关闭。'],
 'alignment_note_ids':['issue-f11-mask-notation-20260930'],'related_issue_ids':['issue-f11-or-intermediate-20260930']}
attach_step_map(f11_and)

centering={
 'id':'library-baseline-centering','paper_id':None,'title':'公共结果：空集交互与去基线转换','kind':'library_result','result_scope':'Explicit raw/centered convention conversion','rewrite_status':'complete_library_result','shared_proof_id':None,'shared_proof_ids':[],
 'source_refs':[],
 'statement_tex':r'g_0(S):=g(S)-g(\varnothing),\quad I_g(\varnothing)=g(\varnothing),\quad I_{g_0}(\varnothing)=0,\quad S\ne\varnothing\Longrightarrow I_{g_0}(S)=I_g(S)',
 'assumptions':generic_assumptions,'definitions':generic_definitions+[definition('centering-definition','模型输出基线取为标量 b=g(∅)=v(x_∅)。把它作为常数函数从 g 的每一个值中减去。',r'g_0(S):=g(S)-b,\qquad b:=g(\varnothing)=v(x_\varnothing)')],
 'overview':'空集交互承载常数基线。把每个模型输出都减去同一个 v(x_∅)，只会去掉这个空集项，任何非空交互都保留。这是公共库的记号转换结果，服务于不同论文约定的比较，不冒充某篇论文新定理。',
 'proof_steps':[
 step('step-1','直接计算两个空集值',r'''空集只有一个子集，指数为 0，所以 I_g(∅)=g(∅)=v(x_∅)。另一方面，g₀(∅)=g(∅)−g(∅)=0，因此 I_{g₀}(∅)=0。两个交互变换作用于不同的集合函数；不能从后一个零值推出原始模型输出为零。''',r'I_g(\varnothing)=v(x_\varnothing),\qquad g_0(\varnothing)=I_{g_0}(\varnothing)=0','空集的子集族、(−1)^0=1 与同一数相减。',[ref('Harsanyi.interaction_empty'),ref('Harsanyi.centered_empty'),ref('ReaderV2.masked_empty','paper_adapter'),ref('ReaderV2.sparse_empty','paper_adapter')]),
 step('step-2','常数函数的非空交互为什么消失',r'''设 c(T)=b 为常数函数。若 S=∅，它的交互等于 b。若 S 非空，选 i∈S 并令 S′=S\{i}，则 i∉S′。插入交互引理给出 I_c(S)=I_{Δᵢc}(S′)。由于 c(T∪{i})−c(T)=b−b=0，Δᵢc 是零函数，定义中的每一项都为零。因此非空常数交互为零。这个论证也覆盖单变量 S，此时 S′=∅。''',r'I_c(S)=\begin{cases}b&S=\varnothing,\\0&S\ne\varnothing.\end{cases}','插入交互引理与常数差分为零。',[ref('Harsanyi.interaction_const','reused_exact_declaration','现有常数交互证明同样使用插入差分为零的机制。')]),
 step('step-3','逐项线性性把去基线化成两种情况',r'''去基线函数是 g₀=g−c。交互定义是有限线性和，因此 I_{g₀}(S)=I_g(S)−I_c(S)。把第二步的常数交互公式代入：空集时减去 b，结果是 0；非空时减去 0，结果与 I_g(S) 完全相同。这里必须保留非空条件；在空集上，原交互与去基线交互的值一般不同。''',r'I_{g_0}(S)=I_g(S)-\mathbf1_{S=\varnothing}g(\varnothing)','交互变换对差值的线性性、常数交互公式。',[ref('Harsanyi.interaction_centered'),ref('Harsanyi.interaction_centered_nonempty'),ref('ReaderV2.baseline_nonempty_agreement','paper_adapter','该 adapter 明确要求 S.Nonempty。')]),
 step('step-4','重构式的两种写法都加回同一个基线',r'''把公共重构定理用于 g₀，得到 ∑_{T⊆S}I_{g₀}(T)=g₀(S)=g(S)−g(∅)，两侧加回 g(∅) 就得到第一种写法。由于空集交互为零而非空交互不变，也可把它写成第二种只求非空子集和的式子。

若 S=∅，第一式的交互总和为 0，第二式的非空子集族为空、和也为 0，两式都还原为 g(∅)=v(x_∅)。这说明删去空集项必须明确补回基线。''',r'\begin{aligned}v(x_S)&=v(x_\varnothing)+\sum_{T\subseteq S}I_{g_0}(T)\\&=v(x_\varnothing)+\sum_{\varnothing\ne T\subseteq S}I_g(T).\end{aligned}','公共重构；分离空集求和项；去基线的非空交互不变性。',[ref('ReaderV2.sparse_centered_reconstruction','paper_adapter'),ref('ReaderV2.baseline_explicit_reconstruction','paper_adapter','非空和在真实代码中为 S.powerset.erase ∅，包含 S=∅ 的情形。')])],
 'example_md':example_centered,'lean':lean(['ReaderV2.masked_empty','ReaderV2.sparse_empty','ReaderV2.baseline_nonempty_agreement','ReaderV2.baseline_explicit_reconstruction'],'公共空集/去基线结果的真实模型输出记号适配；不是新论文定理。','not_a_paper_claim'),
 'caveats':['项目旧库的函数参数可能名为 v，但其类型是集合函数，本文统一解释为 g；论文模型 v 的类型是输入样本到实数。','输入全部置为零基线，也不保证模型输出 v(x_∅) 为零；二者是不同层次。','本页只讨论输出减去常数的转换，不证明如何选择最优输入基线。']}
attach_step_map(centering)

f11_pending={
 'id':'iclr2024-generalizable-andor','paper_id':'iclr2024-generalizable','title':'Theorem 2：原文 AND-OR 全式（对齐待确认）','kind':'paper_result','result_scope':'Original full Theorem 2; intentionally not a completed proof','rewrite_status':'not_rewritten_pending_source_review','shared_proof_id':None,'shared_proof_ids':[],
 'source_refs':[source('src-iclr2024-generalizable-main',[3,12,13,14],['p3 Eq.(3)；p12 Eq.(7)；Appendix C OR proof pp13–14'])],
 'statement_tex':r'v(x_T)=v_{\mathrm{and}}(x_T)+v_{\mathrm{or}}(x_T)=\sum_{S\subseteq T}I_{\mathrm{and}}(S\mid x_T)+\sum_{S\in\{S:S\cap T\ne\varnothing\}\cup\{\varnothing\}}I_{\mathrm{or}}(S\mid x_T)',
 'assumptions':[assumption('paper-decomposition','原文固定模型输出的 AND/OR 分量分解；此处只保留原式，不增补修正条件。',r'v(x_T)=v_{\mathrm{and}}(x_T)+v_{\mathrm{or}}(x_T)')],
 'definitions':[definition('or-empty-source-convention','原文明确单列空集 OR 值。本页把它作为原文定义约定记录，不因为 Eq.(2) 的惯用非空适用范围而另造数学错误。',r'I_{\mathrm{or}}(\varnothing\mid x)=v_{\mathrm{or}}(x_\varnothing)')],
 'overview':'保留正式原文全式供核对。第 14 页 OR 推导有具体中间求和问题；正文与附录的 x_T/固定 x 记号还需语义对齐。本轮没有重写或发布完整 Theorem 2 的修正版。已完成的第 12–13 页 AND 子结论另列，不能覆盖这一状态。',
 'original_statement_md':r'这是正式 PDF 第 3 页 Eq.(3) 与第 12 页 Eq.(7) 的原式，保留 \(I_{\mathrm{and}}(S\mid x_T)\)、\(I_{\mathrm{or}}(S\mid x_T)\) 的 x_T 记号。原文出处、OR 定义、以及第 14 页原证明均保持不变。',
 'original_proof_md':r'原文 Appendix C 分成 AND、OR、AND-OR 三部分。第 13–14 页 OR 部分交换有限双重和，再按 L=N\T、L=N、L∩T≠∅ 且 L≠N、L∩T=∅ 且 L≠N\T 四类计算系数，第 14 页 Eq.(9) 得到 OR 总和。相关疑点见下方报告；此处不提供替代证明或补入新假设。',
 'proof_steps':[],'example_md':'','lean':{'status':'not_formalized','label':'完整 Theorem 2 未形式化；原文问题与语义对齐待确认','compiled':False,'axiom_audit':'not_run_for_this_claim','scope':'No Lean declaration for the original full Theorem 2','declarations':[],'source_path':None,'report_path':None,'adapter_code':'','step_map':[]},
 'caveats':['OR 中间求和问题已登记 issue-f11-or-intermediate-20260930；用户确认与修正授权均 pending。','x_T 与固定 x 的差异登记为记号语义对齐说明，不据此判断全定理不成立。','公共库与 AND adapter 的编译通过不能关闭此项原文问题。'],
 'related_issue_ids':['issue-f11-or-intermediate-20260930'],'alignment_note_ids':['issue-f11-mask-notation-20260930']}

items=[cvpr_recon,cvpr_unique,sparse,f11_and,centering,f11_pending]
for item in [reconstruction,uniqueness]+items:
 item['rewrite_status']='not_started' if item['id']=='iclr2024-generalizable-andor' else 'complete'
 item['alignment_status']='pending_alignment' if item['id']=='iclr2024-generalizable-andor' else ('not_a_paper_claim' if item.get('kind')=='library_result' else 'agent_checked_selected_statement')
def declaration_excerpt(name):
 d=DECL[name];lines=(ROOT/d['source_path']).read_text().splitlines();lo=d['line']-1
 end=next((i for i in range(lo+1,len(lines)) if re.match(r'(?:@\[simp\] )?(?:noncomputable )?(?:def|theorem) |end ',lines[i])),len(lines))
 return '\n'.join(lines[lo:end]).strip()
for item in [reconstruction,uniqueness]+items:
 item['user_review_status']='pending' if item.get('kind')=='paper_result' else 'not_a_paper_claim'
 item['completion_scope']=item.get('result_scope',item['lean']['scope'])
 item['lean']['user_review_status']=item['user_review_status']
 if item['lean']['status']=='verified':
  names=item['lean']['declarations']
  if names[0].startswith('ReaderV2.'):
   blocks=[declaration_excerpt('ReaderV2.maskedGame')]+[declaration_excerpt(n) for n in names if n!='ReaderV2.maskedGame']
   item['lean']['adapter_code']='import Harsanyi.Core.Properties\n\nnamespace ReaderV2\nopen Finset Harsanyi\n\n'+'\n\n'.join(blocks)+'\n\nend ReaderV2\n'
   item['lean']['code_kind']='exact_source_declarations_with_import_context'
  else:
   item['lean']['adapter_code']='\n\n'.join(declaration_excerpt(n) for n in reversed(names))
   item['lean']['source_path']=DECL[names[0]]['source_path']
   item['lean']['code_kind']='actual_public_library_source_excerpt'
for item in [reconstruction,uniqueness]+items:
 if item['lean']['status']=='verified':
  item['lean']['encoding_note']='数学上的有限子集族用 Finset 表示；库要求可判定相等关系。论文适配取 Fin n，使 ∀ S : Finset (Fin n) 恰好遍历固定总体的全部掩码。T⊆S 保证指数中的自然数减法没有截断。库源码中的 h1/h2 是插入基数和符号计算；generalizing v/d 保持对任意函数的加强归纳；funext 实现逐点相等。编译检查形式陈述，定义与论文语义的对应仍须人工核对。'
cvpr_recon['display_statement_tex']=[r'w_A:=\sum_{T\subseteq A}(-1)^{|A|-|T|}v(x_T)',r'\forall S\subseteq N,\quad Y(x_S)=\sum_{A\subseteq S}w_A=v(x_S)']
cvpr_unique['display_statement_tex']=[r'\left[\forall S\subseteq N,\quad v(x_S)=\sum_{A\subseteq S}\widetilde w_A\right]',r'\Longrightarrow\quad\forall A\subseteq N,\quad\widetilde w_A=I_g(A)=w_A']
sparse['display_statement_tex']=[r'u(T):=v(x_T)-v(x_\varnothing)',r'I(T):=\sum_{L\subseteq T}(-1)^{|T|-|L|}u(L)',r'\forall S\subseteq N,\quad v(x_S)=\sum_{T\subseteq S}I(T)+v(x_\varnothing)']
f11_and['display_statement_tex']=[r'I_{\mathrm{and}}(S\mid x):=\sum_{L\subseteq S}(-1)^{|S|-|L|}v_{\mathrm{and}}(x_L)',r'\forall T\subseteq N,\quad v_{\mathrm{and}}(x_T)=\sum_{S\subseteq T}I_{\mathrm{and}}(S\mid x)']
centering['display_statement_tex']=[r'g_0(S):=g(S)-g(\varnothing)',r'I_g(\varnothing)=g(\varnothing),\quad I_{g_0}(\varnothing)=0',r'S\ne\varnothing\Longrightarrow I_{g_0}(S)=I_g(S)']
from text_math import mathify
for item in [reconstruction,uniqueness]+items:
 for key in ['overview','example_md','original_statement_md','original_proof_md']:
  if key in item:item[key]=mathify(item[key])
 for group in ['assumptions','definitions','proof_steps']:
  for row in item[group]:
   for key in ['text_md','body_md','justification']:
    if key in row:row[key]=mathify(row[key])
 item['caveats']=[mathify(t) for t in item['caveats']]
 if item.get('original_statement_md'):
  item['original_statement_note']='正式原命题公式摘录与项目中文定位说明；不是原文完整逐字转录。完整正式原文见 PDF。'
  item['original_statement_source_type']='project_source_summary_with_formula_excerpt'
 if item.get('original_proof_md'):
  item['original_proof_note']='原证明路线的项目中文说明或摘要，含明确标注的数学解释；不是原作者证明的完整逐字转录。正式原文见 PDF。'
  item['original_proof_source_type']='project_chinese_explanation_of_source_proof_route'
 for caveat_index,t in enumerate(item['caveats']):
  item['caveats'][caveat_index]=t.replace('数学适配的人工作业已核对','本次代理已核对数学适配与')
content={'schema_version':'2.0','language':'zh-CN','mathematical_content_status':'selected_results_complete','notation':notation,'shared_proofs':[reconstruction,uniqueness],'results':items,'verification_report':REPORT_PATH,'issues_path':'research/reader-v2-20260930/math/issues.json','source_alignment_policy':'Source alignment is a separate human review. Lean checks the formal statement, not the correctness of translating the paper.','excluded_from_public_navigation':['research/reader-v2-20260930/math/experimental/IndependentOR.lean'],'counts':{'papers_with_complete_selected_result':3,'complete_paper_results':4,'complete_library_results':1,'pending_paper_results':1,'shared_complete_proofs':2},'not_formalized':['F11 full Theorem 2 AND-OR formula and original OR proof','F03 sparsity/high-order derivative/Taylor/approximation theorems','classical factorial-weight Shapley equivalence','concrete neural network evaluation and concrete input masking implementation','paper-source semantics of causal interpretation','the original double-sum proof route as a new separate Lean declaration']}
(DATA/'math-content.json').write_text(json.dumps(content,ensure_ascii=False,indent=2)+'\n')

def md(item,shared=None):
 out=['# '+item['title'],'','本页范围：'+item.get('result_scope','公共有限集合定理')+'。','']
 if item.get('source_refs'):
  out+=['## 正式来源','']
  for s in item['source_refs']:
   out+=['- '+s['title']+'，PDF 页 '+','.join(map(str,s['pages']))+'：'+ '; '.join(loc['label'] for loc in s['locations'])+'。来源文件：`'+s['local_path']+'`。','']
 out+=['## 命题','',r'\['+item['statement_tex']+r'\]','', '## 必要定义与适用条件','']
 for a in item['assumptions']+item['definitions']:
  out+=[a['text_md'],'']
  if a.get('formula_tex'):out+=[r'\['+a['formula_tex']+r'\]','']
 out+=['## 证明思路','',item['overview'],'']
 for s in item['proof_steps']:
  out+=['## '+s['title'],'', '<a id="'+s['id']+'"></a>','',s['body_md'],'']
  if s.get('formula_tex'):out+=[r'\['+s['formula_tex']+r'\]','']
  out+=['依据：'+s['justification'],'']
  pass
 if shared:
  out+=['## 复用的完整公共证明','', '以下公共证明作为整体被复用，论文特有定义已在上文逐项对齐。','']
  for s in shared['proof_steps']:
   out+=['### '+s['title'],'',s['body_md'],'',r'\['+s['formula_tex']+r'\]','', '依据：'+s['justification'],'']
 out+=['## 小例子与空集','',item['example_md'] or '此待确认条目不提供重写证明或替代例子。','', '## Lean 检查范围','',item['lean']['scope'],'','声明：'+(', '.join('`'+d+'`' for d in item['lean']['declarations']) or '没有原式对应的 Lean 声明。'),'','报告：`'+str(item['lean'].get('report_path'))+'`。','']
 out+=['## 文字到 Lean 对照','',item['lean'].get('encoding_note','此原式尚无对应形式声明。'),'']
 for sm in item['lean'].get('step_map',[]):
  out+=['- '+sm['step_id']+'：`'+sm['declaration']+'`，`'+sm['source_path']+':'+str(sm['line'])+'`。'+sm['explanation'],'']
 out+=['## 边界说明','']
 for c in item['caveats']:out+=['- '+c,'']
 if item.get('original_proof_md'):out+=['## 原证明路线与本重写的关系','',item['original_proof_md'],'']
 return '\n'.join(out)
for s in [reconstruction,uniqueness]:(MATH/(s['id']+'.zh.md')).write_text(md(s)+'\n')
shared_by={p['id']:p for p in [reconstruction,uniqueness]}
for i in items:(MATH/(i['id']+'.zh.md')).write_text(md(i,shared_by.get(i.get('shared_proof_id')))+'\n')
print('math-content.json and 8 complete/pending Chinese Markdown files written')
