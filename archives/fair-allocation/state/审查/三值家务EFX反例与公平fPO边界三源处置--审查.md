---
id: fair-allocation/trivalued-chores-and-fpo-boundaries-v1
kind: review
type_tag: 审查
title: 三值家务 EFX 反例与公平 fPO 边界三源处置
status: finite-boundaries-integrated-open-generalizations
truth_status: published-counterexample-reproduction; finite-observations; no-general-theorem
review_level: full-source-read-cross-archive-comparison
summary: "完整读取三值 chores 反例边界笔记、其 Fraction 审计程序和两代理公平-fPO 兼容性边界笔记；保留固定反例、精确有限枚举、已知文献异议与接续缺口，区分 fair_chores 与 fair_goods。"
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:history/retired_topic_selection/multi_lane/research/topic_selection/notes/chores_trivalued_exact_boundary.md
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:history/retired_topic_selection/multi_lane/research/topic_selection/probes/chores_trivalued_type_audit.py
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:history/retired_topic_selection/multi_lane/research/topic_selection/notes/fair_fpo_compatibility_boundary.md
source_ids: [31bf6427a3e6f9a4dbda, 6c5b7982ae2a9f1991d5, ac1287425ffd281aa60c]
source_sha256:
  - f065820a5b36deb16e1c87187faa77dc056434769a00a00f2aa53d29f810bb2e
  - 1145b46f785fa3c8eaffc8abd2257fcf55fbbcbc591cb5c88fc6dd3801c3f731
  - 5a64414593b129da01a864942a27017c053878fd77e2ec648ce13eccc36b7046
source_blobs: [73ac96304dc95f1270631946793819e8ebc8c086, 16ff74426b94af54ce989c76b25b89a3ca7b1e98, 3e56a0f13f4cb68660ff86d0eec7afe556a26419]
source_commits: [68fad804ec5946cb296f77dc5b336308a66abf12 (legacy-cleanup), aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c (main)]
evidence_manifest: ../../tools/evidence/retired-fair-multilane-boundaries-20261031/manifest.json
---

# 身份分离与阅读范围

本页合并三个紧密相关但模型不同的历史来源。前两源是 additive chores 的三值 EFX 反例/审计；第三源是 two-agent additive goods 的 WEFX 与 fractional Pareto optimality（fPO）兼容边界。它们都不属于当前六人 CAG-SPE，也不能把 chores 反例转成 goods 结论。原件、SHA、有限字段验证和脚本副本见 [retired-fair-multilane-boundaries-20261031](../../tools/evidence/retired-fair-multilane-boundaries-20261031/)。

# 1. 三值 chores：固定已知反例与有限邻域

## 1.1 模型与 alpha-EFX

`SEL-CHORES-TRIVALUED-AUDIT-v1` 的固定输入有 4 agents、三种 chores (A,B,C) 重数 ((3,5,5))。agents 1、2 对每种 item 的 costs 是 ((R,1,q))，agents 3、4 是 ((R,q,1))；完整分配、同权、可加成本。chores 侧 α-EFX（α≥1）量词是：对每 (i,j) 和每个自身 item (g\in X_i)，

$$
c_i(X_i\setminus\{g\})\le\alpha\,c_i(X_j).
$$

空 own bundle 条件为空；若右侧为零而左侧正，则该分配没有有限 α。不能把它与 goods 的“删对方 item”或 (EFX^+_0) 混写。

## 1.2 完整有限表

原始笔记逐字段给出：

| (R) | (q) | type-count matrices | EFX matrices | best finite α |
|---:|---:|---:|---:|---:|
| 20 | 7 | 62720 | 0 | (23/22) |
| 7 | 7 | 62720 | 60 | 1 |
| 20 | 1 | 62720 | 4 | 1 |
| 19 | 7 | 62720 | 12 | 1 |
| 21 | 7 | 62720 | 4 | 1 |

(62720) 是三类重数在四人间的有限 type-composition 枚举；相同类型的标签不改变该模型的不等式，因此计数矩阵足够核验这些固定输入，但不能替代一般 labelled algorithm。原例 (R=20,q=7) 的一个计数 witness 是：
```text
X_1=(0,3,3),  X_2=(1,2,0),  X_3=X_4=(1,0,1).
```
agent 1 删除自己最小的 (R)-cost item 后剩余成本 23，评价 agent 2 包的成本为 22，故该 allocation 的因子至少 (23/22)；完整枚举支持这是固定实例的最优有限 α。该数值是本地有限核验，不能冒称母文报告的一般新界。

R 从 20 调到 19 或 21、q=1 时 EFX 又出现，说明失败依赖离散组合结构，不支持“大项越大越难”的单调推断。固定实例本身只是已知文献反例复现与参数边界工具，不是新一般下界。

## 1.3 脚本的双 oracle 与输入防护

`chores_trivalued_type_audit.py`（7039 bytes）实现两个独立接口：

- `solve_types` 枚举每类的 compositions；`type_factor` 用自有 bundle 最小单件成本得到删除后的最坏 residual，再对所有比较 bundle 用 `Fraction` 求最小 α；
- `solve_labelled` 展开每个 labelled chore，逐 item 删除并直接检查不等式，作为不依赖“减最小项”捷径的控制 oracle。

程序先核对每类矩阵列和、α、最佳 witness 和预测的组合数；18 个随机/小控制实例要求两个 oracle 的 `optimal_alpha` 相等；显式拒绝空 costs、矩阵维度不齐、负成本和负重数。大例保留 seed 20261020、Python 版本、整数与 `Fraction` 算术、代码 SHA。该实现是复现工具，不是证明任意 (R,q) 的 EFX 分类。

## 1.4 邻域扩展的真实边界

原笔记还记录同一 ((R,q)=(20,7))、重数上界 ((3,5,5)) 下 142 个非空真删除子实例均有 EFX，故该固定反例在删除偏序下极小；以及 (q=2..12,R=q+1..50) 的 473 个整数网格点中 21 个失败，失败点满足观察区间 (2q+6\le R\le3q-1)。这些数字来自笔记引用的另一个 probes/结果来源；本批未将那些程序与结果单独 claim，因此保留为“来源报告的有限观察”，不升级为已证明参数刻画。一般化反例的最小 item 数、连续参数区间和任意 agent 数仍开放。

处置：笔记 `integrated-finite-boundary-review`，程序 `integrated-reproduction-method`。它们应作为已知障碍与有限测试资产保留，不作为新反例 claim。

# 2. two-agent goods：WEFX 与 fPO 的兼容性边界

## 2.1 精确模型

`SEL-FAIR-FPO-PROBE-v1` 固定两代理、两类可复制 goods，数量 A、B 为非负整数。agent 1 的 values 是 (1,a)，agent 2 是 (1,b)，其中 a、b 为严格正有理数；权重 w1、w2 严格为正。完整计数分配是 agent 1 得 (x,y)，agent 2 得 (A-x,B-y)。

\(\alpha\)-WEFX 量词为对所有 \(i,j\) 和每个 \(g\in X_j\)，
$$
\frac{v_i(X_i)}{w_i}\ge\alpha\frac{v_i(X_j\setminus\{g\})}{w_j},\qquad 0\le\alpha\le1.
$$
fPO 是不存在一个分数分配使双方效用都不降且至少一方严格提高。一般算法、零估值、多代理和压缩位复杂度不在此 probe 结论内。

## 2.2 已知致命反例与有限 oracle

Davidiuk 等的已知输入 (A=B=2,a=10,b=9) 中，唯一 EFX 计数分配是双方各 ((1,1))，但存在分数分配使 agent 1 获 (11/10) 个第二类，agent 2 获 2 个第一类和 (9/10) 个第二类，双方弱改进且至少一方严格改进。因此无条件“WEFX/EFX 与 fPO 总兼容”已被反例否定；这不是本队新反例。

独立 probe 采用三个互相独立的有限接口：

1. 正社会权重比 (r) 的阈值区间：第一类给 agent 1 需 (r\ge1)，给 agent 2 需 (r\le1)；第二类阈值对应 (b/a)。
2. ([0,A]\times[0,B]) 分数多边形：以 `Fraction` 精确枚举双方效用不降约束的边界交点，检查是否存在严格改进。
3. 所有整数计数分配逐项删除，计算 α-WEFX，并涵盖空物品、单类为空、相同估值、分数估值和非均等权重。

来源笔记报告 256 个实例、1600 个整数分配上两种 fPO 判定完全一致；已知反例的 fPO 可达最佳公平因子为 (10/11)（agent 1 取 ((0,1))），这是固定输入的精确有限结果。对应程序和 frozen output 是另两个 source，本批未独立 claim，因此不把 256/1600 当本页新运行。

## 2.3 接续边界

此对象的价值是分类接口：正权阈值可先确定 fPO 结构，再问在 (A,B,a,b,w) 的何种区域存在精确 WEFX、或最优近似因子是多少。已知反例只否定无条件兼容，不给多代理/多类型一般下界；有限 probe 与两代理支持权刻画也不认证新颖性。后续必须继续核对 personalized bivalued 文献和近似界，不能把探针的有限一致性写成一般定理。

# 3. 三源比较与处置

这三源共同提供“公平目标与效率目标可能不兼容”的边界资料，但模型和量词不同：三值 chores 用删除自身 item 的 α-EFX；two-agent goods 用删除对方 item 的 WEFX 与 fractional Pareto；它们没有共同的 allocation space 或公平方向。第三阶段关系只能标为“已知反例/有限审计/模型对照”，不能建立跨模型推论。

- `31bf6427a3e6f9a4dbda`：`integrated-finite-boundary-review`，保留 4-agent/(3,5,5) 反例、完整有限表和邻域报告边界。
- `6c5b7982ae2a9f1991d5`：`integrated-reproduction-method`，保留 type 与 labelled 双 oracle、Fraction 算术、控制集与输入拒绝。
- `ac1287425ffd281aa60c`：`retained-known-counterexample-and-finite-probe`，保留两代理 WEFX/fPO 反例、支持权接口和未完成文献/新颖性义务。

所有正文和证据均已保留稳定 ID、来源 SHA、独有内容去向及未读依赖，未把固定反例或有限网格升级为一般数学结论。
