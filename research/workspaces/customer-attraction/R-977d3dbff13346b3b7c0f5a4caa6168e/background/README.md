# 背景利润、精确区间递归与层级核攻击

2026-10-21阶段保存。Q-CAG-HALF仍OPEN。本目录没有一般half证明或真实SPE反例。
本次没有重试已被旧Boss7否定的P+λΔ前缀加强；主要进展是两个普遍合法算法引理及一个结构修复。

- `minvector_ceiling_compression.md`：原myopic-ceiling H超集可精确压成q维逐主题最小值向量，L/E/G全部保留；不保留终局相关性。
- `minvector_ceiling_dp.py`、`minvector_regression.json`：Fraction实现及与旧显式H递归的逐状态对照。552例、9132含终局状态、27068坐标；4660非终局L/E/G全相同。
- `interval_ceiling_relaxation.md`：新增双向量区间递归，用孩子终局收益真实最大值替代无后继myopic上界；普遍合法，H_I⊆H_M、L_I≥L_M、G_I≥G_M。仍需证明或反驳G_I(0)≥OPT/2。
- `interval_ceiling_dp.py`、`interval_regression.json`：双向量与独立显式集合实现对照；552例9132状态，664状态严格缩小H、107状态支付改善，24状态仍严格大于真SPE集合。JSON给首个严格放松完整见证。
- 区间正文定理2：公共核K+每主题1私客、m主题m玩家类，在每个合法前缀区间递归均精确支付剩余最优利润，根G_I=OPT_m=K+m。证明为任意m,K的解析归纳，不是有限枚举。
- `common_core_ceiling_probe.py`：原myopic-ceiling在共同公共核类的对称DP探索。仅机制探针，不承担一般half或区间递归结论；m3,K3原G_M=11/2而区间G_I=6。
- `hierarchical_ceiling_probe.py`与`hierarchical_*q8m8.json`：40个八主题八人层级/交叉公共核浮点攻击，最小G_M/OPT约0.75914。`hierarchical_best_q8m16.json`只是中断的16人探索最新值，没有完整summary，不能按12例完成报告。
- `interval_hierarchy_probe.py`与`interval_hierarchical_*q8m8.json`：80个八主题八人同类浮点攻击，最小G_I/OPT约0.824615。未发现half分离，但这不证明任何全称福利界。

下一步应直接攻击区间超集保留的“同一行动中低于阈值的坏终局”，或证明足以控制其总支付损失的普遍机制。
一个可继续的有限精确路线是记录区间递归min/max/allowed选择的线性cell，再用客户重数LP分离；LP候选必须回放真实区间递归，且即使G_I<OPT/2也只否定此辅助支付，不是SPE反例。

续轮定向攻击：区间正文§6解析排除了旧全部在轨/近轨与固定尾深无界族的所有参数；精确审计见`interval_tail_family_audit.py/json`（20个小参数及m7首个旧half失败实例）。一般区间half尚未闭合。
