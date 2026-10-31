---
id: "unrelated-machines/seven-state-and-gate-localizer-exact-first-20261031"
kind: "review"
type_tag: "审查"
title: "七态 AND endpoint 二次 localizer Exact-first 独立重构"
status: "integrated-narrow-obstruction"
truth_status: "exact-first-scope-reconstruction-consistent-with-later-author-read-after"
review_level: "full-source-read-independent-exact-first"
summary: "完整阅读 Exact-first 独立重构：它在明确的 base≤6、共同 M3、faithful AND endpoint 与原 v-load 合同下，逐步得到 D=Z−CY_i 的 degree-2 null、degree-3 支付和负 localizer -p(1−eta)(d−h)^2。它只排除这一窄接口族，不把作者 Proof、普通 eligibility、一般非线性或一般 UM 结论混入。"
source_refs:
  - "source:87da487058597a428c41:history/source/notes/unrelated_machines/sol_seven_state_and_gate_localizer_obstruction_exact_first_review.md"
legacy_ids:
  - "UM-SEVEN-STATE-AND-LOCALIZER-EXACT-FIRST-v1"
related_objects:
  - "unrelated-machines/seven-state-and-gate-localizer-author-read-after-20261031"
  - "unrelated-machines/seven-state-star-global-quadratic-exact-v1-review"
---

# 1. 来源身份与独立性边界

`clean show` 导出的来源 `87da487058597a428c41` 为
`history/source/notes/unrelated_machines/sol_seven_state_and_gate_localizer_obstruction_exact_first_review.md`，3,801 bytes，SHA-256 `a492c7a07259e2d2b55d46de257bac4687618f88e420f4567d98652fc080ed2e`。本页逐行读取并保留原文于
`archives/unrelated-machines/tools/evidence/seven-state-gate-localizer-exact-first-20261031/original/`。

该来源只读新候选 Exact `sol_seven_state_and_gate_localizer_obstruction_exact_v1.md`（3,070 bytes，SHA-256 `8ca3b942276658319808f3c32d5057b53611555d76bfbf6f4c5f94ea18e511ab`），未读作者新 AND Proof 或策略。它承认七态基础与 affine 分类已知，因此独立性只针对该 Exact 的共同矩、degree 合同与负 localizer 推导，不冒称从整个问题背景盲起。后续 `7ccd86160f25544a1e74` 作者 read-after 已单独归档；两者保留各自时序和证据身份。

# 2. 量词、参数与真实新增端点

正偶 `d,s` 满足 `2≤s≤d/2`，令 `eta=s/d`、`h=s/2`、`p=eta^3/1000`，并沿用七态 law 的 `u0,e`。全部七类质量严格为正，`1≤h≤d/4`。新增 `Z` 是一个真实 degree-one Boolean endpoint，faithful 关系为

\[
Z=C Y_i,
\]

所以 `CY_i` 是 degree 2；指定 localizer 中 `q=Z(H-h)` 的总次数是 2，`g=T-C-H/d` 为 degree 1，`gq²` 总次数为 5。该次数计数属于 base≤6 的明确合同，不能把现有 affine lemma 的 base≤4 偷换进来。

# 3. Null 提升、Boolean 支付与精确负值

令 `D=Z-CY_i`。假设共同 M3 中 `Lhat(D²)=0`，PSD 给出 `Lhat(D r)=0` 对任意次数≤3 的 `r`。取

\[
B=g(H-h)^2,
\]

则 `deg B≤3`。以 `B` 乘新增 `Z²=Z` 的 Boolean 等式（总次数≤5），再用 `D` 对 `B` 的正交性，得到

\[
\widehat L[gZ^2(H-h)^2]=\widehat L[gZ(H-h)^2]
=\widehat L[gCY_i(H-h)^2].
\]

右边只含 `C,Y` 且次数≤5，故 Exact 的 base≤5 匹配把它换成真实七态 `P` 期望。七类中 `C=0` 的项被 `C` 消掉；`C=1,H=0` 因 `Y_i=0` 消掉；`C=1,H=h` 因 `(H-h)^2=0` 消掉；只剩 `C=1,H=d`，给出

\[
\widehat L[gq^2]=-p(1-\eta)(d-h)^2<0.
\]

该式是精确有理值，最小 `d=4,s=2,h=1` 仍成立；不依赖渐近、平均索引或数值 SDP。它说明指定窄接口的二次 localizer 不可能保持。

# 4. 普通 UM 语义与范围限制

Exact-first 同时检查普通 job 语义：新增一枚 unit job `K`，两个新且不同的 private endpoints 取 `Z=CY_i` 与 `1-Z`，逐样本完整执行；新增 private rows 负载至多 1，不改变原 v load。于是候选 law 仍是真实共同 assignment law、任意阶 `M_k` PSD、Boolean/one-hot 完整，但指定原 v localizer 仍为负。

这不是把普通 eligibility 逻辑偷偷增强成 AND：`Z=CY_i` 是作者候选显式提供的 faithful endpoint 关系。若 `Z` 不是新增 degree-one endpoint、只给一阶边际、改变 base 第五次矩、改变原 v load 或改用别的 extraction，以上推导都不能直接套用。非仿射、近似 AND、深层 shared-owner/common-law 和跨背景路由仍须另证。

# 5. 与后续作者 read-after 和全局对象的关系

后续作者 read-after (`7ccd86160f25544a1e74`) 逐式复核了同一 `D`、`B` 和负值，并补充“普通 eligibility 未强制 AND”的范围说明；本页作为先行独立重构保留其未读作者 Proof 的时序。七态 GlobalQuadratic Exact/Coercivity 学习对象研究真实 law、全局 quadratic localizers 与逐行 CONFIG；当前 Exact-first 只否定 faithful AND 加 base≤5 额外合同同时保留原 v localizer，不能与其合并成所有延拓均失败。

本页没有软件运行、没有一般 SDP finder、没有 source decoder、没有 actual near-two gap 或 hardness。第三阶段若建立关系，应连接为“Exact-first窄障碍 → 作者 read-after复核”，并显式保留 base≤6、faithful AND、原 v load 和新增真实 endpoints 四项前件。
