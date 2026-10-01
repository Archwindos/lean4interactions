# F07 independent regression cross-review

Reviewer: `twelve_foundations_math`. This review reads the formal PDF, the current reader statements and steps, and actual Lean proofs/types; it does not infer correctness from status fields. The assigned targets are `dyn-regression`, `dyn-equal-order` and `dyn-zero-noise` (Theorems 3–5).

## Passed mathematical and machine checks

The three targets pass within their explicitly stated, given-defined Boolean regression model. I read/rendered formal PDF pages 8–9 and 21–24, compared Theorem 3/4/5 and Appendix F.4/F.6/F.7, and read the full `GaussianRegression.lean`, `NoisyRegression.lean` and `PaperDynamics.lean` implementations. Upstream Taylor convergence, zero-normalized-trigger definitions and main/component AND scope remain separate; this review does not reclassify those issues.

**Expected loss and argmin.** The source Assumption 1 supplies independent trigger coordinates with variances `2^{|T|} σ²`; preceding source discussion supplies centering. `independent_residual` genuinely derives finite weighted-sum mean and variance from `iIndepFun` plus `MemLp 2`, using independence and variance identities. No desired cross-moment or expected quadratic is assumed. `noisyLoss_expansion` sums these actual integrals over every `Finset α` and obtains the correct penalty coefficient `Fintype.card (Finset α) * q T`. The separate `meanNoisyLoss` is the reciprocal-cardinality multiple of that sum, and `meanNoisyLoss_unique_min` proves strict global inequality for every competing vector, not just a stationary equation. `Fintype.card_finset = 2 ^ Fintype.card α` identifies this cardinality with the source normalization. The source labels are `y=Jw*`, consistent with row masks and column concepts; the original F.4 transposed label typo is already retained/flagged.

Representing the row-noise marginal by a common random family is sufficient for the sum of row expectations: cross-row independence is unnecessary, and it does not assert that the source physically uses perfectly correlated rows. The current reader explicitly explains this. Generic `q` with true variance and nonnegativity covers the source `q_T=2^{|T|}σ²`; nonnegativity is a legitimate variance property, rather than a premise encoding the target.

**Zeta invertibility and zero noise.** `zeta` is exactly `1_{T⊆S}`, including the empty row and column. `zeta_mulVec` identifies it with finite subset reconstruction; `zeta_injective` applies the existing proved Möbius inversion, then `gram_posDef` proves the full Gram matrix positive definite. This removes the false source argument equating determinant with product of diagonal entries. Nonnegative regularization preserves positive definiteness, including `σ=0`. The implementation proves normal-equation solvability and completes the quadratic square to obtain a unique global minimum. `zero_noise_recovery` cancels the actual invertible Gram matrix and restores every coordinate, including `w_∅*=b`, without assuming a zero output baseline. This implies the source nonempty-coordinate Theorem 5.

**Equal-order norms.** `exists_coalition_permutation` constructs a bijection between equal-cardinality coalitions and extends it using a bijection between their complements. It therefore acts on the whole universe and induces `e.finsetCongr` on the whole powerset. `zeta_permutation` preserves actual subset inclusion. `transfer_permutation` conjugates the entire Gram matrix, the order-dependent diagonal and the actual inverse, rather than swapping two arbitrary rows. `row_norm_permutation` reindexes the full column sum. `PaperDynamics.equal_order_norm` uses the original cardinality/`2^{|T|}` penalty and applies `Real.sqrt` to the proved equal squared norms. Zero noise is included. Its arbitrary real parameter is an algebraic extension of the symmetry identity; the source probabilistic interpretation only uses the nonnegative variance `σ²`.

## Concrete remaining source-error annotations

These do not invalidate the repaired proofs, but the reader's issue list should expose them under the proof-only correction contract.

1. **F.4 PDF21 Equation (46) drops `2^{-n}` from the derivative equality.** Equation (45) contains the normalized loss; its literal derivative is `2^{-n}[-2 E[(J+E)^T]y + 2 E[(J+E)^T(J+E)]w]`. Multiplication by the positive constant gives the same zero normal equation, so Equation (47) and the final argmin are unaffected. The current original transcription faithfully keeps the missing factor, and the repaired objective/argmin correctly preserve normalization. Add a precise source proof-error note, without calling Theorem 3 false.
2. **F.6 PDF23 assumes `P_i²=I` after introducing each `P_i` only as a permutation matrix.** A 3-cycle is a permutation whose square is not the identity. Choosing a transposition decomposition would justify that source intermediate sentence, or using `P^{-1}` works for every permutation. The actual rewrite and code use whole-permutation conjugation with its inverse, so the original same-order statement is proved. Add the original involution qualification as a proof-only source note; do not turn it into a new assumption of Theorem 4.

No additional missing mathematical step was found in the assigned three current adapters. Acceptance of source completeness, other targets and global interfaces remains with root.

## Independent evidence

I independently compiled an audit consisting of the current `PaperDynamics.lean` source followed by actual `#print` and `#print axioms` commands for 11 key declarations, including expected residual, injectivity, Gram positive definiteness, unique minimizer, coalition permutation, transfer conjugation, equal-order norm and zero-noise recovery. Command: `source scripts/env.sh; lake -d lean/HarsanyiLib env lean .tmp/f07-cross-review/AuditF07Cross.lean`. Exit code 0; no `sorryAx`; only `propext`, `Classical.choice`, `Quot.sound`. Output is `.tmp/f07-cross-review/actual-types-and-axioms.log`. The package report source hashes were independently compared with all actual files, with zero stale sources; its current declaration count is 75. The original source PDF has 36 physical pages and hash shown below.

```json
{
  "corpus/public/reader/neurips2024-dynamics/content.json": "6057ce756011834466df1ef001ab0f159a8534ee889590250a13227cf08b6458",
  "corpus/public/reader/neurips2024-dynamics/verification/report.json": "307f46d0f15a6832709cda2886e0b46429410c6f17c148a372d5438adf25cba8",
  "corpus/public/reader/neurips2024-dynamics/sources/formal.pdf": "b1d21ad46c8bfb94ce511840d31a700cfa94692e80ddbefc9daa6b58304ac276",
  "corpus/public/reader/neurips2024-dynamics/lean/PaperDynamics.lean": "1f844e75b1ff9f7ce167be54a72ae1a9ce1a94096796a8c9f54138fdc699bc96",
  "lean/HarsanyiLib/Harsanyi/Extensions/NoisyRegression.lean": "b26c3f30819a35280b1341f6eb0b81987a8e296a97bd0f445314d32e8cf2d13b",
  "lean/HarsanyiLib/Harsanyi/Extensions/GaussianRegression.lean": "c82952b61095b93d2308940fa8a97d07fa42f88cd92af64699eeceee15f6241d"
}
```
