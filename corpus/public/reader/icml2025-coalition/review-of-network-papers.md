# HarsanyiNet 的独立数学交叉审查

审查者：`vnext_coalition_math`。本文件是另一数学代理的独立审查，不是作者输入的重写生成器，也不等同于根代理或用户验收。Layerwise 的内容由本代理实施，因此本文件不把自己对 Layerwise 的检查称为独立交叉审查。

实际阅读了 HarsanyiNet 正式 PDF 的数学来源页 3–7、12–16、19，以及这 15 个目标的完整项目中文/英文步骤、全部公共 `HarsanyiNetwork.lean` 源码和当时的 `PaperHarsanyiNet.lean`。逐项比较了定义、有限总体、空集、基线、模型与证明所用前提；并非只查看编译计数。其余背景、训练/实验图表页面的全文完整性不在此次独立审查结论中；它们由论文责任代理的逐页清单负责。来源文件哈希与最终报告类型另见配套 JSON，源码行号可能随后因补充适配而移动。

原文使用中心化 reward $V(S)=v(x_S)-v(x_\varnothing)$，$I(\varnothing)=0$。审查均按这个定义，未把原始输出假设为零；架构的零基线输出是由无偏置结构证明出的另一事实。

| 已实际审读目标 ID | 数学结论及范围核查 | 真实 Lean 对应与限制 |
| --- | --- | --- |
| `hnet-reconstruction` | 原递归定义等于中心化 Möbius 系数。有限双和或递归反演给每个 $T$ 的 $v(x_T)-v(x_\varnothing)$，空掩码也成立。没有把完整输入的一条等式当作全部掩码唯一性。 | `Harsanyi.reconstruction` 对任意游戏成立，实例化中心化游戏即可；`interaction_recursive` 对齐原递归定义。 |
| `hnet-shapley-dividend` | 由经典阶乘边际定义到交互均分。固定 $S\ni i$，环境权重和是 $1/|S|$；空集不在该求和中。中心化在每个边际中抵消。原 Theorem 1 外引 Harsanyi，不存在本篇独立作者 proof block，来源分类正确。 | `factorialShapley_eq_dividendAllocation` 是实际阶乘到均分桥，并非把均分式当定义。 |
| `hnet-unit-interaction` | 原 R1/R2 没有排除空感受野。合法常数单元 $R=\varnothing,z\equiv1$ 满足 R1/R2，而中心化 $J(\varnothing)=0\ne1$；因此原 Lemma 1 字面量词有反例。原代码架构中空场值为零，不能把该额外结构事实补进 R1/R2-only 原命题。 | `empty_unit_counterexample` 核验反例；`requirement_unit_interaction` 保留一般空场分支；`unit_interaction` 只证明实际无偏置架构实例。后两条没有冒充原 Lemma 的无条件完整证明。 |
| `hnet-readout-linearity` | Eq.(2) 在所有掩码与空掩码上成立，故 $g_0(T)=\sum_jw_j(u_j(T)-u_j(\varnothing))$。展开有限变换、交换有限和给全部 $S$ 的加权中心化单元交互。无需每个单元的基线为零。 | `interaction_weighted_sum` 与 `PaperHarsanyiNet.centered_readout` 均真正中心化两侧，覆盖非零原始输出基线。 |
| `hnet-forward-shapley` | $i\in R_j$ 的分支使 $R_j$ 非空，贡献 $w_jz_j(x)/|R_j|$；其余分支包括空场，中心化后贡献零。因此有效条件和成立，并不依赖错误 Lemma 的空场第一结论。原全单元显示分式先除 $|R_j|$ 再乘指示，空场为 $0/0$；须保留原定义域问题，不能用 Lean 实数除零约定判原式全域成立。 | `requirement_forward_shapley` 是全域 mask-law 编码的通用充分引理；`forward_shapley` 和实际坐标 adapter 由架构推出该律。原有限 R1/R2-only 适配的量词问题见后文跟进，分母状态已建议细分。 |
| `hnet-runtime` | 固定图可预处理场集合和基数，扫描 $nM$ 个变量/单元索引对给 $O(nM)$ 累加上界。该计数不能证明相对前向传播总时间“可忽略”；实现、数据结构与硬件比较没有被提升为渐近定理。 | 明确无 dedicated runtime Lean 验证，计数是完整人类算法说明，未把前向传播数学证明当性能证明。 |
| `hnet-architecture-r1-r2` | 原 hard gate 的叶/父归纳有效。父场是孩子场之并，缺变量只需沿一个依赖孩子产生零因子，不是所有第一层单元都零。全部保留则 R1 给值不变。空孩子集合的无偏置线性和是零。 | `value_congr` 推出 R1，`value_mask` 从硬门结构证明 R2，`value_baseline`/`value_empty_receptive` 独立证明架构空项；没有把 R2 当待证结论假设。`Expr` 展开有限 DAG 为有限树，复制共享子表达式不改变数学函数；不声称模型保留原 DAG 计算成本。 |
| `hnet-sparsity-count` | 非零中心化交互支撑包含于感受野有限像集，像集基数不超过单元数。重复场和相消只降低数量，不能改成恰好 $M$。原传统网络 Eq.(9) 忘了输出基线，常数 1 反例仅针对该首等式；近似小尾项不是由 $M$ 上界证明出的。 | `support_subset_fields`/`support_card_le_units` 证明具体有限支撑包含和基数。通用 premise 的全域 mask-law 编码与原有限域适配须分清。 |
| `hnet-cnn-receptive` | 同位置共享 $\tau$ 得相同阈值矩阵、相同孩子集合，场并集相同；不依赖通道线性权重。共享 gate 不意味着 ReLU 输出同步非零：同一非零孩子，线性值 $1,-1$ 给输出 $1,0$。 | `receptive_shared_children` 真正比较同孩子、不同权重的场。单纯同场等式不能作为向量 gate 数值等价的证据。 |
| `hnet-cnn-regroup` | 固定目标 $S$ 必须过滤 $R_j=S$，原末式无过滤相加错误。对同一实际网络的标量输出，有限通道和与向量读出的重组精确成立。更换 scalar all-nonzero gate 为 group at-least-one-nonzero gate 改变函数，孩子向量 $(1,0)$ 已给反例。新 group 网络仍可由子组掩码律归纳证明自身 R2。 | `channel_grouping` 只核验有限重组；`groupedBlock_mask` 真正给向量组 hard-gate 的归纳步；`scalar_grouped_gate_counterexample` 核验不同值。报告正确披露尚无整个递归 vector-CNN 数据类型；scalar `Expr` 不冒充它的完整实现。 |
| `hnet-axiom-linearity` | 对每个背景边际使用加法、齐次分配，提出固定标量，原假设与所有实数标量均保留。 | 完整人类证明；最终 `PaperHarsanyiNet.shapley_add`、`shapley_scale` 分别核验经典边际加法与任意实数缩放。原本篇仍没有独立作者 proof block。 |
| `hnet-axiom-dummy` | 原每个背景边际等于 $V(\{i\})$，阶乘权重按背景大小分为 $n$ 组、各为 $1/n$，总和 1。$n=1$ 同样成立。中心化 $V(\varnothing)=0$ 与原 dummy 定义一致。 | 完整人类证明，未新增非零输出或非空背景条件；最终 `PaperHarsanyiNet.shapley_dummy` 的前提恰为原中心化零空值、玩家属于总体、及全部原 dummy 背景等式。 |
| `hnet-axiom-symmetry` | 原前提推出换位不变：两变量均含/均不含的集合不动，只含一个者按原前提配对。换位把 $i$ 背景双射到 $j$ 背景，基数和边际保持，故归因相等。$i=j$ 自反。 | 完整人类双射证明，未把只总游戏对称偷换成任意 AND/OR 分量分别对称。无 dedicated axiom 形式化声明。 |
| `hnet-axiom-efficiency` | 交换有限均分和，每个非空 $S$ 被其 $|S|$ 个成员累计一次；空系数为零，重构得到 $V(N)$。空总体也成立。 | 完整人类证明与实际经典桥/重构相容；最终 `PaperHarsanyiNet.shapley_efficiency` 真正证明经典阶乘归因的总和，原中心化实例使其等于 $V(N)$。 |
| `hnet-conditional-attribution` | F.8 保持未选变量为原输入 $x$，条件游戏是 $g_Q(T)=g(T\cup(N\setminus Q))$，不是原基线上的限制游戏。$R_j\subseteq T\cup(N\setminus Q)\iff R_j\cap Q\subseteq T$；真正玩家为 $Q$，分母 $|R_j\cap Q|$ 只在含 $i$ 分支计算。空交集给常数单元、中心化后零。效率差是 $g(N)-g(N\setminus Q)$。 | `conditional_receptive` 证明集合等价，`conditional_forward_shapley` 和实际坐标 adapter 从经典边际定义得到交集场均分。generic 引理的全域 law premise 同样需要有限域 paper 适配或明确范围；没有把选中玩家归因冒充原全集玩家归因。 |

## 必须跟进的类型与状态边界

在最初审查的公共源码中，`Harsanyi.Network.requirement_forward_shapley`（约 line 129）、`support_subset_fields`（约 157）、`support_card_le_units`（约 172）及 `conditional_forward_shapley`（约 195）使用 `hu : ∀ j∈J, ∀ T : Finset α, ...`，没有 `T⊆N` 限制。原 R2 是有限总体内的掩码 law。对于 generic 任意 `N` 及任意游戏，这确为更强的充分前提；不能直接把它称为原有限 premise 的 paper 适配。

实际 `Expr` 的 `value_mask` 对所有有限坐标 mask 均由架构证明，所以实际模型 adapter 的这一使用没有新加数学假设。但当时 `PaperHarsanyiNet.lean` 仅有 generic `Expr` 模型 adapter，没有把原有限 R1/R2-only 命题专门实例化为 `Fin n/univ` 的 wrapper。已通知责任代理与根代理：若新增 `Fin n/univ` 适配，则每个 `T` 自动包含于总体，原有限 premise 可直接供给，并不加强原条件；或者报告必须准确披露 generic 充分引理的编码范围。最终补充核对会记录在本文件及 JSON，不以时间推移假设它已经完成。

此外，`hnet-forward-shapley` 初稿状态为 `complete`，但它的原显示全单元分式已登记空场零分母问题。建议改为 `complete_with_original_domain_issue`，保持有效条件和的证明及真实形式化，却不标原未定义表达式全域完整。此项与 `hnet-unit-interaction` 的空场反例分开。

没有在本审查中改写他代理的内容或 Lean。发现的问题已经直接发给责任代理和根代理。

## 最终适配复核

责任代理已经新增并真实编译以下 paper wrappers；本代理逐条阅读了源码、从 collector 提取的真实完整类型、公理依赖和最终报告，而非仅接受口头完成：

- `PaperHarsanyiNet.finite_requirements_attribution`，`lean/PaperHarsanyiNet.lean:38`：变量类型为 `Fin n`、总体为 `Finset.univ`，前提显式是原 `∀T⊆univ` 的 mask law。证明内部用 `subset_univ T` 供给 generic 全域引理；这是有限类型内部恒真事实，不是新增原假设。`c_j` 由在全掩码的同一 law 等于原完整单元输出。
- `PaperHarsanyiNet.finite_support_card`，同文件 line 48：同一原有限掩码域，中心化 readout 的具体非零支撑有限族基数不超过 `J.card`。没有把支撑结论当作假设。
- `PaperHarsanyiNet.finite_conditional_attribution`，同文件 line 58：`Q` 是 `Fin n` 内的集合，前提 `i∈Q` 与原选中玩家一致。真实经典游戏只把 `univ\Q` 固定为原输入，分母是 `R_j∩Q` 基数。所有有限域量词内部消解，没有新全域 mask-law 条件。

因此，初审发现的 generic premise 与 paper 有限域适配间缺口已由真实 wrappers 解决，不作为仍未完成的问题保留。generic 三类充分引理本身仍须按它们的实际全域类型阅读，paper 应用使用以上有限实例或实际架构 adapter。

`hnet-forward-shapley` 最终已改为 `complete_with_original_domain_issue`，Lean 为 `partial_scope_verified`，明确证明有效条件和而不验证原空场分母表达。Lemma 1 仍保留其独立空场反例。CNN grouped-block 步与全部递归 vector-CNN 实现的范围也仍分别披露。

最终 Hnet 报告 `verification/report.json` 为实际 `passed`，41/41 声明逐行 `status=passed`，全部命令 exit 0，源码哈希在复核时全部当前。公理只含 `propext`、`Classical.choice`、`Quot.sound`，没有额外公理；这仍不等于自动证明作者语义。

三条新增经典归因声明另已核对：加法/缩放保留所有原实数系数；dummy 显式保留原中心化零空值和全部背景；效率是实际经典阶乘和的总归因，不是用均分值作定义跳过桥。对称公理仍有完整人类双射证明，未声称不存在的 dedicated 形式化。

本次 15 个目标数学审查已完成。剩余形式化范围是责任代理公开披露的范围：完整 vector-CNN 递归类型、runtime 精确复杂度模型和原未定义表达；它们没有在本报告中被隐去或当作已完成。未独立审查的实验与背景细节如本文件开头所列。


## 最终增量核对：初审文字是历史快照

现有实际 `PaperHarsanyiNet` 已包含 `shapley_add`（line 68）、`shapley_scale`（73）、`shapley_efficiency`（82）、`shapley_dummy`（89）和 `shapley_symmetry`（109）。本次已逐条读取真实类型和源码，核对加法/任意实数缩放、经典阶乘归因效率、原中心化 dummy 背景、及原有限域对称前提。对称声明只要求原 $T\subseteq N\setminus\{i,j\}$ 上的等式，证明通过有限背景拆分保持阶乘权重，不要求任意分量各自对称。

最终报告为 42/42 声明真实 passed，逐行 status 与源码哈希均已复核当前；附带 JSON 已绑定这一报告和当前内容哈希。上文 41 声明报告、表内“无 dedicated axiom 声明”及相应初审文字只记录当时快照，已由本段最终增量核对取代。没有修改 Lean 源码，也不扩张原未定义表达和完整 vector-CNN 的核验范围。
