# 失败路线与准确否定范围

这是全仓入口。失败记录属于数学资产：须说明尝试机制、具体失败步骤、反例或缺口、排除范围、仍成立的回收结果及重试条件。

| 研究模型 | 当前最需避免的误用 | 详细记录 |
| --- | --- | --- |
| 加权拥塞 | 把潜在尾部参数或DAG端点检测限制误当实际博弈阈值；把奇环正局部证书的 ceiling 当全类存在上界；把固定人数或小资源支持游戏当增长下界；把尚待审的势障碍升级为普遍不可能 | [分支失败与回收](research/weighted_congestion_frontier/FAILED_ROUTES.md) |
| 两阶段设施选址 | 将有限终止当位多项式；将固定续局的失败当全部续局反例；把相关机器排程公式直接套到客户费用 | [准确失败目录](research/FAILED_ROUTES_FACILITY.md)及[多设施前沿](research/current/multi_facility/polytime_frontier.md) |
| 顺序客户吸引 | 将末位保证当所有早期玩家保证；将失效安全值/税桥误认为半覆盖反例；忽略真实离轨回复 | [原有逐项反例与回收](research/FAILED_ROUTES_FACILITY.md)、[模型地图](research/current/customer_attraction/README.md) |

旧对话、程序失败、断网、模型评价或有限搜索未找到反例没有数学真值含义。整理和发布不自动提升命题状态。

加权拥塞新增两项准确失败范围：[择证平稳/回返支撑的额外要求](research/current/weighted_congestion/template_certificates/stationary_selector_obstruction.md)与[唯一源私有侧分叉的UF放大](research/current/weighted_congestion/directed_fanout_forcing_cut.md)；详见主题失败记录，均不否定一般存在机制。

[统一低泄漏锚定时钟预算](research/current/weighted_congestion/uniform_clock_budget_barrier.md)现有普适障碍：任意输入和anchor均αlnq/q<1，不能靠改输入环完成全类否定；只限制该充分预算，实际时钟差及非均匀架构仍开放。

[不同步前沿反例](research/current/weighted_congestion/class_front_phase_quotient.md)阻止把严格原环自动推广到每个类前沿端点；内部离前沿改善仍可能存在。[局部矩表示](research/current/weighted_congestion/template_certificates/selector_local_moments.md)也不允许丢selector支撑的全局兼容性或把parity可行例当暂态必要。两项的准确范围与重试条件见主题失败记录。

[共享侧资源与真实clock的限制](research/weighted_congestion_frontier/FAILED_ROUTES.md)现区分：UF下同权共享side仍有目标量级PNE；保环总预算只是必要条件；firstopp失败不等于PNE；43次固定证书不代表最优次数或增长反例族。

[动态层秩的拼接缺口](research/weighted_congestion_frontier/FAILED_ROUTES.md)已区分固定共占height势与逐步换秩：换秩改变势，长实际链不代表无PNE，低单点height也非PNE必要；真正缺少累计图/SCC出口或瞬态dual。
