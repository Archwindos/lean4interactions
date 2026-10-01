# 全篇论文数据与本地只读接口

当前实现读取三篇正式论文的逐页清单、数学内容、符号、问题及真实 Lean 报告。它是本地 Python 查询接口与可下载数据包；没有宣称已经部署 MCP 服务或会自动执行外部代理。Paper2Agent 的论文资源、工具与验证思路用于组织这些可审阅产物。

权威聚合输入为 `research/full-proof-integration-20260930/data/full-content.json`。各论文原输入、正式 PDF 和历史 v2 证据保留；生成器不修改原件。目录覆盖检查只说明输入与入口完整，不代替数学审查。

| 对象 | 主要内容 |
| --- | --- |
| `papers / sources` | 正式论文、版本、独立文件、SHA-256、PDF 页数与可见性 |
| `inventories / coverage` | 全部逐页检查、原编号与别名、证明范围、出现记录和归并目标 |
| `results` | 原数学转录、项目正文、定义映射、共享引用、符号、问题与各自范围 |
| `shared_proofs` | 单存的公共证明及稳定步骤；论文结果引用这些步骤 |
| `symbols` | 规范概念、作用函数、定义域、空集与基线、逐论文原符号映射 |
| `issues` | 原错式、精确来源、证据、影响；错误证明与错误命题分别分类 |
| `lean / reports` | 实际声明、证据角色、类型、代码、成功命令、公理及源新鲜度 |

`rewrite_status` 记录正文交付状态；`rewrite_role / proof_scope` 区分证明、反例、完整范围说明及部分子结论。`statement_assessment` 记录原命题判断。`alignment_status` 是代理对齐，`user_review_status` 单独保存。`lean.evidence_role` 为定理证明、反例、部分子结论或无证据；反例编译不等于原命题证明。

来源采用文件内从 1 起算的 PDF 页码。主文与附录编号别名进入搜索；例如 Sparse 附录 B.4 的误印 Theorem 6 保留为正文 Theorem 3 的别名，另一个真正 Theorem 6 仍是独立结果。每条搜索结果只返回一次，并附全部来源出现。

符号按数学定义及作用域管理。原始、中心化和分量交互不因同字母合并。Lean 类型表达式保存在表示说明中；`lean_names` 只包含真实可查的常量，计划名称另字段保存。

可调用接口：

```bash
source scripts/env.sh
python research/full-proof-integration-20260930/architecture/paper_agent.py papers
python research/full-proof-integration-20260930/architecture/paper_agent.py inventory --paper-id iclr2024-sparse
python research/full-proof-integration-20260930/architecture/paper_agent.py search 'Theorem 6' --paper-id iclr2024-sparse
python research/full-proof-integration-20260930/architecture/paper_agent.py symbols --paper-id iclr2024-generalizable
python research/full-proof-integration-20260930/architecture/paper_agent.py shared
python research/full-proof-integration-20260930/architecture/paper_agent.py issues
python research/full-proof-integration-20260930/architecture/paper_agent.py verification-status cvpr2023-dummy
python research/full-proof-integration-20260930/architecture/paper_agent.py library Harsanyi.Sparsity
python research/full-proof-integration-20260930/architecture/paper_agent.py validate
```

接口只读，不运行 shell、不写论文、不联网、不调用模型。验证读取实际报告并检查源哈希、声明、成功命令及公理；未知或过期证据不会继承元数据的“已通过”。公共库查询读取当前 `catalog/library.json`，不猜测类型。增加论文流程见 `docs/agent-extension-workflow.md`。

新增正式论文无需修改聚合器白名单：在 `research/full-proof-integration-20260930/input-manifest.json` 的 `papers` 增加一条显式配置，并提供对应文件。`metadata_path` 使用现有论文的 `paper-metadata.json` 格式，所有论文和来源都必须是 `public/published`，来源须有实际路径、SHA-256、版本及页数；未配置文件不会自动扫描。配置示例：

```json
{
  "paper_id": "new-formal-paper",
  "metadata_path": "research/full-proof-integration-20260930/new-paper/paper-metadata.json",
  "inventory_path": "research/full-proof-integration-20260930/new-paper/inventory.json",
  "content_path": "research/full-proof-integration-20260930/new-paper/content.json",
  "symbols_path": "research/full-proof-integration-20260930/new-paper/symbols.json",
  "issues_path": "research/full-proof-integration-20260930/new-paper/issues.json"
}
```

当前配置仅包含三篇已授权正式论文。论文标题查询可用 `paper_agent.py paper-search 'Generalizable'`；`search` 返回命题/推导结果及原编号别名。

全篇资源包生成：`python research/full-proof-integration-20260930/architecture/build_package.py`。它导出当前资源 SHA-256、13 个本地查询动作与实际引用图；结构定义位于同目录 `package.schema.json` / `full-content.schema.json`。这些是可执行 Python CLI 的说明与数据，尚不是已注册的远程 MCP 服务。

`architecture/check_api.py` 使用无额外依赖的受限 JSON Schema 验证器，仅处理本包实际声明的关键字；遇到未支持关键字会明确失败，不静默忽略。它同时检查真实查询、引用闭合、证据角色及负例，报告范围是软件接口检查。
