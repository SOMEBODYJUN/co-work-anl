# 失败机制与回收

本轮已审查受限对称拓扑的精确调参障碍。形成反例、obstruction 或有价值的失败路线后，在这里准确记录尝试机制、失败步骤、否定范围、可复用结果和重试条件。

公屏与保存程序的运行说明见 [RUNBOOK.md](RUNBOOK.md) 和 [CHECKPOINT.md](CHECKPOINT.md)。

## Symmetric two-column full-state tuning — closed asymptotic route

尝试：保留一重/同权轻两列策略，仅改变主副费用或完整m状态的attack选择。关键机制：期望中间轨道或混合多项式超过原保守证书sup。失败位置：light稳定整数区间不能与反射相交；边界平移或单轻玩家反演供两strict tests，再endpoint chord与线性系数消元还原原monomial域。

否定范围：α≥ρ=(1+√3)/2的上述完整拓扑，允许任意w>0与非负多项式。不是“原游戏每个状态的最佳改善等于保守min”，而是跨参数sup还原。回收结果：源式包络sharp asymptotic、T_d≤max{ρ,F_d}，d足够大时T_d=F_d。可重试条件：改变叶子关联/费用对称、采用异权full-state机制，或研究α<ρ的有限degree局部现象。完整proof与zero边界见assets/R3/full_topology/proof.md。

## WCF-R3-FIXED-DEGREE-FAIL-v1

尝试保留degree32交叉候选的4权、14资源和amplitudes，仅提高六项monomial次数。具体失败：degree40的0111/1000状态最大改善≤9/5；全部状态极限最佳factor=5235403/2930833<9/5。全support外的high-degree资源趋零，quadratic广播保留，瓶颈换到不同状态。见[完整失败证书与复算](assets/R3/crossover_audit/README.md)。排除这组固定参数的全degree延伸，不排除重配权、系数或增加玩家。可回收满support指示器极限表示；未来只有改参数/拓扑并重证全状态才值得再试。
