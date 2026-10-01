import Harsanyi.Extensions.DecoderSpectralPullback
import Harsanyi.Extensions.DecoderCascade

/-! Real-coordinate differentiation of an actual heterogeneous circular cascade.
The spectral cotangent is DFT(real Riesz gradient)/(MN), as in the source's
full-conjugate-gradient convention. -/
namespace Harsanyi.Frequency.MatrixBackprop
open Finset
open scoped BigOperators
variable {M N : ℕ} [NeZero M] [NeZero N]
variable {I C D : Type*} [Fintype I] [Fintype C] [Fintype D]
variable [DecidableEq I] [DecidableEq C] [DecidableEq D]

abbrev Feature (C : Type*) := C × Grid M N → ℝ

noncomputable def featureLinear (shift : I → Grid M N) (w : D → C → I → ℝ) :
    Feature (M:=M) (N:=N) C →ₗ[ℝ] Feature (M:=M) (N:=N) D where
  toFun := fun f y => ∑ c, ∑ t,w y.1 c t*f (c,y.2+shift t)
  map_add' := by intro f g; funext y; simp [mul_add,sum_add_distrib]
  map_smul' := by intro a f; funext y; simp [mul_assoc,mul_left_comm,mul_sum]

noncomputable def featureCLM (shift : I → Grid M N) (w : D → C → I → ℝ) :
    Feature (M:=M) (N:=N) C →L[ℝ] Feature (M:=M) (N:=N) D :=
  (featureLinear shift w).toContinuousLinearMap

theorem feature_clm_apply (shift : I → Grid M N) (w : D → C → I → ℝ)
    (f : Feature (M:=M) (N:=N) C) (y : D × Grid M N) :
    featureCLM shift w f y = ∑ c,∑ t,w y.1 c t*f (c,y.2+shift t) := rfl

noncomputable def featurePullback (shift : I → Grid M N) (w : D → C → I → ℝ)
    (z : Feature (M:=M) (N:=N) D) : Feature (M:=M) (N:=N) C :=
  fun y => ∑ d, ∑ t,w d y.1 t*z (d,y.2-shift t)

theorem shifted_real_pair (f z : Grid M N → ℝ) (t : Grid M N) :
    (∑ x,z x*f (x+t)) = ∑ x,z (x-t)*f x := by
  apply Fintype.sum_equiv (Equiv.addRight t)
  intro x
  simp

theorem feature_duality (shift : I → Grid M N) (w : D → C → I → ℝ)
    (f : Feature (M:=M) (N:=N) C) (z : Feature (M:=M) (N:=N) D) :
    (∑ y,z y*featureCLM shift w f y) = ∑ x,featurePullback shift w z x*f x := by
  simp only [feature_clm_apply,featurePullback,mul_sum,sum_mul]
  conv_lhs => rw [Fintype.sum_prod_type]
  conv_rhs => rw [Fintype.sum_prod_type]
  have hh (d : D) (c : C) (t : I) :
      (∑ x : Grid M N,z (d,x)*(w d c t*f (c,x+shift t))) =
        ∑ x : Grid M N,(w d c t*z (d,x-shift t))*f (c,x) := by
    calc
      _ = w d c t * ∑ x : Grid M N,z (d,x)*f (c,x+shift t) := by
        simp [mul_sum,mul_assoc,mul_left_comm]
      _ = w d c t * ∑ x : Grid M N,z (d,x-shift t)*f (c,x) := by
        rw [shifted_real_pair (fun x => f (c,x)) (fun x => z (d,x)) (shift t)]
      _ = _ := by simp [mul_sum,mul_assoc]
  calc
    _ = ∑ d,∑ c,∑ t,∑ x : Grid M N,z (d,x)*(w d c t*f (c,x+shift t)) := by
      apply sum_congr rfl
      intro d _
      rw [sum_comm]
      apply sum_congr rfl
      intro c _
      rw [sum_comm]
    _ = ∑ d,∑ c,∑ t,∑ x : Grid M N,(w d c t*z (d,x-shift t))*f (c,x) := by
      simp_rw [hh]
    _ = _ := by
      rw [sum_comm]
      apply sum_congr rfl
      intro c _
      calc
        _ = ∑ d,∑ x : Grid M N,∑ t,(w d c t*z (d,x-shift t))*f (c,x) := by
          apply sum_congr rfl
          intro d _
          rw [sum_comm]
        _ = _ := by rw [sum_comm]

noncomputable def riesz (J : Feature (M:=M) (N:=N) D →L[ℝ] ℝ) :
    Feature (M:=M) (N:=N) D := fun y => J (Pi.single y 1)

theorem riesz_pullback (shift : I → Grid M N) (w : D → C → I → ℝ)
    (J : Feature (M:=M) (N:=N) D →L[ℝ] ℝ) :
    riesz (J.comp (featureCLM shift w)) = featurePullback shift w (riesz J) := by
  funext x
  unfold riesz
  rw [ContinuousLinearMap.comp_apply,finite_real_functional]
  calc
    _ = ∑ y,(J (Pi.single y 1))*featureCLM shift w (Pi.single x 1) y := by
      apply sum_congr rfl
      intro y _
      ring
    _ = ∑ y,featurePullback shift w (riesz J) y*
        (Pi.single (M:=fun _ : C × Grid M N => ℝ) x 1) y :=
      feature_duality shift w (Pi.single x 1) (riesz J)
    _ = _ := by simp [Pi.single_apply]; rfl

theorem pullback_spectrum (shift : I → Grid M N) (w : D → C → I → ℝ)
    (z : Feature (M:=M) (N:=N) D) (c : C) (u : ZMod M) (v : ZMod N) :
    dft2 (fun x => (featurePullback shift w z (c,x) : ℂ)) u v =
      ∑ d,starRingEnd ℂ (offsetResponse shift (fun t => (w d c t : ℂ)) u v) *
        dft2 (fun x => (z (d,x) : ℂ)) u v := by
  have hh : (fun x => (featurePullback shift w z (c,x) : ℂ)) =
      fun x => ∑ d,∑ t,(w d c t : ℂ)*(z (d,x-shift t) : ℂ) := by
    funext x
    simp [featurePullback]
  rw [hh]
  unfold dft2
  rw [transform_finite_sum]
  apply sum_congr rfl
  intro d _
  rw [transform_finite_sum]
  simp_rw [transform_smul]
  have hs (t : I) : transform (gridCharacter u v)
      (fun x => (z (d,x-shift t) : ℂ)) =
      gridCharacter u v (-shift t)*transform (gridCharacter u v) (fun x => (z (d,x) : ℂ)) := by
    simpa only [sub_eq_add_neg] using
      transform_shift (gridCharacter u v) (fun x => (z (d,x) : ℂ)) (-shift t)
  simp_rw [hs]
  simp only [offsetResponse,map_sum,map_mul,Complex.conj_ofReal,grid_character_conjugate,
    sum_mul]
  apply sum_congr rfl
  intro t _
  rw [show starRingEnd ℂ (gridCharacter u v (shift t)) =
    gridCharacter u v (-shift t) from grid_character_conjugate (u,v) (shift t)]
  ring

variable {E : Type*} [Fintype E] [DecidableEq E]

theorem complex_linear_coefficients (A : (C → ℂ) →ₗ[ℂ] (D → ℂ))
    (z : C → ℂ) (d : D) :
    A z d = ∑ c,A (Pi.single c 1) d*z c := by
  calc
    A z d = A (∑ c,z c • Pi.single (M:=fun _ : C => ℂ) c (1:ℂ)) d :=
      congrArg (fun t => A t d) (pi_eq_sum_univ' z)
    _ = _ := by simp [map_sum,map_smul,mul_comm]

noncomputable def conjugateTranspose (A : (C → ℂ) →ₗ[ℂ] (D → ℂ)) :
    (D → ℂ) →ₗ[ℂ] (C → ℂ) where
  toFun := fun z c => ∑ d,starRingEnd ℂ (A (Pi.single c 1) d)*z d
  map_add' := by intro z t; funext c; simp [mul_add,sum_add_distrib]
  map_smul' := by intro a z; funext c; simp [mul_left_comm,mul_sum]

theorem conjugate_transpose_comp (A : (C → ℂ) →ₗ[ℂ] (D → ℂ))
    (B : (D → ℂ) →ₗ[ℂ] (E → ℂ)) :
    conjugateTranspose (B.comp A) =
      (conjugateTranspose A).comp (conjugateTranspose B) := by
  apply LinearMap.ext
  intro z
  funext c
  change (∑ e,starRingEnd ℂ (B (A (Pi.single c 1)) e)*z e) =
    ∑ d,starRingEnd ℂ (A (Pi.single c 1) d)*
      ∑ e,starRingEnd ℂ (B (Pi.single d 1) e)*z e
  have hB (e : E) := complex_linear_coefficients B (A (Pi.single c 1)) e
  simp_rw [hB,map_sum,map_mul,sum_mul,mul_sum]
  rw [sum_comm]
  apply sum_congr rfl
  intro d _
  apply sum_congr rfl
  intro e _
  ring

noncomputable def responseLinear (shift : I → Grid M N) (w : D → C → I → ℝ)
    (u : ZMod M) (v : ZMod N) : (C → ℂ) →ₗ[ℂ] (D → ℂ) where
  toFun := fun z d => ∑ c,offsetResponse shift (fun t => (w d c t : ℂ)) u v*z c
  map_add' := by intro z t; funext d; simp [mul_add,sum_add_distrib]
  map_smul' := by intro a z; funext d; simp [mul_left_comm,mul_sum]

theorem response_basis (shift : I → Grid M N) (w : D → C → I → ℝ)
    (u : ZMod M) (v : ZMod N) (c : C) (d : D) :
    responseLinear shift w u v (Pi.single c 1) d =
      offsetResponse shift (fun t => (w d c t : ℂ)) u v := by
  simp [responseLinear,Pi.single_apply]

noncomputable def featureSpectrum (z : Feature (M:=M) (N:=N) C)
    (u : ZMod M) (v : ZMod N) : C → ℂ :=
  fun c => dft2 (fun x => (z (c,x) : ℂ)) u v

theorem feature_pullback_spectrum (shift : I → Grid M N) (w : D → C → I → ℝ)
    (z : Feature (M:=M) (N:=N) D) (u : ZMod M) (v : ZMod N) :
    featureSpectrum (featurePullback shift w z) u v =
      conjugateTranspose (responseLinear shift w u v) (featureSpectrum z u v) := by
  funext c
  simpa only [featureSpectrum,conjugateTranspose,LinearMap.coe_mk,AddHom.coe_mk,
    response_basis] using pullback_spectrum shift w z c u v

noncomputable def normalizedSpectrum (z : Feature (M:=M) (N:=N) C)
    (u : ZMod M) (v : ZMod N) : C → ℂ :=
  ((M*N : ℕ) : ℂ)⁻¹ • featureSpectrum z u v

theorem actual_kernel_spectral_gradient (shift : I → Grid M N)
    (f : Feature (M:=M) (N:=N) C) (J : Feature (M:=M) (N:=N) D →L[ℝ] ℝ)
    (d : D) (c : C) (u : ZMod M) (v : ZMod N) :
    offsetResponse shift
      (fun t => (((J.comp (realKernelCLM shift (fun c x => f (c,x))))
        (Pi.single (d,c,t) 1) : ℝ) : ℂ)) u v =
      ((M*N : ℕ) : ℂ) * ∑ k : Grid M N,crossFrequencyKernel shift u k.1 v k.2 *
        starRingEnd ℂ (featureSpectrum f k.1 k.2 c) *
        normalizedSpectrum (riesz J) k.1 k.2 d := by
  have hr (t : I) :
      (((J.comp (realKernelCLM shift (fun c x => f (c,x))))
        (Pi.single (d,c,t) 1) : ℝ) : ℂ) =
      spatialInnerPullback (fun x => (f (c,x) : ℂ))
        (fun x => (riesz J (d,x) : ℂ)) (shift t) := by
    rw [actual_real_kernel_pullback,actual_real_spatial_pullback]
    congr 1
    apply sum_congr rfl
    intro x _
    change J (Pi.single (d,x) 1)*f (c,x+shift t) =
      f (c,x+shift t)*J (Pi.single (d,x) 1)
    ring
  simp_rw [hr]
  rw [spectral_kernel_pullback,mul_sum]
  apply sum_congr rfl
  intro k _
  have hc : ((M*N : ℕ) : ℂ) ≠ 0 :=
    Nat.cast_ne_zero.mpr (Nat.mul_ne_zero (NeZero.ne M) (NeZero.ne N))
  simp only [normalizedSpectrum,featureSpectrum,Pi.smul_apply,smul_eq_mul]
  field_simp


section Cascade
variable (S : ℕ → Type*) [∀ n,Fintype (S n)] [∀ n,DecidableEq (S n)]

noncomputable def realNetwork (shift : I → Grid M N)
    (w : ∀ n,S (n+1) → S n → I → ℝ) (b : ∀ n,S (n+1) → ℝ)
    (f : Feature (M:=M) (N:=N) (S 0)) : ∀ n,Feature (M:=M) (N:=N) (S n)
  | 0 => f
  | n+1 => featureCLM shift (w n) (realNetwork shift w b f n)+fun y => b n y.1

noncomputable def networkCLM (shift : I → Grid M N)
    (w : ∀ n,S (n+1) → S n → I → ℝ) :
    ∀ n,Feature (M:=M) (N:=N) (S 0) →L[ℝ] Feature (M:=M) (N:=N) (S n)
  | 0 => ContinuousLinearMap.id ℝ _
  | n+1 => (featureCLM shift (w n)).comp (networkCLM shift w n)

theorem real_network_hasFDerivAt (shift : I → Grid M N)
    (w : ∀ n,S (n+1) → S n → I → ℝ) (b : ∀ n,S (n+1) → ℝ)
    (f : Feature (M:=M) (N:=N) (S 0)) (L : ℕ) :
    HasFDerivAt (fun z => realNetwork S shift w b z L)
      (networkCLM S shift w L) f := by
  induction L with
  | zero => exact hasFDerivAt_id f
  | succ L ih =>
    exact ((featureCLM shift (w L)).hasFDerivAt.comp f ih).add_const (fun y => b L y.1)

noncomputable def networkPullback (shift : I → Grid M N)
    (w : ∀ n,S (n+1) → S n → I → ℝ) :
    ∀ n,Feature (M:=M) (N:=N) (S n) → Feature (M:=M) (N:=N) (S 0)
  | 0 => id
  | n+1 => fun z => networkPullback shift w n (featurePullback shift (w n) z)

theorem network_riesz_pullback (shift : I → Grid M N)
    (w : ∀ n,S (n+1) → S n → I → ℝ) (L : ℕ)
    (J : Feature (M:=M) (N:=N) (S L) →L[ℝ] ℝ) :
    riesz (J.comp (networkCLM S shift w L)) = networkPullback S shift w L (riesz J) := by
  induction L with
  | zero => simp [networkCLM,networkPullback]
  | succ L ih =>
    rw [networkCLM,← ContinuousLinearMap.comp_assoc,ih,riesz_pullback]
    rfl

theorem network_pullback_spectrum (shift : I → Grid M N)
    (w : ∀ n,S (n+1) → S n → I → ℝ) (L : ℕ)
    (z : Feature (M:=M) (N:=N) (S L)) (u : ZMod M) (v : ZMod N) :
    featureSpectrum (networkPullback S shift w L z) u v =
      conjugateTranspose (cascadeLinear S (fun n => responseLinear shift (w n) u v) L)
        (featureSpectrum z u v) := by
  induction L with
  | zero =>
    funext c
    simp [networkPullback,cascadeLinear,conjugateTranspose,Pi.single_apply]
  | succ L ih =>
    rw [networkPullback,ih,feature_pullback_spectrum,cascadeLinear,
      conjugate_transpose_comp]
    rfl

theorem real_network_embeds (shift : I → Grid M N)
    (w : ∀ n,S (n+1) → S n → I → ℝ) (b : ∀ n,S (n+1) → ℝ)
    (f : Feature (M:=M) (N:=N) (S 0)) (L : ℕ) :
    (fun c x => (realNetwork S shift w b f L (c,x) : ℂ)) =
      gridNetwork S shift (fun n d c t => (w n d c t : ℂ))
        (fun n d => (b n d : ℂ)) (fun c x => (f (c,x) : ℂ)) L := by
  induction L with
  | zero => rfl
  | succ L ih =>
    funext d x
    simp only [realNetwork,Pi.add_apply,Complex.ofReal_add,feature_clm_apply,
      Complex.ofReal_sum,Complex.ofReal_mul,gridNetwork,offsetLayer]
    simp_rw [← congrFun (congrFun ih _) _]

theorem actual_real_network_spectrum (shift : I → Grid M N)
    (w : ∀ n,S (n+1) → S n → I → ℝ) (b : ∀ n,S (n+1) → ℝ)
    (f : Feature (M:=M) (N:=N) (S 0)) (u : ZMod M) (v : ZMod N) (L : ℕ) :
    featureSpectrum (realNetwork S shift w b f L) u v =
      cascadeLinear S (fun n => responseLinear shift (w n) u v) L (featureSpectrum f u v) +
      (if u=0 ∧ v=0 then ((M*N : ℕ) : ℂ) else 0) •
        cascadeBias S (fun n => responseLinear shift (w n) u v)
          (fun n d => (b n d : ℂ)) L := by
  have he := real_network_embeds S shift w b f L
  have hc := actual_grid_cascade S shift (fun n d c t => (w n d c t : ℂ))
    (fun n d => (b n d : ℂ)) (fun c x => (f (c,x) : ℂ)) u v L
  change (fun c => dft2 ((fun c x => (realNetwork S shift w b f L (c,x) : ℂ)) c) u v) = _
  rw [he]
  exact hc

theorem actual_suffix_cotangent (shift : I → Grid M N)
    (w : ∀ n,S (n+1) → S n → I → ℝ) (L : ℕ)
    (J : Feature (M:=M) (N:=N) (S L) →L[ℝ] ℝ) (u : ZMod M) (v : ZMod N) :
    normalizedSpectrum (riesz (J.comp (networkCLM S shift w L))) u v =
      conjugateTranspose (cascadeLinear S (fun n => responseLinear shift (w n) u v) L)
        (normalizedSpectrum (riesz J) u v) := by
  rw [network_riesz_pullback]
  unfold normalizedSpectrum
  rw [network_pullback_spectrum,map_smul]

end Cascade

section FullChain
variable (P S : ℕ → Type*) [∀ n,Fintype (P n)] [∀ n,DecidableEq (P n)]
variable [∀ n,Fintype (S n)] [∀ n,DecidableEq (S n)]

theorem actual_cascade_parameter_loss_hasFDerivAt (shift : I → Grid M N)
    (pw : ∀ n,P (n+1) → P n → I → ℝ) (pb : ∀ n,P (n+1) → ℝ)
    (input : Feature (M:=M) (N:=N) (P 0)) (p : ℕ)
    (sw : ∀ n,S (n+1) → S n → I → ℝ) (sb : ∀ n,S (n+1) → ℝ) (L : ℕ)
    (w : S 0 × P p × I → ℝ) (b : Feature (M:=M) (N:=N) (S 0))
    (Loss : Feature (M:=M) (N:=N) (S L) → ℝ)
    (J : Feature (M:=M) (N:=N) (S L) →L[ℝ] ℝ)
    (hL : HasFDerivAt Loss J (realNetwork S shift sw sb
      (realKernelCLM shift (fun c x => realNetwork P shift pw pb input p (c,x)) w+b) L)) :
    HasFDerivAt
      (fun z => Loss (realNetwork S shift sw sb
        (realKernelCLM shift (fun c x => realNetwork P shift pw pb input p (c,x)) z+b) L))
      ((J.comp (networkCLM S shift sw L)).comp
        (realKernelCLM shift (fun c x => realNetwork P shift pw pb input p (c,x)))) w := by
  exact (hL.comp _ (real_network_hasFDerivAt S shift sw sb _ L)).comp w
    ((realKernelCLM shift (fun c x => realNetwork P shift pw pb input p (c,x))).hasFDerivAt.add_const b)

theorem actual_prefix_suffix_response_update (shift : I → Grid M N)
    (pw : ∀ n,P (n+1) → P n → I → ℝ) (pb : ∀ n,P (n+1) → ℝ)
    (input : Feature (M:=M) (N:=N) (P 0)) (p : ℕ)
    (sw : ∀ n,S (n+1) → S n → I → ℝ) (L : ℕ)
    (J : Feature (M:=M) (N:=N) (S L) →L[ℝ] ℝ)
    (w : S 0 × P p × I → ℝ) (d : S 0) (c : P p) (η : ℝ)
    (u : ZMod M) (v : ZMod N) :
    let gradient := (J.comp (networkCLM S shift sw L)).comp
      (realKernelCLM shift (fun c x => realNetwork P shift pw pb input p (c,x)))
    offsetResponse shift (fun t => ((w (d,c,t)-η*gradient (Pi.single (d,c,t) 1) : ℝ) : ℂ)) u v -
      offsetResponse shift (fun t => (w (d,c,t) : ℂ)) u v =
      -(η : ℂ)*((M*N : ℕ) : ℂ) *
        ∑ k : Grid M N,crossFrequencyKernel shift u k.1 v k.2 *
          starRingEnd ℂ ((cascadeLinear P (fun n => responseLinear shift (pw n) k.1 k.2) p
              (featureSpectrum input k.1 k.2) +
            (if k.1=0 ∧ k.2=0 then ((M*N : ℕ) : ℂ) else 0) •
              cascadeBias P (fun n => responseLinear shift (pw n) k.1 k.2)
                (fun n d => (pb n d : ℂ)) p) c) *
          conjugateTranspose (cascadeLinear S (fun n => responseLinear shift (sw n) k.1 k.2) L)
            (normalizedSpectrum (riesz J) k.1 k.2) d := by
  dsimp only
  rw [actual_response_gradient_update,actual_kernel_spectral_gradient]
  rw [mul_assoc]
  congr 1
  congr 1
  apply sum_congr rfl
  intro k _
  rw [actual_suffix_cotangent]
  rw [← actual_real_network_spectrum P shift pw pb input k.1 k.2 p]

end FullChain
end Harsanyi.Frequency.MatrixBackprop
