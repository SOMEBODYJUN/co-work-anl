# 多个单 state outer 的极小 home 权重取整与 source 边界

本页给指定 normalized-flat 输入类的确定性实际近似。outer 数量可随输入增长，每个 outer 只有一个 state；其 home 权重最多为 1/(4096k⁴)。helpers 可以有任意显式 normalized fallback 菜单，并共享同一个资源池。算法只接收 Q，自己求有理 LP 点，输出完整 ordinary UM 的全部原 jobs。它不解决一般 UM-TARGET-v1。

## 1. 精确身份与状态

正式 ID：**UM-MULTI-OUTER-SINGLE-STATE-TINY-HOME-19-10-APPROX-v1**。本稿只覆盖已冻结 Exact 38c85ffe… / 作者 Proof ce05c7d5… 的原 k⁴-tiny 合同；不使用另一个 k² vector lemma 或更宽输入域。

- **Objects / Domain：** 第2节完整 typed Q 与其所有原 jobs 的普通 P(Q)，任意正整数 k 个 single-state outers，全部正 homes 互异，每 home 恰一个 unit-own helper，fallback 只用与 homes 不交的共享 B。非负二进制有理系数，各 state 总量一，允许零 incidence、重复 indexed fallback states、unused 资源、无 fallback helper。
- **Quantifiers：** 对每个满足 max w≤1/(4096k⁴) 的完整显式 Q，只给 Q，存在同一个固定确定性总位多项式算法输出每个原 job 的合法原机器标签。k、state 数、支持宽度与分母均为输入，不作固定常数或数值循环。
- **Exact Statement：** C_max(σ)≤(19/10)OPT(P(Q))；不提供可行点、OPT、实际 target allocation、精度参数、CONFIG/SDP/调度 oracle。
- **Assumptions：** 标准确定性有理 LP 算法、精确有理算术、有限排序和条件期望。无复杂度假设用于正面算法，无 PSD 或实际 joint state-law 假设。
- **Scope：** 每 outer 恰一个原 indexed state、全 homes 互异和 k⁴-tiny 上界均承重。不推广多 outer states、重合 homes、额外 cores、一般 fallback 之外的未声明资源资格或任意 ordinary UM。
- **Conclusion：** 这是 Q-alone 的实际完整调度算法；第10节仅在这个输入域给 source-gap 排除推论，不声称一般困难性或一般正面算法。
- **Dependencies：** 已有 normalized-flat 实际值桥 OPT=2−V；plain common primitive-SA1 的本页完整显式规格；独立资源 weighted-max 的 elementary CDF 界；标准 rational MW、全方差、Efron–Stein 和条件期望。标准工具不认领新颖性。
- **Evidence：** Exact 与作者证明分离冻结；root 已回报实际全文读完它们及独立 Exact-first 重构、作者读后记录。最终正文的实际实读另见[独立审查](../../reviews/unrelated_machines/multi_outer_single_state_tiny_home_rounding_review.md)，不把后读当新的盲票。root 实际全文读有限 Fraction 后端并在新目录重放，准确范围见第11节；它不认证整个算法。
- **Counterevidence / Objections：** 尚无经已报告内部数学审查成立的 fatal；tiny profile、完整请求 coins、逐资源独立规则、双资源共享 helper state、公共分母及全 jobs 回填均必须保留。有限后端不认证整个算法。
- **Status：** 限定数学算法已先陈述独立重构及作者读后，最终实读与有限软件状态在独立审查中分开登记。无端到端实现、外审或全球新颖性认证；一般 UM-TARGET-v1 OPEN。
- **Related Files：** 本页；冻结 Exact/Proof/有限核的准确身份见第11节；经典全输入目标见[模型](model_and_classical_barriers.md)；完整 normalized-flat 值桥见[现有正文](normalized_weighted_menu_santa_value_and_size.md)。独立审查记录由 root 统一关联，未打开记录不回填为本作者实际已读。

## 2. Typed 输入与全部普通 UM jobs

outer O_i 的唯一 indexed state 正支持为 homes g_j，j∈J_i，系数 w_j>0，Σ_(j∈J_i)w_j=1。全部 (i,j) 的 homes 物理互异。每个 g_j 有一个 helper H_j；其 own state 为该 home 的 unit singleton，其他 fallback states s 为 B 上任意显式 normalized 非负有理向量 p_jsu。B 与 homes 不交；不同 helpers 的 fallback supports 可任意共享。可以没有 fallback；没有其他 groups。给定的零 incidences 保留，但不计入上述正 home 支持。

每个 indexed state 建不同 private machine，每资源建 resource machine。每 group 一个 unit selector，只能去该 group 全部 indexed-state private machines；outer selector 因只有一个 state 而只有一个有限端点。每 listed incidence 是一枚原不可拆 job，private time 为其原系数、exact resource time 为一，其他单元为∞。每 state/resource pair 至多一项。

若 groups、states、listed incidences、resources 数为 G,S,I,U，则完整普通输入有 S+U 台机器、G+I jobs、S+2I finite endpoints。全部未选 fallback payload、全部 selectors 和零 jobs 都必须运行；辅助分配中忽略零值不等于从矩阵删 job。输入显式提供此结构，不要求从一般矩阵识别。

记 ν=max_jw_j≤1/(4096k⁴)，所以 Σ_jw_j=k，Σ_jw_j²≤νk。每个 outer 至少 4096k⁴ 个正 homes；这个巨大但显式的数目是输入域限制，不是免费复制或归一化步骤。

## 3. 实际值桥、固定阈值与可靠 FAIL

对 disjoint resource bundles 定义每 group 值为 max_state Σ_bundle p，V 为最大化所有 groups 最小值。有限输入使 V 达到，0≤V≤1，且

    OPT(P(Q))=2−V,       1≤OPT≤2.                       (3.1)

正向：每组挑 attaining state，selector 放其 private，输出该 state bundle 内正 incidence jobs，其他全部 jobs 留各自 private。选 state load≤1+(1−V)，未选 payload=1，resource 至多一枚 unit job。反向：C<2 时每 resource 至多一枚 unit job，selector 所在 state 的输出质量至少 2−C；只读这些正输出即得 disjoint bundles。OPT=2 的边界由正向式推出 V=0；unit selectors 给 OPT≥1。

算法固定 ε=15/16。为每 state 建原 binary A，为每 listed incidence 建原 binary Z。生成 base rows：state partitions、所有 primitive boxes、gates Z≤A、resource capacities ΣZ≤1、每 state perspective quality ΣpZ≥εA。保留每 row 本身及其乘任意同一原 A/Z primitive 或其补的 row；用一个共同对称二阶数组和 X²=X 表示。等式及其乘子按等式处理。

有 d 个 primitives 时 O(d²) variables、O(d(d+S+U)) rows。boxes 的乘子控制全部 pair；系统有界，标准 rational LP 可在总位多项式内返回 exact rational 点或 infeasible。没有 PSD、unit-FSLP、CONFIG 或 free joint law。

actual V≥ε 的 allocation 直接给合法 binary A,Z 和其真实 products，故该 LP 必可行。若 FAIL，V<15/16，actual OPT>17/16。输出全部 incidence 留 private、selectors 任放合法 state 的完整 baseline，C≤2，从而

    C/OPT<32/17<19/10.                                 (3.2)

以下只处理求得有理可行点的分支。

## 4. Singleton 整化及提取的 packing

记一阶为 E。helper own unit state 的正 incidence 为 Z_0、state 为 A_0。quality (Z_0−εA_0)乘(1−Z_0)给 E(A_0Z_0)≥EA_0；gate乘A_0给反向，gate乘Z_0与box(1−A_0)乘Z_0给 E(A_0Z_0)=EZ_0。于是 EA_0=EZ_0；仅用二阶，没有 triple。

outer 唯一 state 的 EA_i=1。令 x_j 是 outer 在 home g_j 的 claim 一阶；home cap给 x_j+EZ_j0≤1。对 fallback 定义

    α_js=EA_js,  ζ_jsu=EZ_jsu,  f_j=Σ_sα_js=1−EA_j0.

于是每 outer 的 Σ_jw_jf_j≥Σ_jw_jx_j≥ε，且

    0≤ζ_jsu≤α_js,  f_j≤1,
    Σ_up_jsuζ_jsu≥εα_js,
    Σ_(j,s)ζ_jsu≤1                  对每 u∈B.          (4.1)

只对正 fallback incidences 保留 ζ 作后端请求，丢弃零 coefficient claims 只减容量、不减 quality。α=0 时 ζ=0，永不计算0/0。无 fallback 的 f=0 沿原式处理。

## 5. 固定概率空间与精确 weighted CDF oracle

helper j 独立选 fallback s，概率 α_js，或 empty，概率1−f_j。给定 s，各正 incidence u 独立请求，概率 r_jsu=ζ_jsu/α_js。等价地预抽所有 positive-mass state 的各 incidence coins，只读取选中 state；coins 总数显式多项式。

给 λ_i≥0、Σλ_i=1，每资源把实际请求 candidates 按 λ_i(j)w_jp_jsu 降序、固定索引打破平局，交给首个实际请求者。令 Q_j 是其 chosen-state 所获值，W_i=Σ_(j∈J_i)w_jQ_j∈[0,1]，g_i(λ)=EW_i。

对资源分数阈值 z>0，令 a_j(z) 是 helper j 发出分数≥z 请求的概率；它等于对应互斥 states 的 ζ 之和。x=Σa_j≤1，不同 helpers 独立，故

    Pr(max score≥z)=1−Π_j(1−a_j)
      ≥1−exp(−x)≥(1−exp(−1))x≥(5/8)x.

实分析常数只用于证明，算法不算指数；e>1+1+1/2+1/6=8/3。有限阶梯积分及(4.1)给

    λ·g(λ)≥(5/8)Σ_(j,s,u)λ_i(j)w_jp_jsuζ_jsu
             ≥(5/8)ε²=1125/2048=:a.                  (5.1)

精确 oracle 不枚举 profiles。candidate(j,s)在u获胜的概率是

    ζ_jsu Π_(h≠j)(1−Σ_(t先于(j,s))ζ_htu).              (5.2)

同一 helper 只选一个 shared state，其其他 states 不另作独立乘积。将(5.2)乘w_jp_jsu、按outer求和即得有理 g；只用多项式次排序、加乘。

## 6. Floored rational MW 与共同分母

取 η=1/32，N=1024k，初始 b_i=1。第t轮设

    p_i=b_i/Σ_hb_h,      λ_i=(7/8)p_i+1/(8k),
    g^t=g(λ),           b_i←b_i(1−ηg_i^t).

保存全部 N 轮每资源的 orders。λ_i≥1/(8k)，λ_i≤1，所有 b 正。由(5.1)与 uniform average g≤1，

    p·g^t≥(a−1/8)/(7/8)=869/1792.

log(1−x)≥−x−x²（0≤x≤1/2）和 log(1−x)≤−x 分别用于各 b_i 和总 b，比较得

    μ_i:=(1/N)Σ_tg_i^t
      ≥(1/N)Σ_tp^t·g^t−η−log(k)/(ηN)
      ≥757/1792>2/5.                                  (6.1)

最后用log k≤k；包括k=1。

bit成本不能把每轮 oracle 分母当递归新数值无界扩张。固定底层 helper categorical probabilities 和预抽 coins，所有完整 outcomes 共享分母 D_0，可取全部原 categorical/coin 分母乘积；log D_0 为 LP点和输入长度的多项式。w_jp_jsu 的共同分母 D_1 也有多项式 log。所有排序方案下 g_i 都有共同分母 D_0D_1，λ只改变 orders。N轮 b_i 分母可取(32D_0D_1)^N，仍为总位多项式。实际计算用(5.2)，不展开指数样本空间。

## 7. 逐 outer 方差：原 k⁴ 合同

保持 helpers 的独立 profiles，但每资源 u **独立**均匀选 t_u∈[N]，使用保存的对应 order；不得以一个全局 t 替代。线性性给 EW_i=μ_i。

令 X_j 为整个 helper profile（state及全部预抽请求coins），只用于 Efron–Stein 独立块分析。给定 X，定义 d_u=max_actual-requesters w_jp_jsu，empty最大值零。有 d_u≤ν，Σ_ud_u≤Σ_jw_j=k，所以按独立 resource rules，

    Var(W_i | X)≤Σ_ud_u²≤νk.                          (7.1)

令 F_i(X)=E_rules W_i。替换 helper j 的旧/新 profile，固定其他 profiles 与每资源 rule。winner只有旧/新j取胜时可变；如果某outer i被j替换，其分数不大于j，若j属于i，自身项也在同一界中。因此各资源的 i-value 变化至多

    (λ_i(j)/λ_i)w_j
      (p_old·1_oldrequest+p_new·1_newrequest).

每个rule都λ_i(j)/λ_i≤8k，旧/新state请求系数和各≤1，故总 |ΔW_i|≤16kw_j，亦有|ΔF_i|同界。Efron–Stein与Σw²≤νk给

    Var F_i≤(1/2)Σ_j(16kw_j)²≤128νk³.

全方差再跨 i 求和，

    Σ_iVarW_i≤νk²+128νk⁴
               ≤129νk⁴≤129/4096<1/25.                 (7.2)

这是逐 i 的原证明，不使用另一个 vector variance/k² profile lemma。全 helper profile 可有指数支持，但这里只作数学独立块，算法不枚举。

## 8. 真正 polynomial 的平方势条件期望

固定中心 μ_i，定义 Ψ=Σ_i(W_i−μ_i)²。由(7.2)，EΨ<1/25。依次固定所有 helper categorical state/empty、所有请求 coins、最后每个资源的 t_u。每次只选原条件下概率正的分支，取 conditional EΨ 最小者；r=0或1不准选概率零选项。

单步 conditional EΨ 的精确值只需每个 W_i 的一、二阶矩。写 W_i=Σ_uY_iu：一阶枚举单资源 winners，二阶为单资源 winner value平方及两不同资源的 winner-pair product。单资源未固定rule至多N种，两资源至多N²对；不是N^|B|种全局rule。

给定 one/two resources、其rules及winners，每 helper 的 factor 对它的**一个 shared state**求和。若它获胜，必须选指定state并请求；它在两资源都获胜时state必须相同。若其candidate排在该资源winner之前但不赢，必须不请求。条件于同一state，不同资源请求coins独立；已固定coins用0/1，尚未固定用原r。不相容state/coin requirements置零。各helpers独立，乘这些factors。这样可处理同一helper影响两资源；不将其state独立重抽。u=v仅用单winner平方，不造两个赢家。

helper states 总选项、coins数、resource规则数以及每次 one/two-resource枚举均为显式多项式。其运算只含原α,r、0/1、1/N与μ_i。底层公共分母可取D_0N^|B|，payoff平方乘D_1²；正概率partial fixing至多再除其多项式bit的整数numerator，条件矩长度仍多项式。无需 exact SDP 或概率倒数次循环。

每步由全期望保证势不升，固定完毕得到实际请求winner allocation，

    Ψ<1/25,      W_i>μ_i−1/5>1/5  对所有i.            (8.1)

**不得在CE后删除请求币，转为在全部chosen states上取max。** 那只保证某个weighted总值，可能降低个别W_i和破坏平方势。最终winner始终按已固定实际请求者。

## 9. 全组回填和完整 schedule

取q=1/10，称Q_j≥q的helper为Good，z_i=Σ_(j∈Good∩J_i)w_j。因Q_j≤1，

    W_i≤z_i+q(1−z_i),
    z_i>(1/5−1/10)/(9/10)=1/9>q.

保留每个Good helper的fallback winner bundle；empty不可能Good。outer i得到这些Good helpers的homes，值z_i>q；其他每个helper得到自己的home，值一。B与homes不交、homes全局互异、fallback winners原已disjoint，所以所有原groups的值至少q。

按第3节恢复：outer selector固定private，输出其Good homes的原正incidence jobs；Good helper选已固定fallback state、只输出其实际winner bundle；其他helper选own state并输出own unit incidence；所有其余jobs留各自private，尤其全部未选indexed states和显式零jobs。每原job恰运行一次且用原有限端点，C≤2−q=19/10。OPT≥1给C≤(19/10)OPT。结合FAIL分支，完整Q-alone算法成立。

## 10. 限定 source-gap 推论

固定任何0<γ<1/10。若一个NP-hard promise问题有多项式归约，其**所有**输出都是本页typed k⁴-tiny域的完整P(Q)，YES有actual OPT≤1，NO有actual OPT≥2−γ，则本算法多项式区分两端：YES输出C≤19/10，NO任一输出C≥2−γ>19/10，精确比较负载与19/10即可。因此在P≠NP条件下不存在这样的source归约。

γ是源NO gap常数，ν是home最大权重，ε=15/16是算法内部LP阈值，三者不同。该推论只针对全部输出都在本页域的源；不排一般 normalized-flat source、不排一般 UM hardness，也不把restricted selector/promise-NO误当actualOPT-NO。

## 11. 冻结来源与有限软件的准确范围

原 Exact：sol_general_repair_multiouter_single_state_tiny_home_19_10_exact_v1.md，SHA256 38c85ffed433edc9742f2e523ae39c820dc315454262a498ff8386b0b6cc001a。原作者Proof：sol_general_repair_multiouter_single_state_tiny_home_19_10_author_proof_v1.md，SHA256 ce05c7d5fb99d78da44a802578ca33c5ba383b15f6fe0c3a64424ff088c00332。本页提供同一算法的自足正文，原冻结字节不改。

原作者有限核 sol_general_repair_balanced_welfare_pair_backend.py，SHA256 460679c82477934bcfdc3ad326f39dd0d0dd0baf7fa4fd75d02df015c7f6b2f0；stdout sol_general_repair_balanced_welfare_pair_backend_run_v1.json，SHA256 e7433d8476ab2ae99218b4e0307198d0a586311fc84734b16ff3d6efb985c21d。

这只测试3helpers、2outers、每helper2states、2resources、2rules、统一请求率的两个小实例：2048与2916个完整outcomes分别核单/双资源moments和11步state→coin→resource-rule CE；最终势分别565057/26873856、8248921/150994944。第二例某outer最终值0，因其没有tiny profile和本页均值前提，不能把它当本算法反例或全算法check。

它没有生成/求解本页LP、没有N轮MW、没有实例化tiny域、没有全jobs调度、没有核一般方差定理或端到端实现。root 已实际全文读195行原字节代码，并在全新scratch目录执行一次原CLI；stdout与作者冻结JSON逐字相同e7433d…，完整argv/cwd/hash及范围在root replay scope。只这个后端被重放，未声明完整算法已实现。独立数学审查、作者代码、root重跑和外审分别登记，不把互读或有限软件升级成一般认证。

一般UM-TARGET-v1仍OPEN；下一承重问题是更一般共享state选择/非UD结构的确定性共同target生成，不能把本限定profile算法当主目标突破。

## 12. 新的 v4 身份：共享 UD 叶、单 outer greedy 与多 outer k² 势

本节及后续新增节独立于前175行的 v1。前缀 SHA256 为 `84d6031655ac43d9c5726ed2cac6f5241e709743232290e604d767602613778a`，本新增部分不改动它。v1继续是原域上的SA1/CDF/MW/平方势条件期望算法。未发布v2/v3仅为保留历史字节的中间草稿，不另建canonical资产。本v4有两个分支：k1用标准submodular greedy解除tiny上界；k≥2用primal势及新k²曲率。不倒改v1或中间草稿的公式、软件、审查身份；k²不借用另一vector方差lemma。

新 Claim：**UM-MULTI-OUTER-SINGLE-STATE-TINY-HOME-19-10-APPROX-v4**。

- **Objects / Domain：** §13 的完整 typed normalized-flat Q、显式生成的全部 ordinary P(Q) 原 jobs。任意输入变量 k≥1 个 single-state outers、全局互异 homes、unit-own helpers、任意共享 B fallback 菜单；还允许任意多个 B-only exact-threshold-UD leaves。k1只保正权归一化、不额外限制ν；k≥2要求最大home权重ν≤1/(16384k²)。
- **Quantifiers：** 对每个该域完整显式 Q，用同一个固定确定性 worst-case 总位多项式算法输出全部原 jobs 的原有限端点 assignment。helpers 数、leaves 数、states 数、资格度、支持宽度、分母数值与 k 都不作固定常数。
- **Exact Statement：** C_max(σ)≤(19/10)OPT(P(Q))。输入只有 Q，不给 feasible point、OPT、joint law、target profile、精度参数或 scheduling oracle。
- **Assumptions：** 标准确定性完整 matching、min-cost flow、整数 lower-bound circulation 和精确有理算术。k1使用固定helper顺序greedy；k≥2精确profile potential最优点只用于证明，算法用普通matching线性oracle做固定次数rational Frank–Wolfe。不调用exact QP/SDP或指数profile优化oracle。
- **Scope：** 仍须single-state outers、所有homes独占、k≥2的k²-tiny上界、额外叶正支持只在B、以及固定ε=15/16的exact threshold-UD iff；k1没有额外tiny条件。没有覆盖多 outer states、home 重叠、home 上的额外叶、一般 nonUD extra groups 或一般 UM。
- **Conclusion：** 通过真实 target 的反证得到 sound FAIL，或者生成真实正质量 allocation 并输出全部原 jobs。FAIL 不是必要点/某个 λ 线性优化失败的替代名称。
- **Dependencies：** normalized-flat 实际桥 OPT=2−V；transversal dual/vacancy matroid；weighted matroid rank 次模性与 symmetric basis exchange；smooth concave potential、rational Frank–Wolfe；共同 prefix-flow 的整数性。上述标准工具不认领新颖性。
- **Evidence：** v4新Exact `8948b47c…` 单独先行；true_hardness只据三个Exact独立得到149行实际allocation算法 `69036ac6…`，root实际全文读后才释放本primal/FW作者追加稿；其80行实际读后 `4d2d398e…`逐项核本算法，不拿另一算法补跳步。前身k⁴域另有NSW的171行Exact-first `ee7f19b1…`、117行作者读后 `e4ad54e8…`；NSW又实际全文读本204行v4追加稿，冻89行知情扩域审 `d2621c15…`。root实际完整读上述来源、独立票和读后票，亲自核新k²代数，并实际完整读126行finite code、fresh stdout逐字重放。最终规范新节实际阅读范围以[审查](../../reviews/unrelated_machines/shared_ud_tiny_home_potential_rounding_review.md)的冻结记录为准。
- **Counterevidence / Objections：** §16 任意 fractional optimum 的stable coupling、§17 actual benchmark强制进展、§18不用exact potential oracle已被实际读后分别攻击，当前精确域无standing fatal。多state outer、重home和一般nonUD extra groups不属于本Claim；tiny条件不可据有限样本删除。
- **Status：** complete scoped deterministic Q-alone total-bit-polynomial algorithm specification；新Exact-first独立重构及实际作者稿读后已完成，规范稿最终实读另记；只有exchange lemma有限软件，无端到端实现、外审或全球新颖性认证。原v1和未发布v2/v3的身份保留；一般UM-TARGET-v1继续OPEN。
- **Related Files：** 本页既有 §1–11 的 v1；[实际值桥](normalized_weighted_menu_santa_value_and_size.md)；[threshold-UD 判别及条件叶流](normalized_menu_configuration_certificate_preservation.md)；[新审查与保真来源](../../reviews/unrelated_machines/shared_ud_tiny_home_potential_rounding_review.md)。定义身份 UM-MULTI-OUTER-SHARED-UD-TINY-HOME-DOMAIN-v4；精确原矩阵及量词见§13。

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

定义 B 上 vacancy matroid M：X 独立 iff 所有 leaves 能完整匹配到 B\X。它是叶侧已饱和的 transversal matroid 的 dual（原资源侧 rank 等于叶数，不假定等于 |B|）；只需普通 matching 作 independence/rank 查询。其 rank 可以为零，某些资源可以是 loop。

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

v4新Exact：`boss11_shared_ud_tiny_home_k2_refinement_exact_v4.md`，SHA256 `8948b47cc8b2f303f7f1446ecb0137da163d0b65e906ec4169c5f85294ef877d`。本页是其k1 greedy与k≥2 primal算法的self-contained canonical追加；独立重构、实际作者读后、知情扩域审和最后实读各保独立原件，不倒改顺序。未发布v3旧Exact `cc9d1037…` 原字节保留，不另建canonical资产。

前身k⁴域Exact：`sol_general_repair_shared_ud_tiny_state_potential_19_10_exact_v1.md`，SHA256 `80fd4ff5b6aab2993e42b995ea369e9441543e754cf3642800c84a784c63cf1d`；其作者Proof：`sol_general_repair_shared_ud_tiny_state_potential_19_10_author_proof_v1.md`，SHA256 `409ce88433cd698d477862098023f7e064dbe7a75426117f3c617e70aad7f435`。原字节和量词域保留。k≥2新k²代数及全部ν依赖的知情作者核查另冻为`sol_general_repair_shared_ud_k2_refinement_informed_audit_v1.md`，SHA256 `ea0ea155880899462b298ff6e9c092ec8201237203bd1dd6684783a03f7084ac`；它是root先给代数后的独立重推，不是fresh Exact-first审票，其中v3的k1-tiny分支不用于本v4。v4的k1 greedy是root指出的标准次模工具直接应用，已在§14.1自足重构；不认领新机制。

作者完整实读及后置自核：`sol_general_repair_shared_ud_tiny_state_potential_author_self_audit_v1.md`，SHA256 `ad50e4e7376ceb50c08e86a75eaa94800f78c9262f8438a130ea89224a0bd9c9`。此是作者自核，不是fresh independent审票；root所报实际读取与最终外部独立状态分别登记。

作者 finite code `sol_general_repair_shared_ud_potential_exchange_small_network_audit_v1.py`，SHA256 `823132666e9442093aec2a2506644d3835e4622b996d4f4da302e391101864ec`；stdout `sol_general_repair_shared_ud_potential_exchange_small_network_audit_run_v1.json`，SHA256 `474aea7b8ce9359ddecf429c455aa807ff375e96fafb5a73ab36820d726c2600`。作者已实际执行并冻结输出：240例直接枚举26674个可行原资源 ownership、242个全部旧 optimal outer-vectors，含160例异质λ和160例same-outer其他helpers，均找到满足(16.1)的一个新 optimum。

这些finite cases只有4/5资源、3helpers分属2outers、1/2叶，不满足本v4的k≥2 tiny域，也不是k1 greedy测试；交换lemma本身不要求tiny，故只checks该lemma。root实际完整读126行原code，在fresh输出路径执行原CLI，stdout与作者328bytes JSON逐字同 `474aea7b…`；规范[code](../../../tests/audits/unrelated_machines/shared_ud_optimal_exchange_small_network_audit.py)保原字节，实际命令、seed和未检查范围见[scope](../../../evidence/runs/unrelated_machines/shared_ud_optimal_exchange_root_replay_scope.json)。没有运行potential/FW/profile搜索、tiny输入、prefix-flow、k1 greedy或全部UM jobs。数学审者未读跑该程序，不代签软件；v1 CDF后端的root重放身份不升级。

本新域仍不解决一般共享state或nonUD结构；一般UM-TARGET-v1 OPEN。

另一条独立证明保存在[149行Exact-first原件](../../../history/source/notes/unrelated_machines/sol_true_hardness_shared_ud_tiny_home_k2_v4_exact_first_attack.md)：维护真实matroid-independent原incidence allocation，以weighted-rank的“两倍当前福利加单helper增益”不等式和平方缺口势直接作局部改进。它不用本稿FW、最优点stable coupling或最后fractional prefix；其自身后续攻击状态单独记于新审查。标准matroid/greedy/光滑势工具不认领新颖性；当前可复用内容是共享叶和任意fallback下，一个共同actual target强制可计算进展并恢复全部原jobs的组合。没有源问题低负载解码，不能把此限域算法称为UM反证。

## 21. 另立v5：O(1/k)-home与全有理实际分配算法

**ID/version：UM-MULTI-OUTER-SINGLE-STATE-TINY-HOME-19-10-APPROX-v5。** 定义身份 UM-MULTI-OUTER-SHARED-UD-TINY-HOME-DOMAIN-v5。本节起为另一量词域及另一算法；不改前382行v1/v4、其审查或软件身份。

- **Objects / Definitions / Domain：** 完整显式Q及§13的全部原P(Q)。single-state outers、跨全体互异homes、各home一个own-unit helper、任意normalized B-only fallback、任意B-only threshold-UD叶，叶阈值固定ε=15/16，全部indexed/zero/inactive jobs均保留。唯一改动是k≥2放宽为ν=max w_j≤1/(1024k)；k=1仍无额外tiny。每outer的正home权重和一，全部菜单非空。
- **Exact Statement / Quantifiers / Conclusion：** 对该域每个完整Q，一个固定确定性worst-case总位多项式算法输出所有原jobs合法σ，Cmax(σ)≤(19/10)OPT(P(Q))。只输入Q，无OPT、point、joint law、profile、精度或调度oracle。所有k、states、helpers、leaves、支持宽度与二进制分母均为输入参数，次数为绝对常数。
- **Assumptions / Dependencies：** 无复杂度假设；§13实际值桥OPT=2−V；原资源vacancy matroid及普通matching实现；weighted matroid rank次模性；本节自足相对余项与有理局部势。后端不用FW、log、非线性优化或精确SDP。标准工具不认领新颖性。
- **Scope：** 只本typed域；不覆盖多state outer、重home、home上extra groups、一般nonUD叶或任意UM矩阵。新ν不是一般大小处理时间的限制，原fallback系数可大。实际OPT≥1，未把一般OPT0模型删掉，而是另立特殊Claim。
- **Evidence / Status：** 作者先冻29行Exact504e与173行不同profile/log/FW Proof0f5e。NSW只获新Exact，保披露旧v4实际I算法背景，独立冻182行074556全有理实际算法。root实际全文读后才释放作者Proof；NSW实际全文读作者Proof另冻115行437c；原作者又实际全文读本新182行算法另冻77行d93d，均未发现精确域内fatal。root实际全文核两套证明与票；最终规范新增部分的实际阅读以新审查记录为准。完整数学规格；无算法软件、外审或全球新颖性认证。
- **Counterevidence / Objections：** 没有从旧v4 PASS自动扩域。下面同outer损失、跨分段余项、可靠FAIL与所有原jobs均另付；尚无general profile选择或近二source decoder。一般UM-TARGET-v1及反面OPEN。
- **Related Files：** 前述v1/v4；[新审查](../../reviews/unrelated_machines/shared_ud_relative_curvature_rounding_review.md)；保真Exact/两个不同算法及真实读后记录在该审查中。

## 22. 共同叶matching、真实候选和参考比较

沿§13，完整实际OPT=2−V∈[1,2]。取r=18/19、A=r²=324/361、q=19/100、t=1/10、N=helpers数≥1。只需构造全组质量≥t，或可靠证明V≤r后用全原jobs C≤2基线；因为(19/10)(2−18/19)=2，FAIL允许等号。

先检查覆盖全部叶的E_l matching。若无，则实际V<ε<r，直接基线。否则令M为叶侧饱和transversal matroid的dual：D⊆B独立 iff B\D仍匹配全部叶。空叶为free matroid，rank0/loops/unused资源均允许。把全部positive fallback incidence(j,s,u)作为原资源u的平行带标签copies，得到matroid；independence用一次普通matching加资源不重复检查实现。

维护实际independent incidence集I，每helper至多用一个原fallback state。各有fallback者初始化首state，I空；无fallback者空记账，不新增原state。令v_j=Σ_(e∈I_j)p_e∈[0,1]，L_i=Σ_(j∈J_i)w_jv_j∈[0,1]。

给当前任意正权h_i，对每helper j和每个原fallback state s，只在ground I_(−j)并该state所有positive原copies上，用精确有理降序matroid greedy求最大权independent集I'_(j,s)，权为h_i(j)w_jp_jsu。其他helpers只保留/丢旧项；j可换整state。每state固定tie规则只取一个线性最优候选，不调用最大非线性势子问题。旧state候选含I，故δ_j=max_s h·(L'−L)≥0；无fallback时δ_j=0。

完整标签上的weighted matroid rank F是单调次模，I独立给F(I)=h·L。任意参考I*每helper至多一个state：

    F(I∪I*_j)≤F(I_(−j)∪I*_j)+W(I_j)
              ≤W(I)+δ_j+W(I_j)。

次模边际求和及Σ_jW(I_j)=W(I)给

    h·L*≤2h·L+Σ_jδ_j。                                      (22.1)

这里不假设当前I为全ground线性最优。若仅作反证假设V>r，从同一次全组实际allocation保留被outer拿home的helpers的fallback bundles，叶各保留一枚E_l代表，得到同一个M-independent I*，同时每outer L_i*≥V²>A。参考不作算法输入，不按i复制B容量。

## 23. 包含同outer挤出的weighted步长

候选替换j∈J_i时，旧/新j的weighted贡献B_old,B_new均≤h_iw_j。按其他helper所属outer记weighted损失T_l≥0，T=ΣT_l。I_(−j)是候选ground内可行解，故线性最优性给T≤B_new。设s_l=h_l(L_l'−L_l)。非owner坐标为−T_l；owner为B_new−B_old−T_i∈[−B_old,B_new]。因此每一个固定tie最优候选都满足

    max_l|s_l|≤h_iw_j， Σ_l|s_l|≤2h_iw_j，
    Σ_l s_l²≤2(h_iw_j)²。                                  (23.1)

同outer的其他helpers损失T_i已计入。该付款不要求新state线性gain正，也不要求额外optimal-face coupling。

## 24. 全有理分段倒数势及所有跨段余项

以下k≥2。取整数m=ceil√k（整数平方比较求），a=1/(8m)、τ=1/100。k≤m²≤2k，a≤1/16。定义

    φ(x)=(x−q)/a²                        (0≤x≤q)，
    φ(x)=1/a−1/(a+x−q)                   (q≤x≤1)，
    Φ(L)=Σ_iφ(L_i)， h_i=φ'(L_i)=1/d_i²，
    d_i=a+max(L_i−q,0)。

φ在q处C1，凹且单调；值与梯度全为有理式。令D0=349/400，K=D0/(1−D0/8)=2792/2851，则

    h_max=64m²≤128k， d_i≤1−q+a≤D0， νh_max≤1/8。

对任意x,y∈[0,1]，h=φ'(x)、s=h(y−x)，若|s|≤1/8，精确有

    φ(y)≥φ(x)+h(y−x)−K s²。                               (24.1)

两点在倒数段时，置d=a+x−q、Δ=y−x，linear term减实际增量恰为Δ²/[d²(d+Δ)]=s²d/(1+sd)，≤Ks²。由d+Δ=d(1+sd)>0，该倒数式可延至y<q；凹图像不高于q处tangent，而实际φ在q以下恰为tangent，故倒数→线性跨段余项更小。两点在线性段余项零。线性→倒数跨段时整段|φ''|≤2/a³，积分余项≤Δ²/a³=a s²≤K s²。边界x=q由连续性包括；没有冻结沿程gradient的假设。

由(23.1)保证每坐标|s_l|≤νh_max≤1/8，故候选真实势增

    Φ(L')−Φ(L)≥h·(L'−L)−2K h_i²w_j²。                      (24.2)

## 25. 确定性局部算法、进展和可靠FAIL

从I空开始，每轮由真实L算h；枚举上述所有原state候选，直接从各I'重算Φ。若有真实增量>τ/N的候选，按固定输入顺序选一个更新；否则停止。只检查有限线性最优候选，不作指数profile枚举。

停止时对每helper实现δ_j的state候选用(24.2)，得（S=Σh_i）

    Σδ_j≤2KΣ_i h_i²Σ_(j∈J_i)w_j²+τ
          ≤2Kν h_max S+τ≤(K/4)S+τ。                         (25.1)

反证V>r且终点某L_i<q。这个坐标h_i=h_max，故S≥64k≥128。逐坐标Lh≤(q−a)h+√h；倒数段为等式，线性段右侧恰qh。Cauchy给Σ√h_i≤√(kS)≤S/8。由同一个L_i*>A参考，

    h·(L*−2L)≥(A−2q+2a−1/4)S
               ≥(9657/36100)S。

但(22.1)、(25.1)使该量≤(K/4)S+τ。净系数

    9657/36100−698/2851=2334307/102921100>0，
    128·2334307/102921100−1/100=59552417/20584220>0，

矛盾。因此终点任一L_i<q确推出actual V≤18/19；输出同一全jobs基线。L_i=q走成功，包含等号。接受前后势范围[−kq/a²,k/a]宽度≤(808/25)k²，每接受增>1/(100N)，故接受次数<3232k²N；actual V低的输入同样停止。

## 26. k1分支及全部原jobs恢复

k=1用同一实际I候选，直接Φ=L_1、h_1=1，仍接受增>1/(100N)。停止后Σδ_j≤τ；若V>r，(22.1)给L_1≥(A−τ)/2=32039/72200>q。moves<100N；没有ν、a、prefix或二次误差，允许w_j=1。

两分支停止后若全部L_i≥q，令Good={j:v_j≥t=1/10}。其home权重z_i满足L_i≤z_i+t(1−z_i)，故z_i≥1/10。Good保留实际I_j的B bundle并把home给outer，其余helper丢弃B bundle回own。Good union为I子集，仍M-independent，在其补中做完整叶matching并各选一个原attaining state。于是所有groups值≥t，全部homes不同且与B不交。

完整编译和输出同§13：每selector去所选原private，只导出真bundle对应的所选state正incidence，其余全部原jobs留原private，包含所有inactive/zero/duplicate payload。每job恰一次、原finite endpoint合法；resource至多一unit job、selected private≤19/10、inactive private≤1。无额外ordinary job/machine/资格；counts仍S+U、G+I、S+2I。成功C≤19/10≤(19/10)OPT；FAIL V≤r使基线C≤2≤(19/10)OPT。

## 27. 总位复杂度、来源与主目标范围

每轮候选至多原fallback states数，ground≤|I|加该state正支持，|I|≤|B|；每候选为polynomially many matching independence queries。m用整数平方比较取得。所有L每轮从当前原incidence bitset直接重算，系数w_jp_jsu有输入多项式位长的共同分母；a、d_i倒数平方、φ线性/倒数式和Φ的k项求和均poly-bit。下一轮不把旧势分母递归嵌入新原系数；原分母数值不作循环次数。结合显式moves界、矩阵构造和逐job输出，worst-case总位次数是绝对多项式。

本后端没有算法代码或有限实例运行；原v1/v4有限软件不升级。root另用Fraction反算固定常数，有限算术不替代上述全称证明。另一不同的作者profile/log/FW算法，及其完整LP分支/atanh误差和位长证明，原字节保存于新审查链接；本实际后端不靠它补步骤，也不把它冒作已实现软件。新颖性与独立论文价值均未认证。

一个已核的直接保值桥说明删除tiny并不免费：给任意m-group normalized菜单Q，每group添独占unit home和own-state，再添仅要该home的unit outer；旧菜单正是helper fallback。新V恰等于旧V（正值迫所有outer拿home），完整ordinary OPT也精确保留。任意新C<2调度迫outer incidence占home、own incidence留ownprivate、helper selector回旧fallback；限制旧jobs得不增成本调度。C≥2则用旧基线。反向保旧σ并让新机器各负载一。Q新counts为groups2m、statesS+2m、incidencesI+2m、resourcesU+m，finite ends S+2I+6m；ν=1。这是既有值桥的直接构造，不认领一般UM归约或新困难性。

因此当前进展仍是O(1/k)限域算法与精确source边界。固定γ∈(0,.1)，若一NP归约全部输出本域、YES actual OPT≤1、NO actual OPT≥2−γ，则本算法区分，P≠NP下排除此特定源；不排一般normalized菜单或一般UM。真正欠缺的仍是一般输入的共同profile选择/实际低负载解码，或一个可证近二的真实整数困难性归约。UM-TARGET-v1正反面均OPEN。
