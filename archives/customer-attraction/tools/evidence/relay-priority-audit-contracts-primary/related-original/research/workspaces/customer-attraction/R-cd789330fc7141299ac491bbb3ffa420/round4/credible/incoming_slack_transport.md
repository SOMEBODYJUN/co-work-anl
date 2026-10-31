# incoming 费用的 off-history IC 与 signed fresh 重置

2026-10-23，credible。一般工作稿，任意人数、任意共同目录、全部有序历史纯 SPE。relay 的[独立对稿审查](../relay/review_incoming_slack_transport.md)已逐式核对 OFF-IC、FRESH、tracked 一半界及 recipient IC 域通过；不称盲审。以下使用一条真实 off-history IC 给出跨叶约束；不声称已支付 K_in 或一般 half。其目的正是打开 [SOURCE-NET](../../round3/credible/owner_hybrid_transport.md) 尚未用过的真实后继激励，而不是另给已付 source 一份 u。

## 1. 自然 action-return 保留的额外见证

固定原实际叶 Z=(S_1,…,S_m)，实际覆盖 C，实际收益 u_i。对一个 actual-prefix 查询 s=(i,a)，记

    A=finish_sigma(Z_<i,a)，    D=u_i(A)，
    e=u_i−D≥0。

原递增捕获流的一项 incoming 来自某个更早查询的真实 rollout。在那个 rollout 上，角色 i 所选 a 是原 σ 在某真实历史 g（长度 i−1）的规定行动。记

    B=finish_sigma(g)，    sigma(g)=a，    v=u_i(B)，
    W=finish_sigma(g,S_i)，    v_S=u_i(W)，
    ell=v−v_S≥0。

ell 是这一个真实节点改选原实际主题 S_i 的原完整 IC slack。多个父历史可以进入同一 actual-prefix 查询；可按父来源线性拆 A_s 的分子和整体标量，然后相加回同一份 w_s。这不允许对 IC 按客户赋不同权。

**适用域承重。** 若把后续查询改为客户的 owner 主题 T_j，通常没有 sigma(g)=T_j，不能原样使用本节 ell≥0。自然 action-return 保留此 off-history 规定行动见证；owner-return 保留最优主题锚定。两者目前没有免费的统一替换。

## 2. 一条完整 off-IC 同时约束全部客户

记 c_P(x) 为 profile P 的总覆盖数。因 S_i⊆C，直接相加给

    e=T_C+T_fresh−ell，                           (OFF-IC)

其中

    T_C=Σ_(x∈S_i)[1/c_Z(x)−1/c_W(x)]
          +Σ_(x∈a∩C)[1/c_B(x)−1/c_A(x)]，
    T_fresh=Σ_(x∈a\C)[1/c_B(x)−1/c_A(x)]。

这些分母均正，因为求和客户由对应同一当前行动实际覆盖。证明仅是

    u_i−D=(u_i−v_S)+(v−D)−ell，

再按共同主题 S_i、a 分解。**OFF-IC 是整条真实 IC 的后果。** T_C 可正可负，ell 以负号保留；不能先把它们全部取正后又单独领取原收益预算。

fresh 包括实际遗漏 R=O\C，也包括 N\(C∪O) 的新 outside 客户。后者可能出现在离轨动作 a 中，绝不等于 actual G=C\O；若要用 owner Hall 运输，仍须保留各真实叶的实际库存。

## 3. fresh 重置只向更深 coverer 产生正角色项

固定 x∈a\C。原实际前缀不覆盖 x。写

    U={j>i:x∈A_j}，    V={j>i:x∈B_j}，
    b=|{j<i:x∈g_j}|，
    c_A=1+|U|，    c_B=b+1+|V|。

逐客户精确为

    1/c_B−1/c_A
      =[|U\V|−|V\U|−b]/(c_A c_B)。              (FRESH)

所以可把 signed 正项送到 A 中新增的未来 coverer U\V，负项留给 B 中消失的未来 coverer V\U 与 off-prefix 的 b 个旧覆盖者。所有新角色严格大于 i；没有把旧祖先删除后当成新 SPE。

对真正从父查询传来的一个 tracked R 客户 x，父查询当前玩家早于 i 且覆盖 x，所以 b≥1。对每个新增角色 j∈U\V，其费用

    1/(c_A c_B)=u_j(A;x)/c_B≤u_j(A;x)/2。         (TRACKED-HALF)

更一般，乘原状态非负整体系数 theta 后，对任一 recipient j，把所有 tracked 客户费用合计 H_j，再除其完整规定利润 v_j(A)，得到一项合法的整体系数 H_j/v_j(A)≤theta/2。v_j=0 时 H_j=0。这一步从完整真实叶 A 的未来节点购买原 IC，适用域合法。

购买方向仍是 (H_j/v_j) d_j(query)≤H_j，不能倒过来用新 query 价格上界 H_j。这里所证的是 H_j≤(theta/2)v_j 的同叶资金容量；尚未把该互斥叶的 v_j 接回 actual u_j。原 K_in 的费用不能据此宣称已下降。

**不是总体收缩。** TRACKED-HALF 是逐 recipient 角色的 whole-IC 系数界，不能将多个未来角色的 theta/2 相加后仍称总费用至多 theta/2；同一 recipient 若从多个互斥父叶接收，也尚未证明其共同容量。

relay 补充的一个可安全合并范围是**同一 actual-query s=(i,a)**：它的 A 固定。若不同父 g 的分拆系数为 theta_g，各自 tracked 集可以不同，则对同一 recipient j，

    Σ_g H_(j,g)≤(Σ_g theta_g)v_j(A)/2
               =w_s^in v_j(A)/2。

因此本节点内部的多个父来源不会额外破坏一半界。不同 s 或不同 A 仍是互斥真实叶，不能把它们的 v_j 当成一份 actual u_j。

## 4. 新库存广播与真正未付项

OFF-IC 必须保留 a 中全部 fresh 客户。对于非 tracked 的 x，off-prefix 可能 b=0，于是 TRACKED-HALF 的一半界不适用。它们分两类：

* x∈R：需要剩余 owner 客户库存，不能既作为原 source 全额注入，又为 off-IC 广播再领一单位。
* x∉C∪O：需由真实 Hall-A/B 送回 O 的缺口库存，不能借 actual G 名义免费支付。

而 T_C 中的多叶收益迁移也未被证明只使用一次 actual I/G。只有把这三类项、负 ell 及已有 gamma 的净库存同时耦合，才可能从 OFF-IC 控制 K_in。当前没有这种共同选择的证明。

若接 priority-threshold 终端，同一吸收 token x 的真实未来 x-coverer 都在其 owner 阈值以下，所以 FRESH 对这个 x 的正 recipient 可以安全标为低阈值。但整条 IC 的 theta_s=A_s/D_s 会广播到同 a 内其它客户 y；即便 y 也属于父 query 的 tracked 集、有 b_y≥1，也不保证 F_s(y) 在吸收 x 的 owner 阈值以下。故这里只得 diagonal x 的阈值标签，不能将所有 tracked 正项称为共同下降的 priority 链，更不能据此领取阶乘或总体收缩预算。

因此目前增加的是：自然 incoming 的 off-history 原 IC 见证、它对 actual slack 的完整约束、以及 tracked 正重置的严格未来/逐 recipient 一半容量。没有将它们当作已证 dynamic-cut 上界，也没有把新方程本身认作半覆盖进展。

## 5. 定义级核验

[独立 Fraction 代码](audit_incoming_slack_transport.py)只重放既存 86 客户匹配反例及 61 客户根税反例；先核原完整历史 30+1554 项 IC，再核 41 个 parent-context 的 OFF-IC 与 71 项 fresh signed 恒等式。没有找新游戏、扫描重数或修改原冻结证据。

这两个旧证书没有出现正的 tracked 新 recipient 项，所以不把其中零次数检查称为对非零 TRACKED-HALF 的经验支持。代码另核 c_A=3、c_B=2 的非零局部计数算术：两个 recipient 各 +1/6，旧前缀 −1/6，净 reset 为1/6，每个 recipient 比例恰1/2；这只是公式回归，不是一份游戏或 SPE 证书。普遍关系仍由第2—3节逐客户证明承担。[新输出](incoming_slack_exact_v2.json)保留这些范围，未覆盖初次运行记录。
