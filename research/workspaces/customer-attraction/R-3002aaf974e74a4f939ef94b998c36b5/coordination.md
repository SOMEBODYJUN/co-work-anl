# Boss36：六人研究的共同接续入口

本轮任务仅为 **Q-CAG-HALF-6**。本页是去重与证据导航，不新增数学结论，不限定研究方法。恢复基线为 main `f16735ef433ae84d475794dfdf90cb44cb2e7225`；当前判断以正文、证据和后续提交为准。

## 精确目标

有限单位客户集 N，有限非空共同目录 S⊆2^N，六名单位权提供者依固定顺序观察全部有序历史，各选一个主题。允许重复、空主题、零客户及任意历史依赖平局。终局客户 x 被 c_x 名提供者覆盖，每名获得 1/c_x；W 是实际并集大小，OPT_6 是六个目录主题可覆盖的最大客户数。对每个实例、每份定义于全部有序历史的纯 SPE，证明 2W≥OPT_6。若为假，须给原模型严格反例、覆盖全部有序历史的完整纯 SPE 和可复现精确核验。松弛坏点、局部菜单、非 SPE 路径及有限阴性搜索均不是答案。

六个研究线程收到同一目标与入口，自由选择方法，允许交流、重叠和自主协作。主方负责读入资料、交流、整理及 checkpoint；本 clone 的 Git 同步、提交、公屏和身份由主方统一操作，避免共享索引竞争。研究者可随时保存有接续价值的未完成正文和代码并通知主方，无需等待成果审核。

## 短入口与可靠边界

| 何时读 | 唯一入口及当前范围 |
| --- | --- |
| 固定模型与历史量词 | `research/current/customer_attraction/model.md`；同计数历史允许不同续局，计数缓存的终局集合不是匿名策略假设 |
| 查数学地图与已有方法 | `research/current/customer_attraction/README.md`、`research/customer_attraction/SYNTHESIS.md`、`RESEARCH_STATE.md`、`FAILED_ROUTES.md`；旧的一般人数优先指令不改变本轮六人目标 |
| 引用五人机制 | `research/current/customer_attraction/five_player_half.md`：五人完整精确证书、内部复核，未记录外审；不含五人任意背景利润定理，也不含六人 |
| 需要真实跨枝报价 | `priced_hidden_reply_projection.md`、`same_source_reply_requery.md`（同上数学目录）：任意尾长局部非负恒等式已证，六人共同总付款未闭合 |
| 需要有限完整策略 | `exact_solver.md`、`credible_continuations.md`、`strategy_cone.md`；全集终局、指定策略锥、完整策略和松弛点严格分开 |
| 使用极大主题机制 | `six_maxima_joint_bound.md`、`seven_maxima_checkpoint.md`：至多六极大子类已闭合；七极大六人有缺口；**没有任意目录→七关注主题且保留全部历史 SPE 的归约** |
| 需要小背景接口 | `research/workspaces/customer-attraction/R-07e7ddcae71544449ffaae7bdddcc1ab/research_1/two_remaining_three_comparison.md`（f16735e）：任意合法旧前缀后恰两名剩余玩家，任意三个比较主题并集 O≤2W，W含旧前缀。`G=(6S+Z+2V+5L)/11`，零背景完整域与正整数背景解析尾部。父方逐式读与作者实现复跑，非第二核验器；不含r5或六人闭合，未完成全仓查重 |

上一 Boss36 入口 `R-3a870729e9524f6da600542c63297d4c/coordination.md` 可追旧来源，但其中将七极大44轨道称作普适六人缺口的表述不可沿用。它们只属于结构子类。目录其他主题可能决定离轨回复；选最优六主题加实际末位、删动作或扩为极大容器均不能自动保留原 SPE。

## 最新正向特例：两项条件不可混同

实际终局记 `(E1,E2,E3,E4,A,B)`。

1. 存在固定两个早期主题逐集合包含 A，则 half。正文：`research/workspaces/customer-attraction/subagent-f/m6_two_early_A_half.md`；精确乘子 `(5/4,5/4,1)`，不是旧消息的非对称权。作者1960扩大位型、Boss40独立3360含h状态核验。内部检查，未外审。
2. 对每名 x∈A，前四主题中覆盖 x 的个数至少三，则 half；无需任何固定早期主题包含整个 A。正文：`research/workspaces/customer-attraction/R-5662d5cb0e5845a980ed10a3b3224cb1/research_1/threefold_penultimate_half.md`。真实 S/Z/V 菜单加四个有序安全行，权 `(1/3,1/2,1/2,2/3)`，末位改 A 权 `3/2`；作者2058域及父方独立3528域 Fraction 核验。内部检查，未外审。

第二项同证书无条件给缺陷 rho。A 中前四负载 k=0,...,4 的最坏 `360rho=(-1079,-299,-93,2,42)`，A 外 rho≥0。因此 `2n3+42n4≥1079n0+299n1+93n2` 是充分条件；没有证明所有 SPE 都满足。两项条件互不蕴含；逐客户负载≥2仍未由这些结果闭合。

## 已知失败机制，只排除其精确范围

- 逐人安全值、逐位置完整菜单、强/弱 iid 福利替代、静态 NE/最低 CCE 福利支付、固定实际前缀归纳及固定缩放税均有真实反例；按失败地图取原文，不重造同一加强。
- **连弱逐人 `u_i≥OPT_m/(2m)` 都已 FALSE（m≥5）**，因此 `OPT_m/(2m−1)` 也不能重提为开放。唯一全历史反族：`R-d3981c0168644971803a9c3380ed687c/round5_general/security/global_extra_individual_counterfamily.md`（相对本题工作区根）；独立内审在同级 `direct/review_global_extra_individual_counterfamily.md`。保险 Cartesian 目录给 `u1=m/(m−1), W=2m, OPT=3m−2`；六人根收益6/5、W12、OPT16。若旧个人CLAIMS仍标OPEN，按原反证校准。它不否定净差逐人付款或真正安全值聚合。
- 冻结其他实际主题的最优元组静态匹配 `Q≤W` 也已 FALSE，区别于真实偏离匹配遗漏。`R-a0bb57fa24044a8794bc7991918a19c6/static_matching/optimal_static_matching_counterexample.md` 给四人W47、OPT52、唯一最优支持上全部24匹配minQ48；`R-105f776c3e6d4a22bb7c380c5df8edc7/dynamic_exchange/static_optimal_assignment_counterexample.md` 给三人W1735、OPT1740、minQ1736。均有完整历史精确核验。六人专属版本或更弱 `Q≤(1+1/m)W` 不由这两例自动裁决。
- 任意合法背景/任意r首两人 `2v_r(b)` 的旧候选已被 `R-cd789330fc7141299ac491bbb3ffa420/round5/menu/pair_attack.md` 更弱PB-extra反证排除。反证r=2475，背景已覆盖全部客户，未证为根实际前缀；不自动否定小r或六人实际前缀专用接口。原聚合安全值仍 OPEN。
- 非根跨枝必须保留旧玩家最终利润变化：`ΔW=ΔV+ΔP_old−Γ`。净目标为 `OPT−W=|O\C|−|C\O|`；不能删除实际覆盖在最优并集外的信用。
- 七极大逐席 seat 行有完整 SPE 反证：不交 B0 有6名私有客户、其他各1，常值选 B0，W6、OPT6=11。只否定逐席行，合法次序统计量形式仍可研究。
- 七极大 route-conditioned `M/L/T` 行族已有五条 route 的纯 Fraction Farkas 障碍，唯一正文与核验：`research/workspaces/customer-attraction/R-3a870729e9524f6da600542c63297d4c/route_lp_boundary/`，commit `4d5f4bc5632a19bcefd1d5d0c66e7f5895370eb9`。它没有实现完整 SPE，不能当目标反例；000000也失败说明粗行族不能替代上述更强菜单。
- 更旧松弛调权、有限无反例、原证书重复运行，只在核验新推导的明确义务时使用。既有入口不是方法白名单。

## 尚缺什么

Q-CAG-HALF-6 仍 OPEN：无无条件证明，亦无经全历史核验的严格目标反例。可用真实局部行尚未共同支付全部早期分支的损失；不同互斥子树不能重复花同一实际利润。亦可换完全不同的机制。候选、作者证明、内部检查、外审及新颖性分别记录。

## 本轮资产

各线程材料保存于本目录 `research_1/` 至 `research_6/`。本页仅链接有新增信息的正文。主方收到可接续资产后及时核对范围、按需入账，并用根 `work.py checkpoint` 保存；只有 `status=pushed` 才报告远端可恢复。
