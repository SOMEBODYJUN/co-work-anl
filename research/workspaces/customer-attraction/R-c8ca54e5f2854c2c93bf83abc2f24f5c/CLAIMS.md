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
