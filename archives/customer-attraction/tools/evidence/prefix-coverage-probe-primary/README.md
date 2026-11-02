# 固定前缀覆盖补偿探针的两原件与恢复

主源641419c9b3c06f082c59（851B JSON）和dabbe5516e3c88e1bb89（3211B程序）均由clean show完整导出，SHA/blob及两冻结定位见[source-manifest.json](source-manifest.json)。数学语义与全部参数边界见[正文](../../../state/程序/固定前缀覆盖补偿的有限全续局探针--程序.md)。

original保原字节；runtime按原parents[5]布局保存原程序及确切冻结customer_attraction的init/model/exact/certificate四依赖，均与inventory同SHA。默认main新执行一次，只改output路径；[execution.json](execution.json)、stdout/stderr和replayed.json保事件。冻结JSON与新JSON除config.output外完全同字段；0退出，stderr空。百样本阴性不是全域证明。

[saved-point-independent.json](saved-point-independent.json)是另一标准库实现对一个保存点的60倍整数收益集合递推，126状态，唯一终局(2,0,4,0,0)、29客户、旧覆盖5、新覆盖23、残余24、余量27。它不调用规范solver，范围仅保存点。实际一次父方驱动源代码完整保存在[共同枢轴包的driver-record.py](../common-pivot-2408-primary/driver-record.py)，其中两原入口和两个独立块分别标明；绝对scratch路径是当次执行定位，不是未来复现必须路径。

重做新事件时应将runtime复制到新目录后运行原probe并指定新output，不覆盖本包历史结果。原程序只需Python标准库。当前完整依赖和原运行输出已保全，不把先前环境丢失的旧运行重述为本次原事件。没有新增LP、完整策略验证或阶段三图。
