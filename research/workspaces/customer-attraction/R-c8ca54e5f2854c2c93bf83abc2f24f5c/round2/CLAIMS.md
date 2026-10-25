# 本轮精确身份

2026-10-25；个人研究账本，非共享canonical状态提升。

## Q-CAG-HALF

原单位客户、有限非空共同目录、任意m、每份全部有序历史纯SPE、任意平局/空重复/零客户的2W≥OPT_m。状态OPEN。没有一般证明或目标反例。

## FINITE-ANONYMOUS-DR-COMPLETION-v1

Exact statement / Domain：任意非空有限行动集A、m≥1及0至m层匿名实势Φ。先减Φ(∅)，取M≥全部含重复局部正二阶差，L≥max[M|v|−Δ_aΦ(v)]。Ψ=Φ+L|v|−M binom(|v|,2)非负、单调DR；所有m人终局及m−1竞争槽query同加D=L−M(m−1)。
Quantifiers / Conclusion：所有终局、角色、有序历史和偏离；完整SPE集合完全保持，固定m的AFC和真正静态安全聚合缺口不变。
Scope：更大的匿名势博弈类，不生成CAG；不适用于保留m竞争槽、向m+1层插入的SUMmin相同缺口结论。
Dependencies：有限二阶差上界、人数项边际、共同常数不变性。
Evidence：independent自足证明，父方先只见合同重构及另写精确核验，curvature合同盲审；原C22全历史身份继承/重述并审计。m1、重复、零二阶集已处理。
Status：内部已核对一般变换和方法域反例；外审/新颖性未认证。没有新增CAG付款。
Files：independent/concavification_theorem.md；curvature/blind_cardinality_dr_review.md；parent/audit_concavification.py/json。

## OLD-ROOT-INDIVIDUAL-FLOORS（状态纠正，非新反例）

Exact statements：原零根每个完整SPE每人u_i≥δ_m；u_i≥δ_(m+1)=f_m(0)；u_i≥OPT_m/(2m)。
Status：均FALSE，peer全m单位客户保险族分别从m≥3、4、5严格否定。原模型量词完整，不是PB背景版本的外推。
Evidence：peer自足一般参数策略/独审；父方读原文后独立重构模式，另写m3/m4全有序历史核验及m5同公式算术。旧来源归属不认领首次。
Counterboundary：不否定W≥mδ、W≥mv或Q-CAG-HALF；MIN-NET仍未证未反驳。
Files：MAIN_PROOF_WORKING.md §1及parent/audit_root_floor_correction.py/json；peer原始路径在正文。

## R-OPTIONAL-FUTURE-LAYER-v1

Exact statement：在既有R-only严格future自然reset流、任意optional-common选择及广义query-source逐边cap下，固定任意角色k和实际未覆盖客户x，有Σ_(role t=k)c_A_t(x)L_tx≤Σ_(role t=k)h_tx |C_x(V_t)∩[k,m]|≤Σ_(source owner<k)p_alphax q_alphax/c_alphax≤1。q为source叶owner严格未来coverer数，c=0无边贡献0。
Objects/Domain/Quantifiers：任意有限原单位客户/共同目录/人数、每份完整纯policy（流本身不需SPE）、任意同合同源库存Σp≤1和可行optional路由；不同有序histories不合并，节点可多入口。
Assumptions：R不被实际B覆盖；source及reset来自同一policy真实完成叶；初始future边≤p/c_W；自然新coverer边强制h/c_A、共同coverer边在[0,h/c_A]；全部边strict future。
Conclusion：全action未来负载密度和及normalized current有一份源券；同action固定query的全部history current可先合并再用一次actual-prefix完整IC付款（此最后一步才需SPE）。原INIT source query覆盖x时q=c−1，得更强source扣减。
Scope/Objections：不是旧Σ c_Vh≤1；不含原初始d/H/J；不同action的整行系数总量仍未付。广义query不cover x时强式1−1/c错误，已改q/c或eta版本。无新ROLE/half结论。
Dependencies：旧NEW-CAP及R-FLOW合同、有限DAG截面守恒；旧uniform捕获流仅为角点。
Evidence/Status：jointflow解析；父方只见合同重构；curvature盲审和更强未来负载权精化；作者及父方各自定义级Fraction实现。内部已核对，未认证外审或新颖性。
Files：jointflow/same_query_history_aggregation.md；curvature/blind_optional_jointflow_section_review.md；parent/audit_layer_current_parent.py/json；作者audit_layer_current.py/json。
