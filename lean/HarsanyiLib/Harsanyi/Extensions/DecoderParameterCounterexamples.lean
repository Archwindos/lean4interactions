import Harsanyi.Extensions.DecoderKernelMoments

/-! Actual independently sampled Gaussian square kernels on an 8×8 grid.
The two counterexamples use separate permitted parameter choices: (m,q)=(1,1/16)
for absolute second-moment growth and (m,q)=(1,1) for the DC/non-DC ratio. -/
namespace Harsanyi.Frequency.Parameters
open Finset MeasureTheory ProbabilityTheory
open scoped BigOperators

noncomputable def gaussianKernelSpace (K : ℕ) (m : ℝ) (q : NNReal) :
    Measure (Fin K × Fin K → ℝ) := Measure.pi (fun _ => gaussianReal m q)

instance (K : ℕ) (m : ℝ) (q : NNReal) : IsProbabilityMeasure (gaussianKernelSpace K m q) := by
  unfold gaussianKernelSpace
  infer_instance

theorem gaussian_kernel_coordinate_law (K : ℕ) (m : ℝ) (q : NNReal) (t : Fin K × Fin K) :
    (gaussianKernelSpace K m q).map (fun ω => ω t) = gaussianReal m q :=
  (measurePreserving_eval (fun _ : Fin K × Fin K => gaussianReal m q) t).map_eq

theorem gaussian_kernel_independent (K : ℕ) (m : ℝ) (q : NNReal) :
    iIndepFun (fun t : Fin K × Fin K => fun ω : Fin K × Fin K → ℝ => ω t)
      (gaussianKernelSpace K m q) :=
  iIndepFun_pi (fun _ => measurable_id.aemeasurable)

noncomputable def kernelSOM (K : ℕ) (m : ℝ) (q : NNReal) (u v : ZMod 8) : ℝ :=
  ∫ ω, Complex.normSq (randomKernelResponse (fun t => fun ω => ω t) u v ω)
    ∂gaussianKernelSpace K m q

theorem actual_kernel_som (K : ℕ) (m : ℝ) (q : NNReal) (u v : ZMod 8) :
    kernelSOM K m q u v = Complex.normSq ((m : ℂ)*phaseSum (M:=8) (N:=8) (K:=K) u v) +
      (K*K : ℕ)*(q : ℝ) := by
  exact actual_kernel_second_moment (gaussianKernelSpace K m q)
    (fun t => fun ω => ω t) m q (fun t => measurable_pi_apply t)
    (gaussian_kernel_coordinate_law K m q) (gaussian_kernel_independent K m q) u v

theorem std_character_eight_four : ZMod.stdAddChar (4 : ZMod 8) = -1 := by
  have h := ZMod.stdAddChar_coe (4 : ℤ) (N:=8)
  norm_num only [Int.cast_ofNat] at h
  rw [h]
  rw [show 2*Real.pi*Complex.I*(4:ℂ)/8 = (Real.pi : ℂ)*Complex.I by ring]
  exact Complex.exp_pi_mul_I

theorem phase_sum_one (u v : ZMod 8) : phaseSum (M:=8) (N:=8) (K:=1) u v = 1 := by
  simp [phaseSum,Fintype.sum_prod_type,Fin.sum_univ_one,squareShift,grid_character_apply]

theorem phase_sum_two_40 : phaseSum (M:=8) (N:=8) (K:=2) (4 : ZMod 8) 0 = 0 := by
  simp [phaseSum,Fintype.sum_prod_type,Fin.sum_univ_two,squareShift,
    grid_character_apply,std_character_eight_four]

theorem phase_sum_four_40 : phaseSum (M:=8) (N:=8) (K:=4) (4 : ZMod 8) 0 = 0 := by
  have h8 : (4 : ZMod 8)*(1+1) = 0 := by decide
  have h12 : (4 : ZMod 8)*(1+1+1) = 4 := by decide
  simp [phaseSum,Fintype.sum_prod_type,Fin.sum_univ_succ,squareShift,
    grid_character_apply,std_character_eight_four]
  rw [h8,h12,std_character_eight_four]
  simp

theorem phase_sum_dc (K : ℕ) : phaseSum (M:=8) (N:=8) (K:=K) (0 : ZMod 8) 0 = (K*K : ℕ) := by
  simp [phaseSum,grid_character_apply,Fintype.card_prod]

theorem kernel_size_one_som : kernelSOM 1 1 (1/16) 4 0 = 17/16 := by
  rw [actual_kernel_som,phase_sum_one]
  norm_num [Complex.normSq]

theorem kernel_size_two_som : kernelSOM 2 1 (1/16) 4 0 = 1/4 := by
  rw [actual_kernel_som,phase_sum_two_40]
  norm_num

theorem actual_kernel_size_growth_counterexample :
    kernelSOM 2 1 (1/16) 4 0 < kernelSOM 1 1 (1/16) 4 0 := by
  rw [kernel_size_two_som,kernel_size_one_som]
  norm_num

theorem kernel_size_two_dc_ratio : kernelSOM 2 1 1 0 0 / kernelSOM 2 1 1 4 0 = 5 := by
  rw [actual_kernel_som,actual_kernel_som,phase_sum_dc,phase_sum_two_40]
  norm_num [Complex.normSq]

theorem kernel_size_four_dc_ratio : kernelSOM 4 1 1 0 0 / kernelSOM 4 1 1 4 0 = 17 := by
  rw [actual_kernel_som,actual_kernel_som,phase_sum_dc,phase_sum_four_40]
  norm_num [Complex.normSq]

theorem actual_kernel_dc_ratio_counterexample :
    kernelSOM 2 1 1 0 0 / kernelSOM 2 1 1 4 0 <
      kernelSOM 4 1 1 0 0 / kernelSOM 4 1 1 4 0 := by
  rw [kernel_size_two_dc_ratio,kernel_size_four_dc_ratio]
  norm_num

end Harsanyi.Frequency.Parameters
