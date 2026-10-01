import Lean.Util.CollectAxioms
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

open Lean Elab Command Meta
set_option pp.universes true
set_option pp.fullNames true
set_option pp.piBinderTypes true
run_cmd liftTermElabM do
  for name in #[`Harsanyi.Layerwise.andComponent, `Harsanyi.Layerwise.orComponent, `Harsanyi.Layerwise.component_sum, `Harsanyi.Layerwise.component_empty, `Harsanyi.Layerwise.and_or_matching, `Harsanyi.Layerwise.restricted, `Harsanyi.Layerwise.conditional_and_or_matching, `Harsanyi.Layerwise.shapley_and_or, `Harsanyi.Layerwise.restricted_and, `Harsanyi.Layerwise.complementary_order_count, `Harsanyi.Layerwise.singleton_activation, `Harsanyi.Layerwise.singleton_merge, `Harsanyi.Layerwise.orUnanimity_singleton, `Harsanyi.Layerwise.shared, `Harsanyi.Layerwise.scalar_strength_decomposition, `Harsanyi.Layerwise.thresholded_strength_counterexample, `Harsanyi.Layerwise.duplicated_baseline_counterexample, `Harsanyi.Layerwise.strengthEffect, `Harsanyi.Layerwise.strengthUniverse, `Harsanyi.Layerwise.strengthGame, `Harsanyi.Layerwise.strengthGame_dividends, `Harsanyi.Layerwise.significantStrength, `Harsanyi.Layerwise.allStrength, `Harsanyi.Layerwise.overlapStrength, `Harsanyi.Layerwise.forgetStrength, `Harsanyi.Layerwise.strength_supports, `Harsanyi.Layerwise.strength_full_outputs, `Harsanyi.Layerwise.normalized_thresholded_counterexample, `PaperLayerwise.actual_matching, `PaperLayerwise.repeated_mask, `PaperLayerwise.actual_remasked_matching, `PaperLayerwise.actual_shapley, `Harsanyi.reconstruction] do
    let info ← getConstInfo name
    let signature ← ppExpr info.type
    let axioms ← Lean.collectAxioms name
    let deps := info.type.getUsedConstants ++ (info.value?.map Expr.getUsedConstants).getD #[]
    let kind := match info with | .thmInfo _ => "theorem" | .inductInfo _ => "inductive" | _ => "definition"
    liftM <| IO.println ("NETWORK_API:" ++ (Json.mkObj [
      ("name", toJson name.toString), ("signature", toJson signature.pretty),
      ("kind", toJson kind), ("axioms", toJson (axioms.map Name.toString)),
      ("dependencies", toJson (deps.map Name.toString))]).compress)
