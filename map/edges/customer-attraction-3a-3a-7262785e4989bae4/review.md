# M-63c882b0c8414805a43d4d8d4e43f4e3 审读与边复用

## 对象与承重结论

对象是“独立初段与折扣尾闭包在同一真实末端的合法联合投影”（version 1，proved；registration pin `403896c58e3ef32a0658cf8f47cd52451777da770e2e6a2dbb15cd3345668f6e`）。模型是有限客户、有限非空共同标签目录，允许重复/空覆盖；单位提供者观察完整有序历史并依同一完整策略行动，完整纯 SPE 对全部合法偏离满足弱 IC，保留平局与零客户。固定合法源 h、余人数 k≥3、真实回复映射 `C_h`，强制 T 得 B(T),C(T)，再强制同一真实 C(T) 得 J(T),V(T)，所以 `V(T)=C_h(C_h(T))`；同一 C 和最终 V 的会员位是组合中共享的隐藏坐标。

正文第一合同把两枝 34 行与强 PAIR 用任意客户无关非负权 alpha 合账：

`B_alpha=(a_T+a_C)r+A_alpha u_m+D_alpha K >= Σ_x E_alpha,x(t,b,c,j,v,s,s')`,

其中 s,s′∈{0,…,k−3}。第二合同用独立非负权 beta，在每个合法当前主题上给 H_beta(t,c,s)，尾部人数为 k−2，预算 `B_beta=a_beta r+A_beta u_m+D_beta K`。四条二状态 Bellman 策略经有限共同目录的加性最大值闭包给 `B_beta >= Σ_x Psi_beta,x(1_F)`；不要求 F* 在真实回复循环上，也不把辅助势当玩家效用。

对初段真实 `V=V(T0)` 使用尾合同并相加，保留两个式中的同一 v，再把真实会员域扩大成全部合法 `(b,c,j,v,s,s′)`，得正文式 (7)：

`(a_T+a_C+a_beta)r +(A_alpha+A_beta)u_m +(D_alpha+D_beta)K >= Σ_x min[E_alpha,x+Psi_beta,x(v)]`。

因此联合隐藏最小值逐客户不小于分别最小值；`gain = Σ_x(L_joint−L_sep) >= 0`，但这只证明固定 alpha/beta/delta 的联合投影相对该组分别投影的增益，不能升级为超出全部独立参数锥的严格包含。beta=0 精确恢复旧初段投影；delta=0 的非零 beta 只是新增一次尾合同，不应称为折扣循环增益；换历史源必须另付该源真实收益。

## 证据与有限结论

`master_cuts/dynamic_5752_exact.json` 是 4849 列必要 LP 点（`exact_feasible=true`、`exact_optimum_claim=false`、`verified_rows=5752`）；`selected_prefix_tail_5752.json` 固定 16 条有理行。独立 `main_verify_prefix_tail_5752.json` 返回 `status=PASS`，按全部六索引、四确定 Bellman 策略、共享 v 重新构建 16×4849 系数并核 exact joint/separate/gain。16 条中 12 条 beta 非零且分别投影 slack 非负、联合 slack 严格负；另 4 条 beta=0 只是原共同查询锥的重新配权。`prefix_tail_beta_zero_audit.json` 的 `columns=4849`、`all_equal=true`（delta=3/4）精确确认 beta=0 嵌入。上述有限点不是完整 SPE，也不推出六人 half 或所有 alpha′/beta′ 参数族的严格分离。

## 复用的现役 canonical 关系

本任务不新造同端点边。已核对并原样复用以下 accepted JSON：

1. `boss2-six-cross-pair-and-discount-pay-shared-terminal`：`{M-e394b173b9b1419588c6c380da4bd326, M-b233ef00a9c34e189817cdfb7a495107} ⇒ M-63c882b0c8414805a43d4d8d4e43f4e3`。其条件正是同一完整策略/合法有序源、共同真实 V、固定菜单、alpha/beta 非负、共同预算相加；解释逐项对应正文式 (1)、(6)、(7)，并明确不把 16 行有限严格性扩大为全锥结论。
2. `boss2-six-cross-shared-tail-to-rz-income-credit`：以 M-63 为 source 的固定 actual 第四源应用，正确支付两合同预算并保持共享 v；它是核心定理在后续 R/Z 收入信用中的已证使用，不反向增添一般假设。
3. `boss2-six-cross-hierarchy-and-shared-tail-pay-39-more-rows`：以 M-63 为 source 的 5752/5775/5783 有限层级行来源，保留共同预算与 shared-v 语义；其有限最优/对偶数值仍由目标证书承担，不把本核心升级为完整目标证明。

## overlap 处置

- `M-b233ef00a9c34e189817cdfb7a495107`：同源折扣尾闭包已经作为 canonical 边的第二个 ALL 前提与 M-e394 一起支付式 (7)，固定菜单、`0≤delta<1`、有限目录最大值、尾预算和同一真实 V 均已核清；没有未付的独立 3B 比较，关闭该 overlap。
- `M-e394b173b9b1419588c6c380da4bd326`：同源 34+PAIR 初段与共同隐藏 `(b,c,j,v)` 合账已经作为 canonical 边的第一 ALL 前提，且保留 `k−3` 计数压缩、PAIR 自交平均和同一 C；本轮没有新的端点或条件，关闭该 overlap。

## 未付证明义务

仍需把有限 necessary cuts 与真实 actual 收益、全局 SPE 实现和六人 half 目标分开处理；固定 alpha/beta 的联合严格性不证明全参数锥严格分离。下一桥是跨 actual 第五源的平衡 k=2 统一正加性价格，并须分列两个源钱包、每次支付完整常数；这不属于本任务。
