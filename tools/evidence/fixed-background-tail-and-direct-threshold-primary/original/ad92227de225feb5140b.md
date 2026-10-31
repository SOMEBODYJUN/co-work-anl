# 真安全值聚合桥：本轮停止点

2026-10-24。一般共同目录、任意人数、每个完整有序历史纯SPE；一般 Q-CAG-HALF 仍 OPEN。本子任务没有得到新的一般支付关系、完整证明或目标反例。没有修改共享数学身份、运行git或外发消息。

## 已核旧范围

- 真安全值 `v_m` 使用不观察查询实现的静态联合对手；`OPT_m <= (2m-1)v_m` 已证。逐人 `u_i>=v_m` 已被完整SPE否定；聚合 `W>=m v_m` 及较弱 `W>=(m-1/2)v_m` 仍开放。来源：`research/current/customer_attraction/oblivious_security.md`、`security_chain_and_local_boundary.md`。
- 安全链 `sum_i D_i=W-mv_m` 为恒等式；逐步非负失败。不能从链恒等式得到全局总债预算。
- 强/弱iid福利基准、PI最优势增量、任意查询p的总去相关、实际均匀删除静态核、旧背景已覆盖直方图信用均按原范围失败；没有把它们重新列为开放桥。
- extra-one逐首位、自由完整菜单Mfull、WP2保持开放。本轮兄弟子任务 strategic_relay 研究Mfull，故这里没有重复对同一候选加固定核。
- 随机删静态对手槽给 `(r-1)v_(r-1)(b)<=r v_r(b)` 是**旧结果**，并非本轮新增。准确来源为 `R-acd97406d8c4409d962eab2adcdc520c/round4_security/security_population_limit.md` 第2节，含任意固定非负背景b版本和全目录极限。它没有支付真实SPE的IC。

## 本轮实际推导与检验

曾检验是否仅由实际每位的稳健偏离floor

`u_i(z) >= max_T sum_(x in T) 1/[b_i(x)+m-i+1]`

即可推出安全值聚合。答案是否；`audit_floor_relaxation.py` 保留一次浮点发现后独立重建的精确小见证，并明确识别其倒二真实IC失败。它不是SPE，不是half反例，不据此发展新的负模板。父方的三窗口环还已击穿更强的阈值菜单放宽，本小见证不构成本轮主线推进。

另考察任意背景剩余利润候选 `P_r(b)>=F_r(b)/2`，其中 `F_r=max sum d/(b+d)`。它自然包含原根目标，但标量归纳仍欠根短缺由真实尾超额支付；没有得到新式。兄弟 general_proof 已接收此对象作独立推导。

## 准确未闭合点

在固定完整SPE，安全最优查询与真实响应相关；静态安全值的对手不观察查询。必须用全部真实后继IC控制此适应性，或允许跨位置支付。`W>=m v_m`、`W>=(m-1/2)v_m` 或 `sum_i u_i>=m v_(m+1)` 在这里均未证明。随机优先权解释、复制查询链和势删除式没有消去已知跨枝删除势差，故不以重述、无反例或静态单调性冒充一般推进。

文件：本README；`audit_floor_relaxation.py`（标准库Fraction独立核验）；`floor_relaxation_audit.json`（本次运行输出）。
