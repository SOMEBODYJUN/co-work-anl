# 精确身份与检查状态

Q-CAG-HALF 原量词仍 OPEN；本轮暂未得到新无条件一般福利界或目标反例。

## R4-SELF-CONSISTENT-POOL-EXISTENCE

对每份原完整 SPE 的所有实际前缀真实单步查询构造共同平均竞争负载。存在主题分布 p，支持仅在该共同分数背景的最佳查询上。

状态：父方一般连续性证明，capacity 已从定义独立重构归一化、极限与纯点 Jensen，未发现致命异议；无外审或新颖性认证。它不含付款、不含新福利界。定义和证明见 [root稿](root/self_consistent_pool.md)。

## R4-SELF-CONSISTENT-POOL-PAYMENT

上述自洽点中，存在一个值 G≤W/m。

状态：OPEN。纯自洽点若存在即可由原 IC 和 Jensen 支付，但纯点一般存在性已被下项否定；混合点存在不等于付款。原目标的真正静态分数安全聚合仍 OPEN。

## R4-PURE-SC-NO

每份原完整 SPE 的真实平均负载算子总有纯自洽主题，为假。

精确见证：m=3、六个不同共同主题、16 单位客户；全部 43 有序决策历史的 258 条比较非负，实际 (0,3,4)，收益 (9/2,5,9/2)，W=14、OPT=16。每个 A 的唯一池化最佳查询分别为 (5,5,5,2,2,2)，全部严格胜过对角。发现只用一份既有完整形式策略锥检验本精确候选，证书不依赖数值最优性。

内部证据：direct 精确单位审计与 construction 独立定义级展开、完整 6×6 查询矩阵。无外审、新颖性或最小性认证。[独立审查](construction/review_no_pure_selfconsistent.md)。本例反而对所有 p 都有 max_T g_T(p)≤107/24<14/3，故不反驳混合 SC 付款、真聚合或 half。

## R4-PREFIX-CAP-SALVAGE

任意原完整 SPE 实际前缀 h_k 强制 A 后，任取完整尾 SPE 终局 y。若第一 k 位至少一人的 y 收益不超过其原实际收益，则 y 属于全部实际位置的 admissible 菜单并集 D；从而前缀总收益 cap 已足够。输出格可以变成更早的经济实际行动列，不保证仍在 D_kA。

若 y 不在 D，则前 k 位全部严格改善，并能把它向上补成一份完整根 SPE。因而对最小福利且在该层最大化首人收益的原 SPE，任意上述 y 若 W(y)≤W，便在 D。

状态：menu 自足全历史拼合证明，capacity 独立重构，root 独立获得 promotion/minW 推论并核对；内部解析检查，未外审或认证新颖性。一般域关系，不是新福利下界；仍缺生产低插入且预算合格端点的交换。[正文](menu/shared_prefix_cap_salvage.md)。

## R4-PB-FRACTIONAL-PLATEAU-NO

任意合法背景版本 FF-LEADER 与局部 δ 链为假：沿既有 PB 完整子 SPE，真正自由分数值 δ 连续三次真实 F 行动保持不变，实际收益 u<δ，故每次局部余额为 u−δ<0。

状态：security 精确鞍点及合法分布构造；induction 独立凸切线、singleton 边界、混合负载与 Fraction 核查通过，root 对稿及复跑。完整全历史 SPE 身份继承已审 PB 定理，本轮未重证整个 PB 策略；无外审/新颖性认证。背景已经覆盖全部客户且未证在轨，不反驳根逐人 δ、根聚合或 half。[正文](security/pb_fractional_saddle_plateau.md)、[内审](induction/independent_review_pb_fractional_plateau.md)。

## R4-POOLED-ALL-P-NO

对每份原完整 SPE、每个查询分布 p，平均所有真实位置竞争负载得到 μ 后总有 mΣ_xp_x/(1+μ_x)≤W，为假。635 单位客户、六主题三人完整策略，全部 258 条 IC 非负；u=(154,154,154)，W=462、OPT=558，坏 p=(e_2+e_5)/2，正差 40617/340340。

状态：security 单次定向发现，direct 独立单位展开精确核验；未外审/认证新颖性或最小性。固定竞争(0,2) cap=154=W/3，所以真正安全值和 δ 聚合仍支付。没有证明坏 p 自洽，不否定 SC 存在付款。[精确输入](security/pooled_mean_background_raw.json)、[独立审计](direct/pooled_635_independent_audit.json)。
