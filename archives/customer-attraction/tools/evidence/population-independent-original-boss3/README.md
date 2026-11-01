# Boss3：人口父独立审计两原件

两primary共7960B，全文读取并核原字节：[source-manifest](source-manifest.json)、[原程序](original/population_independent_audit.py)、[原JSON](original/population_independent_audit.json)。本次只恢复父方两件；此前14缺件中的作者8件在邻证据目录，余4件不在本批。

[正式计算页](../../../state/计算/十三与四十客户的一至四人父审计恢复--计算.md)自足解释真实六客户类型/两重数、全部八有限case、计数全集的必要充分性、完整有序策略构造/验证、严格字段和输出边界。人数1…4，不含q族或当前六人half结论。

原入口只需Python标准库、无外部输入、不读其相邻JSON。它按位掩码重数求精确计数终局集合，再递归展开每个有序历史动作并验证全部强制四动作；不是把策略限制为计数函数。入口只向stdout打印报告，不写文件。

## 本轮一次真实原入口

clone外runtime执行未改源码一次，约0.079秒exit0，stderr空；[stdout](replay/stdout.txt)3493B逐字节等冻结JSON。[event](replay/event.json)保实际路径/argv/cwd、源和日志指纹、字节对应。runtime绝对路径仅记录本次历史，未来直接单文件复制到任何临时目录执行即可。

这一次入口内部八次audit累计224完整有序决策节点、896含自身比较（672非自身）。small最差福利序列8,13,12,13；strict为27,40,39,39。原`all_comparisons_strict`和`minimum_gap`只累计非自身；不能按字段名把自身0差也说成严格。

原JSON不保存完整动作表、逐节点收益/逐比较gap、全部有序路径或缓存表。当前没有为补这个输出范围另跑证书导出；保完整源码和实际执行，不把3.5KB摘要冒作完整证书文件。

## 对既有充分证据的只读对应

[compare_reports.py](compare_reports.py)只解析原报告、原代码AST常量、[作者旧报告](../population-exchange-family-boss3/original/population_exchange_audit.json)及[旧独立定义输出](../maximal-population-and-ordered-compression-primary/new-definition-audit/output.json)，不import/执行审计、不再计算效用/BI/LP。实际1次exit0：[event](comparison-event.json)、[stdout](comparison-stdout.txt)、[完整output](comparison-output.json)。四个m2/m3共享案例的全部计数、minW、OPT、选定根路径、节点/比较计数、严格性及最小差一致；两组bitmask重数也一致。不存在父原完整动作输出，因此不谎报逐历史策略相同。

新增四个m1/m4记录在对应output完整保留。原入口没有q参数/affine行；不复跑先前q族，也不把历史独立先验转授本轮。可复用只读对应命令：

`python compare_reports.py --repository-root /absolute/path/to/repository`

它会覆盖同目录comparison-output.json；应在独立副本运行并单列新事件。原件及实际日志仍保冻结身份。

关系语义在[relation-review](relation-review.json)，最终指纹/链接/receipt检查在[self-check](self-check.json)。本批两个receipt均integrated，不写共享索引或旧正文。没有网络/Git/claim/done动作，保存由父方串行。
