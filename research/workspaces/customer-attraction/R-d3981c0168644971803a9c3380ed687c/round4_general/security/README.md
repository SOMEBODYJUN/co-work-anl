# round4 security：精确边界与未完成的一般付款

2026-10-24。研究对象严格为Q-CAG-HALF一般共同目录、任意人数、每份完整历史纯SPE。**主目标、真正强/弱聚合安全值、根自由分数聚合桥均保持OPEN；本轮没有新的全输入福利下界。**

## 可复核资产

1. [PB自由分数鞍点及真实前三步平台](pb_fractional_saddle_plateau.md)：从已有PB完整背景SPE定理，推导一个真正自由分数鞍点和显式负载保持混合。任意合法背景FF-LEADER以及局部链 `u+(r−1)δ_child−rδ_parent≥0` 均被严格反驳；前三步真实F的δ完全相同而u<δ。只否定任意背景版本，不能套到零根或在轨前缀版本。`audit_pb_fractional_plateau.py` / `pb_fractional_plateau_audit.json` 精确检查标量与混合；完整SPE依赖旧PB解析证明。本轮新推论已通过 [induction独立内部审查](../induction/independent_review_pb_fractional_plateau.md)，并有 [独立脚本](../induction/independent_check_pb_fractional_plateau.py) 与 [精确输出](../induction/independent_pb_fractional_plateau_checks.json)。旧PB全部历史证明未在本轮重新独立证明；无外审或新颖性认证。
2. [635客户原始输入](pooled_mean_background_raw.json)：对“先跨角色平均真实菜单竞争负载再取倒数”的all-p候选给严格反例，mG−W=40617/340340。W462，OPT558，实际利润全为154；固定对手(0,2)已cap所有查询到154，故不反驳真正安全值或δ聚合。direct在未读发现代码/输出前独立单位展开核查了全部258项IC及上述值，见 [独立审计](../direct/pooled_635_independent_audit.json) 与 [脚本](../direct/audit_pooled_635.py)。发现程序/输出为 `probe_pooled_mean_background.py` / `pooled_mean_background_probe.json`。不再扩展all-p修补或把这些方法障碍作为一般主线。
3. 本目录其余 `probe_*optimal_fractional_payment*`、`probe_*fractional_local_chain*` 与对应JSON：固定旧六主题完整形式策略、固定有理p/q的精确KKT线性约束下做的少量定点数值攻击。均未给反例或证明，最优值落全兴趣客户等号射线。已有FF-LEADER旧资产早做过类似较广诊断；本轮这些工作是重复的阴性诊断，不算一般推进。不得把数值最优0称为锥证书，更不得推广人数/策略。

## KKT为何没有自动给付款

设p*,q*为自由分数鞍点，根k=m−1，D_x=1+kq*_x。记真实角色菜单的平均竞争分布为q_i、平均客户负载μ_ix=k(q_i)_x，并定义

    H_A=Σ_(x∈A) p*_x/D_x²,
    H_q=Σ_A q*_A H_A.

精确倒数展开给

    F_i(p*)−δ_m
      = k[H_q−Σ_A(q_i)_A H_A]
        +Σ_x p*_x(μ_ix−kq*_x)²/[(1+μ_ix)D_x²] ≥0.

第一项非负正是q*的KKT，第二项非负是凸曲率。这只是静态下界及其余量，**没有给真实u_i或W付款**。代回原 `W−Σ_iF_i=Σ_i(e_i+κ_i+J_i)`，仍需共同支付负去相关κ；把这些非负余项列出并不能控制κ。PB推论证明全背景甚至可让优化值连续三步不升而真实u<δ，所以不能把这一KKT松弛当作万能局部钱包。

## 一般m及m=5压力测试

无条件静态界仍为OPT_m≤(2m−1)δ_m；本轮没有证明W与δ的新一般关系。

- 若未来证明根强聚合W≥mδ_m，则一般OPT≤(2−1/m)W；同一推导m=5为OPT_5≤9W/5<2W。
- 较弱根桥W≥(m−1/2)δ_m恰给OPT≤2W；m=5需要W≥(9/2)δ_5。
- 这些均是**条件**结论。本轮PB任意背景局部链失败，KKT测试未形成付款，故没有无条件m=5半覆盖结论。没有开启五人专用扫描、调系数或目录项目。

下一次实质接续应提供根/在轨前缀共同支付的真实新关系，或证明某个适当最优p/池化自洽p的真实菜单能付费；静态KKT、少量定点无反例和任意背景障碍都不能替代该关系。
