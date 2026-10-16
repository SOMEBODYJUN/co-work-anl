# 不相关并行机：突破统一常数2壁垒的研究地图

本轮新主攻是 `UM-TARGET-v1`：一般二进制有理输入R∥C_max上，构造确定性位多项式时间、统一常数(2−ε)近似。目标仍OPEN；未形成新算法。旧拥塞/设施研究保留原身份，不作为本题数学依赖。

新阶段边界见[长链替换与固定机器联合投影](long_path_coalition_gap.md)：经典gap可移到任意大围长的简单机器图；只共享单机边际的固定大小联合见证仍有sup gap2。完整多机交叠相容性不在该否定范围，且三机完整相容性已能解决这批树宽2反例。完整证明、独立攻击和有限核验分别登记，未声称原创算法或全球新颖性。

先读[协作入口](../../unrelated_machines/README.md)与[精确账本](../../unrelated_machines/CLAIMS.md)，再读[模型、舍入与配置间隙的自足重构](model_and_classical_barriers.md)。[文献清单](../../unrelated_machines/literature_manifest.json)区分已取得原文、已核结果和待处理来源。[当前前沿](../../unrelated_machines/RESEARCH_STATE.md)说明下一步需要完成什么。

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

## 联合迁移的需求树压力接口

[有向需求树与真实调度的精确任务桥梁](rooted_dag_degree_token_bridge.md)给UM-DAG-DEGREE-TOKEN-IDENTITY-v1及UM-TARGET-IMPLIES-DAG-DEGREE-v1：一顶点一机器、unit入任务与本地子任务外溢，精确OPT=2−截断最大需求比例；二进制大需求用单填充保持任务数O(E+V)。正确阈值缩放使任何主目标算法都须构造常数比例需求根树。一般方向已由MMDA/Santa Claus文献知道，本页是可复用直接重构，不冒充新算法/新困难性。

读取链：本题账本→正文§1合同/§2–5构造及位复杂度→rooted_dag_token_bridge_review.md→rooted_dag_token_bridge.py及独立审计→rooted_dag_token_bridge_audit.json。原始Bamas2025 v2字节与定义/脚注位置见manifest；一轮SA定理只核对陈述，未转成调度层级结论。

新增派生UM-COORDINATE-REPAIR-ST-GAP-v1（循环批次正文cyclic_batch_repair_and_fork_obstruction.md§9）：与boss7真实最优凸包固定槽族衔接，工作量守恒使本逐坐标优化器仍0轮且gap→2。这个限制已覆盖配置来源；它不扩大fork关于one-destination、makespan非增的另一合同。下一机制必须允许低负载接收机上升并共同控制最大负载，不能把更强初始化单独当成循环算法的补丁。

新增派生UM-COORDINATE-REPAIR-ST-GAP-v1（同稿§9）：与boss7真实最优凸包固定槽族衔接，工作量守恒使本逐坐标优化器仍0轮且gap→2。这个限制已覆盖配置来源；它不扩大fork关于one-destination、makespan非增的另一合同。下一机制必须允许低负载接收机上升并共同控制最大负载，不能把更强初始化单独当成循环算法的补丁。

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
