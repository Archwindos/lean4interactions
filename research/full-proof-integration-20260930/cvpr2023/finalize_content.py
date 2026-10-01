"""Idempotent finishing pass: readable independent proofs and current audit references."""
from pathlib import Path
import hashlib
import json

ROOT=Path.cwd()
BASE=ROOT/'research/full-proof-integration-20260930/cvpr2023'
path=BASE/'content.json'
data=json.loads(path.read_text())
EXAMPLE=r'令 $N=\{1,2\}$，$g(\varnothing)=7$、$g(\{1\})=8$、$g(\{2\})=9$、$g(\{1,2\})=13$。于是 $w_\varnothing=7$、$w_{\{1\}}=1$、$w_{\{2\}}=2$、$w_{\{1,2\}}=3$。'
overview={
'cvpr2023-reconstruction':'展开交互并交换有限双和。除当前保留集合本身以外，每个输出的系数都由正负子集配对消去。',
'cvpr2023-uniqueness':'空掩码固定常数项；每个较大集合的等式，在减去已固定的真子集系数后，唯一确定当前系数。',
'cvpr2023-linearity':'在每个子集输出处代入两模型之和，再把有限交替和按加法分开。',
'cvpr2023-dummy':'原量词包括空环境，单变量模型满足加法前提却有非零单变量交互，直接反驳原命题。',
'cvpr2023-symmetry':'把含新变量和不含新变量的子集配对，再逐项使用两个变量在相同环境下的等效输出。',
'cvpr2023-anonymity':'变量重标记给出子集的一一对应，保留基数、符号和对应输出，因此交互值保持相等。',
'cvpr2023-recursive':'按新增变量是否出现拆分交互和，两组的差正是“变量在场”条件游戏的交互减去原交互。',
'cvpr2023-interaction-distribution':'未包含目标模式时输出全零；恰好目标模式时留下一个系数；严格包含时剩余变量使符号配对消去。',
'cvpr2023-marginal-decomposition':'重构每个差分输出，再交换有限求和。差分变量没有全部出现的交互被消去，只留下包含全部差分变量的项。',
'cvpr2023-shapley':'将经典边际定义中的每个差分展开为交互和。有限阶乘卷积算出每项的总权重，得到对模式内变量的均分。',
'cvpr2023-shapley-interaction':'把目标集合视为一个整体差分，并对外部变量按原阶乘权重平均；同一有限权重和给出交互系数。',
'cvpr2023-shapley-taylor':'低于截断阶数的目标保留原交互，高于阶数的目标为零；最高阶目标的有限权重和给出二项系数倒数。',
'cvpr2023-scm-subset-sum':'AND触发就是“模式包含于保留集合”的指示。把它代入线性根的有限和，得到被激活模式的系数和。',
'cvpr2023-baseline-faithfulness':'每个基线重新定义掩码输出并重算全部交互，完整重构的平方残差逐项为零。原句涉及截断损失的额外解释另列反例。',
'cvpr2023-aog-regrouping':'父模式的变量集合是所有孩子变量集合的并集。有限个孩子的触发乘积等于父触发，故共享子节点的重组保留根输出。',
'cvpr2023-addmul-coefficients':'先从实际零基线坐标掩码证明每个乘积项是纯AND响应，再按交互线性性合并；系数由原样本中的乘积决定。'}
bodies={
'cvpr-recon-main':r'对固定 $S$ 展开 $w_A$。每对 $L\subseteq A\subseteq S$ 只出现一次，交换有限求和不改变项。固定 $L$ 后，用 $B=A\setminus L\subseteq S\setminus L$ 给出一一对应，且 $|A|-|L|=|B|$。若 $L\ne S$，任选 $i\in S\setminus L$，把 $B$ 按是否含 $i$ 配对，符号相反，内和为零；若 $L=S$，只有 $B=\varnothing$，内和为一。因此只留下 $g(S)$。',
'cvpr-unique-induction':r'基例 $S=\varnothing$ 给出 $d_\varnothing=g(\varnothing)=w_\varnothing$。强归纳假设是：对所有 $A\subseteq N$ 且 $|A|<|S|$，都有 $d_A=w_A$。每个真子集都满足这个范围。在 $S$ 上分别应用假设的重构与已证重构，减去相同的真子集项，得到 $d_S=w_S$。任意 $S$ 均成立，因此系数逐项唯一。',
'cvpr-unique-empty':EXAMPLE+r' 空集等式固定 $d_\varnothing=7$，两个单变量等式固定 $d_{\{1\}}=1$、$d_{\{2\}}=2$，再用完整输入等式固定 $d_{\{1,2\}}=3$。若只知道 $g(N)=13$，把全部系数13放在空集或放在 $N$ 都满足这一个等式，因此不能省略其他掩码。',
'linearity-pointwise':r'设 $g_v(U)=g_t(U)+g_u(U)$ 对全部 $U\subseteq N$ 成立。固定 $A$ 后，每个 $U\subseteq A$ 都可代入该前提。原证明在交替和内把输出写成固定的 $x_A$；修正版在每一项使用对应的 $x_U$，原命题保持不变。',
'linearity-distribute':r'对每个 $U\subseteq A$，用乘法分配律把交替系数乘以输出之和拆成两项，再用有限求和的加法分配律拆成两和。这两和分别就是 $I_{g_t}(A)$ 和 $I_{g_u}(A)$。',
'linearity-empty':r'$A=\varnothing$ 时，结论是三个输出基线满足 $b_v=b_t+b_u$，不需要任何一个为零。例如常数模型 $t(x)=2$ 和 $u(x)=5$ 相加为 $v(x)=7$，空集交互为7，非空交互都为零。',
'symm-split':r'设 $i\notin S$、$j\notin S$。$S\cup\{i\}$ 的子集唯一写成 $U$ 或 $U\cup\{i\}$，其中 $U\subseteq S$。后一类的基数增加一，因此对应符号相反。每个 $U$ 都不含 $i,j$，所以原等效合作前提可逐项使用。',
'symm-substitute':r'每个括号的第一项可由前提换成 $g(U\cup\{j\})$，第二项不变。按含 $j$ 与不含 $j$ 的子集重新合并，就得到 $w_{S\cup\{j\}}$。当 $i=j$ 时等式仍成立，不需要增加二者不同的假设。',
'symm-empty':r'$S=\varnothing$ 时只需 $g(\{i\})=g(\{j\})$，共同减去 $g(\varnothing)$ 即可。例如 $g(\varnothing)=7$、$g(\{i\})=g(\{j\})=8$、$g(\{i,j\})=12$，两个单变量交互都为1；若 $i\ne j$，二阶交互为3。',
'anon-bijection':r'对变量置换 $\pi$，定义 $g^\pi(V)=g(\pi^{-1}V)$。映射 $U\mapsto\pi U$ 一一对应 $S$ 与 $\pi S$ 的子集，并保持基数；逆映射是 $V\mapsto\pi^{-1}V$。',
'anon-reindex':r'新交互的每个子集项对应原来的 $U$，指数满足 $|\pi S|-|\pi U|=|S|-|U|$，输出满足 $g^\pi(\pi U)=g(U)$。对应项逐一相等，所以总和相等。',
'anon-empty':EXAMPLE+r' 交换变量1和2时，单变量交互1和2交换位置，空集交互7和二阶交互3保持不变。置换把空集仍映到空集，因此输出基线不变。',
'rec-context':r'令 $g_i(U)=g(U\cup\{i\})$，即始终保留变量 $i$ 的条件游戏。原 $w_{S\mid i\,\mathrm{present}}$ 对应 $I_{g_i}(S)$。条件游戏的空集值是 $g(\{i\})$，不一定等于 $g(\varnothing)$。',
'rec-pair':r'设 $i\notin S$。含 $i$ 的子集 $U\cup\{i\}$ 的指数为 $|S|+1-(|U|+1)=|S|-|U|$；不含 $i$ 的子集 $U$ 多一个负号。两类合并成 $g_i(U)-g(U)$，再由线性性分成两项。',
'rec-empty':EXAMPLE+r' 当 $S=\{2\}$、$i=1$ 时，条件交互为 $13-8=5$，原交互为 $9-7=2$，相减得到二阶交互3。若 $S=\varnothing$，公式给 $w_{\{i\}}=g(\{i\})-g(\varnothing)$，不要求它为零。',
'dist-outside':r'若 $T\not\subseteq S$，任意 $U\subseteq S$ 都不可能包含 $T$，故 $u_T(U)=0$，每个交互项为零。此情形同时覆盖 $S$ 是 $T$ 的真子集和二者不可比的情况，补齐原证明漏掉的不可比集合。',
'dist-equal':r'若 $S=T$，只有 $U=T$ 这一项输出为 $c$，符号为1，其余真子集输出全为零。$T=\varnothing$ 时也只有空集项 $c$。',
'dist-superset':r'若 $T\subsetneq S$，只有包含 $T$ 的 $U$ 可能贡献。令 $B=U\setminus T\subseteq S\setminus T$，这是双射，指数为 $|S\setminus T|-|B|$。差集非空，选其中一个变量，再把含它与不含它的 $B$ 配对，符号相反，全部消去。',
'dist-example':r'若 $T=\varnothing$，$u_T$ 是常数 $c$，只有空集交互为 $c$。若 $N=\{1,2\}$、$T=\{1\}$、$c=3$，则 $g(\varnothing)=0$、$g(\{1\})=3$、$g(\{2\})=0$、$g(N)=3$，对应交互为0、3、0、0。原文遗漏的不可比集合 $S=\{2\}$ 已由第一情形处理。',
'marg-expand':r'固定差分变量集合 $T$ 与环境集合 $S$，要求 $T\cap S=\varnothing$。对每个 $L\subseteq T$ 重构 $g(L\cup S)$。每个 $K\subseteq L\cup S$ 唯一写成 $A\cup U$，其中 $A=K\cap L\subseteq L$、$U=K\cap S\subseteq S$。因为两总体不相交，这个表示不重复计数。',
'marg-cancel':r'按 $U$ 再按 $A$ 分组。固定 $A\subseteq T$，外层 $L$ 唯一写成 $A\cup B$，其中 $B\subseteq T\setminus A$，符号为 $(-1)^{|T|-|A|-|B|}$。若 $A\ne T$，从差集选一个变量把 $B$ 配对消去；若 $A=T$，只有空集 $B$，系数为1。因此每个 $U$ 只留下 $w_{T\cup U}$。',
'marg-empty':EXAMPLE+r' 当 $T=\{1\}$、$S=\{2\}$，差分为 $13-9=4$，右侧 $w_{\{1\}}+w_{\{1,2\}}=1+3=4$。$T=\varnothing$ 时左侧为 $g(S)$，右侧为重构和；$S=\varnothing$ 时两侧都是 $w_T$。',
'shapley-definition':r'取 $i\in N$，记 $n=|N|\ge1$。经典Shapley值对每个环境 $S\subseteq N\setminus\{i\}$ 的边际 $g(S\cup\{i\})-g(S)=\Delta_{\{i\}}g(S)$，按阶乘权重 $|S|!(n-|S|-1)!/n!$ 加权求和。',
'factorial-lemma':r'对任意有限集合 $R$、非负整数 $a,b$，记 $m=|R|$，$F_R(a,b)=\sum_{A\subseteq R}(a+|A|)!(b+m-|A|)!$。对 $R$ 作插入归纳，并加强归纳命题为对所有 $a,b$ 成立。$R=\varnothing$ 时两边都是 $a!b!$。插入新变量 $i\notin R$ 后，按 $A$ 是否含 $i$ 分组得到 $F_{R\cup\{i\}}(a,b)=F_R(a,b+1)+F_R(a+1,b)$。归纳假设给出的两项有共同分母 $(a+b+2)!$ 和共同大阶乘 $(a+b+m+2)!$，小阶乘相加为 $a!(b+1)!+(a+1)!b!=a!b!(a+b+2)$。约去正数 $a+b+2$ 得插入后的公式。全部阶乘为正，除法合法；论证包括 $a=0$、$b=0$、$m=0$。',
'factorial-coefficient':r'取正整数 $k$、有限环境集合 $E$ 及 $L\subseteq E$。记 $m=|E|$、$l=|L|$、$R=E\setminus L$。每个包含 $L$ 的 $S\subseteq E$ 唯一写成 $L\cup A$，其中 $A\subseteq R$，且 $|S|=l+|A|$、$|R|=m-l$。将上一引理用于 $a=l$、$b=k-1$；利用 $k(k-1)!=k!$ 并约去大阶乘 $(m+k)!$，得到下式，包括 $L=\varnothing$ 和 $L=E$。',
'factorial-transform':r'若 $T\cap E=\varnothing$，边际分解给 $\Delta_Tg(S)=\sum_{U\subseteq S}w_{T\cup U}$。每对 $U\subseteq S\subseteq E$ 恰好出现一次，交换有限双和。固定 $U$ 后，所有包含它的环境的权重之和由上一引理给出，所以每个 $w_{T\cup U}$ 得到下式中的精确系数。',
'shapley-specialize':r'在加权差分恒等式中取 $T=\{i\}$、$E=N\setminus\{i\}$、$k=1$，于是 $m=n-1$，左侧权重恰好是经典Shapley阶乘权重。右侧系数为 $\binom{|U|+1}{1}^{-1}=1/(|U|+1)$，得到原结论。差分集合与环境不相交，且 $k>0$，满足引理的全部前提。',
'shapley-empty-example':EXAMPLE+r' 因此 $\phi_g(1)=1+3/2=5/2$、$\phi_g(2)=2+3/2=7/2$，总和为 $6=g(N)-b$。环境 $U$ 可以为空，但分配的是非空交互 $\{i\}$；输出基线 $b$ 不分配给变量。若 $N=\{i\}$，唯一环境为空，公式给 $\phi_g(i)=g(\{i\})-b$。',
'sii-definition':r'记 $t=|T|$、$E=N\setminus T$、$m=n-t=|E|$。SII对整体目标 $T$ 的差分使用权重 $|S|!(m-|S|)!/(m+1)!$，不是分别对 $T$ 中的变量分配。原集合范围包括 $T=\varnothing$ 和 $T=N$。',
'sii-specialize':r'$T\cap E=\varnothing$。在加权差分恒等式取 $k=1$，左侧权重逐项等于原定义，右侧系数为 $1/(|U|+1)$，得原结论。$T=N$ 时环境为空，唯一项是 $w_N$；$T=\varnothing$ 时左侧是按该权重平均的原输出，右侧包括空交互 $b$。',
'sii-example':EXAMPLE+r' 当 $T=N$，SII为 $w_N=3$；当 $T=\{1\}$，它等于 $\phi_g(1)=5/2$。当 $T=\varnothing$，阶乘定义给 $(7/3)+(8/6)+(9/6)+(13/3)=19/2$；交互形式给 $7+1/2+2/2+3/3=19/2$，两侧相等。',
'sti-low':r'在正整数阶数 $k$ 的定义域内，若 $|T|<k$，环境空集上的差分按定义就是 $w_T$；$T=\varnothing$ 时值为 $b$。若 $|T|>k$，定义直接给零。这两个分支不除以 $n$，也不需要 $n\ge k$。',
'sti-top-weight':r'若 $|T|=k$，由于 $k>0$、$T\subseteq N$，有 $n\ge k\ge1$，除以 $n$ 合法。设 $E=N\setminus T$、$m=n-k$。对 $S\subseteq E$，记 $s=|S|\le m\le n-1$。二项系数的阶乘式给 $\frac{k}{n}\binom{n-1}{s}^{-1}=\frac{k\,s!(n-1-s)!}{n!}=\frac{k\,s!(m+k-1-s)!}{(m+k)!}$，恰好是加权差分引理的权重。$S=\varnothing$ 也在范围内。',
'sti-top-finish':r'差分变量 $T$ 与环境 $E$ 不相交，且 $k>0$，所以一般加权差分引理给出 $\binom{|U|+k}{k}^{-1}$ 的系数。与低于阶数、高于阶数的两个定义分支合并，得到完整三分支结论。',
'sti-example':EXAMPLE+r' 当 $k=1$，空目标值为7，两单变量目标分别为 $5/2$、$7/2$，二变量目标高于 $k$，值为零。当 $k=2$，四个目标的值为7、1、2、3，总和13。若 $N=\varnothing$ 而 $k\ge1$，仅有低阶空目标，值为 $b$。正阶数是当前定义域解释；原文仅写第 $k$ 阶，未显式写出不等式。',
'scm-trigger':r'固定保留集合 $S$，令 $X_i=\mathbf1_{i\in S}$。若 $A\subseteq S$，乘积中每个因子为1；否则至少一个因子为0。因此 $C_A(x_S)=\prod_{i\in A}X_i=\mathbf1_{A\subseteq S}$。空积为1，所以空模式始终触发。',
'scm-sum':r'将触发等式代入任意有限保留模式族 $\Omega$ 的SCM线性根，不包含于 $S$ 的项为零，其余项保留。因此输出是 $\sum_{A\in\Omega,\,A\subseteq S}w_A$。不要求 $\Omega$ 含全部模式；当 $\Omega=\mathcal P(N)$ 时，该和由重构等于 $g(S)$。',
'base-rereconstruct':r'对任意输入基线 $r$，以它定义全部 $x_S^{(r)}$ 及 $g_r(S)=v(x_S^{(r)})$，再重算 $I_{g_r}$。有限重构给每个 $S$ 的精确输出。换基线后必须重算集合函数和全部交互；这些系数一般会改变。',
'base-unfaith':r'不删模式时，每个残差 $g_r(S)-\sum_{A\subseteq S}I_{g_r}(A)$ 都为零，平方为零，有限和仍为零。任何两个基线各自适用该结论。截断到 $\Omega$ 后，残差不再由此定理保证为零。',
'base-truncated-counterexample':r'原句“just affects $\|w_\Omega\|_1$”若解释为截断损失不随基线变，则不成立。取单变量模型 $v(z)=z$、原输入 $x=1$、输入基线 $r$，只保留 $\Omega=\{\varnothing\}$。完整交互为 $w_\varnothing=r$、$w_{\{1\}}=1-r$，截断损失为 $[r-r]^2+[1-r]^2=(1-r)^2$，随 $r$ 改变。完整交互损失始终为零；原句中的完整重构子断言已证，但不能据此将截断解释算作整体通过。',
'aog-union':r'对有限变量集合 $A,B$ 及保留集合 $T$，$A\cup B\subseteq T$ 当且仅当 $A\subseteq T$ 且 $B\subseteq T$。因此 $C_{A\cup B}(x_T)=C_A(x_T)C_B(x_T)$，即使 $A,B$ 重叠也成立，因为触发值为0或1。',
'aog-tree':r'令有限孩子族为 $\mathcal C$，孩子 $c$ 所包含的原变量集合为 $V_c$，父模式为 $A=\bigcup_{c\in\mathcal C}V_c$。对孩子族作插入归纳：空孩子族的并集为空、触发与空积都为1；加入一个孩子后，由二集合并集等式，把父触发拆成该孩子触发乘以其余孩子触发，再应用归纳假设。因此 $C_A(x_T)=\prod_{c\in\mathcal C}C_{V_c}(x_T)$。孩子变量允许重叠，且同一孩子可被多个父模式共享。对每个原模式采用这样的分组，乘积等于原触发；保持原系数 $w_A$ 并逐项累加，根输出相同。',
'aog-empty':r'例如共享节点 $\beta=\{5,6\}$ 把模式 $\{4,5,6\}$ 写成孩子 $\{4\}$ 与 $\beta$。保留 $T=\{4,5\}$ 时两种表示都不触发；保留 $T=\{4,5,6\}$ 时都触发。空模式的触发与空孩子积都为1。这里只证明等价重组；原MDL贪心算法的最优性属于独立问题。',
'addmul-binary':r'原坐标 $x_i\in\{0,1\}$，输入基线为零。对一个项 $c_A\prod_{i\in A}x_i$，若 $A\subseteq S$，掩码保留全部因子；否则有某个因子被置零。因此该项在实际掩码 $x_S$ 上等于 $c_A\bigl(\prod_{i\in A}x_i\bigr)\mathbf1_{A\subseteq S}$。样本中任一因子为零使该项系数为零；空项的空积为1。相同变量集合的原项先合并系数。',
'addmul-transform':r'记不同变量集合构成有限族 $\mathcal P$，且 $v(z)=\sum_{A\in\mathcal P}c_A\prod_{i\in A}z_i$。上一坐标掩码等式把实际 $g(S)=v(x_S)$ 转成纯AND函数之和。每个纯AND响应的交互只在自身集合 $A$ 非零；有限和的线性性说明固定 $B$ 只收到 $A=B$ 的项。因此 $I_g(B)=c_B\prod_{i\in B}x_i$（若 $B\in\mathcal P$），否则为零。',
'addmul-examples':r'补充第14页的模型为 $v(x)=3x_1-2x_2x_3-x_3x_4x_5+5x_4x_6$。在 $x=(1,1,1,1,1,1)$，非零交互逐一为 $w_{\{1\}}=3$、$w_{\{2,3\}}=-2$、$w_{\{3,4,5\}}=-1$、$w_{\{4,6\}}=5$。在 $x=(1,1,0,1,1,1)$，只剩 $w_{\{1\}}=3$ 和 $w_{\{4,6\}}=5$。完整输出分别为5和8；两例空掩码输出及空交互均为零。这是原加乘响应的精确系数说明。'}
step_names={
'cvpr-recon-context':['FullCvpr.reconstruction'], 'cvpr-recon-main':['Harsanyi.reconstruction'], 'cvpr-recon-empty':['Harsanyi.interaction_empty'],
'cvpr-unique-quantifiers':['FullCvpr.uniqueness'], 'cvpr-unique-induction':['Harsanyi.reconstruction_unique'],
'linearity-pointwise':['FullCvpr.linearity'], 'linearity-distribute':['Harsanyi.interaction_add'], 'linearity-empty':['Harsanyi.interaction_empty'],
'dummy-counterexample':['FullCvpr.dummy_statement_counterexample'],
'symm-split':['Harsanyi.interaction_insert'], 'symm-substitute':['Harsanyi.interaction_symmetry'], 'symm-empty':['Harsanyi.interaction_singleton'],
'anon-bijection':['Harsanyi.interaction_relabel'], 'anon-reindex':['FullCvpr.anonymity'], 'anon-empty':['Harsanyi.interaction_empty'],
'rec-context':['Harsanyi.interaction_context_difference'], 'rec-pair':['FullCvpr.recursive'], 'rec-empty':['Harsanyi.interaction_singleton'],
'dist-outside':['Harsanyi.interaction_unanimity'], 'dist-equal':['Harsanyi.interaction_unanimity'], 'dist-superset':['FullCvpr.interaction_distribution'],
'marg-expand':['Harsanyi.reconstruct_union_disjoint'], 'marg-cancel':['Harsanyi.higherMarginal_eq_sum_interaction'], 'marg-empty':['Harsanyi.higherMarginal_eq_sum_interaction'],
'shapley-definition':['Harsanyi.factorialShapley'], 'factorial-lemma':['Harsanyi.factorial_powerset_sum'], 'factorial-coefficient':['Harsanyi.sum_supersets_eq_sum_complement','Harsanyi.factorialWeight_superset_sum','Harsanyi.factorial_ratio_eq_choose_inv'], 'factorial-transform':['Harsanyi.weighted_higherMarginal_eq'], 'shapley-specialize':['Harsanyi.factorialShapley_eq_dividends','FullCvpr.shapley'],
'sii-definition':['Harsanyi.factorialShapleyInteraction'], 'sii-specialize':['Harsanyi.factorialShapleyInteraction_eq_dividends','FullCvpr.shapley_interaction'],
'sti-low':['Harsanyi.shapleyTaylor'], 'sti-top-weight':['Harsanyi.factorialWeight_eq_inv_choose'], 'sti-top-finish':['Harsanyi.shapleyTaylor_eq_dividends','FullCvpr.shapley_taylor'],
'scm-trigger':['FullCvpr.andTrigger_product'], 'scm-sum':['FullCvpr.causalOutput_eq_sum_subset','FullCvpr.causalOutput_full'],
'base-rereconstruct':['FullCvpr.reconstruction'], 'base-unfaith':['FullCvpr.complete_unfaithfulness_zero'], 'base-truncated-counterexample':['FullCvpr.baseline_truncated_loss_counterexample'],
'aog-union':['FullCvpr.andTrigger_union'], 'aog-tree':['FullCvpr.andTrigger_children','FullCvpr.causalOutput_regrouped'], 'aog-empty':['FullCvpr.andTrigger_children'],
'addmul-binary':['FullCvpr.masked_monomial'], 'addmul-transform':['FullCvpr.interaction_finite_sum','FullCvpr.addmul_coordinate_adapter'],
'dummy-nonempty-exact-domain':['Harsanyi.interaction_additive_dummy_nonempty'], 'dummy-nonempty-pair':['Harsanyi.interaction_additive_dummy_nonempty']}
generic=r'固定有限总体 $N$。集合函数 $g:\mathcal P(N)\to\mathbb R$ 的输出基线为 $b=g(\varnothing)$，交互为 $I_g(A)=\sum_{U\subseteq A}(-1)^{|A|-|U|}g(U)$。记 $w_A=I_g(A)$。所有子集和包括空集，且 $w_\varnothing=b$。差分为 $\Delta_Tg(S)=\sum_{L\subseteq T}(-1)^{|T|-|L|}g(L\cup S)$。原始输出不要求零基线；中心化函数 $g_0=g-b$ 仅使空交互变为零。'
assumptions={
'shared-harsanyi-linearity':[r'$g,h:\mathcal P(N)\to\mathbb R$；$A\subseteq N$。'],
'shared-harsanyi-symmetry':[r'$S\subseteq N$，$i,j\in N\setminus S$；对每个 $U\subseteq S$，$g(U\cup\{i\})=g(U\cup\{j\})$。'],
'shared-harsanyi-anonymity':[r'$\pi:N\to N$ 是置换；$g^\pi(V)=g(\pi^{-1}V)$；$S\subseteq N$。'],
'shared-harsanyi-recursive':[r'$i\in N\setminus S$；$g_i(U)=g(U\cup\{i\})$。'],
'shared-harsanyi-interaction-distribution':[r'$T,S\subseteq N$，$c\in\mathbb R$；$u_T(U)=c\mathbf1_{T\subseteq U}$。空 $T$ 与不可比集合均包括。'],
'shared-harsanyi-marginal-decomposition':[r'$T,S\subseteq N$；$T\cap S=\varnothing$。'],
'shared-harsanyi-factorial-convolution':[r'$T,E\subseteq N$，$T\cap E=\varnothing$；$k\in\mathbb N$、$k>0$；$m=|E|$。'],
'shared-harsanyi-shapley-dividend':[r'$i\in N$；经典阶乘权重边际定义 $\phi_g$；$n=|N|\ge1$。'],
'shared-harsanyi-shapley-interaction-dividend':[r'$T\subseteq N$；原SII阶乘权重定义，环境为 $N\setminus T$；包括空目标。'],
'shared-harsanyi-shapley-taylor-dividend':[r'$T\subseteq N$；正整数阶数 $k>0$ 的原三分支STI定义。原文未显式写 $k>0$，此为正阶定义域解释，$k=0$ 不在当前核验范围。'],
'shared-harsanyi-dummy-nonempty':[r'$i\in N\setminus S$；$S\ne\varnothing$；$c\in\mathbb R$，对每个 $U\subseteq S$ 有 $g(U\cup\{i\})=g(U)+c$。']}

for obj in data['results']+data['shared_proofs']:
    if obj['id'] in overview: obj['overview']=overview[obj['id']]
    if obj['id'] in assumptions:
        obj['assumptions']=assumptions[obj['id']]
        obj['definitions']=[{'id':'finite-game','body_md':generic}]
    for s in obj.get('proof_steps',[]):
        if s['id'] in bodies: s['body_md']=bodies[s['id']]
        if s['id'] in ['factorial-coefficient','factorial-transform']:
            s['formula_tex']=s['formula_tex'].replace('M','E')
    if obj['id']=='shared-harsanyi-factorial-convolution':
        obj['statement_tex']=obj['statement_tex'].replace('M','E')
    if obj['id']=='proof-finite-mobius-reconstruction-v2':
        obj['overview']=r'每次插入新变量 $i$，把子集分成含 $i$ 与不含 $i$ 两类。含 $i$ 的交互等于插入差分的交互；对两类分别应用加强归纳假设，中间输出相消，留下当前输出。'
    if obj['id']=='shared-harsanyi-dummy-nonempty':
        obj['proof_steps'][0]['body_md']=r'此公共性质要求 $S\ne\varnothing$，与CVPR原量词不同，不能替代其错误命题。由 $i\notin S$ 及恒定边际 $g(U\cup\{i\})-g(U)=c$，含 $i$ 的交互等于 $S$ 上常数游戏 $c$ 的交互。'
        obj['proof_steps'][1]['body_md']=r'按含 $i$ 和不含 $i$ 的子集配对，指数差一，得到 $I_g(S\cup\{i\})=c\sum_{U\subseteq S}(-1)^{|S|-|U|}$。因为 $S$ 非空，取 $j\in S$ 再按是否含 $j$ 配对，符号相反，和为零。$S=\varnothing$ 时该和为 $c$，说明非空条件必要。'
        obj['proof_steps'][1]['justification']=r'不要求 $g(\varnothing)=0$；在上述前提下 $c=g(\{i\})-g(\varnothing)$。'

byid={r['id']:r for r in data['results']}
byid['cvpr2023-aog-regrouping']['statement_tex']=r'A=\bigcup_{c\in\mathcal C}V_c\ \Rightarrow\ C_A(x_T)=\prod_{c\in\mathcal C}C_{V_c}(x_T),\qquad\sum_{A\in\Omega}w_A\prod_{c\in\mathcal C_A}C_{V_c}(x_T)=\sum_{A\in\Omega}w_AC_A(x_T)'
byid['cvpr2023-aog-regrouping']['assumptions']=[r'每个父模式 $A$ 是有限孩子变量集合 $V_c$ 的并集；触发取 $\mathbf1_{A\subseteq T}$；保留原系数与线性根。允许共享孩子和重叠变量。']
byid['cvpr2023-aog-regrouping']['lean']['declarations']=['FullCvpr.andTrigger_children','FullCvpr.causalOutput_regrouped']
byid['cvpr2023-aog-regrouping']['lean']['scope']='arbitrary finite child family trigger product and exact preservation of the weighted linear root under correct variable-union grouping; does not assert MDL optimality'
byid['cvpr2023-aog-regrouping']['proof_steps'][1]['formula_tex']=r'C_{\bigcup_{c\in\mathcal C}V_c}(x_T)=\prod_{c\in\mathcal C}C_{V_c}(x_T).'
byid['cvpr2023-addmul-coefficients']['statement_tex']=r'v(z)=\sum_{A\in\mathcal P}c_A\prod_{i\in A}z_i,\quad r=0\ \Rightarrow\ I_{S\mapsto v(x_S)}(B)=\begin{cases}c_B\prod_{i\in B}x_i&B\in\mathcal P,\\0&B\notin\mathcal P.\end{cases}'
byid['cvpr2023-addmul-coefficients']['proof_steps'][1]['formula_tex']=r'I_g(B)=\begin{cases}c_B\prod_{i\in B}x_i&B\in\mathcal P,\\0&B\notin\mathcal P.\end{cases}'
byid['cvpr2023-addmul-coefficients']['lean']['declarations']=['FullCvpr.masked_monomial','FullCvpr.addmul_coordinate_adapter']
byid['cvpr2023-addmul-coefficients']['lean']['scope']='actual coordinate polynomial evaluated at zero-baseline coordinate masks, with interaction coefficients for every subset; applies to both original binary inputs and all listed source monomials'
byid['cvpr2023-scm-subset-sum']['lean']['declarations']=['FullCvpr.andTrigger_product','FullCvpr.causalOutput_eq_sum_subset','FullCvpr.causalOutput_full']
base=byid['cvpr2023-baseline-faithfulness']
base['rewrite_status']='blocked_by_source_issue'
base['mathematical_rewrite_core_status']='complete'
base['lean']['declarations']=['FullCvpr.complete_unfaithfulness_zero','FullCvpr.baseline_truncated_loss_counterexample']
base['lean']['scope']='full-vector reconstruction subclaim and exact truncated-loss counterexample; source compound clause is not validated as a whole'
base['alignment_status']='compound_claim_split_without_statement_change'
data['counts']={'proof_targets':16,'results_present':16,'rewrite_complete':14,'partial_result_with_source_issue':1,'statement_errors':1}

# The Generalizable fragment has source fields owned by the UI agent, which this pass never changes.
fragment_path=BASE/'generalizable-finite-results.json'
fragment=json.loads(fragment_path.read_text())
defs=r'固定 $N=\{1,\ldots,n\}$、模型 $v:\mathbb R^n\to\mathbb R$、样本 $x$ 和同一个输入基线 $r$。记 $g(A)=v(x_A)$，$b=g(\varnothing)$。二次掩码定义条件游戏 $g_T(A)=v((x_T)_A)=g(T\cap A)$。AND为 $I_g(S)=\sum_{L\subseteq S}(-1)^{|S|-|L|}g(L)$，另记 $w_A=I_g(A)$。非空OR为 $O_g^N(S)=-I_{g^c}(S)$，其中 $g^c(L)=g(N\setminus L)$；空OR单独规定 $O_g^N(\varnothing)=g(\varnothing)$。所有子集和包括空集，原始输出不要求零基线。涉及分量时分别以 $v_{and},v_{or}$ 定义对应游戏和条件游戏。'
component_defs=defs+r' 原第4、6页允许按掩码标签任意给定 $\gamma_A$，因此联合分解的最一般对象是 $g_{and}(A)=\tfrac12g(A)+\gamma_A$、$g_{or}(A)=\tfrac12g(A)-\gamma_A$，或任意满足 $g(A)=g_{and}(A)+g_{or}(A)$ 的两个集合函数。条件分量按标签定义为 $g_{and,T}(L)=g_{and}(T\cap L)$、$g_{or,T}(L)=g_{or}(T\cap L)$。原符号 $v_{and}(x_A),v_{or}(x_A)$ 在此表示这些掩码标签值；若两分量确实来自输入函数，才进一步解释为对向量的函数求值。允许 $x_i=r_i$，不要求不同标签产生不同输入，也不要求任意 $\gamma_A$ 延拓为输入空间上的单值函数。'
gen_bodies={
'f11-mask-comp':r'固定坐标 $i$：若 $i\in T\cap L$，两次掩码都保留 $x_i$；若 $i\notin L$，第二次给 $r_i$；若 $i\in L\setminus T$，第一次已经给 $r_i$，第二次保留的仍是 $r_i$。逐坐标相同，得 $(x_T)_L=x_{T\cap L}$。两次必须使用同一输入基线 $r$。',
'f11-mask-zero-pair':r'若 $S\not\subseteq T$，取 $i\in S\setminus T$。每个 $U\subseteq S\setminus\{i\}$ 满足 $T\cap(U\cup\{i\})=T\cap U$，故对应条件输出相同。交互中的两项符号相反，逐对消去，结果为零。不要求模型线性或 $g(\varnothing)=0$。',
'f11-mask-boundary':r'$S=\varnothing$ 始终包含于 $T$，因此消失命题不包括空交互；空交互为 $b$。$T=N$ 时不存在 $S\not\subseteq T$。$T=\varnothing$ 时，全部非空 $S$ 的条件交互为零。',
'f11-and-coeff-align':r'对 $S\subseteq T$，每个 $L\subseteq S$ 也有 $L\subseteq T$，故 $T\cap L=L$。因此标签条件游戏 $g_{and,T}(L)=g_{and}(T\cap L)$ 在所有求和项上等于 $g_{and}(L)$，逐项得到 $I_{g_{and,T}}(S)=I_{g_{and}}(S)$。若分量是输入函数，掩码合成 $(x_T)_L=x_L$ 给出同一关系。',
'f11-and-reconstruct':r'对任意集合函数 $g_{and,T}$ 应用完整有限重构，得到 $\sum_{S\subseteq T}I_{g_{and,T}}(S)=g_{and,T}(T)=g_{and}(T)$，因为 $T\cap T=T$。上一条对齐又给 $\sum_{S\subseteq T}I_{g_{and}}(S)$ 同值。两个和都包含空集项 $g_{and}(\varnothing)$；不增加零基线条件。',
'f11-and-empty':r'$T=\varnothing$ 时唯一求和项为 $S=\varnothing$，左右都是 $g_{and}(\varnothing)$。任意标签分量与实际输入函数分量都满足此边界。',
'f11-or-literal-game':r'固定 $T\subseteq N$，令 $h(L)=g_{or,T}(L)=g_{or}(T\cap L)$，保持原父式的条件掩码标签。于是 $h(N\setminus L)=g_{or}(T\setminus L)$。分量来自输入函数时，这才写成 $v_{or}((x_T)_{N\setminus L})=v_{or}(x_{T\setminus L})$；原第13页直接使用 $v_{or}(x_{N\setminus L})$ 一般不等。证明对任意标签函数成立，无需其能延拓为输入函数。',
'f11-or-filter':r'对每个 $S\subseteq N$，$S\cap T=\varnothing$ 当且仅当 $S\subseteq N\setminus T$。故相交子集族为 $\mathcal P(N)\setminus\mathcal P(N\setminus T)$，后者包含于前者；有限求和等于两个全族的和相减。空集在两个全族中都出现，始终不属于相交族。',
'f11-or-transform':r'令 $f(L)=-h(N\setminus L)$。对非空 $S$，有限和对整体负号的线性性给 $O_h^N(S)=I_f(S)$。相交族不含空集，故可逐项替换。两次重构给 $f(N)-f(N\setminus T)=-h(\varnothing)+h(T)$；这里由 $T\subseteq N$ 有 $N\setminus(N\setminus T)=T$。再用 $h(T)=g_{or}(T)$、$h(\varnothing)=g_{or}(\varnothing)$。',
'f11-or-baseline':r'空OR按定义单列 $O_h^N(\varnothing)=h(\varnothing)=g_{or}(\varnothing)$。加回此基线便重构 $g_{or}(T)$。$T=\varnothing$ 时相交族为空，只有基线；$T=N$ 时重构完整标签值。因此也涵盖原case1/2在空掩码时重合的边界。',
'f11-parent-decompose':r'原分解在每个掩码标签上满足 $g(U)=g_{and}(U)+g_{or}(U)$。特别是作者任意的 $\gamma_U$ 参数化，逐项相加立即抵消 $\gamma_U$。即使某个 $x_i=r_i$ 使两标签对应同一向量，两分量仍可作为集合函数使用；证明不另加标签值能延拓为输入函数的条件。',
'f11-parent-add':r'AND部分重构 $g_{and}(T)$，OR部分重构 $g_{or}(T)$；相加并使用原分解，得到 $g(T)=v(x_T)$。两个空项合计为 $g(\varnothing)$。全部系数仍由条件标签游戏 $g_{and,T},g_{or,T}$ 定义，输入函数分量版本是其特例。',
'f11-dual-definition':r'对 $S\ne\varnothing$，OR式的各项就是 $g^c$ 的AND变换，但整体有负号。数值一般互为相反数，绝对值相等。空OR另规定为 $g(\varnothing)$；负AND在空集为 $-g(N)$，一般不同，必须分开。',
'f11-dual-example':EXAMPLE+r' 补集游戏 $g^c$ 的两个单变量AND值为 $-4$、$-5$，二阶值为3；对应OR值为4、5、$-3$，空OR基线为7。反转AND的空值为13，不能用其负值 $-13$ 代替7。',
'f11-or-example':EXAMPLE+r' 固定原输入的OR系数是 $O_g^N(\{1\})=4$、$O_g^N(\{2\})=5$、$O_g^N(N)=-3$，空值7。对原父式的 $T=\{1\}$，应使用条件游戏 $h_T(L)=g(T\cap L)$，其四个输出依次为7、8、7、8，OR系数为1、0、0，空值7。相交求和使用 $\{1\}$ 与 $N$，所以条件式给 $7+1+0=8=g(T)$。固定原输入式也给 $7+4-3=8$，但逐项系数不同。$T=\varnothing$ 时仅基线7；$T=N$ 时两种游戏一致，得 $7+4+5-3=13$。',
'f11-shapley-component':r'原Theorem3的 $I_{and}(S\mid x)$ 来自模型 $v$ 自身的AND定义，不是任意学习分解中 $v_{and}$ 的系数。取 $g(A)=v(x_A)$、$i\in N$，即满足经典阶乘Shapley与共有证明的前提。',
'f11-shapley-reindex':r'环境 $U\subseteq N\setminus\{i\}$ 与含 $i$ 的交互集合一一对应：$S=U\cup\{i\}$，逆映射 $U=S\setminus\{i\}$，且 $|S|=|U|+1$。逐项换索引，便得到原分母 $|S|$。空集不含 $i$，不参与分配。',
'f11-count-bijection':r'每个 $i\in N$ 选择保留或基线。保留坐标的集合 $S$ 唯一表示该设置，反之每个 $S\subseteq N$ 给一个设置，所以 $n$ 个二值选择有 $2^n$ 个掩码设置，即 $|\mathcal P(N)|=2^n$。即使某个 $x_i=r_i$ 使不同设置产生相同向量，设置数仍为 $2^n$。',
'f11-count-queries':r'一次对每个设置查询模型的完整枚举有 $2^n$ 次调用；$m$ 个模型各枚举一次有 $m2^n$ 次。这是查询方案的计数，不能单独推出全部交互变换、训练或梯度优化的总运行时间。',
'f11-count-boundary':r'$n=0$ 时唯一空设置，数目为 $1=2^0$；$n=6$ 时为64个设置。原时间表为实验测量，不能由设置计数推出具体秒数。'}
step_names.update({
'f11-mask-comp':['Harsanyi.maskCoordinates_comp'], 'f11-mask-zero-pair':['Harsanyi.and_mask_interaction_zero','FullGeneralizable.and_mask_zero'], 'f11-mask-boundary':['Harsanyi.maskCoordinates_comp'],
'f11-dual-game':['Harsanyi.orInteraction'], 'f11-dual-definition':['Harsanyi.or_dual','FullGeneralizable.or_duality'],
'f11-exact-adapt':['FullGeneralizable.exact_and_reconstruction'],
'f11-and-coeff-align':['FullGeneralizable.label_and_coefficient_eq','FullGeneralizable.literal_and_coefficient_eq'], 'f11-and-reconstruct':['FullGeneralizable.label_and_reconstruction','FullGeneralizable.literal_and_reconstruction'], 'f11-and-empty':['Harsanyi.interaction_empty'],
'f11-or-literal-game':['FullGeneralizable.labelConditionalGame','Harsanyi.maskCoordinates_complement'], 'f11-or-filter':['Harsanyi.activated_subset_sum'], 'f11-or-transform':['Harsanyi.or_reconstruction','FullGeneralizable.label_or_nonempty_sum'], 'f11-or-baseline':['FullGeneralizable.label_or_reconstruction'],
'f11-parent-decompose':['FullGeneralizable.label_and_or_reconstruction'], 'f11-parent-add':['FullGeneralizable.literal_and_or_reconstruction','FullGeneralizable.label_and_or_reconstruction'],
'f11-boolean-truth':['FullGeneralizable.boolean_or_additive'], 'f11-boolean-expand':['FullGeneralizable.boolean_decomposition'], 'f11-boolean-support':['Harsanyi.orInteraction_unanimity','FullCvpr.addmul_coordinate_adapter'],
'f11-shapley-component':['FullGeneralizable.shapley'], 'f11-shapley-reindex':['Harsanyi.dividendAllocation_eq_insert_sum','Harsanyi.factorialShapley_eq_dividendAllocation','FullGeneralizable.shapley'],
'f11-count-bijection':['FullGeneralizable.mask_count'], 'f11-count-queries':['FullGeneralizable.mask_count']})
shared_byid={s['id']:s for s in data['shared_proofs']}
for r in fragment['results']:
    r['definitions']=[{'id':'f11-coordinate-objects','body_md':defs}]
    if r['id'] in ['iclr2024-generalizable-and','iclr2024-generalizable-or','iclr2024-generalizable-andor']:
        r['definitions']=[{'id':'f11-coordinate-and-label-objects','body_md':component_defs}]
        r['completion_scope']='complete arbitrary mask-label component statement, including every gamma assignment; actual input-function variant retained as a special case'
        r['lean']['scope']=r['completion_scope']
        r['assumptions']=[r'$g(U)=v(x_U)$；有限 $N$、$T\subseteq N$；AND/OR分量为任意集合函数，父定理要求对全部标签 $U$ 满足 $g(U)=g_{and}(U)+g_{or}(U)$。无需 $x_i\ne r_i$ 或分量延拓假设。']
        if r['id']=='iclr2024-generalizable-and':
            r['statement_tex']=r'g_{and}(T)=\sum_{S\subseteq T}I_{g_{and,T}}(S)=\sum_{S\subseteq T}I_{g_{and}}(S),\quad g_{and,T}(L)=g_{and}(T\cap L).'
            r['lean']['declarations']=['FullGeneralizable.literal_and_coefficient_eq','FullGeneralizable.literal_and_reconstruction','FullGeneralizable.label_and_coefficient_eq','FullGeneralizable.label_and_reconstruction']
        elif r['id']=='iclr2024-generalizable-or':
            r['statement_tex']=r'g_{or}(T)=O_{g_{or,T}}^N(\varnothing)+\sum_{\substack{S\subseteq N\\S\cap T\ne\varnothing}}O_{g_{or,T}}^N(S),\quad g_{or,T}(L)=g_{or}(T\cap L).'
            r['lean']['declarations']=['Harsanyi.activated_subset_sum','Harsanyi.or_reconstruction','FullGeneralizable.literal_or_reconstruction','FullGeneralizable.literal_or_nonempty_sum','FullGeneralizable.label_or_nonempty_sum','FullGeneralizable.label_or_reconstruction']
        else:
            r['statement_tex']=r'v(x_T)=\sum_{S\subseteq T}I_{g_{and,T}}(S)+O_{g_{or,T}}^N(\varnothing)+\sum_{\substack{S\subseteq N\\S\cap T\ne\varnothing}}O_{g_{or,T}}^N(S).'
            r['lean']['declarations']=['FullGeneralizable.literal_and_or_reconstruction','FullGeneralizable.label_and_or_reconstruction']
            r['overview']='任意掩码标签分量分别在条件标签游戏中精确重构，两个分量相加恢复原模型输出；标签碰撞不影响此有限恒等式。'
    if r['id']=='f11-shapley':
        shared_steps=shared_byid['shared-harsanyi-shapley-dividend']['proof_steps']
        r['proof_steps']=[r['proof_steps'][0]]+json.loads(json.dumps(shared_steps))+[r['proof_steps'][-1]]
        r['symbol_ids']=[x for x in r['symbol_ids'] if x!='sym-or-interaction']+['sym-shapley']
    for s in r['proof_steps']:
        if s['id'] in bodies: s['body_md']=bodies[s['id']]
        if s['id'] in gen_bodies: s['body_md']=gen_bodies[s['id']]
        if s['id']=='f11-and-reconstruct':s['formula_tex']=r'\sum_{S\subseteq T}I_{g_{and,T}}(S)=\sum_{S\subseteq T}I_{g_{and}}(S)=g_{and}(T).'
        if s['id']=='f11-or-transform':s['formula_tex']=r'\sum_{S\cap T\ne\varnothing}O_h^N(S)=h(T)-h(\varnothing)=g_{or}(T)-g_{or}(\varnothing).'
        if s['id']=='f11-parent-add':s['formula_tex']=r'v(x_T)=\sum_{S\subseteq T}I_{g_{and,T}}(S)+O_{g_{or,T}}^N(\varnothing)+\sum_{S\subseteq N:S\cap T\ne\varnothing}O_{g_{or,T}}^N(S).'
        if s['id'] in ['factorial-coefficient','factorial-transform']: s['formula_tex']=s['formula_tex'].replace('M','E')
    if r['id']=='f11-or-duality':
        r['source_comparison_note_md']=r'原footnote 5将反转后的量称为same AND；项目根据原Eq.(2)明确保留整体负号。原文未给一个独立的完整负号处理证明，来源类别不得写成作者已证明了此逐式对齐。'
    if r['id']=='iclr2024-generalizable-theorem1':
        r['proof_steps'][1:]=json.loads(json.dumps(byid['cvpr2023-reconstruction']['proof_steps'][1:]))
for s in fragment['shared_proofs']:
    s['definitions']=[{'id':'finite-or-game','body_md':generic+r' 非空OR定义为 $O_g^N(S)=-I_{g^c}(S)$，$g^c(L)=g(N\setminus L)$；空OR为 $g(\varnothing)$。'}]
    s['assumptions']=[r'$T\subseteq N$；$g:\mathcal P(N)\to\mathbb R$；非空OR取补集游戏的负AND变换，空OR单列原输出基线。']

# Fix original/canonical Beta mapping without silently correcting the original source.
symbols=json.loads((BASE/'symbols.json').read_text())
records=symbols.get('symbols',[]) if isinstance(symbols,dict) else symbols
for s in records:
    if s['id']=='sym-cvpr-beta':
        for m in s.get('paper_mappings',[]):
            m['original_definition_tex']=r'B(p,q)=\int_0^1x^{p-1}(1-x)^{1-q}\,dx'
            m['relationship']='conflict'
    if s['id']=='sym-cvpr-sti-order':
        s['assumptions']=[r'当前STI闭式核验采用正整数阶数 $k>0$ 的有效定义域解释；CVPR原文仅写k-th，未显式写不等式；k=0没有计入已核验范围。']
(BASE/'symbols.json').write_text(json.dumps(symbols,ensure_ascii=False,indent=2)+'\n')
data['symbols']=records

report=json.loads((BASE/'verification/report.json').read_text())
fresh=report['status']=='passed' and all(hashlib.sha256((ROOT/f['path']).read_bytes()).hexdigest()==f['sha256'] for f in report['source_files'])
if not fresh:
    raise RuntimeError('finite report is stale or failed; compile/audit frozen sources before finalizing')
decls={d['name']:d for d in report['declarations']}
all_objects=data['results']+data['shared_proofs']+fragment['results']+fragment['shared_proofs']
for obj in all_objects:
    ln=obj['lean']
    for name in ln['declarations']:
        if name not in decls: raise RuntimeError('missing audited declaration '+name)
    ln.update({'status':'verified','compiled':True,'axiom_audit':'passed','build_id':report['build_id'],'source_fingerprint':report['source_fingerprint'],'report_path':str((BASE/'verification/report.json').relative_to(ROOT)),'source_semantics_automatically_verified':False})
    first=decls[ln['declarations'][-1]]
    ln.update({'statement':first['signature'],'source_path':first['source_path'],'line':first['line']})
    if obj['id']=='cvpr2023-dummy':
        ln.update({'status':'counterexample_verified','label':'原命题不成立；反例声明已编译和审计','scope':'exact original empty-inclusive premise with a nonzero singleton interaction; refutation only'})
    elif obj['id']=='cvpr2023-baseline-faithfulness':
        ln.update({'status':'partial','label':'完整向量子断言与截断反例已验证；原复合句不算整体通过','verified_subclaim_status':'passed'})
    else: ln['label']='所列精确范围已编译并通过公理审计'
    if obj['id'] in ['cvpr2023-shapley','shared-harsanyi-shapley-dividend','f11-shapley']:
        ln['notes_md']='Lean 经典Shapley对象由阶乘权重边际定义；等分交互式是证明结论。'
    for step in obj.get('proof_steps',[]):
        if step['id'] in step_names:
            step['lean_refs']=[]
            for name in step_names[step['id']]:
                if name not in decls: raise RuntimeError('missing step declaration '+name)
                d=decls[name]
                step['lean_refs'].append({'declaration':name,'source_path':d['source_path'],'line':d['line'],'scope':'definition' if d['kind']=='definition' else 'proved_general_identity_or_paper_adapter','explanation_md':'这一步引用该真实定义或声明；数值例子的代入仍属于正文计算。'})
    ln['step_map']=[{'step_id':s['id'],**r} for s in obj.get('proof_steps',[]) for r in s.get('lean_refs',[])]
    if obj in data['results'] or obj in fragment['results']:
        md='# '+obj['title']+'\n\n'
        for d in obj['definitions']: md+=d.get('body_md',d.get('text_md',''))+'\n\n'
        md+=r'\['+obj['statement_tex']+r'\]'+'\n\n'+obj['overview']+'\n\n'
        for s in obj['proof_steps']:
            md+='## '+s['title']+'\n\n'+s['body_md']+'\n\n'
            if s['formula_tex']:md+=r'\['+s['formula_tex']+r'\]'+'\n\n'
        (ROOT/obj['rewrite_path']).write_text(md)
for issue in data['issues']+fragment['issues']:
    if issue.get('id') in ['cvpr-issue-linearity-index','cvpr-issue-beta-proof','cvpr-issue-distribution-incomparable','issue-f11-or-intermediate-20260930']:
        issue['status']='proof_repaired_and_formally_audited'
fragment['counts']={'finite_targets':9,'rewrite_complete':9,'lean_verified_scopes':9}
data['counts'].update({'lean_full_result_scopes_verified':14,'lean_partial_compound_result':1,'lean_counterexample_verified':1,'audited_declarations':len(decls)})
path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
fragment_path.write_text(json.dumps(fragment,ensure_ascii=False,indent=2)+'\n')
print('CVPR targets 16: 14 full scopes, 1 compound partial, 1 false statement/refutation; Generalizable finite scopes 9; audit',len(decls))
