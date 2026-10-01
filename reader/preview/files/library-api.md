# 公共 API 阅读入口

当前公共包为 **HarsanyiLib 0.2.0**。精确 Lean 类型、源码行号、依赖、公理及当前报告见 [catalog/library.json](../catalog/library.json)。目录由编译环境生成，中文用途说明不替代实际类型。

基础当前统一报告为 [20261001T032325-2](../reports/lean/20261001T032325-2/report.json)，最新路径以 catalog 绑定值为准。基础公共目录包含 154 条 API：39 个定义、101 个定理、1 个结构类型、1 个构造器和 12 个投影。新增独立扩展通过活动论文实际报告及下方查询接口取得，不默认计入基础版本。不能把 API 总数当作论文证明数量；源码变化后先重新验证。

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

表中入口以 `Harsanyi` 为命名空间前缀。`import Harsanyi` 导入基础版本中的这些模块；独立新扩展须 direct import 其实际模块并查单独报告。仅需要部分结果时可导入相应模块。模型输出写作 `v(x_S)`，传入 `Game` 的对象为明确的 `g(S)=v(x_S)`；原始、中心化和分量交互不得混用。

十二篇已通过独立数学根准入，最终全量软件验收另行执行。新增公共扩展的精确可调用声明来自各篇实际报告；当前聚合后 `library` 查询返回真实 `import`、类型、源码、当前性与公理。以下包括 F04 实际模型补充、F10 以及 F06 的18个公共模块；独立扩展不计入基础154条的审计范围。

| 直接导入的公共模块（前缀 `Harsanyi.Extensions.`） | 输入与复用边界 |
| --- | --- |
| `HarsanyiNetwork`、`LayerwiseKnowledge`、`CoalitionAttribution` | 已验收六篇中的实际结构/定义转换；空感受野、架构子句与估计器约定按实际类型核对 |
| `RobustnessFinite` | 有限玩家与实际幂集上下文、二阶差分和有限平均；允许非零输出基线，空上下文族平均的库约定不替代论文的未定义商 |
| `PolynomialSupport`、`TaylorMoments` | 有限多项式支持、实际掩码与独立随机变量的积分矩；不建立任意 DNN 的无限 Taylor 展开 |
| `GaussianRegression`、`ConceptGaussian`、`NoisyRegression` | 明确概率测度、真实 Gaussian 法律与矩、独立或成对独立的有限特征、有限二阶矩及正方差下的期望回归；固定特征模型与真实网络训练需另作适配 |
| `TransformationEntropy`、`TransformationFinite`、`TransformationChains`、`TransformationCorrelation` | 有限输出的归一化非负联合律、条件熵/MI/总相关和粗细化；零质量分支按实际定义处理，不把连续输入默认为有限输入 |
| `TransformationGates`、`TransformationKernels`、`TransformationRefinement` | 任意可测输入概率空间、有限门/标签和可测条件核；确定性门与一般随机核分开，真实门标签联合律由积分生成 |
| `TransformationAffine` | 固定门下有限实矩阵的仿射组合；本论文 ReLU 门到这些矩阵的转换在独立论文适配中 |
| `TransformationEBM`、`TransformationRelaxation` | 有限状态归一化 EBM、明确经验律/先验、可微参数和连续正值域；不宣称采样误差、硬门近似收敛或 MCMC 收敛已证明 |
| `TransformationCounterexamples` | 实际有限分布、门与打印估计式的明确反例；每个反例只覆盖其准确类型 |
| `TransformationOperators`、`TransformationGaussianCounterexample` | 固定 dropout/max-pool 算子与有限门、实际独立 Gaussian 噪声生成律和联合分布；本论文网络与 Eq.(24) 的连接在独立论文适配中，不推广到随机训练或任意网络 |
| `DifficultyCounting` | 有限玩家的实际上下文、子集双射、按阶组合计数与两个原错误式的明确实例；非零分母和原始/中心化对象分别核对 |
| `DifficultyKappa` | 实际掩码单 ReLU、Gaussian 输入与归一化交互积分界及源等式的实际反例；正确积分下界不替代原文未成立的等号 |
| `DifficultyRegression` | 固定有限特征、真实 Gaussian 噪声和半期望损失下的回归最优系数与协方差解释；保留正方差、独立性和均值条件，不宣称一般网络训练已证明 |

F06 的下列路径为真实公共模块，统一命名空间是 `Harsanyi.Frequency`，部分结果位于 `MatrixBackprop`、`MultiChannel`、`Valid` 等子命名空间。导航依据实际源码、独立根类型读取及[最终296声明报告](../corpus/public/reader/icml2023-decoder/verification/report.json)；实际类型与当前源码检查仍是每次调用的依据。

| 直接导入模块（前缀 `Harsanyi.Extensions.`） | 对象、前提与论文适配边界 |
| --- | --- |
| `DecoderFrequency`、`DecoderGrid`、`DecoderFourier` | 有限群字符与实际未归一化 DFT；二维 `Grid M N = ZMod M × ZMod N` 要求非零网格尺寸。保留频率符号、正向空间位移、逆变换的尺寸因子、常数偏置的 DC 项；不能套到未声明边界的任意卷积 |
| `DecoderCascade` | 有限通道的线性仿射层实际复合及偏置累积；无非线性激活的圆周卷积模型。变动通道维数按真实矩阵类型处理，不用标量乘积替代多通道复合 |
| `DecoderBackprop`、`DecoderSpectralPullback`、`DecoderMatrixBackprop` | 实数空间连续线性层、损失的真实 Fréchet 导数、前缀/后缀拉回与 DFT 共轭转置；归一化频域梯度和未归一化 DFT 必须对应，不能漏共轭、通道收缩或尺寸因子 |
| `DecoderMoments`、`DecoderKernelMoments`、`DecoderLayerMoments` | 概率测度、可测实 Gaussian 核、有限二阶矩和真实核内/层间独立性下的复响应均值与模方二阶矩。`gaussianReal` 的第二参数是方差；复 Gaussian 不自动等于 circular Gaussian，弱一阶矩因子化不能代替独立性。公共 log helper 使用正核尺寸/正方差充分条件，更一般的每个因子为正定义域由论文适配另行核对 |
| `DecoderMultiChannel` | 随机矩阵级联的实际均值、二阶矩递推与闭式；保留核内、行间、层间及前缀列对象的独立性。带除法的闭式另要求实际通道数非零，不将仅一阶独立条件升级为二阶矩条件 |
| `DecoderUpsampling`、`DecoderPadding`、`DecoderValid` | 注入式 scatter/零插值的真实频谱，实际裁剪/valid 层与圆周模型的明确转换；valid 的不越界解释要求核尺寸合法，三角商要求正弦分母非零。Padding 中具体 2×2→3×3 反例不等于任意图像的通用随机频率独立定理 |
| `DecoderCounterexample`、`DecoderDepthCounterexample`、`DecoderParameterCounterexamples`、`DecoderWeakIndependence` | 满足所列实际模型条件的频谱约束、深度/核大小/均值比例与弱一阶条件反例；它们证明准确反例或辅助结论，不证明原文所有学习趋势，也不以相关性小推出独立 |

公共模块位于 `lean/HarsanyiLib/Harsanyi/Extensions/`。`corpus/public/reader/<paper_id>/lean/Paper*.lean` 是论文应用，读取公共库并核对本论文定义/条件；它们不会因为声明已编译而变为独立公共 API。新模块不修改旧基础 barrel，基础 0.2.0 与独立扩展报告分别关联。

论文适配保存在各篇活动目录及其实际报告指向的源码中，公共库不反向导入论文或网页。公共 Core 说明在 `corpus/public/theorems/`；当前公共正文、论文适配与逐步对应在 [全篇数据](../reader/data/full-content.json) 和阅读器中。共享正文只存一份，各论文保存自己的量词与定义对齐。历史研究目录及报告保持只读，不充当新篇已完成的证据。

```bash
source scripts/env.sh
python reader/architecture/paper_agent.py library Harsanyi.Sparsity.CoefficientWitness
python reader/architecture/paper_agent.py library Harsanyi.Entropy.entropy_chain
python reader/architecture/paper_agent.py library Harsanyi.ConceptGaussian.feature_expected_loss
python reader/architecture/paper_agent.py shared
```

基础调用示例见 [Consumer.lean](../examples/library-consumer/Consumer.lean)，独立扩展组合示例见 [ExtensionConsumer.lean](../examples/library-consumer/ExtensionConsumer.lean)及[实际消费报告](../reader/evidence/twelve-paper-20261001/direct-import-consumer-checks.json)。按[AI 调用说明](ai-use-library.md)先检索准确前提、直接导入公共模块、写本论文定义转换，再 `#check`/编译并登记来源与范围。本库没有把训练、未量化近似或原命题的反例当作已证明结论；每个结果的范围和证据角色由论文数据分别记录。基础接口处于 0.2.0 阶段，升级时核对版本、真实类型与新报告。
