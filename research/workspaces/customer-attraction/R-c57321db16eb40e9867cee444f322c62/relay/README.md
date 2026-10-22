# 一般signed relay debt：净额投影与跨深度义务

2026-10-22。Q-CAG-HALF仍OPEN。这里严格保留同一个比较组合、真实S/Z、实际F以及未覆盖/重复E信用；不把固定人数角点加行当作一般机制。

- [projected_relay_debt.md](projected_relay_debt.md)：普遍精确守恒`Debt−threshold=m(OPT−2W)+ΣK`，K≥0，说明旧充分支付比half更强；净δ−S只看实际路径和末回复边际，真实D及中继负载消失。给3人8客户两个完整SPE，实际路径及全部实际菜单末回复完全相同、同一最少主题最优组合，但真实中继负载、D和离轨福利不同。
- [audit_projected_debt.py](audit_projected_debt.py)与[精确报告](projected_debt_audit.json)：从定义核验两个策略各39项比较与所有信用恒等式。不导入旧发现器。
- [clone_drift_unbounded_family.md](clone_drift_unbounded_family.md)：任意完整SPE的两客户2q人无限族；同一最少最优查询下，未配对跨角色差与复制slack分别调和无界、差精确1/(2q)。严格排除将该深度差单独按固定常数W支付；不否定保留抵销的全局净债务。
- `algebra/`：内部研究员探索同主题克隆的跨深度真实节点望远镜，以及额外跨角色drift是否有符号控制。该目录的明确状态见其README。

准确范围和待审状态见[CLAIMS.md](CLAIMS.md)。当前文件可checkpoint；未操作git或work.py。

当前可接续义务：重新引入真实内部节点，不能声称净额仍保存中继slack；也不能因投影丢失信息就断言一般half不可证明。下一次判别为克隆/强制回放所生drift的完整SPE攻击与精确支付接口。
