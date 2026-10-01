import Consumer

/-- An executable illustration using exact rationals. Its output illustrates the formula;
the general real-valued conclusions live in `Consumer.lean`. -/
def demoInteraction (v : Finset (Fin 2) → ℚ) (S : Finset (Fin 2)) : ℚ :=
  ∑ T ∈ S.powerset, (-1 : ℚ) ^ (S.card - T.card) * v T

def main : IO Unit := do
  let N : Finset (Fin 2) := {0, 1}
  let v : Finset (Fin 2) → ℚ := fun S =>
    7 + (if 0 ∈ S then 2 else 0) + (if 1 ∈ S then 3 else 0) +
      (if N ⊆ S then 5 else 0)
  IO.println s!"baseline={v ∅}; I0={demoInteraction v {0}}; I1={demoInteraction v {1}}; I01={demoInteraction v N}"
  IO.println s!"reconstruction={∑ S ∈ N.powerset, demoInteraction v S}; v(N)={v N}"
