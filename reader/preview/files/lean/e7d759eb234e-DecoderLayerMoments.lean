import Harsanyi.Extensions.DecoderKernelMoments

namespace Harsanyi.Frequency
open Finset MeasureTheory ProbabilityTheory
open scoped BigOperators
variable {Ω ι : Type*} [MeasurableSpace Ω] [Fintype ι] [DecidableEq ι]
variable {M N K : ℕ} [NeZero M] [NeZero N]
variable (μ : Measure Ω) [IsProbabilityMeasure μ]

theorem independent_complex_product_mean (T : ι → Ω → ℂ)
    (hm : ∀ l, Measurable (T l)) (hi : iIndepFun T μ) :
    (∫ ω, ∏ l,T l ω ∂μ) = ∏ l, ∫ ω,T l ω ∂μ :=
  hi.integral_fun_prod_eq_prod_integral (fun l => (hm l).aestronglyMeasurable)

theorem actual_independent_layer_mean
    (W : ι → Fin K × Fin K → Ω → ℝ) (m : ι → ℝ) (q : ι → NNReal)
    (hm : ∀ l t, Measurable (W l t))
    (hl : ∀ l t, μ.map (W l t) = gaussianReal (m l) (q l))
    (hlayers : iIndepFun (fun l ω => fun t => W l t ω) μ)
    (u : ZMod M) (v : ZMod N) :
    (∫ ω, ∏ l,randomKernelResponse (W l) u v ω ∂μ) =
      ∏ l, (m l : ℂ)*phaseSum (K:=K) u v := by
  have hT : ∀ l, Measurable (randomKernelResponse (W l) u v) := by
    intro l
    unfold randomKernelResponse offsetResponse
    fun_prop
  have hiT : iIndepFun (fun l => randomKernelResponse (W l) u v) μ :=
    hlayers.comp
      (fun _ z => offsetResponse (squareShift K) (fun t => (z t : ℂ)) u v)
      (fun _ => by unfold offsetResponse; fun_prop)
  rw [independent_complex_product_mean μ _ hT hiT]
  apply prod_congr rfl
  intro l _
  exact actual_kernel_mean μ (W l) (m l) (q l) (hm l) (hl l) u v

theorem independent_complex_product_second_moment (T : ι → Ω → ℂ)
    (hm : ∀ l, Measurable (T l)) (hi : iIndepFun T μ) :
    (∫ ω, Complex.normSq (∏ l,T l ω) ∂μ) =
      ∏ l, ∫ ω,Complex.normSq (T l ω) ∂μ := by
  have hN : iIndepFun (fun l ω => Complex.normSq (T l ω)) μ :=
    hi.comp (fun _ z => Complex.normSq z) (fun _ => by fun_prop)
  have hmN : ∀ l, AEStronglyMeasurable (fun ω => Complex.normSq (T l ω)) μ := by
    intro l
    exact (by fun_prop : Measurable (fun ω => Complex.normSq (T l ω))).aestronglyMeasurable
  simp only [map_prod]
  exact TaylorMoments.product_mean hN hmN

theorem actual_independent_layer_moments
    (W : ι → Fin K × Fin K → Ω → ℝ) (m : ι → ℝ) (q : ι → NNReal)
    (hm : ∀ l t, Measurable (W l t))
    (hl : ∀ l t, μ.map (W l t) = gaussianReal (m l) (q l))
    (hwithin : ∀ l, iIndepFun (W l) μ)
    (hlayers : iIndepFun (fun l ω => fun t => W l t ω) μ)
    (u : ZMod M) (v : ZMod N) :
    (∫ ω, Complex.normSq (∏ l,randomKernelResponse (W l) u v ω) ∂μ) =
      ∏ l, (Complex.normSq ((m l : ℂ)*phaseSum (K:=K) u v)+(K*K : ℕ)*(q l : ℝ)) := by
  have hT : ∀ l, Measurable (randomKernelResponse (W l) u v) := by
    intro l
    unfold randomKernelResponse offsetResponse
    fun_prop
  have hiT : iIndepFun (fun l => randomKernelResponse (W l) u v) μ := by
    have h := hlayers.comp
      (fun _ z => offsetResponse (squareShift K) (fun t => (z t : ℂ)) u v)
      (fun _ => by unfold offsetResponse; fun_prop)
    exact h
  rw [independent_complex_product_second_moment μ _ hT hiT]
  apply prod_congr rfl
  intro l _
  exact actual_kernel_second_moment μ (W l) (m l) (q l) (hm l) (hl l) (hwithin l) u v

theorem actual_independent_layer_log_moments
    (W : ι → Fin K × Fin K → Ω → ℝ) (m : ι → ℝ) (q : ι → NNReal)
    (hm : ∀ l t, Measurable (W l t))
    (hl : ∀ l t, μ.map (W l t) = gaussianReal (m l) (q l))
    (hwithin : ∀ l, iIndepFun (W l) μ)
    (hlayers : iIndepFun (fun l ω => fun t => W l t ω) μ)
    (hK : 0<K) (hq : ∀ l, 0<(q l : ℝ)) (u : ZMod M) (v : ZMod N) :
    Real.log (∫ ω,Complex.normSq (∏ l,randomKernelResponse (W l) u v ω) ∂μ) =
      ∑ l,Real.log (Complex.normSq ((m l : ℂ)*phaseSum (K:=K) u v)+(K*K : ℕ)*(q l : ℝ)) := by
  rw [actual_independent_layer_moments μ W m q hm hl hwithin hlayers u v]
  apply Real.log_prod
  intro l _
  have hp : 0<Complex.normSq ((m l : ℂ)*phaseSum (K:=K) u v)+(K*K : ℕ)*(q l : ℝ) := by
    have hn := Complex.normSq_nonneg ((m l : ℂ)*phaseSum (K:=K) u v)
    have hc : (0:ℝ)<(K*K : ℕ) := Nat.cast_pos.mpr (Nat.mul_pos hK hK)
    exact add_pos_of_nonneg_of_pos hn (mul_pos hc (hq l))
  exact ne_of_gt hp

end Harsanyi.Frequency
