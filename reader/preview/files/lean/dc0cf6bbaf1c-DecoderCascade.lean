import Harsanyi.Extensions.DecoderGrid

namespace Harsanyi.Frequency
open Finset
open scoped BigOperators
variable {M N : ℕ} [NeZero M] [NeZero N]
variable (C : ℕ → Type*) [∀ n, Fintype (C n)]

noncomputable def gridNetwork {I : Type*} [Fintype I]
    (shift : I → Grid M N) (w : ∀ n, C (n+1) → C n → I → ℂ)
    (b : ∀ n, C (n+1) → ℂ) (f : C 0 → Grid M N → ℂ) :
    ∀ n, C n → Grid M N → ℂ
  | 0 => f
  | n+1 => offsetLayer shift (w n) (gridNetwork shift w b f n) (b n)

noncomputable def spectrumLinear {I : Type*} [Fintype I]
    (shift : I → Grid M N) (w : C (n+1) → C n → I → ℂ)
    (u : ZMod M) (v : ZMod N) : (C n → ℂ) →ₗ[ℂ] (C (n+1) → ℂ) where
  toFun := fun z d => ∑ c, offsetResponse shift (w d c) u v * z c
  map_add' := by intro x y; funext d; simp [mul_add, sum_add_distrib]
  map_smul' := by intro a z; funext d; simp [mul_left_comm, mul_comm, mul_assoc, mul_sum]

noncomputable def cascadeLinear (T : ∀ n, (C n → ℂ) →ₗ[ℂ] (C (n+1) → ℂ)) :
    ∀ L, (C 0 → ℂ) →ₗ[ℂ] (C L → ℂ)
  | 0 => LinearMap.id
  | L+1 => (T L).comp (cascadeLinear T L)

noncomputable def cascadeBias (T : ∀ n, (C n → ℂ) →ₗ[ℂ] (C (n+1) → ℂ))
    (b : ∀ n, C (n+1) → ℂ) : ∀ L, C L → ℂ
  | 0 => 0
  | L+1 => T L (cascadeBias T b L) + b L

noncomputable def biasTerm (T : ∀ n, (C n → ℂ) →ₗ[ℂ] (C (n+1) → ℂ))
    (b : ∀ n, C (n+1) → ℂ) : ∀ L, ℕ → C L → ℂ
  | 0, _ => 0
  | L+1, j => if j=L then b L else T L (biasTerm T b L j)

theorem cascade_bias_sum (T : ∀ n, (C n → ℂ) →ₗ[ℂ] (C (n+1) → ℂ))
    (b : ∀ n, C (n+1) → ℂ) (L : ℕ) :
    cascadeBias C T b L = ∑ j ∈ range L, biasTerm C T b L j := by
  induction L with
  | zero => simp [cascadeBias]
  | succ L ih =>
    rw [sum_range_succ, cascadeBias, ih, map_sum]
    have hsum : (∑ j ∈ range L, biasTerm C T b (L+1) j) =
        ∑ j ∈ range L, T L (biasTerm C T b L j) := by
      apply sum_congr rfl
      intro j hj
      simp [biasTerm, ne_of_lt (mem_range.mp hj)]
    rw [hsum]
    simp [biasTerm]

theorem actual_grid_cascade {I : Type*} [Fintype I]
    (shift : I → Grid M N) (w : ∀ n, C (n+1) → C n → I → ℂ)
    (b : ∀ n, C (n+1) → ℂ) (f : C 0 → Grid M N → ℂ)
    (u : ZMod M) (v : ZMod N) (L : ℕ) :
    (fun d => dft2 (gridNetwork C shift w b f L d) u v) =
      cascadeLinear C (fun n => spectrumLinear C shift (w n) u v) L
        (fun c => dft2 (f c) u v) +
      (if u=0 ∧ v=0 then ((M*N : ℕ) : ℂ) else 0) •
        cascadeBias C (fun n => spectrumLinear C shift (w n) u v) b L := by
  induction L with
  | zero => simp [gridNetwork, cascadeLinear, cascadeBias]
  | succ L ih =>
    have hs := congrArg (spectrumLinear C shift (w L) u v) ih
    funext d
    rw [gridNetwork, offset_layer_dft]
    change spectrumLinear C shift (w L) u v
      (fun c => dft2 (gridNetwork C shift w b f L c) u v) d + _ = _
    rw [ih, map_add, map_smul]
    simp only [cascadeLinear, LinearMap.comp_apply, cascadeBias, Pi.add_apply,
      Pi.smul_apply, smul_eq_mul, mul_add]
    split_ifs <;> simp <;> ring

end Harsanyi.Frequency
