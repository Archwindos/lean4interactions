import Harsanyi.Extensions.DecoderGrid

namespace Harsanyi.Frequency
open Finset AddChar
open scoped BigOperators
variable {M N : ℕ} [NeZero M] [NeZero N]

theorem grid_character_comm (a b : Grid M N) :
    gridCharacter a.1 a.2 b = gridCharacter b.1 b.2 a := by
  simp only [grid_character_apply,mul_comm]

theorem grid_character_sum (u : ZMod M) (v : ZMod N) :
    (∑ x : Grid M N, gridCharacter u v x) =
      if u=0 ∧ v=0 then ((M*N : ℕ) : ℂ) else 0 := by
  rw [AddChar.sum_eq_ite]
  simp only [grid_character_trivial,Fintype.card_prod,ZMod.card]

theorem grid_orthogonality (u u' : ZMod M) (v v' : ZMod N) :
    (∑ x : Grid M N, gridCharacter (u-u') (v-v') x) =
      if u=u' ∧ v=v' then ((M*N : ℕ) : ℂ) else 0 := by
  rw [grid_character_sum]
  simp only [sub_eq_zero]

theorem dft2_twice (f : Grid M N → ℂ) (a : Grid M N) :
    dft2 (fun k => dft2 f k.1 k.2) a.1 a.2 = (M*N : ℕ)*f (-a) := by
  unfold dft2 transform
  simp_rw [mul_sum]
  rw [sum_comm]
  have hh (x k : Grid M N) :
      gridCharacter a.1 a.2 (-k)*(gridCharacter k.1 k.2 (-x)*f x) =
        gridCharacter (a.1+x.1) (a.2+x.2) (-k)*f x := by
    rw [grid_character_comm k (-x)]
    simp only [grid_character_apply,Prod.fst_neg,Prod.snd_neg,add_mul,
      mul_neg,neg_mul,neg_add,sub_eq_add_neg,map_add_eq_mul,mul_comm k.1 x.1,mul_comm k.2 x.2]
    ring
  simp_rw [hh,← sum_mul]
  have hn (u : ZMod M) (v : ZMod N) :
      (∑ k : Grid M N, gridCharacter u v (-k)) =
        if u=0 ∧ v=0 then ((M*N : ℕ) : ℂ) else 0 := by
    have hr : (∑ k : Grid M N, gridCharacter u v (-k)) = ∑ k, gridCharacter u v k :=
      Fintype.sum_equiv (Equiv.neg _) _ _ (fun _ => rfl)
    rw [hr,grid_character_sum]
  simp_rw [hn]
  have he (x : Grid M N) : a.1+x.1=0 ∧ a.2+x.2=0 ↔ x=-a := by
    rw [add_comm a.1,add_comm a.2]
    simp only [add_eq_zero_iff_eq_neg,Prod.ext_iff,Prod.fst_neg,Prod.snd_neg]
  simp only [he,ite_mul,zero_mul]
  simp

noncomputable def inverseDft2 (f : Grid M N → ℂ) (x : Grid M N) : ℂ :=
  ((M*N : ℕ) : ℂ)⁻¹ * dft2 f (-x.1) (-x.2)

theorem inverse_dft2 (f : Grid M N → ℂ) :
    inverseDft2 (fun k => dft2 f k.1 k.2) = f := by
  funext x
  simp only [inverseDft2]
  rw [show dft2 (fun k => dft2 f k.1 k.2) (-x.1) (-x.2) =
      (M*N : ℕ)*f x by simpa using dft2_twice f (-x)]
  rw [← mul_assoc,inv_mul_cancel₀]
  · simp
  · exact Nat.cast_ne_zero.mpr (Nat.mul_ne_zero (NeZero.ne M) (NeZero.ne N))

theorem std_character_conjugate {n : ℕ} [NeZero n] (z : ZMod n) :
    starRingEnd ℂ (ZMod.stdAddChar z) = ZMod.stdAddChar (-z) := by
  rw [ZMod.stdAddChar_apply,ZMod.stdAddChar_apply]
  calc
    starRingEnd ℂ (ZMod.toCircle z : ℂ) = ((ZMod.toCircle z)⁻¹ : Circle) :=
      (Circle.coe_inv_eq_conj _).symm
    _ = (ZMod.toCircle (-z) : ℂ) := by rw [map_neg_eq_inv]

theorem grid_character_conjugate (a x : Grid M N) :
    starRingEnd ℂ (gridCharacter a.1 a.2 x) = gridCharacter a.1 a.2 (-x) := by
  simp only [grid_character_apply,map_mul,std_character_conjugate,
    Prod.fst_neg,Prod.snd_neg,mul_neg]

theorem grid_character_neg_frequency (a x : Grid M N) :
    gridCharacter (-a.1) (-a.2) (-x) = gridCharacter a.1 a.2 x := by
  simp only [grid_character_apply,Prod.fst_neg,Prod.snd_neg,neg_mul_neg]

theorem dft2_neg_input (f : Grid M N → ℂ) (a : Grid M N) :
    dft2 (fun x => f (-x)) a.1 a.2 = dft2 f (-a.1) (-a.2) := by
  unfold dft2 transform
  apply Fintype.sum_equiv (Equiv.neg _)
  intro x
  simpa only [Equiv.neg_apply,neg_neg] using
    congrArg (fun z => z*f (-x)) (grid_character_neg_frequency a (-x)).symm

theorem dft2_inverse (f : Grid M N → ℂ) (a : Grid M N) :
    dft2 (inverseDft2 f) a.1 a.2 = f a := by
  change transform (gridCharacter a.1 a.2)
    (fun x => ((M*N : ℕ) : ℂ)⁻¹ * dft2 f (-x.1) (-x.2)) = _
  rw [transform_smul]
  change ((M*N : ℕ) : ℂ)⁻¹ * dft2 (fun x => dft2 f (-x.1) (-x.2)) a.1 a.2 = _
  have hn := dft2_neg_input (fun k => dft2 f k.1 k.2) a
  simp only [Prod.fst_neg,Prod.snd_neg] at hn
  rw [hn]
  rw [show dft2 (fun k => dft2 f k.1 k.2) (-a.1) (-a.2) =
      (M*N : ℕ)*f a by simpa using dft2_twice f (-a)]
  rw [← mul_assoc,inv_mul_cancel₀]
  · simp
  · exact Nat.cast_ne_zero.mpr (Nat.mul_ne_zero (NeZero.ne M) (NeZero.ne N))

theorem hermitian_inverse_real (f : Grid M N → ℂ)
    (hf : ∀ k, f (-k)=starRingEnd ℂ (f k)) (x : Grid M N) :
    starRingEnd ℂ (inverseDft2 f x) = inverseDft2 f x := by
  unfold inverseDft2 dft2 transform
  rw [map_mul]
  simp only [map_inv₀,Complex.conj_natCast]
  congr 1
  rw [map_sum]
  have hh (k : Grid M N) :
      starRingEnd ℂ (gridCharacter (-x.1) (-x.2) (-k)*f k) =
        gridCharacter (-x.1) (-x.2) (-(-k))*f (-k) := by
    rw [map_mul,← hf,grid_character_conjugate (-x.1,-x.2) (-k)]
  simp_rw [hh]
  exact Fintype.sum_equiv (Equiv.neg _) _ _ (fun _ => rfl)

theorem dft2_parseval_pair (f g : Grid M N → ℂ) :
    (∑ k : Grid M N, starRingEnd ℂ (dft2 f k.1 k.2)*dft2 g k.1 k.2) =
      ((M*N : ℕ) : ℂ) * ∑ x : Grid M N, starRingEnd ℂ (f x)*g x := by
  unfold dft2 transform
  simp_rw [map_sum,map_mul,mul_sum,sum_mul]
  rw [sum_comm]
  have hh (x y k : Grid M N) :
      starRingEnd ℂ (gridCharacter k.1 k.2 (-x))*starRingEnd ℂ (f x)*
          (gridCharacter k.1 k.2 (-y)*g y) =
        gridCharacter (x.1-y.1) (x.2-y.2) k * (starRingEnd ℂ (f x)*g y) := by
    rw [grid_character_conjugate k (-x)]
    simp only [neg_neg]
    rw [grid_character_comm k x,grid_character_comm k (-y)]
    simp only [grid_character_apply,sub_eq_add_neg,add_mul,neg_mul,
      Prod.fst_neg,Prod.snd_neg,map_add_eq_mul]
    ring
  have hp (x : Grid M N) :
      (∑ k : Grid M N, ∑ y : Grid M N,
        starRingEnd ℂ (gridCharacter k.1 k.2 (-x))*starRingEnd ℂ (f x)*
          (gridCharacter k.1 k.2 (-y)*g y)) =
        ((M*N : ℕ) : ℂ)*(starRingEnd ℂ (f x)*g x) := by
    rw [sum_comm]
    simp_rw [hh,← sum_mul,grid_character_sum]
    have he (y : Grid M N) : x.1-y.1=0 ∧ x.2-y.2=0 ↔ y=x := by
      simp only [sub_eq_zero,Prod.ext_iff]
      exact and_congr eq_comm eq_comm
    simp only [he,ite_mul,zero_mul]
    simp
  calc
    _ = ∑ k : Grid M N, ∑ x : Grid M N, ∑ y : Grid M N,
      starRingEnd ℂ (gridCharacter k.1 k.2 (-x))*starRingEnd ℂ (f x)*
        (gridCharacter k.1 k.2 (-y)*g y) := by
      rw [sum_comm]
      apply sum_congr rfl
      intro k _
      rw [sum_comm]
    _ = ∑ x : Grid M N, ∑ k : Grid M N, ∑ y : Grid M N,
      starRingEnd ℂ (gridCharacter k.1 k.2 (-x))*starRingEnd ℂ (f x)*
        (gridCharacter k.1 k.2 (-y)*g y) := by rw [sum_comm]
    _ = _ := by simp_rw [hp]

theorem dft2_parseval_normSq (f : Grid M N → ℂ) :
    (∑ k : Grid M N, Complex.normSq (dft2 f k.1 k.2)) =
      (M*N : ℕ)*∑ x : Grid M N, Complex.normSq (f x) := by
  have h := congrArg Complex.re (dft2_parseval_pair f f)
  simpa only [Complex.re_sum,Complex.mul_re,Complex.ofReal_re,Complex.ofReal_im,
    Complex.natCast_re,Complex.natCast_im,zero_mul,sub_zero,
    Complex.conj_re,Complex.conj_im,neg_mul,sub_neg_eq_add,Complex.normSq_apply] using h

end Harsanyi.Frequency
