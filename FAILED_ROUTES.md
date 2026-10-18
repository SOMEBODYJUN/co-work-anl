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

[全局四阶负载松弛的锐利二间隙](research/current/unrelated_machines/c2_unit_multislice_gap.md)（`UM-C2-LOAD-UNIT-GAP-v1`）已闭合裸C2-load本身的义务：m≥3,n=m+1单位同机上T_C2=n/m、OPT2，显式有理PSD证书给supgap2。这不同于固定贪心坏例；其三阶同机矩为负、CONFIG阈值2，故不含C2+CONFIG或一般算法困难性。该裸C2命题的范围不变；后续[弱H2合取的新二间隙](research/current/unrelated_machines/weak_h2_configuration_moment_gap.md)另行关闭只共享一阶CONFIG的合同。共享行二阶在该新族上阈值精确，一般强合同与UM-TARGET-v1仍OPEN。

## 弱单调小步的闭环失效及可回收临时超额

尝试以中性预修普遍补足旧严格lex长链搜索：闭环族把尾边正回流到已满root，任意局部后缀先增root，任何Cmax非增非平凡动作必须完整激活一个新环。全部最小成本槽初始化来自真实最优凸包，最小改件/参与机恰d+1，可随规模线性增长。失败属于该修复合同本身错误，不是主目标困难性。回收：单任务路径到OPT的最小峰值精确B+c，c=1/k²；只需微小暂时超额，且该cactus可精确解。重试应允许可控超额或原子长环，并证明一般共同守容及总进展。见[闭环正文](research/current/unrelated_machines/cyclic_batch_repair_and_fork_obstruction.md)§11。

异端时间也不是一概阻断共同选择：上下比例包络可把真实出口转成κ预算，用b_hz d_h成本排序及同一home容量流恢复所有sink。只有上包络时LP必要性仍失效；共同资格/唯一home仍承重。见[有界畸变正面合同](research/current/unrelated_machines/distorted_group_joint_slot_rounding.md)。

单任务复制端口的纯内部一致性接口已由[向下投影锐界](research/current/unrelated_machines/signed_one_job_port_downset.md)限制：移出任何入向端口只减少内部负载，两一致态遂强制混合态；精确计数逐参数可达到。失效步骤是把一般PCSP变量多次出现免费复制成两端真实任务。只否定保留外部出现槽、外部容量不参与投影的single-job接口；外部共同容量的两任务负控确能等值。可回收的是计数/零值处理/已有见证的实际混合构造；重试必须改变为多任务编码或共同外部一致性并证明完整调度低负载解码，不能只增内部辅助图。

[三host可用性复制的锐三半障碍](research/current/unrelated_machines/three_host_selector_sharp_three_halves.md)排除“只用a或同时用b,c保完整YES、两单输出坏侧都推近2”的独立空/满预载接口：非负行权二色闭包可实际拼接出某坏侧≤3T/2，任意加大内部图或多任务仍不能改变。失效步骤是把满载机器视为近似调度中完全不可停车；实际NO允许的剩余容量必须计入。同一机制给SC三特殊item复制的half锐界。回收二色闭包/实际拼接/逐台预载核验；重试必须改外部联合状态/解码合同，不从此排所有gadgets或一般算法。

[整束冲突偷换的具体失败](research/current/unrelated_machines/duplication_state_majority_floor.md)：残余label只需选择部分孩子，行/列全束交叠不能禁止二者同时出现在真实树。sK4可选5组各3格得5/8；旧所有K≥s的1/2锐性撤回，正确的多数下界和K≥2s锐例保留。重试需按每标签整数配额的真实Hall容量解码，不能用全束交叠图代替。

[增加独立预载扇出不能消除缺一逃逸](research/current/unrelated_machines/weighted_fanout_profile_boundary.md)：给only-a与all-B实际YES，则任意输出pair的两个缺一OPT和≤3T；内部图增大、多任务、任意源端时间均不能让每缺一状态接近二。只有one-output-free的星虽可2−1/q，也不满足这个NO合同。回收加权闭包与真实状态预算；重试须给跨模块共同容量或另一读出合同及完整源解码。

[仅严格端正确的双轨阈值编码无法自动保留近二NO](research/current/unrelated_machines/dual_rail_threshold_soundness_boundary.md)：C1确等价源严格解，但C>1可只外送真轨一部分ports。scalar整类及unit外部容量整类均有实际3/2；全cube源连弱端也NO却实际OPT趋1。否定范围仅明确归一化/单例外合同；可回收整数流、原P锐例和cube精确式。重试需不同的跨层一致性/相关选择以及对所有低负载实际σ的可靠解码。

[加深私有树或重排半密度unit读出仍不能放大到近二](research/current/unrelated_machines/unit_readout_pruned_forest_boundary.md)：唯一unit incoming+k枚总small负载1让半质量槽匹配给全高度三半，涵盖所有arity≤2A wiring。改d>2A若仍全正负degree平衡，非空源严格YES已空；补dummy须防纯dummy配额子树并核共同外部容量。失败范围不超出明确成本/私有结构/密度；可回收一般forest IFF、树命中门槛及同64open真OPT1对7/4，后续需真实非此域联合soundness。

[仅把clause密度提高到另一个固定D仍不足作任意近二归约](research/current/unrelated_machines/unit_readout_calibrated_cardinality_slots.md)：校准计数槽给每固定D统一2−1/(4D)结构类算法，即使k,h增长。D可以随目标ε改变，未被一般排除；仍需实际YES和所有pruned森林NO解码。强基数LP一般只充分，不能用不可行偷判NO；弱激活LP又不支持舍入。回收精确见证/两反例/有界密度算法；重试须真正避开共同基数证书。

## 逐机器价格与局部 anchor 不能免费交换全局选择

尝试对每个非负机器价格优化big匹配，再用残余light流，希望由所有价格各自通过推出同一个匹配。失效在凸化：这些测试精确等价任务守恒+big分数基数+LST容量，仍包含经典CONFIG趋二族；不是价格oracle不可算。原两机数值例还遗漏δ>3/20分类范围，且OPT>T，只能说明量词交换。漏掉p≤T剪枝时甚至固定m损失m。回收显式最小费用流oracle、精确min–max身份及最优价格共同big面的可检验成功证书；普通扰动价唯一不足，面失败不能作OPT>T证据。逐机anchor凸化也含CONFIG，a_i>0不能给统一ε。重试须新的跨机器状态/实际联合舍入损失，不是更多价格或专族样本。详见[自足正文](research/current/unrelated_machines/heavy_light_price_convexification.md)；此为已知工具的接口综合，非一般不可能性。

## 不能从固定残余次模免费推出共同角色选择

尝试用残余throughput的次模性选择大任务占位。正确部分是任意异端p的固定R容量格次模；失效步骤有两处：占位损失D本为超模，且H同时移除任务与扣容量后V根本不继承次模（2×2原OPT1/2、四值2/1/1/2）。即使宏身份固定、tiny同尺寸，任意固定严格次二α的可行占位族仍能精确为任意图独立集，D=诱导边数，故不是免费拟阵或固定p交换系统。回收一般F性质、primal/dual求值证书与精确图表示；原实例都有显式OPT1，不是调度困难性。重试需同时保留R(H)、h(H)的共同恢复与实际联合舍入余量，不能以近似总通过量代替全任务完成。见[完整范围](research/current/unrelated_machines/residual_throughput_and_occupation_projection.md)。

[完整单位树的叶流与选择重组](research/current/unrelated_machines/unit_readout_global_leaf_flow_and_selector_mixing.md)：任意clause密度下固定h有实际(1+2^(−1/h))近似；给p份同一P完整C1见证时，N≥p的任意covered selector坐标重组有锐2−1/(2p−1)实际负载。h、p增长及NO无完整YES均承重，一般主目标及其反面OPEN，外审与新颖性未认证。

## 同一一阶CONFIG合取与槽损失凸化的失败机制

尝试：把C2-load共同四阶矩与完整CONFIG共享同一一阶点，或将完整实际槽损失逐机凸化，期望统一跨过相对T的二倍壁垒。失效：稀释星族中，条件激活块的单位multislice伪矩容纳b+k任务于b+1资源，但激活仅1/k，使同一一阶资源占用恰1，CONFIG1完全看不到该条件超额；实际整数OPT仍2−1/k。参数化PSD/所有localizer和同x配置均已证明，不是有限搜索反例。

回收：一般N≥m+1的degree2 multislice PSD及可显式生成的条件张量/混合；共享同机二阶后，零pair的PSD传播给任意端条件单槽容量，从而**整个同族强阈值**精确等于OPT。失败只排弱H2，不排强二阶/三阶非负/其他算法，亦非一般困难性。准确Claim、证明及审查沿[同一正文](research/current/unrelated_machines/weak_h2_configuration_moment_gap.md)读取。

另[完整槽包络](research/current/unrelated_machines/slot_envelope_and_configuration_identity.md)精确区分两个常混淆动作：固定容量后凸化子水平集恰CONFIG；先凸化上图则只剩线性负载。非凸min max包络本身等于OPT，因此没有免费共同选择。重试必须新增跨机相关机制或给可计算近似非凸进展；只精确计费单行损失或重新调价不够。

## 固定势与局部repair的新增失败机制

固定总工作量并不能保证局部势下降有效：`research/current/unrelated_machines/fixed_work_convex_local_minimum_near_two.md` 的同机族使二次势、排序势和固定批量单调路线均停在趋二状态。失败原因是必要迁移批量随机器数线性增长，而不是总工作量变化；未来若允许全局或无界批量，需另给可计算势下降及位复杂度证明。

严格unit双树源编译的新增失败范围见[专题记录](research/unrelated_machines/FAILED_ROUTES.md)：CONFIG1整轨LP可求且可五三实际输出，但近unit阈值1+1/k仍保经典趋二gap；不得把两阈值混用。

[固定批量且仅给小幅临时增载](research/current/unrelated_machines/pruned_first_move_and_transient_peak.md)也可能无法启动：m=k+1的真实OPT=T环族，任意非空≤k件首批负载至少max(2T,C+T/2)。此上界同时是一般剪枝首步的锐界；不能因首步存在就宣称全程或改善。初态不声明ST来源，强初始化和无界共同批次未排除。

## 逐行均匀平层读出不能仅靠跨测试相关压低支付

尝试用同一源标签控制许多测试来挽回独立局部guard的soundness。对simple、逐复合行均匀、每right资源数等于其degree的准确合同，整数碰撞势加一次全局匹配总能保每点ceil-half，flat原sigma≤3/2。因此共享标签本身不够。可回收的是实际共同标签/资源算法；重试需非均匀行、有效多重请求、跨资源组耦合或多层祖先约束，并重证全部机器与源解码。删除假设的反例仅否定绝对负载延伸，不否定更大类另一三二近似。见[正文](research/current/unrelated_machines/row_uniform_correlated_guard_rounding.md)。

[坐标切片源编译](research/current/unrelated_machines/coordinate_slice_source_compilation_counterexample.md)可逐对手坐标只删一个值而保D−1叉；源partial-MinRep NO甚至双射/CONFIG1不补weak decoder。保留精确阈值与padding工具，重试需真实跨test/不同共享结构。

## 强配置相容不等于真实共同二阶law

尝试用本行CONFIG全部同阶矩+全局固定阶PSD直接抽取保给定二阶的重匹配分布。失败是接口本身错误：[奇数切片K22编译](research/current/unrelated_machines/strong_configuration_matching_moment_obstruction.md)的所有短事件非负、全部负载恒1，却使整数选块数形式方差为0而均值半整数。回收自足harmonic PSD、精确位长和锐修复半径1/[4N(N−1)]；该半径趋零，所有实例显然OPT1。只排精确保矩接口，重试应允许定量改矩/直接共同实际选择；不据此否定强松弛的实际舍入。

[永久缓冲激活与共同解锁路径](research/current/unrelated_machines/permanent_buffer_activation_and_priority_deadlocks.md)给锐分数窗口[1/3,1/2]和静态/优先级反例；[保留坏环与实际最大件全程锐界](research/current/unrelated_machines/held_cycle_release_and_assigned_max_path.md)用共同保护来流及源补集证明：每个正阈值源有一件eligible时，给定目标的完整路径可构造；并覆盖标准有序槽实际输出。局部promise类峰U逐参数锐，不冒充实际ST输出锐性。具体τ仍是承重输入，未知目标、任意剪枝初态与一般统一次二输出仍OPEN。

UM-TARGET-v1限定新资产（2026-10-18）：[一般双见证查询分离与锐3/2费用合同](research/current/unrelated_machines/two_witness_query_separation.md)、[单home完整查询模式](research/current/unrelated_machines/single_home_cascade_query_separation.md)、[超立方菜单的Hall与锐3/2](research/current/unrelated_machines/coordinate_slice_source_compilation_counterexample.md)。均已实际独立内审；是给定见证/结构类的边界，不构成主命题正反面证明。精确身份、输入域、实现和未覆盖义务以本题账本为准。


[QUERY-COUNT-FEE-v3](research/current/unrelated_machines/two_witness_query_separation.md)进一步排除单件tiny聚合读取的固定费逃逸：正T两strict模式、β≥3/2，W≤κF迫至少d−2floorκ枚query旧端>(β−1)T。条件性改派费必要界，不是UM困难性；零质量原异议已修复。


[严格重中端占位gap胶合](research/current/unrelated_machines/unit_presence_two_witness_sharp_gluing.md)允许cross-role且两strict见证下给2−gap/2的完整mixed，但不锁job身份。共同尺寸精确重开已修复冻结baseline guard与孤立机遗漏；仅tiny审计，主目标仍OPEN。


[保护环共享子句OR错配](research/current/unrelated_machines/near_unit_implication_pcsp_and_physical_copy_obligation.md)记录一个完整物理接线失败：同一共同匹配让所有SAT/UNSAT公式都strict≤1。只排该接法，重试必须防实际身份交换；主目标未升级。


[有界菜单两组资源联合近似](research/current/unrelated_machines/degree_two_group_bounded_menu_joint_rounding.md)给特定weighted menu类相对OPT的2−1/(2K)；结合旧VW MaxMin算法的直接结构推论，非generalUM。Q2、固定K的加权重试仍不能承载近2严格unit源；重试需真实突破跨组degree/菜单或原矩阵结构，主目标未解。 [有限组交互](research/current/unrelated_machines/weighted_menu_bounded_group_interaction_rounding.md)另给任意K、固定M/Δ的实际改善；[三坐标与三态正规形](research/current/unrelated_machines/degree_three_weighted_menu_cube_embedding.md)精确保OPT/V把任意normalized flat源降K3/资源度3再入zero cube，标准path已核BCG归属。[SC值桥/菜单数锐界](research/current/unrelated_machines/normalized_weighted_menu_santa_value_and_size.md)只排同U逐玩家shortcut。原source无须先限K/Δ，剩余承重仍是norm1与全partial导出的tiny-gap NO decoder，主目标未解。

[笛卡尔菜单的反向放大与一致性差距](research/current/unrelated_machines/cartesian_menu_recoupling_and_coordinate_consistency.md)：一个明确裸product实际OPT=1+2^-t趋1；额外逐坐标语义的配额却为floor((3/2)^t)/2^t趋0。两精确值排同族常数保值事后修复，尚缺真实负载实现的一致性；只否定该放大合同，非一般困难性。

[分块一致性、线性秩与全域缺项标尺](research/current/unrelated_machines/cartesian_menu_block_coherence_rank_and_deficit.md)回收已完成的精确结构：bounded blocks才指数衰减，无环单输入链仍保1/2；q元affine重选与coordinate一致相反极限；并发投影给任意nonlinear缺项必要条件。均未实现物理coherence；主反向承重继续是低负载全局decoder，停止以更多局部tensor数值代替该义务。

[逐机统一内部索引交换](research/current/unrelated_machines/machine_uniform_query_return_index_exchange.md)、[direct共居严格SAT及三半锐逃逸](research/current/unrelated_machines/direct_cohabiting_query_return_strict_sat_and_sharp_escape.md)与[真实直线源/累计路径编译障碍](research/current/unrelated_machines/line_set_packing_and_take_continue_compilation_obstructions.md)关闭各自精确接口；全部原jobs和全机负载已核，未关闭近二源NO的全局decoder。标准matching/Hall扣除新颖性，E曾误标签的proof-aware审查已另冻纠正，并由真正statement-first重构补齐。只有明确改变外部共同容量/partial AND机制时才重试这些具体桥。

[任意异权私有子句的三半上界与共享外端边界](research/current/unrelated_machines/general_weighted_private_clause_exchange_and_shared_outside_boundary.md)：固定辅助内部single-query/single-return接口的3T/2交换可与真实变量环共同匹配，所有局部索引strict可选时整公式实际≤1.5T；不是私有outside免费替ring。标准四任务环与小query返回池允许共享外部身份，但孤立OPT1且未保变量一致性。重试须改变精确模板的共同容量/边界，不能仅在私有Hc增加异权aux；主源NO联合decoder仍未闭合。

[仿射线逐tuple加globaldummy的完整编译](research/current/unrelated_machines/affine_line_tuple_groups_global_dummy_compilation_escape.md)另行关闭一种此前未分析的自然桥：n个tuple groups配n−q个共享dummy、q≤非空relations数，strict unit iff原full-set packing≥q，但无需源解仍actual≤1.5。选择q个不同relations恢复Hall不变量，所有未选state任务保留；不把这个新精确范围倒改成旧D已排，也不外推其它全局守卫/权重/阈值。

[完整归一化菜单的配置证书保持](research/current/unrelated_machines/normalized_menu_configuration_certificate_preservation.md)补足normalform的分数合同：flat machine CONFIG(1) iff positive-support FSLP iff state-dummy SC CONFIG(1)，zero原jobs仍全覆盖；再接SC路径得到rowtotal≤3/item正度≤3而CONFIG1/actual1/D。只排此LP充分性，未排actualOPT≥1的promise常数算法；标准路径/旧gap非新源，主目标OPEN。

[并行sum关系任意状态重赋权的半保留](research/current/unrelated_machines/weighted_affine_parallel_relation_reweighting_obstruction.md)补上不同范围：source value1/R的完整并行sum关系，即使任意state-dependent非负norm1权，仍可实际半保留/全部job≤1.5。条件于整个state保持c均匀，再把共点交唯一例外；singleton关系能V0，故不推广任意关系，不排避开本族的hard image。

[异权内部与重读口的bulk OR实际三半逃逸](research/current/unrelated_machines/bulk_or_commit_two_witness_interpolation.md)给完整block-ring双池下任意异权I/正C时间(.5,1]的committer：两个不同一真全原strict见证经半项配对/共同流，仍有全False全部原job实际≤1.5。内部异权collector与重C都不能单独挡split；缺两全局strict见证的跨子句NO不在范围，不是near2源。

[单标签边际均匀LINE的趋二实际间隙](research/current/unrelated_machines/tagged_affine_line_uniform_marginal_gap.md)给真LINE反例：每incidence label均匀、各state norm1，但V=1/(R−1)/实际OPT=2−1/(R−1)；共同arityR与R-partite可zero padding保值。此非pairwise-independent原hard image，未给源value/CONFIG新结论/计算困难性。

[宽矩形LINE的重细资源共同避冲突](research/current/unrelated_machines/tagged_affine_line_wide_rectangle_joint_escape.md)给出明确额外状态自由度：L>b(D−1)逐组避开旧marks，再以同一B保marks/独占点、每组损失≤Mβ；sparse正点给actual1，L>2q(D−1)²任意权给actual≤1.5。所有固定截距/原jobs保留，不把PI或alphabet可增当rectangle前提。

[两完整actual插值与实际used池端义务](research/current/unrelated_machines/bulk_or_commit_two_witness_interpolation.md)新增同页§6–10 v4：任意P的两actual与指定F原端改派，剩余job双出现配对得逐机件数与负载同τ；bulk J可接全部非pool仍全False≤1.5，任意pool得≤1.5+d/2，真正排near2须已用近unit J_pool身份改变。旧v3前缀/强输出范围保留；未知两witness不免费，不是sourceNO。

[仿射线两两独立的结构边界](research/current/unrelated_machines/tagged_affine_line_pairwise_independence_boundary.md)：单primary/onehot helpers在指定pairwise边际下可按条件化Hall全部actual1；多primary公共4D simplex陪集族则所有local pairs uniform仍V=2/(R+1)/实际OPT=2−2/(R+1)，common q/partite/全部zero jobs保留。后者只删唯一main即unit，不是robust或hard image/主反面。
