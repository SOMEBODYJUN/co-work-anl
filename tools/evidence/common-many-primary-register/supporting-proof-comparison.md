---
id: "facility-games/common-many/primary-register-chronology-and-contract-review"
kind: "review"
type_tag: "审查"
title: "登记命题的时序纠错与接口核查"
status: "primary-proofs-compared; finite-arithmetic-cross-checks-passed; polynomial-imports-separated"
review_status: "internal mathematical reconstruction; no external review or priority certification"
summary: "按真实证明区分旧浅层选择器、一般完整盒有限存在、MAX与RANGE导入、同输入等轻权流细化及仍有效的旧势反例；登记和入口的历史开放句不覆盖后续已证存在性。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/current/multi_facility/greedy_box_global_progress.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/current/multi_facility/height_two_box.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/current/multi_facility/three_site_chain_box.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/current/multi_facility/depth_three_box_boundary.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/current/multi_facility/equal_light_flow.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/current/multi_facility/polytime_frontier.md#2026-10-07-update;MF-PURE-CAP-POLY;SC-K-UNIFORM-LIGHT-FLOW-2;SC-K-GREEDY-FIXED-POTENTIAL-NO"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/current/multi_facility/adaptive_reset_floor.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/current/multi_facility/frozen_overload_completion.md"
---

# 登记命题的时序纠错与接口核查

本页是主登记清洗所用的承重比较：原稿中的“已证”“开放”“多项式”分别还原成具体命题、量词、外部算法合同及实际软件层级。它不把登记行数、更新日期或PASS字样当作通用证明。全文阅读的原件和定向读取的长原件区段分列在[原件核读记录](independent-read-manifest.json)；其中122708字节`polytime_frontier.md`只定向核读本页需要的区段，没有声称整份已读或由本比较代为done。

## 固定模型与三个不同问题

物理模型均是有限正权不可拆客户、有限非空共同站点目录、显式k≥2带标签设施；客户被覆盖就必须选一覆盖设施，独立混合。权u客户选设施f的条件成本是u加其他客户在f的期望总重。客户先整原子选站s、再独立均匀选本站q_s家设施时，其跨站比较为

\[
(W_s-u)/q_s\le W_t/q_t.\tag{1}
\]

必须扣掉源的**一名原客户全部自重**，检查其全部原已占选项。原游戏没有人为盒容量；使目标超盒的严格改善仍是合法偏离。未开站客户在真实设施偏离后会重新确定服务集，不是固定在轨客户菜单的一部分。

规范贪心先后插入k家，首次开站固定首次覆盖原池J_s⁰、重量W_s⁰；旧站下一分数W_s⁰/(q_s+1)，新站为尚未覆盖重量。正覆盖时末分数γ>0且

\[
q_s\gamma\le W_s^0\le(q_s+1)\gamma,
\qquad N_v\le\gamma\ (v未开).
\tag{2}
\]

客户原归属h的最终q_h不小于其任一其他已占选项的q。冻结仅一个已占选项的客户及u≥γ客户于原站。剩下逐名轻客户u<γ。以下必须区分：在此占位**存在**完整盒NE；用某特定目标的每个最优解选出NE；在输入位长多项式时间找到它并完成全部续局。前者不保证后两者。

## 一般存在已经补足，旧浅层证明仍有独立内容

三站链原件处理H→M→L、每边任意多且互不等权的轻客户，结论是完整盒中每个原客户势

\[
P=\sum_s\frac{W_s^2-\sum_{i:a_i=s}u_i^2}{2q_s}
\tag{3}
\]

的全局极小者都是NE。高度二原件推广到每条开站有向路径≤2、允许多父合流与分叉、每名轻客户恰两选项，仍不提供全局最小化位多项式算法。其关键是被盒上界挡住的反向改善，令目标u负载M、客户重w、δ=M+w−(q_u+1)γ>0；u的每个入邻h没有入边。当前在u的整原来源池重量S_h≤γ，且送回后h不超原盒。按固定次序选池到首次累计S≥δ，则δ≤S<δ+γ；退池再归还w客户保持所有盒。精确势差严格小于

\[
\sum_h(1/q_u-1/q_h)[(S_h^2+T_h)/2-S_h\gamma]
 +(\operatorname{cross}-S\delta)/q_u<0.
\]

这里T_h≤S_h²、S_h≤γ及首越规则逐项给符号。三站链有更短的“全部上游入池一次退回”独立推导。后续一般定理不保证任意图上仍能用这个旧P选择器，因此这些证明及其精确量词不应被删成历史摘要。

2026-10-07一般原件`greedy_box_global_progress.md`改用不同的势。归一化w_i=u_i/γ∈(0,1)、c_s=W_s⁰/γ−q_s∈[0,1]，置

\[
X_s=c_s+\sum_{a_i=s}w_i-\sum_{h_i=s}w_i,
\quad p_s=X_s/q_s,
\quad e_i=(X_{a_i}-w_i)/q_{a_i},
\quad r_i=(1-w_i)/q_{h_i}.
\]

按全部不同r阈值ρ₁<⋯<ρ_d建立

\[
\mathcal P=(\operatorname{sort}_{\uparrow}(\min(p_s,\rho_1)),-N_1,
 \ldots,\operatorname{sort}_{\uparrow}(\min(p_s,\rho_d)),-N_d),
\tag{4}
\]

N_l为阈值ρ_l组的离家人数；每站每块只出现一次，计数紧跟各自截断块。满足自身保护H:e_i≤r_i的客户作任意严格改善，或在外且违反H的客户归家，均严格增大同一交错字典序势。归家不必是客户改善。改善后非负下盒保留；任意归家顺序至多n次即修复完整盒及H：若终态X_s>1，s必有外来i，且最大归属重数给e_i>(1−w_i)/q_s≥r_i，与无可归家者矛盾。初态原归属已有盒/H，所以“严格改善—完整归家修复”有限终止，终态检查全部原选项而得到NE。

共有S=∏_i|A_i|个允许赋值，**包括中途超上盒赋值**，每个微步推进故改善加归家合计≤S−1。客户跨批可反复离家、归家；没有逐人仅动一次结论。可交错操作，但未完成修复中作改善者仍须满足其自身H。数学存在允许实数；位界用显式有理数据，轨迹不保存时多项式空间。S−1及势虽有多项式二进制位长，数值可指数，故不推出一般位多项式总时间，也没有给超多项式下界。

因此旧chain/height-two末尾的“一般盒存在未决”只保留为原稿时间状态；当前正确状态是**所有规范贪心占位有完整盒NE及有限构造，一般统一位多项式选择仍未证**。两种结构DP联合这个同冻结存在性和BOX-TO-2形成新SC-K-BOX-STRUCTURED-POLY-2，去掉旧存在性输入中的两选项/深度二限制；双侧个体度、图宽或局部权种等DP自身参数仍保留。不能悄悄扩大旧ID量词，也不能由一般有限轨迹推得DP的多项式界。

## MAX、RANGE和在轨/离轨责任

以下是外部受限相同链Nashification的不同算法合同。输入是正有理任务、每人非空允许的**标签设施**集和一份完整可行纯赋值。机器成本为设施总负载；不能把q_s家站点自动换成速度q_s相关机器。

| 合同 | 输出约束 | 本批原稿中的实际使用 |
| --- | --- | --- |
| MAX | 位多项式求同一完整允许游戏纯NE，终态最大负载≤初态最大值 | 受帽纯完成；AR；BOX-TO-2；基本冻结超载η版；完整续局的默认查询 |
| RANGE | MAX并使终态最小负载≥初态最小值；逐关联分量调用分别保各分量范围 | 等q/分量/重数分组RANGE及轻分量的在轨选择；AD首轮纯装箱后保γ；冻结超载可选μ_C强化 |

RANGE强于MAX。只保最大值不推出最小值不减。`adaptive_reset_floor.md`明确称RANGE来自追踪论文§4 blocking-flow及阶段/互补链的**推导**，并非Theorem4.7独立列出的原句。此前审查的作者PDF检索未成功，现存记录不构成本轮重新读到论文；本页也未取得该论文或核外部运行界。因此此处将位多项式结论保留为明确导入合同，有限正确性可独立证明。没有把原稿引用、较新登记或旧PASS升级成新的原论文独立核验。

有限严格纯改善本身同时保持两端：L_g+w<L_f时，新源L_f−w>L_g≥旧min，新目标增加；新目标<L_f≤旧max，源减少。半平方负载和下降w(L_g+w−L_f)<0，有限状态终止。这证明一个有限RANGE过程，却不证明步数多项式，故原审计的strict replies不是论文调度器实现。

受帽完成先删去**独占且原子自身>B**的巨客户及设施，在普通设施游戏以MAX保最大≤B，再放回。普通客户进巨设施成本>B，巨客户已付自身重不能严格改善，所以重新接纳后检查了全原允许集。仅说“过帽箱含一个巨客户”不够，不能另有轻客户。

冻结静止超载允许多客户箱，但需逐个冻结i核M_h−w_i≤每个其他冻结箱负载及每个普通替代站的强制原子纯NE下界η_s；残余纯NE给普通设施≥η_s且MAX保≤B，因而全游戏NE。η仅由残余普通设施和残余客户计算，不能把冻结客户算入。若另用普通关联分量初始最小值μ_C增强成max(η_s,μ_C)，才需要额外RANGE。基本η版**不需要MIN合同**。

完整盒在轨NE接BOX-TO-2不需RANGE，也不需H。存续源q_u≥2的在轨收益a=W_u/q_u≥γ使本源W_u=q_ua正好满足q_u−1静止设施的装箱预算；其他站由盒得W_t≤(q_t+1)a。消失的q_u=1源用**全局原贪心池重置**，不是将原池预算套在后来选中的客户池。令K为原q=1站，P为其原客户并集；最早开K时贪心比较给w(P∩C_t)≤2γ，所有其已占备选仍在K。新目标源孤儿加真正新客户由原池预算≤2γ。于是偏离者受帽≤2a，再用MAX完成纯NE。

不同标签的真实单坐标偏离给不同布局，k(|S|−1)条显式例外加在轨策略及默认NE规则构成一份完整续局；无需列|S|^k全表。当前生产离轨/默认仍用有限pure_improve，未实现导入MAX；即使等权在轨流已位多项式，也不能称当前完整程序总运行位多项式。

## 旧、新等轻权流覆盖同一原模型输入类

旧SC-K-UNIFORM-LIGHT-FLOW-2已允许任意部分重叠、任意重数、无限制图宽；仅要求冻结重客户/单选项后其余轻客户具有同一个物理权u∈(0,γ)。新SC-K-EQUAL-LIGHT-FLOW-2使用同一MF类，不是新扩大输入覆盖。旧目标对冻结重量P_t、变量计数n_t为

\[
F=\sum_t[P_tn_t/q_t+u n_t(n_t-1)/(2q_t)],
\quad n_t\ge\max(0,\lceil(q_t\gamma-P_t)/u\rceil).
\tag{5}
\]

新抽象设置δ=u/γ，H_t为home人数，b_t=c_t−δH_t可负，X_t=b_t+δn_t；在**所有合法赋值、无盒预过滤**最小化

\[
\Psi=\sum_t[b_tn_t+\delta n_t(n_t-1)/2]/q_t.
\]

因P_t/γ=q_t+b_t，有F/γ=N+Ψ。新证明对**每个**无约束极小者用两条逐名home返路径：负X端沿出边走到无出边终点，返路端点差X_s/q_s−(X_z−δ)/q_z<0，故下盒；违反H者从home逆追到X_z≤1−δ、q_z≥q_hi，连同该客户返路得差≤(1−δ)/q_hi−e_i<0。等权使中间每站一进一出抵消，home→option严格增序保证路径客户互异。H再排除X_t>1，单移目标差排除全部原菜单严格改善。

所以无约束最优者全满足旧下盒，旧、新最优值差常数，**最优赋值集合完全相同**；新贡献是删下界机器、自动H性质、明确负成本整数增广实现及位复杂度证明。单位客户节点及每站可达客户数M_t个slot不展开二进制q，恰N次增广；Bellman–Ford处理负残边。canonical严格松弛前驱避免零环，相等距离重写前驱不在该论证内。

优化不能换成任意NE。原严格贪心可实现例q=(3,2,1,1)、c=(1/10,1/10,1/25,0)、δ=1/2、菜单12和23中，away(2,3)是严格跨站NE并满足H，却有X₁=−2/5；home(1,2)才是唯一全局最优。新版同输入结论也不去掉等权：q=(3,2,1,1)、c=(44/45,44/45,2/45,0)、两权4/5和44/45时，唯一极小away(2,3)有X₃=46/45；两人同时返路的内部项恰0，但端点项−88/2025+32/675=8/2025>0。需同时处理不同端点权及不同1−w停止阈值，不能只补“异权内部项”就称证明闭合。

## 普遍存在不撤销的三种旧势反例

| 旧对象和优化域 | 原件的精确失败 | 新一般结果为何不撤销它 |
| --- | --- | --- |
| 固定贪心布局，全部合法站纯赋值的原客户P全局极小 | k8、γ200例仅两个NE，good势86264，bad势86200且是全部16赋值唯一全局极小。bad的B设施收益214，B→G后231客户在每个mixed NE都严格去G，偏离者430，比例215/107>2 | 此P全局极小确是NE，但**因子二不安全**；新方法冻结该≥γ客户且优化截断交错势，量词/选择器不同 |
| 只套下盒、允许两种轻权的P极小 | 参数n≥45且5整除的一族，唯一极小X=M,Y=L使L总重2n+1超过上盒2n；同布局原home已是盒NE | 否定等权反向运送证明的直接异权推广，非盒NE不存在或复杂性下界 |
| 深度三树，全部完整盒内P极小 | k15、γ1000，16轻赋值恰6盒，唯一盒极小势5948950/3非NE：重150客户D→C外部1451>1450，目的C将3050>3000；唯一盒NE势1983200，差650/3 | 否定深度二旧P选择器推广；新构造允许中途超上盒并以归位修复推进另一势，故不冲突 |

第三行特别说明：递归退回整池可保持盒却增加P达650/3，失败在降势断言，不只是可行性。也不是一致有向长路径算法的反例，因为该图有合流分叉。

## 本次自查与交接边界

本比较没有运行canonical流、完整续局、默认求值或论文调度器，没有新增通用软件运行计数。独立标准库Fraction脚本逐项精算四份小输入：旧uniform-flow两变量四赋值的新旧最优集合相同且唯一(M,L)；上述任意NE坏例的四赋值；固定布局势坏例全部16赋值/恰两NE及唯一全局极小；两异权四目标值与返路端点和。全部断言通过。其证据是算术自查，普遍结论仍由原文证明承担；也没有把这些小输入计为新版5242例审计的复跑。

已有正式正文承接分别是[一般盒定理](../../../archives/facility-games/subarchives/common-many/state/定理/规范贪心占位的完整盒均衡与因子二续局--定理.md)、[严格推进引理](../../../archives/facility-games/subarchives/common-many/state/引理/阈值截断与归位计数的严格推进--引理.md)、[浅层盒选择](../../../archives/facility-games/subarchives/common-many/state/定理/开站有向深度二的整池交换盒均衡--定理.md)、[导入合同审查](../../../archives/facility-games/subarchives/common-many/state/审查/受限同链调度导入的最大值与范围义务--审查.md)、[等轻权流](../../../archives/facility-games/subarchives/common-many/state/算法/等重轻客户下盒流与无约束细化--算法.md)和各反例。本页提供的是主登记的时序、量词和接口校正，不重新登记这些对象为新定理。一般异权统一位多项式选择仍是准确接续目标；旧原稿OPEN不覆盖已证存在性，现有有限PASS也不升级未实现的多项式合同。
