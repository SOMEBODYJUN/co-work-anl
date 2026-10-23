# 一般顺序客户吸引：现有成果的衔接与成稿定位

2026-10-23。本文综合现有正文与本轮已保存资产，不提升任何命题的审查等级，也不作外审或新颖性声明。精确身份仍以[模型](../current/customer_attraction/model.md)、[命题账本](CLAIMS.md)、[数学地图](../current/customer_attraction/README.md)及各项实际审查为准。

原问题是：有限单位客户、有限非空共同主题目录、任意人数 $m\ge1$，提供者依次观察完整有序历史选择主题，客户在最终覆盖者间均分；是否每个完整历史依赖纯 SPE 都有 $2W\ge\operatorname{OPT}_m$？重复选择、空主题、零客户及全部离轨平局都属于原量词。**一般命题仍 OPEN，没有统一证明，也没有目标反例。** 现有成果已经给出若干对任意人数、任意目录成立的预算和表示，但尚未把真实后继的适应性统一支付给实际覆盖。后续研究只以这个全范围问题为主线；下列已完成特例作为可调用地基和归档结果保留，不继续以扩大人数、极大主题数或结构边界为独立研究目标。

文献地基应先扣除。[既有文献核对](../current/customer_attraction/literature.md)记录 Deng 等的两人锐 $3/2$ 界和共同目录 $2-1/m$ 下界；Vetta 的有效效用半覆盖是静态 Nash 定理；对称 singleton 的 SPE 终局为 PNE 属于已有单资源机制；层级关联证明采用的最大交叠保护思想有 extension-parallel 拥塞文献来源。客户均分的 Shapley 解释、调和势差、有限逆向归纳、minimax 与 Farkas 工具本身也不能计为本题新增贡献。现有资产的实际内容在于核查这些工具进入共同目录、任意内部子主题和完整历史 SPE 后，哪些推导仍成立。[目录与量词复核](../current/customer_attraction/literature_followup.md)没有给出可直接解决原问题的文献定理；检索未找到不是不存在证明。

目前最直接的全范围正向链从真实路径出发。任取比较客户集 $C$，令 $O=|C|$，用合法主题分数覆盖它，总重为 $\tau\ge1$。[前缀最终利润预算](../current/customer_attraction/fractional_cover_path_budget.md)对每个真实位置给出

\[
O\le P_{i-1}+(m-i+1)\tau u_i,
\qquad
W\ge O F_m(\tau),\quad F_m(\tau)=1-\prod_{r=1}^{m}\left(1-\frac1{r\tau}\right),
\]

其中 $P_{i-1}$ 是早期玩家在**同一实际终局**中的最终利润和。这项递推用真实旧玩家收益支付前缀负载，偏离后的后继只通过合法分母上界控制，因此不需要冻结后继或删除玩家后搬用旧 SPE。取最优并集并用 $\tau\le m$，得到全范围 $W\ge F_m(m)\operatorname{OPT}_m$，其中 $F_m(m)=(1+o(1))H_m/m$；固定 $\tau$ 时保证随人数趋于全部比较覆盖。它也给出 $\tau\le7/2$ 的全人数半覆盖推论和反例的 $\tau>H_m/\log2$ 必要条件，但没有控制 $\tau$ 随人数增长的一般情形。

[实际遗漏私有席位谱](../current/customer_attraction/uncovered_private_seat_spectrum.md)提供另一项全范围预算：固定实际未覆盖的极大全局私有块，只计真实触及这些块的动作。实际每个前缀都零触及，因此阈值可按剩余人数重置，得到 $u_i\ge\lambda_{m-i+1}$、$W\ge\sum_{r=1}^m\lambda_r$。若某个最优并集的遗漏全为这种私有客户，进一步得到锐 $\operatorname{OPT}_m\le(2-1/m)W$。这与分数覆盖递推可以共享实际路径、比较并集和最终利润的记账语言，却尚无将两份信用共同用于任意共享遗漏的预算。不能把两项充分条件的并列当作覆盖全部实例的分类。

另一条全范围链从静态比较游戏出发。[不观察随机查询的安全值](../current/customer_attraction/oblivious_security.md)满足锐 $v_m\ge\operatorname{OPT}_m/(2m-1)$；[静态 iid 凹势](../current/customer_attraction/iid_security_and_flow_barriers.md)确定对称混合 Nash 覆盖基准，并给 $mv_m\le Z_m\le\operatorname{OPT}_m$。因此真正安全值候选 $W\ge(m-1/2)v_m$ 足以完成 half。原iid候选 $W\ge(1-1/(2m))Z_m$ 也曾是充分桥，但个人区已存完整反族，本轮核准后补入[共享§1.2](../current/customer_attraction/iid_security_and_flow_barriers.md)，不得继续列为开放。[安全值链](../current/customer_attraction/security_chain_and_local_boundary.md)及[动态 iid 租金记账](../current/customer_attraction/dynamic_iid_debt_boundary.md)把所缺步骤精确写成真实全路径的总债务界，而非每步非负。**静态下界已经成立，实际 SPE 对真正安全值的全树支付仍未成立；对上述iid值的弱支付已经为假。** 强 iid 桥 $W\ge Z_m$ 已由完整 SPE 与最低静态 CCE 的严格分离否定；逐人安全保底、末位最坏回复值的全员保底及静态 NE 替代也不能补上这一缺口。这些分离应在论证衔接处说明，不另包装成多个一般福利进展。

可复用的局部正向机制也已经清楚。[末两人保底](../current/customer_attraction/last_two_floor.md)和[固定背景两人税](../current/customer_attraction/two_remaining_tax.md)分别控制真实后两人的逐人收益与比较利润；三、四人背景利润定理使其中一部分能够合法提升。[末四人提升](../current/customer_attraction/tail_profit_lift.md)给所有 $m\ge4$ 的 $\operatorname{OPT}_m\le(m/2-1/750)W$，但仍随人数增长。它与前述乘积弱界都是一般有效保证，不是人数无关的常数二。非零背景中的剩余利润也不是根终局覆盖，二者须通过已证明的提升接口衔接。

下表保存已完成正面范围的位置。表中的结构条件与路径条件是真实前提；它们不组成下一轮逐项扩张计划。

| 已完成或已有界的范围 | 可调用结果与原正文 | 归档定位 |
| --- | --- | --- |
| 任意目录，$m=1,2$ | 一人最优；两人锐 $\operatorname{OPT}_2\le3W/2$，见[文献及两人机制](../current/customer_attraction/two_remaining_tax.md) | 文献地基及背景工具 |
| 任意目录，$m=3,4$ | [三人锐 $5/3$](../current/customer_attraction/three_player_sharp.md)；[四人 $1499/750$](../current/customer_attraction/four_player_bound.md) | 完整小人数地基；四人未证锐 |
| 任意目录，$m=5$ | [当前索引界约 $2.061695$](../current/customer_attraction/five_player_indexed_bound.md) | 尚未 half；模板最优不等于游戏最坏值 |
| 任意人数，不交极大花瓣、极大向日葵、层级客户极大关联 | [不交](../current/customer_attraction/disjoint_maxima_bound.md)、[向日葵](../current/customer_attraction/sunflower_maxima_bound.md)、[层级关联](../current/customer_attraction/laminar_incidence_bound.md)：带核心锐 $2-1/m$ | 前三者按所述条件递进，内部子主题仍保留 |
| 任意人数、任意极大主题数；客户极大归属数仅 $1,k-1,k$ | [真实中继及驻留支付](../current/customer_attraction/extreme_maximal_membership_floor.md)：合法背景全员 $\theta$ 保底、利润界及带核心锐 $2-1/m$ | 包含向日葵，与一般层级关联类不可比 |
| 至多六个极大覆盖；另恰七极大且 $m\ge7$ | [六极大联合预算](../current/customer_attraction/six_maxima_joint_bound.md)；[七极大来源证明](../current/customer_attraction/seven_maxima_checkpoint.md)：half | 七极大 $m=5,6$ 未闭合；来源完整与现行概述分开 |
| 任意人数、无界目录；某个最优并集 $\tau\le7/2$ | [分数覆盖预算](../current/customer_attraction/fractional_cover_path_budget.md)：half | 全范围引理的条件性推论 |
| 任意人数、无界目录；某个最优并集的遗漏全为极大全局私有客户 | [实际遗漏谱](../current/customer_attraction/uncovered_private_seat_spectrum.md)：锐 $2-1/m$ | 条件依赖给定 SPE 实际并集 |
| 任意目录、人数；实际倒二主题被全部早期主题包含，或至多 $r$ 个例外且 $m\ge(r+1)^2+1$ | [共同倒二主题](../current/customer_attraction/common_penultimate_theme_half.md)、[少量例外](../current/customer_attraction/penultimate_few_exceptions.md)：half | 真实末两人菜单的路径条件推论 |

表示与辅助变换为一般问题保留了可检查的对象，但不应与福利证明混计。[集合值逆向归纳](../current/customer_attraction/exact_solver.md)按计数缓存可实现终局集合，同时为各有序历史独立重构续局；它没有把策略限制成 Markov 规则。[完整策略锥](../current/customer_attraction/strategy_cone.md)保留每条真实偏离，覆盖矩表示则精确区分线性资料、非负实现与激励方向；[覆盖矩正文](../current/customer_attraction/coverage_moment_geometry.md)明确说明末层行空间足够恢复数值，不等于末层不等式足够证明 SPE 或 half。[分数尾部水位化](../current/customer_attraction/fractional_tail_waterfill.md)对全部查询提供同一客户信用池，并精确保留根、背景和尾利润守恒，却不使降权后的对象继承原 SPE。最近的静态拥挤槽[充分排除接口](../workspaces/customer-attraction/R-d3981c0168644971803a9c3380ed687c/shared_omission/static_crowding_cover_slack.md)同样是一般有效的条件引理；所有真实菜单未被证明满足其条件。它们可进入后续证明，当前没有已成立的通用连接把它们的信用支付给 $2W-\operatorname{OPT}_m$。

最近[常数三根修复](../workspaces/customer-attraction/R-d3981c0168644971803a9c3380ed687c/compiler/padded_insurer_repair.md)给一个与原目标精确相容的反例接口。对所有正深度子局已为完整 SPE、仅根有最大获利偏离 $\Delta$ 的计划，利用共同目录 Cartesian 保险修复全部历史；在共同缩放前的记账单位中，保险实际覆盖增加 $(m+1)\Delta$，最优覆盖增加 $(2m-1)\Delta$，所以坏差额减少 $3\Delta$。有理缺陷须共同复制客户清分母，输出全部数值同比例缩放；不是只加两个总主题。因而每个固定 $m\ge2$ 的原 half 等价于所有此类计划的 $\operatorname{OPT}_m-2W\le3\Delta$。该编译及[独立不交保险的锐三稀释界](../workspaces/customer-attraction/R-d3981c0168644971803a9c3380ed687c/compiler/disjoint_insurer_three_sharp.md)已有独立内部重构；后者的共同核心必须包含于所有合法主题，且根以下分量独立。等价重述提供了另一种攻击原问题的方式，尚未给出越过门槛的计划，也没有把半覆盖归纳自动闭合。

既有成果按能够自足回答的问题归并，不按研究轮次、作者或算法数量拆分。以下记录存量资产的整理位置；特殊范围部分只保全来源，不重新启动局部成稿或局部研究任务。

1. **真实路径的覆盖与利润预算。** 以分数覆盖前缀递推为主定理，合并实际遗漏席位谱，统一模型、比较并集、实际最终利润与真实偏离的记账。两个机制及其条件性锐结论分别证明，明确它们尚未共同支付一般共享遗漏；末四人提升作为已有一般弱界的比较。水位化若没有新增连接，放辅助附录或独立短札，不把信用池存在性写成主定理的最后一步。这组已有自足的全范围不等式和明确覆盖推论，适合形成部分结果稿；外部优先性仍须另核。
2. **极大关联结构中的真实中继。** 在统一“客户对极大主题的归属集合”语言下，合并不交、向日葵、层级保护与极端归属驻留证明，写清包含关系与不可比性；扣除 singleton 与最大交叠的文献地基。六、七极大的联合系数证明作为另一种有限结构方法独立归档，不用其病例数充当一般机制。既有小人数最佳界及旧常数作为独立地基归档，不继续逐人数调优。
3. **可信性、静态比较与完整资料。** 将 SPE 不等于 PNE、最低静态 CCE 仍不能代表 SPE、无拥挤 $3/2$ 族、负前缀无限族等，围绕“真实后继为何不能由静态终局替代”组织成一份有主命题的分离稿；完整策略证书作为可核验附录。覆盖矩、非负实现及全树锥可另成表示方法稿，避免把标准求解器实现与新的表示定理混写。
4. **可信编译与稳健根缺陷。** 常数三根修复、精确缩放、全历史拼合、相同人数的等价重述，以及所述独立保险架构的匹配下界，自然组成一篇方法短稿。应与普通有限负例诊断分开；固定锥未越门槛、算法数量和阴性试验不列为数学贡献。该稿的准确结论是可复用编译和架构锐性，不是原猜想已解决。

这些合并建议保留每项现有定理的独立范围与来源，不要求用一篇稿件容纳全部资产。下一项主线成果必须对任意 $m$、任意共同目录提供新的真实全树支付、合法等价归约或完整目标反例；方法不限定为上述预算、安全值、势、运输或编译。现有结构与小人数结果继续可读、可引用、可回归，但不再以扩张特例代替这一全范围义务。
