# Linearity：逐点相加的交互相加：来源数学转录

补充第2页B(2)及第4页D.1(2)：若对全部 $S\subseteq N$ 有 $v(x_S)=t(x_S)+u(x_S)$，则 $w^v_S=w^t_S+w^u_S$。

第4页原完整显示推导（输出下标固定为S，保留错误）：
\[
\begin{aligned}w^v_S&=\sum_{U\subseteq S}(-1)^{|S|-|U|}v(x_S)\\
&=\sum_{U\subseteq S}(-1)^{|S|-|U|}[t(x_S)+u(x_S)]\\
&=\sum_{U\subseteq S}(-1)^{|S|-|U|}t(x_S)+\sum_{U\subseteq S}(-1)^{|S|-|U|}u(x_S)\\
&=w^t_S+w^u_S.\end{aligned}
\]
原式并非Harsanyi定义；问题和具体反例见 cvpr-issue-linearity-index。
