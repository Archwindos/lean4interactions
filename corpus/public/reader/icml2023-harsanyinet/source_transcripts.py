"""Equation-level author transcriptions. Printed errors are intentionally retained."""
from pathlib import Path
import json
BASE=Path(__file__).resolve().parents[1]
TRANSCRIPTS={
'icml2023-harsanyinet':{
'hnet-readout-linearity':r'''Theorem 2, Appendix B, physical PDF page 12. Mathematical transcription of the complete author proof; the source writes $w_u^{(l)}$ for the readout coefficient.

The author first expands the dot products:
\[
v(x)=\sum_{l=1}^L(w_v^{(l)})^\top z^{(l)}(x)
=\sum_{l=1}^L\sum_{u=1}^{m^{(l)}}w_u^{(l)}z_u^{(l)}(x).
\]
The stated linearity property is: if, for every $S\subseteq N$, $v(x_S)=u(x_S)+w(x_S)$ and $(cv)(x_S)=c\,v(x_S)$ for $c\in\mathbb R$, then
\[
I^v(S)=I^u(S)+I^w(S),\qquad I^{(cv)}(S)=cI^v(S).
\]
Since $J_u^{(l)}(S)$ denotes the Harsanyi interaction computed on $z_u^{(l)}(x)$, the author concludes
\[
I(S)=\sum_{l=1}^L\sum_{u=1}^{m^{(l)}}w_u^{(l)}J_u^{(l)}(S).
\]
There are no further proof calculations in this block.''',
'hnet-forward-shapley':r'''Theorem 3, Appendix B, physical PDF pages 12–13. Complete author mathematical proof transcription.

The statement on page 12 is
\[
\varphi(i)=\sum_{l=1}^L\sum_{u=1}^{m^{(l)}}\frac{1}{|R_u^{(l)}|}w_u^{(l)}z_u^{(l)}(x)\mathbf1(R_u^{(l)}\ni i).
\]
The page 13 proof invokes Theorems 1 and 2 and gives exactly the following chain:
\[
\begin{aligned}
\varphi(i)&=\sum_{S\subseteq N:S\ni i}\frac1{|S|}I(S)\\
&=\sum_{S\subseteq N}\frac1{|S|}I(S)\mathbf1(S\ni i)\\
&=\sum_{l=1}^L\sum_{u=1}^{m^{(l)}}\frac1{|R_u^{(l)}|}w_u^{(l)}z_u^{(l)}(x)\mathbf1(R_u^{(l)}\ni i).
\end{aligned}
\]
The text supplies no additional intermediate calculation, and does not state an empty-receptive-field division convention.''',
'hnet-architecture-r1-r2':r'''Theorem 4, Appendix B, physical PDF pages 13–14. Complete author mathematical proof transcription, including the questionable quantifiers and the gate-factor equality as printed.

The receptive field is defined by
\[
R_u^{(l)}=\bigcup_{(l',u')\in S_u^{(l)}}R_{u'}^{(l')},\qquad R_u^{(1)}=S_u^{(1)}.
\]
**(1) Requirement 1.** For arbitrary inputs $\widetilde x=\widetilde z^{(0)}$ and $x=z^{(0)}$, suppose $\widetilde x_i=x_i$ for $i\in R_u^{(l)}$; the goal is $z_u^{(l)}(\widetilde x)=z_u^{(l)}(x)$.

For first-layer neurons, the author considers $R_{u'}^{(1)}=S_{u'}^{(1)}\subseteq R_u^{(l)}$ and writes
\[
g_{u'}^{(1)}(\widetilde x)=(A_{u'}^{(1)})^\top\Sigma_{u'}^{(1)}\widetilde z^{(0)}=(A_{u'}^{(1)})^\top\zeta,
\]
where $\zeta_i=\widetilde z_i^{(0)}$ for $i\in R_{u'}^{(1)}$ and zero otherwise. Similarly,
\[
g_{u'}^{(1)}(x)=(A_{u'}^{(1)})^\top\Sigma_{u'}^{(1)}z^{(0)}=(A_{u'}^{(1)})^\top\eta,
\]
where $\eta_i=z_i^{(0)}=\widetilde z_i^{(0)}$ on this receptive field and zero otherwise. Thus $g_{u'}^{(1)}(\widetilde x)=g_{u'}^{(1)}(x)$ and $z_{u'}^{(1)}(\widetilde x)=z_{u'}^{(1)}(x)$.

For the second layer the author writes
\[
R_{u'}^{(2)}=\bigcup_{(1,u'')\in S_{u'}^{(2)}}R_{u''}^{(1)}\subseteq R_u^{(l)}.
\]
Its children have first-layer receptive fields contained in $R_u^{(l)}$, and their outputs agree on the two samples, so $z_{u'}^{(2)}(\widetilde x)=z_{u'}^{(2)}(x)$. Repeating this argument recursively yields $z_u^{(l)}(\widetilde x)=z_u^{(l)}(x)$, proving R1.

**(2) Requirement 2.** For $x$ and its masked sample $x_S$, the goal is
\[
z_u^{(l)}(x_S)=z_u^{(l)}(x)\prod_{i\in R_u^{(l)}}\mathbf1(i\in S).
\]
The author separates (a) $S\supseteq R_u^{(l)}$ from (b) $S\subsetneq R_u^{(l)}$ or $S$ incomparable with $R_u^{(l)}$ (written $S\cup R_u^{(l)}\ne S$ and $S\cup R_u^{(l)}\ne R_u^{(l)}$).

In case (a), all receptive-field coordinates remain unchanged. The established R1 gives
\[
z_u^{(l)}(x_S)=z_u^{(l)}(x)=z_u^{(l)}(x)\prod_{i\in R_u^{(l)}}\mathbf1(i\in S).
\]
In case (b), choose $j\in R_u^{(l)}\setminus S$. Since $z^{(0)}=x-b$ and masking sets $(x_S)_j=b$, one has
\[
(z_S^{(0)})_j=0,\qquad\prod_{i\in R_u^{(l)}}\mathbf1(i\in S)=0.
\]
There exists a first-layer neuron with $j\in R_{u'}^{(1)}=S_{u'}^{(1)}\subseteq R_u^{(l)}$. The original then prints a universal $\forall u'$ and the equality
\[
h_{u'}^{(1)}(x_S)
=g_{u'}^{(1)}(x_S)\prod_{(0,u'')\in S_{u'}^{(1)}}\mathbf1(z_{u''}^{(0)}(x_S)\ne0)
=g_{u'}^{(1)}(x_S)\mathbf1((z_S^{(0)})_j\ne0)=0,
\]
and hence $z_{u'}^{(1)}(x_S)=0$. The proof continues on page 14: since $j$ lies in the recursive union of child receptive fields, such a first-layer neuron affects the target recursively, so $h_u^{(l)}(x_S)=0$ and $z_u^{(l)}(x_S)=0$. Therefore
\[
z_u^{(l)}(x_S)=z_u^{(l)}(x)\prod_{i\in R_u^{(l)}}\mathbf1(i\in S)=0.
\]
The author concludes R2. The repair explains why the entire product vanishes rather than equating it to one factor, and propagates zero along the relevant ancestor path without the unwarranted universal quantifier.''',
'hnet-unit-interaction':r'''Lemma 1, Appendix C, physical PDF pages 14–15. Complete author mathematical proof transcription. The missing centered-baseline term in the printed recurrence and the source's induction statements are retained.

The lemma claims $J_u^{(l)}(R_u^{(l)})=z_u^{(l)}(x)$ and $J_u^{(l)}(S)=0$ for every $S\ne R_u^{(l)}$, using only R1 and R2. For readability in this transcription write $R=R_u^{(l)}$, $z=z_u^{(l)}(x)$ and $J=J_u^{(l)}$.

The author invokes Definition 2, printing $I(S)=v(S)-\sum_{L\subsetneq S}I(L)$ with $I(\varnothing)=0$, and R2, and writes
\[
J(S)=z_u^{(l)}(x_S)-\sum_{L\subsetneq S}J(L)
=z\prod_{i\in R}\mathbf1(i\in S)-\sum_{L\subsetneq S}J(L).
\]
**(1) At $R$.** First prove $J(L)=0$ for proper subsets $L\subsetneq R$ by induction. When $|L|=1$, every $L'\subseteq L\subsetneq R$ has $\prod_{i\in R}\mathbf1(i\in L')=0$, and the source writes $J(L')=z\prod_{i\in R}\mathbf1(i\in L')=0$. Its induction hypothesis says that when $|L|=k$, all $L'\subseteq L\subsetneq R$ have $J(L')=0$. For $|L|=k+1$, the activation product is zero and all proper-subset interactions vanish, so
\[
J(L)=z\prod_{i\in R}\mathbf1(i\in L)-\sum_{L'\subsetneq L}J(L')=0.
\]
The author concludes this for $1\le|L|<|R|$. Since the product at $R$ is one, the next calculation is
\[
J(R)=z\prod_{i\in R}\mathbf1(i\in R)-\sum_{L\subsetneq R}J(L)=z.
\]
**(2) Away from $R$.** The source separates proper subsets, strict supersets, and incomparable sets. Proper subsets have already been treated. For strict supersets the activation product is one. At $|S|=|R|+1$ it prints
\[
J(S)=z\prod_{i\in R}\mathbf1(i\in S)-\sum_{L\subsetneq S}J(L)
=z-\left[J(R)+\sum_{L\subsetneq S,\,L\ne R}J(L)\right]=0.
\]
The parenthetical text says the remaining $J(L)$ are similarly zero by induction. Assuming the result for $|S|=|R|+k$, it asserts the result for $|S|=|R|+(k+1)$ without another calculation.

On page 15 the incomparable case has product zero and is asserted, again by induction:
\[
J(S)=z\prod_{i\in R}\mathbf1(i\in S)-\sum_{L\subsetneq S}J(L)=0.
\]
The parenthetical source sentence says that for $L\subsetneq S$ the same induction proves $J(S)=0$ (it repeats $S$, rather than $L$). The author then concludes $J(S)=0$ for all $S\ne R$.

The complete source has no empty-field exclusion and no proof of $z(x_\varnothing)=0$ from R1/R2. That boundary makes the lemma false as stated; its counterexample is recorded separately.''',
'hnet-cnn-receptive':r'''Appendix E, physical PDF page 16, first part of the complete Setting 2 proof.

The source assumes that all channel neurons at the same spatial position share
\[
\tau_{(1,h,w)}^{(l)}=\tau_{(2,h,w)}^{(l)}=\cdots=\tau_{(C,h,w)}^{(l)}\in\mathbb R^{CK^2}.
\]
Since $(\Sigma_u^{(l)})_{i,i}=\mathbf1((\tau_u^{(l)})_i>0)$, it concludes equality of all the corresponding selection matrices, then equality of their child sets:
\[
\Sigma_{(1,h,w)}^{(l)}=\cdots=\Sigma_{(C,h,w)}^{(l)},\qquad
S_{(1,h,w)}^{(l)}=\cdots=S_{(C,h,w)}^{(l)}.
\]
Applying the recursive definition in Eq.(8) gives
\[
R_{(1,h,w)}^{(l)}=R_{(2,h,w)}^{(l)}=\cdots=R_{(C,h,w)}^{(l)}.
\]
Thus all channel units at the same spatial location share their receptive field. The following grouping argument is transcribed separately under `hnet-cnn-regroup`; the two records together retain the complete source proof.''',
'hnet-cnn-regroup':r'''Appendix E, physical PDF page 16, second part of the complete Setting 2 proof. The printed sums without receptive-field filters, and the assertion about simultaneous activation, are preserved.

Considering $C$ channels as $C$ units, the source gives $m^{(l)}=HWC$ and writes
\[
I(S=R_{(1,h,w)}^{(l)})=\cdots=I(S=R_{(C,h,w)}^{(l)}),
\]
abbreviated $I(S=R_u^{(l)})$. It then invokes Theorem 2 and Lemma 1 and prints
\[
I(S=R_u^{(l)})
=\sum_{l=1}^L\sum_{u=1}^{m^{(l)}}w_{v,u}^{(l)}J_u^{(l)}(S=R_u^{(l)})
=\sum_{l=1}^L\sum_{u=1}^{HWC}w_{v,u}^{(l)}z_u^{(l)}(x).
\]
Here both weights and unit activations are scalar. The source says equal children make all $h_{(c,h,w)}^{(l)}(x)$ activated or deactivated simultaneously due to the AND operation. It specifies
\[
g_u^{(l)}(x)=(A_u^{(l)})^\top\Sigma_u^{(l)}z^{(l-1)},\qquad
A_u^{(l)}\in\mathbb R^{CK^2},
\]
and stacks the $C$ kernels as $B_u^{(l)}\in\mathbb R^{(CK^2)\times C}$, with $\Sigma_u^{(l)}\in\mathbb R^{(CK^2)\times(CK^2)}$ and local feature $z^{(l-1)}\in\mathbb R^{CK^2}$.

Considering all channels together as one vector unit gives $m^{(l)}=HW$ and prints
\[
I(S=R_{(:,h,w)}^{(l)})
=\sum_{l=1}^L\sum_{u=1}^{m^{(l)}}w_{v,u}^{(l)}J_u^{(l)}(S=R_u^{(l)})
=\sum_{l=1}^L\sum_{u=1}^{HW}(w_{v,u}^{(l)})^\top z_u^{(l)}(x).
\]
Both the weight and output now belong to $\mathbb R^C$. Since the vector unit shares the scalar units' children, the source says it has the same activation state. Its linear map is
\[
g_u^{(l)}(x)=(B_u^{(l)})^\top\Sigma_u^{(l)}z^{(l-1)}\in\mathbb R^C.
\]
The author concludes that channel units at one location share their field and contribute to the same interaction. No summand in the displayed scalar/vector sums is explicitly restricted to units whose receptive field equals the fixed target $S$. The corrected proof supplies this filter and distinguishes a common gate from nonzero post-ReLU outputs.'''
},
'icml2024-layerwise':{
'layer-universal-matching':r'''Appendix F, physical PDF page 15. Complete author mathematical proof transcription of Theorem 3.3; errors are retained. Equation numbers refer to the formal PDF.

The statement (14) specifies $I_{and}(\varnothing\mid x)=v_{and}(x_\varnothing)=v(x_\varnothing)$ and $I_{or}(\varnothing\mid x)=v_{or}(x_\varnothing)=0$, and asserts
\[
v(x_T)=v_{and}(x_T)+v_{or}(x_T)
=\sum_{S\subseteq T}I_{and}(S\mid x_T)+\sum_{S\cap T\ne\varnothing}I_{or}(S\mid x_T).
\]
The complete AND calculation (15) is
\[
\begin{aligned}
\sum_{S\subseteq T}I_{and}(S\mid x_T)
&=\sum_{S\subseteq T}\sum_{L\subseteq S}(-1)^{|S|-|L|}v_{and}(x_L)\\
&=\sum_{L\subseteq T}\sum_{S:L\subseteq S\subseteq T}(-1)^{|S|-|L|}v_{and}(x_L)\\
&=v_{and}(x_T)+\sum_{L\subseteq T,L\ne T}v_{and}(x_L)\underbrace{\sum_{m=0}^{|T|-|L|}(-1)^m}_{\text{source labels this }0}\\
&=v_{and}(x_T).
\end{aligned}
\]
The printed inner sum omits the binomial multiplicity. The complete OR calculation (16), using the source's $S_1,S_2$ grouping, is
\[
\begin{aligned}
\sum_{S\cap T\ne\varnothing}I_{or}(S\mid x_T)
&=-\sum_{S\cap T\ne\varnothing,S\ne\varnothing}\sum_{L\subseteq S}(-1)^{|S|-|L|}v_{or}(x_{N\setminus L})\\
&=-\sum_{L\subseteq N}\sum_{S:S\cap T\ne\varnothing,\,S\supseteq L}(-1)^{|S|-|L|}v_{or}(x_{N\setminus L})\\
&=-v_{or}(x_\varnothing)-v_{or}(x_T)\underbrace{\sum_{|S_2|=1}^{|T|}\binom{|T|}{|S_2|}(-1)^{|S_2|}}_{\text{source labels }-1}\\
&\quad-\sum_{L\cap T\ne\varnothing,L\ne N}v_{or}(x_{N\setminus L})
\underbrace{\sum_{S_1\subseteq N\setminus T\setminus L}\sum_{|S_2|=|T\cap L|}^{|T|}
\binom{|T|-|T\cap L|}{|S_2|-|T\cap L|}(-1)^{|S_1|+|S_2|}}_{\text{source labels }0}\\
&\quad-\sum_{L\cap T=\varnothing,L\ne N\setminus T}v_{or}(x_{N\setminus L})
\underbrace{\sum_{S_2\subsetneq T}\sum_{S_1\subseteq N\setminus T\setminus L}(-1)^{|S_1|+|S_2|}}_{\text{source labels }0}\\
&=v_{or}(x_T)-v_{or}(x_\varnothing).
\end{aligned}
\]
The isolated first two terms are labeled $L=N$ and $L=N\setminus T$. Thus the source states $v_{or}(x_T)=\sum_{S\cap T\ne\varnothing}I_{or}(S)+v_{or}(x_\varnothing)$.

The final calculation (17) is
\[
\begin{aligned}
v(x_T)&=v_{and}(x_T)+v_{or}(x_T)\\
&=\sum_{S\subseteq T}I_{and}(S\mid x_T)+\sum_{S\cap T\ne\varnothing,S\ne\varnothing}I_{or}(S\mid x_T)+v_{or}(x_\varnothing)\\
&=\sum_{S\subseteq T,S\ne\varnothing}I_{and}(S\mid x_T)+v_{and}(x_\varnothing)+\sum_{S\cap T\ne\varnothing}I_{or}(S\mid x_T)+v_{or}(x_\varnothing)\\
&=v(x_\varnothing)+\sum_{S\subseteq T,S\ne\varnothing}I_{and}(S\mid x_T)+\sum_{S\cap T\ne\varnothing}I_{or}(S\mid x_T)\\
&=\sum_{S\subseteq T}I_{and}(S\mid x_T)+\sum_{S\cap T\ne\varnothing}I_{or}(S\mid x_T).
\end{aligned}
\]
The author concludes the theorem. The fixed original-game values in the source expansion and its $x_T$ coefficient labels are independently distinguished in the project rewrite.''',
'layer-salient-matching':r'''Appendix G, physical PDF page 16. Complete author mathematical proof transcription of Lemma 3.4, including its external-reference argument and the duplicate-baseline equality.

The statement (18) says that every masked output can be universally matched by a small set of salient interactions:
\[
\begin{aligned}
v(x_T)&=v_{and}(x_T)+v_{or}(x_T)
=\sum_{S\subseteq T}I_{and}(S\mid x_T)+\sum_{S\cap T\ne\varnothing}I_{or}(S\mid x_T)\\
&\approx v(x_\varnothing)
+\sum_{S\in\Omega_{salient}^{and}:\varnothing\ne S\subseteq T}I_{and}(S\mid x_T)
+\sum_{S\in\Omega_{salient}^{or}:S\cap T\ne\varnothing}I_{or}(S\mid x_T).
\end{aligned}
\]
The entire author argument first cites Ren et al. (2023a) for the claim that, under common conditions (footnote 1), a well-trained DNN output $v_{and}(x_T)$ on all $2^n$ masks is approximated by a small number of AND interactions with salient effects, with $|\Omega_{salient}^{and}|\ll2^n$.

It then invokes Appendix C's assertion that OR interactions are particular AND interactions, and concludes that a well-trained DNN output $v_{or}(x_T)$ is similarly approximated by a small number of OR interactions, with $|\Omega_{salient}^{or}|\ll2^n$.

The final calculation (19), retained exactly in its baseline placement, is
\[
\begin{aligned}
v(x_T)&=v_{and}(x_T)+v_{or}(x_T)\\
&=v(x_\varnothing)+\sum_{S\subseteq T}I_{and}(S\mid x_T)+\sum_{S\cap T\ne\varnothing}I_{or}(S\mid x_T)\\
&\approx v(x_\varnothing)
+\sum_{S\in\Omega_{salient}^{and}:\varnothing\ne S\subseteq T}I_{and}(S\mid x_T)
+\sum_{S\in\Omega_{salient}^{or}:S\cap T\ne\varnothing}I_{or}(S\mid x_T).
\end{aligned}
\]
The author concludes that Lemma 3.4 is proved. The argument contains no quantitative definition of “small” or of the approximation error, and no demonstration that both learned decomposition components satisfy the cited DNN conditions. These gaps and the first equality's duplicate empty AND dividend are recorded separately.''',
'layer-complement-duality':r'''Appendix C, physical PDF page 13. Complete mathematical argument as printed, including the two coordinate definitions and the subsequent sparsity inference.

The source calls OR a specific AND interaction after inverting masked and unmasked states. It defines (11)
\[
(x_{N\setminus T})_i=\begin{cases}x_i&i\in N\setminus T,\\b_i&i\in T,\end{cases}
\]
then defines the supposedly inverted sample in (12) by
\[
(x'_T)_i=\begin{cases}x_i&i\in T,\\b_i&i\in N\setminus T.\end{cases}
\]
It then prints (13)
\[
I_{or}(S\mid x)=-\sum_{T\subseteq S}(-1)^{|S|-|T|}v(x_{N\setminus T})
=-\sum_{T\subseteq S}(-1)^{|S|-|T|}v(x'_T)
=-I_{and}(S\mid x').
\]
The concluding paragraph states that this equality transfers the proven AND sparsity of Ren et al. (2024) to OR sparsity, so most well-trained DNNs encode only a small number of OR interactions. The printed Eq.(12) is the ordinary original mask, not the coordinate-swapped mask needed for the second equality. That equality and the unsupported transfer of sparsity assumptions are treated as separate issues.'''
}}
for pid,items in TRANSCRIPTS.items():
 p=BASE/pid;dest=p/'original-proofs';dest.mkdir(exist_ok=True)
 content=json.loads((p/'content.json').read_text());rs={r['id']:r for r in content['results']}
 for ident,body in items.items():
  (dest/(ident+'.md')).write_text(body+'\n')
  rs[ident].update(original_proof_md=body,original_proof_source_type='complete_author_mathematical_proof_transcription_with_english_prose',original_proof_note='Every calculation and the necessary author argument are retained. Original errors are not silently corrected. Physical source pages and the complete source layout remain available.',source_transcription_status='proof_mathematical_transcription_complete',original_proof_path=str((dest/(ident+'.md')).relative_to(BASE.parents[2])))
 (p/'content.json').write_text(json.dumps(content,ensure_ascii=False,indent=2)+'\n')
 print(pid,'complete author blocks',len(items))
