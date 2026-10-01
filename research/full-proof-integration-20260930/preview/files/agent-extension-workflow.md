# 增加正式论文与扩展可复用库

当前三篇任务覆盖正文、附录及 CVPR 正式补充材料的全部证明目标。此前 v2 选定结果的范围已被全篇授权取代，历史输入和报告仍保留。下面对应当前 `research/full-proof-integration-20260930/` 实现。

1. 确认论文范围，取得可核实的会议或期刊正式全文及补充材料。为论文、版本和源文件建立稳定 ID，记录正式链接、页数及 SHA-256。预印本只作发现线索，私稿保持本地和私有，不进入公开构建。
2. 逐页核查全部来源。登记定理、引理、性质、未编号推导、外引未证、定义、算法和经验条目；保留每次出现的编号、别名及证明范围。目录覆盖数与独立证明数分开。
3. 精确保存原陈述及作者全部数学推导，使用可渲染 TeX；中文连接文字注明项目翻译。PDF 页图及文字抽取作核对证据，整页抽取或摘要不能冒充证明全文。原錯式保留。
4. 对齐量词、定义域、有限总体、空集与基线，再写完整中文证明。当前三篇获 `proof_only_granted`，可以直接修正同一命题的证明并标原错处；原假设和结论不能修改。命题错误单列反例。范围外材料依其具体授权处理。
5. 先查公共符号和共享证明。论文结果只保存自己的定义映射和适配，完整公共正文单存；完全一致的步骤按 ID 和内容建立引用。相似题名仅产生候选关联，不自动共享状态。
6. 在分工独立源码中编写真实 Lean 适配。需要新通用结果时扩展公共库，不复制环境。保留经典定义到交互公式的连接，不能只证明小例子、假设结论或改变原命题来通过。为每个文字步骤填写真实 `lean_refs`。
7. 编译与公理审计，保存命令、退出码、实际类型、源码位置、工具链与源指纹。论文适配报告和公共库报告的范围分开；根代理在源码冻结后运行 `scripts/verify-lean.sh`，生成当前 `catalog/library.json`。用途描述可提供真实示例，未提供时留空。
8. 运行聚合与构建，再检查全目录、原文、正文、符号、来源、问题和 Lean 对照。浏览器报告绑定本次数据、构建清单与脚本哈希；这些软件检查不代替独立数学交叉审阅。新预览仅服务其 `preview/`，验收后接回已有三篇论文 URL。

```bash
source scripts/env.sh
python research/full-proof-integration-20260930/iclr2024-generalizable/build_content.py
python research/full-proof-integration-20260930/aggregate.py
python research/full-proof-integration-20260930/architecture/paper_agent.py validate
python research/full-proof-integration-20260930/build_preview.py
python research/full-proof-integration-20260930/check_preview.py --base http://127.0.0.1:8003/
```

只读查询接口及字段见 `docs/paper-agent-data-model.md`。网页的完整说明、原命题判断、语义对齐、用户审核、实际编译及证据角色分别保存；不得用单一“完成”字段替代。原件及 `research/reader-v2-20260930/` 历史证据不可覆写。

新增正式论文无需修改聚合器白名单：在 `research/full-proof-integration-20260930/input-manifest.json` 的 `papers` 增加一条显式配置，并提供对应文件。`metadata_path` 使用现有论文的 `paper-metadata.json` 格式，所有论文和来源都必须是 `public/published`，来源须有实际路径、SHA-256、版本及页数；未配置文件不会自动扫描。配置示例：

```json
{
  "paper_id": "new-formal-paper",
  "metadata_path": "research/full-proof-integration-20260930/new-paper/paper-metadata.json",
  "inventory_path": "research/full-proof-integration-20260930/new-paper/inventory.json",
  "content_path": "research/full-proof-integration-20260930/new-paper/content.json",
  "symbols_path": "research/full-proof-integration-20260930/new-paper/symbols.json",
  "issues_path": "research/full-proof-integration-20260930/new-paper/issues.json"
}
```

当前配置仅包含三篇已授权正式论文。论文标题查询可用 `paper_agent.py paper-search 'Generalizable'`；`search` 返回命题/推导结果及原编号别名。

未发表稿件应置于 `inbox/<paper>/`，保持 `unpublished/private`，通过本地 archive 流程处理；不要为了接入公开阅读器人为改成 `public/published`。取得正式版本及相应授权后，另建正式源实体与明确公开配置，原私有材料仍保留。
