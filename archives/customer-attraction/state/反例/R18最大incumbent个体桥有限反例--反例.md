---
id: customer-attraction/r18-largest-incumbent-individual-bridge-finite-counterexample
kind: counterexample
type_tag: 反例
title: R-18 最大incumbent候选的根激励误标
status: withdrawn-not-a-SPE-certificate
truth_status: invalid-as-individual-bridge-counterexample; five-profitable-root-deviations
review_level: later-primary-correction-plus-new-unit-definition-reconstruction
scope: 3 players/6 topics; complete formal policy with valid children but failing
  root IC
source_refs:
- clean:663827506601922a81a3:research/workspaces/customer-attraction/R-18e993ca519949aba29e030d3d7b15b3/global_proof/largest_incumbent_n3p6_best.json
- clean:e5885286333aa0d55f8d:research/workspaces/customer-attraction/R-18e993ca519949aba29e030d3d7b15b3/global_proof/largest_incumbent_n3p6_run.json
- local:archives/customer-attraction/state/计算/R18最大incumbent个体桥策略锥探针--计算.md
- local:archives/customer-attraction/state/反例/父方实际incumbent独立全历史审计报告--反例.md
- local:archives/customer-attraction/state/计算/父方实际incumbent完整历史独立审计--计算.md
- local:archives/customer-attraction/state/审查/最大incumbent候选的根激励遗漏与错误认证--审查.md
source_identity:
  inventory_blob: a3c8f557225a319a0f24c750a8ca5b939bf7e35b
  source_sha256: 7dcd445bdfe275e7b0521945ad4242aea3f3401dc0df848fb01c5bcb2fcfcbbd
  source_size_bytes: 5707
evidence_paths:
- archives/customer-attraction/tools/evidence/R-18-global-proof-incumbent-20261031/original/largest_incumbent_n3p6_best.json
- archives/customer-attraction/tools/evidence/R-18-global-proof-incumbent-20261031/comparisons/663827506601922a81a3.md
---

# R-18 最大incumbent候选：原完整SPE认证已撤回

本历史对象保原路径与稳定ID，记录一份被误标为完整SPE的旧候选；**它不是有效个体桥反例**。完整后续依据、客户表、根全部真实偏离、生成器缺行机制及新定义核验见[根激励遗漏审查](../审查/最大incumbent候选的根激励遗漏与错误认证--审查.md)。原5707B JSON及过去运行字节不改。

输入三人六主题、11个整数兴趣类型共963单位客户，确给全部43有序节点形式动作。实际023收益(375/2,579/2,273)，W750、OPT963，形式算术OPT/u0=642/125>5、half余537。这些数值本身不证明SPE。实际023只覆盖750，不是旧正文声称的“覆盖全部963”；最优无序支持为123或135。

按原同一策略强制根0…5，最终收益为(375/2,303,303,357,190,303)。五个替代均严格盈利；实际根并非最优，故无完整SPE，更不能反驳“每份SPE个体≥OPT/(2m−1)”或一般half。后继42节点合法也补不了根行。

源JSON的verified:true是生成器直接写入，不来自verify_canonical调用。生成器虽import该名却未调用，并在构造G时明确跳过空历史，只保后继行及最大主题容量。对G的有理恢复精确不等于对缺失根行精确验证。原源scope声称one full-history SPE应按错误声明保历史，不能当作认证。

真正个体桥后来由[银行完整SPE族](笛卡尔银行完整根菜单的低值自洽分布失败--反例.md)独立否定，不能借该真值倒填本旧输入有效。本例也不与父方四人/61客户incumbent proportional relay合并；二者合同、输入和证据不同。

本对象的原来源处置保历史，当前撤回错误数学认证并保失败原因；Root新审查按963个单位客户、43历史258含自身比较及216终局完整复核，恰五根负行。过去done的字段检查不是数学真实性证明，冻结证据及过去回执仍可恢复。
