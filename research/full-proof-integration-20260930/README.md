# 三篇正式论文的全篇证明阅读库

本目录整合 CVPR 2023 Sparse Concepts、ICLR 2024 Sparse Interaction Primitives 与 ICLR 2024 Generalizable Interaction Primitives。来源是四份正式 PDF：正文、附录与 CVPR 官方补充材料，共 94 页。原件及旧版阅读器保留，未发表私稿不进入本目录的公开快照。

从论文目录选择定理或推导，可阅读中文证明、原命题、作者原证明和 Lean 对照。正文使用 `v(x_S)`；原始、中心化及分量交互通过有作用域的符号记录区分。跨论文共享正文只存一份，论文自己的定义与适配保留在对应页。错误原式可追溯；错误命题、错误子句和定义域疑点分别展示。

## 打开阅读器

所有命令从项目根目录 `/mnt/data2/wyh/lean4project` 执行：

```bash
source scripts/env.sh
python -m http.server 8001 --bind 127.0.0.1 \
  --directory research/full-proof-integration-20260930/preview
```

打开 http://127.0.0.1:8001/ 。服务只暴露生成的 `preview/`，不能将项目根目录作为静态目录。三篇原有 `/papers/<paper_id>/` 地址保持。支持题名、原定理编号、别名及关键词查询；公共证明和规范符号各有独立入口。

## 数据、代码和证据

| 路径 | 用途 |
| --- | --- |
| `input-manifest.json` | 显式列出的公开正式论文；不自动扫描 inbox |
| `cvpr2023/`, `iclr2024-sparse/`, `iclr2024-generalizable/` | 每篇来源、逐页清单、原文、重写、符号、问题和论文适配 |
| 各篇 `inventory.json`, `content.json`, `symbols.json`, `issues.json` | 经审校的论文输入；保留稳定 ID 和原始出现位置 |
| `data/full-content.json` | 聚合结果，包含目录、共享关系、符号和各自状态 |
| `architecture/paper_agent.py` | 给 AI 的本地只读查询工具 |
| `architecture/*.schema.json` | 机器数据结构约束 |
| `ui/`, `build_preview.py`, `preview/` | 阅读界面、构建器、静态快照 |
| `evidence/` | 构建清单、来源页映射、浏览器与状态检查 |
| `root-audit/` | 根代理独立来源、数据、浏览器及最终验收证据 |
| `../../lean/HarsanyiLib/` | 可单独使用的公共数学库 |
| `../../catalog/library.json` | 从实际 Lean 环境生成的公共 API |

清单有 102 个来源条目，归并为 100 个阅读条目，其中 61 个是证明/推导覆盖目标。定义、算法和经验材料另列；父定理及其子结论仍可能分别为阅读目标，所以 **61 不是相互独立的定理数量**。最终数学状态和限制见[根代理验收](root-audit/acceptance.md)、各结果的 `proof_scope` 与实际类型：48 个完整范围内证明、2 个部分结论、4 个范围说明、7 个原文数学问题；这些类别不能混计。

已审校论文输入是聚合构建的依据。各论文目录中的生成/修补脚本记录整理过程；未经审阅差异，不得用旧生成脚本覆盖已修正的作者转录或人工核查结果。新论文可以直接按同一数据格式提供输入，无需复制历史整理脚本。

## 重建和查询

```bash
source scripts/env.sh
python research/full-proof-integration-20260930/iclr2024-generalizable/build_content.py
python research/full-proof-integration-20260930/aggregate.py
python research/full-proof-integration-20260930/architecture/paper_agent.py validate
python research/full-proof-integration-20260930/build_preview.py
```

Generalizable 的数学由两个数学组的 `generalizable-finite-results.json` 与 `generalizable-analysis-results.json` 汇合，原文转录保留在本篇目录。构建只使用显式清单的正式来源和当前报告。

```bash
python research/full-proof-integration-20260930/architecture/paper_agent.py paper-search Generalizable
python research/full-proof-integration-20260930/architecture/paper_agent.py search 'Theorem 6' --paper-id iclr2024-sparse
python research/full-proof-integration-20260930/architecture/paper_agent.py result iclr2024-sparse-theorem2
python research/full-proof-integration-20260930/architecture/paper_agent.py symbols --paper-id iclr2024-sparse
python research/full-proof-integration-20260930/architecture/paper_agent.py shared
python research/full-proof-integration-20260930/architecture/paper_agent.py issues
```

这些接口读本地文件，不调用模型、不运行任意 shell，也不是已部署的 MCP 服务。机器证据查询会核对源码哈希；网页快照需在源码变化后重建。

## 修改数学后验证

只运行受修改影响的验证，再统一更新公共目录。以下分别对应有限组合、Sparse/概率分析、经典混合偏导及公共包：

```bash
python research/full-proof-integration-20260930/cvpr2023/verify_finite.py
python research/full-proof-integration-20260930/iclr2024-sparse/verify_math.py
python research/full-proof-integration-20260930/cvpr2023/verify_derivative.py
scripts/verify-lean.sh
```

替换报告前保留历史证据。报告中的定义、辅助引理、适配及结构投影数量不等于论文定理数量；反例编译通过也不等于原命题被证明。实际源码、成功命令、完整类型和传递公理共同决定可展示状态。白名单只有 `propext`、`Classical.choice`、`Quot.sound`，禁止 `sorryAx`。

启动独立本机服务后可做真实浏览器检查：

```bash
python research/full-proof-integration-20260930/check_preview.py --base http://127.0.0.1:8001/
```

该检查覆盖全部结果的阅读标签、共享正文及步骤往返，报告绑定数据和脚本哈希。它证明软件路径可用，不能替代数学审校。

## 后续论文与代理接手

先读项目 [AGENTS.md](../../AGENTS.md)、[扩展流程](../../docs/agent-extension-workflow.md)、[数据模型](../../docs/paper-agent-data-model.md)、[文字到 Lean](../../docs/human-to-lean.md)、[AI 调用公共库](../../docs/ai-use-library.md)。新增正式论文通过 manifest 增加配置，不修改硬编码白名单。

未发表稿件放在项目 `inbox/<paper>/`，沿用 `scripts/archive inbox` 的私有本地流程，默认 `unpublished/private`。不能为了进入这个公开阅读器而改成 `public/published`。当前三篇获 `proof_only_granted`：可忠实修正证明并标原错处，原假设与结论不变；错误命题单列。其他材料沿用各自授权。

代理分工为两到三名核查/重写数学、一名整理网页和数据、根代理协调验收。本次 max 代理已交付，后续新代理采用 `gpt-6.1-sol / xhigh`。
