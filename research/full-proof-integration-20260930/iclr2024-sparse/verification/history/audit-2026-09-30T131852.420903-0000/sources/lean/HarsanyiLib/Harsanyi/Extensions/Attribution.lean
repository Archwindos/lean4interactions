import Harsanyi.Core.Shapley
import Mathlib.Data.Nat.Choose.Sum

/-! Staging module for full-paper finite attribution results. No baseline is zero by assumption. -/
namespace Harsanyi
open Finset
variable {α : Type*} [DecidableEq α]

/-- The coalition finite difference in a disjoint environment. -/
noncomputable def higherMarginal (g : Game α) (T S : Finset α) : ℝ :=
  interaction (fun L => g (L ∪ S)) T

/-- A reconstruction over disjoint sets is a product of powerset sums. -/
theorem reconstruct_union_disjoint (d : Game α) (A B : Finset α)
    (hAB : Disjoint A B) :
    reconstruct d (A ∪ B) =
      ∑ U ∈ A.powerset, ∑ V ∈ B.powerset, d (U ∪ V) := by
  induction A using Finset.induction_on generalizing d with
  | empty => simp [reconstruct]
  | @insert i A hi ih =>
    have hA : Disjoint A B := disjoint_of_subset_left (subset_insert i A) hAB
    have hiB : i ∉ B := by
      intro hit
      exact (Finset.disjoint_left.mp hAB (mem_insert_self i A) hit)
    have hiAB : i ∉ A ∪ B := by simp [hi, hiB]
    rw [insert_union, reconstruct, sum_powerset_insert hiAB]
    change reconstruct d (A ∪ B) + reconstruct (fun U => d (insert i U)) (A ∪ B) = _
    rw [ih d hA, ih (fun U => d (insert i U)) hA, sum_powerset_insert hi]
    simp_rw [insert_union]

/-- Finite difference decomposition: no empty-coalition or baseline assumption. -/
theorem higherMarginal_eq_sum_interaction (g : Game α) (T S : Finset α)
    (hTS : Disjoint T S) :
    higherMarginal g T S = ∑ U ∈ S.powerset, interaction g (T ∪ U) := by
  have hreconstruct : ∀ L ⊆ T,
      g (L ∪ S) = ∑ U ∈ S.powerset,
        reconstruct (fun K => interaction g (K ∪ U)) L := by
    intro L hLT
    rw [← reconstruction g (L ∪ S), reconstruct_union_disjoint _ _ _
      (disjoint_of_subset_left hLT hTS)]
    exact Finset.sum_comm
  calc
    higherMarginal g T S = interaction (fun L => ∑ U ∈ S.powerset,
        reconstruct (fun K => interaction g (K ∪ U)) L) T := by
      exact interaction_congr _ _ _ hreconstruct
    _ = ∑ U ∈ S.powerset, interaction (reconstruct (fun K => interaction g (K ∪ U))) T := by
      unfold interaction
      simp_rw [Finset.mul_sum]
      exact Finset.sum_comm
    _ = _ := by simp_rw [interaction_reconstruct]

/-- Symmetry only requires equality on the subcoalitions actually used. -/
theorem interaction_symmetry (g : Game α) (S : Finset α) (i j : α)
    (hi : i ∉ S) (hj : j ∉ S)
    (h : ∀ U ⊆ S, g (insert i U) = g (insert j U)) :
    interaction g (insert i S) = interaction g (insert j S) := by
  rw [interaction_insert _ _ _ hi, interaction_insert _ _ _ hj]
  apply interaction_congr
  intro U hU
  simp only [marginal, h U hU]

/-- The paper's context form of the recursive axiom. -/
theorem interaction_context_difference (g : Game α) (S : Finset α) (i : α)
    (hi : i ∉ S) :
    interaction g (insert i S) =
      interaction (fun U => g (insert i U)) S - interaction g S := by
  rw [interaction_insert _ _ _ hi]
  exact interaction_sub _ _ _

/-- Additive dummy interactions of positive environment order vanish.
This explicitly nonempty statement is valid and does not repair CVPR's false empty case. -/
theorem interaction_additive_dummy_nonempty (g : Game α) (S : Finset α) (i : α)
    (hi : i ∉ S) (hS : S.Nonempty) (c : ℝ)
    (h : ∀ U ⊆ S, g (insert i U) = g U + c) :
    interaction g (insert i S) = 0 := by
  rw [interaction_insert _ _ _ hi]
  have he : interaction (marginal g i) S = interaction (fun _ => c) S := by
    apply interaction_congr
    intro U hU
    simp [marginal, h U hU]
  rw [he, interaction_const, if_neg hS.ne_empty]

/-- A finite factorial convolution. It includes all zero-cardinality boundaries. -/
theorem factorial_powerset_sum (R : Finset α) (a b : ℕ) :
    (∑ U ∈ R.powerset, ((a + U.card).factorial : ℝ) *
      ((b + R.card - U.card).factorial : ℝ)) =
    (a.factorial : ℝ) * (b.factorial : ℝ) *
      ((a + b + R.card + 1).factorial : ℝ) / ((a + b + 1).factorial : ℝ) := by
  have fact_ne : ∀ n : ℕ, (n.factorial : ℝ) ≠ 0 := by
    intro n
    exact_mod_cast Nat.factorial_ne_zero n
  have fact_succ : ∀ n : ℕ, ((n + 1).factorial : ℝ) =
      (n + 1 : ℝ) * (n.factorial : ℝ) := by
    intro n
    simp [Nat.factorial_succ]
  induction R using Finset.induction_on generalizing a b with
  | empty =>
    simp only [powerset_empty, sum_singleton, card_empty, Nat.add_zero, Nat.sub_zero]
    field_simp [fact_ne]
  | @insert i R hi ih =>
    rw [sum_powerset_insert hi, card_insert_of_notMem hi]
    have h₁ : ∀ U ∈ R.powerset,
        ((a + U.card).factorial : ℝ) * ((b + (R.card + 1) - U.card).factorial : ℝ) =
          ((a + U.card).factorial : ℝ) * (((b + 1) + R.card - U.card).factorial : ℝ) := by
      intro U hU
      have he : b + (R.card + 1) - U.card = (b + 1) + R.card - U.card := by omega
      rw [he]
    have h₂ : ∀ U ∈ R.powerset,
        ((a + (insert i U).card).factorial : ℝ) *
          ((b + (R.card + 1) - (insert i U).card).factorial : ℝ) =
        (((a + 1) + U.card).factorial : ℝ) * ((b + R.card - U.card).factorial : ℝ) := by
      intro U hU
      have hiU : i ∉ U := fun hit => hi ((mem_powerset.mp hU) hit)
      rw [card_insert_of_notMem hiU]
      have hc := card_le_card (mem_powerset.mp hU)
      have he₁ : a + (U.card + 1) = (a + 1) + U.card := by omega
      have he₂ : b + (R.card + 1) - (U.card + 1) = b + R.card - U.card := by omega
      rw [he₁, he₂]
    rw [sum_congr rfl h₁, sum_congr rfl h₂, ih a (b + 1), ih (a + 1) b]
    have hd₁ : a + (b + 1) + 1 = (a + b + 1) + 1 := by omega
    have hd₂ : (a + 1) + b + 1 = (a + b + 1) + 1 := by omega
    have hn₁ : a + (b + 1) + R.card + 1 = a + b + (R.card + 1) + 1 := by omega
    have hn₂ : (a + 1) + b + R.card + 1 = a + b + (R.card + 1) + 1 := by omega
    rw [hd₁, hd₂, hn₁, hn₂, fact_succ a, fact_succ b, fact_succ (a + b + 1)]
    have hp : (a + b + 1 + 1 : ℝ) ≠ 0 := by positivity
    field_simp [fact_ne, hp]
    push_cast
    ring

/-- Reindex all supersets of L inside N by subsets of N minus L. -/
theorem sum_supersets_eq_sum_complement (N L : Finset α) (hLN : L ⊆ N)
    (f : Game α) :
    (∑ S ∈ N.powerset, if L ⊆ S then f S else 0) =
      ∑ U ∈ (N \ L).powerset, f (L ∪ U) := by
  rw [← Finset.sum_filter]
  symm
  refine Finset.sum_bij (fun U _ => L ∪ U) ?_ ?_ ?_ ?_
  · intro U hU
    have hUR := mem_powerset.mp hU
    apply mem_filter.mpr
    exact ⟨mem_powerset.mpr (union_subset hLN (hUR.trans sdiff_subset)), subset_union_left⟩
  · intro U hU V hV he
    change L ∪ U = L ∪ V at he
    have hUR := mem_powerset.mp hU
    have hVR := mem_powerset.mp hV
    ext i
    constructor
    · intro hiU
      have hiL : i ∉ L := (mem_sdiff.mp (hUR hiU)).2
      have hh : i ∈ L ∪ V := by rw [← he]; exact mem_union_right L hiU
      simpa [hiL] using hh
    · intro hiV
      have hiL : i ∉ L := (mem_sdiff.mp (hVR hiV)).2
      have hh : i ∈ L ∪ U := by rw [he]; exact mem_union_right L hiV
      simpa [hiL] using hh
  · intro S hS
    have hSN := mem_powerset.mp (mem_filter.mp hS).1
    have hLS := (mem_filter.mp hS).2
    refine ⟨S \ L, mem_powerset.mpr ?_, ?_⟩
    · intro i hi
      exact mem_sdiff.mpr ⟨hSN (mem_sdiff.mp hi).1, (mem_sdiff.mp hi).2⟩
    · exact union_sdiff_of_subset hLS
  · intro U _
    rfl

/-- Common factorial weight of the classical attribution definitions. -/
noncomputable def factorialWeight (k m s : ℕ) : ℝ :=
  (k : ℝ) * (s.factorial : ℝ) * ((k - 1 + m - s).factorial : ℝ) /
    ((m + k).factorial : ℝ)

/-- The full coefficient identity, including L=empty and N=L. -/
theorem factorialWeight_superset_sum (k : ℕ) (hk : 0 < k)
    (N L : Finset α) (hLN : L ⊆ N) :
    (∑ S ∈ N.powerset, if L ⊆ S then factorialWeight k N.card S.card else 0) =
      (L.card.factorial : ℝ) * (k.factorial : ℝ) / ((L.card + k).factorial : ℝ) := by
  rw [sum_supersets_eq_sum_complement N L hLN]
  have hcard := card_le_card hLN
  have hR : (N \ L).card = N.card - L.card := card_sdiff_of_subset hLN
  have hterm : ∀ U ∈ (N \ L).powerset,
      factorialWeight k N.card (L ∪ U).card =
        (k : ℝ) / ((N.card + k).factorial : ℝ) *
          (((L.card + U.card).factorial : ℝ) *
            ((k - 1 + (N \ L).card - U.card).factorial : ℝ)) := by
    intro U hU
    have hUR := mem_powerset.mp hU
    have hLU : Disjoint L U := by
      apply Finset.disjoint_left.mpr
      intro i hiL hiU
      exact (mem_sdiff.mp (hUR hiU)).2 hiL
    rw [card_union_of_disjoint hLU]
    have hcU : U.card ≤ (N \ L).card := card_le_card hUR
    have he : k - 1 + N.card - (L.card + U.card) = k - 1 + (N \ L).card - U.card := by
      omega
    simp only [factorialWeight, he]
    ring
  rw [sum_congr rfl hterm, ← Finset.mul_sum, factorial_powerset_sum]
  have hn : L.card + (k - 1) + (N \ L).card + 1 = N.card + k := by omega
  have hd : L.card + (k - 1) + 1 = L.card + k := by omega
  have hk₁ : (k - 1) + 1 = k := by omega
  have hfac : (k.factorial : ℝ) = (k : ℝ) * ((k - 1).factorial : ℝ) := by
    conv_lhs => rw [← hk₁]
    rw [Nat.factorial_succ, Nat.cast_mul, hk₁]
  rw [hn, hd, hfac]
  have hne : ((N.card + k).factorial : ℝ) ≠ 0 := by exact_mod_cast Nat.factorial_ne_zero _
  field_simp [hne]

/-- Extending a smaller powerset sum to a fixed finite universe. -/
theorem sum_powerset_extend (N S : Finset α) (hSN : S ⊆ N) (d : Game α) :
    (∑ U ∈ S.powerset, d U) =
      ∑ U ∈ N.powerset, if U ⊆ S then d U else 0 := by
  rw [← Finset.sum_filter]
  apply Finset.sum_congr
  · ext U
    simp only [mem_powerset, mem_filter]
    exact ⟨fun h => ⟨h.trans hSN, h⟩, fun h => h.2⟩
  · intro U _
    rfl

/-- The common weighted finite-difference transform underlying Shapley, SII and STI. -/
theorem weighted_higherMarginal_eq (g : Game α) (T N : Finset α)
    (hTN : Disjoint T N) (k : ℕ) (hk : 0 < k) :
    (∑ S ∈ N.powerset, factorialWeight k N.card S.card * higherMarginal g T S) =
      ∑ U ∈ N.powerset,
        (U.card.factorial : ℝ) * (k.factorial : ℝ) /
          ((U.card + k).factorial : ℝ) * interaction g (T ∪ U) := by
  have hterm : ∀ S ∈ N.powerset,
      factorialWeight k N.card S.card * higherMarginal g T S =
        ∑ U ∈ N.powerset, if U ⊆ S then
          factorialWeight k N.card S.card * interaction g (T ∪ U) else 0 := by
    intro S hS
    have hSN := mem_powerset.mp hS
    rw [higherMarginal_eq_sum_interaction _ _ _ (disjoint_of_subset_right hSN hTN),
      sum_powerset_extend N S hSN, Finset.mul_sum]
    apply Finset.sum_congr rfl
    intro U _
    split_ifs <;> simp
  rw [sum_congr rfl hterm, Finset.sum_comm]
  apply Finset.sum_congr rfl
  intro U hU
  have he : ∀ S : Finset α,
      (if U ⊆ S then factorialWeight k N.card S.card * interaction g (T ∪ U) else 0) =
        (if U ⊆ S then factorialWeight k N.card S.card else 0) * interaction g (T ∪ U) := by
    intro S
    split_ifs <;> simp
  simp_rw [he]
  rw [← Finset.sum_mul, factorialWeight_superset_sum k hk N U (mem_powerset.mp hU)]

/-- The factorial quotient is the inverse binomial coefficient. -/
theorem factorial_ratio_eq_choose_inv (a k : ℕ) :
    (a.factorial : ℝ) * (k.factorial : ℝ) / ((a + k).factorial : ℝ) =
      1 / ((a + k).choose k : ℝ) := by
  have hc : 0 < (a + k).choose k := Nat.choose_pos (Nat.le_add_left k a)
  have hcne : ((a + k).choose k : ℝ) ≠ 0 := by exact_mod_cast (Nat.ne_of_gt hc)
  have hfne : ((a + k).factorial : ℝ) ≠ 0 := by exact_mod_cast Nat.factorial_ne_zero _
  have he : ((a + k).choose k : ℝ) * (a.factorial : ℝ) * (k.factorial : ℝ) =
      ((a + k).factorial : ℝ) := by
    exact_mod_cast Nat.add_choose_mul_factorial_mul_factorial a k
  field_simp [hcne, hfne]
  nlinarith only [he]

/-- The k=1 kernel is the classical factorial Shapley weight. -/
theorem factorialWeight_one (m s : ℕ) :
    factorialWeight 1 m s =
      (s.factorial : ℝ) * ((m - s).factorial : ℝ) / ((m + 1).factorial : ℝ) := by
  simp [factorialWeight]

/-- The common kernel also matches the reciprocal-choose definition of STI. -/
theorem factorialWeight_eq_inv_choose (k m s : ℕ) (hk : 0 < k) (hsm : s ≤ m) :
    factorialWeight k m s =
      (k : ℝ) / (m + k : ℝ) * (1 / ((m + k - 1).choose s : ℝ)) := by
  have ha : s ≤ m + k - 1 := by omega
  have he : k - 1 + m - s = m + k - 1 - s := by omega
  have hn : m + k - 1 + 1 = m + k := by omega
  have hcne : ((m + k - 1).choose s : ℝ) ≠ 0 := by
    exact_mod_cast (Nat.ne_of_gt (Nat.choose_pos ha))
  have hfne : ((m + k - 1).factorial : ℝ) ≠ 0 := by exact_mod_cast Nat.factorial_ne_zero _
  have hnne : (m + k : ℝ) ≠ 0 := by positivity
  have hch : ((m + k - 1).choose s : ℝ) * (s.factorial : ℝ) *
      ((m + k - 1 - s).factorial : ℝ) = ((m + k - 1).factorial : ℝ) := by
    exact_mod_cast Nat.choose_mul_factorial_mul_factorial ha
  have hchval : (s.factorial : ℝ) * ((m + k - 1 - s).factorial : ℝ) =
      ((m + k - 1).factorial : ℝ) / ((m + k - 1).choose s : ℝ) := by
    apply (eq_div_iff hcne).mpr
    nlinarith only [hch]
  have hfac : ((m + k).factorial : ℝ) =
      (m + k : ℝ) * ((m + k - 1).factorial : ℝ) := by
    conv_lhs => rw [← hn]
    rw [Nat.factorial_succ, Nat.cast_mul, hn]
    simp
  unfold factorialWeight
  rw [he, hfac]
  calc
    _ = (k : ℝ) * ((s.factorial : ℝ) * ((m + k - 1 - s).factorial : ℝ)) /
        ((m + k : ℝ) * ((m + k - 1).factorial : ℝ)) := by ring
    _ = _ := by
      rw [hchval]
      field_simp [hcne, hfne, hnne]

/-- Classical Shapley value defined by factorial-weighted marginal contributions. -/
noncomputable def factorialShapley (g : Game α) (N : Finset α) (i : α) : ℝ :=
  ∑ S ∈ (N.erase i).powerset,
    (S.card.factorial : ℝ) * ((N.card - S.card - 1).factorial : ℝ) /
      (N.card.factorial : ℝ) * (g (insert i S) - g S)

/-- Classical Shapley interaction index, including an empty target coalition. -/
noncomputable def factorialShapleyInteraction (g : Game α) (N T : Finset α) : ℝ :=
  ∑ S ∈ (N \ T).powerset,
    (S.card.factorial : ℝ) * ((N.card - T.card - S.card).factorial : ℝ) /
      ((N.card - T.card + 1).factorial : ℝ) * higherMarginal g T S

/-- The paper's k-th order Shapley--Taylor definition, for positive orders. -/
noncomputable def shapleyTaylor (g : Game α) (N : Finset α) (k : ℕ) (T : Finset α) : ℝ :=
  if T.card < k then higherMarginal g T ∅
  else if T.card = k then (k : ℝ) / N.card *
    ∑ S ∈ (N \ T).powerset, (1 / ((N.card - 1).choose S.card : ℝ)) * higherMarginal g T S
  else 0

/-- Exact equivalence of the classical Shapley formula and equal dividend allocation. -/
theorem factorialShapley_eq_dividends (g : Game α) (N : Finset α) (i : α) (hi : i ∈ N) :
    factorialShapley g N i =
      ∑ S ∈ (N.erase i).powerset, (1 / (S.card + 1 : ℝ)) * interaction g (insert i S) := by
  have hm : (N.erase i).card + 1 = N.card := card_erase_add_one hi
  have hdis : Disjoint ({i} : Finset α) (N.erase i) := by simp
  have hd (S : Finset α) : higherMarginal g {i} S = g (insert i S) - g S := by
    simp [higherMarginal, interaction_singleton]
  have hterm : ∀ S ∈ (N.erase i).powerset,
      (S.card.factorial : ℝ) * ((N.card - S.card - 1).factorial : ℝ) /
          (N.card.factorial : ℝ) * (g (insert i S) - g S) =
        factorialWeight 1 (N.erase i).card S.card * higherMarginal g {i} S := by
    intro S hS
    have he : N.card - S.card - 1 = (N.erase i).card - S.card := by omega
    rw [factorialWeight_one, hm, he, hd]
  unfold factorialShapley
  rw [sum_congr rfl hterm, weighted_higherMarginal_eq _ _ _ hdis 1 (by omega)]
  apply Finset.sum_congr rfl
  intro S _
  rw [factorial_ratio_eq_choose_inv]
  simp

/-- Exact factorial-weighted Shapley interaction / dividend formula. -/
theorem factorialShapleyInteraction_eq_dividends (g : Game α) (N T : Finset α)
    (hTN : T ⊆ N) :
    factorialShapleyInteraction g N T =
      ∑ S ∈ (N \ T).powerset, (1 / (S.card + 1 : ℝ)) * interaction g (T ∪ S) := by
  have hm : (N \ T).card = N.card - T.card := card_sdiff_of_subset hTN
  have hdis : Disjoint T (N \ T) := disjoint_sdiff_self_right
  unfold factorialShapleyInteraction
  have he : ∀ S : Finset α,
      (S.card.factorial : ℝ) * ((N.card - T.card - S.card).factorial : ℝ) /
          ((N.card - T.card + 1).factorial : ℝ) * higherMarginal g T S =
        factorialWeight 1 (N \ T).card S.card * higherMarginal g T S := by
    intro S
    rw [factorialWeight_one, hm]
  rw [sum_congr rfl (fun S _ => he S), weighted_higherMarginal_eq _ _ _ hdis 1 (by omega)]
  apply Finset.sum_congr rfl
  intro S _
  rw [factorial_ratio_eq_choose_inv]
  simp

/-- All three cases of the original Shapley--Taylor statement. -/
theorem shapleyTaylor_eq_dividends (g : Game α) (N T : Finset α) (hTN : T ⊆ N)
    (k : ℕ) (hk : 0 < k) :
    shapleyTaylor g N k T =
      if T.card < k then interaction g T
      else if T.card = k then
        ∑ S ∈ (N \ T).powerset, (1 / ((S.card + k).choose k : ℝ)) * interaction g (T ∪ S)
      else 0 := by
  unfold shapleyTaylor
  split_ifs with hlow htop
  · simp [higherMarginal]
  · have hm : (N \ T).card = N.card - k := by rw [card_sdiff_of_subset hTN, htop]
    have hn : (N \ T).card + k = N.card := by
      have ht := card_le_card hTN
      omega
    rw [Finset.mul_sum]
    have he : ∀ S ∈ (N \ T).powerset,
        (k : ℝ) / N.card * ((1 / ((N.card - 1).choose S.card : ℝ)) * higherMarginal g T S) =
          factorialWeight k (N \ T).card S.card * higherMarginal g T S := by
      intro S hS
      rw [factorialWeight_eq_inv_choose _ _ _ hk (card_le_card (mem_powerset.mp hS)), hn]
      have hnr : ((N \ T).card : ℝ) + (k : ℝ) = (N.card : ℝ) := by exact_mod_cast hn
      rw [hnr]
      ring
    rw [sum_congr rfl he, weighted_higherMarginal_eq _ _ _ disjoint_sdiff_self_right k hk]
    apply Finset.sum_congr rfl
    intro S _
    rw [factorial_ratio_eq_choose_inv]
  · rfl

/-- Reindex equal allocation by removing the distinguished member. -/
theorem dividendAllocation_eq_insert_sum (g : Game α) (N : Finset α) (i : α) (hi : i ∈ N) :
    dividendAllocation g N i =
      ∑ U ∈ (N.erase i).powerset, (1 / (U.card + 1 : ℝ)) * interaction g (insert i U) := by
  unfold dividendAllocation
  rw [← Finset.sum_filter]
  symm
  refine Finset.sum_bij (fun U _ => insert i U) ?_ ?_ ?_ ?_
  · intro U hU
    have hUN := mem_powerset.mp hU
    exact mem_filter.mpr ⟨mem_powerset.mpr (insert_subset hi (hUN.trans (erase_subset i N))), mem_insert_self _ _⟩
  · intro U hU V hV he
    change insert i U = insert i V at he
    have hiU : i ∉ U := fun hh => (mem_erase.mp ((mem_powerset.mp hU) hh)).1 rfl
    have hiV : i ∉ V := fun hh => (mem_erase.mp ((mem_powerset.mp hV) hh)).1 rfl
    have he' := congrArg (fun S => S.erase i) he
    simpa [hiU, hiV] using he'
  · intro S hS
    have hSN := mem_powerset.mp (mem_filter.mp hS).1
    have hiS := (mem_filter.mp hS).2
    refine ⟨S.erase i, mem_powerset.mpr ?_, insert_erase hiS⟩
    exact erase_subset_erase i hSN
  · intro U hU
    have hiU : i ∉ U := fun hh => (mem_erase.mp ((mem_powerset.mp hU) hh)).1 rfl
    rw [card_insert_of_notMem hiU]
    push_cast
    ring

theorem factorialShapley_eq_dividendAllocation (g : Game α) (N : Finset α) (i : α)
    (hi : i ∈ N) : factorialShapley g N i = dividendAllocation g N i := by
  rw [factorialShapley_eq_dividends g N i hi, dividendAllocation_eq_insert_sum g N i hi]

end Harsanyi
