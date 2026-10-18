# 共享 UD 叶、tiny-home k² / k=1 无 tiny：独立 Exact-first 冻结记录

审者：`/root/sol_true_hardness`，2026-10-18。结论：从限定 Exact 自行重构出确定性总位多项式算法，覆盖 v4（故也覆盖 v3）；本记录没有发现数学 fatal。一般 ordinary UM 的 near-2 主问题仍 OPEN。

## 1. 实际阅读及独立性边界

本次全文实际读过以下三个 Exact，并核 SHA256：

- `boss11_shared_ud_tiny_home_k2_refinement_exact_v4.md`：`8948b47cc8b2f303f7f1446ecb0137da163d0b65e906ec4169c5f85294ef877d`，2486 bytes。
- `boss11_shared_ud_tiny_home_k2_refinement_exact_v3.md`：`cc9d1037da7e86c74226968b890eaad6e646c4179bf16fe789a776818d2b6c39`，2124 bytes。
- 仅用作完整输入域的 `sol_general_repair_shared_ud_tiny_state_potential_19_10_exact_v1.md`：`80fd4ff5b6aab2993e42b995ea369e9441543e754cf3642800c84a784c63cf1d`，3867 bytes。

没有打开本候选任何作者 Proof、code、append、NSW review，也没有接收 root 的具体 k² 机制。已知背景包括 normalized-flat 调度/分配对应、transversal/dual matroid 及 weighted-rank 基本性质；不是声称这些背景也全新 blind。本记录的势函数、常数、局部更新、误差和恢复均在只获上述 Exact 后独立重构。

v4 与 v3 的实际量词差异是 k=1 解除 max w 上界；k≥2 仍为 ν=max w≤1/(16384 k²)。下述 k=1 证明确实完全不用 ν。

## 2. 记号与两个足够分支

沿 Exact：outer i 的正 home 权 w_j>0，j∈J_i，Σ_{j∈J_i}w_j=1；所有 home 全局互异，每 home 有唯一 own-unit helper。helper 的 fallback states 只在 B 有正项，且每 state 系数和一。额外叶只在 B 有正项，ε=15/16，H_l={u:max_s p_lsu≥ε}，每个 state 在 B\H_l 的总质量严格小于 ε。所有显式零 incidence 和原 indexed states 都保留在最终普通矩阵中。

定义 V 为原 normalized menu 的最大最小整数分配值：每 group 选一原 state，取得互不相交的资源 bundle，质量为所选 state 在 bundle 上的系数和。总量归一给 0≤V≤1。

对 Exact 的完整普通矩阵有 OPT=2−V：分配质量≥v 时，选中 state 的 selector 留 private，分给它的 incidence jobs 送原 resource，其他所有原 incidence jobs 留各自 private；选中 root 负载 2−quality，未选 root 负载 1，resource 负载至多 1。反向若完整调度 C<2，每 resource 至多容一枚 unit incidence job；取各 selector 所在 state 的外送 incidence，得到互不交 bundle，质量至少 2−C。C≥2 的下界平凡。所有 groups 菜单非空且至少有 outer selector，所以 OPT≥1。

令 a=324/361=(18/19)²、t=1/10、λ=19/100。算法只需以下两分支：

1. 若能构造全组质量至少 t 的实际分配，输出全原 jobs，C≤19/10≤(19/10)OPT。
2. 若能证明 V≤18/19，输出所有 incidence 留 private 的完整 baseline，C≤2≤(19/10)(2−V)。

以下不调用 V、OPT、其见证或优化 oracle；V 只用于反证保证。

## 3. 共享叶的精确 matroid 处理

先在 leaf l—B 的资格图 H_l 上求全叶匹配。若不存在，任何质量≥ε 的分配都会给每叶一枚 H_l 资源：其选中 state 在 H_l 外总值<ε，故达到 ε 必须取 H_l 中正贡献项。资源互斥使这些项成全匹配。因此无全匹配时 V<ε<18/19，直接用分支 2。

以下假定有全叶匹配，叶数为 q（可为零）。令 A 为 B 上的 transversal matroid：独立集是可匹配到不同叶的资源集；r_A(B)=q。令 M=A*。对 R⊆B：

    R independent in M  ⇔  B\R 仍可匹配全部 q 叶。
    r_M(R)=|R|+r_A(B\R)−q。

两式由 matroid 对偶的补基定义直接得出；独立性只需一次普通匹配。无叶时 M 是自由 matroid。任何最终保留的 helper 资源 union 若在 M 独立，就能在剩余 B 给所有叶恢复原 H 匹配；每叶随后选一原 state 使其匹配项系数≥ε。

在带标签的 helper fallback 正 incidence (j,s,u) 上取 M 的平行扩张 Mhat：同一 u 的所有标签是平行副本。独立意即原 u 不重复且原资源集在 M 独立。oracle 只检查重复与上述匹配，不把 state-profile 优化藏入 oracle。

## 4. 局部状态、可计算更新及 rank 证书

维护每个有 fallback 的 helper 的一个原 fallback state s_j，以及一个实际独立 incidence 集 I；I_j 只用该 helper 的 s_j，原资源不重复，union 在 M 独立。无 fallback 的 helper 用空记号，I_j 永远为空；这只是 bookkeeping，不新增 state/job。初始化选任意首个 fallback，I=∅。令

    v_j=Σ_{(j,s_j,u)∈I}p_j,s_j,u ∈[0,1]，
    L_i=Σ_{j∈J_i}w_j v_j ∈[0,1]。

固定任意正 h_i。给完整标签 ground 上 incidence (j,s,u) 权 h_i w_j p_j,s,u，i=i(j)。W(I)=Σ_i h_i L_i。对单 helper j 及其候选原 fallback state s，在 ground

    I_{−j} ∪ {(j,s,u):p_j,s,u>0}

上求最大权 Mhat-independent set I'_{j,s}。这是普通 weighted matroid greedy：按精确有理权降序逐项试独立性，每步只调用 matching。其他 helper 只能失去现有项；j 可以整包换 state。无 fallback j 不更新，定义其增益为零。旧 state 候选包含原 I，故

    δ_j=max_s [W(I'_{j,s})−W(I)] ≥0。

令 I* 是任意可行的参考 helper bundles：每 helper 至多一个原 fallback state，资源 union 在 M 独立，允许部分 helper 为空。则有

    Σ_i h_i L_i* ≤ 2 Σ_i h_i L_i + Σ_j δ_j。              (R)

证明：(固定当前权) weighted rank F(S)=max_{J⊆S independent}W(J) 为单调次模。可将它写成降序权阈值上的 rank 之非负线性组合，故这一性质不需要 base-orderability 或多项集合的强交换假设。F(I)=W(I)，且

    F(I∪I_j*) ≤ F(I_{−j}∪I_j*)+W(I_j)
               ≤ W(I)+δ_j+W(I_j)。

候选 state 用 I_j* 的那个，空 bundle 时任意旧候选足够。对各 j 用次模边际望远镜，F(I∪I*)≤F(I)+Σ_j(F(I∪I_j*)−F(I))，再 Σ_jW(I_j)=W(I)，得 (R)。即使 I* 与 I 对同 helper 使用不同 state，F 的全标签 ground 仍合法；它只用于上界，不作为输出 allocation。

## 5. 近完美真解给出的参考 bundles

若 V>18/19，取达到 V 的真实分配，仅作分析。outer i 收到的正 home 权和≥V。对每枚被 outer 收到的 g_j，helper H_j 不可能靠自己的 own-unit state 达正值，故它在某 fallback state 上收到 B bundle 值至少 V。只保留这些 helper bundles，其他 helper 置空。

每叶值≥V>ε，所以原分配给出互异 H_l 代表；上述 helper bundles 避开这些代表，因而 union 在 M 独立。参考向量满足

    L_i* ≥ V · Σ_{g_j 给 outer i} w_j ≥ V² > a=324/361    (每个 i)。   (W)

此步同时支付了共享 B、叶匹配及所有 outer 的共同见证；并没有为各 outer 分别用不同资源解。

## 6. k≥2 的势函数、真实更新误差与停止

取 γ=3/10，b=1/(50k)，τ=1/100，N=Σ_i|J_i|。定义

    Φ(L)=Σ_i [−(γ−L_i)_+²+b L_i]，
    g_i=2(γ−L_i)_+，h_i=g_i+b，G=Σ_i g_i。

在当前 h 上依第4节求每个候选 I'，以其实际新 L 计算真实 Φ。若某候选 Φ 增加>τ/N，按固定输入次序采用一个；否则停止。每次采用后重新计算 h。无需指数 profile 枚举。

势各坐标梯度 2-Lipschitz，故对任何 Δ：

    Φ(L+Δ) ≥ Φ(L)+Σ_i h_i Δ_i−Σ_i Δ_i²。               (P)

以下误差特意包含同 outer 的其他 helper 被挤出。对 j∈J_i 的一次候选，归一性给新 j bundle 权值≤h_i w_j；因 I_{−j} 是候选 ground 的可行解，最优候选失去其他 helper 的加权质量也≤h_i w_j。于是同 outer 的其他 helper 总损失≤w_j，j 本身净改变绝对值≤w_j，所以 |Δ_i|≤2w_j；其他 outer 只有损失，其总未加权损失≤h_i w_j/b。因此

    Σ_l Δ_l² ≤ 4w_j²+(h_i/b)²w_j²。                    (E1)

停止时对每个选定 weighted-max 候选，真实势增益≤τ/N；由 (P)，其线性增益≤右侧 (E1)+τ/N。取各 helper 的最大线性增益并求和，Σ_{j∈J_i}w_j²≤νΣ_jw_j=ν，得

    Σ_jδ_j ≤ E+τ，
    E≤ν[4k+b^(−2)Σ_i h_i²]
      ≤ν[5k+b^(−2)(3/5+2b)G]。

这里 g_i∈[0,3/5]，故 Σg_i²≤(3/5)G。ν≤1/(16384k²)，k≥2，2b≤1/50，给

    E ≤ 5/32768+(1550/16384)G。                         (E2)

若真有 (W)，由 (R) 和终点误差，D=Σ_i h_i(L_i*−2L_i)≤E+τ。另一方面 g_i>0 时 L_i<3/10，而总有 L_i≤1，所以

    D ≥ (a−3/5)G−(2−a)bk
      = (537/1805)G−398/(361·50)。                     (D)

若某 L_i<19/100，则 G>11/50。合并 (E2)(D) 会要求

    [537/1805−1550/16384]G
       ≤398/(361·50)+5/32768+1/100。

但系数为 3000229/14786560>0；在 G=11/50 左侧减右侧已为

    18388693/1478656000 > 0。

矛盾。因此 V>18/19 时，终点每个 L_i≥19/100。上述确切分数由审者独立的一次 Python Fraction 算术核对；没有执行作者程序，也没有把有限枚举当理论证明。

## 7. k=1 完全无需 tiny

用同一局部候选，但 Φ=L_1、h_1=1。真实势增益等于线性增益；停止标准仍为>τ/N。故 Σ_jδ_j≤τ，(R)(W) 直接给

    L_1 ≥ (324/361−1/100)/2 = 32039/72200 > 19/100。

没有二次更新误差，也没有任何地方使用 max w 或 Σw² 上界；允许某个 w_j=1。无 fallback 的 helper、零有效 M rank 均由相同反证/基线分支覆盖。

## 8. 实际恢复、全部原 jobs 与总位复杂度

在对应算法停止后：若某 L_i<19/100，由上述反证可知 V≤18/19，输出分支 2 baseline。否则令 helper j 被选当且仅当 v_j≥t=1/10。若 W_i 为被选 helpers 的 home 权和，则

    L_i≤W_i+(1−W_i)t，
    W_i≥(19/100−1/10)/(1−1/10)=1/10。

被选 helper 保留其实际 I_j 的 fallback bundle，质量≥1/10，其 home 交给对应 outer；未选 helper 丢弃 B bundle，取自己的原 own-unit state/home，质量一。所有 outer 得到质量≥1/10。被选的 B union 是原 I 的子集，仍 M-independent，故用普通匹配把所有额外叶配进剩余 B，各选一原 state/原匹配项，质量≥ε。各物理 home 互异且 B disjoint homes，故这是所有 groups 的同一真实资源分配。

将它填回完整原矩阵：每组 selector 放其所选原 indexed-state private；只把实际分配 bundle 对应的所选 state incidence jobs 送原 resource，其他所有 incidence jobs（包括未选 states、显式零、重复 states、unused-resource 的 listed 项）一律放原 private。每枚原 job 恰执行一次，有限端点均原有；每原 resource 至多一 unit job。所有选中 private 负载≤19/10，所有未选 private 负载一。baseline 则所有 incidence 都留 private，任意原 state 接 selector，全机≤2。原矩阵和输出仍是 S+U machines、G+I jobs、S+2I finite ends，未增加辅助普通机器或任务。

确定性运行时间：k≥2 时 Φ 始终在 [−9k/100,1/50]，每接受一步增加>1/(100N)，因此接受步数少于 9kN+2N；k=1 的线性势范围[0,1]，少于100N步。每轮候选总数至多输入 fallback state 数；每候选 ground 至多现有 I 加该 state 显式支持，weighted greedy 用多项式次匹配。固定输入顺序决策及破同权，故 worst-case 确定性而非期望/随机重试。

每次 L 都从当前原 incidence 指示集直接重算，只是原有有理 w_j、p 的乘积及有限求和；其分母的位数可用输入各分母位数之和界定，不随迭代次数连乘爆长。h、Φ、greedy 权、比较阈值由这些量与固定常数及 k,N 有理运算得到，位数均多项式。matching 图、current set、候选 ground、最终逐 job 输出也显式多项式。因此上述不调用 OPT、joint law、configuration/profile oracle、随机时间或 generic exact SDP。

## 9. 冻结结论及未认证范围

本记录从已释放 Exact 重构了 v4 全量词内的一条自足证明，包括无叶全匹配、k=1 无 tiny、k≥2 的 k² 阈值、同 outer 挤出误差、所有原 jobs 及总位复杂度。没发现需要放宽 Exact 的例外。此为数学 Exact-first 记录；没有主算法端到端实现、作者软件读取/重放、外部 primary 定理认证或新颖性判定，也不外推 multi-state outer、home 重叠、一般叶或一般 UM。
