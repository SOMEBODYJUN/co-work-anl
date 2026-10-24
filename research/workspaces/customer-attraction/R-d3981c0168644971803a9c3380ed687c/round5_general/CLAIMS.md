# 第五次接续精确身份

原 Q-CAG-HALF 仍 OPEN。暂无新无条件一般福利下界或目标反例。

## R5-REFINED-ACTUAL-LAST-COMPARATOR

对任意原实例、任意人数 m≥1、任意完整有序历史纯 SPE，令 b 为实际前 m−1 位负载、L=v_2(b) 为实际完整额外槽菜单值、u=u_m。则

    OPT_m≤mL+τ(b)+E_Q t_b(A)≤mL+W−u/2

对任意最优菜单列 Q 成立；其中税还精确等于 W−u/2−D_old−e_Q/2−B_Q/2，三项非负。

状态：security 自足推导，capacity 独立逐客户检查通过，root 独立重构；既有覆盖收费/税代数的组合推论，无外审/新颖性认证。不含 mL≤W+u/2 的付款，所以未证明 half。出处及范围见 [正文](security/refined_actual_last_comparator.md)。

## R5-WEAK-LAST-PAYMENT

同对象下 mL≤W+u_m/2，或使用完整 TAX-EXACT 的更弱总税付款。

状态：**FALSE，完整 SPE 反例。** 下项给 k≥12 的真正原模型、全部有序历史反例。静态比较依然成立，原 half 依然 OPEN。

## R5-LAST-AND-ALL-COLUMN-TAX-NO

原共同目录加入 P 池的全参数完整 SPE：每个整数 k≥1，人数 m=k+3，客户 5k+23，六不同主题，实际 P^k012，收益 (5,…,5,5,6,12)。W=OPT_m=5k+23，真正末位完整菜单值 L=6。

强 LAST 差 mL−W=k−5；弱 LAST 差 mL−W−u_m/2=k−11。更自由的全列税优化也严格失败：

    min_Q [m max_T E_Q K_b(T,A)+τ(b)+E_Q t_b(A)]−2W
      =(2k²−41k−33)/(2(k+1)).

最优列唯一为核主题 2；该差对 k≥22 为正，k=22 时 33/46。有限列一行下界覆盖全部 Q，不依赖数值优化。

证明/审查：construction 自足全部历史控制器，capacity 独立解析审查，root 不导入控制器而从原始块第三次重构一般拼合及全部有限核比较。作者 k=12 的 count+mode 完整有限自动机审计通过 233340 项精确比较；不声称逐个遍历整个有序树。root 另核一般参数算式及 k=1,2,6,12,22 边界。无外审、新颖性或最小性认证。

范围：仅否定上述普遍充分桥。实际已经覆盖全部客户；静态背景核 234 加 k−1 个 P 给 v_m、δ_m≤5，W−5m=8，所以没有原目标或真正根安全值聚合反例。

文件：[构造](construction/padded_core_last_budget_counterexample.md)、[全列税证明](security/last_menu_retained_tax_failure.md)、[capacity 内审](capacity/padded_core_controller_review.md)、[root 独立重构](root/core_controller_independent_review.md)。

## R5-PRIVATE-ALIAS-AGGREGATE-TRANSFER

任意原 m 人实例及指定完整 SPE，D 为最大主题大小。每个经济主题加 L≥m 个别名，每别名 P>D 个独有单位客户。可按经济有序历史逐点提升原完整 SPE；所有理性后继选未用别名，经济主题仍可重复。每人收益加 P，福利加 mP，且

    P+δ_m(old)−P(m−1)/L≤δ_m(new)≤P+δ_m(old).

所以任何真正强聚合 δ 反例可用足够多别名保留；所有这些新实例本身都平凡满足 half。这是全输入转移/规范化，不含反例种子，也不保留较弱 (m−1/2)δ 或 ADM 量词。

状态：menu 自足证明，security 独立解析审查通过，接近既有 Cartesian padding 工具，不认领一般规范化或世界新颖性。[正文](menu/private_alias_aggregate_transfer.md)、[内审](security/independent_review_private_alias_transfer.md)。

## R5-ALIGNED-DELETION-SOCIAL-MARGINAL

在原实际前缀，使用同一真实查询 A 对齐各因果删除副本，删位收益之和精确等于 r·原收益减该玩家对剩余总利润的社会边际 q_i；任意背景修正及任意 h 的可对齐域另列。各位置共同查询行总权≤1 时，可用一份 Σq_i(actual)≤U（空背景为独占覆盖 E）支付其对齐 signed sum 及查询边际项。

状态：induction 一般逐客户代数及形式多项式检查，direct 独立核对通过，root 核对并纠正最初过去删位对齐范围。不含物理删后 SPE、正部 regret 或覆盖证书存在性。[正文](induction/aligned_deletion_social_marginal.md)、[内审](direct/review_aligned_deletion_social_marginal.md)。

## 其它分支

SC 保税、半固定过去算子、前缀交换、异质修复与因果删位的准确未证处见 [父方主稿](MAIN_PROOF_WORKING.md)及各分支 README。有限诊断和旧输入的新适用范围不自动算一般主线正向进展。

## R5-GLOBAL-EXTRA-FLOOR

任意原 m 人零根实例和完整 SPE 的每名实际玩家是否满足 u_i≥δ_(m+1)(0)？若真，静态 OPT_m≤2mδ_(m+1)(0) 推出 half。更弱的充分候选是每名实际玩家 2m·u_i≥OPT_m。

状态：**两者均 FALSE**，见下项原模型完整 SPE 家族。量词确为原全局人数 m、空根门槛，不是借用已失败的任意背景局部 δ_(r+1)(b)。此前七环静态 SAFE-ACTION 助手反例本身不满足末位 BR，不能否定本候选；现在的保险构造才是合法全历史证书。

精确别名转移把对手质量替换为 m 后，额外槽缺陷误差≤Pm/L；现在可以应用于下面的实际个体反例种子。它仍未产生强聚合缺陷，不能混同个体与总量。[准确转移](security/global_extra_fractional_alias_transfer.md)。

## R5-GLOBAL-INDIVIDUAL-FLOORS-NO

每个 m≥2 有原模型实例：m 个单位经济客户、m−1 个互不相交的两客户保险块，目录为全部经济/保险对，共 m(m−1) 个不同三客户主题。显式三模式完整历史纯 SPE 的实际收益为

    u_1=m/(m−1)，u_2=…=u_(m−1)=2+1/(m−1)，u_m=2。

W=2m、OPT_m=3m−2；真正优化自由分数门槛为

    δ_m=1+m/(2m−1)，δ_(m+1)=1/2+2(m−1)/(2m−1)。

因此原零根逐人 δ_m floor 对 m≥3 为假；全局额外槽逐人 δ_(m+1) floor 对 m≥4 为假；更弱的每人 2m·u_i≥OPT_m 对 m≥5 也为假。同一推导 m=5 给 u_1=5/4、OPT_5=13、W=10，OPT_5−10u_1=1/2；不是原 half 反例。

完整证明：NORMAL 锚定根经济行动，第一次中间偏离按保险是否已用转入 EXIT 或 PUNISH；两个后者在所有历史均显式可行、最优，不需 BI 黑箱。所有联合坐标偏离和末位平局均覆盖。direct 独立从单位定义重建一般证明，并完整核验 m=3 的 258 项、m=4 的 22620 项有序历史 IC；root 另独立重构三模式、分数最优值及参数多项式。无外审、新颖性或最小性认证。

范围：本族严格满足原 half；静态整数背景给 v_m≤2=W/m，且 W−mδ_m=m(m−1)/(2m−1)>0。不能写成真正聚合安全值或一般平均福利反例。

文件：[自足正文](security/global_extra_individual_counterfamily.md)、[direct 内审](direct/review_global_extra_individual_counterfamily.md)、[root 独立重构](root/global_extra_counterfamily_review.md)、[独立单位审计](direct/audit_global_extra_insurance.py)。
