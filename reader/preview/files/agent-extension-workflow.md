# 增加正式论文与扩展可复用库

当前六篇活动范围覆盖正文、附录及 CVPR 正式补充材料的全部登记目标。此前 v2 选定结果的范围已被全篇授权取代，历史输入和报告仍保留。当前实现入口是 `reader/`，活动输入是 `corpus/public/reader/`。旧研究目录与Lean源码/报告作为历史只读证据保留。

1. 确认论文范围，取得可核实的会议或期刊正式全文及补充材料。为论文、版本和源文件建立稳定 ID，记录正式链接、页数及 SHA-256。预印本只作发现线索，私稿保持本地和私有，不进入公开构建。
2. 逐页核查全部来源。登记定理、引理、性质、未编号推导、外引未证、定义、算法和经验条目；保留每次出现的编号、别名及证明范围。目录覆盖数与独立证明数分开。
3. 精确保存原陈述及作者全部数学推导，使用可渲染 TeX；中文连接文字注明项目翻译。PDF 页图及文字抽取作核对证据，整页抽取或摘要不能冒充证明全文。原錯式保留。
4. 对齐量词、定义域、有限总体、空集与基线，再写完整中文证明。已有授权范围获 `proof_only_granted`，可以直接修正同一命题的证明并标原错处；原假设和结论不能修改。命题错误单列反例。范围外材料依其具体授权处理。
5. 先查公共符号和共享证明。论文结果只保存自己的定义映射和适配，完整公共正文单存；完全一致的步骤按 ID 和内容建立引用。相似题名仅产生候选关联，不自动共享状态。
6. 在分工独立源码中编写真实 Lean 适配。需要新通用结果时扩展公共库，不复制环境。保留经典定义到交互公式的连接，不能只证明小例子、假设结论或改变原命题来通过。为每个文字步骤填写真实 `lean_refs`。
7. 编译与公理审计，保存命令、退出码、实际类型、源码位置、工具链与源指纹。论文适配报告和公共库报告的范围分开；根代理在源码冻结后运行 `scripts/verify-lean.sh`，生成当前 `catalog/library.json`。用途描述可提供真实示例，未提供时留空。
8. 运行聚合与构建，再检查全目录、原文、正文、符号、来源、问题和 Lean 对照。浏览器报告绑定本次数据、构建清单与脚本哈希；这些软件检查不代替独立数学交叉审阅。新预览仅服务其 `preview/`，保留已有论文 URL。

```bash
source scripts/env.sh
python reader/aggregate.py
python reader/architecture/paper_agent.py validate
python reader/build_preview.py
python reader/check_preview.py --base http://127.0.0.1:8001/
```

只读查询接口及字段见 `docs/paper-agent-data-model.md`。网页的完整说明、原命题判断、语义对齐、用户审核、实际编译及证据角色分别保存；不得用单一“完成”字段替代。原件及 `research/reader-v2-20260930/` 历史证据不可覆写。

新增正式论文无需修改聚合器白名单：在 `corpus/public/reader/input-manifest.json` 的 `papers` 增加一条显式配置，并提供对应文件。`metadata_path` 使用现有论文的 `paper-metadata.json` 格式，所有论文和来源都必须是 `public/published`，来源须有实际路径、SHA-256、版本及页数；未配置文件不会自动扫描。配置示例：

```json
{
  "paper_id": "new-formal-paper",
  "metadata_path": "corpus/public/reader/new-formal-paper/paper-metadata.json",
  "inventory_path": "corpus/public/reader/new-formal-paper/inventory.json",
  "content_path": "corpus/public/reader/new-formal-paper/content.json",
  "symbols_path": "corpus/public/reader/new-formal-paper/symbols.json",
  "issues_path": "corpus/public/reader/new-formal-paper/issues.json"
}
```

当前配置含六篇正式论文；构建器不硬编码篇数，新增论文只修改显式manifest并提供数据。该轮确切六篇集合由验收测试核对。论文标题查询可用 `paper_agent.py paper-search 'Generalizable'`；`search` 返回命题/推导结果及原编号别名。

元数据顶层使用 `id` 作为论文ID；每个 `sources` 项使用 `id`、`label`、`kind`、`local_path`、`sha256`、`total_pages`、`visibility`、`publication_status`。文件路径是项目内 `corpus/public/reader/<paper_id>/` 的正式源相对路径，不能以旧私稿或legacy corpus路径代替。清单的 `statement_location`、`proof_location` 和每次 `appearances` 均携带实际 `source_id` 与文件内页码。先运行 `python reader/check_inputs.py` 检查元数据、路径、哈希和逐页台账，再做聚合；内容尚未完成时也可先运行这项来源预检。

未发表稿件应置于 `inbox/<paper>/`，保持 `unpublished/private`，通过本地 archive 流程处理；不要为了接入公开阅读器人为改成 `public/published`。取得正式版本及相应授权后，另建正式源实体与明确公开配置，原私有材料仍保留。


每个result/shared_proof使用 `translations.en` 覆写人读字段，或在 `corpus/public/translations/` 提供英文sidecar。步骤ID、独立公式、Lean声明/路径/行号/签名/报告与状态字段禁止改变；`lean_refs.explanation_md` 可以翻译而机器字段保持。`reader/bilingual.py` 检查证明标题、overview、假设、定义、scope、每步正文与依据、适配与共享正文。内联TeX的文字差异单独报告供数学语义审查，不自动判等价。运行 `python reader/check_bilingual.py` 后再发布。

private池独立提供papers、claims、theorems、issues、reviews与relations；列表和搜索只在选定池活动，private可以单向引用公共theorem/proof。手动导入默认private/unpublished。跨池visibility修订会被拒绝；显式promote只导入另行核查的正式原件，不自动公开私稿证明或评审。旧corpus根层目录是ignored legacy，不能重新当作活动输入。

正式构建默认拒绝缺译/未交付证明目标；开发预览的 `--allow-incomplete-content` / `--allow-incomplete-language` 必须显式声明，不能据其称已验收。issue 英文可置于 sidecar 顶层 `issues:{id:{title,text_md,evidence_md,problem_md,analysis_md,impact_md}}`，原式、分类、授权与状态继承。Lean 对象的 `translations.en` 仅容许展示说明字段（scope/label/encoding_note/statement_md 及逐步说明），其机器字段不改。基础 verify-lean 按实际入口 import 闭包验证，新增独立模块需 direct import 及真实单独报告。

新增论文的英文 Lean 说明应放在数据的 `lean.translations.en` 中（`scope`、`encoding_note`、`statement_md`），逐步说明优先从 `translations.en.proof_steps[id].lean_refs` 按同一 `declaration` 取得英文 `explanation_md`，或在对应 step_map 记录提供只含人读字段的 `translations.en`。机器映射必须相同，不能翻译状态、声明、签名或路径；状态标签按实际当前验证结果生成。`reader/lean_english.py` 的旧句子字典仅为历史资料迁移后备，新论文无需编辑此全局字典。
