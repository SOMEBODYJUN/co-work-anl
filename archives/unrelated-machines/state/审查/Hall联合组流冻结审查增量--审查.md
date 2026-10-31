---
id: unrelated-machines/hall-group-joint-flow-frozen-review-increment
kind: review
type_tag: 审查
title: Hall 联合组流冻结审查增量
status: complete-source-read-integrated
summary: "冻结 Hall 联合流 review 的版本增量：保留共同资格、同组同体积、q-Hall 槽流与未知 OPT promise 的严格量词，并绑定有限审计的真实边界。"
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/reviews/unrelated_machines/hall_group_joint_flow_review.md
  - source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/reviews/unrelated_machines/hall_group_joint_flow_review.md
source_ids:
  - 389c9eda10e6ce9f39a4
related_objects:
  - archives/unrelated-machines/state/审查/Hall联合组流与共享汇点宏分配双源审查--审查.md
  - archives/unrelated-machines/state/审查/Hall联合流与前缀匹配增量审计--审查.md
review_source_sha256: 7ddf4f1b7c4bfcd5003178e30723709bd00d4a00c11d5d9a999903f2544e96b8
---

# 阅读范围与版本身份

冻结源 `389c9eda10e6ce9f39a4` 是 `research/reviews/unrelated_machines/hall_group_joint_flow_review.md` 的内部盲重构与攻击记录，两个冻结提交 `68fad804ec5946cb296f77dc5b336308a66abf12`（legacy-cleanup）和 `aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c`（main）给出同一 SHA-256 `7ddf4f1b7c4bfcd5003178e30723709bd00d4a00c11d5d9a999903f2544e96b8`。本页实际回读该 review、Hall canonical 正文、规范阈值流、独立原矩阵 DFS、OPT-promise 独立核及九个 fixture/证书；它不是外部同行评审、新颖性证明或一般 `UM-TARGET-v1` 结果。

# 承重命题和量词

`UM-HALL-GROUP-JOINT-FLOW-v1` 的输入显式给出 homes `H`、接收机器 `Z`、宏任务和私有组 `J_h`。同一组任务只在 `{h}∪E_h` 可用且组内端点时间相同 `w_j`；宏边严格大于 `T/2`；整数 `q≥2`、`delta≥0`、`q*delta<2`，且
\[
(1/2+1/q)T\le W_h=\sum_{j\in J_h}w_j\le T,
\qquad w_j\le\delta T.
\]
若真实 `OPT≤T`，宏边的严格阈值使每个 home 至多接一件宏；撤离量满足 `e_h>T/q`，把每个 sink 复制 `q` 个槽后得到 Hall 条件。一次联合整数流同时选择宏 home、home 组和共同 sink；成功时
\[
C_{max}\le rT,
\qquad r=\frac{q(2+\delta)}{q+1}<2.
\]
`q` 按容量存储，不能把二进制 `q` 静默展开成输入长度线性副本。共同资格、同组同体积和 `W_h` 下界任一删除都会破坏 Hall 计数或前缀收费。

`UM-HALL-GROUP-PROMISE-APPROX-v1` 不输入 `T`，只在真实 `OPT` 尺度上承诺同一宏边、组负载、单件上界和共同资格结构。算法扫描实际宏瓶颈并调用阈值流，得到 `r*OPT`；该 promise 不是任意输入的可验证前提，不能把样本成功率改写成全输入近似算法。

# 证据、有限边界和相邻对象

冻结 review 绑定了规范 Hall 审计（4448/10122 等有限参数域）、独立 DFS（8123 例）和 exact-OPT promise（301 个样本）以及九个 fixture/证书。它们全用整数/Fraction；有限 `PASS` 只说明保存域内运行完成。审查保留非 matroid 可行家族 `∅,{0},{1},{2},{1,2}`，说明不能直接套用拟阵交换；也保留无资格、空组、零值、过多宏和 `q*delta` 退化分支。`Hall联合流与前缀匹配增量审计--审查.md` 承接 JSON/独立实现的逐字段计数，本页承接 review 源的量词、证明身份与版本 SHA。

与 shared-sink 宏匹配、价格覆盖、联合槽舍入和 3DM 证书的关系都是条件接口或障碍对照，不能把单一共同资格图和同体积假设推广到多汇点、异端点时间或一般 unrelated-machines；`UM-TARGET-v1` 及六人 SPE 目标保持开放。

# 处置结论

该 review 源的数学主张已整合到既有 Hall 联合组流审查，并以本页保留其独有版本身份、内部复核顺序、有限 evidence 边界和失败机制。处置为 `integrated`，不新造一般 Hall 定理，也不把有限审计当全称证明。
