# Return-IC 接续尝试：未得到新的共同资金上界

2026-10-24。本页仅保留本分支后续探索；不把标准逐客户恒等式或 Jensen 观察登记为 Q-CAG-HALF 的新正向进展。一般目标、共同 ROLE 预算及 m=5 无条件 half 仍 OPEN。

固定原 SPE、actual B、角色 k，以及任意该角色真实有序 history g。写

    V=finish_sigma(g),
    U=finish_sigma(g,B_k),
    v=u_k(V), r=u_k(U), u=u_k(B), e=v−r>=0.

此处 U 是在旧 history g 改回实际动作 B_k 的真实 return 叶，绝不是 actual-prefix reset。对 x∈B_k，b_x=c_B(x)、z_x=c_U(x) 均正。定义

    P=Σ_(x∈B_k) Σ_(j≠k:x∈B_j\U_j)1/(b_x z_x),
    N=Σ_(x∈B_k) Σ_(j≠k:x∈U_j\B_j)1/(b_x z_x).

逐客户分母差给 r=u+P−N，故真实 off-history IC 精确给

    v=u+P−N+e,   e>=0.                       (RETURN-LEDGER)

把 return 叶 U 重置到 actual B 时，P 的出口全部是 actual 客户券；保留 current r−P=u−N>0（对非空 B_k）。如果输入为 αv 并把额外 αe 留当前，则同一输入可表示为 actual 客户出口 αP 和角色 k 当前金额 α(u−N+e)。但 e 是正成本；要将当前金额压在 αu 内，仍须 e<=N，真实 IC 本身没有给这个方向。若 B_k 为空，则代数上 u=r=P=N=0；原SPE中只要目录有非空主题，任何实际玩家都可偏离获得至少该主题大小除以m，故不可能有空的实际 B_k。全零主题情形所有量均为0。

对多个同角色 contexts 取 α_t>=0，只得到

    Σ_t α_t v_t=(Σ_tα_t)u+Σ_tα_tP_t−Σ_tα_tN_t+Σ_tα_te_t.

不能把 u 在每个 t 免费花一次。若 Σα_t>1，共同资金超额项仍须由同一次来源和实际券的合法净返还控制；单枝 N 或 P 无论非负与否都未给此共同控制。

一个确实成立的跨 history 凸性观察是：M=Σα_t>0 时，令 Z_x=Σα_t c_(U_t)(x)>0，则

    Σ_tα_t v_t >= Σ_tα_t r_t >= Σ_(x∈B_k) M²/Z_x.

右侧由每个 x 的 Cauchy/Jensen 得到，所有 histories 共用同一实际动作 B_k，保留其真实 return 分母。但目前没有将此**收益下界**接到 R-current 或 source-price 的所需**资金上界**；不能把方向反转，也不声称它填补 ROLE。

后续有价值的接续应直接给完整 SPE 下的共同 inequality，控制 (Σα−1)u、Σαe 与 actual 券过载，或另选一个确实不重复预算的机制。本文没有找到它，不建议继续机械增加来源细化。
