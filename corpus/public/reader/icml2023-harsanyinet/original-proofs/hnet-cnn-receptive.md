Appendix E, physical PDF page 16, first part of the complete Setting 2 proof.

The source assumes that all channel neurons at the same spatial position share
\[
\tau_{(1,h,w)}^{(l)}=\tau_{(2,h,w)}^{(l)}=\cdots=\tau_{(C,h,w)}^{(l)}\in\mathbb R^{CK^2}.
\]
Since $(\Sigma_u^{(l)})_{i,i}=\mathbf1((\tau_u^{(l)})_i>0)$, it concludes equality of all the corresponding selection matrices, then equality of their child sets:
\[
\Sigma_{(1,h,w)}^{(l)}=\cdots=\Sigma_{(C,h,w)}^{(l)},\qquad
S_{(1,h,w)}^{(l)}=\cdots=S_{(C,h,w)}^{(l)}.
\]
Applying the recursive definition in Eq.(8) gives
\[
R_{(1,h,w)}^{(l)}=R_{(2,h,w)}^{(l)}=\cdots=R_{(C,h,w)}^{(l)}.
\]
Thus all channel units at the same spatial location share their receptive field. The following grouping argument is transcribed separately under `hnet-cnn-regroup`; the two records together retain the complete source proof.
