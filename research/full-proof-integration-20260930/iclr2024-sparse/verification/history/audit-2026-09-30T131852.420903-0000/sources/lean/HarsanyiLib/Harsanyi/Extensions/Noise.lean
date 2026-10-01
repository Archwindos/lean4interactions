import Harsanyi.Extensions.OrInteraction
import Mathlib.Probability.Distributions.Gaussian.Real

/-! Genuine random-variable variances, not only a sum of squared signs. -/
namespace Harsanyi
open Finset MeasureTheory ProbabilityTheory
open scoped ProbabilityTheory ENNReal
variable {α Ω : Type*} [DecidableEq α] [MeasurableSpace Ω]

/-- Variance of a constant plus a signed finite sum of independent Gaussian variables.
The Gaussian law entails L² and the correct variance parameter; neither is assumed as the goal. -/
theorem signed_gaussian_variance (μ : Measure Ω) [IsProbabilityMeasure μ]
    (A : Finset α) (ε : α → Ω → ℝ) (c : α → ℝ) (b : ℝ) (σ2 : NNReal)
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
    have hfun : (∑ i ∈ A, fun ω => c i * ε i ω) = (fun ω => ∑ i ∈ A, c i * ε i ω) := by
      funext ω
      simp
    rw [← hfun]
    exact (memLp_finset_sum' _ hp').aestronglyMeasurable
  rw [variance_const_add hs]
  have hfun : (fun ω => ∑ i ∈ A, c i * ε i ω) = (∑ i ∈ A, fun ω => c i * ε i ω) := by
    funext ω
    simp
  rw [hfun]
  rw [IndepFun.variance_sum hp' hi']
  simp_rw [variance_mul]
  rw [sum_congr rfl (fun i hiA => by rw [hc i hiA, hv i hiA])]
  simp

/-- Appendix D: the independent Gaussian noise acts on every subcoalition output. -/
theorem and_gaussian_variance (μ : Measure Ω) [IsProbabilityMeasure μ]
    (T : Finset α) (ε : Finset α → Ω → ℝ) (I : ℝ) (σ2 : NNReal)
    (hm : ∀ L ∈ T.powerset, Measurable (ε L))
    (hlaw : ∀ L ∈ T.powerset, μ.map (ε L) = gaussianReal 0 σ2)
    (hi : Set.Pairwise (↑T.powerset : Set (Finset α)) fun L K => IndepFun (ε L) (ε K) μ) :
    variance (fun ω => I + ∑ L ∈ T.powerset,
      (-1 : ℝ) ^ (T.card - L.card) * ε L ω) μ = (2 : ℝ) ^ T.card * σ2 := by
  rw [signed_gaussian_variance μ T.powerset ε
      (fun L => (-1 : ℝ) ^ (T.card - L.card)) I σ2 hm hlaw hi]
  · simp
  · intro L hL
    rw [← pow_mul, Nat.mul_comm, pow_mul]
    norm_num

/-- The OR case uses the same independent family at the distinct complement masks.
The output identity for a nonempty OR coalition is supplied by the source definition. -/
theorem or_gaussian_variance (μ : Measure Ω) [IsProbabilityMeasure μ]
    (N T : Finset α) (hTN : T ⊆ N) (ε : Finset α → Ω → ℝ) (I : ℝ) (σ2 : NNReal)
    (hm : ∀ L ⊆ N, Measurable (ε L))
    (hlaw : ∀ L ⊆ N, μ.map (ε L) = gaussianReal 0 σ2)
    (hi : Set.Pairwise (↑N.powerset : Set (Finset α)) fun L K => IndepFun (ε L) (ε K) μ) :
    variance (fun ω => I + ∑ L ∈ T.powerset,
      -((-1 : ℝ) ^ (T.card - L.card)) * ε (N \ L) ω) μ = (2 : ℝ) ^ T.card * σ2 := by
  have hm' : ∀ L ∈ T.powerset, Measurable (ε (N \ L)) := by
    intro L hL
    exact hm _ sdiff_subset
  have hlaw' : ∀ L ∈ T.powerset, μ.map (ε (N \ L)) = gaussianReal 0 σ2 := by
    intro L hL
    exact hlaw _ sdiff_subset
  have hi' : Set.Pairwise (↑T.powerset : Set (Finset α)) fun L K =>
      IndepFun (ε (N \ L)) (ε (N \ K)) μ := by
    intro L hL K hK hLK
    apply hi (by exact mem_powerset.mpr sdiff_subset) (by exact mem_powerset.mpr sdiff_subset)
    intro h
    have hLN : L ⊆ N := (mem_powerset.mp hL).trans hTN
    have hKN : K ⊆ N := (mem_powerset.mp hK).trans hTN
    have h' := congrArg (fun U => N \ U) h
    change N \ (N \ L) = N \ (N \ K) at h'
    rw [sdiff_sdiff_eq_self hLN, sdiff_sdiff_eq_self hKN] at h'
    exact hLK h'
  rw [signed_gaussian_variance μ T.powerset (fun L => ε (N \ L))
      (fun L => -((-1 : ℝ) ^ (T.card - L.card))) I σ2 hm' hlaw' hi']
  · simp
  · intro L hL
    rw [neg_sq, ← pow_mul, Nat.mul_comm, pow_mul]
    norm_num

/-- Actual perturbation of a fixed masked-output family, not a hypothesized interaction identity. -/
noncomputable def noisyMaskedGame (g : Game α) (ε : Finset α → Ω → ℝ) (ω : Ω) : Game α :=
  fun L => g L + ε L ω

theorem noisy_and_identity (g : Game α) (ε : Finset α → Ω → ℝ) (ω : Ω) (T : Finset α) :
    interaction (noisyMaskedGame g ε ω) T = interaction g T +
      ∑ L ∈ T.powerset, (-1 : ℝ) ^ (T.card - L.card) * ε L ω := by
  change interaction (fun L => g L + ε L ω) T = _
  rw [interaction_add]
  rfl

theorem noisy_or_identity (g : Game α) (N T : Finset α) (hT : T.Nonempty)
    (ε : Finset α → Ω → ℝ) (ω : Ω) :
    orInteraction (noisyMaskedGame g ε ω) N T = orInteraction g N T +
      ∑ L ∈ T.powerset, -((-1 : ℝ) ^ (T.card - L.card)) * ε (N \ L) ω := by
  rw [or_dual _ _ _ hT.ne_empty, or_dual _ _ _ hT.ne_empty]
  change -interaction (fun L => g (N \ L) + ε (N \ L) ω) T = _
  rw [interaction_add]
  simp only [interaction, neg_add_rev, neg_mul, sum_neg_distrib]
  ring

/-- Full Generalizable AND variance for the perturbed output family, including the raw empty baseline. -/
theorem noisy_masked_and_variance (μ : Measure Ω) [IsProbabilityMeasure μ]
    (g : Game α) (T : Finset α) (ε : Finset α → Ω → ℝ) (σ2 : NNReal)
    (hm : ∀ L ∈ T.powerset, Measurable (ε L))
    (hlaw : ∀ L ∈ T.powerset, μ.map (ε L) = gaussianReal 0 σ2)
    (hi : Set.Pairwise (↑T.powerset : Set (Finset α)) fun L K => IndepFun (ε L) (ε K) μ) :
    variance (fun ω => interaction (noisyMaskedGame g ε ω) T) μ =
      (2 : ℝ) ^ T.card * σ2 := by
  simp_rw [noisy_and_identity]
  exact and_gaussian_variance μ T ε (interaction g T) σ2 hm hlaw hi

/-- Full OR variance for the same fixed masked-output perturbation; the separate empty branch is included. -/
theorem noisy_masked_or_variance (μ : Measure Ω) [IsProbabilityMeasure μ]
    (g : Game α) (N T : Finset α) (hTN : T ⊆ N) (ε : Finset α → Ω → ℝ) (σ2 : NNReal)
    (hm : ∀ L ⊆ N, Measurable (ε L))
    (hlaw : ∀ L ⊆ N, μ.map (ε L) = gaussianReal 0 σ2)
    (hi : Set.Pairwise (↑N.powerset : Set (Finset α)) fun L K => IndepFun (ε L) (ε K) μ) :
    variance (fun ω => orInteraction (noisyMaskedGame g ε ω) N T) μ =
      (2 : ℝ) ^ T.card * σ2 := by
  by_cases hT : T = ∅
  · subst T
    simp only [orInteraction, noisyMaskedGame, if_true, card_empty, pow_zero, one_mul]
    rw [variance_const_add (hm ∅ (empty_subset N)).aestronglyMeasurable]
    rw [← variance_id_map (hm ∅ (empty_subset N)).aemeasurable, hlaw ∅ (empty_subset N)]
    exact variance_id_gaussianReal
  · simp_rw [noisy_or_identity g N T (nonempty_iff_ne_empty.mpr hT) ε]
    exact or_gaussian_variance μ N T hTN ε (orInteraction g N T) σ2 hm hlaw hi

end Harsanyi
