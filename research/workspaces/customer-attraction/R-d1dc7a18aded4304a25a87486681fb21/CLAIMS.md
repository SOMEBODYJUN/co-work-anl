# 本轮精确身份与证据等级

2026-10-24。私人可恢复账本；不把本表列入等同于共享canonical提升。主目标完整量词始终不变；外审与新颖性均未认证。

## Q-CAG-HALF

任意有限单位客户N、有限非空共同目录S⊆2^N、任意m≥1、每个全部有序历史最优的纯SPE，福利覆盖W满足2W≥OPT_m。空主题、重复主题、零客户、任意历史平局全部保留。**OPEN**：本组无一般证明、无目标反例，无新增half已证输入范围。

## LAST-DIFFERENT-ACTION-LEDGER-v1

对象：任意原模型固定非负整数背景b、n≥1名尾玩家、完整suffix-SPE及任意合法B；假设实际路径存在最后非B行动T。k个先行动作的负载为p，之后r个B，k+1+r=n。

精确结论、四项定义与证明见[正文(5)](credible/last_non_B_rigidity.md)：δ_T=α_T−β_T=A_T+C_T+γ_T+ζ_T≥0。α使用T\B的分母b+1，β使用B\T的b+n；γ是该真实节点SPE差，ζ是该真实B孩子比逐客户最坏分母的余量。所有量词不限制目录/人数；不存在最后非B节点时不调用本式。内部解析独立重构，未支付跨节点共同W。

## STABLE-B-RESET-REALIZATION-v1

同一任意背景、任意n，另假设∀T α_T≤β_T，即n−1个B之后末位B全目录最佳。任意历史永远选B的同一policy是完整SPE。全部可实现有序尾终局a，精确等于逐i满足u_i(a)≥ΣB1/(b+p_i+n−i+1)的合法路径；有序prefix trigger以同一reset实现。首次尾玩家的全SPE最小收益精确为ΣB1/(b+n)。

同动作不触发是策略定义边界；充要条件及单B标量简化见[正文(6)–(7)](credible/last_non_B_rigidity.md)和[盲独审](independent_continue/stable_B_trigger_blind_review.md)。任意SPE最后非B在此假设下有两侧前缀0/k刚性；n≥2时其余尾玩家同额ε，旧背景返还另算。一般实例不自动存在该B，不能外推half。

## OPTIMAL-EXCHANGE-GENERATING-REPRESENTATION-v1

任意m最优索引元组O、任意s≤m合法主题列表、客户最优重数d和列表负载c，Bernoulli生成不等式及积分税核见[正文B/I/BH/NU/FL](exchange/bernoulli_optimal_exchange.md)。重复、空主题、零质量及端点按该页定义。源自旧E1/E2的非负组合，**不新增约束**；基本式已有[先读陈述的独立重构](security/bernoulli_exchange_blind_review.md)。锚点/非均匀式由作者和root解析核对，未冒称独审全部扩展。未支付真实枝外部利润的返还池及跨枝共同容量。

## 旧辅助反例的恢复，非新发现

固定α=(m−1)/m、g(T)=ΣT1/(1+αc)、M=maxg、G=Σ覆盖客户1/(1+αc)。旧13人36客户完整SPE有mM−W−G=29481/123025>0；α=1时同旧例差37/66>0。封闭自动机覆盖全部有序历史，root重放原审计112050项比较、menu用独立展开客户/转移实现重核。来源和复现见[menu README](menu/README.md)。只反驳实际负载税桥，不否定真正安全值聚合、LAST、Mpath或half。

旧route5a遗漏半额的错误推论已改为净需求OPT−W；旧通用relay v1保留FALSE，正确ΔW=ΔV+ΔP−Γ另列v2。与远端并发独立纠错安全合并，不认领先发。

## 仍开放的充分候选

LAST、自由Mpath、真正静态安全值聚合、KAPPA?共同价格预算均未在本组证明或否定。精确对象沿共享一般工作稿及本轮security/README恢复；旧证书/旧固定锥的阴性探针已停止，不作为候选真值证据。

## FULL-SPINE-INSURANCE-REPAIR-v1

任意原模型m≥2、任意合法有序终局a，只要求末位是该真实前缀后的最佳回复。对每个i<m及每个合法C（**包括C=A_i**）固定真正child-SPE η_(i,C)，记其中第i人的收益d_i(C)。任取有理g>0满足全部d_i(C)≤u_i(a)+g。

则加入不交保险块B大小m(m−1)g，以及T和m−2个Z各大小(m−1)g，并取全部Cartesian主题；同一末位平局租金可修复整条旧路径，首次任何坐标偏离后永久采用固定η与全B reset。用L统一复制旧客户并清分母，得到原单位客户模型的完整纯SPE，满足

    W_new=L[W_old+(m²−1)g],
    OPT_new=L[OPT_old+(m−1)(2m−1)g],
    OPT_new−2W_new=L[OPT_old−2W_old−3(m−1)g].

g=0时不添加塌缩的空保险标签，按旧路径和首次真旧偏离递归拼接即可。完整定义、量纲、全历史证明见[正文](credible_continue/shared_terminal_rent_compiler.md)；[先读陈述的独立解析审查](independent_continue/full_depth_insurance_compiler_blind_review.md)及root独立重构通过。作者标准库Fraction全树核验是固定实现证据，不承担一般量词。它不改善旧root-only的3Δ修复；没有找到OPT_old−2W_old>3(m−1)g的输入，未解决原half。

## TWO-REAL-CHILD-SLOT-DEFECT-v1

任意合法有序前缀a负载，其一个原真实孩子为T,C^r（r≥1）；同节点强制C后的真正r人child-SPE若存在最后非C动作Q，则原末位BR松弛η_Q及新孩子四税有

    K_(T,C)(Q)=η_Q+A'_Q+E'_Q+γ'_Q+ζ'_Q.

K的两池都使用原真实T,C^r叶中1/[c_x(c_x+1)]。精确集合与各项定义、边界和来源见[正文](budget/terminal_slot_defect_transfer.md)。root与独立子研究员按陈述重构通过。它确实连接两个真实孩子，但不支付旧背景总/逐人利润返还，也没有跨不同根枝共同W容量；文中局部反例不冒称根SPE或half反例。

## LAST-TERMINAL-QUERY-RESERVE-v1

任意原模型m≥2及完整SPE。倒二题B、其前负载d，实际末前b=d+1_B；M_b为LAST的真正单阻挡者minimax。任取对偶最优主题分布p，定义F=Σp_x/(b_x+1)、H(A)=Σ_(x∈A)p_x/[(b_x+1)(b_x+2)]、h=max_A H(A)，则

    M_b=F−h,
    u_m−M_b≥h,
    u_(m−1)−M_b≥H(B).

正文及直接逐客户证明见[末两人税池](security_continue/terminal_query_reserve.md)，root独立重构基本式通过。早期总亏损是否由该池、实际尾松弛或其他信用支付仍未解；不能把尾余量的下界倒用成其上界。
