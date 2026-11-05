---
id: unrelated-machines/single-home-cascade-original-program-review
kind: computation
type_tag: 计算
title: "单home级联的十四任务八模式证书"
status: "exact-finite-certificate-with-explicit-scope"
summary: "固定14机14任务实例的完整查询子集证书，含共home、unit迁移和不采用的无根费用环。"
fixture_source_sha256: cfb25856400d6d0ee6b6cea9cb100d8545c97fe2025643f8a62260763fc69573
source_ids:
  - 978ef2be866136ae323d
  - ba9c71e2bc6052c4f3c0
  - a6f3780bd6fb78eeece6
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:tests/audits/unrelated_machines/single_home_cascade_query_separation.py
  - source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:tests/audits/unrelated_machines/single_home_cascade_query_separation.py
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/reviews/unrelated_machines/single_home_cascade_query_separation_review.md
  - source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/reviews/unrelated_machines/single_home_cascade_query_separation_review.md
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:examples/unrelated_machines/home_cascade_query_patterns.json
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:evidence/runs/unrelated_machines/single_home_cascade_query_patterns_v2.json
---

# 十四任务的完整查询族证书

[单home级联定理](../定理/单home级联的完整查询族与可加费用--定理.md)对两份strict1调度、强home及唯一正小端证明：可预先构造两两不交的非query支持A_q，对每个显式S⊆Q恢复完整原分配，峰不超过1+δ(S)，费用恰为Σ_(q∈S)c_q。以下是一个完整有限实例，检验同一组支持同时适用于全部八个S。

机器和任务各14个，U={U}，Z={z}。q1在H1的小时间1/8；q2、q3共home H2，小时间分别1/8、1/16。每个输出都把z从A的1/5端送到其原零端Z0。非query支持为

\[
A_{q_1}=\{f_1,f_2,f_3,f_5,f_6\},\quad
A_{q_2}=\{f_4\},\quad A_{q_3}=\{g\},
\]

费用(c_q1,c_q2,c_q3)=(34,7,17)。无根环r0,r1的费用19+23=42不被采用，全query构造费58，而给定第二strict输入的非query unit费100。f5的增广路经W0上原U的迁移到W1，再触发f6，因而包含实际unit路径压缩。

| S | 实际峰 | δ(S) | 实际非query费 |
| --- | ---: | ---: | ---: |
| 空 | 1 | 3/16 | 0 |
| q1 | 19/16 | 3/16 | 34 |
| q2 | 9/8 | 1/8 | 7 |
| q3 | 1 | 1/8 | 17 |
| q1,q2 | 17/16 | 1/16 | 41 |
| q1,q3 | 9/8 | 1/8 | 51 |
| q2,q3 | 9/8 | 1/8 | 24 |
| 全部 | 1 | 0 | 58 |

[完整输入、八份输出及构造器](../../tools/evidence/single-home-cascade-originals/README.md)保留每件原任务的实际端、逐机负载、增广路和支持；[证书回算](../../tools/evidence/single-home-cascade-originals/frozen-record-verification.json)逐份从原矩阵核完整分配。构造器只处理请求的显式子集，不自动生成2^|Q|模式；此三query输入恰显式列全八个。一般输入与位复杂度由定理证明，有限实例不声称逐模式最优费用可加。
