# Boss5本轮精确Claim与开放义务

模型统一为CAG-MODEL：有限单位客户、共同有限非空目录、单位提供者、任意m≥1，全部有序历史依赖纯SPE、全部离轨历史与任意平局。主目标Q-CAG-HALF **OPEN**。除具体反例外不设人数或目录上界；改变范围另立身份。个人备份不自动进入共享canonical，无外审/新颖性认证。

## B5-TRUE-EXCHANGE-v1

- Exact statement：固定任意完整策略、同客户前缀负载的真实历史h/h'、同一标记incidence a，R_a(h')−R_a(h)=L_a(h)−L_a(h')。λ全行权的多边和精确等于Σ_v,x d_v(x)/(ρ+c_v(x))；逐incidence守恒足以抵消，标量权守恒不够。
- Objects/domain/assumptions：任意有限模型及标记a≥0；ρ>0，或ρ0且标记正支持原前缀负载正。不要求SPE，真正应用时须保留全历史节点。
- Conclusion/scope：两分支clock表示及合法终局层归并；不构造一般非负BR乘子。
- Dependencies/evidence：倒数差望远镜、有限求和；父方独立重构，774项实现检查。三人五客户完整SPE实际BAC/交换ABA否定无残差和根路径clock支付。
- Counterevidence/status/files：未发现identity漏洞；一般支付仍缺。clock/signed_history_exchange.md、clock/attack/、parent/clock_exchange_review.md。

## B5-RELAY-PROJECTION-v1 / B5-RELAY-SPE-NONINJECTIVE-v1

- Exact statement：对同一非负比较组合z总重τ≥1，净δ−s完全消去真实中继D；保留S/Z/E/F后的Debt满足Debt−threshold=m(C(z)−2W)+ΣK，K≥0。两个3人8客户完整SPE可有同一最少最优z、同实际路径/全部末回复边际，但不同中继负载、D和离轨福利。
- Objects/domain/definitions：任意m和原完整SPE；δ/s/Z/E/F/K定义固定于relay/projected_relay_debt.md；反例单独限制3人。
- Conclusion/scope：刻画投影信息丢失及强充分式与half的差距；不证明投影无法间接受SPE约束，不否定一般half。
- Dependencies/evidence：旧真实菜单identity与标量包络；root独立代数重构、两策略各39比较Fraction验证。
- Counterevidence/status/files：identity内部核验通过；普遍净支付仍OPEN。relay/CLAIMS.md、relay/projected_relay_debt.md、parent/relay_kernel_review.md。

## B5-CLONE-DRIFT-UNBOUNDED-v1

- Exact statement：任意q≥1，两个互斥单客户主题、m=2q，任意完整SPE根终局q/q，W=OPT2。唯一最少最优组合A+B的两条强制克隆ray均有Drift=H_q+H_(q−1)−H_(2q−1)，CloneSlack=2H_q−H_(2q)，CloneSlack−Drift=1/(2q)；分别无界。因此不存在固定K对这套未配对跨角色差给≤KW的一般预算。
- Definitions/quantifiers/scope：所有完整有序历史SPE；具体ray/跨实际位置聚合固定于正文，不排除先保留二者抵销的预算，不排除m相关阈值。
- Dependencies/evidence：方盒/过载的剩余人数归纳、调和求和；root独立重构通过。
- Counterevidence/status/files：无致命异议；一般净运输OPEN。relay/clone_drift_unbounded_family.md及algebra/clone_chain_identity_and_boundary.md。

## B5-SINGLE-KERNEL-JOINT-v1

- Exact statement：任意实际路径、任意m个有序比较主题，单核删除过程满足F=W+χ+D−A；R+P_hat=χ≤W，χ_x=1−1/(c_x+1−z*_x)在比较并集上、其他客户取0。A=S+B+C+O/m≥0（S仅全行非负），D有符号。且χ=F−V_last，D−A=V_last−W。
- Objects/domain/assumptions：任意m原完整SPE；比较可重复/空，不必最优；K、P_hat、last-source精确定义见正文。全行乘子事先固定1，客户整理在后。
- Conclusion/scope：joint实际clock不重计首次hit；净式本身不证明half。强D≤A包括存在最优组合/排列版已被旧14客户完整SPE排除；R_add≤W又被旧71客户例排除。
- Dependencies/evidence：逐客户倒数差、真实SPE原行；896系数检查和四完整策略重放，独立代数/父方/clock交叉审查。
- Counterevidence/status/files：identity内部通过；D≤A+(W−χ)仍OPEN且与half等价。kernel/single_kernel_chronological_budget.md、clock/kernel_interface_review.md、parent/relay_kernel_review.md。

## B5-PAIR-EXTRA-ONE-NO-v1

- Exact statement：不成立“所有原SPE、所有根查询A/B，(f_A(Z(B))+f_B(Z(A)))/2≤u_root”，f分母为额外插入1+c。
- Objects/domain/evidence：既有13人36客户完整SPE的根u5/2，查询T/P给29/11，超3/22；从原DAG真实边重建，112050比较Fraction核验。具体有限反例即可排除全称强桥。
- Scope/status：仅pairwise加强失败。同例完整WP最大1423/605、菜单minimax25/11、自由13槽值9925/4586均小于u；匹配有理证书和全列核验。不否定一般WP/菜单/自由extra-one，不证明它们。
- Dependencies/files：固定源packet，relay/algebra/extra_one_pairwise_counterexample_and_values.md及独立脚本/报告；root审查矩阵证书。无外审或新颖性认证。

## 未决

一般Q-CAG-HALF、真正聚合安全值、WP、自由extra-one及GI-half仍分别保持OPEN；不能因某强桥反例或代数重写提升/否定其他对象。区间新候选结果待独立核实后增列精确身份。
