import Harsanyi.Extensions.HarsanyiNetwork
import Harsanyi.Extensions.CoalitionAttribution
import Mathlib.Data.Nat.Choose.Basic

namespace Harsanyi.Layerwise
open Finset
variable {α : Type*} [DecidableEq α]

noncomputable def andComponent (g γ : Game α) : Game α := fun S => g S / 2 + γ S
noncomputable def orComponent (g γ : Game α) : Game α := fun S => g S / 2 - γ S

theorem component_sum (g γ : Game α) (S : Finset α) :
    andComponent g γ S + orComponent g γ S = g S := by
  unfold andComponent orComponent
  ring

/-- The specified split fixes the empty AND dividend and the empty OR baseline. -/
theorem component_empty (g γ : Game α) (hγ : γ ∅ = g ∅ / 2) :
    andComponent g γ ∅ = g ∅ ∧ orComponent g γ ∅ = 0 := by
  simp only [andComponent, orComponent, hγ]
  constructor <;> ring

/-- Exact fixed-game matching, including T=∅ and a nonzero output baseline. -/
theorem and_or_matching (g γ : Game α) (N T : Finset α) (hTN : T ⊆ N)
    (hγ : γ ∅ = g ∅ / 2) :
    g T = (∑ S ∈ T.powerset, interaction (andComponent g γ) S) +
      ∑ S ∈ N.powerset.filter (fun S => ¬ Disjoint S T),
        orInteraction (orComponent g γ) N S := by
  have ho := or_reconstruction (orComponent g γ) N T hTN
  have hempty := (component_empty g γ hγ).2
  have hzero : orInteraction (orComponent g γ) N ∅ = 0 := by
    simp [orInteraction, hempty]
  change orInteraction (orComponent g γ) N ∅ + _ = _ at ho
  rw [hzero, zero_add] at ho
  rw [← reconstruct, reconstruction, ho]
  exact (component_sum g γ T).symm

/-- Repeated masks use intersection; this is a different OR game from the fixed one. -/
noncomputable def restricted (g : Game α) (T : Finset α) : Game α :=
  fun L => g (T ∩ L)

theorem conditional_and_or_matching (g γ : Game α) (N T : Finset α)
    (hTN : T ⊆ N) (hγ : γ ∅ = g ∅ / 2) :
    g T =
      (∑ S ∈ T.powerset, interaction (andComponent (restricted g T) (restricted γ T)) S) +
      ∑ S ∈ N.powerset.filter (fun S => ¬ Disjoint S T),
        orInteraction (orComponent (restricted g T) (restricted γ T)) N S := by
  simpa [restricted] using and_or_matching (restricted g T) (restricted γ T) N T hTN
    (by simpa [restricted] using hγ)

/-- Appendix B, starting from the classical factorial marginal definition. -/
theorem shapley_and_or (g γ : Game α) (N : Finset α) (i : α) (hi : i ∈ N) :
    factorialShapley g N i =
      ∑ S ∈ N.powerset, if i ∈ S then
        (interaction (andComponent g γ) S + orInteraction (orComponent g γ) N S) / S.card
        else 0 := by
  have hsplit : g = fun S => andComponent g γ S + orComponent g γ S := by
    funext S; exact (component_sum g γ S).symm
  conv_lhs => rw [hsplit]
  exact Coalition.shapley_and_or (andComponent g γ) (orComponent g γ) N i hi

/-- The local AND coefficients agree for retained coalitions. -/
theorem restricted_and (g : Game α) (T S : Finset α) (hST : S ⊆ T) :
    interaction (restricted g T) S = interaction g S := by
  apply interaction_congr
  intro L hLS
  simp [restricted, inter_eq_right.mpr (hLS.trans hST)]

/-- Equality of the numbers of complementary orders, the main-text comparison. -/
theorem complementary_order_count (n m : ℕ) (hm : m ≤ n) :
    n.choose m = n.choose (n - m) := (Nat.choose_symm hm).symm

/-- First-order OR/AND terms have the same activation indicator. -/
theorem singleton_activation (i : α) (T : Finset α) :
    ¬ Disjoint ({i} : Finset α) T ↔ i ∈ T := by simp

theorem singleton_merge (a o : ℝ) (i : α) (T : Finset α) :
    (if ({i} : Finset α) ⊆ T then a else 0) +
      (if ¬ Disjoint ({i} : Finset α) T then o else 0) =
      if i ∈ T then a + o else 0 := by
  by_cases h : i ∈ T <;> simp [h]

/-- A one-element pure OR game equals the corresponding pure AND game. -/
theorem orUnanimity_singleton (i : α) (c : ℝ) :
    orUnanimity ({i} : Finset α) c = unanimity {i} c := by
  funext S
  by_cases h : i ∈ S <;> simp [orUnanimity, unanimity, h]

/-- A same-sign shared scalar has no cancellation in the remaining magnitude. -/
noncomputable def shared (a b : ℝ) : ℝ :=
  if 0 ≤ a ∧ 0 ≤ b then min a b
  else if a ≤ 0 ∧ b ≤ 0 then -min (-a) (-b) else 0

theorem scalar_strength_decomposition (a b : ℝ) :
    |a| = |shared a b| + |a - shared a b| := by
  unfold shared
  split_ifs with hpos hneg
  · rcases hpos with ⟨ha, hb⟩
    have hs : 0 ≤ min a b := le_min ha hb
    have hr : 0 ≤ a - min a b := sub_nonneg.mpr (min_le_left _ _)
    rw [abs_of_nonneg ha, abs_of_nonneg hs, abs_of_nonneg hr]
    ring
  · rcases hneg with ⟨ha, hb⟩
    have hs : 0 ≤ min (-a) (-b) := le_min (neg_nonneg.mpr ha) (neg_nonneg.mpr hb)
    have hr : a + min (-a) (-b) ≤ 0 := by have := min_le_left (-a) (-b); linarith
    rw [abs_of_nonpos ha, abs_of_nonpos (neg_nonpos.mpr hs)]
    simp only [sub_neg_eq_add]
    rw [abs_of_nonpos hr]
    ring
  · simp

/-- Counterexample to the printed thresholded Eq.(8), with different supports. -/
theorem thresholded_strength_counterexample :
    (1 : ℝ) ≠ |shared 1 (1/100)| + |1 - shared 1 (1/100)| - |shared 1 (1/100)| := by
  norm_num [shared]

/-- Counterexample to the extra baseline at the first equality of Eq.(19). -/
theorem duplicated_baseline_counterexample :
    (1 : ℝ) ≠ 1 + interaction (fun _ : Finset α => (1 : ℝ)) ∅ := by simp


/-- Two positive singleton dividends on a two-player universe. -/
noncomputable def strengthEffect (a b : ℝ) (S : Finset (Fin 2)) : ℝ :=
  if S = {0} then a else if S = {1} then b else 0

def strengthUniverse : Finset (Fin 2) := {0,1}
noncomputable def strengthGame (a b : ℝ) : Game (Fin 2) :=
  reconstruct (strengthEffect a b)

theorem strengthGame_dividends (a b : ℝ) (S : Finset (Fin 2)) :
    interaction (strengthGame a b) S = strengthEffect a b S :=
  interaction_reconstruct _ S

/-- The paper's 5%-of-maximum threshold; OR effects are identically zero here. -/
noncomputable def significantStrength (a b : ℝ) : Finset (Finset (Fin 2)) :=
  strengthUniverse.powerset.filter (fun S =>
    (1/20 : ℝ) * max |a| |b| < |strengthEffect a b S|)

noncomputable def allStrength (a b : ℝ) : ℝ :=
  ∑ S ∈ significantStrength a b, |strengthEffect a b S|
noncomputable def overlapStrength (a b c d : ℝ) : ℝ :=
  ∑ S ∈ significantStrength a b ∩ significantStrength c d,
    |shared (strengthEffect a b S) (strengthEffect c d S)|
noncomputable def forgetStrength (a b c d : ℝ) : ℝ :=
  ∑ S ∈ significantStrength a b,
    |strengthEffect a b S - shared (strengthEffect a b S) (strengthEffect c d S)|

theorem strength_supports :
    significantStrength (1/2) (1/2) = {{0},{1}} ∧
    significantStrength (1/101) (100/101) = {{1}} := by
  have hn : strengthUniverse.powerset = {∅,{0},{1},{0,1}} := by decide
  have he0 : (∅ : Finset (Fin 2)) ≠ {0} := by decide
  have he1 : (∅ : Finset (Fin 2)) ≠ {1} := by decide
  have he01 : (∅ : Finset (Fin 2)) ≠ {0,1} := by decide
  have h01 : ({0} : Finset (Fin 2)) ≠ {1} := by decide
  have h0u : ({0} : Finset (Fin 2)) ≠ {0,1} := by decide
  have h1u : ({1} : Finset (Fin 2)) ≠ {0,1} := by decide
  norm_num [significantStrength,hn,strengthEffect,Finset.filter_insert,
    Finset.filter_singleton,he0,he1,he01,h01,h0u,h1u,Ne.symm h01,Ne.symm h0u,Ne.symm h1u]

theorem strength_full_outputs :
    strengthGame (1/2) (1/2) strengthUniverse = 1 ∧
    strengthGame (1/101) (100/101) strengthUniverse = 1 := by
  have hn : strengthUniverse.powerset = {∅,{0},{1},{0,1}} := by decide
  have he0 : (∅ : Finset (Fin 2)) ≠ {0} := by decide
  have he1 : (∅ : Finset (Fin 2)) ≠ {1} := by decide
  have he01 : (∅ : Finset (Fin 2)) ≠ {0,1} := by decide
  have h01 : ({0} : Finset (Fin 2)) ≠ {1} := by decide
  have h0u : ({0} : Finset (Fin 2)) ≠ {0,1} := by decide
  have h1u : ({1} : Finset (Fin 2)) ≠ {0,1} := by decide
  norm_num [strengthGame,reconstruct,hn,strengthEffect,Finset.sum_insert,
    Finset.mem_insert,Finset.mem_singleton,he0,he1,he01,h01,h0u,h1u,
    Ne.symm he0,Ne.symm he1,Ne.symm he01,Ne.symm h01,Ne.symm h0u,Ne.symm h1u]

/-- Exact support and metrics, not merely an abstract scalar arithmetic example. -/
theorem normalized_thresholded_counterexample :
    allStrength (1/2) (1/2) = 1 ∧
    overlapStrength (1/2) (1/2) (1/101) (100/101) = 1/2 ∧
    forgetStrength (1/2) (1/2) (1/101) (100/101) = 99/202 ∧
    allStrength (1/2) (1/2) ≠
      overlapStrength (1/2) (1/2) (1/101) (100/101) +
      forgetStrength (1/2) (1/2) (1/101) (100/101) := by
  rw [allStrength,overlapStrength,forgetStrength,
      strength_supports.1,strength_supports.2]
  norm_num [strengthEffect,shared]
end Harsanyi.Layerwise

