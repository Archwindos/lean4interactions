import Harsanyi.Core.Properties

/-! Experimental local technical check. Not published, not a replacement for
the original ICLR 2024 Generalizable proof. Source issues remain pending. -/
namespace ReaderV2.Experimental
open Finset Harsanyi

section IndependentOR
variable {α : Type*} [DecidableEq α]

/-- Explicit empty convention; the complement transform is used only for nonempty S. -/
noncomputable def orCoefficient (g : Game α) (N S : Finset α) : ℝ :=
  if S = ∅ then g ∅ else -interaction (fun L => g (N \ L)) S

/-- Independently defined project OR reconstruction; not the paper's x_T notation. -/
noncomputable def orReconstruct (g : Game α) (N T : Finset α) : ℝ :=
  orCoefficient g N ∅ +
    ∑ S ∈ N.powerset.filter (fun S => ¬ Disjoint S T), orCoefficient g N S

/-- Intersecting coefficients form the difference of two subset sums. -/
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

/-- OR matching on a fixed finite universe. This has its own proof and audit. -/
theorem independent_or_matching (g : Game α) (N T : Finset α) (hTN : T ⊆ N) :
    orReconstruct g N T = g T := by
  let f : Game α := fun L => -g (N \ L)
  have hneg (S : Finset α) :
      interaction f S = -interaction (fun L => g (N \ L)) S := by
    simp [f, interaction, mul_neg, sum_neg_distrib]
  have hcoeff : ∀ S ∈ N.powerset.filter (fun S => ¬ Disjoint S T),
      orCoefficient g N S = interaction f S := by
    intro S hS
    have hne : S ≠ ∅ := by
      intro he
      subst S
      simpa using (mem_filter.mp hS).2
    rw [orCoefficient, if_neg hne, hneg]
  unfold orReconstruct
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
  simp [f, orCoefficient, hcomp]

end IndependentOR
end ReaderV2.Experimental

#print axioms ReaderV2.Experimental.orCoefficient
#print axioms ReaderV2.Experimental.orReconstruct
#print axioms ReaderV2.Experimental.activated_subset_sum
#print axioms ReaderV2.Experimental.independent_or_matching
