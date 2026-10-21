# 本轮精确Claim与开放义务

本页是个人阶段资产身份，不自动修改共享canonical。模型均为CAG-MODEL：有限单位客户、有限非空共同目录、单位权提供者、任意正人数、完整有序历史纯SPE与任意平局。一般Q-CAG-HALF仍OPEN，未得一般证明或真正反例。外审与新颖性均未认证。

## B5-CLIQUE-ALIGNMENT-v1

- **Objects / domain / quantifiers:** 任意m≥2、q≥1、L≥2；给定同一完整SPE，任意L个长度m−2历史H_r，每族q个合法前置主题Z_i^r及其真实末位F_i^r；任意完整图边方向、固定非负边权λ。
- **Definitions:** 每客户K_r=Σ_i1_(x∈Z_i^r)，a_r=1/(b_r+1)，g_r=1/((b_r+1)(b_r+2))，A_r=Σ_i1_(x∈F_i^r)/(b_r+1+1_(x∈Z_i^r))。令ΣK_r=tq+s，0≤s<q，ell_rs=(K_r+K_s−q)_+，χ=q binom(t,2)+st−Σell。E_rs=(q−1)A_r−(q−1)a_rK_s+g_r(K_rK_s−ell_rs)，ω_x=min_edges λ_rs g_r。
- **Exact statement / conclusion:** χ≥0且为规定K_r的共同索引总重叠缺额精确最小值；真实SPE必有Σ_x[Σ_edges λE−ωχ]≥0。等有效边权时逐客户重排上包络精确；不等权仅保证min-weight下界。
- **Dependencies / evidence:** 真末位BR逐行展开、列占用凸计数及连续模q块构造。作者与root独立解析重构；两套不互导审计。
- **Scope / objections:** 任意q/L/m，但只是必要菜单预算，不是SPE可行性充分条件或根W支付。额外共同索引标签限制精确性。不能按客户选λ。
- **Status / files:** 内部解析审查通过；[正文](coupling/clique_alignment_budget.md)、[独审](parent/clique_alignment_review.md)、[独立审计](parent/clique_independent_audit.json)。

## B5-SAME-QUERY-REDUNDANCY-v1

- **Exact statement:** 若上式所有族逐索引前置主题均为同一T_i，则完整图新必要行被源族原有within-menu O行的非负组合支配，对任意非负边权均不能增加约束。
- **Definitions / quantifiers:** 沿用上一Claim全部量词，额外假设Z_i^r=T_i对所有r,i；实际每客户所有K_r=K且C_rs=K。
- **Dependencies / evidence:** 新行与原行之差是Σ_edges w(K−ell)−ωχ≥0；取所有索引会员集合相同即证明该余项非负。2396坏点的精确核对仅为该一般支配的应用。
- **Scope / objections:** 仅相同前置查询菜单；不排除不同Z族的真正新信息。把旧回复L_i作为新前置需查询原策略真正新回复，现旧坏点无这些字段。
- **Status / files:** 完整解析支配证明及精确应用；[正文及真实缺字段](coupling/same_query_redundancy_and_2396.md)。

## B5-COMMON-TERMINAL-EXCHANGE-v1

- **Exact statement:** 同一完整SPE中，在历史h偏离合法B后终局计数q；若真实末位历史g上σ(g)=B且(g,B)也有计数q，则对每个合法T有u(h)≥U_B(q)≥Σ_(x∈T)1/(1+c_g(x))。
- **Objects / domain / quantifiers:** 任意原模型m≥1、全部有序h及长度m−1的g、全部B/T；要求这两个具体真实分支共享同主题及完整终局计数。
- **Dependencies / evidence:** h的真实偏离最优、同主题同计数收益恒等、g的真实末位BR；root定义级重构。
- **Scope / objections:** 其他SPE里可实现、同福利、任意重排终局均不足以提供见证。
- **Status / files:** 完整短证明且内部独立检查；[正文](credible/common_terminal_exchange.md)、[root审查及推广](parent/common_terminal_exchange_review.md)。

## B5-LOAD-DISTORTION-MATCHING-v1

- **Objects / definitions:** 任意根实际路径S_i、终局负载c*、收益u_i和W。I⊆[m]；E_h与实际并集不交且T_h=S_h∪E_h合法；α∈[0,1]。
- **Assumptions / quantifiers:** 对每个选用边i→h有上一Claim在玩家i实际前缀处的真实见证B,g，且α(1+c_g(x))≤c*_x于S_h、c_g=0于E_h；这些边存在I到I的完美匹配，且某最优m主题组合的漏客户被∪E_h覆盖。
- **Exact conclusion:** Σ_h|E_h|≤(1−α)Σ_(i∈I)u_i≤(1−α)W，故OPT_m≤(2−α)W。α=1/2允许c_g≤2c*−1，含实际无拥挤特例。
- **Dependencies / evidence:** 前一真实交换引理及完美匹配求和。root提出拥挤推广并完整解析证明，作者独立整合。
- **Scope / objections:** 没有证明一般SPE存在这种匹配、扩张主题或漏集覆盖；α=0亦不使这些条件自动成立。
- **Status / files:** 条件性解析证书，内部检查；同上正文§2与root独审。

## B5-MANY-PUNISHER-LIFT-OBSTRUCTION-v1

- **Objects / assumptions:** k≥2早期不交X_i,Y_i，C_i=X_i、A_i=X_i∪Y_i，所有惩罚B_i,l只覆盖本组与外部Z；真实路径C_1,…,C_k,D_1,…,D_q，D⊆Z。指定A_i偏离后末尾B_i,l与B_i,l偏离后末尾A_i/其他B_i,j共享完整终局。
- **Exact conclusion:** 两条真实比较强迫x_i≥x_h/2+a_h（i≠h），故Σa≤Σx/2；即使增加惩罚者人数、异质组和重叠奖励也不能用此模板突破遗漏比1/2。若所列A,D组合覆盖所有客户，则OPT/W≤3/2。
- **Evidence / objections / status:** 完整交换证明与14组展开单位客户公式审计；原拟t>2整数构造甚至违反实际末位BR。只排除该分支几何，不给一般无拥挤上界；[正文](credible/common_terminal_exchange.md)。

## 活跃开放义务

- 真实离轨完整菜单的费用怎样与较早SPE行共同支付根W？相同查询族完整图不能解决旧坏点。
- 更早玩家的完整分数价格B(u_i)≤W；末两位已知，三剩余的有限总重推进正在精确审查。
- `security/full_terminal_debt.md`的加回偏离者H信用、全分布聚合及copositive接口均按其实际状态保留。恒等式不是其聚合非负的证明。
