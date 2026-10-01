import Harsanyi.Extensions.RobustnessFinite

#check Harsanyi.Robustness.pairDelta_baseline
#check Harsanyi.Robustness.pairDelta_smul
#check Harsanyi.Robustness.average_smul

namespace DirectImportConsumer
open Harsanyi Harsanyi.Robustness

variable {α X : Type*} [DecidableEq α]

/-- The paper-facing game is g(S)=v(mask(S)). Its empty output may be nonzero.
The finite context average uses the library convention even for an empty family;
this lemma does not assert that an undefined source average is defined. -/
theorem affine_masked_pair_interaction (v : X → ℝ) (mask : Finset α → X)
    (N : Finset α) (i j : α) (m : ℕ) (a b : ℝ) :
    multiOrderInteraction (fun S => a * v (mask S) + b) N i j m =
      a * multiOrderInteraction (fun S => v (mask S)) N i j m := by
  unfold multiOrderInteraction contextAverage
  have h : pairDelta (fun S => a * v (mask S) + b) i j =
      (fun S => a * pairDelta (fun T => v (mask T)) i j S) := by
    funext S
    calc
      pairDelta (fun T => a * v (mask T) + b) i j S =
          pairDelta (fun T => a * v (mask T)) i j S := by
        simpa only [sub_neg_eq_add] using
          pairDelta_baseline (fun T => a * v (mask T)) i j S (-b)
      _ = a * pairDelta (fun T => v (mask T)) i j S :=
        pairDelta_smul (fun T => v (mask T)) i j S a
  rw [h]
  exact average_smul _ _ _

end DirectImportConsumer

#check DirectImportConsumer.affine_masked_pair_interaction
#print axioms DirectImportConsumer.affine_masked_pair_interaction
