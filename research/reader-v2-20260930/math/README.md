# 本轮数学交付与实际验证

本轮完成三篇正式论文的四个选定结果：CVPR2023 的重构与 Appendix C 唯一性，ICLR2024 Sparse 的 Theorem 1 去基线重构，ICLR2024 Generalizable 附录 C(1) 固定原样本的 AND 分量子结论。另有一个公共空集/去基线结果页面。完整 F11 Theorem 2 单列未开始重写、未形式化，不能由其 AND 子结论的完成状态覆盖。

共同输入是 [math-content.json](../data/math-content.json)。其中两个完整公共证明单独存于 `shared_proofs`，论文各自对齐定义与条件，再引用并直接展示公共全文。中文 Markdown 与 JSON 从 [build-math-content.py](build-math-content.py) 同一输入生成；关键行内记号与展示命题均用 TeX，手机命题另有作者指定的分行，不改机器用完整命题。

正文包括辅助子集拆分、插入交互的基数与符号推导、加强归纳为何对任意函数成立、逆向反演引理、唯一性的全部子集量词与空集边界。小例子原输出为 2、5、7、13，原交互为 2、3、5、3；去基线交互为 0、3、5、3。全部四个掩码的整数计算另有 [numerical-examples.json](numerical-examples.json) 检查。

公开代码：[ReaderAdapters.lean](lean/ReaderAdapters.lean)。本轮没有改既有 `lean/`、`corpus/`、`catalog/` 原件或依赖锁；新增适配使用现有 HarsanyiLib。

实际公开验证：[verification/report.json](verification/report.json)。执行顺序与日志都记录在报告中：读取 Lean 版本；只增量构建 `Harsanyi.Core.Properties` 及其导入；编译公开适配；由 Lean 导出真实签名、依赖与传递公理。9 条适配定义/定理和 10 条实际公共库声明全部通过，公理仅包含 `propext`、`Classical.choice`、`Quot.sound`，没有 `sorryAx`。最终 [final-check.json](final-check.json) 再核当前绑定源码与指纹一致。

复现公开验证须在项目根目录执行：

```bash
source scripts/env.sh
python research/reader-v2-20260930/math/verify-public.py
```

[content-math-check.json](content-math-check.json) 记录 401 条公式经实际 KaTeX 严格检查通过。命题、定义与行内数学的排版检查由 [check-content.js](check-content.js) 执行；排版通过不等于数学语义正确，完整数学链与正式来源另外核对。

来源检查使用四份正式 PDF：CVPR2023 main/supp，ICLR2024 Sparse 与 Generalizable 正式正文及随文附录。`source-review/` 留存页文本定位和八张实际页渲染；只核与本轮选定结果有关的页。原 PDF 不覆写。`original_*_note` 明示原证明字段是项目中文说明/摘要，正式全文以 PDF 为准，不冒充逐字转录。

[issues.json](issues.json) 与 [issues.md](issues.md) 分开保存：一项 F11 OR 原证明中间求和问题（case(3)/(4) 同属该条），以及一项 `x_T`/固定 `x` 的记号语义对齐说明。数学问题有具体正式页、原式、最小局部反例与视觉证据，用户确认和修正授权均 `pending`；最终定理没有被这些局部反例否定。AND 子结论不依赖该 OR 推导。

`experimental/` 只保留已经产生的本地 OR 技术核验材料及单独编译/公理日志，状态 `experimental_not_published`。它不进入普通读者导航或 agent package，不是完整 F11 原证明的替代方案，也不关闭原文问题。

形式化边界与实际文字到代码流程详见 [human-to-lean.md](../../../docs/human-to-lean.md)；证明写作要求见 [proof-writing-standard.md](../../../docs/proof-writing-standard.md)。编译只验证形式陈述，本轮正式来源适配由代理检查，用户审核仍待定。稀疏性、Taylor/高阶导数、近似误差、经典 Shapley 公式等价、具体模型与坐标掩码运行都未被本轮选定适配覆盖。
