import Lean.Util.CollectAxioms
import Harsanyi.Extensions.HarsanyiNetwork
namespace PaperHarsanyiNet
open Finset Harsanyi
variable {α β : Type*} [DecidableEq α]
noncomputable def model (J : Finset β) (w : β → ℝ) (e : β → Network.Expr α)
    (r y : α → ℝ) : ℝ := ∑ j ∈ J, w j * Network.value r y (e j)
/-- All masked outputs are exactly the architecture game, including the empty mask. -/
theorem masked_output (J : Finset β) (w : β → ℝ) (e : β → Network.Expr α)
    (r x : α → ℝ) (T : Finset α) :
    model J w e r (maskCoordinates r x T) =
      ∑ j ∈ J, w j * Network.unitGame (e j) r x T := rfl
/-- The original V and I are centered; this adapter does not assume zero raw baseline. -/
theorem centered_readout (J : Finset β) (w : β → ℝ) (e : β → Network.Expr α)
    (r x : α → ℝ) (S : Finset α) :
    interaction (centered (fun T => model J w e r (maskCoordinates r x T))) S =
      ∑ j ∈ J, w j * interaction (centered (Network.unitGame (e j) r x)) S :=
  Network.interaction_weighted_sum J w (fun j => Network.unitGame (e j) r x) S
/-- Actual masks and classical factorial Shapley, with fields computed by the graph. -/
theorem exact_forward_attribution (J : Finset β) (w : β → ℝ)
    (e : β → Network.Expr α) (r x : α → ℝ) (N : Finset α) (i : α)
    (hi : i ∈ N) (hR : ∀ j ∈ J, Network.receptive (e j) ⊆ N) :
    factorialShapley (fun T => model J w e r (maskCoordinates r x T)) N i =
      ∑ j ∈ J, if i ∈ Network.receptive (e j)
        then w j * Network.value r x (e j) / (Network.receptive (e j)).card else 0 :=
  Network.forward_shapley J w e r x N i hi hR
/-- F.8 masks outside Q keep the original input, not the original baseline. -/
theorem conditional_attribution (J : Finset β) (w : β → ℝ)
    (e : β → Network.Expr α) (r x : α → ℝ) (N Q : Finset α) (i : α)
    (hi : i ∈ Q) (hR : ∀ j ∈ J, Network.receptive (e j) ⊆ N) :
    factorialShapley (fun T => model J w e r (maskCoordinates r x (T ∪ (N \ Q)))) Q i =
      ∑ j ∈ J, if i ∈ Network.receptive (e j) ∩ Q then
        w j * Network.value r x (e j) / (Network.receptive (e j) ∩ Q).card else 0 := by
  exact Network.conditional_forward_shapley J w (fun j => Network.value r x (e j))
    (fun j => Network.receptive (e j)) (fun j => Network.unitGame (e j) r x) N Q i hi hR
    (by intro j _ T; exact Network.value_mask (e j) r x T)

/-- The original finite R1/R2 premise; all masks live in Fin n, not a larger ambient type. -/
theorem finite_requirements_attribution {n : ℕ} (J : Finset β) (w c : β → ℝ)
    (R : β → Finset (Fin n)) (u : β → Game (Fin n)) (i : Fin n)
    (hu : ∀ j ∈ J, ∀ T ⊆ (univ : Finset (Fin n)),
      u j T = if R j ⊆ T then c j else 0) :
    factorialShapley (fun T => ∑ j ∈ J, w j * u j T) univ i =
      ∑ j ∈ J, if i ∈ R j then w j * c j / (R j).card else 0 :=
  Network.requirement_forward_shapley J w c R u univ i (mem_univ i)
    (by intro j _; exact subset_univ _) (by intro j hj T; exact hu j hj T (subset_univ T))

/-- Original finite mask-domain support count, with no global-law assumption added. -/
theorem finite_support_card {n : ℕ} [DecidableEq β] (J : Finset β)
    (w c : β → ℝ) (R : β → Finset (Fin n)) (u : β → Game (Fin n))
    (hu : ∀ j ∈ J, ∀ T ⊆ (univ : Finset (Fin n)),
      u j T = if R j ⊆ T then c j else 0) :
    (univ.powerset.filter (fun S => interaction (centered (fun T =>
      ∑ j ∈ J, w j * u j T)) S ≠ 0)).card ≤ J.card :=
  Network.support_card_le_units J w c R u
    (by intro j hj T; exact hu j hj T (subset_univ T)) univ

/-- Original F.8 finite domain: the players outside Q stay fixed at the full input. -/
theorem finite_conditional_attribution {n : ℕ} (J : Finset β) (w c : β → ℝ)
    (R : β → Finset (Fin n)) (u : β → Game (Fin n)) (Q : Finset (Fin n)) (i : Fin n)
    (hi : i ∈ Q) (hu : ∀ j ∈ J, ∀ T ⊆ (univ : Finset (Fin n)),
      u j T = if R j ⊆ T then c j else 0) :
    factorialShapley (fun T => ∑ j ∈ J, w j * u j (T ∪ (univ \ Q))) Q i =
      ∑ j ∈ J, if i ∈ R j ∩ Q then w j * c j / (R j ∩ Q).card else 0 :=
  Network.conditional_forward_shapley J w c R u univ Q i hi
    (by intro j _; exact subset_univ _) (by intro j hj T; exact hu j hj T (subset_univ T))

/-- The classical factorial definition inherits additive linearity from the proved bridge. -/
theorem shapley_add (a b : Game α) (N : Finset α) (i : α) (hi : i ∈ N) :
    factorialShapley (fun T => a T + b T) N i = factorialShapley a N i + factorialShapley b N i := by
  simp_rw [factorialShapley_eq_dividendAllocation _ _ _ hi]
  exact dividendAllocation_add a b N i

theorem shapley_scale (a : Game α) (c : ℝ) (N : Finset α) (i : α) :
    factorialShapley (fun T => c * a T) N i = c * factorialShapley a N i := by
  unfold factorialShapley
  rw [Finset.mul_sum]
  apply sum_congr rfl
  intro T _
  ring

/-- The actual classical formula, not efficiency of an allocation merely by definition. -/
theorem shapley_efficiency (a : Game α) (N : Finset α) :
    (∑ i ∈ N, factorialShapley a N i) = a N - a ∅ := by
  have h : (∑ i ∈ N, factorialShapley a N i) = ∑ i ∈ N, dividendAllocation a N i := by
    apply sum_congr rfl; intro i hi; exact factorialShapley_eq_dividendAllocation a N i hi
  rw [h,dividendAllocation_efficiency]

/-- Exact original dummy premise on the finite centered game. -/
theorem shapley_dummy (a : Game α) (N : Finset α) (i : α) (hi : i ∈ N)
    (h0 : a ∅ = 0) (hd : ∀ T ⊆ N.erase i, a (insert i T) = a T + a {i}) :
    factorialShapley a N i = a {i} := by
  rw [factorialShapley_eq_dividends a N i hi]
  have he : ∀ S ∈ (N.erase i).powerset,
      (1 / (S.card + 1 : ℝ)) * interaction a (insert i S) =
        if S = ∅ then a {i} else 0 := by
    intro S hS
    by_cases hs : S = ∅
    · subst S; simp [interaction_singleton,h0]
    · have hSN := mem_powerset.mp hS
      have hnot : i ∉ S := fun h => (mem_erase.mp (hSN h)).1 rfl
      rw [interaction_additive_dummy_nonempty a S i hnot
        (nonempty_iff_ne_empty.mpr hs) (a {i})
        (by intro T hTS; exact hd T (hTS.trans hSN))]
      simp [hs]
  rw [sum_congr rfl he]
  simp

/-- Original classical symmetry, proved from its exact finite-domain premise. -/
theorem shapley_symmetry (a : Game α) (N : Finset α) (i j : α)
    (hi : i ∈ N) (hj : j ∈ N)
    (hSym : ∀ T ⊆ N \ {i,j}, a (insert i T) = a (insert j T)) :
    factorialShapley a N i = factorialShapley a N j := by
  by_cases hij : i = j
  · subst j; rfl
  have hji := Ne.symm hij
  let R := (N.erase i).erase j
  have hRi : i ∉ R := by simp [R]
  have hRj : j ∉ R := by simp [R]
  have hNi : N.erase i = insert j R := by
    symm
    exact insert_erase (mem_erase.mpr ⟨hji,hj⟩)
  have hNj : N.erase j = insert i R := by
    dsimp [R]
    have he : (N.erase i).erase j = (N.erase j).erase i := by
      ext k; simp only [mem_erase]; tauto
    rw [he]
    symm
    exact insert_erase (mem_erase.mpr ⟨hij,hi⟩)
  have hRN : R = N \ {i,j} := by ext k; simp [R]; tauto
  unfold factorialShapley
  rw [hNi,hNj,sum_powerset_insert hRj,sum_powerset_insert hRi,
    ← sum_add_distrib,← sum_add_distrib]
  apply sum_congr rfl
  intro T hT
  have hTR := mem_powerset.mp hT
  have hiT : i ∉ T := fun h => hRi (hTR h)
  have hjT : j ∉ T := fun h => hRj (hTR h)
  have he := hSym T (by simpa [← hRN] using hTR)
  simp only [card_insert_of_notMem hiT,card_insert_of_notMem hjT]
  rw [he,insert_comm i j]
end PaperHarsanyiNet




open Lean Elab Command Meta
set_option pp.universes true
set_option pp.fullNames true
set_option pp.piBinderTypes true
run_cmd liftTermElabM do
  for name in #[`Harsanyi.Network.Expr, `Harsanyi.Network.receptive, `Harsanyi.Network.value, `Harsanyi.Network.value_congr, `Harsanyi.Network.value_mask, `Harsanyi.Network.value_baseline, `Harsanyi.Network.value_empty_receptive, `Harsanyi.Network.unitGame, `Harsanyi.Network.unitGame_eq_unanimity, `Harsanyi.Network.unit_interaction, `Harsanyi.Network.interaction_sum, `Harsanyi.Network.interaction_weighted_sum, `Harsanyi.Network.requirement_unit_interaction, `Harsanyi.Network.requirement_forward_shapley, `Harsanyi.Network.support_subset_fields, `Harsanyi.Network.support_card_le_units, `Harsanyi.Network.conditional_receptive, `Harsanyi.Network.conditional_forward_shapley, `Harsanyi.Network.forward_shapley, `Harsanyi.Network.receptive_shared_children, `Harsanyi.Network.channel_grouping, `Harsanyi.Network.groupedBlock, `Harsanyi.Network.groupedBlock_mask, `Harsanyi.Network.scalar_grouped_gate_counterexample, `Harsanyi.Network.empty_unit_counterexample, `PaperHarsanyiNet.model, `PaperHarsanyiNet.masked_output, `PaperHarsanyiNet.centered_readout, `PaperHarsanyiNet.exact_forward_attribution, `PaperHarsanyiNet.conditional_attribution, `PaperHarsanyiNet.finite_requirements_attribution, `PaperHarsanyiNet.finite_support_card, `PaperHarsanyiNet.finite_conditional_attribution, `PaperHarsanyiNet.shapley_add, `PaperHarsanyiNet.shapley_scale, `PaperHarsanyiNet.shapley_efficiency, `PaperHarsanyiNet.shapley_dummy, `PaperHarsanyiNet.shapley_symmetry, `Harsanyi.reconstruction, `Harsanyi.interaction_recursive, `Harsanyi.factorialShapley, `Harsanyi.factorialShapley_eq_dividendAllocation] do
    let info ← getConstInfo name
    let signature ← ppExpr info.type
    let axioms ← Lean.collectAxioms name
    let deps := info.type.getUsedConstants ++ (info.value?.map Expr.getUsedConstants).getD #[]
    let kind := match info with | .thmInfo _ => "theorem" | .inductInfo _ => "inductive" | _ => "definition"
    liftM <| IO.println ("NETWORK_API:" ++ (Json.mkObj [
      ("name", toJson name.toString), ("signature", toJson signature.pretty),
      ("kind", toJson kind), ("axioms", toJson (axioms.map Name.toString)),
      ("dependencies", toJson (deps.map Name.toString))]).compress)
