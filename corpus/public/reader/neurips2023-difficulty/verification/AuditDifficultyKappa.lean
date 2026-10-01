import Lean.Util.CollectAxioms
import Harsanyi.Extensions.DifficultyRegression
import Harsanyi.Extensions.DifficultyCounting
import Harsanyi.Extensions.DifficultyKappa
import Harsanyi.Extensions.ConceptGaussian
import Harsanyi.Extensions.ConceptMasks
import Harsanyi.Extensions.PolynomialSupport
import Harsanyi.Extensions.RobustnessFinite

namespace PaperDifficulty
open Finset MeasureTheory ProbabilityTheory Harsanyi
open scoped BigOperators

/-- Literal source Proposition1 at one genuine Gaussian factor: Var=2, Var²=4. -/
theorem product_variance_counterexample :
    variance (fun z : ℝ => ∏ _i : Fin 1, z) (gaussianReal 0 2) = 2 ∧
      ((∏ _i : Fin 1, ((∫ z : ℝ, z ∂gaussianReal 0 2) ^ 2 +
        variance (id : ℝ → ℝ) (gaussianReal 0 2) ^ 2)) -
        ∏ _i : Fin 1, (∫ z : ℝ, z ∂gaussianReal 0 2) ^ 2) = 4 := by
  simp only [Fin.prod_univ_succ, Fin.prod_univ_zero, mul_one]
  simp only [integral_id_gaussianReal, variance_id_gaussianReal]
  norm_num

noncomputable def sourceTrigger (e : ℝ) : ℝ :=
  |(1 + e) - 0| / 1

/-- Both the lowest and general degree-one source J are the same absolute trigger. -/
theorem lowest_trigger_mean_counterexample (q : NNReal) (hq : q ≠ 0) :
    (∫ e, sourceTrigger e ∂gaussianReal 0 q) > 1 := by
  have hm : (gaussianReal 0 q).map (fun e : ℝ => 1+e) = gaussianReal 1 q := by
    simpa using (gaussianReal_map_const_add (μ := (0:ℝ)) (v := q) (1:ℝ))
  have h := ConceptGaussian.folded_first_moment_gt_one q hq
  rw [← hm] at h
  have he : (∫ z : ℝ, |z| ∂(gaussianReal 0 q).map (fun e : ℝ => 1+e)) =
      (∫ e : ℝ, |1+e| ∂gaussianReal 0 q) := by
    exact integral_map (show Measurable (fun e : ℝ => 1+e) by fun_prop).aemeasurable
      (show AEStronglyMeasurable (fun z : ℝ => |z|)
        ((gaussianReal 0 q).map (fun e : ℝ => 1+e)) from measurable_id.abs.aestronglyMeasurable)
  rw [he] at h
  simpa only [sourceTrigger, sub_zero, div_one, Function.comp_def] using h

/-- The same actual absolute trigger also contradicts the source lowest variance. -/
theorem lowest_trigger_variance_counterexample (q : NNReal) (hq : q ≠ 0) :
    variance sourceTrigger (gaussianReal 0 q) < (q : ℝ) := by
  let μ := gaussianReal 0 q
  have hm : μ.map (fun e : ℝ => 1+e) = gaussianReal 1 q := by
    simpa [μ] using (gaussianReal_map_const_add (μ := (0:ℝ)) (v := q) (1:ℝ))
  have hx := ConceptGaussian.gaussian_feature_moments μ (fun e : ℝ => 1+e) 1 q
    (by fun_prop) hm
  have habs : MemLp sourceTrigger 2 μ := by
    rw [show sourceTrigger = (fun e : ℝ => |1+e|) from by funext e; simp [sourceTrigger]]
    simpa only [Real.norm_eq_abs] using hx.1.norm
  have hs := variance_eq_sub hx.1
  have hv := variance_eq_sub habs
  have he : (∫ e : ℝ, (sourceTrigger e)^2 ∂μ) = (q:ℝ)+1 := by
    simp only [sourceTrigger, sub_zero, div_one, sq_abs]
    change variance (fun e : ℝ => 1+e) μ =
      (∫ e : ℝ, (1+e)^2 ∂μ) - (∫ e : ℝ, 1+e ∂μ)^2 at hs
    rw [hx.2.1, hx.2.2] at hs
    linarith
  change variance sourceTrigger μ = (∫ e : ℝ, sourceTrigger e ^ 2 ∂μ) -
    (∫ e : ℝ, sourceTrigger e ∂μ)^2 at hv
  rw [he] at hv
  have hpos := lowest_trigger_mean_counterexample q hq
  change (∫ e : ℝ, sourceTrigger e ∂μ) > 1 at hpos
  change variance sourceTrigger μ < (q:ℝ)
  nlinarith

noncomputable def featureMeans (i : Fin 2) : ℝ := if i=0 then 1 else 2
noncomputable def featureLaw : Measure (Fin 2 → ℝ) :=
  Measure.pi (fun i => gaussianReal (featureMeans i) 1)

instance : IsProbabilityMeasure featureLaw := by unfold featureLaw; infer_instance

/-- Actual mutually independent Gaussian coordinates with means1,2 and variances1,1. -/
theorem feature_model :
    (∀ i : Fin 2, featureLaw.map (fun z => z i) = gaussianReal (featureMeans i) 1) ∧
      iIndepFun (fun i (z : Fin 2 → ℝ) => z i) featureLaw := by
  constructor
  · intro i
    exact (measurePreserving_eval (fun j => gaussianReal (featureMeans j) 1) i).map_eq
  · exact iIndepFun_pi (fun _ => measurable_id.aemeasurable)

noncomputable def optimalWeights : Fin 2 → ℝ := fun i => if i=0 then 1/6 else 1/3

theorem featureOpt_values :
    ConceptGaussian.featureOpt featureMeans (fun _ : Fin 2 => 1) 1 = optimalWeights := by
  funext i
  fin_cases i <;> norm_num [ConceptGaussian.featureOpt, featureMeans, optimalWeights,
    Fin.sum_univ_succ]

/-- Source G5 Step3 fails for the actual Gaussian regression, with Σ=Σ²=I. -/
theorem regression_step_three_counterexample :
    (∀ w : Fin 2 → ℝ, w ≠ optimalWeights →
      (∫ z, (1 - ∑ i, optimalWeights i * z i) ^ 2 ∂featureLaw) <
        (∫ z, (1 - ∑ i, w i * z i) ^ 2 ∂featureLaw)) ∧
      |optimalWeights 0 / optimalWeights 1| = (1/2:ℝ) ∧
      |optimalWeights 0 / optimalWeights 1| ≠ |(1:ℝ)/(1:ℝ)| := by
  have h := ConceptGaussian.gaussian_feature_unique_min featureLaw
    (fun i (z : Fin 2 → ℝ) => z i) featureMeans (fun _ => (1:NNReal))
    (fun i => measurable_pi_apply i) feature_model.1 feature_model.2
    (fun _ => by norm_num) 1
  simp only [NNReal.coe_one] at h
  rw [featureOpt_values] at h
  refine ⟨h, ?_, ?_⟩ <;> norm_num [optimalWeights]

/-- Actual Boolean masks of a coordinate-product score; x=1,r=0. -/
noncomputable def maskedPolynomial {α : Type*} [DecidableEq α]
    (A T : Finset α) : ℝ := ∏ i ∈ A, (if i∈T then (1:ℝ) else 0)

theorem maskedPolynomial_eq_unanimity {α : Type*} [DecidableEq α] (A T : Finset α) :
    maskedPolynomial A T = unanimity A 1 T := by
  unfold maskedPolynomial unanimity
  split_ifs with h
  · apply Finset.prod_eq_one
    intro i hi
    simp [h hi]
  · obtain ⟨i,hi,hit⟩ := Finset.not_subset.mp h
    exact Finset.prod_eq_zero hi (by simp [hit])

noncomputable def sourceMultiorderRHS {α : Type*} [DecidableEq α]
    (g : Game α) (N : Finset α) (i j : α) (m : ℕ) : ℝ :=
  ∑ l ∈ range (m+1), ((N.card-2).choose (m-l) : ℝ) / ((N.card-2).choose m : ℝ) *
    ∑ L ∈ (N \ {i,j}).powersetCard m, interaction g (L ∪ {i,j})

/-- The actual degree-two masked score has interaction1; the printed |L|=m gives0. -/
theorem multiorder_index_counterexample :
    Robustness.multiOrderInteraction (maskedPolynomial ({0,1}:Finset (Fin 3))) univ 0 1 1 = 1 ∧
      sourceMultiorderRHS (maskedPolynomial ({0,1}:Finset (Fin 3))) univ 0 1 1 = 0 := by
  have hg : maskedPolynomial ({0,1} : Finset (Fin 3)) = unanimity {0,1} 1 :=
    funext (fun T => maskedPolynomial_eq_unanimity _ T)
  have h02 : (0 : Fin 3) ≠ 2 := by decide
  have h12 : (1 : Fin 3) ≠ 2 := by decide
  rw [hg]
  rw [show (univ : Finset (Fin 3)) = {0,1,2} by decide]
  have hC : (({0,1,2} : Finset (Fin 3)) \ {0,1}).powersetCard 1 = {{2}} := by decide
  simp only [Robustness.multiOrderInteraction, Robustness.contextAverage, sourceMultiorderRHS, hC]
  norm_num [Robustness.multiOrderInteraction, Robustness.contextAverage, Robustness.average,
    Robustness.pairDelta, sourceMultiorderRHS, interaction_unanimity, unanimity,
    hC, h02, h12, Fin.sum_univ_succ, Finset.subset_iff, Finset.ext_iff, Finset.sum_range_succ]

/-- Repairing only the |L| index leaves the separate erroneous binomial coefficient. -/
noncomputable def sourceCoefficientRHS {α : Type*} [DecidableEq α]
    (g : Game α) (N : Finset α) (i j : α) (m : ℕ) : ℝ :=
  ∑ l ∈ range (m+1), ((N.card-2).choose (m-l) : ℝ) / ((N.card-2).choose m : ℝ) *
    ∑ L ∈ (N \ {i,j}).powersetCard l, interaction g (L ∪ {i,j})

theorem multiorder_coefficient_counterexample :
    Robustness.multiOrderInteraction (maskedPolynomial ({0,1,2}:Finset (Fin 4))) univ 0 1 2 = 1 ∧
      sourceCoefficientRHS (maskedPolynomial ({0,1,2}:Finset (Fin 4))) univ 0 1 2 = 2 := by
  have hg : maskedPolynomial ({0,1,2} : Finset (Fin 4)) = unanimity {0,1,2} 1 :=
    funext (fun T => maskedPolynomial_eq_unanimity _ T)
  have h02 : (0 : Fin 4) ≠ 2 := by decide
  have h03 : (0 : Fin 4) ≠ 3 := by decide
  have h12 : (1 : Fin 4) ≠ 2 := by decide
  have h13 : (1 : Fin 4) ≠ 3 := by decide
  have h23 : (2 : Fin 4) ≠ 3 := by decide
  have h01 : (0 : Fin 4) ≠ 1 := by decide
  have hN : ({0,1,2,3} : Finset (Fin 4)).card = 4 := by decide
  rw [hg]
  rw [show (univ : Finset (Fin 4)) = {0,1,2,3} by decide]
  have hC2 : (({0,1,2,3} : Finset (Fin 4)) \ {0,1}).powersetCard 2 = {{2,3}} := by decide
  have hC1 : (({0,1,2,3} : Finset (Fin 4)) \ {0,1}).powersetCard 1 = {{2},{3}} := by decide
  have hC0 : (({0,1,2,3} : Finset (Fin 4)) \ {0,1}).powersetCard 0 = {∅} := by decide
  have hR : (({0,1,2,3} : Finset (Fin 4)) \ {0,1}) = {2,3} := by decide
  have hR' : (({1,2,3} : Finset (Fin 4)) \ {0,1}) = {2,3} := by decide
  have hD2 : ({2,3} : Finset (Fin 4)).powersetCard 2 = {{2,3}} := by decide
  have hD1 : ({2,3} : Finset (Fin 4)).powersetCard 1 = {{2},{3}} := by decide
  have hD0 : ({2,3} : Finset (Fin 4)).powersetCard 0 = {∅} := by decide
  simp only [Robustness.multiOrderInteraction, Robustness.contextAverage, sourceCoefficientRHS, hR, hD2]
  norm_num [Robustness.multiOrderInteraction, Robustness.contextAverage, Robustness.average,
    Robustness.pairDelta, sourceCoefficientRHS, interaction_unanimity, unanimity,
    hC2, hC1, hC0, hR, hR', hD2, hD1, hD0, h02, h03, h12, h13, h23, h01, hN, Fin.sum_univ_succ, Finset.subset_iff, Finset.ext_iff, Finset.sum_range_succ] <;> decide

/-- The source dummy premise ranges over every context, including the empty one. -/
theorem source_dummy {α : Type*} [DecidableEq α] (g : Game α) (N S : Finset α)
    (i : α) (hS : S.Nonempty) (hSN : S ⊆ N \ {i})
    (h : ∀ U ⊆ N \ {i}, g (U ∪ {i}) = g U + g {i}) :
    interaction g (S ∪ {i}) = 0 := by
  have hi : i ∉ S := by
    intro hiS
    have := hSN hiS
    simpa using this
  rw [union_singleton]
  exact interaction_additive_dummy_nonempty g S i hi hS (g {i}) (fun U hU => by
    simpa [union_singleton] using h U (hU.trans hSN))

/-- Two-coordinate finite difference, before taking any context average. -/
theorem pairDelta_eq_dividend_sum {α : Type*} [DecidableEq α] (g : Game α)
    (S : Finset α) (i j : α) (hij : i ≠ j) (hi : i ∉ S) (hj : j ∉ S) :
    Robustness.pairDelta g i j S = ∑ L ∈ S.powerset, interaction g (L ∪ {i,j}) := by
  have hd : Disjoint ({i,j} : Finset α) S := by simp [Finset.disjoint_left, hi, hj]
  have he : higherMarginal g {i,j} S = Robustness.pairDelta g i j S := by
    unfold higherMarginal
    rw [interaction_insert _ {j} i (by simp [hij]), interaction_singleton]
    simp only [marginal, singleton_union, empty_union]
    unfold Robustness.pairDelta
    simp only [Finset.insert_union, singleton_union, empty_union]
    ring
  rw [← he, higherMarginal_eq_sum_interaction g _ S hd]
  apply Finset.sum_congr rfl
  intro L _
  rw [union_comm]

/-- Exact context-average relation; source's two wrong combinatorial simplifications are absent. -/
theorem multiorder_context_identity {α : Type*} [DecidableEq α] (g : Game α)
    (N : Finset α) (i j : α) (m : ℕ) (hij : i ≠ j) :
    Robustness.multiOrderInteraction g N i j m =
      Robustness.contextAverage (N \ {i,j}) m
        (fun S => ∑ L ∈ S.powerset, interaction g (L ∪ {i,j})) := by
  unfold Robustness.multiOrderInteraction Robustness.contextAverage Robustness.average
  congr 1
  apply Finset.sum_congr rfl
  intro S hS
  have hs := (Finset.mem_powersetCard.mp hS).1
  apply pairDelta_eq_dividend_sum g S i j hij
  · intro hi
    have := hs hi
    simpa using this
  · intro hj
    have := hs hj
    simpa using this

/-- Correct source-sized grouping, with n-2 variables outside the distinct pair. -/
theorem multiorder_grouped_identity {α : Type*} [DecidableEq α] (g : Game α)
    (N : Finset α) (i j : α) (m : ℕ) (hi : i ∈ N) (hj : j ∈ N)
    (hij : i ≠ j) (hm : m ≤ N.card-2) :
    Robustness.multiOrderInteraction g N i j m =
      ∑ l ∈ range (m+1), ((N.card-2-l).choose (m-l) : ℝ) /
        ((N.card-2).choose m : ℝ) *
          ∑ L ∈ (N \ {i,j}).powersetCard l, interaction g (L ∪ {i,j}) := by
  rw [multiorder_context_identity g N i j m hij,
    DifficultyCounting.context_grouped_average]
  have hsub : ({i,j} : Finset α) ⊆ N := by
    intro x hx
    rcases mem_insert.mp hx with hxi | hxj
    · simpa [hxi] using hi
    · simpa [mem_singleton.mp hxj] using hj
  have hcard : (N \ {i,j}).card = N.card-2 := by
    rw [card_sdiff_of_subset hsub]
    simp [hij]
  rw [hcard]

/-- Original I is an actual lowest-degree coordinate polynomial with arbitrary output baseline. -/
noncomputable def maskedLowest {ι : Type*} [Fintype ι] [DecidableEq ι]
    (a b : ℝ) (z : ι → ℝ) : Game ι :=
  fun T => b + a * ∏ i, if i ∈ T then z i else 0

theorem maskedLowest_eq {ι : Type*} [Fintype ι] [DecidableEq ι]
    (a b : ℝ) (z : ι → ℝ) :
    maskedLowest a b z = fun T => b + unanimity univ (a*∏ i,z i) T := by
  funext T
  unfold maskedLowest unanimity
  by_cases h : (univ : Finset ι) ⊆ T
  · have hi : ∀ i, i ∈ T := fun i => h (mem_univ i)
    simp [h,hi]
  · obtain ⟨i,hi,hit⟩ := Finset.not_subset.mp h
    have hz : (∏ i, if i ∈ T then z i else 0) = 0 :=
      prod_eq_zero hi (by simp [hit])
    simp [h,hz]

theorem lowest_actual_dividend {ι : Type*} [Fintype ι] [DecidableEq ι] [Nonempty ι]
    (a b : ℝ) (z : ι → ℝ) :
    interaction (maskedLowest a b z) univ = a * ∏ i,z i := by
  rw [maskedLowest_eq,interaction_add,interaction_const,interaction_unanimity]
  have hu : (univ : Finset ι) ≠ ∅ := Finset.univ_nonempty.ne_empty
  simp [hu]

/-- Appendix lowest-I moments, with U at the fixed reference and full Gaussian tails. -/
theorem appendix_lowest_actual_moments {Ω ι : Type*} [MeasurableSpace Ω]
    [Fintype ι] [DecidableEq ι] [Nonempty ι] (μ : Measure Ω) [IsProbabilityMeasure μ]
    (ε : ι → Ω → ℝ) (q : NNReal) (s : ι → ℝ) (τ a b : ℝ)
    (hs : ∀ i,s i^2=1) (hτ : τ ≠ 0) (hmeas : ∀ i,Measurable (ε i))
    (hlaw : ∀ i,μ.map (ε i)=gaussianReal 0 q) (hind : iIndepFun ε μ) :
    let U := a * ∏ i,s i*τ
    (∫ ω, interaction (maskedLowest a b (fun i => s i*τ+ε i ω)) univ ∂μ) = U ∧
      variance (fun ω => interaction (maskedLowest a b (fun i => s i*τ+ε i ω)) univ) μ =
        U^2*((1+(q:ℝ)/τ^2)^Fintype.card ι-1) := by
  simp only [lowest_actual_dividend]
  have he : (fun ω => a * (∏ i, (s i*τ+ε i ω))) =
      (fun ω => (a*(∏ i,s i*τ)) * (∏ i,(1+s i*ε i ω/τ))) := by
    funext ω
    exact (ConceptGaussian.lowest_polynomial_identity a τ s (fun i => ε i ω) hs hτ).symm
  rw [he]
  exact ConceptGaussian.lowest_interaction_moments μ ε q s τ (a*∏ i,s i*τ)
    hs hmeas hlaw hind
/-- Exact Cramer adapter to the source regression notation. -/
theorem feature_opt_cramer {ι : Type*} [Fintype ι] [DecidableEq ι]
    (a d : ι → ℝ) (y : ℝ) (hd : ∀ i, 0 < d i) (i : ι) :
    0 < (ConceptGaussian.featureMatrix a d).det ∧
    ConceptGaussian.featureOpt a d y i =
      ((ConceptGaussian.featureMatrix a d).updateCol i (fun j => y*a j)).det /
        (ConceptGaussian.featureMatrix a d).det :=
  DifficultyRegression.feature_opt_cramer a d y hd i

theorem half_loss_strict_iff (a b : ℝ) : (1/2 : ℝ)*a < (1/2 : ℝ)*b ↔ a < b :=
  DifficultyRegression.half_loss_strict_iff a b

/-- Empty interaction is the fixed output baseline, with zero noise variance. -/
theorem empty_interaction_moments {Ω α : Type*} [MeasurableSpace Ω] [DecidableEq α]
    (μ : Measure Ω) [IsProbabilityMeasure μ] (g : Ω → Game α) (b : ℝ)
    (hb : ∀ ω, g ω ∅ = b) :
    (∫ ω, interaction (g ω) ∅ ∂μ) = b ∧
      variance (fun ω => interaction (g ω) ∅) μ = 0 := by
  have he : (fun ω => interaction (g ω) ∅) = fun _ => b := by
    funext ω
    simpa only [interaction_empty] using hb ω
  rw [he]
  constructor
  · simp
  · rw [variance_eq_integral aemeasurable_const]
    simp
end PaperDifficulty

open Lean Elab Command Meta
set_option pp.universes true
set_option pp.fullNames true
set_option pp.piBinderTypes true
run_cmd liftTermElabM do
  for name in #[`Harsanyi.TaylorMoments.monomial, `Harsanyi.TaylorMoments.monomial_mask, `Harsanyi.TaylorMoments.polynomial_mask, `Harsanyi.TaylorMoments.normalized_trigger, `Harsanyi.TaylorMoments.zero_trigger_counterexample, `Harsanyi.TaylorMoments.product_mean, `Harsanyi.TaylorMoments.product_variance, `Harsanyi.TaylorMoments.product_memLp, `Harsanyi.TaylorMoments.gaussian_affine_product, `Harsanyi.TaylorMoments.unit_mean_product_variance, `Harsanyi.TaylorMoments.scaling_ratio, `Harsanyi.TaylorMoments.moving_sign_counterexample, `Harsanyi.NoisyRegression.zeta, `Harsanyi.NoisyRegression.zeta_mulVec, `Harsanyi.NoisyRegression.zeta_injective, `Harsanyi.NoisyRegression.gram_posDef, `Harsanyi.NoisyRegression.normalMatrix, `Harsanyi.NoisyRegression.normal_posDef, `Harsanyi.NoisyRegression.normal_isUnit, `Harsanyi.NoisyRegression.normal_solution, `Harsanyi.NoisyRegression.zero_noise, `Harsanyi.NoisyRegression.quadraticLoss, `Harsanyi.NoisyRegression.symmetric_dot, `Harsanyi.NoisyRegression.quadratic_difference, `Harsanyi.NoisyRegression.quadratic_unique_min, `Harsanyi.NoisyRegression.normal_unique_min, `Harsanyi.NoisyRegression.residualLoss, `Harsanyi.NoisyRegression.residualLoss_expansion, `Harsanyi.NoisyRegression.residual_unique_min, `Harsanyi.NoisyRegression.featureLoss, `Harsanyi.NoisyRegression.feature_normal_scaling, `Harsanyi.NoisyRegression.transferMatrix, `Harsanyi.NoisyRegression.zeta_permutation, `Harsanyi.NoisyRegression.transfer_permutation, `Harsanyi.NoisyRegression.row_norm_permutation, `Harsanyi.NoisyRegression.exists_coalition_permutation, `Harsanyi.NoisyRegression.equal_order_row_norm, `Harsanyi.NoisyRegression.transfer_zero, `Harsanyi.NoisyRegression.diagonal_product_counterexample, `Harsanyi.GaussianRegression.gaussian_memLp, `Harsanyi.GaussianRegression.gaussian_mean, `Harsanyi.GaussianRegression.independent_residual, `Harsanyi.GaussianRegression.gaussian_residual, `Harsanyi.PolynomialSupport.polynomial, `Harsanyi.PolynomialSupport.supportCoefficient, `Harsanyi.PolynomialSupport.mask_terms, `Harsanyi.PolynomialSupport.support_reconstruct, `Harsanyi.PolynomialSupport.interaction_eq_supportCoefficient, `Harsanyi.ConceptGaussian.scaledVariance, `Harsanyi.ConceptGaussian.signed_scaled_law, `Harsanyi.ConceptGaussian.lowest_interaction_moments, `Harsanyi.ConceptGaussian.lowest_polynomial_identity, `Harsanyi.ConceptGaussian.feature_expected_loss, `Harsanyi.ConceptGaussian.featureMatrix, `Harsanyi.ConceptGaussian.pairwise_feature_expected_loss, `Harsanyi.ConceptGaussian.featureOpt, `Harsanyi.ConceptGaussian.featureMatrix_posDef, `Harsanyi.ConceptGaussian.featureLoss_quadratic, `Harsanyi.ConceptGaussian.featureOpt_normal, `Harsanyi.ConceptGaussian.featureOpt_unique_min, `Harsanyi.ConceptGaussian.feature_expected_unique_min, `Harsanyi.ConceptGaussian.pairwise_feature_expected_unique_min, `Harsanyi.ConceptGaussian.gaussian_memLp_any, `Harsanyi.ConceptGaussian.gaussian_feature_moments, `Harsanyi.ConceptGaussian.gaussian_feature_unique_min, `Harsanyi.ConceptGaussian.folded_power_memLp, `Harsanyi.ConceptGaussian.folded_product_moments, `Harsanyi.ConceptGaussian.folded_gaussian_variance_pos, `Harsanyi.ConceptGaussian.reflection_power_bound, `Harsanyi.ConceptGaussian.signed_power_memLp, `Harsanyi.ConceptGaussian.signed_gaussian_moment_ge_one, `Harsanyi.ConceptGaussian.unit_gaussian_power_bounds, `Harsanyi.ConceptGaussian.folded_map_variance_pos, `Harsanyi.ConceptGaussian.folded_subset_moments, `Harsanyi.ConceptGaussian.folded_subset_positive, `Harsanyi.ConceptGaussian.folded_disjoint_moments, `Harsanyi.ConceptGaussian.product_growth_bounds, `Harsanyi.ConceptGaussian.folded_subset_growth, `Harsanyi.ConceptGaussian.folded_first_moment_gt_one, `Harsanyi.ConceptMasks.maskedGame, `Harsanyi.ConceptMasks.masked_dividend, `Harsanyi.ConceptMasks.normalizedMaskedTrigger, `Harsanyi.ConceptMasks.binary_trigger, `Harsanyi.ConceptMasks.linear_representation, `Harsanyi.DifficultyKappa.unitLaw, `Harsanyi.DifficultyKappa.absoluteFirstMoment, `Harsanyi.DifficultyKappa.unit_memLp, `Harsanyi.DifficultyKappa.unit_integrable, `Harsanyi.DifficultyKappa.absoluteFirstMoment_pos, `Harsanyi.DifficultyKappa.chosenScale, `Harsanyi.DifficultyKappa.chosenScale_pos, `Harsanyi.DifficultyKappa.chosenScale_small, `Harsanyi.DifficultyKappa.chosenScale_bound, `Harsanyi.DifficultyKappa.perturbation, `Harsanyi.DifficultyKappa.perturbationVariance, `Harsanyi.DifficultyKappa.perturbation_law, `Harsanyi.DifficultyKappa.perturbation_integrable, `Harsanyi.DifficultyKappa.perturbation_square_integrable, `Harsanyi.DifficultyKappa.perturbation_moments, `Harsanyi.DifficultyKappa.score, `Harsanyi.DifficultyKappa.dividend, `Harsanyi.DifficultyKappa.referenceCoefficient, `Harsanyi.DifficultyKappa.normalizedCoefficient, `Harsanyi.DifficultyKappa.singletonGame, `Harsanyi.DifficultyKappa.singleton_dividend, `Harsanyi.DifficultyKappa.actual_references, `Harsanyi.DifficultyKappa.low_variation, `Harsanyi.DifficultyKappa.high_variation, `Harsanyi.DifficultyKappa.low_tail_bound, `Harsanyi.DifficultyKappa.high_tail_bound, `Harsanyi.DifficultyKappa.lowExpectedVariation, `Harsanyi.DifficultyKappa.highExpectedVariation, `Harsanyi.DifficultyKappa.actual_variation_bounds, `Harsanyi.DifficultyKappa.interactionKappa, `Harsanyi.DifficultyKappa.coefficientKappa, `Harsanyi.DifficultyKappa.actual_kappa_difference, `Harsanyi.DifficultyKappa.literalCoefficientKappa, `Harsanyi.DifficultyKappa.normalized_variation, `Harsanyi.DifficultyKappa.literal_coefficient_kappa_eq, `Harsanyi.DifficultyKappa.gaussian_relu_kappa_counterexample, `Harsanyi.DifficultyKappa.literal_gaussian_relu_kappa_counterexample, `Harsanyi.DifficultyCounting.superset_context_count, `Harsanyi.DifficultyCounting.superset_context_count_all, `Harsanyi.DifficultyCounting.context_double_sum, `Harsanyi.DifficultyCounting.context_grouped_sum, `Harsanyi.DifficultyCounting.context_grouped_average, `Harsanyi.DifficultyRegression.feature_opt_cramer, `Harsanyi.DifficultyRegression.half_loss_strict_iff, `PaperDifficulty.product_variance_counterexample, `PaperDifficulty.sourceTrigger, `PaperDifficulty.lowest_trigger_mean_counterexample, `PaperDifficulty.lowest_trigger_variance_counterexample, `PaperDifficulty.featureMeans, `PaperDifficulty.featureLaw, `PaperDifficulty.feature_model, `PaperDifficulty.optimalWeights, `PaperDifficulty.featureOpt_values, `PaperDifficulty.regression_step_three_counterexample, `PaperDifficulty.maskedPolynomial, `PaperDifficulty.maskedPolynomial_eq_unanimity, `PaperDifficulty.sourceMultiorderRHS, `PaperDifficulty.multiorder_index_counterexample, `PaperDifficulty.sourceCoefficientRHS, `PaperDifficulty.multiorder_coefficient_counterexample, `PaperDifficulty.source_dummy, `PaperDifficulty.pairDelta_eq_dividend_sum, `PaperDifficulty.multiorder_context_identity, `PaperDifficulty.multiorder_grouped_identity, `PaperDifficulty.maskedLowest, `PaperDifficulty.maskedLowest_eq, `PaperDifficulty.lowest_actual_dividend, `PaperDifficulty.appendix_lowest_actual_moments, `PaperDifficulty.feature_opt_cramer, `PaperDifficulty.half_loss_strict_iff, `PaperDifficulty.empty_interaction_moments, `Harsanyi.interaction_symmetry, `Harsanyi.interaction_context_difference, `Harsanyi.interaction_additive_dummy_nonempty, `Harsanyi.interaction_relabel, `Harsanyi.interaction_recursive, `Harsanyi.interaction_const, `Harsanyi.interaction_centered_nonempty, `Harsanyi.Robustness.multiOrderInteraction, `Harsanyi.Robustness.pairDelta, `Harsanyi.Robustness.contextAverage, `Harsanyi.higherMarginal_eq_sum_interaction, `Harsanyi.reconstruction, `Harsanyi.reconstruction_unique, `Harsanyi.interaction_add, `Harsanyi.interaction_unanimity] do
    let info ← getConstInfo name
    let signature ← ppExpr info.type
    let axioms ← Lean.collectAxioms name
    let deps := info.type.getUsedConstants ++ (info.value?.map Expr.getUsedConstants).getD #[]
    let kind := match info with | .thmInfo _ => "theorem" | .inductInfo _ => "inductive" | _ => "definition"
    liftM <| IO.println ("DYNAMICS_API:" ++ (Json.mkObj [
      ("name", toJson name.toString), ("signature", toJson signature.pretty),
      ("kind", toJson kind), ("axioms", toJson (axioms.map Name.toString)),
      ("dependencies", toJson (deps.map Name.toString))]).compress)
