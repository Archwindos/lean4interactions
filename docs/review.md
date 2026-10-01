# 分维度审校与问题确认

当前十二篇正式论文适用用户的最新授权：**直接修正证明、标出原错误，不得修改命题及其假设；错误命题单列。** `fix_authorization: proof_only_granted`、`statement_change_authorization: not_granted`；技术判断仍不等于用户逐条确认。当前范围见[十二篇执行契约](twelve-paper-release-20261001.md)。以下未授权示例适用于尚无修正许可的其他材料，不能用它重复阻塞已授权工作。

完整性、可读性、原文命题对齐和 Lean 验证独立记录。登记论文、提取候选或完成基础引理不能成为整篇完成的依据。

| 维度 | 审查内容 | 完成依据 |
| --- | --- | --- |
| 完整性 | 正文、附录、附件、无编号论证、外部引用 | 逐节复核 inventory 与分母 |
| 重写 | 完整假设、关键步骤、边界、来源 | 中文正文逐项审校 |
| 对齐 | 定义域、量词、全部前提与结论 | 原文/规范/Lean 三方对应 |
| 共享 | 相同命题、证明方法或中间引理 | 保存数学依据及转换证明 |
| Lean | 声明存在、构建、公理依赖、当前指纹 | 真实 reports 与准确 catalog |

报告必须含实际命令、退出码、日志、工具链、依赖和源码指纹。没有成功命令/公理审计、报告过期或出现 sorryAx，都不能展示为当前验证通过。论文 claim 还需要独立对齐；公共定理已验证不能替代这一检查。

论文应用可使用独立报告，保持公共库与私有稿件分离。在 claim metadata 中设置 `verification_report: corpus/claims/<claim_id>/lean/report.json`，`lean_declarations` 仅列该条目实际的应用声明。报告沿用 implementation-contract 的 commands、source_files、source_fingerprint、declarations/status/axioms 结构；source_files 按 path 字符串排序，用约定序列化计算指纹，并覆盖适配源码及所用依赖/工具链证据。report 路径必须是该 claim 的 lean 目录内的相对 JSON 路径，不能指定别的 claim 或公共报告来代替。

后端读取当前源码并复核指纹、成功命令、各应用声明和公理白名单。报告不存在、缺少证据或源码改变时，条目显示未验证/过期；独立报告失效不使公共库报告失效。网页明确标示独立论文应用验证，提供本地报告及报告登记的同目录源码/日志。公开导出不提供原始报告、源码或日志。

清单中已确认的误报、重复出现与被替代记录保留总记录数，并分别记录 false_positive、duplicate_occurrence、superseded。重复/替代需指向 canonical_claim_id；它们不计为独立证明目标。定义/假设/经验观察也不计证明目标。未完成、有问题或等待确认的真实命题仍在分母中。denominator_reviewed 表示清单完整性核对完成，与 alignment_status 和 Lean 验证独立。

## 发现原文疑似错误

保留原文，在 corpus/issues/<issue_id>.yaml 登记；至少包括 issue_id、paper_id/version 或 claim_ids、source_location、original_statement、problem、evidence（反例/推导）、affected_ids 或 impact、visibility、user_confirmation、fix_authorization。问题状态和修正授权不是同一字段。

~~~yaml
schema_version: 1
issue_id: stable-issue-id
paper_id: my-draft
paper_version: v1
claim_ids: [my-draft-claim-id]
source_location:
  section: "实际章节"
  pdf_page: 0  # 填实际页序，不能保留此占位
original_statement: "逐字或忠实保留原陈述"
problem: "说明疑似缺失条件或推导错误"
evidence: "实际反例或逐步推导；不填未经执行的实验"
affected_ids: [my-draft-claim-id]
visibility: private
user_confirmation: pending
fix_authorization: pending
~~~

该示例是未授权材料的模板，保存真实 issue 时必须替换位置、证据及实际已有授权。先排除转录错误，分清原证明步骤错误、原命题有反例、语义条件不明确三类情况。有证明修正权限时，另写同一原命题的正确证明并保留原式；不能补假设或改变结论。命题错误时保存反例及其满足原条件的检查，单列待讨论。没有修正授权的其他材料保持待确认，未受影响工作继续。任何问题都不能仅为提高完成率而移出分母。

公开问题记录也可能泄露私稿结论、编号或作者：继承来源隐私，不因问题记录单独有 public 字样就绕过私有来源。网页只读显示用户确认和修正授权，不提供自动变更按钮。
