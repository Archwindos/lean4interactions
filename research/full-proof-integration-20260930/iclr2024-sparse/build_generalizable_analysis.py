import json
from pathlib import Path
BASE=Path('research/full-proof-integration-20260930/iclr2024-sparse')
GB=Path('research/full-proof-integration-20260930/iclr2024-generalizable')
inv=json.loads((GB/'inventory.json').read_text())
entries={e['id']:e for e in inv['entries']}
results=[]

def result(key, statement, assumptions, symbols, stages, scope, status='complete', shared=None, lean=None, issue=None, statement_status='same_original_mathematical_target'):
    eid='f11-'+key;e=entries[eid]
    refs=[]
    for p in sorted({x['pdf_page'] for x in e['statement_locations']}|{q for x in e['proof_ranges'] for q in range(x['start_pdf_page'],x['end_pdf_page']+1)}):
        refs.append({'source_id':'src-iclr2024-generalizable-main','pdf_page':p,
          'text_path':str(GB/'source-review'/'all-pages.txt'),
          'page_text_json_path':'research/paper-survey-20260930/recent/text/iclr2024-generalizable.pages.json',
          'image_path':str(GB/'source-review'/f'page-{p:02d}.png')})
    results.append({'id':eid,'paper_id':'iclr2024-generalizable','title':e['title'],'kind':e['kind'],'original_label':e['original_label'],
      'inventory_ids':[eid],'source_refs':refs,'statement_tex':statement,'assumptions':assumptions,'definitions':symbols,'symbol_ids':symbols,
      'overview':scope,'proof_steps':[{'id':eid+'-step-'+str(i+1),'title':t,'body_md':b,'formula_tex':f,'justification':j,'lean_refs':[]} for i,(t,b,f,j) in enumerate(stages)],
      'shared_proof_ids':shared or [],'rewrite_status':status,'alignment_status':'agent_checked_formal_source_scope',
      'user_review_status':'pending','completion_scope':scope,'statement_status':statement_status,
      'lean':lean or {'status':'not_formalized','verification_role':'none','completion_scope':'No complete Lean claim for this original target'},
      'related_issue_ids':issue or [],'notation_map':[{'source':'v(x_T)','canonical':'g(T)','meaning':'fixed input and fixed baseline masked-output game; g(∅) unrestricted'}]})

core=['sym-model','sym-input','sym-input-baseline','sym-mask','sym-universe','sym-coalition','sym-game','sym-output-baseline']
result('external-sparsity',r'|\Omega_{\rm salient}|\ll 2^n', ['原文well-trained DNN表述；外引Ren et al. (2024)的三条件，而非本篇新形式前提'],core+['sym-and-interaction','sym-threshold','sym-significant-set'],[
 ('外引范围','正文p3与附录B p12转述稀疏性。附录B第一条件精确要求全空间高于M阶的输出混合导数全部为零（Sparse的1β），经1β⇒1α映到高阶交互精确零；其余两条件是平均输出单调和遮挡平均输出的多项式下界；本篇没有重新证明这些条件蕴含某个定量稀疏率。对应Sparse论文的精确T2/T3及其Case1范围保留为跨文来源。',r'\Omega=\{S:|I(S)|>\tau\}','正式外引与三条件逐项定位'),
 ('可用结论边界','不能把well-trained这个经验描述自行定义成新的数学谓词，然后假设一个足以推出稀疏性的强性质。也不能将Sparse有限n计数界直接升级为对所有网络的严格渐近≪结论。本项目完成来源与条件说明，仍明确本篇无独立原证明。','','外引审校；非新增定理')], '完整外引条件与数学适用范围说明；本篇未提供独立可形式化的定量稀疏命题。',statement_status='external_qualitative_claim_no_local_proof')
result('theorem1-approx',r'v(x_S)\approx\sum_{T\subseteq S:T\in\Omega}I_{\rm and}(T\mid x)',[],core+['sym-and-interaction','sym-threshold','sym-significant-set'],[
 ('分离精确与近似子句','Theorem1的精确全交互重构由有限Möbius恒等式支持，公共证明完整。其少量显著交互≈子句外引Sparse理论与经验稀疏，没有规定统一精度。原approx求和含空集当且仅当∅∈Ω，不能无条件另加基线。令Ω为保留族，raw交互I(∅)=g(∅)，精确重构给含空集在内的遗漏项之和；这解释近似依赖，但没有自动认证其大小。',r'g(S)-\sum_{T\subseteq S:T\in\Omega}I_g(T)=\sum_{T\subseteq S:T\notin\Omega}I_g(T)','有限索引族分组与完整重构'),
 ('近似语义','原文没有给ε或统一误差上界，也没有把“few salient”量化。项目不新增误差前提或将该子句换为阈值误差定理；实验匹配图与外引严格界另列。','','≈原义与来源边界')], '近似子句完整解释，不宣称未量化的原≈与≪已成为完整Lean定理。',shared=['proof-finite-mobius-reconstruction-v2'],statement_status='unquantified_approximation_external_component')
result('proposition1',r'v(x_T)\approx v(x_\varnothing)+\sum_{\varnothing\ne S\subseteq T:S\in\Omega_{\rm and}}I_{\rm and}(S\mid x_T)+\sum_{S\cap T\ne\varnothing:S\in\Omega_{\rm or}}I_{\rm or}(S\mid x_T)', ['原well-trained表述不改写为项目新前提'],core+['sym-and-output','sym-or-output','sym-and-component-interaction','sym-or-interaction','sym-significant-set','sym-conditional-interaction'],[
 ('全部交互精确匹配','原式的条件输入x_T不能丢失。固定同一模型分量vand+vor=v与同一输入基线，定义g^T(L)=v(x_(T∩L))，gand^T(L)=vand(x_(T∩L))，gor^T(L)=vor(x_(T∩L))；这来自重复掩码的交集恒等式。令Iand^T、Ior^T分别为这些条件游戏在同一总体N上的raw AND/OR变换，即原I(S|x_T)。对AND，只保留S⊆T；OR激活族取S∩T≠∅并加原空集项。全部条件游戏在空集的分量和为v(x∅)，在T上的分量和为v(xT)，所以原literal Theorem2精确匹配成立。不能把OR逐项系数Ior^T换成未掩码输入Ior。',r'v(x_T)=v(x_\varnothing)+\sum_{\varnothing\ne S\subseteq T}I_{\rm and}^{T}(S)+\sum_{S\cap T\ne\varnothing}I_{\rm or}^{T}(S)','本篇Theorem2的完整共享证明'),
 ('显著族截断的实际余项','从上式分别移除Ωand、Ωor外的项，误差恰为两组条件交互的遗漏和；每个T的系数族I^T都保持原条件输入。作者要求两显著族≪2^n且能近似所有掩码，但未给本篇独立定量推导；对所有任意分解，精确重构本身不保证这两个余项小。',r'\text{error}(T)=\sum_{\varnothing\ne S\subseteq T:S\notin\Omega_{\rm and}}I_{\rm and}^{T}(S)+\sum_{S\cap T\ne\varnothing:S\notin\Omega_{\rm or}}I_{\rm or}^{T}(S)','有限分组；不补误差或稀疏假设')], '原命题近似与小族主张仍属未量化来源；完整解释其精确依赖与遗漏项，不声称泛化稀疏已严格证明。',shared=['shared-harsanyi-or-reconstruction','proof-finite-mobius-reconstruction-v2'],statement_status='unquantified_approximation_no_local_proof')
result('reparameterization',r'g_{\rm and}(T)=\tfrac12g(T)+\gamma_T,\quad g_{\rm or}(T)=\tfrac12g(T)-\gamma_T', [],core+['sym-and-output','sym-or-output','sym-decomposition-parameter'],[
 ('由参数得到分解','固定输入、模型与掩码基线，取任意实数族γT。逐个T相加，+γT和−γT抵消，故两分量之和是原g(T)，包括空集和未中心化输出基线。',r'(g(T)/2+\gamma_T)+(g(T)/2-\gamma_T)=g(T)','实数加法恒等式'),
 ('由分解恢复唯一参数','若给定任意分量a(T)+b(T)=g(T)，取γT=(a(T)−b(T))/2。代入得到a=g/2+γ及b=g/2−γ。任一参数若满足第一等式，必为a−g/2，因此γ唯一。全体掩码逐点证明给集合函数的一一重参数，不依赖优化成功。',r'\gamma_T=(a(T)-b(T))/2=a(T)-g(T)/2','实数恒等式与函数外延'),
 ('多模型适配','对每个模型i独立使用同一论证，得到γT^(i)和分量；此时γ模型索引不是共享γ，保留后续共同/个体参数约束的区别。','','逐模型全称化')], '全部掩码、任意模型输出与任意分解的一一重参数证明。')
result('rowmax-penalty',r'\operatorname{rowmax}(A)_S=\max_{1\le i\le m}|A_{S,i}|', ['有限m≥1模型；固定行S'],core+['sym-model-count','sym-interaction-matrix','sym-rowmax','sym-entrywise-l1'],[
 ('原行范数','p6定义每行ℓ∞，所以行惩罚是R=max_i|a_i|≥0。若模型j的交互强度已达到R，而其他模型交互强度改变后仍不超过R且j保持该值，新的最大值≤R；保留的j项又给最大值≥R。',r'|a_j|=R,\quad |b_j|=R,\quad\forall i\ |b_i|\le R\quad\Rightarrow\quad\max_i|b_i|=R','有限最大值的上下界'),
 ('总损失的局部不变性','只改变该行、保持其他行时，rowmax向量该坐标不变，因此其ℓ1和不变。这是作者“other models without a penalty”的精确含义；它允许该行的其他值在强度R以内变化，不限制符号。',r'\sum_S\max_i|A_{S,i}|\text{ unchanged}','有限求和逐坐标相等'),
 ('优化解释边界','原文说该目标鼓励共享稀疏集合，这是一种优化设计解释。上述平坦区性质没有证明每个最优解具有相同支撑，也没有保证训练得到的交互跨模型泛化；不追加这种全局结论。','','局部代数性质与经验主张分别呈现')], '原行ℓ∞惩罚的全部有限模型局部不变性；不扩成未给出的最优支撑定理。')
variance_assumptions=['固定模型/输入/基线及固定未加噪交互','原Appendix D：全部输出噪声独立同分布N(0,σ²)','随机变量对全部噪声联合样本求方差，不把自适应γ假设为固定']
result('and-variance',r'\operatorname{Var}(I′_{\rm and}(T))=2^{|T|}\sigma^2',variance_assumptions,core+['sym-and-interaction','sym-gaussian-noise','sym-noise-variance'],[
 ('原实际随机变量身份','Appendix D明确给I′(T)=I(T)+ΣL⊆T cL εL，cL=(−1)^(|T|−|L|)。固定I(T)为常数，所以平移不改变方差。每个高斯项有二阶矩，变号后仍有二阶矩。',r'I′(T)=I(T)+\sum_{L\subseteq T}(-1)^{|T|-|L|}\varepsilon_L','原Proof身份与常数平移'),
 ('独立性与方差可加','对不同L，原IID噪声独立；各自乘确定符号保持独立。有限独立平方可积和的方差是各项方差和，不需要假设待证结论。每个符号平方1，因此每项方差σ²。',r'\operatorname{Var}\left(\sum_{L\subseteq T}c_L\varepsilon_L\right)=\sum_{L\subseteq T}c_L^2\sigma^2','独立随机变量的协方差为零'),
 ('计数与来源式修复','T的子集恰有2^|T|个，故结论成立；T=∅时原raw AND只有输出基线项，其噪声方差σ²，仍满足式。p15首句跨S中心和单εT下标是记号问题；实际同T方差按原Proof而非该首句解释，原首句单列issue。',r'\sum_{L\subseteq T}\sigma^2=2^{|T|}\sigma^2','幂集基数与原raw空集约定')], '原Appendix D固定交互与IID扰动模型的完整随机变量方差证明；不代表重新优化分解γ后的方差。',issue=['f11-issue-variance-expectation-indices'])
result('or-variance',r'\operatorname{Var}(I′_{\rm or}(T))=2^{|T|}\sigma^2',variance_assumptions,core+['sym-or-interaction','sym-gaussian-noise','sym-noise-variance'],[
 ('非空交互实际展开','对非空T⊆N，OR原定义为补集输出的负Möbius变换。将固定gor(L)扰动为gor(L)+εL，有限求和分配即I′or(T)=Ior(T)−ΣL⊆T(−1)^(|T|−|L|)ε(N\\L)。这来自定义，不把等式当目标假设。',r'I′_{\rm or}(T)=I_{\rm or}(T)-\sum_{L\subseteq T}(-1)^{|T|-|L|}\varepsilon_{N\setminus L}','原OR定义与线性分配'),
 ('补集索引与独立性','L,K⊆T⊆N，若N\\L=N\\K，取同总体补集得到L=K。因此不同L使用不同IID输出噪声，重索引后的族保持独立同分布；确定的负号同样平方1。应用完整有限高斯方差和，得到2^|T|σ²。',r'N\setminus(N\setminus L)=L\quad(L\subseteq N)','有限补集双射、真正随机变量方差和'),
 ('原空集分支','Generalizable规定Ior(∅)=vor(x∅)，空集加噪输出本身方差σ²=2^0σ²。这一分支不能用非空OR的负Möbius式替代，也不同于Sparse的中心化空集交互0。','','原独立空集定义')], '完整补集重索引与原OR空集分支的IID方差证明；本篇“Similarly”未给独立原OR细证。')
result('equation10',r'\operatorname{rowmax}(a,b)\stackrel{\rm claimed}{=}|\max(a,b)|',[],core+['sym-interaction-matrix','sym-rowmax','sym-entrywise-l1','sym-redundancy-weight','sym-decomposition-parameter'],[
 ('逐点反例','正式p6 rowmax=每行ℓ∞=max(|a|,|b|)，p16 Eq10展开却用|max(a,b)|。取a=−3,b=2，前者3、后者2，故该行恒等式不成立。Möbius变换可逆，任意这样的两模型AND交互行可由对应掩码输出分解实现，并非非法交互值。',r'\max(|-3|,|2|)=3\ne2=|\max(-3,2)|','直接实数计算；原AND取值无非负约束'),
 ('影响范围与额外索引错误','反例仅否定展开使用的逐点行恒等式，不能据一个点推出两个优化问题最小值必不相等。原Eq10的自由S及T求和中固定xTk、γTk保留为索引排印问题；原带min的父等式在这些索引未解决时未完成命题评估。逐点展开的分析子断言单列反例，不能把原式改成maxabs后宣布完成。','','区分逐点展开子断言与原带min父等式')], '仅否定 signed max 与原行ℓ∞的逐点展开子断言；原完整带min等式保留，自由索引问题及最优值比较未完成评估。',status='blocked_by_source_issue',issue=['f11-issue-rowmax-signed-max','f11-issue-equation10-free-indices'],statement_status='false_pointwise_row_identity; optimization_minima_not_assessed')
result('alpha-zero',r'L_6(A,B;0)=L_5(A,B)',[],['sym-interaction-matrix','sym-rowmax','sym-entrywise-l1','sym-redundancy-weight'],[
 ('原目标定义','记P(A,B)=∥rowmax A∥1+∥rowmax B∥1，Q(A,B)=∥A∥1+∥B∥1。Eq6的逐点目标是P+αQ；代α=0得到P+0Q=P，即Eq5。',r'P+0\cdot Q=P','零乘法与原目标定义'),
 ('优化适配','参数搜索的可行域相同，因此逐点目标函数完全相同，最小化问题也相同。此等式没有声称其他α的泛化曲线，p17–18经验消融另列。α=0句的正式PDF位置为17页，图延续至18页。','','同域同函数；正式页码校正')], '原α=0代入的完整确定性恒等式；实验观察不计为证明。')
issues=[{'id':'f11-issue-variance-expectation-indices','paper_id':'iclr2024-generalizable','kind':'source_proof_notation_error',
 'title':'Appendix D首句方差中心跨S与期望下标不一致','original_formula_tex':r'\mathbb E_{\varepsilon_T\sim N(0,\sigma^2)}[I′_{\rm and}(T)-\mathbb E_{\forall S,\varepsilon_S\sim N(0,\sigma^2)}I′_{\rm and}(S)]^2=2^{|T|}\sigma^2',
 'source_refs':[{'source_id':'src-iclr2024-generalizable-main','pdf_page':15}],
 'analysis_md':'首句内层中心写I′(S)，外层仅εT下标；严格方差须对全部噪声联合样本求期望且中心为同T随机变量的期望。随后原Proof实际使用Var(I′(T))和固定I(T)，其IID方差结论正确。原首句保留，修记号与证明解释，不改最终Var结论。',
 'affected_result_ids':['f11-and-variance'],'impact_scope':'p15引导首句的期望记法；不否定原Proof固定IID方差结论',
 'statement_status':'final_variance_statement_correct_under_original_proof_assumptions','fix_authorization':'proof_only_granted','user_confirmation':'not_required_for_proof_repair','resolution_status':'proof_notation_repaired_in_project_explanation'}]
for r in results:
    if r['id']=='f11-equation10':
        r['analysis_clause_tex']=r.pop('statement_tex')
        r['rewrite_status']='blocked_by_source_issue'
        r['statement_status']='parent_optimization_equation_ill_scoped_and_not_assessed; pointwise_row_expansion_refuted'
        r['clause_assessments']=[{'id':'rowmax_expansion','status':'refuted','counterexample':'a=-3,b=2: row l∞=3; |signed max|=2'}, {'id':'parent_optimization_equation','status':'not_assessed','scope':'original free indices unresolved; pointwise counterexample does not compare minimized values'}]
        r['lean']['verification_role']='counterexample'
report_path=BASE/'verification/report.json'
report=json.loads(report_path.read_text()) if report_path.exists() else {}
da={d['name']:d for d in report.get('declarations',[])}
lean_targets={
 'f11-reparameterization':(['FullGeneralizableAnalysis.masked_model_decomposition','FullGeneralizableAnalysis.decomposition_iff_unique_gamma'],'actual Game(Fin n) on all 2^n original masks, arbitrary real output baseline; unique gamma vector for any original decomposition'),
 'f11-rowmax-penalty':(['FullGeneralizableAnalysis.rowStrength_plateau'],'arbitrary finite nonempty model family; all signs allowed; row l∞ plateau with one retained maximizing component; no global support optimum claim'),
 'f11-and-variance':(['FullGeneralizableAnalysis.masked_model_and_variance','Harsanyi.noisy_masked_and_variance'],'actual masked-model output perturbation, all subset IID Gaussian noises, including raw AND empty output baseline; fixed original I, not adaptively optimized gamma'),
 'f11-or-variance':(['FullGeneralizableAnalysis.masked_model_or_variance','Harsanyi.noisy_masked_or_variance'],'actual same finite masked-model family with complement indices and raw OR empty baseline branch; IID original noise model'),
 'f11-equation10':(['FullGeneralizableAnalysis.signed_max_counterexample'],'only the signed-max versus row-l∞ pointwise clause is refuted; no statement comparing optimization minima'),
 'f11-alpha-zero':(['FullGeneralizableAnalysis.alpha_zero'],'actual row-max and entrywise matrix objective, arbitrary finite rows/models; finite original 2^n×m matrix instance, alpha0 only')}
for r in results:
    if r['id'] not in lean_targets:
        r['verification_role']='scope_explanation'
        continue
    names,scope=lean_targets[r['id']]
    ds=[da[n] for n in names if n in da]
    role='counterexample' if r['id']=='f11-equation10' else 'theorem_proof'
    r['verification_role']=role
    if report.get('status')=='passed' and len(ds)==len(names):
        d=ds[0]
        r['lean']={'status':'verified','verification_role':role,'evidence_role':role,'declarations':names,'scope':scope,'completion_scope':scope,
          'report_path':str(report_path),'compiled':True,'axiom_audit':'passed','build_id':report['build_id'],
          'source_fingerprint':report['source_fingerprint'],'source_path':d['source_path'],'line':d['line'],'statement':d['signature'],
          'axioms':sorted(set(a for d in ds for a in d['axioms'])),'source_semantics_automatically_verified':False}
        for step in r['proof_steps']:
            step['lean_refs']=[{'declaration':d['name'],'source_path':d['source_path'],'line':d['line'],'scope':scope,'report_path':str(report_path)} for d in ds]
(BASE/'generalizable-analysis-results.json').write_text(json.dumps({'paper_id':'iclr2024-generalizable','results':results,'issues':issues,'source_transcription_owner':'reader_multipage_v2_max','authorization':'proof_only_granted; statement modifications forbidden'},ensure_ascii=False,indent=2)+'\n')
print(len(results),'Generalizable analysis results')
