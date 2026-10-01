import Harsanyi.Extensions.TransformationAffine
import Harsanyi.Extensions.TransformationRefinement
import Harsanyi.Extensions.TransformationCounterexamples
import Harsanyi.Extensions.TransformationRelaxation
import Harsanyi.Extensions.TransformationKernels
import Harsanyi.Extensions.TransformationOperators
import Harsanyi.Extensions.TransformationGaussianCounterexample

/-! Source Eq.(1): actual heterogeneous-width ReLU evaluation agrees with the
fixed-gate affine chain on precisely the inputs producing those gate patterns. -/
namespace PaperTransformation
open Harsanyi.GatedAffine
open MeasureTheory ProbabilityTheory
open scoped BigOperators
variable (dim : ℕ → ℕ)

/-! The main IB paragraph reuses Y for labels and network predictions. A
constant actual ReLU feature does not screen off a perfectly informative label.
The singleton conditioning law makes the conditional distribution explicit. -/
noncomputable def ibFeatureLaw : Harsanyi.Entropy.Law PUnit where
  mass := fun _ => 1
  nonneg := by intro z; norm_num
  total := by simp

noncomputable def ibJointLaw : Harsanyi.Entropy.Law (PUnit × (Bool × Bool)) :=
  Harsanyi.Entropy.kernelLaw ibFeatureLaw (fun _ => Harsanyi.Entropy.sameBit)

theorem ib_actual_constant_relu (x : Bool) : max (0 : ℝ) (0 * Harsanyi.Entropy.signedInput x + 1) = 1 := by
  norm_num

theorem ib_label_conditioning_law (z : PUnit) :
    (Harsanyi.Entropy.conditionalRow ibJointLaw z).mass = Harsanyi.Entropy.sameBit.mass := by
  funext xy
  have hz : (Harsanyi.Entropy.rowLaw ibJointLaw).mass z = 1 := by
    exact Harsanyi.Entropy.kernel_marginal ibFeatureLaw (fun _ => Harsanyi.Entropy.sameBit) z
  simp only [Harsanyi.Entropy.conditionalRow, hz, one_ne_zero, ite_false, div_one]
  simp [ibJointLaw, Harsanyi.Entropy.kernelLaw, ibFeatureLaw]

theorem ib_data_label_conditional_information :
    (∑ z : PUnit, (Harsanyi.Entropy.rowLaw ibJointLaw).mass z *
      Harsanyi.Entropy.mutualInformation (Harsanyi.Entropy.conditionalRow ibJointLaw z).mass) =
        Real.log 2 := by
  simp_rw [ib_label_conditioning_law]
  simp [ibJointLaw, Harsanyi.Entropy.kernel_marginal, Harsanyi.Entropy.rowLaw,
    ibFeatureLaw, Harsanyi.Entropy.same_bit_information]

theorem ib_data_label_not_screened_off :
    (∑ z : PUnit, (Harsanyi.Entropy.rowLaw ibJointLaw).mass z *
      Harsanyi.Entropy.mutualInformation (Harsanyi.Entropy.conditionalRow ibJointLaw z).mass) ≠ 0 := by
  rw [ib_data_label_conditional_information]
  exact ne_of_gt (Real.log_pos (by norm_num : (1 : ℝ) < 2))

noncomputable def reluGate {D : Type*} (h : D → ℝ) : D → ℝ :=
  fun d => if 0 < h d then 1 else 0

theorem relu_scalar_fixed_gate (x : ℝ) : max 0 x = (if 0<x then 1 else 0)*x := by
  split_ifs with h
  · rw [max_eq_right h.le]; simp
  · rw [max_eq_left (le_of_not_gt h)]; simp

def gateLinear {D : Type*} (s : D → ℝ) : (D → ℝ) →ₗ[ℝ] (D → ℝ) where
  toFun := fun h d => s d*h d
  map_add' := by intro x y; funext d; simp [mul_add]
  map_smul' := by intro c x; funext d; simp; ring

noncomputable def reluOutput (W : ∀ n, Space dim n →ₗ[ℝ] Space dim (n+1))
    (b : ∀ n, Space dim (n+1)) (x : Space dim 0) : ∀ n, Space dim n
  | 0 => x
  | n+1 => fun d => max 0 ((W n (reluOutput W b x n)+b n) d)

def frozenWeight (W : ∀ n, Space dim n →ₗ[ℝ] Space dim (n+1))
    (s : ∀ n, Space dim (n+1)) (n : ℕ) : Space dim n →ₗ[ℝ] Space dim (n+1) :=
  (gateLinear (s n)).comp (W n)

def frozenBias (b s : ∀ n, Space dim (n+1)) (n : ℕ) : Space dim (n+1) := gateLinear (s n) (b n)

theorem actual_relu_agrees_fixed_gate (W : ∀ n, Space dim n →ₗ[ℝ] Space dim (n+1))
    (b s : ∀ n, Space dim (n+1)) (x : Space dim 0) (L : ℕ)
    (hs : ∀ n, n<L → reluGate (W n (reluOutput dim W b x n)+b n)=s n) :
    reluOutput dim W b x L = networkOutput dim (frozenWeight dim W s) (frozenBias dim b s) x L := by
  induction L with
  | zero => rfl
  | succ L ih =>
    have hg := hs L (Nat.lt_succ_self L)
    have hi := ih (fun n hn => hs n (Nat.lt_succ_of_lt hn))
    funext d
    change max 0 ((W L (reluOutput dim W b x L)+b L) d) =
      s L d * (W L (networkOutput dim (frozenWeight dim W s) (frozenBias dim b s) x L)) d + s L d*(b L) d
    rw [relu_scalar_fixed_gate]
    have hd := congrFun hg d
    change (if 0 < (W L (reluOutput dim W b x L)+b L) d then 1 else 0) = s L d at hd
    rw [hd, hi]
    simp only [Pi.add_apply, mul_add]

theorem actual_relu_region_affine (W : ∀ n, Space dim n →ₗ[ℝ] Space dim (n+1))
    (b s : ∀ n, Space dim (n+1)) (x : Space dim 0) (L : ℕ)
    (hs : ∀ n, n<L → reluGate (W n (reluOutput dim W b x n)+b n)=s n) :
    reluOutput dim W b x L =
      (networkAffine dim (frozenWeight dim W s) (frozenBias dim b s) L).linear x +
      networkOutput dim (frozenWeight dim W s) (frozenBias dim b s) 0 L := by
  rw [actual_relu_agrees_fixed_gate dim W b s x L hs]
  exact network_output_linear_bias dim _ _ x L

/-- Include the final ungated linear output layer in the author's Eq.(1). -/
theorem actual_relu_module_affine (W : ∀ n, Space dim n →ₗ[ℝ] Space dim (n+1))
    (b s : ∀ n, Space dim (n+1)) (x : Space dim 0) (L : ℕ)
    (hs : ∀ n, n<L → reluGate (W n (reluOutput dim W b x n)+b n)=s n)
    {D : Type*} [AddCommGroup D] [Module ℝ D] (U : Space dim L →ₗ[ℝ] D) (c : D) :
    U (reluOutput dim W b x L)+c =
      (U.comp (networkAffine dim (frozenWeight dim W s) (frozenBias dim b s) L).linear) x +
      (U (networkOutput dim (frozenWeight dim W s) (frozenBias dim b s) 0 L)+c) := by
  rw [actual_relu_region_affine dim W b s x L hs]
  simp [map_add, add_assoc]

/-! Original Appendix A operators are evaluated before identifying them with
their fixed gates, rather than inserting the desired affine result as a premise. -/
theorem actual_dropout_module_affine {E D : Type*} [AddCommGroup E] [Module ℝ E]
    (W : E →ₗ[ℝ] (D → ℝ)) (b : D → ℝ) (keep : D → Bool) (x : E) :
    dropoutLinear keep (W x+b) =
      (layer ((dropoutLinear keep).comp W) (dropoutLinear keep b)) x :=
  fixed_dropout_layer_affine W b keep x

theorem actual_pool_module_affine {E D P : Type*} [AddCommGroup E] [Module ℝ E]
    (W : E →ₗ[ℝ] (D → ℝ)) (b : D → ℝ) (window : P → Finset D)
    (hne : ∀ p, (window p).Nonempty) (select : P → D) (x : E)
    (hsel : ∀ p, select p ∈ window p)
    (hmax : ∀ p d, d ∈ window p → (W x+b) d ≤ (W x+b) (select p)) :
    finiteMaxPool window hne (W x+b) =
      (layer ((selectedPoolLinear select).comp W) (selectedPoolLinear select b)) x :=
  fixed_pool_layer_affine W b window hne select x hsel hmax

theorem actual_gaussian_eq24_model (q : NNReal) (hq : 0 < q) :
    (Harsanyi.Entropy.gaussianFeatureSpace q).map
      (fun p => (Harsanyi.Entropy.noisyConstantRelu p,p.1)) =
      (ProbabilityTheory.gaussianReal 1 q) ⊗ₘ Harsanyi.Entropy.gaussianLabelKernel ∧
    Harsanyi.Entropy.actualConstantFeatureEstimator q <
      Harsanyi.Entropy.entropy Harsanyi.Entropy.bitLaw.mass -
        (∫ z : ℝ, Harsanyi.Entropy.entropy
          (fun y => (Harsanyi.Entropy.gaussianLabelKernel z {y}).toReal)
          ∂ProbabilityTheory.gaussianReal 1 q) := by
  rw [Harsanyi.Entropy.actual_gaussian_feature_information_zero]
  exact ⟨Harsanyi.Entropy.gaussian_feature_joint_kernel q,
    Harsanyi.Entropy.actual_constant_feature_estimator_negative q⟩
end PaperTransformation
