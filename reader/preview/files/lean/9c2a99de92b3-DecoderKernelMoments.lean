import Harsanyi.Extensions.DecoderMoments
import Harsanyi.Extensions.DecoderFourier

namespace Harsanyi.Frequency
open Finset AddChar MeasureTheory ProbabilityTheory
open scoped BigOperators
variable {Ω : Type*} [MeasurableSpace Ω]
variable {M N K : ℕ} [NeZero M] [NeZero N]
variable (μ : Measure Ω) [IsProbabilityMeasure μ]

noncomputable def phaseSum (u : ZMod M) (v : ZMod N) : ℂ :=
  ∑ t : Fin K × Fin K, gridCharacter u v (squareShift K t)

noncomputable def randomKernelResponse (W : Fin K × Fin K → Ω → ℝ)
    (u : ZMod M) (v : ZMod N) (ω : Ω) : ℂ :=
  offsetResponse (squareShift K) (fun t => (W t ω : ℂ)) u v

theorem random_response_weighted (W : Fin K × Fin K → Ω → ℝ)
    (u : ZMod M) (v : ZMod N) :
    randomKernelResponse W u v = weightedResponse
      (fun t => gridCharacter u v (squareShift K t)) W := by
  funext ω
  simp only [randomKernelResponse,offsetResponse,weightedResponse,mul_comm]

theorem grid_phase_normSq (u : ZMod M) (v : ZMod N) (x : Grid M N) :
    Complex.normSq (gridCharacter u v x) = 1 := by
  simp only [grid_character_apply,Complex.normSq_mul,Complex.normSq_eq_norm_sq,
    ZMod.stdAddChar_apply,norm_mul,Circle.norm_coe,one_pow,mul_one]

theorem grid_phase_square (u : ZMod M) (v : ZMod N) (x : Grid M N) :
    (gridCharacter u v x)^2 = gridCharacter (2*u) (2*v) x := by
  simp only [grid_character_apply,pow_two,two_mul,add_mul,map_add_eq_mul]
  ring

theorem actual_kernel_mean (W : Fin K × Fin K → Ω → ℝ) (m : ℝ) (q : NNReal)
    (hm : ∀ t, Measurable (W t)) (hl : ∀ t, μ.map (W t) = gaussianReal m q)
    (u : ZMod M) (v : ZMod N) :
    (∫ ω, randomKernelResponse W u v ω ∂μ) = (m : ℂ)*phaseSum (K:=K) u v := by
  have h := fun t => ConceptGaussian.gaussian_feature_moments μ (W t) m q (hm t) (hl t)
  rw [random_response_weighted,weighted_response_mean μ _ W (fun t => (h t).1)]
  simp_rw [(h _).2.1]
  simp only [phaseSum,mul_sum,mul_comm]

theorem actual_kernel_second_moment (W : Fin K × Fin K → Ω → ℝ) (m : ℝ) (q : NNReal)
    (hm : ∀ t, Measurable (W t)) (hl : ∀ t, μ.map (W t) = gaussianReal m q)
    (hi : iIndepFun W μ) (u : ZMod M) (v : ZMod N) :
    (∫ ω, Complex.normSq (randomKernelResponse W u v ω) ∂μ) =
      Complex.normSq ((m : ℂ)*phaseSum (K:=K) u v) + (K*K : ℕ)*(q : ℝ) := by
  rw [random_response_weighted,gaussian_weighted_second_moment μ _ W
    (fun _ => m) (fun _ => q) hm hl hi]
  simp only [grid_phase_normSq,one_mul,sum_const,card_univ,Fintype.card_prod,
    Fintype.card_fin,nsmul_eq_mul,phaseSum]
  congr 1
  rw [mul_sum]
  apply congrArg Complex.normSq
  apply sum_congr rfl
  intro t _
  ring

theorem actual_kernel_pseudocovariance (W : Fin K × Fin K → Ω → ℝ) (m : ℝ) (q : NNReal)
    (hm : ∀ t, Measurable (W t)) (hl : ∀ t, μ.map (W t) = gaussianReal m q)
    (hi : iIndepFun W μ) (u : ZMod M) (v : ZMod N) :
    (∫ ω, (randomKernelResponse W u v ω - ∫ z,randomKernelResponse W u v z ∂μ)^2 ∂μ) =
      (q : ℂ)*phaseSum (K:=K) (2*u) (2*v) := by
  rw [random_response_weighted,gaussian_weighted_pseudocovariance μ _ W
    (fun _ => m) (fun _ => q) hm hl hi]
  simp_rw [grid_phase_square]
  simp only [phaseSum,mul_sum,mul_comm]

theorem actual_kernel_gaussian (W : Fin K × Fin K → Ω → ℝ) (m : ℝ) (q : NNReal)
    (hm : ∀ t, Measurable (W t)) (hl : ∀ t, μ.map (W t) = gaussianReal m q)
    (hi : iIndepFun W μ) (u : ZMod M) (v : ZMod N) :
    IsGaussian (μ.map (randomKernelResponse W u v)) := by
  rw [random_response_weighted]
  exact gaussian_weighted_isGaussian μ _ W (fun _ => m) (fun _ => q) hm hl hi

end Harsanyi.Frequency
