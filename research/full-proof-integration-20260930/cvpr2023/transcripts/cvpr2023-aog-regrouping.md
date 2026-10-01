# AOG：共享AND子模式的等价重组：来源数学转录

正文第5页3.3：And-Sum可等价改写AOG；beta={x5,x6}，{x4,x5,x6}改为{x4,beta}；一般C_S=product_{S′ in Child(S)}C_S′。

**正文PDF第5页3.3，完整有关等价重组的推导段（中文翻译与公式转录）。** 原SCM表示And-Sum：
\[
v(x)\approx\sum_{S\in\Omega}w_SC_S(x)=\sum_{S\in\Omega}w_S.
\]
作者说这一And-Sum可等价转为AOG。三层AOG底层为n个输入变量，第二层每个AND节点编码孩子变量的AND关系；例如 $x_4x_5x_6$ 是 $S=\{x_4,x_5,x_6\}$ 的因果模式，其 $w_S=2.0$。根是noisy OR节点，累加所有孩子AND节点的效应：$\mathrm{output}=\sum_{S\in\Omega}w_SC_S$。
为进一步简化，作者提取不同模式共享的coalition作为新节点：$x_5,x_6$ 在多个模式里共同出现，于是设
\[
\beta=\{x_5,x_6\},\qquad
\{x_4,x_5,x_6\}\longmapsto\{x_4,\beta\}.
\]
于是每个中间层coalition/pattern S的触发状态由其全部孩子的触发状态相乘：
\[
C_S=\prod_{S'\in\operatorname{Child}(S)}C_{S'}.
\]
Child(S)是组成S的全部输入变量或coalition；S触发当且仅当所有孩子触发。上述内容是作者的未编号等价推导；没有独立的树归纳定理。MDL目标及其贪心选择属于下一算法段，单独登记，不伪称此段已证明全局最优。
