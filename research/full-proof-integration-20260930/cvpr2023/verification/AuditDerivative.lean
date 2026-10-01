import Lean.Util.CollectAxioms
import Harsanyi.Extensions.DerivativeCutoff

namespace FullSparseDerivative
open Harsanyi

/-- The original full-space mixed-derivative assumption implies the centered interaction
cutoff, with arbitrary actual coordinate baseline and sample. `hbeta` combines existence
and zero of each requested classical mixed derivative; C1 alone does not supply them. -/
theorem assumption1beta_implies1alpha {n : ℕ} (v : (Fin n → ℝ) → ℝ) (M : ℕ)
    (_hC1 : ContDiff ℝ 1 v) (hbeta : ClassicalMixedDerivativeCutoff v M) (r x : Fin n → ℝ)
    (S : Finset (Fin n)) (hS : M + 1 ≤ S.card) :
    interaction (fun U => v (maskCoordinates r x U) - v (maskCoordinates r x ∅)) S = 0 := by
  exact centered_interaction_zero_of_classicalMixedDerivativeCutoff v M hbeta r x S (by omega)

end FullSparseDerivative

open Lean Elab Command Meta
set_option pp.universes true
set_option pp.fullNames true
set_option pp.piBinderTypes true
run_cmd liftTermElabM do
  for name in #[`Harsanyi.linePartial, `Harsanyi.HasLineDerivatives, `Harsanyi.rectDifference, `Harsanyi.orderedPartial, `Harsanyi.OrderedPartialRegular, `Harsanyi.deriv_line_eq, `Harsanyi.hasLineDerivatives_translate, `Harsanyi.linePartial_translate, `Harsanyi.linePartial_sub, `Harsanyi.hasLineDerivatives_rectDifference, `Harsanyi.linePartial_rectDifference, `Harsanyi.rectDifference_zero_of_orderedPartial_zero, `Harsanyi.coordinateDirection, `Harsanyi.coordinateCurve_eq_update, `Harsanyi.linePartial_coordinate_eq, `Harsanyi.coordinateMoves, `Harsanyi.incrementCoordinates, `Harsanyi.incrementGame, `Harsanyi.incrementCoordinates_insert, `Harsanyi.rectDifference_coordinate_eq_interaction, `Harsanyi.incrementCoordinates_baseline, `Harsanyi.orderedPartial_coordinate_amplitudes, `Harsanyi.orderedPartialRegular_coordinate_amplitudes, `Harsanyi.orderedCoordinatePartial, `Harsanyi.OrderedCoordinateRegular, `Harsanyi.HasClassicalMixedDerivatives, `Harsanyi.MixedDerivativeCutoff, `Harsanyi.ClassicalMixedDerivativeCutoff, `Harsanyi.coordinate_multiIndex_total_order, `Harsanyi.coordinate_multiIndex_finset, `Harsanyi.interaction_zero_of_orderedCoordinatePartial_zero, `Harsanyi.interaction_zero_of_mixedDerivativeCutoff, `Harsanyi.interaction_zero_of_classicalMixedDerivativeCutoff, `Harsanyi.centered_interaction_zero_of_classicalMixedDerivativeCutoff, `Harsanyi.centered_interaction_zero_of_mixedDerivativeCutoff, `FullSparseDerivative.assumption1beta_implies1alpha] do
    let info ← getConstInfo name
    let signature ← ppExpr info.type
    let axioms ← Lean.collectAxioms name
    let deps := info.type.getUsedConstants ++ (info.value?.map Expr.getUsedConstants).getD #[]
    let kind := match info with | .thmInfo _ => "theorem" | _ => "definition"
    liftM <| IO.println ("DERIVATIVE_API:" ++ (Json.mkObj [
      ("name", toJson name.toString), ("signature", toJson signature.pretty),
      ("kind", toJson kind), ("axioms", toJson (axioms.map Name.toString)),
      ("dependencies", toJson (deps.map Name.toString))]).compress)
