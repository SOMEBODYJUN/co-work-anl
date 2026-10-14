# 失败机制与回收

本R2工作分支已核实如下精确接口障碍。形成反例、obstruction 或有价值的失败路线后，在这里准确记录尝试机制、失败步骤、否定范围、可复用结果和重试条件。

公屏与保存程序的运行说明见 [RUNBOOK.md](RUNBOOK.md) 和 [CHECKPOINT.md](CHECKPOINT.md)。

## WC-R2固定幂势去密度障碍（v1）

尝试：将Σw_i^p C_i的稀疏谱控制推广为独立于资源权重人数密度的加入边际界，p∈(0,1)固定。依赖：新增资源上所有其他玩家权重p矩相对own成本有uniform控制。失败：已有N个权1/N玩家、c=x^d，加权1玩家时externality/own新cost=N^(1−p)(1−2^-d)→∞。这是精确接口失败，不是均衡不存在；该固定用户实例可有真正均衡。

否定范围：固定p<1、原正线性cost势的uniform新增边际估计。回收：稀疏谱moment theorem成立，geometric separation给O(log d)。重试条件：资源层抵消/自适应非线性或无需所有状态uniform边际的局部min certification。完整review在assets/R2/weight_density/review.md，当前proof在../current/weighted_congestion/weight_density.md。
