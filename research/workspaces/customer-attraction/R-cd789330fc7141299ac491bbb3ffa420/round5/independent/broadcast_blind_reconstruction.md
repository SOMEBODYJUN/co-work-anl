# 广播组件盲重构（先于作者稿阅读）

2026-10-24。仅依据 root 消息重构，尚未打开 `credible/all_fresh_submarkov_elimination.md`。以下是独立代数与合法域检查，不是 half 证明。

固定原完整 SPE、原实际终局 Z 及其覆盖 C。自然 context t=(g,i)，其中 g 长 i−1，a=σ(g)，B=finish(g)，A=finish(actual_<i,a)。对 x∈a，两个终局均有第 i 位覆盖者，令 J_A,J_B 排除 i，c_A=1+|J_A|、c_B=1+|J_B|。定义 A-only 与 B-only coverer 的 q±=1/(c_Ac_B)。则逐客户

\[
\frac1{c_B}-\frac{|J_A\setminus J_B|}{c_Ac_B}
=\frac{1+|J_A\cap J_B|}{c_Ac_B}
=\frac1{c_A}-\frac{|J_B\setminus J_A|}{c_Ac_B}>0.
\]

因此对非空有正客户的 a，v−P_future−P_past=R=D−N>0。若 a 为空，则这些量全为零，不能写严格正或 β=h/v。有限单位客户模型下 v>0 当且仅当 a 含客户。

每个 future 接收者 j>i 的 context 必须是 (A_<j,j)：A 在 i 之后按原策略继续，所以规定行动 A_j 包含该 x，且此 context 的 B 叶恰是 A。故接收者 v>0；不因原发送 context 的过去 g 与 actual prefix 不同而失去合法性。future 深度严格增加，所以所有自然 context 构成有限 DAG。j<i 时 A_j 是真实 actual action，故可以把 q+ 送到实际 coupon (j,x)；不能把 B 的过去或一条非规定的 A 过去当作当前 IC。

对 i=m，future 为零，全部处理止于 retained R 与 past 出口。全零/空主题节点不接收任何正 future 流；任意非负 b 的说法应限定正利润节点，或明确零利润节点强制 b=0。

任取正利润节点上的 b_t≥0，依深度递推 h_t=b_t+incoming_t，β_t=h_t/v_t。由 DAG 完整有限相消，

\[
\sum_t b_t=\sum_t\beta_t(v_t-P_t^{future})
=\sum_t\beta_t(R_t+P_t^{past})
=\sum_t\beta_t[u_i(Z)+P_t^{past}-N_t-e_t],
\]

其中 e_t=u_i(Z)−D_t≥0 仅使用 actual_<i 处相对 a 的真实偏离 IC。

fresh-only 限制 x∈a\C 时，actual past 完全不覆盖 x，故 P_past=0。对任意 k 个所选角色，单客户所选 A-only 角色数 d≤k 且 c_A≥d+1，所以 d/c_A≤k/(k+1)。乘 1/c_B 后求和，得到 P_selected≤[k/(k+1)]v。future 接收者保留同一个 fresh x，所以 fresh 正利润域也闭合。该角色子集界本身对全客户亦成立；fresh 的额外作用是无 past 出口。

coupon 重构：对每个 actual coverer j 与 x∈Z_j，设 coupon 价值 1/c_Z(x)。正项总和可精确写为 Σ_(j,x) Λ_jx/c_Z(x)，其中

\[
\Lambda_{jx}=\sum_{t:i=j}\beta_t+c_Z(x)\sum_{t:i>j}\beta_tq^+_{tj}(x).
\]

这是需求系数，不是容量上界。b 任意放大即可使 β 与 Λ 同比例放大；若主线还给 source 本身分配 actual coupon，必须在同一容量中计入其需求。负 N 与 e 目前只能保留在精确等式，不能先与任意某张券相配或免费取消。现有代数未给 half。
