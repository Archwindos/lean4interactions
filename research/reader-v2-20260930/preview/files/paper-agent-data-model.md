# 论文与定理数据模型：v2 研究示例

本轮提供三篇正式论文的选定结果、原文定位、共享证明和只读查询接口。它是可运行的本地研究示例；生产库迁移、MCP 协议服务、远程部署和自然语言对话层均未实现。三篇分别拥有论文 ID 与独立页面，补充材料与附录只是同一论文版本的来源，不增加论文数。

设计参考 [Miao et al., Reimagining research papers as interactive and reliable AI agents, Nature, 2026-09-16](https://www.nature.com/articles/s41586-026-11044-y)。文章提出 tools/resources/prompts，要求可执行工具经过真实验证并保存溯源，也允许相关论文共用服务；讨论部分保留人的科学判断。这些是文章主张。下述命题、证明、适配、问题和状态模型是本项目为数学阅读与 Lean 证据设计的契约，文章没有给出这些字段，也不意味着本项目已经接通 MCP。

## 可读真源与三个投影

项目根目录为 `/mnt/data2/wyh/lean4project`。`research/reader-v2-20260930/data/papers.json` 提供论文标题、作者、选定结果、正式版本及不可变 PDF 来源；`data/math-content.json` 由数学代理提供中文证明、公式与逐步 Lean 对应；`architecture/agent-package.json` 保存实体、显式边、资源、工具和流程入口。以上后两个缩写路径都相对于 `research/reader-v2-20260930/`。

`data/source-excerpts/metadata.json` 给出固定来源、哈希、PDF 一基页码、定义和证明边界；旁边的 `.tex` 是经 agent 核对的公式转录，`.txt` 是页文字抽取快照，均不能冒充作者 TeX 源码。正式原件仍在 `research/paper-survey-20260930/`；本轮没有覆写原 PDF、历史 corpus 或生产 schemas。

`architecture/package.schema.json` 声明结构。运行时没有安装新的 JSON Schema 依赖；`paper_agent.py` 的受限验证器只支持此 schema 用到的关键词，对未支持的 schema 关键词直接报错。不能仅凭 JSON 能解析就认为数据有效：结构验证和跨实体语义验证必须一起运行。

## 稳定实体与关系

| 实体 | 保存什么 | 不从它推断什么 |
| --- | --- | --- |
| `papers` / `versions` / `sources` | 论文身份、所选正式版本、文件 URL、路径、SHA-256、可见性 | 下载或收录不表示数学处理完成 |
| `occurrences` | 主文陈述、附录重述、证明子结论的位置与原文标签 | 同一结论的重述不会重复计成独立结果 |
| `propositions` | 规范数学陈述、条件、允许复用的公共命题 | 文句相似不构成命题对齐 |
| `shared_proofs` | 一份公共可读证明及其依赖和实际库声明 | 库引理通过不表示论文陈述已经对齐 |
| `results` / `adapters` | 论文的选定结果、实例化映射、有限变量域、基线约定、适配代码 | 适配通过不代表整篇论文验证完成 |
| `verification_reports` | 一次实际构建报告中选定声明的证据范围 | 同一报告的多个声明选择不是多次独立构建 |
| `issues` / `alignment_notes` | 数学疑点证据与普通记号对齐分别保存；用户确认与修正授权独立 | 技术发现或用户确认都不自动授权修正 |

边的 `type` 明确区分 `appears_in`、`repeats_statement`、`instantiates`、`uses_shared_proof`、`component_of`、`cites_prior_result` 与 `has_build_evidence`。每条边保存审阅状态与证据。新增来源先登记；未经数学对齐的相似关系保持 `candidate`，不得直接连接到一份已完成证明。

公共命题 `prop-set-function-reconstruction` 允许任意实值集合函数，不要求空集值为零。公共证明 `proof-finite-mobius-reconstruction-v2` 被以下三篇实例使用，但通过不同适配保留来源定义：

| 论文 / 选定结果 | 原文与证明 | 适配映射 / 实际 Lean 声明 |
| --- | --- | --- |
| CVPR 2023，`cvpr2023-reconstruction` | 主文 PDF p3 Theorem 1；正式补充 pp2–3 Appendix C | `g(S)=v(mask(S))`，未经中心化；`ReaderV2.cvpr_reconstruction` |
| ICLR 2024 F03，`iclr2024-sparse-reconstruction` | 定义 p3，Theorem 1 p4；p15 Appendix B.1 Eq(7)。本篇明确引用 CVPR 2023，同时重新给出证明 | 对 `g(S)-g(empty)` 实例化，再加一次基线；`ReaderV2.sparse_centered_reconstruction` |
| ICLR 2024 F11，`iclr2024-generalizable-and` | pp12–13 Appendix C(1) 的固定原样本 AND 子结论 | `g(S)=vAnd(mask(S))`，未经中心化；`ReaderV2.generalizable_and_subresult` |

CVPR 2023 的唯一性子结论另用 `proof-finite-mobius-uniqueness-v2` 与 `ReaderV2.cvpr_unique_coefficients`。两条 CVPR 结果是原 Theorem 1 的不同子结论；元数据不把它们虚构成两个原定理编号。

F11 全部 `iclr2024-generalizable-andor` 保留原公式，状态为 `pending_alignment`，没有公共适配声明或完成证明引用。其 AND 子结论是独立的 `theorem_component`，已完成子范围的重写和适配不提升父定理状态。OR 原证明中的疑点与记号对齐问题等待用户确认。独立 OR 实验文件不进入公开 package 的结果、资源和可用接口。

这些适配使用 `Fin n`，量词恰好覆盖一个有限变量集合的所有掩码。`mask` 是显式参数；报告未验证具体 DNN、图像遮挡实现、稀疏性、近似误差或泛化能力。

## 资源、工具和流程

资源注册了四份正式 PDF、核过边界的公式转录、选定结果记录、两份共享证明、公开适配源码、公开构建报告和问题证据。`content_format` 明确区分正式 PDF、文字抽取、经 agent 核对的数学式转录、项目证明与中文说明；数学数据中的 `original_*_md` 说明不能凭字段名被认作作者逐字原文。对 JSON 证明资源使用 `record_collection` / `record_id` 选择单条记录，避免读取不相关或实验内容。资源只能按注册 ID 读取；没有任意文件路径或 shell 参数。

工具真实实现于 `research/reader-v2-20260930/architecture/paper_agent.py`，仅使用现有 Python 标准库。

```bash
source scripts/env.sh
python research/reader-v2-20260930/architecture/paper_agent.py validate
python research/reader-v2-20260930/architecture/paper_agent.py query --paper iclr2024-sparse
python research/reader-v2-20260930/architecture/paper_agent.py get-result cvpr2023-reconstruction
python research/reader-v2-20260930/architecture/paper_agent.py dependencies iclr2024-generalizable-and --depth 2
python research/reader-v2-20260930/architecture/paper_agent.py verification-status iclr2024-generalizable-andor
python research/reader-v2-20260930/architecture/paper_agent.py list-resources
python research/reader-v2-20260930/architecture/paper_agent.py get-resource res-proof-finite-mobius-reconstruction-v2
python research/reader-v2-20260930/architecture/paper_agent.py invoke query '{"paper_id":"iclr2024-sparse"}'
```

所有命令从项目根目录执行。`invoke` 是封闭 JSON 调用入口，按 `tools[].input_schema` 拒绝额外参数；没有安装、构建、写文件、网络请求或 shell 执行工具。`prompts[]` 注册本说明与 `docs/agent-extension-workflow.md`，作为人和 AI 的流程文档，尚未通过 MCP 提供。

agent 阅读结果时先调用 `get-result`，核对原文版本与适配范围，再读取共享证明；需要组合引理时调用 `dependencies`，保留边的关系类型；声称通过 Lean 前调用 `verification-status`。该接口分别返回编译、公理审计、可读重写、代理语义审阅、用户审阅与问题状态。

## 证据新鲜度与可见性

`verification-status` 重新核对报告记录的源码/工具链/依赖哈希，并按项目统一算法计算源指纹；随后检查成功命令、所选声明和显式公理列表。源码变化返回 `stale`；没有公理列表返回不可用；出现 `sorryAx` 或白名单外公理返回失败。不会执行新的 Lean 构建，当前状态只陈述固定报告支持的范围。

选定陈述的代理审校标为 `agent_checked_selected_statement`。可读重写状态使用 `complete/not_started/in_progress`，由 `completion_scope` 明确是选定结果、选定子结果还是完整原定理。用户审核为 `pending`，不会从 Lean 编译成功自动生成 `human-approved`。示例没有整篇完成率，也没有把主文/附录重复出现或待对齐父定理放入一个虚构的整篇分母。

公开查询只返回 public 实体。来源、出现记录、适配和论文派生内容沿来源关系继承可见性；私有端点的边被排除。独立公共库引理仍可保留 public，但指向私稿的使用关系不能公开。安全性与去重测试仅使用内存合成记录，没有读取或导出用户私稿。

## 当前边界

本轮 graph 和 schema 是独立 research demo。既有 `src/archive`、production schemas、corpus 原件与网页生产入口均未迁移。将来若实现 MCP，可以把这组稳定的只读工具封装成服务；服务的运行、权限、协议与独立测试必须另行交付，不能把当前本地 CLI 称为已部署 MCP。
