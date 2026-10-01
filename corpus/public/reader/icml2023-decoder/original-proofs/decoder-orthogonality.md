$$\begin{aligned}\sum_{m=0}^{M-1}\sum_{n=0}^{N-1}e^{-i(um/M+vn/N)2\pi}&=\sum_{m=0}^{M-1}e^{im(-u2\pi/M)}\sum_{n=0}^{N-1}e^{in(-v2\pi/N)}\\&=(M\delta_{-u2\pi/M})(N\delta_{-v2\pi/N})\quad\text{//According to Equation (14)}\\&=\begin{cases}MN,&u=v=0,\\0,&\text{otherwise}.\end{cases}\end{aligned}$$

To simplify the representation, let $\delta_{uv}$ be the simplification of $\delta_{-u2\pi/M}\delta_{-v2\pi/N}$ in the following proofs. Therefore, we have Equation (15).

Similarly, we derive the second equation as follows.

$$\begin{aligned}\sum_{m=0}^{M-1}\sum_{n=0}^{N-1}e^{i((u-u')m/M+(v-v')n/N)2\pi}&=\sum_{m=0}^{M-1}e^{im((u-u')2\pi/M)}\sum_{n=0}^{N-1}e^{in((v-v')2\pi/N)}\\&=MN\delta_{(u-u')2\pi/M}\delta_{(v-v')2\pi/N}\quad\text{//According to Equation (14)}\\&=MN\delta_{u-u'}\delta_{v-v'}\\&=\begin{cases}MN,&u'=u;\ v'=v,\\0,&\text{otherwise}.\end{cases}\end{aligned}$$
