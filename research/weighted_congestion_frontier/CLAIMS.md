# 命题账本

本分支现有团队推导与独立审查中的阶段资产；WC-TARGET v1 仍 OPEN。下列文献条目保持 Paper Fact 身份，新增候选与已完成局部证明分别登记。团队未独立认证所引文献的全文证明。不得把公屏 idea、数值证据或多人赞同升级为 Canonical Record。

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

## WC-ENVELOPE-CEILING v1 — LOCAL PROOF, INTERNALLY REVIEWED

- Exact Statement：论文式(3)两比值的最小值 R 若≥e²，则 R²≤8d ln ln R/(ln R)²；ln d≥16 时 R≤√128·√(d ln ln d)/ln d。
- Objects / Domain / Quantifiers / Assumptions / Definitions / Scope：每个整数d≥1,n≥1,1≤k≤d,实0<w≤1,0≤β≤1；只约束指定两类偏离认证包络。完整身份见下列证明。
- Conclusion：给该证书机制准确有限必要条件；不是a_*(d)上界，不是同拓扑实际最佳均衡因子上界。
- Dependencies：WC-LIT-LOWER v1的精确式(3)，初等log不等式与单变量最大值。
- Evidence：完整一般推导；clean_attack先自主重构后逐行攻击，无fatal objection；Fraction代数与Decimal sanity checks可复现。
- Counterevidence / Objections：不排除不同全状态攻击机制；数值没有严格区间误差保证；外审/新颖性未认证。
- Status：内部独立审查的局部数学资产。Truth有一般证明支持；Value为证书ceiling；Novelty未认证；Mechanism为light衰减与heavy负载跳跃的耦合；Ambition保留主目标OPEN。
- Related Files：[完整证明](assets/R1/envelope_ceiling/README.md)、[核验代码](assets/R1/envelope_ceiling/verify.py)、[结果](assets/R1/envelope_ceiling/verification.json)。

## WC-R1-LF-SHARP v1 — COMPLETE CANDIDATE, REVIEW IN PROGRESS

- Exact Statement：令F_d为论文式(3)对n,k,w,β的参数sup，则F_d∼(2/√e)·√(d ln ln d)/ln d；显式合法参数游戏对每个固定c<2/√e、全部充分大d无任何α<c·√(d ln ln d)/ln d的α-PNE。
- Objects / Domain / Quantifiers / Assumptions / Definitions / Scope：完整采用assets/R1/lower_family/sharp_envelope.md的参数域、全部状态覆盖与sup量词；不假定sup取到。
- Conclusion：细化文献既有族的渐近分析并加强其公开打印的粗渐近下界，未超过文献exact参数sup；不提供全类上界或增长阶匹配。
- Dependencies：WC-LIT-LOWER v1的策略拓扑与式(3)；独立重建的全状态表及uniform一维引理。
- Evidence：完整候选证明、独立内部asymptotic_attack重构；Fraction逐资源全状态与Decimal数值代码结果。clean_attack正在审查冻结稿。
- Counterevidence / Objections：后续文献与优先权未穷尽；同拓扑其他攻击未被该包络上界排除；重要状态提升等待clean review。
- Status：complete candidate。Truth待最后独立攻击；Value/Mechanism为锐渐近与隐藏log-log增益；Novelty未认证；Ambition未满足严格超exact文献族的阶段门槛。
- Related Files：[完整稿](assets/R1/lower_family/sharp_envelope.md)、[代码](assets/R1/lower_family/verify.py)、[结果](assets/R1/lower_family/verification.json)、[来源](assets/R1/lower_family/source_audit.md)。
