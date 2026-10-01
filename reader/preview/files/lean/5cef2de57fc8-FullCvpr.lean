import Harsanyi.Extensions.Attribution
import Harsanyi.Extensions.OrInteraction

namespace FullCvpr
open Finset Harsanyi

noncomputable def maskedGame {X : Type*} {n : ℕ}
    (v : X → ℝ) (mask : Finset (Fin n) → X) : Game (Fin n) := fun S => v (mask S)

theorem reconstruction {X : Type*} {n : ℕ} (v : X → ℝ) (mask : Finset (Fin n) → X)
    (S : Finset (Fin n)) :
    (∑ A ∈ S.powerset, interaction (maskedGame v mask) A) = v (mask S) := by
  exact Harsanyi.reconstruction (maskedGame v mask) S

theorem uniqueness {X : Type*} {n : ℕ} (v : X → ℝ) (mask : Finset (Fin n) → X)
    (d : Game (Fin n)) (h : ∀ S, (∑ A ∈ S.powerset, d A) = v (mask S)) :
    d = interaction (maskedGame v mask) := by
  exact reconstruction_unique (maskedGame v mask) d h

theorem linearity {X : Type*} {n : ℕ} (v t u : X → ℝ) (mask : Finset (Fin n) → X)
    (h : ∀ S, v (mask S) = t (mask S) + u (mask S)) (A : Finset (Fin n)) :
    interaction (maskedGame v mask) A =
      interaction (maskedGame t mask) A + interaction (maskedGame u mask) A := by
  calc
    _ = interaction (fun S => maskedGame t mask S + maskedGame u mask S) A := by
      exact interaction_congr _ _ _ (fun S _ => h S)
    _ = _ := interaction_add _ _ _

theorem symmetry {X : Type*} {n : ℕ} (v : X → ℝ) (mask : Finset (Fin n) → X)
    (i j : Fin n) (h : ∀ U, i ∉ U → j ∉ U → v (mask (insert i U)) = v (mask (insert j U)))
    (S : Finset (Fin n)) (hi : i ∉ S) (hj : j ∉ S) :
    interaction (maskedGame v mask) (insert i S) = interaction (maskedGame v mask) (insert j S) := by
  exact interaction_symmetry _ _ _ _ hi hj (fun U hU => h U (fun hiU => hi (hU hiU))
    (fun hjU => hj (hU hjU)))

theorem anonymity {n : ℕ} (g : Game (Fin n)) (π : Fin n ≃ Fin n) (S : Finset (Fin n)) :
    interaction (fun U => g (U.map π.symm.toEmbedding)) (S.map π.toEmbedding) = interaction g S := by
  exact interaction_relabel π g S

theorem recursive {X : Type*} {n : ℕ} (v : X → ℝ) (mask : Finset (Fin n) → X)
    (S : Finset (Fin n)) (i : Fin n) (hi : i ∉ S) :
    interaction (maskedGame v mask) (insert i S) =
      interaction (fun U => v (mask (insert i U))) S - interaction (maskedGame v mask) S := by
  exact interaction_context_difference _ _ _ hi

theorem interaction_distribution {n : ℕ} (T S : Finset (Fin n)) (c : ℝ) :
    interaction (unanimity T c) S = if S = T then c else 0 := by
  exact interaction_unanimity T c S

theorem marginal_decomposition {X : Type*} {n : ℕ} (v : X → ℝ) (mask : Finset (Fin n) → X)
    (T S : Finset (Fin n)) (h : Disjoint T S) :
    (∑ L ∈ T.powerset, (-1 : ℝ) ^ (T.card - L.card) * v (mask (L ∪ S))) =
      ∑ U ∈ S.powerset, interaction (maskedGame v mask) (T ∪ U) := by
  simpa [higherMarginal, interaction, maskedGame] using
    higherMarginal_eq_sum_interaction (maskedGame v mask) T S h

theorem shapley {X : Type*} {n : ℕ} (v : X → ℝ) (mask : Finset (Fin n) → X) (i : Fin n) :
    factorialShapley (maskedGame v mask) univ i =
      ∑ S ∈ (univ.erase i).powerset, (1 / (S.card + 1 : ℝ)) *
        interaction (maskedGame v mask) (insert i S) := by
  exact factorialShapley_eq_dividends _ _ _ (mem_univ _)

theorem shapley_interaction {X : Type*} {n : ℕ} (v : X → ℝ)
    (mask : Finset (Fin n) → X) (T : Finset (Fin n)) :
    factorialShapleyInteraction (maskedGame v mask) univ T =
      ∑ S ∈ (univ \ T).powerset, (1 / (S.card + 1 : ℝ)) *
        interaction (maskedGame v mask) (T ∪ S) := by
  exact factorialShapleyInteraction_eq_dividends _ _ _ (subset_univ _)

theorem shapley_taylor {X : Type*} {n : ℕ} (v : X → ℝ)
    (mask : Finset (Fin n) → X) (T : Finset (Fin n)) (k : ℕ) (hk : 0 < k) :
    shapleyTaylor (maskedGame v mask) univ k T =
      if T.card < k then interaction (maskedGame v mask) T
      else if T.card = k then
        ∑ S ∈ (univ \ T).powerset, (1 / ((S.card + k).choose k : ℝ)) *
          interaction (maskedGame v mask) (T ∪ S)
      else 0 := by
  exact shapleyTaylor_eq_dividends _ _ _ (subset_univ _) k hk

noncomputable def andTrigger {α : Type*} [DecidableEq α] (A T : Finset α) : ℝ :=
  if A ⊆ T then 1 else 0

theorem andTrigger_union {α : Type*} [DecidableEq α] (A B T : Finset α) :
    andTrigger (A ∪ B) T = andTrigger A T * andTrigger B T := by
  by_cases ha : A ⊆ T <;> by_cases hb : B ⊆ T <;>
    simp [andTrigger, union_subset_iff, ha, hb]

theorem andTrigger_product {α : Type*} [DecidableEq α] (A T : Finset α) :
    andTrigger A T = ∏ i ∈ A, if i ∈ T then (1 : ℝ) else 0 := by
  induction A using Finset.induction_on with
  | empty => simp [andTrigger]
  | @insert i A hi ih =>
    rw [prod_insert hi, ← ih]
    by_cases hiT : i ∈ T <;> by_cases hAT : A ⊆ T <;>
      simp [andTrigger, insert_subset_iff, hiT, hAT]

/-- The full finite child-family rule, with overlapping coalitions permitted. -/
theorem andTrigger_children {α β : Type*} [DecidableEq α]
    (children : Finset β) (vars : β → Finset α) (T : Finset α) :
    andTrigger (children.biUnion vars) T = ∏ c ∈ children, andTrigger (vars c) T := by
  classical
  induction children using Finset.induction_on with
  | empty => simp [andTrigger]
  | @insert c children hc ih =>
    rw [biUnion_insert, prod_insert hc, andTrigger_union, ih]

noncomputable def causalOutput {α : Type*} [DecidableEq α]
    (d : Game α) (Ω : Finset (Finset α)) (T : Finset α) : ℝ :=
  ∑ A ∈ Ω, d A * andTrigger A T

theorem causalOutput_eq_sum_subset {α : Type*} [DecidableEq α]
    (d : Game α) (Ω : Finset (Finset α)) (T : Finset α) :
    causalOutput d Ω T = ∑ A ∈ Ω.filter (fun A => A ⊆ T), d A := by
  classical
  simp [causalOutput, andTrigger, Finset.sum_filter, mul_ite]

/-- Replacing every original pattern by any correct finite child grouping preserves the root sum. -/
theorem causalOutput_regrouped {α β : Type*} [DecidableEq α]
    (d : Game α) (Ω : Finset (Finset α)) (children : Finset α → Finset β)
    (vars : β → Finset α) (h : ∀ A ∈ Ω, (children A).biUnion vars = A) (T : Finset α) :
    (∑ A ∈ Ω, d A * ∏ c ∈ children A, andTrigger (vars c) T) = causalOutput d Ω T := by
  unfold causalOutput
  apply sum_congr rfl
  intro A hA
  rw [← andTrigger_children, h A hA]

theorem causalOutput_full {α : Type*} [DecidableEq α] (g : Game α)
    (N T : Finset α) (hTN : T ⊆ N) :
    causalOutput (interaction g) N.powerset T = g T := by
  unfold causalOutput andTrigger
  have hterm : ∀ A : Finset α,
      interaction g A * (if A ⊆ T then (1 : ℝ) else 0) =
        if A ⊆ T then interaction g A else 0 := by intro A; split_ifs <;> simp
  simp_rw [hterm]
  rw [← sum_powerset_extend N T hTN]
  exact Harsanyi.reconstruction g T

theorem complete_unfaithfulness_zero {X : Type*} {n : ℕ} (v : X → ℝ)
    (mask : Finset (Fin n) → X) :
    (∑ S ∈ (univ : Finset (Fin n)).powerset,
      (v (mask S) - ∑ A ∈ S.powerset, interaction (maskedGame v mask) A)^2) = 0 := by
  simp [FullCvpr.reconstruction]

/-- Exact one-coordinate counterexample to the truncated-loss interpretation. -/
theorem baseline_truncated_loss_counterexample (r : ℝ) :
    (∑ S ∈ ({(0 : Fin 1)} : Finset (Fin 1)).powerset,
      (maskCoordinates (fun _ => r) (fun _ => (1 : ℝ)) S 0 -
        causalOutput
          (interaction (fun U => maskCoordinates (fun _ => r) (fun _ => (1 : ℝ)) U 0))
          {∅} S)^2) = (1 - r)^2 := by
  have hp : ({(0 : Fin 1)} : Finset (Fin 1)).powerset = {∅, {0}} := by decide
  rw [hp]
  simp [causalOutput, andTrigger, maskCoordinates]

theorem interaction_finite_sum {α ι : Type*} [DecidableEq α]
    (P : Finset ι) (gs : ι → Game α) (S : Finset α) :
    interaction (fun U => ∑ a ∈ P, gs a U) S = ∑ a ∈ P, interaction (gs a) S := by
  unfold interaction
  simp_rw [mul_sum]
  exact sum_comm

theorem addmul_interactions {α : Type*} [DecidableEq α] (P : Finset (Finset α))
    (d : Game α) (B : Finset α) :
    interaction (fun S => ∑ A ∈ P, unanimity A (d A) S) B = if B ∈ P then d B else 0 := by
  rw [interaction_finite_sum]
  simp [interaction_unanimity, Finset.sum_ite_eq]

/-- The actual zero-baseline coordinate monomial is a unanimity response after masking. -/
theorem masked_monomial {α : Type*} [DecidableEq α] (x : α → ℝ) (A S : Finset α) (c : ℝ) :
    c * (∏ i ∈ A, maskCoordinates (fun _ => 0) x S i) =
      unanimity A (c * ∏ i ∈ A, x i) S := by
  have he (i : α) : maskCoordinates (fun _ => (0 : ℝ)) x S i =
      x i * (if i ∈ S then (1 : ℝ) else 0) := by
    by_cases hi : i ∈ S <;> simp [maskCoordinates, hi]
  simp_rw [he]
  rw [prod_mul_distrib, ← andTrigger_product]
  by_cases hAS : A ⊆ S <;> simp [unanimity, andTrigger, hAS]

noncomputable def coordinatePolynomial {α : Type*} [DecidableEq α]
    (P : Finset (Finset α)) (c : Game α) (x : α → ℝ) : ℝ :=
  ∑ A ∈ P, c A * ∏ i ∈ A, x i

/-- A coordinate/model bridge, not an assumption that the desired masked game is already known. -/
theorem addmul_coordinate_adapter {α : Type*} [DecidableEq α] (P : Finset (Finset α))
    (c : Game α) (x : α → ℝ) (B : Finset α) :
    interaction (fun S => coordinatePolynomial P c (maskCoordinates (fun _ => 0) x S)) B =
      if B ∈ P then c B * (∏ i ∈ B, x i) else 0 := by
  have he : (fun S => coordinatePolynomial P c (maskCoordinates (fun _ => 0) x S)) =
      (fun S => ∑ A ∈ P, unanimity A (c A * ∏ i ∈ A, x i) S) := by
    funext S
    unfold coordinatePolynomial
    apply sum_congr rfl
    intro A _
    exact masked_monomial x A S (c A)
  rw [he]
  exact addmul_interactions P (fun A => c A * ∏ i ∈ A, x i) B

/-- A refutation of the exact empty-inclusive CVPR dummy statement; not its repair. -/
theorem dummy_statement_counterexample :
    ∃ g : Game (Fin 1),
      (∀ S ⊆ ({(0 : Fin 1)} : Finset (Fin 1)).erase 0,
        g (insert 0 S) = g S + g {0}) ∧ interaction g {0} ≠ 0 := by
  refine ⟨unanimity {(0 : Fin 1)} 1, ?_, ?_⟩
  · intro S hS
    have he : S = ∅ := by simpa using hS
    subst S
    simp [unanimity]
  · norm_num [interaction_singleton, unanimity]

end FullCvpr
