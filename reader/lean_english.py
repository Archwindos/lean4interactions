"""Display translations for formal evidence; no machine fields are overlaid."""
import re
from bilingual import merge_overlay
CJK=re.compile(r'[\u3400-\u9fff]')
TEXT={
'公共系数唯一性及其实际依赖的逆向反演；论文有限总体量词见独立适配。':'Uniqueness of the shared coefficients and its actual inverse-inversion dependency. The fixed finite population quantifiers appear in the separate paper adapter.',
'公共有限集合重构定理及其真实库内归纳证明；论文适配另见各结果。':'Shared finite-set reconstruction theorem and its actual library induction proof. Paper adapters appear under the individual results.',
'实际所列范围通过编译与公理审计；原命题语义人工核查':'The listed scope passed compilation and the axiom audit; correspondence to the original statement is reviewed separately.',
'完整向量子断言与截断反例已验证；原复合句不算整体通过':'The full-vector subclaim and a truncation counterexample are verified; the compound original statement has not passed as a whole.',
'原命题不成立；反例声明已编译和审计':'The original statement is false; the counterexample declaration compiled and passed the audit.',
'所列精确范围已编译并通过公理审计':'The exact listed scope compiled and passed the axiom audit.',
'所列精确范围已编译并审计；原来源问题另列':'The exact listed scope compiled and passed the audit; source issues are recorded separately.',
'Lean 对照已编译':'Lean comparison compiled','尚未形式化':'Not formalized','Lean 证据待更新':'Lean evidence is stale','Lean 证据未取得':'Lean evidence unavailable',
'分项Lean证据已验证':'Lean subcomponent verified','分项Lean证据未取得':'Lean subcomponent evidence unavailable','反例证据未取得':'Counterexample evidence unavailable',
'部分范围的 Lean 证据通过':'Lean evidence verified for a partial scope','部分范围的 Lean 证据未取得':'Lean evidence unavailable for the partial scope',
'反例已验证；原命题未证明':'Counterexample verified; the original statement is not proved','反例核验；原命题未证明':'Counterexample check; the original statement is not proved',
'funext S 在声明开头说明函数相等的含义。':'The initial funext S explains function equality pointwise.',
'interaction_reconstruct 对 S 归纳并 generalizing d；这一步为其 empty 分支。':'interaction_reconstruct inducts on S while generalizing d; this step is its empty branch.',
'reconstruction 最后 simp [marginal] 完成此消去；不是五个新定理各自独立编译。':'The final simp [marginal] in reconstruction performs this cancellation. The five explanatory steps are not five independently compiled new theorems.',
'reconstruction_unique 中先改写 interaction_reconstruct，再用 interaction_congr 将 h T 代入。':'reconstruction_unique first rewrites interaction_reconstruct, then substitutes h T through interaction_congr.',
'原具体Q有限和的正分母域内界。':'The bound for the original concrete Q finite sums on their positive-denominator domain.',
'原均匀边际Banzhaf和真实模型分解的最终适配。':'Final adapter for the original uniform marginal Banzhaf sum and the actual model decomposition.',
'原实际联盟与冲突定义生成分子分母，绝对值非负逐项推出域内界；正分母是原商定义域，零分母问题保留。':'The original concrete coalition and conflict definitions determine numerator and denominator. Termwise nonnegativity of absolute values gives the bound on the quotient domain. A positive denominator identifies that original domain; the zero-denominator issue remains recorded.',
'原非空商定义域的实际模型结论；原空联盟范围不由此补定义。':'Actual model result on the original nonempty quotient domain; this does not define the original expression at the empty coalition.',
'实际Lean路线以有限阶乘卷积证明所需AND权重，OR权重另经补集换元；本段排列计数是独立可读论证。':'The actual Lean route uses finite factorial convolution for the AND weights and a complement substitution for OR weights. The permutation counting here is a separate readable argument.',
'实际原定义的有限和适配；原空集或分母范围另列。':'Finite-sum adapter of the actual original definitions; empty-set and denominator scope issues are recorded separately.',
'实际模型及原γ分解的Theorem3.6；没有额外非空假设。':'Theorem 3.6 for the actual model and the original gamma decomposition, without an additional nonempty premise.',
'对一般交互系数的完整有限和拆分；非空由i∈S推出。':'Complete finite-sum split for general interaction coefficients; nonemptiness follows from i being a member of S.',
'尚未取得该声明的实际类型与源码记录；本步不宣称已形式化。':'An actual type and source record for this declaration is not available; this step does not claim formalization.',
'库证明中的局部 h 使用 sum_powerset_insert；e 在代码中是 fun T => d (insert i T)。':'The local h in the library proof uses sum_powerset_insert; e is fun T => d (insert i T) in the code.',
'库证明的 rw [h, ih] 完成该辅助引理。':'The library proof completes this helper with rw [h, ih].',
'归纳语句 generalizing v 以及 empty 分支都在 reconstruction 的现有证明内。':'The generalizing v induction and empty branch are both inside the existing proof of reconstruction.',
'插入引理证明内实际使用子集拆分；这一步没有另增一个项目定理。':'The insertion lemma actually splits subsets inside its proof; this step does not introduce a separate project theorem.',
'本步调用该声明。其参数和前提见下面实际Lean类型；本条编译范围仍由顶部状态说明。':'This step invokes this declaration. Its actual Lean type below gives its parameters and premises; the status above states the compilation scope.',
'正分母域内完整R′界，原零分母定义问题单列。':'Complete R-prime bound on the positive-denominator domain; the original zero-denominator definition issue is recorded separately.',
'此声明核验所用的重构恒等式；边际相减及激活集合分拆在文字中展开，未另声明此人类步骤完整形式化。':'This declaration checks the reconstruction identity used here. Marginal subtraction and the activation-set split are expanded in prose; this does not claim a separate complete formalization of the human step.',
'现有代码的 sum_congr、ih v 和 ih (marginal v i) 分别实现逐项替换和两次归纳应用。':'The existing sum_congr, ih v and ih (marginal v i) implement termwise replacement and the two induction applications.',
'直接证明原具体有限和的包含关系与非负性，未把分子小于分母作假设。':'Direct proof of inclusion and nonnegativity for the original concrete finite sums; numerator bounded by denominator is not assumed.',
'直接识别覆盖项同权重，部分覆盖余项非负。':'Covered terms have the same weights; the remaining partially covered terms are nonnegative.',
'真实偏导、有限差分或实际掩码声明；没有假设Taylor表示或待证交互消失。':'Actual partial-derivative, finite-difference or mask declaration, without assuming a Taylor representation or the desired vanishing of interactions.',
'该实际模型掩码适配核验最终原Shapley等式，包含原γ分解；不据此声称上面每句分别编译。':'The actual model-mask adapter checks the final original Shapley equality, including the original gamma decomposition; this does not imply that each sentence above compiled separately.',
'该有限子集权重声明对应包含计数；OR背景的不交计数在实际路线中使用补集双射。':'The finite-subset weight declaration corresponds to containment counting; disjoint OR background counting uses a complement bijection in the actual route.',
'这一步引用该真实定义或声明；数值例子的代入仍属于正文计算。':'This step cites the actual definition or declaration; numerical substitution in the example remains a prose calculation.',
'这个三行等式是已存在 interaction_insert 的完整数学内容；h1/h2 位于该声明证明内。':'The three-line equality is the complete mathematical content of the existing interaction_insert; h1 and h2 are local to its proof.',
'这里只要求在 S 的所有子集上相同，不要求两函数处处相同。':'Only equality on every subset of S is required, rather than equality of the two functions everywhere.',
'逐T的成员计数恒等式真正对应|S∩T|重数。':'The termwise membership-count identity corresponds exactly to the multiplicity |S intersection T|.'}
ENCODING={
'Lean的 `deriv` 是总函数；在不可微处也会返回一个默认值。因此仅写 `deriv=0` 不能编码原经典偏导为零。`ClassicalMixedDerivativeCutoff` 对每个原要求的高阶有序坐标列表，同时保存 `OrderedCoordinateRegular`（每个前缀沿下一坐标的真实可微性）与最终偏导在全空间为零。坐标重复次数就是原多重指标，两个计数引理实际验证总阶及特取支撑指标。论文adapter另保留原C1背景，不新增C∞、解析性、Taylor相等或多项式表示。':'Lean deriv is a total function and returns a default value even at nondifferentiable points, so deriv=0 alone does not encode a zero classical partial derivative. For each original higher-order ordered coordinate list, ClassicalMixedDerivativeCutoff stores OrderedCoordinateRegular (true differentiability of each prefix along the next coordinate) and the vanishing of the final partial derivative throughout the space. Coordinate repetition counts are the original multi-index; two counting lemmas check total order and the selected support index. The paper adapter retains the original C1 background without adding C-infinity, analyticity, Taylor equality or a polynomial representation.',
'数学上的有限子集族用 Finset 表示；库要求可判定相等关系。论文适配取 Fin n，使 ∀ S : Finset (Fin n) 恰好遍历固定总体的全部掩码。T⊆S 保证指数中的自然数减法没有截断。库源码中的 h1/h2 是插入基数和符号计算；generalizing v/d 保持对任意函数的加强归纳；funext 实现逐点相等。编译检查形式陈述，定义与论文语义的对应仍须人工核对。':'Finite subset families are represented by Finset, with decidable equality required by the library. The paper adapter uses Fin n, so all S : Finset (Fin n) range over every mask of the fixed population. T subset S prevents truncation of the natural-number subtraction in the exponent. The library h1/h2 calculate insertion cardinalities and signs; generalizing v/d preserves strengthened induction for arbitrary functions; funext establishes pointwise equality. Compilation checks the formal statements; correspondence between definitions and paper semantics still requires review.'}
TEXT.update(ENCODING)

def english_candidate(*values):
 """A supplied English key is usable only if its prose is actually English."""
 return next((value for value in values if isinstance(value,str) and value.strip() and not CJK.search(value)),None)

def attach_lean_english(math_content):
 missing=[]
 for proof in math_content.get('results',[])+math_content.get('shared_proofs',[]):
  lean=proof.get('lean',{});provided=lean.get('translations',{}).get('en',{});merge_overlay(lean,provided,proof['id']+':lean');en=dict(provided)
  for key in ['scope','label','encoding_note','statement_md']:
   text=lean.get(key,'')
   if (text or provided.get(key)) and (CJK.search(text) or CJK.search(str(provided.get(key,'')))):
    if key=='label' and text in TEXT:en[key]=TEXT[text]
    else:
     value=english_candidate(provided.get(key),text,TEXT.get(text))
     if value:en[key]=value
     else:missing.append(proof['id']+':lean:'+key)
  if en:lean.setdefault('translations',{})['en']=en
  steps={s['id']:s for s in proof.get('translations',{}).get('en',{}).get('proof_steps',[])}
  for item in lean.get('step_map',[]):
   provided_item=item.get('translations',{}).get('en',{});merge_overlay(item,provided_item,proof['id']+':lean-step');eng=dict(provided_item);sid=item.get('step_id');title=steps.get(sid,{}).get('title')
   english_ref=next((r for r in steps.get(sid,{}).get('lean_refs',[]) if isinstance(r,dict) and r.get('declaration')==item.get('declaration')),{}).get('explanation_md')
   for key in ['title','explanation_md','explanation','text_md','description']:
    text=item.get(key,'')
    if (text or provided_item.get(key)) and (CJK.search(text) or CJK.search(str(provided_item.get(key,'')))):
     value=english_candidate(provided_item.get(key),title if key=='title' else english_ref if key in {'explanation_md','explanation'} else None,text,TEXT.get(text))
     if value:eng[key]=value
     else:missing.append(proof['id']+':lean_step:'+str(sid)+':'+key)
   if eng:item.setdefault('translations',{})['en']=eng
 return {'status':'passed' if not missing else 'in_progress','missing':missing,'scope':'display_fields_only_machine_fields_unchanged'}
