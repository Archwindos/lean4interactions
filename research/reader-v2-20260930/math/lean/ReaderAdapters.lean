import Harsanyi.Core.Properties

/-! Independent reader adapters. No source-paper proof is overwritten.
`Fin n` fixes the finite universe, so `∀ S` means exactly all masks of that universe.
No assertion of full-paper formalization is made. -/
namespace ReaderV2
open Finset Harsanyi

noncomputable def maskedGame {X : Type*} {n : ℕ}
    (v : X → ℝ) (mask : Finset (Fin n) → X) : Game (Fin n) :=
  fun S => v (mask S)

theorem masked_empty {X : Type*} {n : ℕ}
    (v : X → ℝ) (mask : Finset (Fin n) → X) :
    interaction (maskedGame v mask) ∅ = v (mask ∅) := by
  exact interaction_empty (maskedGame v mask)

theorem cvpr_reconstruction {X : Type*} {n : ℕ}
    (v : X → ℝ) (mask : Finset (Fin n) → X) (S : Finset (Fin n)) :
    (∑ T ∈ S.powerset, interaction (maskedGame v mask) T) = v (mask S) := by
  exact reconstruction (maskedGame v mask) S

theorem cvpr_unique_coefficients {X : Type*} {n : ℕ}
    (v : X → ℝ) (mask : Finset (Fin n) → X) (d : Game (Fin n))
    (faithful : ∀ S : Finset (Fin n), (∑ T ∈ S.powerset, d T) = v (mask S)) :
    d = interaction (maskedGame v mask) := by
  exact reconstruction_unique (maskedGame v mask) d faithful

theorem sparse_centered_reconstruction {X : Type*} {n : ℕ}
    (v : X → ℝ) (mask : Finset (Fin n) → X) (S : Finset (Fin n)) :
    v (mask S) =
      (∑ T ∈ S.powerset, interaction (centered (maskedGame v mask)) T) +
      v (mask ∅) := by
  change v (mask S) = reconstruct (interaction (centered (maskedGame v mask))) S + _
  rw [reconstruction]
  simp [centered, maskedGame]

theorem sparse_empty {X : Type*} {n : ℕ}
    (v : X → ℝ) (mask : Finset (Fin n) → X) :
    interaction (centered (maskedGame v mask)) ∅ = 0 := by
  simp

theorem baseline_nonempty_agreement {X : Type*} {n : ℕ}
    (v : X → ℝ) (mask : Finset (Fin n) → X) (S : Finset (Fin n))
    (hS : S.Nonempty) :
    interaction (centered (maskedGame v mask)) S = interaction (maskedGame v mask) S := by
  exact interaction_centered_nonempty (maskedGame v mask) S hS

theorem baseline_explicit_reconstruction {X : Type*} {n : ℕ}
    (v : X → ℝ) (mask : Finset (Fin n) → X) (S : Finset (Fin n)) :
    v (mask S) = v (mask ∅) +
      ∑ T ∈ S.powerset.erase ∅, interaction (maskedGame v mask) T := by
  have h := reconstruction (maskedGame v mask) S
  unfold reconstruct at h
  rw [← sum_erase_add _ _ (mem_powerset.mpr (empty_subset S)), interaction_empty] at h
  change _ + v (mask ∅) = v (mask S) at h
  linarith

theorem generalizable_and_subresult {X : Type*} {n : ℕ}
    (vAnd : X → ℝ) (mask : Finset (Fin n) → X) (T : Finset (Fin n)) :
    vAnd (mask T) = ∑ S ∈ T.powerset, interaction (maskedGame vAnd mask) S := by
  exact (reconstruction (maskedGame vAnd mask) T).symm

end ReaderV2
