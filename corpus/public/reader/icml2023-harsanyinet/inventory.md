# HarsanyiNet: Computing Accurate Shapley Values in a Single Forward Propagation：正式全文逐页清单

来源SHA256：`ca752800222bcd9326fbee43747b3adfc996e23ff7996de40c72457e661c02ca`；审查22/22物理PDF页。

|PDF页|章节|分类|数学条目|
|---|---|---|---|
|1|Abstract; 1|background|无新数学目标|
|2|1; 2; 2.1|background_and_definitions|hnet-shapley-definition|
|3|2.2; 3; 3.1; 3.2|definitions_and_derived_reconstruction|hnet-centered-definition, hnet-reconstruction|
|4|3.2|numbered_mathematical_statements|hnet-r1-r2, hnet-shapley-dividend, hnet-unit-interaction, hnet-readout-linearity, hnet-forward-shapley|
|5|3.3|architecture_and_complexity|hnet-runtime, hnet-architecture, hnet-architecture-r1-r2, hnet-smooth-gate|
|6|3.4; 4.1|sparsity_scope_and_cnn|hnet-sparsity-count, hnet-cnn-receptive, hnet-experiments, hnet-external-sparsity|
|7|4.1; 4.2|experiments_and_cnn_definition|hnet-cnn-receptive, hnet-cnn-regroup, hnet-experiments|
|8|4.2|experiments|hnet-experiments|
|9|4.2; 5; References|conclusion_and_references|hnet-experiments|
|10|References|references|无新数学目标|
|11|References|references|无新数学目标|
|12|A; B Theorem 2/3|axioms_and_proofs|hnet-readout-linearity, hnet-forward-shapley, hnet-axiom-linearity, hnet-axiom-dummy, hnet-axiom-symmetry, hnet-axiom-efficiency|
|13|B Theorem 3/4|proofs|hnet-forward-shapley, hnet-architecture-r1-r2|
|14|B Theorem 4; C|proofs|hnet-unit-interaction, hnet-architecture-r1-r2|
|15|C; D; E|proofs_and_architecture|hnet-unit-interaction, hnet-architecture|
|16|E Setting 2; F.1|proof_and_experiments|hnet-cnn-receptive, hnet-cnn-regroup, hnet-experiments|
|17|F.1–F.4|experiments|hnet-experiments|
|18|F.4–F.7|experiments|hnet-experiments|
|19|F.7–F.8|conditional_game_derivation|hnet-conditional-attribution, hnet-experiments|
|20|F.5 Figure 8|figures|hnet-experiments|
|21|F.5 Figures 9–10|figures|hnet-experiments|
|22|F.5 Figure 11|figures|hnet-experiments|

## 去重条目

- `hnet-shapley-definition`：Definition 1; Eq.(1)，definition，陈述页[2]，证明页[]。
- `hnet-centered-definition`：Definition 2，definition，陈述页[3]，证明页[]。
- `hnet-reconstruction`：Definition 2 aftermath，derivation，陈述页[3]，证明页[]。
- `hnet-r1-r2`：Requirements R1/R2，definition，陈述页[4]，证明页[]。
- `hnet-shapley-dividend`：Theorem 1; Eq.(3)，external_theorem，陈述页[4]，证明页[]。
- `hnet-unit-interaction`：Lemma 1，lemma，陈述页[4]，证明页[14, 15]。
- `hnet-readout-linearity`：Theorem 2，theorem，陈述页[4]，证明页[12]。
- `hnet-forward-shapley`：Theorem 3; Eq.(4)，theorem，陈述页[4]，证明页[12, 13]。
- `hnet-runtime`：Cost of computing; O(nM)，derivation，陈述页[5]，证明页[]。
- `hnet-architecture`：Eq.(5)–(8)，definition，陈述页[5, 15]，证明页[]。
- `hnet-architecture-r1-r2`：Theorem 4，theorem，陈述页[5]，证明页[13, 14]。
- `hnet-smooth-gate`：Unnumbered tanh approximation，definition，陈述页[5]，证明页[]。
- `hnet-sparsity-count`：At most M; Eq.(9)，derivation，陈述页[6]，证明页[]。
- `hnet-cnn-receptive`：Setting 2，derivation，陈述页[6, 7]，证明页[16]。
- `hnet-cnn-regroup`：Setting 2 proof second half，derivation，陈述页[7]，证明页[16]。
- `hnet-axiom-linearity`：A(1)，external_axiom，陈述页[12]，证明页[]。
- `hnet-axiom-dummy`：A(2)，external_axiom，陈述页[12]，证明页[]。
- `hnet-axiom-symmetry`：A(3)，external_axiom，陈述页[12]，证明页[]。
- `hnet-axiom-efficiency`：A(4)，external_axiom，陈述页[12]，证明页[]。
- `hnet-conditional-attribution`：F.8 unnumbered formula，derivation，陈述页[19]，证明页[]。
- `hnet-experiments`：Tables 1–6; Figures 2–11，empirical_observation，陈述页[6, 7, 8, 9, 16, 17, 18, 19, 20, 21, 22]，证明页[]。
- `hnet-external-sparsity`：Ren et al. (2023b)，external_claim，陈述页[6]，证明页[]。
