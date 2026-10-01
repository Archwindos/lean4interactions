import Harsanyi.Extensions.DecoderFourier
import Mathlib.Analysis.Normed.Module.FiniteDimension

namespace Harsanyi.Frequency
open Finset AddChar
open scoped BigOperators
variable {M N : ℕ} [NeZero M] [NeZero N]
variable {I C D : Type*} [Fintype I] [Fintype C] [Fintype D]
variable [DecidableEq I] [DecidableEq C] [DecidableEq D]

noncomputable def realKernelLinear (shift : I → Grid M N) (f : C → Grid M N → ℝ) :
    ((D × C × I) → ℝ) →ₗ[ℝ] ((D × Grid M N) → ℝ) where
  toFun := fun w y => ∑ c, ∑ t,w (y.1,c,t)*f c (y.2+shift t)
  map_add' := by intro w z; funext y; simp [add_mul,sum_add_distrib]
  map_smul' := by intro a w; funext y; simp [mul_assoc,mul_sum]

noncomputable def realKernelCLM (shift : I → Grid M N) (f : C → Grid M N → ℝ) :
    ((D × C × I) → ℝ) →L[ℝ] ((D × Grid M N) → ℝ) :=
  (realKernelLinear shift f).toContinuousLinearMap

theorem finite_real_functional (J : (D × Grid M N → ℝ) →L[ℝ] ℝ)
    (z : D × Grid M N → ℝ) :
    J z = ∑ y, z y*J (Pi.single y 1) := by
  calc
    J z = J (∑ y,z y • Pi.single (M:=fun _ : D × Grid M N => ℝ) y (1:ℝ)) :=
      congrArg J (pi_eq_sum_univ' z)
    _ = _ := by simp only [map_sum,map_smul,smul_eq_mul]

theorem real_kernel_basis (shift : I → Grid M N) (f : C → Grid M N → ℝ)
    (j : D × C × I) (y : D × Grid M N) :
    realKernelCLM shift f (Pi.single j 1) y =
      if j.1=y.1 then f j.2.1 (y.2+shift j.2.2) else 0 := by
  change (∑ c,∑ t,(Pi.single (M:=fun _ : D × C × I => ℝ) j 1) (y.1,c,t)*f c (y.2+shift t)) = _
  by_cases h : j.1=y.1
  · obtain ⟨d,c,t⟩ := j
    change d=y.1 at h
    subst d
    simp [Pi.single_apply,Prod.mk.injEq,eq_comm,ite_and]
  · have hh (c : C) (t : I) : (y.1,c,t) ≠ j := fun he => h (congrArg Prod.fst he).symm
    simp [Pi.single_eq_of_ne,hh,h]

theorem actual_real_kernel_pullback (shift : I → Grid M N) (f : C → Grid M N → ℝ)
    (J : (D × Grid M N → ℝ) →L[ℝ] ℝ) (j : D × C × I) :
    (J.comp (realKernelCLM shift f)) (Pi.single j 1) =
      ∑ x : Grid M N,J (Pi.single (j.1,x) 1)*f j.2.1 (x+shift j.2.2) := by
  rw [ContinuousLinearMap.comp_apply,finite_real_functional]
  simp_rw [real_kernel_basis]
  rw [Fintype.sum_prod_type]
  simp only [ite_mul,zero_mul]
  simp
  apply sum_congr rfl
  intro x _
  ring

theorem actual_real_layer_loss_hasFDerivAt
    (shift : I → Grid M N) (f : C → Grid M N → ℝ)
    (b : D × Grid M N → ℝ) (w : D × C × I → ℝ)
    (Loss : (D × Grid M N → ℝ) → ℝ) (J : (D × Grid M N → ℝ) →L[ℝ] ℝ)
    (hL : HasFDerivAt Loss J (realKernelCLM shift f w+b)) :
    HasFDerivAt (fun z => Loss (realKernelCLM shift f z+b))
      (J.comp (realKernelCLM shift f)) w := by
  exact hL.comp w ((realKernelCLM shift f).hasFDerivAt.add_const b)

theorem actual_response_gradient_update
    (shift : I → Grid M N) (w r : I → ℝ) (η : ℝ) (u : ZMod M) (v : ZMod N) :
    offsetResponse shift (fun t => (w t-η*r t : ℝ)) u v -
      offsetResponse shift (fun t => (w t : ℂ)) u v =
      -(η : ℂ)*offsetResponse shift (fun t => (r t : ℂ)) u v := by
  simp only [offsetResponse,Complex.ofReal_sub,Complex.ofReal_mul,sub_mul,
    sum_sub_distrib,sub_self,sub_add_cancel,sum_mul,mul_sum,sum_neg_distrib]
  ring_nf
  rw [sum_neg_distrib]

end Harsanyi.Frequency
