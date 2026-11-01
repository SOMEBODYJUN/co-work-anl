# 显式回复真尾利润切面数据

主源56dfbdec811d0c84b8fe的[1671B原表](original/tail_reply_cuts.json)和唯一绑定的[815400B源点](original/early_reply_floors_exact.json)保持原字节，SHA、完整记录、真IC证明及有限范围见[正式正文](../../../state/计算/显式回复真尾利润投影的有理切面--计算.md)。源点仅作本表完整实际输入保存，不在本回执另办理其来源完成。

- [audit_four_cuts.py](audit_four_cuts.py)不import原码或求解LP，以字面六索引边构造下包络和强PAIR平均行。
- [four-cut-audit.json](four-cut-audit.json)保存全部六字段、源点元数据/16hist/194组四态、四个1905系数向量、状态质量和逐hist贡献，以及floor/mixed同布局不同权比较。
- [review-record.json](review-record.json)记录完整读取、共享原函数运行身份、独立核范围和源版本。
- [self-check.json](self-check.json)记录最终JSON/AST/链接/回执和原字节核对。

同批程序证据中的[唯一原函数结果](../tail-reply-query-program/function-replay/original-function-rows.json)与[调用记录](../tail-reply-query-program/function-replay/function-execution.json)共享复用，不重复执行。该记录使用未改源码及只读sys.setprofile观察，只调用四条保存行的原states/coefficient_rows/psi；main、discover及LP都是0。本数据侧独立核先通过，补全状态逐项对照后再通过；两次均不调用原函数。

四条均为r=1、Z成员、alpha=gamma=1，向量恰是已有强PAIR的边类平均；7620系数及256局部身份全等。当前源点四负，既有mixed点四零；后者没有因此获得early全部5287行的可行性或SPE认证。K及1306个旧RR交叠不进入这些切面，不能只改交叠来修复当前负值。

在仓库根只重做独立核：

    python archives/customer-attraction/tools/evidence/tail-reply-query-cuts-data/audit_four_cuts.py --cuts archives/customer-attraction/tools/evidence/tail-reply-query-cuts-data/original/tail_reply_cuts.json --point archives/customer-attraction/tools/evidence/tail-reply-query-cuts-data/original/early_reply_floors_exact.json --author-functions archives/customer-attraction/tools/evidence/tail-reply-query-program/function-replay/original-function-rows.json --repo . --output /tmp/tail-four-cut-audit.json

这个命令只读原函数已保存输出；不会触发216结构LP发现或重建5287行。通用发现器及其参数合同由[程序正文](../../../state/程序/显式回复的真尾利润投影切面程序--程序.md)单独承担。
