import Mathlib.Data.Real.Basic
import Mathlib.Algebra.BigOperators.Group.Finset.Powerset
import Mathlib.Tactic

/-! Finite coalitions. An ambient finite variable set is represented by a finite type
(or by a subtype of a `Finset`); all results also work for finite coalitions in an
arbitrary type. No zero-baseline assumption is implicit. -/
namespace Harsanyi
open Finset
variable {α : Type*} [DecidableEq α]

/-- A real-valued function of finite coalitions. -/
abbrev Game (α : Type*) := Finset α → ℝ

/-- The Harsanyi (Boolean Möbius) transform, including the empty coalition. -/
noncomputable def interaction (v : Game α) (S : Finset α) : ℝ :=
  ∑ T ∈ S.powerset, (-1 : ℝ) ^ (S.card - T.card) * v T

/-- Reconstruct a game by summing dividends of all subcoalitions. -/
noncomputable def reconstruct (d : Game α) (S : Finset α) : ℝ :=
  ∑ T ∈ S.powerset, d T

/-- Explicit conversion to the convention with zero empty-coalition value. -/
noncomputable def centered (v : Game α) : Game α := fun S => v S - v ∅

/-- Marginal contribution of inserting a variable. -/
noncomputable def marginal (v : Game α) (i : α) : Game α :=
  fun S => v (insert i S) - v S

@[simp] theorem interaction_empty (v : Game α) : interaction v ∅ = v ∅ := by
  simp [interaction]

@[simp] theorem reconstruct_empty (d : Game α) : reconstruct d ∅ = d ∅ := by
  simp [reconstruct]

@[simp] theorem centered_empty (v : Game α) : centered v ∅ = 0 := by
  simp [centered]

theorem interaction_congr (v w : Game α) (S : Finset α)
    (h : ∀ T ⊆ S, v T = w T) : interaction v S = interaction w S := by
  apply Finset.sum_congr rfl
  intro T hT
  rw [h T (mem_powerset.mp hT)]

@[simp] theorem interaction_singleton (v : Game α) (i : α) :
    interaction v {i} = v {i} - v ∅ := by
  unfold interaction
  rw [show ({i} : Finset α) = insert i ∅ from rfl,
    sum_powerset_insert (notMem_empty i)]
  simp [sub_eq_add_neg, add_comm]

end Harsanyi
