# 当前状态：十二篇已构建，最终验收收尾

2026-10-01 当前活动输入和服务快照均为十二篇正式论文，新增六篇数学包已全部根准入。实际为14份正式 PDF、331页、358个库存入口、355个阅读结果、256个证明或推导目标和37份公共证明。全量浏览器检查正在收尾，随后只差分复测两条 Decoder 定义域状态元数据；最终计数与当前性以[十二篇整合报告](../reader/evidence/twelve-paper-20261001/twelve-paper-integration.json)为准。

最新用户顺序是：完成当前十二篇整体验收 → 更新记录文档 → 保存第二阶段计划 → 讨论 GitHub 配置。本轮不推送 GitHub，也不启动第二阶段正文或界面实现。根负责来源/数学准入与候选发布边界审查，软件通过不替代数学审阅。复现见[验收操作单](twelve-paper-validation-runbook-20261001.md)，根记录见[十二篇根审查](reviews/twelve-paper-root-audit-20261001.md)。

## 第一轮收尾与十篇历史中间版

以下十篇、八篇计数与检查保留当时的历史意义，不代表随后十二篇输入的当前验收。Decoder 最终数学报告296条声明已根准入，Transformation 后续实际模型报告222条声明也已重新准入；新增实用引理数不等于已证明论文目标数。

NeurIPS 2021 Robustness、ICML 2022 Transformation、NeurIPS 2024 Dynamics 与 ICML 2023 Bayesian 已由根代理独立核对并授权加入活动清单。十篇实际为十二份正式 PDF、275页、286个库存入口、283个阅读结果、198个目标和29份公共证明。来源、双语、目标闭合、符号、当前 Lean 报告与旧六篇保全检查通过；70项针对性回归通过，实际 KaTeX 21,303式无解析错误，475项当前 API 检查通过。

新增两篇有限浏览器初跑1,085项，其中1,065项通过、20个英文原文默认提示失败；47页来源图像全部实际解码，选定十条结果与八份新公共证明的中英正文、Lean、符号与问题可见性已核对。只补翻译层后，对受影响20面板重测645项全部通过，原图和数学内容字节未变。首次失败和受影响复测分别保留；这些检查不代替十二篇冻结后的全量浏览器验收。

十篇中间快照的 Lean 主证据角色为121个定理范围、38个部分范围、11个反例、28个无当前映射；完整重写证明正文118个，其余80个交付反例、部分结论或范围说明。角色与原命题判断是独立维度：当时 F04六个完整机器反例保持反例角色，Eq24 Gaussian适配仍为部分范围；后续完整模型补充见新准入，最终角色须重新计数。以上计数不能相加为已证明的原命题。旧六篇168个结果、15份公共证明及17个无映射目标全部保全。当时输入和页面实现绑定见[十篇整合检查](../reader/evidence/twelve-paper-20261001/ten-paper-integration.json)；本轮尚未发布。此前[八篇中间记录](../reader/evidence/twelve-paper-20261001/eight-paper-integration.json)保留其当时快照语义。

第一轮的公共库复用接口已增加独立扩展的真实 `import`、完整类型、公共源码和当前报告，保留基础0.2.0目录与旧barrel。独立 [ExtensionConsumer](../examples/library-consumer/ExtensionConsumer.lean) 组合三条RobustnessFinite公共引理，在非零基线下证明有限二阶上下文交互的仿射比例律；真实消费编译、Lean类型导出、传递公理与输入指纹见[消费报告](../reader/evidence/twelve-paper-20261001/direct-import-consumer-checks.json)。该例子只验证其实际陈述，不代替新增论文的全篇证明或未入站模块验收。新贡献/AI工作流见[CONTRIBUTING](../CONTRIBUTING.md)和[AI调用库](ai-use-library.md)，最终十二篇冻结仍需重绑全部API证据。

## 已验收基线：独立论文池与六篇双语整合

此前六篇验收日期：2026-10-01。活动输入为 `corpus/public/reader/input-manifest.json`，维护入口为 `reader/`，网页服务目录为 `reader/preview/`。六篇正式源共162页，新增ICML2023 HarsanyiNet、ICML2024 Layerwise、ICML2025 Coalition；来源、数学内容和机器验证的最终范围由新验收报告分别记录。

公开/私稿活动数据已物理分开，默认Store只public；私稿导入默认private，显式 `--private` 进入私稿管理。迁移602份文件哈希守恒、无丢件；公共27个theorem与私池theorem集合无交集，私稿单向引用公共库。迁移哈希与对象数量见 `reader/evidence/migration-summary.json`；详细私稿回滚映射只在被忽略的private池。根代理实际运行完整回归71项通过（7.47秒，本机有界回环HTTP），记录见 `reader/evidence/root-pytest-checks.json`；它们不代表数学内容已验收。

此前六篇严格构建为171个来源清单条目、168个结果页面、104个证明或推导目标、15份共享证明。66个目标交付完整证明正文，38个目标交付反例、部分结论或范围说明；214条来源符号记录映射到151个规范概念。183个结果/共享条目的严格双语覆盖通过，9,932条公式的本地KaTeX解析无错误。独立公式、步骤ID、状态与Lean机器映射跨语言保护；215项内联TeX字符串差异保留在报告并由翻译者进行语义审阅。

此前六篇证据按目标的实际主证据角色互斥记录为69个定理、16个部分范围、2个反例、17个无当前映射目标。新篇分别为HarsanyiNet 10/4/0/1、Layerwise 5/2/0/2、Coalition 6/8/0/5；四项依次为定理/部分范围/反例/无当前映射。部分范围目标也可包含形式化反例，HarsanyiNet空感受野引理与CNN门控子句即保留这种组合，因此主反例角色为0不表示没有机器反例。定理角色并非无条件原命题证明，实际类型、定义域和来源判断仍须逐条读。机器可复算计数见 `reader/evidence/status-summary.json`，脚本为 `reader/summarize_status.py`。新论文独立实际报告分别42/33/59个声明；基础三包160个声明（154个公共API）已实际重验，报告为 `reports/lean/20261001T032325-2/report.json`，各组重叠声明不能相加成论文证明数。

双语与浏览器报告在 `reader/evidence/`，最终浏览器报告以绑定的快照哈希为准。GitHub连接实际写入接口返回403，尚未通过该连接发布，详见 `reader/evidence/root-github-write-check.json`；本机辅助脚本与凭据方法见[上传说明](github-upload.md)。

下文为2026-09-30三篇已验收的历史记录，其计数不能作为六篇当前计数。

# 历史记录：三篇全篇整合已验收并更新阅读入口

更新日期：2026-09-30。两名数学代理核查和重写，一名代理整理数据与网页，根代理独立核对来源、类型、报告和阅读结果。本轮既有 `gpt-6.1-sol / max` 代理已交付；此后新代理使用 `gpt-6.1-sol / xhigh`。

本轮授权覆盖三篇正式论文的正文、附录和 CVPR 官方补充材料。用户已允许直接修正原证明并标出原错处；**原命题及假设不能改变，错误命题单列**。操作授权不等于用户已逐条认可数学判断。

## 来源与目录

| 论文 | 正式 PDF 页数 | 来源清单条目 | 阅读条目 | 证明/推导覆盖目标 |
| --- | ---: | ---: | ---: | ---: |
| CVPR 2023 Sparse Concepts | 10 + 27 | 29 | 28 | 16 |
| ICLR 2024 Sparse Interaction Primitives | 34 | 43 | 42 | 27 |
| ICLR 2024 Generalizable Interaction Primitives | 23 | 30 | 30 | 18 |
| 合计 | 94 | 102 | 100 | 61 |

来源清单记录原始出现，阅读条目保留定义、方法和实验材料；61 个目标还包括母定理与子结论，所以不是 61 个相互独立的定理。根代理已重新计算四份正式 PDF 的 SHA-256，并核实逐页台账覆盖全部页且无重复：[来源/页码检查](../research/full-proof-integration-20260930/root-audit/source-inventory-check.json)。这项机器检查不代替逐页数学审查。

当前入口代码与数据在 [full-proof-integration-20260930](../research/full-proof-integration-20260930/README.md)。8001 已切换到最终快照，三篇原有路径保持。冻结构建、来源、数学边界、服务与全部验收证据见[根代理最终验收](../research/full-proof-integration-20260930/root-audit/acceptance.md)。

61 个目标中，48 个完成原文所述定义域内的中文证明与当前 Lean 证明，2 个只证明复合陈述的部分，4 个完成未量化/外引主张的范围说明，7 个保留原文数学问题与反例或条件分析；所有目标保留在分母。共有 15 份公共证明、101 条规范符号记录、34 条问题记录。用户阅读质量验收仍需由用户判断，不能由代理的软件测试代替。

## 真实 Lean 证据

| 验证范围 | 实际审计声明数 | 当前报告 |
| --- | ---: | --- |
| 有限集合、经典归因、CVPR 与 Generalizable 有限适配 | 117 | [有限组报告](../research/full-proof-integration-20260930/cvpr2023/verification/report.json) |
| Sparse 系数与计数、Generalizable 重参数和真实概率方差 | 73 | [分析组报告](../research/full-proof-integration-20260930/iclr2024-sparse/verification/report.json) |
| 经典混合偏导截断与实际坐标掩码适配 | 36 | [导数组报告](../research/full-proof-integration-20260930/cvpr2023/verification/derivative-report.json) |
| 公共库、PaperProofs、独立调用包 | 160 | [统一构建报告](../reports/lean/20260930T133803-2/report.json) |

这些范围有重叠，声明数不能相加成论文证明数。统一报告的 160 条中，154 条为公共 API、2 条为 PaperProofs、4 条为独立调用包；公共 API 包括 39 个定义、101 个定理、1 个结构类型、1 个构造器和 12 个投影。当前公共版本为 0.2.0，Lean 4.24.0 与 mathlib 提交 `f897ebcf72cd16f89ab4577d0c826cd14afaafc7` 固定。

根代理实际运行了统一构建，读取各组报告、实际类型与关键源码，并重新核对输入哈希；通过报告只含 `propext`、`Classical.choice`、`Quot.sound`，没有 `sorryAx`。有限组补足了任意掩码标签分解，未添加 `x_i≠r_i`。Sparse Eq.(62) 保留作者两个分量空集为零的前提，分别证明分量与父式。导数截断使用经典导数存在且高阶为零的条件，经均值定理证明，没有补解析性。

## 数学问题与证明边界

原文与改写分别存放，问题定位到正式来源页和原式。重构、归因、系数存在性等原证明中的索引、符号和漏分支问题已按同一结论修复。完整结果、部分子句、反例和未量化主张分别保存。

特别需要保留边界的内容包括：CVPR 含空集的 Dummy 原陈述与截断基线损失子句；Sparse 的一般 Taylor 表示读法、噪声独立性、空集 parity 约定、同类别到全局稀疏的推断以及第 8 页 Case 2 推断；Generalizable 的未量化近似、Eq.(10) 的自由索引和逐点范数子断言、整体运行时与查询数的区别。Case 2 的新反例满足原三项假设，但不否定 Theorem 2、3 的精确等式/界。不能把这些条目改成更弱的命题后标作原命题证明成功。

[根代理逐项复核记录](reviews/full-integration-root-crosscheck-20260930.md)保存实际来源检查、发现及修复范围；两名数学代理的独立交叉报告保存在各自研究目录。最终汇总已绑定冻结数据，不能将“正文已写”或“反例编译通过”混作原命题已证明。

根代理核对全部 303 条步骤映射的实际类型、当前报告与源码、行号和下载副本；最终浏览器 1,789 项检查、3,737 条公式解析通过，另有 35 项整合 API/schema 检查与 13 项根代理独立 API 检查。真实浏览器覆盖所有阅读条目与适用标签、共享页面、问题页、搜索、符号和移动页面；没有脚本错误或外部请求。这些是软件与证据检查，不是数学正确性的替代证据。

## 人与 AI 接手

[项目入口](../README.md)、[本轮复现](../research/full-proof-integration-20260930/README.md)、[数据接口](paper-agent-data-model.md)、[新增论文流程](agent-extension-workflow.md)、[文字到 Lean](human-to-lean.md)、[公共库 API](library-api.md)与[AI 调用库](ai-use-library.md)均指向当前实现。新增正式论文通过 manifest 配置。该查询接口是本地只读工具，没有部署 MCP 服务。

私稿继续使用 `inbox/<paper>/` 和本地 `scripts/archive`，默认 private/unpublished。项目环境、Lean、缓存、临时文件均位于项目目录内；原 `mainText.pdf`、私有档案和历史来源保持，没有上传或进入公开 manifest。

## 历史与范围外

[正式版候选表](paper-candidates-20260930.md)的 17 篇候选及 15 项材料缺口仍待整批范围确认；本轮三篇全文授权不自动扩大收录范围。旧版阅读器、首版生产 corpus、其测试及私稿报告保留，各自的历史数字不能与本轮相加。旧阶段完整文字快照存于 `docs/history/`（内部相对链接仍以其原文件位置理解）。

尚未完成的其他研究包括私稿其余命题的审校/形式化、更广候选论文的收录，以及原文未量化主张的进一步数学讨论；这些不是本轮三篇中被遗漏的普通实现工作。
