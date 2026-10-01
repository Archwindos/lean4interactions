import Harsanyi.Core.Mobius

namespace Harsanyi
open Finset
variable {α : Type*} [DecidableEq α]

theorem interaction_add (v w : Game α) (S : Finset α) :
    interaction (fun T => v T + w T) S = interaction v S + interaction w S := by
  simp [interaction, mul_add, sum_add_distrib]

theorem interaction_sub (v w : Game α) (S : Finset α) :
    interaction (fun T => v T - w T) S = interaction v S - interaction w S := by
  simp [interaction, mul_sub, sum_sub_distrib]

theorem interaction_smul (a : ℝ) (v : Game α) (S : Finset α) :
    interaction (fun T => a * v T) S = a * interaction v S := by
  simp [interaction, ← mul_sum, mul_left_comm]

@[simp] theorem interaction_zero (S : Finset α) :
    interaction (fun _ => 0) S = 0 := by simp [interaction]

/-- A constant game has only an empty-coalition dividend. -/
theorem interaction_const (c : ℝ) (S : Finset α) :
    interaction (fun _ => c) S = if S = ∅ then c else 0 := by
  cases S using Finset.induction_on with
  | empty => simp
  | @insert i S hi =>
    rw [interaction_insert _ _ _ hi]
    simp [marginal, interaction]

/-- Centering removes the empty dividend and preserves every nonempty dividend. -/
theorem interaction_centered (v : Game α) (S : Finset α) :
    interaction (centered v) S = interaction v S - if S = ∅ then v ∅ else 0 := by
  unfold centered
  rw [interaction_sub, interaction_const]

theorem interaction_centered_nonempty (v : Game α) (S : Finset α) (hS : S.Nonempty) :
    interaction (centered v) S = interaction v S := by
  rw [interaction_centered, if_neg hS.ne_empty, sub_zero]

/-- Recursive form obtained by isolating the top coalition in reconstruction. -/
theorem interaction_recursive (v : Game α) (S : Finset α) :
    interaction v S = v S - ∑ T ∈ S.powerset.erase S, interaction v T := by
  have h := reconstruction v S
  unfold reconstruct at h
  rw [← sum_erase_add _ _ (mem_powerset.mpr (Subset.refl S))] at h
  linarith

/-- Unanimity/pure AND interaction on `A`; the empty `A` is explicitly allowed. -/
noncomputable def unanimity (A : Finset α) (c : ℝ) : Game α :=
  fun S => if A ⊆ S then c else 0

/-- A single dividend reconstructs exactly a unanimity function. -/
theorem reconstruct_single (A : Finset α) (c : ℝ) (S : Finset α) :
    reconstruct (fun T => if T = A then c else 0) S = unanimity A c S := by
  classical
  simp [reconstruct, unanimity, Finset.sum_ite_eq', mem_powerset]

theorem interaction_unanimity (A : Finset α) (c : ℝ) (S : Finset α) :
    interaction (unanimity A c) S = if S = A then c else 0 := by
  have h : unanimity A c = reconstruct (fun T => if T = A then c else 0) := by
    funext T
    exact (reconstruct_single A c T).symm
  rw [h, interaction_reconstruct]

/-- If inserting `i` changes no subcoalition of `S`, its interaction with `S` vanishes. -/
theorem interaction_dummy (v : Game α) (S : Finset α) (i : α) (hi : i ∉ S)
    (h : ∀ T ⊆ S, v (insert i T) = v T) : interaction v (insert i S) = 0 := by
  rw [interaction_insert v S i hi, ← interaction_zero S]
  apply interaction_congr
  intro T hT
  simp [marginal, h T hT]

/-- Relabeling variables by a bijection preserves the interaction. -/
theorem interaction_relabel {β : Type*} [DecidableEq β] (e : α ≃ β)
    (v : Game α) (S : Finset α) :
    interaction (fun U => v (U.map e.symm.toEmbedding)) (S.map e.toEmbedding) =
      interaction v S := by
  unfold interaction
  refine Finset.sum_bij (fun U _ => U.map e.symm.toEmbedding) ?_ ?_ ?_ ?_
  · intro U hU
    apply mem_powerset.mpr
    have h : U.map e.symm.toEmbedding ⊆ (S.map e.toEmbedding).map e.symm.toEmbedding :=
      Finset.map_subset_map.mpr (mem_powerset.mp hU)
    simpa [Finset.map_map] using h
  · intro U _ V _ h
    exact Finset.map_injective e.symm.toEmbedding h
  · intro T hT
    refine ⟨T.map e.toEmbedding, mem_powerset.mpr ?_, ?_⟩
    · exact (Finset.map_subset_map.mpr (mem_powerset.mp hT))
    · simp [Finset.map_map]
  · intro U _
    simp

end Harsanyi
