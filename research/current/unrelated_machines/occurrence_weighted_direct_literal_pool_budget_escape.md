# 出现位置异权的文字池：完整资格预算下的三半逃逸

读取目的：核查一种真实的多子句共享变量池构造。各 query 可以在同一变量、同一正负侧使用不同时间；本页给出同时安排全部原任务的三半上界，说明这种改动仍不足以产生近二 NO。排序槽与整数匹配是标准工具，不主张新的通用匹配定理。

## 精确身份

- **ID/version**：`UM-OCCURRENCE-WEIGHTED-DIRECT-LITERAL-POOL-BUDGET-ESCAPE-v1`。对应冻结的 statement-only v2 合同；原件未有此稳定 ID，本文首次赋予，不倒填原件。
- **Objects / Domain / Definitions**：显式 CNF 每子句至少两个 literal occurrences；每个 occurrence 是不同身份，允许重复变量/文字。每个位置有非负 binary rational 时间 b_e；每变量每个 polarity 的**全部 eligible occurrences** 时间和各至多 1。普通 UM 矩阵恰为下节的 pools、private roots、queries、selectors；没有其它端、guard、预载或侧约束。
- **Quantifiers / Exact Statement**：对每个该域实例，确定性总位多项式输出同一矩阵所有原任务的完整合法 actual assignment。每子句恰选择一个自己的原 occurrence，只有该 query 导出；每 root 负载至多 1，含 f_v 的 pool 的 query-only 负载至多 1/2，另一 pool 至多 1，故全机峰值至多 3/2。
- **Assumptions / Conclusion**：无复杂度假设，不需 SAT、strict 见证或配置 oracle。上界包含 zero 时间、unused variables、空公式和重复 occurrences；不是普通 UM 的统一新近似比，也不证明某个源问题困难性。
- **Dependencies**：`UM-MODEL-v1`、本页完整对象域、有限二部匹配整数性。证明自足，无有限实验前提。
- **Evidence / Objections / Status**：typed 是原候选提出者且熟悉标准槽匹配，不记对整个方向 blind；对本次新 Exact 只看陈述独立完整重构后冻结，root 实际全文读后才解封作者 Proof，之后另冻实际读后记录。root 为该上界共同研究者，不记盲审。最终正文实际审查的版本与范围见[审查记录](../../reviews/unrelated_machines/occurrence_weighted_direct_literal_pool_budget_escape_review.md)。限定证明完整；无实现、外审或全球新颖性认证。
- **Scope / Related Files**：只排本页独立 private-root / full-sign-budget 编译合同；不排额外跨子句端、shared guards 或更大的资格预算。相关旧域见[直接共居 query/return 的严格 SAT 与三半边界](direct_cohabiting_query_return_strict_sat_and_sharp_escape.md)，二者矩阵不同，不相互转移其锐性或认证。`UM-TARGET-v1` 仍 OPEN。

## 1. 完整实际矩阵

设 N 个变量、M 个子句、L 个 occurrences，k_c≥2。每 occurrence e 属于唯一子句 c(e)，有变量 v(e) 与 polarity s(e)∈{+,-}。要求

\[
b_e\in\mathbb Q_{\ge0},\qquad
\sum_{e:v(e)=v,\ s(e)=s}b_e\le1\quad(v,s).
\]

预算计所有资格，不是只计最终被选位置。不同名字表示不同物理机器或任务，未列有限端全部为 ∞：

| 原任务 | 全部原有限端与时间 |
| --- | --- |
| 每变量 f_v | A_(v,+):1；A_(v,-):1 |
| 每位置 j_e | 自己的 R_e:1；自己的 A_(v(e),s(e)):b_e |
| 每子句 s_c | 该子句每个 occurrence 的 R_e:1 |

有 2N+L 台原机、N+L+M 枚原任务、2N+3L 个 finite 条目。若 N=L=0，增一台 idle 机满足 m≥1，任务仍空。合法文字引用下该情形也有 M=0。空公式与 empty clause 不同；后者不在 k_c≥2 的域内。

所有 zero queries、所有未被选位置和 private roots 都保留。算法槽从不进入这个矩阵。

## 2. 两侧最大位置合槽，其余位置成对

对每变量的每一侧，把全部原 occurrences 按 b 非增排列为 e_1,e_2,…，权 w_1≥w_2≥…≥0，ties 按原索引固定。

把同一变量正负两侧的首项放进同一个容量 1 槽；某侧为空则槽只含另一侧首项。两侧都空时不建槽。每侧剩余项按 (e_2,e_3)、(e_4,e_5)、… 分别成容量 1 槽，奇数剩项单独成槽。各槽至多含两个真实 occurrences，不跨其它变量合并。

建 clause-to-slot 二部图：子句连到含其原 occurrence 的槽，每条边保存一个真实 occurrence witness。若同一子句两个位置落同槽，可以合并边但保留一个见证。

对每个子句，把 1/k_c 质量沿它的每个 occurrence 送往该槽。子句行和为 1；每槽至多两项，每项≤1/2，故槽列和≤1。有限二部匹配整数性给一张同时覆盖全部子句的整数匹配。每子句取其匹配边保存的原 occurrence。一个原 occurrence 只属于一个子句，故不会重复选出同一 query。

这个分数匹配仅证算法图的可行性，不把任务拆分，也不执行虚拟槽。

## 3. 同一输出中的全部负载

同变量两侧首项共享容量 1，所以至多一侧首项被选。把 f_v 放到首项未被选的那一侧；空侧也可选择。若两首项都未选，固定选择一侧即可。

在含 f_v 的侧，首项 w_1 未选，其余每槽至多选一项。因此 query-only 总负载至多

\[
w_2+w_4+w_6+\cdots
\le\frac{w_1+w_2+w_3+\cdots}{2}\le\frac12.
\]

中间不等式逐项用 w_(2t)≤w_(2t-1)；末尾未配对奇项非负。空表给负载 0。该 pool 加上真实 f_v 后至多 3/2；另一侧没有 f_v，被选 queries 只是全部 eligible occurrences 的子集，其总负载至多 1。

对每子句，把 s_c 放到其所选原 R_e，同时把**同一枚** j_e 送到它的原 literal pool。每个其它 j 留自己的 private root。不同 occurrence 有不同 root，包括重复变量或相同文字，所以被选 root 只有 selector、未选 root 只有自己的 query，全部负载至多 1。

所有 f、selector、query 恰执行一次；所有目的地都是该原任务的 finite 端。上面的 pool 界与 root 界属于这同一张实际完整调度，没有逐子句分别使用多份容量。

## 4. 编码长度、退化与独立重构

槽和 witness 图大小 O(N+L+M)，可确定性整数匹配。原 b 只用于二进制有理比较和负载求和；可行性用的 1/k 不需按分母复制。没有按 1/b、参数数值或 denominator 展开。输出给每枚原任务一个原机索引，原 dense 矩阵与稀疏编码下都为总位多项式。

b=0 的 query 若被选，在 pool 实际以 0 执行；否则在自己的 root 以 1 执行，不删除任务。b=1 的 ties 按固定顺序处理。unused variables 只需将 f 放一侧；空任务实例的 idle 机负载 0。算法不处理 unit/empty clauses，因为 1/k≤1/2 是承重前提。

typed 的先行独立稿使用另一种等价构造：每 clause occurrence 分数 1/k，并将每枚 f 在两 pool 各放半份，按真实时间排序造单位槽。f 只占首槽，后槽的真实 query rank 至少为 2ℓ−2，仍得到偶数项总和≤预算一半。该记录先冻结，之后才读本文作者的合并首项构造，两个实际来源不互相倒填。

没有软件运行或有限枚举作为一般证明。全文给出真正构造，不假定未知 strict 模式存在。

## 5. 对反面路线的准确影响

这个候选已经允许多子句共享同一变量 pool、同一 query 的 private-unit / pool-small 角色和逐 occurrence 异权。只要保留完整资格预算≤1，上述全公式 actual≤3/2 就阻止它成为近二 NO 源；严格端的逻辑含义不能补上弱调度 soundness。

不能由此推定所有 query 编译、shared guards 或更大预算都失败。去掉全部预算后，折叠每子句选择会得到一般 unrelated 任务的资格/成本，需另给真实源 YES/NO 与任意低负载调度的解码；不能把一个包含原调度问题的表示改写当作困难性证明。本文不排这些更大域，也不把局部失败称为 UM-TARGET-v1 的否定。
