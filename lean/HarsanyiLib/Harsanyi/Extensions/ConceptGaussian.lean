import Harsanyi.Extensions.GaussianRegression
import Mathlib.MeasureTheory.Measure.OpenPos

set_option maxHeartbeats 1600000
namespace Harsanyi.ConceptGaussian
open Finset MeasureTheory ProbabilityTheory Matrix
variable {Ω ι : Type*} [MeasurableSpace Ω] [Fintype ι] [DecidableEq ι]
variable (μ : Measure Ω) [IsProbabilityMeasure μ]

noncomputable def scaledVariance (σ2 : NNReal) (τ : ℝ) : NNReal :=
  ⟨(σ2 : ℝ) / τ ^ 2, div_nonneg σ2.coe_nonneg (sq_nonneg τ)⟩

/-- The source sign/tau map transforms the actual Gaussian law, not assumed moments. -/
theorem signed_scaled_law (ε : Ω → ℝ) (σ2 : NNReal) (s τ : ℝ)
    (hs : s ^ 2 = 1) (hm : Measurable ε)
    (hlaw : μ.map ε = gaussianReal 0 σ2) :
    μ.map (fun ω => s * ε ω / τ) = gaussianReal 0 (scaledVariance σ2 τ) := by
  let c2 : NNReal := ⟨(s / τ) ^ 2, sq_nonneg _⟩
  have hq : c2 * σ2 = scaledVariance σ2 τ := by
    apply NNReal.coe_injective
    simp only [NNReal.coe_mul, NNReal.coe_mk, c2, scaledVariance, div_pow, hs, one_div]
    ring
  have h : (fun ω => s * ε ω / τ) = (fun z : ℝ => (s / τ) * z) ∘ ε := by
    funext ω
    simp only [Function.comp_apply]
    ring
  rw [h, ← Measure.map_map (show Measurable (fun z : ℝ => (s / τ) * z) from measurable_const.mul measurable_id) hm, hlaw,
    gaussianReal_map_const_mul, mul_zero]
  convert congrArg (gaussianReal 0) hq using 1

/-- Exact lowest-polynomial moments, with untruncated Gaussian tails and moving signs. -/
theorem lowest_interaction_moments (ε : ι → Ω → ℝ) (σ2 : NNReal)
    (s : ι → ℝ) (τ U : ℝ) (hs : ∀ i, s i ^ 2 = 1)
    (hm : ∀ i, Measurable (ε i))
    (hlaw : ∀ i, μ.map (ε i) = gaussianReal 0 σ2)
    (hi : iIndepFun ε μ) :
    (∫ ω, U * ∏ i, (1 + s i * ε i ω / τ) ∂μ) = U ∧
      variance (fun ω => U * ∏ i, (1 + s i * ε i ω / τ)) μ =
        U ^ 2 * ((1 + (σ2 : ℝ) / τ ^ 2) ^ Fintype.card ι - 1) := by
  let η : ι → Ω → ℝ := fun i ω => s i * ε i ω / τ
  have hη : ∀ i, Measurable (η i) := by intro i; dsimp [η]; fun_prop
  have hl : ∀ i, μ.map (η i) = gaussianReal 0 (scaledVariance σ2 τ) :=
    fun i => signed_scaled_law μ (ε i) σ2 (s i) τ (hs i) (hm i) (hlaw i)
  have hind : iIndepFun η μ := by
    simpa only [η, Function.comp_def] using
      hi.comp (fun i z => s i * z / τ) (fun i => (measurable_const.mul measurable_id).div_const τ)
  have h := Harsanyi.TaylorMoments.gaussian_affine_product η (scaledVariance σ2 τ) hη hl hind
  constructor
  · rw [integral_const_mul]
    change U * (∫ ω, ∏ i, (1 + η i ω) ∂μ) = U
    rw [h.1, mul_one]
  · rw [variance_mul]
    change U ^ 2 * variance (fun ω => ∏ i, (1 + η i ω)) μ = _
    rw [h.2]
    rfl

/-- A real monomial's reference coefficient cancels the sign/tau normalization exactly. -/
theorem lowest_polynomial_identity (a τ : ℝ) (s ε : ι → ℝ)
    (hs : ∀ i, s i ^ 2 = 1) (hτ : τ ≠ 0) :
    (a * ∏ i, s i * τ) * (∏ i, (1 + s i * ε i / τ)) =
      a * ∏ i, (s i * τ + ε i) := by
  rw [mul_assoc, ← Finset.prod_mul_distrib]
  congr 1
  apply Finset.prod_congr rfl
  intro i _
  field_simp
  have hh : s i ^ 2 * ε i = ε i := by rw [hs i, one_mul]
  nlinarith only [hh]

/-- The source independent-feature loss is an actual expectation. -/
theorem feature_expected_loss (X : ι → Ω → ℝ) (a d : ι → ℝ)
    (hp : ∀ i, MemLp (X i) 2 μ)
    (ha : ∀ i, ∫ ω, X i ω ∂μ = a i)
    (hd : ∀ i, variance (X i) μ = d i)
    (hi : iIndepFun X μ) (y : ℝ) (w : ι → ℝ) :
    (∫ ω, (y - ∑ i, w i * X i ω) ^ 2 ∂μ) =
      NoisyRegression.featureLoss a d y w := by
  let ε : ι → Ω → ℝ := fun i ω => X i ω - a i
  have hpε : ∀ i, MemLp (ε i) 2 μ := fun i => (hp i).sub (memLp_const (a i))
  have he : ∀ i, ∫ ω, ε i ω ∂μ = 0 := by
    intro i
    dsimp [ε]
    rw [integral_sub ((hp i).integrable (by norm_num)) (integrable_const _)]
    simp [ha]
  have hv : ∀ i, variance (ε i) μ = d i := by
    intro i
    dsimp [ε]
    rw [variance_sub_const (hp i).aestronglyMeasurable, hd]
  have hind : iIndepFun ε μ := by
    simpa only [ε, Function.comp_def] using
      hi.comp (fun i z => z - a i) (fun _ => measurable_id.sub measurable_const)
  have hf : (fun ω => y - ∑ i, w i * X i ω) =
      (fun ω => (y - ∑ i, a i * w i) + ∑ i, (-w i) * ε i ω) := by
    funext ω
    simp only [ε, mul_sub, neg_mul, sum_sub_distrib]
    have hm : (∑ i, w i * a i) = ∑ i, a i * w i := by apply sum_congr rfl; intro i _; ring
    simp only [sum_neg_distrib, hm]
    ring
  simp_rw [congrFun hf]
  rw [GaussianRegression.independent_residual μ ε d hpε he hv hind]
  simp [NoisyRegression.featureLoss, mul_comm]

noncomputable def featureMatrix (a d : ι → ℝ) : Matrix ι ι ℝ :=
  diagonal d + vecMulVec a a

/-- The original regression hypothesis only needs pairwise independence. -/
theorem pairwise_feature_expected_loss (X : ι → Ω → ℝ) (a d : ι → ℝ)
    (hp : ∀ i, MemLp (X i) 2 μ)
    (ha : ∀ i, ∫ ω, X i ω ∂μ = a i)
    (hd : ∀ i, variance (X i) μ = d i)
    (hi : Pairwise fun i j => IndepFun (X i) (X j) μ) (y : ℝ) (w : ι → ℝ) :
    (∫ ω, (y - ∑ i, w i * X i ω) ^ 2 ∂μ) =
      NoisyRegression.featureLoss a d y w := by
  let F : ι → Ω → ℝ := fun i ω => w i * X i ω
  let Z : Ω → ℝ := fun ω => ∑ i, F i ω
  have hpF : ∀ i, MemLp (F i) 2 μ := fun i => (hp i).const_mul (w i)
  have hpZ : MemLp Z 2 μ := by
    simpa only [Z, Finset.sum_apply] using memLp_finset_sum univ (fun i _ => hpF i)
  have hmean : (∫ ω, Z ω ∂μ) = ∑ i, w i * a i := by
    rw [show Z = fun ω => ∑ i, F i ω from rfl,
      integral_finset_sum univ (fun i _ => (hpF i).integrable (by norm_num))]
    simp only [F, integral_const_mul, ha]
  have hpair : Set.Pairwise (↑(univ : Finset ι) : Set ι)
      (fun i j => IndepFun (F i) (F j) μ) := by
    intro i _ j _ hij
    simpa only [F, Function.comp_def] using
      (hi hij).comp (measurable_const.mul measurable_id) (measurable_const.mul measurable_id)
  have hv : variance Z μ = ∑ i, w i ^ 2 * d i := by
    have h := IndepFun.variance_sum (fun i (_ : i ∈ univ) => hpF i) hpair
    have hz : (∑ i, F i) = Z := by funext ω; simp [Z]
    rw [← hz]
    simpa only [F, variance_mul, hd] using h
  have hpR : MemLp (fun ω => y - Z ω) 2 μ := (memLp_const y).sub hpZ
  have hRmean : (∫ ω, y - Z ω ∂μ) = y - ∑ i, w i * a i := by
    rw [integral_sub (integrable_const _) (hpZ.integrable (by norm_num)), integral_const, hmean]
    simp
  have hRvar := variance_eq_sub hpR
  rw [variance_const_sub hpZ.aestronglyMeasurable, hv, hRmean] at hRvar
  have hcomm : (∑ i, w i * a i) = ∑ i, a i * w i := by
    apply sum_congr rfl; intro i _; ring
  change (∫ ω, (y - Z ω) ^ 2 ∂μ) = _
  change (∑ i, w i ^ 2 * d i) = (∫ ω, (y - Z ω) ^ 2 ∂μ) -
    (y - ∑ i, w i * a i) ^ 2 at hRvar
  unfold NoisyRegression.featureLoss
  rw [hcomm] at hRvar
  have hsum : (∑ i, w i ^ 2 * d i) = ∑ i, d i * w i ^ 2 := by
    apply sum_congr rfl; intro i _; ring
  rw [hsum] at hRvar
  linarith

noncomputable def featureOpt (a d : ι → ℝ) (y : ℝ) : ι → ℝ :=
  fun i => (y / (1 + ∑ j, a j ^ 2 / d j)) * (a i / d i)

theorem featureMatrix_posDef (a d : ι → ℝ) (hd : ∀ i, 0 < d i) :
    (featureMatrix a d).PosDef := by
  apply (Matrix.posDef_diagonal_iff.mpr hd).add_posSemidef
  simpa only [star_trivial] using Matrix.posSemidef_vecMulVec_self_star a

theorem featureLoss_quadratic (a d : ι → ℝ) (y : ℝ) (w : ι → ℝ) :
    NoisyRegression.featureLoss a d y w = y ^ 2 +
      NoisyRegression.quadraticLoss (featureMatrix a d) (fun i => y * a i) w := by
  unfold NoisyRegression.featureLoss NoisyRegression.quadraticLoss featureMatrix
  simp only [add_mulVec, dotProduct_add]
  have hd : w ⬝ᵥ (diagonal d *ᵥ w) = ∑ i, d i * w i ^ 2 := by
    simp only [dotProduct, mulVec_diagonal]
    apply sum_congr rfl
    intro i _
    ring
  have ha : w ⬝ᵥ (vecMulVec a a *ᵥ w) = (a ⬝ᵥ w) ^ 2 := by
    rw [vecMulVec_mulVec]
    change w ⬝ᵥ (fun i => a i * (a ⬝ᵥ w)) = _
    calc
      _ = (w ⬝ᵥ a) * (a ⬝ᵥ w) := by
        simp only [dotProduct, Finset.sum_mul]
        apply sum_congr rfl
        intro i _
        ring
      _ = _ := by rw [dotProduct_comm w a]; ring
  have hy : (fun i => y * a i) ⬝ᵥ w = y * (a ⬝ᵥ w) := by simp only [dotProduct, mul_sum, mul_assoc]
  rw [hd, ha, hy]
  change (y - a ⬝ᵥ w) ^ 2 + _ = _
  ring

theorem featureOpt_normal (a d : ι → ℝ) (y : ℝ) (hd : ∀ i, 0 < d i) :
    featureMatrix a d *ᵥ featureOpt a d y = fun i => y * a i := by
  let t := ∑ j, a j ^ 2 / d j
  have ht : 0 ≤ t := sum_nonneg fun i _ => div_nonneg (sq_nonneg _) (le_of_lt (hd i))
  have hden : 1 + t ≠ 0 := ne_of_gt (by linarith)
  have hsum : a ⬝ᵥ featureOpt a d y = y / (1 + t) * t := by
    change (∑ i, a i * (y / (1 + t) * (a i / d i))) = _
    rw [mul_sum]
    apply sum_congr rfl
    intro i _
    ring
  funext i
  simp only [featureMatrix, add_mulVec, mulVec_diagonal, vecMulVec_mulVec, Pi.add_apply]
  rw [hsum]
  change d i * (y / (1 + t) * (a i / d i)) + a i * (y / (1 + t) * t) = _
  field_simp [ne_of_gt (hd i), hden]

theorem featureOpt_unique_min (a d : ι → ℝ) (y : ℝ) (hd : ∀ i, 0 < d i) :
    ∀ w, w ≠ featureOpt a d y →
      NoisyRegression.featureLoss a d y (featureOpt a d y) <
        NoisyRegression.featureLoss a d y w := by
  intro w hw
  simpa only [featureLoss_quadratic, add_lt_add_iff_left] using
    NoisyRegression.quadratic_unique_min (featureMatrix a d) (featureMatrix_posDef a d hd)
      (fun i => y * a i) (featureOpt a d y) (featureOpt_normal a d y hd) w hw

/-- The original expected feature loss has this unique global optimum. -/
theorem feature_expected_unique_min (X : ι → Ω → ℝ) (a d : ι → ℝ)
    (hp : ∀ i, MemLp (X i) 2 μ) (ha : ∀ i, ∫ ω, X i ω ∂μ = a i)
    (hv : ∀ i, variance (X i) μ = d i) (hi : iIndepFun X μ)
    (hd : ∀ i, 0 < d i) (y : ℝ) :
    ∀ w, w ≠ featureOpt a d y →
      (∫ ω, (y - ∑ i, featureOpt a d y i * X i ω) ^ 2 ∂μ) <
        (∫ ω, (y - ∑ i, w i * X i ω) ^ 2 ∂μ) := by
  intro w hw
  simp_rw [feature_expected_loss μ X a d hp ha hv hi]
  exact featureOpt_unique_min a d y hd w hw

/-- Actual loss and unique minimizer under the source pairwise-independence assumption. -/
theorem pairwise_feature_expected_unique_min (X : ι → Ω → ℝ) (a d : ι → ℝ)
    (hp : ∀ i, MemLp (X i) 2 μ) (ha : ∀ i, ∫ ω, X i ω ∂μ = a i)
    (hv : ∀ i, variance (X i) μ = d i)
    (hi : Pairwise fun i j => IndepFun (X i) (X j) μ)
    (hd : ∀ i, 0 < d i) (y : ℝ) :
    ∀ w, w ≠ featureOpt a d y →
      (∫ ω, (y - ∑ i, featureOpt a d y i * X i ω) ^ 2 ∂μ) <
        (∫ ω, (y - ∑ i, w i * X i ω) ^ 2 ∂μ) := by
  intro w hw
  simp_rw [pairwise_feature_expected_loss μ X a d hp ha hv hi]
  exact featureOpt_unique_min a d y hd w hw

/-- All moments are discharged from the actual Gaussian map-law. -/
theorem gaussian_memLp_any (X : Ω → ℝ) (a : ℝ) (q : NNReal)
    (p : ENNReal) (hp : p ≠ ⊤) (hm : Measurable X)
    (hl : μ.map X = gaussianReal a q) : MemLp X p μ := by
  have hx : MemLp id p (μ.map X) := by rw [hl]; exact memLp_id_gaussianReal' p hp
  simpa only [Function.comp_def, id_eq] using hx.comp_measurePreserving ⟨hm, hl ▸ rfl⟩

theorem gaussian_feature_moments (X : Ω → ℝ) (a : ℝ) (q : NNReal)
    (hm : Measurable X) (hl : μ.map X = gaussianReal a q) :
    MemLp X 2 μ ∧ (∫ ω, X ω ∂μ) = a ∧ variance X μ = q := by
  refine ⟨gaussian_memLp_any μ X a q 2 (by norm_num) hm hl, ?_, ?_⟩
  · calc
      (∫ ω, X ω ∂μ) = ∫ z, z ∂μ.map X := by
        symm
        simpa only [id_eq] using integral_map hm.aemeasurable
          (aestronglyMeasurable_id : AEStronglyMeasurable (id : ℝ → ℝ) (μ.map X))
      _ = a := by rw [hl]; exact integral_id_gaussianReal
  · rw [← variance_id_map hm.aemeasurable, hl]
    exact variance_id_gaussianReal

theorem gaussian_feature_unique_min (X : ι → Ω → ℝ) (a : ι → ℝ)
    (q : ι → NNReal) (hm : ∀ i, Measurable (X i))
    (hl : ∀ i, μ.map (X i) = gaussianReal (a i) (q i))
    (hi : iIndepFun X μ) (hq : ∀ i, 0 < (q i : ℝ)) (y : ℝ) :
    ∀ w, w ≠ featureOpt a (fun i => (q i : ℝ)) y →
      (∫ ω, (y - ∑ i, featureOpt a (fun j => (q j : ℝ)) y i * X i ω) ^ 2 ∂μ) <
        (∫ ω, (y - ∑ i, w i * X i ω) ^ 2 ∂μ) := by
  have h := fun i => gaussian_feature_moments μ (X i) (a i) (q i) (hm i) (hl i)
  exact feature_expected_unique_min μ X a (fun i => (q i : ℝ))
    (fun i => (h i).1) (fun i => (h i).2.1) (fun i => (h i).2.2) hi hq y

/-- Arbitrary integer folded powers of a Gaussian are L2, without tail truncation. -/
theorem folded_power_memLp (X : Ω → ℝ) (a : ℝ) (q : NNReal) (k : ℕ)
    (hm : Measurable X) (hl : μ.map X = gaussianReal a q) :
    MemLp (fun ω => |X ω| ^ k) 2 μ := by
  by_cases hk : k = 0
  · simp only [hk, pow_zero]
    exact memLp_const 1
  have hx := gaussian_memLp_any μ X a q ((2 : ENNReal) * (k : ENNReal)) (ENNReal.mul_ne_top (by norm_num) (by simp)) hm hl
  have hp := hx.norm_rpow_div (k : ENNReal)
  have hkn : (k : ENNReal) ≠ 0 := by exact_mod_cast hk
  simpa only [ENNReal.toReal_natCast, Real.rpow_natCast, Real.norm_eq_abs,
    ENNReal.mul_div_cancel_right hkn (by simp)] using hp

/-- Exact moments of the original absolute trigger, with all Gaussian power premises discharged. -/
theorem folded_product_moments (X : ι → Ω → ℝ) (a : ι → ℝ)
    (q : ι → NNReal) (k : ι → ℕ) (hm : ∀ i, Measurable (X i))
    (hl : ∀ i, μ.map (X i) = gaussianReal (a i) (q i)) (hi : iIndepFun X μ) :
    (∫ ω, ∏ i, |X i ω| ^ k i ∂μ) = ∏ i, (∫ ω, |X i ω| ^ k i ∂μ) ∧
      variance (fun ω => ∏ i, |X i ω| ^ k i) μ =
        (∏ i, ((∫ ω, |X i ω| ^ k i ∂μ) ^ 2 + variance (fun ω => |X i ω| ^ k i) μ)) -
        (∏ i, (∫ ω, |X i ω| ^ k i ∂μ) ^ 2) := by
  let F : ι → Ω → ℝ := fun i ω => |X i ω| ^ k i
  have hp : ∀ i, MemLp (F i) 2 μ :=
    fun i => folded_power_memLp μ (X i) (a i) (q i) (k i) (hm i) (hl i)
  have hf : ∀ i, Measurable (F i) := fun i => (hm i).abs.pow_const (k i)
  have hind : iIndepFun F μ := by
    simpa only [F, Function.comp_def] using
      hi.comp (fun i z => |z| ^ k i) (fun i => measurable_id.abs.pow_const (k i))
  exact ⟨TaylorMoments.product_mean hind (fun i => (hf i).aestronglyMeasurable),
    TaylorMoments.product_variance hind (fun i => (hf i).aestronglyMeasurable)
      hp (TaylorMoments.product_memLp hind hf hp)⟩


theorem folded_gaussian_variance_pos (a : ℝ) (q : NNReal) (hq : q ≠ 0) (k : ℕ) (hk : k ≠ 0) :
    0 < variance (fun z : ℝ => |z| ^ k) (gaussianReal a q) := by
  let μ := gaussianReal a q
  let f : ℝ → ℝ := fun z => |z| ^ k
  have hp : MemLp f 2 μ := folded_power_memLp μ id a q k measurable_id (by simp [μ])
  have hm : Measurable f := measurable_id.abs.pow_const k
  haveI : NoAtoms μ := noAtoms_gaussianReal hq
  apply lt_of_le_of_ne (variance_nonneg f μ)
  intro hz
  have he : evariance f μ = 0 := by
    rw [← hp.ofReal_variance_eq, ← hz]
    simp
  have hae : f =ᵐ[μ] fun _ => ∫ z, f z ∂μ := (evariance_eq_zero_iff hm.aemeasurable).mp he
  obtain ⟨z0, hz0⟩ := hae.exists
  have hfinite : ∀ᵐ z ∂μ, z ∈ ({z0, -z0} : Set ℝ) := by
    filter_upwards [hae] with z hz
    have habs : |z| = |z0| := (pow_left_inj₀ (abs_nonneg _) (abs_nonneg _) hk).mp (hz.trans hz0.symm)
    rcases (abs_eq_abs.mp habs) with h | h
    · simp [h]
    · simp [h]
  have hnot : ∀ᵐ z ∂μ, z ∉ ({z0, -z0} : Set ℝ) :=
    ((Set.finite_singleton (-z0)).insert z0).countable.ae_notMem μ
  have hfalse : ∀ᵐ z ∂μ, False := hfinite.and hnot |>.mono (fun _ h => h.2 h.1)
  exact hfalse.exists.choose_spec

lemma reflection_power_bound (x : ℝ) (k : ℕ) : 2 ≤ x ^ k + (2 - x) ^ k := by
  let t := x - 1
  have heq : x ^ k + (2 - x) ^ k =
      ∑ i ∈ range (k + 1), ((t ^ i + (-t) ^ i) * (k.choose i : ℝ)) := by
    have h1 : x = t + 1 := by dsimp [t]; ring
    have h2 : 2 - x = (-t) + 1 := by dsimp [t]; ring
    rw [h2, h1, add_pow, add_pow, ← sum_add_distrib]
    apply sum_congr rfl
    intro i _
    simp only [one_pow, mul_one]
    ring
  rw [heq, sum_range_succ']
  have hn : 0 ≤ ∑ i ∈ range k, (t ^ (i + 1) + (-t) ^ (i + 1)) * (k.choose (i + 1) : ℝ) := by
    apply sum_nonneg
    intro i _
    apply mul_nonneg _ (Nat.cast_nonneg _)
    rcases Nat.even_or_odd (i + 1) with h | h
    · rw [h.neg_pow]
      exact add_nonneg (h.pow_nonneg _) (h.pow_nonneg _)
    · rw [h.neg_pow]
      simp
  norm_num only [pow_zero, Nat.choose_zero_right, Nat.cast_one, mul_one]
  linarith

lemma signed_power_memLp (μ : Measure ℝ) [IsProbabilityMeasure μ]
    (a : ℝ) (q : NNReal) (hl : μ = gaussianReal a q) (k : ℕ) :
    MemLp (fun x : ℝ => x ^ k) 2 μ := by
  have h := folded_power_memLp μ id a q k measurable_id (by simpa using hl)
  apply (memLp_norm_iff (measurable_id.pow_const k).aestronglyMeasurable).mp
  simpa only [Real.norm_eq_abs, abs_pow] using h

theorem signed_gaussian_moment_ge_one (q : NNReal) (k : ℕ) : 1 ≤ ∫ x : ℝ, x ^ k ∂gaussianReal 1 q := by
  let μ := gaussianReal 1 q
  have hp := signed_power_memLp μ 1 q rfl k
  have hint := hp.integrable (by norm_num)
  have hm : Measurable (fun x : ℝ => 2 - x) := measurable_const.sub measurable_id
  have hl : μ.map (fun x : ℝ => 2 - x) = μ := by
    dsimp [μ]
    rw [gaussianReal_map_const_sub]
    norm_num
  have heq : (∫ x : ℝ, (2 - x) ^ k ∂μ) = ∫ x : ℝ, x ^ k ∂μ := by
    calc
      _ = ∫ x : ℝ, x ^ k ∂μ.map (fun x : ℝ => 2 - x) := by
        symm
        simpa only [id_eq] using integral_map_of_stronglyMeasurable hm (measurable_id.pow_const k).stronglyMeasurable
      _ = _ := by rw [hl]
  have hr : Integrable (fun x : ℝ => (2 - x) ^ k) μ := by
    have hmap : Integrable (fun x : ℝ => x ^ k) (μ.map (fun x : ℝ => 2 - x)) := by rw [hl]; exact hint
    simpa only [Function.comp_def, id_eq] using
      (integrable_map_measure (measurable_id.pow_const k).aestronglyMeasurable hm.aemeasurable).mp hmap
  have hbound : (∫ x : ℝ, (2 : ℝ) ∂μ) ≤ ∫ x : ℝ, x ^ k + (2 - x) ^ k ∂μ :=
    integral_mono (integrable_const _) (hint.add hr) (fun x => reflection_power_bound x k)
  rw [integral_add hint hr, heq] at hbound
  simp only [integral_const, measureReal_univ_eq_one, smul_eq_mul, one_mul] at hbound
  linarith


theorem unit_gaussian_power_bounds (X : Ω → ℝ) (q : NNReal) (k : ℕ) (hm : Measurable X)
    (hl : μ.map X = gaussianReal 1 q) :
    1 ≤ (∫ ω, X ω ^ k ∂μ) ∧ (∫ ω, X ω ^ k ∂μ) ≤ ∫ ω, |X ω| ^ k ∂μ := by
  have hs : MemLp (fun ω => X ω ^ k) 2 μ := by
    apply (memLp_norm_iff (hm.pow_const k).aestronglyMeasurable).mp
    simpa only [Real.norm_eq_abs, abs_pow] using folded_power_memLp μ X 1 q k hm hl
  constructor
  · have hi : (∫ ω, X ω ^ k ∂μ) = ∫ z : ℝ, z ^ k ∂gaussianReal 1 q := by
      calc
        _ = ∫ z : ℝ, z ^ k ∂μ.map X := by
          symm
          simpa only [id_eq] using integral_map_of_stronglyMeasurable hm (measurable_id.pow_const k).stronglyMeasurable
        _ = _ := by rw [hl]
    rw [hi]
    exact signed_gaussian_moment_ge_one q k
  · apply integral_mono (hs.integrable (by norm_num))
      ((folded_power_memLp μ X 1 q k hm hl).integrable (by norm_num))
    intro ω
    change X ω ^ k ≤ |X ω| ^ k
    rw [← abs_pow]
    exact le_abs_self _

theorem folded_map_variance_pos (X : Ω → ℝ) (a : ℝ) (q : NNReal) (k : ℕ) (hq : q ≠ 0) (hk : k ≠ 0)
    (hm : Measurable X) (hl : μ.map X = gaussianReal a q) :
    0 < variance (fun ω => |X ω| ^ k) μ := by
  have hmp : MeasurePreserving X μ (gaussianReal a q) := ⟨hm, hl⟩
  have heq : variance (fun ω => |X ω| ^ k) μ =
      variance (fun z : ℝ => |z| ^ k) (gaussianReal a q) := by
    simpa only [id_eq] using hmp.variance_fun_comp (measurable_id.abs.pow_const k).aemeasurable
  rw [heq]
  exact folded_gaussian_variance_pos a q hq k hk


lemma folded_subset_moments (X : ι → Ω → ℝ) (q : ι → NNReal) (k : ι → ℕ)
    (hm : ∀ i, Measurable (X i)) (hl : ∀ i, μ.map (X i) = gaussianReal 1 (q i))
    (hi : iIndepFun X μ) (T : Finset ι) :
    (∫ ω, ∏ i ∈ T, |X i ω| ^ k i ∂μ) = ∏ i ∈ T, ∫ ω, |X i ω| ^ k i ∂μ ∧
    variance (fun ω => ∏ i ∈ T, |X i ω| ^ k i) μ =
      (∏ i ∈ T, ((∫ ω, |X i ω| ^ k i ∂μ) ^ 2 + variance (fun ω => |X i ω| ^ k i) μ)) -
      (∏ i ∈ T, (∫ ω, |X i ω| ^ k i ∂μ) ^ 2) := by
  letI : Fintype T := Finset.fintypeCoeSort T
  have h := folded_product_moments μ (fun i : T => X i) (fun _ => 1) (fun i : T => q i)
    (fun i : T => k i) (fun i => hm i) (fun i => hl i) (hi.precomp Subtype.val_injective)
  have hprod (f : ι → ℝ) : (∏ i : T, f i) = ∏ i ∈ T, f i := Finset.prod_coe_sort T f
  have hf : (fun ω => ∏ i : T, |X i ω| ^ k i) =
      (fun ω => ∏ i ∈ T, |X i ω| ^ k i) := by
    funext ω
    exact hprod (fun i => |X i ω| ^ k i)
  rw [hf] at h
  have hmprod := hprod (fun i => ∫ ω, |X i ω| ^ k i ∂μ)
  have hsprod := hprod (fun i => (∫ ω, |X i ω| ^ k i ∂μ) ^ 2 + variance (fun ω => |X i ω| ^ k i) μ)
  have hvprod := hprod (fun i => (∫ ω, |X i ω| ^ k i ∂μ) ^ 2)
  rw [hmprod, hsprod, hvprod] at h
  exact h

lemma folded_subset_positive (X : ι → Ω → ℝ) (q : ι → NNReal) (k : ι → ℕ)
    (hm : ∀ i, Measurable (X i)) (hl : ∀ i, μ.map (X i) = gaussianReal 1 (q i))
    (hi : iIndepFun X μ) (hq : ∀ i, q i ≠ 0) (hk : ∀ i, k i ≠ 0)
    (T : Finset ι) (hT : T.Nonempty) :
    1 ≤ (∫ ω, ∏ i ∈ T, |X i ω| ^ k i ∂μ) ∧
      0 < variance (fun ω => ∏ i ∈ T, |X i ω| ^ k i) μ := by
  have hmean : ∀ i, 1 ≤ ∫ ω, |X i ω| ^ k i ∂μ :=
    fun i => (unit_gaussian_power_bounds μ (X i) (q i) (k i) (hm i) (hl i)).1.trans
      (unit_gaussian_power_bounds μ (X i) (q i) (k i) (hm i) (hl i)).2
  have hvar : ∀ i, 0 < variance (fun ω => |X i ω| ^ k i) μ :=
    fun i => folded_map_variance_pos μ (X i) 1 (q i) (k i) (hq i) (hk i) (hm i) (hl i)
  have h := folded_subset_moments μ X q k hm hl hi T
  constructor
  · rw [h.1]
    calc
      1 = ∏ i ∈ T, (1 : ℝ) := by simp
      _ ≤ _ := Finset.prod_le_prod (fun _ _ => zero_le_one) (fun i _ => hmean i)
  · rw [h.2]
    apply sub_pos.mpr
    apply Finset.prod_lt_prod_of_nonempty _ _ hT
    · intro i _
      exact sq_pos_of_pos (lt_of_lt_of_le zero_lt_one (hmean i))
    · intro i _
      linarith [hvar i]

lemma folded_disjoint_moments (X : ι → Ω → ℝ) (q : ι → NNReal) (k : ι → ℕ)
    (hm : ∀ i, Measurable (X i)) (hl : ∀ i, μ.map (X i) = gaussianReal 1 (q i))
    (hi : iIndepFun X μ) (A B : Finset ι) (hab : Disjoint A B) :
    let JA := fun ω => ∏ i ∈ A, |X i ω| ^ k i
    let JB := fun ω => ∏ i ∈ B, |X i ω| ^ k i
    let JAB := fun ω => ∏ i ∈ A ∪ B, |X i ω| ^ k i
    (∫ ω, JAB ω ∂μ) = (∫ ω, JA ω ∂μ) * (∫ ω, JB ω ∂μ) ∧
    variance JAB μ = variance JA μ * ((∫ ω, JB ω ∂μ) ^ 2 + variance JB μ) +
      (∫ ω, JA ω ∂μ) ^ 2 * variance JB μ := by
  dsimp only
  have h1 := folded_subset_moments μ X q k hm hl hi A
  have h2 := folded_subset_moments μ X q k hm hl hi B
  have h12 := folded_subset_moments μ X q k hm hl hi (A ∪ B)
  constructor
  · rw [h12.1, h1.1, h2.1, Finset.prod_union hab]
  · rw [h12.2, h1.2, h2.2, h1.1, h2.1, Finset.prod_union hab, Finset.prod_union hab]
    simp_rw [← Finset.prod_pow]
    ring

lemma product_growth_bounds (ma mb va vb p : ℝ)
    (hma : 1 ≤ ma) (hmb : p ≤ mb) (hp : 1 ≤ p) (hva : 0 < va) (hvb : 0 < vb) :
    let v := va * (mb ^ 2 + vb) + ma ^ 2 * vb
    v / va > p ^ 2 ∧ (ma * mb / v) / (ma / va) < 1 / p := by
  have hmap : 0 < ma := lt_of_lt_of_le zero_lt_one hma
  have hpp : 0 < p := lt_of_lt_of_le zero_lt_one hp
  have hmbp : 0 < mb := hpp.trans_le hmb
  have hv : 0 < va * (mb ^ 2 + vb) + ma ^ 2 * vb := by positivity
  have hsq : p ^ 2 ≤ mb ^ 2 := sq_le_sq₀ hpp.le hmbp.le |>.mpr hmb
  have hterm : va * p ^ 2 < va * (mb ^ 2 + vb) + ma ^ 2 * vb := by
    have hbase := mul_le_mul_of_nonneg_left hsq hva.le
    have hstrict : 0 < va * vb := mul_pos hva hvb
    have hn : 0 ≤ ma ^ 2 * vb := mul_nonneg (sq_nonneg _) hvb.le
    nlinarith
  dsimp only
  constructor
  · exact (lt_div_iff₀ hva).mpr (by simpa [mul_comm] using hterm)
  · have hratio : (ma * mb / (va * (mb ^ 2 + vb) + ma ^ 2 * vb)) / (ma / va) =
        mb * va / (va * (mb ^ 2 + vb) + ma ^ 2 * vb) := by field_simp
    rw [hratio]
    apply (div_lt_div_iff₀ hv hpp).mpr
    have hbb : mb * p ≤ mb ^ 2 := by nlinarith [mul_le_mul_of_nonneg_left hmb hmbp.le]
    have hbase := mul_le_mul_of_nonneg_left hbb hva.le
    have hstrict : 0 < va * vb := mul_pos hva hvb
    have hn : 0 ≤ ma ^ 2 * vb := mul_nonneg (sq_nonneg _) hvb.le
    nlinarith

lemma folded_subset_growth (X : ι → Ω → ℝ) (q : ι → NNReal) (k : ι → ℕ)
    (hm : ∀ i, Measurable (X i)) (hl : ∀ i, μ.map (X i) = gaussianReal 1 (q i))
    (hi : iIndepFun X μ) (hq : ∀ i, q i ≠ 0) (hk : ∀ i, k i ≠ 0)
    (A B : Finset ι) (hA : A.Nonempty) (hB : B.Nonempty) (hab : Disjoint A B) :
    let JA := fun ω => ∏ i ∈ A, |X i ω| ^ k i
    let JAB := fun ω => ∏ i ∈ A ∪ B, |X i ω| ^ k i
    let p := ∏ i ∈ B, ∫ ω, X i ω ^ k i ∂μ
    variance JAB μ / variance JA μ > p ^ 2 ∧ 1 ≤ p ^ 2 ∧
      ((|∫ ω, JAB ω ∂μ| / variance JAB μ) / (|∫ ω, JA ω ∂μ| / variance JA μ)) < 1 / p ∧
      1 / p ≤ 1 := by
  let JA := fun ω => ∏ i ∈ A, |X i ω| ^ k i
  let JB := fun ω => ∏ i ∈ B, |X i ω| ^ k i
  let JAB := fun ω => ∏ i ∈ A ∪ B, |X i ω| ^ k i
  let p := ∏ i ∈ B, ∫ ω, X i ω ^ k i ∂μ
  have hma := folded_subset_positive μ X q k hm hl hi hq hk A hA
  have hmb := folded_subset_positive μ X q k hm hl hi hq hk B hB
  have hb := folded_subset_moments μ X q k hm hl hi B
  have hp : 1 ≤ p := by
    calc
      1 = ∏ i ∈ B, (1 : ℝ) := by simp
      _ ≤ p := Finset.prod_le_prod (fun _ _ => zero_le_one)
        (fun i _ => (unit_gaussian_power_bounds μ (X i) (q i) (k i) (hm i) (hl i)).1)
  have hpmb : p ≤ ∫ ω, JB ω ∂μ := by
    rw [show (∫ ω, JB ω ∂μ) = ∏ i ∈ B, ∫ ω, |X i ω| ^ k i ∂μ from hb.1]
    apply Finset.prod_le_prod
    · intro i _
      exact zero_le_one.trans (unit_gaussian_power_bounds μ (X i) (q i) (k i) (hm i) (hl i)).1
    · intro i _
      exact (unit_gaussian_power_bounds μ (X i) (q i) (k i) (hm i) (hl i)).2
  have hd := folded_disjoint_moments μ X q k hm hl hi A B hab
  have hg := product_growth_bounds (∫ ω, JA ω ∂μ) (∫ ω, JB ω ∂μ)
    (variance JA μ) (variance JB μ) p hma.1 hpmb hp hma.2 hmb.2
  dsimp only at hd hg ⊢
  refine ⟨?_, ?_, ?_, ?_⟩
  · rw [hd.2]
    exact hg.1
  · nlinarith [hp]
  · have haa : |∫ ω, JA ω ∂μ| = ∫ ω, JA ω ∂μ := abs_of_nonneg (zero_le_one.trans hma.1)
    have habs : |∫ ω, JAB ω ∂μ| = ∫ ω, JAB ω ∂μ := by
      rw [hd.1]
      exact abs_of_nonneg (mul_nonneg (zero_le_one.trans hma.1) (zero_le_one.trans hmb.1))
    rw [habs, haa, hd.1, hd.2]
    exact hg.2
  · exact (div_le_one (lt_of_lt_of_le zero_lt_one hp)).mpr hp


theorem folded_first_moment_gt_one (q : NNReal) (hq : q ≠ 0) :
    1 < ∫ z : ℝ, |z| ∂gaussianReal 1 q := by
  let μ := gaussianReal 1 q
  have hid : Integrable (id : ℝ → ℝ) μ := (memLp_id_gaussianReal (μ := 1) (v := q) 2).integrable (by norm_num)
  have habs : Integrable (fun z : ℝ => |z|) μ := hid.norm
  have hint : Integrable (fun z : ℝ => |z| - z) μ := habs.sub hid
  have hn : ∀ z : ℝ, 0 ≤ |z| - z := fun z => sub_nonneg.mpr (le_abs_self _)
  have hpos : 0 < ∫ z : ℝ, |z| - z ∂μ := by
    apply lt_of_le_of_ne (integral_nonneg hn)
    intro hz
    have hae : (fun z : ℝ => |z| - z) =ᵐ[μ] 0 :=
      (integral_eq_zero_iff_of_nonneg hn hint).mp hz.symm
    have hv : (fun z : ℝ => |z| - z) =ᵐ[volume] 0 :=
      (gaussianReal_absolutelyContinuous' 1 hq).ae_eq hae
    have heq : (fun z : ℝ => |z| - z) = 0 := MeasureTheory.Measure.eq_of_ae_eq hv (continuous_abs.sub continuous_id) continuous_const
    have := congrFun heq (-1)
    norm_num at this
  have his : Integrable (fun z : ℝ => z) μ := hid
  rw [integral_sub habs his] at hpos
  have hmean : (∫ z : ℝ, z ∂μ) = 1 := integral_id_gaussianReal
  rw [hmean] at hpos
  linarith

end Harsanyi.ConceptGaussian
