# 接 round8 密度界后的跨 action 付款尝试

2026-10-24，residual。固定任意有限单位客户、共同有限目录、任意人数和每份全部有序历史纯 SPE。**Q-CAG-HALF 与 FRESH-RESIDUAL 仍 OPEN。** 本次没有新共同付款定理或残余容量反例。以下是接到新组件后的实际推导与准确停止点，不是重新证明库存或密度界。

## 1. 新输入已经解决的部分

已实读同行 `R-cd789330fc7141299ac491bbb3ffa420/round8/inventory/source_preserving_density_envelope.md` 和 `round8/GENERAL_PROOF_WORKING.md`。NEW-CAP 可保留同一 d、H、各行 future 总量；客户保持核在全部非实际 context 有 f_sx≤1。同一目标的父节点可以很多，证明依靠同角色质量反链，而不是唯一父节点。**支持保持、初始密度及每 context 一次 whole-IC 已不是缺口。**

I-future 按新 a_ix 重算 J 后直接付清。只保留 R 客户进入同客户图；其余量为

    Q_l=2u_l−d_l−H_l−J_l。

本次试图证明同一角色全部 current 的合计≤Q_l，没有再为单节点合法性领一次进展。

## 2. 同 action 推导与去重

先取所有共同 future 边全满的 uniform-reset 角点。对 s=(g,l)，其规定动作 a，reset 叶 A_a=finish(B_<l,a)；R current 精确为

    A_s=Σ_(x∈a∩R) h_sx/c_Aa(x)。

固定角色 l 的全部同客户质量路径构成反链，所以

    Σ_(s:role l)h_sx≤A_x^init:=Σ_i a_ix≤1。

同一 action a 的所有历史可以在 IC 前合并。置 H_ax=Σ_(s:role l,action a)h_sx，则

    Σ_(s:action a)A_s
      =Σ_xH_ax/c_Aa(x)
      ≤(max_xH_ax)D_a≤(max_xH_ax)u_l，
    D_a=u_l(A_a)。

root随后指出准确去重入口；已实读 `round8/residual/common_action_reset_deduplication.md` 与 `round3/credible/increasing_role_capture_flow.md`。上式是旧按 (l,a,x) 状态压缩捕获流的独立重构，**不是新组件或新 Claim**。旧总吸收/完整 query 收益标量还可能比 max 密度收费更便宜。

真正的跨 action 量为

    A_l=Σ_a Σ_xH_ax/c_Aa(x)。

逐客户 Σ_aH_ax≤1 不给 Σ_a max_xH_ax≤1；不能为不同 a 各领一份 u_l。共同边全满把 raw current 向未来移，但没有消除这条跨 action 付款义务。

## 3. 尝试把真实 ell 接到便宜的 query 标量

为避免用 max 密度作浪费上界，对每个旧自然 context s 定义

    θ_s=A_s/D_a，
    V_s=finish(g)， v_s=u_l(V_s)，
    W_s=finish(g,B_l)， z_s=u_l(W_s)， ell_s=v_s−z_s≥0，
    e_a=u_l−D_a≥0。

D_a=0 时 A_s=0 并取 θ_s=0。所有未到达客户 h_sx=0；求和仍包括 action a 的完整客户集，不能只保留 R 后将 IC 逐客户加权。

置

    C_s=Σ_(x∈a)(θ_s−h_sx)/c_Vs(x)，
    T_s=θ_s(u_l−z_s)。

直接展开得

    θ_su_l
      =Σ_x h_sx/c_Vs(x)+C_s+T_s−θ_sell_s，

所以同一角色的真实 current 为

    A_l=Σ_sΣ_x h_sx/c_Vs(x)
        +Σ_s[C_s+T_s−θ_sell_s−θ_se_a]。          (ROLE-TRY)

这里确实使用了 g 上改实际主题 B_l 的真实 off-history IC，而非把 actual-prefix IC 再写一次。所有正 incoming R 客户在 V_s 中已有较早 coverer，因此首项可按 tracked 对角项处理。但是本式与已读 round5/rank 的 DENSITY/GLOBAL-IN 是同机制的角色分组，**不新认领一般关系**。

新 f≤1 限制 h_sx≤1/c_Vs(x)，但没有给括号总和非正或≤Q_l减首项：

- T_s 中 z_s 是不同旧历史的真实返回叶利润，不是一份共享 actual u_l；
- C_s 是不同客户请求与旧/新负载比的协方差项，f≤1 没有固定其符号；
- 保留 −θ_s ell_s 和 −θ_s e_a 是必要的，但它们尚未支配同一角色全部正 T_s+C_s。

固定同一 action 时可以先合并 current，θ 的合计也相应合并；不同 action 的 D_a、reset 叶和 h 支持不同，上式没有产生合法的跨 action 抵销。

## 4. 全目录 IC 的下一步未闭合

进一步尝试在每个 g 上将规定 a 与全部其它最优源主题 T_i 比较。它们确实可看见 R，而返回 B_l 只看 C：

    v_s≥u_l(finish(g,T_i))。

然而这些完成叶保留旧首偏离又加新查询。要用其早期角色利润共同支付 ROLE-TRY 的正项，必须处理其强制未来，不能把它们当 actual-prefix 或旧角色 prescribed 利润。本次没有得到可与 NEW-CAP 同一来源库存、同一 J 和同一剩余钱包兼容的抵销式。

因此目前没有一条已落实的 cross-action IC 承重步可继续迭代。准确交接是：新密度组件已消去支持保持问题；同 action 历史压缩是旧机制；真正还需证明 ROLE-TRY 的跨 action signed 正项共同付清，或绕开此式取得另一条总福利关系。本次停止在这条已知缺口，不扩展任意注入、纯 policy 反例或固定人数扫描。
