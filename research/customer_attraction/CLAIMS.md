# 顺序客户吸引：一般半覆盖的精确身份与命题索引

研究存档：customer-attraction；目标身份：Q-CAG-HALF。

本页固定已有 `Q-CAG-HALF` 身份，整理不创建更强的新版本。其他 CA 命题的逐项范围、依赖与证据仍以[全仓现行账本](../current/claims.md)、[五轴审查状态](../review_status.json)和所链接自足正文为准。

## Q-CAG-HALF

| 项目 | 精确内容 |
| --- | --- |
| Exact Statement | 对下述每个实例、每个完整历史依赖纯 SPE \(\sigma\)，有 \(2W(\alpha(\sigma))\ge\operatorname{OPT}_m\) |
| Objects / Definitions | [CAG-MODEL](../current/customer_attraction/model.md)：有限客户集 \(N\)、有限非空共同目录 \(\mathcal S\subseteq2^N\)、终局客户覆盖重数 \(c_x\)、均分收益 \(u_i\)、覆盖福利 \(W=\sum_i u_i\)、最优 \(m\) 主题覆盖 \(\operatorname{OPT}_m\) |
| Domain / Assumptions | \(m\ge1\)；所有提供者单位权，所有客户单位价值；依次观察全部有序历史各选一次主题；所有人可选同一目录 |
| Quantifiers | \(\forall N\;\forall\mathcal S\;\forall m\ge1\;\forall\sigma\in\mathrm{PureSPE}(N,\mathcal S,m)\) |
| Scope / Boundary | 允许空主题、重复选择、零客户、全部历史依赖平局；类型整数重数表示不同单位客户；不涵盖异目录、带权提供者或混合行为 SPE |
| Conclusion | 一般目录、任意人数的覆盖福利至少为最优的一半；零最优值使用乘法不等式，不定义 \(0/0\) |
| Dependencies | 模型、完整有序历史上的 SPE 定义及最优覆盖定义；一般证明尚缺，不把任何候选安全值桥设为必要前提 |
| Paper Fact | [Deng 等 arXiv:2307.07174v2](https://arxiv.org/html/2307.07174v2) §6 提出超过两人时 sPoA 上界二的猜想；[文献范围复核](../current/customer_attraction/literature.md)区分原文措辞与本页共同目录输入类 |
| Evidence | 三人、四人、有限极大主题数及层级关联类已有内部完整证明；它们各有自己的精确身份，均不覆盖本页全部量词 |
| Counterevidence / Objections | 尚无本目标反例；已有反例击穿逐人安全值、根总税、局部非负预算、静态 NE 导入等指定辅助桥 |
| Status | **OPEN**；完整一般证明与目标反例均未取得；没有外部同行评审或全球新颖性认证 |
| Related Files | [原目标页](../questions/customer_attraction_half_coverage.md)、[数学地图](../current/customer_attraction/README.md)、[前沿](RESEARCH_STATE.md)、[失败记录](FAILED_ROUTES.md)、[精确计算合同](../current/customer_attraction/exact_solver.md) |

## 已有承重资产：引用时回到原陈述

| 身份 | 可使用的结果 | 必须保留的范围 |
| --- | --- | --- |
| `CA-THREE-SHARP-5-3` | [三人锐界](../current/customer_attraction/three_player_sharp.md)：\(\operatorname{OPT}_3\le(5/3)W\)，有匹配下界 | 恰三人；不是任意人数定理 |
| `CA-FOUR-UPPER-1499-750` | [四人一般目录上界](../current/customer_attraction/four_player_bound.md)：\(\operatorname{OPT}_4\le(1499/750)W\)，其中 \(1499/750<2\) | 恰四人；未证常数尖锐 |
| `CA-FIVE-INDEXED-UPPER` | [五人索引偏离上界](../current/customer_attraction/five_player_indexed_bound.md)：\(\operatorname{OPT}_5\le\beta W\)，\(\beta\approx2.06169478572>2\) | 未达到半覆盖；`\beta` 的精确有理数以原文为准 |
| `CA-SIX-MAXIMA-HALF` | [六极大联合预算](../current/customer_attraction/six_maxima_joint_bound.md)：任意人数半覆盖 | 至多六个不同包含极大覆盖；内部子主题与关联可以任意 |
| `CA-SEVEN-MAXIMA-N7-PLUS` | [七极大来源证明](../current/customer_attraction/seven_maxima_checkpoint.md)：七人以上 \(U=\operatorname{OPT}_m\le2W\) | 恰七个极大覆盖、\(m\ge7\)；来源证明完整且已内审，现行页只是依赖概述；\(m=5,6\) 仍缺分支 |
| `CA-LAMINAR-INCIDENCE-MAXIMA-2M1` | [层级关联锐界](../current/customer_attraction/laminar_incidence_bound.md)：带共同核心的 \(2-1/m\) 界 | 客户的极大主题关联为层级族；不等于一般目录 |
| `CA-FRACTIONAL-COVER-PATH-BUDGET` / `CA-FRACTIONAL-COVER-7-2-HALF` | [真实前缀利润递推](../current/customer_attraction/fractional_cover_path_budget.md)及乘积界；某个最优并集τ≤7/2时全人数半覆盖 | 分数覆盖数条件承重，任意目录无条件half仍OPEN；P必须为旧玩家最终收益和 |
| `CA-ACTUAL-PRIVATE-SEAT-SPECTRUM-v1` / `CA-OPTIMAL-PRIVATE-OMISSIONS-2M1-v1` | [实际遗漏席位谱](../current/customer_attraction/uncovered_private_seat_spectrum.md)：一般逐位置谱预算；某个最优并集的实际遗漏全为极大全局私有客户时锐OPT≤(2−1/m)W | 任意人数、目录与已覆盖客户共享；私有遗漏条件承重。触块计数不等于旧路由计数；独立内部解析审查，无外审/新颖性认证 |
| `CA-COMMON-PENULTIMATE-HALF-v1` / `CA-PENULTIMATE-FEW-EXCEPTIONS-HALF-v1` | [末两人菜单](../current/customer_attraction/common_penultimate_theme_half.md)及[少量遗漏平方阈值](../current/customer_attraction/penultimate_few_exceptions.md)给无界人数/目录的实际路径条件性half | 倒二A被全部早期主题包含；或至多r个不包含且m≥(r+1)²+1。一般路径仍OPEN，外审与新颖性未认证 |
| `CA-EXACT-PURE-SPE-ALL` / `CA-STRATEGY-CONE` | [全集逆归纳](../current/customer_attraction/exact_solver.md)与[完整策略重数锥](../current/customer_attraction/strategy_cone.md) | 精确有限工具；完整树证书可能指数大，有限运行不是一般证明 |
| `CA-OBLIVIOUS-MIXED-SECURITY-2N1` | [静态安全值](../current/customer_attraction/oblivious_security.md)：\(v_m(0)\ge\operatorname{OPT}_m/(2m-1)\) | 对手不观察查询抽样；从安全值到真实顺序福利仍缺聚合桥 |

这里的“完整”指所列范围内的数学证明及相应内部审查；外审、优先权、实现和一般适用性分别报告。改变量词、输入域、均衡概念、价值或权重约定时另立身份，不沿用 `Q-CAG-HALF`。

新增机制边界：[`CA-WORST-PNE-WELFARE-NO`](../current/customer_attraction/worst_pne_welfare_counterexample.md)否定同实例最差静态PNE福利支配桥；完整有限证书及独立内审，不影响 Q-CAG-HALF 的OPEN状态。

新增机制边界：[`CA-WORST-CCE-WELFARE-NO`](../current/customer_attraction/worst_cce_welfare_counterexample.md)给十三客户完整SPE覆盖9，低于同实例每个静态CCE的期望福利；精确最低2785/297。独立内部精确核验通过，不改变一般半覆盖或真正聚合静态安全值的开放状态。

新增机制边界：[`CA-FRACTIONAL-ACTUAL-LOAD-WEAK-NO-v1`](../current/customer_attraction/fractional_actual_load_counterexample.md)对每个m≥4给出四主题完整SPE无限族，否定原正桥`CA-FRACTIONAL-ACTUAL-LOAD-WEAK-v1`；该无限族本身不否定精确实际税充分桥。后者已由[既存13人36客户完整SPE](../workspaces/customer-attraction/R-c50fecc37aa44fb4a69a2122bb70e5fe/security/refined_tax_counterexample.md)独立否定，2026-10-24恢复该状态并精确重放；不能再列为开放候选。半覆盖及真正聚合静态安全值仍OPEN；外审与新颖性未认证。

独立简化版本：[`CA-WORST-CCE-WELFARE-8`](../current/customer_attraction/eight_customer_cce_welfare_gap.md)使用八单位客户、四主题和计数依赖完整策略给W6<min_CCE E[W]=544/87，OPT3=8。它保留原十三客户身份，外审、新颖性和最小性未认证。


新的无界结构子类：`CA-EXTREME-MAXIMAL-THETA-v1` / `CA-EXTREME-MAXIMAL-WELFARE-v1`。若每个客户在k个极大主题中属于1、k−1或k个，则任意合法背景与剩余人数的完整SPE全员有theta保底，并有背景利润界与空背景带核心锐2−1/m界；内部子主题任意。精确身份见[账本](../current/claims.md)，完整证明与独立内审见[正文](../current/customer_attraction/extreme_maximal_membership_floor.md)。这不改变一般目标的OPEN状态。


2026-10-23全成果清洗补入 `CA-IID-WEAK-WELFARE-NO-v1`：[完整SPE反族](../current/customer_attraction/iid_security_and_flow_barriers.md) §1.2否定同定义弱iid桥 `W≥(1−1/(2m))Z_m`；原成果早存个人区，本轮重构并补共享状态，非新发现。真正安全值强/弱聚合及Q-CAG-HALF仍OPEN。

新增候选接口：[`CA-INCIDENCE-LP-DYNAMIC-BUDGET-v1`](../current/customer_attraction/incidence_lp_dynamic_budget.md)把现有极大覆盖路由的统一预算细化为关联覆盖 LP 与后缀包络；`tau_inc <= 2` 的输入类由此得到半覆盖。高密度共享关联仍未闭合，候选尚待独立清洗，不能升级一般目标状态。

## 2026-10-24 Boss9 阶段性一般接口

| ID | 精确范围 | 结论与边界 | 证据 |
| --- | --- | --- | --- |
| `CA-SEQUENTIAL-DEVIATION-SHARES-v1` | 任意有限共同目录、任意 m、任意完整历史依赖纯 SPE；固定实际根路径及任意合法强制主题 | 对每个位置有真实偏离份额下界 `u_i >= |T\\U|/(m-i+1)`，精确式 `u_i >= sum_{x in T\\U}1/(1+q_i(T,x))`，并在后继主题 `R subseteq T` 时有同枝收益继承。最坏分母聚合不足以推出 half；这是一般引理与开放支付接口，不是主命题证明。2026-10-24 已修正文 §4 的另一个算术跳步：遗漏半额付款只给所述账本中的 OPT≤3W，非 half；底层引理不变。 | [`route5a/sequential_deviation_share_lemma.md`](../workspaces/customer-attraction/R-1740705e79f14baba6326b951a52152f/route5a/sequential_deviation_share_lemma.md)；[勘误审查](../workspaces/customer-attraction/R-65d0f88edf3849b39ca5eb79760e970b/parent/route5a_independent_review.md)，未外审 |
| `CA-CROSS-BRANCH-RELAY-v1` | 原称任意完整历史节点、任意强制主题 T 与原策略动作 A* | **FALSE（通用非根版本）**：原结论 `ΔW<=ΔV` 漏掉旧玩家最终利润变化；两人三客户完整 SPE 有 ΔW=1、ΔV=0。根特例仍正确，原 claim 量词不暗改为根。删位势比较 R2 独立成立，不能再称与该错误福利式无条件等价。 | [原稿勘误](../workspaces/customer-attraction/R-1740705e79f14baba6326b951a52152f/representation/cross_branch_welfare_relay_identity.md)、[既有完整反证与审查](../workspaces/customer-attraction/R-cef41b80a6e048b5a395b738d3b0b6e7/harmonic/relay_erratum.md)；正文先前已修，本轮纠正滞后的本账本 |
| `CA-CROSS-BRANCH-RELAY-v2` | 任意完整历史节点、任意强制主题 T 与原策略动作 A*；P 为早期玩家最终利润，V 为后继最终利润，Γ 为当前玩家不偏离的非负收益差 | `ΔW=ΔV+ΔP−Γ<=ΔV+ΔP`。旧 `ΔW<=ΔV` 对某项比较成立恰当且仅当 ΔP≤Γ。根 P=0；一般非根不能删 P。R2 删位势比较继续独立有效；尚无跨互斥子树共同支付，不推出 half。 | [修正正文 R1-v2/R2](../workspaces/customer-attraction/R-1740705e79f14baba6326b951a52152f/representation/cross_branch_welfare_relay_identity.md)、[既有独立审查](../workspaces/customer-attraction/R-cef41b80a6e048b5a395b738d3b0b6e7/exchange/relay_correction_review.md)；非本轮新机制，未外审 |
| `CA-STATIC-SMOOTHNESS-SPE-BRIDGE-NO-v1` | 任意静态终局与顺序 CAG 的完整纯 SPE | 静态终局满足 (1,1)-smoothness，静态 PNE 因而满足半覆盖；完整三人 SPE 证书显示冻结静态偏离收益不能替换真实后继收益。只否定该桥，不否定主命题。 | [`smoothness_bridge_obstruction.md`](../workspaces/customer-attraction/R-1740705e79f14baba6326b951a52152f/route3/smoothness_bridge_obstruction.md)；完整有限证书与审计，未外审 |
| `CA-PAIR-INCIDENCE-LP-OBSTRUCTION-v1` | 完整 pair-incidence 目录 K_s，s >= m >= 2；单偏离、单一非负关联乘子模板 | 根 LP 对偶精确 `B(m)=ms/2`，不能单独利用最优解至多选 m 个主题；这是证明接口障碍，不是低福利 SPE 或 Q-CAG-HALF 反例。 | [`complete_pair_incidence_lp_obstruction.md`](../workspaces/customer-attraction/R-1740705e79f14baba6326b951a52152f/representation/complete_pair_incidence_lp_obstruction.md)；解析对偶计算，未外审 |
| `CA-HARMONIC-BRANCH-DELETION-OBSTRUCTION-v1` | CAG-MODEL，三人、六共同主题、四单位客户及完整有序历史纯 SPE | 精确恒等式 `u_i=Phi(z)-Phi(z^{-i})` 成立，但完整 SPE 不保证强制分支调和势逐点不降；43 个历史、215 个偏离的证书给实际路径 `(T1,T3,T4)` 与强制根 `T0` 的势差 `-1/2`。见证 `W=OPT_3=4`，只否定该潜势归纳接口，不否定 Q-CAG-HALF。 | [`potential_branch_obstruction.md`](../workspaces/customer-attraction/R-1740705e79f14baba6326b951a52152f/route1/potential_branch_obstruction.md)；精确全历史核验，未外审 |

## 个人阶段强化合同的精确反证索引

`B18-LOCAL-REFUND-v1/v2`（正文别名`ONCE-REFUND-FLOOR`）已FALSE：原模型任意根完整SPE，实际C，最优联合O，D=O\C，f_D(r)为r主题在D上的最大覆盖，e_i=Σ_(x∈B_i\O)1/c_B(x)。v1要求每个O及每个实际i都有u_i+e_i>=f_D(m-i+1)−f_D(m-i)；v2只要求存在同一O使全部i成立。唯一最优179客户完整SPE同时反驳两版本：u=(34,35,38)，W107，OPT111，e=(34,0,34)，f_D=(0,36,72,72)，倒二35<36。全部57有序节点399比较及唯一最优性已有作者、独立盲核和父方另路单位客户审计。其充分性求和正确，但前提为假；跨角色信用和原half仍未解决。完整Objects/Domain/Quantifiers/Definitions/Dependencies/Evidence/Objections及来源在[个人精确账本](../workspaces/customer-attraction/R-b659ddeec819493bb10dc58441fa7b3d/CLAIMS.md)，[自足反例](../workspaces/customer-attraction/R-b659ddeec819493bb10dc58441fa7b3d/refund/unique_optimum_refund_floor_counterexample.md)从旧71客户机制派生。此索引用于避免重走已反驳的合同，不表示正式共享成稿、外审或全球新颖性认证。
