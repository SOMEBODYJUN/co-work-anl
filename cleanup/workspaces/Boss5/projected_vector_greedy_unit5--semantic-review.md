---
source_id: 5ff9a119d94cf419d0ad
source_path: examples/unrelated_machines/projected_vector_greedy_unit5.json
source_sha256: 9818f23c6a9190f1cbe4a1f08aa761c4a063ee810925e057b4a6823d77af5222
status: ready-for-parent-review
recommended_disposition: integrated
recommended_target: archives/unrelated-machines/state/审查/固定阶与事件链向量贪心双源审查--审查.md
---

# `projected_vector_greedy_unit5.json` 语义清洗

## 来源身份与输入合同

冻结源是 `examples/unrelated_machines/projected_vector_greedy_unit5.json`，源 ID `5ff9a119d94cf419d0ad`，SHA-256 `9818f23c6a9190f1cbe4a1f08aa761c4a063ee810925e057b4a6823d77af5222`，2351 字节。两个冻结提交中的同路径内容相同。

输入声明 `um.projected-vector-greedy.unit.v1`：5 台 identical machines、5 个 jobs、目标处理上界 `T=1`，每个 job 在每台机器的处理时间均为 1；分布含 14 个 assignment atom，每个权重为 1，概率规则是按总权重归一化。`job_order` 是 0,1,2,3,4；`expected_assignment` 为 `[0,1,2,3,1]`。该 JSON 是输入夹具，不含算法实现、调度证明或全称结论。

## 与既有精确审计的对应

既有 `archives/unrelated-machines/tools/evidence/projected-vector-padded-query-20261030/projected_vector_greedy_audit.json` 已保存该输入 SHA、审计脚本 SHA 和 Fraction 运行范围。canonical Gram-inverse 路线的精确结果为：5 台机器、5 个 jobs、14 个 atoms、Gram 维数 12；5 步都严格选出，最小状态归一化间隙为

\[
60889883528620/1391369553599211>0.
\]

选出的 assignment 是 `[0,1,2,3,1]`，负载 `[1,2,1,1,0]`，makespan 为 2。审计中的 `max_support_makespan=1` 是分布支撑中每个源调度都满足的真实上界；贪心输出的 `makespan=2` 是该固定输入和固定顺序下的实际坏结果。另有独立 `vector_moment_greedy_independent.py --all-orders` 运行命令，不能把当前正文中的一般障碍误读成只对一个顺序成立，也不能把有限 all-orders 运行扩展为任意输入的算法定理。

同一 evidence 包另含 3 机、323 job 的正控制输入；它只用于区分严格正提升和 unit collision，不能与本 5×5 输入拼接为一个统一实例。

## 数学范围与处置

本源独有内容是可复现的 5×5 单位时间、14 原子真实最优分布输入；其数学结论由既有双源向量贪心审查和 Fraction 审计承载。它应标为 `integrated` 到 `固定阶与事件链向量贪心双源审查--审查.md`，并把源副本、SHA 与已有 `projected_vector_greedy_audit.json` 的输入映射补入 `projected-vector-padded-query-20261030` evidence manifest。

必须保留的边界：输入的 14 个支撑调度各自峰值为 1，但该源不自带“真实最优”证明；固定 Gram-inverse 审计给出本实例的有限严格碰撞结果，不证明任意固定阶、任意输入、任意任务顺序都失败。它属于 unrelated-machines 向量贪心对象，不进入 customer-attraction 六人 SPE/half 结论。

复现入口（既有 evidence 字段）为：

```sh
python3 tests/audits/unrelated_machines/projected_vector_greedy.py \
  examples/unrelated_machines/projected_vector_greedy_unit5.json \
  examples/unrelated_machines/projected_vector_control3_positive.json
python3 tests/audits/unrelated_machines/vector_moment_greedy_independent.py \
  examples/unrelated_machines/projected_vector_greedy_unit5.json --all-orders
```

本次完成了源输入逐字段阅读和与既有审计/正文的范围核对；没有修改正式 Git、没有 checkpoint、没有登记 `done`。
