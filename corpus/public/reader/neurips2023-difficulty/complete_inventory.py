"""Explicit source boundaries for F10; the mathematical denominator is not inferred from content."""
import json
from pathlib import Path
P=Path(__file__).parent
old=json.loads((P/'inventory.json').read_text());sid=old['sources'][0]['source_id']
E=[]
def entry(i,label,title,kind,pages,section,proof=(),psection=None,reason=None,external=False):
 def loc(ps,s):return dict(source_id=sid,pdf_pages=list(ps),section=s)
 E.append(dict(id=i,original_label=label,title=title,kind=kind,statement_location=loc(pages,section),proof_location=loc(proof,psection or section),appearances=[loc(pages,section)]+([loc(proof,psection or section)] if proof else []),external_reference=external,determination_basis='Official published main text and appendix were checked at these local source boundaries.',proof_target=reason is None,merge_target_id=None,**({'non_proof_reason':reason} if reason else {})))
entry('diff-interaction','Main Eq.(1)','原始 Harsanyi 交互','definition',[3],'3.1',reason='Eq.(1) defines the dividend of a fixed masked-input game; it does not assert a separate theorem.')
entry('diff-universal','Theorem1; Main Eq.(3), exact equality','全部掩码精确重构','theorem',[4],'3.1',[4],'3.1',external=True)
entry('diff-salient-reconstruction','Main Eq.(2); Theorem1 Eq.(3), approximate clauses','显著支持近似重构','derivation',[3,4],'3.1',external=True)
entry('diff-sparsity','3.1; citations [45],[47],[27]','稀疏出现与外引范围','external_theorem',[3,4],'3.1',external=True)
entry('diff-concept-order','Complexity (order) paragraph','概念支持阶数','definition',[4],'3.1',reason='This paragraph defines complexity/order as support cardinality and illustrates the terminology.')
entry('diff-reference','Reference-value paragraph; footnote4','输入参考距离与裁剪','definition',[4,5],'3.2',reason='The reference rule, its clipping footnote and the Gaussian approximation specify a model rather than a proved identity.')
entry('diff-taylor','Theorem2; Main Eq.(4); G.1 local Eq.(2)–(8)','Taylor 支持展开','theorem',[4,17],'3.2; G.1',[17,18],'G.1')
entry('diff-moments','Theorem3 main lowest-J clause; Main Eq.(5); related G.2 local Eq.(9)–(13)','正文最低阶绝对触发矩','theorem',[5],'3.2',[18,19],'G.2')
entry('diff-lowest-interaction','G.2 repeated Theorem3: J prose but unnumbered lowest-I display; local Eq.(9)–(13) argument','附录最低阶有符号交互矩变体','theorem',[18],'G.2',[18,19],'G.2')
entry('diff-general-moments','Theorem3 general-degree clause; Main Eq.(6); G.2 local Eq.(14)–(18)','一般绝对触发矩','theorem',[5,19],'3.2; G.2',[19],'G.2')
entry('diff-product','G.2 Proposition1','独立乘积矩原式','proposition',[18],'G.2')
entry('diff-order-variance-argument','After Theorem3, unnumbered chaotic-coefficient inference','单项方差到整体阶数推论','derivation',[5],'3.2',[5],'3.2')
entry('diff-order-variance-metrics','E^(s), V^(s), E^(s)/sqrt(V^(s)); Figure2','噪声平均与标准差稳定指标','empirical',[5,6],'3.2',reason='These displayed formulas define finite experimental aggregates; Figure2 is an observation, not an algebraic order theorem.')
entry('diff-trigger-definition','Main Eq.(7)','固定参考系数与连续触发','definition',[5,6],'3.2.1',reason='Eq.(7) defines a quotient trigger. Its zero-coefficient boundary is recorded separately; the quotient definition is not a separate theorem.')
entry('diff-binary','Theorem4; Main Eq.(8); G.3 local Eq.(19)–(24)','掩码触发的二值状态','theorem',[6,20],'3.2.1; G.3',[6,20],'3.2.1; G.3')
E[-1]['appearances'].append(dict(source_id=sid,pdf_pages=[3],section='3.1, mouth-patch AND explanation'))
entry('diff-linear-representation','Main Eq.(9), exact equality and approximate salient sum','连续触发线性表示','derivation',[6],'3.2.1',[6],'3.2.1')
entry('diff-learning-consistency-argument','3.2.2 unnumbered learning-difficulty inference','一致性到学习难度的解释','derivation',[6,7],'3.2.2',[6,7],'3.2.2')
entry('diff-training-metrics','beta(S); kappa(S); Figures3–4','类别一致性与扰动指标','empirical',[7,8],'3.2.2',reason='Beta and kappa introduce experimental metrics and plots. The asserted equality between the two kappa expressions is a separate true proof target diff-kappa-conversion.')
entry('diff-kappa-conversion','3.2.2 unnumbered equality between two kappa expressions','跨样本 κ 约分等式','derivation',[7],'3.2.2',[7],'3.2.2')
entry('diff-efficiency','Appendix D property(1)','交互效率','external_theorem',[15],'D',external=True)
entry('diff-linearity','Appendix D property(2)','交互线性','theorem',[15],'D')
entry('diff-dummy','Appendix D property(3), nonempty S','非空上下文 Dummy','theorem',[15],'D')
entry('diff-symmetry','Appendix D property(4)','变量对称性','theorem',[16],'D')
entry('diff-anonymity','Appendix D property(5)','变量匿名性','theorem',[16],'D')
entry('diff-recursion','Appendix D property(6), unnumbered','交互递归差分','theorem',[16],'D')
entry('diff-distribution','Appendix D property(7), unnumbered','纯 AND 交互分布','theorem',[16],'D')
entry('diff-multiorder-definition','Appendix F; local Eq.(1)','上下文基数 m 的多阶交互','definition',[16],'F',reason='Appendix F defines a context-size average. Context size m and concept support size |S| are distinct notions; the G.4 relation is separately targeted.')
entry('diff-multiorder','G.4; local Eq.(25)','多阶交互组合关系','derivation',[20,21],'G.4',[20,21],'G.4')
entry('diff-regression','G.5 Steps1–3; local Eq.(26)–(28)','独立特征回归与最后比例','derivation',[21],'G.5',[21],'G.5')
entry('diff-experiments','Appendix H Experimental Settings; related experimental occurrences in C and E','正式实验设置','empirical',[22],'H',reason='Appendix H specifies architectures, training, sampling, perturbation and attack implementations. These configurations do not assert an additional mathematical theorem; the separate formula and inference targets remain explicit.')
E[-1]['appearances'] += [dict(source_id=sid,pdf_pages=[14,15],section='C, additional experiments'),dict(source_id=sid,pdf_pages=[16],section='E, additional experiments')]
entry('diff-training-similarity','3.2.3 unnumbered Jaccard and sign-split formulas; Figure5','训练终点概念 Jaccard 相似度','definition',[8],'3.2.3',reason='The unnumbered formulas define sign-split vectors and weighted Jaccard similarity; Figure5 is a finite observation.')
entry('diff-adversarial-metric','alpha(S), A^(s); Figure6','对抗扰动敏感指标','empirical',[9],'4.1',reason='Alpha and A^(s) define experimental attack sensitivity aggregates; their numerical order trend is empirical.')
entry('diff-fast-learning-inference','3.2.3 unnumbered consistency-to-speed inference','稳定性到快学解释','derivation',[8],'3.2.3',[8],'3.2.3')
entry('diff-adversarial-inference','4.1 multiorder-to-concept explanation','多阶关系到对抗鲁棒性解释','derivation',[8,9],'4.1',[8,9],'4.1',external=True)
entry('diff-noise-learning-inference','4.2 first bullet, Arpit/Cheng','白噪声慢学的概念解释','derivation',[9],'4.2',[9],'4.2',external=True)
entry('diff-shallow-learning-inference','4.2 second bullet, Mangalam/Prabhu','浅模型易样本的概念解释','derivation',[9,10],'4.2',[9,10],'4.2',external=True)
entry('diff-frequency-learning-inference','4.2 third bullet, Xu','频谱先后顺序的概念解释','derivation',[10],'4.2',[10],'4.2',external=True)
entry('diff-adversarial-learning-inference','4.2 fourth bullet, Liu','对抗训练快学的概念解释','derivation',[10],'4.2',[10],'4.2',external=True)
sections={1:'Abstract; 1',2:'1; 2',3:'2; 3; 3.1',4:'3.1; 3.2',5:'3.2; 3.2.1; footnote4',6:'3.2.1; 3.2.2',7:'3.2.2',8:'3.2.2; 3.2.3; 4.1',9:'4.1; 4.2',10:'4.2; 5; References',11:'References',12:'References',13:'References',14:'A; B; C',15:'C; D',16:'D; E; F',17:'G.1',18:'G.1; G.2; Proposition1',19:'G.2',20:'G.3; G.4',21:'G.4; G.5',22:'H'}
notes={1:'Abstract and motivation; no local proof.',2:'Related-work definitions and cited empirical results; no local proof.',3:'Eq.(1) definition, Eq.(2) exact/approximate reconstruction and cited sparsity.',4:'Theorem1 exact/approximate clauses; Theorem2 and support/order definitions.',5:'Theorem3 lowest/general moments, chaotic-coefficient inference, noise aggregates and reference footnote.',6:'Theorem4 and short binary proof, Eq.(7)–(9), and learning-consistency interpretation.',7:'Beta and kappa definitions, asserted kappa conversion and learning interpretation.',8:'Figure4 continuation, 3.2.3 learning-speed inference and unnumbered Jaccard definitions, Figure5 and 4.1 external multiorder explanation.',9:'Alpha/A experimental metrics, Figure6 and the first two 4.2 unnumbered cited learning explanations.',10:'The cross-page shallow-model explanation, frequency/adversarial-learning explanations, Section5 limitations and references.',11:'Bibliography only.',12:'Bibliography only.',13:'Bibliography only.',14:'Literature and experimental implementation; cited claims remain external.',15:'C experimental plot and D efficiency/linearity/nonempty-dummy statements.',16:'D symmetry/anonymity/recursion/distribution; E plots; F multiorder definition.',17:'G.1 complete Taylor/faithfulness argument, local Eqs.(2)–(8).',18:'G.1 concluding paragraph, G.2 Proposition1 and lowest-degree argument, Eqs.(12)–(13).',19:'G.2 general-degree argument local Eqs.(14)–(18), including absolute/signed transition.',20:'G.3 complete binary-trigger proof local Eqs.(19)–(24) and G.4 initial difference decomposition.',21:'G.4 final Eq.(25) with two distinct errors; G.5 all three regression steps Eqs.(26)–(28).',22:'H exact model/optimizer/perturbation settings; no additional local proof.'}
old.update(entries=E,proof_targets=[e['id'] for e in E if e['proof_target']],review_status='source_inventory_complete_pending_content_math_review')
old['page_audit']=[dict(source_id=sid,pdf_page=p,section=sections[p],classification='statements_and_arguments' if p in [3,4,5,6,7,8,9,10,15,16,17,18,19,20,21] else 'references' if p in [11,12,13] else 'empirical_and_background',entry_ids=[e['id'] for e in E if any(p in a['pdf_pages'] for a in e['appearances'])],review_status='agent_reviewed',evidence_path=str((P/'source-evidence'/f'page-{p:02}.txt').relative_to(Path.cwd())),note=notes[p]) for p in range(1,23)]
(P/'inventory.json').write_text(json.dumps(old,ensure_ascii=False,indent=2)+'\n')
print(len(E),'entries',len(old['proof_targets']),'targets')
