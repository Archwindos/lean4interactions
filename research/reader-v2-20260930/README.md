# 多篇正式论文的证明阅读原型

本目录是独立阅读原型，输入仅含 CVPR 2023 Sparse Concepts、ICLR 2024 Sparse Interaction Primitives、ICLR 2024 Generalizable Interaction Primitives 三篇公开正式论文。正式 PDF 由固定文件哈希核对。原文标签提供公式摘录与项目中文说明；正式原文由 PDF 对应页提供，可直接展开阅读。选定公式的 TeX 是项目核对转录，不是作者源码。

读者从论文列表进入某一篇的目录，再打开独立可链接的结果页。中文证明默认全文呈现；原命题、原证明、Lean 对照使用简单标签切换。公共证明数据只存一份，结果页在论文自己的定义与适配之后直接显示完整公共推导。给 AI 与维护者的关系图、只读入口和处理范围另放独立页面。

ICLR 2024 Generalizable 的完成范围是附录 C(1) 固定输入的 AND 子结论。完整 AND/OR Theorem 2 的原文对齐与原证明疑点另列，不能把该子结论的完成状态推广到整个定理。实验 OR 文件没有进入网页快照。

从项目根目录构建：

```bash
source scripts/env.sh
python research/reader-v2-20260930/build_preview.py
```

只提供生成后的 `preview/`，服务默认入口可与旧 demo 相同：

```bash
source scripts/env.sh
python -m http.server 8001 --bind 127.0.0.1 \
  --directory research/reader-v2-20260930/preview
```

浏览器验收临时使用 8002。Playwright Python 安装和 Chromium 复用旧原型的本地工具，不复制或安装大环境：

```bash
source scripts/env.sh
python -m http.server 8002 --bind 127.0.0.1 \
  --directory research/reader-v2-20260930/preview
# 在另一个终端运行：
python research/reader-v2-20260930/check_preview.py \
  --base-url http://127.0.0.1:8002/
```

文件职责：

- `ui/`：页面样式与安全的本地数学渲染器。
- `build_preview.py`：正式来源白名单、多篇论文与结果的独立静态路径、快照和哈希清单。
- `data/papers.json`、`data/math-content.json`：论文元数据、原文对照、完整证明、Lean 对应。
- `math/`：数学代理生成的审校、适配及验证资料；实验目录不会公开。
- `architecture/`：关系数据包和只读查询工具。
- `evidence/`：实际浏览器操作、截图、构建清单和生产文件未改动核验；不随网页提供。
- [设计与验收说明](../../docs/reader-v2.md)。

正式站点、原始论文、权威 corpus 和公共 Lean 库源码未由本 UI 工作改动。三篇论文的全部命题清单、整篇重写与完整形式化仍属后续范围。

最终实际验收：Chromium 153，194 项浏览器检查通过，19 张截图；桌面 1440×1050，手机 390×844。三篇论文、4 个完整重写的论文结果、1 个待对齐的原定理入口、1 个公共中心化结果均有独立路径；另外有 2 个原文核验页。三篇论文切换、分行公式、正式 PDF 原文图、TeX 转录、Lean 双向步骤链接和 F11 问题证据都经过操作。无 JavaScript 错误、公式渲染错误、外部请求或页面横向溢出，719 个生产文件哈希保持不变。9 项状态契约检查另核实候选共享证明不能冒充已重写，以及陈旧来源、失败命令、不允许的公理或缺失声明不能继承 Lean 已编译状态。

验收记录：

- [真实浏览器报告](evidence/browser-checks.json)
- [状态契约与 Lean 证据校验](evidence/status-contract-checks.json)
- [桌面证明中段](evidence/17-common-proof-middle-desktop.png)
- [手机证明中段](evidence/18-common-proof-middle-mobile.png)
- [F11 正式原文证据](evidence/19-generalizable-specific-evidence-desktop.png)
