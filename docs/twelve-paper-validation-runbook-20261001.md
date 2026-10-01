# 十二篇第一轮最终验收执行顺序

这是待 F06 正式准入后执行的操作单，不是通过报告。授权、数学审查与发布边界以[第一轮契约](twelve-paper-release-20261001.md)和根验收记录为准。第二轮界面布局、全库记号改写与公共证明归并仍只做设计。

所有命令在 `/mnt/data2/wyh/lean4project` 执行，shell 使用 `login:false`。先完成维护文档的最终模块导航及当前范围说明，再冻结输入；生成的当前证据均位于 `reader/evidence/twelve-paper-20261001/`。八篇、十篇中间报告和首次失败报告保留，不覆盖成十二篇最终报告。本文中的浏览器命令读取真实发布目录，不启用候选 UI 路由覆盖。

## 1. 冻结前的人工门与预期分母

六篇新增论文分别须有当前 `root-f01/f04/f06/f07/f08/f10-admission.json`，状态为 `approved_for_phase1_reader_admission`，其中全部 `input_hashes` 与实际文件一致。F06 尚未准入时停止；不能用 draft admission、软件通过或 `in_progress` 代替根准入。每篇来源/数学反馈及互审缺项由根逐项核销，特别包括同标题在正文与附录的对象、前提或公式不同的出现记录。

下表是本操作单编写时的候选预期，F06 仍在开发。冻结后从实际库存和内容重新计算；发现新增数学目标就更新预期及根准入，不能为保持表中数字删除目标。

| 输入 | 阅读 results | proof targets | 正式 PDF 文件 | 实际物理页 | 实际报告声明数 |
| --- | ---: | ---: | ---: | ---: | ---: |
| 原六篇基线 | 168 | 104 | 7 | 162 | 按原当前报告保全 |
| F01 Robustness | 27 | 26 | 2 | 30 | 80 |
| F04 Transformation | 34 | 31 | 1 | 22 | 222 |
| F06 Decoder，开发预期 | 34 | 30 | 1 | 34 | 待实际最终报告 |
| F07 Dynamics | 32 | 22 | 1 | 36 | 75 |
| F08 Bayesian | 22 | 15 | 1 | 25 | 103 |
| F10 Difficulty | 38 | 28 | 1 | 22 | 170 |
| 候选合计 | 355 | 256 | 14 | 331 | 不将各报告声明数相加当作已证明目标数 |

来源出现记录另计：库存使用 `all_occurrences`、`occurrences` 或 `appearances`，保留每条实际位置与编号；F06 的独立 `source-occurrence-map.json` 当前 52 个出现记录也单独核对。出现记录可多对一归并到 result，result 也可能只是定义或实验说明。证明目标以布尔字段及显式归并后的唯一 result ID 集合为分母。共享正文数按实际唯一 shared ID 计数，不能把同一证明被多篇引用的次数当作独立证明数。

冻结前必须确认：原六篇的 168 results、15 shared、104 targets，以及 17 个无 Lean 映射目标保持原意义；新条目的 `false` 分类与理由已人工读过；完整证明、条件性子结果、反例、外部依据/范围说明分别记录。Lean 的 `theorem_proof/counterexample/partial_component/none` 是机器证据维度，不能覆盖源命题判断。

## 2. 项目环境与最终准入哈希门

```bash
set -euo pipefail
source scripts/env.sh
python - <<'PY'
import hashlib
import json
import sys
from pathlib import Path
sys.path.insert(0, 'reader')
from input_manifest import load_manifest

root = Path.cwd()
baseline = json.loads(Path('reader/evidence/six-paper-preservation-baseline.json').read_text())
new = {
    'f01': 'neurips2021-robustness',
    'f04': 'icml2022-transformation',
    'f06': 'icml2023-decoder',
    'f07': 'neurips2024-dynamics',
    'f08': 'icml2023-bayesian',
    'f10': 'neurips2023-difficulty',
}
manifest = load_manifest()
assert {p['paper_id'] for p in manifest['papers']} == set(baseline['paper_ids']) | set(new.values())
assert len(manifest['papers']) == 12
bound = {}
for short, paper_id in new.items():
    path = Path('reader/evidence/twelve-paper-20261001') / ('root-' + short + '-admission.json')
    admission = json.loads(path.read_text())
    assert admission['status'] == 'approved_for_phase1_reader_admission', str(path)
    assert admission['paper_id'] == paper_id, str(path)
    assert admission.get('input_hashes'), str(path)
    required = {'corpus/public/reader/' + paper_id + '/' + name for name in (
        'content.json', 'inventory.json', 'paper-metadata.json', 'symbols.json',
        'issues.json', 'verification/report.json')}
    assert required <= set(admission['input_hashes']), str(path)
    for relative, expected in admission['input_hashes'].items():
        target = root / relative
        assert target.is_file() and hashlib.sha256(target.read_bytes()).hexdigest() == expected, relative
        bound[relative] = expected
    bound[path.as_posix()] = hashlib.sha256(path.read_bytes()).hexdigest()
bound['corpus/public/reader/input-manifest.json'] = hashlib.sha256(
    Path('corpus/public/reader/input-manifest.json').read_bytes()).hexdigest()
record = {'status': 'admitted_input_hashes_current', 'scope': 'Root admission hash gate only; later full checks remain.',
          'paper_count': 12, 'input_hashes': bound}
Path('reader/evidence/twelve-paper-20261001/final-input-freeze.json').write_text(
    json.dumps(record, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({'status': record['status'], 'paper_count': 12, 'bound_inputs': len(bound)}))
PY
```

**停止条件：** 未准入、清单不恰为授权十二篇、任何根绑定文件变化。由数学作者更新实际内容/报告，根重新审阅绑定；不能修改哈希期待值来绕过。此门不证明报告的传递依赖仍新鲜，后续严格构建和 API 检查继续检查实际依赖。

## 3. 聚合、库存与证明交付契约

```bash
python reader/check_inputs.py
python reader/aggregate.py
python reader/architecture/build_package.py
python reader/architecture/paper_agent.py validate
python reader/check_completion.py
python reader/check_bilingual.py
python reader/check_symbols.py
python reader/check_preservation.py
```

| 检查 | 实际分母与证据 | 停止条件 |
| --- | --- | --- |
| 输入 | `input-preflight.json`：12 篇、14 个实际 PDF、331 页；每篇全部逐页 audit | 源 hash/实际页数/来源 ID、精确覆盖、目标映射或分类契约错误 |
| 聚合 | `aggregate-report.json`、`data/full-content.json`：每个 inventory entry 唯一解析，逐条目标与根目标集合一致 | 默认丢目标、隐式跨 ID 映射、重复引用、共享/符号/问题悬挂 |
| 机器包 | `architecture/agent-package.json` 的 validation，加查询接口 `validate` | schema 或来源/循环步骤引用校验失败 |
| 证明内容 | `content-completion-checks.json`：实际全部 proof targets；当前候选为 256 | 未交付、空证明/引用、整页抽取冒充完整 TeX、未知角色或明确项目注污染作者字段 |
| 双语 | `bilingual-checks.json`：全部正文、条件、定义、步骤、共享、符号、问题的人读字段 | 缺译、英文夹未译中文、保护字段被翻译层覆盖；内联公式差异未审结 |
| 符号 | `symbol-coverage-checks.json`：每个源符号记录及全部映射，canonical 数可小于源记录数 | 作用域/定义域/基线/冲突映射丢失或跨 owner 错映射 |
| 保全 | `six-paper-preservation-checks.json`：168 results、15 shared、原件和输入、17 个无 Lean 映射目标 | 原六篇非翻译语义或来源字节改变、旧证据被新报告静默替换 |

`check_completion.py` 的 `required_manual_step_basis_reviews` 必须由数学审查核对实际步骤依据；不要求把正文已有论证机械复制到第二字段。`check_bilingual.py` 的退出码只拒绝 missing，**内联公式差异另设停止门**：无差异可继续；有差异须逐项核对实际公式并保存与当前 full-content hash 一致的审阅记录，未审结停止。不能用“字符串差异”自动认定数学错误，也不能因退出码为零忽略差异。

开发稿预检的 `machine_role_status_reviews` 同样须作者依据实际类型裁定。例如完整错误子句的机器反例与父命题部分反驳可以共存；只有有限域组件而人读反例未 formalize 时保持 `partial_component`。不根据声明名字自动改角色。

## 4. 实际公式、公共 API 与独立消费

```bash
node reader/check_math.js
python reader/architecture/check_api.py --report-name twelve-paper-api-checks.json
python reader/check_library_consumer.py
```

`math-rendering-check.json` 必须由真实本地 KaTeX 解析当前全量公式，errors 为零；公式数按当前实际输入记录，不预设或以公式数表示数学完成。入站契约同时拒绝损坏的控制字符，KaTeX 成功不能替代该检查。

`twelve-paper-api-checks.json` 检查当前查询/类型/源码/公理/报告绑定、全部实际独立公共声明及真实 direct import。最终 `docs/library-api.md`、`docs/ai-use-library.md`、添加论文流程须覆盖已准入的 Entropy/Gates、Gaussian/Polynomial/NoisyRegression、Transformation 实际模型扩展、Fourier/Decoder 和 Difficulty 公共模块；精确名称来自实际报告与 `paper_agent.py library`，论文 `Paper*` 应用仍标论文适配。基础 0.2.0 的 154 条不替代独立扩展清单。无需改旧 barrel 或为刷新数据无谓重跑基础统一审计。

`direct-import-consumer-checks.json` 必须实际编译 `ExtensionConsumer.lean`、组合三条公共 Robustness 引理，输出精确定理类型及传递公理；当前预期 10 项检查和 1 条独立消费定理，允许非零模型输出 baseline。消费成功只证明这条应用，不代表任一原论文的全部命题成立。

**停止条件：** 公式错误、API 缺少当前声明/类型/import、非公共适配被冒充公共模块、实际依赖 stale、编译或公理审计失败。若需要数学报告重跑，交对应作者更新并由根重新绑定；不得编辑旧报告宣称当前。

## 5. 严格构建与实际状态核对

```bash
python reader/build_preview.py
python reader/summarize_status.py
```

正式命令不带 `--allow-incomplete-content` 或 `--allow-incomplete-language`。严格构建检查聚合输入和输出字节、当前实际报告的命令/编译/声明类型/允许公理/传递源码 hash、来源和逐步证据，并生成 `build-manifest.json`、`requested-lean-checks.json`、`lean-bilingual-checks.json`、`status-contract-checks.json`、`source-pages-manifest.json` 及实际 `preview/data.public.json`。

`status-summary.json` 是实际计数，不是数学验收。逐篇比较 `proof_targets` 与冻结库存；人读 proof/scope/counterexample/source-material 和机器 theorem/counterexample/component/none 分开。非目标定义即使有机器定理仍不加进 proof-target 分母，原 17 个 none 不包装为完整 Lean。全部映射证据均须 current，不映射的明示目标保留准确 none。

**停止条件：** 构建例外或非零退出、目标丢失、证据 stale/unavailable、显式角色被状态覆盖、原文转录被误称中文解释、定义/实验条目被称完整证明。构建完成后，后续浏览器期间冻结数据/UI/输入，不能一边修改一边审查。

## 6. 真正服务的全量浏览器、源图及性能

若已有本组 `8004` 服务读取 `reader/preview`，继续使用该服务；否则在另一终端启动下面命令。不要停止用户的 `8001` 服务；不得将服务器启动命令放在后续验收的前台串行链中。

```bash
source scripts/env.sh
python -m http.server 8004 --bind 127.0.0.1 --directory reader/preview
```

在验收终端执行：

```bash
python reader/check_preview.py --base http://127.0.0.1:8004/ --report-name twelve-paper-browser-checks.json --screenshot-prefix twelve
python reader/check_source_presentation.py --base http://127.0.0.1:8004/ --report-name twelve-paper-source-presentation-checks.json
python reader/check_render_environment.py
python reader/check_reading_performance.py --base http://127.0.0.1:8004/ --report-name twelve-paper-reading-performance.json
```

全量浏览器报告须绑定实际 served data/JS/CSS 与本机生成字节、清单、build 输入和检查实现，运行前后不变。分母是实际全部 result 页面、shared 页面、中英文、全部可用作者陈述/证明 tabs、12 篇全部展开符号映射及 14 个 PDF/331 页图。检查所有来源图真实 HTTP 字节与 Chromium 解码；源码问题/反例保持明显可见。中文逐页检查 Lean tab 和本条首个映射步骤的往返，不能据此宣称逐个映射步骤的交互都已浏览。窄屏、搜索、共享入口、符号深链接、语言和返回阅读位置分别验证。

来源展示专项报告核对作者完整转录、项目译述、无独立作者证明的真实 CN/EN 说明，以及非目标定义/实验的“条目说明”标签；有真实 Lean 的非目标定义仍能打开机器证据。此处不使用 `--candidate-ui`，最终测试的就是已构建 UI。

冷缓存渲染只重生成一页真实正式来源，记录项目内 Poppler 依赖/版本及同源解码；其他已核对源图继续复用，不重新生成 331 页制造变化。性能报告是 `measured`，提供首页、最大目录、长证明、全符号表各 5 次本机导航、实际搜索与长页滚动；不是远程性能承诺或数学 pass。比较十篇原记录的符号 58,765 DOM 节点/约 1.04s 等实际瓶颈，将改善留给第二轮，不能靠删字段或隐藏重要问题降低数字。

**停止条件：** 任一实际页面错误、英文未译字段、错标签、JS/KaTeX 错误、溢出、源图失败、语言/返回状态丢失、served 字节不符或运行期间输入变化。浏览器需要本机 Chromium 启动权限时使用既有批准的本机浏览器执行方式，不把 sandbox 启动失败写成数学失败。失败保留报告；修复后按受影响范围复测，输入/数据普遍改变则重新完整矩阵。

## 7. 回归和公开发布边界

```bash
pytest -q
```

最终冻结快照跑一次项目现有完整回归，涵盖库存真实负例、控制字符、双语保护、保全、角色独立、来源/池隔离、公共 direct import、网页与性能行为。记录实际测试总数、命令退出码、日志及全部测试/被测实现 hash；不预设历史的 62 或 70 为最终总数，不新增仅复制实现的镜像测试。新增变化、失败或未解决问题才扩大/重复验证。

以下两步由根执行。现有发布脚本会读取项目内私池隔离种子，整合代理的禁读私稿约束仍适用；根只提供路径分类/计数/问题结论报告，不导出私稿元数据或正文。

```bash
python scripts/check-publication.py --worktree --report reader/evidence/twelve-paper-20261001/root-twelve-publication-worktree.json
```

根用项目内临时 `GIT_INDEX_FILE` 构造完整候选快照，确认真实主 index 前后字节不变。下面只检查根已准备好的临时候选 index，不进行主 index staging、commit 或 push：

```bash
GIT_INDEX_FILE="$PWD/.tmp/twelve-publication-index" python scripts/check-publication.py --report reader/evidence/twelve-paper-20261001/root-twelve-publication-candidate-index.json
```

**停止条件：** forbidden 非空、检查异常、review warnings 未逐项核销，候选 index 包含项目环境、缓存、临时内容、私池/未发表来源、本机上传脚本、production-baseline，或真实主 index 字节改变。退出码为零只表示没有 forbidden，不能替代 warnings 审查。已知 synthetic negative-fixture 的隔离代码引用可由根核实后记录例外，不能按数量机械放行。报告明确 `candidate-index` 范围，不称主 index 已准备发布；后续获新上传指令后仍需检查真正发布的 index。

## 8. 当前性闭合、最终报告与提交

执行完毕再检查 `final-input-freeze.json`、`build-manifest.json` 和各报告的所有输入 hash/前后 snapshot 是否仍与当前文件相符，实际数据/JS/CSS 必须与浏览器报告同一快照。最终整合报告写 `twelve-paper-integration.json`，分开列实际 source occurrences、inventory entries、results、proof targets、unique shared、符号、Lean 报告声明及去重声明；列出逐目标数学/机器角色、17 个保全 none、各软件检查命令/退出码/报告 hash 与范围。根的来源/数学准入、互审及实际 `root-review-requirements.json` 台账逐项核销独立引用，不预设要求条数，软件通过不自动关闭数学要求。

任何后续数学输入、报告、UI、检查实现或文档变化均须按依赖重新绑定和运行受影响检查；普遍数据变化重新完整浏览器，绝不在最终报告引用旧 hash 却称当前。八篇/十篇和首次失败只作历史与修复证据。

根确认全部门通过后先更新记录文档与第二阶段计划，再与用户讨论 GitHub 配置。本轮不推送，也不启动第二轮实现。后续提交/推送须按用户新的明确指令执行并记录真实提交 SHA、远端 SHA 和结果；不能宣称 GitHub 已发布，不读取或复用旧 token。第二轮仍须根明确阶段切换，不能因本操作单的执行提前改布局或十二篇规范正文。
