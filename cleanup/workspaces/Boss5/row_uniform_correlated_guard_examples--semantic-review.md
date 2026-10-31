---
source_id: b8355ccd87a9b0cbb4d9
source_path: examples/unrelated_machines/row_uniform_correlated_guard_examples.json
source_sha256: ce29fad643077b4fb436db61152c2ab5c11a851403196b7184b9cdd2711bcf7e
status: ready-for-parent-review
recommended_disposition: integrated
recommended_target: archives/unrelated-machines/state/审查/全局基数与逐行均匀相关读出边界有限审查--审查.md
---

# 逐行均匀相关读出例子的语义清洗

## 来源身份和合同

该 JSON 是一个有限输入/结果夹具，标题说明它展示共享标签、奇数度、变化右度和空实例下的完整 `sigma` 与精确负载；源自身明确有限例子不替代一般证明。冻结源版本来自 `68fad804ec5946cb296f77dc5b336308a66abf12` 与 `aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c`，SHA-256 为 `ce29fad643077b4fb436db61152c2ab5c11a851403196b7184b9cdd2711bcf7e`，大小 11874 字节。

每个 example 同时保存二部图输入、标签、选中边、完整 `sigma`、各机器负载、makespan 与 moves；因此可作为既有 row-uniform 审计的源输入和有限回归记录。它不携带通用算法、优化器或全量最优性证明。

## 实际结构

源包含以下边界实例：

- `empty`：空边域，负载 0、makespan 0；
- `degree_zero`：只有左侧标签而无右点，完整 `sigma` 的两个孤立分支 makespan 1；
- `q_one_odd_degree`：一个左点、三个右点的奇数度例，均匀标签输出负载 (4/3,1,1)，makespan (4/3)；
- `frustrated_triangle`：三左三右、两标签共享边的三角例，输出 makespan (3/2)，并保存一次 moves；
- `varying_right_degrees`：右度不一致、三左六标签的完整输出，makespan (3/2)；
- `odd_left_degree`：左度为三的额外奇数边界。

这些字段支持逐任务回算和边界语义检查：选择是左点的共同标签，`selected_edges` 是真实共享子集，资源负载按每条关联边映射后的右资源汇总。不能把不同 example 的 `sigma` 拼成一个全局策略，也不能把一个 makespan 字段读成所有标签 profile 的最优值。

## 与既有正式对象的关系

现有 [全局基数与逐行均匀相关读出边界有限审查](../../../archives/unrelated-machines/state/审查/全局基数与逐行均匀相关读出边界有限审查--审查.md) 已承载 `UM-ROW-UNIFORM-CORRELATED-GUARD-HALF-RETENTION-v2` 的一般证明、平层 unrelated-machines 编译以及 `c7ca54100a256e0b0bd2` 的有限审计。该输入夹具补充的是四个完整调度枚举和奇数度/变化右度/空实例的明确源字节，不应另建第二个 row-uniform 对象。

既有审查中 frustrated-triangle 的独立枚举给出 OPT=3/2；`q_one_odd_degree` 的输出 (4/3) 与 OPT=1 说明该构造不是精确最优算法。源 JSON 本身没有这些独立枚举的证明字段，故这些数值应由对应审计证据承载，不能从夹具单独推出。

## 处置边界和接续

建议将源标记为 `integrated`：

1. 把源 SHA、两个冻结提交引用和输入副本加入 `row-count-uniform-20261030` 的 evidence manifest；
2. 在既有 row-count/uniform review 的 source_refs 或“有限输入”小节中注明六个 example 名称及其边界数值；
3. 保持与紧凑共享逃逸、heavy-matching、最优凸包和 customer-attraction 的模型分离。

后续若要扩大 row-uniform 结论，仍需证明非简单关联、非均匀原像、重复自查询或多次相关读出的合同；本输入夹具不覆盖这些量词，也不涉及 customer-attraction 六人 half 目标。
