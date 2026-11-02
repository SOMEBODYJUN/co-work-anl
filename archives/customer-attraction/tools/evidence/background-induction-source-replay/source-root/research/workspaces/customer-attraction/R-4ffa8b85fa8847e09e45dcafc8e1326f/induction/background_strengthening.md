# 背景半覆盖候选与精确归纳缺口

2026-10-24。探索稿；下面代数恒等式已直接推导，背景候选未证明。

## 状态和候选

固定任意合法有序前缀 h，客户前缀负载为 b，尚余 r 位玩家，固定此子局的一份完整历史依赖纯 SPE。前缀覆盖 P={x:b_x>0}，给定子局的实际完整终局总覆盖为 W_h，活跃 r 位玩家的最终收益总和为 V_h。定义

    C*_h = max_(T_1,...,T_r in S) |P union T_1 union ... union T_r|.

候选背景加强是

    C*_h <= W_h + V_h.                       (BG-HALF?)

若实际剩余玩家新增覆盖为 Delta_h，活跃玩家在 P 上取得的总份额为 F_old，则

    W_h=|P|+Delta_h,  V_h=Delta_h+F_old.

故同一候选等价于

    max_(r themes) |union T_j minus P| <= 2 Delta_h+F_old.

空背景时正是 Q-CAG-HALF。r=1 成立：末位真实最佳回复收益至少任何合法主题在 P 外的新客户数；因此 C*_h-W_h<=V_h。事实上末位节点的松弛至少为本步新增覆盖数，因为 C*_h<=|P|+V_h。

## 逐步归纳没有闭合

令 A 是 h 处的真实规定主题，hA 是其孩子，u 是当前玩家在原完整终局的收益。两节点沿同一路径，故

    W_h=W_(hA),  V_h=u+V_(hA).

定义真实子局松弛

    Q(h)=W_h+V_h-C*_h,
    delta(h)=C*_h-C*_(hA)>=0.

则对任何路径、无需均衡条件，精确有

    Q(h)=Q(hA)+u-delta(h).                   (ID)

只调用孩子 Q(hA)>=0 会要求 delta(h)<=u；这恰是已被
`research/current/customer_attraction/coverage_opportunity_counterexample.md`
否定的逐期覆盖机会收费，不能声称新的背景状态自动让归纳成立。

换成剩余新增覆盖 L_r(P)=C*_h-|P| 也不能消除这个缺口。若 d=|A minus P|，则

    L_r(P)-L_(r-1)(P union A)=delta(h)+d.

表面上“多出 d”的桥 `L_r-L_child<=u+d` 仍严格等价于旧桥 delta<=u。此前消息中一度把它当成不同局部条件，已即时纠正。

真正所需的是在存在负漂移时证明

    Q(hA) >= delta(h)-u,

并且这条信用必须由真实完整后继理性和根的全部合法偏离共同产生。这里没有把它提升为已证引理，也没有把终局当静态 Nash。

## 对八个已有实例的定点检查

运行 `check_background_old_examples.py`。对每个旧实例，规范全集求解器返回每个合法计数前缀可由某份完整历史纯 SPE 实现的全部终局；共享计数缓存没有强制完整策略匿名。检查所有这些 (前缀,终局) 上的 BG-HALF?。

| 旧实例 | 检查点数 | 最小 Q(h) |
| --- | ---: | ---: |
| coverage_opportunity_failure | 54 | 1 |
| tax_bridge_failure | 24 | 1 |
| prefix_balance_failure | 108 | 5/4 |
| individual_security_failure | 94 | 61/6 |
| root_tax_failure | 167 | 0 |
| global_decorrelation_failure | 117 | 12 |
| general_tax_failure | 98 | 0 |
| residual_counterexample | 24 | 3 |

合计 686 点。这只表明这八个已有反例没有否定背景候选；没有证明一般 BG-HALF?，没有证明任意新实例，更没有把有限证据当一般主目标进展。

## 未继续的候选

探索中曾提出 `m max_T |T minus U_actual|<=W`。Root 及时指出已由现存十四客户、两人残余反例否定（W=9，遗漏主题含五客户）。没有重复生成或把这个辅助反例称为 Q 反例。

Extra-one 个体安全值 `u>=v_(r+1)(b)` 的门槛尾部表述也与已有 Mfull 活跃义务重复；本轮没有把重述当进展。
