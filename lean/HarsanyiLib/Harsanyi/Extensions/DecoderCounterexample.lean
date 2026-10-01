import Harsanyi.Extensions.DecoderFourier
import Harsanyi.Extensions.DecoderCascade

/-! The one-step counterexample uses actual real 2×2 kernels on a 4×4 grid,
the original two-frequency loss, its real derivatives, and the actual spatial
two-layer network. Conjugate target completion does not add loss terms. -/
namespace Harsanyi.Frequency
open Finset AddChar
open scoped BigOperators

@[simp] theorem std_character_four_one : ZMod.stdAddChar (1 : ZMod 4) = Complex.I := by
  change ZMod.stdAddChar ((1 : ℤ) : ZMod 4) = Complex.I
  rw [ZMod.stdAddChar_coe]
  convert Complex.exp_pi_div_two_mul_I using 1
  congr 1
  push_cast
  ring

noncomputable def realKernel2 (a b c d : ℝ) (t : Fin 2 × Fin 2) : ℂ :=
  if t.1=0 then (if t.2=0 then a else b) else (if t.2=0 then c else d)

theorem actual_response01 (a b c d : ℝ) :
    offsetResponse (squareShift (M:=4) (N:=4) 2) (realKernel2 a b c d) 0 1 =
      response01 a b c d := by
  rw [square_kernel_response]
  simp [Fin.sum_univ_two,realKernel2,response01]
  push_cast
  ring

theorem actual_response10 (a b c d : ℝ) :
    offsetResponse (squareShift (M:=4) (N:=4) 2) (realKernel2 a b c d) 1 0 =
      response10 a b c d := by
  rw [square_kernel_response]
  simp [Fin.sum_univ_two,realKernel2,response10]
  push_cast
  ring

noncomputable def deltaGrid : Grid 4 4 → ℂ := fun x => if x=0 then 1 else 0

theorem delta_grid_dft (u v : ZMod 4) : dft2 deltaGrid u v = 1 := by
  simp [dft2,transform,deltaGrid]

noncomputable def kernelLayer4 (w : Fin 2 × Fin 2 → ℂ) (f : Grid 4 4 → ℂ) :
    Grid 4 4 → ℂ := offsetLayer (squareShift 2) (fun (_ _ : Unit) => w)
      (fun _ : Unit => f) (fun _ => 0) ()

theorem kernel_layer_fourier (w : Fin 2 × Fin 2 → ℂ) (f : Grid 4 4 → ℂ)
    (u v : ZMod 4) :
    dft2 (kernelLayer4 w f) u v =
      offsetResponse (squareShift 2) w u v * dft2 f u v := by
  simpa [kernelLayer4] using offset_layer_dft (squareShift (M:=4) (N:=4) 2)
    (fun (_ _ : Unit) => w) (fun _ : Unit => f) (fun _ => 0) () u v

noncomputable def twoLayer4 (w₁ w₂ : Fin 2 × Fin 2 → ℂ) : Grid 4 4 → ℂ :=
  kernelLayer4 w₂ (kernelLayer4 w₁ deltaGrid)

theorem actual_two_layer_spectrum (w₁ w₂ : Fin 2 × Fin 2 → ℂ) (u v : ZMod 4) :
    dft2 (twoLayer4 w₁ w₂) u v =
      offsetResponse (squareShift 2) w₂ u v * offsetResponse (squareShift 2) w₁ u v := by
  simp only [twoLayer4,kernel_layer_fourier,delta_grid_dft,mul_one]

theorem identity_kernel_response (u v : ZMod 4) :
    offsetResponse (squareShift 2) (realKernel2 1 0 0 0) u v = 1 := by
  rw [square_kernel_response]
  simp [Fin.sum_univ_two,realKernel2]

noncomputable def twoFrequencyLoss (α : ℝ) (w₁ w₂ : Fin 2 × Fin 2 → ℂ) : ℝ :=
  Complex.normSq (dft2 (twoLayer4 w₁ w₂) 0 1 - (1-α : ℂ)) +
  Complex.normSq (dft2 (twoLayer4 w₁ w₂) 1 0 - (1+α : ℂ))

theorem actual_real_loss_identity_layer (α a b c d : ℝ) :
    twoFrequencyLoss α (realKernel2 a b c d) (realKernel2 1 0 0 0) =
      realLoss α a b c d := by
  simp only [twoFrequencyLoss,actual_two_layer_spectrum,identity_kernel_response,one_mul,
    actual_response01,actual_response10,response01,response10,realLoss,Complex.normSq_apply]
  simp only [Complex.add_re,Complex.add_im,Complex.sub_re,Complex.sub_im,
    Complex.ofReal_re,Complex.ofReal_im,Complex.mul_re,Complex.mul_im,
    Complex.I_re,Complex.I_im,Complex.one_re,Complex.one_im]
  ring

theorem actual_real_loss_layer_exchange (α : ℝ) (w₁ w₂ : Fin 2 × Fin 2 → ℂ) :
    twoFrequencyLoss α w₁ w₂ = twoFrequencyLoss α w₂ w₁ := by
  simp only [twoFrequencyLoss,actual_two_layer_spectrum,mul_comm]

theorem actual_gradient00 (α : ℝ) :
    HasDerivAt (fun q => twoFrequencyLoss α (realKernel2 q 0 0 0) (realKernel2 1 0 0 0)) 0 1 := by
  simpa only [actual_real_loss_identity_layer] using realLoss_gradient00 α

theorem actual_gradient01 (α : ℝ) :
    HasDerivAt (fun q => twoFrequencyLoss α (realKernel2 1 q 0 0) (realKernel2 1 0 0 0)) (-2*α) 0 := by
  simpa only [actual_real_loss_identity_layer] using realLoss_gradient01 α

theorem actual_gradient10 (α : ℝ) :
    HasDerivAt (fun q => twoFrequencyLoss α (realKernel2 1 0 q 0) (realKernel2 1 0 0 0)) (2*α) 0 := by
  simpa only [actual_real_loss_identity_layer] using realLoss_gradient10 α

theorem actual_gradient11 (α : ℝ) :
    HasDerivAt (fun q => twoFrequencyLoss α (realKernel2 1 0 0 q) (realKernel2 1 0 0 0)) 0 0 := by
  simpa only [actual_real_loss_identity_layer] using realLoss_gradient11 α

theorem actual_spatial_one_step_not_target (α η : ℝ) (ha : 0<α) (he : 0<η) :
    dft2 (twoLayer4 (realKernel2 1 (2*η*α) (-2*η*α) 0)
      (realKernel2 1 (2*η*α) (-2*η*α) 0)) 1 0 ≠ (1+α : ℂ) := by
  rw [actual_two_layer_spectrum,actual_response10,← pow_two]
  exact two_layer_one_step_counterexample α η ha he

noncomputable def completedTargetSpectrum (α : ℝ) (k : Grid 4 4) : ℂ :=
  1 + (if k=(1,0) then (α : ℂ) else 0) + (if k=-(1,0) then (α : ℂ) else 0) -
    (if k=(0,1) then (α : ℂ) else 0) - (if k=-(0,1) then (α : ℂ) else 0)

theorem completed_target_hermitian (α : ℝ) (k : Grid 4 4) :
    completedTargetSpectrum α (-k) = starRingEnd ℂ (completedTargetSpectrum α k) := by
  have hc (p : Grid 4 4) : starRingEnd ℂ (if k=p then (α : ℂ) else 0) =
      if k=p then (α : ℂ) else 0 := by split_ifs <;> simp
  simp only [completedTargetSpectrum,map_add,map_sub,map_one,hc,
    neg_eq_iff_eq_neg,neg_neg]
  ring

noncomputable def completedTargetImage (α : ℝ) : Grid 4 4 → ℂ :=
  inverseDft2 (completedTargetSpectrum α)

theorem completed_target_image_real (α : ℝ) (x : Grid 4 4) :
    (completedTargetImage α x).im = 0 := by
  have h := congrArg Complex.im
    (hermitian_inverse_real (completedTargetSpectrum α) (completed_target_hermitian α) x)
  simpa only [Complex.conj_im] using (show (completedTargetImage α x).im=0 from by
    change -(completedTargetImage α x).im=(completedTargetImage α x).im at h
    linarith)

theorem completed_target_selected_frequencies (α : ℝ) :
    dft2 (completedTargetImage α) 0 1 = (1-α : ℂ) ∧
      dft2 (completedTargetImage α) 1 0 = (1+α : ℂ) := by
  have h10 : (1 : ZMod 4) ≠ 0 := by decide
  have h1n : (1 : ZMod 4) ≠ -1 := by decide
  constructor
  · rw [completedTargetImage,dft2_inverse (completedTargetSpectrum α) (0,1)]
    simp [completedTargetSpectrum,h10,h1n,Ne.symm h10]
  · rw [completedTargetImage,dft2_inverse (completedTargetSpectrum α) (1,0)]
    simp [completedTargetSpectrum,h10,h1n,Ne.symm h10]

theorem source_constraint43 :
    1 / Complex.normSq (dft2 deltaGrid 0 1) = (1:ℝ) ∧
      1 / Complex.normSq (dft2 deltaGrid 1 0) = (1:ℝ) := by
  simp [delta_grid_dft]

theorem source_constraint44 :
    (((2-1 : ℝ)*(1-0)/4 + (2-1 : ℝ)*(0-1)/4)*Real.pi/2) = 0 := by ring

theorem source_constraint45 :
    dft2 (twoLayer4 (realKernel2 1 0 0 0) (realKernel2 1 0 0 0)) 0 1 = 1 ∧
      dft2 (twoLayer4 (realKernel2 1 0 0 0) (realKernel2 1 0 0 0)) 1 0 = 1 := by
  simp [actual_two_layer_spectrum,identity_kernel_response]

theorem source_constraint46 (u v : ZMod 4) :
    (∑ _ : Fin 2, Complex.normSq (offsetResponse (squareShift 2)
      (realKernel2 1 0 0 0) u v) * Complex.normSq (1:ℂ)) = (2:ℝ) := by
  simp [identity_kernel_response]

end Harsanyi.Frequency
