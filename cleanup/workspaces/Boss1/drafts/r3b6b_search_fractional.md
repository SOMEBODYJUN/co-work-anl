# R-3b6b search_fractional.py 清洗摘要

源 `2eb5e65540a85e23fdeb`：固定 `Random(6709884)`，n=3..6 各100个随机 k=7 实例，mask 概率0.22、重数1..9。调用 ExactSPESolver 求根 floor，benchmark 用 SLSQP 连续分数目标；对每个首动作计算 `D=u+(n-1)vb-nv`，仅当 `D<-1e-4` 才写 obstruction。冻结源没有 obstruction 输出，不能把未触发当成全称不等式。处置 retained，详见正式增量页。
