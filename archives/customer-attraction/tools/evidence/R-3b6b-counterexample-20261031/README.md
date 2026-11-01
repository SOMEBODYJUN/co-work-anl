# R-3b6b counterexample 小批（2026-10-31）

八个来源均由 `clean show --out` 完整导出。`source-manifest.json` 保存冻结路径、SHA/大小与本地字节核对，`clean-show/` 保存原始 stdout/stderr。

## 精确与有限复放

- `anchor_lift_audit.py` 以计数状态定义完整策略；`--max-players 7` 的 12 条记录与冻结 `anchor_lift_exact.json` 完全相同。每条记录通过全部计数状态的每个动作比较，count invariance 覆盖所有有序历史。AB 分支从 m=2 到 7 的 `(W,OPT)` 为 `(9,10),(13,14),(17,18),(21,22),(25,26),(29,30)`；DE 分支为 `(8,10),(12,14),(16,18),(20,22),(24,26),(28,30)`。m=7 AB 的 `last_threshold_violation=1` 是该辅助桥的阈值读数，不是当前六人 CAG 半值失败；`29>30/2`。
- `certified_m5k7_maximal.json` 声明有限搜索得到的完整五人七主题纯 SPE。独立用仓内 `tmp/weak_matching_replay/customer_attraction` 的定义级验证器复放：2801 个决策历史、16806 个单步偏离、`W=1000`、`OPT=1800`、比值 `9/5`，终局计数和源一致。
- `last_share_m5k7.json` 原文明确是浮点候选未认证。把它交给 `certify_candidate.py` 后，从支持等式恢复整数客户多重集，完整验证得到一个不同的精确点：`W=3, OPT=3`、2801 历史，不能把原浮点 ratio 当作证书。
- `fork_family_search.py` 对 `(forks=2,branches=4,players=5)` 的有限参数网格运行到 `best=1.7`；`cone_search.py` 以固定 seed、2 starts、2 steps smoke 到 `best=1.8`。两者都只生成浮点 LP/候选，未证明存在相应纯 SPE。

本批是 R-3b6b 的辅助桥和有限搜索资料。它没有把辅助模型迁移成当前六人、六提供者、完整有序历史、任意平局的 CAG-HALF 反例，也没有推出一般定理。
