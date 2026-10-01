# Theorem 5：环境中的高阶边际分解：来源数学转录

补充第2、6页Theorem 5：$T\subseteq N\setminus S$，定义 $\Delta v_T(x_S)=\sum_{L\subseteq T}(-1)^{|T|-|L|}v(x_{L\cup S})$，则 $\Delta v_T(x_S)=\sum_{U\subseteq S}w_{T\cup U}$。第6页另给 $T=\{i\}$ 的特例 $\Delta v_{\{i\}}(x_S)=\sum_{L\subseteq S}w_{L\cup\{i\}}$，并引用[40]。

第6页作者全部计算如下（用L′等哑变量；末两行作者按大小l计数时，符号指数仍印作|L|，这里保留说明）：
\[
\begin{aligned}\Delta v_T(x_S)&=\sum_{L\subseteq T}(-1)^{|T|-|L|}v(x_{L\cup S})\\
&=\sum_{L\subseteq T}(-1)^{|T|-|L|}\sum_{K\subseteq L\cup S}w_K\\
&=\sum_{L\subseteq T}(-1)^{|T|-|L|}\sum_{L'\subseteq L}\sum_{S'\subseteq S}w_{L'\cup S'}\\
&=\sum_{S'\subseteq S}\left[\sum_{L\subseteq T}(-1)^{|T|-|L|}\sum_{L'\subseteq L}w_{L'\cup S'}\right]\\
&=\sum_{S'\subseteq S}\left[\sum_{L'\subseteq T}\sum_{L'\subseteq L\subseteq T}(-1)^{|T|-|L|}w_{L'\cup S'}\right]\\
&=\sum_{S'\subseteq S}\left[w_{T\cup S'}+\sum_{L'\subsetneq T}\sum_{l=|L'|}^{|T|}\binom{|T|-|L'|}{l-|L'|}(-1)^{|T|-|L|}w_{L'\cup S'}\right]\\
&=\sum_{S'\subseteq S}\left[w_{T\cup S'}+\sum_{L'\subsetneq T}w_{L'\cup S'}\underbrace{\sum_{l=|L'|}^{|T|}\binom{|T|-|L'|}{l-|L'|}(-1)^{|T|-|L|}}_{=0}\right]\\
&=\sum_{S'\subseteq S}w_{T\cup S'}.
\end{aligned}
\]
第三行用L与S不相交；第二行用Theorem1。
