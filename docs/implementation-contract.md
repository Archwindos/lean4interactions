# 首次实现的协作契约

日期：2026-09-30。状态：实施中。由根代理协调；细节需要变更时同步所有消费者。

本文保留首版 corpus 的技术契约。当前三篇全篇整合的责任、格式、授权与验收以[全篇执行契约](full-paper-integration-20260930.md)为准；当前两名数学代理、一名集成代理，本次完成后新代理使用 `gpt-6.1-sol / xhigh`。

## 分工

- backend_environment：Conda/Python、src/archive（除 web.py）、CLI、源数据读写与索引、导入提取、schemas、templates、后端测试。
- lean_library：Lean 安装、lean、examples/library-consumer、catalog、corpus/theorems、Lean 构建与审计脚本，以及 library-quickstart/library-api/formalization/ai-use-library/math-conventions 文档。
- web_docs：src/archive/web.py、web、test_web.py、README、PLAN 和其余说明文档。
- 根代理：AGENTS、本契约、STATUS、跨模块检查及任务重新分配。

以上为首轮所有权。用户随后要求子代理改为 `gpt-6.1-sol / max`：`web_docs_max` 接手网页、文档和覆盖率/独立报告接口，`manuscript_review_max` 接手私稿，`public_pilot_api_max` 负责公开试点与独立 API 试用；数学反例由 `issue_crosscheck_max` 独立局部复核。交付后的新增编辑先由根代理协调，避免覆盖。

## 手动导入

输入目录 `inbox/<folder>/` 包含 PDF、TeX 或 Markdown 材料，可带 `metadata.yaml`。缺少题名时使用文件夹或文件名作为临时题名，状态为待补充。不要求 DOI、URL 或已发表信息。

元数据统一使用 `paper_id`、`version`、`title`、`authors`、`publication_status`、`source_type`、`visibility`。`source_type` 为 `manual` 或 `public_url`；手动输入默认 `publication_status: unpublished` 和 `visibility: private`。

归档到 `corpus/papers/<paper_id>/<version>/`，原始文件复制到 sources，manifest 记录相对路径、SHA-256 和来源。具体 files 字段结构由后端 schemas 定义并通知网页代理。按内容和身份重复导入必须幂等，文件更新产生新版本，禁止越界路径和符号链接读取。

项目根目录已有用户材料时，保留原文件，可作为 private 手动材料导入；不得将该材料上传到网页检索、外部解析或模型服务。

## 数据文件

- 文件是真源，SQLite 是可重建索引。
- YAML 是可编辑元数据格式；JSON 用于 API 目录与构建证据。
- `corpus/theorems/<theorem_id>/metadata.yaml` 至少包含 schema_version、theorem_id、title、summary、assumptions、visibility、proofs、lean_declarations、tags。
- `statement.tex` 保存统一数学陈述。`proofs/<proof_id>/proof.zh.md` 保存中文证明，旁置 metadata.yaml，包含 proof_id、theorem_id、lean_declarations、dependencies、visibility。
- `corpus/claims/<claim_id>/metadata.yaml` 关联 paper_id、paper_version、source_location、original_label、theorem_ids、proof_ids、review_status、visibility。
- `corpus/relations.yaml` 采用顶层 schema_version 和 relations 列表，关系含 from_id、to_id、relation_type、review_status、evidence、visibility。
- 用共同 JSON/YAML 键记录原文对应与实际审校；自动提取一律为候选。未提取完不展示成已完整。
- 私有性沿衍生内容传播。已存在公共定理可保留公共，但指向私稿的来源、关联、私有新证明及其元数据在公开导出中排除。

人工清单保留所有出现记录。`kind` 或 `disposition` 为 `false_positive`、`duplicate_occurrence`、`superseded` 的记录不计入独立待证目标；重复/替代记录通过 `canonical_claim_id` 指向主条目。定义、假设和经验观察也不计待证目标；数学问题、外引但证明未提供的结果不能因此从分母移除。`denominator_reviewed` 只说明所声明材料范围内的清单经过审阅，不说明证明已重写、对齐或通过 Lean。

主 claim 的 `original.tex` 可包含完整原命题、附录重述和原证明，明确标记来源边界；自动候选快照另存，原 PDF/TeX 始终保持不变。公共 proof 的 `steps` 元数据用稳定步骤 ID 关联 `lean_declarations`；网页仅接受严格的 `step-正整数` 内部锚点，并提供步骤与 API/源码双向链接。

## 数学问题登记与用户确认

用户最新要求：当前三篇的原证明错误直接修正并标出原错误，禁止修改命题；命题错误单列。首版问题记录位于 `corpus/issues/<issue_id>.yaml`，新一轮位于 full-proof-integration 的各篇 issues.json；至少包含 issue_id、关联 paper/claim/theorem IDs、source_location、original_statement、problem、evidence、affected_ids、visibility、assessment、user_confirmation、fix_authorization、status。

新问题继承当前范围已有授权，不机械重置为 pending。当前三篇使用 `fix_authorization: proof_only_granted`、`statement_change_authorization: not_granted`；assessment 区分证明错误、已找到原命题反例、语义缺口等技术判断。技术判断不等于用户逐条确认。先排除提取/OCR错误，不捏造问题记录。

当前三篇的证明修正另存并关联原式及授权，不再重复申请。原命题与全部假设保持不变，原命题有反例时单列，不能通过加条件或弱化结论关闭问题。其他材料按其已有授权处理。网页提供具体问题与来源定位，隐私沿派生关系继承；普通工程错误可正常修复。

## Lean 目录与验证报告

采用 `lean/HarsanyiLib` 与 `lean/PaperProofs` 两个包。Lean 代理选定 Lean 4.24.0 / mathlib v4.24.0，具体相容版本以最终锁定文件为准。

`catalog/library.json` 的共同外层：

```json
{
  "schema_version": 1,
  "library": "HarsanyiLib",
  "library_version": "0.1.0",
  "lean_version": "4.24.0",
  "mathlib_revision": "实际锁定提交",
  "source_fingerprint": "实际源码与锁定依赖指纹",
  "verification_report": "reports/lean/<build_id>/report.json",
  "declarations": []
}
```

每个 declaration 至少包含 `name`（完全限定名）、`module`、`signature`（从实际 Lean 环境取得）、`kind`、`title`、`summary`、`theorem_id`（无对应则 null）、`proof_id`（无对应则 null）、`source_path`（项目内相对路径）、`line`、`assumptions`、`dependencies`、`axioms`、`visibility`、`verification_status`。无法从工具取得的字段保持空或明确未知，不能填造。

验证报告外层至少包含 schema_version、build_id、status（passed/failed/unavailable）、generated_at、source_fingerprint、toolchain、mathlib_revision、commands、declarations。每条声明记录 name、status、axioms；命令记录 cwd、命令参数、exit_code、log_path。报告由真实执行生成。

报告还保存 `source_files: [{path, sha256}, ...]`。path 是项目内相对路径，覆盖实际 Lean 源码、工具链配置及依赖锁。source_fingerprint 为按 path 排序后的这份列表经 `json.dumps(records, sort_keys=True, ensure_ascii=False, separators=(',', ':'))` 序列化再取 UTF-8 SHA-256。后端与验证器采用同一算法；公理字段缺失表示未知，不能默认当作空公理列表。

后端和网页校验源码/工具链/依赖指纹；无法证实与当前文件相符时显示未验证或过期，而不是直接信任 metadata 中的 verified 字样。直接引用 public theorem 不代表论文 claim 已对齐。

论文适配可使用独立报告：claim metadata 的 `verification_report` 必须指向其自身 `corpus/claims/<claim_id>/lean/` 下的 JSON，`lean_declarations` 列出实际受该报告验证的声明。独立报告同样保存成功命令、声明及显式公理列表、源码和依赖 SHA-256、按完整路径字符串排序计算的指纹；不能拿公共库报告替代适配验证。网页标记 `verification_scope: independent_claim`，核验独立指纹，不将其与公共 catalog 指纹强行比较。报告、源码与日志仅在本地按白名单提供；公开视图拒绝原始独立证据，私稿派生内容继续 private。原命题对齐状态仍需单独审阅。

## 运行接口

Python 包名 `archive`，CLI 入口 `archive`，项目脚本 `scripts/archive`。优先提供 `python -m archive` 入口。命令至少覆盖 ingest（本地和公开来源）、inbox、extract、validate、build、search、search-lemmas、show-lemma、impact、verify、serve；具体参数由后端落实并同步文档。

网页工厂建议 `archive.web.create_app(root=...)`；默认绑定 127.0.0.1。前端只消费 ArchiveStore 或后端导出的读取函数，接口由后端和网页代理直接协调。测试临时目录也放在本项目 .tmp 下。

公开导出明确选择 public 模式；不得包含 private 稿件、私有衍生内容或指向私稿的关系。默认本地网页可以阅读用户的 private 材料。

静态导出为每个可见论文版本建立页面并保留版本链接，不能把带旧版本参数的来源链接静默改指最新版本。独立 AI 试用及科研问题的补充证据保存到各自 reports 目录，不冒充全局 Lean 报告已经覆盖新增源码。

## 首次集成验收

1. 项目内 Conda 和 Lean 可运行，记录真实版本及路径。
2. 本地投入 PDF/TeX 可入库，重复导入不重复，越界路径拒绝，未发表材料默认私有。
3. 提取、搜索、论文页、公共定理页和真实 Lean 报告可串联。
4. 库的一般性基础定理有无占位的构建与传递公理审计；consumer 组合已有引理得到新结果。
5. 证明、来源、共享关系与已完成状态不混淆。至少建立已核对的跨来源共享案例，未核对的保持候选。
6. 文档提供真实运行命令、手动导入方法、AI 使用库流程和未完成清单。
