import Harsanyi.Core.Properties

open Finset Harsanyi

namespace APIPlaytestMax

/-- Removing the baseline after an affine output change deletes exactly the
    empty coefficient; every nonempty coefficient is scaled by `a`. -/
theorem centered_affine_interaction {α : Type*} [DecidableEq α]
    (v : Game α) (a b : ℝ) (S : Finset α) :
    interaction (centered (fun T => a * v T + b)) S =
      if S = ∅ then 0 else a * interaction v S := by
  rw [interaction_centered, interaction_add, interaction_smul, interaction_const]
  by_cases hS : S = ∅
  · subst S
    simp only [if_pos rfl, interaction_empty]
    ring
  · simp only [if_neg hS, add_zero, sub_zero]

/-- Any coefficient function reconstructing the centered affine game must
    have the above coefficients, including the zero empty coefficient. -/
theorem centered_affine_unique {α : Type*} [DecidableEq α]
    (v d : Game α) (a b : ℝ)
    (h : ∀ S, reconstruct d S = centered (fun T => a * v T + b) S) :
    d = fun S => if S = ∅ then 0 else a * interaction v S := by
  have hd := reconstruction_unique (centered (fun T => a * v T + b)) d h
  rw [hd]
  funext S
  exact centered_affine_interaction v a b S

/-- A checkable witness that omitting nonemptiness is unsound in the separate
    rejection fixture: for the constant-one game, the empty coefficient is 1. -/
theorem empty_centering_counterexample :
    interaction (centered (fun _ : Finset (Fin 1) => (1 : ℝ))) ∅ ≠
      interaction (fun _ : Finset (Fin 1) => (1 : ℝ)) ∅ := by
  rw [interaction_empty, interaction_empty]
  norm_num [centered]

end APIPlaytestMax

#print axioms APIPlaytestMax.centered_affine_interaction
#print axioms APIPlaytestMax.centered_affine_unique
#print axioms APIPlaytestMax.empty_centering_counterexample
