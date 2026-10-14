# 命题账本

本分支现有经过独立重构的奇数环无限下界，完整现行证明在 [research/current/weighted_congestion_frontier.md](../current/weighted_congestion_frontier.md)。下列文献条目保持 Paper Fact；公屏 idea、有限计算和多人赞同本身不升级为 Canonical Record。

## WC-TARGET v1 — OPEN

- Exact Statement / Conclusion：刻画 MODEL 中 a_*(d)，优先全类 o(d) 存在上界或严格提高核实过基线的无限非存在族下界。
- Objects / Domain / Quantifiers / Assumptions / Definitions / Scope：完全采用 MODEL.md；任意有限 E,N、多资源策略、任意正实权、非负系数次数至多 d，不限制人数。
- Dependencies：WC-LIT-UPPER-D、WC-LIT-LOWER、WC-LIT-N 是基线和约束，不是完成证明。
- Evidence：来源 §7 提出缩小缺口；OC-AMPLIFIER-LIMIT-v1 与 OC-AMPLIFIER-ENVELOPE-v1 已给出全类下界 E_d∼d/ln d，严格超过原式(3)参数全域。
- Counterevidence / Objections：没有全类 o(d) 存在证明；仍有对数缺口。该构造的 forcing barrier 不能升级为全类上界；全球优先权未认证。
- Status：OPEN；下界阶段突破已内部独立审查，最终增长阶未判定；Ambition 保持全类。
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

## OC-INTERFACE-v1 — INTERNALLY REVIEWED

- Exact Statement / Conclusion：奇数 m≥3 的 hub/cohort 游戏，若逐点 strict light 与 hub inequalities q_iN_i>p_iP_i、n_ip_iQ_i>q_(i+1)M_(i+1)，则每个纯状态有严格 α-改善。正参数的权重实现等价于 ∏x_i=∏t_i；N_i,Q_i>0 时正系数可行性等价于 ∏n_iN_iQ_i/(M_iP_i)>1。
- Objects / Domain / Quantifiers / Assumptions / Definitions：任意有限奇数环；正 hub/cohort 权、整数 n_i≥1、α>1、主次数 1≤k_i≤d、侧次数 d、正费用系数。资源、策略、全部符号逐项定义在现行页。成本与 strict 边界采用 MODEL。
- Scope：构造族的全状态充分证书与其系数可行性；非一般游戏存在上界。
- Dependencies：MODEL、literal load identities、奇数 parity、正乘积可行性；不导入外部定理。
- Evidence：一般证明；独立先重构后攻击；定义级 Fraction 程序和原 fixture 全状态复算。
- Counterevidence / Objections：偶数环可有交替均衡；不能忽略 weight-cycle 恒等式、侧资源 solo baseline 或 strict 端点。
- Status：Canonical Record of internally reviewed proof；外审未记录；机制可复用，世界新颖性未认证。
- Related Files：../current/weighted_congestion_frontier.md、assets/R1/odd_cycle/README.md、assets/R1/odd_ring_audit/state_review.md。

## OC-AMPLIFIER-LIMIT-v1 — INTERNALLY REVIEWED LOWER BREAKTHROUGH

- Exact Statement：整数 d≥1、0<t<1、1<α<H_d(t)，H_d(t)=((1+t)^d+t^(d+1))/(1+t(1+t)^d)，存在合法有限游戏没有 α-PNE；α,t 有理时全参数可有理。每个 d≥4 存在游戏在 α=d/(ln d+2) 本身仍无 α-PNE。
- Objects / Domain / Quantifiers / Assumptions / Definitions：MODEL 全类内的 binary odd-ring 子类；一个 degree-1 reset，其他主资源和全部侧资源 degree d；人数、权比和系数不受额外限制。
- Scope / Conclusion：a_*(d)≥sup_(0<t<1)H_d(t)（d≥2），以及 d≥4 的显式下界；不声称同一游戏取得 limiting supremum，不给上界或高效构造。
- Dependencies：OC-INTERFACE-v1、有限 R≡1 mod4 与 floor 参数、显式正系数 recipe；数学一般证明无需外部 import。
- Evidence：原冻结 commit a3f0c7a 的 complete proof；本轮两项独立审查；有理 exact coefficient tests；与原式(3)全域 O(√d) ceiling 的自足比较，d≥256 严格超越。
- Counterevidence / Objections：未发现 fatal objection；实例可能极大；有限验证不是无限族证明；文献检索非全球优先权认证。
- Status：完整一般证明与内部独立审查；相对于已核实文献基线满足阶段下界突破，WC-TARGET 仍 OPEN。
- Related Files：../current/weighted_congestion_frontier.md、assets/R1/odd_cycle/general_lower_bound.md、assets/R1/odd_ring_audit/asymptotic_review.md、assets/R1/odd_ring_audit/literature_review.md。

## OC-AMPLIFIER-ENVELOPE-v1 — INTERNALLY REVIEWED

- Exact Statement / Conclusion：每个整数 d≥2，存在游戏没有 E_d-PNE，E_d=d/[(d+1)d^(1/(d+1))−d]>1；a_*(d)≥E_d。构造下界 envelope U_d=max_(0<t<1)H_d(t) 满足 E_d<U_d<E_d+2^(−d)，故 E_d∼d/ln d。
- Objects / Domain / Quantifiers / Assumptions / Definitions / Scope：同一 MODEL 与 OC-AMPLIFIER-LIMIT-v1 构造；E_d 是可排除的显式倍率，U_d 是这一已证下界表达式的最优值，非整个资源拓扑或全类的上界。
- Dependencies：OC-AMPLIFIER-LIMIT-v1；严格凸 g(t)=t+(1+t)^(−d) 的精确最小化及正 correction。
- Evidence：独立 reviewer 一般推导，协调者复核；精确有理小次数构造与明确标注的 Decimal 诊断。
- Counterevidence / Objections：U_d endpoint 未声称由单一游戏达到；浮点 correction 舍入为零不否定严格数学不等式。
- Status：完整内部证明、独立审查；是本轮新 finite-d corollary，不改变上一 claim 身份；外审和全球 priority 未记录。
- Related Files：../current/weighted_congestion_frontier.md、assets/R1/odd_ring_audit/asymptotic_review.md、assets/R1/odd_ring_audit/verify_linear_reset.py。

## OC-LIGHT-FORCING-EXACT-v1 — INTERNALLY REVIEWED

- Exact Statement / Conclusion：对 OC-INTERFACE-v1 游戏、α>1，若每个 light inequality 严格成立，则不存在 α-PNE 当且仅当每个 hub inequality 严格成立。任意失败 hub edge（包括等号）给一个具体 α-PNE：该边唯一同色、其余 hub 边交替、全部 cohort 反位。
- Objects / Domain / Quantifiers / Assumptions / Definitions / Scope：同一正参数奇数环；全 light-forcing 假设是必要范围限制，未证明无此假设的全 topology characterization。
- Dependencies：OC-INTERFACE-v1 的 IF；反位 light 的稳定比较、反色 hub 的稳定比较、唯一同色边赋色。
- Evidence：独立状态审查的一般证明；保存 exact boundary fixtures 和 literal resources 的全部偏离复算。
- Counterevidence / Objections：不能删去所有 light inequalities 的共同前提；其外的全状态覆盖另有机制可能。
- Status：完整内部证明，独立 root 复核，外审未记录；可回收失败边界和真实均衡构造。
- Related Files：../current/weighted_congestion_frontier.md、assets/R1/odd_ring_audit/state_review.md、assets/R1/odd_ring_audit/verify_state_review.py、assets/R1/odd_ring_audit/state_verification.json。

## OC-INTERFACE-BARRIER-v1 — INTERNALLY REVIEWED, RESTRICTED MECHANISM

- Exact Statement / Conclusion：α>1，整数 d≥1，任意环、正 x_i,t_i 满足 weight closure，整数 n_i≥1、1≤k_i,D_i≤d。若该 strict coefficient interface 可行，则 (α−1)(α^(1/d)−1)<1，故它不能超过 (1+o(1))d/ln d。
- Objects / Domain / Quantifiers / Assumptions / Definitions / Scope：仅 OC-INTERFACE-v1 的同时 light/hub inequalities，允许侧次数 D_i 各异；不是 a_*(d) 上界。
- Dependencies：N_i,Q_i>0、weight closure、∏n_i bound、N/M 与 Q/P 比较。
- Evidence：原冻结一般证明和两项独立攻击；与下界构造的 leading constant 相同。
- Counterevidence / Objections：没有所有 light forcing 时不能推出 game 的近似均衡；新 state-covering 机制仍开放。
- Status：完整内部审查的 mechanism obstruction；Truth 与范围已闭合，Novelty 未认证，Ambition 不扩大为全类。
- Related Files：../current/weighted_congestion_frontier.md、assets/R1/odd_cycle/INTERFACE_BARRIER.md、assets/R1/odd_ring_audit/state_review.md。
