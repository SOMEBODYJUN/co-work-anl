# Shared-UD / tiny-state 19/10：作者 Proof 实际全文读后审

审者：`/root/sol_nsw_independent_attack`，2026-10-18。结论：本页逐项重构后，未发现所读作者数学证明的 fatal；作者的 primal smooth-deficit / exchange / Frank–Wolfe 路线成立。它与我先行的 dual strongly-convex 势路线是不同算法，下文不拿先行结果填补作者步骤。软件范围为无端到端实现或运行认证，全球新颖性未认证。

## 1. 真实次序和实际读取范围

先实际全文读 Exact `/workspace/scratch/038d9dcc4cac/sol_general_repair_shared_ud_tiny_state_potential_19_10_exact_v1.md`，SHA `80fd4ff5b6aab2993e42b995ea369e9441543e754cf3642800c84a784c63cf1d`，1–38 行；在没有作者 Proof/机制时冻结 `/workspace/scratch/038d9dcc4cac/sol_shared_ud_tiny_state_potential_19_10_independent_exact_first.md`，SHA `ee7f19b141ced5d231bfa22229473b644306782e15ff700f79fee4315edc2d90`，18995 bytes、171 lines、0444。父 agent 实际全文读该先行记录后才释放 Proof；原记录没有改字节。

本轮唯一新增本地阅读是 `/workspace/scratch/038d9dcc4cac/sol_general_repair_shared_ud_tiny_state_potential_19_10_author_proof_v1.md`，复核 SHA `409ce88433cd698d477862098023f7e064dbe7a75426117f3c617e70aad7f435`，13302 bytes、164 lines；按 1–100、101–164 两块实际全文读取，无截断。父 agent 随释放信息给出“primal smooth deficit、weighted exchange、FW”的方向，因此这是有先行独立重构的知情 read-after，绝不标成又一张新盲票。

没有读取新 working note、作者代码、运行记录、其他 review 或待追加 canonical；没有 repo/Git/Work/token 操作。此前的旧 k^4-tiny 作者读后、leaf-matroid 背景和自写 given-law 工具属于已知背景，不作为本候选作者证明的替代。本轮仅用 `Fraction` 逐项核算下列常数，没有算法软件验证。

## 2. 对象、可靠无匹配分支和全部普通 jobs

作者完整保留 Exact：k 个 single-state outers、全局不同 homes、每 home 唯一 own-unit helper、任意显式 normalized B-only fallback states、B-only exact-threshold-UD extra leaves，ν=max w_j≤1/(4096k^4)。H=helpers 数，不是 leaf 重边集 H_l；H≥1。原 zeros、重复 indexed states、unused resources 都仍在完整普通 P 中。

作者第 1 节 value 桥可独立逐方向复核。实际 disjoint allocation 值 V 生成 makespan≤2-V 的全 job assignment；反向任何 C<2 的普通 schedule 中 resource unit jobs 各自独占，selector 所在原 state 的导出正价值≥2-C。C=2 边界结合正向不等式给 V=0，故 OPT=2-V∈[1,2]。没有要求给定 schedule 没有 inactive exports；反向只忽略它们的价值，正向重新安排全部原 jobs。

在 ε=15/16 下，叶 bundle 值≥ε 必含全菜单定义的 H_l 物品，否则所选 state 的值≤b_l<ε。叶各选一个这样的物品给 full matching；反向每个 H_l 物品都可枚举到一个原 state 使该叶值≥ε。故叶无 full matching 确推出实际 V<ε，而非仅一个 relaxation FAIL。基线把全部 payload 留各自 private、各组 selector 放一原 private，C≤2，ratio<32/17<19/10。这个分支真正覆盖域内没有完匹配的输入。

有 full matching 时 vacancy matroid M 是 resource-side transversal T 的 dual；D independent in M iff B\D 可匹配全部叶。叶为空是 free matroid，rank(M)=0、unused resources 和 loops/coloops 均不妨碍这个等价。extra leaves 不被当成 singleton states；只在匹配后选择原达到 ≥ε 的 state。

## 3. 固定 profile 的 network、rank function 和 comparator

作者 empty 是辅助 profile 符号，不新增原 state：最终此 helper 回原 own state。固定 profile 的 B-ownership / 叶匹配 polytope 是普通 integral network：每资源至多一 owner、每叶 demand 一、helper 无 resource 数量上界。其投影 outer payoff 每坐标在 [0,1]，因为每 helper 只采用一个 normalized state，Σ_{j∈J_i}w_j=1。

对正 λ，固定 profile 的 linear optimum f_λ 可取 matroid-parallel-copy weighted base；每资源有一个零权 dummy，保证删除/加入 state 后 matroid rank 保持。也可显式算 c_u=max_j λ_i(j)w_jp_jsu，再用 Σc_u 减去 mincost 全叶匹配费用；从而这不是未知 profiles 的优化 oracle。option-set f_λ 的 submodularity 由 threshold weighted-rank 积分及 disjoint option copy blocks 直接推出。

作者实际 V≥ε 时的 comparator O 正确且仅用于分析：从实际 allocation 保留 outer 拿 home 的 helpers 的 fallback states/bundles，它们各值≥ε；各 outer 拿到 home 正权≥ε；叶各保留其 bundle 内的一枚 H_l 物品。由全部 bundles 原已不交，剩余 B 分配在 M 中合法，于是 f_λ(O)≥ε²Σ_iλ_i。算法没有获得、搜索或查询实际 allocation / O。这个必要比较对象与输入一个免费 integral benchmark 不同。

## 4. 平滑势、最优线性面和 deficit 稳定性

作者的 θ=1/32 是势的 slope floor，与恢复 helper quality q=1/10 不同；我先行稿中另用 θ=1/10，不能因此误判常数不一致。作者取 c=5/16，

    Φ(W)=(θ/k)Σ_iW_i-Σ_i(c-W_i)_+²，   P(S)=max_{W feasible}Φ(W)。

每坐标单调，gradient λ_i=θ/k+2(c-W_i)_+>0，gradient 全局 2-Lipschitz，Φ 范围 [-kc²,θ]。对任意精确最大点 W*，凸 feasible payoff polytope 的 first-order inequality 给 λ·(W-W*)≤0，故 W* 在同一 λ-linear optimal face，f_λ(S)=λ·W*。

稳定式 P(S)-Φ(W)≥||d(W)-d*||² 可以不假设 Φ 对全部 W 强凹。将负 Φ 写成 Σd_i²-(θ/k)ΣW_i，约束 d_i≥c-W_i、d_i≥0。最优点的 first-order 线性项对任何 feasible (W,d(W)) 非负，目标差恰为该线性项加 ||d-d*||²。因此只控制 deficits 正确，不会在 W_i≥c 的平坦部分误用强凹。

## 5. 任意 λ-optimal fractional allocation 的稳定交换：独立补足证明

这是我重点重新攻击的步骤。先给两个精确 basis 敏感性事实，适用于任意最优 basis、所有 ties，而非只选某个特别的 greedy optimum。

删除 ground 中一个 e：若当前最大权 basis C 不含 e，无需变化；若含 e，新 ground 仍有满 rank（零 dummies 保证），取任一新最优 basis D。symmetric basis exchange 给 f∈D\C，使 C-e+f 和 D-f+e 同为 bases。旧最优性 w(C)≥w(D-f+e) 推 w(C-e+f)≥w(D)，所以只换一个元素就已新最优。选择最大权可行 replacement 同样成立。

加入一个新 e：若新最优 basis 不使用 e，旧 C 仍最优；否则对一个新最优 D 含 e，用 symmetric exchange 找 f∈C\D 使 D-e+f 和 C-f+e 都是 bases。D-e+f 在旧 ground 中，故 w(C)≥w(D-e+f)，推出 C-f+e 是新最优。这正可由 fundamental circuit 的最小权可删项实现；如没有增益则可保持旧 basis。循环删除全部旧 j copies、再逐项加入新 j copies，始终是对应当前 ground 的最优 basis。

记旧 j 的 weighted value 为 A、新 j 的最终 weighted value 为 B，均≤λ_i(j)w_j。删除阶段其他 helpers 只增，总 weighted gain G≤A，因为删除 ground 不会增加线性最优值。加入阶段其他 helpers 只减，总 weighted loss L≤B，因为加 ground 不会降低线性最优值。中途可能用另一个尚未删掉的旧 j copy 或换掉刚加入的新 j copy，这不影响其他 helpers 的单调方向或最终 A/B 总账。

将 helper changes 聚到 outers，非 j-owner 坐标的 weighted change 在 [-B,A]；owner 坐标含 j 的 B-A，再加本 outer 其他 helpers 的 gain/loss，所以在 [-A,B]。于是

    max_i |λ_iΔW_i|≤max(A,B)≤λ_i(j)w_j，
    Σ_i |λ_iΔW_i|≤|B-A|+G+L≤2max(A,B)≤2λ_i(j)w_j。

这没有把 j 当成独占一个 outer，也没有把两个方向交换费用误相加为四倍。两端都是对应 ground 的 λ 最优 basis，故 λ·ΔW=f_λ(S')-f_λ(S) 精确。

现在给任意 λ-optimal fractional feasible allocation：其原 network flow 可分解成 integral feasible vertices，因 λ·W 已是最大值，分解中的每个正权重 vertex 都在同一个 linear optimal face。每个 integral claim set 可用零 dummies 扩成 M-parallel-extension 的 basis，保持原 helper payoff；基于最优值，它也是 λ-optimal basis。逐 basis 做上述更新再平均，得新 profile 下的 feasible W'，精确保留两端 optimum 值差；L∞/L1 界由凸性保留。这是对每一个旧最优 fractional payoff/flow 的存在耦合，不是只证明存在一对特别的端点。

算法不需实际分解这个 fractional optimum，也不需输出耦合；耦合只证明另一个 profile 的 maximum potential 至少有这么大。这一存在用法与把不能计算的 coupled optimizer 当 oracle 有实质区别。

由上述 weighted bounds，||ΔW||²≤2(λ_i(j)/λ_min)²w_j²=:B_j。Φ 的 2-smoothness 给 P(S')-P(S)≥Δ_j-B_j，恰是作者 (4.2)–(4.3)，不用任意高阶非负性、SDP 或先行 dual 势来补足。

## 6. curvature 总账、small-k 和实际 comparator 的进展

submodular option 比较逐项给 Σ_jΔ_j≥f_λ(O)-2f_λ(S)。因为 λ=θ/k+2d，Σλ=θ+2D，且 λ·W*≤θ+2cD（D=Σd），真实 V≥ε 时

    ΣΔ_j≥(65/128)D-287/8192。

每 outer 的 Σw_j²≤ν。用 λ_min≥θ/k 和 d_i²≤cd_i，

    ΣB_j≤(2ν/λ_min²)Σλ_i²
          ≤1/(2048k³)+D/(16k³)+(5/8)D/k²。

k≥2 时右侧≤1/16384+(21/128)D，故 summed potential gain≥(11/32)D-575/16384。当 D≥9/80，该值≥293/81920=ρ>0。k=1 用真实 λ_min=λ_1，直接 ΣB≤2ν≤1/2048，此时同一个 D 下净 gain≥885/40960=177/8192>ρ。作者没有把粗 floor 应用于 k=1 而漏掉正余量。

因此坏 profile 在真实 V≥ε 时，总有某个实际列出的单 helper option swap 使 P 增≥ρ/H。O 不必知道；算法枚举所有原 fallback options 加 empty 已包含其各分量。重复 indexed states 和 same/empty option 不影响 summed inequality。

## 7. 有限 Frank–Wolfe 估值与实际分母

起点 W=0 加任一全叶匹配是 feasible。每步 gradient λ>0，用固定 profile 的精确匹配线性 oracle 取一个 integral payoff V_t，γ_t=2/(t+2)，更新完整 flow 和 W 的相同凸组合。其 feasible property 与全部叶 rows 全程保持。2-smooth concavity、payoff diameter²≤k 给 gap_{t+1}≤(1-γ_t)gap_t+kγ_t²；初始 gap≤θ+kc²≤2k，归纳得到 gap_t≤4k/(t+2)。取 T_FW=ceil(4k/ξ)、ξ=1/(2^20H²)，得实际 P_hat=Φ(W_hat)∈[P-ξ,P]。

位复杂度不能只说“有理迭代”：γ_0=1，所以 t 步后 vertex r=0,…,t-1 的显式权重确为 2(r+1)/(t(t+1))，权重总和一。原 integral payoff 的坐标都是原 w_jp_jsu 的子和，可选 bitlength polynomial(input) 的固定共同分母 D_1。因此 W_t 的分母可取 D_1 t(t+1)，完整 flow 取 t(t+1)。可以直接维护加权整数累计量，或每步约分；不会出现 t! 型编码长度或数值分母次迭代。

每步 gradient、matching price、comparison、Φ(W_t) 的编码长度因此 polynomial(input,log t)。T_FW=O(kH²) 有固定巨大常数但仍为绝对 polynomial。无需 exact QP/SDP finder、输入 precision、随机 profile 期望求值或 exponential configuration oracle。同一 profile 的起点、步数、tie 次序固定，使 P_hat 真是确定的函数。

## 8. 可靠 FAIL 与整个 profile 循环的终止

停止输出条件是所有 W_hat_i≥25/128。若某坐标失败，其 d_hat_i>15/128。deficit 稳定性给 |d_hat_i-d_i*|≤sqrtξ≤1/1024<3/640=15/128-9/80，所以该精确 optimum 的 D>9/80。

若真实 V≥ε，上一节存在 exact P 改善≥ρ/H。新估值至少 P_new-ξ，当前估值至多 P_current，因此 observed P_hat 改善≥ρ/H-ξ>τ=1/(2048H)。最后不等式对 H≥1 由 ρ-1/2^20-1/2048=16187/5242880>0 直接保证。故“没有改善”分支真实推出 V<ε；没有把 near-optimum Φ 或 profile solver 当 actual scheduling oracle。

每次接受 observed P_hat 至少增加 τ；因相同 profile 评价可重现且 Φ 范围 [-kc²,θ]，无论输入实际 V 高低，moves≤(θ+kc²)/τ+1=O(kH)。每次枚举候选数为原 helper fallback states 加 H，乘上每次 O(kH²) matching calls，得到固定绝对次数的总位 polynomial，未穷举所有 profile，也无随机拒绝或采样停时。

## 9. 共同 prefix-flow 的独立构造与完整回填

成功的同一 fractional flow 有全部叶完整匹配和每 outer W_hat_i≥25/128。令 a_iu=max_{j∈J_i}w_jp_{j,S_j,u}；每列把原 outer claims 给一个达到最大值的 selected-state helper，只会增值，保持列容量与 leaf flows，且 a_iu≤ν。固定 profile 的 normalized states 还给 Σ_u a_iu≤Σ_jw_j=1，但 rounding 不需此总和恰为一。

对 outer 的正系数资源按 a_1≥…≥a_m>0 排序，原 fractional claims z_r，prefix F_l=Σ_{r≤l}z_r。明确的 integer circulation 可这样构造：source 进入该 outer 的末节点 v_m；链 v_l→v_{l-1} 携带前 l-1 个资源的总流，lower floor(F_{l-1})；source→v_m 的 lower 是 floor(F_m)。每 v_l→resource u_l capacity 一。所有链 upper 可取 |B|；每叶另有 source→leaf lower=upper 一、leaf→H_l 资源边；全部资源→sink capacity 一，再加 sink→source 回流边。原 aggregated claims 加叶 flows 见证 feasibility，所有 lower/upper integer，故普通 integral maxflow 给同一张全局资源分配和全叶 matching。

选中资源的 integer prefix counts N_l≥floor(F_l)。置 a_{m+1}=0，summation by parts 给 utility 差≤Σ_l(a_l-a_{l+1})(F_l-floor(F_l))≤a_1≤ν。因此每 outer 得

    W_i≥25/128-ν≥799/4096， 且 799/4096-19/100=519/102400>0。

这是与全部叶共用 resource capacity 的一个 circulation，绝不是各 outer 各自 rounding 后拼接。原 zero utility edges 可不选，不需要虚构零 incidence；positive-owned 资源按原 profile state 给 argmax helper，故每 helper 真实 q_j≤1。

以 q=1/10 定义 Good helpers。若其 outer home mass 为 z_i，则 W_i≤z_i+q(1-z_i)；由 W_i>19/100=q+q(1-q)，得 z_i>q。Good 保留 B bundle 并释放 own home，outer 拿这些 homes；非 Good helper 回原 own state 拿唯一 home；叶保留其 H_l 匹配资源并选一个原 attaining state。全 homes 不同且 B 与 homes 不交，因此真正全局 disjoint，全部 groups 值≥q。

最后 selectors 放上述原 indexed states 的原 privates，只导出其真正领到的正 incidence jobs，其余所有原 jobs（包括原零 jobs、inactive 正 payload、重复 indexed states payload）都留各自原 private。资源负载≤1、selected private≤2-q=19/10、inactive private≤1。所有 jobs 逐个恰执行一次，有限资格未改；machine/job/finite-endpoint counts 仍为 S+U、G+I、S+2I。successful C≤19/10≤(19/10)OPT，可靠 FAIL 基线 ratio<32/17，两分支闭合。

## 10. 结论与限制

作者第 1–9 节全文已实际读取，其主承重任意 λ-optimal fractional base coupling、curvature 的 k=1 分支、deficit 近似、FW 显式 rational weights、有限 profile 改善和同一 prefix-flow，我均在本页按作者算法重构，未发现 fatal。支持的是新 Exact 的原 k^4-tiny / B-only UD-leaf 输入域和 Q-alone deterministic 19/10，不升级为一般 normalized Q、multi-state outers、非tiny homes、homes上的 extra leaf、nonUD extras 或一般 UM。

我的先行算法用 min-α strongly-convex 势、有理 projected subgradient、末尾 fixed-profile LP 与 utility slots；作者用 max-W smooth deficit 势、stable exchange、FW 与 integer prefix circulation。它们结论相同，证明接口分别核查；本次没有拿已通过的先行结论当作者推导依据。

本轮未读取任何软件/运行产物，只有常数 Fraction 核算。算法仍为数学规格，无端到端软件认证；全球新颖性未认证。本记录另冻，先行 ee7f19b 字节保持不变；后续 canonical actual read 须另记录，不能提前认证未读正文。
