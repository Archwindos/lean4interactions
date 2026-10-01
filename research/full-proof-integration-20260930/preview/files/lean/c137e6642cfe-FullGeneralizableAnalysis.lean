import Harsanyi.Extensions.Noise
import Mathlib.Data.Finset.Lattice.Fold

namespace FullGeneralizableAnalysis
open Finset Harsanyi MeasureTheory ProbabilityTheory
open scoped ProbabilityTheory

variable {α : Type*} [DecidableEq α]

/-- A gamma family is in bijection with all decompositions on every masked input. -/
theorem decomposition_iff_unique_gamma (g a b : Game α)
    (h : ∀ T, a T + b T = g T) :
    ∃! γ : Game α, (∀ T, a T = g T / 2 + γ T) ∧ (∀ T, b T = g T / 2 - γ T) := by
  refine ⟨fun T => (a T - b T) / 2, ?_, ?_⟩
  · constructor <;> intro T <;> have hh := h T <;> linarith
  · intro γ hγ
    funext T
    have h1 := hγ.1 T
    have hh := h T
    linarith

theorem gamma_gives_decomposition (g γ : Game α) :
    ∀ T, (g T / 2 + γ T) + (g T / 2 - γ T) = g T := by
  intro T
  ring

/-- Actual Fin n mask family: Game (Fin n) has exactly the original 2^n coordinates. -/
theorem masked_model_decomposition (n : ℕ) (v : (Fin n → ℝ) → ℝ) (r x : Fin n → ℝ)
    (a b : Game (Fin n)) (h : ∀ T, a T + b T = v (maskCoordinates r x T)) :
    ∃! γ : Game (Fin n),
      (∀ T, a T = v (maskCoordinates r x T) / 2 + γ T) ∧
      (∀ T, b T = v (maskCoordinates r x T) / 2 - γ T) :=
  decomposition_iff_unique_gamma _ _ _ h

variable {ρ ι : Type*}

noncomputable def rowStrength (I : Finset ι) (hI : I.Nonempty) (a : ι → ℝ) : ℝ :=
  I.sup' hI fun i => |a i|

/-- All finite models, with arbitrary signs. A retained maximizing component fixes the row norm. -/
theorem rowStrength_plateau (I : Finset ι) (hI : I.Nonempty) (a b : ι → ℝ)
    (j : ι) (hj : j ∈ I) (ha : ∀ i ∈ I, |a i| ≤ |a j|)
    (hb : ∀ i ∈ I, |b i| ≤ |a j|) (hkeep : |b j| = |a j|) :
    rowStrength I hI b = rowStrength I hI a := by
  have heq (c : ι → ℝ) (hc : ∀ i ∈ I, |c i| ≤ |a j|)
      (hjc : |c j| = |a j|) : rowStrength I hI c = |a j| := by
    apply le_antisymm
    · exact Finset.sup'_le hI _ hc
    · rw [← hjc]
      exact Finset.le_sup' (fun i => |c i|) hj
  rw [heq b hb hkeep, heq a ha rfl]

noncomputable def pooledPenalty (R : Finset ρ) (I : Finset ι) (hI : I.Nonempty)
    (A B : ρ → ι → ℝ) : ℝ :=
  ∑ S ∈ R, (rowStrength I hI (A S) + rowStrength I hI (B S))

noncomputable def entryPenalty (R : Finset ρ) (I : Finset ι) (A B : ρ → ι → ℝ) : ℝ :=
  ∑ S ∈ R, ∑ i ∈ I, (|A S i| + |B S i|)

noncomputable def matrixObjective (R : Finset ρ) (I : Finset ι) (hI : I.Nonempty)
    (A B : ρ → ι → ℝ) (α : ℝ) : ℝ :=
  pooledPenalty R I hI A B + α * entryPenalty R I A B

/-- The exact Eq6 alpha=0 specialization, for the actual row and entrywise matrix penalties. -/
theorem alpha_zero (R : Finset ρ) (I : Finset ι) (hI : I.Nonempty) (A B : ρ → ι → ℝ) :
    matrixObjective R I hI A B 0 = pooledPenalty R I hI A B := by
  simp [matrixObjective]

/-- This only refutes the pointwise row expansion used in Eq10, not an equality of minima. -/
theorem signed_max_counterexample :
    max (|(-3 : ℝ)|) (|(2 : ℝ)|) ≠ |max (-3 : ℝ) 2| := by norm_num

variable {Ω : Type*} [MeasurableSpace Ω]

/-- Paper-level AND variance: an actual model evaluated on a fixed masked-output family.
The raw empty interaction is included, exactly as in Generalizable. -/
theorem masked_model_and_variance (n : ℕ) (v : (Fin n → ℝ) → ℝ) (r x : Fin n → ℝ)
    (μ : Measure Ω) [IsProbabilityMeasure μ] (T : Finset (Fin n))
    (ε : Finset (Fin n) → Ω → ℝ) (σ2 : NNReal)
    (hm : ∀ L ∈ T.powerset, Measurable (ε L))
    (hlaw : ∀ L ∈ T.powerset, μ.map (ε L) = gaussianReal 0 σ2)
    (hi : Set.Pairwise (↑T.powerset : Set (Finset (Fin n))) fun L K => IndepFun (ε L) (ε K) μ) :
    variance (fun ω => interaction (fun L => v (maskCoordinates r x L) + ε L ω) T) μ =
      (2 : ℝ) ^ T.card * σ2 := by
  exact noisy_masked_and_variance μ (fun L => v (maskCoordinates r x L)) T ε σ2 hm hlaw hi

/-- Paper-level OR variance, with complement indices in the same finite coordinate universe.
The separately defined raw OR empty baseline has variance sigma². -/
theorem masked_model_or_variance (n : ℕ) (v : (Fin n → ℝ) → ℝ) (r x : Fin n → ℝ)
    (μ : Measure Ω) [IsProbabilityMeasure μ] (T : Finset (Fin n))
    (ε : Finset (Fin n) → Ω → ℝ) (σ2 : NNReal)
    (hm : ∀ L : Finset (Fin n), Measurable (ε L))
    (hlaw : ∀ L : Finset (Fin n), μ.map (ε L) = gaussianReal 0 σ2)
    (hi : Set.Pairwise (↑(univ : Finset (Fin n)).powerset : Set (Finset (Fin n)))
      fun L K => IndepFun (ε L) (ε K) μ) :
    variance (fun ω => orInteraction (fun L => v (maskCoordinates r x L) + ε L ω) univ T) μ =
      (2 : ℝ) ^ T.card * σ2 := by
  exact noisy_masked_or_variance μ (fun L => v (maskCoordinates r x L)) univ T (subset_univ _) ε σ2
    (fun L hL => hm L) (fun L hL => hlaw L) hi

end FullGeneralizableAnalysis
