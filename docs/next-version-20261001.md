# 2026-10-01 独立论文池与六篇双语阅读器执行计划

本计划执行用户已授权的结构更新、六篇正式论文和全文符号/双语整合。数学正确性、来源清单、文字重写、Lean证据、网页可用性分别验收；本文件不是完成报告。

## 活动数据布局

`corpus/public/` 与 `corpus/private/` 是物理独立的活动数据池，各自具有 `papers/`、`claims/`、`theorems/`、`issues/`、`reviews/`、`relations.yaml`。默认 `ArchiveStore` 与网页只打开 public；CLI 必须以 `--collection private` 或 `--private` 显式打开私稿，不能全局读取后过滤。私稿允许单向引用公共 Lean 库；public 不扫描 private。

公开阅读输入只接受 `corpus/public/reader/input-manifest.json` 的显式六篇清单：`cvpr2023-sparse-concepts`、`iclr2024-sparse`、`iclr2024-generalizable`、`icml2023-harsanyinet`、`icml2024-layerwise`、`icml2025-coalition`。每篇输入位于 `corpus/public/reader/<paper_id>/`，包括 metadata、逐页 inventory、content、symbols、issues。新活动构建器置于 `reader/`，输出 `reader/preview/`；原 research 验收目录是不可覆盖的历史快照。

原三篇活动内容复制后重映射输入/来源路径；原 Lean 源码和报告的哈希路径继续作为只读证据，避免无必要的编译或改写。历史公开研究快照保留。旧 `corpus/papers`、`claims`、`theorems`、`issues`、`reviews` 和混合 relations 迁移后只作为 ignored legacy 保留，不再被活动 store 读取或写入。

## 迁移及安全边界

迁移按 manifest visibility 和来源/依赖路由；private 的原件、匿名claims、问题、评审、关联、私有派生物全部进入 private。保留每个原文件与目标文件的 SHA-256、路由依据和回滚映射；原件不删除。未标可公开的未知记录保守进入 private；公理审计和来源状态不因此改变。新增手动导入默认 private/unpublished。公共导入只在明确 published/public 元数据下进入 public。

`.gitignore` 将忽略整个 private、legacy、私稿 inbox 与混合历史报告。publication 检查更新为发现活动 private、检测暂存区及 tracked private derivatives、核对显式正式 PDF 白名单和迁移证据；仅 ignore 不足以保证已跟踪材料排除。

## 双语契约

中文字段保持原结构；每个 result/shared_proof 的 `translations.en` 只覆写人读字段：标题、overview、assumptions、definitions、scope、proof_steps的title/body_md/justification、notation注释、适配和共享证明正文。步骤ID、原公式、原符号、Lean声明及映射必须一致。旧篇可使用 `corpus/public/translations/<paper_id>.en.json`，形状为 `{schema_version,paper_id,results:{id:{...}}}`；共享 sidecar为 `{schema_version,shared_proofs:{id:{...}}}`。zh/en切换持久化，不能只翻UI。原作者转录与原公式保真，英文译文明确其项目译文身份。

三名内容责任：网络代理负责新HarsanyiNet和Layerwise及旧CVPR/有限共享英文；coalition代理负责新Coalition及旧Sparse/其共享英文；结构代理负责旧Generalizable30条及独有共享英文，并核对15个历史共享的完整覆盖。

## 实施和验收顺序

1. 迁移可重跑、导入路由、默认store物理隔离；记录所有迁移文件哈希与原件保留状态。
2. 复用已验收的聚合、Lean真实性检查、静态阅读器，移到维护入口；严格六篇清单并检查所有inventory目标进入结果索引。
3. 双语内容覆盖检查、步骤/公式/Lean映射不变检查；统一符号表保留原文作用域与基线区分，禁止字符串替换原陈述。
4. 当前公开构建实际浏览器检查全部论文/结果/共享/符号/问题页面、语言切换持久化、搜索及移动端，保存报告与截图。网页通过不代表数学通过。
5. README、AI扩展流程和结构文档指向新活动入口；根代理独立审阅来源完整性、数学与Lean证据，汇报仍未证明/部分/命题错误。

本代理不提交或push、不读取token。上传脚本由根代理另行安排。本轮三个新正式PDF应按各数学代理元数据与PMLR原件哈希逐一白名单。
