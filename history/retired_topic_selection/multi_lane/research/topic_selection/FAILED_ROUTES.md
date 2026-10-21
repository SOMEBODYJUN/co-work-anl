# 已排除选题与可回收信息

原一般不相关机统一优于2及其一般反面：保留OPEN；本轮暂退出主攻，因为目前没有与本轮预算相称的可验证全输入切入口，而非数学上已否定或无价值。

其他淘汰项待首轮原文与后续核实后登记。每项说明原问题、已知覆盖/失败位置、排除范围、保留工具和何种条件变化时值得重开；不将网络失败当数学反证。

## NA02：把weighted Leontief精确多项式当新公开题

作者A问题没有误读：2509.08767v3与AAMAS2026正式版§8仍写weighted polynomial开放。但[已知接口重构与完整来源链](notes/leontief_fisher_known_interface.md)核实，Brandt等的NE=Lindahl、Tao–Zheng2025的public Leontief/private linear Fisher对偶及Orlin2010算法直接覆盖其目标。失败类型是新颖性被既有定理直接覆盖，非我们算法不成立。保留同一估值矩阵、预算、零值、精确spending输出和有理恢复接口；只有新的约束或偏好确实破坏这条已有桥且有自然价值时才另立问题，不能靠给已知推论改名重开。

## 固定真实权重势的37/33，以及单字母表递推立题

AT01的37/33仅在指定有限人口及真实权重缩放模板内最优。[全人数type-scaled构造](notes/finite_weight_scaled_potential.md)给更好的64/59，因此淘汰“这个小常数就是新最佳阈值”的叙事。AT02固定{1,3}的curl充分条件已由HKM2011 Proposition3.4直接包含；单递推通解不足主成果。保留统一字母表结构、可验证最优模板和非平凡动态后果的可能性；未否定全部有限权重研究。

## 重边多重图中的内部单位包全平分

[五顶点、k=1反例](notes/heavy_edge_residual_and_charity.md)严格否定把非heavy端点内部的所有平行包先平分的压缩。容量可以沿普通路径传播且超过奇偶误差量级。一般FPT未被否定；保留森林阈值消息，只有能表示完整边界响应的压缩才可重试。

## 背包类内均匀化与无条件Poisson拆分

[精确反例](notes/two_size_knapsack_obstructions.md)否定固定x时最坏权重总可类内统一，允许零权sub-support亦失败；保持期望成本的Bernoulli拆分也可提高ratio。没有否定可同时改x的全局归约，没有否定一般CRS猜想。另EC2025的一般knapsack基线已为1/3，旧“超过.279”不再是普通CRS新目标。

## 配置预算的伪新常数与已经闭合的两类型LP子题

GA05等opening-cost是CCPV2011配置coverage+bins拟阵的已知范围。GA06给定稀疏支持的[确定性(1−1/e)/2基线](notes/configuration_reduction_boundary.md)可由旧pipage直接推出；不能以从1/8改成普通常数立题，亦不能把指数pricing当免费。GA16任意维两射线的[充分性](notes/two_profile_lp_in_arbitrary_dimension.md)已在本轮闭合并入GA01，不再占未解题名额；高维没有“至多两射线必要”的结论。

## 无条件personalized bivalued WEFX+fPO

不能直接作为肯定存在目标。2604.08345未来方向的更一般措辞须与2601.03438 §1已知两代理正估值反例核对：等权已不可兼容，所以任意权重版本亦不可一般成立。已独立复现，见[边界记录](notes/fair_fpo_compatibility_boundary.md)。失败类型是一般命题为假；保留支持权阈值与精确支配oracle。仅在增加可检验结构假设、弱化近似公平或改PO后重开，并另立版本。

## 一般additive chores EFX肯定存在，以及直接由旧例推出强近似障碍

He–Tao 2606.08872v2 §3给出反例；[本轮精确复现](notes/chores_trivalued_exact_boundary.md)确认固定例无EFX，但最优α仅23/22，且大项成本向两侧改变均可恢复EFX。一般肯定存在失败属于命题错误；将该固定例称强近似下界属于证据范围扩大。保留类型压缩与逐项移除oracle；新近似/结构题必须另立精确范围并补新机制。

## 任意EFX起点的逐效用单调Pareto补全

[三代理五物品参数族](notes/personalized_bivalued_monotone_completion_obstruction.md)否定了这个强桥。失败类型为路线合同本身为假：起点EFX、非PO，但全部严格Pareto支配者都非EFX。一般EFX+普通PO存在问题未被否定；基例仍有13个EFX+PO。保留小参数反例及独立oracle；限制起点/允许暂时效用下降/另建全局势时可重开。全球新颖性未确认，不单独当主选题。
