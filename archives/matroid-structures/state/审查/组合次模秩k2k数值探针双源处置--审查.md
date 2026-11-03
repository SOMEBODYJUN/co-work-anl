---
id: matroid-structures/combinatorial-submodular-k2k-numerical-probe-v1
kind: review
type_tag: 审查
title: 组合次模秩 k2k 数值探针双源处置
status: finite-numerical-evidence-no-global-proof
truth_status: numerical finite evidence; rank checks finite only
review_level: full-source-read
summary: "完整读取 combinatorial_submodular_k2k.py 与结果 JSON；保留 k=2..16 的 SLSQP 约束优化、k≤4 的显式 rank enumeration 和浮点误差边界，明确不构成全局优化或渐近定理。"
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:history/retired_topic_selection/multi_lane/research/topic_selection/probes/combinatorial_submodular_k2k.py
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:history/retired_topic_selection/multi_lane/research/topic_selection/probes/combinatorial_submodular_k2k_results.json
source_ids: [b069b4c79a03708a055d, 59209d4561b3eddcbb4d]
source_sha256:
  - 936eda8b34beca49b6f0b76a0914592e2ca993b4f09f2378569054c7b5f3888b
  - b81d695f184a4d4930b3ccc045fe38f86c946156222e703d5505a55d92c5e62a
source_blobs: [31d65d3aa9b67458b2949867ba0bbe8a5fc317f8, 01338c1775976f07fdefa8a570be73db4ae77d27]
source_commits: [68fad804ec5946cb296f77dc5b336308a66abf12 (legacy-cleanup), aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c (main)]
evidence_manifest: ../../tools/evidence/retired-combinatorial-submodular-k2k-20261031/manifest.json
---

# 对象与实现

这组源属于 combinatorial submodular / matroid-rank 数值探针，不是 fair_chores rank-cap-2、goods-with-copies 或当前 CAG-SPE。脚本声明“finite numerical probe, not a global optimization proof”，使用 Python 3、NumPy/SciPy、seed 20261020。原件、结果、SHA 和验证见 [retired-combinatorial-submodular-k2k-20261031](../../tools/evidence/retired-combinatorial-submodular-k2k-20261031/)。

`nullity(a)` 令 (p_i=a_i^2/4)，计算
[
N(a)=\sum_i p_i-1+\prod_i(1-p_i),
]
`ratio(a)=1-N(a)/(k+1)`。对每个 k=2..16，SLSQP 在 (a_i\in[1,2])、(sum_i a_i=k+1) 下优化 ratio；起点包括均匀向量、每个坐标取 2 的向量和 120 个 Dirichlet 随机扰动。结果取成功局部 runs 中的最小值，不是证明全局最优。

`enum_rank(x)` 把 (2k) 个 Bernoulli bits 按 k 对分组；若一对同时选中，`c` 计数，rank 为
[
\sum_i b_i-\max(0,c-1).
]
]
它显式枚举 (2^{2k}) bits，用于 k≤4 的 formula/direct sanity checks。

# 数值结果

`combinatorial_submodular_k2k_results.json` 大小 7476 bytes，状态字段明确为 `finite numerical evidence, not proof`。base optimization 的 best ratio 如下（仅列 k 与 best；symmetric/one_full 也保留在原 JSON）：

| k | best numerical ratio | symmetric | one-full |
|---:|---:|---:|---:|
| 2 | 0.89453125 | 0.89453125 | 0.9166667 |
| 3 | 0.8703613 | 0.8737997 | 0.875 |
| 4 | 0.8500000 | 0.8599216 | 0.85 |
| 5 | 0.8333333 | 0.8487710 | 0.8333333 |
| 6 | 0.8214286 | 0.8394126 | 0.8214286 |
| 7 | 0.8125000 | 0.8314309 | 0.8125 |
| 8 | 0.8055556 | 0.8245627 | 0.8055556 |
| 9 | 0.8000000 | 0.8186137 | 0.8 |
| 10 | 0.7954545 | 0.8134314 | 0.7954545 |
| 11 | 0.7916667 | 0.8088929 | 0.7916667 |
| 12 | 0.7884615 | 0.8048982 | 0.7884615 |
| 13 | 0.7857143 | 0.8013647 | 0.7857143 |
| 14 | 0.7833333 | 0.7982244 | 0.7833333 |
| 15 | 0.78125 | 0.7954207 | 0.78125 |
| 16 | 0.7794118 | 0.7929066 | 0.7794118 |

最佳向量在多数 k 中接近 one-full：一个坐标约 2，其余约 1；但 k=2/3 的局部 SLSQP 结果与 one-full/symmetric 有细微差异。这个模式是候选启发，不是全局极值分类或渐近公式。

rank_checks 共 16 行（k=1..4、zero/all/balanced/random），formula 与 enumeration 最大误差约 (4.4\times10^{-16})，其余为 0。误差是浮点枚举的机器精度，不能替代精确有理证明；`Fraction` 只被导入而未用于优化主循环。

# 处置与接续

- `b069b4c79a03708a055d`：`integrated-finite-numerical-method`，保留 SLSQP 约束、随机起点、bounds/sum 条件和显式 rank enumeration。
- `59209d4561b3eddcbb4d`：`integrated-finite-numerical-evidence`，保留 k=2..16 表、successful starts、symmetric/one-full 对照和 16 rank checks。

后续若要升级，需要证明全局最优结构（例如 one-full 的极值性）、控制 SLSQP 局部最优与浮点误差，并给出所有 k 的符号推导。当前对象不进入 fair-allocation 的公平定理主线，也不从数值 ratio 表推导 general matroid/rank-cap 结论。
