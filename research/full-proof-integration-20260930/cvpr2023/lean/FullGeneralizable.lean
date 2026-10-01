import Harsanyi.Extensions.Attribution
import Harsanyi.Extensions.OrInteraction

namespace FullGeneralizable
open Harsanyi Finset

theorem and_mask_zero {n : ℕ} (v : (Fin n → ℝ) → ℝ) (r x : Fin n → ℝ)
    (T S : Finset (Fin n)) (hST : ¬ S ⊆ T) :
    interaction (conditionalCoordinateGame v r x T) S = 0 := by
  exact and_mask_interaction_zero v r x T S hST

theorem or_duality {n : ℕ} (v : (Fin n → ℝ) → ℝ) (r x : Fin n → ℝ)
    (S : Finset (Fin n)) (hS : S ≠ ∅) :
    orInteraction (fun L => v (maskCoordinates r x L)) univ S =
      -interaction (fun L => v (maskCoordinates r x (univ \ L))) S := by
  exact or_dual _ _ _ hS

theorem exact_and_reconstruction {n : ℕ} (v : (Fin n → ℝ) → ℝ)
    (r x : Fin n → ℝ) (T : Finset (Fin n)) :
    (∑ S ∈ T.powerset, interaction (fun L => v (maskCoordinates r x L)) S) =
      v (maskCoordinates r x T) := by
  exact reconstruction _ _

theorem literal_and_reconstruction {n : ℕ} (vand : (Fin n → ℝ) → ℝ)
    (r x : Fin n → ℝ) (T : Finset (Fin n)) :
    (∑ S ∈ T.powerset, interaction (conditionalCoordinateGame vand r x T) S) =
      vand (maskCoordinates r x T) := by
  rw [← reconstruct, reconstruction]
  simp [conditionalCoordinateGame, maskCoordinates_idempotent]

theorem literal_and_coefficient_eq {n : ℕ} (v : (Fin n → ℝ) → ℝ)
    (r x : Fin n → ℝ) (T S : Finset (Fin n)) (hST : S ⊆ T) :
    interaction (conditionalCoordinateGame v r x T) S =
      interaction (fun L => v (maskCoordinates r x L)) S := by
  apply interaction_congr
  intro L hLS
  have hLT : L ⊆ T := hLS.trans hST
  simp only [conditionalCoordinateGame, maskCoordinates_comp, inter_eq_right.mpr hLT]

theorem literal_or_reconstruction {n : ℕ} (vor : (Fin n → ℝ) → ℝ)
    (r x : Fin n → ℝ) (T : Finset (Fin n)) :
    orInteraction (conditionalCoordinateGame vor r x T) univ ∅ +
      (∑ S ∈ (univ : Finset (Fin n)).powerset.filter (fun S => ¬ Disjoint S T),
        orInteraction (conditionalCoordinateGame vor r x T) univ S) =
      vor (maskCoordinates r x T) := by
  change orReconstruction (conditionalCoordinateGame vor r x T) univ T = _
  rw [or_reconstruction _ _ _ (subset_univ _)]
  simp [conditionalCoordinateGame, maskCoordinates_idempotent]

theorem literal_or_nonempty_sum {n : ℕ} (vor : (Fin n → ℝ) → ℝ)
    (r x : Fin n → ℝ) (T : Finset (Fin n)) :
    (∑ S ∈ (univ : Finset (Fin n)).powerset.filter (fun S => ¬ Disjoint S T),
        orInteraction (conditionalCoordinateGame vor r x T) univ S) =
      vor (maskCoordinates r x T) - vor (maskCoordinates r x ∅) := by
  have h := literal_or_reconstruction vor r x T
  have hbase : orInteraction (conditionalCoordinateGame vor r x T) univ ∅ =
      vor (maskCoordinates r x ∅) := by
    simp [orInteraction, conditionalCoordinateGame, maskCoordinates_comp]
  rw [hbase] at h
  linarith

/-- The original parent Theorem 2, retaining coefficients conditioned on x_T. -/
theorem literal_and_or_reconstruction {n : ℕ} (v vand vor : (Fin n → ℝ) → ℝ)
    (r x : Fin n → ℝ)
    (h : ∀ U, v (maskCoordinates r x U) =
      vand (maskCoordinates r x U) + vor (maskCoordinates r x U)) (T : Finset (Fin n)) :
    v (maskCoordinates r x T) =
      (∑ S ∈ T.powerset, interaction (conditionalCoordinateGame vand r x T) S) +
      (orInteraction (conditionalCoordinateGame vor r x T) univ ∅ +
        ∑ S ∈ (univ : Finset (Fin n)).powerset.filter (fun S => ¬ Disjoint S T),
          orInteraction (conditionalCoordinateGame vor r x T) univ S) := by
  rw [literal_and_reconstruction, literal_or_reconstruction, h T]

/-- Conditional masking for a component defined on mask labels.  This also allows
    arbitrary gamma labels when different labels give the same input vector. -/
noncomputable def labelConditionalGame {n : ℕ} (a : Game (Fin n))
    (T : Finset (Fin n)) : Game (Fin n) := fun L => a (T ∩ L)

theorem label_and_coefficient_eq {n : ℕ} (a : Game (Fin n))
    (T S : Finset (Fin n)) (hST : S ⊆ T) :
    interaction (labelConditionalGame a T) S = interaction a S := by
  apply interaction_congr
  intro L hLS
  have hLT : L ⊆ T := hLS.trans hST
  simp only [labelConditionalGame, inter_eq_right.mpr hLT]

theorem label_and_reconstruction {n : ℕ} (a : Game (Fin n))
    (T : Finset (Fin n)) :
    (∑ S ∈ T.powerset, interaction (labelConditionalGame a T) S) = a T := by
  rw [← reconstruct, reconstruction]
  simp [labelConditionalGame]

theorem label_or_reconstruction {n : ℕ} (b : Game (Fin n))
    (T : Finset (Fin n)) :
    orInteraction (labelConditionalGame b T) univ ∅ +
      (∑ S ∈ (univ : Finset (Fin n)).powerset.filter (fun S => ¬ Disjoint S T),
        orInteraction (labelConditionalGame b T) univ S) = b T := by
  change orReconstruction (labelConditionalGame b T) univ T = _
  rw [or_reconstruction _ _ _ (subset_univ _)]
  simp [labelConditionalGame]

theorem label_or_nonempty_sum {n : ℕ} (b : Game (Fin n))
    (T : Finset (Fin n)) :
    (∑ S ∈ (univ : Finset (Fin n)).powerset.filter (fun S => ¬ Disjoint S T),
        orInteraction (labelConditionalGame b T) univ S) = b T - b ∅ := by
  have h := label_or_reconstruction b T
  have hbase : orInteraction (labelConditionalGame b T) univ ∅ = b ∅ := by
    simp [orInteraction, labelConditionalGame]
  rw [hbase] at h
  linarith

/-- Original Theorem 2 with arbitrary mask-label components a and b.  No
    extension of their gamma values to single-valued input functions is assumed. -/
theorem label_and_or_reconstruction {n : ℕ} (v : (Fin n → ℝ) → ℝ)
    (r x : Fin n → ℝ) (a b : Game (Fin n))
    (h : ∀ U, v (maskCoordinates r x U) = a U + b U) (T : Finset (Fin n)) :
    v (maskCoordinates r x T) =
      (∑ S ∈ T.powerset, interaction (labelConditionalGame a T) S) +
      (orInteraction (labelConditionalGame b T) univ ∅ +
        ∑ S ∈ (univ : Finset (Fin n)).powerset.filter (fun S => ¬ Disjoint S T),
          orInteraction (labelConditionalGame b T) univ S) := by
  rw [label_and_reconstruction, label_or_reconstruction, h T]

noncomputable def bit (a : Bool) : ℝ := if a then 1 else 0

theorem boolean_or_additive (a b : Bool) :
    bit (a || b) = bit a + bit b - bit (a && b) := by
  cases a <;> cases b <;> norm_num [bit]

theorem boolean_decomposition (a b c d e : Bool) :
    bit (a && b && c) + bit (b && c) + bit (c && d) + bit (d || e) =
      bit (a && b && c) + bit (b && c) + bit (c && d) + bit d + bit e - bit (d && e) := by
  rw [boolean_or_additive]
  ring

theorem shapley {n : ℕ} (v : (Fin n → ℝ) → ℝ) (r x : Fin n → ℝ) (i : Fin n) :
    factorialShapley (fun S => v (maskCoordinates r x S)) univ i =
      ∑ S ∈ (univ : Finset (Fin n)).powerset,
        if i ∈ S then interaction (fun L => v (maskCoordinates r x L)) S / S.card else 0 := by
  exact factorialShapley_eq_dividendAllocation _ _ _ (mem_univ _)

theorem mask_count (n : ℕ) :
    ((univ : Finset (Fin n)).powerset).card = 2 ^ n := by simp

end FullGeneralizable
