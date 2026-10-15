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
- Related Files：research/current/weighted_congestion/polynomial_curvature/three_load_curvature_bound.md、verify.py、results.json、review.md。


## WC-R1-THREELOAD-ENVELOPE v1 — EXACT BASIC TOOL

完整精确身份与一般证明见 [extension.md](../current/weighted_congestion/polynomial_curvature/three_point_polynomial_envelope.md)。对任意 0<L<H<U、ε∈(0,1)，在所有非零非负系数多项式且 p(L)≤εp(H) 中，p(U)/p(H) 的精确最小值由相邻两个次数的单项式凸组合取得；可行最小整数次数为 ceil(log(1/ε)/log(H/L))，超过此次数不再降低该最优值。一般离散凸包证明与有理精确回归已完成，主对话知情复核；基础分析工具不主张新颖，不是新博弈门槛。


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
- Dependencies / Evidence / Objections / Status / Related Files：完整身份、全部推导和边界见[Integer quadratic triad has exact pure factor 286/267](../current/weighted_congestion/quadratic_triad/three_player_integer_obstruction.md)；精确复算见[tests/audits/weighted_congestion/quadratic_triad/verify.py](../../tests/audits/weighted_congestion/quadratic_triad/verify.py)与[evidence/runs/weighted_congestion/quadratic_triad/verification.json](../../evidence/runs/weighted_congestion/quadratic_triad/verification.json)。完整证明与精确核验已保存，独立审查按五轴表分别登记；外审及新颖性未认证。WC-TARGET v1仍OPEN。


## WC-R1-RESOURCE-SUPPORT v1 — LOCAL ASSET

- Exact Statement / Objects / Domain / Quantifiers / Assumptions / Definitions / Scope / Conclusion：All finite positive-weight congestion games with nonnegative nondecreasing costs and at most r>=1 potential users per resource; unweighted social-cost minimizers are r-PNE. No full-class o(d) claim.
- Dependencies / Evidence / Objections / Status / Related Files：完整身份、全部推导和边界见[Bounded resource user support gives r-PNE](../current/weighted_congestion/resource_support.md)；精确复算见[tests/audits/weighted_congestion/signed_columns/verify.py](../../tests/audits/weighted_congestion/signed_columns/verify.py)与[evidence/runs/weighted_congestion/signed_columns/verification.json](../../evidence/runs/weighted_congestion/signed_columns/verification.json)。完整证明与精确核验已保存，独立审查按五轴表分别登记；外审及新颖性未认证。WC-TARGET v1仍OPEN。


## WC-R1-SOURCE-D2-ENVELOPE v1 — LOCAL ASSET

- Exact Statement / Objects / Domain / Quantifiers / Assumptions / Definitions / Scope / Conclusion：All integer n>=1,k in {1,2}, w,beta in [0,1] in arXiv:2002.07466v3 equation (3); strict polynomial inequalities cover zero denominators. Not a G2 upper bound.
- Dependencies / Evidence / Objections / Status / Related Files：完整身份、全部推导和边界见[Source equation (3) at d=2 has ceiling 19/18](../current/weighted_congestion/quadratic_source/source_family_envelope.md)；精确复算见[tests/audits/weighted_congestion/quadratic_source/verify.py](../../tests/audits/weighted_congestion/quadratic_source/verify.py)与[evidence/runs/weighted_congestion/quadratic_source/verification.json](../../evidence/runs/weighted_congestion/quadratic_source/verification.json)。完整证明与精确核验已保存，独立审查按五轴表分别登记；外审及新颖性未认证。WC-TARGET v1仍OPEN。

## WC-R1-DAG-STEP v1 — 内部独立证明，辅助模型

- Exact Statement / Objects / Domain / Quantifiers / Assumptions / Definitions / Scope / Conclusion：完全采用 research/current/weighted_congestion/step_dag/step_dependency_threshold.md；任意 finite simple DAG 的对称 step dependency game，满足明确严格载荷分离与非负幅度，幅度全域的最佳纯均衡门槛为唯一 q=1+ΣP_kq^{-k}，由正幅度取得。
- Dependencies：真实 threshold 载荷化简、topological greedy、path recursion；完整证明自足。
- Evidence：独立先重构、两份不互相导入的 Fraction literal verifiers。
- Counterevidence / Objections：不属于 G_d 多项式模型；equal load separation 可使化简失效；bounded DAG path height 不自动给 sqrt(m) 界。
- Status：完整内部审查，外审/新颖性未认证。Truth 已内部支持；Value 为 exact dependency 接口；Mechanism 是 path counts；Ambition 辅助。
- Related Files：research/current/weighted_congestion/step_dag/step_dependency_threshold.md、research/reviews/weighted_congestion/step_dag/independent_review.md、tests/audits/weighted_congestion/step_dag/verify.py、evidence/runs/weighted_congestion/step_dag/verification.json、tests/audits/weighted_congestion/step_dag/independent_audit.py。

## WC-R1-MULTICOLUMN-2 v1 — INTERNALLY REVIEWED LOCAL RESULT

- Exact Statement / Conclusion：补列多列游戏存在2-PNE；q=3的拓扑最坏最佳均衡倍率的上确界恰为2。一般q固定、n→∞时最坏最佳倍率趋(q−1)/(q−2)，本结论允许次数随n增加。
- Objects / Domain / Quantifiers / Assumptions：每个整数q≥3,n≥1，一个权1重玩家与n个共同轻权0<w≤1玩家；每列主资源共同费用f、各玩家私有卫星共同费用g，任意非负非减f,g。重玩家选整列；轻玩家选该列主资源及自己在其它全部列的卫星。精确费用与U(n,q)见RESULT。
- Definitions / Scope：MODEL成本与α-PNE弱边界；仅上述补列拓扑，不允许偷换为异重、w>1或任意多列游戏。
- Dependencies：固定重列轻玩家精确势最小、非重列平衡、非减性；一般证明不导入外部定理。
- Evidence：完整分支证明、独立先重构后审查、两份Fraction逐资源及人数轨道审计；显式多项式锐性族逐状态覆盖。
- Counterevidence / Objections：未发现对2-PNE证明的fatal objection；w≤1实际用于负载排序，不能省略。sharpness/U补充已由主对话检查，独立审查主要针对核心2-PNE。
- Status：内部审查通过的局部机制障碍；外部审查、新颖性未认证。Truth有自足证明；Value排除自然多列扩展并解释平衡逃逸；Novelty未定；Mechanism平衡轻NE支付重偏离；Ambition局部，不完成WC-TARGET。
- Related Files：research/current/weighted_congestion/multicolumn/complement_column_escape.md、tests/audits/weighted_congestion/multicolumn/verify.py、evidence/runs/weighted_congestion/multicolumn/evidence.json；research/reviews/weighted_congestion/multicolumn_review/REVIEW.md、tests/audits/weighted_congestion/multicolumn_review/verify_multicolumn.py、evidence/runs/weighted_congestion/multicolumn_review/exact_test_results.json。

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
- Evidence：research/current/weighted_congestion/source_envelope/sharp_asymptotic_envelope.md、review.md；Decimal验证仅诊断，未用来证明一般不等式。
- Counterevidence / Objections：未见fatal objection；极慢收敛不影响asymptotic，未认证后续文献全球优先权。源式sup本来已知，因此不称严格超过其基线。
- Status：完整一般证明与独立内部攻击；未外审。Truth有proof、Value给参数优化边界、Novelty未认证、Mechanism全局消元与局部化、Ambition为受限族。
- Related Files：assets/R3/sharp_source_review/、../current/weighted_congestion/README.md、根graph/review_status/assets。


## WC-R3-FULL-TOPOLOGY-REDUCTION v3 — INTERNAL PROOF

- Version history：v1 α≥2；v2 α≥φ、全部w>0；v3 α≥ρ=(1+√3)/2，右支单轻玩家允许w反演；每版范围明确，旧版为subcase。
- Exact Statement：对每个degree≤d对称同轻权两列F,G游戏和每个α≥ρ，若无α-PNE，则存在原式(3)域内monomial参数，其两test均strict通过同α。
- Objects / Domain / Quantifiers / Assumptions / Definitions / Scope：n≥1整数，w>0，F,G任意非负系数degree≤d同主/同副多项式；完整策略参proof；新游戏参数可改变。
- Conclusion：源包络F_d≤actual拓扑sup T_d≤max{ρ,F_d}；F_d≥ρ时T_d=F_d，所以该拓扑与源包络有同一sharp asymptotic。非a_*(d)上界。
- Dependencies：light稳定区间/反射、平移保持系数、右支n′α(α−1)<1和单轻反演、endpoint chord及系数线性消元。
- Evidence：research/current/weighted_congestion/source_topology/symmetric_two_column_reduction.md、verify.py/results.json；research/reviews/weighted_congestion/source_topology_review/review.md及独立literal checker。
- Counterevidence / Objections：初版φ仅w≤1的解释已由w≥1时z≥u机制补齐；v3不能坚持整个还原保持原w。F≡0直接存在PNE，zero分母未除。未见fatal objection。
- Status：完整一般证明及独立攻击；未外审、未认证novelty。Truth有proof、Value封闭整个受限搜索、Mechanism为整数稳定区间、Ambition不涉及异权/交叉拓扑。
- Related Files：assets/R3/full_topology/、assets/R3/topology_attack/、../current/weighted_congestion/README.md。


## WC-R3-SOURCE32-178-v1 — COMPLETE STATED SCOPE

- Exact Statement / Conclusion: For every original source parameter, min(H,L)<=89/50; all n,k and real w,beta are covered by analytic reduction plus exact negative interval certificates.
- Objects / Domain / Quantifiers / Assumptions / Definitions / Scope: exact identity in `research/current/weighted_congestion/source_degree32/symmetric_source_interval_certificate.md`; MODEL cost and weak equilibrium conventions apply. No claim of a full-class upper bound.
- Dependencies: WC-SOURCE-FORMULA; all joint premises remain explicit.
- Evidence: evidence/certificates/weighted_congestion/source_degree32/certificate.json, evidence/runs/weighted_congestion/source_degree32/verification.json, evidence/runs/weighted_congestion/crossover/main_check_results.json; separate independently authored verifier and direct reconstruction.
- Counterevidence / Objections: no remaining objection to the exact stated scope; fixed-degree improvement does not prove an unbounded family. External review and priority unverified.
- Status: complete exact statements with independent internal reconstruction; unrefereed. Truth: proved stated scope; Value: reusable separation/sign certificate/failure; Novelty: unassessed; Mechanism: explicit incidence and real-domain elimination; Ambition: WC-TARGET OPEN.
- Related Files: research/current/weighted_congestion/source_degree32/symmetric_source_interval_certificate.md, tests/audits/weighted_congestion/source_degree32/verify.py, tests/audits/weighted_congestion/crossover/main_check.py


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
- Objects / Domain / Quantifiers / Assumptions / Definitions / Scope: full exact identity in `research/current/weighted_congestion/density_padding/optional_user_density_padding.md`; arbitrary positive real weights where universally quantified, specified rational amplitudes for constructive families, MODEL weak cost inequalities.
- Dependencies: WC-MODEL and the direct proof in the linked account. No unproved migration between models.
- Evidence: authored general proof, independently reconstructed review `research/reviews/weighted_congestion/density_padding/review.md`, and actual exact code/records listed below. Finite sampling remains separate from proof.
- Counterevidence / Objections: selector failures do not prove nonexistence; occupied interval is not every geometric interval; retuned m1,m2 fail; cubic boundary is only for prescribed witnesses. No unresolved fatal objection within stated scope.
- Status: complete stated-scope proofs with independent internal reconstruction; unrefereed. Truth: stated scope proved; Value: reusable interface/obstruction/reduction; Novelty: unassessed; Mechanism: explicit linked derivation; Ambition: full WC-TARGET remains OPEN.
- Related Files: research/current/weighted_congestion/density_padding/optional_user_density_padding.md, research/reviews/weighted_congestion/density_padding/review.md, tests/audits/weighted_congestion/density_padding/verify.py, tests/audits/weighted_congestion/density_padding/independent_check.py, evidence/runs/weighted_congestion/density_padding/verification.json, evidence/runs/weighted_congestion/density_padding/independent_verification.json


## WC-R3-ODD-RING-CERTIFICATE-v1 — COMPLETE GENERAL PROOF / INTERNAL REVIEW

- Exact Statement / Conclusion: For odd m>=3, n_i>=1, positive u_i,v_i, 1<=k_i<=d and alpha>1, the specified two strict local tests have positive coefficients iff all N_i,Q_i>0 and product n_i N_i Q_i/(M_i P_i)>1. They exclude alpha-PNE at every state.
- Objects / Domain / Quantifiers / Assumptions / Definitions: full exact identity in `research/current/weighted_congestion/odd_ring/cohort_lower_bound_and_envelope.md`, sections 1–6; costs and weak alpha-PNE use MODEL.md. Positive rational construction is a subclass of arbitrary positive-real-weight G_d.
- Scope: Fixed exact positive local-test system; iff is coefficient feasibility, not all possible ring nonexistence.
- Dependencies: WC-MODEL; explicit elementary proofs, no imported nonexistence theorem.
- Evidence: complete general proof, independent reconstruction before reading the initial route, two envelope attacks, Fraction full-state small game and separate exact growing-certificate checks.
- Counterevidence / Objections: no unresolved fatal objection in the stated scope; finite tests do not prove generality. Later-literature search is not exhaustive; global priority unverified.
- Status: canonical stated-scope internal mathematical result, unrefereed. Truth: proved scope; Value: growing lower/usable mechanism boundary; Novelty: unverified; Mechanism: odd parity and weight-cycle amplification; Ambition: lower stage breakthrough, WC-TARGET OPEN.
- Related Files: `research/current/weighted_congestion/odd_ring_linear.md`, `research/current/weighted_congestion/odd_ring/cohort_lower_bound_and_envelope.md`, `tests/audits/weighted_congestion/odd_ring/verify.py`, `evidence/runs/weighted_congestion/odd_ring/verification.json`, `research/reviews/weighted_congestion/odd_ring_independent/REVIEW.md`, `research/reviews/weighted_congestion/odd_ring_independent/EXACT_ENVELOPE_REVIEW.md`, `research/reviews/weighted_congestion/odd_ring_parameters/exact_envelope_review.md`, `research/reviews/weighted_congestion/odd_ring_literature/notes.md`.


## WC-R3-ODD-RING-ENVELOPE-v1 — COMPLETE GENERAL PROOF / INTERNAL REVIEW

- Exact Statement / Conclusion: For each d>=2 and alpha>1, some finite odd ring satisfies the positive monomial local-test system iff alpha<T_d=sup_R>1 [R(1+R)^d+1]/[(1+R)^d+R^(d+1)]. H_d<T_d<=H_d+1/(2^d+1), H_d=d/[(d+1)d^(1/(d+1))-d], hence T_d~d/ln d.
- Objects / Domain / Quantifiers / Assumptions / Definitions: full exact identity in `research/current/weighted_congestion/odd_ring/cohort_lower_bound_and_envelope.md`, sections 1–6; costs and weak alpha-PNE use MODEL.md. Positive rational construction is a subclass of arbitrary positive-real-weight G_d.
- Scope: Certificate envelope only; failure does not imply an equilibrium. Strict endpoint alpha=T_d is infeasible for these tests.
- Dependencies: WC-MODEL, WC-R3-ODD-RING-CERTIFICATE-v1; explicit elementary proofs, no imported nonexistence theorem.
- Evidence: complete general proof, independent reconstruction before reading the initial route, two envelope attacks, Fraction full-state small game and separate exact growing-certificate checks.
- Counterevidence / Objections: no unresolved fatal objection in the stated scope; finite tests do not prove generality. Later-literature search is not exhaustive; global priority unverified.
- Status: canonical stated-scope internal mathematical result, unrefereed. Truth: proved scope; Value: growing lower/usable mechanism boundary; Novelty: unverified; Mechanism: odd parity and weight-cycle amplification; Ambition: lower stage breakthrough, WC-TARGET OPEN.
- Related Files: `research/current/weighted_congestion/odd_ring_linear.md`, `research/current/weighted_congestion/odd_ring/cohort_lower_bound_and_envelope.md`, `tests/audits/weighted_congestion/odd_ring/verify.py`, `evidence/runs/weighted_congestion/odd_ring/verification.json`, `research/reviews/weighted_congestion/odd_ring_independent/REVIEW.md`, `research/reviews/weighted_congestion/odd_ring_independent/EXACT_ENVELOPE_REVIEW.md`, `research/reviews/weighted_congestion/odd_ring_parameters/exact_envelope_review.md`, `research/reviews/weighted_congestion/odd_ring_literature/notes.md`.


## WC-R3-ODD-RING-LOWER-v1 — COMPLETE GENERAL PROOF / INTERNAL REVIEW

- Exact Statement / Conclusion: For every integer d>=2 and real 1<=alpha<T_d, a finite rational-weight/coefficient congestion game, all resource latencies positive monomials of degree exactly d, has no alpha-PNE. Therefore a_*(d)>=T_d~d/ln d and liminf a_*(d)ln(d)/d>=1.
- Objects / Domain / Quantifiers / Assumptions / Definitions: full exact identity in `research/current/weighted_congestion/odd_ring/cohort_lower_bound_and_envelope.md`, sections 1–6; costs and weak alpha-PNE use MODEL.md. Positive rational construction is a subclass of arbitrary positive-real-weight G_d.
- Scope: Game may depend on alpha; unbounded player count/support and huge input size allowed. No endpoint game, polynomial-time construction, full-class upper, matched growth, or global priority claim.
- Dependencies: WC-MODEL, WC-R3-ODD-RING-CERTIFICATE-v1, WC-R3-ODD-RING-ENVELOPE-v1; explicit elementary proofs, no imported nonexistence theorem.
- Evidence: complete general proof, independent reconstruction before reading the initial route, two envelope attacks, Fraction full-state small game and separate exact growing-certificate checks.
- Counterevidence / Objections: no unresolved fatal objection in the stated scope; finite tests do not prove generality. Later-literature search is not exhaustive; global priority unverified.
- Status: canonical stated-scope internal mathematical result, unrefereed. Truth: proved scope; Value: growing lower/usable mechanism boundary; Novelty: unverified; Mechanism: odd parity and weight-cycle amplification; Ambition: lower stage breakthrough, WC-TARGET OPEN.
- Related Files: `research/current/weighted_congestion/odd_ring_linear.md`, `research/current/weighted_congestion/odd_ring/cohort_lower_bound_and_envelope.md`, `tests/audits/weighted_congestion/odd_ring/verify.py`, `evidence/runs/weighted_congestion/odd_ring/verification.json`, `research/reviews/weighted_congestion/odd_ring_independent/REVIEW.md`, `research/reviews/weighted_congestion/odd_ring_independent/EXACT_ENVELOPE_REVIEW.md`, `research/reviews/weighted_congestion/odd_ring_parameters/exact_envelope_review.md`, `research/reviews/weighted_congestion/odd_ring_literature/notes.md`.


## WC-R3-ODD-RING-POLYNOMIAL-ENVELOPE-v1 — COMPLETE STATED-SCOPE PROOF

- Exact Statement / Conclusion: For d>=2 and alpha>1, allowing each odd-ring group independent nonnegative degree-at-most-d shapes F_i,G_i, common across its action copies/cohort, does not change positive two-local-test feasibility: some finite certificate exists iff alpha<T_d. Constants in mixtures and arbitrary positive real weights are covered; zero shapes cannot satisfy the strict tests.
- Objects / Domain / Quantifiers / Assumptions / Definitions: PROOF.md section8, d>=2, alpha>1, finite odd ring, n_i>=1, nonnegative shapes degree<=d, resource-independent positive weights, shared action/cohort shapes and positive group amplitudes. Feasibility is existential over shapes/parameters.
- Scope: This is a certificate ceiling, not full-class or actual-topology equilibrium existence. Action-specific and clone-specific shape asymmetries are excluded. Sufficiency existential over chosen shapes, not for every prescribed shape.
- Dependencies: WC-R3-ODD-RING-CERTIFICATE-v1 and ENVELOPE-v1, plus exact denominator-weighted convex identities, including degree0 negative factors.
- Evidence: general proof independently attacked; actual Fraction mixed-degree checks with constants, zero-shape exclusions and signed individual differences.
- Counterevidence / Objections: no unresolved fatal within scope; infeasibility does not supply a pure stable profile. General partially aligned cohort and reverse light deviations remain an actual-topology gap.
- Status: stated-scope internally proved, unrefereed. Truth: proved; Value: closes mixed-shape tuning; Novelty: unassessed; Mechanism: convexity with positive denominators; Ambition: boundary, WC-TARGET OPEN.
- Related Files: research/current/weighted_congestion/odd_ring/cohort_lower_bound_and_envelope.md section8; research/reviews/weighted_congestion/odd_ring_parameters/polynomial_envelope_review.md; check_polynomial_envelope.py; polynomial_envelope_verification.json.


## WC-R3-ODD-RING-SINGLETON-UPPER-v1 — COMPLETE RESTRICTED EXISTENCE PROOF

- Exact Statement / Conclusion: Every odd m>=3 ring with n_i=1 at every group, arbitrary positive real weights, symmetric action copies and nonnegative polynomial fees of degree at most d>=2 (zero fees permitted), has a min{2,T_d}-PNE. A T_d-PNE exists among the 2m single-conflict profiles modulo global action exchange.
- Objects / Domain / Quantifiers / Assumptions / Definitions: every finite odd m>=3, all n_i=1, positive real u_i,v_i, same group fee shape on both action copies, nonnegative degree<=d, d>=2; zero resources allowed. Uses MODEL's weak alpha-PNE, exact pure costs.
- Scope: Restricted actual-topology existence, not sharpness and not a general-cohort or full-model upper. The smaller factor-2 equilibrium is not claimed to be single-conflict when 2<T_d.
- Dependencies: WC-R3-ODD-RING-POLYNOMIAL-ENVELOPE-v1; exact defect-state cycle, correct reversed ring/role map, direct total-cost support-two inequality in PROOF.md section9.
- Evidence: internal independent defect-graph derivation, root reconstruction and exact small graph checks including zero fees and reverse resource/player map. Finite code uses safe alpha=d; endpoint T_d is established by the general proof.
- Counterevidence / Objections: more than one light per group destroys the simple defect-cycle representation; cannot promote this to arbitrary cohorts. No unresolved fatal within stated scope.
- Status: internally proved, unrefereed. Truth: stated subclass proved; Value: actual-topology boundary and representation; Novelty: unverified; Mechanism: arc counting/reversed roles/support; Ambition: structural subcase, WC-TARGET OPEN.
- Related Files: research/current/weighted_congestion/odd_ring/cohort_lower_bound_and_envelope.md section9; research/reviews/weighted_congestion/odd_ring_parameters/SINGLETON_NOTE.md; check_singleton_graph.py; singleton_graph_verification.json.

## WC-R1-MULTIPLIER-BARRIER v1 — INTERNALLY REVIEWED METHOD OBSTRUCTION

- 中文数学名称：任意玩家乘子的有限多尺度边际夹逼障碍。
- Exact Statement / Objects / Domain / Quantifiers / Assumptions / Definitions / Scope / Conclusion：完整身份与证明固定于[现行重构](../current/weighted_congestion/separable_ordinal_obstruction.md)“精确身份”；d≥2、1≤α<ρ_d，任意正实权，有限见证。第一项允许F,h依完整权向量；第二项允许F_e依完整游戏但要求每条严格α改善边下降，游戏所有费用x^d、策略族2^E。两项不能互换，也不能升级为无均衡。
- Dependencies：第一项为MODEL、等权类双重平均、同端点路径、有限黎曼和分离；第二项共同依赖MODEL、第一项、先固定有限资源数和同一游戏自同构平均。
- Evidence：冻结ec827a9原证明的独立先重构后攻击，父研究者逐式核查及新现行自足重构；Fraction有限核验另列。
- Counterevidence / Objections：全空精确均衡始终存在；非可分势、只选部分改善、依游戏选极小点目标不在排除范围；ρ_d端点不排除。未见所述范围内fatal objection。
- Status：complete stated-scope proof with independent reconstruction and exact finite audit; unrefereed。Truth=所述范围内部证明；Value=方法边界与量词修补；Novelty=未认证；Mechanism=有限多尺度与资源束；Ambition=不改变WC-TARGET OPEN。
- Related Files：[独立审查](../reviews/weighted_congestion/ordinal_potentials/game_specific_independent_attack.md)、[核验代码](../../tests/audits/weighted_congestion/ordinal_potentials/verify_finite_bundle_bridge.py)、[冻结结果](../../evidence/runs/weighted_congestion/ordinal_potentials/finite_bundle_independent_checks.json)。

## WC-R1-GAME-SPECIFIC-SEPARABLE-ORDINAL-BARRIER v1 — INTERNALLY REVIEWED METHOD OBSTRUCTION

- 中文数学名称：依完整游戏选择的资源可分严格序势障碍。
- Exact Statement / Objects / Domain / Quantifiers / Assumptions / Definitions / Scope / Conclusion：完整身份与证明固定于[现行重构](../current/weighted_congestion/separable_ordinal_obstruction.md)“精确身份”；d≥2、1≤α<ρ_d，任意正实权，有限见证。第一项允许F,h依完整权向量；第二项允许F_e依完整游戏但要求每条严格α改善边下降，游戏所有费用x^d、策略族2^E。两项不能互换，也不能升级为无均衡。
- Dependencies：第一项为MODEL、等权类双重平均、同端点路径、有限黎曼和分离；第二项共同依赖MODEL、第一项、先固定有限资源数和同一游戏自同构平均。
- Evidence：冻结ec827a9原证明的独立先重构后攻击，父研究者逐式核查及新现行自足重构；Fraction有限核验另列。
- Counterevidence / Objections：全空精确均衡始终存在；非可分势、只选部分改善、依游戏选极小点目标不在排除范围；ρ_d端点不排除。未见所述范围内fatal objection。
- Status：complete stated-scope proof with independent reconstruction and exact finite audit; unrefereed。Truth=所述范围内部证明；Value=方法边界与量词修补；Novelty=未认证；Mechanism=有限多尺度与资源束；Ambition=不改变WC-TARGET OPEN。
- Related Files：[独立审查](../reviews/weighted_congestion/ordinal_potentials/game_specific_independent_attack.md)、[核验代码](../../tests/audits/weighted_congestion/ordinal_potentials/verify_finite_bundle_bridge.py)、[冻结结果](../../evidence/runs/weighted_congestion/ordinal_potentials/finite_bundle_independent_checks.json)。

## WC-ACTION-SIGNATURE-COMPRESSION-v1 — INTERNALLY RECONSTRUCTED

- 中文数学名称：有限动作的资源签名压缩。
- Exact Statement / Objects / Domain / Quantifiers / Assumptions / Definitions / Scope / Conclusion：对每个固定有限正实权向量、正动作数m_i、次数d≥0，所有资源数的MODEL游戏在全部状态及真实偏离成本上等价于2^(Σm_i)−1个非空动作签名资源，单项式系数非负。保留零费用资源区分动作，不要求逐字保留空策略。
- Dependencies：MODEL与系数线性合并。Evidence：完整恒等式证明、独立先重构后攻击、Fraction复验。Counterevidence / Objections：不控制动作总数和无限模板族的统一倍率。
- Status：完整一般证明及内部独立审查，未外审；Truth为表示定理，Value为消去任意资源数，Novelty未评估，Mechanism为关联签名，Ambition为工具。
- Related Files：research/current/weighted_congestion/template_certificates/finite_action_duality.md；research/reviews/weighted_congestion/template_certificates/finite_action_duality_review.md；tests/audits/weighted_congestion/template_certificates/verify_template_certificates.py；evidence/runs/weighted_congestion/template_certificates/exact_audit.json。

## WC-ALLSTATE-SELECTOR-ALTERNATIVE-v1 — INTERNALLY RECONSTRUCTED

- 中文数学名称：全状态择证的精确线性替代。
- Exact Statement / Objects / Domain / Quantifiers / Assumptions / Definitions / Scope / Conclusion：对上述每个固定模板、每个实α≥1、每个逐状态合法偏离selector h，恰有a≥0,B_h a>0或λ≥0,Σλ=1,B_hᵀλ≤0之一成立。固定权重及动作数的所有游戏都有α-PNE，当且仅当每个h均有后一证书。权与α有理时可取有理证书；λ可依完整h。
- Dependencies：WC-ACTION-SIGNATURE-COMPRESSION-v1、有限行凸包/闭负象限替代、自足有理仿射面论证。Evidence：一般证明、独立攻击和两份不同有理核验。Counterevidence / Objections：单个h的dual或单个环不等于全类保证；没有统一C,d0。
- Status：完整一般证明及内部独立审查，未外审；Truth为精确替代，Value为全状态搜索与存在证书接口，Novelty未评估，Mechanism为线性锥替代，Ambition保持工具。
- Related Files：research/current/weighted_congestion/template_certificates/finite_action_duality.md；research/reviews/weighted_congestion/template_certificates/finite_action_duality_review.md；tests/audits/weighted_congestion/template_certificates/independent_two_column_alternative.py；evidence/runs/weighted_congestion/template_certificates/independent_two_column_alternative.json。

## WC-GAME-SPECIFIC-MINIMIZER-EQUIVALENCE-v1 — SCOPE LEMMA

- 中文数学名称：依游戏最小点选择与近似纯均衡存在等价。
- Exact Statement / Objects / Domain / Quantifiers / Assumptions / Definitions / Scope / Conclusion：对每个有限MODEL游戏G、每个实α≥1，G有α-PNE当且仅当存在可依整个游戏任意选择的资源集函数F_e，使Σ_eF_e(S_e(s))的每个全局最小点都是α-PNE。对任意指定合法s*，F_e(U)=|U△S_e(s*)|唯一选s*。
- Dependencies：有限性和入射双重计数。Evidence：直接一般证明，子研究者独立提出、主研究者复核，有限目标状态对核验。Counterevidence / Objections：以s*为输入不提供找均衡方法，不能循环推出新倍率；不要求对全部改善下降。旧序势障碍身份不变。
- Status：完整直接证明及内部核对，未外审；Truth为等价，Value为量词边界，Novelty未评估，Mechanism为入射距离，Ambition不是存在界。
- Related Files：research/current/weighted_congestion/separable_ordinal_obstruction.md第四节；research/reviews/weighted_congestion/ordinal_potentials/minimizer_scope_review.md；tests/audits/weighted_congestion/template_certificates/verify_template_certificates.py；evidence/runs/weighted_congestion/template_certificates/exact_audit.json。


## WC-HIGH-DEGREE-SHARE-v1 — 高次费用与资源最小个体份额

- Exact Statement / Conclusion：每个MODEL有限游戏，费用c_e=a_e0+Σ_(j≥k_e)a_ej x^j，按实际非零最低正次数k_e定义λ_e=1−(1−min_(i∈U_e)w_i/Σ_(j∈U_e)w_j)^k_e；无用户或无正次项取λ_e=1。势Σ_e[a_e0 n_e+Σ_(j≥1)a_ej x_e^j]的每个单方局部最小点是(max_e λ_e^−1)-PNE。纯d次无α-PNE必有某正次收费资源潜在用户份额严格小于1−(1−1/α)^(1/d)。固定正权向量的最低正次数趋无穷时，保证对所有有限拓扑及系数一致趋1。
- Objects / Domain / Quantifiers / Assumptions / Definitions：任意有限非空玩家/资源、正实权、任意非空有限资源子集策略族（含空策略）、非负系数。q_e只在非空潜在用户上取；λ_e取法、势和每次真实偏离详见正文。所有近似不等式取弱边界，无0/0。
- Scope：实例相关结构存在界；最低正次数不能换成最高次数，全类q无统一下界。固定人数但权随次数变化不在一致极限范围。
- Dependencies：MODEL、真实负载、有限状态最小化、非负整数幂差；不导入外部存在定理。
- Evidence：完整直接证明；先独立重构后读冻结正文攻击，绑定正文SHA256 f01084498e843db3e8491014debe02cb421b2091aeb4d12344e7d0175e14cabd；两套Fraction有限审计。
- Counterevidence / Objections：无尚成立fatal；潜在份额只是充分界的实例参数，optional padding可使其失去判别力；必要小份额不是坏状态或改善者证书。低次混合/不同玩家乘子不能直接拼接。
- Status：complete structural proof; internally reviewed; unrefereed。Truth：所述结构类已内部证明；Value：必要小份额与一致高次极限；Novelty：未认证；Mechanism：删去幂差及常数人数势；Ambition：全类目标仍OPEN。
- Related Files：research/current/weighted_congestion/high_degree_share.md；research/reviews/weighted_congestion/high_degree_share_review.md；tests/audits/weighted_congestion/high_degree_share/verify.py; tests/audits/weighted_congestion/high_degree_share/check_independent.py; evidence/runs/weighted_congestion/high_degree_share/verification.json; evidence/runs/weighted_congestion/high_degree_share/independent_verification.json。

## 严格反例规范形与普遍阈值端点

### WC-INTEGER-MONOMIAL-COUNTEREXAMPLE-v1 — 严格反例的整数单位单项式规范形

- Exact Statement / Objects / Domain / Quantifiers：每个整数d≥0、每个实α≥1，全MODEL有无α-PNE反例，当且仅当正整数权、每资源费用x^k（0≤k≤d）、每策略非空的有限反例存在；玩家数可保持，不保策略/资源数。
- Assumptions / Definitions / Scope / Conclusion：严格全状态改善、真实负载；允许起始零费/空策略/异构策略族。逐倍率反例存在归约，不声称保持原实例β或给统一规模界。
- Dependencies：有限严格余量与连续性、有理稠密、清分母、资源复制和动作取商；无需外部均衡定理。
- Evidence：完整自足证明、先重构后冻结攻击、Fraction实际复制资源oracle；配套见下。
- Counterevidence / Objections：α为无理时只断言存在归约；固定有理α的枚举只半判定反例，未输出没有真值含义。
- Status：complete direct proof; independently reconstructed and exactly audited; unrefereed。Truth为规范形等价；Value为可枚举反例域；Novelty未认证；Mechanism为strict margin；Ambition不含全类上界。
- Related Files：[正文](../current/weighted_congestion/template_certificates/integer_counterexample_normal_form.md)、[独立攻击](../reviews/weighted_congestion/template_certificates/integer_counterexample_normal_form_review.md)、`tests/audits/weighted_congestion/template_certificates/verify_integer_normal_form.py`、`evidence/runs/weighted_congestion/template_certificates/integer_normal_form_audit.json`。

### WC-UNIVERSAL-THRESHOLD-ENDPOINT-v1 — 普遍阈值的端点闭性

- Exact Statement / Objects / Domain / Quantifiers：每个d≥0，单实例可行集为非空闭射线[β(G),∞)，β有限且由纯状态取得；有理游戏β有理。全类可行集是[a_*(d),∞)，a_*=sup_G β(G)，也等于整数单位单项式且非空策略子类的sup。
- Assumptions / Definitions / Scope / Conclusion：MODEL原对象和inf定义不变；零成本直接分类。全类端点在每游戏分别可行，不意味着有某游戏取得sup或a_*有理/可计算。
- Dependencies：有限状态闭射线、正文自足(d+1)粗存在界、WC-INTEGER-MONOMIAL-COUNTEREXAMPLE-v1（规范子类sup等式）。
- Evidence：完整证明及独立冻结攻击；有限审计只检查编码与端点语义。
- Counterevidence / Objections：端点闭性没有缩小当前d/log d与d的缺口；没有全类参数紧致性假设。
- Status：complete direct proof; independently reconstructed and exactly audited; unrefereed。Truth为端点；Value为精确全类量词接口；Novelty未认证；Mechanism为闭射线交；Ambition仍OPEN。
- Related Files：同前项。

## WC-ORDERED-COHORT-FREEZING-v1 — 有序权组的尾部负载冻结存在界

- Exact Statement / Conclusion：任意MODEL游戏、d≥0和玩家有序非空划分，资源组潜在用户最小/最大权a,b与后组潜在总权L定义A=max_(e,j)(b/a)(1+L/a)^d（无潜在用户取1）。依次固定先组背景，最小化按(1+L/a)^d/a缩放的活动组Shapley势并冻结，任取阶段全局最小均得到A-PNE。若组内比≤R且L≤εa，给R(1+ε)^d；不控制全类最佳划分参数。
- Objects / Domain / Quantifiers / Assumptions / Definitions / Scope：完整采用[正文](../current/weighted_congestion/weight_bands/ordered_tail_freezing.md)的精确身份；每个实权、每个合法偏离按真实负载。对象限制不得省略；主目标保持OPEN。
- Dependencies：WC-MODEL, WC-R3-DENSE-SHARE-v1, WC-ORDERED-TAIL-PARAMETERS；有限最小化、单项式比较或DAG拓扑递推；正文逐项给出，无外部存在定理导入。
- Evidence：一般证明；先依据精确命题独立重构，后读冻结hash逐项攻击；Fraction独立实现与实际运行分开记录。
- Counterevidence / Objections：只证此实例参数界，无全类Cd/ln d；不要求同一势对全部改善边下降。未处理的全类义务不升级；外审/优先权未认证。
- Status：complete stated-scope proof; independently reconstructed and exactly audited; unrefereed。Truth按所写范围；Value为接口及准确边界；Novelty未认证；Mechanism见正文；Ambition不是全类完成。
- Related Files：[正文](../current/weighted_congestion/weight_bands/ordered_tail_freezing.md)、[审查](../reviews/weighted_congestion/weight_bands/ordered_tail_freezing_review.md)；规范代码和冻结结果见正文审计合同及assets.json。

## WC-ORDERED-TAIL-PARAMETER-LIMIT-v1 — 两权级有序尾部参数的精确最优值

- Exact Statement / Conclusion：任意d≥1,H≥1,K≥1，单资源一名权H玩家及K名单位权玩家、费用x^d、人人可选空策略或该资源。全部有序非空划分的最小A恰为min{H,(1+K/H)^d}。K=ceil(H²)时恰H，固定d仍可无界；游戏有全空精确PNE。
- Objects / Domain / Quantifiers / Assumptions / Definitions / Scope：完整采用[正文](../current/weighted_congestion/weight_bands/ordered_tail_freezing.md)的精确身份；每个实权、每个合法偏离按真实负载。对象限制不得省略；主目标保持OPEN。
- Dependencies：WC-MODEL, WC-ORDERED-TAIL-PARAMETERS；有限最小化、单项式比较或DAG拓扑递推；正文逐项给出，无外部存在定理导入。
- Evidence：一般证明；先依据精确命题独立重构，后读冻结hash逐项攻击；Fraction独立实现与实际运行分开记录。
- Counterevidence / Objections：只否定对该潜在尾部A参数的统一控制，不否定冻结程序可能有更精细分析，也不是均衡非存在。未处理的全类义务不升级；外审/优先权未认证。
- Status：complete stated-scope proof; independently reconstructed and exactly audited; unrefereed。Truth按所写范围；Value为接口及准确边界；Novelty未认证；Mechanism见正文；Ambition不是全类完成。
- Related Files：[正文](../current/weighted_congestion/weight_bands/ordered_tail_freezing.md)、[审查](../reviews/weighted_congestion/weight_bands/ordered_tail_freezing_review.md)；规范代码和冻结结果见正文审计合同及assets.json。

## WC-DAG-LOW-LEAKAGE-DEGREE-BUDGET-v1 — 有向无环阶跃端点的低泄漏次数预算

- Exact Statement / Conclusion：任意非空有限simple DAG、d≥1及ε∈(0,1)，令z=ε^(-1/d),P_k为k顶点有向路径数,S_D(z)=ΣP_kz^(k−1)。存在根权1、正轻权W<1及outsum<w_v、非零非负degree≤d费用通过p0(W)≤εp0(1)和pv(1+outsum)≤εpv(1+w_v)，当且仅当z(z−1)S_D(z)≤1。全部可行权有正文slack表示；饱和时权唯一。原辅助step阈值q满足q(q−1)≤1/[z(z−1)]≤d/ln(1/ε)，固定ε的√d量级在检测系统内可达。
- Objects / Domain / Quantifiers / Assumptions / Definitions / Scope：完整采用[正文](../current/weighted_congestion/polynomial_curvature/dag_low_leakage_budget.md)的精确身份；每个实权、每个合法偏离按真实负载。对象限制不得省略；主目标保持OPEN。
- Dependencies：WC-MODEL, WC-DAG-ENDPOINT-TESTS, WC-R1-DAG-STEP；有限最小化、单项式比较或DAG拓扑递推；正文逐项给出，无外部存在定理导入。
- Evidence：一般证明；先依据精确命题独立重构，后读冻结hash逐项攻击；Fraction独立实现与实际运行分开记录。
- Counterevidence / Objections：iff仅是指定端点检测系统；未控制高平台过冲或真实全状态偏离，不给实际多项式博弈的β上界。未处理的全类义务不升级；外审/优先权未认证。
- Status：complete stated-scope proof; independently reconstructed and exactly audited; unrefereed。Truth按所写范围；Value为接口及准确边界；Novelty未认证；Mechanism见正文；Ambition不是全类完成。
- Related Files：[正文](../current/weighted_congestion/polynomial_curvature/dag_low_leakage_budget.md)、[审查](../reviews/weighted_congestion/polynomial_curvature/dag_low_leakage_budget_review.md)；规范代码和冻结结果见正文审计合同及assets.json。


## WC-TWO-WEIGHT-ORDER-BLEND-v1 — 两权类别双排序混合势

- Exact Statement / Objects / Domain / Quantifiers：对每个d≥2及MODEL有限游戏，若所有玩家权重属于固定{a,b}、a≥b>0，则双排序混合势的每个单方局部最小点为A_d=(1+√(4d−3))/2-PNE，任意严格A_d改善终止；各类人数、权比、拓扑和系数任意。d≤1或仅一权时有精确PNE。不是任意权重全类上界。
- Assumptions / Definitions / Scope：固定全局两权值而非逐资源任意选两权，任意有限非空玩家/资源、正实权、任意有限非空资源子集策略族、非负degree≤d多项式；允许空策略、常数和零费用。D,U为相反排序加权离散积分，λ解(d−1)λ²=1+λ。
- Conclusion：共享玩家乘子h重=λa、h轻=(1+λ)b，所有局部势最小点满足弱A_d-PNE；没有计算时间或全类匹配声明。
- Dependencies：MODEL、凸排序交换、逐项导数界、有限势最小化；不导入外部存在定理。
- Evidence：完整一般证明，先从exact statement独立重构后攻击冻结hash；两份不互相导入的Fraction核验。
- Counterevidence / Objections：已修正a=b时按固定类别选乘子和严格A_d改善措辞；未见所述范围内fatal。三类没有同样互补精确边际，全类任意多权仍OPEN。
- Status：complete structural proof; independently reconstructed and exactly audited; unrefereed。Truth=子类完整内部证明；Value=任意权比/人数的两权桥；Novelty=未认证；Mechanism=双排序互补边际；Ambition=结构子类。
- Related Files：research/current/weighted_congestion/weight_bands/two_weight_order_blend.md；research/reviews/weighted_congestion/weight_types/two_weight_order_blend_review.md；tests/audits/weighted_congestion/weight_types/verify_order_blend.py；tests/audits/weighted_congestion/weight_types/independent_order_blend.py；evidence/runs/weighted_congestion/weight_types/order_blend.json；evidence/runs/weighted_congestion/weight_types/independent_order_blend.json。

### WC-SELECTOR-UNIT-SPEED-STATIONARY-BARRIER-v1 — 单位速度平稳择证的无界损失

- Exact Statement / Objects / Domain / Quantifiers / Assumptions / Definitions / Scope / Conclusion：For every finite real alpha>=1 and d>=1, some finite positive rational weight two-action template and full selector have no unit-speed stationary dual, already witnessed by an affine column; this is no nonexistence result. 完整中文逐项身份及符号见[自足正文](../current/weighted_congestion/template_certificates/stationary_selector_obstruction.md)；该链接是精确陈述来源，不以本段英文压缩替代量词。
- Dependencies：MODEL及正文所列完整前提；择证支撑等价另用全状态线性替代，分叉割另用精确拓扑和弱UF。
- Evidence：[独立先重构后冻结攻击](../reviews/weighted_congestion/template_certificates/stationary_selector_obstruction_review.md)及正文末节的精确代码和冻结证据；有限核验不是一般证明。
- Counterevidence / Objections：只能使用正文写明的限制；单位速度障碍不否定持留率，仿射dual不外推高次，recurrent支撑不是一般dual要求，UF不能从真实非存在自动推出。
- Status：complete stated-scope proof; independently reconstructed and exactly audited; unrefereed。Truth为所述精确Claim；Value为机制或边界；Novelty未认证；Ambition不完成唯一全类命题。
- Related Files：上述正文、审查及从正文审计合同连接的code/run。

### WC-AFFINE-SELECTOR-CYCLE-DUAL-v1 — 任意仿射择证的循环权重对偶

- Exact Statement / Objects / Domain / Quantifiers / Assumptions / Definitions / Scope / Conclusion：For every finite positive-weight action template and tagged selector, every selected cycle gives an affine dual by lambda_s proportional to the selected mover weight; self-loops are allowed and all affine columns sum to zero at alpha=1. 完整中文逐项身份及符号见[自足正文](../current/weighted_congestion/template_certificates/stationary_selector_obstruction.md)；该链接是精确陈述来源，不以本段英文压缩替代量词。
- Dependencies：MODEL及正文所列完整前提；择证支撑等价另用全状态线性替代，分叉割另用精确拓扑和弱UF。
- Evidence：[独立先重构后冻结攻击](../reviews/weighted_congestion/template_certificates/stationary_selector_obstruction_review.md)及正文末节的精确代码和冻结证据；有限核验不是一般证明。
- Counterevidence / Objections：只能使用正文写明的限制；单位速度障碍不否定持留率，仿射dual不外推高次，recurrent支撑不是一般dual要求，UF不能从真实非存在自动推出。
- Status：complete stated-scope proof; independently reconstructed and exactly audited; unrefereed。Truth为所述精确Claim；Value为机制或边界；Novelty未认证；Ambition不完成唯一全类命题。
- Related Files：上述正文、审查及从正文审计合同连接的code/run。

### WC-RECURRENT-SUPPORT-FIP-EQUIVALENCE-v1 — 循环支撑择证与全模板有限改善性等价

- Exact Statement / Objects / Domain / Quantifiers / Assumptions / Definitions / Scope / Conclusion：For fixed finite weights, action counts, degree, real alpha>=1 and any fixed nonempty signature-column subcone, every selector admits a dual supported on its recurrent states iff every nonnegative-coefficient game on that template has no strict alpha-improvement cycle; this is stronger than mere PNE existence. 完整中文逐项身份及符号见[自足正文](../current/weighted_congestion/template_certificates/stationary_selector_obstruction.md)；该链接是精确陈述来源，不以本段英文压缩替代量词。
- Dependencies：MODEL及正文所列完整前提；择证支撑等价另用全状态线性替代，分叉割另用精确拓扑和弱UF。
- Evidence：[独立先重构后冻结攻击](../reviews/weighted_congestion/template_certificates/stationary_selector_obstruction_review.md)及正文末节的精确代码和冻结证据；有限核验不是一般证明。
- Counterevidence / Objections：只能使用正文写明的限制；单位速度障碍不否定持留率，仿射dual不外推高次，recurrent支撑不是一般dual要求，UF不能从真实非存在自动推出。
- Status：complete stated-scope proof; independently reconstructed and exactly audited; unrefereed。Truth为所述精确Claim；Value为机制或边界；Novelty未认证；Ambition不完成唯一全类命题。
- Related Files：上述正文、审查及从正文审计合同连接的code/run。

### WC-DIRECTED-FANOUT-FORCING-CUT-v1 — 分叉双人侧反馈的统一强迫割均衡

- Exact Statement / Objects / Domain / Quantifiers / Assumptions / Definitions / Scope / Conclusion：For d>=2 and alpha>=T_d, every finite unique-source light/multihead-private-pair-side topology satisfying the weak uniform aligned-light forcing inequalities admits an all-anti alpha-PNE selected by any local minimum of the stated weighted cut; no unrestricted existence claim. 完整中文逐项身份及符号见[自足正文](../current/weighted_congestion/directed_fanout_forcing_cut.md)；该链接是精确陈述来源，不以本段英文压缩替代量词。
- Dependencies：MODEL及正文所列完整前提；择证支撑等价另用全状态线性替代，分叉割另用精确拓扑和弱UF。
- Evidence：[独立先重构后冻结攻击](../reviews/weighted_congestion/directed_fanout_forcing_cut_review.md)及正文末节的精确代码和冻结证据；有限核验不是一般证明。
- Counterevidence / Objections：只能使用正文写明的限制；单位速度障碍不否定持留率，仿射dual不外推高次，recurrent支撑不是一般dual要求，UF不能从真实非存在自动推出。
- Status：complete stated-scope proof; independently reconstructed and exactly audited; unrefereed。Truth为所述精确Claim；Value为机制或边界；Novelty未认证；Ambition不完成唯一全类命题。
- Related Files：上述正文、审查及从正文审计合同连接的code/run。

## WC-DAG-EXTREMAL-AMPLITUDE-ALL-IN-v1 — 阶跃DAG极值幅度的多项式全入状态

- Exact Statement / Conclusion：任意非空有限simple DAG，root权1、正轻权W<1且outsum<w_v、原双列binary策略；两列相同非零非负degree≤d费用，d≥1。令q=q_D>1、h_v=(1+Σ_in h_u)/q且Σh=q−1，存在A>0使p0(1)=A、pv(1+w_v)=A h_v。真实全入状态是max{1+1/q,B_d(q)}-PNE，B_d(q)=q/[1+(q−1)(1+1/[q(q−1)])^(−d)]；d≥16时统一为4√(d/ln d)-PNE。不要求低漏/高平台保真，但必须保留极值幅度条件。
- Objects / Domain / Quantifiers / Assumptions / Definitions / Scope：对每个上述有限DAG、合法正实权和实系数；准确资源、策略与幅度(N)见[正文](../current/weighted_congestion/step_dag/polynomial_extremal_all_in.md)第1节。费用正归一化，不将任意MODEL的零费用/空策略偷换进子类。
- Dependencies：MODEL、WC-R1-DAG-STEP的q/h及路径展开、真实负载、单项式次数界、总权缺口矩、Jensen。与端点低泄漏预算无逻辑依赖。
- Evidence：一般直接证明；先仅由exact statement独立重构，再逐式攻击冻结hash；两份不互相导入的Fraction实际资源审计。
- Counterevidence / Objections：仅限所写DAG策略及极值幅度；任意幅度/全类策略尚无归约，不是本题一般肯定证明，也不是非存在下界。未发现所写范围内fatal；只升内部结果，外审/新颖性未认证。
- Status：complete restricted proof; independently reconstructed and exactly audited; unrefereed。Truth为明确状态的实际存在界；Value为极值幅度模拟边界；Novelty未认证；Mechanism为缺口矩和Jensen；Ambition保留全类题OPEN。
- Related Files：[正文](../current/weighted_congestion/step_dag/polynomial_extremal_all_in.md)、[独立审查](../reviews/weighted_congestion/step_dag/polynomial_extremal_all_in_review.md)；具体代码和冻结记录见正文审计合同。


## WC-CYCLIC-CLONE-IMPROVEMENT-CYCLES-v1 — 循环窗口复制实现近线性倍率的真实改善环

- Exact Statement / Objects / Domain / Quantifiers / Assumptions / Scope / Conclusion：对每个d≥2、每个1≤α<ρ_d=sup_t>0[(d+1)(1+t)^d+t^(d+1)]/[d+(1+t)^(d+1)]，存在正有理权、全部资源费用x^d、人人策略族2^E的有限MODEL游戏，真实偏离图含严格α改善环，同时全空是精确PNE。ρ_d/d→1，故任何全局实值函数（含非可分）不能在该游戏全部严格α改善边下降。
- Definitions：循环类窗口、互补资源对、双同序翻转及加入guard后的有限gain锥；每名light的rank完整枚举而非期望。
- Dependencies：WC-MODEL、WC-R1-MULTIPLIER-BARRIER、WC-ALLSTATE-SELECTOR-ALTERNATIVE-v1；循环窗口的逐人秩均匀化、非负dual零坐标连接、严格锥替代。
- Evidence：完整一般证明；独立先重构瓶颈后攻击冻结稿；代码、参数、seed（适用时）、源码hash、精度和实际结果由正文末节链接。
- Counterevidence / Objections：Only all-improvement termination and global strict ordinal potentials are obstructed; no PNE-nonexistence, chosen-step or minimizer-selection obstruction. 该游戏有精确PNE；不能据此否定唯一题。未见所述范围内fatal。
- Status：complete stated-scope proof; independently reconstructed and exactly audited; unrefereed。Truth=所写方法边界；Value=可复用构造或分离；Novelty=未认证；Mechanism=循环窗口的逐人秩均匀化、非负dual零坐标连接、严格锥替代；Ambition=全类仍OPEN。
- Related Files：research/current/weighted_congestion/cyclic_clone_improvement_cycles.md；research/reviews/weighted_congestion/ordinal_potentials/cyclic_clone_improvement_cycles_review.md；tests/audits/weighted_congestion/cyclic_clone/verify_lift.py；tests/audits/weighted_congestion/cyclic_clone/verify_cycle_certificate.py；tests/audits/weighted_congestion/cyclic_clone/independent_lift.py；evidence/runs/weighted_congestion/cyclic_clone/lift.json；evidence/runs/weighted_congestion/cyclic_clone/cycle_certificate.json；evidence/runs/weighted_congestion/cyclic_clone/independent_lift.json。


## WC-COMMON-POWER-MIXTURE-MINIMIZER-OBSTRUCTION-v1 — 共同幂混合全局最小点的线性障碍

- Exact Statement / Objects / Domain / Quantifiers / Assumptions / Scope / Conclusion：对每个d≥32，存在四玩家四资源、正有理权/系数、纯d次费用且有精确PNE的有限游戏，使任意非零非负Borel测度μ（全部状态目标有限）给出的Pμ(s)=Σ_e a_e∫_(p>0)x_e(s)^p dμ(p)每个全局最小点都非α-PNE，对全部1≤α<d/16成立；μ可依完整游戏。
- Definitions：同一实例的两独立移动者及固定背景；保留原a_e、全部资源共同非负μ，p>0时0^p=0。
- Dependencies：WC-MODEL；两构件目标差的同一正系数逐实幂严格分离并积分。
- Evidence：完整一般证明；独立先重构瓶颈后攻击冻结稿；代码、参数、seed（适用时）、源码hash、精度和实际结果由正文末节链接。
- Counterevidence / Objections：Does not cover per-resource normalization, elimination of fixed-background players followed by a new coefficient rule, arbitrary separable objectives, nonseparable objectives or PNE nonexistence. 该游戏有精确PNE；不能据此否定唯一题。未见所述范围内fatal。
- Status：complete stated-scope proof; independently reconstructed and exactly audited; unrefereed。Truth=所写方法边界；Value=可复用构造或分离；Novelty=未认证；Mechanism=两构件目标差的同一正系数逐实幂严格分离并积分；Ambition=全类仍OPEN。
- Related Files：research/current/weighted_congestion/common_power_mixture_obstruction.md；research/reviews/weighted_congestion/ordinal_potentials/common_power_mixture_review.md；tests/audits/weighted_congestion/ordinal_potentials/verify_common_power_mixture.py；tests/audits/weighted_congestion/ordinal_potentials/independent_common_power_mixture.py；evidence/runs/weighted_congestion/common_power_mixture/author.json；evidence/runs/weighted_congestion/common_power_mixture/independent.json。


## WC-WEIGHT-CLASS-TRIANGULAR-POTENTIAL-v1 — 有限权类别三角排序混合势

- Exact Statement / Conclusion：对每个d≥2,k≥1，全MODEL中全球正权值至多k种的每个游戏有A_(d,k)-PNE，其中A∈[1,d)唯一满足A=Σ_(j=0)^(k−1)((d−1)/A)^j。三角排序混合势的每个单方局部min均是该均衡，全部严格A改善终止；任意人数、权比、费用/策略均覆盖。A≤B=(d−1)/(d^(1/k)−1)，固定k时A∼d^(1−1/k)，k≤ln d/lnln d且d≥16给2d/ln d。
- Objects / Domain / Quantifiers / Assumptions / Definitions / Scope：完全采用MODEL，费用系数任意非负实数、次数≤d，任意有限多资源策略（含空）、零/常数费用；A、π、λ、S、固定/可动及代表权定义固定在[正文](../current/weighted_congestion/weight_bands/finite_weight_class_potentials.md)。k不是资源各自种类数或某状态活跃类别数。
- Dependencies：WC-MODEL、WC-TRIANGULAR-ORDER-DEFINITION；完整边际、有限最小化、背景展开和取整链分别由正文证明。
- Evidence：先仅给精确statement独立重构瓶颈后冻结攻击；另一份informed攻击准确区分；两份独立Fraction源码/参数/seed（适用时）/精度/hash/实际结果由正文末节连接。
- Counterevidence / Objections：无尚成立fatal；固定d时k无界A趋d，不得用子类C=2,d0=16替代全类题。B粗方案与两权原Claim未被静默改写。
- Status：complete structural proof; independently reconstructed and exactly audited; unrefereed。Truth=所写子类/归约；Value=有限可动权类桥；Novelty=未认证；Mechanism=三角排序累计下界；Ambition=全类目标仍OPEN。
- Related Files：research/current/weighted_congestion/weight_bands/finite_weight_class_potentials.md；research/reviews/weighted_congestion/weight_types/finite_weight_classes_reconstruction_review.md；research/reviews/weighted_congestion/weight_types/finite_weight_classes_informed_review.md；tests/audits/weighted_congestion/weight_types/verify_triangular_classes.py；tests/audits/weighted_congestion/weight_types/independent_triangular_classes.py；evidence/runs/weighted_congestion/weight_types/triangular_classes.json；evidence/runs/weighted_congestion/weight_types/independent_triangular_classes.json。


## WC-WEIGHT-CLASS-FIXED-BACKGROUND-v1 — 固定玩家背景的非负多项式精确吸收

- Exact Statement / Conclusion：对每个d≥2,k≥1，全MODEL中只有可动玩家（策略族非单元素）的权值至多k种时，即使任意固定玩家的权种类无限制，仍有A_(d,k)-PNE。c_e(B_e+x)展开仍非负系数并逐状态保持可动者成本；无可动玩家时唯一状态精确。
- Objects / Domain / Quantifiers / Assumptions / Definitions / Scope：完全采用MODEL，费用系数任意非负实数、次数≤d，任意有限多资源策略（含空）、零/常数费用；A、π、λ、S、固定/可动及代表权定义固定在[正文](../current/weighted_congestion/weight_bands/finite_weight_class_potentials.md)。k不是资源各自种类数或某状态活跃类别数。
- Dependencies：WC-MODEL、WC-WEIGHT-CLASS-TRIANGULAR-POTENTIAL-v1；完整边际、有限最小化、背景展开和取整链分别由正文证明。
- Evidence：先仅给精确statement独立重构瓶颈后冻结攻击；另一份informed攻击准确区分；两份独立Fraction源码/参数/seed（适用时）/精度/hash/实际结果由正文末节连接。
- Counterevidence / Objections：无尚成立fatal；固定d时k无界A趋d，不得用子类C=2,d0=16替代全类题。B粗方案与两权原Claim未被静默改写。
- Status：complete structural proof; independently reconstructed and exactly audited; unrefereed。Truth=所写子类/归约；Value=有限可动权类桥；Novelty=未认证；Mechanism=三角排序累计下界；Ambition=全类目标仍OPEN。
- Related Files：research/current/weighted_congestion/weight_bands/finite_weight_class_potentials.md；research/reviews/weighted_congestion/weight_types/finite_weight_classes_reconstruction_review.md；research/reviews/weighted_congestion/weight_types/finite_weight_classes_informed_review.md；tests/audits/weighted_congestion/weight_types/verify_triangular_classes.py；tests/audits/weighted_congestion/weight_types/independent_triangular_classes.py；evidence/runs/weighted_congestion/weight_types/triangular_classes.json；evidence/runs/weighted_congestion/weight_types/independent_triangular_classes.json。


## WC-WEIGHT-CLASS-CLUSTER-ROUNDING-v1 — 窄权簇的单向取整与近似均衡提升

- Exact Statement / Conclusion：对每个d≥2,k≥1,R≥1，若每个可动玩家有固定标签τ使v_τ≤w_i≤Rv_τ，其中k个代表权为正，则全MODEL原游戏有R^d A_(d,k)-PNE；固定玩家无需取整且权不受限。代表可重复/缺席；R=exp(1/d)时损失e，结合类别门槛给2e d/ln d的该明确子类界。
- Objects / Domain / Quantifiers / Assumptions / Definitions / Scope：完全采用MODEL，费用系数任意非负实数、次数≤d，任意有限多资源策略（含空）、零/常数费用；A、π、λ、S、固定/可动及代表权定义固定在[正文](../current/weighted_congestion/weight_bands/finite_weight_class_potentials.md)。k不是资源各自种类数或某状态活跃类别数。
- Dependencies：WC-MODEL、WC-WEIGHT-CLASS-FIXED-BACKGROUND-v1；完整边际、有限最小化、背景展开和取整链分别由正文证明。
- Evidence：先仅给精确statement独立重构瓶颈后冻结攻击；另一份informed攻击准确区分；两份独立Fraction源码/参数/seed（适用时）/精度/hash/实际结果由正文末节连接。
- Counterevidence / Objections：无尚成立fatal；固定d时k无界A趋d，不得用子类C=2,d0=16替代全类题。B粗方案与两权原Claim未被静默改写。
- Status：complete structural proof; independently reconstructed and exactly audited; unrefereed。Truth=所写子类/归约；Value=有限可动权类桥；Novelty=未认证；Mechanism=三角排序累计下界；Ambition=全类目标仍OPEN。
- Related Files：research/current/weighted_congestion/weight_bands/finite_weight_class_potentials.md；research/reviews/weighted_congestion/weight_types/finite_weight_classes_reconstruction_review.md；research/reviews/weighted_congestion/weight_types/finite_weight_classes_informed_review.md；tests/audits/weighted_congestion/weight_types/verify_triangular_classes.py；tests/audits/weighted_congestion/weight_types/independent_triangular_classes.py；evidence/runs/weighted_congestion/weight_types/triangular_classes.json；evidence/runs/weighted_congestion/weight_types/independent_triangular_classes.json。


## WC-ANCHORED-POLYNOMIAL-CYCLE-LOCK-v1 — 锚定三元多项式时钟的双轮改善环全状态锁定

- Exact Statement / Conclusion：任意n≥3,p≥0的MODEL两动作游戏，若有按0,…,n−1翻全1再同序翻回0的严格α≥1改善环，则仅加2L个正单项式资源、保持原玩家/权重/旧资源及两个动作标签，可得到无α-PNE游戏，次数≤max(p,D)。L=C(n−1,2)，B上界全部原状态玩家成本，η为环最小严格差，δ=max_(0,i,j)(1−min(w0,wi,wj)/(w0+wi+wj))，D=ceil[ln(4α²BL/η)/ln(1/δ)]。全有理输入给全有理输出。
- Objects / Domain / Quantifiers / Assumptions / Definitions / Scope：全MODEL的任意有限两动作实例及实α≥1，正实权、非负实多项式、允许原空动作和零费用；输入严格双同序环、B>0、0<η≤B及0<δ<1定义固定在[正文](../current/weighted_congestion/anchored_cycle_lock.md)。输出只含两个增广动作，不能再添空动作或2^E。
- Dependencies：WC-MODEL、锚定010/101 literal和真实负载、有限最大最小、最早反位修复及泄漏差估计；不以某个环存在定理为编译证明前提。
- Evidence：审查者读作者稿前完整独立重构，再攻击冻结hash；两份不互相导入的Fraction代码分别核验真实三玩家base+compiler和条件式时钟几何。源码hash、运行环境、参数、seed及结果见正文审计合同。
- Counterevidence / Objections：无尚成立fatal；D依完整实例，未控制q=max(p,D)上的α ln q/q，不能用本接口替代全类否定或上界。
- Status：complete stated-scope proof; independently reconstructed and exactly audited; unrefereed。Truth=所述全状态编译定理；Value=可复用cycle-to-no-PNE桥；Novelty=未认证；Mechanism=锚定三元与最早反位修复；Ambition=唯一全类判定仍OPEN。
- Related Files：research/current/weighted_congestion/anchored_cycle_lock.md；research/reviews/weighted_congestion/ordinal_potentials/anchored_cycle_lock_review.md；tests/audits/weighted_congestion/cyclic_clone/verify_clock_compiler.py；tests/audits/weighted_congestion/cyclic_clone/independent_clock.py；evidence/runs/weighted_congestion/cyclic_clone/cycle_lock_triad.json；evidence/runs/weighted_congestion/cyclic_clone/independent_clock.json。


## WC-ANCHORED-DEGREE-THREE-LOCK-OBSTRUCTION-v1 — 三次双轮环的锚定时钟次数保持障碍

- Exact Statement / Conclusion：显式四玩家有理三次基体G，权(1,1/2,1/4,1/8)、α=21/20，有严格双同序环及0101/1010精确PNE。任意λ>0，对λG只加anchor0的T012,T013,T023互补010/101同费pair，每T独立任意degree≤3非负多项式（可零/省略），若0000玩家0及1100玩家2的总αmargin均≥0，则0101/1010全部四个翻位margin均<0，故仍αPNE。
- Objects / Domain / Quantifiers / Assumptions / Definitions / Scope：精确系数、对象和变换固定在[正文](../current/weighted_congestion/anchored_clock_degree_barrier.md)；完整采用MODEL的真实成本和零成本不等式。只限明示基体、anchor、phase、同pair两侧同费及degree≤3；不排常数倍degree、其他anchor、两侧异费、辅助玩家或其他拓扑。
- Dependencies：WC-MODEL, WC-CUBIC-ANCHOR-CONE-DEFINITION；前提的直接证明及使用位置由正文明确。
- Evidence：先从精确statement独立重构，再攻击freeze；两份不互相导入的Fraction实际成本代码及运行命令/环境/hash/输入/seed适用性由正文审计合同连接。
- Counterevidence / Objections：无尚成立fatal；只限明示基体、anchor、phase、同pair两侧同费及degree≤3；不排常数倍degree、其他anchor、两侧异费、辅助玩家或其他拓扑。
- Status：complete fixed-architecture proof; independently reconstructed and exactly audited; unrefereed。Truth=上述限定命题；Value=可复用桥或精确方法限制；Novelty=未认证；Mechanism=四对显式有理x³基体；三种anchor0 triple各degree0..3共12列；四个简单非负dual仅用γ0、γ2，clock残差非正且base严格负。 Ambition=全类匹配上界判定仍OPEN。
- Related Files：research/current/weighted_congestion/anchored_clock_degree_barrier.md；research/reviews/weighted_congestion/ordinal_potentials/anchored_clock_degree_barrier_review.md；tests/audits/weighted_congestion/cyclic_clone/verify_clock_degree_barrier.py；tests/audits/weighted_congestion/cyclic_clone/independent_clock_degree_barrier.py；evidence/runs/weighted_congestion/cyclic_clone/clock_degree_barrier.json；evidence/runs/weighted_congestion/cyclic_clone/independent_clock_degree_barrier.json。


## WC-ANTICHAIN-CORE-NORMAL-FORM-v1 — 去包含支配与必选背景的空交反链核心规范形

- Exact Statement / Conclusion：任意d≥0 MODEL游戏有不依α的有限core变换：或给显式exactPNE，或得到同次数界、原玩家非空子集/原权的H，人人≥2非空两两不可包含且交集空的策略；固定lift将每个实α≥1的任意H αPNE提升原游戏。同一固定d、实α处，全类无αPNE反例存在等价于该core策略结构的正整数权/单位单项式x^j(j≤d)反例存在。
- Objects / Domain / Quantifiers / Assumptions / Definitions / Scope：精确系数、对象和变换固定在[正文](../current/weighted_congestion/template_certificates/integer_counterexample_normal_form.md)；完整采用MODEL的真实成本和零成本不等式。提升单向、不保人数/资源数、不保最佳因子或逐状态反投影；没有无限规范模板的规模截止或全类C,d0。旧整数v1身份/保人数义务不改。
- Dependencies：WC-MODEL, WC-ANTICHAIN-CORE-DEFINITION, WC-INTEGER-MONOMIAL-COUNTEREXAMPLE-v1；前提的直接证明及使用位置由正文明确。
- Evidence：先从精确statement独立重构，再攻击freeze；两份不互相导入的Fraction实际成本代码及运行命令/环境/hash/输入/seed适用性由正文审计合同连接。
- Counterevidence / Objections：无尚成立fatal；提升单向、不保人数/资源数、不保最佳因子或逐状态反投影；没有无限规范模板的规模截止或全类C,d0。旧整数v1身份/保人数义务不改。
- Status：complete direct proof; independently reconstructed and exactly audited; unrefereed。Truth=上述限定命题；Value=可复用桥或精确方法限制；Novelty=未认证；Mechanism=A_i为包含极小动作，F_i=∩A_i=∩S_i，B_e为全体必选权和；用c_e(B_e+x)、a减F_i，删除singleton；原成本=core成本+自身偏离不变K_i≥0。 Ambition=全类匹配上界判定仍OPEN。
- Related Files：research/current/weighted_congestion/template_certificates/integer_counterexample_normal_form.md；research/reviews/weighted_congestion/template_certificates/antichain_core_normal_form_review.md；tests/audits/weighted_congestion/template_certificates/verify_antichain_core.py；tests/audits/weighted_congestion/template_certificates/independent_antichain_core.py；evidence/runs/weighted_congestion/template_certificates/antichain_core.json；evidence/runs/weighted_congestion/template_certificates/independent_antichain_core.json。

## WC-UNIFORM-CLOCK-BUDGET-BARRIER-v1 — 统一低泄漏锚定时钟预算的普适次数障碍

- Exact Statement / Objects / Domain / Quantifiers / Assumptions / Definitions / Scope / Conclusion：任意n≥3、整数p≥0的MODEL两动作严格α≥1双同序环、任意锚点，B为全状态原成本有限上界、η为环最小严格差、L=C(n−1,2)、δ=max锚定三元(1−minw/Σw)。若任意整数D≥1满足δ^D≤η/(4α²BL)，则全局权比R>α、D>(R+1)ln(4α²BL/η)>2(α+1)ln(2α)，且每个实q≥D均有αlnq/q<α/(α+1)<1；包括实际输出最高次数。只封闭该统一充分预算的目标否定证书，非实际最小锁定次数下界或全类PNE存在结论。
- Dependencies：MODEL；WC-R3-DENSE-LOCAL-v1 的 strict R-FIP；WC-ANCHORED-CLOCK-DEFINITION 的双轮输入和统一预算；初等对数单调性。非从均衡存在性推出无改善环。
- Evidence：完整一般证明；先独立重构后冻结攻击；两份Fraction、有理对数余项及最小D反验，作者另重算真实三玩家输入。
- Counterevidence / Objections：不将(U)提升为必要条件；actual有向clock差、非统一幅度/次数、多项式或其他架构不受限制；无αPNE不代表无更大倍率PNE。
- Status：complete budget-obstruction proof; independently reconstructed and exactly audited; unrefereed。Truth仅预算障碍，Value为封闭输入优化路线，Novelty未认证，Mechanism为R-FIP与最坏三元耦合，Ambition保持唯一全类题OPEN。
- Related Files：[统一低泄漏锚定时钟预算的普适次数障碍](../current/weighted_congestion/uniform_clock_budget_barrier.md)、[独立审查](../reviews/weighted_congestion/ordinal_potentials/uniform_clock_budget_barrier_review.md)；两代码与冻结记录从正文读取。


## WC-CLONE-FRONT-PHASE-QUOTIENT-v1 — 循环窗口前沿的扭转平移与精确相位商

- Exact Statement / Conclusion：任意m≥2,N≥1正类权、每类至少参与一test的循环窗口两动作lift（保留零系数资源），同test全部index及pair两侧同费；共同index平移并wrap翻bit逐成本/偏离协变。合法class prefix/suffix由x∈(Z2N)^m编码，对角T使x各加1，商恰(2N)^(m−1)，单clone留front动作恰±1（N1两邻居重合）。有显式2N长forward成本表及backward r+1交换式。
- Objects / Domain / Quantifiers / Assumptions / Definitions / Scope：精确条件与完整定义见[正文](../current/weighted_congestion/class_front_phase_quotient.md)；采用MODEL非负费用、正权和真实偏离。count是互异MODEL动作状态；单测试子项可缺席类，但不能把空/空标签当两策略。class0商动作改变所有相对相位，须保mover标签。不是对全front出口或PNE的断言。
- Dependencies：WC-MODEL, WC-CLASS-FRONT-DEFINITION；共同前提的使用与自足代数证明由正文分节给出。
- Evidence：先由精确statement独立重构再攻击实际冻结hash；两份独立Fraction代码/输入/命令/精度/seed适用性及结果见正文审计合同。
- Counterevidence / Objections：无未结范围内fatal；count是互异MODEL动作状态；单测试子项可缺席类，但不能把空/空标签当两策略。class0商动作改变所有相对相位，须保mover标签。不是对全front出口或PNE的断言。
- Status：complete stated-scope proof; independently reconstructed and exactly audited; unrefereed。Truth=所述表示/机制/反例；Value=可复用精确接口；Novelty未认证；Ambition=唯一全类题仍OPEN。
- Related Files：[正文](../current/weighted_congestion/class_front_phase_quotient.md)、[独立审查](../reviews/weighted_congestion/ordinal_potentials/class_fronts_review.md)及正文末节的audit/run。


## WC-CLASS-INTERNAL-CLOCK-FRONT-OBSTRUCTION-v1 — 类内时钟的前沿出口障碍与不同步反例

- Exact Statement / Conclusion：任意α≥1，同权类内递增锚定010/101同费三元时钟在每条合法front边的own old=new=c(2w)，clock margin≤0。显式12player/N4/degree8/α21/20有理窗口lift有strict24步环，但phase(0,4,0)六端点margin<−9/50；512front恰8稳定，仍有内部clone margin>1/5。故strict环不自动给每个类front改善端点，任意此类clock不新增front内改善。
- Objects / Domain / Quantifiers / Assumptions / Definitions / Scope：精确条件与完整定义见[正文](../current/weighted_congestion/class_front_phase_quotient.md)；采用MODEL非负费用、正权和真实偏离。局部lemma要两端均非full触发；front使用递增锚定三元，不涵盖任意乱序wrap。实例非αPNE，有离front出口；不排所有类内compiler或其他同步机制。
- Dependencies：WC-MODEL, WC-CLONE-FRONT-PHASE-QUOTIENT-v1, WC-CLASS-FRONT-FIXTURE；共同前提的使用与自足代数证明由正文分节给出。
- Evidence：先由精确statement独立重构再攻击实际冻结hash；两份独立Fraction代码/输入/命令/精度/seed适用性及结果见正文审计合同。
- Counterevidence / Objections：无未结范围内fatal；局部lemma要两端均非full触发；front使用递增锚定三元，不涵盖任意乱序wrap。实例非αPNE，有离front出口；不排所有类内compiler或其他同步机制。
- Status：complete stated-scope proof; independently reconstructed and exactly audited; unrefereed。Truth=所述表示/机制/反例；Value=可复用精确接口；Novelty未认证；Ambition=唯一全类题仍OPEN。
- Related Files：[正文](../current/weighted_congestion/class_front_phase_quotient.md)、[独立审查](../reviews/weighted_congestion/ordinal_potentials/class_fronts_review.md)及正文末节的audit/run。


## WC-DEGREE-LOCAL-COST-COMPRESSION-v1 — 有限次局部成本空间与全成本资源压缩

- Exact Statement / Conclusion：固定n≥1,m_i≥1,d≥0与正实权，D=Σ_i m_i Σ_(T⊆N\i,|T|≤d)∏_(j∈T)(m_j−1)。全部玩家cost tables位于维D局部张量空间；任意游戏可用≤D正系数单项式签名类型及≤Σm_i零费私有动作marker保所有state/deviation成本和动作标签，core可保持。binary时D=2nΣ_(r≤min(d,n−1))C(n−1,r)，一般D=O_d((Σm_i)^(d+1))。
- Objects / Domain / Quantifiers / Assumptions / Definitions / Scope：精确条件与完整定义见[正文](../current/weighted_congestion/template_certificates/selector_local_moments.md)；采用MODEL非负费用、正权和真实偏离。不保原资源身份、单位系数或算法效率；零成本可用0正资源但markers保MODEL合法。所有人数/动作数无界，维界不是全类规模截止。
- Dependencies：WC-MODEL, WC-DEGREE-LOCAL-SPACE-DEFINITION；共同前提的使用与自足代数证明由正文分节给出。
- Evidence：先由精确statement独立重构再攻击实际冻结hash；两份独立Fraction代码/输入/命令/精度/seed适用性及结果见正文审计合同。
- Counterevidence / Objections：无未结范围内fatal；不保原资源身份、单位系数或算法效率；零成本可用0正资源但markers保MODEL合法。所有人数/动作数无界，维界不是全类规模截止。
- Status：complete structural proof; independently reconstructed and exactly audited; unrefereed。Truth=所述表示/机制/反例；Value=可复用精确接口；Novelty未认证；Ambition=唯一全类题仍OPEN。
- Related Files：[正文](../current/weighted_congestion/template_certificates/selector_local_moments.md)、[独立审查](../reviews/weighted_congestion/template_certificates/selector_local_moments_review.md)及正文末节的audit/run。


## WC-SELECTOR-LOCAL-MOMENT-INTERFACE-v1 — 全状态择证的低阶矩极锥与小支撑接口

- Exact Statement / Conclusion：固定任意完整selector h及实α≥1，其概率dual等价conv{Ψ_h(s)}∩K^-非空；Ψ只含所选动作边和≤d对手动作的signed discounted矩，K为全部允许资源cost vectors锥。若dual存在，有≤D+1状态支撑dual。binary指定单mover翻位支撑且α1时，dual存在等价两方向≤d上下文矩匹配/无degree≤d严格多项式分离；α>1仅primitive非负tests乘性夹逼。
- Objects / Domain / Quantifiers / Assumptions / Definitions / Scope：精确条件与完整定义见[正文](../current/weighted_congestion/template_certificates/selector_local_moments.md)；采用MODEL非负费用、正权和真实偏离。不能删selector-support marginal-polytope条件、改成任意局部一致矩或强求feature=0；不要求stationary/recurrent，未保证每selector可行或单mover证书。
- Dependencies：WC-DEGREE-LOCAL-COST-COMPRESSION-v1, WC-ALLSTATE-SELECTOR-ALTERNATIVE-v1, WC-ANTICHAIN-CORE-NORMAL-FORM-v1, WC-SELECTOR-MOMENT-DEFINITION；共同前提的使用与自足代数证明由正文分节给出。
- Evidence：先由精确statement独立重构再攻击实际冻结hash；两份独立Fraction代码/输入/命令/精度/seed适用性及结果见正文审计合同。
- Counterevidence / Objections：无未结范围内fatal；不能删selector-support marginal-polytope条件、改成任意局部一致矩或强求feature=0；不要求stationary/recurrent，未保证每selector可行或单mover证书。
- Status：complete structural proof; independently reconstructed and exactly audited; unrefereed。Truth=所述表示/机制/反例；Value=可复用精确接口；Novelty未认证；Ambition=唯一全类题仍OPEN。
- Related Files：[正文](../current/weighted_congestion/template_certificates/selector_local_moments.md)、[独立审查](../reviews/weighted_congestion/template_certificates/selector_local_moments_review.md)及正文末节的audit/run。


## WC-TRANSIENT-PARITY-SELECTOR-DUAL-v1 — 完全暂态奇偶支撑的择证对偶

- Exact Statement / Conclusion：每个d≥0、每个d+3维正实权向量，都有binary无self-loop且唯一2cycle的selector，及全部支撑在暂态state的概率λ，对全部signature的degree0..d列在α1恰零、对所有α≥1非正；限制core proper signatures仍成立。flag0偶active states均匀分布，active维d+2使cost active-degree≤d+1严格低于维数。
- Objects / Domain / Quantifiers / Assumptions / Definitions / Scope：精确条件与完整定义见[正文](../current/weighted_congestion/template_certificates/selector_local_moments.md)；采用MODEL非负费用、正权和真实偏离。仅证明transient dual可行；唯一2cycle自身也有dual，不证明暂态必要/更优，不给任意selector或全类存在。
- Dependencies：WC-MODEL, WC-SELECTOR-LOCAL-MOMENT-INTERFACE-v1, WC-PARITY-SELECTOR-DEFINITION；共同前提的使用与自足代数证明由正文分节给出。
- Evidence：先由精确statement独立重构再攻击实际冻结hash；两份独立Fraction代码/输入/命令/精度/seed适用性及结果见正文审计合同。
- Counterevidence / Objections：无未结范围内fatal；仅证明transient dual可行；唯一2cycle自身也有dual，不证明暂态必要/更优，不给任意selector或全类存在。
- Status：complete structural proof; independently reconstructed and exactly audited; unrefereed。Truth=所述表示/机制/反例；Value=可复用精确接口；Novelty未认证；Ambition=唯一全类题仍OPEN。
- Related Files：[正文](../current/weighted_congestion/template_certificates/selector_local_moments.md)、[独立审查](../reviews/weighted_congestion/template_certificates/selector_local_moments_review.md)及正文末节的audit/run。

## WC-ANCHORED-ACTUAL-MARGIN-INTERFACE-v1 — 锚定双轮时钟的有向差分、线性预算与逐次数锐效率

- Exact Statement / Objects / Domain / Quantifiers / Assumptions / Definitions / Scope / Conclusion：任意n≥3、α≥1、正权两动作MODEL基体的严格双同序环，任意逐三元非负多项式同费010/101锚定pair：两半合法margin同为g_i，非法firstopp i的真实clock margin恰g_i+Σ_{j later同anchor}Δ_ij，Δ≥0。γ_i为两半base margin之min、B覆盖全部base成本时，γ_i+g_i>0及每i<j的g_i+Δ_ij>αB给全状态无αPNE的n+L条充分线性约束。保环必要Σg=−(α−1)ΣS、(α−1)ΣS<Γ；degree≤D的Δ/S锐界为逐0..D单项式max，一般不取最高次；κ逐状态列界另给保原αPNE的全玩家充分条件。明示四玩家三次基体有43次实际证书，原uniform预算选值91。
- Dependencies：WC-MODEL、锚定010/101实际用户表、非负多项式凸组合、有限最大最小；条件障碍只使用本文保环预算。
- Evidence：完整一般推导、精确冻结审查及真实资源Fraction核验；源码、seed/参数、Python版本、误差控制和实际运行hash由[正文](../current/weighted_congestion/anchored_clock_actual_margins.md)末节连接。
- Counterevidence / Objections：约束仅充分、总预算仅必要；κ稳定条件非必要，保firstopp失败不等于PNE；不保证给定D可行或B可多项式时间计算。43不称最优，91只是统一充分预算选值。没有一般次数效率或全类结论。 所述范围无尚成立fatal；外审和新颖性未认证。
- Status：complete stated-scope interface proof; independently reconstructed and exactly audited; unrefereed。Truth仅精确范围；Value为可复用表示/选态接口；Mechanism见正文；Ambition保留WC-TARGET OPEN。
- Related Files：[正文](../current/weighted_congestion/anchored_clock_actual_margins.md)、[独立审查](../reviews/weighted_congestion/ordinal_potentials/actual_clock_margins_review.md)，配套代码、输入、证据见正文审计合同。

## WC-SHARED-SIDE-TRUNCATED-ROSENTHAL-v1 — 同权主玩家共享侧资源的统一强迫截断势均衡

- Exact Statement / Objects / Domain / Quantifiers / Assumptions / Definitions / Scope / Conclusion：对每个d≥2、有限同权u>0 hubs/任意正异权lights，每light唯一source、每side唯一light并允许任意hub子集H_j及空集/含source、两动作副本同费非负degree≤d；若α≥A_d=[1−(d−1)d^(−d/(d−1))]^(−1)，且逐light弱UF为F_v(u+w)+ΣG_j(w)≥α[F_v(W_v)+ΣG_j(w+|H_j|u)]，则所写截断Rosenthal势任hub单翻位局部最小点配全anti lights给αPNE。A_d≤2d/ln d对全部d≥2，常数仅限该子类。
- Dependencies：WC-MODEL、WC-SHARED-SIDE-BUDGET-POTENTIAL-v1、本文正部望远镜(TR)及UF聚合预算；无外部定理。
- Evidence：完整一般推导、精确冻结审查及真实资源Fraction核验；源码、seed/参数、Python版本、误差控制和实际运行hash由[正文](../current/weighted_congestion/shared_side_truncated_potential.md)末节连接。
- Counterevidence / Objections：共同hub权、每side唯一light、每light唯一source、动作副本同费与UF最坏负载均承重。不覆盖异权hub、多source side或UF失败且直接AS+B未满足的全类情形；子类C2,d0=2不代替唯一题。 所述范围无尚成立fatal；外审和新颖性未认证。
- Status：complete structural proof; independent bottleneck reconstruction and frozen attack; exactly audited; unrefereed。Truth仅精确范围；Value为可复用表示/选态接口；Mechanism见正文；Ambition保留WC-TARGET OPEN。
- Related Files：[正文](../current/weighted_congestion/shared_side_truncated_potential.md)、[独立审查](../reviews/weighted_congestion/shared_side_truncated_potential_review.md)，配套代码、输入、证据见正文审计合同。

## WC-SHARED-SIDE-BUDGET-POTENTIAL-v1 — 同权主玩家共享侧资源的直接侧势预算均衡

- Exact Statement / Objects / Domain / Quantifiers / Assumptions / Definitions / Scope / Conclusion：相同unique-light/shared-hub/unique-source拓扑，任意d≥0、实α≥1；H_j(m)=Σ_{r≤m}[G_j(w+ru)−αG_j(ru)]_+、M_v=αF_v(u+W_v)−F_v(u)。若逐light AS为F_v(W_v)+ΣG_j(w+|H_j|u)≤α[F_v(u+w)+ΣG_j(w)]，逐source Σ_jH_j(|H_j|)≤M_v，则同一有限势每个单hub局部最小点配全anti是αPNE。无需UF或α≥A_d。
- Dependencies：WC-MODEL、同权fixed-light势边际、source重置误差、有限局部最小化；不调用TR/M标量界或UF聚合。
- Evidence：完整一般推导、精确冻结审查及真实资源Fraction核验；源码、seed/参数、Python版本、误差控制和实际运行hash由[正文](../current/weighted_congestion/shared_side_truncated_potential.md)末节连接。
- Counterevidence / Objections：AS与源预算是充分假设，不证明所有该拓扑游戏都满足；仍限同权hub、unique-light/unique-source和同费副本。此ID扩大degree/alpha域并改变假设，未静默改UF-v1；后置抽象攻击不冒充初次未读稿全证明重构。 所述范围无尚成立fatal；外审和新颖性未认证。
- Status：complete conditional proof; independently attacked after abstraction; exactly audited; unrefereed。Truth仅精确范围；Value为可复用表示/选态接口；Mechanism见正文；Ambition保留WC-TARGET OPEN。
- Related Files：[正文](../current/weighted_congestion/shared_side_truncated_potential.md)、[独立审查](../reviews/weighted_congestion/shared_side_truncated_potential_review.md)，配套代码、输入、证据见正文审计合同。

## WC-WEIGHT-INTERACTION-HEIGHT-POTENTIAL-v1 — 潜在可动用户共占高度的三角排序势

- Exact Statement / Objects / Domain / Quantifiers / Assumptions / Definitions / Scope / Conclusion：对任意d≥2 MODEL游戏，先吸收singleton固定玩家背景；非空可动玩家图置i→j当wi>wj且二者各有策略使用同一资源，k为DAG最长路径顶点数。则有A_(d,k)-PNE及全部严格A改善下降的身份子集资源可加势。A仍为A=Σ_{j<k}((d−1)/A)^j在[1,d)唯一根；全局不同权值数任意大，无可动者精确PNE。
- Dependencies：MODEL、跨资源共同层秩、原三角势根及排序边际、第7节背景吸收；完整证明见原稿第11–12节。H2只在闭词端点使用边际估计。
- Evidence：先仅据新exact Claim自主重构，再攻击冻结hash；两路Fraction从身份排序/实际端点重算，运行参数/seed/精度/hash见正文第13节与JSON。
- Counterevidence / Objections：潜在共占height是同一个全局玩家图参数，不能换成逐资源种类数或单点用户数；k无全类统一界。原有限权类ID中的k不变，本新ID单独扩大输入类。 已修去解释中未经本命题证明的存在暗示，无尚成立fatal；未外审/新颖性未认证。
- Status：complete structural proof; independently reconstructed and exactly audited; unrefereed。Truth为所写结构界/必要条件；Value为相容层秩复用；Mechanism为身份子集排序及固定势望远镜；Ambition全类仍OPEN。
- Related Files：[正文第11–13节](../current/weighted_congestion/weight_bands/finite_weight_class_potentials.md)、[独立重构与冻结攻击](../reviews/weighted_congestion/weight_types/interaction_height_review.md)，代码/证据由正文进入。

## WC-REALIZED-INTERACTION-CHAIN-CYCLE-v1 — 严格改善闭合词中的实际共占长权链

- Exact Statement / Objects / Domain / Quantifiers / Assumptions / Definitions / Scope / Conclusion：对任意d≥2、实α≥1 MODEL游戏的非空有限严格α改善闭合真实单方词，令M为至少移动一次玩家；其余按沿词不变策略吸收背景。在M上按wi>wj及某端点状态实际同资源置弧，height为k，则α<A_(d,k)。所以任正整数K≥1、α≥A_(d,K)的这种闭词必含至少K+1顶点降权实际共占链，各边可来自不同状态/资源。
- Dependencies：MODEL、跨资源共同层秩、原三角势根及排序边际、第7节背景吸收；完整证明见原稿第11–12节。H2只在闭词端点使用边际估计。
- Evidence：先仅据新exact Claim自主重构，再攻击冻结hash；两路Fraction从身份排序/实际端点重算，运行参数/seed/精度/hash见正文第13节与JSON。
- Counterevidence / Objections：只为给定严格改善闭词的必要链，不构造近d环，不证明无PNE；未访问状态不用相容，不把整链断言为同一状态共占。动态换秩改变势，尚无SCC出口或瞬态dual。 已修去解释中未经本命题证明的存在暗示，无尚成立fatal；未外审/新颖性未认证。
- Status：complete structural proof; independently reconstructed and exactly audited; unrefereed。Truth为所写结构界/必要条件；Value为相容层秩复用；Mechanism为身份子集排序及固定势望远镜；Ambition全类仍OPEN。
- Related Files：[正文第11–13节](../current/weighted_congestion/weight_bands/finite_weight_class_potentials.md)、[独立重构与冻结攻击](../reviews/weighted_congestion/weight_types/interaction_height_review.md)，代码/证据由正文进入。

## WC-AFFINE-FULL-SIGNATURE-RIGIDITY-v1 — 异权仿射全签名成本射线的刚性

- ID/version / 中文数学名称：WC-AFFINE-FULL-SIGNATURE-RIGIDITY-v1，异权仿射全签名成本射线的刚性。独立新身份，不改先前局部矩/压缩/暂态Claim。
- Exact Statement / Objects / Domain / Quantifiers / Assumptions / Definitions / Scope / Conclusion：每个n≥2及不全相等正实权w、binary标签，V_i(s)=s_iΣ_jw_js_j的任何同玩家/权/标签完整成本保真有限非负系数多项式资源表示，在忽略零费/无人用资源后只能为全n玩家仅动作1使用、费用a_e x且Σa_e=1。任意提高有限degree仍不能把全部正资源潜在用户支持降到<n；V为有限表示锥K_fin的极射线。正费用指非零多项式，潜在用户指至少一合法动作使用资源；完整成本含所有真实偏离成本。
- Dependencies：WC-MODEL、非负资源锥及binary完整成本表定义、正权使非零多项式在正负载严格正、两人真实负载差分、二项式严格不等式、有限非负叠加。全部在[正文第9节](../current/weighted_congestion/template_certificates/selector_local_moments.md)自足证明，不依赖其他均衡定理。
- Evidence：独立审查先从较弱statement重构并强化到n≥2/不全等权/极射线，再攻击冻结7a2ee0b7；规范正文只读diff通过。独立Fraction审计225个pair代数、2331列逐face消元和7160个等权边界成本位置，代码/run由正文第10节接入；有限检查不替一般实参数/任意有限degree证明。
- Counterevidence / Objections：只限完整成本保真、固定玩家/权/标签和有限表示锥，不声称闭包/暴露射线；等权存在≤2用户高次资源表示。原V有全0精确PNE，不限制改权/加玩家/仅保均衡或单向lift，也不反驳≤D资源数量压缩，未解全类题。等权n≥3用pair资源x^q/(2^q−1)和私人常数可保全成本；n2等权也有非线性同负载表示。无尚成立数学fatal。
- Status：complete structural proof; independently reconstructed and exactly audited; unrefereed。Truth仅完整成本保真表示障碍；Value为资源锥不可局部化边界；Mechanism为一对异权contrast加solo预算饱和；Novelty/外审未认证，Ambition保留WC-TARGET OPEN。
- Related Files：[同一正文§9–10](../current/weighted_congestion/template_certificates/selector_local_moments.md)、[独立审查刚性部分](../reviews/weighted_congestion/template_certificates/selector_local_moments_review.md)、`tests/audits/weighted_congestion/template_certificates/verify_affine_full_signature.py`、`evidence/runs/weighted_congestion/template_certificates/affine_full_signature_rigidity.json`。


## WC-SELECTOR-UNBOUNDED-MOVER-SUPPORT-v1 — 奇环缺陷择证的无界跨玩家补偿与锐支撑门槛

- ID/version / 中文数学名称：WC-SELECTOR-UNBOUNDED-MOVER-SUPPORT-v1，奇环缺陷择证的无界跨玩家补偿与锐支撑门槛。独立新身份，不改原始局部矩/压缩/暂态或刚性Claim。
- Exact Statement / Objects / Domain / Quantifiers / Assumptions / Definitions / Scope / Conclusion：每个奇n≥3、d≥1、共同正权及任意binary缺陷择证（每态翻转一条相等邻边左端点），完整/proper签名degree0..d均有显式2n周期均匀dual。每个1≤α<2^d的任意dual须对全部n名移动者及其两方向给正质量；令r=(2^d−α)/(α2^d−1)，每方向≥r^(n−1)/[(1+α)Σ_(j<n)r^j]，最小状态支撑恰2n；α1各方向1/(2n)。min-index择证在α≥2^d有单mover二点dual，最小支撑恰2。定量界不宣称除α1外锐；所有负载与偏离按MODEL。
- Dependencies：MODEL、完整动作签名矩阵与proper/core定义、奇环缺陷、逐资源离散原函数、两个正pair列及私人degree0列；[正文§11](../current/weighted_congestion/template_certificates/selector_local_moments.md)自足给出。
- Evidence：先据精确statement独立重构，再攻击冻结736cff45正文与canonical差异；两套不互相导入的整数/Fraction审计，实际命令、参数、seed不适用、Python版本/hash与范围由正文§12接入。有限检查不替一般证明。
- Counterevidence / Objections：只限制统一有界移动者/状态支撑的dual构造；原族等权、有完整α1 dual，不是无PNE例，不排依n/动作数/D的支撑界或无界多玩家拼接；端点二点只限min-index择证。奇数n、d≥1、严格α<2^d承重；没有尚成立fatal，外审/新颖性未认证。
- Status：complete structural proof; independently reconstructed and exactly audited; unrefereed。Truth为精确支撑定理；Value为排除有限玩家局部拼接；Mechanism为pair正列迫闭环补偿；Ambition保持WC-TARGET OPEN。
- Related Files：[正文](../current/weighted_congestion/template_certificates/selector_local_moments.md)、[独立审查](../reviews/weighted_congestion/template_certificates/selector_mover_support_review.md)，代码与冻结结果见§12。


## WC-ANCHORED-FULL-UNIFORM-BUDGET-ESCAPE-v1 — 原全三元统一时钟的低泄漏预算非必要证书

- Exact Statement / Objects / Domain / Quantifiers / Assumptions / Definitions / Scope / Conclusion：明示四玩家三次基体、权(1,1/2,1/4,1/8)、α=21/20；保留全部T012/T013/T023原010/101同费pair与统一M=2αB，只将次数取80，所得游戏全部16态有指定严格α出口且保留八条环边，但δ^80>η/(4α²BL)；满足(U)的最小整数为91。只证明(U)在原全三元统一幅度架构中也非必要，不称80最优或一般增长族。 完整资源、全部状态有理外包及B/η/δ见[正文第4节](../current/weighted_congestion/anchored_clock_degree_barrier.md)。只有两个明示动作，不能添加空策略。
- Dependencies：MODEL、明示固定三次基体、原时钟literal和真实负载、有限有理整数幂；不以LP或uniform充分条件证明非存在。
- Evidence：独立statement重构后攻击冻结2d9591c0；两路不互相导入的Fraction重建全部资源/状态/偏离、互补、八行区间与80/90/91幂反查。
- Counterevidence / Objections：稀疏43次例不能独自证明原uniform架构逃逸，本条补上该范围。固定实例不解决唯一题；uniform预算障碍在原假设下保持。无尚成立fatal；未外审/新颖性未认证。
- Status：complete finite certificate; independently reconstructed and exactly audited; unrefereed。Truth为有限全状态证书及预算非必要；Value为原架构边界；Mechanism为真实有向差；Ambition全类仍OPEN。
- Related Files：[正文](../current/weighted_congestion/anchored_clock_degree_barrier.md)、[独立审查](../reviews/weighted_congestion/ordinal_potentials/anchored_clock_degree_barrier_review.md)；两份新代码和新冻结记录从正文审计合同进入，基体输入复用原43次JSON而不改写。
