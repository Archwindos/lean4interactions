import Harsanyi.Extensions.DecoderLayerMoments

namespace Harsanyi.Frequency
open Finset MeasureTheory ProbabilityTheory
open scoped BigOperators

noncomputable def quarterGaussianLaw : Measure ℝ := gaussianReal 0 (1/4 : NNReal)
instance : IsProbabilityMeasure quarterGaussianLaw := by unfold quarterGaussianLaw; infer_instance
noncomputable def quarterGaussianLayers (L : ℕ) : Measure (Fin L → ℝ) :=
  Measure.pi (fun _ => quarterGaussianLaw)

instance (L : ℕ) : IsProbabilityMeasure (quarterGaussianLayers L) := by
  unfold quarterGaussianLayers quarterGaussianLaw
  infer_instance

theorem quarter_gaussian_coordinate_law (l : Fin L) :
    (quarterGaussianLayers L).map (fun ω => ω l) = quarterGaussianLaw :=
  (measurePreserving_eval (fun _ : Fin L => quarterGaussianLaw) l).map_eq

theorem quarter_gaussian_independent (L : ℕ) :
    iIndepFun (fun l : Fin L => fun ω : Fin L → ℝ => ω l) (quarterGaussianLayers L) := by
  exact iIndepFun_pi (fun _ : Fin L => measurable_id.aemeasurable)

theorem actual_unit_kernel_gaussian_depth_moment
    {M N : ℕ} [NeZero M] [NeZero N] (L : ℕ) (u : ZMod M) (v : ZMod N) :
    (∫ ω,Complex.normSq (∏ l : Fin L,
      randomKernelResponse (fun _ : Fin 1 × Fin 1 => fun ω : Fin L → ℝ => ω l) u v ω)
        ∂quarterGaussianLayers L) = (1/4 : ℝ)^L := by
  have hr (l : Fin L) (ω : Fin L → ℝ) :
      randomKernelResponse (fun _ : Fin 1 × Fin 1 => fun ω : Fin L → ℝ => ω l) u v ω =
        (ω l : ℂ) := by
    simp [randomKernelResponse,offsetResponse,Fintype.sum_prod_type,
      Fin.sum_univ_one,squareShift,grid_character_apply]
  simp_rw [hr]
  have hi := (quarter_gaussian_independent L).comp (fun (_ : Fin L) (z : ℝ) => (z : ℂ))
    (fun _ => Complex.measurable_ofReal)
  change iIndepFun (fun l : Fin L => fun ω : Fin L → ℝ => (ω l : ℂ))
    (quarterGaussianLayers L) at hi
  have hp := independent_complex_product_second_moment (quarterGaussianLayers L)
    (fun l : Fin L => fun ω : Fin L → ℝ => (ω l : ℂ))
    (fun l => Complex.measurable_ofReal.comp (measurable_pi_apply l)) hi
  simp only [Function.comp_apply] at hp
  rw [hp]
  have hs (l : Fin L) : (∫ ω : Fin L → ℝ,Complex.normSq (ω l : ℂ)
      ∂quarterGaussianLayers L) = (1/4 : ℝ) := by
    have h := ConceptGaussian.gaussian_feature_moments (quarterGaussianLayers L)
      (fun ω => ω l) 0 (1/4 : NNReal) (measurable_pi_apply l) (quarter_gaussian_coordinate_law l)
    have hv := variance_eq_sub h.1
    rw [h.2.1,h.2.2] at hv
    simp only [Complex.normSq_ofReal]
    simpa only [pow_two,zero_pow,OfNat.ofNat_ne_zero,sub_zero,NNReal.coe_div,
      NNReal.coe_one,NNReal.coe_ofNat,Pi.mul_apply,zero_mul] using hv.symm
  simp_rw [hs]
  simp

theorem actual_gaussian_depth_growth_counterexample :
    (∫ ω,Complex.normSq (∏ l : Fin 2,
      randomKernelResponse (fun _ : Fin 1 × Fin 1 => fun ω : Fin 2 → ℝ => ω l)
        (1 : ZMod 4) (1 : ZMod 4) ω) ∂quarterGaussianLayers 2) <
    (∫ ω,Complex.normSq (∏ l : Fin 1,
      randomKernelResponse (fun _ : Fin 1 × Fin 1 => fun ω : Fin 1 → ℝ => ω l)
        (1 : ZMod 4) (1 : ZMod 4) ω) ∂quarterGaussianLayers 1) := by
  rw [actual_unit_kernel_gaussian_depth_moment,actual_unit_kernel_gaussian_depth_moment]
  norm_num

end Harsanyi.Frequency
