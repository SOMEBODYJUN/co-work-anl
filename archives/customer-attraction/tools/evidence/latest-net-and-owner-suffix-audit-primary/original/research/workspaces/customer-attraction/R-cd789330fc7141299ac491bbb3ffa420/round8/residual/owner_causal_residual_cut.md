# 原 full-SAFE 剩余容量的 owner 后缀必要条件

2026-10-24，residual8。一般模型：有限单位客户、有限非空共同目录、任意人数、每份完整有序历史纯 SPE，含任意平局、空主题、重复和零源。**Q-CAG-HALF 及原 RESIDUAL-CAP 仍 OPEN。** 本页不是新增福利界。

## 同一初始化的路由无关必要条件

沿用 [坐标初始化](../../round7/parent/optimal_coordinate_initialization.md)，固定同一个实际叶 B、比较元组 T 和第一正价列 H。对每个比较角色 i，剩余库存 r_i 分为 current d_i 与 future b_i，故

    r_i=d_i+b_i,   |O|=sum_i(r_i+H_i).

最大 current 的特定选择为 d_i=min(r_i,u_i)，但下面只需 d_i+b_i=r_i。原 full-SAFE/合法 CLIP 的 [源因果合同](../../round7/parent/source_order_reconstruction.md) 给：owner i 的 future 源最终只能付给实际角色 j>=i。客户重采不破坏这个时间合同；它不是同客户券支持。

因此，对每个后缀 S_k={k,...,m}，原角色剩余 cap 若成立，必有

    sum_(i>=k)(r_i+H_i) <= 2 sum_(j>=k)u_j.             (SUFFIX-NEC)

证明：b(S_k)<=Aout(S_k)<=2u(S_k)-d(S_k)-H(S_k)，再代入 b+d=r。来自更早 owner 的流还可能额外落在后缀，故不能把第一处不等式改为等式。

这个 cut 独立于坐标比例和后续路由。它只必要，不充分。k=1 正好是 |O|<=2W，不能把整组 cut 的存在性作为已证的新全输入不等式。k=m 可由末位 r_m<=queryprofit<=u_m 与 H_m<=u_m 得到。

原存在性允许共同选择最优 T；一个坏排列不否定它。如果同一实例的全部最优元组均被 proper suffix cut 排除，才否定原限制路由 RESIDUAL-CAP，仍不否定 HALF。

## 一次固定完整策略锥的定向攻击

[脚本](attack_suffix_inventory.py) 仅用既有 root_tax_failure 的完整策略：四人、六主题、actual=(A,A,A,F)。变量为全部63个非空兴趣类型的非负客户质量；保留全部1295条非自身真实 IC。全部126个无序四主题组合的覆盖行要求固定多重集 ABCD 最优。

对每个 proper suffix，LP 要求 ABCD 的24个排列在同一个客户向量上全部有 cut violation>=z，最大化 z，并归一化客户总质量为1。这是对精确一般候选的有限攻击，不生成随机策略或扩展规模。

[冻结输出](suffix_inventory_cone_attack.json)：suffix 起点2、3、4的数值最优值分别约为 -1/7、-1/7、-21/148；有理化返回点满足全部输入行，其最小 cut 值亦为这些负数。没有正分离者。未重构精确对偶，故只报告数值求解器未分离，不升格为整个策略锥的精确定理；更不证明一般 cut 或 HALF。不继续扩样。

## 接口限制

peer [I-future 直接实际补余](../../../R-d3981c0168644971803a9c3380ed687c/next_general/global_credit/coordinate_residual_attack.md) 能合法付到 owner 之前的 coverer，故本 cut 不适用于其全部付款图。先直接付清 I、只将 R 入 fresh 图时有新的时间必要条件，但 source/current/余预算必须重算，不能照搬本页 r+H。

真实缺口仍是用全部 off-history IC 控制同一角色多来源的共同金额。本页没有补上这条关系，不能将必要 cut 或未分离报告作主线推进。
