# tree_transport 接续入口

主目标Q-CAG-HALF仍OPEN。本目录仅保存全树跨分支表示和证明模板的实质资产。

- `monotone_support_obstruction.md`：新增精确MT-9/4障碍。3人6主题的真实完整SPE图上，即使加入全部单标签锋利稀释、同支持总支付、全部可见覆盖单调性，仍有根1、比较9/4的非负有理伪收益。不是客户反例；文中给次模缺额1/24及Shapley线性缺额1/12。
- `monotone_candidate.json`：全部126收益顶点及完整43历史策略的有理证书。
- `verify_monotone_support.py`、`monotone_support_audit.json`：标准库Fraction定义级独立于LP的核验及实际输出。
- `explore_support.py`：发现LP；`support_candidate.json`是未加单调的较弱候选，`submodular_candidate.json`是加入可见单调次模后的29/16有限可行点。后两者不支持普遍命题，也不声称精确最优性。

下一步：在保留全部真实有序历史的前提下，加入完整共同Shapley一致性或非负客户表示的承重耦合；不再把同支持总支付守恒视为足够修复。
