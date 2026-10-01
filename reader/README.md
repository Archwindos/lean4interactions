# 当前六篇双语阅读器

活动输入只来自 `corpus/public/reader/input-manifest.json` 的显式正式论文清单；不扫描私稿、inbox或旧corpus根目录。输入新增论文无需编辑构建器。历史研究快照和Lean证据保留原路径与哈希。

```bash
source scripts/env.sh
python reader/aggregate.py
python reader/architecture/build_package.py
python reader/architecture/paper_agent.py validate
python reader/check_bilingual.py
python reader/check_completion.py
python reader/check_symbols.py
node reader/check_math.js
python reader/build_preview.py
python reader/summarize_status.py
python3 -m http.server 8001 --bind 127.0.0.1 --directory reader/preview
python reader/check_preview.py --base http://127.0.0.1:8001/
```

首页进入六篇目录；zh/en语言切换持久化并翻译证明正文、条件、定义和共享正文。原文标签、独立公式、步骤ID和Lean机器映射不变。英语覆盖测试与正文中的内联公式差异报告分开保存；字符串差异不自动判定数学不等价。

各结果的原文整理、重写、源命题判断、Lean范围、公理审计及用户审阅分别记录。浏览器通过只验证软件展示。新公共模块支持直接导入，AI接口`library`也返回来自每篇独立实际报告的新扩展声明，不把它们冒充统一基础版本。

迁移summary只公开公共文件哈希与对象计数；私稿详细路径与回滚证据在本地`corpus/private/migration/report.json`，整个私池被Git忽略。私稿引用公共证明不复制入私池，也不扩私稿列表/搜索。

正式构建默认拒绝缺失英文或未交付的证明目标。开发调试可显式用 `python reader/build_preview.py --allow-incomplete-content`；仅缺译开发预览还需 `--allow-incomplete-language`。这些预览不构成完成验收。`python reader/check_completion.py` 将完整证明、交付的反例/范围分析与待补目标分开，不将范围分析计为原命题证明。浏览器脚本使用 `source scripts/env.sh` 后的项目 Python（本机浏览器依赖为 Python 3.12），并绑定实际生成的 data、JS、输入清单与脚本 hash。

`verify-lean.sh` 的基础 API 按审计入口 `Harsanyi`、`Papers`、`Consumer/Main` 的实际本包 import 闭包发现声明并绑定源码；基础 `Harsanyi` 当前154条。独立新扩展应直接导入 `Harsanyi.Extensions.HarsanyiNetwork`、`Harsanyi.Extensions.LayerwiseKnowledge` 或 `Harsanyi.Extensions.CoalitionAttribution`，并查看各篇当前真实 report。新模块不在基础 barrel，不能仅以基础审计宣称已验证。
