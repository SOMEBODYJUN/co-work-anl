# 一般 half 的 harmonic / 末位删除重置子任务

2026-10-24；本区是个人探索备份，不自动提升共享数学状态。Q-CAG-HALF 仍 OPEN，无外审或世界新颖性认证。

## 当前可用结果

1. `last_deletion_one_counterexample.md`：完整21节点、35单位客户的纯 SPE 严格否定一般系数一末位删除重置候选 `max_T u_i(Z_T^-)<=u_i(Z)+u_m(Z)`。根实际返还恰为0；严格缺口来自偏离枝删除末位后的12单位返还。原福利与OPT都为35，故不是一般 half 反例。`audit_last_deletion_one.py` 逐单位客户检查全部84项原 SPE 比较和全部5个保留历史的因果删除，输出 `last_deletion_one_audit.json` 和完整 `last_deletion_one_certificate.json`。本稿作者审计已完成，其他代理独立复核状态由root另记。
2. `h4_reconstruction_and_refined_packet.md`：明确区分消息中的源定义与本子任务推测的 harmonic endpoint 定义；旧十三人 max-query 支付反例没有击穿推测H4，且其中每个最优元组都可以排序后留出至少3的H4余额。全packet的 `audit_h4_refined_packet.py` / `.json` 不依赖原发现器或缓存预期字段。

## 已停止的有限候选诊断

`probe_inferred_h4.py` / `.json` 只对既有六节点 portfolio matching 策略锥做一次候选专用LP；`perturb_refined_h4.py` / `.json` 只改变旧十三人packet原有八类型重数，保留同一完整自动机并用16状态DP处理所有最优排序。都没有正违反；这些浮点LP诊断不证明一般H4、一般half或新固定人数正面定理。后者没有保存精确对偶，因此不把负最优值写成已核准锥定理。root指示后已停止进一步H4负向扰动。

## 停止点与下一步

系数一重置已被明确辅助反例否定；系数二的一般逐客户上界由general_induction分支负责，不能将本例称其反例。下一步由root决定一般支付的新接口；本区不继续枚举特殊人数、扩张类或优化局部常数。
