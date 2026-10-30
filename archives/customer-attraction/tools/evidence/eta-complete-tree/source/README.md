# 完整树上的 η 候选审计，而非局部回复闭包

2026-10-26。状态：**接口及参数化核验已证；一般 η 付款与六人 half 仍 OPEN。**
没有新目标反例，也没有六人半覆盖证书。本目录仅由本轮 credible_tree 子任务维护，未改共享正文或账本。

唯一候选来源是 [最优首动作机会损失](../../../../current/customer_attraction/optimal_first_action_branch_gap.md) §5 的末尾：保留全部 ξ、只删 η 的充分付款，等价于

\[
 \sum_{i=1}^m\min_{A\in\mathcal A^*(h_i)}\frac{\eta_{i,A}}{r_i}
 \le 2W-\operatorname{OPT}_m.\tag{E}
\]

本目录新增的可复用信息是：对**固定单位客户实例**，能不采样完整策略而精确优化 (E) 在全部完整有序历史纯 SPE 上的最大违反量。该接口专门保留非极小离轨续局；它不同于只用默认最小源收益证书测试 (E)。精确递推与证明见 [eta_complete_tree.md](eta_complete_tree.md)，实现见 [eta_complete_tree.py](eta_complete_tree.py)。

独立小树 oracle 直接枚举全部有序历史策略，不使用集合值 BI：两主题三人全部 8 个二进制客户类型输入的 1,024 棵策略，及三主题二人全部 128 个输入的 10,368 棵策略。每个输入的 SPE 终局全集和 (E) 最坏违反量均与新 DP 精确一致，包含零客户、空主题、重复覆盖及不同历史独立平局。证据为 [eta_dp_audit.json](eta_dp_audit.json)，审计器为 [audit_eta_complete_tree.py](audit_eta_complete_tree.py)。这只是实现和量词审计，不提高一般候选真值。

保留两个针对明确候选的六人输入，不保留无信息阴性扫描表：

| 输入 | 全部完整 SPE 的最大 (E) 违反量 | 用途 |
| --- | ---: | --- |
| [六人七主题星形](six_star.json) | 0 | 正 η 的系数锐性；[精确输出](six_star_eta.json)核验 19,608 个有序节点、137,256 项比较 |
| [两个三人星形的六人耦合](two_stars_six.json) | −3/4 | 查询菜单跨组件而不能按三人结果直接相加；[精确输出](two_stars_six_eta.json)核验 37,449 个有序节点、299,592 项比较 |

六人星形不是新游戏发现：它参数化了共享 [tax_bridge_counterexample.md](../../../../current/customer_attraction/tax_bridge_counterexample.md) 的三人星形。它与旧 all-big 的 η 现象不同：旧 all-big 最优查询有 η=0，而此族全 B 路径上每层最小 η/r=1，必须支付正总额 m。本文另解析刻画该星形族**全部** SPE 的在轨叶，并证明其最坏 (E) 违反量恰为零；详见同一正文 §4。

已检查旧七客户零 regret 正 reset 的边界；本目录没有用 promotion 免费或 IC regret 唯一付款。原 (E) 本身需要真正全树新关系，当前 DP 是完整有限检验接口，不是该关系。未发现反例以后停止加样本，未把阴性实验写成支持一般真值。

复现：

```sh
python3 research/workspaces/customer-attraction/R-a8ee6fdb155c47da95540775b4a6a2db/tree/audit_eta_complete_tree.py
python3 research/workspaces/customer-attraction/R-a8ee6fdb155c47da95540775b4a6a2db/tree/eta_complete_tree.py research/workspaces/customer-attraction/R-a8ee6fdb155c47da95540775b4a6a2db/tree/six_star.json
python3 research/workspaces/customer-attraction/R-a8ee6fdb155c47da95540775b4a6a2db/tree/eta_complete_tree.py research/workspaces/customer-attraction/R-a8ee6fdb155c47da95540775b4a6a2db/tree/two_stars_six.json
```

脚本可用 `--save-actions --output <本目录内新文件>` 保存完整有序历史策略；默认只保存最坏目标、路径查询表及精确核验计数，整棵策略可由相同确定性算法再生。无优化器或浮点依赖。没有外审或新颖性认证。
