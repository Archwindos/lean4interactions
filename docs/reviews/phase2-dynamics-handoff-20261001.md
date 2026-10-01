# 第二轮数学接续手册

第一轮 F07/F08/F10 与转交的 F04 补项均已根验收；F06 最终交叉审查见 `docs/reviews/f06-cross-review-20261001.{md,json}`，绑定 content `edf8fa8f…`、report `83716554…`、Paper `406ea769…`。本手册不启动第二轮写入。本轮先完成验收记录与第二轮计划，再按用户要求讨论 GitHub 配置，不推送；根明确开始第二轮后，由新的 `gpt-6.1-sol / high` 代理接续。

旧三篇只读逐条候选位于 `docs/reviews/phase2-dynamics-readonly-20261001.json`：HarsanyiNet 22 条、Layerwise 17 条、Coalition 29 条，共 68 条、129 个中英对应步骤。每条含稳定 result/step IDs、具体 finding、当前 shared IDs/实际 Lean 声明及输入哈希。它是预审候选，不是修订完成或当前冻结输入证明；接续时先比较哈希。根任务依据是 `docs/twelve-paper-phase2-workorders-20261001.md` 与 `reader/evidence/twelve-paper-20261001/root-phase2-review-notes.json`。

优先处理以下六点：

- 规范对象固定为 $g(S)=v(x_S)$、$b=g(\varnothing)$、$g_0=g-b$。HarsanyiNet 的原 $V$ 已中心化，规范重写应绑定 $g_0$；原作者符号保留。重构式是 $\sum_{S\subseteq T}I_{g_0}(S)=g(T)-b$，公共 raw-game 重构要显式实例化到 $g_0$。
- Layerwise 当前正文已有实际原样本/重掩码适配，活动 content 无 `not_delivered`。遇旧状态先追查派生数据来源，不凭旧提示覆盖真实证据。跨样本期望中的局部游戏、输出基线、归一化系数与概念集合应显式带 $x$ 索引。
- Coalition 的数值二项式系数恒等式有效，但当前实际类型只证等价的 factorial predecessor kernel，不能先改角色为完整机器证明。轻量共享桥候选是 `DifficultyCounting.superset_context_count` 加按支持纤维分组；是否实施由根的新分工决定。
- Layerwise/Coalition 多处 `paper_mappings.original_definition` 填了规范变量。作者原定义与规范定义必须分开，逐原页修映射，不能把规范公式称为作者式。作者正文/原证明/PDF/历史来源证据保留。
- 公共证明复用须分清 raw $g$、centered $g_0$、任意 AND/OR 分解、固定样本与重掩码分解、最优解选择。普通 Shapley 值线性不是 dividend 本身的同一命题，$\gamma$ 依赖的分解归因也不能直接当普通 $\phi_g$。
- F07/F08/F10 的 Taylor/真实 Gaussian 矩/回归已共用实际公共证明。保留原绝对触发与真实最低阶 signed interaction 的区别；联合独立乘积矩与两两独立平方损失不是同一条件。F10 一般 context 双计数已在公共 `DifficultyCounting`，Cramer/半损失适配也已有独立公共模块。先查实际接口和报告，不再造相似库。

全局 manifest、英文覆盖层、符号聚合与共享种子由整合代理拥有；给它逐条补丁意图，避免并发写。没有数学变化时只补实际受影响的人读/映射检查；变更 Lean 时重跑相应声明、公理与来源哈希。我的第二轮实现尚未开始，未修改旧三篇内容、来源或 Lean。
