# 单核 signed overload 的接口审查：两种弱化已被旧完整 SPE 排除

2026-10-22。承接同工作区 `kernel/single_kernel_chronological_budget.md`（写作时先核对其定义级脚本）。本页是旧反例向新变量的精确转译，不声称发现新 SPE 反例。一般 Q-CAG-HALF 仍 OPEN。

## 1. 当前一般式没有被反驳

单核真正保留的恒等式为

    Cov = W + chi + D - A,
    A = S+B+C+O/m >= 0,
    0 <= chi <= W.

因此所需一般预算为 `D <= A+(W-chi)`。这和 half 经恒等式等价，尚需额外真实 SPE 约束证明。本页两例均不反驳它。

本次直接审查的对象是希望简化该 signed overload 的两种支付：选一个有利 OPT 排列使 `D<=A`；或丢弃 actual-only 客户、改用去重添加查询 `R_add<=W`。两者均已有完整原模型反例，不应继续列为 OPEN。

## 2. 存在有利排列也不能保证 D<=A

来源是 Boss2 的 [14客户 PFR-OPT 反例](../../R-64201cd12083425899e2d643ec9bc087/next_boss/partition_attack/optimal_partition_counterexample.md)。该例完整 SPE 实际为 AB，两个主题不交，各收益4，W=8；唯一 OPT 支持为互不交的 T,S，OPT=10。

在任意比较排列中，每个最优客户只有一个 source，故 kernel 最后 source owner 的冻结替换收费为

    R_last = sum_(x in OPT) 1/[c_x+1-z_(i*(x))(x)] = Cov-chi.

原 PFR-OPT 的任意分派比 last-owner 更宽；既然该例所有分派、所有匹配都收9，last-owner 必然也是9。故两种 OPT 排列均有

    chi=1,  D-A=Cov-W-chi=1.

独立逐客户重建真实偏离得到更精确值 `S=B=C=O=0, A=0, D=1`。根改 T 后真实回复 Q、根改 S 后真实回复 R；它们分别稀释该 root source 中两名已被实际 A 覆盖的客户。两种有利重排都不能删除这1单位 signed overload。

这严格否定“每个完整 SPE 存在一个 OPT 多重集及排列，使 D<=A”。不是仅否定某个 aligned 排列。真正预算仍有 `W-chi=7`，本例 half 余量为6。

## 3. 丢弃 actual-only 客户后，去重添加也不够

来源是旧 Boss5 的 [最优遗漏反例及解析族](../../R-171cd7d518434f36a48cd50df29c9303/global/optimal_omission_exchange_counterexample.md)。对每个 k>=3，已有完整二人 SPE 实际 AB，不交且收益分别 `6k-2,7k-2`，所以

    W=13k-4, OPT=14k-4,
    U=|OPT\actual|=14k-6,
    G=|actual\OPT|=13k-6.

唯一 OPT 支持为不交 T,Q；两个最优客户已被实际 B 覆盖，其他最优客户均未实际覆盖。两个 OPT 排列直接代入新 kernel 给出

    chi=1/2,  A=0,  D=k-1/2,
    R_last=14k-9/2,   R_last-W=k-1/2.

这里正 D 完全来自 root source 在真实离轨回复 R 或 S 中被再次 hit 的 `2k-1` 名原未覆盖客户：每人贡献1/2。当前两条真实节点的 slack 均为零，因而不能把该正债写成已经存在的真实 slack。

若为避免删除实际当前覆盖，改成去重添加收费，则

    R_add=sum_(x in OPT) 1/(c_x+1)=U+2/2=14k-5,
    R_add-W=k-1>0.

k=3 即71客户原例：`W35, OPT38, chi1/2, D5/2, A0, R_last75/2, R_add37`。因此 `R_add<=W` 也失败；问题不是只能给 last-owner 换个匹配。

对添加收费有一般恒等式

    R_add=Cov-sum_(x in OPT∩actual) c_x/(c_x+1).

它丢弃了 actual-only 客户的根信用。上族 `G=13k-6` 很大，保留 U-G=OPT-W 才是实际净覆盖缺口。不能把整个 U 或 R_add 交给 W 支付，再据失败放弃真正 half。

## 4. 仍可用的边界与下一步

真正全终局税 `tau_full=sum_(c_x>0)c_x/(c_x+1)` 在这两个原 SPE 中没有失败。14客户例 `W+tau_full-OPT=2`；上族 `tau_full=W/2`，所以余量为 `(11k/2)-2>0`。本页不声称该一般税桥成立，只说明这些反例不能排除它。

结合 [真实交换审查](signed_history_exchange.md)，不能通过同计数历史匿名化把 D 删掉，也不能仅要求它由 A 支付。下一次应保持单核原来完整容量 `W-chi`，同时用真实中继节点约束正 D；尤其应针对上述 zero-slack 族说明实际覆盖中哪部分源/汇容量支付该正债。若最终只利用 `D-A=Cov-W-chi` 重排，则仍只是 half 同义式。

`audit_kernel_interfaces.py` 不导入单核实现，从显式单位客户类型和完整二人策略独立重建所有真实节点、全部主题对、唯一最优性及上表参数；`kernel_interface_audit.json`记录本轮运行。一般失败身份继承上述旧资产，当前工作仅认证其向新接口的转译，避免重复攻击已失败的桥。
