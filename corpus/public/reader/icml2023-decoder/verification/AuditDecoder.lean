import Lean.Util.CollectAxioms
import Harsanyi.Extensions.DecoderMatrixBackprop
import Harsanyi.Extensions.DecoderMultiChannel
import Harsanyi.Extensions.DecoderCounterexample
import Harsanyi.Extensions.DecoderPadding
import Harsanyi.Extensions.DecoderUpsampling
import Harsanyi.Extensions.DecoderDepthCounterexample
import Harsanyi.Extensions.DecoderValid
import Harsanyi.Extensions.DecoderParameterCounterexamples
import Harsanyi.Extensions.DecoderWeakIndependence

/-! Formal-paper adapters. Each actual loss derivative is tied to the same
network state and functional used in its frequency update. -/
namespace PaperDecoder
open Harsanyi.Frequency Harsanyi.Frequency.MatrixBackprop Finset
open scoped BigOperators
variable {M N K : ℕ} [NeZero M] [NeZero N]
variable (P S : ℕ → Type*) [∀ n,Fintype (P n)] [∀ n,DecidableEq (P n)]
variable [∀ n,Fintype (S n)] [∀ n,DecidableEq (S n)]

theorem actual_corollary_3_4
    (pw : ∀ n,P (n+1) → P n → Fin K × Fin K → ℝ)
    (pb : ∀ n,P (n+1) → ℝ)
    (input : Feature (M:=M) (N:=N) (P 0)) (p : ℕ)
    (sw : ∀ n,S (n+1) → S n → Fin K × Fin K → ℝ)
    (sb : ∀ n,S (n+1) → ℝ) (L : ℕ)
    (w : S 0 × P p × (Fin K × Fin K) → ℝ) (b : S 0 → ℝ)
    (Loss : Feature (M:=M) (N:=N) (S L) → ℝ)
    (J : Feature (M:=M) (N:=N) (S L) →L[ℝ] ℝ)
    (hLoss : HasFDerivAt Loss J (realNetwork S (squareShift K) sw sb
      (realKernelCLM (squareShift K)
        (fun c x => realNetwork P (squareShift K) pw pb input p (c,x)) w +
        fun y => b y.1) L))
    (d : S 0) (c : P p) (η : ℝ) (u : ZMod M) (v : ZMod N) :
    let F := realNetwork P (squareShift K) pw pb input p
    let wholeLoss := fun z => Loss (realNetwork S (squareShift K) sw sb
      (realKernelCLM (squareShift K) (fun c x => F (c,x)) z+fun y => b y.1) L)
    let gradient := (J.comp (networkCLM S (squareShift K) sw L)).comp
      (realKernelCLM (squareShift K) (fun c x => F (c,x)))
    HasFDerivAt wholeLoss gradient w ∧
      offsetResponse (squareShift K)
        (fun t => ((w (d,c,t)-η*(fderiv ℝ wholeLoss w) (Pi.single (d,c,t) 1) : ℝ) : ℂ)) u v -
        offsetResponse (squareShift K) (fun t => (w (d,c,t) : ℂ)) u v =
      -(η : ℂ)*((M*N : ℕ) : ℂ)*
        ∑ k : Grid M N,crossFrequencyKernel (squareShift K) u k.1 v k.2 *
          starRingEnd ℂ (featureSpectrum F k.1 k.2 c) *
          conjugateTranspose (cascadeLinear S
            (fun n => responseLinear (squareShift K) (sw n) k.1 k.2) L)
            (normalizedSpectrum (riesz J) k.1 k.2) d := by
  dsimp only
  have hD := actual_cascade_parameter_loss_hasFDerivAt P S (squareShift K)
    pw pb input p sw sb L w (fun y => b y.1) Loss J hLoss
  constructor
  · exact hD
  · rw [hD.fderiv,actual_response_gradient_update,actual_kernel_spectral_gradient,mul_assoc]
    congr 1
    congr 1
    apply sum_congr rfl
    intro k _
    rw [actual_suffix_cotangent]

section GaussianCascade
open MeasureTheory ProbabilityTheory Harsanyi.Frequency.MultiChannel
variable {Ω : Type*} [MeasurableSpace Ω]
variable (μ : Measure Ω) [IsProbabilityMeasure μ]

/-- A.4 Equations (31)--(32), under the genuinely independent reading of the
additional prose. Prefix-column independence remains explicit: it is not
inferred from the weaker first-moment displays or from layer independence. -/
theorem actual_appendix_equations31_32
    (W : ∀ n,S (n+1) → S n → Fin K × Fin K → Ω → ℝ)
    (hmW : ∀ n d c t,Measurable (W n d c t))
    (m : ℕ → ℝ) (q : ℕ → NNReal)
    (hl : ∀ n d c t,μ.map (W n d c t) = gaussianReal (m n) (q n))
    (hwithin : ∀ n d c,iIndepFun (W n d c) μ)
    (hrows : ∀ n d,iIndepFun (fun c ω t => W n d c t ω) μ)
    (hlayers : iIndepFun (fun n ω d c t => W n d c t ω) μ)
    (u : ZMod M) (v : ZMod N)
    (hprefix : ∀ n c,iIndepFun
      (fun d => cascadeEntry S (kernelMatrices S W u v) (n+1) c d) μ)
    (n : ℕ) (hC : ∀ j≤n,1 < Fintype.card (S (j+1)))
    (c : S 0) (d : S (n+1)) :
    (∫ ω,cascadeEntry S (kernelMatrices S W u v) (n+1) c d ω ∂μ) =
      sourceMean S (fun j => (m j : ℂ)*phaseSum (K:=K) u v) n ∧
    (∫ ω,Complex.normSq (cascadeEntry S (kernelMatrices S W u v) (n+1) c d ω) ∂μ) =
      sourceSOM S (fun j => (m j : ℂ)*phaseSum (K:=K) u v)
        (fun j => Complex.normSq ((m j : ℂ)*phaseSum (K:=K) u v)+(K*K : ℕ)*(q j : ℝ)) n := by
  exact actual_gaussian_cascade_closed μ S W hmW m q hl hwithin hrows hlayers
    u v hprefix n (fun j hj => Nat.ne_of_gt (lt_trans (by decide) (hC j hj))) c d
end GaussianCascade
/-- Ratios of the independently proved finite products, on their ordinary
nonzero denominator domain. This does not assert a training probability. -/
theorem finite_moment_ratio (a b : Fin L → ℝ) :
    (∏ l,a l)/(∏ l,b l) = ∏ l,a l/b l := by
  exact (Finset.prod_div_distrib a b).symm

theorem moment_factor_mono {r₀ r₁ t₀ t₁ c₀ c₁ : ℝ}
    (hr₀ : 0≤r₀) (ht₀ : 0≤t₀) (hr : r₀≤r₁) (ht : t₀≤t₁) (hc : c₀≤c₁) :
    t₀*r₀+c₀ ≤ t₁*r₁+c₁ := by
  nlinarith [mul_nonneg (sub_nonneg.mpr ht) (sub_nonneg.mpr hr)]

theorem mean_preference_ratio_mono {rLow rHigh t₀ t₁ c : ℝ}
    (hr : 0≤rHigh) (hLH : rHigh≤rLow) (ht : 0≤t₀)
    (hT : t₀≤t₁) (hc : 0<c) :
    (t₀*rLow+c)/(t₀*rHigh+c) ≤ (t₁*rLow+c)/(t₁*rHigh+c) := by
  have h0 : 0<t₀*rHigh+c := add_pos_of_nonneg_of_pos (mul_nonneg ht hr) hc
  have h1 : 0<t₁*rHigh+c := add_pos_of_nonneg_of_pos
    (mul_nonneg (le_trans ht hT) hr) hc
  rw [div_le_div_iff₀ h0 h1]
  nlinarith [mul_nonneg (sub_nonneg.mpr hT) (sub_nonneg.mpr hLH),
    mul_nonneg (mul_nonneg (sub_nonneg.mpr hT) (sub_nonneg.mpr hLH)) hc.le]

section PositiveMomentFactors
open MeasureTheory ProbabilityTheory
variable {Ω ι : Type*} [MeasurableSpace Ω] [Fintype ι] [DecidableEq ι]
variable (μ : Measure Ω) [IsProbabilityMeasure μ]

/-- The source logarithm on its full ordinary positive-moment domain.
Positive Gaussian variances are sufficient, but zero variances with nonzero
mean responses are also covered. -/
theorem actual_positive_factor_log_som
    (W : ι → Fin K × Fin K → Ω → ℝ) (m : ι → ℝ) (q : ι → NNReal)
    (hm : ∀ l t,Measurable (W l t))
    (hl : ∀ l t,μ.map (W l t) = gaussianReal (m l) (q l))
    (hwithin : ∀ l,iIndepFun (W l) μ)
    (hlayers : iIndepFun (fun l ω => fun t => W l t ω) μ)
    (u : ZMod M) (v : ZMod N)
    (hpos : ∀ l,0 < Complex.normSq ((m l : ℂ)*phaseSum (K:=K) u v)+
      (K*K : ℕ)*(q l : ℝ)) :
    Real.log (∫ ω,Complex.normSq (∏ l,randomKernelResponse (W l) u v ω) ∂μ) =
      ∑ l,Real.log (Complex.normSq ((m l : ℂ)*phaseSum (K:=K) u v)+
        (K*K : ℕ)*(q l : ℝ)) := by
  rw [actual_independent_layer_moments μ W m q hm hl hwithin hlayers u v]
  apply Real.log_prod
  intro l _
  exact ne_of_gt (hpos l)
end PositiveMomentFactors
end PaperDecoder


open Lean Elab Command Meta
set_option pp.universes true
set_option pp.fullNames true
set_option pp.piBinderTypes true
run_cmd liftTermElabM do
  for name in #[`Harsanyi.Frequency.Grid, `Harsanyi.Frequency.MatrixBackprop.Feature, `Harsanyi.Frequency.MatrixBackprop.actual_cascade_parameter_loss_hasFDerivAt, `Harsanyi.Frequency.MatrixBackprop.actual_kernel_spectral_gradient, `Harsanyi.Frequency.MatrixBackprop.actual_prefix_suffix_response_update, `Harsanyi.Frequency.MatrixBackprop.actual_real_network_spectrum, `Harsanyi.Frequency.MatrixBackprop.actual_suffix_cotangent, `Harsanyi.Frequency.MatrixBackprop.complex_linear_coefficients, `Harsanyi.Frequency.MatrixBackprop.conjugateTranspose, `Harsanyi.Frequency.MatrixBackprop.conjugate_transpose_comp, `Harsanyi.Frequency.MatrixBackprop.featureCLM, `Harsanyi.Frequency.MatrixBackprop.featureLinear, `Harsanyi.Frequency.MatrixBackprop.featurePullback, `Harsanyi.Frequency.MatrixBackprop.featureSpectrum, `Harsanyi.Frequency.MatrixBackprop.feature_clm_apply, `Harsanyi.Frequency.MatrixBackprop.feature_duality, `Harsanyi.Frequency.MatrixBackprop.feature_pullback_spectrum, `Harsanyi.Frequency.MatrixBackprop.networkCLM, `Harsanyi.Frequency.MatrixBackprop.networkPullback, `Harsanyi.Frequency.MatrixBackprop.network_pullback_spectrum, `Harsanyi.Frequency.MatrixBackprop.network_riesz_pullback, `Harsanyi.Frequency.MatrixBackprop.normalizedSpectrum, `Harsanyi.Frequency.MatrixBackprop.pullback_spectrum, `Harsanyi.Frequency.MatrixBackprop.realNetwork, `Harsanyi.Frequency.MatrixBackprop.real_network_embeds, `Harsanyi.Frequency.MatrixBackprop.real_network_hasFDerivAt, `Harsanyi.Frequency.MatrixBackprop.responseLinear, `Harsanyi.Frequency.MatrixBackprop.response_basis, `Harsanyi.Frequency.MatrixBackprop.riesz, `Harsanyi.Frequency.MatrixBackprop.riesz_pullback, `Harsanyi.Frequency.MatrixBackprop.shifted_real_pair, `Harsanyi.Frequency.MultiChannel.RandomMatrix, `Harsanyi.Frequency.MultiChannel.actual_cascade_source_closed, `Harsanyi.Frequency.MultiChannel.actual_cascade_uniform_moments, `Harsanyi.Frequency.MultiChannel.actual_gaussian_cascade_closed, `Harsanyi.Frequency.MultiChannel.actual_gaussian_row_moments, `Harsanyi.Frequency.MultiChannel.affineSequence, `Harsanyi.Frequency.MultiChannel.cascadeEntry, `Harsanyi.Frequency.MultiChannel.cascade_entry_measurable, `Harsanyi.Frequency.MultiChannel.cascade_entry_prefix_congr, `Harsanyi.Frequency.MultiChannel.cascade_entry_succ, `Harsanyi.Frequency.MultiChannel.complex_cross_moment, `Harsanyi.Frequency.MultiChannel.crossCoefficient, `Harsanyi.Frequency.MultiChannel.cross_coefficient_source, `Harsanyi.Frequency.MultiChannel.diagonalCoefficient, `Harsanyi.Frequency.MultiChannel.diagonal_product_source, `Harsanyi.Frequency.MultiChannel.finite_affine_expansion, `Harsanyi.Frequency.MultiChannel.independent_complex_mul_memLp, `Harsanyi.Frequency.MultiChannel.independent_layer_prefix, `Harsanyi.Frequency.MultiChannel.kernelMatrices, `Harsanyi.Frequency.MultiChannel.matrixLinear, `Harsanyi.Frequency.MultiChannel.meanSequence, `Harsanyi.Frequency.MultiChannel.mean_sequence_product, `Harsanyi.Frequency.MultiChannel.mean_sequence_source_closed, `Harsanyi.Frequency.MultiChannel.pastMatrices, `Harsanyi.Frequency.MultiChannel.past_matrices_measurable, `Harsanyi.Frequency.MultiChannel.row_column_mean, `Harsanyi.Frequency.MultiChannel.row_column_second_moment, `Harsanyi.Frequency.MultiChannel.somSequence, `Harsanyi.Frequency.MultiChannel.som_sequence_affine, `Harsanyi.Frequency.MultiChannel.som_sequence_source_closed, `Harsanyi.Frequency.MultiChannel.sourceMean, `Harsanyi.Frequency.MultiChannel.sourceSOM, `Harsanyi.Frequency.Parameters.actual_kernel_dc_ratio_counterexample, `Harsanyi.Frequency.Parameters.actual_kernel_size_growth_counterexample, `Harsanyi.Frequency.Parameters.actual_kernel_som, `Harsanyi.Frequency.Parameters.gaussianKernelSpace, `Harsanyi.Frequency.Parameters.gaussian_kernel_coordinate_law, `Harsanyi.Frequency.Parameters.gaussian_kernel_independent, `Harsanyi.Frequency.Parameters.kernelSOM, `Harsanyi.Frequency.Parameters.kernel_size_four_dc_ratio, `Harsanyi.Frequency.Parameters.kernel_size_one_som, `Harsanyi.Frequency.Parameters.kernel_size_two_dc_ratio, `Harsanyi.Frequency.Parameters.kernel_size_two_som, `Harsanyi.Frequency.Parameters.phase_sum_dc, `Harsanyi.Frequency.Parameters.phase_sum_four_40, `Harsanyi.Frequency.Parameters.phase_sum_one, `Harsanyi.Frequency.Parameters.phase_sum_two_40, `Harsanyi.Frequency.Parameters.std_character_eight_four, `Harsanyi.Frequency.Valid.actual_mixing_alpha_zero, `Harsanyi.Frequency.Valid.actual_valid_equation17_counterexample, `Harsanyi.Frequency.Valid.actual_valid_output_frequency_zero, `Harsanyi.Frequency.Valid.crop, `Harsanyi.Frequency.Valid.cropIndex, `Harsanyi.Frequency.Valid.crop_dft, `Harsanyi.Frequency.Valid.croppedOffsetLayer, `Harsanyi.Frequency.Valid.cropped_offset_layer_dft, `Harsanyi.Frequency.Valid.cropped_offset_layer_dft_bias, `Harsanyi.Frequency.Valid.deltaKernel, `Harsanyi.Frequency.Valid.exponential_sine_factor, `Harsanyi.Frequency.Valid.frequencyDifference, `Harsanyi.Frequency.Valid.geometric_real_sine_quotient, `Harsanyi.Frequency.Valid.geometric_sine_quotient, `Harsanyi.Frequency.Valid.inverse_dft2_character, `Harsanyi.Frequency.Valid.mixingAlpha, `Harsanyi.Frequency.Valid.original_constant_spectrum, `Harsanyi.Frequency.Valid.printedValidAlpha, `Harsanyi.Frequency.Valid.printed_valid_alpha_value, `Harsanyi.Frequency.Valid.realValidLayer, `Harsanyi.Frequency.Valid.real_valid_constant_delta, `Harsanyi.Frequency.Valid.real_valid_layer_embedding, `Harsanyi.Frequency.Valid.validLayer, `Harsanyi.Frequency.Valid.valid_index_bounds, `Harsanyi.Frequency.Valid.valid_indices_no_wrap, `Harsanyi.Frequency.Valid.valid_layer_dft, `Harsanyi.Frequency.Valid.valid_layer_eq_crop, `Harsanyi.Frequency.Valid.witness_frequency_difference, `Harsanyi.Frequency.Valid.witness_grid_frequency_difference, `Harsanyi.Frequency.WeakIndependence.W1, `Harsanyi.Frequency.WeakIndependence.W2, `Harsanyi.Frequency.WeakIndependence.actual_each_second_moment, `Harsanyi.Frequency.WeakIndependence.actual_first_product_factorization, `Harsanyi.Frequency.WeakIndependence.actual_first_product_zero, `Harsanyi.Frequency.WeakIndependence.actual_not_independent, `Harsanyi.Frequency.WeakIndependence.actual_product_second_moment, `Harsanyi.Frequency.WeakIndependence.actual_sign_gaussian_independence, `Harsanyi.Frequency.WeakIndependence.actual_sign_mean_zero, `Harsanyi.Frequency.WeakIndependence.actual_unit_kernel_each_som, `Harsanyi.Frequency.WeakIndependence.actual_unit_kernel_first_factorization, `Harsanyi.Frequency.WeakIndependence.actual_unit_kernel_product_som, `Harsanyi.Frequency.WeakIndependence.actual_unit_kernel_response, `Harsanyi.Frequency.WeakIndependence.actual_unit_kernel_weak_counterexample, `Harsanyi.Frequency.WeakIndependence.actual_w1_law, `Harsanyi.Frequency.WeakIndependence.actual_w1_mean_zero, `Harsanyi.Frequency.WeakIndependence.actual_w2_law, `Harsanyi.Frequency.WeakIndependence.actual_w2_mean_zero, `Harsanyi.Frequency.WeakIndependence.actual_weak_first_moment_counterexample, `Harsanyi.Frequency.WeakIndependence.fairSignLaw, `Harsanyi.Frequency.WeakIndependence.joint_map_split, `Harsanyi.Frequency.WeakIndependence.measurable_w1, `Harsanyi.Frequency.WeakIndependence.measurable_w2, `Harsanyi.Frequency.WeakIndependence.signGaussianSpace, `Harsanyi.Frequency.WeakIndependence.signValue, `Harsanyi.Frequency.WeakIndependence.standard_gaussian_fourth_moment, `Harsanyi.Frequency.actual_correlated_padding_counterexample, `Harsanyi.Frequency.actual_gaussian_depth_growth_counterexample, `Harsanyi.Frequency.actual_gradient00, `Harsanyi.Frequency.actual_gradient01, `Harsanyi.Frequency.actual_gradient10, `Harsanyi.Frequency.actual_gradient11, `Harsanyi.Frequency.actual_grid_cascade, `Harsanyi.Frequency.actual_independent_layer_log_moments, `Harsanyi.Frequency.actual_independent_layer_mean, `Harsanyi.Frequency.actual_independent_layer_moments, `Harsanyi.Frequency.actual_kernel_gaussian, `Harsanyi.Frequency.actual_kernel_mean, `Harsanyi.Frequency.actual_kernel_pseudocovariance, `Harsanyi.Frequency.actual_kernel_second_moment, `Harsanyi.Frequency.actual_real_kernel_pullback, `Harsanyi.Frequency.actual_real_layer_loss_hasFDerivAt, `Harsanyi.Frequency.actual_real_loss_identity_layer, `Harsanyi.Frequency.actual_real_loss_layer_exchange, `Harsanyi.Frequency.actual_real_spatial_pullback, `Harsanyi.Frequency.actual_response01, `Harsanyi.Frequency.actual_response10, `Harsanyi.Frequency.actual_response_gradient_update, `Harsanyi.Frequency.actual_spatial_one_step_not_target, `Harsanyi.Frequency.actual_two_layer_spectrum, `Harsanyi.Frequency.actual_unit_kernel_gaussian_depth_moment, `Harsanyi.Frequency.actual_zero_insert_frequency_blocks, `Harsanyi.Frequency.affine_circular_layer, `Harsanyi.Frequency.biasTerm, `Harsanyi.Frequency.cascadeBias, `Harsanyi.Frequency.cascadeLinear, `Harsanyi.Frequency.cascade_bias_sum, `Harsanyi.Frequency.character_frequency_difference, `Harsanyi.Frequency.circularCorrelation, `Harsanyi.Frequency.completedTargetImage, `Harsanyi.Frequency.completedTargetSpectrum, `Harsanyi.Frequency.completed_target_hermitian, `Harsanyi.Frequency.completed_target_image_real, `Harsanyi.Frequency.completed_target_selected_frequencies, `Harsanyi.Frequency.complex_ofReal_zero_iff, `Harsanyi.Frequency.crossFrequencyKernel, `Harsanyi.Frequency.cross_frequency_diagonal, `Harsanyi.Frequency.deltaGrid, `Harsanyi.Frequency.delta_grid_dft, `Harsanyi.Frequency.dft2, `Harsanyi.Frequency.dft2_constant, `Harsanyi.Frequency.dft2_inverse, `Harsanyi.Frequency.dft2_neg_input, `Harsanyi.Frequency.dft2_parseval_normSq, `Harsanyi.Frequency.dft2_parseval_pair, `Harsanyi.Frequency.dft2_sum, `Harsanyi.Frequency.dft2_twice, `Harsanyi.Frequency.dropped_product_counterexample, `Harsanyi.Frequency.edgePad23, `Harsanyi.Frequency.edge_pad_constant_dft, `Harsanyi.Frequency.edge_pad_original, `Harsanyi.Frequency.edge_pad_position_injective, `Harsanyi.Frequency.edge_pad_zero, `Harsanyi.Frequency.finite_real_functional, `Harsanyi.Frequency.frequencyBlock, `Harsanyi.Frequency.frequency_block_remainder, `Harsanyi.Frequency.gaussian_weighted_isGaussian, `Harsanyi.Frequency.gaussian_weighted_pseudocovariance, `Harsanyi.Frequency.gaussian_weighted_second_moment, `Harsanyi.Frequency.geometric, `Harsanyi.Frequency.geometric_norm_le, `Harsanyi.Frequency.geometric_one, `Harsanyi.Frequency.geometric_quotient, `Harsanyi.Frequency.geometric_root, `Harsanyi.Frequency.geometric_telescoping, `Harsanyi.Frequency.gridCharacter, `Harsanyi.Frequency.gridNetwork, `Harsanyi.Frequency.grid_character_comm, `Harsanyi.Frequency.grid_character_conjugate, `Harsanyi.Frequency.grid_character_int, `Harsanyi.Frequency.grid_character_neg_frequency, `Harsanyi.Frequency.grid_character_sum, `Harsanyi.Frequency.grid_character_trivial, `Harsanyi.Frequency.grid_orthogonality, `Harsanyi.Frequency.grid_phase_normSq, `Harsanyi.Frequency.grid_phase_square, `Harsanyi.Frequency.hermitian_inverse_real, `Harsanyi.Frequency.identity_kernel_response, `Harsanyi.Frequency.independent_complex_product_mean, `Harsanyi.Frequency.independent_complex_product_second_moment, `Harsanyi.Frequency.insertCoordinate, `Harsanyi.Frequency.insertGrid, `Harsanyi.Frequency.insert_coordinate_injective, `Harsanyi.Frequency.insert_grid_injective, `Harsanyi.Frequency.inserted_character, `Harsanyi.Frequency.inverseDft2, `Harsanyi.Frequency.inverse_dft2, `Harsanyi.Frequency.kernelLayer4, `Harsanyi.Frequency.kernelResponse, `Harsanyi.Frequency.kernel_layer_fourier, `Harsanyi.Frequency.multiChannelLayer, `Harsanyi.Frequency.multiChannelLayer_fourier, `Harsanyi.Frequency.offsetLayer, `Harsanyi.Frequency.offsetResponse, `Harsanyi.Frequency.offset_layer_dft, `Harsanyi.Frequency.padded_phase_normSq_one, `Harsanyi.Frequency.phaseSum, `Harsanyi.Frequency.product_update_exact, `Harsanyi.Frequency.quarterGaussianLaw, `Harsanyi.Frequency.quarterGaussianLayers, `Harsanyi.Frequency.quarter_gaussian_coordinate_law, `Harsanyi.Frequency.quarter_gaussian_independent, `Harsanyi.Frequency.randomKernelResponse, `Harsanyi.Frequency.random_response_weighted, `Harsanyi.Frequency.realKernel2, `Harsanyi.Frequency.realKernelCLM, `Harsanyi.Frequency.realKernelLinear, `Harsanyi.Frequency.realLoss, `Harsanyi.Frequency.realLoss_gradient00, `Harsanyi.Frequency.realLoss_gradient01, `Harsanyi.Frequency.realLoss_gradient10, `Harsanyi.Frequency.realLoss_gradient11, `Harsanyi.Frequency.real_gaussian_pseudocovariance, `Harsanyi.Frequency.real_kernel_basis, `Harsanyi.Frequency.real_weighted_square, `Harsanyi.Frequency.response01, `Harsanyi.Frequency.response10, `Harsanyi.Frequency.scatter, `Harsanyi.Frequency.scatter_elsewhere, `Harsanyi.Frequency.scatter_original, `Harsanyi.Frequency.shifted_inner_parseval, `Harsanyi.Frequency.source_constraint43, `Harsanyi.Frequency.source_constraint44, `Harsanyi.Frequency.source_constraint45, `Harsanyi.Frequency.source_constraint46, `Harsanyi.Frequency.spatialInnerPullback, `Harsanyi.Frequency.spectral_kernel_pullback, `Harsanyi.Frequency.spectrumLinear, `Harsanyi.Frequency.squareShift, `Harsanyi.Frequency.square_kernel_response, `Harsanyi.Frequency.std_character_conjugate, `Harsanyi.Frequency.third_root_geometric_zero, `Harsanyi.Frequency.transform, `Harsanyi.Frequency.transform_add, `Harsanyi.Frequency.transform_circularCorrelation, `Harsanyi.Frequency.transform_const, `Harsanyi.Frequency.transform_finite_sum, `Harsanyi.Frequency.transform_scatter, `Harsanyi.Frequency.transform_shift, `Harsanyi.Frequency.transform_smul, `Harsanyi.Frequency.twoFrequencyLoss, `Harsanyi.Frequency.twoLayer4, `Harsanyi.Frequency.two_layer_one_step_counterexample, `Harsanyi.Frequency.weightedResponse, `Harsanyi.Frequency.weighted_response_centered_square, `Harsanyi.Frequency.weighted_response_mean, `Harsanyi.Frequency.weighted_response_memLp, `Harsanyi.Frequency.weighted_response_second_moment, `Harsanyi.Frequency.zeroInsert, `Harsanyi.Frequency.zero_insert_dft_repeats, `Harsanyi.Frequency.zero_insert_elsewhere, `Harsanyi.Frequency.zero_insert_original, `PaperDecoder.actual_appendix_equations31_32, `PaperDecoder.actual_corollary_3_4, `PaperDecoder.actual_positive_factor_log_som, `PaperDecoder.finite_moment_ratio, `PaperDecoder.mean_preference_ratio_mono, `PaperDecoder.moment_factor_mono] do
    let info ← getConstInfo name
    let signature ← ppExpr info.type
    let axioms ← Lean.collectAxioms name
    let deps := info.type.getUsedConstants ++ (info.value?.map Expr.getUsedConstants).getD #[]
    let kind := match info with | .thmInfo _ => "theorem" | _ => "definition"
    liftM <| IO.println ("FOUNDATIONS_API:" ++ (Json.mkObj [
      ("name", toJson name.toString), ("signature", toJson signature.pretty),
      ("kind", toJson kind), ("axioms", toJson (axioms.map Name.toString)),
      ("dependencies", toJson (deps.map Name.toString))]).compress)
