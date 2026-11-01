# R-1740705e79f14baba6326b951a52152f 的个人研究工作区

研究存档：`customer-attraction`；发布身份：`R-1740705e79f14baba6326b951a52152f`。

## 当前问题

主目标 Q-CAG-HALF 仍研究任意有限共同目录、任意人数和全部完整历史依赖纯 SPE。当前路线从客户在极大主题间的关联超图出发，检查 routed maximal-theme / incidence-LP 动态预算以及真实后继之间的 cross-branch relay。

## 已保存资产

- [`representation/complete_pair_incidence_lp_obstruction.md`](representation/complete_pair_incidence_lp_obstruction.md)：完整 pair-incidence `K_s` 的精确 LP 对偶计算。它证明单偏离的极大关联 LP 在根节点即被 `B(m)=ms/2` 卡住，即使把比较对象换成精确 `OPT_m`；这只是证明接口 obstruction，不是低福利 SPE 或 Q-CAG 反例。
- relay 初稿已勘误：一般节点的准确式为 `ΔW=ΔV+ΔP_old−Γ≤ΔV+ΔP_old`；只有根或另证旧玩家总利润不增时可丢 P。删去当前人的 harmonic 势仍保留旧玩家，不能称纯后继势。根式及通用调和式仍成立，跨枝共同付款未闭合；见[勘误](../R-cef41b80a6e048b5a395b738d3b0b6e7/harmonic/relay_erratum.md)。
- [`route5a/sequential_deviation_share_lemma.md`](route5a/sequential_deviation_share_lemma.md)：全范围证明偏离份额下界 (L1)–(L3)，并给出后继主题包含于偏离主题时的同枝收益继承 (L4)；最坏分母在不交遗漏主题上只有调和量级，不能单独闭合 half。2026-10-24 已修 §4：遗漏半额条件的所述账本只给 OPT≤3W；修正充分接口须支付 OPT−W，并保留实际覆盖中最优并集外的信用。L1--L4 不变，见稿内勘误与独立审查链接。
- [`route3/smoothness_bridge_obstruction.md`](route3/smoothness_bridge_obstruction.md)：严格证明静态终局的 `(1,1)`-smoothness，并用完整三人 SPE 证书说明静态冻结偏离不能直接替代真实后继收益。
- [`representation/cross_branch_welfare_relay_identity.md`](representation/cross_branch_welfare_relay_identity.md)：修正版节点福利式保留旧玩家返还，根式为特例；删去当前人的调和势保留其他全部玩家，互斥子树的共同付款仍未证。
- [`route1/potential_branch_obstruction.md`](route1/potential_branch_obstruction.md)：精确写出 (u_i=\Phi(z)-\Phi(z^{-i}))，并用 43 个历史、215 个偏离的完整 SPE 证书否定“每个 SPE 分支都逐点增大调和势”的自然归纳；见证本身 (W=\operatorname{OPT}_3=4)，不是主命题反例。

## 当前判断与下一步

现有 LP 对每个客户类型只支付一次非负 incidence multiplier；对高密度 pair-incidence，它必须把所有 `s` 个端点都纳入预算。继续闭合一般命题需要第二层真实后继信用（例如跨端点 edge balancing、分支耦合或直接利用 m-theme cap），不能把该障碍扩大为原猜想失败。若继续探索，须保留全部有序历史和任意平局，并区分辅助模板失败与 Q-CAG-HALF 真反例。
