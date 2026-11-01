# 同客 reset 密度不变量：父方解析检查

2026-10-24。检查[精确候选](../global_credit_next/customer_density_reset_invariant.md)
的 INV/INIT/EDGE 合同及纯流结论。只审这个客户不重采版本，
不把旧标量重采流也纳入范围；未外审/新颖性认证，不证明 half。

固定实际并集 C 外的一个客户 x。source k 的库存 rho_k(x) 总和≤1，
每个 source 只在 k 以后角色注入，每条初始单边≤rho_k/c_receiver、
该 source 总注入≤rho_k。natural 节点规定动作覆盖 x；
每条 reset 正边原流 h_parent(x)/c_receiver，允许只减流，且当前分叉总流<h_parent。
角色严格上升。这些假设同时必要于所给证明，不能仅保留总库存条件而删去单边上限。

作者后续核对纠正了初始化的一个过宽援引：raw round7 坐标边一般只有
`a_ijx≤min(p_ix/(c_Y−1),1/c_Y)`，未必满足本稿所需的 `a_ijx≤p_ix/c_Y`。
因此本审查只认证明确 INV/INIT/EDGE 合同；raw round7 不免费适用。
owner INIT 或另有该强单边容量的子核才可直接接入。

对任意同一 receiver history s，其首次不同于 actual 的角色 k 唯一。
每个 natural parent reset 的前缀在其当前角色以前等于 actual，当前主题覆盖 x
而 actual 不覆盖 x，因此所有 parent 的角色恰为 k，reset 完成叶都等于同一 B_s。
初始 source 注入 s 也只能来自 k；否则首次偏离位置不同，不能是同一有序 history。

保留 source 标签后，每个 x 质量只沿角色递增的非增质量流行进。
所以角色 k 的所有 parent 输入之和≤sum_(q<k)rho_q(x)。source k 的原库存
尚未进入角色 k natural 节点，故此和与当前 source k 初始库存不重复计费。
共同分母给

\[
h_s(x)c_{B_s}(x)
\le\rho_k(x)+\sum_{t:role(t)=k,reset(t)=B_s}h_t(x)
\le\sum_{q\le k}\rho_q(x)\le1.
\]

这也处理一个 receiver 同时有初始注入和多个递归 parent 的情况。
各 parent 分叉不复制质量，但将这个结论变成 beta 时只对同一个 receiver
提取共同分母；不能把不同 receiver 的 beta 再相加仍声称≤1。

父方从这些合同独立重构，未发现纯 DENSITY/PREFIX-DENSITY 的 fatal objection。
其数学内容是非增质量 cut 与真实有序 history 的共同分母，不使用 SPE 的 IC。

本页没有重新独立审查所引用 whole-IC 退款核。只有在那些原核或另有合法
CLIP 证明时，beta_max≤1 才可和旧付款身份合用得到逐 context L_t≤u_role(t)。
任意删正边不自动保留该结论。更没有推出同一 actual 角色下所有 context
的费用总和≤其一份实际利润。共同钱包仍缺新的真实 IC 上界。
