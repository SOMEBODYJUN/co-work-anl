# 不相关并行机的当前研究前沿

主目标 `UM-TARGET-v1` 仍OPEN：尚无一般确定性位多项式统一(2−ε)调度算法。

已有经典地基、原始文献和本轮[大边匹配残余及共享逃逸反例](../current/unrelated_machines/heavy_matching_residual_and_escape.md)。新限范围资产为：安全位多项式GHMR过滤器；简单机器支撑下仍有配置gap2；加入必经大边匹配虽识别原两树和路径占位瓶颈，但共享小端z使其首轮完全不删边、真实OPT/T仍趋2。详见[精确账本](CLAIMS.md)、[冻结独立审查](../reviews/unrelated_machines/heavy_matching_escape_review.md)。这些是新接口/反例，不是主目标的近似突破，全球新颖性未认证。

真正瓶颈更精确为：单个星的最优撤离匹配忽略其余任务的小端负载，也没有一个同时满足所有机器残余容量的共同匹配。共享z族是新候选必须经过的攻击输入。下一高信息行动是构造跨星的条件容量切面或可求解耦合松弛，并检验其是否切掉整个逃逸族，而不只排除当前一份证书。整体选择大边整数匹配再接小边分数补全的接口也需检查其自身复杂度，不能当作免费oracle。

仍须闭合：一般统一余量、全部机器同时负载、实际分配、oracle与总位复杂度。困难性归约、2005完整舍入和受限指派局部搜索仍未全部独立复原；需要时按承重条件核原文。下载、重构、有限核验、内审、外审及新颖性分轴记录。

新获严格边界：`UM-LONG-PATH-GAP-v1` 把经典两树终端平行任务替成长链，保留OPT=2−1/k与T=1+1/k证书，获得任意大围长简单图。`UM-COALITION-PROJECTION-GAP-v1` 证明每个固定r、仅共享单机配置分布的r机器联合投影仍sup gap2；不能称作完整SA障碍。正文和独立审查见[新入口](../current/unrelated_machines/long_path_coalition_gap.md)。标准树分解耦合又证明完整三机交叠一致性在这批树宽2族上精确，给出了真正缺失信息的界面。

下一可判别义务已收窄：让不同局部见证共享多机相关性，并控制一般图的求解/舍入复杂度；或整体消去可解的低树宽挂件，保留其真实边界负载接口。单边界挂件只需一个可实现最小负载，多边界则不能逐坐标最小化（单任务两端即可反驳），完整Pareto表也可能指数。尚无证明把一般输入的大任务限制在可消去挂件中。此接口观察不另冒充新算法或新理论成果。

优先行动：

1. 先独立复核经典舍入/gap的承重细节及已有审查异议，复跑有限证据；不用通读全部旧仓库。
2. 对新候选给精确接口：新增跨机器约束、组合下界、交换规则或其他机制；在两树gap族上推导它是否真正提供信息。
3. 对小输入求精确OPT，找退化/零边/极端尺寸/异长两机反例；有限实验只能区分机制。
4. 形成可复用引理、表示、反例或障碍后及时保存，并明确它如何接近主目标；没有信息增量时不制造资产。
5. 承重外部定理按需逐步重构。LST困难性归约、2005完整舍入、受限指派局部搜索等仍不是本专题已独立复现的证明。

路线可变，不设方法白名单、排他认领或固定轮数。新颖性和独立论文价值需持续对照最接近结果；通用目标的潜力不替代对新数学内容的实质评价。

## 新候选的具体进展与失效

强制残余容量计数闭包（UM-CARDINALITY-CLOSURE-v1）保留任意T可行调度、单调且确定性位多项式，并可清分母二分得到B≤OPT；在原VW族B=OPT。聚合二阶bundle约束同样把原族强化阈值推到OPT（UM-BUNDLE-MOMENT-v1）。这超过原单机配置证书的信息，但仍不够一般近似。

任务细分将瓶颈藏在两子任务共用的capacity-one中间机器，保持整数OPT=2−1/k及配置证书T=1+1/k；简单图上完整两机器配置coupling可从边际构造，因此其sup gap仍2（UM-PAIR-SUBDIVISION-GAP-v1），计数闭包在T≥1无第一次删除。证明、审查和有限范围从[正文](../current/unrelated_machines/bundle_coupling_subdivision_barrier.md)进入。boss4已有更一般长链独立推导，后续复用共同资产，不重复树族。

下一步具体义务：能否先有效消去这类中间机器，同时保留一般实例的可行性和输出提升？再攻击多个容量一资源共享的情形。不能把消去一个细分gadget当全类结论。

## 当前可判别的共同容量接口

[共同选择与条件块切面](../current/unrelated_machines/joint_matching_completion_and_block_cuts.md)已把下一步细化：给定共同H与small分数容量，ST直接产生(3/2+δ)T调度；固定有理δ<1/3的精确选择NP完全，甚至N空且每job恰一个small端。旧1/3归约本身未排该区间；新半单位身份已在P≠NP下排除整个δ<1/2的(Aδ)保证构造。共享z族现可由每末簇Z_g≥(r_B−1)Y_v加祖先配置行整体排除，强化阈值恰真实OPT；这不是一般块分离或gap定理。

后续优先：利用联合槽舍入的实际损失，或研究能识别条件块且有可控求解/舍入的松弛。固定δ<1/2的(Aδ)共同见证保证构造已由半单位归约排除（P≠NP）；逐机只改负载加max仍失败。共享z只修专用族，不把‘又切掉一个族’升级为突破；一般多小端任务和长距离完整相关性仍承重。


生成树提取路线新增精确断点：UM-TREE-MARKOV-COMPLETION-NO-v1的五机实例中，真实最优分布经指定tree-Markov再耦合，坏态冻结树任务后最优补全恰2T。[正文与一步修复](../current/unrelated_machines/tree_markov_completion.md)说明缺的是非树相关性；并未排除择态、换树或迁移。当前还缺一般repair/相关保存机制的统一余量及总位多项式证明。本轮内部探索没有形成可提升的主目标算法；有限高树宽筛查未给可靠一般结论，不入Canonical。

## 可恢复消元后的真实瓶颈

UM-MINIMAL-STAR-CONTRACTION-v1已给精确T消去及任意残余调度B→max(B,T)逆恢复，可重复且总位多项式。它能还原长度二细分；但[紧凑容量一星族](../current/unrelated_machines/minimal_star_contraction_and_capacity_gap.md)在T1无极小星或单/双域传播，仍有全部GPC₂ pair witnesses，OPT=2−1/k。此族基于已知SC资源机制，全球新颖性未认证。

boss4给出的UM-STAR-Q-JOB-COMPRESSION-NO-v1共同采用：q≥2个普通任务不能保相应星的全部残余容量profile，须保不同原任务身份。下一具体路线是强制资源任务Q的匹配收缩与最大撤离权W，而不是逐机min envelope；h>T/2的单槽版本与boss3 GHMR重叠，后续优先复用其共同资产。多槽/小候选只是标准匹配工具的适用范围补全，目前没有统一余量证明。


逐边条件化有新的可判别断点：UM-DILUTED-SINK-PROBE-GAP-v1在T=1+1/k同时通过配置可行、全部边独立强制LST和局部星匹配，而OPT=2−1/k。稀释引理说明N(T−1)额外分数容量没有对应整数槽。[正文](../current/unrelated_machines/diluted_sink_probe_gap.md)第9节给安全位多项式加强：在每个条件LP内部保留大任务基数，准确识别本族；尚无一般近似保证。下一义务是为“配置可行＋加强条件探针”找统一舍入，或构造真正通过它的新族；不能把未加约束的条件点当共同配置。


UM-DILUTED-ESCAPE-PROBE-GAP-v1进一步使配置＋全部普通LST边探针＋现行GHMR合用仍gap2。新增共享1/2小端后下界经四活跃底簇重证；条件内基数/配置及同行块容量切面没有被此族排除。当前新增信息需求是条件内共同守恒，不是更多相互独立证书。


## 全局资源计数接口已完成核验

多槽/全任务身份路线已由UM-GLOBAL-ROW-COUNT-FILTER-v1精确化；固定全行下界的所有子池可以一次全局匹配涵盖。UM-COMPACT-COUNT-ESCAPE-GAP-v1却给N=2k²的紧凑攻击族：每台机器均能在计数见证中空置，所以任意单机配置/强制边独立延伸都通过，GPC₂(1)可行且OPT=2−1/k。无极小星/旧计数传播起点。正文与真实有限证据见row_count_escape_gap.md入口；这不是条件LST或条件配置反例。

现有块cut对该族仍精确：全局激活边际至少2k，与每块条件逃逸相乘使z负载≥2(r_B−1)>B。故继续给本族专用修补的信息价值已低；关键未解义务仍是一般条件块的可分离表示或联合舍入，不能免费使用NP难的整数激活选择。

## 直接联合舍入后的当前跨尺度义务

[直接联合槽的正面衔接](../current/unrelated_machines/joint_slot_prefix_rounding.md)给UM-ROW-SPREAD-TWO-ROUND-v1：删去零任务后每行正时间跨度≤2（逐机尺度不同）时，显式前缀计数LP加一次全任务槽匹配给3/2位多项式构造。它是VW/ST已知机制的直接推论，绕过过强(Aδ)见证；未消除一般行内跨尺度混合，主目标仍OPEN。

当前缺的是任意行内大小混合时仍有统一余量的联合容量或交换机制。零任务可以精确删除，但一般tiny任务不能免费丢弃；逐行量化还必须证明任务覆盖、误差累积和总位复杂度。下一行动应固定这个跨尺度保持义务，优先检验其在两树、共享容量和半单位例上的行为，不再把(Aδ)承诺选择当开放免费步骤。

## 当前更强的条件探针边界

[三选稀疏深树](../current/unrelated_machines/sparse_conditioned_configuration_gap.md)已证明UM-SPARSE-CONDITIONED-CONFIG-GAP-v1：不仅普通LST，连每条边分别强制后的完整配置LP也各自可行，而整数OPT/T仍趋2。机制是单条件扰动几何衰减与整数同时二叉扩散的分离。不同条件点无共同基点/交叠分布，故不构成完整层级下界；完整四机器bag一致性在该族上反而精确。路径端点星消元可触发，本结果未排其后续强化。

前沿因此不再是单纯给每次探针更多单机不等式。下一高信息行动是让条件点共享多机相关性，或证明可恢复消元与联合大小任务迁移能保留统一余量和位多项式输出；仍无主目标算法。半单位共同匹配窗口以同行已核UM-JOINT-HALF-PROMISE-NO-v1为准，不继续把δ∈[1/3,1/2)作为开放的普遍Aδ构造路线。

紧凑族已推进到尖锐多行预算UM-COMPACT-MULTIROW-EXTENSION-v1：即使全部非中心机及N−2k个中心同时守真实容量，每个独立配置pin仍可延伸；再多一中心且pin z空则存在失败。这明确了局部见证失效并非只因只查一行。新增强度只有共同相关性/实际联合舍入才可能跨越；本族专用cut已精确，不继续制造同族的微小修补。

## 完整条件证书仍缺共同base

UM-MACHINE-CONFIG-PROBE-GAP-v1已将“加强每个探针”推进到全部本地合法配置各自可在完整配置LP取概率1。紧凑族T1仍OPT=2−1/k，原基数/pair合同同时成立但未在条件内部重新耦合。已有共同逃逸一阶矩立即导出块cut；下一高信息行动应选择可计算共同条件容量或直接联合舍入，不能继续把独立条件LP可行性当成一致性。证明/双路实际证书/独立冻结审查从row_count_escape_gap.md§7进入。

## 联合槽路线的真实OPT断点

UM-OPTIMAL-CONVEX-ST-SLOT-GAP-v1在完全相同机器上给OPT1及显式真实最优凸分解，所有固定ST槽matching却恰2m/(m+1)。问题是逐机ceil期望任务数的容量，连选择最佳matching也无法避免。所有支撑边均正，分数负载恰真实OPT，并非LPgap。该族可以一轮跨槽迁移恢复最优，见[正文](../current/unrelated_machines/optimal_convex_fixed_slot_gap.md)。下一义务必须允许改变槽输出空间/保留联合配置或repair；单纯让x更强不够。一般统一余量及位多项式迭代仍未解。

## 可求解循环批次与初始化后的分流缺口

UM-ROBUST-CYCLIC-BATCH-OPT-v1已给固定η的实际局部优化器：exact-profit菜单＋严格转向＋重复机器剪接，≤4m/η成功轮，终态无ηT鲁棒循环；并未给近似比。UM-BATCH-SUPPORT-REPAIR-NO-v1要求同机撤离任务数无界；UM-FORK-MINCOST-ROUND-REPAIR-NO-v1的正支撑padding甚至使最小成本槽分配唯一，值2−1/k，但任何每机单目的地的makespan不增repair皆无首次变化。

范围关键：该x不是配置投影（A上big质量>1），未称basic，不能据此否定配置初始化。下一高信息义务是可共同实现的多目的地分流合流，或一个能排除该相关结构的具体初始化不变量；仅正支撑、总成本不增或增大循环菜单不足。自足入口为[正文](../current/unrelated_machines/cyclic_batch_repair_and_fork_obstruction.md)与其冻结审查/实际证据。

## 严格下降邻域的机器规模与可回收中性路径

UM-OPT-HULL-LONG-CHAIN-LOCAL-GAP-v1在两个真实OPT调度凸组合与全部mincost ST输出上给C=2−1/k，严格lex改善的最小参与机器数恰d+2。它排除固定机器邻域的严格下降假充分义务；不排弱Cmax单调算法，本族从链尾逆序腾空后单件迁入即可改进。证明、槽证书和独立270336全调度审计见[循环正文§10](../current/unrelated_machines/cyclic_batch_repair_and_fork_obstruction.md)。下一高信息行动是在一般实例找可共同实现、允许中性预修的容量释放结构，并证明总进展界；不是扩大固定严格下降邻域。

## 用实际需求树检验联合迁移

[压缩任务桥梁](../current/unrelated_machines/rooted_dag_degree_token_bridge.md)给真实OPT=2−b*与任意C<2调度的实际根树解码，而不是LPgap。大k填充和正确有限阈值缩放已闭合位复杂度；已知MMDA必要方向并非原创成果。一般联合repair需要同时维护unit激活与子资源唯一性。独立攻击已覆盖边界和缩放；Bamas2025一轮SA陈述已定位，但未做任何调度层级保真。主目标仍OPEN。

循环批次正文所述“配置初始化未排除”仅属于fork的单目的地、makespan非增范围。新UM-COORDINATE-REPAIR-ST-GAP-v1证明本逐坐标优化器本身即使在真最优凸包槽初始化也会0轮、gap→2（boss7族＋守恒直接推论）。因此纯逐坐标单调不再是全类改善候选；接收机上升但全局max受控的多源容量接口仍是实际未解义务。

上述“配置初始化未排除”仅属于fork的单目的地、makespan非增范围。新UM-COORDINATE-REPAIR-ST-GAP-v1证明本逐坐标优化器本身即使在真最优凸包槽初始化也会0轮、gap→2（boss7族＋守恒直接推论）。因此纯逐坐标单调不再是全类改善候选；接收机上升但全局max受控的多源容量接口仍是实际未解义务。

## 真实最优边际与可恢复批量迁移后的前沿

固定x的row/count输出合同已被UM-OPT-HULL-ROW-DISCREPANCY-GAP-v1精确限制；UM-OPT-HULL-PAIR-NC-GAP-v1给保持边际且同sink pair负相关的尖锐近2期望/成功界。不是松弛低估OPT，而是禁止集中整组撤离。

UM-FOREST-BOUNDARY-AUGMENT-v1现给实际单边界标量：真实根负载不高于任何原内部T解，内部资源误差局部付费并按max恢复。classic gap的机器bundle支撑是树，可用本接口；此结构FPTAS已有先例，不作新全局算法。

当前真正缺口：一般多边界/有环高树宽核心上，如何可计算地联合集中迁移，保持统一余量与总位多项式进展。一轮条件矩固定后不自动保留同层系统，不能免费迭代；同族小切面改进也不关闭主目标。

## 联合迁移候选的新准确边界

[多拟阵容量外包](../current/unrelated_machines/minimal_star_contraction_and_capacity_gap.md#7-原任务地集上多拟阵容量外包的精确损失)与[最小总处理量面](../current/unrelated_machines/optimal_convex_fixed_slot_gap.md#6-最小总处理量的整个最优面也可能丢掉修复边)新增两个准确接口边界：保全部本地可行集的p拟阵交最优容量损失max(1,2−p/k)；basic且整个最小处理量面的支撑也可近2OPT，即使OPT/LST→1。两者均为已知工具的简单扩展，不能排除一般联合迁移；重新开放零质量边和允许真实工作量上升仍是下一义务。

## 大小任务共同重选与浅层正面构造

UM-FROZEN-MACRO-TINY-REOPT-GAP-v1允许微任务全部有限边和真实全局重优化，仍有精确值2r/(r+1)；UM-MACRO-MIGRATION-FRONTIER-v1量化达到固定2−ε必须改r−O(1/ε)个宏任务。故仅把tiny LP重开不能作一般充分步骤，宏任务共同占位本身必须可变。正文为optimal_hull_marginal_rounding_barrier.md§10。

正面UM-DEPTH-TWO-HALF-v1对r→U→W异质需求、任意共享终端，给半比例实际根树及相应token族3/2调度；无树宽约束，按需求位长多项式。它是标准贪心收费的限域构造，未解决再多一层的共享资源，也没有一般统一ε。下一步应探索能同时改变宏任务并保真实共享容量的可计算标量/相关接口，而不把浅层或tiny单独改善代替主目标。

[双边界森林的相关菜单](../current/unrelated_machines/forest_boundary_contraction.md)：`UM-FOREST-TWO-BOUNDARY-MENU-v1`给a精确支配、b乘性保零和实际任务见证，任务不交挂件共享边界可求和；菜单共同选择与串行嵌套仍需新机制。

[同机槽族的单目的地修复](../current/unrelated_machines/optimal_convex_fixed_slot_gap.md)：`UM-ONE-DESTINATION-SLOT-REPAIR-v1`给最小迁移m(m−1)/2，并可整批沿路径严格下降至OPT；仅此显式族，接收机允许增载。

两项均已自足证明、独立内部攻击和有限精确核验；都是限结构正面接口/修复，未认证全球新颖性，不形成一般输入的统一ε。UM-TARGET-v1保持OPEN。

端点预处理缺口已按新身份闭合：每步外部配置互斥保证CONFIG双向与条件边前向转换，支持S+r、位复杂度计入显式证书。稀疏族P_k收每底簇两端后无极小星，全部最终边仍可独立强制，OPT/T→2。不是所有预处理或共同base的否定；下一高信息义务仍为一般相关保存和联合容量，更多同类独立探测不提供统一余量。

[单共享汇点的共同宏任务匹配](../current/unrelated_machines/shared_sink_joint_macro_assignment.md)：UM-SHARED-SINK-JOINT-MACRO-v1。∀给定H∪{z}、仅homes可用且每有限边>T/2的宏任务、各任务仅在唯一指定home与公共z的非空子集可用的私有组、二进制有理T≥0及0<η≤1，有确定性poly(总位长,1/η)算法返回FAIL或实际调度，所有home≤T、z≤(1+η)T；OPT≤T时必成功，故FAIL蕴含OPT>T。私有任务无需尺寸上界，宏任务图任意。 每个macro/home或empty模式的真实最小整组撤离成本，保零乘性覆盖DP与带dummy成本的全局最小权完美匹配；误差只对同一个真实sink预算求和，不按home数量累积。 仅单共享sink与唯一home的给定结构，宏任务每有限边严格>T/2承重；成功不判定T精确可行，不含一般多sink/多home转换或统一ε。标准覆盖背包+匹配的组合接口，未认证新颖性。 一般UM-TARGET-v1仍OPEN。

## 对称矩重置后的准确前沿

[任务聚合、单机矩运输阈值与同边际修复](../current/unrelated_machines/symmetric_moment_reset_and_single_machine_threshold.md)给UM-SYMMETRIC-JOB-AGGREGATION-v1及UM-SINGLE-MACHINE-MOMENT-RESET-THRESHOLD-v1。前者是给定R的可检查列条件；后者在真实最优分布上区分既定矩推前需2T与同Rx重新耦合只需T。不得写成Rx不属新N或同层求解不可能。读取链：CLAIMS→正文→symmetric_moment_reset_review.md→双路代码/实际q2输入与证书/symmetric_moment_reset_audit.json。

一般不相关输入中如何可计算地重建共同条件容量、输出统一低于2且保证总位多项式进展仍未解决；本结果不提供R搜索器。标准凸锥和二分图工具保留来源，全球新颖性与独立论文价值未认证。

## 共同拥塞流之后：固定支撑已可求，支撑选择仍开放

[共同流正文](../current/unrelated_machines/rooted_dag_congestion_flow.md)闭合一次整数流提取及固定W最小整数K搜索。K单调的拓扑重分配避免按数值扫描；1/(2K−1)由层宽2^d−1族精确达到，不能仅改分析提升合同保证。全支撑最优κ*满足(1+1/b*)/2≤κ*≤ceil(1/b*)，说明寻找好W仍携带真实树选择问题，而不是已解决的固定W流。

一般activation LP即使加x_vw≤a_v仍被四段单位汇流走廊族击穿；它不是强共同证书。下一高信息义务：从一般输入/阈值承诺中构造有用W或保留其共同条件路径容量，并证明统一K与实际输出；不得先知道好树再选择W。当前没有通过攻击的一般W算法，不继续制造同一LP的小修补。UM-TARGET-v1仍OPEN。

同一正文§9另立UM-INDEPENDENT-UNIFORM-MOMENT-RESET-v1：独立均匀转移旧删机choices所生的新矩可确定精确计算，最小包q+2、负载1+2/q，q≥3严格小于固定后备的2。必须修同任务对角；一般m不保此界、个别态仍2T，故只作为限族正面运输，不提升主目标。双路实际矩/原分布coins枚举及冻结审查从正文进入。

## 跨路线整合后的可判别前沿

[冻结整合审查](../reviews/unrelated_machines/joint_capacity_route_feasibility_review.md)确认已有真实局部构造，尚无一般统一ε。菜单全局选择已含unrelated graph balancing；DAG-token任意深度且非根需求有固定上界时已有标准最大流标尺，不能只加深路径当新机制；真低秩矩存在不等于可提取。最新阈值repair仍缺真实进展势，失败不是不可行；单sink共同macro接口靠可加真实成本耦合，多sink需另证整数选择。优先判别一般共同容量/重新耦合与总位进展，不重复独立探针或把局部修复当全类保证。
