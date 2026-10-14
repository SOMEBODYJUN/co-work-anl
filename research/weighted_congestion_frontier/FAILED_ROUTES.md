# 失败机制与回收

本轮已审查受限对称拓扑的精确调参障碍。形成反例、obstruction 或有价值的失败路线后，在这里准确记录尝试机制、失败步骤、否定范围、可复用结果和重试条件。

公屏与保存程序的运行说明见 [RUNBOOK.md](RUNBOOK.md) 和 [CHECKPOINT.md](CHECKPOINT.md)。

## Symmetric two-column full-state tuning — closed asymptotic route

尝试：保留一重/同权轻两列策略，仅改变主副费用或完整m状态的attack选择。关键机制：期望中间轨道或混合多项式超过原保守证书sup。失败位置：light稳定整数区间不能与反射相交；边界平移或单轻玩家反演供两strict tests，再endpoint chord与线性系数消元还原原monomial域。

否定范围：α≥ρ=(1+√3)/2的上述完整拓扑，允许任意w>0与非负多项式。不是“原游戏每个状态的最佳改善等于保守min”，而是跨参数sup还原。回收结果：源式包络sharp asymptotic、T_d≤max{ρ,F_d}，d足够大时T_d=F_d。可重试条件：改变叶子关联/费用对称、采用异权full-state机制，或研究α<ρ的有限degree局部现象。完整proof与zero边界见assets/R3/full_topology/proof.md。

## WCF-R3-FIXED-DEGREE-FAIL-v1

尝试保留degree32交叉候选的4权、14资源和amplitudes，仅提高六项monomial次数。具体失败：degree40的0111/1000状态最大改善≤9/5；全部状态极限最佳factor=5235403/2930833<9/5。全support外的high-degree资源趋零，quadratic广播保留，瓶颈换到不同状态。见[完整失败证书与复算](assets/R3/crossover_audit/README.md)。排除这组固定参数的全degree延伸，不排除重配权、系数或增加玩家。可回收满support指示器极限表示；未来只有改参数/拓扑并重证全状态才值得再试。

## Separate-band Shapley normalization and minimum-potential density

按每player所在band单独除scale会让two-user cubic混合差分κ与κ/M冲突，ordinary exact potential不存在；恢复同一个weighted potential仍可由two singleton bands造成selector ≥d/6损失。详见[dense proof](assets/R3/dense_bands/README.md)。仅排除该归一化/selector，不排除其他势或存在证明。更强的[全模型padding reduction](assets/R3/potential_padding/proof.md)说明minimum occupied potentialdensity任意大仍与全类同threshold；新玩家通过empty退出，无法提供active density。可回收本地R接口、iid-share表示、potential/active distinction；重试必须引入并保持active/mandatory condition或新的shared-scale机制。

## Odd-ring positive local tests: tuning has an exact ceiling

尝试只增加奇环长度、改变cohort数、权尺度、主费用monomial degree或系数以继续提高α。新精确失败机制：F_(k,n)(x)≤F_(k,1)(nx)，Q/(tP)=F_(d,1)(1/t)，权乘积相等；α≥T_d迫使所有因子≤1，使正系数严格闭环不可能。否定范围仅指定两类正localtest系统，不是整个策略拓扑或全类存在问题。回收成长族a_*(d)≥T_d∼d/ln d、有理系数构造及程度预算(α−1)lnα<d。重试须采用完整state dependent攻击、改变局部test或新反馈拓扑，而非继续同证书调参。详见assets/R3/odd_ring_sharp/PROOF.md。

混合多项式扩展亦已封住：任意每组nonnegative degree≤d形状F_i,G_i的两个归一化因子都是monomial因子按正M_k/P_k的凸组合，constant项给负因子而非例外；故仍有同exact T_d。精确范围保留action/cohort共shape；action或clone异形费用需要新claim。完整actualtopology仍缺从certificate失败到真实稳定状态的桥，不能偷升该范围。
