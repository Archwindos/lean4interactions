We prove Lemma A.1 as follows.

Proof. First, let us use the letter $S\in\mathbb C$ to denote the term of $\sum_{n=0}^{N-1}e^{in\theta}$.

$$S=\sum_{n=0}^{N-1}e^{in\theta}.$$

Therefore, $e^{i\theta}S$ is formulated as follows.

$$e^{i\theta}S=\sum_{n=1}^{N}e^{in\theta}\in\mathbb C.$$

Then, $S$ can be computed as $S=(e^{i\theta}S-S)/(e^{i\theta}-1)$. Therefore, we have

$$\begin{aligned}S&=\frac{e^{i\theta}S-S}{e^{i\theta}-1}\\&=\frac{\sum_{n=1}^{N}e^{in\theta}-\sum_{n=0}^{N-1}e^{in\theta}}{e^{i\theta}-1}\\&=\frac{e^{iN\theta}-1}{e^{i\theta}-1}\\&=\frac{e^{iN\theta/2}-e^{-iN\theta/2}}{e^{i\theta/2}-e^{-i\theta/2}}e^{i(N-1)\theta/2}\\&=\frac{(e^{iN\theta/2}-e^{-iN\theta/2})/(2i)}{(e^{i\theta/2}-e^{-i\theta/2})/(2i)}e^{i(N-1)\theta/2}\\&=\frac{\sin(N\theta/2)}{\sin(\theta/2)}e^{i(N-1)\theta/2}.\end{aligned}$$

Therefore, we prove that $\sum_{n=0}^{N-1}e^{in\theta}=\frac{\sin(N\theta/2)}{\sin(\theta/2)}e^{i(N-1)\theta/2}$.

Then, we prove the special case that when $N\theta=2k\pi$, $k\in\mathbb Z$, $-N<k<N$, $\sum_{n=0}^{N-1}e^{in\theta}=N\delta_\theta=\begin{cases}N,&\theta=0,\\0,&\text{otherwise},\end{cases}$ as follows.

When $\theta=0$, we have

$$\begin{aligned}\lim_{\theta\to0}\sum_{n=0}^{N-1}e^{in\theta}&=\lim_{\theta\to0}\frac{\sin(N\theta/2)}{\sin(\theta/2)}e^{i(N-1)\theta/2}\\&=\lim_{\theta\to0}\frac{\sin(N\theta/2)}{\sin(\theta/2)}\\&=N.\end{aligned}$$

When $\theta\ne0$, and $N\theta=2k\pi$, $k\in\mathbb Z$, $-N<k<N$, we have

$$\begin{aligned}\sum_{n=0}^{N-1}e^{in\theta}&=\frac{\sin(N\theta/2)}{\sin(\theta/2)}e^{i(N-1)\theta/2}\\&=\frac{\sin(k\pi)}{\sin(k\pi/N)}e^{i(N-1)k\pi/N}\\&=0.\end{aligned}$$
