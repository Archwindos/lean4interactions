# 独立来源对齐复核（agent）

复核者：负责本轮来源/数据结构的 agent；不是用户审核，也不自动表示未来科学使用已获批准。复核对象为正式 PDF 的选定数学陈述、数学代理的新中文证明和实际公开适配 `math/lean/ReaderAdapters.lean`。本记录只确认下表范围的语义对应；原 PDF 与论文证明未被修改。

| 结果 ID | 正式位置 | 独立核对结果 |
| --- | --- | --- |
| `cvpr2023-reconstruction` | 正式主文 p3 Theorem 1；正式补充 pp2–3 Appendix C | 同一固定样本/基线的全部子集，空集系数是原输出基线。公共函数 `g(S)=v(mask(S))` 的未中心化交互与原系数逐项一致。公开适配使用 `Fin n`，全称量词没有扩大到有限总体外。因果图指示函数到子集和的数学解释完整，但具体因果图运行未由 Lean 建模。 |
| `cvpr2023-uniqueness` | 同一原 Theorem 1 的唯一性 clause；正式补充 pp2–3 | 必须同一组系数在全部子集上精确匹配。公共证明先证明逆反演，再代入匹配假设；适配 `faithful` 恰好覆盖所有 `Finset (Fin n)`。没有把唯一性扩到任意 AND/OR 分解或近似匹配。 |
| `iclr2024-sparse-reconstruction` | p3 Eq(1)、p4 Theorem 1、p15 Appendix B.1 Eq(7) | 原 `u(T)=v(x_T)-v(x_empty)` 与 `centered (maskedGame v mask)` 对齐；交互空集为零，原输出基线只在和外加入一次。`sparse_empty` 明确记录边界。此精确恒等式不需要稀疏性假设；没有形式化 Theorems 2–3。 |
| `iclr2024-generalizable-and` | pp12–13 Appendix C(1) 的固定原样本 AND 子陈述 | 选定原式为 `Iand(S|x)`，对固定 `vAnd` 和固定掩码形成未中心化集合函数，空集系数等于 `vAnd(mask(empty))`。`generalizable_and_subresult` 只验证这个子结论，未加入原文没有的零基线或特殊优化假设。 |

公共重构证明的五步完整展开了子集分类、插入交互差分、对任意函数加强归纳、对差分函数再用归纳和最终消去。唯一性证明完整展开逆反演的局部函数一致性和全部掩码前提。两份证明的可读公式与现有 `Harsanyi.reconstruction` / `interaction_reconstruct` / `reconstruction_unique` 的实际代码一致；不会把一行 `exact` 当成已经解释全部数学推导。

F03 p4 的外引与本篇 p15 重证分别记录，参考文献 p11 的 Ren et al. (2023a) 明确对应这篇 CVPR 2023。跨文复用来自一般集合函数定理的三个实例，保留不同基线定义与实际适配，关系是实例化而非只凭相似文字判同一原命题。

F11 全部 Theorem 2 的原 `x_T` 记号、OR 空集特殊约定与原 Appendix C(2) 中间求和均保留。`issue-f11-or-intermediate-20260930` 是待用户确认的原证明步骤疑点；`issue-f11-mask-notation-20260930` 是独立的记号对齐说明，`is_mathematical_error:false`。没有在这里补条件、修原文或发布独立 OR 实验作为替代证明。父定理继续 `pending_alignment/not_started`，公开包无其适配证据。

实际编译与公理依赖由数学代理的固定公开报告提供；本地工具重新核对该报告源指纹和所选声明。此复核与编译证据各自保存，Lean 没有自动验证中文翻译、PDF 语义或具体 DNN/mask 实现。
