# 掩码消失：含已遮掉变量的AND交互为零

固定 $N=\{1,\ldots,n\}$、模型 $v:\mathbb R^n\to\mathbb R$、样本 $x$ 和同一个输入基线 $r$。记 $g(A)=v(x_A)$，$b=g(\varnothing)$。二次掩码定义条件游戏 $g_T(A)=v((x_T)_A)=g(T\cap A)$。AND为 $I_g(S)=\sum_{L\subseteq S}(-1)^{|S|-|L|}g(L)$，另记 $w_A=I_g(A)$。非空OR为 $O_g^N(S)=-I_{g^c}(S)$，其中 $g^c(L)=g(N\setminus L)$；空OR单独规定 $O_g^N(\varnothing)=g(\varnothing)$。所有子集和包括空集，原始输出不要求零基线。涉及分量时分别以 $v_{and},v_{or}$ 定义对应游戏和条件游戏。

\[S\not\subseteq T\ \Rightarrow\ I_{and}(S\mid x_T)=0\]

同一基线的两次掩码等于集合交集；已缺失变量使子集对的输出相同而符号相反。

## 完整掩码合成引理

固定坐标 $i$：若 $i\in T\cap L$，两次掩码都保留 $x_i$；若 $i\notin L$，第二次给 $r_i$；若 $i\in L\setminus T$，第一次已经给 $r_i$，第二次保留的仍是 $r_i$。逐坐标相同，得 $(x_T)_L=x_{T\cap L}$。两次必须使用同一输入基线 $r$。

\[g_T(L)=g(T\cap L).\]

## 选出已被遮掉的变量并配对子集

若 $S\not\subseteq T$，取 $i\in S\setminus T$。每个 $U\subseteq S\setminus\{i\}$ 满足 $T\cap(U\cup\{i\})=T\cap U$，故对应条件输出相同。交互中的两项符号相反，逐对消去，结果为零。不要求模型线性或 $g(\varnothing)=0$。

\[S\not\subseteq T\ \Longrightarrow\ I_{g_T}(S)=0.\]

## 空集和未掩码边界

$S=\varnothing$ 始终包含于 $T$，因此消失命题不包括空交互；空交互为 $b$。$T=N$ 时不存在 $S\not\subseteq T$。$T=\varnothing$ 时，全部非空 $S$ 的条件交互为零。

