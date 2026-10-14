# 命题账本

本分支尚无改善普遍门槛的团队新定理。下列文献条目是 Paper Fact，团队并未独立认证全文证明。局部工具与主目标分开登记；不得把公屏 idea、数值证据或多人赞同升级为 Canonical Record。

## WC-R1-PREFIX-SMOOTHING v1 — LOCAL OBSTRUCTION

- Exact Statement：整数 m≥3，L=3/2−2^(−m)、H=3/2、U=2−2^(−m)。任意非零非负系数有限次数多项式 p 与 ε∈(0,1)，若 p(L)≤εp(H)，则 p(U)/p(H)≥ε^(−2^(m−2))；还必有 d≥log(1/ε)/log(H/L)。
- Objects / Domain / Quantifiers / Assumptions / Definitions：上式量化所有 m、p、ε；三个负载由原 binary-prefix 游戏卫星 a_1 的合法纯状态达到。d 为 p 的次数上限。
- Scope / Conclusion：原阶跃的低泄漏与有界高平台失真不能同时被任意高次非负多项式普遍模拟；不排除利用高端过冲、重配系数、修改权重或拓扑的下界。
- Dependencies：log p(exp t) 的凸性在 proof.md 自足证明；原文 Theorem 5 的权重和策略已核对。
- Evidence：一般证明；标准库 Fraction 检查实际可达负载、全部指定系数向量及次数不等式，结果见 results.json；独立先重构攻击见 review.md。
- Counterevidence / Objections：m=2 不满足所写指数结论；零多项式不作除法；基础分析不主张新颖。该 obstruction 不是 a_*(d) 上界/下界。
- Status：一般证明的局部研究资产，内部独立审查；没有外部评审或完整优先权认证。WC-TARGET v1 仍 OPEN。
- Related Files：assets/R1/prefix_curvature/proof.md、verify.py、results.json、review.md。

## WC-R1-THREELOAD-ENVELOPE v1 — EXACT BASIC TOOL

完整精确身份与一般证明见 [extension.md](assets/R1/prefix_curvature/extension.md)。对任意 0<L<H<U、ε∈(0,1)，在所有非零非负系数多项式且 p(L)≤εp(H) 中，p(U)/p(H) 的精确最小值由相邻两个次数的单项式凸组合取得；可行最小整数次数为 ceil(log(1/ε)/log(H/L))，超过此次数不再降低该最优值。一般离散凸包证明与有理精确回归已完成，主对话知情复核；基础分析工具不主张新颖，不是新博弈门槛。

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
