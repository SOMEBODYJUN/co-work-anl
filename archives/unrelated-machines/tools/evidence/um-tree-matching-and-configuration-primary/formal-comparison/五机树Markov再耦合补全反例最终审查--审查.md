---
id: "unrelated-machines/tree-markov-completion-review"
kind: "review"
type_tag: "审查"
title: "五机树 Markov 再耦合补全反例最终审查"
status: "integrated-exact-finite-counterexample"
truth_status: "finite-tree-markov-contract-refuted-with-small-positive-boundary"
review_level: "full-source-read-cross-object-and-code-audit-comparison"
scope: "UM-TREE-MARKOV-COMPLETION-NO-v1、真实全局分布到生成树边际的 Markov 再耦合、五机严格 2T 补全失败和至多四机正面边界"
summary: "完整读取 4975658e3ef8ba0c8506 审查记录并比较 tree_markov canonical、主/独立精确审计、prefix/Gram 与相关 tree/completion 对象。五机路径反例保持 OPT=1 的真实全局分布和四个 1/4 Markov 态，其中一态冻结树任务后任何非树任务补全都需 makespan 2；这只反驳固定生成树、冻结树任务和每态严格小于 2T 的全称合同，不否定择态、换树、任务迁移或一般 UM 算法。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/reviews/unrelated_machines/tree_markov_completion_review.md"
  - "clean:4975658e3ef8ba0c8506"
  - "related-source:9e66cf0e6411197f7a23:research/current/unrelated_machines/tree_markov_completion.md"
  - "related-source:72369fac674ccdc4c862:evidence/runs/unrelated_machines/tree_markov_completion_audit.json"
  - "related-source:4793fd8514c206c37797: evidence/runs/unrelated_machines/independent_tree_markov_completion_audit.json"
related_objects:
  - "双件见证树Markov与类型压缩三源审查--审查.md"
  - "独立稀释残余与树Markov完成审计--审查.md"
  - "三叉彩虹困难与树Markov联合审查--审查.md"
  - "前缀原子证书解码桥与full-degree生成义务审查--审查.md"
  - "前缀原子有限精度与相对Gram审计--审查.md"
  - "严格次二批量能垒与前缀原子解码双源审查--审查.md"
evidence_paths:
  - "archives/unrelated-machines/tools/evidence/tree-markov-completion-20261031/original/tree_markov_completion_review.md"
---

# 来源身份与冻结对象

本页处理 clean source `4975658e3ef8ba0c8506`，原路径为 `research/reviews/unrelated_machines/tree_markov_completion_review.md`，冻结 blob `362d6bff7212d9b24c9cf884fdd3483922af64ed`，源 SHA-256 `627ae18f30b5c34dd8a2aba95861758998a914f9fac9c7b78628b7e222e1274d`，大小 2,966 B。原文已复制到 `evidence_paths`。

被审基线为 main `8701a61b677f1b319053dfa82e7e12ebd7870e64`。当前正文 `research/current/unrelated_machines/tree_markov_completion.md` 的 SHA-256 为 `73628429e0c9773a3cfc083a8b3d87ef3b20004a583df6f5dce2492309a31817`，Claim 为 `UM-TREE-MARKOV-COMPLETION-NO-v1`。规范程序 `tests/audits/unrelated_machines/tree_markov_completion.py` SHA-256 为 `981a354cfb9a41c939a967df8767a3f988d2d13cc732ceaeae802588ea6d72fb`；对应冻结结果 ID `72369fac674ccdc4c862`、SHA `cf2d1bd613e8ac0567f051cc0cf22c0e3059e1775a2e78cff3aec17a5e51b855`。独立实现/结果 ID `4793fd8514c206c37797` 作为第二条精确路径，不重复计为新实例族。

该审查不是外部同行评议；两位内部研究者的独立性只覆盖本组任务重构，未认证全球新颖性。处置为 **integrated-exact-finite-counterexample**。

# 1. 被反驳的 Markov completion 合同

输入是一份真实全局 `T`-调度分布 `D`、一个连通生成树 `F` 和每任务恰两台可用机器的 ordinary UM 实例。每个机器对至多共享一个任务。构造只保留完整单机配置分布和 `F` 上相邻机器对的完整联合边际，然后沿 `F` 按父状态条件分布做 Markov 再耦合。

该 Markov 耦合保持树边 pair marginals 和单机 marginals，但不承诺非树 pair 或高阶交叠。对每个正概率耦合态，合同冻结 `F` 上树任务的分配，再最优补齐非树任务，并声称应能保持 makespan 严格小于 `2T`。审查反驳的正是这个全称量词：**每个正概率树耦合态、固定树任务、无迁移修复，都不能保证严格次二补全。**

它没有反驳以下路线：改选树、保留更多非树相关性、先择态再补全、移动树任务、全局重新优化或允许经过峰值 `≥2T` 的中间状态。

# 2. 五机精确反例

取 `T=1`，机器为 `1,2,3,4,5`，生成树为路径

\[
1-2-3-4-5.
\]

树任务为 `a,b,d,e`，非树任务为 `c`。有限端点如下：

| 任务 | 两个有限端点 |
|---|---|
| `a` | `p_{1a}=1`, `p_{2a}=1/2` |
| `b` | `p_{2b}=1/2`, `p_{3b}=1` |
| `d` | `p_{3d}=1`, `p_{4d}=1/2` |
| `e` | `p_{4e}=1/2`, `p_{5e}=1` |
| `c` | `p_{1c}=p_{5c}=1` |

真实全局分布 `D` 以概率 `1/2` 取调度 A，以概率 `1/2` 取调度 B：

- A：`c→1`、`a,b→2`、`d→4`、`e→5`，负载为 `(1,1,0,1/2,1)`；
- B：`a→1`、`b→2`、`d,e→4`、`c→5`，负载为 `(1,1/2,0,1,1)`。

两种完整调度峰值均为 1，且任务 `c` 的单位端点给出 `OPT=1`。

机器 3 在 `D` 中恒为空，因而路径 Markov 再耦合将左分支 `(a,b)` 与右分支 `(d,e)` 独立；四种左/右组合各以 `1/4` 出现。坏态取左侧 B、右侧 A，冻结

\[
a\to1,quad b\to2,quad d\to4,quad e\to5.
\]

机器 1 和 5 的树负载均已为 1，而 `c` 只能放在 1 或 5；任一补全的 makespan 都恰为 2。因而这个正概率树 Markov 态不能严格补成 `<2T`，尽管原全局分布的每个真实调度都达到 `T=1`。

有限代码逐一构造 32 个完整整数分配、四个 Markov 支持态和每态两种 `c` 补全；所有单机与四条树边 pair marginals 用 Fraction/整数重算，无随机数或浮点误差。独立实现不导入主实现，用逐条件扩展生成同样四态并核对坏补全质量 1/4。

# 3. 反例的修复事实与至多四机边界

该反例不构成所有修复算法的下界。冻结坏态后，把 `a` 从机器 1 移到机器 2，再把 `c` 放回机器 1，即可恢复峰值 1 调度；也可以重新选树或直接从原全局 `D` 的支持中择态。因而这里失败的是“固定树任务、局部 Markov 态逐态补全”的接口，而非 ordinary UM 可行性。

当前正文还给出一个正面边界：在同一合同下，至多 4 台机器的连通树只能是 star 或 double-star；总有一个顶点或中央树边覆盖全部树边。该中心配置或中央 pair 配置在真实分布 `D` 的某个支持态中出现，并决定全部树任务方向；原 `D` 支持态提供 `T` 补全。因此五机是该具体合同的最小机器数边界。

该正面边界不能扩展到：

- 断开森林；
- 每个机器对共享多个任务；
- 不来自真实全局分布的 pair 数据；
- 允许任务迁移后的全局解码；
- 任意树深度或分支度的 Markov completion theorem。

# 4. 与 prefix/Gram/局部边际对象的关系

树 Markov 反例和 prefix/Gram 对象有共同方法边界：单机 marginals、部分 pair marginals 或低阶 Gram 数据可能无法恢复非树兼容性。前缀原子桥要求一个共同非负守恒 law 和**所有完整原子**逐机局部化；树 Markov 只保留生成树 pair，正是少了非树相关性。因而不能用低阶树边际替代 full-degree localizer，也不能把四态有限反例改写成一般 prefix law 生成器失败定理。

相反，若在真实全局 `D` 中保留全部高阶相关性并先择态，再执行完整调度，反例不再适用。任何后续修复需明确：可见 sigma-field、允许保留的非树相关性、任务迁移规则、补全顺序和完整负载/位复杂度量词。

# 5. 有限证据、去重与开放义务

既有《双件见证树 Markov 与类型压缩三源审查》和《独立稀释残余与树 Markov 完成审计》已经记录本五机反例的数值和两条程序路径。本页的独有处置是：

- 重新绑定当前 canonical 正文 SHA、主程序 SHA 和 clean source ID；
- 明确审查对象的全称量词是“每个正概率树态、冻结树任务、严格小于 `2T` 的补全”；
- 明确五机反例的 `OPT=1`、坏态概率 `1/4`、补全峰值 2；
- 记录至多四机中心覆盖的正面边界；
- 把任务迁移、换树、择态和保留非树相关性列为不受反驳的修复路线。

未完成义务包括：

- 对任意树深度、分支度和可见边际定义一般 Markov completion theorem；
- 设计能保留非树相关性的全局 completion/decoder；
- 把局部边际失败接到一般 ordinary UM gap 或 hardness；
- 从一般 `(P,T)` 生成可用的全阶 joint law 或可靠 FAIL；
- 证明与 prefix atomic、PCSP、raw SH3 或 private-group pool 的统一归约。

`UM-TARGET-v1`、一般近二算法/硬度、外部同行评议和全球新颖性均保持 OPEN。

# 6. 结论

`4975658e3ef8ba0c8506` 保留一个精确五机树 Markov 再耦合反例：真实全局分布 `D` 的两个 `T=1` 调度各峰值 1，生成树 pair marginals 的 Markov 再耦合产生四个 `1/4` 态，其中坏态冻结树任务后非树任务 `c` 的任意补全峰值为 2。它严格反驳固定树任务、逐态、无迁移的 `<2T` completion 合同；同时，四机连通树的中心覆盖给出该合同的正面边界。

有限 Fraction 程序和独立实现只核对该明确实例，不把重复程序路径计为新实例族，也不把有限反例升级为一般 Markov theorem、ordinary UM hardness 或主目标算法结论。
