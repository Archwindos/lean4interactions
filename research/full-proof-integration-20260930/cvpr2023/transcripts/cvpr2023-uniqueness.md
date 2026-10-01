# Appendix C：全部掩码重构系数唯一：来源数学转录

正式来源：正文 PDF 第3页 Theorem 1/Eq.(3)；补充 PDF 第2页 C/Eq.(2)。固定输入 $x$，取 $\Omega=2^N$，每个因果效应为 $w_A=\sum_{U\subseteq A}(-1)^{|A|-|U|}v(x_U)$。作者主张 $\forall S\subseteq N,\ Y(x_S)=v(x_S)$；补充材料另主张 Harsanyi dividend 是满足该忠实性要求的唯一度量。

以下转录补充第3页完整证明数学内容（作者把两部分称为 necessity 与 sufficiency）。由正文SCM，$Y(x_S)=\sum_{A\in\Omega}w_A C_A(x_S)=\sum_{A\subseteq S}w_A$，故忠实性等价于 $v(x_S)=\sum_{A\subseteq S}w_A$。

**Necessity 原计算：** 对每个 $S\subseteq N$，
\[
\begin{aligned}
\sum_{A\subseteq S}w_A
&=\sum_{A\subseteq S}\sum_{L\subseteq A}(-1)^{|A|-|L|}v(x_L)\\
&=\sum_{L\subseteq S}\sum_{A\subseteq S:A\supseteq L}(-1)^{|A|-|L|}v(x_L)\\
&=\sum_{L\subseteq S}\sum_{a=|L|}^{|S|}\sum_{\substack{L\subseteq A\subseteq S\\|A|=a}}(-1)^{a-|L|}v(x_L)\\
&=\sum_{L\subseteq S}v(x_L)\sum_{m=0}^{|S|-|L|}\binom{|S|-|L|}{m}(-1)^m
=v(x_S).
\end{aligned}
\]
**Sufficiency 原证明：** 假设另一组系数 $\widetilde w_A$ 对全部掩码满足 $v(x_S)=\sum_{A\subseteq S}\widetilde w_A$。按 $|S|$ 归纳。作者列出三个基例：
\[
\widetilde w_\varnothing=v(x_\varnothing)=w_\varnothing;\quad
\widetilde w_{\{i\}}=v(x_{\{i\}})-v(x_\varnothing)=w_{\{i\}};\quad
\widetilde w_{\{i,j\}}=v(x_{\{i,j\}})-v(x_{\{i\}})-v(x_{\{j\}})+v(x_\varnothing)=w_{\{i,j\}}.
\]
原文字写“假设对任意 $|S|=s\ge2$ 成立，考虑 $|S|=s+1$”，计算中使用全部真子集的归纳结论：
\[
\begin{aligned}
v(x_S)&=\widetilde w_S+\sum_{A\subsetneq S}\widetilde w_A\\
&=\widetilde w_S+\sum_{A\subsetneq S}\sum_{L\subseteq A}(-1)^{|A|-|L|}v(x_L)\\
&=\widetilde w_S+\sum_{L\subsetneq S}\sum_{L\subseteq A\subsetneq S}(-1)^{|A|-|L|}v(x_L)\\
&=\widetilde w_S+\sum_{L\subsetneq S}\sum_{a=|L|}^{|S|-1}\sum_{\substack{L\subseteq A\subsetneq S\\|A|=a}}(-1)^{a-|L|}v(x_L)\\
&=\widetilde w_S+\sum_{L\subsetneq S}v(x_L)\underbrace{\sum_{m=0}^{|S|-|L|-1}\binom{|S|-|L|}{m}(-1)^m}_{0-(-1)^{|S|-|L|}}\\
&=\widetilde w_S-\sum_{L\subsetneq S}(-1)^{|S|-|L|}v(x_L).
\end{aligned}
\]
移项得到 $\widetilde w_S=v(x_S)+\sum_{L\subsetneq S}(-1)^{|S|-|L|}v(x_L)=\sum_{L\subseteq S}(-1)^{|S|-|L|}v(x_L)=w_S$，从而唯一性成立。原文字归纳句与计算实际采用的强归纳作用范围在重写中明示；不修改原命题。
