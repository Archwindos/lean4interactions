Let the above auto-encoder be trained to convergence. Then, we computed the Pearson's correlation coefficient between each random pair of variables $|\Delta T_{d_1c_1}^{(l,uv)}|$ and $|\Delta T_{d_2c_2}^{(l,uv)}|$ through different images, denoted by $r(|\Delta T_{d_1c_1}^{(l,uv)}|,|\Delta T_{d_2c_2}^{(l,uv)}|)$, to measure the relevance between two elements $T_{d_1c_1}^{(l,uv)}$ and $T_{d_2c_2}^{(l,uv)}$ in $T^{(l,uv)}$. Here, $\Delta T^{(l,uv)}$ denoted the change of $T^{(l,uv)}$ when we updated parameters $\mathbf W$ for a single gradient-descent step on a single input sample. Results in Table 1 show that even when the network was fully trained, different elements in $T^{(l,uv)}$ had low Pearson's correlation coefficient $r$. This proved that our assumption that all elements in $T^{(l,uv)}$ were irrelevant to each other was reasonable. The last three convolutional layers in the decoder showed a larger Pearson's correlation coefficient, because network parameters close to the output layer had been converged to the principle feature direction of each category. Nevertheless, our experiments showed that for most layers, we could keep Assumption 4.1, which enabled to us to prove that convolution operations in these layers weakened high-frequency components.

Table 1. Pearson's correlation coefficient between each random pair of variables $|\Delta T_{d_1c_1}^{(l,uv)}|$ and $|\Delta T_{d_2c_2}^{(l,uv)}|$ through different images.

$$\begin{array}{c|c}
\text{Depth of the decoder network}&\mathbb E_{u,v,d_1,c_1,d_2,c_2}\!\left[r\!\left(|\Delta T_{d_1c_1}^{(l,uv)}|,|\Delta T_{d_2c_2}^{(l,uv)}|\right)\right]\\\hline
1&0.011\\
2&-0.002\\
3&0.018\\
4&-0.001\\
5&-0.013\\
6&0.026\\
7&0.018
\end{array}$$
