# 失败路线与准确否定范围

这是全仓入口。失败记录属于数学资产：须说明尝试机制、具体失败步骤、反例或缺口、排除范围、仍成立的回收结果及重试条件。

| 研究模型 | 当前最需避免的误用 | 详细记录 |
| --- | --- | --- |
| 加权拥塞 | 把潜在尾部参数或DAG端点检测限制误当实际博弈阈值；把奇环正局部证书的 ceiling 当全类存在上界；把固定人数或小资源支持游戏当增长下界；把尚待审的势障碍升级为普遍不可能 | [分支失败与回收](research/weighted_congestion_frontier/FAILED_ROUTES.md) |
| 两阶段设施选址 | 将有限终止当位多项式；将固定续局的失败当全部续局反例；把相关机器排程公式直接套到客户费用 | [准确失败目录](research/FAILED_ROUTES_FACILITY.md)及[多设施前沿](research/current/multi_facility/polytime_frontier.md) |
| 顺序客户吸引 | 将末位保证当所有早期玩家保证；将失效安全值/税桥误认为半覆盖反例；忽略真实离轨回复 | [原有逐项反例与回收](research/FAILED_ROUTES_FACILITY.md)、[模型地图](research/current/customer_attraction/README.md) |

旧对话、程序失败、断网、模型评价或有限搜索未找到反例没有数学真值含义。整理和发布不自动提升命题状态。
