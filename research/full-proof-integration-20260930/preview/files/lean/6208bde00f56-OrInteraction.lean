import Harsanyi.Core.Properties

/-! OR interactions with the paper's separate empty-coalition convention.
The proof avoids the erroneous inner-zero assertion in Appendix C(2).
No theorem or assumption from the paper is changed. -/
namespace Harsanyi
open Finset
variable {α : Type*} [DecidableEq α]

noncomputable def orInteraction (g : Game α) (N S : Finset α) : ℝ :=
  if S = ∅ then g ∅ else -interaction (fun L => g (N \ L)) S

noncomputable def orReconstruction (g : Game α) (N T : Finset α) : ℝ :=
  orInteraction g N ∅ +
    ∑ S ∈ N.powerset.filter (fun S => ¬ Disjoint S T), orInteraction g N S

/-- Intersecting coalitions are the difference of two subset families, including T=∅. -/
theorem activated_subset_sum (d : Game α) (N T : Finset α) :
    (∑ S ∈ N.powerset.filter (fun S => ¬ Disjoint S T), d S) =
      reconstruct d N - reconstruct d (N \ T) := by
  have hsets : N.powerset.filter (fun S => ¬ Disjoint S T) =
      N.powerset \ (N \ T).powerset := by
    ext S
    simp only [mem_filter, mem_powerset, mem_sdiff, subset_sdiff]
    tauto
  rw [hsets]
  exact sum_sdiff_eq_sub (powerset_mono.mpr (sdiff_subset : N \ T ⊆ N))

/-- Exact OR matching on any fixed finite universe. -/
theorem or_reconstruction (g : Game α) (N T : Finset α) (hTN : T ⊆ N) :
    orReconstruction g N T = g T := by
  let f : Game α := fun L => -g (N \ L)
  have hneg (S : Finset α) :
      interaction f S = -interaction (fun L => g (N \ L)) S := by
    simp [f, interaction, mul_neg, sum_neg_distrib]
  have hcoeff : ∀ S ∈ N.powerset.filter (fun S => ¬ Disjoint S T),
      orInteraction g N S = interaction f S := by
    intro S hS
    have hne : S ≠ ∅ := by
      intro he
      subst S
      simpa using (mem_filter.mp hS).2
    rw [orInteraction, if_neg hne, hneg]
  unfold orReconstruction
  rw [sum_congr rfl hcoeff, activated_subset_sum, reconstruction, reconstruction]
  have hcomp : N \ (N \ T) = T := by
    ext i
    simp only [mem_sdiff]
    constructor
    · intro h
      by_contra hiT
      exact h.2 ⟨h.1, hiT⟩
    · intro hiT
      exact ⟨hTN hiT, fun h => h.2 hiT⟩
  simp [f, orInteraction, hcomp]

/-- A literal change of masked/unmasked states is a negative AND transform for nonempty S. -/
theorem or_dual (g : Game α) (N S : Finset α) (hS : S ≠ ∅) :
    orInteraction g N S = -interaction (fun L => g (N \ L)) S := by
  simp [orInteraction, hS]

/-- Coordinate masking with one fixed baseline, including a masked input as the base sample. -/
def maskCoordinates {β : Type*} (r x : α → β) (S : Finset α) : α → β :=
  fun i => if i ∈ S then x i else r i

/-- Repeated masking retains the intersection; the baseline is not recomputed. -/
theorem maskCoordinates_comp {β : Type*} (r x : α → β) (T L : Finset α) :
    maskCoordinates r (maskCoordinates r x T) L = maskCoordinates r x (T ∩ L) := by
  funext i
  by_cases hiT : i ∈ T <;> by_cases hiL : i ∈ L <;>
    simp [maskCoordinates, hiT, hiL]

theorem maskCoordinates_idempotent {β : Type*} (r x : α → β) (T : Finset α) :
    maskCoordinates r (maskCoordinates r x T) T = maskCoordinates r x T := by
  rw [maskCoordinates_comp, inter_self]

theorem maskCoordinates_insert_absent {β : Type*} (r x : α → β)
    (T U : Finset α) (i : α) (hi : i ∉ T) :
    maskCoordinates r (maskCoordinates r x T) (insert i U) =
      maskCoordinates r (maskCoordinates r x T) U := by
  funext j
  by_cases hj : j = i
  · subst j
    simp [maskCoordinates, hi]
  · simp [maskCoordinates, hj]

/-- The literal conditional game appearing in I(S | x_T). -/
noncomputable def conditionalCoordinateGame {β : Type*} (v : (α → β) → ℝ)
    (r x : α → β) (T : Finset α) : Game α :=
  fun L => v (maskCoordinates r (maskCoordinates r x T) L)

/-- If a coalition contains an already masked variable, its AND interaction is zero. -/
theorem and_mask_interaction_zero {β : Type*} (v : (α → β) → ℝ)
    (r x : α → β) (T S : Finset α) (hST : ¬ S ⊆ T) :
    interaction (conditionalCoordinateGame v r x T) S = 0 := by
  obtain ⟨i, hiS, hiT⟩ := Finset.not_subset.mp hST
  conv_lhs => rw [← insert_erase hiS]
  apply interaction_dummy _ _ _ (notMem_erase i S)
  intro U _
  simp only [conditionalCoordinateGame, maskCoordinates_insert_absent r x T U i hiT]

/-- Mask composition in the complemented argument used by the literal OR proof. -/
theorem maskCoordinates_complement {β : Type*} (r x : α → β)
    (N T L : Finset α) (hTN : T ⊆ N) :
    maskCoordinates r (maskCoordinates r x T) (N \ L) = maskCoordinates r x (T \ L) := by
  rw [maskCoordinates_comp]
  have he : T ∩ (N \ L) = T \ L := by
    ext i
    simp only [mem_inter, mem_sdiff]
    exact ⟨fun h => ⟨h.1, h.2.2⟩, fun h => ⟨h.1, hTN h.1, h.2⟩⟩
  rw [he]

/-- Pure OR response on a nonempty target set. -/
noncomputable def orUnanimity (A : Finset α) (c : ℝ) : Game α :=
  fun S => if Disjoint A S then 0 else c

theorem orInteraction_unanimity (A N S : Finset α) (c : ℝ)
    (hAN : A ⊆ N) (hA : A.Nonempty) :
    orInteraction (orUnanimity A c) N S = if S = A then c else 0 := by
  have hgame : (fun L => orUnanimity A c (N \ L)) =
      (fun L => c - unanimity A c L) := by
    funext L
    have hiff : Disjoint A (N \ L) ↔ A ⊆ L := by
      constructor
      · intro hd i hiA
        by_contra hiL
        exact Finset.disjoint_left.mp hd hiA (mem_sdiff.mpr ⟨hAN hiA, hiL⟩)
      · intro hAL
        exact Finset.disjoint_left.mpr (fun i hiA hiR => (mem_sdiff.mp hiR).2 (hAL hiA))
    by_cases hAL : A ⊆ L <;> simp [orUnanimity, unanimity, hiff, hAL]
  by_cases hS : S = ∅
  · subst S
    have hEA : (∅ : Finset α) ≠ A := Ne.symm hA.ne_empty
    simp [orInteraction, orUnanimity, hEA]
  · rw [orInteraction, if_neg hS, hgame, interaction_sub, interaction_const, if_neg hS,
      interaction_unanimity]
    split_ifs <;> ring

end Harsanyi
