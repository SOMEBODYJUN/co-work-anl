---
id: "unrelated-machines/fixed-arity-sink-convex-20261030-review"
kind: "review"
type_tag: "审查"
title: "固定过载、固定 sink 与凸局部最小有限审计"
status: "complete"
truth_status: "exact-fraction-finite-audits"
review_level: "source-read-finite-scope-no-general-approximation-theorem"
scope: "unrelated-machines 三个固定容量/固定sink/固定work审计；只保留有限Fraction证据与明确未实现项"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:evidence/runs/unrelated_machines/fixed_arity_overload_witness_audit.json"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:evidence/runs/unrelated_machines/fixed_sink_occupation_audit.json"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:evidence/runs/unrelated_machines/fixed_work_convex_local_minimum_audit.json"
evidence_dir: "archives/unrelated-machines/tools/evidence/fixed-arity-sink-convex-20261030"
---

# 1. 三源对象与全量阅读

本批完整读取三个冻结 JSON（2,173、2,105、4,105 字节），逐字段遍历顶层 scope、精确算术声明、嵌套 finite counts、slacks、counterexample、occupation faces、parameter checks、五个 fixed-work cases 与 family checks。原始字节、SHA-256、来源 ID 和路径保存在 `tools/evidence/fixed-arity-sink-convex-20261030/manifest.json`。三源均采用 `fractions.Fraction`，但其模型身份和未实现范围不同，不能把三个输出合并成一个算法结论。

# 2. 固定 arity overload：三流包络与大槽端点

`fixed_arity_overload_witness_audit.json` 声明 `status="all exact finite audits passed; no universal proof is inferred from these tests"`，seed=20261019，有限局部行分布 5,440、给定 big-only 全证书 484、tuple CSP 等价检查 4,092、8 个非法输入拒绝；覆盖 12 个 `(arity=4..7, long/short/zero)` big-slot classes。它实现的是 triple integer capacity flow 与给定 big-only 证书校验/舍入；明确未实现 general rational LP backend 和 general makespan approximation。

完整三机/多矩阵 oracle 字段为：机器数 2、jobs 1/2/3、14,424 个有限矩阵、65,640 个实际 schedules，其中 21,093 个 reliable failures、22,179 个 successful flows；报告将 `unavailable=true` 保留，不能把“完整 oracle 未提供”抹去。三流 envelope 的有限见证 `B3=11/6`、实际 OPT=1、8 个 schedules 全查、`hardness_claim=false`，合法坏流 sigma 为 `[0,0,0]`。

唯一明确的 scope counterexample 是一行 big-only 配置：矩阵为五个 `1/4`，普通 OPT=5/4，而 big-config LP 在 `T=1` 不可行，因为五个 job 只能走 big endpoint，总期望工作量 `5/4>1`。它反驳的是该 big-only LP 配置的可行性，不是一般 unrelated-machines 近似下界。slack 序列包含 `1,1/2,1/6,1/216,1/2176782336`；最大有限 certificate total 为 `19/14`。这些是指定有限测试的参数，不可推广到所有机器/任务。

# 3. 固定 sink occupation：有限局部菜单与占用面

`fixed_sink_occupation_audit.json` 的 scope 明确为 finite independent audits, not the general proof，seed=910217、Fraction 完整枚举。局部菜单部分覆盖 112 cases、378 actual modes、997 assignments，保留 468 个 feasible local witnesses；zero-target 部分枚举 4,454 matrices、33,910 assignments。occupation faces 部分有 26 cases、6,659 active systems、58 vertices、88 support roundings，并恢复 12 个 actual schedules；最大 fractional homes 为 4。

两个 tight examples 的字段也逐项保留：一个 active systems=7、vertices=2、恢复3个 schedules；另一个 active systems=2024、vertices=4、恢复9个 schedules。one-sided bisection 仅覆盖 16,380 张 acceptance tables 和 1,024 个 scaled macro contract cases，scope 明确“不含 LP 或 full scheduler”。

五个 exact parameter checks 全部给 `gamma=1/4,sink_bound=3/2`，分别为
\[
(K,\beta,\text{heavy\_limit})=(1,1/8,10),(2,1/16,40),(3,1/24,90),(10,1/80,1000),(100,1/800,100000).
\]
这说明固定参数族上的 sink bound 复核，不是一般占用算法或近似比定理。

# 4. 固定工作凸局部最小：五个 identical-machine 家族

`fixed_work_convex_local_minimum_audit.json` 的 claim 为 `UM-FIXED-WORK-CONVEX-LOCAL-MINIMUM-v1`，scope 是 exact Fraction audit of fixed-work identical-machine family; not hardness。五个案例分别为 `(m,jobs)=(3,10),(4,17),(5,26),(8,65),(12,145)`，机器数等于 m，全部 processing times positive、总工作量不变量成立、所有一跳边有限、分析最优值在 Markdown 中给出。

每个案例都验证：初始负载向量一跳到“all-one”动作严格增加 \(\Phi_2\) 且词典序更差；穷举最优值等于解析最优值。代表性数据：

| m | jobs | 初始负载 | 最优负载 | analytic=exhaustive OPT | 最小一跳 \(\Delta\Phi_2\) | 初始比值 |
|---:|---:|---|---|---:|---:|---:|
| 3 | 10 | (2,4/3,4/3) | (5/3,5/3,4/3) | 5/3 | 2/9 | 6/5 |
| 4 | 17 | (2,5/4,5/4,5/4) | (3/2,3/2,5/4,3/2) | 3/2 | 1/8 | 4/3 |
| 5 | 26 | (2,6/5,6/5,6/5,6/5) | (7/5,7/5,6/5,7/5,7/5) | 7/5 | 2/25 | 10/7 |
| 8 | 65 | (2,9/8×7) | (5/4,9/8,5/4×6) | 5/4 | 1/32 | 8/5 |
| 12 | 145 | (2,13/12×11) | (7/6,13/12,7/6×10) | 7/6 | 1/72 | 12/7 |

支持下界 `eps=1/10` 为 3、3、3、3、4，`eps=1/2` 为 4、4、5、6、8。`family_checks` 还明确 `m>=3`、`zero_opt_boundary` 在该 family 外部，需另行处理 zero edges。

# 5. 比较、处置与接续

1. 固定 arity 源的 14,424 矩阵、三流 envelope 与 big-only infeasibility 是有限配置/局部障碍；其 `not_implemented` 明示一般 rational LP 与 makespan approximation 未完成。处置为保留有限证据，不写成 hardness 或算法下界。
2. 固定 sink 源的 occupation faces、one-sided bisection 和 3/2 sink bound 属于不同层级：局部菜单、占用顶点、有限阈值逻辑不能互相替代 full scheduler。处置为同一审查稿分节集成，保留各自 scope。
3. 固定 work 源给出 identical-machine family 的解析/穷举一致性与局部势上升；claim 明确 `not hardness`，不把局部最小构造解释成全局负面结果。
4. 三源都属于 unrelated-machines 数学对象，与当前 CAG 六人目录覆盖模型没有相同玩家/客户语义；不得移入 Q-CAG-HALF-6 证明或反例链。

结论等级：本批是三个互不混同的有限 Fraction 审计，保留可复用的局部不等式、占用面和凸势数据；没有一般 LP、FPTAS/EPTAS、makespan 近似、hardness 或均衡定理。
