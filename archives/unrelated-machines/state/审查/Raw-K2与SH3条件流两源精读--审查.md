---
id: "unrelated-machines/raw-k2-sh3-conditional-flow-two-source-review"
kind: "review"
type_tag: "审查"
title: "Raw K2 与 SH3 条件流两源精读"
status: "necessary-contract-read-no-decoder"
summary: "两份 review 源分别确认 raw K2 完整 local-law canonical pullback 的给定点非扩展、raw SA3→canonical SA1 同点提取，以及 raw SH3 的 conditional subtree first-flow、M3/zero-column 削减、inclusion capacity cut 与 source-hardness边界。它们是必要接口/障碍，不是 shared integer decoder、一般 UM hardness 或 near-two 结果。"
source_refs:
  - "clean:275160bc0b228ff1fab1"
  - "clean:f6559683ff8f91b86994"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/reviews/unrelated_machines/raw_k2_canonical_pullback_and_sa3_repair_review.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/reviews/unrelated_machines/raw_sh3_conditional_subtree_flow_and_inclusion_capacity_review.md"
---

# 读域与来源

`275160bc0b228ff1fab1`（SHA `12efef755aa9731d4eb361396487bed7513dbdc11b6363c286e850725b820aa9`）审 raw K2 新 §13/§14：完整 local-law/canonical pullback obstruction 与 raw SA3→canonical SA1 同点提取；`f6559683ff8f91b86994`（SHA `b9bafa9f56899ed579e5c67dfc7bedbde9eb55ecb7ac469e1e680d5ecd6cc8e0`）审 raw SH3 conditional subtree flow/inclusion capacity。两源均 clean show 全文实读，原件与 manifest 在 `archives/unrelated-machines/tools/evidence/raw-k2-sh3-review-20261031/`，receipt 草稿在 `cleanup/workspaces/Boss2/raw-k2-sh3-receipts-20261031.json`。

# 1. Raw K2 full local-law obstruction

raw K2 的 18-machine/17-job binary-rational family（`0<c<1`、`T=1+c`）同时满足共同 M2、global affine load localizers、完整 row first/pair laws 和每机三端支持；但跨机 `L(b1b2b3)=-1/160`，canonical claim×state 与 quality×state 同点项也为 `-1/160`、`-c/160`。另有 actualOPT=1 的全 17 jobs schedule；因此负矩是 given-point canonical pullback 的非扩展，不是 actual gap，也不阻止换 canonical point/另求 R。

raw K2 旧 14-machine first/pair 版本仍保留其局限：同机 triple `7/160` 不相容；不能把旧程序的未重跑状态改写成新软件证书。新 §13 的 finite code 只核 18 个 localizers、72 monomials/patterns、负式与 C=1 witness，在有限 c（1/1000、1/2、3/4、999/1000）上精确 Fraction 重跑；没有 general SDP/LP backend、全 schedule 枚举或 decoder。

# 2. Raw SA3→canonical SA1 同点提取

对于 normalized-flat SA3 点，原 boxes、physical slack、unit cap1 乘至多三原 literals，Boolean/one-hot 保到 degree4；所有真实 `T<2` schedules 给 Dirac 点，因此 LP infeasible 才是 sound threshold FAIL。给定同点 `A=a,Z=aE`，四-literal 正性与 `1−aE` 展开支付全部目标 SA1 条目，quality 乘子最多三原 literals；固定 degree rational LP 的 vertex/Cramer/Hadamard 给显式位长。

这是点级 pullback：只保 canonical M1，不提供 M2/CONFIG 或 exact SDP finder，也不能反向声称 raw 与 canonical 两系统包含关系。zero/inactive/unused/repeated states 保留；source cap1 不能替换 T-cap。最小层/锐性/全 group rounding 均未宣称。它的用途是把给定 raw SA3/canonical 点条件映射回 SA1，而不是构造任意实际调度。

# 3. Raw SH3 conditional subtree flow

raw SH3 输入含 native unique-home 与 unit-only entry jobs、sink 无 home/quota，common degree≤6/M3、Boolean ideals、物理 load localizers 与完整 row CFG first/pair。对 non-home unit endpoint E（`p=L(E)>0`）定义 first mass `a`、child flow `b_u`、edge flow `y`，得到 `0≤b_u≤p`、每 token/arc flux≤b_u、内部 export≥`k_u(2−T)b_u`。DAG 拓扑按比例前推得到必要 first-flow；zero-column/M3 可迭代删除 unit heads，保留 original jobs/home/k，mandatory one-hot 为空才 sound FAIL。

当 `(T−1)k_u` 为整数时，活动 home marginal 可在 hypersimplex 分解为整数 exported tokens，配 incoming labels 恢复一根 CFG(1) first-flow；非网格不得 ceil，且不能把 CFG 恢复误用于原 supplied higher moments。k=1 的无衰减 corridor 依额外 incoming/home pair-zero，不能泛化到所有 rows。

inclusion capacity cut family 使用 q-subsets/2q-subsets/q-subsets selectors，positive U mass 给 `δd1(δd2−M)≤H`；严格反向 selectors first mass=0 与 one-hot 冲突，实际 schedule 也执行相同 f/e exports。CONFIG(1) 有显式 witness，峰值上界 `max(1,2−1/d1,2−1/d2)`；这不是有限 q 精确 OPT，也不能直接写成 raw SH3 integrality gap。

# 4. 关系、实现与未解义务

K2 的 given-point nonextension 和 SA3→SA1 point pullback，SH3 的 necessary first-flow/inclusion cut，是不同层次：前者拒绝某个 canonical aggregate 点的原身份 lift，后者给 raw flow 的必要接口和 sound FAIL。两者均未给 shared integer owner/forest decoder、source-to-UM Karp reduction、一般 UM 近二 hardness 或统一算法；source-hardness 角色不能替代这些缺口。

有限软件只验证列明 localizers/参数/120 个 selector families 与小 toy；没有全矩阵/全部 schedules/actual decoder。外部 paper 事实和新颖性按各原审查范围保留，不把程序 PASS 写成数学定理。处置为 `necessary-contract-read-no-decoder`；后续引用需保留 degree/M3、网格与 k=1 条件、canonical point 量词、inclusion cut 的专用族和一般 UM 未解边界。
