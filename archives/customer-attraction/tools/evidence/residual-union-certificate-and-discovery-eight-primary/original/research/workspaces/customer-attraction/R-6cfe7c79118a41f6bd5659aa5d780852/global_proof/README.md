# 一般半覆盖直接证明工作区

当前目标：Q-CAG-HALF 一般共同目录、任意人数、每个完整历史依赖纯 SPE 的 `2W≥OPT_m`；仍 OPEN。本目录不修改共享数学状态。

当前已闭合的小资产是 [残余比较并集桥的两人反例](residual_union_bridge_counterexample.md)。它否定更强辅助桥 `W≥max_{m主题}|∪T_j\C|`，不是主目标反例。

- `residual_counterexample.json`：27 单位客户、6 主题、2 玩家及全部 7 个决策节点的 SPE 证书。
- `audit_residual_counterexample.py`：直接依定义使用 `Fraction` 重算全部终局、最佳回复、根偏离及最优覆盖，不导入规范模型或求解器。
- `full_two_residual_lp.py`：发现用的有限策略锥线性规划；数值 LP 不作为正确性前提。
- `residual_two_lp.py`：初始不完整根偏离模板；保存一个只否定该松弛模板的点。未补全根分支的松弛点不称为 SPE。
- `search_residual.py`、`search_background_residual.py`：精确全集随机发现实验；有限未发现反例不证明全称结论。

下一步：直接攻击精确 `2W−OPT_m`，保留最优组合的重叠收益与被覆盖客户的复用；C/Y 二分后仅对 Y 比较并集收费已过强。
