# 独立 AI 公共库试用记录

2026-09-30，未参与 HarsanyiLib 实现的 `gpt-6.1-sol / max` 子代理完成独立试用。完整证据在 [report.json](../../reports/api-playtest/20260930-max-centered-affine/report.json)；任务在 [task.yaml](../../reports/api-playtest/20260930-max-centered-affine/task.yaml)，最终源码在 [Playtest.lean](../../reports/api-playtest/20260930-max-centered-affine/Playtest.lean)。

先读取 AGENTS、PLAN、implementation-contract、ai-use-library、library-quickstart、library-api、api-playtest 与 math-conventions，再按 `uniqueness / 唯一性`、`centering / 中心化`、`linearity`、`constant` 查询机器目录 [catalog/library.json](../../catalog/library.json)。选择和编写证明之前没有阅读公共 Lean 核心实现，也未阅读或导入 `Consumer.lean`。现有核心文件只按交付要求计算 SHA-256，未展示正文；锁定报告所有文件哈希仍然匹配。

新任务是确定去基线仿射游戏的全部系数，并证明重构系数唯一。对于任意实值有限集合函数 (v) 与 (a,b\in\mathbb R)，证明

\[
 I_{\operatorname{centered}(T\mapsto a v(T)+b)}(S)
 =\begin{cases}0&S=\varnothing,\\a I_v(S)&S\ne\varnothing.\end{cases}
\]

若 (R_d(S)=\operatorname{centered}(T\mapsto av(T)+b)(S)) 对所有有限集合成立，则 (d) 必须等于上述系数函数。这一全域公式保留空集边界；没有假设 (v(\varnothing)=0)，也没有排除 (a=0)。

实际依赖 `interaction_centered`、`interaction_add`、`interaction_smul`、`interaction_const`、`interaction_empty`，随后组合 `reconstruction_unique`。证明项的直接常量审计保存于 [dependencies.log](../../reports/api-playtest/20260930-max-centered-affine/dependencies.log)，确认首条新结论确实使用了五条公共定理；唯一性结论引用该新结论和公共唯一性定理。

复用已有 consumer 的锁定 Lake 依赖环境，只编译独立 scratch 文件。实际最终命令如下，退出状态为 0：

```bash
source scripts/env.sh
cd examples/library-consumer
lake env lean ../../.tmp/api-playtest-max/Playtest.lean
lake env lean ../../.tmp/api-playtest-max/Dependencies.lean
```

最终三条声明（两个新组合结论与一个反例证据）的 `#print axioms` 均只列出 `propext`、`Classical.choice`、`Quot.sound`。日志为 [playtest-attempt-2.log](../../reports/api-playtest/20260930-max-centered-affine/playtest-attempt-2.log)。初次草稿因为 `simp only` 未消去规范化为 `True` 的条件而编译失败；只修正 scratch 的化简步骤，初稿和失败日志仍保留，未把初次含 `sorryAx` 的失败输出列为可信结果。

缺前提试用单独存于 [MissingPremise.lean](../../reports/api-playtest/20260930-max-centered-affine/MissingPremise.lean)。直接调用 `interaction_centered_nonempty v S` 而未提供 `S.Nonempty`，Lean 实际退出 1，指出得到的是 `S.Nonempty → ...`，不是所需等式。对于常数一游戏与 (S=\varnothing)，中心化交互为 0，原交互为 1；该反例也已用 Lean 证明。拒绝日志在 [missingpremise-attempt-1.log](../../reports/api-playtest/20260930-max-centered-affine/missingpremise-attempt-1.log)。这是合成 API 使用测试，未写入真实论文的问题目录。

可从持久证据目录复现，清理 `.tmp` 不会删除答案：

```bash
source scripts/env.sh
cd examples/library-consumer
lake env lean ../../reports/api-playtest/20260930-max-centered-affine/Playtest.lean
lake env lean ../../reports/api-playtest/20260930-max-centered-affine/Dependencies.lean
lake env lean ../../reports/api-playtest/20260930-max-centered-affine/MissingPremise.lean
```

最后一条命令应失败，前两条应成功。库版本为 0.1.0，Lean 4.24.0，mathlib 固定提交 `f897ebcf72cd16f89ab4577d0c826cd14afaafc7`。此次未改核心库、既有 consumer 或指纹文件，也未重复运行三包全量验证。此次目标的检索、签名和最小导入均足够；没有发现必须修复的 API 缺项。整篇论文审校、其它数学对象和未知新目标的可用性不由本试用证明。
