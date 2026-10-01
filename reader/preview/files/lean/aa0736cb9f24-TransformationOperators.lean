import Harsanyi.Extensions.TransformationAffine
import Mathlib.Data.Finset.Max

/-! Actual fixed dropout and finite max-pool operators. A max-pool gate selects
one maximizing input per nonempty window, including ties. The pool output is
not assumed linear; equality to the fixed selection action is proved. -/
namespace Harsanyi.GatedAffine
open Finset

noncomputable def dropoutLinear {D : Type*} (keep : D → Bool) :
    (D → ℝ) →ₗ[ℝ] (D → ℝ) where
  toFun h d := if keep d then h d else 0
  map_add' := by
    intro x y
    funext d
    cases hk : keep d <;> simp [hk]
  map_smul' := by
    intro c x
    funext d
    cases hk : keep d <;> simp [hk]

def selectedPoolLinear {D P : Type*} (select : P → D) :
    (D → ℝ) →ₗ[ℝ] (P → ℝ) where
  toFun h p := h (select p)
  map_add' := by intro x y; rfl
  map_smul' := by intro c x; rfl

noncomputable def finiteMaxPool {D P : Type*} (window : P → Finset D)
    (hne : ∀ p, (window p).Nonempty) (h : D → ℝ) : P → ℝ :=
  fun p => (window p).sup' (hne p) h

noncomputable def maximizingSelector {D P : Type*} (window : P → Finset D)
    (hne : ∀ p, (window p).Nonempty) (h : D → ℝ) : P → D :=
  fun p => Classical.choose ((window p).exists_mem_eq_sup' (hne p) h)

theorem maximizingSelector_spec {D P : Type*} (window : P → Finset D)
    (hne : ∀ p, (window p).Nonempty) (h : D → ℝ) (p : P) :
    maximizingSelector window hne h p ∈ window p ∧
      finiteMaxPool window hne h p = h (maximizingSelector window hne h p) :=
  Classical.choose_spec ((window p).exists_mem_eq_sup' (hne p) h)

theorem finite_max_pool_selected {D P : Type*} (window : P → Finset D)
    (hne : ∀ p, (window p).Nonempty) (h : D → ℝ) :
    finiteMaxPool window hne h = selectedPoolLinear (maximizingSelector window hne h) h := by
  funext p
  exact (maximizingSelector_spec window hne h p).2

theorem fixed_maximizer_pool {D P : Type*} (window : P → Finset D)
    (hne : ∀ p, (window p).Nonempty) (select : P → D) (h : D → ℝ)
    (hsel : ∀ p, select p ∈ window p)
    (hmax : ∀ p d, d ∈ window p → h d ≤ h (select p)) :
    finiteMaxPool window hne h = selectedPoolLinear select h := by
  funext p
  apply le_antisymm
  · exact Finset.sup'_le (hne p) h (hmax p)
  · exact Finset.le_sup' h (hsel p)

variable {E D P : Type*} [AddCommGroup E] [Module ℝ E]

theorem fixed_dropout_layer_affine (W : E →ₗ[ℝ] (D → ℝ))
    (b : D → ℝ) (keep : D → Bool) (x : E) :
    dropoutLinear keep (W x + b) =
      (layer ((dropoutLinear keep).comp W) (dropoutLinear keep b)) x := by
  simp [layer]

theorem fixed_pool_layer_affine (W : E →ₗ[ℝ] (D → ℝ)) (b : D → ℝ)
    (window : P → Finset D) (hne : ∀ p, (window p).Nonempty) (select : P → D)
    (x : E) (hsel : ∀ p, select p ∈ window p)
    (hmax : ∀ p d, d ∈ window p → (W x+b) d ≤ (W x+b) (select p)) :
    finiteMaxPool window hne (W x+b) =
      (layer ((selectedPoolLinear select).comp W) (selectedPoolLinear select b)) x := by
  rw [fixed_maximizer_pool window hne select (W x+b) hsel hmax]
  simp [layer]

end Harsanyi.GatedAffine
