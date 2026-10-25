# 当前精确身份

用户本轮目标HALF(5)已由原上传证明CA-FIVE-HALF-EXACT-v1闭合，并经本团队复跑和独立审查。当前[精确身份](round8_five/CLAIMS.md)及[完整复核](round8_five/imported_half5_check/README.md)区分来源与本轮贡献。一般人数仍OPEN，无外审/新颖性认证。

以下旧一般Claim按各原量词保存。

# 历史接续入口

[round5_general/CLAIMS.md](round5_general/CLAIMS.md) 登记实际末位保税比较推论及未证 WEAK-LAST 付款；Q-CAG-HALF 仍 OPEN，没有新无条件福利界或目标反例。

[round4_general/CLAIMS.md](round4_general/CLAIMS.md) 区分自洽真实负载查询的连续性存在事实与未证共同付款。Q-CAG-HALF 仍 OPEN，暂无新无条件福利下界或目标反例。

[round3_general/CLAIMS.md](round3_general/CLAIMS.md)登记本轮两项经独立内部审查的辅助反例与仍OPEN的STATIC-2候选。Q-CAG-HALF没有一般证明、目标反例或新增全输入福利下界。以下旧Claim按原范围保留，不重复认领。

# 精确命题身份（个人区）

## CA-PREFIX-COUPLED-SEAT-BUDGET-v1

- **Objects/domain/quantifiers：** CAG-MODEL 的每个有限单位客户实例、每个有限非空共同目录、任意 m≥1、每个完整有序历史纯 SPE σ、每个实际位置 i。重复主题、空主题、零客户及任意历史依赖平局保留。
- **Definitions：** C 为同一 σ 的固定实际覆盖，B_j 为不同极大覆盖，Q_j 为 B_j 中实际遗漏的全局私有块。冻结该位置真实负载 b、r=m−i+1。G_j(k)=|Q_j|/k+Σ_(B_j\Q_j)1/(b_x+r)。F_j(k) 对 r−1 个合法竞争主题中至多 k−1 个触及 Q_j 的完整根收益取极小，1≤k≤r；Λ_i、λ_i 分别为 F、G 全部席位的第 r 大。
- **Conclusion/scope：** u_i≥Λ_i≥λ_i，W≥Σ_iΛ_i≥Σ_iλ_i；λ_i 逐位置不弱于旧实际遗漏私有谱与直接分母保底的最大值，且有完整 SPE 的严格增强例。全部 Q_j 为空时 F=G，退回直接分母保底。
- **Dependencies：** 既有超集席位机制、固定实际遗漏的零触块计数、单位玩家同叶包含支配、全部有序历史的真实偏离 IC；没有调用原 half 或 SPE 删除/冻结桥。
- **Evidence/status：** 自足一般解析证明；induction 先只见 G 陈述独立重构，再读稿审 F；root 定义级重构。menu 独立展开单位客户、重构完整策略并复算严格增强例，root 重跑该标准库审计通过。内部检查完成，未外审、未认证全球新颖性。
- **Objections/open obligations：** 无已成立的本引理致命异议；未证明 ΣΛ_i≥OPT_m/2 或 OPT_m−W≤ΣΛ_i。没有改变 Q-CAG-HALF 的 OPEN 状态或扩展原命题已证范围。
- **Related files：** continuation_general/omission/prefix_coupled_seat_budget.md、induction/private_offset_spectrum_independent_review.md、menu/refined_spectrum_numerical_review.md 及相邻实际脚本/JSON；共享工作稿 general_half_proof.md §3.1。

## ROOT-ONLY-REPAIR-3-v1

- Objects/domain/quantifiers：每个原CAG-MODEL实例、每个m>=2、每个完整纯计划tau，其在每个正深度子局已为SPE；根A不必最优。全部有序历史、重复/空主题、任意历史平局保留。
- Definition：u为实际根收益，d_B为按原tau完整后继的真实根偏离收益，Delta=max_B d_B−u>=0。给定有理s>=Delta且s>0。
- Conclusion：存在同m单位提供者、合法新共同Cartesian目录的完整纯SPE，旧坐标实际路径不变；W_new=W_old+(m+1)s、OPT_new=OPT_old+(2m−1)s、gap_new=gap_old−3s。有理账面数共同整数缩放成单位客户。Delta=0时旧计划已经SPE，无需修复。
- Dependencies：分支后独立Cartesian收益可加，H/L_X/L_Y/leaf-BI完整续局，最优组合可按位置同时配对。
- Evidence/status：自足一般证明及作者Fraction联合全树核验；independent/insurer_blind_review.md独立盲重构与定义级回放未发现致命异议。内部解析可靠，未外审/未认证新颖性；非Q-CAG-HALF解答。
- Related：compiler/padded_insurer_{statement,repair}.md、audit_padded_insurer.py/.json、independent/insurer_blind_*。

## ROBUST-ROOT-ONLY-3-EQUIV-v1

原Q-CAG-HALF（对所有共同目录，固定任意m>=2）等价于：每个上述root-only计划均满足OPT_old<=2W_old+3Delta。正向对Delta>0应用ROOT-ONLY-REPAIR-3-v1、取s=Delta并清分母；Delta=0直接用原命题。反向在完整SPE取Delta=0。该等价不证明任一边；当前状态OPEN等价重述，不冒充新half机制。

## 其他资产的实际审查状态（以下历史待审文字以对应审查记录为准）

compiler/disjoint_insurer_three_sharp.md（准确架构三系数锐下界）、shared_omission/credible_degree_two_negative_flux.md（真实完整SPE无条件驻留负flux）各以正文量词为准，审查未完成时保持作者结果身份。

## DISJOINT-INSURER-DILUTION-3-v1

- Domain：每个m>=2，所有合法主题共同含K，去K后不同极大花瓣两两不交，任意内部子主题；固定同一根A，任意两份完整后继SPE。
- Definition/conclusion：高/低首人收益差delta>0，高分支福利W_H，同保险OPT_m=O，则2W_H−O>=|K|+3delta；每个m都有达到3delta的空核例。任意fixed-root后继分支另有2W−O>=0，允许任意多独立此类坐标异号求和得到修复成本>=3Delta。
- Status：作者一般证明、independent/insurer_three_sharp_review.md独立内部解析攻击及Fraction复核通过；不含根可遗漏的极大共同核，不含根以下跨坐标耦合。无外审/新颖性认证。

## DEG2-CREDIBLE-NEG-FLUX-v1

- Domain：q>=2、m=q+1、2q极大主题，两等组；每条跨组边b>=1单位客户、同组边整数0<=a<=b单位客户；完整全历史纯SPE。
- Conclusion/evidence：存在正文明确SPE，根L=theta=qb/2+(q−1)a、各后继H=(q−1/2)b+(q−1)a/2、均匀驻留根尾差−(q−1)(b−a)/2，W=OPT。a>0,q>=3时另有最优比较集共享遗漏D=G=a*binom(q−1,2)>0。
- Status：full_depth/degree_two_review.md独立解析审查通过；已修正1–1平局取最近动作组，代码原本正确。仅否定无条件根尾平均支付，根不严格低于theta。无外审/新颖性认证。

## STATIC-CROWDING-DOMINATION-v1

任意incidence、任意合法背景、r=q+1个剩余者和同一完整SPE的真实强制极大根菜单。h_x=max_{i∈I_x}K_i(x)。若q个整数合法静态槽p使c_p(x)>=h_x，则theta_r(b)<=max_i d_i<=u。degree2为顶点多重覆盖。root独立通分和单位客户核对通过（parent/static_crowding_review.md）。普遍存在这样的p已经被K5三人真实SPE需求C5、覆盖成本3>q2否定；一般half/degree2 theta仍OPEN。

## POPULATION-DELETION-ALL-v1

每个m>=2取偶t>=4、d>=1、整数0<epsilon<t/2，L=d+(m+1)t/2+epsilon；m个不交L块Ai及从各块取t并含d私有的T。全部m人完整SPE实际各Ai一次，W=OPT=mL，联合U；每个1<=s<m全部SPE均根T后fresh不同块，故全部覆盖U外私有。任意历史/重复均保留。security/population_review.md独立内部解析审查通过。新增是统一全人数/全部较少人数/原均衡最优范围，不认领首次否定固定人数联合删除。

## SECURITY-OPT-REAL-TAIL-GAP-v1

每个m>=2，复用旧两core稀有叶静态实例，存在指定安全最优均匀叶p*，对每份完整SPE及每个强制根a，其m−1真实尾列B(a)满足F_p*(B(a))>=v_m+m/[4(m+1)]。同族每个真实历史下当前及未来SPE行动者收益>=v_m，OPT_m=3m²。independent/strict_tail_review.md独立内部审查通过。存在指定p*不扩大为任意p*；尾列不含根，未否定Mfull或聚合安全值。无外审/新颖性认证。

## 仍开放/仅观察

B2两步安全债务非负仍OPEN；有限诊断及固定p,Q策略锥未命中不作一般证据。祖先cap reset递推是精确集合值BI的带条件重述，不能自动形成福利机制。所有Finite JSON范围见各正文，均非计算证明原half。


2026-10-23清洗同步：常数三锐性和负flux的独立内部审查已经完成，分别见`independent/insurer_three_sharp_review.md`、`full_depth/degree_two_review.md`。本轮一般关系稿另见共享`research/reviews/customer_attraction/general_research_curation.md`；无新增外审或一般half证明。

## 第六次接续的个人精确身份

全阶擦除、损失势、终局嵌套、真实floor付款的窄反例，以及已知末两行去相关接入，见[round6账本](round6_general/CLAIMS.md)。证明与独立内审已有记录，外审和新颖性未认证；没有升级一般half或共享负载/统一价格候选。

## 第七次精确身份

见[round7账本](round7_general/CLAIMS.md)：一般共同后继帽、全参数纯退出、signed费用改善、有限真实字典LP及边界分开。全部强制含own和full-history已独立检查；外审/新颖性未认证。没有将实际金额改善称为一般half闭合。
