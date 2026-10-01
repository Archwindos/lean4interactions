# 正式版论文候选：独立验收报告

验收通过，未解决错误为0。验收仅针对2026-09-30冻结的17项候选、15项正式材料缺口和3项正式版低优先人工筛查记录；候选仍待用户确认，不代表已正式收录、完成证明重写或Lean验证。

| 项目 | 独立核查结果 |
|---|---:|
| 正式版候选 | 17（优先11、次级与导读6） |
| 正式材料缺口 | 15（整体证明数均未核实） |
| 候选独立正式PDF | 19（17份正文及2份补充） |
| 本轮正式材料核查集合 | 26篇取得正文、28份非重复正式PDF |
| 本地文件核查 | 29份PDF路径，包括1份与正文同SHA256的重复supp |
| 正式PDF首页题名与作者次序 | 17/17通过，含近期10/10 |
| 最终表与CSV | 32个稳定ID与对应字段一致，用户决定全部待确认或待材料后确认 |

28份非重复材料及重复supp的文件存在、SHA256、实际PDF页数与当前记录一致。13项候选另有缓存的正式venue citation元数据可核，4项依据已有正式PDF来源记录及PDF出版标识核身份；本轮没有联网重新取得来源。NeurIPS2021 Robustness的landing题名与PDF题名不同，但作者、正式文件标识和已登记题名别名一致。

正文和补充文件的证明页码分别按各PDF的物理页定位，所有候选页段在对应文件范围内。抽查近期有证明/推导的9项首个定位页，并保留标题和上下文；没有重新逐一计算全篇Proof数量。编号陈述数、已有本地证明目标数、Proof/独立推导单元和人工下界各保留原口径，不能相加成独立定理数，也没有做跨论文共享证明去重。

FITEE2025 Personal View的0项是导读参考；AAAI2024 Generalization的1项明确标为近似推导；Generalizable虽只有2项，推荐依据是基础相关性。这些条目没有统称大量完整证明。Monitoring和其余材料缺口的整体proof_count均为null，未用正文未见证明或未取得附件推成全篇0。候选实际来源及计数版均为正式文件；arXiv去重键与嵌套发现记录仅作为历史线索保留。

本轮发现的两处元数据问题已交原所有者修正并复验：Sparse与Robustness的顶层total_pages现在对应正文10/14页，材料合计分别37/30页；W14的正式正文10页已补入材料记录，表与CSV显示“正文10页；补充待取得/核实”，整体证明数继续未核实。没有自行修改其他代理所有文件。

两项earlier材料仅做过自动初筛，最终留在discovery_only，不进入上述正式材料计数，也不据此断言证明少。原论文命题的数学正确性与修正不在本轮范围内；已有ICLR2024 Sparse编号误标说明继续保留，没有改原陈述、补假设或改证明。

机器报告与冻结文件SHA256见[report.json](report.json)。逐文件证据见[input-file-checks.json](input-file-checks.json)，首页身份见[title-author-checks.json](title-author-checks.json)，正式来源记录见[publication-source-checks.json](publication-source-checks.json)，抽查定位见[proof-scope-samples.json](proof-scope-samples.json)，表与CSV一致性见[selection-consistency.json](selection-consistency.json)。报告对应的输入与交付物快照均在机器报告中记录。
