import Harsanyi.Extensions.TaylorMoments

namespace Harsanyi.PolynomialSupport
open Finset
variable {α κ : Type*} [DecidableEq α] [DecidableEq κ]

/-- An arbitrary finite list of monomials; equal supports may have different degrees. -/
noncomputable def polynomial (P : Finset κ) (A : κ → Finset α) (c : κ → ℝ)
    (degree : κ → α → ℕ) (z : α → ℝ) : ℝ :=
  ∑ k ∈ P, c k * TaylorMoments.monomial (A k) (degree k) z

noncomputable def supportCoefficient (P : Finset κ) (A : κ → Finset α) (c : κ → ℝ)
    (degree : κ → α → ℕ) (z : α → ℝ) (T : Finset α) : ℝ :=
  ∑ k ∈ P, if A k = T then c k * TaylorMoments.monomial (A k) (degree k) z else 0

theorem mask_terms (P : Finset κ) (A : κ → Finset α) (c : κ → ℝ)
    (degree : κ → α → ℕ) (z : α → ℝ) (S : Finset α)
    (hd : ∀ k ∈ P, ∀ i ∈ A k, degree k i ≠ 0) :
    polynomial P A c degree (fun i => if i ∈ S then z i else 0) =
      ∑ k ∈ P, if A k ⊆ S then c k * TaylorMoments.monomial (A k) (degree k) z else 0 := by
  unfold polynomial
  apply sum_congr rfl
  intro k hk
  rw [TaylorMoments.monomial_mask (A k) S _ _ (hd k hk)]
  split_ifs <;> simp

/-- Grouping by support is proved by exchanging two finite sums. -/
theorem support_reconstruct (P : Finset κ) (A : κ → Finset α) (c : κ → ℝ)
    (degree : κ → α → ℕ) (z : α → ℝ) (S : Finset α) :
    reconstruct (supportCoefficient P A c degree z) S =
      ∑ k ∈ P, if A k ⊆ S then c k * TaylorMoments.monomial (A k) (degree k) z else 0 := by
  unfold reconstruct supportCoefficient
  rw [sum_comm]
  apply sum_congr rfl
  intro k hk
  simp

/-- Full dividend identification for arbitrary finite monomials, including repeated supports. -/
theorem interaction_eq_supportCoefficient (P : Finset κ) (A : κ → Finset α) (c : κ → ℝ)
    (degree : κ → α → ℕ) (z : α → ℝ)
    (hd : ∀ k ∈ P, ∀ i ∈ A k, degree k i ≠ 0) (T : Finset α) :
    interaction (fun S => polynomial P A c degree (fun i => if i ∈ S then z i else 0)) T =
      supportCoefficient P A c degree z T := by
  have h : (fun S => polynomial P A c degree (fun i => if i ∈ S then z i else 0)) =
      reconstruct (supportCoefficient P A c degree z) := by
    funext S
    rw [mask_terms P A c degree z S hd, support_reconstruct]
  rw [h, interaction_reconstruct]

end Harsanyi.PolynomialSupport
