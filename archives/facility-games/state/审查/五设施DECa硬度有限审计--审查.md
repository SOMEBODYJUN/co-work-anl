---
id: "facility-games/five-site-deca-hardness-20261030-review"
kind: "review"
type_tag: "审查"
title: "五地点 DECa 硬度有限审计"
status: "finite-evidence-classified"
truth_status: "exact-rational-regressions-with-explicit-scope"
review_level: "full-json-read-and-cross-source-comparison"
scope: "SC-FIVE-DECa-HARD 两份五地点、两设施 exact-hardness 回归；有限实例全局最优由完整枚举或已证同址正规形核定，不是普遍 FPTAS/EPTAS、近似比或均衡定理"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:evidence/runs/five_site_exact_hardness.json"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:evidence/runs/five_site_exact_hardness_edges.json"
evidence_dir: "archives/facility-games/tools/evidence/five-site-hardness-20261030"
related_objects:
  - "facility-games/state/审查/共享流与多设施有限审计边界--审查.md"
  - "facility-games/state/审查/四设施独立核验与近带有限审计--审查.md"
---

# 1. 来源、对象与完整读取

后续纠正：这里始终是**两个带标签设施、五个共同目录地点**，保留旧文件名仅为已有引用兼容。后续全文读取构造器及原审计源码后，确认 `full_diagonal_enumeration=false` 的实例使用已证同址正规形，而非漏掉同址后只求部分域最优；`source_yes` 是输入SUBSET SUM的精确真值。以下按该实际合同修正，原两份JSON字节与计数不改。

本批实读两份冻结 JSON：主回归 `five_site_exact_hardness.json`（16,371 字节）与边界增量 `five_site_exact_hardness_edges.json`（13,679 字节）。原始字节、源 SHA-256、大小和 ID 保存在 `tools/evidence/five-site-hardness-20261030/manifest.json`。两份文件均声明 claim=`SC-FIVE-DECa-HARD`，但 scope 分别是 “Finite exact regression, not a universal proof” 和 “Additional finite exact regression, not a universal proof”。

我逐字段解析了顶层计数、每个 case 的参数、`accepted_closed_supports`、`distinct_support_load_pieces`、`factors_by_unordered_layout`、`alpha_star`、`normalized_T/gap/mu`、`numbers`、`source_yes/target`、`full_diagonal_enumeration` 与整数位长；未把 `all_assertions_passed=true` 当作超出源量词的证明。相关 facility-games 正文 `共享流与多设施有限审计边界--审查.md` 和 `四设施独立核验与近带有限审计--审查.md` 已全文比较，用于区分本批五地点 DECa 对象、既有四地点 32/19 实例和近带 heavy-support 对象。

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

这些是同一有限生成器中的参数边界：`source_yes` 与 `target` 随案例输入改变；它们不能被重写为“所有 11 客户实例的因子正好是 a”，也不能把 `source_yes=false` 的单个有限输入当成一般困难度下界。所有 11 客户案例 `full_diagonal_enumeration=true`，但这只覆盖该文件生成的完整对角布局，不等于设施数、权重和客户类型的全称枚举。

## 2.2 15 客户的扩展

15 客户、`numbers=[2,3]` 的六个案例没有逐支持枚举同址NE（`full_diagonal_enumeration=false`），而使用共同目录的同址正规形。对 (a=3/2)，有两条 `source_yes=true`（`alpha_star=3/2`，目标分别2、5）和一条 `source_yes=false`（`alpha_star=24954579/16636376`，`normalized_gap=5/8368128`，目标4）。对 (a=809/500)，同样两条 `source_yes=true`（目标2、5）和一条 `source_yes=false`（`alpha_star=280396293225452391/173298079840138000`，`normalized_gap=54523/346596704256000`，目标4）。原报告没有`source_no`字段。

原`optimum(...,False)`先精确枚举全部异址NE闭支持，取异址坐标极小威胁H，再把每同址候选置为max(1,2H(t)/reach(t))，并对全部异址负载区间优化放松目标。由[同址正规形](../算法/同址平衡正规形与异址交叠参数精确优化--算法.md)，全表最小值确为这个有限实例的全局α*：同址平衡给基准，严格更优的异址候选才能被选中，其实际同址偏离自动安全。个别异址表项仍是放松值，不能各自直接当成可实现倍率；`full=true`小例还另核两种全局算法相等。故这里的15客户全局值有效，有限六例仍不代替一般归约证明。

# 3. 边界增量：9 个追加有限案例

`five_site_exact_hardness_edges.json` 的总计为 `cases=9`、`invalid_source_inputs_rejected=6`、`all_assertions_passed=true`、`repository_checks_run=false`。其中 5 个案例为 11/15 客户的 `numbers=[2]` 或 `[2,2]`，4 个案例把 (a) 推到两个边界有理数：

* (a=1000001/1000000) 的 11 客户成对案例：一个 `alpha_star=a, source_yes=true,target=2`；另一个 `alpha_star=3087013734684966674319/3087010647007652000000, source_yes=false,target=1`，`normalized_gap=666667/3087010831007744`。
* (a=161803398874989/10^{14}) 的近黄金比例有理近似成对案例：达到案 `alpha_star=a, source_yes=true,target=2`；伴侣的 `alpha_star` 是大有理数、`source_yes=false,target=1`，`normalized_gap` 为显式正分数，且最大整数位长达到 277。
* (a=3/2) 的 15 客户 `[2,2]` 四例中，三例达到基准（目标 0、2、4），一例 `source_yes=false` 且 `alpha_star=225855459/150570196`、`normalized_gap=55/75737088`、目标 1。

这批边界输入的价值是验证实现对接近 1、近黄金比例和重复编号的有理精度处理；`invalid_source_inputs_rejected=6` 则保留输入拒绝路径。最大整数位长和极小 margin 说明不能用 float 摘要替代原始有理值。

# 4. 术语、比较与数学边界

* **`source_yes` 的正确量词。** `source_answer(numbers,target)`枚举原输入的所有0/1子集，检查是否恰好和为target；它是SUBSET SUM的精确YES真值，与客户NE支持选择无关。0和总和目标允许，故出现0、1、2、4、5不构成范围异常。它不是概率或算法成功率。
* **`alpha_star` 的正确量词。** 每个case是构造出的该具体游戏的全局最优倍率；依据是全部布局支持枚举，或全部异址支持加已证明的同址正规形。它不覆盖任意同客户数游戏。`factors_by_unordered_layout`的15项是布局候选，False分支的异址项为放松值；全表最小才按正规形保证可实现。
* **与既有四地点来源。** 既有32实例审计的计数是`yes=8,no=24`，19实例独立核验是`yes=8,no=11`；本批14+9个五地点case使用不同claim、不同`numbers`与不同支持生成器，不能把计数相加，也不能把有限SUBSET SUM真值直接当一般FPTAS/EPTAS结论。这里的设施数始终为2。
* **与近带审计。** 近带源检查固定 heavy-support central representative 的 `near_feasible`；本批检查 DECa 的 support/load pieces 和 factor `alpha_star`。两者都用有限精确算术，但定义域、目标布尔量和参数化不同，不能互换。
* **与 CAG 六人目标。** 本模型也有有限共同目录，但仅有两家设施，末级是加权原子客户的独立混合NE；它与六提供者按完整有序历史选择客户子集、终局均分的纯SPE覆盖目标不同。本批不建立CAG迁移边。

# 5. 处置与后续

两个来源均 **integrated** 到本审查稿，同时保留主回归与边界增量的独立 raw JSON。主回归的 14 个 case、1,103 parameter tests、96 forced-macro tests 和 3 个 invalid factor inputs；边界增量的 9 个 case、6 个 invalid source inputs、极小 margin 与大整数位长，均写入证据 manifest 与 receipt。

15客户行的同址闭合与`source_yes/target`的意义已由原源码和已证正规形对齐，不再列作未闭合义务。可接续工作是核新输入/实现的精确合同、复核一般归约及输出证书的范围；不必为已用解析正规形覆盖的同址重新穷举。当前文件仍只分类14+9个有限回归，不证明一般hardness、FPTAS/EPTAS或任意设施数结论。后续全称声明须引用其准确解析证明，不能从案例成功次数推出。

结论等级：**精确有限回归与边界证据**。不能升级为普遍算法、全局近似比、PLS/hardness 定理，也不能迁移成 CAG 六人 half 覆盖结论。
