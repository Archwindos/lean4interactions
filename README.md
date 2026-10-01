# lean4interactions · Harsanyi 交互证明档案库

本项目把 DNN 交互论文的正式原文、规范符号、中英证明重写、共享数学结果和 Lean 4 证明放在同一阅读入口，方便研究者核查论证，也方便后续论文与 AI 复用公共库 `HarsanyiLib`。论文原陈述、项目重写和实际机器验证分别保存；原文中的错误步骤、反例与未明确的条件可以追溯。

仓库提供三部分：可直接在本机打开的论文阅读器、可独立调用的 Lean 数学库，以及用于导入和维护稿件的本地档案工具。

## 当前收录与证明范围

当前活动阅读器位于 `reader/preview/`，显式清单收录六篇正式论文，共七份 PDF、162 页：

| 论文 ID | 正式论文 | 页数 |
| --- | --- | ---: |
| `cvpr2023-sparse-concepts` | CVPR 2023 Sparse Concepts | 10 + 27 |
| `iclr2024-sparse` | ICLR 2024 Sparse Interaction Primitives | 34 |
| `iclr2024-generalizable` | ICLR 2024 Generalizable Interaction Primitives | 23 |
| `icml2023-harsanyinet` | ICML 2023 HarsanyiNet | 22 |
| `icml2024-layerwise` | ICML 2024 Layerwise Change of Knowledge | 22 |
| `icml2025-coalition` | ICML 2025 Attributions in a Coalition | 24 |

每篇包含正文、附录及其正式补充材料的逐页清单。证明、定义、方法与经验材料分别呈现；英文切换覆盖证明正文、假设、定义和共享证明，原公式与 Lean 映射保持。每个结果的完整证明、条件性说明、部分结论、命题反例及机器验证分别记录，不能用网页存在或编译数量代替数学完成数。

当前汇总为171个来源清单条目、168个阅读结果、104个证明或推导目标，以及15份共享证明。104个目标中，66个交付记录范围内的完整证明正文，38个交付反例、部分结论或范围说明；214条来源符号记录统一到151个规范概念，并保留定义域与原记号。逐篇计数与机器证据角色见[当前统计](reader/evidence/status-summary.json)。Lean 主证据角色互斥统计为69个定理、16个部分范围、2个反例与17个无当前映射目标。部分范围目标也可能含形式化反例，例如HarsanyiNet的空感受野引理与CNN门控子句；这些反例保留在实际声明中。定理角色仍以实际类型与记录范围为准，不表示所有原命题均成立。

原三篇在 2026-09-30 的验收为100个阅读条目、61个目标，其中48个在记录范围内完成中文与 Lean 证明，另有13个部分、范围说明或原文问题目标。该统计属于[历史验收](research/full-proof-integration-20260930/root-audit/acceptance.md)，不与本轮新篇直接相加；当前数量与检查报告见 [reader/evidence](reader/evidence/) 和[当前状态](docs/STATUS.md)。来源、数学边界与独立软件检查见[本轮根验收记录](docs/reviews/next-version-root-audit-20261001.md)。结构或语言测试不能代替原命题语义审查。

本轮完整回归71项通过，实际Chromium六篇中英遍历5,501项通过、零失败；浏览器报告绑定冻结快照与全部构建输入，见[浏览器检查](reader/evidence/browser-checks.json)。

## 快速开始：打开论文阅读器

只阅读已生成的静态快照，需要 Python 3 和浏览器。以下命令使用 Bash，从克隆后的仓库根目录执行：

```bash
git clone https://github.com/Archwindos/lean4interactions.git
cd lean4interactions
source scripts/env.sh
python3 -m http.server 8001 --bind 127.0.0.1 \
  --directory reader/preview
```

打开 **http://127.0.0.1:8001/**，按论文进入目录，或检索题名、原定理编号、别名和关键词。每个结果可切换中文/English证明、原命题、作者原证明及 Lean 步骤对应；共享证明、符号和原文问题各有独立入口。正式 PDF 使用对应源文件的页码定位。结束服务时按 `Ctrl+C`。

服务目录使用上面的 `preview/`，它是显式公开清单生成的快照。阅读器使用从 HTTP 根目录开始的资源路径，因此请通过此服务打开，不能直接双击 HTML，也不能直接作为 GitHub Pages 子路径站点。私稿的本地档案界面另用 8000 端口，见下文。

## 安装完整开发环境

当前安装脚本和 Conda 锁文件面向 **Linux x86_64**。准备可执行的 Conda（如 Miniforge）、Git、`curl`、`tar` 和 `zstd`；首次安装需要网络下载 Python 包、Lean、mathlib 和官方缓存。其他系统需另行准备对应工具链，当前脚本没有提供其安装流程。

在仓库根目录运行：

```bash
source scripts/env.sh
scripts/bootstrap.sh
python scripts/check-python-locks.py
scripts/lean-install.sh
```

`bootstrap.sh` 使用 `CONDA_EXE`，未设置时寻找 `conda` 命令，创建 Python 3.12 环境并安装本地档案工具。如果 Conda 未在 PATH 中，先将 `CONDA_EXE` 设为实际可执行文件路径；例如已将 Miniforge 安装到仓库内的 `.tools/miniforge/` 时：

```bash
export CONDA_EXE="$PWD/.tools/miniforge/bin/conda"
scripts/bootstrap.sh
```

`check-python-locks.py` 检查依赖锁中是否残留本机文件路径。`lean-install.sh` 下载并校验固定的 Lean 4.24.0 二进制，获取固定 mathlib 提交与模块缓存。公共库为 **HarsanyiLib 0.2.0**，mathlib 提交为 `f897ebcf72cd16f89ab4577d0c826cd14afaafc7`。

环境、工具、缓存与临时文件分别位于 `.conda-env/`、`.tools/`、`.cache/`、`.tmp/`，不修改 HOME 或 shell profile。之后每次打开终端，从仓库根目录运行 `source scripts/env.sh` 即可使用已有环境。离线使用完整开发环境需要事先准备好这些依赖；Git 克隆不包含工具链与缓存。

## 可选浏览器验收依赖

阅读已生成的静态站点只需 Python 3 和普通浏览器。运行 `reader/check_preview.py` 的自动验收另需 Playwright 与 Chromium；这些工具被忽略，也不属于生产环境依赖锁。以下固定版本对应本轮实际安装和验收，使用项目的 Python 3.12，并把 Python 包和浏览器都安装在项目目录中：

```bash
source scripts/env.sh
python -m pip install \
  --target research/reader-redesign-20260930/browser-tools/python \
  playwright==1.63.0 pyee==13.0.1 greenlet==3.5.6 typing_extensions==4.16.0
export PYTHONPATH="$PWD/research/reader-redesign-20260930/browser-tools/python${PYTHONPATH:+:$PYTHONPATH}"
export PLAYWRIGHT_BROWSERS_PATH="$PWD/research/reader-redesign-20260930/browser-tools/browsers"
python -m playwright install chromium
```

安装和运行使用同一个 `PLAYWRIGHT_BROWSERS_PATH`，见[Playwright 官方浏览器说明](https://playwright.dev/python/docs/browsers)。按快速开始在另一终端启动 8001 服务后，运行 `python reader/check_preview.py --base http://127.0.0.1:8001/`。公式解析检查 `node reader/check_math.js` 另需 Node.js，直接使用仓库内的 KaTeX，不需要 npm 安装。

## 使用和验证 Lean 库

公共库只依赖 mathlib，可脱离网页和档案工具使用。安装依赖后，在仓库根目录运行：

```bash
source scripts/env.sh
scripts/verify-lean.sh
```

该命令构建 `lean/HarsanyiLib`、`lean/PaperProofs` 和 `examples/library-consumer`，按审计入口的实际本包 import 闭包导出类型、逐声明审计公理，并更新基础154条 API 的 `catalog/library.json`。新独立 Extensions 的额外接口使用各篇真实报告验收，不由基础 barrel 审计代替。报告路径由脚本输出，历史报告保留。可信声明的公理白名单为 `propext`、`Classical.choice`、`Quot.sound`，禁止 `sorryAx`。源码改变后需重新验证，旧报告不能自动证明新源码。

公共库提供 Möbius 交互与重构、唯一性、中心化、Shapley 等归因、AND/OR、稀疏性、噪声方差及经典混合偏导截断结果。下面摘自已编译的调用包，证明仿射变换对非空交互的影响：

```lean
import Harsanyi

namespace LibraryConsumer
open Finset Harsanyi
variable {α : Type*} [DecidableEq α]

theorem affine_nonempty (v : Game α) (a b : ℝ) (S : Finset α) (hS : S.Nonempty) :
    interaction (fun T => a * v T + b) S = a * interaction v S := by
  rw [interaction_add, interaction_smul, interaction_const, if_neg hS.ne_empty, add_zero]

end LibraryConsumer
```

可构建的下游包在 [examples/library-consumer](examples/library-consumer/Consumer.lean)。从根目录运行示例：

```bash
source scripts/env.sh
cd examples/library-consumer
lake build
lake exe demo
cd ../..
```

公共库基础版和论文具体适配分别验证。新扩展直接导入 `Harsanyi.Extensions.HarsanyiNetwork`、`Harsanyi.Extensions.LayerwiseKnowledge` 或 `Harsanyi.Extensions.CoalitionAttribution`，对应报告与实际范围由只读查询接口返回。统一基础库保持0.2.0；新模块独立报告不冒充已经重验的统一版本。上面的三包验证不会自动构建全部研究证明；论文适配的重跑命令为：

```bash
source scripts/env.sh
python research/full-proof-integration-20260930/cvpr2023/verify_finite.py
python research/full-proof-integration-20260930/iclr2024-sparse/verify_math.py
python research/full-proof-integration-20260930/cvpr2023/verify_derivative.py
python corpus/public/reader/icml2023-harsanyinet/verify_network.py
python corpus/public/reader/icml2023-harsanyinet/verify_network.py icml2024-layerwise
python corpus/public/reader/icml2025-coalition/verify_coalition.py
```

查看[公共库快速开始](docs/library-quickstart.md)、[API 说明](docs/library-api.md)和[当前阅读器复现说明](reader/README.md)。API 声明数、辅助引理数和论文证明数不可混计。

## 数学符号与边界

模型原始输出统一记作 `v(x_S)`；输入基线是向量 `r`，输出基线是标量 `v(x_∅)`。集合函数与中心化函数分别为：

```text
g(S)  = v(x_S)
g₀(S) = v(x_S) − v(x_∅)
```

原始交互、中心化交互、AND/OR 分量和再次掩码后的条件游戏分别记录。非空交互在中心化前后相同，空集交互有不同值；不能默认原输出的基线为零。Lean 的 `Game α` 使用 `Finset α → ℝ`，求和总体和参与集合均有限。具体定义、量词、分母条件和概率假设见[数学约定](docs/math-conventions.md)与各结果的实际类型。

当前结果没有把未量化的近似、模型训练效果或整体优化运行时间当作已证明结论。Sparse Case 2 的推断反例不否定 Theorem 2、3 的精确结论。浏览器检查和编译检查各自验证软件或形式化对象，不能替代中文证明与原文语义的核对。

## AI 查询和接手

本地只读接口可以检索论文、命题、符号、共享证明、问题和当前验证证据：

```bash
source scripts/env.sh
python reader/architecture/paper_agent.py paper-search Generalizable
python reader/architecture/paper_agent.py search 'Theorem 6' --paper-id iclr2024-sparse
python reader/architecture/paper_agent.py result iclr2024-sparse-theorem2
python reader/architecture/paper_agent.py verification-status iclr2024-sparse-theorem2
python reader/architecture/paper_agent.py library Harsanyi.Sparsity.CoefficientWitness
python reader/architecture/paper_agent.py validate
```

该接口读本地文件，核对验证证据的源码哈希，不调用模型；它是已实现的 CLI/Python 接口，尚未部署为 MCP 服务。`validate` 检查来源、逐页覆盖和数据关系，不进行数学证明审查。

AI 接手先读 [AGENTS.md](AGENTS.md)、[扩展流程](docs/agent-extension-workflow.md)和[数据模型](docs/paper-agent-data-model.md)。使用库时先查 [catalog/library.json](catalog/library.json) 的真实签名、推荐导入、版本和报告，再逐项对齐前提。文字到 Lean 的对应与交付要求见[中文证明到 Lean](docs/human-to-lean.md)及[AI 调用库](docs/ai-use-library.md)。

## 目录结构

```text
lean/HarsanyiLib/                         独立公共 Lean 库
lean/PaperProofs/                         基础论文调用包
examples/library-consumer/               可构建的独立调用示例
reader/                                 当前通用构建、UI、只读AI入口及验收证据
  preview/                               六篇双语静态阅读入口
corpus/public/                          独立公开池
  reader/input-manifest.json             显式正式论文清单
  reader/<paper_id>/                     每篇来源、清单、内容、符号与问题
  translations/                         旧篇与共享证明英文sidecar
corpus/private/                         独立私稿池，全部忽略，不公开
research/full-proof-integration-20260930/ 历史三篇快照及不可变Lean证据
research/paper-survey-20260930/           正式源文件与调研记录
catalog/                                公共 API 及说明
src/archive/                            本地稿件档案工具
scripts/、locks/                         环境、构建、验证与依赖锁
docs/、reports/                          使用文档与实际验证报告
inbox/                                  本地投入稿件；仓库仅保留 README.md
templates/                              元数据模板
```

旧阅读器与早期报告保留历史状态；当前阅读入口以 `reader/preview/` 为准，各阶段的计数不能相加。更广的[正式版候选表](docs/paper-candidates-20260930.md)未全部收录。

## 新增正式论文或私有稿件

新增公开正式论文时，先核实正式版本及其补充材料，记录来源链接、页数与 SHA-256。按现有格式建立 `paper-metadata.json`、`inventory.json`、`content.json`、`symbols.json` 和 `issues.json`，完成逐页清点、原文转录、中文重写、符号映射与实际验证，再在 `input-manifest.json` 增加显式配置。详细格式和构建命令见[扩展流程](docs/agent-extension-workflow.md)。公开阅读器只使用 `corpus/public/reader/input-manifest.json` 配置，不扫描 `corpus/private/` 或 `inbox/`；私稿不能通过改标签冒充正式来源。

未发表稿件在本地放入 `inbox/<paper>/`，将 [templates/paper-metadata.yaml](templates/paper-metadata.yaml) 复制为该目录的 `metadata.yaml`，保留默认 `unpublished/private`。例如：

```yaml
paper_id: my-draft
version: v1
title: 稿件题名
source_type: manual
publication_status: unpublished
visibility: private
```

安装完整 Python 环境后，从根目录运行；`my-draft` 与 `v1` 应对应导入返回的实际 ID 和版本：

```bash
source scripts/env.sh
scripts/archive inbox
scripts/archive --private extract my-draft --version v1
scripts/archive --private validate
scripts/archive --private build
scripts/archive --private serve --host 127.0.0.1 --port 8000
```

打开 http://127.0.0.1:8000/ 查看本地档案。导入保留原件，内容变化另建版本；自动提取只登记候选，仍需全文审校。详见[新增论文](docs/add-paper.md)。

**未发表论文及其来源副本、提取内容、证明、页面和报告等派生材料留在本地，不上传此仓库。** 仓库的 `inbox/` 仅保留 `README.md`，元数据模板位于 `templates/`。`.gitignore` 用于防止误纳入文件，既不是材料的公开授权，也不会自动删除已被 Git 跟踪的内容。后续添加稿件时须同时核对其元数据、私有派生关系和提交文件；公开清单与本地档案的可见性设置不能替代这项核对。默认 `ArchiveStore` 和 `archive serve` 只使用公开池与当前六篇 reader；`--private` 显式进入私稿管理。私稿可以引用公共证明，公共池不会读私稿。修改visibility不能迁移论文；`archive promote` 要求另行核对的正式PDF和正式publisher链接，并保留私稿及其衍生物。

安装完整 Python 环境后，公开提交前可运行[发布检查](scripts/check-publication.py)：

```bash
source scripts/env.sh
python scripts/check-publication.py --report .tmp/publish-20261001/staged-audit.json
```

默认检查 Git 暂存区的实际文件内容，覆盖已知私稿路径、私有/未发表元数据、原件复制、正文重叠、常见凭证格式、缓存/编译产物、未收录的调研下载及超过 95 MiB 的单个文件。报告只列路径与规则。暂存前可加 `--worktree` 检查工作区；退出码 0 表示通过已知规则，新增未标记私稿与变换后的图像仍需人工核对。

## 许可

本项目代码沿用仓库的 [Apache License 2.0](LICENSE)。论文 PDF、作者材料及 KaTeX 等第三方资源保留各自许可与权利归属，仓库许可证不扩大覆盖这些材料。

本机一键上传的检查、提交、实时推送和凭据配置见 [上传说明](docs/github-upload.md)。脚本 `scripts/upload-github.local.sh` 被忽略，仅本机使用；`--check-only` 不修改暂存区、提交或远端。
