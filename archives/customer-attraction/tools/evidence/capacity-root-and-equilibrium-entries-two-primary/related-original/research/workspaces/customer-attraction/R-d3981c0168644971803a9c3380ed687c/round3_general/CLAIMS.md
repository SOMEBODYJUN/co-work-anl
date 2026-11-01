# 本轮精确身份

Q-CAG-HALF：原模型、任意人数与共同目录、全部完整历史纯SPE，仍OPEN；本轮无新全输入福利下界或目标反例。

## LOCAL-COPY-HALF-AND-PAYOFF-RATIO-NO-v1

- **Refuted quantifiers：** 对每个原实例、每份完整SPE、每个实际j<l，强制l复制B_j后的原真实续局收益≥u_j(B)/2；以及原实际u_j(B)≤2u_l(B)。
- **Witness：** 三人、五个不同共同主题，六不交单位客户块(6,12,8,2,2,5)，共35；实际A,E,D，收益(18,8,9)，强制第二A后的真实叶A,A,F1，复制者8<9。
- **Full-history proof：** 固定A的整个二人孩子五行动收益皆8，末位回复逐行最优；其余四个根孩子任取完整BI。根A独占18且为唯一最大主题大小，严格最优。实际W=OPT=35。
- **Evidence：** exchange解析正文、作者完整审计、子分支先只读原始块的独立审查、root另一次单位展开与155项完整比较均通过。内部审查；无外审或全球新颖性认证。
- **Scope：** 实际A∩E为空，故不反驳带交集支持的prefix请求cap2；也不反驳STATIC-2或half。没有优化本族常数。
- **Files：** [正文](exchange/copy2_counterexample.md)、[独立报告](exchange/copy2_independent_review.md)、[root审计](root/audit_copy_half.py)。

## LOCAL-ALL-P-FRACTIONAL-JENSEN-PAYMENT-NO-v1

- **Refuted quantifiers：** 每个原实例、每份完整SPE、每个合法主题分布p，位置i强制A并保留真实后继后删当前，μ_ix=E_A c_x(B_i(A))、F_i(p)=Σ_xp_x/(1+μ_ix)总有Σ_iF_i(p)≤W。
- **Witness：** 三人、六不同共同主题、817单位客户，完整43节点策略，p_2=p_5=1/2；u=(197,200,200)、W=597、OPT=710；F=(1016/5,11827/60,200)，ΣF−W=199/60>0。
- **Evidence：** 一个既有完整形式策略锥的单次定向发现；作者定义级单位展开与direct独立实现均核258项全历史比较通过。root重跑独立实现并核范围。证明依赖精确witness，不依赖浮点求解器最优性。
- **Unrefuted scope certified：** 固定竞争(0,2)六查询cap199，所以v_3≤199=W/3；坏p对偶值≤275/2<142≤δ_3，也非v最优p。因此未反驳δ最优p付款、W≥mδ、真正聚合安全值或half。
- **Status：** 精确辅助反例，独立内部审查通过；无外审、最小性或全球新颖性声明。
- **Files：** [正文](equilibrium/fractional_global_payment_boundary.md)、[原始输入](equilibrium/fractional_global_raw.json)、[独立报告](direct/review_jensen_candidate_counterexample.md)。

## LOCAL-STATIC-2-CANDIDATE-v1

- **Statement：** 任意原完整SPE实际B，对每个i,T有u_i(T,B_−i)≤2u_i(B)。
- **Conditional use：** 标准逐客户静态比较会给OPT≤3W，仅是一般弱中间界，不是half或本轮已证常数。
- **Status：** OPEN；没有本轮证明或反例。旧输入及三份固定策略锥的有限阴性不能提升状态，未作精确整锥对偶认证。
- **Unpaid：** 原IC只给真实D_i(T)≤u_i；多尾响应税的共同上界仍缺。
- **File：** [准确攻击记录](direct/static_approximation_attack.md)。
