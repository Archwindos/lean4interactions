And $\|\frac{Loss}{\partial\mathbf W}\|$ can be computed as follows.

$$\begin{aligned}
\left\|\frac{Loss}{\partial\mathbf W}\right\|^2
&=\sum_{l,d,c}\sum_{t,s}\left(\frac{\partial Loss}{\partial W^{(l)[\mathrm{ker}=d]}_{cts}}\right)^2\\
&=\sum_{l,d,c}\sum_{t,s}\frac{\partial Loss}{\partial\overline W^{(l)[\mathrm{ker}=d]}_{cts}}\cdot\frac{\partial Loss}{\partial\overline W^{(l)[\mathrm{ker}=d]}_{cts}}\\
&=\sum_{l,d,c}\sum_{t,s}\frac{\partial Loss}{\partial\overline W^{(l)[\mathrm{ker}=d]}_{cts}}\sum_{u,v}\frac{\partial Loss}{\partial\overline T^{(l,uv)}_{dc}}e^{-i(ut/M+vs/N)2\pi}\\
&=\sum_{l,d,c}\sum_{u,v}\frac{\partial Loss}{\partial\overline T^{(l,uv)}_{dc}}\sum_{t,s}\frac{\partial Loss}{\partial\overline W^{(l)[\mathrm{ker}=d]}_{cts}}e^{-i(ut/M+vs/N)2\pi}\\
&=\sum_{l,d,c}\sum_{u,v}\frac{\partial Loss}{\partial\overline T^{(l,uv)}_{dc}}\frac{\partial Loss}{\partial T^{(l,uv)}_{dc}}\\
&=\sum_{l,d,c}\sum_{u,v}\frac{\partial Loss}{\partial\overline T^{(l,uv)}_{dc}}\overline{\frac{\partial Loss}{\partial T^{(l,uv)}_{dc}}}\\
&=\sum_{l,d,c}\sum_{u,v}\left|\frac{\partial Loss}{\partial\overline T^{(l,uv)}_{dc}}\right|^2\\
&\propto\sum_{l,d,c}\sum_{u,v}\alpha^2\\
&\propto\alpha^2.
\end{aligned}\tag{56}$$

Therefore, the weight change $\|\Delta\mathbf W\|$ can be computed as follows:

$$\begin{aligned}
\|\Delta\mathbf W\|&=\eta\cdot\left\|\frac{Loss}{\partial\mathbf W}\right\|\\
&\propto\eta\cdot\sqrt{\|\Delta\mathbf W\|^2}\\
&\propto\frac{MN\alpha}{K^2-\dfrac{\sin(K(u_2-u_1)\pi/M)\sin(K(v_2-v_1)\pi/N)}{\sin((u_2-u_1)\pi/M)\sin((v_2-v_1)\pi/N)}}\quad\text{//Equation (55) and Equation (56)}.
\end{aligned}\tag{57}$$
