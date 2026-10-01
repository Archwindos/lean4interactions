import Harsanyi.Extensions.TransformationCounterexamples
import Mathlib.Probability.Distributions.Gaussian.Real
import Mathlib.Probability.Distributions.Uniform
import Mathlib.Probability.Independence.Basic
import Mathlib.Probability.Kernel.Composition.MeasureCompProd

/-! An actual source-model instance for Eq.(24): a constant ReLU layer, balanced
labels and independent Gaussian perturbation. The pushed joint measure is
connected to a genuine constant label kernel, not only an entropy-zero scalar. -/
namespace Harsanyi.Entropy
open MeasureTheory ProbabilityTheory

noncomputable def balancedLabelMeasure : Measure Bool :=
  (PMF.uniformOfFintype Bool).toMeasure

instance : IsProbabilityMeasure balancedLabelMeasure := by
  unfold balancedLabelMeasure
  infer_instance

theorem balanced_label_mass (y : Bool) : balancedLabelMeasure {y} = ENNReal.ofReal (bitLaw.mass y) := by
  rw [balancedLabelMeasure, PMF.toMeasure_apply_singleton _ _ (measurableSet_singleton y)]
  norm_num [PMF.uniformOfFintype_apply, bitLaw, ENNReal.ofReal_div_of_pos]

noncomputable def gaussianFeatureSpace (q : NNReal) : Measure (Bool × ℝ) :=
  balancedLabelMeasure.prod (gaussianReal 0 q)

instance (q : NNReal) : IsProbabilityMeasure (gaussianFeatureSpace q) := by
  unfold gaussianFeatureSpace
  infer_instance

noncomputable def constantReluFeature (y : Bool) : ℝ := max 0 (0*signedInput y+1)

noncomputable def noisyConstantRelu (p : Bool × ℝ) : ℝ := constantReluFeature p.1+p.2

theorem constant_relu_feature (y : Bool) : constantReluFeature y = 1 := by
  norm_num [constantReluFeature]

theorem noisy_constant_relu_eq (p : Bool × ℝ) : noisyConstantRelu p = 1+p.2 := by
  simp [noisyConstantRelu, constant_relu_feature]

theorem gaussian_feature_noise_law (q : NNReal) :
    (gaussianFeatureSpace q).map Prod.snd = gaussianReal 0 q := by
  rw [gaussianFeatureSpace, Measure.map_snd_prod, measure_univ, one_smul]

theorem gaussian_feature_label_law (q : NNReal) :
    (gaussianFeatureSpace q).map Prod.fst = balancedLabelMeasure := by
  simp [gaussianFeatureSpace, Measure.map_fst_prod]

theorem noisy_constant_relu_law (q : NNReal) :
    (gaussianFeatureSpace q).map noisyConstantRelu = gaussianReal 1 q := by
  have he : noisyConstantRelu = (fun z : ℝ => 1+z) ∘ Prod.snd := by
    funext p
    exact noisy_constant_relu_eq p
  rw [he, ← Measure.map_map (by fun_prop) measurable_snd, gaussian_feature_noise_law,
    gaussianReal_map_const_add]
  norm_num

theorem gaussian_feature_independent (q : NNReal) :
    IndepFun (Prod.fst : Bool × ℝ → Bool) noisyConstantRelu (gaussianFeatureSpace q) := by
  have h : IndepFun (fun p : Bool × ℝ => p.1) (fun p => (1:ℝ)+p.2)
      (balancedLabelMeasure.prod (gaussianReal 0 q)) :=
    indepFun_prod measurable_id (by fun_prop)
  have he : noisyConstantRelu = fun p : Bool × ℝ => 1+p.2 :=
    funext noisy_constant_relu_eq
  rw [he]
  exact h

noncomputable def gaussianLabelKernel : Kernel ℝ Bool := Kernel.const ℝ balancedLabelMeasure

theorem gaussian_feature_joint_kernel (q : NNReal) :
    (gaussianFeatureSpace q).map (fun p => (noisyConstantRelu p,p.1)) =
      (gaussianReal 1 q) ⊗ₘ gaussianLabelKernel := by
  have hm : Measurable noisyConstantRelu := by
    have he : noisyConstantRelu = fun p : Bool × ℝ => 1+p.2 :=
      funext noisy_constant_relu_eq
    rw [he]
    fun_prop
  rw [gaussianLabelKernel, Measure.compProd_const]
  change _ = (gaussianReal 1 q).prod balancedLabelMeasure
  rw [(indepFun_iff_map_prod_eq_prod_map_map hm.aemeasurable measurable_fst.aemeasurable).mp
    (gaussian_feature_independent q).symm, noisy_constant_relu_law, gaussian_feature_label_law]

theorem gaussian_label_kernel_mass (z : ℝ) (y : Bool) :
    gaussianLabelKernel z {y} = ENNReal.ofReal (bitLaw.mass y) := by
  simpa [gaussianLabelKernel] using balanced_label_mass y

/-- Finite-label conditional entropy computes actual MI for the constructed
joint law: the genuine kernel is the same balanced label law at every feature. -/
theorem actual_gaussian_feature_information_zero (q : NNReal) :
    entropy bitLaw.mass -
      (∫ z : ℝ, entropy (fun y => (gaussianLabelKernel z {y}).toReal) ∂gaussianReal 1 q) = 0 := by
  simp_rw [gaussian_label_kernel_mass, ENNReal.toReal_ofReal (bitLaw.nonneg _)]
  simp

noncomputable def constantFeatureKernel (q : NNReal) (y z : Bool) : ℝ :=
  Real.exp (-(constantReluFeature y-constantReluFeature z)^2/(2*(q:ℝ)))

theorem actual_constant_feature_kernel (q : NNReal) (y z : Bool) :
    constantFeatureKernel q y z = 1 := by
  simp [constantFeatureKernel, constant_relu_feature]

/-- Two examples, one in each class. Both literal source factors are 1/P=1/2. -/
noncomputable def actualConstantFeatureEstimator (q : NNReal) : ℝ :=
  -(1/2:ℝ) * ∑ y : Bool, Real.log ((1/2:ℝ)*∑ z : Bool, constantFeatureKernel q y z) -
    ∑ y : Bool, (1/2:ℝ) * (-(1/2:ℝ)*Real.log ((1/2:ℝ)*constantFeatureKernel q y y))

theorem actual_constant_feature_estimator_negative (q : NNReal) :
    actualConstantFeatureEstimator q < 0 := by
  have h := printed_constant_feature_estimator_negative
  simp only [actualConstantFeatureEstimator, actual_constant_feature_kernel, Fintype.sum_bool]
  nlinarith

/-- The literal source Eq.(24) counterexample binds its actual joint measure
and conditional label kernel, plus the two displayed factors 1/P. -/
theorem actual_gaussian_eq24_counterexample (q : NNReal) (hq : 0 < q) :
    (∀ y, constantReluFeature y = 1) ∧
    (gaussianFeatureSpace q).map noisyConstantRelu = gaussianReal 1 q ∧
    (gaussianFeatureSpace q).map (fun p => (noisyConstantRelu p,p.1)) =
      (gaussianReal 1 q) ⊗ₘ gaussianLabelKernel ∧
    (entropy bitLaw.mass -
      (∫ z : ℝ, entropy (fun y => (gaussianLabelKernel z {y}).toReal) ∂gaussianReal 1 q)) = 0 ∧
    actualConstantFeatureEstimator q < 0 := by
  exact ⟨constant_relu_feature, noisy_constant_relu_law q, gaussian_feature_joint_kernel q,
    actual_gaussian_feature_information_zero q, actual_constant_feature_estimator_negative q⟩

end Harsanyi.Entropy
