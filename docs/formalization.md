# 形式化与验证

公共包是 `lean/HarsanyiLib`，命名空间 `Harsanyi`。下游 `lean/PaperProofs` 保存通用的中心化约定适配；当前三篇正式论文的完整适配与独立报告保存在 `research/full-proof-integration-20260930/` 各论文目录。私稿证据另保存在其 claim 目录，不能混入公开材料。`examples/library-consumer` 是第二个独立 Lake 包，证明新的仿射非空交互结论和去基线重构唯一性推论。依赖方向为 mathlib → HarsanyiLib → 下游；公共库不能反向导入论文包或 archive。

有限集合的核心证明利用 mathlib `Finset.sum_powerset_insert`，把全部子集分成含新增元素与不含新增元素的两组。项目检查过 mathlib 的一般 incidence-algebra Möbius 反演接口；当前实现选择直接有限集合归纳，从而避免引入尚未连接到显式 (−1) 幂系数的抽象 Möbius 函数。双向反演与唯一性适用于任意有限集合，未借助固定维数例子。

`scripts/verify-lean.sh` 调用只依赖标准库的 Python 编排器。其每次执行依次：

1. 记录工具链实测版本。
2. 完整 `lake build` 公共库、PaperProofs 和 consumer。
3. 在各自已构建的环境中读取声明 `ConstantInfo.type`，用 Lean 的 pretty printer 输出包含隐式参数和 universe 的真实类型。
4. 对每个源码明确导出的公共定义/定理执行 `#print axioms`，同时用内核环境的 `Lean.collectAxioms` 生成机器可读的传递公理列表。
5. 检查声明列表完整、axioms 字段存在且为字符串列表，并拒绝白名单以外的任何依赖。白名单仅有 `propext`、`Classical.choice`、`Quot.sound`；`sorryAx` 不在其中。
6. 运行 consumer 可执行示例，保存逐命令退出码与日志，生成报告和绑定报告的 API 目录。

公开 API 包括源码中有名称的顶层 `def`、`abbrev`、`theorem`、`lemma`，以及已登记 `structure` 的类型、构造器和投影；编译器内部生成的方程与匹配辅助常量不是额外稳定 API，其传递依赖会包含在审计中。声明自身的类型常量和证明表达式常量形成实际直接依赖；目录中的依赖不会由中文文字猜测。

`reports/lean/<build_id>/report.json` 保存 `source_files`，每项有项目内相对路径与 SHA-256。指纹算法为对按 path 排序的列表执行

```python
sha256(json.dumps(records, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode())
```

指纹覆盖三包 Lean 源码、Lake 配置、toolchain、manifest、Lean 版本锁与验证脚本。运行开始与结束的快照必须一致，否则该次报告失败。目录与后端都把报告绑定到这一指纹；源码更改后不可沿用历史 `verified` 字样。命令记录采用 `argv`、`cwd`、`exit_code`、`log_path`。

原始 Core 数学结果的中文证明位于 `corpus/theorems/<theorem_id>/proofs/<proof_id>/proof.zh.md`；本轮扩展的完整公共正文及适配汇集于 `research/full-proof-integration-20260930/data/full-content.json`。步骤锚点与 `steps[].lean_declarations` 关联真实声明；数学依赖映射到统一 theorem_id，底层 Lean 名保存在 `lean_dependencies`。网页的提取状态、人工对齐状态和 Lean 验证状态必须分别展示。

新增公共定理先检索目录，优先在下游组合已有引理。新通用引理需要声明、中文说明、明确前提、实际构建、公理审计和下游回归。修改公开假设或结论需要版本/迁移说明。0.2.0 已包含经典阶乘 Shapley/SII/STI 连接、OR 掩码理论、明确概率条件下的方差，以及经典高阶混合偏导截断的均值定理证明。各扩展的真实条件须查 catalog。整篇原命题的范围、反例和未量化主张仍需逐条看论文适配，不能由公共库编译状态推断。

发现原文数学错误时，记录来源、原陈述、具体错误、反例/推导和影响。当前三篇已获 `proof_only_granted`：保留原命题与全部假设，直接修复证明；原命题有反例则单列，不增补条件使其通过。其他材料依其已有授权处理，规则见[审校说明](review.md)。Lean 工程错误可正常修复，但不能把缺少数学前提当作类型错误默默补上。
