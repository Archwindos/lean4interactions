# Theorem 2：完整字面AND-OR联合匹配

固定 $N=\{1,\ldots,n\}$、模型 $v:\mathbb R^n\to\mathbb R$、样本 $x$ 和同一个输入基线 $r$。记 $g(A)=v(x_A)$，$b=g(\varnothing)$。二次掩码定义条件游戏 $g_T(A)=v((x_T)_A)=g(T\cap A)$。AND为 $I_g(S)=\sum_{L\subseteq S}(-1)^{|S|-|L|}g(L)$，另记 $w_A=I_g(A)$。非空OR为 $O_g^N(S)=-I_{g^c}(S)$，其中 $g^c(L)=g(N\setminus L)$；空OR单独规定 $O_g^N(\varnothing)=g(\varnothing)$。所有子集和包括空集，原始输出不要求零基线。涉及分量时分别以 $v_{and},v_{or}$ 定义对应游戏和条件游戏。 原第4、6页允许按掩码标签任意给定 $\gamma_A$，因此联合分解的最一般对象是 $g_{and}(A)=\tfrac12g(A)+\gamma_A$、$g_{or}(A)=\tfrac12g(A)-\gamma_A$，或任意满足 $g(A)=g_{and}(A)+g_{or}(A)$ 的两个集合函数。条件分量按标签定义为 $g_{and,T}(L)=g_{and}(T\cap L)$、$g_{or,T}(L)=g_{or}(T\cap L)$。原符号 $v_{and}(x_A),v_{or}(x_A)$ 在此表示这些掩码标签值；若两分量确实来自输入函数，才进一步解释为对向量的函数求值。允许 $x_i=r_i$，不要求不同标签产生不同输入，也不要求任意 $\gamma_A$ 延拓为输入空间上的单值函数。

\[v(x_T)=\sum_{S\subseteq T}I_{g_{and,T}}(S)+O_{g_{or,T}}^N(\varnothing)+\sum_{\substack{S\subseteq N\\S\cap T\ne\varnothing}}O_{g_{or,T}}^N(S).\]

任意掩码标签分量分别在条件标签游戏中精确重构，两个分量相加恢复原模型输出；标签碰撞不影响此有限恒等式。

## 完整掩码合成引理

固定坐标 $i$：若 $i\in T\cap L$，两次掩码都保留 $x_i$；若 $i\notin L$，第二次给 $r_i$；若 $i\in L\setminus T$，第一次已经给 $r_i$，第二次保留的仍是 $r_i$。逐坐标相同，得 $(x_T)_L=x_{T\cap L}$。两次必须使用同一输入基线 $r$。

\[g_T(L)=g(T\cap L).\]

## 同一掩码上的原分解

原分解在每个掩码标签上满足 $g(U)=g_{and}(U)+g_{or}(U)$。特别是作者任意的 $\gamma_U$ 参数化，逐项相加立即抵消 $\gamma_U$。即使某个 $x_i=r_i$ 使两标签对应同一向量，两分量仍可作为集合函数使用；证明不另加标签值能延拓为输入函数的条件。

## 固定x与字面xT条件系数的对齐

对 $S\subseteq T$，每个 $L\subseteq S$ 也有 $L\subseteq T$，故 $T\cap L=L$。因此标签条件游戏 $g_{and,T}(L)=g_{and}(T\cap L)$ 在所有求和项上等于 $g_{and}(L)$，逐项得到 $I_{g_{and,T}}(S)=I_{g_{and}}(S)$。若分量是输入函数，掩码合成 $(x_T)_L=x_L$ 给出同一关系。

## 应用完整有限重构并核前提

对任意集合函数 $g_{and,T}$ 应用完整有限重构，得到 $\sum_{S\subseteq T}I_{g_{and,T}}(S)=g_{and,T}(T)=g_{and}(T)$，因为 $T\cap T=T$。上一条对齐又给 $\sum_{S\subseteq T}I_{g_{and}}(S)$ 同值。两个和都包含空集项 $g_{and}(\varnothing)$；不增加零基线条件。

\[\sum_{S\subseteq T}I_{g_{and,T}}(S)=\sum_{S\subseteq T}I_{g_{and}}(S)=g_{and}(T).\]

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

## 相加得到父定理字面式

AND部分重构 $g_{and}(T)$，OR部分重构 $g_{or}(T)$；相加并使用原分解，得到 $g(T)=v(x_T)$。两个空项合计为 $g(\varnothing)$。全部系数仍由条件标签游戏 $g_{and,T},g_{or,T}$ 定义，输入函数分量版本是其特例。

\[v(x_T)=\sum_{S\subseteq T}I_{g_{and,T}}(S)+O_{g_{or,T}}^N(\varnothing)+\sum_{S\subseteq N:S\cap T\ne\varnothing}O_{g_{or,T}}^N(S).\]

