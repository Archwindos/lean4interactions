import Harsanyi.Extensions.TransformationCorrelation
import Harsanyi.Extensions.TransformationGates

namespace Harsanyi.Entropy
open Finset MeasureTheory
open scoped BigOperators
variable {Ω A : Type*} [MeasurableSpace Ω] [Fintype A]

theorem entropy_le_card (p : Law A) : entropy p.mass ≤ Fintype.card A := by
  have ht (a : A) : Real.negMulLog (p.mass a) ≤ 1 := by
    have h := gibbs_term (p.mass a) 1 (p.nonneg a) (by norm_num) (fun _ => one_ne_zero)
    simp only [div_one, Real.negMulLog] at h ⊢
    linarith [p.nonneg a]
  exact (sum_le_sum (fun a _ => ht a)).trans_eq (by simp)

theorem kernel_mass_integrable (μ : Measure Ω) [IsProbabilityMeasure μ]
    (k : Ω → Law A) (a : A) (hm : Measurable (fun x => (k x).mass a)) :
    Integrable (fun x => (k x).mass a) μ := by
  apply (integrable_const (1:ℝ)).mono' hm.aestronglyMeasurable
  filter_upwards [] with x
  rw [Real.norm_eq_abs, abs_of_nonneg ((k x).nonneg a)]
  exact law_mass_le_one _ _

noncomputable def mixtureLaw (μ : Measure Ω) [IsProbabilityMeasure μ]
    (k : Ω → Law A) (hm : ∀ a, Measurable (fun x => (k x).mass a)) : Law A where
  mass := fun a => ∫ x, (k x).mass a ∂μ
  nonneg := fun a => integral_nonneg (fun x => (k x).nonneg a)
  total := by
    rw [← integral_finset_sum _ (fun a _ => kernel_mass_integrable μ k a (hm a))]
    simp only [(k _).total]
    simp

theorem kernel_entropy_measurable (k : Ω → Law A)
    (hm : ∀ a, Measurable (fun x => (k x).mass a)) :
    Measurable (fun x => entropy (k x).mass) := by
  apply Finset.measurable_sum
  intro a _
  exact Real.continuous_negMulLog.measurable.comp (hm a)

theorem kernel_entropy_integrable (μ : Measure Ω) [IsProbabilityMeasure μ]
    (k : Ω → Law A) (hm : ∀ a, Measurable (fun x => (k x).mass a)) :
    Integrable (fun x => entropy (k x).mass) μ := by
  apply (integrable_const (Fintype.card A:ℝ)).mono' (kernel_entropy_measurable k hm).aestronglyMeasurable
  filter_upwards [] with x
  rw [Real.norm_eq_abs, abs_of_nonneg (entropy_nonneg (k x))]
  exact entropy_le_card _

variable {Y G : Type*} [Fintype Y] [Fintype G]

theorem row_kernel_measurable (k : Ω → Law (Y × G))
    (hm : ∀ a, Measurable (fun x => (k x).mass a)) (y : Y) :
    Measurable (fun x => (rowLaw (k x)).mass y) := by
  exact Finset.measurable_sum _ (fun g _ => hm (y,g))

theorem column_kernel_measurable (k : Ω → Law (Y × G))
    (hm : ∀ a, Measurable (fun x => (k x).mass a)) (g : G) :
    Measurable (fun x => (columnLaw (k x)).mass g) := by
  exact Finset.measurable_sum _ (fun y _ => hm (y,g))

theorem mutual_information_conditional_entropy (p : Law (Y × G)) :
    mutualInformation p.mass = entropy (columnLaw p).mass - conditionalEntropy p.mass := by
  have h := entropy_chain p.mass p.nonneg
  unfold mutualInformation
  change entropy p.mass = entropy (rowLaw p).mass + conditionalEntropy p.mass at h
  change entropy (rowLaw p).mass+entropy (columnLaw p).mass-entropy p.mass = _
  linarith

theorem conditional_kernel_entropy_integrable (μ : Measure Ω) [IsProbabilityMeasure μ]
    (k : Ω → Law (Y × G)) (hm : ∀ a, Measurable (fun x => (k x).mass a)) :
    Integrable (fun x => conditionalEntropy (k x).mass) μ := by
  have h := (kernel_entropy_integrable μ k hm).sub
    (kernel_entropy_integrable μ (fun x => rowLaw (k x)) (row_kernel_measurable k hm))
  apply h.congr
  filter_upwards [] with x
  have hc := entropy_chain (k x).mass (k x).nonneg
  change entropy (k x).mass = entropy (rowLaw (k x)).mass + conditionalEntropy (k x).mass at hc
  change entropy (k x).mass - entropy (rowLaw (k x)).mass = conditionalEntropy (k x).mass
  linarith

/-- Actual arbitrary-input conditional MI chain. Both terms are integrable
because finite-output entropy is bounded, including zero-probability rows. -/
theorem integral_conditional_information (μ : Measure Ω) [IsProbabilityMeasure μ]
    (k : Ω → Law (Y × G)) (hm : ∀ a, Measurable (fun x => (k x).mass a)) :
    (∫ x, mutualInformation (k x).mass ∂μ) =
      (∫ x, entropy (columnLaw (k x)).mass ∂μ) -
        (∫ x, conditionalEntropy (k x).mass ∂μ) := by
  simp_rw [mutual_information_conditional_entropy]
  exact integral_sub
    (kernel_entropy_integrable μ (fun x => columnLaw (k x)) (column_kernel_measurable k hm))
    (conditional_kernel_entropy_integrable μ k hm)

noncomputable def randomGateCoInformation (μ : Measure Ω) [IsProbabilityMeasure μ]
    (k : Ω → Law (Y × G)) (hm : ∀ a, Measurable (fun x => (k x).mass a)) : ℝ :=
  mutualInformation (mixtureLaw μ k hm).mass - ∫ x, mutualInformation (k x).mass ∂μ

variable {ι : Type*} [Fintype ι] [DecidableEq ι]

/-- Full random-gate source Eq.(3), from the actual conditional kernel and its
actual integrated joint law; no information/entropy equality is a premise. -/
theorem random_gate_correlation_identity (μ : Measure Ω) [IsProbabilityMeasure μ]
    (k : Ω → Law (Y × (ι → Bool))) (hm : ∀ a, Measurable (fun x => (k x).mass a)) :
    randomGateCoInformation μ k hm + totalCorrelation (columnLaw (mixtureLaw μ k hm)) -
      (∑ y, (rowLaw (mixtureLaw μ k hm)).mass y *
        totalCorrelation (conditionalRow (mixtureLaw μ k hm) y)) =
      (∑ d, entropy (coordinateLaw (columnLaw (mixtureLaw μ k hm)) d).mass) -
      (∑ y, (rowLaw (mixtureLaw μ k hm)).mass y *
        ∑ d, entropy (coordinateLaw (conditionalRow (mixtureLaw μ k hm) y) d).mass) -
      ((∫ x, entropy (columnLaw (k x)).mass ∂μ) - (∫ x, conditionalEntropy (k x).mass ∂μ)) := by
  have hc := label_information_correlation_identity (mixtureLaw μ k hm)
  unfold randomGateCoInformation
  rw [integral_conditional_information μ k hm]
  linarith

/-- Full random-gate input-MI version of source Eq.(17). -/
theorem random_input_correlation_identity (μ : Measure Ω) [IsProbabilityMeasure μ]
    (k : Ω → Law (ι → Bool)) (hm : ∀ a, Measurable (fun x => (k x).mass a)) :
    (entropy (mixtureLaw μ k hm).mass - (∫ x, entropy (k x).mass ∂μ)) +
      totalCorrelation (mixtureLaw μ k hm) =
      (∑ d, entropy (coordinateLaw (mixtureLaw μ k hm) d).mass) -
        (∫ x, entropy (k x).mass ∂μ) :=
  information_correlation_identity _ _

end Harsanyi.Entropy
