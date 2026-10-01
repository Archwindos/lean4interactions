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
