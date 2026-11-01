---
id: customer-attraction/r3b6b-finite-residual-cycle-cone-search
kind: computation
type_tag: 计算
title: R-3b6b 有限残余循环策略锥搜索记录
status: finite-floating-candidates-preserved
truth_status: no-certified-half-counterexample; no-universal-security-proof
review_level: full-source-read-and-output-scope-audit
scope: five-player/seven-topic and six-player/eight-topic finite LP searches over residual-cycle strategy cones
summary: Four frozen JSON searches record floating candidates with ratios 1.8 or 11/6, but every record is explicitly uncertified and lacks exact full-history SPE verification. The accompanying CCE and last-player scripts are retained as finite attack programs; the existing R-3b6b exact m5k7 certificate remains a separate complete SPE point above half.
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-3b6b03db882e4de48cfa5b406f57ef8f/boss/cce_bridge_search.py
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-3b6b03db882e4de48cfa5b406f57ef8f/counterexample/last_share_search.py
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-3b6b03db882e4de48cfa5b406f57ef8f/counterexample/search_m5k7.json
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-3b6b03db882e4de48cfa5b406f57ef8f/counterexample/search_m5k7_maximal.json
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-3b6b03db882e4de48cfa5b406f57ef8f/counterexample/search_m5k7_secondary.json
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-3b6b03db882e4de48cfa5b406f57ef8f/counterexample/search_m6k8.json
---

# R-3b6b 有限残余循环策略锥搜索记录

## 搜索目标与证据等级

本批延续 A/B/T/D/E 残余循环路线，尝试在固定完整策略锥中放大最后玩家份额或构造 CCE 桥，从而逼近 \(\operatorname{OPT}>2W\)。四个 JSON 都明确写有 `floating candidate, not certified`；它们保存 LP 浮点支持、有限策略状态和搜索记录，没有有理化客户克隆、完整有序历史 IC 证书或精确对偶。因此它们是有限候选记录，不能作为反例、定理或全局安全结论。

## 四个冻结输出

| 源 | 规模与种子 | 最佳记录 | 约束规模 |
|---|---|---|---:|
|`search_m5k7.json`|5人、7主题、seed 41236|ratio 1.8，target `[5,0,0,0,0,0,0]`|1260 rows / 330 states|
|`search_m5k7_maximal.json`|5人、7主题、seed 32873|ratio 1.8，step 1，incoming 1.8|1260 rows / 330 states|
|`search_m5k7_secondary.json`|5人、7主题、seed 88321|ratio 1.8，target `[4,0,0,1,0,0,0]`|1266 rows / 330 states|
|`search_m6k8.json`|6人、8主题、seed 41236|ratio \(11/6\approx1.8333\)，target `[6,0,0,0,0,0,0,0]`|5544 rows / 1287 states|

记录的 `ratio` 是锥内最后份额或目标函数比值，不能读作 \(\operatorname{OPT}/W\)。JSON 同时保留大量 `choices` 和浮点 weights；没有声明这些权重对应合法单位客户整数实例。

## 两个程序的实际作用

`cce_bridge_search.py` 对随机整数客户实例求最小 CCE 福利 LP，并在发现 LP 值高于规范 SPE 最小福利时，才尝试生成 exact SPE 证书和输出；它本身只保留“需要精确 dual”的数值状态，未给本批报告。有限试验批次覆盖 \((m,k)=(2,3),(3,4),(4,5),(5,7)\) 的若干随机次数，没有全域穷举。

`last_share_search.py` 在五人七主题默认规模上，对12个起点、6步锥迭代优化最后玩家份额；每步输出 incoming share、优化后的 last share、ratio、target、rows 和状态数。它允许随机浮点权重及 residual/root-tax seed，未调用 Fraction 整数恢复。

## 与已整理对象的关系

[R-3b6b 辅助锚点提升与 m5k7 有限证书边界](../障碍/R-3b6b辅助锚点提升与m5k7有限证书边界--障碍.md)保存同一研究族的2801历史完整SPE点（\(W=1000,\operatorname{OPT}=1800\)，比值 \(9/5\)）以及候选恢复边界。本批四个JSON与该对象不同：它们是未认证浮点锥候选，不能替代已认证点，也不能因ratio接近2而声称half失败。

[R-3b942共享遗漏回复循环的完整策略锥攻击](R-3b942共享遗漏循环完整锥攻击--计算.md)已对另一五人七标签种子完成四个有理化端点（\(W=5,\operatorname{OPT}=8\)或7），并逐历史核验；当前对象的浮点候选没有相应的精确克隆与核验，二者保持证据等级分离。

## 接续要求

若继续此路线，应先固定每个候选的有限策略、把LP支持有理化为非负整数客户重数，再用完整有序历史 `verify_certificate` 检查所有单步偏离，最后重新计算真实 \(W\) 和 \(\operatorname{OPT}\)。只有这些步骤都通过且 \(\operatorname{OPT}>2W\) 时，才可创建反例正文；否则保留计算/候选身份。当前输出没有关闭六人 Q-CAG-HALF，也没有提供一般 CCE 到 SPE 的桥。
