import Harsanyi

namespace LibraryConsumer
open Finset Harsanyi
variable {α : Type*} [DecidableEq α]

/-- New conclusion: an affine rescaling changes each nonempty interaction only by its scale. -/
theorem affine_nonempty (v : Game α) (a b : ℝ) (S : Finset α) (hS : S.Nonempty) :
    interaction (fun T => a * v T + b) S = a * interaction v S := by
  rw [interaction_add, interaction_smul, interaction_const, if_neg hS.ne_empty, add_zero]

/-- New conclusion: coefficients reconstructing centered utilities equal the original
dividends on all nonempty coalitions. This combines uniqueness with baseline conversion. -/
theorem baseline_unique_nonempty (v d : Game α)
    (h : ∀ S, reconstruct d S = v S - v ∅) (S : Finset α) (hS : S.Nonempty) :
    d S = interaction v S := by
  have hd : d = interaction (centered v) := reconstruction_unique (centered v) d h
  rw [hd, interaction_centered_nonempty v S hS]

end LibraryConsumer
