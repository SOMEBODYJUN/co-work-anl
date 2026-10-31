# 本轮精确命题与审查状态

## IID-NASH-WELFARE-BRIDGE-NO

- Exact statement：存在CAG-MODEL的八名单位客户、四个不同共同主题、三位单位提供者及完整纯SPE，实际W=6，而静态对称iid混合Nash的唯一覆盖值Z_3=(4344−156√669)/49>6。因此全称W≥Z_m为假。
- Objects / domain：原共同有限目录、单位客户与提供者；Z_m按期望调和势最大者定义，非任意查询分布、非真实安全值。
- Quantifiers / assumptions：对全称福利桥给一个完整反例；所有有序离轨历史均已指定且最优。原一般Q-CAG-HALF保持量词及OPEN状态。
- Definitions / scope：原八客户CA-WORST-CCE-WELFARE-8实例；这里只抽取既有CCE结论的直接推论并给精确iid值，不宣称新实例或最小性。
- Dependencies：CAG-MODEL、CA-IID-SECURITY-BENCHMARK、CA-WORST-CCE-WELFARE-8。混合Nash是CCE可直接由逐玩家最佳回复定义推出。
- Evidence：作者自足代数与Q(√669)审计；根代理独立Q[s]/(7s²+23s−5)逐客户审计及审查。
- Counterevidence / objections：未发现fatal objection；本例真v_3=44/23且3v_3<6，故不反驳真正安全值支付。
- Status：完整有限反例推论，作者及根代理独立重构；外审、全球新颖性均未认证，个人资产尚未shared入库。
- Related files：security/iid_nash_bridge_boundary.md、security/iid_nash_bridge_audit.py、parent/iid_bridge_review.md、parent/audit_iid_bridge_independent.py、parent/iid_bridge_independent_audit.json。

## WEAK-IID-NASH-BRIDGE-NO

- Exact statement：原CAG-MODEL中，102不同共同主题的显式实例及完整纯SPE，对m=20和每个m≥41满足W<(1−1/(2m))Z_m。固定J100，客户数2m+100；实际W2m、OPT_m=2m+min(100,m−1)。
- Objects / domain / quantifiers：每个指定m取单位客户实例，构造一份全部有序历史上的SPE；反驳全称弱iid支付桥。Z_m是静态对称iid混合Nash的唯一覆盖值，不是真安全值。
- Assumptions / definitions / scope：A两客户、B的2(m−1)私有客户、100个A加单客户的Q_j，全部单位。允许所有原模型行动和离轨历史，策略分类只用于定义本例。
- Conclusion：弱iid桥亦为假；不改变原half或真正安全聚合桥。静态背景给v_m≤2，所以本族满足更强真正W≥m v_m。
- Dependencies：CAG-MODEL及Z_m静态定义；全历史最优性与Nash等式在正文自足重建。
- Evidence：作者全参数证明及定义级审计、父盲重构/有理阈值核对、credible研究员盲独审及另一份逐客户精确审计。
- Counterevidence / objections：未发现fatal objection；必须区别OPT与总客户数，也不声称v_m恰2。
- Status：完整解析反例族，三路内部重构；个人备份，尚无共享正式入库、外审或新颖性认证。
- Related files：security/weak_iid_bridge_counterexample.md、security/weak_iid_bridge_audit.py、parent/weak_iid_parent_review.md、credible/weak_iid_independent_review.md及审计。

## FIRST-CONTAINED-FOLLOWER-DP-NO-CONSTANT

- Exact statement：首次包含后继递归L是每个完整SPE当前收益的合法下界，逐路径最小总支付G亦合法；但m个不交孪生组、每组K共同客户与两个私有客户满足L(b,r)=K/r+1、G(0,m)=KH_m+m、OPT_m=m(K+1)。K=m时OPT/G无界。
- Objects / domain / quantifiers：原单位客户共同目录；所有m≥1、K≥1、所有合法计数前缀b，r=m−|b|。这是精确递归下界的障碍，不是SPE福利反例。
- Definitions / assumptions / scope：L/G的完整max-min递归见正文；只有精确U⊆T触发后继收益继承，无包含分支仍允许任意拥挤。
- Dependencies：同终局包含支配、全历史子博弈最优性及有限归纳；OPT由m个不交K+1主题精确达到。
- Evidence：作者全参数证明、credible分支独立重构精确公式与有限Fraction审计、父定义级检查。
- Objections：没有把G误认成真实终局福利；事实上该族所有完整SPE均完全有效率，已有结构结论不受影响。
- Status：完整解析方法障碍；独立审查支持，无外审/新颖性认证。更强myopic-ceiling递归及其一般half义务另立候选，不由本结果否定。
- Related files：independent/containment_copy_floor_boundary.md、independent/copy_protection_dp.py、independent/copy_floor_twins.py、credible/copy_floor_twin_review.md及审计。

## B2-STRICT-UNIQUE-SPE-STATIC-GAP-v1

- Exact statement：三人四主题十二单位客户的显式实例具有唯一完整纯SPE，全部21有序决策历史的指定行动均严格最优；其W11，而全部静态PNE均为ABC排列、W12=OPT_3。亦给十五非空兴趣类型全部正质量的1215单位客户版本：唯一SPE W1112，全部PNE W1214=OPT_3。
- Objects / domain / assumptions：原CAG-MODEL；共同目录四个不同覆盖；无外加tie规则或策略类限制，严格比较迫使策略逐层唯一。
- Quantifiers / definitions / scope：存在性反例，否定将所有无平局实例或唯一SPE实例归约到静态PNE/最差静态PNE福利支付的全称桥；不否定half。
- Dependencies：直接单位客户收益公式、全部真实历史逆向归纳及全部静态终局偏离。
- Evidence：作者自足表格及定义级标准库Fraction审计；父代理先按陈述独立重建84比较与64静态有序终局，结果相同；满支持版本亦由精确审计核对。
- Objections：严格性只针对每个真实节点行动比较及指定静态偏离，不声称所有不相关终局数值两两不同。
- Status：完整有限反例及明确扰动稳健性，内部两路重构；外审/新颖性未认证，个人备份尚未shared入库。
- Related files：global/strict_unique_spe_static_gap.md、global/audit_strict_static_gap.py/json。

## SEPARATED-MODULES-MAXIMUM-TOPIC-EFFICIENCY

- Exact statement：原CAG-MODEL中，目录主题各自完全位于某个两两不交客户模块；全部主题大小≤K，且至少m个不同模块各有一个大小K的目录主题。则每个完整历史纯SPE的每个玩家最终收益K，W=OPT_m=mK。
- Objects / domain / quantifiers：任意m≥1、有限单位客户、任意有限非空共同目录、任意全部历史纯SPE；K≥0，模块内部主题可以任意交叠、并集可以大于K，极大主题数无上界。
- Definitions / assumptions / scope：模块间客户不交，任何一个行动只占用一个模块；这是实质结构假设，不能外推到跨多个模块的主题。K0直接全零。
- Dependencies：任意前缀剩余r人时至少r个所述模块未被触及；全历史后继保底归纳；首次与所偏离K主题相交的后继其myopic上界严格小于K，和归纳保底矛盾。
- Evidence：作者一般归纳、父代理独立重构；规范集合值逆向归纳有限审计只核实现，不替代证明。
- Objections：模块内部不能直接识别为单资源；证明未使用该识别。任一主题大小上界及至少m个模块都不可遗漏。
- Status：完整条件性正面引理，内部两路重构，无外审或新颖性认证；一般half仍OPEN。
- Related files：independent/separated_modules_efficiency.md、independent/module_efficiency_audit.py/json。

## MYOPIC-CEILING-RELAXATION-HALF（开放候选）

- Exact obligation：对正文定义的全深度myopic-ceiling递归，是否所有原实例都满足G(0,m)≥OPT_m/2？
- Objects / assumptions / definitions：同原模型，H(b)按M_A(b)≥L(b)剪除行动，仍保留该行动子树的全部放松终局；不按当前玩家最终收益逐终局过滤，故弱于全集BI。
- Quantifiers / scope：任意m、共同有限目录；若上述全称组合不等式成立，即与合法W≥G桥合成一般half。只证明H包含真实SPE及L/G合法，不证明组合半界。
- Dependencies：有限逆向归纳及当前行动myopic上界；与首次包含DP不同，不由该DP孪生族障碍否定。
- Evidence / objections：有限精确回归与canonical求解器交叉；没有普遍half证书、也没有该新递归的精确坏族。高myopic但低最终收益的不可信行动仍可能被保留，这是当前主要攻击点。
- Status：候选OPEN，不将无反例样本升级为一般数学事实。
- Related files：independent/myopic_ceiling_dp.py、independent/myopic_ceiling_relaxation.md（待正文完成后以实际文件为准）、independent/README.md。
