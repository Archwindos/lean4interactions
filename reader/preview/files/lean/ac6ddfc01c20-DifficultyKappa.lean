import Harsanyi.Extensions.ConceptGaussian
namespace Harsanyi.DifficultyKappa
open MeasureTheory ProbabilityTheory
noncomputable def unitLaw : Measure ℝ := gaussianReal 0 1
instance : IsProbabilityMeasure unitLaw := by unfold unitLaw; infer_instance
noncomputable def absoluteFirstMoment : ℝ := ∫ z : ℝ, |z| ∂unitLaw
lemma unit_memLp : MemLp (id : ℝ → ℝ) 2 unitLaw := memLp_id_gaussianReal' 2 (by norm_num)
lemma unit_integrable : Integrable (id : ℝ → ℝ) unitLaw := unit_memLp.integrable (by norm_num)
lemma absoluteFirstMoment_pos : 0 < absoluteFirstMoment := by
  have hn : 0 ≤ absoluteFirstMoment := integral_nonneg (fun _ => abs_nonneg _)
  have hz : absoluteFirstMoment ≠ 0 := by
    intro h
    have he : (fun z : ℝ => |z|) =ᵐ[unitLaw] 0 :=
      (integral_eq_zero_iff_of_nonneg (fun _ => abs_nonneg _) unit_integrable.abs).mp h
    have h0 : (id : ℝ → ℝ) =ᵐ[unitLaw] (fun _ => 0) := by
      filter_upwards [he] with z hz
      simpa only [Pi.zero_apply, abs_eq_zero, id_eq] using hz
    have hv := variance_congr h0
    have hzv : variance (fun _ : ℝ => (0:ℝ)) unitLaw = 0 := variance_zero unitLaw
    rw [hzv] at hv
    norm_num [unitLaw, variance_id_gaussianReal] at hv
  exact lt_of_le_of_ne hn (Ne.symm hz)
noncomputable def chosenScale : ℝ := absoluteFirstMoment / (8 * (1 + absoluteFirstMoment))
lemma chosenScale_pos : 0 < chosenScale := by
  have hm := absoluteFirstMoment_pos
  unfold chosenScale
  exact div_pos absoluteFirstMoment_pos (by positivity)
lemma chosenScale_small : chosenScale < 1/8 := by
  have hm := absoluteFirstMoment_pos
  unfold chosenScale
  apply (div_lt_div_iff₀ (by positivity) (by norm_num)).2
  nlinarith
lemma chosenScale_bound : chosenScale < absoluteFirstMoment / 8 := by
  have hm := absoluteFirstMoment_pos
  unfold chosenScale
  apply (div_lt_div_iff₀ (by positivity) (by norm_num)).2
  nlinarith [absoluteFirstMoment_pos]
noncomputable def perturbation (σ z : ℝ) : ℝ := σ * z
noncomputable def perturbationVariance (σ : ℝ) : NNReal := ⟨σ^2, sq_nonneg _⟩
lemma perturbation_law (σ : ℝ) :
    unitLaw.map (perturbation σ) = gaussianReal 0 (perturbationVariance σ) := by
  simpa [unitLaw, perturbation, perturbationVariance] using
    (gaussianReal_map_const_mul (μ := (0:ℝ)) (v := (1:NNReal)) σ)
lemma perturbation_integrable (σ : ℝ) : Integrable (perturbation σ) unitLaw :=
  unit_integrable.const_mul σ
lemma perturbation_square_integrable (σ : ℝ) :
    Integrable (fun z => perturbation σ z ^ 2) unitLaw :=
  (unit_memLp.const_mul σ).integrable_sq
lemma perturbation_moments (σ : ℝ) (hσ : 0 ≤ σ) :
    (∫ z, |perturbation σ z| ∂unitLaw) = σ * absoluteFirstMoment ∧
      (∫ z, perturbation σ z ^ 2 ∂unitLaw) = σ ^ 2 := by
  constructor
  · simp_rw [perturbation, abs_mul, abs_of_nonneg hσ]
    rw [integral_const_mul]
    rfl
  · have hv := variance_eq_sub (unit_memLp.const_mul σ)
    have hi : (∫ z, perturbation σ z ∂unitLaw) = 0 := by
      change (∫ z, σ * (id z) ∂unitLaw) = 0
      rw [integral_const_mul]
      simp [unitLaw, integral_id_gaussianReal]
    have hv' : variance (perturbation σ) unitLaw = σ^2 := by
      unfold perturbation
      change variance (fun z => σ * id z) unitLaw = σ^2
      rw [variance_mul]
      simp [unitLaw, variance_id_gaussianReal]
    change variance (perturbation σ) unitLaw =
      (∫ z, perturbation σ z ^ 2 ∂unitLaw) - (∫ z, perturbation σ z ∂unitLaw)^2 at hv
    rw [hi, hv'] at hv
    linarith
/-- Actual single-ReLU score with nonzero output baseline. -/
noncomputable def score (t : ℝ) : ℝ := max 0 (t + 1/2)
noncomputable def dividend (x e : ℝ) : ℝ := score (x+e) - score 0
noncomputable def referenceCoefficient (x : ℝ) : ℝ := dividend x 0
noncomputable def normalizedCoefficient (x e : ℝ) : ℝ := dividend x e / referenceCoefficient x
noncomputable def singletonGame (x e : ℝ) : Game (Fin 1) :=
  fun T => score (if (0 : Fin 1) ∈ T then x+e else 0)
lemma singleton_dividend (x e : ℝ) :
    interaction (singletonGame x e) {0} = dividend x e := by
  simp [interaction_singleton, singletonGame, dividend]
lemma actual_references : score 0 = 1/2 ∧ referenceCoefficient (-1) = -1/2 ∧
    referenceCoefficient 1 = 1 ∧ normalizedCoefficient (-1) 0 = 1 ∧
      normalizedCoefficient 1 0 = 1 := by
  norm_num [score, dividend, referenceCoefficient, normalizedCoefficient]
lemma low_variation (e : ℝ) :
    |dividend (-1) e - referenceCoefficient (-1)| = max 0 (e-1/2) := by
  rw [actual_references.2.1]
  have hm : max 0 (e-1/2) ≥ 0 := le_max_left _ _
  simp only [dividend, score, show (-1:ℝ)+e+1/2=e-1/2 by ring]
  norm_num [abs_of_nonneg hm]
lemma high_variation (e : ℝ) :
    |dividend 1 e - referenceCoefficient 1| = |e| - max 0 (-e-3/2) := by
  rw [actual_references.2.2.1]
  simp only [dividend, score, show (1:ℝ)+e+1/2=3/2+e by ring]
  norm_num
  by_cases h : 0 ≤ 3/2+e
  · rw [max_eq_right h, max_eq_left (by linarith : -e-3/2 ≤ 0)]
    congr 1
    ring
  · have he : e < 0 := by linarith
    rw [max_eq_left (le_of_not_ge h), max_eq_right (by linarith : 0 ≤ -e-3/2), abs_of_neg he]
    norm_num
lemma low_tail_bound (e : ℝ) : max 0 (e-1/2) ≤ e^2/2 := by
  by_cases h : 0 ≤ e-1/2
  · rw [max_eq_right h]; nlinarith [sq_nonneg (e-1)]
  · rw [max_eq_left (le_of_not_ge h)]; positivity
lemma high_tail_bound (e : ℝ) : max 0 (-e-3/2) ≤ e^2/6 := by
  by_cases h : 0 ≤ -e-3/2
  · rw [max_eq_right h]; nlinarith [sq_nonneg (e+3)]
  · rw [max_eq_left (le_of_not_ge h)]; positivity
noncomputable def lowExpectedVariation (σ : ℝ) : ℝ :=
  ∫ z, |dividend (-1) (perturbation σ z) - referenceCoefficient (-1)| ∂unitLaw
noncomputable def highExpectedVariation (σ : ℝ) : ℝ :=
  ∫ z, |dividend 1 (perturbation σ z) - referenceCoefficient 1| ∂unitLaw
lemma actual_variation_bounds (σ : ℝ) (hσ : 0 ≤ σ) :
    lowExpectedVariation σ ≤ σ^2/2 ∧
      σ*absoluteFirstMoment - σ^2/6 ≤ highExpectedVariation σ := by
  have hp := perturbation_integrable σ
  have hl : Integrable (fun z => max 0 (perturbation σ z - 1/2)) unitLaw :=
    (integrable_const 0).sup (hp.sub (integrable_const _))
  have ht : Integrable (fun z => max 0 (-perturbation σ z - 3/2)) unitLaw :=
    (integrable_const 0).sup (hp.neg.sub (integrable_const _))
  have hs := perturbation_square_integrable σ
  have hlow := integral_mono hl (hs.div_const 2) (fun z => low_tail_bound (perturbation σ z))
  have htail := integral_mono ht (hs.div_const 6) (fun z => high_tail_bound (perturbation σ z))
  simp_rw [integral_div, (perturbation_moments σ hσ).2] at hlow htail
  constructor
  · simpa only [lowExpectedVariation, low_variation] using hlow
  · unfold highExpectedVariation
    simp_rw [high_variation]
    rw [integral_sub hp.abs ht, (perturbation_moments σ hσ).1]
    linarith
/-- Exact equal-probability data averages for inputs -1,1 and reference0. -/
noncomputable def interactionKappa (σ : ℝ) : ℝ :=
  ((lowExpectedVariation σ + highExpectedVariation σ)/2) /
    ((|referenceCoefficient (-1)|+|referenceCoefficient 1|)/2)
noncomputable def coefficientKappa (σ : ℝ) : ℝ :=
  (((lowExpectedVariation σ / |referenceCoefficient (-1)|) +
    (highExpectedVariation σ / |referenceCoefficient 1|))/2) /
    ((|normalizedCoefficient (-1) 0|+|normalizedCoefficient 1 0|)/2)
lemma actual_kappa_difference (σ : ℝ) :
    interactionKappa σ - coefficientKappa σ =
      (highExpectedVariation σ - 2*lowExpectedVariation σ)/6 := by
  unfold coefficientKappa interactionKappa
  rw [actual_references.2.1, actual_references.2.2.1,
    actual_references.2.2.2.1, actual_references.2.2.2.2]
  norm_num
  ring
noncomputable def literalCoefficientKappa (σ : ℝ) : ℝ :=
  ((∫ z, |normalizedCoefficient (-1) (perturbation σ z) -
    normalizedCoefficient (-1) 0| ∂unitLaw) +
   (∫ z, |normalizedCoefficient 1 (perturbation σ z) -
    normalizedCoefficient 1 0| ∂unitLaw)) / 2 /
      ((|normalizedCoefficient (-1) 0| + |normalizedCoefficient 1 0|) / 2)

lemma normalized_variation (x e : ℝ) :
    |normalizedCoefficient x e - normalizedCoefficient x 0| =
      |dividend x e - referenceCoefficient x| / |referenceCoefficient x| := by
  unfold normalizedCoefficient
  rw [← sub_div, abs_div]
  rfl

lemma literal_coefficient_kappa_eq (σ : ℝ) :
    literalCoefficientKappa σ = coefficientKappa σ := by
  unfold literalCoefficientKappa coefficientKappa
  simp_rw [normalized_variation, integral_div]
  rfl

/-- Genuine untruncated Gaussian counterexample to the source cancellation across data. -/
theorem gaussian_relu_kappa_counterexample :
    unitLaw.map (perturbation chosenScale) = gaussianReal 0 (perturbationVariance chosenScale) ∧
    0 < chosenScale ∧ score 0 = 1/2 ∧ coefficientKappa chosenScale < interactionKappa chosenScale := by
  refine ⟨perturbation_law _, chosenScale_pos, actual_references.1, ?_⟩
  have hb := actual_variation_bounds chosenScale (le_of_lt chosenScale_pos)
  have hgap : (7/6:ℝ)*chosenScale^2 < chosenScale*absoluteFirstMoment := by
    have hp := chosenScale_pos
    have hm := absoluteFirstMoment_pos
    have hbound := chosenScale_bound
    nlinarith
  have he := actual_kappa_difference chosenScale
  nlinarith
theorem literal_gaussian_relu_kappa_counterexample :
    unitLaw.map (perturbation chosenScale) = gaussianReal 0 (perturbationVariance chosenScale) ∧
    0 < chosenScale ∧ score 0 = 1/2 ∧
    literalCoefficientKappa chosenScale < interactionKappa chosenScale := by
  rw [literal_coefficient_kappa_eq]
  exact gaussian_relu_kappa_counterexample
end Harsanyi.DifficultyKappa
