import Harsanyi.Core.Properties

namespace Harsanyi
open Finset
variable {α : Type*} [DecidableEq α]

/-- Dividend allocation: each nonempty dividend is split equally among its members.
This is the Harsanyi dividend expression for the Shapley value; equivalence to the
factorial-weighted marginal formula is a separate future theorem. -/
noncomputable def dividendAllocation (v : Game α) (N : Finset α) (i : α) : ℝ :=
  ∑ S ∈ N.powerset, if i ∈ S then interaction v S / S.card else 0

theorem dividendAllocation_add (v w : Game α) (N : Finset α) (i : α) :
    dividendAllocation (fun S => v S + w S) N i =
      dividendAllocation v N i + dividendAllocation w N i := by
  unfold dividendAllocation
  rw [← sum_add_distrib]
  apply sum_congr rfl
  intro S _
  split_ifs <;> simp [interaction_add, add_div]

/-- Summing a coalition's equal shares yields exactly its nonempty dividend. -/
theorem sum_dividend_shares (x : ℝ) (N S : Finset α) (hSN : S ⊆ N) :
    (∑ i ∈ N, if i ∈ S then x / S.card else 0) = if S = ∅ then 0 else x := by
  classical
  have h : (∑ i ∈ N, if i ∈ S then x / S.card else 0) =
      ∑ i ∈ S, x / S.card := by
    calc
      _ = ∑ i ∈ S, if i ∈ S then x / S.card else 0 := by
        symm
        apply sum_subset hSN
        intro i _ hi
        simp [hi]
      _ = _ := by apply sum_congr rfl; intro i hi; simp [hi]
  rw [h]
  by_cases hs : S = ∅
  · simp [hs]
  · have hc : (S.card : ℝ) ≠ 0 := by
      exact_mod_cast (card_ne_zero.mpr (nonempty_iff_ne_empty.mpr hs))
    simp [hs, nsmul_eq_mul]
    field_simp

/-- Efficiency for a finite variable set, with the baseline term kept explicitly. -/
theorem dividendAllocation_efficiency (v : Game α) (N : Finset α) :
    (∑ i ∈ N, dividendAllocation v N i) = v N - v ∅ := by
  classical
  unfold dividendAllocation
  rw [sum_comm]
  have h : (∑ S ∈ N.powerset, ∑ i ∈ N,
      if i ∈ S then interaction v S / S.card else 0) =
      ∑ S ∈ N.powerset, if S = ∅ then 0 else interaction v S := by
    apply sum_congr rfl
    intro S hS
    exact sum_dividend_shares _ N S (mem_powerset.mp hS)
  rw [h]
  have hsum : (∑ S ∈ N.powerset, if S = ∅ then 0 else interaction v S) =
      (∑ S ∈ N.powerset, interaction v S) - interaction v ∅ := by
    have hf : ∀ S : Finset α, (if S = ∅ then 0 else interaction v S) =
        interaction v S - if S = ∅ then interaction v ∅ else 0 := by
      intro S
      by_cases hS : S = ∅ <;> simp [hS]
    simp_rw [hf, sum_sub_distrib]
    simp [Finset.sum_ite_eq', empty_mem_powerset]
  rw [hsum, ← reconstruct, reconstruction, interaction_empty]

theorem dividendAllocation_centered (v : Game α) (N : Finset α) (i : α) :
    dividendAllocation (centered v) N i = dividendAllocation v N i := by
  unfold dividendAllocation
  apply sum_congr rfl
  intro S _
  by_cases hi : i ∈ S
  · simp [hi, interaction_centered_nonempty v S ⟨i, hi⟩]
  · simp [hi]

/-- A pure interaction divides its coefficient equally among its members. -/
theorem dividendAllocation_unanimity (A N : Finset α) (c : ℝ) (i : α) (hA : A ⊆ N) :
    dividendAllocation (unanimity A c) N i = if i ∈ A then c / A.card else 0 := by
  classical
  unfold dividendAllocation
  have h : ∀ S ∈ N.powerset,
      (if i ∈ S then interaction (unanimity A c) S / S.card else 0) =
      if S = A then (if i ∈ A then c / A.card else 0) else 0 := by
    intro S _
    by_cases hS : S = A
    · simp [hS, interaction_unanimity]
    · simp [hS, interaction_unanimity]
  rw [sum_congr rfl h]
  simp [Finset.sum_ite_eq', mem_powerset, hA]

end Harsanyi
