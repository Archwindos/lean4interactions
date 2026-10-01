# 正式版证明阅读原型

状态：待确认方案。正式站点、权威 corpus 与 Lean 源码没有修改。

运行入口：<http://127.0.0.1:8001/>；推荐先看 `?case=reconstruction`、`?case=shapley`、`?case=reference`。独立原型服务仅绑定 `127.0.0.1`；根代理已重启并核验页面返回 HTTP 200。服务退出后可按下方命令重启。

仅用 CVPR 2023 官方 CVF 公开正文（10 页）与官方补充材料（27 页）作正式示例。Theorem 1 的数学核心与既有公共重构、唯一性结果已对照；中文证明来自已有权威文件，没有产生新数学证明。完整正式版目录、正式版 corpus 迁移与其余重写仍未完成。正式源原文以 PDF 为准。

原文面板的辅助 TeX 来自 arXiv:2111.06206v6，清楚标明这一来源及与正式材料对照的范围；它不是 CVPR 作者源码，引用和公式编号保留辅助来源的编号。原样显示与复制逐字保留辅助 TeX。旧版 18 条候选与 Dummy 记录只存于历史审计，未计入正式目录；旧直达链接显示“旧版审计入口”。

入口与材料：

- [完整方案](../../docs/redesign-20260930.md)
- [本地 HTML](preview/index.html)
- [正式版源与对照](evidence/formal-edition-audit.json)
- [投诉页面审计](evidence/display-audit.json)
- [浏览器核验](evidence/browser-checks.json)
- [产物冻结清单](evidence/frozen-manifest.json)

最终检查：Chromium 153，77 项通过、9 张截图，1440×1050 与 390×844。辅助 TeX DOM/复制逐字一致，步骤到声明与返回、未完成状态、旧直达链接与窄屏目录实际操作。无页面 JavaScript 错误、数学渲染错误、外部请求或页面横向溢出；719 个生产/corpus/Lean 文件哈希未改变。这里只复核已有 Lean 报告指纹，没有运行新构建。

服务器只提供 `preview/`。`evidence/` 与 `browser-tools/` 未提供 HTTP 访问，不可将整个 research 目录当作发布目录。私稿不在原型中。

需要重启时，从项目根目录运行：

```bash
source scripts/env.sh
python -m http.server 8001 --bind 127.0.0.1 \
  --directory research/reader-redesign-20260930/preview
```

复现数据快照：

```bash
source scripts/env.sh
python research/reader-redesign-20260930/build_preview.py
```

原型只整理已有内容，尚未把提议的数据契约、提取修复和展示调整应用到生产系统。
