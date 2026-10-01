from pathlib import Path
import json

ROOT=Path('research/full-proof-integration-20260930/cvpr2023')
def issue(id,title,category,pages,original,evidence,impact,results,statement_status='no_counterexample_found'):
    return {'id':id,'paper_id':'cvpr2023-sparse-concepts','title':title,'category':category,
      'source_refs':[{'source_id':'src-cvpr2023-supplement' if category!='algorithm_or_definition_boundary' else 'src-cvpr2023-main','version_id':'ver-cvpr2023-formal','pdf_pages':pages}],
      'original_formula_tex':original,'evidence_md':evidence,'impact_md':impact,'related_result_ids':results,
      'original_statement_status':statement_status,'user_confirmation':'not_individually_reviewed',
      'fix_authorization':'proof_only_granted','statement_fix_authorization':'not_granted',
      'authorization_basis':'用户最新明确：直接标注并修正错误证明；不得修改命题；命题错误单独列出。',
      'status':'statement_error_unrepaired' if statement_status=='counterexample_verified' else 'proof_repair_in_progress' if results else 'boundary_recorded',
      'agent_evidence_status':'pdf_and_formula_checked','user_review_status':'pending'}

issues=[
issue('cvpr-issue-dummy-empty','Dummy 原陈述包括空集，结论错误','statement_counterexample',[2,4],r'\forall S\subseteq N\setminus\{i\},\;v(x_{S\cup\{i\}})=v(x_S)+v(x_{\{i\}})\ \Longrightarrow\ \forall S\subseteq N\setminus\{i\},\;w_{S\cup\{i\}}=0',
  r'取 $N=\{i\}$，$v(x_\varnothing)=0$、$v(x_{\{i\}})=1$。原前提只有 $S=\varnothing$ 一个实例，$1=0+1$ 成立。按原定义 $w_{\{i\}}=1-0=1\ne0$。第4页末把 $\sum_{S^{\prime}\subseteq S}(-1)^{|S|-|S^{\prime}|}$ 统一写为0，在 $S=\varnothing$ 时实际为1。PDF图像 supp-04.png 可逐式复核。',
  '只否定原 Dummy 陈述的全部量词版本。其他性质与Theorem1–5不依赖该错误。不能添加S非空条件或删去单变量结论后称原命题证明完成。', ['cvpr2023-dummy'],'counterexample_verified'),
issue('cvpr-issue-linearity-index','Linearity 原证明把求和内输出索引印为固定 S','proof_display_index_error',[4],r'w^v_S=\sum_{S^{\prime}\subseteq S}(-1)^{|S|-|S^{\prime}|}v(x_S)',
  r'内层应随求和变量变化，但原式固定为 $x_S$。取 $S=\{i\}$、$v(x_\varnothing)=0$、$v(x_{\{i\}})=1$，原显示右侧为 $-1+1=0$，按原定义左侧为1。原稿随后t,u输出亦相同索引。原陈述的线性性没有改变；修正证明直接逐项使用 $g_v(U)=g_t(U)+g_u(U)$。',
  '错误限于原证明显示式，线性性原命题可按现有公共interaction_add忠实证明。', ['cvpr2023-linearity']),
issue('cvpr-issue-beta-proof','Theorem2–4 的 Beta 定义排印与零参数边界','proof_definition_and_boundary_error',[7,8,9,10,11],r'B(p,q)=\int_0^1x^{p-1}(1-x)^{1-q}\,dx;\quad B(|N|-|L|-k,|L|+k);\quad \int_0^1|L|(1-x)^{|L|-1}\,dx=1',
  r'第7页(ii)明示 $p,q>0$ 却将指数写为 $1-q$。取 $(p,q)=(1,2)$，其积分发散，后续有限阶乘公式不匹配。同页 $L=\varnothing,k=0$ 是求和允许项，却调用 $B(|N|,0)$，超出正参数定义；①在 $|L|=0$ 时被积函数在开区间上为零，统一写成1不成立。Theorem3第9页和Theorem4第10–11页复用这一路线，故归并为同一issue。另极端剩余集合为空时②的重编号上界成为负数，须明确空和，而原文未单独处理。',
  '原Shapley、SII、STI结论未发现反例。保持同一命题的全部允许集合，使用有限阶乘卷积给完整证明，含L空集与剩余集合为空，避免修补原积分域而改变目标。', ['cvpr2023-shapley','cvpr2023-shapley-interaction','cvpr2023-shapley-taylor']),
issue('cvpr-issue-distribution-incomparable','纯AND分布证明的三个case没有覆盖不可比集合','proof_case_coverage_gap',[5,6],r'S\subsetneq T;\quad S=T;\quad S\supsetneq T',
  r'原目标量化全部 $S\subseteq N$，但原证明只写上述三类。例 $N=\{1,2\}$、$T=\{1\}$、$S=\{2\}$ 落在三类之外。目标 $w_S=0$ 在此仍真，因为没有 $U\subseteq S$ 包含T。修正证明以 $T\not\subseteq S$、$S=T$、$T\subsetneq S$ 分组（不改原陈述），也可直接复用已编译的interaction_unanimity。',
  '原目标正确，原证明缺case。Add-Mul推导复用这个目标，保留同一原命题并完成修证明。', ['cvpr2023-interaction-distribution','cvpr2023-addmul-coefficients']),
issue('cvpr-issue-l0-support','选择集合大小与非零系数个数不总相等','algorithm_or_definition_boundary',[4],r'\|\boldsymbol w_\Omega\|_0=|\Omega|',
  r'第4页定义 $w^{\prime}_S=w_S$ 若 $S\in\Omega$，否则为0。若 $S\in\Omega$ 而 $w_S=0$，它贡献集合大小却不贡献L0范数；例如全零模型、$\Omega=\{\varnothing\}$ 给0与1。两类可行表示的最优值可能通过删除零项联系，但原逐项相等并无无条件证明。',
  '这是算法段的原等式边界，不是编号定理；不静默把Omega定义改为support。目录保留原式和反例。', [],'counterexample_verified'),
issue('cvpr-issue-lagrange-equivalence','L0约束与固定罚参数目标的等价箭头未被证明','algorithm_or_definition_boundary',[4],r'\min\mathrm{unfaith}\ \mathrm{s.t.}\|w_\Omega\|_0\le M\ \Longleftrightarrow\ \min\mathrm{unfaith}+\lambda\|w_\Omega\|_0',
  '原Eq.(6)没有规定罚参数如何选取或证明离散非凸目标的强对偶。一般离散优化中，可行点 (support,error)=(0,3),(1,2),(2,0)，约束M=1选择中点，但任何lambda要选中点都需lambda≤1且lambda≥2，矛盾。本反例针对一般等价箭头，没有声称这一三点实例已由本文某个DNN产生。',
  '只能按原文登记为启发式目标转换/松弛；不当作本篇已证明的数学等价。', []),
issue('cvpr-issue-ratio-zero-denominator','已解释比例在全部效应为零时未定义','algorithm_or_definition_boundary',[5],r'R_\Omega=\frac{\sum_{S\in\Omega}|w_S|}{\sum_{S\in\Omega}|w_S|+|\Delta|}',
  r'取 $v(x_S)=0$ 对所有S，得到全部 $w_S=0$、$\Delta=0$，分母为0。原文未给此边界约定。符号表把分母非零记录为表达式的定义域条件，不据此修改原论文命题或杜撰R值。',
  '仅影响指标的零模型边界与符号域；重构/唯一性仍适用。', [],'counterexample_verified')]
(ROOT/'issues.json').write_text(json.dumps({'paper_id':'cvpr2023-sparse-concepts','issues':issues,'authorization':'proof_only_granted; statements must remain unchanged'},ensure_ascii=False,indent=2)+'\n')
lines=['# CVPR 2023 原陈述与证明问题','', '用户已授权直接标注并修正证明，禁止修改命题；此授权不等于用户逐个审阅数学事实。原命题错误单列，完整原文另见transcripts。','']
for x in issues:
    lines += [f'## {x["title"]} (`{x["id"]}`)','',f'类别：{x["category"]}；来源：{x["source_refs"][0]["source_id"]} PDF 第 '+','.join(map(str,x['source_refs'][0]['pdf_pages']))+' 页。','',r'\['+x['original_formula_tex']+r'\]','',x['evidence_md'],'',x['impact_md'],'',f'原陈述状态：`{x["original_statement_status"]}`；证明修正授权：`proof_only_granted`；命题修改授权：`not_granted`。','']
(ROOT/'issues.md').write_text('\n'.join(lines))
print(len(issues),'issues written')
