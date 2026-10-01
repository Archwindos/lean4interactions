import Harsanyi.Extensions.DecoderKernelMoments
import Mathlib.Probability.Distributions.Uniform
import Mathlib.MeasureTheory.Integral.Prod

namespace Harsanyi.Frequency.WeakIndependence
open MeasureTheory ProbabilityTheory

noncomputable def fairSignLaw : Measure Bool :=
  (1/2:ENNReal) • Measure.dirac true + (1/2:ENNReal) • Measure.dirac false

instance : IsProbabilityMeasure fairSignLaw := by
  constructor
  norm_num [fairSignLaw,Measure.add_apply,Measure.smul_apply]
  exact ENNReal.inv_two_add_inv_two

noncomputable def signGaussianSpace : Measure (Bool × ℝ) :=
  fairSignLaw.prod (gaussianReal 0 1)

instance : IsProbabilityMeasure signGaussianSpace := by
  unfold signGaussianSpace
  infer_instance

def signValue (b : Bool) : ℝ := if b then 1 else -1
def W1 (p : Bool × ℝ) : ℝ := p.2
def W2 (p : Bool × ℝ) : ℝ := signValue p.1 * p.2

theorem measurable_w1 : Measurable W1 := measurable_snd
theorem measurable_w2 : Measurable W2 :=
  ((measurable_of_finite signValue).comp measurable_fst).mul measurable_snd

theorem actual_sign_gaussian_independence :
    IndepFun (fun p : Bool × ℝ => signValue p.1) W1 signGaussianSpace :=
  indepFun_prod (measurable_of_finite signValue) measurable_id

theorem joint_map_split {E : Type*} [MeasurableSpace E]
    (f : Bool × ℝ → E) (hf : Measurable f) :
    signGaussianSpace.map f =
      (1/2:ENNReal) • (gaussianReal 0 1).map (fun x => f (true,x)) +
      (1/2:ENNReal) • (gaussianReal 0 1).map (fun x => f (false,x)) := by
  rw [signGaussianSpace,fairSignLaw,Measure.add_prod,Measure.prod_smul_left,
    Measure.prod_smul_left,Measure.dirac_prod,Measure.dirac_prod,Measure.map_add _ _ hf,
    Measure.map_smul,Measure.map_smul,Measure.map_map hf measurable_prodMk_left,
    Measure.map_map hf measurable_prodMk_left]
  rfl

theorem actual_w1_law : signGaussianSpace.map W1 = gaussianReal 0 1 := by
  rw [signGaussianSpace]
  change (fairSignLaw.prod (gaussianReal 0 1)).map Prod.snd = _
  rw [Measure.map_snd_prod,measure_univ,one_smul]

theorem actual_w2_law : signGaussianSpace.map W2 = gaussianReal 0 1 := by
  rw [joint_map_split W2 measurable_w2]
  have ht : (fun x : ℝ => W2 (true,x)) = id := by funext x; simp [W2,signValue]
  have hf : (fun x : ℝ => W2 (false,x)) = fun x => -x := by funext x; simp [W2,signValue]
  rw [ht,hf,Measure.map_id,gaussianReal_map_neg]
  simp only [neg_zero,← add_smul]
  norm_num
  rw [ENNReal.inv_two_add_inv_two,one_smul]

theorem standard_gaussian_fourth_moment :
    (∫ x : ℝ, x^4 ∂gaussianReal 0 1) = 3 := by
  have hm : iteratedDeriv 4 (mgf (fun x : ℝ => x) (gaussianReal 0 1)) 0 =
      ∫ x : ℝ, x^4 ∂gaussianReal 0 1 := by
    simpa using iteratedDeriv_mgf_zero (X:=fun x : ℝ => x) (μ:=gaussianReal 0 1) (by simp) 4
  rw [← hm,mgf_fun_id_gaussianReal]
  simp only [NNReal.coe_one,zero_mul,zero_add,one_mul]
  have h1 : deriv (fun t : ℝ => Real.exp (t^2/2)) =
      fun t => t*Real.exp (t^2/2) := by
    funext t
    rw [_root_.deriv_exp (by fun_prop)]
    simp
    ring
  have h2 : deriv (fun t : ℝ => t*Real.exp (t^2/2)) =
      fun t => (1+t^2)*Real.exp (t^2/2) := by
    funext t
    rw [deriv_fun_mul (by fun_prop) (by fun_prop),h1]
    simp
    ring
  have h3 : deriv (fun t : ℝ => (1+t^2)*Real.exp (t^2/2)) =
      fun t => (3*t+t^3)*Real.exp (t^2/2) := by
    funext t
    rw [deriv_fun_mul (by fun_prop) (by fun_prop),h1]
    simp
    ring
  rw [iteratedDeriv_succ,iteratedDeriv_succ,iteratedDeriv_succ,iteratedDeriv_one,h1,h2,h3]
  rw [deriv_fun_mul (by fun_prop) (by fun_prop),h1]
  simp
  have hpoly : HasDerivAt (fun t : ℝ => 3*t+t^3) 3 0 := by
    convert ((hasDerivAt_id (0:ℝ)).const_mul 3).add ((hasDerivAt_id (0:ℝ)).pow 3) using 1 <;> norm_num
  exact hpoly.deriv

theorem actual_sign_mean_zero : (∫ b : Bool, signValue b ∂fairSignLaw) = 0 := by
  rw [integral_fintype _ Integrable.of_finite]
  norm_num [fairSignLaw,signValue,measureReal_def,Measure.add_apply,Measure.smul_apply,Fintype.sum_bool]

theorem actual_w1_mean_zero : (∫ p, W1 p ∂signGaussianSpace) = 0 :=
  (ConceptGaussian.gaussian_feature_moments signGaussianSpace W1 0 1
    measurable_w1 actual_w1_law).2.1

theorem actual_w2_mean_zero : (∫ p, W2 p ∂signGaussianSpace) = 0 :=
  (ConceptGaussian.gaussian_feature_moments signGaussianSpace W2 0 1
    measurable_w2 actual_w2_law).2.1

theorem actual_first_product_zero : (∫ p, W1 p*W2 p ∂signGaussianSpace) = 0 := by
  have he : (fun p => W1 p*W2 p) = fun p : Bool × ℝ => signValue p.1*p.2^2 := by
    funext p
    simp only [W1,W2]
    ring
  rw [he,signGaussianSpace,integral_prod_mul signValue (fun x : ℝ => x^2),actual_sign_mean_zero,zero_mul]

theorem actual_first_product_factorization :
    (∫ p, W1 p*W2 p ∂signGaussianSpace) =
      (∫ p, W1 p ∂signGaussianSpace)*(∫ p, W2 p ∂signGaussianSpace) := by
  rw [actual_first_product_zero,actual_w1_mean_zero,actual_w2_mean_zero,mul_zero]

theorem actual_product_second_moment :
    (∫ p, |W1 p*W2 p|^2 ∂signGaussianSpace) = 3 := by
  have he (p : Bool × ℝ) : |W1 p*W2 p|^2 = W1 p^4 := by
    rw [sq_abs]
    cases hb : p.1 <;> simp [W1,W2,signValue,hb] <;> ring
  simp_rw [he]
  calc
    _ = ∫ x : ℝ, x^4 ∂signGaussianSpace.map W1 := by
      symm
      simpa only [id_eq] using integral_map_of_stronglyMeasurable measurable_w1
        (measurable_id.pow_const 4).stronglyMeasurable
    _ = 3 := by rw [actual_w1_law]; exact standard_gaussian_fourth_moment

theorem actual_each_second_moment :
    (∫ p, |W1 p|^2 ∂signGaussianSpace) = 1 ∧
    (∫ p, |W2 p|^2 ∂signGaussianSpace) = 1 := by
  have hm1 := ConceptGaussian.gaussian_feature_moments signGaussianSpace W1 0 1
    measurable_w1 actual_w1_law
  have hm2 := ConceptGaussian.gaussian_feature_moments signGaussianSpace W2 0 1
    measurable_w2 actual_w2_law
  constructor
  · have h := variance_eq_sub hm1.1
    rw [hm1.2.1,hm1.2.2] at h
    simpa [sq_abs,Pi.pow_apply] using h.symm
  · have h := variance_eq_sub hm2.1
    rw [hm2.2.1,hm2.2.2] at h
    simpa [sq_abs,Pi.pow_apply] using h.symm

theorem actual_weak_first_moment_counterexample :
    signGaussianSpace.map W1 = gaussianReal 0 1 ∧
    signGaussianSpace.map W2 = gaussianReal 0 1 ∧
    (∫ p, W1 p*W2 p ∂signGaussianSpace) =
      (∫ p, W1 p ∂signGaussianSpace)*(∫ p, W2 p ∂signGaussianSpace) ∧
    (∫ p, |W1 p*W2 p|^2 ∂signGaussianSpace) ≠
      (∫ p, |W1 p|^2 ∂signGaussianSpace)*(∫ p, |W2 p|^2 ∂signGaussianSpace) := by
  refine ⟨actual_w1_law,actual_w2_law,actual_first_product_factorization,?_⟩
  rw [actual_product_second_moment,actual_each_second_moment.1,actual_each_second_moment.2]
  norm_num

theorem actual_not_independent : ¬IndepFun W1 W2 signGaussianSpace := by
  intro hi
  have hi2 := hi.comp (measurable_id.pow_const 2) (measurable_id.pow_const 2)
  have h := hi2.integral_fun_mul_eq_mul_integral
    (measurable_w1.pow_const 2).aestronglyMeasurable
    (measurable_w2.pow_const 2).aestronglyMeasurable
  have he : (fun p => |W1 p*W2 p|^2) = fun p => W1 p^2*W2 p^2 := by
    funext p
    rw [sq_abs,mul_pow]
  have h1 : (∫ p, W1 p^2 ∂signGaussianSpace) = 1 := by
    simpa only [sq_abs] using actual_each_second_moment.1
  have h2 : (∫ p, W2 p^2 ∂signGaussianSpace) = 1 := by
    simpa only [sq_abs] using actual_each_second_moment.2
  have h3 := actual_product_second_moment
  rw [he] at h3
  change (∫ p, W1 p^2*W2 p^2 ∂signGaussianSpace) =
    (∫ p, W1 p^2 ∂signGaussianSpace)*(∫ p, W2 p^2 ∂signGaussianSpace) at h
  rw [h1,h2,one_mul,h3] at h
  norm_num at h

theorem actual_unit_kernel_response {M N : ℕ} [NeZero M] [NeZero N]
    (W : Bool × ℝ → ℝ) (u : ZMod M) (v : ZMod N) (p : Bool × ℝ) :
    randomKernelResponse (fun _ : Fin 1 × Fin 1 => W) u v p = (W p : ℂ) := by
  simp [randomKernelResponse,offsetResponse,Fintype.sum_prod_type,
    Fin.sum_univ_one,squareShift,grid_character_apply]

theorem actual_unit_kernel_product_som {M N : ℕ} [NeZero M] [NeZero N]
    (u : ZMod M) (v : ZMod N) :
    (∫ p, Complex.normSq
      (randomKernelResponse (fun _ : Fin 1 × Fin 1 => W1) u v p *
        randomKernelResponse (fun _ : Fin 1 × Fin 1 => W2) u v p) ∂signGaussianSpace) = 3 := by
  simp_rw [actual_unit_kernel_response,← Complex.ofReal_mul,Complex.normSq_ofReal]
  have h := actual_product_second_moment
  simp only [sq_abs] at h
  simpa only [pow_two] using h

theorem actual_unit_kernel_each_som {M N : ℕ} [NeZero M] [NeZero N]
    (u : ZMod M) (v : ZMod N) :
    (∫ p, Complex.normSq (randomKernelResponse (fun _ : Fin 1 × Fin 1 => W1) u v p)
      ∂signGaussianSpace) = 1 ∧
    (∫ p, Complex.normSq (randomKernelResponse (fun _ : Fin 1 × Fin 1 => W2) u v p)
      ∂signGaussianSpace) = 1 := by
  simp_rw [actual_unit_kernel_response,Complex.normSq_ofReal]
  have h := actual_each_second_moment
  simp only [sq_abs] at h
  simpa only [pow_two] using h

theorem actual_unit_kernel_first_factorization {M N : ℕ} [NeZero M] [NeZero N]
    (u : ZMod M) (v : ZMod N) :
    (∫ p, randomKernelResponse (fun _ : Fin 1 × Fin 1 => W1) u v p *
      randomKernelResponse (fun _ : Fin 1 × Fin 1 => W2) u v p ∂signGaussianSpace) =
    (∫ p, randomKernelResponse (fun _ : Fin 1 × Fin 1 => W1) u v p ∂signGaussianSpace) *
      (∫ p, randomKernelResponse (fun _ : Fin 1 × Fin 1 => W2) u v p ∂signGaussianSpace) := by
  simp_rw [actual_unit_kernel_response,← Complex.ofReal_mul,integral_complex_ofReal]
  rw [actual_first_product_factorization,Complex.ofReal_mul]

theorem actual_unit_kernel_weak_counterexample {M N : ℕ} [NeZero M] [NeZero N]
    (u : ZMod M) (v : ZMod N) :
    (∫ p, Complex.normSq
      (randomKernelResponse (fun _ : Fin 1 × Fin 1 => W1) u v p *
        randomKernelResponse (fun _ : Fin 1 × Fin 1 => W2) u v p) ∂signGaussianSpace) ≠
    (∫ p, Complex.normSq (randomKernelResponse (fun _ : Fin 1 × Fin 1 => W1) u v p)
      ∂signGaussianSpace) *
    (∫ p, Complex.normSq (randomKernelResponse (fun _ : Fin 1 × Fin 1 => W2) u v p)
      ∂signGaussianSpace) := by
  rw [actual_unit_kernel_product_som,actual_unit_kernel_each_som u v |>.1,
    actual_unit_kernel_each_som u v |>.2]
  norm_num

end Harsanyi.Frequency.WeakIndependence
