import Lean.Util.CollectAxioms
import Harsanyi.Extensions.TransformationAffine
import Harsanyi.Extensions.TransformationRefinement
import Harsanyi.Extensions.TransformationCounterexamples
import Harsanyi.Extensions.TransformationRelaxation
import Harsanyi.Extensions.TransformationKernels
import Harsanyi.Extensions.TransformationOperators
import Harsanyi.Extensions.TransformationGaussianCounterexample

/-! Source Eq.(1): actual heterogeneous-width ReLU evaluation agrees with the
fixed-gate affine chain on precisely the inputs producing those gate patterns. -/
namespace PaperTransformation
open Harsanyi.GatedAffine
open MeasureTheory ProbabilityTheory
open scoped BigOperators
variable (dim : ℕ → ℕ)

/-! The main IB paragraph reuses Y for labels and network predictions. A
constant actual ReLU feature does not screen off a perfectly informative label.
The singleton conditioning law makes the conditional distribution explicit. -/
noncomputable def ibFeatureLaw : Harsanyi.Entropy.Law PUnit where
  mass := fun _ => 1
  nonneg := by intro z; norm_num
  total := by simp

noncomputable def ibJointLaw : Harsanyi.Entropy.Law (PUnit × (Bool × Bool)) :=
  Harsanyi.Entropy.kernelLaw ibFeatureLaw (fun _ => Harsanyi.Entropy.sameBit)

theorem ib_actual_constant_relu (x : Bool) : max (0 : ℝ) (0 * Harsanyi.Entropy.signedInput x + 1) = 1 := by
  norm_num

theorem ib_label_conditioning_law (z : PUnit) :
    (Harsanyi.Entropy.conditionalRow ibJointLaw z).mass = Harsanyi.Entropy.sameBit.mass := by
  funext xy
  have hz : (Harsanyi.Entropy.rowLaw ibJointLaw).mass z = 1 := by
    exact Harsanyi.Entropy.kernel_marginal ibFeatureLaw (fun _ => Harsanyi.Entropy.sameBit) z
  simp only [Harsanyi.Entropy.conditionalRow, hz, one_ne_zero, ite_false, div_one]
  simp [ibJointLaw, Harsanyi.Entropy.kernelLaw, ibFeatureLaw]

theorem ib_data_label_conditional_information :
    (∑ z : PUnit, (Harsanyi.Entropy.rowLaw ibJointLaw).mass z *
      Harsanyi.Entropy.mutualInformation (Harsanyi.Entropy.conditionalRow ibJointLaw z).mass) =
        Real.log 2 := by
  simp_rw [ib_label_conditioning_law]
  simp [ibJointLaw, Harsanyi.Entropy.kernel_marginal, Harsanyi.Entropy.rowLaw,
    ibFeatureLaw, Harsanyi.Entropy.same_bit_information]

theorem ib_data_label_not_screened_off :
    (∑ z : PUnit, (Harsanyi.Entropy.rowLaw ibJointLaw).mass z *
      Harsanyi.Entropy.mutualInformation (Harsanyi.Entropy.conditionalRow ibJointLaw z).mass) ≠ 0 := by
  rw [ib_data_label_conditional_information]
  exact ne_of_gt (Real.log_pos (by norm_num : (1 : ℝ) < 2))

noncomputable def reluGate {D : Type*} (h : D → ℝ) : D → ℝ :=
  fun d => if 0 < h d then 1 else 0

theorem relu_scalar_fixed_gate (x : ℝ) : max 0 x = (if 0<x then 1 else 0)*x := by
  split_ifs with h
  · rw [max_eq_right h.le]; simp
  · rw [max_eq_left (le_of_not_gt h)]; simp

def gateLinear {D : Type*} (s : D → ℝ) : (D → ℝ) →ₗ[ℝ] (D → ℝ) where
  toFun := fun h d => s d*h d
  map_add' := by intro x y; funext d; simp [mul_add]
  map_smul' := by intro c x; funext d; simp; ring

noncomputable def reluOutput (W : ∀ n, Space dim n →ₗ[ℝ] Space dim (n+1))
    (b : ∀ n, Space dim (n+1)) (x : Space dim 0) : ∀ n, Space dim n
  | 0 => x
  | n+1 => fun d => max 0 ((W n (reluOutput W b x n)+b n) d)

def frozenWeight (W : ∀ n, Space dim n →ₗ[ℝ] Space dim (n+1))
    (s : ∀ n, Space dim (n+1)) (n : ℕ) : Space dim n →ₗ[ℝ] Space dim (n+1) :=
  (gateLinear (s n)).comp (W n)

def frozenBias (b s : ∀ n, Space dim (n+1)) (n : ℕ) : Space dim (n+1) := gateLinear (s n) (b n)

theorem actual_relu_agrees_fixed_gate (W : ∀ n, Space dim n →ₗ[ℝ] Space dim (n+1))
    (b s : ∀ n, Space dim (n+1)) (x : Space dim 0) (L : ℕ)
    (hs : ∀ n, n<L → reluGate (W n (reluOutput dim W b x n)+b n)=s n) :
    reluOutput dim W b x L = networkOutput dim (frozenWeight dim W s) (frozenBias dim b s) x L := by
  induction L with
  | zero => rfl
  | succ L ih =>
    have hg := hs L (Nat.lt_succ_self L)
    have hi := ih (fun n hn => hs n (Nat.lt_succ_of_lt hn))
    funext d
    change max 0 ((W L (reluOutput dim W b x L)+b L) d) =
      s L d * (W L (networkOutput dim (frozenWeight dim W s) (frozenBias dim b s) x L)) d + s L d*(b L) d
    rw [relu_scalar_fixed_gate]
    have hd := congrFun hg d
    change (if 0 < (W L (reluOutput dim W b x L)+b L) d then 1 else 0) = s L d at hd
    rw [hd, hi]
    simp only [Pi.add_apply, mul_add]

theorem actual_relu_region_affine (W : ∀ n, Space dim n →ₗ[ℝ] Space dim (n+1))
    (b s : ∀ n, Space dim (n+1)) (x : Space dim 0) (L : ℕ)
    (hs : ∀ n, n<L → reluGate (W n (reluOutput dim W b x n)+b n)=s n) :
    reluOutput dim W b x L =
      (networkAffine dim (frozenWeight dim W s) (frozenBias dim b s) L).linear x +
      networkOutput dim (frozenWeight dim W s) (frozenBias dim b s) 0 L := by
  rw [actual_relu_agrees_fixed_gate dim W b s x L hs]
  exact network_output_linear_bias dim _ _ x L

/-- Include the final ungated linear output layer in the author's Eq.(1). -/
theorem actual_relu_module_affine (W : ∀ n, Space dim n →ₗ[ℝ] Space dim (n+1))
    (b s : ∀ n, Space dim (n+1)) (x : Space dim 0) (L : ℕ)
    (hs : ∀ n, n<L → reluGate (W n (reluOutput dim W b x n)+b n)=s n)
    {D : Type*} [AddCommGroup D] [Module ℝ D] (U : Space dim L →ₗ[ℝ] D) (c : D) :
    U (reluOutput dim W b x L)+c =
      (U.comp (networkAffine dim (frozenWeight dim W s) (frozenBias dim b s) L).linear) x +
      (U (networkOutput dim (frozenWeight dim W s) (frozenBias dim b s) 0 L)+c) := by
  rw [actual_relu_region_affine dim W b s x L hs]
  simp [map_add, add_assoc]

/-! Original Appendix A operators are evaluated before identifying them with
their fixed gates, rather than inserting the desired affine result as a premise. -/
theorem actual_dropout_module_affine {E D : Type*} [AddCommGroup E] [Module ℝ E]
    (W : E →ₗ[ℝ] (D → ℝ)) (b : D → ℝ) (keep : D → Bool) (x : E) :
    dropoutLinear keep (W x+b) =
      (layer ((dropoutLinear keep).comp W) (dropoutLinear keep b)) x :=
  fixed_dropout_layer_affine W b keep x

theorem actual_pool_module_affine {E D P : Type*} [AddCommGroup E] [Module ℝ E]
    (W : E →ₗ[ℝ] (D → ℝ)) (b : D → ℝ) (window : P → Finset D)
    (hne : ∀ p, (window p).Nonempty) (select : P → D) (x : E)
    (hsel : ∀ p, select p ∈ window p)
    (hmax : ∀ p d, d ∈ window p → (W x+b) d ≤ (W x+b) (select p)) :
    finiteMaxPool window hne (W x+b) =
      (layer ((selectedPoolLinear select).comp W) (selectedPoolLinear select b)) x :=
  fixed_pool_layer_affine W b window hne select x hsel hmax

theorem actual_gaussian_eq24_model (q : NNReal) (hq : 0 < q) :
    (Harsanyi.Entropy.gaussianFeatureSpace q).map
      (fun p => (Harsanyi.Entropy.noisyConstantRelu p,p.1)) =
      (ProbabilityTheory.gaussianReal 1 q) ⊗ₘ Harsanyi.Entropy.gaussianLabelKernel ∧
    Harsanyi.Entropy.actualConstantFeatureEstimator q <
      Harsanyi.Entropy.entropy Harsanyi.Entropy.bitLaw.mass -
        (∫ z : ℝ, Harsanyi.Entropy.entropy
          (fun y => (Harsanyi.Entropy.gaussianLabelKernel z {y}).toReal)
          ∂ProbabilityTheory.gaussianReal 1 q) := by
  rw [Harsanyi.Entropy.actual_gaussian_feature_information_zero]
  exact ⟨Harsanyi.Entropy.gaussian_feature_joint_kernel q,
    Harsanyi.Entropy.actual_constant_feature_estimator_negative q⟩
end PaperTransformation


open Lean Elab Command Meta
set_option pp.universes true
set_option pp.fullNames true
set_option pp.piBinderTypes true
run_cmd liftTermElabM do
  for name in #[`PaperTransformation.ibFeatureLaw, `PaperTransformation.ibJointLaw, `PaperTransformation.ib_actual_constant_relu, `PaperTransformation.ib_label_conditioning_law, `PaperTransformation.ib_data_label_conditional_information, `PaperTransformation.ib_data_label_not_screened_off, `PaperTransformation.reluGate, `PaperTransformation.relu_scalar_fixed_gate, `PaperTransformation.gateLinear, `PaperTransformation.reluOutput, `PaperTransformation.frozenWeight, `PaperTransformation.frozenBias, `PaperTransformation.actual_relu_agrees_fixed_gate, `PaperTransformation.actual_relu_region_affine, `PaperTransformation.actual_relu_module_affine, `PaperTransformation.actual_dropout_module_affine, `PaperTransformation.actual_pool_module_affine, `PaperTransformation.actual_gaussian_eq24_model, `Harsanyi.GatedAffine.layer, `Harsanyi.GatedAffine.layer_apply, `Harsanyi.GatedAffine.layer_comp, `Harsanyi.GatedAffine.Space, `Harsanyi.GatedAffine.networkAffine, `Harsanyi.GatedAffine.networkOutput, `Harsanyi.GatedAffine.network_output_affine, `Harsanyi.GatedAffine.network_output_linear_bias, `Harsanyi.Entropy.LayerState, `Harsanyi.Entropy.initialLayerLaw, `Harsanyi.Entropy.layerChainLaw, `Harsanyi.Entropy.layer_chain_entropy, `Harsanyi.Entropy.deterministicInputInformation, `Harsanyi.Entropy.deterministic_input_information_eq_entropy, `Harsanyi.Entropy.pushLaw, `Harsanyi.Entropy.push_expectation, `Harsanyi.Entropy.push_mass_ge, `Harsanyi.Entropy.coordinateLaw, `Harsanyi.Entropy.productCoordinateLaw, `Harsanyi.Entropy.totalCorrelation, `Harsanyi.Entropy.product_coordinate_support, `Harsanyi.Entropy.total_correlation_nonneg, `Harsanyi.Entropy.total_correlation_zero_iff_independent, `Harsanyi.Entropy.total_correlation_entropy_identity, `Harsanyi.Entropy.information_correlation_identity, `Harsanyi.Entropy.conditional_correlation_identity, `Harsanyi.Entropy.label_information_correlation_identity, `Harsanyi.Entropy.extendedReluGateLaw, `Harsanyi.Entropy.extended_relu_gate_information, `Harsanyi.Entropy.relu_prefix_clause_counterexample, `Harsanyi.Entropy.scalarGate, `Harsanyi.Entropy.scalar_gate_mean, `Harsanyi.Entropy.scalar_gate_variance, `Harsanyi.Entropy.binaryGateKDE, `Harsanyi.Entropy.binary_gate_kde_formula, `Harsanyi.Entropy.variance_bandwidth_kde_counterexample, `Harsanyi.Entropy.singleton_class_kernel_zero, `Harsanyi.Entropy.normalized_class_co_information_bound_counterexample, `Harsanyi.Entropy.dropoutReluLaw, `Harsanyi.Entropy.dropout_relu_gate, `Harsanyi.Entropy.removed_dropout_gate, `Harsanyi.Entropy.dropout_relu_information, `Harsanyi.Entropy.dropout_relu_variance, `Harsanyi.Entropy.dropout_relu_actual_law, `Harsanyi.Entropy.log_four_thirds_lower, `Harsanyi.Entropy.binary_kde_three_upper, `Harsanyi.Entropy.additional_randomness_kde_counterexample, `Harsanyi.Entropy.gateDistanceSq, `Harsanyi.Entropy.correlatedData, `Harsanyi.Entropy.independentData, `Harsanyi.Entropy.gateKernelSum, `Harsanyi.Entropy.fourPointTCEstimate, `Harsanyi.Entropy.gate_kernel_sums, `Harsanyi.Entropy.four_point_tc_formula, `Harsanyi.Entropy.exact_synthesis_tc_counterexample, `Harsanyi.Entropy.same_bit_vector_variance, `Harsanyi.Entropy.source_bandwidth_tc_counterexample, `Harsanyi.Entropy.printed_constant_feature_estimator_negative, `Harsanyi.Entropy.independent_continuous_feature_label_information_zero, `Harsanyi.Entropy.partition, `Harsanyi.Entropy.law_has_positive_mass, `Harsanyi.Entropy.partition_pos, `Harsanyi.Entropy.ebmLaw, `Harsanyi.Entropy.ebm_log_mass, `Harsanyi.Entropy.partition_hasFDerivAt, `Harsanyi.Entropy.log_partition_hasFDerivAt, `Harsanyi.Entropy.ebmNegativeLogLikelihood, `Harsanyi.Entropy.ebm_nll_eq_negative_log_probability, `Harsanyi.Entropy.empirical_marginal_prior_nll, `Harsanyi.Entropy.ebm_nll_hasFDerivAt, `Harsanyi.Entropy.cross_entropy_decomposition, `Harsanyi.Entropy.Law, `Harsanyi.Entropy.entropy, `Harsanyi.Entropy.marginal, `Harsanyi.Entropy.conditionalEntropy, `Harsanyi.Entropy.mutualInformation, `Harsanyi.Entropy.divergence, `Harsanyi.Entropy.law_mass_le_one, `Harsanyi.Entropy.entropy_nonneg, `Harsanyi.Entropy.marginal_nonneg, `Harsanyi.Entropy.mass_le_marginal, `Harsanyi.Entropy.mass_zero_of_marginal_zero, `Harsanyi.Entropy.entropy_chain, `Harsanyi.Entropy.conditional_entropy_nonneg, `Harsanyi.Entropy.entropy_marginal_le, `Harsanyi.Entropy.gibbs_term, `Harsanyi.Entropy.divergence_nonneg, `Harsanyi.Entropy.gibbs_term_strict, `Harsanyi.Entropy.divergence_zero_iff, `Harsanyi.Entropy.rowLaw, `Harsanyi.Entropy.columnLaw, `Harsanyi.Entropy.independentLaw, `Harsanyi.Entropy.mutual_information_eq_divergence, `Harsanyi.Entropy.mutual_information_nonneg, `Harsanyi.Entropy.entropy_subadditive, `Harsanyi.Entropy.co_information_identity, `Harsanyi.Entropy.exclusive_shared_identity, `Harsanyi.Entropy.binary_entropy_half, `Harsanyi.Entropy.conditional_entropy_graph, `Harsanyi.Entropy.mutual_information_graph, `Harsanyi.Entropy.bitLaw, `Harsanyi.Entropy.sameBit, `Harsanyi.Entropy.constantGate, `Harsanyi.Entropy.bit_entropy, `Harsanyi.Entropy.same_bit_information, `Harsanyi.Entropy.constant_gate_information, `Harsanyi.Entropy.prefix_direction_counterexample, `Harsanyi.Entropy.signedInput, `Harsanyi.Entropy.firstFeature, `Harsanyi.Entropy.first_relu_gate_constant, `Harsanyi.Entropy.second_relu_gate_label, `Harsanyi.Entropy.two_point_kde_counterexample, `Harsanyi.Entropy.kernelLaw, `Harsanyi.Entropy.kernel_marginal, `Harsanyi.Entropy.conditional_entropy_kernel, `Harsanyi.Entropy.entropy_kernel, `Harsanyi.Entropy.entropy_comp_equiv, `Harsanyi.Entropy.refinedKernelLaw, `Harsanyi.Entropy.refined_row_mass, `Harsanyi.Entropy.refined_column_mass, `Harsanyi.Entropy.refined_entropy, `Harsanyi.Entropy.refined_information_difference, `Harsanyi.Entropy.refined_information_monotone, `Harsanyi.Entropy.conditionalRow, `Harsanyi.Entropy.kernel_disintegration, `Harsanyi.Entropy.actual_conditional_entropy, `Harsanyi.Entropy.actual_joint_refinement_monotone, `Harsanyi.Entropy.gateLabelAt, `Harsanyi.Entropy.gate_label_column, `Harsanyi.Entropy.gate_label_conditional_information_zero, `Harsanyi.Entropy.gate_label_entropy_zero, `Harsanyi.Entropy.conditionalGateEntropy, `Harsanyi.Entropy.conditional_gate_entropy_zero, `Harsanyi.Entropy.conditionalGateLabelInformation, `Harsanyi.Entropy.conditional_gate_label_information_zero, `Harsanyi.Entropy.gate_label_mass_integrable, `Harsanyi.Entropy.gateLabelLaw, `Harsanyi.Entropy.deterministicGateCoInformation, `Harsanyi.Entropy.deterministic_gate_co_information_eq, `Harsanyi.Entropy.deterministic_gate_co_information_nonneg, `Harsanyi.Entropy.balancedLabelMeasure, `Harsanyi.Entropy.balanced_label_mass, `Harsanyi.Entropy.gaussianFeatureSpace, `Harsanyi.Entropy.constantReluFeature, `Harsanyi.Entropy.noisyConstantRelu, `Harsanyi.Entropy.constant_relu_feature, `Harsanyi.Entropy.noisy_constant_relu_eq, `Harsanyi.Entropy.gaussian_feature_noise_law, `Harsanyi.Entropy.gaussian_feature_label_law, `Harsanyi.Entropy.noisy_constant_relu_law, `Harsanyi.Entropy.gaussian_feature_independent, `Harsanyi.Entropy.gaussianLabelKernel, `Harsanyi.Entropy.gaussian_feature_joint_kernel, `Harsanyi.Entropy.gaussian_label_kernel_mass, `Harsanyi.Entropy.actual_gaussian_feature_information_zero, `Harsanyi.Entropy.constantFeatureKernel, `Harsanyi.Entropy.actual_constant_feature_kernel, `Harsanyi.Entropy.actualConstantFeatureEstimator, `Harsanyi.Entropy.actual_constant_feature_estimator_negative, `Harsanyi.Entropy.actual_gaussian_eq24_counterexample, `Harsanyi.Entropy.entropy_le_card, `Harsanyi.Entropy.kernel_mass_integrable, `Harsanyi.Entropy.mixtureLaw, `Harsanyi.Entropy.kernel_entropy_measurable, `Harsanyi.Entropy.kernel_entropy_integrable, `Harsanyi.Entropy.row_kernel_measurable, `Harsanyi.Entropy.column_kernel_measurable, `Harsanyi.Entropy.mutual_information_conditional_entropy, `Harsanyi.Entropy.conditional_kernel_entropy_integrable, `Harsanyi.Entropy.integral_conditional_information, `Harsanyi.Entropy.randomGateCoInformation, `Harsanyi.Entropy.random_gate_correlation_identity, `Harsanyi.Entropy.random_input_correlation_identity, `Harsanyi.GatedAffine.dropoutLinear, `Harsanyi.GatedAffine.selectedPoolLinear, `Harsanyi.GatedAffine.finiteMaxPool, `Harsanyi.GatedAffine.maximizingSelector, `Harsanyi.GatedAffine.maximizingSelector_spec, `Harsanyi.GatedAffine.finite_max_pool_selected, `Harsanyi.GatedAffine.fixed_maximizer_pool, `Harsanyi.GatedAffine.fixed_dropout_layer_affine, `Harsanyi.GatedAffine.fixed_pool_layer_affine, `Harsanyi.Entropy.coarseLabelLaw, `Harsanyi.Entropy.fineLabelLaw, `Harsanyi.Entropy.actual_projection_information_monotone, `Harsanyi.Entropy.gateRefinementLaw, `Harsanyi.Entropy.deterministic_gate_refinement_information, `Harsanyi.Entropy.gate_refinement_pointwise, `Harsanyi.Entropy.actual_gate_projection_mass, `Harsanyi.Entropy.deterministic_input_gate_refinement, `Harsanyi.Entropy.gate_label_law_pushforward, `Harsanyi.Entropy.deterministic_input_suffix, `Harsanyi.Entropy.relaxedPrior, `Harsanyi.Entropy.relaxed_prior_endpoints, `Harsanyi.Entropy.relaxed_prior_hasDerivAt, `Harsanyi.Entropy.relaxed_prior_positive, `Harsanyi.Entropy.sigmoid_gate_hasDerivAt, `Harsanyi.Entropy.swish_hasDerivAt, `Harsanyi.Entropy.relaxed_prior_sigmoid_positive, `Harsanyi.Entropy.relaxed_prior_outside_domain, `Harsanyi.Entropy.frozenStateLoss, `Harsanyi.Entropy.frozen_state_loss_hasFDerivAt, `Harsanyi.Entropy.frozen_monte_carlo_derivative, `Harsanyi.Entropy.frozen_batch_state_loss_hasFDerivAt] do
    let info ← getConstInfo name
    let signature ← ppExpr info.type
    let axioms ← Lean.collectAxioms name
    let deps := info.type.getUsedConstants ++ (info.value?.map Expr.getUsedConstants).getD #[]
    let kind := match info with | .thmInfo _ => "theorem" | _ => "definition"
    liftM <| IO.println ("TRANSFORMATION_API:" ++ (Json.mkObj [
      ("name", toJson name.toString), ("signature", toJson signature.pretty),
      ("kind", toJson kind), ("axioms", toJson (axioms.map Name.toString)),
      ("dependencies", toJson (deps.map Name.toString))]).compress)
