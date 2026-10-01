# 公共 API 阅读入口

当前公共包为 **HarsanyiLib 0.2.0**。精确 Lean 类型、源码行号、依赖、公理及当前报告见 [catalog/library.json](../catalog/library.json)。目录由编译环境生成，中文用途说明不替代实际类型。

本轮统一报告为 [20260930T133803-2](../reports/lean/20260930T133803-2/report.json)。公共目录包含 154 条 API：39 个定义、101 个定理、1 个结构类型、1 个构造器和 12 个投影。不能把 API 总数当作论文证明数量；源码变化后先重新验证。

| 模块 | 主要入口 | 用途与条件 |
| --- | --- | --- |
| `Harsanyi.Core.Basic` | `Game`, `interaction`, `reconstruct`, `centered`, `marginal` | 实值集合函数、原始交互、重构与去基线 |
| `Harsanyi.Core.Mobius` | `reconstruction`, `interaction_reconstruct`, `reconstruction_unique` | 两个方向的有限 Möbius 反演及系数唯一性 |
| `Harsanyi.Core.Properties` | `interaction_add`, `interaction_centered_nonempty`, `interaction_relabel`, `interaction_unanimity` | 线性、非空中心化转换、置换、纯 AND 函数 |
| `Harsanyi.Core.Shapley` | `dividendAllocation`, `dividendAllocation_efficiency` | 交互均分及总和 |
| `Harsanyi.Extensions.Attribution` | `higherMarginal_eq_sum_interaction`, `factorialShapley_eq_dividends`, `factorialShapleyInteraction_eq_dividends`, `shapleyTaylor_eq_dividends`, `factorialShapley_eq_dividendAllocation` | 经典阶乘定义与交互公式的真实等价；STI 保留正阶条件及三个分支 |
| `Harsanyi.Extensions.OrInteraction` | `or_reconstruction`, `or_dual`, `maskCoordinates`, `conditionalCoordinateGame` | OR 空集基线、补集关系及实际坐标掩码 |
| `Harsanyi.Extensions.Sparsity` | `Sparsity.mean_centered_cutoff_all`, `Sparsity.CoefficientWitness`, `Sparsity.sparse_original_T2_T3` | 各阶均值、有限系数存在性及显著交互计数界；完整前提见实际类型 |
| `Harsanyi.Extensions.Noise` | `signed_gaussian_variance`, `noisy_masked_and_variance`, `noisy_masked_or_variance` | 明确概率测度、独立性及高斯分布下，固定掩码输出的真实方差 |
| `Harsanyi.Extensions.DerivativeCutoff` | `ClassicalMixedDerivativeCutoff`, `interaction_zero_of_classicalMixedDerivativeCutoff` | 经典混合偏导存在且高阶为零，经均值定理推出交互截断；不以 Taylor 收敛替代原条件 |

表中入口以 `Harsanyi` 为命名空间前缀。`import Harsanyi` 导入全部模块；仅需要部分结果时可导入相应模块。模型输出写作 `v(x_S)`，传入 `Game` 的对象为明确的 `g(S)=v(x_S)`；原始、中心化和分量交互不得混用。

论文适配保存在各论文研究目录，公共库不反向导入论文或网页。原始 Core 中文说明仍在 `corpus/theorems/`；本轮完整公共正文、论文适配与逐步对应在 [全篇数据](../research/full-proof-integration-20260930/data/full-content.json) 和阅读器中。共享正文只存一份，各论文保存自己的量词与定义对齐。

```bash
source scripts/env.sh
python research/full-proof-integration-20260930/architecture/paper_agent.py library Harsanyi.Sparsity.CoefficientWitness
python research/full-proof-integration-20260930/architecture/paper_agent.py shared
```

独立调用示例见 [Consumer.lean](../examples/library-consumer/Consumer.lean)，库接入流程见 [快速开始](library-quickstart.md) 与 [AI 调用说明](ai-use-library.md)。本库没有把训练、未量化近似或原命题的反例当作已证明结论；每个结果的范围和证据角色由论文数据分别记录。接口处于 0.2.0 阶段，升级时核对版本、真实类型与新报告。
