# 本工作区精确命题与未闭合义务

研究对象严格为 CAG-MODEL；唯一主目标 Q-CAG-HALF 仍 **OPEN**。
这里是个人研究登记，不自动进入共享 canonical 账本。外审与世界新颖性均未认证。

## PRICE-QUERY-VERTICES-v1

- **Objects/domain/quantifiers：** 每个整数 p≥0、每组非负实重数 r_B（B⊆[p]）、每个 v≥0；C_r(z)=Σ_B r_B min(1,Σ_(a∈B)z_a)，B_r(v)=sup_(z≥0)[C_r(z)−vΣz]。
- **Exact conclusion：** B_r(v) 等于仅依赖 p 的有限有理集合 V_p 上的最大值。V_p 包含0，并包含每个正支撑大小 s 的满秩非空 0/1 行矩阵 A 所解 Ax=1、0<x≤1 的全部补零及坐标排列。
- **Dependencies：** 非负价格下坐标截断、有限超平面 arrangement 的线性 cell、活动等式满秩；不需 SPE 假设。
- **Evidence/status：** 自足任意 p 证明；另一研究员未读实现的数学重构通过。Bareiss 与独立 Fraction Gauss-Jordan 对3004系统一致，p≤4的集合有独立全枚举；p=5 的260顶点为发现者单路精确全枚举。固定16客户来源完整σ的两个加强价格目标各60份有理对偶已由root无优化器复跑通过。
- **Objections/scope：** 不保证多项式规模；不枚举全部σ。固定σ锥证明不能推广成所有策略；旧浮点非正LP不算精确上界。
- **Related files：** [正文](credible/fractional_price_query_reduction.md)、[独审](independent/fractional_price_vertex_audit.md)、[精确实现](credible/fractional_query_vertices.py)、[固定σ证书核验](credible/fixed_policy_price_certificate.py)。

## PRIVATE-CAPACITY-GUARD-v1

- **Objects/domain：** 任意本模型实例、任意m≥1、任意完整纯SPE；取非空G⊆S、λ>0及整数k_T≥1，a_T为T的全目录私有客户数。
- **Assumptions：** Σ_G k_T≥m；每T∈G有 a_T/k_T+(|T|−a_T)/m≥λ 且 |T|<(k_T+1)λ。
- **Exact conclusion：** 在每个合法有序非终局历史，当前玩家最终收益≥λ；若T的前缀次数已≥k_T，当前不会选T。特别W≥mλ。
- **Dependencies：** 全历史逆向归纳、未满容量鸽巢、真实偏离后的私有核份额、其余客户1/m保底。
- **Evidence/status：** 作者与recursion研究员逐量词独立解析重构，root检查未见致命异议；严格上界承担任意平局排除。
- **Scope：** 条件性保底；不声称一般实例存在此证书，也不自动给OPT≤2mλ。
- **Files：** [正文](global/heterogeneous_private_capacity_guard.md)、[独审](recursion/review_capacity_guard.md)。

## SMALL-OUTSIDER-CAPACITY-HALF-v1

- **Objects/quantifiers：** 任意本模型实例、每个完整纯SPE；取G、λ、k如上，a_T仅相对G私有，可被外部主题覆盖。
- **Assumptions：** Σ_G k_T≥m；每T∈G满足 a_T/k_T+(|T|−a_T)/m≥λ、|T|<(k_T+1)λ；每U∈S\G满足|U|<λ。
- **Exact conclusion：** 从每个只含G且未超容量的合法有序前缀起，原SPE剩余路径只用G且不超容量，每名剩余玩家≥λ；特别根W≥mλ。若另Σ_G k_T=m，则自动OPT_m<2mλ≤2W，**不要求G覆盖全部可覆盖客户**。
- **Dependencies：** 合规前缀逆向归纳；外部/超容量动作的当前收益无条件<λ，故不限制其离轨子树；对至多m个比较主题去重后按大小支付OPT。
- **Evidence/status：** 作者完整归纳、independent研究员盲重构及加强推论、root独立核对均通过；主稿接续合并加强中。
- **Scope/objections：** 不声称所有离轨前缀有λ保底；正λ与严格上界承重。外部大主题可污染相对私有核，仍无一般支付。
- **Files：** [主稿](global/small_outsider_capacity_half.md)、[独审及加强](independent/capacity_core_outside_audit.md)。

## NESTED-PREFIX-RECIPROCAL-TRANSPORT-v1

- **Objects/quantifiers：** 固定m≥2和任意完整纯SPE，任意合法嵌套有序历史H_k，0≤k≤m−1，r_k=m−k−1。任意合法主题对a,b（可空或相同）。令K_k(a,b)=f_(H_k)(b)+U_a(H_k+a+r_k b)，τ_k=Σ_x h_k/(h_k+1)。
- **Allowed operations：** 同层真实末位回复步(a,b)→(b,σ_m(H_k+b^r))；或原主题对不变地将k推进1。
- **Exact conclusion：** 任意有限此类运输从(s,a,b)到(t,c,d)满足K_s(a,b)≤K_t(c,d)+τ_t−τ_s。其差由真实末位BR slack及逐客户非负余项精确表示。
- **Dependencies：** 单位客户核K_x=(a∨b)/(h+1)+ab/(h+r+1)的对称性，以及背景增一/剩余clone减一的精确身份。
- **Evidence/status：** 作者逐客户证明；root和coupling2独立检查真实(7)→(8)定义一致；有限Fraction审计用于实现。独立全文审查尚在接续。
- **Obligations：** 多源必须满足每个被新前缀命中客户的加权pair-union容量≤1。尚无任意最优m主题组合的这种路由；单源终点吸收也不补足此缺口。不能增加幽灵玩家取得原游戏不存在的BR行。
- **Files：** [正文](coupling/nested_prefix_reciprocal_transport.md)、[审计](coupling/audit_nested_prefix_transport.py)。

## 原目标与独立开放桥

Q-CAG-HALF、真正W≥m v_m、自由分数背景FF-LEADER、弱逐人u_i≥OPT/(2m−1)、价格B(u_i)≤W、均值价格B(W/m)≤W及全终局税OPT≤W+Σc/(c+1)均未在本工作区闭合。
这些桥身份不同；任一个失败不自动否定主目标。自由分数背景定义与Fenchel切线已在R-077c0c…旧资产中存在，不作为本轮新理论。

最新同行 [唯一最优遗漏反例](../R-171cd7d518434f36a48cd50df29c9303/global/optimal_omission_exchange_counterexample.md)
有完整二人SPE、W35、OPT38、最优遗漏36；因此比较并集C的Σ_(x∈C)1/(c_x+1)≤W也是失败桥，不能仅去掉比较主题重叠后继续当候选。
