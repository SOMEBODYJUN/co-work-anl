# 七极大、六人缺口的精确盘点（research4）

日期：2026-10-27。本文只整理已有冻结资产并记录一次独立行集诊断；不把有限 LP 或逐席松弛升级为 Q-CAG-HALF-6 结论。

## 结论边界

至多六个包含极大的覆盖集已经由 `research/current/customer_attraction/six_maxima_joint_bound.md` 完整证明 `U<=2W`（n>=5），并覆盖六人目标中所有这类目录。恰七个极大集、六名提供者是当前最小未闭合结构；七个以上极大集仍然包含该缺口。目标仍然是原模型的所有有序历史依赖纯 SPE，而不是静态均衡、松弛菜单或有限搜索。

`evidence/certificates/customer_attraction/seven_maxima_partial_checkpoint.tar.gz` 的 n=6 扫描将七极大问题按完整有序根路径的 restricted-growth route 与六集比较目标 K 分轨。总轨道 877；已有 833 个基础树证书，45 个轨道没有最终非负证书（现行数学地图将其记作缺 44，扫描记录另含一个重复/边界计数）。失败目标只出现在 K=123、125、126，分别对应六集 K 漏去标签 2、1、0。其余 K/route 组合有冻结树证书或不在缺口集合。

失败列表（route: K）为：

```text
000010:125
000101:125,126   000102:123
000110:125,126   000120:123
001001:125,126   001010:125,126
001101:125,126   001102:123
001110:125,126   001111:125
001120:126       001210:126       001220:126
010001:125,126   010010:125,126   010021:125
010101:125,126   010110:125,126   010201:125
011001:125,126   011010:125,126   011101:126
011110:125,126   011210:126       011221:123
012001:125       012021:125       012110:126
012120:126       012121:123       012201:125
012210:126
```

这些是方法轨道缺口，不能解释成目标反例；失败 LP 的最优值仍接近半覆盖，且没有完整策略/客户实例。

## 独立诊断

重构了 `history/source/notes/customer_attraction/seven_maxima_checkpoint_2026-10-10/independent_seat_audit.py` 的列语义：每个 route 只允许前六位真实成员出现在该位置路由覆盖的极大集，末位成员由最终极大行动精确决定；K 的列目标是 `W-|O_K|/2`。这正是 route-conditioned 必要不等式的完整压缩域，不是任意历史枚举。

对首个失败轨道 `(0,0,0,0,1,0), K=125`，用 Fraction 重建合法基础行 `M_t`（混合保底）、`L_j`（真实末位最佳回复）和 `T_{jk}`（真实末两人税），并加入现有 `worst`、`H`、`profit` 行族做浮点 LP 仅作诊断；最优客户列余量仍为负，约为 `-0.00337`（加入 worst+H），所以这些已知行不能闭合该轨道。ASR aggregate-seat 候选（`research/workspaces/customer-attraction/R-c99d11e5cc394080a36a00845811d71a/aggregate_seat_row_candidate.md`）在首批缺口同样没有正余量。

逐席 `seat(t,j,k)` 行不能使用：完整 SPE 反例是七个互不相交极大主题，B0 有6个私有客户、其余各1个，所有历史都选B0；根实际收益为1，而逐席 k=1 行要求该收益至少6。该实例 `W=6, OPT_6=11`，仍满足主目标，只否定逐席 LP 行。

## 后续义务

要闭合七极大 n=6，必须找到新的真实跨枝共同付款，或把合法 order-statistic/aggregate-seat 行与末位 BR、末两人税和 route 条件组合成逐列有理证书。不能把逐席 seat、非法固定 owner 排序、有限无反例或接近半的负余量称作目标结果。若新构造走“实际最终极大集 + 六个最优极大集”的七集接口，需特别处理 K 漏去最终标签 0 的情形；这正是失败轨道 126 的集中位置。

一个可缩小缺口的定义级事实是：若目标最优六元组为 `K={B_1,...,B_6}`，且实际最终极大行动为外部的 `B_0`，则最终动作覆盖 `B_0` 的全部客户。因此

```text
O_K ∩ B_0 ⊆ C_actual,
D := O_K \ C_actual ⊆ O_K \ B_0.
```

所以每个实际遗漏目标客户的七极大 incidence 不含 0，只落在六个目标极大集内。对 `D` 做 routed/mixed 六集预算时，任何被路由到 `B_0` 的动作都不覆盖 `D`；但仅对 `D` 的六集系数仍不足以支付 `O_K∩C_actual`，必须和实际覆盖份额、末位最佳响应或新的共同跨枝付款合并。这是缩小证明义务的接口，不是半覆盖结论。

## 复现入口

```text
evidence/certificates/customer_attraction/seven_maxima_partial_checkpoint.tar.gz
history/source/notes/customer_attraction/seven_maxima_checkpoint_2026-10-10/independent_seat_audit.py
research/workspaces/customer-attraction/R-c99d11e5cc394080a36a00845811d71a/aggregate_seat_row_candidate.md
research/workspaces/customer-attraction/R-c99d11e5cc394080a36a00845811d71a/diagnostics/solve7_n6_invalid_lp.py
```
