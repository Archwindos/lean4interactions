from pathlib import Path
import json
D=Path('corpus/public/reader/icml2025-coalition');B=D/'original-proofs';blocks={}
blocks['C']=r'''# Appendix C. Proof of Theorem 2 (main Theorem 3.2)

Source: official PDF pages 12–14. This is a complete mathematical transcription of the author calculation. In this transcription U denotes the background called S in the PDF, and the source's A and B marginal components are written A_U and B_U. The source interaction names Iand and Ior are preserved. These changes only prevent a bound-variable collision; the erroneous nonempty-intersection domains on page 14 are retained below.

According to the definition of Shapley values,
\[
\varphi(i)=\sum_{U\subseteq N\setminus\{i\}}\frac{|U|!(n-|U|-1)!}{n!}[v(U\cup\{i\})-v(U)]
=\mathbb E_{U\subseteq N\setminus\{i\}}[v(U\cup\{i\})-v(U)].
\]
According to Eq. (10), for every U⊆N,
\[
v(U)=v(\varnothing)+\sum_{L\subseteq U,L\ne\varnothing}I_{and}(L)+\sum_{L\cap U\ne\varnothing}I_{or}(L).
\]
Thus
\[
\begin{aligned}
v(U\cup\{i\})-v(U)
&=\left[v(\varnothing)+\sum_{L\subseteq U\cup\{i\},L\ne\varnothing}I_{and}(L)+\sum_{L\cap(U\cup\{i\})\ne\varnothing}I_{or}(L)\right]\\
&\quad-\left[v(\varnothing)+\sum_{L\subseteq U,L\ne\varnothing}I_{and}(L)+\sum_{L\cap U\ne\varnothing}I_{or}(L)\right]\\
&=\left[\sum_{L\subseteq U\cup\{i\},L\ne\varnothing}I_{and}(L)-\sum_{L\subseteq U,L\ne\varnothing}I_{and}(L)\right]
+\left[\sum_{L\cap(U\cup\{i\})\ne\varnothing}I_{or}(L)-\sum_{L\cap U\ne\varnothing}I_{or}(L)\right]\\
&=\underbrace{\sum_{L\subseteq U}I_{and}(L\cup\{i\})}_{A_U}
+\underbrace{\sum_{L\cap U=\varnothing}I_{or}(L\cup\{i\})}_{B_U}.
\end{aligned}
\]
This breaks the Shapley value into E[A_U+B_U]. For the AND part the complete page-13 chain is
\[
\begin{aligned}
\mathbb E_U[A_U]
&=\mathbb E_U\sum_{L\subseteq U}I_{and}(L\cup\{i\})\\
&=\frac1n\sum_{m=0}^{n-1}\frac1{\binom{n-1}m}\sum_{\substack{U\subseteq N\setminus\{i\}\\|U|=m}}\sum_{L\subseteq U}I_{and}(L\cup\{i\})\\
&=\frac1n\sum_{L\subseteq N\setminus\{i\}}\sum_{m=0}^{n-1}\frac1{\binom{n-1}m}\sum_{\substack{U\supseteq L,\ U\subseteq N\setminus\{i\}\\|U|=m}}I_{and}(L\cup\{i\})\\
&=\frac1n\sum_{L\subseteq N\setminus\{i\}}\sum_{m=|L|}^{n-1}\frac1{\binom{n-1}m}\sum_{\substack{U\supseteq L,\ U\subseteq N\setminus\{i\}\\|U|=m}}I_{and}(L\cup\{i\})\\
&=\frac1n\sum_{L\subseteq N\setminus\{i\}}\sum_{m=|L|}^{n-1}\frac{\binom{n-1-|L|}{m-|L|}}{\binom{n-1}m}I_{and}(L\cup\{i\})\\
&=\sum_{L\subseteq N\setminus\{i\}}\underbrace{\left[\frac1n\sum_{k=0}^{n-1-|L|}\frac{\binom{n-1-|L|}k}{\binom{n-1}{|L|+k}}\right]}_{\alpha_L}I_{and}(L\cup\{i\})\\
&=\sum_{L\subseteq N\setminus\{i\}}\frac1{|L|+1}I_{and}(L\cup\{i\})
=\sum_{T\subseteq N,i\in T}\frac1{|T|}I_{and}(T).
\end{aligned}
\]
The source comments give |U|≥|L| in the third-to-fourth line, k=m−|L| in the sixth line, and T=L∪{i} in the last line.

The OR chain on page 14 prints the following domains. **The first three nonempty-intersection conditions are source errors and are not corrected in this original-proof field.**
\[
\begin{aligned}
\mathbb E_U[B_U]
&=\mathbb E_U\sum_{L\cap U\ne\varnothing}I_{or}(L\cup\{i\})\\
&=\frac1n\sum_{m=0}^{n-1}\frac1{\binom{n-1}m}\sum_{\substack{U\subseteq N\setminus\{i\}\\|U|=m}}\sum_{L\cap U\ne\varnothing}I_{or}(L\cup\{i\})\\
&=\frac1n\sum_{L\subseteq N\setminus\{i\}}\sum_{m=0}^{n-1}\frac1{\binom{n-1}m}\sum_{\substack{U\cap L\ne\varnothing,\ U\subseteq N\setminus\{i\}\\|U|=m}}I_{or}(L\cup\{i\})\\
&=\frac1n\sum_{L\subseteq N\setminus\{i\}}\sum_{m=0}^{n-1}\frac1{\binom{n-1}m}\sum_{\substack{U\subseteq N\setminus\{i\}\setminus L\\|U|=m}}I_{or}(L\cup\{i\})\\
&=\frac1n\sum_{L\subseteq N\setminus\{i\}}\sum_{m=0}^{n-1-|L|}\frac1{\binom{n-1}m}\sum_{\substack{U\subseteq N\setminus\{i\}\setminus L\\|U|=m}}I_{or}(L\cup\{i\})\\
&=\frac1n\sum_{L\subseteq N\setminus\{i\}}\sum_{m=0}^{n-1-|L|}\frac{\binom{n-1-|L|}m}{\binom{n-1}m}I_{or}(L\cup\{i\})\\
&=\frac1n\sum_{L\subseteq N\setminus\{i\}}\sum_{k=0}^{n-1-|L|}\frac{\binom{n-1-|L|}{n-1-|L|-k}}{\binom{n-1}{n-1-|L|-k}}I_{or}(L\cup\{i\})\\
&=\frac1n\sum_{L\subseteq N\setminus\{i\}}\sum_{k=0}^{n-1-|L|}\frac{\binom{n-1-|L|}k}{\binom{n-1}{|L|+k}}I_{or}(L\cup\{i\})\\
&=\frac1n\sum_{L\subseteq N\setminus\{i\}}\frac n{|L|+1}I_{or}(L\cup\{i\})\\
&=\sum_{L\subseteq N\setminus\{i\}}\frac1{|L|+1}I_{or}(L\cup\{i\})
=\sum_{T\subseteq N,i\in T}\frac1{|T|}I_{or}(T).
\end{aligned}
\]
The source comments use |U|≤n−1−|L| and k=n−1−|L|−m. Adding both parts concludes
\[
\varphi(i)=\mathbb E_U[A_U]+\mathbb E_U[B_U]
=\sum_{T\subseteq N,i\in T}\frac1{|T|}[I_{and}(T)+I_{or}(T)].
\]
'''
blocks['D']=r'''# Appendix D. Proof of Theorem 3 (main Theorem 3.3)

Source: official PDF pages 14–15. The original names v_and,v_or and original alternating exponents are retained. The displayed exponent +1 differs by two from the common paired form −1, so it is not itself a sign error.

According to the AND/OR definitions,
\[
\begin{aligned}
I_{and}(S)&=\sum_{L\subseteq S}(-1)^{|S|-|L|}v_{and}(L)
=\sum_{L\subseteq S\setminus\{i\}}(-1)^{|S|-|L|+1}[v_{and}(L\cup\{i\})-v_{and}(L)],\\
I_{or}(S)&=-\sum_{L\subseteq S}(-1)^{|S|-|L|}v_{or}(N\setminus L)
=\sum_{L\subseteq S\setminus\{i\}}(-1)^{|S|-|L|+1}[v_{or}(N\setminus L)-v_{or}(N\setminus L\setminus\{i\})],
\end{aligned}
\]
where v(L)=v_and(L)+v_or(L). Define, solely to keep the long source braces readable,
\[
D(L)=[v_{and}(L\cup\{i\})-v_{and}(L)]+[v_{or}(N\setminus L)-v_{or}(N\setminus L\setminus\{i\})].
\]
The source page-15 chain, with each repeated brace D(L) written in this explicitly defined shorthand, is
\[
\begin{aligned}
\sum_{S\subseteq N,S\ni i}\frac{I_{and}(S)+I_{or}(S)}{2^{|S|-1}}
&=\sum_{S\subseteq N,S\ni i}\sum_{L\subseteq S\setminus\{i\}}\frac{(-1)^{|S|-|L|+1}}{2^{|S|-1}}D(L)\\
&=\sum_{S\subseteq N\setminus\{i\}}\sum_{L\subseteq S}\frac{(-1)^{|S|-|L|}}{2^{|S|}}D(L)\\
&=\sum_{L\subseteq N\setminus\{i\}}(-1)^{|L|}\sum_{\substack{S\subseteq N\setminus\{i\}\\S\supseteq L}}\frac{(-1)^{|S|}}{2^{|S|}}D(L)\\
&=\sum_{L\subseteq N\setminus\{i\}}(-1)^{|L|}\frac{(-1)^{|L|}}{2^{|N|-1}}D(L)\\
&=\sum_{L\subseteq N\setminus\{i\}}\frac1{2^{|N|-1}}D(L)\\
&=\sum_{S\subseteq N\setminus\{i\}}\frac{v_{and}(S\cup\{i\})-v_{and}(S)}{2^{|N|-1}}
+\sum_{S\subseteq N\setminus\{i\}}\frac{v_{or}(N\setminus S)-v_{or}(N\setminus S\setminus\{i\})}{2^{|N|-1}}\\
&=\sum_{S\subseteq N\setminus\{i\}}\frac{v_{and}(S\cup\{i\})-v_{and}(S)}{2^{|N|-1}}
+\sum_{S\subseteq N\setminus\{i\}}\frac{v_{or}(S\cup\{i\})-v_{or}(S)}{2^{|N|-1}}\\
&=\sum_{S\subseteq N\setminus\{i\}}\frac{[v_{and}(S\cup\{i\})+v_{or}(S\cup\{i\})]-[v_{and}(S)+v_{or}(S)]}{2^{|N|-1}}\\
&=\sum_{S\subseteq N\setminus\{i\}}\frac{v(S\cup\{i\})-v(S)}{2^{|N|-1}}=B(i).
\end{aligned}
\]
The source comment in the fourth line asserts
\[
\sum_{\substack{S\subseteq N\setminus\{i\}\\S\supseteq L}}\frac{(-1)^{|S|}}{2^{|S|}}=\frac{(-1)^{|L|}}{2^{|N|-1}}.
\]
The last line gives the claimed reformulation.
'''
blocks['E']=r'''# Appendix E. Proof of Theorem 4 and Corollary 5

Source: official PDF pages 15–16. Main labels: Theorem 3.4 and Corollary 3.5. Put J(T)=I_and(T)+I_or(T) only as a shorthand for the exact repeated source bracket.

According to Theorem 2, φ_i=varphi(i)=∑_{T⊆N,i∈T}J(T)/|T|. According to Eq. (6), φ(S)=∑_{T⊇S}|S|J(T)/|T|. The complete calculation is
\[
\begin{aligned}
\sum_{i\in S}\varphi(i)
&=\sum_{i\in S}\sum_{T\subseteq N,T\ni i}\frac1{|T|}J(T)\\
&=\sum_{i\in S}\left[\sum_{T\subseteq N,T\supseteq S}\frac1{|T|}J(T)+\sum_{T\subseteq N,T\not\supseteq S,T\ni i}\frac1{|T|}J(T)\right]\\
&=\sum_{i\in S}\left[\frac1{|S|}\sum_{T\subseteq N,T\supseteq S}\frac{|S|}{|T|}J(T)+\sum_{T\subseteq N,T\not\supseteq S,T\ni i}\frac1{|T|}J(T)\right]\\
&=\sum_{i\in S}\left[\frac1{|S|}\phi(S)+\sum_{T\subseteq N,T\not\supseteq S,T\ni i}\frac1{|T|}J(T)\right]\\
&=\sum_{i\in S}\frac1{|S|}\phi(S)+\sum_{i\in S}\sum_{T\subseteq N,T\not\supseteq S,T\ni i}\frac1{|T|}J(T)\\
&=|S|\frac1{|S|}\phi(S)+\sum_{\substack{T\subseteq N\\T\cap S\ne\varnothing,\ T\cap S\ne S}}\frac{|T\cap S|}{|T|}J(T)\\
&=\phi(S)+\sum_{\substack{T\subseteq N\\T\cap S\ne\varnothing,\ T\cap S\ne S}}\frac{|T\cap S|}{|T|}J(T).
\end{aligned}
\]
The source explains that each J(T)/|T| is counted |T∩S| times. It does not discuss S=empty.

For Corollary 5 the original printed premise is
\[
\forall T\in\{T:S\not\subseteq T,\ T\subseteq N,\ i\in S\},\quad I_{and}(T)=I_{or}(T)=0.
\]
The free i is retained as printed. The source then obtains
\[
\sum_{i\in S}\varphi(i)=\phi(S)+\sum_{\substack{T\subseteq N\\T\cap S\ne\varnothing,\ T\cap S\ne S}}\frac{|T\cap S|}{|T|}J(T)=\phi(S),
\]
and, for the individual variable,
\[
\varphi(i)=\frac1{|S|}\phi(S)+\sum_{T\subseteq N,T\not\supseteq S,T\ni i}\frac1{|T|}J(T)=\frac1{|S|}\phi(S).
\]
This concludes both source results.
'''
blocks['F']=r'''# Appendix F. Proof of Theorem 6 and Corollary 7

Source: official PDF pages 16–17. Main labels: Theorem 3.6 and Corollary 3.7. J(T)=I_and(T)+I_or(T) is a shorthand for the repeated source bracket.

According to Theorem 3.2, varphi(i)=∑_{T⊆N,i∈T}J(T)/|T|. According to Eq. (6), φ(S)=∑_{T⊇S}|S|J(T)/|T|. For every i∈S,
\[
\begin{aligned}
\varphi(i)
&=\sum_{T\subseteq N,T\ni i}\frac1{|T|}J(T)\\
&=\sum_{T\subseteq N,T\supseteq S}\frac1{|T|}J(T)+\sum_{T\subseteq N,T\not\supseteq S,T\ni i}\frac1{|T|}J(T)\\
&=\frac1{|S|}\sum_{T\subseteq N,T\supseteq S}\frac{|S|}{|T|}J(T)+\sum_{T\subseteq N,T\not\supseteq S,T\ni i}\frac1{|T|}J(T)\\
&=\frac1{|S|}\phi(S)+\sum_{T\subseteq N,T\not\supseteq S,T\ni i}\frac1{|T|}J(T).
\end{aligned}
\]
For the corollary set S={i}:
\[
\begin{aligned}
\varphi(i)
&=\frac1{|S|}\phi(S)+\sum_{T\subseteq N,T\not\supseteq S,T\ni i}\frac1{|T|}J(T)\\
&=\frac11\phi(S)+\sum_{T\subseteq N,T\not\supseteq\{i\},T\ni i}\frac1{|T|}J(T)\\
&=\phi(S)=\phi(S=\{i\}).
\end{aligned}
\]
'''
blocks['G1']=r'''# Appendix G.1. Proof of Anonymity

Source: official PDF page 17. Original proof inference about the two components is retained.

The source lists
\[
\begin{aligned}
I_{and,v}(T)&=\sum_{L\subseteq T}(-1)^{|T|-|L|}v_{and}(L),&I_{or,v}(T)&=-\sum_{L\subseteq T}(-1)^{|T|-|L|}v_{or}(N\setminus L),\\
I_{and,\sigma v}(\sigma T)&=\sum_{L\subseteq\sigma T}(-1)^{|\sigma T|-|L|}(\sigma v_{and})(L),&
I_{or,\sigma v}(\sigma T)&=-\sum_{L\subseteq\sigma T}(-1)^{|\sigma T|-|L|}(\sigma v_{or})(N\setminus L).
\end{aligned}
\]
It claims that σv(σS)=v(S) implies σv_and(σS)=v_and(S) and σv_or(σS)=v_or(S). Its two complete change-of-variable chains are
\[
\begin{aligned}
I_{and,\sigma v}(\sigma T)
&=\sum_{L\subseteq\sigma T}(-1)^{|\sigma T|-|L|}(\sigma v_{and})(L)\\
&=\sum_{L=\sigma K\subseteq\sigma T}(-1)^{|\sigma T|-|\sigma K|}(\sigma v_{and})(\sigma K)\\
&=\sum_{L=\sigma K\subseteq\sigma T}(-1)^{|T|-|K|}v_{and}(K)
=\sum_{K\subseteq T}(-1)^{|T|-|K|}v_{and}(K)=I_{and,v}(T),\\
I_{or,\sigma v}(\sigma T)
&=-\sum_{L\subseteq\sigma T}(-1)^{|\sigma T|-|L|}(\sigma v_{or})(N\setminus L)\\
&=-\sum_{L=\sigma K\subseteq\sigma T}(-1)^{|\sigma T|-|\sigma K|}(\sigma v_{or})(N\setminus\sigma K)\\
&=-\sum_{L=\sigma K\subseteq\sigma T}(-1)^{|\sigma T|-|\sigma K|}(\sigma v_{or})(\sigma(N\setminus K))\\
&=-\sum_{L=\sigma K\subseteq\sigma T}(-1)^{|T|-|K|}v_{or}(N\setminus K)
=-\sum_{K\subseteq T}(-1)^{|T|-|K|}v_{or}(N\setminus K)=I_{or,v}(T).
\end{aligned}
\]
With J_v(T)=I_and,v(T)+I_or,v(T), Eq.(6) then gives
\[
\begin{aligned}
\phi_{\sigma v}(\sigma S)
&=\sum_{T\supseteq\sigma S}\frac{|\sigma S|}{|T|}J_{\sigma v}(T)\\
&=\sum_{T=\sigma L\supseteq\sigma S}\frac{|\sigma S|}{|\sigma L|}[I_{and,\sigma v}(\sigma L)+I_{or,\sigma v}(\sigma L)]\\
&=\sum_{T=\sigma L\supseteq\sigma S}\frac{|S|}{|L|}[I_{and,v}(L)+I_{or,v}(L)]\\
&=\sum_{L\supseteq S}\frac{|S|}{|L|}[I_{and,v}(L)+I_{or,v}(L)]=\phi_v(S).
\end{aligned}
\]
'''
blocks['G2']=r'''# Appendix G.2. Proof of Symmetry α

Source: official PDF pages 18–19. The unsupported transfer of total-game symmetry to each component is retained.

The source defines, for k=i,j,
\[
I_{and}(T\cup\{k\})=\sum_{L\subseteq T\cup\{k\}}(-1)^{|T\cup\{k\}|-|L|}v_{and}(L),\quad
I_{or}(T\cup\{k\})=-\sum_{L\subseteq T\cup\{k\}}(-1)^{|T\cup\{k\}|-|L|}v_{or}(N\setminus L).
\]
It then claims that equality v(U∪{i})=v(U∪{j}) for all U⊆N\{i,j} gives the same equalities for v_and and v_or. The full interaction-difference chains are
\[
\begin{aligned}
I_{and}(T\cup\{i\})-I_{and}(T\cup\{j\})
&=\sum_{L\subseteq T\cup\{i\}}(-1)^{|T\cup\{i\}|-|L|}v_{and}(L)-\sum_{L\subseteq T\cup\{j\}}(-1)^{|T\cup\{j\}|-|L|}v_{and}(L)\\
&=\left[\sum_{L\subseteq T}(-1)^{|T\cup\{i\}|-|L|}v_{and}(L)+\sum_{L\subseteq T}(-1)^{|T\cup\{i\}|-|L\cup\{i\}|}v_{and}(L\cup\{i\})\right]\\
&\quad-\left[\sum_{L\subseteq T}(-1)^{|T\cup\{j\}|-|L|}v_{and}(L)+\sum_{L\subseteq T}(-1)^{|T\cup\{j\}|-|L\cup\{j\}|}v_{and}(L\cup\{j\})\right]\\
&=\sum_{L\subseteq T}(-1)^{|T|-|L|}[v_{and}(L\cup\{i\})-v_{and}(L\cup\{j\})]=0,\\
I_{or}(T\cup\{i\})-I_{or}(T\cup\{j\})
&=-\sum_{L\subseteq T\cup\{i\}}(-1)^{|T\cup\{i\}|-|L|}v_{or}(N\setminus L)+\sum_{L\subseteq T\cup\{j\}}(-1)^{|T\cup\{j\}|-|L|}v_{or}(N\setminus L)\\
&=\left[\sum_{L\subseteq T}(-1)^{|T\cup\{j\}|-|L|}v_{or}(N\setminus L)+\sum_{L\subseteq T}(-1)^{|T\cup\{j\}|-|L\cup\{j\}|}v_{or}(N\setminus(L\cup\{j\}))\right]\\
&\quad-\left[\sum_{L\subseteq T}(-1)^{|T\cup\{i\}|-|L|}v_{or}(N\setminus L)+\sum_{L\subseteq T}(-1)^{|T\cup\{i\}|-|L\cup\{i\}|}v_{or}(N\setminus(L\cup\{i\}))\right]\\
&=\sum_{L\subseteq T}(-1)^{|T|-|L|}[v_{or}((N\setminus(L\cup\{i,j\}))\cup\{i\})-v_{or}((N\setminus(L\cup\{i,j\}))\cup\{j\})]=0.
\end{aligned}
\]
Let J(T)=I_and(T)+I_or(T). The complete attribution-difference chain is
\[
\begin{aligned}
\phi(S\cup\{i\})-\phi(S\cup\{j\})
&=\sum_{T\supseteq S\cup\{i\}}\frac{|S\cup\{i\}|}{|T|}J(T)-\sum_{T\supseteq S\cup\{j\}}\frac{|S\cup\{j\}|}{|T|}J(T)\\
&=\left[\sum_{T\supseteq S\cup\{i,j\}}\frac{|S|+1}{|T|}J(T)+\sum_{T\supseteq S\cup\{i\},j\notin T}\frac{|S|+1}{|T|}J(T)\right]\\
&\quad-\left[\sum_{T\supseteq S\cup\{i,j\}}\frac{|S|+1}{|T|}J(T)+\sum_{T\supseteq S\cup\{j\},i\notin T}\frac{|S|+1}{|T|}J(T)\right]\\
&=\sum_{T\supseteq S\cup\{i\},j\notin T}\frac{|S|+1}{|T|}J(T)-\sum_{T\supseteq S\cup\{j\},i\notin T}\frac{|S|+1}{|T|}J(T)\\
&=\sum_{\substack{T\supseteq S\\T\subseteq N\setminus\{i,j\}}}\frac{|S|+1}{|T\cup\{i\}|}J(T\cup\{i\})-\sum_{\substack{T\supseteq S\\T\subseteq N\setminus\{i,j\}}}\frac{|S|+1}{|T\cup\{j\}|}J(T\cup\{j\})\\
&=\sum_{\substack{T\supseteq S\\T\subseteq N\setminus\{i,j\}}}\frac{|S|+1}{|T|+1}\left[(I_{and}(T\cup\{i\})-I_{and}(T\cup\{j\}))+(I_{or}(T\cup\{i\})-I_{or}(T\cup\{j\}))\right]=0.
\end{aligned}
\]
The source concludes φ(S∪{i})=φ(S∪{j}).
'''
blocks['G3']=r'''# Appendix G.3. Proof of Symmetry β

Source: official PDF pages 19–20. This transcription deliberately preserves the printed ∈ indexing of subsets, the |L| in several OR exponents, the unproved disjointness reduction, and the all-equal-cardinality pairing. They are not repaired in this field.

The source begins: “Without loss of generality, we assume S∩T=∅.” For every K⊇L, K⊆N\(S∪T), T′⊆T with T′≠T, S′⊆S with S′≠S and |S′|=|T′|, put X=K∪S∪T′ and Y=K∪S′∪T. The four printed definitions are
\[
I_{and}(X)=\sum_{J\subseteq X}(-1)^{|X|-|J|}v_{and}(J),\quad
I_{or}(X)=-\sum_{J\subseteq X}(-1)^{|X|-|L|}v_{or}(N\setminus J),
\]
\[
I_{and}(Y)=\sum_{J\subseteq Y}(-1)^{|Y|-|J|}v_{and}(J),\quad
I_{or}(Y)=-\sum_{J\subseteq Y}(-1)^{|Y|-|L|}v_{or}(N\setminus J).
\]
The complete AND-difference calculation is
\[
\begin{aligned}
I_{and}(X)-I_{and}(Y)
&=\sum_{J\subseteq X}(-1)^{|X|-|J|}v_{and}(J)-\sum_{J\subseteq Y}(-1)^{|Y|-|J|}v_{and}(J)\\
&=\sum_{J\subseteq K\cup S'\cup T'}\left[
\sum_{\substack{A\in S\setminus S'\\A\ne S\setminus S'}}(-1)^{|X|-|J\cup A|}v_{and}(J\cup A)
-\sum_{\substack{B\in T\setminus T'\\B\ne T\setminus T'}}(-1)^{|Y|-|J\cup B|}v_{and}(J\cup B)\right]\\
&=\sum_{J\subseteq K\cup S'\cup T'}\sum_{\substack{A\in S\setminus S',\ A\ne S\setminus S'\\ B\in T\setminus T',\ B\ne T\setminus T'\\|A|=|B|}}
(-1)^{|Y|-|J\cup B|}[v_{and}(J\cup A)-v_{and}(J\cup B)]\\
&=0.
\end{aligned}
\]
The complete OR-difference calculation is
\[
\begin{aligned}
I_{or}(X)-I_{or}(Y)
&=-\sum_{J\subseteq X}(-1)^{|X|-|L|}v_{or}(N\setminus J)+\sum_{J\subseteq Y}(-1)^{|Y|-|L|}v_{or}(N\setminus J)\\
&=\sum_{J\subseteq K\cup S'\cup T'}\left[
\sum_{\substack{B\in T\setminus T'\\B\ne T\setminus T'}}(-1)^{|Y|-|J\cup B|}v_{or}(N\setminus(J\cup B))
-\sum_{\substack{A\in S\setminus S'\\A\ne S\setminus S'}}(-1)^{|X|-|J\cup A|}v_{or}(N\setminus(J\cup A))\right]\\
&=\sum_{J\subseteq K\cup S'\cup T'}\sum_{\substack{A\in S\setminus S',\ A\ne S\setminus S'\\B\in T\setminus T',\ B\ne T\setminus T'\\|A|=|B|}}
(-1)^{|Y|-|J\cup B|}[v_{or}(N\setminus(J\cup B))-v_{or}(N\setminus(J\cup A))]\\
&=\sum_{J\subseteq K\cup S'\cup T'}\sum_{\substack{A\in S\setminus S',\ A\ne S\setminus S'\\B\in T\setminus T',\ B\ne T\setminus T'\\|A|=|B|}}
(-1)^{|Y|-|J\cup B|}[v_{or}((N\setminus(J\cup A\cup B))\cup A)-v_{or}((N\setminus(J\cup A\cup B))\cup B)]\\
&=\sum_{J\subseteq K\cup S'\cup T'}\sum_{\substack{A\in S\setminus S',\ A\ne S\setminus S'\\B\in T\setminus T',\ B\ne T\setminus T'\\|A|=|B|}}0=0.
\end{aligned}
\]
Now J_effect(U)=I_and(U)+I_or(U) is a distinct shorthand for the repeated source bracket, not the earlier subset variable J. Eq. (6) gives φ(L∪S) and φ(L∪T). The page-20 chain is
\[
\begin{aligned}
\phi(L\cup S)-\phi(L\cup T)
&=\sum_{K\supseteq L\cup S}\frac{|L\cup S|}{|K|}J_{effect}(K)-\sum_{K\supseteq L\cup T}\frac{|L\cup T|}{|K|}J_{effect}(K)\\
&=\left[\sum_{K\supseteq L\cup S\cup T}\frac{|L\cup S|}{|K|}J_{effect}(K)+\sum_{K\supseteq L\cup S,K\not\supseteq T}\frac{|L\cup S|}{|K|}J_{effect}(K)\right]\\
&\quad-\left[\sum_{K\supseteq L\cup S\cup T}\frac{|L\cup T|}{|K|}J_{effect}(K)+\sum_{K\supseteq L\cup T,K\not\supseteq S}\frac{|L\cup T|}{|K|}J_{effect}(K)\right]\\
&=\sum_{K\supseteq L\cup S,K\not\supseteq T}\frac{|L\cup S|}{|K|}J_{effect}(K)-\sum_{K\supseteq L\cup T,K\not\supseteq S}\frac{|L\cup T|}{|K|}J_{effect}(K)\\
&=\sum_{\substack{K\supseteq L\\K\subseteq N\setminus(S\cup T)}}\sum_{T'\subseteq T,T'\ne T}\frac{|L\cup S|}{|K\cup S\cup T'|}J_{effect}(K\cup S\cup T')\\
&\quad-\sum_{\substack{K\supseteq L\\K\subseteq N\setminus(S\cup T)}}\sum_{S'\subseteq S,S'\ne S}\frac{|L\cup T|}{|K\cup S'\cup T|}J_{effect}(K\cup S'\cup T)\\
&=\sum_{\substack{K\supseteq L\\K\subseteq N\setminus(S\cup T)}}\sum_{\substack{T'\subseteq T,T'\ne T\\S'\subseteq S,S'\ne S\\|S'|=|T'|}}\frac{|L\cup T|}{|K\cup S'\cup T|}
\left[I_{and}(K\cup S\cup T')-I_{and}(K\cup S'\cup T)+I_{or}(K\cup S\cup T')-I_{or}(K\cup S'\cup T)\right]\\
&=0.
\end{aligned}
\]
The source concludes the symmetry-β axiom. The change from separate sums to an all-pairs sum is preserved as printed, even though it is not a bijective reindexing.
'''
blocks['G4']=r'''# Appendix G.4. Proof of Additivity

Source: official PDF page 20. The original unsupported inference is retained.

For k absent,1,2, the source separately lists the six definitions
\[
\begin{aligned}
I_{and,v}(T)&=\sum_{L\subseteq T}(-1)^{|T|-|L|}v_{and}(L),& I_{or,v}(T)&=-\sum_{L\subseteq T}(-1)^{|T|-|L|}v_{or}(N\setminus L),\\
I_{and,v_1}(T)&=\sum_{L\subseteq T}(-1)^{|T|-|L|}v_{and,1}(L),& I_{or,v_1}(T)&=-\sum_{L\subseteq T}(-1)^{|T|-|L|}v_{or,1}(N\setminus L),\\
I_{and,v_2}(T)&=\sum_{L\subseteq T}(-1)^{|T|-|L|}v_{and,2}(L),& I_{or,v_2}(T)&=-\sum_{L\subseteq T}(-1)^{|T|-|L|}v_{or,2}(N\setminus L).
\end{aligned}
\]
Here v=v_and+v_or, v₁=v_and,1+v_or,1 and v₂=v_and,2+v_or,2. It claims from v=v₁+v₂ that I_and,v=I_and,v₁+I_and,v₂ and I_or,v=I_or,v₁+I_or,v₂. It then lists Eq. (6) for each of the three games and calculates
\[
\begin{aligned}
\phi_v(S)
&=\sum_{T\supseteq S}\frac{|S|}{|T|}[I_{and,v}(T)+I_{or,v}(T)]\\
&=\sum_{T\supseteq S}\frac{|S|}{|T|}[(I_{and,v_1}(T)+I_{and,v_2}(T))+(I_{or,v_1}(T)+I_{or,v_2}(T))]\\
&=\sum_{T\supseteq S}\frac{|S|}{|T|}[I_{and,v_1}(T)+I_{or,v_1}(T)]
+\sum_{T\supseteq S}\frac{|S|}{|T|}[I_{and,v_2}(T)+I_{or,v_2}(T)]\\
&=\phi_{v_1}(S)+\phi_{v_2}(S).
\end{aligned}
\]
'''
blocks['G5']=r'''# Appendix G.5. Proof of Dummy

Source: official PDF page 21. The first AND summand is printed v_and(T), not v_and(L); this source typo is retained. The unsupported component-dummy inference is also retained.

For every T containing i the source writes
\[
\begin{aligned}
I_{and}(T)&=\sum_{L\subseteq T}(-1)^{|T|-|L|}v_{and}(T)
=\sum_{L\subseteq T\setminus\{i\}}(-1)^{|T|-|L|+1}[v_{and}(L\cup\{i\})-v_{and}(L)],\\
I_{or}(T)&=-\sum_{L\subseteq T}(-1)^{|T|-|L|}v_{or}(N\setminus L)
=\sum_{L\subseteq T\setminus\{i\}}(-1)^{|T|-|L|+1}[v_{or}(N\setminus L)-v_{or}(N\setminus L\setminus\{i\})].
\end{aligned}
\]
It asserts that for every U⊆N\{i}, v(U∪{i})=v(U) implies both v_and(U∪{i})=v_and(U) and v_or(U∪{i})=v_or(U). It therefore calculates
\[
I_{and}(T)=\sum_{L\subseteq T\setminus\{i\}}(-1)^{|T|-|L|+1}[v_{and}(L\cup\{i\})-v_{and}(L)]=0,
\]
\[
I_{or}(T)=\sum_{L\subseteq T\setminus\{i\}}(-1)^{|T|-|L|+1}[v_{or}(N\setminus L)-v_{or}(N\setminus L\setminus\{i\})]=0.
\]
Eq. (6) finally gives
\[
\phi(S)=\sum_{T\supseteq S}\frac{|S|}{|T|}[I_{and}(T)+I_{or}(T)]
=\sum_{T\supseteq S,T\ni i}\frac{|S|}{|T|}[I_{and}(T)+I_{or}(T)]=0.
\]
'''
blocks['G6']=r'''# Appendix G.6. Proof of Corollary 8

Source: official PDF page 21. Main label: Corollary 3.8. J(T)=I_and(T)+I_or(T) abbreviates the repeated source bracket.

Shapley efficiency gives v(N)−v(empty)=∑_{i∈N}varphi(i). Theorem 4 gives the coalition/conflict decomposition. The complete calculation is
\[
\begin{aligned}
v(N)-v(\varnothing)
&=\sum_{i\in N}\varphi(i)\\
&=\sum_{i\in S}\varphi(i)+\sum_{i\in N\setminus S}\varphi(i)\\
&=\phi(S)+\sum_{i\in N\setminus S}\varphi(i)
+\sum_{\substack{T\subseteq N\\T\cap S\ne\varnothing,T\cap S\ne S}}\frac{|T\cap S|}{|T|}[I_{and}(T)+I_{or}(T)].
\end{aligned}
\]
'''
for k,v in blocks.items():(B/(k+'.md')).write_text(v+'\n')
path=D/'content.json';x=json.loads(path.read_text());mapping={'shapley':'C','banzhaf':'D','conflict':'E','no-conflict':'E','individual':'F','singleton':'F','anonymity':'G1','symmetry-alpha':'G2','symmetry-beta':'G3','additivity':'G4','dummy':'G5','efficiency':'G6'}
for r in x['results']:
 key=r['id'].removeprefix('coalition-')
 if key in mapping:
  b=mapping[key];r['original_proof_md']=blocks[b];r['original_proof_path']=str(B/(b+'.md'));r['original_proof_source_type']='complete_author_mathematical_proof_transcription';r['original_proof_note']='完整作者数学推导逐式转录；英语论证文字按原语义重述，原错域、错指标和非法推断保留；不是项目修正证明。';r['translations']['en']['original_proof_md']=blocks[b];r['translations']['en']['original_proof_note']='Complete author mathematical calculation, equation by equation. English connective prose is restated faithfully; the source errors remain. This is distinct from the project repair.'
  r['source_transcription_status']='complete_mathematical_transcription'
 elif key in ['shapley-coefficient','banzhaf-coefficient']:
  r['original_proof_source_type']='no_separate_author_proof';r['original_proof_md']='原作者使用该恒等式而没有单独证明；它的完整原计算出现于 '+str(B/('C.md' if key=='shapley-coefficient' else 'D.md'))+'。';r['translations']['en']['original_proof_md']='The author uses this identity without a separate proof. Its full calculation occurrence is preserved in '+str(B/('C.md' if key=='shapley-coefficient' else 'D.md'))+'.'
path.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
print('Full source calculation blocks',len(blocks))
