# AI 使用公共库

先检查 `catalog/library.json` 的 library_version、lean_version、mathlib_revision、source_fingerprint 与 verification_report。当前库工作区为 0.2.0，使用 Lean 4.24.0 和 mathlib 提交 `f897ebcf72cd16f89ab4577d0c826cd14afaafc7`；与 `lean/HarsanyiLib/lakefile.toml` 对照，不能将升级前的目录当作新版本证据。报告的 status 必须为 passed，且 source_files 的实际 SHA-256 仍匹配。无需启动 archive，即可使用公共数学库；宣称完成某篇论文命题时，还须读取该命题的正式原文、符号映射和适配条件。

查询目录时按中英文 title、summary、tags 搜索，再读取完整 signature 和推荐 import。例如查询 `uniqueness`、`唯一性`、`centering`、`中心化`。精确签名由实际 Lean 环境提取，不能按中文简称猜测参数次序。可直接使用标准库读取离线目录：

```bash
source scripts/env.sh
python - <<'PY'
import json
catalog = json.load(open('catalog/library.json'))
for item in catalog['declarations']:
    if 'uniqueness' in item['tags'] or 'centering' in item['tags']:
        print(item['name'], item['import'], item['signature'], sep='\n')
PY
```

对于目标“给游戏加常数 b 并乘比例 a，非空交互怎样变化”，应依次选择 `interaction_add`、`interaction_smul`、`interaction_const`。核对 S.Nonempty 后，用 `hS.ne_empty` 化简常数分支。完整可构建代码在 `examples/library-consumer/Consumer.lean` 的 `affine_nonempty`；最短命令见 library-quickstart。

对于目标“某系数函数重构 v(S)−v(∅)，它是否就是 v 的交互”，必须先识别定义差异。`reconstruction_unique` 的目标应实例化为 `centered v`，得到 d=interaction(centered v)；只有在 S 非空时，才能调用 `interaction_centered_nonempty` 得到 d(S)=interaction v(S)。这一过程在 `baseline_unique_nonempty` 中实际构建，未复制公共证明正文。

核对前提时逐项写出：变量类型/有限集合、是否包含空集、是否去基线、变量 i 是否已在 S 中、是否有非空约束、分母是否非零、纯交互的 A 是否包含于总体 N。`interaction_congr` 可处理只在目标子集族上一致的定义；它不需要函数在所有有限集合上全局相等。

常见失败：

- `Unknown identifier`：检查 `import Harsanyi.Core.Properties` 或 `import Harsanyi`，以及 `open Harsanyi`，不要用过期目录中的声明名。
- `Game α` 和 `Set α → ℝ` 类型不匹配：库使用 `Finset α`；先明确有限总体并转换域，不用类型强制替换掩盖域变化。
- `interaction_insert` 不能应用：它要求 i∉S；i 已在 S 时并不产生新的差分阶数。
- 去基线游戏与原游戏不能直接套唯一性：先使用 `centered`，保留空集差异。
- 所有集合上的仿射比例公式无法由 `affine_nonempty` 得到：缺少 S.Nonempty。例 v=0、a=1、b=1、S=∅ 时左边为 1，右边为 0。不能悄悄把错误目标登记为已证明。
- 对 `dividendAllocation` 的性质不能直接冒充经典 Shapley 公式。0.2.0 工作区已实现连接定理 `Harsanyi.factorialShapley_eq_dividendAllocation`；先在当前目录中确认它的真实签名和有效报告，再引用。

跨论文调用时，先从规范符号表选择准确的概念实例。原始游戏、中心化游戏、AND/OR 分量游戏和再次掩码后的条件游戏即使使用同一字母，也不能互换。常用桥包括 `maskCoordinates_comp`、`interaction_centered_nonempty`、`or_dual`；它们各有明确适用条件，不是无条件记号替换。

涉及原 Assumption 1-β 时，使用 `ClassicalMixedDerivativeCutoff` 表达所要求高阶混合偏导的真实存在与处处为零。该条件仅作用于总阶高于截断阶数的有序坐标列表；前缀可微性是经典迭代导数存在的展开。Lean 的 `deriv` 在不可微处也有默认值，单独的 `deriv = 0` 不足以编码原假设。实际截断证明经过有限差分和一元均值定理，不需要添加 Taylor 级数相等、解析性或多项式表示假设。

`Harsanyi.Sparsity.CoefficientWitness` 保存 Theorem 2 所需的全部存在性见证及约束。使用 `sparse_original_coefficient_witness` 得到见证后，通过其字段读取系数表示、范围及对数界；`sparse_original_T2_T3` 进一步给出同一个见证对应的计数界。不得自行假设 `representation` 再将其称为从论文三假设证明了存在性，也不得把有限维系数界直接解释成一致渐近稀疏性。字段类型和参数顺序应从实际 Lean 提取结果读取。

人写证明到 Lean 的衔接顺序是：保留原陈述；列出定义和全部前提；把证明分成可独立说明理由的步骤；为每步查找公共引理或证明新引理；写出论文对象到库对象的适配；最后编译并审计。步骤到声明的链接用于核对这一对应，不表示编译器已检查中文语义。精确陈述、近似解释、反例和条件适配必须各自注明范围。

已有库不够时，保存检索词、候选声明、前提差异与确切缺口。先在下游验证辅助结果；具有普遍复用价值时按当前任务授权加入公共库，不修改既有定理来迎合目标。若缺口揭示原文数学错误，登记来源、原陈述、证据及影响，并按[已有修正授权](review.md)处理：当前三篇允许直接修证明，禁止改变原命题或添加假设；原命题有反例时单列。普通导入、命名和 Lean 构建问题可以自行修复。

交付时保存下游源码、所用公共引理清单、库/Lean/mathlib 版本、真实构建命令与退出状态、自己的 `#print axioms` 结果。当前三包统一验证命令为 `scripts/verify-lean.sh`；它只覆盖清单中已有三个包，新包须另行构建与审计，不能宣称被旧报告覆盖。

2026-09-30 已由未参与库实现的 `gpt-6.1-sol / max` 代理完成一次独立试用：仅依交付文档与目录开始，组合六条公共引理证明包含空集分支的去基线仿射公式及唯一性，并保留缺前提调用的实际失败记录。参见 [试用说明](reviews/api-playtest.md) 和 [独立报告](../reports/api-playtest/20260930-max-centered-affine/report.json)。后续新证明仍须保存自己的执行证据，不能直接沿用这次试用的通过状态。
