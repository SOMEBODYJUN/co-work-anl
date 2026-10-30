---
id: "unrelated-machines/knapsack-matroid-large-bundle-finite-review-20261030"
kind: "review"
type_tag: "审查"
title: "Knapsack 拟阵包络与大束碰撞有限审查"
status: "finite-audits-classified"
truth_status: "exact-fraction-finite-envelopes-with-explicit-universal-boundaries"
review_level: "full-json-read-and-cross-archive-comparison"
scope: "knapsack/matroid envelope enumeration, exponential circuit witnesses, and large-bundle collision floor audits"
source_refs:
  - "source:8aad4f636216c29f8373:evidence/runs/unrelated_machines/knapsack_matroid_envelope_audit.json"
  - "source:4d29d36f9284fa20e472:evidence/runs/unrelated_machines/knapsack_matroid_exponential_audit.json"
  - "source:55dd85065c708217946e:evidence/runs/unrelated_machines/large_bundle_collision_square_root_audit.json"
evidence_manifest: "../../tools/evidence/knapsack-bundle-20261030/source-manifest.json"
---

# 1. 对象、范围和证据等级

本批三项来源都属于 unrelated-machines 的资源束/拟阵/容量包络线，但层级不同：第一项枚举 (k\le4) 的所有 family truth tables 与可 admissible matroid；第二项给出 (k=3..9) 的 fundamental-circuit/witness 参数族和若干 exact endpoints；第三项对大需求标签束执行 normative 与 independent 两路冻结核验，并包含 rooted-DAG token bridge。

三源都使用整数或 `fractions.Fraction`，并明确 finite scope。它们可提供精确 envelope、候选下界和有限碰撞/着色机制，不能替代全 (k,p) 拟阵证明、一般 CONFIG/LP 求解器、近二调度硬度或新颖性认证。与《配置剥离与联合匹配有限审计》、重型匹配/森林边界、双轨阈值批比较后，保留各源的独有量词，不把不同资源束合同拼成一个统一 theorem。

# 2. Knapsack–matroid envelope：(k\le4) 的全表

## 2.1 运行合同

`8aad4f636216c29f8373` 的 claim 为 `UM-KNAPSACK-MATROID-ENVELOPE-v1`，对应 `minimal_star_contraction_and_capacity_gap.md` 的冻结说明；脚本使用所有 family truth tables、直接拟阵公理检查和所有带重复的无序 tuple。算术是 (1/k) 单位的整数权重并输出 Fraction，范围为 (k=1,2,3,4)、(p=1,\ldots,k+1)。来源明确是 finite exhaustive audit，未测试调度算法，也未给出所有 (k,p) 的普遍证明。

## 2.2 精确表格

| (k) | truth tables | admissible matroids | (p) | tuples examined | minimum units | (D) |
|---:|---:|---:|---:|---:|---:|---:|
| 1 | 2 | 2 | 1,2 | 2,3 | 1,1 | 1,1 |
| 2 | 8 | 4 | 1,2,3 | 4,10,20 | 3,2,2 | 3/2,1,1 |
| 3 | 128 | 8 | 1,2,3,4 | 8,36,120,330 | 5,4,3,3 | 5/3,4/3,1,1 |
| 4 | 32768 | 16 | 1,2,3,4,5 | 16,136,816,3876,15504 | 7,6,5,4,4 | 7/4,3/2,5/4,1,1 |

`attaining_tuple_indices`、来源 SHA 和每个 (p) 的 witness 索引均在 evidence 副本中保留。表中 (D) 形成从 (7/4) 到 (1) 的有限 envelope 曲线；例如 (k=4,p=3) 的 (D=5/4) 与之前 bundle-subdivision/重型匹配批的局部目标膨胀相邻，但输入合同是拟阵容量 tuple，不能直接合并。

## 2.3 数学身份和缺口

这项运行支持“在显式 (k\le4) truth-table/matroid 类上，所有重复 tuple 的最小单位数和 D 值可被精确列出”。它不支持：

- 对任意 (k,p) 的 envelope 公式；
- 从 (D) 直接获得 unrelated-machines 的 OPT 或 CONFIG 阈值；
- 一个调度舍入算法；
- 由同一实现重复运行得出的独立数学证明。

后续若要升级，必须先定义 matroid rank/knapsack 资源与机器—作业矩阵的同一映射，再证明 tuple envelope 如何成为配置可行性或整数调度下界。

# 3. Exponential matroid witness：参数族和 fundamental-circuit 边界

## 3.1 运行规模

`4d29d36f9284fa20e472` 状态为 `all exact checks passed`，无随机 seed、整数/Fraction 算术。检查 16 个 parameter cases、2674 个 fundamental circuit cases 和 109351 个 explicit circuit witness checks。其十六行以 (k\) 和 (r) 给出 witness load、witness count、单个 matroid 最多排除的 witness 数、(q\) 下界与 ratio。

代表性精确行：

| (k) | (r) | witness load | witness count | max excluded | (q_{m lower}) | ratio |
|---:|---:|---:|---:|---:|---:|---:|
| 3 | 1 | 4/3 | 3 | 1 | 3 | 3 |
| 4 | 1 | 3/2 | 4 | 2 | 2 | 2 |
| 5 | 1 | 8/5 | 5 | 3 | 2 | 5/3 |
| 5 | 2 | 6/5 | 10 | 1 | 10 | 10 |
| 6 | 2 | 4/3 | 15 | 3 | 5 | 5 |
| 7 | 3 | 8/7 | 35 | 1 | 35 | 35 |
| 8 | 3 | 5/4 | 56 | 4 | 14 | 14 |
| 9 | 4 | 10/9 | 126 | 1 | 126 | 126 |

全部十六行和 exact endpoints 保存在原 JSON。`exact_endpoints` 在 ((k,r)=(3,1),(5,2),(7,3),(9,4)) 给出 (q=3,10,35,126)；前两行还检查 augmentation axiom，后两行 `augmentation_axiom_checked=false`，所以后两项只能叫 endpoint 数值/构造输出，不能称为完整拟阵验证。

## 3.2 有限机制和误读风险

这些行展示一个机制：随着 (r) 增大，witness count 可以让每个单一 matroid 排除的数量变小，从而 (q_{m lower}) 和 ratio 快速增长（例如 (k=9,r=4) 的 (q=126)、ratio=126）。这可作为“多拟阵外包的 witness 数量可能呈组合增长”的候选障碍；但它还没有把 witness 族解码为任意 unrelated-machines 的有效机器/作业实例，也没有证明 ratio 是任何算法必须付出的近似因子。

源限制明确这是 finite formula/construction audit，不能替代 matroid proof。尤其 (k=7,r=3) 与 (k=9,r=4) 的 augmentation 未检查，不能因 `exact_q` 字段就声称完整独立集结构已验证。

# 4. 大需求标签束碰撞锐界：normative + independent

## 4.1 Normative exact run

`55dd85065c708217946e` 的 schema=1、日期 2026-10-17、状态 `pass`，整数/Fraction、无数值容差。normative 主运行覆盖：

- exhaustive_bundle_instances=4056；
- color_runs=11832；
- strict improving moves=12186，且从路径重算同为12186；
- (q\in\{1,3\})、resource_count (1..4) 的 exhaustive scope；
- 17 个 invalid cases rejected，3 个 large-resource-ID cases；
- nonrecursive augmenting chain size=1200；24 个 small-common-pool oracle cases。

空 family 约定为 (q=0,c=0,score=\Lambda=1)，并明确不属于 positive-root theorem。`source_proof` 的机制是 defective-coloring potential、Cauchy 和 capacitated Hall，且 `external_theorem_imports=[]`；它仍声明 finite executable checks do not replace the general proof。

square-pool witnesses 给出 (q=t^2) 的精确端点：

| (q) | (t) | exact optimum = algorithm score = Λ |
|---:|---:|---:|
| 1 | 1 | 1 |
| 4 | 2 | 1/2 |
| 9 | 3 | 1/3 |
| 16 | 4 | 1/4 |
| 25 | 5 | 1/5 |
| 36 | 6 | 1/6 |

每个端点还保存 algorithm-selected、allocation、optimum witness 和 augmenting steps；这说明在列明 square pool 上算法与 oracle 精确相等，不是一般大束实现的证明。

`token_bridge` 只检查 35 个 actual schedules，其中 16 个 below-two decoded、19 个 alpha-zero cases；它把标签束结果连接到 rooted DAG token 记录，但 scope 仍是有限实际树/完整任务调度检查。

## 4.2 Independent exact run

独立程序不导入 normative imports，覆盖 complete single-label bundles on three resources、(q=1..4)：

- cases=2800；
- resource-parent assignments=88586；
- eta-collision necessity checks=105599；
- Hall subset checks=74412；
- parameter claim checks=10738；
- strict defective recolorings=17450。

40 个 benchmark 从 (c=1) 到 (c=41) 保存 exact=lower，例如 (c=1) 为1，(c=3) 为1/2，…，(c=41) 为1/40。独立结果的身份是独立有限算术和 parent-assignment 审计；它没有把 normative 的有限程序升级为一般 proof，也没有 hardness implication。

## 4.3 安全解释

该双路核验支持以下安全结论：在列明的资源数量、q 范围、bundle 结构和 square-pool 端点上，缺陷着色/容量 Hall 计算和算法输出可以被精确重算，且若干 square-pool 实例达到 oracle。它不能推出任意资源数、任意 bundle multiplicity 或任意 unrelated-machines 输入的近二调度困难性。`nonrecursive augmenting chain size=1200` 是最大测试链长度，不是所有链的复杂度界。

# 5. 与全仓对象的比较和处置

1. 与《配置剥离与联合匹配有限审计》：本批新增拟阵 envelope、fundamental circuit 和大束 square-pool；它们与 bundle peeling、tensor guard、C2 parity 使用相似的容量/匹配语言，但变量、资源和量词不同，不把 D/ratio/q 直接并入既有配置定理。
2. 与《重型匹配凸化与逃逸残余审计》：heavy-matching 批已给 (k=4..64) 的另一压缩 ratio 族；本批 exponential matroid 的 ratio 来自 witness 排除和 q 下界，large-bundle 的 score 来自 defective coloring/Hall。三者是相邻障碍，不是同一算法的下界。
3. 与《双轨阈值与整除中性修复联合选择有限审计》：该批的 Q=m/m² tick 修复和半单位 3DM 研究另一输入合同；本批空 family convention、square-pool witness 和大需求 ID 是独有边界。
4. 与森林/循环边界：rooted-DAG token bridge 只提供 35 个实际树调度记录，不能替代森林或 home-unit cycle 的任意输入分析。
5. 与 CAG 六人 half：三源均为 machine/resource/bundle 语义，不含客户目录、完整历史或纯 SPE，保持 unrelated-machines 独立身份。

逐源处置：

- `8aad...`：integrated 为 (k\le4) knapsack–matroid envelope finite table，保留全部 tuple/单位/D 字段及 all-k,p 限制。
- `4d29...`：retained 为 exponential witness/circuit candidate obstruction，保留十六行参数、exact endpoints 和 augmentation 未检查边界，不写成一般拟阵定理或 hardness。
- `55dd...`：integrated 为 normative+independent 大束碰撞 finite audit，保留 4056/2800 案例、12186 改善步、105599 collision、74412 Hall 和 square-pool 端点；不写成一般近二调度定理。

# 6. 后续接续

若要推进这条线，先完成三件事：把 matroid/knapsack envelope 映射到明确的机器—作业资格；对 (k=7,9) endpoints 补 augmentation/independent-set 证明；把 square-pool/token bridge 的有限算法输出嵌入统一的全局配置和任务调度对象。当前批的正式真值等级保持“有限 exact envelope、候选组合障碍、双路重放”，没有关闭一般 unrelated-machines 近似或复杂度问题。
