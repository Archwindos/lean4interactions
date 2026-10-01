# 正式论文双语阅读器

当前显式输入清单和服务快照均为十二篇正式论文：14份 PDF、331页、355个阅读结果、256个目标、37份公共证明。全部新增数学包已根准入；最终软件与浏览器验收正在收尾。最新要求是先检查、记录和第二阶段计划，再讨论 GitHub 配置；本轮不推送或实施第二阶段。复现见[最终验收顺序](../docs/twelve-paper-validation-runbook-20261001.md)，当前结论见[状态](../docs/STATUS.md)。有限检查工具 `check_admitted_preview.py`/`check_source_labels.py` 的八篇、十篇证据保留历史范围，完整矩阵使用 `check_preview.py`。

活动输入只来自 `corpus/public/reader/input-manifest.json` 的显式正式论文清单；不扫描私稿、inbox或旧corpus根目录。输入新增论文无需编辑构建器。历史研究快照和Lean证据保留原路径与哈希。

```bash
source scripts/env.sh
python reader/aggregate.py
python reader/architecture/build_package.py
python reader/architecture/paper_agent.py validate
python reader/check_bilingual.py
python reader/check_completion.py
python reader/check_symbols.py
python reader/check_inputs.py
python reader/check_preservation.py
node reader/check_math.js
python reader/build_preview.py
python reader/check_render_environment.py
python reader/summarize_status.py
python3 -m http.server 8001 --bind 127.0.0.1 --directory reader/preview
python reader/check_preview.py --base http://127.0.0.1:8001/
```

首页进入显式清单中的论文目录；zh/en语言切换持久化并翻译证明正文、条件、定义和共享正文。原文标签、独立公式、步骤ID和Lean机器映射不变。英语覆盖测试与正文中的内联公式差异报告分开保存；字符串差异不自动判定数学不等价。

当前扩篇验收证据单独写入 `reader/evidence/twelve-paper-20261001/`，保留此前六篇最终报告。构建先验证聚合报告绑定的全部来源和实现输入，再确认聚合输出字节匹配；输入改变后须重新运行聚合。正式源预检核对实际 PDF 页数与元数据/库存的一致性，旧六篇保全检查比较已验收的来源、正文及机器状态，允许仅更新英文展示翻译。当前六篇是已验收基线；新增六篇逐篇完整后才进入活动清单。

读取已发布静态快照只需 Python 3 HTTP 服务与浏览器。重新聚合/构建使用 `scripts/bootstrap.sh` 安装的项目 Python、pypdf 和 Poppler；冷缓存原页图片由 `.conda-env/bin/pdftoppm` 生成。Conda 环境与包缓存均在项目内，已核对图片缓存继续复用。`check_render_environment.py` 仅重新生成一页正式来源，在临时本机同源服务核对字节与 Chromium 解码，并记录真实安装和工具版本；该检查还需下述 README 的 Playwright/Chromium 浏览器验收依赖。

各结果的原文整理、重写、源命题判断、Lean范围、公理审计及用户审阅分别记录。浏览器通过只验证软件展示。新公共模块支持直接导入，AI接口`library`也返回来自每篇独立实际报告的新扩展声明，不把它们冒充统一基础版本。

迁移summary只公开公共文件哈希与对象计数；私稿详细路径与回滚证据在本地`corpus/private/migration/report.json`，整个私池被Git忽略。私稿引用公共证明不复制入私池，也不扩私稿列表/搜索。

正式构建默认拒绝缺失英文或未交付的证明目标。开发调试可显式用 `python reader/build_preview.py --allow-incomplete-content`；仅缺译开发预览还需 `--allow-incomplete-language`。这些预览不构成完成验收。`python reader/check_completion.py` 将完整证明、交付的反例/范围分析与待补目标分开，不将范围分析计为原命题证明。浏览器脚本使用 `source scripts/env.sh` 后的项目 Python（本机浏览器依赖为 Python 3.12），并绑定实际生成的 data、JS、输入清单与脚本 hash。

`verify-lean.sh` 的基础 API 按审计入口 `Harsanyi`、`Papers`、`Consumer/Main` 的实际本包 import 闭包发现声明并绑定源码；基础 `Harsanyi` 当前154条。独立新扩展由 `paper_agent.py library` 返回其公共源路径的真实 `import`、类型与当前 report；模块条件和论文应用边界见[API 阅读入口](../docs/library-api.md)。实际组合消费见[ExtensionConsumer](../examples/library-consumer/ExtensionConsumer.lean)。新模块不在基础 barrel，不能仅以基础审计宣称已验证。
