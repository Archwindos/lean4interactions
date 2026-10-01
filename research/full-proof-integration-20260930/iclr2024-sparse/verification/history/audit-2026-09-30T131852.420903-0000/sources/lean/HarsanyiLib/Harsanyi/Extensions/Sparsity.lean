import Harsanyi.Core.Properties
import Mathlib.Analysis.SpecialFunctions.Log.Base

/-! Exact finite combinatorics for ICLR 2024 Sparse. No zero model-output baseline.
The matrix proof uses finite differences, avoiding the source's determinant sign error. -/
namespace Harsanyi.Sparsity
open Finset

theorem choose_coefficients_zero (n M : ℕ) (hMn : M ≤ n) (a : ℕ → ℝ)
    (hz : ∀ j ≤ M, ∑ k ∈ range (M + 1), (Nat.choose (n - j) k : ℝ) * a k = 0) :
    ∀ k ≤ M, a k = 0 := by
  induction M generalizing n a with
  | zero =>
    intro k hk
    have h := hz 0 (by omega)
    have hk0 : k = 0 := by omega
    simpa [hk0] using h
  | succ M ih =>
    have hd : ∀ j ≤ M,
        ∑ k ∈ range (M + 1), (Nat.choose ((n - 1) - j) k : ℝ) * a (k + 1) = 0 := by
      intro j hj
      have h0 := hz j (by omega)
      have h1 := hz (j + 1) (by omega)
      have hn : n - j = (n - (j + 1)) + 1 := by omega
      have hsub : (n - 1) - j = n - (j + 1) := by omega
      have hdiff :
          (∑ k ∈ range (M + 2), (Nat.choose (n - j) k : ℝ) * a k) -
          (∑ k ∈ range (M + 2), (Nat.choose (n - (j + 1)) k : ℝ) * a k) =
          ∑ k ∈ range (M + 1), (Nat.choose ((n - 1) - j) k : ℝ) * a (k + 1) := by
        conv_lhs => lhs; rw [sum_range_succ']
        conv_lhs => rhs; rw [sum_range_succ']
        simp only [Nat.choose_zero_right, Nat.cast_one, one_mul]
        rw [show (∑ k ∈ range (M + 1), (Nat.choose (n - j) (k + 1) : ℝ) * a (k + 1)) + a 0 -
            ((∑ k ∈ range (M + 1), (Nat.choose (n - (j + 1)) (k + 1) : ℝ) * a (k + 1)) + a 0) =
            (∑ k ∈ range (M + 1), (Nat.choose (n - j) (k + 1) : ℝ) * a (k + 1)) -
            (∑ k ∈ range (M + 1), (Nat.choose (n - (j + 1)) (k + 1) : ℝ) * a (k + 1)) by ring]
        rw [← sum_sub_distrib]
        apply sum_congr rfl
        intro k hk
        rw [hn, Nat.choose_succ_succ', Nat.cast_add, hsub]
        ring
      rw [← hdiff, h0, h1]
      ring
    have hat : ∀ k ≤ M, a (k + 1) = 0 := by
      simpa using ih (n - 1) (by omega) (fun k => a (k + 1)) hd
    have ha0 : a 0 = 0 := by
      have h := hz 0 (by omega)
      rw [sum_range_succ'] at h
      have hs : (∑ k ∈ range (M + 1), (Nat.choose (n - 0) (k + 1) : ℝ) * a (k + 1)) = 0 := by
        apply sum_eq_zero
        intro k hk
        rw [hat k (by have := mem_range.mp hk; omega), mul_zero]
      rw [hs] at h
      simpa using h
    intro k hk
    cases k with
    | zero => exact ha0
    | succ k => exact hat k (by omega)

/-- Lemma 3, with exactly M positive-order coefficients and M+1 tested rows. -/
theorem binomial_matrix_kernel (n M : ℕ) (hM : 0 < M) (hMn : M < n) (w : ℕ → ℝ)
    (hz : ∀ j ≤ M, ∑ k ∈ Icc 1 M,
      ((Nat.choose (n - j) k : ℝ) / (Nat.choose n k : ℝ)) * w k = 0) :
    ∀ k ∈ Icc 1 M, w k = 0 := by
  let a : ℕ → ℝ := fun k => if k = 0 then 0 else w k / (Nat.choose n k : ℝ)
  have ha : ∀ j ≤ M, ∑ k ∈ range (M + 1), (Nat.choose (n - j) k : ℝ) * a k = 0 := by
    intro j hj
    calc
      _ = ∑ k ∈ Icc 1 M, ((Nat.choose (n - j) k : ℝ) / (Nat.choose n k : ℝ)) * w k := by
        rw [show range (M + 1) = insert 0 (Icc 1 M) by ext k; simp; omega]
        rw [sum_insert (by simp)]
        simp only [a, if_pos rfl, mul_zero, zero_add]
        apply sum_congr rfl
        intro k hk
        have hk0 : k ≠ 0 := by have := (mem_Icc.mp hk).1; omega
        rw [if_neg hk0]
        ring
      _ = 0 := hz j hj
  have hzero := choose_coefficients_zero n M (Nat.le_of_lt hMn) a ha
  intro k hk
  have hk1 := (mem_Icc.mp hk).1
  have hkM := (mem_Icc.mp hk).2
  have hk0 : k ≠ 0 := by omega
  have hden : (Nat.choose n k : ℝ) ≠ 0 := by
    exact_mod_cast Nat.choose_ne_zero (by omega : k ≤ n)
  have h := hzero k hkM
  simp only [a, if_neg hk0] at h
  exact (div_eq_zero_iff.mp h).resolve_right hden

theorem binomial_coefficients_zero_of_le (n M : ℕ) (hMn : M ≤ n) (w : ℕ → ℝ)
    (hz : ∀ j ≤ M, ∑ k ∈ Icc 1 M,
      ((Nat.choose (n - j) k : ℝ) / (Nat.choose n k : ℝ)) * w k = 0) :
    ∀ k ∈ Icc 1 M, w k = 0 := by
  let a : ℕ → ℝ := fun k => if k = 0 then 0 else w k / (Nat.choose n k : ℝ)
  have ha : ∀ j ≤ M, ∑ k ∈ range (M + 1), (Nat.choose (n - j) k : ℝ) * a k = 0 := by
    intro j hj
    calc
      _ = ∑ k ∈ Icc 1 M, ((Nat.choose (n - j) k : ℝ) / (Nat.choose n k : ℝ)) * w k := by
        rw [show range (M + 1) = insert 0 (Icc 1 M) by ext k; simp; omega]
        rw [sum_insert (by simp)]
        simp only [a, if_pos rfl, mul_zero, zero_add]
        apply sum_congr rfl
        intro k hk
        have hk0 : k ≠ 0 := by have := (mem_Icc.mp hk).1; omega
        rw [if_neg hk0]
        ring
      _ = 0 := hz j hj
  have hzero := choose_coefficients_zero n M hMn a ha
  intro k hk
  have hk1 := (mem_Icc.mp hk).1
  have hkM := (mem_Icc.mp hk).2
  have hk0 : k ≠ 0 := by omega
  have hden : (Nat.choose n k : ℝ) ≠ 0 := by
    exact_mod_cast Nat.choose_ne_zero (by omega : k ≤ n)
  have h := hzero k hkM
  simp only [a, if_neg hk0] at h
  exact (div_eq_zero_iff.mp h).resolve_right hden


variable {α : Type*} [DecidableEq α]

noncomputable def orderTotal (d : Game α) (N : Finset α) (k : ℕ) : ℝ :=
  ∑ S ∈ N.powersetCard k, d S

noncomputable def meanOutput (g : Game α) (N : Finset α) (m : ℕ) : ℝ :=
  (∑ S ∈ N.powersetCard m, g S) / (Nat.choose N.card m : ℝ)

/-- Each k-set is contained in exactly choose(n-k,m-k) m-masks. -/
theorem card_supermasks (N T : Finset α) (m : ℕ) (hTN : T ⊆ N) (hTm : T.card ≤ m) :
    ((N.powersetCard m).filter fun S => T ⊆ S).card =
      Nat.choose (N.card - T.card) (m - T.card) := by
  classical
  have hbij : ((N.powersetCard m).filter fun S => T ⊆ S).card =
      ((N \ T).powersetCard (m - T.card)).card := by
    refine card_bij' (fun S _ => S \ T) (fun R _ => R ∪ T) ?_ ?_ ?_ ?_
    · intro S hS
      rcases mem_filter.mp hS with ⟨hSN, hTS⟩
      rcases mem_powersetCard.mp hSN with ⟨hSN, hc⟩
      apply mem_powersetCard.mpr
      exact ⟨sdiff_subset_sdiff hSN (Subset.refl T), by rw [card_sdiff_of_subset hTS, hc]⟩
    · intro R hR
      rcases mem_powersetCard.mp hR with ⟨hR, hc⟩
      have hdis : Disjoint R T := disjoint_of_subset_left hR sdiff_disjoint
      apply mem_filter.mpr
      constructor
      · apply mem_powersetCard.mpr
        exact ⟨union_subset (Subset.trans hR sdiff_subset) hTN,
          by rw [card_union_of_disjoint hdis, hc]; omega⟩
      · exact subset_union_right
    · intro S hS
      exact sdiff_union_of_subset (mem_filter.mp hS).2
    · intro R hR
      have hdis : Disjoint R T :=
        disjoint_of_subset_left (mem_powersetCard.mp hR).1 sdiff_disjoint
      ext x
      simp only [mem_sdiff, mem_union]
      have hd := disjoint_left.mp hdis
      constructor
      · rintro ⟨hx | hx, hn⟩
        · exact hx
        · exact (hn hx).elim
      · intro hx
        exact ⟨Or.inl hx, fun ht => hd hx ht⟩
  rw [hbij, card_powersetCard, card_sdiff_of_subset hTN]

theorem subset_layer_sum (d : Game α) (N : Finset α) (m k : ℕ) (hkm : k ≤ m) :
    (∑ S ∈ N.powersetCard m, ∑ T ∈ S.powersetCard k, d T) =
      (Nat.choose (N.card - k) (m - k) : ℝ) * orderTotal d N k := by
  classical
  have hfilter : ∀ S ∈ N.powersetCard m,
      S.powersetCard k = (N.powersetCard k).filter fun T => T ⊆ S := by
    intro S hS
    have hSN := (mem_powersetCard.mp hS).1
    ext T
    simp only [mem_powersetCard, mem_filter]
    constructor
    · intro h
      exact ⟨⟨Subset.trans h.1 hSN, h.2⟩, h.1⟩
    · intro h
      exact ⟨h.2, h.1.2⟩
  calc
    _ = ∑ S ∈ N.powersetCard m, ∑ T ∈ N.powersetCard k, if T ⊆ S then d T else 0 := by
      apply sum_congr rfl
      intro S hS
      rw [hfilter S hS, sum_filter]
    _ = ∑ T ∈ N.powersetCard k, ∑ S ∈ N.powersetCard m, if T ⊆ S then d T else 0 := sum_comm
    _ = ∑ T ∈ N.powersetCard k, (Nat.choose (N.card - k) (m - k) : ℝ) * d T := by
      apply sum_congr rfl
      intro T hT
      have hTN := (mem_powersetCard.mp hT).1
      have hTc := (mem_powersetCard.mp hT).2
      rw [← sum_filter, sum_const, nsmul_eq_mul, card_supermasks N T m hTN (by omega), hTc]
    _ = _ := by simp [orderTotal, mul_sum]

theorem layer_sum_reconstruct (d : Game α) (N : Finset α) (m : ℕ) :
    (∑ S ∈ N.powersetCard m, reconstruct d S) =
      ∑ k ∈ range (m + 1), (Nat.choose (N.card - k) (m - k) : ℝ) * orderTotal d N k := by
  classical
  calc
    _ = ∑ S ∈ N.powersetCard m, ∑ k ∈ range (m + 1), ∑ T ∈ S.powersetCard k, d T := by
      apply sum_congr rfl
      intro S hS
      rw [reconstruct, Finset.sum_powerset, (mem_powersetCard.mp hS).2]
    _ = ∑ k ∈ range (m + 1), ∑ S ∈ N.powersetCard m, ∑ T ∈ S.powersetCard k, d T := sum_comm
    _ = _ := by
      apply sum_congr rfl
      intro k hk
      exact subset_layer_sum d N m k (by have := mem_range.mp hk; omega)

theorem choose_ratio (n m k : ℕ) (hmn : m ≤ n) (hkm : k ≤ m) :
    (Nat.choose (n - k) (m - k) : ℝ) / (Nat.choose n m : ℝ) =
      (Nat.choose m k : ℝ) / (Nat.choose n k : ℝ) := by
  have hn1 : (Nat.choose n m : ℝ) ≠ 0 := by exact_mod_cast Nat.choose_ne_zero hmn
  have hn2 : (Nat.choose n k : ℝ) ≠ 0 := by exact_mod_cast Nat.choose_ne_zero (hkm.trans hmn)
  have h := Nat.choose_mul hmn hkm
  have hr : (Nat.choose n m : ℝ) * (Nat.choose m k : ℝ) =
      (Nat.choose n k : ℝ) * (Nat.choose (n - k) (m - k) : ℝ) := by exact_mod_cast h
  apply (div_eq_div_iff hn1 hn2).mpr
  nlinarith [hr]

/-- Lemma 2 before the high-order cutoff, for every valid mask size. -/
theorem mean_reconstruction (d : Game α) (N : Finset α) (m : ℕ) (hmn : m ≤ N.card) :
    meanOutput (reconstruct d) N m =
      ∑ k ∈ range (m + 1), ((Nat.choose m k : ℝ) / (Nat.choose N.card k : ℝ)) * orderTotal d N k := by
  unfold meanOutput
  rw [layer_sum_reconstruct, sum_div]
  apply sum_congr rfl
  intro k hk
  have hkm : k ≤ m := by have := mem_range.mp hk; omega
  rw [show (Nat.choose (N.card - k) (m - k) : ℝ) * orderTotal d N k / (Nat.choose N.card m : ℝ) =
      ((Nat.choose (N.card - k) (m - k) : ℝ) / (Nat.choose N.card m : ℝ)) * orderTotal d N k by ring,
    choose_ratio N.card m k hmn hkm]

/-- Full Lemma 2 in the original range M≤m≤n, including arbitrary model baseline. -/
theorem mean_centered_cutoff (g : Game α) (N : Finset α) (M m : ℕ)
    (hMm : M ≤ m) (hmn : m ≤ N.card)
    (hcut : ∀ S ⊆ N, M < S.card → interaction (centered g) S = 0) :
    meanOutput (centered g) N m =
      ∑ k ∈ Icc 1 M, ((Nat.choose m k : ℝ) / (Nat.choose N.card k : ℝ)) *
        orderTotal (interaction (centered g)) N k := by
  classical
  have hr : reconstruct (interaction (centered g)) = centered g := by
    funext S
    exact reconstruction _ S
  rw [← hr, mean_reconstruction _ _ _ hmn]
  rw [hr]
  symm
  apply sum_subset ?_ ?_
  · intro k hk
    have := (mem_Icc.mp hk).2
    exact mem_range.mpr (by omega)
  · intro k hk hkn
    by_cases hk0 : k = 0
    · subst k
      simp [orderTotal]
    · have hMk : M < k := by
        have := mem_range.mp hk
        simp only [mem_Icc, not_and_or, not_le] at hkn
        omega
      have hzero : orderTotal (interaction (centered g)) N k = 0 := by
        apply sum_eq_zero
        intro S hS
        rcases mem_powersetCard.mp hS with ⟨hSN, hc⟩
        exact hcut S hSN (by omega)
      rw [hzero, mul_zero]

/-- The mean formula is also valid below M: terms with k>m have zero binomial coefficients. -/
theorem mean_centered_cutoff_all (g : Game α) (N : Finset α) (M m : ℕ)
    (hmn : m ≤ N.card)
    (hcut : ∀ S ⊆ N, M < S.card → interaction (centered g) S = 0) :
    meanOutput (centered g) N m =
      ∑ k ∈ Icc 1 M, ((Nat.choose m k : ℝ) / (Nat.choose N.card k : ℝ)) *
        orderTotal (interaction (centered g)) N k := by
  classical
  by_cases hMm : M ≤ m
  · exact mean_centered_cutoff g N M m hMm hmn hcut
  have hr : reconstruct (interaction (centered g)) = centered g := by
    funext S
    exact reconstruction _ S
  rw [← hr, mean_reconstruction _ _ _ hmn, hr]
  have he : range (m + 1) = insert 0 (Icc 1 m) := by ext k; simp; omega
  rw [he, sum_insert (by simp)]
  simp only [Nat.choose_zero_right, Nat.cast_one, div_self (one_ne_zero : (1 : ℝ) ≠ 0)]
  have hz : orderTotal (interaction (centered g)) N 0 = 0 := by simp [orderTotal]
  rw [hz, mul_zero, zero_add]
  apply sum_subset
  · intro k hk
    exact mem_Icc.mpr ⟨(mem_Icc.mp hk).1, by have := (mem_Icc.mp hk).2; omega⟩
  · intro k hk hkm
    have hm_lt : m < k := by
      have hk1 := (mem_Icc.mp hk).1
      simp only [mem_Icc, not_and_or, not_le] at hkm
      omega
    rw [Nat.choose_eq_zero_of_lt hm_lt, Nat.cast_zero, zero_div, zero_mul]

@[simp] theorem mean_centered_zero (g : Game α) (N : Finset α) :
    meanOutput (centered g) N 0 = 0 := by simp [meanOutput]

@[simp] theorem meanOutput_top (g : Game α) (N : Finset α) :
    meanOutput g N N.card = g N := by simp [meanOutput, powersetCard_self]

noncomputable def totalStrength (d : Game α) (N : Finset α) (k : ℕ) : ℝ :=
  ∑ S ∈ N.powersetCard k, |d S|

noncomputable def salientFamily (d : Game α) (N : Finset α) (k : ℕ) (τ : ℝ) : Finset (Finset α) :=
  (N.powersetCard k).filter fun S => τ ≤ |d S|

noncomputable def cancellationRatio (d : Game α) (N : Finset α) (k : ℕ) : ℝ :=
  orderTotal d N k / totalStrength d N k

theorem threshold_count (d : Game α) (N : Finset α) (k : ℕ) (τ : ℝ) :
    τ * (salientFamily d N k τ).card ≤ totalStrength d N k := by
  classical
  calc
    _ = ∑ S ∈ salientFamily d N k τ, τ := by simp [mul_comm]
    _ ≤ ∑ S ∈ salientFamily d N k τ, |d S| := by
      apply sum_le_sum
      intro S hS
      exact (mem_filter.mp hS).2
    _ ≤ totalStrength d N k := by
      apply sum_le_sum_of_subset_of_nonneg (filter_subset _ _)
      intro S hS hn
      exact abs_nonneg _

/-- The exact counting inequality in B.4, in its stated non-cancellation case.
Theorem 2's coefficient expression is a separate dependency, not assumed as the goal. -/
theorem salient_count_bound (d : Game α) (N : Finset α) (k : ℕ) (τ : ℝ) (hτ : 0 < τ)
    (hη : cancellationRatio d N k ≠ 0) :
    ((salientFamily d N k τ).card : ℝ) ≤
      |orderTotal d N k| / (τ * |cancellationRatio d N k|) := by
  have hs : totalStrength d N k ≠ 0 := by
    intro h
    apply hη
    simp [cancellationRatio, h]
  have hs0 : 0 ≤ totalStrength d N k := sum_nonneg fun _ _ => abs_nonneg _
  have hspos : 0 < totalStrength d N k := lt_of_le_of_ne hs0 (Ne.symm hs)
  have heq : |orderTotal d N k| / |cancellationRatio d N k| = totalStrength d N k := by
    rw [cancellationRatio, abs_div, abs_of_pos hspos]
    have ha : orderTotal d N k ≠ 0 := by
      intro h
      apply hη
      simp [cancellationRatio, h]
    field_simp
  have h := threshold_count d N k τ
  apply (le_div_iff₀ (mul_pos hτ (abs_pos.mpr hη))).mpr
  calc
    ((salientFamily d N k τ).card : ℝ) * (τ * |cancellationRatio d N k|) =
      (τ * (salientFamily d N k τ).card) * |cancellationRatio d N k| := by ring
    _ ≤ totalStrength d N k * |cancellationRatio d N k| :=
      mul_le_mul_of_nonneg_right h (abs_nonneg _)
    _ = |orderTotal d N k| := by
      exact (div_eq_iff (abs_pos.mpr hη).ne').mp heq |>.symm


/-- Existence of leading coefficients with all low digits zero. This general lemma does not
assume the desired representation; its premises are a sum bound and the degenerate-zero case. -/
theorem coefficient_normalization (b μ p : ℝ) (hb : 1 < b) (hp : 0 < p)
    (K : Finset ℕ) (hK : K.Nonempty) (A : ℕ → ℝ)
    (hμ : 0 ≤ μ) (hlower : μ ≤ ∑ k ∈ K, A k)
    (hupper : (∑ k ∈ K, A k) ≤ b ^ p * μ)
    (hzero : μ = 0 → ∀ k ∈ K, A k = 0) :
    ∃ (δ : ℝ) (c : ℕ → ℝ),
      (∀ k ∈ K, |c k| ≤ 1) ∧
      (∀ k ∈ K, A k = c k * b ^ (p + δ) * μ) ∧
      0 < (∑ k ∈ K, c k) ∧
      δ ≤ Real.logb b (1 / (∑ k ∈ K, c k)) := by
  classical
  have hb0 : 0 < b := by linarith
  have hb1 : b ≠ 1 := by linarith
  by_cases hμ0 : μ = 0
  · let q := hK.choose
    have hq : q ∈ K := hK.choose_spec
    refine ⟨-p, fun k => if k = q then 1 else 0, ?_, ?_, ?_, ?_⟩
    · intro k hk
      dsimp only
      split_ifs <;> norm_num
    · intro k hk
      rw [hzero hμ0 k hk, hμ0, mul_zero]
    · simp [sum_ite_eq', hq]
    · simp [sum_ite_eq', hq, Real.logb_one]
      linarith
  · have hμpos : 0 < μ := lt_of_le_of_ne hμ (Ne.symm hμ0)
    let C : ℝ := 1 + ∑ k ∈ K, |A k / μ|
    have hC1 : 1 ≤ C := by
      dsimp [C]
      exact le_add_of_nonneg_right (sum_nonneg fun k hk => abs_nonneg _)
    have hCpos : 0 < C := by linarith
    let c : ℕ → ℝ := fun k => (A k / μ) / C
    have hcSum : (∑ k ∈ K, c k) = (∑ k ∈ K, A k) / (μ * C) := by
      dsimp [c]
      rw [← sum_div, ← sum_div]
      ring
    have hsumpos : 0 < ∑ k ∈ K, c k := by
      rw [hcSum]
      exact div_pos (lt_of_lt_of_le hμpos hlower) (mul_pos hμpos hCpos)
    have hcupper : C * (∑ k ∈ K, c k) ≤ b ^ p := by
      rw [hcSum]
      have heq : C * ((∑ k ∈ K, A k) / (μ * C)) = (∑ k ∈ K, A k) / μ := by
        field_simp
      rw [heq]
      exact (div_le_iff₀ hμpos).mpr (by simpa [mul_comm] using hupper)
    refine ⟨Real.logb b C - p, c, ?_, ?_, hsumpos, ?_⟩
    · intro k hk
      dsimp [c]
      rw [abs_div, abs_of_pos hCpos]
      apply (div_le_one hCpos).mpr
      have hsingle : |A k / μ| ≤ ∑ j ∈ K, |A j / μ| :=
        Finset.single_le_sum (f := fun j => |A j / μ|) (fun j hj => abs_nonneg _) hk
      dsimp [C]
      linarith
    · intro k hk
      have he : p + (Real.logb b C - p) = Real.logb b C := by ring
      rw [he, Real.rpow_logb hb0 hb1 hCpos]
      dsimp [c]
      field_simp
    · apply (Real.le_logb_iff_rpow_le hb (one_div_pos.mpr hsumpos)).mpr
      rw [Real.rpow_sub hb0, Real.rpow_logb hb0 hb1 hCpos]
      apply (le_div_iff₀ hsumpos).mpr
      rw [div_mul_eq_mul_div]
      exact (div_le_iff₀ (Real.rpow_pos_of_pos hb0 p)).mpr (by simpa [mul_comm] using hcupper)

/-- T2's existence construction from the original cutoff, mean monotonicity and robustness.
M=n is included. n>1 and 1≤M≤n are the source expression's nontrivial defined domain.
No positive-singleton-mean premise is added. -/
theorem sparse_coefficient_existence (g : Game α) (N : Finset α) (M : ℕ) (p : ℝ)
    (hn : 1 < N.card) (hM : 0 < M) (hMn : M ≤ N.card) (hp : 0 < p)
    (hcut : ∀ S ⊆ N, M < S.card → interaction (centered g) S = 0)
    (hmono : ∀ m' m, m' ≤ m → m ≤ N.card →
      meanOutput (centered g) N m' ≤ meanOutput (centered g) N m)
    (hrob : ∀ m' m, 0 < m → m' ≤ m → m ≤ N.card →
      ((m' : ℝ) / (m : ℝ)) ^ p * meanOutput (centered g) N m ≤ meanOutput (centered g) N m') :
    ∃ (δ : ℝ) (c : ℕ → ℝ),
      (∀ k ∈ Icc 1 M, |c k| ≤ 1) ∧
      (∀ k ∈ Icc 1 M, orderTotal (interaction (centered g)) N k =
        c k * (N.card : ℝ) ^ (p + δ) * meanOutput (centered g) N 1) ∧
      0 < (∑ k ∈ Icc 1 M, c k) ∧
      δ ≤ Real.logb N.card (1 / (∑ k ∈ Icc 1 M, c k)) := by
  classical
  let μ := fun m => meanOutput (centered g) N m
  let A := orderTotal (interaction (centered g)) N
  have hμnonneg : ∀ m ≤ N.card, 0 ≤ μ m := by
    intro m hm
    have h := hmono 0 m (Nat.zero_le _) hm
    simpa [μ] using h
  have htop : μ N.card = ∑ k ∈ Icc 1 M, A k := by
    dsimp only [μ]
    rw [mean_centered_cutoff_all g N M N.card (le_refl _) hcut]
    apply sum_congr rfl
    intro k hk
    have hd : (Nat.choose N.card k : ℝ) ≠ 0 := by
      exact_mod_cast Nat.choose_ne_zero ((mem_Icc.mp hk).2.trans hMn)
    rw [div_self hd, one_mul]
  have hupper (m : ℕ) (hm0 : 0 < m) (hm : m ≤ N.card) : μ m ≤ (m : ℝ) ^ p * μ 1 := by
    have hmpos : 0 < (m : ℝ) := by exact_mod_cast hm0
    have h := hrob 1 m hm0 (by omega) hm
    have hr : ((1 : ℝ) / (m : ℝ)) ^ p = ((m : ℝ) ^ p)⁻¹ := by
      rw [one_div, ← Real.rpow_neg_eq_inv_rpow, Real.rpow_neg hmpos.le]
    rw [Nat.cast_one, hr] at h
    have he : ((m : ℝ) ^ p) * (((m : ℝ) ^ p)⁻¹ * μ m) = μ m := by
      field_simp [ne_of_gt (Real.rpow_pos_of_pos hmpos p)]
    have hh := mul_le_mul_of_nonneg_left h (le_of_lt (Real.rpow_pos_of_pos hmpos p))
    simpa only [he, μ] using hh
  have hzero : μ 1 = 0 → ∀ k ∈ Icc 1 M, A k = 0 := by
    intro hz
    have hμzero : ∀ m ≤ N.card, μ m = 0 := by
      intro m hm
      by_cases hm0 : m = 0
      · subst m
        simp [μ]
      · have h := hupper m (by omega) hm
        rw [hz, mul_zero] at h
        exact le_antisymm h (hμnonneg m hm)
    apply binomial_coefficients_zero_of_le N.card M hMn A
    intro j hj
    rw [← mean_centered_cutoff_all g N M (N.card - j) (Nat.sub_le _ _) hcut]
    exact hμzero _ (Nat.sub_le _ _)
  apply coefficient_normalization (N.card : ℝ) (μ 1) p (by exact_mod_cast hn) hp
    (Icc 1 M) (by exact ⟨1, mem_Icc.mpr ⟨le_refl _, hM⟩⟩) A (hμnonneg 1 (by omega))
  · rw [← htop]
    exact hmono 1 N.card (by omega) (le_refl _)
  · rw [← htop]
    exact hupper N.card (by omega) (le_refl _)
  · exact hzero



noncomputable def leadingAggregate (N : Finset α) (M m0 : ℕ) (c : ℕ → ℝ) : ℝ :=
  ∑ k ∈ Icc 1 M, ((Nat.choose m0 k : ℝ) / (Nat.choose N.card k : ℝ)) * c k

noncomputable def digitAggregate (N : Finset α) (M m0 : ℕ) (a : ℕ → ℕ → ℝ) (i : ℕ) : ℝ :=
  ∑ k ∈ Icc 1 M, ((Nat.choose m0 k : ℝ) / (Nat.choose N.card k : ℝ)) * a k i

/-- The complete T2 witness, with an arbitrary finite low-digit family J.
The all-zero witness covers the conventional J={i<floor p} and an additionally written a0.
The coefficient identities, digit constraints, weighted aggregates and both sign bounds are retained. -/
structure CoefficientWitness (g : Game α) (N : Finset α) (M : ℕ) (p : ℝ) (J : Finset ℕ) where
  m0 : ℕ
  c : ℕ → ℝ
  δ : ℝ
  a : ℕ → ℕ → ℝ
  witnessRange : N.card - M ≤ m0 ∧ m0 ≤ N.card
  leadingBound : ∀ k ∈ Icc 1 M, |c k| ≤ 1
  representation : ∀ k ∈ Icc 1 M,
    orderTotal (interaction (centered g)) N k =
      (c k * (N.card : ℝ) ^ (p + δ) + ∑ i ∈ J, a k i * (N.card : ℝ) ^ i) *
        meanOutput (centered g) N 1
  constantBound : ∀ k ∈ Icc 1 M, |a k 0| < N.card
  digitBounds : ∀ k ∈ Icc 1 M, ∀ i ∈ J, 0 < i →
    ∃ d ∈ range N.card, |a k i| = (d : ℝ)
  aggregateNonzero : leadingAggregate N M m0 c ≠ 0
  positiveBound : 0 < leadingAggregate N M m0 c →
    δ ≤ Real.logb N.card ((1 / leadingAggregate N M m0 c) *
      (1 - ∑ i ∈ J, digitAggregate N M m0 a i / ((N.card : ℝ) ^ (p - i))))
  negativeBound : leadingAggregate N M m0 c < 0 →
    δ ≤ Real.logb N.card ((1 / (-leadingAggregate N M m0 c)) *
      (∑ i ∈ J, digitAggregate N M m0 a i / ((N.card : ℝ) ^ (p - i))))

/-- Full T2, without assuming a nonzero singleton mean, G nonempty, or M<n. -/
theorem sparse_original_coefficient_witness (g : Game α) (N : Finset α) (M : ℕ) (p : ℝ)
    (J : Finset ℕ) (hn : 1 < N.card) (hM : 0 < M) (hMn : M ≤ N.card) (hp : 0 < p)
    (hcut : ∀ S ⊆ N, M < S.card → interaction (centered g) S = 0)
    (hmono : ∀ m' m, m' ≤ m → m ≤ N.card →
      meanOutput (centered g) N m' ≤ meanOutput (centered g) N m)
    (hrob : ∀ m' m, 0 < m → m' ≤ m → m ≤ N.card →
      ((m' : ℝ) / (m : ℝ)) ^ p * meanOutput (centered g) N m ≤ meanOutput (centered g) N m') :
    Nonempty (CoefficientWitness g N M p J) := by
  obtain ⟨δ, c, hc, hrep, hpos, hbound⟩ :=
    sparse_coefficient_existence g N M p hn hM hMn hp hcut hmono hrob
  have hagg : leadingAggregate N M N.card c = ∑ k ∈ Icc 1 M, c k := by
    unfold leadingAggregate
    apply sum_congr rfl
    intro k hk
    have hd : (Nat.choose N.card k : ℝ) ≠ 0 := by
      exact_mod_cast Nat.choose_ne_zero ((mem_Icc.mp hk).2.trans hMn)
    rw [div_self hd, one_mul]
  refine ⟨{
    m0 := N.card
    c := c
    δ := δ
    a := fun _ _ => 0
    witnessRange := ⟨Nat.sub_le _ _, le_refl _⟩
    leadingBound := hc
    representation := ?_
    constantBound := ?_
    digitBounds := ?_
    aggregateNonzero := ?_
    positiveBound := ?_
    negativeBound := ?_ }⟩
  · intro k hk
    simpa using hrep k hk
  · intro k hk
    simp only [abs_zero]
    exact_mod_cast (by omega : 0 < N.card)
  · intro k hk i hi hi0
    refine ⟨0, mem_range.mpr (by omega), ?_⟩
    simp
  · rw [hagg]
    exact ne_of_gt hpos
  · intro h
    simpa [digitAggregate, hagg] using hbound
  · intro h
    rw [hagg] at h
    exact (not_lt_of_ge hpos.le h).elim

/-- The complete source T3 expression, including substitution of T2's same coefficients. -/
theorem salient_bound_original_coefficients (g : Game α) (N : Finset α) (M : ℕ) (p : ℝ)
    (J : Finset ℕ) (w : CoefficientWitness g N M p J) (k : ℕ) (hk : k ∈ Icc 1 M)
    (τ : ℝ) (hτ : 0 < τ)
    (hμ : 0 ≤ meanOutput (centered g) N 1)
    (hη : cancellationRatio (interaction (centered g)) N k ≠ 0) :
    ((salientFamily (interaction (centered g)) N k τ).card : ℝ) ≤
      meanOutput (centered g) N 1 / (τ * |cancellationRatio (interaction (centered g)) N k|) *
        |w.c k * (N.card : ℝ) ^ (p + w.δ) + ∑ i ∈ J, w.a k i * (N.card : ℝ) ^ i| := by
  have h := salient_count_bound (interaction (centered g)) N k τ hτ hη
  rw [w.representation k hk, abs_mul, abs_of_nonneg hμ] at h
  convert h using 1 <;> ring

/-- T2 and T3 from the paper's actual assumptions, with no representation premise added. -/
theorem sparse_original_T2_T3 (g : Game α) (N : Finset α) (M : ℕ) (p : ℝ)
    (J : Finset ℕ) (hn : 1 < N.card) (hM : 0 < M) (hMn : M ≤ N.card) (hp : 0 < p)
    (hcut : ∀ S ⊆ N, M < S.card → interaction (centered g) S = 0)
    (hmono : ∀ m' m, m' ≤ m → m ≤ N.card →
      meanOutput (centered g) N m' ≤ meanOutput (centered g) N m)
    (hrob : ∀ m' m, 0 < m → m' ≤ m → m ≤ N.card →
      ((m' : ℝ) / (m : ℝ)) ^ p * meanOutput (centered g) N m ≤ meanOutput (centered g) N m') :
    ∃ w : CoefficientWitness g N M p J, ∀ k ∈ Icc 1 M, ∀ τ : ℝ, 0 < τ →
      cancellationRatio (interaction (centered g)) N k ≠ 0 →
      ((salientFamily (interaction (centered g)) N k τ).card : ℝ) ≤
        meanOutput (centered g) N 1 / (τ * |cancellationRatio (interaction (centered g)) N k|) *
          |w.c k * (N.card : ℝ) ^ (p + w.δ) + ∑ i ∈ J, w.a k i * (N.card : ℝ) ^ i| := by
  obtain ⟨w⟩ := sparse_original_coefficient_witness g N M p J hn hM hMn hp hcut hmono hrob
  refine ⟨w, ?_⟩
  intro k hk τ hτ hη
  have hμ := hmono 0 1 (by omega) (by omega)
  have hμ0 : 0 ≤ meanOutput (centered g) N 1 := by simpa using hμ
  exact salient_bound_original_coefficients g N M p J w k hk τ hτ hμ0 hη

end Harsanyi.Sparsity
