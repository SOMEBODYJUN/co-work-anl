# 第七轮 global：真实 off-IC 的拥挤债与共同投影

2026-10-24。只研究任意人数、任意有限共同目录和每个完整历史纯 SPE 的一般命题。**Q-CAG-HALF、ROLE-CAP2、共同 source 支付均 OPEN。** 无 git/work.py 写操作，没有覆盖前轮资产。

- [静态中间分母 off-IC 分解](static_denominator_off_ic.md)：精确式 u_i=v−ℓ+T_B+T_W，保留真正 off-history slack；过去 B 拥挤与未来 W 响应分别有明确利润支配。初始单 reset 过去角色合法，进入第二次 forced W 后不假称自然过去利润。coupling 未读本证明、仅收合同后 [独立重构](../coupling/static_denominator_and_query_projection_review.md) 恒等式与逐边界，并补出 synthetic query-projection。root 指出的多强制闭合缺口已明确记入正文。
- 同文 §7 的 COMMON-CAP 是一条局部容量不等式：同客户所有共同 coverer 的密度≤L 的请求，可以联合投影到 parent 券，输出密度≤L·|common|/c_F≤L。它同时接 prefix 与 common-future 请求；exclusive-future 请求、whole-profit 重采样与跨历史共同 cap 仍未付。未把该局部界称为 HALF 进展。
- 同文 §8 接上 coupling/credible 分别得到、root 亦独立重构的 [固定 B 静态列容量](../coupling/fixed_parent_static_column_capacity.md)：全部角色 SD 第一正项在同一 recipient 列共同≤L 倍 actual-new 利润，global 补出精确缺额 1−(c_Z−|common|)/[c_Z(c_B+1)]。由支持不交，fresh/own-intersection 既有客户券可与该输出共同用同一份 B 利润；尚未证明 whole-profit 重采样保留这条支持不变量。它是一条新的普遍局部支付关系，未闭合跨 B 的主容量。
- [固定 assignment 的 CLIP 攻击实现](attack_role_cap.py)：明确攻击一般候选“任意固定最优主题槽分配、first-owner 分割均有 CLIP role cap2”。生成完整有序历史 SPE 证书，建立精确 Fraction 系数 DAG，浮点 LP 自由选择全部合法 CLIP 子边，仅作为候选测试。两个 [200 次记录](role_cap_attack_5x5.json)、[300 次记录](role_cap_attack_6x5.json) 没有浮点分离；后者是在 root 停止新扫描指令到达前已运行、取消时已完成。无精确 cap 证书，没有从阴性测试推出候选成立，也没有扩展任何人数特例。

本轮另已向 root/credible/transport 传递原 forward reset 图的结构：每个非actual目标自然历史的 first-departure 角色唯一确定其全部原正边 parent 的角色与 action，因此其 incoming 可以按共同 reset query 因式分解。该结构尚未给出 source 密度 cap，不计新的福利不等式。

root 后续给出最优参照逆 SD 的具体两预算初始化；本组 [独立审查](two_budget_initialization_audit.md) 核对定义、符号、真实 W-future 域及逐客户 COORD-CLIP。新初始化可在 PB/current/future 三出口保留每个 OPT 客户总库存一，不使用逐客户 IC。后续 Aout_j≤2u_j−d_j−Bcol_j 仍是未证一般候选；出口时间支持为 j≥源 i，不是严格 >i，也未继承 fresh HIT/PRICE。

下一步是给 SD+合法投影选择同一份非负权，支付 gross excess β(u_i−v) 的联合拥挤债；要控制环、whole-profit 重采样和 source 的互斥性。仅有每边合法、每个局部投影不增密度或有限 LP 无分离都不够。
