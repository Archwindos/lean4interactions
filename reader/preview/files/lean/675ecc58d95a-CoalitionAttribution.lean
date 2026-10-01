import Harsanyi.Extensions.Attribution
import Harsanyi.Extensions.OrInteraction

namespace Harsanyi.Coalition
open Finset
variable {α : Type*} [DecidableEq α]

noncomputable def totalEffect (a o : Game α) (N T : Finset α) : ℝ :=
  interaction a T + orInteraction o N T

noncomputable def shares (J : Game α) (N : Finset α) (i : α) : ℝ :=
  ∑ T ∈ N.powerset, if i ∈ T then J T / T.card else 0

/-- A total Lean definition. Its empty-set value is an implementation convention,
not a repair of the paper's undefined 0/0 term. Paper adapters use nonempty S. -/
noncomputable def attribution (J : Game α) (N S : Finset α) : ℝ :=
  ∑ T ∈ N.powerset, if S ⊆ T then (S.card : ℝ) * (J T / T.card) else 0

noncomputable def conflict (J : Game α) (N S : Finset α) : ℝ :=
  ∑ T ∈ N.powerset,
    if ¬ S ⊆ T then ((S ∩ T).card : ℝ) * (J T / T.card) else 0

noncomputable def individualConflict (J : Game α) (N S : Finset α) (i : α) : ℝ :=
  ∑ T ∈ N.powerset, if i ∈ T ∧ ¬ S ⊆ T then J T / T.card else 0

 theorem sum_membership (S T : Finset α) (c : ℝ) :
    (∑ i ∈ S, if i ∈ T then c else 0) = ((S ∩ T).card : ℝ) * c := by
  rw [← sum_filter]
  have he : S.filter (fun i => i ∈ T) = S ∩ T := by ext i; simp
  rw [he]
  simp [nsmul_eq_mul]

 theorem sum_shares (J : Game α) (N S : Finset α) :
    (∑ i ∈ S, shares J N i) = attribution J N S + conflict J N S := by
  unfold shares attribution conflict
  rw [sum_comm, ← sum_add_distrib]
  apply sum_congr rfl
  intro T _
  rw [sum_membership]
  by_cases h : S ⊆ T
  · rw [if_pos h, if_neg (not_not.mpr h), inter_eq_left.mpr h]; simp
  · simp [h]

 theorem individual_split (J : Game α) (N S : Finset α) (i : α)
    (hi : i ∈ S) :
    shares J N i = attribution J N S / S.card + individualConflict J N S i := by
  have hc : (S.card : ℝ) ≠ 0 := by exact_mod_cast (card_ne_zero.mpr ⟨i, hi⟩)
  unfold shares attribution individualConflict
  rw [sum_div, ← sum_add_distrib]
  apply sum_congr rfl
  intro T _
  by_cases h : S ⊆ T
  · have hit := h hi
    simp [h, hit]
    field_simp
  · by_cases hit : i ∈ T <;> simp [h, hit]

 theorem singleton (J : Game α) (N : Finset α) (i : α) :
    attribution J N {i} = shares J N i := by
  simp [attribution, shares, singleton_subset_iff]

 theorem no_conflict (J : Game α) (N S : Finset α)
    (hz : ∀ T ⊆ N, ¬ S ⊆ T → (S ∩ T).Nonempty → J T = 0) :
    (∑ i ∈ S, shares J N i) = attribution J N S := by
  rw [sum_shares]
  have hc : conflict J N S = 0 := by
    unfold conflict
    apply sum_eq_zero
    intro T hT
    by_cases hST : S ⊆ T
    · simp [hST]
    · by_cases hne : (S ∩ T).Nonempty
      · simp [hST, hz T (mem_powerset.mp hT) hST hne]
      · have hem : S ∩ T = ∅ := not_nonempty_iff_eq_empty.mp hne
        simp [hem]
  rw [hc, add_zero]

 theorem individual_no_conflict (J : Game α) (N S : Finset α) (i : α)
    (hi : i ∈ S) (hz : ∀ T ⊆ N, i ∈ T → ¬ S ⊆ T → J T = 0) :
    shares J N i = attribution J N S / S.card := by
  rw [individual_split J N S i hi]
  have hc : individualConflict J N S i = 0 := by
    unfold individualConflict
    apply sum_eq_zero
    intro T hT
    by_cases h : i ∈ T ∧ ¬ S ⊆ T
    · simp [h, hz T (mem_powerset.mp hT) h.1 h.2]
    · simp [h]
  rw [hc, add_zero]

 theorem attribution_add (J K : Game α) (N S : Finset α) :
    attribution (fun T => J T + K T) N S = attribution J N S + attribution K N S := by
  unfold attribution
  rw [← sum_add_distrib]
  apply sum_congr rfl
  intro T _
  split_ifs <;> simp [add_div, mul_add]

 theorem factorialShapley_add (a o : Game α) (N : Finset α) (i : α) :
    factorialShapley (fun S => a S + o S) N i =
      factorialShapley a N i + factorialShapley o N i := by
  unfold factorialShapley
  rw [← sum_add_distrib]
  apply sum_congr rfl
  intro S _
  ring

 theorem dualShapley (o : Game α) (N : Finset α) (i : α) (hi : i ∈ N) :
    factorialShapley (fun L => -o (N \ L)) N i = factorialShapley o N i := by
  unfold factorialShapley
  let R := N.erase i
  have hm : R.card + 1 = N.card := card_erase_add_one hi
  refine sum_bij (fun S _ => R \ S) ?_ ?_ ?_ ?_
  · intro S hS
    exact mem_powerset.mpr sdiff_subset
  · intro S hS T hT he
    have hs := mem_powerset.mp hS
    have ht := mem_powerset.mp hT
    change R \ S = R \ T at he
    ext j
    have hh := congrArg (fun L => j ∈ L) he
    simp only [mem_sdiff] at hh
    by_cases hj : j ∈ R
    · tauto
    · have hjs : j ∉ S := fun h => hj (hs h)
      have hjt : j ∉ T := fun h => hj (ht h)
      simp [hjs, hjt]
  · intro T hT
    exact ⟨R \ T, mem_powerset.mpr sdiff_subset, Finset.sdiff_sdiff_eq_self (mem_powerset.mp hT)⟩
  · intro S hS
    have hs : S ⊆ R := mem_powerset.mp hS
    have hc : (R \ S).card = R.card - S.card := card_sdiff_of_subset hs
    have hcle := card_le_card hs
    have h1 : N \ S = insert i (R \ S) := by
      ext j
      have hiS : i ∉ S := fun h => (mem_erase.mp (hs h)).1 rfl
      simp only [mem_sdiff, mem_insert, R, mem_erase]
      constructor
      · intro h
        by_cases he : j = i
        · exact Or.inl he
        · exact Or.inr ⟨⟨he, h.1⟩, h.2⟩
      · rintro (rfl | h)
        · exact ⟨hi, hiS⟩
        · exact ⟨h.1.2, h.2⟩
    have h2 : N \ insert i S = R \ S := by ext j; simp [R]; tauto
    dsimp only
    rw [h1, h2, hc]
    have h3 : N.card - S.card - 1 = R.card - S.card := by omega
    have h4 : N.card - (R.card - S.card) - 1 = S.card := by omega
    rw [h3, h4]
    ring

 theorem or_shares (o : Game α) (N : Finset α) (i : α) :
    dividendAllocation (fun L => -o (N \ L)) N i =
      shares (fun T => orInteraction o N T) N i := by
  unfold dividendAllocation shares
  apply sum_congr rfl
  intro T _
  by_cases hi : i ∈ T
  · have ht : T ≠ ∅ := ne_empty_of_mem hi
    simp [hi, orInteraction, ht, interaction, mul_neg, sum_neg_distrib]
  · simp [hi]

/-- Theorem 3.2: actual factorial-weighted marginals, not an allocation assumption. -/
 theorem shapley_and_or (a o : Game α) (N : Finset α) (i : α) (hi : i ∈ N) :
    factorialShapley (fun S => a S + o S) N i =
      shares (totalEffect a o N) N i := by
  rw [factorialShapley_add, ← dualShapley o N i hi,
    factorialShapley_eq_dividendAllocation a N i hi,
    factorialShapley_eq_dividendAllocation (fun L => -o (N \ L)) N i hi,
    or_shares]
  unfold dividendAllocation shares totalEffect
  rw [← sum_add_distrib]
  apply sum_congr rfl
  intro T _
  by_cases hit : i ∈ T <;> simp [hit, add_div]

/-- Eq. (10), with both empty-coalition component baselines retained. -/
 theorem universal_matching (a o : Game α) (N S : Finset α) (hSN : S ⊆ N) :
    a S + o S = a ∅ + o ∅ +
      (∑ T ∈ S.powerset, if T = ∅ then 0 else interaction a T) +
      ∑ T ∈ N.powerset.filter (fun T => ¬ Disjoint T S), orInteraction o N T := by
  have ha := reconstruction a S
  have ho := or_reconstruction o N S hSN
  have hs : (∑ T ∈ S.powerset, if T = ∅ then 0 else interaction a T) =
      a S - a ∅ := by
    have he : ∀ T : Finset α, (if T = ∅ then 0 else interaction a T) =
        interaction a T - if T = ∅ then interaction a ∅ else 0 := by
      intro T; by_cases h : T = ∅ <;> simp [h]
    simp_rw [he, sum_sub_distrib]
    rw [show (∑ T ∈ S.powerset, interaction a T) = a S from ha]
    simp [sum_ite_eq']
  rw [hs]
  unfold orReconstruction at ho
  rw [show orInteraction o N ∅ = o ∅ by simp [orInteraction]] at ho
  linarith

 theorem ratio_bounds (a d : ℝ) (ha : 0 ≤ a) (had : a ≤ d) (hd : 0 < d) :
    0 ≤ a / d ∧ a / d ≤ 1 := by
  exact ⟨div_nonneg ha (le_of_lt hd), (div_le_one hd).mpr had⟩


/-- Paper Theorem 3.4, using the actual classical Shapley definition. -/
theorem paper_conflict (a o : Game α) (N S : Finset α) (hSN : S ⊆ N) :
    (∑ i ∈ S, factorialShapley (fun U => a U + o U) N i) =
      attribution (totalEffect a o N) N S + conflict (totalEffect a o N) N S := by
  have he : (∑ i ∈ S, factorialShapley (fun U => a U + o U) N i) =
      ∑ i ∈ S, shares (totalEffect a o N) N i := by
    apply sum_congr rfl
    intro i hi
    exact shapley_and_or a o N i (hSN hi)
  rw [he, sum_shares]

/-- Paper Theorem 3.6. Nonemptiness follows from its original membership premise. -/
theorem paper_individual (a o : Game α) (N S : Finset α) (hSN : S ⊆ N)
    (i : α) (hi : i ∈ S) :
    factorialShapley (fun U => a U + o U) N i =
      attribution (totalEffect a o N) N S / S.card +
        individualConflict (totalEffect a o N) N S i := by
  rw [shapley_and_or a o N i (hSN hi), individual_split _ _ _ _ hi]

theorem paper_singleton (a o : Game α) (N : Finset α) (i : α) (hi : i ∈ N) :
    attribution (totalEffect a o N) N {i} =
      factorialShapley (fun U => a U + o U) N i := by
  rw [singleton, shapley_and_or a o N i hi]

/-- Corollary 3.5 with the exact partial-coverage zero-effect premise. -/
theorem paper_no_conflict (a o : Game α) (N S : Finset α) (hSN : S ⊆ N)
    (hz : ∀ T ⊆ N, ¬ S ⊆ T → (S ∩ T).Nonempty →
      interaction a T = 0 ∧ orInteraction o N T = 0) :
    (∑ i ∈ S, factorialShapley (fun U => a U + o U) N i) =
      attribution (totalEffect a o N) N S := by
  have he : (∑ i ∈ S, factorialShapley (fun U => a U + o U) N i) =
      ∑ i ∈ S, shares (totalEffect a o N) N i := by
    apply sum_congr rfl
    intro i hi
    exact shapley_and_or a o N i (hSN hi)
  rw [he]
  apply no_conflict
  intro T hT hST hne
  obtain ⟨ha, ho⟩ := hz T hT hST hne
  simp [totalEffect, ha, ho]

theorem paper_individual_no_conflict (a o : Game α) (N S : Finset α)
    (hSN : S ⊆ N) (i : α) (hi : i ∈ S)
    (hz : ∀ T ⊆ N, ¬ S ⊆ T → (S ∩ T).Nonempty →
      interaction a T = 0 ∧ orInteraction o N T = 0) :
    factorialShapley (fun U => a U + o U) N i =
      attribution (totalEffect a o N) N S / S.card := by
  rw [shapley_and_or a o N i (hSN hi)]
  apply individual_no_conflict _ _ _ _ hi
  intro T hT hit hST
  obtain ⟨ha, ho⟩ := hz T hT hST ⟨i, mem_inter.mpr ⟨hi, hit⟩⟩
  simp [totalEffect, ha, ho]

theorem paper_efficiency (a o : Game α) (N S : Finset α) (hSN : S ⊆ N) :
    (a N + o N) - (a ∅ + o ∅) =
      attribution (totalEffect a o N) N S +
      (∑ i ∈ N \ S, factorialShapley (fun U => a U + o U) N i) +
      conflict (totalEffect a o N) N S := by
  have he : (∑ i ∈ N, factorialShapley (fun U => a U + o U) N i) =
      (a N + o N) - (a ∅ + o ∅) := by
    have hh : (∑ i ∈ N, factorialShapley (fun U => a U + o U) N i) =
        ∑ i ∈ N, dividendAllocation (fun U => a U + o U) N i := by
      apply sum_congr rfl
      intro i hi
      exact factorialShapley_eq_dividendAllocation _ _ _ hi
    rw [hh, dividendAllocation_efficiency]
  have hp := sum_sdiff hSN (f := fun i => factorialShapley (fun U => a U + o U) N i)
  have hs := paper_conflict a o N S hSN
  linarith

/-- Full-universe attribution equals its coefficient when the universe is nonempty. -/
theorem attribution_full (J : Game α) (N : Finset α) (hN : N.Nonempty) :
    attribution J N N = J N := by
  have hc : (N.card : ℝ) ≠ 0 := by exact_mod_cast (card_ne_zero.mpr hN)
  unfold attribution
  have he : ∀ T ∈ N.powerset,
      (if N ⊆ T then (N.card : ℝ) * (J T / T.card) else 0) =
        if T = N then J N else 0 := by
    intro T hT
    have ht := mem_powerset.mp hT
    by_cases hh : N ⊆ T
    · have eq : T = N := subset_antisymm ht hh
      subst T
      simp
      field_simp
    · have hn : T ≠ N := by intro eq; subst T; exact hh subset_rfl
      simp [hh, hn]
  rw [sum_congr rfl he]
  simp [sum_ite_eq']

/-- An exact Lean witness for the N=2 additive-game counterexample coefficients. -/
theorem pair_counterexample_effect (P : Finset α) (hP : P.Nonempty) :
    totalEffect (unanimity P 1) (orUnanimity P 1) P P = 2 := by
  norm_num [totalEffect, interaction_unanimity,
    orInteraction_unanimity P P P 1 subset_rfl hP]

theorem pair_counterexample_attribution (P : Finset α) (hP : P.Nonempty) :
    attribution (totalEffect (unanimity P 1) (orUnanimity P 1) P) P P = 2 := by
  rw [attribution_full _ _ hP, pair_counterexample_effect P hP]


noncomputable def banzhaf (g : Game α) (N : Finset α) (i : α) : ℝ :=
  (1 / (2 : ℝ) ^ (N.erase i).card) *
    ∑ S ∈ (N.erase i).powerset, (g (insert i S) - g S)

 theorem uniformWeight_superset (N L : Finset α) (hLN : L ⊆ N) :
    (∑ S ∈ N.powerset, if L ⊆ S then 1 / (2 : ℝ) ^ N.card else 0) =
      1 / (2 : ℝ) ^ L.card := by
  rw [sum_supersets_eq_sum_complement N L hLN]
  simp only [sum_const, card_powerset, nsmul_eq_mul, Nat.cast_pow, Nat.cast_ofNat]
  have hc : L.card + (N \ L).card = N.card := by
    rw [card_sdiff_of_subset hLN]
    exact Nat.add_sub_of_le (card_le_card hLN)
  rw [← hc, pow_add]
  field_simp

 theorem banzhaf_eq_dividends (g : Game α) (N : Finset α) (i : α) :
    banzhaf g N i =
      ∑ U ∈ (N.erase i).powerset,
        (1 / (2 : ℝ) ^ U.card) * interaction g (insert i U) := by
  let R := N.erase i
  have hdis : Disjoint ({i} : Finset α) R := by simp [R]
  have hd (S : Finset α) : higherMarginal g {i} S = g (insert i S) - g S := by
    simp [higherMarginal, interaction_singleton]
  unfold banzhaf
  rw [mul_sum]
  have he : ∀ S ∈ R.powerset,
      (1 / (2 : ℝ) ^ R.card) * (g (insert i S) - g S) =
        ∑ U ∈ R.powerset, if U ⊆ S then
          (1 / (2 : ℝ) ^ R.card) * interaction g (insert i U) else 0 := by
    intro S hS
    have hs := mem_powerset.mp hS
    rw [← hd, higherMarginal_eq_sum_interaction _ _ _ (disjoint_of_subset_right hs hdis),
      sum_powerset_extend R S hs, mul_sum]
    apply sum_congr rfl
    intro U _
    by_cases h : U ⊆ S <;> simp [h]
  rw [sum_congr rfl he, sum_comm]
  apply sum_congr rfl
  intro U hU
  have ht : ∀ S : Finset α,
      (if U ⊆ S then (1 / (2 : ℝ) ^ R.card) * interaction g (insert i U) else 0) =
      (if U ⊆ S then 1 / (2 : ℝ) ^ R.card else 0) * interaction g (insert i U) := by
    intro S; split_ifs <;> simp
  simp_rw [ht]
  rw [← sum_mul, uniformWeight_superset R U (mem_powerset.mp hU)]

 theorem dualBanzhaf (o : Game α) (N : Finset α) (i : α) (hi : i ∈ N) :
    banzhaf (fun L => -o (N \ L)) N i = banzhaf o N i := by
  unfold banzhaf
  congr 1
  let R := N.erase i
  refine sum_bij (fun S _ => R \ S) ?_ ?_ ?_ ?_
  · intro S _; exact mem_powerset.mpr sdiff_subset
  · intro S hS T hT he
    have hs := mem_powerset.mp hS
    have ht := mem_powerset.mp hT
    change R \ S = R \ T at he
    ext j
    have hh := congrArg (fun L => j ∈ L) he
    simp only [mem_sdiff] at hh
    by_cases hj : j ∈ R
    · tauto
    · have hjs : j ∉ S := fun h => hj (hs h)
      have hjt : j ∉ T := fun h => hj (ht h)
      simp [hjs, hjt]
  · intro T hT
    exact ⟨R \ T, mem_powerset.mpr sdiff_subset, Finset.sdiff_sdiff_eq_self (mem_powerset.mp hT)⟩
  · intro S hS
    have hs : S ⊆ R := mem_powerset.mp hS
    have h1 : N \ S = insert i (R \ S) := by
      ext j
      have hiS : i ∉ S := fun h => (mem_erase.mp (hs h)).1 rfl
      simp only [mem_sdiff, mem_insert, R, mem_erase]
      constructor
      · intro h
        by_cases he : j = i
        · exact Or.inl he
        · exact Or.inr ⟨⟨he, h.1⟩, h.2⟩
      · rintro (rfl | h)
        · exact ⟨hi, hiS⟩
        · exact ⟨h.1.2, h.2⟩
    have h2 : N \ insert i S = R \ S := by ext j; simp [R]; tauto
    dsimp only
    rw [h1, h2]
    ring

 theorem banzhaf_and_or (a o : Game α) (N : Finset α) (i : α) (hi : i ∈ N) :
    banzhaf (fun S => a S + o S) N i =
      ∑ U ∈ (N.erase i).powerset, (1 / (2 : ℝ) ^ U.card) *
        totalEffect a o N (insert i U) := by
  have hadd : banzhaf (fun S => a S + o S) N i = banzhaf a N i + banzhaf o N i := by
    unfold banzhaf
    rw [← mul_add, ← sum_add_distrib]
    congr 1
    apply sum_congr rfl
    intro S _; ring
  rw [hadd, ← dualBanzhaf o N i hi, banzhaf_eq_dividends, banzhaf_eq_dividends,
    ← sum_add_distrib]
  apply sum_congr rfl
  intro U _
  have ht : insert i U ≠ ∅ := ne_empty_of_mem (mem_insert_self i U)
  simp [totalEffect, orInteraction, ht, interaction, mul_neg, sum_neg_distrib]
  ring


noncomputable def strength (a o : Game α) (N T : Finset α) : ℝ :=
  |interaction a T| + |orInteraction o N T|
noncomputable def coveredStrength (a o : Game α) (N S : Finset α) : ℝ :=
  ∑ T ∈ N.powerset, if S ⊆ T then strength a o N T / T.card else 0
noncomputable def memberStrength (a o : Game α) (N : Finset α) (i : α) : ℝ :=
  ∑ T ∈ N.powerset, if i ∈ T then strength a o N T / T.card else 0
noncomputable def coalitionStrength (a o : Game α) (N S : Finset α) : ℝ :=
  ∑ T ∈ N.powerset, if S ⊆ T then (S.card : ℝ) * (strength a o N T / T.card) else 0
noncomputable def intersectStrength (a o : Game α) (N S : Finset α) : ℝ :=
  ∑ T ∈ N.powerset, ((S ∩ T).card : ℝ) * (strength a o N T / T.card)

theorem strength_nonneg (a o : Game α) (N T : Finset α) : 0 ≤ strength a o N T := by
  exact add_nonneg (abs_nonneg _) (abs_nonneg _)
theorem strength_div_nonneg (a o : Game α) (N T : Finset α) :
    0 ≤ strength a o N T / T.card := by
  exact div_nonneg (strength_nonneg a o N T) (Nat.cast_nonneg _)

theorem coveredStrength_le_memberStrength (a o : Game α) (N S : Finset α)
    (i : α) (hi : i ∈ S) :
    0 ≤ coveredStrength a o N S ∧ coveredStrength a o N S ≤ memberStrength a o N i := by
  constructor
  · apply sum_nonneg
    intro T _
    split_ifs
    · exact strength_div_nonneg a o N T
    · exact le_refl 0
  · apply sum_le_sum
    intro T _
    by_cases hST : S ⊆ T
    · simp [hST, hST hi]
    · by_cases hit : i ∈ T
      · simpa [hST, hit] using strength_div_nonneg a o N T
      · simp [hST, hit]

theorem rprime_bounds (a o : Game α) (N S : Finset α) (i : α) (hi : i ∈ S)
    (hd : 0 < memberStrength a o N i) :
    0 ≤ coveredStrength a o N S / memberStrength a o N i ∧
      coveredStrength a o N S / memberStrength a o N i ≤ 1 := by
  obtain ⟨ha, had⟩ := coveredStrength_le_memberStrength a o N S i hi
  exact ratio_bounds _ _ ha had hd

theorem coalitionStrength_le_intersectStrength (a o : Game α) (N S : Finset α) :
    0 ≤ coalitionStrength a o N S ∧
      coalitionStrength a o N S ≤ intersectStrength a o N S := by
  constructor
  · apply sum_nonneg
    intro T _
    split_ifs
    · exact mul_nonneg (Nat.cast_nonneg _) (strength_div_nonneg a o N T)
    · exact le_refl 0
  · apply sum_le_sum
    intro T _
    by_cases h : S ⊆ T
    · simp [h, inter_eq_left.mpr h]
    · simpa [h] using mul_nonneg (Nat.cast_nonneg (S ∩ T).card) (strength_div_nonneg a o N T)

theorem q_bounds (a o : Game α) (N S : Finset α)
    (hd : 0 < intersectStrength a o N S) :
    0 ≤ coalitionStrength a o N S / intersectStrength a o N S ∧
      coalitionStrength a o N S / intersectStrength a o N S ≤ 1 := by
  obtain ⟨ha, had⟩ := coalitionStrength_le_intersectStrength a o N S
  exact ratio_bounds _ _ ha had hd

theorem r_bounds (a o : Game α) (N S : Finset α) (i : α)
    (hd : 0 < |attribution (totalEffect a o N) N S / S.card| +
        |individualConflict (totalEffect a o N) N S i|) :
    0 ≤ |attribution (totalEffect a o N) N S / S.card| /
      (|attribution (totalEffect a o N) N S / S.card| +
        |individualConflict (totalEffect a o N) N S i|) ∧
    |attribution (totalEffect a o N) N S / S.card| /
      (|attribution (totalEffect a o N) N S / S.card| +
        |individualConflict (totalEffect a o N) N S i|) ≤ 1 := by
  apply ratio_bounds _ _ (abs_nonneg _) _ hd
  exact le_add_of_nonneg_right (abs_nonneg _)


/-- Subset geometric sum, including an empty universe. -/
theorem powerset_geometric (R : Finset α) (q : ℝ) :
    (∑ U ∈ R.powerset, q ^ U.card) = (1 + q) ^ R.card := by
  induction R using Finset.induction_on with
  | empty => simp
  | @insert i R hi ih =>
    rw [sum_powerset_insert hi, card_insert_of_notMem hi]
    have hc : ∀ U ∈ R.powerset, (insert i U).card = U.card + 1 := by
      intro U hU
      exact card_insert_of_notMem (fun hit => hi ((mem_powerset.mp hU) hit))
    have hs : (∑ U ∈ R.powerset, q ^ (insert i U).card) =
        (∑ U ∈ R.powerset, q ^ U.card) * q := by
      rw [sum_mul]
      apply sum_congr rfl
      intro U hU
      rw [hc U hU, pow_succ]
    rw [hs, ih, pow_succ]
    ring

/-- The exact signed power kernel printed in Appendix D. -/
theorem signed_half_superset (R L : Finset α) (hLR : L ⊆ R) :
    (∑ U ∈ R.powerset, if L ⊆ U then (-1 : ℝ) ^ U.card / 2 ^ U.card else 0) =
      (-1 : ℝ) ^ L.card / 2 ^ R.card := by
  rw [sum_supersets_eq_sum_complement R L hLR]
  have ht : ∀ W ∈ (R \ L).powerset,
      (-1 : ℝ) ^ (L ∪ W).card / 2 ^ (L ∪ W).card =
        ((-1 : ℝ) / 2) ^ L.card * ((-1 : ℝ) / 2) ^ W.card := by
    intro W hW
    have hd : Disjoint L W := by
      apply disjoint_left.mpr
      intro i hiL hiW
      exact (mem_sdiff.mp ((mem_powerset.mp hW) hiW)).2 hiL
    rw [card_union_of_disjoint hd, ← div_pow, pow_add]
  rw [sum_congr rfl ht, ← mul_sum, powerset_geometric]
  have hp : (1 : ℝ) + (-1 : ℝ) / 2 = 1 / 2 := by norm_num
  rw [hp, div_pow, div_pow, one_pow]
  have hc : L.card + (R \ L).card = R.card := by
    rw [card_sdiff_of_subset hLR]
    exact Nat.add_sub_of_le (card_le_card hLR)
  rw [← hc, pow_add]
  field_simp

/-- The reciprocal-order Shapley coefficient on a predecessor universe. -/
theorem shapley_kernel (R L : Finset α) (hLR : L ⊆ R) :
    (∑ U ∈ R.powerset, if L ⊆ U then factorialWeight 1 R.card U.card else 0) =
      1 / ((L.card : ℝ) + 1) := by
  rw [factorialWeight_superset_sum 1 (by omega) R L hLR]
  simp only [Nat.factorial_one, Nat.cast_one, mul_one]
  rw [Nat.factorial_succ, Nat.cast_mul, Nat.cast_add, Nat.cast_one]
  have hne : (L.card.factorial : ℝ) ≠ 0 := by exact_mod_cast Nat.factorial_ne_zero _
  field_simp

/-- Exact Möbius support of a finite sum of pure AND games. -/
theorem toy_and_support {β : Type*} [DecidableEq β] (K : Finset β)
    (supports : β → Finset α) (weights : β → ℝ) (S : Finset α) :
    interaction (fun U => ∑ k ∈ K, unanimity (supports k) (weights k) U) S =
      ∑ k ∈ K, if S = supports k then weights k else 0 := by
  induction K using Finset.induction_on with
  | empty => simp
  | @insert k K hk ih =>
    simp only [sum_insert hk]
    rw [interaction_add, interaction_unanimity, ih]

end Harsanyi.Coalition
