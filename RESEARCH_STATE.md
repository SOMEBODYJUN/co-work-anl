# 当前研究前沿

## 新主攻：一般不相关并行机的统一常数2壁垒

`UM-TARGET-v1` 仍OPEN；本次建立独立存档 `unrelated-machines`、[精确模型与地基](research/current/unrelated_machines/README.md)、[承重前沿](research/unrelated_machines/RESEARCH_STATE.md)及[BOSS启动](research/unrelated_machines/BOSS_START.md)。已知槽舍入与配置gap重构不作为原创突破；新增[安全大边匹配过滤及共享逃逸容量反例](research/current/unrelated_machines/heavy_matching_residual_and_escape.md)，逐星匹配即使覆盖必经大边也仍可保留gap趋2。尚无一般新算法。新增[长链与固定机器联合投影边界](research/current/unrelated_machines/long_path_coalition_gap.md)：任意大围长简单图仍保留gap2；只共享单机边际的固定大小联合见证不足，完整三机交叠相容性在该树宽2族上精确。该阶段已内部独立攻击，无一般算法或新颖性认证。新存档按scope隔离保存，旧研究保留原精确身份。

已形成[强制残余容量计数闭包与细分攻击](research/current/unrelated_machines/bundle_coupling_subdivision_barrier.md)：过滤器健全且位多项式，在原两树族精确但被任务细分绕过；完整两机器配置耦合仍有sup gap2。此为准确方法边界，未给统一新近似比。独立覆盖与有限证据见正文入口。

新[五机树再耦合反例](research/current/unrelated_machines/tree_markov_completion.md)表明：真实最优分布也可能在丢掉非树相关性后产生冻结任务无法低于2T补全的态；本例可一步修复，仍缺一般repair/位复杂度证明。

新增[极小超载星精确消去](research/current/unrelated_machines/minimal_star_contraction_and_capacity_gap.md)可提升实际调度，已独立攻击；它与现有传播/pair强化仍被紧凑共享容量族限制。多任务压缩须保身份，下一路线是资源池匹配接口，尚无统一ε。

## 已完成的拥塞旧题：严格否定

[线性次数的全状态无均衡族](research/current/weighted_congestion/linear_degree_allstate_lower_bound.md)已给完整一般证明：每整数d≥2^20存在MODEL有限游戏，每个纯状态都有严格(d/10)改善。新身份`WC-LINEAR-DEGREE-ALLSTATE-NONEXISTENCE-v1`与`WC-MATCHING-LOG-UPPER-NEGATIVE-v1`严格否定绝对C,d0的普遍(Cd/ln d)-PNE保证。所有参数正有理、费用纯d次、每人两个非空不交动作；不限制人数、资源数或权比。

承重链为健康窗口成本预算→全部product-front端点覆盖→同类最早异位单人修复→实际clock degree=d→∀C∀d0否定量词。独立先重构后冻结攻击覆盖这条链；整数/Fraction审计只支持所列实际有限输入。追加审查另给不经对数或微分的整数分层次数证明，完整多类拼装核验明确区分基体扭转与固定锚点时钟的非对称性；原冻结正文及Claim范围不变。W漏定义和B_actual未定义已修复并按最终hash复核；没有尚成立的fatal objection。外部同行评审、新颖性与最优常数未认证。

现有结论已重构为[自足英文主稿](research/current/weighted_congestion/linear_threshold_article.pdf)，包含完整一般证明、已核引用和实际十页PDF；内部全文审读及逐页检查已完成。此为写作交付状态，未改变数学身份，未认证全球优先权或录用。

## 长期目标与剩余义务

WC-TARGET v1原身份保持刻画a_*(d)。新下界d/10与另列Paper Fact的一般d上界给增长阶Θ(d)，但没有求出精确常数或有限d最优值。优先后续可核查/简化新证明、优化参数、检索优先权并组织外审。全类o(d)存在性已经被新全状态族否定，不再作为开放义务。

旧奇环T_d下界及一般cohort奇环实际阈值恰T_d、有限权类/height势、共享side的UFτ预算、森林lift、完整selector表示与方法障碍均按原合同保留；新结果不升级其他候选。详细范围从[专题数学地图](research/current/weighted_congestion/README.md)、[精确账本](research/weighted_congestion_frontier/CLAIMS.md)与[资产目录](research/CATALOG.md)进入。

## 独立保留的研究线

设施选址的共同目录/稀疏异构尖锐界、复杂度、任意设施数因子2与有限构造均保留；一般位多项式构造仍开放。顺序客户吸引的一般半覆盖仍开放。正占用核是独立秩/闭包工具，一般WC签名桥仍未建立。这些目标不被本次题目替代。

研究状态、证明、内审、外审、实现和新颖性分开记录。按[研究生产规则](research/REPOSITORY_GUIDE.md)维护正文、精确账本、数学图、目录与入口，运行相应核验并通过work.py checkpoint普通推送main；远端送达和数学验收分别核对。
