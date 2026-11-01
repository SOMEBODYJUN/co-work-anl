# 完整策略抽样全终局税：首样本证据

主源 `e5e7b1ed15215d571c72` 为1737B `worst_tax.py`。自足模型、目标、抽样合同及验收缺口见[程序正文](../../../state/程序/完整策略抽样的全终局税探针--程序.md)。这里保的是新运行的一个完整样本，不是原设计80轮全部扫描。

|文件|实际身份|
|---|---|
|[原worst_tax.py](original/worst_tax.py)|1737B冻结采样器，无main guard，导入也启动循环|
|[原tax_probe.py](related/tax_probe.py)|1887B冻结helper；本源exec其main前定义、顶层seed及默认sigma|
|[规范依赖目录](dependencies/customer_attraction/)|四份冻结model/exact/certificate/package入口，不改字节|
|[run_first_sample.py](run_first_sample.py)|root所写记录器：runpy运行未改源码，只读profile观察；第二轮首次Python调用前主动抛计划停止异常|
|[执行事件](first-sample/execution.json)|1样本/15LP，7.980107452秒、原normal_return=false、80轮未完成、六源前后SHA同、无候选文件|
|[原始捕获](first-sample/capture.json)|18客户种子、259个有序动作、15个LP完整状态、63维浮点权、根与选择结果|
|[原Gamma压缩表](first-sample/original-gamma.json.gz)|1554×63原Fraction行；含259自身零行，不去重|
|[stdout](first-sample/stdout.txt)、[stderr](first-sample/stderr.txt)|原脚本首轮打印与空stderr；打印−f为负，不是f负|
|[audit_first_sample.py](audit_first_sample.py)|root所写独立单位客户核：不导原helper/规范solver/LP，两个新点各259历史/1554行动|
|[单位客户审计](first-sample/unit-client-audit.json)|全部3108条实际/偏离/差值账，种子18客户及事后7客户点；0新LP|
|[manifest.json](manifest.json)|六份来源、所有既有不可变资产指纹、完整阅读比较与运行责任|
|[self-check.json](self-check.json)|后续正文整理者的静态结构/源指纹/链接检查，不新增数学运行|

新首种子路径(5,4,4,5)，18客户、W=OPT4=18、全终局税40/3。首个选中的原LP为fun=0.02857142857142858>0；原FOUND条件未触发。独立核验另把这个正点回构为mask1/2/8各1、mask52重4的7客户点，沿同一完整策略有W4、OPT7、税16/5，精确余额1/5，总质量归一后1/35。这只证明一个可行点，未提供该策略锥的精确下界。

固定AAAF策略的[15精确对偶证书](../terminal-tax-fixed-policy-probe/exact-audit.json)属于另一个动作图；不能移到本新sigma。原61客户完整认证与旧R105随机扫描亦未重复。

本包两次已发生的计算由root完成：一次原首样本观测及一次独立单位客户核验。正文整理者接手后仅完整读取和静态解析。`run_first_sample.py`需新runtime且会写first-sample，`audit_first_sample.py`也直接写现有审计文件；若今后另行复现，应先复制证据包到独立目录并保留新事件，不能覆盖这里的已归档输出。当前归档不再次运行这些入口。
