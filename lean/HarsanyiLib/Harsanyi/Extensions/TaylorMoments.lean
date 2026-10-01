import Harsanyi.Core.Properties
import Mathlib.Probability.Independence.Integration
import Mathlib.Probability.Moments.Variance
import Mathlib.Probability.Distributions.Gaussian.Real

set_option maxHeartbeats 1200000

namespace Harsanyi.TaylorMoments
open Finset MeasureTheory ProbabilityTheory
open scoped ProbabilityTheory
variable {α Ω : Type*} [DecidableEq α]

/-- A coordinate monomial with support A and strictly positive degrees on A. -/
noncomputable def monomial (A : Finset α) (degree : α → ℕ) (z : α → ℝ) : ℝ :=
  ∏ i ∈ A, z i ^ degree i

/-- Masking a monomial retains it exactly when its support is retained. -/
theorem monomial_mask (A S : Finset α) (degree : α → ℕ) (z : α → ℝ)
    (hd : ∀ i ∈ A, degree i ≠ 0) :
    monomial A degree (fun i => if i ∈ S then z i else 0) =
      if A ⊆ S then monomial A degree z else 0 := by
  classical
  by_cases h : A ⊆ S
  · rw [if_pos h]
    apply prod_congr rfl
    intro i hi
    simp [h hi]
  · rw [if_neg h]
    obtain ⟨i, hi, his⟩ := Finset.not_subset.mp h
    apply prod_eq_zero hi
    simp [his, hd i hi]

/-- A finite polynomial is reconstructed by coefficients grouped by monomial support. -/
theorem polynomial_mask (P : Finset (Finset α)) (c : Finset α → ℝ)
    (degree : Finset α → α → ℕ) (z : α → ℝ) (S : Finset α)
    (hd : ∀ A ∈ P, ∀ i ∈ A, degree A i ≠ 0) :
    (∑ A ∈ P, c A * monomial A (degree A) (fun i => if i ∈ S then z i else 0)) =
    ∑ A ∈ P, if A ⊆ S then c A * monomial A (degree A) z else 0 := by
  apply sum_congr rfl
  intro A hA
  rw [monomial_mask A S _ _ (hd A hA)]
  split_ifs <;> simp

/-- Normalization of an exactly supported nonzero term. The nonzero premise is explicit. -/
theorem normalized_trigger (A S : Finset α) (u : ℝ) (hu : u ≠ 0) :
    (if A ⊆ S then u else 0) / u = if A ⊆ S then (1 : ℝ) else 0 := by
  split_ifs <;> simp [hu]

/-- The printed unconditional normalization fails when the interaction vanishes. -/
theorem zero_trigger_counterexample : (0 : ℝ) / 0 ≠ 1 := by norm_num

section Probability
variable [MeasurableSpace Ω] {μ : Measure Ω} [IsProbabilityMeasure μ]
variable {ι : Type*} [Fintype ι] {X : ι → Ω → ℝ}

/-- Actual independent random variables, not formal moment placeholders. -/
theorem product_mean (h : iIndepFun X μ)
    (hm : ∀ i, AEStronglyMeasurable (X i) μ) :
    (∫ ω, ∏ i, X i ω ∂μ) = ∏ i, ∫ ω, X i ω ∂μ :=
  h.integral_fun_prod_eq_prod_integral hm

/-- Independent product variance, including all first and second moments. -/
theorem product_variance (h : iIndepFun X μ)
    (hm : ∀ i, AEStronglyMeasurable (X i) μ)
    (hp : ∀ i, MemLp (X i) 2 μ)
    (hprod : MemLp (fun ω => ∏ i, X i ω) 2 μ) :
    variance (fun ω => ∏ i, X i ω) μ =
      (∏ i, ((∫ ω, X i ω ∂μ) ^ 2 + variance (X i) μ)) -
      (∏ i, (∫ ω, X i ω ∂μ) ^ 2) := by
  have hs : iIndepFun (fun i ω => X i ω ^ 2) μ :=
    h.comp (fun _ x => x ^ 2) (fun _ => measurable_id.pow_const 2)
  have hms : ∀ i, AEStronglyMeasurable (fun ω => X i ω ^ 2) μ :=
    fun i => (hm i).pow 2
  rw [variance_eq_sub hprod]
  change (∫ ω, (∏ i, X i ω) ^ 2 ∂μ) - (∫ ω, ∏ i, X i ω ∂μ) ^ 2 = _
  simp_rw [← Finset.prod_pow]
  rw [hs.integral_fun_prod_eq_prod_integral hms, product_mean h hm]
  have hx : ∀ i, (∫ ω, X i ω ^ 2 ∂μ) =
      (∫ ω, X i ω ∂μ) ^ 2 + variance (X i) μ := by
    intro i
    rw [variance_eq_sub (hp i)]
    simp only [Pi.pow_apply]
    ring
  simp_rw [hx, Finset.prod_pow]

/-- Independent square-integrable factors have a square-integrable product. -/
theorem product_memLp (h : iIndepFun X μ)
    (hm : ∀ i, Measurable (X i)) (hp : ∀ i, MemLp (X i) 2 μ) :
    MemLp (fun ω => ∏ i, X i ω) 2 μ := by
  have hf : ∀ i, Integrable (fun x : ℝ => x ^ 2) (μ.map (X i)) := by
    intro i
    apply (integrable_map_measure (by fun_prop) (hm i).aemeasurable).2
    simpa only [Function.comp_def] using (hp i).integrable_sq
  have hi := Integrable.fintype_prod hf
  have heq := (iIndepFun_iff_map_fun_eq_pi_map (fun i => (hm i).aemeasurable)).1 h
  rw [← heq] at hi
  have hs := hi.comp_aemeasurable (by fun_prop : AEMeasurable (fun ω i => X i ω) μ)
  apply (memLp_two_iff_integrable_sq (by fun_prop)).2
  simpa only [Function.comp_def, ← Finset.prod_pow] using hs

/-- A complete Gaussian lowest-order product calculation, with no moment hypotheses. -/
theorem gaussian_affine_product (ε : ι → Ω → ℝ) (q : NNReal)
    (hm : ∀ i, Measurable (ε i))
    (hlaw : ∀ i, μ.map (ε i) = gaussianReal 0 q)
    (hi : iIndepFun ε μ) :
    (∫ ω, ∏ i, (1 + ε i ω) ∂μ) = 1 ∧
      variance (fun ω => ∏ i, (1 + ε i ω)) μ =
        (1 + (q : ℝ)) ^ Fintype.card ι - 1 := by
  have hp : ∀ i, MemLp (ε i) 2 μ := by
    intro i
    have h : MemLp id 2 (μ.map (ε i)) := by
      rw [hlaw i]
      exact memLp_id_gaussianReal' 2 (by norm_num)
    simpa only [Function.comp_def, id_eq] using
      h.comp_measurePreserving ⟨hm i, hlaw i ▸ rfl⟩
  have hp' : ∀ i, MemLp (fun ω => 1 + ε i ω) 2 μ := by
    intro i
    exact (memLp_const (p := 2) (μ := μ) (1 : ℝ)).add (hp i)
  have hi' : iIndepFun (fun i ω => 1 + ε i ω) μ :=
    hi.comp (fun _ x => 1 + x) (fun _ => measurable_const.add measurable_id)
  have hm' : ∀ i, Measurable (fun ω => 1 + ε i ω) := by
    intro i
    fun_prop
  have hmean : ∀ i, ∫ ω, (1 + ε i ω) ∂μ = 1 := by
    intro i
    rw [integral_add (integrable_const 1) ((hp i).integrable (by norm_num))]
    have he : (∫ ω, ε i ω ∂μ) = 0 := by
      calc
        (∫ ω, ε i ω ∂μ) = ∫ z, z ∂μ.map (ε i) := by
          symm
          simpa only [id_eq] using integral_map (hm i).aemeasurable (aestronglyMeasurable_id : AEStronglyMeasurable (id : ℝ → ℝ) (μ.map (ε i)))
        _ = 0 := by rw [hlaw i]; exact integral_id_gaussianReal
    simp [he]
  have hvar : ∀ i, variance (fun ω => 1 + ε i ω) μ = q := by
    intro i
    rw [variance_const_add (hm i).aestronglyMeasurable]
    rw [← variance_id_map (hm i).aemeasurable, hlaw i]
    exact variance_id_gaussianReal
  exact unit_mean_product_variance_aux hi' hm' hp' hmean hvar
where
  unit_mean_product_variance_aux {X : ι → Ω → ℝ} (h : iIndepFun X μ)
      (hm : ∀ i, Measurable (X i)) (hp : ∀ i, MemLp (X i) 2 μ)
      (hmean : ∀ i, ∫ ω, X i ω ∂μ = 1)
      (hvar : ∀ i, variance (X i) μ = q) :
      (∫ ω, ∏ i, X i ω ∂μ) = 1 ∧
      variance (fun ω => ∏ i, X i ω) μ = (1 + (q : ℝ)) ^ Fintype.card ι - 1 := by
    constructor
    · rw [product_mean h (fun i => (hm i).aestronglyMeasurable)]
      simp [hmean]
    · rw [product_variance h (fun i => (hm i).aestronglyMeasurable) hp (product_memLp h hm hp)]
      simp [hmean, hvar]

/-- Lowest signed multilinear moment once each actual factor has mean 1 and variance q. -/
theorem unit_mean_product_variance (q : ℝ) (h : iIndepFun X μ)
    (hm : ∀ i, AEStronglyMeasurable (X i) μ)
    (hp : ∀ i, MemLp (X i) 2 μ)
    (hprod : MemLp (fun ω => ∏ i, X i ω) 2 μ)
    (hmean : ∀ i, ∫ ω, X i ω ∂μ = 1)
    (hvar : ∀ i, variance (X i) μ = q) :
    (∫ ω, ∏ i, X i ω ∂μ) = 1 ∧
    variance (fun ω => ∏ i, X i ω) μ = (1 + q) ^ Fintype.card ι - 1 := by
  constructor
  · rw [product_mean h hm]
    simp [hmean]
  · rw [product_variance h hm hp hprod]
    simp [hmean, hvar]

end Probability

/-- Algebraic scaling used by the Bayesian concept bound. -/
theorem scaling_ratio (u m v : ℝ) (hu : u ≠ 0) (hv : v ≠ 0) :
    |m| / v = |u| * (|u * m| / (u ^ 2 * v)) := by
  rw [abs_mul, ← sq_abs u]
  have hau : |u| ≠ 0 := abs_ne_zero.mpr hu
  field_simp
  <;> ring

/-- The source sign-dependent odd-degree coefficient cannot be fixed across orthants. -/
theorem moving_sign_counterexample :
    (-1 : ℝ) * ((-1 : ℝ) * (-1 : ℝ)) ≠ (1 : ℝ) := by norm_num

end Harsanyi.TaylorMoments
