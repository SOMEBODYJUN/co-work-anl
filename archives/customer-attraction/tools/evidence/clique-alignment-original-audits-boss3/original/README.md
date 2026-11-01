# 共同客户的完整图对齐预算

2026-10-21；研究备份，未提交。主目标 Q-CAG-HALF 仍 OPEN。

- `clique_alignment_budget.md`：从真实末位 BR 行推导一般 q、L、m 的完全图共同对齐扣除；给全部 K 下的精确闭式、任意权的安全下界、K5 严格超越全部环预算，以及一般图精确整数表示。
- `audit_clique_alignment.py`：独立于规范包的 Fraction/枚举公式回归。
- `clique_alignment_audit.json`：本轮有限审计记录；不替代任意规模证明。
- `clique_alignment_audit_expanded.json`：另加入 q=2,…,8 的任何真边子图零损失族审计。
- `same_query_redundancy_and_2396.md`、`evaluate_2396_clique.py`、`evaluation_2396_clique.json`：精确确认原2396坏点的三份前置查询族完全相同，新完全图行被旧族内 O 行支配；准确列出真正缺少的新查询回复。

当前可复用 Claim：全 O 完全图各边的独立 Fréchet 包络须扣除 χ；等有效边权时精确，任意边权只声称 min-weight 下界。χ 由全体菜单列次数的整数凸性产生，不能由环预算完全替代。早期真实分支到根路径 W 的无重复收费仍未闭合。

审查：root 已独立重构定义/方向和连续余数取等构造，并完成独立定义级有限审计，见 `../parent/clique_alignment_review.md`。下一步应新增不同的真实前置查询族并寻找根支付；2396点已有三份相同T_i查询菜单时本机制严格冗余，不应在该对象上继续调图权。
