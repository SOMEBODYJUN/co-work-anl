# 命题账本

下列文献条目保留 Paper Fact 层级；本轮经整理的局部结果另列。一般证明、有限证据、独立审查与外部发表分别记录，公屏候选不自动升级。

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

## WC-R1-INTEGER-TRIAD v1 — LOCAL ASSET

- Exact Statement / Objects / Domain / Quantifiers / Assumptions / Definitions / Scope / Conclusion：Exactly the six-resource degree-two game with weights (16,2,5); all eight binary profiles and 24 deviations, including endpoint PNE.
- Dependencies / Evidence / Objections / Status / Related Files：完整身份、全部推导和边界见[Integer quadratic triad has exact pure factor 286/267](assets/R1/integer_triad/proof.md)；精确复算见[assets/R1/integer_triad/verify.py](assets/R1/integer_triad/verify.py)与[assets/R1/integer_triad/verification.json](assets/R1/integer_triad/verification.json)。内部独立重构，外审及新颖性未认证。WC-TARGET v1仍OPEN。

## WC-R1-RESOURCE-SUPPORT v1 — LOCAL ASSET

- Exact Statement / Objects / Domain / Quantifiers / Assumptions / Definitions / Scope / Conclusion：All finite positive-weight congestion games with nonnegative nondecreasing costs and at most r>=1 potential users per resource; unweighted social-cost minimizers are r-PNE. No full-class o(d) claim.
- Dependencies / Evidence / Objections / Status / Related Files：完整身份、全部推导和边界见[Bounded resource user support gives r-PNE](assets/R1/cyclic_layers/resource_support.md)；精确复算见[assets/R1/cyclic_layers/verify.py](assets/R1/cyclic_layers/verify.py)与[assets/R1/cyclic_layers/verification.json](assets/R1/cyclic_layers/verification.json)。内部独立重构，外审及新颖性未认证。WC-TARGET v1仍OPEN。

## WC-R1-SOURCE-D2-ENVELOPE v1 — LOCAL ASSET

- Exact Statement / Objects / Domain / Quantifiers / Assumptions / Definitions / Scope / Conclusion：All integer n>=1,k in {1,2}, w,beta in [0,1] in arXiv:2002.07466v3 equation (3); strict polynomial inequalities cover zero denominators. Not a G2 upper bound.
- Dependencies / Evidence / Objections / Status / Related Files：完整身份、全部推导和边界见[Source equation (3) at d=2 has ceiling 19/18](assets/R1/source_d2_envelope/proof.md)；精确复算见[assets/R1/source_d2_envelope/verify.py](assets/R1/source_d2_envelope/verify.py)与[assets/R1/source_d2_envelope/verification.json](assets/R1/source_d2_envelope/verification.json)。内部独立重构，外审及新颖性未认证。WC-TARGET v1仍OPEN。
