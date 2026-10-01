"""Finite-difference/MVT repair of the original full-space derivative cutoff proof."""
from pathlib import Path
import hashlib, json

BASE=Path('research/full-proof-integration-20260930/cvpr2023')
PAPER='iclr2024-sparse'
REF={'source_id':'src-iclr2024-sparse-main','version_id':'ver-iclr2024-sparse-formal','pdf_pages':[5,16],'section':'Assumption 1-β; Appendix B.2 Eq.(14)–(15)'}
report_path=BASE/'verification/derivative-report.json'
report=json.loads(report_path.read_text()) if report_path.exists() else None
fresh=bool(report and report['status']=='passed' and all(hashlib.sha256(Path(f['path']).read_bytes()).hexdigest()==f['sha256'] for f in report['source_files']))
decls={d['name']:d for d in report['declarations']} if fresh else {}
def refs(names):
    out=[]
    for name in names:
        d=decls.get(name)
        if d: out.append({'declaration':name,'source_path':d['source_path'],'line':d['line'],'scope':'actual_derivative_identity_or_mask_adapter','explanation_md':'真实偏导、有限差分或实际掩码声明；没有假设Taylor表示或待证交互消失。'})
    return out
def step(id,title,body,formula,names):
    return {'id':id,'title':title,'body_md':body,'formula_tex':formula,'justification':'','lean_refs':refs(names)}
defs=[{'id':'derivative-cutoff-objects','body_md':r'固定 $N=\{1,\ldots,n\}$、模型 $v:\mathbb R^n\to\mathbb R$、输入 $x$ 与输入基线 $r$。掩码在集合 $A$ 内取 $x_i$，其余取 $r_i$，定义 $g(A)=v(x_A)$、$b=g(\varnothing)$、$g_0(A)=g(A)-b$。原Sparse交互为 $I(A)=I_{g_0}(A)=\sum_{L\subseteq A}(-1)^{|A|-|L|}g_0(L)$，故 $I(\varnothing)=0$。$e_i$ 是坐标单位向量；$a_i=x_i-r_i$ 是第 $i$ 个坐标的实际掩码增量。'}]
steps=[
step('cutoff-classical-partials','把原混合导数的存在与顺序展开',r'经典偏导定义为 $D_i f(z)=\left.\frac{d}{dt}f(z+t e_i)\right|_{t=0}$。这等于把其余坐标固定、以第 $i$ 个坐标值为参数的普通导数。用非降序坐标列表 $(i_1,\ldots,i_q)$ 编码多重指标 $\kappa_i$：它等于列表中 $i$ 的出现次数，$q=\sum_i\kappa_i$。从左到右依次取偏导，定义 $P_0=v$、$P_j=D_{i_j}P_{j-1}$。原1-β的经典“混合导数存在且为零”要求相应前缀偏导沿下一坐标的导数真实存在，并给出 $P_q(z)=0$ 对全部 $z$。项目把这些存在条件与高阶零值一起编码在同一个1-β谓词中，只对原要求的 $q>M$ 列表使用它；没有另加所有低阶导数全局光滑的假设。原C1背景保留，但C1本身不保证高阶导数存在。原分母排写未另说明操作顺序，项目固定升序依次取导；如果采用反序约定，通用差分引理按同样的反序使用即可，不靠混合偏导换序。',r'P_j=D_{i_j}P_{j-1},\qquad q=\sum_{i\in N}\kappa_i.', ['Harsanyi.linePartial_coordinate_eq','Harsanyi.coordinate_multiIndex_total_order','Harsanyi.ClassicalMixedDerivativeCutoff']),
step('cutoff-difference-derivative','完整辅助引理：有限平移差分与真实坐标导数交换',r'定义有限差分 $\delta_{a,i}f(z)=f(z+a e_i)-f(z)$。如果 $f$ 沿坐标 $i$ 在每个点可微，则任何有限个平移后的加减也沿该坐标可微。平移不改变曲线导数：$D_i(f(\cdot+h))(z)=D_i f(z+h)$，因为 $(z+t e_i)+h=(z+h)+t e_i$。再由普通一元导数的差法则，得 $D_i(\delta_{a,j}f)=\delta_{a,j}(D_i f)$。对差分个数归纳，任意有限矩形差分都与这个真实偏导交换；这里只使用平移和有限加减，不使用高阶方向链式公式或无限级数。',r'D_i\bigl(\delta_{a,j}f\bigr)(z)=\delta_{a,j}(D_i f)(z).', ['Harsanyi.hasLineDerivatives_translate','Harsanyi.linePartial_translate','Harsanyi.linePartial_sub','Harsanyi.hasLineDerivatives_rectDifference','Harsanyi.linePartial_rectDifference']),
step('cutoff-mvt-induction','完整解析引理：混合偏导恒零使矩形差分恒零',r'对坐标列表长度 $q$ 归纳，并允许任意方向和任意实数步长。空列表时，矩形差分与零阶偏导都是 $f$；假设它恒零即得结论。对非空列表，先取第一个方向 $i_1$，其余差分记为 $R$。原前缀存在条件说明 $D_{i_1}f$ 沿剩余取导顺序可微，而其最终混合导数恒零。归纳假设给 $R(D_{i_1}f)=0$。上一辅助引理于是给 $D_{i_1}(Rf)=R(D_{i_1}f)=0$。对每个固定 $z$，一元函数 $H(t)=(Rf)(z+t e_{i_1})$ 在全实线上可微，且 $H\prime(t)=0$。一元均值定理推出 $H(a_{i_1})=H(0)$，即 $\delta_{a_{i_1},i_1}Rf(z)=0$。负步长、零步长都在全实线结论内，不需另加输入区间或正增量条件。',r'P_q\equiv0\ \Longrightarrow\ \delta_{a_{i_1},i_1}\cdots\delta_{a_{i_q},i_q}f\equiv0.', ['Harsanyi.deriv_line_eq','Harsanyi.rectDifference_zero_of_orderedPartial_zero']),
step('cutoff-mask-bridge','完整适配引理：矩形差分就是实际坐标掩码交互',r'把列表取为 $S$ 的不同坐标，步长为 $a_i=x_i-r_i$，起点为 $r$。对列表作归纳：空列表的值为 $v(r)=g(\varnothing)$，与原始交互空项相同。加入一个尚未出现的坐标 $i$，矩形差分分成起点平移 $a_i e_i$ 的剩余矩形与原起点的剩余矩形之差。在每个剩余子集 $U$ 上，因为 $i\notin U$，平移后的向量正是保留 $U\cup\{i\}$ 的坐标掩码；原向量是保留 $U$ 的掩码。两组交替和相减，正好是交互定义按含 $i$ 与不含 $i$ 配对的插入式。因此矩形差分与 $I_g(S)$ 相等，且整个引理适用于任意模型 $v$，没有先假设集合函数是多项式。',r'\left(\prod_{i\in S}\delta_{x_i-r_i,i}\right)v(r)=\sum_{U\subseteq S}(-1)^{|S|-|U|}v(x_U)=I_g(S).', ['Harsanyi.incrementCoordinates_insert','Harsanyi.rectDifference_coordinate_eq_interaction','Harsanyi.incrementCoordinates_baseline']),
step('cutoff-apply-beta','特取原1-β的一个高阶多重指标',r'设 $|S|\ge M+1$。按升序列出 $S$，每个坐标只出现一次，所以所选多重指标是 $\kappa_i=1$（$i\in S$）与 $\kappa_i=0$（$i\notin S$），总阶恰为 $|S|>M$。原1-β在全部展开点上给这一实际混合偏导的存在条件及恒零值。解析引理说明相应矩形差分为零，实际掩码适配引理再给 $I_g(S)=0$。步长只影响有限差分，不进入偏导的存在或零值前提；任意 $x,r$ 都适用。',r'\kappa_i=\mathbf1_{i\in S},\qquad |\kappa|=|S|>M\ \Longrightarrow\ I_g(S)=0.', ['Harsanyi.coordinate_multiIndex_finset','Harsanyi.orderedPartial_coordinate_amplitudes','Harsanyi.orderedPartialRegular_coordinate_amplitudes','Harsanyi.interaction_zero_of_classicalMixedDerivativeCutoff']),
step('cutoff-centered-source','接回原Sparse中心化交互及命题范围',r'$|S|>M\ge0$ 保证 $S\ne\varnothing$。减去输出基线 $b$ 的常数游戏只影响空交互，所以 $I_{g_0}(S)=I_g(S)=0$，得到原1-α。原作者B.2依赖Lemma1的无限Taylor形式；这里保留原式，另用全空间1-β下的有限差分路线修正其证明。一般Lemma1在未给定有效Taylor表示的读法下有独立问题；若把Eq.(2)当已给定有效表示，支撑分组是另一作用域。此修正不改那条独立Lemma的假设或结论。',r'|S|\ge M+1\ \Longrightarrow\ I(S)=I_{g_0}(S)=I_g(S)=0.', ['Harsanyi.centered_interaction_zero_of_classicalMixedDerivativeCutoff','FullSparseDerivative.assumption1beta_implies1alpha']),
step('cutoff-example','非零输出基线的二变量例子',r'取 $v(z_1,z_2)=5+2z_1-3z_2$，$M=1$。全部总阶至少2的经典混合导数恒零。任意输入 $x$ 和基线 $r$ 给 $I(\{1\})=2(x_1-r_1)$、$I(\{2\})=-3(x_2-r_2)$、$I(\{1,2\})=0$。输出基线 $b=5+2r_1-3r_2$ 一般不为零，但中心化空交互为零，高阶结论不受影响。', '', [])]
encoding=r'Lean的 `deriv` 是总函数；在不可微处也会返回一个默认值。因此仅写 `deriv=0` 不能编码原经典偏导为零。`ClassicalMixedDerivativeCutoff` 对每个原要求的高阶有序坐标列表，同时保存 `OrderedCoordinateRegular`（每个前缀沿下一坐标的真实可微性）与最终偏导在全空间为零。坐标重复次数就是原多重指标，两个计数引理实际验证总阶及特取支撑指标。论文adapter另保留原C1背景，不新增C∞、解析性、Taylor相等或多项式表示。'
names=['Harsanyi.interaction_zero_of_classicalMixedDerivativeCutoff','Harsanyi.centered_interaction_zero_of_classicalMixedDerivativeCutoff','FullSparseDerivative.assumption1beta_implies1alpha']
lean={'status':'verified' if fresh else 'not_yet_verified','compiled':fresh,'axiom_audit':'passed' if fresh else 'pending','declarations':names,'report_path':str(report_path),'scope':'entire original derivative-cutoff implication under the classical meaning that the stated global high-order mixed derivatives exist and are zero; actual arbitrary coordinate mask and source centering are included','encoding_note':encoding,'source_semantics_automatically_verified':False}
if fresh:
    first=decls[names[-1]]
    lean.update({'build_id':report['build_id'],'source_fingerprint':report['source_fingerprint'],'statement':first['signature'],'source_path':first['source_path'],'line':first['line'],'step_map':[{'step_id':s['id'],**r} for s in steps for r in s['lean_refs']]})
result={'id':'iclr2024-sparse-derivative-cutoff','paper_id':PAPER,'title':'Assumption 1-β ⇒ 1-α：用真实混合偏导和有限差分证明','kind':'unnumbered_implication','original_label':'Assumption 1-β ⇒ Assumption 1-α','inventory_ids':['derivative-cutoff'],'source_refs':[REF],
'statement_tex':r'\left[\forall z\in\mathbb R^n,\ \forall\kappa\in\mathbb N^n,\ |\kappa|\ge M+1:\ D^\kappa v(z)\text{存在且为}0\right]\ \Longrightarrow\ \forall S\subseteq N,\ |S|\ge M+1:\ I(S)=0',
'assumptions':[r'原C1函数背景；原1-β在全空间量化的高阶混合偏导按经典存在语义理解。前缀可微性是这些迭代偏导定义的展开，不能仅凭Lean总函数deriv的零值代替。',r'同一固定输入基线 $r$ 用于全部掩码；$M\in\mathbb N$。不添加解析性、无穷Taylor等式或多项式前提。'],
'definitions':defs,'overview':'全空间混合偏导恒零使相应矩形差分恒零；真实坐标掩码的交替和就是这一差分，再接回非空中心化交互。','proof_steps':steps,'shared_proof_ids':['shared-harsanyi-derivative-cutoff-mvt'],
'symbol_ids':['sym-model','sym-input','sym-input-baseline','sym-mask','sym-universe','sym-coalition','sym-game','sym-centered-game','sym-and-interaction','cutoff-order','mixed-derivative','sym-coordinate-direction','sym-coordinate-step','sym-coordinate-partial','sym-rectangular-difference'],
'notation_map':[{'original_tex':'b','canonical_tex':'r','relationship':'renaming','meaning':'原输入基线向量，非输出基线标量'},{'original_tex':'u(S)','canonical_tex':'g_0(S)','relationship':'same_definition'},{'original_tex':'I(S)','canonical_tex':'I_{g_0}(S)','relationship':'centered_variant'}],
'rewrite_status':'complete','completion_scope':lean['scope'],'alignment_status':'agent_checked_classical_derivative_semantics_with_ordering_convention','user_review_status':'pending','lean':lean,'related_issue_ids':['sparse-issue-taylor-validity'],'merge_policy':{'preserve_original_statement_and_proof_fields':True,'source_statement_tex_owner':'full_sparse_proofs_max'},'fix_authorization':'proof_only_granted','statement_fix_authorization':'not_granted','source_proof_correction_note_md':'保留原Eq.(14)–(15)和其Lemma1依赖；有限差分/MVT是同一原命题的修正证明，未将一般Lemma1改成解析性版本。'}
shared={'id':'shared-harsanyi-derivative-cutoff-mvt','title':'共享完整证明：真实混合偏导零与矩形有限差分','statement_tex':result['statement_tex'],'assumptions':result['assumptions'],'definitions':defs,'overview':result['overview'],'proof_steps':steps[:-1],'rewrite_status':'complete','alignment_status':result['alignment_status'],'user_review_status':'pending','lean':{**lean,'declarations':['Harsanyi.rectDifference_zero_of_orderedPartial_zero','Harsanyi.interaction_zero_of_classicalMixedDerivativeCutoff']}}
symbol_specs=[('sym-coordinate-direction','e_i',r'(e_i)_j=\mathbf1_{i=j}','坐标单位向量','ℝⁿ'),('sym-coordinate-step','a_i',r'a_i=x_i-r_i','实际坐标差分步长','ℝ，可正可负或零'),('sym-coordinate-partial','D_i',r'D_i f(z)=\left.\frac{d}{dt}f(z+t e_i)\right|_{t=0}','经典坐标偏导','模型及各前缀偏导→实值函数'),('sym-rectangular-difference',r'\delta_{a,i}',r'\delta_{a,i}f(z)=f(z+a e_i)-f(z)','有限平移差分','实值函数→实值函数')]
symbols=[]
for id,tex,definition,name,type_ in symbol_specs:
    symbols.append({'id':id,'canonical_id':id,'canonical_tex':tex,'name_zh':name,'definition_tex':definition,'description_md':'项目有限差分修正路线的规范辅助符号；不是静默替换原作者符号。','type_or_domain':type_,'scope':'derivative cutoff repair only','assumptions':['经典偏导的使用需要真实存在；有限差分本身不需要可微。'],'empty_set_convention':'空列表有限差分为原函数；论文高阶目标非空。','baseline_convention':'输入基线r任意；非空中心化交互等于原始交互。','aliases':[],'paper_mappings':[{'paper_id':PAPER,'version_id':REF['version_id'],'original_tex':None,'original_definition_tex':None,'relation_type':'derived_quantity','source_id':REF['source_id'],'pdf_pages':REF['pdf_pages'],'scope':'project proof repair auxiliary; not author notation'}],'lean_names':{'sym-coordinate-direction':['Harsanyi.coordinateDirection'],'sym-coordinate-step':['Harsanyi.coordinateMoves'],'sym-coordinate-partial':['Harsanyi.linePartial'],'sym-rectangular-difference':['Harsanyi.rectDifference']}[id],'version':'full-paper-20260930'})
md='# '+result['title']+'\n\n'+defs[0]['body_md']+'\n\n'+result['overview']+'\n\n'
for s in steps:
    md+='## '+s['title']+'\n\n'+s['body_md']+'\n\n'
    if s['formula_tex']:md+=r'\['+s['formula_tex']+r'\]'+'\n\n'
md+='## 形式编码与来源边界\n\n'+encoding+'\n'
rewrite_path=BASE/'math/derivative-cutoff-mvt.zh.md'
rewrite_path.write_text(md)
result['rewrite_path']=str(rewrite_path)
out={'paper_id':PAPER,'results':[result],'shared_proofs':[shared],'symbols':symbols,'issues':[],'merge_policy':'replace derivative-cutoff project rewrite/Lean only; retain Sparse owner complete author statement/proof transcription and all original issue records','verification_status':lean['status']}
(BASE/'derivative-cutoff-results.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print('derivative cutoff rewrite complete; Lean',lean['status'])
