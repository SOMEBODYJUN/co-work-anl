---
id: "facility-games/five-site-deca-hardness-20261030-review"
kind: "review"
type_tag: "审查"
title: "五设施 DECa 硬度有限审计"
status: "finite-evidence-classified"
truth_status: "exact-rational-regressions-with-explicit-scope"
review_level: "full-json-read-and-cross-source-comparison"
scope: "SC-FIVE-DECa-HARD 两份五设施 exact-hardness 回归；仅有限精确支持枚举与参数边界，不是普遍 FPTAS/EPTAS、近似比或均衡定理"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:evidence/runs/five_site_exact_hardness.json"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:evidence/runs/five_site_exact_hardness_edges.json"
evidence_dir: "archives/facility-games/tools/evidence/five-site-hardness-20261030"
related_objects:
  - "facility-games/state/审查/共享流与多设施有限审计边界--审查.md"
  - "facility-games/state/审查/四设施独立核验与近带有限审计--审查.md"
---

# 1. 来源、对象与完整读取

本批实读两份冻结 JSON：主回归 `five_site_exact_hardness.json`（16,371 字节）与边界增量 `five_site_exact_hardness_edges.json`（13,679 字节）。原始字节、源 SHA-256、大小和 ID 保存在 `tools/evidence/five-site-hardness-20261030/manifest.json`。两份文件均声明 claim=`SC-FIVE-DECa-HARD`，但 scope 分别是 “Finite exact regression, not a universal proof” 和 “Additional finite exact regression, not a universal proof”。

我逐字段解析了顶层计数、每个 case 的参数、`accepted_closed_supports`、`distinct_support_load_pieces`、`factors_by_unordered_layout`、`alpha_star`、`normalized_T/gap/mu`、`numbers`、`source_yes/target`、`full_diagonal_enumeration` 与整数位长；未把 `all_assertions_passed=true` 当作超出源量词的证明。相关 facility-games 正文 `共享流与多设施有限审计边界--审查.md` 和 `四设施独立核验与近带有限审计--审查.md` 已全文比较，用于区分本批五设施 DECa 对象、既有四设施 32/19 实例和近带 heavy-support 对象。

# 2. 主回归：14 个有限精确案例

主 JSON 的总计字段为：`parameter_search_tests=1103`、`forced_macro_tests=96`、`strict_boundary_counterexample_verified=true`、`invalid_factor_inputs_rejected=3`、`cases=14`、`all_assertions_passed=true`、`repository_checks_run=false`。因此它是成功的源内精确回归，但没有运行仓库级测试，也没有把案例集合声明成完整参数空间。

14 个案例按客户数和编号向量分为：

| 客户数 | `numbers` | 案例数 | 完整对角枚举 | `source_yes` | `source_no` |
|---:|---|---:|---:|---:|---:|
| 11 | [2] | 8 | 8 | 4 | 4 |
| 15 | [2,3] | 6 | 0 | 4 | 2 |

每个 case 对 15 个无序布局保存精确因子。`accepted_closed_supports` 在 11 客户案例为 489–499，15 客户案例为 9,440–9,590；`distinct_support_load_pieces` 分别在 195–200、698–702。非目标布局的最小加性 margin 在普通参数中为 `1/16`、`1/32` 或 `1/128`，在微小扰动/超大有理分母边界中变为更小的正有理数，说明实现确实保留了严格边界而不是四舍五入。

## 2.1 11 客户的基准对

四组基准 `a` 各有一个达到基准的 `source_yes=true` 案例和一个超过基准的 `source_yes=false` 伴侣：

* (a=7/5)：达到案 `alpha_star=7/5`；伴侣 `alpha_star=51594515/36852348`，`normalized_gap=877/37094400`，目标分别为 2 与 1。
* (a=3/2)：达到案 `alpha_star=3/2`；伴侣 `2528491/1685624`，`normalized_gap=55/2543616`，目标分别为 2 与 1。
* (a=8/5)：达到案 `alpha_star=8/5`；伴侣 `21185470/13240893`，`normalized_gap=103/52992000`，目标分别为 2 与 1。
* (a=809/500)：达到案 `alpha_star=809/500`；伴侣 `309929424744143/191550941273040`，`normalized_gap=54523/9577562112000`，目标分别为 2 与 1。

这些是同一有限生成器中的参数边界：`source_yes` 与 `target` 随案例输入改变；它们不能被重写为“所有 11 客户实例的因子正好是 a”，也不能把 `source_no` 当成一般困难度下界。所有 11 客户案例 `full_diagonal_enumeration=true`，但这只覆盖该文件生成的完整对角布局，不等于设施数、权重和客户类型的全称枚举。

## 2.2 15 客户的扩展

15 客户、`numbers=[2,3]` 的六个案例没有完整对角枚举（`full_diagonal_enumeration=false`），而是在记录的有限支持域上审计。对 (a=3/2)，有三条 `source_yes=true`（`alpha_star=3/2`，目标 2 或 5）和一条 `source_no=false`（`alpha_star=24954579/16636376`，`normalized_gap=5/8368128`，目标 4）。对 (a=809/500)，有两条 `source_yes=true`（目标 2、5）和一条 `source_no=false`（`alpha_star=280396293225452391/173298079840138000`，`normalized_gap=54523/346596704256000`，目标 4）。

该分层显示：扩充到 15 客户后，某些编号下仍可达到给定基准，另一些支持布局会产生严格有理缺口；但由于没有完整对角枚举，不能把缺口解释为该参数族的全局最优值，更不能导出任意 15 客户设施游戏的 hardness 定理。

# 3. 边界增量：9 个追加有限案例

`five_site_exact_hardness_edges.json` 的总计为 `cases=9`、`invalid_source_inputs_rejected=6`、`all_assertions_passed=true`、`repository_checks_run=false`。其中 5 个案例为 11/15 客户的 `numbers=[2]` 或 `[2,2]`，4 个案例把 (a) 推到两个边界有理数：

* (a=1000001/1000000) 的 11 客户成对案例：一个 `alpha_star=a, source_yes=true,target=2`；另一个 `alpha_star=3087013734684966674319/3087010647007652000000, source_yes=false,target=1`，`normalized_gap=666667/3087010831007744`。
* (a=161803398874989/10^{14}) 的近黄金比例有理近似成对案例：达到案 `alpha_star=a, source_yes=true,target=2`；伴侣的 `alpha_star` 是大有理数、`source_yes=false,target=1`，`normalized_gap` 为显式正分数，且最大整数位长达到 277。
* (a=3/2) 的 15 客户 `[2,2]` 四例中，三例达到基准（目标 0、2、4），一例 `source_no=false` 且 `alpha_star=225855459/150570196`、`normalized_gap=55/75737088`、目标 1。

这批边界输入的价值是验证实现对接近 1、近黄金比例和重复编号的有理精度处理；`invalid_source_inputs_rejected=6` 则保留输入拒绝路径。最大整数位长和极小 margin 说明不能用 float 摘要替代原始有理值。

# 4. 术语、比较与数学边界

* **`source_yes` 的正确量词。** 它是源程序在该 case、该支持域和该目标字段上的布尔判定；`target` 甚至取 0、1、2、4、5，随 case 改变。不能把它解释为概率、算法成功率或所有布局存在某种均衡的全称。
* **`alpha_star` 的正确量词。** 每个 case 给出了支持枚举下的精确有理因子/候选最优值；15 客户行明确没有完整对角枚举，因此只可称记录域内的精确值。`factors_by_unordered_layout` 的 15 项是布局级输出，不是不同均衡的计数。
* **与既有四设施来源。** 既有 32 实例审计的计数是 `yes=8,no=24`，19 实例独立核验是 `yes=8,no=11`；本批 14+9 个五设施 case 使用不同 claim、不同 `numbers` 与不同支持生成器，不能把计数相加，也不能把五设施 `source_yes` 接成四设施 FPTAS/EPTAS 结论。
* **与近带审计。** 近带源检查固定 heavy-support central representative 的 `near_feasible`；本批检查 DECa 的 support/load pieces 和 factor `alpha_star`。两者都用有限精确算术，但定义域、目标布尔量和参数化不同，不能互换。
* **与 CAG 六人目标。** facility-games 的设施/共享客户模型没有 CAG 的有限共同目录、顺序单位提供者、完整有序历史纯 SPE 和终局客户均分量词；本批不建立 CAG 迁移边。

# 5. 处置与后续

两个来源均 **integrated** 到本审查稿，同时保留主回归与边界增量的独立 raw JSON。主回归的 14 个 case、1,103 parameter tests、96 forced-macro tests 和 3 个 invalid factor inputs；边界增量的 9 个 case、6 个 invalid source inputs、极小 margin 与大整数位长，均写入证据 manifest 与 receipt。

可接续的数学工作是：补充 15 客户行的完整 diagonal/support closure；明确 `source_yes/target` 的定义与目标变换；将有限 `alpha_star` 与正文中的一般 DECa 目标逐式对齐。当前文件没有证明任意设施数、任意客户权重、任意布局或任意均衡选择器下的 FPTAS/EPTAS，也没有给出一般 hardness 下界。任何后续全称声明都必须从新的完整支持枚举或解析证明开始。

结论等级：**精确有限回归与边界证据**。不能升级为普遍算法、全局近似比、PLS/hardness 定理，也不能迁移成 CAG 六人 half 覆盖结论。
