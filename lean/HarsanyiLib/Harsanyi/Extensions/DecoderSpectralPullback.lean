import Harsanyi.Extensions.DecoderBackprop

namespace Harsanyi.Frequency
open Finset AddChar
open scoped BigOperators
variable {M N : ℕ} [NeZero M] [NeZero N]
variable {I : Type*} [Fintype I]

noncomputable def spatialInnerPullback (f d : Grid M N → ℂ) (t : Grid M N) : ℂ :=
  ∑ x,starRingEnd ℂ (f (x+t))*d x

theorem shifted_inner_parseval (f d : Grid M N → ℂ) (t : Grid M N) :
    spatialInnerPullback f d t = ((M*N : ℕ) : ℂ)⁻¹ *
      ∑ k : Grid M N,gridCharacter k.1 k.2 (-t)*
        starRingEnd ℂ (dft2 f k.1 k.2)*dft2 d k.1 k.2 := by
  have hp := dft2_parseval_pair (fun x => f (x+t)) d
  have ht (k : Grid M N) : dft2 (fun x => f (x+t)) k.1 k.2 =
      gridCharacter k.1 k.2 t * dft2 f k.1 k.2 := transform_shift _ f t
  simp_rw [ht,map_mul,grid_character_conjugate] at hp
  have hc : ((M*N : ℕ) : ℂ) ≠ 0 := Nat.cast_ne_zero.mpr
    (Nat.mul_ne_zero (NeZero.ne M) (NeZero.ne N))
  rw [hp,inv_mul_cancel_left₀ hc]
  rfl

noncomputable def crossFrequencyKernel (shift : I → Grid M N)
    (u uk : ZMod M) (v vk : ZMod N) : ℂ :=
  ((M*N : ℕ) : ℂ)⁻¹ * ∑ t,gridCharacter (u-uk) (v-vk) (shift t)

theorem character_frequency_difference (u uk : ZMod M) (v vk : ZMod N) (t : Grid M N) :
    gridCharacter u v t * gridCharacter uk vk (-t) =
      gridCharacter (u-uk) (v-vk) t := by
  simp only [grid_character_apply,sub_eq_add_neg,add_mul,neg_mul,
    Prod.fst_neg,Prod.snd_neg,mul_neg,map_add_eq_mul]
  ring

theorem spectral_kernel_pullback (shift : I → Grid M N) (f d : Grid M N → ℂ)
    (u : ZMod M) (v : ZMod N) :
    offsetResponse shift (fun t => spatialInnerPullback f d (shift t)) u v =
      ∑ k : Grid M N,crossFrequencyKernel shift u k.1 v k.2 *
        starRingEnd ℂ (dft2 f k.1 k.2)*dft2 d k.1 k.2 := by
  unfold offsetResponse
  simp_rw [shifted_inner_parseval,mul_sum,sum_mul]
  rw [sum_comm]
  apply sum_congr rfl
  intro k _
  unfold crossFrequencyKernel
  rw [mul_sum, sum_mul, sum_mul]
  apply sum_congr rfl
  intro t _
  have hh := character_frequency_difference u k.1 v k.2 (shift t)
  rw [← hh]
  ring

theorem cross_frequency_diagonal (shift : I → Grid M N) (u : ZMod M) (v : ZMod N) :
    crossFrequencyKernel shift u u v v =
      (Fintype.card I : ℂ)/((M*N : ℕ) : ℂ) := by
  simp [crossFrequencyKernel,grid_character_apply,div_eq_mul_inv,mul_comm]

theorem actual_real_spatial_pullback {f d : Grid M N → ℝ} (t : Grid M N) :
    spatialInnerPullback (fun x => (f x : ℂ)) (fun x => (d x : ℂ)) t =
      ((∑ x : Grid M N,f (x+t)*d x : ℝ) : ℂ) := by
  simp [spatialInnerPullback,Complex.ofReal_mul,Complex.ofReal_sum]

end Harsanyi.Frequency
