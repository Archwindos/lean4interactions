F.8, formal PDF page 19. Complete author mathematical construction and displayed chain, with the original symbols preserved.

To reduce computational cost, the authors randomly sampled $n=12$ foreground variables as input variables on image datasets. Ground-truth Shapley values were computed by masking the selected twelve variables and keeping all other variables at their original sample values. The selected set is denoted $\widehat N$, with $|\widehat N|=12$. Specifically, the baseline is set by
\[
\forall i\notin\widehat N,\ b_i=x_i,\qquad\forall i\in\widehat N,\ b_i=0.
\]
Based on this baseline sample, the authors obtained $2^{|\widehat N|}$ different masked samples. For HarsanyiNet they computed the Shapley values for the selected variables based on Theorem 1, visiting sets containing a selected variable, written $S\ni i,\ \forall i\in\widehat N$. The source explicitly says that $|S|$ denotes the number of selected variables in $S$. Its displayed construction is
\[
\varphi(i)=\sum_{S\subseteq N:\,S\ni i,\,i\in\widehat N}\frac{1}{|S|}I(S),
\qquad\sum_{i=1}^{n}\varphi(i)=v(x_N=x)-v(x_\varnothing).
\]
For the ShapNets comparison, the authors instead set each unselected variable's baseline to zero, producing $x'_i=x_i$ for $i\in\widehat N$ and $x'_i=0$ otherwise, and computed the selected-variable attributions of ShapNet on this masked input sample. This different comparison construction is preserved rather than conflated with the preceding conditional game.
