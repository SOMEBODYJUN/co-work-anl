# round4 relay：可预测激活路由与整条 IC 解耦

2026-10-23。只攻一般 Q-CAG-HALF 全部量词；仍 OPEN。不 git、不改共享与旧冻结，由 root 统一 checkpoint。

本轮从 round3 共用 Exp 世界接续，但不重做 Phi/Psi ghost 恒等式。当前新对象见 `predictable_activation_transport.md`：将阈值层内的最高钟覆盖者改为最早激活未来覆盖者，使到达当前状态只依赖已过去的激活；由此得到非owner状态吸收的 Beta(2,c)=1/[c(c+1)] 上界。原完整 IC 最终只购买积分后的非负常数系数，不按钟条件化。

该界为全部合法原实际-prefix查询及任意固定 owner/残源成立；尚无多查询共同成本界，不能据此认领 half 或 NET。mixed 收到精确定义后独立重构了源归一、可预测性与 Beta 界；没有独立证明费用合并。

- `audit_predictable_activation.py` / `predictable_activation_audit.json`：仅对一张分支/合并查询 DAG 作定义级精确回归，9个source、每个64个激活向量，81个状态多项式比较与18个角色联合界均通过。不扫描SPE或特殊目录。
- `adaptive_cancellation_priority_world.md`：将逐客户吸收边际放入同一 Uniform 角色优先级世界，各客户以自身 owner 优先级为阈值，所有源逐world各一单位。允许观察完整世界后在同一实际 Hall-A Gamma 中取消，剩余总量仍逐world为OPT-W；积分后仍只购买整条原 IC 常数，SOURCE-NET保留。取消选择可放入费用期望内，但其普遍费用<=W仍未证明。mixed收到精确定义后独立重构该耦合与归一，并指出适应取消后Beta上界不可再乘平均残源。
- 该稿进一步用固定state排序witness，将路径放宽为任意依全世界选择的激活未来coverer；强制等到没有激活coverer才吸收。原始 source1/c、无缩放Beta2与SOURCE-NET仍成立，可共同优化终点与取消；V_best<=W仍未证。
- `audit_priority_coupling.py` / `priority_coupling_audit.json`：同一DAG上的独立排列世界核验，对比前一冻结报告的全部精确吸收边际；只校对定义，不认证一般费用界。
- `review_mixed_joint_owner_credit.md`：独立重构 mixed 的 owner-absent I 信用/查询联合核。同U世界下exact-role credit=e_j、剩余query质量=kappa，fixed-state排序界<=真实modified边际；明确不能沿用已暴露未来J的条件独立式，也不覆盖owner实际present情形或共同费用。
- 该review另核mixed新random winner coupon Hall-B：逐world全cut给G取消，平均角色边=e、sink=beta；可取消实际存在的R/I-query，避免lambda/kappa相关性，但SOURCE-NET须另证，不与Gamma_A合领G。
- `adaptive_cancellation_cut_formula.md`：独立重推后发现与shared `net_dynamic_rank.md` §2–4同对象，已明确引用，不另认新rank/费用公式。shared已核本人逐批sink增广证明；本页只保留推导与新adaptive world逐点调用接口，未新增<=W付款。
- `review_incoming_slack_transport.md`：独立核credible的OFF-IC、fresh reset和tracked逐recipient系数1/2，IC域/符号通过；补同一actual查询的多父贡献可安全合并，跨query叶仍未付。

当前最具体的接续是证明适应取消/路径费用 V_best<=W，或更弱、放弃局部delta后的全cut费用 V_0<=W；最早路径版本为 V_adapt。也可用新的合法全树路由继续降费。不能把取消多面体、随机终点及 IC 系数分别优化后当作同一可行方案。
