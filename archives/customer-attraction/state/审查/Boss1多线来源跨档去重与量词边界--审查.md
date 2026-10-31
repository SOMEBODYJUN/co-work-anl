---
id: repository-cleanup/boss1-multi-lane-cross-source-audit
kind: review
type_tag: 审查
title: Boss1退役多线来源的跨档去重与量词边界
status: draft-cross-source-audit
summary: 完整读取五份 Boss1 当前退役 topic-selection 冻结源，核对 atomic/weighted-congestion、fair-allocation、resource-activation、bottleneck-knapsack、budget-games 与 local-potential-games 的现有对象；给出逐源处置建议、独有内容去向及不能合并的量词边界。
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:history/retired_topic_selection/multi_lane/research/topic_selection/FAILED_ROUTES.md
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:history/retired_topic_selection/multi_lane/research/topic_selection/candidate_pool.json
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:history/retired_topic_selection/multi_lane/research/topic_selection/lanes/fair.md
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:history/retired_topic_selection/multi_lane/research/topic_selection/lanes/gap.md
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:history/retired_topic_selection/multi_lane/research/topic_selection/lanes/nash.md
source_ids:
  - a6641af55f2036d64c0a
  - 58d0751a06d2b99edbd9
  - e341a8cf73b1d0385717
  - 2e5a9f373be7adbd8030
  - a177ad0d3653d7eaf428
source_sha256:
  - e6573bedc3edae2468dbc170317949b5f8d9f2ca4777d3e64378f4be8db5094e
  - d37099039588ceadf0b2dfceae689f4def554728063e56c62ebf2e5523a610c6
  - 5bda1ca4fab88dda59d3274e4cd82e7b2a568cbff74183b8abb21c64fcfd782c
  - 8e14e6d6525cc353091aa0484c6c72dc447f581d6227d6232fb3f960db06b68e
  - 69026c488b16be1abbf73105e001b4ad29269062e0012ed82f5c60c7c2fd2d6c
review_level: full-source-read-and-cross-archive-scan
---

# 阅读范围

五份源均从冻结提交 `68fad804ec5946cb296f77dc5b336308a66abf12` 导出并完整读取；当前源大小依次为 4493、85125、24784、29238、16446 字节。`candidate_pool.json` 解析为 59 条候选：atomic 14 条、fair 20 条、gap 19 条、nash 6 条。候选状态不是数学真值；`exclude` 是当前选题排除，`probe` 是已有有限证明/实验入口，`reserve` 和 `needs_verification` 仍是候选或待排重。

现有结果树已含若干同题正式对象，故本批不应再造同名定理。最关键的已覆盖目标是：

- `archives/weighted-congestion/state/反例/两玩家二策略无纯均衡--反例.md`：独立四状态正二次成本反例，已经给出 AG-01/AT 类候选只能作选题背景，不能从有限反例推出 PLS-hard 或一般无 PNE。
- `archives/weighted-congestion/state/审查/原子拥塞重选题与失败路线--审查.md`、`archives/weighted-congestion/state/资料/原子拥塞候选线与37-33小证书--资料.md`：atomic 候选、37/33 与 64/59 权重势模板、旧全类量词边界已分开保存。
- `archives/customer-attraction/state/审查/多线候选池逐卡量词与去重边界--审查.md`：当前代理已将 59 条 JSON 逐卡量词和状态整合；`archives/fair-allocation/state/审查/多线候选池实际比较与去重边界--审查.md` 仍是另一版本的排序/尺度摘要，不能把摘要文件当候选 JSON 的逐条替代。
- `archives/resource-activation/state/资料/两列射线启用值的二维分类与全维充分性--资料.md`：gap/GA01 的真正分数 LP 三列反例、二维 iff 与全维充分性已有自足正文；当前 `gap.md` 的重复证明不应再建同定理。
- `archives/budget-games/state/定理/分段线性凹偏好的共享超梯度合并判别--定理.md`、`archives/budget-games/state/等价/共同形状可分凹偏好的对数边际规划--等价.md`、`archives/budget-games/state/资料/克隆识别与Leontief均衡的不同恢复接口--资料.md`：nash/NA02–NA04 的 Leontief/Fisher、polyhedral clone 与共同形状 KKT 已有独立对象。
- `archives/fair-allocation/state/审查/退役公平家务有限证据三源处置--审查.md` 与相邻 generator/toy review：fair lane 的 rank/图定向有限证据已有处置，但其模型与 chores rank、signed endpoint graph 不能互换。

# 逐源处置建议

## `a6641af55f2036d64c0a`：`FAILED_ROUTES.md`

建议 `integrated`，但必须按章节拆分目标并保留原件，不可单一复制到 weighted-congestion。当前源相对于已完成的 independent-review FAILED_ROUTES（SHA `efb40503...`）不是字节重复：它新增 NA02 Leontief/Fisher 覆盖、37/33 被 64/59 支配、重边内部平分反例、两尺寸 knapsack 均匀化/Poisson 拆分障碍、配置预算伪新常数、WEFX+fPO 不相容、additive chores EFX 反例及 EFX→Pareto 补全反例。建议去向：

| 章节 | 建议对象/证据 | 语义状态 |
|---|---|---|
| NA02、克隆/Leontief覆盖 | `archives/budget-games/state/资料/克隆识别与Leontief均衡的不同恢复接口--资料.md` | 已有已知工具重构；不把原作者仍写 open 当团队新解 |
| 37/33、有限权势排雷 | `archives/weighted-congestion/state/资料/原子拥塞候选线与37-33小证书--资料.md` | 37/33 只限模板/人数；64/59 与全类下界独立 |
| 重边平分、原子失败路线 | `archives/weighted-congestion/state/审查/原子拥塞重选题与失败路线--审查.md` + `tools/evidence/atomic-games/FAILED_ROUTES.md` | 只限制特定压缩合同；不能外推一般 FPT/无算法 |
| 向量 LP/配置/GAP | `archives/resource-activation/state/资料/两列射线启用值的二维分类与全维充分性--资料.md`；`archives/bottleneck-knapsack/state/审查/广义指派候选池的状态与证据边界--审查.md` | 真实分数 LP、配置 LP、整数 knapsack 分开 |
| chores/EFX/WEFX 与 Pareto | `archives/fair-allocation/state/审查/多线候选池实际比较与去重边界--审查.md` 及 fair-chores finite-evidence reviews | 反例只针对注明删除语义、人数和成本域 |

该源仍有跨档独有价值：它记录“排除原因、保留工具和何种条件变化时重开”，而不是新定理。若不能一次把各章节的完整承重内容补进现有对象，应先 `retained` 到 `archives/repository-cleanup` 的历史审查，再在后续批次拆分；不能 `duplicate`。

## `58d0751a06d2b99edbd9`：`candidate_pool.json`

建议 `integrated` 到 `archives/customer-attraction/state/审查/多线候选池逐卡量词与去重边界--审查.md`，并把原 JSON 及 SHA 放入 `archives/customer-attraction/tools/evidence/retired-candidate-pool-20261031/` manifest；fair-allocation 的 `多线候选池实际比较与去重边界--审查.md` 仅作既有排序版本交叉引用。它是 59 条候选的机器可读逐项登记（atomic 14 / fair 20 / gap 19 / nash 6），而现有多线审查只引用 BATTLE 摘要且正文只点名少数 ID；两者不是逐字重复。应保留每条 `id/title/status/exact_question/known_overlap/fatal_risk/result_file`，但候选状态不可进入 theorem tree。

状态分布：atomic `reserve=6, needs_verification=5, exclude=3`；fair `reserve=10, needs_verification=6, probe=4`；gap `reserve=12, needs_verification=3, probe=1, exclude=3`；nash `reserve=4, probe=1, exclude=1`。后续清洗以该 JSON 的精确字段为索引，BATTLE 的排序只作为版本化比较，不改写原 ID 或量词。

独有接续是候选来源/方法/停止条件图：AT/FA/GA/NA 的 `known_overlap` 明确指出哪些是标准工具风险、哪些有限证据、哪些应先查文献。建议第三阶段只建“候选→正式对象/排除理由”关系，不把候选之间串成证明链。

## `e341a8cf73b1d0385717`：`lanes/fair.md`

建议 `integrated` 到 `archives/fair-allocation/state/审查/近似公平分配首轮候选池与边界--审查.md`，并把 complete multipartite 命题独立放入 `archives/fair-allocation/state/引理/完全多部图均匀最大EF1--引理.md`；不能只标 duplicate。它的独有数学内容不在候选标题，而在实际证明/实验边界：

1. complete multipartite conflict graph 上 uniform maximal EF1 的完整构造证明（按 part size 前缀拆成大小 1/2 bundle）；这是条件模型的自足证明，但来源自己也说明新颖性未核，不能升级为任意 graph/cactus 定理。
2. He–Tao 四人三值 chores 反例的 62,720 个 labelled type-count allocations、142 个删除子实例、473 个整数 `(r,L)` 点及 21 个失败点；这是有限复核，不能写成实参数区域定理或“13 件最小”全称结论。
3. complete multipartite 构造的 343,536 个整数 partition×人数核验；这是证明实现检查，不能替代证明。
4. F01/F03/F11 三条研究合同的停止条件和模型边界。F03 的 cactus 方向必须与 signed endpoint graph 的双三角有限反例分开；F11 的 two-size budget chores 必须保留 housekeeper/feasible-subset 量词。

建议把实验输出 `probe_results.json`、`trivalued_grid.json`、`deletion_subinstances.json` 作为 evidence 资源对象；若未找到原件，只保留来源中的精确计数和“需重取原脚本”的说明，不凭摘要补造。与已有 `fair-chores` finite-evidence review 的独有差异是：本源有 13 件三值固定成本删除极小性和 complete-multipartite 证明，旧 JSON review 只有另一组随机 profile/图定向/秩二抽样。

## `2e5a9f373be7adbd8030`：`lanes/gap.md`

建议 `integrated`，拆为 resource-activation 的数学对象和 bottleneck-knapsack 的候选审查，不建立“GAP 总定理”。已有 `archives/resource-activation/state/资料/两列射线启用值的二维分类与全维充分性--资料.md` 已包含 §4 三列 Fraction 反例、二维必要性和全维两射线充分性；当前源的自足证明应作为 source_ref/版本证据接入，而非重复对象。GA02/GA04/GA06–GA15 的候选定义、文献接口和停止条件接入 `archives/bottleneck-knapsack/state/审查/广义指派候选池的状态与证据边界--审查.md`，并保留 GA03/GA05/GA16 的排除理由。

`gap.md` 另有 reserved-capacity greedy 引理
\[
f(S)\ge [1-e^{-(\rho-\delta)}]OPT
\]
（成本每件≤δB、返回成本≤ρB、单调子模，按 marginal density 选到不能加入为止）。这是标准分析的完整自足推导；可作为 bottleneck-knapsack `state/引理` 的候选，但必须注明“未查新颖性、未证明 tight”，不能把它和 Group GAP 1/19 或任意配置 LP 比值混合。

## `a177ad0d3653d7eaf428`：`lanes/nash.md`

建议 `integrated`，按候选实际模型拆到 budget-games、local-potential-games 与 weighted-congestion：

| 当前卡 | 建议去向 | 去重/边界 |
|---|---|---|
| N1/NA01 cactus 玩家特定 singleton 拥塞随机 BR | `archives/local-potential-games/state/资料/Nash候选...` 新版本或补充对象 | 树/单环已有 O(n²) 事实；一般猜想状态未穷尽，不能称开放已认证 |
| N2/NA02 weighted Leontief bit-poly NE | `archives/budget-games/state/资料/克隆识别与Leontief均衡的不同恢复接口--资料.md` | 已有 NE=Lindahl/Fisher 接口；不能把 AAMAS 仍写 open 当新解 |
| N3/NA03 polyhedral clone invariance | `archives/budget-games/state/定理/分段线性凹偏好的共享超梯度合并判别--定理.md` | 当前对象已有 2^R poly(R,m,L) 识别与三项目反例；一般凹效用不覆盖 |
| N4/NA04 common-shape separable log-gradient | `archives/budget-games/state/等价/共同形状可分凹偏好的对数边际规划--等价.md` | 只覆盖共同 f、正估值；不能外推 player-specific f_i 或精确有理算法 |
| N5/NA05 nonconvex NE social-cost selection | `archives/local-potential-games/state/资料/Nash候选...` 新版本 | 任意 NE 可构造不等于在非凸 NE 集上做社会成本选择；候选/未解义务 |
| N6/NA06 two-type pair-strategy PNE | `archives/local-potential-games/state/资料/Nash候选...` 与 atomic candidate review 交叉链接 | 对称 size-2 global Min Potential 的 NP-hard 不等于任意 PNE 搜索硬度；不能用两玩家四状态 toy 代替复杂度证明 |
| N7/FT-SMOOTH | `archives/weighted-congestion/state/审查/原子拥塞重选题与失败路线--审查.md` 或新增 weighted 动力学资料 | 仅当近似势与 smoothed 动态的桥完整证明后才升级；黑盒拼接不算独立结果 |

# 必须保留的量词冲突

1. **候选排序 vs 数学真值。** `candidate_pool.json` 的 `reserve/probe/exclude` 是选题状态；不等于定理、反例或全球新颖性。BATTLE/lanes 的排序与后续对象必须保留版本时间点。
2. **全局最小势、任意 PNE、存在 PNE。** atomic/NA06 中一般 size-2 global potential minimization NP-hard；这不能推出 local PNE search PLS-hard，也不能由一个 no-PNE toy 推出任意规模 no-PNE。
3. **有限 profile vs 全域。** fair lane 的 62,720/142/473/343,536、fair-chores 的随机 profile、gap 的 8 个启用集和 nash 的 25 anchor/有限动态都只支持具体编码域；空 witness 不推出一般存在。
4. **模型身份。** signed endpoint graph 的 EFX^+_0、rank-cap-2 chores、uniform maximal partial coloring、budget chores EF1、CAG/SPE、weighted congestion PNE 各有不同 bundle、删除、成本和均衡定义。不能从 cactus 一种模型的反例转到另一种。
5. **已知覆盖与候选延续。** NA02 Leontief/Fisher 已有工具重构；GA01 二维 LP 已有内证；N3/N4 已有自足对象。后续只保留未覆盖的量词或新结构，不以“旧报告仍写 open”重开。

# 交接动作建议

正文与必要 evidence 先由 Boss1 串行 checkpoint 推送，再分别对五个源提交 `clean done`；每条 receipt 应说明：完整读取、与哪些正式对象逐项比较、独有内容去向、未升级的量词理由。若当前工作区不能一次拆分 `FAILED_ROUTES.md` 的跨档章节，先记录 `retained` 并在 receipt 中列明待拆分段落，禁止标 `duplicate` 或直接 `retired`。
