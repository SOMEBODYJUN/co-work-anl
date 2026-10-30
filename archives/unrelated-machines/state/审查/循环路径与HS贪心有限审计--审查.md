---
id: "unrelated-machines/cycle-path-hs-greedy-finite-review-20261030"
kind: "review"
type_tag: "审查"
title: "循环路径、归属单位环与 HS 贪心有限审计"
status: "finite-audits-classified"
truth_status: "exact-fraction-source-read-with-explicit-quantifier-boundaries"
review_level: "full-json-read-and-cross-archive-comparison"
source_refs:
  - "source:17cdc777df7f39271a28:evidence/runs/unrelated_machines/held_cycle_assigned_max_path_audit.json"
  - "source:dc60e11fbb6bc8c153cb:evidence/runs/unrelated_machines/home_unit_cycle_and_directed_token_audit.json"
  - "source:7ae41ce4d0f4baf510f5:evidence/runs/unrelated_machines/hs_effect_greedy_exact_m3_audit.json"
evidence_manifest: "../../tools/evidence/cycle-path-hs-20261030/source-manifest.json"
---

# 1. 对象和共同证据口径

本批完整读取三份冻结 JSON：一份给定实际目标的 held-cycle 路径构造审计，一份归属单位环/有向 token 消环审计，一份三台 identical machines、一个 big job 和八个 1/4 small jobs 的 HS 型贪心对照。三者均为 Fraction/整数精确算术，模型不同，不能合并成一个通用调度算法结论。

它们共同保留一个量词纪律：源文件都假定实际目标、根树或显式菜单已经给定；程序字段检查的是指定输入族的构造、消环或贪心选择。没有任何一个源从任意 (R\|C_{\max}) 输入搜索低 makespan 目标、证明全局近似比或证明所有 tie/order 的行为。

# 2. 给定目标的 held-cycle 路径构造

## 2.1 精确输入和四个主案例

`17cdc777df7f39271a28` 的主脚本为 `tests/audits/unrelated_machines/held_cycle_buffer_path.py`，Fraction 算术，主结果和 independent 结果都 `passed`。scope 明确写成“actual target is supplied；finite verification separate from universal proof and bit-polynomial construction”。四个 canonical 案例为：

| 案例 | order | peak | protected vertices / 参数 |
|---|---|---:|---|
| protected_two_cycle | [2,3,4,5,6,7,8,9,0,1] | 12/5 | {0,1} |
| shared_protected_receivers_and_trees | [10,12,2,3,4,5,6,7,8,9,11,13,0,1] | 11/5 | {0,1} |
| priority_family | [0,2,4,6,1,3,5,7] | 47/20 | (c=19/10,d=1/10,q=3/5) |
| priority_family | [0,2,4,6,1,3,5,7] | 4019/2000 | (c=151/100,d=1/1000,q=1) |

附加字段给出 `degenerate_cases=4`、一个极小有理尺度 (1/14821387422376473014217086081112052205218558037201992197050570753012880593911817)，以及 `no_eligible_but_path_peak=7/4`。这些是边界和数值稳定性见证，不是对所有参数的峰值公式。

## 2.2 局部 sharp promise 和独立核验

主输出的 `sharp_local_promise_cases` 是 (C=1,5/4,3/2,7/4,2)，对应 path peak (2,2,2,9/4,5/2)。它只说明在列明 promise 下构造器的峰值输出，不说明该峰值对任意目标或任意路径顺序都是最优。

独立脚本 `held_cycle_buffer_path_independent.py` 不导入 canonical 实现，复核 split cycle 的 peak (12/5)、protected vertices {0,1}，并确认 tree case、3 个 degenerate cases。独立脚本的作用是交叉验证列明案例，不是完整算法重构。

## 2.3 可接续内容和失败机制

该源适合继续研究“给定目标后如何沿 held cycle 保留缓冲”的局部构造，以及 protected receiver/tree 组合的峰值上界。要形成定理，必须补齐任意目标的表示、路径选择、循环分解、位复杂度和峰值证明；当前源明确没有 general U path 或 target solver。`no_eligible_but_path_peak=7/4` 应保留为无可选边时仍有路径峰值的边界，不能被忽略为异常。

# 3. 归属单位环与 directed-token bridge

## 3.1 全部小图和穷举范围

`dc60e11fbb6bc8c153cb` 的状态为 `PASS`，无随机种子，使用 exact integers 和 `fractions.Fraction`。主脚本文件哈希和独立脚本哈希均在原 JSON 保留。主运行覆盖所有 64 个 loopless simple 3-vertex directed graphs、每个 root、需求向量取 ({0,1,2,2^{80}+7}) 的全部合法组合、每个 complete token assignment 以及每个 root-tree edge subset。

精确计数为：`normalization_schedules=9803`、`schedules_with_cycles=4034`、`subtwo_normalizations=992`、`boundary_fixtures=3`；directed-token 部分 `digraphs=64`、`token_instances=6591`、`complete_assignments=151959`、`subtwo_decodings=1767`、`tree_schedules=17004`。最大需求 (1208925819614629174706183) 只证明实现能在大整数输入上运行，不能替代任意位长的复杂度证明。

## 3.2 独立结果和量词边界

独立运行得到 `assignments=83936`、`boundary_checks=3`、`cycle_instances=18306`、`cycles_removed=18306`、`root_normalizations=18554`、`sub_two=21212`。这支持列明三顶点输入上“检测到的环均被消除”的有限实现证据。

源的 limits 明确：这是 finite implementation evidence；universal claims 有另行证明；实际 (sigma) 或 rooted tree 仍需给定，没有 general low-makespan schedule search；64 个三顶点图不构成一般 complexity 或 approximation proof。故“18306 cycles_removed”不能写成所有机器环均可消除，也不能从三顶点推出任意顶点数。

## 3.3 和既有周期菜单审查的关系

既有《周期菜单修复与独立交叉核对》已登记 fanout/ring/padded-fork 的合成菜单修复与 `extract_cycle` 交叉测试。本源的独有内容是：

- 归属单位环（home unit cycle）与有向 token 的完整三顶点图枚举；
- 需求向量含 (2^{80}+7) 的大整数边界；
- 归一化前后 cycle、sub-two 和 root-tree 计数；
- 不导入 canonical 实现的独立 cycle removal 计数。

两批都保持“给定输入、有限审计”身份，不把 cycle removal 直接移植为一般 LP 初始化或完整优化器正确性。

# 4. 三机 HS 型贪心和 rank-one 对照

## 4.1 输入和真实最优值

`7ae41ce4d0f4baf510f5` 的对象是 3 台 identical machines、1 个大小 1 的 big job、8 个大小 (1/4) 的 small jobs。真实最优值为 1；隐含实际调度数 210，均匀 latent distribution 为 (1/210)。V1 维数为 17，正交基整数范数完整保存在原 JSON，`job_partition_identity_verified=true`、`row_load_identity_verified=true`，full trace defect=66。

## 4.2 full-HS 贪心：确切的坏分配

固定 job order 为 big first、随后 small labels ascending；精确 tie 取最小 label。full-HS 的 assignment 为

[
(0,1,1,1,1,1,1,1,1),
]

实际负载为 ((1,2,0))，因此 makespan=2，而 true OPT=1，得到该指定输入/顺序下的精确比值 2。第一步三个机器并列；第二步机器 1、2 并列；从第三步开始，机器 1 由严格正 gap 逐步被选中。最后一项 strict gap 为
(12131586226051/108904936711689216>0)，最终 (K_{HS}^2=3369699728819633/18296029367563788288)。这证明一个具体 tie-breaking/order 的 full-HS 选择确实产生坏分配，但没有证明所有 tie 或所有 order 都坏。

## 4.3 rank-one 贪心对照

同一输入的 rank-one state greedy assignment 为

[
(0,1,2,2,1,1,1,2,2),
]

负载为 ((1,1,1))，makespan=1。其首两步也是 tie，第三步起有严格正 gap；最后 strict gap 为
(35088380977/6050274261760512>0)，最终 state (G)-norm 平方为
(28360619690999/1016446075975766016)。该对照说明 full-HS 目标与 rank-one 状态目标在同一固定输入上可产生完全不同的整调度，不能把一个状态的势函数结论套给另一个。

## 4.4 与向量贪心审查的关系

已有《固定阶向量贪心与 q=13 线性缺口增量审计》处理给定真实最优源和固定阶矩向量贪心；本源只添加一个 m=3 的 HS/rank-one 分离：full-HS 在指定 order/tie 下比值 2，rank-one 达到 1。两者都要求给定源/分布与顺序，不提供任意输入的近似下界或 hardness。后续若要声称“HS 一定失败”，必须量化 order、tie、状态表示和初始分布，并给出一个输入族，而不是只引用本行。

# 5. 总结性处置和后续义务

三源均已完整读取、保存原字节并与周期菜单、重型匹配、固定阶向量和固定工作审查比较。逐源处置：

- `17cdc...`：集成 held-cycle 四案例、local sharp promise、独立 split-cycle 复核；保留给定目标和无 general solver 的边界。
- `dc60...`：集成 64 个三顶点图、token/assignment/tree 计数与独立 cycle removal；保留大需求与有限量词。
- `7ae41...`：集成 true OPT=1、full-HS 坏分配/严格 gap、rank-one 平衡对照；明确 order/tie-specific。

这些内容都归入 unrelated-machines 审查，不进入 CAG 六人 half 覆盖证明。若继续推进，先补全给定目标到一般输入的编译、cycle/token 的任意顶点推广、HS 订单/tie 的全量族分析，然后再讨论算法或 hardness。没有一项本批结果关闭一般问题。
