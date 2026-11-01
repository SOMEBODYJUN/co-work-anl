# 六人级联扫描两原表

[正式正文](../../../state/计算/六人级联扫描快照与同覆盖大块的完整策略--计算.md)完整保七条历史、八个最佳字段、六个客户类型和19608条原动作的数学合同。两原件原样保存；2.5 MB动作表没有压成直方图或改写为计数策略。

- `original/cascade_scan.json`：请求20轮，只保存0…6；不补造退出原因。
- `original/cascade_scan_best.json`：11客户、W6/OPT11、七标签中T0=T1。完整图的唯一非统一计数组只是别名不同。
- `audit_saved_data.py`、`data-audit.json`、`execution.json`：唯一一次新的全字段/全动作读取及其事件。读取器核解析SPE证明的全部前提，不重算117648项IC；该数是解析覆盖域的基数。
- `source-manifest.json`：两源完整库存身份以及跨包复用的实际生成器/四依赖。
- `comparison-manifest.json`：全文比较对象与对应作用。
- `finalize_static.py`、`self-check.json`：只检查原件、报告、源代码AST、链接与两份回执，不再执行数据读取器或任何数学程序。

生成器原件复用[Boss3的cascade包](../cascade-original-nine-boss3/original/f08bcbcb7a5f6f2bd41b/cascade_attack.py)，不重复复制。当前字段相容不能唯一绑定历史生产版本。原main/LP/BI/规范验证器及完整数值IC重放均为0；真实一次数据读取事件在仓外完成，移入的报告保持原字节。

若需要在未来独立复核数据，读取器使用显式输入及**尚不存在**的输出：

```sh
python audit_saved_data.py original/cascade_scan.json original/cascade_scan_best.json /absolute/new-output.json
```

这会产生新的读取事件，不能冒称原发现重放。当前已充分核验的数据没有为补计数重跑。
