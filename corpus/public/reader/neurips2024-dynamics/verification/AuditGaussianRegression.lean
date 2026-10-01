import Lean.Util.CollectAxioms
import Harsanyi.Extensions.GaussianRegression
import Harsanyi.Extensions.PolynomialSupport
import Harsanyi.Extensions.Noise
import Harsanyi.Extensions.LayerwiseKnowledge

set_option maxHeartbeats 1000000
namespace PaperDynamics
open Finset Matrix MeasureTheory ProbabilityTheory
open Harsanyi Harsanyi.NoisyRegression Harsanyi.GaussianRegression
variable {α Ω : Type*} [Fintype α] [DecidableEq α] [MeasurableSpace Ω]

/-- Appendix A efficiency, with the raw empty term. -/
theorem efficiency (g : Game α) (N : Finset α) :
    (∑ S ∈ N.powerset, interaction g S) = g N := reconstruction g N

theorem dummy (g : Game α) (S : Finset α) (i : α) (hi : i ∉ S)
    (hS : S.Nonempty) (h : ∀ U ⊆ S, g (insert i U) = g U + g {i}) :
    interaction g (insert i S) = 0 := by
  rw [interaction_insert g S i hi]
  have hc : interaction (marginal g i) S = interaction (fun _ => g {i}) S := by
    apply interaction_congr
    intro U hU
    simp [marginal, h U hU]
  rw [hc, interaction_const, if_neg hS.ne_empty]

theorem symmetry (g : Game α) (S : Finset α) (i j : α) (hi : i ∉ S) (hj : j ∉ S)
    (h : ∀ U ⊆ S, g (insert i U) = g (insert j U)) :
    interaction g (insert i S) = interaction g (insert j S) := by
  rw [interaction_insert g S i hi, interaction_insert g S j hj]
  apply interaction_congr
  intro U hU
  simp only [marginal, h U hU]

noncomputable def noisyLoss (μ : Measure Ω) (ε : Finset α → Ω → ℝ)
    (y w : Finset α → ℝ) : ℝ :=
  ∑ S : Finset α, ∫ ω, (y S - (zeta *ᵥ w) S + ∑ T, (-w T) * ε T ω) ^ 2 ∂μ

/-- Exact loss expansion; no large-sample limit and no Gaussian assumption added. -/
theorem noisyLoss_expansion (μ : Measure Ω) [IsProbabilityMeasure μ]
    (ε : Finset α → Ω → ℝ) (q : Finset α → ℝ)
    (hp : ∀ T, MemLp (ε T) 2 μ)
    (he : ∀ T, ∫ ω, ε T ω ∂μ = 0)
    (hv : ∀ T, variance (ε T) μ = q T)
    (hi : iIndepFun ε μ) (y w : Finset α → ℝ) :
    noisyLoss μ ε y w = residualLoss (fun T => Fintype.card (Finset α) * q T) y w := by
  unfold noisyLoss residualLoss
  simp_rw [independent_residual μ ε q hp he hv hi]
  rw [sum_add_distrib]
  have hs : (∑ S : Finset α, (y S - (zeta *ᵥ w) S) ^ 2) =
      (y - zeta *ᵥ w) ⬝ᵥ (y - zeta *ᵥ w) := by
    simp only [dotProduct, Pi.sub_apply, pow_two]
  rw [hs]
  congr 1
  simp only [neg_sq, sum_const, card_univ, nsmul_eq_mul, mul_sum]
  apply sum_congr rfl
  intro T _
  ring

/-- Theorem 3's actual expected-noise argmin, for its exact finite-moment model. -/
theorem noisyLoss_unique_min (μ : Measure Ω) [IsProbabilityMeasure μ]
    (ε : Finset α → Ω → ℝ) (q : Finset α → ℝ)
    (hp : ∀ T, MemLp (ε T) 2 μ)
    (he : ∀ T, ∫ ω, ε T ω ∂μ = 0)
    (hv : ∀ T, variance (ε T) μ = q T)
    (hq : ∀ T, 0 ≤ q T) (hi : iIndepFun ε μ) (y : Finset α → ℝ) :
    let c := fun T => (Fintype.card (Finset α) : ℝ) * q T
    let u := (normalMatrix c)⁻¹ *ᵥ (zetaᵀ *ᵥ y)
    ∀ w, w ≠ u → noisyLoss μ ε y u < noisyLoss μ ε y w := by
  dsimp only
  intro w hw
  simp_rw [noisyLoss_expansion μ ε q hp he hv hi]
  apply residual_unique_min _ _ y w hw
  intro T
  exact mul_nonneg (Nat.cast_nonneg _) (hq T)

/-- The original uniform-mask mean loss, rather than its unnormalized sum. -/
noncomputable def meanNoisyLoss (μ : Measure Ω) (ε : Finset α → Ω → ℝ)
    (y w : Finset α → ℝ) : ℝ :=
  (Fintype.card (Finset α) : ℝ)⁻¹ * noisyLoss μ ε y w

/-- Positive normalization preserves the actual unique global minimizer. -/
theorem meanNoisyLoss_unique_min (μ : Measure Ω) [IsProbabilityMeasure μ]
    (ε : Finset α → Ω → ℝ) (q : Finset α → ℝ)
    (hp : ∀ T, MemLp (ε T) 2 μ)
    (he : ∀ T, ∫ ω, ε T ω ∂μ = 0)
    (hv : ∀ T, variance (ε T) μ = q T)
    (hq : ∀ T, 0 ≤ q T) (hi : iIndepFun ε μ) (y : Finset α → ℝ) :
    let c := fun T => (Fintype.card (Finset α) : ℝ) * q T
    let u := (normalMatrix c)⁻¹ *ᵥ (zetaᵀ *ᵥ y)
    ∀ w, w ≠ u → meanNoisyLoss μ ε y u < meanNoisyLoss μ ε y w := by
  dsimp only
  intro w hw
  unfold meanNoisyLoss
  apply mul_lt_mul_of_pos_left (noisyLoss_unique_min μ ε q hp he hv hq hi y w hw)
  apply inv_pos.mpr
  exact_mod_cast Fintype.card_pos (α := Finset α)

/-- Theorem 5 includes the source empty baseline. -/
theorem zero_noise_recovery (w : Finset α → ℝ) :
    (normalMatrix (fun _ => 0))⁻¹ *ᵥ (zetaᵀ *ᵥ (zeta *ᵥ w)) = w := zero_noise w

/-- A complete correlated-marginal counterexample to Lemma 1's variance clause. -/
theorem correlated_noise_counterexample (μ : Measure Ω) [IsProbabilityMeasure μ]
    (Z : Ω → ℝ) (σ2 : NNReal) (hσ : σ2 ≠ 0) (hm : Measurable Z) (hlaw : μ.map Z = gaussianReal 0 σ2) :
    variance (fun ω => interaction (fun _ : Finset (Fin 1) => Z ω) {0}) μ ≠ 2 * σ2 := by
  have hz : (fun ω => interaction (fun _ : Finset (Fin 1) => Z ω) {0}) = (fun _ => 0) := by
    funext ω
    rw [interaction_const]
    simp
  rw [hz]
  rw [show variance (fun _ : Ω => (0 : ℝ)) μ = 0 from variance_zero μ]
  change (0 : ℝ) ≠ 2 * σ2
  have h : (σ2 : ℝ) ≠ 0 := by exact_mod_cast hσ
  exact ne_of_lt (by positivity)

/-- Theorem 4 for the exact finite subset design, including zero noise. -/
theorem equal_order_norm (σ2 : ℝ) (T U : Finset α) (hcard : T.card = U.card) :
    Real.sqrt (∑ V, transferMatrix (fun A => (Fintype.card (Finset α) : ℝ) * 2 ^ A.card * σ2) T V ^ 2) =
    Real.sqrt (∑ V, transferMatrix (fun A => (Fintype.card (Finset α) : ℝ) * 2 ^ A.card * σ2) U V ^ 2) := by
  apply congrArg Real.sqrt
  simpa only [mul_assoc, mul_left_comm] using
    equal_order_row_norm ((Fintype.card (Finset α) : ℝ) * σ2) T U hcard

/-- Full matrix boundary refuting Proposition 1's unconditional strictness. -/
theorem zero_noise_row_ratio (T U : Finset α) :
    Real.sqrt (∑ V, transferMatrix (fun _ => (0 : ℝ)) T V ^ 2) /
      Real.sqrt (∑ V, transferMatrix (fun _ => (0 : ℝ)) U V ^ 2) = 1 := by
  rw [transfer_zero]
  simp [Matrix.one_apply]

/-- The actual Appendix C noise-split definitions with a bounded correction. -/
theorem noise_split_counterexample (S : Finset α) :
    let g : Game α := fun _ => 1
    let γ : Game α := fun _ => 1
    let δ : Game α := fun _ => 0
    |δ S| ≤ (0.02 : ℝ) * |g univ - g ∅| ∧
      ((g S - δ S) / 2 + γ S) + ((g S - δ S) / 2 + γ S) ≠ g S - δ S := by
  norm_num

/-- Appendix D uniqueness of transform coefficients, not merely of one game's dividends. -/
theorem transform_coefficients_unique (a : Finset α → Finset α → ℝ)
    (hm : ∀ g : Game α, ∀ S : Finset α,
      (∑ T ∈ S.powerset, ∑ U ∈ T.powerset, a T U * g U) = g S)
    (S U : Finset α) (hUS : U ⊆ S) :
    a S U = (-1 : ℝ) ^ (S.card - U.card) := by
  let d : Game α := fun L => if L = U then 1 else 0
  let c : Game α := fun T => ∑ L ∈ T.powerset, a T L * d L
  have hc : c = fun T => interaction d T := by
    funext T
    have hh := Harsanyi.reconstruction_unique d c (fun W => hm d W)
    exact congrFun hh T
  have hs := congrFun hc S
  simpa only [c, d, Harsanyi.interaction, mul_ite, mul_one, mul_zero,
    Finset.sum_ite_eq', Finset.mem_powerset, if_pos hUS] using hs

end PaperDynamics

open Lean Elab Command Meta
set_option pp.universes true
set_option pp.fullNames true
set_option pp.piBinderTypes true
run_cmd liftTermElabM do
  for name in #[`Harsanyi.TaylorMoments.monomial, `Harsanyi.TaylorMoments.monomial_mask, `Harsanyi.TaylorMoments.polynomial_mask, `Harsanyi.TaylorMoments.normalized_trigger, `Harsanyi.TaylorMoments.zero_trigger_counterexample, `Harsanyi.TaylorMoments.product_mean, `Harsanyi.TaylorMoments.product_variance, `Harsanyi.TaylorMoments.product_memLp, `Harsanyi.TaylorMoments.gaussian_affine_product, `Harsanyi.TaylorMoments.unit_mean_product_variance, `Harsanyi.TaylorMoments.scaling_ratio, `Harsanyi.TaylorMoments.moving_sign_counterexample, `Harsanyi.NoisyRegression.zeta, `Harsanyi.NoisyRegression.zeta_mulVec, `Harsanyi.NoisyRegression.zeta_injective, `Harsanyi.NoisyRegression.gram_posDef, `Harsanyi.NoisyRegression.normalMatrix, `Harsanyi.NoisyRegression.normal_posDef, `Harsanyi.NoisyRegression.normal_isUnit, `Harsanyi.NoisyRegression.normal_solution, `Harsanyi.NoisyRegression.zero_noise, `Harsanyi.NoisyRegression.quadraticLoss, `Harsanyi.NoisyRegression.symmetric_dot, `Harsanyi.NoisyRegression.quadratic_difference, `Harsanyi.NoisyRegression.quadratic_unique_min, `Harsanyi.NoisyRegression.normal_unique_min, `Harsanyi.NoisyRegression.residualLoss, `Harsanyi.NoisyRegression.residualLoss_expansion, `Harsanyi.NoisyRegression.residual_unique_min, `Harsanyi.NoisyRegression.featureLoss, `Harsanyi.NoisyRegression.feature_normal_scaling, `Harsanyi.NoisyRegression.transferMatrix, `Harsanyi.NoisyRegression.zeta_permutation, `Harsanyi.NoisyRegression.transfer_permutation, `Harsanyi.NoisyRegression.row_norm_permutation, `Harsanyi.NoisyRegression.exists_coalition_permutation, `Harsanyi.NoisyRegression.equal_order_row_norm, `Harsanyi.NoisyRegression.transfer_zero, `Harsanyi.NoisyRegression.diagonal_product_counterexample, `Harsanyi.GaussianRegression.gaussian_memLp, `Harsanyi.GaussianRegression.gaussian_mean, `Harsanyi.GaussianRegression.independent_residual, `Harsanyi.GaussianRegression.gaussian_residual, `Harsanyi.PolynomialSupport.polynomial, `Harsanyi.PolynomialSupport.supportCoefficient, `Harsanyi.PolynomialSupport.mask_terms, `Harsanyi.PolynomialSupport.support_reconstruct, `Harsanyi.PolynomialSupport.interaction_eq_supportCoefficient, `PaperDynamics.efficiency, `PaperDynamics.dummy, `PaperDynamics.symmetry, `PaperDynamics.noisyLoss, `PaperDynamics.noisyLoss_expansion, `PaperDynamics.noisyLoss_unique_min, `PaperDynamics.meanNoisyLoss, `PaperDynamics.meanNoisyLoss_unique_min, `PaperDynamics.zero_noise_recovery, `PaperDynamics.correlated_noise_counterexample, `PaperDynamics.equal_order_norm, `PaperDynamics.zero_noise_row_ratio, `PaperDynamics.noise_split_counterexample, `PaperDynamics.transform_coefficients_unique, `Harsanyi.reconstruction, `Harsanyi.reconstruction_unique, `Harsanyi.interaction_insert, `Harsanyi.interaction_add, `Harsanyi.interaction_recursive, `Harsanyi.interaction_relabel, `Harsanyi.interaction_unanimity, `Harsanyi.or_dual, `Harsanyi.maskCoordinates_complement, `Harsanyi.or_reconstruction, `Harsanyi.Layerwise.and_or_matching, `Harsanyi.and_gaussian_variance, `Harsanyi.signed_gaussian_variance] do
    let info ← getConstInfo name
    let signature ← ppExpr info.type
    let axioms ← Lean.collectAxioms name
    let deps := info.type.getUsedConstants ++ (info.value?.map Expr.getUsedConstants).getD #[]
    let kind := match info with | .thmInfo _ => "theorem" | .inductInfo _ => "inductive" | _ => "definition"
    liftM <| IO.println ("DYNAMICS_API:" ++ (Json.mkObj [
      ("name", toJson name.toString), ("signature", toJson signature.pretty),
      ("kind", toJson kind), ("axioms", toJson (axioms.map Name.toString)),
      ("dependencies", toJson (deps.map Name.toString))]).compress)
