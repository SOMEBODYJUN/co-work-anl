# 全树证书探索：最优前缀 hybrid 账本与准确停界

2026-10-25。研究对象为一般 Q-CAG-HALF：任意有限单位客户、有限共同目录、任意人数及每份完整有序历史纯 SPE；允许空主题、重复选择和全部平局。**本轮无新付款、无新 Claim，主目标仍 OPEN。** 未运行新的数值实例搜索，未执行 Git 或外部消息操作。

本轮读取根 `AGENTS.md`、目标与模型、`general_half_proof.md`、`strategy_cone.md`、`security_cone_duality.md`、`coverage_moment_geometry.md` 及相关跨枝账本。以下只是检查过的精确 hybrid 递推，作用与已有 BG/relay 重合，不另计一般证明推进。

## 固定最优元组的真实 hybrid

固定同一份完整纯 SPE σ，及任意合法比较元组 `(T_1,…,T_m)`。令 `z_i` 为先强制前 i 位选择 `(T_1,…,T_i)`，余下玩家沿原 σ 的完整终局；`z_0` 是原根实际终局，`z_m` 为比较元组。记 `O=W(z_m)`、`W=W(z_0)`，并定义

\[
\Delta_{i,j}=u_j(z_i)-u_j(z_{i-1}),\qquad
\gamma_i=u_i(z_{i-1})-u_i(z_i)\ge0.
\]

这里 `z_{i-1}` 是有序历史 `(T_1,…,T_{i-1})` 下的原 σ rollout，所以 γ_i 非负恰来自该真实节点的一步偏离约束；后继并未冻结。利润守恒逐次给

\[
 W(z_i)-W(z_{i-1})
 =\sum_{j<i}\Delta_{i,j}+\sum_{j>i}\Delta_{i,j}-\gamma_i.
\tag{H1}
\]

从 i=1 到 m 求和是精确恒等式

\[
 O-W=\sum_i\sum_{j\ne i}\Delta_{i,j}-\sum_i\gamma_i.
\tag{H2}
\]

其中固定旧位 j 的全部后来 reset 只可望远镜为

\[
 \sum_{i>j}\Delta_{i,j}=u_j(z_m)-u_j(z_j).
\tag{H3}
\]

`u_j(z_j)` 是强制最优前缀后的真实叶收益；它既不是原根 `u_j(z_0)`，也未由原根利润单独支付。故 H2 不能把这些互斥分支的信用免费相加到 W。即使每项 γ_i≥0，也没有得到控制右侧 reset 总量的共同容量。

## 查重与停界

- [现行最优首动作分支缺口 BG](../../../../current/customer_attraction/optimal_first_action_branch_gap.md)已按覆盖最优补全把同类 reset 细分为真实孩子损失和非负信用。
- [已纠正的全节点 relay](../../R-1740705e79f14baba6326b951a52152f/representation/cross_branch_welfare_relay_identity.md)的 `R1-v2` 已包含 H1 中不可遗漏的旧玩家利润变化；只保留后继利润变化不合法。
- [一般证明工作稿](../../../../current/customer_attraction/general_half_proof.md) §§3.2、6、7 已准确保留跨枝共同支付未完成的身份。

H1—H3 没有新增非负金额或统一不变量，因此不另立 Claim、不扩展有限规模检查。直接代入 m=5 仍只得同样的恒等式，**不能无条件推出 `OPT_5≤2W`**。需要一条真正控制所有旧位及后继 reset 的新共同支付，或采用其他一般机制；本轮没有获得它。
