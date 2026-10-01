# 近期正式版候选筛查结果

截至2026-09-30，已实查14篇正式版：优先建议7篇、次级参考3篇、正式附件待取得1篇、证明较少3篇。另有4篇正式期刊全文待取得，证明数量未核。只有取得并核对正式PDF的recommend/secondary共10篇进入待用户确认表。

|题名|正式版|证明/推导单元|独立编号结果|PDF页|建议理由|
|---|---|---:|---:|---|---|
|[Where We Have Arrived in Proving the Emergence of Sparse Interaction Primitives in DNNs](https://proceedings.iclr.cc/paper_files/paper/2024/hash/db0ee27cb50dd9087b133f6e7d28a90e-Abstract-Conference.html)|ICLR 2024|11|10|15–27|证明密集：10个独立编号结果均有本地证明，加1个假设蕴含证明；含组合矩阵、稀疏上界及三种Shapley指标关系。|
|[Towards Attributions of Input Variables in a Coalition](https://proceedings.mlr.press/v267/zheng25d.html)|ICML 2025|10|7|12–21|证明密集：7个编号定理/推论、10个证明小节；coalition与单变量归因关系及AND/OR分配公理可逐项对齐。|
|[Towards the Dynamics of a DNN Learning Symbolic Interactions](https://papers.neurips.cc/paper_files/paper/2024/hash/5aa96d1caa0d0b99d534b67df06be2ff-Abstract-Conference.html)|NeurIPS 2024|8|9|16–24|证明密集：7个本地有专门证明的编号目标及一个方程证明，涵盖噪声、Taylor触发函数、回归最优解和两阶段动态。|
|[Bayesian Neural Networks Avoid Encoding Complex and Perturbation-Sensitive Concepts](https://proceedings.mlr.press/v202/ren23a.html)|ICML 2023|6|7|15–22|证明密集：6个编号目标有对应证明，连接BNN不确定性、概念复杂度、扰动矩及回归权重；Prop G.1声明未算额外证明。|
|[HarsanyiNet: Computing Accurate Shapley Values in a Single Forward Propagation](https://proceedings.mlr.press/v202/chen23s.html)|ICML 2023|5|5|12–14, 16|证明较集中且Harsanyi基础重要：精确Shapley网络构造有4个本地编号证明及1个CNN扩展证明，适合连接核心有限集合理论。|
|[Towards the Difficulty for a Deep Neural Network to Learn Concepts of Different Complexities](https://papers.neurips.cc/paper_files/paper/2023/hash/8143b8c73073a9a23b9c18e400066471-Abstract-Conference.html)|NeurIPS 2023|4|5|17–21|3个本地编号证明及1个完整组合关系推导，解释复杂概念的学习难度；G.5回归草图另记、不充当完整证明。|
|[Defining and Extracting Generalizable Interaction Primitives from DNNs](https://proceedings.iclr.cc/paper_files/paper/2024/hash/67a9b444cbcd647572c88194619f72d5-Abstract-Conference.html)|ICLR 2024|2|4|12–15|证明数量不多，但Harsanyi/AND-OR基础重要：精确重构和方差共2个证明单元；引用的Theorem 1/3及Prop 1不额外算本地证明。|

完整逐篇原文定位、研究内容、固定来源PDF/sha256及计数依据在papers.json与formal-proof-inventory.json，验证结果在validation.json。综述、基础技术说明及单个近似推导均明确区分；不是所有推荐项都称证明密集。
未确证正式发表的预印本（包括2026最新符号pattern、百万Agent、水印、区域primitive等）只保留discovery；用户“只取正式版”要求优先于此前预印本推荐。未在网上取得附件不等于论文没有证明，未宣称检索绝无遗漏。
