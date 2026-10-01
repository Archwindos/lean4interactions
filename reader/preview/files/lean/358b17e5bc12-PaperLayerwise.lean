import Harsanyi.Extensions.LayerwiseKnowledge
namespace PaperLayerwise
open Finset Harsanyi
variable {α : Type*} [DecidableEq α]
/-- Actual coordinate masks instantiate the fixed-game matching identity. -/
theorem actual_matching (v : (α → ℝ) → ℝ) (r x : α → ℝ) (γ : Game α)
    (N T : Finset α) (hTN : T ⊆ N)
    (hγ : γ ∅ = v (maskCoordinates r x ∅) / 2) :
    v (maskCoordinates r x T) =
      (∑ S ∈ T.powerset, interaction (Layerwise.andComponent (fun L => v (maskCoordinates r x L)) γ) S) +
      ∑ S ∈ N.powerset.filter (fun S => ¬ Disjoint S T),
        orInteraction (Layerwise.orComponent (fun L => v (maskCoordinates r x L)) γ) N S :=
  Layerwise.and_or_matching (fun L => v (maskCoordinates r x L)) γ N T hTN hγ
/-- Repeated coordinate masks are intersections; no conditional identity is assumed. -/
theorem repeated_mask (r x : α → ℝ) (T L : Finset α) :
    maskCoordinates r (maskCoordinates r x T) L = maskCoordinates r x (T ∩ L) := by
  funext i
  by_cases hiT : i ∈ T <;> by_cases hiL : i ∈ L <;> simp [maskCoordinates,hiT,hiL]
/-- The literal remasked source interpretation is also proved from the split. -/
theorem actual_remasked_matching (v : (α → ℝ) → ℝ) (r x : α → ℝ) (γ : Game α)
    (N T : Finset α) (hTN : T ⊆ N)
    (hγ : γ ∅ = v (maskCoordinates r x ∅) / 2) :
    v (maskCoordinates r x T) =
      (∑ S ∈ T.powerset, interaction (Layerwise.andComponent
        (fun L => v (maskCoordinates r (maskCoordinates r x T) L)) (Layerwise.restricted γ T)) S) +
      ∑ S ∈ N.powerset.filter (fun S => ¬ Disjoint S T),
        orInteraction (Layerwise.orComponent
        (fun L => v (maskCoordinates r (maskCoordinates r x T) L)) (Layerwise.restricted γ T)) N S := by
  simp_rw [repeated_mask]
  exact Layerwise.conditional_and_or_matching (fun L => v (maskCoordinates r x L)) γ N T hTN hγ
/-- Classical factorial Shapley of the actual probe/model mask game. -/
theorem actual_shapley (v : (α → ℝ) → ℝ) (r x : α → ℝ) (γ : Game α)
    (N : Finset α) (i : α) (hi : i ∈ N) :
    factorialShapley (fun L => v (maskCoordinates r x L)) N i =
      ∑ S ∈ N.powerset, if i ∈ S then
        (interaction (Layerwise.andComponent (fun L => v (maskCoordinates r x L)) γ) S +
          orInteraction (Layerwise.orComponent (fun L => v (maskCoordinates r x L)) γ) N S) / S.card else 0 :=
  Layerwise.shapley_and_or (fun L => v (maskCoordinates r x L)) γ N i hi
end PaperLayerwise
