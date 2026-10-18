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
