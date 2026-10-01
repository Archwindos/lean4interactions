import Harsanyi.Core.Properties
import Mathlib.LinearAlgebra.Matrix.PosDef
import Mathlib.LinearAlgebra.Matrix.NonsingularInverse
import Mathlib.Analysis.InnerProductSpace.StarOrder
import Mathlib.Data.Real.StarOrdered
import Mathlib.Logic.Equiv.Set
import Mathlib.Data.Fintype.EquivFin

namespace Harsanyi.NoisyRegression
open Finset Matrix
variable {α : Type*} [Fintype α] [DecidableEq α]

noncomputable def zeta : Matrix (Finset α) (Finset α) ℝ :=
  fun S T => if T ⊆ S then 1 else 0

/-- The design matrix is exactly the Boolean subset-sum operator, including the empty column. -/
theorem zeta_mulVec (w : Finset α → ℝ) (S : Finset α) :
    (zeta *ᵥ w) S = Harsanyi.reconstruct w S := by
  classical
  change (∑ T, (if T ⊆ S then (1 : ℝ) else 0) * w T) = ∑ T ∈ S.powerset, w T
  simp_rw [ite_mul, one_mul, zero_mul]
  rw [← Finset.sum_filter]
  congr 1
  ext T
  simp

/-- Boolean Möbius inversion proves injectivity for every finite universe. -/
theorem zeta_injective : Function.Injective (zeta (α := α)).mulVec := by
  intro u v huv
  funext S
  have h : Harsanyi.reconstruct u = Harsanyi.reconstruct v := by
    funext T
    simpa only [zeta_mulVec] using congrFun huv T
  have hh := congrArg (fun g => Harsanyi.interaction g S) h
  simpa only [Harsanyi.interaction_reconstruct] using hh

/-- Correct Gram positive-definiteness proof, valid even when noise is zero. -/
theorem gram_posDef : ((zeta (α := α))ᵀ * zeta).PosDef := by
  simpa using Matrix.PosDef.conjTranspose_mul_self zeta zeta_injective

noncomputable def normalMatrix (c : Finset α → ℝ) : Matrix (Finset α) (Finset α) ℝ :=
  zetaᵀ * zeta + diagonal c

theorem normal_posDef (c : Finset α → ℝ) (hc : ∀ T, 0 ≤ c T) :
    (normalMatrix c).PosDef := by
  change (zetaᵀ * zeta + diagonal c).PosDef
  apply gram_posDef.add_posSemidef
  exact Matrix.posSemidef_diagonal_iff.mpr hc

theorem normal_isUnit (c : Finset α → ℝ) (hc : ∀ T, 0 ≤ c T) :
    IsUnit (normalMatrix c) := (normal_posDef c hc).isUnit

/-- Exact unique solution of the noisy normal equations. -/
theorem normal_solution (c : Finset α → ℝ) (hc : ∀ T, 0 ≤ c T)
    (y w : Finset α → ℝ) :
    normalMatrix c *ᵥ w = zetaᵀ *ᵥ y ↔
      w = (normalMatrix c)⁻¹ *ᵥ (zetaᵀ *ᵥ y) := by
  have hu := normal_isUnit c hc
  constructor
  · intro h
    have h' := congrArg (fun z => (normalMatrix c)⁻¹ *ᵥ z) h
    simpa only [mulVec_mulVec, Matrix.nonsing_inv_mul _ (((normalMatrix c).isUnit_iff_isUnit_det.mp hu)), one_mulVec] using h'
  · intro h
    rw [h, mulVec_mulVec, Matrix.mul_nonsing_inv _ (((normalMatrix c).isUnit_iff_isUnit_det.mp hu)), one_mulVec]

/-- At zero noise every original coefficient is recovered, with arbitrary empty baseline. -/
theorem zero_noise (w : Finset α → ℝ) :
    (normalMatrix (fun _ => 0))⁻¹ *ᵥ (zetaᵀ *ᵥ (zeta *ᵥ w)) = w := by
  symm
  apply (normal_solution (fun _ => 0) (fun _ => le_rfl) (zeta *ᵥ w) w).mp
  simp [normalMatrix, mulVec_mulVec]

section Quadratic
variable {ι : Type*} [Fintype ι] [DecidableEq ι]
noncomputable def quadraticLoss (A : Matrix ι ι ℝ) (h : ι → ℝ) (w : ι → ℝ) : ℝ :=
  w ⬝ᵥ (A *ᵥ w) - 2 * (h ⬝ᵥ w)

theorem symmetric_dot (A : Matrix ι ι ℝ) (hs : Aᵀ = A) (u v : ι → ℝ) :
    u ⬝ᵥ (A *ᵥ v) = v ⬝ᵥ (A *ᵥ u) := by
  rw [dotProduct_mulVec, dotProduct_comm, ← vecMul_transpose A, hs]

/-- Completing the square proves global minimality rather than merely stationarity. -/
theorem quadratic_difference (A : Matrix ι ι ℝ) (hs : Aᵀ = A)
    (h w u : ι → ℝ) (hu : A *ᵥ u = h) :
    quadraticLoss A h w - quadraticLoss A h u =
      (w - u) ⬝ᵥ (A *ᵥ (w - u)) := by
  unfold quadraticLoss
  rw [← hu]
  simp only [mulVec_sub, sub_dotProduct, dotProduct_sub]
  rw [symmetric_dot A hs w u]
  rw [dotProduct_comm (A *ᵥ u) w, dotProduct_comm (A *ᵥ u) u]
  nlinarith [symmetric_dot A hs u w]

theorem quadratic_unique_min (A : Matrix ι ι ℝ) (hA : A.PosDef)
    (h u : ι → ℝ) (hu : A *ᵥ u = h) :
    ∀ w, w ≠ u → quadraticLoss A h u < quadraticLoss A h w := by
  intro w hwu
  have hs : Aᵀ = A := by simpa using hA.isHermitian
  have hdiff := quadratic_difference A hs h w u hu
  have hp : 0 < (w - u) ⬝ᵥ (A *ᵥ (w - u)) := by
    simpa only [star_trivial] using hA.2 (w - u) (sub_ne_zero.mpr hwu)
  linarith
end Quadratic

/-- The explicit inverse formula is the unique global minimizer of the finite noisy quadratic. -/
theorem normal_unique_min (c : Finset α → ℝ) (hc : ∀ T, 0 ≤ c T)
    (y : Finset α → ℝ) :
    ∀ w, w ≠ (normalMatrix c)⁻¹ *ᵥ (zetaᵀ *ᵥ y) →
      quadraticLoss (normalMatrix c) (zetaᵀ *ᵥ y)
        ((normalMatrix c)⁻¹ *ᵥ (zetaᵀ *ᵥ y)) <
      quadraticLoss (normalMatrix c) (zetaᵀ *ᵥ y) w := by
  apply quadratic_unique_min _ (normal_posDef c hc)
  exact (normal_solution c hc y _).mpr rfl

/-- Exact residual objective; a constant and positive scale do not affect its minimizer. -/
noncomputable def residualLoss (c : Finset α → ℝ) (y w : Finset α → ℝ) : ℝ :=
  (y - zeta *ᵥ w) ⬝ᵥ (y - zeta *ᵥ w) + ∑ T, c T * w T ^ 2

theorem residualLoss_expansion (c : Finset α → ℝ) (y w : Finset α → ℝ) :
    residualLoss c y w = y ⬝ᵥ y +
      quadraticLoss (normalMatrix c) (zetaᵀ *ᵥ y) w := by
  unfold residualLoss quadraticLoss normalMatrix
  simp only [add_mulVec, dotProduct_add, ← mulVec_mulVec]
  have hb : w ⬝ᵥ (zetaᵀ *ᵥ (zeta *ᵥ w)) = (zeta *ᵥ w) ⬝ᵥ (zeta *ᵥ w) := by
    rw [dotProduct_mulVec, vecMul_transpose]
  have hc : (zetaᵀ *ᵥ y) ⬝ᵥ w = y ⬝ᵥ (zeta *ᵥ w) := by
    rw [dotProduct_comm, dotProduct_mulVec, vecMul_transpose, dotProduct_comm]
  have hd : w ⬝ᵥ (diagonal c *ᵥ w) = ∑ T, c T * w T ^ 2 := by
    simp only [dotProduct, mulVec_diagonal, pow_two]
    apply sum_congr rfl
    intro T _
    ring
  rw [hb, hc, hd]
  simp only [sub_dotProduct, dotProduct_sub]
  rw [dotProduct_comm (zeta *ᵥ w) y]
  ring

theorem residual_unique_min (c : Finset α → ℝ) (hc : ∀ T, 0 ≤ c T)
    (y : Finset α → ℝ) :
    ∀ w, w ≠ (normalMatrix c)⁻¹ *ᵥ (zetaᵀ *ᵥ y) →
      residualLoss c y ((normalMatrix c)⁻¹ *ᵥ (zetaᵀ *ᵥ y)) < residualLoss c y w := by
  intro w hw
  simpa only [residualLoss_expansion, add_lt_add_iff_left] using normal_unique_min c hc y w hw

/-- A positive diagonal independent-feature model has one common shrinkage multiplier. -/
noncomputable def featureLoss {ι : Type*} [Fintype ι] (a d : ι → ℝ) (y : ℝ) (w : ι → ℝ) : ℝ :=
  (y - ∑ i, a i * w i) ^ 2 + ∑ i, d i * w i ^ 2

/-- Derive coefficient scaling from the normal equations, without Cramer's ratio division. -/
theorem feature_normal_scaling {ι : Type*} [Fintype ι]
    (a d w : ι → ℝ) (y : ℝ) (hd : ∀ i, d i ≠ 0)
    (hn : ∀ i, d i * w i = a i * (y - ∑ j, a j * w j)) :
    ∀ i, w i = (y - ∑ j, a j * w j) * (a i / d i) := by
  intro i
  rw [← mul_div_assoc]
  apply (eq_div_iff (hd i)).2
  nlinarith [hn i]

noncomputable def transferMatrix (c : Finset α → ℝ) : Matrix (Finset α) (Finset α) ℝ :=
  (normalMatrix c)⁻¹ * (zetaᵀ * zeta)

/-- Variable permutation preserves the exact subset-design matrix. -/
theorem zeta_permutation (e : α ≃ α) :
    (zeta (α := α)).submatrix e.finsetCongr e.finsetCongr = zeta := by
  ext S T
  simp [zeta, Equiv.finsetCongr_apply, Finset.map_subset_map]

/-- Conjugation invariance of the actual regularized transfer matrix. -/
theorem transfer_permutation (e : α ≃ α) (c : Finset α → ℝ)
    (hc : ∀ S, c (e.finsetCongr S) = c S) :
    (transferMatrix c).submatrix e.finsetCongr e.finsetCongr = transferMatrix c := by
  have hb : ((zeta (α := α))ᵀ * zeta).submatrix e.finsetCongr e.finsetCongr = zetaᵀ * zeta := by
    rw [← Matrix.submatrix_mul_equiv (zeta (α := α))ᵀ zeta e.finsetCongr e.finsetCongr e.finsetCongr]
    rw [← Matrix.transpose_submatrix, zeta_permutation]
  have hd : (diagonal c).submatrix e.finsetCongr e.finsetCongr = diagonal c := by
    ext S T
    change (if e.finsetCongr S = e.finsetCongr T then c (e.finsetCongr S) else 0) = _
    simp only [e.finsetCongr.injective.eq_iff, hc, diagonal]
    rfl
  have ha : (normalMatrix c).submatrix e.finsetCongr e.finsetCongr = normalMatrix c := by
    change ((zeta (α := α))ᵀ * zeta + diagonal c).submatrix e.finsetCongr e.finsetCongr = _
    change ((zeta (α := α))ᵀ * zeta).submatrix e.finsetCongr e.finsetCongr + (diagonal c).submatrix e.finsetCongr e.finsetCongr = _
    rw [hb, hd]
    rfl
  unfold transferMatrix
  rw [← Matrix.submatrix_mul_equiv (normalMatrix c)⁻¹ ((zeta (α := α))ᵀ * zeta) e.finsetCongr e.finsetCongr e.finsetCongr]
  rw [← Matrix.inv_submatrix_equiv (normalMatrix c) e.finsetCongr e.finsetCongr, ha, hb]

/-- Squared Euclidean row norms are invariant under any variable permutation. -/
theorem row_norm_permutation (e : α ≃ α) (c : Finset α → ℝ)
    (hc : ∀ S, c (e.finsetCongr S) = c S) (T : Finset α) :
    (∑ U, transferMatrix c (e.finsetCongr T) U ^ 2) =
      ∑ U, transferMatrix c T U ^ 2 := by
  have hp := transfer_permutation e c hc
  calc
    (∑ U, transferMatrix c (e.finsetCongr T) U ^ 2) =
        ∑ U, transferMatrix c (e.finsetCongr T) (e.finsetCongr U) ^ 2 :=
      (Equiv.sum_comp e.finsetCongr _).symm
    _ = ∑ U, transferMatrix c T U ^ 2 := by
      apply sum_congr rfl
      intro U _
      exact congrArg (fun z : ℝ => z ^ 2) (congrFun (congrFun hp T) U)

/-- Construct a permutation of the entire universe from equal-cardinality coalitions. -/
theorem exists_coalition_permutation (T U : Finset α) (hcard : T.card = U.card) :
    ∃ e : α ≃ α, e.finsetCongr T = U := by
  classical
  let e0 : (↑T : Set α) ≃ (↑U : Set α) := Finset.equivOfCardEq hcard
  have hcomp : Fintype.card ↥((↑T : Set α)ᶜ) = Fintype.card ↥((↑U : Set α)ᶜ) := by
    rw [Fintype.card_compl_set, Fintype.card_compl_set]
    simpa using congrArg (fun k => Fintype.card α - k) hcard
  let e1 := Fintype.equivOfCardEq hcomp
  let ext := (Equiv.Set.compl e0).symm e1
  refine ⟨ext.val, ?_⟩
  apply Finset.eq_of_subset_of_card_le
  · intro x hx
    obtain ⟨t, ht, rfl⟩ := Finset.mem_map.mp hx
    have h := ext.property ⟨t, ht⟩
    change ext.val t ∈ U
    rw [h]
    exact (e0 ⟨t, ht⟩).property
  · simp [Equiv.finsetCongr_apply, hcard]

/-- Theorem 4 for every finite universe and all nonnegative or zero noise levels. -/
theorem equal_order_row_norm (σ2 : ℝ) (T U : Finset α) (hcard : T.card = U.card) :
    (∑ V, transferMatrix (fun A => (2 : ℝ) ^ A.card * σ2) T V ^ 2) =
      ∑ V, transferMatrix (fun A => (2 : ℝ) ^ A.card * σ2) U V ^ 2 := by
  obtain ⟨e, he⟩ := exists_coalition_permutation T U hcard
  have h := row_norm_permutation e (fun A => (2 : ℝ) ^ A.card * σ2)
    (fun A => by simp [Equiv.finsetCongr_apply]) T
  rw [he] at h
  exact h.symm

theorem transfer_zero : transferMatrix (α := α) (fun _ => 0) = 1 := by
  have hu := (normalMatrix (α := α) (fun _ => 0)).isUnit_iff_isUnit_det.mp
    (normal_isUnit (fun _ => 0) (fun _ => le_rfl))
  have hz : normalMatrix (α := α) (fun _ => 0) = zetaᵀ * zeta := by
    simp [normalMatrix]
  unfold transferMatrix
  rw [← hz]
  exact Matrix.nonsing_inv_mul _ hu

/-- Printed determinant justification already fails for the one-variable zeta Gram. -/
theorem diagonal_product_counterexample :
    Matrix.det (!![(2 : ℝ), 1; 1, 1]) ≠ (2 : ℝ) * 1 := by
  norm_num [Matrix.det_fin_two]

end Harsanyi.NoisyRegression
