# F07/F08/F10 coverage and shared proof plan

The official files contain 36 + 25 + 22 = 83 physical pages. F10's official supplemental URL is byte-identical to the main file and is not a second source. Ownership is limited to the three paper directories, independent new extension modules and per-paper verification scripts. No global manifest, barrel, historical evidence, staging or publication is changed here.

Inventory records 19 / 16 / 13 reading entries, including definitions, external statements, algorithms and empirical results. Proof/argument targets retain source and appendix aliases. All 83 pages have a classification and source text evidence, including references and the NeurIPS checklist. Full mathematical transcriptions are authored separately: page text is evidence, never labelled a full TeX proof.

Reusable verified dependencies:

- `Harsanyi.reconstruction`, `interaction_reconstruct`, `reconstruction_unique`: exact finite Boolean Möbius inversion with the raw empty baseline.
- `Harsanyi.or_dual` and existing split reconstruction: fixed AND/OR components, with the component baselines explicit.
- `Harsanyi.noisy_and_identity`, `signed_gaussian_variance`: exact noisy dividend identity; the Gaussian variance theorem requires the actual independent law. F07 Lemma 1's printed marginal-only statement is audited separately rather than silently strengthened.
- New `TaylorMoments.lean`: finite monomial masking/support, normalized nonzero trigger identity, actual independent-product first/second moment/variance identities; usable by all three adapters. No unrestricted analytic Taylor conclusion is inferred from a finite polynomial theorem.
- New `NoisyRegression.lean`: Boolean zeta injectivity, Gram positive definiteness, nonnegative diagonal regularization and quadratic minimization; diagonal independent-feature regression scaling shared with F08 and F10. Paper adapters state their exact finite setup.

Potential source issues are kept in their original position and investigated individually: unrestricted Taylor equalities for ReLU networks, input-dependent signs in odd monomials, nondegenerate Gaussian tails versus hard sign preservation, zero interaction denominators, missing noise independence, the F07 Gram determinant argument and transposed output vector, the F10 G.4 binomial factor/inner degree index, and unqualified zero-variance regression ratios. Proof-only corrections do not change original hypotheses or statements. Each surviving valid target receives a complete bilingual proof and actual declaration; false or undefined clauses receive precise source-local evidence and a separate formal counterexample where possible.

The aggregate external-properties entry will be split into seven individually searchable axioms. Appendix B's three sparsity conditions will likewise be separate source statements. F07 Appendix C is optimization, not Shapley: the initial label is corrected after the full page review. F07 Appendix C also prints both decomposition branches with the same sign in its noise-removal paragraph; this is retained as a source equation issue, not silently corrected in transcription.
