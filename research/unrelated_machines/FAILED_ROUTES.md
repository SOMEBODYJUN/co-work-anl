# 不相关并行机的已知方法障碍与回收接口

以下是已知障碍/适用范围，并非宣称本团队已逐一尝试失败。

| 路线与机制 | 准确失败位置和排除范围 | 可回收信息与重试条件 |
| --- | --- | --- |
| 从配置可行性T直接舍入到(2−ε)T | UM-CONF-GAP-v1两树族使OPT/T趋近2；排除该统一合同，不排所有使用配置的算法 | 仍可用配置识别重任务；须加入真正跨机器兼容性、强化下界或其他额外机制，并在同一gap族上说明作用 |
| 只加单机器有效配置不等式 | 每台机器的0/1可行配置凸包已被配置LP表达，这类切割不能切掉投影 | 多机器耦合约束不在此否定范围；须展示切掉哪个分数证书及分离/求解复杂度 |
| 固定r机器联合见证，但不同见证只共享单机边际 | 长链把终端容量冲突移到任意长环；所有≤r机器诱导森林，分别可耦合，CC_r阈值仍给gap趋2；精确身份UM-COALITION-PROJECTION-GAP-v1 | [正文](../current/unrelated_machines/long_path_coalition_gap.md)给严格合同。回收森林耦合与高围长生成器；完整多机overlap一致性不被排除，三机完整相容性已能解决本树宽2族 |
| 用2−1/m宣布统一常数突破 | 1/m随无界m趋零，不能给∃统一ε；这是量词不匹配 | 保留加性舍入工具；新界须有独立于m,n、精度和P的正常数余量 |
| 用restricted assignment/等边长图平衡直接推广 | p_ij相同的假设在异长两机例中失效；一般gap族正利用大小方向差异 | 比较每个转移/势/扩展路径的实际机器时间，提出明确迁移引理后再推广 |
| 用估值、局部搜索终止或准多项式冒充多项式构造 | 缺实际输出σ或总运行时间为输入位长的多项式；有限状态终止不够 | 可回收存在性、交换结构和阻塞树；需独立的迭代上界及位复杂度 |
| 有限测试未找到反例/平均表现优秀 | 证据只覆盖有限参数，不能证明全称最坏情况 | 保存准确oracle、实例、seed和证据范围，用来区分机制、攻击新候选 |

原arXiv配置gap构造的高度索引疑点已用独立基例/递推处理，见[正文第4节](../current/unrelated_machines/model_and_classical_barriers.md)。工具失败、403或全文未取得仅是访问状态，没有数学真值意义。

未来新增真实失败记录须写尝试、所依机制、失败步骤、具体反例/缺失条件、排除范围、仍成立部分与重试条件。不要只记录“某方法没用”。

## 已实际构造并攻击：逐星大边匹配残余

尝试：唯一小端任务通过大边匹配卸载；先局部匹配，后加入全部必经大边任务N。安全性与总位多项式已证，能逐层排除原两树证书，属于可回收接口。

局部版的失败：用终端路径的k−1个unit占位任务替代平行终端，给每条星任务不同终端；忽略N时会错误假设所有终端都空。加入N可修复这一点。

GHMR版的失败：占位任务都新增共同z上的1/2小边，故不再属于N。每个被强制大边查询可卸空当前U_i，但未匹配占位任务的小端总容量未计；不同查询也不要求共用一个调度。k≥4时二叉下传迫使至少四个占位任务去z，负载≥2，所以真实OPT仍2−1/k，配置T₀=1+1/k证书及GHMR首轮零删边同时成立。

准确排除：不能仅据“配置T可行＋本GHMR固定点通过”承诺统一(2−ε)T。没有排除联合匹配容量、嵌套探测、全部配置强化或UM-TARGET-v1。回收：安全过滤、简单支撑gap、共享容量攻击族及条件切面接口。[完整证明与证据](../current/unrelated_machines/heavy_matching_residual_and_escape.md)。重试须明确加入了哪条跨星同时容量信息并证明可求解/可舍入。

## 已实际攻击：二阶修复及计数闭包

尝试机制：用任务束二阶互补消除原配置证书，或以强制残余容量和基数外溢作安全删边。前者在原族强化阈值恰OPT，后者也在原族精确，证明与实现均仍成立。

具体失败：每原任务经capacity-one中间机器细分后，各机器对只共享一个任务。完整pair配置分布可由单任务互补边际拼出，计数闭包没有首次删除；整数障碍和原低目标分数证书同时保留。属于候选强度不足，不是健全性错误，也非原目标不可能。

排除范围：仅这些传播/局部LP值的统一(2−ε)T合同；不排跨三机器overlap一致性、先消去中间机器或相对OPT的其他机制。回收一般安全过滤、单调二分下界、配置证书提升及调度压回接口。重试需提供能穿过中间机器保留原两端信息的可计算机制。见[自足证明与冻结攻击](../current/unrelated_machines/bundle_coupling_subdivision_barrier.md)。

## 已实际定位：把共同大边选择当免费oracle

尝试在T=OPT先整体选择big匹配，再以small分数流接3/2舍入。条件舍入完全成立；失败在共同H选择并非普通匹配：无pins的完美3DM归约已在T1、N空、每job唯一small、时间{1/3,1}上编码精确选择，固定有理δ<1/3容量余量仍NP完全（P≠NP时不能免费调用）。这是接口选择强度过高，未否定近似目标；旧归约在δ=1/3失效；新半单位归约以不同输入身份覆盖整个δ<1/2，且将精确判定提升为对OPT≤T承诺构造的排除（条件P≠NP）。δ=1/2时全small，归约不再保真。回收给定H的完整构造和专用共享z族的条件块切面；后者确实修复整个族，但尚无一般分离/舍入。见[完整身份/证明/证据](../current/unrelated_machines/joint_matching_completion_and_block_cuts.md)。


## 已实际攻击：树再耦合后冻结任务再补全

尝试：从完整相容数据只保留生成树pair，再用残量LP/ST补非树任务。五机反例即使起点是真实全局T分布，tree-Markov支持也有1/4坏态使两端容量都耗尽，剩余唯一任务最优补全2T。失效属于丢失非树相关性，不是源分布不相容或ST错误。准确身份UM-TREE-MARKOV-COMPLETION-NO-v1，见[正文](../current/unrelated_machines/tree_markov_completion.md)。回收：至多四机连通树的中心覆盖保证T补全；本坏态一次迁移即可修复。重试应允许repair/聪明选态或保存非树相关性，不将此小例扩大成普遍困难性。

## 已实际攻击：先消去极小超载星再耦合两机器

消去是正确并可恢复调度的接口，不应随主路线失败删除。它修复长度二mid的隔离，却在中心/全局/局部三层容量一竞争中无可触发机器；全部任务≥3可用机，旧单/双域传播也无起点，GPC₂证书仍T1可行而OPT→2。失败属强度不足；回收精确min见证、逆序恢复与位多项式消元。

对q≥2外溢重复min会复用同一原任务，rank envelope又可能丢正向可行性；boss4一般profile证明排除q个普通任务的完整残余接口表示。保identity的matching/matroid接口、辅助结构或近似消去未被排除。精确域、一般证明、来源与证据见[自足稿](../current/unrelated_machines/minimal_star_contraction_and_capacity_gap.md)。


## 独立配置可行性加全部逐边LST探针

实际尝试是用强制每个分配边为1的普通LST测试修复配置gap，并配局部星匹配。它切原终端，但[稀释终端构造](../current/unrelated_machines/diluted_sink_probe_gap.md)保留整数一槽，扩大分数余量使每条边各有全局条件点；配置与全部测试仍有gap趋2。失败属于精确合同的真实反例，不是求解器失败。它没有同时在条件LP内保持单位任务基数，且星匹配遗漏其他阻塞任务占槽。回收容量稀释引理、显式条件证书和安全过滤。重试条件：将大任务槽/全局残余容量放进每个条件点；第9节已证明这种加强准确识别本族，尚未排除此新合同。


共享z再接入稀释族后，现行GHMR也首轮零删除；全部新增z边各有条件LST点。因此“GHMR后再做所有普通边探针”的精确合同仍失败。失败机制分别是共享小端容量未同时安置、终端额外分数容量未保单位槽。同行UM-ESCAPE-BLOCK-CUT-v1的条件不等式适用于此N终端替换，仍可修复该族，不扩大为所有条件化不可能。


## 全任务多槽匹配仍遗漏共同真实负载

实际尝试：将GHMR拓展到给定全行下界的多槽资源池，覆盖全部不能留中心的任务，再最大化当前中心卸载；该安全过滤及全池支配子池的引理成立。紧凑N=2k²族使每个被查机器可以在基数分配中完全空置，故每机任意配置也有延伸；但至少2k个中心同时接X时，各自需一Y去z，z负载≥2，真实OPT仍2−1/k。失败为必要条件强度不足：其他中心可在合法count内真实超载，不是任务身份复用或matching算法错误。

只排除正文全局单行/计数合同与GPC₂及列明预处理的合取，不排条件LST/config、每池重新提高H或共同真实负载算法。回收精确过滤、支配引理、compact/pair/avoid证书；旧条件块cut能修整个本族。重试应增加可求解且可舍入的跨中心条件容量，先核是否真正共用负载见证。见[自足正文](../current/unrelated_machines/row_count_escape_gap.md)。

半单位接口的honest salvage见[逐行前缀联合舍入](../current/unrelated_machines/joint_slot_prefix_rounding.md)：直接联合所有任务、不先固定H，可以在行宽≤2子类得3/2。已知工具推论不升级为一般新算法；真正未修复的是任意跨尺度容量，不是H精确接口本身。

## 固定阈值中任务配置与固定势均不能替代共同动作

新失败边界 `UM-MEDIUM-CONFIG-TINY-BARRIER-v1`：对任意固定有理 \(0<\alpha<1/5\)，经典两树族的 \(k=4,T=5/4\) 已使全部有限边 \(1/4>\alpha T\)，配置 LP 在 \(T\) 可行而 \(\operatorname{OPT}/T=7/5>1+\alpha\)。因此“配置 LP 加一次独立 tiny-ST 收费 \(\alpha T\)”在此阈值下完全退化为配置间隙；列数可枚举不等于 LP 到共同整数选择已有积分提升。它不排更强跨机器约束、改变分类或直接联合舍入。

`UM-FIXED-WORK-CONVEX-POTENTIAL-BARRIER-v1` 进一步给出固定松弛的参数化边界：\(h\) 个核心、每核心 \(q\) 个 home/tiny 私有叶、一个全核心时间1的大任务，\(t=(h-1)/(hq)\)，OPT=1。最小总工作量支撑及其标准槽匹配值为 \(2-1/h\)；取 \(q=h^2\) 时任何固定 \(W\le\rho h\) 仍有 \(C_{\max}\ge2-1/h-(\rho-1)ht/(1-t)\)。对固定有限非减凸 \(f\)，若 \(q>(1-1/h)(f(3)-f(2))/(f(1)-f(0))\)，\(\sum_i f(L_i)\) 的每个全局最小解也保留近二坏态。失败只针对固定正支撑/工作量/分离势；重开昂贵叶边、自适应 hinge、机器加权、非可加势与临时增载仍可重试。完整定义和 Fraction 小参数核验见[问题正文](../questions/unrelated_machines/fixed_work_and_medium_config_barriers.md)。

## 独立单边条件配置仍未保存共同相关性

尝试机制：把逐边LST探针加强为每次强制边内完整配置可行性，保住全部单机容量形状和大任务槽。新稀疏深树族仍接受：单次扰动沿α→rα衰减，仅有限深度的底簇须撤离；微小γ容纳这些簇的全部占位任务。但实际调度沿至少二叉分支扩散到深树全部底部，逼出γ2^(H−1)=2的负载。失败在不同查询没有共同相关性，不在单机配置或精确计算错误。

局部修补也有陷阱：路径支撑不能只凭总空槽数固定移出ceil(kβ−1)条占位边；应把坏簇全部k−1条撤走，原M预算已足够。回收稀疏全边配置证书、长距离分数衰减/整数分叉的区分，以及完整四机器交集联合分布的精确拼接逃生口。未排更强层级、消元后探针或UM-TARGET-v1。[完整证明与限制](../current/unrelated_machines/sparse_conditioned_configuration_gap.md)。

多行真实容量的§6锐界进一步排除只增加独立查询行数的同族补救：最多N−2k个中心与全部非中心行同时真实可行，仍有每配置独立见证；N−2k+1中心时pin z空才出现Hall缺口。失败机制是把2k个激活中心在查询间变换，不能拼成共同调度。一般共同相关/条件块强化未被排除。

## 全部单机完整配置分别延伸到全配置LP

尝试机制：每个单机配置各自强制为1，检验其余所有机器真实配置容量与任务覆盖，以安全删除无延伸配置。紧凑共享逃逸族每一个本地配置均可延伸，故无首次删除，OPT/T仍趋2。失败已不在单次证书遗漏其他机器负载，而在不同探针不共享同一base及条件混合一阶矩。回收全部显式有理延伸构造与多项式证书生成；把逃逸坐标与共同base联结可导出已有条件块cut。没有排除完整SA/LS、条件pair耦合、共同容量或OPT相对算法；也不能把一个失败本地配置当拒绝T证据。精确身份UM-MACHINE-CONFIG-PROBE-GAP-v1，正文row_count_escape_gap.md§7。

## 真最优凸包点加固定标准槽匹配仍不够

尝试机制：把共同大边接口换成全部任务联合ST，并希望只要分数点足够强，或在固定槽图里选最优matching，即能统一低于2。失败已定位到输出空间：m台identical机器、一个unit与m²−1个1/(m+1)任务，显式m个最优调度平均给x=1/m，但每机只有m槽且总槽=总任务，任何cover都强制每机m任务，大任务机负载2m/(m+1)。不是分数可行性错误，更不是原调度困难性。

回收：给定的凸分量可直接返回；任意槽输出只需把大任务机m−1个small逐个迁至其他机器，即达OPT1，且修改数最优。重试必须改变槽容量/选择另一点或允许跨槽联合修复；单纯更精确oracle或最佳同图matching无效。精确身份、独立攻击和实际证据见[自足稿](../current/unrelated_machines/optimal_convex_fixed_slot_gap.md)。

## 循环批量局部最优不能直接提升成统一近似

实际尝试：以缩放菜单支持任意批次，兼容线图寻找任意长机器循环，再用固定净余量保证总多项式终止。正面算法正确，未丢弃。失效步骤是从“Cmax≤2T且来自正支撑最小成本槽舍入”推断存在好循环：padding分流族有真实OPT1和唯一最小成本槽分配2−1/k，却没有任意非平凡、每机单目的地的makespan不增修复。

这是交换机制强度不足，非算法实现错误、非一般近似困难性。须允许同一机器向多个目的地同时撤离或保更强初始化结构；反例x违反配置big基数，故配置投影初始化尚未排除。无界批量与长循环分别必要但并不充分。完整算法、反例、逐量词范围及独立审查见[循环批次正文](../current/unrelated_machines/cyclic_batch_repair_and_fork_obstruction.md)。

## 不能把未缩放需求树或SA间隙直接当调度突破/下界

对需求树直接任务实例有OPT=2−b*。b*很小时，即使主目标算法也可能输出C≥2，无法从该未缩放输出解码正比例；免费把OPT写成1会使论证失败。回收为[有限阈值需求缩放](../current/unrelated_machines/rooted_dag_degree_token_bridge.md)§5：在τ=b*时scaled OPT才恰1，Γ只按显式出度枚举，避免巨大k。MMDA一轮SA间隙没有经过伪分布/层级保真，不能推出调度SA gap或复杂度困难性。

追加的实际失败：即使把初始化强化到真实OPT凸包，逐坐标非增循环算法仍不能用于全类统一改善。相同机器的总工作量守恒迫使每台负载不变；boss7固定槽族给近2的实际输入。准确身份UM-COORDINATE-REPAIR-ST-GAP-v1，只是已有族与守恒的直接桥梁，未重报新颖性。回收局部异质性减工作量工具；下一步须允许接收机增载而守住全局max。

## 固定真实最优边际的行包络与负相关

尝试保持给定x的行计数/负载，靠重排、偏移或固定额外槽改善。私有sink把整组OPT撤离在均匀边际中稀释为每sink负载1/r；固定a,b包络只准floor(ak/r+b)项，B所在home仍趋2。失败在输出合同阻止集中迁移，不在x松弛低估OPT。

取消逐次row界后，同sink pair-NC仍使碰撞对不足；期望/尾界与尖锐分布见optimal_hull_marginal_rounding_barrier.md。回收精确放大量与碰撞预算；换x、正相关迁移/选态未被排除。forest_boundary_contraction.md允许整批修复这些森林，故不作一般困难性。其单标量不适用于未证的多边界情形。


## 完整保留背包的固定数量拟阵交及精确总工作量保持

本轮实际尝试以原任务拟阵接口协调多源分流/合流。匹配可保身份，但一般背包若完整外包成p个拟阵交，单重件+k小件的最小最坏容量恰max(1,2−p/k)；固定p仍趋2。失败是局部接口强度不足，不是匹配安全性错误。回收精确分类、命中集公式和随p增长的锐门槛；辅助元素、选择性profile及全局择优未排除。见minimal_star_contraction_and_capacity_gap.md§7及UM-KNAPSACK-MATROID-ENVELOPE-v1。

另一补救猜想是选assignment-LP basic或最小真实工作量点，再保支撑/冻积分任务/精确不增总工作量。跨机小扰动使整个最小工作量面都丢掉必须用的边，尽管OPT/LST→1；相对OPT的输出比仍趋2。属于输出合同失败，不是一般下界差距。回收显式basic点和精确工作量修复阶梯：允许m−1件重开后仅增(m−1)/m工作量即OPT，相对成本增幅趋0，故不能否定任何固定乘法成本余量。见optimal_convex_fixed_slot_gap.md§6及UM-MIN-WORK-FACE-SUPPORT-GAP-v1。

## 冻结宏任务后重开全部微任务仍不足

实际尝试：保留ST输出的宏任务，只把全部tiny重放到所有有限边，允许任意多源多目的地、真实负载和精确联合优化。共享Z族有OPT1及真实最优凸分解产生的实际槽输出，但宏任务分占r个home后，2r工作只能放r+1机器，故精确最优2r/(r+1)趋2。失败在宏任务的共同占位，不在tiny舍入精度、槽图或逐行不增。

回收：尖锐迁移前沿ceil(2(r−d)k/(r−d+1))/k；固定改善必改近乎全部宏任务，而本族共同重选宏任务后直接可最优解。只限制上述固定/有限宏任务变动合同，不是一般近似困难性。再试必须共同选择宏任务及微任务卸载的共享真实容量。精确身份、独立冻结审查和双路实际枚举见optimal_hull_marginal_rounding_barrier.md§10。

精确双端Pareto集合可能指数大，不能推成无近似菜单：forest_boundary_contraction.md§9现有多项式相关菜单，一端精确支配、另一端乘性保零；独立取坐标min及普通job压缩仍不成立。任务不交挂件可共享边界求和，但一般核心选项及任意串行嵌套尚未闭合。槽族的单目的地修复可以整批严格下降，故本族不否定允许接收机增载的路径repair；一般实例仍未获进展保证。

先做极小星再独立CONFIG探针也不足以统一相对T改善：收缩后的三选稀疏族无规则且全部最终边可独立条件化，见UM-CONTRACTED-SPARSE-CONFIG-GAP-v1。失败机制仍是跨查询共享容量不一致，不是消元错误。回收UM-STAR-CONFIG-TRANSFER-v1的外部互斥/Q占用证书接口；无占用条件不能从整数等价推出CONFIG等价，逆向条件边也不可推。重试须加入共同相关性、更多规则或一般实际联合迁移。

固定宏任务的后处理边界没有扩大成联合选择不可能。UM-SHARED-SINK-JOINT-MACRO-v1把每home的整组实际撤离压成一个保零近似成本，并全局共同匹配宏任务；在单sink/唯一home结构可正确求和。将同一成本化直接用于多sink会丢同时预算，尚无此推广。见[正面正文](../current/unrelated_machines/shared_sink_joint_macro_assignment.md)。

## 既定条件矩运输不能免费视为同层重置

尝试：从共同对称条件矩删一机器并吸收包，仅将该机的旧choices确定送到后备机器，再使用RYRᵀ。失效是命题错误：显式均匀真实最优分布在任何吸收负载<2T时都有新true列超载；旧矩来自真实最优分布，且在T≤包负载<2T的区间残余真实T调度存在。正文symmetric_moment_reset_and_single_machine_threshold.md§3–5给精确反例。

回收：§2给任务聚合的逐列保留条件；§6证明同一个Rx在T包时可由真实匹配分解重建有效矩。因此反例仅否定既定矩的特定运输，不否定同层重新求解，更不是N(P) gap或主目标困难性。重试条件是可计算的重新耦合/改其他旧choices，并证明一般残余容量和输出复杂度。

## 激活边际不能代替共同拥塞与支撑搜索

尝试：用a_r=1、入流=a、出流≥ka及父激活上界x_vw≤a_v直接导出常数比例需求根树。失效：四段r-v-w-x-t族在a_v=a_w=1/q、a_x=a_t=1时全部满足，但同分叉的所有w强制复用同一个x，故真实b*=1/q。属于这项充分命题本身为假，不是工具失败；不否定强共同K证书、SA或一般调度算法。

回收：[共同流正文](../current/unrelated_machines/rooted_dag_congestion_flow.md)的分叉独立供给＋低点守恒＋同步接收容量可用一次整数流提取，固定W最小K也可求；但1/(2K−1)在该合同上尖锐。只有提供能选择好W/共同条件资源或改变合同的新信息时才值得重试；不把逐点边际条件当作已具共同证书。

同族的确定后备2T门槛不可外推到随机选择的新矩：新§9在m=2q时把精确包门槛降为q+2。它不改变旧RYRᵀ反例，因为随机任务选择需额外同任务对角修正；同样不能将限族矩输出误作实际调度算法。

## 跨路线拼接时新增的审查界面

局部菜单可以高效求出，仍不能免费在任意核心共同选择：单任务双边界菜单保留原双端分配问题。真实低秩矩可恢复仿射候选，但通用低秩真矩提取在全big半单位族中会恢复精确调度；不能以存在Dirac矩替代提取。阈值内修复也不自动是真实负载下降。准确推导、范围、可回收标准流标尺及未升级候选见[共同容量整合审查](../reviews/unrelated_machines/joint_capacity_route_feasibility_review.md)。没有排除一般主目标或其他矩/菜单机制。

多个sink并非一概阻断共同选择：[占位基与大贡献分支](../current/unrelated_machines/fixed_sink_occupation_rounding.md)在每固定K下可输出≤3T/2；不能把macro身份相关的完整匹配边菜单套用2K支撑引理，也不能取扩展空间basic点代替投影顶点。回收占位基交换与精确home DP；真正未解仍是K不受限、多home任务及一般统一ε。

## 真最优凸包初始化也不能补足固定机器严格下降

实际尝试：允许接收机增载、全量重开边和每机任意任务批次，但每次只考察固定数量机器上的严格lex下降。UM-OPT-HULL-LONG-CHAIN-LOCAL-GAP-v1的root宏微＋专属链实例在真OPT凸包点上，所有mincost槽输出仍2−1/k；任何新root任务迁出都迫整条容量释放链，而不改root的后缀先动只会恶化lex。因此最小参与机数d+2无界，非小任务数量或坏成本平局导致。

回收：精确任务/机器支持d+1/d+2、两个真实OPT分量、严格激活费用差、带标签独立枚举；链尾逐件中性Cmax腾空后再迁root任务直接成功。只否定固定σ上的有界机器严格lex邻域，不否定弱Cmax单调链、全局共同搜索或主目标。重试需允许中性容量释放并给一般可构造性及总步数。入口为[循环正文§10](../current/unrelated_machines/cyclic_batch_repair_and_fork_obstruction.md)。

## 不能把单位走廊复杂度当成所有支撑的枚举复杂度

原k≥K合同在K=1把单位需求点也当无条件供给，完整W会受不可达/重复汇流义务阻塞；这是原接口范围限制，不是根树困难性。回收：另立新2K阈值合同，全部守恒点/终端可免费加入，只有高点需要子集枚举，阈值缩放得到非单位参数精确算法。失效范围仍是一般h增长的2^h枚举，不能靠单位走廊或固定h特例消掉该因子。见[共同流正文](../current/unrelated_machines/rooted_dag_congestion_flow.md)§7–10。

## 多接收预算的标量化何时可回收

一般多sink任意资格下，最小加权和仍不能免费保证全部容量。新[完整profile池正文§9](../current/unrelated_machines/shared_sink_joint_macro_assignment.md#9-有界-profile-畸变的完整接收池)明确增加完整资格和给定共同work上下包络，才可由总work预算加逐边βT界恢复全部真实负载；允许macro真实退出，未冻结大小身份。回收范围是该显式结构；重试一般模型必须控制局部Hall容量或证明合用的分解，不能只把多预算再写成一个标量。

## 从配置gap种子到任意覆盖接线的soundness步骤失败

尝试：等倍复制机器/任务、逐incidence置换接线并消短环，希望每个输出继承原近2整数负载。失效是该普遍soundness命题错误：有理配置证书可被某finite cover精确实现成真实调度；再取高围长cover仍保持该负载。任意cover反而满足T_CONF不变、OPT不增。具体4机7任务种子OPT5/3、T_CONF4/3，6-cover可真调度到4/3，而恒等6-cover仍5/3。

回收：[有限覆盖恒等式](../current/unrelated_machines/configuration_finite_cover_obstruction.md)及输出敏感构造、自由字高围长存在性。否定范围仅所有接线/只凭高围长的合同；精选接线、扩张性、随机高概率结论和源相关PCP归约未被排除。重试须给排除坍缩接线的新全局限制、低负载调度的源解码及实际多项式规模。UM-TARGET-v1仍OPEN。

## 不完整资格可共同恢复，但任意残余容量不能免费当拟阵

[共同资格组联合流](../current/unrelated_machines/hall_group_joint_flow.md)不要求pool完整：每组真实最低出口给q槽Hall后，macro和接收资格可在一个整数流共同选。它回收无界sink数的正面范围，但依赖同组共同资格/等端体积和组总量下界。省去组下界可漏掉T真解，strict Hall不能把每机q槽降成q−1；任意有理接收余量的unit-demand可分流组族也不必满足拟阵交换（正文§6四个半容量sink负控制）。失败只限这些免费推广，不是一般近似困难性。下一步需一般分组提取或允许不同任务资格/异端时间的可恢复容量。

## 全空间HS贪心与过强小缺陷生成义务

实际尝试：对共同全局C₂矩压缩乘法，K₀取全空间恒等算子，每任务选择最大HS子分支。真实最优分布的完整四阶矩仍会在三机、先单位后八个1/4任务、最小机器标签平局下输出负载(1,2,0)。失效属于这个固定贪心合同本身，不是伪矩不可实现或缺少共同base；不排秩一初态、全部顺序或其他矩算法。

回收：同一个压缩接口有可检验的近平坦充分条件，给定小δ矩时可以精确有理提取实际(1+3δ)T调度。但不能把所有OPT≤T输入的此类矩生成当作免费oracle；它会要求过强的低于3/2承诺输出，P≠NP下已有半单位归约阻止这种补洞。应改变生成/舍入合同并处理大缺陷，或提供其他一般机制。[正文、独立攻击和冻结证据](../current/unrelated_machines/global_assignment_moment_rounding.md)保留准确范围，UM-TARGET-v1仍OPEN。

## 大配置间隙、高围长和多环数量不推出计算困难

尝试从两树近2配置gap删平行边、拉长局部环，直接用整数负载传播宣称near2 hardness。失效在源NP难输入和可靠性归约根本尚未建立：新[高围长仙人掌族](../current/unrelated_machines/cactus_configuration_gap_and_block_exactness.md)仍supgap2，却可用真实最小割点负载按块精确求解。每块只是一个长环（b1），总环数与高度可很大。

回收：稀疏循环窗口配置证书、g任务/g−1内部容量的末端强制、最大顶点块环秩2^b poly精确算法，以及单环连通分量CONFIG精确的锐结构区别。b按每个labelled任务计数，绝不能合并平行束后声称精确P。重试hardness须逃出b=O(log L)可解输出族（P≠NP条件下），或用support>2/全局一致性源解码；b无界本身也不够。未证明主目标反面。

## 私有递归无放大与完全元素池丢失NO

尝试用半单位3DM/需求树桥梁的既有困难性放大近2。私有终端递归的具体失效是乘法预期错误：精确值取min；所有固定根门/串接的一元格闭包在保YES=1时输出≥原β。完全pool共享的失效是soundness错误：克隆把分母r分数完美匹配整数化，四边NO在双克隆及直接坐标张量所有t≥2变YES。

回收：[两个精确恒等与反例身份](../current/unrelated_machines/private_graft_and_resource_repetition.md)，不是主目标反证。只排上述明确重复合同，不能排其他共享/一致性归约。重试条件：增加真实整数一致性且证明任何小正比例树仍解码源矛盾；还需对每固定ε有合法规模界。原SA gap、原配置gap或更多失败均不能填这个步骤。

## 固定阶压缩丢失新鲜任务与最高次数的相关性

尝试：固定真实最优矩、V_r与A_e，从1开始逐任务最大化‖A_eψ‖²。失效类型是命题错误：任何固定r都有真实最优源，任意顺序的每个普通任务都严格选机器0，比例(n−1)/(4r+2)，并非平局瑕疵。根数界控制每个真实源态，低阶独立性却令评分只见单任务概率；被截掉的是h_eψ_=r。可回收精确评分恒等式和一般nT上界，给线性量级；不能扩成层级gap、OPT估值障碍或所有谱方法不可能。重新尝试须实质改变真正条件化、矩重建或共同容量反馈。正文、审查、代码和冻结证据见[准确入口](../current/unrelated_machines/truncated_multiplication_vector_greedy_barrier.md)。

## 真实最优矩不自动保证固定投影向量规则守容

尝试：从真实T可行（甚至最优）分布压缩出Ae，ψ初1，每job选max||Aeψ||²后左乘，期待其共同正矩与容量localizer给统一余量。

失效机制：压缩更新不保已选事件的真实交支撑。严格多数后重复相同指示仍严格获胜；一维事件支持子空间使幂收敛到该事件并遗忘此前互斥重任务。正有理fullcube实现全部算子，三机全正时间校准使真实OPT=T1而输出>k−1/2；不是抽象PSD伪实现或零时间遗漏。五机五单位任务另有无辅助的严格2倍证书。

回收：精确多数/持续性/净化及可计算有限事件链；全部压缩若交换则是真实投影，可保T。只排固定给定μ/固定任务顺序/固定更新，不排换μ、重新条件化/耦合、调序、修复或UM-TARGET-v1。再试必须给保过去共同支撑或可恢复容量的额外不变量，不能只增加同一真实矩的阶数。一般副本数没有poly(k)声称。完整证明、scope及双路证据见[压缩向量正文](../current/unrelated_machines/projected_vector_greedy_unbounded.md)。

## 加权组出口替代固定组数预算

此前共同资格组的正负下界限制属于固定q槽Hall接口。新[加权出口联合槽](../current/unrelated_machines/weighted_group_joint_slot_rounding.md)允许W_h∈[0,T]，不设正下界、接收机数不固定；尺寸d_h=(W_h−T/2)_+经共同LP和带home容量的槽流，实际出口≤d_h，得到home≤(3/2+δ)T、sink≤3T/2。旧q槽反例仍限制旧接口，不可外推为缺少组下界时所有联合算法失败。共同资格/等端时间/唯一home的分组仍承重，未给一般UM转换；主目标仍OPEN。

## 单层共享资源只把近二 soundness 变成逐层配额 gap

尝试：用根—选择点—配额中间点—共享资源的单层需求树，把源匹配的完整领取层 (t=K) 当作唯一一致性测试。

失效机制：该接口有精确恒等式 (b^*=\max_{t\le K}\min(1,\nu_t/q,t/K))。任意正评分树都给出一个 (t=\lceil Kb\rceil) 的不交 (t)-资源族；反向任何这样的族都能直接构树。因此只压低完整 (K)-层的匹配数，不能排除中间配额层的低比例树。有限审计覆盖4788个全枚举实例和100个随机边界，普遍性来自两向证明。

回收：这把下一归约义务具体化为所有 (t>\delta K) 同时满足 (
u_t/q\le\delta)，同时YES必须保有 (
u_K=q)；需要跨层编码/高距离一致性，而不是继续复制同一资源池。该结果不是近二困难性，也不证明 (
u_t) 的一般复杂度。

## 仿射互补加 dummy 不能自动恢复固定基数

尝试：将 Santa 效用编码为 (p_{ij}=B-\lambda u_{ij})，补 dummy 资源到每机 (q) 件，再从任意近似 makespan 输出按数量裁剪，借此把 Santa 困难性直接变成近二调度困难性。

失效机制：在等基数子类中才有 (L_i=qB-\lambda u_i) 的互补恒等式；对任意 (1<\rho<2)，只要整数 (q\ge1/(\rho-1))，全同效用实例就允许 (q+1/q-1) 的 (\rho)-可行溢出。更具体的 (q=2)、\(\rho=1.9\) 两机矩阵中，makespan 为 (1.5OPT) 的三件溢出解按数量裁剪后把源最小效用从2降到0。增加 (B) 以阻止溢出又使互补效用项相对基线变小，近二比率趋近1；这只是该仿射黑盒接口的参数边界。

回收：若要重试，必须加入非仿射槽/过载选择器，并单独证明位多项式输出的整数基数和源效用保真；不能把乘性makespan界当成等基数证书。精确正文、独立复核与Fraction结果见[仿射边界](../current/unrelated_machines/affine_complement_cardinality_boundary.md)。


## 成对冲突资源不能自行实现近二整数一致性

尝试机制：每对不相容标签共享一枚资源，增加束宽/标签数以迫低比例树解码一致赋值。具体失效：资源处单射着色后，每变量至少有一种颜色承担1/Δ需求，某颜色又保留1/Δ变量；Δ2始终留下真实b≥1/2，奇数束宽也成立。成对相同束达到1/2，故不是舍入分析松。

回收：一般异质束1/Δ真实树、按局部比例排序的组关联度(2−1/Δ_G)实际调度、逐束宽锐例及重数必要条件。只限制四层变量私有标签/终端资源合同；不排高重数、跨层选择器或一般困难性。重试须让所有局部完整选择都产生足够高碰撞并证明低比例实际树的源解码，且保YES与位规模。见[正文](../current/unrelated_machines/bounded_collision_label_resource_floor.md)。


## 提高束宽不能省略碰撞规模与根整数计数

从成对冲突切换为高重数并扩大标签束，仍未完成近二soundness。整束缺陷着色的真实容量匹配给Λ_c；平方池q=Δ=K=t²精确b*=1/t，并直接可构造最优调度。失败位置是将高重数/大K当作源NO解码的充分理由；它们只可能满足必要条件。

回收有限Λ公式、共同池精确界、原资源匹配以及η必要不等式；沿η→0且ηKmin→∞必有liminfη²Δ≥1。没有大需求或趋零条件不能扩大该渐近结论。重试必须构造真正源相关的一致性并证明任意低比例树可解码，同时保持YES和位规模。见[正文](../current/unrelated_machines/large_bundle_collision_square_root_floor.md)。

[全局四阶负载松弛的锐利二间隙](../current/unrelated_machines/c2_unit_multislice_gap.md)（`UM-C2-LOAD-UNIT-GAP-v1`）已闭合裸C2-load本身的义务：m≥3,n=m+1单位同机上T_C2=n/m、OPT2，显式有理PSD证书给supgap2。这不同于固定贪心坏例；其三阶同机矩为负、CONFIG阈值2，故不含C2+CONFIG或一般算法困难性。该裸C2命题的范围不变；后续[弱H2合取的新二间隙](../current/unrelated_machines/weak_h2_configuration_moment_gap.md)另行关闭只共享一阶CONFIG的合同。共享行二阶在该新族上阈值精确，一般强合同与UM-TARGET-v1仍OPEN。

## 弱单调小步的闭环失效及可回收临时超额

尝试以中性预修普遍补足旧严格lex长链搜索：闭环族把尾边正回流到已满root，任意局部后缀先增root，任何Cmax非增非平凡动作必须完整激活一个新环。全部最小成本槽初始化来自真实最优凸包，最小改件/参与机恰d+1，可随规模线性增长。失败属于该修复合同本身错误，不是主目标困难性。回收：单任务路径到OPT的最小峰值精确B+c，c=1/k²；只需微小暂时超额，且该cactus可精确解。重试应允许可控超额或原子长环，并证明一般共同守容及总进展。见[闭环正文](../../research/current/unrelated_machines/cyclic_batch_repair_and_fork_obstruction.md)§11。

异端时间也不是一概阻断共同选择：上下比例包络可把真实出口转成κ预算，用b_hz d_h成本排序及同一home容量流恢复所有sink。只有上包络时LP必要性仍失效；共同资格/唯一home仍承重。见[有界畸变正面合同](../../research/current/unrelated_machines/distorted_group_joint_slot_rounding.md)。

单任务复制端口的纯内部一致性接口已由[向下投影锐界](../current/unrelated_machines/signed_one_job_port_downset.md)限制：移出任何入向端口只减少内部负载，两一致态遂强制混合态；精确计数逐参数可达到。失效步骤是把一般PCSP变量多次出现免费复制成两端真实任务。只否定保留外部出现槽、外部容量不参与投影的single-job接口；外部共同容量的两任务负控确能等值。可回收的是计数/零值处理/已有见证的实际混合构造；重试必须改变为多任务编码或共同外部一致性并证明完整调度低负载解码，不能只增内部辅助图。

[三host可用性复制的锐三半障碍](../current/unrelated_machines/three_host_selector_sharp_three_halves.md)排除“只用a或同时用b,c保完整YES、两单输出坏侧都推近2”的独立空/满预载接口：非负行权二色闭包可实际拼接出某坏侧≤3T/2，任意加大内部图或多任务仍不能改变。失效步骤是把满载机器视为近似调度中完全不可停车；实际NO允许的剩余容量必须计入。同一机制给SC三特殊item复制的half锐界。回收二色闭包/实际拼接/逐台预载核验；重试必须改外部联合状态/解码合同，不从此排所有gadgets或一般算法。

[整束冲突偷换的具体失败](../current/unrelated_machines/duplication_state_majority_floor.md)：残余label只需选择部分孩子，行/列全束交叠不能禁止二者同时出现在真实树。sK4可选5组各3格得5/8；旧所有K≥s的1/2锐性撤回，正确的多数下界和K≥2s锐例保留。重试需按每标签整数配额的真实Hall容量解码，不能用全束交叠图代替。

[增加独立预载扇出不能消除缺一逃逸](../current/unrelated_machines/weighted_fanout_profile_boundary.md)：给only-a与all-B实际YES，则任意输出pair的两个缺一OPT和≤3T；内部图增大、多任务、任意源端时间均不能让每缺一状态接近二。只有one-output-free的星虽可2−1/q，也不满足这个NO合同。回收加权闭包与真实状态预算；重试须给跨模块共同容量或另一读出合同及完整源解码。

[仅严格端正确的双轨阈值编码无法自动保留近二NO](../current/unrelated_machines/dual_rail_threshold_soundness_boundary.md)：C1确等价源严格解，但C>1可只外送真轨一部分ports。scalar整类及unit外部容量整类均有实际3/2；全cube源连弱端也NO却实际OPT趋1。否定范围仅明确归一化/单例外合同；可回收整数流、原P锐例和cube精确式。重试需不同的跨层一致性/相关选择以及对所有低负载实际σ的可靠解码。

## 门槛覆盖的固定前缀恢复缺口与回收

尝试：用最小覆盖FPTAS成本e构造共同sink槽，再输出另一个固定前缀。失效步骤是前缀越过需求d，可能比e更重；T1、τ1/2、权(2/5,2/5,1/5)给前缀4/5、最小覆盖3/5。5r组OPT1族还使代理总成本1/2、真实sink负载r。失败属于输出/证明耦合错误，不是主目标困难性；同行4300c26据此正确撤回完成状态。

回收：本次直接恢复同一覆盖X，使真实成本=e；另修正大单件UB忽略小件覆盖的问题，同时比较两类可行UB，并明确截断精确覆盖DP。修复经独立冻结核查后保留原结构合同与one-sided搜索，不把旧review追认为正确。重试其他输出集合前必须重计真实成本或另给统一误差预算。见[纠错复核](../reviews/unrelated_machines/threshold_cover_and_support_release_review.md)。

前缀矩旧双3/2互补例只改变literal，完整B负载恒3/2，bit-only测试漏检。替换为单非零bit任务保留原存在性Claim，新增实际端、整机负载和精确PSD核验；不限制算法重耦合。rank-jump抽象toy的错误任务守恒补齐说法也已删除，不能拿未满足完整假设的toy当反例。

[加深私有树或重排半密度unit读出仍不能放大到近二](../current/unrelated_machines/unit_readout_pruned_forest_boundary.md)：唯一unit incoming+k枚总small负载1让半质量槽匹配给全高度三半，涵盖所有arity≤2A wiring。改d>2A若仍全正负degree平衡，非空源严格YES已空；补dummy须防纯dummy配额子树并核共同外部容量。失败范围不超出明确成本/私有结构/密度；可回收一般forest IFF、树命中门槛及同64open真OPT1对7/4，后续需真实非此域联合soundness。

[仅把clause密度提高到另一个固定D仍不足作任意近二归约](../current/unrelated_machines/unit_readout_calibrated_cardinality_slots.md)：校准计数槽给每固定D统一2−1/(4D)结构类算法，即使k,h增长。D可以随目标ε改变，未被一般排除；仍需实际YES和所有pruned森林NO解码。强基数LP一般只充分，不能用不可行偷判NO；弱激活LP又不支持舍入。回收精确见证/两反例/有界密度算法；重试须真正避开共同基数证书。

## 逐机器价格与局部 anchor 不能免费交换全局选择

尝试对每个非负机器价格优化big匹配，再用残余light流，希望由所有价格各自通过推出同一个匹配。失效在凸化：这些测试精确等价任务守恒+big分数基数+LST容量，仍包含经典CONFIG趋二族；不是价格oracle不可算。原两机数值例还遗漏δ>3/20分类范围，且OPT>T，只能说明量词交换。漏掉p≤T剪枝时甚至固定m损失m。回收显式最小费用流oracle、精确min–max身份及最优价格共同big面的可检验成功证书；普通扰动价唯一不足，面失败不能作OPT>T证据。逐机anchor凸化也含CONFIG，a_i>0不能给统一ε。重试须新的跨机器状态/实际联合舍入损失，不是更多价格或专族样本。详见[自足正文](../current/unrelated_machines/heavy_light_price_convexification.md)；此为已知工具的接口综合，非一般不可能性。

## 不能从固定残余次模免费推出共同角色选择

尝试用残余throughput的次模性选择大任务占位。正确部分是任意异端p的固定R容量格次模；失效步骤有两处：占位损失D本为超模，且H同时移除任务与扣容量后V根本不继承次模（2×2原OPT1/2、四值2/1/1/2）。即使宏身份固定、tiny同尺寸，任意固定严格次二α的可行占位族仍能精确为任意图独立集，D=诱导边数，故不是免费拟阵或固定p交换系统。回收一般F性质、primal/dual求值证书与精确图表示；原实例都有显式OPT1，不是调度困难性。重试需同时保留R(H)、h(H)的共同恢复与实际联合舍入余量，不能以近似总通过量代替全任务完成。见[完整范围](../current/unrelated_machines/residual_throughput_and_occupation_projection.md)。

## 完整树的一致性不能只检查叶数或少数完整模式

尝试忽略祖先而把叶流直接当配额森林会失效；回收为只删除同一flow叶、用锐hitting阈值真正提取祖先，任意密度固定h得到1+2^(−1/h)实际近似。尝试让少数完整YES模式覆盖的坐标混合在近2被拒绝，也被给定见证的锐2−1/(2p−1)重组界限制；另一轨必须固定parent，不能误用全轨强LP。具体失效、全局原任务计费、每p锐profile及N<p反例见[正文](../current/unrelated_machines/unit_readout_global_leaf_flow_and_selector_mixing.md)。

否定范围仅本完整私有单位树和同一P的给定完整见证；NO输出可能没有这些见证，固定h与p也可随目标gap增长。下一需真正跨层一致性与任意低实际σ的源解码，不能把这里的条件边界写成一般近二困难性。重试应给出脱离这些合同的完整P，而非新增同一参数样本。

## 同一一阶CONFIG合取与槽损失凸化的失败机制

尝试：把C2-load共同四阶矩与完整CONFIG共享同一一阶点，或将完整实际槽损失逐机凸化，期望统一跨过相对T的二倍壁垒。失效：稀释星族中，条件激活块的单位multislice伪矩容纳b+k任务于b+1资源，但激活仅1/k，使同一一阶资源占用恰1，CONFIG1完全看不到该条件超额；实际整数OPT仍2−1/k。参数化PSD/所有localizer和同x配置均已证明，不是有限搜索反例。

回收：一般N≥m+1的degree2 multislice PSD及可显式生成的条件张量/混合；共享同机二阶后，零pair的PSD传播给任意端条件单槽容量，从而**整个同族强阈值**精确等于OPT。失败只排弱H2，不排强二阶/三阶非负/其他算法，亦非一般困难性。准确Claim、证明及审查沿[同一正文](../current/unrelated_machines/weak_h2_configuration_moment_gap.md)读取。

另[完整槽包络](../current/unrelated_machines/slot_envelope_and_configuration_identity.md)精确区分两个常混淆动作：固定容量后凸化子水平集恰CONFIG；先凸化上图则只剩线性负载。非凸min max包络本身等于OPT，因此没有免费共同选择。重试必须新增跨机相关机制或给可计算近似非凸进展；只精确计费单行损失或重新调价不够。

## 严格单位阈值的整轨标签编译

尝试：用私有任意深双树把C1的源标签解码直接延伸到近2 NO。失效机制：CONFIG1精确消元为可求整轨LP；多数轨有activearity≤2A，再只对active轨建槽给完整五三σ。失败范围为严格(1,ρ>5/3) promise gap，不是否定所有此类实例或其他threshold。可回收：全阈值正部多面体、k1精确流、闭合两树精确Tconf。重试须改变严格单位合同或跨轨/跨机耦合，并重证低σ的源解码；单增树高/总arity无效。见[正文](../current/unrelated_machines/unit_readout_configuration_threshold_polytope.md)。

## 首步可算不等于全程进展，小幅临时预算也会锁死

尝试允许接收机增载，以一个缓冲机器沿链迁移，期望首次可动即有全程守容。一般首步U=max(2T,C+T/2)确可计算，计数证明与单向NO保留；但移动后可超原2T，直接迭代失去假设。迁出量小于缓冲超额还可能同时产生第二个缓冲机器，单链不变量不足。

新的精确障碍不是同族数值样本：对每C/T∈[1,2]及固定批量k，m=k+1环族OPT=T、任意非空≤k改变后值≥U，且单件到指定另一最优调度的最小峰恰U。C=T允许零步到最优集合，孤立图只取C≤B<U。坏初态不声称来自ST/配置最优凸包，不能升级成这些初始化或一般困难性。回收首步计数与显式峰值路径；重试须给新的缓冲集合/共同容量及总进展。见[正文](../current/unrelated_machines/pruned_first_move_and_transient_peak.md)。

## 逐价重选不能保证纯自洽重轻角色

尝试：对残余轻任务求最优机器价格，再在该价格下选最便宜的 heavy matching，迭代至固定点，借此把 `∀λ∃H` 变成共同 `H`。自洽条件本身是正确的充分证书：若 `λ_H` 是固定 `H` 的残余 makespan 最优对偶且 `H` 在同一 `g(·,λ_H)` 下最小，则 `H` 全局最小化残余值；但它不是一般存在性条件。

精确失效：对任意 `β∈[1/2,1)` 的两机三任务参数族，`OPT≤T` 且全局最优 placement 的自身最优对偶会严格偏好另一个次优 placement，反向亦然，纯 saddle 不存在。这里必须保留被重 placement 覆盖任务从轻基线中扣除的 `−μ_j(λ)`；忽略该项会改变接口。回收是可核验的条件证书与最佳响应边界，不能把局部迭代或逐价 oracle 当一般算法。见 [自洽对偶正文](../current/unrelated_machines/heavy_light_saddle_certificate_and_cycle.md)。

## 逐行均匀平层读出不能仅靠跨测试相关压低支付

尝试用同一源标签控制许多测试来挽回独立局部guard的soundness。对simple、逐复合行均匀、每right资源数等于其degree的准确合同，整数碰撞势加一次全局匹配总能保每点ceil-half，flat原sigma≤3/2。因此共享标签本身不够。可回收的是实际共同标签/资源算法；重试需非均匀行、有效多重请求、跨资源组耦合或多层祖先约束，并重证全部机器与源解码。删除假设的反例仅否定绝对负载延伸，不否定更大类另一三二近似。见[正文](../current/unrelated_machines/row_uniform_correlated_guard_rounding.md)。

## 私有树分叉不能无损转为XOS下包络

[精确包络](../current/unrelated_machines/private_tree_branching_valuation_and_minorants.md)证明single-state全叶值的加性下包络损失G=k[1−(1−1/k)^h]可达Theta(logB/loglogB)。这只否定统一常数、逐点支配的XOS下替代合同，不否定其它估值算法或一般UM次二。可回收精确demand、blocking分离与紧凑single-state LP；重试必须保留真实祖先兼容或补偿这个损失，不把oracle障碍当NP-hardness。

## 统一端口数量加unit parking不能把fractional gap升级成实际hardness

[同一结构的两份合同](../current/unrelated_machines/uniform_port_parking_matroid_gap_and_actual_approximation.md)：每C vacancy-independent且uniform边际属于P(M)仍有1/D共同保留；但真实最佳保留β*可由published two-value polymatroid算法常数近似，普通UM得到2−1/(4+η)。失败是把βLP1误当完整integer YES。可回收精确OPT=2−β*、Rado计数和显式Hall家族；重试需真正退出该合同，不把更多aux/大LPgap当新计算障碍。

## Ordinary non-delta扇出不能原样保近单位promise

[精确源与塌陷公式](../current/unrelated_machines/near_unit_implication_pcsp_and_physical_copy_obligation.md)区分一般PCSP真NP-hard和物理编译缺口。pin一out0、量化k−3个out，strict为b⇒y=z1，weak为b⇒y+z≥max(0,r−k+3)；r≤k−3后weak完全无约束。失败是把ordinary最小support在weak端也当最小，不否定更大promise gadget、实际循环或多尺度设计。可回收精确strongfixing源与三型合法任务语义，重试必须给共同source decoder。

## 仅增加small可选端或复制裸unit-presence不能免费补decoder

[原生多端的双流与exact正规形](../current/unrelated_machines/near_unit_implication_pcsp_and_physical_copy_obligation.md)表明：每job至少2小端且small行≤k有实际五三；balanced k小端类strict阈值只剩unit匹配。真正全输入表达力可保在SU两端+unit-only三端，未变成可求解源。

[两实际见证胶合](../current/unrelated_machines/unit_presence_two_witness_sharp_gluing.md)进一步排裸machine unit-presence的抗弱阈值复制：uniform给逐k锐B，任意tiny a<1/3给绝对<2。失败是把unit方向或局部onehot当可无损复制label；不排medium端、任务身份/外部联合状态。可回收exact normalform与actualgluing；重试要给完整低负载σ到source解码，不能只改更多原生端数。

## 按component一次收费不能自动导出短list

中等环/多label路径的导出补入只给总O(|B|)标签规模；每右点取两公共像原像已经能用≤2|B|标签使全部right agreement。[精确度数预算](../current/unrelated_machines/list_agreement_degree_budget_and_decoder.md)还给确定性线性地板及每图锐的全agree阈值。失败步骤是把总预算当逐左list或逐right局部s_b；可回收参数检查，重试须给真实P中每新label多incidence费用/正确局部预算，不能只拉长cycle或增加code distance。未否定其它归约或主目标。

源预算本身的logg障碍已被[线性degree源](../current/unrelated_machines/partial_minrep_linear_degree_source_and_fee_bridge.md)绕过：更低原cover配rare上尾，而非普通常数尾界。但把source度数改成O(g)没有实现实际首label费用；旧component一次收费、拉长cycle或code distance仍须逐job核c/F。重试条件为真实π接口、constant-fraction trigger及固定费的完整P；未否定其它归约。

[坐标切片编译](../current/unrelated_machines/coordinate_slice_source_compilation_counterexample.md)的fatal为每对手坐标只删一个值，全树仍D−1叉。已给完整P、NO精确OPT1+1/D、保源NO的private-output padding，以及双射/均匀纤维/CONFIG1反例。只否定该叶共享与坐标顺序，非一般q或UM；重试须改变实际跨test耦合。


[v3正则高围长源](../current/unrelated_machines/partial_minrep_linear_degree_source_and_fee_bridge.md)消除“复制后任意lists失控/删环破正规性”这一特定源接口障碍；靠rare-tail同时性与有限switch，不是任意lift保hardness。高girth和正则性仍不能替代实际weak调度的源解码。


均匀私有完整状态树若叶map各自单射且对所有源都保CONFIG1，则无论任意菜单/端口编号，actualOPT≤5/3；因此它不可能提供近2的NO源soundness。失效环节是把源不一致自动变成叶资源不可pack，Haxell给出反向存在。参见[完整边界](../current/unrelated_machines/private_injective_tree_configuration_floor.md)。重试需超出该精确域，不能仅独立重编号；这不否定一般UM或非注入近二CONFIG族。


私有uniform树仅靠有界每state叶重数的CONFIG证书不能免费给任意near2 NO：上界2−1/(μ+2)，所需μ至少约1/δ。平星可精确解却有G一阶趋2，所以参数gap也不是算法困难性。见[重数界](../current/unrelated_machines/private_injective_tree_configuration_floor.md)。单tree源虽在全局重数3已NP完全，仍只k3小比值；低重数SAT逻辑门不自动放大分叉gap。

共同b且每行≤2正非unit资格的近二承载已由[实际sharp3/2算法](../current/unrelated_machines/joint_slot_prefix_rounding.md)排除；不是只相对CONFIG障碍。重试需退出此域并核全原job身份和共享负载；不推广至三small/不同big时间，更不否定主命题。

[现有三叉底层palette的对齐张量/纯收缩](../current/unrelated_machines/ternary_rainbow_subtree_exact_hardness.md)已严格失败：张量YES的实际OPT=2−(2/3)^k，gap≤5/4且趋1；纯k≥2收缩连strong(d−1)也无。重试须改变上述具体操作/着色，而不是只允许QP展开。另[单树µ精确gap](../current/unrelated_machines/private_injective_tree_configuration_floor.md)有CONFIG(1+1/d)却q=d/µ，故近全strong分叉不能换为CONFIG promise；仍非所有方法/算法困难性。

## 强配置相容不等于真实共同二阶law

尝试用本行CONFIG全部同阶矩+全局固定阶PSD直接抽取保给定二阶的重匹配分布。失败是接口本身错误：[奇数切片K22编译](../current/unrelated_machines/strong_configuration_matching_moment_obstruction.md)的所有短事件非负、全部负载恒1，却使整数选块数形式方差为0而均值半整数。回收自足harmonic PSD、精确位长和锐修复半径1/[4N(N−1)]；该半径趋零，所有实例显然OPT1。只排精确保矩接口，重试应允许定量改矩/直接共同实际选择；不据此否定强松弛的实际舍入。

[永久缓冲激活与共同解锁路径](../current/unrelated_machines/permanent_buffer_activation_and_priority_deadlocks.md)给锐分数窗口[1/3,1/2]和静态/优先级反例；[保留坏环与实际最大件全程锐界](../current/unrelated_machines/held_cycle_release_and_assigned_max_path.md)用共同保护来流及源补集证明：每个正阈值源有一件eligible时，给定目标的完整路径可构造；并覆盖标准有序槽实际输出。局部promise类峰U逐参数锐，不冒充实际ST输出锐性。具体τ仍是承重输入，未知目标、任意剪枝初态与一般统一次二输出仍OPEN。

单件函数图没有安全断口不再是给定目标路径的真实障碍：保留坏环边时，所有其它入流统一受S+Q−β<U保护，源补集再激活坏环。旧证书仍准确失败，不能据此否定路径。真正剩下的是无单eligible且不满足实际最大件初态promise的共同动作，以及未知τ的全输入选择；见[新正文](../current/unrelated_machines/held_cycle_release_and_assigned_max_path.md)。

2026-10-18：[一般双见证查询分离的锐3/2费用合同](../current/unrelated_machines/two_witness_query_separation.md)；[单正小端级联的完整查询立方体](../current/unrelated_machines/single_home_cascade_query_separation.md)；[超立方分组菜单的Hall保留与锐3/2实际界](../current/unrelated_machines/coordinate_slice_source_compilation_counterexample.md)。一般双见证tiny query的单次改派费不能复用为near2固定激活费，准确分离阈值3/2且sharp；单home全留初态另有完整query cube；超立方分组菜单全类actual≤3/2（DGR特例19/15）。失败范围仅精确合同；非OPT困难性，UM-TARGET-v1正反面仍OPEN。重试须改变读取初态聚合量/费用/源相关接口或slice真实结构，并给完整实际decoder。


[单件query计数与近单位读取必要条件](../current/unrelated_machines/two_witness_query_separation.md)另立QUERY-COUNT-FEE-v3：即使聚合大，tiny单件仍有大批合格低费query；一次费用W≤F迫至少d−2枚query初态>(β−1)T。原η0严格错误实际修复并保留；仅双strict改派收费合同，非主反证。


[严格重中端gap占位胶合](../current/unrelated_machines/unit_presence_two_witness_sharp_gluing.md)新增HEAVY-MEDIUM-STRICT-WITNESS-v1：两actual≤T，只用过端有heavy/medium间隔κ，则两mixed实际≤(2−κ/2)T，允许跨角色；仍不读具体job身份。同期修复公共尺寸满流遗漏冻结baseline guard及孤立机，不升级tiny审计为通用后端。


[保护环公共子句OR的身份错配](../current/unrelated_machines/near_unit_implication_pcsp_and_physical_copy_obligation.md)新增CLAUSE-OR-FAILURE-v2：此明确Ci+Rc+unit-clause接线对任意公式都actual≤1，源NO全部丢失；共同匹配证书可回收，重试须阻止返回blocker与导出query索引交换，不能免费加同编号约束。空源idle已修，非所有identity-copy不可能。


[两组资源加权菜单的联合近似](../current/unrelated_machines/degree_two_group_bounded_menu_joint_rounding.md)新增DEGREE-TWO-BOUNDED-MENU-JOINT-ROUNDING-v2：每resource跨≤2groups、每组≤K显式states、private总量≤1，group平均接已有VW2近似给完整实际C≤2−(2−OPT)/(2K)≤(2−1/(2K))OPT，bonus精确保OPT；Q2/K7任意cell权也在27/14结构界内。不是先big匹配再diffuse补全，非generalUM；menus2的unit阈值另可2SAT。
