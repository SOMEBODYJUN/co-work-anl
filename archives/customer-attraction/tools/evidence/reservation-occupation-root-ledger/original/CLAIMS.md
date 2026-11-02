# 本轮个人命题账本

所有条目的共同模型是 CAG-MODEL：有限单位客户、有限非空共同目录、单位玩家、完整有序历史纯 SPE，空主题/重复/零客户/任意平局按每项明示范围处理。个人内部审查不等于外审或新颖性认证。主目标 Q-CAG-HALF 的对象、量词、结论均未改变，仍 OPEN。

## R22-DISJOINT-RESERVATION-LIFT-v1

* Exact statement / scope：任意旧 n≥2、任意旧完整 σ，其所有规定收益≥η>0。δ_T=min_S|T∩S|；正整数 J 满足 J/2≤η、J≥max_T(|T|−δ_T/2)、每个 |T|/2>J/n。加入 disjoint J 客户主题 B 和一名先行动者，则存在完整 SPE，根 B，B 后且没有额外 B 的每个旧有序历史逐字执行 σ。
* Objects / domain / assumptions / definitions：原共同模型；J 名新客户仅喜欢 B。严格第三条件排除旧空主题，仅为本引理条件。全文给出整数与共同放大约定。
* Conclusion：实际叶 (B,z_old)，新根利润 J，旧利润不变，W_new=W_old+J。
* Dependencies：有限逆向归纳；同叶均分；旧 σ 的全部真实 IC。
* Evidence：root 解析证明；direct 只收到陈述后的独立检查；old34/J19 的逐字保留版本验证全部新历史。
* Counterevidence / objections：没有未解决致命异议。最初 canonical 证书曾改旧并列行动，不能作为“逐字保留”的证书；已另存 literal 版本，原证书仍合法。
* Status：个人内部独立审查通过的条件性构造引理；没有普遍福利提升、外审或新颖性认证。
* Related files：parent/disjoint_reservation_lift.md；direct/review_disjoint_reservation_lift.md；direct/audit_disjoint_reservation_lift.py；direct/disjoint_reservation_literal_certificate.json。

## R22-POSITIVE-DEPTH-SECURITY-NO-v1

* Exact statement：存在四人、七主题、53单位客户和完整纯 SPE，使非首位 i=2 的 u_i<v_4(0)。这里 v_m=max_p min_(m−1合法静态竞争主题) E_p 查询收益，竞争主题不观察查询实现。
* Objects / domain / quantifiers：共同模型的合法有限见证；所有有序历史包括离轨历史逐项定义，没有限制平局。
* Assumptions / conclusion：见证实际 u=(19,29/3,67/6,67/6)，v_4=28481/2924，v_4−u_2=647/8772>0。因此“每个实例每个完整 SPE 每个 i≥2 有 u_i≥v_m”是 FALSE。
* Dependencies：旧34客户个体失败输入；不交保留构造；完整新策略及匹配静态原始/对偶证书。
* Evidence：security 的定义级 Fraction 审计；menu 不导入求解器的独立逐单位客户审计；direct literal 策略审计；root 实际重跑三者。
* Counterevidence / objections：不否定聚合桥。W=51、OPT=53、W−4v_4=8800/731>0、2W−OPT=49>0。
* Status：所述加强已被内部独立审查反驳；不是一般 half 反例，无最小性/外审/新颖性声明。
* Related files：security/positive_depth_floor_counterexample.md；security/positive_depth_floor_game.json；security/positive_depth_floor_certificate.json；menu/reservation_blind_review.md/.py/.json。

## R22-INTEGER-OCCUPATION-RESERVE-v1

* Exact statement / domain：任意固定有序前缀、任意完整形式计划、n≥1位单位后继及任意目录分布 p。K 是完整真实根完成叶的 extra-slot 矩阵，q 是 source A∼p 后真实后继的平均主题分布。G=pᵀKp，D=平均真实根偏离利润，V⁺=extra-slot 折扣后的尾利润。
* Assumptions / definitions：后继客户负载为非负整数，根 membership 为0/1；不要求计划本身为 SPE。全部符号、逐客户分母和非负分解见正文。
* Conclusion：nqᵀKp=V⁺+I，I≥0 且 I≥G−D；所以 G+V⁺≤D+nqᵀKp。若当前 IC 有效，进一步≤u+nqᵀKp。
* Dependencies：逐客户协方差恒等式、单位负载整数性、最后一步当前整行 IC。
* Evidence：relay 解析证明；root 独立重构；independent 盲推确认有序 pair 因子与分母；有限 Fraction 回归为实现检查。
* Counterevidence / objections：任意分数尾质量不在合同内；V⁺不能换成实际尾福利；该式不支付另一个 root-reset pᵀKq。
* Status：个人内部独立审查通过的通用组件，尚未接通一般 half，无外审/新颖性认证。
* Related files：relay/working.md §§8–9；parent/occupation_reserve_review.md；independent/occupation_reserve_review.md；relay/audit_two_block_pair.py。

## R22-STATIONARY-SUCCESSOR-SOURCE-NO-v1

* Exact statement：在任意合法节点令 P(T|A) 为强制 A 后真实后继的主题经验频率。候选“存在 Q≥0、ΣQ=1、PQ=Q 且 KQ≤u1”是 FALSE。
* Objects / domain / quantifiers / assumptions：共同模型，r≥2 的真实子 SPE，全目录查询；反例是既有八人两块完整策略，仅新增对该选分布规则的检验，不声称新底层实例。
* Conclusion：唯一 stationary Q 的 cap=2773/840>13/4=u，差43/840；自由 Mfull=851/280<u，W=OPT=32。
* Dependencies：旧策略 DAG 的完整边与 IC；有理线性代数及查询收益。
* Evidence：menu 和 independent 两路不导入求解器的全历史 DAG 核验、stationary 唯一性、自由 minimax 原始/对偶；root 重跑独立审计。
* Counterevidence / objections：只否定 occupation equality 的附加约束；不否定自由 Mfull/Mpath、局部同分布二次型或 half。
* Status：受限规则内部独立反驳；不是主目标反例，无外审/新颖性声明。
* Related files：menu/stationary_source_failure_and_free_source_interface.md；independent/stationary_source_review.md；independent/audit_stationary_source.py。

## 仍开放且未提升的候选

2Σ_i 全历史最低利润≥OPT；Σ_i最低利润≥m v_m；自由 Mpath≤W/m；全路径弱 extra-slot 同分布预算；G>u 时沿真实后继边际的 derivative>0。有限通过均不提升这些命题。逐 cross-pair 局部 cap 和一个更强 quantitative derivative 公式已在 relay/working.md 精确排除；没有将其失败扩大到所列弱候选。
