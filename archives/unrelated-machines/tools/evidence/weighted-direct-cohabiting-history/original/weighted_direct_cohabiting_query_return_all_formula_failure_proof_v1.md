# 异权直接共居查询—返回接口：作者 Proof v1

对应 Exact：`weighted_direct_cohabiting_query_return_all_formula_failure_exact_v1.md`，SHA256 `076561e78796927d6792f6dfb3c581c11afd263752b9098abd9f35d58df2ddfb`。

作者 rainbow，2026-10-18。仅 clone 外 scratch 冻结，先交 root；不直接转 Exact-only reviewer。本证明不改动 Exact、旧 medium sensor、旧 §9、machine-uniform v2 或此前审查来源。

## 1. 原矩阵、空公式及实际任务身份

全部机器、jobs、有限端与参数严格按对应 Exact。非空时 q_i 有三个原端 M_i:ρ、M_{i^+}:1、C_i:x_i；b_i 有 pin(i):ρ、C_i:1；u_c 只在该 clause 的真实 C_i 以时间 y_i 执行。真实 x_i,y_i>0 且 x_i+y_i≤1；dummy x_i=1、无 clause；ρ>1/2。

空公式的 N=m=L=0 单列返回一台 idle 原机与空分配，实际 OPT0。下文非空，所有变量环已显式 padding 到至少3，因此 M_i 与 M_{i^+} 不同。

## 2. strict 满足赋值的全部原 jobs 构造

给源 Φ 的满足赋值。对每变量 v，令 z_v=0 表示其值 true，z_v=1 表示 false。每 clause 选一个真文字 occurrence i；它的 polarity s_i 正好等于 z_v。不同 clauses 的所选 occurrence 身份不同，即使变量或文字重复也不会复制任务。

对被选 i，令 q_i→C_i、b_i→pin(i)=M_{i+z_v}、u_c→C_i。其余索引（包括全部 dummy）令 q_i→M_{i+z_v}、b_i→C_i。每变量的第 i 条有效 cycle edge 只有一件原任务：所选时为 b_i，否则为 q_i；它们全取同一方向 z_v，所以恰一件到每台 M_i，原处理时间均≤1。

所选 C_i 有 q_i 与该 occurrence 所属 clause 的 u_c，两枚真实 jobs 合计 x_i+y_i≤1；其它 C_i 只有 b_i unit。所有 q/b/u 原 jobs 整件各一次，机器负载同时≤1，得到 strict 完整调度。

## 3. 任意 strict 调度的同编号返回及 SAT 解码

给全部原 jobs 的任意实际 σ，峰≤1。所有 M_i 上可能的 finite 时间为 ρ 或1，均>1/2，故每台 M_i 至多一件。

令 E={i:σ(q_i)=C_i}，R={i:σ(b_i)=pin(i)}。由于 x_i>0（dummy 为1），若 q_i 在 C_i，unit b_i 不能也在该 C_i，所以 b_i 必在 pin(i)。这给逐索引包含 E⊆R。

M 机器上实际 jobs 总数恰为 N−|E|+|R|：每 q 不在 C 就在 M，每 b 不在 C 就在 pin，u 没有 M 资格。N 台 M 每台最多一件，因此 |R|≤|E|。与包含合起来，E=R，且 N 台 M 均恰一件。由此 q_i@C_i 当且仅当同编号 b_i 返回 pin(i)，不是靠另一个 occurrence 的返回补总数。

每个 u_c 必在某真实 C_i 执行，y_i>0 排斥该机上的 unit b_i，故 i∈R=E；所以该 clause 的确读到同编号 q_i@C_i。

为每条 cycle edge 定义方向 z_i：若 i∉E，取 q_i 的实际 M_i/M_{i^+} 端；若 i∈E，取返回 b_i 的端 pin(i)，方向 z_i=s_i。每个索引恰有一枚有效边任务在 M，每台 M 又恰一件。机器 M_i 收到的件数为

    (1−z_i)+z_{i^-}=1，

所以 z_i=z_{i^-}，整条变量环同向。将该变量置 true 当 z_v=0、false 当 z_v=1。每个 u_c 所在真实 i 有 s_i=z_v，其文字为真，因此这确实是 Φ 的满足赋值。dummy 可以在 σ 中读出，但不属于 u_c 资格，不能冒充 clause 见证。

全过程只扫描实际 jobs 目的地、计数并沿显式环读取方向，确定性总位多项式。至此 strict≤1 当且仅当 SAT，空公式的真值与空调度也兼容。

## 4. 对所有公式的 baseline / active 划分

不求源赋值。定义

    C_0={c:存在 i∈c，y_i≤1/2}，C_1=其余 clauses，h=|C_1|。

每个 baseline c∈C_0 固定一个 y_i≤1/2 的真实索引 t(c)。每个 active c∈C_1 的所有 y_i>1/2，所以 x_i≤1−y_i<1/2。

以下在一个分析性二部图中暂时仅表示 q_i、b_i 及 active u_c。Baseline u_c 只是暂未放入该图，仍是原 P 必须恢复的原任务；第6节逐件加回，不删出实际输入。

## 5. 只对 active clauses 的一个共同完美匹配

右侧分析节点为全部 M_i、C_i，以及每 active clause 的一个 virtual 标签 V_c，共2N+h。左侧为全部原 q_i、b_i、active 原 u_c，也共2N+h。仅列以下无权资格边：

- q_i→M_i、M_{i^+}；若 i 属于 active c，再有 q_i→V_c。
- b_i→pin(i)、C_i。
- active u_c→其 clause 的每个 C_i。

图中**没有任何 q_i→C_i 边**。Virtual V_c 只作匹配选择的分析节点，绝不是原 P 的机器；最终不在它执行任何任务。Baseline / dummy 的 C_i 在该图只有 b_i 一个 job 邻居。

给每 active occurrence i∈c 定义 θ_i=1/k_c≤1/2；其余 θ_i=0。构造同一份全图分数匹配：

    b_i→pin(i) 质量 θ_i，b_i→C_i 质量1−θ_i；
    active u_c→C_i 质量 θ_i（i∈c）；
    q_i→V_c 质量 θ_i（active i∈c）。

每 q_i 的两个 M 端先各放1/2，再从其 pin(i) 那个端减 θ_i。因为 θ_i≤1/2，所有分数非负。每 q 的总量为 1−θ_i+θ_i=1，每 b 总量1；每 active u 总量 Σ_{i∈c}1/k_c=1。

每个 M_i 的两个相邻 q 基量和1；从任意 q 的 pin 端所扣 θ_i，被同编号 b 的 pin 质量逐项补回，所以每 M 的总质量恰1。Active C_i 有 b 的1−θ_i 加 u 的θ_i，总量1；baseline/dummy C_i 只有 b 的1。每 V_c 收到其 k_c 个 q 的1/k_c，总量1。

因此这是一个共同的完整 fractional perfect matching。对任意左侧 job 子集，质量1逐件相加且右侧每节点容量1推出 Hall；标准确定性整数匹配给同一资格图上的一个 actual perfect matching。这里匹配只是组合选择，不把原 weighted jobs 分数执行。

该整数匹配有以下重要全局事实：

- 每 baseline/dummy C_i 的唯一邻居是 b_i，所以 b_i 必留该 C_i；这覆盖了全部 baseline 原 b，不会让 active 子图偷偷借用其返回资格。
- 每 active V_c 恰接一枚 q_{j(c)}，所以每 active clause 恰有一个 query 被选作随后导出。
- 每 active u_c 在某个 C_{r(c)}，迫同编号 b_{r(c)} 取 pin；反之 active C_i 若不接 b_i，只能接自己 clause 的 u_c。因此每 active clause 恰一枚 b 返回，其余 b 留 C。
- 每台 M_i 恰接一枚 q 或 b，特别所有返回 b 的 pin 互异。Baseline/dummy q 没有 virtual 边，也没有 C 边，因此都在环内。

这正是旧保护环 §9 的共同匹配技术针对 active 子族的直接应用；不称新的匹配定理。k_c≥2 是 θ_i≤1/2 的实质条件，本证明不纳入 unit clauses。

## 6. 恢复所有原 jobs，消去每个 virtual 节点

从上述整数匹配得到原 P 的 actual τ：

1. 所有图中 q_i 若取 M_i/M_{i^+}，保留该原端及其真实 ρ/1 时间；若取 V_c，则改放该同一原 q_i 自身 C_i，真实时间 x_i。
2. 所有 b_i 保留图中原 C_i/pin 端，真实时间1/ρ。
3. Active u_c 保留图中的原 C_i 端，但按其真实时间 y_i 执行。
4. 每个暂未入图的 baseline 原 u_c 全部加回，放 C_{t(c)}，真实时间 y_{t(c)}≤1/2。

每件原 q/b/u 都恰执行一次；没有额外分析任务需要执行，也没有任何实际目的地是 virtual V_c。原资格全由第1节的真实矩阵提供。

逐类核全部原机器的负载：

| 原机器 | 完整 τ 上的任务与负载 |
| --- | --- |
| 每个 M_i | 完美匹配的一件原 q 或 b，真实时间≤1 |
| Baseline C_i | b_i unit；若 i=t(c) 再有原 u_c，合计≤1+1/2；无导出 q |
| Dummy C_i | 只有原 b_i，负载1 |
| Active C_i，匹配有 b_i | 没有 u_c；可能有本 clause 导出的同编号 q_i，负载≤1+x_i<3/2 |
| Active C_i，匹配无 b_i | 匹配恰有原 u_c；可能再有导出的同编号 q_i，负载≤y_i+x_i≤1 |

没有两 clauses 的 u 同到一个 C_i，因为 occurrence 只属于一个 clause；重复文字或变量不改变其不同物理身份。Baseline 的原 q/b 保持整个共同匹配原状，baseline 的原 u 明确在第4步恢复且负载已计。所有 M/C 在同一个完整 τ 内同时≤3/2。

这证明所有 Φ、所有合法异权、所有环排序和 dummy polarity 下的主失败结论。即使输入 UNSAT，也不需要求源解或未知 strict witness 来输出这份实际三半调度。

## 7. 显式位复杂度与准确结论

最少 padding 时 N≤L+2v，非空原矩阵2N台机器、2N+m原 jobs、5N+L有限资格，完整 dense 项2N(2N+m)。若另给更长显式 dummy 表则按其实际 N 计，不按压缩参数宣称线性输出。

Baseline 分类只需对原 y_i 与1/2作有理比较。分析匹配图为显式多项式规模；θ_i=1/k_c 的编码位长 O(log L)。所有部分和/合法性/权重与负载回算的位长由输入有理编码长度多项式控制。整数匹配仅用图，不需要按 x_i、y_i、ρ 的倒数或分母生成任务。最终每个原 job 输出一个原机器编号，总输出多项式。

原 medium pair-sensor 有 D/h、此处没有；旧 §9 有真实公共 R_c、此处 virtual V_c 仅是证明工具，最终已全部消去。没有冒称这些旧输入或其量词被本版静默加强。本构造真正增加的内容是 occurrence-dependent 异权 direct co-location、baseline/active 混合以及全部原 jobs 的共同负载恢复，技术核心 matching 已明确扣除。

这不是 source near-2 hardness；严格 SAT 双向性只验证候选严格端，不能补上已经被全公式3/2逃逸破坏的弱 decoder。也不是一般 medium 共居接口不可能性、一般 UM 算法或所有身份复制器不可能性。没有有限枚举代替证明、没有新软件、外审或全球新颖性认证；主目标保持 OPEN。
