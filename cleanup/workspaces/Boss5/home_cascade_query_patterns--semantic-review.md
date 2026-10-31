---
source_id: 978ef2be866136ae323d
source_path: examples/unrelated_machines/home_cascade_query_patterns.json
source_sha256: cfb25856400d6d0ee6b6cea9cb100d8545c97fe2025643f8a62260763fc69573
status: ready-for-checkpoint
recommended_disposition: integrated
recommended_targets:
  - archives/unrelated-machines/state/计算/单home级联原程序与分层审查证据--计算.md
  - archives/unrelated-machines/tools/evidence/single-home-cascade-originals/provenance.json
---

# 单home级联输入夹具语义清洗

## 来源与模型边界

该冻结 JSON 是单home级联证据包的输入夹具，不是程序、证明或独立反例。源 ID 为 `978ef2be866136ae323d`，两个冻结提交内容相同，SHA-256 为 `cfb25856400d6d0ee6b6cea9cb100d8545c97fe2025643f8a62260763fc69573`，大小 2742 字节。

它给出 14 台机器、一个 unit job、13 个 home job、三个 query `q1,q2,q3`，以及两份完整分配 `sigma0/sigma1`。`sigma0` 将全部 home job 留在 home，`sigma1` 将 query 送到 unit 端，同时保留零端、单位迁移链和无根费用环。

## 实际读取的精确字段

- `q1` 的 home 为 H1，正小端为 1/8；`q2,q3` 共居 H2，正小端分别为 1/8、1/16。
- `f1,f2` 从 A 经 D/E，`f3` 从 D 到 H2，`f4` 从 B 到 H1，`f5` 从 E 到 W0，`f6` 从 W1 到 K，形成带 unit 迁移的闭包。
- `g` 从 C 到 L；`r0,r1` 构成无根费用环；`z` 从 A 的 1/5 正端可迁移到 Z0 的零端。
- `nonquery_unit_weights` 给出 f1…f6、g、r0、r1 的权重；预期闭包为 A_q1={f1,f2,f3,f5,f6}、A_q2={f4}、A_q3={g}，丢弃 D={r0,r1}，f5 的终点为 W1。
- 八个 `audit_patterns` 对 query 子集逐一给出 peak、delta 和 fee；全 query 的夹具值为 peak 1、delta 0、fee 58，空 query 为 peak 1、delta 3/16、fee 0。

## 与既有证据的关系

现有 `single-home-cascade-originals` 证据包已经保存同一输入副本、原程序、独立 review 和 frozen v2 输出；输入副本 SHA 与本次 clean show 完全一致。frozen v2 记录 `all_checks_passed=true`，八个子集模式的完整分配由既有计算对象解释。本次没有把输入 JSON 当作新的运行，也没有重复声称原构造器已执行。

该夹具支持既有定理的一个有限实例：严格输入、强 home、唯一正小端、零端与 unit 迁移链同时存在；它不扩展到多正小端、弱模式、任意 UM 实例或 customer-attraction 六人 half 模型。无新增数学命题，建议 `integrated` 到现有单home程序/分层审查对象与 provenance。
