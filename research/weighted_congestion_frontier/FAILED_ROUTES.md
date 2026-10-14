# 失败机制与回收

## WC-R1-RESOURCE-SUPPORT v1：只堆叠有界support局部模块不能给无界下界

尝试：任意重叠三玩家triad模块，增加人数/层数/degree而每资源仍最多三潜在user。依赖：以局部偏离循环传播至全状态并放大倍率。失败：无权社会成本的逐资源变化满足ΔΦ≤3 C_i(new)−C_i(old)，全局最小者总有3-PNE；这是真正一般上界障碍，非有限搜索失败。否定范围仅support有统一常数界的模块组合，不否定增长support的signed-column族。回收完整r-PNE势论证和必要support增长条件；重试须让support增长或改变模型（模型改变需新Claim）。[完整证明](assets/R1/cyclic_layers/resource_support.md)。

公屏与保存程序的运行说明见 [RUNBOOK.md](RUNBOOK.md) 和 [CHECKPOINT.md](CHECKPOINT.md)。

## 浮点MILP容差不能认证全状态

一些高次数筛查返回tiny positive margin，而导出系数后从literal资源负载逐state精确复算得到倍率1或小于目标。失败位于数值可行性及容差，不是被搜索数学命题的反例。回收：资源列归一化、删不可能帮助strict改善的paired常数项、候选必须完整Fraction重放。具体输入、参数与实际报告见[层状筛查](assets/R1/cyclic_layers/TRIAD_AND_EXTENSION.md)。
