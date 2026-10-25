# 顺序客户吸引成果总账：一般组件、条件结论、开放义务与桥梁边界

**读取范围更新：** 下文为原截止分类及明确增补，不是随HEAD自动完备的真值快照。下一轮从[短接续材料](SYNTHESIS.md)和[当前前沿](RESEARCH_STATE.md)进入；五人557行独立已审上界强于下表437行，旧值不能再无限定称“当前最佳”。本轮不重新审完全部正文。

本轮补齐的路由：[最优首动作真实孩子缺口](../current/customer_attraction/optimal_first_action_branch_gap.md)为已有全范围恒等式，跨孩子正项仍未支付；[关联LP动态预算](../current/customer_attraction/incidence_lp_dynamic_budget.md)仍为待独立清洗候选，不因进入current升级。冻结实际前缀的P+λΔ整体归纳已被[52客户完整证书](../workspaces/customer-attraction/R-5c4f6385eec046eb9a20052facacba11/background/global_actual_prefix_counterexample.md)否定。

盘点基线：2026-10-23，`69e6012bd585e1e1b53b7535a1cff661fe35a855` 同步后的实际文件，并纳入整理过程中新增的 `general_half_proof.md`。覆盖 `research/current/customer_attraction/` 的 **71份数学/定义/文献/衔接正文及1份README**，并对照 `research/current/claims.md`、`research/customer_attraction/CLAIMS.md`、`research/review_status.json` 和 `research/assets.json`。正文声明、命题量词、来源证明、内审、外审与实现保持独立；本轮是分类和登记核对，**没有重新审完全部证明，也不提升任何审查等级**。

唯一继续研究的目标是原 **Q-CAG-HALF**：有限单位客户、有限非空共同目录、任意人数m、每个完整有序历史纯SPE均满足 `2W>=OPT_m`；允许空主题、重复选择、零客户与任意历史依赖平局。它仍 **OPEN**，没有完整一般证明或真正目标反例。当前授权只攻一般m、一般目录；下列条件目录、固定人数和局部常数成果保留供引用与提取一般组件，**停止把扩张这些特殊范围作为研究任务**。特殊实例只用于检验一个明确的一般候选。

## 审查字段怎么读

下表“审查”忠实压缩现有五轴登记，不表示本轮新复审：

| 记号 | 现有登记的准确含义 |
|---|---|
| E | `current_proof=complete`，`internal_review=current_exact_audit`。具体独立解析重构/定义级核验范围回正文与审查资产，不把该字段自动解释为全部证明已外审。 |
| M | `current_proof=complete`，`internal_review=multiple_audits`。多路内部检查，仍非外部同行认证。 |
| C | 条件提升接口登记 `current_proof=conditional`、`internal_review=multiple_audits`；明确条件下的代数推导已内审，普遍满足该条件未证。 |
| S | 来源证明完整并获独立内审；现行正文登记 `depends_on_claims`，只给依赖概述，不能将现行概述冒充完整系数证明。 |
| D | 定义或文献范围核对，不是另一个新定理的证明等级。 |
| X | 正文有独立Fraction机制审计与冻结证据，但未在 `current/claims.md` 找到独立对应命题行；不补造身份或等级。 |

本次读到的CA命题登记中，`external_review` 均为 `not_recorded`；各自新颖性、最小性和尖锐性仅在正文明确证明时使用。基线 `research/assets.json` 对原71份文件均有proof路径覆盖，无漏映射或失效proof路径；新增衔接工作稿已在资产合同以`customer_attraction_general_half_working_account`登记，状态为不完整工作稿、已证关系及范围内部复核；不因被本账纳入就提升其证明等级。总资产包状态不替代每个命题的精确范围。

## 一、全范围正向定理与实际证明组件

这里的“全范围”指不限制原目录或总人数的陈述/参数化组件；它不意味着一般half已经成立。固定尾部人数的组件另在第二类明确列出，避免把局部尾部定理写成全体玩家保底。

| 完整正文路径及身份 | 精确已证范围与结论 | 依赖、用途与剩余限制 | 审查 |
|---|---|---|---|
| [一般证明工作稿§3.1](../current/customer_attraction/general_half_proof.md#31-冻结真实前缀的联合客户席位一般付款的精细加强)；`CA-PREFIX-COUPLED-SEAT-BUDGET-v1` | 任意原实例、每个完整历史纯 SPE、每个实际前缀：完整利润席位 F 与显式前缀价格席位 G 给 `u_i≥Λ_i≥λ_i`、`W≥ΣΛ_i≥Σλ_i`。 | 新的同利润耦合精细化，承接既有超集席位归纳；严格加强旧私有谱/分母界的逐位置最大值。Q全空时两谱都退回分母界，尚不支付一般 half。 | E；G先盲重构、F随后读稿核对，另一实现补全严格例全部策略并逐历史审计；无外审或新颖性认证 |
| [research/current/customer_attraction/last_two_floor.md](../current/customer_attraction/last_two_floor.md)；`CA-LAST-TWO-FLOOR`、`CA-ALL-N-WELFARE-4N` | 任意总人数n>=2，任意完整历史的末两人各有局部theta保底；合并最大主题保底得 `W>=4(n−1)OPT_n/[n(2n−1)]`。 | 真实末位最佳回复、两人配对势差；一般弱福利界，不能把theta保底扩大到全部玩家。n>=5未达half。 | E |
| [research/current/customer_attraction/tail_profit_lift.md](../current/customer_attraction/tail_profit_lift.md)；`CA-TAIL-FOUR-ALL-N` | 任意目录、n>=4、全部纯SPE：`OPT_n<=(n/2−1/750)W`；另给固定k尾部利润定理的合法组合接口。 | 依赖四人**背景剩余利润**界、最优主题索引子集比较与实际前缀税；没有使用已否定的一般根税。常数随n增长，不是half。 | M；实现登记none |
| [research/current/customer_attraction/oblivious_security.md](../current/customer_attraction/oblivious_security.md)；`CA-OBLIVIOUS-MIXED-SECURITY-2N1` | 任意m与目录，静态对手不观察随机查询，`v_m(0)>=OPT_m/(2m−1)`，下界锐。 | 静态minimax比较定理；实际后继能观察偏离，从v到W仍须另证聚合桥。 | M |
| [research/current/customer_attraction/fractional_cover_path_budget.md](../current/customer_attraction/fractional_cover_path_budget.md)；`CA-FRACTIONAL-COVER-PATH-BUDGET` | 任意比较客户集C、分数覆盖总重tau、真实位置i及r=m−i+1：`|C|<=P_(i−1)+r tau u_i`；迭代得 `W>=|C|[1−prod_(r=1)^m(1−1/(r tau))]`。 | 真实偏离的负载上界和同一实际终局的旧玩家最终利润；P不能换成离轨旧玩家利润。tau无界仍不支付一般half；条件推论见第二类。 | E；正文记两路独立逐客户审查 |
| [research/current/customer_attraction/uncovered_private_seat_spectrum.md](../current/customer_attraction/uncovered_private_seat_spectrum.md)；`CA-ACTUAL-PRIVATE-SEAT-SPECTRUM-v1` | 任意实例/SPE，固定实际未覆盖的极大全局私有块，以真实触块次数定义席位；每个位置有对应谱保底，W支付前m大席位和。 | 有限极大元、同终局包含支配和全历史归纳；新的触块计数不能当作旧路由计数。一般预算成立，但未支付共享遗漏；条件锐界见第二类。 | E；盲独立解析重构与有限回放 |
| [research/current/customer_attraction/dynamic_maxima_bound.md](../current/customer_attraction/dynamic_maxima_bound.md)；`CA-DYNAMIC-MAXIMA-FLOOR`、`CA-DYNAMIC-MAXIMA-MIXED` | 任意极大主题数s>=2、任意人数n的全历史路由保底；`D_t=max{t+s(n−t)/2,n+s−1}`，每位 `u>=c/n+(U−c)/D_t`，故 `W>=c+(U−c)sum_t1/D_t`；另有私有/共享混合包络。 | 全主题归属一个包含极大元、真实中继支配、客户关联计数。s可增长，参数化预算不自动给一般half。少极大结论见第二类。 | M |
| [research/current/customer_attraction/sunflower_maxima_bound.md](../current/customer_attraction/sunflower_maxima_bound.md) §8；`CA-MAXIMA-SUPERSET-SEATS` | 任意目录、任意人数，按全局私有量与其余客户量构造superset席位，前缀剩余席位条件给逐人保底及根 `W>=m nu`。 | 同终局包含比较及真实后继归纳；一般共享并集预算未闭合。本文主福利定理仍要求sunflower，见第二类。 | M |
| [research/current/customer_attraction/three_maxima_bound.md](../current/customer_attraction/three_maxima_bound.md) §2 | 其中带核心的通用superset席位引理不限制极大主题数；真实前缀有足够剩余席位即给每个剩余人对应保底。 | 这是sunflower通用席位机制的带核心版本；三极大全并集收费部分有额外条件。 | M |
| [research/current/customer_attraction/two_remaining_tax.md](../current/customer_attraction/two_remaining_tax.md) §6；`CA-LAST-NODE-OPT-TAX` | 任意m、只需实际末位最佳回复的终局，`OPT_m<=m u_m+tau_0(c_<m)`。 | 逐客户末位查询求和；末位不高于平均时可推出根税，但不能据此无条件推出根税或half。恰两人税另列第二类。 | E |
| [research/current/customer_attraction/continuation_lemmas.md](../current/customer_attraction/continuation_lemmas.md) 末节 | 任意合法前缀、剩r人，当前收益至少 `max_T sum_(x in T)1/(b_x+r)`。 | 真实偏离分母的普遍上界；不冻结后继。该文件主体的残余/匿名/静态桥反例另列第五类。 | E（相关登记与独立定义级审计） |
| [research/current/customer_attraction/iid_security_and_flow_barriers.md](../current/customer_attraction/iid_security_and_flow_barriers.md) §1；`CA-IID-SECURITY-BENCHMARK` | 任意目录/人数的静态凹调和势最大者恰为对称混合Nash；其iid期望覆盖Z唯一且 `m v_m<=Z_m<=OPT_m`。 | 凹势、KKT、二项式恒等式；静态结论完整。强 `W>=Z_m` 与弱 `W>=(1−1/(2m))Z_m` 均已被反驳；真正v的强/弱聚合桥仍OPEN，不能将静态基准写成SPE福利定理。 | M |
| [research/current/customer_attraction/fractional_tail_waterfill.md](../current/customer_attraction/fractional_tail_waterfill.md)；`CA-FRACTIONAL-TAIL-WATERFILL-v1` | 任意非负整数背景、保留单位根、有限单位尾主题、阈值t>=0，存在同一分数尾权，使全部主题查询增益共享一个信用池 `H<=sum_j(t−u_j)_+`，且根/背景返还和尾质量利润精确守恒。 | **给定终局的代数引理，不要求也不产生SPE。** 辅助权一般无理，不是新的单位玩家实例；降权后不能直接调用单位玩家SPE归纳，跨真实树支付仍缺。 | E；盲独立重构、边界审计 |

## 二、有附加条件或固定人数的已证成果：保留，停止扩张

这些定理在其原范围内继续有效。此分类不把“已证明”降为猜想，也不授权继续补特殊人数、增极大数或调局部常数。

| 完整正文路径及身份 | 精确范围与已证结果 | 依赖/可复用部分与边界 | 审查 |
|---|---|---|---|
| [research/current/customer_attraction/three_player_sharp.md](../current/customer_attraction/three_player_sharp.md)；`CA-THREE-SHARP-5-3` | 恰三人、任意目录、全部完整纯SPE：`OPT_3<=(5/3)W`，有匹配下界。 | 真实L_i/Q/R回复、非负恒等式；不构成任意人数归纳链。 | M |
| [research/current/customer_attraction/three_player_bound.md](../current/customer_attraction/three_player_bound.md)；`CA-THREE-UPPER-142-81` | 恰三人旧界 `OPT_3<=(142/81)W`。 | 固定背景两人税到根覆盖的独立机制保留；不是当前最佳三人界。 | M |
| [research/current/customer_attraction/four_player_bound.md](../current/customer_attraction/four_player_bound.md)；`CA-FOUR-UPPER-1499-750` | 恰四人、空根背景、任意目录：`OPT_4<=(1499/750)W<2W`；未证锐。 | 原完整策略的根偏离及后继自身比较，不冻结后继。 | M |
| [research/current/customer_attraction/five_player_bound.md](../current/customer_attraction/five_player_bound.md)；`CA-FIVE-UPPER-221-100` | 恰五人：系数 `24236714656727/10967499015623`，约2.209867，仍>2。 | 两条真实中途偏离、恰两人税组合；上界不是低效SPE实例。 | M |
| [research/current/customer_attraction/five_player_reply_bound.md](../current/customer_attraction/five_player_reply_bound.md)；`CA-FIVE-REPLY-UPPER` | 恰五人：系数 `493266145873827/234749688354196`，约2.101243，仍>2。 | 三个真实末位菜单及匹配项消去；保留独立机制，不作当前最佳界。 | M |
| [research/current/customer_attraction/five_player_indexed_bound.md](../current/customer_attraction/five_player_indexed_bound.md)；`CA-FIVE-INDEXED-UPPER` | 恰五人共享旧437行界：beta=`145473820534756099649387160645076613709/70560308704423797361284609157664425493`，约2.061695>2。 | 保留真实索引回复与联合直方图；437行模板精确最优仍不等于原游戏最坏比例。 | M |
| [research/current/customer_attraction/three_remaining_profit_bound.md](../current/customer_attraction/three_remaining_profit_bound.md)；`CA-THREE-REMAINING-PROFIT-5-3` | 任意合法固定背景、恰三名剩余人：同背景最优剩余利润 `F_3(b)<=(5/3)P_tail`，统一常数锐。 | 三人真实回复恒等式加背景校正；剩余利润不是全局覆盖，可供一般尾部提升。 | M |
| [research/current/customer_attraction/four_remaining_profit_bound.md](../current/customer_attraction/four_remaining_profit_bound.md)；`CA-FOUR-REMAINING-PROFIT-1499-750` | 任意合法固定背景、恰四名剩余人：`F_4(b)<=(1499/750)P_tail`；未证锐。 | 真实D/Q/R/S节点及背景聚合校正；一般提升只能用此背景版，不能裸搬空背景根证明。 | M |
| [research/current/customer_attraction/two_remaining_tax.md](../current/customer_attraction/two_remaining_tax.md)；`CA-TWO-REMAINING-TAX` | 任意固定合法背景、恰两剩余人、任意比较主题对：最优比较剩余利润不超过实际剩余利润加倒二主题的局部税。空背景重构3/2。 | 三条真实比较及对称交叠恒等式；一般首步税和总税均不能由此递推。 | E |
| [research/current/customer_attraction/global_new_uniform_portfolio_two.md](../current/customer_attraction/global_new_uniform_portfolio_two.md)；`CA-UNIFORM-PORTFOLIO-TWO` | 任意背景、恰两剩余人、两个比较主题：`2R_b(T,S)<=P_tail+V1T+V1S+V2T+V2S`。 | 四个真实末节点slack及背景多项式；任意人数平均支付未证。 | M |
| [research/current/customer_attraction/disjoint_maxima_bound.md](../current/customer_attraction/disjoint_maxima_bound.md)；`CA-DISJOINT-MAXIMA-2M1` | 删除**全目录共同核心**后不同极大花瓣不交，任意人数：带核心锐 `2−1/m` 界；该范围每历史只选极大花瓣。 | singleton席位和真实扩张续局；不能把结论中的“每步极大”无条件外推到一般sunflower内部主题。 | M |
| [research/current/customer_attraction/sunflower_maxima_bound.md](../current/customer_attraction/sunflower_maxima_bound.md)；`CA-SUNFLOWER-MAXIMA-2M1`、`CA-SUNFLOWER-PRIVATE-GAP` | 极大覆盖为sunflower、内部子主题任意，任意人数：`OPT<=c+(2−1/m)(W−c)`，锐。只有额外“非极大遗漏私有客户”条件才推出每历史只选极大主题。 | superset席位；允许内部主题遗漏极大共同核心。福利结论不依赖额外private-gap假设。 | M |
| [research/current/customer_attraction/laminar_incidence_bound.md](../current/customer_attraction/laminar_incidence_bound.md)；`CA-LAMINAR-INCIDENCE-THETA`、`CA-LAMINAR-INCIDENCE-MAXIMA-2M1` | 客户的极大主题关联集合成laminar家族，内部子主题任意；任意n人实例的每个合法前缀，全部剩余人各>=该实例全局theta_n；空根有带核心锐 `2−1/n` 界。 | 层级席位/真实包含中继；不将全局theta_n重写成任意背景的新局部theta_r(b)定理，不是一般交叠目录。 | M |
| [research/current/customer_attraction/extreme_maximal_membership_floor.md](../current/customer_attraction/extreme_maximal_membership_floor.md)；`CA-EXTREME-MAXIMAL-THETA-v1`、`CA-EXTREME-MAXIMAL-WELFARE-v1` | k个极大主题可无界，每个客户关联数仅1、k−1或k；任意合法背景/人数全员theta保底，并有背景利润及空根带核心锐 `2−1/m` 界。 | 最小人数反证、真实中继、驻留逐客户支付；真正中间关联未覆盖。与laminar类不可比。 | E；盲独立解析重构 |
| [research/current/customer_attraction/three_maxima_bound.md](../current/customer_attraction/three_maxima_bound.md)；`CA-THREE-MAXIMA-HALF` | 至多三极大任意人数half；n>=2还给全并集 `U<=2W−c`；单极大与n=1单独处理。 | 共享加权静态席位；一般组件见第一类。 | M |
| [research/current/customer_attraction/dynamic_maxima_bound.md](../current/customer_attraction/dynamic_maxima_bound.md)；`CA-FIVE-MAXIMA-HALF` | 至多五极大、任意人数half；n>=5给 `U<=2W−c`；至多四极大强化的n范围按正文。 | 通用动态保底、混合包络及已有小人数定理；不外推到无界极大数。 | M |
| [research/current/customer_attraction/six_maxima_joint_bound.md](../current/customer_attraction/six_maxima_joint_bound.md)；`CA-SIX-MAXIMA-HALF` | 至多六不同极大覆盖，任意关联/私有块/内部子主题，任意人数half；n>=5给 `U<=2W`。 | 动态混合保底、真实末位、两人税与实际会员联合预算；不普遍多减一个共同核心。 | M |
| [research/current/customer_attraction/six_maxima_no_private.md](../current/customer_attraction/six_maxima_no_private.md)；`CA-SIX-MAXIMA-NO-PRIVATE-HALF`、`CA-SIX-MAXIMA-NINE-PLUS-HALF` | 至多六极大且核心外无全局私有客户：任意人数half，n>=5有 `U<=2W−c`；另不限制私有块时n>=9也有该核心强化。 | 共享查询单调包络、有限有理分支及解析尾部；一般六极大half已另证，本文保留更强条件结论。 | M |
| [research/current/customer_attraction/seven_maxima_checkpoint.md](../current/customer_attraction/seven_maxima_checkpoint.md)；`CA-SEVEN-MAXIMA-N7-PLUS` | 恰七极大、n>=7：来源完整证明 `U=OPT_n<=2W`。n=5、6仍缺明确轨道，不是此定理。 | 来源使用动态混合保底、真实末位与恰两人税，包含解析无限尾部；当前页未重写全部系数。禁止将来源完整降格为仅候选，也禁止将缺失分支算通过。 | S |
| [research/current/customer_attraction/common_penultimate_theme_half.md](../current/customer_attraction/common_penultimate_theme_half.md)；`CA-COMMON-PENULTIMATE-HALF-v1` | m>=3，实际倒二主题A包含于全部更早实际主题时half，目录无界。 | 真实末两人菜单两两比较及早期改A保底；实际路径条件承重。 | E |
| [research/current/customer_attraction/penultimate_few_exceptions.md](../current/customer_attraction/penultimate_few_exceptions.md)；`CA-PENULTIMATE-FEW-EXCEPTIONS-HALF-v1` | 实际倒二A至多被r个更早主题遗漏，r>=1、m>=(r+1)^2+1时half。 | 早期/末位联合收费；平方阈值未证锐，大量遗漏不能沿原乘子无条件外推。 | E |
| [research/current/customer_attraction/fractional_cover_path_budget.md](../current/customer_attraction/fractional_cover_path_budget.md)；`CA-FRACTIONAL-COVER-7-2-HALF` | 某个最优并集C的分数覆盖数tau_C<=7/2时任意人数half；更一般产品<=1/2也充分。 | 依赖第一类前缀产品；m<=4使用已有小人数定理。一般反例必须每个最优并集tau_C>H_m/log2。 | E |
| [research/current/customer_attraction/uncovered_private_seat_spectrum.md](../current/customer_attraction/uncovered_private_seat_spectrum.md)；`CA-OPTIMAL-PRIVATE-OMISSIONS-2M1-v1` | 某个最优并集O的实际遗漏O\C全为极大全局私有客户，则任意人数锐 `OPT<=(2−1/m)W`；已覆盖客户可任意共享。 | 第一类真实遗漏席位谱；条件只约束遗漏，不是全部客户。一般共享遗漏未控制。 | E |
| [research/current/customer_attraction/selected_security_cones.md](../current/customer_attraction/selected_security_cones.md)；`CA-SELECTED-SECURITY-CONES` | 三棵指定完整形式策略的整个非负重数SPE锥有聚合安全证书，部分逐人证书；另五个固定游戏对指定安全最优p完成全部有序SPE预算枚举。 | 共同静态Q及逐类型非负全树证书；固定锥/固定游戏结论，不是任意策略结论。 | M |
| [research/current/customer_attraction/policy_security_checkpoints.md](../current/customer_attraction/policy_security_checkpoints.md)；`CA-NEW-POLICY-CONE-SECURITY` | 保存的21棵完整策略的整个非负重数SPE锥均有 `W>=n v_n`。 | 共同Q和20971个精确客户坐标证书；只限保存策略，不能按其n/标签数扩大范围。同文件逐人反例见第五类。 | E |

## 三、一般候选仍未证明：接口成立不等于桥成立

下列都是对一般m、一般目录的开放义务或可选充分桥。它们可能强于Q-CAG-HALF；未证不等于不可证明，也不是研究必须接受的前提。反例已排除的加强不留在此表。

| 开放义务 | 原路径/依赖及准确状态 |
|---|---|
| 原Q-CAG-HALF：`2W>=OPT_m` | [research/customer_attraction/CLAIMS.md](CLAIMS.md)、[research/questions/customer_attraction_half_coverage.md](../questions/customer_attraction_half_coverage.md)。未得完整一般证明或目标反例。 |
| 真正聚合静态安全值 `W>=m v_m(0)`；较弱充分桥 `W>=(m−1/2)v_m(0)` | [research/current/customer_attraction/security_chain_and_local_boundary.md](../current/customer_attraction/security_chain_and_local_boundary.md)、[research/current/customer_attraction/security_cone_duality.md](../current/customer_attraction/security_cone_duality.md)。静态下界已证；逐人v与聚合theta已反驳，均不否定这两条桥。 |
| 全路径安全债务 `sum D_i>=−v_m(0)/2`，或更强 `sum D_i>=0` | [research/current/customer_attraction/security_chain_and_local_boundary.md](../current/customer_attraction/security_chain_and_local_boundary.md)。精确恒等式 `sum D_i=W−m v_m(0)`已证；局部 `D_i>=0` 和相应更强逐步条件已反驳。 |
| 对每份完整形式策略和最优比较元组，存在全历史非负证书 `2c−o=Gamma^T lambda+r` | [research/questions/customer_attraction_general_handoff.md](../questions/customer_attraction_general_handoff.md)、[research/current/customer_attraction/strategy_cone.md](../current/customer_attraction/strategy_cone.md)。有限Farkas合同成立，但普遍证书存在性/构造未证；不循环用主目标宣称证书存在。 |
| 安全值锥接口对所有完整策略和查询分布均能选共同静态对手与非负全行权 | [research/current/customer_attraction/security_cone_duality.md](../current/customer_attraction/security_cone_duality.md)。固定策略、固定p的minimax/Farkas等价已证；全称支付义务仍未证，指定锥成功不外推。 |
| 只对适当安全最优p建立真实菜单独立查询总支付 | [research/current/customer_attraction/global_security_budget_boundaries.md](../current/customer_attraction/global_security_budget_boundaries.md)、[research/current/customer_attraction/selected_security_cones.md](../current/customer_attraction/selected_security_cones.md)。对**全部p**的总去相关/补偿预算已反驳；选择适当最优p的存在性仍另待证明。 |
| 末回复规范化的有符号旧玩家份额转移能由共同根预算支付；或商空间提升普遍成立 | [research/current/customer_attraction/terminal_reply_transport.md](../current/customer_attraction/terminal_reply_transport.md)、[research/current/customer_attraction/terminal_tie_quotient.md](../current/customer_attraction/terminal_tie_quotient.md)。条件接口已内审；一般净债非负或普遍half拼合未证。保留一个既定早期乘子提升已被反驳，不能重列为开放桥。 |
| 分数水位共同信用与原单位玩家完整策略树的真实偏离共同支付 | [research/current/customer_attraction/fractional_tail_waterfill.md](../current/customer_attraction/fractional_tail_waterfill.md)。同一信用池及利润守恒成立；降权后SPE继承、跨根补偿和一般half/GAP支付均未得出。 |
| 含根额外一槽的全路径混合 `M_path<=W/m` | [research/current/customer_attraction/general_half_proof.md](../current/customer_attraction/general_half_proof.md) §8是衔接说明，原义务在所链接工作区。每列是合法m槽静态背景，故菜单值>=v_(m+1)；聚合SPE支付仍未证。逐位置加强 `M_i<=u_i` 已由下述零根保险族反驳；产品闭包的兼容性等价不提供统一位置权的存在性。 |
| 所有仅根可能不最优的root-only计划满足 `OPT_old<=2W_old+3Delta` | [research/current/customer_attraction/general_half_proof.md](../current/customer_attraction/general_half_proof.md) §9与其根修复来源。常数三修复把该稳健预算与原half联系；等价表示本身不证明任一边，不把root-only计划当作完整SPE。 |

## 四、辅助表示、计算、条件提升与文献工具

这些资产回答精确计算、表示或条件等价的问题；不得以“工具正确”“有限证书通过”替代一般福利命题。

| 完整正文路径 | 精确合同与用途 | 审查 |
|---|---|---|
| [research/current/customer_attraction/model.md](../current/customer_attraction/model.md) | 原CAG-MODEL；完整有序历史纯SPE、单位客户均分、共同有限目录及OPT定义。与主动客户设施NE模型分离。 | D |
| [research/current/customer_attraction/literature.md](../current/customer_attraction/literature.md) | 一手文献与模型导入边界；静态valid-utility/Shapley结论不能直接导入顺序SPE。含SPE非PNE有限证书，另见第五类。 | 文献D；证书E |
| [research/current/customer_attraction/literature_followup.md](../current/customer_attraction/literature_followup.md) | 2026-10-09检索与原文量词复核：两人证明的目录条件、set-packing排斥收益、短视多轮BR时间模型。检索未得不构成不存在或新颖性证明。 | D；无独立CA命题行 |
| [research/current/customer_attraction/exact_solver.md](../current/customer_attraction/exact_solver.md)；`CA-EXACT-PURE-SPE-ALL` | 集合值BI精确返回任意有限实例每前缀全部纯SPE终局，能重构覆盖全部有序历史的完整策略；集合按计数缓存不强制同计数节点同回复。非位多项式、非混合SPE。 | E；规范实现implemented |
| [research/current/customer_attraction/credible_continuations.md](../current/customer_attraction/credible_continuations.md)；`CA-CREDIBLE-CONTINUATIONS` | 非极小可信孩子菜单覆盖全部完整SPE；默认极小续局只足以实现终局全集，不枚举所有形式策略。联合MILP产生候选，具体策略锥结论只限其固定空间。 | E |
| [research/current/customer_attraction/strategy_cone.md](../current/customer_attraction/strategy_cone.md)；`CA-STRATEGY-CONE` | 固定完整形式策略的SPE客户重数恰为有理锥；W=1紧截面、固定(m,p)有理达到性与Farkas证书。缺少真实行的松弛不属于此合同。 | E |
| [research/current/customer_attraction/coverage_moment_geometry.md](../current/customer_attraction/coverage_moment_geometry.md)；五项CA覆盖矩身份 | 对任意固定m,p，收益/覆盖资料等价于至多m主题并集矩；任意策略末层比较span含全部非公共方向；非负类型列仍全为极射线；可依实例有理稀疏到d种类型。 | E；正文独立解析重构与精确审计 |
| [research/current/customer_attraction/mobius_compiler.md](../current/customer_attraction/mobius_compiler.md)；`CA-MOBIUS-BOOLEAN`、`CA-MOBIUS-FULL-HISTORY-EMBED` | 有符号子集势的唯一反演、非负整数实现条件及充分正偏置的全历史嵌入；重复计数扩张被固定。辅助负客户不是合法输入，嵌入不保效率比。偏置屏障另见第五类。 | M |
| [research/current/customer_attraction/security_cone_duality.md](../current/customer_attraction/security_cone_duality.md)；`CA-SECURITY-CONE-DUAL` | 固定策略、固定有理p的全重数安全支付与共同静态Q/非负全树行证书精确等价；minimax/Farkas的组合接口。不同覆盖标签合同还需存在区分实现w0。 | M；一般桥未证 |
| [research/current/customer_attraction/security_chain_and_local_boundary.md](../current/customer_attraction/security_chain_and_local_boundary.md)；`CA-SECURITY-CHAIN-INTERFACE` | 背景安全值单调嵌入和真实路径债务望远镜恒等式；末两人控制尾端，不控制所有早期项。开放桥见第三类，局部反例见第五类。 | M |
| [research/current/customer_attraction/dynamic_iid_debt_boundary.md](../current/customer_attraction/dynamic_iid_debt_boundary.md)；`CA-DYNAMIC-IID-DEBT-INTERFACE` | 任意合法背景的静态凹势/KKT、残余iid收益唯一性、前缀租金恒等式和全局债务等价。恒等式 `sum_h D_h=Z_m−W` 保持成立；等价弱iid全局预算 `sum_h D_h<=Z_m/(2m)` 已被完整SPE族反驳，不再列OPEN。 | M（原接口）；弱桥反例见第五类 |
| [research/current/customer_attraction/stationary_pair_transport.md](../current/customer_attraction/stationary_pair_transport.md)；`CA-STATIONARY-PAIR-TRANSPORT` | 任意真实末两人回复图循环给共同静态背景Q和逐类型非负两行恒等式；指定配对模板的全部类型非负余项等价于stationarity。 | M；指定核反例另列 |
| [research/current/customer_attraction/terminal_reply_transport.md](../current/customer_attraction/terminal_reply_transport.md)；`CA-TERMINAL-REPLY-DUAL-LIFT` | 末回复同计数规范化保根覆盖；末行可非负提升，早期误差是有符号旧玩家份额转移；DAG不变量与条件证书提升。规范化后早期不自动仍为SPE。 | C |
| [research/current/customer_attraction/terminal_tie_quotient.md](../current/customer_attraction/terminal_tie_quotient.md)；`CA-TERMINAL-TIE-QUOTIENT-LIFT`、`CA-TERMINAL-TIE-LOCAL-QUADRATIC` | reciprocal真实末行给可付有符号子空间；商空间条件提升与局部二次判别成立，有限成功不等于一般half证书。 | 提升C；局部判别M |
| [research/current/customer_attraction/general_half_proof.md](../current/customer_attraction/general_half_proof.md) | 本轮新增的一般证明衔接**工作稿**：集中真实行、通用前缀产品、静态比较、安全债务、承诺重置、水位与完整菜单/根修复接口，并在未证连接处明确停下。不是一般证明；原引理等级仍回各唯一正文，工作区导入接口也不因重述自动成为已独立审核的新current定理。 | 整理工作稿；不设新的完整证明或外审等级 |
| [research/current/customer_attraction/README.md](../current/customer_attraction/README.md) | 全部现行数学资产导航与跨机制边界；是读取地图，不是新的证明来源。 | D；不设新CA身份 |

## 五、对明确桥梁、模板或表示限制的反例与障碍

这些资产否定的对象以本表写明者为准。完整SPE反例、非SPE分离点、合法路径、固定证书失败与解析编译屏障严格分开；**没有一项是Q-CAG-HALF的反例**。

| 完整正文路径及身份 | 被否定的准确桥/模板；证据对象 | 保留结论与重试边界 | 审查 |
|---|---|---|---|
| [research/current/customer_attraction/continuation_lemmas.md](../current/customer_attraction/continuation_lemmas.md)；`CA-RESIDUAL-NO`、`CA-HISTORY-TIES`、`CA-SPE-NON-PNE` | 两人14客户完整SPE否定逐人/聚合最大实际残余主题保底；三人singleton例否定强制匿名平局及两方向收益单调；三客户证书否定SPE终局必为静态PNE。 | 同计数的**可实现集合**可缓存；实际指定策略不必同回复。真实偏离分母保底保留。 | E |
| [research/current/customer_attraction/literature.md](../current/customer_attraction/literature.md)；`CA-SPE-NON-PNE` | 两人四客户完整证书亦否定SPE=>PNE桥；外部静态定理不能自动导入。 | 不否定静态定理本身或一般half。 | E |
| [research/current/customer_attraction/worst_pne_welfare_counterexample.md](../current/customer_attraction/worst_pne_welfare_counterexample.md)；`CA-WORST-PNE-WELFARE-NO` | 三人16客户完整SPE W15，而全部静态PNE福利16，否定改选同实例较差PNE支付W的桥。 | 实际非PNE还不够，此例排除另选PNE修复；不否定聚合安全值。 | E |
| [research/current/customer_attraction/worst_cce_welfare_counterexample.md](../current/customer_attraction/worst_cce_welfare_counterexample.md)；`CA-WORST-CCE-WELFARE-NO` | 三人13客户完整SPE W9，最低不对称任意相关静态CCE期望福利2785/297>9；有原始/对偶。 | 只更换静态比较对象为CCE也不能修复。OPT_3=12，half仍成立。 | E |
| [research/current/customer_attraction/eight_customer_cce_welfare_gap.md](../current/customer_attraction/eight_customer_cce_welfare_gap.md)；`CA-WORST-CCE-WELFARE-8` | 三人8客户四主题完整SPE W6，最低静态CCE恰544/87>6。 | 更小独立见证，保留13客户原身份；最小性未认证。 | E |
| [research/current/customer_attraction/iid_security_and_flow_barriers.md](../current/customer_attraction/iid_security_and_flow_barriers.md)；`CA-IID-STRONG-WELFARE-NO`、`CA-FULL-TREE-AVERAGING-NO` | 由既有CCE反例与静态Nash属于CCE，否定强W>=Z_m；另有**非SPE分离向量**否定节点内先平均全部偏离/固定深度权支付模板。 | 静态 `m v<=Z<=OPT` 仍真；弱iid另有下行完整SPE反例，真正v强/弱聚合仍OPEN。分离向量不是游戏反例。 | M |
| [research/current/customer_attraction/iid_security_and_flow_barriers.md](../current/customer_attraction/iid_security_and_flow_barriers.md) §1.2；`CA-IID-WEAK-WELFARE-NO-v1` | 多花瓣完整SPE严格否定弱 `W>=(1−1/(2m))Z_m`，因此也否定其等价全局iid总债预算。m=20、J=100时102主题140客户，W40、OPT59，有严格有理分离；固定102主题的同族对每个m>=41成立。 | Z_m恰为同一个静态凹势最大者/对称iid Nash覆盖值，不是换基准。原[个人全文](../workspaces/customer-attraction/R-d321c149379b425493c5e8a5e03c6f39/security/weak_iid_bridge_counterexample.md)、[父代理独立审查](../workspaces/customer-attraction/R-d321c149379b425493c5e8a5e03c6f39/parent/weak_iid_parent_review.md)及[盲独立审查](../workspaces/customer-attraction/R-d321c149379b425493c5e8a5e03c6f39/credible/weak_iid_independent_review.md)均保存。本族有合法静态背景给v_m<=2，且W=2m>=m v_m；不否定真正v强/弱聚合或一般half。 | 完整解析族、定义级精确审计及多路独立内部重构；共享身份同轮补入，无外审/新颖性认证 |
| [research/current/customer_attraction/portfolio_matching_counterexample.md](../current/customer_attraction/portfolio_matching_counterexample.md)；`CA-PORTFOLIO-MATCHING-NO` | 两人86客户完整SPE，唯一最优组合两种匹配真实偏离和均不足付遗漏。 | 只排除将最优主题匹配到实际玩家的指定收费，不排除跨玩家/跨节点支付。 | E |
| [research/current/customer_attraction/tax_bridge_counterexample.md](../current/customer_attraction/tax_bridge_counterexample.md)；`CA-TAX-BRIDGE-NO` | 空背景三人15客户完整SPE否定逐首步机会成本税递推，严格差1/2。 | 此例整条根税恰等；两人局部税不受影响。 | E |
| [research/current/customer_attraction/general_tax_counterexample.md](../current/customer_attraction/general_tax_counterexample.md)；`CA-GENERAL-TAX-NO` | 完整七人根SPE实际到达的非零背景、四剩余人，总税失败；并有无限族。 | 背景剩余利润与全局覆盖须区分；不由此直接判空根总税。 | E |
| [research/current/customer_attraction/root_tax_counterexample.md](../current/customer_attraction/root_tax_counterexample.md)；`CA-ROOT-TAX-NO` | 四人61客户完整SPE：OPT61、W38、实际根税45/2，否定 `OPT<=W+tau`，严格差1/2。 | 真正空背景根顺序反例；half、两人税及聚合安全值均未否定。 | M |
| [research/current/customer_attraction/two_remaining_tax.md](../current/customer_attraction/two_remaining_tax.md)；`CA-ROOT-TAX-ORDER-COUNTS-NO` | 根税对终局任意排序/计数的加强失败；只有真实实际末位节点才有合法BR查询。 | 本文件两人税和末节点OPT税组件保持；实际根税另有真正四人SPE反例。 | M；主两人税E |
| [research/current/customer_attraction/coverage_opportunity_counterexample.md](../current/customer_attraction/coverage_opportunity_counterexample.md)；`CA-COVERAGE-OPPORTUNITY-NO` | 三人11客户完整SPE，某步最优覆盖补全损失delta_i>u_i，否定当期收费。 | 总机会损失望远镜恒等式保留，不能将逐步失败写成终局总预算失败。 | E |
| [research/current/customer_attraction/prefix_balance_counterexample.md](../current/customer_attraction/prefix_balance_counterexample.md)；`CA-PREFIX-BALANCE-NO`有限证书 | 四人22客户完整SPE给负实际前缀余额。 | 是下行全人数族的一个具体证书；不是另一条一般福利定理。 | M |
| [research/current/customer_attraction/prefix_balance_family.md](../current/customer_attraction/prefix_balance_family.md)；同身份 | 每个n>=4有完整SPE负首步余额；任何固定首位权重alpha<2均不能统一修复。 | half与该族根税仍成立；允许局部欠债的全局机制未排除。 | M |
| [research/current/customer_attraction/aggregate_theta_counterexample.md](../current/customer_attraction/aggregate_theta_counterexample.md)；`CA-AGGREGATE-LAST-FLOOR-NO` | 每个n>=3存在完整SPE `W=n theta_n−1`，否定聚合末位最坏BR保底。 | theta与不观察查询的v不同；真正W>=nv仍开放。 | M |
| [research/current/customer_attraction/uploaded_tool_audit.md](../current/customer_attraction/uploaded_tool_audit.md)；`CA-LAST-FLOOR-ALL-PLAYERS-NO` | 四人12主题完整SPE首位收益theta−1，否定全员theta保底；同时核对上传工具与规范递推。 | 上传包仅来源，有限工具对照不证明一般猜想。 | E |
| [research/current/customer_attraction/individual_security_counterexample.md](../current/customer_attraction/individual_security_counterexample.md)；`CA-INDIVIDUAL-SECURITY-NO` | 三人34客户完整SPE与唯一安全最优分布，否定逐人 `u_i>=v_m`。 | 本例聚合安全桥、half成立，不能把逐人失败扩大为聚合失败。 | M |
| [research/current/customer_attraction/general_half_proof.md](../current/customer_attraction/general_half_proof.md) §8；[既有全人数零根保险族](../workspaces/customer-attraction/R-d3981c0168644971803a9c3380ed687c/round5_general/security/global_extra_individual_counterfamily.md) | 逐位置完整额外槽菜单 `M_i<=u_i` 已失败：m≥4 有 `M_1>=v_(m+1)>=δ_(m+1)>u_1`；m5根 `u_1=5/4<25/18=δ_6`。 | 是原根实际位置，不是旧PB任意背景外推；该族 `M_1<2=W/m`，因此未否定全路径 Mpath 或 half。仅将旧反族转接到完整菜单精确合同，不认领新实例。 | 既有全历史解析内审；[独立合同核查](../workspaces/customer-attraction/R-e7c3c9a51d38458aa551eec469e04cf2/independent/mfull_insurance_scope_review.md)与父方逐式重构 |
| [research/current/customer_attraction/policy_security_checkpoints.md](../current/customer_attraction/policy_security_checkpoints.md)；`CA-FIVE-INDIVIDUAL-SECURITY-NO` | 五人十不同极大主题86客户完整SPE又否定逐人v；另21指定锥有聚合正证书见第二类。 | 不证明两个早期玩家同时低于v，不反驳聚合桥。 | E |
| [research/current/customer_attraction/continuation_security_barriers.md](../current/customer_attraction/continuation_security_barriers.md)；`CA-ADAPTIVE-DECORRELATION-NO`、`CA-ACTUAL-ROOT-TAIL-MENU-NO`、`CA-CREDIBLE-MENU-SECURITY-NO-ALL-N` | 完整SPE否定多后继普遍去相关、真实根回复菜单替代真正静态安全对手；含36客户及任意n>=3构造。 | `CA-ONE-FOLLOWER-DECORRELATION`的任意背景恰一后继恒等式仍成立；根菜单minimax不等于真正v。 | M |
| [research/current/customer_attraction/global_security_budget_boundaries.md](../current/customer_attraction/global_security_budget_boundaries.md)；`CA-AGGREGATE-DECORRELATION-NO`、`CA-ONPATH-DECOUPLED-BUDGET-NO` | 完整89/36客户SPE分别否定无松弛总去相关及对**全部p**的含激励松弛总补偿预算。 | `W−sum C_i=sum e_i+sum kappa_i`恒等式保留；适当安全最优p或任意共同静态Q支付未被否定。 | M |
| [research/current/customer_attraction/security_chain_and_local_boundary.md](../current/customer_attraction/security_chain_and_local_boundary.md)；`CA-LOCAL-SECURITY-INDUCTION-NO` | 完整SPE实际路径有负局部D_i，否定逐步安全债务非负及对应更强弱系数局部条件。 | 全路径恒等式和全局桥保留开放，末两人非负也保持。 | M |
| [research/current/customer_attraction/dynamic_iid_debt_boundary.md](../current/customer_attraction/dynamic_iid_debt_boundary.md)；`CA-WEAK-LOCAL-IID-DRIFT-NO` | 五人七主题60客户完整SPE实际节点否定指定弱局部iid漂移。 | 这个60客户例仍满足较弱全局iid不等式；其全称版本已由另一个多花瓣族反驳。局部失败和全局失败的证据对象须分开。 | M |
| [research/current/customer_attraction/stationary_pair_transport.md](../current/customer_attraction/stationary_pair_transport.md)；`CA-PRESCRIBED-STATIC-KERNELS-NO` | 完整SPE分别否定根回复驻留核的W/m cap和实际经验iid核的W/(m−1/2) cap。 | 末两人循环运输恒等式不受影响；不排除重选Q、全部节点菜单或全历史非均匀支付。 | M |
| [research/current/customer_attraction/fractional_actual_load_counterexample.md](../current/customer_attraction/fractional_actual_load_counterexample.md)；`CA-FRACTIONAL-ACTUAL-LOAD-WEAK-NO-v1` | 每个m>=4有四主题完整SPE，W=m²、OPT=m²+1，否定实际均匀缩放背景的 `(m−1/2)M<=W`。 | 静态代数保留；本族本身没有反驳精确税桥，但该桥另已被旧13人36客户完整SPE否定，见下一行。真正v、half仍开放。 | E |
| [research/current/customer_attraction/fractional_actual_load_counterexample.md](../current/customer_attraction/fractional_actual_load_counterexample.md) §4；[旧36客户完整策略](../workspaces/customer-attraction/R-c50fecc37aa44fb4a69a2122bb70e5fe/security/refined_tax_counterexample.md) | `alpha=(m−1)/m` 的精确实际税充分桥 `mM<=W+G_C` 已由旧13人完整SPE严格反证：W=33、OPT=36、M=3、G_C=708669/123025，差29481/123025>0。 | 普遍代数 `OPT<=mM+W−G_C` 保留；真正安全值、Mfull/Mpath与half未被反驳。本轮只纠正总账滞后并重放既有112050项精确IC，不认领新反例。 | E；既有独立审计，本轮定义级重放 |
| [research/current/customer_attraction/optimal_last_query_counterexample.md](../current/customer_attraction/optimal_last_query_counterexample.md)；`CA-OPTIMAL-LAST-QUERY-SUM-NO` | 四人1651客户完整SPE，唯一最优主题组合在真实末节点的查询和>W，否定“另选最优组合即可使查询和付W”。 | 只是根税充分接口失败；独立实际根税反例另有正文。 | M |
| [research/current/customer_attraction/random_position_exchange_boundary.md](../current/customer_attraction/random_position_exchange_boundary.md)；`CA-RANDOM-PREFIX-EXCHANGE-NO` | 三人五客户完整SPE否定随机最优主题排列前缀的位置交换步骤。 | 随机排列不能代替真实后继回复控制；不否定任意随机分析。 | E |
| [research/current/customer_attraction/collision_free_occupancy_obstruction.md](../current/customer_attraction/collision_free_occupancy_obstruction.md)；`CA-COLLISION-FREE-LOAD-PAYMENT-NO` | 两人五客户完整SPE实际无拥挤、W4<OPT5；否定一切f(0)=0、f(1)=1的纯负载可加OPT支付。 | 改f(2),f(3),…无法修复该见证；half不受否定。 | E |
| [research/current/customer_attraction/collision_free_three_halves_family.md](../current/customer_attraction/collision_free_three_halves_family.md)；`CA-COLLISION-FREE-FAMILY-3-2` | 任意m>=2有完整无拥挤SPE，W=2m、OPT=3m−1，比率趋3/2；普遍纯负载支付需f(1)>=3/2。 | 全历史Q/B归纳的真SPE族；不是一般half反例或无拥挤类上界。 | E |
| [research/current/customer_attraction/coverage_moment_geometry.md](../current/customer_attraction/coverage_moment_geometry.md)；`CA-EXACT-OPT-EXTERNAL-FOLD-NO`及CR-6 | 精确保全部资料的非负折叠不能预先删OPT外类型；另所有末层行非负仍可根福利低，例子**不是完整SPE**。 | 线性span、非负行锥和全树激励不能混同；依实例有理稀疏化仍成立。 | E |
| [research/current/customer_attraction/five_player_lift_obstruction.md](../current/customer_attraction/five_player_lift_obstruction.md)；`CA-FIVE-LIFT-ROWS-NO` | 指定460行必要条件松弛有O>2W有理点；辅助O不是真实OPT，未给完整策略。 | 只否定这组行/乘子模板，不能称SPE或half反例。 | M |
| [research/current/customer_attraction/five_player_indexed_obstruction.md](../current/customer_attraction/five_player_indexed_obstruction.md)；`CA-FIVE-INDEXED-ROWS-NO` | 指定437行索引松弛的有理原始/对偶匹配，模板最优值>2。 | 模板精确最优不是原游戏可达下界；只调同模板乘子不能闭合half。 | M |
| [research/current/customer_attraction/six_maxima_seat_obstructions.md](../current/customer_attraction/six_maxima_seat_obstructions.md) | n=5,6,7,8的合法路由路径使动态席位和<OPT/2；这些路径**没有SPE认证**。 | 席位逐人下界仍合法，单靠其路径求和不足；六极大half已有另行联合证明。 | X；独立Fraction机制审计 |
| [research/current/customer_attraction/terminal_tie_lift_obstruction.md](../current/customer_attraction/terminal_tie_lift_obstruction.md)；`CA-TERMINAL-TIE-FIXED-LIFT-NO` | 目标为2c−o、加入全部同计数末行等式后，仍未必能保留一个既定规范化证书的早期乘子提升。 | 只否定固定乘子保留；不否定共同重选乘子、商空间工具或一般half证书。 | M |
| [research/current/customer_attraction/mobius_compiler.md](../current/customer_attraction/mobius_compiler.md)；`CA-MOBIUS-BIAS-BARRIER` | 指定充分大正偏置编译器自身满足half的严格正余量，不能据该安全编译器产目标反例。 | 解析方法屏障，不是SPE桥反例；小偏置/其他非均匀补偿须另核全部历史。 | M |
| [research/current/customer_attraction/compiler_security_barrier.md](../current/customer_attraction/compiler_security_barrier.md)；`CA-MOBIUS-SECURITY-BIAS-BARRIER` | 对p>=n>=2、r_B=x_B+K合法的n-distinct终局，逐人 `u_i−v_n>=K c_(p,n)−sum|x_B|`；标准K=4sum|x_B|+1给至少1/4余量。 | 更强编译器屏障，非一般逐人v定理；标准嵌入另保证根SPE用不同标签。较小偏置不在结论内。 | M |

## 六、登记核对、冲突与恢复入口

1. **文件覆盖。** 本账明确列出本目录原70份正文、整理时新增的1份一般衔接工作稿以及README，共72文件；混合文件按不同statement分列，重复路径不重复计算成果数量。其余工作区草稿不自动升为current成果，不在此盘点数字内。
2. **总身份仍OPEN。** 所有反例/障碍都按明确辅助对象登记；没有把“某固定LP不能推出”写成“一般命题不可证明”，没有把有限阴性搜索写成一般定理。第三类开放桥也不被强制作为唯一研究路线。
3. **现有等级。** 七极大区分来源完整/现行依赖概述；terminal两份提升保留conditional字段；six-maxima-seat正文只有机制审计而无独立claim行，保留X，交由登记维护者决定是否需新增身份。本账不补造登记、不回写状态。
4. **过时局部前沿措辞。** `three_maxima_bound.md`等早期正文中的“更多极大仍开放”描述其当时局部边界，不能覆盖后来至多六极大和七极大n>=7的已证范围；当前一般前沿以本账、精确Claims及现行RESEARCH_STATE合读。这里不改旧定理量词，也不据一句过时开放措辞撤销后续结果。
5. **身份不替代语义。** `CA-FIVE-UPPER-221-100`名称保留旧粗常数，现行精确系数已在第二类列明；`CA-PREFIX-BALANCE-NO`同时承载22客户有限证书与任意n>=4族，故两个正文均保留；聚合theta、聚合v与iid Z分别处理。
6. **依赖与资产入口。** 精确命题和五轴等级分别回 [research/current/claims.md](../current/claims.md)、[research/review_status.json](../review_status.json)；实现/审查/证据/来源路径回 [research/assets.json](../assets.json) 及各正文。主要资产包为 `sequential_customer_attraction`、`customer_attraction_global_transport_round`、`customer_attraction_terminal_tie_quotient`、`customer_attraction_penultimate_menu_half`、`customer_attraction_extreme_maximal_membership`、`customer_attraction_uncovered_private_spectrum`、`customer_attraction_fractional_tail_waterfill`。
7. **弱iid状态纠正。** 本轮重新读到d321的既有个人完整族与parent/credible审查，并经本组root、当前安全稿作者及独立清洗者核对，确认它使用同一Z_m且为完整SPE；故弱iid及其等价总债从第三类OPEN移入第五类已反驳桥。静态iid基准、凹势/KKT和债务恒等式不受影响；真正v_m的两条聚合桥与Q-CAG-HALF保持OPEN。本次仅整合既有证据，不宣称新实例发现或重新实验。

本账只改变读取组织和研究用途标记；没有改写已有真值、输入域、纯SPE量词、条件或证明状态。后续一般研究可提取第一/四类组件，重新组合真实全历史机制；第二类停止扩张，第五类仅在一个明确新的一般候选需要时用于反例诊断。


2026-10-23推送同步增补：共享数学文件仍为72份，水位正文新增的VAR、统一缩尾税账和有条件可信性来源按原范围接续；没有新增无条件SPE定理。个人区完整清单已补到固定提交5b183a1a（74 actor、4130文件），见WORKSPACE_RESULTS的增量节。新稿正文分类与实际阅读覆盖另见SYNTHESIS，本总账不因此提升全部原审查等级。
