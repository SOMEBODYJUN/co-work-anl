---
id: "unrelated-machines/conditional-leaf-hall-shared-sink-review"
kind: "review"
type_tag: "审查"
title: "条件叶 Hall 与共享汇点联合审查"
status: "finite-evidence-classified"
truth_status: "finite-exact-audits-with-explicit-joint-feasibility-boundaries"
review_level: "full-json-read-and-cross-archive-comparison"
summary: "五个 unrelated-machines 冻结输出分别检查条件叶流的边际一致性、Hall 路径投影以及共享 sink 的有限 assignment oracle。它们保留 partial-z、zero-lambda、beta=1、空端点、巨大分母和非法合同边界；它们没有给出一般联合 LP 可行性、任意规模 Hall 定理、舍入算法或近似比。"
scope: "conditional leaf consistent marginals, Hall path projection, and shared-sink joint assignment audits"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:evidence/runs/unrelated_machines/conditional_leaf_consistent_marginals_independent.json"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:evidence/runs/unrelated_machines/conditional_leaf_consistent_marginals_independent.json"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:evidence/runs/unrelated_machines/conditional_leaf_hall_path_projection_independent.json"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:evidence/runs/unrelated_machines/conditional_leaf_hall_path_projection_independent.json"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:evidence/runs/unrelated_machines/conditional_leaf_hall_root_replay_scope.json"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:evidence/runs/unrelated_machines/conditional_leaf_hall_root_replay_scope.json"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:evidence/runs/unrelated_machines/shared_sink_joint_assignment_audit.json"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:evidence/runs/unrelated_machines/shared_sink_joint_assignment_audit.json"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:evidence/runs/unrelated_machines/shared_sink_joint_independent_audit.json"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:evidence/runs/unrelated_machines/shared_sink_joint_independent_audit.json"
source_ids:
  - "409bcd01bd377010b36d"
  - "e7c981ac171cf2eb2260"
  - "a36b4eba229032d2fb63"
  - "4fd6fc76e0fdb26ebf9c"
  - "998115b036c511c05ab7"
---

# 条件叶 Hall 与共享汇点联合审查

本页逐字段读取五个冻结 JSON，并把它们同 `unrelated-machines` 已有的 Hall、配置、私有 sink、三维匹配和 fractional-to-integral 障碍正文比较。前两份大输出研究一组条件叶的边际与 Hall 路径投影；第三份是只登记脚本重放范围的 root-scope 记录；后两份研究共享 sink、home/macro 与 tiny 任务的联合 assignment。它们使用 Fraction 或整数精确算术，但输出仍是有限审计。`PASS` 或计数相等不代替联合流证明，也不把同一边际的逐行构造误写成全局 joint distribution。

## 1. 条件叶边际一致性：三个 fixture 的精确字段

`409bcd01bd377010b36d` (`conditional_leaf_consistent_marginals_independent.json`) 保存三个命名 fixture，并在每个状态、叶、端口和资源上给出 `global_leaf_flow`、条件叶流、matching mixture、hole table 与机器负载。主族 `family_t2` 有 17 个 cores、40 个 leaves、64 个 resources、36 个 states；审计检查 1,440 条条件行、2,304 个条件列和 1,360 个 MC rows，分解出 176 个 integral matching pieces，每状态最多 6 片，`epsilon=1`。每个叶的典型全局边际是端口 0 为 (3/4)、端口 1 为 (1/4)，而每个条件列的 mixture 仍给出相同边际；这验证的是指定构造的 marginal consistency，不是存在一个对所有核心状态同时适用的统一 joint matching oracle。

同一源还保留两个小的语义回归 fixture：

* `partial_z_zero_lambda_d0_d1_d2` 有 2 cores、1 leaf、7 resources、3 states；检查 3 条条件行、18 列、4 个 MC rows、4 个 integral pieces，`epsilon=2/5`。它显式保留 partial (z)、重复的 zero-(lambda) 状态和 (d=0,1,2) 尾部；零状态不被删去，空的条件 matching 也作为合法输出记录。
* `beta_one_with_d2_and_zero_states` 仍为 2 cores、1 leaf、7 resources，但有 4 states、6 个 `beta=1` 状态、4 条条件行、24 列和 2 个 integral pieces，`epsilon=1`。其全局叶流为端口 0 的 0、端口 1 的 1；这说明 beta=1 与零状态可同时出现在合同中，不能由“通常的部分叶”假设悄然排除。

这些字段共同支持“在三个明确 fixture 中，逐条件行的分数流可由有限整数 matching pieces 复原，并保持指定边际”的有限结论。源没有给出任意核心数、任意叶度、任意 (z,lambda,d,eta) 的 LP 可行性判据；也没有证明条件 matching 的选择能在不同核心之间耦合成一个全局分布。`integral_matching_pieces` 是构造记录，不是对所有可行分解的最小值或复杂度界。

## 2. Hall 路径投影：大族与 toy 语义边界

`e7c981ac171cf2eb2260` (`conditional_leaf_hall_path_projection_independent.json`) 的独立 exact audit 使用一个 `t=2,D=4` 的 diffuse family：17 cores、40 leaves、64 resources、116 states、144 incidences、180 machines、201 jobs、404 finite entries，实际 assignment 的 peak 为 (3/2)。输出列出 36 个 (lambda) 状态、64 个 (z) 条目、80 条 global leaf-flow 边和 1,440 条 conditional leaf-flow 行；主族中每个叶端口的典型 flow 仍为 (3/4,1/4)。全部机器负载只出现 (0,1,3/2)，因此 (3/2) 是此固定输入的 exact finite peak，而不是一个无界族的阈值定理。

该源同时保存一个更小的 toy：旧 resources=6 扩为 7，加入 1 个 new leaf，(epsilon=2/5)，并显式标记 `partial_z=true`、`zero_lambda_duplicate=true`、4 个 explicit zero jobs 以及 (d=0,1,2) 分支；给出的 complete-tail schedule 覆盖 12 machines、18 jobs，peak 为 2。toy 的用途是回归接口语义：partial (z)、重复 (lambda=0)、零 job 和尾部状态都参与条件投影；它不是主族的更强 bound。

`a36b4eba229032d2fb63` (`conditional_leaf_hall_root_replay_scope.json`) 是同一 audit 的 root-scope 记录。它确认 canonical script 的 SHA、弱审计与 MC 审计的冻结 JSON 对比，以及“完整脚本已执行”的重放范围；它把范围写成：弱族为 180 machines/201 jobs/404 entries、actual peak (3/2)；MC 侧为 1,360 rows、1,440 conditional leaf rows、2,304 columns、176 full matching pieces，并保留 partial-z/zero-lambda/(d=0,1,2) 与 beta=1 fixture。该 scope 明确未测试 larger instances、general LP feasibility backend、joint-core/PSD constraints 和 computational hardness。它是程序/版本边界证据，不应被重新叙述成另一个数学证明。

因此，Hall 路径投影在本批只说明：在给定 diffuse family 和 toy 的路径结构中，逐叶条件流可以与指定 global marginals 对齐；它没有说明任意 Hall 子集都能同时匹配，尤其没有解决多个叶共享资源时的跨叶耦合。真正的 Hall theorem 需要写出资源集合、叶集合、所有条件状态的联合量词以及从局部 flows 到整数 assignment 的解码，这些字段在源中仍是未实现接口。

## 3. 共享 sink assignment：有限 oracle 与边界分层

`4fd6fc76e0fdb26ebf9c` (`shared_sink_joint_assignment_audit.json`) 使用 Fraction loads 与清分母后的整数 Hungarian/matching。它检查 500 个 cover-subset oracle cases、200 个 matching-permutation cases、600 个 random actual-schedule cases 和 235 个 random promised cases，并枚举了 155,915 个包含边界的实际 assignments；另有 10 个 invalid-contract cases。源自己把范围标为 finite independent subset/permutation/actual-assignment checks，不是一般证明或 novelty certification。

边界分类是该源最有用的独有内容。`sink_only_empty`、`empty_with_homes`、`zero_endpoints`、`home_only_tiny`、`sink_only_tiny`、`zero_cost_cover` 与 `large_tiny_requires_cover` 都在 promise 域中返回 `SCHEDULE`，即使 sink/home 集合为空、端点负载为零、或 tiny 任务只能落在单一端；`dummy_cost_is_essential` 保留了负载 `(1,1/2,1)` 的实际调度。相反，`positive_zero_target`、`macro_zero_target`、`infeasible_mandatory_home` 与 `infeasible_mandatory_sink` 返回 `REJECT_TARGET`，表示目标合同本身不满足 promise。`huge_rational_denominator` 使用极大有理分母且仍返回合法调度，说明实现确实走 exact Fraction，而不是浮点容差。

这些边界不能被压成一个“sink 总量充足则必有 schedule”的命题：同一审计同时保留 mandatory home/sink 的拒绝分支，且 `promise=false` 时拒绝是合同语义而非调度反例。`dummy_cost` 也说明一个空/虚拟目的地的成本项会影响可行判定；移除它不能作为无害简化。

## 4. 独立 residual-flow 复核与计数差异

`998115b036c511c05ab7` (`shared_sink_joint_independent_audit.json`) 用独立 residual-flow matching 与 exact Fraction/integer floor budgets 复核候选实现。它覆盖 39,200 systematic cases、2,000 random cases、14 invalid-contract cases，共 41,207 cases 和 593,913 actual assignments；标记 23,280 个 promised cases。候选实现统计为 25,252 successes，独立构造为 23,663 successes；去掉 `T`-feasibility 检查后，候选和独立路径分别有 1,972 与 383 successes。计数不能直接相除当作概率，因为 success 集包含边界和非 promise 分支，且两条路径的 rejection 语义不同；它们的价值是对同一输入合同的实现交叉检查。

独立输出保留七个边界名称：`no_home_empty`、`no_private_with_feasible_macro`、`zero_global_optimum_positive_target`、`positive_sink_rounds_to_zero`、`huge_denominators` 和 `empty_home_baseline_cost` 可被候选/独立路径接受；`no_private_infeasible_macros` 明确返回候选 `REJECT_TARGET` 且独立路径失败。最后一个失败分支说明“无 private sink”并不自动保证宏层可行，必须把 macro feasibility 作为输入前提；`T`-feasibility 与实际 sink assignment 是两个合同层。

两份 shared-sink 输出的共同结论是：在声明的有限域，候选与独立 matching 能在许多边界上保持一致，并能识别若干 promise 违反。它们没有证明任意共享 sink 网络的 residual-flow 充分性，也没有给出多项式算法、通用 integrality gap 或任意 (T,epsilon) 的近似比。特别是 independent constructor 的加性 sink budget 不是 actual zero optimum 的强保证；源明确把这一点列为 limitation。

## 5. 对象边界、比较和接续

条件叶 audit 与共享 sink audit 共享“分数边际先行、整数 matching 后验”的接口语言，但对象不同。前者固定 diffuse (t=2,D=4) 的叶/端口投影和条件 mixture；后者固定 home/macro/tiny/sink 的联合 assignment 与目标合同。不能用前者的 (3/4,1/4) 叶流替代后者的 sink capacity，也不能把 shared-sink 的 finite assignment count 反推为 Hall projection 的一般可行性。

与已有《Hall 联合流与前缀匹配增量审计》的关系是相邻增量：已有对象研究 group-level Hall flow、3DM completion 和一个 parity NO 的 fractional-to-integral gap；本页新增的 conditional-leaf 源只处理叶路径边际与同一叶条件 matching，shared-sink 源则提供另一组空端点/巨大分母/非法合同边界。它们不能合并成一条统一 Hall 算法。

与已有私有 sink 边际和树估值审查的关系也是接口级的：那些对象给出私有 sink 的最优值、分布或 signed-price 证据；本页的 shared sink 是 joint assignment oracle，且承诺条件以 macro feasibility、target 与 dummy cost 为核心。相同的词 `sink` 不表示相同的资源/量词。

若要接到一般理论，必须补齐四个可验证接口：

1. 对任意核心/叶/资源图写出联合 Hall 条件，并说明每个条件 flow 如何在所有核心状态上同时耦合；
2. 把 partial (z)、zero (lambda)、beta=1、零 job 和 empty endpoint 作为模型允许的状态，而不是预处理删项；
3. 对 shared sink 的 `promise`、`T`-feasibility、dummy cost 和 zero-target 逐一给出可判定量词，区分 `REJECT_TARGET` 与真实无调度反例；
4. 在随机/系统计数之外给出可复核的全局 assignment 解码，或明确保留为有限 oracle。

本页因此把五源处置为 `integrated` 的有限证据：它们适合回归测试、边界反例和后续 Hall/flow 证明的输入契约；没有把任何有限成功率、峰值 (3/2)、或 residual-flow 交叉计数写成当前 Q-CAG-HALF-6 的六人 SPE 结论，也没有宣称一般 unrelated-machines 近二结果。
