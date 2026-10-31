---
id: matroid-structures/exchange-distance-and-equal-theta-ledger-interfaces
kind: resource-review
type_tag: 审查
status: duplicate-of-existing-integrated-object
source_ids:
  - 337758284556a6ae802a
source_sha256: fc085fe0d3d52506259c027445ce034dd5a29f6d291bb152d364697184b069b4
source_size: 7385
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:history/retired_topic_selection/multi_lane/research/topic_selection/notes/combinatorial_equal_theta_correlation.md
  - source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:history/retired_topic_selection/multi_lane/research/topic_selection/notes/combinatorial_equal_theta_correlation.md
existing_targets:
  - archives/matroid-structures/state/资料/交换距离与等长theta相关间隙的独立接口--资料.md
  - tools/evidence/retired-topic-claims/related/history/retired_topic_selection/multi_lane/research/topic_selection/notes/combinatorial_equal_theta_correlation.md
---

# 实读与处置

`clean show 337758284556a6ae802a` 导出的冻结源为 7385 字节，SHA-256 为 `fc085fe0d3d52506259c027445ce034dd5a29f6d291bb152d364697184b069b4`；`legacy-cleanup` 与 `main` 两个冻结提交内容相同。全文是 `CS-THETA-EXACT-v1` 的等长多路 theta graphic-matroid correlation-gap 证明候选，给出对所有 `k,ℓ≥2` 的有限有理最小值公式、support-tight/coloops 约化、base-domain 质量参数化、路径内 AM–GM 和两坐标平方差凸性；同时记录新颖性、外部文献排重、等式 argmin 相图及不等长延伸仍未闭合。k=3 的旧 `637/729` 已在源内修正为 `3565/4096` 的非对称 `(1/2,1/2,0)` 点，不能把旧数值当结论。

全仓比较发现该源已经被完整纳入现有对象 `archives/matroid-structures/state/资料/交换距离与等长theta相关间隙的独立接口--资料.md`：对象 `legacy_ids` 含 `CS-THETA-EXACT-v1`，正文保留上述公式、证明路线、k=3 修正、有限 SLSQP/小规模检查和新颖性/应用缺口；原件已逐字保全于 `tools/evidence/retired-topic-claims/related/history/retired_topic_selection/multi_lane/research/topic_selection/notes/combinatorial_equal_theta_correlation.md`，其 SHA 与本次 clean show 完全一致。该对象同时区分另一份交换距离源，不把二者当作数学依赖。

因此本次来源没有新的独有数学内容需要另建对象；建议 `disposition=duplicate`（已由既有对象完整吸收），保留当前源 ID、双冻结 source_refs 和哈希回执。不要将证明候选升格为已证定理，不要将有限 SLSQP 或 k≤16 观测推广为全参数 argmin，也不要把外部文献关键词核查写成新颖性认证。若需精确 provenance，可在既有对象 frontmatter 增补本源两条 source_refs；这属于来源索引修补，不改变数学状态。
