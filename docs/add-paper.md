# 从本地稿件加入档案

本流程适用于未发表稿、公开论文的本地副本以及后续版本。无需 DOI 或 URL。使用前读取 README 的运行方式；所有源文件须在项目内，禁止沿符号链接读取其他项目。

1. 将 PDF、TeX、Markdown 和附件放入 inbox/<folder>/，保留原文件。可添加 metadata.yaml，字段见 README；手动输入默认 unpublished/private。题名和作者未知时保持待补，不猜测作者。
2. 执行 scripts/archive inbox。查看返回的 paper_id、version 和归档相对路径，核对 manifest.files 的 SHA-256、文件角色和附件列表。确认材料版本完整，会议/arXiv 版本分别归档。
3. 执行 scripts/archive extract <paper_id> --version <version>。提取结果是候选；PDF 公式须回看原页，页序与印刷页码分别登记。执行 scripts/archive validate 和 scripts/archive build。
4. 在论文页查看 inventory。按正文、附录、补充材料逐节核查 Theorem/Lemma/Proposition/Corollary、无编号推导、性质证明与外部引用。将遗漏登记到 inventory；不得只依据 Proof 字样认定完整。完整性分母核对前保持 denominator_reviewed: false。
5. claim 保存稳定 ID、原编号、来源位置、原陈述与原证明。区分定义、假设、经验观察、数学命题、缺失证明与外部依赖；项目补写须明确来源类别。人工确认自动误报使用 disposition: false_positive；正文/附录重复出现使用 duplicate_occurrence，旧记录被新记录替代使用 superseded。重复/替代记录用 canonical_claim_id 指向主条目，保留原位置与分类依据。这些记录继续计入总记录数，证明目标只计主条目；有问题、证明缺失或未完成的真实目标不能按误报排除。
6. 读取 docs/math-conventions.md，逐项记录原文符号、统一定义和 Lean 定义之间的关系；先检索公共库与 relations。可疑相似结果保持候选，实际核对后才关联。涉及基线/定义转换或特例要有连接证据。
7. 按 docs/proof-style.md 重写并关联 Lean 声明；发现原文错误先建立 issue，并继承已有授权，规则见 docs/review.md。当前三篇已允许修证明但不许改命题；其他材料不自动取得同样许可。原文保持，修正证明另存；命题错误则列出反例，不改假设或结论。
8. 分别更新重写、对齐、审校状态，实际运行 verify，保存报告。公共定理验证通过不代表 claim 已对齐；不把未完成条目移出分母。
9. 运行 validate、build、coverage，在网页核对双向来源链接与状态。公开前执行 export --public 并检查私有继承；本地稿默认继续 private。

~~~bash
scripts/archive inbox
scripts/archive extract my-draft --version v1
scripts/archive validate
scripts/archive build
scripts/archive search --query my-draft
scripts/archive coverage
scripts/archive serve
~~~

中断恢复时先读 manifest、inventory、claims 和现有 reports，补完下一项，重复导入相同内容不建立重复版本。内容变化使用新版本；跨版本旧来源和审校记录保留。

题名/作者人工核对后可以用 update-metadata 命令修改描述字段，它保存本地历史记录。修改 visibility 为 public 是实质公开意图，需用户明确授权；不要把自动提取成功视为公开许可。
