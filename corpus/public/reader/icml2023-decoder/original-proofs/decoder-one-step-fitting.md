In this section, we prove Theorem 4.5 in the main paper. Recall that we consider the input $x\in\mathbb R^{M\times N}$ with a single channel to simplify the proof. Then, $G\in\mathbb C^{M\times N}$, $H\in\mathbb C^{M\times N}$, and $H^*\in\mathbb C^{M\times N}$ denote spectrums of the input, the output, and the target image to fit, respectively. Specifically, $H^*_{u_1v_1}=(1-A)G^{(u_1v_1)}$, and $H^*_{u_2v_2}=(1+\overline A)G^{(u_2v_2)}$, where $A=\alpha e^{i\phi}$ and $\overline A$ denotes the conjugate of $A$; $\alpha>0$; $\phi<\pi/2$. Theorem 4.5 proves a case that weights $\mathbf W$ is optimized to satisfy $H_{u_1v_1}=H^*_{u_1v_1}$ and $H_{u_2v_2}=H^*_{u_2v_2}$ simultaneously.

Proof. Let us provide specific constrains as follows, so as to make the auto-encoder learnable (i.e., ensuring $\Delta\mathbf W$ is real-valued) and make the objective function can reach zero by a single step of gradient descent.

$$\lambda_1=\frac1{|G_{u_1v_1}|^2};\qquad\lambda_2=\frac1{|G_{u_2v_2}|^2}.\tag{43}$$

$$A=\alpha e^{i\phi},\qquad\text{s.t. }\phi=\left(\frac{(K-1)(u_2-u_1)}M+\frac{(K-1)(v_2-v_1)}N\right)\frac\pi2.\tag{44}$$

$$\mathbb T^{(u_2v_2)(L:1)}=\mathbb T^{(u_1v_1)(L:1)}=1.\tag{45}$$

$$\sum_{l=1}^L\|\mathbb T^{(u_1v_1)(L:l+1)}\|^2\|\mathbb T^{(u_1v_1)(l-1:1)}\|^2=\sum_{l=1}^L\|\mathbb T^{(u_2v_2)(L:l+1)}\|^2\|\mathbb T^{(u_2v_2)(l-1:1)}\|^2.\tag{46}$$

If the objective function can reach zero (i.e., $H_{u_1v_1}=H^*_{u_1v_1}$ and $H_{u_2v_2}=H^*_{u_2v_2}$) by a single step of gradient descent, the change of weights $\Delta\mathbf W$ can be rewritten as $\eta\frac{Loss}{\partial\mathbf W}$, where $\eta$ denotes the learning rate, $\frac{Loss}{\partial\mathbf W}$ denotes the gradient on weights. Then, we will prove the formulations of $\eta$ and $\|\frac{Loss}{\partial\mathbf W}\|$.

According to Corollary 3.3, the network output $H_{uv}$ can be computed as follows.

$$H_{uv}=\mathbb T^{(uv)(L:1)}G_{uv},\tag{47}$$

where $\mathbb T^{(uv)(L:1)}=T^{(L,uv)}T^{(L-1,uv)}\cdots T^{(1,uv)}\in\mathbb C^{1\times1}$.

According to Corollary 3.4, after a single step of gradient descent, the change of $\mathbb T^{(uv)(L:1)}$ can be computed as follows.

$$\begin{aligned}
\Delta\mathbb T^{(uv)(L:1)}
&=\Delta(T^{(L,uv)}T^{(L-1,uv)}\cdots T^{(1,uv)})\\
&\approx\sum_{l=1}^L\mathbb T^{(L:l+1)(uv)}\Delta T^{(l,uv)}\mathbb T^{(l-1:1)(uv)}\quad\text{//First order approximation}\\
&=-\eta MN\sum_{l=1}^L\mathbb T^{(L:l+1)(uv)}\left(\sum_{u'v'}\chi_{u'v'uv}\overline{\mathbb T}^{(l-1:1)(uv)}\overline G_{uv}\frac{\partial Loss}{\partial\overline H^T_{uv}}\overline{\mathbb T}^{(L:l-1)(uv)}\right)^T\mathbb T^{(l-1:1)(uv)}\\
&=-2\eta MN\left(\lambda_1\chi_{u_1v_1uv}\overline G_{u_1v_1}(H_{u_1v_1}-H^*_{u_1v_1})+\lambda_2\chi_{u_2v_2uv}\overline G_{u_2v_2}(H_{u_2v_2}-H^*_{u_2v_2})\right)\sum_{l=1}^L\|\mathbb T^{(L:l+1)(uv)}\|^2\|\mathbb T^{(l-1:1)(uv)}\|^2\\
&=-2\eta MN\left(\chi_{u_1v_1uv}\left(\mathbb T^{(L:1)(u_1v_1)}-\frac{H^*_{u_1v_1}}{G_{u_1v_1}}\right)+\chi_{u_2v_2uv}\left(\mathbb T^{(L:1)(u_2v_2)}-\frac{H^*_{u_2v_2}}{G_{u_2v_2}}\right)\right)\sum_{l=1}^L\|\mathbb T^{(L:l+1)(uv)}\|^2\|\mathbb T^{(l-1:1)(uv)}\|^2\quad\text{//According to Equation (43)}\\
&=-2\eta MN(A\chi_{u_1v_1uv}-\overline A\chi_{u_2v_2uv})\sum_{l=1}^L\|\mathbb T^{(L:l+1)(uv)}\|^2\|\mathbb T^{(l-1:1)(uv)}\|^2\quad\text{//Equation (45)}.
\end{aligned}\tag{48}$$

For frequencies $[u_1,v_1]$ and $[u_2,v_2]$, we have:

$$\Delta\mathbb T^{(L:1)(u_1v_1)}=-2\eta MN(A\chi_{u_1v_1u_1v_1}-\overline A\chi_{u_2v_2u_1v_1})\sum_{l=1}^L\|\mathbb T^{(L:l+1)(u_1v_1)}\|^2\|\mathbb T^{(l-1:1)(u_1v_1)}\|^2.\tag{49}$$

$$\Delta\mathbb T^{(L:1)(u_2v_2)}=-2\eta MN(A\chi_{u_1v_1u_2v_2}-\overline A\chi_{u_2v_2u_2v_2})\sum_{l=1}^L\|\mathbb T^{(L:l+1)(u_2v_2)}\|^2\|\mathbb T^{(l-1:1)(u_2v_2)}\|^2.\tag{50}$$


