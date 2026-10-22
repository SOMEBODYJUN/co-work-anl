# 接续prices个人检查点

本目录只保存Boss5接续prices工作；不提升共享Claim。原Q-CAG-HALF仍OPEN。

- [signed_delta_selection_boundaries.md](signed_delta_selection_boundaries.md)：保存旧36客户δ*根=2；固定13人完整SPE否定所有共同μ总δ预算，并精确区分2002个最优组合的最小/最大；保留真实S/Z及新增重叠余项后正确的剩余义务。
- [probe_signed_delta.py](probe_signed_delta.py)、[signed_delta_report.json](signed_delta_report.json)：定义级Fraction审计与全部矩阵。
- [packet13_source.json.gz](packet13_source.json.gz)、[packet13_all_nodes_audit.json.gz](packet13_all_nodes_audit.json.gz)：原13人完整自动机快照及112050项SPE比较。

当前状态：作者检查通过；父方独立重算13人反例中。未外推任意padding参数。下一步优先研究可选择最优支持的同一μ支付，保留真实G及查询重叠信用，避免独立max损失。
