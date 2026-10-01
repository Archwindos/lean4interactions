import Harsanyi.Extensions.DecoderMatrixBackprop
import Harsanyi.Extensions.DecoderMultiChannel
import Harsanyi.Extensions.DecoderCounterexample
import Harsanyi.Extensions.DecoderPadding
import Harsanyi.Extensions.DecoderUpsampling
import Harsanyi.Extensions.DecoderDepthCounterexample
import Harsanyi.Extensions.DecoderValid
import Harsanyi.Extensions.DecoderParameterCounterexamples
import Harsanyi.Extensions.DecoderWeakIndependence

/-! Formal-paper adapters. Each actual loss derivative is tied to the same
network state and functional used in its frequency update. -/
namespace PaperDecoder
open Harsanyi.Frequency Harsanyi.Frequency.MatrixBackprop Finset
open scoped BigOperators
variable {M N K : ℕ} [NeZero M] [NeZero N]
variable (P S : ℕ → Type*) [∀ n,Fintype (P n)] [∀ n,DecidableEq (P n)]
variable [∀ n,Fintype (S n)] [∀ n,DecidableEq (S n)]

theorem actual_corollary_3_4
    (pw : ∀ n,P (n+1) → P n → Fin K × Fin K → ℝ)
    (pb : ∀ n,P (n+1) → ℝ)
    (input : Feature (M:=M) (N:=N) (P 0)) (p : ℕ)
    (sw : ∀ n,S (n+1) → S n → Fin K × Fin K → ℝ)
    (sb : ∀ n,S (n+1) → ℝ) (L : ℕ)
    (w : S 0 × P p × (Fin K × Fin K) → ℝ) (b : S 0 → ℝ)
    (Loss : Feature (M:=M) (N:=N) (S L) → ℝ)
    (J : Feature (M:=M) (N:=N) (S L) →L[ℝ] ℝ)
    (hLoss : HasFDerivAt Loss J (realNetwork S (squareShift K) sw sb
      (realKernelCLM (squareShift K)
        (fun c x => realNetwork P (squareShift K) pw pb input p (c,x)) w +
        fun y => b y.1) L))
    (d : S 0) (c : P p) (η : ℝ) (u : ZMod M) (v : ZMod N) :
    let F := realNetwork P (squareShift K) pw pb input p
    let wholeLoss := fun z => Loss (realNetwork S (squareShift K) sw sb
      (realKernelCLM (squareShift K) (fun c x => F (c,x)) z+fun y => b y.1) L)
    let gradient := (J.comp (networkCLM S (squareShift K) sw L)).comp
      (realKernelCLM (squareShift K) (fun c x => F (c,x)))
    HasFDerivAt wholeLoss gradient w ∧
      offsetResponse (squareShift K)
        (fun t => ((w (d,c,t)-η*(fderiv ℝ wholeLoss w) (Pi.single (d,c,t) 1) : ℝ) : ℂ)) u v -
        offsetResponse (squareShift K) (fun t => (w (d,c,t) : ℂ)) u v =
      -(η : ℂ)*((M*N : ℕ) : ℂ)*
        ∑ k : Grid M N,crossFrequencyKernel (squareShift K) u k.1 v k.2 *
          starRingEnd ℂ (featureSpectrum F k.1 k.2 c) *
          conjugateTranspose (cascadeLinear S
            (fun n => responseLinear (squareShift K) (sw n) k.1 k.2) L)
            (normalizedSpectrum (riesz J) k.1 k.2) d := by
  dsimp only
  have hD := actual_cascade_parameter_loss_hasFDerivAt P S (squareShift K)
    pw pb input p sw sb L w (fun y => b y.1) Loss J hLoss
  constructor
  · exact hD
  · rw [hD.fderiv,actual_response_gradient_update,actual_kernel_spectral_gradient,mul_assoc]
    congr 1
    congr 1
    apply sum_congr rfl
    intro k _
    rw [actual_suffix_cotangent]

section GaussianCascade
open MeasureTheory ProbabilityTheory Harsanyi.Frequency.MultiChannel
variable {Ω : Type*} [MeasurableSpace Ω]
variable (μ : Measure Ω) [IsProbabilityMeasure μ]

/-- A.4 Equations (31)--(32), under the genuinely independent reading of the
additional prose. Prefix-column independence remains explicit: it is not
inferred from the weaker first-moment displays or from layer independence. -/
theorem actual_appendix_equations31_32
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
    (n : ℕ) (hC : ∀ j≤n,1 < Fintype.card (S (j+1)))
    (c : S 0) (d : S (n+1)) :
    (∫ ω,cascadeEntry S (kernelMatrices S W u v) (n+1) c d ω ∂μ) =
      sourceMean S (fun j => (m j : ℂ)*phaseSum (K:=K) u v) n ∧
    (∫ ω,Complex.normSq (cascadeEntry S (kernelMatrices S W u v) (n+1) c d ω) ∂μ) =
      sourceSOM S (fun j => (m j : ℂ)*phaseSum (K:=K) u v)
        (fun j => Complex.normSq ((m j : ℂ)*phaseSum (K:=K) u v)+(K*K : ℕ)*(q j : ℝ)) n := by
  exact actual_gaussian_cascade_closed μ S W hmW m q hl hwithin hrows hlayers
    u v hprefix n (fun j hj => Nat.ne_of_gt (lt_trans (by decide) (hC j hj))) c d
end GaussianCascade
/-- Ratios of the independently proved finite products, on their ordinary
nonzero denominator domain. This does not assert a training probability. -/
theorem finite_moment_ratio (a b : Fin L → ℝ) :
    (∏ l,a l)/(∏ l,b l) = ∏ l,a l/b l := by
  exact (Finset.prod_div_distrib a b).symm

theorem moment_factor_mono {r₀ r₁ t₀ t₁ c₀ c₁ : ℝ}
    (hr₀ : 0≤r₀) (ht₀ : 0≤t₀) (hr : r₀≤r₁) (ht : t₀≤t₁) (hc : c₀≤c₁) :
    t₀*r₀+c₀ ≤ t₁*r₁+c₁ := by
  nlinarith [mul_nonneg (sub_nonneg.mpr ht) (sub_nonneg.mpr hr)]

theorem mean_preference_ratio_mono {rLow rHigh t₀ t₁ c : ℝ}
    (hr : 0≤rHigh) (hLH : rHigh≤rLow) (ht : 0≤t₀)
    (hT : t₀≤t₁) (hc : 0<c) :
    (t₀*rLow+c)/(t₀*rHigh+c) ≤ (t₁*rLow+c)/(t₁*rHigh+c) := by
  have h0 : 0<t₀*rHigh+c := add_pos_of_nonneg_of_pos (mul_nonneg ht hr) hc
  have h1 : 0<t₁*rHigh+c := add_pos_of_nonneg_of_pos
    (mul_nonneg (le_trans ht hT) hr) hc
  rw [div_le_div_iff₀ h0 h1]
  nlinarith [mul_nonneg (sub_nonneg.mpr hT) (sub_nonneg.mpr hLH),
    mul_nonneg (mul_nonneg (sub_nonneg.mpr hT) (sub_nonneg.mpr hLH)) hc.le]

section PositiveMomentFactors
open MeasureTheory ProbabilityTheory
variable {Ω ι : Type*} [MeasurableSpace Ω] [Fintype ι] [DecidableEq ι]
variable (μ : Measure Ω) [IsProbabilityMeasure μ]

/-- The source logarithm on its full ordinary positive-moment domain.
Positive Gaussian variances are sufficient, but zero variances with nonzero
mean responses are also covered. -/
theorem actual_positive_factor_log_som
    (W : ι → Fin K × Fin K → Ω → ℝ) (m : ι → ℝ) (q : ι → NNReal)
    (hm : ∀ l t,Measurable (W l t))
    (hl : ∀ l t,μ.map (W l t) = gaussianReal (m l) (q l))
    (hwithin : ∀ l,iIndepFun (W l) μ)
    (hlayers : iIndepFun (fun l ω => fun t => W l t ω) μ)
    (u : ZMod M) (v : ZMod N)
    (hpos : ∀ l,0 < Complex.normSq ((m l : ℂ)*phaseSum (K:=K) u v)+
      (K*K : ℕ)*(q l : ℝ)) :
    Real.log (∫ ω,Complex.normSq (∏ l,randomKernelResponse (W l) u v ω) ∂μ) =
      ∑ l,Real.log (Complex.normSq ((m l : ℂ)*phaseSum (K:=K) u v)+
        (K*K : ℕ)*(q l : ℝ)) := by
  rw [actual_independent_layer_moments μ W m q hm hl hwithin hlayers u v]
  apply Real.log_prod
  intro l _
  exact ne_of_gt (hpos l)
end PositiveMomentFactors
end PaperDecoder
