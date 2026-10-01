import json
from pathlib import Path
P=Path(__file__).parent;d=json.loads((P/'content.json').read_text())
base=['sym-model','sym-game','sym-output-baseline','sym-universe','sym-mask']
comp=['sym-coalition-and-component','sym-coalition-or-component','sym-coalition-decomposition-parameter','sym-coalition-and-effect','sym-coalition-or-effect']
J=['sym-coalition-total-effect'];phi=['sym-coalition-attribution'];sh=['sym-coalition-shapley'];ui=['sym-coalition-individual-conflict'];cf=['sym-coalition-total-conflict']
sets={'shapley':base+comp+J+sh,'banzhaf':base+comp+J+['sym-coalition-banzhaf'],'conflict':base+comp+J+phi+sh+cf,'no-conflict':base+comp+J+phi+sh+cf,'individual':base+comp+J+phi+sh+ui,'singleton':base+comp+J+phi+sh,'efficiency':base+comp+J+phi+sh+cf,'anonymity':base+comp+J+phi,'symmetry-alpha':base+comp+J+phi,'symmetry-beta':base+comp+J+phi,'additivity':base+comp+J+phi,'dummy':base+comp+J+phi,'shapley-coefficient':['sym-universe','sym-coalition-shapley'],'banzhaf-coefficient':['sym-universe','sym-coalition-banzhaf'],'matching':base+comp,'R':base+comp+J+phi+ui+['sym-coalition-metric-R'],'Rprime':base+comp+['sym-coalition-metric-Rprime'],'Q':base+comp+['sym-coalition-metric-Q'],'toy-support':base,'illustration':base+comp+J+phi+cf,'logit':['sym-model','sym-game'],'shapley-definition':base+sh,'and-or-definition':base+comp,'sparse-optimization':base+comp,'conflict-definition':base+phi+ui+cf+sh,'banzhaf-definition':base+['sym-coalition-banzhaf'],'coalition-definition':base+comp+J+phi,'empirical':['sym-model','sym-mask'],'external-comparison':phi+sh}
zh=r'''固定有限总体 $N$、输入 $x$ 和输入基线向量 $r$；$g(U)=v(x_U)$，$b=g(\varnothing)$。局部 $a=g_{and}$、$o=g_{or}$ 简写两个原分量，$a(U)=g(U)/2+\gamma_U$、$o(U)=g(U)/2-\gamma_U$。$A=I_{g_{and}}$、$O=O_{g_{or}}$ 分别简写 AND 分量的 Möbius 交互与非空 OR 负补集交互；$J=A+O$。原始输出基线不默认零。'''
en=r'''Fix a finite universe $N$, input $x$, and input baseline vector $r$; put $g(U)=v(x_U)$ and $b=g(\varnothing)$. Local $a=g_{and}$ and $o=g_{or}$ abbreviate the two source components, $a(U)=g(U)/2+\gamma_U$ and $o(U)=g(U)/2-\gamma_U$. Local $A=I_{g_{and}}$ and $O=O_{g_{or}}$ abbreviate the AND component’s Möbius dividend and the nonempty OR negative complementary dividend; $J=A+O$. The raw output baseline need not vanish.'''
phiz=r'''对非空联盟 $S$，原 Eq.(6) 为 $\phi(S)=\sum_{T\subseteq N,S\subseteq T}|S|J(T)/|T|$。原空联盟项含 $0/0$，此处不新增取值约定。'''
phie=r'''For a nonempty coalition $S$, Eq.(6) is $\phi(S)=\sum_{T\subseteq N,S\subseteq T}|S|J(T)/|T|$. The source empty-coalition term contains $0/0$; no new value convention is inserted here.'''
for r in d['results']:
 k=r['id'].removeprefix('coalition-');r['symbol_ids']=sets[k]
 ez=r['translations']['en']
 if comp[0] in sets[k]:
  r['definitions']=[{'id':'coalition-objects','body_md':zh}];ez['definitions']=[{'id':'coalition-objects','body_md':en}]
  if phi[0] in sets[k]:r['definitions'].append({'id':'coalition-attribution-object','body_md':phiz});ez['definitions'].append({'id':'coalition-attribution-object','body_md':phie})
 elif k in ('shapley-coefficient','banzhaf-coefficient'):
  r['definitions']=[];ez['definitions']=[];r['notation_map']=[];ez['notation_map']=[]
 elif k=='toy-support':
  r['definitions']=[{'id':'coalition-toy-game','body_md':r'二进制输入、零输入基线；掩码游戏 $g(U)=f(x_U)$，$T_k$ 为原单项式支撑。本条计算总游戏的 Harsanyi AND 系数 $I_g$，不是学习分解的 $A,O$。'}];ez['definitions']=[{'id':'coalition-toy-game','body_md':r'Use binary inputs and zero input baseline, with masked game $g(U)=f(x_U)$ and source monomial supports $T_k$. This entry computes the total game’s Harsanyi AND dividend $I_g$, distinct from the learned split’s $A,O$.'}]
  r['notation_map']=r['notation_map'][:1];ez['notation_map']=ez.get('notation_map',[])[:1] if 'notation_map' in ez else r['notation_map']
 else:r['definitions']=[];ez['definitions']=[]
 if k=='shapley-coefficient':
  r['assumptions']=[r'原系数定义域 $n=|N|\ge1$，$0\le l=|L|\le n-1$。'];ez['assumptions']=[r'The source coefficient domain is $n=|N|\ge1$ and $0\le l=|L|\le n-1$.']
  r['proof_steps'][0]['body_md']=r'令 $R=N\setminus\{i\}$、$L\subseteq R$、$l=|L|$、$n=|R|+1$，$w(U)=|U|!(n-|U|-1)!/n!$。均匀随机排列中 $w(U)$ 是 $U$ 恰为 $i$ 前驱集的概率；$L$ 全在 $i$ 前当且仅当 $i$ 在 $L\cup\{i\}$ 中最后出现，概率为 $1/(l+1)$。按 $|U|=l+k$ 分组，满足 $L\subseteq U\subseteq R$ 的集合数为 $\binom{n-1-l}{k}$，且 $w(U)=1/[n\binom{n-1}{l+k}]$，所以得到原显示二项式系数等式。OR 不交背景用补集双射或最先出现计数得到同一值。Lean 核验等价阶乘前驱有限和；按基数分组到显示二项式式子的解释是人类适配，未另作直接数值索引声明。'
  ez['proof_steps'][0]['body_md']=r'Let $R=N\setminus\{i\}$, $L\subseteq R$, $l=|L|$, $n=|R|+1$, and $w(U)=|U|!(n-|U|-1)!/n!$. In a uniform random permutation, $w(U)$ is the probability that $U$ is exactly the predecessor set of $i$. All of $L$ precedes $i$ precisely when $i$ is last in $L\cup\{i\}$, with probability $1/(l+1)$. Grouping by $|U|=l+k$ yields $\binom{n-1-l}{k}$ containing backgrounds, each with $w(U)=1/[n\binom{n-1}{l+k}]$, proving the displayed binomial identity. A complement bijection or first-position count gives the same OR value. Lean checks the equivalent factorial predecessor sum; grouping it into the displayed cardinality-indexed formula is the human adaptation, without a separate numeric-index declaration.'
 if k=='banzhaf-coefficient':
  r['assumptions']=[r'$R$ 为有限集合，$L\subseteq R$，包括 $L=\varnothing$ 与 $L=R$。'];ez['assumptions']=[r'$R$ is finite and $L\subseteq R$, including $L=\varnothing$ and $L=R$.']
  r['proof_steps'][0]['body_md']=r'唯一写 $U=L\cup W$，$W\subseteq R\setminus L$，则 $|U|=|L|+|W|$。有限和化为 $(-1/2)^{|L|}\sum_{W\subseteq R\setminus L}(-1/2)^{|W|}$。大小为 $j$ 的 $W$ 有 $\binom{|R|-|L|}{j}$ 个，二项式定理给内和 $(1-1/2)^{|R|-|L|}$。乘回得到 $(-1)^{|L|}/2^{|R|}$；$R=L$ 时内和只有空项 $1$。'
  ez['proof_steps'][0]['body_md']=r'Write uniquely $U=L\cup W$ with $W\subseteq R\setminus L$, so $|U|=|L|+|W|$. The finite sum becomes $(-1/2)^{|L|}\sum_{W\subseteq R\setminus L}(-1/2)^{|W|}$. There are $\binom{|R|-|L|}{j}$ subsets of size $j$; the binomial theorem gives inner sum $(1-1/2)^{|R|-|L|}$. Multiplication yields $(-1)^{|L|}/2^{|R|}$, including $R=L$, where the inner sum is the single empty term $1$.'
 if k=='toy-support':
  r['proof_steps'][0]['body_md']=r'对于二进制输入和零输入基线，$\prod_{j\in T_k}(x_U)_j=\mathbf1_{T_k\subseteq U}\prod_{j\in T_k}x_j$，因此 $g$ 是有限个纯 AND 游戏之和，权重为 $w_k\prod_{j\in T_k}x_j$。纯 AND 的 Möbius 系数只在支撑 $T_k$ 取该权重；交互线性性给显示式。原支撑两两不同时无需合并重复项；全一输入时乘积系数为 $1$，带零坐标时对应单项式消失。这是总游戏的 Harsanyi 支撑，不意味着学习分解的 $A,O$ 唯一或只有这些支撑；也不把拟合网络的近似当成该目标函数的精确恒等式。'
  ez['proof_steps'][0]['body_md']=r'For binary inputs and zero input baseline, $\prod_{j\in T_k}(x_U)_j=\mathbf1_{T_k\subseteq U}\prod_{j\in T_k}x_j$. Thus $g$ is a finite sum of pure AND games with weights $w_k\prod_{j\in T_k}x_j$. A pure AND dividend is its weight at support $T_k$ and zero elsewhere; interaction linearity gives the displayed formula. Distinct source supports require no duplicate merging. At the all-one input the product is $1$; zero coordinates remove the corresponding monomial. This is the total game’s Harsanyi support, without claiming uniqueness or the same supports for learned $A,O$, and without treating approximate network fitting as an exact identity of the target function.'
import runpy
runpy.run_path(str(P.parent/'shared_dependencies.py'))['apply_shared_dependencies'](d,P)
(P/'content.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
s=json.loads((P/'symbols.json').read_text());maps={'sym-coalition-and-component':'sym-and-output','sym-coalition-or-component':'sym-or-output','sym-coalition-and-effect':'sym-and-component-interaction','sym-coalition-or-effect':'sym-or-component-interaction','sym-coalition-decomposition-parameter':'sym-decomposition-parameter','sym-coalition-shapley':'sym-shapley'}
for a in s['symbols']:a['canonical_id']=maps.get(a['id'],a['id'])
(P/'symbols.json').write_text(json.dumps(s,ensure_ascii=False,indent=2)+'\n')
