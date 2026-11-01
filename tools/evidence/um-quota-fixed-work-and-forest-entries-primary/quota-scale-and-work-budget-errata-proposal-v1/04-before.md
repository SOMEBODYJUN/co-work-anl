---
id: unrelated-machines/fixed-work-local-minimum-and-optimal-convex-slot-review
kind: review
title: 固定工作局部极小与真实凸包固定槽双源审查
status: complete-source-read-corrected-scope-integrated
truth_status: "one strict single-move local-minimum family plus one exact fixed-slot gap family; multi-round obstruction withdrawn"
scope: "fixed total-work potential local minimum and optimal-convex-hull standard-slot loss, including one-destination repair and minimum-work-face extensions"
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/current/unrelated_machines/fixed_work_convex_local_minimum_near_two.md
  - source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/current/unrelated_machines/fixed_work_convex_local_minimum_near_two.md
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/current/unrelated_machines/optimal_convex_fixed_slot_gap.md
  - source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/current/unrelated_machines/optimal_convex_fixed_slot_gap.md
source_ids:
  - 536f2637ce915451c9fe
  - 7ff5e8374a6b9826845c
inventory_sha256:
  536f2637ce915451c9fe: 36a2e934c25e0c3686a731c12bee5196b1b645f5fa2e1ca2dfab04b3eb9f4c9d
  7ff5e8374a6b9826845c: 37f9ae7920ff063c3cd6dcf331d974194bde2f3e5913c7ebc0a7e7e2db333e29
---

# 阅读范围与对象区分

本批完整读取 `fixed_work_convex_local_minimum_near_two.md` 与 `optimal_convex_fixed_slot_gap.md`，并回读其引用的审查、审计和经典 ST 槽舍入接口。两源都在完全相同机器或真实最优凸包的 unrelated-machines 子类中，研究局部修复与标准有序槽图的边界；它们都明确不是一般近二算法、复杂度困难性或六人 SPE 的证明。

第一源的身份为 `UM-FIXED-WORK-CONVEX-LOCAL-MINIMUM-v1`：固定总工作量使每个分配的总处理量相同，初态是二次负载势和降序负载词典序势的严格单任务局部极小，峰值比真实 OPT 趋近 2。正文已核实范围修正，撤回“最终大支持下界推出固定批量多轮失败”的外推；三件启动批次可严格下降并走到 OPT。第二源的身份为 `UM-OPTIMAL-CONVEX-ST-SLOT-GAP-v1`：分数点明确来自真实最优调度的均匀凸组合，但标准单位槽图的每个覆盖匹配都固定每台机器的任务数，峰值趋近 2；槽图外有精确多项式修复。正文还保留 `UM-ONE-DESTINATION-SLOT-REPAIR-v1` 和 `UM-MIN-WORK-FACE-SUPPORT-GAP-v1` 的派生边界，均须与主身份分开。

# 一、固定总工作量下的严格单任务局部极小

## 1. 实例、OPT 与近二比值

对每个整数 (m\ge3)，取 (m) 台完全相同机器、两件 unit 任务 (u_1,u_2)（每台处理时间 1）以及 (m^2-1) 件 tiny 任务（每台处理时间 (1/m)）。初态 (sigma^0) 把两个 unit 放在机器 0，把 tiny 均分到其余 (m-1) 台，每台 (m+1) 件，故
\[
L(\sigma^0)=(2,d,d,\ldots,d),\qquad d=1+1/m.
\]
所有完整分配的总工作量固定为
\[
W=2+(m^2-1)/m=m+2-1/m.
\]

真实最优峰值精确为 (1+2/m)。达到它的分配把两个 unit 分开，各自再放两件 tiny；其余 tiny 在其他机器上按 (m+1) 或 (m+2) 件分配。反向计数：若峰值严格小于 (1+2/m)，两个 unit 必须分开；两个 unit 机器各剩余容量严格小于 (2/m)，至多各放一件 tiny，其余 (m-2) 台至多各放 (m+1) 件，总 tiny 容量小于 (m^2-1)，矛盾。因此
\[
\operatorname{OPT}=1+2/m,qquad C_{\max}(\sigma^0)=2,qquad
C_{\max}(\sigma^0)/\operatorname{OPT}=2m/(m+2)\to2.
\]

## 2. 两种势的单任务局部极小

二次势 (Phi(sigma)=\sum_iL_i^2) 的三类单任务换机差值均严格为正：

* unit 从机器 0 移到 tiny 机器：((2,d)\mapsto(1,d+1))，(DeltaPhi=2/m)；
* tiny 从 tiny 机器移回机器 0：((d,2)\mapsto(d-1/m,2+1/m)=(1,2+1/m))，(DeltaPhi=2/m)；
* tiny 在两个非 0 机器之间移动：((d,d)\mapsto(d-1/m,d+1/m)=(1,1+2/m))，(DeltaPhi=2/m^2)。

把负载按非增序排列后，前两类把最大值升至 (2+1/m)；第三类保持首项 2，却把第二项从 (1+1/m) 升至 (1+2/m)。因此排序词典序也严格变差。该性质确实来自单任务邻域，而非总工作量势偏好：所有分配的 (W) 完全相同。

## 3. 一次大支持下界及已撤回的外推

对任意 (0<\varepsilon<1)，若最终峰值不超过 (2-\varepsilon)，两个 unit 必须分开，至少一个 unit 离开初始机器 0。接收该 unit 的机器原有 (m+1) 件 tiny，最终至多保留
\[
\lfloor m(1-\varepsilon)\rfloor=m-\lceil\varepsilon m\rceil
\]
件 tiny，所以至少 (1+\lceil\varepsilon m\rceil) 件 tiny 离开；连同 unit，直接从 (sigma^0) 一步到目标的 Hamming 支持至少 (2+\lceil\varepsilon m\rceil)。这只是一次重分配的支持下界。

正文曾把该下界外推为固定批量多轮严格下降的障碍；该语句已明确撤回。公屏反例给出三件启动批次：把一件 unit 从机器 0 移到 leaf，并把两件 tiny 反向移动，二次势差为 (-2(m-2)/m^2<0)，排序势也下降；随后沿 leaf 向其他机器逐件迁移 tiny，可在严格下降路径上达到 OPT。故本族仍可用于审查单任务局部搜索，但不能证明固定批量路径不存在，也不能冒充一般算法困难性。

## 4. 复杂度和边界

显式矩阵有 (m(m^2+1)=O(m^3)) 条目，每个数为 (O(log m)) 位；构造、局部动作和支持计数均按显式输入位长多项式完成。(m=2)、空任务、零处理时间和不可用边不属于本族；零 OPT 输入应单独选择零端。精确全局最小化二次势本身至少包含 PARTITION：两台机器总量 (W) 下，势为
\[
S^2+(W-S)^2=W^2/2+2(S-W/2)^2,
\]
判定能否达到 (W^2/2) 等价于找 (S=W/2)。这是对“把全局势最小化当免费子程序”的复杂度提醒，不是新的 (R\|C_{\max}) hardness。

# 二、真实最优凸包上的固定槽近二间隙

## 5. 精确构造与所有槽匹配的值

对每个 (m\ge2)，取 (m) 台完全相同机器、一个大任务 (b)（每台处理时间 1）和 (m^2-1) 个 tiny（每台处理时间 (1/(m+1))）。把 tiny 分成 (m-1) 组 (G_1,\ldots,G_{m-1})，每组 (m+1) 件。调度 (sigma^a) 把 (b) 给机器 (a)，并把 (G_r) 循环移位到其他机器；每台负载恰为 1，因此 (operatorname{OPT}=1)。均匀平均 (m) 个最优调度得到 (x_{ij}=1/m)，所以 (x) 明确位于真实最优整数调度凸包，而非仅在配置 LP 投影中。

每台机器的分数任务质量为 (m)，标准有序单位槽图因此恰有 (m) 个槽。任何覆盖全部 (m^2) 个任务的槽匹配都必须用尽所有槽，每台最终恰接 (m) 个任务。大任务所在机器还接 (m-1) 个 tiny，峰值精确为
\[
2m/(m+1)=2-2/(m+1),
\]
其他机器负载为 (m/(m+1))。任务平局如何排列不改变这个计数，且标准 Hall/增广匹配保证覆盖匹配存在。因此失败不是挑到了坏的槽匹配，而是固定槽图没有保留每台 (m+1) 件 tiny 的真实最优分量。

这给出 `UM-OPTIMAL-CONVEX-ST-SLOT-GAP-v1`：不存在统一 (\varepsilon>0)，使该固定槽接口在所有此类 (x) 上都能输出 ((2-\varepsilon)T) 覆盖匹配。它只约束固定槽图的输出空间；可直接输出已知的最优分量、重建 (x)、重新打开槽外边或允许迁移的算法均不受限。

## 6. 槽图外的精确修复和单目的地派生身份

给定任意槽匹配，移走大任务机上的 (m-1) 个 tiny，分别送到其他 (m-1) 台机器，即恢复 OPT=1，恰改变 (m-1) 件任务。它突破槽容量，因此不与槽图内重新匹配矛盾。

`UM-ONE-DESTINATION-SLOT-REPAIR-v1` 进一步要求每个源机器离开的原任务至多去一个外部目的地。大任务不动时，small 迁移功能图必须依次访问全部机器，最小 Hamming 距离精确为
\[
m(m-1)/2.
\]
若强制大任务搬走，最小距离为 (m(m+1)/2)。该派生身份保留一个正面同步路径：按路径逐批搬运原始 small 任务，第 (t) 批后的峰值为 ((2m-t)/(m+1))，每批严格下降，最后到 1；接收机可以增载，所以它不满足逐坐标负载非增合同。正文还提醒不能把所有合法修复都说成达到最小距离，例如 (m=3) 可有 Hamming 7 的合法循环修复。

## 7. 最小工作量面的更强支撑障碍

`UM-MIN-WORK-FACE-SUPPORT-GAP-v1` 是独立派生对象，不属于真实最优凸包身份。它取大任务在任机时间 (m)，每台 home 有 (m-1) 个小任务，home 时间 1、其他机器时间 (1+1/m)，令 (T=m+1/m)。在目标 (T) 的 assignment LP 上最小化总处理量 (W(x))，整个最优面都把所有 small 积分固定 home，只让大任务在机器间有正质量；每个最优点的正支撑都相同。任何只用该正支撑的整数分配峰值为 (2m-1)，而 OPT 恰 (m+1/m)，比值趋近 2，且 (T_{LST}=m) 与 OPT 比值趋近 1。

支撑面公式为
\[
W(x)=m^2+\frac1m S(x),
\]
其中 (S(x)) 是 small 离 home 的分数质量；最小面要求 (S=0)。大任务份额满足 (sum_i b_i=1) 且 (b_i\ge1/m^2>0)，所以打开整个最小工作量面仍不能引入跨机 small 边。源码给出 basic 点、active 等式满列秩和有限独立枚举。允许总工作量上升 (q) 后，至多 (q) 件 small 离 home 的最优峰值为
\[
\max\{2m-1-\min(q,m-1),\;m+1/m\};
\]
恢复 OPT 需要 (m-1) 件 small 离 home，说明该反例不应扩大为任意固定乘法成本松弛的反例。

# 三、证据、比较和接续义务

固定工作源的精确审计用 `Fraction` 检查构造、势差、排序势、支持下界并在 (m=3) 枚举全部分配；它验证列举参数，不能替代一般公式。已有公屏反驳和独立 Fraction 复核已经把多轮外推从正文真值中剔除。

固定槽源及其派生身份有规范和独立审计，核对最优凸分解、槽图、覆盖匹配、Hamming 修复和有限实例；这些证据支持精确计数与范围，不能把标准 ST 二倍上界变成新算法。源中引用的最小工作量经典 ST 例只承担背景和机制定位，未作全球新颖性认证。

两源共同说明：局部势、固定槽任务基数和最小工作量面支撑都可能丢失好整数调度，但三者的失败机制不同。固定工作族只排除单任务严格下降邻域；固定槽族排除同一单位槽图内的所有覆盖匹配；最小工作量族排除固定成本最优面正支撑的直接舍入。它们都允许通过多任务同步、接收机增载、重新打开槽外边、使用完整凸分解或改变目标函数来逃逸。

后续算法若想越过这些边界，应明确给出至少一项新机制：保留真实最优凸分解而非压成逐机槽基数、允许接收机负载上升并共同控制全局峰值、允许工作量有限增加并量化代价，或在新支撑上证明可构造的全局交换。不能把固定工作源已撤回的多轮障碍重新使用，也不能因给出一个槽外修复就声称固定槽接口已经可修复。两个来源均已准确归档；`UM-TARGET-v1` 与 SPE 目标继续开放。
