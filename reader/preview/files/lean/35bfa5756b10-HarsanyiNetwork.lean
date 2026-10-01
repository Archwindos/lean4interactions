import Harsanyi.Extensions.Attribution
import Harsanyi.Extensions.OrInteraction

/-! Exact finite Harsanyi networks. The syntax unfolds any finite feed-forward DAG
into a finite tree, retaining arbitrary skip connections by repeated subexpressions.
Weights are fixed during inference; there are no biases in a Harsanyi block. -/
namespace Harsanyi.Network
open Finset
variable {α : Type*} [DecidableEq α]

inductive Expr (α : Type*) where
  | input (i : α)
  | block (k : ℕ) (children : Fin k → Expr α) (weight : Fin k → ℝ)

noncomputable def receptive : Expr α → Finset α
  | .input i => {i}
  | .block _ children _ => univ.biUnion (fun j => receptive (children j))

noncomputable def value (r x : α → ℝ) : Expr α → ℝ
  | .input i => x i - r i
  | .block _ children weight =>
      max (if ∀ j, value r x (children j) ≠ 0
        then ∑ j, weight j * value r x (children j) else 0) 0

/-- R1 follows from dependency on the actual selected children. -/
theorem value_congr (e : Expr α) (r x y : α → ℝ)
    (h : ∀ i ∈ receptive e, x i = y i) : value r x e = value r y e := by
  induction e with
  | input i => simp only [receptive, mem_singleton] at h; simp [value, h i rfl]
  | block k children weight ih =>
    have hc : ∀ j, value r x (children j) = value r y (children j) := by
      intro j
      apply ih j
      intro i hi
      exact h i (mem_biUnion.mpr ⟨j, mem_univ j, hi⟩)
    simp only [value, hc]

/-- R2 for every mask, proved recursively from the hard gate, not assumed. -/
theorem value_mask (e : Expr α) (r x : α → ℝ) (S : Finset α) :
    value r (maskCoordinates r x S) e =
      if receptive e ⊆ S then value r x e else 0 := by
  induction e with
  | input i =>
    by_cases hi : i ∈ S <;> simp [value, receptive, maskCoordinates, hi]
  | block k children weight ih =>
    by_cases hRS : receptive (.block k children weight) ⊆ S
    · rw [if_pos hRS]
      apply value_congr
      intro i hi
      simp [maskCoordinates, hRS hi]
    · rw [if_neg hRS]
      obtain ⟨i, hi, hiS⟩ := Finset.not_subset.mp hRS
      obtain ⟨j, _, hij⟩ := mem_biUnion.mp hi
      have hchild : ¬ receptive (children j) ⊆ S := fun h => hiS (h hij)
      have hz : value r (maskCoordinates r x S) (children j) = 0 := by
        rw [ih j, if_neg hchild]
      have hgate : ¬ ∀ j, value r (maskCoordinates r x S) (children j) ≠ 0 := by
        intro hall
        exact hall j hz
      simp [value, hgate]

/-- A bias-free block has zero baseline, including zero selected children. -/
theorem value_baseline (e : Expr α) (r : α → ℝ) : value r r e = 0 := by
  induction e with
  | input i => simp [value]
  | block k children weight ih => simp [value, ih]

/-- Empty receptive fields have zero value in this architecture. -/
theorem value_empty_receptive (e : Expr α) (r x : α → ℝ)
    (h : receptive e = ∅) : value r x e = 0 := by
  rw [← value_baseline e r]
  exact value_congr e r x r (by simp [h])

noncomputable def unitGame (e : Expr α) (r x : α → ℝ) : Game α :=
  fun S => value r (maskCoordinates r x S) e

theorem unitGame_eq_unanimity (e : Expr α) (r x : α → ℝ) :
    unitGame e r x = unanimity (receptive e) (value r x e) := by
  funext S
  exact value_mask e r x S

/-- The actual architecture makes the empty-field boundary valid. -/
theorem unit_interaction (e : Expr α) (r x : α → ℝ) (S : Finset α) :
    interaction (centered (unitGame e r x)) S =
      if S = receptive e then value r x e else 0 := by
  have hz : unitGame e r x ∅ = 0 := by
    simpa [unitGame, maskCoordinates] using value_baseline e r
  rw [interaction_centered, hz]
  simp only [ite_self, sub_zero, unitGame_eq_unanimity, interaction_unanimity]

theorem interaction_sum {β : Type*} (J : Finset β)
    (w : β → ℝ) (u : β → Game α) (S : Finset α) :
    interaction (fun T => ∑ j ∈ J, w j * u j T) S =
      ∑ j ∈ J, w j * interaction (u j) S := by
  unfold interaction
  simp_rw [Finset.mul_sum]
  rw [Finset.sum_comm]
  apply sum_congr rfl
  intro j _
  apply sum_congr rfl
  intro T _
  ring

/-- Finite weighted readouts preserve the centered game convention. -/
theorem interaction_weighted_sum {β : Type*} (J : Finset β)
    (w : β → ℝ) (u : β → Game α) (S : Finset α) :
    interaction (centered (fun T => ∑ j ∈ J, w j * u j T)) S =
      ∑ j ∈ J, w j * interaction (centered (u j)) S := by
  have he : centered (fun T => ∑ j ∈ J, w j * u j T) =
      (fun T => ∑ j ∈ J, w j * centered (u j) T) := by
    funext T
    simp [centered, mul_sub, sum_sub_distrib]
  rw [he, interaction_sum]

/-- Precise general boundary of Lemma 1 under its two stated requirements. -/
theorem requirement_unit_interaction (R : Finset α) (c : ℝ) (u : Game α)
    (h : ∀ T, u T = if R ⊆ T then c else 0) (S : Finset α) :
    interaction (centered u) S =
      if R = ∅ then 0 else if S = R then c else 0 := by
  have hu : u = unanimity R c := by funext T; exact h T
  rw [hu, interaction_centered, interaction_unanimity]
  by_cases hR : R = ∅
  · subst R
    simp [unanimity]
  · have hRe : ¬ R ⊆ (∅ : Finset α) := by simpa using hR
    simp [hR, unanimity, hRe]

/-- Theorem 3 under R1/R2 themselves, with no nonempty-field assumption. -/
theorem requirement_forward_shapley {β : Type*} (J : Finset β) (w c : β → ℝ)
    (R : β → Finset α) (u : β → Game α) (N : Finset α) (i : α)
    (hi : i ∈ N) (hR : ∀ j ∈ J, R j ⊆ N)
    (hu : ∀ j ∈ J, ∀ T, u j T = if R j ⊆ T then c j else 0) :
    factorialShapley (fun T => ∑ j ∈ J, w j * u j T) N i =
      ∑ j ∈ J, if i ∈ R j then w j * c j / (R j).card else 0 := by
  rw [factorialShapley_eq_dividendAllocation _ _ _ hi]
  unfold dividendAllocation
  have hd : ∀ S ∈ N.powerset,
      (if i ∈ S then interaction (fun T => ∑ j ∈ J, w j * u j T) S / S.card else 0) =
        ∑ j ∈ J, if i ∈ S then w j * interaction (u j) S / S.card else 0 := by
    intro S _
    rw [interaction_sum]
    by_cases hiS : i ∈ S <;> simp [hiS, Finset.sum_div]
  rw [sum_congr rfl hd, Finset.sum_comm]
  apply sum_congr rfl
  intro j hj
  have hunit : u j = unanimity (R j) (c j) := by funext T; exact hu j hj T
  simp_rw [hunit, interaction_unanimity]
  have he : ∀ S ∈ N.powerset,
      (if i ∈ S then w j * (if S = R j then c j else 0) / S.card else 0) =
        if S = R j then (if i ∈ R j then w j * c j / (R j).card else 0) else 0 := by
    intro S _
    by_cases h : S = R j <;> simp [h]
  rw [sum_congr rfl he]
  simp [Finset.sum_ite_eq', mem_powerset, hR j hj]

/-- Every nonzero centered dividend has some unit's receptive field. -/
theorem support_subset_fields {β : Type*} [DecidableEq β]
    (J : Finset β) (w c : β → ℝ) (R : β → Finset α) (u : β → Game α)
    (hu : ∀ j ∈ J, ∀ T, u j T = if R j ⊆ T then c j else 0)
    (S : Finset α)
    (hS : interaction (centered (fun T => ∑ j ∈ J, w j * u j T)) S ≠ 0) :
    S ∈ J.image R := by
  by_contra hnot
  apply hS
  rw [interaction_weighted_sum]
  apply sum_eq_zero
  intro j hj
  have hne : S ≠ R j := by intro he; exact hnot (mem_image.mpr ⟨j,hj,he.symm⟩)
  rw [requirement_unit_interaction (R j) (c j) (u j) (hu j hj) S]
  split_ifs <;> simp_all

theorem support_card_le_units {β : Type*} [DecidableEq β]
    (J : Finset β) (w c : β → ℝ) (R : β → Finset α) (u : β → Game α)
    (hu : ∀ j ∈ J, ∀ T, u j T = if R j ⊆ T then c j else 0) (N : Finset α) :
    (N.powerset.filter (fun S => interaction (centered (fun T => ∑ j ∈ J, w j * u j T)) S ≠ 0)).card ≤ J.card := by
  apply le_trans (card_le_card (t := J.image R) ?_) (card_image_le)
  intro S hS
  exact support_subset_fields J w c R u hu S (mem_filter.mp hS).2

/-- Fixing outside variables replaces each receptive field by its selected part. -/
theorem conditional_receptive (R N Q T : Finset α) (hRN : R ⊆ N) :
    R ⊆ T ∪ (N \ Q) ↔ R ∩ Q ⊆ T := by
  constructor
  · intro h i hi
    rcases mem_inter.mp hi with ⟨hiR, hiQ⟩
    rcases mem_union.mp (h hiR) with hiT | hiF
    · exact hiT
    · exact False.elim ((mem_sdiff.mp hiF).2 hiQ)
  · intro h i hiR
    by_cases hiQ : i ∈ Q
    · exact mem_union_left _ (h (mem_inter.mpr ⟨hiR, hiQ⟩))
    · exact mem_union_right _ (mem_sdiff.mpr ⟨hRN hiR, hiQ⟩)

/-- F.8: outside variables stay at the original input, and are not new players. -/
theorem conditional_forward_shapley {β : Type*} (J : Finset β) (w c : β → ℝ)
    (R : β → Finset α) (u : β → Game α) (N Q : Finset α) (i : α)
    (hi : i ∈ Q) (hR : ∀ j ∈ J, R j ⊆ N)
    (hu : ∀ j ∈ J, ∀ T, u j T = if R j ⊆ T then c j else 0) :
    factorialShapley (fun T => ∑ j ∈ J, w j * u j (T ∪ (N \ Q))) Q i =
      ∑ j ∈ J, if i ∈ R j ∩ Q then w j * c j / (R j ∩ Q).card else 0 := by
  apply requirement_forward_shapley J w c (fun j => R j ∩ Q)
    (fun j T => u j (T ∪ (N \ Q))) Q i hi
  · intro j _; exact inter_subset_right
  · intro j hj T
    rw [hu j hj]
    simp only [conditional_receptive _ _ _ _ (hR j hj)]

/-- Shapley values are derived from the factorial marginal definition. -/
theorem forward_shapley {β : Type*} (J : Finset β) (w : β → ℝ)
    (u : β → Expr α) (r x : α → ℝ) (N : Finset α) (i : α)
    (hi : i ∈ N) (hR : ∀ j ∈ J, receptive (u j) ⊆ N) :
    factorialShapley (fun T => ∑ j ∈ J, w j * unitGame (u j) r x T) N i =
      ∑ j ∈ J, if i ∈ receptive (u j)
        then w j * value r x (u j) / (receptive (u j)).card else 0 := by
  rw [factorialShapley_eq_dividendAllocation _ _ _ hi]
  unfold dividendAllocation
  have hs : ∀ S ∈ N.powerset,
      interaction (fun T => ∑ j ∈ J, w j * unitGame (u j) r x T) S =
        ∑ j ∈ J, w j * interaction (unitGame (u j) r x) S := by
    intro S _
    exact interaction_sum J w _ S
  have hd : ∀ S ∈ N.powerset,
      (if i ∈ S then interaction (fun T => ∑ j ∈ J, w j * unitGame (u j) r x T) S / S.card else 0) =
        ∑ j ∈ J, if i ∈ S then w j * interaction (unitGame (u j) r x) S / S.card else 0 := by
    intro S hS
    rw [hs S hS]
    by_cases hiS : i ∈ S <;> simp [hiS, Finset.sum_div]
  rw [sum_congr rfl hd]
  rw [Finset.sum_comm]
  apply sum_congr rfl
  intro j hj
  simp_rw [unitGame_eq_unanimity, interaction_unanimity]
  have he : ∀ S ∈ N.powerset,
      (if i ∈ S then w j * (if S = receptive (u j) then value r x (u j) else 0) / S.card else 0) =
        if S = receptive (u j) then
          (if i ∈ receptive (u j) then w j * value r x (u j) / (receptive (u j)).card else 0) else 0 := by
    intro S _
    by_cases h : S = receptive (u j) <;> simp [h]
  rw [sum_congr rfl he]
  simp [Finset.sum_ite_eq', mem_powerset, hR j hj]

/-- Same children imply same receptive field, independently of channel weights. -/
theorem receptive_shared_children (k : ℕ) (c : Fin k → Expr α)
    (w₁ w₂ : Fin k → ℝ) :
    receptive (.block k c w₁) = receptive (.block k c w₂) := rfl

/-- Channel grouping is an exact finite sum; no claim of equal ReLU activation. -/
theorem channel_grouping {β γ : Type*} (J : Finset β) (C : Finset γ)
    (w z : β → γ → ℝ) :
    (∑ j ∈ J, ∑ c ∈ C, w j c * z j c) =
      ∑ p ∈ J ×ˢ C, w p.1 p.2 * z p.1 p.2 := by
  rw [Finset.sum_product]

/-- Grouped CNN gates test nonzero channel vectors, rather than every coordinate. -/
noncomputable def groupedBlock {β : Type*} (J : Finset β) (m : ℕ)
    (w z : β → Fin m → ℝ) : ℝ :=
  if ∀ j ∈ J, ∃ c, z j c ≠ 0
  then max (∑ j ∈ J, ∑ c, w j c * z j c) 0 else 0

/-- Inductive block step for the source's grouped-channel CNN gate. -/
theorem groupedBlock_mask {β : Type*} [DecidableEq β] (J : Finset β) (m : ℕ)
    (R : β → Finset α) (w z zT : β → Fin m → ℝ) (T : Finset α)
    (hz : ∀ j ∈ J, ∀ c, zT j c = if R j ⊆ T then z j c else 0) :
    groupedBlock J m w zT =
      if J.biUnion R ⊆ T then groupedBlock J m w z else 0 := by
  by_cases hR : J.biUnion R ⊆ T
  · rw [if_pos hR]
    have he : ∀ j ∈ J, ∀ c, zT j c = z j c := by
      intro j hj c
      rw [hz j hj c, if_pos (by intro i hi; exact hR (mem_biUnion.mpr ⟨j,hj,hi⟩))]
    have hgate : (∀ j ∈ J, ∃ c, zT j c ≠ 0) ↔ (∀ j ∈ J, ∃ c, z j c ≠ 0) := by
      constructor <;> intro h j hj
      · obtain ⟨c,hc⟩ := h j hj; exact ⟨c, by simpa [he j hj c] using hc⟩
      · obtain ⟨c,hc⟩ := h j hj; exact ⟨c, by simpa [he j hj c] using hc⟩
    have hsum : (∑ j ∈ J, ∑ c, w j c * zT j c) = ∑ j ∈ J, ∑ c, w j c * z j c := by
      apply sum_congr rfl; intro j hj; simp_rw [he j hj]
    simp only [groupedBlock, hgate, hsum]
  · rw [if_neg hR]
    obtain ⟨i,hi,hiT⟩ := Finset.not_subset.mp hR
    obtain ⟨j,hj,hiR⟩ := mem_biUnion.mp hi
    have hjR : ¬ R j ⊆ T := fun h => hiT (h hiR)
    have hzero : ∀ c, zT j c = 0 := by intro c; rw [hz j hj c, if_neg hjR]
    have hgate : ¬ ∀ j ∈ J, ∃ c, zT j c ≠ 0 := by
      intro h; obtain ⟨c,hc⟩ := h j hj; exact hc (hzero c)
    simp [groupedBlock,hgate]

/-- Changing scalar-AND to vector-nonzero gates does not preserve numerical values. -/
theorem scalar_grouped_gate_counterexample :
    max ((1 : ℝ) * (if (1 : ℝ) ≠ 0 ∧ (0 : ℝ) ≠ 0 then 1 else 0)) 0 ≠
      max ((1 : ℝ) * (if (1 : ℝ) + (0 : ℝ) ≠ 0 then 1 else 0)) 0 := by
  norm_num

/-- Literal R1/R2 alone allow the false empty-field case in Lemma 1. -/
theorem empty_unit_counterexample :
    interaction (centered (unanimity (∅ : Finset α) 1)) ∅ ≠ (1 : ℝ) := by
  simp
end Harsanyi.Network
