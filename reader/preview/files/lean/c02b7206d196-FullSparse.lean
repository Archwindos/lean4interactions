import Harsanyi.Extensions.Sparsity
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

/-- General matching identity, retaining the OR output baseline explicitly. -/
theorem and_or_matching {n : ℕ} (v : (Fin n → ℝ) → ℝ) (r x : Fin n → ℝ)
    (a b : Game (Fin n)) (h : ∀ S, centered (maskedGame v r x) S = a S + b S)
    (S : Finset (Fin n)) :
    centered (maskedGame v r x) S = reconstruct (interaction a) S + orReconstruction b univ S := by
  rw [reconstruction, or_reconstruction b univ S (subset_univ _)]
  exact h S

/-- Original Eq62 AND component with its explicit zero empty condition. -/
theorem and_matching_zero_baseline {n : ℕ} (a : Game (Fin n)) (ha0 : a ∅ = 0)
    (S : Finset (Fin n)) :
    a S = ∑ T ∈ S.powerset, interaction a T ∧ interaction a ∅ = 0 := by
  constructor
  · exact (reconstruction a S).symm
  · simpa using ha0

/-- Original Eq62 OR component: its zero empty condition removes the baseline summand. -/
theorem or_matching_zero_baseline {n : ℕ} (b : Game (Fin n)) (hb0 : b ∅ = 0)
    (S : Finset (Fin n)) :
    b S = ∑ T ∈ (univ : Finset (Fin n)).powerset.filter (fun T => ¬ Disjoint T S),
      orInteraction b univ T ∧ orInteraction b univ ∅ = 0 := by
  have hb : orReconstruction b univ S = b S := or_reconstruction b univ S (subset_univ _)
  have he : orInteraction b univ ∅ = 0 := by simp [orInteraction, hb0]
  constructor
  · simpa only [orReconstruction, he, zero_add] using hb.symm
  · exact he

/-- Literal original Eq62, including both original zero-empty component conditions. -/
theorem and_or_matching_eq62 {n : ℕ} (v : (Fin n → ℝ) → ℝ) (r x : Fin n → ℝ)
    (a b : Game (Fin n)) (ha0 : a ∅ = 0) (hb0 : b ∅ = 0)
    (h : ∀ S, centered (maskedGame v r x) S = a S + b S) (S : Finset (Fin n)) :
    a S = (∑ T ∈ S.powerset, interaction a T) ∧
    b S = (∑ T ∈ (univ : Finset (Fin n)).powerset.filter (fun T => ¬ Disjoint T S),
      orInteraction b univ T) ∧
    centered (maskedGame v r x) S =
      (∑ T ∈ S.powerset, interaction a T) +
      (∑ T ∈ (univ : Finset (Fin n)).powerset.filter (fun T => ¬ Disjoint T S),
        orInteraction b univ T) := by
  obtain ⟨ha, _⟩ := and_matching_zero_baseline a ha0 S
  obtain ⟨hb, _⟩ := or_matching_zero_baseline b hb0 S
  refine ⟨ha, hb, ?_⟩
  rw [h S, ha, hb]


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
