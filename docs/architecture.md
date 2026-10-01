# 数据与展示架构

首版使用 Python 3.12、FastAPI、Jinja 服务端页面和 SQLite FTS5。文件是权威内容；build 下索引可删除后重建。网页只消费 ArchiveStore，不在搜索请求中生成证明、不调用外部 AI，也不请求 CDN。

## 模块边界

src/archive/ingest.py 处理项目内手动材料和明确请求的公开 URL；extract.py 从本地材料登记候选；store.py 统一读取、版本/指纹状态和公开过滤；search.py 构建可重建索引；validate.py 检查路径、校验值和关联；web.py 提供只读页面；export.py 导出同一筛选视图。

Lean 公共库位于 lean/HarsanyiLib，论文应用位于 lean/PaperProofs，下游示例位于 examples/library-consumer。公共库不依赖 archive、网页或论文包。catalog/library.json 是实际 Lean 环境提取的接口与报告关联，报告位于 reports/lean/<build_id>/。

## 实体与稳定链接

| 实体 | 权威文件 | 入口 |
| --- | --- | --- |
| 论文版本 | corpus/papers/<id>/<version>/manifest.yaml、inventory.yaml | /papers/<id>?version=<version> |
| 原文出现位置 | corpus/claims/<id>/metadata.yaml、original.tex、alignment.yaml | /claims/<id> |
| 规范结果 | corpus/theorems/<id>/metadata.yaml、statement.tex | /theorems/<id> |
| 证明方法 | 同结果目录 proofs/<proof_id>/metadata.yaml、proof.zh.md | /proofs/<proof_id> |
| 数学问题 | corpus/issues/<issue_id>.yaml | /issues/<issue_id> |
| Lean API | catalog/library.json | /library/<qualified-name> |

claim 关联多个 theorem_ids / proof_ids；同一结果允许多种证明；relations 保存核对依据和关系类型。来源的缺失假设不能被正确公共定理遮盖。共享证明页反向列出 claims，原文页可以返回统一证明。

proof.steps 的 ID 对应正文独立的严格 `<a id="step-N"></a>` 标记，网页将它转换为安全内部锚点。步骤到 API 签名、源码以及 API 返回步骤的链接从当前筛选后的 catalog 生成；不接收任意原始 HTML。数学 dependencies 链接 archive 实体，lean_dependencies 链接实际目录中的声明。

静态导出为论文最新入口和每个可见版本分别生成页面。`/papers/<id>?version=<version>` 按版本匹配文件，来源不会静默跳到最新版本；公开快照只生成公开版本。导出保留步骤片段链接，并将离线 API 搜索结果指向相应声明页。

## 首版展示决策（2026-09-30）

采用轻量 FastAPI/Jinja 页面，先完成档案、中文证明、准确 API 与真实证据的关联。KaTeX 固定 0.16.22，包下载缓存位于 .cache/downloads，dist、字体及 LICENSE 位于 web/static/vendor/katex。归档包 SHA-256 为 e9e0d167db3175481cbadaff38e8d90b130f6a3ddb451a47e43c577fd511f365；来源是 npm registry 的 katex-0.16.22.tgz。页面使用本地 JS/CSS，trust: false；未知命令或错误提取保留可读源码，排版成功也保留原始 LaTeX。

Verso/doc-gen4 仍是后续候选，尚未进行实际兼容性和成本比较。首版选择服务端模板是为了先形成可运行、隐私可审查的档案；不以尚未执行的工具评估宣称已得出性能结论。后续替换展示层不能改变权威 ID、独立库或证据模型。

## 状态与隐私

提取、重写、对齐、审校和 Lean 验证是独立状态。验证以当前指纹、真实成功命令、声明存在及传递公理白名单计算，不能直接相信 metadata 的 verified。依赖和源码变化后旧报告显示过期。

完整性分母与形式化对齐分开。coverage 的 total_candidates 包含清单全部记录；定义、假设、经验观察以及 false_positive、duplicate_occurrence、superseded 不计 proof_targets。重复/替代的出现位置仍可回查；其他待处理或有问题的数学条目保留为目标。仅 denominator_reviewed 为 true 时计算覆盖率；它本身不认证 alignment 或 Lean。

claim 可通过 verification_report 指定自己 `corpus/claims/<claim_id>/lean/` 中的相对 JSON 报告。其验证复用同一命令、源码指纹与公理检查，独立于公共 catalog 指纹。公共定理的验证仍来自公共报告。本地证据路由只允许该 claim 指定的报告，以及报告登记的同目录 Lean 源码/日志；其他 corpus 元数据不作为原始下载暴露。公开视图拒绝这些原始证据。

手动未发表材料默认 private。本地视图可读；public_view 排除私有论文、claims、新的私稿衍生 theorem/proof、关系与搜索摘要。独立公共结果可保留，但私稿来源边不能随它公开。公开模式的全文源码/日志路由默认拒绝，公开静态导出移除其链接；未来如需公开，必须先生成经过筛选的专用产物。

所有数学问题先记录用户确认和独立修正授权，页面只读，不提供自动确认按钮。
