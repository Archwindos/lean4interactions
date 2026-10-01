# Appendix C(1)：固定样本与字面条件AND重构

固定 $N=\{1,\ldots,n\}$、模型 $v:\mathbb R^n\to\mathbb R$、样本 $x$ 和同一个输入基线 $r$。记 $g(A)=v(x_A)$，$b=g(\varnothing)$。二次掩码定义条件游戏 $g_T(A)=v((x_T)_A)=g(T\cap A)$。AND为 $I_g(S)=\sum_{L\subseteq S}(-1)^{|S|-|L|}g(L)$，另记 $w_A=I_g(A)$。非空OR为 $O_g^N(S)=-I_{g^c}(S)$，其中 $g^c(L)=g(N\setminus L)$；空OR单独规定 $O_g^N(\varnothing)=g(\varnothing)$。所有子集和包括空集，原始输出不要求零基线。涉及分量时分别以 $v_{and},v_{or}$ 定义对应游戏和条件游戏。 原第4、6页允许按掩码标签任意给定 $\gamma_A$，因此联合分解的最一般对象是 $g_{and}(A)=\tfrac12g(A)+\gamma_A$、$g_{or}(A)=\tfrac12g(A)-\gamma_A$，或任意满足 $g(A)=g_{and}(A)+g_{or}(A)$ 的两个集合函数。条件分量按标签定义为 $g_{and,T}(L)=g_{and}(T\cap L)$、$g_{or,T}(L)=g_{or}(T\cap L)$。原符号 $v_{and}(x_A),v_{or}(x_A)$ 在此表示这些掩码标签值；若两分量确实来自输入函数，才进一步解释为对向量的函数求值。允许 $x_i=r_i$，不要求不同标签产生不同输入，也不要求任意 $\gamma_A$ 延拓为输入空间上的单值函数。

\[g_{and}(T)=\sum_{S\subseteq T}I_{g_{and,T}}(S)=\sum_{S\subseteq T}I_{g_{and}}(S),\quad g_{and,T}(L)=g_{and}(T\cap L).\]

先用掩码交集解释两种条件系数一致，再逐项复用完整有限重构。

## 固定x与字面xT条件系数的对齐

对 $S\subseteq T$，每个 $L\subseteq S$ 也有 $L\subseteq T$，故 $T\cap L=L$。因此标签条件游戏 $g_{and,T}(L)=g_{and}(T\cap L)$ 在所有求和项上等于 $g_{and}(L)$，逐项得到 $I_{g_{and,T}}(S)=I_{g_{and}}(S)$。若分量是输入函数，掩码合成 $(x_T)_L=x_L$ 给出同一关系。

## 应用完整有限重构并核前提

对任意集合函数 $g_{and,T}$ 应用完整有限重构，得到 $\sum_{S\subseteq T}I_{g_{and,T}}(S)=g_{and,T}(T)=g_{and}(T)$，因为 $T\cap T=T$。上一条对齐又给 $\sum_{S\subseteq T}I_{g_{and}}(S)$ 同值。两个和都包含空集项 $g_{and}(\varnothing)$；不增加零基线条件。

\[\sum_{S\subseteq T}I_{g_{and,T}}(S)=\sum_{S\subseteq T}I_{g_{and}}(S)=g_{and}(T).\]

## 空集边界

$T=\varnothing$ 时唯一求和项为 $S=\varnothing$，左右都是 $g_{and}(\varnothing)$。任意标签分量与实际输入函数分量都满足此边界。

