# 失败路线与准确否定范围

新主攻的[配置LP障碍、模型迁移和复杂度误用](research/unrelated_machines/FAILED_ROUTES.md)单独维护；新增长链反例精确限制仅共享单机边际的固定机器联合投影，未限制完整多机overlap相容性；逐星匹配另被共享小端容量击穿，保留安全过滤接口；五机反例另限制任意树再耦合态冻结任务后的低于2补全合同；这些方法边界与配置gap都不证明一般算法目标为假。下列旧题记录保持原范围。
此前拥塞题已有[线性次数的全状态严格反例](research/current/weighted_congestion/linear_degree_allstate_lower_bound.md)，准确否定普遍Cd/ln d保证。旧同类clock路线缺失的全前沿覆盖已由新专用健康输入另证；全局极差预算及通用strict-sweep反例仍有效。

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
