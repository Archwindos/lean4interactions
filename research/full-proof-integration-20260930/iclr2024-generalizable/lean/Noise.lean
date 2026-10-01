import Harsanyi.Core.Properties
import Mathlib.Probability.Distributions.Gaussian.Real

/-! Genuine random-variable variances, not only a sum of squared signs. -/
namespace Harsanyi
open Finset MeasureTheory ProbabilityTheory
open scoped ProbabilityTheory ENNReal
variable {α Ω : Type*} [DecidableEq α] [MeasurableSpace Ω]

/-- Variance of a constant plus a signed finite sum of independent Gaussian variables.
The Gaussian law entails L² and the correct variance parameter; neither is assumed as the goal. -/
theorem signed_gaussian_variance (μ : Measure Ω) [IsProbabilityMeasure μ]
    (A : Finset α) (ε : α → Ω → ℝ) (c : α → ℝ) (b : ℝ) (σ2 : ℝ≥0)
    (hm : ∀ i ∈ A, Measurable (ε i))
    (hlaw : ∀ i ∈ A, μ.map (ε i) = gaussianReal 0 σ2)
    (hi : Set.Pairwise (↑A : Set α) fun i j => IndepFun (ε i) (ε j) μ)
    (hc : ∀ i ∈ A, c i ^ 2 = 1) :
    variance (fun ω => b + ∑ i ∈ A, c i * ε i ω) μ = (A.card : ℝ) * σ2 := by
  have hp : ∀ i ∈ A, MemLp (ε i) 2 μ := by
    intro i hiA
    have h : MemLp id 2 (μ.map (ε i)) := by
      rw [hlaw i hiA]
      exact memLp_id_gaussianReal' 2 (by norm_num)
    simpa only [Function.comp_def, id_eq] using
      h.comp_measurePreserving ⟨hm i hiA, hlaw i hiA ▸ rfl⟩
  have hv : ∀ i ∈ A, variance (ε i) μ = σ2 := by
    intro i hiA
    rw [← variance_id_map (hm i hiA).aemeasurable, hlaw i hiA]
    exact variance_id_gaussianReal
  have hp' : ∀ i ∈ A, MemLp (fun ω => c i * ε i ω) 2 μ := by
    intro i hiA
    simpa only [smul_eq_mul] using (hp i hiA).const_smul (c i)
  have hi' : Set.Pairwise (↑A : Set α) fun i j =>
      IndepFun (fun ω => c i * ε i ω) (fun ω => c j * ε j ω) μ := by
    intro i hiA j hjA hij
    simpa only [Function.comp_def] using
      (hi hiA hjA hij).comp (measurable_const.mul measurable_id) (measurable_const.mul measurable_id)
  have hs : AEStronglyMeasurable (fun ω => ∑ i ∈ A, c i * ε i ω) μ := by
    exact ((memLp_finset_sum' _ hp').aestronglyMeasurable)
  rw [variance_const_add hs]
  change variance (∑ i ∈ A, fun ω => c i * ε i ω) μ = _
  rw [IndepFun.variance_sum hp' hi']
  simp_rw [variance_mul]
  rw [sum_congr rfl (fun i hiA => by rw [hc i hiA, hv i hiA]; simp)]
  simp

/-- Appendix D: the independent Gaussian noise acts on every subcoalition output. -/
theorem and_gaussian_variance (μ : Measure Ω) [IsProbabilityMeasure μ]
    (T : Finset α) (ε : Finset α → Ω → ℝ) (I : ℝ) (σ2 : ℝ≥0)
    (hm : ∀ L ∈ T.powerset, Measurable (ε L))
    (hlaw : ∀ L ∈ T.powerset, μ.map (ε L) = gaussianReal 0 σ2)
    (hi : Set.Pairwise (↑T.powerset : Set (Finset α)) fun L K => IndepFun (ε L) (ε K) μ) :
    variance (fun ω => I + ∑ L ∈ T.powerset,
      (-1 : ℝ) ^ (T.card - L.card) * ε L ω) μ = (2 : ℝ) ^ T.card * σ2 := by
  rw [signed_gaussian_variance μ T.powerset ε
      (fun L => (-1 : ℝ) ^ (T.card - L.card)) I σ2 hm hlaw hi]
  · simp
  · intro L hL
    rw [← pow_mul]
    simp [Nat.mul_comm, pow_mul]

end Harsanyi
