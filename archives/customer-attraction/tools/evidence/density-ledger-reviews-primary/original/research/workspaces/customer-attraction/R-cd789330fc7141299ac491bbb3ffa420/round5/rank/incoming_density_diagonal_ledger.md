# 自然 incoming 的整行密度账与全父子对角返还

2026-10-24，rank_transport。一般工作组件。第1—5节经 dynamic [盲重构](../dynamic/review_density_ledger_blind.md)及[对稿审查](../dynamic/review_density_ledger.md)，第6—7节经[补充独审](../dynamic/review_density_ledger_supplement.md)；通过的是所列恒等式、IC域、自然路由与合法充分归约，**没有共同总费用上界**。对象为任意人数、任意有限共同目录、每个完整有序历史上的纯 SPE；Q-CAG-HALF 仍 OPEN。本文不新造实例或扫描。它把 round4 的真实 off-history action-return IC 与原 fairshare 捕获流合并，新增全父子首项的精确共同账；仍未支付 actual-return 项与跨客户协方差。

## 1. 固定一份源、一份 actual 取消和原流

固定完整 SPE σ，实际终局 Z=(S_1,…,S_m)，实际收益 u_i、覆盖 C。固定最优 m 槽元组、owner 及**同一份** actual Hall-A 取消 γ，R=O\C、ρ_x=1−γ_x，M=Σ_Rρ_x。以下也可直接取任意固定 ρ_x∈[0,1]；除初始化外，不再领取任何 actual G。

使用 round3 的原自然 action-return/fairshare 流。状态 q=(k,a) 在原 actual 前缀下查询 a，真实叶 B_q=finish_σ(Z_{<k},a)。f_q(x)≥0 是客户 x∈R∩a 的总到达密度，含 source 与 incoming。因 actual 前缀不覆盖 R，写

    c_q(x)=1+|F_q(x)|,
    A_q=Σ_x f_q(x)/c_q(x),
    D_q=u_k(B_q),    w_q=A_q/D_q。

当前吸收 f_q(x)/c_q(x)，向每个 i∈F_q(x) 发同量。子动作是 B_{q,i}，角色严格递增。全流守恒给

    Σ_q A_q=M。                                      (ABS)

零量状态取 w=0。正量必有 D>0。所有查询仍是同一 σ 的原 actual-prefix 真实叶；这里没有把 B_q 后继作为重置后的规定后继。

## 2. 每条父子来源保留完整真实 context

一条父子来源 g=(q,i) 满足 i>k；令 b=B_{q,i}，s=(i,b) 是 reset 后状态，其实际前缀查询叶为 A_s=finish_σ(Z_{<i},b)。定义客户到达密度（在 b 外及 R 外补零）

    f_g(x)=1_(x∈b) f_q(x)/c_q(x)。

同一子 s 可有很多父来源 g，且 f_s^in=Σ_(g→s)f_g。这里的 g 还保留真正旧历史 h_g=(B_{q,1},…,B_{q,i−1})，在此历史原 σ 规定行动正好是 b。因此

    B_g=finish_σ(h_g)=B_q,
    W_g=finish_σ(h_g,S_i),
    v_g=u_i(B_g),    z_g=u_i(W_g),
    ℓ_g=v_g−z_g≥0                                  (OFF-IC)

是一条完整真实后继 IC。记 c_A(x)=c_x(A_s)，c_Bg(x)=c_x(B_g)。对 f_g(x)>0 的 tracked R 客户，父查询玩家 k<i 已覆盖 x，故 c_Bg(x)=c_q(x)≥2。

把子吸收按父来源线性分拆，取

    a_g=Σ_(x∈b) f_g(x)/c_A(x),
    θ_g=a_g/D_s,    D_s=u_i(A_s)。

于是 Σ_(g→s)θ_g=w_s^in。θ_g 是一个非负常数，只乘**完整** OFF-IC。不会对客户分别重权。D_s=0 时全部 a_g=0，可略去。

## 3. 精确密度水位式

在 b 上取概率 μ_s(x)=[1/c_A(x)]/D_s，定义 r_g(x)=c_A(x)/c_Bg(x)。其中 b 内分母均正。θ_g=E_μ f_g。再令

    T_g=θ_g(u_i−z_g),
    C_g=Σ_(x∈b)[θ_g−f_g(x)]/c_Bg(x)
       =−D_s Cov_μ(f_g,r_g)。

则有

    θ_g u_i = Σ_x f_g(x)/c_Bg(x)
               +T_g−θ_gℓ_g+C_g。                 (DENSITY)

证明：Σ_x f_g/c_Bg+C_g=θ_g v_g，而 v_g−ℓ_g=z_g。右端正好为 θ_g[v_g+u_i−z_g−ℓ_g]=θ_g u_i。协方差式来自

    D_s E_μ r_g=v_g,
    D_s E_μ(f_g r_g)=Σ_x f_g(x)/c_Bg(x)。

因此 DENSITY 也给一个真实 IC 后果

    θ_g u_i ≤ Σ_x f_g(x)/c_Bg(x)+T_g+C_g。        (DENSITY-IC)

这里 T_g 可正可负；不能把其负部丢掉后另外领取一份 actual I/G。C_g 是精确的跨客户广播账：低于水位 θ_g 的客户正领取 θ_g−f_g 的 B_g 份额，高于水位的客户偿还。其符号由 f_g 与 c_A/c_Bg 的相关性决定，不能默认非正。

与逐 recipient 一半界不同，第一项是完整当前 query 的一个**总现金**项。tracked 性给

    Σ_x f_g(x)/c_Bg(x) ≤ (1/2)Σ_x f_g(x)。        (TRACKED-DIAG)

这并不声称 θ_g u_i≤incoming/2，因为 T_g+C_g−θ_gℓ_g 仍在。

## 4. 全父子首项只用一次总源预算：M−H

定义

    H=Σ_qΣ_(x∈R∩a_q) f_q(x)/c_q(x)^2。

全父子来源共同求和给精确式

    Σ_gΣ_x f_g(x)/c_Bg(x)=M−H。                  (DIAGONAL)

证明：固定父 q 与客户 x，它向恰好 c_q(x)−1 位真实未来 coverer 发送 f_q(x)/c_q(x)。在每条这样的 g 中，B_g=B_q，故再乘 1/c_Bg(x)=1/c_q(x)。所有子来源的贡献恰为

    f_q(x)[c_q(x)−1]/c_q(x)^2
      =f_q(x)/c_q(x)−f_q(x)/c_q(x)^2。

对 q,x 求和，再用 ABS 即得 DIAGONAL。它不把 c−1 个 recipient 各自的一半界误求和为一半；也不把互斥 B_g 的整份利润看成多份 actual 钱。这里只有原一个父 q 的真实客户份额沿其原全部子出口分拆一次。

边界 c_q=1 时该父没有出口，等式两边均零。R 空、ρ 全零、空主题及空流均自动成立。

## 5. incoming 总费用的完整合并

令

    K^in=Σ_s u_i w_s^in,
    T=Σ_g T_g,    COV=Σ_g C_g,
    L=Σ_g θ_gℓ_g≥0。

由 DENSITY、DIAGONAL 得

    K^in=M−H+T+COV−L。                          (GLOBAL-IN)

若 K^src 是 source 吸收购买原 actual IC 的费用，则

    K^src+K^in−M=K^src−H+T+COV−L。              (GLOBAL-SLACK)

这是将真实内部 IC 接到原 TOTAL 费用的实际位置。源费用此前可由同一 actual Hall-A 取消预付；GLOBAL-IN 没有再使用那份 G。它保留非负内部 slack L 的有利负号，并保留 H 的共同对角返还。若后续能用**同一份** actual I/G 库存及路由选择控制 T+COV−L，便可进入整条 IC 总费用 ≤W 的充分桥。

目前没有该共同上界，故 GLOBAL-IN 不是 half 的新证明，也不能把 M−H 直接称为全部 incoming 已付。其新增内容是：全部自然 incoming 的 tracked 对角项可完整压成 M−H，不再遗留按 recipient 相加的歧义；真正跨客户广播精确压成 COV，与 actual-return T 分开。

本公式特定于原 fairshare 流和自然 action-return 的真父见证。若改用任意 owner-return、priority 路由、对某客户只选一个 future、或别的重新采样，需重新证明相应 DIAGONAL；不得把不同 context/不同流的首项和 COV 混用。

## 6. 保持同一整行账的 captured-mass 自然重分配

下面给出一个可直接证明的扩展，不再把等份出口视为必要。对每个 q,x，**当前吸收仍固定** f_q(x)/c_q(x)；对其真实 future coverer i∈F_q(x)，选任意非负出口 t_(q,i)(x)，只要求

    Σ_(i∈F_q(x)) t_(q,i)(x)
        =f_q(x)[c_q(x)−1]/c_q(x)。              (REDISTRIBUTE)

出口仍进入真实规定主题 B_{q,i}，并保留同一父 context h_(q,i)。允许将全部 captured mass 送给一个 future；不允许把当前吸收也一起改掉。F 为空时右端零。

此时每条父来源用 f_g(x)=t_(q,i)(x) 替代第2节的等份定义。ABS、DENSITY、TRACKED-DIAG 均保持。更关键的是固定父 q,x 后

    Σ_i f_(q,i)(x)/c_B(q,i)(x)
       =[Σ_i t_(q,i)(x)]/c_q(x)
       =f_q(x)[c_q(x)−1]/c_q(x)^2。

所以 DIAGONAL、GLOBAL-IN 与 GLOBAL-SLACK 完整保持。这里使用的只有总 captured mass 和所有真父 context 共享同一 B_q 负载，未使用各 recipient 等份。

这个扩展**不保留**原等份流的非owner HIT≤1/2、priority MARG-CAP 或相应旧 owner-势折扣。一个客户可以把大于一半的 mass 送到同一 future；这些接口必须另证。本文只将其用于总质量、完整原 IC 及实际一次取消的 TOTAL 充分桥。

### 固定实例的自然总价格可按严格角色逆推

对每个合法状态 s=(i,a)、x∈R∩a，记单位到达量在上述重分配族中的最小实际总费用为 V_s(x)。其 current 整行费用对来源线性分拆为

    u_i/[D_s c_s(x)]。

因角色严格递增，有限逆推给精确 Bellman 式

    V_s(x)=u_i/[D_s c_s(x)]
            +[c_s(x)−1]/c_s(x)
                 ·min_(j∈F_s(x))V_(j,B_sj)(x)，   (NATURAL-BELLMAN)

其中 c_s=1 时第二项为零，不取空集最小值。选择一个达到最小值的真实 future，把全部 captured mass 发给它，即同时达到该单位源的最小价格。对不同来源的最优规则可以固定为同一个状态/客户决策；总成本是源质量的非负线性函数，所以并行合流不破坏 Bellman 最优性。最终 IC 系数仍是所有来源相加后的唯一 A_s/D_s，不是按客户重权原 IC。

原完整 actual IC 给 u_i≥D_s。由严格角色归纳，V_s(x)≥1：当 c=1 直接成立；c>1 时右端至少1/c+(c−1)/c=1。

固定同一个 matching/owner 后，初始化价格 v_x=V_(o(x),T_o(x))(x)。actual Hall-A 的 Γ、rank、GREEDY 与 TOTAL 消元可原样应用，因为源到总费用仍线性；没有扩大或复制 actual 取消。故这一自然重分配族的**最小总费用**精确为

    min_(γ∈Γ)Σ_x(1−γ_x)v_x
      =∫_0^∞ [|{x:v_x≥t}|−r({x:v_x≥t})]dt。

与原固定等份路由相比，v_x 只会下降。本文仍未证明该积分≤W；新增的是保留真实后继 IC 与 M−H 共同账时，一类可解析优化的自然路由自由。它真正接到主证明的 TOTAL 付款步，不能把“成本下降”本身称作动态 Hall cut 已支付。

## 7. 完全放弃逐行钱包后，纯总费用允许任意比较源删减

这是一个与 actual Hall-A 支付不同的弱化，须单独命名为 **TOTAL-TRIM**。令 r=|R|、g=|G|。因为最优覆盖不小于实际覆盖，r≥g，且

    r−g=OPT−W。

若只需要总费用 K≤W，而不再保留逐行 η、SOURCE-NET 或 actual I/G 运输，那么可以任取

    0≤γ_x≤1，Σ_Rγ_x=g，ρ_x=1−γ_x。

它只是从比较覆盖中删除 g 单位源，使所需证明的总源量为 OPT−W；这里 γ **不是一份 actual G 运输证书**。任何合法守恒 IC 流仍给

    OPT−W=Σ_xρ_x=总吸收≤K(ρ)。

因此若找到任意这种 trim 与流满足 K(ρ)≤W，依然闭合 half。actual 收益 K 的右端逐项只使用原 u_i；没有在任何分支重新领取 actual 退款。删掉 g 个比较源是目标 R≤I+2G 中左移一份 G 的代数，不能同时宣称由它得到了旧 η_i 的逐行钱包。

固定任一源到付款的非负线性路由，记单位价格 v_x≥1。TOTAL-TRIM 的最优值为

    min_(0≤γ≤1,Σγ=g)Σ_x(1−γ_x)v_x
      =sum of the r−g smallest prices v_x
      =∫_0^∞ (|{x:v_x≥t}|−g)_+ dt。             (TRIM-PRICE)

证明：把 γ 全放在最高价的 g 个客户即可；g 为整数，积分表达由嵌套价格层逐层相加直接得到。空集与 r=g 时值零；相同价格任意平局不影响值。也可以写成

    OPT−W+∫_1^∞ (|{x:v_x≥t}|−g)_+dt。

因此新的纯总价充分桥是

    sum of the r−g lowest natural prices ≤W。    (TOTAL-TRIM?)

它尚未证明。它弱于同一固定路由、固定 owner 的原 Hall 限制 TOTAL，因为原 Γ 是这里 trim 集的子集；相应地原 r_Hall(S)≤min(g,|S|)，故原层 cut 缺额至少 (|S|−g)_+。这个弱化没有给任意 γ 补出合法 actual 运输，也不继承先前已付 source 的结论。若未来仍需要逐行 η 或 COV 的 actual 网络支付，必须保留原 Γ；不能把任意 trim 与原 source 预付的好处相加。


### 来源核对补充

root随后实读同行[自由起点/总钱包审查](../../../R-b6d636d360e14c11aeb4b76415ed422b/direction_review/continuation_general_scope/incoming_payment.md)§四式(5)–(6)与seq217，发现其已明确写出自由κ价格及任意净源删减。同类自由trim不计本轮新发现；本页保留自然重分配与M−H整行账的自足衔接。两者都没有普遍费用上界，不再以第二个最短路/静态LP作为新推进。
