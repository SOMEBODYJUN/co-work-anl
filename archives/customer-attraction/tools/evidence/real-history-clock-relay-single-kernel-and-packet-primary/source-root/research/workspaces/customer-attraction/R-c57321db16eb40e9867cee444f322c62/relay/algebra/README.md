# 真实克隆链与 extra-one 候选的精确鉴别

2026-10-22，Boss5 内部研究草稿。CAG-MODEL / Q-CAG-HALF 不变，主目标仍 OPEN；本目录不操作 git 或 work.py。

| 文件 | 精确用途与状态 |
| --- | --- |
| `clone_chain_identity_and_boundary.md` | 任意人数、任意真实历史的复制查询链恒等式，接回同一 mu 的 delta 并保留 S/Z/E/F/DepthSlack；作者推导，直接父方已核对式 (1)-(6)，无一般 drift 根支付。 |
| `probe_clone_drift.py` / `clone_drift_witness.json` | 两客户、两主题、五人的全部 31 个真实节点及 62 个 Fraction SPE 比较。复制查询 slack 为零，但已有查询玩家收益上升 1/6；仅否定逐次克隆松弛支付强桥。 |
| `extra_one_pairwise_counterexample_and_values.md` | 原 13 人完整 packet 给 PAIR-EXTRA-ONE-v1 精确反例 29/11>5/2；同时区分完整 WP、菜单 minmax、自由背景 minmax，避免将强桥失败升级为弱桥失败。 |
| `probe_packet_extra_one.py` / `packet_extra_one_report.json` | 从原 packet 真实边独立重构全部 112050 SPE 行；计算完整六主题 WP 最大、菜单混合 minmax 及 8568 列自由背景混合 minmax，全部最终证书用 Fraction 检查。 |

## 精确 Claim 状态

- **CLONE-CHAIN-IDENTITY-v1：解析恒等式，尚无独立正式审查。** 对任意实际前缀、同一查询 T、全部后继真实节点复制链成立；跨角色差 v-a 与全克隆端点差仍承重。
- **CLONE-DRIFT-BY-LOCAL-SLACK-v1：已假。** “一次复制引起的已有查询玩家收益上升，可由该次复制激励 slack 的非负倍数支付”被两客户完整 SPE 否定。
- **PAIR-EXTRA-ONE-v1：已假。** 对任意两查询的 cross 平均都不超过根收益，被原 36 客户 13 人完整 SPE 否定。
- **一般 WP / 菜单混合桥 / 自由背景混合桥：本目录不作一般结论。** 固定 packet 的完整值分别为 1423/605、25/11、9925/4586，全部小于根收益 5/2。

下一步：若继续克隆路线，先写客户无关的跨链运输核，检验 v-a 的内部净系数是否真正守恒；若继续 extra-one 路线，直接检验完整二次或自由混合候选，保留 diagonal 信用。禁止将上面有限实例的阴性测试上升为一般定理。
