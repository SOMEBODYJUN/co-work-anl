# 极小可信续局首回复前移的严格间隙报告

主源73408151b274cac9fe38的[590B完整原报告](original/minimum_reply_commutation_report.json)保全部15字段，SHA-256 `3834ff80162300c16bb14a17c65d3bc95ac07455ce6c58333410b411cf8bbc37`。[正式正文](../../../state/计算/极小可信续局首回复前移的严格间隙报告--计算.md)完整给15客户输入、末位16报价、四末BR函数、五份完整尾SPE、最低值71/30与13/6、1/5差、67/30门槛及两个客户系数式。

已全文读2779B原程序、590B报告、4766B数学稿、4009B研究README、原main被动捕获及当前独立报告，并比较极小尾/信号重置/覆盖商/父checkpoint的现有正式对象。此例不调用商编译，不能借同目录action_quotient_replay的64/200/六人商测试继承认证。具体路径、来源、大小与SHA见[manifest](manifest.json)。

原实现唯一执行由[程序包](../minimum-reply-commutation-program/README.md)负责：未改源码经runpy进入main，被动profile只在返回时读取局部变量；[事件](../minimum-reply-commutation-program/rerun/execution.json)记main调用1次、exit0、stderr空，590B stdout逐字节等原报告。[capture](../minimum-reply-commutation-program/rerun/captured-main-locals.json)保96收益、五策略及中间量。没有为换成无包装CLI再跑一次；本数据任务原main运行0次。

[audit_grouped_types.py](audit_grouped_types.py)是不同的知情核验路径：不导入原代码，按九个客户类型和重数直接计算16个终局的96收益，先求四末位BR函数，再选各函数下第五位全部最大者，恢复五SPE。它不扫1024个原动作表；所有96值/完整五策略/15原字段和tie、delta逐项通过。报告及本次一次运行说明分别在[independent-report.json](independent-report.json)、[independent-execution.json](independent-execution.json)。原脚本与结果在clone外只读阶段完成，正式持久化后未重复数学循环。

将来如需有意复查，可从仓库根执行：

```sh
python3 -B archives/customer-attraction/tools/evidence/minimum-reply-commutation-report/audit_grouped_types.py --report archives/customer-attraction/tools/evidence/minimum-reply-commutation-report/original/minimum_reply_commutation_report.json --capture archives/customer-attraction/tools/evidence/minimum-reply-commutation-program/rerun/captured-main-locals.json
```

命令只输出JSON；输入路径会随调用位置变化，当前保存报告保实际原运行的clone外路径，不为外观重写历史路径。源码/输入SHA使持久副本可核对。

原last_comparisons=256、source_comparisons=64是通过末BR筛选的16个(c,replies)组合分别固定增加16、4后的名义预算；all/any短路及BR预计算不在这两个动态计数里。5份完整尾策略只有4种规定尾，不能删掉离轨回复不同的重复终局。

此固定例没有验证完整六人根策略、前缀可达性或福利/OPT，没有主题商结论及half反例；一般交换不增方向由既有完整尾平移证明承担。空主题、零客户、重复及任意历史平局保在一般模型，当前有限测试只测一个四覆盖不同的实例。

[自查](self-check.json)仅核实际落点、SHA、JSON、Python语法、正文表与已有数据的一致性、实链接和回执，不再执行原main或两套数学枚举。未操作Git、claim、done或sync。
