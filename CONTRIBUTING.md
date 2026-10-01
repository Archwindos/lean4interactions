# 贡献说明

先读 [AGENTS.md](AGENTS.md) 和[当前状态](docs/STATUS.md)。本轮授权整理十二篇正式论文，活动收录以 [input-manifest.json](corpus/public/reader/input-manifest.json) 为准；开发包不因源码、页面或编译存在就算完成。首轮严格验收与后续符号、共享证明、阅读流程更新按[阶段契约](docs/twelve-paper-release-20261001.md)分别进行。

## 环境与文件边界

从仓库根目录运行 `source scripts/env.sh`。Python/Conda、Lean、依赖、缓存和临时文件分别放在 `.conda-env/`、`.tools/`、`.cache/`、`.tmp/`，不修改系统安装或 shell 配置。保留原始材料和历史证据；多代理工作先确认文件所有权，公共字段变更同步数据作者。

未发表材料使用本地 `inbox/` 和 `corpus/private/`。公共构建和查询不读取这些目录，私稿可以引用独立公共库。取得正式发表版本后按明确授权另建正式来源，不把改 visibility 当作迁移或发布。

## 增加正式论文

1. 核实正式全文与补充材料，保存原件、正式链接、版本、实际 PDF 页数及 SHA-256。
2. 逐页建立全部数学目标与非目标清单。新条目须显式 `proof_target`；非目标有实际分类理由。外引命题、错误命题、未编号推导和未完成目标保留分母。每个条目唯一映射到实际结果，跨 ID 合并明确登记。
3. 转录作者完整陈述、假设、prose 和 TeX 推导，核对原页。作者错式及近似号保留，项目评论、翻译和修正证明分别保存。
4. 对齐原符号、量词、作用域、空集与基线，给出规范中英完整证明及局部定义。当前授权可修同一原命题的证明，禁止改变原假设和结论；命题错误单列反例及影响关系。
5. 检索当前公共 API 的完整类型和前提，导入公共模块并写本论文定义转换，实际编译与审计。通用证明留在公共库，论文专属适配留在应用目录；共享正文单存并按真实 ID 引用。
6. 分别登记原文、完整重写、命题判断、数学审阅、Lean 证据角色和用户审阅。独立核对全部来源与目标，再将完整包显式接入 manifest。保留旧 ID、来源、正文和机器证据。

字段、稳定枚举和入站映射见[数据模型](docs/paper-agent-data-model.md)；完整工作流见[增加论文](docs/add-paper.md)和[扩展流程](docs/agent-extension-workflow.md)。开发包可用 `reader/check_draft_admission.py` 预检接口，不替代数学或来源审查。本轮冻结、全量检查、当前性闭合与准确公开提交边界见[十二篇验收操作单](docs/twelve-paper-validation-runbook-20261001.md)。

## 公共库与验证

新公共模块直接导入 `Harsanyi.Extensions.<Module>`，以独立实际报告导出签名、公理和完整本地 import 闭包。不要为了导出新模块改动旧 barrel；基础入口确有变更时才重验基础目录。库的前提与论文的适配范围必须分别说明。可执行的新证明例子见[独立消费文件](examples/library-consumer/ExtensionConsumer.lean)和[AI 使用库](docs/ai-use-library.md)。

```bash
source scripts/env.sh
python reader/check_inputs.py
python reader/aggregate.py
python reader/architecture/build_package.py
python reader/check_completion.py
python reader/check_bilingual.py
python reader/check_symbols.py
python reader/architecture/check_api.py
python reader/check_library_consumer.py
node reader/check_math.js
python reader/build_preview.py
```

公式检查及真实浏览器命令、依赖和报告位置见 [reader/README.md](reader/README.md)。报告绑定实际输入和脚本哈希，源码或输入变化后重新检查；编译、软件、双语和浏览器通过不等于作者全命题已证明。选择能检出实际错误的回归，不增加只复述实现的测试。

公开提交前运行 `python scripts/check-publication.py --worktree`；准备好准确暂存区后运行 `python scripts/check-publication.py` 并人工核对 index。未发表原件、派生证明和报告、环境、缓存、凭据及本机上传脚本不进入公开提交。提交和推送状态按实际结果报告，认证未就绪时继续独立验收。
