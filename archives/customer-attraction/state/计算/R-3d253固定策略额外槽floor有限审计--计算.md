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

源脚本读取一份 m=3、p=6 的完整有序策略，枚举 43 个决策历史（含空历史根）、63 个非空兴趣掩码；每个节点对全部六个动作建立 IC 行，共 258 行，再对全部 56 个三槽计数背景建立固定查询约束。它分别测试均匀查询、`(10,10,21,10,10,21)/82` 与 `(25,25,9,25,25,9)/118`。三个 HiGHS LP 均成功，浮点 LP 的根收益约束设为 1，最大化的固定查询保证分别为 0.8081729145558925、0.7972906250307196 和 0.7806883069065271；因此该有限锥没有给出根 floor 的严格违反。

Fraction 重建中 uniform 的固定查询值为 `2393/2961`、v4 为 `11381761/14579136`，IC 最小松弛为 0；v3 重建根收益约为 `1.0000000000116744`，其 IC 有约 `-1.2456091138041423e-11` 的严格负有理松弛，因此恢复点不可行，不能当作精确可行证书。原脚本没有提供有理对偶或全部锥顶点，不能把浮点 optimum 当作精确上界。下面的新核验只认证保存的原始权重点和固定查询值。

伴随 JSON 仅保存一个五人、两块的 count-state 统计：`root_threshold=29/3`，12 个 `root_minima` 均为 `29/3`，6188 个计数状态、4368 个终局状态、9496 个保留结果。它不含完整策略、全部偏离行或有理对偶证书。

因此本对象保留有限计算及下列完整历史的点上证书，不构成普遍额外槽安全定理或六人半覆盖结论。它与既有固定背景聚合探针和父方额外槽反例保持独立。


## 保存点的独立有理核验与数值勘误

上一批把 v3 IC 松弛误写为约 `-1.25e-47`；从保存的分子分母直接求值，应为 `-1.2456091138041423e-11`。保存 JSON 原件未改。`verify_recovered.py` 不导入 LP 或原探针，直接按客户掩码和全部有序终局重算收益，对 43 节点各六动作检查 258 条真实 IC，并用 216 个允许重复的有序三背景覆盖全部 56 个计数背景。三份重建的根收益、最小 IC、固定查询保证均与原保存 Fraction 字段严格相同。

| 保存权重点 | 根收益 | 最小 IC | 固定查询保证 | 清分母倍率 / 单位客户总数 | 完整历史点上结论 |
|---|---:|---:|---:|---:|---|
| uniform | 1 | 0 | 2393/2961 | 329 / 1722 | 三人纯 SPE |
| v3 | 约1.0000000000116744 | 约−1.24561×10⁻¹¹ | 约0.79729 | 不采用 | 恢复点不满足 IC |
| v4 | 1 | 0 | 11381761/14579136 | 61776 / 227556 | 三人纯 SPE |

清分母的实现是：对每个非空兴趣掩码 M 建立 `scale*w_M` 个不同的单位客户，恰由 M 中标签覆盖；标签及完整策略均不合并。非负有理重数转整数后，每个历史的收益和 IC 同比放大。有限完全信息树中每个节点的单步动作比较成立，由逆向归纳给这份完整策略为纯 SPE，含全部离轨历史及平局。该点上认证不要求它是 LP 最优点，也不证明所有权重的上界。

两个认证点的固定查询值均严格低于根收益，只是候选未被它们违反；固定查询不等于对全部查询优化后的安全值。v3 仍严格不可行，不能因误差小就称 SPE。五人两块 JSON 没有因此获得新策略证书。复现依赖、原字节重放及独立输出见 [证据包](../../tools/evidence/r3d253-credible-extra-slot-Boss8/README.md)。
