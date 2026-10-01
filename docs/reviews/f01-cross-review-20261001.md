# F01 独立交叉数学复核（2026-10-01）

审阅者：twelve_dynamics_math。范围为 root 指定的三个核心目标；未替代全篇根审。对照正式 supplement B.1–B.3（PDF3–5）、H（PDF9–10）、content 人读步骤、RobustnessFinite 实际证明代码与最新80声明报告。该报告 passed，传递公理仅为指定白名单；本轮独立检查其输入哈希与实际类型，不把声明计数当作原论文完成数。

数学结论通过。归因递推的合法区间是 i∈N、0≤m≤n−2。令R=N\{i}、q=|R|：插入带标记上下文计数为(m+1)·C(q,m+1)，删除同一标记计数为(q−m)·C(q,m)，均等于q·C(q−1,m)。Lean的sum_insert_flags用真正插入/擦除双射，sum_erase_contexts重排合法j∉S的标记，context_average_step从这些等式推导实际powersetCard平均并证明全部分母非零。attribution_recurrence再将两次边际之差识别为pairDelta。没有先假设待证递推，也没有对界外空均值使用概率解释。

交互效率的权重严格等于原(n−1−m)/(n(n−1))，外和按有序不同变量对i≠j；因此没有额外1/2。实际interaction_efficiency保留g(empty)，只在n≥2的有定义范围陈述。order_sum_accumulation的三角求和使第m阶出现n−1−m次，factorial Shapley效率给外1/n，平均其他变量给1/(n−1)。重写与原B.1(5)的公式一致，不默认b=0。

dropout反例完整保留固定k、floor和原(1−alpha)。正式H定义k=floor((1−alpha)n)，却在Eq14/15后续将k视为未取整(1−alpha)n。n=4、alpha=2/5给k=2；实际uniform powersetCard均值为2，原式cardinalGame右边为12/5。cardinal_game_interaction验证不同变量所有pair差为0，linear_masked_sum_cardinal给全1输入/零输入遮罩的实际线性网络实现。该固定大小模型无Gaussian sigma参数，反例不依赖噪声假设。b=0是所选合法反例的值，不是全局前提。范围正确地只否定原取整子句，不宣称一般改正后的k/n公式已形式化。

须修正一处步骤证据定位：robustness-dropout-expansion中fixed_size_floor_counterexample、fixed_size_cardinal_mean、cardinal_game_interaction当前全部绑定step-3“分开截断机制与错误系数”，而此步主体为一般包含计数。这些实际声明应绑定step-1构造与step-2比较；step-3一般截断计数尚无人读对应的机器证明，不应以这些反例声明充当它的验证。whole-entry counterexample角色及scope本身准确。另step-3效率文本的“phi^(0)(i)(i)”是多余重复(i)，宜删除。以上不影响三个核心数学结论，但步骤映射须在入站前修正。

复核证据文件为同目录f01-cross-review-evidence-20261001.json，包含本轮所读输入哈希及声明类型。未改F01数学或内容文件。
