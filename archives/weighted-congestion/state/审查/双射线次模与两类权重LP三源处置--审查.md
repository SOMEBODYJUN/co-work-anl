---
id: weighted-congestion/gap-tools-two-ray-and-two-class-v1
kind: review
type_tag: 审查
title: 双射线次模与两类权重 LP 三源处置
status: finite-numerical-evidence-no-universal-gap-theorem
truth_status: finite numerical evidence; exploratory formulations
review_level: full-source-read
summary: "完整读取 two_ray_search.py/JSON 与 two_class_attack.py；保留双资源射线 enabling-set submodularity 随机 LP 检查、两类 one-large/two-small 权重 LP 及边界网格探索，明确有限数值结果不构成次模或近似下界定理。"
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:history/retired_topic_selection/multi_lane/research/topic_selection/probes/gap_tools/two_ray_search.py
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:history/retired_topic_selection/multi_lane/research/topic_selection/probes/gap_tools/two_ray_search.json
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:history/retired_topic_selection/multi_lane/research/topic_selection/probes/gap_tools/two_class_attack.py
source_ids: [568da6bdf9b911e06494, 29dc49c58094acbb1534, 736f8c7925ac853537f9]
source_sha256:
  - 040f906afa36709a80c8848ed0b0a692830a653bcc3719b23f54036a481d26f4
  - 216c1a17aa1e11d5d5c7ca834d608453192efb9fe80d34a3ad14f41b88a833ed
  - affd74711e28905c7d322a35e75159f6411e5c6d2c78ea620d7f8e38ca1fc03f
source_blobs: [240e1bdb7c11d2503756c3d2ea3790b98dab162e, 264ba583a51074683ef24c03d67a81c52b5bbf0b, c5ffc169dfc66425aa0a9194bddbbe0262e40083]
source_commits: [68fad804ec5946cb296f77dc5b336308a66abf12 (legacy-cleanup), aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c (main)]
evidence_manifest: ../../tools/evidence/retired-gap-tools-20261031/manifest.json
---

# 模型与阅读范围

三源属于 weighted-congestion gap tools，不是 fair-allocation 的 EFX/SD-EF1，也不是当前 CAG-SPE。第一、二源研究两条非负资源射线上的 enabling-set LP value；第三源固定 one-large-or-two-small knapsack feasibility 下的 adversarial weight LP。原件、SHA、验证和脚本副本在 [retired-gap-tools-20261031](../../tools/evidence/retired-gap-tools-20261031/)。

# 1. `two_ray_search.py` 与结果 JSON：两射线 value function 的有限次模搜索

source IDs `568da6bdf9b911e06494`（1517 bytes，SHA `040f906afa36709a80c8848ed0b0a692830a653bcc3719b23f54036a481d26f4`）和 `29dc49c58094acbb1534`（126 bytes，SHA `216c1a17aa1e11d5d5c7ca834d608453192efb9fe80d34a3ad14f41b88a833ed`）。

脚本固定 (n=6)。每次生成两个 2D rays、每 item 的两类 type、正整数 scales、容量 cap 和 weights；对每个 subset mask，调用 SciPy `linprog` 最大化被激活 item 的总 weight。随后逐对未激活 item 计算
$$
V(S\cup\{i,j\})+V(S)-V(S\cup\{i\})-V(S\cup\{j\}),
$$

一旦 defect>1e-7 即保存 counterexample。冻结 JSON 报告 seed 20261020、trials 300、`counterexamples=[]`，并明确 scope 为“Numerical evidence only; all b,w not exhausted.”

这是有限数值探索：rays 仅 1..8、scales 1..4、cap 3..24、weights 1..14，且只 n=6。无反例不证明所有 two-ray LP value functions submodular，更不证明任意资源维度或 weighted-congestion 主目标。处置：`integrated-finite-numerical-method` + `integrated-finite-numerical-evidence`。

# 2. `two_class_attack.py`：固定 x 的权重 LP 与 Poisson 边界

source ID `736f8c7925ac853537f9`，大小 3989 bytes，SHA `affd74711e28905c7d322a35e75159f6411e5c6d2c78ea620d7f8e38ca1fc03f`。脚本声明 finite weight LP exact formulation but numerical solutions are evidence, not universal lower-bound proofs。

## 2.1 固定-x LP

`solve(x,na)` 把前 `na` item 视为 large 类，后项为 small 类；允许的 support 集 (s) 满足 large 至多 1 或 small 至多 2。变量是 item weights 和每个 activation set 的 (t_R)，约束每个 allowed support 的权重和不超过 (t_R)，并固定 (x\cdot w=1)。目标是按独立 activation probabilities 加权的 (t_R) 期望，使用 SciPy HiGHS `linprog`。这提供的是一个精确写出的有限 LP，不是全域 adversarial weight lower bound。

`uniform_subsupport` 仅搜索每个 size class 一种正权，枚举 support 和权重比 ((1,0),(0,1),(1,1),(2,1))；它是受限比较族。`poisson` 计算 uniform class 权重在若干比值下的 Poisson-limit 公式，脚本只检查 (u/v\in\{0,1,2,\infty\})。

## 2.2 数值范围

主程序对 ((n_a,n_b)=(1,2),(2,3),(2,4)) 各 20 cases，固定 (a=0.7,b=0.4)，随机 (x) 并按 cost>1 缩放；比较 unrestricted LP 与 class-uniform supports，记录 violations；随后在 no-mixing feasibility 边界上以 1201 个 grid points 搜 Poisson minimum。输出写入脚本同名 `.json`，本批没有冻结该运行输出，故正文只认证代码逻辑与有限方法，不虚称数值结论。

注释中给出 no-mixing cost closure 的分段公式，但这只是脚本作者的下一步分析接口；没有经过符号证明或全域审计。任何由 Poisson grid 得到的比值都不能作为 weighted-congestion 的 asymptotic gap。

# 3. 处置与模型边界

- `568da6bdf9b911e06494`：`integrated-finite-numerical-method`，保存 two-ray LP value/submodularity 检查。
- `29dc49c58094acbb1534`：`integrated-finite-numerical-evidence`，保存 300 trials/zero counterexamples/finite-only scope。
- `736f8c7925ac853537f9`：`integrated-finite-numerical-method`，保存 fixed-x weight LP、support restriction 和 Poisson boundary grid 代码。

这些对象可在第三阶段作为“有限数值探索/候选障碍”连接到 weighted-congestion gap 工具；不能建立 submodularity theorem、uniformization theorem 或 universal approximation lower bound。它们也不与 fair-allocation 的 EF/EFX 模型建立未经证明的桥接。
