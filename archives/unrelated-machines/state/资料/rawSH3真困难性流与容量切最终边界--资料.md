---
id: "unrelated-machines/raw-sh3-true-hardness-flow-inclusion-boundary"
kind: "bridge"
type_tag: "资料"
title: "raw SH3 真困难性流与容量切最终边界"
status: "final-source-read-with-hardness-boundary"
summary: "三份 true-hardness 记录确认 raw SH3 conditional subtree flow、inclusion capacity cut、M3 zero-column迭代删除、整数网格 CFG 恢复和全部原 jobs/位复杂度；最终规范修复了符号重赋值。它仍是必要系统与 sound FAIL 接口，不是一般UM hardness、integer forest decoder或软件认证。"
source_refs:
  - "clean:36245e7351ec810a6ff3"
  - "clean:a9709046d079f132f1ac"
  - "clean:f190dbb29d0f136e1b73"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/sol_true_hardness_raw_sh3_flow_inclusion_final_actual_read_v2.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/sol_true_hardness_raw_sh3_flow_inclusion_v2_author_read_after.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/sol_true_hardness_raw_sh3_general_firstflow_statement_first_reconstruction.md"
---

# 来源身份与最终范围

三份来源是最终 flow/inclusion 规范 read-after、作者 v2 read-after 和 general first-flow Exact-first 独立重构。它们由 true-hardness 角色读取，但本页保留其严格边界：提供必要 raw SH3 流、集合容量切、sound FAIL 与整数网格辅助 CFG，不自动给出 source hardness、actual integer forest、一般 UM 近二算法或软件审计。

| clean ID | 原路径 | SHA-256 | 大小 | 实读性质 |
|---|---|---|---:|---|
| `36245e7351ec810a6ff3` | `history/source/notes/unrelated_machines/sol_true_hardness_raw_sh3_flow_inclusion_final_actual_read_v2.md` | `859cc65437d07e91d6d0b3dab4e674952e67b1ac76dae4322f26b5eff886de96` | 5,190 B | 最终规范稿 actual-read；修订后的唯一符号句定向核验 |
| `a9709046d079f132f1ac` | `history/source/notes/unrelated_machines/sol_true_hardness_raw_sh3_flow_inclusion_v2_author_read_after.md` | `0d2c4fc28e203d04dbe49f5724ee0ee1b5c9097fbb35e15733034045a8900ecb` | 6,932 B | general flow/inclusion 作者 read-after，对照独立重构 |
| `f190dbb29d0f136e1b73` | `history/source/notes/unrelated_machines/sol_true_hardness_raw_sh3_general_firstflow_statement_first_reconstruction.md` | `f758700937f7ccb7526327eb0f6757639cb69cb0a468e8aadbf1cdf300047e8f` | 11,723 B | general first-flow Exact-first 陈述先行独立重构 |

证据原件、manifest 在 `archives/unrelated-machines/tools/evidence/raw-sh3-true-hardness-20261031/`，回执草稿在 `cleanup/workspaces/Boss2/raw-sh3-true-hardness-receipts-20261031.json`。

# 1. 最终规范的必要 flow 合同

输入是 native unique-home/unit-head layered DAG 和 unit-only entry jobs；sink 无自有 jobs/导出需求。共同 functional L 作用到 degree≤6，原 Boolean/one-hot ideals、M3、每物理行完整 CONFIG(T) first/pair、global degree-two load localizers 均使用同一点。任意非-home unit endpoint E 在 vertex v 且 p=L(E)>0 时，定义 b_u=L(E C_u)、y_(u,j,w)=L(E C_u X_(u,j,w))。unit-pair null 及 M3 multiplier 提升给出

`0≤b_u≤p`，`sum_w y_(u,j,w)≤b_u`，`sum_j y_(u,j,w)≤b_u`，
`sum_(j,w)y_(u,j,w)≥k_u(2−T)b_u`。

DAG 拓扑前推设 a_v=p、a_w 为原 unit head flux 总和；令 `f=(a_u/b_u)y`（b_u=0 时为零），则 a_u≤p、每 token/arc flux≤a_u、内部行 export≥r_u a_u，r_u=k_u(2−T)。最终版本明确修复了符号歧义：a、f 始终表示根质量 p 的流；归一化活动为 a_u/p，inactive 为 1−a_u/p。

这是新的一阶流，不保持 supplied L 的原 first/pair/higher moments，也不把其它 entry jobs、selectors 或原全实例免费重排；flow feasibility 是必要接口，不是 actual forest。

# 2. M3 zero-column、迭代删除和整数网格 CFG

若某 raw endpoint x 的 first mass L(x)=0，Boolean x 是 M3 零列；与 degree≤2 单项式相乘仍为零列，从而所有相关 degree≤6 moments vanish。限制余变量后，ideals、M3、localizers 和 row CONFIG first/pair 均保留。只删 unit heads，home jobs、k_u、原 job identities 不删；若 mandatory one-hot job 的资格被删空，才给 sound FAIL。迭代次数由原 unit endpoints 数量支付，LP/位长 polynomial。

若 `(T−1)k_u` 是整数，活动 home marginal vector 在 hypersimplex 中，可分解成恰 d_u=k_u(2−T) 个 exported tokens；与 incoming label distribution 配对可恢复新流的一阶 full CONFIG(T)。非网格不可 ceil(r)，也不能把此 CFG 恢复套到 supplied raw moments 的二阶表。

k_u=1 有额外同一行 incoming/home pair zero，故可以用 export total=a_u 的无衰减 corridor；generic rows 仍用 r_u a_u。最终稿明确区分两种合同，不把 k=1 加强式外推至所有非网格行。

# 3. Inclusion capacity cut 与完整 original jobs

q 为四倍数、m≥100q；机器 U_S、B_W、Z_R 分别对应 q-subsets、2q-subsets、q-subsets。U selector、d1 个 f home 1/d1、B_W 上 unit alternatives，B_W 有 d2 个 e home 1/d2、Z_R 上 unit alternatives，全部 jobs/finite entries 显式列出。

对 positive U selector A，H_S={R:|R∩S|≥q/4}，H=|H_S|，M 为每个 W⊃S 在 H_S 外的 q-subsets 数。条件 flow 给

`δd1(δd2−M)≤H`。

严格反向时所有 selectors first mass=0，与 one-hot 冲突，因此 raw SH3 必 infeasible；实际 T schedule 也必须执行同一数量的 f/e exports 到 distinct B/terminal slots。CONFIG(1) 有完整显式 witness，实际 path assignment 的上界为 max(1,2−1/d1,2−1/d2)，但不声称有限 q 下精确 OPT。

二项式 estimates、floor payment、fixed powers s1≤q^a、s2≤q^b 和 m≥100q 支付最终 strict FAIL，且所有算术/输入规模有 polynomial bit bound。该 family 的 raw SH3 failure 与 CONFIG optimum one 是 distinct conclusions；不能把它直接写成 raw SH3 integrality gap without specifying relaxation semantics。

# 4. Source-hardness 与软件边界

虽然来源由 true-hardness 角色读取，实际安全结论仍是：这套 raw SH3 flow/inclusion system 可作为必要 LP、端点删减和 sound FAIL 接口，且可在明确 rational input 上生成。它没有提供：

- 从 arbitrary source 到该 raw SH3 family 的完整 Karp/PCP reduction；
- 从 canonical subtree flow 到 shared integer ownership/actual forest 的 decoder；
- 一般 UM 的固定小于二近似或 hardness；
- exact SDP finder、软件重放或 finite audit 的本轮认证。

最终稿的 primary/PDF/software 说明在来源中被引用，但本轮没有把对应代码、JSON 或 PDF 当作独立证据。原文明确保留 growing-depth shared-owner 问题为开放义务。

# 本轮实际处置

三源均完整实读，比较 final hash 修订、作者 read-after、general first-flow、M3 zero-column 迭代、real quota、integer-grid CFG、inclusion capacity cut、完整 original jobs 和 source-hardness boundary。没有运行软件；原件和 manifest 在 evidence，正文归档为资料，回执草稿单列，暂不 checkpoint/done。
