# Appendix C(2)：OR完整重构与原证明修正

固定 $N=\{1,\ldots,n\}$、模型 $v:\mathbb R^n\to\mathbb R$、样本 $x$ 和同一个输入基线 $r$。记 $g(A)=v(x_A)$，$b=g(\varnothing)$。二次掩码定义条件游戏 $g_T(A)=v((x_T)_A)=g(T\cap A)$。AND为 $I_g(S)=\sum_{L\subseteq S}(-1)^{|S|-|L|}g(L)$，另记 $w_A=I_g(A)$。非空OR为 $O_g^N(S)=-I_{g^c}(S)$，其中 $g^c(L)=g(N\setminus L)$；空OR单独规定 $O_g^N(\varnothing)=g(\varnothing)$。所有子集和包括空集，原始输出不要求零基线。涉及分量时分别以 $v_{and},v_{or}$ 定义对应游戏和条件游戏。 原第4、6页允许按掩码标签任意给定 $\gamma_A$，因此联合分解的最一般对象是 $g_{and}(A)=\tfrac12g(A)+\gamma_A$、$g_{or}(A)=\tfrac12g(A)-\gamma_A$，或任意满足 $g(A)=g_{and}(A)+g_{or}(A)$ 的两个集合函数。条件分量按标签定义为 $g_{and,T}(L)=g_{and}(T\cap L)$、$g_{or,T}(L)=g_{or}(T\cap L)$。原符号 $v_{and}(x_A),v_{or}(x_A)$ 在此表示这些掩码标签值；若两分量确实来自输入函数，才进一步解释为对向量的函数求值。允许 $x_i=r_i$，不要求不同标签产生不同输入，也不要求任意 $\gamma_A$ 延拓为输入空间上的单值函数。

\[g_{or}(T)=O_{g_{or,T}}^N(\varnothing)+\sum_{\substack{S\subseteq N\\S\cap T\ne\varnothing}}O_{g_{or,T}}^N(S),\quad g_{or,T}(L)=g_{or}(T\cap L).\]

相交集合族等于全部子集去掉不相交子集；两个精确重构值相减，再单独加回OR基线。

## 保持字面条件样本并修正原代入

固定 $T\subseteq N$，令 $h(L)=g_{or,T}(L)=g_{or}(T\cap L)$，保持原父式的条件掩码标签。于是 $h(N\setminus L)=g_{or}(T\setminus L)$。分量来自输入函数时，这才写成 $v_{or}((x_T)_{N\setminus L})=v_{or}(x_{T\setminus L})$；原第13页直接使用 $v_{or}(x_{N\setminus L})$ 一般不等。证明对任意标签函数成立，无需其能延拓为输入函数。

## 完整辅助引理：相交子集族是两个子集族之差

对每个 $S\subseteq N$，$S\cap T=\varnothing$ 当且仅当 $S\subseteq N\setminus T$。故相交子集族为 $\mathcal P(N)\setminus\mathcal P(N\setminus T)$，后者包含于前者；有限求和等于两个全族的和相减。空集在两个全族中都出现，始终不属于相交族。

\[\sum_{\substack{S\subseteq N\\S\cap T\ne\varnothing}}d_S=\sum_{S\subseteq N}d_S-\sum_{S\subseteq N\setminus T}d_S.\]

## 对补集负游戏作两次重构

令 $f(L)=-h(N\setminus L)$。对非空 $S$，有限和对整体负号的线性性给 $O_h^N(S)=I_f(S)$。相交族不含空集，故可逐项替换。两次重构给 $f(N)-f(N\setminus T)=-h(\varnothing)+h(T)$；这里由 $T\subseteq N$ 有 $N\setminus(N\setminus T)=T$。再用 $h(T)=g_{or}(T)$、$h(\varnothing)=g_{or}(\varnothing)$。

\[\sum_{S\cap T\ne\varnothing}O_h^N(S)=h(T)-h(\varnothing)=g_{or}(T)-g_{or}(\varnothing).\]

## 单独加回原空OR基线

空OR按定义单列 $O_h^N(\varnothing)=h(\varnothing)=g_{or}(\varnothing)$。加回此基线便重构 $g_{or}(T)$。$T=\varnothing$ 时相交族为空，只有基线；$T=N$ 时重构完整标签值。因此也涵盖原case1/2在空掩码时重合的边界。

## 带非零基线的二变量检验

令 $N=\{1,2\}$，$g(\varnothing)=7$、$g(\{1\})=8$、$g(\{2\})=9$、$g(\{1,2\})=13$。于是 $w_\varnothing=7$、$w_{\{1\}}=1$、$w_{\{2\}}=2$、$w_{\{1,2\}}=3$。 固定原输入的OR系数是 $O_g^N(\{1\})=4$、$O_g^N(\{2\})=5$、$O_g^N(N)=-3$，空值7。对原父式的 $T=\{1\}$，应使用条件游戏 $h_T(L)=g(T\cap L)$，其四个输出依次为7、8、7、8，OR系数为1、0、0，空值7。相交求和使用 $\{1\}$ 与 $N$，所以条件式给 $7+1+0=8=g(T)$。固定原输入式也给 $7+4-3=8$，但逐项系数不同。$T=\varnothing$ 时仅基线7；$T=N$ 时两种游戏一致，得 $7+4+5-3=13$。

