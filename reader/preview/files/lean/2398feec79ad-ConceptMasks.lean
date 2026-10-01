import Harsanyi.Core.Properties

namespace Harsanyi.ConceptMasks
open Finset
variable {α : Type*} [DecidableEq α]

noncomputable def maskedGame (g : Game α) (T : Finset α) : Game α := fun U => g (U ∩ T)

theorem masked_dividend (g : Game α) (T S : Finset α) :
    interaction (maskedGame g T) S = if S ⊆ T then interaction g S else 0 := by
  classical
  by_cases h : S ⊆ T
  · rw [if_pos h]
    apply interaction_congr
    intro U hUS
    simp [maskedGame, inter_eq_left.mpr (hUS.trans h)]
  · rw [if_neg h]
    obtain ⟨i, hiS, hiT⟩ := Finset.not_subset.mp h
    have hS : insert i (S.erase i) = S := insert_erase hiS
    rw [← hS]
    apply interaction_dummy _ _ _ (notMem_erase _ _)
    intro U _
    have hf : insert i U ∩ T = U ∩ T := by
      ext j
      by_cases hj : j = i
      · simp [hj, hiT]
      · simp [hj]
    simp only [maskedGame, hf]

noncomputable def normalizedMaskedTrigger (g : Game α) (T S : Finset α) : ℝ :=
  interaction (maskedGame g T) S / interaction g S

theorem binary_trigger (g : Game α) (T S : Finset α) (h : interaction g S ≠ 0) :
    normalizedMaskedTrigger g T S = if S ⊆ T then 1 else 0 := by
  rw [normalizedMaskedTrigger, masked_dividend]
  split_ifs <;> simp [h]

/-- A fixed nonzero reference family normalizes actual current dividends exactly. -/
theorem linear_representation (h : Game α) (U : Game α) (T : Finset α)
    (hu : ∀ S ⊆ T, U S ≠ 0) :
    h T = ∑ S ∈ T.powerset, U S * (interaction h S / U S) := by
  rw [← reconstruction h T]
  apply sum_congr rfl
  intro S hST
  have hS := hu S (mem_powerset.mp hST)
  field_simp

end Harsanyi.ConceptMasks
