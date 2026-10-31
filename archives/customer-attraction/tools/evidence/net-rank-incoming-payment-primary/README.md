# 固定价格取消与入流付款：原件及一次回归

本目录保存五份正式认领主源37087字节、三个实际依赖2107字节，以及新空根中的一次未改原程序执行。主源ID、冻结commit/path、Git blob、SHA-256、大小及证据位置见[source-manifest.json](source-manifest.json)。冻结来源是`68fad804ec5946cb296f77dc5b336308a66abf12`与`aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c`的相同内容，原件未经改写。

- `original/`保五份原件，含历史1033B报告；它从未放入运行输出位置。
- `inputs/`保935B游戏JSON、481B完整策略JSON和691B真实`customer_attraction/__init__.py`。最后一份仅供`Path.is_file()`找根，不被import，其导入模块也未被程序使用。
- `replay/source-root/`按原repo相对路径保未改7959B程序及三个必要文件；运行前不存在旁边的报告，运行后才生成新1033B报告。
- [execute-once.py](replay/execute-once.py)以`runpy.run_path`实际调用原脚本一次，断言启用。外部profile只计源码入口，结束后只导出已有globals；不再调用原函数。
- [execution.json](replay/execution.json)记录argv/cwd/环境版本/时间/状态/新旧输出SHA；[stdout.txt](replay/stdout.txt)与新报告、冻结报告逐字节一致，[stderr.txt](replay/stderr.txt)为空。
- [execution-state.json](replay/execution-state.json)是外部辅助导出，含44次capture、42份单位价格/取消、10query菜单、零残余source/maxflow及84比较/128策略实际循环域，不冒充原报告字段。

这不是新SPE搜索或一般人数验证。原脚本实际检查30项全历史IC、25终局最优性；后局部取消只剩末角色一单位源，incoming0、残余Hall源0、正增广0。原报告PASS不能升格为一般incoming付款、NET-FRAC、动态cut预算或six-player half证明。数学内容见[单证书计算](../../../state/计算/净删源捕获与自由查询的单证书回归--计算.md)和[内部核读](../../../state/审查/固定价格取消与入流付款的内部核读--审查.md)。

更早原流/Hall/自由query及共享激活导航仍是其它待逐源整理材料；这里没有替旁读或导航源提交done。当前阶段二的关系判断、自查、五份semantic receipts及精确copy清单放在`cleanup/workspaces/Boss4/r3-net-rank-incoming-payment/`。
