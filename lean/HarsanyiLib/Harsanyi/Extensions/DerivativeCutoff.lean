import Harsanyi.Extensions.Attribution
import Harsanyi.Extensions.OrInteraction
import Mathlib.Analysis.Calculus.Deriv.Shift
import Mathlib.Analysis.Calculus.MeanValue
import Mathlib.Data.Finset.Sort

namespace Harsanyi

section Rectangles
variable {E : Type*} [AddCommGroup E] [Module ℝ E]

/-- A genuine one-variable derivative along a coordinate/direction, evaluated at zero. -/
noncomputable def linePartial (f : E → ℝ) (d : E) (z : E) : ℝ :=
  deriv (fun t : ℝ => f (z + t • d)) 0

/-- Existence of this line derivative at every point; no Taylor/analyticity premise. -/
def HasLineDerivatives (f : E → ℝ) (d : E) : Prop :=
  ∀ z, Differentiable ℝ (fun t : ℝ => f (z + t • d))

/-- A finite iterated rectangular difference. The scalar is the step along each direction. -/
noncomputable def rectDifference : List (E × ℝ) → (E → ℝ) → E → ℝ
  | [], f, z => f z
  | (d, a) :: rest, f, z => rectDifference rest f (z + a • d) - rectDifference rest f z

/-- Mixed derivative: take the list's directions from left to right. -/
noncomputable def orderedPartial : List (E × ℝ) → (E → ℝ) → E → ℝ
  | [], f, z => f z
  | (d, _) :: rest, f, z => orderedPartial rest (linePartial f d) z

/-- The classical existence conditions hidden by notation for an iterated mixed derivative.
The step sizes are immaterial: only directions enter the derivative conditions. -/
def OrderedPartialRegular : List (E × ℝ) → (E → ℝ) → Prop
  | [], _ => True
  | (d, _) :: rest, f => HasLineDerivatives f d ∧ OrderedPartialRegular rest (linePartial f d)

theorem deriv_line_eq (f : E → ℝ) (d z : E) (t : ℝ) :
    deriv (fun s : ℝ => f (z + s • d)) t = linePartial f d (z + t • d) := by
  unfold linePartial
  have he : (fun s : ℝ => f ((z + t • d) + s • d)) =
      (fun s : ℝ => (fun u : ℝ => f (z + u • d)) (t + s)) := by
    funext s
    simp [add_smul, add_assoc]
  rw [he]
  simpa only [add_zero] using (deriv_comp_const_add (fun u : ℝ => f (z + u • d)) t (0 : ℝ)).symm

theorem hasLineDerivatives_translate {f : E → ℝ} {d : E}
    (hf : HasLineDerivatives f d) (a : E) : HasLineDerivatives (fun z => f (z + a)) d := by
  intro z
  convert hf (z + a) using 1
  funext t
  abel_nf

theorem linePartial_translate (f : E → ℝ) (d a z : E) :
    linePartial (fun y => f (y + a)) d z = linePartial f d (z + a) := by
  unfold linePartial
  congr 1
  funext t
  abel_nf

theorem linePartial_sub {f g : E → ℝ} {d : E}
    (hf : HasLineDerivatives f d) (hg : HasLineDerivatives g d) (z : E) :
    linePartial (fun y => f y - g y) d z = linePartial f d z - linePartial g d z := by
  exact deriv_sub ((hf z).differentiableAt) ((hg z).differentiableAt)

theorem hasLineDerivatives_rectDifference {f : E → ℝ} {d : E}
    (hf : HasLineDerivatives f d) (moves : List (E × ℝ)) :
    HasLineDerivatives (rectDifference moves f) d := by
  induction moves with
  | nil => exact hf
  | cons p rest ih =>
    rcases p with ⟨e, a⟩
    intro z
    exact ((hasLineDerivatives_translate ih (a • e)) z).sub (ih z)

/-- Differentiation commutes with the finite rectangle's translated finite sums. -/
theorem linePartial_rectDifference {f : E → ℝ} {d : E}
    (hf : HasLineDerivatives f d) (moves : List (E × ℝ)) (z : E) :
    linePartial (rectDifference moves f) d z = rectDifference moves (linePartial f d) z := by
  induction moves generalizing z with
  | nil => rfl
  | cons p rest ih =>
    rcases p with ⟨e, a⟩
    have hr := hasLineDerivatives_rectDifference hf rest
    change linePartial (fun y => rectDifference rest f (y + a • e) - rectDifference rest f y) d z = _
    rw [linePartial_sub (hasLineDerivatives_translate hr (a • e)) hr,
      linePartial_translate, ih, ih]
    rfl

/-- A vanishing actual mixed derivative forces a rectangular finite difference to vanish.
Only the derivative existence for its ordered prefixes is assumed. -/
theorem rectDifference_zero_of_orderedPartial_zero (moves : List (E × ℝ)) (f : E → ℝ)
    (hregular : OrderedPartialRegular moves f) (hzero : ∀ z, orderedPartial moves f z = 0) :
    ∀ z, rectDifference moves f z = 0 := by
  induction moves generalizing f with
  | nil => exact hzero
  | cons p rest ih =>
    rcases p with ⟨d, a⟩
    rcases hregular with ⟨hf, hrest⟩
    have hz : ∀ z, rectDifference rest (linePartial f d) z = 0 :=
      ih (linePartial f d) hrest hzero
    intro z
    have hr := hasLineDerivatives_rectDifference hf rest
    have hderiv : ∀ t : ℝ, deriv (fun s : ℝ => rectDifference rest f (z + s • d)) t = 0 := by
      intro t
      rw [deriv_line_eq, linePartial_rectDifference hf]
      exact hz _
    have he := is_const_of_deriv_eq_zero (hr z) hderiv a 0
    change rectDifference rest f (z + a • d) - rectDifference rest f z = 0
    simpa using sub_eq_zero.mpr he

end Rectangles

section Coordinates
variable {α : Type*} [DecidableEq α]

def coordinateDirection (i : α) : α → ℝ := Pi.single i 1

theorem coordinateCurve_eq_update (z : α → ℝ) (i : α) (t : ℝ) :
    z + t • coordinateDirection i = Function.update z i (z i + t) := by
  funext j
  by_cases hj : j = i
  · subst j
    simp [coordinateDirection]
  · simp [coordinateDirection, hj]

/-- This is exactly the classical partial derivative with the coordinate value as parameter. -/
theorem linePartial_coordinate_eq (f : (α → ℝ) → ℝ) (i : α) (z : α → ℝ) :
    linePartial f (coordinateDirection i) z =
      deriv (fun s : ℝ => f (Function.update z i s)) (z i) := by
  unfold linePartial
  simp_rw [coordinateCurve_eq_update]
  simpa only [add_zero] using
    deriv_comp_const_add (fun s : ℝ => f (Function.update z i s)) (z i) (0 : ℝ)

def coordinateMoves (h : α → ℝ) (indices : List α) : List ((α → ℝ) × ℝ) :=
  indices.map (fun i => (coordinateDirection i, h i))

def incrementCoordinates (z h : α → ℝ) (S : Finset α) : α → ℝ :=
  fun i => z i + if i ∈ S then h i else 0

noncomputable def incrementGame (f : (α → ℝ) → ℝ) (z h : α → ℝ) : Game α :=
  fun S => f (incrementCoordinates z h S)

theorem incrementCoordinates_insert (z h : α → ℝ) (i : α) (U : Finset α) (hi : i ∉ U) :
    incrementCoordinates (z + h i • coordinateDirection i) h U =
      incrementCoordinates z h (insert i U) := by
  funext j
  by_cases hj : j = i
  · subst j
    simp [incrementCoordinates, coordinateDirection, hi]
  · simp [incrementCoordinates, coordinateDirection, hj]

/-- The actual masked-coordinate interaction is the rectangular difference.
No representation of the model by a polynomial is assumed. -/
theorem rectDifference_coordinate_eq_interaction (f : (α → ℝ) → ℝ) (h : α → ℝ)
    (indices : List α) (hnodup : indices.Nodup) (z : α → ℝ) :
    rectDifference (coordinateMoves h indices) f z = interaction (incrementGame f z h) indices.toFinset := by
  induction indices generalizing z with
  | nil =>
    simp only [coordinateMoves, List.map_nil, rectDifference, List.toFinset_nil,
      interaction_empty, incrementGame]
    congr 1
    funext i
    simp [incrementCoordinates]
  | cons i rest ih =>
    rcases List.nodup_cons.mp hnodup with ⟨hi, hrest⟩
    have hi' : i ∉ rest.toFinset := by simpa using hi
    have he : interaction (incrementGame f (z + h i • coordinateDirection i) h) rest.toFinset =
        interaction (fun U => incrementGame f z h (insert i U)) rest.toFinset := by
      apply interaction_congr
      intro U hU
      have hiU : i ∉ U := fun hit => hi' (hU hit)
      simp only [incrementGame, incrementCoordinates_insert z h i U hiU]
    rw [List.toFinset_cons]
    change rectDifference (coordinateMoves h rest) f (z + h i • coordinateDirection i) -
      rectDifference (coordinateMoves h rest) f z =
      interaction (incrementGame f z h) (insert i rest.toFinset)
    rw [ih hrest, ih hrest, he, interaction_context_difference _ _ _ hi']

theorem incrementCoordinates_baseline (r x : α → ℝ) (S : Finset α) :
    incrementCoordinates r (x - r) S = maskCoordinates r x S := by
  funext i
  by_cases hi : i ∈ S <;> simp [incrementCoordinates, maskCoordinates, hi]

/-- Steps do not enter either the derivative or its existence conditions. -/
theorem orderedPartial_coordinate_amplitudes (h h' : α → ℝ) (indices : List α)
    (f : (α → ℝ) → ℝ) (z : α → ℝ) :
    orderedPartial (coordinateMoves h indices) f z =
      orderedPartial (coordinateMoves h' indices) f z := by
  induction indices generalizing f with
  | nil => rfl
  | cons i rest ih =>
    simp only [coordinateMoves, List.map_cons, orderedPartial]
    exact ih (linePartial f (coordinateDirection i))

theorem orderedPartialRegular_coordinate_amplitudes (h h' : α → ℝ) (indices : List α)
    (f : (α → ℝ) → ℝ) :
    OrderedPartialRegular (coordinateMoves h indices) f ↔
      OrderedPartialRegular (coordinateMoves h' indices) f := by
  induction indices generalizing f with
  | nil => rfl
  | cons i rest ih =>
    simp only [coordinateMoves, List.map_cons, OrderedPartialRegular]
    exact and_congr_right (fun _ => ih (linePartial f (coordinateDirection i)))

noncomputable def orderedCoordinatePartial (indices : List α) (f : (α → ℝ) → ℝ) : (α → ℝ) → ℝ :=
  orderedPartial (coordinateMoves (fun _ => 0) indices) f

def OrderedCoordinateRegular (indices : List α) (f : (α → ℝ) → ℝ) : Prop :=
  OrderedPartialRegular (coordinateMoves (fun _ => 0) indices) f

end Coordinates

section FiniteCoordinates
variable {n : ℕ}

/-- Classical coordinate mixed derivatives are encoded by nondecreasing coordinate lists.
The exponent of coordinate i is its number of occurrences; prefixes are the derivatives
whose existence is implicit in classical iterated-partial notation. -/
def HasClassicalMixedDerivatives (f : (Fin n → ℝ) → ℝ) : Prop :=
  ∀ indices : List (Fin n), indices.Sorted (· ≤ ·) → OrderedCoordinateRegular indices f

/-- Full-space mixed-partial cutoff, indexed by the sorted list representing a multi-index. -/
def MixedDerivativeCutoff (f : (Fin n → ℝ) → ℝ) (M : ℕ) : Prop :=
  ∀ indices : List (Fin n), indices.Sorted (· ≤ ·) → M < indices.length →
    ∀ z, orderedCoordinatePartial indices f z = 0

/-- Exact classical source meaning: each requested high-order partial exists and is zero.
Its prefix existence is part of that particular iterated derivative's definition; this
does not demand a separate global existence hypothesis for every lower-order list. -/
def ClassicalMixedDerivativeCutoff (f : (Fin n → ℝ) → ℝ) (M : ℕ) : Prop :=
  ∀ indices : List (Fin n), indices.Sorted (· ≤ ·) → M < indices.length →
    OrderedCoordinateRegular indices f ∧ (∀ z, orderedCoordinatePartial indices f z = 0)

/-- The list encoding preserves the original multi-index total order. -/
theorem coordinate_multiIndex_total_order (indices : List (Fin n)) :
    (∑ i : Fin n, indices.count i) = indices.length := by
  calc
    _ = ∑ i ∈ indices.toFinset, indices.count i := by
      symm
      apply Finset.sum_subset (Finset.subset_univ _)
      intro i _ hi
      apply List.count_eq_zero.mpr
      simpa using hi
    _ = indices.length := List.sum_toFinset_count_eq_length indices

theorem coordinate_multiIndex_finset (S : Finset (Fin n)) (i : Fin n) :
    (S.sort (· ≤ ·)).count i = if i ∈ S then 1 else 0 := by
  rw [List.count_eq_of_nodup (S.sort_nodup _)]
  simp

/-- Only the single mixed derivative attached to S is needed, including its prefix existence. -/
theorem interaction_zero_of_orderedCoordinatePartial_zero (f : (Fin n → ℝ) → ℝ)
    (r x : Fin n → ℝ) (S : Finset (Fin n))
    (hregular : OrderedCoordinateRegular (S.sort (· ≤ ·)) f)
    (hzero : ∀ z, orderedCoordinatePartial (S.sort (· ≤ ·)) f z = 0) :
    interaction (fun U => f (maskCoordinates r x U)) S = 0 := by
  let indices := S.sort (· ≤ ·)
  have hreg : OrderedPartialRegular (coordinateMoves (x - r) indices) f :=
    (orderedPartialRegular_coordinate_amplitudes (x - r) (fun _ => 0) indices f).mpr
      hregular
  have hz : ∀ z, orderedPartial (coordinateMoves (x - r) indices) f z = 0 := by
    intro z
    rw [orderedPartial_coordinate_amplitudes (x - r) (fun _ => 0)]
    exact hzero z
  have hrect := rectDifference_zero_of_orderedPartial_zero
    (coordinateMoves (x - r) indices) f hreg hz r
  rw [rectDifference_coordinate_eq_interaction f (x - r) indices (S.sort_nodup _) r] at hrect
  have hgame : incrementGame f r (x - r) = (fun U => f (maskCoordinates r x U)) := by
    funext U
    simp [incrementGame, incrementCoordinates_baseline]
  simpa [indices, hgame] using hrect

/-- A convenient all-orders regularity variant, separate from the exact paper adapter. -/
theorem interaction_zero_of_mixedDerivativeCutoff (f : (Fin n → ℝ) → ℝ)
    (M : ℕ) (hregular : HasClassicalMixedDerivatives f) (hcutoff : MixedDerivativeCutoff f M)
    (r x : Fin n → ℝ) (S : Finset (Fin n)) (hMS : M < S.card) :
    interaction (fun U => f (maskCoordinates r x U)) S = 0 := by
  exact interaction_zero_of_orderedCoordinatePartial_zero f r x S
    (hregular _ (S.sort_sorted _))
    (hcutoff _ (S.sort_sorted _) (by simpa using hMS))

/-- Specializing the full-space source cutoff to the multi-index with each coordinate
of S once proves the actual masked-coordinate interaction vanishes. -/
theorem interaction_zero_of_classicalMixedDerivativeCutoff (f : (Fin n → ℝ) → ℝ)
    (M : ℕ) (hbeta : ClassicalMixedDerivativeCutoff f M)
    (r x : Fin n → ℝ) (S : Finset (Fin n)) (hMS : M < S.card) :
    interaction (fun U => f (maskCoordinates r x U)) S = 0 := by
  rcases hbeta (S.sort (· ≤ ·)) (S.sort_sorted _) (by simpa using hMS) with ⟨hr, hz⟩
  exact interaction_zero_of_orderedCoordinatePartial_zero f r x S hr hz

theorem centered_interaction_zero_of_classicalMixedDerivativeCutoff (f : (Fin n → ℝ) → ℝ)
    (M : ℕ) (hbeta : ClassicalMixedDerivativeCutoff f M)
    (r x : Fin n → ℝ) (S : Finset (Fin n)) (hMS : M < S.card) :
    interaction (centered (fun U => f (maskCoordinates r x U))) S = 0 := by
  have hS : S ≠ ∅ := by intro he; subst S; simp at hMS
  rw [interaction_centered_nonempty _ S (Finset.nonempty_iff_ne_empty.mpr hS)]
  exact interaction_zero_of_classicalMixedDerivativeCutoff f M hbeta r x S hMS

/-- The centered convention used by ICLR2024 Sparse changes only the empty coefficient. -/
theorem centered_interaction_zero_of_mixedDerivativeCutoff (f : (Fin n → ℝ) → ℝ)
    (M : ℕ) (hregular : HasClassicalMixedDerivatives f) (hcutoff : MixedDerivativeCutoff f M)
    (r x : Fin n → ℝ) (S : Finset (Fin n)) (hMS : M < S.card) :
    interaction (centered (fun U => f (maskCoordinates r x U))) S = 0 := by
  have hS : S ≠ ∅ := by intro he; subst S; simp at hMS
  rw [interaction_centered_nonempty _ S (Finset.nonempty_iff_ne_empty.mpr hS)]
  exact interaction_zero_of_mixedDerivativeCutoff f M hregular hcutoff r x S hMS

end FiniteCoordinates

end Harsanyi
