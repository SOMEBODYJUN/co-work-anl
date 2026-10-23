# 本轮精确命题和状态

## Q-CAG-HALF

沿用共享模型与原量词，仍OPEN。没有一般证明或完整SPE目标反例。

## B9-STATIONARY-INCIDENCE-FACTOR-v1

- Exact statement：对整数n≥1、有限根集、非负整数路由矩阵N=(n_ji)，每列和n且n_ii=0，任意平稳概率N pi=n pi、任意归属I、整数0≤K_i≤Σ_(j∈I)n_ji以及背景b≥0，定义a_i=1_(i∈I)，R=Σpi_i a_i/(b+a_i+K_i)、F=Σpi_i K_i/[n(b+a_i+K_i)]，零贡献项单独按0计。则R≥beta F，beta=n(b+1)/(n(b+1)+floor(n²/4))；此统一系数最优。
- Objects/domain：抽象路由菜单与一个客户的系数。实际背景取非负整数；解析代数亦对非负实数b成立，不改变原CAG。
- Assumptions/quantifiers：上述每一个菜单、平稳概率和客户。pi允许零值。不假设该菜单为SPE。
- Sharpness：四根I={1,2}、q=floor(n/2)及正文的无self整数矩阵取等。四个实际主题{x,p1},{x,p2},{p3},{p4}实现该客户的全部计数；附加标记的总收益不声称取等，更不声称SPE。
- Dependencies：平稳容量Σpi K≤nΣ_(i∈I)pi；整数q(n−q)≤floor(n²/4)；逐分支有理恒等式。
- Evidence：自足解析证明、先独立重构的审查、root逐式复核；Fraction核验仅查算术。
- Counterevidence/objections：未发现成立的代数异议。扩大为真实SPE、总客户收益sharp或原half反例均不成立，正文没有这样宣称。
- Status：完整证明、独立内部重构通过；个人资产未正式共享入库，外审及新颖性未认证。
- Related files：[正文](charging/stationary_intermediate_incidence_factor.md)、[独审](structural/independent_stationary_factor_review.md)、[核验](structural/stationary_factor_fraction_check.py)。

## 根完整菜单平均福利候选

固定原m人完整SPE，Z_1(A)为强制根选A后同一sigma的完整m槽终局。候选为存在一个查询不依赖的Q∈Delta({Z_1(A)})，使全部合法主题T同时有E_QΣ_(x∈T)1/(1+c_x(Z))≤W/m。它比只看实际端点弱，且与旧的r−1槽菜单、Mfull≤u1、同p推送不同。当前未证、未找到完整反例；有限阴性不增加其状态。
