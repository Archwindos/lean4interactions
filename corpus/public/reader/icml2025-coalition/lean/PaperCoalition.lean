import Harsanyi.Extensions.CoalitionAttribution
namespace PaperCoalition
open Finset Harsanyi Harsanyi.Coalition
variable {n : ℕ}
noncomputable def maskedGame (v : (Fin n → ℝ) → ℝ) (r x : Fin n → ℝ) : Game (Fin n) :=
  fun S => v (maskCoordinates r x S)
noncomputable def andComponent (g γ : Game (Fin n)) : Game (Fin n) := fun S => g S / 2 + γ S
noncomputable def orComponent (g γ : Game (Fin n)) : Game (Fin n) := fun S => g S / 2 - γ S
 theorem component_sum (g γ : Game (Fin n)) :
    (fun S => andComponent g γ S + orComponent g γ S) = g := by
  funext S
  simp only [andComponent, orComponent]
  ring
noncomputable def effect (g γ : Game (Fin n)) : Game (Fin n) :=
  totalEffect (andComponent g γ) (orComponent g γ) univ

 theorem theorem32 (v : (Fin n → ℝ) → ℝ) (r x : Fin n → ℝ)
    (γ : Game (Fin n)) (i : Fin n) :
    factorialShapley (maskedGame v r x) univ i =
      shares (effect (maskedGame v r x) γ) univ i := by
  simpa only [component_sum, effect] using
    shapley_and_or (andComponent (maskedGame v r x) γ)
      (orComponent (maskedGame v r x) γ) univ i (mem_univ i)

 theorem theorem33 (v : (Fin n → ℝ) → ℝ) (r x : Fin n → ℝ)
    (γ : Game (Fin n)) (i : Fin n) :
    banzhaf (maskedGame v r x) univ i =
      ∑ U ∈ (univ.erase i).powerset, (1 / (2 : ℝ) ^ U.card) *
        effect (maskedGame v r x) γ (insert i U) := by
  simpa only [component_sum, effect] using
    banzhaf_and_or (andComponent (maskedGame v r x) γ)
      (orComponent (maskedGame v r x) γ) univ i (mem_univ i)

/-- Source all-subsets quantifier has an undefined empty attribution.
This adapter explicitly records the nonempty original quotient domain. -/
 theorem theorem34_nonempty (v : (Fin n → ℝ) → ℝ) (r x : Fin n → ℝ)
    (γ : Game (Fin n)) (S : Finset (Fin n)) (_hS : S.Nonempty) :
    (∑ i ∈ S, factorialShapley (maskedGame v r x) univ i) =
      attribution (effect (maskedGame v r x) γ) univ S +
        conflict (effect (maskedGame v r x) γ) univ S := by
  simpa only [component_sum, effect] using
    paper_conflict (andComponent (maskedGame v r x) γ)
      (orComponent (maskedGame v r x) γ) univ S (subset_univ S)

 theorem theorem36 (v : (Fin n → ℝ) → ℝ) (r x : Fin n → ℝ)
    (γ : Game (Fin n)) (S : Finset (Fin n)) (i : Fin n) (hi : i ∈ S) :
    factorialShapley (maskedGame v r x) univ i =
      attribution (effect (maskedGame v r x) γ) univ S / S.card +
        individualConflict (effect (maskedGame v r x) γ) univ S i := by
  simpa only [component_sum, effect] using
    paper_individual (andComponent (maskedGame v r x) γ)
      (orComponent (maskedGame v r x) γ) univ S (subset_univ S) i hi

 theorem corollary37 (v : (Fin n → ℝ) → ℝ) (r x : Fin n → ℝ)
    (γ : Game (Fin n)) (i : Fin n) :
    attribution (effect (maskedGame v r x) γ) univ {i} =
      factorialShapley (maskedGame v r x) univ i := by
  simpa only [component_sum, effect] using
    paper_singleton (andComponent (maskedGame v r x) γ)
      (orComponent (maskedGame v r x) γ) univ i (mem_univ i)

 theorem corollary38_nonempty (v : (Fin n → ℝ) → ℝ) (r x : Fin n → ℝ)
    (γ : Game (Fin n)) (S : Finset (Fin n)) (_hS : S.Nonempty) :
    maskedGame v r x univ - maskedGame v r x ∅ =
      attribution (effect (maskedGame v r x) γ) univ S +
        (∑ i ∈ univ \ S, factorialShapley (maskedGame v r x) univ i) +
        conflict (effect (maskedGame v r x) γ) univ S := by
  have h := paper_efficiency (andComponent (maskedGame v r x) γ)
      (orComponent (maskedGame v r x) γ) univ S (subset_univ S)
  have he (U : Finset (Fin n)) : andComponent (maskedGame v r x) γ U +
      orComponent (maskedGame v r x) γ U = maskedGame v r x U := by
    dsimp [andComponent, orComponent]; ring
  simpa only [component_sum, effect, he] using h
end PaperCoalition
