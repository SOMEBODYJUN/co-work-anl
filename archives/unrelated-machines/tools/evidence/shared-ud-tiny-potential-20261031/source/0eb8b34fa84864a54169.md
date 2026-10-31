## 12. 新的 v4 身份：共享 UD 叶、单 outer greedy 与多 outer k² 势

本节及后续新增节独立于前175行的 v1。前缀 SHA256 为 `84d6031655ac43d9c5726ed2cac6f5241e709743232290e604d767602613778a`，本草稿不复制或改动它。v1继续是原域上的SA1/CDF/MW/平方势条件期望算法。未发布v2/v3仅为保留历史字节的中间草稿，不另建canonical资产。本v4有两个分支：k1用标准submodular greedy解除tiny上界；k≥2用primal势及新k²曲率。不倒改v1或中间草稿的公式、软件、审查身份；k²不借用另一vector方差lemma。

新 Claim：**UM-MULTI-OUTER-SINGLE-STATE-TINY-HOME-19-10-APPROX-v4**。

- **Objects / Domain：** §13 的完整 typed normalized-flat Q、显式生成的全部 ordinary P(Q) 原 jobs。任意输入变量 k≥1 个 single-state outers、全局互异 homes、unit-own helpers、任意共享 B fallback 菜单；还允许任意多个 B-only exact-threshold-UD leaves。k1只保正权归一化、不额外限制ν；k≥2要求最大home权重ν≤1/(16384k²)。
- **Quantifiers：** 对每个该域完整显式 Q，用同一个固定确定性 worst-case 总位多项式算法输出全部原 jobs 的原有限端点 assignment。helpers 数、leaves 数、states 数、资格度、支持宽度、分母数值与 k 都不作固定常数。
- **Exact Statement：** C_max(σ)≤(19/10)OPT(P(Q))。输入只有 Q，不给 feasible point、OPT、joint law、target profile、精度参数或 scheduling oracle。
- **Assumptions：** 标准确定性完整 matching、min-cost flow、整数 lower-bound circulation 和精确有理算术。k1使用固定helper顺序greedy；k≥2精确profile potential最优点只用于证明，算法用普通matching线性oracle做固定次数rational Frank–Wolfe。不调用exact QP/SDP或指数profile优化oracle。
- **Scope：** 仍须single-state outers、所有homes独占、k≥2的k²-tiny上界、额外叶正支持只在B、以及固定ε=15/16的exact threshold-UD iff；k1没有额外tiny条件。没有覆盖多 outer states、home 重叠、home 上的额外叶、一般 nonUD extra groups 或一般 UM。
- **Conclusion：** 通过真实 target 的反证得到 sound FAIL，或者生成真实正质量 allocation 并输出全部原 jobs。FAIL 不是必要点/某个 λ 线性优化失败的替代名称。
- **Dependencies：** normalized-flat 实际桥 OPT=2−V；transversal dual/vacancy matroid；weighted matroid rank 次模性与 symmetric basis exchange；smooth concave potential、rational Frank–Wolfe；共同 prefix-flow 的整数性。上述标准工具不认领新颖性。
- **Evidence：** v4新Exact `8948b47c…` 单独冻结并交fresh审者先行；其独立重构及后读、最终实读尚待完成，本草稿不先认定结论。前身k⁴域Exact `80fd4ff5…` 与作者Proof `409ce884…` 原件保留；root已回报完整读它们并核stable exchange、曲率、FW位长和soundFAIL，也回报NSW已核k⁴作者Proof，具体审查记录不替代v4新审。root与本作者分别实际Fraction核新k²代数。作者另有完整自核与有限exchange枚举，范围见§20。
- **Counterevidence / Objections：** 目前作者及 root 所报定点核算未见 fatal；最承重义务是 §16 任意 fractional optimum 的 stable coupling、§17 从 actual target 强制多项式进展、§18 不借用 exact potential oracle。保留等待独立重构的状态。
- **Status：** 新的待独立后置审查量词扩域候选；尚无完整算法软件、外审或全球新颖性认证。原v1或未发布v2/v3的审查不自动升级至v4；一般UM-TARGET-v1继续OPEN。
- **Related Files：** 本页既有 §1–11 的 v1；[实际值桥](normalized_weighted_menu_santa_value_and_size.md)；[threshold-UD 判别及条件叶流](normalized_menu_configuration_certificate_preservation.md)；[classical 模型边界](model_and_classical_barriers.md)。新冻结来源身份见 §20，最终审查关联由 root 统一登记。

## 13. 完整新域、原矩阵与实际阈值

令 J_i 为 outer i 的 helpers，H=|J|≥1。outer i 只有一个原 indexed state，其正系数为互异 homes g_j 上的 w_j>0，Σ_(j∈J_i)w_j=1；所有 (i,j) 的 homes 全局互异。每 helper H_j 有 own indexed state，正支持为 g_j、系数一；其所有其他 fallback states 是 B 上任意显式 normalized 向量 p_jsu≥0，B 与 homes 不交。helper可无fallback；重复indexed states仍为不同private machines。令ν=max_j w_j，k1不额外限制ν（归一化本身给ν≤1）；k≥2要求ν≤1/(16384k²)。原k⁴域包含于此：k1解除上界、k2相等、k>2严格更宽。

此外有任意多个 leaf groups，正支持全部在 B。对每 leaf l 定义

    E_l={u∈B: max_s p_lsu≥ε},
    b_l=max_s Σ_(u∈B\E_l)p_lsu,       ε=15/16.

要求 b_l<ε。于是对任意 bundle A，leaf 的原菜单值≥ε iff A∩E_l非空：正向从一条系数≥ε的原 state incidence 得到；反向若不交 E_l，每个 state 的整条尾巴总和都小于 ε。这是多项式显式检查，不把 leaves 视为固定单一 state 或字面 unit-singleton。除了上述 outers、helpers 与 leaves，没有其他 groups。

每个 normalized group 的原菜单非空。全部 indexed state/resource pair 至多一条 listed incidence，允许列出零；零 incidence 可在任意原资源上，但不参与正支持资格。未用资源、未选 state、零 incidence 全保留。结构随 Q 给出，不要求从一般 ordinary 矩阵识别。

按前文原编译，每 state 一台独立 private machine，每原资源一台 resource machine；每 group 一枚 unit selector，只能去该 group 的全部原 private machines；每 listed incidence 一枚原 job，private time 等于原系数、resource time 精确一，其余∞。若 groups、states、incidences、resources 数为 G,S,I,U，则有 S+U 台原机器、G+I 枚原 jobs、S+2I 个 finite endpoints。稠密展开也仅为这些显式数量的多项式。

令 V 是原 normalized-flat 的最佳最小 group 值。实际有 OPT=2−V，1≤OPT≤2。给 disjoint bundles，各 group 选 attaining state，把所取正 incidences 输出 resource，其余 payload 留原 private，selector 在所选 private 的负载为2−该组值。反向 C<2 使所有 resource-unit jobs 独占，selector 所在 state 输出值至少2−C。OPT=2 边界由正向式同样闭合。baseline 为各 selector 任放原 private、全部 incidences 留 private，所有原 jobs 均完成，C≤2。

若叶图 l→E_l 无完整 matching，exact iff 直接给 actual V<ε；baseline 的比值小于2/(2−ε)=32/17<19/10。以下只需叶图存在完整 matching 的分支；空叶集合允许，空 B 或 rank0 也不跳过。

## 14. 固定 helper profile 的可实现线性 oracle

定义 B 上 vacancy matroid M：X 独立 iff 所有 leaves 能完整匹配到 B\X。它是满 rank transversal matroid 的 dual；只需普通 matching 作 independence/rank 查询。其 rank 可以为零，某些资源可以是 loop。

helper profile A 为每 helper 选一个原 fallback indexed state或 empty，不选 own state。固定 A 时，将 B 分给 chosen helper states，并同时完整匹配所有 leaves；每资源至多一个 owner。helper 可取多个资源，其 chosen-state 值 Q_j≤1，outer 的辅助 welfare 为

    W_i=Σ_(j∈J_i) w_j Q_j ∈[0,1].

其 fractional feasible region 是普通 bipartite ownership/leaf-matching network：leaf row恰一、resource列≤一、helper claims无额外下界。它 integral；把 unused resources 作为 dummy 所有权即可。它不要求每 helper 达到 ε，亦暂不分配 homes。

对正向量 λ，令 f_λ(A) 是固定 profile 下最大 λ·W。每 helper candidate (j,s,u) 权重为 λ_i(j)w_jp_jsu；同资源的 candidates 是 M 的 parallel copies，另加每资源零 dummy。于是 f_λ 是 weighted matroid rank，普通 matching 可确定性计算：令 t_u=max_(active j at u) λ_i(j)w_jp_j,s_j,u，空 max为零，则

    f_λ(A)=Σ_u t_u − min_(full leaf matching) Σ_(matched u) t_u.

未被叶使用的资源交给达到 t_u 的 helper，或留 dummy。此只优化给定的 A，不优化指数 joint profile。

把每个原 fallback option 看成它的 candidate copies 集，f_λ 在全部 options 上单调次模：weighted matroid rank 是各权重 threshold rank 的非负组合，按 option 取 union 保持次模性。每 helper 只选一 option 或 empty。 这个数学集合函数在非profile集合上可含同一helper的多个options，供次模不等式使用；normalized Q_j≤1、W_i≤1与stable大小界只在合法一option profiles上使用。

若 actual V≥ε，则存在一个共同实际 benchmark profile O，对所有 λ 同时满足

    f_λ(O)≥ε²Σ_i λ_i.                                (14.1)

证明只取实际 allocation：outer 拿走 home j 时，helper 的 own state 值为零，故必须有一个 B fallback state/bundle 值≥ε。保留这些 helpers 的 fallback states/bundles，其他 helpers 设 empty；每 outer 被拿 homes 的 w 质量至少 ε，故 welfare≥ε²。每叶保留实际 bundle 中一枚 E_l 资源，与这些 helper bundles 不交。算法没有得到、查询或枚举 O；它只在进展与 soundFAIL 的反证中出现。

### 14.1 k1：不需要tiny的确定性greedy分支

此处固定λ_1=1，f(A)为§14的integral matching welfare，f(∅)=0。按输入固定helper顺序，当前已选options为G_(j−1)；在该helper的全部fallback indexed states加empty中，选使f(G_(j−1)+option)最大的一个，每次均用普通matching精确计算。完成后得合法profile G，再求一次其integral最佳B allocation和完整叶matching，记W=f(G)。不使用fractional potential或prefix舍入。

这个greedy对全profile最大值f_opt给1/2保证。对任意benchmark options O_j，单调次模性给

    f(O)≤f(G)+Σ_j [f(G+O_j)−f(G)].

每个final marginal不大于该helper轮到时的marginal，后者不大于当步greedy gain；全部gain望远镜和为f(G)，故f(O)≤2f(G)。这是标准partition-constrained submodular工具的自足直接应用。

若W<1/4，则f_opt≤2W<1/2<ε²=225/256；由(14.1)反证actualV<ε，输出baseline C≤2，比值小于32/17。若W≥1/4则成功：integral B allocation中称Q_j≥q=1/10的helpers为Good，W≤z+q(1−z)给z≥1/6>q，直接按§19回填全部groups和原jobs，C≤19/10。额外叶仍使用原ε=15/16的完整matching；没有把leaf域改成另一个阈值。

本分支没有home权重tiny要求，没有ν的prefix损失。helpers无fallback时仍有empty；无完整叶matching已在§13走实际baseline分支。greedy至多逐个原option做polynomially many matching查询，cost为原w_jp_jsu的有理数，位长与次数均为输入多项式。

## 15. k≥2：凹势及 near-optimum 稳定性

以下§15–18只用于k≥2分支；k1已经由§14.1完成，不套用其tiny、曲率或prefix损失。取固定常数及输入确定参数

    c=5/16,  θ=1/32,  ξ=1/(2^20 H²),
    τ=1/(2048H),  w_stop=25/128.

定义

    Φ(W)=(θ/k)Σ_iW_i − Σ_i(c−W_i)_+²,
    P(A)=max_(fixed-profile feasible W) Φ(W).

−kc²≤P(A)≤θ；Φ 单调凹且可微，gradient Lipschitz常数二。精确 optimum W* 的 gradient 为 λ_i=θ/k+2d_i，d_i=(c−W_i*)_+，λ_min≥θ/k。first-order optimality给

    f_λ(A)=λ·W*.                                    (15.1)

此 λ* 与精确 optimum 只在分析中出现，算法不免费调用它。若 W_hat 是同 profile 的可行点，则

    P(A)−Φ(W_hat)≥||d(W_hat)−d(W*)||².                (15.2)

把最大化等价写成最小化 Σd_i²−(θ/k)ΣW_i，约束 d_i≥c−W_i、d_i≥0 与原 network feasible region。最优点处凸目标的一阶项非负，剩余恰为 deficit 平方差，得到(15.2)；不要求 W* 唯一。

## 16. 任意最优 fractional point 的稳定 profile 交换

固定 λ>0、profile A 和其中任意 λ-optimal fractional W。只替换 helper j 为一个原 fallback或 empty，得到 A'，记 Δ_j=f_λ(A')−f_λ(A)。存在新 profile 下的 λ-optimal fractional W'，使

    λ·(W'−W)=Δ_j,
    max_i |λ_i(W_i'−W_i)|≤λ_i(j)w_j,
    Σ_i |λ_i(W_i'−W_i)|≤2λ_i(j)w_j.                  (16.1)

先在最大权 integral matroid basis上证明。删除全部旧 j copies 时，每删一个已入 basis 的元素只需一次最佳 replacement 即可保持全局最优；插入每个新 j copy 时至多一次 fundamental-circuit 交换。单元素最优敏感性由 symmetric basis exchange 直接给出；零 dummy 保证 rank不降。

删除阶段除 j 外的 helpers 只增，总 weighted 增量 G≤旧 j 贡献 A_0，因为 ground 删除不能提高最优值。插入阶段其他 helpers 只减，总 weighted 损量 L≤新 j 贡献 B_0，因为 ground 增加不降最优值。A_0,B_0≤λ_i(j)w_j。聚到 outers 后，owner 坐标为 B_0−A_0+g_owner−l_owner∈[−A_0,B_0]；其他坐标在[−B_0,A_0]，L1≤A_0+B_0+|A_0−B_0|。同 outer 的其他 helpers 已包括，叶 matching 允许整体重排。

任意 fractional optimal network point 可分解成同一 linear-optimal face 的 integral vertices；各 helper independent claims 可补零 dummy 为 basis。逐分量更新后平均，(16.1)仍成立。分解只用于存在性，算法不计算它。

因此

    ||W'−W||² ≤ 2(λ_i(j)/λ_min)²w_j² =: B_j.

当 W=W* 为当前 Φ-optimum 时，smoothness 给真正跨 profile 的势增

    P(A')−P(A)≥Δ_j−B_j.                             (16.2)

这不是原 jobs 逐个迁移时的 transient-load 声称。

## 17. actual 高值强制单替换进展

对(14.1)的未知共同 O，令 A_j 只把 helper j 替换成 O 的 option。单调次模性给

    Σ_j [f_λ(A_j)−f_λ(A)] ≥ f_λ(O)−2f_λ(A).          (17.1)

具体地，f(O)≤f(A)+Σ_j[f(A+o_j)−f(A)]；每 add marginal≤单替换增量加删除损失 l_j=f(A)−f(A−a_j)，且Σl_j≤f(A)。empty、原 option 相同及重复 indexed options 均合法。

设 Dsum=Σd_i。若 actual V≥ε，由(14.1)、(15.1)及 λ·W*≤θ+2cDsum，

    Σ_jΔ_j≥ε²Σλ−2λ·W*
           ≥(65/128)Dsum−287/8192.                  (17.2)

曲率由 tiny 而非 LP marginal 付款。Σ_(j∈J_i)w_j²≤ν；k≥2 时，

    Σ_jB_j ≤ (2νk²/θ²)Σ_iλ_i²
      ≤2νk + (8νk/θ + 8cνk²/θ²)Dsum
      ≤1/16384+(21/128)Dsum.

这里Σλ_i²≤θ²/k+4θDsum/k+4cDsum；新ν≤1/(16384k²)给constant≤1/(8192k)≤1/16384，Dsum系数≤1/(64k)+5/32≤21/128。没有使用H≥const·k⁵。若Dsum≥9/80，合(16.2)、(17.2)得到

    Σ_j[P(A_j)−P(A)]
      ≥(11/32)Dsum−575/16384
      ≥293/81920=:ρ.                               (17.3)

因此本k≥2分支有某个单helper option替换增P≥ρ/H。算法枚举每helper的全部原fallback options加empty，必含该替换，不用知道O或λ*。k1不在此付款，其独立greedy分支无需任何ν上界。

## 18. 有理后端、完整搜索与 soundFAIL

固定 profile A 的 P(A) 用 rational Frank–Wolfe 近似。从 W=0和任意完整叶 matching开始；第 t=0,1,…步取当前 gradient λ，调用 §14 的普通 matching linear oracle 得 integral payoff R_t，令 γ_t=2/(t+2)，同时更新 W及完整 flow 为(1−γ_t)旧值+γ_t新值。

Φ 的 smoothness、域 diameter²≤k 给 gap_(t+1)≤(1−γ_t)gap_t+kγ_t²，故 t 步后 gap≤4k/(t+2)。固定执行 N=ceil(4k/ξ) 次，返回可行 W_hat 和 P_hat(A)=Φ(W_hat)，满足

    P(A)−ξ≤P_hat(A)≤P(A).                           (18.1)

tie、初始 matching和 N 都由输入固定，使 P_hat 是 profile 的确定函数。每个 integral payoff 由输入 w_jp_jsu 的和组成，取一个公共分母 D_1，其 log位长是输入多项式。t≥1步后的 vertex 权重恰为2(r+1)/(t(t+1))，所以 W分母可取D_1t(t+1)、flow分母可取t(t+1)。gradient、matching comparisons、Φ平方及阈值比较都保持多项式位长；不是每次分母递归相乘。N=O(kH²)，不按任何原分母数值循环。

k≥2分支从全empty helper profile开始，循环如下；k1使用§14.1的不同greedy算法：

1. 求当前 W_hat、P_hat。若每个 W_hat_i≥25/128，转 §19。
2. 枚举每 helper 的每个原 fallback option与 empty，分别重算新 profile 的 P_hat。若存在增加至少τ=1/(2048H)的候选，选最大者、固定索引打破平局，继续。
3. 若无此候选，输出 baseline 全 jobs 调度。

第3步确有 actual V<ε。否则某个 W_hat_i<25/128给 d_hat_i>15/128；由(15.2)、(18.1)，精确 optimum 的 deficit sum>15/128−sqrtξ>9/80，其中sqrtξ≤1/1024<3/640。于是(17.3)有某候选 P增≥ρ/H，新旧近似差≥ρ/H−ξ>τ，矛盾。这里从 actualV≥ε推导共同 O再强制进展，**不是从一个 λ oracle 或必要 relaxation 失败跳到实际不可行**。

每次接受候选使确定的 P_hat 至少增τ，range在[−kc²,θ]，故最多O(kH)次 moves。每轮候选数至多全部原 helper fallback states数加H，每次 O(kH²) 次 matching，所有运算 poly-bit。因此 worst-case 总位复杂度为绝对多项式；actual V低的输入也有同一停止界。FAIL分支 actual OPT>17/16，baseline C≤2的比值小于32/17。

## 19. k≥2 prefix-flow 与两分支的全部原 jobs

k1成功时已有§14.1的integral B allocation、完整叶matching和W≥1/4；它直接进入下面的Good helper回填，**不使用任何prefix或ν损失界**，因为k1允许ν=1。

仅在k≥2分支，成功时每个W_hat_i≥25/128。对fixed helper states定义

    a_iu=max_(j∈J_i) w_jp_j,s_j,u,
    0≤a_iu≤ν,       Σ_u a_iu≤1.

empty helper 不提供 candidate，空 max 取零。聚合同 outer 的 fractional resource claims，并交给该资源上达到 a_iu 的 helper，只增加 W_i；全部 leaf rows 和资源容量保留。对每 outer 按 a_iu 降序列正边 u_1,…,u_m，令 F_l 为前 l 项 fractional claim count，要求整数前缀 count≥floor F_l。

这些要求与所有 leaf exact matching放同一张 lower-bound circulation：outer 用 nested-prefix 链，source→q_m 的 lower为 floor F_m、upper为m；对l=m,…,2，q_l→q_(l−1) 的 lower为 floor F_(l−1)、upper为m；每 q_l→u_l容量一。若m=0则省略该outer链。叶 source→l的 lower=upper一，l→E_l 的资源边容量一；每 resource→sink容量一，sink→source总容量取|B|。其余上述边lower为零。原 fractional flow 见证可行；全部 bounds整数，普通 integral flow 给共同完整叶 matching 和整数 outer claims。

分部求和给每 outer weighted deficit≤最大 a_iu≤ν，因为各前缀只可能比原 count 少不到一。将 outer-owned资源交给其 argmax helper，得到真实 fallback bundles，

    W_i≥25/128−ν≥799/4096>19/100.

两分支共同取q=1/10。Good helpers是chosen-state Q_j≥q者，令其home权重z_i=Σ_(Good∩J_i)w_j。因Q_j≤1，W_i≤z_i+q(1−z_i)。k≥2使用上式W_i>19/100给z_i>q；k1直接用integral W≥1/4给z≥(1/4−1/10)/(9/10)=1/6>q。保留 Good helper 的 B bundle，outer取其 homes；其他 helper各取自己的 home。每叶保留 matching资源，再选提供该 E_l incidence≥ε 的一个原 indexed state。homes互异且与B不交，所以所有原 groups 的质量至少q。

最后选择这些原 states，把 selector放其 private，只输出所取正 incidence jobs，其余全部原 incidences留原 private。未选 fallback payload、unused资源、重复 indexed states、显式零 jobs与全部 extra leaves都已处理；每原 job恰一次、只用原 finite endpoints。C≤2−q=19/10，OPT≥1给相对19/10保证。结合 baseline/FAIL 分支即新域算法。

固定0<γ<1/10时，前文 source-gap 排除的相同比较也适用新域：若所有归约输出都在新域、YES actual OPT≤1、NO actual OPT≥2−γ，则算法以19/10负载阈值区分。因此仅在P≠NP下排除此指定域的实际 source归约，不排一般 normalized-flat source或一般 UM hardness。

## 20. 新冻结来源与有限软件范围

v4新Exact：`boss11_shared_ud_tiny_home_k2_refinement_exact_v4.md`，SHA256 `8948b47cc8b2f303f7f1446ecb0137da163d0b65e906ec4169c5f85294ef877d`。本文是其k1 greedy与k≥2 primal算法的self-contained canonical追加候选，不借用未完成的新独立审查。未发布v3旧Exact `cc9d1037…` 原字节保留，不另建canonical资产。

前身k⁴域Exact：`sol_general_repair_shared_ud_tiny_state_potential_19_10_exact_v1.md`，SHA256 `80fd4ff5b6aab2993e42b995ea369e9441543e754cf3642800c84a784c63cf1d`；其作者Proof：`sol_general_repair_shared_ud_tiny_state_potential_19_10_author_proof_v1.md`，SHA256 `409ce88433cd698d477862098023f7e064dbe7a75426117f3c617e70aad7f435`。原字节和量词域保留。k≥2新k²代数及全部ν依赖的知情作者核查另冻为`sol_general_repair_shared_ud_k2_refinement_informed_audit_v1.md`，SHA256 `ea0ea155880899462b298ff6e9c092ec8201237203bd1dd6684783a03f7084ac`；它是root先给代数后的独立重推，不是fresh Exact-first审票，其中v3的k1-tiny分支不用于本v4。v4的k1 greedy是root指出的标准次模工具直接应用，已在§14.1自足重构；不认领新机制。

作者完整实读及后置自核：`sol_general_repair_shared_ud_tiny_state_potential_author_self_audit_v1.md`，SHA256 `ad50e4e7376ceb50c08e86a75eaa94800f78c9262f8438a130ea89224a0bd9c9`。此是作者自核，不是fresh independent审票；root所报实际读取与最终外部独立状态分别登记。

作者 finite code `sol_general_repair_shared_ud_potential_exchange_small_network_audit_v1.py`，SHA256 `823132666e9442093aec2a2506644d3835e4622b996d4f4da302e391101864ec`；stdout `sol_general_repair_shared_ud_potential_exchange_small_network_audit_run_v1.json`，SHA256 `474aea7b8ce9359ddecf429c455aa807ff375e96fafb5a73ab36820d726c2600`。作者已实际执行并冻结输出：240例直接枚举26674个可行原资源 ownership、242个全部旧 optimal outer-vectors，含160例异质λ和160例same-outer其他helpers，均找到满足(16.1)的一个新 optimum。

这些finite cases只有4/5资源、3helpers分属2outers、1/2叶，不满足本v4的k≥2 tiny域，也不是k1 greedy测试；交换lemma自身不要求tiny，因此仅是该lemma的独立形式有限校准。它没有执行potential/FW/profile搜索、tiny输入、prefix-flow或全部UM jobs，没有完整算法认证；本稿不声称root已读/跑这个新code，也不借用v1 CDF后端的root重放身份。v4新Claim的独立Exact-first、作者读后及最终正文实读尚待root统一补齐；不能用原v1或未发布v2/v3审票代替。

本新域仍不解决一般共享state或nonUD结构；一般UM-TARGET-v1 OPEN。
