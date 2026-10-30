# 精确状态与恢复索引

本工作区全部对象沿原CAG-MODEL：有限单位客户、共同有限非空目录、单位提供者、每份全有序历史纯SPE、全部平局。改变模型或量词者不称Q-CAG-HALF结果。通用目标仍OPEN；以下分别标级。每项详细Objects/Domain/Quantifiers/Assumptions/Definitions/Dependencies/Evidence/Objections位于相应自足正文。

| 身份 | 精确核心陈述与范围 | 状态、依赖、证据及异议 |
| --- | --- | --- |
| CA-EXTREME-MAXIMAL-THETA-v1 | k个包含极大覆盖中，每客户归属数∈{1,k−1,k}；任意合法背景b、任意r≥1、全部完整SPE中每个剩余玩家≥theta_r(b)。 | 已共享；发现者和独立研究员先分别重构，父方再逐式复核。一般中间归属不覆盖，无外审/新颖性认证。[正文](../../../current/customer_attraction/extreme_maximal_membership_floor.md)。 |
| CA-EXTREME-MAXIMAL-WELFARE-v1 | 同域内P_r≥rF_r/(2r−1)；空背景OPT_m≤c+(2−1/m)(W−c)，c为极大共同core。 | 已共享，依赖前项和整数逐客户静态代数。既有向日葵族给锐性，不称新下界。 |
| LOCAL-CREDIBLE-PRICE-LB-v1 | 真实阈值v^cred_r=max_A min_(SPE孩子)U_A；L_0=0,L_r=v^cred_r+min_A L_child。每个SPE利润≥L。 | 直接人数归纳。更强PRICE-HALF:F_r≤2L_r仍OPEN；惩罚/奖励孩子可不相容，有限菜单森林阴性不提升。[正文](induction/credible_threshold_path_credit.md)。 |
| LOCAL-TWO-THEME-REPAIR-v1 | m≥2的完整正深SPE计划，根缺口Delta；两独立保险行动笛卡尔成2p目录，以(m+1)Delta新增客户修复全SPE。 | 作者完整推导、父方阅读核对及独立数据重放；成本下界仅独立两主题保险模板。原聊天“总目录+2”构造未恢复。[正文](credible/two_theme_root_repair.md)。 |
| LOCAL-JOINT-COPY-OBSTRUCTION-v1 | 全k元子集目录、|N|=(m+1)k,k≥max(2,m−1)，联合q同标签copy预算为(k+1)H_m−1，OPT=mk且真实每个SPE均最优。 | 作者证明与父方解析重构；反驳该弱floor接口，不是SPE福利反例。[正文](global/joint_copy_floor_obstruction.md)。 |
| LOCAL-CONTAINMENT-RELAY-v1 | 给真实根菜单环A_i，选真实后继B_i⊆A_(i+1)；若下包含人数a_i、上包含人数c_j满足所有i≠j有a_i+c_j≥r，则Σd_i≥Σe_i逐客户成立。 | 作者与父方独立充分性复核；可排除最小extra-one坏例的合格环，未证明一般菜单存在此环。[正文](positivity/replicated_block_cycle.md)。 |
| LOCAL-AGGREGATE-DELETE-IDENTITY-v1 | 假较少人数聚合安全成立，选择保留tail权重并保持均值t+eta≥t，则P_r−rt=epsilon_*+kappa+eta+R−C。 | 精确代数和完整小SPE边界。PAY:C−R≤epsilon_*+kappa+eta仍OPEN，不把等价改写当证明。[正文](global/aggregate_tail_deletion_identity.md)。 |
| LOCAL-SIGNED-COMPLETION-v1 | 固定比较support P，先每主题一次，剩余重复次数最小化B或Q时，可全放到一个P成员。 | B的凹性、Q的线性直接引理；所有最优support的signed全局支付仍OPEN。[正文](signed/README.md)。 |

共同异议：有限SPE搜索、固定完整策略锥、内部多人赞同均不证明一般全称命题；一个致命异议足以阻止对应项提升。各代码/参数/种子/输出在所属正文明确，未认证全球新颖性。
