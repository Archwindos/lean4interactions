# Theorem 1：从掩蔽输出到公共重构定理

固定原文的 DNN、输入样本 (\boldsymbol{x}) 和同一套掩蔽基线。变量总体为有限集合 $N=\{1,\ldots,n\}$。定义集合函数 $g(S)=v(\boldsymbol{x}_S)$：(S) 中的变量保留原值，其余变量按固定基线掩蔽。Lean 取 `maskedOutput : Game (Fin n)`，所有 `Finset (Fin n)` 恰好表示原文的全部 (2^n) 个掩蔽集合。

原文要求保留所有模式，即 $\Omega=2^N$，并定义

\[
w_T=\sum_{L\subseteq T}(-1)^{|T|-|L|}g(L)=I_g(T).
\]

SCM 中的模式 (T) 在 (\boldsymbol{x}_S) 上被触发，当且仅当 $T\subseteq S$。原文附录 C 直接将它写成

\[
Y(\boldsymbol{x}_S)=\sum_{T\subseteq S}w_T=R_{I_g}(S).
\]

因此原文 Theorem 1 的数学核心恰好是公共结果 `harsanyi-reconstruction`，调用 `Harsanyi.reconstruction maskedOutput S` 得到 $Y(\boldsymbol{x}_S)=g(S)$。共同中文证明由 `proof-reconstruction-v1` 维护，本条目只保存来源和定义适配，未复制公共证明正文。

空集没有删除。原文附录 C 的基例明确写出 $w_\varnothing=v(\boldsymbol{x}_\varnothing)$。模式空集在每个掩蔽集合上都触发，贡献基线；公共库的 `interaction_empty` 采用相同约定。本适配没有添加 $g(\varnothing)=0$，也没有将原函数改为 `centered g`。

正文来源为 v6 PDF 第 3 页、印刷页 3、§3.1 Theorem 1；TeX 为 `AOG.tex:205–215`，标签 `th:harsanyi-faithful`。完整证明位于附录 C 的 PDF/印刷页 14–15，TeX `appendix.tex:131–186`。原文的重构证明通过交换双重求和和二项式抵消展开；公共证明为项目新增证明，关系记录只认定规范化命题相同及复用同一公共证明，未认定两种论证方法相同。

实际适配声明与公理审计在 `reports/public-pilot/20260930-sparse-concepts-v6/PublicPilot.lean` 和 `lean-applications.log`。这个结果针对固定样本的全模式精确重构；不据此宣称剪枝后的稀疏图精确重构、因果识别、整个 DNN 的性质或整篇论文全部已审校。
