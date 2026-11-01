<!-- 可追加到既有“R5662研究checkpoint的版本清单与有限复核--资源.md”；不是新数学对象。 -->

## 冻结入口版本与既有有限输出的进一步对应

174条manifest和本次冻结inventory的完整(path,SHA256,size)比较仍为172条同版、2条另版、0条缺路径。两个入口的完整差异如下；它们是版本身份差异，不表示入口内容数学错误：

|入口|manifest所报snapshot版本|本次冻结同路径版本|
|---|---|---|
|FRONTIER.md|8086B；SHA256 `228ae0b1edbf4b9f8f2c01aa4884ecb46d7ef1b6305bc1ea97f5a5b911f077ed`|source ID `bbe87642e2efce14d63c`；9820B；SHA256 `6e89b1a05e7def262dae3612a6b5bfee17763a114acb2a7f52d22f48a08f53c7`|
|README.md|3221B；SHA256 `d57fc596b071189c7e99c2acde812beafa303f5004b1d975753297c3d4279a37`|source ID `2febc458086d3c08984e`；3913B；SHA256 `e8b0dbe0aa9f95a5836777cf55eacf9edb37fe35a840960c534d9bf57c71e30b`|

现有[普通点有限审计输出](../../tools/evidence/potential-menu-joint/replay/audit_normal.json)为2184B，SHA256 `cf0adfcdd698eb91cadeab684da3734c49b884889cf9af7928e2080955201946`，与manifest所列`research_6/audit_potential_menu_joint.json`同版。它与本页父方potential replay恰有13个共享顶层字段，全部精确相同：scope、scale、unit_customer_count、customer_types、potential_multisets、maximum_potential、budget_W_plus_C、argmax、actual_payoffs、三类minimum_slack以及完整penultimate_all_alternatives_support_slack。普通audit另外保有势超额0及私有谱失败数据；父方replay另有执行代码SHA、int64上界与review_scope。两份报告的字段差异不抹去各自来源。

现保存的5937B[审计代码](../../tools/evidence/potential-menu-joint/replay/audit_potential_menu_joint.py)与manifest同为SHA256 `245483e74f526dccfb0e0bcf5346afb0fdabd2d91a09fa7592bea3dd83becdf3`；它不是父方replay所报`ff1536b0667244ca05a49ab1ea76a291dba50784524921e0dd5028c4b9364ec5`的逐字节版本。共享数值相同只说明保存输出吻合，不能取代该历史执行版本的代码追溯。

这些报告的小量算式也相容：C(23,6)=100947，十八分量argmax和为6，六实际收益之和W=1，最大势减W+C为0；十八倒二support slack恰5正、6零、7负。潜势整数上界8338358321338500恰为单位客户数56723525995500乘60H6=147，低于有符号int64上界。这是转写与标量相容性复核，没有重新运行历史入口、遍历全部势多重集、重构矩阵或给完整SPE认证。
