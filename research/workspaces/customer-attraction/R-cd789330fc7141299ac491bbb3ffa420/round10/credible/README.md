> 当前后续状态：相邻钱包的existential最优元组/指派版本也已由[root全人数族](../parent/optimal_assignment_adjacent_wallet_counterfamily.md)否定；本页较早OPEN仅为阶段历史。原HALF与较宽弱K桥不受此否定。冻结JSON不原位改写。

# 第十轮 credible：真实完整策略中的相邻退出税反例

2026-10-24，credible10。原对象始终为 Q-CAG-HALF：任意有限共同目录、任意人数、每个完整历史依赖纯 SPE；**主命题仍 OPEN**。本目录的新严格结果只是否定 root 本轮提出的全范围加强 StrongA，不是 HALF 反例。没有新增受限目录正面定理、固定人数常数项目或一般阴性结论。

- `strong_adjacent_counterexample.md`：精确 StrongA、59 类型单位客户完整反例、真正全部历史 IC、弱最优指派版在该点的准确状态及一般人数机制的五人压力测试。
- `strong_adjacent_gap_attack.py` / `strong_adjacent_gap_attack.json`：在本目录已存在的同一完整策略锥中，固定旧端点的 frozen-row 最大查询元组，优化 StrongA 有符号差。精确恢复后的正差为 `2714689114258275`，归一化为 `3143/835942`。输入、每个有序历史的行动及全部精确标量完整保存。
- `audit_strong_adjacent_packet.py` / `strong_adjacent_independent_audit.json`：独立标准库整数实现，不导入规范 solver、cone、scipy 或规范 verifier；核全部 4,681 个决策历史、32,767 个非自身比较，并在同一点枚举全部 32,768 个有序比较元组，得到 840 个最优比较元组的最小 frozen 指派成本。另有 tree10 的真正独立 raw-only 审查，见 `../tree/strong_adjacent_raw_independent_audit.json`。
- `simplify_strong_adjacent_packet.py` / `strong_adjacent_simplified_packet.json`：只在同一个成功策略锥中尝试一次整数客户数压缩。MILP 超时且没有返回可用整数点；没有简化反例，没有得到不可简化的证明。保留原证书。
- `compact_exchange_independent_review.json`：exchange10 随后独立构造了更简洁的 10 单位客户、三人 StrongA 反例。本支另从明确的客户集合与 21 历史策略表直接重建，核 63 个非自身 IC 全通过，`Q11-W9-Csum1=1`；最小最优指派 `(D,D,A)` 给 `Q6`，弱版差 `-4`。应优先用 exchange 的紧凑见证展示 StrongA 失败；本支巨大五人原型只保留来源，不继续压缩。

## 转向前的原目标构造尝试

`bank_upgrade_attempt.py` / `bank_upgrade_attempt_m5.json` 尝试重复辅助银行加 A,A,B 可信残余结构，在参数化的 m 架构上只实例化 m=5 压力。m=5 有八个共同主题，LP 允许全部 255 个非空客户关联类型；不是把旧 PB 的背景或权重搬入原目标。根无外生背景，全部客户与提供者为单位。旧 A,A,B 核及 padding 只作选取真实策略的源种子；对任意 m 的可实现性未证明，每次使用均由真正完整 BI 验证。

`repeated_upgrade_attempt.py` / `repeated_upgrade_attempt_m5.json` 在同一个原目标架构上，用原策略的全部可信孩子菜单重选惩罚，优先最大化不同动作对实际遗漏客户的拥挤；有 129 个 offpath 孩子使用非最小的可信当前利润。两个精确端点分别仅有 `OPT/W=321176/229141` 与 `63464208590/44924837031`，不违反 HALF，不是任何一般正面证据。它们只供应本轮 StrongA 的已有完整策略锥。

`last_profit_pressure.py` 保留同一一般必要坏点关系 `(2m−1)u_m>=2W` 的压力诊断。原 bank 策略锥的精确端点在 `last_profit_original_pressure_m5.json`，比率 `223145/161892`，必要行恰等号，仍非 HALF 反例。refitted 策略锥的 `last_profit_pressure_m5.json` 返回 HiGHS Unknown / primal Infeasible；不把这个浮点状态称为策略锥精确不可行。

## 保存与实际停止位置

只修改本目录；没有 git、work.py、令牌或外部通信调用。StrongA 已被真正完整单位客户 SPE 否定，弱“存在一个最优比较指派”版仍 OPEN。当前证书上的弱版有很大的负差，不能把 StrongA 反例升级为弱版反例或 HALF 反例。没有外审或新颖性认证。
