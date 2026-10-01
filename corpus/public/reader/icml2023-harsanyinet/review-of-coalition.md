# 独立交叉复核：ICML 2025 Coalition

复核者：数学代理 B，2026-10-01。复核基于正式 source.pdf 的逐页文本、原式全转录、content.json 与真实 Lean 源码，不以根代理判断替代数学核对。此文档是代理审阅，非用户逐项认可。

实际核对了 inventory 的全部 19 个数学目标：coalition-shapley、coalition-banzhaf、coalition-conflict、coalition-no-conflict、coalition-individual、coalition-singleton、coalition-anonymity、coalition-symmetry-alpha、coalition-symmetry-beta、coalition-additivity、coalition-dummy、coalition-efficiency、coalition-R、coalition-Rprime、coalition-Q、coalition-toy-support、coalition-matching、coalition-shapley-coefficient、coalition-banzhaf-coefficient。主要原式逐行定位为正式 PDF 3–7、12–21 页；附录 G.1–G.6 全链分别在 PDF17、18、19–20、20、21、21 页。核对 inventory 的24页覆盖记录，但未独立重新图像审阅其余经验图表和文献页，亦未重新运行训练/实验；这些不冒称数学实验证实。

## 原定义到经典指标的桥

Theorem3.2 从 PDF12 的阶乘权重边际定义开始，而非以均分式作为前提。PDF14 的 OR 计数链首行把上一页的不交条件误写成交集非空；重写保留原错式，并用不交环境补集或负补游戏直接证明。公共 `shapley_and_or` 实际调用 `factorialShapley_add`、`dualShapley` 和已证的 `factorialShapley_eq_dividendAllocation`。其中 `dualShapley` 将 i 的前驱总体 R 的环境 U 双射到 R\U，交换两阶乘参数并逐式改写补集边际；不是定义另一个名为Shapley的分配函数。

Theorem3.3 的原 Banzhaf 是所有前驱环境的均匀边际平均，权重为 2^{-(n-1)}。实际 `banzhaf` 明确采用此有限平均；`banzhaf_eq_dividends` 重构边际并计数上集，`dualBanzhaf` 以相同补集双射处理 OR。所得目标 T 的权重为 2^{-(|T|-1)}。`PaperCoalition.theorem32/theorem33` 实例化真实坐标掩码与原 g/2±gamma 分解，未把分配恒等式假设为经典定义。存在玩家 i 自动使 n≥1，2的幂分母恒正。

PDF13 的 Shapley 二项式计数系数完整人读论证与公共阶乘上集系数一致。新增 `shapley_kernel` 核验实际有限前驱和，按基数分组到原数值索引公式仍准确标人类适配。PDF15 的有符号 Banzhaf 上集内和由 U=L∪W 唯一分解得到 (-1/2)^|L|(1-1/2)^{|R\L|}，结果 (-1)^|L|/2^|R|；`signed_half_superset` 直接验证这条原式，包括 R=L 的空和族边界。

## G.1–G.5 的命题边界与反例

PDF17 G.1 从总游戏置换不变直接推出所选两个分量各自运输，缺少选解规则依据。若同一既定分解一起运输，则换元证明成立。稀疏 L1 优化允许多个最优解时，单独重选最优分解不保证匿名性；内容将其标为选解范围问题，未将合法运输证明改称无条件原公理证明。

PDF18 G.2 与 PDF19 G.3 同样把总游戏对称性错误提升为每个分量对称性。独立复核其反例：取 N={1,2,3}、P={1,3}，a(U)=1[P⊆U]+1[2∈U]，o(U)=1[U∩P≠∅]。按 U∩P 的基数0/1/2，可逐项看出 a+o=|U|；原 gamma=a-g/2 合法。唯一非零非空系数为 A(P)=1、O(P)=1、A({2})=1，L1=3。全掩码匹配使任意合法分解的非空系数总和为 g(N)-g(∅)=3，因此三角不等式给 L1≥3；该例达界，确为全局最优。联盟归因 Φ(P)=2，而 Φ({2,3})=0。取 α 的 i=1,j=2,L={3}，β 的 S={1},T={2},L={3}，总基数游戏满足源页全部对称前提，结论失败。该证据不依赖非最优自由分解，也不补分量对称性。

G.3 还有独立索引问题：源页先称 S∩T=∅ 而未给一般重叠情形的合法化约；又将两个分别遍历的有限和改成等基数子集对的双和，重复计数且排除完整子集。由于原命题本身已被上述全局最优反例否定，重写完整保存其原错误链而不尝试添假设证明一个新命题。

PDF20 G.4 的总游戏可加性不能推出独立选出的分量可加。其全局最优反例取 N={1,2}，g1=1[1∈U]、g2=1[2∈U]。两个子游戏取纯AND分解，总游戏取 a=1[N⊆U]、o=1[U≠∅]。逐掩码满足 a+o=g1+g2；子游戏L1各1，总游戏L1=2，分别达到 |g_k(N)-g_k(∅)| 和 |g(N)-g(∅)| 的全局下界。子游戏对N的联盟归因均0，总游戏为2，可加性结论失败。原两子游戏也分别依赖不相交坐标，不能以“independent”一词排除此数学反例。公共 attribution_add 只证明系数已可加时的充分代数事实，不冒充这个原公理。

PDF21 G.5 把总游戏dummy直接提升为分量dummy，依据缺失。显示定义反例 g=0、gamma=1[N⊆U]、a=gamma、o=-gamma 在N={1,2}给 A(N)=O(N)=1、O({1})=O({2})=-1、Φ(N)=2。然而此例L1=4而零分解L1=0，故其正确范围只是否定任意显示分解版本。当前内容明确不声称反驳全局最优选解规则版本，该区别必要且已保留。

## 分母及后续结论

PDF15–16 的冲突分解对非空联盟成立，且3.6的原 i∈S 自动保证S非空。原3.4及3.8全子集量词还包括空S，而原Φ(empty)末项有0/0；公共Lean总除法的零约定不能补原定义。实际 `_nonempty` 适配与partial_scope标识准确。Corollary3.5源自由 i 量词未形成明确的部分覆盖集合定义；重写说明预期部分覆盖条件，保留原歧义，并将其Lean声明作为该条件化范围，而不称全部原文字式通过。G.6使用真实经典效率及冲突分解，输出基线不被丢弃。

R/R′/Q的原比例在零分母处未定义。各分母为非负和，若有值且非零则必正；正分母域上分子≤分母，故区间[0,1]成立。R′靠 i∈S 的索引包含，Q靠全部覆盖S项与分母该子类的相同权重。形式化显式 hd:0<d 是原商有值范围，内容没有把这个域说明伪装成新增原命题假设，更没有令0/0=0后宣称原全域成立。

PDF7的二进制目标函数在零输入基线下，单项式的掩码值为纯AND指示乘以原坐标乘积；线性性得精确目标支撑。若输入某坐标为零，该项系数消失；这不保证拟合DNN的输出恰等于目标，也不保证其学习AND/OR分解唯一。人类适配与 `toy_and_support` 的部分形式范围已分别标明。

未发现需修改的命题或遗漏原数学目标。当前需持续保持的限制是：匿名性选解未规定、Dummy反例非最优、空联盟/零分母域、数值索引与二进制掩码的局部Lean范围。建议验收以59声明的真实审计和各目标scope分别判断，不把编译声明数量当成19原命题全部通过。
