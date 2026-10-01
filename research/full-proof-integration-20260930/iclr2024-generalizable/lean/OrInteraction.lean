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

end Harsanyi
