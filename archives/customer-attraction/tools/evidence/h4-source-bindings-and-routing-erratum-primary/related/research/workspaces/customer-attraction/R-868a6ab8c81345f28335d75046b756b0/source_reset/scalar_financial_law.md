# 完整 query 收益的 scalar 金融账，不等价于逐客户覆盖

2026-10-24。个人一般推导与精确接口审计，未独立外审。任意人数、任意有限共同目录、每个完整有序历史纯 SPE；单位客户与单位提供者。**Q-CAG-HALF 仍 OPEN。** 本文没有得到新的全输入共同预算上界。新增核查是：旧 `generalized_child_routing.md` 写出的 coordinatewise query-cover LP 虽然独立充分，却不是 `w=A/D` scalar flow 的等价投影。下面保留完整 D 中的已覆盖客户信用，给正确的金融/流接口，避免把这个修复误认成 incoming 已付。

## 1. 实际前缀查询与完整收益

固定完整纯 SPE σ，实际路径 S、覆盖 C、各角色收益 u_i。固定一个最优 m 元组，其并集 O；记 R=O\C、G=C\O，δ=OPT−W=|R|−|G|。实际位置 i 强制合法主题 a 后沿原 σ 的真实叶为 Z_i(a)，完整当前收益为 D_i(a)。原 IC 给 D_i(a)≤u_i。

对 x∈R∩a 写 r_(i,a,x)=1/c_x(Z_i(a))。由于实际前缀不覆盖 R，r=1/(1+未来 coverer 数)，严格正。查询 D 包括 a 的全部客户，不能只保留 R 贡献。

任一合法递增角色流，对状态 s=(i,a,x) 设总到达 f_s≥0，吸收 a_s=r_s f_s；送往任意更晚、包含 x 的查询的总流为 (1−r_s)f_s。源质量 q_x 只初始化一次。有限角色 DAG 守恒给

    Σ_(s属于x) a_s=q_x。

对 query row q=(i,a) 聚合 A_q=Σ_(x∈R∩a)a_(q,x)。定义唯一整行 IC 乘子

    w_q=A_q/D_q  (A_q=0 时取 0)。

正 A 必有正 D。由完整原行的 IC，恰有

    Σ_x q_x=Σ_q A_q=Σ_q w_qD_q≤Σ_q w_qu_i=:K。
                                                        (FINANCE)

这是合法的固定实例 scalar 金融账。D 中 I/G 等客户的真实 query 收益用于降低共同系数 w；没有给每个客户分别购买一份 IC。若额外证明 K≤W，才得到目标净缺口 δ≤W。

一个明确的“完整 D 信用”分拆为：记 D_q^R=Σ_(x∈R∩a)r_(q,x)，D_q^C=D_q−D_q^R≥0，则

    Σ_(x∈R∩a) [f_(q,x)−w_q] r_(q,x)=w_qD_q^C。
                                                        (COLLATERAL)

即 scalar 账允许一行中 tracked R 密度超过共同水位 w 的总价差，由同一真实 query 的非 R 利润一次抵押。右侧已经进入 A=wD，不能另当成新增 actual 现金重复领取。COLLATERAL 是逐行恒等式，不是跨叶预算定理。

## 2. 为什么旧 coordinatewise LP 不是同一接口

来源：`R-b28b3013e6464e70862b4993359a6964/cross_tree/generalized_child_routing.md`。该文确实写了 “Equivalently, forgetting the flow decomposition … query-cover LP”，并写 “The flow is one constructive way to satisfy the covering inequalities …”。其 LP 要求

    Σ_(i,a:x∈a) w_(i,a) r_(i,a,x)≥1  (x∈R)。       (COORD)

COORD 本身是正确充分条件：对 x 求和后，Σ_xΣ_qw_qr_qx≤Σ_qw_qD_q，再用原 IC 即可。问题仅在声称 scalar flow 的 w=A/D 自动满足 COORD；FINANCE 只保存总吸收，没有保存这个逐坐标不等式。旧更早的 `increasing_role_capture_flow.md` §3 已明确说“此处不声称 w 逐客户支配流入”，这点才是正确接口。

最简合法例为 m=1，A={p,q,z}、B={p,q,x}，共同目录 {A,B}，σ选 A。两行动大小都是 3，所以这是完整纯 SPE；取最优 B，则 R={x}、G={z}。唯一 B-source 吸收 1，D=3，w=1/3，金融费用 wu=1，但坐标覆盖 wr=1/3<1。

为避免仅依赖 δ=0 边界，下面独审父方给出的 **δ=1 全参数完整两人族**。令 common 为 t≥0 个单位客户，A=common∪{a_1,a_2}，B=common∪{x}，共同目录 {A,B}。根选 A，第二人在 A 或 B 后都选 A。记 u=(t+2)/2。

| 历史 | 规定行动、规定当前收益 | 另一行动、当前收益 |
| --- | --- | --- |
| 根 | A，u | B，u |
| A 后 | A，u | B，u |
| B 后 | A，(t+4)/2 | B，(t+1)/2 |

表的逐项计算为：根 A 的真实 AA 利润为 (t+2)/2；根 B 的真实 BA 利润为 1+t/2；A 后选 B 的利润也为 1+t/2；B 后选 A 的利润为 2+t/2。最后一行的严格优势恒为 3/2，其余行平局。以上列全全部三个决策历史，故对每个整数 t≥0 都是完整纯 SPE，包括 t=0。

实际 AA，W=t+2、各角色收益 u；最优 AB 覆盖 t+3，R={x}、G=0、δ=1。把遗漏客户初始化在 (1,B)；其真实叶 BA 中没有未来覆盖 x，故 r=1、D_1(B)=u、A_abs=1、w=1/u。于是

    总吸收=1，scalar 金融费用=1，COORD 覆盖=1/u=2/(t+2)。

所有 B rows 的 r 都是 1、D=u；A rows 不含遗漏客户，故独立 coordinate LP 的最低费用为 u=(t+2)/2。scalar 流最低费用恰为 1：上面流程达到 1，反向归纳或 ρ≥1 加总吸收 1 给下界 1。因此两接口最优值的比为 (t+2)/2，无界。t=0 时比为 1，t≥1 时严格分离。完整 D 中 t 个已覆盖交集客户贡献的 t/2 单位 query 利润，正是损失的 collateral。此族始终满足 2W≥OPT，不是 half 反例。

这只否定旧文的等价/自动映射，不否定 COORD 的独立充分性。族与比值由父方提出，本子组独立核全历史收益、t=0 边界及两个优化值；不认领构造发现。`interface_audit.py` 仅在 t=0 与 t=7 用 Fraction 从集合回放边界算术，不导入旧作者实现，不把参数采样当一般证明。

若需要一个由任意 flow 自动生成的 COORD 证书，可用 λ_q=max_x f_(q,x) 代替 w_q，则 Σ_qλ_qr_qx≥q_x。一般 λ_qD_q≥A_q，故它可能比 scalar 系数贵。把 λ 偷换回 A/D 正好丢失 COLLATERAL。

## 3. 任意-child 的正确保留完整 D 的价格

设 ρ_(i,a)=u_i/D_i(a)；有正 tracked 客户的查询必有 D>0，完整 SPE 下 ρ≥1。对单位 x 到达状态 s=(i,a,x)，当前金融费用是 ρ_s r_s；剩余质量只能送往严格更晚的位置。允许全部 remaining mass 送到任意合法更晚 query（无需属于旧叶 coverer），则精确最小价格为

    V_s(x)=ρ_s r_s +(1−r_s) min_(j>i,b∋x)V_(j,b,x)。 (ARB)

r_s=1 时第二项按零计。对 i 反向归纳：固定当前吸收后，余量线性，分流不能优于最低价孩子，选择最低价孩子达到右侧。这一证明不调用任何被重置旧叶的内部 IC。自由起点价格 κ_x=min_sV_s(x)，所以给定 q 的最小金融费用恰为 Σ_xq_xκ_x；所有客户的最优流可以最后聚合为唯一 query 行系数 A_q/D_q，仍满足 FINANCE。

ARB 扩大了 `free_start_capture_prices.md` 的“孩子位置必须为旧 F 的角色、动作自由”接口；也扩大了 rank 稿 natural-Bellman 的“孩子必须旧 F 且沿旧规定动作”接口。只可声称价格不升，不能声称它自动满足总钱包。自然父见证的 OFF-IC 和 `GLOBAL-IN=M−H+T+COV−L` 依赖旧叶规定行动与共享负载； arbitrary-child 不继承该式。

正确的线性流金融法是：变量 z_s 为一次源注入，e_st 为合法递增边流，f_s=z_s+Σ_te_ts；Σ_te_st=(1−r_s)f_s；Σ_sz_s=q_x；目标 min Σ_sρ_sr_sf_s。每个客户独立，系数固定，故 ARB 是该 flow LP 的精确求值，不是 COORD 的投影。

其固定 q 的价格对偶可写为：对每个 x 取势 φ_s 和自由起点下界 k_x，要求

    φ_s≤ρ_sr_s+(1−r_s)φ_t  (每个合法 child t)，
    φ_s≤ρ_s               (r_s=1)，
    k_x≤φ_s               (每个 x-state s)。

最大化 Σ_xq_xk_x。反向归纳的最大势恰为 V，k=κ；源/流金融式给弱对偶，递推实现给强对偶。这里保留完整 D；它既不重复领取 u_i，也不产生新的普遍 κ 上界。

## 4. 本轮预算研究的准确停止点

只用总钱包并放弃 Hall-η 合同，可自由保留 δ 单位 R 质量；最小费是 δ 个最低 ARB 价格之和。这是旧 TOTAL-TRIM/KAPPA 接口在更宽路由族下的合法值改进。还须证明对某个最优 O 该和≤W，才能共同支付全部 incoming。

本轮没有找到这一全输入新不等式。SOURCE-NET 仅付同一实际 γ/f/η 下的初始化；不能与任意自由 trim 混用。自然 incoming 的 M−H 是已存在、真正共用总源的一项关系，但 T/COV−L 未付。把它们改名为 dual deficit、IC tax 或重置债没有改变承重缺口，因此不作为新结果。

## 来源

- `R-b28b3013e6464e70862b4993359a6964/cross_tree/source_fractional_matching.md`、`generalized_child_routing.md`。
- `R-cd789330fc7141299ac491bbb3ffa420/round3/credible/increasing_role_capture_flow.md`、`owner_hybrid_transport.md`。
- `R-3d2531ded15f453daef73b30eef82940/transport/free_start_capture_prices.md`。
- `R-cd789330fc7141299ac491bbb3ffa420/round5/rank/incoming_density_diagonal_ledger.md`。
- `R-b6d636d360e14c11aeb4b76415ed422b/direction_review/continuation_general_scope/incoming_payment.md`。

以上来源路径均相对 `research/workspaces/customer-attraction/`。未声称 ARB/dual 表示有全球新颖性；本次价值是修正 scalar 与 coordinate 接口的错误合并，并准确保留未付预算。
