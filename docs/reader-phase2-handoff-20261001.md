# Reader 第二轮交接

第二轮使用用户指定的 `gpt-6.1-sol / high`；根也使用 high。最新用户要求先完成检查与记录、保存第二阶段计划，再讨论 GitHub 配置；本轮不推送或实施第二阶段，后续明确授权后才切换。工作仍仅在项目内，`login:false`、`source scripts/env.sh`，环境/缓存/临时文件留在项目。不得读私稿、旧 token 或本机上传脚本。

## 接续入口

- 第一轮执行与停止门：[最终 runbook](twelve-paper-validation-runbook-20261001.md)。第一轮最终报告目标为 `reader/evidence/twelve-paper-20261001/twelve-paper-integration.json`，以其真实完成状态及 hash 为准。
- 当前数据：`corpus/public/reader/input-manifest.json` → `reader/data/full-content.json` → `reader/preview/data.public.json`；构建/当前性证据在 `reader/evidence/twelve-paper-20261001/`，维护工具在 `reader/`。
- 根授权与数学准入：[发布契约](twelve-paper-release-20261001.md)、`root-f01/f04/f06/f07/f08/f10-admission.json`、根审查台账与实际 `root-review-requirements.json`。出现数、results、targets、shared 和 Lean declarations 分开计数。
- 真实任务设计：[四条阅读路径评估](reader-workflow-evaluation-20261001.md)、[设计补充](reader-workflow-design-supplement-20261001.md)。基于长证明、错误命题、公共证明、符号映射四条实际路径复核改善。
- 数据/公共模块说明：[数据契约](paper-agent-data-model.md)、`reader/architecture/admission-contract.json`、[公共 API](library-api.md)、[AI 调用](ai-use-library.md)、[扩展流程](agent-extension-workflow.md)。精确类型与 import 来自当前实际报告，不把新增扩展算进基础 154 条或改旧 barrel。

## 第一轮收尾状态，待最终报告替换

当前 manifest 与已服务 preview 均为12篇，355 results /256 targets /37 shared /14正式 PDF /331页。全量浏览器旧快照 data SHA `35589c845d574f86dea3d6ca0b32c08b810b1d41e39cd451e75b8320fc6f9dab`，UI SHA `1582953670b3cee8559e9468e2486abf9689a67743e6d4139d8240bf467b3049`。两条 F06 定义域状态元数据在全轮结束后最小修正，最终快照与差分承接关系以最终整合报告为准；331源图、正文、Lean 未变时不重复全量验收。八篇、十篇和首次失败证据保留历史意义。

第一轮已实现必要语义修复：作者转录/项目译述/无作者独立证明的源说明正确分类；非目标定义/实验使用“条目说明”，有真实 Lean 的定义仍能看证据。这些不是第二轮布局重排。实际候选 Chromium 专项检查见 `source-and-material-presentation-candidate-checks.json`；发布后以完整十二篇 browser 与 source-presentation 报告为准。

## 第二轮已认可方向

- 默认连续阅读：结论、源命题判断和本页有效范围 → 本条条件/局部符号 → 论文完整论证 → Lean 证据入口。显著数学问题不得藏入低频菜单。
- 作者原文一个对照入口；下载/JSON/源码等低频操作集中收纳。所有返回保留语言与当前步骤/阅读位置。
- 公共证明稳定独立链接、实际前提适配，保留一份权威正文。F06 四份 shared 目前复制整段 paper steps 并改 ID；数学作者先改为真实引用与适配，不靠 UI 文本去重隐藏重复。
- `reader.js` 的 `relatedPapers/currentShared` 还只用单数 `shared_proof_id`；第二轮统一使用实际数组入口，对所有共享 ID 的交集去重，不按标题或首个 ID 猜关系。
- 符号详情按需渲染，保留全数据搜索、所有映射/冲突、深链接与就地查看。十篇符号页曾有 58,765 DOM 节点、约 1.04s；用同任务实测，不删字段降低数字。
- κ页条件中的裸 `U_x/C_x`、`sigma/m0` 工程拼写按实际数学边界补 TeX；KaTeX零错不能证明全部数学已渲染。根已记录实际截图，留第二轮处理。
- Lean 优先呈现实际源码声明、明确前提/结论与当前步骤对应；完整机器类型、公理与报告可展开。不得字符串替换改变机器证据。

## 保全与文件所有权

第二轮不再用旧重写字段 byte-identical 作为总体标准；保全正式原件、真实作者原文、稳定 ID 与无目标丢失，另列明确允许变更和源边界纠正例外。`f11-matching-metric` 的原字段混入项目中文注，应依据正式 PDF21 Appendix M 分离并保存旧字段/例外依据；原作者式保留 `m/v`，规范式可用 `rho/g/b`，AND/OR 索引不误合并，零分母不补值。`layer-universal-matching` 遗留 proof_scope 需按实际适配核对，不能凭统计自动升降。

整合代理拥有 `reader/`、全局 manifest、机器接口、软件检查与维护文档；数学代理拥有对应论文数据、规范证明/符号/共享适配和 Lean 源码/报告；根拥有授权、root-* 证据、最终审查与 GitHub 提交。阶段切换时根指定新的 high 代理及全十二篇数学分工，先确认文件所有权，不能多个代理改同文件。第一轮归属为 foundation(F01/F04/F06)、dynamics(F07/F08/F10)，旧六篇第二轮归属另由根分派。

复用已通过且仍当前的证据，只在新变化、失败或未解决问题涉及的范围复测；数据普遍变化才重跑完整浏览器。标准不降低，软件通过不核销数学缺项。publication 由根执行，公开证据只记路径分类/计数/结论。
