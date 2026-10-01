import Harsanyi.Core.Properties

open Finset Harsanyi

namespace APIPlaytestMax.RejectionFixture

-- Intentionally rejected synthetic API call: the theorem needs S.Nonempty.
-- This is not an assertion about any source paper and is not a corpus issue.
theorem centering_without_nonempty {α : Type*} [DecidableEq α]
    (v : Game α) (S : Finset α) :
    interaction (centered v) S = interaction v S := by
  exact interaction_centered_nonempty v S

end APIPlaytestMax.RejectionFixture
