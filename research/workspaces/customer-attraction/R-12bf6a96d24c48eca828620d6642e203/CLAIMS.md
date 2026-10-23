# 本轮精确Claim账本

总目标Q-CAG-HALF采用仓库CAG-MODEL全部原量词，仍OPEN；这里的个人备份不是共享canonical入库。

| ID | Exact statement、域与量词 | 依赖、证据与状态 | 文件 |
|---|---|---|---|
| B9-AGG-EXTRASLOT-STRONG-NO-v1 | 存在合法单位客户实例、完整历史纯SPE与目录分布p，使完整m槽真实偏离菜单上的sum_i G_i^+(p)>sum_i D_i(p)；三人34客户含空主题见证 | 复用旧完整输入，新沿全部实际位置聚合；父与作者两路定义级精确内审；非half反例 | parent/extra_slot_independent_review.md、menu_minimax/aggregate_extra_slot_empty_dilution.md |
| B9-EMPTY-DIRECTIONAL-TEST-v1 | 任何含空E的有限形式策略、任何q与e∈[0,1]，p_e=(1-e)delta_E+e q的D-G精确为e[D(q)-H_E(q)]+e²[H_E(q)-G(q)] | 双线性证明；不需SPE；没有正面福利结论 | parent/extra_slot_independent_review.md |
| B9-PRIVATE-PADDING-TRANSFER-v1 | 完整SPE从不指定E，全部指定收益min eta>0；原客户乘整数K、新添整数J个E私有客户，K eta>=J则同sigma仍完整SPE；沿无E实际路径的差变为KDelta(e)+(mJ/2)(1-e)² | 全历史比较的一般证明与独立重构；改变实例另立Claim，不改原目标 | parent/nonempty_padding_transfer.md |
| B9-NONEMPTY-AGG-EXTRASLOT-NO-v1 | 存在七非空不同共同主题、2279单位客户、三人完整SPE、p，使sumD-sumG=-7/384；同构造K,J参数存在负差iffK>66J | 父逐单位审计与作者盲独审；仅强桥反例，无外审/新颖性认证；W2144、OPT2278 | parent/nonempty_padding_transfer.md及两份独立脚本 |

G_i^+包含完整m槽强制终局，再增加一槽独立查询；D_i是原游戏第i位真实强制收益。sumG<=W和存在自由聚合背景Q均仍OPEN，本账本没有因强桥失败而否定它们。其他研究分支只按其已写正文的实际范围接续，阴性有限扫描不提升Claim。

## 新增中继边界与一般静态工具

- B9-ACTUAL-PREFIX-INCUMBENT-RELAY-NO-v1：原模型61客户四人完整SPE，实际BAAF。f_r(b,T)定义为强制T后的所有纯SPE续局中入场收益最小值。沿真实根动作B，有f4(empty,A)=9<(3/4)f3(B,A)=39/4；同sigma的V及节点max亦失败。依赖既有root_tax客户输入、新完整证书、全末BR条件表；父与作者两路定义级内审通过。只否定该比例递推，无half反例；详见parent/actual_incumbent_independent_review.md与direct_cover/正文。
- B9-OPT-RANDOM-SLOT-EXCHANGE-v1：任意有限实例、任意m槽实际元组和最优m槽比较元组（可重复），所有r均有outside新增概率和≤opt丢失概率和，逐客户系数P_r(d)Q_r(c)；调和加权核为C(m,c+d)/(d C(m,c)C(m,d))。无SPE假设；父独立Vandermonde重构通过，无外审/新颖性认证；详见signed_harmonic/optimal_exchange_moments.md与parent/独审。仅静态最优性非负组合，不含half结论。
- B9-REPEATED-TAIL-TEMPLATE-NO-v1：给定作者C_i/A_i/B_i/D目录与指定actual C_1…C_k D^r、fresh-A_i deviation后B_i^r两条真实路径，r>=2不能同时属于一完整SPE，因d>=rc/2且d<=c/(r+1)。c>0，r正整数，其他参数按正文；父独立重算两条末位收益通过。只反驳这条路径模板，不排除所有多尾或森林构造；详见credible_attack/repeated_tail_obstruction.md。
