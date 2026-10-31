---
id: fair-allocation/retired-trivalued-chores-fpo-matroid-results-v1
kind: review
type_tag: 审查
title: 退役三值家务、FPO 与拟阵交换结果三源复现
status: finite-exact-results-reproduced; models-kept-independent
truth_status: fixed-instance-certificates; no-general-theorem
review_level: full-json-read-cross-object-comparison
summary: "完整读取三值 chores 类型审计、fair FPO 独立 Fraction 交叉检查和 n≤5 拟阵交换穷举；保留 alpha=23/22 固定障碍、10/11 FPO 反例与有限交换直径统计，严格不外推连续/任意n结论。"
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:history/retired_topic_selection/multi_lane/research/topic_selection/probes/results/chores_trivalued_type_audit_20261020.json
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:history/retired_topic_selection/multi_lane/research/topic_selection/probes/results/fair_fpo_independent.json
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:history/retired_topic_selection/multi_lane/research/topic_selection/probes/results/matroid_exchange_diameter_independent_20261020.json
source_ids: [804a27a2cded4f022da8, 018d90eb4aee7838c480, 4a4127c9a96303599be0]
source_sha256:
  - c570f3ad42aedc205072dc30633303f16fe3c636d127e6baeec9acdedce3e011
  - 946bd77da963fb3cedfa24f8555b4f4cf7dffad71fd286fb0e2e334085fffae2
  - 5a2549b3607a18588ad55940fa2e7d920f827f409c542e2f3d5ed84fe3a99c33
source_sizes: [9338, 3539, 4465]
source_blobs: [82ced74cea637fe8a8ee14555451f3e6deb983a2, 3996c458b398f70e2667b03e35f5addbc6fe4947, 044dcb68c5a01073499af9020519af38429e20ae]
source_commits: [68fad804ec5946cb296f77dc5b336308a66abf12 (legacy-cleanup), aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c (main)]
evidence_manifest: ../../tools/evidence/retired-topic-selection-fair-results-20261031/manifest.json
---

# 三个来源的模型身份

三份 JSON 都来自退役选题 probe，但模型不同：第一份是四人三类型 chores 的固定成本审计，第二份是 additive goods 的 EFX 与 fPO 兼容性检查，第三份是抽象 labelled matroid 的 basis-exchange 图穷举。它们的“无失败/有反例”不能相互迁移。

## 1. 三值 chores 类型审计

来源 ID `804a27a2cded4f022da8`，大小 9,338 字节，SHA-256 `c570f3ad42aedc205072dc30633303f16fe3c636d127e6baeec9acdedce3e011`。来源声明原模型来自 arXiv `2606.08872v2 §3`，算术为整数与 Fraction、seed 20261020、无容差。另有 24 个独立 labelled controls，均记录最优 alpha=1；4 个非法输入被拒绝。

核心固定实例为四人、类型重数 `[3,5,5]`，成本矩阵两类对称：前两人行 `(large,1,medium)`，后两人行 `(large,medium,1)`。主要参数 `large=20, medium=7` 时：

- 完整 type allocations 数 62,720；
- EFX type allocations 为 0；
- 最优 alpha 为 `23/22`；
- 有 4 个达到最优 alpha 的 type allocations；
- 一份 witness 的四个 bundle 为 `[[0,3,3],[1,2,0],[1,0,1],[1,0,1]]`。

同一结构的边界对照显示：`(large,medium)=(7,7)` 有 60 个 EFX allocations 且 alpha=1；`(20,1)` 有 4 个，`(19,7)` 有 12 个，`(21,7)` 有 4 个。因而“增大 large 必然使 EFX 变难”不是由这组有限数据支持的单调命题。

该结果是固定三类型/四人/给定参数的精确枚举；它不证明一般三值 chores 的近似下界、最小件数或连续参数区域结论。已有 fair_chores 文档把它作为固定实例障碍保存，本批补回源 ID 和完整结果字段。

## 2. fair FPO 独立 Fraction 交叉检查

来源 ID `018d90eb4aee7838c480`，大小 3,539 字节，SHA-256 `946bd77da963fb3cedfa24f8555b4f4cf7dffad71fd286fb0e2e334085fffae2`。JSON 明示 `fractions.Fraction; no numerical solver`，共检查 256 个实例、1,600 个 allocations。

经典固定例为两类 goods 数量 \(A=B=2\)，两名代理同权估值参数 \(a=10,b=9\)：唯一记录的 EFX allocation 为 `[1,1]`，但最佳 fPO allocation 为 `[0,1]`，最佳 fPO quality 为 `10/11`。参数族 `(a,b)=(3,2),(4,3),(5,4),(10,9),(100,99)` 的质量分别为 `1,4/5,5/6,10/11,100/101`；weighted examples 还记录权重 `(2,1)` 与 `(3,1)` 时质量 `5/11` 和 `2/3`。

JSON 状态写明“known counterexample reproduced”，并限制为 finite exact crosscheck。它只说明在该 additive goods/FPO 语义下，EFX 和分数 Pareto 改进存在固定冲突；不证明所有 fPO、所有人数/物品数的近似下界，也不提供算法复杂度结论。

## 3. 拟阵交换直径穷举

来源 ID `4a4127c9a96303599be0`，大小 4,465 字节，SHA-256 `5a2549b3607a18588ad55940fa2e7d920f827f409c542e2f3d5ed84fe3a99c33`。JSON 明示 integer bitsets、无浮点、穷举，`max_n=5`。总计：498 个带标号抽象拟阵、28,424 个非空基支持、18,833 个按每个拟阵分别去重的交换有向图、242,976 个可达的不同地面元素有序对，全部 finite cases passed。图的顶点是地面元素，计数不指基对；支持重复产生同一图时只检查一次，不同拟阵产生同一图时仍分别计数。源码机制、独立交叉核验与复现见[五元以内拟阵公共基交换距离核验](../../../matroid-structures/state/计算/五元以内拟阵公共基交换距离核验--计算.md)。

strata 给出 `n≤5`、各 rank 的 matroid/profile/graph/pair 数。`longest_witnesses` 的键为 `δ=rank−girth`，按这个差值分四类；每类保留一个达到该类有限最大距离的见证，未列全部达到者：

- 标记 `-1`：n=4、rank=2、girth=3，距离 2，bound 2；
- 标记 `0`：n=4、rank=2、girth=2，距离 2，bound 3；
- 标记 `1`：n=5、rank=2、girth=1，距离 2，bound 4；
- 标记 `2`：n=5、rank=3、girth=1，距离 1，bound 5。

这些数据说明所枚举交换图在小 n 上没有违反探针的距离界，但不证明更大 n、所有 matroid 类、任何游戏成本 corollary 或新颖性。`limits` 字段明确保留这些边界；第三阶段可将 n≤5 统计与 matroid-exchange 候选连接，不把有限穷举改写成渐近直径定理。

## 证据等级与独有内容去向

**精确固定结果：** 第一源 alpha=`23/22` 的四人三类型障碍、第二源 `10/11` FPO 反例与 256/1600 Fraction 检查、第三源 n≤5 的 498/28,424/18,833/242,976 穷举统计。

**模型边界：** chores 的 EFX 删除语义、goods 的 EFX/fPO 语义和抽象 matroid exchange 图保持独立；不能用一个模型的无失败或反例替代另一个模型。

**未建立：** 没有一般三值 EFX 定理、没有任意规模 fPO 近似定理、没有更大 n 的 matroid 直径证明，也没有外部新颖性认证。原三份 JSON、稳定 ID、SHA 与本审查正文是全部独有去向。
