Lemma 1, Appendix C, physical PDF pages 14–15. Complete author mathematical proof transcription. The missing centered-baseline term in the printed recurrence and the source's induction statements are retained.

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

The complete source has no empty-field exclusion and no proof of $z(x_\varnothing)=0$ from R1/R2. That boundary makes the lemma false as stated; its counterexample is recorded separately.
