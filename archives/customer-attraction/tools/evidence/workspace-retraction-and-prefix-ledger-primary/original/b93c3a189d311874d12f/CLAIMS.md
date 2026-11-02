# 精确命题与证据等级

2026-10-24，个人研究账本，不自动升级共享canonical。

## Q-CAG-HALF

Objects/Domain：有限单位客户N、有限非空共同S⊆2^N、任意整数m≥1，固定顺序观察全部有序历史选题；空/重复/任意平局均含内。收益Σ1/c_x。
Quantifiers/Conclusion：每份完整纯SPE的根终局2W≥OPT_m，含零客户。
Status：OPEN；本轮没有一般证明、目标反例或新无条件福利界。
Files：GENERAL_WORKING.md、共享model.md和一般证明工作稿。

## ATOM-RETRACTION-v1

Exact statement：固定正文§1同一真实合法流，逐初始客户边完整拆标签，§2回撤式成立；存在共同cap成功回撤 iff §3全部λ≥0 cuts成立。
Objects/Assumptions：有限future DAG、同质mandatory/common约束、A固定、F=A+ΣK逐角色全额追踪；零边不除零，未追踪固定余流必须另加。
Scope/Conclusion：扩展终局付款合同下的条件线性修复；新初始d可能超过旧u。不保证任意SPE都能成功修复。
Dependencies：旧joint certificate/来源回撤、有限维凸分离。
Evidence：作者解析、independent合同盲重构、父方第三重构与定义级回放。转述未明全追踪的警点已由正文澄清。
Status：内部已审条件工具；无外审/全球新颖性认证。
Files：common_capacity/atom_retraction_and_dispersion_rebate.md；independent/routing_blind_review.md；parent/stage_one_review.md。

## DISPERSION-REBATE-v1

任意上述合同、任意非负λ，按质量加权owner合并的价格需求减逐边需求，精确为Σ_i min(D_i,E_i)。依赖正部恒等式，三方重构与有理审计通过。抽象三角数据证明线性修复类严格包含，不称SPE数据。λ恒1返还零，原half总资金未付。状态：内部已审有限维工具，非新IC付款关系。

## FRACTIONAL-ARBITRARY-BACKGROUND-FLOOR-v1

Exact candidate：任意原合法有序前缀b、任意余r人及其每份完整子SPE，当前u≥f_r(b)，f_r用r个分数竞争槽定义。
Status：FALSE；既有PB-extra构造的直接推论，不是新反例族或重做全树证明。固定查询对全部分数q仍有Jensen下界f_r(b)≥s>u，父方独立算术复核。
Scope/Counterboundary：背景全覆盖且可能离轨；不反驳根实际/聚合弱版、2m u_i≥OPT_m或half。
Files：potential_dual/fractional_background_floor_corollary.md；parent/audit_fractional_background.py/json；来源R-cd789.../round5/menu/pair_attack.md。

## AFC-CAG-v0

Exact statement：固定任意原CAG-MODEL输入及每份完整有序历史纯SPEσ，实际B、W；z_i(A)为在原实际前缀强制A后执行同一σ所得叶，v_i(A)只删当前槽。对每个合法查询分布p，是否有Σ_i min_A G_p(v_i(A))≤W，G为对独立查询的均分插入收益。
Scope：任意m、目录、客户、平局；与Mfull额外一槽及原分布直接推送不同。列可依位置/p选，但必须来自同一σ。
Conclusion if true：有限minimax给W≥m v_m，静态安全界给OPT_m≤(2−1/m)W。m5的9/5只是条件后果。
Status：OPEN。纯查询由真实IC直接支付；混合查询循环流未付。
Evidence：一份固定旧policy/固定p的12项80坐标势证书；该旧36客户实例全p原始=对偶164/5<W34。父方定义级独立重构。均不支持一般真值提升。
Related files：aggregate_security/aggregate_free_column_candidate.md；parent/free_column_balance.md；parent/audit_free_column_certificate.py/json；fresh_menu_attack/contract.md。

## AFC-ANON-POTENTIAL-v0

Exact stronger statement：将AFC对象改成任意有限共同动作集、匿名边际势收益u_i(z)=F_m(z)−F_(m−1)(z\i)的完整纯SPE，要求同一聚合自由列付款。即使加收益非负及各层势单调，结论仍FALSE。
Counterexample：m=3、22循环标签，F3无相邻对为11否则0，F2同标签10、相邻−1、其他为均匀插入F3均值；加11常数到每人收益。完整策略和自足证明见正文。实际总效用25，自由列最小值(11,11,12)和34；uniform静态安全值≥11。各层非负单调扩展存在，但DR失败。
Scope：不是客户均分实例，不是原half或CAG-AFC反例；不得称总效用25为覆盖福利。
Evidence/Status：作者解析；父方未读稿独立重构；另写脚本核507有序节点11154项行动比较及全部终局非负/DR违例。内部已审方法边界，无外审或全球新颖性认证。
Files：fresh_analytic/anonymous_potential_boundary.md；parent/audit_anonymous_potential.py/json。

## AFC-FULL-MENU-ENVELOPE-v1

Exact statement：固定任意CAG实例和有理p，正文E/F/R/H递推精确给出所有完整历史纯SPE的AFC最大gap；离轨孩子各自按当前cap选最大查询终局，actual列固定目标B，再优化到B的实际顺序。
Assumptions/Dependencies：有限原目录/人数；canonical集合值SPE全集；不同完整有序子树独立拼合，计数仅缓存可实现集合。
Conclusion/Scope：通用有限反例oracle，不声称多项式复杂度或右端总非正，不另开逐n项目。
Evidence：作者自足证明、父方独立重构拼合；七项独立完整策略穷举和空零/平局边界回放一致。
Status：内部核对的候选攻击工具；非新IC资金。Files：fresh_menu_attack/contract.md、full_menu.py、verify_oracle.py、oracle_audit.jsonl。

## SHARE-DELETION-AVERAGE-CLOSURE-v0

Exact candidate：固定原完整SPE的m槽实际叶，删除玩家i且其覆盖客户价值乘(c−1)/c，记减少人数游戏最坏SPE福利L_i；是否Σ_iL_i≤(m−1)W。
Status：FALSE；同一已存individual_security_failure输入有W32、L=(125/6,125/6,70/3)，总65>64。合理清分母为单位客户游戏。删除首位/最小收益者保实际叶的更强闭包也FALSE。
Evidence：independent探索、父方另写精确代码重构原与各删后全历史证书；没有新原目标反例。
Files：independent/general_reconstruction.md；parent/audit_share_deletion.py/json。

## PAIR-INSURANCE-SOURCE-STOP-v1

Exact statement：对正文明确的旧k组pair/reservoir目录和非SPE目标C1...Ck,D，每个整数k≥4的异质保险表达式2Σδ+maxδ严格超过旧差额k−8。
Mechanism/Dependencies：正常前缀剩n人且k≥2n时，全有序历史逆归纳给真正fresh-pair可信值至少8；最后floor(k/2)−1位δ≥6。仅比较既有保险表达式，不声称所有修补成本下界。
Evidence/Status：作者一般解析；新研究员先盲重构再对稿；父方第三重构及奇偶算术回归。内部已审，未解决一般half。
Files：credible_construction/pair_reservoir_candidate_stop.md；fresh_credible_review/blind_review.md、manuscript_comparison.md。
