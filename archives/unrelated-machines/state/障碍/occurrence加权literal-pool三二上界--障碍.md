---
id: "unrelated-machines/occurrence-weighted-direct-literal-pool-three-halves"
kind: "obstruction"
type_tag: "障碍"
title: "occurrence 加权 direct literal pool 的三二上界"
status: "proved-bounded-compiler-with-explicit-scope"
summary: "对显式 CNF occurrence、每变量正负 eligible 权总和各≤1、每 clause occurrence 数≥2 的 direct literal-pool 编译，确定性 matching 选一 occurrence/cla​​use，选中 f_v 的 literal pool query load≤1/2、另一 pool≤1，全部原 jobs 保留且 Cmax≤3/2。该证明阻断该精确 full-budget compiler 作为 near-two NO source，不扩到额外端点、大预算、一般UM或hardness。"
source_refs:
  - "clean:2a81da0cb6e1a2ebd5ec"
  - "clean:61819e5c09d142ab5879"
  - "clean:0281430d4d25b6ae33a4"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/sol_literal_budget_exact_first_attack.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/sol_literal_budget_author_read_after.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/sol_literal_budget_canonical_scope_review.md"
---

# 对象、来源与结论范围

三份来源共同审查 occurrence-weighted direct literal-pool v2：Exact-first 独立攻击、author Proof read-after、canonical scope review。结论为一个明确的**三二上界障碍**：在该 full eligible-budget、private-root/direct-pool 矩阵中，无论公式是否满足 SAT，均可构造完整实际 Cmax≤3/2 schedule。因此该精确编译不能把 UNSAT 变成 near-two NO。

| clean ID | 原路径 | SHA-256 | 大小 | 实读性质 |
|---|---|---|---:|---|
| `2a81da0cb6e1a2ebd5ec` | `history/source/notes/unrelated_machines/sol_literal_budget_exact_first_attack.md` | `c7595ac3593377a94ea61da549abac5cc0bdc466160bd29443021548b79d4c74` | 9,125 B | 只读 Exact 的独立完整构造、matching、全 jobs、位复杂度和退化 |
| `61819e5c09d142ab5879` | `history/source/notes/unrelated_machines/sol_literal_budget_author_read_after.md` | `77849b586c3ce0940e74f544acfda02a456553f16fb1a7421923015f9e766272` | 8,248 B | 作者 Proof read-after；核对 clause-only graph 与独立 all-job matching 等价 |
| `0281430d4d25b6ae33a4` | `history/source/notes/unrelated_machines/sol_literal_budget_canonical_scope_review.md` | `601d8feb61e9c0cdd3d4b4bce362100a4af281e1db150e2d0564864eebda0453` | 9,165 B | canonical 全文 scope review；确认 v2 identity、零端点、限制和非循环性 |

证据原件和 manifest 位于 `archives/unrelated-machines/tools/evidence/literal-budget-three-halves-20261031/`，回执草稿在 `cleanup/workspaces/Boss2/literal-budget-three-halves-receipts-20261031.json`。

# 精确矩阵与 matching construction

输入是显式 CNF；每 clause 至少两个 occurrence，重复变量/文字 occurrence 具有独立 physical identity。每变量 v 有两个 literal pools，各 pool 的 eligible query 权非负且总和≤1；每个变量有一枚 unit `f_v`，可去任一 pool 的第一 slot。每个 occurrence query 是原不可拆 job：自己的 private root 端时间一、对应 literal pool 端时间为其 weight；每个 clause 有 selector，可放任一 occurrence root。没有额外 guard/endpoint/隐藏 inactive 约束。

对每个 literal pool，按权重非增排列 query `q_1,...,q_d`。建第一 slot，放 `{f_v,q_1}`（d=0 时仅 f_v）；之后 slots 为 `(q_2,q_3),(q_4,q_5),...`，最后奇数 query可单独成 slot。另给每个 occurrence 一个 root slot。matching graph 边为：f_v→其两个第一 slots；每个 query→自身 root slot和其唯一 pool slot；每个 clause selector→该 clause occurrence roots。

fractional witness：f_v 两边各 1/2，query 两边各 1/2，clause selector 对每 occurrence 边权 1/k_c。clause 行和一；第一 pool slot 至多 1/2+1/2，其余 pool slots 至多两 query 各 1/2；root slot 收 1/2+1/k_c≤1。Hall 给覆盖所有原 jobs 的 deterministic matching，固定 identity tie-break 即可实现。

作者 Proof 的 clause-only graph 与 Exact-first 的 all-job graph 等价：作者将两个 first pool slots 共并为一个 special slot；独立构造先匹配全部 jobs，再把未选 occurrence query 放回自身空 root。两者都选出每 clause 恰一个 original occurrence，保留零 query、重复 occurrence 和未选 roots。

# 三二负载界与完整实际输出

若某 pool 收到 f_v，则 q_1 不能同时占用该 slot；其余 slots 的最大 query 权为偶数序列之和。若排序权为 b_1≥…≥b_d，

`2 sum_h b_(2h) <= sum_i b_i <=1`，

故该 pool query-only load≤1/2；加 f_v 的 unit load 得≤3/2。另一 pool 只含其 eligible queries 子集，load≤1。每个 selected root 只执行 selector，unselected root 只执行其 query，故 load=1；每个原 job 恰执行一次、原 finite endpoint 不变，完整 P 的 Cmax≤3/2。

权重为零仍按 occurrence identity 排序并保留；unused variables 的 f_v 只占一个 first slot；无 clauses、N=L=0、奇数 occurrence、重复文字和空/zero query 都有明确分支。该结论不是 SAT witness、实际 optimum 或 LP oracle 的结果，而是对每份输入的直接 schedule。

# 位复杂度与 canonical scope

Graph 左侧 N+L+M，pool slots≤2N+L/2，root slots L，edges=2N+3L；M≤L/2。排序只用 binary-rational cross multiplication，matching 只用 integer augmenting paths，不按权重倒数、分母或最小正值展开。完整 dense matrix、zero jobs 和所有 private roots 均保留，输出总位长 polynomial。

canonical scope 明确：这是 bounded compiler 的独立 identity，新 identity 不回溯认证旧域；不声称 strict-SAT 等价、sharpness、一般 UM approximation、额外 endpoint/guard/更大 budget 的 impossibility、hardness 或 global novelty。更大预算可表达一般 assignment，但若把一般 UM 问题直接重写为 literal-pool syntax 会循环，不能代替 source YES/NO 与 arbitrary-low-load decoder。

# 本轮实际处置

三源均完整实读并比较 Exact-first matching、author clause-only matching、canonical scope、零/重复/unused 退化、all-job schedule 和 bit cost。没有运行新代码或外部审核；原件和 manifest 在 evidence，正文归档为障碍，回执草稿单列。
