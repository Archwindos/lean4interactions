import Harsanyi.Extensions.TransformationFinite
import Harsanyi.Extensions.TransformationGates

namespace Harsanyi.Entropy
universe u
open Finset MeasureTheory
open scoped BigOperators

def LayerState (G : ℕ → Type u) : ℕ → Type u
  | 0 => PUnit.{u+1}
  | n+1 => LayerState G n × G n

noncomputable instance layerStateFintype (G : ℕ → Type u) [∀ n, Fintype (G n)] :
    ∀ n, Fintype (LayerState G n)
  | 0 => inferInstanceAs (Fintype PUnit.{u+1})
  | n+1 => @instFintypeProd _ _ (layerStateFintype G n) (inferInstanceAs (Fintype (G n)))

noncomputable def initialLayerLaw : Law PUnit.{u+1} where
  mass := fun _ => 1
  nonneg := fun _ => by norm_num
  total := by simp

noncomputable def layerChainLaw (G : ℕ → Type u) [∀ n, Fintype (G n)]
    (k : ∀ n, LayerState G n → Law (G n)) : ∀ n, Law (LayerState G n)
  | 0 => initialLayerLaw
  | n+1 => kernelLaw (layerChainLaw G k n) (k n)

/-- Full arbitrary-depth entropy chain for actual successive conditional laws;
each extension is the genuine joint law, not an assumed entropy increment. -/
theorem layer_chain_entropy (G : ℕ → Type u) [∀ n, Fintype (G n)]
    (k : ∀ n, LayerState G n → Law (G n)) (L : ℕ) :
    entropy (layerChainLaw G k L).mass =
      ∑ n ∈ range L, ∑ s, (layerChainLaw G k n).mass s * entropy (k n s).mass := by
  induction L with
  | zero => simp [layerChainLaw, initialLayerLaw, entropy]
  | succ L ih =>
    change entropy (kernelLaw (layerChainLaw G k L) (k L)).mass = _
    rw [entropy_kernel, ih, sum_range_succ]

noncomputable def deterministicInputInformation {Ω G Y : Type*} [MeasurableSpace Ω]
    [Fintype G] [Fintype Y] [DecidableEq G]
    (μ : Measure Ω) [IsProbabilityMeasure μ] (f : Ω → G) (k : Ω → Law Y)
    (hm : ∀ z, Measurable (fun x => (gateLabelAt f k x).mass z)) : ℝ :=
  entropy (columnLaw (gateLabelLaw μ f k hm)).mass - conditionalGateEntropy μ f k

theorem deterministic_input_information_eq_entropy {Ω G Y : Type*} [MeasurableSpace Ω]
    [Fintype G] [Fintype Y] [DecidableEq G]
    (μ : Measure Ω) [IsProbabilityMeasure μ] (f : Ω → G) (k : Ω → Law Y)
    (hm : ∀ z, Measurable (fun x => (gateLabelAt f k x).mass z)) :
    deterministicInputInformation μ f k hm = entropy (columnLaw (gateLabelLaw μ f k hm)).mass := by
  simp [deterministicInputInformation, conditional_gate_entropy_zero]

end Harsanyi.Entropy
