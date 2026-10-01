#!/usr/bin/env python3
"""Organize full source mathematics, then merge independently reviewed result fragments."""
import copy
import json
from pathlib import Path
P=Path(__file__).resolve().parent;ROOT=P.parents[2];PAPER='iclr2024-generalizable'
inv=json.loads((P/'inventory.json').read_text())
src=inv['sources'][0]['source_id']
statements={
'f11-model-mask':r'v:\mathbb R^n\to\mathbb R,\quad x=[x_1,\ldots,x_n]^\top,\quad N=\{1,\ldots,n\}',
'f11-and-definition':r'I_{\mathrm{and}}(S\mid x)=\sum_{T\subseteq S}(-1)^{|S|-|T|}v(x_T),\quad I_{\mathrm{and}}(\varnothing\mid x)=v(x_\varnothing)',
'f11-and-mask-zero':r'i\in S,\ x_i\text{ masked}\quad\Longrightarrow\quad I_{\mathrm{and}}(S\mid x_{\mathrm{masked}})=0',
'f11-or-definition':r'I_{\mathrm{or}}(S\mid x)=-\sum_{T\subseteq S}(-1)^{|S|-|T|}v(x_{N\setminus T}),\quad I_{\mathrm{or}}(\varnothing\mid x)=v(x_\varnothing)',
'f11-or-duality':r'S\ne\varnothing:\quad I_{\mathrm{or}}(S\mid x)=-I_{h}(S),\quad h(T)=v(x_{N\setminus T})',
'f11-significant-definition':r'\Omega=\{S\subseteq N:|I(S\mid x)|>\tau\}',
'iclr2024-generalizable-theorem1':r'\forall S\subseteq N:\quad v(x_S)=\sum_{T\subseteq S}I_{\mathrm{and}}(T\mid x)',
'f11-theorem1-approx':r'v(x_S)=\sum_{T\subseteq S}I_{\mathrm{and}}(T\mid x)\approx\sum_{T\subseteq S:T\in\Omega}I_{\mathrm{and}}(T\mid x),\quad|\Omega|\ll2^n',
'iclr2024-generalizable-andor':r'\begin{aligned}v(x_T)&=v_{\mathrm{and}}(x_T)+v_{\mathrm{or}}(x_T)\\&=\sum_{S\subseteq T}I_{\mathrm{and}}(S\mid x_T)+\sum_{S\in\{S:S\cap T\ne\varnothing\}\cup\{\varnothing\}}I_{\mathrm{or}}(S\mid x_T)\end{aligned}',
'iclr2024-generalizable-and':r'\forall T\subseteq N:\quad v_{\mathrm{and}}(x_T)=\sum_{S\subseteq T}I_{\mathrm{and}}(S\mid x)',
'iclr2024-generalizable-or':r'v_{\mathrm{or}}(x_T)=I_{\mathrm{or}}(\varnothing\mid x_T)+\sum_{S:S\cap T\ne\varnothing}I_{\mathrm{or}}(S\mid x_T),\quad I_{\mathrm{or}}(\varnothing\mid x_T)=v_{\mathrm{or}}(x_\varnothing)',
'f11-proposition1':r'\begin{aligned}v(x_T)&=\sum_{S\subseteq T}I_{\mathrm{and}}(S\mid x_T)+\sum_{S\in\{S:S\cap T\ne\varnothing\}\cup\{\varnothing\}}I_{\mathrm{or}}(S\mid x_T)\\&\approx v(x_\varnothing)+\sum_{\varnothing\ne S\subseteq T:S\in\Omega^{\mathrm{and}}}I_{\mathrm{and}}(S\mid x_T)+\sum_{S\cap T\ne\varnothing:S\in\Omega^{\mathrm{or}}}I_{\mathrm{or}}(S\mid x_T),\quad |\Omega^{\mathrm{and}}|,|\Omega^{\mathrm{or}}|\ll2^n\end{aligned}',
'f11-boolean-decomposition':r'\begin{aligned}f(x)&=x_1\wedge x_2\wedge x_3+x_2\wedge x_3+x_3\wedge x_4+x_4\vee x_5\\x_4\vee x_5&=x_4+x_5-x_4\wedge x_5,\qquad x_i\in\{0,1\}\end{aligned}',
'f11-transferability':r'\begin{aligned}\Omega_{\mathrm{shared}}^{\mathrm{and/or}}&=\bigcap_{i=1}^m\Omega^{\mathrm{and/or},(i)}\\s_{\mathrm{and/or}}^{(i)}&=|\Omega_{\mathrm{shared}}^{\mathrm{and/or}}|/|\Omega^{\mathrm{and/or},(i)}|\end{aligned}',
'f11-reparameterization':r'v_{\mathrm{and}}^{(i)}(x_T)=0.5v^{(i)}(x_T)+\gamma_T^{(i)},\quad v_{\mathrm{or}}^{(i)}(x_T)=0.5v^{(i)}(x_T)-\gamma_T^{(i)}',
'f11-objectives':r'\begin{aligned}\text{Eq.(4)}:\ &\min_{\{\gamma_T\}}\|I_{\mathrm{and}}\|_1+\|I_{\mathrm{or}}\|_1\\\text{Eq.(5)}:\ &\min_{\{\gamma_T^{(i)}\}}\|\operatorname{rowmax}(I_{\mathrm{and}})\|_1+\|\operatorname{rowmax}(I_{\mathrm{or}})\|_1\\\text{Eq.(6)}:\ &\min_{\{\gamma_T^{(i)}\}}(\|\operatorname{rowmax}(I_{\mathrm{and}})\|_1+\|\operatorname{rowmax}(I_{\mathrm{or}})\|_1)+\alpha(\|I_{\mathrm{and}}\|_1+\|I_{\mathrm{or}}\|_1)\end{aligned}',
'f11-rowmax-penalty':r'\operatorname{rowmax}(I_{\mathrm{and}})=[\|I_{\mathrm{and}}[1,:]\|_\infty,\ldots,\|I_{\mathrm{and}}[2^n,:]\|_\infty]^\top',
'f11-shared-gamma':r'\begin{aligned}\gamma_T^{(i)}&=\bar\gamma_T+\hat\gamma_T^{(i)},\quad|\hat\gamma_T^{(i)}|<\tau_\gamma^{(i)}\\\tau_\gamma^{(i)}&=0.5\mathbb E_x[|v^{(i)}(x)-v^{(i)}(x_\varnothing)|]\\|\hat\gamma_T^{(i)}|>\tau_\gamma^{(i)}&\ \Longrightarrow\ \hat\gamma_T^{(i)}=\tau_\gamma^{(i)}\operatorname{sign}(\hat\gamma_T^{(i)})\end{aligned}',
'f11-and-variance':r'\operatorname{Var}(I_{\mathrm{and}}^{\prime(i)}(T))=2^{|T|}\sigma^2',
'f11-or-variance':r'\operatorname{Var}(I_{\mathrm{or}}^{\prime(i)}(T))=2^{|T|}\sigma^2',
'f11-noise-error':r'\begin{aligned}v^{(i)}(x_T)&=v_{\mathrm{and}}^{(i)}(x_T)+v_{\mathrm{or}}^{(i)}(x_T)+\epsilon_T^{(i)}\\|\epsilon_T^{(i)}|&<\tau_\epsilon^{(i)}=0.02|v^{(i)}(x)-v^{(i)}(x_\varnothing)|\\|\epsilon^{(i)}|>\tau_\epsilon^{(i)}&\ \Longrightarrow\ |\epsilon^{(i)}|=\tau_\epsilon^{(i)}\operatorname{sign}(\epsilon_T^{(i)})\end{aligned}',
'f11-shapley':r'\phi(i)=\sum_{S\subseteq N:S\ni i}\frac{1}{|S|}I_{\mathrm{and}}(S\mid x)',
'f11-mask-complexity':r'|2^N|=2^{|N|}=2^n',
'f11-alpha-zero':r'\alpha=0:\quad\text{Eq.(6) loss}=\text{Eq.(5) loss}',
'f11-matching-metric':r'm=\frac{\sum_{S\in\{\mathrm{top}\ k\ \mathrm{interactions}\}}|I(S)|}{\sum_{S\in\{\mathrm{top}\ k\ \mathrm{interactions}\}}|I(S)|+|v(N)-v(\varnothing)-\sum_{S\in\{\mathrm{top}\ k\ \mathrm{interactions}\}}I(S)|}'
}
and_proof=r'''以下是附录 C(1) 第12–13页作者全部数学推导的中文译文和公式转录，保留 Eq.(8) 第一行的 \(x_T\) 原记号。

作者先陈述固定样本 \(x\) 的 AND 重构，并定义
\[I_{\mathrm{and}}(S\mid x)=\sum_{L\subseteq S}(-1)^{|S|-|L|}v_{\mathrm{and}}(x_L).\]
为计算 \(\sum_{S\subseteq T}I_{\mathrm{and}}(S\mid x)\)，先交换 \(L\subseteq S\subseteq T\) 的求和次序。固定 \(L\)，计算含 \(L\) 的所有 \(S\) 对输出 \(v_{\mathrm{and}}(x_L)\) 的线性组合，再对 \(L\subseteq T\) 累加。

情形(1)：\(L=S=T\)，唯一项为 \((-1)^{|T|-|T|}v_{\mathrm{and}}(x_L)=v_{\mathrm{and}}(x_L)\)。

情形(2)：\(L\subseteq S\subseteq T,L\ne T\)。令 \(m=|S|-|L|\)，则 \(0\le m\le|T|-|L|\)，这样的 \(S\) 有 \(\binom{|T|-|L|}{m}\) 个。因此
\[\sum_{S:L\subseteq S\subseteq T}(-1)^{|S|-|L|}v_{\mathrm{and}}(x_L)=v_{\mathrm{and}}(x_L)\sum_{m=0}^{|T|-|L|}\binom{|T|-|L|}{m}(-1)^m=0.\]
作者 Eq.(8) 全部计算为
\[\begin{aligned}
\sum_{S\subseteq T}I_{\mathrm{and}}(S\mid x_T)
&=\sum_{S\subseteq T}\sum_{L\subseteq S}(-1)^{|S|-|L|}v_{\mathrm{and}}(x_L)\\
&=\sum_{L\subseteq T}\sum_{S:L\subseteq S\subseteq T}(-1)^{|S|-|L|}v_{\mathrm{and}}(x_L)\\
&=v_{\mathrm{and}}(x_T)+\sum_{L\subseteq T:L\ne T}v_{\mathrm{and}}(x_L)\underbrace{\sum_{m=0}^{|T|-|L|}\binom{|T|-|L|}{m}(-1)^m}_{=0}\\
&=v_{\mathrm{and}}(x_T).
\end{aligned}\]
固定 \(x\) 的系数定义与显示式 \(x_T\) 的对应在项目重写中另作解释；这里不静默改动原式。
'''
or_proof=r'''以下转录附录 C(2) 第13–14页完整原数学论证，保留错误中间断言与原记号。作者欲证
\[v_{\mathrm{or}}(x_T)=I_{\mathrm{or}}(\varnothing\mid x_T)+\sum_{S:S\cap T\ne\varnothing}I_{\mathrm{or}}(S\mid x_T),\quad I_{\mathrm{or}}(\varnothing\mid x_T)=v_{\mathrm{or}}(x_\varnothing).\]
原定义是 \(I_{\mathrm{or}}(S\mid x)=-\sum_{L\subseteq S}(-1)^{|S|-|L|}v_{\mathrm{or}}(x_{N\setminus L})\)。作者交换求和次序，固定 \(L\subseteq N\)，按下列四类计算 \(S\supseteq L,S\cap T\ne\varnothing\) 的系数。

情形(1)：\(L=N\setminus T\)。令 \(|S'|=|S|-|L|\)，其范围为 \(1\le |S'|\le|T|\)，对应子集数为 \(\binom{|T|}{|S'|}\)，原式为
\[\sum_{S:S\cap T\ne\varnothing,S\supseteq L}(-1)^{|S|-|L|}v_{\mathrm{or}}(x_{N\setminus L})=v_{\mathrm{or}}(x_T)\underbrace{\sum_{|S'|=1}^{|T|}\binom{|T|}{|S'|}(-1)^{|S'|}}_{=-1}=-v_{\mathrm{or}}(x_T).\]

情形(2)：\(L=N\)，于是 \(S=N\)。原文系数为 \((-1)^{|N|-|N|}v_{\mathrm{or}}(x_\varnothing)=v_{\mathrm{or}}(x_\varnothing)\)。

情形(3)：\(L\cap T\ne\varnothing,L\ne N\)。原文定义
\[S'=\{i:i\in S,i\notin L,i\in N\setminus T\},\quad S''=\{i:i\in S,i\notin L,i\in T\},\]
满足 \(|S|-|L|=|S'|+|S''|\)、\(0\le|S''|\le|T|-|T\cap L|\)，并写 \(S'+S''+L=S\)。固定 \(S'\)，原文按 \(|S''|\) 计数并断言
\[v_{\mathrm{or}}(x_{N\setminus L})\sum_{S'\subseteq N\setminus T\setminus L}\underbrace{\sum_{|S''|=0}^{|T|-|T\cap L|}\binom{|T|-|T\cap L|}{|S''|}(-1)^{|S'|+|S''|}}_{=0}=0.\]
此处内层逐项为0的断言有原证明错误；原式保留，证据与忠实修正证明另列。

情形(4)：\(L\cap T=\varnothing,L\ne N\setminus T\)。原文用相同 \(S'\)，并定义 \(S''=\{i:i\in S,i\in T\}\)，写 \(0\le|S''|\le|T|\) 与 \(S'+S''+L=S\)，随后计算
\[v_{\mathrm{or}}(x_{N\setminus L})\sum_{S'\subseteq N\setminus T\setminus L}\underbrace{\sum_{|S''|=0}^{|T|}\binom{|T|}{|S''|}(-1)^{|S'|+|S''|}}_{=0}=0.\]
这份原分类把不满足 \(S\cap T\ne\varnothing\) 的 \(|S''|=0\) 纳入内层；不在原文层修正。

为完整保存 Eq.(9)，下面的 \(C_3(L)\)、\(C_4(L)\) **仅是项目排版缩写**，分别指上面情形(3)、(4)内外两层和，并非新定义或修正版。
\[\begin{aligned}
\sum_{S:S\cap T\ne\varnothing}I_{\mathrm{or}}(S\mid x_T)
&=\sum_{S:S\cap T\ne\varnothing}\left[-\sum_{L\subseteq S}(-1)^{|S|-|L|}v_{\mathrm{or}}(x_{N\setminus L})\right]\\
&=-\sum_{L\subseteq N}\sum_{S:S\cap T\ne\varnothing,S\supseteq L}(-1)^{|S|-|L|}v_{\mathrm{or}}(x_{N\setminus L})\\
&=-\left[\sum_{|S'|=1}^{|T|}\binom{|T|}{|S'|}(-1)^{|S'|}\right]v_{\mathrm{or}}(x_T)-v_{\mathrm{or}}(x_\varnothing)\\
&\quad-\sum_{L\cap T\ne\varnothing,L\ne N}C_3(L)v_{\mathrm{or}}(x_{N\setminus L})\\
&\quad-\sum_{L\cap T=\varnothing,L\ne N\setminus T}C_4(L)v_{\mathrm{or}}(x_{N\setminus L})\\
&=-(-1)v_{\mathrm{or}}(x_T)-v_{\mathrm{or}}(x_\varnothing)\\
&\quad-\sum_{L\cap T\ne\varnothing,L\ne N}\left[\sum_{S'\subseteq N\setminus T\setminus L}0\right]v_{\mathrm{or}}(x_{N\setminus L})\\
&\quad-\sum_{L\cap T=\varnothing,L\ne N\setminus T}\left[\sum_{S'\subseteq N\setminus T\setminus L}0\right]v_{\mathrm{or}}(x_{N\setminus L})\\
&=v_{\mathrm{or}}(x_T)-v_{\mathrm{or}}(x_\varnothing).
\end{aligned}\]
原式在空 \(T\) 时的分类边界也由项目新证明明确覆盖，不向原命题加入非空限制。
'''
variance_proof=r'''附录 D 第15页完整原数学证明译文：给定
\[I_{\mathrm{and}}^{\prime(i)}(T)=I_{\mathrm{and}}^{(i)}(T)+\sum_{T'\subseteq T}(-1)^{|T|-|T'|}\epsilon_{T'}^{(i)},\]
原文把固定交互 \(I_{\mathrm{and}}^{(i)}(T)\) 视为常数，因此它与高斯噪声独立、方差为零，并得
\[\begin{aligned}\operatorname{Var}(I_{\mathrm{and}}^{\prime(i)}(T))
&=\operatorname{Var}\left(I_{\mathrm{and}}^{(i)}(T)+\sum_{T'\subseteq T}(-1)^{|T|-|T'|}\epsilon_{T'}^{(i)}\right)\\
&=\operatorname{Var}(I_{\mathrm{and}}^{(i)}(T))+\operatorname{Var}\left(\sum_{T'\subseteq T}(-1)^{|T|-|T'|}\epsilon_{T'}^{(i)}\right)\\
&=\operatorname{Var}\left(\sum_{T'\subseteq T}(-1)^{|T|-|T'|}\epsilon_{T'}^{(i)}\right).
\end{aligned}\]
每个 \(\epsilon_T^{(i)}\sim\mathcal N(0,\sigma^2)\) 在所有子集上独立同分布，因此
\[\operatorname{Var}(I_{\mathrm{and}}^{\prime(i)}(T))=\operatorname{Var}(\epsilon_{T'_1}^{(i)})+\cdots+\operatorname{Var}(\epsilon_{T'_{2^{|T|}}}^{(i)})=2^{|T|}\sigma^2.\]
这里 \(T'\subseteq T\) 共 \(2^{|T|}\) 个。原附录 D 标题提及 AND 和 OR，但正文只给上述 AND 细证；正文第7页的 OR 方差声明另条登记，不冒充作者已另写OR证明。
'''
proofs={'iclr2024-generalizable-and':and_proof,'iclr2024-generalizable-or':or_proof,
 'iclr2024-generalizable-andor':and_proof+'\n\n'+or_proof+r'''

附录 C(3) 全部合成步骤：用上述 AND 和 OR universal matching，作者得
\[v(x_T)=v_{\mathrm{and}}(x_T)+v_{\mathrm{or}}(x_T)=\sum_{S\subseteq T}I_{\mathrm{and}}(S\mid x_T)+\sum_{S\in\{S:S\cap T\ne\varnothing\}\cup\{\varnothing\}}I_{\mathrm{or}}(S\mid x_T),\]
从而主张 AND-OR universal matching。''','f11-and-variance':variance_proof}
proofs.update({
'f11-or-duality':r'''第3页正文与脚注5的完整未编号数学解释：作者说反转变量的掩码/未掩码状态，使OR可看作一种AND。AND以基线值 \(b_i\) 为掩码状态，原值 \(x_i\) 为存在状态；如果把 \(b_i\) 当作存在，把 \(x_i\) 当作掩码，用 \(v(b_T)\) 表示 \(v(x_{N\setminus T})\)，作者称Eq.(2)可按Eq.(1)同样的方式构造。这里保留两条原定义：
\[I_{\mathrm{and}}(S\mid x)=\sum_{T\subseteq S}(-1)^{|S|-|T|}v(x_T),\]
\[I_{\mathrm{or}}(S\mid x)=-\sum_{T\subseteq S}(-1)^{|S|-|T|}v(x_{N\setminus T}).\]
原脚注没有另写完整负号证明。根据定义的负号与空集例外由项目重写明确推导。''',
'f11-boolean-decomposition':r'''第4页 Challenge1 完整数学例的译文。给定 \(x=[x_1,x_2,x_3,x_4,x_5]^\top\)、\(x_i\in\{0,1\}\)，作者取
\[f(x)=x_1\wedge x_2\wedge x_3+x_2\wedge x_3+x_3\wedge x_4+x_4\vee x_5.\]
第一种分解为
\[v_{\mathrm{and}}(x)=x_1\wedge x_2\wedge x_3+x_2\wedge x_3+x_3\wedge x_4,\quad v_{\mathrm{or}}(x)=x_4\vee x_5.\]
于是作者列出一项OR \(I_{\mathrm{or}}(\{4,5\})\) 和三项AND \(I_{\mathrm{and}}(\{1,2,3\})\)、\(I_{\mathrm{and}}(\{2,3\})\)、\(I_{\mathrm{and}}(\{3,4\})\)。第二种分解完全用AND，令
\[\begin{aligned}v_{\mathrm{and}}(x)&=x_1\wedge x_2\wedge x_3+x_2\wedge x_3+x_3\wedge x_4+x_4\vee x_5\\
&=x_1\wedge x_2\wedge x_3+x_2\wedge x_3+x_3\wedge x_4+(x_4+x_5-x_4\wedge x_5),\\v_{\mathrm{or}}(x)&=0.\end{aligned}\]
原文据 \(x_i\in\{0,1\}\) 得此项共有六个AND primitives，并用它说明不同分解产生不同交互。随后说明实际DNN关系复杂，难以写显式DNN表达式或确定ground-truth分解；该例没有声称两个分解是不同全局最优解。''',
'f11-reparameterization':r'''第4页Section2.3与第6页多模型版本的全部未编号代数说明。作者要学习 \(v(x_T)=v_{\mathrm{and}}(x_T)+v_{\mathrm{or}}(x_T)\) 的合适分解，令
\[v_{\mathrm{and}}(x_T)=0.5v(x_T)+\gamma_T,\qquad v_{\mathrm{or}}(x_T)=0.5v(x_T)-\gamma_T.\]
作者据此把学习分解等价地写成学习参数 \(\{\gamma_T:T\subseteq N\}\)。第6页对每个模型 \(i\) 重述
\[v_{\mathrm{and}}^{(i)}(x_T)=0.5v^{(i)}(x_T)+\gamma_T^{(i)},\qquad v_{\mathrm{or}}^{(i)}(x_T)=0.5v^{(i)}(x_T)-\gamma_T^{(i)}.\]
这是作者给出的重参数式与等价解释，没有另一段隐藏的逆向证明；项目重写把逆参数和唯一性完整展开。''',
'f11-rowmax-penalty':r'''第6页Eq.(5)之后的完整未编号数学说明。作者定义
\[I_{\mathrm{and}}=[I_{\mathrm{and}}^{(1)},\ldots,I_{\mathrm{and}}^{(m)}]\in\mathbb R^{2^n\times m},\]
\[\operatorname{rowmax}(I_{\mathrm{and}})=[\|I_{\mathrm{and}}[1,:]\|_\infty,\ldots,\|I_{\mathrm{and}}[2^n,:]\|_\infty]^\top\in\mathbb R^{2^n}.\]
OR矩阵同样定义。每一子集行的operator返回m个模型中最显著的交互强度。与Eq.(4)不同，Eq.(5)每行只惩罚这一最显著强度。作者解释：若一个模型在该子集编码强交互，其余m−1个模型也可提取同一交互而不增加该行惩罚；l1目的使模型共享类似的稀疏集合。大多数子集上作者希望所有模型的交互接近零。这是损失函数的局部惩罚解释，不是优化必然找到泛化解的数学定理。''',
'f11-mask-complexity':r'''附录G第16–17页完整理论计数与范围说明译文。作者说：给定具有n个输入变量的样本，提取AND-OR交互的时间复杂度是 \(2^n\)，需要生成掩码样本用于模型推理。依据既有实验设置，变量数不太大：实际选择一部分输入变量，其余保持固定背景。作者报告三任务耗时：任务1是45.14秒，任务2是46.61秒，任务3是27.15秒，并指出等待模型推理可用于实际分析。

这一段唯一明确的数学计数是所有变量子集/掩码模式为 \(2^n\)。作者没有另给求和变换、优化迭代次数、每次模型推理代价的完整复杂度证明。项目证明和Lean仅验证掩码/查询的数量，不将它冒充为整个优化过程的运行时间界。'''
})
equation10=r'''\begin{aligned}
\mathrm{Loss}&=\min_{\{\gamma_{T_k}^{(1)},\gamma_{T_k}^{(2)}\}}(\|\operatorname{rowmax}(I_{\mathrm{and}})\|_1+\|\operatorname{rowmax}(I_{\mathrm{or}})\|_1)+\alpha(\|I_{\mathrm{and}}\|_1+\|I_{\mathrm{or}}\|_1)\\
&=\min_{\{\gamma_{T_k}^{(1)},\gamma_{T_k}^{(2)}\}}\sum_{T_k\subseteq N}\left|\max\left(\sum_{T\subseteq S}(-1)^{|S|-|T|}[0.5v^{(1)}(x_{T_k})+\gamma_{T_k}^{(1)}],\sum_{T\subseteq S}(-1)^{|S|-|T|}[0.5v^{(2)}(x_{T_k})+\gamma_{T_k}^{(2)}]\right)\right|\\
&\quad+\sum_{T_k\subseteq N}\left|\max\left(-\sum_{T\subseteq S}(-1)^{|S|-|T|}[0.5v^{(1)}(x_{N\setminus T_k})-\gamma_{T_k}^{(1)}],-\sum_{T\subseteq S}(-1)^{|S|-|T|}[0.5v^{(2)}(x_{N\setminus T_k})-\gamma_{T_k}^{(2)}]\right)\right|\\
&\quad+\alpha\sum_{T_k\subseteq N}\sum_{i=1}^2\left|\sum_{T\subseteq S}(-1)^{|S|-|T|}[0.5v^{(i)}(x_{T_k})+\gamma_{T_k}^{(i)}]\right|\\
&\quad+\alpha\sum_{T_k\subseteq N}\sum_{i=1}^2\left|-\sum_{T\subseteq S}(-1)^{|S|-|T|}[0.5v^{(i)}(x_{N\setminus T_k})-\gamma_{T_k}^{(i)}]\right|.
\end{aligned}'''
statements['f11-equation10']=equation10
proofs['f11-equation10']=r'''附录F第16页完整数学解释译文。作者取两个预训练模型 \(v^{(1)},v^{(2)}\) 与 \(N=\{1,2\}\) 的样本。对每模型按Eq.(1)得到四个AND交互，并组成
\[I_{\mathrm{and}}^{(i)}=[I_{\mathrm{and}}(T_1\mid x),I_{\mathrm{and}}(T_2\mid x),I_{\mathrm{and}}(T_3\mid x),I_{\mathrm{and}}(T_4\mid x)]^\top\in\mathbb R^{2^2},\]
\[I_{\mathrm{and}}=[I_{\mathrm{and}}^{(1)},I_{\mathrm{and}}^{(2)}]\in\mathbb R^{2^2\times2}.\]
OR矩阵作者称同样获得。作者随后把Eq.(6)损失展开成下面完整Eq.(10)，并说只需用梯度下降优化 \(\{\gamma_{T_k}^{(1)},\gamma_{T_k}^{(2)}\}\) 即可降低Eq.(6)损失。原式保留signed max、自由索引S、原输出索引Tk和min的位置；项目未替作者修这些原式。

\['''+equation10+r'''\]
反例 \((-3,2)\) 只反驳其中采用的行最大范数逐点展开；本记录没有证明两个优化问题的最小值不同。父min等式与未定义索引的严格意义单独标为未判定。'''
descriptions={
'f11-equation10':'作者在附录F用两个模型、两个变量形成四行交互矩阵，将Eq.(6)损失写为下列Eq.(10)，并说用梯度下降优化其中参数。这是保留的完整作者原数学式；问题判断另列。',
'f11-external-sparsity':'附录B逐项列出三项外引条件：(1) DNN输出对输入变量的高阶导数全部为零；(2) DNN对掩码样本表现良好，掩码越少置信度越高；(3) 置信度在掩码样本上不会显著下降。作者据Ren等(2024)主张少量显著交互可近似全部掩码输出。本篇没有该外引结果的原证明。',
'f11-objectives':r'原Eq.(4)的两向量各含全部 \(2^n\) 个交互。Eq.(5),(6)的矩阵每行对应同一子集、每列对应模型。\(\operatorname{rowmax}\) 定义为每行 \(\ell_\infty\) 范数，即最大绝对值；\(\|\cdot\|_1\) 明确为矩阵/向量所有元素绝对值之和。Eq.(6)有 \(\alpha\in[0,1]\)。这些是目标函数定义；作者关于提高泛化与避免捷径的解释没有给出训练保证的数学定理。',
'f11-procedure-example':r'附录L完整8步：1. 六token“A stitch in time saves nine”，每个变量取对应token嵌入；BERTBASE域为 \(\mathbb R^{768}\)，BERTLARGE为 \(\mathbb R^{1024}\)。2. 各输入基线取本模型特殊token的嵌入。3. 枚举全部 \(2^6=64\) 个掩码：\(T_0=\varnothing,T_1=\{6\},T_2=\{5\},T_3=\{5,6\},\ldots,T_{62}=\{1,2,3,4,5\},T_{63}=N\)。4. 各模型计算 \(v(x_{T_j})=\log\frac{p(y=y^{\mathrm{truth}}\mid x_{T_j})}{1-p(y=y^{\mathrm{truth}}\mid x_{T_j})}\)。5. 对各模型/掩码设 \(v_{\mathrm{and}}=0.5v+\gamma, v_{\mathrm{or}}=0.5v-\gamma\)。6. 对两模型均按 Eq.(1),(2)计算 \(I_{\mathrm{and}}(T_j\mid x)=\sum_{T\subseteq T_j}(-1)^{|T_j|-|T|}v_{\mathrm{and}}(x_T)\)、\(I_{\mathrm{or}}(T_j\mid x)=-\sum_{T\subseteq T_j}(-1)^{|T_j|-|T|}v_{\mathrm{or}}(x_{N\setminus T})\)。作者Step6把所有j含空集一并写，OR空集值仍要对照Section2.1的单列约定。7. 以Eq.(6)学习gamma并回第5步迭代到收敛。8. 最终各模型集合 \(\Omega^{(i)}=\{T_j\subseteq N:|I_{\mathrm{and/or}}^{(i)}(T_j\mid x)|>\tau^{(i)}\)。这是算法例，不是收敛或一般正确性证明。',
'f11-empirical':'正文Section3与附录E,H,I,J,K,M,N,O.1为数据集、图表和经验比较。N.1设两次初始化gamma~N(0,1)，报告BERTBASE AND/OR重叠10.90%/16.18%、BERTLARGE 17.84%/20.90%；没有数学证明这些是不同全局最优解。N.2删除学习误差后绘制所有掩码匹配误差。经验图不计为新的数学证明。',
'f11-background-selection':'附录E与O.2：从全样本变量选定t<n个变量形成N，未选变量保持输入状态。SST-2在语义token中选最多10个；SQuAD将词及其对应全部tokens整体掩码，选择10词；MNIST-3选8个前景3×3patch，零patch作为输入基线。文中背景/stopword缺乏交互是经验取舍，不等于已证明的零交互条件。'}
results=[]
proof_types={
 'f11-or-duality':'complete_author_footnote_explanation_transcription',
 'f11-boolean-decomposition':'complete_author_example_derivation_transcription',
 'f11-reparameterization':'complete_author_unnumbered_derivation_transcription',
 'f11-rowmax-penalty':'complete_author_unnumbered_explanation_transcription',
 'f11-equation10':'complete_author_unnumbered_derivation_transcription',
 'f11-mask-complexity':'complete_author_count_and_empirical_scope_transcription',
}
author_statements={
 'f11-and-mask-zero':r'作者在Section 2.1说明：若交互集合中一个变量已被掩码，表示这些变量共同作用的AND交互为零。',
 'f11-or-duality':r'正文与脚注5称：反转变量的掩码与未掩码状态，OR可看作特定AND交互。把原基线值当作变量存在，把原输入值当作掩码状态，即用 \(v(b_T)\) 表示 \(v(x_{N\setminus T})\)，可以按AND式构造OR。',
 'f11-external-sparsity':r'附录B据Ren等(2024)列出三项条件：(1) DNN输出对输入变量的高阶导数全部为零；(2) DNN对掩码样本表现良好，掩码越少置信度越高；(3) 置信度在掩码样本上不会显著下降。作者称在这些条件下，少量显著交互可以近似匹配全部掩码输出。',
 'iclr2024-generalizable-theorem1':r'Theorem 1称：所有AND交互之和精确匹配每个掩码样本的输出，少量显著AND交互进一步近似匹配这些输出。',
 'f11-theorem1-approx':r'Theorem 1中的近似部分称：显著AND交互集合很小，保留这些交互可以近似匹配每个掩码输出。',
 'iclr2024-generalizable-andor':r'Theorem 2称：每个掩码输入的模型输出，可以由该输入的AND和OR交互精确表示。作者在附录C分别给出两分量及其合成。',
 'iclr2024-generalizable-and':r'附录C(1)欲证：保留标签为T的输入上，AND分量的输出等于全部S⊆T的AND交互之和。',
 'iclr2024-generalizable-or':r'附录C(2)欲证：OR分量的输出等于空集基线与所有S∩T非空的OR交互之和。',
 'f11-proposition1':r'Proposition 1称：少量显著AND与OR交互，可以在所有掩码样本上近似表示DNN输出。',
 'f11-boolean-decomposition':r'作者给出五个二值变量的函数算例，同一函数可以分成三个AND项与一个OR项，也可以只分成六个AND项。',
 'f11-reparameterization':r'作者把AND和OR两分量重参数化为模型输出的一半加减每个掩码标签的参数，并称该重参数化与任意原分解等价。',
 'f11-rowmax-penalty':r'作者定义每行的rowmax为这一子集在各模型的交互构成的行向量之最大绝对值范数；Eq.(5)对每个子集只惩罚其中最显著的交互强度。',
 'f11-and-variance':r'正文Section 2.3.2称：模型输出受高斯噪声 \(\epsilon_T\sim\mathcal N(0,\sigma^2)\) 扰动时，AND交互的方差为下式，随阶数指数增加。附录D逐项计算该方差。',
 'f11-or-variance':r'正文接着称：类似地，OR交互的方差也为 \(2^{|T|}\sigma^2\)，因此交互的方差/不稳定性随阶数指数增加。',
 'f11-shapley':r'Theorem 3称：度量变量重要性的Shapley值，可以将每个AND交互在其成员中均分，再累加变量i所参与的这些份额。作者注明这一关系来自Harsanyi(1963)。',
 'f11-equation10':r'附录F中，作者对两个模型和两个变量组成四行交互矩阵，把Eq.(6)损失展开为下列完整Eq.(10)，并称用梯度下降优化这些参数即可降低损失。',
 'f11-mask-complexity':r'附录G原文数学主张：理论上，对含 \(n\) 个输入变量的样本，提取AND-OR交互的时间复杂度是 \(2^n\)，并需要生成掩码样本用于模型推理。',
 'f11-alpha-zero':r'附录I说明：当 \(\alpha=0\) 时，Eq.(6)退化为Eq.(5)。',
}
for e in inv['entries']:
 id=e['id'];refs=[]
 for loc in e['statement_locations']:refs.append({'source_id':src,'locations':[{'pdf_page':loc['pdf_page'],'role':'statement','label':e['original_label']}]})
 for loc in e['proof_ranges']:
  refs.append({'source_id':src,'locations':[{'pdf_page':n,'role':'proof','label':loc['section']} for n in range(loc['start_pdf_page'],loc['end_pdf_page']+1)]})
 tex=statements.get(id,'');original=author_statements.get(id,descriptions.get(id,e['classification_basis']))
 original_tex=statements['f11-theorem1-approx'] if id=='iclr2024-generalizable-theorem1' else '' if id=='f11-mask-complexity' else tex
 if original_tex:original+='\n\n\\['+original_tex+'\\]'
 if id=='f11-or-duality':
  original=author_statements[id]+r'''原Eq.(2)为
\[I_{\mathrm{or}}(S\mid x)=-\sum_{T\subseteq S}(-1)^{|S|-|T|}v(x_{N\setminus T}).\]'''
 if id=='f11-and-variance':
  original+=r'''

正文第7页与附录D第15页首段的另一原出现为：
\[\mathbb E_{\epsilon_T\sim\mathcal N(0,\sigma^2)}\left[I_{\mathrm{and}}^{\prime(i)}(T)-\mathbb E_{\forall S,\epsilon_S\sim\mathcal N(0,\sigma^2)}I_{\mathrm{and}}^{\prime(i)}(S)\right]^2=2^{|T|}\sigma^2.\]
'''
 r=dict(id=id,paper_id=PAPER,title=e['title'],kind=e['kind'],original_label=e['original_label'],inventory_ids=[id],source_refs=refs,
  statement_tex=tex,assumptions=[],definitions=[],original_statement_md=original,
  original_proof_md=proofs.get(id,'本篇没有独立展开该项原证明；外引、算法或经验条目按类型记录。' if not e['proof_ranges'] else '本项原数学论证的精确转录仍在整理；完整PDF页已提供。'),
  original_statement_source_type='formal_mathematical_transcription_with_project_translation' if tex or id in descriptions else 'source_scope_summary',
  original_proof_source_type=proof_types.get(id,'complete_author_mathematical_transcription_with_project_translation') if id in proofs else 'no_local_original_proof' if not e['proof_ranges'] else 'transcription_in_progress',
  original_statement_note='数学原式据正式PDF核对；中文是项目译文。原PDF版面保留。',original_proof_note='原数学推导与项目忠实修正证明分开；原错误等号仍保留。',
  source_transcription_status='complete_mathematical_transcription' if id in proofs else 'statement_transcribed' if tex or id in descriptions else 'in_progress',
  overview=e['classification_basis'],proof_steps=[],shared_proof_ids=[],symbol_ids=[],notation_map=[],proof_target=e['proof_target'],
  rewrite_status='not_started' if e['proof_target'] else 'not_applicable',alignment_status='source_checked',user_review_status='pending',
  lean={'status':'not_formalized','declarations':[],'evidence_role':'none'},related_issue_ids=[])
 if id=='f11-mask-complexity':r['original_statement_note']+=' 项目范围说明：中文证明和Lean只核验掩码/查询数量；不把它冒充作者整个运行时间主张的证明。'
 if id=='f11-and-variance':r['original_statement_note']+=' 项目核对说明：原期望式的内层用了S而非固定T；它与后续Var推导分别保存，问题见关联记录。'
 if id=='f11-or-duality':r['original_statement_note']+=' 项目核对说明：脚注没有单独展开负号证明；项目按原Eq.(2)明确负号与非空范围。'
 results.append(r)
base={r['id']:r for r in results};issues=[];shared=[];fragment_inputs=[]
for folder in (P.parent/'cvpr2023',P.parent/'iclr2024-sparse'):
 for path in sorted(set(folder.glob('staging/*generalizable*.json'))|set(folder.glob('generalizable-*-results.json'))):
  value=json.loads(path.read_text());rows=value.get('results',[]) if isinstance(value,dict) else value
  if not isinstance(rows,list):continue
  for row in rows:
   if row.get('paper_id',PAPER)!=PAPER:continue
   id=row['id'];previous=base.get(id,{})
   merged=copy.deepcopy(previous);merged.update(row)
   for key in ('original_statement_md','original_statement_source_type','original_statement_note','original_proof_note','source_transcription_status'):
    if key in previous:merged[key]=previous[key]
   # Source mathematics is independently organized; short route summaries from
   # a proof fragment cannot replace a complete author transcription.
   if id in proofs:merged['original_proof_md']=proofs[id];merged['original_proof_source_type']=proof_types.get(id,'complete_author_mathematical_transcription_with_project_translation')
   base[id]=merged
  if isinstance(value,dict):issues+=value.get('issues',[]);shared+=value.get('shared_proofs',[])
  fragment_inputs.append(str(path.relative_to(ROOT)))
symbols=json.loads((P/'symbols.json').read_text())['symbols']
out=dict(schema_version='3.0',paper_id=PAPER,inventory_path=str((P/'inventory.json').relative_to(ROOT)),results=list(base.values()),shared_proofs=shared,issues=issues,symbols=symbols,fragment_inputs=fragment_inputs)
(P/'content.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'results':len(base),'fragments':fragment_inputs},ensure_ascii=False))
