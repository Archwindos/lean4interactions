import Harsanyi.Extensions.ConceptGaussian
import Harsanyi.Extensions.DecoderGrid
import Mathlib.Probability.Distributions.Gaussian.Basic

namespace Harsanyi.Frequency
open Finset MeasureTheory ProbabilityTheory
open scoped BigOperators
variable {Ω ι : Type*} [MeasurableSpace Ω] [Fintype ι] [DecidableEq ι]
variable (μ : Measure Ω) [IsProbabilityMeasure μ]

noncomputable def weightedResponse (a : ι → ℂ) (X : ι → Ω → ℝ) (ω : Ω) : ℂ :=
  ∑ i, a i * (X i ω : ℂ)

theorem weighted_response_memLp (a : ι → ℂ) (X : ι → Ω → ℝ)
    (hp : ∀ i, MemLp (X i) 2 μ) : MemLp (weightedResponse a X) 2 μ := by
  have hh : weightedResponse a X = ∑ i, fun ω => a i * (X i ω : ℂ) := by
    funext ω
    simp [weightedResponse]
  rw [hh]
  exact memLp_finset_sum' _ (fun i _ => by simpa only [smul_eq_mul] using (hp i).ofReal.const_smul (a i))

theorem weighted_response_mean (a : ι → ℂ) (X : ι → Ω → ℝ)
    (hp : ∀ i, MemLp (X i) 2 μ) :
    (∫ ω, weightedResponse a X ω ∂μ) = ∑ i, a i*(∫ ω, X i ω ∂μ : ℝ) := by
  unfold weightedResponse
  rw [integral_finset_sum]
  · simp_rw [integral_const_mul,integral_complex_ofReal]
  · intro i _
    exact ((hp i).integrable (by norm_num)).ofReal.const_mul _

theorem weighted_response_centered_square (a : ι → ℂ) (X : ι → Ω → ℝ)
    (q : ι → ℝ) (hp : ∀ i, MemLp (X i) 2 μ)
    (he : ∀ i, ∫ ω, X i ω ∂μ = 0) (hv : ∀ i, variance (X i) μ = q i)
    (hi : iIndepFun X μ) :
    (∫ ω, weightedResponse a X ω ^ 2 ∂μ) = ∑ i, a i^2*(q i : ℂ) := by
  have hc (i j : ι) : (∫ ω, X i ω*X j ω ∂μ) = if i=j then q i else 0 := by
    by_cases hij : i=j
    · subst j
      have h := variance_eq_sub (hp i)
      rw [he i,hv i] at h
      simpa only [pow_two,zero_mul,sub_zero,if_pos rfl] using h.symm
    · rw [if_neg hij,(hi.indepFun hij).integral_fun_mul_eq_mul_integral
        (hp i).aestronglyMeasurable (hp j).aestronglyMeasurable,he i,he j,mul_zero]
  have hprod (i j : ι) : Integrable (fun ω => a i*a j*((X i ω*X j ω : ℝ) : ℂ)) μ := by
    have h : Integrable (fun ω => X i ω*X j ω) μ := (hp i).integrable_mul (hp j)
    exact h.ofReal.const_mul _
  have hs (ω : Ω) : weightedResponse a X ω^2 =
      ∑ i, ∑ j, a i*a j*((X i ω*X j ω : ℝ) : ℂ) := by
    simp only [weightedResponse,pow_two,sum_mul,mul_sum,Complex.ofReal_mul]
    apply sum_congr rfl
    intro i _
    apply sum_congr rfl
    intro j _
    ring
  simp_rw [hs]
  rw [integral_finset_sum _ (fun i _ => integrable_finset_sum _ (fun j _ => hprod i j))]
  simp_rw [integral_finset_sum _ (fun j _ => hprod _ j),integral_const_mul,
    integral_complex_ofReal,hc]
  have hi' (i j : ι) : ((if i=j then q i else 0 : ℝ) : ℂ) =
      if i=j then (q i : ℂ) else 0 := by split_ifs <;> rfl
  simp_rw [hi']
  simp [mul_ite,pow_two]

theorem real_weighted_square (w : ι → ℝ) (X : ι → Ω → ℝ) (m q : ι → ℝ)
    (hp : ∀ i, MemLp (X i) 2 μ) (hm : ∀ i, ∫ ω, X i ω ∂μ = m i)
    (hq : ∀ i, variance (X i) μ = q i) (hi : iIndepFun X μ) :
    (∫ ω, (∑ i, w i*X i ω)^2 ∂μ) = (∑ i, w i*m i)^2 + ∑ i, w i^2*q i := by
  have h := ConceptGaussian.feature_expected_loss μ X m q hp hm hq hi 0 w
  simpa only [zero_sub,neg_sq,NoisyRegression.featureLoss,mul_comm] using h

theorem weighted_response_second_moment (a : ι → ℂ) (X : ι → Ω → ℝ)
    (m q : ι → ℝ) (hp : ∀ i, MemLp (X i) 2 μ)
    (hm : ∀ i, ∫ ω, X i ω ∂μ = m i) (hq : ∀ i, variance (X i) μ = q i)
    (hi : iIndepFun X μ) :
    (∫ ω, Complex.normSq (weightedResponse a X ω) ∂μ) =
      Complex.normSq (∑ i, a i*(m i : ℂ)) + ∑ i, Complex.normSq (a i)*q i := by
  let R : Ω → ℝ := fun ω => ∑ i, (a i).re*X i ω
  let I : Ω → ℝ := fun ω => ∑ i, (a i).im*X i ω
  have hpR : MemLp R 2 μ := by
    have h : R = ∑ i, fun ω => (a i).re*X i ω := by funext ω; simp [R]
    rw [h]; exact memLp_finset_sum' _ (fun i _ => by simpa only [smul_eq_mul] using (hp i).const_smul (a i).re)
  have hpI : MemLp I 2 μ := by
    have h : I = ∑ i, fun ω => (a i).im*X i ω := by funext ω; simp [I]
    rw [h]; exact memLp_finset_sum' _ (fun i _ => by simpa only [smul_eq_mul] using (hp i).const_smul (a i).im)
  have hr := real_weighted_square μ (fun i => (a i).re) X m q hp hm hq hi
  have hi' := real_weighted_square μ (fun i => (a i).im) X m q hp hm hq hi
  have hn (ω : Ω) : Complex.normSq (weightedResponse a X ω) = R ω^2+I ω^2 := by
    simp [weightedResponse,Complex.normSq_apply,Complex.mul_re,Complex.mul_im,R,I,pow_two]
  simp_rw [hn]
  rw [integral_add hpR.integrable_sq hpI.integrable_sq,hr,hi']
  simp only [Complex.normSq_apply,Complex.re_sum,Complex.im_sum,Complex.mul_re,
    Complex.mul_im,Complex.ofReal_re,Complex.ofReal_im,mul_zero,zero_mul,sub_zero,add_zero,zero_add]
  have hs : (∑ i, (a i).re^2*q i) + (∑ i, (a i).im^2*q i) =
      ∑ i, ((a i).re*(a i).re+(a i).im*(a i).im)*q i := by
    rw [← sum_add_distrib]
    apply sum_congr rfl
    intro i _
    ring
  nlinarith only [hs]

theorem gaussian_weighted_second_moment (a : ι → ℂ) (X : ι → Ω → ℝ)
    (m : ι → ℝ) (q : ι → NNReal) (hX : ∀ i, Measurable (X i))
    (hl : ∀ i, μ.map (X i) = gaussianReal (m i) (q i)) (hi : iIndepFun X μ) :
    (∫ ω, Complex.normSq (weightedResponse a X ω) ∂μ) =
      Complex.normSq (∑ i, a i*(m i : ℂ)) + ∑ i, Complex.normSq (a i)*(q i : ℝ) := by
  have h := fun i => ConceptGaussian.gaussian_feature_moments μ (X i) (m i) (q i) (hX i) (hl i)
  exact weighted_response_second_moment μ a X m (fun i => (q i : ℝ))
    (fun i => (h i).1) (fun i => (h i).2.1) (fun i => (h i).2.2) hi

theorem gaussian_weighted_pseudocovariance (a : ι → ℂ) (X : ι → Ω → ℝ)
    (m : ι → ℝ) (q : ι → NNReal) (hX : ∀ i, Measurable (X i))
    (hl : ∀ i, μ.map (X i) = gaussianReal (m i) (q i)) (hi : iIndepFun X μ) :
    (∫ ω, (weightedResponse a X ω - ∫ z, weightedResponse a X z ∂μ)^2 ∂μ) =
      ∑ i, a i^2*(q i : ℂ) := by
  have h := fun i => ConceptGaussian.gaussian_feature_moments μ (X i) (m i) (q i) (hX i) (hl i)
  let ε : ι → Ω → ℝ := fun i ω => X i ω-m i
  have hp : ∀ i, MemLp (ε i) 2 μ := fun i => (h i).1.sub (memLp_const (m i))
  have he : ∀ i, ∫ ω, ε i ω ∂μ=0 := by
    intro i
    dsimp [ε]
    rw [integral_sub ((h i).1.integrable (by norm_num)) (integrable_const _),(h i).2.1]
    simp
  have hv : ∀ i, variance (ε i) μ=(q i : ℝ) := by
    intro i
    dsimp [ε]
    rw [variance_sub_const (h i).1.aestronglyMeasurable,(h i).2.2]
  have hiε : iIndepFun ε μ :=
    hi.comp (fun i z => z-m i) (fun _ => measurable_id.sub measurable_const)
  have hs (ω : Ω) : weightedResponse a X ω - ∫ z, weightedResponse a X z ∂μ =
      weightedResponse a ε ω := by
    rw [weighted_response_mean μ a X (fun i => (h i).1)]
    simp_rw [(h _).2.1]
    simp [weightedResponse,ε,Complex.ofReal_sub,mul_sub,sum_sub_distrib]
  simp_rw [hs]
  exact weighted_response_centered_square μ a ε (fun i => (q i : ℝ)) hp he hv hiε

/-- The real Gaussian embedded into ℂ has actual nonzero pseudocovariance. -/
theorem real_gaussian_pseudocovariance (m : ℝ) (q : NNReal) :
    (∫ z : ℝ, ((z-m : ℝ) : ℂ)^2 ∂gaussianReal m q) = (q : ℂ) := by
  have h : (∫ z : ℝ, (z-m)^2 ∂gaussianReal m q) = (q : ℝ) := by
    have hv := variance_eq_integral (μ:=gaussianReal m q) (X:=fun z : ℝ => z) measurable_id.aemeasurable
    simpa only [variance_fun_id_gaussianReal,integral_id_gaussianReal] using hv.symm
  have hc : (fun z : ℝ => ((z-m : ℝ) : ℂ)^2) =
      (fun z : ℝ => (((z-m)^2 : ℝ) : ℂ)) := by
    funext z
    norm_cast
  rw [hc,integral_complex_ofReal,h]

/-- Independent real Gaussian weights stay Gaussian under their actual complex
linear phase sum. This uses real-linear maps and convolution of independent laws,
and does not replace any weight by circular complex noise. -/
theorem gaussian_weighted_isGaussian (a : ι → ℂ) (X : ι → Ω → ℝ)
    (m : ι → ℝ) (q : ι → NNReal) (hX : ∀ i, Measurable (X i))
    (hl : ∀ i, μ.map (X i) = gaussianReal (m i) (q i)) (hi : iIndepFun X μ) :
    IsGaussian (μ.map (weightedResponse a X)) := by
  let Y : ι → Ω → ℂ := fun i ω => a i*(X i ω : ℂ)
  have hY : ∀ i, Measurable (Y i) := by intro i; dsimp [Y]; fun_prop
  have hlY : ∀ i, IsGaussian (μ.map (Y i)) := by
    intro i
    let L : ℝ →L[ℝ] ℂ := (ContinuousLinearMap.mul ℝ ℂ (a i)).comp Complex.ofRealCLM
    have hh : μ.map (Y i) = (gaussianReal (m i) (q i)).map L := by
      rw [← hl i,Measure.map_map L.measurable (hX i)]
      rfl
    rw [hh]
    infer_instance
  have hiY : iIndepFun Y μ := by
    exact hi.comp (fun i z => a i*(z : ℂ)) (fun i => by fun_prop)
  have hs : ∀ s : Finset ι, IsGaussian (μ.map (fun ω => ∑ i ∈ s, Y i ω)) := by
    intro s
    induction s using Finset.induction_on with
    | empty => simp only [sum_empty,Measure.map_const,measure_univ,one_smul]; infer_instance
    | @insert i s his ih =>
      letI : IsGaussian (μ.map (fun ω => ∑ j ∈ s, Y j ω)) := ih
      letI : IsGaussian (μ.map (Y i)) := hlY i
      have hh := hiY.indepFun_finset_sum_of_notMem hY his
      have heq : (∑ j ∈ s,Y j) = (fun ω => ∑ j ∈ s,Y j ω) := by funext ω; simp
      have hh' : IndepFun (fun ω => ∑ j ∈ s,Y j ω) (Y i) μ := by
        rw [heq] at hh
        exact hh
      have hm : Measurable (fun ω => ∑ j ∈ s, Y j ω) := by fun_prop
      have hc := hh'.map_add_eq_map_conv_map₀' hm.aemeasurable (hY i).aemeasurable
        (inferInstance) (inferInstance)
      simp only [Finset.sum_apply] at hc
      simp only [sum_insert his]
      have he : (fun ω => Y i ω+∑ j ∈ s,Y j ω) =
          (fun ω => ∑ j ∈ s,Y j ω+Y i ω) := by funext ω; exact add_comm _ _
      rw [he]
      change IsGaussian (μ.map ((fun ω => ∑ j ∈ s,Y j ω) + Y i))
      rw [hc]
      infer_instance
  simpa only [weightedResponse,Y] using hs Finset.univ

end Harsanyi.Frequency
