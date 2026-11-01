# 带目标终局控制器的首对安全值锥探针及三保存点

正文分为[程序合同](../../../state/程序/带目标终局控制器的首对安全值锥探针--程序.md)和[三份数据及精度边界](../../../state/计算/首对安全值锥的三个保存点与微小激励误差--计算.md)。四主源原字节在original/；两个冻结提交、blob、SHA、实读相关比较及交付资产绑定见[source-manifest.json](source-manifest.json)。

|原主源|字节|保存意义|
|---|---:|---|
|[pair_cone_probe.py](original/pair_cone_probe.py)|5331|固定完整控制器客户锥与静态查询交替数值优化；默认200trial未重跑|
|[pair_cone_best_6_3.json](original/pair_cone_best_6_3.json)|24278|q6/r3，28控制状态，111行，质量mask49=7|
|[pair_cone_best_6_4.json](original/pair_cone_best_6_4.json)|70821|q6/r4，84控制状态，361行，质量mask63=4|
|[pair_cone_best_7_5.json](original/pair_cone_best_7_5.json)|345554|q7/r5，330控制状态，1726行，两个近整数质量，原点不是精确SPE|

本源实际依赖[3943 B背景程序](../background-security-pair-probe/original/background_pair_probe.py)，它动态载入[4073 B整数终局全集程序](../coverage-step-background/research/workspaces/customer-attraction/R-7e9f44beea424d469713364afe7dd180/background_induction/search_background.py)。两件已全文实读，均为共享原件，不另重复它们的原入口或数学核验。背景程序导出的security在本源未被调用。

唯一新增数学事件是[audit_saved_points.py](audit_saved_points.py)，[execution.json](execution.json)记录其一次成功。它只用标准库读取三表，完整提升3103个有序决策历史，逐节点真实偏离比较；没有导入原码、原solver、NumPy/SciPy，没有LP或随机扫描。三种数值解释各21419个IC，共64257项；完整静态背景287个，每种解释1932个查询矩阵元素。

[point-audit.json](point-audit.json)保所有正质量、负零位置、参数、状态和各解释结果；[完整账本](point-details.json.gz)含每个有序行动、全部有理IC及静态矩阵。字面/binary的7/5点各有781负IC，最小分别−1/10¹⁶及−1/45035996273704960；原点未被宣布精确SPE。另定义[整数校准输入](calibration-inputs.json)后同控制器通过全史检查，首对2且静态安全值1；原JSON保持不变。

三表都只是trial0/start0/iteration0的改善快照。没有原completed、全命令、运行环境、初始整数客户或完整LP状态，不能据它们补出默认200trial已完成。前两原点精确取等、第三整数校准取等，都不认证整个固定锥最优，更不恢复已经被后继PB-extra反例否定的任意合法背景首对桥。

静态检查见[self_check.py](self_check.py)与[self-check.json](self-check.json)：只做原件及共享依赖指纹、JSON/AST、完整gzip账本结构、实际链接和receipt targets，不导入或重跑数学入口。复现唯一独立核应在新scratch目录放置`round20-pair_cone_best_6_3.json`等三个原文件，其子目录`round20-security-pair/`放原审计脚本；脚本从自身父目录找输入，且拒绝覆盖已有point-audit.json。本包不为改变布局而修改已经执行并绑定的脚本。

报告中的`reported_ratio_minus_query_guarantee`统一用原ratio十进制字面数，分别减去各质量解释下的保存query保证；它不是“binary ratio本身已精确求得”的字段。两个未匹配的原7/5安全值区间如实保留，不额外优化。只有整数校准与前两整数原点有匹配双边证书。
