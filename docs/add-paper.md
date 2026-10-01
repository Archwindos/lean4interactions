# 加入正式论文或本地稿件

正式论文进入当前阅读器的顺序是“正式来源 → 逐页目标清单 → 作者原文 → 规范双语证明 → Lean 适配与真实证据 → 独立审阅 → 显式收录”。完整字段与命令见[扩展流程](agent-extension-workflow.md)，枚举及目标映射见[数据模型](paper-agent-data-model.md)。先在 `corpus/public/reader/<paper_id>/` 建立开发包，不因文件存在就加入 `input-manifest.json`。正式 PDF 和补充材料须有真实链接、版本、页数和 SHA-256；不得使用预印本替换正式版。

清单须涵盖正文、附录、补充材料的全部数学结果与未编号实质推导。新条目逐项显式给出 `proof_target`，非目标保留来源支持的分类理由；外引命题、原错命题及尚无证明的真实目标不移出分母。一个库存条目唯一解析到一个 result，跨 ID 合并须显式登记。原文转录保存作者完整 prose、公式及错式，项目解释与修正证明单列。先核对量词、定义域、空集和基线，再写规范中英证明和局部符号映射；不以整页抽取、摘要或模板步骤替代作者原证与完整重写。

Lean 层先检索实际公共 API 的全部前提，直接导入公共模块，明确本论文定义到库对象的转换，再编译本论文适配并导出实际类型、传递公理和 import 闭包哈希。论文适配不能冒充通用模块；文字已完整、原命题有反例、机器仅部分编码和无 Lean 映射分别记录。开发包可用 `reader/check_draft_admission.py` 预检字段与双语，预检不代替来源忠实度或数学交叉审阅。全部独立验收通过后才修改显式 manifest，严格运行来源、聚合、完成度、双语、符号、公式、API 及真实浏览器检查。输入变化后重新绑定报告，保留旧 ID、原件和证据。

当前十二篇授权允许修正同一原命题的证明并标明原错处，禁止改原假设或结论；命题不成立时单列反例。开发篇继续保留 `in_progress` 或实际范围，不能把软件通过标为数学完成。公开提交还须核对实际工作树和暂存区的出版检查，操作要求见[贡献说明](../CONTRIBUTING.md)。

以下本地归档流程适用于私稿与待核查材料，不自动接入公开阅读器。

本流程适用于未发表稿、公开论文的本地副本以及后续版本。无需 DOI 或 URL。使用前读取 README 的运行方式；所有源文件须在项目内，禁止沿符号链接读取其他项目。

1. 将 PDF、TeX、Markdown 和附件放入 inbox/<folder>/，保留原文件。可添加 metadata.yaml，字段见 README；手动输入默认 unpublished/private。题名和作者未知时保持待补，不猜测作者。
2. 执行 scripts/archive inbox。查看返回的 paper_id、version 和归档相对路径，核对 manifest.files 的 SHA-256、文件角色和附件列表。确认材料版本完整，会议/arXiv 版本分别归档。
3. 对默认私稿执行 `scripts/archive --private extract <paper_id> --version <version>`。提取结果是候选；PDF 公式须回看原页，页序与印刷页码分别登记。执行 `scripts/archive --private validate` 和 `scripts/archive --private build`。
4. 在论文页查看 inventory。按正文、附录、补充材料逐节核查 Theorem/Lemma/Proposition/Corollary、无编号推导、性质证明与外部引用。将遗漏登记到 inventory；不得只依据 Proof 字样认定完整。完整性分母核对前保持 denominator_reviewed: false。
5. claim 保存稳定 ID、原编号、来源位置、原陈述与原证明。区分定义、假设、经验观察、数学命题、缺失证明与外部依赖；项目补写须明确来源类别。人工确认自动误报使用 disposition: false_positive；正文/附录重复出现使用 duplicate_occurrence，旧记录被新记录替代使用 superseded。重复/替代记录用 canonical_claim_id 指向主条目，保留原位置与分类依据。这些记录继续计入总记录数，证明目标只计主条目；有问题、证明缺失或未完成的真实目标不能按误报排除。
6. 读取 docs/math-conventions.md，逐项记录原文符号、统一定义和 Lean 定义之间的关系；先检索公共库与 relations。可疑相似结果保持候选，实际核对后才关联。涉及基线/定义转换或特例要有连接证据。
7. 按 docs/proof-style.md 重写并关联 Lean 声明；发现原文错误先建立 issue，并继承已有授权，规则见 docs/review.md。当前十二篇的授权见[发布契约](twelve-paper-release-20261001.md)：可修证明，不许改命题；其他材料依其既有授权处理。原文保持，修正证明另存；命题错误则列出反例，不改假设或结论。
8. 分别更新重写、对齐、审校状态，实际运行 verify，保存报告。公共定理验证通过不代表 claim 已对齐；不把未完成条目移出分母。
9. 运行 validate、build、coverage，在网页核对双向来源链接与状态。公开前执行 export --public 并检查私有继承；本地稿默认继续 private。

~~~bash
scripts/archive inbox
scripts/archive --private extract my-draft --version v1
scripts/archive --private validate
scripts/archive --private build
scripts/archive --private search --query my-draft
scripts/archive --private coverage
scripts/archive --private serve
~~~

中断恢复时先读 manifest、inventory、claims 和现有 reports，补完下一项，重复导入相同内容不建立重复版本。内容变化使用新版本；跨版本旧来源和审校记录保留。

题名/作者人工核对后可以用 update-metadata 命令修改描述字段，它保存本地历史记录。修改 visibility 为 public 是实质公开意图，需用户明确授权；不要把自动提取成功视为公开许可。
