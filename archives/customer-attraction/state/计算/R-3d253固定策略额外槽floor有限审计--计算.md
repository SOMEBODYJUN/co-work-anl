---
id: customer-attraction/r3d253-fixed-policy-extra-slot-floor
kind: computation
type_tag: 计算
title: R-3d253 固定策略额外槽 floor 有限审计
status: finite-cone-audit-complete; no-certified-violation
truth_status: finite-experiment-only
review_level: full-source-read-and-exact-source-replay
scope: one m=3,p=6 ordered policy cone; three fixed query distributions; companion m=5 two-block count-state report
summary: The fixed cone has root payoff normalized to one and finite LP guarantees below one for all three tested queries. The companion report records a 29/3 threshold but no complete strategy or unit-customer certificate.
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-3d2531ded15f453daef73b30eef82940/credible/probe_extra_slot_floor.py
  - source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-3d2531ded15f453daef73b30eef82940/credible/probe_extra_slot_floor.py
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-3d2531ded15f453daef73b30eef82940/credible/two_block_extra_slot_probe.json
  - source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-3d2531ded15f453daef73b30eef82940/credible/two_block_extra_slot_probe.json
evidence_packet: archives/customer-attraction/tools/evidence/r3d253-credible-extra-slot-Boss8/
legacy_ids:
  - 1722a6701a0af40ad587
  - b3b7b18839b2cdcf27a8
---

# 对象与计算

源脚本读取一份 m=3、p=6 的完整有序策略，枚举 43 个非空决策历史、63 个非空兴趣掩码，并对每个三槽静态背景建立 IC 行和固定查询约束。它分别测试均匀查询、`(10,10,21,10,10,21)/82` 与 `(25,25,9,25,25,9)/118`。三个 HiGHS LP 均成功，根收益归一为 1，最大化的固定查询保证分别为 0.8081729145558925、0.7972906250307196 和 0.7806883069065271；因此该有限锥没有给出根 floor 的严格违反。

Fraction 重建中 uniform 的固定查询值为 `2393/2961`、v4 为 `11381761/14579136`，IC 最小松弛为 0；v3 重建只有约 `-1.25e-47` 的浮点伪负，不能当作精确可行证书。脚本没有精确化 LP 最优点、枚举全部锥顶点，也没有把连续掩码权重转成单位客户。

伴随 JSON 仅保存一个五人、两块的 count-state 统计：`root_threshold=29/3`，12 个 `root_minima` 均为 `29/3`，6188 个计数状态、4368 个终局状态、9496 个保留结果。它不含完整策略、全部偏离行或有理对偶证书。

因此本对象的真值范围是有限计算记录：不构成额外槽安全定理、反例、完整 SPE 或六人半覆盖结论。它与既有固定背景聚合探针和父方额外槽反例保持独立；后续若升级，必须恢复单位客户并对全部有序历史做 Fraction 证书。
