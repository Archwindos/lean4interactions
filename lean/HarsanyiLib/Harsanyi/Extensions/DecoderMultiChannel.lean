import Harsanyi.Extensions.DecoderLayerMoments
import Harsanyi.Extensions.DecoderCascade

/-! Genuine probability-space row/column moments. A product of first moments
is not used as a replacement for independence. -/
namespace Harsanyi.Frequency.MultiChannel
open Finset MeasureTheory ProbabilityTheory
open scoped BigOperators
variable {Ω C : Type*} [MeasurableSpace Ω] [Fintype C] [DecidableEq C]
variable (μ : Measure Ω) [IsProbabilityMeasure μ]

theorem complex_cross_moment (X : C → Ω → ℂ)
    (hm : ∀ c,Measurable (X c)) (hp : ∀ c,MemLp (X c) 2 μ)
    (hi : Pairwise (fun i j => IndepFun (X i) (X j) μ))
    (m : ℂ) (s : ℝ) (he : ∀ c,∫ ω,X c ω ∂μ = m)
    (hs : ∀ c,∫ ω,Complex.normSq (X c ω) ∂μ = s) (i j : C) :
    (∫ ω,X i ω*starRingEnd ℂ (X j ω) ∂μ) =
      if i=j then (s : ℂ) else m*starRingEnd ℂ m := by
  by_cases hij : i=j
  · subst j
    simp only [if_pos rfl,Complex.mul_conj]
    rw [integral_complex_ofReal,hs]
    simp
  · rw [if_neg hij]
    have hc := (hi hij).comp measurable_id (by fun_prop : Measurable (starRingEnd ℂ))
    have h := hc.integral_fun_mul_eq_mul_integral (hm i).aestronglyMeasurable
      (by fun_prop : Measurable (fun ω => starRingEnd ℂ (X j ω))).aestronglyMeasurable
    simp only [Function.comp_apply,id_eq] at h
    rw [h]
    rw [integral_conj,he i,he j]

theorem row_column_mean (A X : C → Ω → ℂ)
    (hmA : ∀ c,Measurable (A c)) (hmX : ∀ c,Measurable (X c))
    (hpA : ∀ c,MemLp (A c) 2 μ) (hpX : ∀ c,MemLp (X c) 2 μ)
    (hi : IndepFun (fun ω c => A c ω) (fun ω c => X c ω) μ)
    (a m : ℂ) (heA : ∀ c,∫ ω,A c ω ∂μ = a)
    (heX : ∀ c,∫ ω,X c ω ∂μ = m) :
    (∫ ω,∑ c,A c ω*X c ω ∂μ) = (Fintype.card C : ℂ)*a*m := by
  have hp (c : C) : Integrable (fun ω => A c ω*X c ω) μ := by
    simpa only [Pi.mul_apply] using (hpA c).integrable_mul (hpX c)
  rw [integral_finset_sum _ (fun c _ => hp c)]
  have hh (c : C) : IndepFun (A c) (X c) μ :=
    hi.comp (measurable_pi_apply c) (measurable_pi_apply c)
  simp_rw [(hh _).integral_fun_mul_eq_mul_integral
    (hmA _).aestronglyMeasurable (hmX _).aestronglyMeasurable,heA,heX]
  simp [mul_assoc]

theorem row_column_second_moment (A X : C → Ω → ℂ)
    (hmA : ∀ c,Measurable (A c)) (hmX : ∀ c,Measurable (X c))
    (hpA : ∀ c,MemLp (A c) 2 μ) (hpX : ∀ c,MemLp (X c) 2 μ)
    (hiA : Pairwise (fun i j => IndepFun (A i) (A j) μ))
    (hiX : Pairwise (fun i j => IndepFun (X i) (X j) μ))
    (hi : IndepFun (fun ω c => A c ω) (fun ω c => X c ω) μ)
    (a m : ℂ) (b s : ℝ) (heA : ∀ c,∫ ω,A c ω ∂μ = a)
    (heX : ∀ c,∫ ω,X c ω ∂μ = m)
    (hsA : ∀ c,∫ ω,Complex.normSq (A c ω) ∂μ = b)
    (hsX : ∀ c,∫ ω,Complex.normSq (X c ω) ∂μ = s) :
    (∫ ω,Complex.normSq (∑ c,A c ω*X c ω) ∂μ) =
      (Fintype.card C : ℝ)*b*s +
        (Fintype.card C : ℝ)*((Fintype.card C : ℝ)-1)*Complex.normSq (a*m) := by
  have hAA (i j : C) : Integrable (fun ω => A i ω*starRingEnd ℂ (A j ω)) μ := by
    simpa only [Pi.star_apply] using (hpA i).integrable_mul (hpA j).star
  have hXX (i j : C) : Integrable (fun ω => X i ω*starRingEnd ℂ (X j ω)) μ := by
    simpa only [Pi.star_apply] using (hpX i).integrable_mul (hpX j).star
  have hij (i j : C) : IndepFun
      (fun ω => A i ω*starRingEnd ℂ (A j ω))
      (fun ω => X i ω*starRingEnd ℂ (X j ω)) μ :=
    hi.comp (by fun_prop : Measurable (fun z : C → ℂ => z i*starRingEnd ℂ (z j)))
      (by fun_prop : Measurable (fun z : C → ℂ => z i*starRingEnd ℂ (z j)))
  have hZ (i j : C) : Integrable
      (fun ω => (A i ω*X i ω)*starRingEnd ℂ (A j ω*X j ω)) μ := by
    have h := (hij i j).integrable_mul (hAA i j) (hXX i j)
    convert h using 1
    funext ω
    simp only [Pi.mul_apply,map_mul]
    ring
  have hE (i j : C) : (∫ ω,(A i ω*X i ω)*starRingEnd ℂ (A j ω*X j ω) ∂μ) =
      if i=j then ((b*s : ℝ) : ℂ) else (Complex.normSq (a*m) : ℂ) := by
    have hpoint (ω : Ω) :
        (A i ω*X i ω)*starRingEnd ℂ (A j ω*X j ω) =
          (A i ω*starRingEnd ℂ (A j ω))*(X i ω*starRingEnd ℂ (X j ω)) := by
      simp only [map_mul]
      ring
    simp_rw [hpoint]
    rw [(hij i j).integral_fun_mul_eq_mul_integral (hAA i j).aestronglyMeasurable
      (hXX i j).aestronglyMeasurable,
      complex_cross_moment μ A hmA hpA hiA a b heA hsA,
      complex_cross_moment μ X hmX hpX hiX m s heX hsX]
    split_ifs with h
    · simp
    · rw [← Complex.mul_conj]
      simp only [map_mul]
      ring
  have hn (ω : Ω) : (Complex.normSq (∑ c,A c ω*X c ω) : ℂ) =
      ∑ i,∑ j,(A i ω*X i ω)*starRingEnd ℂ (A j ω*X j ω) := by
    rw [← Complex.mul_conj,map_sum,sum_mul]
    simp_rw [mul_sum]
  apply Complex.ofReal_injective
  rw [← integral_complex_ofReal]
  simp_rw [hn]
  rw [integral_finset_sum _ (fun i _ => integrable_finset_sum _ (fun j _ => hZ i j))]
  simp_rw [integral_finset_sum _ (fun j _ => hZ _ j),hE]
  have hi' (i j : C) : (if i=j then ((b*s : ℝ) : ℂ) else (Complex.normSq (a*m) : ℂ)) =
      (Complex.normSq (a*m) : ℂ) +
        if i=j then ((b*s-Complex.normSq (a*m) : ℝ) : ℂ) else 0 := by
    split_ifs <;> push_cast <;> ring
  simp_rw [hi']
  simp only [sum_add_distrib,sum_ite_eq,mem_univ,if_true,sum_const,card_univ,nsmul_eq_mul]
  push_cast
  ring

theorem independent_complex_mul_memLp {A X : Ω → ℂ}
    (hmA : Measurable A) (hmX : Measurable X) (hpA : MemLp A 2 μ) (hpX : MemLp X 2 μ)
    (hi : IndepFun A X μ) : MemLp (fun ω => A ω*X ω) 2 μ := by
  apply (memLp_two_iff_integrable_sq_norm (by fun_prop)).2
  have hN := hi.comp (by fun_prop : Measurable (fun z : ℂ => ‖z‖^2))
    (by fun_prop : Measurable (fun z : ℂ => ‖z‖^2))
  have h := hN.integrable_mul
    (hpA.integrable_norm_pow (by norm_num : (2:ℕ) ≠ 0))
    (hpX.integrable_norm_pow (by norm_num : (2:ℕ) ≠ 0))
  simpa only [Pi.mul_apply,Function.comp_apply,norm_mul,mul_pow] using h

theorem actual_gaussian_row_moments {M N K : ℕ} [NeZero M] [NeZero N]
    (W : C → Fin K × Fin K → Ω → ℝ) (X : C → Ω → ℂ)
    (hmW : ∀ c t,Measurable (W c t)) (hmX : ∀ c,Measurable (X c))
    (mW : ℝ) (q : NNReal) (hl : ∀ c t,μ.map (W c t) = gaussianReal mW q)
    (hiW : iIndepFun (fun c ω t => W c t ω) μ)
    (hiWithin : ∀ c,iIndepFun (W c) μ)
    (hpX : ∀ c,MemLp (X c) 2 μ) (hiX : iIndepFun X μ)
    (hi : IndepFun (fun ω c t => W c t ω) (fun ω c => X c ω) μ)
    (mX : ℂ) (sX : ℝ) (heX : ∀ c,∫ ω,X c ω ∂μ = mX)
    (hsX : ∀ c,∫ ω,Complex.normSq (X c ω) ∂μ = sX) (u : ZMod M) (v : ZMod N) :
    (∫ ω,∑ c,randomKernelResponse (W c) u v ω*X c ω ∂μ) =
      (Fintype.card C : ℂ)*((mW : ℂ)*phaseSum (K:=K) u v)*mX ∧
    (∫ ω,Complex.normSq (∑ c,randomKernelResponse (W c) u v ω*X c ω) ∂μ) =
      (Fintype.card C : ℝ)*
        (Complex.normSq ((mW : ℂ)*phaseSum (K:=K) u v)+(K*K : ℕ)*(q : ℝ))*sX +
      (Fintype.card C : ℝ)*((Fintype.card C : ℝ)-1)*
        Complex.normSq (((mW : ℂ)*phaseSum (K:=K) u v)*mX) := by
  let A := fun c => randomKernelResponse (W c) u v
  have hmA : ∀ c,Measurable (A c) := by
    intro c
    unfold A randomKernelResponse offsetResponse
    fun_prop
  have hpA : ∀ c,MemLp (A c) 2 μ := by
    intro c
    change MemLp (randomKernelResponse (W c) u v) 2 μ
    rw [random_response_weighted]
    exact weighted_response_memLp μ _ (W c) (fun t =>
      (ConceptGaussian.gaussian_feature_moments μ (W c t) mW q (hmW c t) (hl c t)).1)
  have hiA : iIndepFun A μ :=
    hiW.comp (fun _ z => offsetResponse (squareShift K) (fun t => (z t : ℂ)) u v)
      (fun _ => by unfold offsetResponse; fun_prop)
  have hAX : IndepFun (fun ω c => A c ω) (fun ω c => X c ω) μ :=
    by
    have h := hi.comp (by
      change Measurable (fun z : C → Fin K × Fin K → ℝ =>
        fun c => offsetResponse (squareShift K) (fun t => (z c t : ℂ)) u v)
      unfold offsetResponse
      fun_prop) measurable_id
    simpa only [Function.comp_apply,id_eq] using h
  exact ⟨row_column_mean μ A X hmA hmX hpA hpX hAX _ _
      (fun c => actual_kernel_mean μ (W c) mW q (hmW c) (hl c) u v) heX,
    row_column_second_moment μ A X hmA hmX hpA hpX
      (fun _ _ h => hiA.indepFun h) (fun _ _ h => hiX.indepFun h) hAX _ _ _ _
      (fun c => actual_kernel_mean μ (W c) mW q (hmW c) (hl c) u v) heX
      (fun c => actual_kernel_second_moment μ (W c) mW q (hmW c) (hl c) (hiWithin c) u v) hsX⟩

section RandomCascade
variable (S : ℕ → Type*) [∀ n,Fintype (S n)] [∀ n,DecidableEq (S n)]
abbrev RandomMatrix (n : ℕ) := S (n+1) → S n → ℂ

noncomputable def matrixLinear {n : ℕ} (A : RandomMatrix S n) :
    (S n → ℂ) →ₗ[ℂ] (S (n+1) → ℂ) where
  toFun := fun z d => ∑ c,A d c*z c
  map_add' := by intro z t; funext d; simp [mul_add,sum_add_distrib]
  map_smul' := by intro a z; funext d; simp [mul_left_comm,mul_sum]

noncomputable def cascadeEntry (A : ∀ n,Ω → RandomMatrix S n) (L : ℕ)
    (c : S 0) (d : S L) (ω : Ω) : ℂ :=
  cascadeLinear S (fun n => matrixLinear S (A n ω)) L (Pi.single c 1) d

theorem cascade_entry_succ (A : ∀ n,Ω → RandomMatrix S n) (L : ℕ)
    (c : S 0) (d : S (L+1)) (ω : Ω) :
    cascadeEntry S A (L+1) c d ω = ∑ e,A L ω d e*cascadeEntry S A L c e ω := rfl

theorem cascade_entry_measurable (A : ∀ n,Ω → RandomMatrix S n)
    (hm : ∀ n,Measurable (A n)) (L : ℕ) (c : S 0) (d : S L) :
    Measurable (cascadeEntry S A L c d) := by
  induction L with
  | zero => exact measurable_const
  | succ L ih =>
    change Measurable (fun ω => ∑ e,A L ω d e*cascadeEntry S A L c e ω)
    apply Finset.measurable_fun_sum
    intro e _
    exact ((measurable_pi_apply e).comp ((measurable_pi_apply d).comp (hm L))).mul (ih e)

theorem cascade_entry_prefix_congr (A B : ∀ n,Ω → RandomMatrix S n) (L : ℕ)
    (h : ∀ n<L,A n=B n) (c : S 0) (d : S L) :
    cascadeEntry S A L c d = cascadeEntry S B L c d := by
  induction L with
  | zero => rfl
  | succ L ih =>
    funext ω
    rw [cascade_entry_succ,cascade_entry_succ,h L (Nat.lt_succ_self L)]
    apply sum_congr rfl
    intro e _
    rw [congrFun (ih (fun n hn => h n (Nat.lt_trans hn (Nat.lt_succ_self L))) e) ω]

noncomputable def pastMatrices (L : ℕ)
    (z : (j : range L) → RandomMatrix S j) (n : ℕ) : RandomMatrix S n :=
  if h : n<L then z ⟨n,mem_range.mpr h⟩ else 0

theorem past_matrices_measurable (L n : ℕ) :
    Measurable (fun z : (j : range L) → RandomMatrix S j => pastMatrices S L z n) := by
  unfold pastMatrices
  split_ifs <;> fun_prop

theorem independent_layer_prefix (A : ∀ n,Ω → RandomMatrix S n)
    (hm : ∀ n,Measurable (A n)) (hi : iIndepFun A μ) (L : ℕ) (c : S 0) :
    IndepFun (A L) (fun ω d => cascadeEntry S A L c d ω) μ := by
  have hd : Disjoint ({L} : Finset ℕ) (range L) := by simp
  have hb := hi.indepFun_finset {L} (range L) hd hm
  let eval := fun z : (j : ({L}:Finset ℕ)) → RandomMatrix S j => z ⟨L,by simp⟩
  let pastColumn := fun z : (j : range L) → RandomMatrix S j =>
    fun d => cascadeEntry S (fun n (_ : Unit) => pastMatrices S L z n) L c d ()
  have he : Measurable eval := by unfold eval; fun_prop
  have hp : Measurable pastColumn := by
    unfold pastColumn
    apply measurable_pi_lambda
    intro d
    have h := cascade_entry_measurable S
      (fun n (z : (j : range L) → RandomMatrix S j) => pastMatrices S L z n)
      (past_matrices_measurable S L) L c d
    exact h
  have h := hb.comp he hp
  have hprefix (ω : Ω) (d : S L) :
      pastColumn (fun j : range L => A j ω) d = cascadeEntry S A L c d ω := by
    have heq := cascade_entry_prefix_congr S
      (fun n (_ : Unit) => pastMatrices S L (fun j : range L => A j ω) n)
      (fun n (_ : Unit) => A n ω) L (by
        intro n hn
        funext x
        simp [pastMatrices,hn]) c d
    exact congrFun heq ()
  have heq : (eval ∘ fun ω j => A j ω) = A L := rfl
  have hp_eq : (pastColumn ∘ fun ω (j : range L) => A j ω) =
      fun ω d => cascadeEntry S A L c d ω := by
    funext ω d
    exact hprefix ω d
  rw [heq,hp_eq] at h
  exact h

noncomputable def meanSequence (a : ℕ → ℂ) : ℕ → ℂ
  | 0 => a 0
  | n+1 => (Fintype.card (S (n+1)) : ℂ)*a (n+1)*meanSequence a n

noncomputable def somSequence (a : ℕ → ℂ) (b : ℕ → ℝ) : ℕ → ℝ
  | 0 => b 0
  | n+1 => (Fintype.card (S (n+1)) : ℝ)*b (n+1)*somSequence a b n+
      (Fintype.card (S (n+1)) : ℝ)*((Fintype.card (S (n+1)) : ℝ)-1)*
        Complex.normSq (a (n+1)*meanSequence S a n)

theorem actual_cascade_uniform_moments (A : ∀ n,Ω → RandomMatrix S n)
    (hm : ∀ n,Measurable (A n))
    (hp : ∀ n d c,MemLp (fun ω => A n ω d c) 2 μ)
    (hi : iIndepFun A μ)
    (hrow : ∀ n d,iIndepFun (fun c ω => A n ω d c) μ)
    (hprefix : ∀ n c,iIndepFun (fun d => cascadeEntry S A (n+1) c d) μ)
    (a : ℕ → ℂ) (b : ℕ → ℝ)
    (he : ∀ n d c,∫ ω,A n ω d c ∂μ = a n)
    (hs : ∀ n d c,∫ ω,Complex.normSq (A n ω d c) ∂μ = b n)
    (n : ℕ) :
    ∀ c d,MemLp (cascadeEntry S A (n+1) c d) 2 μ ∧
      (∫ ω,cascadeEntry S A (n+1) c d ω ∂μ) = meanSequence S a n ∧
      (∫ ω,Complex.normSq (cascadeEntry S A (n+1) c d ω) ∂μ) = somSequence S a b n := by
  have hbase (c : S 0) (d : S 1) :
      cascadeEntry S A 1 c d = fun ω => A 0 ω d c := by
    funext ω
    simp [cascadeEntry,cascadeLinear,matrixLinear,Pi.single_apply]
  induction n with
  | zero =>
    intro c d
    rw [hbase]
    exact ⟨hp 0 d c,he 0 d c,hs 0 d c⟩
  | succ n ih =>
    intro c d
    let X := fun e => cascadeEntry S A (n+1) c e
    let R := fun e ω => A (n+1) ω d e
    have hmX : ∀ e,Measurable (X e) := fun e => cascade_entry_measurable S A hm (n+1) c e
    have hmR : ∀ e,Measurable (R e) := fun e =>
      (measurable_pi_apply e).comp ((measurable_pi_apply d).comp (hm (n+1)))
    have hpX : ∀ e,MemLp (X e) 2 μ := fun e => (ih c e).1
    have hpR : ∀ e,MemLp (R e) 2 μ := hp (n+1) d
    have hRX : IndepFun (fun ω e => R e ω) (fun ω e => X e ω) μ := by
      have h := (independent_layer_prefix μ S A hm hi (n+1) c).comp
        (measurable_pi_apply d) measurable_id
      simpa only [Function.comp_apply,id_eq] using h
    have hprod : ∀ e,MemLp (fun ω => R e ω*X e ω) 2 μ := by
      intro e
      have h := hRX.comp (measurable_pi_apply e) (measurable_pi_apply e)
      exact independent_complex_mul_memLp μ (hmR e) (hmX e) (hpR e) (hpX e) h
    have hout : cascadeEntry S A (n+2) c d = fun ω => ∑ e,R e ω*X e ω := by
      funext ω
      exact cascade_entry_succ S A (n+1) c d ω
    rw [hout]
    refine ⟨?_,?_,?_⟩
    · have hsum := memLp_finset_sum' univ (fun e _ => hprod e)
      have hs : (∑ e,fun ω => R e ω*X e ω) = fun ω => ∑ e,R e ω*X e ω := by
        funext ω
        simp
      rw [hs] at hsum
      exact hsum
    · exact row_column_mean μ R X hmR hmX hpR hpX hRX (a (n+1)) (meanSequence S a n)
        (he (n+1) d) (fun e => (ih c e).2.1)
    · exact row_column_second_moment μ R X hmR hmX hpR hpX
        (fun _ _ h => (hrow (n+1) d).indepFun h)
        (fun _ _ h => (hprefix n c).indepFun h) hRX
        (a (n+1)) (meanSequence S a n) (b (n+1)) (somSequence S a b n)
        (he (n+1) d) (fun e => (ih c e).2.1)
        (hs (n+1) d) (fun e => (ih c e).2.2)

theorem mean_sequence_product (a : ℕ → ℂ) (n : ℕ) :
    (Fintype.card (S (n+1)) : ℂ)*meanSequence S a n =
      ∏ j ∈ range (n+1),(Fintype.card (S (j+1)) : ℂ)*a j := by
  induction n with
  | zero => simp [meanSequence]
  | succ n ih =>
    rw [meanSequence,prod_range_succ,← ih]
    ring

noncomputable def sourceMean (a : ℕ → ℂ) (n : ℕ) : ℂ :=
  (Fintype.card (S (n+1)) : ℂ)⁻¹ *
    ∏ j ∈ range (n+1),(Fintype.card (S (j+1)) : ℂ)*a j

theorem mean_sequence_source_closed (a : ℕ → ℂ) (n : ℕ)
    (hC : Fintype.card (S (n+1)) ≠ 0) :
    meanSequence S a n = sourceMean S a n := by
  rw [sourceMean,← mean_sequence_product]
  exact (inv_mul_cancel_left₀ (Nat.cast_ne_zero.mpr hC) _).symm

noncomputable def affineSequence (d e : ℕ → ℝ) (s : ℝ) : ℕ → ℝ
  | 0 => s
  | n+1 => d n*affineSequence d e s n+e n

theorem finite_affine_expansion (d e : ℕ → ℝ) (s : ℝ) (n : ℕ) :
    affineSequence d e s n =
      s*(∏ j ∈ range n,d j)+∑ i ∈ range n,e i*(∏ j ∈ Ico (i+1) n,d j) := by
  induction n with
  | zero => simp [affineSequence]
  | succ n ih =>
    have hsum :
        (∑ i ∈ range n,e i*(∏ j ∈ Ico (i+1) (n+1),d j)) =
          (∑ i ∈ range n,e i*(∏ j ∈ Ico (i+1) n,d j))*d n := by
      rw [sum_mul]
      apply sum_congr rfl
      intro i hi
      rw [prod_Ico_succ_top (Nat.succ_le_iff.mpr (mem_range.mp hi))]
      ring
    rw [affineSequence,ih,prod_range_succ,sum_range_succ,hsum]
    simp only [Ico_self,prod_empty,mul_one]
    ring

noncomputable def diagonalCoefficient (b : ℕ → ℝ) (j : ℕ) : ℝ :=
  (Fintype.card (S (j+1)) : ℝ)*b (j+1)

noncomputable def crossCoefficient (a : ℕ → ℂ) (j : ℕ) : ℝ :=
  (Fintype.card (S (j+1)) : ℝ)*((Fintype.card (S (j+1)) : ℝ)-1)*
    Complex.normSq (a (j+1)*meanSequence S a j)

theorem som_sequence_affine (a : ℕ → ℂ) (b : ℕ → ℝ) (n : ℕ) :
    somSequence S a b n =
      affineSequence (diagonalCoefficient S b) (crossCoefficient S a) (b 0) n := by
  induction n with
  | zero => rfl
  | succ n ih => simp only [somSequence,affineSequence,diagonalCoefficient,crossCoefficient,ih]

theorem cross_coefficient_source (a : ℕ → ℂ) (j : ℕ)
    (hC : Fintype.card (S (j+1)) ≠ 0) :
    crossCoefficient S a j =
      ((Fintype.card (S (j+1)) : ℝ)-1)/(Fintype.card (S (j+1)) : ℝ)*
        Complex.normSq (meanSequence S a (j+1)) := by
  simp only [crossCoefficient,meanSequence,Complex.normSq_mul,Complex.normSq_natCast]
  have hc : (Fintype.card (S (j+1)) : ℝ) ≠ 0 := Nat.cast_ne_zero.mpr hC
  field_simp

theorem diagonal_product_source (b : ℕ → ℝ) (n : ℕ) :
    (Fintype.card (S (n+1)) : ℝ)*
      (b 0*(∏ j ∈ range n,diagonalCoefficient S b j)) =
      ∏ j ∈ range (n+1),(Fintype.card (S (j+1)) : ℝ)*b j := by
  induction n with
  | zero => simp
  | succ n ih =>
    rw [prod_range_succ,prod_range_succ,diagonalCoefficient,← ih]
    ring

noncomputable def sourceSOM (a : ℕ → ℂ) (b : ℕ → ℝ) (n : ℕ) : ℝ :=
  (Fintype.card (S (n+1)) : ℝ)⁻¹ *
    (∏ j ∈ range (n+1),(Fintype.card (S (j+1)) : ℝ)*b j)+
  ∑ i ∈ range n,((Fintype.card (S (i+1)) : ℝ)-1)/(Fintype.card (S (i+1)) : ℝ)*
    Complex.normSq (sourceMean S a (i+1))*
      (∏ j ∈ Ico (i+1) n,diagonalCoefficient S b j)

theorem som_sequence_source_closed (a : ℕ → ℂ) (b : ℕ → ℝ) (n : ℕ)
    (hC : ∀ j≤n,Fintype.card (S (j+1)) ≠ 0) :
    somSequence S a b n = sourceSOM S a b n := by
  rw [som_sequence_affine,finite_affine_expansion]
  unfold sourceSOM
  congr 1
  · rw [← diagonal_product_source]
    exact (inv_mul_cancel_left₀ (Nat.cast_ne_zero.mpr (hC n le_rfl)) _).symm
  · apply sum_congr rfl
    intro i hi
    rw [cross_coefficient_source S a i (hC i (Nat.le_of_lt (mem_range.mp hi))),
      mean_sequence_source_closed S a (i+1) (hC (i+1) (Nat.succ_le_iff.mpr (mem_range.mp hi)))]

theorem actual_cascade_source_closed (A : ∀ n,Ω → RandomMatrix S n)
    (hm : ∀ n,Measurable (A n)) (hp : ∀ n d c,MemLp (fun ω => A n ω d c) 2 μ)
    (hi : iIndepFun A μ) (hrow : ∀ n d,iIndepFun (fun c ω => A n ω d c) μ)
    (hprefix : ∀ n c,iIndepFun (fun d => cascadeEntry S A (n+1) c d) μ)
    (a : ℕ → ℂ) (b : ℕ → ℝ)
    (he : ∀ n d c,∫ ω,A n ω d c ∂μ = a n)
    (hs : ∀ n d c,∫ ω,Complex.normSq (A n ω d c) ∂μ = b n)
    (n : ℕ) (hC : ∀ j≤n,Fintype.card (S (j+1)) ≠ 0) (c : S 0) (d : S (n+1)) :
    (∫ ω,cascadeEntry S A (n+1) c d ω ∂μ) = sourceMean S a n ∧
    (∫ ω,Complex.normSq (cascadeEntry S A (n+1) c d ω) ∂μ) = sourceSOM S a b n := by
  have h := actual_cascade_uniform_moments μ S A hm hp hi hrow hprefix a b he hs n c d
  rw [h.2.1,h.2.2,mean_sequence_source_closed S a n (hC n le_rfl),
    som_sequence_source_closed S a b n hC]
  exact ⟨rfl,rfl⟩

noncomputable def kernelMatrices {M N K : ℕ} [NeZero M] [NeZero N]
    (W : ∀ n,S (n+1) → S n → Fin K × Fin K → Ω → ℝ)
    (u : ZMod M) (v : ZMod N) : ∀ n,Ω → RandomMatrix S n :=
  fun n ω d c => randomKernelResponse (W n d c) u v ω

theorem actual_gaussian_cascade_closed {M N K : ℕ} [NeZero M] [NeZero N]
    (W : ∀ n,S (n+1) → S n → Fin K × Fin K → Ω → ℝ)
    (hmW : ∀ n d c t,Measurable (W n d c t))
    (m : ℕ → ℝ) (q : ℕ → NNReal)
    (hl : ∀ n d c t,μ.map (W n d c t) = gaussianReal (m n) (q n))
    (hwithin : ∀ n d c,iIndepFun (W n d c) μ)
    (hrows : ∀ n d,iIndepFun (fun c ω t => W n d c t ω) μ)
    (hlayers : iIndepFun (fun n ω d c t => W n d c t ω) μ)
    (u : ZMod M) (v : ZMod N)
    (hprefix : ∀ n c,iIndepFun
      (fun d => cascadeEntry S (kernelMatrices S W u v) (n+1) c d) μ)
    (n : ℕ) (hC : ∀ j≤n,Fintype.card (S (j+1)) ≠ 0) (c : S 0) (d : S (n+1)) :
    (∫ ω,cascadeEntry S (kernelMatrices S W u v) (n+1) c d ω ∂μ) =
      sourceMean S (fun j => (m j : ℂ)*phaseSum (K:=K) u v) n ∧
    (∫ ω,Complex.normSq (cascadeEntry S (kernelMatrices S W u v) (n+1) c d ω) ∂μ) =
      sourceSOM S (fun j => (m j : ℂ)*phaseSum (K:=K) u v)
        (fun j => Complex.normSq ((m j : ℂ)*phaseSum (K:=K) u v)+(K*K : ℕ)*(q j : ℝ)) n := by
  let A := kernelMatrices S W u v
  have hmA : ∀ j,Measurable (A j) := by
    intro j
    apply measurable_pi_lambda
    intro d
    apply measurable_pi_lambda
    intro c
    unfold A kernelMatrices randomKernelResponse offsetResponse
    fun_prop
  have hpA : ∀ j d c,MemLp (fun ω => A j ω d c) 2 μ := by
    intro j d c
    change MemLp (randomKernelResponse (W j d c) u v) 2 μ
    rw [random_response_weighted]
    exact weighted_response_memLp μ _ (W j d c) (fun t =>
      (ConceptGaussian.gaussian_feature_moments μ (W j d c t) (m j) (q j)
        (hmW j d c t) (hl j d c t)).1)
  have hiA : iIndepFun A μ :=
    hlayers.comp
      (fun _ z => fun d c => offsetResponse (squareShift K) (fun t => (z d c t : ℂ)) u v)
      (fun _ => by unfold offsetResponse; fun_prop)
  have hrowA : ∀ j d,iIndepFun (fun c ω => A j ω d c) μ := by
    intro j d
    exact (hrows j d).comp
      (fun _ z => offsetResponse (squareShift K) (fun t => (z t : ℂ)) u v)
      (fun _ => by unfold offsetResponse; fun_prop)
  exact actual_cascade_source_closed μ S A hmA hpA hiA hrowA hprefix _ _
    (fun j d c => actual_kernel_mean μ (W j d c) (m j) (q j)
      (hmW j d c) (hl j d c) u v)
    (fun j d c => actual_kernel_second_moment μ (W j d c) (m j) (q j)
      (hmW j d c) (hl j d c) (hwithin j d c) u v) n hC c d

end RandomCascade
end Harsanyi.Frequency.MultiChannel
