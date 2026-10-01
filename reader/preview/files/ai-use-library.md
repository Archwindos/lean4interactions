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

已有库不够时，保存检索词、候选声明、前提差异与确切缺口。先在下游验证辅助结果；具有普遍复用价值时按当前任务授权加入公共库，不修改既有定理来迎合目标。若缺口揭示原文数学错误，登记来源、原陈述、证据及影响，并按[当前十二篇修正授权](twelve-paper-release-20261001.md)处理：已授权范围允许直接修证明，禁止改变原命题或添加假设；原命题有反例时单列。普通导入、命名和 Lean 构建问题可以自行修复。

交付时保存下游源码、所用公共引理清单、库/Lean/mathlib 版本、真实构建命令与退出状态、自己的 `#print axioms` 结果。基础三包验证命令为 `scripts/verify-lean.sh`，按入口的实际 import 闭包审计；它不覆盖未导入的新扩展。活动论文与独立扩展通过 `python reader/architecture/paper_agent.py library` 查询，各条提供实际类型、源码、报告与当前证据。新增模块用其实际 `Harsanyi.Extensions.<Module>` direct import 和独立真实报告，不为查询方便改动旧 barrel 或将新模块冒充基础 154 条 API。统一公共库版本更新留待第二阶段审查。

对于独立扩展，按“检索准确前提 → 导入公共模块 → 写论文定义转换 → `#check` 和编译 → 保存来源与范围”使用。下例查询真实的二阶差分基线不变性；接口返回 `import`、`source_path`、完整 `signature`、独立 `report_path` 与 `current_evidence`。只在编译、公理审计和源新鲜度均通过时将其作为当前证据。

```bash
source scripts/env.sh
python reader/architecture/paper_agent.py library Harsanyi.Robustness.pairDelta_baseline
cd examples/library-consumer
lake env lean ExtensionConsumer.lean
```

[ExtensionConsumer.lean](../examples/library-consumer/ExtensionConsumer.lean) 仅直接导入 `Harsanyi.Extensions.RobustnessFinite`，先 `#check` 三条公共引理，再定义论文面对的游戏 `g(S)=v(mask(S))`，组合常数平移不变性、比例律与有限平均的比例律，证明仿射变换只按比例改变二阶上下文交互。例子不要求 `g(∅)=0`，没有复制公共证明。它采用库中空上下文族平均为零的定义；不能据此替原论文分母为零的商式补值，也不说明训练过程或渐近稀疏性已形式化。

从项目根目录运行 `python reader/check_library_consumer.py`，可重新构建所用公共模块、在独立下游环境编译例子、由 Lean 导出其实际类型与传递公理，并绑定消费源码、实际 import 闭包、配置和真实日志。当前记录见[独立扩展消费检查](../reader/evidence/twelve-paper-20261001/direct-import-consumer-checks.json)。此脚本不更新基础目录，不改变任何论文结果状态；报告只覆盖这个新结论。Entropy/Gates、Gaussian、Fourier 等模块须以各自实际报告和入站后的查询结果为准，不能沿用这个例子的通过状态。

公共模块取自 `lean/HarsanyiLib/Harsanyi/Extensions/`，可通过其 `Harsanyi.Extensions.<Module>` 路径复用；论文专属 adapter 留在对应 `corpus/public/reader/<paper>/lean/` 或应用包。分类依据是源码位置和实际职责，不由 `Paper*` 名字推断。当前查询只包含已聚合活动快照所引用报告中的公共声明；未入站稿件的代码存在不代表接口已发布或论文已完成。

新增领域按以下对象选择入口，再查完整签名。准确模块清单与条件见[公共模块导航](library-api.md)，不能仅按“entropy”“Gaussian”“Fourier”关键词认定两个对象相同。

| 新证明的实际对象 | 可检索的公共模块 | 应先写出的适配和条件 |
| --- | --- | --- |
| 有限输出熵、MI、总相关 | `TransformationEntropy/Finite/Chains/Correlation` | 归一化非负联合律、有限输出索引与实际熵定义；连续输入可生成有限输出，不改成有限输入假设 |
| 确定门、随机条件门、固定网络算子 | `TransformationGates/Kernels/Refinement/Operators` | 本论文的门/标签联合律，随机核的可测性与归一化，或固定 dropout/max-pool 的真实门模型；不把一般随机训练当固定门 |
| 有限多项式交互或 Taylor 有限项 | `PolynomialSupport/TaylorMoments` | 有限总体、支持、幂次数与原始基线；有限支持不建立任意神经网络无限展开或截断误差界 |
| Gaussian 特征、噪声矩与回归 | `ConceptGaussian/GaussianRegression/NoisyRegression/DifficultyRegression` | 实际分布、均值/方差、可测性、独立或定理明确要求的成对独立、有限二阶矩及正方差；噪声标准差与方差不能互换 |
| 实际上下文组合计数或交互积分难度 | `RobustnessFinite/DifficultyCounting/DifficultyKappa` | 原始/中心化交互与空集、上下文阶/分母、真实掩码和归一化积分；正确子结果和原错误等式分开登记 |
| 有限网格卷积、频谱、矩阵梯度 | `DecoderGrid/Fourier/Cascade/MatrixBackprop` 等 `Decoder*` 模块 | `ZMod` 网格尺寸、DFT 归一化、正向位移、实空间损失导数、共轭转置与通道数；圆周/裁剪/valid/插值边界明确区分 |

例如 Entropy 目标先查询 `Harsanyi.Entropy.entropy_chain`，Gaussian 回归先查询 `Harsanyi.ConceptGaussian.feature_expected_loss`。Decoder 的实际二维变换对象在 `Harsanyi.Frequency.dft2`，矩阵级联闭式入口在 `Harsanyi.Frequency.MultiChannel.actual_cascade_source_closed`。F06 已正式准入，其实际报告包含296个声明和18个公共模块；检索对应完整类型与当前证据后，再在下游 `#check`。如果接口没有返回声明，停止把它登记为当前已验证依赖，核对聚合快照、活动报告与模块 import。

频域对象与集合游戏没有相同类型：`Grid M N → ℂ` 不是 `Game α`。若目标从图像模型构造交互，先定义其输入掩码和实值输出，再连接到有限玩家游戏；若目标是卷积/DFT，则保留复频域与实空间之间的实际转换。调用多通道二阶矩闭式时，逐项检查层、行与前缀列独立性及非零通道数；仅有原文的一阶乘积期望等式时不能套用更强的机器定理。

2026-09-30 已由未参与库实现的 `gpt-6.1-sol / max` 代理完成一次独立试用：仅依交付文档与目录开始，组合六条公共引理证明包含空集分支的去基线仿射公式及唯一性，并保留缺前提调用的实际失败记录。参见 [试用说明](reviews/api-playtest.md) 和 [独立报告](../reports/api-playtest/20260930-max-centered-affine/report.json)。后续新证明仍须保存自己的执行证据，不能直接沿用这次试用的通过状态。
