---
id: "unrelated-machines/optimal-convex-slot-input-semantic-review"
kind: "review"
type_tag: "审查"
title: "三机真实最优凸包固定槽输入夹具语义清洗"
status: "ready-for-integration"
truth_status: "input-fixture-with-finite-audit-boundary"
review_level: "full-source-read-and-cross-archive-comparison"
scope: "identical-machines; m=3; one unit job and eight small jobs; input only"
source_sha256: "f3899476eb7dcb1b0475c54981f6b49e226c49344315a7933b725836f195ab20"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:examples/unrelated_machines/optimal_convex_slot_input.json"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:examples/unrelated_machines/optimal_convex_slot_input.json"
---

# 来源身份与实际内容

冻结源 `ad3aa0a720cfb4d680e4` 是一个 600 字节 JSON 输入夹具，SHA-256 为
`f3899476eb7dcb1b0475c54981f6b49e226c49344315a7933b725836f195ab20`。它在
`legacy-cleanup` 与 `main` 两个冻结提交中内容相同。字段给出 `m=3` 台相同机器、
`n=9` 个任务、一个处理时间为 1 的大任务和八个处理时间为 1/4 的小任务；三行
`P` 完全相同，`unavailable_marker` 为 null，参数只重复记录 `m=3`。

该 JSON 不包含调度动作、凸组合系数、槽匹配、修复路径或审计结果，不能单独证明
任何调度结论。它只是既有固定槽对象的输入身份，客户/调度语义必须与同批冻结证书
和审计程序一起解释。

# 与既有固定槽对象的对应

全仓已有的《固定槽跨槽修复与最小工作面支撑障碍有限审查》以及
`slot-repair-20261030` 证据包已经用该输入核对两条主张：

* `UM-OPTIMAL-CONVEX-ST-SLOT-GAP-v1`：一般参数族的固定标准槽图会强制坏匹配；
  对本输入的 m=3 实例，主审计与独立槽审计均保留完整槽支持和有限枚举范围。
* `UM-OPTIMAL-CONVEX-SLOT-REPAIR-v1`：跨槽同步修复的单目的地约束、Hamming 距离
  阈值和逐批负载下降；修复审计使用有理/整数算术，不能读成一般算法保证。

既有正文明确区分真实最优凸包成员、固定槽图输出和最小工作面整面。允许直接
选择一个显式最优分量、重选凸组合、改变槽图或增加少量工作量时，固定槽输入的
障碍不再自动适用。

# 处置决定与边界

本源应 `integrated` 到既有固定槽审查和 `slot-repair-20261030/source-manifest.json`，
不新建重复数学对象。独有内容是可复现的三机九任务输入夹具及其源版本/哈希身份；
既有审计已经承载所有数学结论和有限证据。不得把输入 JSON 单独升级为一般
unrelated-machines 近似困难性、NP-hardness、全球 `<2` 算法结论或当前六人
customer-attraction half 结论。

复现入口仍是既有证据包列出的三个审计程序；本批没有修改程序或重新声称外部评审。
