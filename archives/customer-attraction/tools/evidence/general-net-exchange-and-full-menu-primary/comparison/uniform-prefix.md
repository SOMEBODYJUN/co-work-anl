---
id: "customer-attraction/uniform-actual-prefix-portfolio-interface"
kind: "conjecture"
type_tag: "候选"
title: "真实前缀均匀组合接口"
status: "open"
truth_status: "unproved-candidate-with-finite-negative-searches"
review_level: "full-source-read-exact-finite-replays-and-floating-cone-boundary"
scope: "有限单位客户、有限非空共同目录、完整有序历史纯SPE；m个比较主题允许重复；不声称六人结论"
summary: "候选不等式 m|∪T_j|≤(m−1)W+Σ_{i,j}V_{ij} 若普遍成立即给 OPT_m≤(2−1/m)W；17个精确完整策略样本、70个四人策略锥和一个五人锥未发现负余量，但没有一般证明。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-acd97406d8c4409d962eab2adcdc520c/resume_uniform/README.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-acd97406d8c4409d962eab2adcdc520c/resume_uniform/probe.py"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-acd97406d8c4409d962eab2adcdc520c/resume_uniform/existing_results.json"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-acd97406d8c4409d962eab2adcdc520c/resume_uniform/cone_probe.py"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-acd97406d8c4409d962eab2adcdc520c/resume_uniform/cone_results.json"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-acd97406d8c4409d962eab2adcdc520c/resume_uniform/m5p7_cone_result.json"
---

# 真实前缀均匀组合接口

## 候选命题

固定一份有限共同目录完整有序历史纯SPE。令 (W) 为实际根终局覆盖客户数。给定 (m) 个比较主题 (T_1,ldots,T_m)（允许重复），令 (C=\bigcup_jT_j)。对每一位玩家 (i) 和每个 (T_j)，令 (V_{ij}) 为该玩家在其**实际前缀**改选 (T_j)，然后沿同一完整策略在改变后的历史继续所得到的真实最终收益。候选接口是

\[
\boxed{m|C|\le (m-1)W+\sum_{i=1}^m\sum_{j=1}^mV_{ij}.}
\tag{UP\(_\mathrm{actual}\)}
\]

它量化的是完整真实偏离，不能冻结实际末位回复或把不同有序历史的计数策略拼接。若对每份完整SPE和每个比较元组成立，则对达到 (operatorname{OPT}_m) 的元组使用 SPE 的实际行动最优性 (V_{ij}\le u_i)，得到

\[
m\operatorname{OPT}_m\le (m-1)W+m\sum_i u_i=(2m-1)W,
\qquad
\operatorname{OPT}_m\le(2-1/m)W.
\]

这个推论比 half 略强，但候选本身尚未证明。尤其不能把有限探针的非负余量写成一般六人结论。

## 现有精确有限证据

`existing_results.json` 对17个可读取完整策略/证书样本，以 `Fraction` 枚举每个非空主题支持并对重复位置填入该支持中真实偏离和最小的主题，精确最小化给定支持的余量。各样本均无负余量；余量为零的样本包括 `tax_bridge_failure.json`，因此“未发现负值”不意味着严格裕度。其余代表性最小余量为：

* `aggregate_theta_failure`：(166/3)；
* `coverage_opportunity_failure`：(17/3)；
* `dynamic_iid_local`：(545/3)；
* `five_individual_security`：(1551/5)；
* `root_tax_failure`：(33/2)；
* `worst_pne_welfare_failure`：(137/6)。

这17项是仓库中可读取且有证书的有限样本，不是对所有实例的搜索。

## 固定策略锥探针

`cone_probe.py` 在完整四人五主题策略锥上，对全部非空客户类型和每个 (m)-元重复比较多重集做浮点LP；`cone_results.json` 报告70棵锥、每棵70个比较，共4900次尝试，所有 `failure=false`。`minimum_float_gap` 全为 `0.0` 是程序以零作初始下界且未找到负候选，不能解释为严格正证书，也没有恢复完整有理对偶。`m5p7_cone_result.json` 对一棵五人七主题锥枚举462个多重集，同样 `failure=false`。

README明确把这些结果限定为“旧冻结样本/一棵策略锥的有限发现过程”，即使恢复有理顶点也要逐历史核验后才能成为反例；当前没有任何严格负有理点。

## 与既有对象的边界

该候选与“均匀组合背景归纳不能丢弃尾部余量”不同：后者反驳的是把尾部非负余量直接当作局部归纳付款；这里是根处对全部真实前缀偏离的组合式。它也不同于已经否定的固定均匀分数背景或一一匹配收费接口。有限样本通过不代表任意静态安全值桥，更不等于六人 Q-CAG-HALF-6 已证。

后续若出现负浮点候选，必须恢复有理客户重数、完整目录和全部有序历史SPE比较；若只得到锥内负点而没有完整策略，最多是固定锥证据，不能当原模型反例。当前此候选仍是开放的真实前缀跨分支支付接口。
