import Harsanyi.Extensions.TransformationEntropy

namespace Harsanyi.Entropy
open Finset
open scoped BigOperators
variable {A B C : Type*} [Fintype A] [Fintype B] [Fintype C]

noncomputable def kernelLaw (q : Law A) (k : A → Law B) : Law (A × B) where
  mass := fun z => q.mass z.1 * (k z.1).mass z.2
  nonneg := fun z => mul_nonneg (q.nonneg _) ((k _).nonneg _)
  total := by
    simp [Fintype.sum_prod_type, ← mul_sum, (k _).total, q.total]

theorem kernel_marginal (q : Law A) (k : A → Law B) (a : A) :
    marginal (kernelLaw q k).mass a = q.mass a := by
  simp [marginal, kernelLaw, ← mul_sum, (k a).total]

theorem conditional_entropy_kernel (q : Law A) (k : A → Law B) :
    conditionalEntropy (kernelLaw q k).mass = ∑ a, q.mass a * entropy (k a).mass := by
  classical
  unfold conditionalEntropy
  simp_rw [kernel_marginal]
  apply sum_congr rfl
  intro a _
  by_cases ha : q.mass a = 0
  · simp [ha]
  · congr 1
    apply congrArg entropy
    funext b
    change q.mass a * (k a).mass b / q.mass a = (k a).mass b
    field_simp

theorem entropy_kernel (q : Law A) (k : A → Law B) :
    entropy (kernelLaw q k).mass = entropy q.mass + ∑ a, q.mass a * entropy (k a).mass := by
  rw [entropy_chain _ (kernelLaw q k).nonneg, conditional_entropy_kernel]
  have h : marginal (kernelLaw q k).mass = q.mass := by
    funext a
    exact kernel_marginal q k a
  rw [h]

theorem entropy_comp_equiv {D E : Type*} [Fintype D] [Fintype E]
    (e : D ≃ E) (p : E → ℝ) : entropy (fun d => p (e d)) = entropy p := by
  unfold entropy
  exact Equiv.sum_comp e (fun x => Real.negMulLog (p x))

/-- The original three-variable joint law, regrouped to refined-gate/label form. -/
noncomputable def refinedKernelLaw (q : Law A) (k : A → Law (B × C)) : Law ((A × B) × C) where
  mass := fun z => q.mass z.1.1 * (k z.1.1).mass (z.1.2,z.2)
  nonneg := fun z => mul_nonneg (q.nonneg _) ((k _).nonneg _)
  total := by
    change (∑ z : (A × B) × C, (kernelLaw q k).mass ((Equiv.prodAssoc A B C) z)) = 1
    rw [Equiv.sum_comp]
    exact (kernelLaw q k).total

theorem refined_row_mass (q : Law A) (k : A → Law (B × C)) (a : A) (b : B) :
    (rowLaw (refinedKernelLaw q k)).mass (a,b) =
      (kernelLaw q (fun a => rowLaw (k a))).mass (a,b) := by
  simp [rowLaw, marginal, refinedKernelLaw, kernelLaw, ← mul_sum]

theorem refined_column_mass (q : Law A) (k : A → Law (B × C)) (c : C) :
    (columnLaw (refinedKernelLaw q k)).mass c =
      (columnLaw (kernelLaw q (fun a => columnLaw (k a)))).mass c := by
  simp [columnLaw, refinedKernelLaw, kernelLaw, Fintype.sum_prod_type, ← mul_sum]

theorem refined_entropy (q : Law A) (k : A → Law (B × C)) :
    entropy (refinedKernelLaw q k).mass = entropy (kernelLaw q k).mass := by
  exact entropy_comp_equiv (Equiv.prodAssoc A B C) (kernelLaw q k).mass

/-- Genuine finite conditional-information chain identity, including zero-mass
conditioning states: all kernels on those states are multiplied by zero. -/
theorem refined_information_difference (q : Law A) (k : A → Law (B × C)) :
    mutualInformation (refinedKernelLaw q k).mass -
      mutualInformation (kernelLaw q (fun a => columnLaw (k a))).mass =
        ∑ a, q.mass a * mutualInformation (k a).mass := by
  have hr : (rowLaw (refinedKernelLaw q k)).mass =
      (kernelLaw q (fun a => rowLaw (k a))).mass := by
    funext z
    exact refined_row_mass q k z.1 z.2
  have hc : (columnLaw (refinedKernelLaw q k)).mass =
      (columnLaw (kernelLaw q (fun a => columnLaw (k a)))).mass := by
    funext c
    exact refined_column_mass q k c
  unfold mutualInformation
  change entropy (rowLaw _).mass + entropy (columnLaw _).mass - entropy _ -
    (entropy (rowLaw _).mass + entropy (columnLaw _).mass - entropy _) = _
  rw [hr, hc, refined_entropy, entropy_kernel, entropy_kernel, entropy_kernel]
  simp_rw [show (rowLaw (kernelLaw q (fun a => columnLaw (k a)))).mass = q.mass by
    funext a; exact kernel_marginal q _ a]
  change _ = ∑ a, q.mass a *
    (entropy (rowLaw (k a)).mass + entropy (columnLaw (k a)).mass - entropy (k a).mass)
  simp_rw [mul_sub, mul_add, sum_sub_distrib, sum_add_distrib]
  ring

theorem refined_information_monotone (q : Law A) (k : A → Law (B × C)) :
    mutualInformation (kernelLaw q (fun a => columnLaw (k a))).mass ≤
      mutualInformation (refinedKernelLaw q k).mass := by
  have h : 0 ≤ ∑ a, q.mass a * mutualInformation (k a).mass :=
    sum_nonneg (fun a _ => mul_nonneg (q.nonneg a) (mutual_information_nonneg (k a)))
  rw [← refined_information_difference] at h
  linarith

/-- Disintegrate an actual finite joint law. On zero-mass conditioning states
the existing column marginal is an arbitrary normalized fallback, multiplied by
zero in every joint or conditional-information expression. -/
noncomputable def conditionalRow (p : Law (A × B)) (a : A) : Law B where
  mass := fun b => if (rowLaw p).mass a = 0 then (columnLaw p).mass b
    else p.mass (a,b)/(rowLaw p).mass a
  nonneg := by
    intro b; split_ifs
    · exact (columnLaw p).nonneg b
    · exact div_nonneg (p.nonneg _) ((rowLaw p).nonneg _)
  total := by
    classical
    split_ifs with ha
    · exact (columnLaw p).total
    · rw [← sum_div]
      exact div_self ha

theorem kernel_disintegration (p : Law (A × B)) :
    (kernelLaw (rowLaw p) (conditionalRow p)).mass = p.mass := by
  funext z
  change (rowLaw p).mass z.1 * (if (rowLaw p).mass z.1 = 0 then _ else _) = _
  by_cases h : (rowLaw p).mass z.1 = 0
  · simp only [h, ite_true, zero_mul]
    exact (mass_zero_of_marginal_zero p.mass p.nonneg z.1 h z.2).symm
  · simp only [h, ite_false]
    field_simp

theorem actual_conditional_entropy (p : Law (A × B)) :
    conditionalEntropy p.mass = ∑ a, (rowLaw p).mass a * entropy (conditionalRow p a).mass := by
  have h := conditional_entropy_kernel (rowLaw p) (conditionalRow p)
  rw [kernel_disintegration] at h
  exact h

theorem actual_joint_refinement_monotone (p : Law (A × (B × C))) :
    mutualInformation (kernelLaw (rowLaw p) (fun a => columnLaw (conditionalRow p a))).mass ≤
      mutualInformation (refinedKernelLaw (rowLaw p) (conditionalRow p)).mass :=
  refined_information_monotone _ _

end Harsanyi.Entropy
