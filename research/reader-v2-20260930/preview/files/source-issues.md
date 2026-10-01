# F11 正式原证明的局部问题与记号对齐说明

本报告仅登记具体原文事实、局部反例与影响范围。用户确认 `pending`，修正授权 `pending`。未改写原文、未补入假设、未发布完整 Theorem 2 的替代证明。普通抽取或记号待核对不会计作数学错误。

## 一项原证明中间步骤问题

问题 ID：`issue-f11-or-intermediate-20260930`。正式文件：`research/paper-survey-20260930/recent/pdf/iclr2024-generalizable.pdf`，PDF 第 14 页，Appendix C 的 OR proof case(3)/(4)。已直接看过 [整页图像](source-review/iclr2024-generalizable-page-14.png)，确认 case(3) 的 underbrace 只覆盖内层和，排除文本抽取的定位错误。

原文 case(3) 的条件是 \(L\cap T\ne\varnothing\)、\(L\ne N\)。其式中把下面内层和标为零：

\[
\underbrace{\sum_{m=0}^{|T|-|T\cap L|}\binom{|T|-|T\cap L|}{m}(-1)^{|S'|+m}}_{=0}.
\]

取 \(N=\{1,2\}\)、\(T=L=\{1\}\)，满足原文条件。此时 \(|T|-|T\cap L|=0\)，内层只有 \(m=0\)。当 \(S'=\varnothing\) 时内层和为 1；当 \(S'=\{2\}\) 时为 −1。因而对这两个允许的固定 \(S'\)，原文内层 `=0` 都不成立。

外层遍历 \(S'\subseteq\{2\}\)，两项 1 与 −1 总和仍为 0。这说明此反例只否定内层的逐项断言，不否定最终 OR 重构定理。影响范围是第 14 页分类计算中间等号及其说明。

同页 case(4) 另有被计数集合的范围问题：它同时要求 \(L\cap T=\varnothing\) 和 \(S\cap T\ne\varnothing\)，并定义 \(S''=S\cap T\)，但内层按 \(0\le|S''|\le|T|\) 求和。\(S''=\varnothing\) 不满足这次计数条件。取 \(N=\{1,2\}\)、\(T=\{1\}\)、\(L=\varnothing\)、\(S'=\varnothing\)：实际有效的内层仅 \(m=1\)，和为 −1；原显示范围含 \(m=0,1\)，和为 0。外层其他项仍可能抵消，因此也不把这个范围问题当作最终定理的反例。

附录 C(1) PDF 第 12–13 页的固定原样本 AND 子结论不依赖这些 OR 分类计算。本轮 AND 适配的 Lean 成功不会确认、修改或关闭本问题。需用户先确认这条原证明问题，修正方案另行授权；本报告不提供修正方案。

## 一项记号语义对齐说明

说明 ID：`issue-f11-mask-notation-20260930`，分类是 `notation_alignment_note`，不是数学错误。

正文 PDF 第 3 页 Eq.(3) 与第 12 页 Eq.(7) 的全文陈述使用 \(I_{\mathrm{and}}(S\mid x_T)\) 和 \(I_{\mathrm{or}}(S\mid x_T)\)。但第 12 页 Proof(1) 的明确子结论和下一段定义使用固定原样本 \(x\)：

\[
\forall T\subseteq N,\quad v_{\mathrm{and}}(x_T)=\sum_{S\subseteq T}I_{\mathrm{and}}(S\mid x).
\]

本轮已完成结果按这条原式对齐，正文 full Theorem 2 的 \(x_T\) 原式保留。完整公式的系数如何依赖再次掩码仍需核对，尚无据此判定原定理不成立的证据。原文给出的 OR 空集值 \(I_{\mathrm{or}}(\varnothing\mid x)=v_{\mathrm{or}}(x_\varnothing)\) 单列为定义约定，不额外登记数学错误。

原件未改动；完整 AND-OR 陈述的对齐、重写与形式化均未完成，用户审核状态 `pending`。相关图片：[第 3 页](source-review/iclr2024-generalizable-page-3.png)、[第 12 页](source-review/iclr2024-generalizable-page-12.png)。

