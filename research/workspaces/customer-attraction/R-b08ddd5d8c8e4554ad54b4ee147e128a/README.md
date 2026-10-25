# Boss7：一般顺序半覆盖的研究桌面

研究存档 customer-attraction；发布身份 R-b08ddd5d8c8e4554ad54b4ee147e128a。
唯一主目标 Q-CAG-HALF 仍 OPEN，模型以 research/current/customer_attraction/model.md 为准。
全部历史依赖纯SPE、任意有限目录与人数、空主题和零客户的量词不变。

## 本轮实际新增材料

- [均匀删除比较式的精确反例候选](boss/uniform_deletion_boundary.md)：五人六主题31单位客户；完整策略已由定义级规范核验，独立审查进行中。只反驳固定均匀删除静态核；不反驳可优化删除支持、真静态安全值或半覆盖。
- 纯续局门槛与仿射包络（原正文 `dynamic_induction/nonconvex_screen.md` 未物化，不作为可复核来源）：四人四主题的非凸筛选边界，子分支与Boss独立Fraction核对；只否定明确的无损筛选等式。
- [独立有序历史审计](boss/audit_affine_obstruction.py)及其JSON：不导入规范求解器，复算仿射筛选边界。
- potential_transport/ 正在精确化静态对称iid均衡福利桥的反例；成熟状态以该目录README及后续审查为准。
- global_proof/、counterexample_search/ 保留一般交换、弱逐人门槛和可信反例构造的进行中研究，不是已证半覆盖。

## 当前方向与接续

均匀删除比较式已出现真实SPE候选反例，下一步审计并转向可优化删除分布、真实分支菜单或独立的直接覆盖机制。仿射状态有非凸门槛缺失，不能靠混合纯续局无损恢复。仍缺的是一般跨真实分支总支付，不是更多有限无反例样本。

所有有限搜索仅支持列明范围。个人文件允许未完成、失败和未独审；不自动成为共享canonical记录。研究员共用本actor，由Boss统一checkpoint；只有work.py回执pushed才说明远端保存。
