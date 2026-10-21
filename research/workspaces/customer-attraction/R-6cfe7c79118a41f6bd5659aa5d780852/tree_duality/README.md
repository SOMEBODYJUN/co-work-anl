# 全深度收益形式图与任意逐历史乘子的精确流压缩

本目录由 Boss5 子研究员 tree_duality 在 2026-10-21 写入。只含本轮探索资产；没有修改共享正文、没有提交，也没有证明一般 Q-CAG-HALF。

- [payoff_form_graph.md](payoff_form_graph.md)：自足精确图流等价、全深度 SCC 有符号支付、森林支持压缩及严格扩大末端平局空间的完整 SPE。
- [graph_probe.py](graph_probe.py)、[graph_probe.json](graph_probe.json)：四人三主题严格扩大例的 Fraction 完整历史核验及完整策略。
- [graph_flow_audit.py](graph_flow_audit.py)、[graph_flow_audit.json](graph_flow_audit.json)：独立定义级图流、闭集判别、森林压缩和有限策略回归。
- [residual_union_independent_review.md](residual_union_independent_review.md)：27 客户残余并集桥反例的逐单位客户独立审查，附独立脚本及 JSON。
- [fractional_cover_review.md](fractional_cover_review.md)：对根代理分数覆盖递推的独立数学审查。

当前精确缺口：压缩后的图流存在性没有自动解决。对每个**真实策略诱导**的图和根终局，仍需构造满足正余项的流散度；任意抽象图不够，也不能只保留 SCC 支付而丢弃 DAG 边。
