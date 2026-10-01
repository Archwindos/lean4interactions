# 三篇正式论文的全篇证明整合与符号规范

用户已经明确授权并要求完整处理已有三篇，覆盖正文、附录及正式补充材料。此前四个选定结果是历史示例，不是本轮完成标准。本轮由三个 `gpt-6.1-sol / max` 代理实施：两名数学代理、一名专职网页/数据整合代理；根代理协调依赖、核对缺项与验收。用户已要求本任务完成后，后续新代理使用 `gpt-6.1-sol / xhigh`，本轮不切换正在工作的模型。

最新授权：用户明确要求“直接修正”原证明错误，标出错误位置，但“不能修正命题”，命题错误要单独列出。当前三篇的证明修正权限是 `proof_only_granted`；原假设与结论保持不变，命题修改未授权。不再对这三篇的每个证明错误重复请求权限；用户授权不等于其已逐个核验数学判断。

## 来源边界与责任

| 论文 ID | 正式文件 | 核查范围 | 内容实施责任 |
| --- | --- | --- | --- |
| `cvpr2023-sparse-concepts` | CVPR 2023 正文 10 页、正式补充材料 27 页 | 全部 37 页，来源文件独立计页 | `full_cvpr_proofs_max` |
| `iclr2024-sparse` | ICLR 2024 Sparse 正式 PDF 34 页 | 全部 34 页 | `full_sparse_proofs_max` |
| `iclr2024-generalizable` | ICLR 2024 Generalizable 正式 PDF 23 页 | 全部 23 页 | 初核/转录由整合代理完成；组合数学归 CVPR 代理，方差/重参数/近似主张归 Sparse 代理 |

94 页是来源审查范围，不是证明数量。正文重述、附录证明、多个子结论与外引分别登记；去重必须依据数学内容和依赖，不能简单按同名编号合并。外引但本篇没有证明的陈述依然可查，清楚标注本篇无原证明。

每名数学代理独占各自 `research/full-proof-integration-20260930/<paper>/`；第三篇的新数学结果分别写入它们目录中的 `generalizable-finite-results.json` 与 `generalizable-analysis-results.json`，由整合代理汇合。整合代理独占网页、共同输入、查询接口与规范符号表，不与数学代理并发编辑同一文件。新增可复用 Lean 模块在 `HarsanyiLib/Harsanyi/Extensions/` 中按文件分工，既有 Core 接口保持。新成果核对后合入现有阅读入口；旧 PDF、旧证明与历史构建报告保留。

## 全文清单与机器输入

每篇首先提供 `inventory.json` 与 `inventory.md`。清单至少包含：

- `paper_id`、正式 `sources`（路径、source_id、SHA256、页数）和 `review_scope`。
- `page_audit`：每个正式文件的每一 PDF 页均有检查结论、章节、数学条目 ID；无数学证明的页也明确分类，不能省略后声称完整。
- `entries`：稳定 ID、原编号/别名、标题、条目类型、原陈述位置、证明起止页及章节、全部出现位置、归并目标、外引情况与判定依据。
- 归并后的证明目标与原文出现分别计数。定义、假设、经验观察、算法描述、说明例子保留分类，不能任意增减待证目标分母。
- `review_status: agent_reviewed` 不等于用户审阅通过；完整性清单与数学正确性是独立状态。

每篇提供 `content.json`，复用现有 v2 结果的主要字段，允许新增字段：

```json
{
  "paper_id": "stable-paper-id",
  "results": [],
  "shared_proofs": [],
  "issues": [],
  "symbols": [],
  "inventory_path": "project-relative-path"
}
```

结果至少保存 `id, paper_id, title, kind, original_label, inventory_ids, source_refs, statement_tex, assumptions, definitions, original_statement_md, original_proof_md, original_statement_source_type, original_proof_source_type, overview, proof_steps, shared_proof_ids, symbol_ids, notation_map, rewrite_status, alignment_status, user_review_status, lean, related_issue_ids`。公式使用标准 TeX；完整原文转录、项目译文、项目重写明确分类。原作者证明的摘要不能标为原证明全文。原 PDF 对应页提供逐式核对依据。

`proof_steps` 沿用 `id, title, body_md, formula_tex, justification, lean_refs`，每个引理调用要说明前提。已有稳定 ID（例如四个旧论文结果）保留，附录别名与新的原文出现关联到它们，避免生成重复入口。

状态分别记录：

- 原文清单是否完整、原陈述/证明是否转录完整；
- 中文重写 `complete/in_progress/not_started/blocked_by_false_statement`；原命题待判定时另标语义核查状态；
- 代理语义对齐与用户审核；
- Lean 无报告、构建失败、部分范围、当前通过；
- 原数学问题 `user_confirmation` 与 `fix_authorization`。

原证明有问题的条目仍在原位置完整可读，并指向具体原式、证据和影响。在原命题及其全部条件不变的情况下另写修正证明；允许换证明路线或补全缺失步骤，修正内容和原文不能混淆。若原命题本身错误，则单独显示原陈述与反例，不补条件使其变真。不能通过删除问题条目提高完成率。

## 公共证明与独立形式化

重构、唯一性沿用既有公共证明 ID。CVPR 内容代理先负责跨论文共同的交互性质、边际差分、Shapley、Shapley interaction 与 Shapley–Taylor；Sparse 代理据明确前提复用，重点完成本篇高阶交互、均值、线性代数与界。Generalizable 代理处理独有的方差和重参数推导并复用公共结果。

Lean 的形式陈述必须匹配原论文量词、有限总体、基线及其他条件。禁止把待证结论作为假设、只验证结论的弱版本、只验有限小例子或把一般库引理当作完整论文应用通过。实际报告绑定来源、声明、代码、工具链和公理。共享库新增内容需独立审校后统一发布，调用者不用复制实现。

如果实际不能完成某项形式化，记录具体未完成的数学步骤和现有部分证明；任务继续推进，最终不宣称全部形式化。原命题错误、语义尚待核对与普通 Lean 工程待办分开。

## 规范符号表

符号按数学概念与作用域管理，不能仅做字符串替换。全局规范记录至少包括：

`id, canonical_tex, name_zh, definition_tex, description_md, type_or_domain, scope, assumptions, empty_set_convention, baseline_convention, aliases, paper_mappings, lean_names, version`。

每个 `paper_mapping` 保存论文/版本、原符号 TeX、原定义、PDF 页与公式编号、对应规范概念以及关系类型：`same_definition`、`renaming`、`centered_variant`、`derived_quantity`、`conflict` 或 `pending_alignment`。同字母不同意义分开记录，同一意义不同字母经定义核对后关联。

基本约定：模型为 `v:X→ℝ`；固定输入 `x`、输入基线向量 `r`，保留变量集合 `S⊆N` 得到 `x_S`；集合函数 `g(S)=v(x_S)`；输出基线标量 `b=v(x_∅)`；中心化 `g₀(S)=g(S)−b`。原始交互、中心化交互、AND/OR、交互阶数、平均输出、显著性阈值与噪声方差分开定义。原文中的 `b` 若指输入基线，不得误当规范输出基线标量。约定不授权修改原陈述。

网页提供公共符号表、按论文筛选的对照，以及证明中的相关符号入口。给 AI 的接口按概念 ID 查询定义、原文映射、前提和 Lean 名称；符号冲突必须显式返回。

## 收尾验收

1. 三份逐页清单覆盖四份正式文件的全部 94 页；另一名代理交叉核对章节、编号、未编号推导和证明边界，根代理核对缺项。
2. 所有目标都出现在论文目录，有正式原文入口、实际内容或具体待办/疑点；不得遗留只能展示精选结果的白名单。
3. 每个“重写完成”确有完整正文或完整共享正文加忠实适配；每个“Lean 通过”确有当前、准确范围的实际报告。
4. 原文重复不重复计目标；共享证明不重复存储，跨论文条件逐项核对；问题不从分母消失。
5. 规范符号表覆盖全部已登记数学条目所需的核心符号，原符号保真、作用域和空集/基线条件可查，映射冲突不静默替换。
6. 原始材料哈希不变；全部新增目录项、来源页、共享依赖、符号入口和状态在实际浏览器检查。
7. 最终报告分别给出来源审查、原文整理、重写、共享和 Lean 的数量与缺口。完成度由内容证据决定，软件测试数量仅说明软件检查范围。

本文件是执行和验收契约，不是已完成报告。实际进度、条目清单和检查报告随实施保存，完成前不填造数字。
