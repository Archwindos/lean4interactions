Understanding the cascaded convolution operations in the frequency domain. Corollary 3.3 means that conducting multiple cascaded convolution operations on an input $x$ is essentially equivalent to conducting matrix multiplication on spectrums of $x$. As Figure 2 shows, for all frequencies except for the fundamental frequency, we have the output spectrum $\mathbf h^{(uv)}=\mathbb T^{(uv)(L:1)}\mathbf g^{(uv)}$.

Besides, the learning of parameters $\mathbf W^{(l)}$ affects the matrix $T^{(l,uv)}$. Therefore, we further reformulate the change of $T^{(l,uv)}$ during the learning process, as follows.

In this section, we prove Corollary 3.3 in Section 3 of the main paper, as follows.

Proof. Let $\mathbf G^{(l)}=[G^{(l,1)},G^{(l,2)},\cdots,G^{(l,C_l)}]\in\mathbb C^{C_l\times M\times N}$ denote feature spectrums of the $l$-th layer. Let $\mathbf g^{(l,uv)}=[G^{(l,1)}_{uv},G^{(l,2)}_{uv},\cdots,G^{(l,C_l)}_{uv}]^\top\in\mathbb C^{C_l}$ denote the frequency component at the frequency $[u,v]$. When $l=0$, $\mathbf g^{(0,uv)}$ denotes the frequency component of the input sample. When $l=L$, $\mathbf g^{(L,uv)}$ denotes the frequency component of the network output. Based on Theorem 3.2, $\mathbf g^{(l,uv)}$ can be computed as follows.

$$\forall l=1,2,\ldots,L,\qquad \mathbf g^{(l,uv)}=T^{(l,uv)}\mathbf g^{(l-1,uv)}+\delta_{uv}MN\mathbf b^{(l)}.$$

Then, the frequency component $\mathbf g^{(L,uv)}$ of the network output can be computed as follows.

$$\begin{aligned}
\mathbf g^{(L,uv)}&=T^{(L,uv)}\mathbf g^{(L-1,uv)}+\delta_{uv}MN\mathbf b^{(L)}\\
&=T^{(L,uv)}\left(T^{(L-1,uv)}\mathbf g^{(L-2,uv)}+\delta_{uv}MN\mathbf b^{(L-1)}\right)+\delta_{uv}MN\mathbf b^{(L)}\\
&=T^{(L,uv)}T^{(L-1,uv)}\mathbf g^{(L-2,uv)}+T^{(L,uv)}\delta_{uv}MN\mathbf b^{(L-1)}+\delta_{uv}MN\mathbf b^{(L)}\\
&=\cdots\\
&=T_{dc}^{(l,uv)}\cdots T^{(1,uv)}\mathbf g^{(0,uv)}+MNT_{dc}^{(l,uv)}\cdots T^{(2,uv)}\mathbf b^{(1)}\delta_{uv}+\cdots+MN\mathbf b^{(L)}\delta_{uv}\\
&=T_{dc}^{(l,uv)}\cdots T^{(1,uv)}\mathbf g^{(0,uv)}+\delta_{uv}MN\left(T_{dc}^{(l,uv)}\cdots T^{(2,uv)}\mathbf b^{(1)}+\cdots+MN\mathbf b^{(L)}\right).
\end{aligned}$$

Let $\mathbb T^{(uv)(L:1)}=T_{dc}^{(l,uv)}\cdots T^{(2,uv)}T^{(1,uv)}$ and $\boldsymbol\beta=MN\left(\mathbf b^{(L)}+\sum_{j=2}^{L}\mathbb T^{(00)(L:j)}\mathbf b^{(j-1)}\right)$. Let $\mathbf h^{(uv)}=\mathbf g^{(L,uv)}$ denote the frequency component of the network output, and let $\mathbf g^{(uv)}=\mathbf g^{(0,uv)}$ denote the frequency component of the input sample. Then, we prove that $\mathbf h^{(uv)}$ can be computed as follows.

$$\mathbf h^{(uv)}=\mathbb T^{(uv)(L:1)}\mathbf g^{(uv)}+\delta_{uv}\boldsymbol\beta.$$
