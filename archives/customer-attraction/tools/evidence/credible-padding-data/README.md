# 独立P主题填充的三份有限数据

正式[数据正文](../../../state/计算/独立主题填充完整策略的三个有限审计点--计算.md)完整解释k=1、5、10的16字段、八客户类型、实际路径及全部六query有理数。存在一份指定完整SPE，不能读作全部SPE相同或最差福利。一般k构造与阈值见[解析反族](../../../state/反例/独立主题饱和续局的全人数实际分数税反族--反例.md)。

- [k1原件](original/padding_k1.json)、[k5原件](original/padding_k5.json)、[k10原件](original/padding_k10.json)分别1418、1472、1524B，全部原字节保留；[来源清单](source-manifest.json)绑定12份已全文读取来源，只有三JSON是本包主源。
- [独立终局核](audit_terminal_data.py)、[实际事件](execution.json)及[完整结果](terminal-audit.json)是本数据包唯一新数学执行：146单位客户、185覆盖支持，核实际收益/负载、g/G/M/Δ、OPT和一份合法静态对手。0原helper、0BI、0全DAG IC、0LP。结果明确原DAG统计未由终局核重算。
- [程序方唯一k1原main](../credible-padding-program/replay/execution.json)、[外层事件](../credible-padding-program/replay/process-capture.json)、[重生表](../credible-padding-program/replay/report.json)是另一次明确分工的原实现运行。原表逐字同；[完整原DAG](../credible-padding-program/replay/original-dag.json.gz)、[原BI缓存](../credible-padding-program/replay/original-solver-cache.json)由[返回旁观包装](../credible-padding-program/replay_main.py)保存，没有第二份SPE求解实现。k5/k10未重跑。
- [原程序](../credible-padding-program/original/all_k_padding.py)、[数学原稿](../credible-padding-theory/original/all_k_padding.md)、[原README](../credible-saturation-research-entry/original/README.md)和实际四规范依赖均共享，避免重复副本。
- [复制失败原稿](../replicated-omissions-failure/original/replicated_omissions_failure.md)、[k17原表](../replicated-omissions-failure/original/replicated_k17_direct_audit.json)只作全读比较，不复跑54末行动；q≥2失败不能误否q1单池构造。
- [阅读比较记录](review-record.json)保旧36客户packet与本k10不同的决策节点/IC统计、一般padding条件和具体事件范围；[封包脚本](check_package.py)只核原件指纹、保存数组和捕获结构、收据及链接，结果为self-check.json。

可从仓根执行python3 -I -B archives/customer-attraction/tools/evidence/credible-padding-data/check_package.py，仅刷新静态self-check.json，不再执行数学审计。audit_terminal_data.py保留用于未来明确需要的复现，不因封包或浏览而自动运行。

minimum_slack含自身比较，0不证明非自身平局。M是固定actual分数背景query最大值，非真正安全值；k10正Δ仅反辅助税桥。三点half余额均正，合法静态对手使v≤5且W−mv≥1。所有运行身份、有限参数和全k解析量词都分别保存。
