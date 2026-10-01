from pathlib import Path
import json,re
D=Path(__file__).parent
p=D/'author-transcripts-a1.json';d=json.loads(p.read_text())
for t in d['transcripts']:
 for k in ['original_statement_md','original_proof_md']:
  t[k]=re.sub(r'\\n(?=[A-Z])','\n',t[k])
main=json.loads((D/'author-transcripts-main-extra.json').read_text())
statement=next(t['original_statement_md'] for t in main['transcripts'] if t['key']=='main-theorem-3.2')
proof=r"""In this section, we prove Theorem 3.2 in Section 3 of the main paper, as follows.

Proof. Given each $c$-th channel of the feature spectrum $G^{(c)}$, the corresponding feature $F^{(c)}$ in the time domain can be computed as follows.

$$F^{(c)}_{mn}=\frac1{MN}\sum_{u=0}^{M-1}\sum_{v=0}^{N-1}G^{(c)}_{uv}e^{i(um/M+vn/N)2\pi}.$$

Then, let us conduct the convolution operation (in Equation (1) in the main paper) on feature $\mathbf F=[F^{(1)},F^{(2)},\ldots,F^{(C)}]$, in order to obtain output feature $\widetilde{\mathbf F}\in\mathbb R^{D\times M'\times N'}$.

$$\begin{gathered}
\forall d=1,2,\ldots,D;\quad0\le m<M';\quad0\le n<N';\\
\begin{aligned}
\widetilde F^{(d)}_{mn}
&=b^{(d)}+\sum_{c=1}^{C}\sum_{t=0}^{K-1}\sum_{s=0}^{K-1}W^{[\mathrm{ker}=d]}_{cts}F^{(c)}_{m+t,n+s}\\
&=b^{(d)}+\sum_{c=1}^{C}\sum_{t=0}^{K-1}\sum_{s=0}^{K-1}W^{[\mathrm{ker}=d]}_{cts}\frac1{MN}\sum_{u=0}^{M-1}\sum_{v=0}^{N-1}G^{(c)}_{uv}e^{i(u(m+t)/M+v(n+s)/N)2\pi}\\
&=b^{(d)}+\sum_{c=1}^{C}\frac1{MN}\sum_{u=0}^{M-1}\sum_{v=0}^{N-1}G^{(c)}_{uv}e^{i(um/M+vn/N)2\pi}\sum_{t=0}^{K-1}\sum_{s=0}^{K-1}W^{[\mathrm{ker}=d]}_{cts}e^{i(ut/M+vs/N)2\pi}\\
&=b^{(d)}+\sum_{c=1}^{C}\frac1{MN}\sum_{u=0}^{M-1}\sum_{v=0}^{N-1}T^{(uv)}_{dc}G^{(c)}_{uv}e^{i(um/M+vn/N)2\pi}.
\end{aligned}
\end{gathered}$$

Then, let us conduct the DFT on each channel of $\widetilde{\mathbf F}$, in order to obtain feature spectrums $H^{(d)}_{u'v'}$ of $\widetilde{\mathbf F}$.

$$\begin{gathered}
\forall d=1,2,\ldots,D;\quad0\le u'<M';\quad0\le v'<N';\\
\begin{aligned}
H^{(d)}_{u'v'}
&=\sum_{m=0}^{M'-1}\sum_{n=0}^{N'-1}\widetilde F^{(l,d)}_{mn}e^{-i(u'm/M'+v'n/N')2\pi}\\
&=\sum_{m=0}^{M'-1}\sum_{n=0}^{N'-1}e^{-i(u'm/M'+v'n/N')2\pi}
\left(b^{(d)}+\sum_{c=1}^{C}\frac1{MN}\sum_{u=0}^{M-1}\sum_{v=0}^{N-1}T^{(uv)}_{dc}G^{(c)}_{uv}e^{i(um/M+vn/N)2\pi}\right)\quad\text{//Equation (15)}\\
&=M'N'b^{(d)}\delta_{u'v'}+\sum_{c=1}^{C}\sum_{u=0}^{M-1}\sum_{v=0}^{N-1}T^{(uv)}_{dc}G^{(c)}_{uv}\frac1{MN}\sum_{m=0}^{M'-1}\sum_{n=0}^{N'-1}e^{i((u/M-u'/M')m+(v/N-v'/N')n)2\pi}\\
&\quad\text{//Let }\alpha_{u'v'uv}=\frac1{MN}\sum_{m=0}^{M'-1}\sum_{n=0}^{N'-1}e^{i((u/M-u'/M')m+(v/N-v'/N')n)2\pi}\\
&=M'N'b^{(d)}\delta_{u'v'}+\sum_{u=0}^{M-1}\sum_{v=0}^{N-1}\alpha_{u'v'uv}\sum_{c=1}^{C}T^{(uv)}_{dc}G^{(c)}_{uv}.
\end{aligned}
\end{gathered}$$

When the convlution operation does not apply paddings, and its stride size is 1, $M'=M-K+1$, $N'=N-K+1$. In this way, $\alpha_{u'v'uv}$ can be rewritten as follows.

$$\begin{aligned}
\alpha_{u'v'uv}
&=\frac1{MN}\sum_{m=0}^{M'-1}\sum_{n=0}^{N'-1}e^{i((u/M-u'/M')m+(v/N-v'/N')n)2\pi}\\
&\quad\text{//}M'=M-K+1,\ N'=N-K+1\\
&=\frac1{MN}\sum_{m=0}^{M-K}\sum_{n=0}^{N-K}e^{i((u/M-u'/(M-K+1))m+(v/N-v'/(N-K+1))n)2\pi}\\
&=\frac1{MN}\sum_{m=0}^{M-K}e^{i(u/M-u'/(M-K+1))2\pi m}\sum_{n=0}^{N-K}e^{i(v/N-v'/(N-K+1))2\pi n}\\
&\quad\text{//According to Equation (13)}\\
&=\frac1{MN}\frac{\sin((M-K)\lambda_{uu'}\pi)}{\sin(\lambda_{uu'}\pi)}
\frac{\sin((N-K)\gamma_{vv'}\pi)}{\sin(\gamma_{vv'}\pi)}
e^{i((M-K)\lambda_{uu'}+(N-K)\gamma_{vv'})\pi}.
\end{aligned}\tag{17}$$

where $\lambda_{uu'}=((u-u')M-u(K-1))/(M(M-K+1))$, $\gamma_{vv'}=((v-v')N-v(K-1))/(N(N-K+1))$.

Therefore, we prove that the vector $\mathbf h^{(u'v')}=[H^{(1)}_{u'v'},H^{(2)}_{u'v'},\ldots,H^{(D)}_{u'v'}]^\top\in\mathbb C^D$ can be computed as follows.

$$\forall d=1,2,\ldots,D;\qquad
\mathbf h^{(u'v')}=\delta_{u'v'}M'N'\mathbf b+\sum_{u=0}^{M-1}\sum_{v=0}^{N-1}\alpha_{u'v'uv}T^{(uv)}\mathbf g^{(uv)}.$$

Furthermore, based on Assumption 3.1, the convolution operation does not change the size of the feature map, i.e., $M'=M$, $N'=N$. In this case, $\alpha_{u'v'uv}$ can be computed as follows.

$$\begin{aligned}
\alpha_{u'v'uv}
&=\frac1{MN}\sum_{m=0}^{M'-1}\sum_{n=0}^{N'-1}e^{i((u/M-u'/M')m+(v/N-v'/N')n)2\pi}\\
&=\frac1{MN}\sum_{m=0}^{M-1}\sum_{n=0}^{N-1}e^{i((u-u')m/M+(v-v')n/N)2\pi}\quad\text{//}M'=M,\ N'=N\\
&=\frac1{MN}\sum_{m=0}^{M-1}e^{i((u-u')2\pi/M)m}\sum_{n=0}^{N-1}e^{i((v-v')2\pi/N)n}\quad\text{//According to Equation (16)}\\
&=\delta_{u-u'}\delta_{v-v'}.
\end{aligned}\tag{18}$$

where $\delta_{u-u'}=\begin{cases}1,&u'=u,\\0,&\text{otherwise},\end{cases}$; $\delta_{v-v'}=\begin{cases}1,&v'=v,\\0,&\text{otherwise}.\end{cases}$

Therefore, $\mathbf h^{(u'v')}$ can be computed as follows.

$$\begin{aligned}
\mathbf h^{(u'v')}
&=\sum_{u=0}^{M'-1}\sum_{v=0}^{N'-1}\alpha_{u'v'uv}T^{(u'v')}\mathbf g^{(u'v')}+\delta_{u'v'}M'N'\mathbf b\\
&=\sum_{u=0}^{M-1}\sum_{v=0}^{N-1}\delta_{u-u'}\delta_{v-v'}T^{(u'v')}\mathbf g^{(u'v')}+\delta_{u'v'}MN\mathbf b\\
&=T^{(u'v')}\mathbf g^{(u'v')}+MN\mathbf b\delta_{u'v'}.
\end{aligned}$$

Then, we prove that $\mathbf h^{(uv)}=T^{(uv)}\mathbf g^{(uv)}+MN\mathbf b\delta_{uv}$."""
row=dict(key='A.1',source_pages=[3,12,13,14],equation_labels=['3','17','18'],
 original_statement_md=statement,original_proof_md=proof,transcription_notes=[
 'PDF12–13 and the A.1 portion of PDF14 were checked against rendered pages. The printed extra l in the output feature and the repeated u′v′ factors in the final sums are preserved.',
 'Equation17 retains the off-by-one sine numerators. The subsequent circular branch is a separate valid specialization and does not use those faulty numerators.'])
d['transcripts']=[t for t in d['transcripts'] if t['key']!='A.1']+[row]
p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
