# 近期正式版证据（截至2026-09-30）

用户最新要求只取正式版。本部分14篇正式公开PDF已逐篇核对，另4篇正式期刊元数据已核实、正式全文未取得。arXiv初筛保存在历史台账，不能替用其计数。候选仍待用户确认，没有正式导入。

计数分别表示独立编号陈述、本地有专门证明的编号目标、证明/推导块及含证明的PDF物理页，不能相加。正文与附录同一陈述去重；一个多部分Proof块计一次，独立Proof块分别计。引用定理、方法公式、数据解题例和未展开草图不计完整证明。计数是文件内容人工清点，不等于数学正确性全面审稿。

|正式题名/来源|发表年及venue|证明/推导单元|独立编号结果|本地编号证明|PDF证明页|编号/章节定位|
|---|---|---:|---:|---:|---|---|
|[Where We Have Arrived in Proving the Emergence of Sparse Interaction Primitives in DNNs](https://proceedings.iclr.cc/paper_files/paper/2024/hash/db0ee27cb50dd9087b133f6e7d28a90e-Abstract-Conference.html)|2024 ICLR|11|10|10|15–27|B.1 Theorem 1; B.2 Lemma 1; B.2 Assumption 1-β implies 1-α; B.3 Lemma 2; B.3 Lemma 3; B.3 Theorem 2; B.4 Main Theorem 3, appendix mislabels it Theorem 6; B.5 Lemma 4; B.5 Theorem 4; B.6 Theorem 5; B.7 Theorem 6|
|[Towards Attributions of Input Variables in a Coalition](https://proceedings.mlr.press/v267/zheng25d.html)|2025 ICML|10|7|7|12–21|C Theorem 3.2 (appendix label Theorem 2); D Theorem 3.3 (appendix label Theorem 3); E Theorem 3.4 and Corollary 3.5; F Theorem 3.6 and Corollary 3.7; G.1 Anonymity; G.2 Symmetry-α; G.3 Symmetry-β; G.4 Additivity; G.5 Dummy; G.6 Corollary 3.8 / Efficiency|
|[Towards the Dynamics of a DNN Learning Symbolic Interactions](https://papers.neurips.cc/paper_files/paper/2024/hash/5aa96d1caa0d0b99d534b67df06be2ff-Abstract-Conference.html)|2024 NeurIPS|8|9|7|16–24|F.1 Theorem 2 universal matching; F.2 Lemma 3; F.2 Equations (6) and (7); F.3 Lemma 1; F.4 Theorem 3; F.5 Lemma 2; F.6 Theorem 4; F.7 Theorem 5|
|[Bayesian Neural Networks Avoid Encoding Complex and Perturbation-Sensitive Concepts](https://proceedings.mlr.press/v202/ren23a.html)|2023 ICML|6|7|6|15–22|G.1 Lemma 2.1; G.2 Theorem 2.2; G.3 Theorem 2.3; G.4 Theorem 2.4; G.5 Theorem 2.5; G.6 Theorem 2.6|
|[HarsanyiNet: Computing Accurate Shapley Values in a Single Forward Propagation](https://proceedings.mlr.press/v202/chen23s.html)|2023 ICML|5|5|4|12–14, 16|B Theorem 2; B Theorem 3; B Theorem 4; C Lemma 1; E Harsanyi-CNN Setting 2|
|[Towards the Difficulty for a Deep Neural Network to Learn Concepts of Different Complexities](https://papers.neurips.cc/paper_files/paper/2023/hash/8143b8c73073a9a23b9c18e400066471-Abstract-Conference.html)|2023 NeurIPS|4|5|3|17–21|G.1 Theorem 2; G.2 Theorem 3; G.3 Theorem 4; G.4 Concepts and multi-order interactions|
|[Defining and Extracting Generalizable Interaction Primitives from DNNs](https://proceedings.iclr.cc/paper_files/paper/2024/hash/67a9b444cbcd647572c88194619f72d5-Abstract-Conference.html)|2024 ICLR|2|4|1|12–15|C Theorem 2: AND, OR, combined under one Proof block; D Variance of AND/OR interactions|
|[Layerwise Change of Knowledge in Neural Networks](https://proceedings.mlr.press/v235/cheng24b.html)|2024 ICML|2|2|2|15–16|F Theorem 3.3; G Lemma 3.4|
|[Explaining Generalization Power of a DNN Using Interactive Concepts](https://ojs.aaai.org/index.php/AAAI/article/view/29655)|2024 AAAI|1（近似推导）|3|0|5–6|Main pp5–6 Taylor/moment and approximate variance-growth analysis|
|[Towards the first principles of explaining DNNs: interactions explain the learning dynamics](https://doi.org/10.1631/FITEE.2401025)|2025 FITEE|0|0|0|—|Full acquired formal PDF inspected; no local proof block verified|
|[Monitoring Primitive Interactions During the Training of DNNs](https://ojs.aaai.org/index.php/AAAI/article/view/34223)|2025 AAAI|None（仅正文，附件未核实）|1|0|—|Theorem 2.1 at PDF p3 points to proof in Appendix E, which is absent from the acquired official nine-page PDF|
|[Does a Neural Network Really Encode Symbolic Concepts?](https://proceedings.mlr.press/v202/li23at.html)|2023 ICML|0|0|0|—|Full acquired formal PDF inspected; no local proof block verified|
|[Identifying Semantic Induction Heads to Understand In-Context Learning](https://aclanthology.org/2024.findings-acl.412/)|2024 Findings of ACL|0|0|0|—|Full acquired formal PDF inspected; no local proof block verified|
|[Challenging the Explanation Based on Preceding Tokens: Discovering Transferable Non-Literal Biasing](https://aclanthology.org/2026.acl-short.52/)|2026 ACL (short papers)|0|0|0|—|Full acquired formal PDF inspected; no local proof block verified|

ICLR2024 Sparse：34页正式版，B.7证明延续到27页；正文Theorem3在B.4误标Theorem6，按内容去重后10个编号目标及11个证明块。Generalizable：正式版23页，C/D证明在12–15页，未沿用24页arXiv版页码。
NeurIPS2023 Difficulty：main与supplement URL下载SHA256相同，22页含同一附录，仅计一次；G.1–3三个定理证明加G.4完整关系推导=4单元，G.5回归三步草图另记1，不计完整证明。
AAAI2025 Monitoring：仅取得9页正式正文，Theorem2.1明确指向未取得AppendixE；整体证明量未核实。AAAI2024 Generalization的1单元是正文近似方差分析，与完整编号定理证明区分。
四篇待取得期刊PDF：Taylor TPAMI2024、Attribution Survey TPAMI2026、Attribute Obfuscation TPAMI2025、Introspective Math Word Problems TASLP2024。IEEE存入Crossref的题名、发表信息、ORCID及SJTU作者身份已核；官方PDF接口HTTP418，证明数均null，未用预印本补位。

原95条arXiv作者查询仅用于发现分母，近期36个主PDF全部已查；有2份首三页未给个人作者身份，不冒充PDF身份核实。正式14篇PDF均实际核实张拳石及SJTU身份。所有原始发现PDF保留，预印本不进入正式候选主表。数学疑点仅保留在原预印本调研记录，未影响正式候选建议。
