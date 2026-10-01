import Mathlib.Analysis.Fourier.ZMod
import Mathlib.Analysis.Fourier.FiniteAbelian.Orthogonality
import Mathlib.Tactic

/-! Finite circular correlation and its unnormalised Fourier representation.
The positive shift is the cross-correlation convention of the paper. -/
namespace Harsanyi.Frequency
open Finset AddChar
open scoped BigOperators
variable {G : Type*} [AddCommGroup G] [Fintype G]

noncomputable def transform (χ : AddChar G ℂ) (f : G → ℂ) : ℂ :=
  ∑ x, χ (-x) * f x
noncomputable def circularCorrelation (w f : G → ℂ) (x : G) : ℂ :=
  ∑ t, w t * f (x+t)
noncomputable def kernelResponse (χ : AddChar G ℂ) (w : G → ℂ) : ℂ :=
  ∑ t, w t * χ t

 theorem transform_add (χ : AddChar G ℂ) (f g : G → ℂ) :
    transform χ (fun x => f x+g x) = transform χ f + transform χ g := by
  simp [transform, mul_add, sum_add_distrib]

 theorem transform_smul (χ : AddChar G ℂ) (a : ℂ) (f : G → ℂ) :
    transform χ (fun x => a*f x) = a*transform χ f := by
  simp [transform, mul_left_comm, mul_comm, mul_assoc, mul_sum]

 theorem transform_shift (χ : AddChar G ℂ) (f : G → ℂ) (t : G) :
    transform χ (fun x => f (x+t)) = χ t * transform χ f := by
  unfold transform
  rw [mul_sum]
  apply Fintype.sum_equiv (Equiv.addRight t)
  intro x
  change χ (-x) * f (x+t) = χ t * (χ (-(x+t)) * f (x+t))
  have hh : χ t * χ (-(x+t)) = χ (-x) := by
    rw [← map_add_eq_mul]
    congr 1
    abel
  rw [← mul_assoc, hh]

 theorem transform_circularCorrelation (χ : AddChar G ℂ) (w f : G → ℂ) :
    transform χ (circularCorrelation w f) = kernelResponse χ w * transform χ f := by
  unfold circularCorrelation transform
  simp_rw [mul_sum]
  rw [sum_comm]
  have hh (t : G) : (∑ x : G, χ (-x)*(w t*f (x+t))) =
      w t * transform χ (fun x => f (x+t)) := by
    simp [transform, mul_sum]; congr 1; ext x; ring
  simp_rw [hh]
  simp_rw [transform_shift, ← mul_assoc]
  unfold kernelResponse
  simp_rw [mul_assoc]
  rw [← mul_sum]
  simpa only [mul_assoc, transform] using (sum_mul (univ : Finset G) (fun t => w t * χ t) (transform χ f)).symm

 theorem transform_const (χ : AddChar G ℂ) (b : ℂ) :
    transform χ (fun _ => b) = if χ = 0 then (Fintype.card G : ℂ)*b else 0 := by
  classical
  unfold transform
  rw [← sum_mul]
  have hh : (∑ x : G, χ (-x)) = ∑ x : G, χ x := by
    exact Fintype.sum_equiv (Equiv.neg G) _ _ (fun x => rfl)
  rw [hh, AddChar.sum_eq_ite]
  split_ifs <;> simp

 theorem affine_circular_layer (χ : AddChar G ℂ) (w f : G → ℂ) (b : ℂ) :
    transform χ (fun x => circularCorrelation w f x + b) =
      kernelResponse χ w * transform χ f +
        if χ = 0 then (Fintype.card G : ℂ)*b else 0 := by
  rw [transform_add, transform_circularCorrelation, transform_const]

variable {C D : Type*} [Fintype C] [Fintype D]
noncomputable def multiChannelLayer (w : D → C → G → ℂ) (f : C → G → ℂ)
    (b : D → ℂ) (d : D) (x : G) : ℂ :=
  ∑ c, circularCorrelation (w d c) (f c) x + b d

 theorem multiChannelLayer_fourier (χ : AddChar G ℂ) (w : D → C → G → ℂ)
    (f : C → G → ℂ) (b : D → ℂ) (d : D) :
    transform χ (multiChannelLayer w f b d) =
      ∑ c, kernelResponse χ (w d c) * transform χ (f c) +
        if χ = 0 then (Fintype.card G : ℂ)*b d else 0 := by
  unfold multiChannelLayer
  rw [transform_add, transform_const]
  congr 1
  unfold transform
  simp_rw [mul_sum]
  rw [sum_comm]
  apply sum_congr rfl
  intro c _
  rw [← mul_sum]
  exact transform_circularCorrelation χ (w d c) (f c)

/-- A finite geometric polynomial; it is defined even at z=1. -/
noncomputable def geometric (n : ℕ) (z : ℂ) : ℂ := ∑ t ∈ range n, z^t

 theorem geometric_one (n : ℕ) : geometric n 1 = n := by simp [geometric]

 theorem geometric_telescoping (n : ℕ) (z : ℂ) :
    geometric n z * (z-1) = z^n-1 := by
  unfold geometric
  induction n with
  | zero => simp
  | succ n ih => rw [sum_range_succ, add_mul, ih, pow_succ]; ring

 theorem geometric_quotient (n : ℕ) (z : ℂ) (hz : z ≠ 1) :
    geometric n z = (z^n-1)/(z-1) := by
  apply (eq_div_iff (sub_ne_zero.mpr hz)).2
  exact geometric_telescoping n z

 theorem geometric_root (n : ℕ) (z : ℂ) (hz : z^n=1) :
    geometric n z = if z=1 then n else 0 := by
  split_ifs with h
  · rw [h, geometric_one]
  · rw [geometric_quotient n z h, hz]; simp

 theorem geometric_norm_le (n : ℕ) (z : ℂ) (hz : ‖z‖=1) :
    ‖geometric n z‖ ≤ n := by
  calc
    ‖geometric n z‖ ≤ ∑ t ∈ range n, ‖z^t‖ := norm_sum_le _ _
    _ = n := by simp [norm_pow, hz]

/-- Exact two-layer product, including the term dropped by A.7 Eq.(48). -/
 theorem product_update_exact (a b da db : ℂ) :
    (a+da)*(b+db)-a*b = da*b+a*db+da*db := by ring

 theorem dropped_product_counterexample :
    ((1+(1:ℂ))*(1+1)-1*1) ≠ ((1:ℂ)*1+1*1) := by norm_num

 theorem complex_ofReal_zero_iff (variance : ℝ) :
    (variance : ℂ) = 0 ↔ variance = 0 := by simp

end Harsanyi.Frequency

namespace Harsanyi.Frequency
/-- Exact frequency responses of a real 2×2 kernel at (0,1) and (1,0)
for a 4×4 spatial grid. Coefficients are 1,i in the DFT convention. -/
noncomputable def response01 (a b c d : ℝ) : ℂ := (a+c : ℝ) + (b+d : ℝ)*Complex.I
noncomputable def response10 (a b c d : ℝ) : ℂ := (a+b : ℝ) + (c+d : ℝ)*Complex.I
/-- One-layer real loss when the other identity layer is fixed. -/
noncomputable def realLoss (α a b c d : ℝ) : ℝ :=
  (a+c-(1-α))^2 + (b+d)^2 + (a+b-(1+α))^2 + (c+d)^2

 theorem realLoss_gradient00 (α : ℝ) :
    HasDerivAt (fun q => realLoss α q 0 0 0) 0 1 := by
  convert (((hasDerivAt_id (1:ℝ)).sub_const (1-α)).pow 2).add
    (((hasDerivAt_id (1:ℝ)).sub_const (1+α)).pow 2) using 1 <;> first | (funext q; simp only [realLoss, Pi.add_apply, Pi.pow_apply, id_eq]; ring) | (simp only [id_eq]; ring)
 theorem realLoss_gradient01 (α : ℝ) :
    HasDerivAt (fun q => realLoss α 1 q 0 0) (-2*α) 0 := by
  convert ((hasDerivAt_id (0:ℝ)).pow 2).add
    (((hasDerivAt_id (0:ℝ)).sub_const α).pow 2) |>.const_add (α^2) using 1 <;> first | (funext q; simp only [realLoss, Pi.add_apply, Pi.pow_apply, id_eq]; ring) | (simp only [id_eq]; ring)
 theorem realLoss_gradient10 (α : ℝ) :
    HasDerivAt (fun q => realLoss α 1 0 q 0) (2*α) 0 := by
  convert (((hasDerivAt_id (0:ℝ)).add_const α).pow 2).add
    ((hasDerivAt_id (0:ℝ)).pow 2) |>.add_const (α^2) using 1 <;> first | (funext q; simp only [realLoss, Pi.add_apply, Pi.pow_apply, id_eq]; ring) | (simp only [id_eq]; ring)
 theorem realLoss_gradient11 (α : ℝ) :
    HasDerivAt (fun q => realLoss α 1 0 0 q) 0 0 := by
  convert (((hasDerivAt_id (0:ℝ)).pow 2).add ((hasDerivAt_id (0:ℝ)).pow 2)).const_add
    (2*α^2) using 1 <;> first | (funext q; simp only [realLoss, Pi.add_apply, Pi.pow_apply, id_eq]; ring) | (simp only [id_eq]; ring)

 theorem two_layer_one_step_counterexample (α η : ℝ) (ha : 0<α) (he : 0<η) :
    (response10 1 (2*η*α) (-2*η*α) 0)^2 ≠ (1+α : ℂ) := by
  intro h
  have him := congrArg Complex.im h
  simp [response10, Complex.mul_re, Complex.mul_im, pow_two] at him
  have hc : 0 < 2*η*α := by positivity
  nlinarith
end Harsanyi.Frequency
