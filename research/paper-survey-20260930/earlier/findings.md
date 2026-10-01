# 早期公开论文筛查：正式版口径冻结说明

日期：2026-09-30。范围由首次公开年份分工：本目录负责首次公开不晚于2022的记录；正式发表在2023/2024的旧预印本仍由本目录核对。近期代理负责首次公开2023以后及其另外核对的近期非arXiv发表记录。

用户最新要求是“只取走正式版的论文”。下表的计数均来自实际取得的正式会议PDF及正式supplement；arXiv只保留为发现和版本对照。此次调研没有正式入库论文，没有改corpus、Lean或网站，也没有读取/发送任何未发表私稿。

## 可合并的文件

- `formal-candidates.json`：7篇正式材料已人工核对的候选，4篇主推荐、3篇次级。合并主表直接读取此文件。
- `formal-pending.json`：10项已发表但正式PDF、正式证明附件或附件最终版身份未取得/未核实的记录，不移植预印本计数。
- `papers.json`：82行完整发现台账；`is_formal_version=true`且`recommendation`为`recommend/secondary`才能进入正式候选主表。其余是发现、初筛或待取得记录。
- `papers.arxiv-discovery.json`：59个早期作者索引记录及其固定arXiv版本筛查。保留原证明结构证据，但不作为正式待收录表。
- `publication-index/title-mapping.json`：个人官网中76个带PDF/arXiv链接的publication条目逐项对应mergekey和责任代理；76/76已映射。
- `survey-qa.json`：必需字段、文件SHA256和正式证明页段检查，未发现错误。

`proof_count`是实际证明/推导单元数量，`numbered_result_count`是独立编号Theorem/Lemma/Proposition/Corollary陈述数量；两者不能相加。`manual_lower_bound`表示保守下界。PDF页段包含陈述、准备和相关推导，不能当作纯证明页数。本文与附录的重复陈述不重计；一个联合证明不因对应多个结果而重复计数；标准外引性质/定理没有本地证明时不算本论文实际证明。

顶层`total_pages`对应`local_pdf`指向的primary PDF实际页数；`total_material_pages`才是正文与正式补充材料的合计。Sparse分别为10与37，Robustness分别为14与30；`materials`保留各文件自己的页数。表格中的“正文10+补充27”等展示的是材料组成。

## 正式材料已核的候选

| 正式论文 / venue | 已取得正式材料 | 独立编号结果 | 实际证明或推导单元 | 位置（文件内PDF页） | 建议 |
|---|---:|---:|---:|---|---|
| [Defining and Quantifying the Emergence of Sparse Concepts in DNNs](https://openaccess.thecvf.com/content/CVPR2023/html/Ren_Defining_and_Quantifying_the_Emergence_of_Sparse_Concepts_in_DNNs_CVPR_2023_paper.html), CVPR2023 | 正文10+补充27 | 5 Theorems | 12，人工确数 | 补充C / PDF3：Th1；D.1 / PDF4–5：7性质；D.2 / PDF6–11：Th5,2,3,4 | 主推荐 |
| [Defects of Convolutional Decoder Networks in Frequency Representation](https://proceedings.mlr.press/v202/tang23i.html), ICML2023 | 34 | 8（5Th、2Cor、1Lemma） | ≥9 | 正文同文件附录A / PDF11–25 | 主推荐 |
| [Towards Theoretical Analysis of Transformation Complexity of ReLU DNNs](https://proceedings.mlr.press/v162/ren22b.html), ICML2022 | 22 | 0；另有3个Properties | 10个显式Proof段，人工确数 | B.1–B.4 / PDF13–15，逐页3、4、3段 | 主推荐 |
| [A Unified Game-Theoretic Interpretation of Adversarial Robustness](https://papers.nips.cc/paper/2021/hash/1f4fe6a4411edc2ff625888b4093e917-Abstract.html), NeurIPS2021 | 正文14+补充16 | 1 Proposition | ≥15 | 补充B.1–B.4 / PDF2–7：13段；D,G / PDF8–9：2段 | 主推荐 |
| [Building Interpretable Interaction Trees for Deep NLP Models](https://ojs.aaai.org/index.php/AAAI/article/view/17685), AAAI2021 | 10 | 0 | 3，人工确数 | Appendix / PDF8：Eq5、Eq6/7、Eq8三关系证明 | 次级 |
| [Interpreting Multivariate Shapley Interactions in DNNs](https://ojs.aaai.org/index.php/AAAI/article/view/17299), AAAI2021 | 10 | 0 | 1，已读附录关系推导 | Appendix / PDF9–10：B([A])与elementary interaction components关系 | 次级 |
| [Quantification and Analysis of Layer-wise and Pixel-wise Information Discarding](https://proceedings.mlr.press/v162/ma22b.html), ICML2022 | 35 | 0 | ≥2 | B / PDF12：Eq4推导；C / PDF12–13：concentration与IB关系 | 次级 |

正式Sparse的Theorem1陈述在supplement PDF2，实际necessity/sufficiency证明在PDF3；两部分合计一个证明单元。此前arXiv v6为38页、证明页段PDF14–23；正式文件为10+27页，表内计数与页码已按正式文件重新读取，不能沿用旧分页。七个性质不是七个编号定理。

NeurIPS官方landing/BibTeX使用`Towards a Unified Game-Theoretic View of Adversarial Perturbations and Robustness`，正式PDF首页使用`A Unified Game-Theoretic Interpretation of Adversarial Robustness`。PDF链接由该landing直接取得，作者/内容已对应，别名写入JSON。

Interaction Trees正式作者顺序已按首页改为Die Zhang、Hao Zhang、Huilin Zhou、Xiaoyi Bao、Da Huo、Ruizhao Chen、Xu Cheng、Mengyue Wu、Quanshi Zhang。其正式10页版含arXiv9页版缺少的附录证明。Multivariate Shapley正式10页版亦含旧arXiv版缺少的一段实际推导，不能据旧版缺附件就把正式版标成全部未取得。

## 正式材料缺口

| 论文 / 已确认发表身份 | 缺口与本轮事实 |
|---|---|
| A Unified Approach to Interpreting and Boosting Adversarial Transferability, ICLR2021 | [官方PDF](https://openreview.net/pdf?id=X76iqnUbBjz)、官方API及API2均403；web.open亦browser challenge。arXiv≥8证明只作发现证据。 |
| Interpreting and Boosting Dropout from a Game-Theoretic View, ICLR2021 | [官方PDF](https://openreview.net/pdf?id=Jacdvfjicf7)及两个API均403，未取得正式文件。 |
| Interpretable Complex-Valued Neural Networks for Privacy Protection, ICLR2020 | [官方PDF](https://openreview.net/pdf?id=SHDG97ukaIH)及两个API均403，未取得正式文件。arXiv A中5组操作证明不能填成正式版数。 |
| Can We Faithfully Represent Masked States to Compute Shapley Values on a DNN?, ICLR2023 | [官方PDF](https://openreview.net/pdf?id=YV8tP7bW6Kt)及两个API均403，未取得正式文件。 |
| Discovering and Explaining the Representation Bottleneck of DNNs, ICLR2022 | [官方PDF](https://openreview.net/pdf?id=iRCUlgmdfHJ)及两个API均403，未取得正式文件。 |
| [Batch Normalization Is Blind to the First and Second Derivatives of the Loss](https://ojs.aaai.org/index.php/AAAI/article/view/29978), AAAI2024 | 正式正文9页已取，有Th1–2及Cor1共3个编号结果；实际证明引用Appendices，正式附件未取得。第二galley31716下载后确认是Underline会议报告，不是supplement。 |
| [Clarifying the Behavior and the Difficulty of Adversarial Training](https://ojs.aaai.org/index.php/AAAI/article/view/29032), AAAI2024 | 正式正文9页已取，有Th1–6及Lemma1共7个编号结果；实际附录证明未取得。第二galley29957是Underline报告。正式作者名单不含旧预印本的Jie Ren。 |
| [3D-Rotation-Equivariant Quaternion Neural Networks](https://www.ecva.net/papers/eccv_2020/papers_ECCV/html/3539_ECCV_2020_paper.php), ECCV2020 | ECVA正文17页已取；arXiv21页版额外附录含的4类操作证明不在此文件，正式附件未取得。不能自动与后续TPAMI扩展合并。 |
| [Mining And-Or Graphs for Graph Matching and Object Discovery](https://openaccess.thecvf.com/content_iccv_2015/html/Zhang_Mining_And-Or_Graphs_ICCV_2015_paper.html), ICCV2015 | 正式CVF正文9页已取；作者官网另有18页Supplementary，人工读到3个长证明段（PDF2–11）。正式venue landing仅挂main，未独立核该作者附件的最终正式版本身份，故正式proof_count留空。 |
| [Towards a Deep and Unified Understanding of Deep Neural Models in NLP](https://proceedings.mlr.press/v97/guan19a.html), ICML2019 | 正式PMLR正文10页已取。个人主页所链Microsoft`camera_paper_with_supp_3.pdf`403；猜测PMLR独立supp路径404。完整证明附件未取得。 |

对前五篇亦试题名限定`proceedings.iclr.cc`检索，当前仅返回2024/2025论文的参考文献，未找到旧论文本文入口。不会反复冲同一403，也不会用预印本填补正式候选。

## 覆盖、材料数与排除口径

本次早期台账有59个arXiv作者查询记录，实际取得55个固定版本PDF。另有23篇非arXiv论文记录，取得24份PDF材料（ICCV2015正文/作者补充分开）。后来增取13份venue PDF材料。磁盘共92份PDF，92个不同SHA256；这里包含旧版、正式版、正文和补充，绝不是92篇待收录论文。

82行台账经明确重复/extended-abstract关系得到79个mergekey；剔除1项撤回及2个编辑合集后可识别76个独立研究工作组。该数字仍包括未核正式版本的作者职业期论文和预印本，不是76篇实验室正式论文。14个工作已至少取得正式venue正文，其中7个有可比较的正式证明结构候选，另外7个仍为附件待取得或低信号初筛。7个正式候选对应9份正式PDF材料（两篇正文/补充各分开）。

arXiv未取得普通PDF的4条有明确官方原因：

- [2203.14101](https://arxiv.org/abs/2203.14101)：作者撤回，官方说明due to critical issues。这里只转记撤回事实，不自行判断数学错误。
- [2111.03536](https://arxiv.org/abs/2111.03536)：作者说明误申新ID，previous=2103.07364，按同一工作合并。
- [2107.08821](https://arxiv.org/abs/2107.08821)、[1901.08813](https://arxiv.org/abs/1901.08813)：workshop proceedings仅HTML/HTML source；不是可把合集定理算给张拳石的独立研究论文。

1901.07538与1805.07468、1901.06978与1804.10272分别是作者已说明的extended-abstract/full-paper关系，保留材料但按同一工作mergekey。2010.04055与2207.11694是正式前期/扩展研究关系，不因主题相近自动合成同一版本。

`Proving Common Mechanisms Shared by Twelve Methods of Boosting Adversarial Transferability`的97页预印本有大量证明，`Trap of Feature Diversity in the Learning of MLPs`的35页预印本亦有证明，但当前未确证对应正式venue，只保留发现记录。不能从“证明多”直接推成满足用户“正式版”条件，也不把“未确证”写成永未发表。

## 官方索引核对与边界

从[SJTU JHC官方人员页](https://jhc.sjtu.edu.cn/people/members/quanshi-zhang.html)、[实验室官网](https://sjtu-xai-lab.github.io/)、[作者个人publication页](http://qszhang.com/index.php/publications/)及[SJTU计算机系人员页](https://www.cs.sjtu.edu.cn/jiaoshiml/zhangquanshi.html)交叉识别人员和论文。快照保存于`publication-index/`。个人publication页可枚举的76个PDF/arXiv链接条目已逐项映射；其中2016以前一些论文的首页单位是Tokyo/UCLA，明确作为作者职业期边界，不能都称SJTU实验室论文。

该76是“带PDF/arXiv链接模块”的枚举范围；无链接的publication模块不在这份派生枚举中。近期代理补查其中的近期venue-only记录，本目录不承诺所有无链接论文已穷尽。arXiv作者Atom共95个记录亦只是公开作者查询结果，不等于全世界或全实验室论文总数。`quanshizhang.com`无法打开、旧faculty publication接口超时；这些未用于作完整覆盖证明，抓取失败有日志。DBLP仅作为全局交叉线索，不能以反机器人HTML冒充可用XML目录。

实验室旧官网存在明显复用错误：Transformation Complexity与Information Discarding共用一个Paper链接；Interaction Trees/Quaternion部分链接复用Multivariate Shapley。此次实际核PDF首页题名与作者，不依据anchor邻近标题给错论文计数。

所有55个arXiv PDF及24个非arXiv材料均完成逐页关键词定位；高证明信号和重要无编号证明另人工读正文/附录。自动命中只用于定位，不作为独立证明确数。低信号未完全人工建立证明清单的论文仍标初筛/未决，数值留空；不把低相关、无关键词或只含引用证明写成“证明为0”。

OpenReview实际下载到的HTML是browser challenge，不是可用论文metadata页；`publication-index/source-quality.json`明确标记。部分OJS HTML响应gzip编码，原响应保留，另存`.decoded.html`用于读取。页数统一以pdfinfo为准，再逐页pdftotext抽取；不按全文控制符分割伪造PDF页数。

此轮只做版本和证明密度筛选，没有逐条数学审校、没有完整命题抽取，也没有任何Lean验证声明。后续正式处理范围仍以用户确认候选为准。
