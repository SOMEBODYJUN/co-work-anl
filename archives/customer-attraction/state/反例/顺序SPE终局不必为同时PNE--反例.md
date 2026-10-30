---
id: "customer-attraction/sequential-spe-outcome-not-simultaneous-pne"
kind: "counterexample"
type_tag: "反例"
title: "顺序SPE终局不必是固定其他行动的同时PNE"
status: "complete"
truth_status: "exact-counterexample"
review_level: "full-tree-and-independent-replay"
legacy_ids:
  - "CA-SPE-NON-PNE"
summary: "三客户三主题完整SPE的路径(C,A,C)中，中间人静态偏离B获4/3，但真实顺序续局只获5/6。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/current/customer_attraction/continuation_lemmas.md#CA-SPE-NON-PNE"
---

# 顺序SPE终局不必是固定其他行动的同时PNE

采用[完整历史共同目录模型](../定义/共同目录完整历史模型--定义.md)，三名提供者、三个单位客户，目录 $A=\{a\},B=\{a,b\},C=\{b,c\}$。第一人选C；第二人在前缀A、B、C后分别选C、B、A。第三人的完整策略为：

| 历史 | AA | AB | AC | BA | BB | BC | CA | CB | CC |
|---|---|---|---|---|---|---|---|---|---|
| 回复 | C | C | B | C | C | C | C | B | B |

各末位回复均为最佳反应。第二人在A、B、C后的最大真实续局收益分别为 $3/2,5/6,1$，指定行动分别达到这些值。根节点的三个续局收益为 $1/2,5/6,1$，所以C是严格最佳选择。全部13个节点均已指定并检查，这是完整纯SPE。

在轨终局 $(C,A,C)$ 的收益是 $(1,1,1)$，福利3，最优覆盖也为3。若同时行动且把另外两人的选择固定为C、C，中间人从A改为B可得 $1+1/3=4/3>1$，故该终局不是同时PNE。

顺序博弈中的真实偏离历史是CB，末玩家随后选B。中间人的收益变为 $1/2+1/3=5/6$，小于原来的1。因此SPE最优性没有给出冻结后人行动的静态PNE不等式；不能先筛选同时PNE再声称得到了全部SPE终局。

[独立单位客户重放](../../tools/evidence/continuation-bridges/replay.json)检查13个节点、26个备选行动；[规范solver回归](../计算/完整历史求解器的精确复现--计算.md)也为指定路径重构并核验完整证书。两者分别是给定证书定义级重放和算法接口检验，没有据此认证一般福利猜想。

源文献页还记录两人四客户的另一非PNE例；本三人三客户例是独立具体证书，否定同一桥梁而非另一数学主张。与[历史平局反例](同负载历史的不同续局--反例.md)的用途不同：这里的关键是偏离后行动响应，不是单独的同计数破平局现象。
