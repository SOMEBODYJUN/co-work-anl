# 当前研究前沿

## 新主攻：一般不相关并行机的统一常数2壁垒

`UM-TARGET-v1` 仍OPEN；本次建立独立存档 `unrelated-machines`、[精确模型与地基](research/current/unrelated_machines/README.md)、[承重前沿](research/unrelated_machines/RESEARCH_STATE.md)及[BOSS启动](research/unrelated_machines/BOSS_START.md)。已知槽舍入与配置gap重构不作为原创突破；新增[安全大边匹配过滤及共享逃逸容量反例](research/current/unrelated_machines/heavy_matching_residual_and_escape.md)，逐星匹配即使覆盖必经大边也仍可保留gap趋2。尚无一般新算法。新增[长链与固定机器联合投影边界](research/current/unrelated_machines/long_path_coalition_gap.md)：任意大围长简单图仍保留gap2；只共享单机边际的固定大小联合见证不足，完整三机交叠相容性在该树宽2族上精确。该阶段已内部独立攻击，无一般算法或新颖性认证。新存档按scope隔离保存，旧研究保留原精确身份。

已形成[强制残余容量计数闭包与细分攻击](research/current/unrelated_machines/bundle_coupling_subdivision_barrier.md)：过滤器健全且位多项式，在原两树族精确但被任务细分绕过；完整两机器配置耦合仍有sup gap2。此为准确方法边界，未给统一新近似比。独立覆盖与有限证据见正文入口。

[共同大边选择与块容量](research/current/unrelated_machines/joint_matching_completion_and_block_cuts.md)进一步定位：给定见证可条件舍入，低余量精确选择NP完全；专用条件块切面恢复整个共享逃逸族阈值。仍缺一般统一余量和构造；这些接口结果不升级主目标。

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

不相关并行机的独立配置＋逐边普通LST路线新增稀释终端gap2；在条件探针内保留大任务基数可以准确识别该族。详见[正文与下一义务](research/current/unrelated_machines/diluted_sink_probe_gap.md)，未得统一改善算法。


共享小端与稀释终端组合已进一步反驳“配置＋GHMR＋全部普通LST边探针”这一必要证书合取的统一阈值改善；主目标仍OPEN，条件内更强约束尚未被排除。

半单位新身份已关闭固定大小分界的共同见证窗口：每个固定δ∈[0,1/2)的(Aδ)存在性NP完全；P≠NP下无总位多项式OPT≤T承诺构造。它仍不是统一低于2算法的困难性，下一步转向实际联合舍入损失。见[共同选择正文§3a](research/current/unrelated_machines/joint_matching_completion_and_block_cuts.md)。

[全局单行基数与紧凑共享逃逸](research/current/unrelated_machines/row_count_escape_gap.md)新增安全位多项式查询及准确反例：完整任务身份/多槽/每机每配置计数延伸仍与GPC₂合用保持gap2；条件块切面仍可识别本族。UM-TARGET-v1继续OPEN；一般共同负载耦合与统一舍入未解。

[直接联合槽的正面衔接](research/current/unrelated_machines/joint_slot_prefix_rounding.md)给UM-ROW-SPREAD-TWO-ROUND-v1：删去零任务后每行正时间跨度≤2（逐机尺度不同）时，显式前缀计数LP加一次全任务槽匹配给3/2位多项式构造。它是VW/ST已知机制的直接推论，绕过过强(Aδ)见证；未消除一般行内跨尺度混合，主目标仍OPEN。

[稀疏深树的条件配置证书](research/current/unrelated_machines/sparse_conditioned_configuration_gap.md)进一步排除仅叠加独立单边完整配置测试的统一阈值改善：每任务至多三选，间隙仍趋2。已独立重构、逐边精确核验；完整四机器交集联合分布可识别该族，极小星预处理范围尚未覆盖。下一义务是共同相关性或联合迁移，不是更多独立单机测试。

紧凑共享逃逸新增多行真实容量的尖锐预算，见同正文§6与UM-COMPACT-MULTIROW-EXTENSION-v1；独立行见证可同时覆盖除2k个中心外的全部机器，仍不足以给共同T调度。

最新条件化义务已细化：UM-MACHINE-CONFIG-PROBE-GAP-v1在紧凑共享逃逸族上证明所有单机完整配置均有各自完整配置LP延伸。单个证书已同时守住各机容量，失败来自证书之间无共同base。对共同逃逸一阶矩的条件混合要求会恢复已有块cut；一般可计算耦合/联合舍入仍缺。
