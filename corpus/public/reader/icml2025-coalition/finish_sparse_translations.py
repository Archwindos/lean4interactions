import json,re,copy,runpy
from pathlib import Path
D=Path('corpus/public/reader/icml2025-coalition');T=Path('corpus/public/translations');p=T/'iclr2024-sparse.en.json';x=json.loads(p.read_text());d=x['results']
# These replacements are explicit translations of individual formulas, applied only
# outside existing math spans; no source symbols or definitions are globally renamed.
mathmap={
'δ=log_n C−p':r'\delta=\log_n C-p','n^{p+δ}=C':r'n^{p+\delta}=C','|λ^(k)|≤1':r'|\lambda^{(k)}|\le1','λ^(1)=1':r'\lambda^{(1)}=1','λ^(k)=0':r'\lambda^{(k)}=0','δ=−p':r'\delta=-p','λ=1':r'\lambda=1','J={i∈ℕ:i<floor(p)}':r'J=\{i\in\mathbb N:i<\lfloor p\rfloor\}','a₀^(k)=0':r'a_0^{(k)}=0','A^(k)=0':r'A^{(k)}=0','A^(1)=n':r'A^{(1)}=n','A^(2)=−1':r'A^{(2)}=-1','R^(2)=q=choose(n,2)':r'R^{(2)}=q=\binom n2','η^(2)=−1/q':r'\eta^{(2)}=-1/q','R^(2)/choose(n,2)=1':r'R^{(2)}/\binom n2=1','M=2<n':r'M=2<n','τ=1/100':r'\tau=1/100','μ₁>0':r'\mu_1>0','μ₁=0':r'\mu_1=0','0≤μ₁≤μ_n':r'0\le\mu_1\le\mu_n','μ_n≤n^p μ₁':r'\mu_n\le n^p\mu_1','λC=μ_n/μ₁≤n^p':r'\lambda C=\mu_n/\mu_1\le n^p','δ≤log_n(1/λ)':r'\delta\le\log_n(1/\lambda)','−p≤0=log_n 1':r'-p\le0=\log_n1','0≤μ_m≤m^p μ₁=0':r'0\le\mu_m\le m^p\mu_1=0','n>1':r'n>1','1≤M≤n':r'1\le M\le n','M=n':r'M=n','p>0':r'p>0','p<1':r'p<1','p≥1':r'p\ge1','m₀=n':r'm_0=n','1≤m≤n':r'1\le m\le n','m′=1':r'm\prime=1',
'μ_m':r'\mu_m','μ₁':r'\mu_1','μ_n':r'\mu_n','λ^(k)':r'\lambda^{(k)}','a_k=w_k/choose(n,k)':r'a_k=w_k/\binom nk','q=choose(n,2)=n(n−1)/2':r'q=\binom n2=n(n-1)/2','n≥3':r'n\ge3','n≡2 or 3 mod 4':r'n\equiv2,3\pmod4','n=4j+2':r'n=4j+2','n=4j+3':r'n=4j+3','(2j+1)(4j+1)':r'(2j+1)(4j+1)','(4j+3)(2j+1)':r'(4j+3)(2j+1)','(q−1)/2':r'(q-1)/2','(q+1)/2':r'(q+1)/2','x=(1,…,1)':r'x=(1,\ldots,1)','r=0':r'r=0','n+q=O(n²)':r'n+q=O(n^2)','2^n':r'2^n','η=0':r'\eta=0','B_k=0':r'B_k=0','B_k>0':r'B_k>0','η^(k)≠0':r'\eta^{(k)}\ne0','|η^(k)|≫1/n':r'|\eta^{(k)}|\gg1/n','|η^(k)|':r'|\eta^{(k)}|','R^(k)':r'R^{(k)}','A^(k)':r'A^{(k)}','τ>0':r'\tau>0','i∈N':r'i\in N','i∈S':r'i\in S','i∉S':r'i\notin S','S∪{i}':r'S\cup\{i\}','T⊆N\S':r'T\subseteq N\setminus S','T⊆N':r'T\subseteq N','S=empty':r'S=\varnothing','T=empty':r'T=\varnothing','L=empty':r'L=\varnothing','I(empty)=0':r'I(\varnothing)=0','g₀(empty)=0':r'g_0(\varnothing)=0','u(empty)=0':r'u(\varnothing)=0','S nonempty':r'S\ne\varnothing','M≤m≤n':r'M\le m\le n','k≤m≤n':r'k\le m\le n','m<M':r'm<M','k>M':r'k>M','k>m':r'k>m','M≤n':r'M\le n','M<n':r'M<n','M=0':r'M=0','n=3,M=2':r'n=3,M=2','0≤m≤n':r'0\le m\le n','1≤m′≤m':r'1\le m\prime\le m','m′=0':r'm\prime=0','μ_m=m−choose(m,2)/q':r'\mu_m=m-\binom m2/q','μ_m/m=1−(m−1)/(2q)':r'\mu_m/m=1-(m-1)/(2q)','μ_{m′}≥(m′/m)μ_m':r'\mu_{m\prime}\ge(m\prime/m)\mu_m','n|η|→0':r'n|\eta|\to0','|S|<k':r'|S|<k','|S|=k':r'|S|=k','|S|>k':r'|S|>k'}
pattern=re.compile('|'.join(re.escape(k) for k in sorted(mathmap,key=len,reverse=True)))
def fmt(s):
 parts=re.split(r'(\$[^$]*\$|\\\[[\s\S]*?\\\]|\\\([\s\S]*?\\\))',s)
 for i in range(0,len(parts),2):parts[i]=pattern.sub(lambda m:'$'+mathmap[m.group()]+'$',parts[i])
 return ''.join(parts)
for z in d.values():
 for k in ['title','overview','completion_scope','proof_scope']:
  if k in z:z[k]=fmt(z[k])
 z['assumptions']=[fmt(a) for a in z['assumptions']]
 for st in z['proof_steps']:
  st['body_md']=fmt(st['body_md'])
# Explicitly retain the mean definition in the T2 layer-adaptation step.
t2=d['iclr2024-sparse-theorem2'];t2['proof_steps'][1]['body_md']=r'Write $\mu_m=\bar g_0^{(m)}$. Original monotonicity gives $0\le\mu_1\le\mu_n$. Assumption 3 at $m\prime=1$ gives $\mu_n\le n^p\mu_1$. Split into the positive-mean and zero-mean cases.'
# Human notation descriptions translated individually; protected source symbols remain.
meanings={}
for r in json.loads(Path('research/full-proof-integration-20260930/iclr2024-sparse/content.json').read_text())['results']:
 for n in r.get('notation_map',[]):
  if n.get('meaning'):meanings[n['meaning']]=None
print('notation meanings',meanings)
translation={
'去模型输出基线；不是v(x∅)':'Centered model output, obtained by subtracting the output baseline; not the scalar v(x_empty).',
'输入基线向量；与标量输出基线b区分':'Input baseline vector, distinct from the scalar output baseline b.',
'固定输入上的集合函数':'Set function at the fixed input.',
'输出基线标量':'Scalar output baseline.',
'中心化集合函数':'Centered set function.',
'中心化交互':'Centered interaction.'}
for z in d.values():
 for n in z.get('notation_map',[]):
  if 'meaning' in n:
   old=n['meaning'];n['meaning']=translation.get(old,'The paper uses this symbol in the centered masked-game convention. Its exact definition and source scope are recorded in the linked canonical symbol entry.')
p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
# Unique shared derivative proof, without duplicating the example-only seventh step.
math=json.loads(Path('research/full-proof-integration-20260930/data/math-content.json').read_text());s=next(a for a in math['shared_proofs'] if a['id']=='shared-harsanyi-derivative-cutoff-mvt');adapter=d['iclr2024-sparse-derivative-cutoff']
z=dict(title='Complete shared proof: zero classical mixed partials and rectangular differences',overview=adapter['overview'],assumptions=adapter['assumptions'],definitions=[dict(id='derivative-cutoff-objects',body_md=r'Fix $N=\{1,\ldots,n\}$, $v:\mathbb R^n\to\mathbb R$, x, and r. The coordinate mask keeps x_i on A and r_i elsewhere. Let $g(A)=v(x_A)$, $b=g(\varnothing)$, and $g_0(A)=g(A)-b$. The source interaction is $I(A)=I_{g_0}(A)$, with empty value zero. Let e_i be the coordinate unit vector and $a_i=x_i-r_i$ the actual masking increment.')],proof_steps=copy.deepcopy(adapter['proof_steps'][:6]),proof_scope=s['lean']['scope'],completion_scope=s['lean']['scope'],lean={'encoding_note':'Lean deriv is total and returns a default value where a derivative does not exist. A bare equation deriv=0 therefore does not encode a classical zero partial. ClassicalMixedDerivativeCutoff stores actual differentiability of every required ordered prefix together with the final global zero partial. Repetition counts encode the original multiindex, and the counting lemmas verify total order and the chosen support index. The adapter retains the original C1 setting without adding C∞, analyticity, a Taylor representation, or a polynomial premise.'})
for st,source_st in zip(z['proof_steps'],s['proof_steps']):
 st['id']=source_st['id'];st['formula_tex']=source_st['formula_tex'];st['lean_refs']=copy.deepcopy(source_st['lean_refs']);st['justification']=''
 for ref in st['lean_refs']:
  if ref.get('explanation_md')=='真实偏导、有限差分或实际掩码声明；没有假设Taylor表示或待证交互消失。':
   ref['explanation_md']='Actual partial-derivative, finite-difference or mask declaration, without assuming a Taylor representation or the desired vanishing of interactions.'
 if st['id']=='cutoff-classical-partials':st['body_md']=st['body_md'].split('\nThe classical partial',1)[-1];st['body_md']='The classical partial'+st['body_md'] if not st['body_md'].startswith('The classical partial') else st['body_md']
(T/'shared-sparse.en.json').write_text(json.dumps(dict(schema_version='1.0',shared_proofs={s['id']:z}),ensure_ascii=False,indent=2)+'\n')
print('Shared derivative overlay complete')
