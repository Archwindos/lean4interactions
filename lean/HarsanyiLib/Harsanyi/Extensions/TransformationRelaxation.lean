import Harsanyi.Extensions.TransformationEBM
import Mathlib.Analysis.SpecialFunctions.Sigmoid

namespace Harsanyi.Entropy
open Finset
open scoped BigOperators

noncomputable def relaxedPrior (p s : ℝ) : ℝ := 1-p+s*(2*p-1)

theorem relaxed_prior_endpoints (p : ℝ) : relaxedPrior p 0 = 1-p ∧ relaxedPrior p 1 = p := by
  constructor <;> unfold relaxedPrior <;> ring

theorem relaxed_prior_hasDerivAt (p s : ℝ) :
    HasDerivAt (relaxedPrior p) (2*p-1) s := by
  convert ((hasDerivAt_id s).mul_const (2*p-1)).const_add (1-p) using 1
  ring

theorem relaxed_prior_positive (p s : ℝ) (hp : 0 < p) (hp1 : p < 1)
    (hs : 0 ≤ s) (hs1 : s ≤ 1) : 0 < relaxedPrior p s := by
  have he : relaxedPrior p s = (1-s)*(1-p)+s*p := by unfold relaxedPrior; ring
  rw [he]
  by_cases hz : s=0
  · simp [hz]; linarith
  · exact add_pos_of_nonneg_of_pos (mul_nonneg (sub_nonneg.mpr hs1) (by linarith))
      (mul_pos (lt_of_le_of_ne hs (Ne.symm hz)) hp)

theorem sigmoid_gate_hasDerivAt (β x : ℝ) :
    HasDerivAt (fun t => Real.sigmoid (β*t))
      (Real.sigmoid (β*x)*(1-Real.sigmoid (β*x))*β) x := by
  simpa only [id_eq, mul_one] using
    (Real.hasDerivAt_sigmoid (β*x)).comp x ((hasDerivAt_id x).const_mul β)

theorem swish_hasDerivAt (β x : ℝ) :
    HasDerivAt (fun t => t*Real.sigmoid (β*t))
      (Real.sigmoid (β*x)+x*(Real.sigmoid (β*x)*(1-Real.sigmoid (β*x))*β)) x := by
  simpa only [id_eq, one_mul] using
    (hasDerivAt_id x).mul (sigmoid_gate_hasDerivAt β x)

theorem relaxed_prior_sigmoid_positive (p β x : ℝ) (hp : 0 < p) (hp1 : p < 1) :
    0 < relaxedPrior p (Real.sigmoid (β*x)) :=
  relaxed_prior_positive p _ hp hp1 (Real.sigmoid_nonneg _) (Real.sigmoid_le_one _)

/-- The author's linear extension is positive on the sigmoid range, but need
not be positive on the unbounded state space of an unconstrained Gaussian step. -/
theorem relaxed_prior_outside_domain : relaxedPrior (3/4) (-1) = -1/4 := by
  norm_num [relaxedPrior]

variable {D E F : Type*} [Fintype D]
  [NormedAddCommGroup E] [NormedSpace ℝ E]
  [NormedAddCommGroup F] [NormedSpace ℝ F]

noncomputable def frozenStateLoss (z : ℝ) (f : F → ℝ) (q : D → F → ℝ) (s : E → F) (θ : E) : ℝ :=
  z-f (s θ)-∑ d, Real.log (q d (s θ))

/-- Exact chain rule for source Eq.(40) on the stated smooth relaxation:
the EBM and its partition are frozen, and every prior factor is positive. -/
theorem frozen_state_loss_hasFDerivAt (z : ℝ) (f : F → ℝ) (q : D → F → ℝ)
    (s : E → F) (θ : E) (df : F →L[ℝ] ℝ) (dq : D → F →L[ℝ] ℝ) (ds : E →L[ℝ] F)
    (hf : HasFDerivAt f df (s θ)) (hq : ∀ d, HasFDerivAt (q d) (dq d) (s θ))
    (hpos : ∀ d, 0 < q d (s θ)) (hs : HasFDerivAt s ds θ) :
    HasFDerivAt (frozenStateLoss z f q s)
      (-(df.comp ds)-∑ d, (q d (s θ))⁻¹ • (dq d).comp ds) θ := by
  unfold frozenStateLoss
  exact ((hf.comp θ hs).const_sub z).sub
    (HasFDerivAt.fun_sum (u := (univ : Finset D))
      (fun d _ => ((hq d).comp θ hs).log (hpos d).ne'))

/-- Source Eq.(38)'s equality after the approximate expectation replacement.
Synthesized and data states are frozen during this parameter derivative. -/
theorem frozen_monte_carlo_derivative {A : Type*} [Fintype A]
    (r t : Law A) (f : A → E → ℝ) (df : A → E →L[ℝ] ℝ) (θ : E)
    (hf : ∀ a, HasFDerivAt (f a) (df a) θ) :
    HasFDerivAt (fun x => (∑ a, t.mass a*f a x)-(∑ a, r.mass a*f a x))
      ((∑ a, t.mass a • df a)-(∑ a, r.mass a • df a)) θ := by
  exact (HasFDerivAt.fun_sum (u := (univ : Finset A)) (fun a _ => (hf a).const_mul (t.mass a))).sub
    (HasFDerivAt.fun_sum (u := (univ : Finset A)) (fun a _ => (hf a).const_mul (r.mass a)))

/-- Source Eq.(40)'s entire finite layer/sample sum, allowing a different state
space at each layer. Weights may be the source 1/n for every sample, so their
sum is the number of penalized layers rather than being forced to one. -/
theorem frozen_batch_state_loss_hasFDerivAt {I : Type*} [Fintype I]
    (S C : I → Type*) [∀ i, NormedAddCommGroup (S i)] [∀ i, NormedSpace ℝ (S i)]
    [∀ i, Fintype (C i)]
    (w z : I → ℝ) (f : ∀ i, S i → ℝ) (q : ∀ i, C i → S i → ℝ)
    (s : ∀ i, E → S i) (θ : E)
    (df : ∀ i, S i →L[ℝ] ℝ) (dq : ∀ i, C i → S i →L[ℝ] ℝ) (ds : ∀ i, E →L[ℝ] S i)
    (hf : ∀ i, HasFDerivAt (f i) (df i) (s i θ))
    (hq : ∀ i d, HasFDerivAt (q i d) (dq i d) (s i θ))
    (hpos : ∀ i d, 0 < q i d (s i θ))
    (hs : ∀ i, HasFDerivAt (s i) (ds i) θ) :
    HasFDerivAt (fun x => ∑ i, w i*frozenStateLoss (z i) (f i) (q i) (s i) x)
      (∑ i, w i • (-(df i).comp (ds i)-∑ d, (q i d (s i θ))⁻¹ • (dq i d).comp (ds i))) θ := by
  exact HasFDerivAt.fun_sum (u := (univ : Finset I)) (fun i _ =>
    (frozen_state_loss_hasFDerivAt (z i) (f i) (q i) (s i) θ
      (df i) (dq i) (ds i) (hf i) (hq i) (hpos i) (hs i)).const_mul (w i))

end Harsanyi.Entropy
