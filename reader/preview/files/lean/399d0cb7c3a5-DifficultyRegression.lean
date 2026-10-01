import Harsanyi.Extensions.ConceptGaussian

namespace Harsanyi.DifficultyRegression
open Matrix
open scoped BigOperators

/-- Source Eq.(27) is Cramer's formula for the already established unique optimizer. -/
theorem feature_opt_cramer {ι : Type*} [Fintype ι] [DecidableEq ι]
    (a d : ι → ℝ) (y : ℝ) (hd : ∀ i, 0 < d i) (i : ι) :
    0 < (ConceptGaussian.featureMatrix a d).det ∧
    ConceptGaussian.featureOpt a d y i =
      ((ConceptGaussian.featureMatrix a d).updateCol i (fun j => y*a j)).det /
        (ConceptGaussian.featureMatrix a d).det := by
  let K := ConceptGaussian.featureMatrix a d
  have hK : K.PosDef := ConceptGaussian.featureMatrix_posDef a d hd
  have hp : 0 < K.det := hK.det_pos
  refine ⟨hp, ?_⟩
  have hc : K.det • ConceptGaussian.featureOpt a d y = Matrix.cramer K (fun j => y*a j) := by
    apply (Matrix.mulVec_injective_iff_isUnit.mpr hK.isUnit)
    rw [Matrix.mulVec_smul, ConceptGaussian.featureOpt_normal a d y hd, Matrix.mulVec_cramer]
  have he := congrFun hc i
  simp only [Pi.smul_apply, smul_eq_mul, Matrix.cramer_apply] at he
  apply (eq_div_iff hp.ne').mpr
  simpa only [mul_comm] using he

/-- The author's one-half loss has exactly the same strict comparisons and hence argmin. -/
theorem half_loss_strict_iff (a b : ℝ) : (1/2 : ℝ)*a < (1/2 : ℝ)*b ↔ a < b := by
  constructor <;> intro h <;> linarith
end Harsanyi.DifficultyRegression
