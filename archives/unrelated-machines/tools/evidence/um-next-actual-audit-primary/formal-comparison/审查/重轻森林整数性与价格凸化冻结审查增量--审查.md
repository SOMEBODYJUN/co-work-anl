---
id: unrelated-machines/heavy-light-forest-integrality-price-convexification-frozen-review-increment
kind: review
type_tag: 审查
title: 重轻森林整数性与价格凸化冻结审查增量
status: complete-source-read-integrated
truth_status: "incremental reread confirms the exact forest counterfamily and the scoped price-convexification interface"
summary: "本增量实际重读两份冻结 review 源，记录其相对既有双源正文的版本校正、证据绑定和严格适用范围；不把审查稿升级为一般调度定理。"
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/reviews/unrelated_machines/heavy_light_forest_integrality_boundary.md
  - source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/reviews/unrelated_machines/heavy_light_forest_integrality_boundary.md
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/reviews/unrelated_machines/heavy_light_price_convexification.md
  - source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/reviews/unrelated_machines/heavy_light_price_convexification.md
source_ids:
  - b7724da00b7bc1ee746e
  - ad117632752525a91aa0
related_objects:
  - archives/unrelated-machines/state/审查/重轻森林整数性与价格凸化双源审查--审查.md
  - archives/unrelated-machines/state/障碍/逐价格重匹配与共同残余的量词缺口--障碍.md
evidence:
  - archives/unrelated-machines/tools/evidence/frozen-macro-tiny-20261030/source/frozen_macro_tiny_audit.json
  - archives/unrelated-machines/tools/evidence/heavy-matching-20261030/source/heavy_light_price_convexification_release_audit.json
---

# 阅读与版本关系

本页是对两个已归档重轻对象的冻结审查稿增量，不新造一个调度模型。实际读取的两个源分别是 `UM-HEAVY-LIGHT-FOREST-INTEGRALITY-BARRIER-v1` 的 review 版本和 `UM-HEAVY-LIGHT-PRICE-CONVEXIFICATION-v1` 的 review 版本；两源均来自 `legacy-cleanup` 与 `main` 冻结提交。它们与[重轻森林整数性与价格凸化双源审查](重轻森林整数性与价格凸化双源审查--审查.md)所引用的原始正文相同主题，但此次源版本的独有价值是版本校正、独立复核范围和证据哈希的明确绑定。

# 森林整数性边界的核对

第一源的参数族仍是：中心任务在每台机器耗时 \(\beta T\)，每台机器有唯一私有任务耗时
\(aT=(1-\beta/m)T\)，中心边在残余图中形成星（私有叶可使其成为带叶树）。当中心任务以
\(1/m\) 分数分配时每台负载恰为 \(T\)，均匀价格给出同一残余对偶值，因此确有 pure saddle；
整数放置中心任务到一台机器后，该机负载为
\[
  aT+\beta T=(1+\beta-\beta/m)T,
\]
可随 \(m\to\infty\)、\(\beta\to1\) 趋近 \(2T\)。森林、纯 saddle 和 \(R(H)\le T\) 不能推出整数补全；已有反馈边/叶消元合同在这族上应返回 `FAIL`，这与“LP 已经是整数”的断言是两件事。

冻结审查特别校正最小例的缩放：在未缩放参数 \(m=2,\beta=2/3,T=1\) 时，所有相关边耗时为 \(2/3\)，等比例乘以 3 后才得到三项耗时 \(2\)、阈值 \(T=3\) 的两机三任务实例。此前曾写成乘以 \(9/2\) 的内部草稿不属于冻结结论；本页和既有正式审查均采用乘 3 的精确算术。该校正不改变趋二参数族，也不把例子升级为一般 hardness。

# 价格凸化接口的核对

第二源固定
\[
 E_T=\{(i,j):p_{ij}\le T\},\qquad
 B=\{p_{ij}>\beta T\}\cap E_T,
\]
再在任务到 big/light 机器的网络流多面体上允许不同的 big placement 混合。网络流顶点整性给出凸包，但它忘掉了一个共同的整数 \(H\)；因此
\[
 \exists H\ \forall\lambda\quad G(H,\lambda)\le0
\]
与
\[
 \forall\lambda\ \exists H\quad G(H,\lambda)\le0
\]
不得互换。固定 \(H\) 的 Farkas 证书、剪枝后的 ST 上界 \(2T\)、未剪枝固定机器数的 \(mT\) 界，以及所有最优价格流共享同一 big 向量时的共同面出口，均保持原有精确范围。

源版本列出的三项 nonfatal 修补是实质可复用的审查记录：小的非最优价格扰动不能替代最优面检查；空/全零配置不能强取正 anchor；实现必须显式恢复 fractional-light 共同面、检查强制 big 反值，并保留 `Q` 非空但容量失败的例子。当前冻结对象与 `heavy_light_price_convexification_release_audit.json` 的 Fraction 结果相符，包含空任务、零边、混合角色、容量冲突、重边冲突和剪枝丢任务分支。审查仍是有限 oracle 与给定见证下的位多项式接口，未集成一般 LP/费用流求解器，也未认证外部新颖性。

# 关系、处置和接续

两份冻结 review 源的数学内容已由既有双源对象承载，本增量保留的独有信息是最小例缩放更正、release audit 的代码/基线哈希以及 nonfatal 修补清单。因此它与既有双源审查是“版本审查增量”关系，而不是新的独立定理；不应把当前页的 `complete-source-read-integrated` 解释为 `UM-TARGET-v1` 已解决。

可继续的工作是：寻找跨机器共同容量证书，或证明精确最优价格面强制同一 big placement；仅增强逐价格 oracle、anchor 或局部森林测试不能消除凸化造成的相关性。当前六人 Q-CAG-HALF 目标与一般 unrelated-machines 目标均未由本页解决。
