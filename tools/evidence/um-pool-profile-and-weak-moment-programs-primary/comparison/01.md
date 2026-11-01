---
id: "unrelated-machines/minimal-star-contraction-capacity-pair-finite-review"
kind: "review"
type_tag: "审查"
title: "极小星收缩与配置耦合有限审查"
status: "finite-exact-audit-with-scope-limits"
truth_status: "finite-replay-supports-the-stated-star-and-pair-certificates; no-general-gap-theorem-from-the-audit"
review_level: "full-json-read-and-related-object-comparison"
scope: "minimal-star contraction, capacity-one pair couplings, nested lift replay, and q-profile compression boundaries"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:evidence/runs/unrelated_machines/minimal_star_capacity_audit.json"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:evidence/runs/unrelated_machines/minimal_star_capacity_audit.json"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/current/unrelated_machines/minimal_star_contraction_and_capacity_gap.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/current/unrelated_machines/minimal_star_contraction_and_capacity_gap.md"
evidence:
  base_commit: "974813e88ff9f80cdda9a1f817be990ce1d90816"
  audit_sha256: "17c4dc79114969228e6eb1c7f02714b22e5145776792f3612ac057589a8558cc"
---

# 审查范围

本对象读取了 `minimal_star_capacity_audit.json` 的全部字段，并回读其主数学稿《极小超载星消去、容量一资源竞争与普通任务压缩边界》。证据由四个 Fraction 精确脚本组成：极小星主重放、容量一星全 pair 耦合、独立极小星重放和 star-profile compression。它支持已声明输入上的有限精确核验；它不把有限枚举、pairwise coupling 或历史脚本输出升级成一般 unrelated-machines 近二算法、复杂度结论或外部同行评审。

## 1. 极小星消元的有限复核

主稿的 `UM-MINIMAL-STAR-CONTRACTION-v1` 假设当前剪枝实例中的机器 `v` 有非空全部邻任务 `F`，且

\[
S=\sum_{a\in F}p_{va}>T,\qquad S-p_{va}\le T\quad(\forall a\in F).
\]

它把 `v` 和 `F` 收缩成一个替代任务 `e`，在每个剩余机器 `i` 使用 `\min_{a\in F}p_{ia}`。主稿给出可行性双向等价；从任意约化分配恢复原任务时只保证 `C_{\max}\le\max(B,T)`，因此不能把它误写成对任意超阈值调度保持同一 makespan 的等价变换。

审计实际使用 `fractions.Fraction`、无容差，抽样 4,000 个矩阵，涉及 956 个适用收缩、3,972 次 lift、776 个不等星情形和 563 个零条目情形。对目标为 1 的星族，完整有限端点为

| `k` | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 已审计整数最优值 | `3/2` | `5/3` | `7/4` | `9/5` | `11/6` | `13/7` | `15/8` | `17/9` | `19/10` | `21/11` | `23/12` |

其中 `k=2` 的独立脚本穷举了 82,944 个整数分配（尺度 2），得到整数最优 3、精确最优 `3/2`。`k=3..12` 的 `minimal_star_irreducible=true` 只表示该有限族没有被所测的合法收缩消去；它不是所有机器矩阵都不可收缩的证明。嵌套收缩审计另抽样 5,000 个矩阵，保留 2,602 个初始合法剪枝实例，检查 122 条至少两步链、123 次嵌套步、83 个拒绝证书和 89,712 个完整 lift；最多看到 3 步。其用途是核对逆序恢复和边界实现，不能替代主稿的符号证明。

## 2. 容量一星的 pair 耦合证书

主稿的紧凑族有 `k` 个中心、`k-1` 个全局机器和每块 `k+1` 个局部资源机，任务时间只有 `1/k` 与 `1`。它给出目标 1 的逐机器配置点、全部机器对的联合配置分布，并证明整数最优值 `2-1/k`。审计把 pair 合同限定为：每个机器边际是给定配置点，正质量配置在同一 pair 上不重复选任务；**不要求**不同 pair 的联合分布拼成一个全局联合分布。

在 `k=3..12` 上，支持配置数从 84 增至 3,900；机器对从 136 增至 15,931；显式相容 pair coupling 从 37 增至 1,279；显式 joint entries 从 249 增至 31,776。Factorized product pairs 与 explicit pairs 分开计数，不能把 factorization 当作额外独立全局证书。每一行均重算出 `minimal_overload_star_irreducible=true` 及整数最优 `2-1/k`，状态为 `all exact assertions passed`。

这份证据因此只支持“该紧凑族上的 pairwise GPC₂(1) 证书和整数端点可重放”。它不支持把 pairwise coupling 自动粘成三台以上机器的一致联合分布，也不提供 GPC₂ 的通用求解器或一般配置 LP 算法。它与已有《Knapsack 拟阵包络与大束碰撞有限审查》中的拟阵 envelope 相邻但对象不同：这里保留中心/全局/局部资源任务的实际机器合同，不能直接把 `D=2-1/k` 表格改称拟阵交的普遍界。

## 3. 独立重放与 profile 压缩边界

独立极小星脚本使用另一个 seed、Fraction 算术，检查 1,095 个合法 fixture、369 个拒绝 fixture、92 个 contraction、7 个 nested fixture 和 7,486 个 residual schedules lift；该结果依然是有限采样，不是一般证明。

`star_profile_compression.py` 对 `q=2,\ldots,8` 的原始 star profile 逐项检查，所有被剪枝分配分别为 19、65、211、665、2,059、6,305、19,171；可行 profile 数为 `q+1`，不可行 profile 数为 4、11、26、57、120、247、502。它报告 2 个特定 envelope counterexamples，并明确任意替代矩阵的排除来自主稿的普遍证明，不来自这些有限枚举。主稿的 `UM-STAR-Q-JOB-COMPRESSION-NO-v1` 只排除固定 q 个普通替代任务、保留所有残余容量 profile 的局部表示；它没有排除带身份的匹配/拟阵接口、增加机器或任务、全局非局部算法、随机化或近似消元。

## 4. 与已有对象的关系

- 与《极小超载星消去、容量一资源竞争与普通任务压缩边界》：本审查保留主稿的精确收缩条件、`\max(B,T)` 恢复界、紧凑容量一族、pairwise GPC₂ 合同和 q-profile 障碍；独有内容是四脚本的实际 SHA、运行规模和有限端点表。
- 与《Knapsack 拟阵包络与大束碰撞有限审查》：二者都出现 `2-1/k` 或容量/匹配语言，但拟阵来源的自由/唯一回路合同和本批的实际机器任务族不同。拟阵审查中的 `(k,p)` envelope、fundamental circuit 和 square-pool collision 不能由本批 pair coupling 直接推出；本批 pair coupling 也不能补上拟阵 `k=7,9` augmentation 未检查的缺口。
- 与共同容量流、未知目标和森林/循环对象：本批仍是 unrelated-machines 的资源/配置模型，不含六人客户、完整历史或纯 SPE 量词；不能跨模型当作 CAG half 证书。

## 5. 真实状态、用途与缺口

**已证明（主稿范围内）：** 极小星可行性双向收缩；给定约化分配的 `\max(B,T)` 恢复界；紧凑容量一星的 `2-1/k` 整数下界/构造；q-profile 的局部不可能性证明。

**有限精确证据：** 上表端点、嵌套 lift、pairwise coupling、独立重放和 profile enumeration。它们可用于回归实现、核对配置/任务身份和测试未来保留身份的匹配接口。

**仍开放：** 一般输入是否存在统一的余量、全局耦合或优于 2 的舍入；如何把保留任务身份的 Hall/matching 接口接到任意多尺寸机器；是否存在通用多项式 GPC₂ oracle。新颖性和外部评审均未认证。下一步若要扩展，必须先明确多机器联合分布或匹配证书的共同一致性，不能用 pairwise 表格替代。
