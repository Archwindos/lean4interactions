Appendix F, physical PDF page 15. Complete author mathematical proof transcription of Theorem 3.3; errors are retained. Equation numbers refer to the formal PDF.

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
The author concludes the theorem. The fixed original-game values in the source expansion and its $x_T$ coefficient labels are independently distinguished in the project rewrite.
