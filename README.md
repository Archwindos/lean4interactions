# lean4interactions · Harsanyi 交互证明档案库

本项目整理 DNN 交互研究中的正式论文，将作者原文、规范符号、中英证明重写、共享数学结果和 Lean 4 证明放在同一阅读入口。研究者可以对照原文核查论证，后续论文和 AI 可以查找、调用独立公共库 `HarsanyiLib` 中的准确声明。

仓库包含静态论文阅读器、独立 Lean 数学库，以及用于导入和维护稿件的本地档案工具。原陈述、项目重写和机器验证分别保存，便于追溯证明依据及适用范围。

## 功能与数学边界

- **正式原文对照**：保存正式会议或期刊版本、附录和正式补充材料，按 PDF 页码关联逐页清单、命题与证明。
- **中英证明阅读**：检索题名、原定理编号、别名和关键词；切换中文/English，阅读原命题、作者原证明、重写步骤及对应 Lean 声明。
- **共享证明与 Lean 库**：公共证明正文集中保存，各篇记录自身定义和条件到公共结果的适配；`HarsanyiLib` 可脱离网页和档案工具使用。
- **符号与问题记录**：保留论文原符号、定义域和作用域到规范概念的映射，分别记录证明步骤错误、命题反例、条件缺口和部分结论。
- **独立私稿池**：公开阅读器只读取显式公开清单；私稿保存在本地独立池，可以引用公共证明，公开池不读取私稿。

论文原陈述和假设保持原样。证明有错误时，标注原错误位置与依据，再给出同一原命题的修正证明；原命题本身错误时单列反例，不能通过添加假设或改变结论把它变成已证明命题。

完整文字证明、条件性说明、部分组件、反例和未形式化结果分别记录。Lean 编译与公理审计覆盖具体声明及其前提；高阶库定义、辅助引理或模型子结果的编译，不等于原论文定理已经证明。浏览器检查验证展示行为，不能替代原文语义和数学审查。

模型原始输出统一记作 `v(x_S)`。输入基线是向量 `r`，输出基线是标量 `v(x_∅)`；集合函数与中心化函数分别为：

```text
g(S)  = v(x_S)
g₀(S) = v(x_S) − v(x_∅)
```

非空交互在中心化前后相同，空集交互不同，不能默认原始输出基线为零。Lean 的 `Game α` 使用 `Finset α → ℝ`；AND/OR 分量、再次掩码的条件游戏、概率假设与分母条件须逐项核对。详见[数学约定](docs/math-conventions.md)和各声明的实际类型。

## 一键打开阅读器

只阅读仓库中已有的静态快照，需要 **Python 3.8+ 和浏览器**。启动器只使用 Python 标准库，无需安装 Conda、Lean 或构建依赖。

```bash
git clone https://github.com/Archwindos/lean4interactions.git
cd lean4interactions
./start.sh
```

Linux / macOS 执行 `./start.sh`；Windows 双击根目录的 `start.bat`，或在终端运行它。启动后打印本机地址并自动打开浏览器，保持终端打开，按 `Ctrl+C` 停止服务。默认使用 8000 端口，被占用时自动选择空闲端口；服务只监听 `127.0.0.1`。

需要手动打开浏览器或指定端口时：

```bash
./start.sh --no-browser --port 8080
```

Windows 可运行 `start.bat --no-browser --port 8080`。`--port 0` 自动分配端口；更多选项见[启动说明](docs/start-reader.md)。当前入口是 [reader/preview](reader/preview/index.html)，页面资源使用 HTTP 根路径，请通过启动器访问。不要直接双击 HTML；部署到 GitHub Pages 子路径时还需处理资源路径。

## 开发环境与阅读器重建

其他使用者自行配置所需环境。仓库提供的安装脚本和 Conda 锁文件面向 **Linux x86_64**，需要 Conda、Git、`curl`、`tar` 和 `zstd`；首次安装需要网络。其他系统需准备对应 Python 包、Poppler 和 Lean 工具链。

从仓库根目录执行：

```bash
source scripts/env.sh
scripts/bootstrap.sh
python scripts/check-python-locks.py
scripts/lean-install.sh
```

`bootstrap.sh` 创建 Python 3.12 环境并安装档案工具、pypdf 与 Poppler。若 Conda 不在 PATH，先将 `CONDA_EXE` 设为实际可执行文件路径。`lean-install.sh` 安装固定 Lean 4.24.0，获取锁定的 mathlib 提交与官方缓存；准确版本见[依赖锁](locks/lean-dependencies.json)和 [Lake 配置](lean/HarsanyiLib/lakefile.toml)。

本机环境 `.conda-env/`、工具 `.tools/`、缓存 `.cache/`、临时文件 `.tmp/` 均为被忽略的本地存储，**不随仓库上传或克隆分发**。脚本不修改 HOME 或 shell profile；已有本地环境可通过 `source scripts/env.sh` 使用。离线开发需提前准备依赖，阅读静态快照则只需系统 Python。

活动输入由 [input-manifest.json](corpus/public/reader/input-manifest.json) 显式配置。修改内容后，按顺序重新聚合、构建数据包和阅读快照：

```bash
source scripts/env.sh
python reader/aggregate.py
python reader/architecture/build_package.py
python reader/architecture/paper_agent.py validate
python reader/build_preview.py
```

构建核对聚合输入和输出的 SHA-256，检查正式 PDF 页数；缺失原页缓存由 `pdftoppm` 重新生成。默认构建拒绝缺译或未交付的证明目标，开发预览选项与完整检查命令见[阅读器维护说明](reader/README.md)和[论文扩展流程](docs/agent-extension-workflow.md)。`validate` 检查来源、逐页覆盖和数据关系，不进行数学证明审查。

可选浏览器验收另需 Playwright 与 Chromium，它们也留在本地。以下版本为已有验收环境的配置：

```bash
source scripts/env.sh
python -m pip install \
  --target research/reader-redesign-20260930/browser-tools/python \
  playwright==1.63.0 pyee==13.0.1 greenlet==3.5.6 typing_extensions==4.16.0
export PYTHONPATH="$PWD/research/reader-redesign-20260930/browser-tools/python${PYTHONPATH:+:$PYTHONPATH}"
export PLAYWRIGHT_BROWSERS_PATH="$PWD/research/reader-redesign-20260930/browser-tools/browsers"
python -m playwright install chromium
```

在另一终端运行 `./start.sh --no-browser --port 8001`，再运行 `python reader/check_preview.py --base http://127.0.0.1:8001/`。公式解析检查 `node reader/check_math.js` 另需 Node.js，使用仓库内的 KaTeX，无需 npm 安装。

## 调用与验证 Lean 库

公共库只依赖 mathlib。安装工具链后，可独立构建公共包或运行三包验证：

```bash
source scripts/env.sh
(cd lean/HarsanyiLib && lake build)
scripts/verify-lean.sh
```

`verify-lean.sh` 构建 `lean/HarsanyiLib`、`lean/PaperProofs` 和 `examples/library-consumer`，按审计入口的实际 import 闭包导出类型、审计逐声明公理，并更新 [catalog/library.json](catalog/library.json)。源码改变后需重新验证，旧报告不能证明新源码。可信声明的公理白名单为 `propext`、`Classical.choice`、`Quot.sound`，禁止 `sorryAx`。

基础模块包含有限 Möbius 交互与重构、唯一性、中心化、Shapley 等归因、AND/OR、稀疏性、噪声方差和经典混合偏导截断结果。下面的例子使用可加性、比例律和常数函数交互，证明仿射变换对非空交互的影响：

```lean
import Harsanyi.Core.Properties

open Finset Harsanyi
example {α : Type*} [DecidableEq α] (v : Game α) (a b : ℝ)
    (S : Finset α) (hS : S.Nonempty) :
    interaction (fun T => a * v T + b) S = a * interaction v S := by
  rw [interaction_add, interaction_smul, interaction_const, if_neg hS.ne_empty, add_zero]
```

可构建的下游包见 [Consumer.lean](examples/library-consumer/Consumer.lean)。独立扩展组合示例见 [ExtensionConsumer.lean](examples/library-consumer/ExtensionConsumer.lean)：

```bash
source scripts/env.sh
(cd examples/library-consumer && lake build && lake exe demo)
(cd examples/library-consumer && lake env lean ExtensionConsumer.lean)
```

新增公共扩展用实际 `Harsanyi.Extensions.<Module>` 路径直接导入，并查看对应独立报告；基础审计不会自动覆盖所有论文适配或未导入的扩展。具体模块、完整前提和下游配置见[公共库快速开始](docs/library-quickstart.md)与[API 说明](docs/library-api.md)。已有论文适配的独立重验入口包括：

```bash
source scripts/env.sh
python research/full-proof-integration-20260930/cvpr2023/verify_finite.py
python research/full-proof-integration-20260930/iclr2024-sparse/verify_math.py
python research/full-proof-integration-20260930/cvpr2023/verify_derivative.py
python corpus/public/reader/icml2023-harsanyinet/verify_network.py
python corpus/public/reader/icml2023-harsanyinet/verify_network.py icml2024-layerwise
python corpus/public/reader/icml2025-coalition/verify_coalition.py
```

这些入口只覆盖各自报告范围，其他论文按其活动目录中的实际验证脚本运行。

## AI 查询与复用

本地只读 CLI 可以检索论文、结果、符号、共享证明、问题和验证证据：

```bash
source scripts/env.sh
python reader/architecture/paper_agent.py paper-search Generalizable
python reader/architecture/paper_agent.py search 'Theorem 6' --paper-id iclr2024-sparse
python reader/architecture/paper_agent.py result iclr2024-sparse-theorem2
python reader/architecture/paper_agent.py verification-status iclr2024-sparse-theorem2
python reader/architecture/paper_agent.py library Harsanyi.Sparsity.CoefficientWitness
python reader/architecture/paper_agent.py shared
```

接口读取本地文件并核对报告的源码哈希，不调用模型；目前实现为 CLI/Python 接口，尚未部署为 MCP 服务。复用前先读准确签名、直接导入路径、条件和当前证据，再写论文对象到公共库对象的适配，编译并保存自己的审计结果。

AI 接手先读 [AGENTS.md](AGENTS.md)、[贡献说明](CONTRIBUTING.md)、[扩展流程](docs/agent-extension-workflow.md)和[数据模型](docs/paper-agent-data-model.md)。步骤与 Lean 对应要求见[中文证明到 Lean](docs/human-to-lean.md)，模块选择与实际消费流程见[AI 调用库](docs/ai-use-library.md)。

## 新增论文与管理私稿

新增公开论文时，先核实正式版本和补充材料，记录来源链接、页数与 SHA-256，再建立 `paper-metadata.json`、`inventory.json`、`content.json`、`symbols.json` 和 `issues.json`。完成逐页清点、原文转录、双语重写、符号映射及相应范围的验证后，将配置加入显式清单。详细格式见[扩展流程](docs/agent-extension-workflow.md)。

未发表稿件在本地放入 `inbox/<paper>/`，将 [templates/paper-metadata.yaml](templates/paper-metadata.yaml) 复制为 `metadata.yaml`，保留默认 `unpublished/private`。安装完整 Python 环境后，可使用以下入口；`my-draft` 和 `v1` 应替换为导入返回的实际 ID 与版本：

```bash
source scripts/env.sh
scripts/archive inbox
scripts/archive --private extract my-draft --version v1
scripts/archive --private validate
scripts/archive --private build
scripts/archive --private serve --host 127.0.0.1 --port 8000
```

打开 http://127.0.0.1:8000/ 查看本地私稿档案，使用与公开阅读器不同的空闲端口。导入保留原件，内容变化另建版本；自动提取只登记候选，仍需全文审校。详见[新增论文](docs/add-paper.md)。默认档案查询和服务使用公开池，`--private` 显式进入独立私稿池。

**未发表论文、私有来源副本及其提取内容、证明、页面和报告留在本地，不上传仓库。** `inbox/` 只提交说明，元数据模板放在 `templates/`。修改 visibility 不构成发表迁移；`archive promote` 要求另行核对的正式 PDF 和出版方链接，并保留私稿及其衍生物。公开池不读取 `corpus/private/` 或 `inbox/`。

公开提交前运行[出版检查](scripts/check-publication.py)：

```bash
source scripts/env.sh
python scripts/check-publication.py --report .tmp/publication-staged-audit.json
```

默认核对 Git 暂存区的实际内容；暂存前可加 `--worktree`。检查覆盖已知私稿、未发表元数据、原件复制、凭据模式、缓存和大文件等规则，新增未标记材料仍需人工核对。`.gitignore` 不会自动移除已有跟踪文件，也不构成公开授权。仓库上传方法见[上传说明](docs/github-upload.md)；本机辅助脚本被忽略，不随仓库分发。

## 目录结构

```text
lean/HarsanyiLib/            独立公共 Lean 库
lean/PaperProofs/            论文调用包
examples/library-consumer/  独立下游调用示例
reader/                     聚合、构建、UI、只读查询和检查入口
  preview/                  已构建的正式论文双语静态阅读器
corpus/public/              公开档案池与显式 reader 清单
corpus/private/             本地私稿池，被忽略
catalog/                    公共 API 目录
src/archive/                本地稿件档案工具
research/                   调研记录与报告仍依赖的历史来源/源码
scripts/、locks/             启动、环境、验证与依赖锁
docs/、reports/              使用文档与实际验证报告
inbox/、templates/           本地稿件投入目录与可提交模板
```

## 许可

代码使用 [Apache License 2.0](LICENSE)。论文 PDF、作者材料和 KaTeX 等第三方资源保留各自许可与权利归属，仓库许可证不扩大覆盖这些材料。

## 本版本更新

当前显式清单和 `reader/preview/` 快照覆盖 **12 篇正式论文、14 份 PDF、331 页、355 个阅读结果、256 个证明或推导目标、37 份共享证明**。阅读结果包含定义、方法和范围说明，数量不代表原命题已证明或全部形式化。

| 论文 ID | 正式论文 | 页数 |
| --- | --- | ---: |
| `cvpr2023-sparse-concepts` | CVPR 2023 Sparse Concepts | 10 + 27 |
| `iclr2024-sparse` | ICLR 2024 Sparse Interaction Primitives | 34 |
| `iclr2024-generalizable` | ICLR 2024 Generalizable Interaction Primitives | 23 |
| `icml2023-harsanyinet` | ICML 2023 HarsanyiNet | 22 |
| `icml2024-layerwise` | ICML 2024 Layerwise Change of Knowledge | 22 |
| `icml2025-coalition` | ICML 2025 Attributions in a Coalition | 24 |
| `neurips2021-robustness` | NeurIPS 2021 Adversarial Robustness | 14 + 16 |
| `neurips2024-dynamics` | NeurIPS 2024 Learning Dynamics | 36 |
| `icml2022-transformation` | ICML 2022 Transformation Complexity | 22 |
| `icml2023-bayesian` | ICML 2023 Bayesian Neural Networks | 25 |
| `icml2023-decoder` | ICML 2023 Image Decoder Frequency Bias | 34 |
| `neurips2023-difficulty` | NeurIPS 2023 Concept Learning Difficulty | 22 |

本版本扩展了正式论文与公共模块，加入独立公开/私稿池、双语阅读内容、符号作用域映射和共享证明适配；新增扩展保持直接导入及独立报告。基础 `HarsanyiLib` 为 0.2.0，基础目录的154条 API 与扩展声明分别审计。证明修正和原命题反例按实际对象标注，范围分析与部分组件不计为原命题完整证明。

新增 `start.sh` / `start.bat`，直接展示已有快照。Linux 启动已做最小验证；Windows 启动器尚未在 Windows 实机测试。环境与依赖缓存仅存本地，不包含在上传内容中。

十二篇最终整体验收**尚未闭合**，剩余事项见[状态记录](docs/STATUS.md)和[验收操作单](docs/twelve-paper-validation-runbook-20261001.md)。现有数学报告与软件检查各自覆盖其记录范围，不据此宣称全部正式命题已证明或全量验收完成。阶段记录与修复依据见[根审查记录](docs/reviews/twelve-paper-root-audit-20261001.md)；历史阶段的计数只描述当时快照，不与本版本相加。

本次清理删除旧 demo、公开验收截图及可重建原页缓存。保留当前阅读器的正式 PDF 与原页展示图片，以及活动数学报告绑定的源码、来源副本、转录和哈希证据；历史媒体链接不再作为可用图片入口。清理记录见[清理说明](docs/CLEANUP.md)。后续数学、界面第二阶段及发布安排以用户另行授权为准。
