# 同客户传播的全图密度上界：加强初始化与同角色父节点反链

2026-10-24，inventory8。任意有限共同目录、任意人数及每份完整历史依赖纯 SPE。**Q-CAG-HALF 仍 OPEN。** 本文给一般输入上的来源保持组件，不给共同实际钱包上界。空主题、重复主题及任意历史平局均保留。

Natural reset 始终是 `A_t=finish_sigma(B_<i,sigma_i(g))`，其中 B 是原实际叶；绝不是 `finish_sigma(g,B_i)`。许多不同 off-history 父节点可以合并到同一 reset 叶，本文允许合并。关键是同一**非实际目标 context**的全部父节点处在同一角色，因此在固定客户质量流中构成反链。

本地客户保持核已经见于 [peer 最大客户密度核 §2](../../../R-d3981c0168644971803a9c3380ed687c/next_general/credible/coordinate_support_attack.md)，本文不重新认作新核。新增候选组件是：加强 round7 全 O 初始化边界后，该核在全部实际生成的非实际 context 都满足逐客户利润密度不超过1。因此各 context 的 whole-IC 系数可以统一取1。**不同 context 同一角色的系数之和仍未控制。**

## 1. 更强初始化子容量保留原 current/future 总额

固定原完整策略 sigma、实际叶 B、实际利润 u_i，以及任意比较元组 T、并集 O；取最优时才使用 |O|=OPT。沿用 [round7 坐标初始化](../../round7/parent/optimal_coordinate_initialization.md)：对 x∈T_i，

    p_ix=1/c_T(x), d_ix=c_B(x)+1−1_(x∈B_i),
    W_i=finish_sigma(B_<i,T_i),
    r_ix=p_ix−P^B_ix≥0.

保留原全部 P^B 支付，记其 actual 列为 H_l。每条原 future 正边 j>i、x∈(W_i)_j\B_j 的子容量可进一步收紧为

    qhat_ijx=min(p_ix,1/d_ix)/c_Wi(x)
             ≤1/[d_ix c_Wi(x)].                    (NEW-CAP)

这特别要求每条初始化输出满足

    c_Wi(x) a_ijx≤p_ix.                            (INIT-DENSITY)

证明这仍允许原 current 总额。固定 (i,x)，缩写

    t=c_T(x), d=d_ix, w=c_Wi(x),
    nB=|{l:x∈B_l\T_l}|,
    n=|{j>i:x∈(W_i)_j\B_j}|,
    nMinus=|{j>i:x∈B_j\(W_i)_j}|.

因为 W_i 在 i 以前与 B 相同，w=d+n−nMinus。置 k=d−nB。若 x∈B_i，k=|B_x∩T_x|；否则 k=1+|B_x∩T_x|，共同 coverer 不含 i。故

    1≤k≤min(d,t),    r_ix=k/(td),
    qhat_ix=n min(d,t)/(tdw).

于是

    k w−n min(d,t)
      =kd−k nMinus+n[k−min(d,t)]≤kd≤td,

即 `(r_ix−qhat_ix)_+≤1/w`。先求和，之后只用实际节点 i 的一次完整合法偏离：

    Σ_x(r_ix−qhat_ix)_+≤u_i(W_i)≤u_i.             (INIT-WHOLE-IC)

故 b_i=(r_i−u_i)_+、r_i=Σ_xr_ix 仍不超过 `S_i=Σ_x min(r_ix,qhat_ix)`。若 S_i>0，取

    a_ix=(b_i/S_i) min(r_ix,qhat_ix),

否则全零；再按 qhat_ijx 比例分到各 j。则

    p_ix=P^B_ix+c_ix+Σ_j>i a_ijx,
    c_ix=r_ix−a_ix≥0,
    d_i=Σ_xc_ix=min(r_i,u_i)≤u_i,
    Σ_j>i a_ijx=a_ix≤p_ix.

H、d_i、b_i 与原初始化相同；只改变逐客户剪枝。每条边仍为原正边子容量。这里没有逐客户使用 IC。
