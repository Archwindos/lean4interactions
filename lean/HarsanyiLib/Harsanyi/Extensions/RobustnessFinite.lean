import Harsanyi.Extensions.Attribution
import Mathlib.Data.Finset.Powerset
import Mathlib.Tactic

namespace Harsanyi.Robustness
open Finset
open scoped BigOperators
variable {α : Type*} [DecidableEq α]

noncomputable def average {β : Type*} (s : Finset β) (f : β → ℝ) : ℝ :=
  (s.card : ℝ)⁻¹ * ∑ t ∈ s, f t
noncomputable def contextAverage (R : Finset α) (m : ℕ) (f : Game α) : ℝ :=
  average (R.powersetCard m) f
noncomputable def pairDelta (g : Game α) (i j : α) (S : Finset α) : ℝ :=
  g (insert i (insert j S))-g (insert i S)-g (insert j S)+g S
noncomputable def multiOrderInteraction (g : Game α) (N : Finset α) (i j : α) (m : ℕ) : ℝ :=
  contextAverage (N \ {i,j}) m (pairDelta g i j)
noncomputable def multiOrderAttribution (g : Game α) (N : Finset α) (i : α) (m : ℕ) : ℝ :=
  contextAverage (N.erase i) m (fun S => g (insert i S)-g S)

 theorem average_add {β : Type*} (s : Finset β) (f h : β → ℝ) :
    average s (fun t => f t+h t) = average s f+average s h := by
  simp [average, sum_add_distrib, mul_add]
 theorem average_sub {β : Type*} (s : Finset β) (f h : β → ℝ) :
    average s (fun t => f t-h t) = average s f-average s h := by
  simp [average, sum_sub_distrib, mul_sub]
 theorem average_smul {β : Type*} (s : Finset β) (f : β → ℝ) (a : ℝ) :
    average s (fun t => a*f t) = a*average s f := by
  simp [average, mul_sum, mul_left_comm, mul_assoc]
 theorem average_const {β : Type*} (s : Finset β) (hs : s.Nonempty) (a : ℝ) :
    average s (fun _ => a) = a := by
  have hn : (s.card : ℝ) ≠ 0 := by exact_mod_cast card_ne_zero.mpr hs
  simp [average, hn]
 theorem pairDelta_add (g h : Game α) (i j : α) (S : Finset α) :
    pairDelta (fun S => g S+h S) i j S = pairDelta g i j S+pairDelta h i j S := by
  unfold pairDelta; ring
 theorem pairDelta_smul (g : Game α) (i j : α) (S : Finset α) (a : ℝ) :
    pairDelta (fun S => a*g S) i j S = a*pairDelta g i j S := by
  unfold pairDelta; ring
 theorem pairDelta_comm (g : Game α) (i j : α) (S : Finset α) :
    pairDelta g i j S = pairDelta g j i S := by
  unfold pairDelta; rw [insert_comm]; ring
 theorem pairDelta_baseline (g : Game α) (i j : α) (S : Finset α) (b : ℝ) :
    pairDelta (fun S => g S-b) i j S = pairDelta g i j S := by
  unfold pairDelta; ring
 theorem interaction_linearity (g h : Game α) (N : Finset α) (i j : α) (m : ℕ) :
    multiOrderInteraction (fun S => g S+h S) N i j m =
      multiOrderInteraction g N i j m+multiOrderInteraction h N i j m := by
  unfold multiOrderInteraction contextAverage
  rw [show pairDelta (fun S => g S+h S) i j = (fun S => pairDelta g i j S+pairDelta h i j S) from funext (pairDelta_add g h i j)]
  exact average_add _ _ _
 theorem interaction_homogeneity (g : Game α) (N : Finset α) (i j : α) (m : ℕ) (a : ℝ) :
    multiOrderInteraction (fun S => a*g S) N i j m = a*multiOrderInteraction g N i j m := by
  unfold multiOrderInteraction contextAverage
  rw [show pairDelta (fun S => a*g S) i j = (fun S => a*pairDelta g i j S) from funext (fun S => pairDelta_smul g i j S a)]
  exact average_smul _ _ _
 theorem interaction_commutativity (g : Game α) (N : Finset α) (i j : α) (m : ℕ) :
    multiOrderInteraction g N i j m = multiOrderInteraction g N j i m := by
  unfold multiOrderInteraction
  rw [pair_comm]
  rw [show pairDelta g i j = pairDelta g j i from funext (pairDelta_comm g i j)]
 theorem interaction_baseline (g : Game α) (N : Finset α) (i j : α) (m : ℕ) :
    multiOrderInteraction (centered g) N i j m = multiOrderInteraction g N i j m := by
  unfold multiOrderInteraction centered
  rw [show pairDelta (fun S => g S-g ∅) i j = pairDelta g i j from funext (fun S => pairDelta_baseline g i j S (g ∅))]
 theorem interaction_dummy (g : Game α) (N : Finset α) (i j : α) (m : ℕ)
    (hij : i ≠ j) (hj : j ∈ N) (c : ℝ)
    (hd : ∀ S ⊆ N.erase i, g (insert i S)=g S+c) :
    multiOrderInteraction g N i j m = 0 := by
  unfold multiOrderInteraction contextAverage average
  have hh : ∀ S ∈ (N \ {i,j}).powersetCard m, pairDelta g i j S = 0 := by
    intro S hS
    have hSN := (mem_powersetCard.mp hS).1
    have hSi : S ⊆ N.erase i := by
      intro a ha
      have := mem_sdiff.mp (hSN ha)
      simp only [mem_insert, mem_singleton] at this
      exact mem_erase.mpr ⟨fun he => this.2 (Or.inl he), this.1⟩
    have hsji : insert j S ⊆ N.erase i :=
      insert_subset (mem_erase.mpr ⟨Ne.symm hij,hj⟩) hSi
    simp [pairDelta, hd S hSi, hd (insert j S) hsji]
  rw [sum_eq_zero hh]; simp

 theorem attribution_linearity (g h : Game α) (N : Finset α) (i : α) (m : ℕ) :
    multiOrderAttribution (fun S => g S+h S) N i m =
      multiOrderAttribution g N i m+multiOrderAttribution h N i m := by
  unfold multiOrderAttribution contextAverage
  have hh : (fun S => (g (insert i S)+h (insert i S))-(g S+h S)) =
      (fun S => (g (insert i S)-g S)+(h (insert i S)-h S)) := by funext S; ring
  rw [hh, average_add]
 theorem attribution_dummy (g : Game α) (N : Finset α) (i : α) (m : ℕ) (hm : m ≤ (N.erase i).card)
    (c : ℝ) (hd : ∀ S ⊆ N.erase i, g (insert i S)=g S+c) :
    multiOrderAttribution g N i m = c := by
  unfold multiOrderAttribution contextAverage average
  have hh : ∑ S ∈ (N.erase i).powersetCard m, (g (insert i S)-g S) =
      ∑ _S ∈ (N.erase i).powersetCard m, c := by
    apply sum_congr rfl
    intro S hS
    rw [hd S (mem_powersetCard.mp hS).1]; ring
  rw [hh]
  change average ((N.erase i).powersetCard m) (fun _ => c)=c
  exact average_const _ ((powersetCard_nonempty).2 hm) c
 theorem attribution_top (g : Game α) (N : Finset α) (i : α) (hi : i ∈ N) :
    multiOrderAttribution g N i (N.erase i).card = g N-g (N.erase i) := by
  simp [multiOrderAttribution, contextAverage, powersetCard_self, average, insert_erase hi]
 theorem attribution_zero (g : Game α) (N : Finset α) (i : α) :
    multiOrderAttribution g N i 0 = g {i}-g ∅ := by
  simp [multiOrderAttribution, contextAverage, average]
 theorem accumulation_telescope (a : ℕ → ℝ) (m : ℕ) :
    a m = a 0 + ∑ k ∈ range m, (a (k+1)-a k) := by
  induction m with
  | zero => simp
  | succ m ih => rw [sum_range_succ, ← add_assoc, ← ih]; ring

/-- Reindex a flagged subset by adjoining the flag. -/
theorem sum_insert_flags (R : Finset α) (m : ℕ) (f : Game α) :
    (∑ j ∈ R, ∑ S ∈ (R.erase j).powersetCard m, f (insert j S)) =
      (m+1 : ℝ) * ∑ T ∈ R.powersetCard (m+1), f T := by
  have hj (j : α) (hj : j ∈ R) :
      (∑ S ∈ (R.erase j).powersetCard m, f (insert j S)) =
        ∑ T ∈ (R.powersetCard (m+1)).filter (fun T => j ∈ T), f T := by
    refine sum_bij (fun S _ => insert j S) ?_ ?_ ?_ ?_
    · intro S hS
      have hs := mem_powersetCard.mp hS
      have hn : j ∉ S := fun h => (mem_erase.mp (hs.1 h)).1 rfl
      exact mem_filter.mpr ⟨mem_powersetCard.mpr
        ⟨insert_subset hj (hs.1.trans (erase_subset _ _)), by simpa [hn] using hs.2⟩,
        mem_insert_self _ _⟩
    · intro S hS U hU he
      have hn : j ∉ S := fun h => (mem_erase.mp ((mem_powersetCard.mp hS).1 h)).1 rfl
      have hm : j ∉ U := fun h => (mem_erase.mp ((mem_powersetCard.mp hU).1 h)).1 rfl
      simpa [hn,hm] using congrArg (fun T => T.erase j) he
    · intro T hT
      have ht := mem_powersetCard.mp (mem_filter.mp hT).1
      have hjT := (mem_filter.mp hT).2
      refine ⟨T.erase j, mem_powersetCard.mpr ⟨erase_subset_erase j ht.1, ?_⟩, insert_erase hjT⟩
      have hc := card_erase_add_one hjT
      omega
    · intro S _; rfl
  rw [sum_congr rfl hj]
  simp_rw [sum_filter]
  rw [sum_comm]
  calc
    _ = ∑ T ∈ R.powersetCard (m+1), (T.card : ℝ)*f T := by
      apply sum_congr rfl
      intro T hT
      have ht := (mem_powersetCard.mp hT).1
      have hsum : (∑ j ∈ R, if j ∈ T then f T else 0) = ∑ j ∈ T, f T := by
        rw [← sum_filter]
        congr 1
        ext j
        simp only [mem_filter]
        exact ⟨fun h => h.2, fun h => ⟨ht h,h⟩⟩
      rw [hsum]; simp
    _ = _ := by
      rw [mul_sum]
      apply sum_congr rfl
      intro T hT
      rw [(mem_powersetCard.mp hT).2]; simp

 theorem sum_erase_contexts (R : Finset α) (m : ℕ) (f : α → Game α) :
    (∑ j ∈ R, ∑ S ∈ (R.erase j).powersetCard m, f j S) =
      ∑ S ∈ R.powersetCard m, ∑ j ∈ R \ S, f j S := by
  have he (j : α) : (R.erase j).powersetCard m =
      (R.powersetCard m).filter (fun S => j ∉ S) := by
    ext S
    simp only [mem_powersetCard, mem_filter]
    constructor
    · rintro ⟨h,c⟩
      exact ⟨⟨h.trans (erase_subset _ _),c⟩, fun hj => (mem_erase.mp (h hj)).1 rfl⟩
    · rintro ⟨⟨h,c⟩,hn⟩
      exact ⟨fun x hx => mem_erase.mpr ⟨fun h => hn (h ▸ hx),h hx⟩,c⟩
  simp_rw [he, sum_filter]
  rw [sum_comm]
  apply sum_congr rfl
  intro S _
  rw [sdiff_eq_filter, sum_filter]

 theorem sum_erase_same (R : Finset α) (m : ℕ) (f : Game α) :
    (∑ j ∈ R, ∑ S ∈ (R.erase j).powersetCard m, f S) =
      (R.card-m : ℝ) * ∑ S ∈ R.powersetCard m, f S := by
  rw [sum_erase_contexts, mul_sum]
  apply sum_congr rfl
  intro S hS
  have hs := mem_powersetCard.mp hS
  have hc := card_le_card hs.1
  rw [sum_const, nsmul_eq_mul, card_sdiff_of_subset hs.1, hs.2, Nat.cast_sub (by omega)]

 theorem context_average_step (R : Finset α) (m : ℕ) (hm : m < R.card) (f : Game α) :
    contextAverage R (m+1) f - contextAverage R m f =
      average R (fun j => contextAverage (R.erase j) m (fun S => f (insert j S)-f S)) := by
  have hR : (R.card : ℝ) ≠ 0 := by exact_mod_cast (by omega : R.card ≠ 0)
  have h0 : ((R.powersetCard m).card : ℝ) ≠ 0 := by
    exact_mod_cast (card_ne_zero.mpr (powersetCard_nonempty.mpr (by omega)))
  have h1 : ((R.powersetCard (m+1)).card : ℝ) ≠ 0 := by
    exact_mod_cast (card_ne_zero.mpr (powersetCard_nonempty.mpr (by omega)))
  have he : ((R.card-1).choose m : ℝ) ≠ 0 := by
    exact_mod_cast (Nat.ne_of_gt (Nat.choose_pos (by omega)))
  have hcard (j : α) (hj : j ∈ R) :
      ((R.erase j).powersetCard m).card = (R.card-1).choose m := by
    rw [card_powersetCard, card_erase_of_mem hj]
  have hn0 : (R.card : ℝ) * ((R.card-1).choose m : ℝ) =
      (R.card-m : ℝ) * ((R.powersetCard m).card : ℝ) := by
    have h := sum_erase_same R m (fun _ => 1)
    simp only [sum_const, nsmul_eq_mul, mul_one] at h
    rw [sum_congr rfl (fun j hj => congrArg (fun n : ℕ => (n:ℝ)) (hcard j hj))] at h
    simpa using h
  have hn1 : (R.card : ℝ) * ((R.card-1).choose m : ℝ) =
      (m+1 : ℝ) * ((R.powersetCard (m+1)).card : ℝ) := by
    have h := sum_insert_flags R m (fun _ => 1)
    simp only [sum_const, nsmul_eq_mul, mul_one] at h
    rw [sum_congr rfl (fun j hj => congrArg (fun n : ℕ => (n:ℝ)) (hcard j hj))] at h
    simpa using h
  have hs : (∑ j ∈ R, contextAverage (R.erase j) m (fun S => f (insert j S)-f S)) =
      ((R.card-1).choose m : ℝ)⁻¹ *
        ((m+1 : ℝ)*(∑ T ∈ R.powersetCard (m+1), f T) -
         (R.card-m : ℝ)*(∑ S ∈ R.powersetCard m, f S)) := by
    unfold contextAverage average
    rw [sum_congr rfl (fun j hj => by rw [hcard j hj])]
    rw [← mul_sum]
    simp_rw [sum_sub_distrib]
    rw [sum_insert_flags, sum_erase_same]
  change average (R.powersetCard (m+1)) f - average (R.powersetCard m) f = (R.card : ℝ)⁻¹ * _
  rw [hs]
  unfold average
  field_simp [hR,h0,h1,he]
  linear_combination (∑ T ∈ R.powersetCard (m+1), f T) * ((R.powersetCard m).card : ℝ) * hn1 - ((R.powersetCard (m+1)).card : ℝ) * (∑ S ∈ R.powersetCard m, f S) * hn0

 theorem attribution_recurrence (g : Game α) (N : Finset α) (i : α) (m : ℕ)
    (hm : m < (N.erase i).card) :
    multiOrderAttribution g N i (m+1)-multiOrderAttribution g N i m =
      average (N.erase i) (fun j => multiOrderInteraction g N i j m) := by
  rw [multiOrderAttribution, multiOrderAttribution,
    context_average_step (N.erase i) m hm]
  unfold average
  apply congrArg (fun t : ℝ => ((N.erase i).card : ℝ)⁻¹*t)
  apply sum_congr rfl
  intro j hj
  have he : (N.erase i).erase j = N \ {i,j} := by
    ext a; simp only [mem_erase, mem_sdiff, mem_insert, mem_singleton]; tauto
  change contextAverage ((N.erase i).erase j) m (fun S => _) = multiOrderInteraction g N i j m
  rw [he]
  unfold multiOrderInteraction
  apply congrArg (contextAverage (N \ {i,j}) m)
  funext S
  unfold pairDelta
  rw [insert_comm]; ring

 theorem factorial_average_orders (R : Finset α) (f : Game α) :
    (∑ S ∈ R.powerset, factorialWeight 1 R.card S.card*f S) =
      (R.card+1 : ℝ)⁻¹ * ∑ m ∈ range (R.card+1), contextAverage R m f := by
  rw [sum_powerset, mul_sum]
  apply sum_congr rfl
  intro m hm
  have hmR : m ≤ R.card := by have := mem_range.mp hm; omega
  unfold contextAverage average
  simp_rw [mul_sum]
  apply sum_congr rfl
  intro S hS
  rw [(mem_powersetCard.mp hS).2,
    factorialWeight_eq_inv_choose 1 R.card m (by omega) hmR, card_powersetCard]
  simp; ring

 theorem shapley_orders (g : Game α) (N : Finset α) (i : α) (hi : i ∈ N) :
    factorialShapley g N i = (N.card : ℝ)⁻¹ *
      ∑ m ∈ range N.card, multiOrderAttribution g N i m := by
  have hc := card_erase_add_one hi
  unfold factorialShapley
  have ht : ∀ S ∈ (N.erase i).powerset,
    (S.card.factorial : ℝ)*((N.card-S.card-1).factorial : ℝ)/(N.card.factorial : ℝ)*
      (g (insert i S)-g S) = factorialWeight 1 (N.erase i).card S.card*(g (insert i S)-g S) := by
    intro S _
    rw [factorialWeight_one]
    have he : N.card-S.card-1 = (N.erase i).card-S.card := by omega
    rw [he,hc]
  rw [sum_congr rfl ht, factorial_average_orders]
  have hcr : ((N.erase i).card : ℝ)+1 = (N.card : ℝ) := by exact_mod_cast hc
  rw [hc,hcr]; rfl

 theorem shapley_efficiency (g : Game α) (N : Finset α) :
    (∑ i ∈ N, factorialShapley g N i) = g N-g ∅ := by
  rw [sum_congr rfl (fun i hi => factorialShapley_eq_dividendAllocation g N i hi)]
  exact dividendAllocation_efficiency g N

 theorem attribution_efficiency (g : Game α) (N : Finset α) :
    (N.card : ℝ)⁻¹ * (∑ i ∈ N, ∑ m ∈ range N.card, multiOrderAttribution g N i m) =
      g N-g ∅ := by
  rw [mul_sum, ← sum_congr rfl (fun i hi => shapley_orders g N i hi)]
  exact shapley_efficiency g N

 theorem average_sum {β γ : Type*} (s : Finset β) (t : Finset γ) (f : β → γ → ℝ) :
    average s (fun b => ∑ c ∈ t, f b c) = ∑ c ∈ t, average s (fun b => f b c) := by
  unfold average
  rw [sum_comm, mul_sum]

 theorem attribution_accumulation (g : Game α) (N : Finset α) (i : α) (m : ℕ)
    (hm : m ≤ (N.erase i).card) :
    multiOrderAttribution g N i m = multiOrderAttribution g N i 0 +
      average (N.erase i) (fun j => ∑ k ∈ range m, multiOrderInteraction g N i j k) := by
  rw [average_sum]
  have h := accumulation_telescope (multiOrderAttribution g N i) m
  rw [sum_congr rfl (fun k hk => attribution_recurrence g N i k (by have := mem_range.mp hk; omega))] at h
  exact h

 theorem triangular_sum (a : ℕ → ℝ) (n : ℕ) :
    (∑ m ∈ range (n+1), ∑ k ∈ range m, a k) =
      ∑ k ∈ range n, (n-k : ℝ)*a k := by
  induction n with
  | zero => simp
  | succ n ih =>
    rw [sum_range_succ, ih, sum_range_succ]
    rw [sum_range_succ]
    have he : ∀ k ∈ range n, (n+1-k : ℝ)*a k = (n-k : ℝ)*a k + a k := by
      intro k hk
      have hkN := mem_range.mp hk
      ring
    push_cast
    rw [sum_congr rfl he, sum_add_distrib]
    ring

 theorem average_map {β : Type*} [DecidableEq β] (e : α ↪ β) (s : Finset α) (f : β → ℝ) :
    average (s.map e) f = average s (fun a => f (e a)) := by
  simp [average, sum_map]

 theorem contextAverage_map {β : Type*} [DecidableEq β] (e : α ↪ β) (R : Finset α)
    (m : ℕ) (f : Game β) :
    contextAverage (R.map e) m f = contextAverage R m (fun S => f (S.map e)) := by
  unfold contextAverage
  rw [powersetCard_map, average_map]
  rfl

 theorem attribution_relabel (g : Game α) (N : Finset α) (i : α) (m : ℕ) (e : α ≃ α) :
    multiOrderAttribution g (N.map e.toEmbedding) (e i) m =
      multiOrderAttribution (fun S => g (S.map e.toEmbedding)) N i m := by
  unfold multiOrderAttribution
  have he := map_erase e.toEmbedding N i
  simp only [Equiv.coe_toEmbedding] at he
  rw [← he, contextAverage_map]
  apply congrArg (contextAverage (N.erase i) m)
  funext S
  simp [map_insert]

 theorem interaction_relabel (g : Game α) (N : Finset α) (i j : α) (m : ℕ) (e : α ≃ α) :
    multiOrderInteraction g (N.map e.toEmbedding) (e i) (e j) m =
      multiOrderInteraction (fun S => g (S.map e.toEmbedding)) N i j m := by
  unfold multiOrderInteraction
  have he : (N.map e.toEmbedding) \ {e i,e j} = (N \ {i,j}).map e.toEmbedding := by
    simp [map_sdiff]
  rw [he, contextAverage_map]
  apply congrArg (contextAverage (N \ {i,j}) m)
  funext S
  simp [pairDelta, map_insert]

 theorem swap_map_self (i j : α) (S : Finset α) (h : i ∈ S ↔ j ∈ S) :
    S.map (Equiv.swap i j).toEmbedding = S := by
  ext a
  simp only [mem_map_equiv, Equiv.symm_swap]
  by_cases ha : a=i
  · subst a; simpa using h.symm
  by_cases hb : a=j
  · subst a; simpa using h
  rw [Equiv.swap_apply_of_ne_of_ne ha hb]

 theorem swap_game_of_cooperation (g : Game α) (N : Finset α) (i j : α)
    (h : ∀ R ⊆ N \ {i,j}, g (insert i R)=g (insert j R))
    (S : Finset α) (hS : S ⊆ N) :
    g (S.map (Equiv.swap i j).toEmbedding) = g S := by
  by_cases hi : i ∈ S <;> by_cases hj : j ∈ S
  · rw [swap_map_self i j S (by simp [hi,hj])]
  · have hr : S.erase i ⊆ N \ {i,j} := by
      intro a ha
      have hs := mem_erase.mp ha
      exact mem_sdiff.mpr ⟨hS hs.2, by simp only [mem_insert, mem_singleton]; rintro (he | he); exact hs.1 he; exact hj (he ▸ hs.2)⟩
    have hjr : j ∉ S.erase i := fun hh => hj (mem_of_mem_erase hh)
    have he : S.map (Equiv.swap i j).toEmbedding = insert j (S.erase i) := by
      conv_lhs => rw [← insert_erase hi]
      simp only [map_insert, Equiv.coe_toEmbedding, Equiv.swap_apply_left]
      rw [swap_map_self i j (S.erase i) (by simp [hjr])]
    rw [he, ← h (S.erase i) hr, insert_erase hi]
  · have hr : S.erase j ⊆ N \ {i,j} := by
      intro a ha
      have hs := mem_erase.mp ha
      exact mem_sdiff.mpr ⟨hS hs.2, by simp only [mem_insert, mem_singleton]; rintro (he | he); exact hi (he ▸ hs.2); exact hs.1 he⟩
    have hir : i ∉ S.erase j := fun hh => hi (mem_of_mem_erase hh)
    have he : S.map (Equiv.swap i j).toEmbedding = insert i (S.erase j) := by
      conv_lhs => rw [← insert_erase hj]
      simp only [map_insert, Equiv.coe_toEmbedding, Equiv.swap_apply_right]
      rw [swap_map_self i j (S.erase j) (by simp [hir])]
    rw [he, h (S.erase j) hr, insert_erase hj]
  · rw [swap_map_self i j S (by simp [hi,hj])]

 theorem attribution_congr (g h : Game α) (N : Finset α) (i : α) (m : ℕ)
    (hi : i ∈ N) (hh : ∀ S ⊆ N, g S=h S) :
    multiOrderAttribution g N i m = multiOrderAttribution h N i m := by
  unfold multiOrderAttribution contextAverage average
  congr 1
  apply sum_congr rfl
  intro S hS
  have hs := (mem_powersetCard.mp hS).1.trans (erase_subset _ _)
  change g (insert i S)-g S = h (insert i S)-h S
  rw [hh S hs, hh (insert i S) (insert_subset hi hs)]

 theorem interaction_congr (g h : Game α) (N : Finset α) (i j : α) (m : ℕ)
    (hi : i ∈ N) (hj : j ∈ N) (hh : ∀ S ⊆ N, g S=h S) :
    multiOrderInteraction g N i j m = multiOrderInteraction h N i j m := by
  unfold multiOrderInteraction contextAverage average
  congr 1
  apply sum_congr rfl
  intro S hS
  have hs := (mem_powersetCard.mp hS).1.trans sdiff_subset
  unfold pairDelta
  rw [hh S hs, hh (insert i S) (insert_subset hi hs), hh (insert j S) (insert_subset hj hs),
    hh (insert i (insert j S)) (insert_subset hi (insert_subset hj hs))]

 theorem attribution_symmetry (g : Game α) (N : Finset α) (i j : α) (m : ℕ)
    (hi : i ∈ N) (hj : j ∈ N)
    (h : ∀ R ⊆ N \ {i,j}, g (insert i R)=g (insert j R)) :
    multiOrderAttribution g N i m = multiOrderAttribution g N j m := by
  have hn := swap_map_self i j N (by simp [hi,hj])
  have he := attribution_relabel g N i m (Equiv.swap i j)
  rw [hn, Equiv.swap_apply_left] at he
  rw [he]
  exact attribution_congr g _ N i m hi (fun S hS => (swap_game_of_cooperation g N i j h S hS).symm)

 theorem interaction_symmetry (g : Game α) (N : Finset α) (i j k : α) (m : ℕ)
    (hi : i ∈ N) (hj : j ∈ N) (hk : k ∈ N) (hki : k ≠ i) (hkj : k ≠ j)
    (h : ∀ R ⊆ N \ {i,j}, g (insert i R)=g (insert j R)) :
    multiOrderInteraction g N i k m = multiOrderInteraction g N j k m := by
  have hn := swap_map_self i j N (by simp [hi,hj])
  have he := interaction_relabel g N i k m (Equiv.swap i j)
  rw [hn, Equiv.swap_apply_left, Equiv.swap_apply_of_ne_of_ne hki hkj] at he
  rw [he]
  exact interaction_congr g _ N i k m hi hk (fun S hS => (swap_game_of_cooperation g N i j h S hS).symm)

 theorem order_sum_accumulation (g : Game α) (N : Finset α) (i : α) (hi : i ∈ N) :
    (∑ m ∈ range N.card, multiOrderAttribution g N i m) =
      (N.card : ℝ)*multiOrderAttribution g N i 0 +
        average (N.erase i) (fun j => ∑ k ∈ range (N.erase i).card,
          ((N.erase i).card-k : ℝ)*multiOrderInteraction g N i j k) := by
  have hc := card_erase_add_one hi
  rw [sum_congr rfl (fun m hm => attribution_accumulation g N i m (by have := mem_range.mp hm; omega))]
  rw [sum_add_distrib]
  simp only [sum_const, card_range, nsmul_eq_mul]
  congr 1
  rw [← average_sum, ← hc]
  apply congrArg (average (N.erase i))
  funext j
  exact triangular_sum (multiOrderInteraction g N i j) (N.erase i).card

 theorem interaction_efficiency (g : Game α) (N : Finset α) (hN : 2 ≤ N.card) :
    g N = g ∅ + (∑ i ∈ N, multiOrderAttribution g N i 0) +
      ∑ i ∈ N, ∑ j ∈ N.erase i, ∑ m ∈ range (N.card-1),
        ((N.card : ℝ)-1-m)/((N.card : ℝ)*((N.card : ℝ)-1))*multiOrderInteraction g N i j m := by
  have hn : (N.card : ℝ) ≠ 0 := by exact_mod_cast (by omega : N.card ≠ 0)
  have hn1 : (N.card : ℝ)-1 ≠ 0 := by
    have hreal : (2:ℝ) ≤ N.card := by exact_mod_cast hN
    linarith
  have hp (i : α) (hi : i ∈ N) :
    (N.card : ℝ)⁻¹*(∑ m ∈ range N.card, multiOrderAttribution g N i m) =
      multiOrderAttribution g N i 0 + ∑ j ∈ N.erase i, ∑ m ∈ range (N.card-1),
        ((N.card : ℝ)-1-m)/((N.card : ℝ)*((N.card : ℝ)-1))*multiOrderInteraction g N i j m := by
    rw [order_sum_accumulation g N i hi]
    have hc : (N.erase i).card = N.card-1 := card_erase_of_mem hi
    have hcr : ((N.erase i).card : ℝ) = (N.card : ℝ)-1 := by
      rw [hc, Nat.cast_sub (by omega), Nat.cast_one]
    unfold average
    have hcrN : ((N.card-1 : ℕ):ℝ) = (N.card : ℝ)-1 := by rw [← hc,hcr]
    rw [hc,hcrN,mul_add,mul_sum]
    have hbase : (N.card : ℝ)⁻¹*((N.card : ℝ)*multiOrderAttribution g N i 0) =
      multiOrderAttribution g N i 0 := by field_simp
    rw [hbase]
    congr 1
    simp_rw [mul_sum]
    apply sum_congr rfl
    intro j hj
    apply sum_congr rfl
    intro m hm
    field_simp [hn,hn1]
  have h := attribution_efficiency g N
  rw [mul_sum, sum_congr rfl hp, sum_add_distrib] at h
  linarith

/-- The conditional-information convention is the source Eq. (7) convention. -/
noncomputable def conditionalMI (H : Game α) (i : α) (S : Finset α) : ℝ :=
  H S-H (insert i S)
noncomputable def conditionalCoI (H : Game α) (i j : α) (S : Finset α) : ℝ :=
  conditionalMI H i S-conditionalMI H i (insert j S)
 theorem entropy_interaction (H : Game α) (N : Finset α) (i j : α) (m : ℕ) :
    multiOrderInteraction H N i j m =
      contextAverage (N \ {i,j}) m (conditionalCoI H i j) := by
  unfold multiOrderInteraction
  apply congrArg (contextAverage (N \ {i,j}) m)
  funext S
  unfold conditionalCoI conditionalMI pairDelta
  ring
 theorem entropy_shared_benefit (H : Game α) (i j : α) (S : Finset α) :
    H S-H (insert i (insert j S)) =
      conditionalMI H i (insert j S)+conditionalMI H j (insert i S)+conditionalCoI H i j S := by
  simp only [conditionalCoI,conditionalMI]
  rw [insert_comm]; ring

 theorem average_abs_le {β : Type*} (s : Finset β) (f : β → ℝ) :
    |average s f| ≤ average s (fun t => |f t|) := by
  have hn : 0 ≤ (s.card : ℝ)⁻¹ := by positivity
  unfold average
  rw [abs_mul, abs_of_nonneg hn]
  exact mul_le_mul_of_nonneg_left (abs_sum_le_sum_abs _ _) hn
 theorem disentanglement_bounds {β : Type*} (s : Finset β) (f : β → ℝ)
    (hd : 0 < average s (fun t => |f t|)) :
    0 ≤ |average s f|/average s (fun t => |f t|) ∧
      |average s f|/average s (fun t => |f t|) ≤ 1 := by
  exact ⟨div_nonneg (abs_nonneg _) hd.le, (div_le_one hd).mpr (average_abs_le s f)⟩
 theorem disentanglement_zero_domain {β : Type*} (s : Finset β) :
    average s (fun _ => |(0:ℝ)|)=0 := by simp [average]

noncomputable def cardinalGame : Game α := fun S => (S.card : ℝ)
 theorem cardinal_game_interaction (N : Finset α) (i j : α) (m : ℕ) (hij : i ≠ j) (hj : j ∈ N) :
    multiOrderInteraction cardinalGame N i j m = 0 := by
  apply interaction_dummy cardinalGame N i j m hij hj 1
  intro S hS
  have hn : i ∉ S := fun h => (mem_erase.mp (hS h)).1 rfl
  simp [cardinalGame, hn]
 theorem fixed_size_cardinal_mean (N : Finset α) (k : ℕ) (hk : k ≤ N.card) :
    contextAverage N k cardinalGame = (k : ℝ) := by
  unfold contextAverage
  have he : ∀ S ∈ N.powersetCard k, cardinalGame S = (k : ℝ) :=
    fun S hS => by rw [cardinalGame, (mem_powersetCard.mp hS).2]
  unfold average
  rw [sum_congr rfl he]
  exact average_const _ (powersetCard_nonempty.mpr hk) _
 theorem fixed_size_floor_counterexample :
    Nat.floor ((1-(2/5:ℝ))*4) = 2 ∧
      contextAverage (univ : Finset (Fin 4)) 2 cardinalGame ≠ (1-(2/5:ℝ))*4 := by
  constructor
  · norm_num [Nat.floor_eq_iff]
  · rw [fixed_size_cardinal_mean _ _ (by simp)]
    norm_num

 theorem attribution_homogeneity (g : Game α) (N : Finset α) (i : α) (m : ℕ) (c : ℝ) :
    multiOrderAttribution (fun S => c*g S) N i m = c*multiOrderAttribution g N i m := by
  unfold multiOrderAttribution
  have he : (fun S => c*g (insert i S)-c*g S) = (fun S => c*(g (insert i S)-g S)) := by funext S; ring
  rw [he]
  exact average_smul _ _ _
 theorem shapley_linearity (g h : Game α) (N : Finset α) (i : α) (hi : i ∈ N) :
    factorialShapley (fun S => g S+h S) N i = factorialShapley g N i+factorialShapley h N i := by
  simp_rw [shapley_orders _ N i hi, attribution_linearity, sum_add_distrib, mul_add]
 theorem shapley_homogeneity (g : Game α) (N : Finset α) (i : α) (hi : i ∈ N) (c : ℝ) :
    factorialShapley (fun S => c*g S) N i = c*factorialShapley g N i := by
  simp_rw [shapley_orders _ N i hi, attribution_homogeneity, ← mul_sum]
  ring
 theorem shapley_dummy (g : Game α) (N : Finset α) (i : α) (hi : i ∈ N) (c : ℝ)
    (hd : ∀ S ⊆ N.erase i, g (insert i S)=g S+c) :
    factorialShapley g N i = c := by
  rw [shapley_orders g N i hi]
  have hc := card_erase_add_one hi
  have he : ∀ m ∈ range N.card, multiOrderAttribution g N i m = c := by
    intro m hm
    apply attribution_dummy g N i m (by have := mem_range.mp hm; omega) c hd
  rw [sum_congr rfl he]
  have hn : (N.card : ℝ) ≠ 0 := by exact_mod_cast (by omega : N.card ≠ 0)
  simp [hn]
 theorem shapley_symmetry (g : Game α) (N : Finset α) (i j : α) (hi : i ∈ N) (hj : j ∈ N)
    (h : ∀ R ⊆ N \ {i,j}, g (insert i R)=g (insert j R)) :
    factorialShapley g N i = factorialShapley g N j := by
  rw [shapley_orders g N i hi, shapley_orders g N j hj]
  simp_rw [attribution_symmetry g N i j _ hi hj h]
 theorem interaction_sub (g h : Game α) (N : Finset α) (i j : α) (m : ℕ) :
    multiOrderInteraction (fun S => g S-h S) N i j m =
      multiOrderInteraction g N i j m-multiOrderInteraction h N i j m := by
  have he : (fun S => g S-h S) = (fun S => g S+(-1)*h S) := by funext S; ring
  rw [he,interaction_linearity,interaction_homogeneity]; ring
 theorem attribution_sub (g h : Game α) (N : Finset α) (i : α) (m : ℕ) :
    multiOrderAttribution (fun S => g S-h S) N i m =
      multiOrderAttribution g N i m-multiOrderAttribution h N i m := by
  have he : (fun S => g S-h S) = (fun S => g S+(-1)*h S) := by funext S; ring
  rw [he,attribution_linearity,attribution_homogeneity]; ring
 theorem attacking_decomposition (normal attacked : Game α) (N : Finset α) (hN : 2 ≤ N.card) :
    attacked N-normal N = attacked ∅-normal ∅+
      (∑ i ∈ N, (multiOrderAttribution attacked N i 0-multiOrderAttribution normal N i 0)) -
        ∑ i ∈ N, ∑ j ∈ N.erase i, ∑ m ∈ range (N.card-1),
          ((N.card : ℝ)-1-m)/((N.card : ℝ)*((N.card : ℝ)-1))*
          (multiOrderInteraction normal N i j m-multiOrderInteraction attacked N i j m) := by
  have h := interaction_efficiency (fun S => attacked S-normal S) N hN
  simp only [attribution_sub,interaction_sub] at h
  convert h using 1
  simp_rw [mul_sub, sum_sub_distrib]
  ring

 theorem source_dummy_baseline (g : Game α) (N : Finset α) (i : α)
    (hd : ∀ S ⊆ N.erase i, g (insert i S)=g S+g {i}) : g ∅=0 := by
  have h := hd ∅ (empty_subset _)
  simp only [insert_empty_eq] at h
  linarith
 theorem source_shapley_dummy (g : Game α) (N : Finset α) (i : α) (hi : i ∈ N)
    (hd : ∀ S ⊆ N.erase i, g (insert i S)=g S+g {i}) :
    factorialShapley g N i = g {i}-g ∅ := by
  rw [source_dummy_baseline g N i hd,sub_zero]
  exact shapley_dummy g N i hi (g {i}) hd

noncomputable def conditionalShapleyDifference (g : Game α) (N : Finset α) (i j : α) : ℝ :=
  factorialShapley (fun S => g (insert j S)) (N.erase j) i-factorialShapley g (N.erase j) i
 theorem shapley_interaction_orders (g : Game α) (N : Finset α) (i j : α)
    (hi : i ∈ N) (hj : j ∈ N) (hij : i ≠ j) :
    conditionalShapleyDifference g N i j = ((N.card-1 : ℕ):ℝ)⁻¹ *
      ∑ m ∈ range (N.card-1), multiOrderInteraction g N i j m := by
  have hie : i ∈ N.erase j := mem_erase.mpr ⟨hij,hi⟩
  unfold conditionalShapleyDifference
  rw [shapley_orders _ _ _ hie,shapley_orders _ _ _ hie, ← mul_sub, ← sum_sub_distrib]
  have he : (N.erase j).erase i = N \ {i,j} := by
    ext a; simp only [mem_erase, mem_sdiff, mem_insert, mem_singleton]; tauto
  have ht : ∀ m ∈ range (N.erase j).card,
    multiOrderAttribution (fun S => g (insert j S)) (N.erase j) i m-
      multiOrderAttribution g (N.erase j) i m = multiOrderInteraction g N i j m := by
    intro m hm
    unfold multiOrderAttribution contextAverage
    rw [← average_sub,he]
    unfold multiOrderInteraction contextAverage
    apply congrArg (average ((N \ {i,j}).powersetCard m))
    funext S
    unfold pairDelta
    rw [insert_comm]; ring
  rw [sum_congr rfl ht,card_erase_of_mem hj]

 theorem source_attack_decomposition (normal attacked : Game α) (N : Finset α) (hN : 2 ≤ N.card) :
    normal N-attacked N = normal ∅-attacked ∅+
      (∑ i ∈ N, (multiOrderAttribution normal N i 0-multiOrderAttribution attacked N i 0)) +
        ∑ i ∈ N, ∑ j ∈ N.erase i, ∑ m ∈ range (N.card-1),
          ((N.card : ℝ)-1-m)/((N.card : ℝ)*((N.card : ℝ)-1))*
          (multiOrderInteraction normal N i j m-multiOrderInteraction attacked N i j m) := by
  have h := interaction_efficiency (fun S => normal S-attacked S) N hN
  simpa only [attribution_sub,interaction_sub] using h

 theorem flag_count_identity (R : Finset α) (m : ℕ) :
    (m+1 : ℝ)*(R.card.choose (m+1) : ℝ) =
      (R.card-m : ℝ)*(R.card.choose m : ℝ) ∧
    (R.card-m : ℝ)*(R.card.choose m : ℝ) =
      (R.card : ℝ)*((R.card-1).choose m : ℝ) := by
  have ht (j : α) (hj : j ∈ R) : ((R.erase j).powersetCard m).card = (R.card-1).choose m := by
    rw [card_powersetCard,card_erase_of_mem hj]
  have h0 := sum_erase_same R m (fun _ => 1)
  have h1 := sum_insert_flags R m (fun _ => 1)
  simp only [sum_const,nsmul_eq_mul,mul_one,card_powersetCard] at h0 h1
  simp_rw [card_powersetCard] at ht
  have hx : (∑ j ∈ R, ((R.erase j).card.choose m : ℝ)) =
      (R.card : ℝ)*((R.card-1).choose m : ℝ) := by
    rw [sum_congr rfl (fun j hj => congrArg (fun n : ℕ => (n:ℝ)) (ht j hj))]
    simp
  rw [hx] at h0 h1
  exact ⟨h1.symm.trans h0,h0.symm⟩

 theorem average_nonneg {β : Type*} (s : Finset β) (f : β → ℝ) (h : ∀ t ∈ s, 0 ≤ f t) :
    0 ≤ average s f := mul_nonneg (by positivity) (sum_nonneg h)
 theorem average_nonpos {β : Type*} (s : Finset β) (f : β → ℝ) (h : ∀ t ∈ s, f t ≤ 0) :
    average s f ≤ 0 := mul_nonpos_of_nonneg_of_nonpos (by positivity) (sum_nonpos h)
 theorem disentanglement_same_sign_nonneg {β : Type*} (s : Finset β) (f : β → ℝ)
    (hd : 0 < average s (fun t => |f t|)) (h : ∀ t ∈ s, 0 ≤ f t) :
    |average s f|/average s (fun t => |f t|)=1 := by
  have he : average s (fun t => |f t|)=average s f := by
    unfold average
    rw [sum_congr rfl (fun t ht => abs_of_nonneg (h t ht))]
  rw [he,abs_of_nonneg (average_nonneg s f h)]
  rw [he] at hd
  exact div_self (ne_of_gt hd)
 theorem disentanglement_same_sign_nonpos {β : Type*} (s : Finset β) (f : β → ℝ)
    (hd : 0 < average s (fun t => |f t|)) (h : ∀ t ∈ s, f t ≤ 0) :
    |average s f|/average s (fun t => |f t|)=1 := by
  have he : average s (fun t => |f t|) = -average s f := by
    unfold average
    rw [sum_congr rfl (fun t ht => abs_of_nonpos (h t ht)),sum_neg_distrib]
    ring
  rw [abs_of_nonpos (average_nonpos s f h), ← he]
  exact div_self (ne_of_gt hd)
 theorem shapley_interaction_commutativity (g : Game α) (N : Finset α) (i j : α)
    (hi : i ∈ N) (hj : j ∈ N) (hij : i ≠ j) :
    conditionalShapleyDifference g N i j=conditionalShapleyDifference g N j i := by
  rw [shapley_interaction_orders g N i j hi hj hij,
    shapley_interaction_orders g N j i hj hi hij.symm]
  simp_rw [interaction_commutativity g N i j]
/-- A linear sum model on all-one inputs and zero input masks realizes the counterexample game. -/
noncomputable def linearMaskedSum [Fintype α] (S : Finset α) : ℝ :=
  ∑ i : α, if i ∈ S then 1 else 0
 theorem linear_masked_sum_cardinal [Fintype α] (S : Finset α) :
    linearMaskedSum S=cardinalGame S := by
  unfold linearMaskedSum cardinalGame
  rw [sum_boole,filter_mem_eq_inter,univ_inter]

end Harsanyi.Robustness
