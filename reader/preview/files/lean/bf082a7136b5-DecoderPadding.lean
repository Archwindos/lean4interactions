import Harsanyi.Extensions.DecoderKernelMoments
import Harsanyi.Extensions.DecoderUpsampling

namespace Harsanyi.Frequency
open Finset AddChar MeasureTheory ProbabilityTheory
open scoped BigOperators

noncomputable def edgePad23 (f : Fin 2 × Fin 2 → ℂ) : Grid 3 3 → ℂ :=
  scatter (squareShift 2) f

theorem edge_pad_position_injective :
    Function.Injective (squareShift (M:=3) (N:=3) 2) := by
  intro x y h
  apply Prod.ext <;> apply Fin.ext
  · have hh := congrArg (fun z : Grid 3 3 => z.1.val) h
    simpa only [squareShift,ZMod.val_natCast_of_lt (by omega : x.1.val<3),
      ZMod.val_natCast_of_lt (by omega : y.1.val<3)] using hh
  · have hh := congrArg (fun z : Grid 3 3 => z.2.val) h
    simpa only [squareShift,ZMod.val_natCast_of_lt (by omega : x.2.val<3),
      ZMod.val_natCast_of_lt (by omega : y.2.val<3)] using hh

theorem edge_pad_original (f : Fin 2 × Fin 2 → ℂ) (t : Fin 2 × Fin 2) :
    edgePad23 f (squareShift 2 t) = f t :=
  scatter_original _ _ edge_pad_position_injective t

theorem edge_pad_zero (f : Fin 2 × Fin 2 → ℂ) (x : Grid 3 3)
    (hx : x ∉ Set.range (squareShift (M:=3) (N:=3) 2)) : edgePad23 f x = 0 :=
  scatter_elsewhere _ _ x hx

theorem edge_pad_constant_dft (z : ℂ) :
    dft2 (edgePad23 (fun _ => z)) 1 1 =
      z * (1+ZMod.stdAddChar (-1 : ZMod 3))^2 := by
  rw [dft2,edgePad23,transform_scatter]
  simp only [Fintype.sum_prod_type,squareShift,grid_character_apply,Prod.fst_neg,
    Prod.snd_neg]
  simp [Fin.sum_univ_two,pow_two]
  ring

theorem third_root_geometric_zero :
    1+ZMod.stdAddChar (-1 : ZMod 3)+(ZMod.stdAddChar (-1 : ZMod 3))^2 = 0 := by
  have hp : (ZMod.stdAddChar (-1 : ZMod 3))^3 = 1 := by
    rw [← map_nsmul_eq_pow]
    have h : (3 : ℕ) • (-1 : ZMod 3) = 0 := by decide
    rw [h,map_zero_eq_one]
  have hn : ZMod.stdAddChar (-1 : ZMod 3) ≠ 1 := by
    intro h
    have he : (-1 : ZMod 3)=0 := ZMod.injective_stdAddChar (h.trans (map_zero_eq_one _).symm)
    exact (by decide : (-1 : ZMod 3) ≠ 0) he
  have h := geometric_root 3 (ZMod.stdAddChar (-1 : ZMod 3)) hp
  simpa [geometric,hn,Finset.sum_range_succ] using h

theorem padded_phase_normSq_one :
    Complex.normSq ((1+ZMod.stdAddChar (-1 : ZMod 3))^2) = 1 := by
  have h := third_root_geometric_zero
  have he : 1+ZMod.stdAddChar (-1 : ZMod 3) = -(ZMod.stdAddChar (-1 : ZMod 3))^2 := by
    linear_combination h
  rw [he]
  simp only [map_pow,Complex.normSq_neg,Complex.normSq_eq_norm_sq,
    ZMod.stdAddChar_apply,norm_neg,norm_pow,Circle.norm_coe,one_pow]

variable {Ω : Type*} [MeasurableSpace Ω]
variable (μ : Measure Ω) [IsProbabilityMeasure μ]

theorem actual_correlated_padding_counterexample (U : Ω → ℝ) (q : NNReal)
    (hm : Measurable U) (hl : μ.map U = gaussianReal 0 q) (hq : 0<(q : ℝ)) :
    (∫ ω,Complex.normSq (dft2 (edgePad23 (fun _ => (U ω : ℂ))) 1 1) ∂μ) -
      (∫ ω,Complex.normSq (dft2 (fun _ : Grid 2 2 => (U ω : ℂ)) 1 1) ∂μ) ≠ 0 := by
  have hu := ConceptGaussian.gaussian_feature_moments μ U 0 q hm hl
  have hs : (∫ ω,U ω^2 ∂μ) = (q : ℝ) := by
    have h := variance_eq_sub hu.1
    rw [hu.2.1,hu.2.2] at h
    simpa using h.symm
  have h10 : (1 : ZMod 2) ≠ 0 := by decide
  simp_rw [edge_pad_constant_dft,dft2_constant]
  simp only [h10,false_and,if_false,Complex.normSq_zero,integral_zero,sub_zero,
    Complex.normSq_mul,padded_phase_normSq_one,mul_one,Complex.normSq_ofReal]
  simp only [← pow_two]
  rw [hs]
  exact ne_of_gt hq

end Harsanyi.Frequency
