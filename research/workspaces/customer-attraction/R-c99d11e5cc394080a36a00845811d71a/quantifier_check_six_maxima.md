# Q-CAG-HALF-6 量词边界核对

当前状态：未解决目标；本文件记录一个排除误推的严格量词检查（2026-10-27）。

现有 `six_maxima_joint_bound` 只证明**原共同目录本身**的包含极大覆盖集合数 `s<=6` 时的半覆盖。不能把任意目录中额外主题删掉后套用该定理：删主题会改变每个离轨历史的合法偏离集合及其后继，原完整历史依赖纯 SPE 一般不再是删后目录上的 SPE；同时删除也可能改变真实末位行动的极大性。故“取最优六主题并丢掉其余主题”不是合法量词保持操作。

对原目录固定一份 SPE 和最优六主题，取其六个极大容器并加入实际终局最后行动的极大覆盖，最多得到七个极大集合。于是若试图以 `six_maxima_joint_bound` 覆盖 unrestricted `n=6`，承重点落在恰七极大、六提供者分支。仓库中的 `seven_maxima_checkpoint` 已明确：`n=6` 七极大证书尚缺 44 个 route/比较轨道（扫描共 877 轨道，已有 833）；故不能把该缺口静默当作定理。

精确证据：
- `research/current/customer_attraction/six_maxima_joint_bound.md` 的 theorem scope 明确为“at-most-six-maxima class”。
- `research/current/customer_attraction/seven_maxima_checkpoint.md` 明确恰七极大 `n=5,6` 未闭合，n6 缺 44 轨道。
- `evidence/certificates/customer_attraction/seven_maxima_partial_checkpoint.tar.gz` 中 `scan_n6_seat.json` 给出 877 orbit、45 failures（其中 1 条 rounding failure；44 个真正未证）。

因此本核对的结论是：six-maxima 定理不能直接解决 Q-CAG-HALF-6；当前仍需独立七极大 n6 完成、一般跨目录付款证明，或严格原模型反例。

## Seat-row obstruction (exact)

The attempted n=6 seven-maxima LP used rows named `seat(t,j,k)`. Their implementation has, for a singleton incidence I={j}, coefficient `1/(h+k)` for every k=1,…,n−t. That is not a valid individual SPE lower bound. An exact counterinstance is seven private maxima with multiplicities `(6,1,1,1,1,1,1)` and n=6. The complete history-dependent certificate in `seat_row_counterexample_certificate.json` has terminal `(6,0,0,0,0,0,0)` and passes `verify_certificate` on all 19,608 ordered decision histories (117,648 deviations). Along the root path all six choose B0. For the six B0-private customers, each actual per-customer share is 1/6, whereas `seat(0,0,1)` charges 1; the aggregate row would demand u_0≥6, while actual u_0=1. Hence any LP feasibility obtained by adding all seat rows is not a valid SPE certificate. The valid mechanism only guarantees an order-statistic/r-th-seat statement after selecting an appropriate seat, not every k-row simultaneously.

A stronger continuation-sensitive obstruction invalidates even the route-specific repair `k=1+#(future route-j actions)`. For n=2 with themes B0,B1 and private masses 2 and 1, the complete SPE certificate on path (1,0) (root picks B1; after either root action the follower picks B0) verifies every history. At root, for j=0 the actual route suffix has no future 0, so k=1; a route-count seat row would charge the two B0-private customers at 1 each and require u0≥2, but actual root payoff is 1. The deviation to B0 changes the continuation to B0, yielding only 1 per deviator, so SPE IC does not support the route-row bound. History-dependent replies are the obstruction.
