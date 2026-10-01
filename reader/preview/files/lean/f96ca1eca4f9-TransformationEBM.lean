import Harsanyi.Extensions.TransformationCorrelation
import Mathlib.Analysis.SpecialFunctions.ExpDeriv
import Mathlib.Analysis.SpecialFunctions.Log.Deriv

namespace Harsanyi.Entropy
open Finset
open scoped BigOperators
variable {A E : Type*} [Fintype A] [NormedAddCommGroup E] [NormedSpace ℝ E]

noncomputable def partition (q : Law A) (f : A → ℝ) : ℝ := ∑ a, q.mass a * Real.exp (f a)

theorem law_has_positive_mass (q : Law A) : ∃ a, 0 < q.mass a := by
  by_contra h
  push_neg at h
  have hz : ∀ a, q.mass a = 0 := fun a => le_antisymm (h a) (q.nonneg a)
  have ht := q.total
  simp [hz] at ht

theorem partition_pos (q : Law A) (f : A → ℝ) : 0 < partition q f := by
  obtain ⟨a, ha⟩ := law_has_positive_mass q
  apply lt_of_lt_of_le (mul_pos ha (Real.exp_pos _))
  exact single_le_sum (fun b _ => mul_nonneg (q.nonneg b) (Real.exp_pos _).le) (mem_univ a)

noncomputable def ebmLaw (q : Law A) (f : A → ℝ) : Law A where
  mass := fun a => q.mass a * Real.exp (f a) / partition q f
  nonneg := fun a => div_nonneg (mul_nonneg (q.nonneg a) (Real.exp_pos _).le) (partition_pos q f).le
  total := by
    rw [← sum_div]
    exact div_self (partition_pos q f).ne'

theorem ebm_log_mass (q : Law A) (f : A → ℝ) (a : A) (hq : 0 < q.mass a) :
    Real.log ((ebmLaw q f).mass a) = f a + Real.log (q.mass a) - Real.log (partition q f) := by
  change Real.log (q.mass a * Real.exp (f a) / partition q f) = _
  rw [Real.log_div (mul_pos hq (Real.exp_pos _)).ne' (partition_pos q f).ne',
    Real.log_mul hq.ne' (Real.exp_ne_zero _), Real.log_exp]
  ring

theorem partition_hasFDerivAt (q : Law A) (f : A → E → ℝ) (d : A → E →L[ℝ] ℝ)
    (θ : E) (hf : ∀ a, HasFDerivAt (f a) (d a) θ) :
    HasFDerivAt (fun x => partition q (fun a => f a x))
      (∑ a, (q.mass a * Real.exp (f a θ)) • d a) θ := by
  unfold partition
  have h := HasFDerivAt.fun_sum (u := (univ : Finset A))
    (fun a _ => (hf a).exp.const_mul (q.mass a))
  simpa only [smul_smul] using h

theorem log_partition_hasFDerivAt (q : Law A) (f : A → E → ℝ) (d : A → E →L[ℝ] ℝ)
    (θ : E) (hf : ∀ a, HasFDerivAt (f a) (d a) θ) :
    HasFDerivAt (fun x => Real.log (partition q (fun a => f a x)))
      (∑ a, (ebmLaw q (fun a => f a θ)).mass a • d a) θ := by
  have h := (partition_hasFDerivAt q f d θ hf).log (partition_pos q _).ne'
  convert h using 1
  simp only [smul_sum, smul_smul, ebmLaw, div_eq_mul_inv]
  congr 1
  ext a
  rw [mul_comm]

/-- Negative log likelihood with the empirical law explicit. The prior remains
fixed during the EBM parameter update, as in the author's alternating training. -/
noncomputable def ebmNegativeLogLikelihood (q r : Law A) (f : A → ℝ) : ℝ :=
  Real.log (partition q f) - ∑ a, r.mass a * (f a + Real.log (q.mass a))

theorem ebm_nll_eq_negative_log_probability (q r : Law A) (f : A → ℝ)
    (hq : ∀ a, r.mass a ≠ 0 → 0 < q.mass a) :
    ebmNegativeLogLikelihood q r f = -(∑ a, r.mass a * Real.log ((ebmLaw q f).mass a)) := by
  have ht (a : A) : r.mass a * Real.log ((ebmLaw q f).mass a) =
      r.mass a * (f a + Real.log (q.mass a) - Real.log (partition q f)) := by
    by_cases ha : r.mass a = 0
    · simp [ha]
    · rw [ebm_log_mass q f a (hq a ha)]
  simp_rw [ht, mul_sub, sum_sub_distrib, ← sum_mul, r.total, one_mul]
  unfold ebmNegativeLogLikelihood
  ring

/-- The paper's product of actual marginal activation priors covers the full
empirical support, including deterministic coordinates with rate zero or one. -/
theorem empirical_marginal_prior_nll {ι : Type*} [Fintype ι] [DecidableEq ι]
    (r : Law (ι → Bool)) (f : (ι → Bool) → ℝ) :
    ebmNegativeLogLikelihood (productCoordinateLaw r) r f =
      -(∑ a, r.mass a * Real.log ((ebmLaw (productCoordinateLaw r) f).mass a)) := by
  apply ebm_nll_eq_negative_log_probability
  intro a ha
  exact lt_of_le_of_ne ((productCoordinateLaw r).nonneg a)
    (Ne.symm (product_coordinate_support r a ha))

theorem ebm_nll_hasFDerivAt (q r : Law A) (f : A → E → ℝ) (d : A → E →L[ℝ] ℝ)
    (θ : E) (hf : ∀ a, HasFDerivAt (f a) (d a) θ) :
    HasFDerivAt (fun x => ebmNegativeLogLikelihood q r (fun a => f a x))
      ((∑ a, (ebmLaw q (fun a => f a θ)).mass a • d a) - ∑ a, r.mass a • d a) θ := by
  unfold ebmNegativeLogLikelihood
  apply (log_partition_hasFDerivAt q f d θ hf).sub
  have h := HasFDerivAt.fun_sum (u := (univ : Finset A))
    (fun a _ => ((hf a).add_const (Real.log (q.mass a))).const_mul (r.mass a))
  exact h

/-- Exact Shannon cross entropy decomposition. It does not identify a fitted
model law with the true gate law. -/
theorem cross_entropy_decomposition (r p : Law A)
    (hs : ∀ a, r.mass a ≠ 0 → p.mass a ≠ 0) :
    -(∑ a, r.mass a * Real.log (p.mass a)) = entropy r.mass + divergence r.mass p.mass := by
  have ht (a : A) : r.mass a * Real.log (r.mass a / p.mass a) =
      -Real.negMulLog (r.mass a) - r.mass a * Real.log (p.mass a) := by
    by_cases ha : r.mass a = 0
    · simp [ha]
    · rw [Real.log_div ha (hs a ha)]
      simp [Real.negMulLog]
      ring
  unfold divergence
  simp_rw [ht, sum_sub_distrib]
  simp only [sum_neg_distrib]
  change _ = entropy r.mass + (-entropy r.mass - _)
  ring

end Harsanyi.Entropy
