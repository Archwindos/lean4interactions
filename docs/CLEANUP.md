# 旧生成文件清理（2026-10-01）

按用户“老文件清理掉”“验收图片也不需要”的授权，删除旧阅读原型整站、验收截图、旧原页审阅渲染图，以及重复的 PDF 原页图像缓存。没有删除论文 PDF 原件。

`reader/preview/` 当前十二篇阅读站点全部保留，包括页面实际使用的 `files/source-pages/` 原页图像。`start.sh` / `start.bat` 仍直接打开此快照，无须重建。

## 回收记录

下表以删除前普通文件的精确字节数统计，不含目录占用。共删除 **1218 个文件，252,427,532 字节（240.73 MiB）**。

| 已删除路径范围 | 文件数 | 字节数 |
| --- | ---: | ---: |
| `reader/evidence/*.png` | 16 | 2,084,275 |
| `reader/evidence/source-pages/*.png` | 162 | 45,888,129 |
| `reader/evidence/twelve-paper-20261001/*.png` | 66 | 9,872,423 |
| `reader/evidence/twelve-paper-20261001/source-pages/*.png` | 169 | 45,210,126 |
| `research/full-proof-integration-20260930/cvpr2023/source-evidence/*.png` | 8 | 951,399 |
| `research/full-proof-integration-20260930/evidence/*.png` | 13 | 1,618,771 |
| `research/full-proof-integration-20260930/evidence/source-pages/*.png` | 94 | 25,723,125 |
| `research/full-proof-integration-20260930/iclr2024-generalizable/source-review/*.png` | 6 | 1,888,813 |
| `research/full-proof-integration-20260930/iclr2024-sparse/evidence/pages/*.png` | 34 | 10,392,982 |
| `research/full-proof-integration-20260930/iclr2024-sparse/review-evidence/*.png` | 2 | 592,271 |
| `research/full-proof-integration-20260930/preview/` | 373 | 55,994,522 |
| `research/full-proof-integration-20260930/root-audit/*.png` | 9 | 1,290,692 |
| `research/reader-redesign-20260930/evidence/*.png` | 14 | 4,146,830 |
| `research/reader-redesign-20260930/evidence/legacy-arxiv/*.png` | 9 | 1,686,589 |
| `research/reader-redesign-20260930/preview/` | 82 | 10,089,789 |
| `research/reader-v2-20260930/data/source-excerpts/*.png` | 3 | 861,836 |
| `research/reader-v2-20260930/evidence/*.png` | 19 | 2,314,263 |
| `research/reader-v2-20260930/evidence/source-pages/*.png` | 12 | 3,723,063 |
| `research/reader-v2-20260930/math/source-review/*.png` | 8 | 3,600,557 |
| `research/reader-v2-20260930/preview/` | 119 | 24,497,077 |

逐文件路径、删除前大小与 SHA-256 的本机台账为 `.tmp/old-generated-files-cleanup-result.json`（忽略上传）；表内字节数可直接求和复算。

## 保留与重建

- 保留 `research/` 中仍被当前输入或 Lean 报告指纹引用的源码、正式来源 PDF、文字稿、证明、适配、历史 verification 报告和日志；保留论文候选 metadata。
- 保留 evidence 中的 JSON 与文字报告。报告里的旧截图路径和旧审阅图路径仅是历史记录，清理后不再代表随仓库提供的图片。
- 图像缓存来自保留的正式 PDF；`reader/build_preview.py` 检查文件存在及 hash，缺失时通过 `pdftoppm` 自动重建。日常启动无需运行构建器。
- 当前原页展示使用 `source.page_images` 中的发布路径；旧 `image_path` / `image_paths` 审阅元数据不作为产品页面图片请求。
- 旧原型 `research/*/preview/` 已移除，历史说明、代码和验收文字仍保留；查看项目使用当前 `reader/preview/`。
- 环境、工具、本机缓存、私稿、用户原件和 Git index 未由清理脚本修改。

生成媒体的忽略规则已追加到 `.gitignore`，防止重建后再次纳入待上传集合。

清理后按删除前 SHA-256 核对：当前预览 1,071 个文件、活动来源与证明材料 224 个文件全部未变；清单中 1,218 个文件全部已删除。HEAD 与 Git index 在清理实施期间未变。
