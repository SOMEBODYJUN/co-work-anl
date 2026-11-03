# 本轮精确研究账本（个人资产，非共享状态提升）

主目标Q-CAG-HALF仍OPEN。对象统一采用仓库CAG-MODEL：有限单位客户、共同有限非空目录、单位提供者、每个完整有序历史上的纯SPE，允许空主题、重复、零客户及任意历史依赖平局。以下辅助身份不改变主目标的对象或量词。

## B2-TERMINAL-RESPONDER-EXCHANGE-v1

- Exact statement：实际路径(C_1,...,C_k,D)，m=k+1>=2，各主题两两不交。固定i<=k及合法T；若原策略在i改T后的其余早期玩家确实仍选各自原主题、末位真实回复R，令U为实际覆盖集合，则
  `3|Ci|/2−[|T\U|+|T∩Ci|+|T∩(U\Ci)|/2] = g_i+g_R+g_D+|Ci\R|/2 >=0`。
- Objects/domain/quantifiers：上述原完整SPE的任意指定i,T；不限人数、目录；仅指定真实分支满足响应条件，其余历史自由但仍需原SPE。
- Definitions：g_i为早期实际收益减真实偏离收益，g_R为离轨末位真回复相对D的收益差，g_D为实际末位D相对合法R的收益差。
- Conclusion/scope：三个真实节点的非负交换证书；不能去掉响应条件。
- Dependencies：CAG-MODEL，实际主题不交，给定真实分支的早期行动保持事实。
- Evidence：正文解析恒等式；16个全部客户会员分支Fraction实现核对。父独立定义推导，global只见定理陈述后盲重构，再逐稿核对。
- Objections：未消除fatal objection无；W集合/标量记号须拆开。一般响应已另立有符号缺口版本，非直接外推。
- Status：完整解析证明与两路内部重构；未认证外审、新颖性或常数最优。
- Files：[正文](credible/terminal_responder_exchange.md)、[父审查](parent_tail/terminal_responder_parent_review.md)、[盲审](global/terminal_responder_independent_review.md)、[审计](credible/audit_terminal_responder_exchange.py)。

## B2-SINGLE-TERMINAL-RESPONSE-HALF-v1

- Exact statement：在上一对象下，若存在一个达到OPT_m的m元组(T_1,...,T_m)，使全部i<=k,j<=m的真实i→T_j分支均保持其他早期主题，则
  `OPT_m <= [(8k²+11k+4)/(4(k+1)²)] W < 2W`（后者限W>0）；W=0时OPT=0。
- Domain/quantifiers：任意k>=1、原共同目录、每个满足该存在性条件的完整历史纯SPE。最优元组可重复；不改为每个元组满足条件。
- Dependencies：上一交换证书、实际末位BR、非负并集收费及显式凸合。真实两预算为`OPT<=(2+1/k)P+L/2`及`OPT<=P/2+(k+1)L`。
- Evidence/status/objections：解析全参数凸合，父与global独立重构相同系数，100个k有限实现检查不承担任意k量词。未见未消除fatal objection；强响应条件承重，不声称一般无拥挤half或锐常数；外审/新颖性未认证。
- Files：同上一正文§3及两份审查。

## B2-COLLISION-FREE-RESPONSE-DEFECT-v1

- Exact statement：保留实际两两不交路径，取消其他早期行动保持条件。任意i,T，p为其他实际早期负载，h'为真实偏离后的其他早期负载，t,r,d为T/真实末位R/实际末位D会员。令`F(h)=(r−t)/(h+t+r)−d/(h+t+1)`（r=t时首项取0），`Delta_iT=Σ_x[F(h')−F(p)]`。上一交换identity右端须减Delta_iT。对任意最优m元组，Delta_tot=Σ_i,j Delta_i,Tj，有
  `OPT_m <= beta_k W + [(2k+1)/(2(k+1)^2)] Delta_tot`。
- Domain/quantifiers：任意完整SPE，其实际路径不交；任意合法i,T及任意最优m元组。Delta有符号；没有假设或证明其普遍非负。
- Dependencies：原三个真实节点slack及逐客户收益的精确背景错配。
- Evidence/status：父首先推导，credible从原收益独立重构，全会员与负载有限Fraction审计；解析接口，未闭合一般支付，不认证外审/新颖性。
- Counterevidence：下条否定Delta_tot<=C W的任意统一常数预算。接口本身仍成立。
- Files：[正文](credible/response_defect.md)、[审计](credible/audit_response_defect.py)。

## B2-UNIFORM-RESPONSE-DEFECT-BUDGET-NO-v1

- Exact statement：对每个整数k>=2，已有3/2无拥挤族的同一目录和客户可选择完整纯SPE，实际C_1,...,C_k,D，m=k+1，W=2k+2，OPT=3k+2；对指定最优元组(A_1,...,A_k,D)，上条Delta_tot=k(k−1)/2。因此Delta_tot/W→∞。不存在与人数和实例无关的有限常数C，能对每个实际无拥挤完整SPE及每个最优m元组保证Delta_tot<=C W。
- Definitions/assumptions：X_i两客户、a_i单客户、公共b,d；A_i=X_i∪{a_i},B_i=X_i∪{b},C_i=X_i,D={b,d}。对一步偏离至已触及旧A_j或D，全部剩余玩家各取一次fresh A，i<k时末位组不同于i。其余按原Q/B归纳粘合。
- Scope：否定全查询统一缺口预算，不否定有选择/有权查询，不反驳half；本族OPT/W<3/2。
- Dependencies：已审CA-COLLISION-FREE-FAMILY-3-2完整Q/B构造；达到主题最大大小3的fresh A子SPE及有序first-deviation子树不交。
- Evidence：任意k完整SPE符号粘合，逐查询Delta表解析证明；k2..20单位客户Fraction核对仅实现检查。父重构粘合与核函数，global独立攻击后写审查。
- Objections/status：无未消除fatal objection；完整证明与内部独立检查，外审/新颖性未认证。未把query-only审计冒充全部有序历史验证。
- Files：[正文](credible/response_defect_budget_obstruction.md)、[独审](global/response_defect_independent_review.md)、[审计](credible/audit_response_defect.py)及同名json。

## 其他个人工具的准确层级

- `customer_coupling/anchored_cut_lift.md`：固定m共同客户矩锥的精确Boolean二次化/锚定cut锥零面表示；父已核对AND罚、偶m可逆、奇m投影及显式正罚，不含一般half乘子。详细CL-1/2/3精确身份在该稿。标准思想在本对象的自足实现，不认证新颖性。
- `security/high_background_reduction.md`：静态整数安全值与分数背景值的Jensen方差误差界、合法大背景的二阶矩阵归约及严格余量提升。父已独立核对(1)−(7)，指出并已由作者修正probe标度说明；不是一般leader或聚合安全证明。
- `parent_tail/probe_three_tail_price.py`与early_opportunity各探针：有限模板和完整指定策略锥计算，仅记录实际范围。所有浮点不可行/无正缺口均不改变数学目标状态。
