# Boss32 协作与恢复记录

- 研究存档：`customer-attraction`
- 主目标：`Q-CAG-HALF-6`，恰六名单位权提供者；任意有限单位客户集与有限共同目录；所有完整有序历史依赖纯 SPE；允许空主题、重复、零客户和任意平局；目标 `2W >= OPT_6`。
- 本 clone：`/workspace/scratch/3f81de614e46/co-work-anl-boss32`，分支 `main`，发布身份 `R-4ba33d9e7be24b0bb0303308d2bcb2ec`。
- 启动依据：附件 `work.py` 与仓库外凭据路径已自动识别；`work.py start --save customer-attraction --role boss` 已成功恢复并同步。凭据未写入此文件。
- 启动时同步的远端头：`2160176fc63aa811a6d9b0dd1360361cfcec6a55`。当前数学状态仍为六人 OPEN。

## 已读取的可靠入口

根 `README.md`、`RESEARCH_STATE.md`、`CLAIMS.md`、`FAILED_ROUTES.md`、`AGENTS.md`；
`research/current/customer_attraction/model.md`、`README.md`；
`research/customer_attraction/RESEARCH_STATE.md`、`FAILED_ROUTES.md`、`RUNBOOK.md`、`BOSS_START.md`；
五人精确证书 `research/current/customer_attraction/five_player_half.md`；
任意人数共同末位报价/隐藏回复投影 `research/current/customer_attraction/priced_hidden_reply_projection.md`；
同源回复再查询 `research/current/customer_attraction/same_source_reply_requery.md`；
近期六人停界、静态势障碍和尾利润投影的入口文件。

## 数学状态

五人 `CA-FIVE-HALF-EXACT-v1` 已有完整精确计算机辅助证明，内部复核通过，未记录外审；不能直接套到有背景五人后缀或六人。六人没有完整证明，也没有覆盖全部有序历史的原模型目标反例。已有六人必要行松弛点、静态势点、局部查询投影和有限无反例均不升级为目标结论。当前最重要未付义务是跨真实分支、早期位置、共同末位报价与尾利润之间的一次性共同付款。

## 子代理运行边界

按用户要求多次尝试启动平台允许的同一 `gpt-6.1-sol`、`ultra`、同一完整目标的研究代理。早先波次曾全部返回 `Selected model is at capacity`；本轮容量短暂释放后，`research15`--`research18` 已进入运行，且 `research15` 自主派生两席继续研究。没有降级模型或虚称启动。所有进入调度的代理均收到同一完整目标和下述去重简报；未预先指定证明/反例/实验路线。

## 接续动作

1. 轮询并读取本地子代理回报、公屏、收件箱及远端新提交；
2. 对任何候选只保留精确量词、对象、证据等级和未解决异议；
3. 有实质推导或可复现实验时写入个人工作区并用根 `work.py checkpoint` 保存，只有 `status=pushed` 才报告远端已保存；
4. 继续保持六人主目标 OPEN，直到取得完整证明、完整原模型反例，或确认运行边界下没有更多实质工作。

## 远端接续（同步至 e1cf5eab）

本次同步后读取了同行新推送的实质边界：

- `R-3257.../notes/root_supported_reply_bound.md` 给出任意人数的条件界；六人若目标失败，真实回复触及根遗漏的并集须满足 `|B|>W/5`。这是必要结构，不是六人证明。
- `R-ad571.../exhaustive_k4_binary.py` 对四主题、六人、全部 15 个非空二值客户类型重数 `{0,1}` 的 32767 个实例做完整纯 SPE 递推，零个 half 违例；这是有限证据，不是普适结论。
- `research/current/customer_attraction/six_maxima_joint_bound.md` 的精确证书覆盖全目录至多六个极大覆盖集；任意目录仍可能有七个或更多极大集，因此不能直接闭合本目标。
- `R-5c817.../parent/static_potential_barrier.md` 的静态势加实际末位报价点被倒二真实 IC 排除，不能当反例；六人目标仍 OPEN。
- `R-7f5d.../notes/q7_joint_row_obstruction.md` 给出七个极大主题、六人路由 `(0,0,0,0,1,0)` 上的精确 Farkas 停界：现有 41 条自然 mixed/末位 BR/末两位税行族不能直接推广到七极大情形。脚本逐列核验 1631 列与 17 个有理支持点；这是模板障碍，不是 SPE 反例。

这些材料均已区分为条件引理、有限观察或方法边界，没有升级为目标证明/反例。

## 2026-10-27 继续整理：七极大与去重简报

本次从远端 `bfa4f635` 同步至当前 `main`，读取并核对了 `R-c99d11e5...` 的六人小目录精确筛查、七极大 `seat` 停界、合法 aggregate-seat 候选和量词核对，以及 `R-ffea2744...` 的跨族末位包络、coverage-credit debt、二阶关联图候选和凸化障碍。给研究代理的共同简报如下，作为防重复边界而非方法白名单：

1. **已证但不足**：五人精确半覆盖；至多六个全局极大覆盖集的联合预算；真实全历史 IC、前缀预算、共同报价/隐藏回复投影；`OPT-W=L-E` 净差恒等式；根遗漏触及必要条件（六人若失败须有 `|B|>W/5`）。这些均不能直接覆盖 unrestricted 六人。
2. **已严格判死的辅助路线**：逐席 `seat(t,j,k)`（七个互不相交主题、私有质量 `(6,1,1,1,1,1,1)` 的完整 SPE 使根 `u_0=1` 而逐席行要求 `u_0>=6`）；按未来 route 计数的 seat 修复（完整 n=2 历史依赖续局反例）；静态势加实际末位报价（被倒二真实 IC 排除）；固定前缀归纳、逐期非负税、逐人静态安全值、SPE→静态 NE、残余匹配和有限无反例，均不得重新当作六人证明。
3. **仍开放且值得承重**：
   - 将七极大席位的合法第 `r` 大次序统计量改写成带分段/owner 排序的 aggregate row，并完成全部44缺失轨道的有理核验；当前统一 `K/(p_j+k)` 上界接入首次为负，不能直接使用。
   - 证明真实分支共同支付 `Delta<=E` 或较弱的 `RM-gap/UR-gap`，其中 `E` 是覆盖、重复和实际并集外客户形成的精确信用；必须保留真实后继与跨位置共享，不能冻结分母。
   - 完全换方法，但要保留原模型的全历史、平局、重复、空主题量词，并输出可复现精确证据。
4. **已有有限数据只作导航**：四主题六人 32767 个二值类型全 SPE 递推零违例；二/三主题六人筛查零目标违例；这些不是普适证明，也不是反例。

本简报已发给当前运行的代理及其自主派生席位；它们仍可自由换路线，但应把新产出落成正文和精确核验，不再重复上述已判死模板。

## 后续整理：条件界、文献和精确下界族

- `R-5ba0899f.../subagent_2/omitted_optimal_multiplicity.md` 及独立复核给出真实路径递推：对任意最优比较六元组，六人有 `I+D^*≤(6718464/2352949)W`。若该六元组中每个实际遗漏客户的比较重数至少为2，则 `OPT_6≤9071413/4705898·W<2W`；严格目标违例必须有 `D>W` 且大量单次遗漏。该引理只缩小反例结构，尚未支付单次遗漏。
- `R-6fadc22.../notes/position_aware_reply_bound.md` 保留真实强制分支的位置权重；六人严格违例须由较早位置触及遗漏客户产生的 `β(x)` 总惩罚超过 `W/6`。它不允许把互斥后继分支免费合账。
- `R-6fadc22.../notes/incidence_tau_six_boundary.md` 给出候选 `τ_inc≤8/3` 的结构半覆盖区域，但源动态预算仍待独立清洗，不能升级为定理。
- `all_b_m6/` 是完整精确的非违例下界族：六人、一个六客户大主题加五个 singleton，常值全选大主题是全部 55,986 项历史/偏离均满足 IC 的纯 SPE，`W=6, OPT_6=11, OPT/W=11/6`。它实现已知 `2−1/6` 下界但仍满足目标；不是反例。
- `orderstat_obstruction/` 是新的精确方法边界：七极大六人的旧 `M_t+L_j+T_{j,l}` 41 行族在 4064 literal columns 上有 8 轨道有理 Farkas 对偶，所有行平均非负而 base average `-2027846/107130789`，故该行族无法闭合 `U≤2W`。这不否定合法 order-statistic aggregate 行，也不是原模型反例；若 checkpoint 因自动审查拒绝，保留其本地状态并重试同步后推送。
- 文献笔记 `notes/arxiv_sequential_context.md` 仅作背景：Deng 等给出两代理 `3/2` 结果、更多代理 `2−1/m` 下界，并把上界2列为开放方向；其模型不替代本题完整全历史纯SPE量词。
