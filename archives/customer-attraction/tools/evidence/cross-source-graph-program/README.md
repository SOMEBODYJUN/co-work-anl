# 旧回复跨实际源的共同报价图：冻结原件与当前局部核验

正文：[旧回复跨实际源的共同报价图程序](../../../state/程序/旧回复跨实际源的共同报价图程序--程序.md)。本目录只承担源 `cd5e6005172bdbc1524f`；相关JSON/helper/历史audit按依赖保全，不另冒清洗完成登记。

`original/cross_source_graph.py` 为4371B主源，`related/priced_hidden_reply.py` 为2908B价格helper，`related/cross_source_priced_optimum_exact.json` 为815736B旧cross点。原件没有修补；字节、SHA、冻结commit/path/blob均见 [source-manifest.json](source-manifest.json)。大split点共用相邻split-basic-graph-program证据，不重复存一份。

当前新增 [audit_added_rows.py](audit_added_rows.py) 用标准库和Fraction，只提取原psi/build定义，以空继承基底对形式hist基执行新增行逻辑；独立参考按字面隐藏态而非排序压缩计算。它不运行原main、不生成旧3945行、不求解LP。结果 [audit-report.json](audit-report.json) 和 [added-row-slacks.json](added-row-slacks.json) 保513922基系数检查、5760价格键以及旧cross982行、旧split14行全部精确余量。形式基不是实际游戏，两个点也未在本脚本验证全图。

在结果仓库根目录重放新局部核验：

```sh
python3 archives/customer-attraction/tools/evidence/cross-source-graph-program/audit_added_rows.py --split-point archives/customer-attraction/tools/evidence/split-basic-graph-program/related/split_basic_exact.json
```

输出默认写回本目录的两份派生报告；可用 `--out` 指定隔离输出目录。该命令会精确核四份冻结输入SHA，启用assert运行，不使用 `python -O`。本轮初次运行使用clone外共享runtime的同SHA split点；增加hist定义检查后已用上述持久路径再次运行。当前执行信息见 [audit-execution.json](audit-execution.json)。

原主入口依赖旧目录布局和根work.py定位标记，不宜直接在本扁平保全目录运行。原路径、旧hist输入与依赖由 [联合图依赖清单](../combined-branch-master-program/rerun/available-frozen-files-manifest.json) 和 [隔离重放器](../combined-branch-master-program/rerun/replay_default_once.py) 保留。该重放器对应已真实执行的**联合图默认** `combined_branch_master.py --verify`，它内部调用cross.build（priced+optimum），不是再次优化或单独cross点验证。其 [执行记录](../combined-branch-master-program/rerun/execution.json)、[stdout](../combined-branch-master-program/rerun/stdout.txt)、[stderr](../combined-branch-master-program/rerun/stderr.txt) 已全文实读，结果为另一联合点5108行最小余量0。

原cross单独入口如需未来验证，应恢复完整目录、同版本依赖和同模式exact文件，再执行 `cross_source_graph.py --priced --optimum --verify`。这只是接续命令，本轮没有执行它。默认不带verify则会启动浮点优化并可能写文件，本次没有执行。已有旧cross点的作者全4927报告、当前982局部核、联合点5108原运行及一般SPE四者分别陈述。
