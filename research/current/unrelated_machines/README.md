# 不相关并行机：突破统一常数2壁垒的研究地图

当前存档为 `unrelated-machines`。本轮新主攻是 `UM-TARGET-v1`：一般二进制有理输入R∥C_max上，构造确定性位多项式时间、统一常数(2−ε)近似。目标仍OPEN；未形成新算法。新 boss 先读[BOSS研究总览与路线分诊](../../unrelated_machines/BOSS_RESEARCH_BRIEF.md)，再按选定承重义务进入本地图。旧拥塞/设施研究保留原身份，不作为本题数学依赖。

新阶段边界见[长链替换与固定机器联合投影](long_path_coalition_gap.md)：经典gap可移到任意大围长的简单机器图；只共享单机边际的固定大小联合见证仍有sup gap2。完整多机交叠相容性不在该否定范围，且三机完整相容性已能解决这批树宽2反例。完整证明、独立攻击和有限核验分别登记，未声称原创算法或全球新颖性。

先读[协作入口](../../unrelated_machines/README.md)与[精确账本](../../unrelated_machines/CLAIMS.md)，再读[模型、舍入与配置间隙的自足重构](model_and_classical_barriers.md)。[文献清单](../../unrelated_machines/literature_manifest.json)区分已取得原文、已核结果和待处理来源。[当前前沿](../../unrelated_machines/RESEARCH_STATE.md)说明下一步需要完成什么。
本轮方向审计见[team_direction_audit.md](../../reviews/unrelated_machines/team_direction_audit.md)：已有资产主要关闭局部合同，任意输入的共同容量桥仍是唯一主轴。

| 定义/Claim | 内容与真实状态 | 依赖和作用 |
| --- | --- | --- |
| UM-MODEL-v1 | 非负有理、不可用边、不可拆分、全部任务必须安排 | 目标、LP与所有算法共同合同；含零最优值 |
| UM-TARGET-v1 | ∃统一ε>0，∃确定性位多项式算法，∀输入输出≤(2−ε)OPT | 开放研究目标；m不能固定，不能用估值代替调度 |
| UM-ST-ROUND-v1 | 给定剪枝LP可行x，槽匹配输出L_i≤fractional load+support max≤2T | 已知结果自足重构；Hall与非增排序；程序仅实现此舍入接口 |
| UM-CONF-GAP-v1 | 配置LP的sup gap=2，甚至每任务两台可选机器 | 两树构造、递推配置证书＋整数下界＋舍入上界；阻止纯粹相对配置值的统一改进 |
| UM-LONG-PATH-GAP-v1 | 任意给定围长下，简单机器图配置gap仍sup2 | 经典两树＋长链阈值保真；[正文](long_path_coalition_gap.md)、[独立审查](../../reviews/unrelated_machines/long_path_coalition_review.md) |
| UM-COALITION-PROJECTION-GAP-v1 | 任意固定r的单机边际相容联合投影仍sup gap2 | 高围长族＋森林耦合；不含全交叠一致性；完整三机相容性在本族精确 |

真实依赖是模型→LP定义→配置边际投影→经典舍入上界；模型→两树族→整数下界与配置可行性→gap下界→与上界合成gap=2。gap只限制一个下界/舍入合同，不推出主目标为假。有限核验只检查所列参数。

研究路线是种子：可以探索跨机器兼容性、更强松弛、组合下界、局部搜索/交换结构、新表示及复杂度归约。每条路线先写精确义务与它如何绕过已知gap；不要求服从固定方法清单，也不要求先完成全领域综述才能检验一个有信息价值的想法。

| 文件 | 数学资产及何时读取/修改 |
| --- | --- |
| research/current/unrelated_machines/model_and_classical_barriers.md | 精确模型、全量词目标、零值边界、槽舍入完整证明、重索引gap构造与障碍准确范围；引入新工具或算法前核对合同 |
| research/unrelated_machines/CLAIMS.md | 逐命题身份与认知层；改假设或结论须新版本 |
| research/unrelated_machines/LITERATURE.md、literature_manifest.json | 文献结果、版本、取得状态、定理位置与PDF哈希；使用外部定理时查原文 |
| research/unrelated_machines/RESEARCH_STATE.md、FAILED_ROUTES.md | 当前未闭合义务和已知障碍；新候选出现时更新，不记录普通流水账 |
| tests/audits/unrelated_machines/rounding_and_gap.py | Fraction舍入、枚举oracle、显式配置证书、特定树族DP；算法或构造变更时运行 |
| evidence/runs/unrelated_machines/classical_baseline_audit.json | 初始有限核验冻结记录；重跑输出到scratch，不覆盖原记录 |
| research/questions/unrelated_machines/barrier_escape_obligations.md | 新算法必须跨过的下界/构造/复杂度义务；具体路线产生后细化 |
| research/unrelated_machines/BOSS_START.md | 可复制到新对话的完整启动提示词；恢复、存档路由、研究与保存要求 |
| research/current/unrelated_machines/long_path_coalition_gap.md | 高围长gap运输、CC_r精确定义及全交叠相容性逃生口；提出局部强化前先核对范围，沿正文进入双路代码/输入/证书/冻结证据 |

## 新增的匹配残余路线与准确边界

[大边匹配残余、简单支撑与共享逃逸容量](heavy_matching_residual_and_escape.md)给出三个新限范围身份：`UM-HEAVY-MATCH-FILTER-v1`安全位多项式过滤、`UM-SIMPLE-SUPPORT-GAP-v1`简单支撑配置gap、`UM-ESCAPE-MATCH-GAP-v1`共享小端容量方法反例。主目标仍OPEN；不是统一低于2算法，未认证全球新颖性。读取顺序：精确账本→正文§1–5→冻结审查→两路代码/证据。真实依赖为模型/经典两树→路径终端配置与整数计数→逃逸族；匹配安全性单独依赖逐次删边与任务权增广。有限核验仅为checks。

| 新长期文件 | 内容、作用及读取条件 |
| --- | --- |
| research/current/unrelated_machines/heavy_matching_residual_and_escape.md | 全量词安全过滤、总位复杂度、三层瓶颈/反例；设计匹配或跨机器容量候选时读 |
| research/reviews/unrelated_machines/heavy_matching_escape_review.md | 独立先重构后冻结攻击，实际hash、边界及未解决义务；引用新Claim前读 |
| tests/audits/unrelated_machines/heavy_matching_residual.py | 任务权匹配、过滤固定点、显式路径/逃逸配置及小矩阵枚举 |
| tests/audits/unrelated_machines/ghmr_independent.py | 不同实现的matching oracle、独立证书与压缩容量DP；交叉核对而非一般证明 |
| evidence/runs/unrelated_machines/heavy_matching_residual_audit.json、heavy_matching_escape_independent.json | 两路实际参数、代码hash与有限结果；重跑写scratch，不覆盖 |

## 计数传播与跨机器相容性接口

[成束任务的二阶相容性、计数传播与细分障碍](bundle_coupling_subdivision_barrier.md)给UM-BUNDLE-MOMENT-v1、UM-CARDINALITY-CLOSURE-v1、UM-PAIR-SUBDIVISION-GAP-v1。原VW族可被二阶相容性或健全计数传播识别；细分保持整数OPT、提升分数证书，令简单图上的完整pair coupling仍sup gap2。新目标不是反复切旧族，而是跨中间容量机器的信息保持与可构造性。

读取链：本题账本→正文→[冻结审查](../../reviews/unrelated_machines/bundle_subdivision_review.md)→规范计数/耦合及不导入核心的独立审计→[完整冻结记录](../../../evidence/runs/unrelated_machines/bundle_subdivision_audit.json)。主目标继续OPEN，新颖性/外审未认证；同存档boss4的长链推广是独立重叠发现，不再把长度2变换当独占新家族。

## 共同匹配选择与条件块容量

[共同大边选择、小边补全及块切面](joint_matching_completion_and_block_cuts.md)明确三个身份：UM-JOINT-SMALL-ROUND-v1给定H,x输出(3/2+δ)T；UM-JOINT-CHOICE-NP-v1证明固定有理δ<1/3的精确选择NP完全，连N空/每job唯一small也成立；UM-ESCAPE-BLOCK-CUT-v1则通过随B变化的末簇条件切面，把整个共享逃逸族的强化阈值恢复为真实OPT。均已独立重构/冻结攻击，外审与新颖性未认证。

读取顺序：本题精确账本→正文§1合同/§2条件舍入/§3限域复杂度/§4限族切面→joint_matching_completion_review.md→joint_matching_completion_audit.json及其三份实际审计代码。原始Karp重印源的版本/hash与读到的位置见manifest；没有把下载说成完整源证明重构。

下一义务已被半单位扩展修正：固定δ<1/2的(Aδ)承诺搜索在P≠NP下均不可能；应转向实际槽损失或可分离/可舍入的条件块强化，仍无统一新算法。文件入口完整路径为research/current/unrelated_machines/joint_matching_completion_and_block_cuts.md、research/reviews/unrelated_machines/joint_matching_completion_review.md、tests/audits/unrelated_machines/{joint_matching_completion,unique_small_matching_audit,joint_matching_completion_independent}.py及evidence/runs/unrelated_machines/joint_matching_completion_audit.json；新候选必须同时攻击共享z、长链与一般多小端输入。

新增失败路线见[固定工作量与中任务配置分解边界](../../questions/unrelated_machines/fixed_work_and_medium_config_barriers.md)：固定阈值的“配置 LP 加 tiny 槽损失”在 α<1/5 时退化为经典配置间隙；固定总工作量和固定非减凸分离势也会被私有昂贵叶族锁在近二。该页只排除所列合同，重开边与自适应共同势仍是开放方向。

[生成树再耦合的五机反例](tree_markov_completion.md)进一步定位算法接口：即使pair来自真实全局最优分布，任意tree-Markov态冻结树任务后仍可能只可补到2T；一步迁移可修复此例，不排一般repair。状态见UM-TREE-MARKOV-COMPLETION-NO-v1及正文链接的独立审查/双路证据。

## 可恢复消元与共享容量一资源

[极小超载星消去、容量一资源竞争与普通任务压缩边界](minimal_star_contraction_and_capacity_gap.md)：UM-MINIMAL-STAR-CONTRACTION-v1保T可行性，任何新调度B可提升≤max(B,T)；可以消去前一阶段的中间机器。紧凑资源族却让本消元、计数闭包及一般完整pair coupling合用仍gap2（UM-CAPACITY-ONE-PAIR-GAP-v1）。boss4提供的UM-STAR-Q-JOB-COMPRESSION-NO-v1进一步说明q≥2外溢不能用q个独立普通任务保全部残余容量。

读取链：精确账本→新稿第1节恢复算法→第3–5节准确失败范围→[独立冻结审查](../../reviews/unrelated_machines/minimal_star_capacity_review.md)→实际代码/冻结证据。原始BLMRS2024的取得、机制重构和未读全证明单列manifest。一般匹配身份接口及统一近似仍OPEN。


## 逐边线性探针与配置证书仍缺共同条件容量

[稀释终端正文](diluted_sink_probe_gap.md)给出新的严格合同边界：N=k(k−1)个终端与N−1个单位阻塞任务保持整数一槽，却让全部边分别强制为1的LST点利用NT−k=N−1分数余量。因此配置可行＋全部线性边探针＋局部星匹配仍sup gap2。它不否定GHMR、更强条件LP或UM-TARGET-v1。把大任务基数放入每个探针内部就能准确识别此族，说明额外约束必须在条件内共同守容。

| 入口 | 何时读取 |
| --- | --- |
| research/current/unrelated_machines/diluted_sink_probe_gap.md | 设计逐边条件LP时先核对独立证书与共同条件约束的差别；含完整族、算法合同、位复杂度及精确范围 |
| research/reviews/unrelated_machines/diluted_sink_probe_review.md | 引用三项局部结论前核对冻结哈希、独立攻击和C有理编码修补 |
| tests/audits/unrelated_machines/diluted_sink_probe_gap.py、independent_dilution_audit.py | 重跑实际稀疏配置与条件点；主全边和独立抽样覆盖严格分开 |
| evidence/runs/unrelated_machines/diluted_sink_probe_gap_audit.json、independent_dilution_audit.json | 查真实参数、算术、源哈希和未核验范围；不覆盖冻结结果 |


共享小端扩展见同稿第11节（UM-DILUTED-ESCAPE-PROBE-GAP-v1）：全部普通LST边探针、现行GHMR、配置和星匹配可同时接受而OPT/T趋2；准确引用boss3共享机制。新增边后下界已重证，双路实际核验已审；条件块切面仍可见此共享容量，主目标未解。

[半单位全窗口扩展](joint_matching_completion_and_block_cuts.md)§3a（本数学目录同名正文）另立UM-JOINT-HALF-CHOICE-NP-v1及UM-JOINT-HALF-PROMISE-NO-v1：唯一small、时间{1/2,1}使(Aδ)在所有δ<1/2等价OPT≤1，关闭先前列出的共同见证窗口。旧1/3版原身份保留；δ=1/2及其他舍入合同不被排除。冻结审查和两份独立审计从正文进入。

## 全局基数探针后的共同负载瓶颈

[全局单行基数匹配与紧凑共享逃逸](row_count_escape_gap.md)给UM-GLOBAL-ROW-COUNT-FILTER-v1与UM-COMPACT-COUNT-ESCAPE-GAP-v1。固定全行下界时无需枚举资源子池；但紧凑族有每机avoid证书，连任意单机配置都可延伸成全局计数见证，GPC₂仍T1可行而OPT=2−1/k。读取顺序：精确账本→正文§1合同/§2–4证明→row_count_escape_review.md→row_count_escape_audit.json与三份审计代码；实际k2输入/配置/达到调度也已保存。

失败点是把真实超载移到当前未精确查询的其他中心。条件块cut直接适配能修本族，不另宣称新成果；下一义务是一般可分离的共同负载/条件容量及统一舍入，不再只优化逐机最大卸载值。外审与全球新颖性未认证，主目标仍OPEN。

[直接联合槽的正面衔接](joint_slot_prefix_rounding.md)给UM-ROW-SPREAD-TWO-ROUND-v1：删去零任务后每行正时间跨度≤2（逐机尺度不同）时，显式前缀计数LP加一次全任务槽匹配给3/2位多项式构造。它是VW/ST已知机制的直接推论，绕过过强(Aδ)见证；未消除一般行内跨尺度混合，主目标仍OPEN。

## 稀疏全边条件配置的准确边界

[三选稀疏深树与微小共享逃逸](sparse_conditioned_configuration_gap.md)给UM-SPARSE-CONDITIONED-CONFIG-GAP-v1：每k≥3、每任务至多三选，OPT=2−1/k；T=1+1/k下每条有限边分别有x_ij=1完整配置证书，因此独立配置探针和基数LST删边均无起点。不同查询不共用相关性是实质缺口；完整四机器bag在整个交集的联合分布一致可精确拼接本族。路径端点可触发极小星，未覆盖预处理后的合同。

读取链：精确账本→自足稿→sparse_conditioned_configuration_review.md→sparse_conditioned_configuration.py及独立程序→实际稀疏输入、最高逃逸配置/调度证书、sparse_conditioned_configuration_audit.json。主目标仍OPEN；此为条件松弛的方法边界，不是一般近似困难性。

紧凑共享逃逸正文§6另给UM-COMPACT-MULTIROW-EXTENSION-v1：任意U含至多N−2k个中心时，每个单机配置均可延伸并让U全部机器同时守真实容量；N−2k+1中心加z空pin有明确失败。故“更多独立行见证”仍缺共同相关性，尖锐预算和实际构造不改变主目标OPEN状态。

## 完整单机配置探针的精确新边界

UM-MACHINE-CONFIG-PROBE-GAP-v1复用紧凑N=2k²族，T1时每机器每个合法完整C分别有y_iC=1的完整配置LP延伸，OPT=2−1/k。它不要求共同base或条件pair相容；(MP)本身不是整数可行必要条件，仅安全删失败配置。读取链：专题CLAIMS→row_count_escape_gap.md§7→machine_config_probe_review.md→compact_config_probe.py与compact_config_probe_independent.py→compact_config_probe_audit.json。双路实际有限核验与一般证明分开；共同逃逸一阶矩可恢复旧块cut，主目标OPEN，外审/新颖性未认证。

## 真实最优凸包仍会丢失于固定槽图

[真实最优凸包与固定有序槽图](optimal_convex_fixed_slot_gap.md)给UM-OPTIMAL-CONVEX-ST-SLOT-GAP-v1：完全相同机器上也可有显式OPT1的全局凸分解，而由平均x生成的每一个槽匹配都逼近2OPT。每机槽数饱和强制平衡任务数，排除了好整数分量。不是配置gap；更强x或在同图里择优均不足，本族却有一轮最优跨槽修复。主目标仍OPEN。

读取链：本题账本→正文→optimal_convex_slot_review.md→optimal_convex_slot_gap.py及独立审计→optimal_convex_slot_gap_audit.json；输入及显式凸分量/匹配证书由正文链接。下一义务是改变联合槽容量/保留配置相关性或给一般repair，不能将本例升级为算法困难性。

## 循环批量修复与真正的分流义务

[循环批量修复与分流合流障碍](cyclic_batch_repair_and_fork_obstruction.md)给三个准确身份：固定η的总位多项式局部优化器，常数单机迁出数的真实OPT障碍，以及唯一最小成本LST槽分配仍须多目的地分流的padding族。程序允许任意批量和循环长度，成功轮数≤4m/η，但局部终态没有统一近似保证。反例所用x违反配置大任务基数，未排配置投影/选基本点/换支撑。读取链：本题Claim→正文§2–4算法/§5–7边界→冻结审查→规范实现与独立审计、实际k2输入/槽证书与运行记录。标准图搜索和背包缩放扣除后的全球新颖性、独立论文价值未认证。

身份：UM-ROBUST-CYCLIC-BATCH-OPT-v1, UM-BATCH-SUPPORT-REPAIR-NO-v1, UM-FORK-MINCOST-ROUND-REPAIR-NO-v1。

[UM-OPT-HULL-LONG-CHAIN-LOCAL-GAP-v1：真最优凸包长链修复](cyclic_batch_repair_and_fork_obstruction.md#10-真实最优凸包初始化后的无界机器长链义务)把参与机器数的义务与单机批量分开：所有mincost槽输出值2−1/k，严格lex改善恰需d+1任务/d+2台机器。两个真实最优分量、实际槽图、双路证据与[冻结攻击](../../reviews/unrelated_machines/optimal_hull_long_chain_review.md)可追溯；允许先中性腾空链尾即有逐件弱Cmax修复，不是一般算法障碍。

## 联合迁移的需求树压力接口

[有向需求树与真实调度的精确任务桥梁](rooted_dag_degree_token_bridge.md)给UM-DAG-DEGREE-TOKEN-IDENTITY-v1及UM-TARGET-IMPLIES-DAG-DEGREE-v1：一顶点一机器、unit入任务与本地子任务外溢，精确OPT=2−截断最大需求比例；二进制大需求用单填充保持任务数O(E+V)。正确阈值缩放使任何主目标算法都须构造常数比例需求根树。一般方向已由MMDA/Santa Claus文献知道，本页是可复用直接重构，不冒充新算法/新困难性。

读取链：本题账本→正文§1合同/§2–5构造及位复杂度→rooted_dag_token_bridge_review.md→rooted_dag_token_bridge.py及独立审计→rooted_dag_token_bridge_audit.json。原始Bamas2025 v2字节与定义/脚注位置见manifest；一轮SA定理只核对陈述，未转成调度层级结论。

新增派生UM-COORDINATE-REPAIR-ST-GAP-v1（循环批次正文cyclic_batch_repair_and_fork_obstruction.md§9）：与boss7真实最优凸包固定槽族衔接，工作量守恒使本逐坐标优化器仍0轮且gap→2。这个限制已覆盖配置来源；它不扩大fork关于one-destination、makespan非增的另一合同。下一机制必须允许低负载接收机上升并共同控制最大负载，不能把更强初始化单独当成循环算法的补丁。

## 固定最优边际断点与单边界批量恢复

[UM-OPT-HULL-ROW-DISCREPANCY-GAP-v1及UM-OPT-HULL-PAIR-NC-GAP-v1](optimal_hull_marginal_rounding_barrier.md)：x本是真实OPT显式平均，固定row/count仍sup2；同sink pair-NC的期望和尾界均尖锐。不是配置gap或主目标困难性；正文§9→optimal_hull_marginal_review.md→三路审计/冻结证据及k2r4实际输入/概率证书。

[UM-FOREST-BOUNDARY-AUGMENT-v1](forest_boundary_contraction.md)：给定唯一boundary、内部无外接的森林，任意批量父包knapsack给b≤b*(T)、内部≤(1+η)T；用根单端任务恢复max(B,(1+η)T)，每次删机器的重复消元不按深度累计。正文→forest_boundary_contraction_review.md→upward/downward两算法及冻结范围。已知结构DP机制背景见JMS2017 manifest，不认证新颖性。

仍缺一般多边界/有环核心的可计算共同选择或统一修复进展；两条链不推出UM-TARGET-v1。

## 容量外包与最小总处理量初始化

[多拟阵容量外包](minimal_star_contraction_and_capacity_gap.md#7-原任务地集上多拟阵容量外包的精确损失)与[最小总处理量面](optimal_convex_fixed_slot_gap.md#6-最小总处理量的整个最优面也可能丢掉修复边)新增两个准确接口边界：保全部本地可行集的p拟阵交最优容量损失max(1,2−p/k)；basic且整个最小处理量面的支撑也可近2OPT，即使OPT/LST→1。两者均为已知工具的简单扩展，不能排除一般联合迁移；重新开放零质量边和允许真实工作量上升仍是下一义务。

精确身份UM-KNAPSACK-MATROID-ENVELOPE-v1、UM-MIN-WORK-FACE-SUPPORT-GAP-v1；由正文增补沿原review进入新代码/冻结证据，旧真OPT凸包身份不变。

大小任务共同修复进一步分清两条事实：[冻结宏任务的全微任务重开](optimal_hull_marginal_rounding_barrier.md#10-冻结宏任务后的微任务全局重开间隙与尖锐迁移前沿)即使精确联合优化仍趋2，并有尖锐宏任务迁移前沿；[两层异质需求贪心](rooted_dag_degree_token_bridge.md#7-两层需求树的半比例贪心与任务桥梁的二分之三负载界)给无宽度限制的浅层半比例树和对应3/2实际调度。一般多层/多边界联合选择仍OPEN，二者不是主目标突破。

[双边界森林的相关菜单](forest_boundary_contraction.md)：`UM-FOREST-TWO-BOUNDARY-MENU-v1`给a精确支配、b乘性保零和实际任务见证，任务不交挂件共享边界可求和；菜单共同选择与串行嵌套仍需新机制。

[同机槽族的单目的地修复](optimal_convex_fixed_slot_gap.md)：`UM-ONE-DESTINATION-SLOT-REPAIR-v1`给最小迁移m(m−1)/2，并可整批沿路径严格下降至OPT；仅此显式族，接收机允许增载。

两项均已自足证明、独立内部攻击和有限精确核验；都是限结构正面接口/修复，未认证全球新颖性，不形成一般输入的统一ε。UM-TARGET-v1保持OPEN。

新增UM-STAR-CONFIG-TRANSFER-v1（[星正文§8](minimal_star_contraction_and_capacity_gap.md#8-外部配置互斥下的配置点双向保持)）：逐步外部配置互斥使CONFIG双向可行、全部条件边向前保持，支持最多每步加一；缺占用/反向probe有反例。UM-CONTRACTED-SPARSE-CONFIG-GAP-v1（[稀疏正文末节](sparse_conditioned_configuration_gap.md)）收两端后无规则、仍全边独立CONFIG且gap2，补旧v1预处理缺口。读取链为专题CLAIMS→两正文→star_configuration_transfer_review.md→两份同名前缀代码及实际输入/证书/star_configuration_transfer_audit.json。主目标OPEN，完整共同base/联合迁移未排。

[单共享汇点的共同宏任务匹配](shared_sink_joint_macro_assignment.md)：UM-SHARED-SINK-JOINT-MACRO-v1。∀给定H∪{z}、仅homes可用且每有限边>T/2的宏任务、各任务仅在唯一指定home与公共z的非空子集可用的私有组、二进制有理T≥0及0<η≤1，有确定性poly(总位长,1/η)算法返回FAIL或实际调度，所有home≤T、z≤(1+η)T；OPT≤T时必成功，故FAIL蕴含OPT>T。私有任务无需尺寸上界，宏任务图任意。 每个macro/home或empty模式的真实最小整组撤离成本，保零乘性覆盖DP与带dummy成本的全局最小权完美匹配；误差只对同一个真实sink预算求和，不按home数量累积。 仅单共享sink与唯一home的给定结构，宏任务每有限边严格>T/2承重；成功不判定T精确可行，不含一般多sink/多home转换或统一ε。标准覆盖背包+匹配的组合接口，未认证新颖性。 一般UM-TARGET-v1仍OPEN。

## 对称矩重置后的准确前沿

[任务聚合、单机矩运输阈值与同边际修复](symmetric_moment_reset_and_single_machine_threshold.md)给UM-SYMMETRIC-JOB-AGGREGATION-v1及UM-SINGLE-MACHINE-MOMENT-RESET-THRESHOLD-v1。前者是给定R的可检查列条件；后者在真实最优分布上区分既定矩推前需2T与同Rx重新耦合只需T。不得写成Rx不属新N或同层求解不可能。读取链：CLAIMS→正文→symmetric_moment_reset_review.md→双路代码/实际q2输入与证书/symmetric_moment_reset_audit.json。

一般不相关输入中如何可计算地重建共同条件容量、输出统一低于2且保证总位多项式进展仍未解决；本结果不提供R搜索器。标准凸锥和二分图工具保留来源，全球新颖性与独立论文价值未认证。

## 共同流的正面提取与真正的支撑选择

[共同拥塞流与支撑搜索](rooted_dag_congestion_flow.md)给UM-DAG-CONGESTION-FLOW-v1：给同一K证书，一次整数流输出b≥1/(2K−1)，对所有整数K尖锐；固定W的证书/最小K均位多项式可求，未知W选择仍承重。UM-DAG-ACTIVATION-CORRIDOR-GAP-v1表明父激活上界及单位走廊守恒的边际LP仍可b*=1/q。正文→冻结审查→规范与独立代码→实际输入/证书/冻结证据均互连；不升级主目标。

完整路径：`research/current/unrelated_machines/rooted_dag_congestion_flow.md`、`research/reviews/unrelated_machines/rooted_dag_congestion_review.md`、`tests/audits/unrelated_machines/rooted_dag_congestion_flow.py`、`tests/audits/unrelated_machines/rooted_dag_congestion_independent.py`、`evidence/runs/unrelated_machines/rooted_dag_congestion_audit.json`；分别承担自足证明、冻结攻击、规范构造、独立oracle和有限结果。

同一正文§9另立UM-INDEPENDENT-UNIFORM-MOMENT-RESET-v1：独立均匀转移旧删机choices所生的新矩可确定精确计算，最小包q+2、负载1+2/q，q≥3严格小于固定后备的2。必须修同任务对角；一般m不保此界、个别态仍2T，故只作为限族正面运输，不提升主目标。双路实际矩/原分布coins枚举及冻结审查从正文进入。

## 跨路线的当前可行性判断

[共同容量路线整合审查](../../reviews/unrelated_machines/joint_capacity_route_feasibility_review.md)冻结三条正面接口及单目的地修复的独立覆盖，区分一般菜单核心、矩提取与实际共同迁移。附最大流标准标尺及精确有限审计；不新增或扩大主目标Claim。它说明哪些是可复用局部构造，哪些候选仍缺同一证书中的全机器容量与总位多项式进展。

[固定数量共享汇点的占位基交换与三半调度](fixed_sink_occupation_rounding.md)给三个分离身份：UM-OCCUPATION-MODE-SIDE-CONSTRAINT-v1允许任意K但仅界定2K个分数组；UM-FIXED-SINK-PRIVATE-GROUP-THREE-HALVES-v1在固定K的给定阈值下输出实际≤3T/2；UM-FIXED-SINK-MACRO-PROMISE-APPROX-v1用含OPT的大宏promise及非单调one-sided整数二分给真正≤3OPT/2。唯一home/给定分组和固定K仍承重，通用LP软件未实现，新颖性未认证。一般主目标下一缺口是不受限的接收容量与跨home/跨尺寸任务身份，UM-TARGET-v1仍OPEN。

## 守恒通道与非单位分叉参数

[共同流正文](rooted_dag_congestion_flow.md)§7–10另立UM-DAG-TRANSIT-CONGESTION-v1和UM-DAG-NONUNIT-PARAMETER-EXACT-v1：把k<2K改为守恒而不降低1/(2K−1)锐界，全部L/Z可零流补入W；支撑搜索只猜高点，K=1配合阈值缩放给h=#{k≥2}的2^h poly(位长)精确实际根树。旧合同身份保留；指数未消失，一般UM目标仍OPEN。规范亲身实现、独立全树/原边流、冻结审查和结果由正文互链，新颖性未认证。

[新增共同退出合同](shared_sink_joint_macro_assignment.md#8-宏任务也可退出共同匹配而非冻结大小身份)：`UM-SHARED-SINK-MACRO-EXIT-v1`允许宏任务真实退出及宏数超过home数；`UM-BOUNDED-PROFILE-EXIT-POOL-v1`在显式完整pool且`a_zc_j≤p_zj≤ρa_zc_j, p_zj≤βT`时，共同选择全部宏与私有撤离，输出home≤T、pool≤`[ρ(1+η)+β]T`，OPT≤T必成功。sink数不固定。标准cover/匹配/加权总量恢复组合，已独立审查及两路Fraction核验；一般资格、跨home任务与结构提取仍未闭合，UM-TARGET-v1仍OPEN。

## 反向困难性：有限覆盖不能免费提供可靠性

[配置下界的有限覆盖实现](configuration_finite_cover_obstruction.md)给`UM-CONFIG-FINITE-COVER-v1`：任意置换cover保持T_CONF且整数OPT不增；某个cover甚至在任意预设高围长下恰达到T_CONF。这是标准图覆盖机制的调度重构，只限制“所有接线/仅高围长自动soundness”，不排精选接线或其他归约。读取正文→冻结审查→双路精确构造与真实证书；主目标及其反面仍未证明。下一义务是源相关YES/NO调度解码与位多项式规模，不能继续用局部gap代替。

[共同资格组的联合流与未知OPT恢复](hall_group_joint_flow.md)：共同资格私有组现可在**sink数不固定**时共同选择macro/home/receiver：`UM-HALL-GROUP-JOINT-FLOW-v1`用每occupied组出口>T/q的Hall条件、一个整数流和真实前缀输出≤`q(2+δ)/(q+1)T`；`UM-HALL-GROUP-PROMISE-APPROX-v1`在同结构关于OPT的承诺下用有限瓶颈搜索直接输出相同比例OPT调度。q≥2、qδ<2，W_h∈[(1/2+1/q)T,T]、每私有件≤δT、同组共同资格与等端体积承重。q增长时改善可趋零；一般矩阵分组/跨home/异端时间转换仍未解。标准Hall/flow/prefix组合，未认证新颖性，UM-TARGET-v1保持OPEN。

## 全局分配矩的压缩算子与近平坦恢复

[全局四阶矩正文](global_assignment_moment_rounding.md)给UM-GLOBAL-MOMENT-NEARFLAT-EXTRACTION-v1与UM-GLOBAL-MOMENT-HS-GREEDY-GAP-v1：前者从给定共同证书的小全空间trace缺陷提取实际调度；后者用真实最优均匀分布攻击指定全空间HS贪心。读取链为精确CLAIMS→正文C₂/投影漏损/提取/反例→global_assignment_moment_rounding_review.md→nearflat_moment_extraction.py与独立代码→对应冻结结果及global_assignment_moment_freeze.json。通用证书生成未给出；不把初态零缺陷或Dirac矩存在误作一般算法。

## 可解图结构上仍可出现配置间隙二

[高围长仙人掌配置锐界与真实块算法](cactus_configuration_gap_and_block_exactness.md)分开三个身份：UM-CACTUS-HIGH-GIRTH-CONFIG-GAP-v1使任意给定围长的simple cactus仍CONFIG supgap2；UM-TWO-CHOICE-BLOCK-RANK-EXACT-v1以最大顶点块环秩b在2^b poly(L)输出精确调度；UM-PSEUDOFOREST-CONFIG-EXACT-v1仅在每连通分量≤单环时使CONFIG精确。平行任务不能合并计参。正文→冻结攻击→三份实际代码/输入/真实配置及调度证书/冻结结果可复现。AMO对称cactus与VW为已知祖先，未认证扩展新颖性。真正near2困难性不能只靠LPgap、深树或高围长；support≤2且b=O(log L)的输出族可精确解，仍须更强源相关一致性。主目标与反面均未证明。

## 反面路线需要真正的整数一致性

[私有需求树组合与共享重复](private_graft_and_resource_repetition.md)给UM-PRIVATE-GRAFT-NO-AMPLIFICATION-v1及UM-RESOURCE-REPETITION-SOUNDNESS-NO-v1：私有递归只取瓶颈，完整YES保留时不能缩小固定NO比例；完全元素池等价分母受限分数匹配，parity源坐标张量所有t≥2反变YES。不是近2困难性，UM-TARGET-v1仍OPEN。

读取链：专题CLAIMS→正文§1真正gap合同/§2–3恒等/§4–5反例→private_graft_repetition_review.md→三份规范/独立审计与private_graft_repetition_audit.json。不是所有共享或所有tensor归约的排除；一般低比例树到源NO矛盾的soundness仍缺。

## 真实最优矩的固定阶向量贪心边界

[固定阶压缩乘法向量贪心](truncated_multiplication_vector_greedy_barrier.md)证明 UM-TRUE-MOMENT-VECTOR-GREEDY-LINEAR-GAP-v1：一般真实T源上该规则合法且≤nT；对每固定r，有限域多项式真实最优源使任何任务顺序都严格选同一普通机器，近似比(n−1)/(4r+2)。故其最坏量级线性，即使给完整真实矩及容量局部化条件也如此。它不排真正条件化、重新构矩、容量反馈或其他算法；主目标仍OPEN。读取链为精确账本→正文§1–5→冻结审查→实际Gram/Fraction审计→q13输入与2197个最优源原子。有限高阶检查范围按冻结记录，全球新颖性未认证。

## 真实最优矩的固定向量规则已被严格击穿

[压缩向量贪心正文](projected_vector_greedy_unbounded.md)另立两个身份：UM-PROJECTED-VECTOR-GREEDY-UNBOUNDED-v1在三机、全正有限时间、真实最优分布上给无界比；UM-PROJECTED-VECTOR-GREEDY-UNIT-COLLISION-v1给五机五单位任务的严格2倍小证书。正文§2–5的重复净化保同一V，并逐阶段控制非零overlap；独立审查及双路实际Fraction证据已串联，未认证新颖性或外审。

本结果终止的是固定顺序max||Aeψ||²后左乘的具体充分机制。真实所有阶矩和逐行容量算子也不能免费保过去联合支撑；仍不排重新耦合、自适应顺序、好μ选择或其他提取。§8的交换算子边界可回收；真正未解仍是一般输入可求的共同容量与实际输出/总进展，UM-TARGET-v1保持OPEN。

## 新的可重开结构与零质量支撑边界

[跨过配置间隙后的开放义务](../../questions/unrelated_machines/barrier_escape_obligations.md)登记 `UM-THRESHOLD-COVER-JOINT-SLOT-v1` 的共同资格/等端私有组门槛界。原FPTAS见证换固定前缀的恢复有fatal gap，同行已正确撤回旧完成状态；本次修复可证二近似UB与截断DP，实际迁出同一覆盖X，使真实成本等于LP权重。经[独立冻结复核](../../reviews/unrelated_machines/threshold_cover_and_support_release_review.md)，原 `R*=((1+η)(3+δ))/(2+η)<2` 和one-sided搜索在声明结构类内重新闭合。一般任务分解、共同容量生成仍未闭。

同页的 `UM-LST-SUPPORT-RELEASE-v0` 旧族仍反驳固定正支撑填充，但其精确 `OPT=1−49/[100(m+1)]<1`，撤回旧的 `OPT=T=1` 标签。新增 `UM-LST-SUPPORT-RELEASE-OPTIMAL-v1` 用 `r` 个独立块把真实 `OPT` 固定为1，并证明少于 `r` 条零质量边时比值为 `2−1/m`；容量释放机制必须允许支撑扩张或共同 `(H,z)` 证书。rank-jump-one 路线已分层：对真实有限正权支持可用 Boolean 代数闭合恢复 `R+1` 原子；对一般伪矩仍缺共同交换投影与 `V2` localizer。`4-2√2` 支持候选未认证。

## 加权共同组的新增正面接口

[共同资格私有组的加权出口与联合槽](weighted_group_joint_slot_rounding.md)给`UM-WEIGHTED-GROUP-JOINT-SLOT-v1`及未知OPT的`UM-WEIGHTED-GROUP-PROMISE-APPROX-v1`：给定不交home/sink、唯一home私有组、同组共同资格与等端w_j≤δT、W_h≤T及macro端>T/2，在0≤δ<1/2时实际输出≤(3/2+δ)T（sink≤3T/2）；无组负载正下界、sink数不固定。未知OPT承诺版用单调加权LP及有理整数网格搜索。数学算法完整，软件仅实现给定精确LP见证的验证/舍入；独立审查与双路有限Fraction核验已登记，外审/新颖性未认证。一般矩阵如何生成这些分组和处理异端容量仍未解，UM-TARGET-v1保持OPEN。

## 新候选：组—汇点比例处理时间

问题账本新增 `UM-RATIO-GROUP-JOINT-SLOT-v1` 与 `UM-RATIO-GROUP-PROMISE-APPROX-v1` 候选。它把 `weighted_group_joint_slot_rounding.md` 的“组内所有有限端时间相同”放宽为：对每个组 `h` 和共同资格 sink `z`，存在任务无关比例 `ρ_hz`，使 `p_zj=ρ_hz w_j`。按 `c_hz=ρ_hz(W_h−T/2)_+` 排序造槽并与宏/home容量一次整数流，可得 home≤`(3/2+δ)T`、sink≤`(1+ρ_max/2)T`；固定 `δ<1/2, ρ_max<2` 才有结构类统一低于2。候选正文、必要性、未知OPT单调网格和待审义务见 [组—汇点比例联合槽候选](../../questions/unrelated_machines/group_sink_ratio_joint_slot_candidate.md)。分组生成、唯一home和共同资格仍未从一般矩阵中可计算提取，`UM-TARGET-v1`保持OPEN。

## 更宽的固定宏占位候选

`UM-HOMOGENEOUS-MACRO-PRIVATE-ST-v1` 把私有任务资格放宽到任意逐件集合 `A_j⊆H∪Z`，并允许每条私有边有不同处理时间，只要求≤`δT`；承重条件改为 `|B|=|H|`、宏只在 home、每个 home 的宏边时间固定为 `P_h>T/2` 且宏图有完美匹配。任取宏完美匹配后，私有 LST LP 的 home 容量 `T−P_h` 与匹配无关，ST 舍入给 `(1+δ)T` 候选。承诺 `P_h>OPT/2`、私有边≤`δOPT` 时，网格搜索给未知 OPT 的 `(1+δ̄)` 候选。该接口是标准 LST/ST 的结构重构，未认证新颖性；宏身份相关时长、宏数不等于 home 数或大私有边会重新产生联合容量义务。正文见 [同质大宏任意私有边候选](../../questions/unrelated_machines/homogeneous_macro_private_edge_st_rounding_candidate.md)。

## 异质宏身份下的统一残余容量候选

[异质大宏统一残余容量](heterogeneous_macro_uniform_residual_st_rounding.md)给 `UM-HETEROGENEOUS-MACRO-ARBITRARY-TINY-v1`：宏数等于 home 数、宏仅在 home、每条有限宏边严格大于 `T/2` 且不超过 `T`，但宏时长可依赖任务身份；tiny 任务资格与边成本完全逐件任意，只需每条 tiny 边≤`δT`。任意宏完美匹配后把全部 home tiny 容量统一收紧到 `T/2`，保留 OPT tiny 分配作 LP 见证，ST 后得到 `(3/2+δ)T`；承诺未知 OPT 版本以保留全部 tiny 边的单调 `F(t)` 和 `Q` 网格整数二分给 `(3/2+δ̄)OPT`。这去掉了同质宏和共同资格/等端 tiny 假设，但仍承重 `|B|=|H|` 与大宏 promise，不是一般 UM 算法。

同一正文记录 `UM-HETERO-TINY-3PARTITION-FLOW-BARRIER-v1`：即使所有异质 tiny 边均缩放到任意固定 `δT` 以下，精确 T 可行性仍可编码强 3-PARTITION，分数残余 LP 可行而整数调度不可行；该障碍只反驳普通整数流/简单 polymatroid 精确化，不反驳 ST 加性余量候选。

## 严格次二局部修复能垒

[严格次二批量能垒](strict_sub2_batch_barrier.md)给 `UM-STRICT-SUB2-BATCH-BARRIER-v1`：每个 `k≥2` 都有真实 `OPT=1` 的三机族，其 `Cmax<2` 坏态在每步最多 `k` 件且中间态严格 `<2` 的状态图中孤立，首个出口需 `k+1` 件。进一步，对任意固定目标余量 `ε` 和常数支持预算 `r`，取 `k>max{r,1/(8ε)}` 后坏态仍高于 `(2−ε)OPT`，因此常数支持的严格次二局部修复不能达到目标。它只限制局部修复，不是一般近似困难性；下一步若走修复路线必须允许规模增长的共同容量释放、跨过 `2T` 或全局重选。

## 三维匹配需求树的低比例地板

[仿射互补负载的基数解码边界](affine_complement_cardinality_boundary.md)记录 `UM-AFFINE-COMPLEMENT-CARDINALITY-BOUNDARY-v1`：p=B−λu 在等基数时反转Santa目标，但任何ρ>1的makespan界都允许q+1件溢出；ρ=1.9的精确矩阵显示按数量裁剪可把源最小效用从1变0。它只否定该黑盒解码接口。

[单层配额超图的精确值](single_layer_quota_hypergraph_obstruction.md)冻结 `UM-SINGLE-LAYER-QUOTA-VALUE-v1`：共享资源邻域的根树值恰为 `max_t min(1,ν_t/q,t/K)`；因此近2归约必须同时压低所有中间配额层，而不只是完整K层。该恒等式与4788个Fraction全枚举/100个随机边界已核验，不是一般困难性。

[三维匹配需求树障碍](three_dimensional_matching_demand_floor_obstruction.md)冻结 `UM-3DM-DEMAND-FLOOR-OBSTRUCTION-v1`：标准 (D_K(A)) 编码满足
(b^*=max\{\min(\mu/q,1/K),\min(\nu/q,2/K)\})，其中 (mu) 是 (X) 到 (Y\cup Z) 的一资源匹配、(
u) 是三维匹配。故完美 YES 的值恰为 (2/K)；放大三元组需求不能把 NO 压低而保持 YES 值1，固定 (K=2) 又留下单终端地板。公共资源族 (Q_{q,K}) 的精确 Hall 值可趋零，但尚未编码 NP 一致性。该结果只限制这一直接桥梁，不是一般困难性；下一义务是共享标签/高距离一致性并控制位长。

## 条件反面路线的最短缺口

[Santa Claus 无常数近似假设下的条件反面界](santa_conditional_reverse_barrier.md)冻结 `UM-SANTA-NO-CONSTANT-CONDITIONAL-v1`：若假设一般 Santa Claus 对每个固定常数都无多项式近似，则结合 LST 的 (<3/2) 困难性和 BLMRS 的 (2-1/\\alpha\to\\alpha+\\eta) 转换，可条件排除所有统一 (2-\\varepsilon) 调度算法。该假设尚未证明，故这是条件技术路线和精确缺口，不是主目标无条件反面。

## k-均匀资源束的分层逃逸障碍

[k-均匀资源束地板](k_uniform_bundle_matching_floor.md) 冻结 `UM-K-UNIFORM-BUNDLE-FLOOR-v1`：对根→(X)→超边→资源的需求树，精确有 (b^*=\max_t\min(\nu_t/q,t/K))，其中 (
u_t) 是每个超边取 (t) 个互不冲突资源的束匹配数。三维匹配的 (1/2) 逃逸只是 (k=K=2) 特例。任何近2反面归约必须同时压低所有 (j)-of-(k) 层；只压低完整超边匹配、提高需求或复制资源都不够。


## 低重数标签资源的新精确边界

[低重数标签资源的确定性地板与锐界](bounded_collision_label_resource_floor.md)：所选资源重数Δ给真实b≥1/Δ，二重资源对任意束宽恰保留1/2；全局不同变量组度Δ_G给无需见证的实际(2−1/Δ_G)桥梁调度。只排除该四层有界碰撞接口的近二归约；高重数/跨层一致性与一般UM-TARGET-v1仍OPEN。

读取正文§1–3a的三个精确身份→bounded_collision_label_floor_review.md→两份bounded_collision_bundle审计及冻结记录；后续应攻击每个局部完整选择均高碰撞的源相关解码，不能只增加成对冲突资源数量。


## 大需求束的有限锐界与高碰撞义务

进一步的[大需求束碰撞界与平方池锐性](large_bundle_collision_square_root_floor.md)给含根上取整的Λ_c真实树，q=Δ=K=t²时精确maxΛ=b*=1/t；带η→0及ηKmin→∞条件的NO侧必要量为liminfη²Δ≥1。只约束资源束接口，源问题解码和一般困难性仍缺。

正文给UM-LARGE-BUNDLE-COLLISION-FLOOR-v1完整域及式(9)精确必要量；读取冻结审查、两份large_bundle_collision代码及独立原父点/实际调度证据后再用于归约。不能把可解的平方池近二OPT当NP困难性。

[全局四阶负载松弛的锐利二间隙](c2_unit_multislice_gap.md)（`UM-C2-LOAD-UNIT-GAP-v1`）已闭合裸C2-load本身的义务：m≥3,n=m+1单位同机上T_C2=n/m、OPT2，显式有理PSD证书给supgap2。这不同于固定贪心坏例；其三阶同机矩为负、CONFIG阈值2，故不含C2+CONFIG或一般算法困难性。该裸C2命题的范围不变；后续[弱H2合取的新二间隙](weak_h2_configuration_moment_gap.md)另行关闭只共享一阶CONFIG的合同。共享行二阶在该新族上阈值精确，一般强合同与UM-TARGET-v1仍OPEN。

[闭环容量释放](../../../research/current/unrelated_machines/cyclic_batch_repair_and_fork_obstruction.md)§11把严格下降障碍推进到弱最大负载单调小步：真实最优凸包的全部最小成本槽输出仍趋2，最小非平凡改件/参与机恰d+1；但单任务到OPT的最小峰值仅为B+1/k²。它不是一般困难性，且该cactus族可精确解。

[异端有界畸变共同组](../../../research/current/unrelated_machines/distorted_group_joint_slot_rounding.md)在给定上下比例包络、唯一home/共同资格结构下联合选宏与接收机，给home≤(1+r+δ)T、sink≤[κ+B̄(1−r)]T，且闭合未知OPT搜索；固定κ+B̄δ<2时只有该结构类具统一改善。 一般UM-TARGET-v1仍OPEN；下一高信息义务是允许可控临时增载的共同容量修复及总位多项式进展，或在一般矩阵中生成保统一余量的相关结构。

## 路线复盘与下一道硬门槛

本题目前属于“诊断与限域接口取得实质进展，通用桥梁尚未推进”的状态。逐边/逐机/多行条件证书的趋二反例，已经把缺口从“再加一个局部不等式”收紧为多机共同相关容量；单汇点、固定 home、固定需求上界和固定支撑的联合构造，则证明受限共同成本确实可以被一次整数过程控制。两类成果都保留，但不能合并成一般算法。

后续候选必须对准 `JC-THRESHOLD-ε(T)`：对任意输入和候选 `T≥0`，从 `P` 本身产生共同容量证书并实际输出所有任务的整数分配，使每台机器≤`(2−ε)T`；若失败，必须有可独立验证的 `FAIL⇒OPT>T` 语义。`T=0`、零边、不可用边、空任务和极大分母属于同一合同。若采用 big/tiny 分解，固定 `β<1` 时“big 联合可求且 tiny 在剩余容量有分数解”确实会由 ST 给 `(1+β)T`，但 big 选择、tiny 可行性与全部机器容量的共同求解正是未解义务，不能把它当作免费匹配/流 oracle。

路线若在两树/长链、共享小端多行、全 tiny 分区、零质量支撑边和异长二机攻击上仍缺全输入可求证书、共同整数输出、统一不退化 `ε`、可靠 FAIL 语义或总位长多项式进展，就只登记为局部边界/反例并停止同类微调。详见专题前沿中的路线复盘段。

本轮团队资产清点已经写入[专题研究状态](../../unrelated_machines/RESEARCH_STATE.md#团队阶段清点去重后的路线矩阵-2026-10-17)。boss3 的大边/小边条件块路线与 boss6 的批量修复路线都指向“多目的地共同容量与实际整数输出”这一共享义务；后续应合并检查，不再各自复制逐星探针或逐坐标反例。其他路线按该矩阵分别归入经典前提、联合迁移、受限正面接口、矩/需求树和反面硬度，工作桌面只保留入口与卡点。

[单任务外接端口的向下投影与锐计数](signed_one_job_port_downset.md)给`UM-SIGNED-ONE-JOB-PORT-DOWNSET-v1`：保留一个外部出现端点且排除外部容量时，两一致态强制至少2^z(2^a+2^b−1)个严格可行状态，固定T>0逐参数锐；不能用该纯内部接口实现等值复制。BG一般signed阈值PCSP的近二困难性不保持调度双出现限制；多任务编码及外部联合容量仍未解，UM-TARGET-v1保持OPEN。

[单层配额超图平方根重数地板](single_layer_quota_sqrt_multiplicity_floor.md)：对每个邻域至少 K、资源总重数至多 Δ 的单层接口，计数得 b≥1/(√Δ+1)−1/K，并由资源总量给 b≤1/√Δ（在相应密度下）。这比有界碰撞的 1/Δ 地板更强，明确要求近二归约使用平方级碰撞或跨层一致性；不构成一般硬度。

[三外接机器选择器的锐三半界](three_host_selector_sharp_three_halves.md)：给only-a和b+c-free的两份实际C≤T调度，单调二色行权闭包输出only-b或only-c的完整C≤3T/2调度，且两任务锐；内部规模、资格任意，所有预载逐台核。同一机制对一般SC三特殊item给无条件可构造半值，亦锐。两者仅限制明确可用性复制接口；一般主目标和反面仍OPEN，新颖性/外审未认证。

## 反面路线新增的模型与复制边界

[Santa restricted边界](santa_restricted_bridge_boundary.md)核清 Haeupler–Saha–Srinivasan 的常数算法只适用于每件物品具有统一固有值的 restricted Santa；需求 \(k_v>1\) 的 token 桥梁任务在父/子端分别为 \(1/k_v\) 与 \(1\)，不保持该结构。故 restricted Santa 结果不能导入一般 UM 或当前 MMDA 反面路线。

[两份完整复制地板](duplication_two_copy_floor.md)证明：若每个变量的两份完整标签束在各自副本内不交，则资源二着色给出 \(b\ge1/2\) 的实际根树；这把简单 duplication 的 soundness 上限写成精确一半，并与 BCG §7 的复制警示分开。当前仍缺跨层整数一致性，使 YES 保持 \(b^*=1\) 而 NO 的每个高比例树都能解码源见证。


## 共同尺寸可重开 repair 接口

[共同尺寸微任务的可重开容量流](common_size_reopen_capacity_flow.md)登记 `UM-COMMON-SIZE-REOPEN-v1`：给定冻结核心、共同尺寸资格流和 `q_max` 头部余量时，有序槽允许接收机增载并输出实际整修复；每个支持连通分量内单一尺寸时，整数槽最大流无加性损失。Farkas 价格给一般可分流的精确阻塞证书；两机三件的 Fraction 反例说明分数共同容量不保证不可拆分整性。一般核心选择、异端时间和统一余量仍未解决。

[两状态行列池锐性修复](duplication_state_majority_floor.md)：标签可只选部分资源，s=K=4的真实最优为5/8，反驳旧附属1/2断言；主多数下界仍成立。新精确整数前沿及显式达到构造已独立重构，原K≥2s数例保留；不是一般近二困难性。

[多输出加权状态预算](weighted_fanout_profile_boundary.md)扩展三host接口：给两实际YES，对任意候选输出集K和有理β构造实际C≤(2−β_i)T；真实OPT总和≤(2|K|−1)T，加权星取等。任意两个缺一OPT之和≤3T，至多一个可严格超三半，任意扇出二叉树同时锐；不能用仅单输出近二星代替全局复制soundness。主目标保持OPEN。

[双轨阈值编码边界](dual_rail_threshold_soundness_boundary.md)：归一化scalar整类总有实际3/2（ST半质量直接推论），改unit容量亦总3/2，两种绝对T1界各有完整锐例。非均匀单例外有精确匹配合同；完整signedcube的真实OPT有min_B精确式且趋1。四成本模型分开，未将NO源自动解码为NO调度，主目标正反面仍OPEN。

[单位读出配额森林边界](unit_readout_pruned_forest_boundary.md)：一般arity下实际C<2等价全部变量mandatory r=ceil(k(2−C))森林可注入slots；但arity≤2A时，任意深度和任意wiring均有实际≤1+floor(k/2)/k≤3/2（经典ST半质量推论），14机15job绝对界锐。叶命中精确门槛(k−r+1)^h说明dummy补齐义务；相同64open的两模块真实OPT为1与7/4，叶容量不能代替祖先兼容。一般目标正反面仍OPEN。

[校准计数槽](unit_readout_calibrated_cardinality_slots.md)将单位读出树的半质量推广为有理下传证书：行分数任务数≤整数k−r+1给实际2−r/k。uniform x_h闭式提供所有wiring密度界；任意固定D≥2、arity≤D A的同结构类有确定性位poly统一2−1/(4D)算法，k,h可无界。已扣VW既有2−1/k及经典ST；D无界或一般P仍无统一ε，反面目标保持OPEN。

## 机器价格路线的精确退出条件

[价格凸化与锐容量界](heavy_light_price_convexification.md)将原min–max候选修正为显式LP：剪枝后全部标量机器价格仅给LST+big基数，joint gap仍sup2；不剪枝固定m锐界m。精确dual最优价若暴露同一big放置，可检验并恢复共同light见证和实际ST输出；一般输入没有这种面保证，面失败也不能可靠拒绝T。下界复用经典两树，不宣称新困难性。下一义务是可计算的非可加跨机器状态或实际联合损失，而非调价/anchor局部凸化。

## 固定残余函数与任务身份耦合

[容量格次模与占位图表示](residual_throughput_and_occupation_projection.md)给任意异端p、固定R的可求throughput格次模性质；固定占位时缺口D是超模。任务身份随H改变则不继承（2×2实际OPT1/2负控制）。更精确地，对每固定α<2及tiny上界，严格次二完成族可实现任意图独立集，D(I)恰为诱导边数；这些实例原OPT1可直接构造，故不是一般困难性。下一步仍是同时处理容量扣减、任务角色变化及实际舍入损失，不能从固定R次模或免费拟阵识别补上。


[两状态quota orientation表示](two_state_quota_orientation_obligation.md)把固定 \(\delta\) 的真实根树存在性精确翻译成rail方向、标签quota和资源单射；完整支付才是2-SAT，部分支付是quota packing。此表示替代继续堆叠资源复制，下一义务是证明该quota对象的gap soundness或构造其不可行障碍。

[完整单位树的叶流与选择重组](unit_readout_global_leaf_flow_and_selector_mixing.md)：任意clause密度下固定h有实际(1+2^(−1/h))近似；给p份同一P完整C1见证时，N≥p的任意covered selector坐标重组有锐2−1/(2p−1)实际负载。h、p增长及NO无完整YES均承重，一般主目标及其反面OPEN，外审与新颖性未认证。

## 同点合取的新增理论边界

[弱H2与强二阶配置的分离](weak_h2_configuration_moment_gap.md)给参数化一般证明：全局C2-load与完整CONFIG仅共享同一一阶x时，正值整数间隙上确界仍为2。k≥3的多项式规模稀释星族在T=1+(k−1)/(k²+1)有显式有理共同证书，而真实OPT=2−1/k；关键是条件激活中的伪矩超额在一阶配置投影中被稀释。全局PSD、所有负载localizer、相同x配置及位复杂度均分别证明。共享行二阶的强合同则在**同一族所有T**上阈值恰等于OPT；零pair经PSD传输成全局条件单槽容量。二者是不同Claim，不能外推成一般强H2定理或计算困难性。

[完整槽包络的精确表示](slot_envelope_and_configuration_identity.md)把所有尺度的真实槽上界写成E=ΣΔp·ceil(prefix x)，证明全局min max E=OPT。固定T后逐行凸化子水平集恰CONFIG；先凸化整个上图则只剩线性分数负载。可验证完整损失并未免费解决共同选择。后续要攻共享二阶及更强跨机信息的可计算性/实际提取，或绕过这些松弛的一般构造，停止把上述已排弱合取当充分接口。

[允许换轨的稀疏部分投影解码接口](../../questions/unrelated_machines/sparse_partial_projection_coupling_decoder_obligation.md)仅保留下一反面承重义务：同一vertex边际μ、projection次耦合及β/L>γ的真实浓缩。标准有给定证书decoder不等于调度归约；统一alphabet R的基线1/R使只保直方图或恰β=θ、L=θR时无法严格分离；近似量需另核常数。调度→证书OPEN，未进入canonical图/完成Claim账本。


[两状态quota orientation的Hall切分解](two_state_quota_hall_cut_decomposition.md)进一步给定变量子集与rail方向的精确支付判据：所有标签子集都必须通过Hall邻域不等式，资源度至多二时可拆分为私有、内部共享和边界共享三项。固定方向可由整数流输出实际支付或给出独立Hall缺口；同时选择方向和把单方向失败提升为全输入 `FAIL` 仍未解决。

[配置正部阈值与严格单位五三界](unit_readout_configuration_threshold_polytope.md)：完整私有单位树的CONFIG(T<2)恰由Σ(q−t)+≤floor(k(T−1))q描述；CONFIG1等价整轨LP并有完整C≤5/3输出（偶k≤3/2，k1≤1）。闭合两树精确Tconf=1+s*/k，经典gap族仍为1+1/k，故不外推为一般次二或近二困难性。

[剪枝调度首步与有界批量临时峰值](pruned_first_move_and_transient_peak.md)登记 UM-PRUNED-FIRST-MOVE-BOUND-v1 与 UM-BOUNDED-BATCH-TRANSIENT-PEAK-SHARP-v1：给定T剪枝σ、T≤C≤2T且另一τ≤T，某直接单件步≤U=max(2T,C+T/2)；无需τ可枚举一步或可靠NO。每固定k的m=k+1环族达到U及指定目标minimax。C=T排除零步歧义、孤立区间C≤B<U。一步可能增载，下一承重义务是一般缓冲集合/共同容量和总进展；初态不假设ST来源。正文→pruned_first_move_transient_peak_review.md→三个审计/实际输入及路径证书→pruned_first_move_transient_peak_audit.json。

## 本轮新增的精确桥与可解结构

[机器—任务关联反馈边参数的精确阈值算法](incidence_cycle_rank_exact.md)登记 `UM-INCIDENCE-FEEDBACK-EXACT-v1`：对有限关联图的反馈边数 `b`，枚举实际使用的反馈边后把余图化为森林，用叶交换精确输出 `T`-可行调度，复杂度 `2^b·poly(L)`；`b≤1` 时覆盖任意任务支持度的位多项式精确子类。它把一般输入的剩余难点定位到有环核心，不改变主目标 OPEN 状态。

[子线性联合投影的高围长近二边界](sublinear_coalition_projection_high_girth_gap.md)把上述长链构造按机器数对角化到任意 `r(M)=o(M)`：围长最终超过 `r(M)`，但 `OPT/T_CC_{r(M)}` 仍趋2；这是固定阶联合投影结果的量词加强，不是总位长困难性。

[重轻自洽 saddle 的森林整数补全边界](heavy_light_forest_integrality_boundary.md)给 `T=1` 参数族：残余分数值恰 `T`、均匀对偶是纯自洽，关联图仍是森林，但整数 `OPT/T=1+β−β/m` 可趋2。它只否定纯分数补全合同，不能替代反馈边森林的精确 `FAIL` 语义。

[全阶共同矩与负载局部化器的整数提取桥](full_degree_moment_localizer_decoding_bridge.md)登记 `UM-FULL-DEGREE-MOMENT-DECODING-v1`：次数 `2n+1` 的 Boolean/one-hot 共同泛函和次数 `n` 负载 localizer 必然含真实 `T`-可行原子；证书和原子族可指数大，故这是共同矩路线的完结义务而非多项式算法。

[重轻角色的自洽对偶证书与YES固定点边界](heavy_light_saddle_certificate_and_cycle.md)登记 `UM-HEAVY-LIGHT-SADDLE-CERTIFICATE-v1`：残余 LP 最优对偶与同价重任务最小化共同给全局角色及 `(1+β)T` ST 输出；参数化两机 YES 族表明纯 saddle 在 `OPT≤T` 时也可能不存在。逐价格 min–max 仍不能直接替代共同角色。

[逐行均匀相关读出的半数保留与平层三二调度](row_uniform_correlated_guard_rounding.md)给任意native标签数及跨测试相关的共同ceil-half匹配，并输出该显式平层原矩阵的全部任务、实际负载≤3/2。整数势避免有理微幅改进；simple与复合行均匀承重。它排除这一读出合同的near-zero soundness，不扩展到非均匀、多重自查询或多层树，一般目标正反面保持OPEN。

pDM阈值桥的[合入审查](../../reviews/unrelated_machines/pdm_threshold_domain_and_gap_review.md)保留原v1完整源域及gap方向异议：非退化固定参数域的算术内核成立，但尚未写显然NO/空YES合法分支；加一是NO下界。合法编译另由已有槽定理给(1,1+1/d) promise边界。原v1暂记条件性，不以默补假设维持完整归约状态。

[私有分叉树估值与支持域](private_tree_branching_valuation_and_minorants.md)新增精确signed demand、全叶XOS包络损失k[1−(1−1/k)^h]及single-state紧凑minorant LP；显式叶预算最大损失阶logB/loglogB。一般源计算gap和共同资源分配未由这些oracle解决；generic LP优化未实现，外审与新颖性未认证。

[统一端口与全局单位停车](uniform_port_parking_matroid_gap_and_actual_approximation.md)把每C独立仍1/D共同保留的显式余横截CONFIGgap，与BLMRS两值polymatroid算法给同结构真实2−1/(4+η)近似分开；D不统一或非单位停车未覆盖，通用算法未实现。

[近单位蕴含promise与物理复制](near_unit_implication_pcsp_and_physical_copy_obligation.md)给精确minion及所有固定k,r的一般PCSP NP-hardness，ordinaryFeder三坐标步骤在weak端可塌成full cube；真实两端/类型/全机decoder仍OPEN，不升级主反面。

[任务正规形与native边界](near_unit_implication_pcsp_and_physical_copy_obligation.md)新增三个独立身份：多小端双流在small行≤k/每job至少2小端时实际≤5/3；二叉单位选择器在C<2b无损恢复原机负载，且normal class（SU两端+unit-only最多3端）与UM-TARGET的统一次二算法存在等价。没有提供该核心求解器或near2hardness。

[两实际见证的单位占位胶合](unit_presence_two_witness_sharp_gluing.md)则给{1,1/k}逐k锐B(k)与任意tiny[0,a]的3(1+a)/2实际mixed分配；它只限裸presence复制，不排medium时间、任务身份或共同source解码。主目标正反面仍OPEN。

[列表agreement度数预算](list_agreement_degree_budget_and_decoder.md)给实际agr≥L(D−1)/(2d+L(D−1))及全agree通用锐阈值ceil2d/D。总O(|B|)标签数不足以调用短list soundness；仍缺每新增label跨多incidence收费的真实任务机制，主反面OPEN。

[部分MinRep线性度数源](partial_minrep_linear_degree_source_and_fee_bridge.md)用更强原soundness与rare covered上尾得到Δ=O_rho(g)，同覆盖禁令必需Ω(g)度数。它把充分物理费从logg降为固定常数；实际P、constant-fraction trigger、原投影decoder和fee仍未构造，随机归约采用NP不包含BPP，主反面OPEN。

[坐标切片编译反例](coordinate_slice_source_compilation_counterexample.md)给strictP1 iff完美源及NO实际OPT恰1+1/D；保promise padding仍低C，双射/均匀纤维和CONFIG1也不能修复。需真正跨test一致性/新叶共享，未得一般q或UM困难性。


[部分MinRep源v3](partial_minrep_linear_degree_source_and_fee_bridge.md)联合保证arbitrary-copy列表NO、线性degree、simple正则及任意固定高围长；固定G/FAIL/随机归约不略，未得物理decoder。


[源v5](partial_minrep_linear_degree_source_and_fee_bridge.md)处理任意不正规typed源，degree-mass复制同时保便宜copylists NO与equalfibers；v4非空域已显式修复，仍未供UMdecoder。


[私有注入树配置五三界](private_injective_tree_configuration_floor.md)：均匀small/私有内部/状态注入的精确结构边界，任意重新编号端口仍适用。


[三叉二叉彩虹的精确困难性](ternary_rainbow_subtree_exact_hardness.md)：完整等高树自足SAT归约、原P全任务回填与小gap，非near2。


[私有树重数界](private_injective_tree_configuration_floor.md)全CONFIG≤2−1/(μ+2)且G一阶系数1；[三叉彩虹](ternary_rainbow_subtree_exact_hardness.md)全局重数2/3为精确NP门槛。

[共同b双small行实际sharp3/2](joint_slot_prefix_rounding.md)已双陈述先行/双读后审查并root精确核验；PSM2018框架直接推广，旧row-spread域不改。near2须退出该行结构并有真实低σ解码，一般目标正反面仍OPEN。

[单强制根的µ精确gap](private_injective_tree_configuration_floor.md)已证明sup=2−1/µ；[三叉自然放大限制](ternary_rainbow_subtree_exact_hardness.md)已核YES实际漂移和纯收缩失效。两者均实际陈述先行/读后内审；前者不是多state Gµ，后者不排所有张量，主目标正反面仍OPEN。


[前缀原子证书的确定性解码桥](succinct_prefix_atomic_decoding_bridge.md)登记 `UM-PREFIX-ATOMIC-DECODING-v1`：若能按位多项式查询部分分配原子权、保持 one-hot 守恒并对完整原子给出逐机局部化，则O(|E|)次正延伸查询即可输出T可行调度；证书存在恰等价于OPT≤T。它把全阶矩路线的未解部分收窄为succinct证书生成或sound FAIL，不是一般算法。

## 锚点亏缺共同选择与精确保矩的边界

[锚点缺额联合舍入](anchor_deficiency_joint_rounding.md)从同一个LP共同选择anchor位置，并让任意跨分量/异端tiny仅做一次ST；分量缺额≤d0时，实际界为`[2−(1−α)/(d0+1)+β]T`。弱OPT所用边尺度承诺下，仅上截的单调整数二分给同系数OPT保证，无额外网格损失。余秩筛选门槛`1/(d+1)`锐；未声称调度系数最优。固定身份/有界亏缺仍承重。

[强配置匹配矩边界](strong_configuration_matching_moment_obstruction.md)证明任意固定阶、所有短事件非负且本行CONFIG同阶相容，仍可没有保给定二阶的真实共同匹配law；保一阶的锐二阶修复距离为`1/[4N(N−1)]`。实际OPT1且距离趋零，非调度gap。一般输入的混合身份、无界阻塞集和允许改矩后的全机统一余量仍缺；UM-TARGET-v1保持OPEN。

[永久缓冲激活与共同解锁路径](permanent_buffer_activation_and_priority_deadlocks.md)给锐分数窗口[1/3,1/2]和静态/优先级反例；[保留坏环与实际最大件全程锐界](held_cycle_release_and_assigned_max_path.md)用共同保护来流及源补集证明：每个正阈值源有一件eligible时，给定目标的完整路径可构造；并覆盖标准有序槽实际输出。局部promise类峰U逐参数锐，不冒充实际ST输出锐性。具体τ仍是承重输入，未知目标、任意剪枝初态与一般统一次二输出仍OPEN。

## 本轮从枚举转向的一般性数学边界

[多小端柔性密度的整数流障碍](mixed_small_endpoint_density_flow_barrier.md)登记 `UM-SMALL-DENSITY-FLOW-BARRIER-v1`：在 `{1,1/k}` 物理编译中，若每台机器 small incidence 不超过 `k` 且至少 `γ` 比例来自 `d_j≥2` 的多端任务，则均匀分流加整数容量流给出 `C≤2−floor(γk/2)/k`（`Q` unit-only 任务先做容量1匹配；匹配失败则 `OPT≥2`）。柔性端下界 `D` 时系数改为 `γ(1−1/D)`；三端 clause 结构约为 `4/3`。因此近二编译必须令柔性密度逐机趋零、离开单尺度，或把一致性转移到 unit/medium 端。`Q=∅` 分支只给绝对负载界，不冒充相对 `OPT` 近似。

[固定轮 assignment Sherali--Adams 的趋二间隙](fixed_sa_assignment_gap.md)登记 `UM-FIXED-SA-ASSIGNMENT-GAP-v1`：`m` 台相同机、`m+1` 个 unit 任务的均匀局部注入伪分布在 `T=1+1/(m-r+1)` 通过固定 `r` 轮完整 literal SA，而真实 `OPT=2`；固定 `r` 时比值趋 2。它证明固定层 assignment/LST 局部舍入不能提供统一改善，但不限制 configuration-LP、增长层数、SOS/Lasserre 或直接算法。该证明不依赖大规模枚举；`UM-TARGET-v1` 仍 OPEN。

[加权小端柔性密度与 ST 的次二障碍](weighted_small_st_barrier.md)把流障碍推广到 mixed small 时间：若逐机 small 总工作 `s_i≤1`，其中至少 `γ` 比例的工作来自多端任务，且每条 small 边 `≤β`，则显式等分支撑加 ST 舍入、再叠加 unit-only 匹配，给出 `C≤2−γ/2+β`。这排除了更一般的多尺度/任意支持图编译；仍允许 `γ→0`、较大 small 边和跨机器联合结构。

[未知目标下的共同尺寸精确重开](unknown_target_common_size_exact_repair.md)闭合了冻结核心、公共微任务尺寸接口：未知 B 可由有限候选阈值与整数流精确搜索；异尺寸共享机器立即遇到 Partition/装箱耦合。[未知目标 Partition 障碍](unknown_target_partition_search_obstruction.md)说明给定目标的全程路径合同不能把 τ 量词免费删除；这只是目标选择复杂度边界，UM-TARGET-v1 仍 OPEN。
2026-10-18 新增实际读取/费用合同与cube桥边界：[一般双见证查询分离的锐3/2费用合同](two_witness_query_separation.md)；[单正小端级联的完整查询立方体](single_home_cascade_query_separation.md)；[超立方分组菜单的Hall保留与锐3/2实际界](coordinate_slice_source_compilation_counterexample.md)。前两者需同一P两实际见证，cube3/2为限定结构；均不升级UM主目标。


[单件query计数与近单位读取必要条件](two_witness_query_separation.md)另立QUERY-COUNT-FEE-v3：即使聚合大，tiny单件仍有大批合格低费query；一次费用W≤F迫至少d−2枚query初态>(β−1)T。原η0严格错误实际修复并保留；仅双strict改派收费合同，非主反证。


[严格重中端gap占位胶合](unit_presence_two_witness_sharp_gluing.md)新增HEAVY-MEDIUM-STRICT-WITNESS-v1：两actual≤T，只用过端有heavy/medium间隔κ，则两mixed实际≤(2−κ/2)T，允许跨角色；仍不读具体job身份。同期修复公共尺寸满流遗漏冻结baseline guard及孤立机，不升级tiny审计为通用后端。


[保护环公共子句OR的身份错配](near_unit_implication_pcsp_and_physical_copy_obligation.md)新增CLAUSE-OR-FAILURE-v2：此明确Ci+Rc+unit-clause接线对任意公式都actual≤1，源NO全部丢失；共同匹配证书可回收，重试须阻止返回blocker与导出query索引交换，不能免费加同编号约束。空源idle已修，非所有identity-copy不可能。


[两组资源加权菜单的联合近似](degree_two_group_bounded_menu_joint_rounding.md)新增DEGREE-TWO-BOUNDED-MENU-JOINT-ROUNDING-v2：每resource跨≤2groups、每组≤K显式states、private总量≤1，group平均接已有VW2近似给完整实际C≤2−(2−OPT)/(2K)≤(2−1/(2K))OPT，bonus精确保OPT；Q2/K7任意cell权也在27/14结构界内。不是先big匹配再diffuse补全，非generalUM；menus2的unit阈值另可2SAT。 [有限组交互](weighted_menu_bounded_group_interaction_rounding.md)另给任意K、固定M/Δ的实际改善；[三坐标与三态正规形](degree_three_weighted_menu_cube_embedding.md)精确保OPT/V把任意normalized flat源降K3/资源度3再入zero cube，标准path已核BCG归属。[SC值桥/菜单数锐界](normalized_weighted_menu_santa_value_and_size.md)只排同U逐玩家shortcut。原source无须先限K/Δ，剩余承重仍是norm1与全partial导出的tiny-gap NO decoder，主目标未解。

[笛卡尔菜单的反向放大与一致性差距](cartesian_menu_recoupling_and_coordinate_consistency.md)：一个明确裸product实际OPT=1+2^-t趋1；额外逐坐标语义的配额却为floor((3/2)^t)/2^t趋0。两精确值排同族常数保值事后修复，尚缺真实负载实现的一致性；只否定该放大合同，非一般困难性。

[分块一致性、线性秩与全域缺项标尺](cartesian_menu_block_coherence_rank_and_deficit.md)回收已完成的精确结构：bounded blocks才指数衰减，无环单输入链仍保1/2；q元affine重选与coordinate一致相反极限；并发投影给任意nonlinear缺项必要条件。均未实现物理coherence；主反向承重继续是低负载全局decoder，停止以更多局部tensor数值代替该义务。

[逐机统一内部索引交换](machine_uniform_query_return_index_exchange.md)、[direct共居严格SAT及三半锐逃逸](direct_cohabiting_query_return_strict_sat_and_sharp_escape.md)与[真实直线源/累计路径编译障碍](line_set_packing_and_take_continue_compilation_obstructions.md)关闭各自精确接口；全部原jobs和全机负载已核，未关闭近二源NO的全局decoder。标准matching/Hall扣除新颖性，E曾误标签的proof-aware审查已另冻纠正，并由真正statement-first重构补齐。只有明确改变外部共同容量/partial AND机制时才重试这些具体桥。

[任意异权私有子句的三半上界与共享外端边界](general_weighted_private_clause_exchange_and_shared_outside_boundary.md)：固定辅助内部single-query/single-return接口的3T/2交换可与真实变量环共同匹配，所有局部索引strict可选时整公式实际≤1.5T；不是私有outside免费替ring。标准四任务环与小query返回池允许共享外部身份，但孤立OPT1且未保变量一致性。重试须改变精确模板的共同容量/边界，不能仅在私有Hc增加异权aux；主源NO联合decoder仍未闭合。

[仿射线逐tuple加globaldummy的完整编译](affine_line_tuple_groups_global_dummy_compilation_escape.md)另行关闭一种此前未分析的自然桥：n个tuple groups配n−q个共享dummy、q≤非空relations数，strict unit iff原full-set packing≥q，但无需源解仍actual≤1.5。选择q个不同relations恢复Hall不变量，所有未选state任务保留；不把这个新精确范围倒改成旧D已排，也不外推其它全局守卫/权重/阈值。

[完整归一化菜单的配置证书保持](normalized_menu_configuration_certificate_preservation.md)补足normalform的分数合同：flat machine CONFIG(1) iff positive-support FSLP iff state-dummy SC CONFIG(1)，zero原jobs仍全覆盖；再接SC路径得到rowtotal≤3/item正度≤3而CONFIG1/actual1/D。只排此LP充分性，未排actualOPT≥1的promise常数算法；标准路径/旧gap非新源，主目标OPEN。

[并行sum关系任意状态重赋权的半保留](weighted_affine_parallel_relation_reweighting_obstruction.md)补上不同范围：source value1/R的完整并行sum关系，即使任意state-dependent非负norm1权，仍可实际半保留/全部job≤1.5。条件于整个state保持c均匀，再把共点交唯一例外；singleton关系能V0，故不推广任意关系，不排避开本族的hard image。

[异权内部与重读口的bulk OR实际三半逃逸](bulk_or_commit_two_witness_interpolation.md)给完整block-ring双池下任意异权I/正C时间(.5,1]的committer：两个不同一真全原strict见证经半项配对/共同流，仍有全False全部原job实际≤1.5。内部异权collector与重C都不能单独挡split；缺两全局strict见证的跨子句NO不在范围，不是near2源。

[单标签边际均匀LINE的趋二实际间隙](tagged_affine_line_uniform_marginal_gap.md)给真LINE反例：每incidence label均匀、各state norm1，但V=1/(R−1)/实际OPT=2−1/(R−1)；共同arityR与R-partite可zero padding保值。此非pairwise-independent原hard image，未给源value/CONFIG新结论/计算困难性。

[宽矩形LINE的重细资源共同避冲突](tagged_affine_line_wide_rectangle_joint_escape.md)给出明确额外状态自由度：L>b(D−1)逐组避开旧marks，再以同一B保marks/独占点、每组损失≤Mβ；sparse正点给actual1，L>2q(D−1)²任意权给actual≤1.5。所有固定截距/原jobs保留，不把PI或alphabet可增当rectangle前提。

[两完整actual插值与实际used池端义务](bulk_or_commit_two_witness_interpolation.md)新增同页§6–10 v4：任意P的两actual与指定F原端改派，剩余job双出现配对得逐机件数与负载同τ；bulk J可接全部非pool仍全False≤1.5，任意pool得≤1.5+d/2，真正排near2须已用近unit J_pool身份改变。旧v3前缀/强输出范围保留；未知两witness不免费，不是sourceNO。

[仿射线两两独立的结构边界](tagged_affine_line_pairwise_independence_boundary.md)：单primary/onehot helpers在指定pairwise边际下可按条件化Hall全部actual1；多primary公共4D simplex陪集族则所有local pairs uniform仍V=2/(R+1)/实际OPT=2−2/(R+1)，common q/partite/全部zero jobs保留。后者只删唯一main即unit，不是robust或hard image/主反面。


## 任意剪枝初态的共同入流剥离

[任务包屏蔽与全输入锐路径](bundle_inflow_peeling_and_pruned_transient_sharpness.md)：先选源包及补集均足够释放的二分，再剥低内部入流顶点，保留核心、逆序激活、补集封口。全部剪枝σ≤C到给定τ≤T的路径峰≤max(2T,C+T/2)，旧两机族给全输入逐参数锐性。含逐机可计算profile、规范代码、独立攻击及冻结核验。具体τ仍承重；UM-TARGET-v1保持OPEN。

[原地拟阵外包的指数数量界](minimal_star_contraction_and_capacity_gap.md#9-固定次二容量外包需要超多项式数量的原地拟阵)另立UM-KNAPSACK-MATROID-EXPONENTIAL-v1：把大件改为1−r/k后，完整保留全部容量1可行集且所有共同独立集固定次二，需超多项式原输入位长的静态拟阵数；精确最少数为C(k,k−r−1,r)。只限本地完整外包，不推出一般调度困难性。
[多件共同激活、保留目标边与复制反放大](multi_activation_cover_and_replication_barriers.md)给定 `sigma,tau` 的静态共同激活充分桥，并精确记录静态证书非必要的动态例、复制和不交块的反放大边界。[高维匹配来源与需求树部分配额障碍](kdm_high_dimensional_quota_obstruction.md)则核对 LST 的高维匹配 gap，并证明直接超边需求树必须同时控制所有部分配额层；完整 KDM gap 不足以生成近二 UM hardness。两页均不改变 `UM-TARGET-v1` 的 OPEN 状态。
