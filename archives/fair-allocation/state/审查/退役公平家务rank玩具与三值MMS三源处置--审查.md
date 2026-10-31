---
id: fair-chores/rank-toy-mms-and-graph-results-v1
kind: review
type_tag: 审查
title: 退役公平家务秩玩具、三值 MMS 与图定向结果三源处置
status: finite-evidence-integrated-with-retired-negative-lesson
truth_status: finite-computational-evidence; open-general-claims-preserved
review_level: full-frozen-result-read-cross-archive-comparison
summary: "完整读取 rank_toy_results、toy_results 两个冻结 JSON；区分 class-touch 成本与真正 rank-cap-2、三人三件配额 MMS、signed endpoint 图定向以及被淘汰的 sharp-Delta 玩具，不把有限无反例升级为一般定理。"
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:history/retired_topic_selection/independent_review/evidence/runs/topic_selection/fair_chores/rank_toy_results.json
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:history/retired_topic_selection/independent_review/evidence/runs/topic_selection/fair_chores/toy_results.json
source_ids: [ec9078c268c9f73c28ff, a17cc0b56d2466699cdb]
source_sha256:
  - c55c56b356811fea08ec04548a0ad3aff51ec40f8def5411fe873e31b7972a3e
  - 3a097378f4b2e209ac1d9c34c6317bb626617b74c557b2e9931d49969b3a9251
source_blobs: [4d21e242d42a2d2ca1c6b18e50372be26872f2c7, 8791cf7139f8cdf47b78147d3a05c00ce653a232]
source_commits: [68fad804ec5946cb296f77dc5b336308a66abf12 (legacy-cleanup), aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c (main)]
evidence_manifest: ../../tools/evidence/retired-fair-chores-toy-results-20261031/manifest.json
---

# 阅读范围与模型身份

本页处置两个冻结结果摘要；原 JSON、source blob、SHA、字段校验和验证脚本见 [retired-fair-chores-toy-results-20261031](../../tools/evidence/retired-fair-chores-toy-results-20261031/)。本批没有把对应生成脚本当作已重跑程序。两源虽然同属 `fair_chores` 退役研究线，`toy_results.json` 内仍并列保存三个不同候选模型：三人三件配额 chores MMS、signed endpoint 图定向 (EFX^+_0)，以及 restricted additive + optimum social cost 的 sharp-(Delta) 负面玩具。它们分别归类，不能把一个对象的“无失败”搬给另一个对象。

# 1. `rank_toy_results.json`：partition-rank 成本的有限精确枚举

冻结 source ID `ec9078c268c9f73c28ff`，路径是 `fair_chores/rank_toy_results.json`，SHA-256 为 `c55c56b356811fea08ec04548a0ad3aff51ec40f8def5411fe873e31b7972a3e`，大小 1133 bytes。五行聚合如下：

| n | m | classes | loops | profiles 完成 | 每 profile allocation | seed | counterexample |
|---:|---:|---:|---|---:|---:|---:|---|
| 3 | 8 | 2 | false | 1000/1000 | (6561=3^8) | 20261020 | null |
| 3 | 9 | 2 | true | 500/500 | (19683=3^9) | 20261021 | null |
| 3 | 8 | 3 | false | 1000/1000 | (6561=3^8) | 20261022 | null |
| 3 | 8 | 3 | true | 1000/1000 | (6561=3^8) | 20261023 | null |
| 4 | 7 | 2 | true | 500/500 | (16384=4^7) | 20261024 | null |

每一行的 `requested_trials` 等于 `completed_trials`，表示随机 profile 计划完成；每个 profile 内部穷举了把 (m) 件物品给 (n) 个 agent 的全部 (n^m) 标号分配。因而其量词是“抽样 profile、profile 内完整 allocation 枚举”，不是所有 cost profile 的穷举。

## 1.1 与 FC-LEMMA-R2-2C-v1 的边界

两类、无 loops 的第一行是两平行类局部引理的相邻有限测试；但 JSON 没有写出引理证明，也不覆盖所有 (n,m)。两类有 loops 的第二行已越过原引理的 no-loop 假设。更关键的是，候选报告明确说明三类行的成本是**触达类数**，不是 (\min(2,\text{触达类数})) 的真正 rank-cap-2 成本。因此三类行不能与本批已处置的 `rank2_cap_results.json`（ID `d096e18feaaf131152a6`）合并，也不能声称已验证“所有 rank≤2”。

此源保留的独有内容是：2/3 classes、loops 开关、五组 (n,m)、seed、profile 数、每 profile 的 (n^m) 精确分配数以及全部 `counterexample=null`。正确状态为有限正面证据；下一义务仍是为三类 rank-cap=2、loops 和个性化类标号寻找覆盖/共同彩虹机制或最小反例。处置：`integrated-finite-evidence`。

# 2. `toy_results.json`：三值配额 MMS、图定向和淘汰的 sharp-Δ 玩具

冻结 source ID `a17cc0b56d2466699cdb`，SHA-256 为 `3a097378f4b2e209ac1d9c34c6317bb626617b74c557b2e9931d49969b3a9251`，大小 2370 bytes。该 JSON 不是单一模型；以下逐对象处置其三个顶层字段。

## 2.1 `mms`：三人、九件、每人三件的有限配额检查

三行都固定 (n=3,q=3)，即 (m=3n=9) 且每个 agent 必须得到恰好三件 chores。值域分别为 `[0,1,2]`、`[1,2,3]`、`[1,2,5]`；每行请求并完成 10,000 个随机 profiles，seed 分别为 20261020、20261021、20261022。每个 profile 精确枚举 280 个无标号三三 partition 和 1680 个 labelled allocations；这两个数字分别是

[
\frac{9!}{(3!)^3 3!}=280,
\qquad
\frac{9!}{(3!)^3}=1680.
]

三行 `first_failure=null`，所以在相应有限值域和随机样本内未发现 exact constrained-MMS 失败。候选报告的目标是每个 agent (i) 的

[
\mu_i=\min_{\text{partition of 9 items into 3 triples}}\max_B c_i(B),
\qquad c_i(X_i)\le\mu_i,
]

同时满足每人三件。这里“10,000 个 profile 且每 profile 全枚举”仍不是三值域全称证明，也没有从空 `first_failure` 推出任意 (n)、任意 (m=3n) 或任意非负实数成本的 exact MMS。值集合平移的讨论也必须保留其条件：同一常数平移在 exact quota 下对比较有特殊抵消，不能替代对三值结构的证明。

这部分的首 proof obligation 是从三值 quota 的有限极点/交换结构抽取可推广机制，或找最小不可分配 profile；现有数据是有限候选证据，不是完成的 MMS 定理。处置：`integrated-finite-evidence`。

## 2.2 `mixed_graphs`：另一个图定向有限批次

这四行与本批另一源 `mixed_extension_results.json` 的图对象相同，但值域和计数不同：

| 图 | endpoint 值域 | profiles | exhaustive | 结果 |
|---|---|---:|---|---|
| (C_3) | ({-1,1}) | 64 | true | `no_EFXplus0_witness=null` |
| (C_4) | ({-1,1}) | 256 | true | `no_EFXplus0_witness=null` |
| (C_5) | ({-1,1}) | 1024 | true | `no_EFXplus0_witness=null` |
| (C_5) | ({-2,-1,1,2}) | 10000 | false, seed 20261020 | `no_EFXplus0_witness=null` |

前三个 profile 数为 (2^{2|E|})，对应每条边两个端点取 ({-1,1}) 的有限穷举；最后一行是固定 seed 的随机正面记录。它不包含零值，且没有覆盖 `mixed_extension_results` 中零值 (C_3/C_4)、六点挂树单圈和五点双三角 cactus 的记录。此前已处置的五点双三角 cactus 仍保留 trial 686 的有限障碍；本四行不能抵消或升级该障碍，只能说明不同 profile 域的有限差异。

该字段属于 signed endpoint additive (EFX^+_0)，不是 chores rank 成本。处置为 `integrated-finite-model-comparison`：保留独有值域、图大小、seed 和计数，并在第三阶段以有限验证/模型对照关系接续，不写成所有 cycle 的存在定理。

## 2.3 `discarded_alpha_idea`：restricted additive + OPT 的简单边界

该字段固定 (Delta=5)，成本矩阵

[
\begin{pmatrix}5&1&0\\5&0&1\end{pmatrix},
]

记录最小社会成本 5，以及两个最优分配：`assignment=[0,1,0]` 与 `[1,1,0]`，两者的 `alpha=[5,1]`。候选报告将它归入 restricted additive chores (c_{ie}in\{0,c_e\}) 且要求社会成本最优时的 EFX 因子 (Delta=\max c_e/\min_{c_e>0}c_e) 负面教训，并说明 (Delta=5) 的 (2^3) allocations 被逐一核验。核心机制是先把正成本归一为 binary，再用 binary EFX+PO；按最大/最小正成本比放大计数不等式得到 (Delta)-EFX，且该矩阵说明在 OPT 上因子可达 (Delta)。

它不是一个新的开放定理：该推论简单、候选清单已将 FC-07 淘汰。正确处置是 `retained-negative-lesson`：保留具体矩阵、两个 OPT assignment、alpha 字段及为什么“不能包装成新论文”的理由；不把 alpha 数组误读成普遍 EFX 因子证明，也不把有限三物品核验当作任意 (m) 的紧性定理。

# 3. 两源比较与交接

`rank_toy_results` 的 `counterexample=null` 覆盖五个 class/loops 组合的有限随机 profiles，但三类 rows 明确不是 rank-cap-2；`toy_results.mms` 是三人九件 exact-quota 的另一 chores 模型；`toy_results.mixed_graphs` 和 `mixed_extension_results` 共享 signed graph 研究入口却使用不同值域，不能拼成单一穷举域；`discarded_alpha_idea` 则是已淘汰的 restricted-cost 负面 lesson。它们共同提供边界地图，不能合并成“fair_chores 已解决”。

逐源处置：

- `ec9078c268c9f73c28ff`：`integrated-finite-evidence`，保留五组 rank-toy 聚合、profile/allocation 两层量词和三类非-rank-cap-2 警告。
- `a17cc0b56d2466699cdb`：拆成三个独立对象：三值 quota MMS 的有限正面证据、signed graph 的有限模型对照、restricted-cost sharp-Δ 的保留负面 lesson；不因同一 JSON 而合并公平定义。

两份 JSON 均通过 `clean show` 完整导出并逐字段读取；必要原件、manifest、验证脚本和 `validation.json` 在 evidence 目录。生成脚本尚未作为本批已读来源，验证脚本只检查 SHA、大小和字段形状，不替代数学判断。
