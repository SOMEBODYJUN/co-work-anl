# 全树收益图与一般半覆盖对偶

本目录是 Boss7 内部研究备份；Q-CAG-HALF 仍 OPEN。

- `outcome_payoff_graph.md`：固定完整有序策略的收益图、SCC 显式有符号支付，以及精确商图锥分解。给出 18 单位客户完整 SPE，SCC 像空间严格大于仅末层平局空间。
- `audit_outcome_payoff_graph.py`：从所有有序历史、所有客户类型重建真实行；Fraction 检查全部 SPE 行、路径支付、两个空间的精确秩，并可输出冻结 JSON。
- `outcome_payoff_graph_audit_v2.json`：上述脚本的冻结输出，增加 n=1/p=1 边界；原 `outcome_payoff_graph_audit.json` 保留首次运行。

一般证明尚缺：在任意完整策略对应的商图上，共同选取非负跨 SCC 流、有符号 SCC 内运输和非负客户余项，支付 `2c-o`。图分解本身只是精确换表示，不保证该支付存在。SCC 像只给已知行锥 lineality 的显式子空间；映射后的额外线性关系可以使真正 lineality 更大。

下一步探索商图上的全局预算或可失败的严格加强，保留全部历史的可实现边；不固定早期乘子，不把抽象有向无环商图误称为映射后无 lineality 的锥。
