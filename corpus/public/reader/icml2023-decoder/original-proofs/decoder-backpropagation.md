In this section, we prove Corollary 3.4 in Section 3 of the main paper, as follows.

Proof. **First, we focus on a single convolutional layer.**

According to the DFT and the inverse DFT, we can obtain the mathematical relationship between $G^{(l,c)}_{uv}$ and $F^{(l,c)}_{mn}$, and the mathematical relationship between $T^{(l,uv)}_{dc}$ and $W^{(l)[\mathrm{ker}=d]}_{cts}$, as follows.

$$\begin{gathered}
\left\{\begin{aligned}
G^{(l,c)}_{uv}&=\sum_{m=0}^{M-1}\sum_{n=0}^{N-1}F^{(l,c)}_{mn}e^{-i(um/M+vn/N)2\pi},\\
F^{(l,c)}_{mn}&=\frac1{MN}\sum_{u=0}^{M-1}\sum_{v=0}^{N-1}G^{(l,c)}_{uv}e^{i(um/M+vn/N)2\pi};
\end{aligned}\right.\\
\left\{\begin{aligned}
T^{(l,uv)}_{dc}&=\sum_{t=0}^{K-1}\sum_{s=0}^{K-1}W^{(l)[\mathrm{ker}=d]}_{cts}e^{i(ut/M+vs/N)2\pi},\\
W^{(l)[\mathrm{ker}=d]}_{cts}&=\frac1{MN}\sum_{u=0}^{M-1}\sum_{v=0}^{N-1}T^{(l,uv)}_{dc}e^{-i(ut/M+vs/N)2\pi}.
\end{aligned}\right.
\end{gathered}\tag{19}$$

Based on Equation (19) and the derivation rule for complex numbers (Kreutz-Delgado, 2009), we can obtain the mathematical relationship between $\frac{\partial Loss}{\partial\overline G^{(l,c)}_{uv}}$ and $\frac{\partial Loss}{\partial\overline F^{(l,c)}_{mn}}$, and the mathematical relationship between $\frac{\partial Loss}{\partial\overline T^{(l,uv)}_{dc}}$ and $\frac{\partial Loss}{\partial\overline W^{(l)[\mathrm{ker}=d]}_{cts}}$, as follows. Note that when we use gradient descent to optimize a real-valued loss function $Loss$ with complex variables, people usually treat the real and imaginary values, $a\in\mathbb C$ and $b\in\mathbb C$, of a complex variable $(z=a+bi)$ as two separate real-valued variables, and separately update these two real-valued variables. In this way, the exact optimization step of $z$ computed based on such a technology is equivalent to $\frac{\partial Loss}{\partial\overline z}$. Since $F^{(l,c)}_{mn}$ and $W^{(l)[\mathrm{ker}=d]}_{cts}$ are real numbers, $\frac{\partial Loss}{\partial\overline F^{(l,c)}_{mn}}=\frac{\partial Loss}{\partial F^{(l,c)}_{mn}}$ and $\frac{\partial Loss}{\partial\overline W^{(l)[\mathrm{ker}=d]}_{cts}}=\frac{\partial Loss}{\partial W^{(l)[\mathrm{ker}=d]}_{cts}}$.

$$\begin{gathered}
\left\{\begin{aligned}
\frac{\partial Loss}{\partial\overline G^{(l,c)}_{uv}}&=\frac1{MN}\sum_{m=0}^{M-1}\sum_{n=0}^{N-1}\frac{\partial Loss}{\partial\overline F^{(l,c)}_{mn}}e^{-i(um/M+vn/N)2\pi},\\
\frac{\partial Loss}{\partial\overline F^{(l,c)}_{mn}}&=\sum_{u=0}^{M-1}\sum_{v=0}^{N-1}\frac{\partial Loss}{\partial\overline G^{(l,c)}_{uv}}e^{i(um/M+vn/N)2\pi};
\end{aligned}\right.\\
\left\{\begin{aligned}
\frac{\partial Loss}{\partial\overline T^{(l,uv)}_{dc}}&=\frac1{MN}\sum_{t=0}^{K-1}\sum_{s=0}^{K-1}\frac{\partial Loss}{\partial\overline W^{(l)[\mathrm{ker}=d]}_{cts}}e^{i(ut/M+vs/N)2\pi},\\
\frac{\partial Loss}{\partial\overline W^{(l)[\mathrm{ker}=d]}_{cts}}&=\sum_{u=0}^{M-1}\sum_{v=0}^{N-1}\frac{\partial Loss}{\partial\overline T^{(l,uv)}_{dc}}e^{-i(ut/M+vs/N)2\pi}.
\end{aligned}\right.
\end{gathered}\tag{20}$$

Let us conduct the convolution operation (based on Assumption 3.1) on the feature map $\mathbf F^{(l-1)}=[F^{(l-1,1)},F^{(l-1,2)},\ldots,F^{(l-1,C)}]\in\mathbb R^{C\times M\times N}$, and obtain the output feature map $\mathbf F^{(l)}=[F^{(l,1)},F^{(l,2)},\ldots,F^{(l,D)}]\in\mathbb R^{D\times M\times N}$ of the $l$-th layer as follows.

$$F^{(l,d)}_{mn}=b^{(d)}+\sum_{c=1}^{C}\sum_{t=0}^{K-1}\sum_{s=0}^{K-1}W^{(l)[\mathrm{ker}=d]}_{cts}F^{(l-1,c)}_{m+t,n+s}.\tag{21}$$

Based on Equation (19) and Equation (20), and the derivation rule for complex numbers (Kreutz-Delgado, 2009), the exact optimization step of $T^{(l,uv)}_{dc}$ in real implementations can be computed as follows.

$$\begin{aligned}
\frac{\partial Loss}{\partial\overline T^{(l,uv)}_{dc}}
&=\frac1{MN}\sum_{t=0}^{K-1}\sum_{s=0}^{K-1}\frac{\partial Loss}{\partial\overline W^{(l)[\mathrm{ker}=d]}_{cts}}e^{i(ut/M+vs/N)2\pi}\qquad\text{//Equation (20)}\\
&=\frac1{MN}\sum_{t=0}^{K-1}\sum_{s=0}^{K-1}\left(\sum_{m=0}^{M-1}\sum_{n=0}^{N-1}\frac{\partial Loss}{\partial\overline F^{(l,d)}_{mn}}\cdot\overline F^{(l-1,c)}_{m+t,n+s}\right)e^{i(ut/M+vs/N)2\pi}\quad\text{//Equation (21)}\\
&=\frac1{MN}\sum_{t=0}^{K-1}\sum_{s=0}^{K-1}\left(\sum_{m=0}^{M-1}\sum_{n=0}^{N-1}\frac{\partial Loss}{\partial\overline F^{(l,d)}_{mn}}\cdot\frac1{MN}\sum_{u'=0}^{M-1}\sum_{v'=0}^{N-1}\overline G^{(l-1,c)}_{u'v'}e^{-i(u'(m+t)/M+v'(n+s)/N)2\pi}\right)e^{i(ut/M+vs/N)2\pi}\quad\text{//Equation (19)}\\
&=\frac1{MN}\sum_{t=0}^{K-1}\sum_{s=0}^{K-1}\left(\sum_{u'=0}^{M-1}\sum_{v'=0}^{N-1}\overline G^{(l-1,c)}_{u'v'}e^{-i(u't/M+v's/N)2\pi}\cdot\frac1{MN}\sum_{m=0}^{M-1}\sum_{n=0}^{N-1}\frac{\partial Loss}{\partial\overline F^{(l,d)}_{mn}}e^{-i(u'm/M+v'n/N)2\pi}\right)e^{i(ut/M+vs/N)2\pi}\\
&=\frac1{MN}\sum_{t=0}^{K-1}\sum_{s=0}^{K-1}\left(\sum_{u'=0}^{M-1}\sum_{v'=0}^{N-1}\overline G^{(l-1,c)}_{u'v'}\frac{\partial Loss}{\partial\overline G^{(l,d)}_{u'v'}}e^{-i(u't/M+v's/N)2\pi}\right)e^{i(ut/M+vs/N)2\pi}\quad\text{//Equation (20)}\\
&=\frac1{MN}\sum_{t=0}^{K-1}\sum_{s=0}^{K-1}\sum_{u'=0}^{M-1}\sum_{v'=0}^{N-1}\overline G^{(l-1,c)}_{u'v'}\frac{\partial Loss}{\partial\overline G^{(l,d)}_{u'v'}}e^{i((u-u')t/M+(v-v')s/N)2\pi}\\
&=\sum_{u'=0}^{M-1}\sum_{v'=0}^{N-1}\overline G^{(l-1,c)}_{u'v'}\frac{\partial Loss}{\partial\overline G^{(l,d)}_{u'v'}}\cdot\frac1{MN}\sum_{t=0}^{K-1}\sum_{s=0}^{K-1}e^{i((u-u')t/M+(v-v')s/N)2\pi}\\
&=\sum_{u'=0}^{M-1}\sum_{v'=0}^{N-1}\chi_{u'v'uv}\overline G^{(l-1,c)}_{u'v'}\frac{\partial Loss}{\partial\overline G^{(l,d)}_{u'v'}}.
\end{aligned}$$

// Let $\chi_{u'v'uv}=\frac1{MN}\sum_{t=0}^{K-1}\sum_{s=0}^{K-1}e^{i((u-u')t/M+(v-v')s/N)2\pi}$.

where $\chi_{u'v'uv}$ can be rewritten as follows.

$$\begin{aligned}
\chi_{u'v'uv}&=\frac1{MN}\sum_{t=0}^{K-1}\sum_{s=0}^{K-1}e^{i((u-u')t/M+(v-v')s/N)2\pi}\\
&=\frac1{MN}\sum_{t=0}^{K-1}e^{i((u-u')2\pi/M)t}\sum_{s=0}^{K-1}e^{i((v-v')2\pi/N)s}\\
&=\frac1{MN}\frac{\sin(K(u-u')\pi/M)}{\sin((u-u')\pi/M)}\frac{\sin(K(v-v')\pi/N)}{\sin((v-v')\pi/N)}\cdot e^{i((K-1)(u-u')/M+(K-1)(v-v')/N)\pi}\quad\text{//According to Equation (13)}.
\end{aligned}$$

Similarly, we computed the gradient of the loss function w.r.t. the spectrum map $\overline G^{(l-1,c)}$ as follows.

$$\begin{aligned}
\frac{\partial Loss}{\partial\overline G^{(l-1,c)}_{u'v'}}
&=\frac1{MN}\sum_{m=0}^{M-1}\sum_{n=0}^{N-1}\frac{\partial Loss}{\partial\overline F^{(l-1,c)}_{mn}}e^{-i(u'm/M+v'n/N)2\pi}\quad\text{//Equation (20)}\\
&=\frac1{MN}\sum_{m=0}^{M-1}\sum_{n=0}^{N-1}\left(\sum_{t=0}^{K-1}\sum_{s=0}^{K-1}\overline W^{(l)[\mathrm{ker}=d]}_{cts}\cdot\frac{\partial Loss}{\partial\overline F^{(l,d)}_{m-t,n-s}}\right)e^{-i(u'm/M+v'n/N)2\pi}\quad\text{//Equation (21)}\\
&=\frac1{MN}\sum_{m=0}^{M-1}\sum_{n=0}^{N-1}\left(\sum_{t=0}^{K-1}\sum_{s=0}^{K-1}\overline W^{(l)[\mathrm{ker}=d]}_{cts}\cdot\sum_{u=0}^{M-1}\sum_{v=0}^{N-1}\frac{\partial Loss}{\partial\overline G^{(l,d)}_{uv}}e^{i(u(m-t)/M+v(n-s)/N)2\pi}\right)e^{-i(u'm/M+v'n/N)2\pi}\quad\text{//According to Equation (20)}\\
&=\frac1{MN}\sum_{m=0}^{M-1}\sum_{n=0}^{N-1}\left(\sum_{u=0}^{M-1}\sum_{v=0}^{N-1}\frac{\partial Loss}{\partial\overline G^{(l,d)}_{uv}}e^{i(um/M+vn/N)2\pi}\cdot\sum_{t=0}^{K-1}\sum_{s=0}^{K-1}\overline W^{(l)[\mathrm{ker}=d]}_{cts}e^{-i(ut/M+vs/N)2\pi}\right)e^{-i(u'm/M+v'n/N)2\pi}\\
&=\frac1{MN}\sum_{m=0}^{M-1}\sum_{n=0}^{N-1}\left(\sum_{u=0}^{M-1}\sum_{v=0}^{N-1}\frac{\partial Loss}{\partial\overline G^{(l,d)}_{uv}}\overline T^{(l,uv)}_{dc}e^{i(um/M+vn/N)2\pi}\right)e^{-i(u'm/M+v'n/N)2\pi}\quad\text{//Equation (19)}\\
&=\sum_{u=0}^{M-1}\sum_{v=0}^{N-1}\frac{\partial Loss}{\partial\overline G^{(l,d)}_{uv}}\overline T^{(l,uv)}_{dc}\cdot\frac1{MN}\sum_{m=0}^{M-1}\sum_{n=0}^{N-1}e^{i((u-u')m/M+(v-v')n/N)2\pi}\\
&=\sum_{u=0}^{M-1}\sum_{v=0}^{N-1}\frac{\partial Loss}{\partial\overline G^{(l,d)}_{uv}}\overline T^{(l,uv)}_{dc}\cdot\delta_{u-u'}\delta_{v-v'}\quad\text{//Equation (16)}\\
&=\frac{\partial Loss}{\partial\overline G^{(l,d)}_{u'v'}}\overline T^{(l,u'v')}_{dc}.
\end{aligned}$$

Based on the derived $\frac{\partial Loss}{\partial\overline T^{(l,uv)}_{dc}}\in\mathbb C$ and $\frac{\partial Loss}{\partial\overline G^{(l-1,c)}_{u'v'}}\in\mathbb C$, we can further compute gradients $\frac{\partial Loss}{\partial(\overline T^{(l,uv)})^\top}\in\mathbb C^{D\times C}$ and $\frac{\partial Loss}{\partial(\overline{\mathbf g}^{(l-1,u'v')})^\top}\in\mathbb C^C$ as follows.

$$\frac{\partial Loss}{\partial(\overline T^{(l,uv)})^\top}=\sum_{u'=0}^{M-1}\sum_{v'=0}^{N-1}\chi_{u'v'uv}\overline{\mathbf g}^{(l-1,u'v')}\frac{\partial Loss}{\partial(\overline{\mathbf g}^{(l,u'v')})^\top}.\tag{22}$$

$$\frac{\partial Loss}{\partial(\overline{\mathbf g}^{(l-1,u'v')})^\top}=\frac{\partial Loss}{\partial(\overline{\mathbf g}^{(l,u'v')})^\top}\overline T^{(l,u'v')}.\tag{23}$$

Furthermore, **we extend the above proof of a single convolutional layer to a network with $L$ cascaded convolutional layers.** Let $\mathbf g^{(l,u'v')}$ denote the frequency component at the frequency $[u',v']$ of the $l$-th layer's output feature, and let $T^{(l,uv)}$ the matrix computed by the $l$-th layer's convolutional weights. Then, according to Equation (23), the gradient w.r.t. $\mathbf g^{(l,u'v')}$ can be computed as follows.

$$\begin{aligned}
\frac{\partial Loss}{\partial(\overline{\mathbf g}^{(l,u'v')})^\top}&=\frac{\partial Loss}{\partial(\mathbf g^{(L,u'v')})^\top}\overline T^{(L,u'v')}\cdots\overline T^{(l+1,u'v')}\\
&=\frac{\partial Loss}{\partial(\overline{\mathbf g}^{(L,u'v')})^\top}\overline{\mathbb T}^{(u'v')(L:l+1)}.
\end{aligned}\tag{24}$$

According to Equation (22), the gradient w.r.t. $T^{(l,uv)}$ can be computed as follows.

$$\begin{aligned}
\frac{\partial Loss}{\partial(\overline T^{(l,uv)})^\top}
&=\sum_{u'=0}^{M-1}\sum_{v'=0}^{N-1}\chi_{u'v'uv}\overline{\mathbf g}^{(l-1,u'v')}\frac{\partial Loss}{\partial(\overline{\mathbf g}^{(l,u'v')})^\top}\\
&=\sum_{u'=0}^{M-1}\sum_{v'=0}^{N-1}\chi_{u'v'uv}\left(\overline{\mathbb T}^{(u'v')(l-1:1)}\overline{\mathbf g}^{(0,u'v')}+\overline{\boldsymbol\beta'}\delta_{u'v'}\right)\frac{\partial Loss}{\partial(\overline{\mathbf g}^{(L,u'v')})^\top}\overline{\mathbb T}^{(u'v')(L:l+1)}\quad\text{//Corollary 3.3}\\
&=\sum_{u'=0}^{M-1}\sum_{v'=0}^{N-1}\chi_{u'v'uv}\left(\overline{\mathbb T}^{(u'v')(l-1:1)}\overline{\mathbf g}^{(u'v')}+\overline{\boldsymbol\beta'}\delta_{u'v'}\right)\frac{\partial Loss}{\partial(\overline{\mathbf h}^{(u'v')})^\top}\overline{\mathbb T}^{(u'v')(L:l+1)}.
\end{aligned}\tag{25}$$

// Let $\mathbf g^{(uv)}=\mathbf g^{(0,uv)}$; $\mathbf h^{(uv)}=\mathbf g^{(L,uv)}$.

Let us use the gradient descent algorithm to update the convlutional weight $W_c^{(l)[\mathrm{ker}=d]}|_n$ of the $n$-th epoch, the updated frequency spectrum $W_c^{(l)[\mathrm{ker}=d]}|_{n+1}$ can be computed as follows.

$$\forall t,s,\qquad W^{(l)[\mathrm{ker}=d]}_{cts}|_{n+1}=W^{(l)[\mathrm{ker}=d]}_{cts}|_n-\eta\cdot\frac{\partial Loss}{\partial\overline W^{(l)[\mathrm{ker}=d]}_{cts}}.$$

where $\eta$ is the learning rate. Then, the updated frequency spectrum $T^{(l,uv)}|_{n+1}$ computed based on Equation (20) is given as follows.

$$\begin{aligned}
\Delta T^{(l,uv)}_{dc}&=T^{(l,uv)}_{dc}|_{n+1}-T^{(l,uv)}_{dc}|_n\\
&=\sum_{t=0}^{K-1}\sum_{s=0}^{K-1}W^{(l)[\mathrm{ker}=d]}_{cts}|_{n+1}e^{i(ut/M+vs/N)2\pi}-T^{(l,uv)}_{dc}|_n\quad\text{//Equation (19)}\\
&=\sum_{t=0}^{K-1}\sum_{s=0}^{K-1}\left(W^{(l)[\mathrm{ker}=d]}_{cts}|_n-\eta\cdot\frac{\partial Loss}{\partial\overline W^{(l)[\mathrm{ker}=d]}_{cts}}\right)e^{i(ut/M+vs/N)2\pi}-T^{(l,uv)}_{dc}|_n\\
&=\left(\sum_{t=0}^{K-1}\sum_{s=0}^{K-1}W^{(l)[\mathrm{ker}=d]}_{cts}|_ne^{i(ut/M+vs/N)2\pi}-T^{(l,uv)}_{dc}|_n\right)-\eta\sum_{t=0}^{K-1}\sum_{s=0}^{K-1}\frac{\partial Loss}{\partial\overline W^{(l)[\mathrm{ker}=d]}_{cts}}e^{i(ut/M+vs/N)2\pi}\\
&=-\eta\sum_{t=0}^{K-1}\sum_{s=0}^{K-1}\frac{\partial Loss}{\partial\overline W^{(l)[\mathrm{ker}=d]}_{cts}}e^{i(ut/M+vs/N)2\pi}\quad\text{//Equation (19)}\\
&=-\eta MN\frac{\partial Loss}{\partial\overline T^{(l,uv)}_{dc}}\quad\text{//Equation (20)}.
\end{aligned}$$

Therefore, we prove that any step on $W^{(l)[\mathrm{ker}=d]}_{cts}$ equals to $MN$ step on $T^{(uv)}_{dc}$. In this way, pull Equation (25) in the change of $T^{(l,uv)}$ can be computed as follows.

$$\left(\Delta T^{(l,uv)}\right)^\top=-\eta MN\sum_{u'=0}^{M-1}\sum_{v'=0}^{N-1}\chi_{u'v'uv}\left(\overline{\mathbb T}^{(u'v')(l-1:1)}\overline{\mathbf g}^{(u'v')}+\delta_{u'v'}\overline{\boldsymbol\beta'}\right)\frac{\partial Loss}{\partial(\overline{\mathbf h}^{(u'v')})^\top}\overline{\mathbb T}^{(u'v')(L:l+1)}.\tag{26}$$
