# HarsanyiLib 最短使用流程

当前库工作区版本为 0.2.0，Lean 4.24.0；mathlib 提交为 `f897ebcf72cd16f89ab4577d0c826cd14afaafc7`（v4.24.0）。版本以 `lean/HarsanyiLib/lakefile.toml` 为准，实际验证状态以 `catalog/library.json` 引用的报告及其源码哈希为准。工作区升级不使旧报告自动有效。库的 Lake 配置锁定真实 git 提交，公共库只依赖 mathlib，不依赖 Python archive、网页或 PaperProofs。

在本项目根目录运行：

```bash
source scripts/env.sh
cd lean/HarsanyiLib
lake build
```

已有安装的工具链与缓存全部位于项目内。需要在新的 Linux x86_64 项目副本准备依赖时，运行 `scripts/lean-install.sh`；它下载固定 Lean 二进制、检查锁定的 SHA-256、获取固定 mathlib 与官方模块缓存。此安装需要网络，不修改 HOME 或 shell profile。离线副本必须携带工具链、缓存及依赖。单独携带 `lean/HarsanyiLib` 时，也可用相同版本的 Lean/Lake 执行 `lake update`、`lake exe cache get`、`lake build`；所有依赖由库的固定 manifest 决定。

独立下游已经位于 `examples/library-consumer`。其 `lakefile.toml` 用

```toml
[[require]]
name = "HarsanyiLib"
path = "../../lean/HarsanyiLib"
```

锁定本地库。这个路径只用在当前目录布局；新下游项目须按自己的位置修改它。`Consumer.lean` 中的一个新结论是“仿射重标定只按比例改变非空交互”：

```lean
import Harsanyi.Core.Properties

open Finset Harsanyi
example {α : Type*} [DecidableEq α] (v : Game α) (a b : ℝ)
    (S : Finset α) (hS : S.Nonempty) :
    interaction (fun T => a * v T + b) S = a * interaction v S := by
  rw [interaction_add, interaction_smul, interaction_const, if_neg hS.ne_empty, add_zero]
```

先拆可加性，再提出比例，最后用常数函数仅有空集交互的性质。非空前提至关重要。另一个新结论 `baseline_unique_nonempty` 组合唯一性和中心化转换，证明重构去基线游戏的系数与原游戏非空交互一致。

运行真实下游与数值演示：

```bash
source scripts/env.sh
cd examples/library-consumer
lake build
lake exe demo
```

示例输出 `baseline=7; I0=2; I1=3; I01=5` 与 `reconstruction=17; v(N)=17`。程序以精确有理数展示公式；一般实数结论已在 Consumer 中证明，数值输出不替代一般性证明。

回到根目录运行 `scripts/verify-lean.sh`，同时构建三包、导出真实签名、执行逐声明 `#print axioms` 和传递公理检查，并更新 `catalog/library.json`。报告路径由脚本打印；旧报告保留。构建成功与公理审计成功需要同时成立，源码变化使旧报告过期。

新增证明可以按数学对象选择模块，再从目录读取实际签名：

| 导入模块 | 提供的内容 | 使用时需核对 |
| --- | --- | --- |
| `Harsanyi.Core.Properties` | Möbius 交互、重构、唯一性、线性、中心化 | 原始输出与去基线输出的空集值不同 |
| `Harsanyi.Extensions.Attribution` | 高阶差分、阶乘权重 Shapley、Shapley interaction、Shapley–Taylor | 总体、目标子集、环境不相交；Shapley–Taylor 的实际正阶范围 |
| `Harsanyi.Extensions.OrInteraction` | OR 变换与重构、坐标掩码合成、条件输入 | OR 空集单列为输出基线；条件样本不能直接替换成原样本 |
| `Harsanyi.Extensions.Sparsity` | 分层均值、二项式矩阵、系数存在性见证、显著交互计数界 | 均值单调性、鲁棒性、截断条件、参数定义域及非零抵消比例 |
| `Harsanyi.Extensions.Noise` | 实际随机变量的交互方差与掩码噪声桥接 | 概率测度、噪声分布与独立性；固定模型输出和自适应参数须分清 |
| `Harsanyi.Extensions.DerivativeCutoff` | 混合偏导恒零、矩形有限差分、实际掩码交互截断 | 经典导数必须真实存在；不能只用 Lean 总函数 `deriv` 的数值为零代替可微性 |

共享库声明与某篇论文的应用是两个层次：公共库用于复用，论文适配核对原符号、基线和量词。全部论文应用及其独立报告见 `research/full-proof-integration-20260930/`；三包验证不会自动构建这个目录的所有研究文件。新下游仍须单独构建并审计。
