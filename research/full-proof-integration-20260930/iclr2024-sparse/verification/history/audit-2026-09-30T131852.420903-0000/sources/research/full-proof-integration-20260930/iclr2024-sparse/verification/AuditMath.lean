import Lean.Util.CollectAxioms
import Harsanyi.Extensions.Sparsity
import Harsanyi.Extensions.Noise
import Harsanyi.Extensions.Attribution
import Harsanyi.Extensions.OrInteraction


namespace FullSparse
open Finset Harsanyi Harsanyi.Sparsity

noncomputable def maskedGame {n : ℕ} (v : (Fin n → ℝ) → ℝ) (r x : Fin n → ℝ) : Game (Fin n) :=
  fun S => v (maskCoordinates r x S)

/-- Exact T1 with actual coordinate masks and an arbitrary model-output baseline. -/
theorem theorem1 {n : ℕ} (v : (Fin n → ℝ) → ℝ) (r x : Fin n → ℝ) (S : Finset (Fin n)) :
    v (maskCoordinates r x S) =
      reconstruct (interaction (centered (maskedGame v r x))) S + v (maskCoordinates r x ∅) := by
  rw [reconstruction]
  simp [centered, maskedGame]

/-- Exact L2 in the source range M≤m≤n. -/
theorem lemma2 {n : ℕ} (v : (Fin n → ℝ) → ℝ) (r x : Fin n → ℝ) (M m : ℕ)
    (hMm : M ≤ m) (hmn : m ≤ n)
    (hcut : ∀ S : Finset (Fin n), M < S.card → interaction (centered (maskedGame v r x)) S = 0) :
    meanOutput (centered (maskedGame v r x)) univ m =
      ∑ k ∈ Icc 1 M, ((Nat.choose m k : ℝ) / (Nat.choose n k : ℝ)) *
        orderTotal (interaction (centered (maskedGame v r x))) univ k := by
  simpa using mean_centered_cutoff (maskedGame v r x) univ M m hMm (by simpa using hmn)
    (fun S hS hM => hcut S hM)

/-- Complete T2 witness from the original three conditions in its positive-order defined domain.
J is any finite low-digit family; its all-zero witnesses cover both customary p<1 readings. -/
theorem theorem2 {n : ℕ} (v : (Fin n → ℝ) → ℝ) (r x : Fin n → ℝ) (M : ℕ) (p : ℝ)
    (J : Finset ℕ) (hn : 1 < n) (hM : 0 < M) (hMn : M ≤ n) (hp : 0 < p)
    (hcut : ∀ S : Finset (Fin n), M < S.card → interaction (centered (maskedGame v r x)) S = 0)
    (hmono : ∀ m' m, m' ≤ m → m ≤ n →
      meanOutput (centered (maskedGame v r x)) univ m' ≤ meanOutput (centered (maskedGame v r x)) univ m)
    (hrob : ∀ m' m, 0 < m → m' ≤ m → m ≤ n →
      ((m' : ℝ) / (m : ℝ)) ^ p * meanOutput (centered (maskedGame v r x)) univ m ≤
        meanOutput (centered (maskedGame v r x)) univ m') :
    Nonempty (CoefficientWitness (maskedGame v r x) univ M p J) := by
  apply sparse_original_coefficient_witness
  · simpa using hn
  · exact hM
  · simpa using hMn
  · exact hp
  · exact fun S hS hc => hcut S hc
  · intro m' m hm' hm
    exact hmono m' m hm' (by simpa using hm)
  · intro m' m hm0 hm' hm
    exact hrob m' m hm0 hm' (by simpa using hm)

/-- T3 includes the final original T2 coefficient expression, with no conclusion-as-premise. -/
theorem theorem3 {n : ℕ} (v : (Fin n → ℝ) → ℝ) (r x : Fin n → ℝ) (M : ℕ) (p : ℝ)
    (J : Finset ℕ) (hn : 1 < n) (hM : 0 < M) (hMn : M ≤ n) (hp : 0 < p)
    (hcut : ∀ S : Finset (Fin n), M < S.card → interaction (centered (maskedGame v r x)) S = 0)
    (hmono : ∀ m' m, m' ≤ m → m ≤ n →
      meanOutput (centered (maskedGame v r x)) univ m' ≤ meanOutput (centered (maskedGame v r x)) univ m)
    (hrob : ∀ m' m, 0 < m → m' ≤ m → m ≤ n →
      ((m' : ℝ) / (m : ℝ)) ^ p * meanOutput (centered (maskedGame v r x)) univ m ≤
        meanOutput (centered (maskedGame v r x)) univ m') :
    ∃ w : CoefficientWitness (maskedGame v r x) univ M p J, ∀ k ∈ Icc 1 M, ∀ τ : ℝ, 0 < τ →
      cancellationRatio (interaction (centered (maskedGame v r x))) univ k ≠ 0 →
      ((salientFamily (interaction (centered (maskedGame v r x))) univ k τ).card : ℝ) ≤
        meanOutput (centered (maskedGame v r x)) univ 1 /
          (τ * |cancellationRatio (interaction (centered (maskedGame v r x))) univ k|) *
          |w.c k * (n : ℝ) ^ (p + w.δ) + ∑ i ∈ J, w.a k i * (n : ℝ) ^ i| := by
  simpa using sparse_original_T2_T3 (maskedGame v r x) univ M p J
    (by simpa using hn) hM (by simpa using hMn) hp
    (fun S hS hc => hcut S hc)
    (fun m' m hm' hm => hmono m' m hm' (by simpa using hm))
    (fun m' m hm0 hm' hm => hrob m' m hm0 hm' (by simpa using hm))

/-- The valid nonempty Sparse dummy property; source additive constant is u({i}). -/
theorem dummy {n : ℕ} (v : (Fin n → ℝ) → ℝ) (r x : Fin n → ℝ)
    (S : Finset (Fin n)) (i : Fin n) (hi : i ∉ S) (hS : S.Nonempty)
    (h : ∀ U, i ∉ U → centered (maskedGame v r x) (insert i U) =
      centered (maskedGame v r x) U + centered (maskedGame v r x) {i}) :
    interaction (centered (maskedGame v r x)) (insert i S) = 0 := by
  apply interaction_additive_dummy_nonempty _ S i hi hS (centered (maskedGame v r x) {i})
  intro U hU
  exact h U (fun hhit => hi (hU hhit))

/-- Exact L4; disjointness is precisely T⊆N\S in the paper. -/
theorem lemma4 {n : ℕ} (v : (Fin n → ℝ) → ℝ) (r x : Fin n → ℝ)
    (T S : Finset (Fin n)) (hTS : Disjoint T S) :
    higherMarginal (centered (maskedGame v r x)) T S =
      ∑ U ∈ S.powerset, interaction (centered (maskedGame v r x)) (T ∪ U) :=
  higherMarginal_eq_sum_interaction _ _ _ hTS

/-- T4 uses the classical factorial-weighted definition, genuinely proved equal to the allocation. -/
theorem theorem4 {n : ℕ} (v : (Fin n → ℝ) → ℝ) (r x : Fin n → ℝ) (i : Fin n) :
    factorialShapley (centered (maskedGame v r x)) univ i =
      ∑ S ∈ ((univ : Finset (Fin n)).erase i).powerset,
        (1 / (S.card + 1 : ℝ)) * interaction (centered (maskedGame v r x)) (insert i S) :=
  factorialShapley_eq_dividends _ _ _ (mem_univ _)

theorem theorem5 {n : ℕ} (v : (Fin n → ℝ) → ℝ) (r x : Fin n → ℝ) (T : Finset (Fin n)) :
    factorialShapleyInteraction (centered (maskedGame v r x)) univ T =
      ∑ S ∈ ((univ : Finset (Fin n)) \ T).powerset,
        (1 / (S.card + 1 : ℝ)) * interaction (centered (maskedGame v r x)) (T ∪ S) :=
  factorialShapleyInteraction_eq_dividends _ _ _ (subset_univ _)

theorem theorem6 {n : ℕ} (v : (Fin n → ℝ) → ℝ) (r x : Fin n → ℝ)
    (k : ℕ) (hk : 0 < k) (T : Finset (Fin n)) :
    shapleyTaylor (centered (maskedGame v r x)) univ k T =
      if T.card < k then interaction (centered (maskedGame v r x)) T
      else if T.card = k then
        ∑ S ∈ ((univ : Finset (Fin n)) \ T).powerset,
          (1 / ((S.card + k).choose k : ℝ)) * interaction (centered (maskedGame v r x)) (T ∪ S)
      else 0 :=
  shapleyTaylor_eq_dividends _ _ _ (subset_univ _) k hk

/-- The paper's purely algebraic noise decomposition, including the centered empty interaction. -/
theorem noise_linearity {n : ℕ} (v : (Fin n → ℝ) → ℝ) (r x : Fin n → ℝ)
    (ε : Game (Fin n)) (S : Finset (Fin n)) :
    interaction (centered (fun U => maskedGame v r x U + ε U)) S =
      interaction (centered (maskedGame v r x)) S + interaction (centered ε) S := by
  have he : centered (fun U => maskedGame v r x U + ε U) =
      fun U => centered (maskedGame v r x) U + centered ε U := by
    funext U
    simp only [centered]
    ring
  rw [he, interaction_add]

/-- Sparse's centered OR-to-reverse-AND relation includes its zero empty convention. -/
theorem or_reverse {n : ℕ} (v : (Fin n → ℝ) → ℝ) (r x : Fin n → ℝ)
    (S : Finset (Fin n)) :
    orInteraction (centered (maskedGame v r x)) univ S =
      interaction (fun L => centered (maskedGame v r x) univ -
        centered (maskedGame v r x) ((univ : Finset (Fin n)) \ L)) S := by
  by_cases hS : S = ∅
  · subst S
    simp [orInteraction]
  · rw [or_dual _ _ _ hS, interaction_sub, interaction_const, if_neg hS]
    ring

/-- Eq62 from the original same centered decomposition; no gamma algorithm error is assumed. -/
theorem and_or_matching {n : ℕ} (v : (Fin n → ℝ) → ℝ) (r x : Fin n → ℝ)
    (a b : Game (Fin n)) (h : ∀ S, centered (maskedGame v r x) S = a S + b S)
    (S : Finset (Fin n)) :
    centered (maskedGame v r x) S = reconstruct (interaction a) S + orReconstruction b univ S := by
  rw [reconstruction, or_reconstruction b univ S (subset_univ _)]
  exact h S


/-- The source linearity condition is checked on every coordinate coalition. -/
theorem linearity {n : ℕ} (v : (Fin n → ℝ) → ℝ) (r x : Fin n → ℝ)
    (u1 u2 : Game (Fin n)) (h : ∀ S, centered (maskedGame v r x) S = u1 S + u2 S)
    (S : Finset (Fin n)) :
    interaction (centered (maskedGame v r x)) S = interaction u1 S + interaction u2 S := by
  have he : centered (maskedGame v r x) = fun U => u1 U + u2 U := funext h
  rw [he, interaction_add]

theorem symmetry {n : ℕ} (v : (Fin n → ℝ) → ℝ) (r x : Fin n → ℝ)
    (S : Finset (Fin n)) (i j : Fin n) (hi : i ∉ S) (hj : j ∉ S)
    (h : ∀ U, i ∉ U → j ∉ U → centered (maskedGame v r x) (insert i U) =
      centered (maskedGame v r x) (insert j U)) :
    interaction (centered (maskedGame v r x)) (insert i S) =
      interaction (centered (maskedGame v r x)) (insert j S) := by
  apply interaction_symmetry _ S i j hi hj
  intro U hU
  exact h U (fun hu => hi (hU hu)) (fun hu => hj (hU hu))

theorem anonymity {n : ℕ} (v : (Fin n → ℝ) → ℝ) (r x : Fin n → ℝ)
    (π : Fin n ≃ Fin n) (S : Finset (Fin n)) :
    interaction (fun U => centered (maskedGame v r x) (U.map π.symm.toEmbedding))
      (S.map π.toEmbedding) = interaction (centered (maskedGame v r x)) S :=
  interaction_relabel π _ S

theorem recursive {n : ℕ} (v : (Fin n → ℝ) → ℝ) (r x : Fin n → ℝ)
    (S : Finset (Fin n)) (i : Fin n) (hi : i ∉ S) :
    interaction (centered (maskedGame v r x)) (insert i S) =
      interaction (fun U => centered (maskedGame v r x) (insert i U)) S -
        interaction (centered (maskedGame v r x)) S :=
  interaction_context_difference _ S i hi

/-- Displayed pure-interaction game, including the constant-game T=empty boundary.
It is not falsely declared centered when T=empty and c≠0. -/
theorem distribution {n : ℕ} (T S : Finset (Fin n)) (c : ℝ) :
    interaction (unanimity T c) S = if S = T then c else 0 :=
  interaction_unanimity T c S

/-- Exactly n positive mask-size layers with t requested samples per layer.
This is a count of requested evaluations, not a run-time or concentration claim. -/
theorem sampling_evaluation_count (n t : ℕ) : (∑ _m ∈ Icc 1 n, t) = n * t := by
  simp [Nat.card_Icc, Nat.mul_comm]

noncomputable def examplePolynomial (z : Fin 5 → ℝ) : ℝ :=
  z 0 * z 1 * z 2 + z 0 * z 1 + z 1 * z 2 + z 1 + z 2

/- The actual Appendix H mean of all ten two-variable masks, with baseline 0 and active input 1. -/
set_option maxHeartbeats 1000000 in
theorem example_mean_two :
    meanOutput (centered (maskedGame examplePolynomial (fun _ => 0) (fun _ => 1))) univ 2 = 1 := by
  have h2 : (univ : Finset (Fin 5)).powersetCard 2 =
      {{0,1},{0,2},{0,3},{0,4},{1,2},{1,3},{1,4},{2,3},{2,4},{3,4}} := by decide
  unfold meanOutput
  rw [h2]
  simp (disch := decide) only [Finset.sum_insert, Finset.sum_singleton]
  norm_num [centered, maskedGame, examplePolynomial, maskCoordinates, Nat.choose, Fin.ext_iff]

/- Corrected proof arithmetic: the missing x3 term makes the mean 19/10, while the source conclusion survives. -/
set_option maxHeartbeats 1000000 in
theorem example_mean_three :
    meanOutput (centered (maskedGame examplePolynomial (fun _ => 0) (fun _ => 1))) univ 3 = 19 / 10 := by
  have h3 : (univ : Finset (Fin 5)).powersetCard 3 =
      {{0,1,2},{0,1,3},{0,1,4},{0,2,3},{0,2,4},{0,3,4},{1,2,3},{1,2,4},{1,3,4},{2,3,4}} := by decide
  unfold meanOutput
  rw [h3]
  simp (disch := decide) only [Finset.sum_insert, Finset.sum_singleton]
  norm_num [centered, maskedGame, examplePolynomial, maskCoordinates, Nat.choose, Fin.ext_iff]

/-- Only the original Appendix H comparison, not a general average-monotonicity theorem. -/
theorem example_mean_monotone_comparison :
    meanOutput (centered (maskedGame examplePolynomial (fun _ => 0) (fun _ => 1))) univ 2 ≤
      meanOutput (centered (maskedGame examplePolynomial (fun _ => 0) (fun _ => 1))) univ 3 := by
  rw [example_mean_two, example_mean_three]
  norm_num

end FullSparse


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

open Lean Elab Command Meta
set_option pp.universes true
set_option pp.fullNames true
set_option pp.piBinderTypes true
run_cmd liftTermElabM do
  for name in #[`Harsanyi.Sparsity.choose_coefficients_zero, `Harsanyi.Sparsity.binomial_matrix_kernel, `Harsanyi.Sparsity.binomial_coefficients_zero_of_le, `Harsanyi.Sparsity.orderTotal, `Harsanyi.Sparsity.meanOutput, `Harsanyi.Sparsity.card_supermasks, `Harsanyi.Sparsity.subset_layer_sum, `Harsanyi.Sparsity.layer_sum_reconstruct, `Harsanyi.Sparsity.choose_ratio, `Harsanyi.Sparsity.mean_reconstruction, `Harsanyi.Sparsity.mean_centered_cutoff, `Harsanyi.Sparsity.mean_centered_cutoff_all, `Harsanyi.Sparsity.mean_centered_zero, `Harsanyi.Sparsity.meanOutput_top, `Harsanyi.Sparsity.totalStrength, `Harsanyi.Sparsity.salientFamily, `Harsanyi.Sparsity.cancellationRatio, `Harsanyi.Sparsity.threshold_count, `Harsanyi.Sparsity.salient_count_bound, `Harsanyi.Sparsity.coefficient_normalization, `Harsanyi.Sparsity.sparse_coefficient_existence, `Harsanyi.Sparsity.leadingAggregate, `Harsanyi.Sparsity.digitAggregate, `Harsanyi.Sparsity.CoefficientWitness, `Harsanyi.Sparsity.sparse_original_coefficient_witness, `Harsanyi.Sparsity.salient_bound_original_coefficients, `Harsanyi.Sparsity.sparse_original_T2_T3, `Harsanyi.signed_gaussian_variance, `Harsanyi.and_gaussian_variance, `Harsanyi.or_gaussian_variance, `Harsanyi.noisyMaskedGame, `Harsanyi.noisy_and_identity, `Harsanyi.noisy_or_identity, `Harsanyi.noisy_masked_and_variance, `Harsanyi.noisy_masked_or_variance, `FullSparse.maskedGame, `FullSparse.theorem1, `FullSparse.lemma2, `FullSparse.theorem2, `FullSparse.theorem3, `FullSparse.dummy, `FullSparse.lemma4, `FullSparse.theorem4, `FullSparse.theorem5, `FullSparse.theorem6, `FullSparse.noise_linearity, `FullSparse.or_reverse, `FullSparse.and_or_matching, `FullSparse.linearity, `FullSparse.symmetry, `FullSparse.anonymity, `FullSparse.recursive, `FullSparse.distribution, `FullSparse.sampling_evaluation_count, `FullSparse.examplePolynomial, `FullSparse.example_mean_two, `FullSparse.example_mean_three, `FullSparse.example_mean_monotone_comparison, `FullGeneralizableAnalysis.decomposition_iff_unique_gamma, `FullGeneralizableAnalysis.gamma_gives_decomposition, `FullGeneralizableAnalysis.masked_model_decomposition, `FullGeneralizableAnalysis.rowStrength, `FullGeneralizableAnalysis.rowStrength_plateau, `FullGeneralizableAnalysis.pooledPenalty, `FullGeneralizableAnalysis.entryPenalty, `FullGeneralizableAnalysis.matrixObjective, `FullGeneralizableAnalysis.alpha_zero, `FullGeneralizableAnalysis.signed_max_counterexample, `FullGeneralizableAnalysis.masked_model_and_variance, `FullGeneralizableAnalysis.masked_model_or_variance] do
    let info ← getConstInfo name
    let signature ← ppExpr info.type
    let axioms ← Lean.collectAxioms name
    let deps := info.type.getUsedConstants ++ (info.value?.map Expr.getUsedConstants).getD #[]
    let kind := match info with | .thmInfo _ => "theorem" | .inductInfo _ => "structure" | _ => "definition"
    liftM <| IO.println ("SPARSE_API:" ++ (Json.mkObj [
      ("name", toJson name.toString), ("signature", toJson signature.pretty),
      ("kind", toJson kind), ("axioms", toJson (axioms.map Name.toString)),
      ("dependencies", toJson (deps.map Name.toString))]).compress)

