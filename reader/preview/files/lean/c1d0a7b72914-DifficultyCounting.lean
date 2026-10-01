import Harsanyi.Extensions.RobustnessFinite
namespace Harsanyi.DifficultyCounting
open Finset
open scoped BigOperators
variable {α : Type*} [DecidableEq α]

/-- Superset contexts are in bijection with their residual subsets outside L. -/
theorem superset_context_count (R L : Finset α) (m : ℕ) (hLR : L ⊆ R)
    (hlm : L.card ≤ m) :
    ((R.powersetCard m).filter (fun S => L ⊆ S)).card =
      (R.card-L.card).choose (m-L.card) := by
  rw [← card_sdiff_of_subset hLR, ← card_powersetCard]
  apply card_bij (fun S _ => S \ L)
  · intro S hS
    obtain ⟨hs,hLS⟩ := mem_filter.mp hS
    obtain ⟨hSR,hSm⟩ := mem_powersetCard.mp hs
    apply mem_powersetCard.mpr
    constructor
    · intro x hx
      have h := mem_sdiff.mp hx
      exact mem_sdiff.mpr ⟨hSR h.1,h.2⟩
    · rw [card_sdiff_of_subset hLS, hSm]
  · intro S hS T hT h
    have hLS := (mem_filter.mp hS).2
    have hLT := (mem_filter.mp hT).2
    calc S = L ∪ (S \ L) := (union_sdiff_of_subset hLS).symm
         _ = L ∪ (T \ L) := by rw [h]
         _ = T := union_sdiff_of_subset hLT
  · intro W hW
    obtain ⟨hWR,hWm⟩ := mem_powersetCard.mp hW
    have hd : Disjoint L W := by
      apply disjoint_left.mpr
      intro x hxL hxW
      exact (mem_sdiff.mp (hWR hxW)).2 hxL
    have hUnion : (L ∪ W).card = m := by rw [card_union_of_disjoint hd,hWm]; omega
    have hU : L ∪ W ∈ (R.powersetCard m).filter (fun S => L ⊆ S) := by
      apply mem_filter.mpr
      refine ⟨mem_powersetCard.mpr ⟨?_,hUnion⟩,subset_union_left⟩
      exact union_subset hLR (hWR.trans sdiff_subset)
    refine ⟨L ∪ W,hU,?_⟩
    ext x
    simp only [mem_sdiff,mem_union]
    have hw : x ∈ W → x ∉ L := fun hx => (mem_sdiff.mp (hWR hx)).2
    tauto

theorem superset_context_count_all (R L : Finset α) (m : ℕ) (hLR : L ⊆ R) :
    ((R.powersetCard m).filter (fun S => L ⊆ S)).card =
      if L.card ≤ m then (R.card-L.card).choose (m-L.card) else 0 := by
  split_ifs with h
  · exact superset_context_count R L m hLR h
  · have he : (R.powersetCard m).filter (fun S => L ⊆ S) = ∅ := by
      apply filter_eq_empty_iff.mpr
      intro S hS hLS
      have hs := (mem_powersetCard.mp hS).2
      have hc := card_le_card hLS
      rw [hs] at hc
      exact h hc
    rw [he,card_empty]

/-- Count each L once for every size-m context S containing it. -/
theorem context_double_sum (R : Finset α) (m : ℕ) (f : Finset α → ℝ) :
    (∑ S ∈ R.powersetCard m, ∑ L ∈ S.powerset, f L) =
      ∑ L ∈ R.powerset, (if L.card ≤ m then
        ((R.card-L.card).choose (m-L.card) : ℝ) else 0) * f L := by
  have inner (S : Finset α) (hSR : S ⊆ R) :
      (∑ L ∈ S.powerset, f L) = ∑ L ∈ R.powerset, if L ⊆ S then f L else 0 := by
    have hsub := powerset_mono.mpr hSR
    calc
      _ = ∑ L ∈ S.powerset, if L ⊆ S then f L else 0 := by
        apply sum_congr rfl
        intro L hL
        simp [mem_powerset.mp hL]
      _ = _ := sum_subset hsub (fun L _ hnot => by
        have hns : ¬L ⊆ S := by simpa only [mem_powerset] using hnot
        simp [hns])
  calc
    _ = ∑ S ∈ R.powersetCard m, ∑ L ∈ R.powerset, if L ⊆ S then f L else 0 := by
      apply sum_congr rfl
      intro S hS
      exact inner S (mem_powersetCard.mp hS).1
    _ = ∑ L ∈ R.powerset, ∑ S ∈ R.powersetCard m, if L ⊆ S then f L else 0 := sum_comm
    _ = _ := by
      apply sum_congr rfl
      intro L hL
      rw [← sum_filter]
      simp only [sum_const,nsmul_eq_mul]
      rw [superset_context_count_all R L m (mem_powerset.mp hL)]
      split_ifs <;> simp

/-- Group the residual-support count by its cardinality l. -/
theorem context_grouped_sum (R : Finset α) (m : ℕ) (f : Finset α → ℝ) :
    (∑ S ∈ R.powersetCard m, ∑ L ∈ S.powerset, f L) =
      ∑ l ∈ range (m+1), ((R.card-l).choose (m-l) : ℝ) *
        ∑ L ∈ R.powersetCard l, f L := by
  rw [context_double_sum]
  have hf := sum_fiberwise_eq_sum_filter R.powerset (range (m+1)) card
    (fun L => ((R.card-L.card).choose (m-L.card) : ℝ) * f L)
  rw [sum_filter] at hf
  simp only [mem_range,Nat.lt_succ_iff] at hf
  calc
    _ = ∑ L ∈ R.powerset, if L.card ≤ m then
        ((R.card-L.card).choose (m-L.card) : ℝ) * f L else 0 := by
      apply sum_congr rfl
      intro L _
      split_ifs <;> simp
    _ = ∑ l ∈ range (m+1), ∑ L ∈ R.powerset with L.card=l,
        ((R.card-L.card).choose (m-L.card) : ℝ) * f L := hf.symm
    _ = _ := by
      apply sum_congr rfl
      intro l _
      rw [powersetCard_eq_filter, mul_sum]
      apply sum_congr rfl
      intro L hL
      rw [(mem_filter.mp hL).2]

/-- The uniform context average has the corrected binomial coefficient. -/
theorem context_grouped_average (R : Finset α) (m : ℕ) (f : Finset α → ℝ) :
    Robustness.contextAverage R m (fun S => ∑ L ∈ S.powerset, f L) =
      ∑ l ∈ range (m+1), ((R.card-l).choose (m-l) : ℝ) /
        (R.card.choose m : ℝ) * ∑ L ∈ R.powersetCard l, f L := by
  unfold Robustness.contextAverage Robustness.average
  rw [card_powersetCard,context_grouped_sum,mul_sum]
  apply sum_congr rfl
  intro l _
  ring
end Harsanyi.DifficultyCounting
