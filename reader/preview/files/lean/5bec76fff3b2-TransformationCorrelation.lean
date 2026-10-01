import Harsanyi.Extensions.TransformationFinite
import Mathlib.Algebra.BigOperators.Ring.Finset

namespace Harsanyi.Entropy
open Finset
open scoped BigOperators
variable {A B : Type*} [Fintype A] [Fintype B] [DecidableEq B]

noncomputable def pushLaw (p : Law A) (f : A → B) : Law B where
  mass := fun b => ∑ a, if f a = b then p.mass a else 0
  nonneg := fun b => sum_nonneg (fun a _ => by split_ifs <;> simp_all [p.nonneg a])
  total := by
    classical
    rw [sum_comm]
    simp [p.total]

theorem push_expectation (p : Law A) (f : A → B) (h : B → ℝ) :
    (∑ b, (pushLaw p f).mass b * h b) = ∑ a, p.mass a * h (f a) := by
  classical
  unfold pushLaw
  simp_rw [sum_mul]
  rw [sum_comm]
  apply sum_congr rfl
  intro a _
  simp

theorem push_mass_ge (p : Law A) (f : A → B) (a : A) :
    p.mass a ≤ (pushLaw p f).mass (f a) := by
  classical
  change p.mass a ≤ ∑ x, if f x = f a then p.mass x else 0
  have h : (if f a = f a then p.mass a else 0) ≤
      ∑ x : A, if f x = f a then p.mass x else 0 :=
    single_le_sum (f := fun x : A => if f x = f a then p.mass x else 0)
      (fun x _ => by dsimp; split_ifs <;> simp_all [p.nonneg x]) (mem_univ a)
  simpa using h

variable {ι : Type*} [Fintype ι] [DecidableEq ι]

noncomputable def coordinateLaw (p : Law (ι → Bool)) (d : ι) : Law Bool := pushLaw p (fun s => s d)

noncomputable def productCoordinateLaw (p : Law (ι → Bool)) : Law (ι → Bool) where
  mass := fun s => ∏ d, (coordinateLaw p d).mass (s d)
  nonneg := fun s => prod_nonneg (fun d _ => (coordinateLaw p d).nonneg _)
  total := by
    rw [← Fintype.prod_sum]
    simp only [(coordinateLaw p _).total, prod_const_one]

noncomputable def totalCorrelation (p : Law (ι → Bool)) : ℝ :=
  divergence p.mass (productCoordinateLaw p).mass

theorem product_coordinate_support (p : Law (ι → Bool)) (s : ι → Bool) (hs : p.mass s ≠ 0) :
    (productCoordinateLaw p).mass s ≠ 0 := by
  apply prod_ne_zero_iff.mpr
  intro d _
  exact ne_of_gt (lt_of_lt_of_le (lt_of_le_of_ne (p.nonneg s) (Ne.symm hs))
    (push_mass_ge p (fun s => s d) s))

theorem total_correlation_nonneg (p : Law (ι → Bool)) : 0 ≤ totalCorrelation p :=
  divergence_nonneg p (productCoordinateLaw p) (product_coordinate_support p)

theorem total_correlation_zero_iff_independent (p : Law (ι → Bool)) :
    totalCorrelation p = 0 ↔ p.mass = (productCoordinateLaw p).mass :=
  divergence_zero_iff p _ (product_coordinate_support p)

/-- Full multivariate total-correlation identity from the actual KL definition,
not from a premise postulating the desired entropy equality. -/
theorem total_correlation_entropy_identity (p : Law (ι → Bool)) :
    entropy p.mass + totalCorrelation p = ∑ d, entropy (coordinateLaw p d).mass := by
  classical
  have term (s : ι → Bool) :
      p.mass s * Real.log (p.mass s / (productCoordinateLaw p).mass s) =
        -Real.negMulLog (p.mass s) - ∑ d, p.mass s * Real.log ((coordinateLaw p d).mass (s d)) := by
    by_cases hs : p.mass s = 0
    · simp [hs]
    · have hc (d : ι) : (coordinateLaw p d).mass (s d) ≠ 0 :=
        ne_of_gt (lt_of_lt_of_le (lt_of_le_of_ne (p.nonneg s) (Ne.symm hs))
          (push_mass_ge p (fun s => s d) s))
      rw [Real.log_div hs (product_coordinate_support p s hs)]
      change p.mass s * (Real.log (p.mass s) - Real.log (∏ d, (coordinateLaw p d).mass (s d))) = _
      rw [Real.log_prod univ (fun d => (coordinateLaw p d).mass (s d)) (fun d _ => hc d)]
      simp only [mul_sub, mul_sum, Real.negMulLog]
      ring
  unfold totalCorrelation divergence
  simp_rw [term, sum_sub_distrib]
  rw [sum_comm (f := fun s d => p.mass s * Real.log ((coordinateLaw p d).mass (s d)))]
  have hc (d : ι) : (∑ s, p.mass s * Real.log ((coordinateLaw p d).mass (s d))) =
      -entropy (coordinateLaw p d).mass := by
    rw [← push_expectation p (fun s => s d) (fun b => Real.log ((coordinateLaw p d).mass b))]
    simp [entropy, coordinateLaw, Real.negMulLog, neg_mul, sum_neg_distrib]
  simp_rw [hc, sum_neg_distrib]
  change entropy p.mass + (-entropy p.mass - -(∑ d, entropy (coordinateLaw p d).mass)) = _
  ring

/-- Source's input-information/TC identity retains a genuine conditional-entropy
residual; for deterministic gates the separate gate kernel proves it zero. -/
theorem information_correlation_identity (p : Law (ι → Bool)) (hconditional : ℝ) :
    (entropy p.mass - hconditional) + totalCorrelation p =
      (∑ d, entropy (coordinateLaw p d).mass) - hconditional := by
  have h := total_correlation_entropy_identity p
  linarith

theorem conditional_correlation_identity (q : Law A) (k : A → Law (ι → Bool)) :
    (∑ a, q.mass a * entropy (k a).mass) +
      (∑ a, q.mass a * totalCorrelation (k a)) =
        ∑ a, q.mass a * ∑ d, entropy (coordinateLaw (k a) d).mass := by
  rw [← sum_add_distrib]
  apply sum_congr rfl
  intro a _
  rw [← mul_add, total_correlation_entropy_identity]

/-- Source Eq.(22), for the actual label/gate joint law. The conditioned gate
laws are obtained by disintegration, without postulating the entropy/TC result. -/
theorem label_information_correlation_identity (p : Law (A × (ι → Bool))) :
    mutualInformation p.mass + totalCorrelation (columnLaw p) -
      (∑ a, (rowLaw p).mass a * totalCorrelation (conditionalRow p a)) =
    (∑ d, entropy (coordinateLaw (columnLaw p) d).mass) -
      (∑ a, (rowLaw p).mass a * ∑ d, entropy (coordinateLaw (conditionalRow p a) d).mass) := by
  have hj := entropy_chain p.mass p.nonneg
  have ht := total_correlation_entropy_identity (columnLaw p)
  have hc := conditional_correlation_identity (rowLaw p) (conditionalRow p)
  rw [← actual_conditional_entropy] at hc
  unfold mutualInformation
  change entropy (rowLaw p).mass + entropy (columnLaw p).mass - entropy p.mass + _ - _ = _
  change entropy p.mass = entropy (rowLaw p).mass + conditionalEntropy p.mass at hj
  linarith

end Harsanyi.Entropy
