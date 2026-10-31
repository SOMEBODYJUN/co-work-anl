---
id: "unrelated-machines/input-fixtures-dualrail-hs-hall-incremental-review"
kind: "review"
type_tag: "审查"
title: "双轨、HS 贪心与 Hall 联合流输入三源增量审查"
status: "integrated-scoped-fixtures"
truth_status: "exact-input-read-with-existing-proof-and-finite-audit-boundaries"
review_level: "full-clean-show-read-and-cross-archive-comparison"
summary: "完整读取三个此前未勾选的 unrelated-machines 输入源：四条 A=2 双轨重复 occurrence、三机一大八小 HS 输入、九个 Hall 联合流/宏任务 fixture。它们的独有内容是可复现的原始输入与边界参数；双轨和 HS 的承重结论已有正文，Hall 的一般结论仍限于已有有限审计。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:examples/unrelated_machines/dual_rail_scalar_and_unit_sharp_input.json"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:examples/unrelated_machines/dual_rail_scalar_and_unit_sharp_input.json"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:examples/unrelated_machines/full_hs_m3_input.json"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:examples/unrelated_machines/full_hs_m3_input.json"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:examples/unrelated_machines/hall_group_joint_flow_cases.json"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:examples/unrelated_machines/hall_group_joint_flow_cases.json"
source_sha256:
  - "4cea6fd3f6d653db85b89e4993019983ecac7dee5c2b99eff48e116656f543af"
  - "fc10ef86519740b9178bfc91dd22475e24fc1cf2dde373aa426ad32a0d361e62"
  - "169e3e2e5c7d07828587df471f7c422ce95631b597fbce9a4e8263795c542322"
---

# 1. 阅读、冻结和来源身份

本批用 `work.py clean show` 从冻结提交导出并逐字读取三个 JSON；没有用结果树中的旧摘要代替输入本身。三个路径在 `legacy-cleanup` 提交 `68fad804ec5946cb296f77dc5b336308a66abf12` 与 `main` 提交 `aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c` 均存在且内容相同，所以每个源版本只保留一份数学身份，并在来源字段中保留两处冻结定位。

| 源 ID | 冻结路径 | SHA-256 | 本批独有身份 |
|---|---|---|---|
| `375c2a556cc044d50832` | `examples/unrelated_machines/dual_rail_scalar_and_unit_sharp_input.json` | `4cea6fd3f6d653db85b89e4993019983ecac7dee5c2b99eff48e116656f543af` | 四个 `A=2` clause 的具体重复 occurrence 双轨实例 |
| `6b9edb3477e3323c4725` | `examples/unrelated_machines/full_hs_m3_input.json` | `fc10ef86519740b9178bfc91dd22475e24fc1cf2dde373aa426ad32a0d361e62` | 三机、一个 1 与八个 `1/4` 的 full-HS/rank-one 对照输入 |
| `50558e252eca7ba30f02` | `examples/unrelated_machines/hall_group_joint_flow_cases.json` | `169e3e2e5c7d07828587df471f7c422ce95631b597fbce9a4e8263795c542322` | 九个共同资格、宏任务、空目标和大分母 Hall fixture 及其完整矩阵 |

这些源不是 customer-attraction 六人 SPE 的输入；它们保留在 `unrelated-machines`。本页是输入资源的增量审查，不把源文件误写成新的普遍定理。

# 2. 双轨标量与单位锐例输入

## 2.1 精确输入

文件给出变量 `x,y,z` 和四个 clause；每个 clause 的外机容量 `A=2`，occurrence 顺序和符号为：

1. `(x+, x+, y+)`；
2. `(x-, x-, y+)`；
3. `(y-, z+, z+)`；
4. `(y-, z-, z-)`。

因此每条变量符号轨恰有 `K=2` 个 occurrence。重复 occurrence 是不同 job，不应被压缩成一次字面；每个 port 在轨上使用 `1/K=1/2`，在 clause 外机上使用 `1/A=1/2`，selector 在两条轨上可用时为 1。该 JSON 没有隐藏赋值、随机量或外部容量字段，适合直接喂给双轨审计器。

## 2.2 与既有双轨对象的比较

现有《双轨阈值实际前沿与逐行均匀相关防护双源审查》及 `threshold-bundle-20261030` 的 `dual_rail_threshold_soundness_boundary_audit.json` 已把这四条 clause 作为“重复 occurrence 三半锐例”。本次逐字段比较确认：变量名、符号、`A=2`、每轨计数、重复 occurrence 语义均一致；没有一个新参数可以形成第二个模型。故本源的数学去向是：

- 作为 `UM-NORMALIZED-DUAL-RAIL-UNIVERSAL-THREE-HALVES-v1` 的可复现 sharp input，保留严格源无解与实际 `OPT=3/2` 的边界；
- 作为 split-capacity 版本的同一符号模板输入，但 split unit 外机改变机器合同，不能把两种 OPT 证书混称；
- 作为完整双轨正文中“弱端阈值不能自动解码”的具体 witness；它不能单独承担通用三半证明、一般 `UM-TARGET-v1` 复杂度或 customer-attraction 结论。

由符号矛盾可直接检查严格源无解：前两条若取 `y=true` 会同时要求 `x=true` 与 `x=false`；若取 `y=false`，后三、四条会同时要求 `z=true` 与 `z=false`。这只是源端 NO 性质；实际调度的三半上界和下界来自已入库的双轨正文与有限证书，而不是从本 JSON 自动推出。

# 3. 三机 full-HS 输入

## 3.1 输入合同

`full_hs_m3_input.json` 明确固定：

- `machines=3`，目标阈值字段 `T="1"`；
- 任务 0 的处理时间为 `(1,1,1)`；任务 1 至 8 的处理时间均为 `(1/4,1/4,1/4)`；
- 顺序是 `[0,1,2,3,4,5,6,7,8]`，tie-break 为最小机器标签；
- `moment_distribution` 的支持是所有 makespan-one 调度，共 210 个，权重为 `1/210`；
- 初始化为 `K=identity on full V1`；score 是 `tr((Ae K)^dagger(Ae K)) with moment Gram adjoint`；更新为 `K <- Ae K`，明确没有 square-root 归一化或 rank-one 初始化。

`jobs` 中的九行和 `job_order` 逐项核对，确认大任务先于八个小任务，且没有额外背景负载。`T=1` 与 true optimum=1 的关系由已有审计证书核验；本输入本身不声称一个新的最优性证明。

## 3.2 与 HS 审计的关系和承重边界

现有《循环路径、归属单位环与 HS 贪心有限审计》及 `cycle-path-hs-20261030/hs_effect_greedy_exact_m3_audit.json` 已对这份输入给出：full-HS 在指定顺序和最小标签 tie-break 下的分配为 `(0,1,1,1,1,1,1,1,1)`，负载 `(1,2,0)`，makespan=2；同一输入的 rank-one state greedy 给出 `(0,1,2,2,1,1,1,2,2)`，负载 `(1,1,1)`，makespan=1。所有 score 与严格 gap 是 Fraction；`full_trace_defect=66`、`V1_dimension=17` 及 210 个 latent schedules 也在原证据中保留。

本次输入阅读确认这些结果的承重条件没有被输入文件遗漏：full-HS 与 rank-one 是两种不同状态更新，不能把 rank-one 的平衡误作 full-HS 的性质；`T=1` 只是该 fixture 的目标标记，不是对任意机器/任务的阈值。坏分配依赖给定 job order 和 tie-break，因而属于**有限、顺序特定的反例**，不能推广成所有 HS tie/order 都失败，也不能把一次 `m=3` 输入写成一般近似下界。

其独有内容已经归入既有 HS 审查和证据目录；本批不复制完整 trace。若后续研究 HS 家族，应先量化顺序、tie、状态维数和初始 Gram，而不是把这个输入当成黑箱“算法失败”标签。

# 4. Hall 联合流/宏任务 fixture 输入

## 4.1 九个命名案例

该文件包含 `layout` 元数据（宏任务先列、随后 home group；机器先列 home、后列 sink；全部有理数为精确字符串）以及九个命名案例。每个案例同时给出结构化 `input` 和 `original_matrix_job_major`；矩阵中的 `None` 是不合格位置，不是零处理时间。

| 案例 | 关键输入 | 保留的数学边界 |
|---|---|---|
| `huge_q_empty_jobs` | 空 group/eligibility/macros，`k=1`，`q=2^180`，`delta=1/q`，`T=1` | 大整数 `q` 与空任务合同；不能当作复杂度或无界证明 |
| `joint_reselection` | 三组各四个 `1/4`，资格 `[[],[0],[1]]`，两条宏边，`k=q=2`，`delta=1/4`，`T=1` | 两条宏边共享中间组，必须联合重选；逐组独立拼接会改变矩阵 |
| `large_denominator` | 一组五项含极小 `1/N`、`1/2` 及补足有理数，单宏 `3/4`，`q=2` | 精确 Fraction 与大分母，不能用浮点近似替代 |
| `near_factor_two` | 三组各两个 `1/2`，每组一个 `3/4` 宏，`k=1,q=3`，`delta` 为接近 `2/3` 的精确有理数 | 接近二的参数边界；不是“达到二”的普遍实例 |
| `pruned_only_macro_edge` | 一组两个 `1/2`，单一宏边 `2`，`k=1,q=2,delta=1/2,T=1` | 只有宏边且应触发剪枝/拒绝的合同 |
| `unknown_opt_bottleneck` | 三组各四个 `1/4`，资格 `[[],[0],[1]]`，两条 `11/10` 宏边，`k=2,q=3,delta=1/4`，无 `T` 字段 | 刻意保留未知 OPT/瓶颈接口；不能用承诺外的 T 结论 |
| `zero_macro` | 一组两个 `1/2`、无宏，`k=0,q=2,delta=1/2,T=1` | 零宏任务与正 group 负载分离 |
| `zero_target` | 单组 `[0]`、无宏，`k=0,q=2,delta=0,T=0` | 全零目标和零工作语义 |
| `zero_target_positive_macro` | 单组 `[0]`、宏边 `1`，`k=0,q=2,delta=0,T=0` | 零目标但有正宏，测试输入合同拒绝/不可行边界 |

逐案阅读 `original_matrix_job_major` 确认：矩阵行数按宏任务和 group jobs 展开，列数按 home/sink 的固定布局；重复的 `1/4` 行仍是不同 job。没有把 `None` 改成 0，也没有删除零目标和空资格案例。

## 4.2 与既有 Hall 审查和独有内容

现有《未归档配置证书批次与量词边界》和《Hall 联合流与前缀匹配增量审计》已读取同一 fixture 的运行输出，记录了有限参数域、联合阈值 DFS、exact-OPT promise、独立实现以及没有 Hall oracle/没有无界 `q` 结论。本源新增且必须保留的是**完整原始输入与九个命名边界**，尤其是：

- `joint_reselection` 的共享中间组，说明联合选择不是按宏边分开求解；
- `unknown_opt_bottleneck` 的缺省 `T`，说明 unknown-OPT 接口与阈值接口是不同量词；
- `huge_q_empty_jobs`、`large_denominator` 和两个 zero-target fixture，确保实现对大整数、精确有理数、空/零输入的行为可复现；
- `near_factor_two` 与 `pruned_only_macro_edge`，保留接近二和宏边剪枝的失败/边界机制。

这些输入支持已有有限审计的重放，但不新增普遍 Hall 保留、统一近似比、NP 完全性或 `UM-TARGET-v1` 结论。`q` 是显式 sink 列表长度的接口参数；`q=2^180` 的案例恰好没有 jobs，不能用来声称对二进制压缩的巨大 `q` 也有同等显式复杂度。`unknown_opt_bottleneck` 没有 `T`，不能按其它案例的 `T`-feasible 统计归类。

# 5. 证据、去向与接续

本批三个源均完整读取、保留原字节并与已有正式正文及证据比较：

1. `375c2a...` 作为双轨四 clause 重复 occurrence 的**资源输入**被整合到双轨 scoped contracts；不新造对象，不丢弃重复 occurrence 的身份。
2. `6b9edb...` 作为 full-HS/rank-one 的**有限实验输入**被整合到 HS 审查；保留指定顺序、tie、状态初始化和 210 个真实 makespan-one 支持。
3. `50558e...` 作为 Hall 联合流的**九例输入资源**被整合到 Hall 有限审查；原矩阵和全部空/零/大分母边界保持可复现。

相应的既有程序和证据位置为：

- 双轨：`archives/unrelated-machines/tools/evidence/threshold-bundle-20261030/dual_rail_threshold_soundness_boundary_audit.json` 及其 `normalized_dual_rail_*`、`balanced_dual_rail_*` 审计；
- HS：`archives/unrelated-machines/tools/evidence/cycle-path-hs-20261030/hs_effect_greedy_exact_m3_audit.json`；
- Hall：`archives/unrelated-machines/tools/evidence/hall-joint-20261030/` 下主审计、独立 DFS、OPT promise 与 manifest。

接续时应把本页当作输入/证据索引：双轨的三半证明、full-HS 的坏分配和 Hall 的有限成功/拒绝统计分别继承各自对象的适用条件；不能跨模型拼成一个“全仓统一近似”。第三阶段若建边，可把三源连接到对应审查/定理对象，关系类型写成“来源输入/有限核验/反例见证”，不写成逻辑依赖。六人 SPE 半覆盖问题不受本批任何结果关闭。
