# F06 第一轮终包自审

正式文件为 ICML 2023《Defects of Convolutional Decoder Networks in Frequency Representation》，正文与附录合在同一 34 页 PDF，SHA256 为 25cf5804c4d93cc1117adf2afb9ad84c96ccb86cba14cc5be3a11d3c420aeb57。活动包在 corpus/public/reader/icml2023-decoder/。最终逐文件哈希与角色列表见同名 JSON；全局 reader manifest 由整合代理负责，本代理未修改。

34 页逐页清单闭合，包括参考文献、经验结果和非证明页。独立来源出现表的 51 个出现均显式映射，A.7 原宽条目另精确拆出所选频率更新，合计 52 个出现、34 个阅读入口、30 个数学目标、4 个非目标。原作者正文陈述、A.1–A.7、B.1–B.4 和 C.6/C.7 未编号推理分别完整保留；同一作者重复公式通过出现映射归并，没有复制计数为新定理。来源支持包的项目注保留在独立 notes，不占 original 字段。

18 个公共 Decoder 模块和 PaperDecoder 六个声明实际编译。报告记录 296 个实际 Lean 常量类型、依赖和传递公理；声明数包括定义与辅助引理，并不等于论文目标数。全部公理均限于 propext、Classical.choice、Quot.sound，未用 sorry。报告的 33 个来源哈希在最终预检保持新鲜。两项关键纸面适配将真实 loss/状态/导数与完整前后缀更新绑定，并将真实 Gaussian 矩阵级联接到 Eq31/32；一般正矩因子 log wrapper 覆盖零方差但非零均值响应，不把正方差充分条件冒充唯一范围。

七个目标有精确可编译定理证据，六个目标有真实模型反例证据，八个目标有明确分量证据。它们与原命题评估分开：例如多通道闭式完整实现于明确的强独立模型，但 hrow/hprefix 没有由原弱一阶显示式推出；因此页面仍显示条件性分量。原普通正弦商的零域、valid 分子项数、实际核参数、独立 Gaussian 深度、相关像素 padding 和真实两层一步更新的问题均独立登记，正确 DFT 传播没有因错误子句而被整体否定。

九个目标没有单独 Lean 证据：移位设置的幅值解释是人读反例；其它频率全程固定系数及消约有缺口；padding、upsampling、拟合难度、自然图像和层位置条目主要评估从已收录算子恒等式或矩推断训练行为的范围；高维 cosine 与低 Pearson 推断独立性的未量化论证保留完整作者链及具体人读反例。它们均没有标成机器证明，也没有用添加前提的方法声称原目标成立。相应精确算子/矩/真实一步反例已有独立可查询目标，不把这些未量化解释改造为作者未陈述的新概率定理。

最终本地 source/page/目标分母/真实报告新鲜度/双语/内容完成度预检通过。严格双语缺项为零，步骤 TeX 差异为零。实际 KaTeX 共渲染 2710 个公式出现，零错误；此数包含原文与双语重复出现，不代表数学目标数。独立源审由整合代理完成，根代理独立核读主干与反例，dynamics 独立复核全 34 条和关键实际类型。

复现命令均在项目根目录、login:false 环境先 source scripts/env.sh：

    python corpus/public/reader/icml2023-decoder/build_content.py
    python corpus/public/reader/icml2023-decoder/verify_decoder.py
    python corpus/public/reader/icml2023-decoder/bind_verification.py
    python corpus/public/reader/icml2023-decoder/preflight_decoder.py
    node corpus/public/reader/icml2023-decoder/verify_katex.cjs

build_content 产生未验开发态；只有真实报告通过后 binder 才标记重写完成并绑定实际角色。第一轮尚待根正式准入和提交。第二轮仅交接要点于 twelve-foundations-phase2-handoff-20261001.md，未启动新的 xhigh 实现。


## 第一轮定义域状态纠正

根浏览器检查发现旧 edf8fa8f… 包把两项商式定义域问题显示为“复合陈述中的一部分有反例”。这是过期的元数据判定，已纠正；数学正文、原陈述、原证明、全部Lean源码、296声明报告及33个编译来源均未变化。旧数学、原文和交叉审报告保留原哈希，不冒称这些旧报告重新审查了新标签。

- decoder-backpropagation：statement_assessment从partially_refuted改scope_under_review，rewrite_status从complete改complete_with_original_domain_issue，proof角色保留。中英scope_label明确“有限和解释下完整证明；原正弦商存在未定义频率”。相关错误仅为商定义域与局部错步，不是最终Eq5矩阵命题的反例。
- decoder-geometric-sum：同样更正assessment及domain状态，元角色从partial_proof_with_refuted_clause改partial_component。中英标签明确分母零点的未定义域；有限和和合法商域已证，没有数值子句反例。

其它32项逐一核查并保留：K增长、padding非DC、一步零loss的部分反驳均有真实原模型反例，不能随本补丁删除。两项库存元字段同步；4共享证明、原文、全部人读证明步骤及目标分母完全不变。最终content新SHA e457f5388d581359a8f37e249651f2eeca4320a457b44f49439c3a3fe32cabc3，inventory新SHA 70310d481040c9531680d99f8bfc2d98f7c273edcb7c34302e8a98006e405759；机器报告仍为83716554…、PaperDecoder仍为406ea769…。

逐字段前后差异及34项审核见 verification/status-assessment-correction.json。已同步状态函数与生成器/binder，避免重新生成时回退。元数据补丁后文本预检、严格双语与实际KaTeX重跑通过；双语缺项/公式差异均0，2710式渲染0错。全页面与331张来源图继续引用整合者保存的pre-status-fix稳定快照，随后只差分核对受影响标签和英文展示；没有重编译或伪改先前机器审计报告。
