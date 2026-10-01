import Harsanyi.Extensions.DecoderFrequency

/-! Actual two-dimensional unnormalized DFT and positive-shift finite kernels.
Offsets are summed individually, including coincident modular offsets. -/
namespace Harsanyi.Frequency
open Finset AddChar
open scoped BigOperators
variable {M N : ℕ} [NeZero M] [NeZero N]

abbrev Grid (M N : ℕ) := ZMod M × ZMod N

noncomputable def gridCharacter (u : ZMod M) (v : ZMod N) : AddChar (Grid M N) ℂ where
  toFun := fun x => ZMod.stdAddChar (u*x.1) * ZMod.stdAddChar (v*x.2)
  map_zero_eq_one' := by simp
  map_add_eq_mul' := by
    intro x y
    simp only [Prod.fst_add, Prod.snd_add, mul_add, map_add_eq_mul]
    ring

@[simp] theorem grid_character_apply (u : ZMod M) (v : ZMod N) (x : Grid M N) :
    gridCharacter u v x = ZMod.stdAddChar (u*x.1)*ZMod.stdAddChar (v*x.2) := rfl

theorem grid_character_int (u v t s : ℤ) :
    gridCharacter (u : ZMod M) (v : ZMod N) ((t : ZMod M),(s : ZMod N)) =
      Complex.exp (2*Real.pi*Complex.I*(u*t)/M) *
        Complex.exp (2*Real.pi*Complex.I*(v*s)/N) := by
  simp only [grid_character_apply, ← Int.cast_mul]
  rw [ZMod.stdAddChar_coe, ZMod.stdAddChar_coe]

noncomputable def dft2 (f : Grid M N → ℂ) (u : ZMod M) (v : ZMod N) : ℂ :=
  transform (gridCharacter u v) f

theorem dft2_sum (f : Grid M N → ℂ) (u : ZMod M) (v : ZMod N) :
    dft2 f u v = ∑ m : ZMod M, ∑ n : ZMod N,
      ZMod.stdAddChar (-(u*m))*ZMod.stdAddChar (-(v*n))*f (m,n) := by
  simp only [dft2, transform, Fintype.sum_prod_type, grid_character_apply,
    Prod.fst_neg, Prod.snd_neg, mul_neg]

theorem grid_character_trivial (u : ZMod M) (v : ZMod N) :
    gridCharacter u v = 0 ↔ u = 0 ∧ v = 0 := by
  constructor
  · intro h
    have hm := congrArg (fun χ : AddChar (Grid M N) ℂ => χ (1,0)) h
    have hn := congrArg (fun χ : AddChar (Grid M N) ℂ => χ (0,1)) h
    simp only [grid_character_apply, mul_one, mul_zero, map_zero_eq_one, mul_one, one_mul,
      AddChar.zero_apply] at hm hn
    constructor
    · exact ZMod.injective_stdAddChar (hm.trans (map_zero_eq_one _).symm)
    · exact ZMod.injective_stdAddChar (hn.trans (map_zero_eq_one _).symm)
  · rintro ⟨rfl,rfl⟩
    ext x
    simp

theorem dft2_constant (u : ZMod M) (v : ZMod N) (b : ℂ) :
    dft2 (fun _ : Grid M N => b) u v = if u=0 ∧ v=0 then (M*N : ℕ)*b else 0 := by
  rw [dft2, transform_const]
  simp only [grid_character_trivial, Fintype.card_prod, ZMod.card]

noncomputable def offsetLayer {I C D : Type*} [Fintype I] [Fintype C]
    (shift : I → Grid M N) (w : D → C → I → ℂ)
    (f : C → Grid M N → ℂ) (b : D → ℂ) (d : D) (x : Grid M N) : ℂ :=
  ∑ c, ∑ t, w d c t * f c (x+shift t) + b d

noncomputable def offsetResponse {I : Type*} [Fintype I]
    (shift : I → Grid M N) (w : I → ℂ) (u : ZMod M) (v : ZMod N) : ℂ :=
  ∑ t, w t * gridCharacter u v (shift t)

theorem transform_finite_sum {I : Type*} [Fintype I] (χ : AddChar (Grid M N) ℂ)
    (f : I → Grid M N → ℂ) :
    transform χ (fun x => ∑ i, f i x) = ∑ i, transform χ (f i) := by
  unfold transform
  simp_rw [mul_sum]
  rw [sum_comm]

theorem offset_layer_dft {I C D : Type*} [Fintype I] [Fintype C]
    (shift : I → Grid M N) (w : D → C → I → ℂ)
    (f : C → Grid M N → ℂ) (b : D → ℂ) (d : D) (u : ZMod M) (v : ZMod N) :
    dft2 (offsetLayer shift w f b d) u v =
      ∑ c, offsetResponse shift (w d c) u v * dft2 (f c) u v +
        if u=0 ∧ v=0 then (M*N : ℕ)*b d else 0 := by
  unfold offsetLayer
  rw [dft2, transform_add, transform_finite_sum]
  have ht (c : C) : transform (gridCharacter u v)
      (fun x => ∑ t, w d c t * f c (x+shift t)) =
        offsetResponse shift (w d c) u v * dft2 (f c) u v := by
    rw [transform_finite_sum]
    simp_rw [transform_smul, transform_shift]
    simp only [offsetResponse, dft2, sum_mul, mul_assoc]
  simp_rw [ht]
  rw [show transform (gridCharacter u v) (fun _ => b d) =
      if u=0 ∧ v=0 then (M*N : ℕ)*b d else 0 from dft2_constant u v (b d)]

noncomputable def squareShift (K : ℕ) (t : Fin K × Fin K) : Grid M N :=
  ((t.1.val : ZMod M),(t.2.val : ZMod N))

theorem square_kernel_response (K : ℕ) (w : Fin K × Fin K → ℂ)
    (u : ZMod M) (v : ZMod N) :
    offsetResponse (squareShift K) w u v =
      ∑ t : Fin K, ∑ s : Fin K,
        w (t,s)*ZMod.stdAddChar (u*(t.val : ZMod M))*ZMod.stdAddChar (v*(s.val : ZMod N)) := by
  simp only [offsetResponse, Fintype.sum_prod_type, squareShift, grid_character_apply]
  congr 1
  funext t
  congr 1
  funext s
  ring

end Harsanyi.Frequency
