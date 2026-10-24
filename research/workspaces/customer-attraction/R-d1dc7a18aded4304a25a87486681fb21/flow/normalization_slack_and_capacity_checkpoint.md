# 自然 context 归一化退款的精确含义：一般探索检查点

2026-10-24，global_flow。对象始终为一般有限共同目录、任意人数和全部有序历史纯 SPE。**本页没有新的半覆盖福利下界，也没有支付 actual 多来源共同容量；Q-CAG-HALF 仍 OPEN。** 下面第2—4节是直接代数推导，未另行独立审查。其用途仅是区分一个可用的路由控制和真实 off-history IC 的新增约束。

## 1. 已读接口及准确停点

本轮读了根四入口、CAG-MODEL、一般证明稿、本题状态与失败地图，另读：

- `R-cd789.../round5/credible/all_fresh_submarkov_elimination.md`；
- `R-cd789.../round6/credible/safe_coupon_netting.md`；
- `R-cd789.../round6/relay/global_role_coupon_hitting.md`；
- `R-3d253.../transport/free_start_capture_prices.md`；
- `extreme_maximal_membership_floor.md` 和 `R-7c3db.../relay/actual_marked_relay.md`。

SAFE、CLIP、全角色集合命中界、KAPPA?、末偏离剥离树与标记净债都属于既有接口，本页不重新认领。未得到能把它们的同一 actual 钱包多来源容量闭合的新不等式。

## 2. 一般非负吸收行

固定既有全客户 SAFE 图中的一个 natural context。记原完整规定利润为 `v>0`，全部正 recipient 原价为 `q_j>=0`，总量 `P=sum_j q_j<v`。future recipient 是真实更深 context；past recipient 是 actual 终端钱包。SAFE 后当前角色的净金额为

    L=v-P=u_i-N-e>0。

对任意输入利润质量 h，原行按 `beta=h/v` 支付当前 `beta L`，并向 recipient j 送 `beta q_j`，总量恰为 h。

取任意数

    0<=chi<L,

改用

    nu=v-chi,
    beta_chi=h/nu,

并把额外负项 chi 留在当前同一整行账中。新的非负行是

    当前吸收：h(L-chi)/(v-chi)，
    recipient j：h q_j/(v-chi)。                 (R)

各项非负且和为 h；future 仍严格增加角色，past 仍只通 actual 终点。它对应精确账

    h=beta_chi[u_i+P^< -N-e-chi]

加上匹配 future 出入的望远镜，不能同时保留原 beta 的退款或旧 coupon 负载。

**这里的代数并不需要 chi<=ell，也不需要使用 off-history IC。** 任意满足 chi<L 的数都给同一类合法非负归一化。因此只在这一公式中选择 `chi<=ell`，尚不能声称 off-history IC 提供了一份新库存或付款。真正利用 ell 必须另有一个把它与 source、路由或共同 wallet 联系起来的约束。

端点 chi=L 也可代数取到：若 P>0，则 nu=P，当前吸收为零且全部质量送往 recipient；若 P=0，端点 nu=0 不允许。为避免零分母，上文仅使用开端点。P=0 时任何合法 chi<L 都仍把全部 h 留给当前，实际终端付款完全不变。

## 3. 任意终端价格下的精确敏感度

给当前 actual 钱包一个非负价格 z_i，固定各 recipient 的后续每单位最小/指定费用 C_j。past 终点取它的 actual 角色价格，future C_j 是其严格更深延续费用。只改变本节点 chi，其单位输入费用为

    C_i(chi)=[z_i(L-chi)+sum_j q_j C_j]/(v-chi)。

直接求导得

    C_i'(chi)=sum_j q_j(C_j-z_i)/(v-chi)^2。       (S)

符号与 chi 无关。因此，在其余后续选择固定时：

- recipient 的 q 加权平均费用小于当前价格时，增加 chi 降低该价格目标；
- recipient 的 q 加权平均费用大于当前价格时，增加 chi 提高该价格目标；
- 两者相等时，该目标不变。

若允许闭紧区间 `0<=chi<=bar_chi<L`，最优 chi 必在某个端点，或全区间同值。多个 future 的后续控制也允许优化时，可从末角色反向使用这个端点规则；它只是给定终端价格下的路由优化，不是 actual 共同容量的证明。

特别取全部终端价格为1，各后续费用均为1，(S)恒为0且每单位输入费用恒为1。无论怎样选择 chi，同一批来源的总终端净金额都等于其总质量；此控制不能单靠质量守恒推出来源总质量<=W或<=2W。

## 4. 与 off-history IC 矩形的区别

记当前 off-history 为 g、其规定动作 a、actual 当前动作 S_i。四叶为

    B=finish(g,a)， A=finish(actual_<i,a)，
    V=finish(g,S_i)， Z=actual。

原两条真实 IC 给

    v_B>=v_V， u_i>=D_A，
    v_B+u_i-v_V-D_A=ell+e>=0。                 (RECT)

RECT 是两条既有 IC 的合法和，未新增真值。对于 fresh 客户，V 和 Z 的当前动作 S_i 没有 fresh 收益；但 RECT 仍不提供 `v_B<=actual wallet` 的上界。把 ell 命名为退款而只做第2节的分母缩小，并没有改变这个方向。

目前没有找到能用 RECT、共同目录的其它合法偏离，或标记中继，把多个同角色来源共同压到同一份 u_i 的一般关系。此为本轮实际未完成点。

## 5. 其它探索的状态

曾暂提“存在一个最优 m 元组，其均匀实际真偏离满足 `sum_i E D_i>=OPT/2`”。父方指出均匀最优实际偏离已有 `R-a409.../restore_attack/` 的 UR-gap 和 `R-64201.../independent_attack/` 来源；未把这视为新发现，未运行有限扫描或提升真值。既有遗漏匹配反例不直接否定 OPT/2 版本，但本轮没有给该版本新增证明或反例。

当前保存仅为可恢复的探索检查点。下一步仍应直接找能控制同一 actual 共同容量的新全输入关系；不以归一化重编码、其它固定角色例或无目标有限扫描冒充一般推进。
