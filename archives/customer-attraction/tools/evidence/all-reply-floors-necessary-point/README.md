# 实际报价地板图的固定有理点

源daefb4354a8db9a4653d、815347B。完整原件复用[已保文件](../all-reply-actual-floors-program/related/all_reply_floors_exact.json)，SHA-256为f6f4d5c28857e8e6350bdc8528daa6109122bce8a6fb00e8ac5c3150ffc42314，不再复制815KB。所有12字段和1905列保在该文件；[正式正文](../../../state/计算/显式回复实际报价地板图的有理点--计算.md)解释其模型、参数、16hist、194组三状态、1306交叠、后继切除和SPE边界。

## 独立数据核与原main事件

在仓库根运行python -I archives/customer-attraction/tools/evidence/all-reply-floors-necessary-point/audit_floor_point.py，可用标准库重算全部字段/列、隐含00、交叠上界、六R/Z容量、旧B/C预算及OPT单换，输出independent-point-audit.json。其两次外部准备运行与一次最终默认路径运行如实区分在independent-execution.json；没有原图导入或发现LP。

报告还逐1306项检查集合交叠Fréchet下界：191项负；列1205给两R边缘均等hist质量而保存交叠0的明确见证。这是保持原辅助量逐项不变的会员实现缺陷，不能当成原线性图不通过。195个交叠值低于其嵌套最大值；全共同阈值抬升在原行正交叠条件下可改变这些坐标而保旧行，但不能修复只读hist/R/Z的后继PAIR负值。

rerun/保第一次对该floor权点与4963flags的原验证main调用。它由capture_floor_main.py设置原argv --priced --optimum --verify，再用runpy.run_path(original, run_name="__main__")执行未改原源；sys.setprofile仅在原main返回时读取names、cols、slacks、w。原函数和数值未被替换，主源及输入保持原字节。观察器另核全部1905个生成列描述符。

这是带只读观测的原main调用，不是无包装普通CLI，也不是另一套独立4963行推导。正常开启assert、退出0、stderr空，原4963余量为2723正2240零。原stdout和全部名称/分数保在rerun/stdout.txt及rerun/original-row-slacks.json；执行环境、实际命令、原argv、49份冻结依赖SHA和原点SHA保在rerun/execution.json。未运行优化或重复旧9900发现事件。

capture_floor_main.py可在已准备的完整冻结运行树上以两个参数RUNTIME和OUTPUT运行；OUTPUT须先存在。该运行树的源文件由[联合程序依赖包](../combined-branch-master-program/README.md)和本点共享输入提供。historical-run_original_once.py是此次外部运行的原封装记录，保其真实外部布局路径，不伪装成自动准备环境的通用入口；不应为检查本证据而再次运行。

## 既有证据复用与审计

reconcile_evidence.py只读取报告，核本点SHA及逐分数相等性：当前独立数据审与原main的194个状态上界、2612交叠上界、28项其它预算；已有36floor余量与原main末36行；已有8cut及72mixed中本点的映射/负值。它不重建图或重跑发现器。

source-manifest.json记录实际来源、全文比较及运行身份；self-check.json核最终target、JSON、脚本语法、链接、源码/原点/运行报告SHA。原4963可行性、局部独立数据检查、Fréchet反实现见证和完整SPE严格分开；没有最优性、全域half或完整反例结论。
