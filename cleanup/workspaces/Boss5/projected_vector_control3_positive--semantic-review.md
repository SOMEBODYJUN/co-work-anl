---
source_id: 8984d363d1340f6c861d
source_path: examples/unrelated_machines/projected_vector_control3_positive.json
source_sha256: f76a2da028ca6088253e9e4be691389add76ba43d6c247786f09e80384982cab
status: ready-for-parent-review
recommended_disposition: integrated
recommended_target: archives/unrelated-machines/state/审查/向量贪心填充叉与累计路径冻结审计--审查.md
---

# 投影向量贪心三机正值输入夹具

## 输入合同

源是 `UM-PROJECTED-VECTOR-GREEDY-UNIT-COLLISION-v1` 相关三机正值实验的输入夹具。它有 3 台机器、323 件任务、目标峰值 1、12 个有理权重原子；`processing_times` 的三行长度均为 323，所有处理时间为正有理数。`distribution` 的权重按总和归一，`job_order` 为 0 到 322，未列边没有被隐式补成可用边。

夹具记录 `expected_assignment`、`expected_loads=(2579/966,0,1)`、12 个原子和 7 个事件块，并附 `OPT_certificate`：固定最后任务在每台机器处理时间为 1 给出下界，每个分布原子的 makespan 为 1 给出上界。因此输入层面只保存一个可核对的正值实例和其最优性见证，不是投影规则的生成器。

## 与既有运行和正文的关系

冻结 `projected_vector_greedy_audit.json` 已把该输入的 SHA-256、Fraction 审计命令和双路脚本写入证据包；其中三机 323 任务运行输出正是 `expected_loads`，并核对所有步骤严格完成。独立审计同时检查处理时间、原子概率、Gram/投影字段和边界拒绝；本次不重跑构造器，也不把夹具本身当作新的算法定理。

正式对象 `向量贪心、填充叉与累计路径冻结审计` 已承载三机正值、五机碰撞和固定顺序无界正文的量词关系。该输入只补齐三机正值实例的可复现源身份和哈希：它不改变“给定真实最优分布与固定顺序的有限证书”范围，也不否定重新耦合、交换投影或自适应调序的开放路线。

## 处置边界

将源标为 `integrated`，保存到 `projected-vector-padded-query-20261030` evidence 目录并链接正式审查。不得从 `expected_loads` 单独外推一般近似比、复杂度困难性或所有顺序失败；更不得与 customer-attraction 六人 half 模型混合。复现应使用冻结审计中列出的 Fraction 命令和同一源 SHA。
