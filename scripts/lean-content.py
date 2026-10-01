#!/usr/bin/env python3
"""Authoritative Chinese mathematical descriptions; no paper provenance is inferred."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMMON = ["变量类型 α 的相等关系可判定；S、T、N 为有限子集。", "v、w、d 为实值集合函数，不默认 v(∅)=0。"]

# name, title, statement, specific assumptions, proof steps, tags
ROWS = [
("interaction_empty", "空集交互就是基线", r"I_v(\varnothing)=v(\varnothing)", [], [
"空集仅有一个子集，即空集自身。", "代入定义，指数为 0，系数为 1，故唯一一项是 v(∅)。"], ["empty", "baseline", "空集"]),
("reconstruct_empty", "空集重构", r"R_d(\varnothing)=d(\varnothing)", [], [
"重构求和遍历空集的全部子集。", "这个子集族只有 ∅，于是得到 d(∅)。"], ["empty", "reconstruction"]),
("centered_empty", "中心化后的空值为零", r"v^\circ(\varnothing)=0", [], [
"中心化定义为 v°(S)=v(S)−v(∅)。", "在 S=∅ 时两项相同，因此差为零。"], ["baseline", "centering", "中心化"]),
("interaction_congr", "只需核对目标集合的子集", r"(\forall T\subseteq S,\ v(T)=w(T))\Longrightarrow I_v(S)=I_w(S)", ["∀ T⊆S，v(T)=w(T)。"], [
"交互的求和只读取 T⊆S 处的集合函数值。", "逐项使用假设替换 v(T) 为 w(T)，系数与求和指标不变。"], ["locality", "前提转换"]),
("interaction_singleton", "单点交互是相对基线的增量", r"I_v(\{i\})=v(\{i\})-v(\varnothing)", [], [
"单点集合的子集分为 ∅ 和 {i}。", "前一项的指数为 1，后一项的指数为 0，所以分别是 −v(∅) 和 v({i})。"], ["singleton", "单点", "baseline"]),
("interaction_insert", "增加变量等于取有限差分", r"i\notin S\Longrightarrow I_v(S\cup\{i\})=I_{\Delta_i v}(S),\quad\Delta_i v(T)=v(T\cup\{i\})-v(T)", ["i∉S。"], [
"把 S∪{i} 的所有子集唯一分成不含 i 的 T⊆S，以及含 i 的 T∪{i}。", "i 不在 S 中，所以 |S∪{i}|=|S|+1；对任意 T⊆S 也有 i∉T。", "不含 i 的项比原系数多一个负号；含 i 的项中两边基数都增 1，原系数保持不变。", "配对相加得到 (−1)^(|S|−|T|)[v(T∪{i})−v(T)]，即差分的交互。"], ["recursion", "finite difference", "递推"]),
("reconstruction", "全部交互精确重构集合函数", r"\sum_{T\subseteq S}I_v(T)=v(S)", [], [
"对有限集合 S 作插入归纳，并使归纳假设对任意实值集合函数成立。空集情形由空集交互给出。", "对 S∪{i}，把子集拆成 T 与 T∪{i} 两组。第一组的交互总和由归纳假设等于 v(S)。", "第二组由增加变量公式变成 Δ_i v 的交互总和，归纳假设给出 Δ_i v(S)。", "两组相加为 v(S)+[v(S∪{i})−v(S)]=v(S∪{i})。空集基线包含在求和中。"], ["Möbius inversion", "reconstruction", "反演", "重构"]),
("interaction_reconstruct", "子集和的交互恢复原系数", r"I_{R_d}(S)=d(S),\quad R_d(S)=\sum_{T\subseteq S}d(T)", [], [
"对 S 作插入归纳，空集情形直接计算。", "若 i∉S，则对任意 T⊆S，R_d(T∪{i})−R_d(T)=∑_(U⊆T)d(U∪{i})；两组中不含 i 的项抵消。", "因此 R_d 的插入差分，在 S 的每个子集上等于新系数函数 U↦d(U∪{i}) 的重构。", "使用局部一致性和归纳假设，得到其在 S 上的交互为 d(S∪{i})。"], ["Möbius inversion", "inverse", "反向反演"]),
("reconstruction_unique", "重构系数唯一", r"(\forall S,\ R_d(S)=v(S))\Longrightarrow d=I_v", ["∀ S，R_d(S)=v(S)。"], [
"对任意 S，反向反演给出 d(S)=I_(R_d)(S)。", "假设保证 R_d 与 v 在所有子集上相等，故局部一致性给出 I_(R_d)(S)=I_v(S)。", "逐点相等推出两个集合函数相等；不需要 v(∅)=0。"], ["uniqueness", "唯一性"]),
("interaction_injective", "交互变换是单射", r"I_v=I_w\Longrightarrow v=w", [], [
"若两个交互函数相同，则其在任意 S 的子集总和也相同。", "分别用重构定理把两个总和恢复成 v(S) 与 w(S)。逐点相等即得函数相等。"], ["injective", "单射"]),
("interaction_add", "交互的可加性", r"I_{v+w}(S)=I_v(S)+I_w(S)", [], [
"展开交互定义，把每个系数乘以 v(T)+w(T)。", "使用乘法对加法的分配律，再用有限和的可加性拆成两个交互。"], ["linearity", "additivity", "线性"]),
("interaction_sub", "交互保持差值", r"I_{v-w}(S)=I_v(S)-I_w(S)", [], [
"把系数乘以 v(T)−w(T) 按减法分配展开。", "有限和保持减法，两个求和分别就是 I_v(S) 与 I_w(S)。"], ["linearity", "subtraction"]),
("interaction_smul", "交互保持实数缩放", r"I_{av}(S)=aI_v(S)", ["a∈ℝ。"], [
"实数乘法可交换结合，每一项可改写为 a[(−1)^(|S|−|T|)v(T)]。", "把与 T 无关的 a 提到有限和外，即得结论。a=0 和负数都包含在内。"], ["linearity", "scale", "缩放"]),
("interaction_zero", "零函数的交互为零", r"I_0(S)=0", [], [
"交互定义中的每一项都含因子 0。", "零项的有限和等于 0，空集也成立。"], ["zero", "linearity"]),
("interaction_const", "常数只贡献空集交互", r"I_c(S)=\begin{cases}c&S=\varnothing\\0&S\ne\varnothing\end{cases}", ["c∈ℝ。"], [
"若 S=∅，空集交互给出 c。", "若 S 非空，将其写成 S₀∪{i} 且 i∉S₀。常数函数的插入差分处处为 c−c=0。", "增加变量公式与零函数交互给出非空集合上的交互为 0。"], ["constant", "baseline", "常量"]),
("interaction_centered", "中心化只移除空集交互", r"I_{v^\circ}(S)=I_v(S)-\mathbf1_{S=\varnothing}v(\varnothing)", [], [
"中心化是 v 减去常数函数 v(∅)。", "先应用交互保持差值，再应用常数交互公式。", "S=∅ 时结果为 0；其他集合上被减去的常数交互为 0。"], ["centering", "baseline", "中心化"]),
("interaction_centered_nonempty", "非空交互不受中心化影响", r"S\ne\varnothing\Longrightarrow I_{v^\circ}(S)=I_v(S)", ["S.Nonempty（等价于 S≠∅）。"], [
"中心化公式仅在空集处减去基线。", "S 非空使对应指示函数为 0，因而交互保持不变。非空前提不能删除。"], ["centering", "nonempty", "非空"]),
("interaction_recursive", "从较小集合交互递推", r"I_v(S)=v(S)-\sum_{T\subsetneq S}I_v(T)", [], [
"重构定理的子集和中，S 本身恰出现一次。", "用 powerset.erase S 分离这一项，剩余指标精确对应严格子集。", "把其余交互总和移到右边。即使 S=∅，剩余和为空，仍得到 I_v(∅)=v(∅)。"], ["recursion", "proper subsets", "递推"]),
("reconstruct_single", "单个系数重构纯 AND 函数", r"R_{d_A}(S)=c\mathbf1_{A\subseteq S},\quad d_A(T)=c\mathbf1_{T=A}", ["A 任意有限集，c∈ℝ；允许 A=∅。"], [
"所有系数中仅 T=A 可能非零。", "若 A⊆S，子集和包含这一项，结果为 c；若 A⊈S，所有项为零。", "当 A=∅ 时它属于每个 S 的子集族，因此得到常数函数 c。"], ["unanimity", "pure interaction", "AND", "纯交互"]),
("interaction_unanimity", "纯 AND 函数只含一个交互", r"I_{u_{A,c}}(S)=c\mathbf1_{S=A},\quad u_{A,c}(T)=c\mathbf1_{A\subseteq T}", ["A 任意有限集，c∈ℝ；允许 A=∅。"], [
"上一结论把 u_(A,c) 写成只在 A 上具有系数 c 的函数 d_A 的重构。", "对子集和使用反向反演，恰恢复 d_A。", "故只有 S=A 的交互可能非零；A=∅ 情形与常数交互一致。"], ["unanimity", "pure interaction", "AND", "纯交互"]),
("interaction_dummy", "无贡献变量的联合交互为零", r"i\notin S,\ (\forall T\subseteq S,\ v(T\cup\{i\})=v(T))\Longrightarrow I_v(S\cup\{i\})=0", ["i∉S。", "对每个 T⊆S，插入 i 不改变 v(T)。"], [
"增加变量公式把目标变为差分 Δ_i v 在 S 上的交互。", "假设使 Δ_i v 在 S 的每个子集上等于 0。", "用局部一致性把差分交互换成零函数交互，结果为 0。只知道 v(S∪{i})=v(S) 不足以应用此结论。"], ["dummy", "null player", "无贡献变量"]),
("interaction_relabel", "变量双射重命名保持交互", r"I_{v\circ e^{-1}}(e(S))=I_v(S)", ["e:α≃β 是双射；α、β 的相等关系可判定。"], [
"双射 e 把 S 的子集一一对应到 e(S) 的子集，其逆是逐元素应用 e⁻¹。", "该对应保持子集基数，故交替符号的指数不变。", "重命名游戏在 e(T) 上的值是 v(T)，于是对应求和项相等；有限求和双射给出结论。"], ["symmetry", "bijection", "relabel", "对称"]),
("dividendAllocation_add", "等分交互归因的可加性", r"\phi_i(v+w;N)=\phi_i(v;N)+\phi_i(w;N)", [], [
"逐个 S⊆N 展开等分交互归因。若 i∉S，两侧该项均为零。", "若 i∈S，交互可加性给出分子之和；实数除法保持分子加法。", "对所有 S 求和得到归因可加性。此处使用的是 dividendAllocation 定义，尚未形式证明其与阶乘权重公式等价。"], ["allocation", "Shapley dividend", "linearity"]),
("sum_dividend_shares", "一个非空交互的份额总和", r"\sum_{i\in N}\mathbf1_{i\in S}\frac{x}{|S|}=\begin{cases}0&S=\varnothing\\x&S\ne\varnothing\end{cases}", ["S⊆N，x∈ℝ。"], [
"由于 S⊆N，N 中不属于 S 的变量贡献为零，所以求和可以缩到 S。", "S=∅ 时没有任何项，和为 0。", "S 非空时 |S|>0，求和有 |S| 个相同的 x/|S|，总和为 x。证明显式验证分母非零，没有取消零分母。"], ["allocation", "efficiency", "division", "分母"]),
("dividendAllocation_efficiency", "总归因等于去基线的总值", r"\sum_{i\in N}\phi_i(v;N)=v(N)-v(\varnothing)", [], [
"交换有限的变量求和与子集求和。", "每个非空 S 的等分份额之和由上一结论等于 I_v(S)；空集没有成员，贡献为 0。", "所以总和等于所有子集交互之和减去 I_v(∅)。", "重构定理与空集交互分别给出 v(N) 和 v(∅)。允许 N=∅，此时两边都是 0。尚未形式证明经典阶乘边际公式的等价性。"], ["allocation", "efficiency", "baseline", "效率"]),
("dividendAllocation_centered", "等分交互归因保持中心化", r"\phi_i(v^\circ;N)=\phi_i(v;N)", [], [
"归因求和中的有效项满足 i∈S，故 S 非空。", "对这些项，中心化不改变交互；其他项两边都是零。", "逐项相等推出总和相等。空集基线未分配给任何变量。"], ["allocation", "centering", "baseline"]),
("dividendAllocation_unanimity", "纯交互在成员间均分", r"A\subseteq N\Longrightarrow\phi_i(u_{A,c};N)=\mathbf1_{i\in A}\frac{c}{|A|}", ["A⊆N。允许 A=∅，此时 i∉A，结果为 0。"], [
"纯 AND 函数的交互只在 S=A 时为 c，其余 S 的交互为零。", "假设 A⊆N 保证归因的子集和包含 A 这一项。", "若 i∈A，唯一有效项为 c/|A|；若 i∉A，没有有效项。A=∅ 时使用后一分支，未要求取消零分母。"], ["allocation", "unanimity", "pure interaction"]),
]

DEFINITIONS = {
"Game": ("实值集合函数", "Game α = Finset α → ℝ；有限总体可选用其元素子类型。"),
"interaction": ("Harsanyi / Boolean Möbius 变换", "I_v(S)=∑_(T⊆S)(−1)^(|S|−|T|)v(T)，包含空集。"),
"reconstruct": ("子集求和重构", "R_d(S)=∑_(T⊆S)d(T)。"),
"centered": ("中心化转换", "v°(S)=v(S)−v(∅)，显式去除基线。"),
"marginal": ("插入差分", "Δ_i v(S)=v(S∪{i})−v(S)。"),
"unanimity": ("纯 AND / unanimity 函数", "u_(A,c)(S)=c 若 A⊆S，否则为 0；A=∅ 时为常数。"),
"dividendAllocation": ("按成员等分交互归因", "φ_i(v;N)=∑_(S⊆N,i∈S)I_v(S)/|S|。这是 dividend 形式；与经典阶乘权重的边际 Shapley 公式之间的等价定理仍未形式化。"),
}

def yaml_file(path, values):
    path.write_text("\n".join(f"{key}: {json.dumps(value, ensure_ascii=False)}" for key, value in values.items()) + "\n")

def main():
    descriptions = {}
    for name, (title, summary) in DEFINITIONS.items():
        descriptions["Harsanyi." + name] = {"title": title, "summary": summary,
                                            "assumptions": COMMON, "tags": [name]}
    catalog = ROOT / "catalog/library.json"
    verified = {d["name"]: d for d in json.loads(catalog.read_text())["declarations"]} if catalog.exists() else {}
    theorem_names = {row[0] for row in ROWS}
    for name, title, statement, assumptions, steps, tags in ROWS:
        declaration = "Harsanyi." + name
        theorem_id = "harsanyi-" + name.replace("_", "-")
        proof_id = "proof-" + name.replace("_", "-") + "-v1"
        summary = title + "。统一约定见 docs/math-conventions.md。"
        descriptions[declaration] = {"title": title, "summary": summary, "assumptions": COMMON + assumptions,
            "theorem_id": theorem_id, "proof_id": proof_id, "tags": tags,
            "summary_en": name.replace("_", " "), "statement_tex": statement}
        base = ROOT / "corpus/theorems" / theorem_id
        proof = base / "proofs" / proof_id
        proof.mkdir(parents=True, exist_ok=True)
        lean_dependencies = [d for d in verified.get(declaration, {}).get("dependencies", [])
                        if d.startswith("Harsanyi.") and d != declaration]
        dependencies = ["harsanyi-" + d.removeprefix("Harsanyi.").replace("_", "-")
                        for d in lean_dependencies if d.removeprefix("Harsanyi.") in theorem_names]
        yaml_file(base / "metadata.yaml", {"schema_version": 1, "theorem_id": theorem_id,
            "title": title, "summary": summary, "assumptions": COMMON + assumptions,
            "visibility": "public", "proofs": [proof_id], "lean_declarations": [declaration], "tags": tags,
            "origin": "project_derived", "source_claim_ids": [], "paper_alignment_status": "not_applicable"})
        (base / "statement.tex").write_text(statement + "\n")
        yaml_file(proof / "metadata.yaml", {"schema_version": 1, "proof_id": proof_id, "theorem_id": theorem_id,
            "lean_declarations": [declaration], "dependencies": dependencies, "visibility": "public",
            "lean_dependencies": lean_dependencies,
            "steps": [{"id": "step-" + str(i), "lean_declarations": [declaration]}
                      for i in range(1, len(steps) + 1)],
            "origin": "project_new_proof", "source_claim_ids": [], "review_status": "project_authored"})
        text = f"# {title}\n\n命题：\\({statement}\\)。\n\n"
        text += "前提：" + "；".join(COMMON + assumptions) + "\n\n"
        text += "证明思路：" + steps[0] + "\n\n"
        for index, step in enumerate(steps, 1):
            text += f"<a id=\"step-{index}\"></a>\n\n{index}. {step}\n\n"
        text += f"Lean 关键声明：`{declaration}`。各步骤解释同一声明的证明；类型转换和求和重写属于形式化辅助操作。\n\n"
        text += "来源与对齐：这是本项目一般性数学证明的中文重写，没有宣称来自某篇论文，也没有把任何论文条目标记为已对齐。论文引用映射需另行核对。\n"
        (proof / "proof.zh.md").write_text(text)
    (ROOT / "catalog/descriptions.json").write_text(json.dumps(descriptions, ensure_ascii=False, indent=2) + "\n")
    print(f"Wrote {len(ROWS)} theorem proofs and {len(descriptions)} API descriptions")

if __name__ == "__main__":
    main()
