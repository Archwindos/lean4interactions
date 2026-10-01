import Mathlib.LinearAlgebra.AffineSpace.AffineMap
import Mathlib.Data.Matrix.Basic
import Mathlib.Tactic

namespace Harsanyi.GatedAffine
variable {E F H : Type*} [AddCommGroup E] [Module ℝ E]
    [AddCommGroup F] [Module ℝ F] [AddCommGroup H] [Module ℝ H]

def layer (W : E →ₗ[ℝ] F) (b : F) : E →ᵃ[ℝ] F where
  toFun := fun x => W x + b
  linear := W
  map_vadd' := by intro p v; simp [map_add, add_assoc, add_comm, add_left_comm]

theorem layer_apply (W : E →ₗ[ℝ] F) (b : F) (x : E) : layer W b x = W x + b := rfl

theorem layer_comp (U : F →ₗ[ℝ] H) (c : H) (W : E →ₗ[ℝ] F) (b : F) :
    (layer U c).comp (layer W b) = layer (U.comp W) (U b + c) := by
  ext x
  simp [layer, map_add, add_assoc]

variable (dim : ℕ → ℕ)
abbrev Space (n : ℕ) := Fin (dim n) → ℝ

noncomputable def networkAffine (W : ∀ n, Space dim n →ₗ[ℝ] Space dim (n+1))
    (b : ∀ n, Space dim (n+1)) : ∀ n, Space dim 0 →ᵃ[ℝ] Space dim n
  | 0 => AffineMap.id ℝ (Space dim 0)
  | n+1 => (layer (W n) (b n)).comp (networkAffine W b n)

noncomputable def networkOutput (W : ∀ n, Space dim n →ₗ[ℝ] Space dim (n+1))
    (b : ∀ n, Space dim (n+1)) (x : Space dim 0) : ∀ n, Space dim n
  | 0 => x
  | n+1 => W n (networkOutput W b x n) + b n

/-- The actual finite chain with arbitrary layer widths is affine once every
gate's selection matrix is fixed and absorbed into the corresponding W. -/
theorem network_output_affine (W : ∀ n, Space dim n →ₗ[ℝ] Space dim (n+1))
    (b : ∀ n, Space dim (n+1)) (x : Space dim 0) (n : ℕ) :
    networkOutput dim W b x n = networkAffine dim W b n x := by
  induction n with
  | zero => rfl
  | succ n ih => simp [networkOutput, networkAffine, ih, layer]

theorem network_output_linear_bias (W : ∀ n, Space dim n →ₗ[ℝ] Space dim (n+1))
    (b : ∀ n, Space dim (n+1)) (x : Space dim 0) (n : ℕ) :
    networkOutput dim W b x n = (networkAffine dim W b n).linear x +
      networkOutput dim W b 0 n := by
  simp_rw [network_output_affine]
  simpa using congrFun (AffineMap.decomp (networkAffine dim W b n)) x

end Harsanyi.GatedAffine
