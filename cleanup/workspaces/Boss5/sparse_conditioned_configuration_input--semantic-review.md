---
source_id: 43148c03f8be141c1526
source_path: examples/unrelated_machines/sparse_conditioned_configuration_input.json
source_sha256: c057fcf5bc2f3671c0ecd553405a721edceb53d74abaa26f257bb5bd2ebc4ee3
status: ready-for-parent-review
recommended_disposition: integrated
recommended_target: archives/unrelated-machines/state/审查/稀疏配置与强矩匹配双源增量审查--审查.md
---

# 稀疏深树条件配置输入夹具的语义清洗

## 来源身份与结构

冻结源为 `43148c03f8be141c1526`，路径为
`examples/unrelated_machines/sparse_conditioned_configuration_input.json`，两份冻结提交的内容相同，SHA-256 为
`c057fcf5bc2f3671c0ecd553405a721edceb53d74abaa26f257bb5bd2ebc4ee3`，大小 276615 字节。
JSON 顶层字段为 `title, k, H, gamma, threshold, infinity, machines, jobs`，其中
`k=3`, `H=5`, `gamma=1/8`, `threshold=4/3`，未列处理边表示无穷/不可用。

逐结构读取确认：`machines` 有 729 条，`jobs` 有 1051 条。机器标签由树/终端/共享汇点构成，任务处理时间是有限有理数；输入本身只给模型实例，不给配置证书、真实调度、策略动作或优化器结果。

## 与既有稀疏配置对象的关系

现有 `archives/unrelated-machines/state/审查/稀疏配置与强矩匹配双源增量审查--审查.md` 已承载同一稀疏深树对象的 canonical 定义、逐边配置合同、整数最优值 (2-1/k)、端点收缩条件和 (k=3,H=5) 的 2426 条有限边审计。既有 `sparse-transfer-20261030` evidence manifest 也已记录该输入 SHA、witness SHA、主/独立审计命令和冻结输出。

本输入夹具的独有内容是可复现的完整 729 机/1051 任务实例；它与主审计中的 2426 条有限边、forced mass 1、整数上界 (5/3)、sink 负载 (3/4) 一一对应。主审计的 Fraction 重放和符号正文分别承担有限核验与一般量词；不能把这个 JSON 直接当成逐边证书或一般配置算法。

## 量词与缺口

应保留的结论是：在声明的 (k=3,H=5) 输入上，它是稀疏深树条件配置合同的输入夹具；一般 (k,H) 族的证明由 canonical 正文承担；有限程序不替代证明。该合同允许每条边分别选择配置点，不要求跨边共同基点/联合分布/交叠机器一致性。因此它不单独给出真实调度共同相关性、通用 LP 分离算法、SA/SDP 层级下界或低于 2 的普遍近似比。

该对象属于 `unrelated-machines`，不与 customer-attraction 六人 SPE/共同目录目标合并。

## 建议处置

将源标为 `integrated`：

- 正式对象：既有稀疏配置与强矩匹配双源增量审查；
- 输入证据：`archives/unrelated-machines/tools/evidence/sparse-transfer-20261030/sparse_conditioned_configuration_input.json`；
- 版本/重放入口：`source-manifest.json` 及 `sparse-conditioned-{main,independent}-rerun.json`。

不新建数学对象、不把输入夹具误写成证明、不升级为 unrelated-machines 的一般结论或 customer-attraction 结论。
