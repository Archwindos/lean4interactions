# Interaction distribution：纯AND只在指定集合有交互：来源数学转录

补充第2、5页(7)：对T子集N及实常数c，$v_T(x_S)=c$ 若 $T\subseteq S$，否则为0。则 $w_T=c$，且全部 $S\ne T$ 有 $w_S=0$。

第5–6页原完整三case证明：
\[
S\subsetneq T:\quad w_S=\sum_{U\subseteq S}(-1)^{|S|-|U|}\underbrace{v(x_U)}_{U\subseteq S\subsetneq T\Rightarrow v(x_U)=0}=0.
\]
\[
S=T:\quad w_S=w_T=\sum_{U\subseteq T}(-1)^{|T|-|U|}v(x_U)
=v(T)+\sum_{U\subsetneq T}(-1)^{|T|-|U|}\underbrace{v(x_U)}_{=0}=c.
\]
\[
S\supsetneq T:\quad w_S=c\sum_{\substack{U\subseteq S\\U\supseteq T}}(-1)^{|S|-|U|}
=c\sum_{m=0}^{|S|-|T|}\binom{|S|-|T|}{m}(-1)^m=0.
\]
原文没有写S,T不可比的case。第二式原 $v(T)$ 是模型/集合函数混记，转录保留；项目统一为g(T)。
