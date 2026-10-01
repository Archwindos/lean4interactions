# Theorem 2：原文 AND-OR 全式（对齐待确认）

本页范围：Original full Theorem 2; intentionally not a completed proof。

## 正式来源

- ICLR 2024 Generalizable 正式正文及随文附录，PDF 页 3,12,13,14：Eq.(2) OR 约定；Theorem 2 Eq.(3); Appendix C Eq.(7) 及 Proof(1) 固定 x AND 子结论; Appendix C(1) Eq.(8) AND 推导与 OR proof 起点; Appendix C(2) OR 分类计算与 Eq.(9)。来源文件：`research/paper-survey-20260930/recent/pdf/iclr2024-generalizable.pdf`。

## 命题

\[v(x_T)=v_{\mathrm{and}}(x_T)+v_{\mathrm{or}}(x_T)=\sum_{S\subseteq T}I_{\mathrm{and}}(S\mid x_T)+\sum_{S\in\{S:S\cap T\ne\varnothing\}\cup\{\varnothing\}}I_{\mathrm{or}}(S\mid x_T)\]

## 必要定义与适用条件

原文固定模型输出的 AND/OR 分量分解；此处只保留原式，不增补修正条件。

\[v(x_T)=v_{\mathrm{and}}(x_T)+v_{\mathrm{or}}(x_T)\]

原文明确单列空集 OR 值。本页把它作为原文定义约定记录，不因为 Eq.(2) 的惯用非空适用范围而另造数学错误。

\[I_{\mathrm{or}}(\varnothing\mid x)=v_{\mathrm{or}}(x_\varnothing)\]

## 证明思路

保留正式原文全式供核对。第 14 页 OR 推导有具体中间求和问题；正文与附录的 \(x_T\)/固定 x 记号还需语义对齐。本轮没有重写或发布完整 Theorem 2 的修正版。已完成的第 12–13 页 AND 子结论另列，不能覆盖这一状态。

## 小例子与空集

此待确认条目不提供重写证明或替代例子。

## Lean 检查范围

No Lean declaration for the original full Theorem 2

声明：没有原式对应的 Lean 声明。

报告：`None`。

## 文字到 Lean 对照

此原式尚无对应形式声明。

## 边界说明

- OR 中间求和问题已登记 issue-f11-or-intermediate-20260930；用户确认与修正授权均 pending。

- \(x_T\) 与固定 x 的差异登记为记号语义对齐说明，不据此判断全定理不成立。

- 公共库与 AND adapter 的编译通过不能关闭此项原文问题。

## 原证明路线与本重写的关系

原文 Appendix C 分成 AND、OR、AND-OR 三部分。第 13–14 页 OR 部分交换有限双重和，再按 \(L=N\)\T、\(L=N\)、L∩\(T\ne \varnothing\) 且 \(L\ne N\)、L∩\(T=\varnothing\) 且 \(L\ne N\)\T 四类计算系数，第 14 页 Eq.(9) 得到 OR 总和。相关疑点见下方报告；此处不提供替代证明或补入新假设。

