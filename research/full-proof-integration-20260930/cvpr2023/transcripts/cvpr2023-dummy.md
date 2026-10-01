# Dummy：原命题空集反例（不修改）：来源数学转录

补充第2、4页(3)：若 $i\in N$ 且 $\forall S\subseteq N\setminus\{i\},\ v(x_{S\cup\{i\}})=v(x_S)+v(x_{\{i\}})$，则 $\forall S\subseteq N\setminus\{i\},\ w_{S\cup\{i\}}=0$。

第4页原完整推导：
\[
\begin{aligned}w_{S\cup\{i\}}&=\sum_{U\subseteq S\cup\{i\}}(-1)^{|S|+1-|U|}v(x_U)\\
&=\sum_{U\subseteq S}(-1)^{|S|+1-|U|}v(x_U)+\sum_{U\subseteq S}(-1)^{|S|-|U|}v(x_{U\cup\{i\}})\\
&=\sum_{U\subseteq S}(-1)^{|S|+1-|U|}v(x_U)+\sum_{U\subseteq S}(-1)^{|S|-|U|}[v(x_S)+v(x_{\{i\}})]\\
&=\left[\sum_{U\subseteq S}(-1)^{|S|-|U|}\right]v(x_{\{i\}})=0.\end{aligned}
\]
原第三行同样出现固定下标S；最后“=0”在S空集时错误。原命题错误，项目不发布补条件版作为替代。
