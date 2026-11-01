# 完整类型松弛点的父分支精确复核

本轮接续 Boss3 原身份，目标 `Q-CAG-HALF` 仍 **OPEN**。

`audit_full_primal.py` 不导入本轮列定价程序。它复用已有独立审查的437行定义计算器，并把10条末位非对角行和110条保留交叠的末两人行全部按字面索引求和重新构造。输入是 `../round4_pricing/exact_primal_overlap1.json`；输出 `audit_full_primal.json` 保存输入哈希和精确结果。

首个新点有60个正有理类型，W=1，比较覆盖约2.04202004419，全部557条必要条件余量非负；逐项等于发现者报告。因此，旧64类型支持被排除不意味着这些必要条件在完整直方图宇宙已能推出half。这是**模板障碍**，没有实际目录的OPT证书或完整SPE。

后续共同客户跨族切割已发现这个新点仍不能按其边缘语义补全；具体范围以 `../round4_coupling/` 中精确证书为准。本复核不把新点称作一般猜想反例，也不声称其为557行模板精确最优值。

运行：在仓库根执行 `python research/workspaces/customer-attraction/R-c4732bee2f7b4e50a70568170e3334ae/round4_parent/audit_full_primal.py`。只写本人目录的独立输出，不覆盖既有冻结点。
