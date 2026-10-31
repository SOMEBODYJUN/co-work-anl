---
id: customer-attraction/r2fc-round3-global-fractional-floor-safe-action
kind: obstruction
type_tag: 障碍
title: fractional floor 与 safe-action 充分引理的有限探针边界
status: finite-probe-retained
truth_status: finite-random-evidence; no-universal-claim
scope: R-2fc8878b4bdd4328bbc1bcf1df8ca831/round3_global 五个 JSON/脚本；固定随机种子、有限 trial、数值 SLSQP 与 ExactSPESolver 根阈值
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-2fc8878b4bdd4328bbc1bcf1df8ca831/round3_global/fractional_floor_m3q6.json
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-2fc8878b4bdd4328bbc1bcf1df8ca831/round3_global/fractional_floor_m4q7.json
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-2fc8878b4bdd4328bbc1bcf1df8ca831/round3_global/fractional_floor_probe.py
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-2fc8878b4bdd4328bbc1bcf1df8ca831/round3_global/safe_action_m3q6.json
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-2fc8878b4bdd4328bbc1bcf1df8ca831/round3_global/threshold_safe_action_probe.py
evidence_packet: ../../tools/evidence/R-2fc-round3-global-20261031/
---

# 定义域与执行

两个 fractional-floor 报告在固定 `players/topics/seed/trials/seconds` 上随机生成非空客户类型；每个实例调用精确 `ExactSPESolver.threshold((0,...,0))` 得根 floor，再用 SLSQP 在单纯形上最小化分数地板。脚本把正候选标成 `candidate_only`，没有任何全称声称。safe-action 报告/脚本只检查数值阈值下动作组合，不声称存在完整 SPE。

五源均成功读取；脚本 `py_compile` 通过。smoke 副本（3 trials）结果：fractional floor 最佳根/数值 floor 约为 `21/17≈1.2353` 的比值，safe-action `best_bad_action_count=3` 且 `candidate=null`。正式 1000 trial 报告中 m3q6 的最佳比值约 1，m4q7 约 1.1156，safe-action 候选仍为空。

# 处置与数学边界

这些材料是有限随机实验与数值优化诊断。`root_over_fractional≥1` 只说明抽到的记录没有在该数值容差下击穿 floor；`candidate=null` 只说明有限步没有找到指定配置。它们不等于分数 floor 的一般下界、不等于 safe-action 引理成立、不等于对所有完整 SPE 的福利半界，也不构成 Q-CAG-HALF 的证明或反例。后续若要升级，必须给出 exact Fraction 输入、完整历史偏离证书和对所有合法目录/人数的量词处理。
