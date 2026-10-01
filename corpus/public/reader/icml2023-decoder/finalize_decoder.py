"""Final human proofs and precise bindings to frozen, compiled declarations."""
from finish_decoder import st,items,names,GAUSS

def finalize(p):
 rows={r['id'].removeprefix('decoder-'):r for r in p.rows}
 def refs(ns,*xs):return [ns+'.'+x for x in xs]
 def replace(s,steps,scope,role=None,ass=None):
  r=rows[s];r['proof_steps']=[];r['translations']['en']['proof_steps']=[]
  for k,(z,e,bz,be,ft,ln) in enumerate(steps,1):
   sid=f"{r['id']}-step-{k}"
   r['proof_steps'].append(dict(id=sid,title=z,body_md=bz,formula_tex=ft,justification='',lean_refs=ln))
   r['translations']['en']['proof_steps'].append(dict(id=sid,title=e,body_md=be,justification='',lean_refs=ln))
  r['overview']=steps[0][2];r['translations']['en']['overview']=steps[0][3]
  r['scope'],r['translations']['en']['scope']=scope
  r['lean']['scope']=scope[0];r['lean']['translations']['en']['scope']=scope[1]
  r['lean']['declarations']=list(dict.fromkeys(n for x in steps for n in x[-1]))
  if role:r['lean']['evidence_role']=role
  if ass:r['assumptions'],r['translations']['en']['assumptions']=items(r['id'],'assumption',ass)
 matrix='Harsanyi.Frequency.MatrixBackprop';multi='Harsanyi.Frequency.MultiChannel'
 valid='Harsanyi.Frequency.Valid';weak='Harsanyi.Frequency.WeakIndependence';param='Harsanyi.Frequency.Parameters'
 r=rows['geometric-sum']
 r['proof_steps'][1]['lean_refs']+=refs(valid,'geometric_real_sine_quotient','geometric_sine_quotient')
 r['translations']['en']['proof_steps'][1]['lean_refs']=r['proof_steps'][1]['lean_refs']
 r['scope']=r'有限和全域、非单位根商及$\sin(\theta/2)\ne0$的实际实三角商均已验证。原任意$\theta$商的普通定义域问题保留，不把Lean总化除法当作作者实商。'
 r['translations']['en']['scope']=r'The everywhere-defined finite sum, non-unit quotient and actual real sine quotient on $\sin(\theta/2)\ne0$ are verified. The ordinary domain problem in the source universal quotient remains; Lean total division is not substituted for the author’s ordinary quotient.'
 r['lean']['scope']=r['scope'];r['lean']['translations']['en']['scope']=r['translations']['en']['scope']
 r['lean']['declarations']+=refs(valid,'geometric_real_sine_quotient','geometric_sine_quotient')
 r=rows['valid-convolution']
 r['proof_steps'][0]['lean_refs']=refs(valid,'cropped_offset_layer_dft_bias','valid_indices_no_wrap','valid_layer_dft','real_valid_layer_embedding')
 r['translations']['en']['proof_steps'][0]['lean_refs']=r['proof_steps'][0]['lean_refs']
 r['proof_steps'][1]['body_md']+=r'该系数反例同时接到真实实输入$f\equiv1$与$\delta_{00}$核：旧谱仅DC为9，真实$2\times2$输出恒1，其$(1,1)$谱为0；打印系数预测$(-1/9)\cdot1\cdot9=-1$。所以不是只比较两个孤立符号。'
 r['translations']['en']['proof_steps'][1]['body_md']+=r' The coefficient witness is also connected to actual real input $f\equiv1$ and the $\delta_{00}$ kernel. The old spectrum is 9 only at DC; the actual $2\times2$ output is constant one and has spectrum zero at $(1,1)$, whereas the printed coefficient predicts $(-1/9)\cdot1\cdot9=-1$. This compares actual operators rather than isolated symbols.'
 r['proof_steps'][1]['lean_refs']=refs(valid,'witness_grid_frequency_difference','actual_valid_equation17_counterexample')
 r['translations']['en']['proof_steps'][1]['lean_refs']=r['proof_steps'][1]['lean_refs']
 r['scope']='一般周期延拓后裁剪的完整跨频式、有效无padding不越界连接，以及真实实卷积的Eq17反例均已验证。原正弦分子项数错误单列，原相位不判错。'
 r['translations']['en']['scope']='The full mixing identity for cropping a periodically extended input, the no-wrap connection to valid convolution, and an actual real-convolution counterexample to Equation (17) are verified. Only the sine-numerator count is refuted; the original phase is correct.'
 r['lean']['scope']=r['scope'];r['lean']['translations']['en']['scope']=r['translations']['en']['scope']
 r['lean']['declarations']=list(dict.fromkeys(n for x in r['proof_steps'] for n in x['lean_refs']));r['lean']['evidence_role']='counterexample'
 replace('backpropagation',[
 st('在同一网络状态求loss导数','Differentiate the loss at the same network state',
 r'固定原第$l$层真实实权重$W$、常数通道偏置$b$及前后缀。前缀空间输出记$F$，后缀为有序仿射网络$S$。假设原loss在实际$S(\mathrm{Conv}_W(F)+b)$处有实Fréchet导数$J$；真实权重到中层输出是连续线性映射$B_F$，后缀导数是实际有序层算子$A_S$。链式法则给$d_W Loss=J\circ A_S\circ B_F$，与后续更新使用同一$J,W,F$；参数基向量给逐实坐标梯度，不把$T$当独立复参数。',
 r'Fix the actual real weights $W$, constant channel bias $b$, and the prefix and suffix around source layer $l$. Let $F$ be the actual prefix output and $S$ the ordered affine suffix. Assume the real loss has Fréchet derivative $J$ at the actual $S(\mathrm{Conv}_W(F)+b)$. The parameter-to-middle-output map is a continuous linear map $B_F$ and the suffix derivative is its actual ordered layer operator $A_S$. The chain rule gives $d_W Loss=J\circ A_S\circ B_F$, using the same $J,W,F$ in the subsequent update. Parameter basis vectors give real coordinate gradients; $T$ is not treated as an independent complex parameter.',
 r'd_W Loss=J\circ A_S\circ B_F',refs(matrix,'actual_cascade_parameter_loss_hasFDerivAt','real_network_hasFDerivAt')),
 st('求后缀伴随并显式求通道和','Compute the suffix adjoint with every channel sum',
 r'设$D=\mathrm{riesz}(J)$是最终空间梯度。单层实伴随为$(A^*D)_c(x)=\sum_{d,t,s}W_{dcts}D_d(x-(t,s))$，包含全部输出通道$d$。其DFT是$\overline T^{\top}\widehat D$；复合伴随反转顺序，所以中层梯度$D_l$满足$\widehat D_l(k)=\overline{\mathbb T^{(k)(L:l+1)}}^{\top}\widehat D(k)$。矩阵$T^{(l)}$为$C_l\times C_{l-1}$，其共轭转置及转置更新的外积为$C_{l-1}\times C_l$；修复A.3漏$\sum_d$和维度标注，不改正确终式。',
 r'Let $D=\mathrm{riesz}(J)$ be the final spatial gradient. The one-layer real adjoint is $(A^*D)_c(x)=\sum_{d,t,s}W_{dcts}D_d(x-(t,s))$, including every output channel $d$. Its DFT is $\overline T^{\top}\widehat D$. Adjoints reverse the composition order, so the middle gradient $D_l$ satisfies $\widehat D_l(k)=\overline{\mathbb T^{(k)(L:l+1)}}^{\top}\widehat D(k)$. Matrix $T^{(l)}$ has shape $C_l\times C_{l-1}$; its conjugate transpose and the transposed-update outer product have shape $C_{l-1}\times C_l$. This repairs the omitted $\sum_d$ and transpose annotation in A.3 while preserving the correct final formula.',
 r'\widehat D_l(k)=\overline{\mathbb T^{(k)(L:l+1)}}^{\top}\widehat D(k)',refs(matrix,'riesz_pullback','pullback_spectrum','conjugate_transpose_comp','network_pullback_spectrum','actual_suffix_cotangent')),
 st('按归一化谱应用Parseval','Apply Parseval with the normalized spectrum',
 r'定义$E(k)=\widehat D(k)/(MN)$，则$E_l(k)=\overline{\mathbb T^{(k)(L:l+1)}}^{\top}E(k)$。真实核坐标导数$r_{dcts}=\sum_xF_c(x+(t,s))D_{l,d}(x)$，Parseval给$r_{dcts}=\sum_k\overline{\chi_k(t,s)\widehat F_c(k)}E_{l,d}(k)$。用有限$\chi_{k,uv}=(MN)^{-1}\sum_{t,s<K}\chi_{uv}(t,s)\overline{\chi_k(t,s)}$，正相位梯度响应等于$MNq_{dc}(u,v)$，其中$q_{dc}=\sum_k\chi_{k,uv}\overline{\widehat F_c(k)}E_{l,d}(k)$。相同频率仍取有限和合法值，不能丢掉对角项。',
 r'Define $E(k)=\widehat D(k)/(MN)$; then $E_l(k)=\overline{\mathbb T^{(k)(L:l+1)}}^{\top}E(k)$. The actual kernel-coordinate derivative is $r_{dcts}=\sum_xF_c(x+(t,s))D_{l,d}(x)$. Parseval gives $r_{dcts}=\sum_k\overline{\chi_k(t,s)\widehat F_c(k)}E_{l,d}(k)$. With the finite sum $\chi_{k,uv}=(MN)^{-1}\sum_{t,s<K}\chi_{uv}(t,s)\overline{\chi_k(t,s)}$, the positive-phase gradient response is $MNq_{dc}(u,v)$, where $q_{dc}=\sum_k\chi_{k,uv}\overline{\widehat F_c(k)}E_{l,d}(k)$. Equal-frequency terms retain their legitimate finite-sum values and are never dropped.',
 r'E=\widehat D/(MN),\quad q_{dc}(u,v)=\sum_k\chi_{k,uv}\overline{\widehat F_c(k)}E_{l,d}(k)',refs(matrix,'actual_kernel_spectral_gradient','actual_real_network_spectrum')),
 st('连接实际前缀与精确参数更新','Connect the actual prefix and exact parameter update',
 r'前缀$\widehat F(k)=\mathbb T^{(k)(l-1:1)}g(k)+\delta_k\beta^{\prime}$包含全部$MN$偏置。由于$T$对真实$W$线性，更新$W-\eta\nabla_W Loss$精确给$\Delta T=-\eta MNq$；代入前缀谱和后缀伴随即原Eq5。论文适配把实际HasFDerivAt与使用$\mathrm{fderiv}$的更新写成一个合取，确保同一loss和状态。作者完整共轭梯度按实Riesz梯度读取；标准Wirtinger导数另有二倍换算，不能混用。',
 r'The actual prefix spectrum $\widehat F(k)=\mathbb T^{(k)(l-1:1)}g(k)+\delta_k\beta^{\prime}$ retains every $MN$ bias. Since $T$ is linear in real $W$, the update $W-\eta\nabla_W Loss$ gives the exact $\Delta T=-\eta MNq$. Substituting the actual prefix spectrum and suffix adjoint yields source Equation (5). The paper adapter conjoins the actual HasFDerivAt statement with the update using $\mathrm{fderiv}$, binding the same loss and state. Read the author’s full conjugate gradient as the real Riesz gradient; standard Wirtinger derivatives require a separate factor-of-two conversion.',
 r'\Delta T_{dc}(u,v)=-\eta MN\sum_k\chi_{k,uv}\overline{\widehat F_c(k)}\left[\overline{\mathbb T^{(k)(L:l+1)}}^{\top}E(k)\right]_d',refs(matrix,'actual_prefix_suffix_response_update')+['PaperDecoder.actual_corollary_3_4'])
 ],('同一真实实网络状态与loss的可微性→全异宽前缀/后缀→完整偏置→实Riesz梯度→原完整共轭/MN更新已验证；普通正弦商零域以有限χ修复，原错步可追溯。',
 'The derivative of the same actual real-network loss and state is connected to heterogeneous prefixes/suffixes, complete biases, the real Riesz gradient and the full conjugated/MN update. Finite χ repairs the ordinary sine-quotient domain; original erroneous proof steps remain traceable.'),'theorem_proof')
 rows['backpropagation']['proof_scope']='full_original_statement_with_finite_sum_domain_repair'
 rows['backpropagation']['rewrite_role']='proof'
 r=rows['independence-scope']
 r['proof_steps'][1]['lean_refs']=refs(weak,'actual_w1_law','actual_w2_law','actual_first_product_factorization','standard_gaussian_fourth_moment','actual_unit_kernel_weak_counterexample','actual_not_independent')
 r['translations']['en']['proof_steps'][1]['lean_refs']=r['proof_steps'][1]['lean_refs']
 r['scope']='真实独立层模型与实际U/BU Gaussian核反例均已验证：弱一阶显示式不推出二阶分解；不将该反例冒称真正独立prose模型的反例。'
 r['translations']['en']['scope']='Both the genuinely independent layer model and the actual U/BU Gaussian-kernel witness are verified. The weak first-moment displays do not imply second-moment factorization; this witness does not refute the genuinely independent prose model.'
 r['lean']['scope']=r['scope'];r['lean']['translations']['en']['scope']=r['translations']['en']['scope']
 r['lean']['declarations']=list(dict.fromkeys(n for x in r['proof_steps'] for n in x['lean_refs']));r['lean']['evidence_role']='counterexample'
 channelass=r'本条按A.4强prose条件证明：各层真实实Gaussian核；核内元素独立，每个输出行的不同输入核向量联合独立，整个层向量跨层联合独立。另保留每个前缀矩阵同一输入列的所有输出条目联合独立（Lean的hprefix），这是作者额外“所有元素独立”文字的模型读取，不能由层间独立或$d\ne d^{\prime}$且$c\ne c^{\prime}$的一阶显示式推出。所有$C_l>1$。'
 channelen=r'This entry proves the strong A.4 prose model: actual real Gaussian kernels, independence within kernels, joint independence of input-kernel vectors in each output row, and joint independence of whole layers. It explicitly retains joint independence of all output entries in each fixed input column of every prefix matrix (Lean hprefix). This reads the additional “all elements independent” prose and is not derived from layer independence or the first-moment display requiring both $d\ne d^{\prime}$ and $c\ne c^{\prime}$. All $C_l>1$.'
 replace('multi-channel-moments',[
 st('从实际Gaussian核获得每个响应矩','Obtain every response moment from actual Gaussian kernels',
 r'令$z_l=\mu_lR_{uv}$、$a_l=|z_l|^2+K^2\sigma_l^2$。实际有限实核相位和给$\mathbb ET_{dj}^{(l)}=z_l$及$\mathbb E|T_{dj}^{(l)}|^2=a_l$，同时提供可测性和$L^2$。真实层矩阵由这些响应组成，前缀$P_l=T_l\cdots T_1$按原顺序定义。当前层向量与过去全部层向量的独立性经可测复合得到当前行与整个旧列独立，不把待证矩等式放进假设。',
 r'Put $z_l=\mu_lR_{uv}$ and $a_l=|z_l|^2+K^2\sigma_l^2$. The actual finite real-kernel phase sum gives $\mathbb ET_{dj}^{(l)}=z_l$ and $\mathbb E|T_{dj}^{(l)}|^2=a_l$, together with measurability and $L^2$. These responses form the actual layer matrices, with $P_l=T_l\cdots T_1$ in source order. Independence of the current layer from all past layers is transported through measurable composition to independence of the current row and whole old column. No desired moment identity is assumed.',
 r'z_l=\mu_lR_{uv},\qquad a_l=|z_l|^2+K^2\sigma_l^2',refs(multi,'independent_layer_prefix','actual_gaussian_row_moments','kernelMatrices')+names('actual_kernel_mean','actual_kernel_second_moment')),
 st('推导均值与共轭二阶递推','Derive the mean and conjugated second-moment recurrences',
 r'均值从$\mathbb E\sum_jT_{dj}P_{jc}=\sum_j(\mathbb ET_{dj})(\mathbb EP_{jc})$得$m_l=C_{l-1}z_lm_{l-1}$。平方模展开为$\sum_{j,k}T_{dj}\overline{T_{dk}}P_{jc}\overline{P_{kc}}$；当前行与旧列独立先分解两向量积分，再分别用行内和前缀同列的真实独立性。$j=k$有$C_{l-1}$项，每项$a_ls_{l-1}$；$j\ne k$有$C_{l-1}(C_{l-1}-1)$项，每项$|z_lm_{l-1}|^2$。$L^2$及独立乘积保证这些复积分存在。因此$s_l=C_{l-1}a_ls_{l-1}+C_{l-1}(C_{l-1}-1)|z_lm_{l-1}|^2$。hprefix是这里明确使用的模型条件，没有证明它由一般深层iid网络自动产生。',
 r'The mean follows from $\mathbb E\sum_jT_{dj}P_{jc}=\sum_j(\mathbb ET_{dj})(\mathbb EP_{jc})$: $m_l=C_{l-1}z_lm_{l-1}$. Expand the squared magnitude as $\sum_{j,k}T_{dj}\overline{T_{dk}}P_{jc}\overline{P_{kc}}$. Independence of the current row and old column first factors the two vector integrals; then use actual row independence and prefix-column independence. There are $C_{l-1}$ diagonal terms $a_ls_{l-1}$ and $C_{l-1}(C_{l-1}-1)$ off-diagonal terms $|z_lm_{l-1}|^2$. The $L^2$ and independent-product arguments make these complex integrals well defined. Thus $s_l=C_{l-1}a_ls_{l-1}+C_{l-1}(C_{l-1}-1)|z_lm_{l-1}|^2$. This explicitly uses hprefix; it does not derive that assumption from a general deep iid network.',
 r'm_l=C_{l-1}z_lm_{l-1},\quad s_l=C_{l-1}a_ls_{l-1}+C_{l-1}(C_{l-1}-1)|z_lm_{l-1}|^2',refs(multi,'complex_cross_moment','row_column_mean','row_column_second_moment','actual_cascade_uniform_moments')),
 st('有限展开并核对Eq31–32指标','Expand finitely and align the indices in (31)–(32)',
 r'基例$m_1=z_1,s_1=a_1$。归纳得$m_L=C_L^{-1}\prod_{j=1}^LC_jz_j$。令$d_l=C_{l-1}a_l$、$e_l=C_{l-1}(C_{l-1}-1)|z_lm_{l-1}|^2$，逐次展开$s_l=d_ls_{l-1}+e_l$得$s_L=s_1\prod_{j=2}^Ld_j+\sum_{l=2}^Le_l\prod_{j=l+1}^Ld_j$。因$C_{l-1}>0$，均值递推给$e_l=(C_{l-1}-1)C_{l-1}^{-1}|m_l|^2$，代回即原Eq32：$s_L=C_L^{-1}\prod_{j=1}^LC_ja_j+\sum_{l=2}^L\frac{C_{l-1}-1}{C_{l-1}}\left|C_l^{-1}\prod_{j=1}^lC_jz_j\right|^2\prod_{k=l+1}^LC_{k-1}a_k$。Lean零起始指标$n=L-1,i=l-2$；逆$C_l$确在平方模内，末端空积1。',
 r'The base cases are $m_1=z_1,s_1=a_1$. Induction gives $m_L=C_L^{-1}\prod_{j=1}^LC_jz_j$. With $d_l=C_{l-1}a_l$ and $e_l=C_{l-1}(C_{l-1}-1)|z_lm_{l-1}|^2$, finite expansion of $s_l=d_ls_{l-1}+e_l$ gives $s_L=s_1\prod_{j=2}^Ld_j+\sum_{l=2}^Le_l\prod_{j=l+1}^Ld_j$. Since $C_{l-1}>0$, the mean recurrence gives $e_l=(C_{l-1}-1)C_{l-1}^{-1}|m_l|^2$. Substitution yields source Equation (32): $s_L=C_L^{-1}\prod_{j=1}^LC_ja_j+\sum_{l=2}^L\frac{C_{l-1}-1}{C_{l-1}}\left|C_l^{-1}\prod_{j=1}^lC_jz_j\right|^2\prod_{k=l+1}^LC_{k-1}a_k$. Lean uses $n=L-1,i=l-2$; the inverse $C_l$ lies inside the squared magnitude, and terminal empty products equal one.',
 r'm_L=\frac1{C_L}\prod_{j=1}^LC_jz_j,\quad s_L=\frac1{C_L}\prod_{j=1}^LC_ja_j+\sum_{l=2}^L\frac{C_{l-1}-1}{C_{l-1}}\left|\frac1{C_l}\prod_{j=1}^lC_jz_j\right|^2\prod_{k=l+1}^LC_{k-1}a_k',refs(multi,'finite_affine_expansion','mean_sequence_source_closed','som_sequence_source_closed','actual_gaussian_cascade_closed')+['PaperDecoder.actual_appendix_equations31_32']),
 st('保留弱显示式与增长解释的范围','Retain the weak-display and growth boundaries',
 r'上述是真实随机矩阵级联的条件性有限闭式。原仅一阶$d\ne d^{\prime},c\ne c^{\prime}$显示式未控制同列的共轭交叉矩，不能删去hprefix；U/BU机器实例已显示一阶分解不足。闭式中的正因子也可能小于1，不能从有限展开推出普遍指数增加；单通道实际Gaussian递减反例在独立条目登记。',
 r'The result is a conditional finite formula for an actual random-matrix cascade. The weak first-moment display for $d\ne d^{\prime},c\ne c^{\prime}$ does not control same-column conjugated cross moments, so hprefix cannot be removed. The machine U/BU witness already shows the inadequacy of first-moment factorization. Positive factors can also be below one; finite expansion does not imply universal exponential increase. The actual scalar Gaussian decay witness is indexed separately.',
 '',refs(weak,'actual_unit_kernel_weak_counterexample'))
 ],('实际Gaussian核→真实矩阵级联均值/SOM递推→有限闭式Eq31/32完整验证于上述强独立模型。hrow/hprefix保留且未从原弱显示等式推导；因此对原弱读取及附带普遍增长解释仍为条件性有效分量。',
 'Actual Gaussian kernels, random-matrix cascade recurrences and finite Equations (31)–(32) are fully verified in the explicitly stated strong independence model. hrow/hprefix remain premises and are not derived from the weak displays; the original weak reading and universal growth interpretation therefore retain conditional component scope.'),'partial_component',[GAUSS,(channelass,channelen)])
 for s in ['moment-parameter-growth','frequency-preference','mean-preference']:
  r=rows[s];r['lean']['evidence_role']='partial_component'
 r=rows['moment-parameter-growth']
 r['proof_steps'][0]['lean_refs']=['PaperDecoder.moment_factor_mono']
 r['proof_steps'][1]['lean_refs']=refs(param,'gaussian_kernel_coordinate_law','gaussian_kernel_independent','actual_kernel_som','actual_kernel_size_growth_counterexample')
 r['scope']='固定量的非严格单调性和真实独立Gaussian核K反例已验证；K与R按实际核同时改变。普遍严格增长与训练难度并未由这些结果证明。'
 r['translations']['en']['scope']='Non-strict monotonicity with fixed quantities and the actual independent-Gaussian K witness are verified. K and R change together in the real kernel. These results do not prove universal strict growth or learning difficulty.'
 r=rows['frequency-preference'];r['proof_steps'][0]['lean_refs']=['PaperDecoder.finite_moment_ratio']+names('actual_independent_layer_moments')
 r['scope']='真实独立层SOM及有限乘积比已验证（普通比值需分母正）；从矩/LLN到单网络学习偏好的未量化推断只给范围说明，未冒充概率定理。'
 r['translations']['en']['scope']='The actual independent-layer SOM and finite product ratio are verified (ordinary ratios require positive denominators). The unquantified inference from moments/LLN to one network’s learning preference remains a scope analysis, not a probability theorem.'
 r=rows['mean-preference'];r['proof_steps'][0]['lean_refs']=['PaperDecoder.mean_preference_ratio_mono']+names('actual_kernel_second_moment')
 r['proof_steps'][0]['body_md']+=r'精确条件写为$r_{\rm low}=|R_{\rm low}|^2\ge r_{\rm high}=|R_{\rm high}|^2\ge0$、$t=|\mu|^2\ge0$和$c=K^2\sigma^2>0$；$t$增加时$(tr_{\rm low}+c)/(tr_{\rm high}+c)$非减，由正分母交叉相乘得$c(t_1-t_0)(r_{\rm low}-r_{\rm high})\ge0$。'
 r['translations']['en']['proof_steps'][0]['body_md']+=r' Precisely, let $r_{\rm low}=|R_{\rm low}|^2\ge r_{\rm high}=|R_{\rm high}|^2\ge0$, $t=|\mu|^2\ge0$, and $c=K^2\sigma^2>0$. Increasing $t$ makes $(tr_{\rm low}+c)/(tr_{\rm high}+c)$ nondecreasing: cross-multiplication by positive denominators reduces this to $c(t_1-t_0)(r_{\rm low}-r_{\rm high})\ge0$.'
 r['scope']='真实核矩公式和均值强度的条件性矩比单调性已验证；c>0为该普通比值的适用域，不加入原全称学习解释。μ=0/K=1等退化偏好边界保留。'
 r['translations']['en']['scope']='The actual kernel moment and conditional monotonicity of its ratio in mean strength are verified. c>0 delimits the ordinary ratio and is not added to the source universal learning interpretation. Zero-mean/K=1 preference boundaries remain.'
 r=rows['kernel-preference']
 r['proof_steps'][0]['lean_refs']=refs(param,'phase_sum_dc','phase_sum_two_40','phase_sum_four_40','kernel_size_two_dc_ratio','kernel_size_four_dc_ratio')
 r['proof_steps'][0]['body_md']=r'本例$M=N=8,\mu=1,\sigma^2=1$。DC每个相位1，$R_{00}=K^2$；频率$(4,0)$的$t$相位是$(-1)^t$，偶$K=2,4$相消，$R_{40}=0$。因此实际独立Gaussian核有$SOM_{00}=K^4+K^2$、$SOM_{40}=K^2$，矩比$K^2+1$给5与17。与前条$\sigma^2=1/16$的下降反例不同，本例用$\sigma^2=1$。'
 r['translations']['en']['proof_steps'][0]['body_md']=r'Here $M=N=8,\mu=1,\sigma^2=1$. Every DC phase is one, so $R_{00}=K^2$. At frequency $(4,0)$ the $t$ phase is $(-1)^t$, cancelling for even $K=2,4$, so $R_{40}=0$. Actual independent Gaussian kernels therefore have $SOM_{00}=K^4+K^2$ and $SOM_{40}=K^2$, giving ratios $K^2+1$, namely 5 and 17. This example uses $\sigma^2=1$, distinct from the preceding decay example with $\sigma^2=1/16$.'
 r['proof_steps'][1]['lean_refs']=refs(param,'actual_kernel_dc_ratio_counterexample')
 r['lean']['evidence_role']='counterexample'
 r['scope']='实际独立Gaussian核、真实相位和、DC/高频积分矩及5→17的不均衡反例完整验证；仅反驳大核普遍缓解该不均衡的解释。'
 r['translations']['en']['scope']='Actual independent Gaussian kernels, phase sums, DC/high-frequency moment integrals and the 5→17 imbalance witness are verified. Only the universal large-kernel alleviation interpretation is refuted.'
 for s in ['moment-parameter-growth','frequency-preference','mean-preference','kernel-preference']:
  r=rows[s];r['lean']['scope']=r['scope'];r['lean']['translations']['en']['scope']=r['translations']['en']['scope']
  r['lean']['declarations']=list(dict.fromkeys(n for x in r['proof_steps'] for n in x['lean_refs']))
  for q,e in zip(r['proof_steps'],r['translations']['en']['proof_steps']):e['lean_refs']=q['lean_refs']
 # All source proofs remain unchanged; this annotates completed engineering only.
 for issue in p.issues:
  if issue['id']=='decoder-issue-backprop-bars':
   issue['impact_md']='局部证明共轭修复；完整真实loss矩阵链现已实际验证。'
   issue['translations']['en']['impact_md']='A local conjugation repair; the complete actual-loss matrix chain is now verified.'

 # Apply log on the declared positive-factor domain; nondegenerate Gaussians
 # are a sufficient condition, not the only admissible case.
 r=rows['single-channel-moments']
 r['proof_steps'][2]['body_md']=r'先按本条已声明的每个矩因子$a_l>0$应用普通实$\log$乘积恒等式：$\log SOM(\mathbb T)=\sum_l\log a_l$。$K>0$且$\sigma_l^2>0$时$a_l\ge K^2\sigma_l^2>0$只是一个充分条件；$\sigma_l^2=0$但$|\mu_lR|>0$也在本范围。若某因子0，普通实$\log0$未定义，原log公式单列域边界，不利用Lean的总化log0值。'
 r['translations']['en']['proof_steps'][2]['body_md']=r'First apply the ordinary logarithmic product identity on the declared domain $a_l>0$: $\log SOM(\mathbb T)=\sum_l\log a_l$. The conditions $K>0$ and $\sigma_l^2>0$ imply $a_l\ge K^2\sigma_l^2>0$ and are sufficient rather than necessary; $\sigma_l^2=0$ with $|\mu_lR|>0$ is also covered. If a factor is zero, the ordinary $\log0$ is undefined. That source-domain boundary is retained rather than using Lean’s totalized log0 value.'
 # Keep the same TeX expressions in both languages, including their domains.
 english={
 ('orthogonality',1):r'Substitute the DFT into its inverse and exchange finite sums. Orthogonality retains only the original position. The factor $MN$ cancels $(MN)^{-1}$. Both directions hold for arbitrary complex inputs.',
 ('valid-convolution',0):r'For general output sampling, first extend the input periodically on the old cyclic grid so every positive offset is defined, then take arbitrary $M^{\prime},N^{\prime}>0$. Substituting the input inverse DFT into actual positive-offset convolution and exchanging finite sums gives $\widehat h_d(k^{\prime})=M^{\prime}N^{\prime}\delta_{k^{\prime},0}b_d+\sum_c\sum_k\alpha_{k^{\prime}k}T_{dc}(k)\widehat f_c(k)$, where $\alpha_{k^{\prime}k}=(MN)^{-1}\sum_{m<M^{\prime},n<N^{\prime}}\chi_k(m,n)\overline{\chi_{k^{\prime}}^{\prime}(m,n)}$. The source valid convolution additionally requires $1\le K\le\min(M,N)$ to prevent wrapping; put $M^{\prime}=M-K+1,N^{\prime}=N-K+1$. The sine numerator omits one term, while the original phase correctly uses the term count minus one.',
 ('valid-convolution',1):r'Take $M=N=3,K=2,u=v=0,u^{\prime}=v^{\prime}=1$, so $\lambda=\gamma=-1/2$. The correct sum is $(1+e^{-i\pi})^2/9=0$. Both printed ratios equal one and their phase is $e^{-i\pi}=-1$, giving $-1/9$, with no zero denominator. The same coefficient witness is connected to real input $f\equiv1$ and the $\delta_{00}$ kernel: the old spectrum is 9 only at DC; the actual $2\times2$ output is constant one, with spectrum zero at $(1,1)$, whereas the printed coefficient predicts $(-1/9)\cdot1\cdot9=-1$. Thus actual operators are compared.',
 ('backpropagation',0):r'Fix source layer $l$, its actual real weights $W$, constant channel bias $b$, and the prefix and suffix. Let $F$ be the actual prefix output and $S$ the ordered affine suffix. Assume the loss at the actual $S(\mathrm{Conv}_W(F)+b)$ has real Fréchet derivative $J$. The parameter-to-middle-output map is continuous linear $B_F$ and the suffix derivative is its actual ordered operator $A_S$. The chain rule gives $d_W Loss=J\circ A_S\circ B_F$, with the same $J,W,F$ in the update. Parameter basis vectors give real coordinate gradients; $T$ is not an independent complex parameter.',
 ('independence-scope',1):r'Reading only the displays, take $K=1,L=2$ with one channel. Let $U\sim\mathcal N(0,1)$ and an independent uniform sign $B\in\{-1,1\}$, with $W_1=U,W_2=BU$. Both marginal laws are standard Gaussian and $\mathbb E[W_1W_2]=\mathbb E[B]\mathbb E[U^2]=0$, satisfying Equation (7); Equation (6) has no single-channel instance. But $\mathbb E|W_1W_2|^2=\mathbb EU^4=3\ne1$. This shows that the weak displays are insufficient, without refuting genuine independence.',
 ('gaussian-response',0):r'Independent real Gaussian weights $W_t$ form a jointly Gaussian real vector. Each $e^{i\theta_t}W_t$ is a real continuous linear map into $\mathbb C$, and independent Gaussian convolution gives a complex Gaussian response. For real $W$, pseudocovariance is $\mathbb E(W-\mu)^2=\sigma^2$; the circular-Gaussian replacement in A.4 is incorrect.',
 ('gaussian-response',1):r'Linearity gives $\mathbb ET=\sum_t\mu e^{i\theta_t}=\mu R$. Independence makes distinct centered cross terms zero, and each diagonal variance contributes $\sigma^2$. Hence $V(T)=K^2\sigma^2$ and $SOM(T)=|\mu R|^2+K^2\sigma^2$. These conclusions use actual Gaussian laws and squared-magnitude integrals.',
 ('single-channel-moments',0):r'Each $T_l$ is a measurable phase sum of its finite real kernel array. Measurable maps preserve independence of whole layer vectors, giving independent families $T_l$ and $|T_l|^2$. The complex Bochner product integral gives $\mathbb E\prod_lT_l=\prod_l\mathbb ET_l=\prod_l(\mu_lR_{uv})$. All Gaussian means are derived from actual laws rather than assuming the desired product identity.',
 ('single-channel-moments',2):r'First use the declared positive factors $a_l>0$ to apply the ordinary real $\log$ identity: $\log SOM(\mathbb T)=\sum_l\log a_l$. The conditions $K>0$ and $\sigma_l^2>0$ imply $a_l\ge K^2\sigma_l^2>0$ and are sufficient rather than necessary; $\sigma_l^2=0$ with $|\mu_lR|>0$ is also covered. If a factor is zero, ordinary $\log0$ is undefined. The source-domain boundary remains; Lean’s totalized log0 is not used.',
 ('multi-channel-moments',1):r'The mean follows from $\mathbb E\sum_jT_{dj}P_{jc}=\sum_j(\mathbb ET_{dj})(\mathbb EP_{jc})$: $m_l=C_{l-1}z_lm_{l-1}$. Expand the squared magnitude as $\sum_{j,k}T_{dj}\overline{T_{dk}}P_{jc}\overline{P_{kc}}$. Independence of the current row and old column factors their vector integrals; then use actual row and prefix-column independence. For $j=k$, there are $C_{l-1}$ terms $a_ls_{l-1}$. For $j\ne k$, there are $C_{l-1}(C_{l-1}-1)$ terms $|z_lm_{l-1}|^2$. The $L^2$ and independent-product arguments make the complex integrals well defined. Thus $s_l=C_{l-1}a_ls_{l-1}+C_{l-1}(C_{l-1}-1)|z_lm_{l-1}|^2$. This explicitly uses hprefix; its validity for a general deep iid network is not assumed automatically.',
 ('moment-parameter-growth',0):r'The factor $a_l$, with fixed $K,R$, is nondecreasing in $|\mu_l|$ and $\sigma_l^2$. With fixed $|\mu_l|$ it is nondecreasing in $|R|$. Growth can be non-strict: at $\mu_l=0$, R has no effect. Products of nonnegative factors preserve this monotonicity.',
 ('moment-parameter-growth',1):r'The phase sum $R_{uv}$ depends on K. Take $M=N=8,L=1,\mu=1,\sigma^2=1/16$ and frequency $(4,0)$. At K=1, R=1 and SOM is $17/16$; at K=2, the phases one and minus one cancel, R=0 and SOM is $1/4$. This refutes the universal increase-in-K subclause.',
 ('depth-growth',0):r'For every finite depth use a genuine product measure of $\mathcal N(0,1/4)$ weights and take $K=1$. Every layer response is its sole real weight at every frequency. The coordinate laws and independence follow from the actual product measure.',
 ('depth-growth',1):r'Independent products of squared magnitudes give the actual SOM $(1/4)^L$. Comparing depths two and one gives $1/16<1/4$. The factors are positive, so the source log-product identity still holds; unconditional increase does not.',
 ('zero-padding',1):r'Take $M=N=2,M^{\prime}=N^{\prime}=3$. All four pixels equal the same $U\sim\mathcal N(0,q)$, so every source Gaussian marginal holds. The old spectrum at (1,1) is zero; the new spectrum is $U(1+z)^2$ with $z=e^{-2\pi i/3}$ and $|1+z|^2=1$. Its SOM is q, whereas the source right-hand side at mean zero is zero.',
 ('natural-input',0):r'For one channel the exact identity $h=\mathbb Tg$ gives $|h|=|\mathbb T||g|$. For several channels there is only an upper bound $\|h\|\le\|\mathbb T\|_{\rm op}\|g\|$ without additional directional control. Cancellation or $\mathbb T=0$ shows that large input magnitude alone does not force large output magnitude or gradient.',
 ('cosine-dimension',0):r'High dimension alone gives no cosine bound: take $x=y=(1,\ldots,1)$ in arbitrarily high dimension, and cosine remains one. Adding a nonzero proportional difference, $y=(1+\epsilon)x$, still gives cosine one. Accumulating squared differences does not by itself control their directional projection.'
 }
 for (s,k),body in english.items():rows[s]['translations']['en']['proof_steps'][k]['body_md']=body
 r=rows['kernel-preference'];en=r['translations']['en']['proof_steps'][0]
 en['body_md']=en['body_md'].replace(r'This example uses $\sigma^2=1$, distinct from the preceding decay example with $\sigma^2=1/16$.',r'The preceding decrease example uses $\sigma^2=1/16$; this distinct example uses $\sigma^2=1$.')
 r=rows['zero-padding'];r['proof_steps'][0]['body_md']=r['proof_steps'][0]['body_md'].replace('$i.i.d.$','i.i.d.')

 r=rows['single-channel-moments']
 r['proof_steps'][2]['lean_refs']=['PaperDecoder.actual_positive_factor_log_som']
 r['translations']['en']['proof_steps'][2]['lean_refs']=r['proof_steps'][2]['lean_refs']
 r['lean']['declarations']=list(dict.fromkeys(n for x in r['proof_steps'] for n in x['lean_refs']))
 # Domain-only metadata must not imply a statement/clause counterexample.
 from status_correction import apply_status_correction
 for row in p.rows:apply_status_correction(row)
