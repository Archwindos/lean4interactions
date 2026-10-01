# OR对偶：反转掩码状态的负AND变换

固定 $N=\{1,\ldots,n\}$、模型 $v:\mathbb R^n\to\mathbb R$、样本 $x$ 和同一个输入基线 $r$。记 $g(A)=v(x_A)$，$b=g(\varnothing)$。二次掩码定义条件游戏 $g_T(A)=v((x_T)_A)=g(T\cap A)$。AND为 $I_g(S)=\sum_{L\subseteq S}(-1)^{|S|-|L|}g(L)$，另记 $w_A=I_g(A)$。非空OR为 $O_g^N(S)=-I_{g^c}(S)$，其中 $g^c(L)=g(N\setminus L)$；空OR单独规定 $O_g^N(\varnothing)=g(\varnothing)$。所有子集和包括空集，原始输出不要求零基线。涉及分量时分别以 $v_{and},v_{or}$ 定义对应游戏和条件游戏。

\[O_g^N(S)=-I_{g^c}(S),\qquad g^c(L)=g(N\setminus L),\ S\ne\varnothing\]

非空OR定义就是补集游戏的负Möbius变换；空集采用作者另外规定的基线值。

## 明确反转状态的集合函数

把原样本中“保留”与“使用基线”两个状态交换，新的集合函数是 $g^c(L)=g(N\setminus L)$。这里反转的是有限状态索引，不是把原模型改成另一个模型。

## 逐项对比非空OR与AND定义

对 $S\ne\varnothing$，OR式的各项就是 $g^c$ 的AND变换，但整体有负号。数值一般互为相反数，绝对值相等。空OR另规定为 $g(\varnothing)$；负AND在空集为 $-g(N)$，一般不同，必须分开。

\[O_g^N(S)=-I_{g^c}(S)\qquad(S\ne\varnothing).\]

## 二变量与空集例子

令 $N=\{1,2\}$，$g(\varnothing)=7$、$g(\{1\})=8$、$g(\{2\})=9$、$g(\{1,2\})=13$。于是 $w_\varnothing=7$、$w_{\{1\}}=1$、$w_{\{2\}}=2$、$w_{\{1,2\}}=3$。 补集游戏 $g^c$ 的两个单变量AND值为 $-4$、$-5$，二阶值为3；对应OR值为4、5、$-3$，空OR基线为7。反转AND的空值为13，不能用其负值 $-13$ 代替7。

