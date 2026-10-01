import Harsanyi.Core.Properties

open Finset Harsanyi

namespace SparseConceptsPublicPilot

-- Fixing a masked input and baseline gives a Game (Fin n). All subsets,
-- including the empty subset, occur in the source theorem.
theorem theorem1_faithfulness (n : ℕ) (maskedOutput : Game (Fin n))
    (S : Finset (Fin n)) :
    reconstruct (interaction maskedOutput) S = maskedOutput S := by
  exact reconstruction maskedOutput S

-- Appendix C further asserts uniqueness under exact faithfulness on all masks.
theorem theorem1_unique_coefficients (n : ℕ)
    (maskedOutput coeffs : Game (Fin n))
    (faithful : ∀ S, reconstruct coeffs S = maskedOutput S) :
    coeffs = interaction maskedOutput := by
  exact reconstruction_unique maskedOutput coeffs faithful

-- Evidence for the displayed Dummy formula only. The source also says
-- "with other variables", so intended scope remains for user confirmation.
def onePlayerGame : Game (Fin 1) :=
  fun S => if (0 : Fin 1) ∈ S then 1 else 0

theorem displayed_dummy_counterexample :
    (∀ S : Finset (Fin 1), (0 : Fin 1) ∉ S →
      onePlayerGame (insert 0 S) = onePlayerGame S + onePlayerGame {0}) ∧
    interaction onePlayerGame ({0} : Finset (Fin 1)) ≠ 0 := by
  constructor
  · intro S hS
    simp [onePlayerGame, hS]
  · rw [interaction_singleton]
    norm_num [onePlayerGame]

end SparseConceptsPublicPilot

#print axioms SparseConceptsPublicPilot.theorem1_faithfulness
#print axioms SparseConceptsPublicPilot.theorem1_unique_coefficients
#print axioms SparseConceptsPublicPilot.displayed_dummy_counterexample
