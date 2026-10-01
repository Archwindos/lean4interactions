# Theorem 1精确部分：全部掩码的AND重构

固定 $N=\{1,\ldots,n\}$、模型 $v:\mathbb R^n\to\mathbb R$、样本 $x$ 和同一个输入基线 $r$。记 $g(A)=v(x_A)$，$b=g(\varnothing)$。二次掩码定义条件游戏 $g_T(A)=v((x_T)_A)=g(T\cap A)$。AND为 $I_g(S)=\sum_{L\subseteq S}(-1)^{|S|-|L|}g(L)$，另记 $w_A=I_g(A)$。非空OR为 $O_g^N(S)=-I_{g^c}(S)$，其中 $g^c(L)=g(N\setminus L)$；空OR单独规定 $O_g^N(\varnothing)=g(\varnothing)$。所有子集和包括空集，原始输出不要求零基线。涉及分量时分别以 $v_{and},v_{or}$ 定义对应游戏和条件游戏。

\[\forall T\subseteq N,\quad v(x_T)=\sum_{S\subseteq T}I_{and}(S\mid x)\]

原始AND变换含空集系数。所有子集的有限消去留下当前掩码输出，精确部分不依赖稀疏假设。

## 适配原始AND定义

固定x和r后，论文 $I_{and}(A\mid x)$ 就是 $I_g(A)$。它采用原始输出，空集为b。

## 有限双重求和与区间消去

对固定 $S$ 展开 $w_A$。每对 $L\subseteq A\subseteq S$ 只出现一次，交换有限求和不改变项。固定 $L$ 后，用 $B=A\setminus L\subseteq S\setminus L$ 给出一一对应，且 $|A|-|L|=|B|$。若 $L\ne S$，任选 $i\in S\setminus L$，把 $B$ 按是否含 $i$ 配对，符号相反，内和为零；若 $L=S$，只有 $B=\varnothing$，内和为一。因此只留下 $g(S)$。

\[\sum_{A\subseteq S}w_A=\sum_{L\subseteq S}g(L)\sum_{B\subseteq S\setminus L}(-1)^{|B|}=g(S).\]

## 空集与两个变量核对

$S=\varnothing$ 时只有 $w_\varnothing=b$。取 $g(\varnothing)=7,g(\{1\})=8,g(\{2\})=9,g(\{1,2\})=13$，系数为7,1,2,3；完整输入和为13，空输入为7，单变量输入分别为8和9。

