# F06 transferred public modules — 2026-10-01

The three new modules are owned by `twelve_dynamics_math`; paper content, adapters, report and final admission remain with `twelve_foundations_math` and root. Earlier public files and barrels were not edited. Full source hashes and build/type/axiom evidence are in the companion JSON; the actual type output is `.tmp/decoder-transfer/types-and-axioms.log`. This is a module handoff, not a claim that F06 as a whole is admitted.

## Actual crop and valid convolution

`Harsanyi.Frequency.Valid` defines canonical-representative `cropIndex`, `crop`, and

$$\alpha_{k'k}=\frac1{MN}\sum_{x\in\mathrm{Grid}(A,B)}\chi_{k'}^{A,B}(-x)\chi_k^{M,N}(\mathrm{cropIndex}(x)).$$

The original and output DFTs are unnormalised. `inverse_dft2_character` evaluates the actual inverse transform. Substituting that evaluation into the actual cropped DFT and exchanging the two finite sums gives `crop_dft`. Applying the existing actual positive-offset convolution formula gives `cropped_offset_layer_dft`; isolating the constant bias directly on the output grid gives `cropped_offset_layer_dft_bias`:

$$\widehat h_d(k')=AB\,\mathbf1_{k'=0}b_d+\sum_k\alpha_{k'k}\sum_c T_{dc}(k)\widehat f_c(k).$$

Arbitrary positive A,B mean periodic extension followed by sampling/cropping; this theorem does not identify every padding operator with that sampling. `validLayer` instead explicitly samples integer sums of output coordinates and positive kernel offsets. `valid_layer_eq_crop` and `valid_layer_dft` connect this actual operator to the Fourier identity. For 0<K≤M,N and A=M−K+1, B=N−K+1, `valid_index_bounds` proves each integer sample is strictly below M,N and `valid_indices_no_wrap` proves its modular representative equals that physical integer sample. `realValidLayer` and `real_valid_layer_embedding` connect actual real input and real kernel sums to their complex embeddings.

中文：两次DFT均未归一化，输入逆变换贡献1/(MN)，输出常偏置的谱为AB倍偏置。公共证明先逐点代入真正逆DFT，再交换有限和，不假定频率之间独立。任意A,B仅描述周期延拓后裁剪/采样；无padding有效尺寸另外证明每个采样整数不越界且mod代表不绕回，因此确实与真实valid卷积一致。实输入和实核的嵌入逐项保留乘法与有限和。

For the Eq.(17) source clause, `deltaKernel` is the actual real 2×2 delta00 kernel and the input is identically1 on Grid(3,3). Its actual valid output is identically1 on Grid(2,2), whose new frequency(1,1) DFT is0. `original_constant_spectrum` proves the input has only original DC coefficient9. `actual_mixing_alpha_zero` proves the correct DC-to-(1,1) alpha is0. `frequencyDifference` is oldFreq/oldSize−outFreq/outSize, and `witness_grid_frequency_difference` binds the actual grid frequencies to −1/2. The literal source sine quotient in `printedValidAlpha` instead equals −1/9, with sine denominators nonzero. `actual_valid_equation17_counterexample` also binds the actual delta-kernel DC response and input DC spectrum: the printed prediction is −1 while the actual output coefficient is0. The printed phase is correct; its sine numerators omit one term.

中文：取原网格3×3、核2×2、有效输出2×2，全一实输入、delta00实核。原谱仅DC=9，实际新频率(1,1)为0；旧频0到新频1的真实频差为−1/2。两正弦分母均不为零，原alpha打印式为−1/9，乘实际核DC响应1和原谱9预测−1，故是完整实际卷积模型反例。错误在正弦分子少一项，不能误标原相位错误。

`exponential_sine_factor` proves the exact exponential difference. `geometric_sine_quotient` and its real version prove the n-term geometric polynomial formula

$$\sum_{t<n}e^{2it\theta}=e^{i(n-1)\theta}\frac{\sin(n\theta)}{\sin\theta},\qquad\sin\theta\ne0.$$

The finite polynomial remains defined at zero-denominator boundaries. The old public `geometric_one`, `geometric_root` and direct finite sums provide those branches; the sine quotient is not used there. 中文：n项和的正弦分子为sin(nθ)，相位用(n−1)θ。仅在正弦分母非零时使用商，边界直接使用有限多项式，不补一个没有来源的商值。

## Actual Gaussian kernel-size counterexamples

`Harsanyi.Frequency.Parameters.gaussianKernelSpace K m q` is the actual finite product of N(m,q) laws over K×K real kernel coordinates. Coordinate laws and full independence are proved. `kernelSOM` integrates the norm square of the existing actual positive-offset `randomKernelResponse`; `actual_kernel_som` reuses the existing general Gaussian theorem:

$$SOM_K(u,v)=|mR_K(u,v)|^2+K^2q.$$

On Grid(8,8) at frequency(4,0), `phase_sum_one` is1 and `phase_sum_two_40`, `phase_sum_four_40` are0. For m=1,q=1/16, `kernel_size_one_som` is17/16 and `kernel_size_two_som` is1/4. Thus `actual_kernel_size_growth_counterexample` strictly refutes universal increase with K. Separately, m=1,q=1 gives actual DC/non-DC ratios5 for K=2 and17 for K=4, proved by `kernel_size_two_dc_ratio`, `kernel_size_four_dc_ratio` and `actual_kernel_dc_ratio_counterexample`. These two witnesses have different permitted Gaussian variance choices; they must not be presented as a single parameter setting.

中文：真实有限Gaussian乘积律证明每个核坐标的边缘及联合独立，SOM是实际核响应模平方积分，不是把期望末式当假设。8×8网格频率(4,0)的相位和在K=1为1、在K=2/4为0。第一组m=1,q=1/16给17/16降到1/4；另一组m=1,q=1给DC/该非DC的比率从5升到17。两组参数不同，应在适配中分别列出。

## Actual weak first-moment condition

`Harsanyi.Frequency.WeakIndependence.signGaussianSpace` is an actual product of a fair Boolean sign and standard Gaussian U. Define W1=U and W2=BU. `joint_map_split` proves the actual sign-conditioned mixture law; Gaussian symmetry gives `actual_w2_law`, while `actual_w1_law` follows from the product marginal. Both are N(0,1). The sign and U are actually independent, but W1 and W2 are not.

The fair sign mean is0, so the actual first product is E(BU²)=0=EW1·EW2. The fourth derivative of the actual standard Gaussian MGF exp(t²/2) at0 gives `standard_gaussian_fourth_moment`=3. Pointwise B²=1 then gives E|W1W2|²=EU⁴=3, whereas the individual second moments are1. `actual_weak_first_moment_counterexample` binds actual normal marginals, the displayed first-moment factorization and the failed second-moment factorization. `actual_not_independent` proves nonindependence by applying independence to the squared coordinates and contradicting3≠1.

`actual_unit_kernel_response` connects each real random variable to an actual singleton square convolution kernel. `actual_unit_kernel_product_som`=3, `actual_unit_kernel_each_som`=(1,1), `actual_unit_kernel_first_factorization` and `actual_unit_kernel_weak_counterexample` therefore make the same witness an actual two-layer Fourier-response example at any permitted grid frequency. This refutes sufficiency of the displayed weak first-moment condition for the SOM product claim. It does not refute the valid fully independent-layer theorem.

中文：在真正独立的公平sign×标准Gaussian空间中取W1=U、W2=BU；Gaussian反射同律证明W2也是N(0,1)。原显示的一阶乘积条件确实成立，但两者模平方乘积期望为3而非1。四阶矩不是假设，由实际MGF四次导数证明；平方独立的必要因子化反过来证W1/W2并不独立。再逐点证明单元素实际卷积核响应就是对应实变量的复嵌入，将一阶条件和失败的SOM乘积都连接到真实两层频域对象。真正联合独立层的有效定理不受此反例影响。
