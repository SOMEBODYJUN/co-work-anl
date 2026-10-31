# 作者证明候选：共享 UD 停车的确定性 tiny state-profile 势

2026-10-18，/root/sol_general_repair。对应新 Exact ONLY：sol_general_repair_shared_ud_tiny_state_potential_19_10_exact_v1.md，SHA256 80fd4ff5b6aab2993e42b995ea369e9441543e754cf3642800c84a784c63cf1d。先仅给 root，fresh reviewer 应先冻结独立重构。本稿不改原38c/ce05或其canonical，不使用随机working note作为确定性证明，不声称新颖性或一般 UM 突破。无端到端代码。

## 1. 输入、常数、真实值桥与叶匹配

严格按新 Exact：k≥1，helper集合J，H=|J|≥1，j的outer为i(j)，Σ_(j∈J_i)w_j=1，全homes物理互异，ν=max w_j≤1/(4096k⁴)。helper own-home unit，fallback normalized states只用B；额外 leaves正支持也只在B，在 ε=15/16 满足exact threshold-UD iff。全部零incidences保留，不参加辅助正值选项；最终留自己的private。

令V为normalized-flat最优最小group值。有标准且自足的 OPT(P(Q))=2−V、1≤OPT≤2：从bundles选attaining states，selectors放该private，所取正incidences输出resource，其余全部原jobs留private；反向C<2使resource unit jobs独占，selector所在state输出值≥2−C。OPT=2边界由正向式给V=0。所有未选state payload、零jobs和额外leaf groups在此完整矩阵中均保留。

叶在 ε 下正好等价于得到其H_l中一枚资源。若叶图无full matching，则actualV<ε，baseline C≤2给ratio<32/17<19/10。以下假设full leaf matching存在。令M为B上vacancy matroid：S∈M iff全部叶可匹配到B\S。这是相应满秩transversal matroid的dual；独立性由一次普通matching判断，不调用隐式优化oracle。

固定常数

    ε=15/16,  c=5/16,  θ=1/32,
    ξ=1/(2^20 H^2),  τ=1/(2048H),  w_stop=25/128.

ξ是算法自己由显式H计算的有理数，不是输入精度oracle。

## 2. state profile下的实际fractional welfare

profile S 为每helper选一个原fallback indexed state或empty；empty没有candidate。资源candidate e=(j,s,u) 的outer-value是w_jp_jsu。给一个profile，允许在它的positive candidates中分配B资源给helpers，同时完整匹配全部叶；每资源至多一个owner。得到outer utility

    W_i=Σ_(j∈J_i)w_jΣ_u p_j,s_j,u x_ju,    0≤W_i≤1.

这些B分配不必满足每helper阈值，也暂不分配homes。其fractional polytope只是bipartite资源ownership/叶matching的普通network polytope：helper claims可任意多，leaf row恰一，resource列≤一。它是integral，任何fractional点可分解成真实B allocations；可用dummy owner承接unused resources。输入positive candidates和leaf H edges均显式。

给任意正outer weights λ，λ-linear maximum称 f_λ(S)。可由M的resource-parallel extension上的weighted matroid greedy求出：每positive candidate是一份copy，所有同资源copies平行，另给每资源一个零值dummy copy以补足base；candidate权重是λ_i(j)w_jp_jsu。读出selected copies后给每个剩余资源集求leaf matching。也可用mincostfull-leafmatching计算同值。都是标准确定性poly matching，不是优化未知state profile。

在全fallback-option ground上，f_λ是monotone submodular：weighted matroid rank为各threshold rank的非负积分，按每option的一组不同candidate copies取union保持submodularity。每helper一个option或empty是partition约束。只在以下证明使用该性质；算法不求其全局最优。

若actualV≥ε，则存在一个profile O，使对每λ

    f_λ(O)≥ε²Σ_iλ_i.                                  (2.1)

证明：取实际达到allocation。outer拿走home j时，其helper失去unit-own正物品，必须有fallback attaining state和B bundle值≥ε。保留这些helpers的fallback states/bundles，其他helpers设empty；每outer被取homes的w总量≥ε。额外叶从实际bundle保留一枚H_l物品，与helpers所取B不交，故M-independent。福利≥εΣ_iλ_iΣ_(被outer取home j∈J_i)w_j≥ε²Σλ。这里只用于soundFAIL反证，算法没有获得此O或actual target。

## 3. profile势及其λ-optimal面

对profile S定义

    Φ(W)=(θ/k)Σ_iW_i−Σ_i(c−W_i)_+²,
    P(S)=max_(W feasible at S) Φ(W).

其范围为 −kc²≤P≤θ；Φ单调、可微、凹，gradient λ_i=θ/k+2(c−W_i)_+始终正，gradient Lipschitz常数二。若W*达到P，令d_i=(c−W_i*)_+、Dsum=Σd_i，则first-order optimality给

    f_λ(S)=λ·W*,     λ_min≥θ/k.                         (3.1)

还需一个近似optimum的稳定性。把问题等价写为min Σd_i²−(θ/k)ΣWi，linear constraints d_i≥c−Wi、d_i≥0，再加原flow polytope。任意feasible(W,d)与optimum(W*,d*)满足

    P(S)−Φ(W)≥||d(W)−d*||²,                            (3.2)

因为convex quadratic的first-order项在最优点非负，其余恰为deficit平方差。此不需要算法精确求QP；仅用精确optimum的数学存在。

## 4. stable weighted-matroid state exchange lemma

固定profile S的λ-optimal fractional B allocation W。替换helper j的state为s'（或empty），令S'为新profile、Δ_j=f_λ(S')−f_λ(S)。存在S'下的fractional feasible W'，满足

    λ·(W'−W)=Δ_j,
    max_i |λ_i(W_i'−W_i)|≤λ_i(j)w_j,
    Σ_i |λ_i(W_i'−W_i)|≤2λ_i(j)w_j.                    (4.1)

完整理由：先在λ-optimal integral matroid base上证明。删掉所有旧j-copies；每删除一个当前base内元素，使用最大权可行replacement保持weighted-optimal base。weighted matroid exchange说明删一个元素只需一个replacement；不在base则无需改变。此阶段除helper j外的helper效用只增；总增加的weighted值G不超过j初始weighted值A≤λ_i(j)w_j，因为最优值不随ground删除增加。

再逐个加入新j-copies；每个新元素用fundamental-circuit最小权交换，或不入base，以保持weighted-optimality。其他helpers效用只减，总weighted减少L不超过j最终weighted值B≤λ_i(j)w_j，因为增加ground不降低weighted最优值。

helper级变化为j的B−A与其他helpers的非负gains-minus-losses，总gain≤A、总loss≤B。聚到outers后，非j-owner坐标在[−B,A]，j所属outer坐标在[−A,B]；weighted L1不超过A+B+|A−B|=2max(A,B)。得到(4.1)。同outer其他helpers的gain/loss也包含，不能当j独占outer。

fractional λ-optimal点是λ-optimal integral bases的凸组合：network integral，且同一linear optimal face的所有正权重vertices仍optimal。对每个base执行上述更新再平均，(4.1)的L∞/L1界由凸性保留。无需算法显式求这个coupling，它只给某个新profile可达到的势lower bound。

于是

    ||W'−W||²
      ≤λ_min^(-2) max_i|λ_iΔW_i|·Σ_i|λ_iΔW_i|
      ≤2(λ_i(j)/λ_min)²w_j²=:B_j.                     (4.2)

Φ的二次smoothness给

    P(S')−P(S)≥Φ(W')−Φ(W*)≥Δ_j−B_j                   (4.3)

当W=W*为当前Φ-optimum。此是实际不同profile之间的非单调resource重算，但同一全局势的进展界；不声称逐原job transient-load路径。

## 5. 对每个坏profile必有poly大进展或actual soundFAIL

对target profile O的helper options o_j，令S_j=S−{s_j}+{o_j}。option-submodularity给

    Σ_j [f_λ(S_j)−f_λ(S)]≥ f_λ(O)−2f_λ(S).             (5.1)

证明：f(O)≤f(S)+Σ_j[f(S+o_j)−f(S)]。每项≤Δ_j+l_j，其中l_j=f(S)−f(S−s_j)；submodularity给Σl_j≤f(S)。empty和相同option也按此式合法。

若actualV≥ε，合(2.1)、(3.1)，令Dsum=Σd_i，有

    Σ_jΔ_j≥ε²Σλ−2λ·W*
      ≥2(ε²−2c)Dsum−(2−ε²)θ
      =(65/128)Dsum−287/8192.                          (5.2)

使用 λ·W*≤θ+2cDsum，ε²=225/256。

由Σ_(j∈J_i)w_j²≤ν和(4.2)，当k≥2，

    Σ_jB_j≤(2ν/λ_min²)Σ_iλ_i²
       ≤1/(2048k³)+Dsum/(16k³)+(5/8)Dsum/k²
       ≤1/16384+(21/128)Dsum.

其中Σλ_i²≤θ²/k+4θDsum/k+4cDsum，ν≤1/(4096k⁴)。因此当Dsum≥9/80时，

    Σ_j[P(S_j)−P(S)]
       ≥(11/32)Dsum−575/16384
       ≥293/81920=:ρ>0.                               (5.3)

k=1须用actual λ_min=λ_1而非floor粗界：ΣB_j≤2ν≤1/2048，(5.2)在Dsum≥9/80给剩余≥885/40960>ρ。不能遗漏这个small-k分支。

所以如果actualV≥ε且exact-optimal deficit sum≥9/80，至少一个单helper state替换的P提升≥ρ/H。算法枚举所有helper的全部原fallback options加empty，必包含这些未知target o_j；不要求知道O。

## 6. 只用有理matching实现势的poly近似

给profile S，确定性返回feasible fraction flow及 W_hat，值 P_hat=Φ(W_hat)，使

    P(S)−ξ≤P_hat≤P(S).

从W=0和任意full leaf matching开始，用rational Frank–Wolfe。第t步求gradient λ=θ/k+2(c−W)_+，用第2节固定profile的weighted matching/matroid-greedy linear oracle得到integral payoff V_t，再取 γ_t=2/(t+2)，W←(1−γ_t)W+γ_tV_t，flow也取同凸组合。

smooth concavity、diameter²≤k给 gap_(t+1)≤(1−γ_t)gap_t+γ_t²k，所以t步后gap≤4k/(t+2)。取T_FW=ceil(4k/ξ)，次数poly(k,H)，只需linear matching，不调用exact QP/SDP或profile oracle。

每个integral V_t payoff来自原w,p，能以输入系数公共分母D_1表示；t次后的flow恰为过去vertices的权重2(r+1)/(t(t+1))之和，因此denominator可取D_1t(t+1)，bit长度poly。gradient、所有matching comparisons、Φ、最终P_hat都有poly位长。每次profile评价固定同一T_FW、起点与tie规则，P_hat(S)是确定函数。

## 7. 完整确定性profile算法与soundFAIL

初始化所有helpers empty，额外叶匹配存在。循环：

1. 对当前S运行第6节，得到W_hat,P_hat。
2. 若全部W_hat_i≥25/128，转第8节输出。
3. 否则枚举每helper j的所有fallback states加empty，分别求新profile的P_hat。如果某替换使P_hat增加至少τ=1/(2048H)，选最大值、固定索引打破平局，继续。
4. 若没有这样的替换，输出baseline并判内部actualV<ε。

最后一步确sound：若actualV≥ε，某W_hat_i<25/128给d_hat_i>15/128；由(3.2)与ξ，exact-optimal d_i≥15/128−sqrtξ>9/80，因为sqrtξ≤1/1024<3/640。故(5.3)给某P提升≥ρ/H，新旧近似差至少ρ/H−ξ>1/(2048H)=τ，矛盾。

每次实际P_hat至少增τ，而其range在[−kc²,θ]，所以至多(θ+kc²)/τ+1=O(kH)次profile moves。所有candidate评价数是原helper states数加H，不枚举指数profile。no-improvement FAIL时actualOPT=2−V>17/16，baseline C≤2给ratio<32/17。输入actualV低也不会导致无穷运行，势range仍保证终止。

## 8. 给定成功profile的共同prefix-flow与全部group回填

此时fractionalW_hat_i≥25/128。固定helper states，令

    a_iu=max_(j∈J_i) w_jp_j,s_j,u,

empty为零。a_iu≤ν，Σ_ua_iu≤1。将同outer的fractional claims聚合，给每资源该outer内达到a_iu的helper只会增utility；全部叶fractionalmatching与总resource容量仍保留。

按每outer的a_iu降序排序positive edges，把每个prefix claim质量F_l取floor作为integer lower count。构造source→outer nested-prefix链→resource→sink，并将source→每leaf lower=upper一、leaf→H_l→同resource容量一合在一张circulation。原fractional flow见证可行，所有lower/upper整数，maxflow integrality给完整叶matching和整数outer claims。

weighted summation by parts使每outer损失≤max a_iu≤ν（无须这些artificial coefficients总和恰一）。将每个outer-owned resource交给argmax helper，实际weightedfallback值

    W_i≥25/128−ν≥799/4096>19/100.

取q=1/10，Good helpers为chosen-state Q_j≥q。其outer home mass z_i满足 W_i≤z_i+q(1−z_i)，故z_i>q。保留Good helper的fallback bundle，给outer其homes，其他helpers各own-home；额外UD叶保留matching，它们quality≥ε。homes与B不交、全home互异，所有groups的真实quality≥q。

选这些原indexed states、放全部selectors、只输出所领正incidence jobs，其余所有原jobs包括未选states和zero jobs留各自private。得到完整普通P的C≤2−q=19/10；unit selectors给OPT≥1，所以ratio≤19/10。

## 9. scope、规模与待独立攻击点

新算法完全不需要原SA1 feasible点：每步只依赖Q、当前profile、普通matching线性oracle、显式rational arithmetic和integer prefix-flow。helpers数H、states、edges全显式；T_FW=O(kH²)、每轮candidate evaluations和O(kH)总moves是absolute polynomial，未按p分母值循环。完全矩阵有S+U台机器、G+I jobs、S+2I finite endpoints，含额外叶、zero/inactive/duplicate indexed payload。

最承重可攻击处是第4节任意λ-optimal fractional allocation的stable helper-state基更新，以及第5节由其L∞+L1支付curvature并对所有k闭合常数；其次是第6–7节near-optimal deficits与soundFAIL，不是随机profile存在或给定target回填。所有extras必须B-only threshold-UD、每outer单state与原k⁴-tiny均仍承重。非tiny heavy states、多outerstates、一般nonUD额外groups或一般UM主目标未解。

本稿是新确定性候选，等待Exact-first独立重构；原随机working note只留历史断点，不当证明。无端到端实现、有限audit、外审或全球新颖性认证。
