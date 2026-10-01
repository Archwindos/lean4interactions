# 全篇论文数据与本地只读接口

当前实现读取显式活动清单中正式论文的逐页库存、数学内容、符号、问题及真实 Lean 报告。十二篇授权范围见 [发布契约](twelve-paper-release-20261001.md)，新增六篇完成后逐篇接入已验收的六篇基线。它是本地 Python 查询接口与可下载数据包；没有宣称已经部署 MCP 服务或会自动执行外部代理。Paper2Agent 的论文资源、工具与验证思路用于组织这些可审阅产物。

活动输入为 `corpus/public/reader/input-manifest.json` 的显式正式清单；聚合输出为 `reader/data/full-content.json`。各论文活动源在 `corpus/public/reader/<paper_id>/`，历史研究快照及原 Lean 证据保留只读；生成器不修改原件。目录覆盖检查只说明输入与入口完整，不代替数学审查。

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
python reader/architecture/paper_agent.py papers
python reader/architecture/paper_agent.py inventory --paper-id iclr2024-sparse
python reader/architecture/paper_agent.py search 'Theorem 6' --paper-id iclr2024-sparse
python reader/architecture/paper_agent.py symbols --paper-id iclr2024-generalizable
python reader/architecture/paper_agent.py shared
python reader/architecture/paper_agent.py issues
python reader/architecture/paper_agent.py verification-status cvpr2023-dummy
python reader/architecture/paper_agent.py library Harsanyi.Sparsity
python reader/architecture/paper_agent.py validate
```

接口只读，不运行 shell、不写论文、不联网、不调用模型。验证读取实际报告并检查源哈希、声明、成功命令及公理；未知或过期证据不会继承元数据的“已通过”。公共库查询读取基础 `catalog/library.json` 及显式论文实际报告中的独立扩展声明，核对当前源哈希，不猜测类型；新扩展用 direct import，与基础版本单独标记。增加论文流程见 `docs/agent-extension-workflow.md`。

新增正式论文无需修改聚合器白名单：在 `corpus/public/reader/input-manifest.json` 的 `papers` 增加一条显式配置，并提供对应文件。`metadata_path` 使用现有论文的 `paper-metadata.json` 格式，所有论文和来源都必须是 `public/published`，来源须有实际路径、SHA-256、版本及页数；未配置文件不会自动扫描。配置示例：

```json
{
  "paper_id": "new-formal-paper",
  "metadata_path": "corpus/public/reader/new-formal-paper/paper-metadata.json",
  "inventory_path": "corpus/public/reader/new-formal-paper/inventory.json",
  "content_path": "corpus/public/reader/new-formal-paper/content.json",
  "symbols_path": "corpus/public/reader/new-formal-paper/symbols.json",
  "issues_path": "corpus/public/reader/new-formal-paper/issues.json"
}
```

当前配置以显式 manifest 为准；构建器不硬编码篇数，也不把开发中的新篇自动扫描为完成。论文标题查询可用 `paper_agent.py paper-search 'Generalizable'`；`search` 返回命题/推导结果及原编号别名。

全篇资源包生成：`python reader/architecture/build_package.py`。它导出当前资源 SHA-256、13 个本地查询动作与实际引用图；结构定义位于同目录 `package.schema.json` / `full-content.schema.json`。这些是可执行 Python CLI 的说明与数据，尚不是已注册的远程 MCP 服务。

`architecture/check_api.py` 使用无额外依赖的受限 JSON Schema 验证器，仅处理本包实际声明的关键字；遇到未支持关键字会明确失败，不静默忽略。它同时检查真实查询、引用闭合、证据角色及负例，报告范围是软件接口检查。

公开阅读器只读显式 public/published 清单，不扫描私稿或旧 corpus 根目录。底层档案库默认只 `corpus/public/`，显式 private 入口只搜索私稿池，可单向解析公共 theorem/proof 依赖，不将公共论文混入私稿列表。中英人读字段通过 `translations.en` 或英文sidecar覆盖；步骤ID、公式、Lean机器映射与状态严格保护，双语显示不提升形式化范围。
# 新正式论文入站契约（十二篇阶段）

作者原文字段 `original_statement_md/original_proof_md` 不容纳明确标为 `Project source note/synopsis (not author text/not an author quotation)` 的项目说明。新篇入站门精确拒绝这类已知污染；项目解释移到 `source_transcription_notes` 或实际项目概述，无独立作者证明保留空字段并注明 `no_local_author_proof`。护栏不根据语言或长度猜测来源，也不等于自动审核作者全文忠实度。原六篇按已验收基线兼容，第二轮再逐条审查来源边界。

活动来源仍以 `corpus/public/reader/input-manifest.json` 为准。稳定枚举与必需字段单存于 [`reader/architecture/admission-contract.json`](../reader/architecture/admission-contract.json)，`load_manifest` / 聚合 / 独立预检共用该契约。冻结基线中的旧六篇维持已验收字段；新篇不能靠缺省值避开目标分母或变成“未发现问题”。

每个新库存 entry 必须有 JSON 布尔 `proof_target`。外引定理、错误命题和未编号实质推导仍为 `true`。`false` 只允许机器契约中列出的定义、假设、方法、算法、实验或纯外部背景分类，并须有来源支持的 `non_proof_reason`。分类合理性由数学审查确定；若“定义”夹带证明，须拆条或改为目标。混合经验标签必须由作者按实际内容规范分类，不能按未知 `kind` 自动排除。若保留根 `proof_targets`，其目标 result ID 集合必须与逐条布尔及 `merge_target_id` 完全一致。只接受 `merge_target_id`（及旧兼容 `merge_id`）；`merged_target_id` 等未知拼写拒绝，显式目标必须对应真实 content result。

每个 entry 必须唯一解析到一个实际 result；两个 results 不能同时用 `inventory_ids` 引用同一 entry。entry ID 与 result ID 不同时必须声明 `merge_target_id` 或 `merge_id`，单独在 result 的 `inventory_ids` 列出旧 ID 不构成合并授权。根 `proof_targets` 只列真实解析后的 result ID，不能列被合并 entry ID。

新 result 使用以下互相独立的字段：

| 字段 | 接受值及含义 |
| --- | --- |
| `rewrite_role` | `proof` 完整记录范围的证明；`counterexample` 反例正文；`statement_scope_explanation` 原命题范围说明；`partial_proof_with_refuted_clause` 部分证明并有被反驳子句；`partial_component` 部分论证；`source_material` 非证明来源材料 |
| `statement_assessment` | `no_statement_error_recorded` 未登记命题错误；`refuted` 整命题反驳；`partially_refuted` 子句反驳；`counterexample_recorded` 已登记待范围核对的反例；`scope_under_review` 范围待核对 |
| `lean.evidence_role` | `theorem_proof` 实际声明覆盖记录命题范围；`partial_component` 仅部分结论/辅助范围；`counterexample` 实际机器反例；`none` 没有映射 |
| `rewrite_status` | 见机器契约；`complete` 说明重写正文交付，不等于全部原命题或 Lean 已证明。`in_progress` / `not_started` 不算交付 |

不接受 `valid`、`false_original_clause`、`complete_proof`、`proved_exact_finite_statement` 等自造角色。需要新语义时先与整合及根代理明确扩展，不能默默翻译成现有角色。文字中的反例不构成 Lean 反例：多项式子结果已形式化、ReLU 反例未形式化时，Lean 应标部分，另在文字/问题记录说明反例范围。

`lean` 是对象，须有明确 `evidence_role` 和 `declarations` 数组。声明为真实名字或带 `name` 的对象；有声明即须有对应实际 `report_path`。`step_map` 用 `step_id`、`declaration`、真实适配的 `explanation_md` 关联，构建从当前报告补真实类型、行号、公理及源码，不靠模板解释冒充逐步覆盖。共享证明自身须交付 `id/title/statement_tex/assumptions/definitions/proof_scope/proof_steps/rewrite_status/lean/translations.en`；条件、定义和步骤为数组，公式保持 TeX。其 Lean 角色、声明、报告必须对应该共享命题自身，不能仅贴一份相关论文报告。无映射时用 `none` 与空声明并明确范围，不隐瞒状态。

新篇经审查的 `lean.evidence_role` 与原命题的 `statement_assessment` 是独立维度：完整形式化一个错误子句的反例，可为 `counterexample`，同时父命题为 `partially_refuted`；只有有限域组件、而反例仍是人读推导时，保持 `partial_component`。聚合不得用 `partial_scope_verified` 或父命题判断覆盖显式角色，也不得靠声明名字包含 `counterexample` 推断新篇组件分类。开发预检把完整角色与旧部分状态措辞并存的条目列入 `machine_role_status_reviews`，由数学作者核对实际类型与范围后裁定；提示本身不升级或降级证据。旧六篇在第一阶段继续保全已验收范围。

论文元数据 `sources[]` 使用 `id`，库存及引用使用 `source_id`；正式来源同时有项目内 `local_path`、实际 `sha256/total_pages`、正式状态/可见性与官方 `url`。原文转录、双语覆盖、数学审查、Lean 当前性分别验收。人读英文字段必须真实补译，保护字段与作者原式不能改变。

新输入的所有字符串递归检查控制字符：普通 prose 容许换行、tab 与合法 CRLF 换行，拒绝孤立 CR、其余 C0 字符和 DEL；`*_tex` 字段及其数组值只容许换行，tab/所有 CR 也拒绝。Python 普通字面量中的 `\beta` 会生成 backspace，`\frac` 会生成 formfeed，`\tau`、`\rho` 也可能损坏：TeX 字面量须用 raw string 或正确转义。检查涵盖正文、英文覆盖、符号原／规范映射、库存、元数据及问题记录，不依赖 KaTeX 能否报错。它仅防字符串转义污染，不代替来源和数学审查；第一阶段旧六篇字段仍按原契约保全。

新论文 issue 须有 `id/title/kind/issue_type/source_refs`。`kind` 保留作者实际分类，`issue_type` 必须显式选机器契约中的六种展示类型，不按未知 kind 默认“命题错误”。`statement_counterexample` 要对应 `original_statement_status=counterexample_verified`；只反驳复合句子句时选 `statement_partial_counterexample` 和 `compound_clause_counterexample_verified`，不能升级为整命题反例。证明步骤、定义/算法边界与待判定范围分别选其稳定类型。

每个 issue 的非空 `source_refs` 记录 `source_id/version_id/pdf_pages`；source identity/version 必须匹配本篇正式元数据，页码为实际文件范围内的正整数数组。只有人读 `source_location` 不提供可跳转来源。至少一个 `related_result_ids` 或 `affected_result_ids` 必须指向实际结果，结果的 `related_issue_ids` 须保留对应关系。content 内和独立 issues 文件均检查。跨篇或范围分类的数学正确性仍由作者与根审查确认。
