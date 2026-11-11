# 精确负载 DP 到有界树宽 FPTAS：v3 定向替代复核

## 当前任务、版本与本次实读范围

本交付对应 `boss5-localfix-repair-c739a698e9b04ffc`，显式替代已 done 的 `unrelated-machines-3a-3a-850a6179151b732e`。核心仍为 `M-14dbe6980117492aa7a3b48c52378dcb`（M14），只读对端仍为 `M-247deecec83946358afe4e89413a7bd1`（M247）。两对象都是通常二进制整数编码、任务不可拆分的 `R||Cmax`；有限端是实际资格，允许同一任务在不同机器上的有限处理时间不同。

| 项目 | 本次核定值 |
| --- | --- |
| 当前中文 body SHA256 | `f322df148d7781110aa8b4460adcbcd1cdffbc2f857ca93f5536abefa6f5fa3a` |
| M14 version / registration pin | 3 / `b4a7cba894657b841b9c88baf9c45f372ed6f7cbbaca225813ea6933b6d7c0ea` |
| M247 version / registration pin | 3 / `f2082f5eaf3a9d65644b2cfe1be641dca8c0d1013cf4712153ec597b09f36f07` |
| 未变的 primary PDF SHA256 | `4b47eaccfcffe81f6713522269b6afa2124bec3d619d6ef3a1b5341db7e48bae` |

新 worker 实读了 `AGENTS.md`、`research/IMPLEMENTATION.md`、`prompts/03-map-worker.md`，新旧完整任务、新旧版本问题所涉的两个完整当前对象合同、旧 receipt、完整旧 edge/review/reading-ledger，以及当前共享中文全文。另读取已经交付的精确远端增量审查，并亲自用 `git show` / `git diff` 对照提交 `56650ea6813513decee236e0353647e07ff7cc63` 与 `724c402aeef432b2e6848fe1b1b67a0ddae33ba3`：正文只变一个 rankwidth 计数段，两对象完整记录均只变 `body.sha256` 与 `version:2→3`；当前工作树正文也独立核为上表 SHA。随后独立检查下文的上界、舍入、cap、分解递归、负载 DP、回溯与位复杂度。

旧 task850 的 primary 实读记录作为历史继承：PDF 文本页1–11，加页12开头至 Lemma17 前半；视觉核页4、6、7、9、11、12；未把页13–19算作那次重审。此次没有新增 PDF 逐页阅读或视觉核对，也没有重做旧记录的 1,962 条 canonical 端点扫描。当前中文正文 frontmatter 的历史“19页实读”是更早资源整理的来源说明，不是本 worker 的阅读声明。新 ledger 原样保存旧 ledger 内容，并另列本次实际阅读和独立证明范围。

原 task850 的有效证明保留于下文。旧 review 的“当前 v2”与任务归属路由均属旧交付时点；本交付使用上表 v3 输入，不改写旧 done 的任何资产。M14 的合法 `B≤2OPT` 是论文辅助路线；新贡献的 `B_min` 是另一个已付清的可计算上界，从未冒称它也满足二倍界。边保持 accepted、unconditional、ALL 的局部 contribution，不提升为 whole_result。

## 目标量词与成立范围

固定一个整数树宽界 `k`。对每个有限、可行的二进制整数处理时间实例，以及输入的有理精度 `epsilon>0`，构造一个合法调度，其 makespan 不超过 `(1+epsilon)OPT`，总位运算时间对实例长度与 `1/epsilon` 为多项式；次数可以依赖固定 `k`。这不是关于参数 `k` 的 EPTAS 或 FPT 近似时间声明，亦不是只凭树宽的精确 FPT。

空任务返回空调度。若存在无有限资格端的任务，先判不可行。为兼容零处理时间，下面构造的上界若为 0，所构造的调度已经最优；其余情况网格严格为正。中文正文使用正有限处理时间时，这个零值分支自然省略。

本边只交付核心陈述中的 FPTAS 部分。核心还包含独立的弱 NP-hard 性，不能把同一 DP 的算法用途说成已经推导了困难性。因此使用 contribution，而非 whole_result。

## 一、完全付清的初等上界

对每个任务 `j`，选一个使有限 `p_ij` 最小的机器 `i(j)`，并把任务放到此端。记所得合法调度的 makespan 为 `B_min`。扫描输入与作有限整数比较即能构造它。

设 `sigma*` 为任一最优调度。每个任务满足

`min_i p_ij <= p_{sigma*(j),j} <= OPT`。

因此

`OPT <= B_min <= sum_j min_i p_ij <= n OPT`。

这提供所需的可计算上界，不调用 LST 2-近似，也不需要把未阅读的外部算法藏在 conditions。它和论文中 `OPT<=B<=2OPT` 的上界是两个不同构造；不宣称 `B_min` 满足论文那个更强的 2 倍界。

## 二、网格、误差与有限状态

设 `epsilon0=min{epsilon,1}`。当 `n>=1` 且 `B_min>0` 时取

`q=epsilon0 B_min/n^2`，`a_ij=ceil(p_ij/q)`（仅对原有限端）。

只改变处理时间，不复制任务、不增加资格端，三种资格图不变。对原最优调度，每台机器最多接收 `n` 个任务，故

`q load_a(sigma*,i) <= load_p(sigma*,i)+nq <= OPT+nq`。

于是原最优调度在缩放整数实例中满足总负载 cap

`K=floor((B_min+nq)/q)=floor(n^2/epsilon0+n)`。

对精确整数负载 DP 只保留每机 `0,...,K` 的状态。该剪枝保留至少一个最优的缩放调度：以上原最优调度已经在 cap 内，缩放最优值不会更大。每个局部负载都是最终负载的非负子和，因此中间状态剪枝同样不会丢掉这份调度。大于 K 的单端时间无需展开枚举；算出后跳过即可。若把这种端临时视为禁止端，原分解仍然是子图的有效分解，树宽不会增大。

`M-247...` 提供的正是 `L^{O(k)}O(nm)` 型 DP，而不只是任意的 `f(k,OPT)poly(input)` 存在性。这里 `L<=K+1=O(n^2/epsilon0+n)`，代入后仍对固定树宽为多项式。不能从抽象 FPT 时间的一般 `f` 自动推出 FPTAS；本比较依赖明确的负载状态复杂度。

DP 回溯得到缩放最优调度 `sigma_a`，还原到原处理时间仍合法，并满足

`C_p(sigma_a) <= q C_a(sigma_a) <= q C_a(sigma*) <= OPT+nq <= (1+epsilon0)OPT <= (1+epsilon)OPT`。

这就是精确 DP 的实际算法贡献，没有未付的上界算法。

## 三、位复杂度、分解和 cap 的含义

设输入位长为 N，`epsilon0=u/v` 为正有理数。`B_min` 是输入整数子和，位长至多 `O(N+log n)`。缩放时间可直接用整数算式

`a_ij=ceil(n^2 v p_ij/(u B_min))`

计算；乘法、除法和比较的操作数位长为 `poly(N+bits(epsilon)+log n)`。不会建立长度等于原数值 `B_min` 或最大处理时间的数组。DP 只枚举 `0..K` 的整数负载；单端若比 K 大，检测后跳过。位运算的额外开销为输入长度与精度编码长度的多项式。

若分解作为显式输入，直接应用对象 M247 的契约。对只承诺固定宽度的原始图，也可以用以下简单的 `|V|^{O(k)}` 搜索找分解，从而无需在本边中调用一个未交付的专用 FPT 分解识别后端：枚举 `S subset V, |S|<=k+1` 及 `G-S` 的连通分量 C，状态问 `G[S union C]` 是否有宽度 k、根袋 S 的分解。对 `N(C)=S` 的状态，枚举 `S subset B subset S union C`、`|B|<=k+1`、`B cap C` 非空；对 `G[C-B]` 的每个分量 D 递归核 `(N(D),D)`，把对应分解接到袋 B 即可。边界中没有 C 邻居的顶点先删去，再把原根袋 S 接回。按 |C| 递增求值。根袋 S 下 C 的出现位置连通，故所有含 C 顶点的袋落在同一子树；每个边界顶点都有 C 邻居，第一张接触 C 的袋必含整个 S。这保证上述枚举完整。状态数与枚举数均为 `|V|^{O(k)}`，固定 k 时为多项式。

对 dual 图，任务的资格机器集合是团，某袋完整包含它；把该任务作为叶袋 `M(j) union {j}` 接在此袋，得到宽度至多 `k+1` 的 incidence 分解。此处必须用正确的团下界 `|M(j)|<=k+1`，不能用源文漏减一的 Remark 7。对 incidence 图直接用其分解。

cap 的标准 DP 可视为给 incidence 分解的每个活跃任务存一位“已选某资格端”、每个活跃机器存负载 `0..T`。介绍一条资格边时决定选或不选；选择须任务尚未分配，再把 `a_ij` 加至机器负载。忘任务时要求该位为 1；合并节点把两孩子的任务位相加并要求至多 1，把机器负载相加并要求至多 T。每条边恰介绍一次，遗忘机器时其负载已完整。对 T 在 `0..K` 二分作可行性 DP 并回溯即可精确优化。其状态规模 `2^{O(k)}(T+1)^{O(k)}`，确保上述 cap 修改是真正可实施的，而不是把“全体调度的负载值数”错误说成被 OPT 自动界住。

## 四、与论文 2 倍上界路线的关系

论文页 4 另取 `OPT<=B<=2OPT`，`delta=epsilon/2`，`q=delta B/n`。这条路线在正确 cap 下同样成立：

`OPT_rounded <= OPT+nq=OPT+delta B <= (1+epsilon)OPT`，

`cap=B+nq=(1+delta)B`，

`scaled cap=floor(n/delta+n)`，`L<=floor(n/delta+n)+1`。

原 PDF 写的 `(1+delta/n)B` 太小：`n=2,m=1,p_1=p_2=1,B=2,delta=3/10` 时，`q=3/10`，每任务向上取整为 `6/5`，总负载 `12/5` 超过其 `23/10` cap；修正 cap 为 `13/5` 即容纳。原文的 `n/delta+2` 状态数也随之改为上述正确值。修正不改变固定 k 的 FPTAS 复杂度阶。新边选择前面的初等上界路线，故不从外部引用支取 B 的计算保证。

## 五、困难性及反方向比较

两个相同机器的 `P2||Cmax` 是本模型特例。令每个任务同时可在两机器执行，dual 图是 K2，incidence 图是 `K_{2,n}`，树宽分别为 1 和至多 2。PARTITION 的整数 a_j 作为任务时间、总和 2A 时，makespan 至多 A 当且仅当有和为 A 的划分。因此核心的弱 NP-hard 性有独立的标准两机归约，且和上述 FPTAS 一致。这只是说明核心边界保持有效；本边没有把 M247 的算法性结论误写成困难性来源。

反方向也不能把 M14 的 FPTAS 直接当作 M247 的整条精确 FPT：取 `epsilon<1/OPT` 虽可利用整数目标间隔，但所得 `(n/epsilon)^{O(k)}` 或本轮 `(n^2/epsilon)^{O(k)}` 时间含 `n^{O(k)}`，并不能交付 M247 要求的参数对 FPT 中固定输入次数，尤其不能替代最大资格度路线。没有追加反向整条边。

## 本次对分解与状态语义的独立细化

上述分解搜索可按以下不变量直接核其完备性。状态 `(S,C)` 中 `|S|≤k+1`，C 是 `G-S` 的一个连通分量；询问 `G[S∪C]` 是否有宽度 k、根袋 S 的分解。若边界不紧，即 `N_G(C)⊊S`，先解紧边界 `(N_G(C),C)`，再在上方接回袋 S；反向也可从任一以 S 为根的分解中删去 `S-N_G(C)`，因此此化简等价。紧边界下，所有含某个 C 顶点的袋的并在分解树中连通：C 的每条图边使相应两个顶点的袋子树相交，C 连通后整个并连通。其离根最近的袋 B 是唯一的；对每个 `s∈S=N(C)`，存在一条边 sc、c∈C，所以 s 同时出现于根袋 S 和含 sc 的袋，沿路径必出现在 B。故枚举的某个 B 必含整个 S 且至少一个 C 顶点，并且 `|B|≤k+1`。删除 B 后每个 D 的全部外邻居都在 B，D 是 `G-N(D)` 的连通分量。将原分解限制到 `N(D)∪D` 可得所需子问题，反向把这些分解经 `N(D)` 挂到 B、再挂回 S 即成立。每个递归 D 比 C 小；边界集合与候选袋均只需枚举大小至多 k+1 的顶点集，所以总时间、保存的分解及回溯指针均为 `|V|^{O(k)}`。这明确支付固定 k 的多项式分解入口，不宣称参数 k 的 FPT 识别时间。

对 incidence 的精确目标 T 可行性 DP，使用有唯一 introduce-edge 节点的 nice decomposition。状态的任务位记录该子树已选择的资格边数（只能0或1），机器负载记录该子树已选择边对该机器的处理时间之和。介绍任务/机器时分别初始化0；介绍资格边 ij 时可不选，或在任务位为0时选择并累加 `a_ij`。忘任务强制其位为1；此时它的全部资格边均已在子树介绍。忘机器时所有贡献也已齐全，只需已有负载不超 T。join 两子树介绍的边互不重复，任务位求和并限制至多1，机器负载求和并限制至多T。空根接受时每个任务恰分配一次，且每机器负载不超T；任一合法调度则在每个节点产生这样的状态。每一中间负载是最终负载的非负子和，故 cap 剪枝安全。若零加工时间允许，选边仍把任务位从0置1，任务分配与负载0不会混淆。

宽 w 的每袋状态至多 `2^{w+1}(T+1)^{w+1}`，即使 join 穷举状态对也为 `(T+1)^{O(w)}` 乘仅依 w 的因子。对 `0≤T≤K` 二分并记真实回溯指针，只多一个 `O(log(K+1))` 因子。对 dual 宽 k，用每任务的资格机器团所在袋挂一个 `M(j)∪{j}` 叶袋，incidence 宽至多 k+1；构造不需增加任何资格边。状态中的 K+1 明确包括零负载。

令原输入总位长为 N、精度编码长度为 E。`K=O(n² max{1,1/epsilon}+n)`，上述全部步骤的位运算时间可写成 `(|V|+|E_graph|+K+1)^{O(k+1)} poly(N+E)`；这里图边数不是精度位长 E。对每个固定 k，它对实例长度和 `1/epsilon` 为多项式。每条父指针只存有限状态索引与选择端，恢复时每任务输出一个实际机器标识，共 `O(n log(m+1))` 个输出位，再按原处理时间求 makespan 的位开销也是多项式。此输出保证不是只求一个近似目标数值。

## v3 唯一增量及旧证明继续有效的理由

两精确提交间，body 从 `b2ae90415d0b340c9c0039bf68005854f06b0da4acc35e0f44a22a97d2ebc5ed`（18,718 bytes）变为 `f322df148d7781110aa8b4460adcbcd1cdffbc2f857ca93f5536abefa6f5fa3a`（18,922 bytes）。唯一数学差异是 rankwidth 类型/尺寸计数补含零：

`Π_{h,s}(φ_{h,s}+1) ≤ (n+1)^{κd} ≤ (n+1)^{2^k d}`。

每个坐标 `ι_{h,s}∈{0,…,φ_{h,s}}` 恰有 `φ_{h,s}+1` 个候选值，坐标笛卡尔积给出精确候选计数；后续可行性筛选只会减少它。`φ_{h,s}≤n`，坐标数为κd；cut-rank≤k的 GF(2) 行空间至多有 `2^k` 个向量，所以κ≤2^k。n=1的一类一尺寸已有0和1两种选择，旧 `n^{κd}` 上界确实漏零；固定 k,d 时补正仍为多项式。此次独立核的是这一段与 treewidth 证明互不承重，未声称新核原 PDF Remark20 或未读页的完整 rankwidth DP。

M14/M247 的 model、statement、quantifiers、assumptions、scope、objections、truth_status、evidence 与 sources 均未变，只有 body SHA 与 version 改动。treewidth 的精确负载 DP、上界与舍入/cap 链完全不使用上述 rankwidth 向量计数；其中 `0..K` 本来就有 K+1 个状态。因此应保留所有原有效数学，定向替换 stale 的绑定和覆盖收据。

## 旧 task850 已完成的最小勘误历史


以下为旧 task850 已完成、并由 v3 当前正文完整保留的勘误历史；并非本次提出新的源文修改请求。原 PDF 的冻结字节从未改动，旧文中源文错误与中文转写错误仍分别保留。

1. 中文“基础参数关系”两式及 PDF 页 6 Remark 7。Before: `twp>=max_i|J(i)|`、`twd>=max_j|M(j)|`。After: 两右端都减 1。属于源文错误；单任务单机器图的宽度 0 已反驳原式。源文页 5 本身已正确写最大团大小减一。
2. 中文 dual 段 `L<=OPT` 或 `L<=2max_i|J(i)|`。After: 在负载裁剪目标 T 的 DP 内，`L<=T+1`；最优目标处为 `OPT+1`；另一支为 `L<=2^{max_i|J(i)|}`。指数是中文转写错误，原 PDF 页 4 的指数正确。原文把 OPT 说成全体调度的 load 数界则也必须加裁剪含义与 0 状态，不能作全体调度无条件陈述。
3. PDF 页 4 基础舍入段 `(1+delta/n)B`、`n/delta+2`。After: `(1+delta)B`、`floor(n/delta+n)+1`，并附上一节反例与逐机累加误差。属于源文错误。中文 Theorem 3 原先只概述网格，可加正确 cap/状态数和误差解释。
4. 中文 rankwidth 开头和 PDF 页 12 声称加入 universal job 与只处理该 job 的机器后，primal 和 dual 都是完全图。After: 此构造只使 dual 完全；primal 是原 primal 加一个 universal job 顶点，旧任务间非边仍是非边。原 primal 是新增图的诱导子图，原来无界的 rankwidth 不会因此变成 1。保留 dual 构造与 OPT 相等，删除此构造推出 primal rankwidth=1 的错误断言。属于源文错误；不据此宣称已重审或否定 Theorem 4 的 incidence-rankwidth PTAS。
5. 中文 Lemma 17 的 big-job 网格 `delta^2 B/n`。After: `delta^2 B`。属于中文转写错误，PDF 页 12 没有 `/n`。中文和源文的“至多 `1/delta+1` 种尺寸”也过小；改为至多 `ceil(1/delta^2)+1` 种（含 small clones），仍对固定 epsilon 为常数。big jobs 的 `p_j<=OPT<=B`，网格为 `delta^2B`，直接给出此界。这里只纠正已读前半 Lemma 17，没有展开未读 rankwidth DP。

6. 中文 primal 段的 `M(J_t union Jtilde_t)=Mtilde_t union Mcheck_t`。After: 左侧 `J_t` 改为 `Jcheck_t`。PDF 页 7 Lemma 9(6) 及证明本来就有 check，属于中文漏记号；nearly-inactive 是 active 的子集，原中文式并不表达 inactive 与 nearly-inactive 的机器覆盖。此处是 M232 的直接转写修正，并非本轮新边的前提。

另在已读 source 的承重公式发现三处应由语义补正的排版缺漏，中文概述没有逐式抄入：PDF 页 9 的 nearly-inactive machine 式 `Mtilde_t=Mt minus Mcheck_parent` 应为 `Mt minus M_parent`（等价 `Mt cap Mcheck_parent`）；页 11 incidence `Psi` 的 `J'=A disjoint-union X` 应为 `J' union Jtilde_t=A disjoint-union X`；同页 `Xi(lambda,...)` 应补上左右投影负载和等于 lambda 的约束。它们分别由“在 parent 失活”的定义、将所有 nearly-inactive 任务恰分配一次、以及负载守恒直接强制。上述标准 flag/load DP 也解释了这几个正确语义。此处不重新登记普通修复步骤。

共享正文当前有四个登记 owner：M14、`M-232414c2d8e744ccaba95138638a15dc`、M247、`M-3452046f3bdd47c48b17a0a3038ba4b2`。改 body 全文 SHA 必须刷新四个引用；语义重点是 M14/M247 的舍入与状态、M345 的 rankwidth 旁注/rounding 数字。M232 还直接涉及上一条式 (6) 的漏 check 转写修正；没有声称重新审理其整条 primal FPT 证明。

## 当前交付与资产处置

新边 `um-constant-tw-exact-load-dp-contributes-fptas-c739` 仅由 M247 的明确 `L^{O(k)}` 精确负载 DP 支付 M14 的 FPTAS 算法部分；独立 PARTITION 弱 NP-hard 性继续保在 `contribution.remaining`，不存在整条定理都由算法推出的含义。反向整条 FPT 不成立的比较理由继续记录在 receipt 的 `additional_comparisons`。新任务没有声明 follow-up 配对，本次也未产生新的开放数学义务，故不额外建3B/3C任务、不用 needs-decision 处置纯版本变化。

新 receipt 的 supersession 对旧 edge、review、reading-ledger 三个旧资产逐项 `replaced`，各自指向本任务新目录中的实际 replacement asset。旧完整证明、最小勘误和历史阅读记录由新 review/ledger 继承；旧文件的原字节不变。当前新边交 Root 在真实 clone 中原生 edge-bind/edge-check；最终 edge SHA 应在绑定后写入新 receipt。结构检查不替代本文件的独立数学核验。
