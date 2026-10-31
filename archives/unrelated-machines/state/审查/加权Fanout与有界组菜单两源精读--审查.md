---
id: "unrelated-machines/weighted-fanout-and-bounded-group-menu-two-source-review"
kind: "review"
type_tag: "审查"
title: "加权 Fanout 与有界组菜单两源精读"
status: "typed-weighted-interface-read"
summary: "两份 review 确认 weighted fanout/profile 的两真实 YES、独立 0/T 预载和 missing-one 3/2 边界，以及 bounded-group weighted menu 的失败/成功双分支匹配合同。均只针对明确 typed interfaces、给定 witnesses/预载和原资源单射，不升级一般 UM hardness/近二。"
source_refs:
  - "clean:0e8c2a1c8ebff9e7900d"
  - "clean:daaed35825823c3c6802"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/reviews/unrelated_machines/weighted_fanout_profile_boundary_review.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/reviews/unrelated_machines/weighted_menu_bounded_group_interaction_rounding_review.md"
---

# 读域与对象

`0e8c2a1c8ebff9e7900d`（SHA `5023cd2ed88cecc7476eb3e4fca518598461d1fa7c572f38ff762ff29631fc9c`）审 weighted fanout profile、missing-one three-halves 与两真实 YES 预载接口；`daaed35825823c3c6802`（SHA `1b35c2da1b45b89241cbe56d6f46e91840a7733778f4f1412d019928950ec31d`）审 bounded-group weighted menu interaction v2 的失败/成功分支。两源均 clean show 全文实读，证据/manifest 在 `archives/unrelated-machines/tools/evidence/weighted-pair-20261031/`，receipt 草稿在 `cleanup/workspaces/Boss2/weighted-pair-receipts-20261031.json`。

# 1. Weighted fanout/profile boundary

对象固定基础不可拆 jobs、非负有理时间、显式两份实际 YES witnesses；状态只切换独立 host 的 0/T 预载。任意候选 K（`|K|≥2`）和有理 simplex β 输出完整实际 σ/chosen，其余输出 free，K 外按 internal 计费。加权闭包逐类冻结：同色权只增，未固定类只进入一次，末类由相减得到配额；β_i=0、L=0、自环均有明确处理。

S1 换目标预载得 μ≤2T；固定 a 预载得 μ≥T。若和式失败，构造 `D<1`、`β_i=d_i+(1−D)/k` 的合法有理 simplex，使每 β_i>d_i，形成严格改进反证；算法本身不调用未知 μ/OPT。T=0 直接 all-zero 处理，零权星与点质量均纳入锐例。满二叉树 profile 中 root=a，q 叶与 2q−1 nodes/2(q−1) edge jobs；missing leaf 返回 parent，得到完整三半 upper/lower。3-output missing-one 反例逐 profile 枚举给 OPT 5/4、7/4、1，说明 pair-sum≤3 不足以保证全部≤3/2。

规范/独立有限构造均保留全部 jobs、K 外机器、零值边界；有限 8118 weighted constructions/2706 local budgets/1263 missing pair 及独立枚举仅 audit。Claim 只限制给定两 YES 与 0/T preloads，不给一般 source reduction 或 UM-TARGET 解答。

# 2. Bounded-group weighted menu interaction

`UM-BOUNDED-GROUP-INTERACTION-WEIGHTED-MENU-v2` 的失败 branch：从任意 `C<1+β` 实际 σ 强制 heavy covering matching，故 `OPT≥1+β`；再用 all-private 2 得 relative≤R。成功 branch：每邻组删一格，损失 `Mβ`，保留完整变量并集 q，随后用共同完整 Δ-block matching 导出≥β。绝不能声称失败 branch 也有绝对 R，也不能把不完整菜单交互 M 当 q 界。

Exact 正式对象已加入 distinct resource set，旧越域例保留：单组单state两枚 private1/2 共用同resource1 时 actualOPT=3/2，不能沿用 Δ=1/M=0 的 OPT1 端点。canonical 读后仅修“原资源”含 bonus 的一句措辞；当前 v2 final SHA 与 read-after 记录相符。实现 none，审查者 18,018 排序有限核验仅辅助，不是全量证明。

# 3. 身份关系、实现与未解

两源共同展示给定 witnesses、预载和 local resource interaction 下的 weighted profile/rounding contracts，但量词不同：Fanout 的 chosen K/β 与 host state、bounded-group 的 failure/success matching、Δ/M/q 均是 typed interface。它们不构成一般 unrelated-machines near-two hardness，也不提供 source decoder/OPT oracle/production implementation。有限审计不能替代全称证明；外审、全球新颖性和独立论文价值未认证。

处置为 `typed-weighted-interface-read`。引用时需保留 independent 0/T preload、两真实 YES、distinct resource set、失败/成功双分支和 local finite evidence 边界。
