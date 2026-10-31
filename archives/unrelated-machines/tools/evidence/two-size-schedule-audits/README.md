# 两尺寸/固定工作五源程序证据

五主源：两尺寸独立review4a5、count-state原程序5e25、带标签独立程序72d、fixed-work原review dc7d、原审计82aa。五比较原件为两尺寸canonical/内部源/旧JSON、fixed-work canonical/旧JSON。全部原字节定位/SHA见[manifest](manifest.json)。正式资源：[两尺寸入口与标签身份](../../../state/计算/整比双尺寸原入口的计数状态与带标签隔离审计--计算.md)、[固定工作单步与纠错范围](../../../state/审查/固定工作单步原审计与三件启动纠错的分域复核--审查.md)。

原三程序只用标准库，无外部输入文件/仓库导入，原main的hardcoded参数完整保。新`count-001`/`labels-001`/`fixed-001`原目录初始空，各只执行未改原入口一次，真实命令/cwd/源码SHA/Python/assert/时间/退出码与stdout/stderr保齐。`run_originals_once.py`拒绝任何目标目录已存在，不会重复覆盖。

两neutral输出按旧9f JSON的两个result逐字段全相等；labels保原Python dict stdout并用literal语法解析，未冒旧stdout原字节。fixed完整4105B stdout与旧de9逐字节相同。见[replay-comparison](replay-comparison.json)。三个有限程序不承担一般证明；单步入口不包含后来的三件修复验证。

`verify_delivery.py`只读原件/已完成运行/冻结字段验证，不再执行数学入口；实际结果`verification.json`。无旧bulk/reset等入口复跑。历史scratch代码别名无独立旧字节，不以规范程序倒造其内容身份。旧JSON/Boss2对象不复领、不改done或共享正文。
