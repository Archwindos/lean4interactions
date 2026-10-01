import Lean.Util.CollectAxioms
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


namespace FullGeneralizable
open Harsanyi Finset

theorem and_mask_zero {n : ℕ} (v : (Fin n → ℝ) → ℝ) (r x : Fin n → ℝ)
    (T S : Finset (Fin n)) (hST : ¬ S ⊆ T) :
    interaction (conditionalCoordinateGame v r x T) S = 0 := by
  exact and_mask_interaction_zero v r x T S hST

theorem or_duality {n : ℕ} (v : (Fin n → ℝ) → ℝ) (r x : Fin n → ℝ)
    (S : Finset (Fin n)) (hS : S ≠ ∅) :
    orInteraction (fun L => v (maskCoordinates r x L)) univ S =
      -interaction (fun L => v (maskCoordinates r x (univ \ L))) S := by
  exact or_dual _ _ _ hS

theorem exact_and_reconstruction {n : ℕ} (v : (Fin n → ℝ) → ℝ)
    (r x : Fin n → ℝ) (T : Finset (Fin n)) :
    (∑ S ∈ T.powerset, interaction (fun L => v (maskCoordinates r x L)) S) =
      v (maskCoordinates r x T) := by
  exact reconstruction _ _

theorem literal_and_reconstruction {n : ℕ} (vand : (Fin n → ℝ) → ℝ)
    (r x : Fin n → ℝ) (T : Finset (Fin n)) :
    (∑ S ∈ T.powerset, interaction (conditionalCoordinateGame vand r x T) S) =
      vand (maskCoordinates r x T) := by
  rw [← reconstruct, reconstruction]
  simp [conditionalCoordinateGame, maskCoordinates_idempotent]

theorem literal_and_coefficient_eq {n : ℕ} (v : (Fin n → ℝ) → ℝ)
    (r x : Fin n → ℝ) (T S : Finset (Fin n)) (hST : S ⊆ T) :
    interaction (conditionalCoordinateGame v r x T) S =
      interaction (fun L => v (maskCoordinates r x L)) S := by
  apply interaction_congr
  intro L hLS
  have hLT : L ⊆ T := hLS.trans hST
  simp only [conditionalCoordinateGame, maskCoordinates_comp, inter_eq_right.mpr hLT]

theorem literal_or_reconstruction {n : ℕ} (vor : (Fin n → ℝ) → ℝ)
    (r x : Fin n → ℝ) (T : Finset (Fin n)) :
    orInteraction (conditionalCoordinateGame vor r x T) univ ∅ +
      (∑ S ∈ (univ : Finset (Fin n)).powerset.filter (fun S => ¬ Disjoint S T),
        orInteraction (conditionalCoordinateGame vor r x T) univ S) =
      vor (maskCoordinates r x T) := by
  change orReconstruction (conditionalCoordinateGame vor r x T) univ T = _
  rw [or_reconstruction _ _ _ (subset_univ _)]
  simp [conditionalCoordinateGame, maskCoordinates_idempotent]

theorem literal_or_nonempty_sum {n : ℕ} (vor : (Fin n → ℝ) → ℝ)
    (r x : Fin n → ℝ) (T : Finset (Fin n)) :
    (∑ S ∈ (univ : Finset (Fin n)).powerset.filter (fun S => ¬ Disjoint S T),
        orInteraction (conditionalCoordinateGame vor r x T) univ S) =
      vor (maskCoordinates r x T) - vor (maskCoordinates r x ∅) := by
  have h := literal_or_reconstruction vor r x T
  have hbase : orInteraction (conditionalCoordinateGame vor r x T) univ ∅ =
      vor (maskCoordinates r x ∅) := by
    simp [orInteraction, conditionalCoordinateGame, maskCoordinates_comp]
  rw [hbase] at h
  linarith

/-- The original parent Theorem 2, retaining coefficients conditioned on x_T. -/
theorem literal_and_or_reconstruction {n : ℕ} (v vand vor : (Fin n → ℝ) → ℝ)
    (r x : Fin n → ℝ)
    (h : ∀ U, v (maskCoordinates r x U) =
      vand (maskCoordinates r x U) + vor (maskCoordinates r x U)) (T : Finset (Fin n)) :
    v (maskCoordinates r x T) =
      (∑ S ∈ T.powerset, interaction (conditionalCoordinateGame vand r x T) S) +
      (orInteraction (conditionalCoordinateGame vor r x T) univ ∅ +
        ∑ S ∈ (univ : Finset (Fin n)).powerset.filter (fun S => ¬ Disjoint S T),
          orInteraction (conditionalCoordinateGame vor r x T) univ S) := by
  rw [literal_and_reconstruction, literal_or_reconstruction, h T]

noncomputable def bit (a : Bool) : ℝ := if a then 1 else 0

theorem boolean_or_additive (a b : Bool) :
    bit (a || b) = bit a + bit b - bit (a && b) := by
  cases a <;> cases b <;> norm_num [bit]

theorem boolean_decomposition (a b c d e : Bool) :
    bit (a && b && c) + bit (b && c) + bit (c && d) + bit (d || e) =
      bit (a && b && c) + bit (b && c) + bit (c && d) + bit d + bit e - bit (d && e) := by
  rw [boolean_or_additive]
  ring

theorem shapley {n : ℕ} (v : (Fin n → ℝ) → ℝ) (r x : Fin n → ℝ) (i : Fin n) :
    factorialShapley (fun S => v (maskCoordinates r x S)) univ i =
      ∑ S ∈ (univ : Finset (Fin n)).powerset,
        if i ∈ S then interaction (fun L => v (maskCoordinates r x L)) S / S.card else 0 := by
  exact factorialShapley_eq_dividendAllocation _ _ _ (mem_univ _)

theorem mask_count (n : ℕ) :
    ((univ : Finset (Fin n)).powerset).card = 2 ^ n := by simp

end FullGeneralizable

open Lean Elab Command Meta
set_option pp.universes true
set_option pp.fullNames true
set_option pp.piBinderTypes true
run_cmd liftTermElabM do
  for name in #[`Harsanyi.higherMarginal, `Harsanyi.reconstruct_union_disjoint, `Harsanyi.higherMarginal_eq_sum_interaction, `Harsanyi.interaction_symmetry, `Harsanyi.interaction_context_difference, `Harsanyi.interaction_additive_dummy_nonempty, `Harsanyi.factorial_powerset_sum, `Harsanyi.sum_supersets_eq_sum_complement, `Harsanyi.factorialWeight, `Harsanyi.factorialWeight_superset_sum, `Harsanyi.sum_powerset_extend, `Harsanyi.weighted_higherMarginal_eq, `Harsanyi.factorial_ratio_eq_choose_inv, `Harsanyi.factorialWeight_one, `Harsanyi.factorialWeight_eq_inv_choose, `Harsanyi.factorialShapley, `Harsanyi.factorialShapleyInteraction, `Harsanyi.shapleyTaylor, `Harsanyi.factorialShapley_eq_dividends, `Harsanyi.factorialShapleyInteraction_eq_dividends, `Harsanyi.shapleyTaylor_eq_dividends, `Harsanyi.dividendAllocation_eq_insert_sum, `Harsanyi.factorialShapley_eq_dividendAllocation, `Harsanyi.orInteraction, `Harsanyi.orReconstruction, `Harsanyi.activated_subset_sum, `Harsanyi.or_reconstruction, `Harsanyi.or_dual, `Harsanyi.maskCoordinates, `Harsanyi.maskCoordinates_comp, `Harsanyi.maskCoordinates_idempotent, `Harsanyi.maskCoordinates_insert_absent, `Harsanyi.conditionalCoordinateGame, `Harsanyi.and_mask_interaction_zero, `Harsanyi.maskCoordinates_complement, `Harsanyi.orUnanimity, `Harsanyi.orInteraction_unanimity, `FullCvpr.maskedGame, `FullCvpr.reconstruction, `FullCvpr.uniqueness, `FullCvpr.linearity, `FullCvpr.symmetry, `FullCvpr.anonymity, `FullCvpr.recursive, `FullCvpr.interaction_distribution, `FullCvpr.marginal_decomposition, `FullCvpr.shapley, `FullCvpr.shapley_interaction, `FullCvpr.shapley_taylor, `FullCvpr.andTrigger, `FullCvpr.andTrigger_union, `FullCvpr.andTrigger_product, `FullCvpr.andTrigger_children, `FullCvpr.causalOutput, `FullCvpr.causalOutput_eq_sum_subset, `FullCvpr.causalOutput_regrouped, `FullCvpr.causalOutput_full, `FullCvpr.complete_unfaithfulness_zero, `FullCvpr.baseline_truncated_loss_counterexample, `FullCvpr.interaction_finite_sum, `FullCvpr.addmul_interactions, `FullCvpr.masked_monomial, `FullCvpr.coordinatePolynomial, `FullCvpr.addmul_coordinate_adapter, `FullCvpr.dummy_statement_counterexample, `FullGeneralizable.and_mask_zero, `FullGeneralizable.or_duality, `FullGeneralizable.exact_and_reconstruction, `FullGeneralizable.literal_and_reconstruction, `FullGeneralizable.literal_and_coefficient_eq, `FullGeneralizable.literal_or_reconstruction, `FullGeneralizable.literal_or_nonempty_sum, `FullGeneralizable.literal_and_or_reconstruction, `FullGeneralizable.bit, `FullGeneralizable.boolean_or_additive, `FullGeneralizable.boolean_decomposition, `FullGeneralizable.shapley, `FullGeneralizable.mask_count, `Harsanyi.interaction, `Harsanyi.reconstruct, `Harsanyi.centered, `Harsanyi.marginal, `Harsanyi.interaction_empty, `Harsanyi.reconstruct_empty, `Harsanyi.centered_empty, `Harsanyi.interaction_congr, `Harsanyi.interaction_singleton, `Harsanyi.interaction_insert, `Harsanyi.reconstruction, `Harsanyi.interaction_reconstruct, `Harsanyi.reconstruction_unique, `Harsanyi.interaction_injective, `Harsanyi.interaction_add, `Harsanyi.interaction_sub, `Harsanyi.interaction_smul, `Harsanyi.interaction_zero, `Harsanyi.interaction_const, `Harsanyi.interaction_centered, `Harsanyi.interaction_centered_nonempty, `Harsanyi.interaction_recursive, `Harsanyi.unanimity, `Harsanyi.reconstruct_single, `Harsanyi.interaction_unanimity, `Harsanyi.interaction_dummy, `Harsanyi.interaction_relabel, `Harsanyi.dividendAllocation, `Harsanyi.dividendAllocation_add, `Harsanyi.sum_dividend_shares, `Harsanyi.dividendAllocation_efficiency, `Harsanyi.dividendAllocation_centered, `Harsanyi.dividendAllocation_unanimity] do
    let info ← getConstInfo name
    let signature ← ppExpr info.type
    let axioms ← Lean.collectAxioms name
    let deps := info.type.getUsedConstants ++ (info.value?.map Expr.getUsedConstants).getD #[]
    let kind := match info with | .thmInfo _ => "theorem" | _ => "definition"
    liftM <| IO.println ("FINITE_API:" ++ (Json.mkObj [
      ("name", toJson name.toString), ("signature", toJson signature.pretty),
      ("kind", toJson kind), ("axioms", toJson (axioms.map Name.toString)),
      ("dependencies", toJson (deps.map Name.toString))]).compress)

