---
id: unrelated-machines/conditional-leaf-hall-proof-canonical-read-after-20261031
kind: review
type_tag: 审查
title: 条件叶 Hall 投影与一致边际四源证明读后
status: integrated-v2-v3-proof-read-after
truth_status: restricted-relaxation-projection-and-family-obstruction
review_level: full-source-read
scope: conditional leaf Hall v2, consistent-marginal v3, path projection, and Q_t family; no actual-YES hardness or generic UM result
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/sol_conditional_leaf_hall_exact_first_review.md
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/sol_conditional_leaf_hall_author_read_after.md
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/sol_conditional_leaf_hall_consistent_marginals_author_read_after.md
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/sol_conditional_leaf_hall_final_canonical_review.md
source_ids: [c36affbedf5dbbdc82cf, ee48773613be507fe14e, 980f7d9ca13ea7f9a0b4, 4c1d42084dbfbe3f593f]
source_sha256:
  - f5e2bbfc15066eff1969a8a91106d92c22103c1c245b80f65eda365e85518812
  - ca41d9f2bde78ceee5a2905ad00ac3ee871467ecfcdc909aa16c2c85d47264f5
  - 4cd8ac153a7532edd5e97a4009e741c2c7142827b7b5f93b96a984da323dff41
  - 5a526fd69b8174218796e674e3f378cd1c6bd7f52ced120dad1121ffd168731b
evidence_manifest: ../../tools/evidence/retired-conditional-leaf-hall-proof-canonical-20261031/manifest.json
related_objects:
  - archives/unrelated-machines/state/障碍/一致条件叶边际仍无福利下界--障碍.md
  - archives/unrelated-machines/state/审查/条件叶Hall与共享汇点联合审查--审查.md
---

# 处置范围与对象身份

本批四源处理同一个 conditional leaf Hall / adjacent-path projection 对象：显式 normalized-flat menu、完整 ordinary matrix、threshold-unit-demand 预处理、旧 R1-R2 relaxation、以及 v3 新增 MC 一致条件边际行。已有《一致条件叶边际仍无福利下界--障碍》保存 v3 Exact-only 原陈述和“待证明”历史状态；本文不覆盖原候选文件，而记录独立 Exact-first、作者 Proof read-after、v3 一致边际 Proof read-after 和 canonical 最终全文核验后得到的证明层增量。

四源独有 SHA 和全文副本位于 `archives/unrelated-machines/tools/evidence/retired-conditional-leaf-hall-proof-canonical-20261031/`。本批没有把作者 checker 的声称执行当作独立运行；独立 v2 审查另有确实运行的 Fraction audit，范围单独登记。

# v2 relaxation 的实际值恒等与 Hall 投影

显式 flat 菜单中，每个 indexed state 的系数总和为一；incidence job 在 private root 的时间是原系数，在 resource machine 的时间是 1；selector 是原 unit job，所有未选 state、zero incidence 与 unused resource 都保留。因此完整 ordinary matrix 的恒等式是 `OPT(P(Q))=2-V(Q)`：

- 给定不交 bundles，选每组最大 state，导出 bundle 中正 incidence，余下原 jobs 留 private，得到 peak 不超过 2-v；
- 给定完整调度且 peak T<2，资源端至多接一个 unit incidence，selected root 的 private load 解出其导出的 state value 至少 2-T，资源导出集合互不交；T>=2 时全 private schedule 作为端点。

阈值 `H_g(epsilon)={u:max_s p_gsu>=epsilon}` 和 `b_g=max_s sum_(u notin H_g) p_gsu` 给出精确 unit-demand 分类：`b_g<epsilon` 当且仅当一个 bundle 达到 epsilon 值时命中 H_g。指定 partition 将原 groups 作为 cores、邻接 path groups 作为 leaves；自动把原 unit-demand groups 也移进 leaves 只有在所有原 groups 都满足非阈值前件时才可用。这个 partition 前提不能省略。

对每个 old resource u 的 d 个 distinct positive core neighbors，转为 d 个 shared group ports，并添加 d-1 adjacent path leaves。旧 basic point `(lambda,z)` 的 global leaf flow 可按 prefix sums 构造：若邻居权为 beta_i=sum_s z_{c_i,s,u}、B_i=sum_{j<=i} beta_j，则 leaf i 在左右 ports 的流为 `(1-B_i,B_i)`（或作者等价的首孔 slack 版本）。行和为一，所有 core+leaf resource columns 不超一；每个 core-state 的 conditional path flow 是该 state 的 lambda 缩放，且在 own port 留出 z。没有除以 lambda，故 zero lambda、d=0、d=1 和 zero/unused data 均闭合。

反向将一个 path block 的 d-1 leaf rows 与 d 个 global columns 相加，恢复旧 resource column `sum_i beta_i<=1`；其余 R1、lambda normalization 和 z bounds 不变。因而在指定 partition 下，full R1-R2 projection 等于旧 basic polytope，extension 具有显式有理多项式位长。正值 allocation 方向利用每个 path 的 d-1 distinct ports，反向值方向说明至多一个 old core port 能保留正值，故 `V(Q^path)=V(Q)`，并且 ordinary OPT 同样保持。正-support FSLP(1) 是 epsilon=1 且 z=lambda 的全支持特例；它不等同于任意 fractional z，也不带入 full CONFIG/PSD。

# Q_t sharp family 与独立核验

canonical 最终稿采用 diffuse parking family：D=t^2；一个 M group 在 `g_(a,j)` 上每项权 1/D；每个 H_(a,j) 有 home state（home resource 权 1）和 parking state（t 个 `A_(a,h)` 各权 1/t）。在 epsilon=1，原 core groups 留在 C，新增 path leaves 属于 L；给定 lambda/z point 的 core resource columns 与 global path flows 可行，且每个 conditional flow 由完整 path matchings 的 rational mixture 构成。

对任意正最小值 allocation，若 M 获得 q 个 home resources，则 q 个 displaced H groups 各需不同 parking resource，故 q<=t；M value 至多 q/D<=1/t。显式取 q=t 并给 displaced helpers distinct parking resources 达到 1/t，因此 `V(Q_t)=1/t`，由 ordinary identity 得 `OPT=2-1/t`。所有 original jobs（包括未选 state、zero incidences 和 duplicate payload）仍安排在完整矩阵中。固定 epsilon>0、t>1/epsilon 时，relaxation 在自身 threshold 可行而 value 低于 epsilon；这是 relaxation obstruction，不是 actual-YES hardness。

独立 Exact-first 记录另外实际运行 Fraction audit：t=2、D=4，完整矩阵 180 machines、201 jobs、404 finite entries，峰 3/2；同时核了 partial-z、zero-lambda、d=0/1/2、unused resource 和显式 zero-job toy。审查文本保留脚本 SHA `a27da8f52dc4fbe2bf719214c1d38ea2fbc75d3ef0a310fcb75b54bb0457fc38` 与结果 SHA `e547154c40c14ae882ffb5bf83903b70724fd55e0fc96421e4173ee4789fa48c`；本批未重跑 author checker，也不把有限 t=2 运行当作任意 t 的证明替代。

# v3 MC 一致边际的增量证明

v3 在每个 core c 与 leaf edge (ell,u) 加入 `sum_s y_cs_(ell,u)=y0_(ell,u)`。该 MC 只要求 conditional edge marginals 的平均与 global flow 相同，不要求 all-core states 的共同 joint law，也不把每个 core 的完整 matching 相关性强行耦合。

consistent-marginals author read-after 对 lower-fill transportation 给出完整扩展：以一个 common hole law pi 为列边际，state row 的 z 为 own-column lower bound；残差行 `lambda-z` 与残差列 `pi-b` 的总量相等，用有序 greedy transport 填补。每次填充耗尽一行或一列，故只需线性数量的 rational fills；b=1、lambda=0、zero coefficient state 都不除法。每条 path 的完整 one-hole matchings 按 transport 权混合，得到 conditional row/column 与 MC；若需同一 core 内完整 matching pieces，可用共同区间端点耦合，仍为多项式数量。

该构造保持指定 partition、d=0/1、positive-neighbor D_+、zero/unused data 和 arbitrary fractional z。反向投影仍仅依赖旧 global columns 与完整 leaf rows，故 MC 不改变 old basic polytope。它没有声称多个 core 的 complete matchings 共享一个 joint schedule law；这一限制是证明成立的必要范围。

# 四源比较、边界和未外推项

| 来源 | 独有内容 | 处置 |
|---|---|---|
| `c36affbedf5dbbdc82cf` | 先行 Exact-first：OPT=2-V、threshold 精确分类、prefix-sum path projection、Q_t 值 1/t、独立 t=2 Fraction audit | integrated；独立重构与有限运行分层保存 |
| `ee48773613be507fe14e` | v2 作者 Proof read-after：slack 放置等价、指定 partition 反例、family value 的另一种 v^2 上界、完整 jobs/位复杂度核验 | integrated；不冒称作者 checker 独立运行 |
| `980f7d9ca13ea7f9a0b4` | v3 MC author Proof read-after：transport table、MC edge marginals、matching-mixture/interval coupling、zero/b=1 边界 | integrated；证明仍不提供 all-core joint law |
| `4c1d42084dbfbe3f593f` | canonical 最终全文：新旧 identity 分离、§8–11 兼容、D_+ 与原 D、Q_t sizes、scope boundary | integrated；不重签旧前缀或历史来源 |

四源共同 PASS 只针对该 relaxation、指定 partition/path projection、Q_t family 和 MC edge-marginal consistency。它们不提供 actual-YES approximation barrier、NP hardness、PCP/UGC、full CONFIG/PSD equivalence、一般 unrelated-machines 算法或 UM-TARGET-v1 结论。现有障碍页中的“v3 Exact-only 尚待证明”应由本增量引用，而不是删除原始历史；如第三阶段需要状态转换，可把“candidate statement -> proof read-after PASS”作为版本关系，不能把 t=2 audit 升格为全参数软件证明。

原件、manifest、哈希校验脚本和 validation PASS 见 `archives/unrelated-machines/tools/evidence/retired-conditional-leaf-hall-proof-canonical-20261031/`。
