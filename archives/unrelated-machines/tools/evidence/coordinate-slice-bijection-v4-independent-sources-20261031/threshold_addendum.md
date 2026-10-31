# 坐标切片编译的精确单位阈值：v2陈述增补

Claim ID/version：`UM-Q-COORDINATE-SLICE-PARTIAL-MINREP-COUNTEREXAMPLE-v2`。

本版继承且保留 v1 Exact A–D 的全部对象、参数、结论及范围：原文件 `coordinate_slice_partial_minrep_counterexample_exact_statement.md`，SHA256 `2d889e2109657bffda860acbad4ce64accd06fd207d47c96fa803647fc15b6a8`。不覆写 v1。v1 仅冻结过候选，尚未作为现行 Claim 登记。

明确对象：simple D-regular 二部全投影游戏、共同 Σ 大小 Q、每个右点的 D 邻居编号；每test资源 [D]^Σ；每左点label状态树根分D tests，随后按固定坐标顺序选择除投影β外的Q−1坐标，叶固定x_β=邻居index；根selector单位任务、每树弧任务父端1/D和子端1。全部树和矩阵显式展开，无额外任务或外部约束。

在 v1 结论以外新增：

1. 对 v1 所定义的任意 simple D-regular 输入游戏（D≥3，Q≥2，两侧非空），该完整实际 P 有 makespan≤1 的合法调度，当且仅当原投影游戏有满足全部边的单标签赋值。两向均须针对全部原任务及实际机器负载。
2. 对 v1 的具体 t copies K_D,D、Σ={0,ell_j,p_i}、π_ij(ell_j)=0、π_ij(其他)=p_i、D>max(2,2g/rho) 的 NO 家，实际最优值**恰为**1+1/D。
3. v1 的复杂度句准确读作“固定满足条件的 g,rho,D，而变化 t 时显式展开为多项式”。固定D本身不逻辑决定rho。没有新增binary D变化时的uniform原输入多项式编译声明。

依赖：只用完整坐标slice定义、实际任务定义、v1 的显式调度上界及处理时间网格；不导入 PCP 困难性。结论不声称 near2 gap、一般UM反面、任何特定PCP像上的逃逸或其它叶排列的失败。

Status：root 已有独立证明，但本文件不含证明。请先只据 Exact 重构新增结论，再读冻结证明攻击；v1独立记录不改。
