# Boss 根路线：动态门槛与真实跨树支付

当前主目标 Q-CAG-HALF 仍 OPEN。此目录保存本轮 root 对一般候选的自足研究，不改变共享数学账本。

- `threshold_budget.md`：定义完整离轨 SPE 续局集合的最小门槛 `Theta_i`，记录候选 `OPT <= W + ΣTheta_i`、已知 `ΣTheta_i <= W`、以及递归支付缺口。
- 同行 `submodular_route/README.md`：静态联盟/报复损失精确分解。
- 同行 `recursive_state/README.md`：owner tax 的逐客户递归接口。

下一判别是对 THRESHOLD 做一般递归证明或完整反例；有限枚举只作为压力测试。所有特殊人数和结构扩张均停线。

2026-10-24 已添加 `experiments/check_threshold_candidate.py` 及两份 JSON 冻结输出；结果仅为有限压力测试，未改变 Q-CAG-HALF 或 THRESHOLD 的 OPEN 状态。
