import Harsanyi

/-! A generic baseline-convention adapter for later paper mappings.
This file does not assert that any paper claim has been extracted or aligned. -/
namespace PaperProofs
open Finset Harsanyi
variable {α : Type*} [DecidableEq α]

/-- A paper using zero-baseline utilities can reconstruct its centered utility. -/
theorem centered_reconstruction (v : Game α) (S : Finset α) :
    reconstruct (interaction (centered v)) S = v S - v ∅ := by
  rw [reconstruction]
  rfl

/-- Nonempty dividends agree under the two baseline conventions. -/
theorem centered_dividend_agreement (v : Game α) (S : Finset α) (hS : S.Nonempty) :
    interaction (centered v) S = interaction v S :=
  interaction_centered_nonempty v S hS

end PaperProofs
