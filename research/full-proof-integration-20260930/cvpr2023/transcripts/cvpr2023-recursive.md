# Recursive：始终保留变量的上下文差分：来源数学转录

补充第2、5页(6)：$i\in N$、$S\subseteq N\setminus\{i\}$。令 $w_{S\mid i\ present}=\sum_{U\subseteq S}(-1)^{|S|-|U|}v(x_{U\cup\{i\}})$，则 $w_{S\cup\{i\}}=w_{S\mid i\ present}-w_S$。

第5页完整计算：
\[
\begin{aligned}w_{S\cup\{i\}}&=\sum_{U\subseteq S\cup\{i\}}(-1)^{|S|+1-|U|}v(x_U)\\
&=\sum_{U\subseteq S}(-1)^{|S|+1-|U|}v(x_U)+\sum_{U\subseteq S}(-1)^{|S|-|U|}v(x_{U\cup\{i\}})\\
&=\sum_{U\subseteq S}(-1)^{|S|-|U|}v(x_{U\cup\{i\}})-\sum_{U\subseteq S}(-1)^{|S|-|U|}v(x_U)\\
&=w_{S\mid i\ present}-w_S.\end{aligned}
\]
