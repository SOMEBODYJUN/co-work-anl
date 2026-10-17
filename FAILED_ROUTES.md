# 失败路线与准确否定范围

当前主攻 `UM-TARGET-v1`，存档 `unrelated-machines`。新题的[配置LP障碍、模型迁移和复杂度误用](research/unrelated_machines/FAILED_ROUTES.md)单独维护；新增长链反例精确限制仅共享单机边际的固定机器联合投影，未限制完整多机overlap相容性；逐星匹配另被共享小端容量击穿，保留安全过滤接口；五机反例另限制任意树再耦合态冻结任务后的低于2补全合同；这些方法边界与配置gap都不证明一般算法目标为假。下列旧题记录保持原范围。
此前拥塞题已有[线性次数的全状态严格反例](research/current/weighted_congestion/linear_degree_allstate_lower_bound.md)，准确否定普遍Cd/ln d保证。旧同类clock路线缺失的全前沿覆盖已由新专用健康输入另证；全局极差预算及通用strict-sweep反例仍有效。

共同大边匹配再补小流的精确选择也有明确[3DM接口障碍](research/current/unrelated_machines/joint_matching_completion_and_block_cuts.md)，新半单位身份排除所有固定δ<1/2的上述见证承诺构造（P≠NP）；主目标与其他调度接口仍未排除。

这是全仓入口。失败记录属于数学资产：须说明尝试机制、具体失败步骤、反例或缺口、排除范围、仍成立的回收结果及重试条件。

| 研究模型 | 当前最需避免的误用 | 详细记录 |
| --- | --- | --- |
| **当前：不相关并行机** | 把独立见证当共同多机容量；把固定槽/矩运输失败当一般调度不可能；把子类、估值或见证选择困难性当主目标答案 | [本题失败与回收](research/unrelated_machines/FAILED_ROUTES.md)、[精确账本](research/unrelated_machines/CLAIMS.md) |
| 加权拥塞 | 把潜在尾部参数或DAG端点检测限制误当实际博弈阈值；把奇环正局部证书的 ceiling 当全类存在上界；把固定人数或小资源支持游戏当增长下界；把尚待审的势障碍升级为普遍不可能 | [分支失败与回收](research/weighted_congestion_frontier/FAILED_ROUTES.md) |
| 两阶段设施选址 | 将有限终止当位多项式；将固定续局的失败当全部续局反例；把相关机器排程公式直接套到客户费用 | [准确失败目录](research/FAILED_ROUTES_FACILITY.md)及[多设施前沿](research/current/multi_facility/polytime_frontier.md) |
| 顺序客户吸引 | 将末位保证当所有早期玩家保证；将失效安全值/税桥误认为半覆盖反例；忽略真实离轨回复 | [原有逐项反例与回收](research/FAILED_ROUTES_FACILITY.md)、[模型地图](research/current/customer_attraction/README.md) |

旧对话、程序失败、断网、模型评价或有限搜索未找到反例没有数学真值含义。整理和发布不自动提升命题状态。

[正占用核的低背景检测失败](research/current/positive_kernels/occupancy_rank_faces.md)给出准确回收：底背景混合差分在有限正锥可判低秩，但归一化高次full-support核使其趋零、极限仍高秩，故无稳定质量预算且不能交换闭包截面。顶背景测试修复为正的锐gap；固定正质量与非负混合仍承重，不推一般签名或均衡结论。

加权拥塞新增两项准确失败范围：[择证平稳/回返支撑的额外要求](research/current/weighted_congestion/template_certificates/stationary_selector_obstruction.md)与[唯一源私有侧分叉的UF放大](research/current/weighted_congestion/directed_fanout_forcing_cut.md)；详见主题失败记录，均不否定一般存在机制。

[统一低泄漏锚定时钟预算](research/current/weighted_congestion/uniform_clock_budget_barrier.md)现有普适障碍：任意输入和anchor均αlnq/q<1，不能靠改输入环完成全类否定；只限制该充分预算，实际时钟差及非均匀架构仍开放。

[不同步前沿反例](research/current/weighted_congestion/class_front_phase_quotient.md)阻止把严格原环自动推广到每个类前沿端点；内部离前沿改善仍可能存在。[局部矩表示](research/current/weighted_congestion/template_certificates/selector_local_moments.md)也不允许丢selector支撑的全局兼容性或把parity可行例当暂态必要。两项的准确范围与重试条件见主题失败记录。

[共享侧资源与真实clock的限制](research/weighted_congestion_frontier/FAILED_ROUTES.md)现区分：UF下同权共享side仍有目标量级PNE；保环总预算只是必要条件；firstopp失败不等于PNE；43次固定证书不代表最优次数或增长反例族。

[动态层秩的拼接缺口](research/weighted_congestion_frontier/FAILED_ROUTES.md)已区分固定共占height势与逐步换秩：换秩改变势，长实际链不代表无PNE，低单点height也非PNE必要；真正缺少累计图/SCC出口或瞬态dual。

[异权全签名刚性](research/current/weighted_congestion/template_certificates/selector_local_moments.md)排除了从低cost interaction degree直接推出全小用户支持的完整成本保真表示。失败是正资源锥的全用户极射线，非维数计算错误；≤D资源数量压缩仍成立，改权/辅助玩家/只保均衡lift的归约不受此结论排除，详见主题失败记录。

新增两项可复用方法失败：[完整成本近似小支持归约](research/current/weighted_congestion/template_certificates/selector_local_moments.md)即使允许改权仍须付人数相关失真；[仅追加同类有序三元clock](research/current/weighted_congestion/class_front_phase_quotient.md)在固定strict sweep输入保留严格精确PNE，任意次数/幅度均不能修复。前者不排辅助玩家或均衡lift，后者不排跨类/其他arity或更高倍率专用输入类；具体收费机制、反例与重试条件见主题失败账本。

[真实环余量依赖与完整锥暂态必要性](research/weighted_congestion_frontier/FAILED_ROUTES.md)分别限制仅依结构参数的actual保环次数、recurrent/点质量dual；均保留特选健康输入或一般瞬态dual的开放接口。

[奇环缺陷择证的补偿链](research/current/weighted_congestion/template_certificates/selector_local_moments.md)排除了固定数量移动者的dual截断：等权可行例仍需全部玩家两方向质量，最小支撑随人数无界；只限制局部拼接，不否定一般存在。

[降序侧势全局最小点与森林扩域的准确失败范围](research/weighted_congestion_frontier/FAILED_ROUTES.md)：同一E的全部global minima均可有近R改善，因此global-min择优不能消局部比；单环也可无exactPNE，单根森林报价不能无证用于有环或多根。两个反例均不否定全类目标，具体可回收接口及重试条件从主题失败账本进入。

[固定hub响应不能自动提升](research/current/weighted_congestion/fixed_hub_light_threshold_response.md)：unique-light子游戏虽有已知FIP并有显式单遍响应，hub偏离仍冻结旧light状态。重选后比较不等于真实单方偏离，现有反例已排除直接lift；可回收阈值接口，仍须新的跨hub兼容预算。

[稀释终端](research/current/unrelated_machines/diluted_sink_probe_gap.md)反驳独立配置＋全部普通线性边探针的统一阈值改善；条件内加入大任务槽可修复本族，所以未排除更强探针或主目标。


独立配置＋GHMR＋所有普通LST边探针的联合合同也被稀释共享小端族击穿；仍不排条件内基数/配置及块容量信息。

半单位新身份已关闭固定大小分界的共同见证窗口：每个固定δ∈[0,1/2)的(Aδ)存在性NP完全；P≠NP下无总位多项式OPT≤T承诺构造。它仍不是统一低于2算法的困难性，下一步转向实际联合舍入损失。见[共同选择正文§3a](research/current/unrelated_machines/joint_matching_completion_and_block_cuts.md)。

全局多槽匹配的[紧凑共享逃逸反例](research/current/unrelated_machines/row_count_escape_gap.md)说明：即使每个查询覆盖全部资源任务，其他机器只守计数仍能把真实超载移到不同中心；不排条件LST/config及共同负载。安全过滤与全池支配引理保留，条件块cut可修本族。

[稀疏深树](research/current/unrelated_machines/sparse_conditioned_configuration_gap.md)使所有单边完整配置探针各自通过，仍有gap趋2；失败在查询间共同相关性缺失。坏簇路径占位须整体撤离，不能只用总槽计数。完整交叠一致性、星消元后探针和主目标未被排除。

完整单机配置分别强制到完整配置LP也不足：紧凑族在每项探针内部守所有机器容量，仍无共同条件base而gap趋2。可回收显式完整y证书；共同逃逸一阶矩/条件块cut未被排除。该性质非一般可行的必要条件，安全操作仅删除无延伸配置，不能因某一失败配置直接拒绝。

[固定ST槽图的真实最优凸包反例](research/current/unrelated_machines/optimal_convex_fixed_slot_gap.md)否定“更强分数点＋同图择优matching”这一充分接口；全局最优凸分量都可被槽基数排除。本例跨槽迁移即恢复1，不排一般repair或UM-TARGET-v1。

[循环批量局部优化的分流缺口](research/current/unrelated_machines/cyclic_batch_repair_and_fork_obstruction.md)：总多项式终止不保证近似改善；逐坐标版本在真最优凸包槽族也零轮停滞。另一单目的地makespan非增fork边界仅限一般LST点，二者范围分开。 新增§10的真实最优凸包长链族：全部最小成本槽输出仍近2，严格lex修复的最小参与机数可任意大；链尾中性预修明确可行，故不限制弱Cmax单调路径。

[固定真实最优边际的逐行偏差与负相关方法边界](research/current/unrelated_machines/optimal_hull_marginal_rounding_barrier.md)已有精确反例及尖锐值。该私有sink族直接可最优解；只排固定边际输出合同，重选点/正相关集中迁移和一般近似仍不受排除。

原任务固定数量拟阵完整外包与最小总工作量面保支撑均有新的[准确失效及回收](research/unrelated_machines/FAILED_ROUTES.md)；不能升级为一般调度困难性。

## 冻结宏任务后重开全部微任务仍不足

实际尝试：保留ST输出的宏任务，只把全部tiny重放到所有有限边，允许任意多源多目的地、真实负载和精确联合优化。共享Z族有OPT1及真实最优凸分解产生的实际槽输出，但宏任务分占r个home后，2r工作只能放r+1机器，故精确最优2r/(r+1)趋2。失败在宏任务的共同占位，不在tiny舍入精度、槽图或逐行不增。

回收：尖锐迁移前沿ceil(2(r−d)k/(r−d+1))/k；固定改善必改近乎全部宏任务，而本族共同重选宏任务后直接可最优解。只限制上述固定/有限宏任务变动合同，不是一般近似困难性。再试必须共同选择宏任务及微任务卸载的共享真实容量。精确身份、独立冻结审查和双路实际枚举见optimal_hull_marginal_rounding_barrier.md§10。

双端精确Pareto可能指数不排除近似相关菜单；已有同机槽反例也可用单目的地路径修复。两项范围修正与未解义务见[专题失败及回收](research/unrelated_machines/FAILED_ROUTES.md)，不升级为主目标算法。

极小星保持整数T可行性不能自动推CONFIG保持；外部占用Q<1的两根两叶小例会失败。加入逐外机配置互斥可回收双向可行、条件边前向转换，但稀疏族收两端后仍无规则且全边独立CONFIG通过。见[正面条件与失效控制](research/current/unrelated_machines/minimal_star_contraction_and_capacity_gap.md#8-外部配置互斥下的配置点双向保持)；不排共同base或一般联合舍入。

固定宏任务后重开微任务的失败仍成立；新UM-SHARED-SINK-JOINT-MACRO-v1允许宏任务与整组撤离共同选择，并解决唯一home/单sink结构。其标量真实成本不自动涵盖多个sink预算；下一缺口是共同相关容量，见[单共享汇点的共同宏任务匹配](research/current/unrelated_machines/shared_sink_joint_macro_assignment.md)。

## 既定条件矩运输不能免费视为同层重置

尝试：从共同对称条件矩删一机器并吸收包，仅将该机的旧choices确定送到后备机器，再使用RYRᵀ。失效是命题错误：显式均匀真实最优分布在任何吸收负载<2T时都有新true列超载；旧矩来自真实最优分布，且在T≤包负载<2T的区间残余真实T调度存在。[正文§3–5](research/current/unrelated_machines/symmetric_moment_reset_and_single_machine_threshold.md)给精确反例。

回收：§2给任务聚合的逐列保留条件；§6证明同一个Rx在T包时可由真实匹配分解重建有效矩。因此反例仅否定既定矩的特定运输，不否定同层重新求解，更不是N(P) gap或主目标困难性。重试条件是可计算的重新耦合/改其他旧choices，并证明一般残余容量和输出复杂度。

需求树的[激活边际走廊失效](research/current/unrelated_machines/rooted_dag_congestion_flow.md)排除含父激活上界的LP直接给统一正常数根树比例；回收共同拥塞流的可构造接口，未知支撑选择未解。未导入调度困难性。

多个sink并非一概阻断共同选择：[占位基与大贡献分支](research/current/unrelated_machines/fixed_sink_occupation_rounding.md)在每固定K下可输出≤3T/2；不能把macro身份相关的完整匹配边菜单套用2K支撑引理，也不能取扩展空间basic点代替投影顶点。回收占位基交换与精确home DP；真正未解仍是K不受限、多home任务及一般统一ε。

同族的确定后备2T门槛不可外推到随机选择的新矩：新§9在m=2q时把精确包门槛降为q+2。它不改变旧RYRᵀ反例，因为随机任务选择需额外同任务对角修正；同样不能将限族矩输出误作实际调度算法。

[守恒扩区](research/current/unrelated_machines/rooted_dag_congestion_flow.md)能把支撑指数选择限制到非单位分叉；尚不能去掉一般h增长的2^h因子。单位路径标准流不是全类共同选择的证明。

一般多接收预算不能免费标量化；新增[完整profile接收池](research/current/unrelated_machines/shared_sink_joint_macro_assignment.md#9-有界-profile-畸变的完整接收池)通过完整资格、共同work上下包络及逐边尺寸获得可回收正面范围，未消除一般资格/跨home瓶颈。

[有限覆盖与反向困难性可靠性缺口](research/current/unrelated_machines/configuration_finite_cover_obstruction.md)已给标准机制的准确调度重构：即使高围长也存在整数OPT坍缩到配置阈值的cover；精选接线与一般困难性仍未排除，UM-TARGET-v1保持OPEN。

不完整资格并非一概排除正面构造：[共同资格私有组](research/current/unrelated_machines/hall_group_joint_flow.md)由真实最低出口量给整数Hall容量，可联合选择macro与receiver；缺少组下界、共同资格或等端体积时不能免费沿用。任意残余容量的组族也不必是拟阵；准确负控制与回收见正文§6。

全空间HS贪心不由真实最优矩自动获益：[三机真实分布反例](research/current/unrelated_machines/global_assignment_moment_rounding.md)在固定初始化、任务顺序和平局下输出2OPT。小缺陷提取仍成立；固定向量版另有[严格的线性坏例](research/current/unrelated_machines/truncated_multiplication_vector_greedy_barrier.md)，其他排序/更新合同须分别审查。一般小缺陷证书生成不能作为免费oracle，准确失败与回收见专题记录。

[高围长仙人掌的配置锐界与精确块算法](research/current/unrelated_machines/cactus_configuration_gap_and_block_exactness.md)表明simple cactus可同时有CONFIG supgap2和真实精确P；单环分量配置精确、最大顶点块环秩b给2^b poly算法。它们限制反面归约的结构，不证明一般目标不存在。

[反面路线的递归与资源重复边界](research/current/unrelated_machines/private_graft_and_resource_repetition.md)记录两个不同失效：私有重复的值是max/min而非乘积；完全元素池可能把分数完美匹配整数化，导致源NO变YES。只限制明确合同，不是一般算法或所有困难性归约的不可能性。

[固定阶压缩乘法向量贪心](research/current/unrelated_machines/truncated_multiplication_vector_greedy_barrier.md)每步丢弃最高次共同相关性。即使矩来自真实最优源，全部选择严格且任意顺序仍有(n−1)/(4r+2)坏例；一般nT上界给同量级。此失败仅限准确评分与固定算子规则，真正条件化/重建未排除。

[真实最优矩的固定压缩向量规则](research/current/unrelated_machines/projected_vector_greedy_unbounded.md)也可能遗忘过去联合支撑：三机全正时间上具体max-norm左乘规则近似比无界。回收事件净化与交换边界；不限制重新耦合、好分布选择、自适应调序或一般算法。

## 加权组出口替代固定组数预算

此前共同资格组的正负下界限制属于固定q槽Hall接口。新[加权出口联合槽](research/current/unrelated_machines/weighted_group_joint_slot_rounding.md)允许W_h∈[0,T]，不设正下界、接收机数不固定；尺寸d_h=(W_h−T/2)_+经共同LP和带home容量的槽流，实际出口≤d_h，得到home≤(3/2+δ)T、sink≤3T/2。旧q槽反例仍限制旧接口，不可外推为缺少组下界时所有联合算法失败。共同资格/等端时间/唯一home的分组仍承重，未给一般UM转换；主目标仍OPEN。


[低重数标签资源的确定性地板与锐界](research/current/unrelated_machines/bounded_collision_label_resource_floor.md)：所选资源重数Δ给真实b≥1/Δ，二重资源对任意束宽恰保留1/2；全局不同变量组度Δ_G给无需见证的实际(2−1/Δ_G)桥梁调度。只排除该四层有界碰撞接口的近二归约；高重数/跨层一致性与一般UM-TARGET-v1仍OPEN。

进一步的[大需求束碰撞界与平方池锐性](research/current/unrelated_machines/large_bundle_collision_square_root_floor.md)给含根上取整的Λ_c真实树，q=Δ=K=t²时精确maxΛ=b*=1/t；带η→0及ηKmin→∞条件的NO侧必要量为liminfη²Δ≥1。只约束资源束接口，源问题解码和一般困难性仍缺。

[全局四阶负载松弛的锐利二间隙](research/current/unrelated_machines/c2_unit_multislice_gap.md)（`UM-C2-LOAD-UNIT-GAP-v1`）已闭合裸C2-load本身的义务：m≥3,n=m+1单位同机上T_C2=n/m、OPT2，显式有理PSD证书给supgap2。这不同于固定贪心坏例；其三阶同机矩为负、CONFIG阈值2，故不含C2+CONFIG或一般算法困难性。一般主目标仍OPEN，下一可判别义务是含完整本地配置信息的共同矩/实际联合舍入。

## 弱单调小步的闭环失效及可回收临时超额

尝试以中性预修普遍补足旧严格lex长链搜索：闭环族把尾边正回流到已满root，任意局部后缀先增root，任何Cmax非增非平凡动作必须完整激活一个新环。全部最小成本槽初始化来自真实最优凸包，最小改件/参与机恰d+1，可随规模线性增长。失败属于该修复合同本身错误，不是主目标困难性。回收：单任务路径到OPT的最小峰值精确B+c，c=1/k²；只需微小暂时超额，且该cactus可精确解。重试应允许可控超额或原子长环，并证明一般共同守容及总进展。见[闭环正文](research/current/unrelated_machines/cyclic_batch_repair_and_fork_obstruction.md)§11。

异端时间也不是一概阻断共同选择：上下比例包络可把真实出口转成κ预算，用b_hz d_h成本排序及同一home容量流恢复所有sink。只有上包络时LP必要性仍失效；共同资格/唯一home仍承重。见[有界畸变正面合同](research/current/unrelated_machines/distorted_group_joint_slot_rounding.md)。

单任务复制端口的纯内部一致性接口已由[向下投影锐界](research/current/unrelated_machines/signed_one_job_port_downset.md)限制：移出任何入向端口只减少内部负载，两一致态遂强制混合态；精确计数逐参数可达到。失效步骤是把一般PCSP变量多次出现免费复制成两端真实任务。只否定保留外部出现槽、外部容量不参与投影的single-job接口；外部共同容量的两任务负控确能等值。可回收的是计数/零值处理/已有见证的实际混合构造；重试必须改变为多任务编码或共同外部一致性并证明完整调度低负载解码，不能只增内部辅助图。

[三host可用性复制的锐三半障碍](research/current/unrelated_machines/three_host_selector_sharp_three_halves.md)排除“只用a或同时用b,c保完整YES、两单输出坏侧都推近2”的独立空/满预载接口：非负行权二色闭包可实际拼接出某坏侧≤3T/2，任意加大内部图或多任务仍不能改变。失效步骤是把满载机器视为近似调度中完全不可停车；实际NO允许的剩余容量必须计入。同一机制给SC三特殊item复制的half锐界。回收二色闭包/实际拼接/逐台预载核验；重试必须改外部联合状态/解码合同，不从此排所有gadgets或一般算法。

[整束冲突偷换的具体失败](research/current/unrelated_machines/duplication_state_majority_floor.md)：残余label只需选择部分孩子，行/列全束交叠不能禁止二者同时出现在真实树。sK4可选5组各3格得5/8；旧所有K≥s的1/2锐性撤回，正确的多数下界和K≥2s锐例保留。重试需按每标签整数配额的真实Hall容量解码，不能用全束交叠图代替。

[增加独立预载扇出不能消除缺一逃逸](research/current/unrelated_machines/weighted_fanout_profile_boundary.md)：给only-a与all-B实际YES，则任意输出pair的两个缺一OPT和≤3T；内部图增大、多任务、任意源端时间均不能让每缺一状态接近二。只有one-output-free的星虽可2−1/q，也不满足这个NO合同。回收加权闭包与真实状态预算；重试须给跨模块共同容量或另一读出合同及完整源解码。

[仅严格端正确的双轨阈值编码无法自动保留近二NO](research/current/unrelated_machines/dual_rail_threshold_soundness_boundary.md)：C1确等价源严格解，但C>1可只外送真轨一部分ports。scalar整类及unit外部容量整类均有实际3/2；全cube源连弱端也NO却实际OPT趋1。否定范围仅明确归一化/单例外合同；可回收整数流、原P锐例和cube精确式。重试需不同的跨层一致性/相关选择以及对所有低负载实际σ的可靠解码。
