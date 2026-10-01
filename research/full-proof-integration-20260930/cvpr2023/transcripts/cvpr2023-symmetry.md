# Symmetry：相同合作输出具有相同交互：来源数学转录

补充第2、4页(4)：若 $i,j\in N$ 且对全部 $U\subseteq N\setminus\{i,j\}$ 有 $v(x_{U\cup\{i\}})=v(x_{U\cup\{j\}})$，则同一范围全部S满足 $w_{S\cup\{i\}}=w_{S\cup\{j\}}$。

补充第4页末至第5页首完整计算：
\[
\begin{aligned}w_{S\cup\{i\}}&=\sum_{U\subseteq S\cup\{i\}}(-1)^{|S|+1-|U|}v(x_U)\\
&=\sum_{U\subseteq S}(-1)^{|S|+1-|U|}v(x_U)+\sum_{U\subseteq S}(-1)^{|S|-|U|}v(x_{U\cup\{i\}})\\
&=\sum_{U\subseteq S}(-1)^{|S|+1-|U|}v(x_U)+\sum_{U\subseteq S}(-1)^{|S|-|U|}v(x_{U\cup\{j\}})\\
&=\sum_{U\subseteq S\cup\{j\}}(-1)^{|S|+1-|U|}v(x_U)=w_{S\cup\{j\}}.\end{aligned}
\]
