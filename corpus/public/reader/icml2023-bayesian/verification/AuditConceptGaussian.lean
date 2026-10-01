import Lean.Util.CollectAxioms
import Harsanyi.Extensions.ConceptGaussian
import Harsanyi.Extensions.PolynomialSupport
import Harsanyi.Extensions.ConceptMasks
import Harsanyi.Extensions.Attribution

set_option maxHeartbeats 1600000
namespace PaperBayesian
open Finset MeasureTheory ProbabilityTheory Matrix
open Harsanyi
variable {ι Ω : Type*} [Fintype ι] [DecidableEq ι] [MeasurableSpace Ω]

/-- Lowest-degree polynomial with an arbitrary output baseline and actual coordinate masks. -/
noncomputable def maskedLowest (a b τ : ℝ) (s : ι → ℝ) (ε : ι → Ω → ℝ)
    (ω : Ω) : Game ι := fun T =>
  b + a * TaylorMoments.monomial univ (fun _ => 1)
    (fun i => if i ∈ T then s i * τ + ε i ω else 0)

theorem lowest_dividend [Nonempty ι] (a b τ : ℝ) (s : ι → ℝ)
    (ε : ι → Ω → ℝ) (ω : Ω) :
    interaction (maskedLowest a b τ s ε ω) univ = a * ∏ i, (s i * τ + ε i ω) := by
  have hg : maskedLowest a b τ s ε ω =
      (fun T => b + unanimity univ (a * ∏ i, (s i * τ + ε i ω)) T) := by
    funext T
    unfold maskedLowest
    rw [TaylorMoments.monomial_mask univ T (fun _ => 1) _ (by simp)]
    simp only [TaylorMoments.monomial, pow_one, unanimity]
    split_ifs <;> simp
  rw [hg, interaction_add, interaction_const, interaction_unanimity]
  simp [Finset.univ_nonempty.ne_empty]

/-- Theorem 2.2 interpreted with its reference coefficient: full Gaussian tails are included. -/
theorem lowest_actual_moments [Nonempty ι] (μ : Measure Ω) [IsProbabilityMeasure μ]
    (a b τ : ℝ) (s : ι → ℝ) (ε : ι → Ω → ℝ) (σ2 : NNReal)
    (hτ : τ ≠ 0) (hs : ∀ i, s i ^ 2 = 1)
    (hm : ∀ i, Measurable (ε i)) (hl : ∀ i, μ.map (ε i) = gaussianReal 0 σ2)
    (hi : iIndepFun ε μ) :
    let U := a * ∏ i, s i * τ
    (∫ ω, interaction (maskedLowest a b τ s ε ω) univ ∂μ) = U ∧
      variance (fun ω => interaction (maskedLowest a b τ s ε ω) univ) μ =
        U ^ 2 * ((1 + (σ2 : ℝ) / τ ^ 2) ^ Fintype.card ι - 1) := by
  have hf : (fun ω => interaction (maskedLowest a b τ s ε ω) univ) =
      (fun ω => (a * ∏ i, s i * τ) * ∏ i, (1 + s i * ε i ω / τ)) := by
    funext ω
    rw [lowest_dividend]
    exact (ConceptGaussian.lowest_polynomial_identity a τ s (fun i => ε i ω) hs hτ).symm
  simp_rw [congrFun hf]
  exact ConceptGaussian.lowest_interaction_moments μ ε σ2 s τ _ hs hm hl hi

/-- The uniform independent-feature expected loss, rather than assumed normal equations. -/
theorem independent_features_optimum (μ : Measure Ω) [IsProbabilityMeasure μ]
    (X : ι → Ω → ℝ) (a d : ι → ℝ) (y : ℝ)
    (hp : ∀ i, MemLp (X i) 2 μ) (ha : ∀ i, ∫ ω, X i ω ∂μ = a i)
    (hv : ∀ i, variance (X i) μ = d i)
    (hi : Pairwise fun i j => IndepFun (X i) (X j) μ) (hd : ∀ i, 0 < d i) :
    ∀ w, w ≠ ConceptGaussian.featureOpt a d y →
      (∫ ω, (y - ∑ i, ConceptGaussian.featureOpt a d y i * X i ω) ^ 2 ∂μ) <
        (∫ ω, (y - ∑ i, w i * X i ω) ^ 2 ∂μ) :=
  ConceptGaussian.pairwise_feature_expected_unique_min μ X a d hp ha hv hi hd y

/-- The exact scaling relation in Theorem 2.6, on its ordinary nonzero denominator domain. -/
theorem scaling_ratio (μ : Measure Ω) [IsProbabilityMeasure μ]
    (C : Ω → ℝ) (U : ℝ) (hU : U ≠ 0) (hV : variance C μ ≠ 0) :
    |∫ ω, C ω ∂μ| / variance C μ =
      |U| * (|∫ ω, U * C ω ∂μ| / variance (fun ω => U * C ω) μ) := by
  rw [integral_const_mul, variance_mul]
  exact TaylorMoments.scaling_ratio U (∫ ω, C ω ∂μ) (variance C μ) hU hV


variable (μ : Measure Ω) [IsProbabilityMeasure μ]

lemma abs_normalized_coordinate (s τ e : ℝ) (hs : s ^ 2 = 1) (hτ : 0 < τ) :
    |s * τ + e| / τ = |1 + s * e / τ| := by
  have ha : |s| = 1 := by nlinarith [sq_abs s, abs_nonneg s]
  have heq : s * (s * τ + e) / τ = 1 + s * e / τ := by
    field_simp
    nlinarith [hs]
  rw [← heq, abs_div, abs_mul, ha, one_mul, abs_of_pos hτ]

lemma scaled_unit_law (ε : Ω → ℝ) (σ2 : NNReal) (s τ : ℝ)
    (hs : s ^ 2 = 1) (hm : Measurable ε) (hl : μ.map ε = gaussianReal 0 σ2) :
    μ.map (fun ω => 1 + s * ε ω / τ) = gaussianReal 1 (ConceptGaussian.scaledVariance σ2 τ) := by
  have h := ConceptGaussian.signed_scaled_law μ ε σ2 s τ hs hm hl
  have hf : (fun ω => 1 + s * ε ω / τ) = (fun z : ℝ => 1 + z) ∘ (fun ω => s * ε ω / τ) := rfl
  rw [hf, ← Measure.map_map (show Measurable (fun z : ℝ => 1 + z) from by fun_prop) (show Measurable (fun ω => s * ε ω / τ) from by fun_prop), h,
    gaussianReal_map_const_add, zero_add]

noncomputable def absoluteTrigger (τ : ℝ) (s : ι → ℝ) (ε : ι → Ω → ℝ)
    (k : ι → ℕ) (T : Finset ι) : Ω → ℝ := fun ω => ∏ i ∈ T, (|s i * τ + ε i ω| / τ) ^ k i

theorem absolute_trigger_growth (ε : ι → Ω → ℝ) (σ2 : NNReal) (s : ι → ℝ) (τ : ℝ) (k : ι → ℕ)
    (hs : ∀ i, s i ^ 2 = 1) (hτ : 0 < τ) (hσ : 0 < (σ2 : ℝ))
    (hm : ∀ i, Measurable (ε i)) (hl : ∀ i, μ.map (ε i) = gaussianReal 0 σ2)
    (hi : iIndepFun ε μ) (hk : ∀ i, k i ≠ 0)
    (A B : Finset ι) (hA : A.Nonempty) (hB : B.Nonempty) (hab : Disjoint A B) :
    let JA := absoluteTrigger τ s ε k A
    let JAB := absoluteTrigger τ s ε k (A ∪ B)
    let p := ∏ i ∈ B, ∫ ω, (1 + s i * ε i ω / τ) ^ k i ∂μ
    variance JAB μ / variance JA μ > p ^ 2 ∧ 1 ≤ p ^ 2 ∧
      ((|∫ ω, JAB ω ∂μ| / variance JAB μ) / (|∫ ω, JA ω ∂μ| / variance JA μ)) < 1 / p ∧
      1 / p ≤ 1 := by
  let X : ι → Ω → ℝ := fun i ω => 1 + s i * ε i ω / τ
  have hXm : ∀ i, Measurable (X i) := by intro i; dsimp [X]; fun_prop
  have hXl : ∀ i, μ.map (X i) = gaussianReal 1 (ConceptGaussian.scaledVariance σ2 τ) :=
    fun i => scaled_unit_law μ (ε i) σ2 (s i) τ (hs i) (hm i) (hl i)
  have hXi : iIndepFun X μ := by
    simpa only [X, Function.comp_def] using hi.comp (fun i z => 1 + s i * z / τ)
      (fun i => measurable_const.add ((measurable_const.mul measurable_id).div_const τ))
  have hq : ConceptGaussian.scaledVariance σ2 τ ≠ 0 := by
    intro hz
    have hco : (σ2 : ℝ) / τ ^ 2 = 0 := congrArg (fun z : NNReal => (z : ℝ)) hz
    have hpos : 0 < (σ2 : ℝ) / τ ^ 2 := div_pos hσ (sq_pos_of_pos hτ)
    linarith
  have hf (T : Finset ι) : absoluteTrigger τ s ε k T = (fun ω => ∏ i ∈ T, |X i ω| ^ k i) := by
    funext ω
    apply prod_congr rfl
    intro i _
    rw [abs_normalized_coordinate (s i) τ (ε i ω) (hs i) hτ]
  simp_rw [hf]
  exact ConceptGaussian.folded_subset_growth μ X (fun _ => ConceptGaussian.scaledVariance σ2 τ) k
    hXm hXl hXi (fun _ => hq) hk A B hA hB hab

/-- Source Theorem 2.3's J at x=1,r=0,tau=1 and degree one. -/
noncomputable def oneCoordinateTrigger (z : ℝ) : ℝ := |(1 + z) - 0| / 1

theorem general_moment_counterexample (q : NNReal) (hq : q ≠ 0) :
    (∫ z : ℝ, oneCoordinateTrigger z ∂gaussianReal 0 q) ≠
      ∫ z : ℝ, (1 + z) ∂gaussianReal 0 q := by
  have hl : (gaussianReal 0 q).map (fun z : ℝ => 1 + z) = gaussianReal 1 q := by
    rw [gaussianReal_map_const_add, zero_add]
  have hf : (∫ z : ℝ, oneCoordinateTrigger z ∂gaussianReal 0 q) =
      ∫ z : ℝ, |z| ∂gaussianReal 1 q := by
    rw [← hl]
    simpa only [oneCoordinateTrigger, sub_zero, div_one, id_eq] using
      (integral_map_of_stronglyMeasurable (show Measurable (fun z : ℝ => 1 + z) from by fun_prop)
        measurable_id.abs.stronglyMeasurable).symm
  have hs : (∫ z : ℝ, (1 + z) ∂gaussianReal 0 q) = 1 := by
    have hid : Integrable (fun z : ℝ => z) (gaussianReal 0 q) :=
      (memLp_id_gaussianReal (μ := 0) (v := q) 2).integrable (by norm_num)
    rw [integral_add (integrable_const _) hid]
    simp [integral_id_gaussianReal]
  rw [hf, hs]
  exact ne_of_gt (ConceptGaussian.folded_first_moment_gt_one q hq)


/-- Both original scale bounds, with every denominator in its defined domain. -/
theorem scaling_bounds (μ : Measure Ω) [IsProbabilityMeasure μ]
    (C : Ω → ℝ) (U amin amax : ℝ) (hU : U ≠ 0) (hV : 0 < variance C μ)
    (hmin : amin ≤ |U|) (hmax : |U| ≤ amax) :
    amin * (|∫ ω, U * C ω ∂μ| / variance (fun ω => U * C ω) μ) ≤
      |∫ ω, C ω ∂μ| / variance C μ ∧
    |∫ ω, C ω ∂μ| / variance C μ ≤
      amax * (|∫ ω, U * C ω ∂μ| / variance (fun ω => U * C ω) μ) := by
  have hp : 0 ≤ |∫ ω, U * C ω ∂μ| / variance (fun ω => U * C ω) μ :=
    div_nonneg (abs_nonneg _) (variance_nonneg _ _)
  rw [scaling_ratio μ C U hU (ne_of_gt hV)]
  exact ⟨mul_le_mul_of_nonneg_right hmin hp, mul_le_mul_of_nonneg_right hmax hp⟩


/-- The printed salient sum includes an inactive singleton at the empty mask. -/
noncomputable def oneVariableMaskedScore (c : ℝ) : Game (Fin 1) :=
  fun T => c * (if (0 : Fin 1) ∈ T then 1 else 0)

theorem salient_empty_mask (c : ℝ) :
    oneVariableMaskedScore c ∅ = 0 ∧
      (∑ S ∈ ({({0} : Finset (Fin 1))} : Finset (Finset (Fin 1))),
        interaction (oneVariableMaskedScore c) S) = c := by
  have hg : oneVariableMaskedScore c = unanimity ({0} : Finset (Fin 1)) c := by
    funext T
    simp [oneVariableMaskedScore, unanimity]
  rw [hg]
  simp [unanimity, interaction_unanimity]

end PaperBayesian

open Lean Elab Command Meta
set_option pp.universes true
set_option pp.fullNames true
set_option pp.piBinderTypes true
run_cmd liftTermElabM do
  for name in #[`Harsanyi.TaylorMoments.monomial, `Harsanyi.TaylorMoments.monomial_mask, `Harsanyi.TaylorMoments.polynomial_mask, `Harsanyi.TaylorMoments.normalized_trigger, `Harsanyi.TaylorMoments.zero_trigger_counterexample, `Harsanyi.TaylorMoments.product_mean, `Harsanyi.TaylorMoments.product_variance, `Harsanyi.TaylorMoments.product_memLp, `Harsanyi.TaylorMoments.gaussian_affine_product, `Harsanyi.TaylorMoments.unit_mean_product_variance, `Harsanyi.TaylorMoments.scaling_ratio, `Harsanyi.TaylorMoments.moving_sign_counterexample, `Harsanyi.NoisyRegression.zeta, `Harsanyi.NoisyRegression.zeta_mulVec, `Harsanyi.NoisyRegression.zeta_injective, `Harsanyi.NoisyRegression.gram_posDef, `Harsanyi.NoisyRegression.normalMatrix, `Harsanyi.NoisyRegression.normal_posDef, `Harsanyi.NoisyRegression.normal_isUnit, `Harsanyi.NoisyRegression.normal_solution, `Harsanyi.NoisyRegression.zero_noise, `Harsanyi.NoisyRegression.quadraticLoss, `Harsanyi.NoisyRegression.symmetric_dot, `Harsanyi.NoisyRegression.quadratic_difference, `Harsanyi.NoisyRegression.quadratic_unique_min, `Harsanyi.NoisyRegression.normal_unique_min, `Harsanyi.NoisyRegression.residualLoss, `Harsanyi.NoisyRegression.residualLoss_expansion, `Harsanyi.NoisyRegression.residual_unique_min, `Harsanyi.NoisyRegression.featureLoss, `Harsanyi.NoisyRegression.feature_normal_scaling, `Harsanyi.NoisyRegression.transferMatrix, `Harsanyi.NoisyRegression.zeta_permutation, `Harsanyi.NoisyRegression.transfer_permutation, `Harsanyi.NoisyRegression.row_norm_permutation, `Harsanyi.NoisyRegression.exists_coalition_permutation, `Harsanyi.NoisyRegression.equal_order_row_norm, `Harsanyi.NoisyRegression.transfer_zero, `Harsanyi.NoisyRegression.diagonal_product_counterexample, `Harsanyi.GaussianRegression.gaussian_memLp, `Harsanyi.GaussianRegression.gaussian_mean, `Harsanyi.GaussianRegression.independent_residual, `Harsanyi.GaussianRegression.gaussian_residual, `Harsanyi.PolynomialSupport.polynomial, `Harsanyi.PolynomialSupport.supportCoefficient, `Harsanyi.PolynomialSupport.mask_terms, `Harsanyi.PolynomialSupport.support_reconstruct, `Harsanyi.PolynomialSupport.interaction_eq_supportCoefficient, `Harsanyi.ConceptGaussian.scaledVariance, `Harsanyi.ConceptGaussian.signed_scaled_law, `Harsanyi.ConceptGaussian.lowest_interaction_moments, `Harsanyi.ConceptGaussian.lowest_polynomial_identity, `Harsanyi.ConceptGaussian.feature_expected_loss, `Harsanyi.ConceptGaussian.featureMatrix, `Harsanyi.ConceptGaussian.pairwise_feature_expected_loss, `Harsanyi.ConceptGaussian.featureOpt, `Harsanyi.ConceptGaussian.featureMatrix_posDef, `Harsanyi.ConceptGaussian.featureLoss_quadratic, `Harsanyi.ConceptGaussian.featureOpt_normal, `Harsanyi.ConceptGaussian.featureOpt_unique_min, `Harsanyi.ConceptGaussian.feature_expected_unique_min, `Harsanyi.ConceptGaussian.pairwise_feature_expected_unique_min, `Harsanyi.ConceptGaussian.gaussian_memLp_any, `Harsanyi.ConceptGaussian.gaussian_feature_moments, `Harsanyi.ConceptGaussian.gaussian_feature_unique_min, `Harsanyi.ConceptGaussian.folded_power_memLp, `Harsanyi.ConceptGaussian.folded_product_moments, `Harsanyi.ConceptGaussian.folded_gaussian_variance_pos, `Harsanyi.ConceptGaussian.reflection_power_bound, `Harsanyi.ConceptGaussian.signed_power_memLp, `Harsanyi.ConceptGaussian.signed_gaussian_moment_ge_one, `Harsanyi.ConceptGaussian.unit_gaussian_power_bounds, `Harsanyi.ConceptGaussian.folded_map_variance_pos, `Harsanyi.ConceptGaussian.folded_subset_moments, `Harsanyi.ConceptGaussian.folded_subset_positive, `Harsanyi.ConceptGaussian.folded_disjoint_moments, `Harsanyi.ConceptGaussian.product_growth_bounds, `Harsanyi.ConceptGaussian.folded_subset_growth, `Harsanyi.ConceptGaussian.folded_first_moment_gt_one, `Harsanyi.ConceptMasks.maskedGame, `Harsanyi.ConceptMasks.masked_dividend, `Harsanyi.ConceptMasks.normalizedMaskedTrigger, `Harsanyi.ConceptMasks.binary_trigger, `Harsanyi.ConceptMasks.linear_representation, `PaperBayesian.maskedLowest, `PaperBayesian.lowest_dividend, `PaperBayesian.lowest_actual_moments, `PaperBayesian.independent_features_optimum, `PaperBayesian.scaling_ratio, `PaperBayesian.abs_normalized_coordinate, `PaperBayesian.scaled_unit_law, `PaperBayesian.absoluteTrigger, `PaperBayesian.absolute_trigger_growth, `PaperBayesian.oneCoordinateTrigger, `PaperBayesian.general_moment_counterexample, `PaperBayesian.scaling_bounds, `PaperBayesian.oneVariableMaskedScore, `PaperBayesian.salient_empty_mask, `Harsanyi.higherMarginal_eq_sum_interaction, `Harsanyi.reconstruction, `Harsanyi.reconstruction_unique, `Harsanyi.interaction_add, `Harsanyi.interaction_unanimity] do
    let info ← getConstInfo name
    let signature ← ppExpr info.type
    let axioms ← Lean.collectAxioms name
    let deps := info.type.getUsedConstants ++ (info.value?.map Expr.getUsedConstants).getD #[]
    let kind := match info with | .thmInfo _ => "theorem" | .inductInfo _ => "inductive" | _ => "definition"
    liftM <| IO.println ("DYNAMICS_API:" ++ (Json.mkObj [
      ("name", toJson name.toString), ("signature", toJson signature.pretty),
      ("kind", toJson kind), ("axioms", toJson (axioms.map Name.toString)),
      ("dependencies", toJson (deps.map Name.toString))]).compress)
