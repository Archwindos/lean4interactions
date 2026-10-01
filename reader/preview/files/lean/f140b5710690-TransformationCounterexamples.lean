import Harsanyi.Extensions.TransformationEntropy
import Harsanyi.Extensions.TransformationCorrelation
import Harsanyi.Extensions.TransformationGates

namespace Harsanyi.Entropy
open Finset
open scoped BigOperators

noncomputable def extendedReluGateLaw : Law (Bool × (Bool × Bool)) where
  mass := fun z => if z.2.1 = true ∧ z.2.2 = z.1 then 1/2 else 0
  nonneg := by intro z; split_ifs <;> norm_num
  total := by simp [Fintype.sum_prod_type, Fintype.sum_bool] <;> norm_num

theorem extended_relu_gate_information : mutualInformation extendedReluGateLaw.mass = Real.log 2 := by
  rw [mutual_information_graph extendedReluGateLaw (fun y => (true,y))]
  · simp [entropy, columnLaw, extendedReluGateLaw, Fintype.sum_prod_type, Fintype.sum_bool,
      Real.negMulLog, one_div, Real.log_inv]
    ring
  · intro y g h
    have h' : ¬(g.1 = true ∧ g.2 = y) := by
      intro hh
      apply h
      exact Prod.ext hh.1 hh.2
    simp [extendedReluGateLaw, h']

/-- Two actual scalar ReLU layers give the constant first gate and a label-equal
second gate; the law retains both coordinates of the larger prefix. -/
theorem relu_prefix_clause_counterexample :
    (∀ x : Bool, 0 < signedInput x + 2) ∧
    (∀ x : Bool, (0 < firstFeature x - 2) ↔ x = true) ∧
    ¬(mutualInformation extendedReluGateLaw.mass ≤ mutualInformation constantGate.mass) := by
  refine ⟨first_relu_gate_constant, second_relu_gate_label, ?_⟩
  rw [extended_relu_gate_information, constant_gate_information]
  exact not_le.mpr (Real.log_pos (by norm_num : (1:ℝ)<2))

noncomputable def scalarGate (b : Bool) : ℝ := if b then 1 else 0

theorem scalar_gate_mean : (∑ b, bitLaw.mass b * scalarGate b) = 1/2 := by
  norm_num [bitLaw, scalarGate, Fintype.sum_bool]

theorem scalar_gate_variance : (∑ b, bitLaw.mass b * (scalarGate b - 1/2)^2) = 1/4 := by
  norm_num [bitLaw, scalarGate, Fintype.sum_bool]

noncomputable def binaryGateKDE (bandwidth : ℝ) : ℝ :=
  -∑ b : Bool, (1/2 : ℝ) * Real.log
    (∑ c : Bool, (1/2 : ℝ) * Real.exp (-(scalarGate b - scalarGate c)^2 / (2*bandwidth)))

theorem binary_gate_kde_formula (bandwidth : ℝ) :
    binaryGateKDE bandwidth = Real.log 2 - Real.log (1+Real.exp (-1/(2*bandwidth))) := by
  unfold binaryGateKDE
  simp [Fintype.sum_bool, scalarGate]
  have h : (1/2:ℝ) + 1/2*Real.exp (-1/(2*bandwidth)) =
      (1+Real.exp (-1/(2*bandwidth))) / 2 := by ring
  simp only [one_div] at h
  rw [add_comm ((2:ℝ)⁻¹*Real.exp _) ((2:ℝ)⁻¹)]
  simp_rw [h, Real.log_div (by positivity : (1+Real.exp (-1/(2*bandwidth))) ≠ 0)
    (by norm_num : (2:ℝ) ≠ 0)]
  ring

/-- This witness substitutes the author's variance bandwidth κ Var(Σ), rather
than selecting a free Gaussian width unrelated to the actual gate law. -/
theorem variance_bandwidth_kde_counterexample (κ : ℝ) (hk : 0 < κ) :
    binaryGateKDE (κ * (∑ b, bitLaw.mass b * (scalarGate b - 1/2)^2)) < entropy bitLaw.mass := by
  rw [scalar_gate_variance, bit_entropy, binary_gate_kde_formula]
  have h : (-1:ℝ)/(2*(κ*(1/4))) = -2/κ := by ring
  rw [h]
  exact two_point_kde_counterexample κ hk

theorem singleton_class_kernel_zero (bw s : ℝ) :
    -Real.log (Real.exp (-(s-s)^2/(2*bw))) = 0 := by simp

/-- Eq.(27) with n=M=2 and one state in each class. The printed class weights
are then normalized, every class KDE is zero, and conditional gate/label MI
given input is zero. Thus this counterexample does not rely on the separate
class-weight error. -/
theorem normalized_class_co_information_bound_counterexample (κ : ℝ) (hk : 0 < κ) :
    binaryGateKDE (κ*(∑ b, bitLaw.mass b*(scalarGate b-1/2)^2)) -
      ((1/2)*(-Real.log (Real.exp (-(0-0:ℝ)^2/(2*(κ/4)))))+
       (1/2)*(-Real.log (Real.exp (-(1-1:ℝ)^2/(2*(κ/4)))))) - 0 <
    mutualInformation sameBit.mass := by
  simp only [sub_self, ne_eq, zero_pow (by norm_num : (2:ℕ)≠0), neg_zero,
    zero_div, Real.exp_zero, Real.log_one, neg_zero, mul_zero, add_zero, sub_zero]
  rw [same_bit_information, ← bit_entropy]
  exact variance_bandwidth_kde_counterexample κ hk

/-- Actual X,B-independent dropout followed by ReLU has gate X∧B. Removing
the dropout gives gate X. The four equally probable states induce this law. -/
noncomputable def dropoutReluLaw : Law (Bool × Bool) where
  mass := fun z => if z.1 = false ∧ z.2 = false then 1/2 else
    if z.1 = true then 1/4 else 0
  nonneg := by intro z; split_ifs <;> norm_num
  total := by simp [Fintype.sum_prod_type, Fintype.sum_bool] <;> norm_num

theorem dropout_relu_gate (x b : Bool) :
    (0 < max (0:ℝ) (scalarGate x * scalarGate b)) ↔ x = true ∧ b = true := by
  cases x <;> cases b <;> norm_num [scalarGate]

theorem removed_dropout_gate (x : Bool) : (0 < max (0:ℝ) (scalarGate x)) ↔ x = true := by
  cases x <;> norm_num [scalarGate]

theorem dropout_relu_information : mutualInformation dropoutReluLaw.mass = (3/4)*Real.log (4/3) := by
  have h2 : Real.log (1/2:ℝ) = -Real.log 2 := by simpa using Real.log_inv (2:ℝ)
  have h4 : Real.log (1/4:ℝ) = -2*Real.log 2 := by
    rw [show (1/4:ℝ)=(2^2)⁻¹ by norm_num, Real.log_inv, Real.log_pow]
    norm_num
  have h34 : Real.log (3/4:ℝ) = Real.log 3 - 2*Real.log 2 := by
    rw [Real.log_div (by norm_num : (3:ℝ)≠0) (by norm_num : (4:ℝ)≠0),
      show (4:ℝ)=2^2 by norm_num, Real.log_pow]
    norm_num
  have h43 : Real.log (4/3:ℝ) = 2*Real.log 2 - Real.log 3 := by
    rw [Real.log_div (by norm_num : (4:ℝ)≠0) (by norm_num : (3:ℝ)≠0),
      show (4:ℝ)=2^2 by norm_num, Real.log_pow]
    norm_num
  norm_num [mutualInformation, entropy, marginal, dropoutReluLaw, Fintype.sum_bool,
    Fintype.sum_prod_type, Real.negMulLog, h2, h4, h34, h43]
  ring

theorem dropout_relu_variance :
    (∑ z : Bool × Bool, dropoutReluLaw.mass z * (scalarGate z.2 - 1/4)^2) = 3/16 := by
  norm_num [dropoutReluLaw, scalarGate, Fintype.sum_prod_type, Fintype.sum_bool]

theorem dropout_relu_actual_law :
    (pushLaw (independentLaw bitLaw bitLaw) (fun z => (z.1, z.1 && z.2))).mass =
      dropoutReluLaw.mass := by
  funext z
  rcases z with ⟨x,b⟩
  cases x <;> cases b <;>
    norm_num [pushLaw, independentLaw, bitLaw, dropoutReluLaw, Fintype.sum_prod_type,
      Fintype.sum_bool]

theorem log_four_thirds_lower : (1/4:ℝ) ≤ Real.log (4/3) := by
  have h := Real.log_le_sub_one_of_pos (by norm_num : (0:ℝ)<3/4)
  have hi : Real.log (3/4:ℝ) = -Real.log (4/3) := by
    rw [show (3/4:ℝ)=(4/3)⁻¹ by norm_num, Real.log_inv]
  rw [hi] at h
  linarith

theorem binary_kde_three_upper : binaryGateKDE 3 ≤ (1/6:ℝ) := by
  rw [binary_gate_kde_formula]
  norm_num
  have he : Real.exp (-1/6:ℝ) ≤ 1 := Real.exp_le_one_iff.mpr (by norm_num)
  have h := Real.log_le_log (by positivity : (0:ℝ)<2*Real.exp (-1/6))
    (show 2*Real.exp (-1/6:ℝ) ≤ 1+Real.exp (-1/6) by linarith)
  rw [Real.log_mul (by norm_num : (2:ℝ)≠0) (Real.exp_ne_zero _), Real.log_exp] at h
  linarith

/-- Eq.(26) fails with genuine additional dropout randomness. κ=16 and the
actual Var(Σ)=3/16 give bandwidth 3, while the sampling-removed gate is X. -/
theorem additional_randomness_kde_counterexample :
    binaryGateKDE (16 * (∑ z : Bool × Bool,
      dropoutReluLaw.mass z * (scalarGate z.2 - 1/4)^2)) < mutualInformation dropoutReluLaw.mass := by
  rw [dropout_relu_variance, dropout_relu_information]
  norm_num
  have h := binary_kde_three_upper
  have hg := log_four_thirds_lower
  nlinarith

noncomputable def gateDistanceSq (s t : Bool × Bool) : ℝ :=
  (scalarGate s.1 - scalarGate t.1)^2 + (scalarGate s.2 - scalarGate t.2)^2
def correlatedData (i : Fin 4) : Bool × Bool := if i.val < 2 then (false,false) else (true,true)
def independentData (i : Fin 4) : Bool × Bool :=
  if i.val = 0 then (false,false) else if i.val = 1 then (false,true) else
    if i.val = 2 then (true,false) else (true,true)
noncomputable def gateKernelSum (data : Fin 4 → Bool × Bool) (s : Bool × Bool) (bw : ℝ) : ℝ :=
  ∑ i, Real.exp (-gateDistanceSq s (data i) / (2*bw))
noncomputable def fourPointTCEstimate (bw : ℝ) : ℝ :=
  (1/4:ℝ) * ∑ i, Real.log
    (gateKernelSum correlatedData (correlatedData i) bw /
      gateKernelSum independentData (correlatedData i) bw)

theorem gate_kernel_sums (b : Bool) (bw : ℝ) :
    gateKernelSum correlatedData (b,b) bw = 2*(1+Real.exp (-2/(2*bw))) ∧
    gateKernelSum independentData (b,b) bw = 1+2*Real.exp (-1/(2*bw))+Real.exp (-2/(2*bw)) := by
  cases b <;> constructor <;>
    norm_num [gateKernelSum, correlatedData, independentData, gateDistanceSq, scalarGate,
      Fin.sum_univ_succ] <;> ring

theorem four_point_tc_formula (bw : ℝ) :
    fourPointTCEstimate bw = Real.log
      (2*(1+Real.exp (-1/(2*bw))^2) / (1+Real.exp (-1/(2*bw)))^2) := by
  have hs (i : Fin 4) : ∃ b, correlatedData i = (b,b) := by
    unfold correlatedData
    split_ifs
    · exact ⟨false,rfl⟩
    · exact ⟨true,rfl⟩
  have he : Real.exp (-2/(2*bw)) = Real.exp (-1/(2*bw))^2 := by
    rw [show (-2:ℝ)/(2*bw) = -1/(2*bw)+ -1/(2*bw) by ring, Real.exp_add]
    ring
  have h (i : Fin 4) : Real.log
      (gateKernelSum correlatedData (correlatedData i) bw /
        gateKernelSum independentData (correlatedData i) bw) =
      Real.log (2*(1+Real.exp (-1/(2*bw))^2)/(1+Real.exp (-1/(2*bw)))^2) := by
    obtain ⟨b,hb⟩ := hs i
    rw [hb, (gate_kernel_sums b bw).1, (gate_kernel_sums b bw).2, he]
    congr 2
    ring
  unfold fourPointTCEstimate
  simp_rw [h]
  simp

theorem exact_synthesis_tc_counterexample (bw : ℝ) :
    fourPointTCEstimate bw < divergence sameBit.mass
      (independentLaw (rowLaw sameBit) (columnLaw sameBit)).mass := by
  rw [← mutual_information_eq_divergence, same_bit_information, four_point_tc_formula]
  have ht : 0 < Real.exp (-1/(2*bw)) := Real.exp_pos _
  apply Real.log_lt_log (by positivity)
  apply (div_lt_iff₀ (by positivity : (0:ℝ)<(1+Real.exp (-1/(2*bw)))^2)).mpr
  nlinarith

theorem same_bit_vector_variance :
    (∑ s : Bool × Bool, sameBit.mass s *
      ((scalarGate s.1-1/2)^2 + (scalarGate s.2-1/2)^2)) = 1/2 := by
  norm_num [sameBit, scalarGate, Fintype.sum_prod_type, Fintype.sum_bool]

theorem source_bandwidth_tc_counterexample (κ : ℝ) (hk : 0 < κ) :
    fourPointTCEstimate (κ * (∑ s : Bool × Bool, sameBit.mass s *
      ((scalarGate s.1-1/2)^2+(scalarGate s.2-1/2)^2))) <
      divergence sameBit.mass (independentLaw (rowLaw sameBit) (columnLaw sameBit)).mass :=
  exact_synthesis_tc_counterexample _

/-- The two literal 1/P factors in source Eq.(24), with two singleton classes
and constant features, give a negative estimator, despite actual independent
continuous-feature/label information being zero. -/
theorem printed_constant_feature_estimator_negative :
    (-(Real.log ((1/2:ℝ)*(1+1))) -
      (1/2)*(-(1/2)*Real.log ((1/2:ℝ)*1)) -
      (1/2)*(-(1/2)*Real.log ((1/2:ℝ)*1))) < 0 := by
  have h := Real.log_pos (by norm_num : (1:ℝ)<2)
  have hhalf : Real.log (1/2:ℝ) = -Real.log 2 := by
    simpa using Real.log_inv (2:ℝ)
  norm_num
  rw [hhalf]
  nlinarith

theorem independent_continuous_feature_label_information_zero {Ω : Type*} [MeasurableSpace Ω]
    (μ : MeasureTheory.Measure Ω) [MeasureTheory.IsProbabilityMeasure μ] :
    entropy bitLaw.mass - (∫ _ : Ω, entropy bitLaw.mass ∂μ) = 0 := by
  simp

end Harsanyi.Entropy
