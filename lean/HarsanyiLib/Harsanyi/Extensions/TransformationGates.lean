import Harsanyi.Extensions.TransformationEntropy
import Mathlib.MeasureTheory.Integral.Bochner.Basic

/-! A deterministic finite gate on an arbitrary input probability space.
The input type is not assumed finite. A conditional label kernel determines the
joint gate/label law by mixture; conditional information is computed from that
kernel, rather than inserted as a zero-information hypothesis. -/
namespace Harsanyi.Entropy
open Finset MeasureTheory
open scoped BigOperators
variable {Ω Y G : Type*} [MeasurableSpace Ω] [Fintype Y] [Fintype G] [DecidableEq G]

noncomputable def gateLabelAt (f : Ω → G) (k : Ω → Law Y) (x : Ω) : Law (Y × G) where
  mass := fun z => if z.2 = f x then (k x).mass z.1 else 0
  nonneg := by intro z; split_ifs <;> simp_all [(k x).nonneg z.1]
  total := by
    classical
    simp [Fintype.sum_prod_type, (k x).total]

theorem gate_label_column (f : Ω → G) (k : Ω → Law Y) (x : Ω) (g : G) :
    (columnLaw (gateLabelAt f k x)).mass g = if g = f x then 1 else 0 := by
  classical
  simp [columnLaw, gateLabelAt, sum_ite_irrel, (k x).total]

theorem gate_label_conditional_information_zero (f : Ω → G) (k : Ω → Law Y) (x : Ω) :
    mutualInformation (gateLabelAt f k x).mass = 0 := by
  rw [mutual_information_graph (gateLabelAt f k x) (fun _ => f x)]
  · unfold entropy
    simp_rw [gate_label_column]
    apply sum_eq_zero
    intro g _
    split_ifs <;> simp
  · intro y g h
    simp [gateLabelAt, h]

theorem gate_label_entropy_zero (f : Ω → G) (k : Ω → Law Y) (x : Ω) :
    entropy (columnLaw (gateLabelAt f k x)).mass = 0 := by
  unfold entropy
  simp_rw [gate_label_column]
  apply sum_eq_zero
  intro g _
  split_ifs <;> simp

noncomputable def conditionalGateEntropy (μ : Measure Ω) (f : Ω → G) (k : Ω → Law Y) : ℝ :=
  ∫ x, entropy (columnLaw (gateLabelAt f k x)).mass ∂μ

theorem conditional_gate_entropy_zero (μ : Measure Ω) (f : Ω → G) (k : Ω → Law Y) :
    conditionalGateEntropy μ f k = 0 := by
  unfold conditionalGateEntropy
  simp_rw [gate_label_entropy_zero]
  simp

noncomputable def conditionalGateLabelInformation (μ : Measure Ω) (f : Ω → G)
    (k : Ω → Law Y) : ℝ := ∫ x, mutualInformation (gateLabelAt f k x).mass ∂μ

theorem conditional_gate_label_information_zero (μ : Measure Ω) (f : Ω → G)
    (k : Ω → Law Y) : conditionalGateLabelInformation μ f k = 0 := by
  unfold conditionalGateLabelInformation
  simp_rw [gate_label_conditional_information_zero]
  simp

theorem gate_label_mass_integrable (μ : Measure Ω) [IsProbabilityMeasure μ]
    (f : Ω → G) (k : Ω → Law Y) (z : Y × G)
    (hm : Measurable (fun x => (gateLabelAt f k x).mass z)) :
    Integrable (fun x => (gateLabelAt f k x).mass z) μ := by
  apply (integrable_const (1 : ℝ)).mono' hm.aestronglyMeasurable
  filter_upwards [] with x
  rw [Real.norm_eq_abs, abs_of_nonneg ((gateLabelAt f k x).nonneg z)]
  exact law_mass_le_one _ _

/-- The actual finite output pushforward law, obtained by integrating conditional
label probabilities together with the deterministic gate. -/
noncomputable def gateLabelLaw (μ : Measure Ω) [IsProbabilityMeasure μ]
    (f : Ω → G) (k : Ω → Law Y)
    (hm : ∀ z, Measurable (fun x => (gateLabelAt f k x).mass z)) : Law (Y × G) where
  mass := fun z => ∫ x, (gateLabelAt f k x).mass z ∂μ
  nonneg := fun z => integral_nonneg (fun x => (gateLabelAt f k x).nonneg z)
  total := by
    rw [← integral_finset_sum _ (fun z _ => gate_label_mass_integrable μ f k z (hm z))]
    simp only [(gateLabelAt f k _).total]
    simp

/-- Source co-information convention, expressed by its exact conditional MI
identity. The conditional component is an actual kernel integral. -/
noncomputable def deterministicGateCoInformation (μ : Measure Ω) [IsProbabilityMeasure μ]
    (f : Ω → G) (k : Ω → Law Y)
    (hm : ∀ z, Measurable (fun x => (gateLabelAt f k x).mass z)) : ℝ :=
  mutualInformation (gateLabelLaw μ f k hm).mass - conditionalGateLabelInformation μ f k

theorem deterministic_gate_co_information_eq (μ : Measure Ω) [IsProbabilityMeasure μ]
    (f : Ω → G) (k : Ω → Law Y)
    (hm : ∀ z, Measurable (fun x => (gateLabelAt f k x).mass z)) :
    deterministicGateCoInformation μ f k hm = mutualInformation (gateLabelLaw μ f k hm).mass := by
  simp [deterministicGateCoInformation, conditional_gate_label_information_zero]

/-- Property 1 adapter: arbitrary input probability space, actual deterministic
gate, finite label/gate law and genuine Shannon nonnegativity. -/
theorem deterministic_gate_co_information_nonneg (μ : Measure Ω) [IsProbabilityMeasure μ]
    (f : Ω → G) (k : Ω → Law Y)
    (hm : ∀ z, Measurable (fun x => (gateLabelAt f k x).mass z)) :
    0 ≤ deterministicGateCoInformation μ f k hm := by
  rw [deterministic_gate_co_information_eq]
  exact mutual_information_nonneg _

end Harsanyi.Entropy
