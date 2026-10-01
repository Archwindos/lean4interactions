For any other frequency component $[u,v]$, where $u\ne u_1$, $u\ne u_2$, $v\ne v_1$, $v\ne v_2$, the change $\Delta\mathbb T^{(uv)(L:1)}$ can be cpmputed as the linear combination of the $\Delta\mathbb T^{(L:1)(u_1v_1)}$ and $\Delta\mathbb T^{(L:1)(u_2v_2)}$ as follows.

$$\Delta\mathbb T^{(uv)(L:1)}=a_1\Delta\mathbb T^{(L:1)(u_1v_1)}+a_2\Delta\mathbb T^{(L:1)(u_2v_2)}.\tag{51}$$

where $a_1\in\mathbb C$ and $a_2\in\mathbb C$ are two complex coefficients, which keep unchanged during the learning process.

On the other hand, the exact change of $\mathbb T^{(uv)(L:1)}$ can be directly computed given the objective function. For frequencies $[u_1,v_1]$ and $[u_2,v_2]$, we have:

$$\Delta\mathbb T^{(L:1)(u_1v_1)}=\frac{H^*_{u_1v_1}}{G_{u_1v_1}}-\mathbb T^{(L:1)(u_1v_1)}=-A.\tag{52}$$

$$\Delta\mathbb T^{(L:1)(u_2v_2)}=\frac{H^*_{u_2v_2}}{G_{u_2v_2}}-\mathbb T^{(L:1)(u_2v_2)}=\overline A.\tag{53}$$

For any other frequency component $[u,v]$, the change $\Delta\mathbb T^{(uv)(L:1)}$ can be computed as follows:

$$\Delta\mathbb T^{(uv)(L:1)}=-a_1A+a_2\overline A.\tag{54}$$

Then, combining Equation (51) and Equation (54), we can obtain the value of $\eta$.

$$\begin{aligned}
\eta&\propto\frac{-a_1A+a_2\overline A}{-a_1(A\chi_{u_1v_1u_1v_1}-\overline A\chi_{u_2v_2u_1v_1})-a_2(A\chi_{u_1v_1u_2v_2}-\overline A\chi_{u_2v_2u_2v_2})}\quad\text{//Equation (46)}\\
&=\frac{-a_1A+a_2\overline A}{-a_1A(\chi_{u_1v_1u_1v_1}-e^{-i2\phi}\chi_{u_2v_2u_1v_1})+a_2\overline A(\chi_{u_2v_2u_2v_2}-e^{i2\phi}\chi_{u_1v_1u_2v_2})}\\
&=\frac{-a_1A+a_2\overline A}{-a_1A+a_2\overline A}\cdot\frac{MN}{K^2-\dfrac{\sin(K(u_2-u_1)\pi/M)\sin(K(v_2-v_1)\pi/N)}{\sin((u_2-u_1)\pi/M)\sin((v_2-v_1)\pi/N)}}\\
&=\frac{MN}{K^2-\dfrac{\sin(K(u_2-u_1)\pi/M)\sin(K(v_2-v_1)\pi/N)}{\sin((u_2-u_1)\pi/M)\sin((v_2-v_1)\pi/N)}}.
\end{aligned}\tag{55}$$


