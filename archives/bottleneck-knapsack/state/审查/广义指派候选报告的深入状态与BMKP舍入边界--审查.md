---
id: bottleneck-knapsack/generalized-assignment-candidate-report-deep-boundaries
kind: review
type_tag: 审查
title: 广义指派候选报告的深入状态与 BMKP／舍入边界
status: retained-candidate-review; no-total-theorem
truth_status: candidate-classification-and-conditional-obligations
review_level: full-source-read-cross-compared
scope: "2026-10-20 广义指派八题候选报告；保留 GA-03 两容量 BMKP 的详细候选接口、GA-01 标准推论风险和其余候选的精确边界；不认证总算法、新颖性或公开性"
summary: "完整读取 16,625 字节候选报告并与现有广义指派候选池、双容量 BMKP 三模块／反方审查、Shmoys–Tardos 费用保持舍入和 Santa Claus／拟阵文献对象比较。报告把 GA-03 留为未闭合的两容量 2/3-epsilon 候选，明确联合 critical 恢复、nested short matching、可丢弃 4pmax 舍入各自的条件与总拼接义务；GA-01 因可能是 2026 舍入框架的标准推论降级。"
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:history/retired_topic_selection/independent_review/research/topic_selection/generalized_assignment/candidate_report.md
  - source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:history/retired_topic_selection/independent_review/research/topic_selection/generalized_assignment/candidate_report.md
source_id: be004118450fa3fe0ea5
source_blob: 6d56b9d4dd6b1ca585e944ad115bfa4ea255b94f
source_sha256: db21b1e4542c766da86bf794ea7f520eb6e80f8c10c796713bd5f7ebb13b2742
source_size_bytes: 16625
related_objects:
  - archives/bottleneck-knapsack/state/审查/广义指派候选池的状态与证据边界--审查.md
  - archives/bottleneck-knapsack/state/候选/双容量瓶颈背包的profile标签与完整枚举--候选.md
  - archives/bottleneck-knapsack/state/资料/双容量BMKP候选的三模块与完整目标--资料.md
  - archives/bottleneck-knapsack/state/审查/两容量BMKP候选的独立反方审查与量词边界--审查.md
  - archives/unrelated-machines/state/资源/广义指派的费用保持与加性负载舍入--资源.md
  - archives/unrelated-machines/state/资源/圣诞老人遇到Makespan与拟阵--资源.md
---

# 来源身份与判断层级

冻结来源是 2026-10-20 的重新选题报告，不是证明稿或新颖性认证。`clean show` 实际导出并完整读取了两个冻结定位上的同一文件：16,625 字节，SHA-256 `db21b1e4542c766da86bf794ea7f520eb6e80f8c10c796713bd5f7ebb13b2742`。报告明确声明公开检索的命中或未命中不构成新颖性证明，也没有承诺在固定期限内解决任何候选。它把八条线的模型、目标、母文献入口、首个义务、玩具检查和主动降级放在一个选题记录中；这里把选题优先级与数学真值分开保存。

报告的独有数学去向不是新增一个总算法：GA-03 的联合类型／全局 critical、容量嵌套 short matching、允许弃置的 `4 p_max` 舍入和总算法尚未闭合的具体账目补充既有 BMKP 对象；GA-01 的显式 transversal 切片和标准推论风险补充候选池中的简短状态。GA-02、GA-04、GA-05、GA-06、GA-07、GA-08 的模型和停止条件与现有候选登记相容，未发现可独立升级为定理的内容。

# 八条候选的精确状态

| ID | 输入与目标 | 报告状态及必须保留的边界 |
|---|---|---|
| GA-01 | 显式二部图 transversal matroid，分数 basis、线性 cost、(k) 个 ([0,1]) 行；输出 cost 不增且各行有 Chernoff 尺度误差 | `LIKELY_STANDARD_COROLLARY_PENDING_CHECK`。可能由 2026 face-preserving error-body／cost-preserving discrepancy 框架直接推出；尚未核面保持实现、位复杂度、分布合同和原问题是否要求更强边际。 |
| GA-02 | 公共资源值 (v_j\in\{1,R\})、任意非负指派 cost、严格总预算、允许弃置；目标 (OPT/4) | `BACKUP`。两种值没有消除 small-resource 共享与玩家选择耦合；只列出首个 Pareto-frontier 审计义务，未给算法。 |
| GA-03 | 公共正有理重量／非负利润、容量恰取 ({B_1,B_2})、包数任意、允许 unused；硬容量 ((2/3-\varepsilon)) 目标 | `DEEP_UNREVIEWED`／主候选。联合恢复与三模块局部证明存在，但 profile 导入、全局枚举、位复杂度、边界和实现仍 open。 |
| GA-04 | height-2 weighted laminar matroid、任意元素序、分数 basis、单 cost；所有 weighted prefix 误差为绝对 (Cw_{max}) | `HOLD`。包含 partition 难核；需跨子树 exchange 不随活动块数累加，未提供全域证明。 |
| GA-05 | restricted Santa Claus 的 ((4-\delta)) 多项式近似 | `REJECT_OLD_TARGET`。近期作者／机构公告造成重复风险，但本报告没有取得可审算法；淘汰旧目标不等于认证新算法。 |
| GA-06 | 每件 item 至多两个 eligible bins 的 offline max-GAP，硬容量，目标 (0.76OPT) | `HOLD`。独立抽样两箱 toy 只有 (3/4)，matching 可恢复更高值；小例不是全域保证。 |
| GA-07 | unit bins、公共 sizes、bin-dependent profits、all-or-nothing groups，组总 size (le m/2)，目标 (1/5) | `BACKUP`。母结果为 (1/6)，reserved-capacity 子问题与最终舍入的同时改善尚未证明。 |
| GA-08 | random-order online max-GAP，不可撤销，硬容量，期望 (0.16OPT) | `HOLD`。母基线约 ((1-\ln2)/2)，新 stopping-time／剩余容量概率义务未完成，不能与 offline 近似混写。 |

这些状态是研究决策标签。它们不证明候选开放、不证明候选困难、也不证明被列为 HOLD 的模型没有更好算法。

# GA-03：两容量 BMKP 的具体候选接口

模型是中央 bottleneck 多背包：每件物品有公共正重量 (w_e) 和非负利润 (p_e)，每个箱容量为 (B_1) 或 (B_2)，容量比和箱子数均无固定界；每件至多使用一次且允许 unused，最大化全部箱的最小利润。候选目标是固定 (arepsilon>0) 时给出输入位长多项式、硬容量的 (2/3-arepsilon) 近似。它没有玩家、偏离、延迟或纯 SPE 量词，不能并入 customer-attraction 或拥塞对象。

报告保留了以下三项条件模块。第一，**联合 critical 恢复**：两种容量各自产生 profile／上舍入标签，并把容量状态、上舍入重量、利润桶和 heavy 标志组成全局 joint type；每个 type 按两种容量下 long 槽的总需求选择全局最重 critical 物品。容量分开选“最重”可能重复原物品，只有全局联合需求的交换保证互不交；被 short 或 unused 的较轻物品可放回，重量不增而每个利润桶损失小于一个桶宽。该交换只在 profile 的自代表、有效状态和 long/short 前提真实成立时有效。

第二，**嵌套 short matching**：对未占 critical 的昂贵池加 zero dummy；能放进大容量的二物品边权为 0，能同时放进小容量的边权为 1，要求固定总 matching 基数且小边数至少为小箱数。固定基数最大权二部匹配等价于全部 short 的 singleton/pair 分配，因而不需要一般的 Exact Matching。该论证依赖正的 short 目标 (Q>0) 来排除 dummy-dummy，并不生成 profile 或保证昂贵物供给存在。

第三，**允许弃置的 (4p_{max}) 舍入**：对满足 (sum_jx_{ej}\le1)、逐箱硬重量和利润下界的 LP，残余极点中的正分数边数 (E)、紧物品行数 (N)、未完成箱数 (M) 满足 (N\le E/2)、(E\le N+2M)，故 (E\le4M)。逐步结束一个箱至多丢四条分数边，得到容量不增、每箱利润损失至多 (4p_{max}) 的部分整数解。允许丢弃是必要条件：一件重量二的物品、两个容量一的箱和各取一半的分数解否定“所有物品必须恰覆盖一次”的过强合同，但不否定 BMKP 主目标。

候选的参数账目为

[
\zeta=1/\lceil\max(100,20/\varepsilon)\rceil,\quad U=1-\zeta,\quad \gamma=U\zeta,\quad \delta=U\zeta^2,\quad K=1/\zeta,
]
[
q_{pre}=2/3-8\zeta,\qquad Q=2/3-11\zeta.
]

其预想流程先以单向阈值 (T) 归一并 cap 利润，再在各容量实例中删除至多一个 heavy-cheap 物品以获得 profile；最后枚举两个 profile、joint-type critical 数、long 配置重数，使用 matching 恢复 short，cheap 池用允许弃置的 LP 舍入。若枚举轮真实命中全部合法 profile、供给和数量见证，报告账目给 long 至少 (Q-4\zeta)，再经 (1+\zeta) 几何网格达到 (2/3-16\zeta\ge2/3-\varepsilon)。这只是“命中见证则输出”的条件结论。

总算法尚未闭合的义务必须同时保留：母文 profile/Lemma 8 的前置利润与 heavy-cheap 条件逐式导入；joint type 的全局可计算性和数量只依 (arepsilon)；profile 自代表、零尺度、无效标签、空 long／short 和零利润边界；全部枚举轮的联合覆盖；未知 (OPT) 的单向 oracle 与有理网格位复杂度；两池物品不抢、昂贵项规范化后的不变量；以及通用实现。报告的 3,000 个 joint Fraction 实例、4,927 次交换和 8,192 个 short-pair 穷举只验证局部合同，不能替代上述全域证明、近似保证或新颖性认证。

这部分与既有《双容量 BMKP 候选的三模块与完整目标》《双容量瓶颈背包的 profile 标签与完整枚举》和独立反方审查互补：既有对象承接最终参数与反方修正，本报告新增的是八题报告中对联合恢复、short matching、(4p_{max}) 舍入的候选语义及总算法义务的集中陈述。不得把它们合并成“模块合取即总定理”。

# GA-01：费用保持舍入切片的降级边界

报告的 GA-01 不是任意 matroid 的已证算法。其切片要求输入显式 transversal graph、fractional basis (x\in P(M))、有理 cost (c) 和 (k) 个 ([0,1]) 行 (a_r)，输出一个 basis，保持 (c(B)\le c\cdot x)，并以常数概率使所有行误差达到 (O(\log(2k)+\sqrt{(a_r\cdot x)\log(2k)}))；不要求精确边际。报告提出 strong base-ordering 的互补 merge，且以 rank-3 transversal（17 bases、136 对）和 (K_4) graphic 边界区分“显式可构造”与“任意 graphic matroid”。

但仓库已有 Shmoys–Tardos 资源对象只证明 generalized assignment 的最小费用槽匹配可保线性费用并给加性负载界；它不是 matroid basis 的 Chernoff 行误差，也没有把成本保持迁移到报告所需的 face-preserving 误差体。报告同时记录 2026 的 face-preserving discrepancy／error-body 框架可能直接给出所需结论，故将 GA-01 降为 `LIKELY_STANDARD_COROLLARY_PENDING_CHECK`。仍需核对 face 保持、均值依赖半径、位复杂度、分布和原 open 是否要求更强合同；在核验前不能以 toy 通过或论文 open 位置写成新定理。

# 全仓比较、来源边界与接续

* `广义指派候选池的状态与证据边界--审查.md` 已从 `candidates.json` 整理八题状态。本源是同一候选池的深入报告版，补充 GA-03 的具体账目和 GA-01 的降级依据；不是八题的第二套互相矛盾状态。
* BMKP 的三模块、profile 候选和反方审查已经保留两容量模型、最终参数、可弃置边界和未闭义务。本源不改变其 candidate／open 身份，也不重新引入旧 (6\zeta/13\zeta) 参数。
* `广义指派的费用保持与加性负载舍入--资源.md` 的 Shmoys–Tardos 定理是任务不可拆分、机器负载和线性费用的 assignment LP 舍入；它不能证明 BMKP 的 max-min 利润、GA-01 的 matroid Chernoff 行界或当前六人 SPE。
* `Santa Claus 遇到 Makespan 与拟阵--资源.md` 给明确 restricted two-value resource/job matroid 归约和 (T\pm\max) 单项的 LP 舍入，但其 basis／polymatroid 和玩家福利量词不同；它不能把 GA-02 的严格总预算 (OPT/4) 或 GA-05 的旧目标直接升级。
* customer-attraction、weighted-congestion、facility 和其它存档的玩家历史／均衡／势函数对象都与本报告的中央 assignment/BMKP 优化保持独立。没有发现可无条件迁移的证明边。

玩具脚本、参数网格、作者／会议开放位置和候选排序的证据层级分别是有限检查、研究线索和选题判断；均不能替代数学证明。报告本身没有完成第三阶段超图关系，后续只宜建“候选补充”“条件模块”“有限证据”“标准推论待核”“来源／方法背景”关系，不建无条件“已证明”边。

**处置建议：`integrated`。** 将本源的八题精确状态与 GA-03／GA-01 独有边界并入本审查对象或新增补充审查对象；保留冻结源 SHA 和两个来源提交。与既有候选池和 BMKP 三模块对象的重复段落在回执中说明，不能将其当作新定理或重复计数。父任务在正式 checkpoint 后，才可据此提交该源的逐项 `done`。
