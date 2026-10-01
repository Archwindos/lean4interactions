# 第二轮接续要点

本文件只交接，未启动第二轮实现。下一轮采用用户指定的 gpt-6.1-sol / high；第一轮数学、来源与实际编译证据保留。

- F01：corpus/public/reader/neurips2021-robustness/；公共数学为 lean/HarsanyiLib/Harsanyi/Extensions/RobustnessFinite.lean。固定样本游戏 g_x(S)=v(x_S) 与分布熵游戏 H_Y(S)=E[H(P(Y|X_S))] 分开；原输出基线保留。经典 Shapley 适配可连现有 dividend 共享证明，配对交互线性不可仅因同名与单个 Harsanyi dividend 合并。
- F04：corpus/public/reader/icml2022-transformation/；最终两个 release 连接已由 dynamics 接手完成，该目录不再归本代理改写。公共依赖为 TransformationEntropy/Gates/Refinement/Affine/EBM 等独立扩展。共享归并需保留任意输入空间的有限标签/门推前律、零支持约定与实际算子连接。原作者已有 sigmoid 连续松弛，不可重新登记成“没有连续延拓”。
- F06：corpus/public/reader/icml2023-decoder/；18 个 Decoder*.lean 公共模块及 lean/PaperDecoder.lean。频谱 g^(uv) 与 coalition 游戏无关；输出 DFT 负相位、核响应正相位、全部空间偏置及 MN 保留。Eq31/32 的强模型 hrow/hprefix 不可在归并中丢失，也不能从原弱一阶显示式自动推出。有限几何和是全域定义，商域、valid 项数及一步反例须保留各自问题范围。
- 真正可复用的 Gaussian 矩与独立乘积已经依赖 dynamics 的 ConceptGaussian/TaylorMoments。第二轮可归并公共证明正文；修改公共源码后须重跑全部受影响的真实报告，不能只重绑哈希。
- 已独立互审 F07/F08/F10，报告在 docs/reviews/f07-cross-review-20261001.md、f08-cross-review-20261001.md、f10-cross-review-20261001.md。三篇文件仍归 dynamics；原始/优化游戏、最低阶有符号 I 与绝对 J、回归真实期望 loss 的区别不可合并消除。

界面第二轮优先精简工程词与重复正文，并显示实际 theorem/counterexample/partial/none 的精确范围。原作者英文、项目注、规范重写及机器声明继续分栏；中文英文不改公式、ID、声明或来源定位。
