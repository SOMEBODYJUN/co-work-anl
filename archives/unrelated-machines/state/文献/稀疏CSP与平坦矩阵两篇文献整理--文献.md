# 稀疏 CSP/MMSNP 与平坦矩阵：两篇文献整理

- **处理身份**：Boss2 / cleaner。
- **来源处理**：两个冻结 PDF 均以 `clean show --out` 导出，再用 `pdftotext -layout` 读取全文；原 PDF、全文文本、manifest 和验证脚本在 `tools/evidence/retired-literature-structural-algebra-20261031/`。
- **对象分离**：第一篇属于有限关系结构/CSP 的稀疏化与 expander 构造；第二篇属于多项式矩问题、Hankel 算子和半定规划。二者都不是当前六人客户 SPE 模型的 payoff 或覆盖证明。

## 来源与稳定证据

|ID|冻结路径|SHA-256|大小|证据文件|
|---|---|---|---:|---|
|`26df96661a014c73e2cc`|`history/source/literature/unrelated_machines/kun_2013_constraints_mmsnp_expander_relational_structures_v2.pdf`|`e6d37a035edb3cbaa3e246e5781a88c8a348eaaa16a57028dd8782dcf7373eea`|183600|`kun_mmsnp.pdf`, `kun_mmsnp.txt`|
|`b0433f284cf362ec6d5e`|`history/source/literature/unrelated_machines/laurent_mourrain_2008_flat_extension.pdf`|`a79a6aae70263cdc0b15415f838df666cfb99d6a00ef87bb1dae381493478fad`|154865|`laurent_flat_extension.pdf`, `laurent_flat_extension.txt`|

`source-manifest.json` 记录全文阅读范围；`validate_sources.py` 对来源 SHA、证据 PDF、提取文本存在性和非空性做 PASS。二进制来源没有只看旧摘要，正文、引理、算法步骤、反例和应用段落均已核对。

## 1. Kun：Constraints, MMSNP and Expander Relational Structures

### 目标与定义

对有限关系类型 `τ`，结构之间的 homomorphism 保持每个关系元组。`CSP(T)` 是能同态到有限结构集 `T` 的结构类；MMSNP 是 Feder–Vardi 的单调单调严格 NP 语言类。来源的 Sparse Incomparability Lemma 目标是在不改变给定小目标结构 `T` 的同态可行性的同时，把输入结构稀疏化到任意指定大 girth。

作者定义 `ε-expander relation`：对任意各坐标子集 `S_i`，关系元组数与独立均匀期望的偏差不超过 `ε|R|`；Lemma 6 证明了子集定义与对 `[0,∞)` 或 `[0,1]` 函数的乘积和式定义等价。`(Δ,ε)`-expander relational structure 要求所有至少二元关系满足该性质且最大元素度不超过 `Δ`。

### 主要定理与算法

1. **Sparse Incomparability（Theorem 1）**：给定正整数 `t,k`、有限关系类型 `τ` 和结构 `S`，可在多项式时间构造同类型 `S'`，使 `girth(S')>k`，并且对所有大小 `<t` 的 `T` 有
   \[
   S\in CSP(T)\iff S'\in CSP(T),
   \]
   同时 `S'→S`。这是确定性多项式时间版本，保留小目标集上的同态可行性而提高 girth。
2. **Expander 构造（Theorem 3）**：给定 `τ,k,ε`，当 `n` 大于仅依赖 `τ,ε,k` 的阈值时，可在多项式时间构造大小 `n`、最大度有界、girth 至少 `k` 的 `ε`-expander relational structure。证明先以随机结构、Chernoff/Markov 界说明存在性，再用 expander graph 与 twisted product 去随机化。
3. **Twisted product（Theorem 9）**：它是 zig-zag product 的关系结构推广。若 `A` 已有 girth 至少 `k` 且 `|A|^{1/k}>Δ(A)Δ(B)`，则可通过逐步置换纤维坐标的算法构造 `C`，使 `girth(C)≥k`。每次减少当前最短环数，使用 BFS 找到需要交换的纤维点；运行时间保持多项式。
4. **CSP 与 MMSNP（Theorem 2）**：对每个有限关系类型和 MMSNP 语言 `L`，存在有限结构集 `T`，使 `L` 与 `CSP(T)` 互有多项式时间归约。证明通过 Feder–Vardi 的有限 girth 中间定理、expander/twisted-product 稀疏化以及 Lemma 13：expander 纤维中从 `C` 到 `T` 的同态可按每个 `B`-纤维多数值抽取成 `B→T`。

### 证明边界与用途

- `t,k,τ` 和小目标结构大小的量词是定理的一部分；不能把“保留小目标同态”替换成所有无限目标或所有参数同时成立。
- expander 关系的乘积估计依赖关系非空、最大元组度和 `ε|T|^r<1` 等条件；twisted product 的算法依赖 `|A|^{1/k}>Δ(A)Δ(B)`。
- 该文献证明的是关系结构同态/CSP 复杂度归约，未涉及客户目录、均分价值、SPE 偏离或六人半覆盖。第三阶段可把它作为“保持有限目标同态的稀疏化/大 girth”方法线索，但不得把其 expander 结论当作当前模型的概率覆盖定理。

## 2. Laurent–Mourrain：A Sparse Flat Extension Theorem for Moment Matrices

### 矩阵模型

令 `K[x]` 为多项式环，`C` 是包含 `1` 的有限单项式集，`C^+ = C∪⋃_i x_iC` 是 closure，`∂C=C^+\\C` 是 border。对线性泛函/矩序列 `Λ`，矩阵 `M_C(y)` 的条目只依赖乘积 `ab`；对应的 Hankel 算子是 `H^C_Λ:Span(C^+)→Span(C^+)^*`。所谓 flat extension 是扩展后秩不增加，并且旧矩阵是主子矩阵。

### 主要结论

1. **经典 flat extension**：正半定且有限秩的完整矩阵有唯一有限原子表示测度；`M_t` 是 `M_{t-1}` 的 flat extension 时，存在唯一完整矩序列扩展。正半定加 flat 条件给出表示测度的充分条件。
2. **稀疏扩展（Theorem 1.4）**：若有限单项式集 `C` connected to `1`（每个单项式可沿着仍在 `C` 中的前缀逐变量生成），且 `M_{C^+}(y)` 是 `M_C(y)` 的 flat extension，则存在唯一完整序列 `\tilde y`，使完整矩阵 `M(\tilde y)` 是 `M_{C^+}(y)` 的 flat extension。Theorem 1.5 给出同一命题的 basis-free Hankel 形式。
3. **交换乘法算子**：对 border prebasis，边界替换产生的乘法算子 `χ_i` 在 `C` connected-to-1 时两两交换，当且仅当基底确实生成商空间的 border basis。作者把这一结构用于 flat kernel 的递归扩展。
4. **表示测度和优化应用（Theorem 3.2）**：若 `Λ` 正且 sparse Hankel operator 满足 rank-flat 条件，则截断序列有 representing measure。由此，半定规划的最优矩若 flat，可证明松弛值等于原多项式在半代数集上的全局最优值，并从矩阵抽取有限原子/全局优化器；对有限实根问题也可用最大秩 flat 解抽取全部根。

### 失败机制与条件

- `connected to 1` 不是装饰条件。来源给出 `C={1,x^3}` 等不连通例子，其中相同秩的局部矩数据无法 flat 扩展；因此不能仅凭秩相等推断全局矩序列存在。
- 即便 `C` connected to `1`，也可能不存在含 `1` 的简单 column basis；作者用 `C={1,x_1,x_1x_2}` 的例子说明必须使用更一般的 kernel/border-basis 论证。
- 正半定、rank-flat、局部化约束和实数域假设各自承担不同义务；文献没有把任意有限矩阵或任意 LP 解自动变成表示测度。

## 跨来源接续

Kun 的 sparse incomparability 处理的是有限关系结构的同态保持，Laurent–Mourrain 的 flat extension 处理的是代数矩数据的全局表示；两者都体现“局部数据 + 明确结构条件 → 可扩展对象”的模式，但扩展对象、量词和失败机制完全不同。它们均归入 unrelated-machines 的文献层，独有内容保存在本正文和 evidence，不合并为当前六人 SPE/目录覆盖主线。
