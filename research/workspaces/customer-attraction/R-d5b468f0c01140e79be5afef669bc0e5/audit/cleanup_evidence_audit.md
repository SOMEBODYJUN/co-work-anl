# 既有正面结果与一般组件：定点证据审计

2026-10-25。仓库 `co-work-anl`；只读研究文件，未联网、未发送仓库消息、未提交、未修改共享正文或冻结证据。本轮不是新数学研究，也没有重新审完全部成果。路径以下均相对仓库根。

## 可直接用于短入口的结论

`Q-CAG-HALF` 仍 **OPEN**。模型是有限单位客户、有限非空共同目录、任意单位提供者人数、全部有序历史上的每个纯 SPE；空主题、重复动作、零客户及任意历史平局保留。三人锐界为 `5/3`，四人为 `1499/750<2`。共享五人登记仍为 `2.06169478572…`，但个人区已有独立全类型对偶审查支持更强的 `2.042155490337931…` 上界；两者没有数学矛盾，是共享入口滞后。更低的 `2.0420789865600059…` 只到作者全域精确自查，不能混写为同等独立审查级别。以上均未闭合五人或一般 half。

这里“上界已内审”不等于外部同行审查、新颖性认证、原游戏锐界或模板原始点可补成 SPE。所有本次查到的相关 `review_status.json` 的外审字段均为 `not_recorded`。

## 固定人数：准确 statement / scope / status / source / review / evidence / objection

| Statement 与 scope | Status | Exact source | Review / evidence | Objection / 使用边界 |
|---|---|---|---|---|
| `CA-THREE-SHARP-5-3`：恰3人、任意共同目录、每个完整历史纯 SPE，`OPT_3≤5W/3`，匹配下界 | 共享完整证明；锐；已有两路独立内审 | `research/current/customer_attraction/three_player_sharp.md` | `tests/audits/customer_attraction_three_player_sharp.py`；冻结 `evidence/runs/2026-10-09/customer_attraction_three_player_sharp.json`；本次重放2048全部会员型、12288展开、160角点、下界39全历史动作比较通过 | 非任意人数定理。实际和离轨主题取自同一原策略；不以有限游戏抽样证明全称结论 |
| `CA-FOUR-UPPER-1499-750`：恰4人、零根背景、任意共同目录、全部完整纯 SPE，`OPT_4≤1499W/750` | 共享完整证明；非锐性声明；多路内审 | `research/current/customer_attraction/four_player_bound.md` | `tests/audits/customer_attraction_four_player.py` 及 `_independent.py`；对应2026-10-09冻结JSON；本次两份重放均通过，128余项最小值0 | 唯一先前福利依赖为 `CA-TWO-REMAINING-TAX`；不依赖三人福利界。没有现成的3→4→5归纳链 |
| `CA-FIVE-INDEXED-UPPER`：恰5人、零根背景、任意目录、全部完整纯 SPE，`OPT_5≤β437 W` | 共享正式登记的完整上界；旧437行模板 | `research/current/customer_attraction/five_player_indexed_bound.md`；障碍为 `five_player_indexed_obstruction.md` | `research/current/claims.md`、`review_status.json` 登记完整/多路内审；正文列两份互不导入精确审计及6144全域条件余项 | `β437>2`。64原子原始点只证该437行必要条件模板不能推half；无完整SPE或实际OPT证书 |
| **个人区557行上界**：同一五人一般目录/完整历史量词，`OPT_5≤β557 W` | **独立全类型对偶内审已通过；尚未共享正式登记** | `research/workspaces/customer-attraction/R-c4732bee2f7b4e50a70568170e3334ae/round4_independent/full_pricing_review.md`；证书 `../round4_pricing/exact_dual_overlap1.json` | 同目录 `full_pricing_audit.py/json` 独立重建活跃行，不导入发现定价器。本次保持SOURCE不变、仅将输出重定向仓库外后重放：51正乘子、1024固定掩码、6个共同d、792/15504直方图、6144条件、最小整数余项0、84零项、无负项；输入SHA与冻结相同 | 足以支持改进的五人福利上界；不要求匹配primal。67原子匹配primal未由该独审重核，因此不能把“松弛精确最优”也称独审通过。不能沿用437行的ID而静默换常数 |
| 557行已有60原子二以上可行点：`W=1`、比较覆盖≈`2.04202004419` | 父方独立核验全部557行通过；仅模板障碍 | 同actor `round4_parent/README.md`、`audit_full_primal.py/json`；输入 `round4_pricing/exact_primal_overlap1.json` | 437旧行复用已审定义，120新增行按字面索引重构；全部余量与报告一致 | 不是557行精确最优声明，也不是SPE/实际OPT。其他跨族条件可进一步分离，不削弱其作为指定模板可行点的身份 |
| 717/727/728/737行：作者报告的更强完整类型系统，其中728最小，`β728≈2.04207898656` | 作者精确原始+全宇宙整数对偶已保存；父未独立接受其全域对偶 | 同actor `round5_pricing/README.md`、`exact_dual_joint_terminal.json` 等实际证书依README；父边界 `round5_parent/README.md` | 父已独审717原始全部717行；已独审727点联合OO分离；727/728/737全原始余量及四个全域对偶仍为作者自查 | 不写成与557同等级。更小模板点均非完整SPE；作者已明确停止逐行常数任务，未来仅复用一般联合支持函数机制 |

### Python Fraction 精确反算

| 数值 | 精确值 | 十进制（精确分数计算） | 与2的关系 |
|---|---|---|---|
| 三人 | `5/3` | `1.666666666666666666666666666666…` | `2−β=1/3` |
| 四人 | `1499/750` | `1.998666666666666666666666666666…` | `2−β=1/750` |
| 五人437行 | `145473820534756099649387160645076613709/70560308704423797361284609157664425493` | `2.061694785720737354094675680447…` | `β−2=4353203125908504926817942329747762723/70560308704423797361284609157664425493>0` |
| 五人557行 | `178528430822287579296070598592537012737/87421565922360356032366460363114422206` | `2.042155490337931083188965785107…` | `β−2=3685298977566867231337677866308168325/87421565922360356032366460363114422206>0` |
| 五人728行（作者） | `903491829723556246762087795616829492745/442437259121664928475146048173419016656` | `2.042078986560005907914880081627…` | 仍严格大于2；README浮点末位不作为精确来源 |

`β437−β557=0.019539295382806270905709895339…`。短入口应以“共享登记 / 个人区独立已审上界 / 作者证书”分层，不能只标“当前最佳2.061695”，也不能把作者728证书自动升级。

## 无人数和目录限制的可接续组件

以下是原量词下的组件，不等于一般half。表内内审为既有登记，本轮仅核对定义、推导接点和来源；除前表算术审计外未逐条重新外审。

| Statement / scope | Status / review | Exact source / evidence | 未支付的义务或不可省略条件 |
|---|---|---|---|
| 任意真实历史旧负载b、余r，当前利润 `u≥max_TΣ_(x∈T)1/(b_x+r)`；同叶包含主题收益支配 | 完整分母引理；一般稿直接推导；顺序份额L1–L4有独立纠错审查 | `research/current/customer_attraction/general_half_proof.md` §2；`continuation_lemmas.md`；个人 `R-1740705e79f14baba6326b951a52152f/route5a/sequential_deviation_share_lemma.md` | 只能同一终局比较收益，不可跨枝搬旧利润；L1是一般分母界在遗漏客户上的专门化，不应再报独立突破 |
| 任意比较集C、分数覆盖总重τ，`|C|≤P_(i−1)+rτu_i`；乘积界 `W≥|C|[1−∏_(r=1)^m(1−1/(rτ))]` | 共享完整；两路解析内审、精确有限回归 | `fractional_cover_path_budget.md`；`review_status` ID `CA-FRACTIONAL-COVER-PATH-BUDGET` | P为实际旧玩家最终收益；τ可增长。无条件τ≤m只给趋零比例；m5该比例精确 `6049/15625=0.387136`，不能写成half |
| 任意全局私有实际遗漏块的触块席位谱；冻结前缀联合F/G谱有 `u_i≥Λ_i≥λ_i`、`W≥ΣΛ_i` | 共享完整；前者盲独立解析、后者G盲重构/F读稿核对及完整SPE严格例独审 | `uncovered_private_seat_spectrum.md`；`general_half_proof.md` §3.1；其所链个人全文和审查 | Q全空时F/G精确退回分母界。一般共享遗漏付款仍缺；不应写成已经解决共享关联 |
| 任意目录的superset席位与动态极大主题路由/私有共享混合包络 | 共享完整，多路内审 | `sunflower_maxima_bound.md` §8；`dynamic_maxima_bound.md`；ID `CA-MAXIMA-SUPERSET-SEATS` / `CA-DYNAMIC-MAXIMA-FLOOR/MIXED` | 参数s可无界，但现有系数不足以无条件half；共同质量不能分别取最大后相加 |
| 任意合法背景、恰两人尾部：配对份额差恒等式、双方局部θ保底、一后继独立去相关；一般弱界 `W≥4(m−1)OPT/[m(2m−1)]` | 共享完整；内审（保底current_exact，去相关multiple） | `last_two_floor.md`；`continuation_security_barriers.md`；`two_remaining_tax.md` | 固定尾长组件可供任意总人数使用，但不可改成全部玩家θ保底或多后继去相关 |
| 任意合法背景末三/末四人利润比较；末四提升到全人数 `OPT_m≤(m/2−1/750)W` | 共享完整，多路内审 | `three_remaining_profit_bound.md`、`four_remaining_profit_bound.md`、`tail_profit_lift.md` | 必须用背景利润版，裸搬空根定理无效；系数随m增长，m5仍大于2 |
| 真正静态不观察查询的安全值 `v_m(0)≥OPT_m/(2m−1)`；一般s槽形式 `OPT_m≤(m+s)v_(s+1)(0)` | 前者共享完整多路内审；后者一般稿直接同目录预算 | `oblivious_security.md`；`general_half_proof.md` §4 | 对手静态联合元组不观察抽样；真实后继观察当前行动，故不推出逐人或聚合支付 |
| 实际安全值链V非降、末位V=u；`ΣD_i=W−mv_m(0)` | 共享完整，多路内审 | `security_chain_and_local_boundary.md`；一般稿§5 | 强 `W≥mv_m` 与弱 `W≥(m−1/2)v_m` 均OPEN；局部D非负、逐人保底、强弱iid替换均已反驳 |
| 最优首动作真实孩子缺口：`r(δ−u)=(r−1)ρ−θ−(r−1)(f+ξ)−η−rΓ`；实际路径Σδ=`OPT−W` | 共享完整全范围恒等式，多路独立内审 | `optimal_first_action_branch_gap.md`；`research/reviews/customer_attraction/optimal_first_action_branch_gap.md`；一般稿§3.2 | 所有负项非负，但跨孩子ρ正项没有总支付。丢ξ/η后的菜单付款已由all-big族否定；恒等式本身保留 |
| 非根跨枝福利修正 `ΔW=ΔV+ΔP_old−Γ≤ΔV+ΔP_old`；根P=0 | 个人已纠错并有独立审查；共享精确索引已区分v1/v2 | `R-1740705e79f14baba6326b951a52152f/representation/cross_branch_welfare_relay_identity.md`；`R-cef41b80a6e048b5a395b738d3b0b6e7/harmonic/relay_erratum.md` | 旧v1“任意节点ΔW≤ΔV”FALSE，不能把量词静默缩根后标成原版本已证。跨互斥子树信用仍未合账 |
| 给定终局分数尾水位：同一尾权、同一全客户信用池H≤低尾总缺口，并守恒根/背景/尾利润 | 共享完整终局代数；盲独立重构、边界审计 | `fractional_tail_waterfill.md`；同名 `research/reviews/customer_attraction/` 审查 | 不要求也不产生SPE。辅助分数权可无理，不能无条件调用单位玩家归纳；多分支重复使用同池不合法 |
| 可信续局全集拼合、完整策略重数锥；末回复证书的条件提升 | 全集/锥是共享完整表示；末回复是已有条件提升接口，相应内审保留 | `exact_solver.md`、`credible_continuations.md`、`strategy_cone.md`；`terminal_reply_transport.md`、`terminal_tie_quotient.md` | 全集表示与有限精确工具本身不提供全称福利支付，不声称位多项式；旁枝威胁必须用未受祖先终局约束的孩子重置。末回复规范化不自动保早期SPE，提升需另付有符号旧玩家误差 |

## 个人区较新的一般组件：保存身份，不自动提升

1. `R-e05f01e191354b028004b433016ae1c9/penultimate_true_query_row.md`：任意m、任意q比较主题，真实倒二查询和 `R_(m−1)≥O−W+t_b(A)`，另有 `≥O−W+F/2`；由同背景一后继去相关及实际全局旧覆盖信用证明。正文记录另一方向/父方逐客户内审，但尚非独立共享Claim登记。本次按正文核对机制，未另造审查等级。它让“最小收益由末两位取得”的路径满足half；所有更早位置仍未付，两项余量不能相加重复收费。
2. 同actor `offspring_menu_loss_bound.md`：任意r≥2、最优首动作A的任意真实尾，`Σλ_(B_l)≤(r−1)(|t_A|+η_A)`；事实上不需要当前IC。正文记录独立逐客户重构。它只控制菜单外静态损失；真实重置差 `C_A−C_B` 无已证符号，不能从低λ推出低真实孩子损失。
3. `R-cd789330fc7141299ac491bbb3ffa420/round2/`：变分规范水位、原规定路径税账及统一正质量缩尾接口已有各自独审。缩尾保可信性有“全部规定行动避非核心正背景”等承重条件；查询池另有实际负载谱条件。恢复入口是各 `shared/credible/tail/README.md`，不得把条件接口写成任意树免费保真。
4. `research/current/customer_attraction/incidence_lp_dynamic_budget.md`：`CA-INCIDENCE-LP-DYNAMIC-BUDGET-v1` 仍为解析**候选**，正文和共享账本都明示待独立清洗；`tau_inc≤2` 的half推论依赖该候选接口。总账中应与已独审组件分开，不能因进入current而升为已内审定理。

## 条件正面边界与下一轮最小输入

保留原有特例资产，无须下一轮重读全部正文：至多六个极大主题、任意m的half；恰七极大且m≥7的来源完整已内审证明（m5/6缺分支）；sunflower/laminar/extreme关联类的带核心锐 `2−1/m`；最优遗漏全私有的锐界；某最优并集分数覆盖τ≤7/2；倒二主题共同包含或少量例外平方阈值。它们都是**原条件下已证**，不会因本轮清理失效，也不能外推任意目录。

短入口建议只给：模型量词 → 原目标OPEN → 三/四人数地基 → 五人三层证据状态 → 一般稿§2–5的已证关系与两个真实付款断点 → 按需个人新组件。核心尚缺的是对所有真实分支的后继理性建立不重复计费的跨角色/跨客户共同预算。数值证书/等价表示、正确局部引理和有限没有反例均不能替代该步骤。

本次实际重放输出只写到仓库外 `cleanup_evidence_replay/full_pricing_audit.json`；三/四审计仅stdout。本报告未改变共享统计、Claim身份或外审字段。
