# 精确负载 DP 到有界 dual/incidence 树宽 FPTAS 的比较

## 身份、边界与阅读

本包核心为 `M-14dbe6980117492aa7a3b48c52378dcb`（常数 dual 或 incidence 树宽 FPTAS 与弱 NP-hard 性），共享比较对象经 Root 原生 read-add 后为 `M-247deecec83946358afe4e89413a7bd1`（双参数精确 FPT，明确保存 `L^{O(k)}O(nm)` 的负载 DP 复杂度）。两者均为整数 `R||Cmax`，有限端表示真实资格，任务不拆分，目标为每机所接任务处理时间之和的最大值。不是 restricted assignment 专用结论，不假定不同机器上的同一任务尺寸一致。

实读两对象的完整当前 model、statement、quantifiers、assumptions、scope、objections、body、evidence 和来源元数据；完整阅读共享中文正文。原 PDF 实读页 1–11（标题、模型、近似/FPT 定义、Theorem 1–4、Section 2 的两个 DP 与舍入、树宽定义、三种树宽动态规划及 Theorem 3 的证明入口），另实读页 12 的 rankwidth 开头与 Lemma 17 前半部。视觉核公式页 4、6、9、11、12。没有把页 13–19、全部 rankwidth DP 或论文引用的 LST/树宽识别外部论文算作本轮完整重证。

原中文 SHA 为 `a842380d2ee484db652986c5d639fb5c1651cc7ca77dff67bac5e898381f4a85`；原 PDF SHA 为 `4b47eaccfcffe81f6713522269b6afa2124bec3d619d6ef3a1b5341db7e48bae`。原 PDF 字节保持不动，发现的源文错误与中文转写错误分开列出。Root 负责共享 source 修正与引用刷新；本 worker 只写仓库外 staging。

本轮以 registry 的 canonical 清单逐个只读扫描 1,962 个边文件的端点，未发现 incident 上述任一对象的现有 canonical 边；也没有可按原 SHA 复用的同一比较。只比较这一精确 DP/FPTAS 对，不由共享模型建立 hub。

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

## 六、最小勘误与受影响路由

以下先/后是给 Root 的可直接应用最小改法。原 PDF 冻结不改；中文正文标明原文笔误，不能默默说原论文原式已正确。

1. 中文“基础参数关系”两式及 PDF 页 6 Remark 7。Before: `twp>=max_i|J(i)|`、`twd>=max_j|M(j)|`。After: 两右端都减 1。属于源文错误；单任务单机器图的宽度 0 已反驳原式。源文页 5 本身已正确写最大团大小减一。
2. 中文 dual 段 `L<=OPT` 或 `L<=2max_i|J(i)|`。After: 在负载裁剪目标 T 的 DP 内，`L<=T+1`；最优目标处为 `OPT+1`；另一支为 `L<=2^{max_i|J(i)|}`。指数是中文转写错误，原 PDF 页 4 的指数正确。原文把 OPT 说成全体调度的 load 数界则也必须加裁剪含义与 0 状态，不能作全体调度无条件陈述。
3. PDF 页 4 基础舍入段 `(1+delta/n)B`、`n/delta+2`。After: `(1+delta)B`、`floor(n/delta+n)+1`，并附上一节反例与逐机累加误差。属于源文错误。中文 Theorem 3 原先只概述网格，可加正确 cap/状态数和误差解释。
4. 中文 rankwidth 开头和 PDF 页 12 声称加入 universal job 与只处理该 job 的机器后，primal 和 dual 都是完全图。After: 此构造只使 dual 完全；primal 是原 primal 加一个 universal job 顶点，旧任务间非边仍是非边。原 primal 是新增图的诱导子图，原来无界的 rankwidth 不会因此变成 1。保留 dual 构造与 OPT 相等，删除此构造推出 primal rankwidth=1 的错误断言。属于源文错误；不据此宣称已重审或否定 Theorem 4 的 incidence-rankwidth PTAS。
5. 中文 Lemma 17 的 big-job 网格 `delta^2 B/n`。After: `delta^2 B`。属于中文转写错误，PDF 页 12 没有 `/n`。中文和源文的“至多 `1/delta+1` 种尺寸”也过小；改为至多 `ceil(1/delta^2)+1` 种（含 small clones），仍对固定 epsilon 为常数。big jobs 的 `p_j<=OPT<=B`，网格为 `delta^2B`，直接给出此界。这里只纠正已读前半 Lemma 17，没有展开未读 rankwidth DP。

6. 中文 primal 段的 `M(J_t union Jtilde_t)=Mtilde_t union Mcheck_t`。After: 左侧 `J_t` 改为 `Jcheck_t`。PDF 页 7 Lemma 9(6) 及证明本来就有 check，属于中文漏记号；nearly-inactive 是 active 的子集，原中文式并不表达 inactive 与 nearly-inactive 的机器覆盖。此处是 M232 的直接转写修正，并非本轮新边的前提。

另在已读 source 的承重公式发现三处应由语义补正的排版缺漏，中文概述没有逐式抄入：PDF 页 9 的 nearly-inactive machine 式 `Mtilde_t=Mt minus Mcheck_parent` 应为 `Mt minus M_parent`（等价 `Mt cap Mcheck_parent`）；页 11 incidence `Psi` 的 `J'=A disjoint-union X` 应为 `J' union Jtilde_t=A disjoint-union X`；同页 `Xi(lambda,...)` 应补上左右投影负载和等于 lambda 的约束。它们分别由“在 parent 失活”的定义、将所有 nearly-inactive 任务恰分配一次、以及负载守恒直接强制。上述标准 flag/load DP 也解释了这几个正确语义。此处不重新登记普通修复步骤。

共享正文当前有四个登记 owner：M14、`M-232414c2d8e744ccaba95138638a15dc`、M247、`M-3452046f3bdd47c48b17a0a3038ba4b2`。改 body 全文 SHA 必须刷新四个引用；语义重点是 M14/M247 的舍入与状态、M345 的 rankwidth 旁注/rounding 数字。M232 还直接涉及上一条式 (6) 的漏 check 转写修正；没有声称重新审理其整条 primal FPT 证明。

当前命中任务：本 task 850a6179151b732e；777902a1e6f15125（claimed/Boss2，命中 M14 只读依赖，Root 核范围）；9a5cd2eb99c8ff5a（available，M247）；d97d472e04065fc5（available，M345）；effdbb6d60f56b34（available，M232）。canonical 扫描时四者均无 incident 现边；这里只要求刷新有效任务与实际命中引用，不扩展成共享源全仓重审。

## 交付判断

一条 accepted、unconditional、ALL 的 proof-step contribution：M247 的明确负载 DP，经本轮完整上界/整数化/误差/位复杂度/回溯说明，给出 M14 的 FPTAS 部分；独立弱困难性留在 contribution.remaining。没有本 task 原声明的 follow-up 配对，没有发现需要发布 3B/3C 的开放数学缺口。反向整条精确 FPT 推导未获支持的理由作为已完成比较写入 additional_comparisons，不填 closed_overlaps。来源勘误与引用刷新是同包定向修复，不伪装成新的研究开放问题。

## 最终当前版本核对

Root 已串行发布本轮 source 勘误与引用刷新。本 worker 对照已读原正文和全部最小补丁核对新 source；本轮边交 Root 按新记录作原生绑定：

- 当前中文 body SHA：`b2ae90415d0b340c9c0039bf68005854f06b0da4acc35e0f44a22a97d2ebc5ed`。
- M14 当前 version 2、pin `2e991ac64d1bc297760daccd30f713ae70c2bdaa42bb3e54a02ae554563a4e86`。
- M247 当前 version 2、pin `fd687a135427e3d9654468452b5db3a8279a4f60bfa41d99904b9d214a241a41`。
- 原 PDF 字节保持原 SHA，阅读范围仍是上文如实列出的范围，没有把共享 source 更新冒作未读 rankwidth 全证明复审。
