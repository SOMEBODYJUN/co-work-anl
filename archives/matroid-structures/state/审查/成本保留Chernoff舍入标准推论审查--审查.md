---
id: matroid-structures/cost-preserving-chernoff-corollary-audit-v1
kind: review
type_tag: 审查
title: 成本保留 Chernoff 舍入标准推论审查
status: retained-likely-standard-corollary-pending-oracle-check
truth_status: internal derivation with explicit technical gates; no external certification
review_level: full-frozen-source-read
summary: "完整读取 COST_CHERNOFF_COROLLARY_CHECK.md；保留其从均值依赖 Chernoff 半径到自洽误差体的推导、cost-preserving face argument 和四项技术门，处置为很可能是既有 2026 工具的直接推论，不宣称新定理或解决原公开问题。"
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:history/retired_topic_selection/independent_review/research/topic_selection/generalized_assignment/COST_CHERNOFF_COROLLARY_CHECK.md
source_ids: [c03d9e6282eba6f0e86f]
source_sha256: [2fed2a5ebf098fe9777af2c2f52fbeb533a0afc82f200718e56a7e86ace65432]
source_blobs: [55220aaaae6f4e5138a73cbaa7b20fcbd1c6848c]
source_commits: [68fad804ec5946cb296f77dc5b336308a66abf12 (legacy-cleanup), aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c (main)]
evidence_manifest: ../../tools/evidence/generalized-assignment-cost-cher-20261031/manifest.json
---

# 来源身份与拟推论合同

冻结源 `COST_CHERNOFF_COROLLARY_CHECK.md` 大小 3777 bytes，SHA-256 `2fed2a5ebf098fe9777af2c2f52fbeb533a0afc82f200718e56a7e86ace65432`，blob `55220aaaae6f4e5138a73cbaa7b20fcbd1c6848c`。原文件状态就是 `LIKELY_STANDARD_COROLLARY_PENDING_CHECK`：这是查重/技术自洽记录，不是已认证新定理。原件与 marker/hash 校验在 [generalized-assignment-cost-cher-20261031](../../tools/evidence/generalized-assignment-cost-cher-20261031/)。

源文把问题放在一个 matroid base polytope 上：(M) 是有限拟阵，(Q=P(M)) 为 base polytope，(x\in Q)，(c) 是有理线性 cost，(a_1,\ldots,a_k\in[0,1]^E)。拟推论希望随机多项式时间输出一个 basis (B)，以常数成功概率同时满足

[
c(B)\le c\cdot x,
\qquad
|a_r(B)-a_r\cdot x|\le O\!\left(L+\sqrt{(a_r\cdot x)L}\right),
\quad L=\lceil\log_2(2k)\rceil.
]

它不要求精确 marginals；“每次输出 cost 都不超过 (c\cdot x)”与 exact marginal 保持通常并不相容。该合同的精确适用域和随机舍入 oracle 依赖必须在接续工作中逐字对照母文，不能因为推导形式漂亮就把它写成一般 generalized-assignment 算法或新 Chernoff 定理。

# 1. 自洽误差体推导

记
[
\mu_r=a_r\cdot x,
\qquad s_r=L+\sqrt{\mu_rL},
\qquad r_r=K s_r,
]
其中 (K) 是待固定的绝对常数，定义中心为 (x) 的误差体
[
R=\{v:|a_r\cdot v|\le r_r\quad\forall r\}.
]

先解
[
\min\{c\cdot y:y\in Q\cap(x-R)\},
]
得到 (y^*)。(x\) 本身使 LP 可行，(Q) 有界所以最优值达到。对每个 (r)，
[
\nu_r=a_r\cdot y^*\le\mu_r+r_r.
]

在 (y^*) 所在最小 face 上使用 face-preserving 的 matroid SwapRounding（或同类 Chernoff rounding），若标准联合成功事件成立，则
[
|a_r(B)-\nu_r|\le C\left(L+\sqrt{\nu_rL}\right).
]
由于 (L\le s_r) 且 (r_r=Ks_r)，
[
\sqrt{r_rL}=\sqrt K\sqrt{s_rL}\le\sqrt K,s_r,
]
从而
[
C\left(L+\sqrt{(\mu_r+r_r)L}\right)
\le C(s_r+\sqrt K,s_r)
\le K s_r=r_r
]
只要 (K\) 取足够大并满足 (K\ge C(1+\sqrt K))。因此同一成功事件下 (z=\mathbf1_B) 位于 (y^*+R)，并且保留 (y^*) 的 face 身份。

这一步是源文的独有承重内容：把原来依赖未知均值 (
u_r) 的半径，先以 (x-R) 的 LP 自洽地吸收一个 (r_r)，再用常数 (K) 闭合，而不是粗略声称“Chernoff 半径显然固定”。它仍是内部推导，未在本批独立复核 SwapRounding 的每个 oracle 细节。

# 2. 成本不增的 face argument

若标准 face-preserving 结论能提供某个 (lambda>0)，使
[
\bar y=y^*+\lambda(y^*-z)\in Q,
]
则
[
\hat y=\frac{\lambda x+\bar y}{1+\lambda}
      =y^*+\frac{\lambda}{1+\lambda}(x-z)
\]
属于 (Q\cap(x-R))，因为 (z-y^*\in R) 且 (R) 是以线性不等式定义的对称凸体。(y^*) 的最优性给出
[
c\cdot y^*\le c\cdot\hat y
 =c\cdot y^*+\frac{\lambda}{1+\lambda}(c\cdot x-c\cdot z),
]
所以 (c\cdot z\le c\cdot x)。同时 (z-x\in R-R=2R)，得到目标误差至多两倍半径；常数吸收在 (O(\cdot)) 中。

该 argument 的适用条件是“(z) 与 (y^*) 在同一个可延伸 face，且 face-preserving rounding 输出确实给 basis”。若只知道普通 SwapRounding 输出一个 basis，不能自动写出这一步的 (lambda)。源文因此把 face 保持列为第一技术门，而不是把成本推导当作无条件完成。

# 3. 四项技术门与真实缺口

1. **面保持与 oracle。** 需要核对标准 SwapRounding 的 basis 分解是否全部位于 (y^*) 的最小 face；可将问题限制到该 face 对应的 matroid minor，但要给出 rank-oracle、分解和位复杂度。不能只援引“拟阵舍入”四个字。
2. **有理输入。** (sqrt{\mu_rL}) 可能不是有理数；可用 (\lceil\sqrt{\mu_rL}\rceil) 的整数上界，每行只增加 1，因 (L\ge1) 被常数吸收。若原问题要求严格位复杂度，这个替换及 (mu_r) 的算术表示必须写全。
3. **联合成功与重试。** 选择 (L) 的常数使 (k) 行同时成功概率至少为常数（源文目标是至少 (1/2)），失败可逐行核验并重复至成功。成本保证只对已核验成功输出承诺；不能把期望输出成本误写成每次输出成本。
4. **合同强度。** 本推导只给 (O(\cdot)) 误差，不给母文可能要求的精确尾概率、精确常数、marginals 或多预算同步合同。若原公开问题要求这些更强属性，必须重新读原文定义，不能由此 note 自动覆盖。

# 4. 处置与接续

本源处置为 `retained-standard-corollary-audit`，不是 `integrated-theorem`：它完整保留自洽半径、LP、face argument、成本不增推导和四项技术门，且准确记录“很可能是 2026 通用工具的标准组合”这一状态。它可作为后续 generalized-assignment/rounding 工作的检查清单：先证明有理 LP 与最小 face 的可计算性，再逐字核对母文 Chernoff 常数、oracle 和成功重试。没有完成这些门以前，不应声称 GA-01 已解决、提出新 matroid Chernoff 定理，或把它迁移到 fair-allocation 的 EF1/SD-EF1 对象。
