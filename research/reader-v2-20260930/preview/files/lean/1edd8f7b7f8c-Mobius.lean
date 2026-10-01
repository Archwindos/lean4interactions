import Harsanyi.Core.Basic

namespace Harsanyi
open Finset
variable {α : Type*} [DecidableEq α]

/-- Insertion is a finite difference: it pairs subsets with and without `i`. -/
theorem interaction_insert (v : Game α) (S : Finset α) (i : α) (hi : i ∉ S) :
    interaction v (insert i S) = interaction (marginal v i) S := by
  unfold interaction marginal
  rw [sum_powerset_insert hi]
  have h1 : ∀ T ∈ S.powerset,
      (-1 : ℝ) ^ ((insert i S).card - T.card) * v T =
      -((-1 : ℝ) ^ (S.card - T.card) * v T) := by
    intro T hT
    have hTS := card_le_card (mem_powerset.mp hT)
    rw [card_insert_of_notMem hi]
    have he : S.card + 1 - T.card = (S.card - T.card) + 1 := by omega
    rw [he, pow_succ]
    ring
  have h2 : ∀ T ∈ S.powerset,
      (-1 : ℝ) ^ ((insert i S).card - (insert i T).card) * v (insert i T) =
      (-1 : ℝ) ^ (S.card - T.card) * v (insert i T) := by
    intro T hT
    have hiT : i ∉ T := fun hit => hi ((mem_powerset.mp hT) hit)
    rw [card_insert_of_notMem hi, card_insert_of_notMem hiT]
    simp
  rw [sum_congr rfl h1, sum_congr rfl h2, ← sum_add_distrib]
  apply sum_congr rfl
  intro T _
  ring

/-- All dividends reconstruct every finite coalition, without a baseline assumption. -/
theorem reconstruction (v : Game α) (S : Finset α) :
    reconstruct (interaction v) S = v S := by
  induction S using Finset.induction_on generalizing v with
  | empty => simp
  | @insert i S hi ih =>
    unfold reconstruct
    rw [sum_powerset_insert hi]
    have h : ∀ T ∈ S.powerset,
        interaction v (insert i T) = interaction (marginal v i) T := by
      intro T hT
      exact interaction_insert v T i (fun hit => hi ((mem_powerset.mp hT) hit))
    rw [sum_congr rfl h]
    change reconstruct (interaction v) S + reconstruct (interaction (marginal v i)) S = _
    rw [ih v, ih (marginal v i)]
    simp [marginal]

/-- The converse Boolean Möbius inversion: transforming subset sums recovers coefficients. -/
theorem interaction_reconstruct (d : Game α) (S : Finset α) :
    interaction (reconstruct d) S = d S := by
  induction S using Finset.induction_on generalizing d with
  | empty => simp
  | @insert i S hi ih =>
    rw [interaction_insert _ _ _ hi]
    have h : interaction (marginal (reconstruct d) i) S =
        interaction (reconstruct (fun T => d (insert i T))) S := by
      apply interaction_congr
      intro T hT
      have hiT : i ∉ T := fun hit => hi (hT hit)
      simp only [marginal, reconstruct, sum_powerset_insert hiT, add_sub_cancel_left]
    rw [h, ih]

/-- Dividends are the unique coefficients that reconstruct all coalitions. -/
theorem reconstruction_unique (v d : Game α)
    (h : ∀ S, reconstruct d S = v S) : d = interaction v := by
  funext S
  rw [← interaction_reconstruct d S]
  apply interaction_congr
  intro T _
  exact h T

theorem interaction_injective : Function.Injective (interaction (α := α)) := by
  intro v w h
  funext S
  have hh := congrArg (fun d => reconstruct d S) h
  simpa only [reconstruction] using hh

end Harsanyi
