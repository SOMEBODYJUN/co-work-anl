# R-2fc global_proof left-over two-source cleanup (2026-10-31)

本证据包对应两个由 Boss2 认领的冻结源。`clean-show/` 保存原始返回字节；`source-manifest.json` 记录冻结 SHA/大小与本地副本；`run-manifest.json` 与 `validation.json` 记录复现命令和检查。

## 源级处置

- `background_regret_probe.py` 是 q=6、r=3 的有限随机 Markov SPE 锥浮点 LP 探针。源码读取了完整状态枚举、单步偏离行、fresh/背景目标与 `linprog` 约束；`py_compile` 通过，`--trials 3 --seed 29393` smoke 退出 0，`best=0.0`，没有候选文件。它只给出固定试验范围的 no-hit，不能作为精确证书或全称半值结论。
- `collision_free_obstruction_audit.json` 是五客户、四主题的固定无碰撞 SPE 审计输出。通过 `clean show` 取得的同源 exact Fraction 审计脚本在 `replay/audit_collision_free_obstruction.py` 中重放，输出 JSON 与源逐字相同：`W=4`、`OPT=5`、`Phi=4`、实际路径 `(2,3)`、20 个比较（15 个非自身）、最小松弛 0，且 `2W-OPT=3`。两个最优路径为 `(0,3)` 和 `(3,0)`。

该 obstruction 只说明这个有限实例的某些负载/势桥不能直接当作严格半值反例；其工作值仍满足 `W>=OPT/2`。`background_regret_probe.py` 的浮点候选生成器与上述精确审计属于不同层次，不能把探针 no-hit 或任意浮点 incumbent 升格成定理。
