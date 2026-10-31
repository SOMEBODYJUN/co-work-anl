# 一般真实多主题中继：本轮准确停止点

2026-10-24。对象为任意有限共同目录、任意人数、每份完整有序历史纯 SPE；Q-CAG-HALF 仍 OPEN。本轮没有获得新的一般承重不等式，没有主目标反例，不作状态提升。

## 精确候选及实际 IC 的接口

固定完整 SPE 的实际终局 z=(S_1,...,S_m)，福利 W。固定任意一个达到 OPT_m 的合法 m 元组 T=(T_1,...,T_m)，允许重复和空主题。令 Z_i(T_j) 是在实际有序前缀 S_{<i} 强制当前行动 T_j 后、以后全部沿原同一完整策略执行的真实终局。设

    V_ij = u_i(Z_i(T_j)).

本轮判别的候选是每个最优元组均满足

    (WA)  sum_(i,j) V_ij >= m(OPT_m-W).

它充分蕴含 half：真实根比较逐项给 V_ij<=u_i，故 sum V<=mW。(WA) 比此前已败的匹配遗漏收费弱；此前反例要求支付 |union(T)\cov(z)|，而此处只要求支付 OPT_m-W，后者还扣去实际覆盖在比较集外的客户。不能由那个旧反例宣称 (WA) 已败。

实际节点 IC 松弛的准确关系为

    e_i = u_i - (1/m)sum_j V_ij >=0,
    2W-OPT_m
      = [W-OPT_m+(1/m)sum_(i,j)V_ij] + sum_i e_i.

第一项非负正是 (WA)。这只是准确定位候选的既有真实行接口，不是新增通用符号关系。各 V_ij 已包含所有真实后继变化；未冻结后继。

## 一次定向攻击及边界修正

`attack_weak_average.py` 在四份已存完整策略锥上检验 (WA)：root_tax、同实例实际 BAAF 策略、34 客户 individual_security 策略、portfolio_matching 策略。每个锥允许全部非空兴趣类型自由取非负重数；保留全部有序历史的真实偏离行；W 归一为1；对每个含重复的 m 元组约束其覆盖不小于所有 m 元组的覆盖，再最小化

    sum V + mW - mOPT.

最终报告 `weak_average_attack.json` 的四个最小数值分别为 1、1、约1.55797101449、1。BAAF 初次仅检查互异元组时得到1.5，补齐重复元组后改为1，最终报告取补齐版本。这是输入边界修正，未生成新随机策略或继续阴性扩样。

这些是有限浮点诊断，不证明 (WA)，也未形成一般 IC 非负组合。若未来发现负点，仍须整数化并逐历史精确核验；脚本含 rational reconstruction 的初步检查，但本轮没有触发。

## 已读的相关既有边界

- `extreme_maximal_membership_floor.md`：极端关联的真实中继驻留证明；中间关联余项不能原样外推。
- `full_root_menu_mixed_obligations.md`：Mfull 及其 extra-one 充分归约，开放；固定势/无环/固定推送均不够。
- `cycle_threshold_obstruction.md`：只保留根低于全部后继的抽象菜单，即便固定增加静态槽数，仍不能支付安全值；必须使用更深后继的自身真实偏离。
- `recent_work_audit.md` 与 `common_customer_covariance_and_stationary_obstruction.md`：指定 stationary 全菜单列分布已被完整 SPE 否定，自由混合未被否定。
- `actual_marked_relay.md`：源根容量与真实剥离行成立，但不同终局客户测度的换标债不能仅靠主题流平衡消去。

停止点：没有推导出利用更深真实 IC 使 (WA) 第一括号非负的新关系。Mfull、真正聚合安全值和一般 half 均维持各自原来的 OPEN 状态。停止本轮采样，不把菜单恒等式或负债重命名计为进展。
