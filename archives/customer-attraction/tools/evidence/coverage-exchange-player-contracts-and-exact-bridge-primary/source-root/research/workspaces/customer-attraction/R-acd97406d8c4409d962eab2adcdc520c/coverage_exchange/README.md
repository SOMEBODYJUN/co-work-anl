# Boss6 coverage_exchange 工作区

2026-10-21。一般 Q-CAG-HALF 仍 OPEN；此目录为内部草稿、审查及有限探针，未自行 git、共享地图或公屏提交。

## 已完成

- `root_near_saturation_review.md`：独立重构 Boss6 `../root_saturation.md` 的一般解析证明，审查通过。特别核对 m=2 分支、I/R 汇总、K=0/m=1 及条件半覆盖范围。
- `player_near_saturation_extension.md`：从根证明提炼 m≥3 任意实际玩家版本；i<m 用真实末位，i=m 用其真实最佳回复与假想 C 的负载估计。母 agent 已收到；候选仍待独立审查。它给 OPT≤(2−1/m)K+(m−1)^2E_i 与 min 收益后的弱无条件边界，不声称解决主目标。

## 弱逐人桥探索

尚未失败的猜想：所有实际玩家 u_i≥OPT_m/(2m)，甚至可能存在更强覆盖保底。已知逐人静态安全值 v_m 的反例并不反驳这个更弱阈值。已告知 Boss6 与 strategy_geometry；后者对若干完整固定策略锥的有限 LP 未找到负值，这不是一般证明。

- `individual_floor_probe.py` / `.jsonl`：随机 3/4/5 人小实例，规范全 SPE 计数集合枚举，检查所有占用主题收益；有限成功，无全称结论。
- `star_floor_probe.py` / `.jsonl`：尖锐大主题/小叶模式的随机非向日葵扰动；仍为有限探索。若输出 `FATAL_WEAK_INDIVIDUAL`，必须提取完整策略并独立定义级核验后再认定反例。

## 当前数学瓶颈

根近饱和仅控制 E_i=m u_i−K 很小时的主题交换。一般情形 (m−1)^2E_i 无已知全局支付，不能据它闭合半覆盖。覆盖交换的真实后继跨分支仍是难点；一一最优主题匹配、逐人残余和前缀余额均未复用为定理。

继续方向：攻击或证明弱逐人 OPT/(2m) 保底；寻找把近饱和交换中 E_i 用多个真实节点共同支付的机制。已有至多六极大结论不作为终点。

## 新失败接口

`k_bridge_failure.md` / `k_plus_m_minus_one_failure.json`：完整三人五主题 SPE 反驳 OPT≤K+(m−1)u_i，失败位于实际末位，55>54。独立定义级核验 `k_bridge_failure_audit.py/.json` 检查31历史/155比较。不能把此例说成弱逐人 OPT/(2m) 或主半覆盖的反例。
