# 第七轮 transport：静态公式与已否定的强指派桥

第八轮纠正：FOMA-EXISTS/ALL已有旧52客户完整反例；初版OPEN标签错误，root独立重放后修正。见 [正文状态更新](frozen_optimal_assignment_working.md)及 [第八轮复核](../../round8/parent/old_assignment_counterexample_replay.json)。静态BONUS/COST/DUAL公式保留，原有限输出不改，不认领新反例。Q-CAG-HALF仍OPEN。


Q-CAG-HALF 仍 OPEN；本目录没有新的已证 SPE 福利下界或 actual C 共同容量。

- `frozen_optimal_assignment_working.md`：准确候选 FOMA-EXISTS/FOMA-ALL、一般静态交集 bonus 指派形式与充分性；均匀排列和任意比较组合的量词边界。正文是开放工作稿，不是 HALF 证明。
- `audit_frozen_optimal_assignment.py`、`frozen_assignment_existing_audit.json`：只读取既有单位客户完整 SPE 证书，精确重验全部真实历史并检查所定义一般候选的冻结指派；不新造游戏或扩固定人数正面范围。
- `diagnose_frozen_assignment_cones.py`、`frozen_assignment_cone_diagnostic.json`：四个既有完整策略脚手架的一次浮点严格分离诊断；无正候选、无有理对偶、无一般正面结论，不继续扩扫描。重复target严格唯一性的无效范围明确保留。

本轮先恢复 round6 fresh/HIT、SAFE/CLIP 和 round5 rank 密度账。它们的合法恒等式和 Markov 表示没有被当作共同容量；本目录的静态桥与它们不混领费用。root指定的348/34/aggregate/individual旧反例均未分离最佳冻结OPT指派，这只是有限目标检查。

未完成：从全部真实 SPE 约束推出最优交集 bonus 的同一总预算，或用完整 SPE 反例否定准确候选。下一步应攻这个关系本身；不继续固定人数/结构类扩张。不改 round6、不运行 git 或 work.py。
