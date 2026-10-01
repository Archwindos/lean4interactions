Similarly, the upper bound for the mutual information w.r.t the output $Y$ can be calculated as

$$\begin{aligned}
I(\widehat T;Y)&=H(\widehat T)-H(\widehat T\mid Y)\\
&=-\frac1P\sum_i\log\frac1P\sum_j\exp\left(-\frac12\frac{\|t_i-t_j\|^2}{\sigma_0^2}\right)\\
&\quad-\sum_{l=1}^L p_l\left[-\frac1P\sum_{i:Y_i=l}\log\frac1P\sum_{j:Y_j=l}\exp\left(-\frac12\frac{\|t_i-t_j\|^2}{\sigma_0^2}\right)\right].
\end{aligned}\tag{24}$$

where $L$ is the number of categories. $P_l$ denotes the number of samples belonging to the $l$-th category. $p_l=P_l/P$ denotes the probability of the category $l$.
