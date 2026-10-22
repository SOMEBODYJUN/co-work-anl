# 可信构造、完整策略锥与区间支付边界

唯一主目标Q-CAG-HALF仍OPEN。所有文件仅涉及共同有限目录、单位客户和单位玩家、全部有序历史纯SPE；
浮点LP/MILP探索不自动成为SPE证书，辅助支付边界也不是主猜想反例。

## 自足一般边界

| 文件 | 内容及当前状态 |
|---|---|
| `exact_floor_half_tightness.md` | q=m−1个不交singleton、m玩家，任意前缀HI=真SPE，但根GI=m/2、所有SPE福利OPT=m−1。证明GI≥cOPT的全人数常数c>1/2不可能。父方已发回盲重构通过；不是GI-half反例。 |
| `audit_exact_floor_tightness.py`、`exact_floor_tightness_audit.json` | 独立真集合BI与HI实现，q1..6共2352前缀核对一般闭式；不导入规范/背景实现。 |
| `two_tail_replication_obstruction.md` | 旧合法单组a/x=2/3例直接复制到每个k≥2均失败：最后fresh C节点改old A，所有真实尾SPE都给7>原6。个人稿，父方尚未记录完成独审。 |
| `audit_replication_obstruction.py`、`replication_obstruction_audit.json` | 从单位客户定义检查k1完整43历史258比较，并核对k2..8两尾全部SPE及类表。一般k依据正文动作类证明。 |

## 有限探索与准确限制

- `two_anchor_cones.py`、`two_anchor_m5.json`、`two_used_m5.json`：两实际锚点与互不交最优叶类的完整策略锥探索；没有超过既有5人9/5比率，不证明全称界。
- `anchor_general_cones.py`、`general_anchor_k2r3*.json`：三锚点、两组、63种任意锚点交叠客户；250个有基准seed完整策略锥最高a/x=1/2。另100个任意seed锥无可行目标，仅记录探索，不排除目录族。
- `anchor_two_tail_milp.py`、`two_tail_milp.json`：固定C0前缀余三人的全部111历史自由策略MILP，非固定锥。120.11秒到时限，仅找到a=0整数候选，8277节点，dual仍a≤2；无最优或不可能结论。
- `interval_cell_attack.py`、`interval_p5m5.json`、`interval_p5m6.json`：完整冻结HI min/max/E/G选择cell。q5m5的500步最高OPT/GI=1.8；q5m6的1000步最高5/3，均有限浮点阴性。边界处excluded动作需重新回放，LP值不是自动合法的HI值。
- `heterogeneous_group_cones.py`、`heterogeneous_k3.json`、`heterogeneous_k3_excess.json`：单尾、三组、允许各组x_i,a_i不同的完整策略锥。250次比率目标最高11/8；300次首组a_1−x_1/2目标最高0。没有证明参数屏障。

2026-10-22上述进程均已结束，报告已稳定；后续持续writer须先输出仓库外、完成后再移入。
当前最有信息的接续义务：区分GI低支付是否来自假终局、不可共同达到的floor，或两者兼有；
前者在singleton族完全消失而后者仍达近半。一般可信坏福利构造仍需实质性地越过共同奖金的old组逃生动作。
