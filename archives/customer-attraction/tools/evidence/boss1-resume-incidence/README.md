# 关联动态预算独立算术审查证据

本批四个指定primary合计23694字节，均经`work.py clean show ID`全文读取/导出，随后逐一核原inventory的字节数、SHA256和Git blob。原件位于original/，未改内容；来源定位和比较材料实际阅读范围见[source-manifest.json](source-manifest.json)。两个冻结来源位置同字节，不计成两次独立审查。

- [审查正文](../../../state/审查/关联动态预算的独立算术审查与停止边界--审查.md)：原异议的数学对象、修正一般LP、全历史证明、范围包含和历史停线边界。
- [程序正文](../../../state/程序/关联动态预算算术审计的输入与精确输出--程序.md)：固定输入、全部输出、精确与数值层级。
- [原审查](original/incidence_scope.md)及[历史消息回执](original/incidence_receipt.json)。
- [原算术代码](original/incidence_numeric_check.py)、[原输出](original/incidence_numeric_check.json)、[本次一次回放](replay.json)及[核验记录](verification.json)。

本次实际运行只有一次原算术main：

```sh
python3 archives/customer-attraction/tools/evidence/boss1-resume-incidence/original/incidence_numeric_check.py > archives/customer-attraction/tools/evidence/boss1-resume-incidence/replay.json
```

随后以`json.loads`比较原输出与stdout，整个嵌套结构相等。Fraction部分是固定有理运算；60位Decimal对数与二分仅为数值诊断。一般产品支配、修正LP全历史归纳、严格log3有理下证由数学正文承担。没有运行博弈求解器、成熟动态/分数覆盖/六人9/2审计核或新策略搜索。消息回执只是历史记录，不授权或代表当前发送消息。
