# 极小可信尾首回复前移程序证据

[正式程序对象](../../../state/程序/极小可信续局首回复前移的精确枚举程序--程序.md)解释固定15单位客户、全部1024两人纯策略、四个末位BR函数、五个完整尾SPE，以及71/30到13/6的严格1/5间隙。它不做主题商，不验证整棵六人根SPE。

[原码](original/verify_minimum_reply_commutation.py)2779B，SHA256 `631c4a897f21e52fffb50e7d76788a4acc36cbf955b86c0f3c42e9a9494c985d`。仅依Python标准库，无输入参数、无文件写出、无优化器。通常直接执行命令为：

```bash
python3 -B archives/customer-attraction/tools/evidence/minimum-reply-commutation-program/original/verify_minimum_reply_commutation.py
```

这只是后续复现说明；本次没有额外执行此无包装命令。[当前唯一执行](rerun/execution.json)由[replay_main_once.py](replay_main_once.py)透明runpy启动未改原main，并在main返回时被动保存局部量。原main1次，stdout590B与冻结报告逐字节相同，源码/参考报告前后SHA不变，exit0/stderr空。包装器不改frame、函数或数学条件，也不再次枚举。

[captured-main-locals.json](rerun/captured-main-locals.json)3610B包含16个终局的六人收益、五份完整SPE策略含离轨四回复、完整见证和断言量。这是原实现输出的额外透明观测，不冒称独立实现。`last_comparisons=256`与`source_comparisons=64`为源码加计的名义槽数，短路条件的真实执行次数没有被这两个字段统计。

另一个报告任务承担九类型按分母的独立精确重构，不重新运行原main，见[报告证据](../minimum-reply-commutation-report/README.md)。原590B JSON只在该报告包保存，本包stdout保本次真实运行输出；旧4766B数学稿和研究README复用既有归档，不重复原件。

[manifest](manifest.json)列实际阅读、历史与当前事件身份、字节指纹；[self-check](self-check.json)保存正式clone格式、路径、receipt和运行绑定检查。没有Git、认领或完成动作由本子代理执行。
