import Harsanyi.Extensions.TransformationChains

namespace Harsanyi.Entropy
open Finset MeasureTheory
open scoped BigOperators
variable {A B C : Type*} [Fintype A] [Fintype B] [Fintype C]

noncomputable def coarseLabelLaw (p : Law (A × (B × C))) : Law (A × C) where
  mass := fun z => ∑ b, p.mass (z.1,(b,z.2))
  nonneg := fun z => sum_nonneg (fun b _ => p.nonneg _)
  total := by
    have ht := p.total
    simp only [Fintype.sum_prod_type] at ht ⊢
    calc
      _ = ∑ a, ∑ b, ∑ c, p.mass (a,(b,c)) := sum_congr rfl (fun a _ => sum_comm)
      _ = 1 := ht

noncomputable def fineLabelLaw (p : Law (A × (B × C))) : Law ((A × B) × C) where
  mass := fun z => p.mass (z.1.1,(z.1.2,z.2))
  nonneg := fun z => p.nonneg _
  total := by
    change (∑ z, p.mass ((Equiv.prodAssoc A B C) z)) = 1
    rw [Equiv.sum_comp]
    exact p.total

theorem actual_projection_information_monotone (p : Law (A × (B × C))) :
    mutualInformation (coarseLabelLaw p).mass ≤ mutualInformation (fineLabelLaw p).mass := by
  have hd := kernel_disintegration p
  have hc : (kernelLaw (rowLaw p) (fun a => columnLaw (conditionalRow p a))).mass =
      (coarseLabelLaw p).mass := by
    funext z
    change (rowLaw p).mass z.1 * (∑ b, (conditionalRow p z.1).mass (b,z.2)) = _
    rw [mul_sum]
    apply sum_congr rfl
    intro b _
    exact congrFun hd (z.1,(b,z.2))
  have hf : (refinedKernelLaw (rowLaw p) (conditionalRow p)).mass = (fineLabelLaw p).mass := by
    funext z
    exact congrFun hd (z.1.1,(z.1.2,z.2))
  have h := actual_joint_refinement_monotone p
  rw [hc, hf] at h
  exact h

variable {Ω Y : Type*} [MeasurableSpace Ω] [Fintype Y] [DecidableEq A] [DecidableEq B]

/-- Actual joint law of coarse gate, added gate and label for arbitrary inputs. -/
noncomputable def gateRefinementLaw (μ : Measure Ω) [IsProbabilityMeasure μ]
    (f : Ω → A × B) (k : Ω → Law Y)
    (hm : ∀ z, Measurable (fun x => (gateLabelAt f k x).mass z)) : Law (A × (B × Y)) where
  mass := fun z => (gateLabelLaw μ f k hm).mass (z.2.2,(z.1,z.2.1))
  nonneg := fun z => (gateLabelLaw μ f k hm).nonneg _
  total := by
    have ht := (gateLabelLaw μ f k hm).total
    simp only [Fintype.sum_prod_type] at ht ⊢
    calc
      _ = ∑ a, ∑ y, ∑ b, (gateLabelLaw μ f k hm).mass (y,(a,b)) :=
        sum_congr rfl (fun a _ => sum_comm)
      _ = ∑ y, ∑ a, ∑ b, (gateLabelLaw μ f k hm).mass (y,(a,b)) := sum_comm
      _ = 1 := ht

/-- Main Property 2 / Eq.(11), with actual deterministic gates and a conditional
label kernel on any measurable input domain. Conditional information vanishes
by computation of the gate kernel, not by an additional hypothesis. -/
theorem deterministic_gate_refinement_information (μ : Measure Ω) [IsProbabilityMeasure μ]
    (f : Ω → A × B) (k : Ω → Law Y)
    (hm : ∀ z, Measurable (fun x => (gateLabelAt f k x).mass z)) :
    mutualInformation (coarseLabelLaw (gateRefinementLaw μ f k hm)).mass -
        conditionalGateLabelInformation μ (fun x => (f x).1) k ≤
      mutualInformation (fineLabelLaw (gateRefinementLaw μ f k hm)).mass -
        conditionalGateLabelInformation μ f k := by
  simp only [conditional_gate_label_information_zero, sub_zero]
  exact actual_projection_information_monotone _

theorem gate_refinement_pointwise (f : Ω → A × B) (k : Ω → Law Y) (x : Ω) (y : Y) (a : A) :
    (gateLabelAt (fun x => (f x).1) k x).mass (y,a) =
      ∑ b, (gateLabelAt f k x).mass (y,(a,b)) := by
  classical
  by_cases ha : a=(f x).1
  · simp [gateLabelAt, Prod.ext_iff, ha]
  · simp [gateLabelAt, Prod.ext_iff, ha]

theorem actual_gate_projection_mass (μ : Measure Ω) [IsProbabilityMeasure μ]
    (f : Ω → A × B) (k : Ω → Law Y)
    (hm : ∀ z, Measurable (fun x => (gateLabelAt f k x).mass z))
    (hm0 : ∀ z, Measurable (fun x => (gateLabelAt (fun x => (f x).1) k x).mass z)) :
    (columnLaw (gateLabelLaw μ (fun x => (f x).1) k hm0)).mass =
      marginal (columnLaw (gateLabelLaw μ f k hm)).mass := by
  funext a
  change (∑ y, ∫ x, (gateLabelAt (fun x => (f x).1) k x).mass (y,a) ∂μ) =
    ∑ b, ∑ y, ∫ x, (gateLabelAt f k x).mass (y,(a,b)) ∂μ
  simp_rw [gate_refinement_pointwise]
  calc
    _ = ∑ y, ∑ b, ∫ x, (gateLabelAt f k x).mass (y,(a,b)) ∂μ := by
      apply sum_congr rfl
      intro y _
      exact integral_finset_sum _ (fun b _ => gate_label_mass_integrable μ f k (y,(a,b)) (hm _))
    _ = _ := sum_comm

theorem deterministic_input_gate_refinement (μ : Measure Ω) [IsProbabilityMeasure μ]
    (f : Ω → A × B) (k : Ω → Law Y)
    (hm : ∀ z, Measurable (fun x => (gateLabelAt f k x).mass z))
    (hm0 : ∀ z, Measurable (fun x => (gateLabelAt (fun x => (f x).1) k x).mass z)) :
    deterministicInputInformation μ (fun x => (f x).1) k hm0 ≤
      deterministicInputInformation μ f k hm := by
  rw [deterministic_input_information_eq_entropy, deterministic_input_information_eq_entropy,
    actual_gate_projection_mass μ f k hm hm0]
  exact entropy_marginal_le _ (columnLaw _).nonneg

variable {T : Type*} [MeasurableSpace T]

/-- The later-gate law computed from an actual intermediate-feature pushforward
equals the same gate law on the original sample space. -/
theorem gate_label_law_pushforward (μ : Measure Ω) [IsProbabilityMeasure μ]
    (t : Ω → T) (ht : Measurable t) [IsProbabilityMeasure (μ.map t)]
    (f : T → A) (k : T → Law Y)
    (hm : ∀ z, Measurable (fun x => (gateLabelAt f k x).mass z))
    (hmc : ∀ z, Measurable (fun x => (gateLabelAt (f ∘ t) (k ∘ t) x).mass z)) :
    (gateLabelLaw (μ.map t) f k hm).mass =
      (gateLabelLaw μ (f ∘ t) (k ∘ t) hmc).mass := by
  funext z
  exact integral_map ht.aemeasurable (hm z).aestronglyMeasurable

/-- Full source suffix-input comparison: later gates depend on T_l=t(T_{l-1}),
and the actual law of T_l is the pushforward of the previous feature law. -/
theorem deterministic_input_suffix (μ : Measure Ω) [IsProbabilityMeasure μ]
    (t : Ω → T) (ht : Measurable t) [IsProbabilityMeasure (μ.map t)]
    (later : T → A) (first : Ω → B) (k : T → Law Y)
    (hm : ∀ z, Measurable (fun x => (gateLabelAt later k x).mass z))
    (hmc : ∀ z, Measurable (fun x => (gateLabelAt (later ∘ t) (k ∘ t) x).mass z))
    (hmf : ∀ z, Measurable (fun x => (gateLabelAt (fun x => (later (t x),first x)) (k ∘ t) x).mass z)) :
    deterministicInputInformation (μ.map t) later k hm ≤
      deterministicInputInformation μ (fun x => (later (t x),first x)) (k ∘ t) hmf := by
  have hp := deterministic_input_gate_refinement μ
    (fun x => (later (t x),first x)) (k ∘ t) hmf hmc
  have he := gate_label_law_pushforward μ t ht later k hm hmc
  rw [deterministic_input_information_eq_entropy] at hp ⊢
  have hc : (columnLaw (gateLabelLaw (μ.map t) later k hm)).mass =
      (columnLaw (gateLabelLaw μ (later ∘ t) (k ∘ t) hmc)).mass := by
    funext a
    change (∑ y, (gateLabelLaw (μ.map t) later k hm).mass (y,a)) = _
    apply sum_congr rfl
    intro y _
    exact congrFun he (y,a)
  rw [hc]
  exact hp

end Harsanyi.Entropy
