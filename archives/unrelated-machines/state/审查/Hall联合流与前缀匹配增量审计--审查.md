---
id: "unrelated-machines/hall-joint-flow-prefix-incremental-review"
kind: "review"
type_tag: "审查"
title: "Hall 联合流与前缀匹配增量审计"
status: "finite-audits-classified"
truth_status: "exact-finite-evidence-with-explicit-reduction-boundaries"
review_level: "full-json-read-source-export-and-cross-archive-comparison"
scope: "五份 unrelated-machines 冻结运行输出：Hall 组联合流、OPT promise 独立审计、joint matching completion、joint slot prefix rounding"
summary: "五源均已从 clean show 全文导出、读取并与已有需求树、配置、Hall 及 Kronecker 对象比较。它们支持精确 Fraction/整数的有限联合流与匹配回归，包含 4448、10122、8123 个有限实例族和一个 10 机 14 任务 parity 3DM NO 舍入证书。joint matching 的 reduction 使用 3DM 作为外部复杂度依赖，有限 JSON 不能独立承担 NP 完全性；joint slot 的实际全局例恰有 OPT=3/2，不能升级成一般近似界。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:evidence/runs/unrelated_machines/hall_group_joint_flow_audit.json"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:evidence/runs/unrelated_machines/hall_group_joint_flow_independent.json"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:evidence/runs/unrelated_machines/hall_group_opt_promise_independent.json"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:evidence/runs/unrelated_machines/joint_matching_completion_audit.json"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:evidence/runs/unrelated_machines/joint_slot_prefix_audit.json"
evidence_manifest: "../../tools/evidence/hall-joint-20261030/source-manifest.json"
---

# Hall 联合流与前缀匹配增量审计

## 1. 对象和证据层级

本页整理五个同源于 unrelated-machines 联合流/联合匹配线的冻结 JSON 输出。原件、blob、冻结提交、大小、SHA-256 和本地复制路径见 [source-manifest.json](../../tools/evidence/hall-joint-20261030/source-manifest.json)。本轮对每个 JSON 做了完整 `clean show` 导出和字段阅读，并把结果同已有的[未归档配置证书批次与量词边界](未归档配置证书批次与量词边界--审查.md)、[私有需求组合与共享三维匹配复制](../障碍/私有需求组合与共享三维匹配复制--障碍.md)、[分组超立方切片菜单的 Hall 保留](../定理/分组超立方切片菜单的Hall保留--定理.md)以及配置/张量审计逐项比较。

这些源分成两个数学接口。第一类把宏任务、半任务、组资格和目标 (T) 放进联合流/阈值 DFS；第二类把一个三维匹配或槽位前缀的分数证书落到实际整数匹配。它们都使用精确 Fraction/整数算术，并允许零目标、空任务、宏边剪枝、重复选槽和巨大分母等边界。`status: PASS` 只说明保存的有限运行完成，不能把有限枚举当作任意输入的 Hall 定理、通用 LP 求解器或近二近似算法。

特别要分清三种量词：

* `hall_group_joint_flow_audit` 与其独立输出只覆盖写明的有限参数域和明确 fixture；它们没有对无界 (q)、宏时间或所有资格图做穷尽。
* `joint_matching_completion_audit` 的 JSON 把 universal reduction proof、经典 perfect3DM 困难性和有限代码审计分开；有限 reduction instances 不是 NP 完全性证明。
* `joint_slot_prefix_audit` 只有一个实际 parity 3DM NO 输入的全局舍入证书；局部 single-row envelope 的大分母抽样不能推出所有全局 LP 的整数化界。

## 2. 五个源的逐项内容与去向

| 源 ID | 冻结输出与实际阅读 | 独有数学内容 | 处置 |
|---|---|---|---|
| `6b44adbc694f4eb1778f` | `hall_group_joint_flow_audit.json`，3455 字节；精确整数/Fraction，9 个命名 fixture 和五个有限参数族 | 基础域 4448 例，其中 (T)-feasible 2278、successful 2773、reliable rejection 1675、非均匀零 job 228；varying-macro 域 10122 例、2071 个 (T)-feasible、2650 个 output；3991 个 unknown-OPT-promise 例；2079 个公式检查；保存非 matroid 可行独立集 (arnothing,{0},{1},{2},{1,2})，明确没有无界穷举和 uniform-(arepsilon) 结论 | integrated 到本页的 Hall 联合流有限审计；不新造统一近似定理 |
| `5fc9e049f0a8a7aaaaed` | `hall_group_joint_flow_independent.json`，439 字节；另一段阈值 DFS 汇总 | 8123 例，原矩阵 (T)-feasible 3688，success 4066，rejection 4057，显式非法拒绝 7；`proof_scope` 明确是 finite original-matrix threshold DFS，**没有 Hall oracle** | integrated 为独立实现证据；不冒称独立一般证明 |
| `2848badca09c5d4df4d8` | `hall_group_opt_promise_independent.json`，518 字节；精确原始 job subset-sum/threshold enumeration 加联合选择 DFS | 301 个 sampled inputs 中 122 个满足 exact-OPT promise 且全部成功，只有 1 个 `strict_t_less_than_OPT_cases`；使用 Fraction/int 和 exhaustive joint-choice bottleneck 检查 | integrated 为 promise/反例边界回归；不能据 122 例把 promise 推广到所有输入 |
| `bc969f57611eec4af74d` | `joint_matching_completion_audit.json`，35048 字节；含 conditional-interface、unique-small-and-block、independent、50 个实际 q=3 tripartite sample 及限制 | 3DM reduction 有 309 例、194 yes、24927 个 exhaustive oracle nodes；q=0,1,2 全 hypergraph 枚举 1、2、256，q=3 仅采样50；block cuts 检查 (k=4,5,6,ldots,64) 的阈值 (7/4,9/5,11/6,ldots,127/64)，并记录 (delta=1/3) counterexample；独立 path-orientation 计数 (8,32,128,512,2048) | integrated 到联合匹配完成审查；把 3DM 复杂度、局部 interval algebra 和有限搜索各自保留 |
| `12b601da50cee4eab718` | `joint_slot_prefix_audit.json`，8638 字节；局部前缀审计和一个全局 parity 3DM NO 舍入证书 | single-row envelope 83810 tested pairs、39673 feasible、38279 positive-support，另有10000 seeded large-denominator samples；实际 10 机14 job，`perfect_3dm_count=0`，Fractional loads 全为1，ST loads 含两个 (3/2)，实际 `OPT=3/2`，并保留完整14项分数证书和整数 assignment | integrated 到前缀/舍入障碍；明确这是一个全局实例和局部 envelope，非通用 LP/近似定理 |

## 3. Hall 联合流：有限域、边界和实际含义

`6b44...` 的审计以 (h=1..3)、半任务数 (k=0..2)、宏边数 (blemin(2,h))、所有宏支持/共同组资格图为基础；固定 (q=2,delta=1/2,W=1)，含两件 half jobs 和 macro (3/4)。非均匀域改用 (q=3,delta=1/3)、group weights ((0,1/3,1/3,1/6))、macro (2/3)；varying 域让宏时间取 `None, 3/5, 1, 5/4` 的所有行组合（排除全 None）。这些描述说明输出确实覆盖了零宏、强制 home、宏边变化和资格图变化，但仍是显式有限域。

基础域有 4448 个枚举输入。`T_feasible=2278` 与 `successful_outputs=2773` 不应被理解为“所有可行输入都输出”：输出计数还包括命名 fixture 和其他分支，审计自身没有把计数声明为一般完备性。`reliable_rejections=1675` 是程序在原矩阵下可靠拒绝的分支；`nonuniform_zero_job_cases=228` 单独保留零 job 语义。varying-macro 域再给出 10122、2071、2650 三个计数，unknown-OPT-promise 3991 例则明确把真实 OPT promise 作为额外前提，不可回填到所有源输入。

审计的 2079 个 formula cases 与 9 个命名 fixture 适合检查分母、空任务、零目标、宏边剪除、重新选槽和大 (q) 的算术。输出写明所有值由 Python Fraction/integer 计算，无浮点误差；也写明“no general UM structure extraction or uniform epsilon for unbounded q”。因此本批新增的是可复核的参数边界和失败机制，不能从计数外推一个无界 Hall 保留比例。

`5fc9...` 提供不同汇总路径：8123 个 finite original-matrix instances，原 (T)-feasible 3688，成功 4066、拒绝 4057、显式非法 7。它的 `proof_scope` 直接否认 Hall oracle；这使它适合当实现交叉检查，不足以把 threshold DFS 改名成多项式算法或证明。`2848...` 进一步把候选输出和真实 OPT promise 分开：301 个采样输入中仅 122 个满足 exact OPT promise，全部 122 成功，只有 1 个严格 (T<OPT) 例。该严格例是应保留的障碍信号：候选阈值与实际最优值不能无条件互换。

审计还保存了一个非 matroid 的可行独立集族
\[
\varnothing,\{0\},\{1\},\{2\},\{1,2\}.
\]
这阻止把可行组/选择结构直接套用 matroid exchange；若需要统一算法，必须另给交换或流可行性的证明。该事实是有限输入中明确导出的结构观察，不是说所有 Hall 家族都非 matroid。

## 4. Joint matching completion：3DM reduction 与 block cuts

`bc969...` 的大 JSON 记录三个代码入口：`joint_matching_completion.py`、`unique_small_matching_audit.py`、`joint_matching_completion_independent.py`，并固定了五个源码 SHA。其 conditional interface 使用 Fraction、没有浮点 solver，309 个 reduction instances 中 194 个 yes，oracle search nodes 为 24927。独立 small/block 部分把 (q=0,1,2) 的 tripartite hypergraph 分别全部枚举为 1、2、256 个，另取 50 个 (q=3) samples；实际 scheduling backtracking nodes 为 2,438,807，检查 `every_job_exactly_one_small=true` 和 `N_empty=true`。

这里的数学桥是：一个条件接口把有限 3DM 选择映射到联合匹配/槽容量问题，另有 Fraction rounding cases 检查给定阈值下的负载。JSON 明确警告：NP-hardness 依赖 universal equivalence proof 与经典 perfect3DM hardness，有限 checks 自己不证明 NP-completeness。故本页只把这些字段登记为“有限实现对照 + 证明所需的外部依赖”，不写成新复杂度定理。

block cuts 的族参数从 (k=4,h=3,T=7/4) 开始，经 (k=5,T=9/5)、(k=6,T=11/6) 延伸到 (k=64,T=127/64)；所有记录的 threshold-cut coefficient 为0。独立 path-orientation 检查的 star-escape patterns 随 (k=2,3,4,5,6) 为 (8,32,128,512,2048)，exact interval checks 在 (k=4,5,8,16,32,64) 上均给 (r) at threshold 为1。这些数值支撑特定 shared-(z) 家族的区间代数和路径方向枚举；JSON 的 limits 同时明确 interval algebra 只属于该识别出的族，不能推广为一般调度约束。

`delta_one_third_counterexample=true` 是本批最重要的负向信息之一：当 (delta=1/3) 时，已有某个 block-cut 候选被明确击穿。它不是所有参数都失败的证明，但足以阻止把 (delta=1/2) 的局部阈值经验静默改写成任意 (delta) 的统一保值。后续若要修复，必须给出新的 block 接口、全局 assignment 和每个低负载输出的解码。

## 5. Joint slot prefix：局部 envelope 与全局 parity 证书

`12b601...` 的 local prefix audit 以单行 slot envelope 为对象：0--4 jobs 的 `{1,3/2,2}` rows，half-integral (x)，half-integer targets (1/2,ldots,5)，再加 10000 个有理大分母边界样本。83810 个 tested pairs 中 39673 feasible，38279 positive-support；所有算术是精确 Fraction，无 tolerance。该统计支持程序在声明域内的行级检查，不能替代多行联合匹配的全局 Hall 条件。

其实际 global certificate 是一个 parity 3DM NO 输入：10 台机器、14 个 jobs、无 perfect 3DM。Fractional certificate 让每台机器的 fractional load 都等于1；独立 ST/整数 assignment 的 machine loads 为
\[
(1,1,1,3/2,3/2,1,1,1,0,0),
\]
并给出 `OPT=3/2`。完整 assignment 为
\[
(0,0,3,4,1,1,2,2,7,3,6,4,5,5).
\]
因此这个输入展示了“局部所有行看似可控、全局整配仍需付出 (3/2)”的具体障碍。`perfect_3dm_count=0` 只针对该输入；它不证明所有 parity NO 或所有 fractional load 1 的实例都有相同 OPT。

局部与全局证书的关系是诊断关系：single-row envelope 可检查每个行内分数支持，global assignment 还必须满足跨行的任务唯一性和资源容量。不能用单行的 83810 次检查替换 14 个任务的全局 Hall/3DM 约束。

## 6. 与既有对象的关系、独有内容和接续

* 与[未归档配置证书批次与量词边界](未归档配置证书批次与量词边界--审查.md)的关系是增量证据。旧批已有九个 `hall_group_joint_flow_cases` fixture 的边界摘要；本批的 `6b44...`、`5fc9...`、`2848...` 提供更大有限参数域、独立 DFS 计数和 exact-OPT promise 对照，并保留原件字节。九例旧摘要与本批不合并成一个“统一算法”结论。
* 与[分组超立方切片菜单的 Hall 保留](../定理/分组超立方切片菜单的Hall保留--定理.md)的关系是证明接口相邻而非同一对象。分组超立方定理的 Hall 并集计数给显式状态选择下的 (C\le3/2) 调度；本批联合流/3DM 输出研究共享资格、联合 threshold 和前缀配额。不能把前者的乘积切片假设默默加入后者，也不能把后者的有限成功率升级成前者的普遍 (c_d) 界。
* 与[私有需求组合与共享三维匹配复制](../障碍/私有需求组合与共享三维匹配复制--障碍.md)的关系是共同的 3DM/分数到整数障碍。旧对象证明完全元素池会把分数完美匹配整数化、导致 NO→YES；本批 `joint_slot_prefix` 以另一个 parity NO 输入展示 fractional load 1 与实际 OPT (3/2) 的落差。两者共同提醒：必须同时证明全局整数一致性和输出解码，不能只看局部分数支持。
* 与已有 Kronecker/tensor 反例的关系是负向验证：`delta_one_third_counterexample` 与 parity 3DM certificate 都阻止用一个局部参数样本冒充任意 tensor/block coherence。它们没有新增一份“更高阶 tensor”定理。

接续研究若要把这条线推进到一般结果，需要逐项补齐：联合资格图的统一 Hall/flow 证明；当真实 OPT 未知时的 promise 去除或可验证条件；δ 变化下 block cuts 的全量证明；以及从每个低于阈值的整数调度反解 3DM 或其他源见证的统一解码。当前五源只完成有限审计、交叉实现和明确障碍记录。

## 7. 逐源处置结论

五源均已实际全文读取、保全字节、核对 JSON 有理数结构并与全仓对象比较。`6b44...`、`5fc9...`、`2848...` 合并为 Hall 联合流有限审计对象，同时分别保留主审计、独立 DFS 和 exact-OPT promise 的独有内容；`bc969...` 保留 3DM reduction、block cuts、独立 path orientation 和复杂度依赖；`12b601...` 保留 single-row envelope、全局 parity NO 和具体 assignment。没有因旧、有限或不在当前主线而丢弃源，也没有把任何有限成功计数写成一般定理。
