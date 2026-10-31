---
id: "unrelated-machines/protected-cycle-clause-or-failure"
kind: "obstruction"
type_tag: "障碍"
title: "保护环共享 clause-OR 的失效"
status: "proved-explicit-compiler-failure-with-empty-case-repair"
summary: "在明确的 protected-cycle clause-OR 矩阵中，真实 q/b/u/dummy 任务存在共同 fractional perfect matching，并由同一原资格图的整数 matching 恢复 Cmax≤1 的完整实际 schedule；含 UNSAT 手工 10-job 证书，故该 OR 编译不保 source NO。v2 修复空公式至少一台 idle machine 的对象边界。"
source_refs:
  - "clean:49cd6d82095834f4adcf"
  - "clean:28818a3d1bca95c1ff20"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/protected_cycle_clause_or_canonical_section9_read_after.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/protected_cycle_shared_clause_or_v2_read_after_review.md"
---

# 对象身份与修复范围

本页审查 `UM-PROTECTED-CYCLE-CIRCUIT-CLAUSE-OR-FAILURE-v2` 的最终第 9 节组合。两份冻结来源均完整读取：一份核验 canonical 第 9 节，另一份按 v1 Exact-first → v2 Exact → 作者 Proof 的顺序作读后核查。结论是一个**明确编译失败障碍**：该保护环与共享 clause-OR 的矩阵对任意公式都可构造 Cmax≤1 的完整实际 schedule，因此不能把公式 UNSAT 直接映射成 source NO。

| clean ID | 原路径 | 源 SHA-256 | 大小 | 本页处置 |
|---|---|---|---:|---|
| `49cd6d82095834f4adcf` | `history/source/notes/unrelated_machines/protected_cycle_clause_or_canonical_section9_read_after.md` | `947063b40da3a58f7d4b82e0842a3ef29aba154f18b0fa79e8411b42aaa9940e` | 4,967 B | canonical §9 最终组合核验；确认密集矩阵、空退化和 10-job 手工解 |
| `28818a3d1bca95c1ff20` | `history/source/notes/unrelated_machines/protected_cycle_shared_clause_or_v2_read_after_review.md` | `82b6cdfaccdc105b7c7b8df2ba75d5f2073c01601f23c3bf7ddf4ba553cc243b` | 5,089 B | v2 Exact/Proof 读后；独立匹配与作者匹配均合法，确认唯一 v1 对象修补 |

原件和哈希 manifest 位于 `archives/unrelated-machines/tools/evidence/protected-cycle-clause-or-20261031/`；回执草稿在 `cleanup/workspaces/Boss2/protected-cycle-clause-or-receipts-20261031.json`。

# 精确模型与第 9 节域

每个 clause 至少两个物理 occurrences，允许重复变量和文字；每个 occurrence 对应独立的 M_i、C_i 资格身份。环索引至少 3 个；dummy 不属于 clause，polarity 任意。变量 q_i、blocker b_i、unit clause job u_c 的有限端和 processing times 与 v2 原矩阵一致；所有有限时间不超过 1，通常取 a∈(0,1)。可选参数 a>B/2 只服务其它环合同，不参与本匹配失败结论。

空公式 N=h=0 时，v2 明确输出一台 idle 原机器和零 jobs；实际负载 0，满足 UM 机器数至少 1。非空公式时机器两侧数量均为 2N+h，没有 idle；声明为每台非 idle machine 恰一原 job。这个 v2 修补了 v1 的空公式对象问题，且没有在空实例伪造 perfect matching 或 R_c 任务。

# 共同分数证书与整数恢复

令每个 clause c 的 occurrence 数为 k_c。canonical 与 v2 Proof 使用同一分数构造：真实 q_i 质量 1/k_c，dummy 质量 0；q_i 在两个环端各放 1/2，再在 pin 方向扣除 x_i；真实 q_i 在 R_c 放 x_i；b_i 的 pin/C 两项质量分别 x_i、1−x_i；unit job u_c 向各 C_i 放 1/k_c。这里 x_i=1/k_c。

每个 q_i、b_i、u_c 总量恰为一，所有分数非负（k_c=2 时 1/2−x_i=0）。M_i 上扣除的 q pin 项由同索引 b pin 项补回；环相邻 edge 各贡献 1/2，总和为一。每个真实 C_i 的 b/u 项和为一，dummy C_i 只有 b 的一；每个 R_c 有 k_c 项 1/k_c。由此得到同一资格图上的共同 fractional perfect matching，覆盖全部 jobs、全部 machines，不是逐机另换见证。

整数恢复在同一原有限资格图上运行 Hall/最大流或等价交替 BFS，得到每个 job 恰选一个原有限端、每台非 idle machine 恰一 job。所有处理时间为 a 或 1，且每台 machine 至少有 unit job，所以完整实际 makespan 恰为 1。R_c 只邻该 clause 的真实 q_i，保留真实 q 身份，但不保证 q_i@R_c 与 u_c@C_j 具有同一 index；该 identity mismatch 正是编译失败的原因。

# 10-job UNSAT 手工见证

取

`Phi=(x or x) and (not x or not x)`，

环 polarity 为 (0,0,1,1)。这是 UNSAT，但对应矩阵有十台 machine、十件 job 的完整整数 matching。例如 1-based 记号的一份手工解是：

- q1→R+，q3→R−，q2→M3，q4→M4；
- b1→C1，b2→M2，b3→C3，b4→M1；
- u+→C2，u−→C4。

每一端均是原矩阵列出的合法 shifted-unit、small-home、正/负 pin 或 clause-unit 端；十件原 job 各用一次，十台 machine 各有一件，峰值恰 1。取 a=9/10 仍成立。

v2 读后还核对了作者 Proof 的另一份 0-based matching：作者解与上述独立解不同，但两者均逐项合法。作者 q 的正/负返回索引和独立解的索引各自错配对应 blocker，正好说明不需要把“同编号 q→同编号 b”偷加成整数约束。两个 matching 不是版本冲突，而是同一矩阵的不同合法证书。

这份 UNSAT 见证是有限手工证书，不依赖数值搜索；它足以反驳“clause-OR 共享环自动保持 NO”的普遍声称，但不产生一般 UM hardness 或近二不可能性。

# 完整矩阵、复杂度与编译含义

按必要规则把不足三次的变量 occurrences 补至三次，N 不超过原 occurrence 数加两倍出现变量数。若接口直接给出更长 dummy 表，输入/输出大小必须按显式表计，不能按未 padding 的公式长度隐式展开。稠密原矩阵有 O((2N+h)^2) 项；稀疏资格图边数 O(N+sum_c k_c)。分数证书项只含常数和 1/k_c，位长按显式输入多项式，不按 1/a 的数值展开。整数 matching、owner 输出和全机负荷回算均在原资格图上完成。

第 9 节因此证明的是：保留私有 C_i、增加公共 R_c 及 unit-clause-job u_c 的这一**具体** clause-OR 编译，对任意公式都存在实际 Cmax≤1 schedule。它不能保留源公式的 UNSAT/NO；不能用 fractional matching 取代真实调度，也不能用任务 identity 错配自动恢复 hardness。

# 与相关主线的边界

本障碍不否定其它 protected-cycle 机制、medium 共居保护、一般 near-unit identity 机制或 UM-TARGET-v1；它只关闭“共享 clause-OR + 该公开 q/b/u 矩阵”的一条编译路线。canonical 第 1–8 节、其它资源合同和全局 near-two claim 不在本批独立认证范围。没有引入 NP/ETH/UGC 假设，没有新颖性认证，没有把一次有限 10-job 手工解说成所有可能矩阵均失败。

# 本轮实际处置

两源均完整实读，比较了 v1 对象问题、v2 idle 修补、全任务/全机器 fractional 证书、Hall/最大流整数恢复、两份不同 10-job matching、稠密输出规模和 identity mismatch。没有运行脚本或有限枚举；原件及 manifest 在 evidence，正文归档为障碍，回执草稿单列，等待 Boss checkpoint/done。
