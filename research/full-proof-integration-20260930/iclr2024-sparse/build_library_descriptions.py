"""Descriptions only: declaration signatures and hashes come from the successful audit."""
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent
ROOT = BASE.parents[2]
REPORT = BASE / 'verification/report.json'
report = json.loads(REPORT.read_text())
assert report['status'] == 'passed'

# A use is an existing, checked proof, not a newly invented toy example.
records = {
 'choose_coefficients_zero': ('二项式基底系数消去', '对连续 M+1 个取值为零的二项式组合逐次作有限差分，推出全部系数为零。', 'M≤n；从零阶到 M 阶的全部 M+1 个系数和测试行。', 'binomial_matrix_kernel'),
 'binomial_matrix_kernel': ('Lemma 3 的二项式矩阵核', '原 (M+1)×M 比值矩阵只有零核，以有限差分避开原行列式漏号。', '0<M<n；所有 j=0,…,M 的行等式；k=1,…,M。', 'sparse_coefficient_existence'),
 'binomial_coefficients_zero_of_le': ('包含 M=n 的系数消去', '把 Lemma 3 的零核结论扩展到 M=n，供 T2 零均值分支使用。', 'M≤n；全部 M+1 行，不需要 M<n 或 μ1≠0。', 'sparse_coefficient_existence'),
 'orderTotal': ('按阶交互有符号总和', '在 N 的全部 k 元子集上求交互系数之和 A(k)。', '有限全集 N；任意实集合函数 d；不是绝对值之和。', 'mean_reconstruction'),
 'meanOutput': ('固定掩码阶的平均输出', '在所有 m 元掩码上取平均，分母为二项式系数。', '有限 N；数学平均的有效域 m≤|N|；定义本身使用 Lean 实数除法。', 'mean_centered_cutoff'),
 'card_supermasks': ('超集掩码计数', '一个 k 元子集被恰好 choose(n-k,m-k) 个 m 元掩码包含。', 'T⊆N 且 |T|≤m≤|N|。', 'subset_layer_sum'),
 'subset_layer_sum': ('按固定交互聚合掩码和', '交换 m 元掩码与其子集的求和次序，再按子集阶数聚合。', 'm≤|N|；有限集合上的完整双重求和。', 'layer_sum_reconstruct'),
 'layer_sum_reconstruct': ('重构输出的层总和', '把一层所有重构输出写为各阶交互总和乘超集计数。', 'm≤|N|；任意系数函数 d，零阶项保留。', 'mean_reconstruction'),
 'choose_ratio': ('二项式系数比值恒等式', '超集计数除以掩码层大小等于 choose(m,k)/choose(n,k)。', 'k≤m≤n，确保用于数学比值的分母非零。', 'mean_reconstruction'),
 'mean_reconstruction': ('逐层平均重构公式', '平均输出等于各阶交互总和乘二项式比例；原始零阶项保留。', 'm≤|N|；g=reconstruct d 是输入形式，不假设待证结论。', 'mean_centered_cutoff'),
 'mean_centered_cutoff': ('Lemma 2 完整均值公式', '对中心化游戏，在高阶交互为零时保留 1 到 M 阶，得到原均值公式。', 'M≤m≤|N|；所有 S⊆N、|S|>M 的中心化交互为零；原输出基线任意。', 'FullSparse.lemma2'),
 'mean_centered_cutoff_all': ('包括低掩码阶的截断均值', 'm<M 时以 choose(m,k)=0 自动移除越阶项，得到所有 m≤n 的同一公式。', 'm≤|N|；原高阶交互零前提，不另加 m≥M。', 'sparse_coefficient_existence'),
 'mean_centered_zero': ('中心化空掩码均值', '中心化后空层均值为零。', '任意有限 N；centered g 在空集取零。', 'sparse_coefficient_existence'),
 'meanOutput_top': ('完整掩码层均值', '全集层只有 N 这一掩码，其均值就是 g(N)。', '任意集合函数 g；不要求输出基线为零。', 'sparse_coefficient_existence'),
 'totalStrength': ('按阶交互绝对强度', '在所有 k 元子集上累加 |d(S)|。', '与有符号 orderTotal 分开；空层和按有限和约定。', 'threshold_count'),
 'salientFamily': ('阈值显著交互族', '保留满足 τ≤|d(S)| 的 k 元子集。', '此定义使用包含等号的阈值；原 τ>0 在后续计数界使用。', 'threshold_count'),
 'cancellationRatio': ('同阶抵消比', '定义 η=A(k)/Σ|d(S)|，保持原有符号约定。', 'Lean 零分母除法定义为零；含 1/|η| 的数学界限另要求 η≠0。', 'salient_count_bound'),
 'threshold_count': ('阈值计数基本不等式', '每个显著系数贡献至少 τ，故 τ·显著数量≤总绝对强度。', '任意实 τ 都满足此乘法式；除以 τ 的后续结论要求 τ>0。', 'salient_count_bound'),
 'salient_count_bound': ('非抵消情形显著交互界', '把阈值计数转换为 |A(k)|/(τ|η|)，包括真实 η 定义。', 'τ>0、η≠0；不是 η=0 完全抵消情形，也还未代入 T2 系数。', 'salient_bound_original_coefficients'),
 'coefficient_normalization': ('系数归一化存在构造', '采用 C=1+Σ|A(k)/μ| 构造有界领先系数与增长偏移；μ=0 单独选一个系数为 1。', 'b>1、p>0、有限非空 K、μ≥0、μ≤ΣA≤b^pμ；μ=0 时所有 A(k)=0。最后一条由论文适配另行证明。', 'sparse_coefficient_existence'),
 'sparse_coefficient_existence': ('从原三条件得到领先系数', '在原截断、均值单调与输出鲁棒性下证明系数存在；由均值方程推出零均值分支所有 A(k)=0。', '|N|>1、1≤M≤|N|、p>0；不增加 μ1≠0、G 非空或 M<n。', 'sparse_original_coefficient_witness'),
 'leadingAggregate': ('领先系数加权总和', '定义原 λ^(m0) 的二项式比值加权和。', '保持原 m0 和各阶 c；在 m0=|N|、M≤|N| 时权重全部为 1。', 'sparse_original_coefficient_witness'),
 'digitAggregate': ('低位系数加权总和', '定义原 a_i^(m0) 的二项式比值加权和。', 'a 的两下标为交互阶 k 与低位 i，二者不能互换。', 'sparse_original_coefficient_witness'),
 'CoefficientWitness': ('Theorem 2 完整存在见证', '同时记录 m0、领先系数、偏移和低位系数，以及原表示式、位界、非零 λ 和两个符号分支的界。', '任意有限低位索引族 J；没有把表示等式当作存在性定理的输入假设。', 'sparse_original_coefficient_witness'),
 'sparse_original_coefficient_witness': ('Theorem 2 原系数式完整存在性', '取 m0=n、低位全部为零，构造满足原全部系数约束和两条符号蕴含的见证。', 'n>1、1≤M≤n、p>0 及原三条件；M=n 与 μ1=0 包含；M=0 的另一读法问题单列。', 'FullSparse.theorem2'),
 'salient_bound_original_coefficients': ('代入同一 T2 见证的计数界', '把同一见证的原完整系数表示式实际代入显著交互计数，得到原 T3 展开。', 'k∈[1,M]、τ>0、η≠0、μ1≥0；w 为真实 CoefficientWitness。', 'FullSparse.theorem3'),
 'sparse_original_T2_T3': ('由原条件推出完整 T2 与 T3', '从原三条件构造见证，并同时证明各阶阈值计数的原系数展开界。', 'n>1、1≤M≤n、p>0；T3 只在 τ>0、η≠0 的原非抵消范围。', 'FullSparse.theorem3'),
 'signed_gaussian_variance': ('独立高斯交错和的方差', '真实随机变量：常量加带 ±1 系数的有限独立高斯和，方差为项数乘 σ²。', '概率测度；每项可测且分布为 N(0,σ²)；对所用项两两独立；c_i²=1。L² 从高斯分布推出。', 'and_gaussian_variance'),
 'and_gaussian_variance': ('AND 交错扰动方差', '在全部 L⊆T 的高斯扰动上求交错和，方差为 2^|T|σ²。', '原 I 为固定常量；子集标签上的噪声可测、同高斯分布且两两独立。', 'noisy_masked_and_variance'),
 'or_gaussian_variance': ('OR 补集索引扰动方差', '补集映射在 T 的子集上单射，从原噪声族传递独立性，得到相同方差。', 'T⊆N；所有 N 子集标签噪声满足分布与独立前提；这是非空 OR 定义的交错和组件。', 'noisy_masked_or_variance'),
 'noisyMaskedGame': ('固定输出族加独立扰动', '把已固定的游戏输出 g(L) 改为 g(L)+ε_L(ω)，保持原模型输出与随机扰动分开。', 'γ 自适应优化产生的噪声不是本定义自动涵盖的原 IID 输出扰动模型。', 'noisy_and_identity'),
 'noisy_and_identity': ('扰动后 AND 交互恒等式', '从实际扰动输出的 Möbius 变换推出 I′=I+交错噪声和，没有假设待证身份。', '任意 T，包括空集；空集为原始输出基线加 ε∅。', 'noisy_masked_and_variance'),
 'noisy_or_identity': ('扰动后非空 OR 交互恒等式', '从 OR 的真实补集定义得到原系数加带负号的补集噪声和。', 'T 非空；空 OR 系数按原定义为 g(∅)，须使用单独分支。', 'noisy_masked_or_variance'),
 'noisy_masked_and_variance': ('实际扰动 AND 系数方差', '对实际 noisyMaskedGame 的 AND 系数证明方差，含原始空集输出基线分支。', '所用子集上的可测性、零均值高斯同分布和两两独立；固定原游戏 g。', 'FullGeneralizableAnalysis.masked_model_and_variance'),
 'noisy_masked_or_variance': ('实际扰动 OR 系数方差', '对同一扰动输出族证明 OR 系数方差；空集直接使用 ε∅，非空使用补集单射。', 'T⊆N；所有 N 子集上的原 IID 高斯模型；固定原游戏 g；σ²允许为零。', 'FullGeneralizableAnalysis.masked_model_or_variance'),
}

by_name = {d['name']: d for d in report['declarations']}
result = []
for d in report['declarations']:
    if not d['source_path'].startswith('lean/HarsanyiLib/Harsanyi/Extensions/'):
        continue
    short = d['name'].split('.')[-1]
    title, purpose, premises, use = records[short]
    use_name = use if '.' in use else ('Harsanyi.' if short in {
      'signed_gaussian_variance', 'and_gaussian_variance', 'or_gaussian_variance',
      'noisyMaskedGame', 'noisy_and_identity', 'noisy_or_identity',
      'noisy_masked_and_variance', 'noisy_masked_or_variance'} else 'Harsanyi.Sparsity.') + use
    used = by_name[use_name]
    full = short in {'binomial_matrix_kernel', 'mean_centered_cutoff',
      'sparse_original_coefficient_witness', 'sparse_original_T2_T3',
      'noisy_masked_and_variance', 'noisy_masked_or_variance'}
    result.append({
      'name': d['name'], 'name_zh': title, 'description_md': purpose,
      'key_premises_md': premises, 'source_path': d['source_path'], 'line': d['line'],
      'signature': d['signature'], 'evidence_role': 'theorem_proof' if full else 'partial_component',
      'example_refs': [{'declaration': use_name, 'source_path': used['source_path'],
        'line': used['line'], 'kind': 'existing_compiled_use'}],
      'report_path': str(REPORT.relative_to(ROOT)), 'build_id': report['build_id'],
      'source_fingerprint': report['source_fingerprint'], 'axioms': d['axioms'],
    })
out = {'schema_version': 1, 'purpose': 'catalog_descriptions_fragment',
  'report_status': 'passed', 'declarations': result,
  'scope': '35 audited public declarations only; constructor/projection signatures are separately extracted by the integrator'}
(BASE/'library-descriptions.json').write_text(json.dumps(out, ensure_ascii=False, indent=2)+'\n')
api = {'schema_version': 1, 'description_scope': out['scope'], 'declarations': {
  d['name']: {
    'declaration': d['name'], 'description_zh': d['name_zh']+'：'+d['description_md'],
    'key_preconditions_md': d['key_premises_md'], 'shared_proof_ids': [],
    'examples': [{'path': e['source_path'], 'line': e['line'], 'declaration': e['declaration'],
                  'kind': e['kind']} for e in d['example_refs']],
    'source_path': d['source_path'], 'line': d['line'],
    'import': 'Harsanyi.Extensions.'+('Sparsity' if '.Sparsity.' in d['name'] else 'Noise'),
    'evidence_role': d['evidence_role'], 'verification_report_path': d['report_path'],
  } for d in result}}
(BASE/'api-descriptions.json').write_text(json.dumps(api,ensure_ascii=False,indent=2)+'\n')
print(len(result), 'public declaration descriptions')
