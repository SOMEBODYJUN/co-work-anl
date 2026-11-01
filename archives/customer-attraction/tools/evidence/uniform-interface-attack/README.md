# 真实前缀均匀接口探针与两个取等保存点

正式对象：[随机策略锥探针与取等记录](../../../state/程序/真实前缀均匀接口的随机策略锥探针与取等记录--程序.md)。

三主源： [uniform_interface_attack.py](original/uniform_interface_attack.py) 2960 B；[uniform_5_3.json](original/uniform_5_3.json) 3494 B；[uniform_6_4.json](original/uniform_6_4.json) 28075 B。完整读取全部代码、94个重数字符串、31与259条历史动作和全部输出字段。第一数是主题数，第二数是玩家数。

- [source-manifest.json](source-manifest.json)：三主源冻结身份、六个共享代码依赖、两份相关原文和正式比较。
- [scope-manifest.json](scope-manifest.json)：真实搜索语义、历史缺字段、两点的新旧证据分层。
- [audit_stored_points.py](audit_stored_points.py)：唯一新增定义核原源码，未导入原程序或依赖。
- [exact-audit/report.json](exact-audit/report.json)：两点精确利润、W/OPT、实际偏离矩阵、目标分别为2和3。
- [exact-audit/case-ledger.json](exact-audit/case-ledger.json)：全部290个历史及1709项含自身行动比较。
- [exact-audit/execution.json](exact-audit/execution.json)：0.00854536700353492秒内部计时、输入前后SHA及报告指纹。
- [check_static.py](check_static.py)、[self-check.json](self-check.json)：指纹/解析/链接/回执检查，不重复数学。

原main0、原helper0、随机搜索0、LP0、规范SPE求解0。新定义核仅两个已存单客户点的一次精确完整历史检查；OPT=1由单客户解析上界与可达性证明，没有穷举全部终局。该事件不是历史100/45轮的重放。

两点在保留同覆盖异标签的原标签模型均达到接口等号且W=OPT=1。[严格共同目录定义](../../../state/定义/共同目录完整历史模型--定义.md)采用集合目录，同覆盖集合只有一个元素；本包未另证明指定全历史策略的商下降或不同标签比较域的迁移，不能默认合并别名就获得严格目录原输入。通用推导也适用于覆盖映射单射的严格子域。历史程序只遍历不同标签组合，未覆盖重复比较；未去重策略锥；有理recover_vertex后本入口未再次verify/W1，候选标记仍由浮点值触发，且无精确dual。故不得将历史阴性或保存点等号升级为所有锥的上界、一般接口或half。

共享原件直接引用既有包： [credible_cone](../uniform-portfolio-search-primary/original/tests/audits/cone_attack_credible_variants.py)、[StrategyCone](../uniform-portfolio-search-primary/original/tests/audits/customer_attraction_strategy_lp.py)、[规范核心来源](../deletion-security-probe-program/source-manifest.json)。这两直接依赖已全文读并与本次clean show逐字匹配；四核心文件此前已全文理解且本次重新绑定SHA，不重导入/复跑。其它padding/security源只比较相关入口，不认领或完成。

新定义核源码使用实际scratch路径并拒绝复用已有输出目录，正式保存不改写事件成另一次执行。静态自查永不调用该脚本或原main。

本次模型边界补注只更新正文/元数据和静态绑定；三原件、原动作及唯一数学事件均不改字节、不重核。
