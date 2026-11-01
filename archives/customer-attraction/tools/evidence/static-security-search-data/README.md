# 五人七主题安全值取等点的证据

主源 `6c4ad31d75f489432f86` 的原1179B快照、完整127权及八字段不变；正文见[精确取等点](../../../state/计算/五人七主题静态安全值探针的精确取等点--计算.md)。准确结论是34单位客户、W29、OPT34、v5=29/5及全历史唯一纯策略sigma(h)=5；不是浮点比例略小于1所暗示的严格反例。

|文件|实际内容|
|---|---|
|[原random_best.json](original/random_best.json)|两个冻结提交相同的完整1179B输入，SHA19ad9937…b15913|
|[audit_point.py](audit_point.py)|标准库独立单位客户核验器；不导入原码，不调用BI或LP|
|[point-audit.json](point-audit.json)|全部八字段与127坐标、11正类型、纯鞍点、六条统一严格差界、唯一策略证明范围和OPT|
|[background-payoffs.json](background-payoffs.json)|210个四人计数背景，每行七个精确Fraction收益与全部差值；含重复背景|
|[terminal-coverages.json](terminal-coverages.json)|462个五人计数终局的真实覆盖，33个达到34；不称它们均为SPE|
|[R5e9 README](related/R5e9-README.md)|全文2588B相关原稿，只作比较，不另行完成此来源|
|[review-record.json](review-record.json)|来源身份、完整实读、相关比较及两类实际事件的清楚分工|
|[self-check.json](self-check.json)|最终结构、账本、源指纹、实际链接与回执目标检查|

独立程序已经执行一次：

```sh
python audit_point.py --source original/random_best.json --output-dir audit
```

实际执行在仓外 `round15-security-record/`，结果原样复制到本目录顶层；该命令是复用入口，不表示归档时再运行一次。新核共1470项精确背景收益及462项终局覆盖，0原导入/helper/main/RNG/BI/LP。完整2801有序历史的唯一性由正文严格差加逆归纳证明，未声称程序另外枚举了一棵2801行策略树。

程序方的[唯一原执行事件](../static-security-search-program/replay/execution.json)对保存点导入未改原码、初始化Probe一次并solve一次：1原BI+1安全LP，0随机main。原[返回对象](../static-security-search-program/replay/original-return.json)保旧四个数值字段同值、792单终局计数状态和实际数据类型范围；程序完整合同见[程序正文](../../../state/程序/静态安全值的有限搜索程序--程序.md)。这并不是原随机历史或未知总tries的重生。

旧v和ratio的十进制误差分别为+1/10^15和−1/10^16；精确鞍点给比例1。一般静态定义、已知逐人失败及聚合桥边界均在正文明确比较，不把本单例延伸为一般SPE桥或六人half。
