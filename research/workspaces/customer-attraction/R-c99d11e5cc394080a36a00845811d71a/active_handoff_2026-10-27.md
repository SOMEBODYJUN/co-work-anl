# Boss35 接续上下文：Q-CAG-HALF-6

日期：2026-10-27。本文是给同一目标的研究代理的短接续，不是新的数学 Claim。

## 固定目标

有限单位客户集、有限非空共同目录、六名单位提供者按固定顺序观察全部有序历史各选一个主题；允许重复、空主题、零客户和任意历史依赖平局。终局客户在覆盖者之间均分，`W` 是覆盖客户数，`OPT_6` 是六个目录主题的最大并集。必须证明每个完整历史依赖纯 SPE 都有 `2W >= OPT_6`，或者给原模型严格反例、完整全历史策略和精确可复现核验。

## 先读的可靠正文

- 模型与量词：`research/current/customer_attraction/model.md`
- 当前前沿与失败分诊：`research/customer_attraction/RESEARCH_STATE.md`、`FAILED_ROUTES.md`、`SYNTHESIS.md`
- 已闭合但范围有限：`six_maxima_joint_bound.md`（至多六个全局极大覆盖）、`five_player_half.md`
- 七极大缺口来源：`seven_maxima_checkpoint.md` 及历史原文 `history/source/notes/customer_attraction/seven_maxima_checkpoint_2026-10-10/seven_plus_source.md`
- 真实路径工具：`fractional_cover_path_budget.md`、`uncovered_private_seat_spectrum.md`、`priced_hidden_reply_projection.md`、`same_source_reply_requery.md`
- 全历史表示合同：`exact_solver.md`、`strategy_cone.md`、`credible_continuations.md`

## 已核对的数学边界

1. `six_maxima_joint_bound.md` 的联合预算使用 mixed floor、真实最终动作的 maximal lemma、末位 BR 与末两位 tax；它完整证明“极大覆盖数至多六”，不能删去目录中额外主题来覆盖七极大，因为删目录会改变所有离轨偏离集合和续局 SPE。
2. 七极大来源证明覆盖 `n>=7`；`n=6` 尚有 `44` 条完整 route（来源记录为 `833/877`）。这是当前最接近的可闭合义务，但不得把未证 route 当作定理。
3. 逐席 `seat(t,j,k)` 行并非 SPE 必然不等式。精确全历史证书：七个互不相交极大主题，`B0` 有 6 个私有客户、其余各 1 个，六人所有历史恒选 `B0` 是完整 SPE；核验 `19608` 个历史、`117648` 个偏离，根 `u0=1`，而非法 `k=1` 行要求 `u0>=6`。该实例 `W=6, OPT6=11`，不是目标反例。
4. 合法席位机制只给第 `r` 大阈值；aggregate order-statistic 行候选尚未接入七极大缺口，不能把浮点正余量当证明。路线-specific seat 版本也有完整两人反例。
5. 直接静态势/末价、强/弱 iid、逐人安全值、固定实际税、局部菜单、有限无反例和必要条件锥坏点均不是原模型证明或反例。消息 378 的静态势点被倒二真实 IC 严格击穿。
6. 条件可回收：若某个最优六主题元组的真实强制回复均不触及根遗漏，则 `OPT <= (2-1/6)W`；若目标失败，真实回复触及的根遗漏并集 `B` 必须满足 `|B|>W/5`。这是必要结构，不是闭合。
7. 真实路径分数覆盖预算给 `W >= OPT*F_6(tau)`；只有 `tau` 受小常数控制时才到 half。私有遗漏席位谱只支付极大全局私有遗漏；共享遗漏仍是主缺口。
8. 公屏 374 的链式同源再查询有严格局部投影改善但未闭合；公屏 385 的四主题/15 类型/二值重数全 `32767` 个六人实例无目标违例，只是有限证据；公屏 392 的七极大联合行族有精确负支持点，是方法障碍而非 SPE 反例。

## 代理自由探索的约束

所有代理收到同一目标和上述入口，不预先分工。可以重叠探索、改走完全不同的方法，但每次保存必须回答：新增了哪条真实 SPE 不等式、哪一类缺失 route 被闭合、或哪一份原模型全历史证书被核验。若只是松弛、局部菜单、浮点 LP、有限搜索或“必要条件坏点”，应明确写为障碍/有限证据，不提升主 Claim。

任何实质工作写入个人工作区 README/正文/代码，并用根 `work.py checkpoint`；只有回执 `status=pushed` 才算远端保存。不要打印或写入凭据。
