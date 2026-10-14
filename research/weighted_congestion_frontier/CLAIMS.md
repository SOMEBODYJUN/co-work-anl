# 命题账本

本R2工作分支新增两个结构claim，完整身份与一般证明见下述入口。下列文献条目是 Paper Fact，团队并未独立认证全文证明。不得把公屏 idea、数值证据或多人赞同升级为 Canonical Record。

## WC-TARGET v1 — OPEN

- Exact Statement / Conclusion：刻画 MODEL 中 a_*(d)，优先全类 o(d) 存在上界或严格提高核实过基线的无限非存在族下界。
- Objects / Domain / Quantifiers / Assumptions / Definitions / Scope：完全采用 MODEL.md；任意有限 E,N、多资源策略、任意正实权、非负系数次数至多 d，不限制人数。
- Dependencies：WC-LIT-UPPER-D、WC-LIT-LOWER、WC-LIT-N 是基线和约束，不是完成证明。
- Evidence：来源 §7 提出缩小缺口；没有团队主目标证明。
- Counterevidence / Objections：所有新路线均未完成；文献后续与精细 finite-d 界须在成功评估前重新核对。
- Status：OPEN；Truth 未判定、Value 取决于贡献、Novelty 未认证、Mechanism 未发现、Ambition 保持全类。
- Related Files：MODEL.md、LITERATURE.md、PRIOR_ASSETS.md、ACCEPTANCE.md。

## WC-LIT-UPPER-D v1 — PAPER FACT

- Exact Statement：每个 d≥1、每个 G∈G_d 存在 d-PNE。
- Objects / Domain / Quantifiers / Assumptions / Definitions / Scope：MODEL 的全类，纯均衡，费用非负系数多项式。
- Conclusion：a_*(d)≤d，非多项式时间承诺，非最强有限 d 界宣称。
- Dependencies：Caragiannis–Fanelli 的近似势函数存在论证。
- Evidence：arXiv:1902.07173 摘要中 (d+δ) 存在保证，δ∈[0,1] 取零；核心下界论文引言及 §7 引述 d 上界。
- Counterevidence / Objections：还需选择性重建证明；社会成本保证的版本差异不影响本条仅记录存在性。
- Status：Paper Fact；未由团队独立证明；Novelty 无。
- Related Files：LITERATURE.md、PRIOR_ASSETS.md。

## WC-LIT-LOWER v1 — PAPER FACT

- Exact Statement：对每个 d≥2、每个 1≤α<α_lit(d)，核心来源定理1的族中存在一个合法游戏没有 α-PNE；游戏可依 α 变化。其式(3)给参数上确界，且 α_lit(d)=Ω(√d/log d)。不得把未取得的 sup 误写成一个固定参数游戏同时达到全部倍率。
- Objects / Domain / Quantifiers / Assumptions / Definitions / Scope：d≥2，多项式非负系数、重玩家与随 d 可增长的轻玩家；渐近结论是大 d，不是小 d 数值公式。
- Conclusion：a_*(d)≥α_lit(d)；不得将渐近常数下界写成精确门槛。
- Dependencies：全状态分两类的偏离比较及显式参数选择。
- Evidence：arXiv:2002.07466v3 §3、Theorem 1、式(3)及其证明。
- Counterevidence / Objections：sup 的端点不一定由一个参数实例取得；数值优化不替代参数全域证明。
- Status：Paper Fact；团队尚未完整重建；Novelty 无。
- Related Files：LITERATURE.md、PRIOR_ASSETS.md。

## WC-LIT-N v1 — PAPER FACT

- Exact Statement：每个有 n 个玩家、任意正权与非递减资源费用的有限加权原子拥塞博弈存在 n-PNE。
- Objects / Domain / Quantifiers / Assumptions / Definitions / Scope：资源独立玩家权、一般非递减费用；非 player-specific cost、非 resource-dependent weights。
- Conclusion：固定人数不能构造随 d 无界的非存在门槛。
- Dependencies：核心来源 §6、Theorem 4。
- Evidence：论文准确陈述；本轮未重建一般证明。
- Counterevidence / Objections：不得从存在性推导高效计算；人数固定的失败不反驳全类目标。
- Status：Paper Fact；Novelty 无。
- Related Files：LITERATURE.md、MODEL.md。

## WC-R2-DENSITY-MOMENT v1 — COMPLETE INTERNAL PROOF

- Exact Statement/Objects/Domain/Quantifiers/Assumptions/Definitions：任意正实有限多重集，R>1、0<p<1，每个[x,Rx)最多K项（计重数）；sum z^p≤A_R(p)K^(1-p)(sum z)^p，A_R(p)=(1−R^-1)^p/(1−R^-p)。
- Scope/Conclusion：幂矩常数是有限序列的sharp supremum，由K重几何链逼近；不主张均衡因子sharp。
- Dependencies：排序链分解、有限尾和望远镜和凹性，无外部定理。
- Evidence/Objections/Status：[完整证明](../current/weighted_congestion/weight_density.md)及独立内部审查；半开端点、空链、重数已检查，无未处理fatal objection；外审与global priority未认证。
- Related Files：当前完整证明、assets/R2/weight_density/review.md、tests/audits/weighted_congestion_density.py、evidence/runs/2026-10-14/weighted_congestion_density.json。

## WC-R2-WEIGHT-DENSITY v1 — COMPLETE INTERNAL PROOF

- Exact Statement/Objects/Domain/Quantifiers/Assumptions：MODEL所有有限游戏、任意正实权与非负degree≤d系数、多资源策略；d≥1，任意R>1,p∈(0,1)，K_R为每资源潜在使用者[x,Rx)最大人数。
- Definitions/Scope/Conclusion：Σw_i^p C_i每个单边局部min是[1+A_R(p)K_R^(1-p)d^p]-PNE，above-factor严格改善终止；K_R=0时全零成本。结构子类，无运行时间保证。d≥3取R=d、p=ln2/lnd得≤1+4K_d，几何分离谱O(log d)。
- Dependencies：WC-R2-DENSITY-MOMENT v1、实际总负载多项式增量界、有限势min。
- Evidence：[完整一般证明](../current/weighted_congestion/weight_density.md)、先自主重构再攻击的内部review、Fraction字面全偏离核验。
- Counterevidence/Objections：K_R全类无界，等权人多时不能直接推出全类o(d)；固定p微权外部增量确无统一界。零cost/空strategy/commonresource均已处理；不声称sharp均衡阈值。
- Status：内部完整证明，Canonical Record限本精确scope；Truth按proof，Value为结构机制，Novelty未认证，Mechanism为敏感度×稀疏moment，Ambition为结构子类；WC-TARGET仍OPEN。
- Related Files：同上一条。
