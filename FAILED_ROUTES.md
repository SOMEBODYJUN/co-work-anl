# 失败路线与准确否定范围

新主攻的[配置LP障碍、模型迁移和复杂度误用](research/unrelated_machines/FAILED_ROUTES.md)单独维护；新增长链反例精确限制仅共享单机边际的固定机器联合投影，未限制完整多机overlap相容性；逐星匹配另被共享小端容量击穿，保留安全过滤接口；五机反例另限制任意树再耦合态冻结任务后的低于2补全合同；这些方法边界与配置gap都不证明一般算法目标为假。下列旧题记录保持原范围。
此前拥塞题已有[线性次数的全状态严格反例](research/current/weighted_congestion/linear_degree_allstate_lower_bound.md)，准确否定普遍Cd/ln d保证。旧同类clock路线缺失的全前沿覆盖已由新专用健康输入另证；全局极差预算及通用strict-sweep反例仍有效。

共同大边匹配再补小流的精确选择也有明确[3DM接口障碍](research/current/unrelated_machines/joint_matching_completion_and_block_cuts.md)，新半单位身份排除所有固定δ<1/2的上述见证承诺构造（P≠NP）；主目标与其他调度接口仍未排除。

这是全仓入口。失败记录属于数学资产：须说明尝试机制、具体失败步骤、反例或缺口、排除范围、仍成立的回收结果及重试条件。

| 研究模型 | 当前最需避免的误用 | 详细记录 |
| --- | --- | --- |
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

[循环批量局部优化的分流缺口](research/current/unrelated_machines/cyclic_batch_repair_and_fork_obstruction.md)：总多项式终止不保证近似改善；逐坐标版本在真最优凸包槽族也零轮停滞。另一单目的地makespan非增fork边界仅限一般LST点，二者范围分开。

[固定真实最优边际的逐行偏差与负相关方法边界](research/current/unrelated_machines/optimal_hull_marginal_rounding_barrier.md)已有精确反例及尖锐值。该私有sink族直接可最优解；只排固定边际输出合同，重选点/正相关集中迁移和一般近似仍不受排除。

原任务固定数量拟阵完整外包与最小总工作量面保支撑均有新的[准确失效及回收](research/unrelated_machines/FAILED_ROUTES.md)；不能升级为一般调度困难性。

## 冻结宏任务后重开全部微任务仍不足

实际尝试：保留ST输出的宏任务，只把全部tiny重放到所有有限边，允许任意多源多目的地、真实负载和精确联合优化。共享Z族有OPT1及真实最优凸分解产生的实际槽输出，但宏任务分占r个home后，2r工作只能放r+1机器，故精确最优2r/(r+1)趋2。失败在宏任务的共同占位，不在tiny舍入精度、槽图或逐行不增。

回收：尖锐迁移前沿ceil(2(r−d)k/(r−d+1))/k；固定改善必改近乎全部宏任务，而本族共同重选宏任务后直接可最优解。只限制上述固定/有限宏任务变动合同，不是一般近似困难性。再试必须共同选择宏任务及微任务卸载的共享真实容量。精确身份、独立冻结审查和双路实际枚举见optimal_hull_marginal_rounding_barrier.md§10。

双端精确Pareto可能指数不排除近似相关菜单；已有同机槽反例也可用单目的地路径修复。两项范围修正与未解义务见[专题失败及回收](research/unrelated_machines/FAILED_ROUTES.md)，不升级为主目标算法。

极小星保持整数T可行性不能自动推CONFIG保持；外部占用Q<1的两根两叶小例会失败。加入逐外机配置互斥可回收双向可行、条件边前向转换，但稀疏族收两端后仍无规则且全边独立CONFIG通过。见[正面条件与失效控制](research/current/unrelated_machines/minimal_star_contraction_and_capacity_gap.md#8-外部配置互斥下的配置点双向保持)；不排共同base或一般联合舍入。

固定宏任务后重开微任务的失败仍成立；新UM-SHARED-SINK-JOINT-MACRO-v1允许宏任务与整组撤离共同选择，并解决唯一home/单sink结构。其标量真实成本不自动涵盖多个sink预算；下一缺口是共同相关容量，见[单共享汇点的共同宏任务匹配](research/current/unrelated_machines/shared_sink_joint_macro_assignment.md)。
