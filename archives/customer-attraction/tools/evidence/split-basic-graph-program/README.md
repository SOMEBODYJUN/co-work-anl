# 对角回复基础图的源程序及局部精确审计

正式对象：[对角回复预算拆分的基础图程序](../../../state/程序/对角回复预算拆分的基础图程序--程序.md)。主源 `48e907edcc1b4908d039` 的 [split_basic_graph.py](original/split_basic_graph.py) 保原4563字节。另保局部审计使用的 [split_basic_exact.json](related/split_basic_exact.json)，它只作本源相关输入，未在本receipt额外处置该数据源。

原程序构造调用链及完整SHA见 [source-manifest.json](source-manifest.json)。旧输入和源码共用 `../combined-branch-master-program/dependencies/` 中的原仓库相对布局，不重复保存大依赖。原联合图 `--verify` 的唯一真实执行见 [共享执行记录](../combined-branch-master-program/rerun/execution.json)，其中调用原split.build并通过56行逐列合回断言；本包没有重复完整图build或原CLI。

本轮新增 `verify_split_rows.py` 直接从真实收益和强PAIR表达式重建系数，只提取原 `values(r,z)` 标量函数作比较。它不导入原图、NumPy或SciPy。73728种局部状态共2064384个系数全等，16hist上106680个新行矩系数全等，冻结split点全部56个新增行余量非负。其余3889行没有在此独立审计。

从仓库根运行：

```sh
python3 -I archives/customer-attraction/tools/evidence/split-basic-graph-program/verify_split_rows.py
```

默认读本包原程序与split点，以及共享依赖中的旧attractive点、nr和nest源码。`--runtime PATH` 可切到保完整原仓库布局的隔离目录；`--output PATH` 可另选报告位置。assert必须开启；脚本拒绝 `-O`。运行只写独立报告，不覆盖原件。

结果见 [independent-report.json](independent-report.json)、[实际执行记录](independent-execution.json)、[stdout](independent-stdout.json)。报告保56个精确余量，不以一个PASS词代替具体域。scope区分独立系数审计、作者原图执行、原旧split点的历史全图报告；没有新LP优化、完整SPE认证或一般half结论。
