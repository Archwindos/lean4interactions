"""Retain physical pages and expose substantive mathematical subclaims separately."""
import json
from pathlib import Path
P=Path(__file__).parent
inv=json.loads((P/'inventory.json').read_text());meta=json.loads((P/'paper-metadata.json').read_text());sid=inv['sources'][0]['source_id']
existing={e['id']:e for e in inv['entries']}
new=[
 ('bnn-superposition-inference','Unnumbered inference after Theorem 2.4','单项触发到整体交互的近似推论','argument',[6],[6],'2.3'),
 ('bnn-order-inference','Unnumbered inference after Theorem 2.6','缩放夹逼后的近似阶数推论','argument',[8],[8],'2.4'),
 ('bnn-binary','Eq.(13)','归一化触发的二值掩码主张','derivation',[7],[7],'2.4'),
 ('bnn-linear-representation','Eq.(14)','固定参考权重的线性输出表示','derivation',[7],[7],'2.4'),
 ('bnn-salient-matching','Eq.(5)','显著交互的近似掩码匹配','derivation',[3,4],[],'2.1'),
 ('bnn-multiorder-link','Appendix D; cited elementary components','交互作为多阶差分的基本分量','external_theorem',[13],[],'D'),
]
for i,label,title,kind,pages,proof,sec in new:
 if i not in existing:
  loc=dict(source_id=sid,pdf_pages=pages,section=sec)
  existing[i]=dict(id=i,original_label=label,title=title,kind=kind,statement_location=loc,proof_location=dict(loc,pdf_pages=proof),appearances=[loc],proof_target=True,merge_target_id=None,external_reference=kind=='external_theorem',determination_basis='独立数学子主张单列，保留作者原式、定义域及未给误差界的问题。')
  inv['entries'].append(existing[i])
existing['bnn-general-moments']['original_label']='Theorem 2.3; Eq.(33)–(38); unnumbered concluding equality'
existing['bnn-growth']['original_label']='Theorem 2.4; Eq.(39)–(46)'
# Eq. (1) is physically on page 2, and feature-distribution modeling is Eq. (6)–(7).
existing['bnn-posterior']['statement_location']['pdf_pages']=[2,3,4,5,23]
existing['bnn-posterior']['appearances'][0]['pdf_pages']=[2,3,4,5,23]
existing['bnn-metrics']['original_label']='Order strength, V/K metrics; Eq.(6)–(7) distribution-fit method'
for ident in ['bnn-binary','bnn-linear-representation']:
 existing[ident]['proof_location']['pdf_pages']=[7]
 existing[ident]['proof_location']['section']='2.4'
 existing[ident]['statement_location']['section']='2.4'
 existing[ident]['related_source_dependencies']=[dict(source_id=sid,pdf_pages=[15,16],section='G.1',note='Taylor support derivation is a dependency; the local author argument is on page 7.')]
for ident in ['bnn-taylor','bnn-reference','bnn-lowest','bnn-general-moments','bnn-growth']:
 existing[ident]['statement_location']['section']=existing[ident]['statement_location']['section'].replace('2.2','2.3')
 for app in existing[ident]['appearances']:
  if any(p in [5,6] for p in app['pdf_pages']):app['section']=app['section'].replace('2.2','2.3')
for ident in ['bnn-trigger','bnn-regression','bnn-objective','bnn-scaling']:
 existing[ident]['statement_location']['section']='2.4'
 for app in existing[ident]['appearances']:
  if any(p in [7,8] for p in app['pdf_pages']):app['section']='2.4'
existing['bnn-trigger']['original_label']='Eq.(12); definitions preceding Eq.(13)–(14)'
reasons={
 'bnn-posterior':'均场变分目标、后验预测及逐层替代模型是作者设定的方法定义；分布拟合的优化问题不声称所有网络精确同律。',
 'bnn-reference':'作者定义输入基线距离、符号及明确忽略小概率越界尾部的近似模型；这些是设置与建模约定。',
 'bnn-trigger':'固定参考系数与归一化触发在Eq.(12)定义；随后二值性及线性重构已拆成独立数学目标。',
 'bnn-objective':'Eq.(15)规定简化回归优化目标；关于其最优解的数学断言在Theorem2.5独立登记。',
 'bnn-metrics':'按样本/同阶子集平均的强度、方差、稳定度与Eq.(6)–(7)逐层KL拟合定义为测量方法，不是经验趋势的普遍定理。',
 'bnn-generalization':'Appendix F的训练/测试类别交互均值、符号拆分和Jaccard相似度是经验泛化指标定义；未给任意测试分布的数学界。',
 'bnn-experiments':'这些页记录图表、模型配置、噪声采样与观测趋势，未从有限实验推出普遍定理。',
}
for e in inv['entries']:
 e['proof_target']=e['id'] not in reasons
 if not e['proof_target']:e['non_proof_reason']=reasons[e['id']]
 elif 'non_proof_reason' in e:del e['non_proof_reason']
 e.pop('merged_target_id',None)
PAGE_NOTES={1: ('Abstract; 1', 'background_and_empirical', '研究问题、BNN不易编码复杂概念的概要和Figure1经验曲线；没有独立作者证明。'), 2: ('1; 2', 'definitions_and_background', 'Introduction关系讨论；均场Gaussian权重及变分KL优化Eq1、后验预测Eq2定义。'), 3: ('2.1', 'statements_and_cited_scope', 'Harsanyi Eq3定义、全mask忠实Eq4与少量显著项Eq5数学主张；稀疏性外引和经验图。'), 4: ('2.1; 2.2', 'definitions_and_modeling', '概念稀疏总结；权重/偏置均值替代及逐层特征Eq6、KL优化Eq7建模定义。'), 5: ('2.2; 2.3', 'statements_and_modeling', '替代BNN特征分布实验；Lemma2.1及Eq8 Taylor定义、输入参考规则、裁剪脚注与明确忽略Gaussian越界尾部；Theorem2.2起。'), 6: ('2.3', 'theorem_statements_and_empirical', 'Theorems2.2–2.4最低交互矩、一般J矩与支持增长不等式及Eq9–11；噪声指标/实验设定。'), 7: ('2.4', 'statements_and_short_arguments', 'Eq12定义、Eq13二值激活的两种完整情形及Eq14线性输出论证；Eq15回归定义、Theorem2.5 Eq16及学习解释；Figure3经验曲线。'), 8: ('2.4; 3', 'statements_argument_and_empirical', 'Theorem2.6 Eq17缩放上下界；其后由界下降到近似学习强度下降的未编号论述独立登记；三组BNN/DNN实验及Figure4。'), 9: ('3; 4; References', 'empirical_and_references', '实验结论、应用架构和训练细节延续，Discussion/Conclusion及参考文献开始；没有新定理证明。'), 10: ('References', 'references', '正式参考文献页，无本地数学证明；外引来源仅作引用不冒充本文作者证明。'), 11: ('References', 'references', '参考文献续页，无本地证明、定义或新增推导。'), 12: ('A; B; C', 'background_cited_scope_and_empirical', 'AppendixA相关研究；B交互定义/忠实与稀疏外引范围；C输入概念选择和经验可视化，无七性质本地清单。'), 13: ('D; E; F', 'cited_mathematical_claim_and_empirical', 'D声称Harsanyi是多阶交互elementary component并引用Ren2021；E对抗实验及Table2；F泛化指标解释开始。'), 14: ('F', 'definitions_and_empirical', 'Eq18类别训练/测试交互相似度、Eq19正负拆分Jaccard定义及Table3实验；零向量分母范围登记。'), 15: ('G.1', 'author_proof', 'Lemma2.1 Taylor式Eq20及支持Q定义；按子集mask求交互Eq21、分交换和及支持筛选证明。'), 16: ('G.1; G.2', 'author_proof_and_proposition', 'G1 Eq22–25含原0^0处理、支持筛选结论；G2最低项定义、原PropositionG1独立乘积均值/方差及Eq26–29开始。'), 17: ('G.2; G.3', 'author_proof', 'G2 Eq30–32最低项方差结式；G3 Eq33–35展开一般次数，含Gaussian奇偶矩与符号尾部近似。'), 18: ('G.3; G.4', 'author_proof', 'G3 Eq36–38和未编号均值/方差结式；G4原增长命题Eq39及Eq40分旧/新增支持，Eq39不归G3。'), 19: ('G.4', 'author_proof', 'G4 Eq41–45逐步方差增长与稳定性比例推导；保留作者所用绝对/有符号矩等式，重写另修证明。'), 20: ('G.4; G.5', 'author_proof', 'G4 Eq46稳定性结式；G5回归损失Eq47–51与矩阵K定义、原逐行驻点链。'), 21: ('G.5', 'author_proof', 'G5 Eq52–57，Cramer公式、三个实际矩阵和原M′；作者省略的行列式步骤未混入原链。'), 22: ('G.5; G.6; H', 'author_proof_and_implementation', 'G5 Eq58最优权重比例；G6原Eq59–60完整尺度换算上下界，保留原Amin/ASmin记号差别；H训练配置及12图像patch采样实现。'), 23: ('H; I', 'implementation_and_definitions', '实现细节、输入归一化、输入参考严格分支和tau0.5；变分BNN/DNN配置与噪声优化定义。'), 24: ('I', 'empirical', 'AppendixI的LeNet/CIFAR10与MLP8/Census特征直方图，Figure7–8；没有数学证明。'), 25: ('I', 'empirical', '更多BNN/替代DNN特征直方图及对照实验图；没有新增数学证明。')}
for a in inv['page_audit']:
 p=a['pdf_page'];a['section'],a['classification'],a['note']=PAGE_NOTES[p];a['entry_ids']=[e['id'] for e in inv['entries'] if p in set(e['statement_location']['pdf_pages']+e['proof_location']['pdf_pages'])]
inv['proof_targets']=[e['id'] for e in inv['entries'] if e['proof_target']]
meta['results']=[e['id'] for e in inv['entries']]
for n,x in [('inventory.json',inv),('paper-metadata.json',meta)]: (P/n).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
print(len(inv['entries']),len(inv['proof_targets']))
