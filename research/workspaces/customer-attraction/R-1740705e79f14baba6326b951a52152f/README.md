# R-1740705e79f14baba6326b951a52152f 的个人研究工作区

研究存档：`customer-attraction`；发布身份：`R-1740705e79f14baba6326b951a52152f`。

## 当前问题

主目标 Q-CAG-HALF 仍研究任意有限共同目录、任意人数和全部完整历史依赖纯 SPE。当前路线从客户在极大主题间的关联超图出发，检查 routed maximal-theme / incidence-LP 动态预算以及真实后继之间的 cross-branch relay。

## 已保存资产

- [`representation/complete_pair_incidence_lp_obstruction.md`](representation/complete_pair_incidence_lp_obstruction.md)：完整 pair-incidence `K_s` 的精确 LP 对偶计算。它证明单偏离的极大关联 LP 在根节点即被 `B(m)=ms/2` 卡住，即使把比较对象换成精确 `OPT_m`；这只是证明接口 obstruction，不是低福利 SPE 或 Q-CAG 反例。
- 节点级 relay 恒等式已传给 Boss：若实际动作为 `A*`，任意强制 `T` 满足 `W(T)-W(A*) <= V(T)-V(A*)`，其中 `V` 是后继总福利；等价 harmonic-potential 增益全部来自后继树。缺口是不同有序历史的 `V` 无自然望远镜。
- [`route5a/sequential_deviation_share_lemma.md`](route5a/sequential_deviation_share_lemma.md)：全范围证明偏离份额下界 (L1)–(L3)，并给出后继主题包含于偏离主题时的同枝收益继承 (L4)；最坏分母在不交遗漏主题上只有调和量级，不能单独闭合 half。
- [`route3/smoothness_bridge_obstruction.md`](route3/smoothness_bridge_obstruction.md)：严格证明静态终局的 `(1,1)`-smoothness，并用完整三人 SPE 证书说明静态冻结偏离不能直接替代真实后继收益。
- [`representation/cross_branch_welfare_relay_identity.md`](representation/cross_branch_welfare_relay_identity.md)：把节点级 relay 写成福利式与删去当前玩家后的调和势式，明确未付项是互斥子树的后继势差。

## 当前判断与下一步

现有 LP 对每个客户类型只支付一次非负 incidence multiplier；对高密度 pair-incidence，它必须把所有 `s` 个端点都纳入预算。继续闭合一般命题需要第二层真实后继信用（例如跨端点 edge balancing、分支耦合或直接利用 m-theme cap），不能把该障碍扩大为原猜想失败。若继续探索，须保留全部有序历史和任意平局，并区分辅助模板失败与 Q-CAG-HALF 真反例。
