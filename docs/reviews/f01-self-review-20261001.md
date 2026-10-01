# F01 final-package self-review

This is the author's implementation review, pending independent root and cross review. It does not record user acceptance. The selected formal paper is **A Unified Game-Theoretic Interpretation of Adversarial Robustness**; the official landing page's **Towards a Unified Game-Theoretic View of Adversarial Perturbations and Robustness** names the same published source. No arXiv substitute is used.

## Source and denominator

The main PDF has 14 physical pages, SHA256 `bb6761a34e1175bebeef66cadb0f3d49f4f1793fa8e1c64e33bb776209bbc70f`. Its separate formal supplement has 16 pages, SHA256 `95938634ace8a0ff3762f1ee74292d0af234487e3a61faf832c59a3d94a5d89b`. Both metadata and inventory bind these same files, hashes and page counts. All 30 pages have explicit page-audit rows, including references and checklist pages. Source evidence files retain page-specific extraction separately from the manual author transcriptions.

The package has 27 reader entries and 26 explicit proof targets. The definition entry alone is outside the proof denominator. The denominator includes the false dropout clause, the D-domain target, the heuristic/scope target and the externally cited uniqueness target. These are not removed by their evidence roles. The 16 local-author-proof entries contain manually transcribed author prose and TeX, with their complete proof-page ranges. The four classical Shapley properties are separate externally attributed source statements with project proofs, rather than fabricated local author proofs. Weber uniqueness remains an external statement without a local proof.

Main pages 4–5, 7–10 and supplementary A–H carry the mathematical statements/derivations. Supplementary E's entropy/log-score explanation, F's repeated output decomposition and D definition, and G's highest-order accumulation formula and detection interpretation have searchable source occurrences. Repeated formulas are merged into their existing targets with all source positions retained. The remaining main/supplementary empirical, background, reference and checklist pages are audited explicitly; empirical conclusions are located in the scope entry rather than promoted to universal theorems.

## Real formal evidence

`lean/HarsanyiLib/Harsanyi/Extensions/RobustnessFinite.lean` builds by direct import, without changing the common barrel. `verification/report.json` reports 80 actual declarations, with exact elaborated types, fresh source hashes and successful module/adapter/axiom audit commands. Dependencies use only `propext`, `Classical.choice` and `Quot.sound`; no `sorryAx` is accepted.

The formalization uses actual `Finset.powersetCard` context averages and their real cardinality normalization. The attribution recurrence is proved by finite flagged-set bijections, not by assuming the recurrence. Telescoping gives accumulation. Classical factorial Shapley allocation is identified with uniform order averages, and the existing dividend-allocation library supplies efficiency. Reordering the resulting triangular finite sum gives exactly the original `(n−1−m)/(n(n−1))` pair weights. Weak cooperation premises yield an actual swap-invariant game, then actual context relabeling proves symmetry. The classic interaction index adapter takes the difference of two factorial Shapley values on the reduced player universe, and proves its equal-order-average relation.

Evidence roles: 22 theorem-proof entries, one counterexample, one partial component and three entries with no whole-target Lean proof. Source statement assessment, rewrite role and evidence role are separate. Definition steps may link to actual declarations without claiming the definition is a theorem.

## Precise remaining formal scope

- `robustness-classical-uniqueness`: the externally cited characterization/uniqueness theorem is not formalized. The four axiom properties have actual adapters, which do not prove their uniqueness.
- `robustness-inference-heuristics`: no formal theorem proves universal perturbation sensitivity, entropy/log-score trend, detector success or defense success. The source itself supplies qualified explanations and experiments.
- `robustness-disentanglement`: actual proofs cover a finite local ratio with positive denominator, the same-sign equality, and the all-zero denominator witness. They do not supply a missing source `0/0` convention or make the outer D average total. The whole original definition remains scope-reviewed and the machine evidence is partial.
- `robustness-dropout-expansion`: the actual fixed-size `Fin 4` counterexample includes the original floor, exact retained-set average, zero pair differences and a realizable linear masked-input game. It refutes the original rounded-rate clause. A general corrected `k/n` expansion is explained by finite counting but has not been formalized and is not claimed to prove source Equations (14)–(15).
- `robustness-entropy-interaction` and `robustness-exclusive-shared-benefits`: machine proofs cover the exact four-conditional-entropy and conditional-information algebra for a real-valued entropy table. They do not construct a Shannon joint distribution from an arbitrary family of masked network outputs. The reader states the common-joint-law compatibility condition explicitly, defines the population entropy game `H_Y(S)=H(Y|X_S)`, and distinguishes it from the fixed-input game `g_x(S)=v(x_S)`. No claim of automatically verified probabilistic source semantics is made.
- `robustness-interaction-nullity`: the actual theorem applies to distinct players, as in the original pair-interaction definition. The displayed `∀j∈N` self-pair reading is preserved and separately marked ambiguous; no theorem proves it for `j=i`.

## Source errors retained and proof-only repairs

The original `+H` entropy game and source Equation (7) co-information convention are preserved. The author proof's negated entropy substitution, opposite intermediate information sign and `H(H|X_S)` typo remain visible; the repaired proof uses the same original conclusion. The B.1 symmetry proof's wrong context exclusions and Equation (7)'s exclusive-variable cancellation typo are preserved and repaired without altering the claims. The original dummy premise is not used to globally set the output baseline to zero: it forces that conclusion only for that special source premise. Every ordinary masked game retains `b=v(x_∅)`.

The floor error, D zero-domain problem and self-pair quantifier ambiguity have independent issue entries with exact locations and source scope. A false original equation is not renamed a successfully proved correction.

## Reproduction

Run from the project root, with `login:false` and project-local environment:

```sh
source scripts/env.sh
python3 -W ignore corpus/public/reader/neurips2021-robustness/build_content.py
python3 corpus/public/reader/neurips2021-robustness/verify_foundations.py
python3 corpus/public/reader/neurips2021-robustness/bind_verification.py
python3 corpus/public/reader/neurips2021-robustness/preflight_robustness.py
node corpus/public/reader/neurips2021-robustness/check_math.js
```

The latest package passes strict input/completion/bilingual checks (zero missing translations and zero inline-formula differences). Actual local KaTeX parses 2,665 formulas successfully. These software checks support delivery and rendering; independent mathematical and source-fidelity acceptance remains with root.
