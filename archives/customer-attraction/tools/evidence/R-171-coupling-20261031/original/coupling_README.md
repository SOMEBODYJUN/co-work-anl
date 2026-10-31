# Boss5 接续：共同客户运输与租金支付

一般 Q-CAG-HALF 仍 OPEN。当前承重问题是把真实全树激励产生的误差嵌入一个共同根路径，证明受控连续窗口拥塞，或另建带抵销的共同客户支付。

* `sparse_slot_complete_spe_obstruction.md`：两个单位客户、两个互斥单例主题的全人数完整 SPE 族，证明任意稀疏未来槽位的 1/j 租金即使 Gamma=1 也对 W 无界。消除旧任意路径障碍“未证 SPE”的限制；不是主目标反例。
* `audit_sparse_slot_complete_spe.py`：有限 q 的全部有序历史及顺序敏感平局策略审计，另用 Fraction 从定义核对稀疏租金。
* `chronological_sparse_rent_and_skip_premium.md`：任意稀疏槽位的 reset 租金精确分成可按同一槽位拥塞支付的真实 hit 时钟租金，以及显式非负 skip-premium。连续窗口时 premium 为零；两个客户的完整 SPE 族中，clock 总量小于1/4，全部无界发散恰在 premium。
* `audit_chronological_sparse_rent.py`：全部有限二元路径/稀疏子集的 Fraction 表示审计及共同拥塞预算检查。

当前新增状态为作者完成，待父方独立攻击；父方已盲核单 hit premium 系数。下一步必须在原 SPE 真实激励行中产生 clock 分母，或用真实松弛/抵销支付 premium；不能只在表示中删去 premium，也不能以根路径来自 SPE 为由删去连续性。
