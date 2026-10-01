"""Nine finite-combination targets; source transcriptions remain owned by the UI/source agent."""
from pathlib import Path
import json

BASE=Path('research/full-proof-integration-20260930/cvpr2023')
PAPER='iclr2024-generalizable'
REF={'source_id':'src-iclr2024-generalizable-main','version_id':'ver-iclr2024-generalizable-formal'}
CVPR=json.loads((BASE/'content.json').read_text())
shared=[];results=[]
def step(id,title,body,formula='',justification=''):
    return {'id':id,'title':title,'body_md':body,'formula_tex':formula,'justification':justification,'lean_refs':[]}
DEFS=[{'id':'f11-coordinate-objects','body_md':r'固定 $N=\{1,\ldots,n\}$、模型 $v:\mathbb R^n\to\mathbb R$、样本 $x$ 和同一个输入基线 $r$。记 $g(A)=v(x_A)$，$b=g(\varnothing)$。对已掩码样本 $x_T$ 再掩码，记 $g_T(A)=v((x_T)_A)$。AND为 $I_g(S)=\sum_{L\subseteq S}(-1)^{|S|-|L|}g(L)$。OR对非空S为 $O_g^N(S)=-I_{g^c}(S)$，其中 $g^c(L)=g(N\setminus L)$；单独规定 $O_g^N(\varnothing)=g(\varnothing)$。空集不能沿用非空OR公式。所有子集求和包括空集。'}]
def add(id,title,label,pages,statement,steps,names,shared_ids=None,assumptions=None,overview='',scope='entire original finite-algebra statement'):
    r={'id':id,'paper_id':PAPER,'title':title,'kind':'finite_theorem_or_derivation','original_label':label,'inventory_ids':[id],
      'source_refs':[{**REF,'pdf_pages':pages}],'statement_tex':statement,'assumptions':assumptions or [r'有限N；固定同一个坐标基线r、样本x和模型；不存在原始输出零基线假设。'],
      'definitions':DEFS,'overview':overview,'proof_steps':steps,'shared_proof_ids':shared_ids or [],
      'symbol_ids':['sym-model','sym-input','sym-input-baseline','sym-mask','sym-universe','sym-coalition','sym-game','sym-output-baseline','sym-and-interaction','sym-or-interaction'],
      'notation_map':[{'original_tex':r'I_{and}(S\mid x)','canonical_tex':'I_g(S)','relationship':'same_definition'},{'original_tex':r'I_{and}(S\mid x_T)','canonical_tex':'I_{g_T}(S)','relationship':'derived_quantity'},{'original_tex':r'I_{or}(S\mid x_T)','canonical_tex':r'O_{g_T}^N(S)','relationship':'derived_quantity'}],
      'rewrite_status':'complete','completion_scope':scope,'alignment_status':'agent_checked_full_statement','user_review_status':'pending',
      'source_transcription_owner':'reader_multipage_v2_max','merge_policy':{'preserve_original_statement_and_proof_fields':True},
      'lean':{'status':'not_yet_verified','declarations':names,'scope':scope,'report_path':str(BASE/'verification/report.json')},'related_issue_ids':[]}
    results.append(r)
    md='# '+title+'\n\n'+DEFS[0]['body_md']+'\n\n'+r'\['+statement+r'\]'+'\n\n'
    for s in steps:
        md+='## '+s['title']+'\n\n'+s['body_md']+'\n\n'
        if s['formula_tex']:md+=r'\['+s['formula_tex']+r'\]'+'\n\n'
    (BASE/'math'/f'{id}.zh.md').write_text(md)
    r['rewrite_path']=str(BASE/'math'/f'{id}.zh.md')
    return r

MASK_STEPS=[step('f11-mask-comp','完整掩码合成引理',r'固定坐标i，若i同时属于T和L，两次掩码都保留xi；若i不属于L，第二次直接给ri；若i属于L但不属于T，第一次已经给ri，第二次保留的仍是ri。因此两个向量的每个坐标相同，得到 $(x_T)_L=x_{T\cap L}$。输入基线必须是同一个r，不能在二次掩码时按新样本重学。',r'g_T(L)=g(T\cap L).'),step('f11-mask-zero-pair','选出已被遮掉的变量并配对子集',r'若S不包含于T，取 $i\in S\setminus T$。对每个 $U\subseteq S\setminus\{i\}$，因i不在T，有 $T\cap(U\cup\{i\})=T\cap U$，故两次掩码输出相同。交互和中对应的U和U∪{i}符号相反，值相同，逐对消去得0。此证明不假设模型线性，也不要求 $g(\varnothing)=0$。',r'S\not\subseteq T\ \Longrightarrow\ I_{g_T}(S)=0.'),step('f11-mask-boundary','空集和未掩码边界',r'S空集永远包含于T，消失命题不包括空交互；它是b。若T=N，所有变量未被遮掉，条件S不包含于T不发生。若T空而S非空，全部含变量交互都被配对消去。')]
add('f11-and-mask-zero','掩码消失：含已遮掉变量的AND交互为零','Section 2.1',[2],r'S\not\subseteq T\ \Rightarrow\ I_{and}(S\mid x_T)=0',MASK_STEPS,['Harsanyi.maskCoordinates_comp','Harsanyi.and_mask_interaction_zero','FullGeneralizable.and_mask_zero'],overview='同一基线的两次掩码等于集合交集；已缺失变量使子集对的输出相同而符号相反。')

DUAL_STEPS=[step('f11-dual-game','明确反转状态的集合函数',r'把原样本中“保留”与“使用基线”两个状态交换，新的集合函数是 $g^c(L)=g(N\setminus L)$。这里反转的是有限状态索引，不是把原模型改成另一个模型。'),step('f11-dual-definition','逐项对比非空OR与AND定义',r'对非空S，原OR式的每项正好是 $g^c(L)$ 的AND变换，并整体多一个负号。它们数值可正可负，稀疏性绝对值相同。空集另规定OR基线为g空；负AND变换在空集为−g(N)，一般不同，故必须分开。',r'O_g^N(S)=-I_{g^c}(S)\qquad(S\ne\varnothing).'),step('f11-dual-example','二变量与空集例子',r'N={1,2}、g空7,g1=8,g2=9,g12=13。反转游戏的两单变量AND值为−4和−5，二阶为3；OR值为4,5,−3，空OR基线单独为7。反转AND的空值13，不能拿其负值−13代替7。')]
add('f11-or-duality','OR对偶：反转掩码状态的负AND变换','Section 2.1; footnote 5',[3],r'O_g^N(S)=-I_{g^c}(S),\qquad g^c(L)=g(N\setminus L),\ S\ne\varnothing',DUAL_STEPS,['Harsanyi.or_dual','FullGeneralizable.or_duality'],overview='非空OR定义就是补集游戏的负Möbius变换；空集采用作者另外规定的基线值。',scope='nonempty OR duality with explicit separate empty convention; does not prove sparsity inheritance assumptions')

EXACT_STEPS=[step('f11-exact-adapt','适配原始AND定义',r'固定x和r后，论文 $I_{and}(A\mid x)$ 就是 $I_g(A)$。它采用原始输出，空集为b。'),*next(x['proof_steps'] for x in CVPR['results'] if x['id']=='cvpr2023-reconstruction')[1:]]
add('iclr2024-generalizable-theorem1','Theorem 1精确部分：全部掩码的AND重构','Theorem 1 exact equality',[3,12,15],r'\forall T\subseteq N,\quad v(x_T)=\sum_{S\subseteq T}I_{and}(S\mid x)',EXACT_STEPS,['FullGeneralizable.exact_and_reconstruction'],['proof-finite-mobius-reconstruction-v2'],overview='原始AND变换含空集系数。所有子集的有限消去留下当前掩码输出，精确部分不依赖稀疏假设。',scope='exact equality component of original Theorem1; approximate/sparsity clause remains a separate inventory target')

AND_STEPS=[step('f11-and-coeff-align','固定x与字面xT条件系数的对齐',r'对S子集T，每个L子集S也包含于T。掩码合成 $(x_T)_L=x_{T\cap L}=x_L$，所以 $I_{and}(S\mid x_T)=I_{and}(S\mid x)$。这解释附录原AND推导为何使用固定x，也补足父定理字面条件系数的联系，不改父式。'),step('f11-and-reconstruct','应用完整有限重构并核前提',r'对集合函数 $g_{and}(L)=v_{and}(x_L)$ 用公共重构，得到 $\sum_{S\subseteq T}I_{g_{and}}(S)=g_{and}(T)$。或者直接对条件函数 $g_{and,T}$ 重构于T，再由掩码幂等 $(x_T)_T=x_T$ 得同值。两种路线中的空集值均为 $v_{and}(x_\varnothing)$。',r'\sum_{S\subseteq T}I_{and}(S\mid x_T)=\sum_{S\subseteq T}I_{and}(S\mid x)=v_{and}(x_T).'),step('f11-and-empty','空集边界',r'T空集时唯一S空，左右都是AND分量输出基线；没有隐藏的零基线条件。')]
add('iclr2024-generalizable-and','Appendix C(1)：固定样本与字面条件AND重构','Appendix C(1)',[12,13],r'v_{and}(x_T)=\sum_{S\subseteq T}I_{and}(S\mid x)=\sum_{S\subseteq T}I_{and}(S\mid x_T)',AND_STEPS,['FullGeneralizable.exact_and_reconstruction','FullGeneralizable.literal_and_coefficient_eq','FullGeneralizable.literal_and_reconstruction'],['proof-finite-mobius-reconstruction-v2'],overview='先用掩码交集解释两种条件系数一致，再逐项复用完整有限重构。')

OR_STEPS=[step('f11-or-literal-game','保持字面条件样本并修正原代入',r'固定当前T，令 $h(L)=v_{or}((x_T)_L)=v_{or}(x_{T\cap L})$。原父式的OR系数是对h的OR变换。补集项必须为 $h(N\setminus L)=v_{or}(x_{T\setminus L})$；原第13页逐项代入 $v_{or}(x_{N\setminus L})$ 一般不相等，原错式另保留在问题记录。'),step('f11-or-filter','完整辅助引理：相交子集族是两个子集族之差',r'T子集N。对每个S子集N，$S\cap T=\varnothing$ 当且仅当 $S\subseteq N\setminus T$，所以相交子集恰为 $\mathcal P(N)\setminus\mathcal P(N\setminus T)$。后者族包含于前者，有限求和为全和减去不相交和。空集一直在两个全族中，不在相交族。',r'\sum_{\substack{S\subseteq N\\S\cap T\ne\varnothing}}d_S=\sum_{S\subseteq N}d_S-\sum_{S\subseteq N\setminus T}d_S.'),step('f11-or-transform','对补集负游戏作两次重构',r'令 $f(L)=-h(N\setminus L)$。每个非空S的OR系数等于I_f(S)，由有限求和对整体负号的线性性。相交族没有空S，所以可逐项替换。两次公共重构给 $f(N)-f(N\setminus T)=-h(\varnothing)+h(T)$，这里使用 $N\setminus(N\setminus T)=T$，需要并已核T子集N。',r'\sum_{S\cap T\ne\varnothing}O_h^N(S)=h(T)-h(\varnothing)=v_{or}(x_T)-v_{or}(x_\varnothing).'),step('f11-or-baseline','单独加回原空OR基线',r'作者规定 $O_h^N(\varnothing)=h(\varnothing)=v_{or}(x_\varnothing)$。把它加回相交和即可得到 $v_{or}(x_T)$。T空时相交族为空，差值0，最终只有基线；T=N时覆盖完整输入。这同时避免原case1/2在T空时重复计数。'),step('f11-or-example','带非零基线的二变量检验',r'使用g空7,g1=8,g2=9,g12=13，固定x的OR系数为4,5,−3，空7。T={1}时激活OR{1}及{1,2}，4−3+7=8；T空无非空激活，只剩7；T=N给4+5−3+7=13。字面hT也分别重构相同目标，但不要求每个OR系数都等于固定x系数。')]
or_result=add('iclr2024-generalizable-or','Appendix C(2)：OR完整重构与原证明修正','Appendix C(2); Eq.(9)',[13,14],r'v_{or}(x_T)=O_{g_{or,T}}^N(\varnothing)+\sum_{\substack{S\subseteq N\\S\cap T\ne\varnothing}}O_{g_{or,T}}^N(S)',OR_STEPS,['Harsanyi.activated_subset_sum','Harsanyi.or_reconstruction','Harsanyi.maskCoordinates_complement','FullGeneralizable.literal_or_reconstruction','FullGeneralizable.literal_or_nonempty_sum'],['shared-harsanyi-or-reconstruction'],overview='相交集合族等于全部子集去掉不相交子集；两个精确重构值相减，再单独加回OR基线。')
shared.append({'id':'shared-harsanyi-or-reconstruction','title':'共享证明：OR补集变换的精确重构','statement_tex':r'g(T)=O_g^N(\varnothing)+\sum_{S\subseteq N,\,S\cap T\ne\varnothing}O_g^N(S)','assumptions':['T⊆N；有限集合函数g；OR空集单列g空。'],'definitions':DEFS,'proof_steps':OR_STEPS[1:4],'rewrite_status':'complete','alignment_status':'agent_checked_full_statement','user_review_status':'pending','lean':{'status':'not_yet_verified','declarations':['Harsanyi.activated_subset_sum','Harsanyi.or_reconstruction'],'report_path':str(BASE/'verification/report.json')}})

PARENT_STEPS=[MASK_STEPS[0],step('f11-parent-decompose','同一掩码上的原分解',r'原假设是在全部原掩码上 $v(x_U)=v_{and}(x_U)+v_{or}(x_U)$。不要求本轮实现某种学习算法，也不增加两分量的唯一性、稀疏性或符号假设。固定T可代入该分解。'),*AND_STEPS[:2],*OR_STEPS[:4],step('f11-parent-add','相加得到父定理字面式',r'AND部分重构 $v_{and}(x_T)$，OR部分重构 $v_{or}(x_T)$。两个空项相加为原输出基线 $v(x_\varnothing)$；所有系数仍按字面xT条件定义。因此相加恰为v(xT)，不把父量词改成仅固定x的选择性子结论。',r'v(x_T)=\sum_{S\subseteq T}I_{and}(S\mid x_T)+\sum_{S\in\{S\subseteq N:S\cap T\ne\varnothing\}\cup\{\varnothing\}}I_{or}(S\mid x_T).')]
parent=add('iclr2024-generalizable-andor','Theorem 2：完整字面AND-OR联合匹配','Theorem 2; Eq.(3),(7)',[3,12,13,14],PARENT_STEPS[-1]['formula_tex'],PARENT_STEPS,['FullGeneralizable.literal_and_or_reconstruction'],['proof-finite-mobius-reconstruction-v2','shared-harsanyi-or-reconstruction'],[r'对全部 $U\subseteq N$，$v(x_U)=v_{and}(x_U)+v_{or}(x_U)$；同一坐标掩码基线；T子集N。'],overview='通过同一基线的掩码合成处理字面xT条件，再把两分量的精确重构相加。')

BOOL_STEPS=[step('f11-boolean-truth','完整二变量OR恒等式',r'把布尔变量视为0/1实数。对(x4,x5)四种赋值(0,0),(1,0),(0,1),(1,1)，右侧 $x_4+x_5-x_4x_5$ 分别为0,1,1,1，恰是OR输出。',r'x_4\lor x_5=x_4+x_5-x_4x_5.'),step('f11-boolean-expand','保持三个共同AND项并展开OR',r'把该恒等式代入原五变量函数，三个AND项不变，得到六个不同变量集合：{1,2,3},{2,3},{3,4},{4},{5},{4,5}，最后系数−1，其余+1。另一分解保持三个AND项，并将{4,5}作为一个OR项。二者逐点相同，没有声称这两种分解是唯一或全局最优。',r'f(x)=x_1x_2x_3+x_2x_3+x_3x_4+x_4+x_5-x_4x_5.'),step('f11-boolean-support','完整输入下的真实交互支持',r'输入全1且基线0时，六个AND乘积项分别是纯AND函数，其系数由公共分布与线性性严格给出。另一路三个AND支持如上、纯OR{4,5}支持一个非空OR系数1；纯OR性质由补集游戏是常数1减纯AND直接证明。输入全0/空掩码两式都0；完整输入两式都4。')]
add('f11-boolean-decomposition','五变量布尔函数：两种精确AND-OR分解','Section 2.2 Challenge 1',[4],r'x_1\land x_2\land x_3+x_2\land x_3+x_3\land x_4+x_4\lor x_5=x_1x_2x_3+x_2x_3+x_3x_4+x_4+x_5-x_4x_5',BOOL_STEPS,['FullGeneralizable.boolean_or_additive','FullGeneralizable.boolean_decomposition','Harsanyi.orInteraction_unanimity','FullCvpr.addmul_coordinate_adapter'],overview='二变量布尔OR等于加法减去共同AND，代入后得到逐点相同而支持项不同的两种分解。',assumptions=['xi∈{0,1}；0输入基线用于交互支持说明；整个函数代数恒等式对全部五个布尔变量成立。'])

SHAPLEY_SHARED=next(x for x in CVPR['shared_proofs'] if x['id']=='shared-harsanyi-shapley-dividend')
SHAPLEY_STEPS=[step('f11-shapley-component','核对是原模型的AND交互',r'Theorem3的 $I_{and}(S\mid x)$ 用函数v自身的原始AND定义；不是任意学习分解中 $v_{and}$ 的系数。取 $g(A)=v(x_A)$，i属于N，经典Shapley前提与共有证明相同。'),*SHAPLEY_SHARED['proof_steps'],step('f11-shapley-reindex','把环境子集换成含i的交互集合',r'共有结论索引U子集N\{i}。映射S=U∪{i}一一对应N中全部含i子集，逆映射U=S\{i}，且 $|S|=|U|+1$。逐项重编号就得到原分母|S|。空S不含i，不参与分配。',r'\phi_g(i)=\sum_{U\subseteq N\setminus\{i\}}\frac{I_g(U\cup\{i\})}{|U|+1}=\sum_{S\subseteq N:i\in S}\frac{I_g(S)}{|S|}.')]
add('f11-shapley','Theorem 3：原模型AND交互与经典Shapley','Theorem 3 (external Harsanyi 1963)',[15],r'\phi_g(i)=\sum_{S\subseteq N:i\in S}\frac{I_{and}(S\mid x)}{|S|}',SHAPLEY_STEPS,['Harsanyi.factorialShapley_eq_dividendAllocation','FullGeneralizable.shapley'],['shared-harsanyi-shapley-dividend'],overview='经典边际阶乘定义先变为等分交互；把外部环境子集与含i的交互集合一一对应，得到作者外引公式。',scope='entire external Shapley statement using the original model v AND coefficients; this paper has no author proof')

COUNT_STEPS=[step('f11-count-bijection','每个变量的两种状态与子集一一对应',r'一个掩码设置对每个i选择保留或基线。保留变量的集合S唯一表示该设置；反过来每个S子集N定义一个设置。因此n个独立二值选择有 $2^n$ 个掩码设置，也即 $|\mathcal P(N)|=2^n$。这里计数的是设置，即使xi=ri导致不同设置生成相同向量，仍可枚举2^n个。'),step('f11-count-queries','完整枚举方案的模型查询数',r'若方案对每个掩码设置查询一次同一模型，恰有2^n次调用；m模型各枚举一次则m2^n次。这是全部模式预计算输出的查询计数，不是完整学习、变换和梯度优化的运行时间证明。交互变换后续算术或设备批处理可改变实际时间。'),step('f11-count-boundary','n为零与六变量原例',r'n=0时唯一空设置，计数1=2^0；n=6时64个设置。原G的时间表属于实测，不能从子集计数推出45.14秒等具体时间。')]
add('f11-mask-complexity','全部掩码设置与枚举模型查询计数','Appendix G',[3,16,17,20,22,23],r'|\mathcal P(N)|=2^{|N|}=2^n',COUNT_STEPS,['FullGeneralizable.mask_count'],overview='掩码设置与变量子集一一对应，给出2^n计数；一次逐掩码查询方案因此有2^n调用。',scope='mask-set cardinality and one-query-per-mask count; not a total training or interaction-computation time bound')

issue={'id':'issue-f11-or-intermediate-20260930','paper_id':PAPER,'title':'OR原证明的分类中间零和、条件输出代入及空掩码重合','category':'proof_case_and_mask_alignment_errors','source_refs':[{**REF,'pdf_pages':[13,14],'section':'Appendix C(2); Eq.(9)'}],
'original_formula_tex':r'\sum_{S:S\cap T\ne\varnothing}I_{or}(S\mid x_T)=\sum_{S:S\cap T\ne\varnothing}\left[-\sum_{L\subseteq S}(-1)^{|S|-|L|}v_{or}(x_{N\setminus L})\right]',
'evidence_md':r'第13页该首代入式不保留二次掩码。取N={1,2}、T={1}、$g(A)=\mathbf1_{N\subseteq A}$、S=N。字面条件游戏hT全零，所以OR系数左0；原右−1。正确逐项输出是 $v_{or}((x_T)_{N\setminus L})=v_{or}(x_{T\setminus L})$。第14页case(3)以 $\sum_{j=0}^{|T|-|T\cap L|}\binom{|T|-|T\cap L|}j(-1)^j=0$ 作内层消去，但T子集L时上界0，和1；例如N={1,2},T=L={1}。完整外层仍能消去，但原标注内零不成立。case(4)激活要求在T新增至少一个变量，原下界印0，应分别核实际索引族；T空时case(1) L=N\T与case(2)L=N重合，不能重复计同一项。',
'impact_md':'错误属于原证明的中间分类和条件式代入；原OR及AND-OR父命题不变。修正证明使用相交子集族差及完整Möbius重构，包含T空，逐项保留literal conditioned sample。',
'related_result_ids':['iclr2024-generalizable-or','iclr2024-generalizable-andor'],'original_statement_status':'no_counterexample_found; proof repaired without changing statement',
'user_confirmation':'not_individually_reviewed','fix_authorization':'proof_only_granted','statement_fix_authorization':'not_granted','status':'proof_repaired_formal_audit_pending','user_review_status':'pending'}
or_result['related_issue_ids']=[issue['id']];parent['related_issue_ids']=[issue['id']]

out={'paper_id':PAPER,'results':results,'shared_proofs':shared,'issues':[issue],'symbols':[],
 'merge_policy':'replace project rewrite and Lean metadata; preserve UI/source agent complete original_statement_md/original_proof_md TeX transcriptions',
 'counts':{'finite_targets':9,'rewrite_complete':9,'lean_pending_audit':9}}
(BASE/'generalizable-finite-results.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print('Generalizable finite fragment:',len(results),'targets')
