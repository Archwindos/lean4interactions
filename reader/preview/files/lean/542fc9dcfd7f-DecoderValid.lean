import Harsanyi.Extensions.DecoderFourier
import Harsanyi.Extensions.DecoderKernelMoments

/-! Fourier mixing for an actual cropped positive-offset convolution.  Both
DFTs are the unnormalised `dft2`; the inverse factor is the original grid size.
General output dimensions mean periodic extension followed by sampling/cropping,
not arbitrary padding. In the valid rectangle, valid_index_bounds proves that
every sampled index stays in the original physical array.
The crop is defined by the canonical integer representatives, not a group
homomorphism between the two grids. -/
namespace Harsanyi.Frequency.Valid
open Finset AddChar
open scoped BigOperators
variable {M N A B : ℕ} [NeZero M] [NeZero N] [NeZero A] [NeZero B]

noncomputable def cropIndex (x : Grid A B) : Grid M N :=
  ((x.1.val : ZMod M), (x.2.val : ZMod N))

noncomputable def crop (f : Grid M N → ℂ) : Grid A B → ℂ :=
  fun x => f (cropIndex x)

noncomputable def mixingAlpha (out : Grid A B) (old : Grid M N) : ℂ :=
  ((M*N : ℕ) : ℂ)⁻¹ * ∑ x : Grid A B,
    gridCharacter out.1 out.2 (-x) * gridCharacter old.1 old.2 (cropIndex x)

theorem inverse_dft2_character (f : Grid M N → ℂ) (x : Grid M N) :
    inverseDft2 f x = ((M*N : ℕ) : ℂ)⁻¹ *
      ∑ k : Grid M N, gridCharacter k.1 k.2 x * f k := by
  simp only [inverseDft2,dft2,transform,grid_character_apply,
    Prod.fst_neg,Prod.snd_neg,neg_mul_neg]
  simp only [mul_comm x.1,mul_comm x.2]

theorem crop_dft (f : Grid M N → ℂ) (out : Grid A B) :
    dft2 (crop f) out.1 out.2 =
      ∑ old : Grid M N, mixingAlpha out old * dft2 f old.1 old.2 := by
  have he (x : Grid A B) : f (cropIndex x) = ((M*N : ℕ) : ℂ)⁻¹ *
      ∑ k : Grid M N, gridCharacter k.1 k.2 (cropIndex x) * dft2 f k.1 k.2 := by
    rw [← inverse_dft2_character]
    exact (congrFun (inverse_dft2 f) (cropIndex x)).symm
  change (∑ x : Grid A B, gridCharacter out.1 out.2 (-x) * f (cropIndex x)) = _
  simp_rw [he,mul_sum]
  rw [sum_comm]
  apply sum_congr rfl
  intro old _
  simp only [mixingAlpha,mul_sum,sum_mul]
  apply sum_congr rfl
  intro x _
  ring

noncomputable def croppedOffsetLayer {I C D : Type*} [Fintype I] [Fintype C]
    (shift : I → Grid M N) (w : D → C → I → ℂ)
    (f : C → Grid M N → ℂ) (b : D → ℂ) (d : D) : Grid A B → ℂ :=
  crop (offsetLayer shift w f b d)

theorem cropped_offset_layer_dft {I C D : Type*} [Fintype I] [Fintype C]
    (shift : I → Grid M N) (w : D → C → I → ℂ)
    (f : C → Grid M N → ℂ) (b : D → ℂ) (d : D) (out : Grid A B) :
    dft2 (croppedOffsetLayer shift w f b d) out.1 out.2 =
      ∑ old : Grid M N, mixingAlpha out old *
        (∑ c, offsetResponse shift (w d c) old.1 old.2 * dft2 (f c) old.1 old.2 +
          if old.1=0 ∧ old.2=0 then (M*N : ℕ)*b d else 0) := by
  rw [croppedOffsetLayer,crop_dft]
  simp_rw [offset_layer_dft]

noncomputable def validLayer (K : ℕ) (w : Fin K × Fin K → ℂ)
    (f : Grid M N → ℂ) (x : Grid A B) : ℂ :=
  ∑ t : Fin K × Fin K, w t *
    f (((x.1.val+t.1.val : ℕ) : ZMod M), ((x.2.val+t.2.val : ℕ) : ZMod N))

theorem valid_layer_eq_crop (K : ℕ) (w : Fin K × Fin K → ℂ)
    (f : Grid M N → ℂ) :
    validLayer (A:=A) (B:=B) K w f =
      crop (fun x => ∑ t : Fin K × Fin K, w t * f (x+squareShift K t)) := by
  funext x
  simp [validLayer,crop,cropIndex,squareShift,Nat.cast_add,Prod.mk_add_mk]

/-- On the actual valid-convolution rectangle, every sampled integer is in
the original array; the modular implementation therefore never wraps. -/
theorem valid_index_bounds (K : ℕ) (hK : 0<K) (hKM : K≤M) (hKN : K≤N)
    (hA : A=M-K+1) (hB : B=N-K+1) (x : Grid A B) (t : Fin K × Fin K) :
    x.1.val+t.1.val < M ∧ x.2.val+t.2.val < N := by
  have hx := ZMod.val_lt x.1
  have hy := ZMod.val_lt x.2
  have ht := t.1.isLt
  have hs := t.2.isLt
  omega

theorem valid_indices_no_wrap (K : ℕ) (hK : 0<K) (hKM : K≤M) (hKN : K≤N)
    (hA : A=M-K+1) (hB : B=N-K+1) (x : Grid A B) (t : Fin K × Fin K) :
    (((x.1.val+t.1.val : ℕ) : ZMod M).val = x.1.val+t.1.val) ∧
    (((x.2.val+t.2.val : ℕ) : ZMod N).val = x.2.val+t.2.val) := by
  have hb := valid_index_bounds K hK hKM hKN hA hB x t
  exact ⟨ZMod.val_natCast_of_lt hb.1,ZMod.val_natCast_of_lt hb.2⟩

theorem valid_layer_dft (K : ℕ) (w : Fin K × Fin K → ℂ)
    (f : Grid M N → ℂ) (out : Grid A B) :
    dft2 (validLayer K w f) out.1 out.2 =
      ∑ old : Grid M N, mixingAlpha out old *
        (offsetResponse (squareShift K) w old.1 old.2 * dft2 f old.1 old.2) := by
  rw [valid_layer_eq_crop,crop_dft]
  apply sum_congr rfl
  intro old _
  congr 1
  have h := offset_layer_dft (squareShift K)
    (fun (_ : Unit) (_ : Unit) => w) (fun (_ : Unit) => f) (fun (_ : Unit) => 0)
    () old.1 old.2
  have he : offsetLayer (squareShift K) (fun (_ : Unit) (_ : Unit) => w)
      (fun (_ : Unit) => f) (fun (_ : Unit) => 0) () =
      fun x => ∑ t : Fin K × Fin K, w t * f (x+squareShift K t) := by
    funext x
    simp [offsetLayer]
  rw [he] at h
  simpa using h

theorem cropped_offset_layer_dft_bias {I C D : Type*} [Fintype I] [Fintype C]
    (shift : I → Grid M N) (w : D → C → I → ℂ)
    (f : C → Grid M N → ℂ) (b : D → ℂ) (d : D) (out : Grid A B) :
    dft2 (croppedOffsetLayer shift w f b d) out.1 out.2 =
      (if out.1=0 ∧ out.2=0 then (A*B : ℕ)*b d else 0) +
      ∑ old : Grid M N, mixingAlpha out old *
        ∑ c, offsetResponse shift (w d c) old.1 old.2 * dft2 (f c) old.1 old.2 := by
  have he : croppedOffsetLayer shift w f b d =
      fun x : Grid A B => croppedOffsetLayer shift w f (fun _ => 0) d x + b d := by
    funext x
    simp [croppedOffsetLayer,crop,offsetLayer]
  rw [he]
  change transform (gridCharacter out.1 out.2) _ = _
  rw [transform_add]
  change dft2 (croppedOffsetLayer shift w f (fun _ => 0) d) out.1 out.2 +
    dft2 (fun _ => b d) out.1 out.2 = _
  rw [cropped_offset_layer_dft,dft2_constant]
  simp only [mul_zero,ite_self,add_zero]
  rw [add_comm]

noncomputable def realValidLayer (K : ℕ) (w : Fin K × Fin K → ℝ)
    (f : Grid M N → ℝ) (x : Grid A B) : ℝ :=
  ∑ t : Fin K × Fin K, w t *
    f (((x.1.val+t.1.val : ℕ) : ZMod M), ((x.2.val+t.2.val : ℕ) : ZMod N))

theorem real_valid_layer_embedding (K : ℕ) (w : Fin K × Fin K → ℝ)
    (f : Grid M N → ℝ) :
    (fun x : Grid A B => (realValidLayer K w f x : ℂ)) =
      validLayer K (fun t => (w t : ℂ)) (fun x => (f x : ℂ)) := by
  funext x
  simp [realValidLayer,validLayer,Complex.ofReal_sum]

noncomputable def deltaKernel (t : Fin 2 × Fin 2) : ℝ := if t=(0,0) then 1 else 0

theorem real_valid_constant_delta :
    realValidLayer (M:=3) (N:=3) (A:=2) (B:=2) 2 deltaKernel (fun _ => 1) =
      fun _ => 1 := by
  funext x
  simp [realValidLayer,deltaKernel]

theorem actual_valid_output_frequency_zero :
    dft2 (fun x : Grid 2 2 =>
      (realValidLayer (M:=3) (N:=3) 2 deltaKernel (fun _ => 1) x : ℂ)) 1 1 = 0 := by
  rw [real_valid_constant_delta]
  norm_num [dft2_constant]

theorem original_constant_spectrum (k : Grid 3 3) :
    dft2 (fun _ : Grid 3 3 => (1:ℂ)) k.1 k.2 = if k=(0,0) then 9 else 0 := by
  rw [dft2_constant]
  have he : k.1=0 ∧ k.2=0 ↔ k=(0,0) := by simp [Prod.ext_iff]
  simp [he]

theorem actual_mixing_alpha_zero : mixingAlpha (M:=3) (N:=3) ((1,1) : Grid 2 2) (0,0) = 0 := by
  have h := crop_dft (fun _ : Grid 3 3 => (1:ℂ)) ((1,1) : Grid 2 2)
  have hc : crop (A:=2) (B:=2) (fun _ : Grid 3 3 => (1:ℂ)) = fun _ => 1 := rfl
  rw [hc] at h
  simp only [original_constant_spectrum,ite_mul,mul_ite,mul_zero,zero_mul] at h
  norm_num [dft2_constant] at h
  exact h

noncomputable def printedValidAlpha (M N K : ℕ) (lam gam : ℝ) : ℂ :=
  ((M*N : ℕ) : ℂ)⁻¹ *
    ((Real.sin ((M-K : ℕ)*lam*Real.pi)/Real.sin (lam*Real.pi) : ℝ) : ℂ) *
    ((Real.sin ((N-K : ℕ)*gam*Real.pi)/Real.sin (gam*Real.pi) : ℝ) : ℂ) *
    Complex.exp (Complex.I * (((M-K : ℕ)*lam+(N-K : ℕ)*gam)*Real.pi : ℝ))

noncomputable def frequencyDifference (oldSize outSize : ℕ) (oldFreq outFreq : ℕ) : ℝ :=
  (oldFreq:ℝ)/oldSize-(outFreq:ℝ)/outSize

theorem witness_frequency_difference : frequencyDifference 3 2 0 1 = (-1/2:ℝ) := by
  norm_num [frequencyDifference]

theorem witness_grid_frequency_difference :
    frequencyDifference 3 2 (0 : ZMod 3).val (1 : ZMod 2).val = (-1/2:ℝ) := by
  rw [show (0 : ZMod 3).val = 0 by rfl,show (1 : ZMod 2).val = 1 by rfl]
  exact witness_frequency_difference

theorem printed_valid_alpha_value : printedValidAlpha 3 3 2 (-1/2) (-1/2) = -(1/9:ℂ) := by
  have hs : Real.sin ((-1/2:ℝ)*Real.pi) ≠ 0 := by
    rw [show (-1/2:ℝ)*Real.pi = -(Real.pi/2) by ring]
    simp
  have he : Complex.I * (((-1/2:ℝ)+(-1/2))*Real.pi : ℝ) =
      -(Real.pi : ℂ)*Complex.I := by push_cast; ring
  simp only [printedValidAlpha,Nat.reduceMul,Nat.reduceSub,Nat.cast_ofNat,
    Nat.cast_one,one_mul,div_self hs,Complex.ofReal_one,mul_one]
  rw [he,show -(Real.pi : ℂ)*Complex.I = -((Real.pi : ℂ)*Complex.I) by ring,
    Complex.exp_neg,Complex.exp_pi_mul_I]
  norm_num

theorem actual_valid_equation17_counterexample :
    Real.sin ((-1/2:ℝ)*Real.pi) ≠ 0 ∧
    mixingAlpha (M:=3) (N:=3) ((1,1) : Grid 2 2) (0,0) = 0 ∧
    printedValidAlpha 3 3 2 (-1/2) (-1/2) = -(1/9:ℂ) ∧
    dft2 (fun x : Grid 2 2 =>
      (realValidLayer (M:=3) (N:=3) 2 deltaKernel (fun _ => 1) x : ℂ)) 1 1 ≠
      printedValidAlpha 3 3 2 (-1/2) (-1/2) *
        offsetResponse (squareShift 2) (fun t => (deltaKernel t : ℂ)) (0 : ZMod 3) (0 : ZMod 3) *
        dft2 (fun _ : Grid 3 3 => (1:ℂ)) 0 0 := by
  refine ⟨?_,actual_mixing_alpha_zero,printed_valid_alpha_value,?_⟩
  · rw [show (-1/2:ℝ)*Real.pi = -(Real.pi/2) by ring]
    simp
  · rw [actual_valid_output_frequency_zero,printed_valid_alpha_value]
    norm_num [offsetResponse,deltaKernel,grid_character_apply,dft2_constant,apply_ite]

theorem exponential_sine_factor (z : ℂ) :
    Complex.exp (2*z*Complex.I)-1 =
      Complex.exp (z*Complex.I) * (2*Complex.I*Complex.sin z) := by
  have hd : Complex.exp (z*Complex.I)-Complex.exp (-z*Complex.I) =
      2*Complex.I*Complex.sin z := by
    rw [← Complex.cos_add_sin_I,← Complex.cos_sub_sin_I]
    ring
  have hm : Complex.exp (z*Complex.I)*Complex.exp (-z*Complex.I) = 1 := by
    rw [← Complex.exp_add]
    simp
  rw [show 2*z*Complex.I = z*Complex.I+z*Complex.I by ring,Complex.exp_add]
  calc
    _ = Complex.exp (z*Complex.I)*
        (Complex.exp (z*Complex.I)-Complex.exp (-z*Complex.I)) := by rw [mul_sub,hm]
    _ = _ := by rw [hd]

/-- The finite geometric polynomial has n terms. The quotient is asserted only
where its sine denominator is nonzero; geometric itself covers every boundary. -/
theorem geometric_sine_quotient (n : ℕ) (z : ℂ) (hs : Complex.sin z ≠ 0) :
    geometric n (Complex.exp (2*z*Complex.I)) =
      Complex.exp (((n:ℂ)-1)*z*Complex.I) *
        (Complex.sin ((n:ℂ)*z) / Complex.sin z) := by
  have hf := exponential_sine_factor z
  have hd : Complex.exp (2*z*Complex.I) ≠ 1 := by
    apply sub_ne_zero.mp
    rw [hf]
    exact mul_ne_zero (Complex.exp_ne_zero _) (mul_ne_zero (mul_ne_zero (by norm_num) Complex.I_ne_zero) hs)
  rw [geometric_quotient n _ hd]
  have hp : Complex.exp (2*z*Complex.I)^n = Complex.exp (2*((n:ℂ)*z)*Complex.I) := by
    rw [← Complex.exp_nat_mul]
    congr 1
    ring
  rw [hp,exponential_sine_factor,hf]
  have he : Complex.exp (((n:ℂ)-1)*z*Complex.I)*Complex.exp (z*Complex.I) =
      Complex.exp ((n:ℂ)*z*Complex.I) := by
    rw [← Complex.exp_add]
    congr 1
    ring
  apply (div_eq_iff (mul_ne_zero (Complex.exp_ne_zero _)
    (mul_ne_zero (mul_ne_zero (by norm_num) Complex.I_ne_zero) hs))).mpr
  field_simp [hs]
  rw [show z*Complex.I*((n:ℂ)-1) = ((n:ℂ)-1)*z*Complex.I by ring]
  calc
    _ = Complex.sin ((n:ℂ)*z) *
        (Complex.exp (((n:ℂ)-1)*z*Complex.I)*Complex.exp (z*Complex.I)) := by rw [he]; ring
    _ = _ := by ring

theorem geometric_real_sine_quotient (n : ℕ) (theta : ℝ) (hs : Real.sin theta ≠ 0) :
    geometric n (Complex.exp (2*(theta:ℂ)*Complex.I)) =
      Complex.exp (((n:ℂ)-1)*(theta:ℂ)*Complex.I) *
        ((Real.sin ((n:ℝ)*theta)/Real.sin theta : ℝ) : ℂ) := by
  have hc : Complex.sin (theta:ℂ) ≠ 0 := by rw [← Complex.ofReal_sin]; exact_mod_cast hs
  simpa only [← Complex.ofReal_natCast,← Complex.ofReal_mul,← Complex.ofReal_sin,
    ← Complex.ofReal_div] using geometric_sine_quotient n (theta:ℂ) hc

end Harsanyi.Frequency.Valid
