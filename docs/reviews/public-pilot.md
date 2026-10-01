# 首篇公开论文的小范围实际试点

2026-09-30 已归档并核对 [Defining and Quantifying the Emergence of Sparse Concepts in DNNs，arXiv v6](https://arxiv.org/abs/2111.06206v6)。作者为 Jie Ren、Mingjie Li、Qirui Chen、Huiqi Deng、Quanshi Zhang；该固定版本日期为 2023-04-03。完整执行证据在 [report.json](../../reports/public-pilot/20260930-sparse-concepts-v6/report.json)。本次完成来源归档与 Theorem 1 的重构/唯一性共享映射，**没有完成整篇论文审校**。

固定版 [PDF](https://arxiv.org/pdf/2111.06206v6) 为 38 页，SHA-256 为 `2f18ed3bc48c095ffbf4ab68a1f6a6545d5e86e562229f3795a46e98f3095a12`；[TeX source](https://arxiv.org/src/2111.06206v6) 包含 37 个文件，原压缩包 SHA-256 为 `d7158da234ffbfaaa2f7e32f89e6977e3f910ac4ae40aac209c90e695f6a85e0`。PDF、源码压缩包、展开源码、下载 HTTP 头、来源 URL 和获取时间均保存在项目内，使用 public / published / public_url 元数据导入。这里的 published 记录公开 arXiv 来源，没有另行核定会议或期刊版本。

论文标识为 `sparse-concepts-2111-06206`、版本 `v6`。来源清单见 [manifest.yaml](../../corpus/papers/sparse-concepts-2111-06206/v6/manifest.yaml)，逐文件哈希复核无差异；版本、页码和附录结构核对见 [source-review.yaml](../../corpus/papers/sparse-concepts-2111-06206/v6/source-review.yaml)。PDF 第 1 页的版本页脚与版本网页一致。附录 A–I 都包含在 PDF 和 `appendix.tex` 中：A/B 起于第 13 页、C 于 14、D 于 15、E 于 24、F/G 于 25、H 于 29、I 于 30；后续图页延伸到 PDF 第 38 页。这些标题位置只是材料范围记录，不代表各节的全部证明已经审核。

实际执行 `scripts/archive ingest inbox/public-sparse-concepts-v6` 与 `scripts/archive extract sparse-concepts-2111-06206 --version v6`，均退出 0。命令与输出保存在 [commands.json](../../reports/public-pilot/20260930-sparse-concepts-v6/commands.json)、ingest.log 和 extract.log。普通网络沙箱的 PDF 下载退出 7；经已授权的 `require_escalated` 自动审批重试后成功，PDF 与 TeX 全部写入项目目录。

人工核对了以下数学结果及其来源：

| 原文出现 | 精确来源 | 共同结果 / 共同证明 |
| --- | --- | --- |
| 正文 Theorem 1，忠实性 | PDF/印刷页 3，§3.1；`AOG.tex:205–215`，`th:harsanyi-faithful` | `harsanyi-reconstruction` / `proof-reconstruction-v1` |
| 同一正文条目的原生 TeX 出现 | 自动提取的独立 TeX 来源条目；保留与 PDF 出现的关系 | 同上，不计作新增数学结果 |
| 附录 C Theorem 1，重构与唯一性句子 | PDF/印刷页 14–15；`appendix.tex:116–186`，`th:app-harsanyi-faithful` | 同上；另 `harsanyi-reconstruction-unique` / `proof-reconstruction-unique-v1` |

固定 DNN、输入和掩蔽基线，定义 $g(S)=v(\boldsymbol{x}_S)$，以 `Game (Fin n)` 精确表示原来的有限域。原文要求 $\Omega=2^N$，并在附录 C 明确把 SCM 写成全部子集系数之和。因此忠实性对应 `Harsanyi.reconstruction`；任何另一套系数若在所有掩蔽集合上精确重构，唯一性对应 `Harsanyi.reconstruction_unique`。空集也参加求和，原文基例是 $w_\varnothing=g(\varnothing)$。没有添加零基线假设、没有中心化原函数，也没有把精确前提改为有限采样或稀疏近似。

各 claim 的 metadata、alignment.yaml、review.yaml 和 adaptation.zh.md 已写入。原文片段与完整证明边界保存于 [source-evidence](../../reports/public-pilot/20260930-sparse-concepts-v6/source-evidence/theorem1-appendixC-statement-proof.tex)，对应 PDF 页的本地渲染图也保留。共同中文证明和核心 Lean 实现只引用既有权威位置，未复制或修改。原文采用双重求和/二项式抵消及基数归纳，公共证明属于项目新增论证；映射没有声称原证明方法完全相同。八条公开关系的核对草稿保存在 [relations-public-draft.yaml](../../corpus/relations-public-draft.yaml)，已由 root 合并到权威 [relations.yaml](../../corpus/relations.yaml)；私有关系由公开视图过滤。

独立有限域应用与问题证据在 [PublicPilot.lean](../../reports/public-pilot/20260930-sparse-concepts-v6/PublicPilot.lean)。实际编译命令为：

```bash
source scripts/env.sh
cd examples/library-consumer
lake env lean ../../reports/public-pilot/20260930-sparse-concepts-v6/PublicPilot.lean
```

该命令退出 0；三个声明的传递公理仅含白名单三项，见 [lean-applications.log](../../reports/public-pilot/20260930-sparse-concepts-v6/lean-applications.log)。archive claim 的 `lean_declarations` 引用精确对齐的公共 `Harsanyi.reconstruction` / `Harsanyi.reconstruction_unique`，其库验证来自现有且哈希仍匹配的 `20260930T052254-2` 报告；人工来源对齐另有证据。独立 `PublicPilot` 声明只作本报告的应用和反例证据，不作为 claim 新声明接入 archive，旧库报告不覆盖它们。本次没有修改冻结文件，也没有再次运行三包全量验证。

顺带观察到 `(3) Dummy axiom` 的范围歧义，已登记 [issue-sparse-concepts-v6-dummy-scope](../../corpus/issues/issue-sparse-concepts-v6-dummy-scope.yaml)：原文说 “with other variables”，而显示的 $\forall S\subseteq N\setminus\{i\}$ 没有排除空集。对于 $N=\{i\}$、$g(\varnothing)=0$、$g(\{i\})=1$，显示前提的唯一情况 $S=\varnothing$ 成立，显示结论却要求 $I_g(\{i\})=0$，其实际值为 1。原文措辞也可能暗指高阶交互，因此技术判断保持 `suspected / scope_ambiguity`，不替作者决定隐含范围。PDF 页 13/16、TeX 全段上下文、末行抵消的空集值及 Lean 检验全部保存。`user_confirmation` 与 `fix_authorization` 均为 pending，没有补前提、改结论或发布修正版；重构/唯一性不受该项影响。

自动提取有 17 个候选，本次另登记 1 个问题关联出现。自动候选含正文引用及重复来源，并漏检 `manualtheorem` 与七条性质中的条目，不能视为完整数学清单。当前 [inventory.yaml](../../corpus/papers/sparse-concepts-2111-06206/v6/inventory.yaml) 有 18 个条目，`completeness_status: partially_reviewed`、`denominator_reviewed: false`。其他性质、Shapley 关系、Shapley interaction、Shapley-Taylor、无编号论证及稀疏近似仍未完成人工审校；本次没有进行其他论文抓取或扩展这些数学对象。
