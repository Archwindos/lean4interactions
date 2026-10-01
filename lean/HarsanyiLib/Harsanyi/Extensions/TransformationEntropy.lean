import Mathlib.Analysis.SpecialFunctions.Log.NegMulLog
import Mathlib.Analysis.SpecialFunctions.BinaryEntropy
import Mathlib.Data.Fintype.BigOperators
import Mathlib.Tactic

/-! Finite Shannon entropy. Zero-mass summands are zero; no conditional probability
is required at a zero-mass event. This module is independent of neural networks. -/
namespace Harsanyi.Entropy
open Finset
open scoped BigOperators
variable {A B : Type*} [Fintype A] [Fintype B]

structure Law (A : Type*) [Fintype A] where
  mass : A → ℝ
  nonneg : ∀ a, 0 ≤ mass a
  total : ∑ a, mass a = 1

noncomputable def entropy (p : A → ℝ) : ℝ := ∑ a, Real.negMulLog (p a)
noncomputable def marginal (p : A × B → ℝ) (a : A) : ℝ := ∑ b, p (a,b)
noncomputable def conditionalEntropy (p : A × B → ℝ) : ℝ :=
  ∑ a, marginal p a * entropy (fun b => p (a,b) / marginal p a)
noncomputable def mutualInformation (p : A × B → ℝ) : ℝ :=
  entropy (marginal p) + entropy (fun b => ∑ a, p (a,b)) - entropy p
noncomputable def divergence (p q : A → ℝ) : ℝ :=
  ∑ a, p a * Real.log (p a / q a)

 theorem law_mass_le_one (p : Law A) (a : A) : p.mass a ≤ 1 := by
  rw [← p.total]
  exact single_le_sum (fun b _ => p.nonneg b) (mem_univ a)

 theorem entropy_nonneg (p : Law A) : 0 ≤ entropy p.mass := by
  apply sum_nonneg
  intro a _
  exact Real.negMulLog_nonneg (p.nonneg a) (law_mass_le_one p a)

 theorem marginal_nonneg (p : A × B → ℝ) (hp : ∀ x, 0 ≤ p x) (a : A) :
    0 ≤ marginal p a := sum_nonneg (fun b _ => hp (a,b))

 theorem mass_le_marginal (p : A × B → ℝ) (hp : ∀ x, 0 ≤ p x) (a : A) (b : B) :
    p (a,b) ≤ marginal p a := single_le_sum (fun c _ => hp (a,c)) (mem_univ b)

 theorem mass_zero_of_marginal_zero (p : A × B → ℝ) (hp : ∀ x, 0 ≤ p x)
    (a : A) (h : marginal p a = 0) (b : B) : p (a,b) = 0 := by
  have hh := mass_le_marginal p hp a b
  rw [h] at hh
  exact le_antisymm hh (hp (a,b))

 theorem entropy_chain (p : A × B → ℝ) (hp : ∀ x, 0 ≤ p x) :
    entropy p = entropy (marginal p) + conditionalEntropy p := by
  classical
  unfold entropy conditionalEntropy
  rw [Fintype.sum_prod_type, ← sum_add_distrib]
  apply sum_congr rfl
  intro a _
  by_cases hm : marginal p a = 0
  · simp [hm, mass_zero_of_marginal_zero p hp a hm]
  · have he (b : B) : p (a,b) = marginal p a * (p (a,b) / marginal p a) := by
      field_simp
    calc
      (∑ b, Real.negMulLog (p (a,b))) =
          ∑ b, ((p (a,b) / marginal p a) * Real.negMulLog (marginal p a) +
            marginal p a * Real.negMulLog (p (a,b) / marginal p a)) := by
              apply sum_congr rfl
              intro b _
              conv_lhs => rw [he b, Real.negMulLog_mul]
      _ = Real.negMulLog (marginal p a) +
          marginal p a * ∑ b, Real.negMulLog (p (a,b) / marginal p a) := by
            rw [sum_add_distrib, ← sum_mul, ← mul_sum, ← sum_div]
            change (marginal p a / marginal p a) * _ + _ = _
            rw [div_self hm, one_mul]

 theorem conditional_entropy_nonneg (p : A × B → ℝ) (hp : ∀ x, 0 ≤ p x) :
    0 ≤ conditionalEntropy p := by
  apply sum_nonneg
  intro a _
  by_cases hm : marginal p a = 0
  · simp [hm]
  · have hmpos : 0 < marginal p a := lt_of_le_of_ne (marginal_nonneg p hp a) (Ne.symm hm)
    apply mul_nonneg hmpos.le
    apply sum_nonneg
    intro b _
    exact Real.negMulLog_nonneg (div_nonneg (hp (a,b)) hmpos.le)
      ((div_le_one hmpos).2 (mass_le_marginal p hp a b))

 theorem entropy_marginal_le (p : A × B → ℝ) (hp : ∀ x, 0 ≤ p x) :
    entropy (marginal p) ≤ entropy p := by
  rw [entropy_chain p hp]
  exact le_add_of_nonneg_right (conditional_entropy_nonneg p hp)

 theorem gibbs_term (p q : ℝ) (hp : 0 ≤ p) (hq : 0 ≤ q)
    (hs : p ≠ 0 → q ≠ 0) : p - q ≤ p * Real.log (p/q) := by
  by_cases h : p = 0
  · simp [h]; exact hq
  have pp : 0 < p := lt_of_le_of_ne hp (Ne.symm h)
  have qq : 0 < q := lt_of_le_of_ne hq (Ne.symm (hs h))
  have hh := mul_le_mul_of_nonneg_left (Real.log_le_sub_one_of_pos (div_pos qq pp)) hp
  rw [Real.log_div qq.ne' pp.ne'] at hh
  rw [Real.log_div pp.ne' qq.ne']
  have hdiv : p * (q/p - 1) = q-p := by field_simp
  rw [hdiv] at hh
  nlinarith

 theorem divergence_nonneg (p q : Law A) (hs : ∀ a, p.mass a ≠ 0 → q.mass a ≠ 0) :
    0 ≤ divergence p.mass q.mass := by
  have hh := sum_le_sum (fun a (_ : a ∈ (univ : Finset A)) =>
    gibbs_term (p.mass a) (q.mass a) (p.nonneg a) (q.nonneg a) (hs a))
  simpa [divergence, sum_sub_distrib, p.total, q.total] using hh

 theorem gibbs_term_strict (p q : ℝ) (hp : 0 ≤ p) (hq : 0 ≤ q)
    (hs : p ≠ 0 → q ≠ 0) (hne : p ≠ q) : p-q < p*Real.log (p/q) := by
  by_cases h : p=0
  · have hqpos : 0<q := lt_of_le_of_ne hq (by simpa [h] using hne)
    simp [h]; exact hqpos
  have pp : 0 < p := lt_of_le_of_ne hp (Ne.symm h)
  have qq : 0 < q := lt_of_le_of_ne hq (Ne.symm (hs h))
  have hr : q/p ≠ 1 := by intro he; have hqp := (div_eq_one_iff_eq h).mp he; exact hne hqp.symm
  have hh := mul_lt_mul_of_pos_left (Real.log_lt_sub_one_of_pos (div_pos qq pp) hr) pp
  rw [Real.log_div qq.ne' pp.ne'] at hh
  rw [Real.log_div pp.ne' qq.ne']
  have hdiv : p*(q/p-1)=q-p := by field_simp
  rw [hdiv] at hh
  nlinarith

 theorem divergence_zero_iff (p q : Law A) (hs : ∀ a, p.mass a ≠ 0 → q.mass a ≠ 0) :
    divergence p.mass q.mass = 0 ↔ p.mass = q.mass := by
  constructor
  · intro hz; funext a
    by_contra ha
    have hall (b : A) : 0 ≤ p.mass b*Real.log (p.mass b/q.mass b)-p.mass b+q.mass b := by
      have h := gibbs_term _ _ (p.nonneg b) (q.nonneg b) (hs b); linarith
    have ha' : 0 < p.mass a*Real.log (p.mass a/q.mass a)-p.mass a+q.mass a := by
      have h := gibbs_term_strict _ _ (p.nonneg a) (q.nonneg a) (hs a) ha; linarith
    have hsum := single_le_sum (fun b _ => hall b) (mem_univ a)
    have he : (∑ b, (p.mass b*Real.log (p.mass b/q.mass b)-p.mass b+q.mass b)) = 0 := by
      change (∑ b, p.mass b*Real.log (p.mass b/q.mass b)) = 0 at hz
      simp [sum_add_distrib, sum_sub_distrib, hz, p.total, q.total]
    rw [he] at hsum
    linarith
  · intro h; unfold divergence
    apply sum_eq_zero
    intro a _
    by_cases ha : p.mass a=0
    · simp [ha]
    · rw [← h, div_self ha, Real.log_one, mul_zero]

noncomputable def rowLaw (p : Law (A × B)) : Law A where
  mass := marginal p.mass
  nonneg := marginal_nonneg p.mass p.nonneg
  total := by simpa [marginal, Fintype.sum_prod_type] using p.total

noncomputable def columnLaw (p : Law (A × B)) : Law B where
  mass := fun b => ∑ a, p.mass (a,b)
  nonneg := fun b => sum_nonneg (fun a _ => p.nonneg (a,b))
  total := by rw [sum_comm]; simpa [Fintype.sum_prod_type] using p.total

noncomputable def independentLaw (p : Law A) (q : Law B) : Law (A × B) where
  mass := fun x => p.mass x.1 * q.mass x.2
  nonneg := fun x => mul_nonneg (p.nonneg x.1) (q.nonneg x.2)
  total := by simp [Fintype.sum_prod_type, ← mul_sum, ← sum_mul, p.total, q.total]

 theorem mutual_information_eq_divergence (p : Law (A × B)) :
    mutualInformation p.mass =
      divergence p.mass (independentLaw (rowLaw p) (columnLaw p)).mass := by
  classical
  have term (a : A) (b : B) :
      p.mass (a,b) * Real.log (p.mass (a,b) /
        (marginal p.mass a * ∑ a', p.mass (a',b))) =
      -Real.negMulLog (p.mass (a,b)) - p.mass (a,b) * Real.log (marginal p.mass a) -
        p.mass (a,b) * Real.log (∑ a', p.mass (a',b)) := by
    by_cases h : p.mass (a,b) = 0
    · simp [h]
    have hh : 0 < p.mass (a,b) := lt_of_le_of_ne (p.nonneg _) (Ne.symm h)
    have ha := lt_of_lt_of_le hh (mass_le_marginal p.mass p.nonneg a b)
    have hb : 0 < ∑ a', p.mass (a',b) := lt_of_lt_of_le hh
      (single_le_sum (fun a' _ => p.nonneg (a',b)) (mem_univ a))
    rw [Real.log_div h (mul_pos ha hb).ne', Real.log_mul ha.ne' hb.ne']
    simp [Real.negMulLog]; ring
  unfold mutualInformation divergence entropy
  simp only [independentLaw, rowLaw, columnLaw, Fintype.sum_prod_type]
  simp_rw [term, sum_sub_distrib]
  rw [sum_comm (f := fun a b => p.mass (a,b) * Real.log (∑ a', p.mass (a',b)))]
  simp_rw [← sum_mul]
  simp only [Real.negMulLog, marginal]
  simp_rw [neg_mul, sum_neg_distrib]
  ring

 theorem mutual_information_nonneg (p : Law (A × B)) : 0 ≤ mutualInformation p.mass := by
  rw [mutual_information_eq_divergence p]
  apply divergence_nonneg
  intro x h
  apply mul_ne_zero
  · exact ne_of_gt (lt_of_lt_of_le (lt_of_le_of_ne (p.nonneg x) (Ne.symm h))
      (mass_le_marginal p.mass p.nonneg x.1 x.2))
  · exact ne_of_gt (lt_of_lt_of_le (lt_of_le_of_ne (p.nonneg x) (Ne.symm h))
      (single_le_sum (fun a _ => p.nonneg (a,x.2)) (mem_univ x.1)))

 theorem entropy_subadditive (p : Law (A × B)) :
    entropy p.mass ≤ entropy (rowLaw p).mass + entropy (columnLaw p).mass := by
  have := mutual_information_nonneg p
  change 0 ≤ entropy (rowLaw p).mass + entropy (columnLaw p).mass - entropy p.mass at this
  linarith

 theorem co_information_identity (h0 hi hj hij : ℝ) :
    hij-hi-hj+h0 = (h0-hi)-(hj-hij) := by ring

 theorem exclusive_shared_identity (h0 hi hj hij : ℝ) :
    h0-hij = (hj-hij)+(hi-hij)+(hij-hi-hj+h0) := by ring

 theorem binary_entropy_half : Real.binEntropy (1/2) = Real.log 2 := by
  simpa using Real.binEntropy_two_inv

end Harsanyi.Entropy

namespace Harsanyi.Entropy
open Finset
open scoped BigOperators
variable {A B : Type*} [Fintype A] [Fintype B]
 theorem conditional_entropy_graph [DecidableEq B] (p : Law (A × B)) (f : A → B)
    (hg : ∀ a b, b ≠ f a → p.mass (a,b)=0) : conditionalEntropy p.mass = 0 := by
  classical
  unfold conditionalEntropy
  apply sum_eq_zero
  intro a _
  by_cases hm : marginal p.mass a=0
  · simp [hm]
  · have hf : marginal p.mass a = p.mass (a,f a) := by
      unfold marginal
      apply sum_eq_single (f a)
      · intro b _ h; exact hg a b h
      · simp
    have he : entropy (fun b => p.mass (a,b) / marginal p.mass a) = 0 := by
      unfold entropy
      apply sum_eq_zero
      intro b _
      by_cases hb : b=f a
      · subst b; change Real.negMulLog (p.mass (a,f a)/marginal p.mass a)=0; rw [← hf, div_self hm]; simp
      · simp [hg a b hb]
    rw [he, mul_zero]

 theorem mutual_information_graph [DecidableEq B] (p : Law (A × B)) (f : A → B)
    (hg : ∀ a b, b ≠ f a → p.mass (a,b)=0) :
    mutualInformation p.mass = entropy (columnLaw p).mass := by
  unfold mutualInformation
  rw [entropy_chain p.mass p.nonneg, conditional_entropy_graph p f hg]
  change entropy (marginal p.mass) + entropy (columnLaw p).mass -
    (entropy (marginal p.mass)+0) = _
  ring

noncomputable def bitLaw : Law Bool where
  mass := fun _ => 1/2
  nonneg := by intro b; norm_num
  total := by simp [Fintype.sum_bool] <;> norm_num
noncomputable def sameBit : Law (Bool × Bool) where
  mass := fun x => if x.1=x.2 then 1/2 else 0
  nonneg := by intro b; split_ifs <;> norm_num
  total := by simp [Fintype.sum_prod_type, Fintype.sum_bool] <;> norm_num
noncomputable def constantGate : Law (Bool × Bool) where
  mass := fun x => if x.2=true then 1/2 else 0
  nonneg := by intro b; split_ifs <;> norm_num
  total := by simp [Fintype.sum_prod_type, Fintype.sum_bool] <;> norm_num
 theorem bit_entropy : entropy bitLaw.mass = Real.log 2 := by
  simp [entropy, bitLaw, Fintype.sum_bool, Real.negMulLog, one_div, Real.log_inv]
 theorem same_bit_information : mutualInformation sameBit.mass = Real.log 2 := by
  rw [mutual_information_graph sameBit id]
  · simpa [entropy, columnLaw, sameBit, bitLaw, Fintype.sum_bool] using bit_entropy
  · intro a b h; simp only [sameBit, id_eq] at *; simp [Ne.symm h]
 theorem constant_gate_information : mutualInformation constantGate.mass = 0 := by
  rw [mutual_information_graph constantGate (fun _ => true)]
  · norm_num [entropy, columnLaw, constantGate, Fintype.sum_bool]
  · intro a b h; simp [constantGate, h]
 theorem prefix_direction_counterexample :
    ¬(mutualInformation sameBit.mass ≤ mutualInformation constantGate.mass) := by
  rw [same_bit_information, constant_gate_information]
  exact not_le.mpr (Real.log_pos (by norm_num : (1:ℝ)<2))
noncomputable def signedInput (b : Bool) : ℝ := if b then 1 else -1
noncomputable def firstFeature (b : Bool) : ℝ := max 0 (signedInput b+2)
 theorem first_relu_gate_constant (b : Bool) : 0 < signedInput b+2 := by
  cases b <;> norm_num [signedInput]
 theorem second_relu_gate_label (b : Bool) : (0< firstFeature b-2) ↔ b=true := by
  cases b <;> norm_num [firstFeature,signedInput]
 theorem two_point_kde_counterexample (κ : ℝ) (hk : 0<κ) :
    Real.log 2 - Real.log (1+Real.exp (-2/κ)) < Real.log 2 := by
  have hh : 1 < 1+Real.exp (-2/κ) := by have := Real.exp_pos (-2/κ); linarith
  have := Real.log_pos hh
  linarith
end Harsanyi.Entropy
