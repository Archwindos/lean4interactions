import Harsanyi.Extensions.DecoderGrid

/-! Zero insertion is a finite pushforward. Its character evaluation proves the
repeated spectrum with the same unnormalised DFT, without an aliasing assumption. -/
namespace Harsanyi.Frequency
open Finset AddChar
open scoped BigOperators

noncomputable def scatter {A B : Type*} [Fintype A] [DecidableEq B]
    (pos : A → B) (f : A → ℂ) (x : B) : ℂ :=
  ∑ a, if pos a=x then f a else 0

theorem scatter_original {A B : Type*} [Fintype A] [DecidableEq B] [DecidableEq A]
    (pos : A → B) (f : A → ℂ) (hi : Function.Injective pos) (a : A) :
    scatter pos f (pos a) = f a := by
  simp [scatter,hi.eq_iff]

theorem scatter_elsewhere {A B : Type*} [Fintype A] [DecidableEq B]
    (pos : A → B) (f : A → ℂ) (x : B) (hx : x ∉ Set.range pos) :
    scatter pos f x = 0 := by
  have h (a : A) : pos a ≠ x := fun hh => hx ⟨a,hh⟩
  simp [scatter,h]

theorem transform_scatter {A B : Type*} [Fintype A] [Fintype B]
    [AddCommGroup B] [DecidableEq B] (pos : A → B) (f : A → ℂ)
    (χ : AddChar B ℂ) :
    transform χ (scatter pos f) = ∑ a, χ (-pos a)*f a := by
  unfold transform scatter
  simp_rw [mul_sum]
  rw [sum_comm]
  apply sum_congr rfl
  intro a _
  simp only [mul_ite, mul_zero]
  simp

variable {M N r : ℕ} [NeZero M] [NeZero N] [NeZero r]

noncomputable def insertCoordinate (r : ℕ) (x : ZMod M) : ZMod (r*M) :=
  (r*x.val : ℕ)

theorem insert_coordinate_injective :
    Function.Injective (insertCoordinate (M:=M) r) := by
  intro x y h
  have hv := congrArg ZMod.val h
  have hx : r*x.val < r*M := Nat.mul_lt_mul_of_pos_left x.val_lt (NeZero.pos r)
  have hy : r*y.val < r*M := Nat.mul_lt_mul_of_pos_left y.val_lt (NeZero.pos r)
  simp only [insertCoordinate, ZMod.val_natCast_of_lt hx, ZMod.val_natCast_of_lt hy] at hv
  exact ZMod.val_injective M (Nat.eq_of_mul_eq_mul_left (NeZero.pos r) hv)

theorem inserted_character (u : ZMod (r*M)) (x : ZMod M) :
    ZMod.stdAddChar (u*insertCoordinate r x) =
      ZMod.stdAddChar ((u.val : ZMod M)*x) := by
  nth_rw 1 [← ZMod.natCast_zmod_val u]
  conv_rhs => rw [← ZMod.natCast_zmod_val x]
  simp only [insertCoordinate, ← Nat.cast_mul]
  have hn (q n : ℕ) [NeZero n] : ZMod.stdAddChar (q : ZMod n) =
      Complex.exp (2*Real.pi*Complex.I*q/n) := by
    simpa only [Int.cast_natCast] using ZMod.stdAddChar_coe (N:=n) (q : ℤ)
  rw [hn,hn]
  congr 1
  push_cast
  have hr : (r : ℂ) ≠ 0 := Nat.cast_ne_zero.mpr (NeZero.ne r)
  have hm : (M : ℂ) ≠ 0 := Nat.cast_ne_zero.mpr (NeZero.ne M)
  field_simp

noncomputable def insertGrid (r : ℕ) (x : Grid M N) : Grid (r*M) (r*N) :=
  (insertCoordinate r x.1,insertCoordinate r x.2)

theorem insert_grid_injective : Function.Injective (insertGrid (M:=M) (N:=N) r) := by
  intro x y h
  apply Prod.ext
  · exact insert_coordinate_injective (congrArg Prod.fst h)
  · exact insert_coordinate_injective (congrArg Prod.snd h)

noncomputable def zeroInsert (f : Grid M N → ℂ) : Grid (r*M) (r*N) → ℂ :=
  scatter (insertGrid r) f

theorem zero_insert_original (f : Grid M N → ℂ) (x : Grid M N) :
    zeroInsert (r:=r) f (insertGrid r x) = f x := by
  classical
  simp only [zeroInsert, scatter, (insert_grid_injective (r:=r)).eq_iff]
  simp

theorem zero_insert_elsewhere (f : Grid M N → ℂ) (x : Grid (r*M) (r*N))
    (hx : x ∉ Set.range (insertGrid (M:=M) (N:=N) r)) : zeroInsert (r:=r) f x = 0 := by
  classical
  have h (a : Grid M N) : insertGrid r a ≠ x := fun hh => hx ⟨a,hh⟩
  simp [zeroInsert,scatter,h]

theorem zero_insert_dft_repeats (f : Grid M N → ℂ)
    (u : ZMod (r*M)) (v : ZMod (r*N)) :
    dft2 (zeroInsert (r:=r) f) u v = dft2 f (u.val : ZMod M) (v.val : ZMod N) := by
  rw [dft2,zeroInsert,transform_scatter]
  unfold dft2 transform
  apply sum_congr rfl
  intro x _
  simp only [grid_character_apply, Prod.fst_neg, Prod.snd_neg, insertGrid,
    mul_neg, map_neg_eq_inv]
  rw [inserted_character,inserted_character]

noncomputable def frequencyBlock (u : ZMod M) (j : Fin r) : ZMod (r*M) :=
  (u.val+j.val*M : ℕ)

theorem frequency_block_remainder (u : ZMod M) (j : Fin r) :
    ((frequencyBlock u j).val : ZMod M) = u := by
  have hh : u.val+j.val*M < r*M := by
    calc
      _ < M+j.val*M := Nat.add_lt_add_right u.val_lt _
      _ = (j.val+1)*M := by ring
      _ ≤ r*M := Nat.mul_le_mul_right M (Nat.succ_le_of_lt j.isLt)
  change (((u.val+j.val*M : ℕ) : ZMod (r*M)).val : ZMod M) = u
  rw [ZMod.val_natCast_of_lt hh]
  simp only [Nat.cast_add,Nat.cast_mul,
    ZMod.natCast_zmod_val,ZMod.natCast_self,mul_zero,add_zero]

theorem actual_zero_insert_frequency_blocks (f : Grid M N → ℂ)
    (u : ZMod M) (v : ZMod N) (s t : Fin r) :
    dft2 (zeroInsert (r:=r) f) (frequencyBlock u s) (frequencyBlock v t) = dft2 f u v := by
  rw [zero_insert_dft_repeats,frequency_block_remainder,frequency_block_remainder]

end Harsanyi.Frequency
