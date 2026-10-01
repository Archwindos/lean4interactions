# 张拳石公开论文：正式版候选确认表

截至2026-09-30，按‘只取正式版’筛选，17项具备正式材料并完成证明密度筛查：11项优先建议、6项次级或导读参考。另15项有正式出版记录，但正式全文、补充材料或其最终版身份仍有缺口，单列待取得。本轮未将新候选正式导入或展开逐篇重写/Lean形式化，已有试点成果另计。

证明/推导单元按实际Proof块或独立证明小节计；编号结果是独立Theorem/Lemma/Proposition/Corollary陈述，包括注明引用的旧结果，两列不能相加。≥表示有具体页码支持的人工下界。页码均为各正式PDF的物理页；‘补充PDF’从补充文件第一页起算。Generalizable的2个单元按基础重要推荐，FITEE的0个单元按导读参考登记，Generalization的1个单元是近似推导，不能把所有候选统称证明密集论文。

## 优先建议（全部列出）

|稳定ID|正式论文及发表版|研究内容|证明/推导单元|独立编号结果|证明位置|正式材料页数|建议依据|用户确认|
|---|---|---|---:|---:|---|---|---|---|
|F01|[A Unified Game-Theoretic Interpretation of Adversarial Robustness](https://papers.nips.cc/paper/2021/hash/1f4fe6a4411edc2ff625888b4093e917-Abstract.html)<br>NeurIPS 2021|用多阶交互统一解释对抗攻击与防御，分析高阶交互扰动、低阶稳健特征及形状偏置。|≥15|1|补充PDF2–7；补充PDF8–9|正文14＋补充16页|正式NeurIPS2021正文14页+补充16页，至少15段证明。Landing/BibTeX标题为Towards a Unified Game-Theoretic View of Adversarial Perturbations and Robustness，正式PDF仍用本标题；已核作者与论文身份。|待确认|
|F02|[Defining and Quantifying the Emergence of Sparse Concepts in DNNs](https://openaccess.thecvf.com/content/CVPR2023/html/Ren_Defining_and_Quantifying_the_Emergence_of_Sparse_Concepts_in_DNNs_CVPR_2023_paper.html)<br>CVPR 2023|把DNN推理拆为稀疏交互概念并组织成因果图/And-Or图，证明任意mask输入的输出可重构。|12|5|补充PDF3；补充PDF4–5；补充PDF6–11|正文10＋补充27页|正式CVPR正文10页+补充27页，人工重核5个独立编号定理和12个实际证明单元；本轮优先正式收录候选。|待确认|
|F03|[Where We Have Arrived in Proving the Emergence of Sparse Interaction Primitives in DNNs](https://proceedings.iclr.cc/paper_files/paper/2024/hash/db0ee27cb50dd9087b133f6e7d28a90e-Abstract-Conference.html)<br>ICLR 2024|在明确网络条件下研究稀疏符号交互的涌现，构造组合矩阵关系、阶数/数量上界，并连接多种Shapley指标。|11|10|PDF15–27|34页|证明密集：10个独立编号结果均有本地证明，加1个假设蕴含证明；含组合矩阵、稀疏上界及三种Shapley指标关系。|待确认|
|F04|[Towards Theoretical Analysis of Transformation Complexity of ReLU DNNs](https://proceedings.mlr.press/v162/ren22b.html)<br>ICML 2022|以信息论量化ReLU网络变换复杂度，证明复杂度与解缠关系，研究训练动态及复杂度控制。|10|0|PDF13–15|22页|正式ICML2022 PDF22页；10段显式证明虽无Theorem编号，仍应纳入多证明候选。|待确认|
|F05|[Towards Attributions of Input Variables in a Coalition](https://proceedings.mlr.press/v267/zheng25d.html)<br>ICML 2025|指出将单变量归因直接相加可能与coalition归因冲突，构建coalition的AND/OR分配并证明相关定理和归因公理。|10|7|PDF12–21|24页|证明密集：7个编号定理/推论、10个证明小节；coalition与单变量归因关系及AND/OR分配公理可逐项对齐。|待确认|
|F06|[Defects of Convolutional Decoder Networks in Frequency Representation](https://proceedings.mlr.press/v202/tang23i.html)<br>ICML 2023|用DFT和圆周卷积分析卷积decoder的前向/反向传播，解释高频表示、零填充和频谱学习的缺陷。|≥9|8|PDF11–25|34页|正式ICML2023 PDF34页，证明与相关推导位于PDF11–25；已在正式文件人工核页与独立结果。|待确认|
|F07|[Towards the Dynamics of a DNN Learning Symbolic Interactions](https://papers.neurips.cc/paper_files/paper/2024/hash/5aa96d1caa0d0b99d534b67df06be2ff-Abstract-Conference.html)<br>NeurIPS 2024|解释DNN学习符号交互的两阶段动态，分析参数噪声、Taylor触发函数、交互阶数与最优回归权重。|8|9|PDF16–24|36页|证明密集：7个本地有专门证明的编号目标及一个方程证明，涵盖噪声、Taylor触发函数、回归最优解和两阶段动态。|待确认|
|F08|[Bayesian Neural Networks Avoid Encoding Complex and Perturbation-Sensitive Concepts](https://proceedings.mlr.press/v202/ren23a.html)<br>ICML 2023|研究BNN为何避免复杂且扰动敏感的概念，连接交互阶数、Taylor展开、随机变量矩及回归权重。|6|7|PDF15–22|25页|证明密集：6个编号目标有对应证明，连接BNN不确定性、概念复杂度、扰动矩及回归权重；Prop G.1声明未算额外证明。|待确认|
|F09|[HarsanyiNet: Computing Accurate Shapley Values in a Single Forward Propagation](https://proceedings.mlr.press/v202/chen23s.html)<br>ICML 2023|设计HarsanyiNet使一次前向传播精确计算Shapley值，证明网络交互结构与归因关系，并推广到CNN构造。|5|5|PDF12–14；PDF16|22页|证明较集中且Harsanyi基础重要：精确Shapley网络构造有4个本地编号证明及1个CNN扩展证明，适合连接核心有限集合理论。|待确认|
|F10|[Towards the Difficulty for a Deep Neural Network to Learn Concepts of Different Complexities](https://papers.neurips.cc/paper_files/paper/2023/hash/8143b8c73073a9a23b9c18e400066471-Abstract-Conference.html)<br>NeurIPS 2023|理论解释复杂交互概念为何难学，分析Taylor触发函数的扰动方差、概念二值激活、与多阶交互的关系及简化回归模型的学习困难。|4|5|PDF17–21|22页|3个本地编号证明及1个完整组合关系推导，解释复杂概念的学习难度；G.5回归草图另记、不充当完整证明。|待确认|
|F11|[Defining and Extracting Generalizable Interaction Primitives from DNNs](https://proceedings.iclr.cc/paper_files/paper/2024/hash/67a9b444cbcd647572c88194619f72d5-Abstract-Conference.html)<br>ICLR 2024|定义并提取可泛化的AND/OR交互primitive，分析任意mask输入的精确重构和交互方差，验证primitive跨模型或输入的泛化。|2|4|PDF12–15|23页|证明数量不多，但Harsanyi/AND-OR基础重要：精确重构和方差共2个证明单元；引用的Theorem 1/3及Prop 1不额外算本地证明。|待确认|

## 次级候选与导读参考

|稳定ID|正式论文及发表版|研究内容|证明/推导单元|独立编号结果|证明位置|正式材料页数|建议依据|用户确认|
|---|---|---|---:|---:|---|---|---|---|
|F12|[Building Interpretable Interaction Trees for Deep NLP Models](https://ojs.aaai.org/index.php/AAAI/article/view/17685)<br>AAAI 2021|用Shapley交互构建句子的可解释树，提出六种交互指标，并比较BERT、ELMo、LSTM等模型。|3|0|PDF8|10页|正式AAAI10页版包含arXiv9页版没有的3段实际证明；数量中等，核心相关次级候选。|待确认|
|F13|[Quantification and Analysis of Layer-wise and Pixel-wise Information Discarding](https://proceedings.mlr.press/v162/ma22b.html)<br>ICML 2022|量化逐层/逐像素信息丢弃，统一比较不同层和模型对输入信息的保留与删除。|≥2|0|PDF12–13|35页|正式ICML35页已核至少2类推导，属于信息论相关次级；不把总页数当证明页数。|待确认|
|F14|[Layerwise Change of Knowledge in Neural Networks](https://proceedings.mlr.press/v235/cheng24b.html)<br>ICML 2024|把知识定义和交互提取扩展到神经网络中间层，追踪逐层知识的保留、增加与丢失，含两个编号理论目标。|2|2|PDF15–16|22页|逐层知识/交互研究有2个清晰目标与证明，是基础matching到中间层应用的次级候选。|待确认|
|F15|[Interpreting Multivariate Shapley Interactions in DNNs](https://ojs.aaai.org/index.php/AAAI/article/view/17299)<br>AAAI 2021|定义多变量Shapley交互和coalition的重要性，量化DNN记忆的原型特征及组内变量协同。|1|0|PDF9–10|10页|正式AAAI10页已核1段关系推导；保留核心定义的次级候选，不能声称此版证明很多。|待确认|
|F16|[Explaining Generalization Power of a DNN Using Interactive Concepts](https://ojs.aaai.org/index.php/AAAI/article/view/29655)<br>AAAI 2024|用交互概念解释DNN泛化，给出Taylor和扰动矩公式及近似方差增长分析，并开展实证验证；公开正文没有专门完整证明附录。|1（近似推导）|3|PDF5–6|9页|公开正式正文有3个编号陈述及1个近似推导；没有专门完整证明附录，应与证明密集成果区分。|待确认|
|F17|[Towards the first principles of explaining DNNs: interactions explain the learning dynamics](https://doi.org/10.1631/FITEE.2401025)<br>FITEE 2025|Personal View讨论交互解释能否构成DNN解释的第一性原理，串联公理、泛化/对抗/瓶颈现象、归因方法统一及两阶段学习动态。|0|0|—|10页|正式Personal View提供交互理论体系与学习动态导读；本地新证明为0，作为基础参考单列。|待确认|

## 正式材料待取得或待核实

下表整体证明数量均未核实，不以预印本或正文编号陈述数量代替。正文已取得的文件保留以便对齐，缺少的证明附件仍待取得。

|稳定ID|正式论文及发表版|已取得正式材料|证明数量|缺口与处理依据|
|---|---|---|---|---|
|W01|[Attribution Explanations for Deep Neural Networks: A Theoretical Perspective](https://doi.org/10.1109/TPAMI.2026.3667600)<br>IEEE Transactions on Pattern Analysis and Machine Intelligence 2026|未取得|未核实|正式出版DOI、作者及SJTU身份已由IEEE存入Crossref的元数据核实；正式PDF接口未取得全文，证明数量未核实，不能替用arXiv计数。|
|W02|[Interpretable Rotation-Equivariant Multiary-Valued Network for Attribute Obfuscation](https://doi.org/10.1109/TPAMI.2025.3599592)<br>IEEE Transactions on Pattern Analysis and Machine Intelligence 2025|未取得|未核实|正式出版DOI、作者及SJTU身份已由IEEE存入Crossref的元数据核实；正式PDF接口未取得全文，证明数量未核实，不能替用arXiv计数。|
|W03|[Monitoring Primitive Interactions During the Training of DNNs](https://ojs.aaai.org/index.php/AAAI/article/view/34223)<br>AAAI 2025|正文9页；补充待取得/核实|未核实|正式9页正文有Theorem 2.1，证明指定在未取得的Appendix E；整体证明密度须取得正式补充材料后再判断。|
|W04|[An Introspective Data Augmentation Method for Training Math Word Problem Solvers](https://doi.org/10.1109/TASLP.2024.3408067)<br>IEEE/ACM Transactions on Audio, Speech, and Language Processing 2024|未取得|未核实|正式出版DOI、作者及SJTU身份已由IEEE存入Crossref的元数据核实；正式PDF接口未取得全文，证明数量未核实，不能替用arXiv计数。|
|W05|[Batch Normalization Is Blind to the First and Second Derivatives of the Loss](https://ojs.aaai.org/index.php/AAAI/article/view/29978)<br>AAAI2024|正文9页；补充待取得/核实|未核实|正式正文9页已核：首页及编号结果可定位，实际证明引用Appendices。官方第二galley经下载确认是Underline会议报告，不是证明supplement。不得照搬旧arXiv附录计数。|
|W06|[Clarifying the Behavior and the Difficulty of Adversarial Training](https://ojs.aaai.org/index.php/AAAI/article/view/29032)<br>AAAI2024|正文9页；补充待取得/核实|未核实|正式正文9页已核：首页及编号结果可定位，实际证明引用Appendices。官方第二galley经下载确认是Underline会议报告，不是证明supplement。不得照搬旧arXiv附录计数。|
|W07|[Unifying Fourteen Post-Hoc Attribution Methods With Taylor Interactions](https://doi.org/10.1109/TPAMI.2024.3358410)<br>IEEE Transactions on Pattern Analysis and Machine Intelligence 2024|未取得|未核实|正式出版DOI、作者及SJTU身份已由IEEE存入Crossref的元数据核实；正式PDF接口未取得全文，证明数量未核实，不能替用arXiv计数。|
|W08|[Can We Faithfully Represent Masked States to Compute Shapley Values on a DNN?](https://openreview.net/forum?id=YV8tP7bW6Kt)<br>ICLR2023|未取得|未核实|正式发表已由作者publication与官方OpenReview公开论文记录交叉识别；网页PDF/API/API2均403，web.open亦官方browser challenge。arXiv证明数保留在发现台账，不能替代正式版。|
|W09|[Discovering and Explaining the Representation Bottleneck of DNNs](https://openreview.net/forum?id=iRCUlgmdfHJ)<br>ICLR2022|未取得|未核实|正式发表已由作者publication与官方OpenReview公开论文记录交叉识别；网页PDF/API/API2均403，web.open亦官方browser challenge。arXiv证明数保留在发现台账，不能替代正式版。|
|W10|[A Unified Approach to Interpreting and Boosting Adversarial Transferability](https://openreview.net/forum?id=X76iqnUbBjz)<br>ICLR2021|未取得|未核实|正式发表已由作者publication与官方OpenReview公开论文记录交叉识别；网页PDF/API/API2均403，web.open亦官方browser challenge。arXiv证明数保留在发现台账，不能替代正式版。|
|W11|[Interpreting and Boosting Dropout from a Game-Theoretic View](https://openreview.net/forum?id=Jacdvfjicf7)<br>ICLR2021|未取得|未核实|正式发表已由作者publication与官方OpenReview公开论文记录交叉识别；网页PDF/API/API2均403，web.open亦官方browser challenge。arXiv证明数保留在发现台账，不能替代正式版。|
|W12|[3D-Rotation-Equivariant Quaternion Neural Networks](https://www.ecva.net/papers/eccv_2020/papers_ECCV/html/3539_ECCV_2020_paper.php)<br>ECCV2020|正文17页；补充待取得/核实|未核实|正式ECCV2020正文17页已取得；arXiv21页版的4类操作证明在额外附录中，不在此正式正文中，正式附件未取得。|
|W13|[Interpretable Complex-Valued Neural Networks for Privacy Protection](https://openreview.net/forum?id=SHDG97ukaIH)<br>ICLR2020|未取得|未核实|正式发表已由作者publication与官方OpenReview公开论文记录交叉识别；网页PDF/API/API2均403，web.open亦官方browser challenge。arXiv证明数保留在发现台账，不能替代正式版。|
|W14|[Towards a Deep and Unified Understanding of Deep Neural Models in NLP](https://proceedings.mlr.press/v97/guan19a.html)<br>ICML2019|正文10页；补充待取得/核实|未核实|正式ICML2019主文10页已取得；个人主页链接的Microsoft全文/补充403，猜测PMLR supplement路径404。未取得附件，不能依据正文或摘要断言完整证明数。|
|W15|[Mining And-Or Graphs for Graph Matching and Object Discovery](https://openaccess.thecvf.com/content_iccv_2015/html/Zhang_Mining_And-Or_Graphs_ICCV_2015_paper.html)<br>ICCV2015|正文9页；补充待取得/核实|未核实|正式ICCV主文9页已取得；作者官网另有18页Supplementary包含3段长证明（PDF2–11），但本轮未从正式venue确认该附件的最终版身份，故不将它计入正式证明数。|

## 计数与检索边界

CVPR2023 Sparse的‘正文10＋补充27页’和NeurIPS2021 Robustness的‘正文14＋补充16页’是两个文件的材料规模，不能当作正文PDF本身的页数。NeurIPS2023 Difficulty主文/补充两个URL下载为同一SHA256文件，不重复计篇数或证明数。
ICLR2024 Sparse按正式题名及34页文件登记，证明延续到PDF27；正文Theorem3在B.4误标Theorem6，按陈述内容去重。Generalizable按正式23页文件，证明在12–15页；Coalition按ICML2025正式24页版本。
单元定位来源于逐篇正式版核查；本轮只核证明密度、版本和位置，没有完成每个证明的数学审校。下界计数及待取得材料会在用户确认范围后的逐篇流程细化。
上述数量按每篇论文分别统计，尚未对跨论文共享的重构、Shapley等证明做命题对齐和去重，不能把各行相加当作公共Lean库的独立定理数。
本轮正式版核查集合含26篇已取得正文的论文、28个不同正式PDF文件；其中待确认候选为17篇/19文件。另2项官方全文仅完成自动初筛，保留发现层，未据此称证明较少。
检索记录另外保留95项arXiv作者索引及91项取得的公开PDF记录，其余为撤回/重复撤回记录与两项HTML文集；它们仅用于发现，不进入正式候选。官方作者publicationlist、实验室主页及官方venue用于补漏；作者主页部分年份未更新，不能据此宣称网上绝无遗漏。

完整发现与排除台账见[full-ledger.md](../research/paper-survey-20260930/full-ledger.md)，机器可读原始字段及选定正式版见[combined-papers.json](../research/paper-survey-20260930/combined-papers.json)，审核选择可用[candidate-selection.csv](../research/paper-survey-20260930/candidate-selection.csv)。所有正式文件的路径、SHA256、逐文件页数及证明页段已检查，验证错误为0。
