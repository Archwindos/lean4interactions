# 手动投入未发表论文

将一篇论文的 PDF、TeX、Markdown 或纯文本放入 `inbox/<folder>/`；附录、图片和其他附件可放在同一目录或子目录。可将 `templates/paper-metadata.yaml` 复制为该目录中的 `metadata.yaml` 并填写。没有 DOI、URL、作者或正式题名也能导入。

```bash
scripts/archive inbox
scripts/archive extract <paper_id> --version <version>
scripts/archive build
```

也可用 `scripts/archive ingest inbox/<folder>` 导入一个批次。默认 `unpublished` 和 `private`，材料只在本地处理，原文件保留。导入结果提供 `paper_id` 和 `version`。请勿将整个项目或工具/缓存目录作为输入，不允许符号链接或越界路径。

来源副本保存到 `corpus/papers/<paper_id>/<version>/sources/`。同一批次重复导入返回已有版本；来源内容改变时产生新版本。若已有来源只需补充题名/作者，用 `scripts/archive update-metadata <paper_id> --title '题名' --author '作者'`，历史元数据保留在该版本的 `metadata-history/`。更改 inbox 的元数据后重新导入遇到冲突会明确报错，不会静默丢弃修改。

自动提取仅生成候选，未核对时不意味着证明完整、命题正确或 Lean 已验证。数学问题应记录后等待用户确认与单独修订授权，不自动修正文稿。

本地网页默认可以查看私稿。公开导出必须显式使用 `scripts/archive export --public`，它按元数据和来源关系过滤；更改为 public 表示后续显式公开导出可包含该内容。
