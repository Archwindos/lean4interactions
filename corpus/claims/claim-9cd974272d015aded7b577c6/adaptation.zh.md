# 附录 C 的 Theorem 1：重构及系数唯一性

沿用正文 Theorem 1 的适配：固定输入、DNN 和掩蔽基线，取 $g(S)=v(\boldsymbol{x}_S)$，变量域为 `Fin n`，$\Omega=2^N$ 包含所有集合及空集。原文将 SCM 准确写成 $Y(\boldsymbol{x}_S)=\sum_{T\subseteq S}w_T$。重构部分引用 `harsanyi-reconstruction` 与共同证明 `proof-reconstruction-v1`；具体定义和空集核对见正文对应条目的 `adaptation.zh.md`。

本次出现还明确增加唯一性句子，并在后续 “Proof for sufficiency” 证明它。用 $d(S)=\widetilde w_S$ 表示任意另一套系数。忠实性前提是

\[
\forall S\subseteq N,\quad R_d(S)=g(S).
\]

这要求在全部掩蔽集合上精确重构，不只是总体 (N) 或一批采样的集合。公共 `Harsanyi.reconstruction_unique g d h` 直接给出 $d=I_g$，即所有原文系数逐项相同。本部分共用 `harsanyi-reconstruction-unique` 与 `proof-reconstruction-unique-v1`，没有另建或复制公共证明。

空集基例是 $\widetilde w_\varnothing=g(\varnothing)=w_\varnothing$，不要求零基线。本规范化没有添加新的数学前提或改变原文结论；`Fin n` 只是把原来的有限总体放入 Lean 的精确域。输入变量之间无需统计独立，因为应用仅使用实值集合函数及有限子集和。

来源是 v6 PDF/印刷页 14 的附录 C Theorem 1、式 (10) 和随后的唯一性句子，证明续于页 15；源码标签 `th:app-harsanyi-faithful`，陈述为 `appendix.tex:116–129`，两个论证边界为 `137–148` 与 `152–186`。原文采用基数归纳及二项式抵消；公共唯一性证明是项目的反演论证。本映射区分命题对齐与证明方法，不宣称原文的每一个推导步骤已经由现有 Lean 代码逐行复现。

独立的有限域应用及实际审计见 `reports/public-pilot/20260930-sparse-concepts-v6/PublicPilot.lean` 与 `lean-applications.log`。另行登记的 Dummy 量词范围歧义不参与本唯一性命题的前提或证明依赖。本次只完成这些核心命题的来源与适配核对，整篇完整性分母仍未确认。
