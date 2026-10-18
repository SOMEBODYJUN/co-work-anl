# Shared-UD / tiny-state 19/10：独立 Exact-first 重构记录

审者：`/root/sol_nsw_independent_attack`。时间：2026-10-18。状态：本文冻结前没有读取本候选作者 Proof、working note、软件或其他审稿；以下是一条自行重构的完整数学路线，不认证尚未读到的作者算法。本候选数学声称未发现 fatal；下文给出的算法规格足以得到 Exact 的结论。没有端到端软件实现或运行认证。

## 1. 实际读取、先后次序和背景

本轮唯一新增读取的候选本地源是 `/workspace/scratch/038d9dcc4cac/sol_general_repair_shared_ud_tiny_state_potential_19_10_exact_v1.md`，实际全文读第 1–38 行，并在写本记录前再次全文读取；SHA-256 为 `80fd4ff5b6aab2993e42b995ea369e9441543e754cf3642800c84a784c63cf1d`，3867 bytes、38 lines。它只给 typed Q、全部普通 jobs 的 P(Q) 和结论，没有作者势或证明。

我此前已独立审过旧 k^4-tiny / 无额外叶的 Exact、读过旧作者 Proof 和 canonical，也已研究叶压力与 dual-transversal matroid，并写过不同的 given-law 方差/偶矩工具。因此这是有方向背景的新 Exact-first，不是零背景盲审。父 agent 已读本候选作者 Proof，但只告知“可冻结未闭合断点、允许叶为空、请不读作者提示”，未向我给出新机制。本记录中的新路线已先以消息概述给父 agent，随后完整写出；未依赖父 agent 的证明结论。

此前检索过一般 matroid/submodular 文献摘要片段，没有读取或引用一个外部定理来代替本页的承重证明。本页的 matroid 贪心、局部搜索、匹配与有理投影推导均在下文展开。此轮只额外用 Python `Fraction` 核了常数等式；没有读/跑本候选软件，没有构造算法镜像测试。没有读取其他新 Proof/review、repo canonical、Git、Work 或 token。

## 2. 记号和全部 jobs 的精确 value 桥

令 n 为全部 helpers 数，w_j 为其唯一 home 在所属 outer i(j) 中的权，δ=max_j w_j≤1/(4096k^4)。有 Σ_{j∈J_i}w_j=1、Σ_j w_j=k、Σ_j w_j²≤kδ。n>0。取 ε=15/16、T_0=17/16、θ=1/10。每个 fallback state 的 B 上正系数总和为一；own state 在 B 上的价值视为零，但它仍是输入中原来的 indexed own state。

把 Q 的实际 max-min 分配值记为 v：每组选择一个原 indexed state，组之间获得不交的原资源集合，取最小原加性值，再最大化。该最大值在有限集合上取到，且 0≤v≤1。对 Exact 的完整 ordinary P(Q)，有

    OPT(P(Q)) = 2-v ∈ [1,2].                                      (1)

确实，从任一这样的分配，把每组 selector 放在其选定 state private，把该 state 获得的正 incidence jobs 导出到 exact resource，其余全部原 jobs 留 private。资源最多一枚 unit job；选定 private 负载≤2-v，未选 private≤1。反向若实际 makespan C<2，每个 resource 至多一枚原 unit incidence job；每组 selector 所在 private 的未导出 payload≤C-1，因此该原 state 的导出正价值≥2-C。只保这些选定 states 的导出资源，即得不交实际分配。若最优 C=2，正向界与 v≥0 完成等式；OPT≥1 也来自 unit selectors。此论证包含 inactive exports、原零 jobs 和所有原 states，无需删掉这些 jobs 或预设 canonical 输入点。

恒可输出基线：每组 selector 取固定第一个原 state private，全部 incidence jobs 留各自 private，C≤2。若最终可靠证明 v<ε，则 OPT>T_0，该基线满足 2/OPT<32/17<19/10。

## 3. 叶匹配及其剩余供给 matroid

直接由显式有理输入计算 H_l 和 b_l；每叶 b_l<ε 是 typed 域的假设。若某实际分配叶值≥ε，其获得的资源必含 H_l 中至少一个资源，否则其值≤b_l<ε。从各叶不交 bundles 各挑一个这样的资源，得到覆盖全部叶的 H-graph 匹配。反向，任一覆盖叶的 H 匹配，可让叶 l 选择在其匹配资源 u 上 p_lsu≥ε 的原 state，只保这一资源，叶值仍≥ε。该 state 可逐项扫描原菜单找到。

所以 H-graph 没有覆盖全部叶的匹配时，v<ε，直接输出第 2 节全部 jobs 基线即可。这处理了域内确实允许的无完匹配输入，并非把它们剔除。

以下假设存在覆盖全部叶的匹配。令 B 上的 transversal matroid T 的 independent sets 为可注入匹配到不同叶的资源集合，rank(T)=|L|；令 M=T*。对任何 D⊆B，

    D independent in M ⇔ B\D spans T ⇔ B\D 可匹配全部叶。          (2)

这是 dual bases extension：D independent in M 等价于可扩充为某个 M basis，其补是 T basis；反向补中有一个 T basis 即可。所有 |L|=0、rank(M)=0、unused resources、loops/coloops 都包括在 (2) 内。算法不会调用指数 matroid 配置 oracle；下面每次精确加权优化都直接化成一次 mincost 全叶匹配。

## 4. 固定 profile 的可计算福利与 submodularity

每 helper 的一个 option 是其一个原 fallback indexed state，或其原 own state 的 null 记号（零 B 价值）。profile S 恰为每 helper 选一个这样的原 option。对 α∈Δ_k，定义 f_α(S) 为在 B 上给 helpers 分配资源、且剩余资源能匹配全部叶时的最大 Σ_j α_i(j) w_j q_j，其中 q_j 是该 helper 在 S_j 下得到的原加性 B 值。

令 c_u=max_j α_i(j)w_j p_{j,S_j,u}，null 的 p=0。则

    f_α(S)=Σ_{u∈B}c_u - min_{全叶匹配 N} Σ_{u∈N}c_u。            (3)

给匹配外每枚正 c_u 资源一个达到最大值的 helper，即达此值。(2) 和非负权的 basis extension 证明最优性。用固定顺序打破所有 ties，(3) 可确定性精确计算；产生的 g_i=Σ_{j∈J_i}w_j q_j 是 α 的 subgradient。每 helper 只用一个 normalized state，所以 0≤g_i≤1；对 α∈Δ，有 0≤f_α(S)≤1。

为证明 combinatorial inequalities，可暂把 options 看作集合 A（允许同一 helper 多个 options 同时出现在这个辅助集合里）。给每个正 incidence (j,s,u) 一枚权 α_i(j)w_jp_jsu 的 u-parallel copy；每个 u 再放一枚零权 dummy。copies 的 matroid 要求原资源互异且原资源集在 M 中 independent。f_α(A) 就是选中 options 的全部 copies 加零 dummies 的 weighted matroid rank。

固定 α 时 f_α 是 normalized、monotone、submodular 的 set function。一个直接证明是 weighted rank 等于对 t≥0 积分的 rank({weight≥t})；每个 threshold 上 matroid rank 对 copy 集合 submodular，selected-option copy blocks 的 union/intersection 保持所需 inequality。零 dummies 对函数值为零，故 f_α(∅)=0。辅助的多-option 集合只用于证明，不被当作输入实际 state choice。

## 5. 加入一个 state 的 marginal 对 α 的 Lipschitz 界

令 K={α∈Δ_k:α_i≥β=1/(8k)}，并令 a=(j,s) 是一个 normalized fallback option。对于固定 option 集 A，

    h_a(α)=f_α(A∪{a})-f_α(A)
    是 L_j=(1+8k)w_j 的 Euclidean-Lipschitz 函数（α∈K）。        (4)

这里不用把 matroid 最优项的导数稳定性当成免费事实。固定 α，在 old copies 与零 dummies 中取一个最大权 greedy basis C。对每个正 threshold t，C 中权≥t 的元素 span 所有 old 权≥t 的元素。加上 new state 中权≥t 的 copies 后，两边 span 的 rank 仍相同；积分 threshold ranks，得到在 C∪new copies 上的最大权 basis 已与全部 old+new copies 的最优值相同。

故新最优 basis C' 可取在 C∪new 中，旧保留项是 C 的子集。全部新 copies 都来自单个 normalized state，所以其未乘 α 的总贡献≤w_j，其 α 加权贡献≤α_i(j)w_j≤w_j。最优值不下降，意味着丢弃的旧 copies 的加权总价≤新贡献≤w_j。由于 α_l≥β，丢弃旧 copies 的未乘 α 总贡献≤w_j/β。因此在一个固定 greedy 次序区间上，h_a 的梯度 l1 范数≤w_j+w_j/β=L_j，Euclidean 范数也≤L_j。

价格比较只给有限个有理超平面。沿任一 K 中线段分段用上述界并用函数连续性处理 ties，得到全局 (4)。全线段落在 ties 上时可取相对内点线段极限；不需要随机 perturbation。null option 的 marginal 恒零，仍满足同一个界。

若 profile S' 只把 helper j 的 option 换掉，对共同的 S\{j} 使用两次 (4)，则 f_α(S')-f_α(S) 是 2L_j-Lipschitz。

## 6. 势值可由有理位多项式算法近似

取 λ=1/8，定义

    J_S(α)=f_α(S)+(λ/2)||α||²，    V(S)=min_{α∈K}J_S(α)。          (5)

J_S 是 λ-strongly convex，最小点 α_S 唯一；不需精确求这个最小点或假设 nonlinear optimization oracle。取 e=1/(8192n)，h=e/(4k)，H=ceil(8k/e²)。从 uniform α 开始做 H 次精确有理 projected subgradient：

    α^(t+1)=Proj_K[α^(t)-h(g^(t)+λα^(t))]。

每一步用 (3) 求 g。K 投影可把 β 从每坐标减去，再对质量 7/8 的非负 simplex 用排序/水位阈值精确完成。||g+λα||²≤4k，diam(K)²≤2。标准投影平方距离 telescoping 给

    min_t J_S(α^(t))-V(S) ≤ 1/(hH)+2hk ≤ e。                   (6)

这里也可直接把凸 subgradient inequality 代入平方距离递推来证明 (6)。保留 H 个实际有理 J 值中最小者作为 Vhat(S)，便有 V(S)≤Vhat(S)≤V(S)+e。

这确实是总位多项式而非只 arithmetic polynomial：所有 g_i 是原 w_jp_jsu 的子和，可取一个 bitlength O(input) 的共同原分母。每次更新及 simplex 投影只给当前坐标共同分母乘原共同分母、固定 h/λ/β 分母和一个≤k 的整数；每轮增加的 bitlength 为 polynomial(input)。H=O(kn²)，故迭代坐标及平方 objective 的 bitlength 仍 polynomial(input)。不同 profile 计算重启 uniform，不把先前 Vhat 的大分母反复嵌套。matching/mincostflow、比较和投影都为确定性有理计算。

## 7. 可终止 profile 局部搜索及其固定 α 保证

从所有 helper 选 own/null 的原 profile 开始。每轮计算当前 Vhat，并扫描全部单 helper 原 option swaps。若某个 S' 的 Vhat(S')-Vhat(S)≥2e，按固定次序取第一个并继续；否则终止。

每次接受的真 V 增长≥e。由 0≤V≤1+λ/2=17/16，接受次数≤8704n。每轮候选数不超过输入原 helper states 数，(6) 每次固定多项式计算；故此局部搜索是 worst-case 总位多项式，未枚举全部 profiles。

停止时每个单 helper j swap 有 V(S')-V(S)<3e。由强凸性以及 swap 的 2L_j-Lipschitz 性，对 d=||α-α_S||，

    J_S'(α) ≥ V(S)+[f_{α_S}(S')-f_{α_S}(S)] +(λ/2)d²-2L_jd。

最小化右边的一元二次式可得

    f_{α_S}(S')-f_{α_S}(S) ≤ 3e+2L_j²/λ =3e+16L_j²。           (7)

对任意 target profile S*，在同一固定 α=α_S 下使用第 4 节 submodularity：

    f_α(S*)≤ f_α(S)+Σ_j [f_α(S∪{S*_j})-f_α(S)]
             ≤2f_α(S)+Σ_j [f_α(S-{S_j}+{S*_j})-f_α(S)]。

第二步是每个 added marginal≤相应 swap gain+删除当前 option 的 loss，而全部 deletion losses 的和≤f_α(S)。相同 option 或 null、重复 indexed states 都遵守此 inequality。于是终止 profile 满足

    f_{α_S}(S*) ≤2f_{α_S}(S)+3ne+16Σ_jL_j²。                  (8)

## 8. 实际高质量解仅作分析 comparator，不是算法输入/oracle

假设（仅供以下 implication 分析）v≥ε，即实际 OPT≤T_0。取达到此实际值的 allocation；把叶各自换成其原 bundle 内的一枚 H 资源及达到≥ε 的原 state。它们仍不交，且不侵占 helpers 的原 fallback bundles。

每 outer 的实际 home 正权总和≥ε。每个给 outer 贡献 home 的 helper 因失去唯一 own 正资源，必选择一个 fallback state，并在 B 上得到值≥ε。取实际 helper fallback states 或 own/null 构成 S*，其 B bundles 避开全部叶匹配。因此每个 outer 的 helper 加权 fallback 总值≥ε²，故对所有 α∈Δ，

    f_α(S*)≥ε²。                                               (9)

算法从来不获得、寻找或查询这份实际 allocation / S*。它只在证明“若真实高质量，则计算出的 profile 后端不会 FAIL”时充当任意比较对象；未把 unknown integral benchmark 当成可计算 oracle。

对 k≥2，由 Σw_j²≤kδ，

    8Σ_j L_j² ≤ (1+8k)²/(512k³) ≤289/4096。

末式在 k=2 达到最大，上式展开为 (64/k+16/k²+1/k³)/512 即可逐项单调验证。由 (8)(9)，并把 3ne/2=3/16384 放宽至 1/2048，

    f_{α_S}(S)≥225/512-1/2048-289/4096=1509/4096。

对任意 α∈K，由 J_S(α)≥V(S)=f_{α_S}(S)+(λ/2)||α_S||²，且 ||α||²≤1，得到 f_α(S)≥1509/4096-1/16=1253/4096。

对任意 α∈Δ，取 α'=(7/8)α+(1/8)uniform∈K。support function 的凸性和 f_uniform(S)≤1 给 f_α'(S)≤(7/8)f_α(S)+1/8，因此

    min_{α∈Δ} f_α(S)≥(8/7)(1253/4096-1/8)
                       =741/3584>1/5， margin=121/17920。       (10)

k=1 时 K={1}，regularizer 是 profile-independent 常数，停止时直接有每个 f swap gain<3e，无需 Lipschitz penalty；submodular 比较给 f_1(S)≥ε²/2-3ne/2>1/5。因此 (10) 所需的严格 1/5 下界对全部 k≥1 成立。

## 9. 最终显式 LP、可靠 FAIL 和同一匹配取整

对终止 profile，令 c_iu=max_{j∈J_i} w_jp_{j,S_j,u}，仍有 0≤c_iu≤δ。解以下普通 polynomial-size rational LP（不是配置 oracle）：

    x_iu≥0, y_lu≥0 (u∈H_l)，
    Σ_i x_iu+Σ_{l:u∈H_l}y_lu≤1  (每 u∈B)，
    Σ_{u∈H_l}y_lu=1             (每叶 l)，
    Σ_u c_iu x_iu≥1/5           (每 outer i)。                  (11)

在 (11) 前三组行所给的 compact polytope 上，max-min utility 的值等于 min_{α∈Δ} f_α(S)：固定 α 的最大化正是 (3) 的 bipartite matching/flow，LP strong duality 或 finite-dimensional minimax 给该等式。因此 (10) 证明：若 v≥ε，则 (11) 可行。若算法得到 (11) 不可行，它可靠推出 v<ε，走全部 jobs 基线；没有声称一个弱 LP feasible certificate 自动是实际解。

(11) 可行时，对每 i 把 x_iu 按 c_iu 非增排列，依次放入长度一的 utility slots。仅保 floor(t_i) 个满 slots，t_i=Σ_u x_iu，丢弃末尾不足一的 slot。构造一个真正共同的 bipartite matching：左侧为全部这些满 slots 加全部原叶，右侧为 B；slot 连其收到正 x fraction 的资源，叶连 H_l。x 的 slot 分解和 y 共同给覆盖所有左节点的 fractional matching，资源列总容量≤1，所以 Hall 或流的整数性给覆盖全部左节点的 integral matching。

这个步骤不是“各 outer 分别匹配再拼”，叶和所有 slots 都在同一个匹配中，故保证全局 disjoint。slot 总数≤|B|；每 x_iu≤1，因而一枚这样的 fraction 最多跨两个 slots，构图 polynomial。

按排序得到的阶梯函数 a_i(t)，fractional utility 是 ∫_0^{t_i}a_i(t)dt。slot h 中匹配到的资源值至少该 slot 的最小值 a_i(h^-)，而 a_i 非增，∫_0^{t_i}a_i≤max_u c_iu+Σ_{h≤floor(t_i)}a_i(h^-)。于是每 outer 实际 slot utility≥1/5-δ。对每个正 c 的匹配资源，给一个达到 c_iu 的 helper j（该 helper 的 profile state 已固定）；零 c 资源可留空。叶使用自己的匹配资源和第 3 节找到的原 state。这样得真实 helper fallback 值 q_j∈[0,1]，且

    W_i=Σ_{j∈J_i}w_jq_j≥1/5-δ≥1/5-1/4096>19/100。             (12)

令 Good={j:q_j≥θ}，r_i=Σ_{j∈J_i∩Good}w_j。由 W_i≤θ+(1-θ)r_i 以及 19/100=θ+(1-θ)θ，得到 r_i>θ。保留 Good helpers 的 B bundles；把其 homes 给其 outer。其余 helper 收回 own home，丢弃原 B bundle。全部叶保留其匹配 B 资源。所有资源仍全局不交，outer 值>θ，Good helper 值≥θ，其他 helper 值一，叶值≥ε，故实际 min-value≥θ。

## 10. 原 job 恢复、所有边界和 19/10 比值

成功分支显式按原 indexed identities 输出全部 jobs：outer selector 去其唯一原 state private，Good helper selector 去 profile 的原 fallback private，其余 helper selector 去原 own private，叶 selector 去达到其 H 匹配资源 ≥ε 的原 state private。仅导出上述选定 states 真分配到的正 incidence jobs；全部其他原 incidence jobs，包括每个显式零 job、所有 inactive states 的正 payload、没有选中的重复 indexed state payload，均留其原 private。

每个原 resource 最多一枚 unit job；每个 selected root 有 selector 一加 payload 至多 1-θ，故负载≤19/10；叶 selected root 更有负载≤17/16；所有 inactive private≤1。零 job private time 为零，无资格改写。没有“只排 selected subproblem”、删除 inactive exports 的输入假设或追加 guard。生成的 S+U machines、G+I jobs、S+2I finite endpoints 与 Exact 一致，输出只用原有限端点。

成功分支 C≤19/10，结合 OPT≥1 得所需 ratio；无叶匹配或 (11) 可靠 FAIL 分支 C≤2，结合 OPT>T_0 得更小的 32/17 比值。算法不需猜 OPT 或求实际 v。

叶数为零时 M 是 free matroid，路线照行；B 为空、无 fallback、rank(M)=0 时允许 (11) FAIL，不能据此错误要求存在资源。每个 helper 仍有原 own state；每个 outer 正 weights 总和一保证 n>0。未用叶 graph 资格度界、leaf state 必为 singleton、fallback tiny 或 unique helper-state support。unused resources、原零资格到 homes/B 任意处、helper/state duplicate indices 均按原输入保留。叶的非空 indexed menu 由 b_l=max_s 的定义所需；若空菜单本身未定义 b_l，就不构成这里声称的 normalized typed 输入。

## 11. 计算范围和结论

逐叶判别、生成全 P、H matching、profile 的 (3) mincost matching、投影势估计、至多 8704n 次 profile 更新、最终 rational LP、utility-slot 全局匹配及逐 job 输出，全为固定绝对次数的 input-bit polynomial。原 rational denominators 的数值不进入迭代上界。强凸 minimum 只按 (6) 近似到固定派生精度 e，不假设 exact SDP 或 precision oracle；单次加权匹配精确，所有比较和 acceptance 固定有理阈值。本路线没有随机采样、期望匹配求值、Las Vegas、全 joint profile 枚举或给定 feasible point。

独立判断：按第 2–10 节自足路线，Exact 的指定 typed Q-alone deterministic 19/10 声称可重构，未发现 fatal。此票只认证 Exact 结论可由上述数学规格实现；尚未读作者的新算法，不能借此为作者未读证明背书。原 k^4-tiny 算法、我自己的 k²/偶矩 given-law lemmas、一般 normalized Q、一般 UM 和任意多state outers 均没有因本记录而升级。

本轮软件范围仅 `Fraction` 常数核算；匹配/LP/势搜索/全 jobs 后端未实现或运行。全球新颖性未认证。下一步须先由父 agent 实际阅读全文，再按其释放范围读作者 Proof 并另冻 read-after；不改本 Exact-first 字节。
