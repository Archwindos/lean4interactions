> 历史调研：以下分类先于用户“只取正式版”约束；不作为当前收录建议。以papers.json及findings.md正式版结果为准。

> 历史调研：以下分类先于用户“只取正式版”约束；不作为当前收录建议。以papers.json及findings.md正式版结果为准。

# 近期候选筛查结果（冻结版）

截至2026-09-30，本部分实查36篇首次arXiv公开于2023–2026的论文和4篇额外官方发表论文，共40篇独立候选；建议优先11、次级16、附件待核实3、证明较少或未见本地证明10。没有将候选正式导入。

## 建议优先候选（全部列出）

|合并键|题名|研究内容|证明/推导单元|编号结果|PDF页|建议依据|
|---|---|---|---:|---:|---|---|
|2605.11404|[Attributing Emergence in Million-Agent Systems](https://arxiv.org/abs/2605.11404v2)|研究百万Agent系统涌现的可扩展归因；分析精确离散归因的困难，提出连续Aumann–Shapley方法并验证归因公理。|8|3|14–17|百万Agent规模归因包括3编号结果和连续归因的4个公理验证；非线性部分明确只证明特定家族反例，未把开放强结论算成证明。|
|2505.01007|[Towards the Resistance of Neural Network Watermarking to Fine-tuning](https://arxiv.org/abs/2505.01007v1)|在频域分析神经网络水印抗微调能力，研究DFT结构、缩放/置换及相关抵抗条件；附录包含多个独立数学证明。|5|7|11–15|水印抗微调的频域理论，包含DFT/几何级数/缩放与置换等多个独立数学目标。|
|2410.04421|[Disentangling Regional Primitives for Image Generation](https://arxiv.org/abs/2410.04421v3)|把图像生成的区域primitive分解为OR逻辑特征分量，研究分量等价表示、可加性及输出重构。|4|3|14–15|生成网络区域primitive的OR逻辑分解；3编号结果、4证明块，原子目标适合复用。|
|2407.19198|[Towards the Dynamics of a DNN Learning Symbolic Interactions](https://arxiv.org/abs/2407.19198v2)|解释DNN学习符号交互的两阶段动态，分析参数噪声、Taylor触发函数、交互阶数与最优回归权重。|8|9|16–24|符号交互学习两阶段动态；含参数噪声、Taylor触发函数、最优回归权重的多步证明。|
|2401.16318|[Defining and Extracting generalizable interaction primitives from DNNs](https://arxiv.org/abs/2401.16318v2)|定义并提取可泛化的AND/OR交互primitive，分析任意mask输入的精确重构和交互方差，验证primitive跨模型或输入的泛化。|2|4|13–16|generalizable AND-OR交互的基础构造；两组实际证明，不能把引述的基础定理再算本论文证明。|
|2309.13411|[Towards Attributions of Input Variables in a Coalition](https://arxiv.org/abs/2309.13411v3)|指出将单变量归因直接相加可能与coalition归因冲突，构建coalition的AND/OR分配并证明相关定理和归因公理。|10|7|12–21|Coalition归因冲突及AND-OR重新分配；定理/推论7项，证明小节10项，编号前缀在附录省略。|
|2305.01939|[Where We Have Arrived in Proving the Emergence of Sparse Symbolic Concepts in AI Models](https://arxiv.org/abs/2305.01939v2)|在明确网络条件下研究稀疏符号交互的涌现，构造组合矩阵关系、阶数/数量上界，并连接多种Shapley指标。|11|10|15–26|稀疏交互涌现主理论；组合矩阵、阶数上界及Shapley三种指标关系有完整多页推导。|
|2304.01811|[HarsanyiNet: Computing Accurate Shapley Values in a Single Forward Propagation](https://arxiv.org/abs/2304.01811v2)|设计HarsanyiNet使一次前向传播精确计算Shapley值，证明网络交互结构与归因关系，并推广到CNN构造。|5|5|12–14, 16|HarsanyiNet精确Shapley构造及CNN扩展；四个本地有编号证明，加一个CNN无编号结论证明。|
|2303.01506|[Understanding and Unifying Fourteen Attribution Methods with Taylor Interactions](https://arxiv.org/abs/2303.01506v2)|用Taylor交互统一14种归因方法，分别建立各方法与交互项的对应关系，包含16个独立编号理论目标及证明。|16|16|18–25|Taylor交互统一14种归因方法；16个独立编号目标，每一目标都有实际证明块。|
|2302.13095|[Bayesian Neural Networks Avoid Encoding Complex and Perturbation-Sensitive Concepts](https://arxiv.org/abs/2302.13095v2)|研究BNN为何避免复杂且扰动敏感的概念，连接交互阶数、Taylor展开、随机变量矩及回归权重。|6|7|15–22|BNN不确定性、交互阶数与敏感性之间的理论联系；含Taylor/随机变量及回归权重推导。|
|venue:neurips2023:8143b8c73073a9a23b9c18e400066471|[Towards the Difficulty for a Deep Neural Network to Learn Concepts of Different Complexities](https://papers.neurips.cc/paper_files/paper/2023/hash/8143b8c73073a9a23b9c18e400066471-Abstract-Conference.html)|理论解释复杂交互概念为何难学，分析Taylor触发函数的扰动方差、概念二值激活、与多阶交互的关系及简化回归模型的学习困难。|4|5|17–21|3个本地编号证明加1个完整关系推导，理论涉及Taylor、随机变量和组合求和；回归草图另记，避免夸大证明完整性。|

## 完整性限制

36篇近期arXiv主PDF全部取得、完整转换；其中2份首三页缺个人作者身份，仅保留查询元数据。4篇venue-only核对公开PDF身份。TASLP2024另一条仅有DOI/ORCID元数据的线索保留discovery，不算已实查。
作者Atom的95项是可复现检索分母，不等于作者全部发表论文。官方个人publicationlist更新到约2024；实验室主页更旧且部分Paper链接错复用。补充检索使用arXiv、PMLR、NeurIPS、AAAI、ACL及FITEE官方来源，但不宣称网上绝无遗漏。
2608.06839、2512.18607、AAAI2025 Monitoring的公开正文明确指向未取得附件，整体证明数量待查；2505.06993也有正文提及但未提供附录C的缺口。
综述/基础技术说明（2304.13312、2508.07636、FITEE2025）保留为secondary：用于研究内容与理论体系导读，本地proof=0不能列为证明密集成果。
没有按研究题目淘汰LLM、Agent、EEG或系统论文；均以实际正文和附录核查结果分类。推荐级别是调研建议，是否收录仍待用户确认。
