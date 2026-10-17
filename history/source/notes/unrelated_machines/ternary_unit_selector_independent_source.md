# 三端单位选择器正规形：独立陈述先行重构

审查者：boss11 内部子研究者 literal_gap_implementation。
审查对象仅为 Exact 文件 `ternary_unit_selector_normal_form_exact_statement.md`，SHA256 `cbebbbface83e98cbbdce49c7a7d772a5bcd876fd7c5d03ffcd1fbcf62268176`。

## 审查纪律与结论

本稿在未读 root/row/pcsp 新证明和 repo 新增 §7 的情况下独立重构。两个候选均没有发现 fatal objection；下列给出完整独立构造及未知 OPT 的算法转移，而非依赖有限测试。新颖性未审查；没有给出 UM 求解器或 UM 困难性。

涉及 ID：
- `UM-TERNARY-UNIT-SELECTOR-NORMAL-FORM-v1`：独立重构成立。
- `UM-TARGET-TERNARY-SELECTOR-EQUIVALENCE-v1`：独立重构成立。

## 一、有限端全部不超过 b 时的实际构造

固定任意正有理数 b，原 P 的每个有限端 p_ij 均在 [0,b]。每个原 job j 有 d_j>=1 个有限端，逐个与一个候选叶一一对应。取一棵有 d_j 个叶的满二叉树；d_j=1 时整树只有一叶。不同 j 的树机器全部私有，且与所有原 machine 副本不同。

为树的每个节点 v 建一台辅助机器 a_v，并加入：

1. 单个 root job，唯一资格是根机器，时间 b。
2. 每个内部节点 v 一个 selector job，资格恰为 a_v 及其两个孩子机器，三个时间均为 b。
3. 对应原边 (i,j) 的每个叶 v 一个 terminal job，恰两个资格：原 machine i 副本时间 p_ij；叶机器 a_v 时间 b。

若 p_ij<b，terminal 是题述 SU 类，包含 p_ij=0；若 p_ij=b，它是两端 unit-only 类。因此所有新 job 均属于指定 normal class。没有任何辅助机器获得 small 资格。

满二叉树的内部节点数是 d_j-1，节点总数是 2d_j-1。其 job 数为 1+(d_j-1)+d_j=2d_j，有限资格数为 1+3(d_j-1)+2d_j=5d_j-2。总计辅助机器 2|E|-n、新 jobs 2|E|、有限资格 5|E|-2n；n=0 时没有 gadget，仅保留 m 台原机器副本。所有大小为 O(m+n+|E|)，不会按 b 或 k 的数值展开。

### (A) 任意原实际调度的扩张

给定原完整 sigma，对每个 j 取 sigma(j) 对应的叶 v*，将此叶 terminal 分配至原 machine sigma(j)，用时恰为 p_sigma(j),j。其他 terminal 全部分配至自己的叶机器。

root job 分配根机器。沿根到 v* 的路径，每个内部节点 selector 分配到路径的下一孩子机器。所有不在此路径上的内部节点 selector 分配到自己的节点机器。

于是每个辅助机器恰有一个时间 b 的 job，负载为 b；原机器的 terminal 负载逐项等于 sigma 中原 job 负载。因此 C(tau)<=max{b,C(sigma)}，实际获得完整合法 tau。

### (B) 任意 C(tau)<2b 的实际调度的收缩

给定任意新完整合法 tau，所有辅助机器上的每个可用 job 都恰有处理时间 b。所以 C(tau)<2b 强制每台辅助机器至多承载一个 job。

对每个 gadget，root job 占据根。若当前到达内部节点，其 selector job 不能也放在当前节点，因此必须放在某一个孩子；继续沿实际分配走到叶。到达的叶已被一个 b-job 占据，其 terminal 不能留在该叶，必须放在对应原 machine 副本。选择该实际 terminal 所对应的原合法端作为 sigma(j)。

同样可用计数核对存在性：gadget 有 V 个辅助机器、V+1 个 jobs，而全部非 terminal jobs 只有本 gadget 辅助资格；在每机至多一个 b-job 的情况下，至少一个 terminal 必须外送原机器。

每个原 job j 只选一个实际已放至原机器的 terminal。由于不同 j 的 terminal 是不同新 jobs，且 p>=0，对每台原 machine i 有

    sum_{j:sigma(j)=i} p_ij <= load_tau(original-copy i).

这是真实完整 sigma，不只是标签或局部模式。扫描每棵树构造选中路径，或扫描外送 terminals，均为总位多项式。非负性在逐机子集负载论证中是必要条件，且题域已满足。

### 两值、零值和边界

若所有原有限 p 属于 {b/k,b}，k>=2，则新非 unit 端全部仍为 b/k，且每个原 small 资格恰出现一次。原 machine 的 small 资格数完全保持；新增 machines 的 small 资格数为零；每个 new small job 为 SU 两端，其余 job 至多三端。只复制 p 和 b 的二进制表示，不展开 k。

空任务无 gadget；零端合法；单可用端使用单叶树；OPT(P)=0 也满足 (A)，但 N 的辅助负载可以是 b，不能宣称 OPT 自动逐值相等。若原某端 p>b，以上 (A) 不能覆盖该端；必须先剪枝。剪枝后某 j 无剩余端时，每个原调度都给 j 用时 >b，因此可靠得 OPT(P)>b。

## 二、normal class 与 UM-TARGET-v1 的真正算法等价

一般 UM 算法显然也适用于 normal class；给定的 common b 只是可忽略附加输入。反方向不假定知道 OPT，也不把阈值存在性误当作算法。

假设存在固定 epsilon>0 的 normal-class 位多项式 actual 算法 F，近似因子至多 2-epsilon。选择一个固定有理常数 eta，0<eta<min{epsilon,1}；从而同一 F 也满足因子 alpha=2-eta。选择固定有理网格比率 g=1+eta/4。

先处理退化：
- 若 n=0，输出空分配，C=0。
- 对每个 j 检查是否存在 p_ij=0。若每个 j 都有零端，选择任意零端即可，OPT=0。
- 否则定义 a_j=min_i p_ij（忽略 infinity），L=max_j a_j，U=sum_j a_j。每个 job 至少一个有限端保证 a_j 有定义；至少一个 job 无零端保证 L>0。

每个实际调度的最大负载至少 L。把各 job 分配至其最短端得到一个合法调度，其最大负载至多 U。因此

    0<L<=OPT(P)<=U<=nL.

生成 b_t=L*g^t，t=0,1,...，直到首次 b_t>=U。固定 eta 下只有 O(log(n+1)) 个阈值；每个有理数的总位长多项式。特别不需要按处理时间最大/最小比或数值大小扫描。

对每个 b_t：
1. 删除 P 中所有 p>b_t 的资格。若某 job 无资格，跳过此可靠 NO 阈值。
2. 对合法剪枝矩阵 P_t 构造 N_{b_t}(P_t)，运行 F，得到完整合法 tau_t。
3. 精确计算 tau_t 的实际负载。仅当 C(tau_t)<2b_t 时用 (B) 解码为原 P 的实际 sigma_t；其他输出跳过。
4. 在得到的所有 sigma_t 中，按原 P 的精确实际 C 选择最小值。

至少一个可收结果存在。取网格里第一个 b_t>=OPT(P)。若 t=0 则 b_t=OPT(P)；若 t>0 则 b_t<g*OPT(P)。原最优调度的每个使用端不超过其机器负载，从而都不超过 OPT(P)<=b_t，故在 P_t 中保留，且 (A) 给 OPT(N_{b_t}(P_t))<=b_t。于是

    C(tau_t)<=alpha*b_t<2b_t,

必能解码，且

    C(sigma_t)<=alpha*b_t<=alpha*g*OPT(P)
                  =(2-eta)(1+eta/4) OPT(P)
                  =(2-eta/2-eta^2/4) OPT(P)
                  <=(2-eta/2) OPT(P).

其他低阈值的 F 输出若偶然小于 2b_t，(B) 仍给原 P 的真实合法调度；只会改善最后的择优，不能引入错误接受。各调用的机器/job/资格数及位长度多项式，调用数多项式，F 的常数因子由固定 eta 控制。因此取得一个与 m,n,P 无关的确定性位多项式实际 (2-eta/2) 算法，满足 UM-TARGET-v1。

## 审查范围与保留事项

本重构同时检查了：严格小于 2b 的必要性；剪枝的量词范围；所有 job 的实际唯一分配；逐台原机器全局负载；零端、OPT0、空任务、单叶 gadget；未知 OPT 的有理网格与总位复杂度；{b/k,b} 的资格保持。没有发现需要额外假设的步骤。允许 C=2b 时辅助机器可容纳两个 unit jobs，(B) 不能由该构造保证；候选仅要求严格不等式，匹配本证明。

这只把主目标转为一个非常受限的 normal class，既不证明其存在次2算法，也不证明近2困难性。未审查任何新颖性或期刊价值。
