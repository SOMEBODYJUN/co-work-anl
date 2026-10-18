# 不相关并行机：新主攻存档与协作入口

固定研究存档：`unrelated-machines`。主目标 `UM-TARGET-v1` 是一般R∥C_max确定性位多项式统一(2−ε)构造，仍OPEN。新对话直接使用 [BOSS_START.md](BOSS_START.md)，附仓库外的githubtoken.txt；无需人工分配内部subagents编号。

当前新增可复用边界：[长链高围长反例与固定机器联合投影](../current/unrelated_machines/long_path_coalition_gap.md)。它排除只共享单机配置分布的固定大小联合见证舍入合同；完整多机交叠一致性不被排除。经典核心与标准耦合的应用分开标记，新颖性未认证，未给一般新算法。

## 先读什么

[BOSS研究总览与路线分诊](BOSS_RESEARCH_BRIEF.md) → 根四入口及AGENTS → [数学地图](../current/unrelated_machines/README.md) → [精确身份](CLAIMS.md) → [当前前沿](RESEARCH_STATE.md) → [基线与障碍](../current/unrelated_machines/model_and_classical_barriers.md) → [独立审查](../reviews/unrelated_machines/classical_foundation_review.md)。按当前义务查[文献](LITERATURE.md)和[真实失败范围](FAILED_ROUTES.md)，不要求通读旧题或所有历史。

团队阶段复盘与去重入口见 [RESEARCH_STATE.md 的路线矩阵](RESEARCH_STATE.md#团队阶段清点去重后的路线矩阵-2026-10-17)：优先按 canonical 正文/审查/证据读取，工作桌面只看入口、当前卡点和待协作问题。
方向与工作模式审计见 [team_direction_audit.md](../reviews/unrelated_machines/team_direction_audit.md)：反例/边界在有序收敛，但一般全输入桥仍未闭合；最新 min–max 候选暂留 questions，不是 canonical。

本轮已有原文语料、定理与版本定位、完整槽舍入重构、配置gap重构及精确程序。2005全文未落地，困难性/2005完整舍入/受限指派局部搜索等尚未全部独立重构；不把首批地基说成“前人所有证明已内化”。后续可边核实承重工具边开展原创研究。

## 怎样协作和保存

复用仓库唯一程序 `research/weighted_congestion_frontier/tools/work.py`；路径历史上带旧题名称，不表示新题使用旧数学模型。新clone首次启动必须显式 `start --save unrelated-machines`。程序将本clone固定到此save；其他存档使用独立clone，不能覆盖本地绑定。

每对话一个boss稳定身份、一个独立clone，全部研究成果进main；subagents由boss汇集，不自行当作独立Work通道。本人桌面在 `research/workspaces/unrelated-machines/<actor>/`，其已推送版本可供同行访问。公屏、提及、私聊和收件箱均按本save路由；同仓私聊是视图隔离，没有双方专属读取权限。

日常完整命令及能力边界见 [RUNBOOK.md](RUNBOOK.md)。默认checkpoint范围按新save选本题八类目录、本题原文目录、共同账本和本人桌面，不包含旧题数学或他人桌面。维护共享程序/范围外导航时显式列全paths；所有待推历史都会审计，不能用只选本轮文件夹带旧提交。未知save默认也不会静默选旧题。

独立Work对话和界面Project仍由用户手动开启；存档、提示词和subagent不等于已经创建新的独立对话。发信不保证收件方正在运行或被唤醒。无排他认领、不限固定人数或轮数；实际规模能力以测量为准。

## 长期资产位置

| 位置 | 内容和读取用途 |
| --- | --- |
| research/current/unrelated_machines/ | 精确模型和自足已知证明重构；新定理按Claim分级，目录不赋予真值 |
| research/unrelated_machines/ | 目标账本、前沿、文献、障碍、启动提示词与操作手册 |
| research/questions/unrelated_machines/ | 尚未闭合的proof obligations和候选；主目标完成前都保留准确状态 |
| research/reviews/unrelated_machines/ | 先重构后攻击的实际审查与冻结hash |
| history/source/literature/unrelated_machines/ | 原始取得版本PDF/PS；hash、页数和解释在manifest与来源对应表 |
| tests/audits/unrelated_machines/ | 可复用精确舍入、构造、枚举与独立攻击程序 |
| examples/unrelated_machines/、evidence/certificates/unrelated_machines/、evidence/runs/unrelated_machines/ | 实际输入、证书、冻结证据分别保存；程序默认stdout，不覆盖冻结记录 |

新Claim同步登记全仓claims、review_status、assets与graph；文件具体名称/用途登记catalog。根README与研究目录持续作为地图。只有真实数学/工程增量入库，不保存逐轮聊天和重复摘要。

## 新增的匹配残余路线与准确边界

[大边匹配残余、简单支撑与共享逃逸容量](../current/unrelated_machines/heavy_matching_residual_and_escape.md)给出三个新限范围身份：`UM-HEAVY-MATCH-FILTER-v1`安全位多项式过滤、`UM-SIMPLE-SUPPORT-GAP-v1`简单支撑配置gap、`UM-ESCAPE-MATCH-GAP-v1`共享小端容量方法反例。主目标仍OPEN；不是统一低于2算法，未认证全球新颖性。读取顺序：精确账本→正文§1–5→冻结审查→两路代码/证据。真实依赖为模型/经典两树→路径终端配置与整数计数→逃逸族；匹配安全性单独依赖逐次删边与任务权增广。有限核验仅为checks。

| 新长期文件 | 内容、作用及读取条件 |
| --- | --- |
| research/current/unrelated_machines/heavy_matching_residual_and_escape.md | 全量词安全过滤、总位复杂度、三层瓶颈/反例；设计匹配或跨机器容量候选时读 |
| research/reviews/unrelated_machines/heavy_matching_escape_review.md | 独立先重构后冻结攻击，实际hash、边界及未解决义务；引用新Claim前读 |
| tests/audits/unrelated_machines/heavy_matching_residual.py | 任务权匹配、过滤固定点、显式路径/逃逸配置及小矩阵枚举 |
| tests/audits/unrelated_machines/ghmr_independent.py | 不同实现的matching oracle、独立证书与压缩容量DP；交叉核对而非一般证明 |
| evidence/runs/unrelated_machines/heavy_matching_residual_audit.json、heavy_matching_escape_independent.json | 两路实际参数、代码hash与有限结果；重跑写scratch，不覆盖 |

新增可复用接口从[计数传播与细分失败](../current/unrelated_machines/bundle_coupling_subdivision_barrier.md)读取：精确身份、一般证明、实际审查和代码证据已串联；未形成统一优于2的算法。

## 共同匹配选择与条件块容量

[共同大边选择、小边补全及块切面](../current/unrelated_machines/joint_matching_completion_and_block_cuts.md)明确三个身份：UM-JOINT-SMALL-ROUND-v1给定H,x输出(3/2+δ)T；UM-JOINT-CHOICE-NP-v1证明固定有理δ<1/3的精确选择NP完全，连N空/每job唯一small也成立；UM-ESCAPE-BLOCK-CUT-v1则通过随B变化的末簇条件切面，把整个共享逃逸族的强化阈值恢复为真实OPT。均已独立重构/冻结攻击，外审与新颖性未认证。

读取顺序：本题精确账本→正文§1合同/§2条件舍入/§3限域复杂度/§4限族切面→joint_matching_completion_review.md→joint_matching_completion_audit.json及其三份实际审计代码。原始Karp重印源的版本/hash与读到的位置见manifest；没有把下载说成完整源证明重构。

下一义务已被半单位扩展修正：固定δ<1/2的(Aδ)承诺搜索在P≠NP下均不可能；应转向实际槽损失或可分离/可舍入的条件块强化，仍无统一新算法。文件入口完整路径为research/current/unrelated_machines/joint_matching_completion_and_block_cuts.md、research/reviews/unrelated_machines/joint_matching_completion_review.md、tests/audits/unrelated_machines/{joint_matching_completion,unique_small_matching_audit,joint_matching_completion_independent}.py及evidence/runs/unrelated_machines/joint_matching_completion_audit.json；新候选必须同时攻击共享z、长链与一般多小端输入。

针对细分修补，新增[极小超载星精确消去与高阶容量边界](../current/unrelated_machines/minimal_star_contraction_and_capacity_gap.md)，包含实际调度提升、无规则紧凑族及boss4多任务接口障碍；不是近似突破。

新的[稀释终端与逐边线性探针边界](../current/unrelated_machines/diluted_sink_probe_gap.md)连接独立配置/条件点证书为何仍不够；加强探针仅对该族精确，主目标仍OPEN。冻结审查和双路证据从数学地图进入。


同稿第11节将boss3共享逃逸与本组稀释合并，新增对配置＋全部普通边探针＋GHMR的联合边界；两阶段审查保持旧身份及来源。

[半单位全窗口扩展](../current/unrelated_machines/joint_matching_completion_and_block_cuts.md)§3a（本数学目录同名正文）另立UM-JOINT-HALF-CHOICE-NP-v1及UM-JOINT-HALF-PROMISE-NO-v1：唯一small、时间{1/2,1}使(Aδ)在所有δ<1/2等价OPT≤1，关闭先前列出的共同见证窗口。旧1/3版原身份保留；δ=1/2及其他舍入合同不被排除。冻结审查和两份独立审计从正文进入。

## 全局基数探针后的共同负载瓶颈

[全局单行基数匹配与紧凑共享逃逸](../current/unrelated_machines/row_count_escape_gap.md)给UM-GLOBAL-ROW-COUNT-FILTER-v1与UM-COMPACT-COUNT-ESCAPE-GAP-v1。固定全行下界时无需枚举资源子池；但紧凑族有每机avoid证书，连任意单机配置都可延伸成全局计数见证，GPC₂仍T1可行而OPT=2−1/k。读取顺序：精确账本→正文§1合同/§2–4证明→row_count_escape_review.md→row_count_escape_audit.json与三份审计代码；实际k2输入/配置/达到调度也已保存。

失败点是把真实超载移到当前未精确查询的其他中心。条件块cut直接适配能修本族，不另宣称新成果；下一义务是一般可分离的共同负载/条件容量及统一舍入，不再只优化逐机最大卸载值。外审与全球新颖性未认证，主目标仍OPEN。

[直接联合槽的正面衔接](../current/unrelated_machines/joint_slot_prefix_rounding.md)给UM-ROW-SPREAD-TWO-ROUND-v1：删去零任务后每行正时间跨度≤2（逐机尺度不同）时，显式前缀计数LP加一次全任务槽匹配给3/2位多项式构造。它是VW/ST已知机制的直接推论，绕过过强(Aδ)见证；未消除一般行内跨尺度混合，主目标仍OPEN。

新增[三选稀疏深树与微小共享逃逸](../current/unrelated_machines/sparse_conditioned_configuration_gap.md)：全部有限边分别有完整条件配置证书，但整数间隙趋2。正文自足，来源连接既有逃逸与同行168；独立审查和实际输入/证据沿链接读取，未声称完整层级障碍。

紧凑共享逃逸正文§6另给UM-COMPACT-MULTIROW-EXTENSION-v1：任意U含至多N−2k个中心时，每个单机配置均可延伸并让U全部机器同时守真实容量；N−2k+1中心加z空pin有明确失败。故“更多独立行见证”仍缺共同相关性，尖锐预算和实际构造不改变主目标OPEN状态。

完整条件化新增[UM-MACHINE-CONFIG-PROBE-GAP-v1](../current/unrelated_machines/row_count_escape_gap.md#7-完整单机配置也分别能延伸到完整配置lp)：同一紧凑族每个合法单机配置均独立延伸到完整配置LP；需共同条件矩才能跨越此障碍，非完整层级下界。

[固定槽图的真实OPT边界](../current/unrelated_machines/optimal_convex_fixed_slot_gap.md)新增一个与LPgap不同的断点：x可有显式全局最优凸分解，所有固定槽matching仍趋2；本族有一轮跨槽修复。完整定义、审查、双路代码与冻结证据由该正文连接；主目标仍OPEN。

## 循环批量修复与真正的分流义务

[UM-OPT-HULL-LONG-CHAIN-LOCAL-GAP-v1：真最优凸包长链修复](../current/unrelated_machines/cyclic_batch_repair_and_fork_obstruction.md#10-真实最优凸包初始化后的无界机器长链义务)把参与机器数的义务与单机批量分开：所有mincost槽输出值2−1/k，严格lex改善恰需d+1任务/d+2台机器。两个真实最优分量、实际槽图、双路证据与[冻结攻击](../reviews/unrelated_machines/optimal_hull_long_chain_review.md)可追溯；允许先中性腾空链尾即有逐件弱Cmax修复，不是一般算法障碍。

[循环批量修复与分流合流障碍](../current/unrelated_machines/cyclic_batch_repair_and_fork_obstruction.md)给三个准确身份：固定η的总位多项式局部优化器，常数单机迁出数的真实OPT障碍，以及唯一最小成本LST槽分配仍须多目的地分流的padding族。程序允许任意批量和循环长度，成功轮数≤4m/η，但局部终态没有统一近似保证。反例所用x违反配置大任务基数，未排配置投影/选基本点/换支撑。读取链：本题Claim→正文§2–4算法/§5–7边界→冻结审查→规范实现与独立审计、实际k2输入/槽证书与运行记录。标准图搜索和背包缩放扣除后的全球新颖性、独立论文价值未认证。

[有向需求树的直接任务桥梁](../current/unrelated_machines/rooted_dag_degree_token_bridge.md)提供可复用真实输入、双向输出和精确OPT恒等；目标算法必具常数比例树构造能力的已知方向已自足重构。大需求填充及阈值位复杂度明确，SA间隙不转移。

新增派生UM-COORDINATE-REPAIR-ST-GAP-v1（循环批次正文cyclic_batch_repair_and_fork_obstruction.md§9）：与boss7真实最优凸包固定槽族衔接，工作量守恒使本逐坐标优化器仍0轮且gap→2。这个限制已覆盖配置来源；它不扩大fork关于one-destination、makespan非增的另一合同。下一机制必须允许低负载接收机上升并共同控制最大负载，不能把更强初始化单独当成循环算法的补丁。

新增派生UM-COORDINATE-REPAIR-ST-GAP-v1（同稿§9）：与boss7真实最优凸包固定槽族衔接，工作量守恒使本逐坐标优化器仍0轮且gap→2。这个限制已覆盖配置来源；它不扩大fork关于one-destination、makespan非增的另一合同。下一机制必须允许低负载接收机上升并共同控制最大负载，不能把更强初始化单独当成循环算法的补丁。

## 固定最优边际断点与单边界批量恢复

[UM-OPT-HULL-ROW-DISCREPANCY-GAP-v1及UM-OPT-HULL-PAIR-NC-GAP-v1](../current/unrelated_machines/optimal_hull_marginal_rounding_barrier.md)：x本是真实OPT显式平均，固定row/count仍sup2；同sink pair-NC的期望和尾界均尖锐。不是配置gap或主目标困难性；正文§9→optimal_hull_marginal_review.md→三路审计/冻结证据及k2r4实际输入/概率证书。

[UM-FOREST-BOUNDARY-AUGMENT-v1](../current/unrelated_machines/forest_boundary_contraction.md)：给定唯一boundary、内部无外接的森林，任意批量父包knapsack给b≤b*(T)、内部≤(1+η)T；用根单端任务恢复max(B,(1+η)T)，每次删机器的重复消元不按深度累计。正文→forest_boundary_contraction_review.md→upward/downward两算法及冻结范围。已知结构DP机制背景见JMS2017 manifest，不认证新颖性。

仍缺一般多边界/有环核心的可计算共同选择或统一修复进展；两条链不推出UM-TARGET-v1。

## 联合迁移候选的新准确边界

[多拟阵容量外包](../current/unrelated_machines/minimal_star_contraction_and_capacity_gap.md#7-原任务地集上多拟阵容量外包的精确损失)与[最小总处理量面](../current/unrelated_machines/optimal_convex_fixed_slot_gap.md#6-最小总处理量的整个最优面也可能丢掉修复边)新增两个准确接口边界：保全部本地可行集的p拟阵交最优容量损失max(1,2−p/k)；basic且整个最小处理量面的支撑也可近2OPT，即使OPT/LST→1。两者均为已知工具的简单扩展，不能排除一般联合迁移；重新开放零质量边和允许真实工作量上升仍是下一义务。

大小任务共同修复进一步分清两条事实：[冻结宏任务的全微任务重开](../current/unrelated_machines/optimal_hull_marginal_rounding_barrier.md#10-冻结宏任务后的微任务全局重开间隙与尖锐迁移前沿)即使精确联合优化仍趋2，并有尖锐宏任务迁移前沿；[两层异质需求贪心](../current/unrelated_machines/rooted_dag_degree_token_bridge.md#7-两层需求树的半比例贪心与任务桥梁的二分之三负载界)给无宽度限制的浅层半比例树和对应3/2实际调度。一般多层/多边界联合选择仍OPEN，二者不是主目标突破。

[双边界森林的相关菜单](../current/unrelated_machines/forest_boundary_contraction.md)：`UM-FOREST-TWO-BOUNDARY-MENU-v1`给a精确支配、b乘性保零和实际任务见证，任务不交挂件共享边界可求和；菜单共同选择与串行嵌套仍需新机制。

[同机槽族的单目的地修复](../current/unrelated_machines/optimal_convex_fixed_slot_gap.md)：`UM-ONE-DESTINATION-SLOT-REPAIR-v1`给最小迁移m(m−1)/2，并可整批沿路径严格下降至OPT；仅此显式族，接收机允许增载。

两项均已自足证明、独立内部攻击和有限精确核验；都是限结构正面接口/修复，未认证全球新颖性，不形成一般输入的统一ε。UM-TARGET-v1保持OPEN。

[星配置保持§8](../current/unrelated_machines/minimal_star_contraction_and_capacity_gap.md#8-外部配置互斥下的配置点双向保持)与[无规则收缩终态](../current/unrelated_machines/sparse_conditioned_configuration_gap.md)补UM-STAR-CONFIG-TRANSFER-v1及UM-CONTRACTED-SPARSE-CONFIG-GAP-v1。已独立冻结攻击和双路全部最终边核验；前者可复用正面接口，后者仅指定预处理＋独立探针边界，主目标仍OPEN。

[单共享汇点的共同宏任务匹配](../current/unrelated_machines/shared_sink_joint_macro_assignment.md)：UM-SHARED-SINK-JOINT-MACRO-v1。∀给定H∪{z}、仅homes可用且每有限边>T/2的宏任务、各任务仅在唯一指定home与公共z的非空子集可用的私有组、二进制有理T≥0及0<η≤1，有确定性poly(总位长,1/η)算法返回FAIL或实际调度，所有home≤T、z≤(1+η)T；OPT≤T时必成功，故FAIL蕴含OPT>T。私有任务无需尺寸上界，宏任务图任意。 每个macro/home或empty模式的真实最小整组撤离成本，保零乘性覆盖DP与带dummy成本的全局最小权完美匹配；误差只对同一个真实sink预算求和，不按home数量累积。 仅单共享sink与唯一home的给定结构，宏任务每有限边严格>T/2承重；成功不判定T精确可行，不含一般多sink/多home转换或统一ε。标准覆盖背包+匹配的组合接口，未认证新颖性。 一般UM-TARGET-v1仍OPEN。

## 对称矩重置后的准确前沿

[任务聚合、单机矩运输阈值与同边际修复](../current/unrelated_machines/symmetric_moment_reset_and_single_machine_threshold.md)给UM-SYMMETRIC-JOB-AGGREGATION-v1及UM-SINGLE-MACHINE-MOMENT-RESET-THRESHOLD-v1。前者是给定R的可检查列条件；后者在真实最优分布上区分既定矩推前需2T与同Rx重新耦合只需T。不得写成Rx不属新N或同层求解不可能。读取链：CLAIMS→正文→symmetric_moment_reset_review.md→双路代码/实际q2输入与证书/symmetric_moment_reset_audit.json。

一般不相关输入中如何可计算地重建共同条件容量、输出统一低于2且保证总位多项式进展仍未解决；本结果不提供R搜索器。标准凸锥和二分图工具保留来源，全球新颖性与独立论文价值未认证。

[共同拥塞流与支撑搜索](../current/unrelated_machines/rooted_dag_congestion_flow.md)给UM-DAG-CONGESTION-FLOW-v1：给同一K证书，一次整数流输出b≥1/(2K−1)，对所有整数K尖锐；固定W的证书/最小K均位多项式可求，未知W选择仍承重。UM-DAG-ACTIVATION-CORRIDOR-GAP-v1表明父激活上界及单位走廊守恒的边际LP仍可b*=1/q。正文→冻结审查→规范与独立代码→实际输入/证书/冻结证据均互连；不升级主目标。

同一正文§9另立UM-INDEPENDENT-UNIFORM-MOMENT-RESET-v1：独立均匀转移旧删机choices所生的新矩可确定精确计算，最小包q+2、负载1+2/q，q≥3严格小于固定后备的2。必须修同任务对角；一般m不保此界、个别态仍2T，故只作为限族正面运输，不提升主目标。双路实际矩/原分布coins枚举及冻结审查从正文进入。

[共同容量路线整合审查](../reviews/unrelated_machines/joint_capacity_route_feasibility_review.md)是判断当前各组路线的入口：含Astra独立攻击、单任务菜单保留原核心、需求流标准标尺、真矩提取限制及同级boss的实际反馈；不把研讨候选升级。

[固定数量共享汇点的占位基交换与三半调度](../current/unrelated_machines/fixed_sink_occupation_rounding.md)给三个分离身份：UM-OCCUPATION-MODE-SIDE-CONSTRAINT-v1允许任意K但仅界定2K个分数组；UM-FIXED-SINK-PRIVATE-GROUP-THREE-HALVES-v1在固定K的给定阈值下输出实际≤3T/2；UM-FIXED-SINK-MACRO-PROMISE-APPROX-v1用含OPT的大宏promise及非单调one-sided整数二分给真正≤3OPT/2。唯一home/给定分组和固定K仍承重，通用LP软件未实现，新颖性未认证。一般主目标下一缺口是不受限的接收容量与跨home/跨尺寸任务身份，UM-TARGET-v1仍OPEN。

## 守恒通道与非单位分叉参数

[共同流正文](../current/unrelated_machines/rooted_dag_congestion_flow.md)§7–10另立UM-DAG-TRANSIT-CONGESTION-v1和UM-DAG-NONUNIT-PARAMETER-EXACT-v1：把k<2K改为守恒而不降低1/(2K−1)锐界，全部L/Z可零流补入W；支撑搜索只猜高点，K=1配合阈值缩放给h=#{k≥2}的2^h poly(位长)精确实际根树。旧合同身份保留；指数未消失，一般UM目标仍OPEN。规范亲身实现、独立全树/原边流、冻结审查和结果由正文互链，新颖性未认证。

[新增共同退出合同](../current/unrelated_machines/shared_sink_joint_macro_assignment.md#8-宏任务也可退出共同匹配而非冻结大小身份)：`UM-SHARED-SINK-MACRO-EXIT-v1`允许宏任务真实退出及宏数超过home数；`UM-BOUNDED-PROFILE-EXIT-POOL-v1`在显式完整pool且`a_zc_j≤p_zj≤ρa_zc_j, p_zj≤βT`时，共同选择全部宏与私有撤离，输出home≤T、pool≤`[ρ(1+η)+β]T`，OPT≤T必成功。sink数不固定。标准cover/匹配/加权总量恢复组合，已独立审查及两路Fraction核验；一般资格、跨home任务与结构提取仍未闭合，UM-TARGET-v1仍OPEN。

## 反向困难性：有限覆盖不能免费提供可靠性

[配置下界的有限覆盖实现](../current/unrelated_machines/configuration_finite_cover_obstruction.md)给`UM-CONFIG-FINITE-COVER-v1`：任意置换cover保持T_CONF且整数OPT不增；某个cover甚至在任意预设高围长下恰达到T_CONF。这是标准图覆盖机制的调度重构，只限制“所有接线/仅高围长自动soundness”，不排精选接线或其他归约。读取正文→冻结审查→双路精确构造与真实证书；主目标及其反面仍未证明。下一义务是源相关YES/NO调度解码与位多项式规模，不能继续用局部gap代替。

[共同资格组的联合流与未知OPT恢复](../current/unrelated_machines/hall_group_joint_flow.md)：共同资格私有组现可在**sink数不固定**时共同选择macro/home/receiver：`UM-HALL-GROUP-JOINT-FLOW-v1`用每occupied组出口>T/q的Hall条件、一个整数流和真实前缀输出≤`q(2+δ)/(q+1)T`；`UM-HALL-GROUP-PROMISE-APPROX-v1`在同结构关于OPT的承诺下用有限瓶颈搜索直接输出相同比例OPT调度。q≥2、qδ<2，W_h∈[(1/2+1/q)T,T]、每私有件≤δT、同组共同资格与等端体积承重。q增长时改善可趋零；一般矩阵分组/跨home/异端时间转换仍未解。标准Hall/flow/prefix组合，未认证新颖性，UM-TARGET-v1保持OPEN。

## 共同全局分配矩的准确接口

[全局四阶分配矩](../current/unrelated_machines/global_assignment_moment_rounding.md)保存给定小δ证书的有理实际提取及全空间HS贪心的真实分布反例。两项身份、源/当前证明、内审、有限实现和开放生成义务分别登记；主目标仍OPEN。

## 可解图结构上仍可出现配置间隙二

[高围长仙人掌配置锐界与真实块算法](../current/unrelated_machines/cactus_configuration_gap_and_block_exactness.md)分开三个身份：UM-CACTUS-HIGH-GIRTH-CONFIG-GAP-v1使任意给定围长的simple cactus仍CONFIG supgap2；UM-TWO-CHOICE-BLOCK-RANK-EXACT-v1以最大顶点块环秩b在2^b poly(L)输出精确调度；UM-PSEUDOFOREST-CONFIG-EXACT-v1仅在每连通分量≤单环时使CONFIG精确。平行任务不能合并计参。正文→冻结攻击→三份实际代码/输入/真实配置及调度证书/冻结结果可复现。AMO对称cactus与VW为已知祖先，未认证扩展新颖性。真正near2困难性不能只靠LPgap、深树或高围长；support≤2且b=O(log L)的输出族可精确解，仍须更强源相关一致性。主目标与反面均未证明。

[反面路线的私有组合与资源复制](../current/unrelated_machines/private_graft_and_resource_repetition.md)区分真正近2计算困难性与复制方法边界。完整YES时私有max/min不压小NO；完全共享克隆又可整数化分数匹配。证明/审查/精确证据已登记，不关闭主目标。

## 真实最优矩的固定阶向量贪心边界

[固定阶压缩乘法向量贪心](../current/unrelated_machines/truncated_multiplication_vector_greedy_barrier.md)证明 UM-TRUE-MOMENT-VECTOR-GREEDY-LINEAR-GAP-v1：一般真实T源上该规则合法且≤nT；对每固定r，有限域多项式真实最优源使任何任务顺序都严格选同一普通机器，近似比(n−1)/(4r+2)。故其最坏量级线性，即使给完整真实矩及容量局部化条件也如此。它不排真正条件化、重新构矩、容量反馈或其他算法；主目标仍OPEN。读取链为精确账本→正文§1–5→冻结审查→实际Gram/Fraction审计→q13输入与2197个最优源原子。有限高阶检查范围按冻结记录，全球新颖性未认证。

## 真实最优矩的固定向量规则已被严格击穿

[压缩向量贪心正文](../current/unrelated_machines/projected_vector_greedy_unbounded.md)另立两个身份：UM-PROJECTED-VECTOR-GREEDY-UNBOUNDED-v1在三机、全正有限时间、真实最优分布上给无界比；UM-PROJECTED-VECTOR-GREEDY-UNIT-COLLISION-v1给五机五单位任务的严格2倍小证书。正文§2–5的重复净化保同一V，并逐阶段控制非零overlap；独立审查及双路实际Fraction证据已串联，未认证新颖性或外审。

本结果终止的是固定顺序max||Aeψ||²后左乘的具体充分机制。真实所有阶矩和逐行容量算子也不能免费保过去联合支撑；仍不排重新耦合、自适应顺序、好μ选择或其他提取。§8的交换算子边界可回收；真正未解仍是一般输入可求的共同容量与实际输出/总进展，UM-TARGET-v1保持OPEN。

## 加权共同组的新增正面接口

[共同资格私有组的加权出口与联合槽](../current/unrelated_machines/weighted_group_joint_slot_rounding.md)给`UM-WEIGHTED-GROUP-JOINT-SLOT-v1`及未知OPT的`UM-WEIGHTED-GROUP-PROMISE-APPROX-v1`：给定不交home/sink、唯一home私有组、同组共同资格与等端w_j≤δT、W_h≤T及macro端>T/2，在0≤δ<1/2时实际输出≤(3/2+δ)T（sink≤3T/2）；无组负载正下界、sink数不固定。未知OPT承诺版用单调加权LP及有理整数网格搜索。数学算法完整，软件仅实现给定精确LP见证的验证/舍入；独立审查与双路有限Fraction核验已登记，外审/新颖性未认证。一般矩阵如何生成这些分组和处理异端容量仍未解，UM-TARGET-v1保持OPEN。

### 新增候选与表示边界

- `UM-RATIO-GROUP-JOINT-SLOT-v1` / `UM-RATIO-GROUP-PROMISE-APPROX-v1`：组内任务在 home 与共同资格 sink 之间按组—汇点恒定比例缩放；按真实比例成本 `ρ_hz d_h` 排序造槽，给出 home `≤(3/2+δ)T`、sink `≤(1+ρ_max/2)T` 的候选接口。唯一 home、共同资格、宏大边和固定比例仍是额外结构，正文在 `research/questions/unrelated_machines/group_sink_ratio_joint_slot_candidate.md`。
- `UM-C2-PREFIX-CONDITIONING-DEGREE-v1`：偶奇五位真实来源的四阶矩完全相同，但深度四前缀的下一步容量相反；仅四阶 C₂ 不能自动提供深层条件 oracle。精确边界在 `research/current/unrelated_machines/c2_prefix_conditioning_degree_boundary.md`。

两项均不关闭 `UM-TARGET-v1`；前者的分组提取、后者的高阶/重算证书仍是一般路线的未解义务。

### 固定宏占位与任意私有资格

新增候选 `UM-HOMOGENEOUS-MACRO-PRIVATE-ST-v1`：`|B|=|H|`，宏只在 homes，且每个 home 的宏端处理时间只依赖 home、满足 `P_h>T/2`；任意私有任务可在任意显式资格边上运行，只要求每条私有边≤`δT`。固定任意宏完美匹配后，LST/ST 给 `(1+δ)T`；承诺 `P_h>OPT/2` 时用网格测试得到未知OPT候选。它精确显示共同资格与唯一home可去掉，但宏占位同质性仍是额外结构，不能替代一般 `UM-TARGET-v1`。


## 低重数标签资源的新精确边界

[低重数标签资源的确定性地板与锐界](../current/unrelated_machines/bounded_collision_label_resource_floor.md)：所选资源重数Δ给真实b≥1/Δ，二重资源对任意束宽恰保留1/2；全局不同变量组度Δ_G给无需见证的实际(2−1/Δ_G)桥梁调度。只排除该四层有界碰撞接口的近二归约；高重数/跨层一致性与一般UM-TARGET-v1仍OPEN。

读取正文§1–3a的三个精确身份→bounded_collision_label_floor_review.md→两份bounded_collision_bundle审计及冻结记录；后续应攻击每个局部完整选择均高碰撞的源相关解码，不能只增加成对冲突资源数量。


## 大需求束的有限锐界与高碰撞义务

进一步的[大需求束碰撞界与平方池锐性](../current/unrelated_machines/large_bundle_collision_square_root_floor.md)给含根上取整的Λ_c真实树，q=Δ=K=t²时精确maxΛ=b*=1/t；带η→0及ηKmin→∞条件的NO侧必要量为liminfη²Δ≥1。只约束资源束接口，源问题解码和一般困难性仍缺。

正文给UM-LARGE-BUNDLE-COLLISION-FLOOR-v1完整域及式(9)精确必要量；读取冻结审查、两份large_bundle_collision代码及独立原父点/实际调度证据后再用于归约。不能把可解的平方池近二OPT当NP困难性。

[全局四阶负载松弛的锐利二间隙](../current/unrelated_machines/c2_unit_multislice_gap.md)（`UM-C2-LOAD-UNIT-GAP-v1`）已闭合裸C2-load本身的义务：m≥3,n=m+1单位同机上T_C2=n/m、OPT2，显式有理PSD证书给supgap2。这不同于固定贪心坏例；其三阶同机矩为负、CONFIG阈值2，故不含C2+CONFIG或一般算法困难性。该裸C2命题的范围不变；后续[弱H2合取的新二间隙](../current/unrelated_machines/weak_h2_configuration_moment_gap.md)另行关闭只共享一阶CONFIG的合同。共享行二阶在该新族上阈值精确，一般强合同与UM-TARGET-v1仍OPEN。

[闭环容量释放](../../research/current/unrelated_machines/cyclic_batch_repair_and_fork_obstruction.md)§11把严格下降障碍推进到弱最大负载单调小步：真实最优凸包的全部最小成本槽输出仍趋2，最小非平凡改件/参与机恰d+1；但单任务到OPT的最小峰值仅为B+1/k²。它不是一般困难性，且该cactus族可精确解。

[异端有界畸变共同组](../../research/current/unrelated_machines/distorted_group_joint_slot_rounding.md)在给定上下比例包络、唯一home/共同资格结构下联合选宏与接收机，给home≤(1+r+δ)T、sink≤[κ+B̄(1−r)]T，且闭合未知OPT搜索；固定κ+B̄δ<2时只有该结构类具统一改善。 一般UM-TARGET-v1仍OPEN；下一高信息义务是允许可控临时增载的共同容量修复及总位多项式进展，或在一般矩阵中生成保统一余量的相关结构。

## 本阶段新增入口：异质宏与严格次二批量

[异质大宏统一残余容量与 ST 舍入](../current/unrelated_machines/heterogeneous_macro_uniform_residual_st_rounding.md) 给 `UM-HETEROGENEOUS-MACRO-ARBITRARY-TINY-v1` 和承诺版 `UM-HETEROGENEOUS-MACRO-PROMISE-v1`：`|B|=|H|`、宏仅在 home 且有限宏边严格大于 `T/2`，宏时间可依身份变化；tiny 资格和边成本任意逐件、每边≤`δT`。统一 home 残余 `T/2` 配合 ST 得 `(3/2+δ)T`，未知 OPT 以保留全部 tiny 边的单调 `F(t)` 和 `Q` 网格整数二分搜索。正文还记录强 3-PARTITION 精确流障碍，限制把异质残余当普通整数流或 polymatroid；这些结构结果不关闭一般主目标。

[严格次二状态图的参数化批量能垒](../current/unrelated_machines/strict_sub2_batch_barrier.md) 给 `UM-STRICT-SUB2-BATCH-BARRIER-v1`：`OPT=1` 坏态负载趋近 2，在每步至多 `k` 件、所有中间态严格 `<2` 的图中孤立，首个出口需 `k+1` 件。它只限制常数批量中性修复，不能作为一般近似困难性。

[单任务外接端口的向下投影与锐计数](../current/unrelated_machines/signed_one_job_port_downset.md)给`UM-SIGNED-ONE-JOB-PORT-DOWNSET-v1`：保留一个外部出现端点且排除外部容量时，两一致态强制至少2^z(2^a+2^b−1)个严格可行状态，固定T>0逐参数锐；不能用该纯内部接口实现等值复制。BG一般signed阈值PCSP的近二困难性不保持调度双出现限制；多任务编码及外部联合容量仍未解，UM-TARGET-v1保持OPEN。

[三外接机器选择器的锐三半界](../current/unrelated_machines/three_host_selector_sharp_three_halves.md)：给only-a和b+c-free的两份实际C≤T调度，单调二色行权闭包输出only-b或only-c的完整C≤3T/2调度，且两任务锐；内部规模、资格任意，所有预载逐台核。同一机制对一般SC三特殊item给无条件可构造半值，亦锐。两者仅限制明确可用性复制接口；一般主目标和反面仍OPEN，新颖性/外审未认证。

本轮反面路线新增：[Santa restricted边界与需求树桥梁的非保真性](../current/unrelated_machines/santa_restricted_bridge_boundary.md)核对 restricted Santa 结果不适用于 \(k_v>1\) 的 token 任务；[两份完整复制的一半一致性地板](../current/unrelated_machines/duplication_two_copy_floor.md)给简单 duplication 合同的 \(b\ge1/2\) 构造。BCG/Bamas/BLMRS 的精确 import 范围与原文哈希已登记在 `LITERATURE.md`、`literature_manifest.json`，不把 SA/LP gap升级为硬度。

[两状态行列池锐性修复](../current/unrelated_machines/duplication_state_majority_floor.md)：标签可只选部分资源，s=K=4的真实最优为5/8，反驳旧附属1/2断言；主多数下界仍成立。新精确整数前沿及显式达到构造已独立重构，原K≥2s数例保留；不是一般近二困难性。

[多输出加权状态预算](../current/unrelated_machines/weighted_fanout_profile_boundary.md)扩展三host接口：给两实际YES，对任意候选输出集K和有理β构造实际C≤(2−β_i)T；真实OPT总和≤(2|K|−1)T，加权星取等。任意两个缺一OPT之和≤3T，至多一个可严格超三半，任意扇出二叉树同时锐；不能用仅单输出近二星代替全局复制soundness。主目标保持OPEN。

[双轨阈值编码边界](../current/unrelated_machines/dual_rail_threshold_soundness_boundary.md)：归一化scalar整类总有实际3/2（ST半质量直接推论），改unit容量亦总3/2，两种绝对T1界各有完整锐例。非均匀单例外有精确匹配合同；完整signedcube的真实OPT有min_B精确式且趋1。四成本模型分开，未将NO源自动解码为NO调度，主目标正反面仍OPEN。

[单位读出配额森林边界](../current/unrelated_machines/unit_readout_pruned_forest_boundary.md)：一般arity下实际C<2等价全部变量mandatory r=ceil(k(2−C))森林可注入slots；但arity≤2A时，任意深度和任意wiring均有实际≤1+floor(k/2)/k≤3/2（经典ST半质量推论），14机15job绝对界锐。叶命中精确门槛(k−r+1)^h说明dummy补齐义务；相同64open的两模块真实OPT为1与7/4，叶容量不能代替祖先兼容。一般目标正反面仍OPEN。

[校准计数槽](../current/unrelated_machines/unit_readout_calibrated_cardinality_slots.md)将单位读出树的半质量推广为有理下传证书：行分数任务数≤整数k−r+1给实际2−r/k。uniform x_h闭式提供所有wiring密度界；任意固定D≥2、arity≤D A的同结构类有确定性位poly统一2−1/(4D)算法，k,h可无界。已扣VW既有2−1/k及经典ST；D无界或一般P仍无统一ε，反面目标保持OPEN。

## 机器价格路线的精确退出条件

[价格凸化与锐容量界](../current/unrelated_machines/heavy_light_price_convexification.md)将原min–max候选修正为显式LP：剪枝后全部标量机器价格仅给LST+big基数，joint gap仍sup2；不剪枝固定m锐界m。精确dual最优价若暴露同一big放置，可检验并恢复共同light见证和实际ST输出；一般输入没有这种面保证，面失败也不能可靠拒绝T。下界复用经典两树，不宣称新困难性。下一义务是可计算的非可加跨机器状态或实际联合损失，而非调价/anchor局部凸化。

## 固定残余函数与任务身份耦合

[容量格次模与占位图表示](../current/unrelated_machines/residual_throughput_and_occupation_projection.md)给任意异端p、固定R的可求throughput格次模性质；固定占位时缺口D是超模。任务身份随H改变则不继承（2×2实际OPT1/2负控制）。更精确地，对每固定α<2及tiny上界，严格次二完成族可实现任意图独立集，D(I)恰为诱导边数；这些实例原OPT1可直接构造，故不是一般困难性。下一步仍是同时处理容量扣减、任务角色变化及实际舍入损失，不能从固定R次模或免费拟阵识别补上。

[完整单位树的叶流与选择重组](../current/unrelated_machines/unit_readout_global_leaf_flow_and_selector_mixing.md)：任意clause密度下固定h有实际(1+2^(−1/h))近似；给p份同一P完整C1见证时，N≥p的任意covered selector坐标重组有锐2−1/(2p−1)实际负载。h、p增长及NO无完整YES均承重，一般主目标及其反面OPEN，外审与新颖性未认证。

## 同点合取的新增理论边界

[弱H2与强二阶配置的分离](../current/unrelated_machines/weak_h2_configuration_moment_gap.md)给参数化一般证明：全局C2-load与完整CONFIG仅共享同一一阶x时，正值整数间隙上确界仍为2。k≥3的多项式规模稀释星族在T=1+(k−1)/(k²+1)有显式有理共同证书，而真实OPT=2−1/k；关键是条件激活中的伪矩超额在一阶配置投影中被稀释。全局PSD、所有负载localizer、相同x配置及位复杂度均分别证明。共享行二阶的强合同则在**同一族所有T**上阈值恰等于OPT；零pair经PSD传输成全局条件单槽容量。二者是不同Claim，不能外推成一般强H2定理或计算困难性。

[完整槽包络的精确表示](../current/unrelated_machines/slot_envelope_and_configuration_identity.md)把所有尺度的真实槽上界写成E=ΣΔp·ceil(prefix x)，证明全局min max E=OPT。固定T后逐行凸化子水平集恰CONFIG；先凸化整个上图则只剩线性分数负载。可验证完整损失并未免费解决共同选择。后续要攻共享二阶及更强跨机信息的可计算性/实际提取，或绕过这些松弛的一般构造，停止把上述已排弱合取当充分接口。

[本轮跨层配额障碍](../current/unrelated_machines/cross_layer_quota_matching_near_two_obstruction.md)给核心—私有集合系统的全层闭式和实际 OPT=2−s/K；[独立集阈值障碍](../questions/unrelated_machines/independent_set_big_residual_interface_obstruction.md)限制先big后残余流的精确接口；[固定工作量局部极小](../current/unrelated_machines/fixed_work_convex_local_minimum_near_two.md)排除固定二次/排序势的单任务下降。它们均未关闭一般 UM-TARGET-v1。

[配置正部阈值与严格单位五三界](../current/unrelated_machines/unit_readout_configuration_threshold_polytope.md)：完整私有单位树的CONFIG(T<2)恰由Σ(q−t)+≤floor(k(T−1))q描述；CONFIG1等价整轨LP并有完整C≤5/3输出（偶k≤3/2，k1≤1）。闭合两树精确Tconf=1+s*/k，经典gap族仍为1+1/k，故不外推为一般次二或近二困难性。

[首步分段容量与固定批量锐临时峰](../current/unrelated_machines/pruned_first_move_and_transient_peak.md)给一般首步 U=max(2T,C+T/2) 与无需目标的单步选择器，及OPT=T的逐参数环能垒。按两项精确ID读取审查/证据；MOVE不保证改善，初态不宣称ST/最优凸包来源，一般全程和主目标仍OPEN。

[逐行均匀相关读出的半数保留与平层三二调度](../current/unrelated_machines/row_uniform_correlated_guard_rounding.md)给任意native标签数及跨测试相关的共同ceil-half匹配，并输出该显式平层原矩阵的全部任务、实际负载≤3/2。整数势避免有理微幅改进；simple与复合行均匀承重。它排除这一读出合同的near-zero soundness，不扩展到非均匀、多重自查询或多层树，一般目标正反面保持OPEN。

[私有分叉树估值与支持域](../current/unrelated_machines/private_tree_branching_valuation_and_minorants.md)新增精确signed demand、全叶XOS包络损失k[1−(1−1/k)^h]及single-state紧凑minorant LP；显式叶预算最大损失阶logB/loglogB。一般源计算gap和共同资源分配未由这些oracle解决；generic LP优化未实现，外审与新颖性未认证。

[统一端口与全局单位停车](../current/unrelated_machines/uniform_port_parking_matroid_gap_and_actual_approximation.md)把每C独立仍1/D共同保留的显式余横截CONFIGgap，与BLMRS两值polymatroid算法给同结构真实2−1/(4+η)近似分开；D不统一或非单位停车未覆盖，通用算法未实现。

[近单位蕴含promise与物理复制](../current/unrelated_machines/near_unit_implication_pcsp_and_physical_copy_obligation.md)给精确minion及所有固定k,r的一般PCSP NP-hardness，ordinaryFeder三坐标步骤在weak端可塌成full cube；真实两端/类型/全机decoder仍OPEN，不升级主反面。

[任务正规形与native边界](../current/unrelated_machines/near_unit_implication_pcsp_and_physical_copy_obligation.md)新增三个独立身份：多小端双流在small行≤k/每job至少2小端时实际≤5/3；二叉单位选择器在C<2b无损恢复原机负载，且normal class（SU两端+unit-only最多3端）与UM-TARGET的统一次二算法存在等价。没有提供该核心求解器或near2hardness。

[两实际见证的单位占位胶合](../current/unrelated_machines/unit_presence_two_witness_sharp_gluing.md)则给{1,1/k}逐k锐B(k)与任意tiny[0,a]的3(1+a)/2实际mixed分配；它只限裸presence复制，不排medium时间、任务身份或共同source解码。主目标正反面仍OPEN。

[列表agreement度数预算](../current/unrelated_machines/list_agreement_degree_budget_and_decoder.md)给实际agr≥L(D−1)/(2d+L(D−1))及全agree通用锐阈值ceil2d/D。总O(|B|)标签数不足以调用短list soundness；仍缺每新增label跨多incidence收费的真实任务机制，主反面OPEN。

[部分MinRep线性度数源](../current/unrelated_machines/partial_minrep_linear_degree_source_and_fee_bridge.md)用更强原soundness与rare covered上尾得到Δ=O_rho(g)，同覆盖禁令必需Ω(g)度数。它把充分物理费从logg降为固定常数；实际P、constant-fraction trigger、原投影decoder和fee仍未构造，随机归约采用NP不包含BPP，主反面OPEN。

[坐标切片编译反例](../current/unrelated_machines/coordinate_slice_source_compilation_counterexample.md)给strictP1 iff完美源及NO实际OPT恰1+1/D；保promise padding仍低C，双射/均匀纤维和CONFIG1也不能修复。需真正跨test一致性/新叶共享，未得一般q或UM困难性。


[部分MinRep源v3](../current/unrelated_machines/partial_minrep_linear_degree_source_and_fee_bridge.md)把arbitrary-copy列表同时性、d=O(g)、simple正则与任意固定girth联合保证；固定G位poly、显式FAIL和随机NP⊄BPP边界保留。


[源v5](../current/unrelated_machines/partial_minrep_linear_degree_source_and_fee_bridge.md)以degree质量copies去除原regular/两侧等大要求，并保typed等纤维；固定误差PCP可接，但一般Q不自动poly(g)。


[私有注入树配置五三界](../current/unrelated_machines/private_injective_tree_configuration_floor.md)：任意菜单、全阈值配置界与严格过滤判定；存在性不冒算法。


[完整三叉二叉彩虹困难性](../current/unrelated_machines/ternary_rainbow_subtree_exact_hardness.md)：重复色/变height的真实NP锚点，原P仅4/3对5/3。


[配置重数与一阶锐渐近](../current/unrelated_machines/private_injective_tree_configuration_floor.md)区分每state μ；[全局叶重数2/3门槛](../current/unrelated_machines/ternary_rainbow_subtree_exact_hardness.md)则为单tree全部辅助色统计，NP调度比值仍5/4。

[共同b双small行实际sharp3/2](../current/unrelated_machines/joint_slot_prefix_rounding.md)已双陈述先行/双读后审查并root精确核验；PSM2018框架直接推广，旧row-spread域不改。near2须退出该行结构并有真实低σ解码，一般目标正反面仍OPEN。

[单强制根的µ精确gap](../current/unrelated_machines/private_injective_tree_configuration_floor.md)已证明sup=2−1/µ；[三叉自然放大限制](../current/unrelated_machines/ternary_rainbow_subtree_exact_hardness.md)已核YES实际漂移和纯收缩失效。两者均实际陈述先行/读后内审；前者不是多state Gµ，后者不排所有张量，主目标正反面仍OPEN。

## 锚点亏缺共同选择与精确保矩的边界

[锚点缺额联合舍入](../current/unrelated_machines/anchor_deficiency_joint_rounding.md)从同一个LP共同选择anchor位置，并让任意跨分量/异端tiny仅做一次ST；分量缺额≤d0时，实际界为`[2−(1−α)/(d0+1)+β]T`。弱OPT所用边尺度承诺下，仅上截的单调整数二分给同系数OPT保证，无额外网格损失。余秩筛选门槛`1/(d+1)`锐；未声称调度系数最优。固定身份/有界亏缺仍承重。

[强配置匹配矩边界](../current/unrelated_machines/strong_configuration_matching_moment_obstruction.md)证明任意固定阶、所有短事件非负且本行CONFIG同阶相容，仍可没有保给定二阶的真实共同匹配law；保一阶的锐二阶修复距离为`1/[4N(N−1)]`。实际OPT1且距离趋零，非调度gap。一般输入的混合身份、无界阻塞集和允许改矩后的全机统一余量仍缺；UM-TARGET-v1保持OPEN。

[永久缓冲激活与共同解锁路径](../current/unrelated_machines/permanent_buffer_activation_and_priority_deadlocks.md)给锐分数窗口[1/3,1/2]和静态/优先级反例；[保留坏环与实际最大件全程锐界](../current/unrelated_machines/held_cycle_release_and_assigned_max_path.md)用共同保护来流及源补集证明：每个正阈值源有一件eligible时，给定目标的完整路径可构造；并覆盖标准有序槽实际输出。局部promise类峰U逐参数锐，不冒充实际ST输出锐性。具体τ仍是承重输入，未知目标、任意剪枝初态与一般统一次二输出仍OPEN。

2026-10-18：[一般双见证查询分离的锐3/2费用合同](../current/unrelated_machines/two_witness_query_separation.md)；[单正小端级联的完整查询立方体](../current/unrelated_machines/single_home_cascade_query_separation.md)；[超立方分组菜单的Hall保留与锐3/2实际界](../current/unrelated_machines/coordinate_slice_source_compilation_counterexample.md)。一般双见证tiny query的单次改派费不能复用为near2固定激活费，准确分离阈值3/2且sharp；单home全留初态另有完整query cube；超立方分组菜单全类actual≤3/2（DGR特例19/15）。失败范围仅精确合同；非OPT困难性，UM-TARGET-v1正反面仍OPEN。重试须改变读取初态聚合量/费用/源相关接口或slice真实结构，并给完整实际decoder。


[单件query计数与近单位读取必要条件](../current/unrelated_machines/two_witness_query_separation.md)另立QUERY-COUNT-FEE-v3：即使聚合大，tiny单件仍有大批合格低费query；一次费用W≤F迫至少d−2枚query初态>(β−1)T。原η0严格错误实际修复并保留；仅双strict改派收费合同，非主反证。


[严格重中端gap占位胶合](../current/unrelated_machines/unit_presence_two_witness_sharp_gluing.md)新增HEAVY-MEDIUM-STRICT-WITNESS-v1：两actual≤T，只用过端有heavy/medium间隔κ，则两mixed实际≤(2−κ/2)T，允许跨角色；仍不读具体job身份。同期修复公共尺寸满流遗漏冻结baseline guard及孤立机，不升级tiny审计为通用后端。


[保护环公共子句OR的身份错配](../current/unrelated_machines/near_unit_implication_pcsp_and_physical_copy_obligation.md)新增CLAUSE-OR-FAILURE-v2：此明确Ci+Rc+unit-clause接线对任意公式都actual≤1，源NO全部丢失；共同匹配证书可回收，重试须阻止返回blocker与导出query索引交换，不能免费加同编号约束。空源idle已修，非所有identity-copy不可能。


[两组资源加权菜单的联合近似](../current/unrelated_machines/degree_two_group_bounded_menu_joint_rounding.md)新增DEGREE-TWO-BOUNDED-MENU-JOINT-ROUNDING-v2：每resource跨≤2groups、每组≤K显式states、private总量≤1，group平均接已有VW2近似给完整实际C≤2−(2−OPT)/(2K)≤(2−1/(2K))OPT，bonus精确保OPT；Q2/K7任意cell权也在27/14结构界内。不是先big匹配再diffuse补全，非generalUM；menus2的unit阈值另可2SAT。 [有限组交互](../current/unrelated_machines/weighted_menu_bounded_group_interaction_rounding.md)另给任意K、固定M/Δ的实际改善；[三坐标与三态正规形](../current/unrelated_machines/degree_three_weighted_menu_cube_embedding.md)精确保OPT/V把任意normalized flat源降K3/资源度3再入zero cube，标准path已核BCG归属。[SC值桥/菜单数锐界](../current/unrelated_machines/normalized_weighted_menu_santa_value_and_size.md)只排同U逐玩家shortcut。原source无须先限K/Δ，剩余承重仍是norm1与全partial导出的tiny-gap NO decoder，主目标未解。

[笛卡尔菜单的反向放大与一致性差距](../current/unrelated_machines/cartesian_menu_recoupling_and_coordinate_consistency.md)：一个明确裸product实际OPT=1+2^-t趋1；额外逐坐标语义的配额却为floor((3/2)^t)/2^t趋0。两精确值排同族常数保值事后修复，尚缺真实负载实现的一致性；只否定该放大合同，非一般困难性。

[分块一致性、线性秩与全域缺项标尺](../current/unrelated_machines/cartesian_menu_block_coherence_rank_and_deficit.md)回收已完成的精确结构：bounded blocks才指数衰减，无环单输入链仍保1/2；q元affine重选与coordinate一致相反极限；并发投影给任意nonlinear缺项必要条件。均未实现物理coherence；主反向承重继续是低负载全局decoder，停止以更多局部tensor数值代替该义务。

[逐机统一内部索引交换](../current/unrelated_machines/machine_uniform_query_return_index_exchange.md)、[direct共居严格SAT及三半锐逃逸](../current/unrelated_machines/direct_cohabiting_query_return_strict_sat_and_sharp_escape.md)与[真实直线源/累计路径编译障碍](../current/unrelated_machines/line_set_packing_and_take_continue_compilation_obstructions.md)关闭各自精确接口；全部原jobs和全机负载已核，未关闭近二源NO的全局decoder。标准matching/Hall扣除新颖性，E曾误标签的proof-aware审查已另冻纠正，并由真正statement-first重构补齐。只有明确改变外部共同容量/partial AND机制时才重试这些具体桥。

[任意异权私有子句的三半上界与共享外端边界](../current/unrelated_machines/general_weighted_private_clause_exchange_and_shared_outside_boundary.md)：固定辅助内部single-query/single-return接口的3T/2交换可与真实变量环共同匹配，所有局部索引strict可选时整公式实际≤1.5T；不是私有outside免费替ring。标准四任务环与小query返回池允许共享外部身份，但孤立OPT1且未保变量一致性。重试须改变精确模板的共同容量/边界，不能仅在私有Hc增加异权aux；主源NO联合decoder仍未闭合。
