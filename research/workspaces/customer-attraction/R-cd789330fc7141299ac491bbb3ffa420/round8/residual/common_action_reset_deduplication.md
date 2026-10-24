# 同 action 的 uniform-reset：独立重构与旧捕获流去重

2026-10-24，residual8。一般 Q-CAG-HALF 仍 OPEN。此页保存与 inventory8、credible8 的数学沟通；**没有新增核或福利结果的认领**。

## 推导与核对

读 [inventory 密度界](../inventory/source_preserving_density_envelope.md) 及 [credible 共同 query](../credible/joint_query_compression.md) 后，我独立尝试：仅对 actual 未覆盖 R 客户，在自然 context 当前动作 a 下重新读取 actual-prefix 完成叶 A=finish_sigma(B_<i,a)，将每份输入 h_x 均匀分给 A 中全部 x-coverer。current 获 h_x/c_A(x)，每位未来 coverer 各获同量；R 无 actual past coverer。

这保持每个客户质量、所有 future 角色严格增加。任意固定角色 i 的全部状态输入满足

    sum_(t:role i) h_tx <= initial_mass_x <= 1,

因为每条质量路径至多经过该角色一次。相同 (i,a) 的全部旧历史有同一 reset A 和同一转移律，可以在调用 IC 前精确合并。令 H_(i,a,x) 为其合并输入，则

    current_(i,a)=sum_x H_(i,a,x)/c_A(x)
                 <= [max_x H_(i,a,x)] D_(i,a)
                 <= u_i max_x H_(i,a,x),

其中 D_(i,a)=u_i(A)<=u_i 是一条原 actual-prefix 完整 IC，且 max_x H<=1。没有逐客户使用 IC。若初始源也按同一均分 query 入图，初始与后继相同 action 可以共同合并，不能先各领一份 u_i。

inventory8 与 credible8 从陈述独立检查上述域及不等式，通过；二者都指出 distinct actions 的系数总和仍未付。该核将 raw reset 的 common-coverer 部分继续送向未来，所以 raw 核 current 中的 common-count 因子消失，但未来压力增加。它通常不是原 SAFE/CLIP 的子核。

## 确认是旧资产

随后查到 [round3 递增角色捕获流](../../round3/credible/increasing_role_capture_flow.md) 已逐字义使用状态 (i,a,x)、actual-prefix query、全部 coverer 均分和严格 future 递归；本次 kernel 与状态压缩就是该旧流。其 [全图命中界](../../round3/mixed/capture_hitting_capacity.md) 亦已证明同角色客户 antichain/HIT。旧稿还用总吸收 A_s/完整 query 收益 D_s 标量化，给定状态费用通常不高于最大密度上界。

因此本次没有新 kernel、没有新容量或新福利推进。其用途是将可信分支共同 query 压缩与现有捕获流准确对齐，避免错误宣称 raw-SAFE 的新 cap。

## 仍未取得的真不等式

逐客户 sum_a H_(i,a,x)<=1，不蕴含 sum_a max_x H_(i,a,x)<=1；不同 action 可以在不同客户上分别达到最大值。全部 source 库存和每 action 一次 IC 仍不足以支付同一角色的多 action 叠加。

真实 off-history IC 从规定动作改实际 B_i 给下界 v_t>=return_t；与 actual-prefix IC 组成 rectangle 后，真实 off-slack 是非负优势，不能直接当退款。未找到将这些 offIC 与同一 actual C/G collateral 共同入账、从而限制 distinct-action 聚合 current 的新关系。下一步若接续，必须补这条付款；不重复此 kernel 推导或扩大有限锥攻击。
