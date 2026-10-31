# 逐 world 联合正查询的 R-only 投影

2026-10-23，credible。一般解析组件，mixed 已[独立重构并留痕核对](../mixed/rankwise_joint_hall.md)通过。任意单位客户共同目录、任意 m、全部有序历史纯 SPE。本文给一项正查询证书的投影关系，**没有证明费用小于 W，Q-CAG-HALF 仍 OPEN**。

## 1. 同一 world 上的两张 Hall 图

固定实际终局 Z、覆盖 C、最优并集 O、owner 分割 Q_i⊆T_i，及 R=O\C、I=O∩C、G=C\O。记 J_x 为实际 coverer 角色集。取全角色互异 priority U，令 w(x) 为 J_x 中 U 最大的角色。

每个 y∈G 把一单位 source coupon 放在 w(y)，角色 source 记 g_i(U)。逐 world 总和为 G，且 E g_i(U)=u_i(G)。这不是每 world 的原角色利润，只在期望上对应实际资金。

构造保留客户标签的两图：

* A(U)：对每个 x∈I，设 owner(x)→w(x) 的单位边，自环可删；对每个 x∈R，设 owner(x)→终点 t 的单位边。
* B(U)：仅对 owner 实际未覆盖的 I 使用资源。若 U_w(x)>U_owner(x)，设 owner→w(x) 单位边；否则设 owner→t 的单位 query 库存。R 仍设单位 query 库存。

B(U) 是 mixed 提出的逐 world 联合图；I-query token 恰在 owner 最高时存在。R token 每 world 始终存在。若 Q_I(U) 为存在的 I-query token 数，则 E Q_I(U)=κ^-，其中 κ^-=Σ_(I中owner未覆x)1/(|J_x|+1)。

## 2. 每个 world 的满流与期望域

对任意角色集 L，source g_U(L) 至多为实际 G 中被 L 的动作覆盖的客户数。owner hybrid 最优性给

    g_U(L)≤#{x∈O:o(x)∈L，J_x∩L=∅}。

右侧每个客户在 A(U) 给一单位出割：实际已覆盖时赢家在 L 外，实际未覆盖时是 R 终点。在 B(U)，同一客户的 owner 必实际未覆盖；或有去 L 外赢家的边，或有 query 终点，亦给出一单位。故两图全部 source cut 足够，均送满 G。B(U) 的角色边升 U、无环；A(U) 可以有环。单位容量与整数 source 可选整数流。

E A(U) 的每个 I 标签边容量为 1/|J_x|，恰为原 actual Hall-A；B(U) 的 I 角色边与 query 终点容量期望均为 1/(|J_x|+1)，恰为 actual Hall-B 的 error/stock。两图源期望均为 g_i。

## 3. 保留联合 R 取消再增广

固定任意 B(U) 满流，其 R/I-query 终点取消量分别记 λ_R、λ_I，总和 G。分解 source-to-sink 路径，仅保留终于 R 的路径。因为 B 的角色边属于 A，source cap 与 R 终点相同，所得为 A(U) 值 λ_R 的合法部分流。

从此部分流在 A(U) 残余网络增广至最大值 G。简单 source-to-t 增广路径不会使用任何终点边的反向边，因为反向边从 t 出发；所以已有每个 R 终点流量均不减少。得到逐客户取消

    γ_R,x(U)≥λ_R,x(U)，    Σ_Rγ_R,x(U)=G。

额外取消的 R 质量恰为 λ_I。其期望流是原 actual Hall-A 的合法流、取消总量 G。

**域不能偷换。** 不保证每个 γ_R(U) 属于固定均值 Hall-A 图的可行集 Γ；保证的是它属于随机图 A(U)，且平均流合法。费用与 U 可相关，不能改用固定平均 γ 的价格公式。

## 4. 正 whole-IC 总费投影

考虑任意使用 B(U) 取消的联合 packet 规则，每个未取消 R/I-query token 沿合法 actual-prefix 查询有限吸收。查询 s 的原完整收益 D_s 不随 U 改变。令联合吸收为 A_s^J(U)，正费用为

    K_J(U)=Σ_s[u_role(s)/D_s]A_s^J(U)。

吸收处 D_s>0。原完整 SPE 给每个固定状态 u_role≥D_s，所以每单位 token 的 query 总费至少1。这只读确定性的原 IC；不对随机 sampled utility 调用新比较。

保留原 joint 的 R 路径，仅删除 γ_R−λ_R 额外取消的 R 质量；所有 I-query packet 不再运行。可先虚拟模拟原联合规则再冻结路径，因此即便原 R 路由依赖 I 标记，保留路径仍合法。

R 费用减少至少 λ_I，联合中剩余 I-query 费用至少 Q_I(U)−λ_I。因此投影的 R-only 正费用满足

    K_R^proj(U)≤K_J(U)−Q_I(U)，
    E K_R^proj≤E K_J−κ^-。                       (PROJECT)

取唯一原 whole-IC 系数 E A_s/D_s，便可购买 E K_R^proj。若某联合证书证明 E K_J≤W+κ^-，则已可构造 R-only 随机 coupon 证书满足 E K_R^proj≤W；其逐 world 残源 R−G 随即给 half。

这没有证明联合费用上界。若联合账用负的 I 信用抵扣费用，而非这里的正 query 总费，须另外核账，不能直接套 PROJECT。

## 5. 保留的接口与准确边界

投影只删除 R token，故原未缩放 MARG-CAP 仍成立，自然 action-return 的 parent 历史也保留，可接 [incoming OFF-IC](incoming_slack_transport.md)。取消适应 U，不能把上界乘平均残源。

投影不保证逐角色 NET、本地 SOURCE-NET 预取消量，亦不保证固定均值 Γ 的每个可行点都能提升到随机 A(U)。本文只证明：这种逐 world 随机 coupon 的联合**正**查询总费证书，可无损投影为合法 R-only 随机图证书。真正需要的费用≤W仍未取得。

### 固定取消量版本的直接推论

本小节由作者后续追加，尚待独立核查；上面的 mixed 回执先针对逐 world 投影。

若联合方案使用原 actual Hall-B 的固定 λ（source 已降为 g_i），也有一项不需要随机 lift 的投影。B 的 I 角色容量 1/(c_x+1) 不超过 actual A 的 1/c_x，R 库存相同。保留 B 送到 R 的子流 λ_R，再在 actual A 残图增广到 G，得到固定 γ∈Γ_A、γ≥λ_R，额外 R 取消总量 λ_I。

对同一个固定 R 路由，单位原客户的总价 v_x≥1，故新增 R 取消至少节约 λ_I。I-query 残源恰 κ^-−λ_I，其正 whole-IC 费用至少此量。因此同样有

    K_R(1−γ)≤K_joint−κ^-。

这里 γ 是原固定均值 A 图的可行点；与随机版的可行域不同。它仍不保留联合方案所用的本地 δ 或逐角色 η 界。结论只说明加入正 I-query packet 不扩大此固定总费证书类，不否定它可用于推导 formal 势、跨叶共同信用或其它实际费用上界。
