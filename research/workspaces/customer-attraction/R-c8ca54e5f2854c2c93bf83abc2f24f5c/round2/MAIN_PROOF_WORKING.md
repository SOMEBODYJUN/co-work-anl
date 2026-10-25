# 本轮一般证明工作稿

2026-10-25。精确目标仍Q-CAG-HALF，OPEN。固定任意原完整SPE实际B，W=覆盖=Σu_i，任意m主题比较并集O。欲证|O|−W≤W，保留L−E，不丢实际在O外的覆盖信用。所有分支都保全部有序历史和平局。

## 1. 已失效的旧逐人候选必须撤回

远端 [原零根保险反族](../../R-d3981c0168644971803a9c3380ed687c/round5_general/security/global_extra_individual_counterfamily.md) 给每个m的完整显式BASE/EXIT/PUNISH控制器：m个经济单元、m−1个两客户银行、所有坐标对均合法。root任意动作都重新锚定BASE，实际u1=m/(m−1)、W=2m、OPT=3m−2。

中间规定收益2+1/(m−1)>2；任何非规定行动若fresh银行会被真实末位复制，若used银行已经受分享，收益均≤2；其后EXIT每人可fresh独占得3，PUNISH除末位都fresh得3、末位复制过去目标得2，故所有子树真实最优。父方读原文后独立重构此证明，并另写控制器重放m3/m4全部有序节点，m5只算同一般公式与实际路径，不声称全树枚举m5。

因此原零根u_i≥δ_m从m≥3失败，extra u_i≥δ_(m+1)从m≥4失败，2m u_i≥OPT从m≥5失败。这里δ_(m+1)=本区上一阶段f_m(0)，所以“根实际f_m个体弱化”也已FALSE。旧PB任意背景例本来没有否定它，但现在有不同的真实零根反例；不能继续记OPEN。真正聚合与half不受反驳。

## 2. 父方直接尝试：净差而非逐人OPT地板

竞争的旧一般候选MIN-NET为OPT≤W+m min_i u_i。若真，min_i u_i≤W/m立即给half；它比half强，不能视为等价重述。原保险族没有否定它，而且(OPT−W)/(m u_min)=(m−2)(m−1)/m²趋1，说明若成立，统一系数m不能缩成固定κm、κ<1。这是旧族的解析必要性，不是新例或真值证据。

父方尝试从最小收益者的真实偏离支付净差。原保险机制中经济块价值a、银行b时，中间可信条件需b/2≥a(m−2)/(m−1)；仅调这两个大小无法产生更便宜的处罚或击穿MIN-NET。一般目录没有相同的银行坐标分解，因此该局部条件不能提升成一般付款。当前仍缺把各互斥偏离枝的处罚收益放进同一实际W的关系。

## 3. 匿名DR仍不足，必须保原均分结构

父方与independent分支从合同分别推导：对有限层Φ，令Ψ(v)=Φ(v)+L|v|−M binom(|v|,2)，M覆盖所有正局部二阶差（含重复动作），L使所有边际非负。减去Φ(∅)后Ψ非负、单调且DR；所有m槽终局和m−1槽竞争查询都同加D=L−M(m−1)。IC、完整SPE集合和AFC/安全聚合差不变。

故上阶段的匿名势反例可变成完整单调DR反例，仍非客户吸引实例。父方重新计算全部局部二阶差、单调边及终局平移，并由curvature只收合同盲重构。这个结果排除了“只补一般DR就能证明AFC”的推导域，没有反驳CAG-AFC或主目标。

原CAG还有更强约束：每个多重集的总边际利润恰等于其support对应的覆盖，重复同一主题不改变总福利；每个资源的同主题稀释精确为1/c。一般势的单调/DR不推出这些恒等关系。后续必须把它们真正接入资金，而不是仅换曲率术语。

## 4. 正在审查的更贴近原模型关系

jointflow已证明原R-only optional-common合同下的固定角色截面。记k层context t的未来负载为f_t(x)=|C_x(V_t)∩[k,m]|，原query-source alpha的owner为i、完整leaf负载c_alpha、strict-future coverer数q_alpha，则

    Σ_(role t=k)c_A_t(x)L_tx ≤ Σ_(role t=k)h_tx f_t(x)
       ≤ B_kx:=Σ_(alpha:owner<k,c_alpha>0)p_alphax q_alpha/c_alpha ≤1。

父方先从合同独立重构，以curvature随后盲推的权f_t替换固定query的目标交集权，得到上述全action强化。目标点的mandatory输出给c_A L≤h(1+common_future)≤h f；上游每节点各edge≤h/c_A，所有k前child各权≤1，至多一个k-child的f等于父reset叶≥k的coverer数，与前面child的角色不交，故每单位输入的截面报酬≤1。初始source逐边cap再给q_alpha/c_alpha。证明对任意完整policy成立，SPE仅在最后完整IC付款时使用。

原INIT source query本身覆盖x，因R没有实际prefix coverer，q_alpha=c_alpha−1，得到更强Σp(1−1/c_alpha)。广义source若query不覆盖x但tail覆盖，只能用q=c−eta，eta=0时不可误减1；c=0无边项取0。父方另写定义级审计，验证这一广义边界、旧7/6 prescribed density重入例及三种common角点；没有假称这些任意policy是SPE。

固定同一query后c_A一致，全部histories的current先合并再由一次实际prefix完整IC付款，补上了旧仅uniform角点的同query聚合。不同query仍须共享同一角色利润；逐客户Σ_a theta_kax≤1不蕴含Σ_a max_x theta_kax≤1。原INIT的d/H/J亦未免费纳入。这是全范围原流组件，不是ROLE可行性、一般half或m5半覆盖。

sharedload继续检验共享凸负载的同最优权付款，fullslots转向更弱全槽SUMmin。它们目前都没有新增无条件付款。m5压力在上述候选尚未证明时没有无条件half结论。
