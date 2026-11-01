# R-2fc round3_global fractional-floor 与 safe-action 五源

五个源均由 Boss2 先认领后 `clean show`，返回码为 0；原始 stdout/stderr、冻结 blob/大小/SHA 在 `source-manifest.json`。探针依赖仓库内既有 `exact-spe/customer_attraction` 实现，smoke 运行副本和 stdout/stderr 保存于 `replay/`。

## 数学读数

- `fractional_floor_m3q6.json`：3 名玩家、6 个主题、1000 个随机实例，完整 `ExactSPESolver.threshold` 与数值分数优化。最佳记录 `root_floor=47/3`、分数值约 `15.6666666667`，比值约 1（浮点误差）；源明确 `universal_claim_proved=false`。
- `fractional_floor_m4q7.json`：4 名玩家、7 个主题、1000 个随机实例。最佳 `root_floor=73/2`、分数值约 `32.7174`，`root_over_fractional≈1.1156`，仍是有限数值搜索。
- `fractional_floor_probe.py`：随机客户类型、精确 SPE 根阈值 oracle 与 SLSQP 分数 floor 的比较；正候选需另做精确证书。smoke 以 3 trials 退出 0。
- `safe_action_m3q6.json`：1000 个随机实例，`best_bad_action_count=5`，`candidate=null`；它攻击一个“安全动作充分引理”，源明确不声称 SPE。
- `threshold_safe_action_probe.py`：在每个实例中寻找全部主题均低于数值 floor 而其他玩家保持高于 floor 的候选，使用浮点阈值和有限组合；3 trials smoke 退出 0，未生成候选。

这些结果说明两个具体有限扫描没有找到一般性反例，但没有证明 fractional floor、safe-action 充分性、所有完整 SPE 或六人 Q-CAG-HALF。所有数值量保留浮点/随机/时限量词；不能把 `root_over_fractional>=1` 外推成普遍不等式。
