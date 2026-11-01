# R-3b6b fractional_explore.py 清洗摘要

源 `ca693c33fc79b2c3adda` 定义客户矩阵、前缀负载和 SLSQP 对数 benchmark；r=1 返回最大单主题分数，r>1 返回连续单纯形候选 `g·q` 与 KKT 样残差。源码明确数值发现不是证明；没有全局最优、有理误差界或离散策略实现。三个下游搜索的随机参数与未命中边界见正式增量页。处置 retained。
