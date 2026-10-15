# 命题账本

本分支已有独立审查的奇数环下界和若干结构结果；部分候选仍待审。下列文献条目是 Paper Fact，团队并未独立认证全文证明。不得把公屏 idea、数值证据或多人赞同升级为 Canonical Record。

## WC-TARGET v1 — OPEN

- Exact Statement / Conclusion：刻画 MODEL 中 a_*(d)，优先全类 o(d) 存在上界或严格提高核实过基线的无限非存在族下界。
- Objects / Domain / Quantifiers / Assumptions / Definitions / Scope：完全采用 MODEL.md；任意有限 E,N、多资源策略、任意正实权、非负系数次数至多 d，不限制人数。
- Dependencies：WC-LIT-UPPER-D、WC-LIT-LOWER、WC-LIT-N 是基线和约束，不是完成证明。
- Evidence：奇数环两种有限构造给出 a_*(d)≥T_d∼d/ln d；见现行奇数环证明与逐命题审查表。
- Counterevidence / Objections：全类上界尚未达到同阶；文献后续与精细 finite-d 界须在成功评估前重新核对。
- Status：OPEN；Truth 未判定、Value 取决于贡献、Novelty 未认证、Mechanism 已有奇数环下界，普遍上界机制待研究、Ambition 保持全类。
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


## 入库状态的使用

冻结稿中的“审查中”“父对话待审”是当时状态。当前逐命题状态以根 `research/review_status.json` 和本目录 `FILES.md` 为准；没有审查文件的内容保持候选。缺失的 `resource_cone/review.md`、`nonseparable_frontier/proof.md` 等只登记缺口，不补造证明或审查。

## OC-INTERFACE-v1 — INTERNALLY REVIEWED

- Exact Statement / Conclusion：奇数 m≥3 的 hub/cohort 游戏，若逐点 strict light 与 hub inequalities q_iN_i>p_iP_i、n_ip_iQ_i>q_(i+1)M_(i+1)，则每个纯状态有严格 α-改善。正参数的权重实现等价于 ∏x_i=∏t_i；N_i,Q_i>0 时正系数可行性等价于 ∏n_iN_iQ_i/(M_iP_i)>1。
- Objects / Domain / Quantifiers / Assumptions / Definitions：任意有限奇数环；正 hub/cohort 权、整数 n_i≥1、α>1、主次数 1≤k_i≤d、侧次数 d、正费用系数。资源、策略、全部符号逐项定义在现行页。成本与 strict 边界采用 MODEL。
- Scope：构造族的全状态充分证书与其系数可行性；非一般游戏存在上界。
- Dependencies：MODEL、literal load identities、奇数 parity、正乘积可行性；不导入外部定理。
- Evidence：一般证明；独立先重构后攻击；定义级 Fraction 程序和原 fixture 全状态复算。
- Counterevidence / Objections：偶数环可有交替均衡；不能忽略 weight-cycle 恒等式、侧资源 solo baseline 或 strict 端点。
- Status：Canonical Record of internally reviewed proof；外审未记录；机制可复用，世界新颖性未认证。
- Related Files：../current/weighted_congestion/README.md、research/current/weighted_congestion/odd_ring_linear/README.md、research/reviews/weighted_congestion/odd_ring_linear_audit/state_review.md。


## OC-AMPLIFIER-LIMIT-v1 — INTERNALLY REVIEWED LOWER BREAKTHROUGH

- Exact Statement：整数 d≥1、0<t<1、1<α<H_d(t)，H_d(t)=((1+t)^d+t^(d+1))/(1+t(1+t)^d)，存在合法有限游戏没有 α-PNE；α,t 有理时全参数可有理。每个 d≥4 存在游戏在 α=d/(ln d+2) 本身仍无 α-PNE。
- Objects / Domain / Quantifiers / Assumptions / Definitions：MODEL 全类内的 binary odd-ring 子类；一个 degree-1 reset，其他主资源和全部侧资源 degree d；人数、权比和系数不受额外限制。
- Scope / Conclusion：a_*(d)≥sup_(0<t<1)H_d(t)（d≥2），以及 d≥4 的显式下界；不声称同一游戏取得 limiting supremum，不给上界或高效构造。
- Dependencies：OC-INTERFACE-v1、有限 R≡1 mod4 与 floor 参数、显式正系数 recipe；数学一般证明无需外部 import。
- Evidence：原冻结 commit a3f0c7a 的 complete proof；本轮两项独立审查；有理 exact coefficient tests；与原式(3)全域 O(√d) ceiling 的自足比较，d≥256 严格超越。
- Counterevidence / Objections：未发现 fatal objection；实例可能极大；有限验证不是无限族证明；文献检索非全球优先权认证。
- Status：完整一般证明与内部独立审查；相对于已核实文献基线满足阶段下界突破，WC-TARGET 仍 OPEN。
- Related Files：../current/weighted_congestion/README.md、research/current/weighted_congestion/odd_ring_linear/general_lower_bound.md、research/reviews/weighted_congestion/odd_ring_linear_audit/asymptotic_review.md、research/reviews/weighted_congestion/odd_ring_linear_audit/literature_review.md。


## OC-AMPLIFIER-ENVELOPE-v1 — INTERNALLY REVIEWED

- Exact Statement / Conclusion：每个整数 d≥2，存在游戏没有 E_d-PNE，E_d=d/[(d+1)d^(1/(d+1))−d]>1；a_*(d)≥E_d。构造下界 envelope U_d=max_(0<t<1)H_d(t) 满足 E_d<U_d<E_d+2^(−d)，故 E_d∼d/ln d。
- Objects / Domain / Quantifiers / Assumptions / Definitions / Scope：同一 MODEL 与 OC-AMPLIFIER-LIMIT-v1 构造；E_d 是可排除的显式倍率，U_d 是这一已证下界表达式的最优值，非整个资源拓扑或全类的上界。
- Dependencies：OC-AMPLIFIER-LIMIT-v1；严格凸 g(t)=t+(1+t)^(−d) 的精确最小化及正 correction。
- Evidence：独立 reviewer 一般推导，协调者复核；精确有理小次数构造与明确标注的 Decimal 诊断。
- Counterevidence / Objections：U_d endpoint 未声称由单一游戏达到；浮点 correction 舍入为零不否定严格数学不等式。
- Status：完整内部证明、独立审查；是本轮新 finite-d corollary，不改变上一 claim 身份；外审和全球 priority 未记录。
- Related Files：../current/weighted_congestion/README.md、research/reviews/weighted_congestion/odd_ring_linear_audit/asymptotic_review.md、tests/audits/weighted_congestion/odd_ring_linear_audit/verify_linear_reset.py。


## OC-LIGHT-FORCING-EXACT-v1 — INTERNALLY REVIEWED

- Exact Statement / Conclusion：对 OC-INTERFACE-v1 游戏、α>1，若每个 light inequality 严格成立，则不存在 α-PNE 当且仅当每个 hub inequality 严格成立。任意失败 hub edge（包括等号）给一个具体 α-PNE：该边唯一同色、其余 hub 边交替、全部 cohort 反位。
- Objects / Domain / Quantifiers / Assumptions / Definitions / Scope：同一正参数奇数环；全 light-forcing 假设是必要范围限制，未证明无此假设的全 topology characterization。
- Dependencies：OC-INTERFACE-v1 的 IF；反位 light 的稳定比较、反色 hub 的稳定比较、唯一同色边赋色。
- Evidence：独立状态审查的一般证明；保存 exact boundary fixtures 和 literal resources 的全部偏离复算。
- Counterevidence / Objections：不能删去所有 light inequalities 的共同前提；其外的全状态覆盖另有机制可能。
- Status：完整内部证明，独立 root 复核，外审未记录；可回收失败边界和真实均衡构造。
- Related Files：../current/weighted_congestion/README.md、research/reviews/weighted_congestion/odd_ring_linear_audit/state_review.md、tests/audits/weighted_congestion/odd_ring_linear_audit/verify_state_review.py、evidence/runs/weighted_congestion/odd_ring_linear_audit/state_verification.json。


## OC-INTERFACE-BARRIER-v1 — INTERNALLY REVIEWED, RESTRICTED MECHANISM

- Exact Statement / Conclusion：α>1，整数 d≥1，任意环、正 x_i,t_i 满足 weight closure，整数 n_i≥1、1≤k_i,D_i≤d。若该 strict coefficient interface 可行，则 (α−1)(α^(1/d)−1)<1，故它不能超过 (1+o(1))d/ln d。
- Objects / Domain / Quantifiers / Assumptions / Definitions / Scope：仅 OC-INTERFACE-v1 的同时 light/hub inequalities，允许侧次数 D_i 各异；不是 a_*(d) 上界。
- Dependencies：N_i,Q_i>0、weight closure、∏n_i bound、N/M 与 Q/P 比较。
- Evidence：原冻结一般证明和两项独立攻击；与下界构造的 leading constant 相同。
- Counterevidence / Objections：没有所有 light forcing 时不能推出 game 的近似均衡；新 state-covering 机制仍开放。
- Status：完整内部审查的 mechanism obstruction；Truth 与范围已闭合，Novelty 未认证，Ambition 不扩大为全类。
- Related Files：../current/weighted_congestion/README.md、research/current/weighted_congestion/odd_ring_linear/INTERFACE_BARRIER.md、research/reviews/weighted_congestion/odd_ring_linear_audit/state_review.md。

## WC-ENVELOPE-CEILING v1 — LOCAL PROOF, INTERNALLY REVIEWED

- Exact Statement：论文式(3)两比值的最小值 R 若≥e²，则 R²≤8d ln ln R/(ln R)²；ln d≥16 时 R≤√128·√(d ln ln d)/ln d。
- Objects / Domain / Quantifiers / Assumptions / Definitions / Scope：每个整数d≥1,n≥1,1≤k≤d,实0<w≤1,0≤β≤1；只约束指定两类偏离认证包络。完整身份见下列证明。
- Conclusion：给该证书机制准确有限必要条件；不是a_*(d)上界，不是同拓扑实际最佳均衡因子上界。
- Dependencies：WC-LIT-LOWER v1的精确式(3)，初等log不等式与单变量最大值。
- Evidence：完整一般推导；clean_attack先自主重构后逐行攻击，无fatal objection；Fraction代数与Decimal sanity checks可复现。
- Counterevidence / Objections：不排除不同全状态攻击机制；数值没有严格区间误差保证；外审/新颖性未认证。
- Status：内部独立审查的局部数学资产。Truth有一般证明支持；Value为证书ceiling；Novelty未认证；Mechanism为light衰减与heavy负载跳跃的耦合；Ambition保留主目标OPEN。
- Related Files：[完整证明](../current/weighted_congestion/source_ceiling/README.md)、[核验代码](../../tests/audits/weighted_congestion/source_ceiling/verify.py)、[结果](../../evidence/runs/weighted_congestion/source_ceiling/verification.json)。


## WC-R1-LF-SHARP v1 — COMPLETE CANDIDATE, REVIEW IN PROGRESS

- Exact Statement：令F_d为论文式(3)对n,k,w,β的参数sup，则F_d∼(2/√e)·√(d ln ln d)/ln d；显式合法参数游戏对每个固定c<2/√e、全部充分大d无任何α<c·√(d ln ln d)/ln d的α-PNE。
- Objects / Domain / Quantifiers / Assumptions / Definitions / Scope：完整采用research/questions/weighted_congestion/source_envelope_candidate/sharp_envelope.md的参数域、全部状态覆盖与sup量词；不假定sup取到。
- Conclusion：细化文献既有族的渐近分析并加强其公开打印的粗渐近下界，未超过文献exact参数sup；不提供全类上界或增长阶匹配。
- Dependencies：WC-LIT-LOWER v1的策略拓扑与式(3)；独立重建的全状态表及uniform一维引理。
- Evidence：完整候选证明、独立内部asymptotic_attack重构；Fraction逐资源全状态与Decimal数值代码结果。clean_attack正在审查冻结稿。
- Counterevidence / Objections：后续文献与优先权未穷尽；同拓扑其他攻击未被该包络上界排除；重要状态提升等待clean review。
- Status：complete candidate。Truth待最后独立攻击；Value/Mechanism为锐渐近与隐藏log-log增益；Novelty未认证；Ambition未满足严格超exact文献族的阶段门槛。
- Related Files：[完整稿](../questions/weighted_congestion/source_envelope_candidate/sharp_envelope.md)、[代码](../../tests/audits/weighted_congestion/source_envelope_candidate/verify.py)、[结果](../../evidence/runs/weighted_congestion/source_envelope_candidate/verification.json)、[来源](../reviews/weighted_congestion/source_envelope_candidate/source_audit.md)。

## WC-R1-PREFIX-SMOOTHING v1 — LOCAL OBSTRUCTION

- Exact Statement：整数 m≥3，L=3/2−2^(−m)、H=3/2、U=2−2^(−m)。任意非零非负系数有限次数多项式 p 与 ε∈(0,1)，若 p(L)≤εp(H)，则 p(U)/p(H)≥ε^(−2^(m−2))；还必有 d≥log(1/ε)/log(H/L)。
- Objects / Domain / Quantifiers / Assumptions / Definitions：上式量化所有 m、p、ε；三个负载由原 binary-prefix 游戏卫星 a_1 的合法纯状态达到。d 为 p 的次数上限。
- Scope / Conclusion：原阶跃的低泄漏与有界高平台失真不能同时被任意高次非负多项式普遍模拟；不排除利用高端过冲、重配系数、修改权重或拓扑的下界。
- Dependencies：log p(exp t) 的凸性在 proof.md 自足证明；原文 Theorem 5 的权重和策略已核对。
- Evidence：一般证明；标准库 Fraction 检查实际可达负载、全部指定系数向量及次数不等式，结果见 results.json；独立先重构攻击见 review.md。
- Counterevidence / Objections：m=2 不满足所写指数结论；零多项式不作除法；基础分析不主张新颖。该 obstruction 不是 a_*(d) 上界/下界。
- Status：一般证明的局部研究资产，内部独立审查；没有外部评审或完整优先权认证。WC-TARGET v1 仍 OPEN。
- Related Files：research/current/weighted_congestion/polynomial_curvature/proof.md、verify.py、results.json、review.md。


## WC-R1-THREELOAD-ENVELOPE v1 — EXACT BASIC TOOL

完整精确身份与一般证明见 [extension.md](../current/weighted_congestion/polynomial_curvature/extension.md)。对任意 0<L<H<U、ε∈(0,1)，在所有非零非负系数多项式且 p(L)≤εp(H) 中，p(U)/p(H) 的精确最小值由相邻两个次数的单项式凸组合取得；可行最小整数次数为 ceil(log(1/ε)/log(H/L))，超过此次数不再降低该最优值。一般离散凸包证明与有理精确回归已完成，主对话知情复核；基础分析工具不主张新颖，不是新博弈门槛。


## WC-R1-HET-ENDPOINT-REDUCTION v1 — LOCAL REDUCTION

- Exact Statement：异权两列 star 的重玩家权 1，轻玩家正权 w_i，总重 W；主多项式 p、各卫星多项式 f_i 非负系数且次数≤d。若 α>1 时严格通过 p(1)+Σf_i(1+w_i)>α[p(1+W)+Σf_i(1)] 与每个 p(1+w_i)+f_i(w_i)>α[p(W)+f_i(1+w_i)]，则存在同次数同权整数 star，无 γ-PNE，其中 γ=1+(floor(n)/n)(α−1)>max{1,α−1/(α−1)}、n=W/w_i 为某个选中权重对应的实数中间量。
- Objects / Domain / Quantifiers / Assumptions / Definitions：任意有限人数、任意正实权、任意非负实系数；完整 paired-column star 策略与身份见 endpoint_reduction.md。实数 n 仅用于代数，不是玩家人数。
- Scope / Conclusion：端点强制证书内，异权性不能改变同权多项式 star 认证倍率的增长阶；不是任意 full-state star 的上界，也未导入同权多项式到文献 monomial 包络的还原。
- Dependencies：单调性、主多项式凸性、按权重密度选择与整数向下取整；一般证明自足。
- Evidence：独立先重构攻击通过；实际有理输入/输出各全状态检查，含常数、零卫星与近整数边界，见 verification.json、review.md。
- Counterevidence / Objections：若某个 singleton 由其他偏离者覆盖而不满足所写轻玩家测试，本条不能应用；n<1 的假想残余量也不能自动取整。
- Status：一般证明的局部 reduction，内部独立审查；新颖性与外部评审未认证。WC-TARGET v1 仍 OPEN。
- Related Files：research/current/weighted_congestion/heterogeneous_endpoint/endpoint_reduction.md、verify_endpoint_reduction.py、verification.json、review.md。


## WC-R1-INTEGER-TRIAD v1 — LOCAL ASSET

- Exact Statement / Objects / Domain / Quantifiers / Assumptions / Definitions / Scope / Conclusion：Exactly the six-resource degree-two game with weights (16,2,5); all eight binary profiles and 24 deviations, including endpoint PNE.
- Dependencies / Evidence / Objections / Status / Related Files：完整身份、全部推导和边界见[Integer quadratic triad has exact pure factor 286/267](../current/weighted_congestion/quadratic_triad/proof.md)；精确复算见[tests/audits/weighted_congestion/quadratic_triad/verify.py](../../tests/audits/weighted_congestion/quadratic_triad/verify.py)与[evidence/runs/weighted_congestion/quadratic_triad/verification.json](../../evidence/runs/weighted_congestion/quadratic_triad/verification.json)。完整证明与精确核验已保存，独立审查按五轴表分别登记；外审及新颖性未认证。WC-TARGET v1仍OPEN。


## WC-R1-RESOURCE-SUPPORT v1 — LOCAL ASSET

- Exact Statement / Objects / Domain / Quantifiers / Assumptions / Definitions / Scope / Conclusion：All finite positive-weight congestion games with nonnegative nondecreasing costs and at most r>=1 potential users per resource; unweighted social-cost minimizers are r-PNE. No full-class o(d) claim.
- Dependencies / Evidence / Objections / Status / Related Files：完整身份、全部推导和边界见[Bounded resource user support gives r-PNE](../current/weighted_congestion/resource_support.md)；精确复算见[tests/audits/weighted_congestion/signed_columns/verify.py](../../tests/audits/weighted_congestion/signed_columns/verify.py)与[evidence/runs/weighted_congestion/signed_columns/verification.json](../../evidence/runs/weighted_congestion/signed_columns/verification.json)。完整证明与精确核验已保存，独立审查按五轴表分别登记；外审及新颖性未认证。WC-TARGET v1仍OPEN。


## WC-R1-SOURCE-D2-ENVELOPE v1 — LOCAL ASSET

- Exact Statement / Objects / Domain / Quantifiers / Assumptions / Definitions / Scope / Conclusion：All integer n>=1,k in {1,2}, w,beta in [0,1] in arXiv:2002.07466v3 equation (3); strict polynomial inequalities cover zero denominators. Not a G2 upper bound.
- Dependencies / Evidence / Objections / Status / Related Files：完整身份、全部推导和边界见[Source equation (3) at d=2 has ceiling 19/18](../current/weighted_congestion/quadratic_source/proof.md)；精确复算见[tests/audits/weighted_congestion/quadratic_source/verify.py](../../tests/audits/weighted_congestion/quadratic_source/verify.py)与[evidence/runs/weighted_congestion/quadratic_source/verification.json](../../evidence/runs/weighted_congestion/quadratic_source/verification.json)。完整证明与精确核验已保存，独立审查按五轴表分别登记；外审及新颖性未认证。WC-TARGET v1仍OPEN。

## WC-R1-DAG-STEP v1 — 内部独立证明，辅助模型

- Exact Statement / Objects / Domain / Quantifiers / Assumptions / Definitions / Scope / Conclusion：完全采用 research/current/weighted_congestion/step_dag/proof.md；任意 finite simple DAG 的对称 step dependency game，满足明确严格载荷分离与非负幅度，幅度全域的最佳纯均衡门槛为唯一 q=1+ΣP_kq^{-k}，由正幅度取得。
- Dependencies：真实 threshold 载荷化简、topological greedy、path recursion；完整证明自足。
- Evidence：独立先重构、两份不互相导入的 Fraction literal verifiers。
- Counterevidence / Objections：不属于 G_d 多项式模型；equal load separation 可使化简失效；bounded DAG path height 不自动给 sqrt(m) 界。
- Status：完整内部审查，外审/新颖性未认证。Truth 已内部支持；Value 为 exact dependency 接口；Mechanism 是 path counts；Ambition 辅助。
- Related Files：research/current/weighted_congestion/step_dag/proof.md、research/reviews/weighted_congestion/step_dag/independent_review.md、tests/audits/weighted_congestion/step_dag/verify.py、evidence/runs/weighted_congestion/step_dag/verification.json、tests/audits/weighted_congestion/step_dag/independent_audit.py。

## WC-R1-MULTICOLUMN-2 v1 — INTERNALLY REVIEWED LOCAL RESULT

- Exact Statement / Conclusion：补列多列游戏存在2-PNE；q=3的拓扑最坏最佳均衡倍率的上确界恰为2。一般q固定、n→∞时最坏最佳倍率趋(q−1)/(q−2)，本结论允许次数随n增加。
- Objects / Domain / Quantifiers / Assumptions：每个整数q≥3,n≥1，一个权1重玩家与n个共同轻权0<w≤1玩家；每列主资源共同费用f、各玩家私有卫星共同费用g，任意非负非减f,g。重玩家选整列；轻玩家选该列主资源及自己在其它全部列的卫星。精确费用与U(n,q)见RESULT。
- Definitions / Scope：MODEL成本与α-PNE弱边界；仅上述补列拓扑，不允许偷换为异重、w>1或任意多列游戏。
- Dependencies：固定重列轻玩家精确势最小、非重列平衡、非减性；一般证明不导入外部定理。
- Evidence：完整分支证明、独立先重构后审查、两份Fraction逐资源及人数轨道审计；显式多项式锐性族逐状态覆盖。
- Counterevidence / Objections：未发现对2-PNE证明的fatal objection；w≤1实际用于负载排序，不能省略。sharpness/U补充已由主对话检查，独立审查主要针对核心2-PNE。
- Status：内部审查通过的局部机制障碍；外部审查、新颖性未认证。Truth有自足证明；Value排除自然多列扩展并解释平衡逃逸；Novelty未定；Mechanism平衡轻NE支付重偏离；Ambition局部，不完成WC-TARGET。
- Related Files：research/current/weighted_congestion/multicolumn/RESULT.md、tests/audits/weighted_congestion/multicolumn/verify.py、evidence/runs/weighted_congestion/multicolumn/evidence.json；research/reviews/weighted_congestion/multicolumn_review/REVIEW.md、tests/audits/weighted_congestion/multicolumn_review/verify_multicolumn.py、evidence/runs/weighted_congestion/multicolumn_review/exact_test_results.json。

## WC-R2-DENSITY-MOMENT v1 — COMPLETE INTERNAL PROOF

- Exact Statement/Objects/Domain/Quantifiers/Assumptions/Definitions：任意正实有限多重集，R>1、0<p<1，每个[x,Rx)最多K项（计重数）；sum z^p≤A_R(p)K^(1-p)(sum z)^p，A_R(p)=(1−R^-1)^p/(1−R^-p)。
- Scope/Conclusion：幂矩常数是有限序列的sharp supremum，由K重几何链逼近；不主张均衡因子sharp。
- Dependencies：排序链分解、有限尾和望远镜和凹性，无外部定理。
- Evidence/Objections/Status：[完整证明](../current/weighted_congestion/weight_density.md)及独立内部审查；半开端点、空链、重数已检查，无未处理fatal objection；外审与global priority未认证。
- Related Files：当前完整证明、research/reviews/weighted_congestion/weight_density/review.md、tests/audits/weighted_congestion_density.py、evidence/runs/2026-10-14/weighted_congestion_density.json。


## WC-R2-WEIGHT-DENSITY v1 — COMPLETE INTERNAL PROOF

- Exact Statement/Objects/Domain/Quantifiers/Assumptions：MODEL所有有限游戏、任意正实权与非负degree≤d系数、多资源策略；d≥1，任意R>1,p∈(0,1)，K_R为每资源潜在使用者[x,Rx)最大人数。
- Definitions/Scope/Conclusion：Σw_i^p C_i每个单边局部min是[1+A_R(p)K_R^(1-p)d^p]-PNE，above-factor严格改善终止；K_R=0时全零成本。结构子类，无运行时间保证。d≥3取R=d、p=ln2/lnd得≤1+4K_d，几何分离谱O(log d)。
- Dependencies：WC-R2-DENSITY-MOMENT v1、实际总负载多项式增量界、有限势min。
- Evidence：[完整一般证明](../current/weighted_congestion/weight_density.md)、先自主重构再攻击的内部review、Fraction字面全偏离核验。
- Counterevidence/Objections：K_R全类无界，等权人多时不能直接推出全类o(d)；固定p微权外部增量确无统一界。零cost/空strategy/commonresource均已处理；不声称sharp均衡阈值。
- Status：内部完整证明，Canonical Record限本精确scope；Truth按proof，Value为结构机制，Novelty未认证，Mechanism为敏感度×稀疏moment，Ambition为结构子类；WC-TARGET仍OPEN。
- Related Files：同上一条。

## R2 方法资产 v1 — 完整内部证明，非主目标突破

WC-R2-RESOURCE-POWER-BRIDGE v1、WC-R2-POWER-PATH-OBSTRUCTION v1、
WC-R2-AFFINE-TWO-TYPE v1 的 Exact Statement、Objects、Domain、Quantifiers、Assumptions、
Definitions、Scope、Conclusion、Dependencies、Evidence、Objections、Status、Related Files
完整固定在[规范证明](../current/weighted_congestion/power_bridge.md)第1节，
及根[现行命题登记](../current/claims.md)。依赖分别为谱packing/排序、路径求和、C1梯度/自项；
有限Fraction与独立重构记录均由README索引。外审与新颖性未认证，WC-TARGET仍OPEN。

## R3-SOURCE-SHARP-ASYMPTOTIC-v1 — INTERNAL PROOF

- Exact Statement / Conclusion：原式(3)源域全部参数sup F_d∼(2/√e)√(d ln ln d)/ln d。显式合法family在两类偏离均趋同常数，故a_*(d)≥(2/√e−o(1))同scale。
- Objects / Domain / Quantifiers / Assumptions / Definitions / Scope：d≥2整数，n≥1整数，k∈{1,…,d}，0<w≤1，0≤β≤1；F_d为两认证倍率min之sup，非单游戏exact threshold或全类上界。
- Dependencies：MODEL、源式(3)两个全状态attack（本轮已独立重构）；完整证明不导入既有matching O上界。
- Evidence：research/current/weighted_congestion/source_envelope/proof.md、review.md；Decimal验证仅诊断，未用来证明一般不等式。
- Counterevidence / Objections：未见fatal objection；极慢收敛不影响asymptotic，未认证后续文献全球优先权。源式sup本来已知，因此不称严格超过其基线。
- Status：完整一般证明与独立内部攻击；未外审。Truth有proof、Value给参数优化边界、Novelty未认证、Mechanism全局消元与局部化、Ambition为受限族。
- Related Files：assets/R3/sharp_source_review/、../current/weighted_congestion/README.md、根graph/review_status/assets。


## WC-R3-FULL-TOPOLOGY-REDUCTION v3 — INTERNAL PROOF

- Version history：v1 α≥2；v2 α≥φ、全部w>0；v3 α≥ρ=(1+√3)/2，右支单轻玩家允许w反演；每版范围明确，旧版为subcase。
- Exact Statement：对每个degree≤d对称同轻权两列F,G游戏和每个α≥ρ，若无α-PNE，则存在原式(3)域内monomial参数，其两test均strict通过同α。
- Objects / Domain / Quantifiers / Assumptions / Definitions / Scope：n≥1整数，w>0，F,G任意非负系数degree≤d同主/同副多项式；完整策略参proof；新游戏参数可改变。
- Conclusion：源包络F_d≤actual拓扑sup T_d≤max{ρ,F_d}；F_d≥ρ时T_d=F_d，所以该拓扑与源包络有同一sharp asymptotic。非a_*(d)上界。
- Dependencies：light稳定区间/反射、平移保持系数、右支n′α(α−1)<1和单轻反演、endpoint chord及系数线性消元。
- Evidence：research/current/weighted_congestion/source_topology/proof.md、verify.py/results.json；research/reviews/weighted_congestion/source_topology_review/review.md及独立literal checker。
- Counterevidence / Objections：初版φ仅w≤1的解释已由w≥1时z≥u机制补齐；v3不能坚持整个还原保持原w。F≡0直接存在PNE，zero分母未除。未见fatal objection。
- Status：完整一般证明及独立攻击；未外审、未认证novelty。Truth有proof、Value封闭整个受限搜索、Mechanism为整数稳定区间、Ambition不涉及异权/交叉拓扑。
- Related Files：assets/R3/full_topology/、assets/R3/topology_attack/、../current/weighted_congestion/README.md。


## WC-R3-SOURCE32-178-v1 — COMPLETE STATED SCOPE

- Exact Statement / Conclusion: For every original source parameter, min(H,L)<=89/50; all n,k and real w,beta are covered by analytic reduction plus exact negative interval certificates.
- Objects / Domain / Quantifiers / Assumptions / Definitions / Scope: exact identity in `research/current/weighted_congestion/source_degree32/PROOF.md`; MODEL cost and weak equilibrium conventions apply. No claim of a full-class upper bound.
- Dependencies: WC-SOURCE-FORMULA; all joint premises remain explicit.
- Evidence: evidence/certificates/weighted_congestion/source_degree32/certificate.json, evidence/runs/weighted_congestion/source_degree32/verification.json, evidence/runs/weighted_congestion/crossover/main_check_results.json; separate independently authored verifier and direct reconstruction.
- Counterevidence / Objections: no remaining objection to the exact stated scope; fixed-degree improvement does not prove an unbounded family. External review and priority unverified.
- Status: complete exact statements with independent internal reconstruction; unrefereed. Truth: proved stated scope; Value: reusable separation/sign certificate/failure; Novelty: unassessed; Mechanism: explicit incidence and real-domain elimination; Ambition: WC-TARGET OPEN.
- Related Files: research/current/weighted_congestion/source_degree32/PROOF.md, tests/audits/weighted_congestion/source_degree32/verify.py, tests/audits/weighted_congestion/crossover/main_check.py


## WCF-R3-CROSS32-AUDIT-v1 — COMPLETE STATED SCOPE

- Exact Statement / Conclusion: One explicit rational four-player 14-resource game has strict >9/5 improvement at every pure state; its exact best factor is frozen. No growing lower-family implication.
- Objects / Domain / Quantifiers / Assumptions / Definitions / Scope: exact identity in `research/current/weighted_congestion/crossover/README.md`; MODEL cost and weak equilibrium conventions apply. No claim of a full-class upper bound.
- Dependencies: WC-MODEL; all joint premises remain explicit.
- Evidence: evidence/certificates/weighted_congestion/crossover/degree32_certificate.json, evidence/runs/weighted_congestion/crossover/main_check_results.json; separate independently authored verifier and direct reconstruction.
- Counterevidence / Objections: no remaining objection to the exact stated scope; fixed-degree improvement does not prove an unbounded family. External review and priority unverified.
- Status: complete exact statements with independent internal reconstruction; unrefereed. Truth: proved stated scope; Value: reusable separation/sign certificate/failure; Novelty: unassessed; Mechanism: explicit incidence and real-domain elimination; Ambition: WC-TARGET OPEN.
- Related Files: research/current/weighted_congestion/crossover/README.md, tests/audits/weighted_congestion/crossover/verify_degree32.py, tests/audits/weighted_congestion/crossover/main_check.py


## WCF-R3-FIXED-DEGREE-FAIL-v1 — COMPLETE STATED SCOPE

- Exact Statement / Conclusion: Keeping crossover weights/amplitudes and raising six degrees gives a 9/5-PNE at degree40; best factors converge to 5235403/2930833<9/5. Reweighting is not excluded.
- Objects / Domain / Quantifiers / Assumptions / Definitions / Scope: exact identity in `research/current/weighted_congestion/crossover/README.md`; MODEL cost and weak equilibrium conventions apply. No claim of a full-class upper bound.
- Dependencies: WC-MODEL; all joint premises remain explicit.
- Evidence: evidence/certificates/weighted_congestion/crossover/degree40_failure_certificate.json, evidence/certificates/weighted_congestion/crossover/fixed_weight_limit_certificate.json, evidence/runs/weighted_congestion/crossover/fixed_degree_scan.json, evidence/runs/weighted_congestion/crossover/main_check_results.json; separate independently authored verifier and direct reconstruction.
- Counterevidence / Objections: no remaining objection to the exact stated scope; fixed-degree improvement does not prove an unbounded family. External review and priority unverified.
- Status: complete exact statements with independent internal reconstruction; unrefereed. Truth: proved stated scope; Value: reusable separation/sign certificate/failure; Novelty: unassessed; Mechanism: explicit incidence and real-domain elimination; Ambition: WC-TARGET OPEN.
- Related Files: research/current/weighted_congestion/crossover/README.md, tests/audits/weighted_congestion/crossover/verify_degree32.py, tests/audits/weighted_congestion/crossover/main_check.py


## WC-R3-CROSS32-TOPOLOGY-SEPARATION-v1 — COMPLETE STATED SCOPE

- Exact Statement / Conclusion: T32<=89/50<9/5<B(G), allowing all positive common light weights and arbitrary nonnegative principal/side polynomial coefficients in the symmetric topology.
- Objects / Domain / Quantifiers / Assumptions / Definitions / Scope: exact identity in `research/current/weighted_congestion/crossover/separation.md`; MODEL cost and weak equilibrium conventions apply. No claim of a full-class upper bound.
- Dependencies: WC-R3-SOURCE32-178-v1, WCF-R3-CROSS32-AUDIT-v1, WC-R3-FULL-TOPOLOGY-REDUCTION-v3; all joint premises remain explicit.
- Evidence: evidence/runs/weighted_congestion/crossover/main_check_results.json; separate independently authored verifier and direct reconstruction.
- Counterevidence / Objections: no remaining objection to the exact stated scope; fixed-degree improvement does not prove an unbounded family. External review and priority unverified.
- Status: complete exact statements with independent internal reconstruction; unrefereed. Truth: proved stated scope; Value: reusable separation/sign certificate/failure; Novelty: unassessed; Mechanism: explicit incidence and real-domain elimination; Ambition: WC-TARGET OPEN.
- Related Files: research/current/weighted_congestion/crossover/separation.md, tests/audits/weighted_congestion/crossover/main_check.py


## WC-R3-DENSE-SHARE-v1 — COMPLETE STATED SCOPE

- Exact Statement / Conclusion: For all positive real finite weight sets and nonnegative polynomial c, uniform Shapley shares of W*c(W) have increasing raw shares, decreasing shares per weight, and minw*c(W)<=phi_i<=maxw*c(W).
- Objects / Domain / Quantifiers / Assumptions / Definitions / Scope: full exact identity in `research/current/weighted_congestion/weight_bands/README.md`; arbitrary positive real weights where universally quantified, specified rational amplitudes for constructive families, MODEL weak cost inequalities.
- Dependencies: WC-MODEL and the direct proof in the linked account. No unproved migration between models.
- Evidence: authored general proof, independently reconstructed review `research/reviews/weighted_congestion/weight_bands_review/independent_review.md`, and actual exact code/records listed below. Finite sampling remains separate from proof.
- Counterevidence / Objections: selector failures do not prove nonexistence; occupied interval is not every geometric interval; retuned m1,m2 fail; cubic boundary is only for prescribed witnesses. No unresolved fatal objection within stated scope.
- Status: complete stated-scope proofs with independent internal reconstruction; unrefereed. Truth: stated scope proved; Value: reusable interface/obstruction/reduction; Novelty: unassessed; Mechanism: explicit linked derivation; Ambition: full WC-TARGET remains OPEN.
- Related Files: research/current/weighted_congestion/weight_bands/README.md, research/reviews/weighted_congestion/weight_bands_review/independent_review.md, tests/audits/weighted_congestion/weight_bands/verify.py, tests/audits/weighted_congestion/weight_bands_review/independent_check.py, evidence/runs/weighted_congestion/weight_bands/verification.json, evidence/runs/weighted_congestion/weight_bands_review/independent_verification.json


## WC-R3-DENSE-LOCAL-v1 — COMPLETE STATED SCOPE

- Exact Statement / Conclusion: For every finite polynomial congestion game, resource potential-user weight ratio at most R>=1 ensures every stated scaled-potential minimizer is R-PNE, with no degree or cardinality factor. Empty strategies and zero costs included.
- Objects / Domain / Quantifiers / Assumptions / Definitions / Scope: full exact identity in `research/current/weighted_congestion/weight_bands/README.md`; arbitrary positive real weights where universally quantified, specified rational amplitudes for constructive families, MODEL weak cost inequalities.
- Dependencies: WC-MODEL, WC-R3-DENSE-SHARE-v1 and the direct proof in the linked account. No unproved migration between models.
- Evidence: authored general proof, independently reconstructed review `research/reviews/weighted_congestion/weight_bands_review/independent_review.md`, and actual exact code/records listed below. Finite sampling remains separate from proof.
- Counterevidence / Objections: selector failures do not prove nonexistence; occupied interval is not every geometric interval; retuned m1,m2 fail; cubic boundary is only for prescribed witnesses. No unresolved fatal objection within stated scope.
- Status: complete stated-scope proofs with independent internal reconstruction; unrefereed. Truth: stated scope proved; Value: reusable interface/obstruction/reduction; Novelty: unassessed; Mechanism: explicit linked derivation; Ambition: full WC-TARGET remains OPEN.
- Related Files: research/current/weighted_congestion/weight_bands/README.md, research/reviews/weighted_congestion/weight_bands_review/independent_review.md, tests/audits/weighted_congestion/weight_bands/verify.py, tests/audits/weighted_congestion/weight_bands_review/independent_check.py, evidence/runs/weighted_congestion/weight_bands/verification.json, evidence/runs/weighted_congestion/weight_bands_review/independent_verification.json


## WC-R3-DENSE-POT-SHARP-v1 — COMPLETE STATED SCOPE

- Exact Statement / Conclusion: For every fixed R>1, an explicit finite-game sequence of local ratio R has unique stated-potential minimizers with factors tending to R, while each game has an exact PNE.
- Objects / Domain / Quantifiers / Assumptions / Definitions / Scope: full exact identity in `research/current/weighted_congestion/weight_bands/README.md`; arbitrary positive real weights where universally quantified, specified rational amplitudes for constructive families, MODEL weak cost inequalities.
- Dependencies: WC-MODEL, WC-R3-DENSE-SHARE-v1 and the direct proof in the linked account. No unproved migration between models.
- Evidence: authored general proof, independently reconstructed review `research/reviews/weighted_congestion/weight_bands_review/independent_review.md`, and actual exact code/records listed below. Finite sampling remains separate from proof.
- Counterevidence / Objections: selector failures do not prove nonexistence; occupied interval is not every geometric interval; retuned m1,m2 fail; cubic boundary is only for prescribed witnesses. No unresolved fatal objection within stated scope.
- Status: complete stated-scope proofs with independent internal reconstruction; unrefereed. Truth: stated scope proved; Value: reusable interface/obstruction/reduction; Novelty: unassessed; Mechanism: explicit linked derivation; Ambition: full WC-TARGET remains OPEN.
- Related Files: research/current/weighted_congestion/weight_bands/README.md, research/reviews/weighted_congestion/weight_bands_review/independent_review.md, tests/audits/weighted_congestion/weight_bands/verify.py, evidence/runs/weighted_congestion/weight_bands/verification.json


## WC-R3-BAND-CURL-v1 — COMPLETE STATED SCOPE

- Exact Statement / Conclusion: Two users of weights 1,M>1 with cubic total cost give incompatible mixed differences kappa versus kappa/M for separately normalized Shapley marginals. This does not rule out weighted or other potentials.
- Objects / Domain / Quantifiers / Assumptions / Definitions / Scope: full exact identity in `research/current/weighted_congestion/weight_bands/README.md`; arbitrary positive real weights where universally quantified, specified rational amplitudes for constructive families, MODEL weak cost inequalities.
- Dependencies: WC-R3-DENSE-SHARE-v1 and the direct proof in the linked account. No unproved migration between models.
- Evidence: authored general proof, independently reconstructed review `research/reviews/weighted_congestion/weight_bands_review/independent_review.md`, and actual exact code/records listed below. Finite sampling remains separate from proof.
- Counterevidence / Objections: selector failures do not prove nonexistence; occupied interval is not every geometric interval; retuned m1,m2 fail; cubic boundary is only for prescribed witnesses. No unresolved fatal objection within stated scope.
- Status: complete stated-scope proofs with independent internal reconstruction; unrefereed. Truth: stated scope proved; Value: reusable interface/obstruction/reduction; Novelty: unassessed; Mechanism: explicit linked derivation; Ambition: full WC-TARGET remains OPEN.
- Related Files: research/current/weighted_congestion/weight_bands/README.md, research/reviews/weighted_congestion/weight_bands_review/independent_review.md, tests/audits/weighted_congestion/weight_bands/verify.py, evidence/runs/weighted_congestion/weight_bands/verification.json


## WC-R3-BAND-LINEAR-v1 — COMPLETE STATED SCOPE

- Exact Statement / Conclusion: For every integer d>=7 the specified unmodified/scaled Shapley selector has unique minima with factor at least d/6 although exact PNE exists. Optional empty-choice padding makes each potential band arbitrarily dense without rescuing this selector.
- Objects / Domain / Quantifiers / Assumptions / Definitions / Scope: full exact identity in `research/current/weighted_congestion/weight_bands/README.md`; arbitrary positive real weights where universally quantified, specified rational amplitudes for constructive families, MODEL weak cost inequalities.
- Dependencies: WC-MODEL, WC-R3-DENSE-SHARE-v1 and the direct proof in the linked account. No unproved migration between models.
- Evidence: authored general proof, independently reconstructed review `research/reviews/weighted_congestion/weight_bands_review/independent_review.md`, and actual exact code/records listed below. Finite sampling remains separate from proof.
- Counterevidence / Objections: selector failures do not prove nonexistence; occupied interval is not every geometric interval; retuned m1,m2 fail; cubic boundary is only for prescribed witnesses. No unresolved fatal objection within stated scope.
- Status: complete stated-scope proofs with independent internal reconstruction; unrefereed. Truth: stated scope proved; Value: reusable interface/obstruction/reduction; Novelty: unassessed; Mechanism: explicit linked derivation; Ambition: full WC-TARGET remains OPEN.
- Related Files: research/current/weighted_congestion/weight_bands/README.md, research/reviews/weighted_congestion/weight_bands_review/independent_review.md, tests/audits/weighted_congestion/weight_bands/verify.py, evidence/runs/weighted_congestion/weight_bands/verification.json


## WCF-R3-SCALED-ORIGINAL-v1 — COMPLETE STATED SCOPE

- Exact Statement / Conclusion: For weights (1,1/(10m),1/(20m),1/(50m)), six degrees32m^2 and original amplitudes, B(G_m)->65/34 and every m>=1 has no9/5-PNE. Any fixed alpha<65/34 is obstructed for all sufficiently large m.
- Objects / Domain / Quantifiers / Assumptions / Definitions / Scope: full exact identity in `research/current/weighted_congestion/crossover/limit_family.md`; arbitrary positive real weights where universally quantified, specified rational amplitudes for constructive families, MODEL weak cost inequalities.
- Dependencies: WC-MODEL and the direct proof in the linked account. No unproved migration between models.
- Evidence: authored general proof, independently reconstructed review `research/reviews/weighted_congestion/crossover_limit_review/review.md`, and actual exact code/records listed below. Finite sampling remains separate from proof.
- Counterevidence / Objections: selector failures do not prove nonexistence; occupied interval is not every geometric interval; retuned m1,m2 fail; cubic boundary is only for prescribed witnesses. No unresolved fatal objection within stated scope.
- Status: complete stated-scope proofs with independent internal reconstruction; unrefereed. Truth: stated scope proved; Value: reusable interface/obstruction/reduction; Novelty: unassessed; Mechanism: explicit linked derivation; Ambition: full WC-TARGET remains OPEN.
- Related Files: research/current/weighted_congestion/crossover/limit_family.md, research/reviews/weighted_congestion/crossover_limit_review/review.md, tests/audits/weighted_congestion/crossover/verify_limit.py, tests/audits/weighted_congestion/crossover_limit_review/check_independent.py, evidence/runs/weighted_congestion/crossover/limit_evidence/finite_scans.json, evidence/runs/weighted_congestion/crossover/limit_evidence/scaled_limits.json, evidence/runs/weighted_congestion/crossover/limit_evidence/uniform_bounds.json, evidence/certificates/weighted_congestion/crossover/limit_evidence/retuned_m3_certificate.json, evidence/runs/weighted_congestion/crossover_limit_review/independent_evidence.json


## WCF-R3-SCALED-RETUNED-v2 — COMPLETE STATED SCOPE

- Exact Statement / Conclusion: With exactly the displayed retuned rational amplitudes, every m>=20 and separately m=3 gives no2-PNE; m=1,2 have2-PNE; B(G_m)->100/49. Version1 m>=52 is a proved subcase, not silently rewritten.
- Objects / Domain / Quantifiers / Assumptions / Definitions / Scope: full exact identity in `research/current/weighted_congestion/crossover/limit_family.md`; arbitrary positive real weights where universally quantified, specified rational amplitudes for constructive families, MODEL weak cost inequalities.
- Dependencies: WC-MODEL and the direct proof in the linked account. No unproved migration between models.
- Evidence: authored general proof, independently reconstructed review `research/reviews/weighted_congestion/crossover_limit_review/review.md`, and actual exact code/records listed below. Finite sampling remains separate from proof.
- Counterevidence / Objections: selector failures do not prove nonexistence; occupied interval is not every geometric interval; retuned m1,m2 fail; cubic boundary is only for prescribed witnesses. No unresolved fatal objection within stated scope.
- Status: complete stated-scope proofs with independent internal reconstruction; unrefereed. Truth: stated scope proved; Value: reusable interface/obstruction/reduction; Novelty: unassessed; Mechanism: explicit linked derivation; Ambition: full WC-TARGET remains OPEN.
- Related Files: research/current/weighted_congestion/crossover/limit_family.md, research/reviews/weighted_congestion/crossover_limit_review/review.md, tests/audits/weighted_congestion/crossover/verify_limit.py, tests/audits/weighted_congestion/crossover_limit_review/check_independent.py, evidence/runs/weighted_congestion/crossover/limit_evidence/finite_scans.json, evidence/runs/weighted_congestion/crossover/limit_evidence/scaled_limits.json, evidence/runs/weighted_congestion/crossover/limit_evidence/uniform_bounds.json, evidence/certificates/weighted_congestion/crossover/limit_evidence/retuned_m3_certificate.json, evidence/runs/weighted_congestion/crossover_limit_review/independent_evidence.json


## WCF-R3-SCALED-TEMPLATE-v1 — COMPLETE STATED SCOPE

- Exact Statement / Conclusion: For every real 1<=alpha<r, r>2 root of r^3-r^2-2r-1, fixed rational amplitudes and a finite M yield strict alpha improvement at every state for all m>=M. The selected-witness cone is infeasible at alpha>=r; full-topology optimality is unclaimed.
- Objects / Domain / Quantifiers / Assumptions / Definitions / Scope: full exact identity in `research/current/weighted_congestion/crossover/limit_family.md`; arbitrary positive real weights where universally quantified, specified rational amplitudes for constructive families, MODEL weak cost inequalities.
- Dependencies: WC-MODEL and the direct proof in the linked account. No unproved migration between models.
- Evidence: authored general proof, independently reconstructed review `research/reviews/weighted_congestion/crossover_limit_review/review.md`, and actual exact code/records listed below. Finite sampling remains separate from proof.
- Counterevidence / Objections: selector failures do not prove nonexistence; occupied interval is not every geometric interval; retuned m1,m2 fail; cubic boundary is only for prescribed witnesses. No unresolved fatal objection within stated scope.
- Status: complete stated-scope proofs with independent internal reconstruction; unrefereed. Truth: stated scope proved; Value: reusable interface/obstruction/reduction; Novelty: unassessed; Mechanism: explicit linked derivation; Ambition: full WC-TARGET remains OPEN.
- Related Files: research/current/weighted_congestion/crossover/limit_family.md, research/reviews/weighted_congestion/crossover_limit_review/review.md, tests/audits/weighted_congestion/crossover/verify_limit.py, tests/audits/weighted_congestion/crossover_limit_review/check_independent.py, evidence/runs/weighted_congestion/crossover/limit_evidence/finite_scans.json, evidence/runs/weighted_congestion/crossover/limit_evidence/scaled_limits.json, evidence/runs/weighted_congestion/crossover/limit_evidence/uniform_bounds.json, evidence/certificates/weighted_congestion/crossover/limit_evidence/retuned_m3_certificate.json, evidence/runs/weighted_congestion/crossover_limit_review/independent_evidence.json


## WC-R3-POTENTIAL-DENSITY-PADDING-v1 — COMPLETE STATED SCOPE

- Exact Statement / Conclusion: Arbitrary finite empty/{e} positive-weight padding preserves all finite-alpha equilibrium projection/lift and original deviation costs. Every occupied potential-weight interval can have minimum count L, yet that subclass and the full G_d have identical successful-factor sets and thresholds.
- Objects / Domain / Quantifiers / Assumptions / Definitions / Scope: full exact identity in `research/current/weighted_congestion/density_padding/proof.md`; arbitrary positive real weights where universally quantified, specified rational amplitudes for constructive families, MODEL weak cost inequalities.
- Dependencies: WC-MODEL and the direct proof in the linked account. No unproved migration between models.
- Evidence: authored general proof, independently reconstructed review `research/reviews/weighted_congestion/density_padding/review.md`, and actual exact code/records listed below. Finite sampling remains separate from proof.
- Counterevidence / Objections: selector failures do not prove nonexistence; occupied interval is not every geometric interval; retuned m1,m2 fail; cubic boundary is only for prescribed witnesses. No unresolved fatal objection within stated scope.
- Status: complete stated-scope proofs with independent internal reconstruction; unrefereed. Truth: stated scope proved; Value: reusable interface/obstruction/reduction; Novelty: unassessed; Mechanism: explicit linked derivation; Ambition: full WC-TARGET remains OPEN.
- Related Files: research/current/weighted_congestion/density_padding/proof.md, research/reviews/weighted_congestion/density_padding/review.md, tests/audits/weighted_congestion/density_padding/verify.py, tests/audits/weighted_congestion/density_padding/independent_check.py, evidence/runs/weighted_congestion/density_padding/verification.json, evidence/runs/weighted_congestion/density_padding/independent_verification.json


## WC-R3-ODD-RING-CERTIFICATE-v1 — COMPLETE GENERAL PROOF / INTERNAL REVIEW

- Exact Statement / Conclusion: For odd m>=3, n_i>=1, positive u_i,v_i, 1<=k_i<=d and alpha>1, the specified two strict local tests have positive coefficients iff all N_i,Q_i>0 and product n_i N_i Q_i/(M_i P_i)>1. They exclude alpha-PNE at every state.
- Objects / Domain / Quantifiers / Assumptions / Definitions: full exact identity in `research/current/weighted_congestion/odd_ring/PROOF.md`, sections 1–6; costs and weak alpha-PNE use MODEL.md. Positive rational construction is a subclass of arbitrary positive-real-weight G_d.
- Scope: Fixed exact positive local-test system; iff is coefficient feasibility, not all possible ring nonexistence.
- Dependencies: WC-MODEL; explicit elementary proofs, no imported nonexistence theorem.
- Evidence: complete general proof, independent reconstruction before reading the initial route, two envelope attacks, Fraction full-state small game and separate exact growing-certificate checks.
- Counterevidence / Objections: no unresolved fatal objection in the stated scope; finite tests do not prove generality. Later-literature search is not exhaustive; global priority unverified.
- Status: canonical stated-scope internal mathematical result, unrefereed. Truth: proved scope; Value: growing lower/usable mechanism boundary; Novelty: unverified; Mechanism: odd parity and weight-cycle amplification; Ambition: lower stage breakthrough, WC-TARGET OPEN.
- Related Files: `research/current/weighted_congestion/odd_ring_linear.md`, `research/current/weighted_congestion/odd_ring/PROOF.md`, `tests/audits/weighted_congestion/odd_ring/verify.py`, `evidence/runs/weighted_congestion/odd_ring/verification.json`, `research/reviews/weighted_congestion/odd_ring_independent/REVIEW.md`, `research/reviews/weighted_congestion/odd_ring_independent/EXACT_ENVELOPE_REVIEW.md`, `research/reviews/weighted_congestion/odd_ring_parameters/exact_envelope_review.md`, `research/reviews/weighted_congestion/odd_ring_literature/notes.md`.


## WC-R3-ODD-RING-ENVELOPE-v1 — COMPLETE GENERAL PROOF / INTERNAL REVIEW

- Exact Statement / Conclusion: For each d>=2 and alpha>1, some finite odd ring satisfies the positive monomial local-test system iff alpha<T_d=sup_R>1 [R(1+R)^d+1]/[(1+R)^d+R^(d+1)]. H_d<T_d<=H_d+1/(2^d+1), H_d=d/[(d+1)d^(1/(d+1))-d], hence T_d~d/ln d.
- Objects / Domain / Quantifiers / Assumptions / Definitions: full exact identity in `research/current/weighted_congestion/odd_ring/PROOF.md`, sections 1–6; costs and weak alpha-PNE use MODEL.md. Positive rational construction is a subclass of arbitrary positive-real-weight G_d.
- Scope: Certificate envelope only; failure does not imply an equilibrium. Strict endpoint alpha=T_d is infeasible for these tests.
- Dependencies: WC-MODEL, WC-R3-ODD-RING-CERTIFICATE-v1; explicit elementary proofs, no imported nonexistence theorem.
- Evidence: complete general proof, independent reconstruction before reading the initial route, two envelope attacks, Fraction full-state small game and separate exact growing-certificate checks.
- Counterevidence / Objections: no unresolved fatal objection in the stated scope; finite tests do not prove generality. Later-literature search is not exhaustive; global priority unverified.
- Status: canonical stated-scope internal mathematical result, unrefereed. Truth: proved scope; Value: growing lower/usable mechanism boundary; Novelty: unverified; Mechanism: odd parity and weight-cycle amplification; Ambition: lower stage breakthrough, WC-TARGET OPEN.
- Related Files: `research/current/weighted_congestion/odd_ring_linear.md`, `research/current/weighted_congestion/odd_ring/PROOF.md`, `tests/audits/weighted_congestion/odd_ring/verify.py`, `evidence/runs/weighted_congestion/odd_ring/verification.json`, `research/reviews/weighted_congestion/odd_ring_independent/REVIEW.md`, `research/reviews/weighted_congestion/odd_ring_independent/EXACT_ENVELOPE_REVIEW.md`, `research/reviews/weighted_congestion/odd_ring_parameters/exact_envelope_review.md`, `research/reviews/weighted_congestion/odd_ring_literature/notes.md`.


## WC-R3-ODD-RING-LOWER-v1 — COMPLETE GENERAL PROOF / INTERNAL REVIEW

- Exact Statement / Conclusion: For every integer d>=2 and real 1<=alpha<T_d, a finite rational-weight/coefficient congestion game, all resource latencies positive monomials of degree exactly d, has no alpha-PNE. Therefore a_*(d)>=T_d~d/ln d and liminf a_*(d)ln(d)/d>=1.
- Objects / Domain / Quantifiers / Assumptions / Definitions: full exact identity in `research/current/weighted_congestion/odd_ring/PROOF.md`, sections 1–6; costs and weak alpha-PNE use MODEL.md. Positive rational construction is a subclass of arbitrary positive-real-weight G_d.
- Scope: Game may depend on alpha; unbounded player count/support and huge input size allowed. No endpoint game, polynomial-time construction, full-class upper, matched growth, or global priority claim.
- Dependencies: WC-MODEL, WC-R3-ODD-RING-CERTIFICATE-v1, WC-R3-ODD-RING-ENVELOPE-v1; explicit elementary proofs, no imported nonexistence theorem.
- Evidence: complete general proof, independent reconstruction before reading the initial route, two envelope attacks, Fraction full-state small game and separate exact growing-certificate checks.
- Counterevidence / Objections: no unresolved fatal objection in the stated scope; finite tests do not prove generality. Later-literature search is not exhaustive; global priority unverified.
- Status: canonical stated-scope internal mathematical result, unrefereed. Truth: proved scope; Value: growing lower/usable mechanism boundary; Novelty: unverified; Mechanism: odd parity and weight-cycle amplification; Ambition: lower stage breakthrough, WC-TARGET OPEN.
- Related Files: `research/current/weighted_congestion/odd_ring_linear.md`, `research/current/weighted_congestion/odd_ring/PROOF.md`, `tests/audits/weighted_congestion/odd_ring/verify.py`, `evidence/runs/weighted_congestion/odd_ring/verification.json`, `research/reviews/weighted_congestion/odd_ring_independent/REVIEW.md`, `research/reviews/weighted_congestion/odd_ring_independent/EXACT_ENVELOPE_REVIEW.md`, `research/reviews/weighted_congestion/odd_ring_parameters/exact_envelope_review.md`, `research/reviews/weighted_congestion/odd_ring_literature/notes.md`.


## WC-R3-ODD-RING-POLYNOMIAL-ENVELOPE-v1 — COMPLETE STATED-SCOPE PROOF

- Exact Statement / Conclusion: For d>=2 and alpha>1, allowing each odd-ring group independent nonnegative degree-at-most-d shapes F_i,G_i, common across its action copies/cohort, does not change positive two-local-test feasibility: some finite certificate exists iff alpha<T_d. Constants in mixtures and arbitrary positive real weights are covered; zero shapes cannot satisfy the strict tests.
- Objects / Domain / Quantifiers / Assumptions / Definitions: PROOF.md section8, d>=2, alpha>1, finite odd ring, n_i>=1, nonnegative shapes degree<=d, resource-independent positive weights, shared action/cohort shapes and positive group amplitudes. Feasibility is existential over shapes/parameters.
- Scope: This is a certificate ceiling, not full-class or actual-topology equilibrium existence. Action-specific and clone-specific shape asymmetries are excluded. Sufficiency existential over chosen shapes, not for every prescribed shape.
- Dependencies: WC-R3-ODD-RING-CERTIFICATE-v1 and ENVELOPE-v1, plus exact denominator-weighted convex identities, including degree0 negative factors.
- Evidence: general proof independently attacked; actual Fraction mixed-degree checks with constants, zero-shape exclusions and signed individual differences.
- Counterevidence / Objections: no unresolved fatal within scope; infeasibility does not supply a pure stable profile. General partially aligned cohort and reverse light deviations remain an actual-topology gap.
- Status: stated-scope internally proved, unrefereed. Truth: proved; Value: closes mixed-shape tuning; Novelty: unassessed; Mechanism: convexity with positive denominators; Ambition: boundary, WC-TARGET OPEN.
- Related Files: research/current/weighted_congestion/odd_ring/PROOF.md section8; research/reviews/weighted_congestion/odd_ring_parameters/polynomial_envelope_review.md; check_polynomial_envelope.py; polynomial_envelope_verification.json.


## WC-R3-ODD-RING-SINGLETON-UPPER-v1 — COMPLETE RESTRICTED EXISTENCE PROOF

- Exact Statement / Conclusion: Every odd m>=3 ring with n_i=1 at every group, arbitrary positive real weights, symmetric action copies and nonnegative polynomial fees of degree at most d>=2 (zero fees permitted), has a min{2,T_d}-PNE. A T_d-PNE exists among the 2m single-conflict profiles modulo global action exchange.
- Objects / Domain / Quantifiers / Assumptions / Definitions: every finite odd m>=3, all n_i=1, positive real u_i,v_i, same group fee shape on both action copies, nonnegative degree<=d, d>=2; zero resources allowed. Uses MODEL's weak alpha-PNE, exact pure costs.
- Scope: Restricted actual-topology existence, not sharpness and not a general-cohort or full-model upper. The smaller factor-2 equilibrium is not claimed to be single-conflict when 2<T_d.
- Dependencies: WC-R3-ODD-RING-POLYNOMIAL-ENVELOPE-v1; exact defect-state cycle, correct reversed ring/role map, direct total-cost support-two inequality in PROOF.md section9.
- Evidence: internal independent defect-graph derivation, root reconstruction and exact small graph checks including zero fees and reverse resource/player map. Finite code uses safe alpha=d; endpoint T_d is established by the general proof.
- Counterevidence / Objections: more than one light per group destroys the simple defect-cycle representation; cannot promote this to arbitrary cohorts. No unresolved fatal within stated scope.
- Status: internally proved, unrefereed. Truth: stated subclass proved; Value: actual-topology boundary and representation; Novelty: unverified; Mechanism: arc counting/reversed roles/support; Ambition: structural subcase, WC-TARGET OPEN.
- Related Files: research/current/weighted_congestion/odd_ring/PROOF.md section9; research/reviews/weighted_congestion/odd_ring_parameters/SINGLETON_NOTE.md; check_singleton_graph.py; singleton_graph_verification.json.
