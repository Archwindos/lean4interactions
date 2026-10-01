import Harsanyi.Extensions.TaylorMoments
import Harsanyi.Extensions.NoisyRegression

set_option maxHeartbeats 1000000
namespace Harsanyi.GaussianRegression
open Finset MeasureTheory ProbabilityTheory Matrix
open scoped ProbabilityTheory
variable {Ω ι : Type*} [MeasurableSpace Ω] [Fintype ι] [DecidableEq ι]
variable (μ : Measure Ω) [IsProbabilityMeasure μ]

theorem gaussian_memLp (X : Ω → ℝ) (q : NNReal) (hm : Measurable X)
    (hlaw : μ.map X = gaussianReal 0 q) : MemLp X 2 μ := by
  have h : MemLp id 2 (μ.map X) := by
    rw [hlaw]
    exact memLp_id_gaussianReal' 2 (by norm_num)
  simpa only [Function.comp_def, id_eq] using h.comp_measurePreserving ⟨hm, hlaw ▸ rfl⟩

theorem gaussian_mean (X : Ω → ℝ) (q : NNReal) (hm : Measurable X)
    (hlaw : μ.map X = gaussianReal 0 q) : (∫ ω, X ω ∂μ) = 0 := by
  calc
    (∫ ω, X ω ∂μ) = ∫ z, z ∂μ.map X := by
      symm
      simpa only [id_eq] using integral_map hm.aemeasurable
        (aestronglyMeasurable_id : AEStronglyMeasurable (id : ℝ → ℝ) (μ.map X))
    _ = 0 := by rw [hlaw]; exact integral_id_gaussianReal

/-- Exact expected residual under the source centered independent finite-variance model. -/
theorem independent_residual (ε : ι → Ω → ℝ) (q : ι → ℝ)
    (hp : ∀ i, MemLp (ε i) 2 μ)
    (hmean : ∀ i, ∫ ω, ε i ω ∂μ = 0)
    (hvar : ∀ i, variance (ε i) μ = q i)
    (hi : iIndepFun ε μ) (w : ι → ℝ) (r : ℝ) :
    (∫ ω, (r + ∑ i, w i * ε i ω) ^ 2 ∂μ) = r ^ 2 + ∑ i, w i ^ 2 * q i := by
  have hp' : ∀ i, MemLp (fun ω => w i * ε i ω) 2 μ := by
    intro i
    simpa only [smul_eq_mul] using (hp i).const_smul (w i)
  have hi' : Set.Pairwise (↑(univ : Finset ι) : Set ι) fun i j =>
      IndepFun (fun ω => w i * ε i ω) (fun ω => w j * ε j ω) μ := by
    intro i _ j _ hij
    simpa only [Function.comp_def] using
      (hi.indepFun hij).comp (measurable_const.mul measurable_id) (measurable_const.mul measurable_id)
  have hpS : MemLp (fun ω => ∑ i, w i * ε i ω) 2 μ := by
    have ht : (∑ i, fun ω => w i * ε i ω) = (fun ω => ∑ i, w i * ε i ω) := by funext ω; simp
    rw [← ht]
    exact memLp_finset_sum' _ (fun i _ => hp' i)
  have he : (∫ ω, (∑ i, w i * ε i ω) ∂μ) = 0 := by
    rw [integral_finset_sum _ (fun i _ => (hp' i).integrable (by norm_num))]
    simp_rw [integral_const_mul, hmean]
    simp
  have hv : variance (fun ω => ∑ i, w i * ε i ω) μ = ∑ i, w i ^ 2 * q i := by
    have ht : (fun ω => ∑ i, w i * ε i ω) = (∑ i, fun ω => w i * ε i ω) := by funext ω; simp
    rw [ht, IndepFun.variance_sum (fun i _ => hp' i) hi']
    apply sum_congr rfl
    intro i _
    rw [variance_mul, hvar i]
  have hpR : MemLp (fun ω => r + ∑ i, w i * ε i ω) 2 μ :=
    (memLp_const (p := 2) (μ := μ) r).add hpS
  have hmR : (∫ ω, (r + ∑ i, w i * ε i ω) ∂μ) = r := by
    rw [integral_add (integrable_const r) (hpS.integrable (by norm_num))]
    simp [he]
  have hvR : variance (fun ω => r + ∑ i, w i * ε i ω) μ = ∑ i, w i ^ 2 * q i := by
    rw [variance_const_add hpS.aestronglyMeasurable, hv]
  rw [variance_eq_sub hpR] at hvR
  simp only [Pi.pow_apply] at hvR
  rw [hmR] at hvR
  linarith

/-- Gaussian laws discharge all finite-moment and centering hypotheses. -/
theorem gaussian_residual (ε : ι → Ω → ℝ) (q : ι → NNReal)
    (hm : ∀ i, Measurable (ε i)) (hlaw : ∀ i, μ.map (ε i) = gaussianReal 0 (q i))
    (hi : iIndepFun ε μ) (w : ι → ℝ) (r : ℝ) :
    (∫ ω, (r + ∑ i, w i * ε i ω) ^ 2 ∂μ) = r ^ 2 + ∑ i, w i ^ 2 * q i := by
  apply independent_residual μ ε (fun i => (q i : ℝ))
    (fun i => gaussian_memLp μ _ _ (hm i) (hlaw i))
    (fun i => gaussian_mean μ _ _ (hm i) (hlaw i)) _ hi w r
  intro i
  rw [← variance_id_map (hm i).aemeasurable, hlaw i, variance_id_gaussianReal]

end Harsanyi.GaussianRegression
