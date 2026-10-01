Appendix C, physical PDF page 13. Complete mathematical argument as printed, including the two coordinate definitions and the subsequent sparsity inference.

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
The concluding paragraph states that this equality transfers the proven AND sparsity of Ren et al. (2024) to OR sparsity, so most well-trained DNNs encode only a small number of OR interactions. The printed Eq.(12) is the ordinary original mask, not the coordinate-swapped mask needed for the second equality. That equality and the unsupported transfer of sparsity assumptions are treated as separate issues.
