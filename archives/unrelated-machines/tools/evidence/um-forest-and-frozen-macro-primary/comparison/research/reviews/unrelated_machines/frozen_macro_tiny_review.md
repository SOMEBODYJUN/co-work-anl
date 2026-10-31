# 共享汇点微任务重开与宏任务迁移前沿的独立冻结审查

审查者：boss9 内部子研究者 joint_repair；boss9 汇总。审查方式为先仅接收 Exact Statement 与家族、独立重构及独立代码核验，再读冻结证明与规范实现。下述限域命题的内部独立重构及冻结攻击完成，未见尚成立的 fatal objection；没有审定全球新颖性、外部评审或主目标完成。

## 1. 被审版本、持久入口与独立顺序

- 正文：`research/current/unrelated_machines/optimal_hull_marginal_rounding_barrier.md`，本次审查范围为新增 §10，最终全文 SHA256 `e25a377256fc2bd0f2d267b2288031486992d437684aabe8aa4a4848fd1f14e3`。这不是对既有 §1–9 的重新审查。
- 规范实现：`tests/audits/unrelated_machines/frozen_macro_tiny_reoptimization.py`，SHA256 `97afaac0c35c67e0738a0b4b5fb41461a7a6f31ac69fd8258a48d751b247df1c`。
- 规范结果：`evidence/runs/unrelated_machines/frozen_macro_tiny_audit.json`，SHA256 `58d7a7636ade0ff26a0e5697d58eb8970023c2454d71348edafc53e1a4cfa8a6`。
- 独立实现：`tests/audits/unrelated_machines/frozen_macro_tiny_independent.py`，SHA256 `803f4d97a500eae7e08ce5b35317350ded43e199be68201adca5f8dd50bdfc69`。
- 独立结果：`evidence/runs/unrelated_machines/frozen_macro_tiny_independent.json`，SHA256 `f306e76183741f38341f0d1e2b1f3fffaab877df0b6f5bf84a451e57703e1320`。

独立顺序：审查者先仅收到精确陈述、机器/任务/时间、x、sigma 与阈值定义，未读证明或代码，即冻结先行重构，其内容哈希为 `b853b3d77a7ea559ab7b94e1b1fbb4054e0cd2069cd60647c2029472edb7f753`。先行重构的实质推导已完整吸收于本审查 §3，不将临时草稿作为后续研究唯一依据。随后写出独立 Fraction/整数 oracle，再读冻结正文，独立攻击新增格点前沿，最后只读规范代码；独立代码从未导入、调用或复制规范生成器/求解核心。首次审查并入稿的全文哈希为 `e4237516bca52cc60b8bd6a010590504306f4f8972548b7035d652e8e757b52c`；最终稿仅将“待冻结独立攻击登记”改成已完成的准确状态，数学内容不变。

## 2. 覆盖的精确身份

`UM-FROZEN-MACRO-TINY-REOPT-GAP-v1`：所有整数 r≥1，k=r(r+1)，2r 机、r(k+1) 任务的所给受限指派族；x 为 r² 个真实 OPT=1 调度的均匀平均；存在该 x 的真实 ST 槽输出 sigma，C=2−1/r，冻结 sigma 全部 macro 后、任意重开 tiny 的精确最优为 2r/(r+1)。任意固定 delta,epsilon∈(0,1)，可共同选 r 满足 tiny≤delta 且冻结值>2−epsilon。

`UM-MACRO-MIGRATION-FRONTIER-v1`：所有整数 0≤d≤r−1，允许至多 d 个 macro 最终机器与 sigma 不同、tiny 完全自由，令 s=r−d，则最优 makespan 为 ceil(2sk/(s+1))/k；允许至少 r−1 次改动时 OPT=1。对所有实 alpha∈[1,2)，M=floor(k alpha)，所需最少 macro 改动为 max(0,r−floor(M/(2k−M)))。实 alpha 是数学恒等量词，未虚称任意未编码实数可作为可计算算法输入。

## 3. 承重独立重构与攻击结果

1. **OPT 及凸分解。** 各显式分量全部 2r 台机器负载恰 1；单位 macro 强制 OPT≥1。轮转标签保证每 macro 的每 H 质量 1/r²、每 Q 质量 1/r；组选择保证 tiny 去 Z 概率 1/r。r=1 零 home-tiny 边已处理。给定平均点没有被升级为基本点/极点。
2. **真实槽边、任务身份及平局。** H 的 macro 总质量 1/r，sigma 的 macro 可取槽 0。keep tiny u=ar+b，1≤b≤r−1，可取槽 a(r−1)+b，区间减槽号的端点为 (1−b)/r 及 (r−b)/r，严格正交。Z 的 u=ar 可取槽 i(r+1)+a。覆盖每个带标签任务且槽互异；r=1 独立检查。这里只需存在这个匹配；没有把所有宏任务位置都写成坏态。每任务在所有有限端时间相同，故全部合法调度总成本恰 2r，这个匹配确也是最小总处理成本匹配。
3. **冻结后全局容量。** 全部 2r 工作只能使用 r 个 H 及 Z，平均下界为 2r/(r+1)；每组外送 2r 件 tiny 同时达到。此结论不依赖槽、逐行包络或负相关，重优化已可完全离开槽图。
4. **macro 移动计数。** C<2 时每个 H/Q 至多一个 macro，至多 d 次改动留下至少 s=r−d 个原 home 被 macro 阻塞。记 M=kC 为整数，则这些 home 共同至少挤出 s(2k−M) 件 tiny，Z 容量最多 M，给下界 M≥ceil(2sk/(s+1))。移 d 个 macro 到不同 Q、每个 blocked home 外送 2k−M_s 件，给实际达到。H 间换 macro、临时变化、跨组协调均不逃过最终态计数；C≥2 候选自动劣于显式达到态。
5. **格点和端点。** s≥1 保证 M_s≥k，k=r(r+1)、s≤r 保证 M_s<2k，所以外送数量合法。alpha≥1 保证 M≥k、2k−M>0 且 floor(M/(2k−M))≥1；可保留的 macro-home 数恰 min(r,floor(M/(2k−M)))，于是最少改动为正文式 (2)，不超过 r−1。alpha=1 给 r−1；r=1,d=0 一致。连续 floor(alpha/(2−alpha)) 仅为必要条件，正文正确另保留格点精确式。
6. **tiny 阈值与编码。** 任意 delta∈(0,1)，先选 r(r+1)≥1/delta，再增 r 满足 r+1>2/epsilon，仍有 tiny≤delta、macro=1>delta，存在量词顺序未反转。机器、任务、平均分解、匹配的显式长度均为 r 多项式，分母位长 O(log r)；没有把以 log r 为输入的指数展开伪称为多项式算法。

## 4. 实际独立核验范围

Python 3.12.14，Fraction 与整数，无浮点；命令为运行上述独立实现并将标准输出保存到新的 scratch 路径，不覆盖冻结结果。

- r=1,…,7 逐个展开全部 r² 个真实最优分量，重算实际负载及完整平均 x。
- r=1,…,20 按实际矩阵时间排序、逐项累加区间，核对显式槽注入；最大 8420 个带标签任务。
- r=1,2 直接枚举全部带标签任务实际分配，各 4、36864 个；求 OPT、冻结 macro 最优及每个 macro 改动预算的最优，并检查 C<2 的 macro-home 数必要界。
- r=1,…,4 独立枚举所有 tiny 组外送整数计数，数量 3、49、2197、194481；对所有 s=1,…,r 核对精确前沿；对 M=k,…,2k−1 全部整数阈值及每格两个有理 alpha 核对最少改动公式。
- tiny 阈值含 1/2、1/1000、999/1000 及极大分母 1/(10^100+3)，整数 isqrt 求最小 r 后反算阈值及前一 r 失败。

这些有限计算检查实现与边界，不承担全称证明；一般范围由 §3 独立重构给出。规范审计和独立审计的实现、参数与范围分别保留，不把二者混写成一次运行。

## 5. 价值、范围与剩余义务

新可复用信息是：无限制 tiny 联合重开不能弥补错误 macro 共同占位；取得固定改善须改动 r−O(1/epsilon) 个 macro，且有精确整数迁移前沿。这区别于只禁止逐坐标增载、固定行偏差或固定负相关；这里允许低负载接收机增加，甚至免费给 tiny 精确全局最优。

该族仍使用基本共享容量计数机制，全球新颖性及论文价值未经认证。它本身直接最优可解，不排任何可共同改动足够多 macro 的多项式算法，也不排选择其他 x/匹配。一般多源多目的地核心上的算法和统一收益仍未闭合，不得升格 `UM-TARGET-v1`。
