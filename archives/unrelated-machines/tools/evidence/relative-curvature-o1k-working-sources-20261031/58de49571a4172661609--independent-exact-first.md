# O(1/k) homes：独立 Exact-first 重构与攻击记录

审者：`/root/sol_nsw_independent_attack`，2026-10-18。结论：从只给出的新 working Exact，结合已经公开给我的 v4 / actual-bundle 背景，可独立重构一条覆盖其完整量词的确定性总位多项式 19/10 算法；未发现 fatal。本页完整给出新的有理分段倒数势及相对余项，不以旧 v4 的 PASS 自动扩域。没有读取本 working 候选的作者 Proof/机制，算法无软件实现认证，全球新颖性未认证。

## 1. 真实读取、先后次序和背景披露

本轮唯一新增本地源是 `/workspace/scratch/038d9dcc4cac/sol_general_repair_relative_curvature_O1k_working_exact_v1.md`。实际全文读第 1–29 行，SHA-256 `504e4d8e13b847aa7ec10f2bb3afa874389a76b6cc0962abfe979a985238a99f`，3007 bytes、29 lines。没有打开任何 O1k Proof、新 general 稿、根讨论、其他审者记录、代码或运行产物，也没有向其他 agent 索取机制。

已知背景须明说：我先审旧 k⁴ Exact，冻 `ee7f19b…`；父 agent 实际读后释放其作者 Proof，我冻 `e4ad54e…`；随后读 k²/k1 v4b 作者追加稿并冻 `d2621c15…`；再实际读 `sol_true_hardness_shared_ud_tiny_home_k2_v4_exact_first_attack.md` 的 149 行新 actual-allocation 算法，冻后置审票 `d55514ae36989bf3990bd0294bb31498731d267f32dffca8599de1fe764629a4`。父 agent 实读 d555 后才给我本次 504e Exact。本轮不是声称对所有方向零背景 blind。

本页的实际 I 单 helper 候选和 weighted-rank 比较沿用上述已读数学背景，但新 O(1/k) 势、全部相对余项及常数在本轮自己推得；在写本记录前已先向父 agent 消息报告公式，没有收到作者 O1k 提示。原先各 frozen 记录均不改字节；不把它们的审查范围追溯扩大。只写 scratch，没有 Git/Work/token 操作。软件范围仅另用 Python Fraction 核本页常数，未实现算法。

## 2. 完整对象、实际值桥和可靠基线

严格按 504e 的 typed Q：k≥1 个 single-state outers，home 权 w_j>0、每 outer Σ_{j∈J_i}w_j=1，全部 homes g_j 全局不同，每 home 唯一 own-unit helper；其他 helper states 任意显式 normalized B-only fallback，B 与 homes 不交。所有额外 leaves 正支持只在 B，在 ε=15/16 有整菜单阈值资格 E_l 和 b_l<ε；所有 menus 非空。k1 无额外 tiny，k≥2 为 ν=max w_j≤1/(1024k)。全部原 zero incidences、重复 indexed states、unused resources 保留。N=helpers 数≥1，Σ_jw_j=k。

令 V 为每组取一个原 state、各取不交资源 bundle 后的最大最小原加性值。0≤V≤1，并对 Exact 完整 ordinary P(Q) 有

    OPT(P(Q))=2−V ∈[1,2]。                              (1)

正向 selector 放所选 state private，所取正 incidences 导出 exact resource，其他全部原 jobs 留 private，得到 C≤2−V。反向 C<2 时每 resource 至多一枚 unit incidence job，selector 所在 state 的导出正价值≥2−C；只取这些 state 的导出 bundles，资源仍不交。C≥2 时 C≥2−V 平凡，合并得 (1)。它不要求给定 ordinary schedule 没有 inactive exports，也没有删原 zero jobs。

取 r=18/19、A=r²=324/361、q=19/100、t=1/10。只需两个分支：真构造全部 groups 值≥t，则全 jobs C≤19/10；或者证明 V≤r，则所有 incidence 留原 private、每组 selector 任取一原 private 的 C≤2 基线满足

    2≤(19/10)(2−V)，  因 (19/10)(2−18/19)=2。             (2)

所以可靠 FAIL 允许 V 等号，无严格 gap 假设。算法没有输入或调用 V、OPT、其见证、给定 feasible point 或精度 oracle。

## 3. 共享叶 matroid、实际 bundles 和可计算候选

先直接算 E_l、b_l，检查覆盖全部 leaves 的 matching。若不存在，则任何实际 V≥ε allocation 都会让每叶拿到一个 E_l 资源（否则其任一 state 的整个尾巴值<ε）；其资源不交会给一个 full matching，矛盾。因此实际 V<ε<r，走 (2) 基线。这真正处理无完整叶匹配输入，不把它排出域。

有 full matching 时，令 B 上 resource-side transversal matroid T 的 independent sets 为可注入匹配到不同叶的资源集，rank(T)=叶数；M=T*。D independent in M iff B\D 可匹配全部叶：D 可扩为 dual basis，当且仅当其补含一个 T basis。用普通 matching 可检测 independent；空叶得 free matroid，rank0、loops/coloops、unused resources 都允许。

完整 positive fallback 标签 e=(j,s,u) 为 M 的 parallel copies；independent 即 underlying resources 不重复且在 M independent。维护实际独立 incidence 集 I，每 helper 至多用一原 fallback state s_j；有 fallback 者初始化任取第一原 state，I=∅；无 fallback 者记空，I_j 永远为空。记

    v_j=Σ_{e∈I_j}p_e ∈[0,1]， L_i=Σ_{j∈J_i}w_jv_j ∈[0,1]。

固定当前正权 h_i，对每 helper j 和每个原 fallback state s，只在 ground I_{−j} ∪ {(j,s,u):p_jsu>0} 上求权 h_i(j)w_jp_jsu 的最大权独立集 I'_{j,s}。这是 matroid greedy：精确有理排序，每步用上述全叶 matching 检查。只有 j 得新 incidence，其他 helpers 只保留/丢旧项。旧 state 的候选包含当前 I，所以

    δ_j=max_s[Σ_i h_iL_i(I'_{j,s})−Σ_i h_iL_i(I)]≥0。

无 fallback j 定义 δ_j=0。算法每 state 只取固定 tie 规则给的一个 linear optimum，不求 nonlinear optimum、不枚举该 state 的全部 subsets 或全部 joint profiles。所有 states 和 ground 都完整显式。

## 4. 共同参考与两份当前福利的精确比较

完整标签 ground 上 weighted matroid rank F(S)=max_{K⊆S independent}Σ_{e∈K}h_i(j)w_jp_e 单调次模；按降序权 threshold ranks 的非负组合可直接证明。I independent 给 F(I)=W(I):=Σ_i h_iL_i。对任意真实可行的参考 I*（每 helper 至多一个 fallback state、允许空），

    F(I∪I_j*)≤F(I_{−j}∪I_j*)+W(I_j)
              ≤W(I)+δ_j+W(I_j)。

第一步是加入 I_j 的 rank 增量至多其全部原权；第二步是原 state 候选含 I_j*，空参考时直接用 δ_j≥0；无 fallback helper 的两者都空。单调次模边际求和给

    Σ_i h_iL_i* =F(I*)≤F(I∪I*)≤2W(I)+Σ_jδ_j。           (3)

此处不假设当前 I 在全 ground 线性最优，不需要任何 λ-optimal fractional 点或其 coupling。含同 helper 多 states 的辅助 F 集合只作数学 rank 上界，实际 I、I* 各自仍一 state。

若仅作反证假设 V>r，取达到 V 的一次全部 groups 实际 allocation。outer i 拿的正 home 权≥V；每个失去 home 的 helper 不能靠其 own-unit state 得正值，必有一个原 fallback B bundle 值≥V。只保留这些 bundles；每叶从原 bundle 选一枚 E_l 资源，其与保留 helper bundles 不交，所以参考 I* 在 M independent，且对全部 i 同时有

    L_i*≥V²>A。                                        (4)

I* 从同一次实际 allocation 得到，不为不同 outer 复用 B；只在 (3) 的分析中出现，算法未获得或求它。去掉原零贡献资源不改变其价值或独立性。

## 5. 每个候选的 weighted L∞/L1：包含 same-outer 丢失

对当前正 h，候选 j 属 outer i。令旧 j weighted value 为 B_old≤h_iw_j，新 j weighted value 为 B_new≤h_iw_j；其他 helpers 的 weighted losses T_l≥0，按所属 outer l 聚合，总 T=Σ_lT_l。I_{−j} 是候选 ground 内可行集，所以任何 linear-optimal 候选满足

    T≤B_new。

令 s_l=h_l(L_l'−L_l)。非 owner l 的 s_l=−T_l；owner 的 s_i=B_new−B_old−T_i。因 T_i≤T≤B_new，owner 坐标在 [−B_old,B_new]，故对每个候选

    max_l |s_l|≤h_iw_j，
    Σ_l|s_l|≤|B_new−B_old|+T≤2h_iw_j，
    Σ_l s_l²≤2(h_iw_j)²。                              (5)

这个 owner bound 明确包含同 outer 其他 helpers 的损失，未把 j 当成独占 outer。即使新 state 的 total linear gain 负、或存在多个同权 optima，(5) 仍成立。它比此前 absolute-coordinate 的 (h_i/b)² 付款强，以下只用 weighted coordinates，不能再把 λ_min 的平方免费丢掉。

## 6. 新的全有理分段倒数势

以下仅用于 k≥2。取整数 m=ceil(sqrt(k))，a=1/(8m)，τ=1/100。m 用整数平方比较求得，不调用 transcendental oracle。对整数 k≥2 有

    k≤m²≤2k，  a≤1/16。

上界可用 k≥(m−1)²+1、m²≤2[(m−1)²+1]（差为 (m−2)²）直接验证。

定义 C1、单调、凹的有理分段函数（q=19/100）

    φ(x)=(x−q)/a²                       (0≤x≤q)，
    φ(x)=1/a−1/(a+x−q)                  (q≤x≤1)，
    Φ(L)=Σ_iφ(L_i)， h_i=φ'(L_i)=1/d_i²，
    d_i=a+max(L_i−q,0)。

两分支在 q 的值同为零、导数同为 1/a²。不是 log 势；值和梯度均只需精确有理运算。

    h_max=1/a²=64m²≤128k，
    d_i≤1−q+a≤349/400=:D_0，
    νh_max≤1/8。                                       (6)

任一候选由 (5) 得 |s_l|≤νh_max≤1/8。下节相对余项只对这种真实允许步长使用，不要求全局固定常数 Euclidean smoothness。

## 7. 分段边界也成立的相对二次余项

对任意 x,y∈[0,1]，h=φ'(x)、s=h(y−x)，若 |s|≤1/8，则

    φ(y)≥φ(x)+h(y−x)−K s²，
    K=D_0/(1−D_0/8)=2792/2851。                        (7)

逐情况验证如下。若 x≥q、y≥q，置 d=a+x−q，Δ=y−x。倒数精确恒等式给 linear term 减实际增量为

    Δ²/[d²(d+Δ)] = s²·d/(1+s d)。

因 d≤D_0、|s|≤1/8，分母≥1−D_0/8>0，系数≤K。若 x≥q、y<q，同样界保证 d+Δ=d(1+s d)>0；在 y 处把倒数公式延伸到 q 以下，其凹图像不高于 q 点的 tangent line。实际 φ(y) 恰是该 tangent line，所以实际 remainder 只会更小，(7) 仍成立。

若 x≤q、y≤q，两者都在同一线性段，remainder 为零。若 x<q<y，在整段上二阶导数绝对值≤2/a³（到 q 前为零），积分 Taylor remainder≤Δ²/a³=a(hΔ)²≤K s²，因为 a≤D_0<K。x=q 的边界由两侧公式或连续性直接包括。由此没有遗漏“跨 cap”而使新 gradient 暴涨的步。

对实际候选逐坐标用 (7) 与 (5)，得到真正可计算势的增量

    Φ(L')−Φ(L)≥[W(I')−W(I)]−2K h_i²w_j²。              (8)

注意系数是 weighted change，不是旧 Euclidean 曲率把 h_min 项漏掉。整个新 O(1/k) 付款就在 (5)–(8) 的额外推导中。

## 8. 确定性算法、停止不等式与新 O(1/k) 付款

从第 3 节 I=∅ 开始。每轮用当前实际 L 计算 h；依次枚举每个原 helper fallback state，在其 candidate ground 上做上述 weighted greedy，直接从所得 I' 重算真实 Φ。若存在 Φ(L')−Φ(L)>τ/N，按固定原输入顺序取第一个，更新 I 和 j 的原 state；否则停止。每次只算一个线性最优候选的 Φ，不把最大 Φ 的子问题当 oracle。

停止时对达到 δ_j 的 state 的固定候选用 (8)，求和可得

    Σ_jδ_j≤2KΣ_i h_i²Σ_{j∈J_i}w_j²+τ
           ≤2KνΣ_i h_i²+τ
           ≤2Kνh_max Σ_i h_i+τ
           ≤(K/4)S+τ，  S=Σ_i h_i。                    (9)

无 fallback helpers 的 δ=0，统一多付其 τ/N 仍合法。关键只用新 ν≤1/(1024k)，没有旧 k²/k⁴ 条件。

假设反证真实 V>r 且终点某 L_i<q。这个坐标 h_i=h_max=64m²，故 S≥64k。并且对每个 L∈[0,1] 都有

    Lh≤(q−a)h+sqrt(h)。

在倒数段是等式，因为 d=1/sqrt(h)、L=q−a+d；在线性段 h=1/a²、L≤q，右边恰 qh。Cauchy–Schwarz 给 Σsqrt(h_i)≤sqrt(kS)≤S/8。因此借 (4)

    Σ_i h_i(L_i*−2L_i)
       ≥[A−2q+2a−1/4]S
       ≥(9657/36100)S。                                (10)

另一方面 (3)(9) 使同一量≤(K/4)S+τ，K/4=698/2851。净系数为

    9657/36100−698/2851=2334307/102921100>0。

因为 S≥64k≥128，净余量减 τ 至少

    128·2334307/102921100−1/100
      =59552417/20584220>0，                            (11)

矛盾。故真实 V>r 时终点必全 L_i≥q。实际算法只需检查此显式条件；某 L_i<q 则可靠得 V≤r，执行 (2) 基线。L_i=q 走成功，没有严格 gap 或精度判定问题。虽然证明余量还更强，本记录不擅自改变 Exact 的域或目标。

## 9. 终止和 k1 完全无 tiny

k≥2 的 Φ range 为 [−kq/a²,k/a]。由 m²≤2k、m≤k，区间宽度≤(128q+8)k²=(808/25)k²。每接受一步真 Φ 增>1/(100N)，所以接受次数<3232k²N；即使实际 V 很低，也同样终止。这是固定次数 polynomial 改善，不是有限状态但可能指数的停时论证。

k=1 另用同一实际 I 候选，直接 Φ=L_1、h_1=1，停止阈值仍>τ/N。每接受增>1/(100N)，moves<100N。停止后 Σδ_j≤τ；若真实 V>r，(3)(4) 给 L_1≥(A−τ)/2=32039/72200>q。完全不使用 ν、m、a 或任何 quadratic error，允许单个 w_j=1。无 fallback、零 M rank 等由同样反证/基线处理。

## 10. 真分配、共享资源和每枚原 job

若终点全 L_i≥q=19/100，令 Good={j:v_j≥t=1/10}。其 outer home mass z_i 满足 L_i≤z_i+t(1−z_i)，所以 z_i≥(q−t)/(1−t)=1/10，包括等号。Good 保留当前实际 I_j 的 B bundle，把 home 给其 outer；其余 helpers 丢弃 B bundle、回原 own state拿 home。Good B union 是 I 子集，仍 M-independent，因此用一次普通 matching 在其补中给所有叶匹配 E_l 资源，并逐叶扫描到原 attaining state（系数≥ε）。

这是同一份完整实际分配：B 内 Good bundles 与叶匹配全局 disjoint，全部 homes 不同且 B 与 homes 不交。outer、Good helper 值≥t，其他 helper 值一，叶值≥ε。没有各 outer 独立取解后重用资源，也没有要求 leaves 自己原本是 singleton states。

显式生成完整 P(Q)，每 selector 去其选定原 state private，只把真 bundle 对应的 selected-state 正 incidence jobs 送 exact resource，所有其余原 incidence jobs（原零、inactive 正 payload、duplicate indexed states、unused resources 上 listed jobs）均留其原 private。每 job 恰一次、只用原有限 endpoints；resource≤1、selected private≤2−t=19/10、inactive private≤1。machine/job/finite-endpoint counts 原封为 S+U、G+I、S+2I。基线同样执行全部原 jobs，C≤2。由 (1)(2) 两输出分支都给相对 19/10。

## 11. 总位复杂度、finder 和所有量词

每轮候选数至多原 fallback state 数，candidate ground≤现有 I 加该 state 显式 support；I 大小≤|B|。weighted matroid greedy 用 polynomially many 普通 matching queries。k≥2 有 <3232k²N moves，k1 有 <100N，均为绝对次数 polynomial，不随输入分母数值循环。整数 m 用二分平方比较精确取得。

每个 L 每轮都从原 incidence bitset 直接重算，是原 w_jp_jsu 的子和，存在 bitlength 为 input 多项式的统一分母。a、q 固定派生有理，d_i=a+max(L_i−q,0)≥a>0；h_i 是 d_i 倒数平方、φ 是一个线性或倒数式，故其 numerator/denominator 位长仍 polynomial。Φ 的 k 项求和最多把 k 个 polynomial-bit 分母相乘，仍 polynomial；比较阈值与候选排序也为精确有理比较。下一轮重新从原 bitset 算 L，不递归把势分母嵌入输入系数。不存在 log、实数根、exact transcendental/SDP oracle、精度参数或随机采样。

本路线直接计算有限候选并以 (8)–(11) 证明 finder 不会错误卡住；没有免费 profile、joint law、fractional feasible point、target、whole-group allocation oracle 或非必要 LP 的“失败”替代实际 FAIL。所有 states/资格/support 数量与 k 均作为输入，完整 P 的生成和逐 job 输出也 polynomial。显式零只在辅助 positive-copy ground 省略，原 ordinary jobs 从未删除。

## 12. 冻结结论和未认证范围

本次只读 504e Exact 后，已独立写出覆盖其新 ν≤1/(1024k)、k1 unrestricted 全量词的完整数学规格；最承重的 weighted step、分段相对余项、阈值等号、停止上界和 alljob 恢复均在本页自证，未发现 fatal。候选作者原 Proof 仍未读，不能提前为它签 PASS；即便作者算法不同，本页也只支持新 Exact 的存在结论。

Python Fraction 仅核 D_0/K、净系数、(11)、k1 和基线等式，不构成算法测试。无端到端实现、有限软件 audit 或外部 primary 来源认证；全球新颖性未认证。此为新的 working Exact-first 记录，未把旧 v4/canonical 的域、算法或审票改写。没有推广到多state outer、home重合、homes上的额外叶、nonUD extras 或一般 ordinary UM；一般 UM-TARGET-v1 仍 OPEN。
