import Harsanyi.Core.Properties

open Finset Harsanyi

namespace APIPlaytestMax

theorem centered_affine_interaction {α : Type*} [DecidableEq α]
    (v : Game α) (a b : ℝ) (S : Finset α) :
    interaction (centered (fun T => a * v T + b)) S =
      if S = ∅ then 0 else a * interaction v S := by
  rw [interaction_centered, interaction_add, interaction_smul, interaction_const]
  by_cases hS : S = ∅
  · subst S
    simp [interaction_empty]
  · simp only [if_neg hS, add_zero, sub_zero]

theorem centered_affine_unique {α : Type*} [DecidableEq α]
    (v d : Game α) (a b : ℝ)
    (h : ∀ S, reconstruct d S = centered (fun T => a * v T + b) S) :
    d = fun S => if S = ∅ then 0 else a * interaction v S := by
  have hd := reconstruction_unique (centered (fun T => a * v T + b)) d h
  rw [hd]
  funext S
  exact centered_affine_interaction v a b S

end APIPlaytestMax

open Lean in
run_cmd do
  let env ← getEnv
  for decl in [`APIPlaytestMax.centered_affine_interaction,
      `APIPlaytestMax.centered_affine_unique] do
    let some info := env.find? decl | throwError "Declaration missing: {decl}"
    let some value := info.value? | throwError "Proof value missing: {decl}"
    let deps := value.getUsedConstants
    logInfo m!"API_DEPENDENCIES {decl}: {deps}"
